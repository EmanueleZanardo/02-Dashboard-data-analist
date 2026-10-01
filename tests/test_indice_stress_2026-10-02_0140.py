"""Test standalone tab142 'Indice di stress di mercato'.

Estrae calcola_indice_stress da app.py via AST (niente Streamlit).
Stile QA: conta i check, 0 fail attesi.
Uso: python3 tests/test_indice_stress_2026-10-02_0140.py
"""
import ast
import os

import numpy as np
import pandas as pd

APP = os.path.expanduser("~/workspace/dashboard-qa/app.py")

tree = ast.parse(open(APP, encoding="utf-8").read())
ns = {"np": np, "pd": pd}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_indice_stress":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
fs = ns["calcola_indice_stress"]

checks = 0
fails = []


def check(name, cond, detail=""):
    global checks
    checks += 1
    if not cond:
        fails.append(f"{name} | {detail}")


def serie_giorni(inizio, medie, ore_per_giorno=None, tz=None):
    """Serie oraria: medie[d] = prezzo costante del giorno d, oppure lista di
    array orari per giorno se ore_per_giorno e' fornita."""
    pezzi = []
    for d, m in enumerate(medie):
        if ore_per_giorno is not None and ore_per_giorno[d] is not None:
            pezzi.append(np.asarray(ore_per_giorno[d], dtype=float))
        else:
            pezzi.append(np.full(24, float(m)))
    idx = pd.date_range(inizio, periods=len(pezzi) * 24, freq="h", tz=tz)
    return pd.Series(np.concatenate(pezzi), index=idx)


# --- 1. Prezzi costanti: SSI tutto 0, calmo ---
s = serie_giorni("2026-01-01", [60.0] * 60)
r = fs(s)
check("costante: no errore", r["errore"] is None, r["errore"])
check("costante: valido", r["valido"] is True)
check("costante: SSI tutti 0", bool((r["serie"]["SSI"] == 0.0).all()),
      str(r["serie"]["SSI"].unique()[:5]))
check("costante: tutti calmi", bool((r["serie"]["Classe"] == "🟢 Calmo").all()))
check("costante: medio 0", r["medio"] == 0.0, r["medio"])
check("costante: sopra soglia 0", r["sopra_soglia"] == 0)
check("costante: n_giorni 60", r["n_giorni"] == 60, r["n_giorni"])
check("costante: mensile 3 righe", len(r["mensile"]) == 3, len(r["mensile"]))

# --- 2. Giorno spike: livello+range+shock alti -> max SSI, crisi ---
medie = [50.0] * 30
ore = [None] * 30
ore[14] = np.concatenate([np.full(12, 100.0), np.full(12, 300.0)])
s = serie_giorni("2026-03-01", medie, ore_per_giorno=ore)
r = fs(s)
check("spike: no errore", r["errore"] is None, r["errore"])
imax = int(r["serie"]["SSI"].to_numpy().argmax())
check("spike: max SSI il giorno 14", r["serie"]["Data"].iloc[imax].strftime("%Y-%m-%d") == "2026-03-15",
      str(r["serie"]["Data"].iloc[imax]))
check("spike: SSI max >= 70", r["massimo"]["valore"] >= 70.0, r["massimo"])
check("spike: classe crisi", r["massimo"]["valore"] >= 70.0 and
      r["serie"]["Classe"].iloc[imax] == "🔴 Crisi", r["serie"]["Classe"].iloc[imax])
check("spike: somma componenti = SSI",
      abs(r["serie"].iloc[imax][["Livello prezzo (pt)", "Range intraday (pt)",
                                 "Shock giornaliero (pt)", "Ore negative (pt)"]].sum()
          - r["serie"]["SSI"].iloc[imax]) < 0.15)
check("spike: livello prezzo 35pt", abs(r["serie"]["Livello prezzo (pt)"].iloc[imax] - 35.0) < 0.01,
      r["serie"]["Livello prezzo (pt)"].iloc[imax])
check("spike: tabella ordinata desc",
      bool((r["tabella"]["SSI"].diff().dropna() <= 0).all()))
check("spike: sopra soglia 70 >= 1", r["sopra_soglia"] >= 1, r["sopra_soglia"])
check("spike: verdetto non vuoto", isinstance(r["verdetto"], str) and len(r["verdetto"]) > 10)

