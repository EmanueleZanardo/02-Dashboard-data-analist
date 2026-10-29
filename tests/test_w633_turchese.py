"""Test tab633 "🔷 Idrogeno turchese: la pirolisi del metano".

Demo calcolata a mano: impianto pilota 500 t H2/anno.
CH4/t H2 = 16,043/4,032/0,95 = 4,188335421888054;
metano 500 x 4,188335421888054 = 2.094,167710944027 t;
carbonio 500 x 12,011/4,032 x 0,9 = 1.340,513392857143 t;
energia 500 x 15 = 7.500 MWh; metano 2094,167710944027 x 15,3 x 40 =
1.281.630,6390977446; elettricita' 7500 x 80 = 600.000;
CRF(7 %, 20 a) = 0,09439292574325567; capex 60.000 x 500 = 30.000.000;
capitale annuo = 30M x CRF + 30M x 4 % = 4.031.787,77229767;
CO2 evitata = 500 x 9,5 - 2094,167710944027 x 1,0 = 2.655,832289055973 t;
carbon black 1340,513392857143 x 300 = 402.154,01785714284;
valore CO2 2655,832289055973 x 95 = 252.304,06746031743;
LCOH = (4.031.787,77229767 + 1.281.630,6390977446 + 600.000
        - 402.154,01785714284 - 252.304,06746031743) / 500
     = 10.517,92065215591 €/t vs grigio 6.000 -> NON_CONVIENTE
(gap 4.517,92); margine = (6.000 - 10.517,92065215591) x 500 =
-2.258.960,326077955 -> payback None.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh633_num", "mh633_nneg", "mh633_pos", "mh633_frac01",
           "mh633_ch4_per_h2_t", "mh633_metano_annuo_t",
           "mh633_carbonio_annuo_t", "mh633_energia_annua_mwh",
           "mh633_costo_metano_annuo", "mh633_costo_elettricita_annua",
           "mh633_crf", "mh633_capex_totale", "mh633_capitale_annuo",
           "mh633_co2_evitata_t", "mh633_ricavo_carbonio",
           "mh633_valore_co2", "mh633_lcoh_netto_eur_t",
           "mh633_verdetto", "mh633_gap_pareggio",
           "mh633_margine_vs_grigio", "mh633_payback_anni",
           "mh633_sensibilita", "mh633_demo")

TITLE633 = "🔷 Idrogeno turchese: la pirolisi del metano"

DEMO = _F["mh633_demo"]()
CH4PH_DEMO = 4.188335421888054
MET_DEMO = 2094.167710944027
CAR_DEMO = 1340.513392857143
EN_DEMO = 7500.0
CM_DEMO = 1281630.6390977446
CE_DEMO = 600000.0
CRF_DEMO = 0.09439292574325567
CXT_DEMO = 30000000.0
CAP_DEMO = 4031787.77229767
CO2_DEMO = 2655.832289055973
RIC_DEMO = 402154.01785714284
VAL_DEMO = 252304.06746031743
LCOH_DEMO = 10517.92065215591
GAP_DEMO = 4517.92065215591
MG_DEMO = -2258960.326077955


class TestW633Validatori:
    def test_num(self):
        assert _F["mh633_num"](3, "x") == 3.0
        for bad in (True, "2", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh633_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh633_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh633_nneg"](-0.1, "x")
        assert _F["mh633_pos"](0.1, "x") == 0.1
        with pytest.raises(ValueError):
            _F["mh633_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh633_frac01"](1, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh633_frac01"](1.01, "x")
        with pytest.raises(ValueError):
            _F["mh633_frac01"](-0.01, "x")


class TestW633Stechiometria:
    def test_ch4_per_h2(self):
        assert _F["mh633_ch4_per_h2_t"](1.0) == pytest.approx(
            16.043 / 4.032)
        assert _F["mh633_ch4_per_h2_t"](0.95) == pytest.approx(
            CH4PH_DEMO)
        with pytest.raises(ValueError):
            _F["mh633_ch4_per_h2_t"](1.5)
        with pytest.raises(ValueError):
            _F["mh633_ch4_per_h2_t"](0.0)

    def test_metano_carbonio(self):
        assert _F["mh633_metano_annuo_t"](500.0, CH4PH_DEMO) == \
            pytest.approx(MET_DEMO)
        assert _F["mh633_carbonio_annuo_t"](500.0, 0.90) == \
            pytest.approx(CAR_DEMO)
        assert _F["mh633_carbonio_annuo_t"](0.0, 0.9) == 0.0

    def test_energia(self):
        assert _F["mh633_energia_annua_mwh"](500.0, 15.0) == \
            pytest.approx(EN_DEMO)
        assert _F["mh633_costo_metano_annuo"](MET_DEMO, 40.0) == \
            pytest.approx(CM_DEMO)
        assert _F["mh633_costo_elettricita_annua"](EN_DEMO, 80.0) == \
            pytest.approx(CE_DEMO)


class TestW633Finanza:
    def test_crf(self):
        assert _F["mh633_crf"](7.0, 20.0) == pytest.approx(CRF_DEMO)
        assert _F["mh633_crf"](0.0, 10.0) == pytest.approx(0.1)

    def test_capex_capitale(self):
        assert _F["mh633_capex_totale"](60000.0, 500.0) == \
            pytest.approx(CXT_DEMO)
        assert _F["mh633_capitale_annuo"](CXT_DEMO, CRF_DEMO, 4.0) == \
            pytest.approx(CAP_DEMO)

    def test_co2_ricavi(self):
        assert _F["mh633_co2_evitata_t"](500.0, 9.5, MET_DEMO, 1.0) == \
            pytest.approx(CO2_DEMO)
        # upstream dominante -> CO2 evitata negativa (non vietata)
        assert _F["mh633_co2_evitata_t"](100.0, 9.5, 2000.0, 1.0) < 0.0
        assert _F["mh633_ricavo_carbonio"](CAR_DEMO, 300.0) == \
            pytest.approx(RIC_DEMO)
        assert _F["mh633_valore_co2"](CO2_DEMO, 95.0) == \
            pytest.approx(VAL_DEMO)
        assert _F["mh633_valore_co2"](-100.0, 95.0) == pytest.approx(
            -9500.0)


class TestW633Lcoh:
    def test_demo(self):
        lcoh = _F["mh633_lcoh_netto_eur_t"](CAP_DEMO, CM_DEMO, CE_DEMO,
                                            RIC_DEMO, VAL_DEMO, 500.0)
        assert lcoh == pytest.approx(LCOH_DEMO)
        assert _F["mh633_verdetto"](lcoh, 6000.0) == "NON_CONVIENTE"
        assert _F["mh633_gap_pareggio"](lcoh, 6000.0) == pytest.approx(
            GAP_DEMO)
        assert _F["mh633_margine_vs_grigio"](6000.0, lcoh,
                                             500.0) == pytest.approx(
            MG_DEMO)
        assert _F["mh633_payback_anni"](CXT_DEMO, MG_DEMO) is None

    def test_degenere(self):
        assert _F["mh633_lcoh_netto_eur_t"](1.0, 1.0, 1.0, 0.0, 0.0,
                                            0.0) is None
        assert _F["mh633_verdetto"](None, 6000.0) == "NON_CALCOLABILE"
        assert _F["mh633_gap_pareggio"](None, 6000.0) is None
        assert _F["mh633_margine_vs_grigio"](6000.0, None,
                                             500.0) is None
        assert _F["mh633_payback_anni"](100.0, None) is None

    def test_verdetti(self):
        assert _F["mh633_verdetto"](5000.0, 6000.0) == "CONVIENTE"
        assert _F["mh633_verdetto"](6000.0, 6000.0) == "CONVIENTE"
        assert _F["mh633_verdetto"](6500.0, 6000.0) == "MARGINALE"
        assert _F["mh633_verdetto"](6899.0, 6000.0) == "MARGINALE"
        # nota: 6000.0 * 1.15 = 6899.999... in float, quindi 6900.0 e'
        # gia' oltre la soglia
        assert _F["mh633_verdetto"](6900.0, 6000.0) == "NON_CONVIENTE"
        assert _F["mh633_verdetto"](6901.0, 6000.0) == "NON_CONVIENTE"

    def test_payback_positivo(self):
        assert _F["mh633_payback_anni"](1000000.0, 250000.0) == \
            pytest.approx(4.0)
        assert _F["mh633_payback_anni"](1000000.0, 0.0) is None


class TestW633Sensibilita:
    def _righe(self):
        return _F["mh633_sensibilita"](
            500.0, 0.95, 0.90, 15.0, 60000.0, 0.0, 7.0, 20.0, 4.0,
            300.0, 9.5, 1.0, 95.0, 6000.0, [40.0, 80.0], [80.0])

    def test_griglia(self):
        righe = self._righe()
        assert len(righe) == 2
        assert righe[0]["p_metano_eur_mwh"] == pytest.approx(40.0)
        assert righe[0]["lcoh_netto_eur_t"] == pytest.approx(
            LCOH_DEMO)
        assert righe[0]["verdetto"] == "NON_CONVIENTE"
        assert righe[1]["lcoh_netto_eur_t"] > LCOH_DEMO

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh633_sensibilita"](
                500.0, 0.95, 0.90, 15.0, 60000.0, 0.0, 7.0, 20.0, 4.0,
                300.0, 9.5, 1.0, 95.0, 6000.0, [], [80.0])

    def test_contributo_over(self):
        with pytest.raises(ValueError):
            _F["mh633_sensibilita"](
                500.0, 0.95, 0.90, 15.0, 60000.0, 150.0, 7.0, 20.0,
                4.0, 300.0, 9.5, 1.0, 95.0, 6000.0, [40.0], [80.0])


class TestW633Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab633:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 792
        assert TITLE633 in titles
        assert TITLE633 in titles

    def test_chain(self):
        assert ", tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792 = st.tabs([" in self._src()
        assert "with tab633:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st633_[a-z0-9_]+", self._ui()))
        attese = {"st633_h2", "st633_eta", "st633_resa", "st633_kwh",
                  "st633_pmet", "st633_pel", "st633_capex", "st633_sub",
                  "st633_tasso", "st633_anni", "st633_ox",
                  "st633_pcarbon", "st633_ef", "st633_up",
                  "st633_pco2", "st633_pgrigio", "st633_sens",
                  "st633_go", "st633_fig", "st633_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st633_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W633 (22/10/2026)')[1]
        sec = sec.split('# W632 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
