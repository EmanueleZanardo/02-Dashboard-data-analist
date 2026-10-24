"""Test tab628 "🚚💧 Trasporto H2: pipeline, trailer o liquido? (logistica idrogeno)".

Demo calcolata a mano: 7000 kg/h x 8000 h -> 56.000.000 kg H2/anno;
distanza 300 km. CRF(8 %, 30 a) = 0,08882743338727227; pipeline:
capex 1.200.000 x 300 = 360.000.000; annuo = 360M x CRF + 360M x 2 %
= 39.177.876,019418016; compressione 56M x 0,10 = 5.600.000;
u_pipeline = 44.777.876,019418016 / 56M = 0,7996049289181788 €/kg.
u_trailer = 0,25 x 300/100 = 0,75 €/kg. LH2: 56M x 1,20 = 67,2M +
56M x 0,18 x 3 = 30,24M + 56M x 2 % x 5,13 = 5,7456M = 103.185.600;
u_lh2 = 1,8426 €/kg. Vincitore: TRAILER (0,75 < 0,7996 < 1,8426);
delivered = 5,13 + 0,75 = 5,88 €/kg. Break-even pipeline vs trailer:
den = 0,25/100 - 1,2M x (CRF + 2 %)/56M = 0,00016798357027273704;
km* = 0,10 / den = 595,2963128336935 km.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh628_num", "mh628_nneg", "mh628_pos", "mh628_frac01",
           "mh628_kg_h2_annui", "mh628_crf",
           "mh628_costo_pipeline_annuo", "mh628_costo_compr_pipeline",
           "mh628_unit_pipeline", "mh628_unit_trailer",
           "mh628_costo_lh2_annuo", "mh628_unit_lh2",
           "mh628_delivered", "mh628_vincitore",
           "mh628_breakeven_pipe_trailer", "mh628_sensibilita",
           "mh628_demo")

TITLE628 = ("🚚💧 Trasporto H2: pipeline, trailer o liquido? "
            "(logistica idrogeno)")

DEMO = _F["mh628_demo"]()
KG_DEMO = 56000000.0
CRF_DEMO = 0.08882743338727227
PIPE_ANN_DEMO = 39177876.019418016
COMPR_DEMO = 5600000.0
U_PIPE_DEMO = 0.7996049289181788
U_TRAILER_DEMO = 0.75
C_LH2_DEMO = 103185600.0
U_LH2_DEMO = 1.8426
KB_DEMO = 595.2963128336935
KM_DEMO = 300.0
LCOH_DEMO = 5.13


class TestW628Validatori:
    def test_num(self):
        assert _F["mh628_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh628_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh628_nneg"](0, "x") == 0.0
        assert _F["mh628_pos"](0.001, "x") == 0.001
        assert _F["mh628_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh628_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh628_pos"](bad, "x")
        for bad in (-0.1, 1.1):
            with pytest.raises(ValueError):
                _F["mh628_frac01"](bad, "x")


class TestW628Catena:
    def test_kg_e_crf(self):
        assert _F["mh628_kg_h2_annui"](7000.0, 8000.0) == KG_DEMO
        assert _F["mh628_crf"](8.0, 30.0) == pytest.approx(CRF_DEMO)
        assert _F["mh628_crf"](0.0, 30.0) == pytest.approx(1.0 / 30.0)
        with pytest.raises(ValueError):
            _F["mh628_kg_h2_annui"](-1.0, 8000.0)
        with pytest.raises(ValueError):
            _F["mh628_crf"](8.0, 0.0)

    def test_pipeline(self):
        pa = _F["mh628_costo_pipeline_annuo"](1200000.0, KM_DEMO,
                                              2.0, CRF_DEMO)
        assert pa == pytest.approx(PIPE_ANN_DEMO)
        cc = _F["mh628_costo_compr_pipeline"](KG_DEMO, 0.10)
        assert cc == COMPR_DEMO
        assert _F["mh628_unit_pipeline"](pa, cc, KG_DEMO) == \
            pytest.approx(U_PIPE_DEMO)
        assert _F["mh628_unit_pipeline"](pa, cc, 0.0) is None

    def test_trailer_lh2(self):
        assert _F["mh628_unit_trailer"](0.25, KM_DEMO) == \
            U_TRAILER_DEMO
        cl = _F["mh628_costo_lh2_annuo"](KG_DEMO, 1.20, 0.18,
                                         KM_DEMO, 2.0, LCOH_DEMO)
        assert cl == pytest.approx(C_LH2_DEMO)
        assert _F["mh628_unit_lh2"](cl, KG_DEMO) == \
            pytest.approx(U_LH2_DEMO)
        assert _F["mh628_unit_lh2"](cl, 0.0) is None

    def test_delivered(self):
        assert _F["mh628_delivered"](LCOH_DEMO, U_TRAILER_DEMO) == \
            pytest.approx(5.88)
        assert _F["mh628_delivered"](LCOH_DEMO, None) is None

    def test_vincitore_stati(self):
        v = _F["mh628_vincitore"](U_PIPE_DEMO, U_TRAILER_DEMO,
                                  U_LH2_DEMO)
        assert v["vincitore"] == "TRAILER"
        assert v["unit_min"] == pytest.approx(U_TRAILER_DEMO)
        assert "risparmio" in v["msg"]
        v2 = _F["mh628_vincitore"](0.50, 0.75, 1.8426)
        assert v2["vincitore"] == "PIPELINE"
        v3 = _F["mh628_vincitore"](None, None, None)
        assert v3["vincitore"] == "NON_CALCOLABILE"

    def test_breakeven(self):
        kb = _F["mh628_breakeven_pipe_trailer"](1200000.0, 2.0,
                                                CRF_DEMO, KG_DEMO,
                                                0.10, 0.25)
        assert kb == pytest.approx(KB_DEMO)
        # portata piccola: il trailer vince sempre (den <= 0)
        assert _F["mh628_breakeven_pipe_trailer"](
            1200000.0, 2.0, CRF_DEMO, 8000000.0, 0.10,
            0.25) is None
        assert _F["mh628_breakeven_pipe_trailer"](
            1200000.0, 2.0, CRF_DEMO, 0.0, 0.10, 0.25) is None
        assert _F["mh628_breakeven_pipe_trailer"](
            1200000.0, 2.0, CRF_DEMO, KG_DEMO, 0.10, 0.0) is None


class TestW628Sensibilita:
    def _args(self):
        return (7000.0, 8000.0, 5.13, 1200000.0, 2.0, 0.10, 8.0,
                30.0, 0.25, 1.20, 0.18, 2.0)

    def test_geometria(self):
        rows = _F["mh628_sensibilita"](*self._args(),
                                       [100.0, 300.0],
                                       [1000.0, 7000.0])
        assert len(rows) == 4
        assert rows[0]["distanza_km"] == 100.0
        assert rows[0]["portata_kg_h"] == 1000.0

    def test_riga_estrema_hand_computed(self):
        # km 100, portata 1000 kg/h (8M kg/anno): pipeline 1,7324,
        # trailer 0,25, LH2 1,4826 -> TRAILER; break-even mai
        rows = _F["mh628_sensibilita"](*self._args(), [100.0],
                                       [1000.0])
        r = rows[0]
        assert r["kg_annui"] == 8000000.0
        assert r["unit_pipeline"] == \
            pytest.approx(1.7324115008090841)
        assert r["unit_trailer"] == pytest.approx(0.25)
        assert r["unit_lh2"] == pytest.approx(1.4826)
        assert r["vincitore"] == "TRAILER"
        assert r["costo_min_eur_kg"] == pytest.approx(0.25)

    def test_monotonia_trailer_distanza(self):
        rows = _F["mh628_sensibilita"](*self._args(),
                                       [100.0, 300.0, 600.0],
                                       [7000.0])
        ut = [r["unit_trailer"] for r in rows]
        assert ut == sorted(ut)

    def test_pipeline_guadagna_scala(self):
        # a 600 km e 20000 kg/h la pipeline batte il trailer
        rows = _F["mh628_sensibilita"](*self._args(), [600.0],
                                       [20000.0])
        r = rows[0]
        assert r["vincitore"] == "PIPELINE"
        assert r["unit_pipeline"] < r["unit_trailer"]

    def test_liste_vuote(self):
        assert _F["mh628_sensibilita"](*self._args(), [],
                                      [7000.0]) == []
        assert _F["mh628_sensibilita"](*self._args(), [300.0],
                                      []) == []

    def test_demo_catena_completa(self):
        d = DEMO
        kg = _F["mh628_kg_h2_annui"](d["portata_kg_h"],
                                     d["ore_annue"])
        crf = _F["mh628_crf"](d["tasso_pct"], d["anni"])
        pa = _F["mh628_costo_pipeline_annuo"](d["capex_eur_km"],
                                              d["distanza_km"],
                                              d["opex_pct"], crf)
        pc = _F["mh628_costo_compr_pipeline"](kg,
                                              d["compr_eur_kg"])
        up = _F["mh628_unit_pipeline"](pa, pc, kg)
        ut = _F["mh628_unit_trailer"](d["tariffa_trailer_100km"],
                                      d["distanza_km"])
        cl = _F["mh628_costo_lh2_annuo"](kg, d["liquef_eur_kg"],
                                         d["tariffa_lh2_100km"],
                                         d["distanza_km"],
                                         d["boiloff_pct"],
                                         d["lcoh_eur_kg"])
        ul = _F["mh628_unit_lh2"](cl, kg)
        ver = _F["mh628_vincitore"](up, ut, ul)
        kb = _F["mh628_breakeven_pipe_trailer"](
            d["capex_eur_km"], d["opex_pct"], crf, kg,
            d["compr_eur_kg"], d["tariffa_trailer_100km"])
        assert kg == pytest.approx(KG_DEMO)
        assert crf == pytest.approx(CRF_DEMO)
        assert pa == pytest.approx(PIPE_ANN_DEMO)
        assert pc == pytest.approx(COMPR_DEMO)
        assert up == pytest.approx(U_PIPE_DEMO)
        assert ut == pytest.approx(U_TRAILER_DEMO)
        assert cl == pytest.approx(C_LH2_DEMO)
        assert ul == pytest.approx(U_LH2_DEMO)
        assert ver["vincitore"] == "TRAILER"
        assert _F["mh628_delivered"](d["lcoh_eur_kg"], ut) == \
            pytest.approx(5.88)
        assert kb == pytest.approx(KB_DEMO)


class TestW628Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab628:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 679
        assert TITLE628 in titles
        assert TITLE628 in titles

    def test_chain(self):
        assert ", tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679 = st.tabs([" in self._src()
        assert "with tab628:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st628_[a-z0-9_]+", self._ui()))
        attese = {"st628_port", "st628_ore", "st628_km",
                  "st628_lcoh", "st628_tasso", "st628_anni",
                  "st628_cxkm", "st628_opex", "st628_compr",
                  "st628_tar", "st628_liq", "st628_tarlh",
                  "st628_boil", "st628_tab", "st628_graf",
                  "st628_go", "st628_fig", "st628_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st628_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W628 (22/10/2026)')[1]
        sec = sec.split('# W627 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
