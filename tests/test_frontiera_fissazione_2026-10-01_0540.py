"""Standalone test for calcola_frontiera_fissazione - tab120 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("calcola_frontiera_fissazione",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_frontiera_fissazione = ns["calcola_frontiera_fissazione"]

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

COLS = ["Hedge ratio (%)", "Costo atteso settimanale (€)",
        "Volatilita' settimanale (€)", "Costo atteso annuo (€)",
        "Volatilita' annua (€)"]

# ---------- 1. Serie piatta 21 giorni a 100, F=100: premio 0, vol 0 ----------
s = serie_giorni(np.full(21, 100.0))
r = calcola_frontiera_fissazione(s, mw=2.0, prezzo_forward=100.0)
check("1 errore None", r["errore"] is None)
check("1 premio_mwh = 0", r["premio_rischio_mwh"] == 0.0)
check("1 premio_annuo = 0", r["premio_rischio_annuo"] == 0.0)
check("1 n_settimane = 3", r["n_settimane"] == 3)
check("1 n_giorni = 21", r["n_giorni"] == 21)
check("1 prob = 0.0 (mai strettamente sotto)", r["prob_spot_meglio_fix"] == 0.0)
check("1 vol_spot_annua = 0", r["vol_spot_annua"] == 0.0)
check("1 costo_spot_annuo = 2*24*100*365.25",
      r["costo_spot_atteso_annuo"] == round(2 * 24 * 100 * 365.25, 0))
check("1 colonne df", list(r["df_frontiera"].columns) == COLS)
check("1 21 punti", len(r["df_frontiera"]) == 21)
check("1 vol sempre 0", (r["df_frontiera"]["Volatilita' annua (€)"] == 0.0).all())
check("1 costo sempre uguale", r["df_frontiera"]["Costo atteso annuo (€)"].nunique() == 1)

# ---------- 2. Due livelli: 14gg @80 + 14gg @120, mw=1, F=100 ----------
s = serie_giorni(np.concatenate([np.full(14, 80.0), np.full(14, 120.0)]))
r = calcola_frontiera_fissazione(s, mw=1.0, prezzo_forward=100.0)
check("2 errore None", r["errore"] is None)
check("2 n_settimane = 4", r["n_settimane"] == 4)
check("2 premio_mwh = 0", r["premio_rischio_mwh"] == 0.0)
check("2 premio_annuo = 0", r["premio_rischio_annuo"] == 0.0)
c_spot_w = np.array([80 * 24 * 7, 80 * 24 * 7, 120 * 24 * 7, 120 * 24 * 7])
mean_w, std_w = c_spot_w.mean(), c_spot_w.std(ddof=1)
check("2 costo sett h=0", r["df_frontiera"]["Costo atteso settimanale (€)"].iloc[0] == round(mean_w, 0))
check("2 vol sett h=0", r["df_frontiera"]["Volatilita' settimanale (€)"].iloc[0] == round(std_w, 0))
check("2 costo sett h=100%", r["df_frontiera"]["Costo atteso settimanale (€)"].iloc[-1] == round(100 * 24 * 7, 0))
check("2 vol sett h=100% = 0", r["df_frontiera"]["Volatilita' settimanale (€)"].iloc[-1] == 0.0)
check("2 vol annua h=0 = std*sqrt(365.25/7)",
      np.isclose(r["df_frontiera"]["Volatilita' annua (€)"].iloc[0], round(std_w * np.sqrt(365.25 / 7), 0), atol=1.0))
check("2 vol dimezza a h=50% (linearita')",
      np.isclose(r["df_frontiera"]["Volatilita' settimanale (€)"].iloc[10], round(std_w / 2, 0), atol=1.0))
check("2 prob = 0.5 (2 sett su 4 sotto il fix)", r["prob_spot_meglio_fix"] == 0.5)
check("2 hedge ratio estremi", r["df_frontiera"]["Hedge ratio (%)"].iloc[0] == 0.0
      and r["df_frontiera"]["Hedge ratio (%)"].iloc[-1] == 100.0)

# ---------- 3. Forward sopra lo spot: premio positivo, prob 0 ----------
s = serie_giorni(np.full(14, 60.0))
r = calcola_frontiera_fissazione(s, mw=1.0, prezzo_forward=90.0)
check("3 premio_mwh = 30", r["premio_rischio_mwh"] == 30.0)
check("3 premio_annuo = 30*24*365.25",
      r["premio_rischio_annuo"] == round(30 * 24 * 365.25, 0))
check("3 prob = 1.0 (spot sempre sotto)", r["prob_spot_meglio_fix"] == 1.0)
check("3 costo h=100% > costo h=0%",
      r["df_frontiera"]["Costo atteso annuo (€)"].iloc[-1] > r["df_frontiera"]["Costo atteso annuo (€)"].iloc[0])

# ---------- 4. Proxy forward (None): media primi 7 giorni ----------
s = serie_giorni(np.concatenate([np.full(7, 50.0), np.full(7, 150.0)]))
r = calcola_frontiera_fissazione(s, mw=1.0, prezzo_forward=None)
check("4 proxy = 50", r["prezzo_forward"] == 50.0)
check("4 premio_mwh = 50-100 = -50", r["premio_rischio_mwh"] == -50.0)

# ---------- 5. Errori e casi limite ----------
r = calcola_frontiera_fissazione(serie_giorni(np.full(14, 100.0)), mw=0)
check("5 mw=0 -> errore", r["errore"] is not None)
r = calcola_frontiera_fissazione(serie_giorni(np.full(14, 100.0)), mw=1, prezzo_forward=-5)
check("5 forward negativo -> errore", r["errore"] is not None)
r = calcola_frontiera_fissazione(serie_giorni(np.full(14, 100.0)), mw=1, n_punti=1)
check("5 n_punti=1 -> errore", r["errore"] is not None)
r = calcola_frontiera_fissazione(serie_giorni(np.full(10, 100.0)), mw=1)  # <14 giorni
check("5 10 giorni -> KPI None, errore None", r["errore"] is None and r["premio_rischio_mwh"] is None
      and len(r["df_frontiera"]) == 0)
r = calcola_frontiera_fissazione(pd.Series([1.0, 2.0, 3.0]), mw=1)  # indice non datetime
check("5 indice non datetime -> KPI None", r["errore"] is None and r["n_settimane"] is None)

# ---------- 6. NaN scartati ----------
s = serie_giorni(np.full(14, 100.0))
s.iloc[5] = np.nan
r = calcola_frontiera_fissazione(s, mw=1.0, prezzo_forward=100.0)
check("6 NaN scartato, errore None", r["errore"] is None and r["n_settimane"] == 2)

# ---------- 7. Giorni extra oltre le settimane complete troncati ----------
s = serie_giorni(np.full(16, 100.0))  # 16 giorni -> 2 settimane, 2 giorni scartati
r = calcola_frontiera_fissazione(s, mw=1.0, prezzo_forward=100.0)
check("7 n_giorni = 14 (troncato)", r["n_giorni"] == 14 and r["n_settimane"] == 2)

print()
print("FAILS:", fails if fails else "nessuno")
raise SystemExit(1 if fails else 0)
