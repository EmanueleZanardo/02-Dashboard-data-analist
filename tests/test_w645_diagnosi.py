"""Test tab645 "🏭📋 Diagnosi energetica: audit e piano di efficientamento".

Demo calcolata a mano: stabilimento con baseline 4.000 MWh elettrici
(180 €/MWh), 1.200.000 Smc gas (0,85 €/Smc), 50.000 l gasolio (1,60 €/l),
produzione 25.000 t.
-> baseline 17.338.000 kWh/anno (4.000.000 + 12.840.000 + 498.000);
costo 1.820.000 €/anno (720.000 + 1.020.000 + 80.000);
tCO2 4.004,5/anno (1.520 + 2.352 + 132,5); EnPI 693,52 kWh/t.
4 interventi (tasso 6 %):
1. Relamping LED: 450 MWh risparmiati, -5.000 € OPEX -> 86.000 €/anno,
   171 tCO2, payback anno 2, VAN +601.010,6 € -> CONVIENTE
2. Recupero calore forni: 180.000 Smc, +8.000 € OPEX -> 145.000 €/anno,
   352,8 tCO2, payback anno 3, VAN +1.058.276,1 € -> CONVIENTE
3. Inverter su motori: 220 MWh -> 39.600 €/anno, 83,6 tCO2, payback 3,
   VAN +201.459,4 € -> CONVIENTE
4. Cappotto + infissi: 60.000 Smc, +2.000 € OPEX -> 49.000 €/anno,
   117,6 tCO2, payback 5, VAN +362.026,1 € -> CONVIENTE
Piano: investimento 760.000 €, risparmio 319.600 €/anno, 3.238.000 kWh
(18,68 % della baseline), 725 tCO2, VAN +2.222.772,3 € -> OBIETTIVO_RAGGIUNTO
(target 10 %). Priorita': Relamping, Recupero calore, Inverter, Cappotto.
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh645_num", "mh645_nneg", "mh645_pos", "mh645_pct100",
           "mh645_int_pos", "mh645_kwh_da_gas", "mh645_kwh_da_gasolio",
           "mh645_tco2_elettrica", "mh645_tco2_gas", "mh645_tco2_gasolio",
           "mh645_baseline_kwh", "mh645_baseline_costo_eur",
           "mh645_baseline_tco2", "mh645_enpi",
           "mh645_int_risparmio_kwh", "mh645_int_risparmio_eur_netto",
           "mh645_int_risparmio_tco2", "mh645_crf", "mh645_flussi",
           "mh645_van", "mh645_tir", "mh645_payback",
           "mh645_int_verdetto", "mh645_piano_aggregati",
           "mh645_quota_risparmio_pct", "mh645_piano_verdetto",
           "mh645_priorita", "mh645_demo_calcoli", "mh645_demo")

TITLE645 = ("🏭📋 Diagnosi energetica: audit e piano di efficientamento")

BASE_KWH_DEMO = 17338000.0
BASE_COSTO_DEMO = 1820000.0
BASE_TCO2_DEMO = 4004.5
ENPI_DEMO = 693.52
QUOTA_DEMO = 18.68
PIANO_INV_DEMO = 760000.0
PIANO_EUR_DEMO = 319600.0
PIANO_VAN_DEMO = 2222772.3


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh645_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "10", float("nan"), float("inf"), None):
            with pytest.raises(ValueError):
                _F["mh645_num"](bad, "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh645_nneg"](-0.1, "x")
        assert _F["mh645_nneg"](0.0, "x") == 0.0

    def test_pct100_bordi(self):
        assert _F["mh645_pct100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh645_pct100"](100.1, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh645_int_pos"](2.5, "x")
        assert _F["mh645_int_pos"](3.0, "x") == 3


class TestConversioni:
    def test_gas_smc_in_kwh(self):
        assert _F["mh645_kwh_da_gas"](1000.0) == pytest.approx(10700.0)

    def test_gasolio_l_in_kwh(self):
        assert _F["mh645_kwh_da_gasolio"](100.0) == pytest.approx(996.0)

    def test_tco2_vettori(self):
        assert _F["mh645_tco2_elettrica"](1000.0,
                                         380.0) == pytest.approx(380.0)
        assert _F["mh645_tco2_gas"](1000.0) == pytest.approx(1.96)
        assert _F["mh645_tco2_gasolio"](100.0) == pytest.approx(0.265)


class TestBaseline:
    def test_demo(self):
        p = _F["mh645_demo"]()
        assert _F["mh645_baseline_kwh"](
            p["e_mwh_anno"], p["gas_smc_anno"],
            p["gasolio_l_anno"]) == pytest.approx(BASE_KWH_DEMO)
        assert _F["mh645_baseline_costo_eur"](
            p["e_mwh_anno"], p["prezzo_e_eur_mwh"], p["gas_smc_anno"],
            p["prezzo_gas_eur_smc"], p["gasolio_l_anno"],
            p["prezzo_gasolio_eur_l"]) == pytest.approx(BASE_COSTO_DEMO)
        assert _F["mh645_baseline_tco2"](
            p["e_mwh_anno"], p["fattore_e_kg_mwh"], p["gas_smc_anno"],
            p["gasolio_l_anno"]) == pytest.approx(BASE_TCO2_DEMO)

    def test_enpi(self):
        assert _F["mh645_enpi"](BASE_KWH_DEMO,
                               25000.0) == pytest.approx(ENPI_DEMO)

    def test_enpi_none_se_produzione_nulla(self):
        assert _F["mh645_enpi"](BASE_KWH_DEMO, 0.0) is None


class TestIntervento:
    def test_relamping_demo(self):
        p = _F["mh645_demo"]()
        it = p["interventi"][0]
        assert _F["mh645_int_risparmio_kwh"](
            it["risp_e_mwh"], it["risp_gas_smc"],
            it["risp_gasolio_l"]) == pytest.approx(450000.0)
        # 450 MWh x 180 € - (-5.000 € di manutenzione risparmiata)
        assert _F["mh645_int_risparmio_eur_netto"](
            it["risp_e_mwh"], p["prezzo_e_eur_mwh"], it["risp_gas_smc"],
            p["prezzo_gas_eur_smc"], it["risp_gasolio_l"],
            p["prezzo_gasolio_eur_l"],
            it["opex_delta_eur"]) == pytest.approx(86000.0)
        assert _F["mh645_int_risparmio_tco2"](
            it["risp_e_mwh"], p["fattore_e_kg_mwh"], it["risp_gas_smc"],
            it["risp_gasolio_l"]) == pytest.approx(171.0)

    def test_crf_tasso_zero(self):
        assert _F["mh645_crf"](0.0, 10) == pytest.approx(0.1)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh645_tir"]([-100.0, -10.0, -10.0]) is None
        assert _F["mh645_tir"]([100.0, 10.0, 10.0]) is None

    def test_payback(self):
        assert _F["mh645_payback"]([-100.0, 10.0, 10.0]) is None
        assert _F["mh645_payback"]([-120000.0, 86000.0, 86000.0]) == 2

    def test_verdetto_conviente_demo(self):
        p = _F["mh645_demo"]()
        it = p["interventi"][0]
        fl = _F["mh645_flussi"](it["investimento_eur"], 86000.0,
                                it["vita_anni"])
        van = _F["mh645_van"](fl, p["tasso_pct"])
        assert van > 0.0
        assert _F["mh645_int_verdetto"](
            van, it["investimento_eur"], 86000.0,
            p["tolleranza_pct"]) == "CONVIENTE"

    def test_verdetto_marginale(self):
        fl = [-100000.0, 28000.0, 28000.0, 28000.0, 28000.0]
        van = _F["mh645_van"](fl, 6.0)
        assert van < 0.0
        assert _F["mh645_int_verdetto"](van, 100000.0, 28000.0,
                                       10.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_se_risparmio_nullo(self):
        assert _F["mh645_int_verdetto"](5000.0, 100000.0, 0.0,
                                       10.0) == "NON_CALCOLABILE"


class TestPiano:
    def test_demo_calcoli(self):
        d = _F["mh645_demo_calcoli"](_F["mh645_demo"]())
        assert d["verdetto_piano"] == "OBIETTIVO_RAGGIUNTO"
        assert d["quota_risparmio_pct"] == pytest.approx(QUOTA_DEMO,
                                                        abs=0.01)
        assert d["piano"]["investimento_tot_eur"] == pytest.approx(
            PIANO_INV_DEMO)
        assert d["piano"]["risparmio_eur_tot"] == pytest.approx(
            PIANO_EUR_DEMO)
        assert d["piano"]["van_tot_eur"] == pytest.approx(PIANO_VAN_DEMO,
                                                         abs=1.0)
        assert d["piano"]["n_interventi"] == 4

    def test_priorita_payback_poi_van(self):
        d = _F["mh645_demo_calcoli"](_F["mh645_demo"]())
        nomi = [r["nome"] for r in d["dettaglio"]]
        assert nomi == ["Relamping LED reparti", "Recupero calore forni",
                        "Inverter su motori", "Cappotto + infissi uffici"]

    def test_verdetto_parziale_e_nessun_risp(self):
        assert _F["mh645_piano_verdetto"](5.0, 10.0,
                                         BASE_KWH_DEMO) == "PARZIALE"
        assert _F["mh645_piano_verdetto"](0.0, 10.0,
                                         BASE_KWH_DEMO) == "NESSUN_RISP"
        assert _F["mh645_piano_verdetto"](12.0, 10.0,
                                         0.0) == "NON_CALCOLABILE"

    def test_piano_ignora_interventi_senza_risparmio(self):
        piano = _F["mh645_piano_aggregati"]([
            {"investimento": 1000.0, "risparmio_eur_netto": 0.0,
             "risparmio_kwh": 0.0, "risparmio_tco2": 0.0,
             "van_eur": -1000.0, "payback_anni": None},
            {"investimento": 2000.0, "risparmio_eur_netto": 500.0,
             "risparmio_kwh": 1000.0, "risparmio_tco2": 1.0,
             "van_eur": 300.0, "payback_anni": 4},
        ])
        assert piano["n_interventi"] == 1
        assert piano["investimento_tot_eur"] == pytest.approx(2000.0)


class TestIntegrazioneUI:
    @staticmethod
    def _src():
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        s = self._src()
        return s.split("with tab645:")[1].split("# Footer")[0]

    def _helpers(self):
        s = self._src()
        return s.split("# W645 (22/10/2026)")[1].split(
            "# W644 (22/10/2026)")[0]

    def test_chain_registry_e_label(self):
        assert ", tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715 = st.tabs([" in self._src()
        assert "with tab645:" in self._src()
        assert TITLE645 in self._src()

    def test_ui_chiavi_e_guard(self):
        ui = self._ui()
        assert "st645_go" in ui and "st645_csv" in ui
        assert "NON CALCOLABILE: baseline nulla" in ui
        assert "mh645_demo_calcoli" in ui

    def test_nessun_segreto_negli_helper(self):
        h = self._helpers().lower()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in h

    def test_chiavi_st_univoche(self):
        ui = self._ui()
        chiavi = re.findall(r'key="(st645_[^"]+)"', ui)
        assert len(chiavi) == len(set(chiavi)) and len(chiavi) >= 14
