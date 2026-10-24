"""Test tab682 "🌬️🧪 DAC: la cattura diretta di CO2 dall'aria paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
impianto DAC da 10000 t/anno all'85 % di utilizzo
(8500 t catturate), consumo elettrico 0,50 MWh/t e
termico 1,80 MWh/t; prezzo elettricita' 120 EUR/MWh,
calore 60 EUR/MWh; OPEX 80 EUR/t; CAPEX 800 EUR per
t/anno di capacita'; credito di carbonio 350 EUR/t;
fattori di emissione 0,35 / 0,20 kg/kWh; vita 20 anni;
WACC 5,0 %; tolleranza 10,0 % del CAPEX.

- catt_t = 8500.0
- e_el_mwh = 4250.0
- e_th_mwh = 15300.0
- costo_energia = 1428000.0
- opex_tot = 680000.0
- ricavi = 2975000.0
- margine = 867000.0
- co2_emessa_t = 4547.5
- co2_netta_t = 3952.5
- capex_tot = 8000000.0
- crf = 0.08024258719069129
- van = 2804736.366982173
- tir = 8.849615662517088 (in uscita: percentuale)
- payback = 10
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
    if (p / "w682_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w682_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w682_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w682_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w682_helpers.py: {missing}")
    return out


_F = _load("mh682_num", "mh682_nneg", "mh682_pos",
           "mh682_int_pos", "mh682_quota", "mh682_pct",
           "mh682_catt_t", "mh682_e_el_mwh",
           "mh682_e_th_mwh", "mh682_costo_energia",
           "mh682_opex_tot", "mh682_ricavi",
           "mh682_margine", "mh682_co2_emessa_t",
           "mh682_co2_netta_t", "mh682_capex_tot",
           "mh682_crf", "mh682_van", "mh682_tir",
           "mh682_payback", "mh682_verdetto",
           "_mh682_neutro", "mh682_calcola",
           "mh682_sensitivita", "mh682_csv",
           "mh682_demo", "demo_calcoli")

TITLE682 = ("🌬️🧪 DAC: la cattura diretta di CO2 "
            "dall'aria paga?")

CATT_DEMO = 8500.0
E_EL_DEMO = 4250.0
E_TH_DEMO = 15300.0
CEN_DEMO = 1428000.0
OPEX_DEMO = 680000.0
RIC_DEMO = 2975000.0
MARG_DEMO = 867000.0
EM_DEMO = 4547.5
NET_DEMO = 3952.5
CAPEX_DEMO = 8000000.0
CRF_DEMO = 0.08024258719069129
VAN_DEMO = 2804736.366982173
TIR_DEMO = 8.849615662517088
PAYBACK_DEMO = 10
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w682_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w682_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh682_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh682_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh682_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh682_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh682_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh682_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh682_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh682_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh682_int_pos"](20.0, "x") == 20

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh682_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh682_quota"](-0.01, "x")

    def test_quota_accetta_estremi(self):
        assert _F["mh682_quota"](0.0, "x") == 0.0
        assert _F["mh682_quota"](1.0, "x") == 1.0

    def test_pct_rifiuta_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh682_pct"](100.01, "x")

    def test_pct_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh682_pct"](-0.01, "x")

    def test_pct_accetta_estremi(self):
        assert _F["mh682_pct"](0.0, "x") == 0.0
        assert _F["mh682_pct"](100.0, "x") == 100.0
        assert _F["mh682_pct"](5.0, "x") == 5.0


class TestFisica:
    def test_catt_demo(self):
        assert _F["mh682_catt_t"](
            10000.0, 0.85) == pytest.approx(CATT_DEMO, rel=REL)

    def test_catt_formula(self):
        assert _F["mh682_catt_t"](
            1000.0, 0.5) == pytest.approx(500.0, rel=1e-12)

    def test_catt_zero_se_utilizzo_zero(self):
        assert _F["mh682_catt_t"](10000.0, 0.0) == 0.0

    def test_catt_rifiuta_capacita_zero(self):
        with pytest.raises(ValueError):
            _F["mh682_catt_t"](0.0, 0.85)

    def test_catt_rifiuta_utilizzo_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh682_catt_t"](10000.0, 1.01)

    def test_catt_rifiuta_utilizzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_catt_t"](10000.0, -0.01)

    def test_e_el_demo(self):
        assert _F["mh682_e_el_mwh"](
            CATT_DEMO, 0.50) == pytest.approx(E_EL_DEMO, rel=REL)

    def test_e_el_formula(self):
        assert _F["mh682_e_el_mwh"](
            1000.0, 0.5) == pytest.approx(500.0, rel=1e-12)

    def test_e_el_zero_se_consumo_zero(self):
        assert _F["mh682_e_el_mwh"](CATT_DEMO, 0.0) == 0.0

    def test_e_el_rifiuta_cattura_negativa(self):
        with pytest.raises(ValueError):
            _F["mh682_e_el_mwh"](-1.0, 0.50)

    def test_e_el_rifiuta_consumo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_e_el_mwh"](CATT_DEMO, -0.01)

    def test_e_th_demo(self):
        assert _F["mh682_e_th_mwh"](
            CATT_DEMO, 1.80) == pytest.approx(E_TH_DEMO, rel=REL)

    def test_e_th_formula(self):
        assert _F["mh682_e_th_mwh"](
            1000.0, 1.8) == pytest.approx(1800.0, rel=1e-12)

    def test_e_th_zero_se_consumo_zero(self):
        assert _F["mh682_e_th_mwh"](CATT_DEMO, 0.0) == 0.0

    def test_e_th_rifiuta_consumo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_e_th_mwh"](CATT_DEMO, -0.01)

    def test_costo_energia_demo(self):
        assert _F["mh682_costo_energia"](
            E_EL_DEMO, E_TH_DEMO, 120.0,
            60.0) == pytest.approx(CEN_DEMO, rel=REL)

    def test_costo_energia_scomposizione(self):
        # elettricita' 510000 + calore 918000
        assert E_EL_DEMO * 120.0 == pytest.approx(510000.0,
                                                  rel=REL)
        assert E_TH_DEMO * 60.0 == pytest.approx(918000.0,
                                                 rel=REL)

    def test_costo_energia_rifiuta_prezzi_negativi(self):
        with pytest.raises(ValueError):
            _F["mh682_costo_energia"](E_EL_DEMO, E_TH_DEMO,
                                      -0.01, 60.0)
        with pytest.raises(ValueError):
            _F["mh682_costo_energia"](E_EL_DEMO, E_TH_DEMO,
                                      120.0, -0.01)

    def test_opex_demo(self):
        assert _F["mh682_opex_tot"](
            CATT_DEMO, 80.0) == pytest.approx(OPEX_DEMO, rel=REL)

    def test_opex_zero_se_unitario_zero(self):
        assert _F["mh682_opex_tot"](CATT_DEMO, 0.0) == 0.0

    def test_opex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_opex_tot"](CATT_DEMO, -0.01)

    def test_ricavi_demo(self):
        assert _F["mh682_ricavi"](
            CATT_DEMO, 350.0) == pytest.approx(RIC_DEMO, rel=REL)

    def test_ricavi_zero_se_credito_zero(self):
        assert _F["mh682_ricavi"](CATT_DEMO, 0.0) == 0.0

    def test_ricavi_rifiuta_credito_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_ricavi"](CATT_DEMO, -0.01)

    def test_margine_demo(self):
        assert _F["mh682_margine"](
            RIC_DEMO, CEN_DEMO,
            OPEX_DEMO) == pytest.approx(MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh682_margine"](100.0, 200.0, 50.0) == -150.0

    def test_margine_zero_se_pareggio(self):
        assert _F["mh682_margine"](1000.0, 600.0, 400.0) == 0.0

    def test_co2_emessa_demo(self):
        assert _F["mh682_co2_emessa_t"](
            E_EL_DEMO, E_TH_DEMO, 0.35,
            0.20) == pytest.approx(EM_DEMO, rel=REL)

    def test_co2_emessa_scomposizione(self):
        # elettricita' 1487,5 t + calore 3060 t
        assert E_EL_DEMO * 0.35 == pytest.approx(1487.5,
                                                 rel=REL)
        assert E_TH_DEMO * 0.20 == pytest.approx(3060.0,
                                                 rel=REL)

    def test_co2_emessa_zero_se_tutto_zero(self):
        assert _F["mh682_co2_emessa_t"](
            0.0, 0.0, 0.35, 0.20) == 0.0

    def test_co2_emessa_rifiuta_fattori_negativi(self):
        with pytest.raises(ValueError):
            _F["mh682_co2_emessa_t"](E_EL_DEMO, E_TH_DEMO,
                                     -0.01, 0.20)
        with pytest.raises(ValueError):
            _F["mh682_co2_emessa_t"](E_EL_DEMO, E_TH_DEMO,
                                     0.35, -0.01)

    def test_co2_netta_demo(self):
        assert _F["mh682_co2_netta_t"](
            CATT_DEMO, EM_DEMO) == pytest.approx(NET_DEMO,
                                                 rel=REL)

    def test_co2_netta_negativa_se_energia_sporca(self):
        # fattori alti: 4250 x 0,80 + 15300 x 0,40
        # = 9520 t emesse > 8500 t catturate
        em = _F["mh682_co2_emessa_t"](E_EL_DEMO, E_TH_DEMO,
                                      0.80, 0.40)
        assert em == pytest.approx(9520.0, rel=REL)
        assert _F["mh682_co2_netta_t"](
            CATT_DEMO, em) == pytest.approx(-1020.0, rel=REL)

    def test_co2_netta_uguale_cattura_se_emissioni_zero(self):
        assert _F["mh682_co2_netta_t"](
            CATT_DEMO, 0.0) == CATT_DEMO

    def test_capex_demo(self):
        assert _F["mh682_capex_tot"](
            10000.0, 800.0) == pytest.approx(CAPEX_DEMO,
                                             rel=REL)

    def test_capex_zero_se_unitario_zero(self):
        assert _F["mh682_capex_tot"](10000.0, 0.0) == 0.0

    def test_capex_rifiuta_capacita_zero(self):
        with pytest.raises(ValueError):
            _F["mh682_capex_tot"](0.0, 800.0)

    def test_capex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_capex_tot"](10000.0, -1.0)

    def test_crf_demo(self):
        assert _F["mh682_crf"](
            5.0, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh682_crf"](
            0.0, 20) == pytest.approx(1.0 / 20.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_crf"](-0.01, 20)

    def test_crf_rifiuta_wacc_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh682_crf"](100.01, 20)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh682_crf"](5.0, 0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh682_van"](
            MARG_DEMO, CAPEX_DEMO, 5.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh682_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 20, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 20 == pytest.approx(
            9340000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh682_van"](MARG_DEMO, -1.0, 5.0, 20)

    def test_tir_demo(self):
        assert _F["mh682_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh682_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh682_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh682_tir"](0.0, MARG_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh682_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh682_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh682_payback"](1000.0, 1000.0, 20) == 1
        assert _F["mh682_payback"](1000.0, 2000.0, 20) == 1

    def test_payback_none_mai(self):
        assert _F["mh682_payback"](CAPEX_DEMO, 1.0, 20) is None

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh682_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh682_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 10.0, MARG_DEMO,
            CATT_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh682_verdetto"](
            -100000.0, CAPEX_DEMO, 10.0, MARG_DEMO,
            CATT_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh682_verdetto"](
            -900000.0, CAPEX_DEMO, 10.0, MARG_DEMO,
            CATT_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh682_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, 0.0,
            CATT_DEMO) == "NON_CALCOLABILE"
        assert _F["mh682_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, -50.0,
            CATT_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_cattura_zero(self):
        assert _F["mh682_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, MARG_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh682_verdetto"](
            0.0, 0.0, 10.0, MARG_DEMO,
            CATT_DEMO) == "CONVIENTE"
        assert _F["mh682_verdetto"](
            1000.0, 0.0, 10.0, MARG_DEMO,
            CATT_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh682_verdetto"](
            -1.0, 0.0, 10.0, MARG_DEMO,
            CATT_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh682_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO, CATT_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh682_verdetto"](100.0, CAPEX_DEMO, 100.01,
                                 MARG_DEMO, CATT_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh682_demo"]()
        d.update(kw)
        return _F["mh682_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["catt_t"] == pytest.approx(CATT_DEMO, rel=REL)
        assert c["e_el_mwh"] == pytest.approx(E_EL_DEMO, rel=REL)
        assert c["e_th_mwh"] == pytest.approx(E_TH_DEMO, rel=REL)
        assert c["costo_energia"] == pytest.approx(CEN_DEMO,
                                                  rel=REL)
        assert c["opex_tot"] == pytest.approx(OPEX_DEMO, rel=REL)
        assert c["ricavi"] == pytest.approx(RIC_DEMO, rel=REL)
        assert c["margine"] == pytest.approx(MARG_DEMO, rel=REL)
        assert c["co2_emessa_t"] == pytest.approx(EM_DEMO,
                                                  rel=REL)
        assert c["co2_netta_t"] == pytest.approx(NET_DEMO,
                                                 rel=REL)
        assert c["capex_tot"] == pytest.approx(CAPEX_DEMO,
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
            "co2_netta_t"] == _F["demo_calcoli"]()[
            "co2_netta_t"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh682_calcola(**mh682_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh682_demo"]()
        b = _F["mh682_calcola"](**d)
        coppie = [("catt_t", CATT_DEMO),
                  ("e_el_mwh", E_EL_DEMO),
                  ("e_th_mwh", E_TH_DEMO),
                  ("costo_energia", CEN_DEMO),
                  ("opex_tot", OPEX_DEMO),
                  ("ricavi", RIC_DEMO),
                  ("margine", MARG_DEMO),
                  ("co2_emessa_t", EM_DEMO),
                  ("co2_netta_t", NET_DEMO),
                  ("capex_tot", CAPEX_DEMO),
                  ("crf", CRF_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh682_demo"]()
        assert d["cap_t_a"] == 10000.0
        assert d["utilizzo"] == 0.85
        assert d["e_el_mwh_t"] == 0.50
        assert d["e_th_mwh_t"] == 1.80
        assert d["p_el_eur_mwh"] == 120.0
        assert d["p_th_eur_mwh"] == 60.0
        assert d["opex_eur_t"] == 80.0
        assert d["capex_eur_ta"] == 800.0
        assert d["credito_eur_t"] == 350.0
        assert d["f_el"] == 0.35
        assert d["f_th"] == 0.20
        assert d["vita_anni"] == 20
        assert d["wacc_pct"] == 5.0
        assert d["toll_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("catt_t", "e_el_mwh", "e_th_mwh",
                       "costo_energia", "opex_tot", "ricavi",
                       "margine", "co2_emessa_t",
                       "co2_netta_t", "capex_tot", "crf",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 10" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_capacita_zero_neutro(self):
        n = self._bc(cap_t_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["catt_t"] == 0.0
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_capacita_negativa_neutro(self):
        n = self._bc(cap_t_a=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_utilizzo_zero_neutro(self):
        n = self._bc(utilizzo=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["catt_t"] == 0.0

    def test_utilizzo_oltre_uno_neutro(self):
        n = self._bc(utilizzo=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_utilizzo_negativo_neutro(self):
        n = self._bc(utilizzo=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_consumi_negativi_neutro(self):
        for k in ("e_el_mwh_t", "e_th_mwh_t"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_prezzi_negativi_neutro(self):
        for k in ("p_el_eur_mwh", "p_th_eur_mwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_opex_negativo_neutro(self):
        n = self._bc(opex_eur_t=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_eur_ta=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fattori_negativi_neutro(self):
        for k in ("f_el", "f_th"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=19.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_oltre_100_neutro(self):
        n = self._bc(wacc_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(toll_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_100_neutro(self):
        n = self._bc(toll_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(p_el_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(cap_t_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_credito_zero_neutro(self):
        # ricavi zero: margine negativo -> neutro
        n = self._bc(credito_eur_t=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_margine_negativo_neutro(self):
        # credito basso: ricavi sotto i costi
        n = self._bc(credito_eur_t=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -8000000 + 867000 x 20 =
        # 9340000 -> CONVIENTE
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(9340000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_ta=0.0)
        assert n["capex_tot"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"

    def test_co2_netta_negativa_ma_calcolabile(self):
        # energia sporca: netta negativa, ma il
        # margine resta positivo -> calcolabile
        n = self._bc(f_el=0.80, f_th=0.40)
        assert n["valid"] is True
        assert n["co2_netta_t"] == pytest.approx(-1020.0,
                                                 rel=REL)

    def test_utilizzo_pieno_calcolabile(self):
        n = self._bc(utilizzo=1.0)
        assert n["valid"] is True
        assert n["catt_t"] == pytest.approx(10000.0, rel=REL)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh682_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh682_neutro"]()
        for chiave in ("valid", "catt_t", "e_el_mwh",
                       "e_th_mwh", "costo_energia",
                       "opex_tot", "ricavi", "margine",
                       "co2_emessa_t", "co2_netta_t",
                       "capex_tot", "crf", "van", "tir",
                       "payback", "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 12
        voci = b["df_tabella"]["Voce"].tolist()
        assert "CO2 catturata (t/anno)" in voci
        assert "Energia elettrica (MWh/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert "CO2 netta (t/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh682_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh682_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Utilizzo x0.8",
                                   "Utilizzo x1.0",
                                   "Utilizzo x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh682_sensitivita"](self._ing())
        assert s.loc["x1.0", "Utilizzo x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh682_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Utilizzo x1.0"]
        assert s.loc["x0.8", "Utilizzo x0.8"] < centro
        assert s.loc["x1.0", "Utilizzo x0.8"] < centro
        assert s.loc["x1.2", "Utilizzo x1.0"] > centro
        assert s.loc["x0.8", "Utilizzo x1.0"] < centro

    def test_sensitivita_colonna_utilizzo_12_degenere(self):
        # 0,85 x 1,2 = 1,02 > 1: la quota di utilizzo
        # esce da [0, 1] -> regime degenere, VAN 0,0
        # (stesso pattern di mh681_sensitivita, senza
        # clamp: la guard resta severa anche qui)
        s = _F["mh682_sensitivita"](self._ing())
        assert (s["Utilizzo x1.2"] == 0.0).all()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh682_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 30

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh682_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_netta_t_anno" in txt
        assert "co2_emessa_t_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "catt_t_anno" in txt
        assert "margine_eur_anno" in txt
        assert "credito_eur_t" in txt
        assert "utilizzo_frazione" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh682_csv"](bc, self._ing())
        assert f"catt_t_anno;{CATT_DEMO}" in txt
        assert f"margine_eur_anno;{MARG_DEMO}" in txt
        assert f"costo_energia_eur_anno;{CEN_DEMO}" in txt
        assert f"e_el_mwh_anno;{E_EL_DEMO}" in txt
        assert f"e_th_mwh_anno;{E_TH_DEMO}" in txt
        assert f"ricavi_eur_anno;{RIC_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def682["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def682\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh682_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W682 (24/10/2026) - tab682' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh682_num", "mh682_nneg", "mh682_pos",
                     "mh682_int_pos", "mh682_quota",
                     "mh682_pct", "mh682_catt_t",
                     "mh682_e_el_mwh", "mh682_e_th_mwh",
                     "mh682_costo_energia",
                     "mh682_opex_tot", "mh682_ricavi",
                     "mh682_margine", "mh682_co2_emessa_t",
                     "mh682_co2_netta_t", "mh682_capex_tot",
                     "mh682_crf", "mh682_van", "mh682_tir",
                     "mh682_payback", "mh682_verdetto",
                     "_mh682_neutro", "mh682_calcola",
                     "mh682_sensitivita", "mh682_csv",
                     "mh682_demo", "demo_calcoli"):
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
        # l'apply (come w681_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w682_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE682) == 1

    def test_blocco_with_tab682(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab682:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE682

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st682_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st681_") for k in keys)
        assert not any(k.startswith("st680_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg682" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg682") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg682")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "CO2 catturata (t/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src
        assert "TIR / Payback" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd682" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_catturata_netta_presente(self):
        src = _ui_src()
        assert "CO2 catturata vs CO2 netta" in src
        assert "energia sporca" in src.lower()

    def test_nota_onesta_credito_presente(self):
        src = _ui_src()
        assert "prezzo del credito" in src.lower()
        assert "200" in src

    def test_dac_vs_ccs_spiegato(self):
        src = _ui_src()
        assert "sorgente puntuale" in src.lower()
        assert "BECCS" in src
        assert "aria ambiente" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi da crediti" in src
        assert "Margine DAC" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh682_csv" in src
        assert "dac_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh682_sensitivita" in src
        assert "Heatmap" in src
        assert "Credito di carbonio" in src
        assert "Utilizzo" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st682_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W682 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab682:")
        assert "mh682_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab682" in (_new_dir() / "w682_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w682_helpers.py", "w682_ui.py",
                   "w682_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
