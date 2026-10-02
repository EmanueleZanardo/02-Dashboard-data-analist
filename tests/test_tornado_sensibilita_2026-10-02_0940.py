"""Standalone test for calcola_tornado_sensibilita - tab150 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_tornado_sensibilita", "_fascia_aeegsi"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_tornado_sensibilita = ns["calcola_tornado_sensibilita"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def flat_hours(n, price, start="2025-01-01", tz=None):
    idx = pd.date_range(start, periods=n, freq="h", tz=tz)
    return pd.Series(np.full(n, price), index=idx, name="p")

KWARGS = dict(mw_f1=1.0, mw_f2=1.0, mw_f3=1.0, p_contr_kw=500.0,
              quota_kw_mese=3.0, oneri_eur_mwh=5.0, delta_pct=10.0)

# --- 1. caso piatto con numeri a mano ---
# 720h = 30gg gennaio 2025 (1 mese, ann=12), prezzo 100, MW=1.0
# ce=72000, cq=500*3*1=1500, co=5*720=3600, base=77100, base_a=925200
r = calcola_tornado_sensibilita(flat_hours(720, 100.0), **KWARGS)
check("piatto: valido e nessun errore", r["valido"] and r["errore"] is None)
check("piatto: n_ore == 720", r["n_ore"] == 720)
check("piatto: n_mesi == 1", r["n_mesi"] == 1)
check("piatto: mwh_tot == 720.0", r["mwh_tot"] == 720.0)
check("piatto: costo_base_annuo == 925200", r["costo_base_annuo"] == 925200.0)
check("piatto: 5 driver", len(r["tornado"]) == 5)
check("piatto: colonne giuste",
      list(r["tornado"].columns) == ["Driver", "Impatto + (EUR/a)", "Impatto - (EUR/a)",
                                    "Ampiezza (EUR/a)", "Quota sul costo (%)"])
exp_order = ["Volumi (MWh)", "Prezzo energia", "Oneri (EUR/MWh)",
             "Quota potenza (EUR/kW)", "Potenza impegnata (kW)"]
check("piatto: ordine driver per ampiezza", list(r["tornado"]["Driver"]) == exp_order)
check("piatto: driver dominante = Volumi (MWh)", r["driver_dominante"] == "Volumi (MWh)")
check("piatto: impatto_max_pos == 90720", r["impatto_max_pos"] == 90720.0)
check("piatto: impatto_max_neg == -90720", r["impatto_max_neg"] == -90720.0)
check("piatto: quota_max_pct == 9.81",
      r["quota_max_pct"] == round(90720.0 / 925200.0 * 100.0, 2) == 9.81)
row = r["tornado"].set_index("Driver")
check("prezzo: +86400 / -86400",
      row.loc["Prezzo energia", "Impatto + (EUR/a)"] == 86400.0
      and row.loc["Prezzo energia", "Impatto - (EUR/a)"] == -86400.0)
check("volumi: +90720 / -90720 (energia + oneri)",
      row.loc["Volumi (MWh)", "Impatto + (EUR/a)"] == 90720.0
      and row.loc["Volumi (MWh)", "Impatto - (EUR/a)"] == -90720.0)
check("quota: +1800 / -1800",
      row.loc["Quota potenza (EUR/kW)", "Impatto + (EUR/a)"] == 1800.0
      and row.loc["Quota potenza (EUR/kW)", "Impatto - (EUR/a)"] == -1800.0)
check("potenza: +1800 / -1800",
      row.loc["Potenza impegnata (kW)", "Impatto + (EUR/a)"] == 1800.0
      and row.loc["Potenza impegnata (kW)", "Impatto - (EUR/a)"] == -1800.0)
check("oneri: +4320 / -4320",
      row.loc["Oneri (EUR/MWh)", "Impatto + (EUR/a)"] == 4320.0
      and row.loc["Oneri (EUR/MWh)", "Impatto - (EUR/a)"] == -4320.0)
check("ampiezze non crescenti",
      bool((r["tornado"]["Ampiezza (EUR/a)"].diff().dropna() <= 0).all()))
check("verdetto cita il dominante", "Volumi (MWh)" in r["verdetto"])
check("verdetto cita ampiezza e totale", "90,720" in r["verdetto"] and "925,200" in r["verdetto"])

# --- 2. delta diverso: linearita' ---
r20 = calcola_tornado_sensibilita(flat_hours(720, 100.0),
                                 **{**KWARGS, "delta_pct": 20.0})
check("delta 20: impatti raddoppiati sul prezzo",
      r20["tornado"].set_index("Driver").loc["Prezzo energia", "Impatto + (EUR/a)"] == 172800.0)

# --- 3. input non validi ---
e1 = calcola_tornado_sensibilita(pd.Series([], dtype=float), **KWARGS)
check("vuota: non valido + errore + tornado vuoto",
      not e1["valido"] and e1["errore"] and e1["tornado"].empty)
e2 = calcola_tornado_sensibilita(flat_hours(10, 100.0), **KWARGS)
check("<24 ore: errore", not e2["valido"] and e2["errore"] is not None)
e3 = calcola_tornado_sensibilita([100.0] * 100, **KWARGS)
check("non-Series: errore", not e3["valido"] and e3["errore"] is not None)
e4 = calcola_tornado_sensibilita(flat_hours(720, 100.0),
                                **{**KWARGS, "mw_f1": 0.0, "mw_f2": 0.0, "mw_f3": 0.0})
check("MW zero: errore", not e4["valido"] and e4["errore"] is not None)
e5 = calcola_tornado_sensibilita(flat_hours(720, 100.0), **{**KWARGS, "delta_pct": 0.0})
check("delta 0: errore", not e5["valido"] and e5["errore"] is not None)
e6 = calcola_tornado_sensibilita(flat_hours(720, 100.0), **{**KWARGS, "delta_pct": 101.0})
check("delta 101: errore", not e6["valido"] and e6["errore"] is not None)
e7 = calcola_tornado_sensibilita(flat_hours(720, 100.0), **{**KWARGS, "p_contr_kw": 0.0})
check("potenza 0: errore", not e7["valido"] and e7["errore"] is not None)
e8 = calcola_tornado_sensibilita(flat_hours(720, 100.0), **{**KWARGS, "quota_kw_mese": -1.0})
check("quota negativa: errore", not e8["valido"] and e8["errore"] is not None)
e9 = calcola_tornado_sensibilita(flat_hours(720, 100.0), **{**KWARGS, "oneri_eur_mwh": -2.0})
check("oneri negativi: errore", not e9["valido"] and e9["errore"] is not None)
e10 = calcola_tornado_sensibilita(flat_hours(720, 100.0), **{**KWARGS, "p_contr_kw": "x"})
check("parametri non numerici: errore", not e10["valido"] and e10["errore"] is not None)
s_ni = flat_hours(720, 100.0)
s_ni.index = pd.RangeIndex(720)
e11 = calcola_tornado_sensibilita(s_ni, **KWARGS)
check("indice non-datetime: errore", not e11["valido"] and e11["errore"] is not None)

# --- 4. NaN e tz-aware ---
s_nan = flat_hours(720, 100.0)
s_nan.iloc[::50] = np.nan
r_nan = calcola_tornado_sensibilita(s_nan, **KWARGS)
check("NaN: valido (dropna)", r_nan["valido"] and r_nan["errore"] is None)
r_tz = calcola_tornado_sensibilita(flat_hours(720, 100.0, tz="Europe/Zurich"), **KWARGS)
check("tz-aware: valido, n_mesi == 1", r_tz["valido"] and r_tz["n_mesi"] == 1)

# --- 5. due mesi -> annualizzazione ---
r_2m = calcola_tornado_sensibilita(flat_hours(1416, 100.0), **KWARGS)  # gen+feb 2025 = 59 gg
check("2 mesi: n_mesi == 2", r_2m["n_mesi"] == 2)
# base periodo = 141600 + 500*3*2 + 5*1416 = 151680 -> annuo x6 = 910080
check("2 mesi: costo annuo annualizzato",
      r_2m["costo_base_annuo"] == round(151680.0 * 6.0, 0))

# --- 6. prezzi negativi su tutto il periodo -> costo base non positivo: errore pulito ---
r_neg = calcola_tornado_sensibilita(flat_hours(720, -20.0), **KWARGS)
check("prezzi negativi piatti: non valido con errore pulito",
      not r_neg["valido"] and r_neg["errore"] is not None
      and r_neg["tornado"].empty)
# prezzi misti (alcune ore negative) ma totale positivo -> valido, segni onesti
s_mix = flat_hours(720, 100.0)
s_mix.iloc[::36] = -50.0  # 20 ore negative
r_mix = calcola_tornado_sensibilita(s_mix, **KWARGS)
check("prezzi misti: valido", r_mix["valido"] and r_mix["errore"] is None)
rm = r_mix["tornado"].set_index("Driver")
check("prezzi misti: shock + sul prezzo aumenta il costo",
      rm.loc["Prezzo energia", "Impatto + (EUR/a)"] > 0)
check("prezzi misti: ampiezze non negative",
      bool((r_mix["tornado"]["Ampiezza (EUR/a)"] >= 0).all()))
check("prezzi misti: costo base annuo coerente",
      r_mix["costo_base_annuo"] == round(((100.0 * 700 + -50.0 * 20) + 1500.0 + 5.0 * 720.0) * 12.0, 0))

# --- 7. determinismo ---
ra = calcola_tornado_sensibilita(flat_hours(720, 100.0), **KWARGS)
rb = calcola_tornado_sensibilita(flat_hours(720, 100.0), **KWARGS)
check("determinismo: tornado identici", ra["tornado"].equals(rb["tornado"]))
check("determinismo: verdetto identico", ra["verdetto"] == rb["verdetto"])

# --- 8. registry tab150 ---
_decl150 = [l for l in src.splitlines() if "st.tabs(" in l and "tab1," in l]
check("registry: tab150 dichiarata",
      any("tab150" in l.split("= st.tabs(")[0] for l in _decl150))
check("registry: titolo presente", '"🎯 Tornado sensibilità"' in src)
check("registry: with tab150 presente", "with tab150:" in src)
check("registry: helper chiamato nella UI",
      "calcola_tornado_sensibilita(prezzi, tn_f1" in src)
check("registry: chiavi widget uniche",
      src.count('key="tn150_') == 7 and src.count('key="csv_tornado"') == 1)

if fails:
    print(f"\n{fails}")
    raise SystemExit(1)
print("\nTUTTI I CHECK VERDI")
