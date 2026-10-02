"""Standalone test for calcola_idrogeno_verde - tab160 (no streamlit)."""
import ast
import re
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_idrogeno_verde":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola = ns["calcola_idrogeno_verde"]

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


# --- 1. numeri a mano: 1 settimana piatta a 100 EUR/MWh, 1 MW ---
# eff 66.66% -> kg_per_mwh = 1000*0.6666/33.33 = 20.000200002
r = calcola(hours([100.0] * 168), potenza_mw=1.0, capex_eur_kw=1500.0,
            opex_eur_kw_anno=40.0, efficienza_pct=66.66,
            prezzo_h2_eur_kg=6.0, tasso_pct=6.0, vita_anni=20)
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_ore == 168", r["n_ore"] == 168)
exp_kg_mwh = 1000.0 * 0.6666 / 33.33
check("mano: kg_per_mwh", abs(r["kg_per_mwh"] - exp_kg_mwh) < 1e-12)
exp_be = 6.0 * exp_kg_mwh
check("mano: prezzo_be", abs(r["prezzo_be_mwh"] - exp_be) < 1e-12)
# candidati linspace(0, p_be, 61): passo ~2.0; il primo con margine max e' 102
check("mano: soglia ottima == 102.0", abs(r["soglia_ottima_mwh"] - 102.0) < 1e-9)
check("mano: ore_annue == 8760", abs(r["ore_annue"] - 8760.0) < 1e-9)
check("mano: fattore_carico == 100", abs(r["fattore_carico_pct"] - 100.0) < 1e-12)
exp_ml_oss = 168.0 * (exp_be - 100.0)
check("mano: margine lordo oss", abs(r["margine_lordo_annuo_eur"] - exp_ml_oss * 8760.0 / 168.0) < 1e-6)
exp_cel = 168.0 * 100.0 * 8760.0 / 168.0
check("mano: costo elettricita' annuo", abs(r["costo_elettricita_annuo_eur"] - exp_cel) < 1e-6)
check("mano: margine netto", abs(r["margine_netto_annuo_eur"] - (r["margine_lordo_annuo_eur"] - 40000.0)) < 1e-6)
exp_kg = 8760.0 * exp_kg_mwh
check("mano: kg_annui", abs(r["kg_annui"] - exp_kg) < 1e-6)
check("mano: ricavo == kg * 6", abs(r["ricavo_annuo_eur"] - exp_kg * 6.0) < 1e-6)
check("mano: capex == 1.5M", abs(r["capex_eur"] - 1500000.0) < 1e-6)
check("mano: opex == 40000", abs(r["opex_annuo_eur"] - 40000.0) < 1e-6)
# NPV: flussi = margine netto costante, fattore att (1-1.06^-20)/0.06
_fatt = (1.0 - 1.06 ** -20) / 0.06
check("mano: npv", abs(r["npv_eur"] - (r["margine_netto_annuo_eur"] * _fatt - 1500000.0)) < 1e-3)
check("mano: payback = capex/margine", abs(r["payback_anni"] - 1500000.0 / r["margine_netto_annuo_eur"]) < 1e-9)
_crf = 0.06 * 1.06 ** 20 / (1.06 ** 20 - 1.0)
exp_lcoh = (_crf * 1500000.0 + 40000.0 + exp_cel) / exp_kg
check("mano: LCOH", abs(r["lcoh_eur_kg"] - exp_lcoh) < 1e-9)
check("mano: verdetto CONVIENE", "CONVIENE" in r["verdetto"])
check("mano: tabella soglie 61 righe", len(r["tabella_soglie"]) == 61)
tab = r["tabella_soglie"]
check("mano: ultima riga = margine max", tab["Margine lordo (kEUR/anno)"].iloc[-1] == tab["Margine lordo (kEUR/anno)"].max())

# --- 2. soglia ottimale su prezzi a due livelli ---
# 168h a 50 + 168h a 150: conviene accendere solo le ore a 50
p2 = hours([50.0] * 168 + [150.0] * 168)
r2 = calcola(p2, potenza_mw=2.0, capex_eur_kw=1500.0,
             opex_eur_kw_anno=40.0, efficienza_pct=66.66,
             prezzo_h2_eur_kg=6.0, tasso_pct=6.0, vita_anni=20)
check("2liv: valido", r2["valido"])
step = exp_be / 60.0
exp_thr = np.ceil(50.0 / step + 1e-12) * step
check("2liv: soglia ottima ~ primo candidato > 50", abs(r2["soglia_ottima_mwh"] - exp_thr) < 1e-9)
check("2liv: ore_annue == 4380", abs(r2["ore_annue"] - 4380.0) < 1e-6)
check("2liv: costo el solo ore care escluse",
      abs(r2["costo_elettricita_annuo_eur"] - 4380.0 * 50.0 * 2.0) < 1e-3)
