"""Test standalone tab126 'Ricavi da riserva (SDL)'.

Estrae calcola_ricavi_riserva da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_ricavi_riserva_2026-10-01_1140.py
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
            "calcola_ricavi_riserva",):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
ris = ns["calcola_ricavi_riserva"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def ore(n, start="2026-01-01"):
    return pd.Series(50.0, index=pd.date_range(start, periods=n, freq="h"))


# --- 1. ricavo potenza esatto su periodo noto ---
s720 = ore(720)  # 30 giorni di gennaio
r = ris(s720, mw_primaria=2.0, prezzo_primaria=14.0)
check("valido base", r["valido"] and r["errore"] is None)
check("n_ore", r["n_ore"] == 720, r["n_ore"])
check("ricavo potenza esatto", r["ricavo_totale"] == 2.0 * 14.0 * 720,
      r["ricavo_totale"])
check("primaria ricavo_potenza", r["per_prodotto"]["primaria"]["ricavo_potenza"] == 20160.0)

# --- 2. energia terziaria ---
r2 = ris(s720, mw_terziaria_pos=1.0, prezzo_terziaria_pos=5.0,
         ore_chiamata_terz_pos=100.0, prezzo_energia_pos=120.0)
att = 1.0 * 5.0 * 720 + 1.0 * 100.0 * 120.0
check("terziaria pos totale", r2["ricavo_totale"] == att, r2["ricavo_totale"])
check("terziaria pos energia", r2["per_prodotto"]["terziaria_pos"]["ricavo_energia"] == 12000.0)
r3 = ris(s720, mw_terziaria_neg=3.0, prezzo_terziaria_neg=4.0,
         ore_chiamata_terz_neg=50.0, prezzo_energia_neg=40.0)
check("terziaria neg totale", r3["ricavo_totale"] == 3.0 * 4.0 * 720 + 3.0 * 50.0 * 40.0,
      r3["ricavo_totale"])
check("energia solo su terziaria pos",
      r2["per_prodotto"]["primaria"]["ricavo_energia"] == 0.0 and
      r2["per_prodotto"]["secondaria"]["ricavo_energia"] == 0.0 and
      r2["per_prodotto"]["terziaria_neg"]["ricavo_energia"] == 0.0)

# --- 3. MW nulli -> ricavo 0, valido ---
r0 = ris(s720)
check("zero MW valido", r0["valido"] and r0["errore"] is None)
check("zero MW ricavo 0", r0["ricavo_totale"] == 0.0)
check("zero MW miglior_prodotto None", r0["miglior_prodotto"] is None)

# --- 4. coerenza mensile ---
rm = ris(s720, mw_primaria=1.0, mw_secondaria=2.0, prezzo_primaria=10.0,
         prezzo_secondaria=7.0, mw_terziaria_pos=1.0, prezzo_terziaria_pos=5.0,
         ore_chiamata_terz_pos=24.0, prezzo_energia_pos=100.0)
dfm = rm["df_mensile"]
check("colonne df", list(dfm.columns) == ["Mese", "Ore", "Primaria (CHF)",
      "Secondaria (CHF)", "Terziaria + (CHF)", "Terziaria - (CHF)", "Totale (CHF)"],
      list(dfm.columns))
check("ore mensili = n_ore", int(dfm["Ore"].sum()) == rm["n_ore"])
check("somma mensili = totale (tol)",
      abs(dfm["Totale (CHF)"].sum() - rm["ricavo_totale"]) < 1.0,
      dfm["Totale (CHF)"].sum())
check("n_mesi", rm["n_mesi"] == 1 and len(dfm) == 1)
check("medio mensile", rm["ricavo_medio_mensile"] == rm["ricavo_totale"])

# periodo su due mesi
s2000 = ore(2000, start="2026-01-15")
r5 = ris(s2000, mw_primaria=1.0, prezzo_primaria=10.0)
check("quattro mesi (gen-apr)", r5["n_mesi"] == 4, r5["n_mesi"])  # 15 gen + 2000h -> 8 apr
check("somma mensili due mesi (tol)",
      abs(r5["df_mensile"]["Totale (CHF)"].sum() - r5["ricavo_totale"]) < 1.0)
check("ore mensili due mesi", int(r5["df_mensile"]["Ore"].sum()) == 2000)

# --- 5. scenari lineari ---
check("scenari chiavi", sorted(r["scenari"].keys()) == [0.0, 0.5, 1.0, 1.5, 2.0])
check("scenario 0 -> 0", r["scenari"][0.0] == 0.0)
check("scenario 2x", r["scenari"][2.0] == 2.0 * r["ricavo_totale"])
check("scenario 1x = totale", r["scenari"][1.0] == r["ricavo_totale"])

# --- 6. sensibilita' (solo potenza, energia invariata) ---
pot = 2.0 * 14.0 * 720
check("sens -30%", r["sensibilita"][-0.3] == pot * -0.3, r["sensibilita"][-0.3])
check("sens +100%", r["sensibilita"][1.0] == pot * 1.0)
check("sens con energia invariata", r2["sensibilita"][1.0] == 1.0 * 5.0 * 720,
      r2["sensibilita"][1.0])

# --- 7. miglior prodotto e quote ---
check("miglior prodotto", rm["miglior_prodotto"] == "secondaria",
      rm["miglior_prodotto"])
q = sum(p["quota"] for p in rm["per_prodotto"].values())
check("quote sommano a 1", abs(q - 1.0) < 1e-12, q)
check("quota migliore coerente",
      abs(rm["quota_migliore"] - rm["per_prodotto"]["secondaria"]["quota"]) < 1e-12)
check("annuo_per_mw", rm["per_prodotto"]["primaria"]["annuo_per_mw"] == 10.0 * 8760.0)

# --- 8. errori di validazione ---
re1 = ris(s720, mw_primaria=-1.0)
check("MW negativo -> errore", re1["errore"] is not None and not re1["valido"])
re2 = ris(s720, prezzo_primaria=-5.0)
check("prezzo negativo -> errore", re2["errore"] is not None)
re3 = ris(s720, mw_primaria=6000.0)
check("MW oltre limite -> errore", re3["errore"] is not None)
re4 = ris(s720, ore_chiamata_terz_pos=721.0, mw_terziaria_pos=1.0)
check("ore chiamata > n_ore -> errore", re4["errore"] is not None)
re5 = ris(s720, ore_chiamata_terz_neg=-2.0, mw_terziaria_neg=1.0)
check("ore chiamata negative -> errore", re5["errore"] is not None)
re6 = ris(s720, prezzo_energia_pos=-10.0, mw_terziaria_pos=1.0,
          ore_chiamata_terz_pos=10.0)
check("prezzo energia negativo -> errore", re6["errore"] is not None)
re7 = ris(pd.Series([50.0, 51.0, 52.0]))
check("indice non datetime -> errore", re7["errore"] is not None)
re8 = ris(ore(10))
check("<24h -> valido False", not re8["valido"] and re8["errore"] is None)
re9 = ris(pd.Series([], dtype=float,
                    index=pd.DatetimeIndex([], tz=None)))
check("serie vuota -> valido False", not re9["valido"])
re10 = ris("non una serie")
check("input non interpretabile -> errore", re10["errore"] is not None)
re11 = ris(s720, mw_primaria="x")
check("MW non numerico -> errore", re11["errore"] is not None)

# --- 9. NaN droppati ---
s_nan = ore(720).copy()
s_nan.iloc[0:48] = np.nan
rn = ris(s_nan, mw_primaria=1.0, prezzo_primaria=10.0)
check("NaN droppati n_ore", rn["n_ore"] == 672, rn["n_ore"])
check("NaN droppati ricavo", rn["ricavo_totale"] == 1.0 * 10.0 * 672)

# --- 10. terziaria senza chiamata -> solo potenza ---
rt = ris(s720, mw_terziaria_pos=2.0, prezzo_terziaria_pos=5.0)
check("terziaria senza chiamata", rt["ricavo_totale"] == 2.0 * 5.0 * 720,
      rt["ricavo_totale"])

print(f"check: {checks}, fail: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
