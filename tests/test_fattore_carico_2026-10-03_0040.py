"""Test calcola_fattore_carico - tab165 (stile pytest, via appfuncs).

Copertura: numeri a mano su scenari controllati (LF, ore equivalenti,
premio vs profilo piatto, what-if taglio picco), tabella mensile,
casi di errore, robustezza dati (NaN/tz/duplicati), determinismo,
registry tab165.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_fattore_carico")
fc = fns["calcola_fattore_carico"]


def serie_48h(prezzo=100.0):
    idx = pd.date_range("2026-01-05", periods=48, freq="h")  # lunedi'
    return pd.Series(float(prezzo), index=idx)


def serie_24h_prezzi_fascia():
    idx = pd.date_range("2026-01-05", periods=24, freq="h")
    return pd.Series([120.0 if 8 <= h < 19 else 60.0 for h in idx.hour], index=idx)


class TestNumeriAMano:
    def test_scenario_a_piatto_per_fascia(self):
        # 48h prezzo piatto 100, MW F1=10/F2=6/F3=4
        # F1: 11h/gg x2 = 22h, F2: 5h/gg x2 = 10h, F3: 8h/gg x2 = 16h
        r = fc(serie_48h(), 10, 6, 4)
        assert r["valido"] and r["errore"] is None
        assert r["energia_mwh"] == pytest.approx(344.0)
        assert r["picco_mw"] == pytest.approx(10.0)
        assert r["potenza_media_mw"] == pytest.approx(344.0 / 48)
        assert r["lf"] == pytest.approx(0.7166667, abs=1e-6)
        assert r["lf_pct"] == pytest.approx(71.66667, abs=1e-4)
        assert r["ore_equivalenti"] == pytest.approx(34.4)
        assert r["n_ore"] == 48
        assert r["costo_reale"] == pytest.approx(34400.0)
        assert r["costo_flat"] == pytest.approx(34400.0)
        assert r["premio_eur"] == pytest.approx(0.0)
        assert r["premio_pct"] == pytest.approx(0.0)
        assert r["giudizio"] == "BUONO"
        m = r["tabella_mensile"]
        assert len(m) == 1 and m.iloc[0]["Mese"] == "2026-01"
        assert m.iloc[0]["Energia (MWh)"] == pytest.approx(344.0)
        assert m.iloc[0]["Fattore di carico (%)"] == pytest.approx(71.7, abs=0.05)

    def test_scenario_a_whatif10(self):
        r = fc(serie_48h(), 10, 6, 4)  # riduzione default 10%
        wk = r["whatif_kpi"]
        assert wk["soglia"] == pytest.approx(9.0)
        assert wk["n_sopra"] == 22  # le 22 ore F1
        assert wk["e_sopra"] == pytest.approx(22.0)
        assert wk["p_sopra"] == pytest.approx(100.0)
        # (10-9)*1000*40*(48/8760) = 219.178...
        assert wk["risp_pot"] == pytest.approx(219.178, abs=1e-2)
        assert wk["risp_en"] == pytest.approx(0.0)  # prezzo sopra = prezzo medio
        w = r["tabella_whatif"]
        assert list(w["Taglio picco (%)"]) == [5, 10, 15, 20, 25, 30]
        # risparmi totali crescenti col taglio
        tot = list(w["Risparmio totale stimato (EUR)"])
        assert all(b >= a for a, b in zip(tot, tot[1:]))

    def test_scenario_b_carico_piatto(self):
        # carico piatto 10 MW -> LF 100%, premio 0 anche con prezzi a due livelli
        r = fc(serie_24h_prezzi_fascia(), 10, 10, 10)
        assert r["valido"]
        assert r["lf"] == pytest.approx(1.0)
        assert r["ore_equivalenti"] == pytest.approx(24.0)
        assert r["costo_reale"] == pytest.approx(21000.0)  # 11*10*120 + 13*10*60
        assert r["premio_eur"] == pytest.approx(0.0)
        assert r["premio_pct"] == pytest.approx(0.0)
        assert r["giudizio"] == "ECCELLENTE"

    def test_scenario_c_carico_solo_f1(self):
        # carico solo in F1 (ore care): LF basso, premio positivo
        r = fc(serie_24h_prezzi_fascia(), 10, 0, 0)
        assert r["valido"]
        assert r["lf"] == pytest.approx(110.0 / 240, abs=1e-9)
        assert r["ore_equivalenti"] == pytest.approx(11.0)
        assert r["costo_reale"] == pytest.approx(13200.0)
        assert r["premio_eur"] == pytest.approx(3575.0)
        assert r["premio_pct"] == pytest.approx(37.142857, abs=1e-4)
        assert r["giudizio"] == "MEDIO"
        wk = r["whatif_kpi"]
        assert wk["soglia"] == pytest.approx(9.0)
        assert wk["e_sopra"] == pytest.approx(11.0)
        assert wk["p_sopra"] == pytest.approx(120.0)
        assert wk["risp_pot"] == pytest.approx(109.589, abs=1e-2)
        assert wk["risp_en"] == pytest.approx(357.5)  # 11*(120-87.5)

    def test_tabella_mensile_due_mesi(self):
        # 48h da sabato 31/01: sabato -> F2 16h + F3 8h; domenica -> F3 24h
        idx = pd.date_range("2026-01-31", periods=48, freq="h")
        r = fc(pd.Series(100.0, index=idx), 10, 6, 4)
        m = r["tabella_mensile"]
        assert set(m["Mese"]) == {"2026-01", "2026-02"}
        assert m["Ore"].sum() == 48
        # gennaio (sabato): 16*6 + 8*4 = 128 MWh, picco 6, LF 88.9%
        # febbraio (domenica): 24*4 = 96 MWh, picco 4, LF 100%
        assert m["Energia (MWh)"].sum() == pytest.approx(224.0)
        r_gen = m[m["Mese"] == "2026-01"].iloc[0]
        r_feb = m[m["Mese"] == "2026-02"].iloc[0]
        assert r_gen["Energia (MWh)"] == pytest.approx(128.0)
        assert r_gen["Picco (MW)"] == pytest.approx(6.0)
        assert r_gen["Fattore di carico (%)"] == pytest.approx(88.9, abs=0.05)
        assert r_feb["Energia (MWh)"] == pytest.approx(96.0)
        assert r_feb["Fattore di carico (%)"] == pytest.approx(100.0)
        assert ((m["Fattore di carico (%)"] > 0) & (m["Fattore di carico (%)"] <= 100)).all()

    def test_premio_pct_none_con_prezzi_negativi(self):
        # costo flat <= 0 -> premio_pct None ma risultato valido
        r = fc(serie_48h(prezzo=-10.0), 10, 6, 4)
        assert r["valido"]
        assert r["premio_pct"] is None
        assert "non calcolabile" in r["verdetto"]

    def test_riduzione_zero(self):
        r = fc(serie_48h(), 10, 6, 4, riduzione_picco_pct=0.0)
        wk = r["whatif_kpi"]
        assert wk["soglia"] == pytest.approx(10.0)
        assert wk["n_sopra"] == 0 and wk["e_sopra"] == pytest.approx(0.0)
        assert wk["risp_pot"] == pytest.approx(0.0)


class TestErrori:
    def test_prezzi_none(self):
        r = fc(None, 10, 6, 4)
        assert not r["valido"] and r["errore"]

    def test_serie_vuota(self):
        r = fc(pd.Series(dtype=float), 10, 6, 4)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        r = fc(pd.Series([1.0, 2.0], index=[0, 1]), 10, 6, 4)
        assert not r["valido"] and "datetime" in r["errore"]

    def test_serie_troppo_corta(self):
        idx = pd.date_range("2026-01-05", periods=20, freq="h")
        r = fc(pd.Series(100.0, index=idx), 10, 6, 4)
        assert not r["valido"] and "troppo corta" in r["errore"]

    def test_mw_negativo(self):
        r = fc(serie_48h(), -1, 6, 4)
        assert not r["valido"] and "negativi" in r["errore"]

    def test_mw_tutti_zero(self):
        r = fc(serie_48h(), 0, 0, 0)
        assert not r["valido"] and "nullo" in r["errore"]

    def test_mw_non_numerici(self):
        r = fc(serie_48h(), "x", 6, 4)
        assert not r["valido"] and r["errore"]

    def test_costo_potenza_negativo(self):
        r = fc(serie_48h(), 10, 6, 4, costo_potenza_eur_kw_anno=-5)
        assert not r["valido"] and r["errore"]

    def test_riduzione_fuori_range(self):
        r = fc(serie_48h(), 10, 6, 4, riduzione_picco_pct=60)
        assert not r["valido"] and "range" in r["errore"]

    def test_riduzione_non_numerica(self):
        r = fc(serie_48h(), 10, 6, 4, riduzione_picco_pct="x")
        assert not r["valido"] and r["errore"]


class TestRobustezza:
    def test_nan_prezzi_scartati(self):
        p = serie_48h()
        p.iloc[5] = np.nan
        r = fc(p, 10, 6, 4)
        assert r["valido"] and r["n_ore"] == 47

    def test_tz_aware(self):
        p = serie_48h().tz_localize("Europe/Zurich")
        r = fc(p, 10, 6, 4)
        assert r["valido"] and r["lf"] == pytest.approx(0.7166667, abs=1e-6)

    def test_duplicati_keep_first(self):
        p = serie_48h()
        dup = pd.concat([p, p.iloc[[0]]])
        r = fc(dup, 10, 6, 4)
        assert r["valido"] and r["n_ore"] == 48
        assert r["lf"] == pytest.approx(0.7166667, abs=1e-6)

    def test_determinismo(self):
        p = serie_48h()
        ra, rb = fc(p, 10, 6, 4), fc(p, 10, 6, 4)
        assert ra["lf"] == rb["lf"]
        assert ra["premio_eur"] == rb["premio_eur"]
        assert ra["tabella_whatif"].equals(rb["tabella_whatif"])
        assert ra["tabella_mensile"].equals(rb["tabella_mensile"])


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab165_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab165" in dvars  # robusto: appartenenza, non ultima in coda
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]  # sequenza senza buchi
        assert len(dvars) == len(withs)  # n variabili dichiarate == n blocchi
        assert '"📊 Fattore di carico"' in src
        keys = re.findall(r'key="(fc165_[^"]+)"', src)
        fkeys = re.findall(r'key=f"(fc165_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 5
        assert len(fkeys) == len(set(fkeys))
        assert re.search(r"^def calcola_fattore_carico\(", src, re.M) is not None
