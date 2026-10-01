"""Test standalone tab130 'Drawdown MtM'.

Estrae calcola_pnl_posizione_aperta e calcola_drawdown_mtm da app.py via AST
(niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_drawdown_mtm_2026-10-01_1540.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_pnl_posizione_aperta", "calcola_drawdown_mtm"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
pnl = ns["calcola_pnl_posizione_aperta"]
ddf = ns["calcola_drawdown_mtm"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_prezzi(valori):
    idx = pd.date_range("2026-01-01", periods=len(valori), freq="D")
    return pd.Series(valori, index=idx)


# --- 1. prezzi piatti = riferimento -> P&L zero ---
r = pnl(serie_prezzi([100.0] * 10), 2.0, 100.0, ruolo="acquisto")
check("valido base", r["valido"] and r["errore"] is None)
check("pnl zero piatto", abs(r["pnl_totale"]) < 1e-9, r["pnl_totale"])
check("n_giorni", r["n_giorni"] == 10, r["n_giorni"])

# --- 2. aritmetica P&L ruolo acquisto ---
# spot 90 sotto ref 100: (100-90)*2MW*24h = 480/giorno, 5 giorni -> 2400
r = pnl(serie_prezzi([90.0] * 5), 2.0, 100.0, ruolo="acquisto")
check("pnl acquisto", abs(r["pnl_totale"] - 2400.0) < 1e-9, r["pnl_totale"])
check("giornaliera acquisto",
      abs(r["serie_giornaliera"].iloc[0] - 480.0) < 1e-9)

# --- 3. ruolo vendita = specchio ---
rv = pnl(serie_prezzi([90.0] * 5), 2.0, 100.0, ruolo="vendita")
check("vendita specchio", abs(rv["pnl_totale"] + r["pnl_totale"]) < 1e-9,
      rv["pnl_totale"])

# --- 4. raddoppio MW raddoppia P&L ---
r2 = pnl(serie_prezzi([90.0] * 5), 4.0, 100.0, ruolo="acquisto")
check("scala MW", abs(r2["pnl_totale"] - 2 * r["pnl_totale"]) < 1e-9)

# --- 5. errori pnl ---
check("mw zero", pnl(serie_prezzi([90.0] * 5), 0.0, 100.0)["errore"] is not None)
check("mw negativo", pnl(serie_prezzi([90.0] * 5), -1.0, 100.0)["errore"] is not None)
check("ruolo ko", pnl(serie_prezzi([90.0] * 5), 2.0, 100.0, ruolo="x")["errore"] is not None)
check("ref nan", pnl(serie_prezzi([90.0] * 5), 2.0, float("nan"))["errore"] is not None)
check("prezzi vuoti", pnl(pd.Series(dtype=float), 2.0, 100.0)["errore"] is not None)
check("un solo giorno", pnl(serie_prezzi([90.0]), 2.0, 100.0)["errore"] is not None)

# --- 6. drawdown su curva nota [0,10,20,10,5,15] ---
curva = pd.Series([0.0, 10.0, 20.0, 10.0, 5.0, 15.0],
                  index=pd.date_range("2026-01-01", periods=6, freq="D"))
d = ddf(curva)
check("valido dd", d["valido"] and d["errore"] is None)
check("max drawdown", abs(d["max_drawdown"] - (-15.0)) < 1e-9, d["max_drawdown"])
check("drawdown <= 0", bool((d["drawdown"] <= 1e-12).all()))
check("picco data", d["picco_data"] == pd.Timestamp("2026-01-03"), d["picco_data"])
check("picco valore", abs(d["picco_valore"] - 20.0) < 1e-9)
check("minimo data", d["minimo_data"] == pd.Timestamp("2026-01-05"))
check("recupero data", d["recupero_data"] is None, d["recupero_data"])
check("recupero giorni", d["recupero_giorni"] is None, d["recupero_giorni"])
check("durata max gg", d["durata_max_giorni"] == 2, d["durata_max_giorni"])
check("drawdown attuale", abs(d["drawdown_attuale"] - (-5.0)) < 1e-9, d["drawdown_attuale"])
check("1 episodio", len(d["episodi"]) == 1, len(d["episodi"]))

# --- 7. curva sempre crescente -> drawdown 0 ---
d = ddf(pd.Series([1.0, 2.0, 3.0, 4.0],
                  index=pd.date_range("2026-01-01", periods=4, freq="D")))
check("crescente dd 0", abs(d["max_drawdown"]) < 1e-12)
check("crescente 0 episodi", len(d["episodi"]) == 0)

# --- 8. curva decrescente -> dd = ultimo - primo ---
d = ddf(pd.Series([10.0, 7.0, 3.0, 1.0],
                  index=pd.date_range("2026-01-01", periods=4, freq="D")))
check("decrescente dd", abs(d["max_drawdown"] - (-9.0)) < 1e-9, d["max_drawdown"])
check("decrescente non recuperato", d["recupero_data"] is None)

# --- 9. coerenza: max_dd == profondita' episodio piu' profondo ---
d = ddf(curva)
prof = max(e["profondita"] for e in d["episodi"])
check("coerenza maxdd/episodio",
      abs(-d["max_drawdown"] - prof) < 1e-9, (d["max_drawdown"], prof))

# --- 10. soglia filtra gli episodi ---
d = ddf(curva, soglia_eur=100.0)
check("soglia esclude", d["n_episodi_soglia"] == 0 and d["df_episodi"].empty)
d = ddf(curva, soglia_eur=10.0)
check("soglia include", d["n_episodi_soglia"] == 1)

# --- 11. errori drawdown ---
check("dd vuota", ddf(pd.Series(dtype=float))["errore"] is not None)
check("dd 1 punto", ddf(pd.Series([5.0]))["errore"] is not None)
check("dd inf", ddf(pd.Series([1.0, float("inf"), 2.0]))["errore"] is not None)
check("dd soglia neg", ddf(curva, soglia_eur=-1.0)["errore"] is not None)

# --- 12. NaN dentro la serie -> droppati, risultato valido ---
s_nan = pd.Series([0.0, np.nan, 10.0, 5.0],
                  index=pd.date_range("2026-01-01", periods=4, freq="D"))
d = ddf(s_nan)
check("nan droppati", d["valido"] and abs(d["max_drawdown"] - (-5.0)) < 1e-9,
      d.get("max_drawdown"))

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
