"""Standalone test for calcola_rischio_volume - tab161 (no streamlit)."""
import ast
import re
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_rischio_volume":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
calcola = ns["calcola_rischio_volume"]

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


# --- 1. numeri a mano: 48h piatte a 100 EUR/MWh, base 10 MW piatto, quota 50%, fisso 90, var 10 ---
r = calcola(hours([100.0] * 48), carico_base_mw=10.0, forma_carico="piatto",
            quota_coperta_pct=50.0, prezzo_coperto_eur_mwh=90.0,
            variazione_carico_pct=10.0)
check("mano: valido e nessun errore", r["valido"] and r["errore"] is None)
check("mano: n_ore == 48", r["n_ore"] == 48)
check("mano: hedge_mw == 5.0", r["hedge_mw"] == 5.0)
check("mano: energia totale 480.0", abs(r["energia_totale_mwh"] - 480.0) < 1e-9)
check("mano: coperta 240.0", abs(r["energia_coperta_mwh"] - 240.0) < 1e-9)
check("mano: aperta 240.0", abs(r["energia_aperta_mwh"] - 240.0) < 1e-9)
check("mano: long 0.0", r["energia_long_mwh"] == 0.0)
check("mano: quota effettiva 50%", abs(r["quota_coperta_effettiva_pct"] - 50.0) < 1e-9)
check("mano: costo totale 456000", abs(r["costo_totale_eur"] - 45600.0) < 1e-6)
check("mano: costo spot 480000", abs(r["costo_spot_eur"] - 48000.0) < 1e-6)
check("mano: risparmio 24000", abs(r["risparmio_vs_spot_eur"] - 2400.0) < 1e-6)
check("mano: scenario -10% = 408000", r["tabella_scenari"]["Costo totale (EUR)"].iloc[0] == 40800.0)
check("mano: scenario base = 456000", r["tabella_scenari"]["Costo totale (EUR)"].iloc[1] == 45600.0)
check("mano: scenario +10% = 504000", r["tabella_scenari"]["Costo totale (EUR)"].iloc[2] == 50400.0)
check("mano: rischio 96000", abs(r["rischio_volume_eur"] - 9600.0) < 1e-6)
check("mano: rischio pct 21.0526%", abs(r["rischio_volume_pct"] - 9600.0 / 45600.0 * 100) < 1e-9)
check("mano: giudizio ALTO", r["giudizio"] == "ALTO" and "ALTO" in r["verdetto"])
check("mano: tabella 3 righe", len(r["tabella_scenari"]) == 3)
check("mano: nomi scenari", list(r["tabella_scenari"]["Scenario carico"]) == ["base -10 %", "base", "base +10 %"])

# --- 2. forma diurna: pesi normalizzati a media 1 ---
r2 = calcola(hours([100.0] * 48), carico_base_mw=8.0, forma_carico="diurno",
             quota_coperta_pct=100.0, prezzo_coperto_eur_mwh=90.0)
check("diurno: valido", r2["valido"])
# pesi grezzi: 14h x1.25 + 10h x0.625 = 23.75 -> media 0.9895833
check("diurno: energia = 8*48 (normalizzata)", abs(r2["energia_totale_mwh"] - 384.0) < 1e-9)
check("diurno: quota 100% -> long di notte > 0", r2["energia_long_mwh"] > 0)
check("diurno: quota 100% media -> picchi diurni aperti > 0", r2["energia_aperta_mwh"] > 0)
check("diurno: quota effettiva = coperta/384", abs(r2["quota_coperta_effettiva_pct"] - r2["energia_coperta_mwh"] / 384.0 * 100.0) < 1e-9)
# costo = coperta*90 - long*100
check("diurno: costo = 384*90 + aperta*10 - long*100",
      abs(r2["costo_totale_eur"] - (384.0 * 90.0 + r2["energia_aperta_mwh"] * 10.0 - r2["energia_long_mwh"] * 100.0)) < 1e-6)

# --- 3. quota 0%: tutto a spot, rischio max ---
r3 = calcola(hours([100.0] * 48), carico_base_mw=10.0, forma_carico="piatto",
             quota_coperta_pct=0.0, prezzo_coperto_eur_mwh=90.0)
check("quota0: costo == costo spot", abs(r3["costo_totale_eur"] - r3["costo_spot_eur"]) < 1e-9)
check("quota0: rischio = 20% del costo", abs(r3["rischio_volume_eur"] - 0.20 * 48000.0) < 1e-6)
check("quota0: risparmio 0", r3["risparmio_vs_spot_eur"] == 0.0)

# --- 4. prezzi a due livelli: diurno cattura di piu' a giorno caro ---
vals = [50.0] * 24 + [150.0] * 24  # giorno1 notte/giorno2...
s4 = hours(vals)
r4 = calcola(s4, carico_base_mw=10.0, forma_carico="piatto", quota_coperta_pct=50.0,
             prezzo_coperto_eur_mwh=80.0, variazione_carico_pct=10.0)
check("2liv: valido", r4["valido"])
# costo = 240*80 + 120*50 + 120*150 = 19200+6000+18000 = 43200
check("2liv: costo 43200", abs(r4["costo_totale_eur"] - 43200.0) < 1e-6)

