"""Test standalone tab135 'Premio di rischio ex-post del forward'.

Estrae calcola_premio_rischio da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_premio_rischio_2026-10-01_1740.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_premio_rischio":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
pr = ns["calcola_premio_rischio"]

E = "\u20ac/MWh"
COL_P = "Premio Base (" + E + ")"
COL_PP = "Premio Base (%)"
COL_PPK = "Premio Peak (" + E + ")"

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_trend():
    # 6 mesi pieni, prezzo costante per mese: 100,110,120,130,140,150
    idx = pd.date_range("2026-01-01", "2026-07-01", freq="h", inclusive="left")
    vals = np.concatenate([
        np.full(len(pd.date_range(f"2026-{m:02d}-01",
                                  f"2026-{m + 1:02d}-01" if m < 6 else "2026-07-01",
                                  freq="h", inclusive="left")),
                100.0 + 10 * (m - 1))
        for m in range(1, 7)
    ])
    return pd.Series(vals, index=idx)


# --- 1. serie piatta: premio zero ovunque ---
s_flat = pd.Series(100.0, index=pd.date_range("2026-01-01", "2026-07-01",
                                              freq="h", inclusive="left"))
r = pr(s_flat, lookback_mesi=3)
check("flat ok", r["ok"] and r["n_mesi"] == 3, (r["ok"], r["n_mesi"]))
check("flat premi base zero", (r["df"][COL_P] == 0.0).all(),
      r["df"][COL_P].tolist())
check("flat premi peak zero", (r["df"][COL_PPK] == 0.0).all(),
      r["df"][COL_PPK].tolist())
check("flat premi pct zero", (r["df"][COL_PP] == 0.0).all(),
      r["df"][COL_PP].tolist())
check("flat premio medio 0", r["premio_medio_base"] == 0.0,
      r["premio_medio_base"])
check("flat quota positivi 0", r["quota_mesi_positivi"] == 0.0,
      r["quota_mesi_positivi"])
check("flat mesi", r["df"]["Mese consegna"].tolist() ==
      ["2026-04", "2026-05", "2026-06"], r["df"]["Mese consegna"].tolist())
check("flat mese ultimo", r["mese_ultimo"] == "2026-06", r["mese_ultimo"])

# --- 2. trend crescente: premio negativo esatto ---
s_tr = serie_trend()
r2 = pr(s_tr, lookback_mesi=3)
check("trend ok", r2["ok"] and r2["n_mesi"] == 3, (r2["ok"], r2["n_mesi"]))
# aprile: formazione gen+feb+mar = (100*31+110*28+120*31)/90 = 110.0 esatto
pa = r2["df"].loc[r2["df"]["Mese consegna"] == "2026-04", COL_P].iloc[0]
check("trend premio aprile -20", abs(pa - (-20.0)) < 1e-9, pa)
# maggio: formazione pesata sui giorni
fm = (110 * 28 + 120 * 31 + 130 * 30) / (28 + 31 + 30)
pm_att = round(fm - 140.0, 2)
pm = r2["df"].loc[r2["df"]["Mese consegna"] == "2026-05", COL_P].iloc[0]
check("trend premio maggio pesato", abs(pm - pm_att) < 1e-9, (pm, pm_att))
check("trend premio medio", abs(r2["premio_medio_base"] -
      round(float(r2["df"][COL_P].mean()), 2)) < 1e-9, r2["premio_medio_base"])
check("trend tutti negativi", (r2["df"][COL_P] < 0).all(),
      r2["df"][COL_P].tolist())
i_bm = r2["df"][COL_P].abs().idxmax()
check("trend bias max = aprile",
      r2["mese_bias_max"] == "2026-04" and
      abs(r2["bias_max_assoluto"] - (-20.0)) < 1e-9,
      (r2["mese_bias_max"], r2["bias_max_assoluto"]))
check("trend ultimo mese giugno",
      r2["mese_ultimo"] == "2026-06" and
      abs(r2["premio_ultimo_mese"] - r2["df"][COL_P].iloc[-1]) < 1e-9,
      (r2["mese_ultimo"], r2["premio_ultimo_mese"]))
# pct coerente: premio/S*100 sul realizzato
row = r2["df"].iloc[0]
check("trend pct coerente",
      abs(row[COL_PP] - row[COL_P] / 130.0 * 100) < 0.01, row[COL_PP])

# --- 3. lookback 1: premio = -10 esatto ogni mese ---
r3 = pr(s_tr, lookback_mesi=1)
check("lb1 n_mesi 5", r3["ok"] and r3["n_mesi"] == 5,
      (r3["ok"], r3["n_mesi"]))
check("lb1 premi -10", ((r3["df"][COL_P] - (-10.0)).abs() < 1e-9).all(),
      r3["df"][COL_P].tolist())

# --- 4. lookback 6: un solo mese di consegna ---
r4 = pr(s_tr, lookback_mesi=6)
check("lb6 n_mesi 1", r4["ok"] and r4["n_mesi"] == 1,
      (r4["ok"], r4["n_mesi"]))
# formazione gen..mag pesata
fm6 = (100 * 31 + 110 * 28 + 120 * 31 + 130 * 30 + 140 * 31) / 151
check("lb6 premio giugno", abs(r4["df"][COL_P].iloc[0] - round(fm6 - 150, 2)) < 1e-9,
      (r4["df"][COL_P].iloc[0], round(fm6 - 150, 2)))

# --- 5. input non validi ---
check("lookback 0", not pr(s_flat, lookback_mesi=0)["ok"])
check("lookback -2", not pr(s_flat, lookback_mesi=-2)["ok"])
check("lookback 2.5", not pr(s_flat, lookback_mesi=2.5)["ok"])
check("copertura 0", not pr(s_flat, copertura_min=0)["ok"])
check("copertura 1.5", not pr(s_flat, copertura_min=1.5)["ok"])
check("serie vuota", not pr(pd.Series(dtype=float))["ok"])
check("indice non datetime",
      not pr(pd.Series([1.0, 2.0], index=[0, 1]))["ok"])
check("un solo mese", not pr(pd.Series(
    100.0, index=pd.date_range("2026-01-01", "2026-02-01", freq="h",
                               inclusive="left")), lookback_mesi=3)["ok"])

# --- 6. NaN e buchi: saltati onestamente, mai crash ---
s_nan = s_flat.copy()
s_nan.iloc[1000:2000] = np.nan
rn = pr(s_nan, lookback_mesi=3)
check("nan non crasha", rn["ok"] and rn["n_mesi"] == 3,
      (rn["ok"], rn["n_mesi"]))
s_allnan_m = s_flat.copy()
s_allnan_m.loc["2026-04"] = np.nan  # mese di consegna tutto NaN
ra = pr(s_allnan_m, lookback_mesi=3)
check("mese consegna NaN saltato",
      ra["ok"] and "2026-04" not in ra["df"]["Mese consegna"].tolist(),
      ra["df"]["Mese consegna"].tolist())
# febbraio interamente mancante: gen+mar=1488h < 0.7*2160 -> aprile saltato;
# per maggio formazione feb+mar+apr = 1464h < 0.7*2136 -> saltato anche lui
idx2 = pd.date_range("2026-01-01", "2026-07-01", freq="h", inclusive="left")
s_short = pd.Series(100.0, index=idx2)
s_short = s_short.drop(s_short.loc["2026-02"].index)
rs = pr(s_short, lookback_mesi=3)
check("formazione scarsa: aprile e maggio saltati",
      rs["ok"] and rs["df"]["Mese consegna"].tolist() == ["2026-06"],
      rs["df"]["Mese consegna"].tolist())

# --- 7. duplicati e disordine ---
s_dup = pd.concat([s_flat, s_flat.iloc[:100]])
s_shuf = s_flat.sample(frac=1.0, random_state=7)
rd = pr(s_dup, lookback_mesi=3)
rh = pr(s_shuf, lookback_mesi=3)
check("duplicati gestiti", rd["ok"] and rd["n_mesi"] == 3,
      (rd["ok"], rd["n_mesi"]))
check("disordine gestito", rh["ok"] and rh["df"].equals(r["df"]),
      rh["n_mesi"])

# --- 8. determinismo ---
r_a = pr(s_tr, lookback_mesi=2)
r_b = pr(s_tr, lookback_mesi=2)
check("determinismo df", r_a["df"].equals(r_b["df"]))
check("determinismo kpi",
      r_a["premio_medio_base"] == r_b["premio_medio_base"] and
      r_a["quota_mesi_positivi"] == r_b["quota_mesi_positivi"])

# --- 9. copertura_min=1.0: l'ora mancante in gennaio invalida le finestre
# di formazione di feb, mar e apr -> nessun mese di consegna, ok False
idx3 = pd.date_range("2026-01-01", "2026-05-01", freq="h", inclusive="left")
s_miss = pd.Series(100.0, index=idx3).drop(idx3[500])
r_strict = pr(s_miss, lookback_mesi=3, copertura_min=1.0)
check("copertura 1.0: nessun mese valido",
      (not r_strict["ok"]) and r_strict["n_mesi"] == 0,
      (r_strict["ok"], r_strict["n_mesi"]))
r_lax = pr(s_miss, lookback_mesi=3, copertura_min=0.7)
check("copertura 0.7: aprile incluso",
      r_lax["ok"] and "2026-04" in r_lax["df"]["Mese consegna"].tolist(),
      r_lax["df"]["Mese consegna"].tolist())

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
