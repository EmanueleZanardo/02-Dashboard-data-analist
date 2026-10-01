"""Test standalone tab137 'Radar prezzo obiettivo'.

Estrae calcola_radar_target da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_radar_target_2026-10-01_1932.py
"""
import ast
import os
import re
import sys

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_radar_target":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
rt = ns["calcola_radar_target"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_rumore(giorni=120, base=100.0, seed=7):
    idx = pd.date_range("2025-06-04", periods=giorni * 24, freq="h")
    rng = np.random.default_rng(seed)
    ore = np.arange(giorni * 24)
    vals = base + 5.0 * np.sin(2 * np.pi * (ore % 24) / 24.0) + rng.normal(0, 2.0, len(ore))
    return pd.Series(vals, index=idx)


def serie_giorni_piatta(valori_giorno, inizio="2026-01-01"):
    # valori_giorno: lista di prezzi (uno al giorno), serie oraria costante nel giorno
    idx = pd.date_range(inizio, periods=len(valori_giorno) * 24, freq="h")
    vals = np.repeat(np.asarray(valori_giorno, dtype=float), 24)
    return pd.Series(vals, index=idx)


# --- validazione parametri ---
s = serie_rumore()
check("target non numerico -> ok False", rt(s, target="abc")["ok"] is False)
check("target inf -> ok False", rt(s, target=float("inf"))["ok"] is False)
r = rt(s, target=90, lato="foo")
check("lato invalido -> ok False", r["ok"] is False, r["motivo"])
r = rt(s, target=90, orizzonte_giorni=3)
check("orizzonte 3 -> ok False", r["ok"] is False)
r = rt(s, target=90, orizzonte_giorni=400)
check("orizzonte 400 -> ok False", r["ok"] is False)
r = rt(s, target=90, lookback_giorni=10)
check("lookback 10 -> ok False", r["ok"] is False)
r = rt(s, target=90, n_scenari=50)
check("scenari 50 -> ok False", r["ok"] is False)
r = rt(s, target=90, seed="x")
check("seed non int -> ok False", r["ok"] is False)
r = rt(pd.Series([1.0, 2.0, 3.0]), target=90)
check("indice non datetime -> ok False", r["ok"] is False)
r = rt(serie_rumore(giorni=10), target=90)
check("<30 giorni -> ok False", r["ok"] is False, r["motivo"])

# --- caso base acquisto ---
r = rt(s, target=90.0, lato="acquisto", orizzonte_giorni=90,
       lookback_giorni=120, n_scenari=2000, seed=42)
check("base ok", r["ok"] is True, r["motivo"])
check("gap_eur = p0 - target",
      abs(r["gap_eur"] - (r["prezzo_corrente"] - 90.0)) < 0.01, r["gap_eur"])
check("gap positivo (target sotto prezzo)", r["gap_eur"] > 0 and r["gap_pct"] > 0,
      (r["gap_eur"], r["gap_pct"]))
check("hit_rate in [0,1]", 0.0 <= r["hit_rate"] <= 1.0, r["hit_rate"])
check("prob_tocco in [0,1]", 0.0 <= r["prob_tocco"] <= 1.0, r["prob_tocco"])
check("stato valido", r["stato"] in ("raggiunto", "vicino", "lontano"), r["stato"])
check("echo parametri", (r["orizzonte_giorni"], r["n_scenari"], r["seed"]) == (90, 2000, 42))
b = r["df_bande"]
check("bande shape/colonne",
      b.shape == (90, 4) and list(b.columns) == ["Giorno", "P10 (€/MWh)", "P50 (€/MWh)", "P90 (€/MWh)"],
      b.shape)
check("P10<=P50<=P90", bool(((b["P50 (€/MWh)"] - b["P10 (€/MWh)"]) >= -1e-9).all())
      and bool(((b["P90 (€/MWh)"] - b["P50 (€/MWh)"]) >= -1e-9).all()))
g = r["df_giornaliero"]
check("giornaliero 120 righe", len(g) == 120, len(g))
m = r["df_mensile"]
check("mensile: hit% = tocchi/giorni",
      bool(((m["Hit rate (%)"] - m["Tocchi"] / m["Giorni"] * 100).abs() < 0.06).all()))
check("mensile: formato mese YYYY-MM",
      bool(m["Mese"].astype(str).str.match(r"^\d{4}-\d{2}$").all()))
check("vol_annua >= 0", r["vol_annua"] >= 0, r["vol_annua"])

# --- target gia' toccato: acquisto ---
s_flat = serie_giorni_piatta([100.0] * 60)
r = rt(s_flat, target=110.0, lato="acquisto")
check("acquisto target sopra -> tocco_ora", r["tocco_ora"] is True)
check("tocco_ora -> prob 1.0", r["prob_tocco"] == 1.0, r["prob_tocco"])
check("stato raggiunto", r["stato"] == "raggiunto", r["stato"])
check("gap negativo", r["gap_eur"] < 0, r["gap_eur"])

# --- vendita speculare ---
r = rt(s_flat, target=90.0, lato="vendita")
check("vendita target sotto -> tocco_ora", r["tocco_ora"] is True)
check("vendita -> prob 1.0", r["prob_tocco"] == 1.0)
check("vendita stato raggiunto", r["stato"] == "raggiunto")
check("vendita gap_eur = target - p0", abs(r["gap_eur"] - (90.0 - r["prezzo_corrente"])) < 0.01,
      r["gap_eur"])

# --- determinismo ---
r1 = rt(s, target=90.0, seed=42)
r2 = rt(s, target=90.0, seed=42)
check("stesso seed -> stessa prob", r1["prob_tocco"] == r2["prob_tocco"])
check("stesso seed -> stesse bande",
      bool((r1["df_bande"]["P50 (€/MWh)"] == r2["df_bande"]["P50 (€/MWh)"]).all()))

# --- serie piatta: sigma 0 ---
r = rt(s_flat, target=90.0, lato="acquisto")
check("sigma0 acquisto irraggiungibile -> prob 0", r["prob_tocco"] == 0.0, r["prob_tocco"])
r = rt(s_flat, target=110.0, lato="vendita")
check("sigma0 vendita irraggiungibile -> prob 0", r["prob_tocco"] == 0.0, r["prob_tocco"])
r = rt(s_flat, target=100.0, lato="acquisto")
check("sigma0 target uguale -> prob 1", r["prob_tocco"] == 1.0, r["prob_tocco"])

# --- prezzi negativi: shift ---
s_neg = serie_giorni_piatta([-20.0] * 30 + [30.0] * 30)
r = rt(s_neg, target=-10.0, lato="acquisto")
check("negativi ok", r["ok"] is True, r["motivo"])
check("shift_usato = 21", r["shift_usato"] == 21.0, r["shift_usato"])

# --- NaN sparsi ---
s_nan = serie_rumore()
s_nan.iloc[::37] = np.nan
r = rt(s_nan, target=90.0)
check("NaN sparsi ok", r["ok"] is True, r["motivo"])
check("NaN: lookback completo", r["n_giorni_lookback"] == 120, r["n_giorni_lookback"])

# --- hit rate esatto ---
s_hr = serie_giorni_piatta([80.0] * 10 + [100.0] * 30)
r = rt(s_hr, target=90.0, lato="acquisto", lookback_giorni=40)
check("hit_rate esatto 0.25", r["hit_rate"] == 0.25, r["hit_rate"])
check("n_hit esatto 10", r["n_hit"] == 10, r["n_hit"])

# --- giorni da ultimo tocco ---
vals = [100.0] * 60
vals[54] = 80.0  # unico tocco 5 giorni prima della fine
s_lt = serie_giorni_piatta(vals)
r = rt(s_lt, target=90.0, lato="acquisto", lookback_giorni=60)
check("ultimo tocco 5 giorni fa", r["giorni_da_ultimo_tocco"] == 5,
      r["giorni_da_ultimo_tocco"])
check("data ultimo tocco", r["data_ultimo_tocco"] == "2026-02-24",
      r["data_ultimo_tocco"])
r = rt(s_flat, target=90.0, lato="acquisto")
check("mai toccato -> None", r["giorni_da_ultimo_tocco"] is None
      and r["data_ultimo_tocco"] is None)

# --- prezzo corrente zero: gap_pct None onesto ---
s_zero = serie_giorni_piatta([0.0] * 60)
r = rt(s_zero, target=50.0, lato="vendita")
check("prezzo zero ok", r["ok"] is True)
check("gap_pct None", r["gap_pct"] is None, r["gap_pct"])

# --- tz-aware ---
s_tz = serie_rumore().tz_localize("Europe/Zurich")
r = rt(s_tz, target=90.0)
check("tz-aware ok", r["ok"] is True, r["motivo"])

# --- tab presente in app.py ---
_src = open(APP, encoding="utf-8").read()
_riga_tabs = next((l for l in _src.splitlines() if "= st.tabs([" in l), "")
check("tab137 in st.tabs",
      "tab137" in _riga_tabs.split("= st.tabs([")[0], _riga_tabs[:60])
check("label Radar prezzo obiettivo", "🎯 Radar prezzo obiettivo" in _src)

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
