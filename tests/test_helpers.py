"""Test delle funzioni pure di calcolo di app.py (senza avviare Streamlit).

Estrae le funzioni da app.py via AST e le esegue in un namespace con
pandas/numpy. Stile dei QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_helpers.py
"""
import ast
import os
import sys

import numpy as np
import pandas as pd

APP = os.path.join(os.path.dirname(__file__), "..", "app.py")
WANT = {"PROFILI_CARICO_TIPO", "profilo_carico_tipo", "shock_scenario",
        "banner_demo", "generate_mock_hourly", "ottimizza_ricarica_ev",
        "generate_mock_zona", "calcola_spread_xb", "ZONE_XB",
        "generate_mock_gas", "calcola_stoccaggio_gas"}

tree = ast.parse(open(APP, encoding="utf-8").read())


class _DummySt:
    """Solo per i decoratori @st.cache_data: li rende no-op nei test."""

    @staticmethod
    def cache_data(*a, **k):
        def deco(fn):
            return fn

        # supporta sia @st.cache_data sia @st.cache_data(...)
        if a and callable(a[0]) and len(a) == 1 and not k:
            return a[0]
        return deco


ns = {"pd": pd, "np": np, "st": _DummySt()}
found = set()
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.Assign)) is False:
        continue
    names = []
    if isinstance(node, ast.FunctionDef):
        names = [node.name]
    else:
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
    for n in names:
        if n in WANT:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, APP, "exec"), ns)  # noqa: S102 - repo proprio
            found.add(n)

checks = failed = 0


def check(name, cond):
    global checks, failed
    checks += 1
    if not cond:
        failed += 1
        print(f"FAIL: {name}")


check("funzioni trovate", found == WANT)

profilo_carico_tipo = ns["profilo_carico_tipo"]
shock_scenario = ns["shock_scenario"]

# --- profilo_carico_tipo ---
p = profilo_carico_tipo("Industriale 3 turni", 10.0)
check("profilo 24 valori", len(p) == 24)
check("industriale piatto", abs(p.sum() - 24 * 0.85 * 10.0) < 1e-6)
check("profilo non negativi", bool((p >= 0).all()))
u = profilo_carico_tipo("Uffici (lun-ven 8-19)", 2.0)
check("uffici picco=2MW", abs(u.max() - 2.0) < 1e-9)
check("uffici notte bassa", u.iloc[3] < u.iloc[10])
g = profilo_carico_tipo("GDO / Supermercato", 1.0)
check("gdo 24 valori", len(g) == 24 and abs(g.max() - 1.0) < 1e-9)
z = profilo_carico_tipo("TipoInesistente", 5.0)
check("tipo sconosciuto -> default industriale", abs(z.sum() - 24 * 0.85 * 5.0) < 1e-6)
z2 = profilo_carico_tipo("Uffici (lun-ven 8-19)", -3)
check("picco negativo -> zeri", bool((z2 == 0).all()))
z3 = profilo_carico_tipo("Uffici (lun-ven 8-19)", "nan")
check("picco non numerico -> zeri", bool((z3 == 0).all()))

# --- shock_scenario ---
idx = pd.date_range("2026-01-01", periods=48, freq="h")
serie = pd.Series([100.0] * 48, index=idx)
r = shock_scenario(serie, 25, 1000.0)
check("shock +25% prezzo medio", abs(r["prezzo_medio_shock"] - 125.0) < 1e-9)
check("shock delta annuo", abs(r["delta"] - 25.0 * 1000.0) < 1e-6)
check("shock costo base", abs(r["costo_base"] - 100.0 * 1000.0) < 1e-6)
r2 = shock_scenario(serie, -50, 1000.0)
check("shock -50%", abs(r2["prezzo_medio_shock"] - 50.0) < 1e-9 and r2["delta"] < 0)
r3 = shock_scenario(pd.Series([], dtype=float), 25, 1000.0)
check("serie vuota -> zeri", r3["delta"] == 0.0 and r3["costo_base"] == 0.0)
r4 = shock_scenario(serie, "xx", 1000.0)
check("shock non numerico -> zeri", r4["delta"] == 0.0)
r5 = shock_scenario(pd.Series([np.nan, np.nan]), 25, 1000.0)
check("serie solo-NaN -> zeri", r5["costo_base"] == 0.0)

# --- generate_mock_hourly deterministico ---
mock = ns["generate_mock_hourly"]
m1 = mock(__import__("datetime").date(2026, 1, 1), __import__("datetime").date(2026, 1, 7))
m2 = mock(__import__("datetime").date(2026, 1, 1), __import__("datetime").date(2026, 1, 7))
check("mock deterministico (seed fisso)", m1.equals(m2))
check("mock 7gg = 168 ore", len(m1) == 168)

# --- ottimizza_ricarica_ev ---
ev = ns["ottimizza_ricarica_ev"]
prezzi_ev = [60.0] * 24
for h in range(17, 21):
    prezzi_ev[h] = 180.0
for h in range(7, 17):
    prezzi_ev[h] = 110.0
r = ev(prezzi_ev, 40.0, 11.0, 17, 7, 92.0, 60.0, 20.0)
check("ev valido", r["valido"])
check("ev risparmio >= 0", r["risparmio_eur"] >= -1e-9)
check("ev energia conservata", abs(sum(r["schedario"]) - 40.0 / 0.92) < 1e-6)
check("ev potenza rispettata", all(s <= 11.0 + 1e-9 for s in r["schedario"]))
fin = set()
hh = 17
while True:
    fin.add(hh)
    hh = (hh + 1) % 24
    if hh == 7:
        break
