"""Test standalone tab143 'Efficienza del fixing'.

Estrae calcola_efficienza_fixing da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_efficienza_fixing_2026-10-02_0240.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_efficienza_fixing":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fv = ns["calcola_efficienza_fixing"]

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


# --- 1. Prezzi costanti 50, fixing 50: battuto 100%, sovracosto 0 ---
s = serie_ore("2026-01-01", [50.0] * 48)
r = fv(s, 50.0)
check("cost50/fix50: no errore", r["errore"] is None, r["errore"])
check("cost50/fix50: valido", r["valido"] is True)
check("cost50/fix50: pct_battuto 100", r["pct_battuto"] == 100.0, r["pct_battuto"])
check("cost50/fix50: sovracosto_eur 0", r["sovracosto_eur"] == 0.0, r["sovracosto_eur"])
check("cost50/fix50: sovracosto_pct 0", r["sovracosto_pct"] == 0.0, r["sovracosto_pct"])
check("cost50/fix50: dist_min 0", r["dist_min"] == 0.0, r["dist_min"])
check("cost50/fix50: dist_max 0", r["dist_max"] == 0.0, r["dist_max"])
check("cost50/fix50: verdetto Eccellente", "Eccellente" in r["verdetto"], r["verdetto"])
check("cost50/fix50: n_ore 48", r["n_ore"] == 48, r["n_ore"])
check("cost50/fix50: mensile 1 riga", len(r["mensile"]) == 1, len(r["mensile"]))

# --- 2. Prezzi costanti 50, fixing 60: battuto 0%, caro ---
r = fv(s, 60.0)
check("cost50/fix60: pct_battuto 0", r["pct_battuto"] == 0.0, r["pct_battuto"])
check("cost50/fix60: sovracosto_eur 10", r["sovracosto_eur"] == 10.0, r["sovracosto_eur"])
check("cost50/fix60: sovracosto_pct 20", r["sovracosto_pct"] == 20.0, r["sovracosto_pct"])
check("cost50/fix60: verdetto Molto caro", "Molto caro" in r["verdetto"], r["verdetto"])
check("cost50/fix60: dist_min 10", r["dist_min"] == 10.0, r["dist_min"])

# --- 3. Serie crescente: statistiche corrette vs numpy ---
vals = np.linspace(40.0, 80.0, 240)
s = serie_ore("2026-03-01", vals)
r = fv(s, 60.0)
check("lin: media ok", r["media"] == round(float(vals.mean()), 2), r["media"])
check("lin: mediana ok", r["mediana"] == round(float(np.median(vals)), 2), r["mediana"])
check("lin: p10/p90 ok",
      r["p10"] == round(float(np.percentile(vals, 10)), 2)
      and r["p90"] == round(float(np.percentile(vals, 90)), 2),
      (r["p10"], r["p90"]))
check("lin: pct_battuto = quota >= 60",
      r["pct_battuto"] == round(float((vals >= 60.0).mean() * 100.0), 1),
      r["pct_battuto"])

# --- 4. Verdetti per fascia: costruisco pct_battuto note ---
def serie_bande(n_alto, n_basso):
    return serie_ore("2026-01-01", [100.0] * n_alto + [0.0] * n_basso)

r = fv(serie_bande(95, 5), 50.0)
check("bande: 95% -> Eccellente", "Eccellente" in r["verdetto"], r["verdetto"])
r = fv(serie_bande(70, 30), 50.0)
check("bande: 70% -> Buono", "Buono" in r["verdetto"] and "Molto" not in r["verdetto"],
      r["verdetto"])
r = fv(serie_bande(50, 50), 50.0)
check("bande: 50% -> Nella norma", "Nella norma" in r["verdetto"], r["verdetto"])
r = fv(serie_bande(30, 70), 50.0)
check("bande: 30% -> Caro", "Caro" in r["verdetto"] and "Molto" not in r["verdetto"],
      r["verdetto"])
r = fv(serie_bande(10, 90), 50.0)
check("bande: 10% -> Molto caro", "Molto caro" in r["verdetto"], r["verdetto"])

# --- 5. Errori di input ---
r = fv(s, 0.0)
check("fix0: errore", r["errore"] is not None and r["valido"] is False, r["errore"])
r = fv(s, -5.0)
check("fixneg: errore", r["errore"] is not None, r["errore"])
r = fv(s, "abc")
check("fixstr: errore", r["errore"] is not None, r["errore"])
r = fv(s, None)
check("fixnone: errore", r["errore"] is not None, r["errore"])
r = fv([1, 2, 3], 50.0)
check("non-series: errore", r["errore"] is not None, r["errore"])
r = fv(pd.Series([50.0] * 30, index=range(30)), 50.0)
check("indice non-datetime: errore", r["errore"] is not None, r["errore"])
r = fv(serie_ore("2026-01-01", [50.0] * 10), 50.0)
check("serie corta <24h: errore", r["errore"] is not None, r["errore"])
check("serie corta: mensile vuoto", len(r["mensile"]) == 0, len(r["mensile"]))
check("serie corta: n_ore 0", r["n_ore"] == 0, r["n_ore"])

# --- 6. Mensile: 60 giorni dal 1/1 -> 3 mesi, scarto coerente ---
s = serie_ore("2026-01-01", [50.0] * (60 * 24))
r = fv(s, 40.0)
check("mensile: 3 mesi", list(r["mensile"]["Mese"]) == ["2026-01", "2026-02", "2026-03"],
      str(list(r["mensile"]["Mese"])))
check("mensile: scarto = media - fix",
      bool(((r["mensile"]["Media €/MWh"] - 40.0).round(2)
            == r["mensile"]["Scarto vs fixing €/MWh"]).all()))
check("mensile: ore battute 100%", bool((r["mensile"]["Ore battute %"] == 100.0).all()))

# --- 7. NaN: nessun crash ---
s = serie_ore("2026-02-01", [50.0] * 72)
s.iloc[5:30] = np.nan
r = fv(s, 50.0)
check("nan: no errore", r["errore"] is None, r["errore"])
check("nan: n_ore 47", r["n_ore"] == 47, r["n_ore"])
check("nan: pct_battuto 100", r["pct_battuto"] == 100.0, r["pct_battuto"])

# --- 8. tz-aware: stesso risultato del naive ---
s_tz = serie_ore("2026-01-01", [50.0] * 48, tz="Europe/Zurich")
r_tz = fv(s_tz, 55.0)
r_na = fv(serie_ore("2026-01-01", [50.0] * 48), 55.0)
check("tz: pct uguale", r_tz["pct_battuto"] == r_na["pct_battuto"])
check("tz: mensile ok", len(r_tz["mensile"]) == 1, len(r_tz["mensile"]))

# --- 9. Fixing sotto il minimo: pct 100, distanze firmate ---
s = serie_ore("2026-01-01", [40.0, 60.0] * 24)
r = fv(s, 30.0)
check("fix<min: pct 100", r["pct_battuto"] == 100.0, r["pct_battuto"])
check("fix<min: dist_min -10", r["dist_min"] == -10.0, r["dist_min"])
check("fix<min: dist_max 30", r["dist_max"] == 30.0, r["dist_max"])
check("fix<min: sovracosto -20", r["sovracosto_eur"] == -20.0, r["sovracosto_eur"])

print(f"checks={checks} fails={len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
