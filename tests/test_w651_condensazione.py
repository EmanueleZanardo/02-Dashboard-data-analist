"""Test tab651 "🔥 Caldaia a condensazione: il retrofit paga?".

Demo calcolata a mano: caldaia esistente 88 % -> condensazione 97 %,
120.000 Smc/anno, prezzo 0,85 €/Smc, CAPEX 45.000 €, fattore CO2 1,96 kg/Smc,
tasso 6 %, vita 15 anni.
-> gas_nuovo = 120.000 x 88 / 97 = 108.865,97938144329 Smc/anno
-> risp_smc  = 11.134,020618556708 Smc/anno
-> risp_eur  = 11.134,020618556708 x 0,85 = 9.463,9175257732 €/anno
-> co2       = 11.134,020618556708 x 1,96 / 1.000 = 21,82268041237115 t/anno
-> flussi [-45.000, 9.463,9175257732 x 15]; VAN(6 %) = 46.915,9234097549 €
-> TIR 0,19594877113080555; payback anno 5 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh651_num", "mh651_nneg", "mh651_pos", "mh651_int_pos",
           "mh651_rendimento_pct", "mh651_gas_nuovo_smc",
           "mh651_risparmio_smc", "mh651_risparmio_eur",
           "mh651_co2_evitata_t", "mh651_flussi",
           "mh651_van", "mh651_tir", "mh651_payback", "mh651_verdetto",
           "mh651_demo", "mh651_demo_calcoli")

TITLE651 = "🔥 Caldaia a condensazione: il retrofit paga?"

GAS_NUOVO_DEMO = 108865.97938144329
RISP_SMC_DEMO = 11134.020618556708
RISP_EUR_DEMO = 9463.9175257732
CAPEX_DEMO = 45000.0
CO2_DEMO = 21.82268041237115
VAN_DEMO = 46915.9234097549
TIR_DEMO = 0.19594877113080555


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh651_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh651_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh651_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh651_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh651_pos"](0, "x")
        assert _F["mh651_pos"](0.5, "x") == 0.5

    def test_int_pos(self):
        assert _F["mh651_int_pos"](15.0, "x") == 15
        with pytest.raises(ValueError):
            _F["mh651_int_pos"](15.5, "x")
        with pytest.raises(ValueError):
            _F["mh651_int_pos"](0, "x")

    def test_rendimento_ok_e_limiti(self):
        assert _F["mh651_rendimento_pct"](97.0, "x") == 97.0
        assert _F["mh651_rendimento_pct"](120.0, "x") == 120.0
        for bad in (0.0, -5.0, 120.1, 200.0):
            with pytest.raises(ValueError):
                _F["mh651_rendimento_pct"](bad, "x")


class TestGas:
    def test_gas_nuovo_demo(self):
        g = _F["mh651_gas_nuovo_smc"](120000.0, 88.0, 97.0)
        assert g == pytest.approx(GAS_NUOVO_DEMO)

    def test_gas_nuovo_stesso_rendimento(self):
        assert _F["mh651_gas_nuovo_smc"](1000.0, 90.0, 90.0) == pytest.approx(1000.0)

    def test_risparmio_demo(self):
        assert _F["mh651_risparmio_smc"](120000.0, GAS_NUOVO_DEMO) == pytest.approx(
            RISP_SMC_DEMO)

    def test_risparmio_negativo_se_nuova_peggiore(self):
        assert _F["mh651_risparmio_smc"](1000.0, 1100.0) == pytest.approx(-100.0)

    def test_risparmio_eur_demo(self):
        assert _F["mh651_risparmio_eur"](RISP_SMC_DEMO, 0.85) == pytest.approx(
            RISP_EUR_DEMO)


class TestCo2:
    def test_co2_demo(self):
        assert _F["mh651_co2_evitata_t"](RISP_SMC_DEMO, 1.96) == pytest.approx(
            CO2_DEMO)

    def test_co2_none_se_risparmio_nullo(self):
        assert _F["mh651_co2_evitata_t"](0.0, 1.96) is None
        assert _F["mh651_co2_evitata_t"](-50.0, 1.96) is None


class TestFinanza:
    def test_flussi_forma(self):
        fl = _F["mh651_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        assert fl[0] == pytest.approx(-CAPEX_DEMO)
        assert len(fl) == 16
        assert all(f == pytest.approx(RISP_EUR_DEMO) for f in fl[1:])

    def test_van_demo(self):
        fl = _F["mh651_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        assert _F["mh651_van"](fl, 6.0) == pytest.approx(VAN_DEMO, abs=1.0)

    def test_tir_demo(self):
        fl = _F["mh651_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        tir = _F["mh651_tir"](fl)
        assert tir == pytest.approx(TIR_DEMO, abs=1e-4)
        npv = sum(f / (1.0 + tir) ** t for t, f in enumerate(fl))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh651_tir"]([1000.0, 100.0, 100.0]) is None
        assert _F["mh651_tir"]([-1000.0, -100.0, -100.0]) is None

    def test_payback_demo(self):
        fl = _F["mh651_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 15)
        assert _F["mh651_payback"](fl) == 5

    def test_payback_none_mai(self):
        assert _F["mh651_payback"]([-1000.0, 10.0, 10.0]) is None

    def test_verdetto_conviente(self):
        assert _F["mh651_verdetto"](RISP_EUR_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh651_verdetto"](1000.0, -3000.0, 45000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh651_verdetto"](1000.0, -6000.0, 45000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh651_verdetto"](0.0, 100.0, CAPEX_DEMO,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh651_verdetto"](-50.0, None, CAPEX_DEMO,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh651_demo_calcoli"]()
        assert c["gas_nuovo_smc"] == pytest.approx(GAS_NUOVO_DEMO)
        assert c["risp_smc"] == pytest.approx(RISP_SMC_DEMO)
        assert c["risp_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert c["capex"] == pytest.approx(CAPEX_DEMO)
        assert c["co2_t"] == pytest.approx(CO2_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=1.0)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=1e-4)
        assert c["payback"] == 5
        assert c["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE651 in self._app()

    def test_helpers_presenti(self):
        assert "# W651 (23/10/2026) - tab651" in self._app()

    def test_chain_bumpata(self):
        assert ", tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738 = st.tabs([" in self._app()

    def test_tab_count_651(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 738
        assert TITLE651 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab651" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab651" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st651_[a-z0-9]+)"', self._app())
        assert len(keys) >= 10
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st650_") for k in keys)

    def test_csv_filename(self):
        assert "caldaia_condensazione.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W651 (23/10/2026)")[1].split("# W650 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
