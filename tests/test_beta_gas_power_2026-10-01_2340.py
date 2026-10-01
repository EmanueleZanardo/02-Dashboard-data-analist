"""Test standalone tab140 'Beta gas-power'.

Estrae calcola_beta_gas_power da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_beta_gas_power_2026-10-01_2340.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_beta_gas_power":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
bg = ns["calcola_beta_gas_power"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_oraria(inizio, giorni, valori_fn):
    idx = pd.date_range(inizio, periods=giorni * 24, freq="h", tz="Europe/Zurich")
    d0 = idx[0].date()
    return pd.Series([valori_fn((ts.date() - d0).days) for ts in idx], index=idx)


# --- dataset sintetico con relazione nota: power = 10 + 2.5 * gas + rumore ---
rng = np.random.default_rng(42)
giorni = 120
gas_idx = pd.date_range("2026-01-01", periods=giorni, freq="D", tz="Europe/Zurich")
gas_vals = 30 + 8 * np.sin(2 * np.pi * np.arange(giorni) / 30.0) + rng.normal(0, 1.5, giorni)
gas = pd.Series(gas_vals, index=gas_idx)
power_g = 10 + 2.5 * gas_vals + rng.normal(0, 2.0, giorni)
pw = serie_oraria("2026-01-01", giorni, lambda dd: power_g[min(dd, giorni - 1)])

r = bg(pw, gas)
check("valido base", r["valido"] and r["errore"] is None, r["errore"])
check("beta ~ 2.5", abs(r["beta"] - 2.5) < 0.15, r["beta"])
check("alpha ~ 10", abs(r["alpha"] - 10) < 2.0, r["alpha"])
check("r2 alto", r["r2"] > 0.9, r["r2"])
check("corr ~ sqrt(r2)", abs(abs(r["correlazione"]) - r["r2"] ** 0.5) < 1e-9, r["correlazione"])
check("n_giorni", r["n_giorni"] == giorni, r["n_giorni"])
check("std_residui ~ 2", abs(r["std_residui"] - 2.0) < 0.5, r["std_residui"])
check("gas_medio", abs(r["gas_medio"] - gas_vals.mean()) < 1e-9, r["gas_medio"])
check("power_medio", abs(r["power_medio"] - power_g.mean()) < 1e-9, r["power_medio"])

# --- relazione esatta: beta 3, alpha 5, r2 1 ---
gas2 = pd.Series(np.linspace(20, 60, 60), index=pd.date_range("2026-03-01", periods=60, freq="D"))
pw2_vals = 5 + 3 * gas2.to_numpy()
pw2 = serie_oraria("2026-03-01", 60, lambda dd: pw2_vals[min(dd, 59)])
r2 = bg(pw2, gas2)
check("beta esatta 3", abs(r2["beta"] - 3.0) < 1e-9, r2["beta"])
check("alpha esatta 5", abs(r2["alpha"] - 5.0) < 1e-9, r2["alpha"])
check("r2 esatto 1", abs(r2["r2"] - 1.0) < 1e-9, r2["r2"])

# --- rolling: n - min_giorni + 1 righe ---
check("rolling righe", len(r["df_rolling"]) == giorni - 30 + 1, len(r["df_rolling"]))
check("rolling colonne", list(r["df_rolling"].columns) == ["Fine finestra", "Beta", "R²"])
check("rolling beta media ~ 2.5", abs(r["df_rolling"]["Beta"].mean() - 2.5) < 0.2,
      r["df_rolling"]["Beta"].mean())
check("rolling beta ultima ~ 2.5", abs(float(r["df_rolling"]["Beta"].iloc[-1]) - 2.5) < 0.4,
      r["df_rolling"]["Beta"].iloc[-1])

# --- scatter ---
check("scatter righe", len(r["df_scatter"]) == giorni, len(r["df_scatter"]))
check("scatter colonne", list(r["df_scatter"].columns) == ["Giorno", "Gas (€/MWh)", "Power (€/MWh)"])

# --- scenari: +10% gas -> delta = beta * 0.1 * gas_medio ---
sc = r["df_scenari"]
check("scenari righe", len(sc) == 6, len(sc))
row10 = sc[sc["Variazione gas"] == "+10 %"].iloc[0]
atteso = r["beta"] * 0.1 * r["gas_medio"]
check("scenario +10% delta", abs(row10["Δ prezzo (€/MWh)"] - atteso) < 0.05, row10["Δ prezzo (€/MWh)"])
check("scenario +10% prezzo atteso",
      abs(row10["Prezzo atteso (€/MWh)"] - (r["power_medio"] + atteso)) < 0.05,
      row10["Prezzo atteso (€/MWh)"])
row_m30 = sc[sc["Variazione gas"] == "-30 %"].iloc[0]
check("scenario -30% negativo", row_m30["Δ prezzo (€/MWh)"] < 0, row_m30["Δ prezzo (€/MWh)"])

# --- profilo peak: solo lun-ven 8-20 ---
rp = bg(pw, gas, profilo="peak")
check("peak valido", rp["valido"], rp["errore"])
check("peak beta ~ 2.5", abs(rp["beta"] - 2.5) < 0.25, rp["beta"])
# giorni peak attesi: lun-ven con ore 8-20 presenti
check("peak giorni <= base", rp["n_giorni"] <= r["n_giorni"], (rp["n_giorni"], r["n_giorni"]))

# --- tz-naive ok ---
r_naive = bg(pw.tz_localize(None), gas.tz_localize(None))
check("tz-naive ok", r_naive["valido"] and abs(r_naive["beta"] - r["beta"]) < 1e-9, r_naive["errore"])

# --- errori puliti ---
re = bg(pd.Series(dtype=float), gas)
check("elettrica vuota -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pw, pd.Series(dtype=float))
check("gas vuota -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pd.Series([1.0, 2.0], index=[0, 1]), gas)
check("indice non-datetime -> errore", not re["valido"] and re["errore"], "doveva fallire")
gas_cost = pd.Series(np.full(60, 40.0), index=pd.date_range("2026-03-01", periods=60, freq="D"))
re = bg(pw2, gas_cost)
check("gas costante -> errore", not re["valido"] and "costante" in re["errore"], re["errore"])
gas_pochi = pd.Series(np.linspace(20, 30, 15), index=pd.date_range("2026-03-01", periods=15, freq="D"))
re = bg(pw2, gas_pochi)
check("pochi giorni -> errore", not re["valido"] and "insufficienti" in re["errore"], re["errore"])
re = bg(pw, gas, profilo="x")
check("profilo invalido -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pw, gas, finestra="xx")
check("finestra non numerica -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pw, gas, min_giorni=5)
check("min_giorni < 10 -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pw, gas, finestra=20, min_giorni=30)
check("finestra < min_giorni -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pw, "non una serie")
check("input non-serie -> errore", not re["valido"] and re["errore"], "doveva fallire")
re = bg(pd.Series(["a", "b"], index=pd.date_range("2026-01-01", periods=2, freq="D")), gas)
check("elettrica non numerica -> errore", not re["valido"] and re["errore"], "doveva fallire")

# --- gas senza sovrapposizione temporale ---
gas_lontano = pd.Series(np.linspace(20, 40, 60), index=pd.date_range("2020-01-01", periods=60, freq="D"))
re = bg(pw2, gas_lontano)
check("nessun giorno comune -> errore", not re["valido"] and re["errore"], "doveva fallire")

print(f"check: {checks}, fail: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
