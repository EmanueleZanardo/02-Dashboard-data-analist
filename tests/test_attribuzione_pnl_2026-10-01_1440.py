"""Test standalone tab129 'Attribuzione P&L'.

Estrae calcola_attribuzione_pnl da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_attribuzione_pnl_2026-10-01_1440.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_attribuzione_pnl":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
attr = ns["calcola_attribuzione_pnl"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


# --- 1. identita' contabile, ruolo vendita ---
r = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita")
check("valido base", r["valido"] and r["errore"] is None)
check("v0 vendita", abs(r["valore_0"] - 950000.0) < 1e-9, r["valore_0"])
check("v1 vendita", abs(r["valore_1"] - 1045000.0) < 1e-9, r["valore_1"])
check("effetto prezzo", abs(r["effetto_prezzo"] - 150000.0) < 1e-9,
      r["effetto_prezzo"])
check("effetto volume", abs(r["effetto_volume"] - (-47500.0)) < 1e-9,
      r["effetto_volume"])
check("effetto incrociato", abs(r["effetto_incrociato"] - (-7500.0)) < 1e-9,
      r["effetto_incrociato"])
somma = r["effetto_prezzo"] + r["effetto_volume"] + r["effetto_incrociato"]
check("somma = delta fisico", abs(somma - (r["valore_1"] - r["valore_0"])) < 1e-9,
      (somma, r["valore_1"] - r["valore_0"]))
check("residuo ~0", abs(r["residuo"]) < 1e-9, r["residuo"])
check("delta totale = delta fisico (no coperture)",
      abs(r["delta_totale"] - 95000.0) < 1e-9, r["delta_totale"])

# --- 2. ruolo acquisto: segno invertito ---
r2 = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="acquisto")
check("valido acquisto", r2["valido"])
check("v0 acquisto negativo", abs(r2["valore_0"] + 950000.0) < 1e-9,
      r2["valore_0"])
check("effetto prezzo acquisto negativo",
      abs(r2["effetto_prezzo"] + 150000.0) < 1e-9, r2["effetto_prezzo"])
check("identita' acquisto", abs(r2["residuo"]) < 1e-9, r2["residuo"])

# --- 3. linearita' nel delta prezzo ---
r3 = attr(95.0, 125.0, 10000.0, 9500.0, ruolo="vendita")
check("raddoppio delta prezzo -> raddoppio effetto prezzo",
      abs(r3["effetto_prezzo"] - 2 * r["effetto_prezzo"]) < 1e-9,
      (r3["effetto_prezzo"], r["effetto_prezzo"]))

# --- 4. coperture ---
cop_long = [{"nome": "F1", "fisso": 100.0, "volume": 5000.0,
             "lato": "acquisto"}]
r4 = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita", coperture=cop_long)
check("long sopra fisso positivo",
      abs(r4["effetto_coperture"] - 50000.0) < 1e-9, r4["effetto_coperture"])
check("dettaglio copertura", len(r4["coperture"]) == 1
      and abs(r4["coperture"][0]["contributo"] - 50000.0) < 1e-9)
check("delta totale con copertura",
      abs(r4["delta_totale"] - (95000.0 + 50000.0)) < 1e-9, r4["delta_totale"])
cop_short = [{"nome": "S1", "fisso": 100.0, "volume": 5000.0,
              "lato": "vendita"}]
r5 = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita", coperture=cop_short)
check("short sopra fisso negativo",
      abs(r5["effetto_coperture"] + 50000.0) < 1e-9, r5["effetto_coperture"])
r6 = attr(95.0, 90.0, 10000.0, 10000.0, ruolo="vendita", coperture=cop_long)
check("long sotto fisso negativo",
      abs(r6["effetto_coperture"] + 50000.0) < 1e-9, r6["effetto_coperture"])

# --- 5. effetto cambio ---
r7 = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita",
          usa_cambio=True, fx_0=0.95, fx_1=0.97)
val_eur_fine = r7["valore_1"] + r7["effetto_coperture"]
check("effetto cambio formula",
      abs(r7["effetto_cambio"] - val_eur_fine * 0.02) < 1e-6,
      r7["effetto_cambio"])
check("valore chf",
      abs(r7["valore_1_chf"] - val_eur_fine * 0.97) < 1e-6, r7["valore_1_chf"])
check("delta chf", abs(r7["delta_totale_chf"]
                       - (r7["valore_1_chf"] - r7["valore_0"] * 0.95)) < 1e-6,
      r7["delta_totale_chf"])
r7b = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita", usa_cambio=False)
check("senza cambio: effetto 0 e delta = eur",
      r7b["effetto_cambio"] == 0.0
      and abs(r7b["delta_totale_chf"] - r7b["delta_totale"]) < 1e-12)

# --- 6. budget ---
r8 = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita",
          budget_prezzo=98.0, budget_volume=10000.0)
vb = 98.0 * 10000.0
check("scostamento totale", abs(r8["scostamento_budget"]
                                - (1045000.0 - vb)) < 1e-9,
      r8["scostamento_budget"])
check("scostamento prezzo",
      abs(r8["scost_budget_prezzo"] - (110.0 - 98.0) * 9500.0) < 1e-9,
      r8["scost_budget_prezzo"])
check("scostamento volume",
      abs(r8["scost_budget_volume"] - (9500.0 - 10000.0) * 98.0) < 1e-9,
      r8["scost_budget_volume"])
res_bd = (r8["scostamento_budget"] - r8["scost_budget_prezzo"]
          - r8["scost_budget_volume"])
check("budget: decomposizione esatta (residuo 0)", abs(res_bd) < 1e-9, res_bd)
r8b = attr(95.0, 110.0, 10000.0, 9500.0, ruolo="vendita")
check("senza budget: None", r8b["scostamento_budget"] is None)

# --- 7. prezzi negativi ammessi (mercati elettrici) ---
r9 = attr(-20.0, 50.0, 1000.0, 1000.0, ruolo="vendita")
check("prezzi negativi ok", r9["valido"] and abs(r9["residuo"]) < 1e-9)

# --- 8. df waterfall ---
check("df 7 righe", len(r["df"]) == 7, len(r["df"]))
check("df colonne", list(r["df"].columns) == ["Componente", "EUR"],
      list(r["df"].columns))
check("df ultima riga = P&L totale",
      r["df"].iloc[-1]["Componente"] == "P&L totale"
      and abs(r["df"].iloc[-1]["EUR"] - r["delta_totale"]) < 1e-9)

# --- 9. NaN-safe: nessun raise, sempre 'errore' ---
cattivi = [
    ("x", 110.0, 10000.0, 9500.0, {}),
    (95.0, 110.0, -5.0, 9500.0, {}),
    (95.0, 110.0, 10000.0, 9500.0, {"ruolo": "pippo"}),
    (95.0, 110.0, 10000.0, 9500.0,
     {"coperture": [{"nome": "X", "fisso": 1, "volume": -3,
                     "lato": "acquisto"}]}),
    (95.0, 110.0, 10000.0, 9500.0,
     {"coperture": [{"nome": "X", "fisso": 1, "volume": 3,
                     "lato": "lato_sconosciuto"}]}),
    (95.0, 110.0, 10000.0, 9500.0,
     {"usa_cambio": True, "fx_0": 0.0, "fx_1": 1.0}),
    (95.0, 110.0, 10000.0, 9500.0,
     {"budget_prezzo": 90.0, "budget_volume": -1.0}),
    (1e9, 110.0, 10000.0, 9500.0, {}),
]
for i, (p0, p1, q0, q1, kw) in enumerate(cattivi):
    rr = attr(p0, p1, q0, q1, **kw)
    check(f"nan-safe caso {i}", (not rr["valido"]) and rr["errore"],
          (i, rr["valore_0"]))

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
