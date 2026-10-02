"""Standalone test for calcola_prezzo_fisso_equo - tab162 (no streamlit)."""
import ast
import re
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_prezzo_fisso_equo":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola = ns["calcola_prezzo_fisso_equo"]

fails = []
_nchecks = [0]


def check(name, cond):
    _nchecks[0] += 1
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def hours(vals, start="2025-01-06", tz=None):
    idx = pd.date_range(start, periods=len(vals), freq="h", tz=tz)
    return pd.Series(np.asarray(vals, dtype=float), index=idx, name="p")


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


# --- 1. numeri a mano: 48h piatte a 100 EUR/MWh, base 10 piatto, premio 5, marg 3, adder 1 ---
r = calcola(hours([100.0] * 48), carico_base_mw=10.0, forma_carico="piatto",
            premio_rischio_pct=5.0, margine_eur_mwh=3.0,
            adder_volume_eur_mwh=1.0)
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_ore == 48", r["n_ore"] == 48)
check("mano: energia totale 480.0", close(r["energia_totale_mwh"], 480.0))
check("mano: costo spot 48000", close(r["costo_spot_eur"], 48000.0))
check("mano: PWP 100.0", close(r["pwp_eur_mwh"], 100.0))
check("mano: premio 5.0", close(r["premio_eur_mwh"], 5.0))
check("mano: prezzo equo 109.0", close(r["prezzo_fisso_equo_eur_mwh"], 109.0))
check("mano: costo equo 52320", close(r["costo_equo_eur"], 52320.0))
check("mano: addon 9%", close(r["addon_pct"], 9.0))
check("mano: giudizio CONTENUTO", r["giudizio"] == "CONTENUTO")
sc = r["scomposizione"]
check("mano: scomposizione 5 righe", len(sc) == 5)
check("mano: scomposizione valori",
      close(sc["EUR/MWh"].iloc[0], 100.0) and close(sc["EUR/MWh"].iloc[1], 5.0)
      and close(sc["EUR/MWh"].iloc[2], 3.0) and close(sc["EUR/MWh"].iloc[3], 1.0)
      and close(sc["EUR/MWh"].iloc[4], 109.0))
sens = r["sensibilita"]
check("mano: sensibilita 3x4", sens.shape == (3, 4))
check("mano: cella (marg 3, premio 5) = 109.0",
      close(float(sens.loc[sens["Margine (EUR/MWh)"] == 3.0, "Premio 5.0 %"].iloc[0]), 109.0))
check("mano: cella (marg 1, premio 2.5) = 104.5",
      close(float(sens.loc[sens["Margine (EUR/MWh)"] == 1.0, "Premio 2.5 %"].iloc[0]), 104.5))
check("mano: cella (marg 5, premio 7.5) = 113.5",
      close(float(sens.loc[sens["Margine (EUR/MWh)"] == 5.0, "Premio 7.5 %"].iloc[0]), 113.5))

# --- 2. forma diurna: 24h, giorno (7-20) a 120, notte a 60, base 10, premio 10, marg 2, adder 0.5 ---
vals = [60.0] * 7 + [120.0] * 14 + [60.0] * 3
r2 = calcola(hours(vals), carico_base_mw=10.0, forma_carico="diurno",
             premio_rischio_pct=10.0, margine_eur_mwh=2.0,
             adder_volume_eur_mwh=0.5)
check("diurno: valido", r2["valido"])
check("diurno: energia totale 240.0", close(r2["energia_totale_mwh"], 240.0))
check("diurno: costo spot 25010.53", close(r2["costo_spot_eur"], 25010.526316, tol=1e-3))
check("diurno: PWP 104.2105", close(r2["pwp_eur_mwh"], 25010.526316 / 240.0, tol=1e-4))
check("diurno: prezzo equo 117.1316",
      close(r2["prezzo_fisso_equo_eur_mwh"], 25010.526316 / 240.0 * 1.10 + 2.5, tol=1e-4))
check("diurno: giudizio MEDIO", r2["giudizio"] == "MEDIO")

# --- 3. giudizio ALTO: premio 30, marg 5, adder 5 su piatto 100 ---
r3 = calcola(hours([100.0] * 48), carico_base_mw=10.0, forma_carico="piatto",
             premio_rischio_pct=30.0, margine_eur_mwh=5.0,
             adder_volume_eur_mwh=5.0)
