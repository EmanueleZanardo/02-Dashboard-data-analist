"""Standalone test for calcola_event_study - tab158 (no streamlit)."""
import ast
import re
import datetime as dt
import numpy as np
import pandas as pd
from scipy.stats import norm

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np, "norm": norm}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_event_study":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_event_study = ns["calcola_event_study"]

fails = []
_nchecks = [0]


def check(name, cond):
    _nchecks[0] += 1
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def ore_hours(start, hours, price=50.0, tz=None):
    idx = pd.date_range(start, periods=hours, freq="h", tz=tz)
    return pd.Series(np.full(hours, price), index=idx)


def daily_price(start, day_prices, tz=None):
    """Serie oraria con prezzo costante per giorno (day_prices = lista)."""
    parts = []
    for i, px in enumerate(day_prices):
        parts.append(ore_hours(pd.Timestamp(start) + pd.Timedelta(days=i),
                               24, price=px, tz=tz))
    return pd.concat(parts)


def approx(a, b, tol=1e-6):
    return abs(float(a) - float(b)) <= tol


# ---------- caso base: 30gg a 50 pre, 30gg a 70 post ----------
s60 = daily_price("2025-01-01", [50.0] * 30 + [70.0] * 30)
r = calcola_event_study(s60, "2025-01-31", finestra_gg=30)
check("base valido", r["valido"] and r["errore"] is None)
check("base n_pre=30", r["n_pre"] == 30)
check("base n_post=30", r["n_post"] == 30)
check("base data_evento", r["data_evento"] == "2025-01-31")
check("base media_pre", approx(r["media_pre"], 50.0))
check("base media_post", approx(r["media_post"], 70.0))
check("base std zero", approx(r["std_pre"], 0.0) and approx(r["std_post"], 0.0))
check("base delta", approx(r["delta"], 20.0))
check("base delta_pct", approx(r["delta_pct"], 40.0))
check("base t_stat inf", np.isinf(r["t_stat"]) and r["t_stat"] > 0)
check("base p_value 0", approx(r["p_value"], 0.0))
check("base significativo", r["significativo"] is True)
check("base direzione", r["direzione"] == "rialzo")
check("base tabella 60 righe", len(r["tabella"]) == 60)
check("base tabella colonne", list(r["tabella"].columns) ==
      ["Giorno", "Periodo", "Prezzo medio (EUR/MWh)",
       "Scostamento da media pre (EUR/MWh)"])
check("base tabella periodi", (r["tabella"]["Periodo"] == "Pre").sum() == 30 and
      (r["tabella"]["Periodo"] == "Post").sum() == 30)
check("base scostamento post", approx(r["tabella"]["Scostamento da media pre (EUR/MWh)"].iloc[30], 20.0))
check("base verdetto non vuoto", isinstance(r["verdetto"], str) and len(r["verdetto"]) > 40)

# ---------- nessun cambiamento: piatto 50/50 ----------
snc = daily_price("2025-01-01", [50.0] * 60)
rn = calcola_event_study(snc, dt.date(2025, 1, 31), finestra_gg=30)
check("piatto valido", rn["valido"])
check("piatto delta 0", approx(rn["delta"], 0.0) and approx(rn["delta_pct"], 0.0))
check("piatto t=0", approx(rn["t_stat"], 0.0))
check("piatto p=1", approx(rn["p_value"], 1.0))
check("piatto non significativo", rn["significativo"] is False)
check("piatto direzione invariato", rn["direzione"] == "invariato")

# ---------- Welch calcolato a mano ----------
# pre: giorni [40, 60] -> m=50, s=14.1421 ; post: giorni [70, 90] -> m=80, s=14.1421
# den = 200/2 + 200/2 = 200 ; t = 30/sqrt(200) = 2.12132 ; p = 2*sf(2.12132) = 0.03389
sw = daily_price("2025-01-01", [40.0, 60.0, 70.0, 90.0])
rw = calcola_event_study(sw, "2025-01-03", finestra_gg=5, min_giorni=2)
check("welch valido", rw["valido"] and rw["n_pre"] == 2 and rw["n_post"] == 2)
check("welch media_pre", approx(rw["media_pre"], 50.0))
check("welch media_post", approx(rw["media_post"], 80.0))
check("welch t_stat", approx(rw["t_stat"], 2.1213203, tol=1e-4))
check("welch p_value", approx(rw["p_value"], 0.0338948, tol=1e-3))
check("welch significativo", rw["significativo"] is True)
check("welch direzione", rw["direzione"] == "rialzo")

