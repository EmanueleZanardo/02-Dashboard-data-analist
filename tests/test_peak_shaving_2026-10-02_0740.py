"""Standalone test for calcola_peak_shaving - tab148 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_peak_shaving", "_fascia_aeegsi"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_peak_shaving = ns["calcola_peak_shaving"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"

def serie_base(giorni=60, start="2026-01-01"):
    """Prezzi orari con punta serale cara e notte economica."""
    n = giorni * 24
    idx = pd.date_range(start, periods=n, freq="h")
    h = idx.hour.to_numpy()
    vals = 60.0 + 40.0 * ((h >= 8) & (h < 20)).astype(float) + 25.0 * ((h >= 17) & (h < 20)).astype(float)
    return pd.Series(vals, index=pd.DatetimeIndex(idx), name="p")

KWARGS = dict(mw_f1=1.0, mw_f2=0.8, mw_f3=0.5, cap_mwh=2.0, pot_mw=1.0,
              eff_pct=85.0, quota_eur_kw_mese=2.5, potenza_attuale_kw=1000.0,
              degrado_eur_mwh=8.0, capex_batteria_eur=0.0, n_soglie=11)

# --- caso base ---
p = serie_base()
r = calcola_peak_shaving(p, **KWARGS)
check("base: valido e nessun errore", r["valido"] and r["errore"] is None)
check("base: picco lordo 1000 kW", abs(r["picco_lordo_kw"] - 1000.0) < 1e-6)
check("base: n_ore corretto", r["n_ore"] == 60 * 24)
check("base: n_mesi = 3 (gen+feb+mar parziale)", r["n_mesi"] == 3)
check("base: sweep ha 11 righe", len(r["sweep"]) == 11)
check("base: colonne sweep giuste",
      list(r["sweep"].columns) == ["Soglia (kW)", "Risparmio annuo netto (€)",
                                   "Potenza ottimale (kW)", "Quota domanda (€/anno)",
                                   "Delta costo energia (€/anno)", "Degrado (€/anno)"])
check("base: ottimo = max dello sweep",
      abs(r["risparmio_annuo_netto"] - r["sweep"]["Risparmio annuo netto (€)"].max()) < 1e-6)
check("base: potenza ottimale <= picco lordo",
      r["potenza_ottimale_kw"] <= r["picco_lordo_kw"] + 1e-6)
check("base: soglia ottima in [550, 1000]",
      550.0 - 1e-6 <= r["soglia_ottima_kw"] <= 1000.0 + 1e-6)
check("base: mensile ha 3 righe", len(r["mensile"]) == 3)
check("base: picchi netti mensili <= lordi",
      bool((r["mensile"]["Picco netto (kW)"] <= r["mensile"]["Picco lordo (kW)"] + 1e-6).all()))
check("base: verdetto non vuoto", isinstance(r["verdetto"], str) and len(r["verdetto"]) > 10)
check("base: categoria valida", r["categoria"] in ("conviene", "non-conviene", "inutile"))
check("base: payback None con capex=0", r["payback_anni"] is None)
check("base: degrado annuo coerente con MWh scaricati",
      abs(r["degrado_annuo"] - r["mwh_scaricati_annui"] * 8.0) < 2.0)
check("base: quota annua coerente",
      abs(r["quota_annua"] - max(0.0, 1000.0 - r["potenza_ottimale_kw"]) * 2.5 * 12) < 2.0)
# riga baseline (soglia = picco): beneficio ~ 0
row_top = r["sweep"].iloc[-1]
check("base: a soglia=picco il beneficio e' ~0", abs(row_top["Risparmio annuo netto (€)"]) < 1.0)
check("base: risparmio annuo >= 0 (baseline inclusa)", r["risparmio_annuo_netto"] >= -1e-6)

# --- determinismo ---
r2 = calcola_peak_shaving(p, **KWARGS)
check("determinismo: stesso risparmio", r2["risparmio_annuo_netto"] == r["risparmio_annuo_netto"])
check("determinismo: stesso sweep",
      r2["sweep"].equals(r["sweep"]))

# --- batteria enorme: la soglia minima non e' sostenibile (la batteria non
# riesce a ricaricarsi sotto T e si esaurisce: i picchi tornano al lordo),
# quindi l'ottimo e' interno ---
kw_big = dict(KWARGS, cap_mwh=50.0, pot_mw=5.0, degrado_eur_mwh=0.0)
rb = calcola_peak_shaving(p, **kw_big)
check("batteria enorme: a soglia minima la batteria si esaurisce (picco = lordo)",
      abs(rb["sweep"].iloc[0]["Potenza ottimale (kW)"] - 1000.0) < 1e-6)
check("batteria enorme: ottimo interno con picco ridotto",
      rb["potenza_ottimale_kw"] < 1000.0 - 1e-6)
check("batteria enorme: categoria conviene", rb["categoria"] == "conviene")
check("batteria enorme: risparmio annuo positivo", rb["risparmio_annuo_netto"] > 0)

# --- batteria minuscola: quasi nessun effetto ---
kw_small = dict(KWARGS, cap_mwh=0.01, pot_mw=0.01)
rs = calcola_peak_shaving(p, **kw_small)
check("batteria minuscola: potenza ottimale ~ picco lordo",
      rs["potenza_ottimale_kw"] > 990.0)

# --- payback con capex ---
kw_cap = dict(KWARGS, capex_batteria_eur=200000.0)
rc = calcola_peak_shaving(p, **kw_cap)
if rc["risparmio_annuo_netto"] > 0:
    check("capex: payback = capex/beneficio",
          abs(rc["payback_anni"] - 200000.0 / rc["risparmio_annuo_netto"]) < 0.05)
else:
    check("capex: payback None se beneficio <= 0", rc["payback_anni"] is None)

# --- quota zero: nessun incentivo di potenza ---
kw_q0 = dict(KWARGS, quota_eur_kw_mese=0.0)
rq = calcola_peak_shaving(p, **kw_q0)
check("quota zero: quota annua = 0", rq["quota_annua"] == 0.0)
check("quota zero: categoria non 'conviene' via quota",
      rq["categoria"] in ("non-conviene", "inutile"))

# --- tz-aware ---
ptz = p.copy()
ptz.index = ptz.index.tz_localize(TZ, nonexistent="NaT", ambiguous="NaT").dropna()
rtz = calcola_peak_shaving(ptz, **KWARGS)
check("tz-aware: valido", rtz["valido"] and rtz["errore"] is None)
check("tz-aware: n_ore coerente (DST NaT droppati)", rtz["n_ore"] == len(ptz))

# --- errori ---
re_ = calcola_peak_shaving(pd.Series([], dtype=float, index=pd.DatetimeIndex([])), **KWARGS)
check("serie vuota: errore", re_["errore"] is not None and not re_["valido"])
re2 = calcola_peak_shaving(pd.Series([1.0, 2.0], index=[0, 1]), **KWARGS)
check("indice non-datetime: errore", re2["errore"] is not None)
re3 = calcola_peak_shaving(p, mw_f1=0.0, mw_f2=0.0, mw_f3=0.0, cap_mwh=2.0, pot_mw=1.0)
check("MW tutti zero: errore", re3["errore"] is not None)
re4 = calcola_peak_shaving(p, **dict(KWARGS, cap_mwh=0.0))
check("cap <= 0: errore", re4["errore"] is not None)
re5 = calcola_peak_shaving(p, **dict(KWARGS, pot_mw=-1.0))
check("pot < 0: errore", re5["errore"] is not None)
re6 = calcola_peak_shaving(p, **dict(KWARGS, eff_pct=0.0))
check("eff = 0: errore", re6["errore"] is not None)
re7 = calcola_peak_shaving(p, **dict(KWARGS, eff_pct=120.0))
check("eff > 100: errore", re7["errore"] is not None)
re8 = calcola_peak_shaving(p, **dict(KWARGS, potenza_attuale_kw=0.0))
check("potenza attuale <= 0: errore", re8["errore"] is not None)
re9 = calcola_peak_shaving(p, **dict(KWARGS, n_soglie=2))
check("n_soglie=2 clampato a 5", len(re9["sweep"]) == 5)
# sweep vuoto ma con colonne giuste in caso di errore
check("errore: sweep con colonne giuste", list(re_["sweep"].columns)[0] == "Soglia (kW)")

print()
print("FAILURES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
