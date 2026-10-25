"""Test tab657 "🌊⚡ Armoniche: quanto costano le distorsioni?".

Demo calcolata a mano: stabilimento con perdite Joule fondamentali
P_base = 30 kW (cavi + trasformatore), THD_I misurata 25 %,
THD residua con filtro attivo 4 %, cos(phi) di spostamento 0,95,
7.000 h/anno, prezzo energia 0,20 EUR/kWh, costi evitati 6.000 EUR/anno
(condensatori + fermi), CAPEX filtro 55.000 EUR, O&M 2.000 EUR/anno,
CO2 elettricita' 0,30 kg/kWh, 6 %, 12 anni, tolleranza 10 %.

- P_harm_0 = 30 x 0,25^2 = 1,875 kW
- P_harm_1 = 30 x 0,04^2 = 0,048 kW
- E_risparmiata = (1,875 - 0,048) x 7.000 = 12.789,0 kWh/anno
- costo perdite prima = 1,875 x 7.000 x 0,20 = 2.625,0 EUR/anno
- costo perdite dopo = 0,048 x 7.000 x 0,20 = 67,2 EUR/anno
- risparmio = (2.625,0 - 67,2) + 6.000 - 2.000 = 6.557,8 EUR/anno
- PF_vero_0 = 0,95 / sqrt(1,0625) = 0,9216353751380653
- PF_vero_1 = 0,95 / sqrt(1,0016) = 0,9492409107856998
- fattore I_rms/I_1 = sqrt(1,0625) = 1,0307764064044151
- CO2 evitata = 12.789 x 0,30 / 1.000 = 3,8367 t/anno
- flussi [-55.000, 6.557,8 x 12]; VAN(6 %) = -20,428207754292544 EUR
  (|VAN| = 20,43 <= 10 % x 55.000 = 5.500 -> MARGINALE)
- TIR = 0,0599322448851759 (5,9932 %); payback anno 9
  (6.557,8 x 8 = 52.462,4 < 55.000 <= 59.020,2 = 6.557,8 x 9)
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh657_num", "mh657_nneg", "mh657_pos", "mh657_int_pos",
           "mh657_frazione", "mh657_thd", "mh657_cosphi",
           "mh657_fattore_rms", "mh657_pf_vero",
           "mh657_perdite_armoniche", "mh657_perdite_totali",
           "mh657_energia", "mh657_costo", "mh657_risparmio",
           "mh657_co2_t", "mh657_flussi", "mh657_van", "mh657_tir",
           "mh657_payback", "mh657_verdetto", "mh657_demo",
           "mh657_demo_calcoli")

TITLE657 = "🌊⚡ Armoniche: quanto costano le distorsioni?"

P_BASE_DEMO = 30.0
THD0_DEMO = 0.25
THD1_DEMO = 0.04
P_HARM_0_DEMO = 1.875
P_HARM_1_DEMO = 0.048
E_SAVE_DEMO = 12789.0
COSTO_PRIMA_DEMO = 2625.0
COSTO_DOPO_DEMO = 67.2
RISP_DEMO = 6557.8
PF_VERO_0_DEMO = 0.9216353751380653
PF_VERO_1_DEMO = 0.9492409107856998
FATTORE_RMS_DEMO = 1.0307764064044151
CO2_DEMO = 3.8367
CAPEX_DEMO = 55000.0
VAN_DEMO = -20.428207754292544
TIR_DEMO = 0.0599322448851759


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh657_num"](True, "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh657_num"](float("nan"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh657_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh657_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh657_int_pos"](2.5, "x")

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh657_frazione"](1.1, "x")

    def test_thd_rifiuta_sopra_due(self):
        with pytest.raises(ValueError):
            _F["mh657_thd"](2.5, "x")

    def test_thd_accetta_due(self):
        assert _F["mh657_thd"](2.0, "x") == 2.0

    def test_cosphi_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh657_cosphi"](0.0, "x")

    def test_cosphi_accetta_uno(self):
        assert _F["mh657_cosphi"](1.0, "x") == 1.0


class TestFisica:
    def test_fattore_rms_demo(self):
        assert _F["mh657_fattore_rms"](THD0_DEMO) == \
            pytest.approx(FATTORE_RMS_DEMO)

    def test_fattore_rms_zero(self):
        assert _F["mh657_fattore_rms"](0.0) == pytest.approx(1.0)

    def test_pf_vero_demo_prima(self):
        assert _F["mh657_pf_vero"](0.95, THD0_DEMO) == \
            pytest.approx(PF_VERO_0_DEMO)

    def test_pf_vero_demo_dopo(self):
        assert _F["mh657_pf_vero"](0.95, THD1_DEMO) == \
            pytest.approx(PF_VERO_1_DEMO)

    def test_pf_vero_senza_armoniche(self):
        assert _F["mh657_pf_vero"](0.95, 0.0) == pytest.approx(0.95)

    def test_pf_vero_minore_cosphi(self):
        assert _F["mh657_pf_vero"](0.95, 0.25) < 0.95

    def test_perdite_armoniche_demo_prima(self):
        assert _F["mh657_perdite_armoniche"](P_BASE_DEMO, THD0_DEMO) == \
            pytest.approx(P_HARM_0_DEMO)

    def test_perdite_armoniche_demo_dopo(self):
        assert _F["mh657_perdite_armoniche"](P_BASE_DEMO, THD1_DEMO) == \
            pytest.approx(P_HARM_1_DEMO)

    def test_perdite_armoniche_zero_senza_thd(self):
        assert _F["mh657_perdite_armoniche"](P_BASE_DEMO, 0.0) == \
            pytest.approx(0.0)

    def test_perdite_totali_demo(self):
        assert _F["mh657_perdite_totali"](P_BASE_DEMO, THD0_DEMO) == \
            pytest.approx(P_BASE_DEMO + P_HARM_0_DEMO)

    def test_energia_demo(self):
        assert _F["mh657_energia"](P_HARM_0_DEMO - P_HARM_1_DEMO,
                                   7000.0) == pytest.approx(E_SAVE_DEMO)

    def test_costo_demo_prima(self):
        assert _F["mh657_costo"](P_HARM_0_DEMO * 7000.0, 0.20) == \
            pytest.approx(COSTO_PRIMA_DEMO)

    def test_costo_demo_dopo(self):
        assert _F["mh657_costo"](P_HARM_1_DEMO * 7000.0, 0.20) == \
            pytest.approx(COSTO_DOPO_DEMO)


class TestEconomia:
    def test_risparmio_demo(self):
        assert _F["mh657_risparmio"](COSTO_PRIMA_DEMO, COSTO_DOPO_DEMO,
                                    6000.0, 2000.0) == \
            pytest.approx(RISP_DEMO)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh657_risparmio"](100.0, 90.0, 0.0,
                                    500.0) == pytest.approx(-490.0)

    def test_co2_demo(self):
        assert _F["mh657_co2_t"](E_SAVE_DEMO, 0.30) == \
            pytest.approx(CO2_DEMO)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh657_flussi"](CAPEX_DEMO, RISP_DEMO, 12)

    def test_flussi_struttura(self):
        fl = _F["mh657_flussi"](CAPEX_DEMO, RISP_DEMO, 12)
        assert fl[0] == -CAPEX_DEMO and len(fl) == 13
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_van_demo(self):
        assert _F["mh657_van"](self._flussi_demo(), 6.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh657_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh657_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh657_payback"](self._flussi_demo()) == 9

    def test_payback_none_mai(self):
        assert _F["mh657_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_marginale_demo(self):
        assert _F["mh657_verdetto"](RISP_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "MARGINALE"

    def test_verdetto_conviente(self):
        assert _F["mh657_verdetto"](1000.0, 500.0, 24000.0,
                                    10.0) == "CONVIENTE"

    def test_verdetto_non_conviente(self):
        assert _F["mh657_verdetto"](1000.0, -15000.0, 24000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh657_verdetto"](0.0, 500.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh657_verdetto"](-5.0, 500.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"


class TestDemoEndToEnd:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh657_demo_calcoli"]()
        assert c["p_harm_0"] == pytest.approx(P_HARM_0_DEMO)
        assert c["p_harm_1"] == pytest.approx(P_HARM_1_DEMO)
        assert c["e_risparmiata"] == pytest.approx(E_SAVE_DEMO)
        assert c["costo_prima"] == pytest.approx(COSTO_PRIMA_DEMO)
        assert c["costo_dopo"] == pytest.approx(COSTO_DOPO_DEMO)
        assert c["risparmio"] == pytest.approx(RISP_DEMO)
        assert c["pf_vero_0"] == pytest.approx(PF_VERO_0_DEMO)
        assert c["pf_vero_1"] == pytest.approx(PF_VERO_1_DEMO)
        assert c["co2_t"] == pytest.approx(CO2_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO)
        assert c["tir"] == pytest.approx(TIR_DEMO)
        assert c["payback"] == 9
        assert c["verdetto"] == "MARGINALE"

    def test_demo_defaults(self):
        d = _F["mh657_demo"]()
        assert d["p_base_kw"] == 30.0
        assert d["thd0_pct"] == 25.0
        assert d["thd1_pct"] == 4.0
        assert d["vita_anni"] == 12


class TestRegistry:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE657 in self._app()

    def test_helpers_presenti(self):
        assert "# W657 (23/10/2026) - tab657" in self._app()

    def test_chain_bumpata(self):
        assert ", tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708 = st.tabs([" in self._app()

    def test_tab_count_657(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 708
        assert TITLE657 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab657" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab657" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st657_[a-z0-9_]+)"', self._app())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st656_") for k in keys)

    def test_csv_filename(self):
        assert "armoniche.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W657 (23/10/2026)")[1].split("# W656 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
