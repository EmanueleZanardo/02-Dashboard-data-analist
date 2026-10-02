"""Standalone test for calcola_business_case_rinnovabile - tab159 (no streamlit)."""
import ast
import re
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_business_case_rinnovabile":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola = ns["calcola_business_case_rinnovabile"]

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


def shape_ref(tec, m, hh):
    m = np.asarray(m, dtype=float)
    hh = np.asarray(hh, dtype=float)
    if tec == "fv":
        dl = 12.0 + 3.6 * np.sin(2.0 * np.pi * (m - 3.5) / 12.0)
        sr = 12.0 - dl / 2.0
        x = (hh + 0.5 - sr) / dl
        dentro = (x > 0.0) & (x < 1.0)
        bell = np.where(dentro, np.sin(np.pi * np.clip(x, 0.0, 1.0)), 0.0)
        irr = 0.60 + 0.40 * np.sin(2.0 * np.pi * (m - 4.5) / 12.0)
        return bell * irr
    w = 1.0 + 0.28 * np.cos(2.0 * np.pi * (m - 1.0) / 12.0)
    return w * (1.0 + 0.10 * np.sin(2.0 * np.pi * (hh - 14.0) / 24.0))


P168 = [100.0] * 168  # settimana piatta a 100 EUR/MWh

# --- 1. numeri a mano: FV, 1 MW, 876 h eq, prezzi piatti ---
r = calcola(hours(P168), tecnologia="fv", potenza_mw=1.0, ore_equivalenti=876.0,
            degrado_pct=0.0, capex_eur_kw=100.0, opex_eur_kw_anno=0.0,
            tasso_pct=0.0, vita_anni=2)
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_ore == 168", r["n_ore"] == 168)
check("mano: energia_annua == 876 MWh", abs(r["energia_annua_mwh"] - 876.0) < 1e-6)
check("mano: ricavo_annuo == 87600 EUR",
      abs(r["ricavo_annuo_eur"] - 87600.0) < 1e-6)
check("mano: prezzo_catturato == 100", abs(r["prezzo_catturato"] - 100.0) < 1e-9)
check("mano: prezzo_medio == 100", abs(r["prezzo_medio"] - 100.0) < 1e-9)
check("mano: sconto == 0 %", abs(r["sconto_cattura_pct"] - 0.0) < 1e-9)
check("mano: capex == 100000 EUR", abs(r["capex_eur"] - 100000.0) < 1e-6)
check("mano: npv == 75200 EUR", abs(r["npv_eur"] - 75200.0) < 1e-6)
check("mano: payback == 1.14 anni",
      r["payback_anni"] is not None and abs(r["payback_anni"] - 1.14) < 1e-9)
check("mano: payback att == payback (tasso 0)",
      r["payback_att_anni"] == r["payback_anni"])
# IRR a mano: -100000 + 87600/(1+r) + 87600/(1+r)^2 = 0  ->  x=1/(1+r)
_disc = 87600.0 ** 2 + 4.0 * 87600.0 * 100000.0
_x = (-87600.0 + np.sqrt(_disc)) / (2.0 * 87600.0)
_irr_att = 1.0 / _x - 1.0
check("mano: IRR ~= 47.1 %", r["irr"] is not None and abs(r["irr"] - _irr_att) < 1e-3)
check("mano: IRR > tasso", r["irr"] is not None and r["irr"] > 0.0)
tab = r["tabella"]
check("mano: tabella 2 righe", len(tab) == 2 and list(tab["Anno"]) == [1, 2])
check("mano: cumulato att. anno2 == 75.2 kEUR",
      abs(tab["Cumulato att. (kEUR)"].iloc[1] - 75.2) < 1e-9)
sc = r["sens_capex"]
check("mano: sens_capex 5 righe", len(sc) == 5)
check("mano: sens_capex base == 75.2 kEUR",
      abs(sc.loc[sc["Variazione CAPEX"] == "base", "NPV (kEUR)"].iloc[0] - 75.2) < 1e-9)
check("mano: sens_capex decrescente",
      list(sc["NPV (kEUR)"]) == sorted(sc["NPV (kEUR)"], reverse=True))
sp = r["sens_prezzo"]
check("mano: sens_prezzo base == 75.2 kEUR",
      abs(sp.loc[sp["Variazione prezzo"] == "base", "NPV (kEUR)"].iloc[0] - 75.2) < 1e-9)
check("mano: sens_prezzo -20% < base",
      sp.loc[sp["Variazione prezzo"] == "-20%", "NPV (kEUR)"].iloc[0] < 75.2)
check("mano: verdetto NPV positivo", "NPV POSITIVO" in r["verdetto"])

