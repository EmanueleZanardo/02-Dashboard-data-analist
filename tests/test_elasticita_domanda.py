"""Test calcola_elasticita_domanda - tab164 (stile pytest, via appfuncs).

Copre: numeri esatti su relazione log-lineare nota, carico rigido,
relazione controintuitiva, what-if calcolabile a mano, casi di errore,
robustezza dati (NaN/tz/duplicati), determinismo, registry tab164.
"""
import re

import numpy as np
import pandas as pd

from appfuncs import load

_F = load("calcola_elasticita_domanda")
calcola = _F["calcola_elasticita_domanda"]

TZ = "Europe/Zurich"


def serie(valori, start="2026-01-05", tz=None, name="p"):
    idx = pd.date_range(start, periods=len(valori), freq="h", tz=tz)
    return pd.Series(np.asarray(valori, dtype=float), index=idx, name=name)


def prezzo_variabile(giorni=30, start="2026-01-05", tz=None):
    """Prezzo orario deterministico sempre > 0 con variabilita' giorno/notte."""
    vals = []
    for d in range(giorni):
        for h in range(24):
            vals.append(60.0 + 40.0 * np.sin(2 * np.pi * h / 24) + 10.0 * (d % 3))
    return serie(vals, start=start, tz=tz)


# ------------------------------------------------------- relazione log-lineare
class TestLogLineare:
    def test_eps_meno_mezzo_esatto(self):
        p = prezzo_variabile(30)
        q = serie(100.0 * p.to_numpy() ** -0.5, name="q")
        r = calcola(p, q)
        assert r["valido"] and r["errore"] is None
        assert r["n_ore"] == 720
        assert abs(r["elasticita"] - (-0.5)) < 1e-9
        assert r["r2"] == 1.0
        assert r["p_value"] == 0.0
        assert r["giudizio"] == "ELASTICA"

    def test_cluster_quartili_coerenti(self):
        p = prezzo_variabile(30)
        q = serie(100.0 * p.to_numpy() ** -0.5, name="q")
        r = calcola(p, q)
        tab = r["tabella_cluster"]
        assert len(tab) == 4
        assert list(tab["Fascia prezzo"]) == ["Q1 (economiche)", "Q2", "Q3", "Q4 (care)"]
        assert (tab["Ore"] == 180).all()
        assert np.allclose(tab["Elasticita'"].to_numpy(), -0.5, atol=1e-9)
        assert (tab["R2"] == 1.0).all()
        assert float(tab.loc[3, "Prezzo medio (EUR/MWh)"]) > float(tab.loc[0, "Prezzo medio (EUR/MWh)"])

    def test_whatif_struttura(self):
        p = prezzo_variabile(30)
        q = serie(100.0 * p.to_numpy() ** -0.5, name="q")
        r = calcola(p, q, shift_pct=10.0)
        w = r["tabella_whatif"]
        assert list(w["Quota spostata (%)"]) == [5, 10, 15, 20, 25, 30]
        assert (w["Risparmio stimato (EUR)"] > 0).all()
        assert (w["Risparmio (%)"] > 0).all()
        assert w["Risparmio stimato (EUR)"].is_monotonic_increasing
        # risparmio al 10% proporzionale alla quota
        r5 = float(w.loc[w["Quota spostata (%)"] == 5, "Risparmio stimato (EUR)"].iloc[0])
        r10 = float(w.loc[w["Quota spostata (%)"] == 10, "Risparmio stimato (EUR)"].iloc[0])
        assert abs(r10 - 2 * r5) < 1e-6


# ------------------------------------------------------------------ casi limite
class TestComportamenti:
    def test_carico_rigido(self):
        p = prezzo_variabile(30)
        q = serie(np.full(720, 10.0), name="q")
        r = calcola(p, q)
        assert r["valido"]
        assert abs(r["elasticita"]) < 1e-12
        assert r["r2"] == 0.0
        assert r["p_value"] > 0.99  # ~1.0 a meno di arrotondamenti float
        assert r["giudizio"] == "NON SIGNIFICATIVA"

    def test_relazione_positiva_controintuitiva(self):
        p = prezzo_variabile(30)
        q = serie(0.1 * p.to_numpy(), name="q")
        r = calcola(p, q)
        assert r["valido"]
        assert abs(r["elasticita"] - 1.0) < 1e-9
        assert r["giudizio"] == "CONTROINTUITIVA"

    def test_moderata(self):
        p = prezzo_variabile(30)
        q = serie(50.0 * p.to_numpy() ** -0.2, name="q")
        r = calcola(p, q)
        assert r["valido"]
        assert abs(r["elasticita"] - (-0.2)) < 1e-9
        assert r["giudizio"] == "MODERATA"


