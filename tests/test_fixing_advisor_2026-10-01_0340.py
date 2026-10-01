"""Standalone test for calcola_fixing_advisor - tab118 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_fixing_advisor",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_fixing_advisor = ns["calcola_fixing_advisor"]

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

W = 30
N = 400  # giorni: storia 370 + recenti 30

# ---------- 1. Serie piatta 400 giorni a 100 -> neutro ----------
s = serie_giorni(np.full(N, 100.0))
r = calcola_fixing_advisor(s, W)
check("1 errore None", r["errore"] is None)
check("1 score = 50.0", r["score"] == 50.0)
check("1 segnale NEUTRO", r["segnale"] == "NEUTRO")
check("1 percentile = 50.0", r["percentile_recente"] == 50.0)
check("1 trend = 0", r["trend_norm"] == 0.0)
check("1 vol_ratio = 1.0", r["vol_ratio"] == 1.0)
check("1 prezzo medio recente = 100", r["prezzo_medio_recente"] == 100.0)
check("1 prezzo medio storico = 100", r["prezzo_medio_storico"] == 100.0)
check("1 premio stagionale = 0", r["premio_stagionale_pct"] == 0.0)
check("1 df_giorni 400 righe", len(r["df_giorni"]) == 400)
check("1 df_mesi 12 righe", len(r["df_mesi"]) == 12)

# ---------- 2. Crollo recente: 370 gg a 100, ultimi 30 a 60 -> FISSA ----------
s2 = serie_giorni(np.concatenate([np.full(370, 100.0), np.full(30, 60.0)]))
r2 = calcola_fixing_advisor(s2, W)
check("2 percentile basso", r2["percentile_recente"] < 10.0)
check("2 segnale FISSA", r2["segnale"] == "FISSA")
check("2 score alto", r2["score"] >= 60.0)
check("2 prezzo recente = 60", abs(r2["prezzo_medio_recente"] - 60.0) < 1e-9)
check("2 storico ~100", abs(r2["prezzo_medio_storico"] - 100.0) < 1e-9)
check("2 percentile frame in [0,100]", r2["df_giorni"]["Percentile rolling (%)"].between(0, 100).all())

# ---------- 3. Spike recente: 370 gg a 100, ultimi 30 a 200 -> ASPETTA ----------
s3 = serie_giorni(np.concatenate([np.full(370, 100.0), np.full(30, 200.0)]))
r3 = calcola_fixing_advisor(s3, W)
check("3 percentile alto", r3["percentile_recente"] > 90.0)
check("3 segnale ASPETTA", r3["segnale"] == "ASPETTA")
check("3 score basso", r3["score"] < 40.0)

# ---------- 4. Trend rialzista recente -> trend_norm > 0 ----------
rng = np.random.default_rng(42)
storia_vals = 100.0 + rng.normal(0, 5.0, 370)
recenti_vals = 100.0 + np.linspace(0, 30.0, 30) + rng.normal(0, 2.0, 30)
s4 = serie_giorni(np.concatenate([storia_vals, recenti_vals]))
r4 = calcola_fixing_advisor(s4, W)
check("4 trend positivo", r4["trend_norm"] > 0.5)
check("4 score entro 0-100", 0.0 <= r4["score"] <= 100.0)

# ---------- 5. Trend ribassista recente -> trend_norm < 0 ----------
recenti_down = 140.0 - np.linspace(0, 40.0, 30) + rng.normal(0, 2.0, 30)
s5 = serie_giorni(np.concatenate([np.full(370, 140.0), recenti_down]))
r5 = calcola_fixing_advisor(s5, W)
check("5 trend negativo", r5["trend_norm"] < -0.5)
check("5 percentile basso (costo calato)", r5["percentile_recente"] < 50.0)

# ---------- 6. Serie corta -> vuoto ----------
s6 = serie_giorni(np.full(40, 100.0))
r6 = calcola_fixing_advisor(s6, W)
check("6 score None (troppo corta)", r6["score"] is None)
check("6 segnale None", r6["segnale"] is None)
check("6 df vuoti", len(r6["df_giorni"]) == 0)

# ---------- 7. NaN e indice non datetime -> gestiti ----------
s7 = serie_giorni(np.full(N, 100.0))
s7.iloc[::7] = np.nan
r7 = calcola_fixing_advisor(s7, W)
check("7 NaN gestiti", r7["errore"] is None and r7["score"] == 50.0)
r8 = calcola_fixing_advisor(pd.Series([1.0, 2.0, 3.0]), W)
check("8 indice non datetime -> vuoto", r8["score"] is None)

# ---------- 8. W clampato / default ----------
r9 = calcola_fixing_advisor(s, 500)  # clampato a 90
check("9 W clampato, df 400 righe", len(r9["df_giorni"]) == 400)
check("9 score 50", r9["score"] == 50.0)

# ---------- 9. Coerenza df_giorni ----------
g = r["df_giorni"]
check("9 colonne", list(g.columns) == ["Data", "Prezzo medio (€/MWh)", "Percentile rolling (%)"])
check("9 date ordinate", g["Data"].is_monotonic_increasing)
check("9 ultimo percentile storia piatta = 100", g["Percentile rolling (%)"].iloc[-1] == 100.0)
check("9 giorni recenti caso 2 percentile = 0", r2["df_giorni"].tail(30)["Percentile rolling (%)"].eq(0.0).all())
check("9 giorni recenti caso 3 percentile = 100", r3["df_giorni"].tail(30)["Percentile rolling (%)"].eq(100.0).all())
check("9 ultima data = 2027-02-04", g["Data"].iloc[-1].date().isoformat() == "2027-02-04")

print()
print(f"Totale check: passati ok, FAIL: {len(fails)}")
if fails:
    print("FALLITI:", fails)
    raise SystemExit(1)
