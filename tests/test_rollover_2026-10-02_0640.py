"""Standalone test for calcola_rollover_coperture - tab147 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_rollover_coperture",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_rollover_coperture = ns["calcola_rollover_coperture"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"
COLS = ["Mese", "Strip (\u20ac/MWh)", "Roll (\u20ac/MWh)", "Roll yield (%)",
        "Regime", "MWh coperti", "Costo roll (\u20ac)"]

def serie_mesi(valori_mensili, start="2026-01-01"):
    vals, idx = [], []
    t = pd.Timestamp(start)
    for v in valori_mensili:
        n_ore = pd.Period(t, freq="M").days_in_month * 24
        vals += [float(v)] * n_ore
        idx += list(pd.date_range(t, periods=n_ore, freq="h"))
        t = t + pd.offsets.MonthBegin(1)
    return pd.Series(vals, index=pd.DatetimeIndex(idx), name="p")

def serie_mesi_tz(valori_mensili, start="2026-01-01"):
    s = serie_mesi(valori_mensili, start)
    # DST: il 29/03/2026 le 02:00 non esistono a Zurigo -> NaT e drop
    s = s.copy()
    s.index = s.index.tz_localize(TZ, nonexistent="NaT", ambiguous="NaT")
    return s.dropna()

# ---------- 1. Serie piatta 4 mesi a 100: roll 0, tutto piatto ----------
s = serie_mesi([100, 100, 100, 100])
r = calcola_rollover_coperture(s, mw=1.0, quota_copertura_pct=50.0)
check("1 errore None", r["errore"] is None)
check("1 valido", r["valido"] is True)
check("1 colonne", list(r["mensile"].columns) == COLS)
check("1 n_roll 2", r["n_roll"] == 2)
check("1 mesi totali 4", r["n_mesi_totali"] == 4)
check("1 totale 0", r["totale_eur"] == 0.0)
check("1 roll medio 0", r["roll_medio_eur_mwh"] == 0.0)
check("1 tutti piatti", r["mesi_piatti"] == 2 and r["mesi_contango"] == 0 and r["mesi_backwardation"] == 0)
check("1 categoria neutro", r["categoria"] == "neutro")
check("1 costo annuo 0", r["costo_annuo_stimato"] == 0.0)
check("1 incidenza 0", r["incidenza_pct"] == 0.0)
check("1 sensibilita 11 righe", len(r["sensibilita"]) == 11)

# ---------- 2. Trend crescente: strip 100,110,120,130 -> contango ----------
s = serie_mesi([100, 110, 120, 130])
r = calcola_rollover_coperture(s, mw=1.0, quota_copertura_pct=50.0, mesi_anticipo=1)
check("2 roll +10,+10", r["mensile"]["Roll (\u20ac/MWh)"].tolist() == [10.0, 10.0])
check("2 yield negativi", all(r["mensile"]["Roll yield (%)"] < 0))
check("2 contango 2", r["mesi_contango"] == 2)
check("2 categoria costo", r["categoria"] == "costo")
# MWh coperti: marzo 744h*0.5=372, aprile 720h*0.5=360 -> totale = 10*372+10*360 = 7320
check("2 totale 7320", abs(r["totale_eur"] - 7320.0) < 0.01)
check("2 mwh riga1 372", abs(r["mensile"]["MWh coperti"].iloc[0] - 372.0) < 0.01)
check("2 costo riga1 3720", abs(r["mensile"]["Costo roll (\u20ac)"].iloc[0] - 3720.0) < 0.01)
check("2 costo annuo", abs(r["costo_annuo_stimato"] - 7320.0 / 2 * 12) < 0.5)
# costo fornitura = 120*744 + 130*720 (MW=1, 100%)
check("2 fornitura", abs(r["costo_fornitura"] - (120 * 744 + 130 * 720)) < 1.0)
check("2 incidenza", abs(r["incidenza_pct"] - 7320.0 / (120 * 744 + 130 * 720) * 100) < 0.01)
# sensibilita: quota 100 -> doppio del costo annuo a quota 50
sens = r["sensibilita"]
check("2 sens quota100 = 2x", abs(sens["Costo annuo stimato (\u20ac)"].iloc[-1] - 2 * r["costo_annuo_stimato"]) < 1.0)
check("2 sens quota0 = 0", sens["Costo annuo stimato (\u20ac)"].iloc[0] == 0.0)

# ---------- 3. Trend decrescente: backwardation guadagno ----------
s = serie_mesi([130, 120, 110, 100])
r = calcola_rollover_coperture(s, mw=1.0, quota_copertura_pct=50.0)
check("3 roll -10,-10", r["mensile"]["Roll (\u20ac/MWh)"].tolist() == [-10.0, -10.0])
check("3 categoria guadagno", r["categoria"] == "guadagno")
check("3 totale -7320", abs(r["totale_eur"] + 7320.0) < 0.01)
check("3 backwardation 2", r["mesi_backwardation"] == 2)

# ---------- 4. quota 0 -> tutto zero ma valido ----------
s = serie_mesi([100, 110, 120])
r = calcola_rollover_coperture(s, quota_copertura_pct=0.0)
check("4 valido", r["valido"] is True)
check("4 totale 0", r["totale_eur"] == 0.0)
check("4 costo annuo 0", r["costo_annuo_stimato"] == 0.0)
check("4 sens tutti 0", (r["sensibilita"]["Costo annuo stimato (\u20ac)"] == 0).all())

# ---------- 5. anticipo 2 mesi ----------
s = serie_mesi([100, 110, 120, 130, 140])
r = calcola_rollover_coperture(s, mesi_anticipo=2)
check("5 n_roll 2 (5-2-1)", r["n_roll"] == 2)
check("5 roll +10,+10", r["mensile"]["Roll (\u20ac/MWh)"].tolist() == [10.0, 10.0])
check("5 mesi consegna apr/mag", r["mensile"]["Mese"].tolist() == ["2026-04", "2026-05"])

# ---------- 6. tz-aware: non crasha, stessi risultati ----------
s = serie_mesi_tz([100, 110, 120])
r = calcola_rollover_coperture(s)
check("6 valido tz", r["valido"] is True)
check("6 n_roll 1", r["n_roll"] == 1)
check("6 roll +10", r["mensile"]["Roll (\u20ac/MWh)"].iloc[0] == 10.0)

# ---------- 7. NaN nel mezzo: vengono ignorati ----------
s = serie_mesi([100, 110, 120])
s.iloc[50:60] = np.nan
r = calcola_rollover_coperture(s)
check("7 valido con NaN", r["valido"] is True)
check("7 n_ore ridotte", r["n_ore"] == len(s) - 10)
check("7 roll +10", r["mensile"]["Roll (\u20ac/MWh)"].iloc[0] == 10.0)

# ---------- 8. soglia alta -> regimi piatti ----------
s = serie_mesi([100, 101, 102, 103])
r = calcola_rollover_coperture(s, soglia_regime_pct=5.0)
check("8 tutti piatti", r["mesi_piatti"] == 2)
r = calcola_rollover_coperture(s, soglia_regime_pct=0.5)
check("8 contango con soglia bassa", r["mesi_contango"] == 2)

# ---------- 9. errori ----------
def is_err(kw, msg_part=None):
    r = calcola_rollover_coperture(**kw)
    ok = r["valido"] is False and r["errore"] is not None
    if msg_part:
        ok = ok and msg_part in r["errore"]
    return ok

s3 = serie_mesi([100, 110, 120])
check("9 serie vuota", is_err({"prezzi": pd.Series(dtype=float)}))
check("9 non series", is_err({"prezzi": [1, 2, 3]}))
check("9 indice non datetime", is_err({"prezzi": pd.Series([1.0, 2.0, 3.0])}))
check("9 meno di 3 mesi", is_err({"prezzi": serie_mesi([100, 110])}, "3 mesi"))
check("9 mw zero", is_err({"prezzi": s3, "mw": 0.0}, "MW"))
check("9 mw negativo", is_err({"prezzi": s3, "mw": -1.0}))
check("9 quota negativa", is_err({"prezzi": s3, "quota_copertura_pct": -5.0}))
check("9 quota >100", is_err({"prezzi": s3, "quota_copertura_pct": 101.0}))
check("9 anticipo 0", is_err({"prezzi": s3, "mesi_anticipo": 0}))
check("9 anticipo 4", is_err({"prezzi": s3, "mesi_anticipo": 4}))
check("9 soglia negativa", is_err({"prezzi": s3, "soglia_regime_pct": -1.0}))

# ---------- 10. yield medio e strip in tabella ----------
s = serie_mesi([100, 110, 120, 130])
r = calcola_rollover_coperture(s)
y = r["mensile"]["Roll yield (%)"].tolist()
check("10 yield riga1", abs(y[0] - (-10 / 100 * 100)) < 0.01)
check("10 yield medio", abs(r["yield_medio_pct"] - sum(y) / 2) < 0.01)
check("10 strip tabella = prezzo pagato", r["mensile"]["Strip (\u20ac/MWh)"].tolist() == [110.0, 120.0])
check("10 mesi tabella", r["mensile"]["Mese"].tolist() == ["2026-03", "2026-04"])

print()
print("FAILURES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