exp_kg2 = 4380.0 * 2.0 * exp_kg_mwh
check("2liv: kg_annui", abs(r2["kg_annui"] - exp_kg2) < 1e-3)
check("2liv: fattore carico 50%", abs(r2["fattore_carico_pct"] - 50.0) < 1e-9)
# verifica indipendente: margine della soglia scelta == max su tutti i 61
ml_tutti = []
for thr in np.linspace(0.0, exp_be, 61):
    m = (p2.to_numpy() < thr) * (exp_be - p2.to_numpy())
    ml_tutti.append(m.sum() * 2.0 * 8760.0 / 336.0)
check("2liv: margine alla soglia == max", abs(r2["margine_lordo_annuo_eur"] - max(ml_tutti)) < 1e-6)
# running always sarebbe peggio
ml_sempre = ml_tutti[-1]
check("2liv: soglia ottimale batte ultimo candidato", r2["margine_lordo_annuo_eur"] >= ml_sempre - 1e-9)
# "sempre acceso" manuale (anche le ore a 150, sopra break-even): distrugge margine
ml_all_ore = (168.0 * (exp_be - 50.0) + 168.0 * (exp_be - 150.0)) * 2.0 * 8760.0 / 336.0
check("2liv: accendere anche le ore a 150 distrugge margine",
      ml_all_ore < r2["margine_lordo_annuo_eur"] - 1e3)

# --- 3. spot sempre sopra break-even: mai acceso ---
r3 = calcola(hours([200.0] * 168), potenza_mw=1.0, efficienza_pct=66.66,
             prezzo_h2_eur_kg=6.0, capex_eur_kw=1500.0, opex_eur_kw_anno=40.0,
             tasso_pct=6.0, vita_anni=20)
check("sopra-BE: valido", r3["valido"])
check("sopra-BE: ore_annue == 0", r3["ore_annue"] == 0.0)
check("sopra-BE: lcoh None", r3["lcoh_eur_kg"] is None)
check("sopra-BE: margine netto == -opex", abs(r3["margine_netto_annuo_eur"] + 40000.0) < 1e-9)
check("sopra-BE: payback None", r3["payback_anni"] is None)
check("sopra-BE: verdetto NON CONVIENE", "NON CONVIENE" in r3["verdetto"])

# --- 4. prezzi negativi: costo elettricita' negativo, tutto acceso ---
r4 = calcola(hours([-20.0] * 168), potenza_mw=1.0, efficienza_pct=66.66,
             prezzo_h2_eur_kg=6.0, capex_eur_kw=1500.0, opex_eur_kw_anno=40.0,
             tasso_pct=6.0, vita_anni=20)
check("neg: valido", r4["valido"])
check("neg: ore 8760", abs(r4["ore_annue"] - 8760.0) < 1e-9)
check("neg: costo el negativo", r4["costo_elettricita_annuo_eur"] < 0)
check("neg: LCOH < prezzo vendita", r4["lcoh_eur_kg"] is not None and r4["lcoh_eur_kg"] < 6.0)

# --- 5. casi di errore ---
for nome, kw in [
    ("potenza 0", dict(potenza_mw=0.0)),
    ("potenza negativa", dict(potenza_mw=-1.0)),
    ("capex negativo", dict(capex_eur_kw=-1.0)),
    ("opex negativo", dict(opex_eur_kw_anno=-1.0)),
    ("efficienza 0", dict(efficienza_pct=0.0)),
    ("efficienza > 100", dict(efficienza_pct=101.0)),
    ("prezzo h2 0", dict(prezzo_h2_eur_kg=0.0)),
    ("prezzo h2 negativo", dict(prezzo_h2_eur_kg=-2.0)),
    ("tasso negativo", dict(tasso_pct=-1.0)),
    ("vita 0", dict(vita_anni=0)),
    ("potenza non numerica", dict(potenza_mw="x")),
]:
    rr = calcola(hours([100.0] * 168), **kw)
    check("errore: " + nome, not rr["valido"] and isinstance(rr["errore"], str))
check("errore: serie vuota", not calcola(pd.Series([], dtype=float))["valido"])
check("errore: serie None", not calcola(None)["valido"])
_rr_ndt = calcola(pd.Series([1.0] * 48, index=range(48)))
check("errore: indice non datetime (valido=False)", not _rr_ndt["valido"])
check("errore: serie < 24h", not calcola(hours([100.0] * 10))["valido"])

