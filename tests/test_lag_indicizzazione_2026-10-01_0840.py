"""Test standalone tab123 'Lag di indicizzazione'.

Estrae calcola_lag_indicizzazione + fascia_oraria da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 hidden_files/test_lag_indicizzazione_2026-10-01_0840.py
"""
import ast
import os
import sys

import numpy as np
import pandas as pd

APP = os.path.join(os.path.dirname(__file__), "..", "..", "dashboard-qa", "app.py")
if not os.path.exists(APP):
    APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_lag_indicizzazione", "fascia_oraria"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
lag = ns["calcola_lag_indicizzazione"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} {detail}")


def serie_ore(n_ore, prezzo, inizio="2026-01-01"):
    idx = pd.date_range(inizio, periods=n_ore, freq="h")
    return pd.Series(prezzo, index=idx, dtype=float)


# --- serie base: 90 giorni (3 mesi), prezzo crescente nel tempo ---
N = 90 * 24
idx = pd.date_range("2026-01-01", periods=N, freq="h")
p = 80.0 + np.arange(N) * 0.02  # trend crescente: M-1/M-2 piu' cari dello spot
s = pd.Series(p, index=idx, dtype=float)
r = lag(s, mw_f1=2.0, mw_f2=1.5, mw_f3=1.0)

check("valido base", r["valido"] is True)
check("nessun errore base", r["errore"] is None)
check("n_mesi", r["n_mesi"] == 3, str(r["n_mesi"]))
check("n_ore", r["n_ore"] == N)
check("convenzioni", r["convenzioni"] == ["Spot", "Media M", "M-1", "M-2", "Trimestrale", "Mobile 30gg"])
check("colonne df", list(r["df_mensile"].columns) == ["Mese"] + r["convenzioni"])
check("righe df", len(r["df_mensile"]) == 3)
check("formato mese", list(r["df_mensile"]["Mese"]) == ["2026-01", "2026-02", "2026-03"])

# costo spot = somma esatta prezzo*mw per fascia
fasce = idx.map(ns["fascia_oraria"])
mwv = fasce.map({"F1": 2.0, "F2": 1.5, "F3": 1.0}).astype(float).to_numpy()
spot_atteso = float((p * mwv).sum())
check("costo spot esatto", abs(r["costo_totale"]["Spot"] - spot_atteso) < 1.0,
      f"{r['costo_totale']['Spot']} vs {spot_atteso}")
check("somma mensile = totale", all(
    abs(r["df_mensile"][c].sum() - r["costo_totale"][c]) < 0.05 for c in r["convenzioni"]))
check("copertura spot 100%", r["copertura"]["Spot"] == 1.0)
check("copertura media M 100%", r["copertura"]["Media M"] == 1.0)
check("copertura trimestrale 100%", r["copertura"]["Trimestrale"] == 1.0)
check("copertura M-1 = 59/90", abs(r["copertura"]["M-1"] - 59 / 90) < 0.001, str(r["copertura"]["M-1"]))
check("copertura M-2 = 31/90", abs(r["copertura"]["M-2"] - 31 / 90) < 0.001, str(r["copertura"]["M-2"]))
check("copertura mobile 30gg", abs(r["copertura"]["Mobile 30gg"] - (N - 720) / N) < 0.001)
check("mwh totale", abs(r["mwh_totale"] - float(mwv.sum())) < 0.01)
check("mw echo", (r["mw_f1"], r["mw_f2"], r["mw_f3"]) == (2.0, 1.5, 1.0))

# con trend crescente, il lag paga la media (piu' bassa) dei mesi scorsi -> risparmia
check("trend up: M-1 risparmia vs spot", r["risparmio_vs_spot"]["M-1"] > 0)
check("trend up: M-2 risparmia piu' di M-1",
      r["risparmio_vs_spot"]["M-2"] > r["risparmio_vs_spot"]["M-1"] > 0)
check("migliore in full-coverage", r["migliore"] in ("Media M", "Trimestrale"))
check("migliore = min costo full", r["costo_totale"][r["migliore"]] == min(
    r["costo_totale"]["Media M"], r["costo_totale"]["Trimestrale"]))
check("TE M-1 = std delta mensili", abs(
    r["tracking_error"]["M-1"] - float(np.std(
        (r["df_mensile"]["M-1"] - r["df_mensile"]["Spot"]).to_numpy(), ddof=1))) < 0.01)
check("max dev = max abs delta", abs(
    r["max_dev_mensile"]["M-2"] - float(np.abs(
        (r["df_mensile"]["M-2"] - r["df_mensile"]["Spot"]).to_numpy()).max())) < 0.01)
check("risparmio coerente", all(
    abs(r["risparmio_vs_spot"][c] - (r["costo_totale"]["Spot"] - r["costo_totale"][c])) < 0.05
    for c in r["risparmio_vs_spot"]))

# --- prezzo piatto: tutte le convenzioni uguali a parita' di copertura ---
sf = serie_ore(60 * 24, 100.0)
rf = lag(sf, mw_f1=1.0, mw_f2=1.0, mw_f3=1.0)
check("flat valido", rf["valido"] is True)
spot_f = rf["costo_totale"]["Spot"]
for c in ("Media M", "Trimestrale"):
    check(f"flat {c} == spot", abs(rf["costo_totale"][c] - spot_f) < 1.0,
          f"{rf['costo_totale'][c]} vs {spot_f}")
