"""Test standalone tab128 'LCOS batteria'.

Estrae calcola_lcos da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_lcos_2026-10-01_1340.py
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
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_lcos":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
lcos = ns["calcola_lcos"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


# --- 1. formula esatta: degrado=0, eff=100%, tasso=0 ---
# E_dis = 365 * 1000/1000 * 0.9 = 328.5 MWh/anno; E_ch uguale
# LCOS = (350000 + 10*(7000 + 328.5*80)) / (10*328.5)
r = lcos(350000.0, opex_annuo_eur=7000.0, capacita_kwh=1000.0,
         cicli_annui=365.0, dod=0.9, efficienza_pct=100.0,
         degrado_annuo_pct=0.0, tasso_sconto_pct=0.0, vita_anni=10,
         costo_ricarica_eur_mwh=80.0)
check("valido base", r["valido"] and r["errore"] is None)
e_dis = 365.0 * 1.0 * 0.9
att = (350000.0 + 10 * (7000.0 + e_dis * 80.0)) / (10 * e_dis)
check("lcos esatto", abs(r["lcos_eur_mwh"] - att) < 1e-9,
      (r["lcos_eur_mwh"], att))
check("energia annua", abs(r["energia_annua_mwh"] - e_dis) < 1e-9,
      r["energia_annua_mwh"])
check("pv energia = 10*E", abs(r["pv_energia_mwh"] - 10 * e_dis) < 1e-9,
      r["pv_energia_mwh"])
check("pv costi esatto",
      abs(r["pv_costi_eur"] - (350000.0 + 10 * (7000.0 + e_dis * 80.0))) < 1e-6,
      r["pv_costi_eur"])
check("df 10 righe", len(r["df"]) == 10, len(r["df"]))

# --- 2. efficienza < 100% alza il LCOS (piu' energia da comprare) ---
r2 = lcos(350000.0, opex_annuo_eur=7000.0, capacita_kwh=1000.0,
          cicli_annui=365.0, dod=0.9, efficienza_pct=85.0,
          degrado_annuo_pct=0.0, tasso_sconto_pct=0.0, vita_anni=10,
          costo_ricarica_eur_mwh=80.0)
check("eff peggiore -> lcos maggiore", r2["lcos_eur_mwh"] > r["lcos_eur_mwh"],
      (r2["lcos_eur_mwh"], r["lcos_eur_mwh"]))
e_ch = e_dis / 0.85
att2 = (350000.0 + 10 * (7000.0 + e_ch * 80.0)) / (10 * e_dis)
check("lcos eff85 esatto", abs(r2["lcos_eur_mwh"] - att2) < 1e-9,
      (r2["lcos_eur_mwh"], att2))

# --- 3. degrado riduce l'energia e alza il LCOS ---
r3 = lcos(350000.0, opex_annuo_eur=7000.0, capacita_kwh=1000.0,
          cicli_annui=365.0, dod=0.9, efficienza_pct=100.0,
          degrado_annuo_pct=2.0, tasso_sconto_pct=0.0, vita_anni=10,
          costo_ricarica_eur_mwh=80.0)
check("degrado -> lcos maggiore", r3["lcos_eur_mwh"] > r["lcos_eur_mwh"],
      (r3["lcos_eur_mwh"], r["lcos_eur_mwh"]))
e_tot = sum(e_dis * 0.98 ** (t - 1) for t in range(1, 11))
check("pv energia degradata", abs(r3["pv_energia_mwh"] - e_tot) < 1e-9,
      r3["pv_energia_mwh"])

# --- 4. raddoppio cicli riduce il LCOS ---
r4 = lcos(350000.0, opex_annuo_eur=7000.0, capacita_kwh=1000.0,
          cicli_annui=730.0, dod=0.9, efficienza_pct=100.0,
          degrado_annuo_pct=0.0, tasso_sconto_pct=0.0, vita_anni=10,
          costo_ricarica_eur_mwh=80.0)
check("doppi cicli -> lcos minore", r4["lcos_eur_mwh"] < r["lcos_eur_mwh"],
      (r4["lcos_eur_mwh"], r["lcos_eur_mwh"]))

# --- 5. valore residuo riduce il PV costi ---
r5 = lcos(350000.0, opex_annuo_eur=7000.0, capacita_kwh=1000.0,
          cicli_annui=365.0, dod=0.9, efficienza_pct=100.0,
          degrado_annuo_pct=0.0, tasso_sconto_pct=0.0, vita_anni=10,
          costo_ricarica_eur_mwh=80.0, valore_residuo_eur=50000.0)
check("residuo riduce pv costi",
      abs(r5["pv_costi_eur"] - (r["pv_costi_eur"] - 50000.0)) < 1e-6,
      r5["pv_costi_eur"])
check("quota residuo", abs(r5["quota_residuo"] - 50000.0 / r5["pv_costi_eur"]) < 1e-12,
      r5["quota_residuo"])

# --- 6. tasso di sconto: fattori di sconto applicati ---
r6 = lcos(350000.0, opex_annuo_eur=7000.0, capacita_kwh=1000.0,
          cicli_annui=365.0, dod=0.9, efficienza_pct=100.0,
          degrado_annuo_pct=0.0, tasso_sconto_pct=5.0, vita_anni=10,
          costo_ricarica_eur_mwh=80.0)
pv_e_att = sum(e_dis / 1.05 ** t for t in range(1, 11))
check("pv energia scontata", abs(r6["pv_energia_mwh"] - pv_e_att) < 1e-9,
      r6["pv_energia_mwh"])
pv_c_att = 350000.0 + sum((7000.0 + e_dis * 80.0) / 1.05 ** t
                          for t in range(1, 11))
check("pv costi scontati", abs(r6["pv_costi_eur"] - pv_c_att) < 1e-6,
      r6["pv_costi_eur"])
check("lcos = pv_c/pv_e",
      abs(r6["lcos_eur_mwh"] - pv_c_att / pv_e_att) < 1e-9)

# --- 7. quote di costo sommano a ~1 ---
qtot = r6["quota_capex"] + r6["quota_opex"] + r6["quota_ricarica"]
check("quote sommano 1", abs(qtot - 1.0) < 1e-12, qtot)

# --- 8. sensibilita' monotoniche ---
sc = r["sens_cicli"]
ks = sorted(sc.keys())
check("sens cicli monotona decrescente",
      all(sc[ks[i]] >= sc[ks[i + 1]] for i in range(len(ks) - 1)),
      list(sc.values()))
sv = r["sens_vita"]
kv = sorted(sv.keys())
check("sens vita monotona decrescente",
      all(sv[kv[i]] >= sv[kv[i + 1]] for i in range(len(kv) - 1)),
      list(sv.values()))
sr = r["sens_ricarica"]
kr = sorted(sr.keys())
check("sens ricarica monotona crescente",
      all(sr[kr[i]] <= sr[kr[i + 1]] for i in range(len(kr) - 1)),
      list(sr.values()))
check("sens ricarica 0 < base", sr[0.0] < r["lcos_eur_mwh"])

# --- 9. errori di validazione (NaN-safe) ---
_base9 = dict(capex_eur=1000.0, opex_annuo_eur=100.0, capacita_kwh=500.0,
              cicli_annui=200.0, dod=0.9, efficienza_pct=90.0,
              degrado_annuo_pct=1.0, tasso_sconto_pct=5.0, vita_anni=10,
              costo_ricarica_eur_mwh=80.0, valore_residuo_eur=0.0)
for nome, kwargs in [
    ("capex negativo", {"capex_eur": -1.0}),
    ("capacita zero", {"capacita_kwh": 0.0}),
    ("cicli zero", {"cicli_annui": 0.0}),
    ("dod > 1", {"dod": 1.5}),
    ("eff zero", {"efficienza_pct": 0.0}),
    ("degrado 100", {"degrado_annuo_pct": 100.0}),
    ("vita 0", {"vita_anni": 0.0}),
    ("ricarica negativa", {"costo_ricarica_eur_mwh": -5.0}),
    ("non numerico", {"capex_eur": "x"}),
    ("nan", {"capex_eur": float("nan")}),
    ("inf", {"opex_annuo_eur": float("inf")}),
]:
    kw = dict(_base9)
    kw.update(kwargs)
    rr = lcos(**kw)
    check(f"errore: {nome}", (not rr["valido"]) and rr["errore"] is not None,
          rr["errore"])
    check(f"df vuoto: {nome}", rr["df"].empty)

# --- 10. vita non intera arrotondata ---
r10 = lcos(100000.0, capacita_kwh=500.0, cicli_annui=200.0, vita_anni=7.6)
check("vita 7.6 -> 8 righe", len(r10["df"]) == 8, len(r10["df"]))

# --- 11. opex zero e ricarica zero ---
r11 = lcos(100000.0, opex_annuo_eur=0.0, capacita_kwh=500.0,
           cicli_annui=200.0, efficienza_pct=100.0, degrado_annuo_pct=0.0,
           tasso_sconto_pct=0.0, vita_anni=5, costo_ricarica_eur_mwh=0.0)
att11 = 100000.0 / (5 * 200.0 * 0.5 * 0.9)
check("lcos solo capex", abs(r11["lcos_eur_mwh"] - att11) < 1e-9,
      (r11["lcos_eur_mwh"], att11))
check("quota capex = 1", abs(r11["quota_capex"] - 1.0) < 1e-12,
      r11["quota_capex"])

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
