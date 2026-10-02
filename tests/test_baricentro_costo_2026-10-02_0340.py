"""Test standalone tab144 'Baricentro del costo'.

Estrae calcola_baricentro_costo (+ helper interni) da app.py via AST
(niente Streamlit). Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_baricentro_costo_2026-10-02_0340.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
        "calcola_baricentro_costo", "_fascia_aeegsi", "_stat_circolari"
    ):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fv = ns["calcola_baricentro_costo"]
fascia = ns["_fascia_aeegsi"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_ore(inizio, valori, tz=None):
    idx = pd.date_range(inizio, periods=len(valori), freq="h", tz=tz)
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


# --- 1. Fasce AEEGSI ---
check("fascia lun 10 = F1", fascia(10, 0) == "F1", fascia(10, 0))
check("fascia lun 7 = F2", fascia(7, 0) == "F2", fascia(7, 0))
check("fascia lun 22 = F2", fascia(22, 0) == "F2", fascia(22, 0))
check("fascia lun 23 = F3", fascia(23, 0) == "F3", fascia(23, 0))
check("fascia dom 10 = F3", fascia(10, 6) == "F3", fascia(10, 6))
check("fascia sab 12 = F2", fascia(12, 5) == "F2", fascia(12, 5))
check("fascia sab 23 = F3", fascia(23, 5) == "F3", fascia(23, 5))

# --- 2. Prezzo piatto, solo F1 (lun+mar): baricentro 13:00 ---
s = serie_ore("2026-01-05", [100.0] * 48)  # 05/01/2026 = lunedi'
r = fv(s, 1.0, 0.0, 0.0)
check("F1 flat: no errore", r["errore"] is None, r["errore"])
check("F1 flat: valido", r["valido"] is True)
check("F1 flat: bary 13:00", r["baricentro_txt"] == "13:00", r["baricentro_txt"])
check("F1 flat: bary_ore ~13", abs(r["baricentro_ore"] - 13.0) < 0.01, r["baricentro_ore"])
check("F1 flat: disp ~3.29h", abs(r["dispersione_ore"] - 3.2872) < 0.01, r["dispersione_ore"])
check("F1 flat: quota centro 45.45%", abs(r["quota_centro_pct"] - 45.4545) < 0.01, r["quota_centro_pct"])
check("F1 flat: n_ore 48", r["n_ore"] == 48, r["n_ore"])
check("F1 flat: mwh 22", r["mwh_tot"] == 22.0, r["mwh_tot"])  # 11 ore F1 x 2 giorni
check("F1 flat: costo 2200", r["costo_tot"] == 2200.0, r["costo_tot"])
check("F1 flat: ore_negative 0", r["ore_negative"] == 0, r["ore_negative"])
check("F1 flat: per_ora 24 righe", len(r["per_ora"]) == 24, len(r["per_ora"]))
check("F1 flat: mensile 1 riga", len(r["mensile"]) == 1, len(r["mensile"]))
check("F1 flat: mensile bary 13:00", r["mensile"]["Baricentro"].iloc[0] == "13:00", r["mensile"]["Baricentro"].iloc[0])
check("F1 flat: mensile costo 2200", r["mensile"]["Costo (€)"].iloc[0] == 2200.0, r["mensile"]["Costo (€)"].iloc[0])

# --- 3. Wrap circolare: costo solo a 23 e 0 -> 23:30, non 11:30 ---
vals = [0.0] * 48
s2 = serie_ore("2026-01-05", vals)
s2 = s2.where(~((s2.index.hour == 23) | (s2.index.hour == 0)), 100.0)
r = fv(s2, 1.0, 1.0, 1.0)
check("wrap: no errore", r["errore"] is None, r["errore"])
check("wrap: bary 23:30", r["baricentro_txt"] == "23:30", r["baricentro_txt"])
check("wrap: disp 0.5h", abs(r["dispersione_ore"] - 0.5) < 0.01, r["dispersione_ore"])
check("wrap: quota centro 100%", r["quota_centro_pct"] == 100.0, r["quota_centro_pct"])

# --- 4. Prezzi tutti negativi -> errore ---
s3 = serie_ore("2026-01-05", [-10.0] * 48)
r = fv(s3, 1.0, 1.0, 1.0)
check("neg: errore", r["errore"] is not None)
check("neg: valido False", r["valido"] is False)
check("neg: per_ora vuoto", len(r["per_ora"]) == 0)

# --- 5. Serie vuota / indice non datetime / MW zero ---
r = fv(pd.Series([], dtype=float), 1.0, 1.0, 1.0)
check("vuota: errore", r["errore"] is not None and r["valido"] is False)
r = fv(pd.Series([1.0, 2.0, 3.0]), 1.0, 1.0, 1.0)
check("no-datetime: errore", r["errore"] is not None and r["valido"] is False)
r = fv(s, 0.0, 0.0, 0.0)
check("mw0: errore potenza", "potenza" in r["errore"], r["errore"])

# --- 6. Prezzi non numerici ignorati ---
s4 = pd.Series(["x", 100.0, 100.0, None] + [100.0] * 44, index=pd.date_range("2026-01-05", periods=48, freq="h"))
r = fv(s4, 1.0, 0.0, 0.0)
check("nonnum: no errore", r["errore"] is None, r["errore"])
check("nonnum: n_ore 46", r["n_ore"] == 46, r["n_ore"])

# --- 7. Due mesi: baricentro mensile si sposta ---
idx = pd.date_range("2026-01-05", periods=24 * 60, freq="h")  # ~2.5 mesi
p = pd.Series(100.0, index=idx)
r = fv(p, 1.0, 0.0, 0.0)   # tutto F1
r2 = fv(p, 0.0, 0.0, 1.0)  # tutto F3 (notte)
check("2mesi: mensile >= 2 righe", len(r["mensile"]) >= 2, len(r["mensile"]))
check("2mesi: bary F1 diverso da F3", r["baricentro_txt"] != r2["baricentro_txt"],
      f"{r['baricentro_txt']} vs {r2['baricentro_txt']}")

# --- 8. Quota % per_ora somma ~100 ---
r = fv(s, 1.0, 1.0, 1.0)
tot = r["per_ora"]["Quota %"].sum()
check("quote: somma ~100", abs(tot - 100.0) < 0.1, tot)
check("quote: colonne giuste", list(r["per_ora"].columns) == ["Ora", "Ore osservate", "Costo (€)", "Quota %"])
check("mensile: colonne giuste", list(r["mensile"].columns) == ["Mese", "Baricentro", "Dispersione (±h)", "Quota ±2h (%)", "Costo (€)"])

# --- 9. tz-aware non rompe il raggruppamento mensile ---
s5 = serie_ore("2026-01-05", [100.0] * 48, tz="Europe/Zurich")
r = fv(s5, 1.0, 0.0, 0.0)
check("tz: no errore", r["errore"] is None, r["errore"])
check("tz: bary 13:00", r["baricentro_txt"] == "13:00", r["baricentro_txt"])
check("tz: mensile 1 riga", len(r["mensile"]) == 1, len(r["mensile"]))

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
