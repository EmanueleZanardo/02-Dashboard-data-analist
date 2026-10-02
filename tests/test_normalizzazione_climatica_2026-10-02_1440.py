"""Standalone test for calcola_normalizzazione_climatica - tab155 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_normalizzazione_climatica", "_fascia_aeegsi"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_normalizzazione_climatica = ns["calcola_normalizzazione_climatica"]

fails = []
_nchecks = [0]


def check(name, cond):
    _nchecks[0] += 1
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def hours(vals, start="2025-01-06", tz=None):
    idx = pd.date_range(start, periods=len(vals), freq="h", tz=tz)
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


def hand_case():
    # 10 giorni (lun-dom + lun-mer), temperature allineate ai weekday:
    # lun-ven T=10.5 (HDD=120, y=160), sab T=24 (CDD=48, y=148),
    # dom T=18 (0, y=100). MW scelti per y = 100 + 0.5*HDD + 1.0*CDD esatto.
    m1, m2, m3 = 2.18 / 11.0, 0.172, 0.1
    prezzi = hours([50.0] * 240)
    temp = hours([10.5] * 24 * 5 + [24.0] * 24 + [18.0] * 24 + [10.5] * 24 * 3)
    return prezzi, temp, m1, m2, m3


# --- 1. numeri a mano: y = 100 + 0.5*HDD + 1.0*CDD ---
prezzi, temp, m1, m2, m3 = hand_case()
r = calcola_normalizzazione_climatica(prezzi, m1, m2, m3, temperatura=temp, min_giorni=10)
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_giorni == 10", r["n_giorni"] == 10)
check("mano: base_kw == 100", abs(r["base_kw"] - 100.0) < 1e-6)
check("mano: kw_per_gg_risc == 0.5", abs(r["kw_per_gg_risc"] - 0.5) < 1e-9)
check("mano: kw_per_gg_raffr == 1.0", abs(r["kw_per_gg_raffr"] - 1.0) < 1e-9)
check("mano: r2 == 1.0", abs(r["r2"] - 1.0) < 1e-12)
check("mano: quote sommano a 100",
      abs(r["quota_risc_pct"] + r["quota_raffr_pct"] + r["quota_base_pct"] - 100.0) < 1e-9)
y_medio_att = (8 * 160.0 + 148.0 + 100.0) / 10.0  # 152.8
check("mano: quota_risc == 0.5*96/152.8*100",
      abs(r["quota_risc_pct"] - (0.5 * 96.0 / y_medio_att * 100.0)) < 1e-9)
check("mano: quota_raffr == 1.0*4.8/152.8*100",
      abs(r["quota_raffr_pct"] - (1.0 * 4.8 / y_medio_att * 100.0)) < 1e-9)
check("mano: energia normalizzata == energia reale (media preservata)",
      abs(r["energia_norm_mwh"] - r["energia_mwh"]) < 1e-9)
check("mano: energia_mwh == 146.8*24*10/1000",
      abs(r["energia_mwh"] - (y_medio_att * 24.0 * 10 / 1000.0)) < 1e-9)
check("mano: tabella 10 righe", len(r["tabella"]) == 10)
check("mano: tabella ha colonne attese",
      list(r["tabella"].columns) == ["Data", "Carico medio (kW)", "HDD", "CDD",
                                    "Carico normalizzato (kW)"])
check("mano: HDD giornalieri [120]*5+[0,0]+[120]*3",
      list(r["tabella"]["HDD"].to_numpy()) == [120.0] * 5 + [0.0, 0.0] + [120.0] * 3)
check("mano: CDD giornalieri [0]*5+[48,0]+[0]*3",
      list(r["tabella"]["CDD"].to_numpy()) == [0.0] * 5 + [48.0, 0.0] + [0.0] * 3)
check("mano: media y_norm == media y",
      abs(float(np.mean(r["y_norm"])) - float(np.mean(r["y"]))) < 1e-12)
check("mano: verdetto cita R² e driver base",
      "R² = 1.00" in r["verdetto"] and "base" in r["verdetto"])
check("mano: chiavi per la UI presenti",
      all(k in r for k in ("giorni", "y", "y_norm", "hdd", "cdd", "tabella", "verdetto")))

# --- 2. errori sui parametri ---
p_ok = hours([50.0] * 240)
t_ok = hours([[10.0, 26.0, 18.0][(i // 24) % 3] for i in range(240)])  # ciclo 10 / 26 / 18 (HDD, CDD e deadband)
e = calcola_normalizzazione_climatica(hours([]), 1, 1, 1, temperatura=t_ok)
check("err: prezzi vuoti", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 1, 1, 1, temperatura=None)
check("err: temperatura mancante", not e["valido"] and "mancante" in e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 1, 1, 1, temperatura=hours([]))
check("err: temperatura vuota", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(pd.Series([1.0, 2.0]), 1, 1, 1, temperatura=t_ok)
check("err: prezzi indice non datetime", not e["valido"] and e["errore"])
p_str = pd.Series(["a"] * 240,
                index=pd.date_range("2025-01-06", periods=240, freq="h"))
e = calcola_normalizzazione_climatica(p_str, 1, 1, 1, temperatura=t_ok)
check("err: prezzi non numerici", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 1, 1, 1, temperatura=t_ok,
                                      t_base_risc=22.0, t_base_raffr=15.5)
check("err: basi invertite", not e["valido"] and "base riscaldamento" in e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 1, 1, 1, temperatura=t_ok,
                                      t_base_risc=None, t_base_raffr=22.0)
check("err: base non valida", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 1, 1, 1, temperatura=t_ok, min_giorni=5)
check("err: min_giorni < 10", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(p_ok, -1, 1, 1, temperatura=t_ok)
check("err: mw negativo", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 0, 0, 0, temperatura=t_ok)
check("err: mw tutti zero", not e["valido"] and e["errore"])
e = calcola_normalizzazione_climatica(p_ok, 1, 1, 1, temperatura=t_ok, min_giorni=30)
check("err: serie troppo corta (10 < 30 giorni)", not e["valido"] and "troppo corta" in e["errore"])

# --- 3. temperatura senza variabilita' utile ---
p10 = hours([50.0] * 240)
t_flat = hours([18.0] * 240)  # sempre in deadband -> HDD=CDD=0
e = calcola_normalizzazione_climatica(p10, 1, 1, 1, temperatura=t_flat, min_giorni=10)
check("err: deadband costante -> non identificabile",
      not e["valido"] and "non identificabile" in e["errore"])
t_cold = hours([10.0] * 240)  # solo HDD, rango 2
e = calcola_normalizzazione_climatica(p10, 1, 1, 1, temperatura=t_cold, min_giorni=10)
check("err: solo HDD -> non identificabile",
      not e["valido"] and "non identificabile" in e["errore"])

# --- 4. caso valido piu' lungo + NaN + giorno scarso ---
p12 = hours([50.0] * 288, start="2025-01-06")
t12_vals = []
for d in range(12):
    t12_vals += [8.0 + d * 1.5] * 24  # 8..24.5 C: HDD>0 i primi giorni, CDD>0 gli ultimi
t12 = hours(t12_vals, start="2025-01-06")
r12 = calcola_normalizzazione_climatica(p12, 0.5, 0.4, 0.3, temperatura=t12, min_giorni=10)
check("12gg: valido", r12["valido"] and r12["errore"] is None)
check("12gg: n_giorni == 12", r12["n_giorni"] == 12)
check("12gg: r2 in [0,1]", 0.0 <= r12["r2"] <= 1.0)
check("12gg: b,c finiti", np.isfinite(r12["kw_per_gg_risc"]) and np.isfinite(r12["kw_per_gg_raffr"]))

t12n = t12.copy()
t12n.iloc[5 * 24:5 * 24 + 3] = np.nan  # 3 ore NaN nel giorno 6 -> giorno tenuto
rn = calcola_normalizzazione_climatica(p12, 0.5, 0.4, 0.3, temperatura=t12n, min_giorni=10)
check("NaN: 3 ore NaN non buttano il giorno", rn["valido"] and rn["n_giorni"] == 12)
t12b = t12.copy()
t12b.iloc[5 * 24:5 * 24 + 14] = np.nan  # 14 ore NaN -> giorno scartato (<20 ore)
rb = calcola_normalizzazione_climatica(p12, 0.5, 0.4, 0.3, temperatura=t12b, min_giorni=10)
check("NaN: giorno con <20 ore valide scartato", rb["valido"] and rb["n_giorni"] == 11)

# --- 5. tz-aware ---
p_tz = hours([50.0] * 240, tz="Europe/Zurich")
t_tz = hours([[10.0, 26.0, 18.0][(i // 24) % 3] for i in range(240)])
r_tz = calcola_normalizzazione_climatica(p_tz, 0.5, 0.4, 0.3, temperatura=t_tz, min_giorni=10)
check("tz: serie tz-aware gestita", r_tz["valido"] and r_tz["n_giorni"] == 10)

# --- 6. determinismo ---
ra = calcola_normalizzazione_climatica(prezzi, m1, m2, m3, temperatura=temp, min_giorni=10)
rb2 = calcola_normalizzazione_climatica(prezzi, m1, m2, m3, temperatura=temp, min_giorni=10)
check("determinismo: r2 identico", ra["r2"] == rb2["r2"])
check("determinismo: verdetto identico", ra["verdetto"] == rb2["verdetto"])
check("determinismo: tabella identica", ra["tabella"].equals(rb2["tabella"]))

# --- 7. registry tab155 ---
_decl = [l for l in src.splitlines() if "st.tabs(" in l and "tab1," in l]
check("registry: tab155 dichiarata",
      any("tab155" in l.split("= st.tabs(")[0] for l in _decl))
check("registry: titolo presente", '"🌡️ Normalizzazione climatica"' in src)
check("registry: with tab155 presente", "    with tab155:" in src)
check("registry: helper chiamato nella UI",
      "calcola_normalizzazione_climatica(prezzi, nc_mw1" in src)
check("registry: chiavi widget uniche",
      src.count('key="nc155_') == 6 and src.count('key="csv_normalizzazione_climatica"') == 1)
check("registry: helper a livello modulo",
      any(isinstance(n, ast.FunctionDef) and n.name == "calcola_normalizzazione_climatica"
          for n in tree.body))

print(f"\nchecks: {_nchecks[0] - len(fails)}, fails: {len(fails)}")
if fails:
    print(fails)
    raise SystemExit(1)
print("TUTTI I CHECK VERDI")
