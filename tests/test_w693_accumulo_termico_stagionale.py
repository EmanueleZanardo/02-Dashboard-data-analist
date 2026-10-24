"""Test tab693 "☀️🗄️ Accumulo termico stagionale: il calore dell'estate per l'inverno paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
calore caricato 1000 MWh/anno; perdite
stagionali 0,30; domanda invernale 800
MWh/anno; efficienza caldaia 0,90; prezzo
gas 80 EUR/MWh; costo carica 5 EUR/MWh;
OPEX fisso 10000 EUR/anno; CAPEX 400000
EUR; vita 25 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del CAPEX); fattore
gas 0,20 t/MWh.

- q_erogata_mwh_a = 700.0
- q_coperta_mwh_a = 700.0
- c_base_eur_a = 62222.22222222222
- costi_carica_eur_a = 5000.0
- opex_fisso_eur_a = 10000.0
- costi_annui_eur_a = 15000.0
- risparmio_eur_a = 47222.22222222222
- co2_evitata_t_a = 155.55555555555554
- capex_eur = 400000.0
- van = 265547.3822854471
- tir = 10.92095698581661
- payback = 9
- verdetto = 'CONVIENTE'

Scomposizione: erogato 1000 x (1 - 0,30) = 700;
coperto min(700, 800) = 700; costo base
700 / 0,90 x 80 = 62222,22; costi carica
1000 x 5 = 5000; costi annui 5000 + 10000 =
15000; risparmio 62222,22 - 15000 = 47222,22;
CO2 700 / 0,90 x 0,20 = 155,56 t.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w693_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w693_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w693_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w693_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w693_helpers.py: {missing}")
    return out


_F = _load("mh693_num", "mh693_nneg", "mh693_pos",
           "mh693_int_pos", "mh693_frac", "mh693_frac01",
           "mh693_tol", "mh693_q_erogata",
           "mh693_q_coperta", "mh693_c_base",
           "mh693_costi_carica", "mh693_costi_annui",
           "mh693_risparmio", "mh693_co2", "mh693_capex",
           "mh693_van", "mh693_tir",
           "mh693_payback", "mh693_verdetto",
           "_mh693_neutro", "mh693_calcola",
           "mh693_sensitivita", "mh693_csv",
           "mh693_demo", "demo_calcoli")

TITLE693 = ("☀️🗄️ Accumulo termico stagionale: "
            "il calore dell'estate per l'inverno paga?")

QEROG_DEMO = 700.0
QCOP_DEMO = 700.0
CBASE_DEMO = 62222.22222222222
CCAR_DEMO = 5000.0
OPEX_DEMO = 10000.0
CANN_DEMO = 15000.0
RISP_DEMO = 47222.22222222222
CO2_DEMO = 155.55555555555554
CAPEX_DEMO = 400000.0
VAN_DEMO = 265547.3822854471
TIR_DEMO = 10.92095698581661
PAYBACK_DEMO = 9
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w693_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w693_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh693_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh693_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh693_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh693_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh693_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh693_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh693_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh693_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh693_int_pos"](25.0, "x") == 25

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh693_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh693_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh693_tol"](0.0, "x") == 0.0
        assert _F["mh693_tol"](1.0, "x") == 1.0

    def test_frac_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh693_frac"](0.0, "x")

    def test_frac_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh693_frac"](1.01, "x")

    def test_frac_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh693_frac"](-0.01, "x")

    def test_frac_accetta_uno(self):
        assert _F["mh693_frac"](1.0, "x") == 1.0

    def test_frac01_accetta_zero_e_uno(self):
        assert _F["mh693_frac01"](0.0, "x") == 0.0
        assert _F["mh693_frac01"](1.0, "x") == 1.0

    def test_frac01_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh693_frac01"](1.01, "x")

    def test_frac01_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh693_frac01"](-0.01, "x")


class TestFisicaEconomia:
    def test_q_erogata_demo(self):
        assert _F["mh693_q_erogata"](
            1000.0, 0.30) == pytest.approx(QEROG_DEMO, rel=REL)

    def test_q_erogata_perdite_zero(self):
        assert _F["mh693_q_erogata"](1000.0, 0.0) == 1000.0

    def test_q_erogata_perdite_uno(self):
        assert _F["mh693_q_erogata"](1000.0, 1.0) == 0.0

    def test_q_erogata_rifiuta_caricato_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_q_erogata"](-1.0, 0.30)

    def test_q_erogata_rifiuta_perdite_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh693_q_erogata"](1000.0, 1.01)

    def test_q_coperta_demo(self):
        assert _F["mh693_q_coperta"](
            QEROG_DEMO, 800.0) == pytest.approx(
            QCOP_DEMO, rel=REL)

    def test_q_coperta_limitata_da_domanda(self):
        assert _F["mh693_q_coperta"](700.0, 500.0) == 500.0

    def test_q_coperta_limitata_da_erogato(self):
        assert _F["mh693_q_coperta"](400.0, 800.0) == 400.0

    def test_q_coperta_domanda_zero(self):
        assert _F["mh693_q_coperta"](700.0, 0.0) == 0.0

    def test_q_coperta_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh693_q_coperta"](-1.0, 800.0)
        with pytest.raises(ValueError):
            _F["mh693_q_coperta"](700.0, -1.0)

    def test_c_base_demo(self):
        assert _F["mh693_c_base"](
            QCOP_DEMO, 0.90, 80.0) == pytest.approx(
            CBASE_DEMO, rel=REL)

    def test_c_base_formula(self):
        assert _F["mh693_c_base"](
            500.0, 0.90, 80.0) == pytest.approx(
            44444.44444444444, rel=1e-12)

    def test_c_base_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh693_c_base"](QCOP_DEMO, 0.0, 80.0)

    def test_c_base_rifiuta_eta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh693_c_base"](QCOP_DEMO, 1.01, 80.0)

    def test_c_base_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_c_base"](QCOP_DEMO, 0.90, -1.0)

    def test_costi_carica_demo(self):
        assert _F["mh693_costi_carica"](
            1000.0, 5.0) == pytest.approx(CCAR_DEMO, rel=REL)

    def test_costi_carica_zero(self):
        assert _F["mh693_costi_carica"](1000.0, 0.0) == 0.0

    def test_costi_annui_demo(self):
        assert _F["mh693_costi_annui"](
            CCAR_DEMO, OPEX_DEMO) == pytest.approx(
            CANN_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh693_risparmio"](
            CBASE_DEMO, CANN_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh693_risparmio"](100.0, 200.0) == -100.0

    def test_co2_demo(self):
        assert _F["mh693_co2"](
            QCOP_DEMO, 0.90, 0.20) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_zero_se_nessun_coperto(self):
        assert _F["mh693_co2"](0.0, 0.90, 0.20) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_co2"](QCOP_DEMO, 0.90, -0.01)

    def test_capex_demo(self):
        assert _F["mh693_capex"](400000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh693_capex"](0.0) == 0.0

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_capex"](-1.0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh693_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-25)) / 0.05
        assert _F["mh693_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh693_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            25) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 25, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + RISP_DEMO * 25 == pytest.approx(
            780555.5555555555, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 25)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh693_van"](RISP_DEMO, -1.0, 0.05, 25)

    def test_tir_demo(self):
        assert _F["mh693_tir"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh693_tir"](CAPEX_DEMO, 0.0, 25) is None
        assert _F["mh693_tir"](CAPEX_DEMO, -100.0, 25) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh693_tir"](0.0, RISP_DEMO, 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh693_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh693_tir"](CAPEX_DEMO, RISP_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 26))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh693_payback"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 8 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 9 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh693_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh693_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh693_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh693_payback"](
            5000000.0, RISP_DEMO, 25) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh693_payback"](0.0, RISP_DEMO, 25) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh693_payback"](CAPEX_DEMO, 0.0, 25) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh693_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh693_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh693_verdetto"](
            -40000.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh693_verdetto"](
            -40001.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh693_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh693_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh693_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"
        assert _F["mh693_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh693_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh693_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh693_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 RISP_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh693_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh693_demo"]()
        d.update(kw)
        return _F["mh693_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["q_erogata_mwh_a"] == pytest.approx(
            QEROG_DEMO, rel=REL)
        assert c["q_coperta_mwh_a"] == pytest.approx(
            QCOP_DEMO, rel=REL)
        assert c["c_base_eur_a"] == pytest.approx(
            CBASE_DEMO, rel=REL)
        assert c["costi_carica_eur_a"] == pytest.approx(
            CCAR_DEMO, rel=REL)
        assert c["costi_annui_eur_a"] == pytest.approx(
            CANN_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "co2_evitata_t_a"] == _F["demo_calcoli"]()[
            "co2_evitata_t_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh693_calcola(**mh693_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh693_demo"]()
        b = _F["mh693_calcola"](**d)
        coppie = [("q_erogata_mwh_a", QEROG_DEMO),
                  ("q_coperta_mwh_a", QCOP_DEMO),
                  ("c_base_eur_a", CBASE_DEMO),
                  ("costi_carica_eur_a", CCAR_DEMO),
                  ("costi_annui_eur_a", CANN_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh693_demo"]()
        assert d["q_caricata_mwh_a"] == 1000.0
        assert d["perdite_stagionali_frac"] == 0.30
        assert d["domanda_invernale_mwh_a"] == 800.0
        assert d["eta_caldaia"] == 0.90
        assert d["prezzo_gas_eur_mwh"] == 80.0
        assert d["costo_carica_eur_mwh"] == 5.0
        assert d["opex_fisso_eur_a"] == 10000.0
        assert d["capex_eur"] == 400000.0
        assert d["vita_anni"] == 25
        assert d["wacc_frac"] == 0.05
        assert d["toll_frac"] == 0.10
        assert d["fattore_gas_t_mwh"] == 0.20

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_erogata_mwh_a",
                       "q_coperta_mwh_a",
                       "c_base_eur_a",
                       "costi_carica_eur_a",
                       "costi_annui_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 9" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_perdite_zero_calcolabile(self):
        # Perdite 0: erogato 1000, coperto 800,
        # base 71111,11, risparmio 56111,11
        n = self._bc(perdite_stagionali_frac=0.0)
        assert n["valid"] is True
        assert n["q_erogata_mwh_a"] == pytest.approx(
            1000.0, rel=REL)
        assert n["q_coperta_mwh_a"] == pytest.approx(
            800.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            56111.11111111111, rel=REL)

    def test_perdite_uno_neutro(self):
        n = self._bc(perdite_stagionali_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_perdite_oltre_uno_neutro(self):
        n = self._bc(perdite_stagionali_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_invernale_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_minore_di_erogata(self):
        # Domanda 500: coperto 500, base 44444,44,
        # risparmio 29444,44
        n = self._bc(domanda_invernale_mwh_a=500.0)
        assert n["valid"] is True
        assert n["q_coperta_mwh_a"] == pytest.approx(
            500.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            29444.44444444444, rel=REL)

    def test_caricata_zero_neutro(self):
        n = self._bc(q_caricata_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_caricata_negativa_neutro(self):
        n = self._bc(q_caricata_mwh_a=-10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_zero_neutro(self):
        n = self._bc(eta_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_oltre_uno_neutro(self):
        n = self._bc(eta_caldaia=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_uno_calcolabile(self):
        # Eta 1,0: base 700 x 80 = 56000,
        # risparmio 41000, CO2 140,0
        n = self._bc(eta_caldaia=1.0)
        assert n["valid"] is True
        assert n["c_base_eur_a"] == pytest.approx(
            56000.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            41000.0, rel=REL)
        assert n["co2_evitata_t_a"] == pytest.approx(
            140.0, rel=REL)

    def test_prezzo_gas_zero_neutro(self):
        # Base 0, risparmio -15000
        n = self._bc(prezzo_gas_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costi_negativi_neutro(self):
        for k in ("costo_carica_eur_mwh",
                  "opex_fisso_eur_a",
                  "capex_eur",
                  "fattore_gas_t_mwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=24.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -400000 + 47222,22 / 1,05 < 0,
        # oltre tolleranza; payback mai
        n = self._bc(vita_anni=1)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(toll_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_uno_neutro(self):
        n = self._bc(toll_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_gas_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(q_caricata_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(q_caricata_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risparmio_negativo_neutro(self):
        # OPEX fisso enorme: 62222,22 - 105000 < 0
        n = self._bc(opex_fisso_eur_a=100000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 25, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur=0.0)
        assert n["capex_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 700000: VAN circa -34453, entro il
        # 10 % di 700000
        n = self._bc(capex_eur=700000.0)
        assert n["capex_eur"] == pytest.approx(
            700000.0, rel=REL)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 700000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(capex_eur=1000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh693_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh693_neutro"]()
        for chiave in ("valid",
                       "q_erogata_mwh_a",
                       "q_coperta_mwh_a",
                       "c_base_eur_a",
                       "costi_carica_eur_a",
                       "opex_fisso_eur_a",
                       "costi_annui_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur", "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 16
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Calore caricato (MWh/anno)" in voci
        assert "Calore erogato (MWh/anno)" in voci
        assert "Calore coperto (MWh/anno)" in voci
        assert "Costo base caldaia (EUR/anno)" in voci
        assert "Costi annui totali (EUR/anno)" in voci
        assert "Risparmio (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh693_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh693_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.8", "x1.0", "x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh693_sensitivita"](self._ing())
        assert s.loc["x1.0", "x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_decrescente_con_perdite(self):
        # VAN cala all'aumentare delle perdite
        s = _F["mh693_sensitivita"](self._ing())
        for colonna in ("x0.8", "x1.0", "x1.2"):
            assert s.loc["x0.8", colonna] > \
                s.loc["x1.0", colonna] > \
                s.loc["x1.2", colonna]

    def test_sensitivita_crescente_con_prezzo_gas(self):
        # VAN cresce con il prezzo gas
        s = _F["mh693_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "x0.8"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.2"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il risparmio resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh693_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh693_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh693_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 26

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh693_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_a" in txt
        assert "costi_annui_eur_a" in txt
        assert "risparmio_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "c_base_eur_a" in txt
        assert "prezzo_gas_eur_mwh" in txt
        assert "q_caricata_mwh_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh693_csv"](bc, self._ing())
        assert f"c_base_eur_a;{CBASE_DEMO}" in txt
        assert f"risparmio_eur_a;{RISP_DEMO}" in txt
        assert f"capex_eur;{CAPEX_DEMO}" in txt
        assert f"costi_annui_eur_a;{CANN_DEMO}" in txt
        assert f"q_coperta_mwh_a;{QCOP_DEMO}" in txt
        assert "costi_carica_eur_a;5000.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def693["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def693\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 12, ui_keys
        demo_keys = set(_F["mh693_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W693 (25/10/2026) - tab693' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh693_num", "mh693_nneg", "mh693_pos",
                     "mh693_int_pos", "mh693_frac",
                     "mh693_frac01", "mh693_tol",
                     "mh693_q_erogata",
                     "mh693_q_coperta", "mh693_c_base",
                     "mh693_costi_carica",
                     "mh693_costi_annui",
                     "mh693_risparmio", "mh693_co2",
                     "mh693_capex",
                     "mh693_van", "mh693_tir",
                     "mh693_payback", "mh693_verdetto",
                     "_mh693_neutro", "mh693_calcola",
                     "mh693_sensitivita", "mh693_csv",
                     "mh693_demo", "demo_calcoli"):
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
        # l'apply (come w692_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w693_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE693) == 1

    def test_blocco_with_tab693(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab693:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE693

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st693_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 17, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st692_") for k in keys)
        assert not any(k.startswith("st691_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg693" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg693") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg693")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Calore coperto (MWh/anno)" in src
        assert "Risparmio (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd693" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_stagionale_presente(self):
        src = _ui_src()
        assert "stagionale" in src
        assert "pit" in src
        assert "BTES" in src
        assert "ATES" in src
        assert "giornaliero" in src
        assert "solare termico" in src
        assert "perdite" in src
        assert "domanda" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo base caldaia" in src
        assert "Risparmio" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh693_csv" in src
        assert "accumulo_termico_stagionale_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh693_sensitivita" in src
        assert "Heatmap" in src
        assert "Perdite stagionali" in src
        assert "Prezzo gas" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st693_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W693 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab693:")
        assert "mh693_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab693" in (_new_dir() / "w693_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w693_helpers.py", "w693_ui.py",
                   "w693_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab692" not in src
        assert "tab691" not in src
        assert "tab690" not in src

    def test_topic_stagionale_non_giornaliero(self):
        # Topic corretto: il titolo e' stagionale
        assert "stagionale" in TITLE693.lower()
        assert "giornaliero" not in TITLE693.lower()
