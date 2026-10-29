"""Test tab636 "🩷 Idrogeno rosa: l'elettrolisi alimentata dal nucleare".

Demo calcolata a mano: elettrolizzatore 50 MW, CF 92 %, efficienza
55 kWh/kg; CAPEX 1,2 M€/MW (60 M€), OPEX 3 %/anno, tasso 6 %, 25 anni;
PPA nucleare 70 €/MWh; mercato H2 6,50 €/kg, grigio SMR 2,00 €/kg,
CO2 evitata 0,0095 tCO2/kg.
MWh elettrici 50 x 8760 x 0,92 = 402.960 MWh/anno;
kg H2 402960 x 1000 / 55 = 7.326.545,4545454545 kg/anno;
CRF(6 %, 25 a) = 0,06 x 1,06^25 / (1,06^25 - 1) = 0,07822671821227395;
CAPEX annuo 60e6 x 0,07822671821227395 = 4.693.603,092736437 €/anno;
OPEX annuo 60e6 x 0,03 = 1.800.000 €/anno;
energia 402960 x 70 = 28.207.200 €/anno;
totale 34.700.803,09273644 €/anno;
LCOH 34700803,09273644 / 7326545,454545454 = 4,736311718534108 €/kg;
quota energia 28207200 / 34700803,09273644 x 100 = 81,28687951289612 %;
green premium 4,736311718534108 - 2,00 = 2,7363117185341084 €/kg;
CO2 di pareggio 2,7363117185341084 / 0,0095 = 288,03281247727455 €/t;
verdetto: LCOH 4,7363 <= mercato 6,50 -> COMPETITIVO.
Sensibilita': CF 0,85 x prezzo 70 -> LCOH 4,809302095354564 €/kg.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh636_num", "mh636_nneg", "mh636_pos", "mh636_frac01",
           "mh636_mwh_elettrici_annui", "mh636_kg_h2_annui",
           "mh636_crf", "mh636_capex_annuo", "mh636_opex_annuo",
           "mh636_costo_energia_annuo", "mh636_lcoh_eur_kg",
           "mh636_quota_energia_pct", "mh636_premium_vs_grigio_eur_kg",
           "mh636_co2_pareggio_eur_t", "mh636_verdetto",
           "mh636_sensibilita", "mh636_demo")

TITLE636 = "🩷 Idrogeno rosa: l'elettrolisi alimentata dal nucleare"

MWH_DEMO = 402960.0
KG_DEMO = 7326545.454545454
CRF_DEMO = 0.07822671821227395
CAPEX_ANN_DEMO = 4693603.092736437
OPEX_DEMO = 1800000.0
EN_DEMO = 28207200.0
LCOH_DEMO = 4.736311718534108
QUOTA_DEMO = 81.28687951289612
PREM_DEMO = 2.7363117185341084
CO2_DEMO = 288.03281247727455
LCOH_CF85 = 4.809302095354564


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh636_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh636_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh636_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh636_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh636_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh636_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh636_frac01"](1.0, "x") == 1.0
        for bad in (-0.01, 1.01):
            with pytest.raises(ValueError):
                _F["mh636_frac01"](bad, "x")


class TestCore:
    def test_mwh_demo(self):
        assert _F["mh636_mwh_elettrici_annui"](50.0, 0.92) == MWH_DEMO

    def test_kg_demo(self):
        assert _F["mh636_kg_h2_annui"](MWH_DEMO, 55.0) == pytest.approx(
            KG_DEMO, rel=1e-12)

    def test_crf_demo(self):
        assert _F["mh636_crf"](6.0, 25.0) == pytest.approx(
            CRF_DEMO, rel=1e-12)

    def test_crf_tasso_zero(self):
        assert _F["mh636_crf"](0.0, 25.0) == pytest.approx(1.0 / 25.0)

    def test_costi_annui_demo(self):
        assert _F["mh636_capex_annuo"](1200000.0, 50.0, 6.0, 25.0) == \
            pytest.approx(CAPEX_ANN_DEMO, rel=1e-12)
        assert _F["mh636_opex_annuo"](1200000.0, 50.0, 3.0) == OPEX_DEMO
        assert _F["mh636_costo_energia_annuo"](MWH_DEMO, 70.0) == EN_DEMO

    def test_lcoh_demo(self):
        assert _F["mh636_lcoh_eur_kg"](CAPEX_ANN_DEMO, OPEX_DEMO, EN_DEMO,
                                       KG_DEMO) == pytest.approx(
            LCOH_DEMO, rel=1e-12)

    def test_lcoh_produzione_nulla(self):
        with pytest.raises(ValueError):
            _F["mh636_lcoh_eur_kg"](1.0, 1.0, 1.0, 0.0)

    def test_quota_energia_demo(self):
        assert _F["mh636_quota_energia_pct"](EN_DEMO, CAPEX_ANN_DEMO,
                                             OPEX_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=1e-12)

    def test_premium_e_co2_demo(self):
        assert _F["mh636_premium_vs_grigio_eur_kg"](
            LCOH_DEMO, 2.0) == pytest.approx(PREM_DEMO, rel=1e-12)
        assert _F["mh636_co2_pareggio_eur_t"](
            PREM_DEMO, 0.0095) == pytest.approx(CO2_DEMO, rel=1e-12)

    def test_co2_gia_competitivo(self):
        assert _F["mh636_co2_pareggio_eur_t"](-0.5, 0.0095) == 0.0
        assert _F["mh636_co2_pareggio_eur_t"](0.0, 0.0095) == 0.0


class TestVerdetto:
    def test_competitivo_demo(self):
        assert _F["mh636_verdetto"](LCOH_DEMO, 6.50, 20.0,
                                    KG_DEMO) == "COMPETITIVO"

    def test_premium_accettabile(self):
        assert _F["mh636_verdetto"](7.0, 6.50, 20.0,
                                    KG_DEMO) == "PREMIUM_ACCETTABILE"

    def test_non_competitivo(self):
        assert _F["mh636_verdetto"](9.0, 6.50, 20.0,
                                    KG_DEMO) == "NON_COMPETITIVO"

    def test_non_calcolabile(self):
        assert _F["mh636_verdetto"](4.0, 6.50, 20.0,
                                    0.0) == "NON_CALCOLABILE"


class TestSensibilita:
    def test_shape_e_valori(self):
        righe = _F["mh636_sensibilita"](
            50.0, 55.0, 1200000.0, 3.0, 6.0, 25.0,
            [0.85, 0.92], [60.0, 70.0, 80.0],
            6.50, 2.00, 20.0, 0.0095)
        assert len(righe) == 6
        r0 = righe[0]
        assert r0["capacity_factor"] == 0.85
        assert r0["prezzo_energia_eur_mwh"] == 60.0
        r1 = [r for r in righe
              if r["capacity_factor"] == 0.85
              and r["prezzo_energia_eur_mwh"] == 70.0][0]
        assert r1["lcoh_eur_kg"] == pytest.approx(LCOH_CF85, rel=1e-12)
        assert all(r["verdetto"] in
                   ("COMPETITIVO", "PREMIUM_ACCETTABILE",
                    "NON_COMPETITIVO") for r in righe)

    def test_liste_vuote(self):
        for cf, pl in ([], [70.0]), ([0.9], []):
            with pytest.raises(ValueError):
                _F["mh636_sensibilita"](
                    50.0, 55.0, 1200000.0, 3.0, 6.0, 25.0, cf, pl,
                    6.50, 2.00, 20.0, 0.0095)

    def test_demo_defaults(self):
        d = _F["mh636_demo"]()
        assert d["potenza_mw"] == 50.0
        assert d["capacity_factor"] == 0.92
        assert d["emissioni_tco2_per_kg"] == 0.0095


class TestUI636:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W636 (22/10/2026)")[1].split(
            "# W635 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab636:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 789
        assert TITLE636 in titles

    def test_registrazione(self):
        assert f'"{TITLE636}"' in self._src()
        assert ", tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789 = st.tabs([" in self._src()
        assert "with tab636:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st636_[a-z0-9_]+", self._ui()))
        attese = {"st636_pw", "st636_cf", "st636_eff", "st636_capex",
                  "st636_opex", "st636_pel", "st636_tasso", "st636_anni",
                  "st636_tol", "st636_pmerc", "st636_pgrigio", "st636_emis",
                  "st636_sens", "st636_go", "st636_fig", "st636_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st636_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
