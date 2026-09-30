"""Standalone test for calcola_confronto_tariffe (+ fascia_oraria) - tab115 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_confronto_tariffe", "fascia_oraria"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_confronto_tariffe = ns["calcola_confronto_tariffe"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"

# --- 1. Calcolo noto a mano: lunedi 2026-09-28, prezzo flat 100, mw 1/2/3 ---
idx = pd.date_range("2026-09-28", "2026-09-28 23:00", freq="h", tz=TZ)
p = pd.Series(np.full(len(idx), 100.0), index=idx)
r = calcola_confronto_tariffe(p, 1.0, 2.0, 3.0, 95.0, 120.0, 100.0, 80.0, 130.0, 90.0, 5.0, 90.0)
check("valido", r["valido"])
# lun: F1=11h (8-19), F2=5h (7-8,19-23), F3=8h -> energia = 11*1+5*2+8*3 = 45
check("mwh == 45", abs(r["mwh"] - 45.0) < 1e-9)
check("ore == 24", r["ore"] == 24)
c = {x["nome"]: x for x in r["righe"]}
check("spot = 4500", abs(c["Spot indicizzata"]["costo"] - 4500.0) < 1e-9)
check("flat = 4275", abs(c["Flat"]["costo"] - 4275.0) < 1e-9)
check("F1/F2/F3 = 4240", abs(c["F1/F2/F3"]["costo"] - 4240.0) < 1e-9)
check("peak/off = 4490", abs(c["Peak/Off-peak"]["costo"] - 4490.0) < 1e-9)
check("spot+spread = 4725", abs(c["Spot + spread"]["costo"] - 4725.0) < 1e-9)
check("cap = 4050", abs(c["Spot con cap"]["costo"] - 4050.0) < 1e-9)
check("migliore = Spot con cap", r["migliore"] == "Spot con cap")
check("peggiore = Spot + spread", r["peggiore"] == "Spot + spread")
check("risparmio_max = 675", abs(r["risparmio_max"] - 675.0) < 1e-9)
check("risparmio_pct = 675/4725*100", abs(r["risparmio_max_pct"] - 675.0 / 4725.0 * 100) < 1e-9)
check("righe ordinate per costo crescente", [x["costo"] for x in r["righe"]] == sorted(c[x["nome"]]["costo"] for x in r["righe"]))
check("prezzo_medio spot = 100", abs(c["Spot indicizzata"]["prezzo_medio"] - 100.0) < 1e-9)
check("risparmio vs peggiore migliore = risparmio_max", abs(c["Spot con cap"]["risparmio_vs_peggiore"] - 675.0) < 1e-9)
check("risparmio peggiore == 0", abs(c["Spot + spread"]["risparmio_vs_peggiore"]) < 1e-9)

# --- 2. Serie vuota -> non valido ---
r2 = calcola_confronto_tariffe(pd.Series([], dtype=float), 1, 1, 1, 95, 120, 100, 80, 130, 90, 2, 150)
check("serie vuota -> valido False", r2["valido"] is False)

# --- 3. Potenze tutte zero -> non valido ---
r3 = calcola_confronto_tariffe(p, 0, 0, 0, 95, 120, 100, 80, 130, 90, 2, 150)
check("mw zero -> valido False", r3["valido"] is False)

# --- 4. Potenza negativa trattata come 0 ---
r4 = calcola_confronto_tariffe(p, -5.0, 1.0, 1.0, 95, 120, 100, 80, 130, 90, 2, 150)
check("mw negativa ok, mwh = 13", r4["valido"] and abs(r4["mwh"] - (5 * 1 + 8 * 1)) < 1e-9)

# --- 5. Prezzi negativi non mandano in crash; cap gestito ---
idx5 = pd.date_range("2026-09-28", "2026-09-28 23:00", freq="h", tz=TZ)
p5 = pd.Series(np.where(idx5.hour < 12, -10.0, 50.0), index=idx5)
r5 = calcola_confronto_tariffe(p5, 1.0, 1.0, 1.0, 95, 120, 100, 80, 130, 90, 2, 150)
check("prezzi negativi valido", r5["valido"])
check("cap non sopra prezzi negativi", {x["nome"]: x for x in r5["righe"]}["Spot con cap"]["costo"] <= {x["nome"]: x for x in r5["righe"]}["Spot indicizzata"]["costo"] + 1e-9)

# --- 6. Spread 0 -> uguale a spot; cap altissimo -> uguale a spot ---
r6 = calcola_confronto_tariffe(p, 1.0, 1.0, 1.0, 95, 120, 100, 80, 130, 90, 0.0, 1e9)
c6 = {x["nome"]: x for x in r6["righe"]}
check("spread 0 == spot", abs(c6["Spot + spread"]["costo"] - c6["Spot indicizzata"]["costo"]) < 1e-9)
check("cap alto == spot", abs(c6["Spot con cap"]["costo"] - c6["Spot indicizzata"]["costo"]) < 1e-9)

# --- 7. Cap sotto tutti i prezzi -> prezzo = cap ---
r7 = calcola_confronto_tariffe(p, 1.0, 1.0, 1.0, 95, 120, 100, 80, 130, 90, 2, 60.0)
c7 = {x["nome"]: x for x in r7["righe"]}
check("cap 60 -> 24*60", abs(c7["Spot con cap"]["costo"] - 24 * 60.0) < 1e-9)

# --- 8. NaN scartati ---
pv = p.copy()
pv.iloc[0] = np.nan
r8 = calcola_confronto_tariffe(pv, 1.0, 2.0, 3.0, 95, 120, 100, 80, 130, 90, 5, 90)
check("NaN scartati, ore == 23", r8["valido"] and r8["ore"] == 23)

# --- 9. Domenica: tutto F3 (peak/off == F1/F2/F3 con soli prezzi F3) ---
idx9 = pd.date_range("2026-10-04", "2026-10-04 23:00", freq="h", tz=TZ)  # domenica
p9 = pd.Series(np.full(len(idx9), 70.0), index=idx9)
r9 = calcola_confronto_tariffe(p9, 1.0, 1.0, 1.0, 95, 120, 100, 80, 130, 90, 2, 150)
c9 = {x["nome"]: x for x in r9["righe"]}
check("domenica: F1/F2/F3 = 24*80", abs(c9["F1/F2/F3"]["costo"] - 24 * 80.0) < 1e-9)
check("domenica: peak/off = 24*90", abs(c9["Peak/Off-peak"]["costo"] - 24 * 90.0) < 1e-9)

# --- 10. Indice naive (tz-less) accettato ---
idx10 = pd.date_range("2026-09-28", "2026-09-28 23:00", freq="h")
p10 = pd.Series(np.full(len(idx10), 100.0), index=idx10)
r10 = calcola_confronto_tariffe(p10, 1.0, 1.0, 1.0, 95, 120, 100, 80, 130, 90, 2, 150)
check("tz-less ok", r10["valido"] and abs(r10["mwh"] - 24.0) < 1e-9)

# --- 11. Deterministico ---
ra = calcola_confronto_tariffe(p, 1.0, 2.0, 3.0, 95, 120, 100, 80, 130, 90, 5, 90)
rb = calcola_confronto_tariffe(p, 1.0, 2.0, 3.0, 95, 120, 100, 80, 130, 90, 5, 90)
check("deterministico", [x["costo"] for x in ra["righe"]] == [x["costo"] for x in rb["righe"]])

print("FAILURES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
