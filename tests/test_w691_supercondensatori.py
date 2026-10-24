"""Test tab691 "⚡ Supercondensatori: potenza istantanea per FFR e peak shaving paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
potenza supercondensatori 2 MW; energia
100 kWh; prezzo FFR 60000 EUR/MW/anno;
disponibilita' 0,98; prezzo picco 120
EUR/kW/anno; cicli 20/giorno; costo ciclo
5 EUR; OPEX fisso 40000 EUR/anno; CAPEX
800000 EUR; vita 15 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del CAPEX); fattore
rete 0,35 t/MWh.

- potenza_kw = 2000.0
- ricavi_ffr_eur_a = 117600.0
- risparmio_picco_eur_a = 240000.0
- ricavi_tot_eur_a = 357600.0
- cicli_a = 7300
- costi_cicli_eur_a = 36500.0
- opex_fisso_eur_a = 40000.0
- costi_tot_eur_a = 76500.0
- margine_eur_a = 281100.0
- energia_annua_mwh_a = 730.0
- co2_evitata_t_a = 255.49999999999997
- capex_eur = 800000.0
- van = 2117721.874532566
- tir = 34.73616394069303
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: potenza 2 x 1000 = 2000 kW;
FFR 2 x 60000 x 0,98 = 117600; picco
2000 x 120 = 240000; ricavi 357600; cicli
20 x 365 = 7300; costi cicli 7300 x 5 =
36500; costi 36500 + 40000 = 76500;
margine 357600 - 76500 = 281100; energia
7300 x 100 / 1000 = 730 MWh; CO2 730 x
0,35 = 255,5 t.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w691_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w691_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w691_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w691_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w691_helpers.py: {missing}")
    return out


_F = _load("mh691_num", "mh691_nneg", "mh691_pos",
           "mh691_int_pos", "mh691_int_nneg",
           "mh691_tol", "mh691_frac",
           "mh691_potenza_kw", "mh691_ricavi_ffr",
           "mh691_risparmio_picco", "mh691_ricavi_tot",
           "mh691_cicli_a", "mh691_costi_cicli",
           "mh691_costi_tot", "mh691_margine",
           "mh691_energia_annua", "mh691_co2",
           "mh691_capex",
           "mh691_van", "mh691_tir",
           "mh691_payback", "mh691_verdetto",
           "_mh691_neutro", "mh691_calcola",
           "mh691_sensitivita", "mh691_csv",
           "mh691_demo", "demo_calcoli")

TITLE691 = ("⚡ Supercondensatori: potenza istantanea "
            "per FFR e peak shaving paga?")

PKW_DEMO = 2000.0
RFFR_DEMO = 117600.0
RPICCO_DEMO = 240000.0
RTOT_DEMO = 357600.0
CICLI_DEMO = 7300
CCICLI_DEMO = 36500.0
OPEX_DEMO = 40000.0
CTOT_DEMO = 76500.0
MARG_DEMO = 281100.0
EA_DEMO = 730.0
CO2_DEMO = 255.49999999999997
CAPEX_DEMO = 800000.0
VAN_DEMO = 2117721.874532566
TIR_DEMO = 34.73616394069303
PAYBACK_DEMO = 3
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w691_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w691_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh691_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh691_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh691_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh691_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh691_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh691_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh691_int_pos"](15.0, "x") == 15

    def test_int_nneg_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh691_int_nneg"](2.5, "x")

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_int_nneg"](-1, "x")

    def test_int_nneg_accetta_zero(self):
        assert _F["mh691_int_nneg"](0, "x") == 0

    def test_int_nneg_accetta_float_intero(self):
        assert _F["mh691_int_nneg"](20.0, "x") == 20

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh691_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh691_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh691_tol"](0.0, "x") == 0.0
        assert _F["mh691_tol"](1.0, "x") == 1.0

    def test_frac_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_frac"](0.0, "x")

    def test_frac_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh691_frac"](1.01, "x")

    def test_frac_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh691_frac"](-0.01, "x")

    def test_frac_accetta_uno(self):
        assert _F["mh691_frac"](1.0, "x") == 1.0

    def test_frac_accetta_demo(self):
        assert _F["mh691_frac"](0.98, "x") == 0.98


class TestFisicaEconomia:
    def test_potenza_kw_demo(self):
        assert _F["mh691_potenza_kw"](2.0) == pytest.approx(
            PKW_DEMO, rel=REL)

    def test_potenza_kw_formula(self):
        assert _F["mh691_potenza_kw"](1.5) == pytest.approx(
            1500.0, rel=1e-12)

    def test_potenza_kw_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_potenza_kw"](0.0)

    def test_ricavi_ffr_demo(self):
        assert _F["mh691_ricavi_ffr"](
            2.0, 60000.0, 0.98) == pytest.approx(
            RFFR_DEMO, rel=REL)

    def test_ricavi_ffr_formula(self):
        assert _F["mh691_ricavi_ffr"](
            10.0, 40000.0, 1.0) == pytest.approx(
            400000.0, rel=1e-12)

    def test_ricavi_ffr_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_ricavi_ffr"](0.0, 60000.0, 0.98)

    def test_ricavi_ffr_rifiuta_prezzo_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_ricavi_ffr"](2.0, 0.0, 0.98)

    def test_ricavi_ffr_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_ricavi_ffr"](2.0, -1.0, 0.98)

    def test_ricavi_ffr_rifiuta_disponibilita_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_ricavi_ffr"](2.0, 60000.0, 0.0)

    def test_ricavi_ffr_rifiuta_disponibilita_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh691_ricavi_ffr"](2.0, 60000.0, 1.01)

    def test_risparmio_picco_demo(self):
        assert _F["mh691_risparmio_picco"](
            PKW_DEMO, 120.0) == pytest.approx(
            RPICCO_DEMO, rel=REL)

    def test_risparmio_picco_zero(self):
        assert _F["mh691_risparmio_picco"](PKW_DEMO, 0.0) == 0.0

    def test_ricavi_tot_demo(self):
        assert _F["mh691_ricavi_tot"](
            RFFR_DEMO, RPICCO_DEMO) == pytest.approx(
            RTOT_DEMO, rel=REL)

    def test_ricavi_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh691_ricavi_tot"](-1.0, RPICCO_DEMO)

    def test_cicli_a_demo(self):
        assert _F["mh691_cicli_a"](20) == CICLI_DEMO

    def test_cicli_a_zero(self):
        assert _F["mh691_cicli_a"](0) == 0

    def test_cicli_a_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh691_cicli_a"](20.5)

    def test_costi_cicli_demo(self):
        assert _F["mh691_costi_cicli"](
            CICLI_DEMO, 5.0) == pytest.approx(
            CCICLI_DEMO, rel=REL)

    def test_costi_cicli_zero(self):
        assert _F["mh691_costi_cicli"](0, 5.0) == 0.0
        assert _F["mh691_costi_cicli"](CICLI_DEMO, 0.0) == 0.0

    def test_costi_tot_demo(self):
        assert _F["mh691_costi_tot"](
            CCICLI_DEMO, OPEX_DEMO) == pytest.approx(
            CTOT_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh691_margine"](
            RTOT_DEMO, CTOT_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh691_margine"](100.0, 200.0) == -100.0

    def test_energia_annua_demo(self):
        assert _F["mh691_energia_annua"](
            CICLI_DEMO, 100.0) == pytest.approx(
            EA_DEMO, rel=REL)

    def test_energia_annua_zero_senza_cicli(self):
        assert _F["mh691_energia_annua"](0, 100.0) == 0.0

    def test_energia_annua_rifiuta_energia_zero(self):
        with pytest.raises(ValueError):
            _F["mh691_energia_annua"](CICLI_DEMO, 0.0)

    def test_co2_demo(self):
        assert _F["mh691_co2"](
            EA_DEMO, 0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_zero_se_nessuna_energia(self):
        assert _F["mh691_co2"](0.0, 0.35) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_co2"](EA_DEMO, -0.01)

    def test_capex_demo(self):
        assert _F["mh691_capex"](800000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh691_capex"](0.0) == 0.0

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_capex"](-1.0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh691_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARG_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh691_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh691_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 15, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 15 == pytest.approx(
            3416500.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh691_van"](MARG_DEMO, -1.0, 0.05, 15)

    def test_tir_demo(self):
        assert _F["mh691_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh691_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh691_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh691_tir"](0.0, MARG_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh691_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh691_tir"](CAPEX_DEMO, MARG_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh691_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARG_DEMO * 2 < 0.0
        assert -CAPEX_DEMO + MARG_DEMO * 3 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh691_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh691_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh691_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        # -5000000 + 281100 x 15 = -783500 < 0 -> None
        assert _F["mh691_payback"](
            5000000.0, MARG_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh691_payback"](0.0, MARG_DEMO, 15) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh691_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh691_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh691_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh691_verdetto"](
            -80000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh691_verdetto"](
            -80001.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh691_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh691_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh691_verdetto"](
            0.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"
        assert _F["mh691_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh691_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh691_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh691_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh691_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 MARG_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh691_demo"]()
        d.update(kw)
        return _F["mh691_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["potenza_kw"] == pytest.approx(
            PKW_DEMO, rel=REL)
        assert c["ricavi_ffr_eur_a"] == pytest.approx(
            RFFR_DEMO, rel=REL)
        assert c["risparmio_picco_eur_a"] == pytest.approx(
            RPICCO_DEMO, rel=REL)
        assert c["ricavi_tot_eur_a"] == pytest.approx(
            RTOT_DEMO, rel=REL)
        assert c["cicli_a"] == CICLI_DEMO
        assert c["costi_cicli_eur_a"] == pytest.approx(
            CCICLI_DEMO, rel=REL)
        assert c["costi_tot_eur_a"] == pytest.approx(
            CTOT_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["energia_annua_mwh_a"] == pytest.approx(
            EA_DEMO, rel=REL)
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
        """mh691_calcola(**mh691_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh691_demo"]()
        b = _F["mh691_calcola"](**d)
        coppie = [("potenza_kw", PKW_DEMO),
                  ("ricavi_ffr_eur_a", RFFR_DEMO),
                  ("risparmio_picco_eur_a", RPICCO_DEMO),
                  ("ricavi_tot_eur_a", RTOT_DEMO),
                  ("costi_cicli_eur_a", CCICLI_DEMO),
                  ("costi_tot_eur_a", CTOT_DEMO),
                  ("margine_eur_a", MARG_DEMO),
                  ("energia_annua_mwh_a", EA_DEMO),
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
        d = _F["mh691_demo"]()
        assert d["potenza_mw"] == 2.0
        assert d["energia_kwh"] == 100.0
        assert d["prezzo_ffr_eur_mw_a"] == 60000.0
        assert d["disponibilita_frac"] == 0.98
        assert d["prezzo_picco_eur_kw_a"] == 120.0
        assert d["cicli_giorno"] == 20
        assert d["costo_ciclo_eur"] == 5.0
        assert d["opex_fisso_eur_a"] == 40000.0
        assert d["capex_eur"] == 800000.0
        assert d["vita_a"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["toll_frac"] == 0.10
        assert d["fattore_rete_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_kw",
                       "ricavi_ffr_eur_a",
                       "risparmio_picco_eur_a",
                       "ricavi_tot_eur_a",
                       "costi_cicli_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "energia_annua_mwh_a",
                       "co2_evitata_t_a",
                       "capex_eur", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_mw=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_energia_zero_neutro(self):
        n = self._bc(energia_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_ffr_zero_neutro(self):
        n = self._bc(prezzo_ffr_eur_mw_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_ffr_negativo_neutro(self):
        n = self._bc(prezzo_ffr_eur_mw_a=-1.0)
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
        assert n["ricavi_ffr_eur_a"] == pytest.approx(
            120000.0, rel=REL)

    def test_cicli_frazione_neutro(self):
        n = self._bc(cicli_giorno=20.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_negativo_neutro(self):
        n = self._bc(cicli_giorno=-1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_zero_cicli_calcolabile(self):
        # 0 cicli: costi cicli 0, costi 40000,
        # margine 357600 - 40000 = 317600 > 0
        n = self._bc(cicli_giorno=0)
        assert n["valid"] is True
        assert n["cicli_a"] == 0
        assert n["energia_annua_mwh_a"] == 0.0
        assert n["co2_evitata_t_a"] == 0.0
        assert n["margine_eur_a"] == pytest.approx(
            317600.0, rel=REL)

    def test_prezzi_costi_negativi_neutro(self):
        for k in ("prezzo_picco_eur_kw_a",
                  "costo_ciclo_eur",
                  "opex_fisso_eur_a",
                  "capex_eur",
                  "fattore_rete_t_mwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_a=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_a=14.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

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
        n = self._bc(prezzo_ffr_eur_mw_a=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_mw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(potenza_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX fisso enorme: 357600 - 436500 < 0
        n = self._bc(opex_fisso_eur_a=400000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur=0.0)
        assert n["capex_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 2920000: VAN circa -2282, entro il
        # 10 % di 2920000
        n = self._bc(capex_eur=2920000.0)
        assert n["capex_eur"] == pytest.approx(
            2920000.0, rel=REL)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 2920000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(capex_eur=4000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh691_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh691_neutro"]()
        for chiave in ("valid",
                       "potenza_kw",
                       "ricavi_ffr_eur_a",
                       "risparmio_picco_eur_a",
                       "ricavi_tot_eur_a",
                       "cicli_a",
                       "costi_cicli_eur_a",
                       "opex_fisso_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "energia_annua_mwh_a",
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
        assert "Potenza supercondensatori (MW)" in voci
        assert "Ricavi FFR (EUR/anno)" in voci
        assert "Risparmio peak shaving (EUR/anno)" in voci
        assert "Ricavi totali (EUR/anno)" in voci
        assert "Cicli (n/anno)" in voci
        assert "Costi totali (EUR/anno)" in voci
        assert "Margine (EUR/anno)" in voci
        assert "Energia annua (MWh/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh691_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh691_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Prezzo picco 96",
                                   "Prezzo picco 120",
                                   "Prezzo picco 144"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh691_sensitivita"](self._ing())
        assert s.loc["x1.0", "Prezzo picco 120"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona_prezzo_ffr(self):
        # VAN cresce con il prezzo FFR
        s = _F["mh691_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Prezzo picco 120"]
        assert s.loc["x0.8", "Prezzo picco 120"] < centro
        assert s.loc["x1.2", "Prezzo picco 120"] > centro

    def test_sensitivita_crescente_con_prezzo_picco(self):
        # Ogni euro/kW di picco in piu' rende
        # 2000 EUR/anno: VAN cresce.
        s = _F["mh691_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Prezzo picco 96"] < \
                s.loc[riga, "Prezzo picco 120"] < \
                s.loc[riga, "Prezzo picco 144"]
        for colonna in ("Prezzo picco 96",
                        "Prezzo picco 120",
                        "Prezzo picco 144"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi variano davvero sulla
        # demo (prezzo FFR e prezzo picco senza
        # tetto): il margine resta positivo su
        # tutta la griglia, nessuna cella puo'
        # essere 0,0 per regime degenere
        s = _F["mh691_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh691_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh691_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh691_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_a" in txt
        assert "ricavi_tot_eur_a" in txt
        assert "margine_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "costi_tot_eur_a" in txt
        assert "prezzo_ffr_eur_mw_a" in txt
        assert "cicli_giorno" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh691_csv"](bc, self._ing())
        assert f"ricavi_tot_eur_a;{RTOT_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"capex_eur;{CAPEX_DEMO}" in txt
        assert f"ricavi_ffr_eur_a;{RFFR_DEMO}" in txt
        assert f"costi_tot_eur_a;{CTOT_DEMO}" in txt
        assert "risparmio_picco_eur_a;240000.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def691["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def691\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 13, ui_keys
        demo_keys = set(_F["mh691_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W691 (24/10/2026) - tab691' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh691_num", "mh691_nneg", "mh691_pos",
                     "mh691_int_pos", "mh691_int_nneg",
                     "mh691_tol", "mh691_frac",
                     "mh691_potenza_kw", "mh691_ricavi_ffr",
                     "mh691_risparmio_picco",
                     "mh691_ricavi_tot",
                     "mh691_cicli_a", "mh691_costi_cicli",
                     "mh691_costi_tot", "mh691_margine",
                     "mh691_energia_annua", "mh691_co2",
                     "mh691_capex",
                     "mh691_van", "mh691_tir",
                     "mh691_payback", "mh691_verdetto",
                     "_mh691_neutro", "mh691_calcola",
                     "mh691_sensitivita", "mh691_csv",
                     "mh691_demo", "demo_calcoli"):
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
        # l'apply (come w690_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w691_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE691) == 1

    def test_blocco_with_tab691(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab691:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE691

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st691_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 18, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st690_") for k in keys)
        assert not any(k.startswith("st689_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg691" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg691") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg691")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi totali (€/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd691" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_supercondensatori_presente(self):
        src = _ui_src()
        assert "supercondensatore ≠ batteria" in src
        assert "E = 1/2 C V" in src
        assert "milioni di cicli" in src
        assert "FFR" in src
        assert "peak shaving" in src
        assert "arbitraggio energetico" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi FFR" in src
        assert "Margine" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh691_csv" in src
        assert "supercondensatori_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh691_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo FFR" in src
        assert "Prezzo picco" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st691_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W691 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab691:")
        assert "mh691_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab691" in (_new_dir() / "w691_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w691_helpers.py", "w691_ui.py",
                   "w691_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab690" not in src
        assert "tab689" not in src
        assert "tab688" not in src

    def test_topic_supercondensatori_non_batteria(self):
        # Topic corretto: il titolo e' supercondensatori
        assert "Supercondensatori" in TITLE691
        assert "batteria" not in TITLE691.lower()
