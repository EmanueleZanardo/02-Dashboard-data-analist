"""Test standalone tab153 'Profili tipo'.

Estrae calcola_profili_tipo, _pesi_profilo_tipo, PROFILI_TIPO e _fascia_aeegsi
da app.py via AST (niente Streamlit). Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_profili_tipo_2026-10-02_1240.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
WANT = {"calcola_profili_tipo", "_pesi_profilo_tipo", "PROFILI_TIPO", "_fascia_aeegsi"}
for node in tree.body:
    nome = getattr(node, "name", None)
    if nome is None and isinstance(node, ast.Assign):
        tg = [t.id for t in node.targets if isinstance(t, ast.Name)]
        nome = tg[0] if tg else None
    if nome in WANT:
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fv = ns["calcola_profili_tipo"]
pesi = ns["_pesi_profilo_tipo"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_ore(inizio, valori, tz=None):
    idx = pd.date_range(inizio, periods=len(valori), freq="h", tz=tz)
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


# --- 1. Prezzo piatto: tutti i profili catturano il prezzo medio ---
s = serie_ore("2026-01-05", [100.0] * 336)  # 2 settimane da lunedi'
r = fv(s, 1000.0)
check("flat: no errore", r["errore"] is None, r["errore"])
check("flat: valido", r["valido"] is True)
check("flat: 5 profili", len(r["tabella"]) == 5, len(r["tabella"]))
for _, row in r["tabella"].iterrows():
    check(f"flat: {row['Profilo']} cattura 100", abs(row["Prezzo catturato (€/MWh)"] - 100.0) < 1e-9, row["Prezzo catturato (€/MWh)"])
    check(f"flat: {row['Profilo']} premio 0", abs(row["Premio vs medio (€/MWh)"]) < 1e-9, row["Premio vs medio (€/MWh)"])
en_att = 1000.0 * 336 / 8760
check("flat: energia periodo", abs(r["energia_periodo"] - en_att) < 0.1, r["energia_periodo"])
check("flat: prezzo medio 100", abs(r["prezzo_medio"] - 100.0) < 1e-9)
tot_mwh = r["tabella"]["Energia (MWh)"].sum()
check("flat: somma MWh = 5x periodo", abs(tot_mwh - 5 * en_att) < 1.0, tot_mwh)

# --- 2. Industriale continuo: fattore di carico 100% ---
fc3 = r["tabella"].loc[r["tabella"]["Profilo"].str.contains("continuo"), "Fattore di carico (%)"].iloc[0]
check("continuo: FC 100%", abs(fc3 - 100.0) < 0.01, fc3)

# --- 3. Quote fasce sommano a 100 ---
for _, row in r["tabella"].iterrows():
    q = row["Quota F1 (%)"] + row["Quota F2 (%)"] + row["Quota F3 (%)"]
    check(f"quote100: {row['Profilo']}", abs(q - 100.0) < 0.2, q)

# --- 4. Spike serale: residenziale paga piu' della media, continuo = media ---
vals = []
for d in pd.date_range("2026-01-05", periods=14, freq="D"):
    for h in range(24):
        vals.append(300.0 if (d.dayofweek < 5 and 19 <= h < 22) else 100.0)
s2 = serie_ore("2026-01-05", vals)
r2 = fv(s2, 1000.0)
check("spike: valido", r2["valido"] is True, r2["errore"])
tab2 = r2["tabella"]
medio = s2.mean()
cont = tab2.loc[tab2["Profilo"].str.contains("continuo"), "Prezzo catturato (€/MWh)"].iloc[0]
res = tab2.loc[tab2["Profilo"].str.contains("Residenziale"), "Prezzo catturato (€/MWh)"].iloc[0]
check("spike: continuo == medio", abs(cont - medio) < 0.01, (cont, medio))
check("spike: residenziale > medio", res > medio, (res, medio))
uff = tab2.loc[tab2["Profilo"].str.contains("Uffici"), "Prezzo catturato (€/MWh)"].iloc[0]
check("spike: uffici < residenziale", uff < res, (uff, res))

# --- 5. Pompa di calore: piu' energia a gennaio che a luglio ---
idx = pd.date_range("2026-01-01", periods=24 * (31 + 28 + 31 + 30 + 31 + 30 + 31), freq="h")
s3 = pd.Series(np.full(len(idx), 80.0), index=idx)
r3 = fv(s3, 8760.0)
check("hp: valido", r3["valido"] is True, r3["errore"])
dm = r3["mensile"]
hp = dm[dm["Profilo"].str.contains("Pompa")]
gen = hp.loc[hp["Mese"] == "2026-01", "MWh"].iloc[0]
lug = hp.loc[hp["Mese"] == "2026-07", "MWh"].iloc[0]
check("hp: gennaio > luglio", gen > lug, (gen, lug))
check("hp: rapporto ~ stagionale", abs(gen / lug - (1.6 / 0.3)) < 0.05, gen / lug)
# il continuo e' proporzionale alle ore del mese (gen 744h vs feb 672h)
ct = dm[dm["Profilo"].str.contains("continuo")]
mwh_ct = ct.set_index("Mese")["MWh"]
check("continuo: MWh proporzionali alle ore", abs(mwh_ct["2026-01"] / mwh_ct["2026-02"] - 744 / 672) < 1e-9,
      (mwh_ct["2026-01"], mwh_ct["2026-02"]))

# --- 6. Determinismo ---
r2b = fv(s2, 1000.0)
check("deterministico", r2["tabella"].equals(r2b["tabella"]))

# --- 7. NaN-safe ---
check("vuota -> errore", fv(pd.Series(dtype=float))["errore"] is not None)
check("indice non datetime -> errore", fv(pd.Series([1.0, 2.0]))["errore"] is not None)
check("troppo corta -> errore", fv(serie_ore("2026-01-05", [100.0] * 100))["errore"] is not None)
check("energia 0 -> errore", fv(s, 0.0)["errore"] is not None)
check("energia negativa -> errore", fv(s, -5.0)["errore"] is not None)
check("energia str -> errore", fv(s, "x")["errore"] is not None)
check("profili sconosciuti -> errore", fv(s, 1000.0, profili=["xxx"])["errore"] is not None)
check("profili None ok", fv(s, 1000.0, profili=None)["valido"] is True)
check("subset profili ok", len(fv(s, 1000.0, profili=["uffici", "residenziale"])["tabella"]) == 2)
s_nan = serie_ore("2026-01-05", [100.0] * 336)
s_nan.iloc[5:10] = np.nan
check("NaN scartati ok", fv(s_nan, 1000.0)["valido"] is True)

# --- 8. tz-aware ---
s_tz = serie_ore("2026-01-05", [100.0] * 336, tz="Europe/Zurich")
rtz = fv(s_tz, 1000.0)
check("tz-aware ok", rtz["valido"] is True, rtz["errore"])

# --- 9. Pesi non negativi e finiti per tutti i profili ---
ore = np.tile(np.arange(24), 14)
dow = np.repeat(np.arange(7), 48)[:336]
mese = np.full(336, 1)
for nome, etichetta, _ in ns["PROFILI_TIPO"]:
    w = pesi(nome, ore, dow, mese)
    check(f"pesi {nome}: finiti e >=0", np.all(np.isfinite(w)) and np.all(w >= 0))
    check(f"pesi {nome}: somma > 0", w.sum() > 0)
check("pesi: profilo ignoto solleva", True)
try:
    pesi("sconosciuto", ore, dow, mese)
    check("pesi: profilo ignoto solleva", False, "nessuna eccezione")
except ValueError:
    pass

# --- 10. Weekend puro: uffici quasi fermi, residenziale attivo ---
s_we = serie_ore("2026-01-10", [100.0] * 48)  # sab+dom
r_we = fv(s_we, 1000.0, min_ore=24)
check("weekend: valido", r_we["valido"] is True, r_we["errore"])
t_we = r_we["tabella"]
pu = t_we.loc[t_we["Profilo"].str.contains("Uffici"), "Picco (MW)"].iloc[0]
pr = t_we.loc[t_we["Profilo"].str.contains("Residenziale"), "Picco (MW)"].iloc[0]
check("weekend: picco uffici < residenziale", pu < pr, (pu, pr))

print(f"checks: {checks}, fails: {len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
