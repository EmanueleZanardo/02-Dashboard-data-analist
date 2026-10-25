"""Test tab698 "🌡️🕳️ Sonde geotermiche: la pompa di calore dal sottosuolo paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
domanda 300 MWh/anno; picco 150 kW; resa 50
W/m; COP 4,5; prezzo elettricita' 220 EUR/MWh;
OPEX annuo 2000 EUR/anno; rendimento caldaia
0,9; prezzo gas 90 EUR/MWh; costo perforazione
40 EUR/m; costo pompa 15000 EUR; vita 25 anni;
WACC 5 %; tolleranza 10 % del CAPEX; fattore
gas 0,20 tCO2/MWh; fattore elettricita' 0,35
tCO2/MWh.

- lunghezza_sonde_m = 3000.0
- energia_elettrica_mwh_a = 66.66666666666667
- costo_baseline_eur_a = 30000.0
- costo_pompa_eur_a = 16666.666666666668
- risparmio_eur_a = 13333.333333333332
- co2_evitata_t_a = 43.33333333333334
- capex_eur = 135000.0
- van = 52919.26088059679
- tir = 8.629383397020145
- payback = 11
- verdetto = 'CONVIENTE'

Scomposizione: lunghezza 150 x 1000 / 50 =
3000; e_el 300 / 4,5 = 66,66666666666667;
c_base 300 / 0,9 x 90 = 30000,0; c_hp
66,66666666666667 x 220 + 2000 =
16666,666666666668; risparmio 30000,0 -
16666,666666666668 = 13333,333333333332; co2
300 / 0,9 x 0,20 - 66,66666666666667 x 0,35 =
43,33333333333334; capex 3000 x 40 + 15000 =
135000,0; VAN -135000,0 +
13333,333333333332 x (1 - 1,05^-25) / 0,05 =
52919,26088059679; payback: cumulato anno 10
-1666,66666666668, anno 11 +11666,66666666665
-> 11.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w699_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w699_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w699_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w699_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w699_helpers.py: {missing}")
    return out


_F = _load("mh698_num", "mh698_nneg", "mh698_pos",
           "mh698_int_pos", "mh698_pct_range",
           "mh698_cop_valido", "mh698_rendimento_valido",
           "mh698_lunghezza_sonde",
           "mh698_energia_elettrica",
           "mh698_costo_baseline", "mh698_costo_pompa",
           "mh698_risparmio", "mh698_co2_evitata",
           "mh698_capex", "mh698_crf", "mh698_van",
           "mh698_tir", "mh698_payback",
           "mh698_verdetto", "mh698_valida",
           "_mh698_neutro", "mh698_calcola",
           "mh698_sensitivita", "mh698_csv",
           "mh698_demo", "demo_calcoli")

TITLE698 = ("🌡️🕳️ Sonde geotermiche: "
            "la pompa di calore dal sottosuolo paga?")

LUNG_DEMO = 3000.0
E_EL_DEMO = 66.66666666666667
C_BASE_DEMO = 30000.0
C_HP_DEMO = 16666.666666666668
RISP_DEMO = 13333.333333333332
CO2_DEMO = 43.33333333333334
CAPEX_DEMO = 135000.0
VAN_DEMO = 52919.26088059679
TIR_DEMO = 8.629383397020145
PAYBACK_DEMO = 11
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.0709524572992296

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w699_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w699_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh698_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh698_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh698_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh698_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh698_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh698_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh698_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh698_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh698_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh698_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh698_int_pos"](25.0, "x") == 25

    def test_pct_range_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh698_pct_range"](-0.01, "x")

    def test_pct_range_rifiuta_cento(self):
        with pytest.raises(ValueError):
            _F["mh698_pct_range"](100.0, "x")

    def test_pct_range_accetta_zero(self):
        assert _F["mh698_pct_range"](0.0, "x") == 0.0

    def test_pct_range_accetta_99(self):
        assert _F["mh698_pct_range"](99.9, "x") == 99.9

    def test_cop_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh698_cop_valido"](1.0, "x")

    def test_cop_rifiuta_sotto_uno(self):
        with pytest.raises(ValueError):
            _F["mh698_cop_valido"](0.5, "x")

    def test_cop_accetta_sopra_uno(self):
        assert _F["mh698_cop_valido"](4.5, "x") == 4.5

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh698_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh698_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh698_rendimento_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh698_demo"]()
        d.update(kw)
        return _F["mh698_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        v = self._val(domanda_mwh_a=0.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_picco_zero_non_valido(self):
        v = self._val(potenza_picco_kw=0.0)
        assert v["valido"] is False

    def test_resa_zero_non_valida(self):
        v = self._val(resa_specifica_w_m=0.0)
        assert v["valido"] is False

    def test_resa_negativa_non_valida(self):
        v = self._val(resa_specifica_w_m=-1.0)
        assert v["valido"] is False

    def test_cop_uno_non_valido(self):
        v = self._val(cop=1.0)
        assert v["valido"] is False

    def test_cop_sotto_uno_non_valido(self):
        v = self._val(cop=0.8)
        assert v["valido"] is False

    def test_prezzo_elettricita_zero_non_valido(self):
        v = self._val(prezzo_elettricita_eur_mwh=0.0)
        assert v["valido"] is False

    def test_rendimento_zero_non_valido(self):
        v = self._val(rendimento_caldaia=0.0)
        assert v["valido"] is False

    def test_rendimento_sopra_uno_non_valido(self):
        v = self._val(rendimento_caldaia=1.2)
        assert v["valido"] is False

    def test_prezzo_gas_zero_non_valido(self):
        v = self._val(prezzo_gas_eur_mwh=0.0)
        assert v["valido"] is False

    def test_prezzi_negativi_non_validi(self):
        for k in ("prezzo_elettricita_eur_mwh",
                  "prezzo_gas_eur_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False

    def test_fattori_negativi_non_validi(self):
        for k in ("fattore_gas", "fattore_elettricita"):
            assert self._val(**{k: -0.01})["valido"] is False

    def test_wacc_cento_non_valido(self):
        v = self._val(wacc_pct=100.0)
        assert v["valido"] is False

    def test_tolleranza_cento_non_valida(self):
        v = self._val(tolleranza_pct=100.0)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=24.5)
        assert v["valido"] is False

    def test_costi_negativi_non_validi(self):
        for k in ("costo_perforazione_eur_m",
                  "costo_pompa_eur", "opex_annuo"):
            assert self._val(**{k: -1.0})["valido"] is False

    def test_nan_non_valido(self):
        v = self._val(cop=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(domanda_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(domanda_mwh_a=True)
        assert v["valido"] is False


class TestFisicaEconomia:
    def test_lunghezza_demo(self):
        assert _F["mh698_lunghezza_sonde"](
            150.0, 50.0) == pytest.approx(LUNG_DEMO, rel=REL)

    def test_lunghezza_rifiuta_resa_zero(self):
        with pytest.raises(ValueError):
            _F["mh698_lunghezza_sonde"](150.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh698_lunghezza_sonde"](0.0, 50.0)

    def test_lunghezza_scala_con_picco(self):
        assert _F["mh698_lunghezza_sonde"](
            300.0, 50.0) == pytest.approx(6000.0, rel=REL)

    def test_lunghezza_cala_con_resa(self):
        assert _F["mh698_lunghezza_sonde"](
            150.0, 100.0) == pytest.approx(1500.0, rel=REL)

    def test_energia_elettrica_demo(self):
        assert _F["mh698_energia_elettrica"](
            300.0, 4.5) == pytest.approx(E_EL_DEMO, rel=REL)

    def test_energia_elettrica_rifiuta_cop_uno(self):
        with pytest.raises(ValueError):
            _F["mh698_energia_elettrica"](300.0, 1.0)

    def test_costo_baseline_demo(self):
        assert _F["mh698_costo_baseline"](
            300.0, 0.9, 90.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_baseline_rifiuta_rendimento_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh698_costo_baseline"](300.0, 1.2, 90.0)

    def test_costo_baseline_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh698_costo_baseline"](300.0, 0.0, 90.0)

    def test_costo_pompa_demo(self):
        assert _F["mh698_costo_pompa"](
            E_EL_DEMO, 220.0, 2000.0) == pytest.approx(
            C_HP_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh698_risparmio"](
            C_BASE_DEMO, C_HP_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh698_risparmio"](
            10000.0, 16666.666666666668) == pytest.approx(
            -6666.666666666668, rel=REL)

    def test_co2_demo(self):
        assert _F["mh698_co2_evitata"](
            300.0, 0.9, 0.20,
            E_EL_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_puo_essere_negativa(self):
        assert _F["mh698_co2_evitata"](
            300.0, 0.9, 0.05,
            E_EL_DEMO, 0.90) < 0.0

    def test_capex_demo(self):
        assert _F["mh698_capex"](
            LUNG_DEMO, 40.0, 15000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_pompa(self):
        assert _F["mh698_capex"](
            LUNG_DEMO, 0.0, 15000.0) == 15000.0

    def test_crf_demo(self):
        assert _F["mh698_crf"](
            0.05, 25) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh698_crf"](0.0, 25) == pytest.approx(
            0.04, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 25 / (1.05 ** 25 - 1.0)
        assert _F["mh698_crf"](0.05, 25) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh698_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-25)) / 0.05
        assert _F["mh698_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh698_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            25) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 25, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh698_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 25)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh698_van"](RISP_DEMO, -1.0, 0.05, 25)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh698_tir"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh698_tir"](CAPEX_DEMO, 0.0, 25) is None
        assert _F["mh698_tir"](CAPEX_DEMO, -100.0, 25) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh698_tir"](0.0, RISP_DEMO, 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh698_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh698_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 26))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh698_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 10 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 11 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh698_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh698_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh698_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh698_payback"](
            50000000.0, RISP_DEMO, 25) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh698_payback"](0.0, RISP_DEMO, 25) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh698_payback"](CAPEX_DEMO, 0.0, 25) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh698_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh698_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh698_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh698_verdetto"](
            -13500.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh698_verdetto"](
            -13500.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh698_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh698_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh698_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh698_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh698_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh698_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh698_demo"]()
        d.update(kw)
        return _F["mh698_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["lunghezza_sonde_m"] == pytest.approx(
            LUNG_DEMO, rel=REL)
        assert c["energia_elettrica_mwh_a"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_pompa_eur_a"] == pytest.approx(
            C_HP_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.05
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh698_calcola(**mh698_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (VAN ±1 EUR,
        TIR ±0,05 punti), chiave per chiave."""
        d = _F["mh698_demo"]()
        b = _F["mh698_calcola"](**d)
        coppie = [("lunghezza_sonde_m", LUNG_DEMO),
                  ("energia_elettrica_mwh_a", E_EL_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_pompa_eur_a", C_HP_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh698_demo"]()
        assert d["domanda_mwh_a"] == 300.0
        assert d["potenza_picco_kw"] == 150.0
        assert d["resa_specifica_w_m"] == 50.0
        assert d["cop"] == 4.5
        assert d["prezzo_elettricita_eur_mwh"] == 220.0
        assert d["opex_annuo"] == 2000.0
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 90.0
        assert d["costo_perforazione_eur_m"] == 40.0
        assert d["costo_pompa_eur"] == 15000.0
        assert d["vita_anni"] == 25
        assert d["wacc_pct"] == 5.0
        assert d["tolleranza_pct"] == 10.0
        assert d["fattore_gas"] == 0.20
        assert d["fattore_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("lunghezza_sonde_m",
                       "energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 11" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_domanda_dimezzata(self):
        # Domanda 150 MWh/a (picco invariato):
        # e_el 33,3333; c_base 15000,0; c_hp
        # 9333,3333; risparmio 5666,6667; co2
        # 21,6667; capex invariato 135000,0
        n = self._bc(domanda_mwh_a=150.0)
        assert n["valid"] is True
        assert n["energia_elettrica_mwh_a"] == pytest.approx(
            33.333333333333336, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            5666.666666666666, rel=REL)
        assert n["co2_evitata_t_a"] == pytest.approx(
            21.666666666666668, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_cop_cinque(self):
        # COP 5,0: e_el 60,0; c_hp 15200,0;
        # risparmio 14800,0; capex invariato
        n = self._bc(cop=5.0)
        assert n["valid"] is True
        assert n["energia_elettrica_mwh_a"] == pytest.approx(
            60.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            14800.0, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["errore"] != ""
        assert n["tir"] is None
        assert n["payback"] is None

    def test_resa_zero_neutro(self):
        n = self._bc(resa_specifica_w_m=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cop_uno_neutro(self):
        n = self._bc(cop=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cop_sotto_uno_neutro(self):
        n = self._bc(cop=0.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_sopra_uno_neutro(self):
        n = self._bc(rendimento_caldaia=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_zero_neutro(self):
        n = self._bc(rendimento_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=24.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -135000 + 13333,33 / 1,05 < 0, oltre
        # tolleranza; payback mai
        n = self._bc(vita_anni=1)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_vita_tredici_marginale(self):
        # VAN circa -9752, entro il 10 % del CAPEX
        n = self._bc(vita_anni=13)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 11

    def test_vita_quindici_conviente(self):
        n = self._bc(vita_anni=15)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_cento_neutro(self):
        n = self._bc(wacc_pct=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_cento_neutro(self):
        n = self._bc(tolleranza_pct=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(cop=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(domanda_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risparmio_negativo_neutro(self):
        # Prezzo elettricita' 600: c_hp 42000,0
        # contro c_base 30000,0 -> risparmio < 0
        n = self._bc(prezzo_elettricita_eur_mwh=600.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_risparmio_zero_non_calcolabile(self):
        # COP tale che c_hp = c_base: prezzo_el
        # 220, opex 2000 -> e_el = 28000/220 =
        # 127,2727 -> COP = 300/127,2727 = 2,3571
        # (approssimato: si usa il caso limite via
        # verdetto diretto, non via calcola)
        assert _F["mh698_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 25, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_perforazione_eur_m=0.0,
                     costo_pompa_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_capex_zero_van_negativo_mai_marginale(self):
        # Caso costruito via verdetto: CAPEX 0 e
        # VAN negativo non puo' essere MARGINALE
        assert _F["mh698_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh698_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh698_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "lunghezza_sonde_m",
                       "energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 20
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Lunghezza sonde (m)" in voci
        assert "Energia elettrica annua (MWh/anno)" in voci
        assert "Costo baseline (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh698_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh698_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh698_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cop(self):
        # VAN cresce con il COP: meno elettricita'
        # assorbita e piu' risparmio, a parita'
        # di prezzo
        s = _F["mh698_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettricita(self):
        # VAN cala con il prezzo elettricita':
        # il costo della pompa sale, il risparmio
        # scende
        s = _F["mh698_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il risparmio resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh698_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh698_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_sensitivita_payback_coerente(self):
        # Payback demo 11: cumulato anno 10 < 0,
        # anno 11 >= 0
        assert -CAPEX_DEMO + RISP_DEMO * 10 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 11 >= 0.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh698_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 26

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh698_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_pompa_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_mwh_a" in txt
        assert "lunghezza_sonde_m" in txt
        assert "co2_evitata_t_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh698_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"lunghezza_sonde_m;{LUNG_DEMO}" in txt
        assert f"energia_elettrica_mwh_a;{E_EL_DEMO}" in txt
        assert "opex_annuo;2000.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def698["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def698\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh698_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh698_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh698_demo():")
        depth = 0
        body = ""
        started = False
        for ch in src[start:]:
            body += ch
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
                if started and depth == 0:
                    break
        demo_keys = set(re.findall(r'"([A-Za-z0-9_]+)":', body))
        ui_keys = set(re.findall(r'_def698\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W699 (25/10/2026) - tab698' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh698_num", "mh698_nneg", "mh698_pos",
                     "mh698_int_pos", "mh698_pct_range",
                     "mh698_cop_valido",
                     "mh698_rendimento_valido",
                     "mh698_lunghezza_sonde",
                     "mh698_energia_elettrica",
                     "mh698_costo_baseline",
                     "mh698_costo_pompa",
                     "mh698_risparmio",
                     "mh698_co2_evitata",
                     "mh698_capex", "mh698_crf",
                     "mh698_van", "mh698_tir",
                     "mh698_payback", "mh698_verdetto",
                     "mh698_valida", "_mh698_neutro",
                     "mh698_calcola", "mh698_sensitivita",
                     "mh698_csv", "mh698_demo",
                     "demo_calcoli"):
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
        # l'apply: si dedenta prima del parse,
        # come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w699_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE698) == 1

    def test_blocco_with_tab698(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab698:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE698

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st698_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st698_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone del brief
        (15 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st698_[a-z0-9_]+)"', _ui_src())
        attese = ["st698_domanda", "st698_picco",
                  "st698_resa", "st698_cop",
                  "st698_prezzo_elettricita", "st698_opex",
                  "st698_rendimento", "st698_prezzo_gas",
                  "st698_fattore_gas",
                  "st698_fattore_elettricita",
                  "st698_costo_perforazione", "st698_costo_pompa",
                  "st698_vita", "st698_wacc_pct",
                  "st698_tolleranza_pct", "st698_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg698" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg698") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg698")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Lunghezza sonde (m)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd698" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_sonde_presente(self):
        src = _ui_src()
        assert "50" in src and "150 m" in src
        assert "10" in src and "12 °C" in src
        assert "geotermia profonda" in src.lower()
        assert "autorizzazione" in src.lower()
        assert "trivellazione" in src.lower()
        assert "falda" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline caldaia a gas" in src
        assert "Pompa di calore" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh698_csv" in src
        assert "sonde_geotermiche_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh698_sensitivita" in src
        assert "Heatmap" in src
        assert "COP" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st698_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W699 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab698:")
        assert "mh698_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab698" in (_new_dir() / "w699_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w699_helpers.py", "w699_ui.py",
                   "w699_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab698"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "69" + "7"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w699_helpers.py", "w699_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_sonde_non_geotermia_profonda(self):
        # Topic corretto: il titolo parla di sonde
        # geotermiche / pompa di calore, non di
        # centrale elettrica geotermica
        assert "Sonde geotermiche" in TITLE698
        assert "pompa di calore" in TITLE698.lower()
