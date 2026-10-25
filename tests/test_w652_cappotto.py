"""Test tab652 "🏢 Cappotto termico: il retrofit dell'involucro paga?".

Demo calcolata a mano: GG 2.400 (fattore 57,6), palazzo uffici
- pareti:    (1,20-0,28) x 800 x 57,6 = 42.393,6 kWh/anno
- copertura: (1,50-0,25) x 500 x 57,6 = 36.000,0 kWh/anno
- infissi:   (3,00-1,20) x 200 x 57,6 = 20.736,0 kWh/anno
tot = 99.129,6 kWh/anno
-> risp_eur = 99.129,6 x 0,14 = 13.878,144 €/anno
-> co2 = 99.129,6 x 0,20 / 1.000 = 19,82592 t/anno
-> capex = 72.000 + 30.000 + 60.000 = 162.000 €
-> flussi [-162.000, 13.878,144 x 25]; VAN(6 %) = 15.409,257567735687 €
-> TIR 0,06981499891810883; payback anno 12 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh652_num", "mh652_nneg", "mh652_pos", "mh652_int_pos",
           "mh652_trasmittanza", "mh652_gradi_giorno",
           "mh652_calore_risparmiato", "mh652_risparmio_eur",
           "mh652_co2_evitata_t", "mh652_flussi",
           "mh652_van", "mh652_tir", "mh652_payback", "mh652_verdetto",
           "mh652_demo", "mh652_demo_calcoli")

TITLE652 = "🏢 Cappotto termico: il retrofit dell'involucro paga?"

DQ_PARETI_DEMO = 42393.6
DQ_COPERTURA_DEMO = 36000.0
DQ_INFISSI_DEMO = 20736.0
DQ_TOT_DEMO = 99129.6
RISP_EUR_DEMO = 13878.144000000002
CAPEX_DEMO = 162000.0
CO2_DEMO = 19.825920000000004
VAN_DEMO = 15409.257567735687
TIR_DEMO = 0.06981499891810883


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh652_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh652_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh652_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh652_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh652_pos"](0, "x")
        assert _F["mh652_pos"](0.5, "x") == 0.5

    def test_int_pos(self):
        assert _F["mh652_int_pos"](25.0, "x") == 25
        with pytest.raises(ValueError):
            _F["mh652_int_pos"](25.5, "x")
        with pytest.raises(ValueError):
            _F["mh652_int_pos"](0, "x")

    def test_trasmittanza_ok_e_limiti(self):
        assert _F["mh652_trasmittanza"](0.28, "x") == 0.28
        assert _F["mh652_trasmittanza"](10.0, "x") == 10.0
        for bad in (0.0, -0.5, 10.1, 50.0):
            with pytest.raises(ValueError):
                _F["mh652_trasmittanza"](bad, "x")

    def test_gradi_giorno_ok_e_limiti(self):
        assert _F["mh652_gradi_giorno"](2400, "x") == 2400
        assert _F["mh652_gradi_giorno"](2400.0, "x") == 2400
        for bad in (0, -100, 6001, 2400.5):
            with pytest.raises(ValueError):
                _F["mh652_gradi_giorno"](bad, "x")


class TestFisica:
    def test_pareti_demo(self):
        q = _F["mh652_calore_risparmiato"](800.0, 1.20, 0.28, 2400)
        assert q == pytest.approx(DQ_PARETI_DEMO)

    def test_copertura_demo(self):
        q = _F["mh652_calore_risparmiato"](500.0, 1.50, 0.25, 2400)
        assert q == pytest.approx(DQ_COPERTURA_DEMO)

    def test_infissi_demo(self):
        q = _F["mh652_calore_risparmiato"](200.0, 3.00, 1.20, 2400)
        assert q == pytest.approx(DQ_INFISSI_DEMO)

    def test_formula_gradi_giorno(self):
        # (U_old - U_new) x A x GG x 24 / 1000
        q = _F["mh652_calore_risparmiato"](100.0, 2.0, 0.5, 2000)
        assert q == pytest.approx(1.5 * 100.0 * 2000 * 24.0 / 1000.0)

    def test_negativo_se_nuova_peggiore(self):
        assert _F["mh652_calore_risparmiato"](100.0, 0.3, 1.0,
                                             2000) == pytest.approx(
            -0.7 * 100.0 * 2000 * 24.0 / 1000.0)

    def test_superficie_zero(self):
        assert _F["mh652_calore_risparmiato"](0.0, 1.2, 0.28, 2400) == 0.0

    def test_risparmio_eur_demo(self):
        assert _F["mh652_risparmio_eur"](DQ_TOT_DEMO, 0.14) == pytest.approx(
            RISP_EUR_DEMO)


class TestCo2:
    def test_co2_demo(self):
        assert _F["mh652_co2_evitata_t"](DQ_TOT_DEMO, 0.20) == pytest.approx(
            CO2_DEMO)

    def test_co2_none_se_risparmio_nullo(self):
        assert _F["mh652_co2_evitata_t"](0.0, 0.20) is None
        assert _F["mh652_co2_evitata_t"](-50.0, 0.20) is None


class TestFinanza:
    def test_flussi_forma(self):
        fl = _F["mh652_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 25)
        assert fl[0] == pytest.approx(-CAPEX_DEMO)
        assert len(fl) == 26
        assert all(f == pytest.approx(RISP_EUR_DEMO) for f in fl[1:])

    def test_van_demo(self):
        fl = _F["mh652_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 25)
        assert _F["mh652_van"](fl, 6.0) == pytest.approx(VAN_DEMO, abs=1.0)

    def test_tir_demo(self):
        fl = _F["mh652_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 25)
        tir = _F["mh652_tir"](fl)
        assert tir == pytest.approx(TIR_DEMO, abs=1e-4)
        npv = sum(f / (1.0 + tir) ** t for t, f in enumerate(fl))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh652_tir"]([1000.0, 100.0, 100.0]) is None
        assert _F["mh652_tir"]([-1000.0, -100.0, -100.0]) is None

    def test_payback_demo(self):
        fl = _F["mh652_flussi"](CAPEX_DEMO, RISP_EUR_DEMO, 25)
        assert _F["mh652_payback"](fl) == 12

    def test_payback_none_mai(self):
        assert _F["mh652_payback"]([-1000.0, 10.0, 10.0]) is None

    def test_verdetto_conviente(self):
        assert _F["mh652_verdetto"](RISP_EUR_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh652_verdetto"](1000.0, -12000.0, 162000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh652_verdetto"](1000.0, -20000.0, 162000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh652_verdetto"](0.0, 100.0, CAPEX_DEMO,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh652_verdetto"](-50.0, None, CAPEX_DEMO,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh652_demo_calcoli"]()
        assert c["dq_elementi_kwh"]["pareti"] == pytest.approx(DQ_PARETI_DEMO)
        assert c["dq_elementi_kwh"]["copertura"] == pytest.approx(
            DQ_COPERTURA_DEMO)
        assert c["dq_elementi_kwh"]["infissi"] == pytest.approx(
            DQ_INFISSI_DEMO)
        assert c["dq_tot_kwh"] == pytest.approx(DQ_TOT_DEMO)
        assert c["risp_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert c["capex"] == pytest.approx(CAPEX_DEMO)
        assert c["co2_t"] == pytest.approx(CO2_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=1.0)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=1e-4)
        assert c["payback"] == 12
        assert c["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE652 in self._app()

    def test_helpers_presenti(self):
        assert "# W652 (23/10/2026) - tab652" in self._app()

    def test_chain_bumpata(self):
        assert ", tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698 = st.tabs([" in self._app()

    def test_tab_count_652(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 698
        assert TITLE652 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab652" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab652" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st652_[a-z0-9_]+)"', self._app())
        assert len(keys) >= 18
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st651_") for k in keys)

    def test_csv_filename(self):
        assert "cappotto_termico.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W652 (23/10/2026)")[1].split("# W651 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