# ---------- t = 0: pre [40,60], post [50,50] ----------
sz = daily_price("2025-01-01", [40.0, 60.0, 50.0, 50.0])
rz = calcola_event_study(sz, "2025-01-03", finestra_gg=5, min_giorni=2)
check("t0 valido", rz["valido"])
check("t0 t_stat 0", approx(rz["t_stat"], 0.0))
check("t0 p_value 1", approx(rz["p_value"], 1.0))
check("t0 non significativo", rz["significativo"] is False)

# ---------- ribasso ----------
srb = daily_price("2025-01-01", [80.0] * 20 + [60.0] * 20)
rrb = calcola_event_study(srb, "2025-01-21", finestra_gg=20)
check("ribasso valido", rrb["valido"])
check("ribasso delta -20", approx(rrb["delta"], -20.0))
check("ribasso direzione", rrb["direzione"] == "ribasso")
check("ribasso significativo", rrb["significativo"] is True)

# ---------- rumore senza shift: p in (0,1] ----------
rng = np.random.default_rng(7)
srn = daily_price("2025-01-01", list(50.0 + 5.0 * rng.standard_normal(40)))
rrn = calcola_event_study(srn, "2025-01-21", finestra_gg=20)
check("rumore valido", rrn["valido"])
check("rumore p in (0,1]", 0.0 < rrn["p_value"] <= 1.0)
check("rumore t finito", np.isfinite(rrn["t_stat"]))
check("rumore non significativo", rrn["significativo"] is False)

# ---------- data_evento come date e come Timestamp ----------
rd1 = calcola_event_study(s60, dt.date(2025, 1, 31), finestra_gg=30)
rd2 = calcola_event_study(s60, pd.Timestamp("2025-01-31"), finestra_gg=30)
check("date ok", rd1["valido"] and approx(rd1["media_post"], 70.0))
check("Timestamp ok", rd2["valido"] and approx(rd2["media_post"], 70.0))

# ---------- tz-aware reso naive, stessi risultati ----------
stz = daily_price("2025-01-01", [50.0] * 30 + [70.0] * 30, tz="Europe/Zurich")
rtz = calcola_event_study(stz, "2025-01-31", finestra_gg=30)
check("tz-aware valido", rtz["valido"])
check("tz-aware stesso delta", approx(rtz["delta"], r["delta"]))

# ---------- duplicati: keep first ----------
sdu = pd.concat([s60, s60.iloc[[0]]])
rdu = calcola_event_study(sdu, "2025-01-31", finestra_gg=30)
check("duplicati valido", rdu["valido"] and approx(rdu["media_pre"], 50.0))

# ---------- NaN orari: media giornaliera su ore valide ----------
sna = s60.copy()
sna.iloc[0:6] = np.nan
rna = calcola_event_study(sna, "2025-01-31", finestra_gg=30)
check("NaN valido", rna["valido"] and approx(rna["media_pre"], 50.0))