# M-1 su prezzo piatto: costo = 100 * energia del 2o mese
idx2 = pd.date_range("2026-01-01", periods=60 * 24, freq="h")
mwv2 = idx2.map(ns["fascia_oraria"]).map({"F1": 1.0, "F2": 1.0, "F3": 1.0}).astype(float).to_numpy()
e_mese2 = float(mwv2[31 * 24:60 * 24].sum())
check("flat M-1 = 100*energia mese2", abs(rf["costo_totale"]["M-1"] - 100.0 * e_mese2) < 1.0)
check("flat risparmio Media M = 0", abs(rf["risparmio_vs_spot"]["Media M"]) < 1.0)
check("flat TE Media M = 0", rf["tracking_error"]["Media M"] == 0.0)

# --- prezzi negativi: nessun crash ---
sn = serie_ore(40 * 24, -5.0)
rn = lag(sn)
check("negativi valido", rn["valido"] is True and rn["errore"] is None)
check("negativi costo spot negativo", rn["costo_totale"]["Spot"] < 0)

# --- edge case ---
rv = lag(pd.Series([], dtype=float))
check("serie vuota non valida", rv["valido"] is False and rv["errore"] is None)
rc = lag(serie_ore(10, 100.0))
check("<24 ore non valido", rc["valido"] is False)
rz = lag(serie_ore(48, 100.0), mw_f1=0.0, mw_f2=0.0, mw_f3=0.0)
check("MW zero -> errore", rz["errore"] is not None and rz["valido"] is False)
rn2 = lag(serie_ore(48, 100.0), mw_f1=-1.0, mw_f2=1.0, mw_f3=1.0)
check("MW negativo -> errore", rn2["errore"] is not None)
rbig = lag(serie_ore(48, 100.0), mw_f1=6000.0)
check("MW oltre limite -> errore", rbig["errore"] is not None)
rstr = lag(serie_ore(48, 100.0), mw_f1="x")
check("MW non numerico -> errore", rstr["errore"] is not None)
ridx = lag(pd.Series([100.0] * 48, index=list(range(48))))
check("indice non datetime -> errore", ridx["errore"] is not None)

# NaN scartati
snn = serie_ore(48, 100.0)
snn.iloc[0:5] = np.nan
rnn = lag(snn)
check("NaN scartati", rnn["valido"] is True and rnn["n_ore"] == 43, str(rnn["n_ore"]))

# un solo mese: M-1/M-2 copertura 0, costo 0
s1m = serie_ore(30 * 24, 100.0)
r1 = lag(s1m)
check("1 mese: M-1 copertura 0", r1["copertura"]["M-1"] == 0.0)
check("1 mese: M-1 costo 0", r1["costo_totale"]["M-1"] == 0.0)
check("1 mese: M-2 copertura 0", r1["copertura"]["M-2"] == 0.0)
check("1 mese valido", r1["valido"] is True and r1["n_mesi"] == 1)

# mobile 30gg: prime 720 ore NaN -> con 30 giorni esatti copertura 0
check("30gg esatti: mobile copertura 0", r1["copertura"]["Mobile 30gg"] == 0.0)
s31 = serie_ore(31 * 24, 100.0)
r31 = lag(s31)
check("31gg: mobile copertura 24/744", abs(r31["copertura"]["Mobile 30gg"] - 24 / 744) < 0.001)

# trend decrescente: il lag paga la media (piu' alta) dei mesi scorsi -> costa di piu'
sd = pd.Series(120.0 - np.arange(N) * 0.02, index=idx, dtype=float)
rd = lag(sd, mw_f1=2.0, mw_f2=1.5, mw_f3=1.0)
check("trend down: M-1 €/MWh > spot", rd["prezzo_medio"]["M-1"] > rd["prezzo_medio"]["Spot"])
check("trend down: M-2 €/MWh > M-1",
      rd["prezzo_medio"]["M-2"] > rd["prezzo_medio"]["M-1"])
check("trend down: migliore in full-coverage", rd["migliore"] in ("Media M", "Trimestrale"))
check("trend up: M-1 €/MWh < spot", r["prezzo_medio"]["M-1"] < r["prezzo_medio"]["Spot"])
check("trend up: M-2 €/MWh < M-1", r["prezzo_medio"]["M-2"] < r["prezzo_medio"]["M-1"])

check("flat prezzo_medio == 100", all(
    abs(rf["prezzo_medio"][c] - 100.0) < 0.01 for c in rf["convenzioni"]
    if rf["prezzo_medio"][c] is not None))
check("prezzo_medio None se copertura 0", r1["prezzo_medio"]["M-1"] is None)
check("prezzo_medio spot = costo/energia",
      abs(r["prezzo_medio"]["Spot"] - r["costo_totale"]["Spot"] / r["mwh_totale"]) < 0.01)

print(f"CHECKS: {checks}, FAILS: {len(fails)}")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
