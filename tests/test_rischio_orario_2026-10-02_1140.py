"""Standalone test for calcola_rischio_orario - tab152 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_rischio_orario", "_fascia_aeegsi"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_rischio_orario = ns["calcola_rischio_orario"]

fails = []
n_checks = [0]
def check(name, cond):
    n_checks[0] += 1
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def flat_hours(n_days, price, start="2026-01-01"):
    idx = pd.date_range(start, periods=n_days * 24, freq="h")
    return pd.Series(np.full(n_days * 24, float(price)), index=idx)

def spike_hours(n_days, ora_spike=19, base=100.0, alto=200.0, basso=50.0,
                start="2026-01-01"):
    """Solo ora_spike varia (alterna alto/basso a giorni alterni)."""
    idx = pd.date_range(start, periods=n_days * 24, freq="h")
    vals = np.full(n_days * 24, float(base))
    ore = idx.hour.to_numpy()
    gg = np.arange(n_days * 24) // 24
    mask = ore == ora_spike
    vals[mask] = np.where(gg[mask] % 2 == 0, alto, basso)
    return pd.Series(vals, index=idx)

# --- 1. serie piatta: costo giornaliero costante -> errore pulito ---
r = calcola_rischio_orario(flat_hours(60, 100.0))
check("piatto: non valido con errore", not r["valido"] and r["errore"] is not None)
check("piatto: errore parla di costante", "costante" in r["errore"])

# --- 2. solo ora 19 varia -> contributo 19 ~= 100%, somma Euler = 100 ---
r = calcola_rischio_orario(spike_hours(60, ora_spike=19))
check("spike: valido", r["valido"] and r["errore"] is None)
check("spike: n_giorni == 60", r["n_giorni"] == 60)
tab = r["tabella"]
contrib = tab["Contributo rischio (%)"].to_numpy()
check("spike: somma contributi == 100 (Euler)", abs(contrib.sum() - 100.0) < 0.15)
c19 = float(tab.loc[tab["Ora"] == "19:00", "Contributo rischio (%)"].iloc[0])
check("spike: ora 19 spiega ~100%", abs(c19 - 100.0) < 0.05)
altri = np.delete(contrib, 19)
check("spike: altre ore ~0%", np.all(np.abs(altri) < 0.05))
check("spike: ora_top == 19", r["ora_top"] == 19)
check("spike: top3_conc ~100%", abs(r["top3_conc"] - 100.0) < 0.05)
check("spike: verdetto cita 19:00", "19:00" in r["verdetto"])

# --- 3. quota costo somma a 100 ---
# tolleranza 0.15: la tabella espone valori arrotondati a 2 decimali,
# l'errore di arrotondamento su 24 righe puo' arrivare a 0.12
quota = tab["Quota costo (%)"].to_numpy()
check("quota costo somma 100", abs(quota.sum() - 100.0) < 0.15)

# --- 4. leva: ora volatile con piccola quota di costo -> leva > 1 ---
r2 = calcola_rischio_orario(spike_hours(60, ora_spike=3, base=100.0, alto=300.0, basso=100.0))
t2 = r2["tabella"]
leva3 = float(t2.loc[t2["Ora"] == "03:00", "Leva rischio (x)"].iloc[0])
quota3 = float(t2.loc[t2["Ora"] == "03:00", "Quota costo (%)"].iloc[0])
check("leva: ora 3 ha leva > 5", leva3 > 5.0)
check("leva: ora 3 quota costo < 10%", quota3 < 10.0)

# --- 5. errori puliti ---
r = calcola_rischio_orario(pd.Series(dtype=float))
check("vuota: errore", not r["valido"] and r["errore"] is not None)
s = flat_hours(60, 100.0)
s.index = pd.RangeIndex(len(s))
r = calcola_rischio_orario(s)
check("indice non-datetime: errore", not r["valido"] and "datetime" in r["errore"])
r = calcola_rischio_orario(spike_hours(20, ora_spike=19))
check("troppo corta: errore", not r["valido"] and "corta" in r["errore"])
r = calcola_rischio_orario(spike_hours(60, ora_spike=19), mw_f1=-1.0)
check("mw negativo: errore", not r["valido"] and "mw_f1" in r["errore"])
r = calcola_rischio_orario(spike_hours(60, ora_spike=19), mw_f1=0.0, mw_f2=0.0, mw_f3=0.0)
check("mw tutti zero: errore", not r["valido"])
r = calcola_rischio_orario(spike_hours(60, ora_spike=19), min_giorni=5)
check("min_giorni < 10: errore", not r["valido"])

# --- 6. tz-aware -> reso naive, nessun errore ---
s = spike_hours(60, ora_spike=19).tz_localize("Europe/Zurich")
r = calcola_rischio_orario(s)
check("tz-aware: valido", r["valido"] and r["errore"] is None)
check("tz-aware: ora_top == 19", r["ora_top"] == 19)

# --- 7. NaN gestiti ---
s = spike_hours(60, ora_spike=19).copy()
s.iloc[::97] = np.nan
r = calcola_rischio_orario(s)
check("NaN: valido", r["valido"] and r["errore"] is None)
check("NaN: ora_top == 19", r["ora_top"] == 19)

# --- 8. determinismo ---
a = calcola_rischio_orario(spike_hours(60, ora_spike=19))
b = calcola_rischio_orario(spike_hours(60, ora_spike=19))
check("deterministico: tabelle identiche",
      a["tabella"].to_csv(index=False) == b["tabella"].to_csv(index=False)
      and a["verdetto"] == b["verdetto"])

# --- 9. colonne tabella e KPI coerenti ---
check("colonne tabella", list(a["tabella"].columns) ==
      ["Ora", "Costo medio (€/g)", "Quota costo (%)", "Volatilità (€/g)",
       "Contributo rischio (%)", "Leva rischio (x)"])
check("24 righe", len(a["tabella"]) == 24)
check("vol_giornaliera > 0", a["vol_giornaliera"] > 0)
check("costo_medio_giorno > 0", a["costo_medio_giorno"] > 0)
check("contrib_top in (0,100]", 0 < a["contrib_top"] <= 100.0)

print()
if fails:
    print("FAILURES:", fails)
    raise SystemExit(1)
print("ALL GREEN (%d checks)" % n_checks[0])