# ---------- casi di errore ----------
e1 = calcola_event_study(pd.Series([], dtype=float), "2025-01-31")
check("err serie vuota", not e1["valido"])
e2 = calcola_event_study(pd.Series([1.0, 2.0], index=[0, 1]), "2025-01-31")
check("err indice non datetime", not e2["valido"])
e3 = calcola_event_study(s60, None)
check("err evento None", not e3["valido"])
e4 = calcola_event_study(s60, "non una data")
check("err evento invalido", not e4["valido"])
e5 = calcola_event_study(s60, "2024-12-01")
check("err evento prima dei dati", not e5["valido"])
e6 = calcola_event_study(s60, "2025-05-01")
check("err evento dopo i dati", not e6["valido"])
e7 = calcola_event_study(s60, "2025-01-31", finestra_gg=3)
check("err finestra troppo piccola", not e7["valido"])
e8 = calcola_event_study(s60, "2025-01-31", finestra_gg=400)
check("err finestra troppo grande", not e8["valido"])
e9 = calcola_event_study(s60, "2025-01-31", finestra_gg="x")
check("err finestra non numerica", not e9["valido"])
e10 = calcola_event_study(s60, "2025-01-31", finestra_gg=30, min_giorni=1)
check("err min_giorni 1", not e10["valido"])
e11 = calcola_event_study(s60, "2025-01-31", finestra_gg=30, min_giorni=31)
check("err min_giorni > finestra", not e11["valido"])
# evento a ridosso dell'inizio: pre troppo corta
e12 = calcola_event_study(s60, "2025-01-03", finestra_gg=30, min_giorni=5)
check("err pre troppo corta", not e12["valido"])
# evento a ridosso della fine: post troppo corta
e13 = calcola_event_study(s60, "2025-02-28", finestra_gg=30, min_giorni=5)
check("err post troppo corta", not e13["valido"])
sall = pd.Series(np.full(48, np.nan),
                 index=pd.date_range("2025-01-01", periods=48, freq="h"))
e14 = calcola_event_study(sall, "2025-01-02")
check("err tutti NaN", not e14["valido"])
e15 = calcola_event_study(s60, "2025-01-31", min_giorni="x")
check("err min_giorni non numerico", not e15["valido"])

# ---------- determinismo ----------
ra = calcola_event_study(srn, "2025-01-21", finestra_gg=20)
rb = calcola_event_study(srn, "2025-01-21", finestra_gg=20)
check("deterministico", ra["verdetto"] == rb["verdetto"] and
      approx(ra["p_value"], rb["p_value"]) and
      ra["tabella"].equals(rb["tabella"]))

# ---------- registry tab158 ----------
n_with = len(re.findall(r"^\s*with tab158:", src, re.M))
check("un solo with tab158", n_with == 1)
m_decl = re.search(r"= st\.tabs\(\[\s*\"⏱️ Profilo giornaliero\"", src)
check("st.tabs trovata", m_decl is not None)
if m_decl is not None:
    lstart = src.rfind("\n", 0, m_decl.start()) + 1
    lend = src.find("\n", m_decl.end())
    decl = src[lstart:lend]
    lhs = re.findall(r"tab\d+", decl.split("= st.tabs", 1)[0])
    titles = re.findall(r'"([^"]+)"', decl.split("st.tabs([", 1)[1])
    check("158 variabili dichiarate", len(lhs) == 158 and "tab158" in lhs)
    check("158 titoli", len(titles) == 158)
    check("titolo tab158", "📍 Event study" in titles)
    check("titolo unico", titles.count("📍 Event study") == 1)
    check("nomi unici", len(lhs) == len(set(lhs)) and len(titles) == len(set(titles)))
else:
    check("158 variabili dichiarate", False)
    check("158 titoli", False)
    check("titolo tab158", False)
    check("titolo unico", False)
    check("nomi unici", False)
check("tab158 usata (decl+with)", len(re.findall(r"\btab158\b", src)) == 2)
keys = re.findall(r'key="(ev158_[^"]+)"', src)
check("chiavi widget uniche", len(keys) == len(set(keys)) and len(keys) >= 3)
check("helper a livello modulo",
      "calcola_event_study" in [n.name for n in tree.body if isinstance(n, ast.FunctionDef)])
check("nessun segreto hardcoded",
      not re.search(r'(?i)(api[_-]?key|password)\s*=\s*["\'][^"\']{8,}["\']', src))

print(f"\nchecks: {_nchecks[0]}, fails: {len(fails)}")
print("TUTTI I CHECK VERDI" if not fails else "FALLIMENTI: " + str(fails))
raise SystemExit(1 if fails else 0)
