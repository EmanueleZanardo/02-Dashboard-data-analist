"""Test standalone tab136 'Effetto festivita''.

Estrae calcola_effetto_festivita da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_effetto_festivita_2026-10-01_1840.py
"""
import ast
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_effetto_festivita":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
ef = ns["calcola_effetto_festivita"]

E = "\u20ac/MWh"
COL_PM = "Prezzo medio (" + E + ")"
COL_SC = "Sconto vs feriale (" + E + ")"
COL_SCP = "Sconto vs feriale (%)"
COL_OSC = "Sconto (" + E + ")"

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_gen_feb(p_fest=60.0, p_fer=100.0):
    # 2026-01-01 -> 2026-03-01 orari: festivi CH-TI = 01-01, 06-01
    idx = pd.date_range("2026-01-01", "2026-03-01", freq="h", inclusive="left")
    festivi = {date(2026, 1, 1), date(2026, 1, 6)}
    vals = np.where([d.date() in festivi for d in idx], p_fest, p_fer).astype(float)
    return pd.Series(vals, index=idx)


# --- caso base: 2 festivita' CH-TI ---
r = ef(serie_gen_feb(), paese="CH-TI")
check("ok base", r["ok"], r["motivo"])
check("n_festivita == 2", r["n_festivita"] == 2, r["n_festivita"])
check("pm feriale 100", r["prezzo_medio_feriale"] == 100.0, r["prezzo_medio_feriale"])
check("pm festivo 60", r["prezzo_medio_festivo"] == 60.0, r["prezzo_medio_festivo"])
check("sconto 40 eur", r["sconto_medio_eur"] == 40.0, r["sconto_medio_eur"])
check("sconto 40 pct", r["sconto_medio_pct"] == 40.0, r["sconto_medio_pct"])
check("weekend classificato", r["n_giorni_weekend"] > 0, r["n_giorni_weekend"])
check("feriali classificati", r["n_giorni_feriali"] > 0, r["n_giorni_feriali"])
df = r["df_festivita"]
check("df 2 righe", len(df) == 2, len(df))
check("df ordinata per sconto desc",
      list(df[COL_SC].values) == sorted(df[COL_SC].values, reverse=True))
check("festa piu scontata = Capodanno (stabile a pari sconto)",
      r["data_festa_piu_scontata"] == "2026-01-01", r["data_festa_piu_scontata"])
check("nomi festivita'",
      set(df["Festivit\u00e0"].values) == {"Capodanno", "Epifania"},
      list(df["Festivit\u00e0"].values))
dfo = r["df_orario"]
check("df_orario 24 righe", len(dfo) == 24, len(dfo))
check("sconto orario uniforme 40",
      (dfo[COL_OSC].fillna(-1) == 40.0).all())
check("ora_sconto_max valida", r["ora_sconto_max"] == 0, r["ora_sconto_max"])
check("sconto_max_orario 40", r["sconto_max_orario"] == 40.0, r["sconto_max_orario"])

# --- profilo di consumo ---
r2 = ef(serie_gen_feb(), paese="CH-TI", mw_fasce={"F1": 1.0, "F2": 1.0, "F3": 1.0})
check("ok profilo", r2["ok"])
check("energia festiva 48 MWh", r2["energia_festiva_mwh"] == 48.0, r2["energia_festiva_mwh"])
check("costo festivo 2880", r2["costo_festivo_profilo"] == 2870.0, r2["costo_festivo_profilo"])
check("costo riferimento 4800", r2["costo_riferimento_profilo"] == 4800.0, r2["costo_riferimento_profilo"])
check("risparmio 1920", r2["risparmio_profilo_eur"] == 1920.0, r2["risparmio_profilo_eur"])
check("risparmio 40%", r2["risparmio_profilo_pct"] == 40.0, r2["risparmio_profilo_pct"])
r2b = ef(serie_gen_feb(), paese="CH-TI", mw_fasce={"F1": 0.0, "F2": 0.0, "F3": 0.0})
check("profilo nullo -> risparmio None", r2b["risparmio_profilo_eur"] is None)
r2c = ef(serie_gen_feb(), paese="CH-TI")
check("senza mw_fasce -> risparmio None", r2c["risparmio_profilo_eur"] is None)

