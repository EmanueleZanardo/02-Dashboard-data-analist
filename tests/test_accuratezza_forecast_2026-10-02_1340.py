"""Standalone test for calcola_accuratezza_forecast + genera_forecast_naive - tab154 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_accuratezza_forecast", "genera_forecast_naive"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_accuratezza_forecast = ns["calcola_accuratezza_forecast"]
genera_forecast_naive = ns["genera_forecast_naive"]

fails = []
_nchecks = [0]
def check(name, cond):
    _nchecks[0] += 1
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def hours(vals, start="2025-01-06", tz=None):
    idx = pd.date_range(start, periods=len(vals), freq="h", tz=tz)
    return pd.Series(np.asarray(vals, dtype=float), index=idx, name="p")

# --- 1. numeri a mano: 4h, e = [1,-1,2,-2] ---
reali = hours([10.0, 20.0, 30.0, 40.0])
fc = hours([11.0, 19.0, 32.0, 38.0])
r = calcola_accuratezza_forecast(reali, fc, min_ore=4, top_n=2)
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_ore == 4", r["n_ore"] == 4)
check("mano: mae == 1.5", r["mae"] == 1.5)
check("mano: rmse == sqrt(2.5)", abs(r["rmse"] - np.sqrt(2.5)) < 1e-12)
check("mano: bias == 0.0", r["bias"] == 0.0)
check("mano: mape == 6.6667 %",
      abs(r["mape"] - ((0.1 + 0.05 + 2.0/30.0 + 0.05) / 4.0 * 100.0)) < 1e-9)
exp_corr = float(np.corrcoef([10, 20, 30, 40], [11, 19, 32, 38])[0, 1])
check("mano: correlazione coerente", abs(r["correlazione"] - exp_corr) < 1e-12)
check("mano: skill None (serie corta)", r["skill"] is None and r["mae_naive"] is None)
check("mano: std_errore == std([1,-1,2,-2])",
      abs(r["std_errore"] - float(np.std([1.0, -1.0, 2.0, -2.0]))) < 1e-12)
pr = r["profilo_orario"]
check("mano: profilo_orario 4 righe ore 0-3", list(pr["ora"]) == [0, 1, 2, 3])
check("mano: profilo err_medio == [1,-1,2,-2]",
      list(pr["err_medio"].round(9)) == [1.0, -1.0, 2.0, -2.0])
check("mano: profilo mae == [1,1,2,2]", list(pr["mae"].round(9)) == [1.0, 1.0, 2.0, 2.0])
pg = r["peggiori"]
check("mano: peggiori top2 = ore 2 e 3", list(pg["Timestamp"]) ==
      ["2025-01-06 02:00", "2025-01-06 03:00"])
check("mano: peggiori errori [2,-2]", list(pg["Errore"].round(9)) == [2.0, -2.0])
check("mano: tabella 9 righe x 2 col", r["tabella"].shape == (9, 2))
check("mano: verdetto senza distorsione", "senza distorsione sistematica" in r["verdetto"])

# --- 2. bias firmato ---
r2 = calcola_accuratezza_forecast(hours([10.0]*48), hours([15.0]*48), min_ore=24)
check("bias: mae == 5.0", r2["mae"] == 5.0)
check("bias: bias == +5.0", r2["bias"] == 5.0)
check("bias: verdetto sovrastima", "sovrastima sistematica" in r2["verdetto"])
r3 = calcola_accuratezza_forecast(hours([10.0]*48), hours([7.0]*48), min_ore=24)
check("bias: verdetto sottostima", "sottostima sistematica" in r3["verdetto"])

# --- 3. skill score: forecast perfetto vs naive ---
h = np.arange(72)
onda = 100.0 + 10.0 * np.sin(2 * np.pi * h / 24.0)
rp, fp = hours(onda), hours(onda)
r4 = calcola_accuratezza_forecast(rp, fp, min_ore=24)
check("skill: mae == 0.0", r4["mae"] == 0.0)
check("skill: skill == 1.0", r4["skill"] == 1.0)
check("skill: mae_naive > 0", r4["mae_naive"] > 0)
check("skill: verdetto batte benchmark", "batte il benchmark naive" in r4["verdetto"])
# forecast piatto peggio del naive su onda
r5 = calcola_accuratezza_forecast(rp, hours(np.full(72, 200.0)), min_ore=24)
check("skill: forecast piatto skill < 0", r5["skill"] is not None and r5["skill"] < 0)
check("skill: verdetto peggio del naive", "peggio del naive" in r5["verdetto"])

# --- 4. casi di errore ---
check("err: serie reale vuota", not calcola_accuratezza_forecast(
    pd.Series([], dtype=float), fc, min_ore=4)["valido"])
check("err: indice non datetime",
      not calcola_accuratezza_forecast(
          pd.Series([1.0, 2.0]), pd.Series([1.0, 2.0]), min_ore=2)["valido"])
check("err: valori non numerici",
      not calcola_accuratezza_forecast(
          pd.Series(["a", "b"], index=pd.date_range("2025-01-01", periods=2, freq="h")),
          fc, min_ore=2)["valido"])
check("err: poche ore in comune",
      not calcola_accuratezza_forecast(hours([1.0]*10), hours([1.0]*10), min_ore=24)["valido"])
check("err: min_ore = 0", not calcola_accuratezza_forecast(reali, fc, min_ore=0)["valido"])
check("err: top_n = 0", not calcola_accuratezza_forecast(reali, fc, min_ore=4, top_n=0)["valido"])
rz = calcola_accuratezza_forecast(hours([0.0]*48), hours([1.0]*48), min_ore=24)
check("zero: valido con reali a zero", rz["valido"])
check("zero: mape None", rz["mape"] is None)
rc = calcola_accuratezza_forecast(hours([5.0]*48), hours([5.0]*48), min_ore=24)
check("costante: correlazione None", rc["correlazione"] is None)

# --- 5. allineamento, NaN, tz ---
r6 = calcola_accuratezza_forecast(hours([10.0]*48), hours([11.0]*24, start="2025-01-07"), min_ore=4)
check("join: n_ore == 24 su indici disallineati", r6["n_ore"] == 24 and r6["valido"])
rn = hours([10.0]*48); rn.iloc[5] = np.nan
r7 = calcola_accuratezza_forecast(rn, hours([10.0]*48), min_ore=4)
check("NaN: scartati (47 ore)", r7["n_ore"] == 47)
r8 = calcola_accuratezza_forecast(hours([10.0]*48, tz="Europe/Zurich"),
                                  hours([10.0]*48, tz="Europe/Zurich"), min_ore=24)
check("tz-aware: valido", r8["valido"] and r8["n_ore"] == 48)

# --- 6. genera_forecast_naive ---
g1 = genera_forecast_naive(hours(np.arange(48, dtype=float)), metodo="lag24")
check("naive lag24: valido", g1["valido"])
check("naive lag24: prime 24 NaN", g1["forecast"].iloc[:24].isna().all())
check("naive lag24: fc[24] == reali[0]",
      g1["forecast"].iloc[24] == 0.0 and g1["forecast"].iloc[47] == 23.0)
g2 = genera_forecast_naive(hours(np.arange(200, dtype=float)), metodo="lag168")
check("naive lag168: fc[168] == reali[0]", g2["forecast"].iloc[168] == 0.0)
g3 = genera_forecast_naive(hours([10.0, 20.0, 30.0] + [0.0]*45), metodo="mm24")
check("naive mm24: fc[3] == media prime 3",
      abs(g3["forecast"].iloc[3] - 20.0) < 1e-12)
check("naive: metodo sconosciuto -> errore",
      not genera_forecast_naive(hours([1.0]*30), metodo="xyz")["valido"])
check("naive: serie vuota -> errore",
      not genera_forecast_naive(pd.Series([], dtype=float))["valido"])
check("naive: deterministico",
      genera_forecast_naive(hours([1.0]*50))["forecast"].equals(
          genera_forecast_naive(hours([1.0]*50))["forecast"]))

# --- 7. determinismo ---
ra = calcola_accuratezza_forecast(reali, fc, min_ore=4, top_n=2)
rb = calcola_accuratezza_forecast(reali, fc, min_ore=4, top_n=2)
check("determinismo: mae identico", ra["mae"] == rb["mae"])
check("determinismo: verdetto identico", ra["verdetto"] == rb["verdetto"])
check("determinismo: tabella identica", ra["tabella"].equals(rb["tabella"]))

# --- 8. registry tab154 ---
_decl = [l for l in src.splitlines() if "st.tabs(" in l and "tab1," in l]
check("registry: tab154 dichiarata",
      any("tab154" in l.split("= st.tabs(")[0] for l in _decl))
check("registry: titolo presente", '"🎯 Accuratezza forecast"' in src)
check("registry: with tab154 presente", "with tab154:" in src)
check("registry: helper chiamato nella UI",
      "calcola_accuratezza_forecast(prezzi, af_fc" in src)
check("registry: chiavi widget uniche",
      src.count('key="af154_') == 3 and src.count('key="csv_accuratezza_forecast"') == 1)
check("registry: helper a livello modulo",
      any(isinstance(n, ast.FunctionDef) and n.name == "calcola_accuratezza_forecast"
          for n in tree.body))

print(f"\nchecks: {_nchecks[0] - len(fails)}, fails: {len(fails)}")
if fails:
    print(fails)
    raise SystemExit(1)
print("TUTTI I CHECK VERDI")
