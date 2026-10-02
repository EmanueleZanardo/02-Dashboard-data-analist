"""Test standalone tab145 'Energia reattiva'.

Estrae calcola_penalita_reattiva (+ _fascia_aeegsi) da app.py via AST
(niente Streamlit). Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_energia_reattiva_2026-10-02_0440.py
"""
import ast
import math
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
        "calcola_penalita_reattiva", "_fascia_aeegsi"
    ):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fv = ns["calcola_penalita_reattiva"]

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


def tanphi(c):
    return math.tan(math.acos(c))


# --- 1. Validazioni ---
r = fv(serie_ore("2026-01-05", [100.0] * 48), 1.0, 1.0, 1.0, 1.0)
check("cos_phi=1 -> errore", r["errore"] is not None and not r["valido"], r["errore"])
r = fv(serie_ore("2026-01-05", [100.0] * 48), 1.0, 1.0, 1.0, 0.0)
check("cos_phi=0 -> errore", r["errore"] is not None and not r["valido"], r["errore"])
r = fv(serie_ore("2026-01-05", [100.0] * 48), 1.0, 1.0, 1.0, 1.2)
check("cos_phi=1.2 -> errore", r["errore"] is not None and not r["valido"], r["errore"])
r = fv(serie_ore("2026-01-05", [100.0] * 48), 1.0, 1.0, 1.0, "xyz")
check("cos_phi non numerico -> errore", r["errore"] is not None and not r["valido"], r["errore"])
r = fv(serie_ore("2026-01-05", [100.0] * 48), 0.0, 0.0, 0.0, 0.85)
check("MW zero -> errore", r["errore"] is not None and not r["valido"], r["errore"])
r = fv(pd.Series([], dtype=float), 1.0, 1.0, 1.0, 0.85)
check("serie vuota -> errore", r["errore"] is not None and not r["valido"], r["errore"])
r = fv(pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2]), 1.0, 1.0, 1.0, 0.85)
check("indice non datetime -> errore", r["errore"] is not None and not r["valido"], r["errore"])

# --- 2. Caso piatto: 1 MW F1 per 48h (lun+mar 05-06/01/2026), cos_phi=0.95 ---
s = serie_ore("2026-01-05", [100.0] * 48)
r = fv(s, 1.0, 0.0, 0.0, 0.95)
check("flat 0.95: no errore", r["errore"] is None, r["errore"])
check("flat 0.95: valido", r["valido"] is True)
check("flat 0.95: n_ore 48", r["n_ore"] == 48, r["n_ore"])
check("flat 0.95: mwh 22", r["mwh_tot"] == 22.0, r["mwh_tot"])  # 11h F1 x 2 gg
atteso_ratio = round(tanphi(0.95) * 100.0, 1)
check("flat 0.95: rapporto", math.isclose(r["rapporto_medio_pct"], atteso_ratio, abs_tol=1e-9),
      (r["rapporto_medio_pct"], atteso_ratio))
check("flat 0.95: penale 0 (sotto 33%)", r["penale_tot"] == 0.0, r["penale_tot"])
check("flat 0.95: risparmio 0", r["risparmio_rifasamento"] == 0.0, r["risparmio_rifasamento"])
check("flat 0.95: mesi_penale 0", r["mesi_con_penale"] == 0, r["mesi_con_penale"])
check("flat 0.95: mensile 1 riga", len(r["mensile"]) == 1, len(r["mensile"]))
check("flat 0.95: colonne mensile", list(r["mensile"].columns) == [
    "Mese", "Attiva (kWh)", "Reattiva (kvarh)", "Rapporto %",
    "Eccedenza t1 (kvarh)", "Eccedenza t2 (kvarh)", "Penale (€)"],
    list(r["mensile"].columns))

# --- 3. cos_phi=0.80 -> tan=0.75, solo scaglione 1 ---
r = fv(s, 1.0, 0.0, 0.0, 0.80)
check("0.80: valido", r["valido"] is True)
check("0.80: tan_phi 0.75", math.isclose(r["tan_phi"], 0.75, rel_tol=1e-12), r["tan_phi"])
check("0.80: rapporto 75%", math.isclose(r["rapporto_medio_pct"], 75.0, rel_tol=1e-9),
      r["rapporto_medio_pct"])
