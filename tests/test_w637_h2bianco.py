"""Test tab637 "🤍 Idrogeno bianco: l'H2 naturale dal sottosuolo".

Demo calcolata a mano: 10 pozzi da 500 Nm3/h, purezza 90 %, disponibilita'
95 %; costo pozzo 2,0 M€ (20 M€), impianto 10 M€ (capex 30 M€), OPEX 4 %/anno,
tasso 7 %, 20 anni; energia purificazione+compressione 3 kWh/kg a
70 €/MWh; mercato H2 6,50 €/kg, grigio SMR 2,00 €/kg,
CO2 evitata 0,0095 tCO2/kg.
kg/h per pozzo 500 x 0,08988 x 0,90 = 40,446 kg/h; 10 pozzi = 404,46 kg/h;
kg/anno 404,46 x 8760 x 0,95 = 3.365.916,12 kg/anno;
CRF(7 %, 20 a) = 0,07 x 1,07^20 / (1,07^20 - 1) = 0,09439292574325567;
capitale annuo 30e6 x 0,09439292574325567 = 2.831.787,77229767 €/anno;
OPEX annuo 30e6 x 0,04 = 1.200.000 €/anno;
energia 3365916,12 x 3 x 70 / 1000 = 706.842,3852 €/anno;
totale 4.738.630,1574976705 €/anno;
LCOH 4738630,1574976705 / 3365916,12 = 1,4078277617618322 €/kg;
risorsa 3365916,12 x 20 = 67.318.322,4 kg;
margine (6,50 - 1,4078277617618322) x 3365916,12 = 17.139.824,62250233 €/a;
payback 30e6 / 17139824,62250233 = 1,7503096245578822 anni;
green premium 1,4078277617618322 - 2,00 = -0,5921722382381678 €/kg;
CO2 di pareggio: premium <= 0 -> 0,0 (gia' competitivo);
verdetto: LCOH 1,4078 <= mercato 6,50 -> COMPETITIVO.
Sensibilita': portata 450 x purezza 0,85 -> LCOH 1,6192091314845083 €/kg.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh637_num", "mh637_nneg", "mh637_pos", "mh637_frac01",
           "mh637_intero_pos", "mh637_kg_h2_annui", "mh637_capex_totale",
           "mh637_crf", "mh637_capitale_annuo", "mh637_opex_annuo",
           "mh637_costo_energia_annuo", "mh637_lcoh_eur_kg",
           "mh637_risorsa_totale_kg", "mh637_margine_annuo_eur",
           "mh637_payback_anni", "mh637_premium_vs_grigio_eur_kg",
           "mh637_co2_pareggio_eur_t", "mh637_verdetto",
           "mh637_sensibilita", "mh637_demo")

TITLE637 = "🤍 Idrogeno bianco: l'H2 naturale dal sottosuolo"

KG_DEMO = 3365916.12
CAPEX_DEMO = 30000000.0
CRF_DEMO = 0.09439292574325567
CAP_ANN_DEMO = 2831787.77229767
OPEX_DEMO = 1200000.0
EN_DEMO = 706842.3852
LCOH_DEMO = 1.4078277617618322
RISORSA_DEMO = 67318322.4
MARGINE_DEMO = 17139824.62250233
PAYBACK_DEMO = 1.7503096245578822
PREM_DEMO = -0.5921722382381678
LCOH_P450_PUR85 = 1.6192091314845083


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh637_num"](3, "x") == 3.0

    def test_num_bool_str_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"),
                    float("-inf"), None):
            with pytest.raises(ValueError):
                _F["mh637_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh637_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh637_nneg"](-1e-9, "x")

    def test_pos(self):
        assert _F["mh637_pos"](0.001, "x") > 0.0
        with pytest.raises(ValueError):
            _F["mh637_pos"](0.0, "x")

    def test_frac01(self):
        assert _F["mh637_frac01"](1.0, "x") == 1.0
        for bad in (-0.01, 1.01):
            with pytest.raises(ValueError):
                _F["mh637_frac01"](bad, "x")

    def test_intero_pos(self):
        assert _F["mh637_intero_pos"](10, "x") == 10
        assert _F["mh637_intero_pos"](10.0, "x") == 10
        for bad in (0, -3, 2.5, True):
            with pytest.raises(ValueError):
                _F["mh637_intero_pos"](bad, "x")


class TestCore:
    def test_kg_demo(self):
        assert _F["mh637_kg_h2_annui"](10, 500.0, 0.90, 0.95) == \
            pytest.approx(KG_DEMO, rel=1e-12)

    def test_kg_purezza_zero(self):
        assert _F["mh637_kg_h2_annui"](10, 500.0, 0.0, 0.95) == 0.0

    def test_capex_demo(self):
        assert _F["mh637_capex_totale"](10, 2000000.0, 10000000.0) == \
            CAPEX_DEMO

    def test_crf_demo(self):
        assert _F["mh637_crf"](7.0, 20.0) == pytest.approx(
            CRF_DEMO, rel=1e-12)

    def test_crf_tasso_zero(self):
        assert _F["mh637_crf"](0.0, 20.0) == pytest.approx(1.0 / 20.0)

    def test_costi_annui_demo(self):
        assert _F["mh637_capitale_annuo"](CAPEX_DEMO, CRF_DEMO) == \
            pytest.approx(CAP_ANN_DEMO, rel=1e-12)
        assert _F["mh637_opex_annuo"](CAPEX_DEMO, 4.0) == OPEX_DEMO
        assert _F["mh637_costo_energia_annuo"](KG_DEMO, 3.0, 70.0) == \
            pytest.approx(EN_DEMO, rel=1e-9)

    def test_lcoh_demo(self):
        assert _F["mh637_lcoh_eur_kg"](CAP_ANN_DEMO, OPEX_DEMO, EN_DEMO,
                                       KG_DEMO) == pytest.approx(
            LCOH_DEMO, rel=1e-12)

    def test_lcoh_produzione_nulla(self):
        assert _F["mh637_lcoh_eur_kg"](1.0, 1.0, 1.0, 0.0) is None

    def test_risorsa_demo(self):
        assert _F["mh637_risorsa_totale_kg"](KG_DEMO, 20.0) == \
            pytest.approx(RISORSA_DEMO, rel=1e-12)

    def test_margine_e_payback_demo(self):
        _mg = _F["mh637_margine_annuo_eur"](6.50, LCOH_DEMO, KG_DEMO)
        assert _mg == pytest.approx(MARGINE_DEMO, rel=1e-9)
        assert _F["mh637_payback_anni"](CAPEX_DEMO, _mg) == pytest.approx(
            PAYBACK_DEMO, rel=1e-12)

    def test_payback_margine_negativo(self):
        assert _F["mh637_payback_anni"](CAPEX_DEMO, -1.0) is None
        assert _F["mh637_payback_anni"](CAPEX_DEMO, 0.0) is None

    def test_margine_lcoh_none(self):
        with pytest.raises(ValueError):
            _F["mh637_margine_annuo_eur"](6.50, None, KG_DEMO)

    def test_premium_e_co2_demo(self):
        assert _F["mh637_premium_vs_grigio_eur_kg"](
            LCOH_DEMO, 2.0) == pytest.approx(PREM_DEMO, rel=1e-12)
        assert _F["mh637_co2_pareggio_eur_t"](
            PREM_DEMO, 0.0095) == 0.0

    def test_co2_pareggio_positivo(self):
        assert _F["mh637_co2_pareggio_eur_t"](2.0, 0.01) == 200.0


class TestVerdetto:
    def test_competitivo_demo(self):
        assert _F["mh637_verdetto"](LCOH_DEMO, 6.50, 20.0,
                                    KG_DEMO) == "COMPETITIVO"

    def test_premium_accettabile(self):
        assert _F["mh637_verdetto"](7.0, 6.50, 20.0,
                                    KG_DEMO) == "PREMIUM_ACCETTABILE"

    def test_non_competitivo(self):
        assert _F["mh637_verdetto"](9.0, 6.50, 20.0,
                                    KG_DEMO) == "NON_COMPETITIVO"

    def test_non_calcolabile(self):
        assert _F["mh637_verdetto"](4.0, 6.50, 20.0,
                                    0.0) == "NON_CALCOLABILE"
        assert _F["mh637_verdetto"](None, 6.50, 20.0,
                                    KG_DEMO) == "NON_CALCOLABILE"


class TestSensibilita:
    def test_shape_e_valori(self):
        righe = _F["mh637_sensibilita"](
            [450.0, 500.0], [0.85, 0.90], 10, 0.95,
            2000000.0, 10000000.0, 4.0, 3.0, 70.0, 7.0, 20.0,
            6.50, 2.00, 20.0, 0.0095)
        assert len(righe) == 4
        r0 = righe[0]
        assert r0["portata_nm3_h"] == 450.0
        assert r0["purezza"] == 0.85
        assert r0["lcoh_eur_kg"] == pytest.approx(
            LCOH_P450_PUR85, rel=1e-12)
        r1 = [r for r in righe
              if r["portata_nm3_h"] == 500.0
              and r["purezza"] == 0.90][0]
        assert r1["lcoh_eur_kg"] == pytest.approx(LCOH_DEMO, rel=1e-12)
        assert all(r["verdetto"] in
                   ("COMPETITIVO", "PREMIUM_ACCETTABILE",
                    "NON_COMPETITIVO", "NON_CALCOLABILE") for r in righe)

    def test_purezza_zero_non_calcolabile(self):
        righe = _F["mh637_sensibilita"](
            [500.0], [0.0], 10, 0.95,
            2000000.0, 10000000.0, 4.0, 3.0, 70.0, 7.0, 20.0,
            6.50, 2.00, 20.0, 0.0095)
        assert righe[0]["lcoh_eur_kg"] is None
        assert righe[0]["verdetto"] == "NON_CALCOLABILE"

    def test_liste_vuote(self):
        for qs, ps in ([], [0.9]), ([500.0], []):
            with pytest.raises(ValueError):
                _F["mh637_sensibilita"](
                    qs, ps, 10, 0.95, 2000000.0, 10000000.0, 4.0, 3.0,
                    70.0, 7.0, 20.0, 6.50, 2.00, 20.0, 0.0095)

    def test_demo_defaults(self):
        d = _F["mh637_demo"]()
        assert d["n_pozzi"] == 10
        assert d["portata_nm3_h"] == 500.0
        assert d["purezza"] == 0.90
        assert d["emissioni_tco2_per_kg"] == 0.0095


class TestUI637:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def _helpers(self):
        s = self._src()
        return s.split("# W637 (22/10/2026)")[1].split(
            "# W636 (22/10/2026)")[0]

    def _ui(self):
        s = self._src()
        return s.split("with tab637:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 755
        assert TITLE637 in titles

    def test_registrazione(self):
        assert f'"{TITLE637}"' in self._src()
        assert ", tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755 = st.tabs([" in self._src()
        assert "with tab637:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st637_[a-z0-9_]+", self._ui()))
        attese = {"st637_npozzi", "st637_portata", "st637_purezza",
                  "st637_disp", "st637_cpozzo", "st637_capex",
                  "st637_opex", "st637_kwh", "st637_pel", "st637_tasso",
                  "st637_anni", "st637_tol", "st637_pmerc",
                  "st637_pgrigio", "st637_emis", "st637_sens",
                  "st637_go", "st637_fig", "st637_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st637_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        for sec in (self._helpers(), self._ui()):
            for w in ("api_key", "apikey", "password", "passwd", "secret"):
                assert w not in sec.lower(), f"sospetto segreto: {w}"
