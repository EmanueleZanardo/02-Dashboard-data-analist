"""Test tab635 "🏛️🎯 Aste FER-X: a che strike conviene partecipare?".

Demo calcolata a mano: FV 10 MW, 1400 ore equivalenti, disponibilita' 98 %.
Energia 10 x 1400 x 0,98 = 13.720 MWh/anno;
catturato 85 x (1 - 0,08) = 78,20 €/MWh;
margine CfD (68 - 62) x 13720 = 82.320 €/anno;
margine merchant (78,2 - 62) x 13720 = 222.264 €/anno;
premio copertura 68 - 78,2 = -10,20 €/MWh;
strike pareggio 62 x 1,10 = 68,20 €/MWh;
P(vittoria) = 1/(1+exp((68-72)/6)) = 0,6607563687658172;
valore atteso = 0,6607563687658172 x 82320
    + 0,3392436312341828 x 222264 = 129.795,11072943648 €/anno;
rendita (6 %, 20 a) = 11,469921218565263;
VAN = 129795,11072943648 x 11,469921218565263 = 1.488.739,6946215914 €;
strike a massimo valore atteso su [43,4, 93,0] passo 0,5 = 84,90
    -> 231.854,54335399112 €/anno;
verdetto: strike 68 < pareggio 68,20 ma margine CfD > 0 -> VALUTA.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh635_num", "mh635_nneg", "mh635_pos", "mh635_frac01",
           "mh635_energia_annua_mwh", "mh635_prezzo_catturato_eur_mwh",
           "mh635_margine_cfd_annuo", "mh635_margine_merchant_annuo",
           "mh635_premio_copertura_mwh", "mh635_strike_pareggio",
           "mh635_prob_aggiudicazione", "mh635_valore_atteso_annuo",
           "mh635_fattore_rendita", "mh635_van_valore_atteso",
           "mh635_strike_massimo_va", "mh635_verdetto",
           "mh635_sensibilita", "mh635_demo")

TITLE635 = "🏛️🎯 Aste FER-X: a che strike conviene partecipare?"

DEMO = _F["mh635_demo"]()
MWH_DEMO = 13720.0
CAT_DEMO = 78.2
MC_DEMO = 82320.0
MM_DEMO = 222264.00000000003
PREMIO_DEMO = -10.200000000000003
PAREGGIO_DEMO = 68.2
PROB_DEMO = 0.6607563687658172
VA_DEMO = 129795.11072943648
FR_DEMO = 11.469921218565263
VAN_DEMO = 1488739.6946215914
BEST_STRIKE_DEMO = 84.9
BEST_VA_DEMO = 231854.54335399112


class TestW635Validatori:
    def test_num(self):
        assert _F["mh635_num"](3, "x") == 3.0
        for bad in (True, "2", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh635_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh635_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh635_nneg"](-0.1, "x")
        assert _F["mh635_pos"](0.1, "x") == 0.1
        with pytest.raises(ValueError):
            _F["mh635_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh635_frac01"](0.98, "x") == 0.98
        for bad in (-0.01, 1.01):
            with pytest.raises(ValueError):
                _F["mh635_frac01"](bad, "x")


class TestW635Fisica:
    def test_energia(self):
        assert _F["mh635_energia_annua_mwh"](10.0, 1400.0, 0.98) == \
            pytest.approx(MWH_DEMO)
        assert _F["mh635_energia_annua_mwh"](10.0, 1400.0, 0.0) == \
            pytest.approx(0.0)
        with pytest.raises(ValueError):
            _F["mh635_energia_annua_mwh"](-1.0, 1400.0, 0.98)
        with pytest.raises(ValueError):
            _F["mh635_energia_annua_mwh"](10.0, 1400.0, 1.5)

    def test_catturato(self):
        assert _F["mh635_prezzo_catturato_eur_mwh"](85.0, 8.0) == \
            pytest.approx(CAT_DEMO)
        assert _F["mh635_prezzo_catturato_eur_mwh"](85.0, 0.0) == \
            pytest.approx(85.0)
        with pytest.raises(ValueError):
            _F["mh635_prezzo_catturato_eur_mwh"](85.0, 100.0)
        with pytest.raises(ValueError):
            _F["mh635_prezzo_catturato_eur_mwh"](-5.0, 8.0)


class TestW635Margini:
    def test_margini_demo(self):
        assert _F["mh635_margine_cfd_annuo"](68.0, 62.0, MWH_DEMO) == \
            pytest.approx(MC_DEMO)
        assert _F["mh635_margine_merchant_annuo"](CAT_DEMO, 62.0,
                                                 MWH_DEMO) == \
            pytest.approx(MM_DEMO)
        assert _F["mh635_premio_copertura_mwh"](68.0, CAT_DEMO) == \
            pytest.approx(PREMIO_DEMO)
        assert _F["mh635_strike_pareggio"](62.0, 10.0) == \
            pytest.approx(PAREGGIO_DEMO)

    def test_margini_negativi(self):
        assert _F["mh635_margine_cfd_annuo"](50.0, 62.0, MWH_DEMO) < 0.0
        assert _F["mh635_premio_copertura_mwh"](90.0, CAT_DEMO) > 0.0
        assert _F["mh635_strike_pareggio"](62.0, 0.0) == pytest.approx(62.0)


class TestW635Probabilita:
    def test_demo(self):
        assert _F["mh635_prob_aggiudicazione"](68.0, 72.0, 6.0) == \
            pytest.approx(PROB_DEMO)

    def test_mediano(self):
        assert _F["mh635_prob_aggiudicazione"](72.0, 72.0, 6.0) == \
            pytest.approx(0.5)

    def test_monotona(self):
        p_basso = _F["mh635_prob_aggiudicazione"](60.0, 72.0, 6.0)
        p_alto = _F["mh635_prob_aggiudicazione"](90.0, 72.0, 6.0)
        assert p_basso > PROB_DEMO > p_alto
        assert 0.0 < p_alto < 1.0

    def test_dispersione_invalida(self):
        with pytest.raises(ValueError):
            _F["mh635_prob_aggiudicazione"](68.0, 72.0, 0.0)


class TestW635ValoreAtteso:
    def test_demo(self):
        assert _F["mh635_valore_atteso_annuo"](PROB_DEMO, MC_DEMO,
                                               MM_DEMO) == \
            pytest.approx(VA_DEMO)
        assert _F["mh635_fattore_rendita"](6.0, 20.0) == pytest.approx(
            FR_DEMO)
        assert _F["mh635_fattore_rendita"](0.0, 20.0) == pytest.approx(20.0)
        assert _F["mh635_van_valore_atteso"](VA_DEMO, 6.0, 20.0) == \
            pytest.approx(VAN_DEMO)

    def test_strike_massimo_va(self):
        s, va = _F["mh635_strike_massimo_va"](62.0, CAT_DEMO, MWH_DEMO,
                                              72.0, 6.0)
        assert s == pytest.approx(BEST_STRIKE_DEMO)
        assert va == pytest.approx(BEST_VA_DEMO)

    def test_valore_atteso_estremi(self):
        # P = 1 -> tutto CfD; P = 0 -> tutto merchant
        assert _F["mh635_valore_atteso_annuo"](1.0, 100.0, 50.0) == \
            pytest.approx(100.0)
        assert _F["mh635_valore_atteso_annuo"](0.0, 100.0, 50.0) == \
            pytest.approx(50.0)


class TestW635Verdetti:
    def test_demo_valuta(self):
        assert _F["mh635_verdetto"](68.0, 62.0, PAREGGIO_DEMO, VA_DEMO,
                                    MC_DEMO, MWH_DEMO) == "VALUTA"

    def test_partecipa(self):
        mc = _F["mh635_margine_cfd_annuo"](70.0, 62.0, MWH_DEMO)
        va = _F["mh635_valore_atteso_annuo"](0.5, mc, MM_DEMO)
        assert _F["mh635_verdetto"](70.0, 62.0, PAREGGIO_DEMO, va, mc,
                                    MWH_DEMO) == "PARTECIPA"

    def test_non_partecipare_sotto_costo(self):
        mc = _F["mh635_margine_cfd_annuo"](60.0, 62.0, MWH_DEMO)
        va = _F["mh635_valore_atteso_annuo"](0.9, mc, MM_DEMO)
        assert _F["mh635_verdetto"](60.0, 62.0, PAREGGIO_DEMO, va, mc,
                                    MWH_DEMO) == "NON_PARTECIPARE"

    def test_non_calcolabile(self):
        assert _F["mh635_verdetto"](68.0, 62.0, PAREGGIO_DEMO, 0.0, 0.0,
                                    0.0) == "NON_CALCOLABILE"


class TestW635Sensibilita:
    def _righe(self):
        return _F["mh635_sensibilita"](
            10.0, 1400.0, 0.98, 8.0, 62.0, 72.0, 6.0, 10.0,
            [68.0], [85.0, 68.0])

    def test_griglia(self):
        righe = self._righe()
        assert len(righe) == 2
        assert righe[0]["strike_eur_mwh"] == pytest.approx(68.0)
        assert righe[0]["baseload_eur_mwh"] == pytest.approx(85.0)
        assert righe[0]["catturato_eur_mwh"] == pytest.approx(CAT_DEMO)
        assert righe[0]["prob_vittoria"] == pytest.approx(PROB_DEMO)
        assert righe[0]["valore_atteso_eur_anno"] == pytest.approx(VA_DEMO)
        assert righe[0]["verdetto"] == "VALUTA"
        assert righe[1]["baseload_eur_mwh"] == pytest.approx(68.0)
        assert righe[1]["catturato_eur_mwh"] == pytest.approx(62.56)

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh635_sensibilita"](
                10.0, 1400.0, 0.98, 8.0, 62.0, 72.0, 6.0, 10.0, [], [85.0])
        with pytest.raises(ValueError):
            _F["mh635_sensibilita"](
                10.0, 1400.0, 0.98, 8.0, 62.0, 72.0, 6.0, 10.0, [68.0], [])


class TestW635Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab635:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 813
        assert TITLE635 in titles
        assert TITLE635 in titles

    def test_chain(self):
        assert ", tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813 = st.tabs([" in self._src()
        assert "with tab635:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st635_[a-z0-9_]+", self._ui()))
        attese = {"st635_mw", "st635_ore", "st635_disp", "st635_base",
                  "st635_sconto", "st635_lcoe", "st635_strike", "st635_med",
                  "st635_sigma", "st635_target", "st635_tasso", "st635_anni",
                  "st635_sens", "st635_go", "st635_fig", "st635_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st635_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W635 (22/10/2026)')[1]
        sec = sec.split('# W634 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