# --- 3. Ore negative: componente negativa > 0 nei giorni negativi ---
medie = [-5.0] * 10 + [50.0] * 20
s = serie_giorni("2026-05-01", medie)
r = fs(s)
check("neg: no errore", r["errore"] is None, r["errore"])
neg_pts = r["serie"]["Ore negative (pt)"].to_numpy()
check("neg: giorni negativi hanno punti > 0", bool((neg_pts[:10] > 0).all()), neg_pts[:3])
check("neg: giorni normali hanno punti 0", bool((neg_pts[10:] == 0).all()), neg_pts[10:13])
check("neg: SSI giorni negativi = 15.0 (solo componente ore negative)",
      np.allclose(r["serie"]["SSI"].to_numpy()[:10], 15.0, atol=0.05),
      str(r["serie"]["SSI"].to_numpy()[:3]))

# --- 4. Pesi custom (1,0,0,0): solo livello prezzo ---
medie = [10.0, 20.0, 30.0, 40.0, 50.0]
s = serie_giorni("2026-07-01", medie)
r = fs(s, pesi=(1, 0, 0, 0))
check("pesi: no errore", r["errore"] is None, r["errore"])
attesi = [0.0, 25.0, 50.0, 75.0, 100.0]
check("pesi: SSI = 100*livello normalizzato",
      np.allclose(r["serie"]["SSI"].to_numpy(), attesi, atol=0.05),
      str(r["serie"]["SSI"].to_numpy()))
check("pesi: pesi normalizzati", r["pesi"] == (1.0, 0.0, 0.0, 0.0), r["pesi"])
check("pesi: classi corrette",
      list(r["serie"]["Classe"]) == ["🟢 Calmo", "🟢 Calmo", "🟠 Stressato",
                                     "🔴 Crisi", "🔴 Crisi"],
      str(list(r["serie"]["Classe"])))

# --- 5. Errori di input ---
check("err: non-series", fs([1, 2, 3])["errore"] is not None)
check("err: indice non datetime",
      fs(pd.Series([1.0] * 100, index=range(100)))["errore"] is not None)
check("err: serie corta",
      fs(serie_giorni("2026-01-01", [50.0] * 2))["errore"] is not None)
check("err: soglia > 100",
      fs(serie_giorni("2026-01-01", [50.0] * 10), soglia=150)["errore"] is not None)
check("err: soglia < 0",
      fs(serie_giorni("2026-01-01", [50.0] * 10), soglia=-1)["errore"] is not None)
check("err: pesi lunghezza", fs(serie_giorni("2026-01-01", [50.0] * 10),
                                pesi=(1, 1))["errore"] is not None)
check("err: pesi somma 0", fs(serie_giorni("2026-01-01", [50.0] * 10),
                              pesi=(0, 0, 0, 0))["errore"] is not None)
check("err: pesi negativi", fs(serie_giorni("2026-01-01", [50.0] * 10),
                               pesi=(1, -1, 0, 0))["errore"] is not None)
check("err: pesi non numerici", fs(serie_giorni("2026-01-01", [50.0] * 10),
                                   pesi="x")["errore"] is not None)

# --- 6. tz-aware = naive ---
s_naive = serie_giorni("2026-01-05", [40.0, 60.0, 55.0, 70.0, 45.0])
s_tz = serie_giorni("2026-01-05", [40.0, 60.0, 55.0, 70.0, 45.0], tz="Europe/Zurich")
r_n, r_t = fs(s_naive), fs(s_tz)
check("tz: no errore", r_t["errore"] is None, r_t["errore"])
check("tz: SSI identici",
      np.allclose(r_n["serie"]["SSI"].to_numpy(), r_t["serie"]["SSI"].to_numpy()),
      f"{r_n['serie']['SSI'].to_numpy()} vs {r_t['serie']['SSI'].to_numpy()}")

# --- 7. NaN: nessun crash, giorni corretti ---
s = serie_giorni("2026-02-01", [50.0] * 10)
s.iloc[5:30] = np.nan
r = fs(s)
check("nan: no errore", r["errore"] is None, r["errore"])
check("nan: n_giorni 10", r["n_giorni"] == 10, r["n_giorni"])

# --- 8. Mensile e soglia custom ---
s = serie_giorni("2026-01-01", [50.0] * 90)
r = fs(s, soglia=50.0)
check("soglia50: costante -> 0 sopra soglia", r["sopra_soglia"] == 0)
check("mensile: mesi gen/feb/mar",
      list(r["mensile"]["Mese"]) == ["2026-01", "2026-02", "2026-03"],
      str(list(r["mensile"]["Mese"])))
check("mensile: SSI medio 0", bool((r["mensile"]["SSI medio"] == 0.0).all()))

print(f"checks={checks} fails={len(fails)}")
for f in fails:
    print("FAIL:", f)
raise SystemExit(1 if fails else 0)