check("ev solo ore in finestra", all(r["schedario"][x] == 0.0 for x in range(24) if x not in fin))
check("ev smart batte immediata", r["costo_immediata"] > r["costo_ottimale"])
r2 = ev(prezzi_ev, 500.0, 11.0, 17, 19)
check("ev finestra corta -> non valido", not r2["valido"])
r3 = ev(prezzi_ev, 50.0, 11.0, 17, 7, 92.0, 60.0, 95.0)
check("ev batteria piena -> non valido", not r3["valido"])
check("ev 23 prezzi -> non valido", not ev([1.0] * 23, 10.0, 5.0)["valido"])
check("ev energia negativa -> non valido", not ev(prezzi_ev, -5.0, 5.0)["valido"])
check("ev potenza zero -> non valido", not ev(prezzi_ev, 10.0, 0.0)["valido"])
r5 = ev([100.0] * 24, 22.0, 11.0, 0, 0)
check("ev prezzi piatti -> risparmio zero", r5["valido"] and abs(r5["risparmio_eur"]) < 1e-9)

# --- calcola_spread_xb / generate_mock_zona ---
xb = ns["calcola_spread_xb"]
idx = pd.date_range("2026-01-01", periods=4, freq="h", tz="Europe/Zurich")
r = xb(pd.Series([50.0, 60.0, 40.0, 70.0], index=idx),
       pd.Series([60.0, 55.0, 40.0, 90.0], index=idx), 1.0)
check("xb valido", r["valido"])
check("xb valore arbitraggio = somma spread positivi",
      abs(r["valore_totale_eur"] - 30.0) < 1e-9)
check("xb spread medio", abs(r["spread_medio"] - 6.25) < 1e-9)
check("xb serie vuota -> non valido", not xb(pd.Series(dtype=float), pd.Series(dtype=float))["valido"])
check("xb capacita' zero -> non valido", not xb(
    pd.Series([1.0, 2.0], index=idx[:2]), pd.Series([2.0, 3.0], index=idx[:2]), 0.0)["valido"])
mz = ns["generate_mock_zona"]
m1z = mz(__import__("datetime").date(2026, 3, 1), __import__("datetime").date(2026, 3, 7),
         "🇮🇹 Italia Nord (IT-NORD)")
m2z = mz(__import__("datetime").date(2026, 3, 1), __import__("datetime").date(2026, 3, 7),
         "🇮🇹 Italia Nord (IT-NORD)")
check("xb mock deterministico", m1z.equals(m2z) and len(m1z) == 168)
check("xb zone registry 3 zone", len(ns["ZONE_XB"]) == 3)

# --- calcola_stoccaggio_gas / generate_mock_gas ---
stocc = ns["calcola_stoccaggio_gas"]
mgas = ns["generate_mock_gas"]


def _sg(prezzi):
    idx = pd.date_range("2026-01-01", periods=len(prezzi), freq="D", tz="Europe/Zurich")
    return pd.Series(prezzi, index=idx, dtype=float)


r = stocc(_sg([10.0, 50.0, 10.0, 50.0]), 10.0, 10.0, 10.0,
          costo_inj_eur_mwh=0.0, costo_wd_eur_mwh=0.0,
          inv_iniziale_pct=0.0, inv_finale_pct=0.0)
check("sg valido", r["valido"])
check("sg valore 800", abs(r["valore_intrinseco_eur"] - 800.0) < 1e-6)
check("sg 2 cicli", abs(r["cicli_equivalenti"] - 2.0) < 1e-9)
r = stocc(_sg([50.0, 10.0]), 10.0, 10.0, 10.0,
          costo_inj_eur_mwh=0.0, costo_wd_eur_mwh=0.0,
          inv_iniziale_pct=0.0, inv_finale_pct=0.0)
check("sg discesa senza stock -> 0", r["valido"] and abs(r["valore_intrinseco_eur"]) < 1e-6)
r = stocc(_sg([50.0, 10.0]), 10.0, 10.0, 10.0,
          costo_inj_eur_mwh=0.0, costo_wd_eur_mwh=0.0,
          inv_iniziale_pct=100.0, inv_finale_pct=0.0)
check("sg stock pieno -> 500", r["valido"] and abs(r["valore_intrinseco_eur"] - 500.0) < 1e-6)
check("sg cap zero -> invalido", not stocc(_sg([10.0, 50.0]), 0.0, 5.0, 5.0)["valido"])
check("sg 1 giorno -> invalido", not stocc(_sg([10.0]), 10.0, 5.0, 5.0)["valido"])
gm1 = mgas(__import__("datetime").date(2026, 1, 1), __import__("datetime").date(2026, 12, 31))
gm2 = mgas(__import__("datetime").date(2026, 1, 1), __import__("datetime").date(2026, 12, 31))
check("sg mock deterministico", gm1.equals(gm2) and len(gm1) == 374)
check("sg mock inverno > estate",
      gm1[gm1.index.month == 1].mean() > gm1[gm1.index.month == 7].mean() + 5.0)

print(f"{checks} check / {failed} fail")
sys.exit(1 if failed else 0)
