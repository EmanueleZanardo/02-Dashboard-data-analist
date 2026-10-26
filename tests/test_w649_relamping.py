"""Test tab649 "💡 Relamping LED: il passaggio a LED paga davvero?".

Demo calcolata a mano: 200 apparecchi highbay da 150 W -> LED 60 W,
4.000 h/anno, prezzo 0,22 €/kWh, manutenzione evitata 1.200 €/anno,
CAPEX 45 €/apparecchio, fattore CO2 0,35 kg/kWh, tasso 6 %, vita 12 anni.
-> E_vecchia = 200 x 150/1000 x 4.000 = 120.000 kWh/anno
-> E_led     = 200 x  60/1000 x 4.000 =  48.000 kWh/anno
-> risp      = 72.000 kWh/anno
-> risp_eur  = 72.000 x 0,22 + 1.200 = 17.040 €/anno
-> capex     = 200 x 45 = 9.000 €
-> co2       = 72.000 x 0,35 / 1.000 = 25,2 t/anno
-> flussi [-9.000, 17.040 x 12]; VAN(6 %) = 133.860,70 €
-> TIR 189,3328 %; payback anno 1 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh649_num", "mh649_nneg", "mh649_pos", "mh649_pct100",
           "mh649_int_pos", "mh649_energia_vecchia_kwh",
           "mh649_energia_led_kwh", "mh649_risparmio_kwh",
           "mh649_risparmio_eur", "mh649_capex_totale",
           "mh649_co2_evitata_t", "mh649_flussi",
           "mh649_van", "mh649_tir", "mh649_payback", "mh649_verdetto",
           "mh649_demo", "mh649_demo_calcoli")

TITLE649 = "💡 Relamping LED: il passaggio a LED paga davvero?"

E_VECCHIA_DEMO = 120000.0
E_LED_DEMO = 48000.0
RISP_KWH_DEMO = 72000.0
RISP_EUR_DEMO = 17040.0
CAPEX_DEMO = 9000.0
CO2_DEMO = 25.2
VAN_DEMO = 133860.70
TIR_DEMO = 1.893328


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh649_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh649_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh649_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh649_nneg"](-0.1, "x")
        assert _F["mh649_pos"](0.1, "x") == pytest.approx(0.1)
        with pytest.raises(ValueError):
            _F["mh649_pos"](0.0, "x")

    def test_pct100(self):
        assert _F["mh649_pct100"](0.0, "x") == 0.0
        assert _F["mh649_pct100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh649_pct100"](100.01, "x")
        with pytest.raises(ValueError):
            _F["mh649_pct100"](-0.01, "x")

    def test_int_pos(self):
        assert _F["mh649_int_pos"](12.0, "x") == 12
        with pytest.raises(ValueError):
            _F["mh649_int_pos"](0, "x")
        with pytest.raises(ValueError):
            _F["mh649_int_pos"](2.5, "x")


class TestEnergia:
    def test_vecchia(self):
        assert _F["mh649_energia_vecchia_kwh"](200.0, 150.0, 4000.0) == \
            pytest.approx(E_VECCHIA_DEMO)

    def test_led(self):
        assert _F["mh649_energia_led_kwh"](200.0, 60.0, 4000.0) == \
            pytest.approx(E_LED_DEMO)

    def test_zero_ore(self):
        assert _F["mh649_energia_vecchia_kwh"](200.0, 150.0, 0.0) == 0.0
        assert _F["mh649_energia_led_kwh"](200.0, 60.0, 0.0) == 0.0

    def test_risparmio(self):
        assert _F["mh649_risparmio_kwh"](E_VECCHIA_DEMO, E_LED_DEMO) == \
            pytest.approx(RISP_KWH_DEMO)

    def test_risparmio_negativo_se_led_peggiore(self):
        assert _F["mh649_risparmio_kwh"](48000.0, 120000.0) == -72000.0

    def test_risparmio_eur_con_manutenzione(self):
        assert _F["mh649_risparmio_eur"](RISP_KWH_DEMO, 0.22, 1200.0) == \
            pytest.approx(RISP_EUR_DEMO)

    def test_risparmio_eur_senza_manutenzione(self):
        assert _F["mh649_risparmio_eur"](RISP_KWH_DEMO, 0.22, 0.0) == \
            pytest.approx(15840.0)

    def test_capex(self):
        assert _F["mh649_capex_totale"](200.0, 45.0) == \
            pytest.approx(CAPEX_DEMO)

    def test_co2(self):
        assert _F["mh649_co2_evitata_t"](RISP_KWH_DEMO, 0.35) == \
            pytest.approx(CO2_DEMO)

    def test_co2_none_se_risparmio_non_positivo(self):
        assert _F["mh649_co2_evitata_t"](0.0, 0.35) is None
        assert _F["mh649_co2_evitata_t"](-100.0, 0.35) is None


class TestFinanza:
    def test_flussi(self):
        f = _F["mh649_flussi"](9000.0, RISP_EUR_DEMO, 12)
        assert f[0] == -9000.0 and len(f) == 13
        assert all(x == pytest.approx(RISP_EUR_DEMO) for x in f[1:])

    def test_van_demo(self):
        f = _F["mh649_flussi"](9000.0, RISP_EUR_DEMO, 12)
        assert _F["mh649_van"](f, 6.0) == pytest.approx(VAN_DEMO, abs=0.05)

    def test_tir_demo(self):
        f = _F["mh649_flussi"](9000.0, RISP_EUR_DEMO, 12)
        assert _F["mh649_tir"](f) == pytest.approx(TIR_DEMO, abs=1e-4)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh649_tir"]([100.0, 50.0, 50.0]) is None
        assert _F["mh649_tir"]([-100.0, -50.0]) is None

    def test_payback_demo(self):
        f = _F["mh649_flussi"](9000.0, RISP_EUR_DEMO, 12)
        assert _F["mh649_payback"](f) == 1

    def test_payback_none_se_mai(self):
        assert _F["mh649_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviene(self):
        assert _F["mh649_verdetto"](17040.0, 133860.70, 9000.0,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        assert _F["mh649_verdetto"](100.0, -800.0, 9000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviene(self):
        assert _F["mh649_verdetto"](100.0, -5000.0, 9000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh649_verdetto"](0.0, 10.0, 9000.0,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh649_verdetto"](-50.0, 10.0, 9000.0,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh649_demo_calcoli"]()
        assert c["e_vecchia"] == pytest.approx(E_VECCHIA_DEMO)
        assert c["e_led"] == pytest.approx(E_LED_DEMO)
        assert c["risp_kwh"] == pytest.approx(RISP_KWH_DEMO)
        assert c["risp_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert c["capex"] == pytest.approx(CAPEX_DEMO)
        assert c["co2_t"] == pytest.approx(CO2_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=0.05)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=1e-4)
        assert c["payback"] == 1
        assert c["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE649 in self._app()

    def test_helpers_presenti(self):
        assert "# W649 (23/10/2026) - tab649" in self._app()

    def test_chain_bumpata(self):
        assert ", tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724 = st.tabs([" in self._app()

    def test_tab_count_649(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 724
        assert TITLE649 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab649" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab649" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st649_[a-z0-9]+)"', self._app())
        assert len(keys) >= 10
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st648_") for k in keys)

    def test_csv_filename(self):
        assert "relamping_led.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W649 (23/10/2026)")[1].split("# W648 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
