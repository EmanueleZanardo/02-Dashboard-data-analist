"""Test standalone di calcola_stoccaggio_estrinseco + generate_mock_gas + calcola_stoccaggio_gas (tab114).

Estrae le funzioni pure da app.py via AST (senza avviare Streamlit) e le
esegue in un namespace con pandas/numpy/scipy. Stile dei QA: conta i check,
0 fail attesi.
Uso: python3 tests/test_stoccaggio_estrinseco_2026-09-30_2339.py
"""
import ast
import os
import sys
import time

import numpy as np
import pandas as pd

APP = os.path.join(os.path.dirname(__file__), "..", "app.py")
WANT = {"generate_mock_gas", "calcola_stoccaggio_gas", "calcola_stoccaggio_estrinseco"}

tree = ast.parse(open(APP, encoding="utf-8").read())


class _DummySt:
    """Solo per i decoratori @st.cache_data: li rende no-op nei test."""

    @staticmethod
    def cache_data(*a, **k):
        def deco(fn):
            return fn

        if a and callable(a[0]) and len(a) == 1 and not k:
            return a[0]
        return deco


ns = {"pd": pd, "np": np, "st": _DummySt()}
found = set()
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.Assign)) is False:
        continue
    names = [node.name] if isinstance(node, ast.FunctionDef) else \
        [t.id for t in node.targets if isinstance(t, ast.Name)]
    for n in names:
        if n in WANT:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, APP, "exec"), ns)  # noqa: S102 - repo proprio
            found.add(n)

assert found == WANT, f"funzioni mancanti in app.py: {WANT - found}"

checks = failed = 0


def check(name, cond):
    global checks, failed
    checks += 1
    if not cond:
        failed += 1
        print(f"FAIL: {name}")


gas = ns["generate_mock_gas"]("2025-01-01", "2025-12-31").dropna()
t0 = time.time()
r = ns["calcola_stoccaggio_estrinseco"](gas, 500.0, 8.0, 12.0, n_scenari=50,
                                       vol_annua_pct=35.0, mean_reversion_giorni=30.0)
dt = time.time() - t0

# 1. valido su input sani
check("valido su mock gas 1 anno", r["valido"] is True)
# 2. convessita' del valore LP nei prezzi: E[V] >= V(E[..]) -> estrinseco >= intrinseco (tolleranza rumore MC)
intr = r["valore_intrinseco_eur"]
estr = r["valore_estrinseco_eur"]
check("estrinseco >= intrinseco (tolleranza 2%)", estr >= intr * 0.98 - 1.0)
# 3. ordinamento percentili
check("p10 <= media <= p90", r["p10_eur"] <= estr <= r["p90_eur"])
# 4. determinismo: stesso seed -> stesso risultato
r2 = ns["calcola_stoccaggio_estrinseco"](gas, 500.0, 8.0, 12.0, n_scenari=50,
                                        vol_annua_pct=35.0, mean_reversion_giorni=30.0)
check("deterministico a parita' di seed", r2["valore_estrinseco_eur"] == estr)
# 5. vol=0 -> percorsi = curva base -> premio ~ 0
r0 = ns["calcola_stoccaggio_estrinseco"](gas, 500.0, 8.0, 12.0, n_scenari=10,
                                        vol_annua_pct=0.0, mean_reversion_giorni=30.0)
check("vol=0 -> premio ~ 0", r0["valido"] and abs(r0["premio_estrinseco_eur"]) < 1e-3)
# 6. serie troppo corta -> non valido
rc = ns["calcola_stoccaggio_estrinseco"](gas.iloc[:1], 500.0, 8.0, 12.0, n_scenari=5)
check("1 giorno -> valido=False", rc["valido"] is False)
# 7. numero scenari rispettato
check("len(valori) == n_scenari", len(r["valori_eur"]) == 50 and r["n_scenari"] == 50)
# 8. plumbing n_scenari piccolo
r5 = ns["calcola_stoccaggio_estrinseco"](gas, 500.0, 8.0, 12.0, n_scenari=5,
                                        vol_annua_pct=35.0, mean_reversion_giorni=30.0)
check("n_scenari=5 valido e 5 valori", r5["valido"] and len(r5["valori_eur"]) == 5)
# 9. giacenze iniziale/finale diverse accettate
rd = ns["calcola_stoccaggio_estrinseco"](gas, 500.0, 8.0, 12.0, inv_iniziale_pct=20.0,
                                        inv_finale_pct=80.0, n_scenari=5)
check("inv 20%->80% valido", rd["valido"] is True)

print(f"check={checks} failed={failed} | 50 scenari in {dt:.1f}s | "
      f"intrinseco={intr:,.0f} estrinseco={estr:,.0f} premio={estr-intr:,.0f} "
      f"({100*(estr-intr)/intr:.1f}%)")
sys.exit(1 if failed else 0)
