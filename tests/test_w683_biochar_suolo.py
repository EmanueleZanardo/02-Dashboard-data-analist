"""Test tab683 "🌱🔥 Biochar: il carbonio della biomassa resta nel suolo?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
10000 t/anno di biomassa secca con resa in biochar
del 30 % (3000 t di biochar), contenuto di carbonio
80 % e frazione stabile 80 %; fattore di processo
0,05 tCO2e/t; energia coprodotta 0,80 MWh/t; prezzo
energia 80 EUR/MWh; costo biomassa 40 EUR/t; OPEX 60
EUR/t di biomassa; CAPEX 500 EUR per t/anno; credito
di carbonio 150 EUR/tCO2e; prezzo agronomico del
biochar 300 EUR/t; vita 20 anni; WACC 5,0 %;
tolleranza 10,0 % del CAPEX.

- biochar_t = 3000.0
- c_stabile_t = 1920.0
- co2_lorda_t = 7040.0
- emissioni_processo_t = 500.0
- co2_netta_t = 6540.0
- energia_mwh = 8000.0
- costo_feedstock = 400000.0
- opex_tot = 600000.0
- costi_tot = 1000000.0
- ricavi_crediti = 981000.0
- ricavi_biochar = 900000.0
- ricavi_energia = 640000.0
- ricavi = 2521000.0
- margine = 1521000.0
- capex_tot = 5000000.0
- crf = 0.08024258719069129
- van = 13955021.931003325
- tir = 30.266356611390183 (in uscita: percentuale)
- payback = 4
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
    if (p / "w683_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w683_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w683_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w683_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w683_helpers.py: {missing}")
    return out


_F = _load("mh683_num", "mh683_nneg", "mh683_pos",
           "mh683_int_pos", "mh683_quota", "mh683_pct",
           "mh683_biochar_t", "mh683_c_stabile_t",
           "mh683_co2_lorda_t",
           "mh683_emissioni_processo_t",
           "mh683_co2_netta_t", "mh683_energia_mwh",
           "mh683_costo_feedstock", "mh683_opex_tot",
           "mh683_costi_tot", "mh683_ricavi_crediti",
           "mh683_ricavi_biochar", "mh683_ricavi_energia",
           "mh683_ricavi", "mh683_margine",
           "mh683_capex_tot", "mh683_crf", "mh683_van",
           "mh683_tir", "mh683_payback", "mh683_verdetto",
           "_mh683_neutro", "mh683_calcola",
           "mh683_sensitivita", "mh683_csv",
           "mh683_demo", "demo_calcoli")

TITLE683 = ("🌱🔥 Biochar: il carbonio della biomassa "
            "resta nel suolo?")

BIO_DEMO = 3000.0
CSTAB_DEMO = 1920.0
LORDA_DEMO = 7040.0
EM_DEMO = 500.0
NET_DEMO = 6540.0
EN_DEMO = 8000.0
CFEED_DEMO = 400000.0
OPEX_DEMO = 600000.0
CTOT_DEMO = 1000000.0
RCRED_DEMO = 981000.0
RBIO_DEMO = 900000.0
REN_DEMO = 640000.0
RIC_DEMO = 2521000.0
MARG_DEMO = 1521000.0
CAPEX_DEMO = 5000000.0
CRF_DEMO = 0.08024258719069129
VAN_DEMO = 13955021.931003325
TIR_DEMO = 30.266356611390183
PAYBACK_DEMO = 4
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w683_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w683_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh683_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh683_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh683_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh683_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh683_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh683_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh683_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh683_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh683_int_pos"](20.0, "x") == 20

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh683_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh683_quota"](-0.01, "x")

    def test_quota_accetta_estremi(self):
        assert _F["mh683_quota"](0.0, "x") == 0.0
        assert _F["mh683_quota"](1.0, "x") == 1.0

    def test_pct_rifiuta_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh683_pct"](100.01, "x")

    def test_pct_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh683_pct"](-0.01, "x")

    def test_pct_accetta_estremi(self):
        assert _F["mh683_pct"](0.0, "x") == 0.0
        assert _F["mh683_pct"](100.0, "x") == 100.0
        assert _F["mh683_pct"](5.0, "x") == 5.0


class TestFisica:
    def test_biochar_demo(self):
        assert _F["mh683_biochar_t"](
            10000.0, 0.30) == pytest.approx(BIO_DEMO, rel=REL)

    def test_biochar_formula(self):
        assert _F["mh683_biochar_t"](
            1000.0, 0.5) == pytest.approx(500.0, rel=1e-12)

    def test_biochar_zero_se_resa_zero(self):
        assert _F["mh683_biochar_t"](10000.0, 0.0) == 0.0

    def test_biochar_rifiuta_feedstock_zero(self):
        with pytest.raises(ValueError):
            _F["mh683_biochar_t"](0.0, 0.30)

    def test_biochar_rifiuta_resa_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh683_biochar_t"](10000.0, 1.01)

    def test_biochar_rifiuta_resa_negativa(self):
        with pytest.raises(ValueError):
            _F["mh683_biochar_t"](10000.0, -0.01)

    def test_c_stabile_demo(self):
        assert _F["mh683_c_stabile_t"](
            BIO_DEMO, 0.80,
            0.80) == pytest.approx(CSTAB_DEMO, rel=REL)

    def test_c_stabile_formula(self):
        assert _F["mh683_c_stabile_t"](
            1000.0, 0.5, 0.5) == pytest.approx(250.0, rel=1e-12)

    def test_c_stabile_zero_se_contenuto_zero(self):
        assert _F["mh683_c_stabile_t"](
            BIO_DEMO, 0.0, 0.80) == 0.0

    def test_c_stabile_zero_se_stabile_zero(self):
        assert _F["mh683_c_stabile_t"](
            BIO_DEMO, 0.80, 0.0) == 0.0

    def test_c_stabile_rifiuta_quote_fuori_intervallo(self):
        with pytest.raises(ValueError):
            _F["mh683_c_stabile_t"](BIO_DEMO, 1.01, 0.80)
        with pytest.raises(ValueError):
            _F["mh683_c_stabile_t"](BIO_DEMO, 0.80, -0.01)

    def test_co2_lorda_demo(self):
        assert _F["mh683_co2_lorda_t"](
            CSTAB_DEMO) == pytest.approx(LORDA_DEMO, rel=REL)

    def test_co2_lorda_rapporto_44_12(self):
        # 120 tC x 44/12 = 440 tCO2e
        assert _F["mh683_co2_lorda_t"](
            120.0) == pytest.approx(440.0, rel=1e-12)

    def test_co2_lorda_zero_se_c_zero(self):
        assert _F["mh683_co2_lorda_t"](0.0) == 0.0

    def test_co2_lorda_rifiuta_c_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_co2_lorda_t"](-1.0)

    def test_emissioni_processo_demo(self):
        assert _F["mh683_emissioni_processo_t"](
            10000.0, 0.05) == pytest.approx(EM_DEMO, rel=REL)

    def test_emissioni_processo_formula(self):
        assert _F["mh683_emissioni_processo_t"](
            2000.0, 0.10) == pytest.approx(200.0, rel=1e-12)

    def test_emissioni_processo_zero_se_fattore_zero(self):
        assert _F["mh683_emissioni_processo_t"](
            10000.0, 0.0) == 0.0

    def test_emissioni_processo_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_emissioni_processo_t"](10000.0, -0.01)

    def test_co2_netta_demo(self):
        assert _F["mh683_co2_netta_t"](
            LORDA_DEMO, EM_DEMO) == pytest.approx(NET_DEMO,
                                                 rel=REL)

    def test_co2_netta_negativa_se_processo_alto(self):
        # processo 8000 t > lorda 7040 t
        assert _F["mh683_co2_netta_t"](
            LORDA_DEMO, 8000.0) == pytest.approx(-960.0,
                                                 rel=REL)

    def test_co2_netta_uguale_lorda_se_processo_zero(self):
        assert _F["mh683_co2_netta_t"](LORDA_DEMO, 0.0) == \
            LORDA_DEMO

    def test_energia_demo(self):
        assert _F["mh683_energia_mwh"](
            10000.0, 0.80) == pytest.approx(EN_DEMO, rel=REL)

    def test_energia_formula(self):
        assert _F["mh683_energia_mwh"](
            1000.0, 1.5) == pytest.approx(1500.0, rel=1e-12)

    def test_energia_zero_se_specifica_zero(self):
        assert _F["mh683_energia_mwh"](10000.0, 0.0) == 0.0

    def test_energia_rifiuta_specifica_negativa(self):
        with pytest.raises(ValueError):
            _F["mh683_energia_mwh"](10000.0, -0.01)

    def test_costo_feedstock_demo(self):
        assert _F["mh683_costo_feedstock"](
            10000.0, 40.0) == pytest.approx(CFEED_DEMO,
                                            rel=REL)

    def test_costo_feedstock_zero_se_prezzo_zero(self):
        assert _F["mh683_costo_feedstock"](10000.0, 0.0) == 0.0

    def test_costo_feedstock_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_costo_feedstock"](10000.0, -0.01)

    def test_opex_demo(self):
        assert _F["mh683_opex_tot"](
            10000.0, 60.0) == pytest.approx(OPEX_DEMO, rel=REL)

    def test_opex_zero_se_unitario_zero(self):
        assert _F["mh683_opex_tot"](10000.0, 0.0) == 0.0

    def test_opex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_opex_tot"](10000.0, -0.01)

    def test_costi_tot_demo(self):
        assert _F["mh683_costi_tot"](
            CFEED_DEMO, OPEX_DEMO) == pytest.approx(
            CTOT_DEMO, rel=REL)

    def test_costi_tot_somma(self):
        assert _F["mh683_costi_tot"](
            300.0, 700.0) == 1000.0

    def test_ricavi_crediti_demo(self):
        assert _F["mh683_ricavi_crediti"](
            NET_DEMO, 150.0) == pytest.approx(RCRED_DEMO,
                                              rel=REL)

    def test_ricavi_crediti_negativi_se_netta_negativa(self):
        assert _F["mh683_ricavi_crediti"](
            -960.0, 150.0) == pytest.approx(-144000.0,
                                            rel=REL)

    def test_ricavi_crediti_zero_se_prezzo_zero(self):
        assert _F["mh683_ricavi_crediti"](NET_DEMO, 0.0) == 0.0

    def test_ricavi_crediti_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_ricavi_crediti"](NET_DEMO, -0.01)

    def test_ricavi_biochar_demo(self):
        assert _F["mh683_ricavi_biochar"](
            BIO_DEMO, 300.0) == pytest.approx(RBIO_DEMO,
                                              rel=REL)

    def test_ricavi_biochar_zero_se_prezzo_zero(self):
        assert _F["mh683_ricavi_biochar"](BIO_DEMO, 0.0) == 0.0

    def test_ricavi_biochar_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_ricavi_biochar"](BIO_DEMO, -0.01)

    def test_ricavi_energia_demo(self):
        assert _F["mh683_ricavi_energia"](
            EN_DEMO, 80.0) == pytest.approx(REN_DEMO, rel=REL)

    def test_ricavi_energia_zero_se_prezzo_zero(self):
        assert _F["mh683_ricavi_energia"](EN_DEMO, 0.0) == 0.0

    def test_ricavi_totali_demo(self):
        assert _F["mh683_ricavi"](
            RCRED_DEMO, RBIO_DEMO,
            REN_DEMO) == pytest.approx(RIC_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh683_margine"](
            RIC_DEMO, CTOT_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh683_margine"](100.0, 250.0) == -150.0

    def test_margine_zero_se_pareggio(self):
        assert _F["mh683_margine"](1000.0, 1000.0) == 0.0

    def test_capex_demo(self):
        assert _F["mh683_capex_tot"](
            10000.0, 500.0) == pytest.approx(CAPEX_DEMO,
                                             rel=REL)

    def test_capex_zero_se_unitario_zero(self):
        assert _F["mh683_capex_tot"](10000.0, 0.0) == 0.0

    def test_capex_rifiuta_feedstock_zero(self):
        with pytest.raises(ValueError):
            _F["mh683_capex_tot"](0.0, 500.0)

    def test_capex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_capex_tot"](10000.0, -1.0)

    def test_crf_demo(self):
        assert _F["mh683_crf"](
            5.0, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh683_crf"](
            0.0, 20) == pytest.approx(1.0 / 20.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_crf"](-0.01, 20)

    def test_crf_rifiuta_wacc_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh683_crf"](100.01, 20)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh683_crf"](5.0, 0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh683_van"](
            MARG_DEMO, CAPEX_DEMO, 5.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh683_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 20, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 20 == pytest.approx(
            25420000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh683_van"](MARG_DEMO, -1.0, 5.0, 20)

    def test_tir_demo(self):
        assert _F["mh683_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh683_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh683_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh683_tir"](0.0, MARG_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh683_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh683_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh683_payback"](1000.0, 1000.0, 20) == 1
        assert _F["mh683_payback"](1000.0, 2000.0, 20) == 1

    def test_payback_none_mai(self):
        assert _F["mh683_payback"](CAPEX_DEMO, 1.0, 20) is None

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh683_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh683_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 10.0, MARG_DEMO,
            BIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh683_verdetto"](
            -100000.0, CAPEX_DEMO, 10.0, MARG_DEMO,
            BIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh683_verdetto"](
            -600000.0, CAPEX_DEMO, 10.0, MARG_DEMO,
            BIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh683_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, 0.0,
            BIO_DEMO) == "NON_CALCOLABILE"
        assert _F["mh683_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, -50.0,
            BIO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_biochar_zero(self):
        assert _F["mh683_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, MARG_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh683_verdetto"](
            0.0, 0.0, 10.0, MARG_DEMO,
            BIO_DEMO) == "CONVIENTE"
        assert _F["mh683_verdetto"](
            1000.0, 0.0, 10.0, MARG_DEMO,
            BIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh683_verdetto"](
            -1.0, 0.0, 10.0, MARG_DEMO,
            BIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        # VAN negativo con CAPEX 0: tolleranza zero,
        # quindi NON_CONVIENTE e mai MARGINALE
        assert _F["mh683_verdetto"](
            -1.0, 0.0, 10.0, MARG_DEMO,
            BIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh683_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO, BIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh683_verdetto"](100.0, CAPEX_DEMO, 100.01,
                                 MARG_DEMO, BIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh683_demo"]()
        d.update(kw)
        return _F["mh683_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["biochar_t"] == pytest.approx(BIO_DEMO, rel=REL)
        assert c["c_stabile_t"] == pytest.approx(CSTAB_DEMO,
                                                 rel=REL)
        assert c["co2_lorda_t"] == pytest.approx(LORDA_DEMO,
                                                 rel=REL)
        assert c["emissioni_processo_t"] == pytest.approx(
            EM_DEMO, rel=REL)
        assert c["co2_netta_t"] == pytest.approx(NET_DEMO,
                                                 rel=REL)
        assert c["energia_mwh"] == pytest.approx(EN_DEMO,
                                                 rel=REL)
        assert c["costo_feedstock"] == pytest.approx(
            CFEED_DEMO, rel=REL)
        assert c["opex_tot"] == pytest.approx(OPEX_DEMO, rel=REL)
        assert c["costi_tot"] == pytest.approx(CTOT_DEMO,
                                               rel=REL)
        assert c["ricavi_crediti"] == pytest.approx(
            RCRED_DEMO, rel=REL)
        assert c["ricavi_biochar"] == pytest.approx(
            RBIO_DEMO, rel=REL)
        assert c["ricavi_energia"] == pytest.approx(
            REN_DEMO, rel=REL)
        assert c["ricavi"] == pytest.approx(RIC_DEMO, rel=REL)
        assert c["margine"] == pytest.approx(MARG_DEMO, rel=REL)
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
        """mh683_calcola(**mh683_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh683_demo"]()
        b = _F["mh683_calcola"](**d)
        coppie = [("biochar_t", BIO_DEMO),
                  ("c_stabile_t", CSTAB_DEMO),
                  ("co2_lorda_t", LORDA_DEMO),
                  ("emissioni_processo_t", EM_DEMO),
                  ("co2_netta_t", NET_DEMO),
                  ("energia_mwh", EN_DEMO),
                  ("costo_feedstock", CFEED_DEMO),
                  ("opex_tot", OPEX_DEMO),
                  ("costi_tot", CTOT_DEMO),
                  ("ricavi_crediti", RCRED_DEMO),
                  ("ricavi_biochar", RBIO_DEMO),
                  ("ricavi_energia", REN_DEMO),
                  ("ricavi", RIC_DEMO),
                  ("margine", MARG_DEMO),
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
        d = _F["mh683_demo"]()
        assert d["feedstock_t_a"] == 10000.0
        assert d["resa_biochar"] == 0.30
        assert d["contenuto_c"] == 0.80
        assert d["frazione_stabile"] == 0.80
        assert d["fattore_processo"] == 0.05
        assert d["energia_mwh_t"] == 0.80
        assert d["p_energia_eur_mwh"] == 80.0
        assert d["costo_feedstock_eur_t"] == 40.0
        assert d["opex_eur_t_feed"] == 60.0
        assert d["capex_eur_ta"] == 500.0
        assert d["prezzo_credito_eur_t"] == 150.0
        assert d["prezzo_biochar_eur_t"] == 300.0
        assert d["vita_anni"] == 20
        assert d["wacc_pct"] == 5.0
        assert d["toll_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("biochar_t", "c_stabile_t",
                       "co2_lorda_t",
                       "emissioni_processo_t", "co2_netta_t",
                       "energia_mwh", "costo_feedstock",
                       "opex_tot", "costi_tot",
                       "ricavi_crediti", "ricavi_biochar",
                       "ricavi_energia", "ricavi", "margine",
                       "capex_tot", "crf", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 4" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_feedstock_zero_neutro(self):
        n = self._bc(feedstock_t_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["biochar_t"] == 0.0
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_feedstock_negativo_neutro(self):
        n = self._bc(feedstock_t_a=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_resa_zero_neutro(self):
        n = self._bc(resa_biochar=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["biochar_t"] == 0.0

    def test_resa_oltre_uno_neutro(self):
        n = self._bc(resa_biochar=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_resa_negativa_neutro(self):
        n = self._bc(resa_biochar=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_contenuto_fuori_intervallo_neutro(self):
        for v in (1.01, -0.01):
            n = self._bc(contenuto_c=v)
            assert n["verdetto"] == "NON_CALCOLABILE", v

    def test_stabile_fuori_intervallo_neutro(self):
        for v in (1.01, -0.01):
            n = self._bc(frazione_stabile=v)
            assert n["verdetto"] == "NON_CALCOLABILE", v

    def test_fattore_processo_negativo_neutro(self):
        n = self._bc(fattore_processo=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_energia_specifica_negativa_neutro(self):
        n = self._bc(energia_mwh_t=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_negativi_neutro(self):
        for k in ("p_energia_eur_mwh",
                  "costo_feedstock_eur_t",
                  "opex_eur_t_feed",
                  "prezzo_credito_eur_t",
                  "prezzo_biochar_eur_t"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_eur_ta=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

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
        n = self._bc(p_energia_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(feedstock_t_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_zero_neutro(self):
        # crediti e biochar a zero: ricavi sotto i
        # costi (solo energia 640000 < 1000000)
        n = self._bc(prezzo_credito_eur_t=0.0,
                     prezzo_biochar_eur_t=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_margine_negativo_neutro(self):
        # biomassa cara: costo 400 EUR/t -> costi
        # 4600000 > ricavi 2521000
        n = self._bc(costo_feedstock_eur_t=400.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -5000000 + 1521000 x 20 =
        # 25420000 -> CONVIENTE
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(25420000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_ta=0.0)
        assert n["capex_tot"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"

    def test_co2_netta_negativa_ma_calcolabile(self):
        # processo pesante (1,0 tCO2e/t): netta
        # 7040 - 10000 = -2960 t, ma il margine
        # resta positivo -> calcolabile
        n = self._bc(fattore_processo=1.0)
        assert n["valid"] is True
        assert n["co2_netta_t"] == pytest.approx(-2960.0,
                                                 rel=REL)

    def test_resa_piena_calcolabile(self):
        n = self._bc(resa_biochar=1.0)
        assert n["valid"] is True
        assert n["biochar_t"] == pytest.approx(10000.0,
                                               rel=REL)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh683_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh683_neutro"]()
        for chiave in ("valid", "biochar_t",
                       "c_stabile_t", "co2_lorda_t",
                       "emissioni_processo_t",
                       "co2_netta_t", "energia_mwh",
                       "costo_feedstock", "opex_tot",
                       "costi_tot", "ricavi_crediti",
                       "ricavi_biochar", "ricavi_energia",
                       "ricavi", "margine", "capex_tot",
                       "crf", "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 17
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Biochar (t/anno)" in voci
        assert "Carbonio stabile (tC/anno)" in voci
        assert "CO2 netta (tCO2e/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh683_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh683_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Biochar x0.8",
                                   "Biochar x1.0",
                                   "Biochar x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh683_sensitivita"](self._ing())
        assert s.loc["x1.0", "Biochar x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh683_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Biochar x1.0"]
        assert s.loc["x0.8", "Biochar x0.8"] < centro
        assert s.loc["x1.0", "Biochar x0.8"] < centro
        assert s.loc["x1.2", "Biochar x1.0"] > centro
        assert s.loc["x0.8", "Biochar x1.0"] < centro
        assert s.loc["x1.2", "Biochar x1.2"] > centro

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi i fattori sono prezzi senza tetto:
        # nessuna cella puo' essere 0,0 per regime
        # degenere (lezione tab682: mai scalare una
        # quota con tetto [0, 1] di +20 %)
        s = _F["mh683_sensitivita"](self._ing())
        assert (s.values != 0.0).all()
        assert (s.values > 0.0).all()

    def test_sensitivita_crescente_in_entrambi_i_fattori(self):
        s = _F["mh683_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Biochar x0.8"] < \
                s.loc[riga, "Biochar x1.0"] < \
                s.loc[riga, "Biochar x1.2"]
        for colonna in ("Biochar x0.8", "Biochar x1.0",
                        "Biochar x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh683_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 30

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh683_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_netta_t_anno" in txt
        assert "emissioni_processo_t_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "biochar_t_anno" in txt
        assert "margine_eur_anno" in txt
        assert "prezzo_credito_eur_t" in txt
        assert "resa_biochar_frazione" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh683_csv"](bc, self._ing())
        assert f"biochar_t_anno;{BIO_DEMO}" in txt
        assert f"margine_eur_anno;{MARG_DEMO}" in txt
        assert f"costi_tot_eur_anno;{CTOT_DEMO}" in txt
        assert f"energia_mwh_anno;{EN_DEMO}" in txt
        assert f"ricavi_eur_anno;{RIC_DEMO}" in txt
        assert f"co2_netta_t_anno;{NET_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def683["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def683\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh683_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W683 (24/10/2026) - tab683' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh683_num", "mh683_nneg", "mh683_pos",
                     "mh683_int_pos", "mh683_quota",
                     "mh683_pct", "mh683_biochar_t",
                     "mh683_c_stabile_t",
                     "mh683_co2_lorda_t",
                     "mh683_emissioni_processo_t",
                     "mh683_co2_netta_t",
                     "mh683_energia_mwh",
                     "mh683_costo_feedstock",
                     "mh683_opex_tot", "mh683_costi_tot",
                     "mh683_ricavi_crediti",
                     "mh683_ricavi_biochar",
                     "mh683_ricavi_energia",
                     "mh683_ricavi", "mh683_margine",
                     "mh683_capex_tot", "mh683_crf",
                     "mh683_van", "mh683_tir",
                     "mh683_payback", "mh683_verdetto",
                     "_mh683_neutro", "mh683_calcola",
                     "mh683_sensitivita", "mh683_csv",
                     "mh683_demo", "demo_calcoli"):
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
        # l'apply (come w682_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w683_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE683) == 1

    def test_blocco_with_tab683(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab683:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE683

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st683_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st682_") for k in keys)
        assert not any(k.startswith("st681_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg683" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg683") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg683")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Biochar (t/anno)" in src
        assert "CO2 netta (tCO2e/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd683" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_solido_presente(self):
        src = _ui_src()
        assert "solido" in src.lower()
        assert "secoli" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi da crediti" in src
        assert "Margine biochar" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh683_csv" in src
        assert "biochar_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh683_sensitivita" in src
        assert "Heatmap" in src
        assert "Credito di carbonio" in src
        assert "Biochar" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st683_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W683 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab683:")
        assert "mh683_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab683" in (_new_dir() / "w683_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w683_helpers.py", "w683_ui.py",
                   "w683_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        """La tab non nomina altre tecnologie di
        rimozione del carbonio: il testo didattico
        parla solo del solido applicato al suolo."""
        src = _ui_src()
        assert "tab682" not in src
        assert "tab681" not in src
        assert "tab680" not in src
