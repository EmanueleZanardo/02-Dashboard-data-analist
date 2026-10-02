"""Standalone test for calcola_costo_per_sito - tab163 (no streamlit)."""
import ast
import re
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_costo_per_sito":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola = ns["calcola_costo_per_sito"]

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


def load_series(vals, start="2025-01-06", tz=None):
    idx = pd.date_range(start, periods=len(vals), freq="h", tz=tz)
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


def close(a, b, tol=1e-2):
    return abs(a - b) < tol


# --- 1. numeri a mano: 48h piatte a 100 EUR/MWh, A piatto 10 MW, B piatto 5 MW ---
p48 = hours([100.0] * 48)
r = calcola(p48, {"A": load_series([10.0] * 48), "B": load_series([5.0] * 48)})
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_ore == 48", r["n_ore"] == 48)
check("mano: energia totale 720", close(r["energia_totale_mwh"], 720.0))
check("mano: costo totale 72000", close(r["costo_totale_eur"], 72000.0))
check("mano: prezzo medio portafoglio 100", close(r["prezzo_medio_portafoglio_eur_mwh"], 100.0))
tab = r["tabella"]
check("mano: tabella 2 righe", len(tab) == 2)
check("mano: energia A 480", close(float(tab.loc[tab["Sito"] == "A", "Energia (MWh)"].iloc[0]), 480.0))
check("mano: costo B 24000", close(float(tab.loc[tab["Sito"] == "B", "Costo (EUR)"].iloc[0]), 24000.0))
check("mano: quota costo A 66.67", close(float(tab.loc[tab["Sito"] == "A", "Quota costo (%)"].iloc[0]), 66.6667))
check("mano: quota energia B 33.33", close(float(tab.loc[tab["Sito"] == "B", "Quota energia (%)"].iloc[0]), 33.3333))
check("mano: scostamenti nulli", close(float(tab["Scost. vs medio (EUR/MWh)"].abs().max()), 0.0))
check("mano: giudizio OMOGENEE", r["giudizio"] == "OMOGENEE")
check("mano: spread 0", close(r["spread_eur_mwh"], 0.0))

# --- 2. numeri a mano: giorno 120 / notte 60, A piatto 10 MW, B diurno 10 MW ---
vals_gn = []
for _ in range(2):
    vals_gn += [60.0] * 7 + [120.0] * 14 + [60.0] * 3
pgn = hours(vals_gn)
w_mean = 23.75 / 24.0
w_diurno = [0.625 / w_mean] * 7 + [1.25 / w_mean] * 14 + [0.625 / w_mean] * 3
b48 = (w_diurno * 2)
r2 = calcola(pgn, {"A": load_series([10.0] * 48), "B": load_series([10.0 * x for x in b48])})
check("profili: valido", r2["valido"])
check("profili: pm A 95.0", close(float(r2["tabella"].loc[r2["tabella"]["Sito"] == "A", "Prezzo medio (EUR/MWh)"].iloc[0]), 95.0))
check("profili: pm B 104.21", close(float(r2["tabella"].loc[r2["tabella"]["Sito"] == "B", "Prezzo medio (EUR/MWh)"].iloc[0]), 104.2105))
check("profili: costo B 50021.05", close(float(r2["tabella"].loc[r2["tabella"]["Sito"] == "B", "Costo (EUR)"].iloc[0]), 50021.05))
check("profili: piu caro B", r2["sito_piu_caro"] == "B")
check("profili: piu economico A", r2["sito_piu_economico"] == "A")
check("profili: spread 9.21", close(r2["spread_eur_mwh"], 9.2105))
check("profili: spread_pct ~9.25", close(r2["spread_pct"], 9.2469, tol=0.05))
check("profili: giudizio MODERATE", r2["giudizio"] == "MODERATE")
check("profili: scost A negativo", float(r2["tabella"].loc[r2["tabella"]["Sito"] == "A", "Scost. vs medio (EUR/MWh)"].iloc[0]) < 0)

# --- 3. giudizio RILEVANTI con gap estremo giorno/notte ---
vals_x = []
for _ in range(2):
    vals_x += [10.0] * 7 + [500.0] * 14 + [10.0] * 3
r3 = calcola(hours(vals_x), {"A": load_series([10.0] * 48), "B": load_series([10.0 * x for x in b48])})
check("estremo: giudizio RILEVANTI", r3["giudizio"] == "RILEVANTI")
check("estremo: piu caro B (diurno)", r3["sito_piu_caro"] == "B")

# --- 4. input DataFrame ---
df_c = pd.DataFrame({"X": load_series([4.0] * 48), "Y": load_series([6.0] * 48)})
r4 = calcola(p48, df_c)
check("DataFrame: valido, costo 48000", r4["valido"] and close(r4["costo_totale_eur"], 48000.0))
check("DataFrame: nomi da colonne", set(r4["tabella"]["Sito"]) == {"X", "Y"})

