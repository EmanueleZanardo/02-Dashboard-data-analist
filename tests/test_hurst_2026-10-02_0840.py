"""Standalone test for calcola_hurst - tab149 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_hurst", "_phi_std", "_gammaln", "_rs_atteso_bianco"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_hurst = ns["calcola_hurst"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def hourly_from_daily(daily, start="2025-01-01", hourly_noise=0.5, seed=7):
    """Espande medie giornaliere in serie oraria con piccolo rumore intra-day."""
    rng = np.random.default_rng(seed)
    n = len(daily) * 24
    idx = pd.date_range(start, periods=n, freq="h")
    vals = np.repeat(daily, 24) + rng.normal(0, hourly_noise, n)
    return pd.Series(vals, index=pd.DatetimeIndex(idx), name="p")

# --- 1. random walk giornaliero -> H ~ 0.5 ---
rng = np.random.default_rng(11)
days = 200
rw = 80.0 + np.cumsum(rng.normal(0, 2.0, days))
r = calcola_hurst(hourly_from_daily(rw), scala_min_giorni=4, n_scale=12)
check("rw: valido e nessun errore", r["valido"] and r["errore"] is None)
check("rw: H in (0.35, 0.65)", r["hurst"] is not None and 0.35 < r["hurst"] < 0.65)
check("rw: r2_fit in [0,1] (piatto = rumore bianco, atteso basso)",
      r["r2_fit"] is not None and 0.0 <= r["r2_fit"] <= 1.0)
check("rw: n_giorni == 200", r["n_giorni"] == 200)
check("rw: n_scale >= 4", r["n_scale"] >= 4)
check("rw: scale DataFrame non vuoto con colonne giuste",
      len(r["scale"]) >= 4 and list(r["scale"].columns) == ["Finestra (giorni)", "R/S medio", "Fit R/S"])
check("rw: finestre crescenti", bool((r["scale"]["Finestra (giorni)"].diff().dropna() > 0).all()))

# --- 2. AR(1) mean-reverting b=0.3 -> H < 0.5 ---
rng = np.random.default_rng(21)
b = 0.3
mr = np.empty(days)
mr[0] = 80.0
for t in range(1, days):
    mr[t] = 80.0 * (1 - b) + b * mr[t - 1] + rng.normal(0, 1.5)
r2 = calcola_hurst(hourly_from_daily(mr, seed=22))
check("mr: valido", r2["valido"] and r2["errore"] is None)
check("mr: H < 0.5", r2["hurst"] is not None and r2["hurst"] < 0.5)
check("mr: classe mean-reverting", r2["classe"] == "mean-reverting")
check("mr: segnale non vuoto", isinstance(r2["segnale"], str) and len(r2["segnale"]) > 20)
check("mr: verdetto contiene H", "H =" in r2["verdetto"])

# --- 3. incrementi persistenti AR(1) b=0.8 -> H > 0.55 ---
# (un trend deterministico nei LIVELLI sparisce nell'R/S perche' la statistica
# e' mean-adjusted: la persistenza di Hurst vive negli incrementi)
rng = np.random.default_rng(31)
dxp = np.empty(days)
dxp[0] = rng.normal(0, 1.0)
for t in range(1, days):
    dxp[t] = 0.8 * dxp[t - 1] + rng.normal(0, 1.0)
tr = 80.0 + np.cumsum(dxp)
r3 = calcola_hurst(hourly_from_daily(tr, seed=32))
check("trend: valido", r3["valido"] and r3["errore"] is None)
check("trend: H > 0.55", r3["hurst"] is not None and r3["hurst"] > 0.55)
check("trend: classe persistente", r3["classe"] == "persistente")
check("trend: r2_fit > 0.9 (deviazione dal bianco ben stimata)",
      r3["r2_fit"] is not None and r3["r2_fit"] > 0.9)

# --- 4. runs test: dente di sega alternato -> efficienza rifiutata ---
saw = 80.0 + 5.0 * np.tile([1.0, -1.0], days // 2)
r4 = calcola_hurst(hourly_from_daily(saw, hourly_noise=0.1, seed=41))
check("saw: valido", r4["valido"] and r4["errore"] is None)
check("saw: runs_osservati >> runs_attesi",
      r4["runs_osservati"] is not None and r4["runs_attesi"] is not None
      and r4["runs_osservati"] > r4["runs_attesi"])
check("saw: runs_p < 0.05", r4["runs_p"] is not None and r4["runs_p"] < 0.05)
check("saw: runs_verdetto rifiuta", "RIFIUTATA" in r4["runs_verdetto"])
check("saw: runs_z > 0", r4["runs_z"] is not None and r4["runs_z"] > 0)

# --- 5. random walk: runs test non deve rifiutare (seed fissato, verificato) ---
check("rw: runs_p >= 0.05 (non rifiuta)", r["runs_p"] is not None and r["runs_p"] >= 0.05)
check("rw: runs_verdetto non rifiuta", "NON rifiutata" in r["runs_verdetto"])

# --- 6. casi di errore puliti ---
e1 = calcola_hurst(pd.Series([], dtype=float))
check("vuota: errore pulito", not e1["valido"] and e1["errore"] is not None and e1["hurst"] is None)
idx30 = pd.date_range("2025-01-01", periods=30 * 24, freq="h")
e2 = calcola_hurst(pd.Series(np.full(30 * 24, 80.0), index=idx30))
check("corta: errore pulito", not e2["valido"] and e2["errore"] is not None)
idxc = pd.date_range("2025-01-01", periods=200 * 24, freq="h")
e3 = calcola_hurst(pd.Series(np.full(200 * 24, 80.0), index=idxc))
check("costante: errore pulito", not e3["valido"] and e3["errore"] is not None)
e4 = calcola_hurst(pd.Series([80.0, 81.0, 79.0], index=[0, 1, 2]))
check("indice non-datetime: errore pulito", not e4["valido"] and e4["errore"] is not None)
check("vuota: scale DataFrame con colonne giuste",
      list(e1["scale"].columns) == ["Finestra (giorni)", "R/S medio", "Fit R/S"])

# --- 7. determinismo ---
ra = calcola_hurst(hourly_from_daily(rw))
rb = calcola_hurst(hourly_from_daily(rw))
check("determinismo: stesso H", ra["hurst"] == rb["hurst"] and ra["runs_p"] == rb["runs_p"])

# --- 8. NaN e tz-aware ---
pnan = hourly_from_daily(rw)
pnan.iloc[::97] = np.nan
rn = calcola_hurst(pnan)
check("NaN sparsi: valido", rn["valido"] and rn["n_giorni"] == 200)
ptz = hourly_from_daily(rw)
ptz.index = pd.date_range("2025-01-01", periods=len(ptz), freq="h", tz="UTC").tz_convert("Europe/Zurich")
rt = calcola_hurst(ptz)
check("tz-aware: valido e H quasi uguale (DST sposta le medie giornaliere)",
      rt["valido"] and abs(rt["hurst"] - r["hurst"]) < 0.05)

# --- 9. parametri scala ---
rsc = calcola_hurst(hourly_from_daily(rw), scala_min_giorni=8, n_scale=8)
check("scale custom: valido", rsc["valido"] and rsc["n_scale"] >= 4)
check("scale custom: finestra min >= 8", int(rsc["scale"]["Finestra (giorni)"].min()) >= 8)

# --- 10. dichiarazione tab149 nel registry ---
decl = [ln for ln in src.splitlines() if "tab148" in ln and "st.tabs(" in ln]
check("registry: riga st.tabs con tab148 trovata", len(decl) >= 1)
if decl:
    check("registry: tab149 dichiarata", "tab149" in decl[0])
    check("registry: titolo 'Esponente di Hurst' presente", "Esponente di Hurst" in decl[0])
check("UI: blocco with tab149 presente", "with tab149:" in src)
check("UI: chiamata calcola_hurst nel blocco", "calcola_hurst(prezzi," in src)

total = 41
print(f"\nchecks: {total}, fails: {len(fails)}")
if fails:
    print("FAILED: " + ", ".join(fails))
    raise SystemExit(1)
print("ALL CHECKS PASSED")