# ------------------------------------------------------------- what-if a mano
class TestWhatIfManuale:
    def test_numeri_a_mano(self):
        # 14 giorni: 7 a 100 EUR/MWh, 7 a 50 EUR/MWh, carico piatto 10 MW
        vals = [100.0] * (7 * 24) + [50.0] * (7 * 24)
        p = serie(vals)
        q = serie(np.full(336, 10.0), name="q")
        r = calcola(p, q)
        assert r["valido"]
        assert r["p_q4_medio"] == 100.0
        assert r["p_q1_medio"] == 50.0
        assert abs(r["e_q4_mwh"] - 840.0) < 1e-9
        assert abs(r["costo_totale"] - 252000.0) < 1e-6
        w = r["tabella_whatif"]
        r10 = float(w.loc[w["Quota spostata (%)"] == 10, "Risparmio stimato (EUR)"].iloc[0])
        assert abs(r10 - 4200.0) < 1e-6
        peq = float(w.loc[w["Quota spostata (%)"] == 10, "Prezzo medio equivalente (EUR/MWh)"].iloc[0])
        assert abs(peq - 73.75) < 1e-9
        # KPI con shift 10%
        r10b = calcola(p, q, shift_pct=10.0)
        assert abs(r10b["risparmio_kpi"] - 4200.0) < 1e-6


# ---------------------------------------------------------------------- errori
class TestErrori:
    def test_prezzi_vuoti(self):
        r = calcola(serie([]), serie(np.full(200, 10.0), name="q"))
        assert not r["valido"] and bool(r["errore"])

    def test_indice_non_datetime(self):
        r = calcola(pd.Series(np.full(200, 100.0)),
                    serie(np.full(200, 10.0), name="q"))
        assert not r["valido"]

    def test_troppo_corta(self):
        r = calcola(prezzo_variabile(4), serie(np.full(96, 10.0), name="q"))
        assert not r["valido"] and "insufficienti" in r["errore"]

    def test_prezzo_costante(self):
        r = calcola(serie(np.full(200, 100.0)),
                    serie(10.0 + np.arange(200) * 0.01, name="q"))
        assert not r["valido"] and "costante" in r["errore"]

    def test_carico_none(self):
        r = calcola(prezzo_variabile(10), None)
        assert not r["valido"]

    def test_carico_non_serie(self):
        r = calcola(prezzo_variabile(10), [10.0] * 240)
        assert not r["valido"]

    def test_nessuna_ora_comune(self):
        r = calcola(prezzo_variabile(10),
                    serie(np.full(240, 10.0), start="2027-01-05", name="q"))
        assert not r["valido"]

    def test_solo_prezzi_negativi(self):
        r = calcola(serie(np.full(200, -5.0)),
                    serie(np.full(200, 10.0), name="q"))
        assert not r["valido"]

    def test_prezzi_negativi_scartati(self):
        vals = list(prezzo_variabile(10).to_numpy())
        vals[::24] = [-10.0] * 10  # 10 ore negative scartate
        p = serie(vals)
        q = serie(np.full(240, 10.0), name="q")
        r = calcola(p, q)
        assert r["valido"] and r["n_scartate"] == 10 and r["n_ore"] == 230


# --------------------------------------------------------------- robustezza
class TestRobustezza:
    def test_tz_aware(self):
        p = prezzo_variabile(10, tz=TZ)
        q = serie(np.full(240, 10.0), tz=TZ, name="q")
        r = calcola(p, q)
        assert r["valido"] and r["n_ore"] == 240

    def test_duplicati_keep_first(self):
        p = prezzo_variabile(10)
        p2 = pd.concat([p, p])  # duplicati
        q = serie(np.full(240, 10.0), name="q")
        r = calcola(p2, q)
        assert r["valido"] and r["n_ore"] == 240

    def test_nan_carico_scartato(self):
        p = prezzo_variabile(10)
        vals = np.full(240, 10.0)
        vals[::12] = np.nan  # 20 ore NaN scartate
        q = serie(vals, name="q")
        r = calcola(p, q)
        assert r["valido"] and r["n_scartate"] == 20 and r["n_ore"] == 220

    def test_determinismo(self):
        p = prezzo_variabile(30)
        q = serie(100.0 * p.to_numpy() ** -0.5, name="q")
        ra, rb = calcola(p, q), calcola(p, q)
        assert ra["elasticita"] == rb["elasticita"]
        assert ra["risparmio_kpi"] == rb["risparmio_kpi"]


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab164_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab164" in dvars  # robusto all'aggiunta di tab successive (era conteggio esatto 164)
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(dvars) == len(withs)
        assert '"⚡ Elasticità domanda"' in src
        keys = re.findall(r'key="(el164_[^"]+)"', src)
        fkeys = re.findall(r'key=f"(el164_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 3
        assert len(fkeys) == len(set(fkeys))
        assert re.search(r"^def calcola_elasticita_domanda\(", src, re.M) is not None
