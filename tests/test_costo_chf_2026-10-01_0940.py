"""Test standalone tab124 'Costo in franchi (EUR/CHF)'.

Estrae calcola_costo_chf + scarica_fx_ecb + fascia_oraria da app.py via AST
(niente Streamlit). Stile QA: conta i check, 0 fail attesi.
Uso: python3 hidden_files/test_costo_chf_2026-10-01_0940.py
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
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_costo_chf", "scarica_fx_ecb", "fascia_oraria"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
chf = ns["calcola_costo_chf"]
scarica = ns["scarica_fx_ecb"]

fascia = ns["fascia_oraria"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} {detail}")


def serie_ore(n_ore, prezzo, inizio="2026-01-01"):
    idx = pd.date_range(inizio, periods=n_ore, freq="h")
    return pd.Series(prezzo, index=idx, dtype=float)


# 1) Tasso costante: proporzionalita' esatta
s = serie_ore(24 * 60, 100.0)
r = chf(s, mw_f1=2.0, mw_f2=1.5, mw_f3=1.0, fx=0.95)
check("valido", r["valido"] is True)
check("errore None", r["errore"] is None)
check("fx_usato costante", r["fx_usato"] == "costante")
check("costo_chf == costo_eur*fx", abs(r["costo_chf"] - r["costo_eur"] * 0.95) < 1e-6)
check("fx_medio_ponderato == fx", r["fx_medio_ponderato"] == 0.95)
ore_f1 = sum(1 for t in s.index if fascia(t) == "F1")
ore_f2 = sum(1 for t in s.index if fascia(t) == "F2")
ore_f3 = sum(1 for t in s.index if fascia(t) == "F3")
atteso_eur = 100.0 * (2.0 * ore_f1 + 1.5 * ore_f2 + 1.0 * ore_f3)
check("costo_eur == somma(prezzo*mw)", abs(r["costo_eur"] - atteso_eur) < 1e-6,
      f"{r['costo_eur']} vs {atteso_eur}")
check("mwh_totale", abs(r["mwh_totale"] - (2.0 * ore_f1 + 1.5 * ore_f2 + 1.0 * ore_f3)) < 1e-9)
check("n_mesi == 3 (60gg dal 1/1)", r["n_mesi"] == 3, str(r["n_mesi"]))
check("n_ore", r["n_ore"] == 24 * 60)
check("df righe == mesi", len(r["df_mensile"]) == r["n_mesi"])
check("df colonne", list(r["df_mensile"].columns) == ["Mese", "Costo EUR", "Costo CHF", "EURCHF medio"])
for _, row in r["df_mensile"].iterrows():
    check("EURCHF medio mese == 0.95", row["EURCHF medio"] == 0.95)
    check("CHF mese proporzionale", abs(row["Costo CHF"] - row["Costo EUR"] * 0.95) < 0.02)

# 2) fx None -> default 0.95 costante
r2 = chf(s)
check("default fx_usato costante", r2["fx_usato"] == "costante")
check("default fx_medio == 0.95", r2["fx_medio_ponderato"] == 0.95)

# 3) Serie giornaliera: forward-fill sulle ore
giorni = pd.date_range("2026-01-01", periods=60, freq="D")
fxd = pd.Series(np.linspace(0.90, 1.00, 60), index=giorni)
r3 = chf(s, fx=fxd)
check("fx_usato storico", r3["fx_usato"] == "storico")
check("n_giorni_fx == 60", r3["n_giorni_fx"] == 60)
check("costo_chf tra bound", r3["costo_eur"] * 0.90 <= r3["costo_chf"] <= r3["costo_eur"] * 1.00)
# prima ora usa il tasso del primo giorno (bfill/ffill ok)
check("fx_medio in range", 0.90 <= r3["fx_medio_ponderato"] <= 1.00)
# weekend buchi: serie solo feriali -> ffill copre
fxd_buco = fxd[fxd.index.weekday < 5]
r3b = chf(s, fx=fxd_buco)
check("buchi feriali ok", r3b["valido"] is True and r3b["fx_usato"] == "storico")

# 4) Sensibilita'
for shock in (-0.05, -0.01, 0.01, 0.05):
    check(f"sens {shock}", r["sensibilita"][shock] == round(r["costo_chf"] * shock, 2))
check("sens simmetrica", abs(r["sensibilita"][0.05] + r["sensibilita"][-0.05]) < 0.02)

# 5) Tasso coperto: segno del risparmio
rc = chf(s, fx=0.95, fx_coperto=0.90)  # coperto piu' basso = franco forte = risparmio
check("coperto costo", rc["costo_chf_coperto"] == round(rc["costo_eur"] * 0.90, 2))
check("risparmio positivo", rc["risparmio_cambio"] > 0, str(rc["risparmio_cambio"]))
rc2 = chf(s, fx=0.95, fx_coperto=1.00)  # coperto peggiore = extracosto
check("extracosto negativo", rc2["risparmio_cambio"] < 0, str(rc2["risparmio_cambio"]))
rc3 = chf(s, fx=0.95, fx_coperto=0.95)
check("parita' zero", rc3["risparmio_cambio"] == 0.0)
rc4 = chf(s, fx=0.95)
check("no coperto -> None", rc4["costo_chf_coperto"] is None and rc4["risparmio_cambio"] is None)

# 6) Errori di input
re_ = chf(s, mw_f1=-1.0)
check("mw negativo -> errore", re_["errore"] is not None and re_["valido"] is False)
re_ = chf(s, mw_f1=0.0, mw_f2=0.0, mw_f3=0.0)
check("mw tutti zero -> errore", re_["errore"] is not None)
re_ = chf(s, mw_f1=6000.0)
check("mw > 5000 -> errore", re_["errore"] is not None)
re_ = chf(s, mw_f1="x")
check("mw non numerico -> errore", re_["errore"] is not None)
re_ = chf(s, fx=0.0)
check("fx zero -> errore", re_["errore"] is not None)
re_ = chf(s, fx=-0.5)
check("fx negativo -> errore", re_["errore"] is not None)
re_ = chf(s, fx=pd.Series(dtype=float))
check("fx serie vuota -> errore", re_["errore"] is not None)
re_ = chf(s, fx=pd.Series([-0.9], index=[pd.Timestamp("2026-01-01")]))
check("fx serie negativa -> errore", re_["errore"] is not None)
re_ = chf(s, fx=0.95, fx_coperto="x")
check("fx_coperto non numerico -> errore", re_["errore"] is not None)
re_ = chf(s, fx=0.95, fx_coperto=0.0)
check("fx_coperto zero -> errore", re_["errore"] is not None)

# 7) NaN-safe
rv = chf(pd.Series(dtype=float))
check("serie vuota -> non valido", rv["valido"] is False and rv["errore"] is None)
rv = chf(serie_ore(10, 100.0))
check("<24 ore -> non valido", rv["valido"] is False)
rv = chf(pd.Series([100.0] * 30, index=range(30)))
check("indice intero -> errore", rv["errore"] is not None)
s_nan = serie_ore(24 * 5, 100.0)
s_nan.iloc[::7] = np.nan
rv = chf(s_nan, fx=0.95)
check("NaN scartati, valido", rv["valido"] is True)
check("NaN: n_ore ridotto", rv["n_ore"] < 24 * 5, str(rv["n_ore"]))

# 8) Prezzi negativi: costo puo' essere negativo, fx_medio None-safe
s_neg = serie_ore(24 * 5, -10.0)
rv = chf(s_neg, fx=0.95)
check("prezzi negativi valido", rv["valido"] is True)
check("costo negativo coerente", rv["costo_chf"] < 0)
check("fx_medio None con costo neg", rv["fx_medio_ponderato"] == 0.95)

# 9) scarica_fx_ecb non solleva mai (offline -> None)
try:
    out = scarica("1900-01-01", "1900-01-05", timeout=5)
    check("scarica offline-safe", out is None or isinstance(out, pd.Series))
except Exception as e:  # noqa: BLE001
    check("scarica non solleva", False, str(e))

print(f"CHECKS: {checks}, FAILS: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
