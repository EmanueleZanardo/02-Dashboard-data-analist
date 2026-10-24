"""Test tab629 "🌬️🏭 Direct Air Capture: il costo della CO2 dall'aria".

Demo calcolata a mano: 1 t/h x 8000 h -> 8.000 t CO2/anno;
CRF(8 %, 25 a) = 0,09367877905196811; capex 800 €/(t/a) x 8000 t
= 6.400.000; capitale annuo = 6,4M x CRF + 6,4M x 4 %
= 855.544,185932596; energia el. 8000 x 1500 x 60/1000 = 720.000;
calore 8000 x 1750 x 20/1000 = 280.000; totale 1.855.544,185932596;
unit = 231,9430232415745 €/t. Benchmark ETS 100 -> NON_CONVIENTE
(gap 131,94; ETS di pareggio = 231,94). Feed PtX: CH4 = 8000/2,7444
= 2.915,03 t; metanolo = 8000/1,3736 = 5.824,11 t;
SAF = 8000/3,1 = 2.580,65 t.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh629_num", "mh629_nneg", "mh629_pos", "mh629_frac01",
           "mh629_t_co2_annue", "mh629_crf", "mh629_capex_totale",
           "mh629_costo_capitale_annuo", "mh629_costo_energia_el",
           "mh629_costo_energia_th", "mh629_costo_unitario",
           "mh629_verdetto", "mh629_feed_metano", "mh629_feed_metanolo",
           "mh629_feed_saf", "mh629_sensibilita", "mh629_demo")

TITLE629 = ("🌬️🏭 Direct Air Capture: il costo della CO2 dall'aria")

DEMO = _F["mh629_demo"]()
T_DEMO = 8000.0
CRF_DEMO = 0.09367877905196811
CAPEX_TOT_DEMO = 6400000.0
CAP_ANN_DEMO = 855544.185932596
EL_DEMO = 720000.0
TH_DEMO = 280000.0
TOT_DEMO = 1855544.185932596
U_DEMO = 231.9430232415745
FEED_CH4_DEMO = 2915.0269639994167
FEED_MEOH_DEMO = 5824.111822947001
FEED_SAF_DEMO = 2580.6451612903224


class TestW629Validatori:
    def test_num(self):
        assert _F["mh629_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh629_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh629_nneg"](0, "x") == 0.0
        assert _F["mh629_pos"](0.001, "x") == 0.001
        assert _F["mh629_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh629_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh629_pos"](bad, "x")
        for bad in (-0.1, 1.1):
            with pytest.raises(ValueError):
                _F["mh629_frac01"](bad, "x")


class TestW629Catena:
    def test_t_co2_e_crf(self):
        assert _F["mh629_t_co2_annue"](1.0, 8000.0) == T_DEMO
        assert _F["mh629_crf"](8.0, 25.0) == pytest.approx(CRF_DEMO)
        assert _F["mh629_crf"](0.0, 25.0) == pytest.approx(1.0 / 25.0)
        with pytest.raises(ValueError):
            _F["mh629_t_co2_annue"](-1.0, 8000.0)
        with pytest.raises(ValueError):
            _F["mh629_crf"](8.0, 0.0)

    def test_capex_e_capitale(self):
        assert _F["mh629_capex_totale"](800.0, T_DEMO) == CAPEX_TOT_DEMO
        ca = _F["mh629_costo_capitale_annuo"](CAPEX_TOT_DEMO, CRF_DEMO, 4.0)
        assert ca == pytest.approx(CAP_ANN_DEMO)
        with pytest.raises(ValueError):
            _F["mh629_capex_totale"](-5.0, T_DEMO)

    def test_energia(self):
        assert _F["mh629_costo_energia_el"](T_DEMO, 1500.0, 60.0) == EL_DEMO
        assert _F["mh629_costo_energia_th"](T_DEMO, 1750.0, 20.0) == TH_DEMO
        assert _F["mh629_costo_energia_el"](T_DEMO, 1500.0, 0.0) == 0.0

    def test_unitario(self):
        assert _F["mh629_costo_unitario"](TOT_DEMO, T_DEMO) == \
            pytest.approx(U_DEMO)
        assert _F["mh629_costo_unitario"](TOT_DEMO, 0.0) is None
        with pytest.raises(ValueError):
            _F["mh629_costo_unitario"](-1.0, T_DEMO)

    def test_verdetto(self):
        v = _F["mh629_verdetto"](U_DEMO, 100.0)
        assert v["verdetto"] == "NON_CONVIENTE"
        assert v["gap"] == pytest.approx(U_DEMO - 100.0)
        assert "231.94" in v["msg"]  # ETS di pareggio citato nel msg
        v2 = _F["mh629_verdetto"](90.0, 100.0)
        assert v2["verdetto"] == "CONVIENTE"
        v3 = _F["mh629_verdetto"](110.0, 100.0)
        assert v3["verdetto"] == "MARGINALE"
        v4 = _F["mh629_verdetto"](None, 100.0)
        assert v4["verdetto"] == "NON_CALCOLABILE"
        with pytest.raises(ValueError):
            _F["mh629_verdetto"](U_DEMO, -1.0)

    def test_feed_ptx(self):
        assert _F["mh629_feed_metano"](T_DEMO) == \
            pytest.approx(FEED_CH4_DEMO)
        assert _F["mh629_feed_metanolo"](T_DEMO) == \
            pytest.approx(FEED_MEOH_DEMO)
        assert _F["mh629_feed_saf"](T_DEMO) == \
            pytest.approx(FEED_SAF_DEMO)
        assert _F["mh629_feed_metano"](0.0) == 0.0

    def test_sensibilita(self):
        rows = _F["mh629_sensibilita"](
            1.0, 8000.0, 8.0, 25.0, 4.0, 1500.0, 1750.0, 20.0, 100.0,
            [400.0, 800.0], [30.0, 60.0, 100.0])
        assert len(rows) == 6
        r00 = rows[0]
        assert r00["capex_spec_eur_tpa"] == 400.0
        assert r00["prezzo_el_eur_mwh"] == 30.0
        # capex dimezzato: capitale annuo dimezzato, energia invariata
        u00 = (CAP_ANN_DEMO / 2 + T_DEMO * 1500.0 * 30.0 / 1000.0
               + TH_DEMO) / T_DEMO
        assert r00["costo_unit_eur_t"] == pytest.approx(u00)
        assert r00["verdetto"] == "NON_CONVIENTE"
        r13 = rows[4]
        assert r13["capex_spec_eur_tpa"] == 800.0
        assert r13["prezzo_el_eur_mwh"] == 60.0
        assert r13["costo_unit_eur_t"] == pytest.approx(U_DEMO)
        assert r13["verdetto"] == "NON_CONVIENTE"

    def test_demo(self):
        d = DEMO
        assert d["portata_t_h"] == 1.0
        assert d["ore_annue"] == 8000.0
        assert d["benchmark_ets"] == 100.0

    def test_catena_completa(self):
        d = dict(DEMO)
        t = _F["mh629_t_co2_annue"](d["portata_t_h"], d["ore_annue"])
        crf = _F["mh629_crf"](d["tasso_pct"], d["anni"])
        cp = _F["mh629_capex_totale"](d["capex_spec_eur_tpa"], t)
        ca = _F["mh629_costo_capitale_annuo"](cp, crf, d["opex_pct"])
        ce = _F["mh629_costo_energia_el"](t, d["kwh_el_t"],
                                          d["prezzo_el_mwh"])
        ct = _F["mh629_costo_energia_th"](t, d["kwh_th_t"],
                                          d["prezzo_th_mwh"])
        tot = ca + ce + ct
        u = _F["mh629_costo_unitario"](tot, t)
        ver = _F["mh629_verdetto"](u, d["benchmark_ets"])
        assert t == pytest.approx(T_DEMO)
        assert crf == pytest.approx(CRF_DEMO)
        assert cp == pytest.approx(CAPEX_TOT_DEMO)
        assert ca == pytest.approx(CAP_ANN_DEMO)
        assert ce == pytest.approx(EL_DEMO)
        assert ct == pytest.approx(TH_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert u == pytest.approx(U_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"
        assert _F["mh629_feed_metano"](t) == pytest.approx(FEED_CH4_DEMO)


class TestW629Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab629:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 692
        assert TITLE629 in titles
        assert TITLE629 in titles

    def test_chain(self):
        assert ", tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692 = st.tabs([" in self._src()
        assert "with tab629:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st629_[a-z0-9_]+", self._ui()))
        attese = {"st629_port", "st629_ore", "st629_pel", "st629_pth",
                  "st629_cx", "st629_anni", "st629_tasso", "st629_opex",
                  "st629_bm", "st629_kel", "st629_kth", "st629_tab",
                  "st629_graf", "st629_go", "st629_fig", "st629_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st629_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W629 (22/10/2026)')[1]
        sec = sec.split('# W628 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
