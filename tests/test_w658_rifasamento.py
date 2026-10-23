"""Test tab658 "⚡ Rifasamento: quanto costa il cos(phi) basso?".

Demo calcolata a mano: P = 500 kW, cos(phi) misurato 0,82,
cos(phi) target 0,97, soglia penali 0,95, 6.000 h/anno, perdite
misurate a cos0 = 12 kW, prezzo reattiva 0,035 EUR/kvarh, prezzo
energia 0,20 EUR/kWh, THD misurata 6 %, CAPEX diretto 45.000 EUR,
O&M 1.200 EUR/anno, CO2 elettricita' 0,30 kg/kWh, 6 %, 15 anni,
tolleranza 0,10 (frazione del CAPEX).

- tan0 = sqrt(1 - 0,82^2) / 0,82 = sqrt(0,3276) / 0,82
       = 0,6980042937197165
- tan1 = sqrt(1 - 0,97^2) / 0,97 = sqrt(0,0591) / 0,97
       = 0,25062362435346847
- tan_soglia = sqrt(1 - 0,95^2) / 0,95 = sqrt(0,0975) / 0,95
       = 0,32868410517886315
- Qc = 500 x (0,6980042937197165 - 0,25062362435346847)
     = 500 x 0,447380669366248 = 223,690334683124 kvar
- Q_eccesso = 500 x (0,6980042937197165 - 0,32868410517886315)
     = 500 x 0,3693201885408535 = 184,66009427042667 kvar
- E_reattiva = 184,66009427042667 x 6.000 = 1.107.960,56562256 kvarh
- penali = 1.107.960,56562256 x 0,035 = 38.778,6197967896 EUR/anno
- perdite dopo = 12 x (0,82/0,97)^2 = 12 x 0,7146349073422609
       = 8,575619088107132 kW
- E_risparmiata = (12 - 8,575619088107132) x 6.000
       = 3,424380911892868 x 6.000 = 20.546,28547135721 kWh/anno
- risparmio = 38.778,6197967896 + 20.546,28547135721 x 0,20 - 1.200
       = 41.687,876891061045 EUR/anno
- CO2 evitata = 20.546,28547135721 x 0,30 / 1.000 = 6,1638856414071626 t
- flussi [-45.000, 41.687,876891061045 x 15];
  VAN(6 %) = 359.883,0401362784 EUR -> CONVIENTE
- TIR = 0,9263476304696108 (92,6348 %); payback anno 2
  (-45.000 + 41.687,88 = -3.312,12 < 0; + 41.687,88 = 38.375,75 >= 0)
- banco detunato: THD 6 % <= 7 % -> False (banco standard OK)
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh658_num", "mh658_nneg", "mh658_pos", "mh658_int_pos",
           "mh658_frazione", "mh658_cosphi", "mh658_tan_da_cosphi",
           "mh658_qc_kvar", "mh658_q_eccesso_kvar",
           "mh658_energia_reattiva_kvarh", "mh658_penali_annue",
           "mh658_perdite_dopo_kw", "mh658_energia_risparmiata_kwh",
           "mh658_capex_da_specifico", "mh658_risparmio_annuo",
           "mh658_co2_t", "mh658_flussi", "mh658_van", "mh658_tir",
           "mh658_payback", "mh658_verdetto", "mh658_banco_detunato",
           "mh658_demo", "mh658_demo_calcoli")

TITLE658 = "⚡ Rifasamento: quanto costa il cos(phi) basso?"

TAN0_DEMO = 0.6980042937197165
TAN1_DEMO = 0.25062362435346847
TAN_SOGLIA_DEMO = 0.32868410517886315
QC_DEMO = 223.690334683124
Q_ECCESSO_DEMO = 184.66009427042667
E_REATTIVA_DEMO = 1107960.56562256
PENALI_DEMO = 38778.6197967896
PERDITE_DOPO_DEMO = 8.575619088107132
E_RISP_DEMO = 20546.28547135721
RISP_DEMO = 41687.876891061045
CO2_DEMO = 6.1638856414071626
CAPEX_DEMO = 45000.0
VAN_DEMO = 359883.0401362784
TIR_DEMO = 0.9263476304696108
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w658_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _helpers_src():
    return (_new_dir() / "w658_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w658_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh658_num"](True, "x")

    def test_num_rifiuta_inf(self):
        with pytest.raises(ValueError):
            _F["mh658_num"](float("inf"), "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh658_num"](float("nan"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh658_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh658_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh658_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh658_int_pos"](True, "x")

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh658_frazione"](1.1, "x")

    def test_cosphi_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh658_cosphi"](0.0, "x")

    def test_cosphi_accetta_uno(self):
        assert _F["mh658_cosphi"](1.0, "x") == 1.0


class TestFisica:
    def test_tan_da_cosphi_demo(self):
        assert _F["mh658_tan_da_cosphi"](0.82) == pytest.approx(TAN0_DEMO)

    def test_tan_da_cosphi_target(self):
        assert _F["mh658_tan_da_cosphi"](0.97) == pytest.approx(TAN1_DEMO)

    def test_tan_da_cosphi_uno_zero(self):
        assert _F["mh658_tan_da_cosphi"](1.0) == pytest.approx(0.0)

    def test_qc_kvar_demo(self):
        assert _F["mh658_qc_kvar"](500.0, 0.82, 0.97) == \
            pytest.approx(QC_DEMO)

    def test_qc_kvar_zero_se_target_peggiore(self):
        assert _F["mh658_qc_kvar"](500.0, 0.97, 0.82) == pytest.approx(0.0)

    def test_q_eccesso_demo(self):
        assert _F["mh658_q_eccesso_kvar"](500.0, 0.82, 0.95) == \
            pytest.approx(Q_ECCESSO_DEMO)

    def test_q_eccesso_zero_se_sopra_soglia(self):
        assert _F["mh658_q_eccesso_kvar"](500.0, 0.97, 0.95) == \
            pytest.approx(0.0)

    def test_energia_reattiva_demo(self):
        assert _F["mh658_energia_reattiva_kvarh"](Q_ECCESSO_DEMO,
                                                  6000.0) == \
            pytest.approx(E_REATTIVA_DEMO)

    def test_penali_demo(self):
        assert _F["mh658_penali_annue"](E_REATTIVA_DEMO, 0.035) == \
            pytest.approx(PENALI_DEMO)

    def test_perdite_dopo_demo(self):
        assert _F["mh658_perdite_dopo_kw"](12.0, 0.82, 0.97) == \
            pytest.approx(PERDITE_DOPO_DEMO)

    def test_perdite_dopo_invariante_se_cos_uguali(self):
        assert _F["mh658_perdite_dopo_kw"](12.0, 0.95, 0.95) == \
            pytest.approx(12.0)

    def test_energia_risparmiata_demo(self):
        assert _F["mh658_energia_risparmiata_kwh"](12.0, PERDITE_DOPO_DEMO,
                                                  6000.0) == \
            pytest.approx(E_RISP_DEMO)

    def test_capex_da_specifico(self):
        assert _F["mh658_capex_da_specifico"](QC_DEMO, 200.0) == \
            pytest.approx(QC_DEMO * 200.0)

    def test_banco_detunato_false_demo(self):
        assert _F["mh658_banco_detunato"](0.06) is False

    def test_banco_detunato_true_sopra_soglia(self):
        assert _F["mh658_banco_detunato"](0.08) is True

    def test_banco_detunato_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh658_banco_detunato"](-0.01)


class TestEconomia:
    def test_risparmio_annuo_demo(self):
        assert _F["mh658_risparmio_annuo"](PENALI_DEMO, E_RISP_DEMO,
                                           0.20, 1200.0) == \
            pytest.approx(RISP_DEMO)

    def test_risparmio_annuo_negativo_possibile(self):
        assert _F["mh658_risparmio_annuo"](100.0, 1000.0, 0.10,
                                           500.0) == pytest.approx(-300.0)

    def test_co2_demo(self):
        assert _F["mh658_co2_t"](E_RISP_DEMO, 0.30) == \
            pytest.approx(CO2_DEMO)

    def test_co2_none_se_non_positiva(self):
        assert _F["mh658_co2_t"](0.0, 0.30) is None
        assert _F["mh658_co2_t"](-5.0, 0.30) is None


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh658_flussi"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)

    def test_flussi_struttura(self):
        fl = _F["mh658_flussi"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_van_demo(self):
        assert _F["mh658_van"](self._flussi_demo(), 6.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh658_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh658_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh658_payback"](self._flussi_demo()) == 2

    def test_payback_none_mai(self):
        assert _F["mh658_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh658_verdetto"](VAN_DEMO, CAPEX_DEMO, RISP_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale(self):
        assert _F["mh658_verdetto"](-2000.0, 45000.0, 1000.0,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh658_verdetto"](-20000.0, 45000.0, 1000.0,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh658_verdetto"](500.0, 45000.0, 0.0,
                                    0.10) == "NON_CALCOLABILE"
        assert _F["mh658_verdetto"](500.0, 45000.0, None,
                                    0.10) == "NON_CALCOLABILE"
        assert _F["mh658_verdetto"](None, 45000.0, 1000.0,
                                    0.10) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh658_demo_calcoli"]()
        assert c["tan0"] == pytest.approx(TAN0_DEMO)
        assert c["tan1"] == pytest.approx(TAN1_DEMO)
        assert c["tan_soglia"] == pytest.approx(TAN_SOGLIA_DEMO)
        assert c["qc_kvar"] == pytest.approx(QC_DEMO)
        assert c["q_eccesso_kvar"] == pytest.approx(Q_ECCESSO_DEMO)
        assert c["e_reattiva_kvarh"] == pytest.approx(E_REATTIVA_DEMO)
        assert c["penali_eur_anno"] == pytest.approx(PENALI_DEMO)
        assert c["perdite_dopo_kw"] == pytest.approx(PERDITE_DOPO_DEMO)
        assert c["e_risp_kwh"] == pytest.approx(E_RISP_DEMO)
        assert c["capex_eur"] == CAPEX_DEMO
        assert c["risparmio_eur_anno"] == pytest.approx(RISP_DEMO)
        assert c["co2_t"] == pytest.approx(CO2_DEMO)
        assert c["van_eur"] == pytest.approx(VAN_DEMO)
        assert c["tir"] == pytest.approx(TIR_DEMO)
        assert c["payback"] == 2
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["banco_detunato"] is False

    def test_demo_defaults(self):
        d = _F["mh658_demo"]()
        assert d["p_kw"] == 500.0
        assert d["cos0"] == 0.82
        assert d["cos1"] == 0.97
        assert d["soglia_cos"] == 0.95
        assert d["capex_eur"] == 45000.0
        assert d["vita_anni"] == 15


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W658 (23/10/2026) - tab658' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh658_num", "mh658_nneg", "mh658_pos",
                     "mh658_int_pos", "mh658_frazione", "mh658_cosphi",
                     "mh658_tan_da_cosphi", "mh658_qc_kvar",
                     "mh658_q_eccesso_kvar",
                     "mh658_energia_reattiva_kvarh", "mh658_penali_annue",
                     "mh658_perdite_dopo_kw",
                     "mh658_energia_risparmiata_kwh",
                     "mh658_capex_da_specifico", "mh658_risparmio_annuo",
                     "mh658_co2_t", "mh658_flussi", "mh658_van",
                     "mh658_tir", "mh658_payback", "mh658_verdetto",
                     "mh658_banco_detunato", "mh658_demo",
                     "mh658_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE658) == 1

    def test_blocco_with_tab658(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab658:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st658_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st657_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg658" in src
        assert "(_rs658 is None) or (_rs658 <= 0.0)" in src

    def test_csv_filename(self):
        assert "rifasamento.csv" in _ui_src()

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
