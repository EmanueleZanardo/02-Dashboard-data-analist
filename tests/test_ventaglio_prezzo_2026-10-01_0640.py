"""Standalone test for calcola_ventaglio_prezzo - tab121 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_ventaglio_prezzo",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_ventaglio_prezzo = ns["calcola_ventaglio_prezzo"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"

def serie_giorni(valori_giornalieri, start="2026-01-01"):
    n = len(valori_giornalieri)
    vals = np.repeat(np.asarray(valori_giornalieri, dtype=float), 24)
    idx = pd.date_range(start, periods=n * 24, freq="h", tz=TZ)
    return pd.Series(vals, index=idx, name="p")

COLS = ["Giorno", "P10 (€/MWh)", "P25 (€/MWh)", "P50 (€/MWh)",
        "P75 (€/MWh)", "P90 (€/MWh)"]

# ---------- 1. Serie piatta 40gg a 100: sigma=0 -> tutto deterministico ----------
s = serie_giorni(np.full(40, 100.0))
r = calcola_ventaglio_prezzo(s)
check("1 errore None", r["errore"] is None)
check("1 colonne df", list(r["df_bande"].columns) == COLS)
check("1 90 righe", len(r["df_bande"]) == 90)
check("1 Giorno 1..90", r["df_bande"]["Giorno"].tolist() == list(range(1, 91)))
check("1 prezzo_partenza 100", r["prezzo_partenza"] == 100.0)
check("1 vol_annua 0", r["vol_annua"] == 0.0)
check("1 shift 0", r["shift_usato"] == 0.0)
check("1 n_giorni_storico 40", r["n_giorni_storico"] == 40)
check("1 p50_fine 100", r["p50_fine"] == 100.0)
check("1 p10_fine 100", r["p10_fine"] == 100.0)
check("1 p90_fine 100", r["p90_fine"] == 100.0)
check("1 tutte le bande = 100",
      (r["df_bande"][COLS[1:]] == 100.0).all().all())
check("1 prob_soglia None senza soglia", r["prob_soglia"] is None)
check("1 seed 42", r["seed"] == 42)
check("1 con_drift False", r["con_drift"] is False)

# ---------- 2. Soglia sulla serie piatta ----------
r = calcola_ventaglio_prezzo(s, soglia=99.99)
check("2 prob sopra 99.99 = 1.0", r["prob_soglia"] == 1.0)
r = calcola_ventaglio_prezzo(s, soglia=100.0)
check("2 prob sopra 100.0 = 0.0 (strettamente >)", r["prob_soglia"] == 0.0)
r = calcola_ventaglio_prezzo(s, soglia=100.01)
check("2 prob sopra 100.01 = 0.0", r["prob_soglia"] == 0.0)

# ---------- 3. Errori di validazione ----------
r = calcola_ventaglio_prezzo(s, n_giorni=6)
check("3 orizzonte 6 -> errore", r["errore"] is not None)
r = calcola_ventaglio_prezzo(s, n_giorni=366)
check("3 orizzonte 366 -> errore", r["errore"] is not None)
r = calcola_ventaglio_prezzo(s, n_giorni="x")
check("3 orizzonte str -> errore", r["errore"] is not None)
r = calcola_ventaglio_prezzo(s, n_scenari=99)
check("3 scenari 99 -> errore", r["errore"] is not None)
r = calcola_ventaglio_prezzo(s, n_scenari=20001)
check("3 scenari 20001 -> errore", r["errore"] is not None)
r = calcola_ventaglio_prezzo(s, soglia="x")
check("3 soglia str -> errore", r["errore"] is not None)
r = calcola_ventaglio_prezzo(s, n_giorni=7, n_scenari=100)
check("3 params minimi ok", r["errore"] is None and len(r["df_bande"]) == 7)
check("3 con parametri minimi n_righe", len(r["df_bande"]) == 7)

# ---------- 4. Storico troppo corto ----------
s20 = serie_giorni(np.full(20, 100.0))
r = calcola_ventaglio_prezzo(s20)
check("4 20 giorni -> errore None ma KPI None", r["errore"] is None and r["prezzo_partenza"] is None)
check("4 df vuota", len(r["df_bande"]) == 0)

# ---------- 5. Serie con prezzi negativi -> shift attivo ----------
neg = np.array([-10.0] * 10 + [50.0] * 20 + [120.0] * 10, dtype=float)
s = serie_giorni(neg)
r = calcola_ventaglio_prezzo(s, n_giorni=30, n_scenari=500, seed=7)
check("5 errore None", r["errore"] is None)
check("5 shift 11", r["shift_usato"] == 11.0)
check("5 prezzo_partenza 120", r["prezzo_partenza"] == 120.0)
check("5 vol_annua > 0", r["vol_annua"] > 0.0)
check("5 p10 <= p50 <= p90",
      r["p10_fine"] <= r["p50_fine"] <= r["p90_fine"])
check("5 bande monotone per riga",
      ((r["df_bande"]["P10 (€/MWh)"] <= r["df_bande"]["P25 (€/MWh)"]) &
       (r["df_bande"]["P25 (€/MWh)"] <= r["df_bande"]["P50 (€/MWh)"]) &
       (r["df_bande"]["P50 (€/MWh)"] <= r["df_bande"]["P75 (€/MWh)"]) &
       (r["df_bande"]["P75 (€/MWh)"] <= r["df_bande"]["P90 (€/MWh)"])).all())

# ---------- 6. Riproducibilita' con stesso seed ----------
ra = calcola_ventaglio_prezzo(s, seed=7, n_giorni=30, n_scenari=500)
check("6 stesso seed -> stesso p50_fine", ra["p50_fine"] == r["p50_fine"])
check("6 stesso seed -> stesse bande",
      ra["df_bande"].equals(r["df_bande"]))
rb = calcola_ventaglio_prezzo(s, seed=8, n_giorni=30, n_scenari=500)
check("6 seed diverso -> p50 diverso (quasi certo)",
      rb["p50_fine"] != r["p50_fine"])

# ---------- 7. Drift vs martingala ----------
s_up = serie_giorni(np.linspace(50.0, 150.0, 40))
r_no = calcola_ventaglio_prezzo(s_up, con_drift=False, n_scenari=3000, seed=3)
r_dr = calcola_ventaglio_prezzo(s_up, con_drift=True, n_scenari=3000, seed=3)
check("7 entrambi ok", r_no["errore"] is None and r_dr["errore"] is None)
check("7 con drift flag true", r_dr["con_drift"] is True)
check("7 drift positivo alza la mediana",
      r_dr["p50_fine"] > r_no["p50_fine"])
check("7 senza drift p50_fine ~ p0 (martingala)",
      abs(r_no["p50_fine"] - 150.0) < 25.0)

# ---------- 8. Indice non datetime / serie vuota ----------
s_bad = pd.Series(np.full(100, 100.0), index=range(100))
r = calcola_ventaglio_prezzo(s_bad)
check("8 indice non datetime -> KPI None", r["prezzo_partenza"] is None and r["errore"] is None)
r = calcola_ventaglio_prezzo(pd.Series(dtype=float))
check("8 serie vuota -> KPI None", r["prezzo_partenza"] is None)

print()
print("FAILURES:", len(fails), fails if fails else "")
