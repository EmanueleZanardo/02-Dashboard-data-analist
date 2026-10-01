"""Test standalone tab141 'Volatilita a termine'.

Estrae calcola_volatilita_termine da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_volatilita_termine_2026-10-02_0040.py
"""
import ast
import os
import re

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_volatilita_termine":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fv = ns["calcola_volatilita_termine"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_giorni_esatti(inizio, medie, tz=None):
    """Serie oraria con prezzo costante dentro ogni giorno = medie[d] (medie giornaliere esatte)."""
    idx = pd.date_range(inizio, periods=len(medie) * 24, freq="h", tz=tz)
    return pd.Series(np.repeat(np.asarray(medie, dtype=float), 24), index=idx)


# --- 1. Prezzi costanti: vol 0, struttura piatta, 3 bucket mensili ---
med = [100.0] * 90  # 2026-01-01 .. 2026-03-31 (31+28+31)
s = serie_giorni_esatti("2026-01-01", med)
r = fv(s)
check("cost.errore_none", r["errore"] is None, r["errore"])
check("cost.valido", r["valido"] is True)
check("cost.n_bucket", r["n_bucket"] == 3, r["n_bucket"])
check("cost.labels", list(r["tabella"]["Bucket"]) == ["2026-01", "2026-02", "2026-03"],
      list(r["tabella"]["Bucket"]))
check("cost.giorni", list(r["tabella"]["Giorni"]) == [31, 28, 31],
      list(r["tabella"]["Giorni"]))
check("cost.vol_zero", (r["tabella"]["Vol annua (€/MWh)"] == 0).all())
check("cost.media_zero", r["media"] == 0.0, r["media"])
check("cost.front_zero", r["front"] == 0.0, r["front"])
check("cost.slope_zero", r["slope"] == 0.0, r["slope"])
check("cost.rapporto_none", r["rapporto"] is None, r["rapporto"])
check("cost.verdetto_piatta", "piatta" in r["verdetto"].lower(), r["verdetto"])
check("cost.n_variazioni", len(r["serie_variazioni"]) == 89, len(r["serie_variazioni"]))

# --- 2. Alternanza 100/102: vol attesa esatta = std(changes,ddof=1)*sqrt(252) ---
# (le variazioni sono datate al giorno d: medie[d]-medie[d-1]; il primo bucket
#  ha giorni-1 variazioni, gli altri hanno tante variazioni quanti giorni)
med2 = [100.0, 102.0] * 45  # 90 giorni: gen(31)/feb(28)/mar(31), variazioni +-2
s2 = serie_giorni_esatti("2026-01-01", med2)
r2 = fv(s2)
med_arr = np.asarray(med2)
exp_v = {}
for _m, _dd in (("2026-01", range(1, 31)), ("2026-02", range(31, 59)), ("2026-03", range(59, 90))):
    _chg = med_arr[list(_dd)] - med_arr[[d - 1 for d in _dd]]
    exp_v[_m] = float(np.std(_chg, ddof=1)) * np.sqrt(252.0)
exp_vols = [exp_v["2026-01"], exp_v["2026-02"], exp_v["2026-03"]]
exp_slope = float(np.cov(np.arange(3.0), np.array(exp_vols), ddof=0)[0, 1]
                  / np.var(np.arange(3.0)))
tab2 = r2["tabella"]
check("alt.errore_none", r2["errore"] is None, r2["errore"])
check("alt.valido", r2["valido"] is True)
check("alt.n_bucket", r2["n_bucket"] == 3, r2["n_bucket"])
check("alt.vol_mesi", all(abs(a - round(e, 2)) < 0.011 for a, e in
                          zip(tab2["Vol annua (€/MWh)"], exp_vols)),
      list(tab2["Vol annua (€/MWh)"]))
exp_pct_gen = round(exp_v["2026-01"] / (3130.0 / 31) * 100, 1)
check("alt.vol_pct", abs(tab2["Vol annua (% prezzo)"].iloc[0] - exp_pct_gen) < 0.06,
      tab2["Vol annua (% prezzo)"].iloc[0])
check("alt.slope_ols", abs(r2["slope"] - exp_slope) < 1e-9, f"{r2['slope']} vs {exp_slope}")
check("alt.rapporto", abs(r2["rapporto"] - max(exp_vols) / min(exp_vols)) < 1e-9, r2["rapporto"])

# --- 3. Due regimi: vol bassa gen-feb, alta mar-apr -> contango, slope > 0 ---
reg1 = [100.0, 101.0] * 30          # 60 giorni, variazioni +-1
reg2 = [100.0, 104.0] * 30
med3 = (reg1 + reg2)[:59] + (reg2 * 2)[:61]  # 59 gg regime1 (gen+feb), 61 gg regime2 (mar+apr)
med3 = med3[:120]
s3 = serie_giorni_esatti("2026-01-01", med3)
r3 = fv(s3)
check("reg.valido", r3["valido"] is True)
check("reg.n_bucket", r3["n_bucket"] == 4, r3["n_bucket"])
check("reg.slope_pos", r3["slope"] is not None and r3["slope"] > 0, r3["slope"])
check("reg.verdetto_contango", "Contango" in r3["verdetto"], r3["verdetto"])
check("reg.max_in_mar_apr", r3["bucket_max"] in ("2026-03", "2026-04"), r3["bucket_max"])
check("reg.min_in_gen_feb", r3["bucket_min"] in ("2026-01", "2026-02"), r3["bucket_min"])
check("reg.rapporto_gt1", r3["rapporto"] is not None and r3["rapporto"] > 2.0, r3["rapporto"])