check("alto: prezzo equo 140.0", close(r3["prezzo_fisso_equo_eur_mwh"], 140.0))
check("alto: giudizio ALTO", r3["giudizio"] == "ALTO")

# --- 4. zeri ammessi: premio 0, marg 0, adder 0 -> equo == PWP ---
r4 = calcola(hours([100.0] * 48), carico_base_mw=10.0, forma_carico="piatto",
             premio_rischio_pct=0.0, margine_eur_mwh=0.0,
             adder_volume_eur_mwh=0.0)
check("zeri: equo == PWP", close(r4["prezzo_fisso_equo_eur_mwh"], r4["pwp_eur_mwh"]))

# --- 5. casi di errore ---
err_cases = [
    ("serie vuota", dict(prezzi=hours([]))),
    ("indice non datetime", dict(prezzi=pd.Series([1.0] * 48))),
    ("serie corta", dict(prezzi=hours([100.0] * 23))),
    ("base zero", dict(prezzi=hours([100.0] * 48), carico_base_mw=0.0)),
    ("base negativa", dict(prezzi=hours([100.0] * 48), carico_base_mw=-5.0)),
    ("forma errata", dict(prezzi=hours([100.0] * 48), forma_carico="notturno")),
    ("premio negativo", dict(prezzi=hours([100.0] * 48), premio_rischio_pct=-1.0)),
    ("premio > 100", dict(prezzi=hours([100.0] * 48), premio_rischio_pct=101.0)),
    ("marg negativo", dict(prezzi=hours([100.0] * 48), margine_eur_mwh=-1.0)),
    ("adder negativo", dict(prezzi=hours([100.0] * 48), adder_volume_eur_mwh=-1.0)),
    ("base non numerica", dict(prezzi=hours([100.0] * 48), carico_base_mw="x")),
    ("tutti NaN", dict(prezzi=hours([np.nan] * 48))),
]
for nome, kw in err_cases:
    rr = calcola(**kw)
    check("errore: " + nome, (not rr["valido"]) and bool(rr["errore"]))

# --- 6. robustezza dati ---
r6 = calcola(hours([100.0] * 48, tz="Europe/Zurich"), carico_base_mw=10.0,
             forma_carico="piatto")
check("tz-aware: valido, PWP 100", r6["valido"] and close(r6["pwp_eur_mwh"], 100.0))
s_dup = pd.concat([hours([100.0] * 48), hours([200.0] * 48)])
r7 = calcola(s_dup, carico_base_mw=10.0, forma_carico="piatto")
check("duplicati: keep-first, PWP 100", r7["valido"] and close(r7["pwp_eur_mwh"], 100.0))
vals_nan = [100.0] * 47 + [np.nan]
r8 = calcola(hours(vals_nan), carico_base_mw=10.0, forma_carico="piatto")
check("NaN: valido su 47 ore", r8["valido"] and r8["n_ore"] == 47)

# --- 7. determinismo ---
ra = calcola(hours(vals), carico_base_mw=10.0, forma_carico="diurno",
             premio_rischio_pct=10.0, margine_eur_mwh=2.0,
             adder_volume_eur_mwh=0.5)
rb = calcola(hours(vals), carico_base_mw=10.0, forma_carico="diurno",
             premio_rischio_pct=10.0, margine_eur_mwh=2.0,
             adder_volume_eur_mwh=0.5)
check("determinismo: stesso prezzo equo",
      close(ra["prezzo_fisso_equo_eur_mwh"], rb["prezzo_fisso_equo_eur_mwh"]))

# --- 8. registry tab162 (robusto a nuove tab: appartenenza, non conteggio esatto) ---
m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
dvars = re.findall(r"tab\d+", m.group(0))
check("registry: tab162 dichiarata tra le variabili",
      "tab162" in dvars and dvars == sorted(dvars, key=lambda t: int(t[3:])))
check("registry: titolo presente", '"💰 Prezzo fisso equo"' in src)
withs = re.findall(r"^    with (tab\d+):", src, re.M)
check("registry: tab162 presente, sequenza senza buchi da 1",
      "tab162" in withs and withs == ["tab%d" % i for i in range(1, len(withs) + 1)])
keys = re.findall(r'key="(pf162_[^"]+)"', src)
check("registry: chiavi widget pf162 uniche",
      len(keys) == len(set(keys)) and len(keys) >= 6)

print("checks: %d, fails: %d" % (_nchecks[0], len(fails)))
if fails:
    raise SystemExit("FAILURES: " + ", ".join(fails))