# --- Pasqua 2026: Ven Santo 03-04 e Pasquetta 06-04 (algoritmo mobile) ---
idx = pd.date_range("2026-04-01", "2026-04-16", freq="h", inclusive="left")
fest_p = {date(2026, 4, 3), date(2026, 4, 6)}
vals = np.where([d.date() in fest_p for d in idx], 50.0, 100.0)
rp = ef(pd.Series(vals, index=idx), paese="CH-TI")
check("pasqua ok", rp["ok"], rp["motivo"])
check("2 festivita' pasquali", rp["n_festivita"] == 2, rp["n_festivita"])
nomi = dict(zip(rp["df_festivita"]["Data"].astype(str), rp["df_festivita"]["Festivit\u00e0"]))
check("Venerdi' Santo 03-04", nomi.get("2026-04-03") == "Venerd\u00ec Santo", nomi)
check("Lunedi' dell'Angelo 06-04", nomi.get("2026-04-06") == "Luned\u00ec dell'Angelo", nomi)

# --- IT vs CH-TI: 25-04 e 01-05 solo in IT ---
idx2 = pd.date_range("2026-04-20", "2026-05-06", freq="h", inclusive="left")
s2 = pd.Series(100.0, index=idx2)
rit = ef(s2, paese="IT")
check("IT ok", rit["ok"], rit["motivo"])
check("IT 2 festivita' (25-04, 01-05)", rit["n_festivita"] == 2, rit["n_festivita"])
rch = ef(s2, paese="CH-TI")
check("CH-TI nessuna festivita' nel periodo -> ok False", not rch["ok"], rch["motivo"])
rch2 = ef(s2, paese="CH")
check("CH come CH-TI qui", not rch2["ok"])

# --- input non validi ---
check("paese invalido", not ef(serie_gen_feb(), paese="XX")["ok"])
check("serie vuota", not ef(pd.Series(dtype=float))["ok"])
check("indice non datetime",
      not ef(pd.Series([1.0, 2.0], index=[0, 1]))["ok"])
check("copertura invalida", not ef(serie_gen_feb(), copertura_min=0.0)["ok"])
check("copertura invalida 2", not ef(serie_gen_feb(), copertura_min=2.0)["ok"])

# --- tz-aware gestito ---
s_tz = serie_gen_feb().tz_localize("Europe/Zurich")
r_tz = ef(s_tz, paese="CH-TI")
check("tz-aware ok", r_tz["ok"], r_tz["motivo"])
check("tz-aware n_festivita 2", r_tz["n_festivita"] == 2, r_tz["n_festivita"])

# --- duplicati gestiti ---
s_dup = pd.concat([serie_gen_feb(), serie_gen_feb().iloc[:5]])
r_dup = ef(s_dup, paese="CH-TI")
check("duplicati ok", r_dup["ok"] and r_dup["n_festivita"] == 2,
      (r_dup["ok"], r_dup["n_festivita"]))

# --- copertura: giorno con 10 ore saltato onestamente ---
s_cov = serie_gen_feb()
s_cov = s_cov.drop(s_cov.loc["2026-01-06"].iloc[10:].index)
r_cov = ef(s_cov, paese="CH-TI")
check("copertura ok", r_cov["ok"], r_cov["motivo"])
check("Epifania saltata -> 1 festivita'", r_cov["n_festivita"] == 1, r_cov["n_festivita"])
check("giorno saltato contato", r_cov["n_giorni_saltati"] >= 1, r_cov["n_giorni_saltati"])

# --- sconto negativo (festivita' piu' cara) onesto ---
s_neg = serie_gen_feb(p_fest=120.0, p_fer=100.0)
r_neg = ef(s_neg, paese="CH-TI")
check("sconto negativo ok", r_neg["ok"])
check("sconto negativo -20", r_neg["sconto_medio_eur"] == -20.0, r_neg["sconto_medio_eur"])

# --- tab presente in app.py ---
_src = open(APP, encoding="utf-8").read()
_riga_tabs = next((l for l in _src.splitlines() if "= st.tabs([" in l), "")
check("tab136 in st.tabs",
      "tab136" in _riga_tabs.split("= st.tabs([")[0], _riga_tabs[:60])
check("label Effetto festivit\u00e0", "\U0001F384 Effetto festivit\u00e0" in _src)

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