# --- 5. casi di errore ---
for nome, kw in [
    ("serie None", dict(prezzi=None)),
    ("serie vuota", dict(prezzi=hours([]))),
    ("indice non datetime", dict(prezzi=pd.Series([1.0, 2.0]))),
    ("serie < 24h", dict(prezzi=hours([100.0] * 23))),
    ("base 0", dict(prezzi=hours([100.0] * 48), carico_base_mw=0.0)),
    ("base negativa", dict(prezzi=hours([100.0] * 48), carico_base_mw=-5.0)),
    ("base non numerica", dict(prezzi=hours([100.0] * 48), carico_base_mw="x")),
    ("forma invalida", dict(prezzi=hours([100.0] * 48), forma_carico="luna")),
    ("quota > 100", dict(prezzi=hours([100.0] * 48), quota_coperta_pct=101.0)),
    ("quota negativa", dict(prezzi=hours([100.0] * 48), quota_coperta_pct=-1.0)),
    ("prezzo fisso non numerico", dict(prezzi=hours([100.0] * 48), prezzo_coperto_eur_mwh="x")),
    ("var 0", dict(prezzi=hours([100.0] * 48), variazione_carico_pct=0.0)),
    ("var > 50", dict(prezzi=hours([100.0] * 48), variazione_carico_pct=51.0)),
    ("var non numerica", dict(prezzi=hours([100.0] * 48), variazione_carico_pct="x")),
]:
    rr = calcola(**kw)
    check("errore %s" % nome, (not rr["valido"]) and isinstance(rr["errore"], str) and len(rr["errore"]) > 0)

# --- 6. NaN / tz / duplicati ---
v6 = [100.0] * 48
v6[10] = np.nan
r6 = calcola(hours(v6), carico_base_mw=10.0)
check("NaN: droppato, n_ore 47", r6["valido"] and r6["n_ore"] == 47)
r6b = calcola(hours([100.0] * 48, tz="Europe/Zurich"), carico_base_mw=10.0)
check("tz-aware: valido", r6b["valido"] and r6b["n_ore"] == 48)
idx = pd.date_range("2025-01-06", periods=48, freq="h")
dup = pd.Series(np.r_[np.full(48, 100.0), [999.0]], index=idx.append(idx[:1]))
r6c = calcola(dup, carico_base_mw=10.0, forma_carico="piatto")
check("duplicati: keep-first, n_ore 48, costo usa 100",
      r6c["valido"] and r6c["n_ore"] == 48 and abs(r6c["costo_totale_eur"] - (0.7 * 480 * 100 + 0.3 * 480 * 100)) < 1e-6)

# --- 7. determinismo ---
ra = calcola(hours([100.0] * 48), carico_base_mw=7.5, forma_carico="diurno",
             quota_coperta_pct=63.0, prezzo_coperto_eur_mwh=95.5)
rb = calcola(hours([100.0] * 48), carico_base_mw=7.5, forma_carico="diurno",
             quota_coperta_pct=63.0, prezzo_coperto_eur_mwh=95.5)
check("determinismo: stesso rischio", ra["rischio_volume_eur"] == rb["rischio_volume_eur"])
check("determinismo: stesso costo", ra["costo_totale_eur"] == rb["costo_totale_eur"])

# --- 8. copertura alta = rischio BASSO su piatto ---
r8 = calcola(hours([100.0] * 48), carico_base_mw=10.0, forma_carico="piatto",
             quota_coperta_pct=100.0, prezzo_coperto_eur_mwh=100.0,
             variazione_carico_pct=10.0)
check("copertura piena: valido", r8["valido"])
check("copertura piena piatto: rischio 14400 = 30% -> ALTO",
      r8["giudizio"] == "ALTO" and abs(r8["rischio_volume_eur"] - 14400.0) < 1e-6)

# --- 9. registry tab161 (robusto all'aggiunta di tab successive) ---
decl = [ln for ln in src.splitlines() if re.search(r"tab159, tab160, tab161(, tab\d+)* = st\.tabs\(\[", ln)]
check("registry: dichiarazione tab161", len(decl) == 1)
seg = decl[0] if decl else ""
dvars = re.findall(r"tab\d+", seg.split("= st.tabs")[0])
check("registry: tab161 tra le variabili dichiarate", "tab161" in dvars)
check("registry: n titoli = n variabili", seg.count('", "') + 1 == len(dvars))
check("registry: titolo Rischio volume presente", '"📦 Rischio volume"' in seg)
withs = re.findall(r"^    with (tab\d+):", src, re.M)
check("registry: with tabN in sequenza 1..n senza buchi",
      withs == ["tab%d" % i for i in range(1, len(withs) + 1)])
check("registry: with tab161 presente", "tab161" in withs)
check("registry: helper a livello modulo",
      any(isinstance(n, ast.FunctionDef) and n.name == "calcola_rischio_volume" for n in tree.body))
check("registry: nessuna chiave widget rv161 duplicata",
      len(re.findall(r'key="rv161_[a-z]+"', src)) == len(set(re.findall(r'key="rv161_[a-z]+"', src))))

print("checks: %d, fails: %d" % (_nchecks[0], len(fails)))


def test_standalone_checks_verdi():
    """Espone a pytest i check standalone (eseguiti all'import del modulo).

    Prima di questa funzione i check giravano silenziosamente in fase di
    collection: un FAIL non faceva fallire la suite.
    """
    assert not fails, f"{len(fails)} check falliti: {fails[:8]}"
