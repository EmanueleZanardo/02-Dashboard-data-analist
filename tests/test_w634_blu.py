"""Test tab634 "🔵 Idrogeno blu: il reforming con cattura CO2 (SMR+CCS)".

Demo calcolata a mano: impianto SMR+CCS 10.000 t H2/anno.
CH4/t H2 = 16,043/4,032/0,75 = 5,305224867724868;
metano 10000 x 5,305224867724868 = 53.052,24867724868 t;
CO2 prodotta 53052,24867724868 x 2,7444 = 145.596,5912698413 t;
catturata x 0,90 = 131.036,93214285717 t; emessa = 14.559,659126984126 t;
energia 10000 x 8 = 80.000 MWh; metano 53052,24867724868 x 15,3 x 40 =
32.467.976,190476194; elettricita' 80000 x 80 = 6.400.000;
CRF(7 %, 20 a) = 0,09439292574325567; capex 25.000 x 10000 = 250.000.000;
capitale annuo = 250M x CRF + 250M x 5 % = 36.098.231,43581392;
ETS residua 14559,659126984126 x 95 = 1.383.167,617063492;
stoccaggio 131036,93214285717 x 50 = 6.551.846,607142858;
LCOH = (36.098.231,43581392 + 32.467.976,190476194 + 6.400.000
        + 1.383.167,617063492 + 6.551.846,607142858) / 10000
     = 8.290,122185049648 €/t (8,29 €/kg) vs grigio 4.500 -> NON_CONVIENTE
(gap 3.790,12); margine = (4.500 - 8.290,122185049648) x 10000 =
-37.901.221,85049648 -> payback None; quota cattura 0,90.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh634_num", "mh634_nneg", "mh634_pos", "mh634_frac01",
           "mh634_ch4_per_h2_t", "mh634_metano_annuo_t",
           "mh634_co2_prodotta_t", "mh634_co2_catturata_t",
           "mh634_co2_emessa_t", "mh634_energia_annua_mwh",
           "mh634_costo_metano_annuo", "mh634_costo_elettricita_annua",
           "mh634_crf", "mh634_capex_totale", "mh634_capitale_annuo",
           "mh634_costo_co2_emessa", "mh634_costo_stoccaggio",
           "mh634_lcoh_blu_eur_t", "mh634_verdetto",
           "mh634_gap_pareggio", "mh634_margine_vs_grigio",
           "mh634_payback_anni", "mh634_quota_cattura",
           "mh634_sensibilita", "mh634_demo")

TITLE634 = "🔵 Idrogeno blu: il reforming con cattura CO2 (SMR+CCS)"

DEMO = _F["mh634_demo"]()
CH4PH_DEMO = 5.305224867724868
MET_DEMO = 53052.24867724868
CO2P_DEMO = 145596.5912698413
CO2C_DEMO = 131036.93214285717
CO2E_DEMO = 14559.659126984126
EN_DEMO = 80000.0
CM_DEMO = 32467976.190476194
CE_DEMO = 6400000.0
CRF_DEMO = 0.09439292574325567
CXT_DEMO = 250000000.0
CAP_DEMO = 36098231.43581392
CCO2_DEMO = 1383167.617063492
CST_DEMO = 6551846.607142858
LCOH_DEMO = 8290.122185049648
GAP_DEMO = 3790.1221850496477
MG_DEMO = -37901221.85049648


class TestW634Validatori:
    def test_num(self):
        assert _F["mh634_num"](3, "x") == 3.0
        for bad in (True, "2", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh634_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh634_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh634_nneg"](-0.1, "x")
        assert _F["mh634_pos"](0.1, "x") == 0.1
        with pytest.raises(ValueError):
            _F["mh634_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh634_frac01"](0.9, "x") == 0.9
        for bad in (-0.01, 1.01):
            with pytest.raises(ValueError):
                _F["mh634_frac01"](bad, "x")


class TestW634Stechiometria:
    def test_ch4_per_h2(self):
        assert _F["mh634_ch4_per_h2_t"](1.0) == pytest.approx(
            16.043 / 4.032)
        assert _F["mh634_ch4_per_h2_t"](0.75) == pytest.approx(
            CH4PH_DEMO)
        with pytest.raises(ValueError):
            _F["mh634_ch4_per_h2_t"](1.5)
        with pytest.raises(ValueError):
            _F["mh634_ch4_per_h2_t"](0.0)

    def test_metano_co2(self):
        assert _F["mh634_metano_annuo_t"](10000.0, CH4PH_DEMO) == \
            pytest.approx(MET_DEMO)
        assert _F["mh634_co2_prodotta_t"](MET_DEMO) == pytest.approx(
            CO2P_DEMO)
        assert _F["mh634_co2_catturata_t"](CO2P_DEMO, 0.90) == \
            pytest.approx(CO2C_DEMO)
        assert _F["mh634_co2_emessa_t"](CO2P_DEMO, 0.90) == pytest.approx(
            CO2E_DEMO)
        # tasso zero -> tutta emessa
        assert _F["mh634_co2_emessa_t"](100.0, 0.0) == pytest.approx(100.0)
        assert _F["mh634_co2_catturata_t"](100.0, 0.0) == pytest.approx(0.0)

    def test_energia_costi(self):
        assert _F["mh634_energia_annua_mwh"](10000.0, 8.0) == pytest.approx(
            EN_DEMO)
        assert _F["mh634_costo_metano_annuo"](MET_DEMO, 40.0) == \
            pytest.approx(CM_DEMO)
        assert _F["mh634_costo_elettricita_annua"](EN_DEMO, 80.0) == \
            pytest.approx(CE_DEMO)


class TestW634Finanza:
    def test_crf(self):
        assert _F["mh634_crf"](7.0, 20.0) == pytest.approx(CRF_DEMO)
        assert _F["mh634_crf"](0.0, 10.0) == pytest.approx(0.1)

    def test_capex_capitale(self):
        assert _F["mh634_capex_totale"](25000.0, 10000.0) == \
            pytest.approx(CXT_DEMO)
        assert _F["mh634_capitale_annuo"](CXT_DEMO, CRF_DEMO, 5.0) == \
            pytest.approx(CAP_DEMO)

    def test_co2_stoccaggio(self):
        assert _F["mh634_costo_co2_emessa"](CO2E_DEMO, 95.0) == \
            pytest.approx(CCO2_DEMO)
        assert _F["mh634_costo_stoccaggio"](CO2C_DEMO, 50.0) == \
            pytest.approx(CST_DEMO)


class TestW634Lcoh:
    def test_demo(self):
        lcoh = _F["mh634_lcoh_blu_eur_t"](CAP_DEMO, CM_DEMO, CE_DEMO,
                                          CCO2_DEMO, CST_DEMO, 10000.0)
        assert lcoh == pytest.approx(LCOH_DEMO)
        assert _F["mh634_verdetto"](lcoh, 4500.0) == "NON_CONVIENTE"
        assert _F["mh634_gap_pareggio"](lcoh, 4500.0) == pytest.approx(
            GAP_DEMO)
        assert _F["mh634_margine_vs_grigio"](4500.0, lcoh,
                                             10000.0) == pytest.approx(
            MG_DEMO)
        assert _F["mh634_payback_anni"](CXT_DEMO, MG_DEMO) is None
        assert _F["mh634_quota_cattura"](CO2C_DEMO,
                                         CO2P_DEMO) == pytest.approx(0.90)

    def test_degenere(self):
        assert _F["mh634_lcoh_blu_eur_t"](1.0, 1.0, 1.0, 1.0, 1.0,
                                         0.0) is None
        assert _F["mh634_verdetto"](None, 4500.0) == "NON_CALCOLABILE"
        assert _F["mh634_gap_pareggio"](None, 4500.0) is None
        assert _F["mh634_margine_vs_grigio"](4500.0, None,
                                             10000.0) is None
        assert _F["mh634_payback_anni"](100.0, None) is None
        assert _F["mh634_quota_cattura"](0.0, 0.0) is None

    def test_verdetti(self):
        assert _F["mh634_verdetto"](4000.0, 4500.0) == "CONVIENTE"
        assert _F["mh634_verdetto"](4500.0, 4500.0) == "CONVIENTE"
        assert _F["mh634_verdetto"](5000.0, 4500.0) == "MARGINALE"
        # nota: 4500.0 * 1.15 = 5175.000000000001 in float, quindi
        # 5175.0 e' ancora entro la soglia MARGINALE
        assert _F["mh634_verdetto"](5175.0, 4500.0) == "MARGINALE"
        assert _F["mh634_verdetto"](5176.0, 4500.0) == "NON_CONVIENTE"

    def test_payback_positivo(self):
        assert _F["mh634_payback_anni"](1000000.0, 250000.0) == \
            pytest.approx(4.0)
        assert _F["mh634_payback_anni"](1000000.0, 0.0) is None


class TestW634Sensibilita:
    def _righe(self):
        return _F["mh634_sensibilita"](
            10000.0, 0.75, 0.90, 8.0, 80.0, 25000.0, 0.0, 7.0, 20.0,
            5.0, 50.0, 4500.0, [40.0], [95.0, 66.5])

    def test_griglia(self):
        righe = self._righe()
        assert len(righe) == 2
        assert righe[0]["p_gas_eur_mwh"] == pytest.approx(40.0)
        assert righe[0]["p_co2_eur_t"] == pytest.approx(95.0)
        assert righe[0]["lcoh_eur_t"] == pytest.approx(LCOH_DEMO)
        assert righe[0]["verdetto"] == "NON_CONVIENTE"
        assert righe[1]["lcoh_eur_t"] < LCOH_DEMO

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh634_sensibilita"](
                10000.0, 0.75, 0.90, 8.0, 80.0, 25000.0, 0.0, 7.0,
                20.0, 5.0, 50.0, 4500.0, [], [95.0])

    def test_contributo_over(self):
        with pytest.raises(ValueError):
            _F["mh634_sensibilita"](
                10000.0, 0.75, 0.90, 8.0, 80.0, 25000.0, 150.0, 7.0,
                20.0, 5.0, 50.0, 4500.0, [40.0], [95.0])


class TestW634Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab634:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 831
        assert TITLE634 in titles
        assert TITLE634 in titles

    def test_chain(self):
        assert ", tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827, tab828, tab829, tab830, tab831 = st.tabs([" in self._src()
        assert "with tab634:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st634_[a-z0-9_]+", self._ui()))
        attese = {"st634_h2", "st634_eta", "st634_catt", "st634_kwh",
                  "st634_pgas", "st634_pel", "st634_capex", "st634_sub",
                  "st634_tasso", "st634_anni", "st634_ox",
                  "st634_pco2", "st634_stoc", "st634_pgrigio",
                  "st634_sens", "st634_go", "st634_fig", "st634_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st634_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W634 (22/10/2026)')[1]
        sec = sec.split('# W633 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