# --- 5. casi di errore ---
err_cases = [
    ("prezzi vuoti", dict(prezzi=hours([]), carichi={"A": load_series([1.0] * 48)})),
    ("indice prezzi non datetime", dict(prezzi=pd.Series([100.0] * 48), carichi={"A": load_series([1.0] * 48)})),
    ("prezzi <24h", dict(prezzi=hours([100.0] * 10), carichi={"A": load_series([1.0] * 48)})),
    ("carichi None", dict(prezzi=p48, carichi=None)),
    ("dict vuoto", dict(prezzi=p48, carichi={})),
    ("nome vuoto", dict(prezzi=p48, carichi={"": load_series([1.0] * 48)})),
    ("serie carico vuota", dict(prezzi=p48, carichi={"A": load_series([])})),
    ("indice carico non datetime", dict(prezzi=p48, carichi={"A": pd.Series([1.0] * 48)})),
    ("carichi negativi", dict(prezzi=p48, carichi={"A": load_series([-1.0] * 48)})),
    ("energia nulla", dict(prezzi=p48, carichi={"A": load_series([0.0] * 48)})),
    ("ore comuni <24", dict(prezzi=hours([100.0] * 48), carichi={"A": load_series([1.0] * 48, start="2026-03-01")})),
    ("tipo carichi errato", dict(prezzi=p48, carichi=[1, 2, 3])),
    ("tutti NaN prezzi", dict(prezzi=hours([np.nan] * 48), carichi={"A": load_series([1.0] * 48)})),
]
for nome, kw in err_cases:
    rr = calcola(**kw)
    check("errore: " + nome, (not rr["valido"]) and bool(rr["errore"]))
# nomi duplicati via DataFrame
df_dup = pd.DataFrame(np.ones((48, 2)), columns=["A", "A"],
                      index=pd.date_range("2025-01-06", periods=48, freq="h"))
rr = calcola(p48, df_dup)
check("errore: nomi duplicati", (not rr["valido"]) and bool(rr["errore"]))

# --- 6. robustezza dati ---
r6 = calcola(hours([100.0] * 48, tz="Europe/Zurich"),
             {"A": load_series([10.0] * 48, tz="Europe/Zurich"), "B": load_series([5.0] * 48)})
check("tz-aware: valido, costo 72000", r6["valido"] and close(r6["costo_totale_eur"], 72000.0))
s_dup = pd.concat([hours([100.0] * 48), hours([200.0] * 48)])
r7 = calcola(s_dup, {"A": load_series([10.0] * 48), "B": load_series([5.0] * 48)})
check("duplicati prezzi: keep-first, pmedio 100",
      r7["valido"] and close(r7["prezzo_medio_portafoglio_eur_mwh"], 100.0))
vals_nan = [100.0] * 47 + [np.nan]
r8 = calcola(hours(vals_nan), {"A": load_series([10.0] * 48), "B": load_series([5.0] * 48)})
check("NaN prezzi: valido su 47 ore", r8["valido"] and r8["n_ore"] == 47)
# NaN nel carico = sito fermo -> 0
c_nan = [10.0] * 24 + [np.nan] * 24
r9 = calcola(p48, {"A": load_series(c_nan), "B": load_series([5.0] * 48)})
check("NaN carico: energia A 240 (meta' ore a 0)",
      r9["valido"] and close(float(r9["tabella"].loc[r9["tabella"]["Sito"] == "A", "Energia (MWh)"].iloc[0]), 240.0))
# ore attive
check("ore attive A 24", int(r9["tabella"].loc[r9["tabella"]["Sito"] == "A", "Ore attive"].iloc[0]) == 24)

# --- 7. determinismo ---
ra = calcola(pgn, {"A": load_series([10.0] * 48), "B": load_series([10.0 * x for x in b48])})
rb = calcola(pgn, {"A": load_series([10.0] * 48), "B": load_series([10.0 * x for x in b48])})
check("determinismo: stesso costo totale",
      close(ra["costo_totale_eur"], rb["costo_totale_eur"], tol=1e-9))

# --- 8. registry tab163 ---
m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
dvars = re.findall(r"tab\d+", m.group(0))
check("registry: 163 variabili dichiarate, ultima tab163",
      len(dvars) == 163 and dvars[-1] == "tab163")
check("registry: titolo presente", '"🏭 Costo per sito"' in src)
withs = re.findall(r"^    with (tab\d+):", src, re.M)
check("registry: 163 with-blocks in sequenza 1..163",
      withs == ["tab%d" % i for i in range(1, 164)])
keys = re.findall(r'key="(cs163_[^"]+)"', src)
fkeys = re.findall(r'key=f"(cs163_[^"]+)"', src)
check("registry: chiavi widget cs163 uniche",
      len(keys) == len(set(keys)) and len(keys) >= 2
      and len(fkeys) == len(set(fkeys)) and len(fkeys) == 3)
check("registry: helper a livello modulo",
      re.search(r"^def calcola_costo_per_sito\(", src, re.M) is not None)

print("checks: %d, fails: %d" % (_nchecks[0], len(fails)))
if fails:
    raise SystemExit("FAILURES: " + ", ".join(fails))
