"""Standalone test for calcola_enpi - tab156 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_enpi", "fascia_oraria"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_enpi = ns["calcola_enpi"]

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


def approx(a, b, tol=1e-6):
    return abs(float(a) - float(b)) <= tol


# ---------- caso base: 2 mesi, prezzo piatto 50, MW=1/1/1 ----------
# gen 2025: 744h -> 744 MWh, 37200 EUR ; feb 2025: 672h -> 672 MWh, 33600 EUR
p2 = ore_hours("2025-01-01", 744 + 672)
prod2 = pd.Series([1000.0, 2000.0],
                  index=pd.PeriodIndex(["2025-01", "2025-02"], freq="M"))
r = calcola_enpi(p2, 1.0, 1.0, 1.0, produzione=prod2, baseline_mesi=1)
check("base valido", r["valido"] and r["errore"] is None)
check("base n_mesi=2", r["n_mesi"] == 2)
check("base mesi", r["mesi"] == ["2025-01", "2025-02"])
check("base energia", approx(r["energia_mwh"][0], 744.0) and approx(r["energia_mwh"][1], 672.0))
check("base costo", approx(r["costo_eur"][0], 37200.0) and approx(r["costo_eur"][1], 33600.0))
check("base kwh_unita", approx(r["kwh_unita"][0], 744.0) and approx(r["kwh_unita"][1], 336.0))
check("base eur_unita", approx(r["eur_unita"][0], 37.2) and approx(r["eur_unita"][1], 16.8))
check("base baseline=744", approx(r["baseline_kwh_unita"], 744.0))
check("base miglioramento ultimo", approx(r["miglioramento_ultimo_pct"], (744 - 336) / 744 * 100))
check("base r2 None con 2 mesi", r["r2"] is None and r["base_mwh_mese"] is None)
check("base tabella colonne", list(r["tabella"].columns) ==
      ["Mese", "Produzione", "Energia (MWh)", "Costo (EUR)",
       "kWh/unita'", "EUR/unita'", "Scost. vs baseline (%)"])
check("base tabella 2 righe", len(r["tabella"]) == 2)
check("base verdetto non vuoto", isinstance(r["verdetto"], str) and len(r["verdetto"]) > 20)

# ---------- OLS esatta: energia = 100 + 2*vol ----------
# MW piatto 1 -> energia_mese = ore del mese: gen744 feb672 mar744 apr720
p4 = ore_hours("2025-01-01", 744 + 672 + 744 + 720, price=10.0)
ene4 = np.array([744.0, 672.0, 744.0, 720.0])
vol4 = (ene4 - 100.0) / 2.0  # [322, 286, 322, 310]
prod4 = pd.Series(vol4, index=pd.PeriodIndex(["2025-01", "2025-02", "2025-03", "2025-04"], freq="M"))
r4 = calcola_enpi(p4, 1.0, 1.0, 1.0, produzione=prod4, baseline_mesi=2)
check("ols valido", r4["valido"])
check("ols a=100", approx(r4["base_mwh_mese"], 100.0, tol=1e-4))
check("ols b=2000 kWh/unita'", approx(r4["kwh_marginale_unita"], 2000.0, tol=1e-3))
check("ols r2=1", approx(r4["r2"], 1.0, tol=1e-9))
check("ols quota_fissa", approx(r4["quota_fissa_pct"], 100.0 / ene4.mean() * 100, tol=1e-6))
check("ols baseline media primi 2", approx(r4["baseline_kwh_unita"],
      float(np.mean(ene4[:2] * 1000.0 / vol4[:2]))))
check("ols scost baseline NaN primi 2",
      r4["tabella"]["Scost. vs baseline (%)"].iloc[:2].isna().all())
check("ols miglioramento ultimo finita", np.isfinite(r4["miglioramento_ultimo_pct"]))

# ---------- input dict ----------
r_dict = calcola_enpi(p2, 1, 1, 1, produzione={"2025-01": 1000.0, "2025-02": 2000.0},
                      baseline_mesi=1)
check("dict valido", r_dict["valido"] and approx(r_dict["kwh_unita"][1], 336.0))

# ---------- input DataFrame (stringhe mese) ----------
df_prod = pd.DataFrame({"mese": ["2025-01", "2025-02"], "vol": [1000.0, 2000.0]})
r_df = calcola_enpi(p2, 1, 1, 1, produzione=df_prod, baseline_mesi=1)
check("dataframe valido", r_df["valido"] and approx(r_df["kwh_unita"][0], 744.0))

# ---------- mesi duplicati sommati ----------
prod_dup = pd.Series([500.0, 500.0, 2000.0],
                     index=pd.PeriodIndex(["2025-01", "2025-01", "2025-02"], freq="M"))
r_dup = calcola_enpi(p2, 1, 1, 1, produzione=prod_dup, baseline_mesi=1)
check("duplicati sommati", r_dup["valido"] and approx(r_dup["volumi"][0], 1000.0))

# ---------- produzione con datetime index ----------
prod_dt = pd.Series([1000.0, 2000.0],
                    index=pd.to_datetime(["2025-01-15", "2025-02-20"]))
r_dt = calcola_enpi(p2, 1, 1, 1, produzione=prod_dt, baseline_mesi=1)
check("datetime index ok", r_dt["valido"] and r_dt["mesi"] == ["2025-01", "2025-02"])

# ---------- tz-aware ----------
p_tz = ore_hours("2025-01-01", 744 + 672, tz="Europe/Zurich")
r_tz = calcola_enpi(p_tz, 1, 1, 1, produzione=prod2, baseline_mesi=1)
check("tz-aware ok", r_tz["valido"] and r_tz["n_mesi"] == 2)

# ---------- NaN nei prezzi ----------
p_nan = p2.copy()
p_nan.iloc[0:10] = np.nan
r_nan = calcola_enpi(p_nan, 1, 1, 1, produzione=prod2, baseline_mesi=1)
check("NaN prezzi scartati", r_nan["valido"] and r_nan["energia_mwh"][0] < 744.0)

# ---------- quota fissa clippata a 100 ----------
# energia decrescente con vol: intercetta > media -> clip
p3 = ore_hours("2025-01-01", 744 + 672 + 744, price=10.0)
ene3 = np.array([744.0, 672.0, 744.0])
vol3 = np.array([1000.0, 2000.0, 3000.0])
# forza energia decrescente via MW diversi per mese: non possibile con profilo unico,
# quindi test diretto del clip: usa volumi tali che a > media
r3 = calcola_enpi(p3, 1, 1, 1,
                  produzione=pd.Series(vol3,
                                       index=pd.PeriodIndex(["2025-01", "2025-02", "2025-03"], freq="M")),
                  baseline_mesi=1)
check("clip quota_fissa in [0,100]",
      r3["quota_fissa_pct"] is not None and 0.0 <= r3["quota_fissa_pct"] <= 100.0)

# ---------- volumi costanti -> r2 None ----------
prod_flat = pd.Series([1000.0, 1000.0, 1000.0],
                      index=pd.PeriodIndex(["2025-01", "2025-02", "2025-03"], freq="M"))
r_flat = calcola_enpi(p3, 1, 1, 1, produzione=prod_flat)
check("volumi costanti -> r2 None", r_flat["valido"] and r_flat["r2"] is None)

# ---------- baseline_mesi > n troncato ----------
r_big = calcola_enpi(p2, 1, 1, 1, produzione=prod2, baseline_mesi=99)
check("baseline troncata", r_big["valido"] and
      approx(r_big["baseline_kwh_unita"], float(np.mean([744.0, 336.0]))))
check("nessun mese oltre baseline -> miglioramento None",
      r_big["miglioramento_ultimo_pct"] is None)

# ---------- casi di errore ----------
e1 = calcola_enpi(p2, 1, 1, 1, produzione=None)
check("err produzione None", not e1["valido"] and "Produzione" in e1["errore"])
e2 = calcola_enpi(pd.Series([], dtype=float), 1, 1, 1, produzione=prod2)
check("err prezzi vuoti", not e2["valido"])
e3 = calcola_enpi(pd.Series([1.0, 2.0], index=[0, 1]), 1, 1, 1, produzione=prod2)
check("err indice non datetime", not e3["valido"])
e4 = calcola_enpi(p2, 0, 0, 0, produzione=prod2)
check("err MW nulli", not e4["valido"])
e5 = calcola_enpi(p2, 1, 1, 1,
                  produzione=pd.Series([0.0, -5.0],
                                       index=pd.PeriodIndex(["2025-01", "2025-02"], freq="M")))
check("err produzione non positiva", not e5["valido"])
e6 = calcola_enpi(p2, 1, 1, 1,
                  produzione=pd.Series([1000.0],
                                       index=pd.PeriodIndex(["2025-01"], freq="M")))
check("err un solo mese", not e6["valido"] and "2 mesi" in e6["errore"])
e7 = calcola_enpi(p2, 1, 1, 1,
                  produzione=pd.Series([1000.0, 2000.0],
                                       index=pd.PeriodIndex(["2024-01", "2024-02"], freq="M")))
check("err mesi fuori periodo", not e7["valido"])
e8 = calcola_enpi(p2, "x", 1, 1, produzione=prod2)
check("err MW non numerici", not e8["valido"])
e9 = calcola_enpi(p2, 1, 1, 1, produzione=[1, 2, 3])
check("err formato produzione", not e9["valido"])

# ---------- determinismo ----------
ra = calcola_enpi(p4, 1, 1, 1, produzione=prod4, baseline_mesi=2)
rb = calcola_enpi(p4, 1, 1, 1, produzione=prod4, baseline_mesi=2)
check("deterministico", ra["verdetto"] == rb["verdetto"] and
      np.array_equal(ra["kwh_unita"], rb["kwh_unita"], equal_nan=True))

# ---------- registry tab156 ----------
import re
n_with = len(re.findall(r"^\s*with tab156:", src, re.M))
check("un solo with tab156", n_with == 1)
m_tabs = re.search(r"= st\.tabs\(\[\s*\"⏱️ Profilo giornaliero\"", src)
check("st.tabs trovata", m_tabs is not None)
if m_tabs is not None:
    lstart = src.rfind("\n", 0, m_tabs.start()) + 1
    lend = src.find("\n", m_tabs.end())
    decl = src[lstart:lend]
    lhs = re.findall(r"tab\d+", decl.split("= st.tabs", 1)[0])
    check("tab156 tra le variabili dichiarate", "tab156" in lhs and len(lhs) == len(re.findall(r'"([^"]+)"', decl.split("st.tabs([", 1)[1])))
    labels = re.findall(r'"([^"]+)"', decl.split("st.tabs([", 1)[1])
else:
    labels = []
check("n titoli = n variabili", len(labels) == len(re.findall(r"tab\d+", decl.split("= st.tabs", 1)[0])) and len(labels) > 0)
check("titolo tab156", "📏 EnPI energetico" in labels)
check("titolo unico", labels.count("📏 EnPI energetico") == 1)
vars_decl = re.findall(r"\btab156\b", src)
check("tab156 usata (decl+with)", len(vars_decl) == 2)
keys = re.findall(r'key="(enpi156_[^"]+)"', src)
check("chiavi widget uniche", len(keys) == len(set(keys)) and len(keys) >= 7)
check("helper a livello modulo",
      "calcola_enpi" in [n.name for n in tree.body if isinstance(n, ast.FunctionDef)])
check("nessun segreto hardcoded",
      not re.search(r'(?i)(api[_-]?key|password)\s*=\s*["\'][^"\']{8,}["\']', src))

print(f"\nchecks: {_nchecks[0]}, fails: {len(fails)}")
print("TUTTI I CHECK VERDI" if not fails else "FALLIMENTI: " + str(fails))
raise SystemExit(1 if fails else 0)
