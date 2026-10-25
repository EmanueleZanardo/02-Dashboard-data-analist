"""Test tab650 "❄️ Free cooling: quanto vale il freddo gratis?".

Demo calcolata a mano: chiller 500 kW_f, 2.500 h/anno copertura totale +
1.500 h/anno copertura parziale al 50 %, COP 4,0, ausiliari 25 kW,
prezzo 0,22 €/kWh, CAPEX 120.000 €, fattore CO2 0,35 kg/kWh, tasso 6 %,
vita 15 anni.
-> freddo_fc = 500 x (2.500 + 1.500 x 0,5) = 1.625.000 kWh_f/anno
-> E_chiller = 1.625.000 / 4 = 406.250 kWh_e/anno
-> E_aux     = 25 x (2.500 + 1.500) = 100.000 kWh/anno
-> risp      = 306.250 kWh/anno
-> risp_eur  = 306.250 x 0,22 = 67.375 €/anno
-> co2       = 306.250 x 0,35 / 1.000 = 107,1875 t/anno
-> flussi [-120.000, 67.375 x 15]; VAN(6 %) = 534.362,78 €
-> TIR 56,0752 %; payback anno 2 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh650_num", "mh650_nneg", "mh650_pos", "mh650_fraz01",
           "mh650_int_pos", "mh650_freddo_fc_kwh_f",
           "mh650_energia_chiller_evitata_kwh", "mh650_energia_aux_fc_kwh",
           "mh650_risparmio_kwh", "mh650_risparmio_eur",
           "mh650_co2_evitata_t", "mh650_flussi",
           "mh650_van", "mh650_tir", "mh650_payback", "mh650_verdetto",
           "mh650_demo", "mh650_demo_calcoli")

TITLE650 = "❄️ Free cooling: quanto vale il freddo gratis?"

FREDDO_DEMO = 1625000.0
E_CH_DEMO = 406250.0
E_AUX_DEMO = 100000.0
RISP_KWH_DEMO = 306250.0
RISP_EUR_DEMO = 67375.0
CAPEX_DEMO = 120000.0
CO2_DEMO = 107.1875
VAN_DEMO = 534362.78
TIR_DEMO = 0.5607515


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh650_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh650_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh650_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh650_nneg"](-0.1, "x")
        assert _F["mh650_pos"](0.1, "x") == pytest.approx(0.1)
        with pytest.raises(ValueError):
            _F["mh650_pos"](0.0, "x")

    def test_fraz01(self):
        assert _F["mh650_fraz01"](0.0, "x") == 0.0
        assert _F["mh650_fraz01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh650_fraz01"](1.01, "x")
        with pytest.raises(ValueError):
            _F["mh650_fraz01"](-0.01, "x")

    def test_int_pos(self):
        assert _F["mh650_int_pos"](15.0, "x") == 15
        with pytest.raises(ValueError):
            _F["mh650_int_pos"](0, "x")
        with pytest.raises(ValueError):
            _F["mh650_int_pos"](2.5, "x")


class TestFreddo:
    def test_freddo_demo(self):
        assert _F["mh650_freddo_fc_kwh_f"](500.0, 2500.0, 1500.0, 0.5) == \
            pytest.approx(FREDDO_DEMO)

    def test_freddo_zero_ore(self):
        assert _F["mh650_freddo_fc_kwh_f"](500.0, 0.0, 0.0, 0.5) == 0.0

    def test_freddo_quota_estremi(self):
        assert _F["mh650_freddo_fc_kwh_f"](500.0, 1000.0, 2000.0, 1.0) == \
            pytest.approx(500.0 * 3000.0)
        assert _F["mh650_freddo_fc_kwh_f"](500.0, 1000.0, 2000.0, 0.0) == \
            pytest.approx(500.0 * 1000.0)

    def test_chiller_evitata(self):
        assert _F["mh650_energia_chiller_evitata_kwh"](FREDDO_DEMO, 4.0) == \
            pytest.approx(E_CH_DEMO)

    def test_chiller_cop_non_positivo(self):
        with pytest.raises(ValueError):
            _F["mh650_energia_chiller_evitata_kwh"](FREDDO_DEMO, 0.0)

    def test_aux(self):
        assert _F["mh650_energia_aux_fc_kwh"](25.0, 2500.0, 1500.0) == \
            pytest.approx(E_AUX_DEMO)

    def test_aux_zero_ore(self):
        assert _F["mh650_energia_aux_fc_kwh"](25.0, 0.0, 0.0) == 0.0


class TestRisparmio:
    def test_risparmio_kwh(self):
        assert _F["mh650_risparmio_kwh"](E_CH_DEMO, E_AUX_DEMO) == \
            pytest.approx(RISP_KWH_DEMO)

    def test_risparmio_negativo_se_aux_domina(self):
        assert _F["mh650_risparmio_kwh"](50000.0, 100000.0) == -50000.0

    def test_risparmio_eur(self):
        assert _F["mh650_risparmio_eur"](RISP_KWH_DEMO, 0.22) == \
            pytest.approx(RISP_EUR_DEMO)

    def test_co2_demo(self):
        assert _F["mh650_co2_evitata_t"](RISP_KWH_DEMO, 0.35) == \
            pytest.approx(CO2_DEMO)

    def test_co2_none_se_risparmio_non_positivo(self):
        assert _F["mh650_co2_evitata_t"](0.0, 0.35) is None
        assert _F["mh650_co2_evitata_t"](-100.0, 0.35) is None


class TestFinanza:
    def test_flussi(self):
        assert _F["mh650_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15) == \
            [-CAPEX_DEMO] + [RISP_EUR_DEMO] * 15

    def test_van_demo(self):
        fl = _F["mh650_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        assert _F["mh650_van"](fl, 6.0) == pytest.approx(VAN_DEMO, abs=1.0)

    def test_tir_demo(self):
        fl = _F["mh650_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        assert _F["mh650_tir"](fl) == pytest.approx(TIR_DEMO, abs=1e-4)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh650_tir"]([1000.0, 100.0, 100.0]) is None

    def test_payback_demo(self):
        fl = _F["mh650_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        assert _F["mh650_payback"](fl) == 2

    def test_payback_none(self):
        assert _F["mh650_payback"]([-1000.0, 10.0, 10.0]) is None

    def test_verdetto_conviente(self):
        fl = _F["mh650_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        v = _F["mh650_verdetto"](RISP_EUR_DEMO,
                                 _F["mh650_van"](fl, 6.0), CAPEX_DEMO, 10.0)
        assert v == "CONVIENTE"

    def test_verdetto_marginale(self):
        assert _F["mh650_verdetto"](100.0, -500.0, 10000.0, 10.0) == \
            "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh650_verdetto"](100.0, -5000.0, 10000.0, 10.0) == \
            "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh650_verdetto"](0.0, 1000.0, 10000.0, 10.0) == \
            "NON_CALCOLABILE"
        assert _F["mh650_verdetto"](-50.0, 1000.0, 10000.0, 10.0) == \
            "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh650_demo_calcoli"]()
        assert c["freddo_fc_kwh_f"] == pytest.approx(FREDDO_DEMO)
        assert c["e_chiller_kwh"] == pytest.approx(E_CH_DEMO)
        assert c["e_aux_kwh"] == pytest.approx(E_AUX_DEMO)
        assert c["risp_kwh"] == pytest.approx(RISP_KWH_DEMO)
        assert c["risp_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert c["capex"] == pytest.approx(CAPEX_DEMO)
        assert c["co2_t"] == pytest.approx(CO2_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=1.0)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=1e-4)
        assert c["payback"] == 2
        assert c["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE650 in self._app()

    def test_helpers_presenti(self):
        assert "# W650 (23/10/2026) - tab650" in self._app()

    def test_chain_bumpata(self):
        assert ", tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715 = st.tabs([" in self._app()

    def test_tab_count_650(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 715
        assert TITLE650 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab650" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab650" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st650_[a-z0-9]+)"', self._app())
        assert len(keys) >= 10
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st649_") for k in keys)

    def test_csv_filename(self):
        assert "free_cooling.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W650 (23/10/2026)")[1].split("# W649 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
