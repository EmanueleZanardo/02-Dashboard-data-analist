"""Test standalone tab146 'Potenza impegnata'.

Estrae calcola_ottimizza_potenza (+ _fascia_aeegsi) da app.py via AST
(niente Streamlit). Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_ottimizza_potenza_2026-10-02_0540.py
"""
import ast
import math
import os
import re

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
        "calcola_ottimizza_potenza", "_fascia_aeegsi"
    ):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fv = ns["calcola_ottimizza_potenza"]

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


# ---------- 1. Caso piatto, numeri calcolabili a mano ----------
# 48h a prezzo costante; mw F1=F2=F3=1.0 -> MW orari = 1.0 MW = 1000 kW;
# fattore_picco=1.0 -> picco mese = 1000 kW.
s = serie_ore("2026-01-01", [80.0] * 48)
r = fv(s, 1.0, 1.0, 1.0, 800.0, 3.0, 10.0, 1.0)
check("piatto: valido", r["valido"] is True, r.get("errore"))
check("piatto: n_ore", r["n_ore"] == 48, r["n_ore"])
check("piatto: picco_max", r["picco_max_kw"] == 1000.0, r["picco_max_kw"])
check("piatto: n_mesi", r["n_mesi"] == 1, r["n_mesi"])
# quota = 800*3 = 2400; penale = (1000-800)*10 = 2000; totale = 4400
check("piatto: costo_attuale", abs(r["costo_attuale"] - 4400.0) < 1e-6, r["costo_attuale"])
check("piatto: mensile totale", abs(r["mensile"]["Totale (€)"].iloc[0] - 4400.0) < 1e-6)
check("piatto: mensile penale", abs(r["mensile"]["Penale (€)"].iloc[0] - 2000.0) < 1e-6)
check("piatto: mesi_superamento", r["mesi_superamento"] == 1, r["mesi_superamento"])
# con penale 10 >> quota 3 l'ottimo deve essere >= picco (1000 kW)
check("piatto: ottimo >= picco", r["potenza_ottima_kw"] >= 1000.0, r["potenza_ottima_kw"])
check("piatto: categoria sottodimensionata", r["categoria"] == "sottodimensionata", r["categoria"])
check("piatto: risparmio_annuo = (4400-3000)*12", abs(r["risparmio_annuo"] - 16800.0) < 1e-6, r["risparmio_annuo"])
check("piatto: costo_ottimo 3000", abs(r["costo_ottimo"] - 3000.0) < 1e-6, r["costo_ottimo"])
check("piatto: verdetto menziona 1,000", "1,000" in r["verdetto"], r["verdetto"][:80])

# ---------- 2. Quota altissima -> ottimo al minimo (0.5 x picco) ----------
r2 = fv(s, 1.0, 1.0, 1.0, 800.0, 100.0, 10.0, 1.0)
check("quota alta: ottimo = 500 (0.5x picco)", r2["potenza_ottima_kw"] == 500.0, r2["potenza_ottima_kw"])
check("quota alta: categoria sovradimensionata", r2["categoria"] == "sovradimensionata", r2["categoria"])

# ---------- 3. Contrattuale sopra il picco -> nessuna penale ----------
r3 = fv(s, 1.0, 1.0, 1.0, 1500.0, 3.0, 10.0, 1.0)
check("sopra picco: penale 0", r3["mensile"]["Penale (€)"].sum() == 0.0)
check("sopra picco: mesi_superamento 0", r3["mesi_superamento"] == 0)
# costo_attuale = 1500*3 = 4500; ottimo con penale 10 vs quota 3 -> 1000 kW = 3000
check("sopra picco: categoria sovradimensionata", r3["categoria"] == "sovradimensionata", r3["categoria"])

# ---------- 4. Adeguata: penale 0 e quota 0 -> tutto a costo zero ----------
r4 = fv(s, 1.0, 1.0, 1.0, 1000.0, 0.0, 0.0, 1.0)
check("zero costi: costo_attuale 0", r4["costo_attuale"] == 0.0, r4["costo_attuale"])
check("zero costi: risparmio_annuo 0", r4["risparmio_annuo"] == 0.0, r4["risparmio_annuo"])

