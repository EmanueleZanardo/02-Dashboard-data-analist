"""Test standalone tab139 'Qualita dati'.

Estrae calcola_qualita_dati da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_qualita_dati_2026-10-01_2240.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_qualita_dati":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
qd = ns["calcola_qualita_dati"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_base(giorni=30, inizio="2026-01-01", seed=7):
    rng = np.random.default_rng(seed)
    idx = pd.date_range(inizio, periods=giorni * 24, freq="h")
    vals = 100.0 + 20.0 * rng.standard_normal(len(idx))
    return pd.Series(vals, index=idx)


S = serie_base()

# --- validazione input ---
r = qd(pd.Series(dtype=float))
check("serie vuota -> errore", r["errore"] is not None, r["errore"])
check("serie vuota -> valido False", r["valido"] is False)
r = qd(pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2]))
check("indice non-datetime -> errore", r["errore"] is not None)
r = qd(pd.Series(["a", "b"], index=pd.date_range("2026-01-01", periods=2, freq="h")))
check("valori non numerici -> errore", r["errore"] is not None)
r = qd(S, soglia_z=-1)
check("soglia_z negativa -> errore", r["errore"] is not None)
r = qd(S, run_piatta_ore=1)
check("run_piatta_ore < 2 -> errore", r["errore"] is not None)
r = qd(S, soglia_z="x")
check("soglia_z non numerica -> errore", r["errore"] is not None)

# --- serie sana: nessun problema ---
r = qd(S)
check("serie sana -> nessun errore", r["errore"] is None, r["errore"])
check("serie sana -> valido", r["valido"] is True)
check("serie sana -> score 100", r["score"] == 100.0, r["score"])
check("serie sana -> verdetto ottima", "ottima" in r["verdetto"], r["verdetto"])
check("serie sana -> copertura 100", r["copertura_pct"] == 100.0, r["copertura_pct"])
check("serie sana -> 0 mancanti", r["n_mancanti"] == 0)
check("serie sana -> 0 duplicati", r["n_duplicati"] == 0)
check("serie sana -> 0 NaN", r["n_nan"] == 0)
check("serie sana -> 0 episodi piatti", r["n_episodi_piatti"] == 0)
check("serie sana -> 0 outlier", r["n_outlier"] == 0, r["n_outlier"])
check("serie sana -> df_problemi vuoto", r["df_problemi"].empty)
check("serie sana -> n_attese = ore", r["n_attese"] == 30 * 24, r["n_attese"])

# --- ore mancanti ---
S_gap = S.drop(S.index[100:105])
r = qd(S_gap)
check("gap -> n_mancanti == 5", r["n_mancanti"] == 5, r["n_mancanti"])
check("gap -> 1 episodio Ore mancanti",
      (r["df_problemi"]["Tipo"] == "Ore mancanti").sum() == 1)
ep = r["df_problemi"][r["df_problemi"]["Tipo"] == "Ore mancanti"].iloc[0]
check("gap -> episodio da 5 ore", ep["Ore"] == 5, ep["Ore"])
check("gap -> inizio/fine episodio giusti",
      ep["Inizio"] == S.index[100] and ep["Fine"] == S.index[104],
      f"{ep['Inizio']} {ep['Fine']}")
check("gap -> score < 100", r["score"] < 100.0, r["score"])
check("gap -> copertura < 100", r["copertura_pct"] < 100.0)

# --- timestamp duplicati ---
S_dup = pd.concat([S, S.iloc[[200]]])
r = qd(S_dup)
check("duplicato -> n_duplicati == 1", r["n_duplicati"] == 1, r["n_duplicati"])
check("duplicato -> problema Timestamp duplicato",
      (r["df_problemi"]["Tipo"] == "Timestamp duplicato").sum() == 1)

# --- valore congelato ---
S_flat = S.copy()
S_flat.iloc[300:308] = 77.77
r = qd(S_flat)
check("run piatto 8h -> 1 episodio", r["n_episodi_piatti"] == 1, r["n_episodi_piatti"])
epf = r["df_problemi"][r["df_problemi"]["Tipo"] == "Valore congelato"].iloc[0]
check("run piatto -> 8 ore", epf["Ore"] == 8, epf["Ore"])
check("run piatto -> dettaglio con valore", "77.77" in epf["Dettaglio"], epf["Dettaglio"])
r2 = qd(S_flat, run_piatta_ore=10)
check("run 8h con soglia 10h -> 0 episodi", r2["n_episodi_piatti"] == 0)

# --- outlier ---
S_out = S.copy()
S_out.iloc[400] = 10000.0
r = qd(S_out)
check("spike -> outlier rilevato", r["n_outlier"] >= 1, r["n_outlier"])
check("spike -> df_outlier non vuoto", not r["df_outlier"].empty)
check("spike -> timestamp in df_outlier",
      S_out.index[400] in set(r["df_outlier"]["Timestamp"]))
check("spike -> z-score alto",
      float(r["df_outlier"].iloc[0]["z-score"]) > 4.0,
      r["df_outlier"].iloc[0]["z-score"])

# --- NaN e negativi ---
S_nan = S.copy()
S_nan.iloc[[10, 11, 12]] = np.nan
r = qd(S_nan)
check("3 NaN -> n_nan == 3", r["n_nan"] == 3, r["n_nan"])
check("NaN -> copertura cala", r["copertura_pct"] < 100.0)
S2_rng = np.random.default_rng(11)
S2_idx = pd.date_range("2026-03-01", periods=20 * 24, freq="h")
S2 = pd.Series(50.0 + 30.0 * S2_rng.standard_normal(len(S2_idx)), index=S2_idx)
r_base2 = qd(S2)
S2_neg = S2.copy()
S2_neg.iloc[[5, 6]] = [-8.0, -15.0]   # negativi lievi: z ~2, non outlier
r_neg = qd(S2_neg)
check("negativi lievi -> conteggiati", r_neg["n_negativi"] >= 2, r_neg["n_negativi"])
check("negativi lievi -> stesso score del baseline",
      r_neg["score"] == r_base2["score"], (r_base2["score"], r_neg["score"]))
S_out_neg = S2.copy()
S_out_neg.iloc[60] = -900.0           # negativo estremo: outlier vero
r_outn = qd(S_out_neg)
check("negativo estremo -> outlier rilevato", r_outn["n_outlier"] >= 1)

# --- tz-aware, non ordinato, determinismo ---
S_tz = S.copy()
S_tz.index = S_tz.index.tz_localize("Europe/Zurich")
r_tz = qd(S_tz)
r_naive = qd(S)
check("tz-aware -> stesso score del naive", r_tz["score"] == r_naive["score"])
check("tz-aware -> 0 mancanti", r_tz["n_mancanti"] == 0)
S_shuf = S.sample(frac=1.0, random_state=3)
r_sh = qd(S_shuf)
check("non ordinato -> flag", r_sh["non_ordinato"] is True)
check("non ordinato -> 0 mancanti comunque", r_sh["n_mancanti"] == 0)
ra, rb = qd(S_gap), qd(S_gap)
check("determinismo -> score uguale", ra["score"] == rb["score"])
check("determinismo -> df_problemi uguali",
      ra["df_problemi"].equals(rb["df_problemi"]))

# --- copertura mensile ---
r = qd(S_gap)
check("df_mensile somma Attese == n_attese",
      r["df_mensile"]["Attese"].sum() == r["n_attese"])
check("df_mensile somma Effettive == n_effettive",
      r["df_mensile"]["Effettive"].sum() == r["n_effettive"])
check("df_mensile formato YYYY-MM",
      all(len(str(m)) == 7 for m in r["df_mensile"]["Mese"]))

# --- serie molto bucata -> verdetto critica ---
S_bad = S.iloc[::3].copy()                       # tiene 1 ora su 3
S_bad = pd.concat([S_bad, S_bad.iloc[[0]]])      # + duplicato
S_bad.iloc[5:9] = np.nan                         # + NaN
S_bad.iloc[50:58] = 42.0                          # + run piatto 8h
S_bad.iloc[60] = 9000.0                           # + outlier
r = qd(S_bad)
check("serie bucata -> score < 70", r["score"] < 70, r["score"])
check("serie bucata -> verdetto critica", "critica" in r["verdetto"], r["verdetto"])
check("serie bucata -> problemi ordinati per Inizio",
      r["df_problemi"]["Inizio"].is_monotonic_increasing)

# --- registrazione tab139 ---
_src = open(APP, encoding="utf-8").read()
_riga_tabs = next((l for l in _src.splitlines() if "= st.tabs([" in l), "")
check("tab139 in st.tabs",
      "tab139" in _riga_tabs.split("= st.tabs([")[0], _riga_tabs[:60])
check("titolo 'Qualità dati' nei tab", "Qualità dati" in _riga_tabs)
check("blocco 'with tab139:' presente", "with tab139:" in _src)
check("helper chiamata nel blocco tab139",
      "calcola_qualita_dati" in
      _src.split("with tab139:")[1].split("# Footer")[0]
      if "with tab139:" in _src else False)

print(f"Qualita dati (tab139): {checks} check, {len(fails)} fail")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
