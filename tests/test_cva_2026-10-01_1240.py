"""Test standalone tab127 'CVA controparte'.

Estrae calcola_cva + CVA_RATING_PD da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_cva_2026-10-01_1240.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())


class _FakeSt:
    @staticmethod
    def cache_data(*a, **k):
        def deco(fn):
            return fn
        return deco


ns = {"np": np, "pd": pd, "st": _FakeSt()}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_cva":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
    elif isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == "CVA_RATING_PD":
                exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
cva = ns["calcola_cva"]
RATING = ns["CVA_RATING_PD"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


# --- 1. formula esatta a orizzonte 1 ---
r = cva({"A": 100000.0}, pd_annua_pct=2.0, lgd_pct=50.0, orizzonte_anni=1.0)
check("valido base", r["valido"] and r["errore"] is None)
check("cva esatto", abs(r["cva_totale"] - 100000.0 * 0.02 * 0.5) < 1e-9,
      r["cva_totale"])
check("ead esatta", r["df"].loc[0, "EAD (EUR)"] == 100000.0)
check("pd_periodo t=1", abs(r["pd_periodo"] - 0.02) < 1e-12, r["pd_periodo"])
check("n_controparti", r["n_controparti"] == 1)
check("n_esposte", r["n_esposte"] == 1)

# --- 2. PD periodo su orizzonte 2 anni ---
r2 = cva({"A": 100000.0}, pd_annua_pct=2.0, lgd_pct=50.0, orizzonte_anni=2.0)
att_pd = 1.0 - 0.98 ** 2
check("pd_periodo t=2", abs(r2["pd_periodo"] - att_pd) < 1e-12, r2["pd_periodo"])
check("cva t=2", abs(r2["cva_totale"] - 100000.0 * att_pd * 0.5) < 1e-9,
      r2["cva_totale"])

# --- 3. MtM negativo e zero non contribuiscono ---
r3 = cva({"Neg": -60000.0, "Zero": 0.0}, pd_annua_pct=2.0, lgd_pct=50.0)
check("mtm neg cva 0", r3["cva_totale"] == 0.0, r3["cva_totale"])
check("mtm neg ead 0",
      (r3["df"]["EAD (EUR)"] == 0.0).all())
check("nessuna esposta", r3["n_esposte"] == 0)
check("peggior None se 0", r3["peggior_controparte"] is None)

# --- 4. multi-controparte: somma, quote, peggiore ---
r4 = cva({"A": 100000.0, "B": 200000.0, "C": -50000.0},
         pd_annua_pct=1.0, lgd_pct=45.0, orizzonte_anni=1.0)
att4 = (100000.0 + 200000.0) * 0.01 * 0.45
check("somma multi", abs(r4["cva_totale"] - att4) < 1e-9, r4["cva_totale"])
check("somma df = totale",
      abs(r4["df"]["CVA (EUR)"].sum() - r4["cva_totale"]) < 1e-9)
check("quote sommano 1", abs(r4["df"]["Quota"].sum() - 1.0) < 1e-12,
      r4["df"]["Quota"].sum())
check("peggior controparte", r4["peggior_controparte"] == "B",
      r4["peggior_controparte"])
check("cva_peggiore", abs(r4["cva_peggiore"] - 200000.0 * 0.01 * 0.45) < 1e-9)
check("quota_peggiore",
      abs(r4["quota_peggiore"] - r4["cva_peggiore"] / r4["cva_totale"]) < 1e-12)
check("n_esposte 2 su 3", r4["n_esposte"] == 2 and r4["n_controparti"] == 3)

# --- 5. PD=0 o LGD=0 -> CVA 0 ---
r5a = cva({"A": 100000.0}, pd_annua_pct=0.0, lgd_pct=45.0)
r5b = cva({"A": 100000.0}, pd_annua_pct=2.0, lgd_pct=0.0)
check("pd 0 -> cva 0", r5a["cva_totale"] == 0.0)
check("lgd 0 -> cva 0", r5b["cva_totale"] == 0.0)

# --- 6. linearita' in PD a orizzonte 1 ---
rb = cva({"A": 100000.0}, pd_annua_pct=1.0, lgd_pct=45.0, orizzonte_anni=1.0)
rd = cva({"A": 100000.0}, pd_annua_pct=2.0, lgd_pct=45.0, orizzonte_anni=1.0)
check("pd doppia -> cva doppio a t=1",
      abs(rd["cva_totale"] - 2.0 * rb["cva_totale"]) < 1e-9)

# --- 7. input lista: nomi generati / nomi param ---
r7 = cva([50000.0, -10000.0], pd_annua_pct=1.0, lgd_pct=45.0)
check("nomi generati",
      list(r7["df"]["Nome"]) == ["Controparte 1", "Controparte 2"],
      list(r7["df"]["Nome"]))
r7b = cva([50000.0, 30000.0], pd_annua_pct=1.0, lgd_pct=45.0,
          nomi=["Alpha", "Beta"])
check("nomi param", list(r7b["df"]["Nome"]) == ["Alpha", "Beta"])

# --- 8. rating mapping ---
check("7 rating", set(RATING.keys()) == {"AAA", "AA", "A", "BBB", "BB", "B", "CCC"},
      sorted(RATING.keys()))
vals = [RATING[k] for k in ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]]
check("rating crescenti", all(b > a for a, b in zip(vals, vals[1:])), vals)
check("rating in (0,100)", all(0 < v < 100 for v in vals))

# --- 9. validazione input ---
re_ = cva({})
check("dict vuoto -> errore", re_["errore"] is not None and not re_["valido"])
re_ = cva([])
check("lista vuota -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0, "A ": 200.0})
check("nomi duplicati (strip) -> errore", re_["errore"] is not None, re_["errore"])
re_ = cva({"": 100.0})
check("nome vuoto -> errore", re_["errore"] is not None)
re_ = cva({"A": "x"})
check("mtm non numerico -> errore", re_["errore"] is not None)
re_ = cva({"A": 1e13})
check("mtm oltre limite -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0} | {f"C{i}": 1.0 for i in range(50)})
check(">50 controparti -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, pd_annua_pct=-1.0)
check("pd negativa -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, pd_annua_pct=101.0)
check("pd >100 -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, lgd_pct=-5.0)
check("lgd negativa -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, lgd_pct=120.0)
check("lgd >100 -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, orizzonte_anni=0.0)
check("orizzonte 0 -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, orizzonte_anni=31.0)
check("orizzonte >30 -> errore", re_["errore"] is not None)
re_ = cva({"A": 100.0}, pd_annua_pct="x")
check("pd non numerica -> errore", re_["errore"] is not None)

# --- 10. scenari e sensibilita' ---
r10 = cva({"A": 100000.0, "B": 50000.0}, pd_annua_pct=2.0, lgd_pct=50.0,
          orizzonte_anni=1.0)
check("scenari_pd keys", set(r10["scenari_pd"].keys()) == {0.5, 2.0, 5.0})
check("scenario pd 2x = 2x base a t=1",
      abs(r10["scenari_pd"][2.0] - 2.0 * r10["cva_totale"]) < 1e-9)
check("scenari_lgd keys", set(r10["scenari_lgd"].keys()) == {-20.0, 20.0})
base_lgd = 150000.0 * 0.02 * 0.5
check("lgd +20pp",
      abs(r10["scenari_lgd"][20.0] - 150000.0 * 0.02 * 0.7) < 1e-9,
      r10["scenari_lgd"][20.0])
check("lgd -20pp",
      abs(r10["scenari_lgd"][-20.0] - 150000.0 * 0.02 * 0.3) < 1e-9)
check("sens_orizzonte keys", set(r10["sens_orizzonte"].keys()) == {0.5, 1.0, 2.0})
check("orizzonte 1x = base",
      abs(r10["sens_orizzonte"][1.0] - r10["cva_totale"]) < 1e-9)
check("orizzonte cresce con t",
      r10["sens_orizzonte"][0.5] < r10["sens_orizzonte"][1.0] < r10["sens_orizzonte"][2.0])

# --- 11. struttura df ---
cols_att = ["Nome", "MtM (EUR)", "EAD (EUR)", "PD annua (%)", "PD periodo (%)",
            "LGD (%)", "CVA (EUR)", "Quota"]
check("df columns", list(r10["df"].columns) == cols_att, list(r10["df"].columns))
check("df righe", len(r10["df"]) == 2)

# --- 12. clamp PD negli scenari (pd*f oltre 100%) ---
r12 = cva({"A": 100000.0}, pd_annua_pct=60.0, lgd_pct=50.0, orizzonte_anni=1.0)
check("scenario pd 5x clamp a 100%",
      abs(r12["scenari_pd"][5.0] - 100000.0 * 1.0 * 0.5) < 1e-9,
      r12["scenari_pd"][5.0])

print(f"checks: {checks}, fails: {len(fails)}")
for f_ in fails:
    print("FAIL:", f_)
raise SystemExit(1 if fails else 0)
