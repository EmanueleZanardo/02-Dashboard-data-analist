"""Standalone test for calcola_calendario_costo - tab117 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("fascia_oraria", "calcola_calendario_costo"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fascia_oraria = ns["fascia_oraria"]
calcola_calendario_costo = ns["calcola_calendario_costo"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"

def serie_base(ore=24 * 14, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=ore, freq="h", tz=TZ)
    return pd.Series(np.full(ore, prezzo), index=idx, name="p")

# ---------- 1. Serie piatta 14 giorni, prezzo 100, MW 1/1/1 ----------
s = serie_base()
r = calcola_calendario_costo(s, 1.0, 1.0, 1.0)
check("1 errore None", r["errore"] is None)
check("1 14 giorni", len(r["df_giorni"]) == 14)
check("1 costo giorno = 2400", abs(r["df_giorni"]["Costo (€)"].iloc[0] - 2400.0) < 1e-6)
check("1 energia giorno = 24", abs(r["df_giorni"]["Energia (MWh)"].iloc[0] - 24.0) < 1e-6)
check("1 prezzo medio = 100", abs(r["df_giorni"]["Prezzo medio (€/MWh)"].iloc[0] - 100.0) < 1e-6)
check("1 picco prezzo = 100", abs(r["df_giorni"]["Picco prezzo (€/MWh)"].iloc[0] - 100.0) < 1e-6)
check("1 costo totale = 33600", abs(r["costo_totale"] - 33600.0) < 1e-6)
check("1 costo medio gg = 2400", abs(r["costo_medio_gg"] - 2400.0) < 1e-6)
check("1 std gg = 0", abs(r["std_gg"]) < 1e-9)
check("1 quota top10 = 14.3", abs(r["quota_top10_gg_pct"] - 14.3) < 0.05)  # ceil(14*10%)=2 gg
check("1 df_settimana 7 righe", len(r["df_settimana"]) == 7)
check("1 somma settimana = totale", abs(r["df_settimana"]["Costo medio (€)"].mul(
    r["df_settimana"]["N giorni"]).sum() - 33600.0) < 1e-6)
check("1 df_mesi 2 righe (set+ott)", len(r["df_mesi"]) == 2 and list(r["df_mesi"]["Mese"]) == ["2026-09", "2026-10"])
check("1 somma mesi = totale", abs(r["df_mesi"]["Costo (€)"].sum() - 33600.0) < 1e-6)
check("1 mesi giorni 3+11", list(r["df_mesi"]["Giorni"]) == [3, 11])
check("1 nomi giorni it", set(r["df_giorni"]["Giorno"].unique()) <= {"Lun","Mar","Mer","Gio","Ven","Sab","Dom"})

# ---------- 2. Spike su un giorno -> giorno piu' caro ----------
s2 = serie_base()
spike_day = s2.index.normalize().unique()[5]
mask = s2.index.normalize() == spike_day
s2 = s2.copy(); s2[mask] = 500.0
r2 = calcola_calendario_costo(s2, 1.0, 1.0, 1.0)
check("2 giorno piu' caro = spike", r2["giorno_piu_caro"]["Data"].date() == spike_day.date())
check("2 costo spike = 12000", abs(r2["giorno_piu_caro"]["Costo"] - 12000.0) < 1e-6)
check("2 giorno piu' economico non spike", r2["giorno_piu_economico"]["Data"].date() != spike_day.date())
check("2 picco prezzo spike = 500", abs(r2["df_giorni"].loc[r2["df_giorni"]["Data"] == spike_day, "Picco prezzo (€/MWh)"].iloc[0] - 500.0) < 1e-6)
check("2 std > 0", r2["std_gg"] > 0)

# ---------- 3. Profili diversi per fascia (MW solo F1) ----------
r3 = calcola_calendario_costo(s, 2.0, 0.0, 0.0)
# giorni lavorativi: F1 = 11 ore (8-19); weekend: 0
lun = r3["df_giorni"].iloc[0]  # 2026-09-28 = lunedi'
check("3 lun F1 2MW: costo 2200", abs(lun["Costo (€)"] - 2200.0) < 1e-6)
dom = r3["df_giorni"].iloc[6]  # domenica
check("3 dom F1=0: costo 0", abs(dom["Costo (€)"]) < 1e-9)
check("3 dom prezzo medio NaN", pd.isna(r3["df_giorni"].iloc[6]["Prezzo medio (€/MWh)"]))
check("3 quota top10 tra 0 e 100", 0 <= r3["quota_top10_gg_pct"] <= 100)

# ---------- 4. Determinismo ----------
r4a = calcola_calendario_costo(s, 1.0, 2.0, 3.0)
r4b = calcola_calendario_costo(s, 1.0, 2.0, 3.0)
check("4 deterministico", r4a["df_giorni"].equals(r4b["df_giorni"]) and r4a["costo_totale"] == r4b["costo_totale"])

# ---------- 5. NaN scartati ----------
s5 = serie_base(); s5.iloc[10] = np.nan
r5 = calcola_calendario_costo(s5, 1.0, 1.0, 1.0)
check("5 NaN scartato: 14 gg", len(r5["df_giorni"]) == 14)
check("5 NaN: primo giorno costo 2300", abs(r5["df_giorni"]["Costo (€)"].iloc[0] - 2300.0) < 1e-6)

# ---------- 6. Casi limite ----------
rv = calcola_calendario_costo(pd.Series([], dtype=float), 1.0, 1.0, 1.0)
check("6 serie vuota: df vuoto", len(rv["df_giorni"]) == 0 and rv["costo_totale"] is None)
ri = calcola_calendario_costo(pd.Series([100.0, 200.0], index=[0, 1]), 1.0, 1.0, 1.0)
check("6 indice non datetime: df vuoto", len(ri["df_giorni"]) == 0)
rz = calcola_calendario_costo(s, 0.0, 0.0, 0.0)
check("6 MW tutti zero: df vuoto", len(rz["df_giorni"]) == 0)
rn = calcola_calendario_costo(s, "x", 1.0, 1.0)
check("6 MW non numerico: df vuoto", len(rn["df_giorni"]) == 0)

# ---------- 7. Mesi multipli ----------
s7 = serie_base(ore=24 * 45, prezzo=80.0)
r7 = calcola_calendario_costo(s7, 1.0, 1.0, 1.0)
check("7 tre mesi (set/ott/nov)", len(r7["df_mesi"]) == 3 and list(r7["df_mesi"]["Mese"]) == ["2026-09", "2026-10", "2026-11"])
check("7 somma mesi = totale", abs(r7["df_mesi"]["Costo (€)"].sum() - r7["costo_totale"]) < 1e-3)
check("7 prezzo medio mese = 80", abs(r7["df_mesi"]["Prezzo medio (€/MWh)"].iloc[0] - 80.0) < 1e-6)

# ---------- 8. Giorno settimebre: giorni più costosi (prezzi F1 alti) ----------
rng = np.random.default_rng(3)
idx8 = pd.date_range("2026-09-28", periods=24 * 21, freq="h", tz=TZ)
px8 = 60.0 + 40.0 * np.array([1.0 if fascia_oraria(t) == "F1" else 0.0 for t in idx8]) + rng.normal(0, 1, len(idx8))
s8 = pd.Series(px8, index=idx8)
r8 = calcola_calendario_costo(s8, 1.0, 1.0, 1.0)
gs = r8["giorno_sett_piu_costoso"]
check("8 giorno sett in giorni lav", gs["Giorno"] in ("Lun", "Mar", "Mer", "Gio", "Ven"))
check("8 giorno sett N giorni = 3", gs["N giorni"] == 3)

print("FAILURES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
