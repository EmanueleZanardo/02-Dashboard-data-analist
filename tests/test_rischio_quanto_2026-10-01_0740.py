"""Standalone test for calcola_rischio_quanto - tab122 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_rischio_quanto",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_rischio_quanto = ns["calcola_rischio_quanto"]

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

COLS = ["rho", "VaR95 (EUR)", "ES95 (EUR)", "Costo atteso (EUR)"]
ATTESO_DET = 100.0 * 24 * 90  # prezzo 100, mw=1, 90 giorni

# ---------- 1. Prezzo piatto, volume deterministico ----------
s = serie_giorni(np.full(40, 100.0))
r = calcola_rischio_quanto(s, mw_base=1.0, rho=0.3, vol_vol=0.0)
check("1 errore None", r["errore"] is None)
check("1 colonne df", list(r["df_sensibilita"].columns) == COLS)
check("1 5 righe sensibilita", len(r["df_sensibilita"]) == 5)
check("1 rhos griglia", r["df_sensibilita"]["rho"].tolist() == [-0.8, -0.4, 0.0, 0.4, 0.8])
check("1 costo_atteso deterministico", r["costo_atteso"] == ATTESO_DET)
check("1 std 0", r["std_costo"] == 0.0)
check("1 var95 = atteso", r["var95"] == ATTESO_DET)
check("1 es95 = atteso", r["es95"] == ATTESO_DET)
check("1 mediano = atteso", r["costo_mediano"] == ATTESO_DET)
check("1 premio quanto 0 (volume det.)", r["premio_quanto"] == 0.0)
check("1 2000 scenari", len(r["costi_scenari"]) == 2000)
check("1 scenari tutti uguali", len(set(r["costi_scenari"])) == 1)
check("1 mw_base", r["mw_base"] == 1.0)
check("1 rho", r["rho"] == 0.3)
check("1 vol_vol", r["vol_vol"] == 0.0)
check("1 n_giorni", r["n_giorni"] == 90)
check("1 n_scenari", r["n_scenari"] == 2000)
check("1 storico 40", r["n_giorni_storico"] == 40)
check("1 prezzo_partenza 100", r["prezzo_partenza"] == 100.0)
check("1 vol annua prezzo 0", r["vol_annua_prezzo"] == 0.0)
check("1 seed 42", r["seed"] == 42)

# ---------- 2. rho ininfluente con volume deterministico ----------
r2 = calcola_rischio_quanto(s, mw_base=1.0, rho=-0.7, vol_vol=0.0)
check("2 var95 rho=-0.7 = rho=0.3", r2["var95"] == r["var95"])
check("2 premio quanto 0 rho=-0.7", r2["premio_quanto"] == 0.0)
check("2 atteso rho=-0.7 = atteso", r2["costo_atteso"] == ATTESO_DET)

# ---------- 3. Volume stocastico, rho=0: media attesa corretta ----------
rng = np.random.default_rng(7)
pg = 80 + 25 * np.abs(np.sin(np.arange(120) * 0.3)) + rng.normal(0, 4, 120)
s3 = serie_giorni(pg)
r3 = calcola_rischio_quanto(s3, mw_base=2.0, rho=0.0, vol_vol=0.2)
atteso_teorico = float(s3.resample("D").mean().dropna().iloc[-1]) * 48 * 90
check("3 errore None", r3["errore"] is None)
check("3 atteso entro 3% del teorico",
      abs(r3["costo_atteso"] - atteso_teorico) / atteso_teorico < 0.03)
check("3 std > 0", r3["std_costo"] > 0)
check("3 var95 >= atteso", r3["var95"] >= r3["costo_atteso"])
check("3 es95 >= var95", r3["es95"] >= r3["var95"])
check("3 premio quanto 0 con rho=0", r3["premio_quanto"] == 0.0)
check("3 var95_rho0 = var95", r3["var95_rho0"] == r3["var95"])

# ---------- 4. Correlazione positiva -> premio quanto > 0 ----------
r4 = calcola_rischio_quanto(s3, mw_base=2.0, rho=0.8, vol_vol=0.25)
check("4 errore None", r4["errore"] is None)
check("4 premio quanto > 0 (rho=0.8)", r4["premio_quanto"] > 0)
check("4 var95 rho=0.8 > var95 rho=0", r4["var95"] > r3["var95"])
check("4 atteso rho=0.8 > atteso rho=0", r4["costo_atteso"] > r3["costo_atteso"])

# ---------- 5. Correlazione negativa -> premio quanto < 0 ----------
r5 = calcola_rischio_quanto(s3, mw_base=2.0, rho=-0.8, vol_vol=0.25)
check("5 premio quanto < 0 (rho=-0.8)", r5["premio_quanto"] < 0)

# ---------- 6. Budget ----------
rb = calcola_rischio_quanto(s, mw_base=1.0, rho=0.3, vol_vol=0.0,
                            budget=ATTESO_DET - 1)
check("6 prob sopra budget=atteso-1 e' 1.0", rb["prob_budget"] == 1.0)
rb = calcola_rischio_quanto(s, mw_base=1.0, rho=0.3, vol_vol=0.0,
                            budget=ATTESO_DET + 1)
check("6 prob sopra budget=atteso+1 e' 0.0", rb["prob_budget"] == 0.0)
rb = calcola_rischio_quanto(s, mw_base=1.0, rho=0.3, vol_vol=0.0)
check("6 prob None senza budget", rb["prob_budget"] is None)

# ---------- 7. Errori di validazione ----------
check("7 mw 0", calcola_rischio_quanto(s, mw_base=0)["errore"] is not None)
check("7 mw negativo", calcola_rischio_quanto(s, mw_base=-1)["errore"] is not None)
check("7 mw > 5000", calcola_rischio_quanto(s, mw_base=5001)["errore"] is not None)
check("7 rho 2", calcola_rischio_quanto(s, rho=2.0)["errore"] is not None)
check("7 rho -2", calcola_rischio_quanto(s, rho=-2.0)["errore"] is not None)
check("7 rho +-0.999 ok", calcola_rischio_quanto(s, rho=0.999)["errore"] is None)
check("7 vol_vol negativa", calcola_rischio_quanto(s, vol_vol=-0.1)["errore"] is not None)
check("7 vol_vol > 2", calcola_rischio_quanto(s, vol_vol=2.5)["errore"] is not None)
check("7 n_giorni 6", calcola_rischio_quanto(s, n_giorni=6)["errore"] is not None)
check("7 n_giorni 400", calcola_rischio_quanto(s, n_giorni=400)["errore"] is not None)
check("7 n_scenari 50", calcola_rischio_quanto(s, n_scenari=50)["errore"] is not None)
check("7 n_scenari 30000", calcola_rischio_quanto(s, n_scenari=30000)["errore"] is not None)
check("7 seed str", calcola_rischio_quanto(s, seed="x")["errore"] is not None)
check("7 budget negativo", calcola_rischio_quanto(s, budget=-5)["errore"] is not None)
check("7 budget str", calcola_rischio_quanto(s, budget="x")["errore"] is not None)

# ---------- 8. Storico insufficiente / indice non datetime ----------
s8 = serie_giorni(np.full(20, 100.0))
r8 = calcola_rischio_quanto(s8)
check("8 20gg: errore None", r8["errore"] is None)
check("8 20gg: costo_atteso None", r8["costo_atteso"] is None)
check("8 20gg: var95 None", r8["var95"] is None)
s8b = pd.Series(np.full(40 * 24, 100.0),
                index=pd.RangeIndex(40 * 24), name="p")
r8b = calcola_rischio_quanto(s8b)
check("8 no-datetime: errore None", r8b["errore"] is None)
check("8 no-datetime: costo None", r8b["costo_atteso"] is None)

# ---------- 9. Prezzi negativi con shift (serie piatta negativa -> deterministico) ----------
pn = serie_giorni(np.full(40, -5.0))
r9 = calcola_rischio_quanto(pn, mw_base=1.0, vol_vol=0.0)
check("9 errore None", r9["errore"] is None)
check("9 shift usato = 6.0", r9["shift_usato"] == 6.0)
check("9 atteso = -5*24*90", r9["costo_atteso"] == -5.0 * 24 * 90)
check("9 std 0", r9["std_costo"] == 0.0)

# ---------- 10. Riproducibilita' ----------
ra = calcola_rischio_quanto(s3, mw_base=2.0, rho=0.5, vol_vol=0.2, seed=123)
rb2 = calcola_rischio_quanto(s3, mw_base=2.0, rho=0.5, vol_vol=0.2, seed=123)
check("10 stesso seed -> stesso var95", ra["var95"] == rb2["var95"])
check("10 stesso seed -> stessi scenari", ra["costi_scenari"] == rb2["costi_scenari"])
rc = calcola_rischio_quanto(s3, mw_base=2.0, rho=0.5, vol_vol=0.2, seed=124)
check("10 seed diverso -> var95 diverso", rc["var95"] != ra["var95"])

print()
print("FAILURES:", len(fails))
if fails:
    raise SystemExit(1)
print("ALL OK")
