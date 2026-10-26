"""Test tab654 "☀️🚿 Solare termico: quanta acqua calda dal tetto?".

Demo calcolata a mano: condominio, 1.500 l/giorno ACS con dT 40 K,
30 m2 di collettori piani, H annua 1.200 kWh/m2, eta0 0,78, k1 3,5,
dT collettore 35 K, G medio 600 W/m2, caldaia 0,9, gas 0,09 €/kWh,
O&M 300 €/anno, CAPEX 24.000 €, CO2 gas 0,20 kg/kWh, 5 %, 20 anni,
tolleranza 10 %.

- eta_coll = 0,78 - 3,5 x 35 / 600 = 0,5758333333333334
- Q_acs = 1.500 x 1,163 x 40 x 365 / 1.000 = 25.469,7 kWh/anno
- Q_prodotta = 30 x 1.200 x 0,5758333333333334 = 20.730,0 kWh/anno
  (< Q_acs -> Q_sol = 20.730,0; f_solare = 0,813908291028163)
- C_base = 20.730 / 0,9 x 0,09 = 2.073,0 €/anno
- risparmio = 2.073 - 300 = 1.773,0 €/anno
- CO2 evitata = 20.730 / 0,9 x 0,20 / 1.000 = 4,606666666666667 t/anno
- flussi [-24.000, 1.773 x 20]; VAN(5 %) = -1.904,5010626766134 €;
  TIR 0,0404496152252758; payback anno 14;
  |VAN| = 1.904,50 <= 10 % x 24.000 = 2.400 -> MARGINALE
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh654_num", "mh654_nneg", "mh654_pos", "mh654_int_pos",
           "mh654_frazione", "mh654_rendimento", "mh654_eta_collettore",
           "mh654_fattore_perdite", "mh654_fabbisogno_acs",
           "mh654_energia_solare", "mh654_frazione_solare",
           "mh654_costo_baseline", "mh654_costo_solare", "mh654_risparmio",
           "mh654_co2_t", "mh654_flussi", "mh654_van", "mh654_tir",
           "mh654_payback", "mh654_verdetto", "mh654_demo",
           "mh654_demo_calcoli")

TITLE654 = "☀️🚿 Solare termico: quanta acqua calda dal tetto?"

ETA_DEMO = 0.5758333333333334
Q_ACS_DEMO = 25469.7
Q_SOL_DEMO = 20730.000000000004
F_SOL_DEMO = 0.813908291028163
C_BASE_DEMO = 2073.0
RISP_DEMO = 1773.0
CO2_DEMO = 4.606666666666667
CAPEX_DEMO = 24000.0
VAN_DEMO = -1904.5010626766134
TIR_DEMO = 0.0404496152252758


def _eta_demo():
    return _F["mh654_eta_collettore"](0.78, 3.5, 35.0, 600.0)


def _q_acs_demo():
    return _F["mh654_fabbisogno_acs"](1500.0, 40.0)


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh654_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh654_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh654_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh654_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh654_pos"](0, "x")
        assert _F["mh654_pos"](0.5, "x") == 0.5

    def test_int_pos(self):
        assert _F["mh654_int_pos"](20.0, "x") == 20
        with pytest.raises(ValueError):
            _F["mh654_int_pos"](20.5, "x")

    def test_frazione_bordi(self):
        assert _F["mh654_frazione"](0, "x") == 0.0
        assert _F["mh654_frazione"](1, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh654_frazione"](1.1, "x")

    def test_rendimento_bordi_aperti(self):
        with pytest.raises(ValueError):
            _F["mh654_rendimento"](0, "x")
        with pytest.raises(ValueError):
            _F["mh654_rendimento"](1, "x")
        assert _F["mh654_rendimento"](0.5, "x") == 0.5


class TestCollettore:
    def test_eta_demo(self):
        assert _eta_demo() == pytest.approx(ETA_DEMO)

    def test_eta_clamp_zero(self):
        # dT enorme / G scarso -> eta 0, non negativa
        assert _F["mh654_eta_collettore"](0.5, 10.0, 100.0, 50.0) == 0.0

    def test_eta_rifiuta_eta0_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh654_eta_collettore"](1.2, 3.5, 35.0, 600.0)

    def test_eta_rifiuta_g_non_positivo(self):
        with pytest.raises(ValueError):
            _F["mh654_eta_collettore"](0.78, 3.5, 35.0, 0.0)


class TestBilancio:
    def test_fattore_perdite_zero(self):
        assert _F["mh654_fattore_perdite"](0.0) == pytest.approx(1.0)

    def test_fattore_perdite_venti(self):
        # 20 % di perdite -> fabbisogno x 1,25
        assert _F["mh654_fattore_perdite"](20.0) == pytest.approx(1.25)

    def test_fattore_perdite_rifiuta_bordi(self):
        with pytest.raises(ValueError):
            _F["mh654_fattore_perdite"](100.0)
        with pytest.raises(ValueError):
            _F["mh654_fattore_perdite"](-1.0)

    def test_fabbisogno_demo(self):
        assert _q_acs_demo() == pytest.approx(Q_ACS_DEMO)

    def test_fabbisogno_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh654_fabbisogno_acs"](0, 40.0)

    def test_energia_solare_cappata_dal_fabbisogno(self):
        # 100 m2 produrrebbero oltre il fabbisogno -> cappato a Q_acs
        q = _F["mh654_energia_solare"](100.0, 1200.0, ETA_DEMO, Q_ACS_DEMO)
        assert q == pytest.approx(Q_ACS_DEMO)

    def test_energia_solare_demo(self):
        q = _F["mh654_energia_solare"](30.0, 1200.0, ETA_DEMO, Q_ACS_DEMO)
        assert q == pytest.approx(Q_SOL_DEMO)

    def test_frazione_solare_demo(self):
        assert _F["mh654_frazione_solare"](Q_SOL_DEMO, Q_ACS_DEMO) == \
            pytest.approx(F_SOL_DEMO)

    def test_frazione_mai_oltre_uno(self):
        assert _F["mh654_frazione_solare"](Q_ACS_DEMO, Q_ACS_DEMO) == \
            pytest.approx(1.0)


class TestCosti:
    def test_costo_baseline_demo(self):
        assert _F["mh654_costo_baseline"](Q_SOL_DEMO, 0.9, 0.09) == \
            pytest.approx(C_BASE_DEMO)

    def test_costo_solare_solo_om(self):
        assert _F["mh654_costo_solare"](300.0) == 300.0
        with pytest.raises(ValueError):
            _F["mh654_costo_solare"](-1.0)

    def test_risparmio_demo(self):
        assert _F["mh654_risparmio"](C_BASE_DEMO, 300.0) == \
            pytest.approx(RISP_DEMO)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh654_risparmio"](100.0, 300.0) == pytest.approx(-200.0)


class TestCo2:
    def test_co2_demo(self):
        assert _F["mh654_co2_t"](Q_SOL_DEMO, 0.9, 0.20) == \
            pytest.approx(CO2_DEMO)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh654_flussi"](CAPEX_DEMO, RISP_DEMO, 20)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 21
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_van_demo(self):
        assert _F["mh654_van"](self._flussi_demo(), 5.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh654_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh654_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh654_payback"](self._flussi_demo()) == 14

    def test_payback_none_mai(self):
        assert _F["mh654_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_marginale_demo(self):
        assert _F["mh654_verdetto"](RISP_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "MARGINALE"

    def test_verdetto_conviente(self):
        assert _F["mh654_verdetto"](1000.0, 5000.0, 24000.0,
                                    10.0) == "CONVIENTE"

    def test_verdetto_non_conviente(self):
        assert _F["mh654_verdetto"](100.0, -5000.0, 24000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh654_verdetto"](0.0, 1.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh654_verdetto"](-50.0, 1.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        r = _F["mh654_demo_calcoli"]()
        assert r["eta_coll"] == pytest.approx(ETA_DEMO)
        assert r["q_acs"] == pytest.approx(Q_ACS_DEMO)
        assert r["q_sol"] == pytest.approx(Q_SOL_DEMO)
        assert r["f_solare"] == pytest.approx(F_SOL_DEMO)
        assert r["c_base"] == pytest.approx(C_BASE_DEMO)
        assert r["risparmio"] == pytest.approx(RISP_DEMO)
        assert r["co2_t"] == pytest.approx(CO2_DEMO)
        assert r["van"] == pytest.approx(VAN_DEMO)
        assert r["tir"] == pytest.approx(TIR_DEMO)
        assert r["payback"] == 14
        assert r["verdetto"] == "MARGINALE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE654 in self._app()

    def test_helpers_presenti(self):
        assert "# W654 (23/10/2026) - tab654" in self._app()

    def test_chain_bumpata(self):
        assert ", tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722 = st.tabs([" in self._app()

    def test_tab_count_654(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 722
        assert TITLE654 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab654" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab654" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st654_[a-z0-9_]+)"', self._app())
        assert len(keys) >= 19
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st653_") for k in keys)

    def test_csv_filename(self):
        assert "solare_termico.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W654 (23/10/2026)")[1].split("# W653 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
