"""Standalone test for calcola_margin_call - tab119 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_margin_call",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_margin_call = ns["calcola_margin_call"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"

def serie_giorni(valori_giornalieri, start="2026-01-01"):
    """valori_giornalieri: array di medie giornaliere -> serie oraria piatta nel giorno."""
    n = len(valori_giornalieri)
    vals = np.repeat(np.asarray(valori_giornalieri, dtype=float), 24)
    idx = pd.date_range(start, periods=n * 24, freq="h", tz=TZ)
    return pd.Series(vals, index=idx, name="p")

COLS = ["Data", "Prezzo (€/MWh)", "P&L giornaliero (€)", "Equity (€)", "Margin call (€)"]

# ---------- 1. Serie piatta 10 giorni a 100, long: nessun movimento ----------
s = serie_giorni(np.full(10, 100.0))
r = calcola_margin_call(s, mw=2.0, direzione="long", prezzo_fix=100.0,
                        margine_iniziale_pct=10.0, margine_manut_pct=5.0,
                        tasso_annuo_pct=4.0)
check("1 errore None", r["errore"] is None)
check("1 mtm = 0.0", r["mtm_finale"] == 0.0)
check("1 n_giorni_margin_call = 0", r["n_giorni_margin_call"] == 0)
check("1 chiamate_totali = 0.0", r["chiamate_totali"] == 0.0)
check("1 max_margin_call = 0.0", r["max_margin_call"] == 0.0)
check("1 nozionale = 48000", r["nozionale"] == 48000.0)
check("1 margine_iniziale = 4800", r["margine_iniziale"] == 4800.0)
check("1 margine_max_richiesto = iniziale", r["margine_max_richiesto"] == r["margine_iniziale"])
check("1 len df = 10", len(r["df_giorni"]) == 10)
check("1 colonne df", list(r["df_giorni"].columns) == COLS)
check("1 equity sempre = mi", (r["df_giorni"]["Equity (€)"] == 4800.0).all())
check("1 costo_fin = 4800*10*0.04/365 (arrotondato a 2 dec)",
      np.isclose(r["costo_finanziamento"], 4800.0 * 10 * 0.04 / 365.0, atol=0.01))

# ---------- 2. Prezzi in salita, long: profitto, nessuna call ----------
s2 = serie_giorni(100.0 + np.arange(10))
r2 = calcola_margin_call(s2, mw=1.0, direzione="long", prezzo_fix=100.0)
check("2 errore None", r2["errore"] is None)
check("2 mtm = 24*45 = 1080", np.isclose(r2["mtm_finale"], 1080.0))
check("2 nessuna call", r2["n_giorni_margin_call"] == 0 and r2["chiamate_totali"] == 0.0)

# ---------- 3. Stessa serie, short: perdita speculare, nessuna call ----------
r3 = calcola_margin_call(s2, mw=1.0, direzione="short", prezzo_fix=100.0)
check("3 errore None", r3["errore"] is None)
check("3 mtm = -1080", np.isclose(r3["mtm_finale"], -1080.0))
check("3 nessuna call (perdita 1080 < mi-mm = 1200)", r3["n_giorni_margin_call"] == 0)

# ---------- 4. Crollo prezzi, long: margin call scattano ----------
crash = [100, 80, 60, 40, 20, 20, 20, 20, 20, 20]
s4 = serie_giorni(crash)
r4 = calcola_margin_call(s4, mw=1.0, direzione="long", prezzo_fix=100.0,
                         margine_iniziale_pct=10.0, margine_manut_pct=5.0,
                         tasso_annuo_pct=4.0)
check("4 errore None", r4["errore"] is None)
check("4 mtm = -14400", np.isclose(r4["mtm_finale"], -14400.0))
check("4 n_calls = 8", r4["n_giorni_margin_call"] == 8)
check("4 chiamate_totali = 14400", np.isclose(r4["chiamate_totali"], 14400.0))
check("4 max_margin_call = 1920", np.isclose(r4["max_margin_call"], 1920.0))
check("4 margine_max = 2400+14400", np.isclose(r4["margine_max_richiesto"], 16800.0))
check("4 equity post-ricarica mai sotto mm=1200",
      (r4["df_giorni"]["Equity (€)"] >= 1200.0).all())
check("4 equity_minima (pre-ricarica) = 480", np.isclose(r4["equity_minima"], 480.0))
# invariante strutturale: equity[i] - equity[i-1] = pnl[i] + call[i]
eq = r4["df_giorni"]["Equity (€)"].values
pn = r4["df_giorni"]["P&L giornaliero (€)"].values
ca = r4["df_giorni"]["Margin call (€)"].values
ok_inv = np.isclose(eq[0] - 2400.0 - pn[0] - ca[0], 0.0)
ok_inv = ok_inv and np.allclose(eq[1:] - eq[:-1] - pn[1:] - ca[1:], 0.0, atol=1e-6)
check("4 invariante equity", bool(ok_inv))
check("4 somma pnl = mtm", np.isclose(pn.sum(), r4["mtm_finale"]))
check("4 costo_fin con chiamate (arrotondato a 2 dec)",
      np.isclose(r4["costo_finanziamento"],
                 (2400.0 * 10 + (1440.0 * 7 + 1440.0 * 6 + 1920.0 * 15)) * 0.04 / 365.0,
                 atol=0.01))

# ---------- 5. Crollo prezzi, short: profitto, nessuna call ----------
r5 = calcola_margin_call(s4, mw=1.0, direzione="short", prezzo_fix=100.0)
check("5 errore None", r5["errore"] is None)
check("5 mtm = +14400", np.isclose(r5["mtm_finale"], 14400.0))
check("5 nessuna call", r5["n_giorni_margin_call"] == 0)

# ---------- 6. prezzo_fix=None -> proxy media primi 7 giorni ----------
s6 = serie_giorni(np.full(10, 100.0))
r6 = calcola_margin_call(s6, mw=1.0, direzione="long", prezzo_fix=None)
check("6 errore None", r6["errore"] is None)
check("6 prezzo_fix = 100.0 (proxy)", np.isclose(r6["prezzo_fix"], 100.0))
check("6 mtm = 0.0", r6["mtm_finale"] == 0.0)

# ---------- 7. Parametri non validi ----------
base = serie_giorni(np.full(10, 100.0))
check("7 mw=0 -> errore", calcola_margin_call(base, mw=0, prezzo_fix=100.0)["errore"] is not None)
check("7 mw<0 -> errore", calcola_margin_call(base, mw=-1, prezzo_fix=100.0)["errore"] is not None)
check("7 direzione errata -> errore", calcola_margin_call(base, mw=1, direzione="x", prezzo_fix=100.0)["errore"] is not None)
check("7 fix=0 -> errore", calcola_margin_call(base, mw=1, prezzo_fix=0.0)["errore"] is not None)
check("7 fix<0 -> errore", calcola_margin_call(base, mw=1, prezzo_fix=-5.0)["errore"] is not None)
check("7 mm=mi -> errore", calcola_margin_call(base, mw=1, prezzo_fix=100.0, margine_iniziale_pct=5.0, margine_manut_pct=5.0)["errore"] is not None)
check("7 mm>mi -> errore", calcola_margin_call(base, mw=1, prezzo_fix=100.0, margine_iniziale_pct=5.0, margine_manut_pct=10.0)["errore"] is not None)
check("7 tasso<0 -> errore", calcola_margin_call(base, mw=1, prezzo_fix=100.0, tasso_annuo_pct=-1.0)["errore"] is not None)

# ---------- 8. Serie vuota / troppo corta / NaN ----------
sv = pd.Series([], dtype=float, index=pd.DatetimeIndex([], tz=TZ))
r8 = calcola_margin_call(sv, mw=1.0, prezzo_fix=100.0)
check("8 vuota: errore None, kpi None", r8["errore"] is None and r8["mtm_finale"] is None)
check("8 vuota: df vuoto", len(r8["df_giorni"]) == 0)
r8b = calcola_margin_call(serie_giorni([100.0]), mw=1.0, prezzo_fix=100.0)
check("8 un giorno: kpi None", r8b["mtm_finale"] is None and r8b["errore"] is None)
s_nan = serie_giorni([100.0, np.nan, 100.0])
r8c = calcola_margin_call(s_nan, mw=1.0, prezzo_fix=100.0)
check("8 NaN scartati: 2 righe, mtm 0", len(r8c["df_giorni"]) == 2 and r8c["mtm_finale"] == 0.0)

# ---------- 9. Indice non datetime ----------
s_nd = pd.Series([100.0] * 48, index=list(range(48)))
r9 = calcola_margin_call(s_nd, mw=1.0, prezzo_fix=100.0)
check("9 non-datetime: kpi None", r9["mtm_finale"] is None and r9["errore"] is None)

print()
print("FAILURES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
