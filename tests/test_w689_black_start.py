"""Test tab689 "⚡🏁 Black start: il riavvio della rete dopo il blackout paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
potenza black-start 50000 kW; prezzo disponibilita'
12 EUR/kW/anno; disponibilita' 0,98; avviamenti test
10/anno; prezzo avviamento 5000 EUR; eventi reali
1/anno; prezzo evento 50000 EUR; costo avviamento
8000 EUR; ore prova 120/anno; costo orario prova
300 EUR; OPEX fisso 150000 EUR/anno; CO2 per
avviamento 12 t; attrezzaggio black-start 800000
EUR; vita 15 anni; WACC 0,05 (5 %); tolleranza
0,10 (10 % del CAPEX).

- ricavi_disponibilita_eur_a = 588000.0
- ricavi_avviamenti_test_eur_a = 50000.0
- ricavi_eventi_eur_a = 50000.0
- ricavi_tot_eur_a = 688000.0
- n_avviamenti_totali = 11
- costi_avviamenti_eur_a = 88000.0
- costi_prove_eur_a = 36000.0
- opex_fisso_eur_a = 150000.0
- costi_tot_eur_a = 274000.0
- margine_eur_a = 414000.0
- co2_extra_t_a = 132.0
- capex_eur = 800000.0
- van = 3497178.4278067676
- tir = 51.64970324500702
- payback = 2
- verdetto = 'CONVIENTE'

Scomposizione: disponibilita' 50000 x 12 x 0,98 =
588000; test 10 x 5000 = 50000; eventi 1 x 50000 =
50000; ricavi 688000; avviamenti totali 11;
costi avviamenti 11 x 8000 = 88000; prove 120 x
300 = 36000; costi 88000 + 36000 + 150000 =
274000; margine 688000 - 274000 = 414000; CO2
11 x 12 = 132 t (extra emessa, non evitata).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w689_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w689_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w689_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w689_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w689_helpers.py: {missing}")
    return out


_F = _load("mh689_num", "mh689_nneg", "mh689_pos",
           "mh689_int_pos", "mh689_int_nneg",
           "mh689_tol", "mh689_frac",
           "mh689_n_tot", "mh689_ricavi_disp",
           "mh689_ricavi_test", "mh689_ricavi_eventi",
           "mh689_ricavi_tot", "mh689_costi_avv",
           "mh689_costi_prove", "mh689_costi_tot",
           "mh689_margine", "mh689_co2",
           "mh689_capex",
           "mh689_van", "mh689_tir",
           "mh689_payback", "mh689_verdetto",
           "_mh689_neutro", "mh689_calcola",
           "mh689_sensitivita", "mh689_csv",
           "mh689_demo", "demo_calcoli")

TITLE689 = ("⚡🏁 Black start: il riavvio della rete "
            "dopo il blackout paga?")

RD_DEMO = 588000.0
RT_DEMO = 50000.0
RE_DEMO = 50000.0
RTOT_DEMO = 688000.0
NTOT_DEMO = 11
CA_DEMO = 88000.0
CP_DEMO = 36000.0
OPEX_DEMO = 150000.0
CTOT_DEMO = 274000.0
MARG_DEMO = 414000.0
CO2_DEMO = 132.0
CAPEX_DEMO = 800000.0
VAN_DEMO = 3497178.4278067676
TIR_DEMO = 51.64970324500702
PAYBACK_DEMO = 2
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w689_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w689_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh689_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh689_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh689_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh689_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh689_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh689_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh689_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh689_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh689_int_pos"](15.0, "x") == 15

    def test_int_nneg_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh689_int_nneg"](2.5, "x")

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_int_nneg"](-1, "x")

    def test_int_nneg_accetta_zero(self):
        assert _F["mh689_int_nneg"](0, "x") == 0

    def test_int_nneg_accetta_float_intero(self):
        assert _F["mh689_int_nneg"](10.0, "x") == 10

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh689_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh689_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh689_tol"](0.0, "x") == 0.0
        assert _F["mh689_tol"](1.0, "x") == 1.0

    def test_frac_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh689_frac"](0.0, "x")

    def test_frac_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh689_frac"](1.01, "x")

    def test_frac_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh689_frac"](-0.01, "x")

    def test_frac_accetta_uno(self):
        assert _F["mh689_frac"](1.0, "x") == 1.0

    def test_frac_accetta_demo(self):
        assert _F["mh689_frac"](0.98, "x") == 0.98


class TestFisicaEconomia:
    def test_n_tot_demo(self):
        assert _F["mh689_n_tot"](10, 1) == NTOT_DEMO

    def test_n_tot_zero(self):
        assert _F["mh689_n_tot"](0, 0) == 0

    def test_n_tot_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh689_n_tot"](10.5, 1)

    def test_ricavi_disp_demo(self):
        assert _F["mh689_ricavi_disp"](
            50000.0, 12.0, 0.98) == pytest.approx(
            RD_DEMO, rel=REL)

    def test_ricavi_disp_formula(self):
        assert _F["mh689_ricavi_disp"](
            10000.0, 10.0, 1.0) == pytest.approx(
            100000.0, rel=1e-12)

    def test_ricavi_disp_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh689_ricavi_disp"](0.0, 12.0, 0.98)

    def test_ricavi_disp_rifiuta_disponibilita_zero(self):
        with pytest.raises(ValueError):
            _F["mh689_ricavi_disp"](50000.0, 12.0, 0.0)

    def test_ricavi_disp_rifiuta_disponibilita_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh689_ricavi_disp"](50000.0, 12.0, 1.01)

    def test_ricavi_disp_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_ricavi_disp"](50000.0, -1.0, 0.98)

    def test_ricavi_test_demo(self):
        assert _F["mh689_ricavi_test"](
            10, 5000.0) == pytest.approx(RT_DEMO, rel=REL)

    def test_ricavi_test_zero(self):
        assert _F["mh689_ricavi_test"](0, 5000.0) == 0.0

    def test_ricavi_eventi_demo(self):
        assert _F["mh689_ricavi_eventi"](
            1, 50000.0) == pytest.approx(RE_DEMO, rel=REL)

    def test_ricavi_eventi_zero(self):
        assert _F["mh689_ricavi_eventi"](0, 50000.0) == 0.0

    def test_ricavi_tot_demo(self):
        assert _F["mh689_ricavi_tot"](
            RD_DEMO, RT_DEMO, RE_DEMO) == pytest.approx(
            RTOT_DEMO, rel=REL)

    def test_ricavi_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh689_ricavi_tot"](-1.0, RT_DEMO, RE_DEMO)

    def test_costi_avv_demo(self):
        assert _F["mh689_costi_avv"](
            NTOT_DEMO, 8000.0) == pytest.approx(
            CA_DEMO, rel=REL)

    def test_costi_prove_demo(self):
        assert _F["mh689_costi_prove"](
            120.0, 300.0) == pytest.approx(CP_DEMO, rel=REL)

    def test_costi_prove_zero(self):
        assert _F["mh689_costi_prove"](0.0, 300.0) == 0.0
        assert _F["mh689_costi_prove"](120.0, 0.0) == 0.0

    def test_costi_tot_demo(self):
        assert _F["mh689_costi_tot"](
            CA_DEMO, CP_DEMO, OPEX_DEMO) == pytest.approx(
            CTOT_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh689_margine"](
            RTOT_DEMO, CTOT_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh689_margine"](100.0, 200.0) == -100.0

    def test_co2_demo(self):
        assert _F["mh689_co2"](
            NTOT_DEMO, 12.0) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_zero_se_nessun_avviamento(self):
        assert _F["mh689_co2"](0, 12.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_co2"](NTOT_DEMO, -0.01)

    def test_capex_demo(self):
        assert _F["mh689_capex"](800000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh689_capex"](0.0) == 0.0

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_capex"](-1.0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh689_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARG_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh689_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh689_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 15, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 15 == pytest.approx(
            5410000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh689_van"](MARG_DEMO, -1.0, 0.05, 15)

    def test_tir_demo(self):
        assert _F["mh689_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh689_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh689_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh689_tir"](0.0, MARG_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh689_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh689_tir"](CAPEX_DEMO, MARG_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_payback_demo(self):
        assert _F["mh689_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARG_DEMO * 1 < 0.0
        assert -CAPEX_DEMO + MARG_DEMO * 2 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh689_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh689_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh689_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        # -7000000 + 414000 x 15 = -790000 < 0 -> None
        assert _F["mh689_payback"](
            7000000.0, MARG_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh689_payback"](0.0, MARG_DEMO, 15) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh689_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh689_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh689_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh689_verdetto"](
            -80000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh689_verdetto"](
            -80001.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh689_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh689_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh689_verdetto"](
            0.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"
        assert _F["mh689_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh689_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh689_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh689_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh689_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 MARG_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh689_demo"]()
        d.update(kw)
        return _F["mh689_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["ricavi_disponibilita_eur_a"] == pytest.approx(
            RD_DEMO, rel=REL)
        assert c["ricavi_avviamenti_test_eur_a"] == pytest.approx(
            RT_DEMO, rel=REL)
        assert c["ricavi_eventi_eur_a"] == pytest.approx(
            RE_DEMO, rel=REL)
        assert c["ricavi_tot_eur_a"] == pytest.approx(
            RTOT_DEMO, rel=REL)
        assert c["n_avviamenti_totali"] == NTOT_DEMO
        assert c["costi_avviamenti_eur_a"] == pytest.approx(
            CA_DEMO, rel=REL)
        assert c["costi_prove_eur_a"] == pytest.approx(
            CP_DEMO, rel=REL)
        assert c["costi_tot_eur_a"] == pytest.approx(
            CTOT_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["co2_extra_t_a"] == pytest.approx(
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
            "co2_extra_t_a"] == _F["demo_calcoli"]()[
            "co2_extra_t_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh689_calcola(**mh689_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh689_demo"]()
        b = _F["mh689_calcola"](**d)
        coppie = [("ricavi_disponibilita_eur_a", RD_DEMO),
                  ("ricavi_avviamenti_test_eur_a", RT_DEMO),
                  ("ricavi_eventi_eur_a", RE_DEMO),
                  ("ricavi_tot_eur_a", RTOT_DEMO),
                  ("costi_avviamenti_eur_a", CA_DEMO),
                  ("costi_prove_eur_a", CP_DEMO),
                  ("costi_tot_eur_a", CTOT_DEMO),
                  ("margine_eur_a", MARG_DEMO),
                  ("co2_extra_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["n_avviamenti_totali"] == NTOT_DEMO
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh689_demo"]()
        assert d["potenza_blackstart_kw"] == 50000.0
        assert d["prezzo_disponibilita_eur_kw_a"] == 12.0
        assert d["disponibilita_frac"] == 0.98
        assert d["n_avviamenti_test_anno"] == 10
        assert d["prezzo_avviamento_eur"] == 5000.0
        assert d["n_eventi_reali_anno"] == 1
        assert d["prezzo_evento_eur"] == 50000.0
        assert d["costo_avviamento_eur"] == 8000.0
        assert d["ore_prova_anno"] == 120.0
        assert d["costo_orario_prova_eur"] == 300.0
        assert d["opex_fisso_eur_a"] == 150000.0
        assert d["co2_per_avviamento_t"] == 12.0
        assert d["costo_attrezzaggio_blackstart_eur"] == 800000.0
        assert d["vita_anni"] == 15
        assert d["wacc"] == 0.05
        assert d["tol_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("ricavi_disponibilita_eur_a",
                       "ricavi_avviamenti_test_eur_a",
                       "ricavi_eventi_eur_a",
                       "ricavi_tot_eur_a",
                       "costi_avviamenti_eur_a",
                       "costi_prove_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "co2_extra_t_a",
                       "capex_eur", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 2" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_blackstart_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_blackstart_kw=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_disponibilita_zero_neutro(self):
        n = self._bc(disponibilita_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_disponibilita_oltre_uno_neutro(self):
        n = self._bc(disponibilita_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_disponibilita_uno_calcolabile(self):
        n = self._bc(disponibilita_frac=1.0)
        assert n["valid"] is True
        assert n["ricavi_disponibilita_eur_a"] == pytest.approx(
            600000.0, rel=REL)

    def test_n_test_frazione_neutro(self):
        n = self._bc(n_avviamenti_test_anno=10.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_n_test_negativo_neutro(self):
        n = self._bc(n_avviamenti_test_anno=-1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_n_reali_frazione_neutro(self):
        n = self._bc(n_eventi_reali_anno=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nessun_avviamento_calcolabile(self):
        # n_test 0, n_reali 0: ricavi solo
        # disponibilita' 588000, costi 186000,
        # margine 402000 > 0
        n = self._bc(n_avviamenti_test_anno=0,
                     n_eventi_reali_anno=0)
        assert n["valid"] is True
        assert n["n_avviamenti_totali"] == 0
        assert n["co2_extra_t_a"] == 0.0
        assert n["margine_eur_a"] == pytest.approx(
            402000.0, rel=REL)

    def test_prezzi_costi_negativi_neutro(self):
        for k in ("prezzo_disponibilita_eur_kw_a",
                  "prezzo_avviamento_eur",
                  "prezzo_evento_eur",
                  "costo_avviamento_eur",
                  "ore_prova_anno",
                  "costo_orario_prova_eur",
                  "opex_fisso_eur_a",
                  "co2_per_avviamento_t",
                  "costo_attrezzaggio_blackstart_eur"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
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
        n = self._bc(prezzo_disponibilita_eur_kw_a=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_blackstart_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(potenza_blackstart_kw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX fisso enorme: 688000 - 974000 < 0
        n = self._bc(opex_fisso_eur_a=850000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(costo_attrezzaggio_blackstart_eur=0.0)
        assert n["capex_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 4300000: VAN = -4300000 + 4297178,43
        # circa -2822, entro il 10 % di 4300000
        n = self._bc(
            costo_attrezzaggio_blackstart_eur=4300000.0)
        assert n["capex_eur"] == pytest.approx(
            4300000.0, rel=REL)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 4300000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(
            costo_attrezzaggio_blackstart_eur=6000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh689_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh689_neutro"]()
        for chiave in ("valid",
                       "ricavi_disponibilita_eur_a",
                       "ricavi_avviamenti_test_eur_a",
                       "ricavi_eventi_eur_a",
                       "ricavi_tot_eur_a",
                       "n_avviamenti_totali",
                       "costi_avviamenti_eur_a",
                       "costi_prove_eur_a",
                       "opex_fisso_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "co2_extra_t_a",
                       "capex_eur", "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 15
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza black-start (kW)" in voci
        assert "Ricavi disponibilita' (EUR/anno)" in voci
        assert "Ricavi totali (EUR/anno)" in voci
        assert "Avviamenti totali (n/anno)" in voci
        assert "Costi totali (EUR/anno)" in voci
        assert "Margine (EUR/anno)" in voci
        assert "CO2 extra (t/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh689_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh689_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Avviamenti test 8",
                                   "Avviamenti test 10",
                                   "Avviamenti test 12"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh689_sensitivita"](self._ing())
        assert s.loc["x1.0", "Avviamenti test 10"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona_prezzo(self):
        # VAN cresce con il prezzo di disponibilita'
        s = _F["mh689_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Avviamenti test 10"]
        assert s.loc["x0.8", "Avviamenti test 10"] < centro
        assert s.loc["x1.2", "Avviamenti test 10"] > centro

    def test_sensitivita_decrescente_con_avviamenti_test(self):
        # Ogni avviamento test in piu' rende 5000 ma
        # costa 8000: margine -3000, VAN cala.
        s = _F["mh689_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Avviamenti test 8"] > \
                s.loc[riga, "Avviamenti test 10"] > \
                s.loc[riga, "Avviamenti test 12"]
        for colonna in ("Avviamenti test 8",
                        "Avviamenti test 10",
                        "Avviamenti test 12"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi variano davvero sulla
        # demo (prezzo senza tetto, avviamenti test
        # 8/10/12): il margine resta positivo su
        # tutta la griglia, nessuna cella puo'
        # essere 0,0 per regime degenere
        s = _F["mh689_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh689_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh689_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 30

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh689_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_extra_t_a" in txt
        assert "ricavi_tot_eur_a" in txt
        assert "margine_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "costi_tot_eur_a" in txt
        assert "prezzo_disponibilita_eur_kw_a" in txt
        assert "n_avviamenti_test_anno" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh689_csv"](bc, self._ing())
        assert f"ricavi_tot_eur_a;{RTOT_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"capex_eur;{CAPEX_DEMO}" in txt
        assert "co2_extra_t_a;132.0" in txt
        assert f"ricavi_disponibilita_eur_a;{RD_DEMO}" in txt
        assert f"costi_tot_eur_a;{CTOT_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def689["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def689\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh689_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W689 (24/10/2026) - tab689' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh689_num", "mh689_nneg", "mh689_pos",
                     "mh689_int_pos", "mh689_int_nneg",
                     "mh689_tol", "mh689_frac",
                     "mh689_n_tot", "mh689_ricavi_disp",
                     "mh689_ricavi_test",
                     "mh689_ricavi_eventi",
                     "mh689_ricavi_tot", "mh689_costi_avv",
                     "mh689_costi_prove", "mh689_costi_tot",
                     "mh689_margine", "mh689_co2",
                     "mh689_capex",
                     "mh689_van", "mh689_tir",
                     "mh689_payback", "mh689_verdetto",
                     "_mh689_neutro", "mh689_calcola",
                     "mh689_sensitivita", "mh689_csv",
                     "mh689_demo", "demo_calcoli"):
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
        # l'apply (come w688_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w689_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE689) == 1

    def test_blocco_with_tab689(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab689:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE689

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st689_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 21, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st688_") for k in keys)
        assert not any(k.startswith("st687_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg689" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg689") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg689")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi totali (€/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 extra (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd689" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_blackstart_presente(self):
        src = _ui_src()
        assert "riavvia la rete da zero" in src
        assert "disponibilità anche se non viene mai chiamato" in src
        assert "riserva di frequenza" in src
        assert "capacità" in src
        assert "carburante" in src
        assert "CO2 extra" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi disponibilità" in src
        assert "Margine" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh689_csv" in src
        assert "black_start_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh689_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo disponibilità" in src
        assert "Avviamenti test" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st689_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W689 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab689:")
        assert "mh689_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab689" in (_new_dir() / "w689_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w689_helpers.py", "w689_ui.py",
                   "w689_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab688" not in src
        assert "tab687" not in src
        assert "tab686" not in src

    def test_topic_blackstart_non_flusso(self):
        # Topic corretto: il titolo e' black start
        assert "Black start" in TITLE689
        assert "flusso" not in TITLE689.lower()
