"""Standalone test for calcola_impronta_co2 - tab157 (no streamlit)."""
import ast
import re
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in (
            "calcola_impronta_co2", "_fascia_aeegsi"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola_impronta_co2 = ns["calcola_impronta_co2"]

fails = []
_nchecks = [0]


def check(name, cond):
    _nchecks[0] += 1
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def ore_hours(start, hours, price=50.0, tz=None):
    idx = pd.date_range(start, periods=hours, freq="h", tz=tz)
    return pd.Series(np.full(hours, price), index=idx)


def approx(a, b, tol=1e-6):
    return abs(float(a) - float(b)) <= tol


# ---------- caso base: 2 mesi, prezzo piatto 50, MW=1/1/1, fattore=1000, eua=100 ----------
# gen 2025: 744h -> 744 MWh, tco2=744, costo 37200, co2 74400, quota 200%
# feb 2025: 672h -> 672 MWh, tco2=672, costo 33600, co2 67200, quota 200%
p2 = ore_hours("2025-01-01", 744 + 672)
r = calcola_impronta_co2(p2, 1.0, 1.0, 1.0, fattore_kg_mwh=1000.0, eua_eur_t=100.0)
check("base valido", r["valido"] and r["errore"] is None)
check("base n_mesi=2", r["n_mesi"] == 2)
check("base mesi", r["mesi"] == ["2025-01", "2025-02"])
check("base energia", approx(r["energia_mwh"][0], 744.0) and approx(r["energia_mwh"][1], 672.0))
check("base costo energia", approx(r["costo_energia_eur"][0], 37200.0) and
      approx(r["costo_energia_eur"][1], 33600.0))
check("base tco2", approx(r["tco2"][0], 744.0) and approx(r["tco2"][1], 672.0))
check("base costo co2", approx(r["costo_co2_eur"][0], 74400.0) and
      approx(r["costo_co2_eur"][1], 67200.0))
check("base quota 200%", approx(r["quota_co2_costo_pct"][0], 200.0) and
      approx(r["quota_co2_costo_pct"][1], 200.0))
check("base tot tco2", approx(r["tot_tco2"], 1416.0))
check("base tot energia", approx(r["tot_energia_mwh"], 1416.0))
check("base tot costo co2", approx(r["tot_costo_co2_eur"], 141600.0))
check("base quota media 200%", approx(r["quota_media_pct"], 200.0))
check("base mese_max", r["mese_max"] == "2025-01")
check("base somma fasce = totale",
      approx(sum(r["tco2_fascia"].values()), r["tot_tco2"]))
check("base tabella colonne", list(r["tabella"].columns) ==
      ["Mese", "Energia (MWh)", "Costo energia (EUR)", "tCO2",
       "Costo CO2 valorizzato (EUR)", "Quota CO2 su costo (%)"])
check("base tabella 2 righe", len(r["tabella"]) == 2)
check("base verdetto non vuoto", isinstance(r["verdetto"], str) and len(r["verdetto"]) > 40)

# ---------- fasce: 48h da lun 2025-01-06, MW 2/3/4, fattore 1000, eua 50 ----------
# lun-ven: F1 8-19 (11h), F2 7-8+19-23 (5h), F3 0-7+23-24 (8h); x2 giorni:
# F1=22h, F2=10h, F3=16h -> tco2 44/30/64, top F3
p48 = ore_hours("2025-01-06", 48, price=20.0)
r48 = calcola_impronta_co2(p48, 2.0, 3.0, 4.0, fattore_kg_mwh=1000.0, eua_eur_t=50.0)
check("fasce valido", r48["valido"])
check("fasce tco2 F1", approx(r48["tco2_fascia"]["F1"], 44.0))
check("fasce tco2 F2", approx(r48["tco2_fascia"]["F2"], 30.0))
check("fasce tco2 F3", approx(r48["tco2_fascia"]["F3"], 64.0))
check("fasce tot", approx(r48["tot_tco2"], 138.0))
check("fasce energia tot", approx(r48["tot_energia_mwh"], 138.0))
check("fasce top F3", r48["fascia_top"] == "F3")
check("fasce quota media", approx(r48["quota_media_pct"],
      (138.0 * 50.0) / (138.0 * 20.0) * 100.0))

# ---------- fattore 0 -> tco2 zero ma valido ----------
r0 = calcola_impronta_co2(p2, 1, 1, 1, fattore_kg_mwh=0.0, eua_eur_t=100.0)
check("fattore 0 valido", r0["valido"] and approx(r0["tot_tco2"], 0.0)
      and approx(r0["tot_costo_co2_eur"], 0.0) and approx(r0["quota_media_pct"], 0.0))

# ---------- prezzo negativo ammesso (spot puo' esserlo), quota NaN-safe ----------
pn = ore_hours("2025-01-01", 744, price=-10.0)
rn = calcola_impronta_co2(pn, 1, 1, 1, fattore_kg_mwh=1000.0, eua_eur_t=100.0)
check("prezzo negativo valido", rn["valido"] and approx(rn["tot_tco2"], 744.0))
check("prezzo negativo quota None", rn["quota_co2_costo_pct"][0] is None
      and rn["quota_media_pct"] is None)

# ---------- tz-aware reso naive, non errore ----------
ptz = ore_hours("2025-01-01", 744 + 672, tz="Europe/Zurich")
rtz = calcola_impronta_co2(ptz, 1, 1, 1, fattore_kg_mwh=1000.0, eua_eur_t=100.0)
check("tz-aware valido", rtz["valido"])
check("tz-aware stessi totali", approx(rtz["tot_tco2"], r["tot_tco2"]))

# ---------- duplicati: keep first ----------
pdu = pd.concat([p2, p2.iloc[[0]]])
rdu = calcola_impronta_co2(pdu, 1, 1, 1, fattore_kg_mwh=1000.0, eua_eur_t=100.0)
check("duplicati ok", rdu["valido"] and approx(rdu["tot_tco2"], 1416.0))

# ---------- NaN prezzi scartati ----------
pnan = p2.copy()
pnan.iloc[::100] = np.nan
rnan = calcola_impronta_co2(pnan, 1, 1, 1, fattore_kg_mwh=1000.0, eua_eur_t=100.0)
check("NaN scartati", rnan["valido"] and
      approx(rnan["tot_energia_mwh"], 1416.0 - len(pnan.iloc[::100])))

# ---------- casi di errore ----------
e1 = calcola_impronta_co2(pd.Series([], dtype=float), 1, 1, 1)
check("err prezzi vuoti", not e1["valido"])
e2 = calcola_impronta_co2(pd.Series([1.0, 2.0], index=[0, 1]), 1, 1, 1)
check("err indice non datetime", not e2["valido"])
e3 = calcola_impronta_co2(p2, 0, 0, 0)
check("err MW nulli", not e3["valido"])
e4 = calcola_impronta_co2(p2, -1, 1, 1)
check("err MW negativi", not e4["valido"])
e5 = calcola_impronta_co2(p2, 1, 1, 1, fattore_kg_mwh=-5.0)
check("err fattore negativo", not e5["valido"])
e6 = calcola_impronta_co2(p2, 1, 1, 1, eua_eur_t=-1.0)
check("err eua negativo", not e6["valido"])
e7 = calcola_impronta_co2(p2, "x", 1, 1)
check("err MW non numerici", not e7["valido"])
e8 = calcola_impronta_co2("non una serie", 1, 1, 1)
check("err serie non numerica", not e8["valido"])
e9 = calcola_impronta_co2(p2, 1, 1, 1, fattore_kg_mwh="abc")
check("err fattore non numerico", not e9["valido"])

# ---------- determinismo ----------
ra = calcola_impronta_co2(p2, 1, 2, 3, fattore_kg_mwh=380.0, eua_eur_t=75.0)
rb = calcola_impronta_co2(p2, 1, 2, 3, fattore_kg_mwh=380.0, eua_eur_t=75.0)
check("deterministico", ra["verdetto"] == rb["verdetto"] and
      np.array_equal(np.array(ra["tco2"]), np.array(rb["tco2"])))

# ---------- registry tab157 ----------
n_with = len(re.findall(r"^\s*with tab157:", src, re.M))
check("un solo with tab157", n_with == 1)
m_decl = re.search(r"= st\.tabs\(\[\s*\"⏱️ Profilo giornaliero\"", src)
check("st.tabs trovata", m_decl is not None)
if m_decl is not None:
    lstart = src.rfind("\n", 0, m_decl.start()) + 1
    lend = src.find("\n", m_decl.end())
    decl = src[lstart:lend]
    lhs = re.findall(r"tab\d+", decl.split("= st.tabs", 1)[0])
    check("157 variabili dichiarate", len(lhs) == 157 and "tab157" in lhs)
    titles = re.findall(r'"([^"]+)"', decl.split("st.tabs([", 1)[1])
    check("157 titoli", len(titles) == 157)
    check("titolo tab157", "🌍 Impronta CO₂" in titles)
    check("titolo unico", titles.count("🌍 Impronta CO₂") == 1)
else:
    check("157 variabili dichiarate", False)
    check("157 titoli", False)
    check("titolo tab157", False)
    check("titolo unico", False)
check("tab157 usata (decl+with)", len(re.findall(r"\btab157\b", src)) == 2)
keys = re.findall(r'key="(co2157_[^"]+)"', src)
check("chiavi widget uniche", len(keys) == len(set(keys)) and len(keys) >= 6)
check("helper a livello modulo",
      "calcola_impronta_co2" in [n.name for n in tree.body if isinstance(n, ast.FunctionDef)])
check("nessun segreto hardcoded",
      not re.search(r'(?i)(api[_-]?key|password)\s*=\s*["\'][^"\']{8,}["\']', src))

print(f"\nchecks: {_nchecks[0]}, fails: {len(fails)}")
print("TUTTI I CHECK VERDI" if not fails else "FALLIMENTI: " + str(fails))
raise SystemExit(1 if fails else 0)
