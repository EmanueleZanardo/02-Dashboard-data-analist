"""Test tab643 "🔥♨️ Waste heat data center: il calore di scarto diventa teleriscaldamento".

Demo calcolata a mano: DC da 10 MW IT, PUE 1,40, recupero 70 %
-> calore scartato 10 x 0,4 x 8760 x 0,7 = 24.528,0 MWh_th/anno.
COP 3,5 -> calore venduto 24.528 x 3,5/2,5 = 34.339,2 MWh_th/anno;
energia PdC 34.339,2 / 3,5 = 9.811,2 MWh_e/anno.
Ricavi: 34.339,2 x 55 = 1.888.656,0 €/anno;
costo energia PdC: 9.811,2 x 90 = 883.008,0 €/anno;
margine = 1.888.656 - 883.008 - 200.000 = 805.648,0 €/anno.
CRF(7 %, 15 a) = 0,1097946247010065; capex annuo
= 3.500.000 x CRF = 384.281,18645352277 €;
costo netto = (384.281,19 + 883.008 + 200.000) / 34.339,2
= 42,729276932879124 €/MWh_th vs benchmark 60 €/MWh_th;
risparmio = (60 - 42,729276932879124) x 34.339,2 = 593.062,8135464771 €/anno.
Copertura = 34.339,2 / 100.000 = 34,3392 %;
quota HP = 883.008 / 1.888.656 = 46,75324675324675 %.
Flussi [-3.500.000, 805.648 x 15]: VAN(7 %) = 3.837.772,7023881697 €;
TIR = 0,21827563195240163 (21,83 %); payback anno 5
-> CONVIENTE (tolleranza 10 %).
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh643_num", "mh643_nneg", "mh643_pos", "mh643_pct100",
           "mh643_cop", "mh643_calore_scartato_mwh_anno",
           "mh643_hp_q_venduto", "mh643_hp_e_consumata",
           "mh643_ricavi_calore", "mh643_costo_energia_hp",
           "mh643_margine_annuo", "mh643_crf", "mh643_capex_annuo",
           "mh643_costo_netto_eur_mwh", "mh643_risparmio_vs_benchmark",
           "mh643_copertura_pct", "mh643_flussi", "mh643_van", "mh643_tir",
           "mh643_payback", "mh643_verdetto", "mh643_quota_hp_pct",
           "mh643_sensibilita", "mh643_demo_calcoli", "mh643_demo")

TITLE643 = ("🔥♨️ Waste heat data center: il calore di scarto diventa "
            "teleriscaldamento")

QS_DEMO = 24528.0
QV_DEMO = 34339.2
EH_DEMO = 9811.2
RIC_DEMO = 1888656.0
CHP_DEMO = 883008.0
MA_DEMO = 805648.0
CRF_DEMO = 0.1097946247010065
CA_DEMO = 384281.18645352277
CN_DEMO = 42.729276932879124
RS_DEMO = 593062.8135464771
COP_DEMO = 34.3392
QP_DEMO = 46.75324675324675
VAN_DEMO = 3837772.7023881697
TIR_DEMO = 0.21827563195240163
PB_DEMO = 5


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh643_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh643_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh643_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh643_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh643_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh643_pos"](0.0, "x")

    def test_pct100(self):
        assert _F["mh643_pct100"](100, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh643_pct100"](100.1, "x")

    def test_cop(self):
        assert _F["mh643_cop"](3.5, "cop") == 3.5
        for bad in (1.0, 0.9, -2.0):
            with pytest.raises(ValueError):
                _F["mh643_cop"](bad, "cop")


class TestCalcoli:
    def test_calore_scartato(self):
        assert _F["mh643_calore_scartato_mwh_anno"](10.0, 1.40, 70.0) \
            == pytest.approx(QS_DEMO)
        assert _F["mh643_calore_scartato_mwh_anno"](0.0, 1.40, 70.0) == 0.0
        assert _F["mh643_calore_scartato_mwh_anno"](10.0, 1.0, 70.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh643_calore_scartato_mwh_anno"](10.0, 0.9, 70.0)

    def test_hp(self):
        assert _F["mh643_hp_q_venduto"](QS_DEMO, 3.5) == pytest.approx(QV_DEMO)
        assert _F["mh643_hp_e_consumata"](QV_DEMO, 3.5) == pytest.approx(EH_DEMO)
        assert _F["mh643_hp_q_venduto"](0.0, 3.5) == 0.0
        with pytest.raises(ValueError):
            _F["mh643_hp_q_venduto"](QS_DEMO, 1.0)

    def test_ricavi_e_costo_hp(self):
        assert _F["mh643_ricavi_calore"](QV_DEMO, 55.0) == pytest.approx(RIC_DEMO)
        assert _F["mh643_costo_energia_hp"](EH_DEMO, 90.0) == pytest.approx(CHP_DEMO)

    def test_margine(self):
        assert _F["mh643_margine_annuo"](RIC_DEMO, CHP_DEMO, 200000.0) \
            == pytest.approx(MA_DEMO)
        assert _F["mh643_margine_annuo"](0.0, 0.0, 100.0) == -100.0

    def test_crf_e_capex_annuo(self):
        assert _F["mh643_crf"](7.0, 15) == pytest.approx(CRF_DEMO)
        assert _F["mh643_crf"](0.0, 15) == pytest.approx(1.0 / 15)
        assert _F["mh643_capex_annuo"](3500000.0, 7.0, 15) == pytest.approx(CA_DEMO)

    def test_costo_netto_risparmio_copertura(self):
        assert _F["mh643_costo_netto_eur_mwh"](CA_DEMO, CHP_DEMO, 200000.0,
                                              QV_DEMO) == pytest.approx(CN_DEMO)
        assert _F["mh643_costo_netto_eur_mwh"](CA_DEMO, CHP_DEMO, 200000.0,
                                              0.0) is None
        assert _F["mh643_risparmio_vs_benchmark"](60.0, CN_DEMO, QV_DEMO) \
            == pytest.approx(RS_DEMO)
        assert _F["mh643_risparmio_vs_benchmark"](60.0, None, QV_DEMO) is None
        assert _F["mh643_copertura_pct"](QV_DEMO, 100000.0) == pytest.approx(COP_DEMO)
        assert _F["mh643_copertura_pct"](QV_DEMO, 0.0) is None

    def test_flussi_van_tir_payback(self):
        fl = _F["mh643_flussi"](3500000.0, MA_DEMO, 15)
        assert fl[0] == -3500000.0 and len(fl) == 16
        assert _F["mh643_van"](fl, 7.0) == pytest.approx(VAN_DEMO)
        assert _F["mh643_tir"](fl) == pytest.approx(TIR_DEMO)
        assert _F["mh643_payback"](fl) == PB_DEMO

    def test_tir_payback_degeneri(self):
        assert _F["mh643_tir"]([-100.0, -50.0, -10.0]) is None
        assert _F["mh643_tir"]([100.0, 50.0, 10.0]) is None
        assert _F["mh643_payback"]([-100.0, 10.0, 10.0]) is None

    def test_verdetto(self):
        assert _F["mh643_verdetto"](100.0, 3500000.0, 10.0) == "CONVIENTE"
        assert _F["mh643_verdetto"](-100000.0, 3500000.0, 10.0) == "MARGINALE"
        assert _F["mh643_verdetto"](-1000000.0, 3500000.0, 10.0) == "NON_CONVIENTE"
        assert _F["mh643_verdetto"](None, 3500000.0, 10.0) == "NON_CALCOLABILE"

    def test_quota_hp(self):
        assert _F["mh643_quota_hp_pct"](CHP_DEMO, RIC_DEMO) == pytest.approx(QP_DEMO)
        assert _F["mh643_quota_hp_pct"](0.0, 0.0) == 0.0

    def test_sensibilita(self):
        p = _F["mh643_demo"]()
        righe = _F["mh643_sensibilita"](p, [50.0, 55.0], [90.0, 100.0])
        assert len(righe) == 4
        r = righe[1]
        assert r["prezzo_calore_eur_mwh"] == 50.0
        assert r["prezzo_energia_eur_mwh"] == 100.0
        assert set(r.keys()) == {"prezzo_calore_eur_mwh",
                                 "prezzo_energia_eur_mwh",
                                 "margine_annuo_eur", "verdetto"}
        assert righe[2]["margine_annuo_eur"] == pytest.approx(MA_DEMO)

    def test_demo_calcoli_completi(self):
        d = _F["mh643_demo_calcoli"](_F["mh643_demo"]())
        assert d["calore_scartato_mwh"] == pytest.approx(QS_DEMO)
        assert d["calore_venduto_mwh"] == pytest.approx(QV_DEMO)
        assert d["energia_pdc_mwh"] == pytest.approx(EH_DEMO)
        assert d["ricavi_calore_eur"] == pytest.approx(RIC_DEMO)
        assert d["costo_energia_hp_eur"] == pytest.approx(CHP_DEMO)
        assert d["margine_annuo_eur"] == pytest.approx(MA_DEMO)
        assert d["costo_netto_eur_mwh"] == pytest.approx(CN_DEMO)
        assert d["risparmio_vs_benchmark_eur"] == pytest.approx(RS_DEMO)
        assert d["copertura_pct"] == pytest.approx(COP_DEMO)
        assert d["van_eur"] == pytest.approx(VAN_DEMO)
        assert d["tir"] == pytest.approx(TIR_DEMO)
        assert d["payback_anni"] == PB_DEMO
        assert d["verdetto"] == "CONVIENTE"
        assert d["quota_hp_pct"] == pytest.approx(QP_DEMO)

    def test_demo_degenere(self):
        p = _F["mh643_demo"]()
        p["p_it_mw"] = 0.0
        d = _F["mh643_demo_calcoli"](p)
        assert d["calore_venduto_mwh"] == 0.0
        assert d["costo_netto_eur_mwh"] is None
        assert d["risparmio_vs_benchmark_eur"] is None
        assert d["verdetto"] == "NON_CALCOLABILE"


class TestRegistrazione:
    def _src(self):
        return (Path(__file__).resolve().parent.parent
                / "app.py").read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W643 (22/10/2026)")[1].split(
            "# W641 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab643:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 676
        assert TITLE643 in titles

    def test_registrazione(self):
        assert f'"{TITLE643}"' in self._src()
        assert ", tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676 = st.tabs([" in self._src()
        assert "with tab643:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st643_[a-z0-9_]+", self._ui()))
        attese = {"st643_pit", "st643_pue", "st643_eta", "st643_cop",
                  "st643_pcal", "st643_pene", "st643_bench", "st643_dom",
                  "st643_capex", "st643_opex", "st643_tasso", "st643_anni",
                  "st643_toll", "st643_sens", "st643_go", "st643_fig1",
                  "st643_fig2", "st643_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st643_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
