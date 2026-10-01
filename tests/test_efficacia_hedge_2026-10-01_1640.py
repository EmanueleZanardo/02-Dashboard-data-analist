"""Test standalone tab131 'Test efficacia hedge'.

Estrae calcola_test_efficacia_hedge da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_efficacia_hedge_2026-10-01_1640.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())

ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == \
            "calcola_test_efficacia_hedge":
        exec(compile(ast.Module(body=[node], type_ignores=[]),
                     "app.py", "exec"), ns)
eff = ns["calcola_test_efficacia_hedge"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_spot(n=150, base=100.0):
    t = np.arange(n, dtype=float)
    vals = base + 8.0 * np.sin(2 * np.pi * t / 7.0) \
        + 0.4 * t + 2.0 * np.sin(2 * np.pi * t / 30.0)
    idx = pd.date_range("2026-01-01", periods=n, freq="D")
    return pd.Series(vals, index=idx)


FIN = 30
r = eff(serie_spot(), tipo_hedge="media_mobile", n_fissaggio=30,
        finestra_gg=FIN, r2_min=0.8)

# --- esito base ---
check("valido", r["valido"] is True and r["errore"] is None,
      f"errore={r['errore']}")
check("n_finestre_coerente",
      r["n_finestre"] == len(r["spot"]) - 1 - FIN + 1,
      f"n={r['n_finestre']} atteso={len(r['spot']) - 1 - FIN + 1}")
check("colonne_df",
      list(r["finestre"].columns) == ["Fine finestra", "Beta", "R²",
                                      "Efficace"],
      str(list(r["finestre"].columns)))
check("len_df", len(r["finestre"]) == r["n_finestre"])

# --- coerenza OLS ultima finestra ---
xh = np.asarray(r["d_hedge_ultima"], dtype=float)
ys = np.asarray(r["d_spot_ultima"], dtype=float)
check("len_scatter", len(xh) == FIN and len(ys) == FIN,
      f"{len(xh)} {len(ys)}")
beta_man = float(np.cov(xh, ys, ddof=0)[0, 1] / np.var(xh))
check("beta_corrente_ols", abs(r["beta_corrente"] - beta_man) < 1e-9,
      f"{r['beta_corrente']} vs {beta_man}")
cc = float(np.corrcoef(xh, ys)[0, 1])
check("r2_corrente_ols", abs(r["r2_corrente"] - cc ** 2) < 1e-9,
      f"{r['r2_corrente']} vs {cc ** 2}")
check("r2_in_[0,1]", 0.0 <= r["r2_corrente"] <= 1.0)
resid = ys - (r["alpha_ultima"] + r["beta_ultima"] * xh)
check("residui_media_zero", abs(float(resid.mean())) < 1e-9,
      f"media residui={resid.mean()}")

# --- le coppie scatter sono davvero l'ultima finestra dei delta ---
ds_man = r["spot"].diff().dropna().to_numpy(dtype=float)
dh_man = r["prezzo_hedge"].diff().dropna().to_numpy(dtype=float)
n_d = min(len(ds_man), len(dh_man))
check("scatter_ultima_finestra",
      np.allclose(xh, dh_man[n_d - FIN:n_d]) and
      np.allclose(ys, ds_man[n_d - FIN:n_d]))

# --- flag Efficace coerente con la definizione ---
ok_flag = True
for _, row in r["finestre"].iterrows():
    atteso = "sì" if (0.8 <= abs(float(row["Beta"])) <= 1.25
                      and float(row["R²"]) >= 0.8) else "no"
    if row["Efficace"] != atteso:
        ok_flag = False
        break
check("flag_efficace_definizione", ok_flag)
check("pct_efficaci",
      abs(r["pct_efficaci"] - 100.0 * r["n_efficaci"] / r["n_finestre"]) < 1e-9)
check("beta_finiti",
      bool(np.isfinite(r["finestre"]["Beta"].to_numpy(dtype=float)).all()))
check("beta_medio",
      abs(r["beta_medio"] - float(r["finestre"]["Beta"].mean())) < 1e-3,
      "tolleranza 1e-3: la tabella arrotonda β a 4 decimali")

# --- basis e statistiche ---
check("basis_definizione",
      np.allclose(r["basis"].to_numpy(dtype=float),
                  (r["spot"] - r["prezzo_hedge"]).to_numpy(dtype=float)))
check("basis_media",
      abs(r["basis_media"] - float(r["basis"].mean())) < 1e-9)
check("tracking_error",
      abs(r["tracking_error"] - float(r["basis"].std())) < 1e-9)
check("indici_allineati",
      r["spot"].index.equals(r["prezzo_hedge"].index)
      and r["spot"].index.equals(r["basis"].index))

# --- tipo indice_mese_precedente ---
r2 = eff(serie_spot(200), tipo_hedge="indice_mese_precedente",
         finestra_gg=FIN, r2_min=0.8)
check("indice_valido", r2["valido"] is True and r2["errore"] is None,
      f"errore={r2['errore']}")
check("indice_primo_mese_escluso",
      r2["spot"].index.min() >= pd.Timestamp("2026-02-01"),
      str(r2["spot"].index.min()))
# con l'indice mensile il fixing e' costante dentro il mese: le finestre
# interamente intra-mese hanno var(Δfh)=0 e vengono saltate onestamente
dh2 = r2["prezzo_hedge"].diff().dropna().to_numpy(dtype=float)
attese_indice = sum(1 for i in range(len(dh2) - FIN + 1)
                    if float(np.var(dh2[i:i + FIN])) > 0)
check("indice_n_finestre",
      r2["n_finestre"] == attese_indice
      and r2["n_finestre"] <= len(r2["spot"]) - 1 - FIN + 1,
      f"n={r2['n_finestre']} attese_con_varianza={attese_indice}")

# --- casi degeneri ---
rc = eff(pd.Series(100.0, index=pd.date_range("2026-01-01", periods=150,
                                              freq="D")))
check("prezzi_costanti_non_valido",
      rc["valido"] is False and rc["errore"] is not None
      and "varianza" in rc["errore"].lower(),
      f"errore={rc['errore']}")
re_ = eff(pd.Series(dtype=float))
check("serie_vuota", re_["valido"] is False and re_["errore"] is not None)
re_ = eff(serie_spot(), finestra_gg=5)
check("finestra_troppo_piccola",
      re_["valido"] is False and re_["errore"] is not None)
re_ = eff(serie_spot(), n_fissaggio=1)
check("n_fissaggio_troppo_piccolo",
      re_["valido"] is False and re_["errore"] is not None)
re_ = eff(serie_spot(), r2_min=1.5)
check("r2_min_fuori_range",
      re_["valido"] is False and re_["errore"] is not None)
re_ = eff(serie_spot(), tipo_hedge="sconosciuto")
check("tipo_non_valido",
      re_["valido"] is False and re_["errore"] is not None)
re_ = eff(serie_spot(), banda=(1.5, 0.5))
check("banda_invertita",
      re_["valido"] is False and re_["errore"] is not None)

# --- robustezza NaN / inf ---
s_nan = serie_spot()
s_nan.iloc[10:15] = np.nan
s_nan.iloc[100] = np.nan
rn = eff(s_nan)
check("nan_tollerati", rn["valido"] is True, f"errore={rn['errore']}")
s_inf = serie_spot()
s_inf.iloc[50] = np.inf
ri = eff(s_inf)
check("inf_rifiutati",
      ri["valido"] is False and ri["errore"] is not None)

# --- banda personalizzata cambia il flag in modo coerente ---
rb = eff(serie_spot(), banda=(0.9, 1.1), r2_min=0.8)
ok_b = True
for _, row in rb["finestre"].iterrows():
    atteso = "sì" if (0.9 <= abs(float(row["Beta"])) <= 1.1
                      and float(row["R²"]) >= 0.8) else "no"
    if row["Efficace"] != atteso:
        ok_b = False
        break
check("banda_custom_coerente", rb["valido"] is True and ok_b)

# --- dati insufficienti ---
rs = eff(serie_spot(40))
check("dati_insufficienti",
      rs["valido"] is False and rs["errore"] is not None,
      f"errore={rs['errore']}")

print(f"{checks} check / {len(fails)} fail")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