ea = 22.0 * 1000.0
ecc1 = (0.75 - 0.33) * ea  # 9240 kvarh
pen_att = round(ecc1 * 0.008, 2)
check("0.80: penale", math.isclose(r["penale_tot"], pen_att, rel_tol=1e-9),
      (r["penale_tot"], pen_att))
mg = r["mensile"].iloc[0]
check("0.80: ecc1 mensile", math.isclose(mg["Eccedenza t1 (kvarh)"], round(ecc1), rel_tol=1e-9),
      mg["Eccedenza t1 (kvarh)"])
check("0.80: ecc2 mensile 0", mg["Eccedenza t2 (kvarh)"] == 0.0, mg["Eccedenza t2 (kvarh)"])
check("0.80: peggior mese 2026-01", r["peggior_mese"] == "2026-01", r["peggior_mese"])
check("0.80: penale_rifasata 0", r["penale_rifasata"] == 0.0, r["penale_rifasata"])
check("0.80: risparmio = penale", math.isclose(r["risparmio_rifasamento"], pen_att, rel_tol=1e-9),
      (r["risparmio_rifasamento"], pen_att))

# --- 4. cos_phi=0.70 -> entrambi gli scaglioni ---
r = fv(s, 1.0, 0.0, 0.0, 0.70)
tp = tanphi(0.70)
check("0.70: rapporto", math.isclose(r["rapporto_medio_pct"], round(tp * 100.0, 1), abs_tol=1e-9),
      r["rapporto_medio_pct"])
e1 = (0.75 - 0.33) * ea
e2 = (tp - 0.75) * ea
pen2 = round(e1 * 0.008 + e2 * 0.012, 2)
check("0.70: penale due scaglioni", math.isclose(r["penale_tot"], pen2, rel_tol=1e-9),
      (r["penale_tot"], pen2))
check("0.70: ecc2 > 0", r["mensile"].iloc[0]["Eccedenza t2 (kvarh)"] > 0.0)
check("0.70: risparmio = penale", math.isclose(r["risparmio_rifasamento"], pen2, rel_tol=1e-9),
      r["risparmio_rifasamento"])

# --- 5. Soglie/tariffe custom: soglia_t1=0.5, tariffa_t1=0.01 ---
r = fv(s, 1.0, 0.0, 0.0, 0.80, tariffa_t1=0.01, tariffa_t2=0.02,
       soglia_t1=0.5, soglia_t2=0.75)
pen_c = round((0.75 - 0.5) * ea * 0.01, 2)
check("custom: penale", math.isclose(r["penale_tot"], pen_c, rel_tol=1e-9),
      (r["penale_tot"], pen_c))

# --- 6. Robustezza dati ---
s_nan = serie_ore("2026-01-05", [100.0] * 24 + [np.nan] * 24)
r = fv(s_nan, 1.0, 0.0, 0.0, 0.80)
check("NaN: valido, n_ore 24", r["valido"] and r["n_ore"] == 24, (r["valido"], r["n_ore"]))
s_tz = serie_ore("2026-01-05", [100.0] * 48, tz="Europe/Zurich")
r = fv(s_tz, 1.0, 0.0, 0.0, 0.80)
check("tz-aware: valido", r["valido"] is True, r["errore"])
check("tz-aware: penale = naive", math.isclose(r["penale_tot"], pen_att, rel_tol=1e-9),
      r["penale_tot"])

# --- 7. Registrazione UI ---
src = open(APP, encoding="utf-8").read()
check("st.tabs: tab145 dichiarato", "tab143, tab144, tab145 = st.tabs([" in src)
check("st.tabs: titolo Energia reattiva", '"⚡ Energia reattiva"' in src)
check("blocco with tab145 presente", "with tab145:" in src)
check("helper chiamato in UI", "calcola_penalita_reattiva(prezzi," in src)

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