# --- 6. NaN, tz-aware, duplicati, determinismo ---
p_nan = hours([100.0] * 100 + [np.nan] * 68)
rn = calcola(p_nan, potenza_mw=1.0, efficienza_pct=66.66, prezzo_h2_eur_kg=6.0)
check("NaN: valido dopo pulizia", rn["valido"] and rn["n_ore"] == 100)
r_tz = calcola(hours([100.0] * 168, tz="Europe/Zurich"), potenza_mw=1.0,
               efficienza_pct=66.66, prezzo_h2_eur_kg=6.0)
check("tz: valido", r_tz["valido"])
check("tz: stessi numeri", abs(r_tz["npv_eur"] - r["npv_eur"]) < 1e-6)
idx = pd.date_range("2025-01-06", periods=168, freq="h")
dup = pd.concat([pd.Series([100.0] * 168, index=idx), pd.Series([100.0] * 168, index=idx)])
rd = calcola(dup, potenza_mw=1.0, efficienza_pct=66.66, prezzo_h2_eur_kg=6.0)
check("duplicati: n_ore == 168", rd["valido"] and rd["n_ore"] == 168)
ra = calcola(hours([100.0] * 168), potenza_mw=1.0, efficienza_pct=66.66, prezzo_h2_eur_kg=6.0)
rb = calcola(hours([100.0] * 168), potenza_mw=1.0, efficienza_pct=66.66, prezzo_h2_eur_kg=6.0)
check("determinismo: verdetto identico", ra["verdetto"] == rb["verdetto"])
check("determinismo: tabella identica", ra["tabella_soglie"].equals(rb["tabella_soglie"]))
check("determinismo: soglia identica", ra["soglia_ottima_mwh"] == rb["soglia_ottima_mwh"])

# --- 7. tasso 0: NPV == margine*vita - capex ---
r0 = calcola(hours([100.0] * 168), potenza_mw=1.0, capex_eur_kw=1500.0,
             opex_eur_kw_anno=40.0, efficienza_pct=66.66, prezzo_h2_eur_kg=6.0,
             tasso_pct=0.0, vita_anni=20)
check("tasso0: npv lineare", abs(r0["npv_eur"] - (r0["margine_netto_annuo_eur"] * 20 - 1500000.0)) < 1e-3)

# --- 8. registry tab160 ---
n_with = len(re.findall(r"^\s*with tab160:", src, re.M))
check("un solo with tab160", n_with == 1)
m_decl = re.search(r"= st\.tabs\(\[\s*\"⏱️ Profilo giornaliero\"", src)
check("st.tabs trovata", m_decl is not None)
if m_decl is not None:
    lstart = src.rfind("\n", 0, m_decl.start()) + 1
    lend = src.find("\n", m_decl.end())
    decl = src[lstart:lend]
    lhs = re.findall(r"tab\d+", decl.split("= st.tabs", 1)[0])
    titles = re.findall(r'"([^"]+)"', decl.split("st.tabs([", 1)[1])
    check("160 variabili dichiarate", len(lhs) == 160 and "tab160" in lhs)
    check("160 titoli", len(titles) == 160)
    check("titolo tab160", "💧 Idrogeno verde" in titles)
    check("titolo unico", titles.count("💧 Idrogeno verde") == 1)
    check("nomi unici", len(lhs) == len(set(lhs)) and len(titles) == len(set(titles)))
else:
    check("160 variabili dichiarate", False)
    check("160 titoli", False)
    check("titolo tab160", False)
    check("titolo unico", False)
    check("nomi unici", False)
check("tab160 usata (decl+with)", len(re.findall(r"\btab160\b", src)) == 2)
keys = re.findall(r'key="(h2160_[^"]+)"', src)
check("chiavi widget uniche", len(keys) == len(set(keys)) and len(keys) >= 3)
check("chiavi widget >= 7", len(keys) >= 7)
check("helper a livello modulo",
      "calcola_idrogeno_verde" in [n.name for n in tree.body
                                   if isinstance(n, ast.FunctionDef)])
check("helper chiamato nella UI",
      "calcola_idrogeno_verde(" in src[src.find("with tab160:"):])
check("edu usato nel titolo", "edu(\"Idrogeno verde\"" in src)
check("download CSV presente", "h2160_csv" in src)
check("nessun with tabN a col 0",
      len(re.findall(r"^with tab\d+:", src, re.M)) == 0)

print("checks: %d, fails: %d" % (_nchecks[0], len(fails)))
raise SystemExit(1 if fails else 0)