# --- 2. profilo FV: notte a zero, giorno > 0 (gennaio) ---
idx = pd.date_range("2025-01-06", periods=168, freq="h")
m_a = idx.month.to_numpy()
h_a = idx.hour.to_numpy()
prof = shape_ref("fv", m_a, h_a)
check("FV: ore 0-4 sempre a zero", bool((prof[h_a <= 4] == 0.0).all()))
check("FV: ore 11-13 sempre > 0", bool((prof[(h_a >= 11) & (h_a <= 13)] > 0).all()))
prof_eo = shape_ref("eolico", m_a, h_a)
check("eolico: ore notturne > 0", bool((prof_eo[h_a <= 4] > 0).all()))
check("eolico: profilo invernale > estivo",
      shape_ref("eolico", [1], [12])[0] > shape_ref("eolico", [7], [12])[0])
check("FV: profilo estivo > invernale a mezzogiorno",
      shape_ref("fv", [7], [12])[0] > shape_ref("fv", [1], [12])[0])

# --- 3. eolico con prezzi piatti: stessa energia annua ---
re_ = calcola(hours(P168), tecnologia="eolico", potenza_mw=1.0,
              ore_equivalenti=876.0, degrado_pct=0.0, capex_eur_kw=100.0,
              opex_eur_kw_anno=0.0, tasso_pct=0.0, vita_anni=2)
check("eolico: valido", re_["valido"])
check("eolico: energia_annua == 876 MWh",
      abs(re_["energia_annua_mwh"] - 876.0) < 1e-6)
check("eolico: prezzo_catturato == 100", abs(re_["prezzo_catturato"] - 100.0) < 1e-9)

# --- 4. prezzo catturato differenziato: giorno caro, notte a buon mercato ---
vals = [100.0] * 168
for i, ts in enumerate(idx):
    if 10 <= ts.hour <= 15:
        vals[i] = 150.0
rf = calcola(hours(vals), tecnologia="fv", potenza_mw=1.0, ore_equivalenti=876.0,
             degrado_pct=0.0, capex_eur_kw=100.0, opex_eur_kw_anno=0.0,
             tasso_pct=0.0, vita_anni=2)
rw = calcola(hours(vals), tecnologia="eolico", potenza_mw=1.0, ore_equivalenti=876.0,
             degrado_pct=0.0, capex_eur_kw=100.0, opex_eur_kw_anno=0.0,
             tasso_pct=0.0, vita_anni=2)
check("cattura: FV cattura piu' dell'eolico a giorno caro",
      rf["prezzo_catturato"] > rw["prezzo_catturato"])
check("cattura: FV sopra la media",
      rf["prezzo_catturato"] > rf["prezzo_medio"])
check("cattura: sconto FV negativo (premio)",
      rf["sconto_cattura_pct"] is not None and rf["sconto_cattura_pct"] < 0.0)

# --- 5. degrado ---
rd = calcola(hours(P168), tecnologia="fv", potenza_mw=1.0, ore_equivalenti=876.0,
             degrado_pct=10.0, capex_eur_kw=100.0, opex_eur_kw_anno=0.0,
             tasso_pct=0.0, vita_anni=3)
check("degrado: valido", rd["valido"])
e1 = rd["tabella"]["Energia (MWh)"].iloc[0]
e3 = rd["tabella"]["Energia (MWh)"].iloc[2]
check("degrado: anno3 == anno1 * 0.9^2", abs(e3 - e1 * 0.81) < 0.2)

# --- 6. casi di errore ---
def bad(**kw):
    base = dict(tecnologia="fv", potenza_mw=1.0, ore_equivalenti=876.0,
                degrado_pct=0.0, capex_eur_kw=100.0, opex_eur_kw_anno=0.0,
                tasso_pct=0.0, vita_anni=2)
    base.update(kw)
    rr = calcola(hours(P168), **base)
    return (not rr["valido"]) and rr["errore"] is not None

check("err: tecnologia ignota", bad(tecnologia="nucleare"))
check("err: potenza 0", bad(potenza_mw=0.0))
check("err: potenza negativa", bad(potenza_mw=-5.0))
check("err: ore_eq 0", bad(ore_equivalenti=0.0))
check("err: ore_eq > 8760", bad(ore_equivalenti=9000.0))
check("err: degrado negativo", bad(degrado_pct=-1.0))
check("err: degrado > 20", bad(degrado_pct=25.0))
check("err: capex negativo", bad(capex_eur_kw=-1.0))
check("err: opex negativo", bad(opex_eur_kw_anno=-1.0))
check("err: tasso negativo", bad(tasso_pct=-1.0))
check("err: tasso > 100", bad(tasso_pct=101.0))
check("err: vita 0", bad(vita_anni=0))
check("err: vita 51", bad(vita_anni=51))
check("err: vita non intera", bad(vita_anni=2.5))
check("err: prezzi vuoti",
      not calcola(pd.Series([], dtype=float), vita_anni=2)["valido"])
