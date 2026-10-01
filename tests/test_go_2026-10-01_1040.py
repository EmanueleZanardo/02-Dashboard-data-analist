"""Test standalone tab125 'Garanzie d'origine (GO)'.

Estrae calcola_costo_go + fascia_oraria da app.py via AST
(niente Streamlit). Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_go_2026-10-01_1040.py
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
            "calcola_costo_go", "fascia_oraria"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
go = ns["calcola_costo_go"]
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


s = serie_ore(24 * 60, 100.0)  # 60 giorni dal 1/1/2026
ore_f1 = sum(1 for t in s.index if fascia(t) == "F1")
ore_f2 = sum(1 for t in s.index if fascia(t) == "F2")
ore_f3 = sum(1 for t in s.index if fascia(t) == "F3")
mwh_attesi = 2.0 * ore_f1 + 1.5 * ore_f2 + 1.0 * ore_f3

# 1) Prezzo scalare, quota 100%: proporzionalita' esatta
r = go(s, mw_f1=2.0, mw_f2=1.5, mw_f3=1.0, quota_verde=1.0, prezzo_go=2.5)
check("valido", r["valido"] is True)
check("errore None", r["errore"] is None)
check("prezzo_medio == 2.5", r["prezzo_medio_go"] == 2.5)
check("mwh_totali", abs(r["mwh_totali"] - mwh_attesi) < 1e-6, str(r["mwh_totali"]))
check("mwh_verdi == totali (q=1)", abs(r["mwh_verdi"] - r["mwh_totali"]) < 1e-9)
check("costo == mwh_verdi*prezzo",
      abs(r["costo_go"] - r["mwh_verdi"] * 2.5) < 0.02, str(r["costo_go"]))
check("incidenza == costo/mwh", abs(r["incidenza_eur_mwh"] - r["costo_go"] / r["mwh_totali"]) < 1e-4)
check("mix_usato None con scalare", r["mix_usato"] is None)
check("n_mesi == 3 (60gg dal 1/1)", r["n_mesi"] == 3, str(r["n_mesi"]))
check("n_ore", r["n_ore"] == 24 * 60)
check("df righe == mesi", len(r["df_mensile"]) == r["n_mesi"])
check("df colonne", list(r["df_mensile"].columns) ==
      ["Mese", "MWh totali", "MWh verdi", "Prezzo GO medio", "Costo GO (€)"])
somma_mensile = r["df_mensile"]["Costo GO (€)"].sum()
check("somma mensile == totale", abs(somma_mensile - r["costo_go"]) < 0.05,
      f"{somma_mensile} vs {r['costo_go']}")
for _, row in r["df_mensile"].iterrows():
    check("prezzo medio mese == 2.5", row["Prezzo GO medio"] == 2.5)
    check("costo mese proporzionale",
          abs(row["Costo GO (€)"] - row["MWh verdi"] * 2.5) < 0.02)

# 2) Default (None, None): mix 70/20/10 su 0.60/1.80/1.20 = 0.90
r2 = go(s)
check("default valido", r2["valido"] is True)
check("default prezzo 0.90", abs(r2["prezzo_medio_go"] - 0.90) < 1e-9,
      str(r2["prezzo_medio_go"]))
check("default mix", r2["mix_usato"] == {"idro": 0.7, "solare": 0.2, "eolico": 0.1},
      str(r2["mix_usato"]))
check("default quota 1.0", r2["quota_verde"] == 1.0)

# 3) Dict prezzi + dict mix: media ponderata
r3 = go(s, prezzo_go={"idro": 1.0, "solare": 4.0}, mix_go={"idro": 3.0, "solare": 1.0})
check("mix normalizzato", r3["mix_usato"] == {"idro": 0.75, "solare": 0.25},
      str(r3["mix_usato"]))
check("prezzo ponderato 1.75", abs(r3["prezzo_medio_go"] - 1.75) < 1e-9,
      str(r3["prezzo_medio_go"]))
check("costo == verdi*1.75", abs(r3["costo_go"] - r3["mwh_verdi"] * 1.75) < 0.02)

# 4) Dict prezzi senza mix: pesi uguali
r4 = go(s, prezzo_go={"idro": 1.0, "eolico": 3.0})
check("pesi uguali default", r4["mix_usato"] == {"idro": 0.5, "eolico": 0.5},
      str(r4["mix_usato"]))
check("prezzo medio 2.0", abs(r4["prezzo_medio_go"] - 2.0) < 1e-9)

# 5) Quota 0 e quota parziale
r5 = go(s, quota_verde=0.0, prezzo_go=2.5)
check("quota 0 valido", r5["valido"] is True)
check("quota 0 costo 0", r5["costo_go"] == 0.0)
check("quota 0 verdi 0", r5["mwh_verdi"] == 0.0)
r6 = go(s, quota_verde=0.5, prezzo_go=2.5)
check("quota 0.5 verdi == meta'", abs(r6["mwh_verdi"] - r6["mwh_totali"] / 2) < 1e-9)
check("quota 0.5 costo == meta' q=1", abs(r6["costo_go"] - r["costo_go"] / 2) < 0.02)

# 6) Scenari e sensibilita'
check("scenari chiavi", set(r["scenari"].keys()) == {0.0, 0.25, 0.5, 0.75, 1.0})
check("scenario 0 -> 0", r["scenari"][0.0] == 0.0)
check("scenario 1 == totale", abs(r["scenari"][1.0] - r["costo_go"]) < 0.02)
check("scenario 0.5 == meta'", abs(r["scenari"][0.5] - r["scenari"][1.0] / 2) < 0.02)
check("sensibilita chiavi", set(r["sensibilita"].keys()) == {-0.5, 0.5, 1.0})
check("sens -50%", abs(r["sensibilita"][-0.5] + r["costo_go"] / 2) < 0.02)
check("sens +100%", abs(r["sensibilita"][1.0] - r["costo_go"]) < 0.02)

# 7) Casi non validi (valido False, errore None)
rv = go(pd.Series([], dtype=float), prezzo_go=1.0)
check("serie vuota non valida", rv["valido"] is False and rv["errore"] is None)
rc = go(serie_ore(10, 100.0), prezzo_go=1.0)
check("<24h non valida", rc["valido"] is False and rc["errore"] is None)

# 8) Errori di input
re1 = go(s, mw_f1=0, mw_f2=0, mw_f3=0, prezzo_go=1.0)
check("MW nulli -> errore", re1["errore"] is not None)
re2 = go(s, quota_verde=1.5, prezzo_go=1.0)
check("quota >1 -> errore", re2["errore"] is not None)
re3 = go(s, quota_verde=-0.1, prezzo_go=1.0)
check("quota <0 -> errore", re3["errore"] is not None)
re4 = go(s, prezzo_go=-1.0)
check("prezzo negativo -> errore", re4["errore"] is not None)
re5 = go(s, prezzo_go={"idro": 1.0}, mix_go={"idro": 0.0})
check("pesi somma 0 -> errore", re5["errore"] is not None)
re6 = go(s, prezzo_go={"nucleare": 1.0})
check("tecnologia sconosciuta -> errore", re6["errore"] is not None)
re7 = go(s, prezzo_go={"idro": 1.0, "solare": 2.0}, mix_go={"idro": 1.0})
check("mix non copre tecnologie -> errore", re7["errore"] is not None)
re8 = go(pd.Series([1.0, 2.0]), prezzo_go=1.0)
check("indice non datetime -> errore", re8["errore"] is not None)

print(f"check: {checks}, fail: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
