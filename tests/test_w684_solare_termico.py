"""Test tab684 "☀️🔥 Solare termico: calore dal sole senza fotovoltaico?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
100 m2 di collettori con irraggiamento 1200
kWh/m2/anno e rendimento medio 50 % (60000
kWh/anno di calore solare), fabbisogno 80000
kWh/anno (copertura 75 %), caldaia a rendimento
90 %; gas 0,09 EUR/kWh; elettricita' 0,25 EUR/kWh;
ausiliario 10 kWh/m2/anno; fattore gas 0,20
kg/kWh; OPEX 8 EUR/m2/anno; CAPEX 600 EUR/m2;
vita 25 anni; WACC 0,05 (5 %); tolleranza 0,10
(10 % del CAPEX).

- q_solare_kwh = 60000.0
- q_utile_kwh = 60000.0
- copertura = 0.75
- gas_risparmiato_kwh = 66666.66666666667
- c_base_eur = 6000.0
- opex_eur = 800.0
- costo_aux_eur = 250.0
- costo_solare_eur = 1050.0
- risparmio_eur = 4950.0
- co2_evitata_t = 13.333333333333336
- capex_eur = 60000.0
- crf = 0.0709524572992296
- van = 9765.025601921574
- tir = 6.568271364934014 (in uscita: percentuale)
- payback = 13
- verdetto = 'CONVIENTE'
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w684_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w684_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w684_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w684_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w684_helpers.py: {missing}")
    return out


_F = _load("mh684_num", "mh684_nneg", "mh684_pos",
           "mh684_int_pos", "mh684_rendimento",
           "mh684_tol", "mh684_q_solare",
           "mh684_q_utile", "mh684_copertura",
           "mh684_gas_risparmiato", "mh684_c_base",
           "mh684_costo_aux", "mh684_opex",
           "mh684_costo_solare", "mh684_risparmio",
           "mh684_co2_evitata", "mh684_capex",
           "mh684_crf", "mh684_van", "mh684_tir",
           "mh684_payback", "mh684_verdetto",
           "_mh684_neutro", "mh684_calcola",
           "mh684_sensitivita", "mh684_csv",
           "mh684_demo", "demo_calcoli")

TITLE684 = ("☀️🔥 Solare termico: calore dal sole "
            "senza fotovoltaico?")

QS_DEMO = 60000.0
QU_DEMO = 60000.0
COP_DEMO = 0.75
GAS_DEMO = 66666.66666666667
CB_DEMO = 6000.0
OPEX_DEMO = 800.0
AUX_DEMO = 250.0
CSOL_DEMO = 1050.0
RISP_DEMO = 4950.0
CO2_DEMO = 13.333333333333336
CAPEX_DEMO = 60000.0
CRF_DEMO = 0.0709524572992296
VAN_DEMO = 9765.025601921574
TIR_DEMO = 6.568271364934014
PAYBACK_DEMO = 13
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w684_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w684_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh684_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh684_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh684_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh684_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh684_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh684_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh684_int_pos"](25.0, "x") == 25

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_rendimento"](0.0, "x")

    def test_rendimento_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh684_rendimento"](1.01, "x")

    def test_rendimento_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_rendimento"](-0.01, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh684_rendimento"](1.0, "x") == 1.0

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh684_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh684_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh684_tol"](0.0, "x") == 0.0
        assert _F["mh684_tol"](1.0, "x") == 1.0


class TestFisica:
    def test_q_solare_demo(self):
        assert _F["mh684_q_solare"](
            100.0, 1200.0, 0.50) == pytest.approx(QS_DEMO,
                                                 rel=REL)

    def test_q_solare_formula(self):
        assert _F["mh684_q_solare"](
            50.0, 1000.0, 0.6) == pytest.approx(30000.0,
                                                rel=1e-12)

    def test_q_solare_zero_se_eta_piccola(self):
        assert _F["mh684_q_solare"](
            100.0, 1200.0, 0.01) == pytest.approx(1200.0,
                                                  rel=1e-12)

    def test_q_solare_rifiuta_area_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_q_solare"](0.0, 1200.0, 0.50)

    def test_q_solare_rifiuta_irraggiamento_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_q_solare"](100.0, 0.0, 0.50)

    def test_q_solare_rifiuta_eta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh684_q_solare"](100.0, 1200.0, 1.01)

    def test_q_solare_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_q_solare"](100.0, 1200.0, 0.0)

    def test_q_utile_demo(self):
        assert _F["mh684_q_utile"](
            QS_DEMO, 80000.0) == pytest.approx(QU_DEMO,
                                               rel=REL)

    def test_q_utile_cappato_dal_fabbisogno(self):
        # calore solare 60000 > fabbisogno 40000
        assert _F["mh684_q_utile"](
            QS_DEMO, 40000.0) == pytest.approx(40000.0,
                                               rel=REL)

    def test_q_utile_uguale_solare_se_sotto_fabbisogno(self):
        assert _F["mh684_q_utile"](
            30000.0, 80000.0) == pytest.approx(30000.0,
                                               rel=REL)

    def test_q_utile_zero_se_solare_zero(self):
        assert _F["mh684_q_utile"](0.0, 80000.0) == 0.0

    def test_q_utile_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh684_q_utile"](-1.0, 80000.0)
        with pytest.raises(ValueError):
            _F["mh684_q_utile"](QS_DEMO, -1.0)

    def test_copertura_demo(self):
        assert _F["mh684_copertura"](
            QU_DEMO, 80000.0) == pytest.approx(COP_DEMO,
                                               rel=REL)

    def test_copertura_uno_se_cappata(self):
        assert _F["mh684_copertura"](
            40000.0, 40000.0) == pytest.approx(1.0, rel=1e-12)

    def test_copertura_rifiuta_fabbisogno_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_copertura"](QU_DEMO, 0.0)

    def test_gas_risparmiato_demo(self):
        assert _F["mh684_gas_risparmiato"](
            QU_DEMO, 0.90) == pytest.approx(GAS_DEMO, rel=REL)

    def test_gas_risparmiato_formula(self):
        # 9000 kWh utili / 0,90 = 10000 kWh di gas
        assert _F["mh684_gas_risparmiato"](
            9000.0, 0.90) == pytest.approx(10000.0, rel=1e-12)

    def test_gas_risparmiato_uguale_se_eta_uno(self):
        assert _F["mh684_gas_risparmiato"](
            QU_DEMO, 1.0) == pytest.approx(QU_DEMO, rel=REL)

    def test_gas_risparmiato_rifiuta_eta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh684_gas_risparmiato"](QU_DEMO, 1.01)

    def test_gas_risparmiato_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_gas_risparmiato"](QU_DEMO, 0.0)

    def test_c_base_demo(self):
        assert _F["mh684_c_base"](
            GAS_DEMO, 0.09) == pytest.approx(CB_DEMO, rel=REL)

    def test_c_base_zero_se_prezzo_zero(self):
        assert _F["mh684_c_base"](GAS_DEMO, 0.0) == 0.0

    def test_c_base_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_c_base"](GAS_DEMO, -0.01)

    def test_costo_aux_demo(self):
        assert _F["mh684_costo_aux"](
            100.0, 10.0, 0.25) == pytest.approx(AUX_DEMO,
                                                rel=REL)

    def test_costo_aux_zero_se_aux_zero(self):
        assert _F["mh684_costo_aux"](100.0, 0.0, 0.25) == 0.0

    def test_costo_aux_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh684_costo_aux"](100.0, -0.01, 0.25)
        with pytest.raises(ValueError):
            _F["mh684_costo_aux"](100.0, 10.0, -0.01)

    def test_opex_demo(self):
        assert _F["mh684_opex"](
            100.0, 8.0) == pytest.approx(OPEX_DEMO, rel=REL)

    def test_opex_zero_se_unitario_zero(self):
        assert _F["mh684_opex"](100.0, 0.0) == 0.0

    def test_costo_solare_demo(self):
        assert _F["mh684_costo_solare"](
            OPEX_DEMO, AUX_DEMO) == pytest.approx(CSOL_DEMO,
                                                  rel=REL)

    def test_costo_solare_somma(self):
        assert _F["mh684_costo_solare"](
            300.0, 700.0) == 1000.0

    def test_risparmio_demo(self):
        assert _F["mh684_risparmio"](
            CB_DEMO, CSOL_DEMO) == pytest.approx(RISP_DEMO,
                                                 rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh684_risparmio"](100.0, 250.0) == -150.0

    def test_risparmio_zero_se_pareggio(self):
        assert _F["mh684_risparmio"](1000.0, 1000.0) == 0.0

    def test_co2_demo(self):
        assert _F["mh684_co2_evitata"](
            GAS_DEMO, 0.20) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_formula(self):
        # 10000 kWh x 0,20 kg/kWh / 1000 = 2,0 t
        assert _F["mh684_co2_evitata"](
            10000.0, 0.20) == pytest.approx(2.0, rel=1e-12)

    def test_co2_zero_se_fattore_zero(self):
        assert _F["mh684_co2_evitata"](GAS_DEMO, 0.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_co2_evitata"](GAS_DEMO, -0.01)

    def test_capex_demo(self):
        assert _F["mh684_capex"](
            100.0, 600.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_zero_se_unitario_zero(self):
        assert _F["mh684_capex"](100.0, 0.0) == 0.0

    def test_capex_rifiuta_area_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_capex"](0.0, 600.0)

    def test_capex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_capex"](100.0, -1.0)

    def test_crf_demo(self):
        assert _F["mh684_crf"](
            0.05, 25) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh684_crf"](
            0.0, 25) == pytest.approx(1.0 / 25.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_crf"](-0.01, 25)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh684_crf"](0.05, 0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh684_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh684_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            25) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 25, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + RISP_DEMO * 25 == pytest.approx(
            63750.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 25)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh684_van"](RISP_DEMO, -1.0, 0.05, 25)

    def test_tir_demo(self):
        assert _F["mh684_tir"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh684_tir"](CAPEX_DEMO, 0.0, 25) is None
        assert _F["mh684_tir"](CAPEX_DEMO, -100.0, 25) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh684_tir"](0.0, RISP_DEMO, 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh684_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh684_payback"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_ceil_arrotonda_su(self):
        # 1000 / 300 = 3,33... -> 4
        assert _F["mh684_payback"](1000.0, 300.0, 25) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh684_payback"](1000.0, 1000.0, 25) == 1
        assert _F["mh684_payback"](1000.0, 2000.0, 25) == 1

    def test_payback_oltre_vita_ceil_puro(self):
        # ceil puro senza tetto di vita: 60000/100 = 600
        assert _F["mh684_payback"](CAPEX_DEMO, 100.0, 25) == 600

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh684_payback"](0.0, RISP_DEMO, 25) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh684_payback"](CAPEX_DEMO, 0.0, 25) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh684_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, RISP_DEMO,
            QU_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh684_verdetto"](
            -5000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            QU_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh684_verdetto"](
            -7000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            QU_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh684_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            QU_DEMO) == "NON_CALCOLABILE"
        assert _F["mh684_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0,
            QU_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_q_utile_zero(self):
        assert _F["mh684_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh684_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO,
            QU_DEMO) == "CONVIENTE"
        assert _F["mh684_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO,
            QU_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh684_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO,
            QU_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh684_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO,
            QU_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh684_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 RISP_DEMO, QU_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh684_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 RISP_DEMO, QU_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh684_demo"]()
        d.update(kw)
        return _F["mh684_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["q_solare_kwh"] == pytest.approx(QS_DEMO,
                                                  rel=REL)
        assert c["q_utile_kwh"] == pytest.approx(QU_DEMO,
                                                 rel=REL)
        assert c["copertura"] == pytest.approx(COP_DEMO,
                                                rel=REL)
        assert c["gas_risparmiato_kwh"] == pytest.approx(
            GAS_DEMO, rel=REL)
        assert c["c_base_eur"] == pytest.approx(CB_DEMO,
                                                rel=REL)
        assert c["opex_eur"] == pytest.approx(OPEX_DEMO,
                                              rel=REL)
        assert c["costo_aux_eur"] == pytest.approx(AUX_DEMO,
                                                   rel=REL)
        assert c["costo_solare_eur"] == pytest.approx(
            CSOL_DEMO, rel=REL)
        assert c["risparmio_eur"] == pytest.approx(RISP_DEMO,
                                                   rel=REL)
        assert c["co2_evitata_t"] == pytest.approx(CO2_DEMO,
                                                   rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO,
                                               rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "co2_evitata_t"] == _F["demo_calcoli"]()[
            "co2_evitata_t"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh684_calcola(**mh684_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh684_demo"]()
        b = _F["mh684_calcola"](**d)
        coppie = [("q_solare_kwh", QS_DEMO),
                  ("q_utile_kwh", QU_DEMO),
                  ("copertura", COP_DEMO),
                  ("gas_risparmiato_kwh", GAS_DEMO),
                  ("c_base_eur", CB_DEMO),
                  ("opex_eur", OPEX_DEMO),
                  ("costo_aux_eur", AUX_DEMO),
                  ("costo_solare_eur", CSOL_DEMO),
                  ("risparmio_eur", RISP_DEMO),
                  ("co2_evitata_t", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO),
                  ("crf", CRF_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh684_demo"]()
        assert d["area_m2"] == 100.0
        assert d["irraggiamento_kwh_m2_a"] == 1200.0
        assert d["eta_media"] == 0.50
        assert d["fabbisogno_kwh_a"] == 80000.0
        assert d["eta_caldaia"] == 0.90
        assert d["prezzo_gas_eur_kwh"] == 0.09
        assert d["prezzo_el_eur_kwh"] == 0.25
        assert d["e_aux_kwh_m2_a"] == 10.0
        assert d["fattore_gas_kg_kwh"] == 0.20
        assert d["opex_eur_m2_a"] == 8.0
        assert d["capex_eur_m2"] == 600.0
        assert d["vita_anni"] == 25
        assert d["wacc"] == 0.05
        assert d["tol_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_solare_kwh", "q_utile_kwh",
                       "copertura", "gas_risparmiato_kwh",
                       "c_base_eur", "opex_eur",
                       "costo_aux_eur", "costo_solare_eur",
                       "risparmio_eur", "co2_evitata_t",
                       "capex_eur", "crf", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 13" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_area_zero_neutro(self):
        n = self._bc(area_m2=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["q_utile_kwh"] == 0.0
        assert n["risparmio_eur"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_area_negativa_neutro(self):
        n = self._bc(area_m2=-10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_eta_oltre_uno_neutro(self):
        n = self._bc(eta_media=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_zero_neutro(self):
        n = self._bc(eta_media=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_caldaia_oltre_uno_neutro(self):
        n = self._bc(eta_caldaia=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_caldaia_zero_neutro(self):
        n = self._bc(eta_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_irraggiamento_zero_neutro(self):
        n = self._bc(irraggiamento_kwh_m2_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fabbisogno_zero_neutro(self):
        n = self._bc(fabbisogno_kwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_negativi_neutro(self):
        for k in ("prezzo_gas_eur_kwh",
                  "prezzo_el_eur_kwh",
                  "fattore_gas_kg_kwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_opex_aux_capex_negativi_neutro(self):
        for k in ("opex_eur_m2_a", "e_aux_kwh_m2_a",
                  "capex_eur_m2"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=24.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tol_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_uno_neutro(self):
        n = self._bc(tol_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_gas_eur_kwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(area_m2=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_gas_basso_risparmio_negativo_neutro(self):
        # gas a 0,01 EUR/kWh: 666,67 - 1050 < 0
        n = self._bc(prezzo_gas_eur_kwh=0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -60000 + 4950 x 25 = 63750
        n = self._bc(wacc=0.0)
        assert n["van"] == pytest.approx(63750.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_m2=0.0)
        assert n["capex_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0

    def test_q_cappato_calcolabile(self):
        # fabbisogno 40000: utile 40000, copertura 1,0
        n = self._bc(fabbisogno_kwh_a=40000.0)
        assert n["valid"] is True
        assert n["q_solare_kwh"] == pytest.approx(QS_DEMO,
                                                  rel=REL)
        assert n["q_utile_kwh"] == pytest.approx(40000.0,
                                                 rel=REL)
        assert n["copertura"] == pytest.approx(1.0, rel=REL)

    def test_eta_piena_calcolabile(self):
        n = self._bc(eta_media=1.0)
        assert n["valid"] is True
        assert n["q_solare_kwh"] == pytest.approx(120000.0,
                                                  rel=REL)
        assert n["q_utile_kwh"] == pytest.approx(80000.0,
                                                 rel=REL)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh684_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh684_neutro"]()
        for chiave in ("valid", "q_solare_kwh",
                       "q_utile_kwh", "copertura",
                       "gas_risparmiato_kwh",
                       "c_base_eur", "opex_eur",
                       "costo_aux_eur", "costo_solare_eur",
                       "risparmio_eur", "co2_evitata_t",
                       "capex_eur", "crf", "van", "tir",
                       "payback", "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 13
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Calore utile (kWh/anno)" in voci
        assert "Copertura solare (frazione)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh684_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh684_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Irraggiamento x0.8",
                                   "Irraggiamento x1.0",
                                   "Irraggiamento x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh684_sensitivita"](self._ing())
        assert s.loc["x1.0", "Irraggiamento x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh684_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Irraggiamento x1.0"]
        assert s.loc["x0.8", "Irraggiamento x0.8"] < centro
        assert s.loc["x1.0", "Irraggiamento x0.8"] < centro
        assert s.loc["x1.2", "Irraggiamento x1.0"] > centro
        assert s.loc["x0.8", "Irraggiamento x1.0"] < centro
        assert s.loc["x1.2", "Irraggiamento x1.2"] > centro

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi i fattori sono senza tetto
        # (prezzo e irraggiamento): nessuna cella
        # puo' essere 0,0 per regime degenere
        s = _F["mh684_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_crescente_in_entrambi_i_fattori(self):
        s = _F["mh684_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Irraggiamento x0.8"] < \
                s.loc[riga, "Irraggiamento x1.0"] < \
                s.loc[riga, "Irraggiamento x1.2"]
        for colonna in ("Irraggiamento x0.8",
                        "Irraggiamento x1.0",
                        "Irraggiamento x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh684_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh684_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_anno" in txt
        assert "gas_risparmiato_kwh_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "q_utile_kwh_anno" in txt
        assert "risparmio_eur_anno" in txt
        assert "prezzo_gas_eur_kwh" in txt
        assert "eta_media_frazione" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh684_csv"](bc, self._ing())
        assert f"q_utile_kwh_anno;{QU_DEMO}" in txt
        assert f"risparmio_eur_anno;{RISP_DEMO}" in txt
        assert f"costo_solare_eur_anno;{CSOL_DEMO}" in txt
        assert f"co2_evitata_t_anno;{CO2_DEMO}" in txt
        assert f"c_base_eur_anno;{CB_DEMO}" in txt
        assert f"q_solare_kwh_anno;{QS_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def684["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def684\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh684_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W684 (24/10/2026) - tab684' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh684_num", "mh684_nneg", "mh684_pos",
                     "mh684_int_pos", "mh684_rendimento",
                     "mh684_tol", "mh684_q_solare",
                     "mh684_q_utile", "mh684_copertura",
                     "mh684_gas_risparmiato",
                     "mh684_c_base", "mh684_costo_aux",
                     "mh684_opex", "mh684_costo_solare",
                     "mh684_risparmio", "mh684_co2_evitata",
                     "mh684_capex", "mh684_crf",
                     "mh684_van", "mh684_tir",
                     "mh684_payback", "mh684_verdetto",
                     "_mh684_neutro", "mh684_calcola",
                     "mh684_sensitivita", "mh684_csv",
                     "mh684_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        # il frammento UI e' indentato di 4 spazi per
        # l'apply (come w683_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w684_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE684) == 1

    def test_blocco_with_tab684(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab684:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE684

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st684_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st683_") for k in keys)
        assert not any(k.startswith("st682_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg684" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg684") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg684")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Calore utile (kWh/anno)" in src
        assert "Copertura solare (%)" in src
        assert "Risparmio (€/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd684" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_calore_diretto_presente(self):
        src = _ui_src()
        assert "calore diretto" in src.lower()
        assert "fotovoltaico" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo gas evitato" in src
        assert "Risparmio annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh684_csv" in src
        assert "solare_termico_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh684_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo del gas" in src
        assert "Irraggiamento" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st684_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W684 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab684:")
        assert "mh684_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab684" in (_new_dir() / "w684_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w684_helpers.py", "w684_ui.py",
                   "w684_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab683" not in src
        assert "tab682" not in src
        assert "tab681" not in src
