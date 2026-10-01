"""Test standalone tab138 'Riconciliazione fattura'.

Estrae calcola_riconciliazione_fattura (+ calcola_stima_bolletta,
fascia_oraria) da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_riconciliazione_fattura_2026-10-01_2040.py
"""
import ast
import os
import sys

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
WANT = {"fascia_oraria", "calcola_stima_bolletta",
        "calcola_riconciliazione_fattura"}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in WANT:
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
rf = ns["calcola_riconciliazione_fattura"]
bo = ns["calcola_stima_bolletta"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_piatta(giorni=60, prezzo=100.0, inizio="2026-01-01"):
    idx = pd.date_range(inizio, periods=giorni * 24, freq="h")
    return pd.Series(np.full(len(idx), prezzo), index=idx)


S = serie_piatta()
ATT = bo(S, 1.0, 1.0, 1.0)  # attesi di riferimento
FATT_OK = {"energia": ATT["energia_eur"], "perdite": ATT["perdite_eur"],
           "dispacciamento": ATT["disp_eur"], "pcv": ATT["pcv_eur"],
           "oneri": ATT["oneri_eur"], "accisa": ATT["accisa_eur"],
           "imponibile": ATT["imponibile_eur"], "iva": ATT["iva_eur"],
           "totale": ATT["totale_eur"]}

# --- validazione input ---
r = rf(S, 1, 1, 1, "non-un-dict")
check("fattura non dict -> errore", r["errore"] is not None, r["errore"])
r = rf(S, 1, 1, 1, {})
check("fattura vuota -> errore", r["errore"] is not None)
r = rf(S, 1, 1, 1, {"energia": None, "totale": None})
check("fattura tutta None -> errore", r["errore"] is not None)
r = rf(S, 1, 1, 1, {"energia": "abc"})
check("importo non numerico -> errore", r["errore"] is not None, r["errore"])
r = rf(S, 1, 1, 1, FATT_OK, toll_ass_eur=-1)
check("soglia EUR negativa -> errore", r["errore"] is not None)
r = rf(S, 1, 1, 1, FATT_OK, toll_pct="x")
check("soglia % non numerica -> errore", r["errore"] is not None)
r = rf(pd.Series(dtype=float), 1, 1, 1, FATT_OK)
check("serie vuota -> errore", r["errore"] is not None, r["errore"])
r = rf(S, 0, 0, 0, FATT_OK)
check("profilo a zero -> errore", r["errore"] is not None, r["errore"])
r = rf(S, 1, 1, 1, {"chiave_sconosciuta": 10.0})
check("solo chiavi ignote -> errore (nessuna voce)",
      r["errore"] is not None, r["errore"])

# --- happy path: fattura identica alla stima ---
r = rf(S, 1, 1, 1, dict(FATT_OK))
check("fattura esatta -> nessun errore", r["errore"] is None, r["errore"])
check("verdetto ok", r["verdetto"] == "ok", r["verdetto"])
check("0 anomalie", r["n_anomalie"] == 0, r["n_anomalie"])
check("9 voci confrontate", r["n_voci"] == 9, r["n_voci"])
check("scostamenti tutti zero",
      (r["df"]["Scostamento (\u20ac)"].abs() < 0.005).all())
check("scost totale zero", abs(r["scost_totale_eur"]) < 0.005,
      r["scost_totale_eur"])
check("scost totale % zero", abs(r["scost_totale_pct"]) < 0.005,
      r["scost_totale_pct"])
check("colonne df",
      list(r["df"].columns) == ["Voce", "Atteso (\u20ac)", "Fatturato (\u20ac)",
                                "Scostamento (\u20ac)", "Scost. (%)", "Esito"],
      list(r["df"].columns))
check("mwh coerente", abs(r["mwh"] - ATT["mwh"]) < 1e-6, r["mwh"])
check("n_mesi coerente", r["n_mesi"] == ATT["n_mesi"], r["n_mesi"])

# --- anomalia sopra doppia soglia ---
f2 = dict(FATT_OK)
f2["energia"] = round(FATT_OK["energia"] * 1.10, 2)  # +10% >> soglie
r = rf(S, 1, 1, 1, f2)
check("energia +10% -> 1 anomalia", r["n_anomalie"] == 1, r["n_anomalie"])
check("verdetto anomalie", r["verdetto"] == "anomalie", r["verdetto"])
check("voce anomala = Materia energia",
      r["voci_anomale"] == ["Materia energia"], r["voci_anomale"])
check("esito riga ANOMALA",
      "ANOMALA" in r["df"].loc[r["df"]["Voce"] == "Materia energia",
                               "Esito"].iloc[0])

# --- sotto soglia: doppia soglia NON superata -> ok ---
f3 = dict(FATT_OK)
f3["energia"] = round(FATT_OK["energia"] * 1.01, 2)  # +1% < 2%
r = rf(S, 1, 1, 1, f3)
check("energia +1% (< soglia %) -> ok", r["verdetto"] == "ok",
      r["voci_anomale"])
f4 = dict(FATT_OK)
f4["pcv"] = round(FATT_OK["pcv"] + 30.0, 2)  # +30 EUR < 50 EUR
r = rf(S, 1, 1, 1, f4)
check("pcv +30 EUR (< soglia EUR) -> ok", r["verdetto"] == "ok",
      r["voci_anomale"])

# --- serve ENTRAMBE le soglie: % alta ma EUR bassa -> ok ---
f5 = dict(FATT_OK)
f5["pcv"] = round(FATT_OK["pcv"] * 1.50, 2)  # +50% ma pochi EUR
r = rf(S, 1, 1, 1, f5, toll_ass_eur=5000.0)
check("+50% ma sotto soglia EUR alta -> ok", r["verdetto"] == "ok",
      r["voci_anomale"])

# --- atteso zero: decide solo la soglia EUR ---
bo0 = bo(S, 1.0, 1.0, 1.0, pcv_mese=0.0)
r = rf(S, 1, 1, 1, {"pcv": 100.0}, pcv_mese=0.0)
check("atteso 0, fatt 100 -> anomala (soglia EUR)",
      r["n_anomalie"] == 1, (r["n_anomalie"], r["errore"]))
check("scost % None con atteso zero",
      r["df"]["Scost. (%)"].iloc[0] is None,
      r["df"]["Scost. (%)"].iloc[0])
r = rf(S, 1, 1, 1, {"pcv": 10.0}, pcv_mese=0.0)
check("atteso 0, fatt 10 (< 50 EUR) -> ok", r["verdetto"] == "ok",
      (r["verdetto"], r["errore"]))
check("stima pcv zero davvero", bo0["pcv_eur"] == 0.0, bo0["pcv_eur"])

# --- sottoinsieme di voci ---
r = rf(S, 1, 1, 1, {"totale": FATT_OK["totale"], "iva": FATT_OK["iva"]})
check("2 voci -> n_voci 2", r["n_voci"] == 2, r["n_voci"])
check("verdetto ok su sottoinsieme", r["verdetto"] == "ok")
check("scost totale popolato", r["scost_totale_eur"] == 0.0,
      r["scost_totale_eur"])
r = rf(S, 1, 1, 1, {"energia": FATT_OK["energia"]})
check("senza totale -> scost_totale None",
      r["scost_totale_eur"] is None and r["scost_totale_pct"] is None)

# --- scostamento negativo (fattura sotto stima) ---
f6 = dict(FATT_OK)
f6["totale"] = round(FATT_OK["totale"] * 0.95, 2)  # -5%
r = rf(S, 1, 1, 1, f6)
check("totale -5% -> anomalia", r["n_anomalie"] == 1, r["n_anomalie"])
check("scost totale negativo", r["scost_totale_eur"] < 0,
      r["scost_totale_eur"])
check("scost totale % circa -5",
      abs(r["scost_totale_pct"] + 5.0) < 0.05, r["scost_totale_pct"])

# --- registrazione tab138 ---
_src = open(APP, encoding="utf-8").read()
_riga_tabs = next((l for l in _src.splitlines() if "= st.tabs([" in l), "")
check("tab138 in st.tabs",
      "tab138" in _riga_tabs.split("= st.tabs([")[0], _riga_tabs[:60])
check("titolo 'Riconciliazione fattura' nei tab",
      "Riconciliazione fattura" in _riga_tabs)
check("blocco 'with tab138:' presente", "with tab138:" in _src)
check("helper chiamata nel blocco tab138",
      "calcola_riconciliazione_fattura" in
      _src.split("with tab138:")[1].split("with tab139:")[0]
      if "with tab138:" in _src else False)

print(f"Riconciliazione fattura (tab138): {checks} check, {len(fails)} fail")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