check("err: indice non datetime",
      not calcola(pd.Series([1.0, 2.0, 3.0] * 60), vita_anni=2)["valido"])
check("err: < 168 ore",
      not calcola(hours([100.0] * 100), vita_anni=2)["valido"])
check("err: prezzi non numerici",
      not calcola(pd.Series(["x"] * 168,
                            index=pd.date_range("2025-01-06", periods=168, freq="h")),
                 vita_anni=2)["valido"])
check("err: param non numerico",
      not calcola(hours(P168), potenza_mw="dieci", vita_anni=2)["valido"])

# --- 7. NaN, tz, duplicati ---
pn = hours([100.0] * 169)
pn.iloc[5] = np.nan
rn_ = calcola(pn, vita_anni=2)
check("NaN: scartato (168 ore)", rn_["valido"] and rn_["n_ore"] == 168)
rz = calcola(hours(P168, tz="Europe/Zurich"), vita_anni=2)
check("tz-aware: valido", rz["valido"] and rz["n_ore"] == 168)
pdup = pd.concat([hours(P168), hours(P168)])
rdu = calcola(pdup, vita_anni=2)
check("duplicati: keep-first (168 ore)", rdu["valido"] and rdu["n_ore"] == 168)

# --- 8. determinismo ---
ra = calcola(hours(P168), vita_anni=2)
rb = calcola(hours(P168), vita_anni=2)
check("determinismo: npv identico", ra["npv_eur"] == rb["npv_eur"])
check("determinismo: verdetto identico", ra["verdetto"] == rb["verdetto"])
check("determinismo: tabella identica", ra["tabella"].equals(rb["tabella"]))

# --- 9. NPV negativo e payback mai ---
rneg = calcola(hours([10.0] * 168), tecnologia="fv", potenza_mw=1.0,
               ore_equivalenti=876.0, degrado_pct=0.0, capex_eur_kw=100.0,
               opex_eur_kw_anno=0.0, tasso_pct=0.0, vita_anni=2)
check("negativo: npv < 0", rneg["valido"] and rneg["npv_eur"] < 0)
check("negativo: payback None", rneg["payback_anni"] is None)
check("negativo: verdetto NPV NEGATIVO", "NPV NEGATIVO" in rneg["verdetto"])

# --- 10. registry tab159 ---
n_with = len(re.findall(r"^\s*with tab159:", src, re.M))
check("un solo with tab159", n_with == 1)
m_decl = re.search(r"= st\.tabs\(\[\s*\"⏱️ Profilo giornaliero\"", src)
check("st.tabs trovata", m_decl is not None)
if m_decl is not None:
    lstart = src.rfind("\n", 0, m_decl.start()) + 1
    lend = src.find("\n", m_decl.end())
    decl = src[lstart:lend]
    lhs = re.findall(r"tab\d+", decl.split("= st.tabs", 1)[0])
    titles = re.findall(r'"([^"]+)"', decl.split("st.tabs([", 1)[1])
    check("tab159 tra le variabili", "tab159" in lhs)
    check("n titoli == n variabili", len(titles) == len(lhs))
    check("almeno 159 tab", len(titles) >= 159)
    check("titolo tab159", "☀️ Business case rinnovabile" in titles)
    check("titolo unico", titles.count("☀️ Business case rinnovabile") == 1)
    check("nomi unici", len(lhs) == len(set(lhs)) and len(titles) == len(set(titles)))
else:
    check("tab159 tra le variabili", False)
    check("n titoli == n variabili", False)
    check("almeno 159 tab", False)
    check("titolo tab159", False)
    check("titolo unico", False)
    check("nomi unici", False)
check("tab159 usata (decl+with)", len(re.findall(r"\btab159\b", src)) == 2)
keys = re.findall(r'key="(bcr159_[^"]+)"', src)
check("chiavi widget uniche", len(keys) == len(set(keys)) and len(keys) >= 3)
check("chiavi widget >= 9", len(keys) >= 9)
check("helper a livello modulo",
      "calcola_business_case_rinnovabile" in [n.name for n in tree.body
                                              if isinstance(n, ast.FunctionDef)])
check("helper chiamato nella UI",
      src.count("calcola_business_case_rinnovabile(") >= 2)
check("nessun segreto hardcoded",
      not re.search(r'(?i)(api[_-]?key|password)\s*=\s*["\'][^"\']{8,}["\']', src))

print(f"\nchecks: {_nchecks[0]}, fails: {len(fails)}")
print("TUTTI I CHECK VERDI" if not fails else "FALLIMENTI: " + str(fails))
raise SystemExit(1 if fails else 0)