# --- 4. Bucket trimestrali ---
r4 = fv(s3, bucket="trimestre")
check("tri.n_bucket", r4["n_bucket"] == 2, r4["n_bucket"])
check("tri.labels", list(r4["tabella"]["Bucket"]) == ["2026Q1", "2026Q2"],
      list(r4["tabella"]["Bucket"]))
check("tri.giorni", list(r4["tabella"]["Giorni"]) == [90, 30], list(r4["tabella"]["Giorni"]))
check("tri.valido", r4["valido"] is True)

# --- 5. Bucket esclusi -> errore pulito ---
r5 = fv(s3, min_giorni=200)
check("esc.errore", r5["errore"] is not None and "Nessun bucket" in r5["errore"], r5["errore"])

# --- 6. Input non validi -> errore pulito, mai eccezioni ---
r6a = fv(pd.Series([], dtype=float))
check("err.vuota", r6a["errore"] is not None, "serie vuota senza errore")
r6b = fv(pd.Series([1.0, 2.0, 3.0]))
check("err.no_datetime", r6b["errore"] is not None and "temporale" in r6b["errore"], r6b["errore"])
r6c = fv(serie_giorni_esatti("2026-01-01", [100.0]))  # 24 ore
check("err.corta", r6c["errore"] is not None, "serie 24h senza errore")
r6d = fv(s, bucket="anno")
check("err.bucket", r6d["errore"] is not None and "mese" in r6d["errore"], r6d["errore"])
r6e = fv(s, min_giorni=1)
check("err.ming", r6e["errore"] is not None, "min_giorni=1 senza errore")
r6f = fv([100.0] * 100)
check("err.lista", r6f["errore"] is not None, "lista senza errore")

# --- 7. Prezzi negativi ammessi, nessun NaN in tabella ---
med7 = [-5.0, 5.0] * 35  # 70 giorni: gen+feb -> 2 bucket
r7 = fv(serie_giorni_esatti("2026-01-01", med7))
check("neg.valido", r7["valido"] is True and r7["errore"] is None)
check("neg.vol_pos", r7["media"] > 0, r7["media"])
check("neg.no_nan_vol", r7["tabella"]["Vol annua (€/MWh)"].notna().all())

# --- 8. tz-aware -> stesso risultato del naive (periodo senza DST: gen+feb) ---
s8z = serie_giorni_esatti("2026-01-01", med3[:59], tz="Europe/Zurich")
s8n = serie_giorni_esatti("2026-01-01", med3[:59])
r8z, r8n = fv(s8z), fv(s8n)
check("tz.stesso_n", r8z["n_bucket"] == r8n["n_bucket"])
check("tz.stessa_media", abs(r8z["media"] - r8n["media"]) < 1e-9, (r8z["media"], r8n["media"]))

# --- 9. NaN orari ignorati ---
s9 = serie_giorni_esatti("2026-01-01", med3[:90]).copy()
s9.iloc[::37] = np.nan
r9 = fv(s9)
check("nan.ok", r9["errore"] is None and r9["valido"], r9["errore"])

# --- 10. Determinismo ---
ra, rb = fv(s3), fv(s3)
check("det.tabella", ra["tabella"].equals(rb["tabella"]))
check("det.slope", ra["slope"] == rb["slope"])

# --- 11. Un solo bucket -> struttura non stimabile ma tabella presente ---
r11 = fv(serie_giorni_esatti("2026-01-01", [100.0, 102.0] * 10), min_bucket=2)
check("uno.non_valido", r11["valido"] is False)
check("uno.verdetto", "non stimabile" in r11["verdetto"], r11["verdetto"])
check("uno.tabella_1riga", len(r11["tabella"]) == 1)
check("uno.slope_none", r11["slope"] is None)

# --- 12. Registry tab141 in app.py ---
src = open(APP, encoding="utf-8").read()
m = re.search(r"tab139, tab140, tab141 = st\.tabs\(\[(.*?)\]\)", src, re.S)
check("reg.dichiarazione", m is not None)
check("reg.titolo", m is not None and "🌊 Volatilità a termine" in m.group(1))
check("reg.with", "    with tab141:" in src)
check("reg.keys_uniche", src.count('key="vt141_bucket"') == 1 and src.count('key="csv_vol_termine"') == 1)

print(f"{checks} check / {len(fails)} fail")
if fails:
    print("FAIL:")
    for f in fails:
        print(" -", f)
    raise SystemExit(1)