# ---------- 5. Due mesi, picchi diversi ----------
# 59 giorni dal 01/01/2026 = gennaio (31) + febbraio (28), 2026 non bisestile.
s5 = serie_ore("2026-01-01", [70.0] * 24 * 59)
r5 = fv(s5, 2.0, 1.0, 0.5, 1500.0, 3.0, 10.0, 1.05)
check("2 mesi: n_mesi 2", r5["n_mesi"] == 2, r5["n_mesi"])
check("2 mesi: mensile 2 righe", len(r5["mensile"]) == 2)
check("2 mesi: colonne mensile", list(r5["mensile"].columns) == ["Mese", "Picco (kW)", "Quota fissa (€)", "Penale (€)", "Totale (€)"])
check("2 mesi: totale = quota+penale", all(abs(r5["mensile"]["Totale (€)"] - r5["mensile"]["Quota fissa (€)"] - r5["mensile"]["Penale (€)"]) < 1e-6))
check("2 mesi: scansione non vuota", len(r5["scansione"]) > 40)
check("2 mesi: scansione colonne", list(r5["scansione"].columns) == ["Potenza (kW)", "Quota fissa (€)", "Penali (€)", "Totale (€)"])
check("2 mesi: ottimo = min scansione", abs(r5["costo_ottimo"] - r5["scansione"]["Totale (€)"].min()) < 1e-6)
check("2 mesi: fattore_picco applicato", r5["picco_max_kw"] == round(2000.0 * 1.05, 0), r5["picco_max_kw"])
check("2 mesi: risparmio_annuo = periodo*6", abs(r5["risparmio_annuo"] - r5["risparmio_periodo"] * 6.0) < 1e-6,
      (r5["risparmio_annuo"], r5["risparmio_periodo"]))

# ---------- 6. Errori puliti ----------
se = serie_ore("2026-01-01", [80.0] * 48)
e = fv(pd.Series([], dtype=float), 1, 1, 1, 800, 3, 10)
check("vuota: errore", e["valido"] is False and e["errore"], e.get("errore"))
check("vuota: mensile vuota con colonne", len(e["mensile"]) == 0 and len(e["mensile"].columns) == 5)
e = fv([1, 2, 3], 1, 1, 1, 800, 3, 10)
check("non-Series: errore", e["valido"] is False, e.get("errore"))
e = fv(pd.Series([1.0, 2.0], index=[0, 1]), 1, 1, 1, 800, 3, 10)
check("indice non-datetime: errore", e["valido"] is False, e.get("errore"))
e = fv(serie_ore("2026-01-01", [80.0] * 10), 1, 1, 1, 800, 3, 10)
check("<24h: errore", e["valido"] is False, e.get("errore"))
e = fv(se, 0.0, 0.0, 0.0, 800, 3, 10)
check("MW zero: errore", e["valido"] is False and "zero" in e["errore"], e.get("errore"))
e = fv(se, 1, 1, 1, 0.0, 3, 10)
check("p_contr 0: errore", e["valido"] is False, e.get("errore"))
e = fv(se, 1, 1, 1, -5.0, 3, 10)
check("p_contr negativa: errore", e["valido"] is False, e.get("errore"))
e = fv(se, 1, 1, 1, 800, -1.0, 10)
check("quota negativa: errore", e["valido"] is False, e.get("errore"))
e = fv(se, 1, 1, 1, 800, 3, -1.0)
check("penale negativa: errore", e["valido"] is False, e.get("errore"))
e = fv(se, 1, 1, 1, 800, 3, 10, 0.0)
check("fattore 0: errore", e["valido"] is False, e.get("errore"))
e = fv(se, 1, 1, 1, "abc", 3, 10)
check("p_contr non numerica: errore", e["valido"] is False, e.get("errore"))

# ---------- 7. NaN e tz-aware ----------
sn = serie_ore("2026-01-01", [80.0] * 30 + [np.nan] * 5 + [80.0] * 13)
rn = fv(sn, 1, 1, 1, 800, 3, 10, 1.0)
check("NaN: valido con 43 ore", rn["valido"] is True and rn["n_ore"] == 43, (rn["valido"], rn["n_ore"]))
stz = serie_ore("2026-01-01", [80.0] * 48, tz="Europe/Zurich")
rz = fv(stz, 1, 1, 1, 800, 3, 10, 1.0)
check("tz-aware: valido", rz["valido"] is True and rz["n_mesi"] == 1, rz.get("errore"))

# ---------- 8. Determinismo ----------
ra = fv(s5, 2.0, 1.0, 0.5, 1500.0, 3.0, 10.0, 1.05)
rb = fv(s5, 2.0, 1.0, 0.5, 1500.0, 3.0, 10.0, 1.05)
check("determinismo: ottimo uguale", ra["potenza_ottima_kw"] == rb["potenza_ottima_kw"])
check("determinismo: mensile uguale", ra["mensile"].equals(rb["mensile"]))

# ---------- 9. Registry tab146 in st.tabs (robusto: non dipende dal n. di tab) ----------
src = open(APP, encoding="utf-8").read()
mdecl = re.search(r"((?:tab\d+,\s*)+tab\d+)\s*=\s*st\.tabs\(\[", src)
decl_vars = set(re.findall(r"tab\d+", mdecl.group(1))) if mdecl else set()
check("registry: tab146 dichiarata", "tab146" in decl_vars)
j = src.find('"⚡ Potenza impegnata"')
check("registry: titolo presente", j != -1)
check("UI: with tab146 presente", "with tab146:" in src)

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
