"""Test tab694 "⚡🔌 Interconnessione HVDC: il cavo in corrente continua paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
potenza 500 MW; utilizzo 0,70; spread 25
EUR/MWh; perdite 0,03; lunghezza 200 km;
costo cavo 1500000 EUR/km; convertitori
200000000 EUR; OPEX fisso 5000000
EUR/anno; vita 40 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del CAPEX).

- energia_lorda_mwh = 3066000.0
- energia_netta_mwh = 2974020.0
- capex_tot_eur = 500000000.0
- ricavi_eur_a = 74350500.0
- margine_eur_a = 69350500.0
- costo_livellato_eur_mwh = 11.479102555805778
- van = 689991218.1926918
- tir = 13.791077418736581
- payback = 8
- verdetto = 'CONVIENTE'

Scomposizione: lorda 500 x 8760 x 0,70 =
3066000; netta 3066000 x (1 - 0,03) =
2974020; CAPEX 200 x 1500000 + 200000000
= 500000000; ricavi 2974020 x 25 =
74350500; margine 74350500 - 5000000 =
69350500; CRF 0,05 x 1,05^40 / (1,05^40 -
1) = 0,058278161166034986; costo
livellato (500000000 x CRF + 5000000) /
2974020 = 11,479102555805778; VAN
-500000000 + 69350500 x (1 - 1,05^-40) /
0,05 = 689991218,1926918.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w694_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w694_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w694_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w694_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w694_helpers.py: {missing}")
    return out


_F = _load("mh694_num", "mh694_nneg", "mh694_pos",
           "mh694_int_pos", "mh694_frac_util",
           "mh694_frac_perdite", "mh694_tol",
           "mh694_energia_lorda", "mh694_energia_netta",
           "mh694_capex", "mh694_ricavi", "mh694_margine",
           "mh694_crf", "mh694_costo_livellato",
           "mh694_van", "mh694_tir",
           "mh694_payback", "mh694_verdetto",
           "_mh694_neutro", "mh694_calcola",
           "mh694_sensitivita", "mh694_csv",
           "mh694_demo", "demo_calcoli")

TITLE694 = ("⚡🔌 Interconnessione HVDC: "
            "il cavo in corrente continua paga?")

LORDA_DEMO = 3066000.0
NETTA_DEMO = 2974020.0
CAPEX_DEMO = 500000000.0
RICAVI_DEMO = 74350500.0
MARG_DEMO = 69350500.0
LIVELLATO_DEMO = 11.479102555805778
VAN_DEMO = 689991218.1926918
TIR_DEMO = 13.791077418736581
PAYBACK_DEMO = 8
VITA_DEMO = 40
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.058278161166034986

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w694_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w694_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh694_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh694_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh694_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh694_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh694_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh694_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh694_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh694_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh694_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh694_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh694_int_pos"](40.0, "x") == 40

    def test_util_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh694_frac_util"](0.0, "x")

    def test_util_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh694_frac_util"](1.01, "x")

    def test_util_accetta_uno(self):
        assert _F["mh694_frac_util"](1.0, "x") == 1.0

    def test_perdite_accetta_zero(self):
        assert _F["mh694_frac_perdite"](0.0, "x") == 0.0

    def test_perdite_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh694_frac_perdite"](1.0, "x")

    def test_perdite_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh694_frac_perdite"](1.01, "x")

    def test_perdite_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh694_frac_perdite"](-0.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh694_tol"](-0.01, "x")

    def test_tol_accetta_zero_e_oltre_uno(self):
        # Spec tab694: tolleranza >= 0, senza tetto.
        assert _F["mh694_tol"](0.0, "x") == 0.0
        assert _F["mh694_tol"](1.5, "x") == 1.5


class TestFisicaEconomia:
    def test_energia_lorda_demo(self):
        assert _F["mh694_energia_lorda"](
            500.0, 0.70) == pytest.approx(LORDA_DEMO, rel=REL)

    def test_energia_lorda_utilizzo_uno(self):
        assert _F["mh694_energia_lorda"](
            500.0, 1.0) == pytest.approx(4380000.0, rel=REL)

    def test_energia_lorda_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh694_energia_lorda"](0.0, 0.70)

    def test_energia_lorda_rifiuta_utilizzo_zero(self):
        with pytest.raises(ValueError):
            _F["mh694_energia_lorda"](500.0, 0.0)

    def test_energia_lorda_rifiuta_utilizzo_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh694_energia_lorda"](500.0, 1.01)

    def test_energia_netta_demo(self):
        assert _F["mh694_energia_netta"](
            LORDA_DEMO, 0.03) == pytest.approx(
            NETTA_DEMO, rel=REL)

    def test_energia_netta_perdite_zero(self):
        assert _F["mh694_energia_netta"](
            LORDA_DEMO, 0.0) == LORDA_DEMO

    def test_energia_netta_rifiuta_perdite_uno(self):
        with pytest.raises(ValueError):
            _F["mh694_energia_netta"](LORDA_DEMO, 1.0)

    def test_capex_demo(self):
        assert _F["mh694_capex"](
            200.0, 1500000.0, 200000000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_convertitori(self):
        assert _F["mh694_capex"](
            0.0, 1500000.0, 200000000.0) == 200000000.0

    def test_capex_zero(self):
        assert _F["mh694_capex"](0.0, 0.0, 0.0) == 0.0

    def test_capex_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh694_capex"](-1.0, 1500000.0, 200000000.0)
        with pytest.raises(ValueError):
            _F["mh694_capex"](200.0, -1.0, 200000000.0)
        with pytest.raises(ValueError):
            _F["mh694_capex"](200.0, 1500000.0, -1.0)

    def test_ricavi_demo(self):
        assert _F["mh694_ricavi"](
            NETTA_DEMO, 25.0) == pytest.approx(
            RICAVI_DEMO, rel=REL)

    def test_ricavi_spread_zero(self):
        assert _F["mh694_ricavi"](NETTA_DEMO, 0.0) == 0.0

    def test_margine_demo(self):
        assert _F["mh694_margine"](
            RICAVI_DEMO, 5000000.0) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh694_margine"](100.0, 200.0) == -100.0

    def test_crf_demo(self):
        assert _F["mh694_crf"](
            0.05, 40) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh694_crf"](0.0, 40) == pytest.approx(
            0.025, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 40 / (1.05 ** 40 - 1.0)
        assert _F["mh694_crf"](0.05, 40) == pytest.approx(
            atteso, rel=1e-12)

    def test_costo_livellato_demo(self):
        assert _F["mh694_costo_livellato"](
            CAPEX_DEMO, CRF_DEMO, 5000000.0,
            NETTA_DEMO) == pytest.approx(
            LIVELLATO_DEMO, rel=REL)

    def test_costo_livellato_none_se_netta_zero(self):
        assert _F["mh694_costo_livellato"](
            CAPEX_DEMO, CRF_DEMO, 5000000.0,
            0.0) is None

    def test_costo_livellato_none_se_netta_negativa(self):
        assert _F["mh694_costo_livellato"](
            CAPEX_DEMO, CRF_DEMO, 5000000.0,
            -1.0) is None


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh694_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARG_DEMO * (
            1.0 - 1.05 ** (-40)) / 0.05
        assert _F["mh694_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh694_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            40) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 40, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 40 == pytest.approx(
            2274020000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh694_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 40)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh694_van"](MARG_DEMO, -1.0, 0.05, 40)

    def test_tir_demo(self):
        assert _F["mh694_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh694_tir"](CAPEX_DEMO, 0.0, 40) is None
        assert _F["mh694_tir"](CAPEX_DEMO, -100.0, 40) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh694_tir"](0.0, MARG_DEMO, 40) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh694_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh694_tir"](CAPEX_DEMO, MARG_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 41))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh694_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARG_DEMO * 7 < 0.0
        assert -CAPEX_DEMO + MARG_DEMO * 8 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh694_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh694_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh694_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh694_payback"](
            5000000000.0, MARG_DEMO, 40) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh694_payback"](0.0, MARG_DEMO, 40) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh694_payback"](CAPEX_DEMO, 0.0, 40) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh694_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_non_conviente(self):
        # Spec tab694: CONVIENTE solo se VAN > 0.
        assert _F["mh694_verdetto"](
            0.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh694_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh694_verdetto"](
            -50000000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh694_verdetto"](
            -50000001.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh694_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh694_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh694_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh694_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh694_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh694_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh694_demo"]()
        d.update(kw)
        return _F["mh694_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["energia_lorda_mwh"] == pytest.approx(
            LORDA_DEMO, rel=REL)
        assert c["energia_netta_mwh"] == pytest.approx(
            NETTA_DEMO, rel=REL)
        assert c["capex_tot_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["ricavi_eur_a"] == pytest.approx(
            RICAVI_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["costo_livellato_eur_mwh"] == pytest.approx(
            LIVELLATO_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "margine_eur_a"] == _F["demo_calcoli"]()[
            "margine_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh694_calcola(**mh694_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh694_demo"]()
        b = _F["mh694_calcola"](**d)
        coppie = [("energia_lorda_mwh", LORDA_DEMO),
                  ("energia_netta_mwh", NETTA_DEMO),
                  ("capex_tot_eur", CAPEX_DEMO),
                  ("ricavi_eur_a", RICAVI_DEMO),
                  ("margine_eur_a", MARG_DEMO),
                  ("costo_livellato_eur_mwh", LIVELLATO_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh694_demo"]()
        assert d["potenza_mw"] == 500.0
        assert d["utilizzo_frac"] == 0.70
        assert d["spread_eur_mwh"] == 25.0
        assert d["perdite_frac"] == 0.03
        assert d["lunghezza_km"] == 200.0
        assert d["costo_cavo_eur_km"] == 1500000.0
        assert d["costo_convertitori_eur"] == 200000000.0
        assert d["opex_fisso_eur_a"] == 5000000.0
        assert d["vita_anni"] == 40
        assert d["wacc_frac"] == 0.05
        assert d["toll_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_lorda_mwh",
                       "energia_netta_mwh",
                       "capex_tot_eur",
                       "ricavi_eur_a",
                       "margine_eur_a",
                       "costo_livellato_eur_mwh",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_perdite_zero_calcolabile(self):
        # Perdite 0: netta 3066000, ricavi 76650000,
        # margine 71650000
        n = self._bc(perdite_frac=0.0)
        assert n["valid"] is True
        assert n["energia_netta_mwh"] == pytest.approx(
            3066000.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            71650000.0, rel=REL)

    def test_utilizzo_uno_calcolabile(self):
        # Utilizzo 1,0: lorda 4380000, netta
        # 4248600, ricavi 106215000, margine
        # 101215000
        n = self._bc(utilizzo_frac=1.0)
        assert n["valid"] is True
        assert n["energia_lorda_mwh"] == pytest.approx(
            4380000.0, rel=REL)
        assert n["energia_netta_mwh"] == pytest.approx(
            4248600.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            101215000.0, rel=REL)

    def test_perdite_uno_neutro(self):
        n = self._bc(perdite_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_perdite_oltre_uno_neutro(self):
        n = self._bc(perdite_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_spread_zero_neutro(self):
        # Ricavi 0, margine -5000000
        n = self._bc(spread_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_mw=-10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_utilizzo_zero_neutro(self):
        n = self._bc(utilizzo_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_utilizzo_oltre_uno_neutro(self):
        n = self._bc(utilizzo_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_lunghezza_negativa_neutro(self):
        n = self._bc(lunghezza_km=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costi_negativi_neutro(self):
        for k in ("costo_cavo_eur_km",
                  "costo_convertitori_eur",
                  "opex_fisso_eur_a"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=39.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -500000000 + 69350500 / 1,05 < 0,
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

    def test_nan_neutro(self):
        n = self._bc(spread_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_mw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(potenza_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX fisso enorme: 74350500 - 80000000 < 0
        n = self._bc(opex_fisso_eur_a=80000000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 40, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(lunghezza_km=0.0,
                     costo_convertitori_eur=0.0)
        assert n["capex_tot_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # Convertitori 900000000: CAPEX 1200000000,
        # VAN circa -10008781,81, entro il 10 %
        # di 1200000000
        n = self._bc(costo_convertitori_eur=900000000.0)
        assert n["capex_tot_eur"] == pytest.approx(
            1200000000.0, rel=REL)
        assert n["van"] == pytest.approx(
            -10008781.807308197, rel=1e-9)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 1200000000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(costo_convertitori_eur=2000000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh694_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh694_neutro"]()
        for chiave in ("valid",
                       "energia_lorda_mwh",
                       "energia_netta_mwh",
                       "capex_tot_eur",
                       "ricavi_eur_a",
                       "margine_eur_a",
                       "costo_livellato_eur_mwh",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["costo_livellato_eur_mwh"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 15
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia lorda (MWh/anno)" in voci
        assert "Energia netta (MWh/anno)" in voci
        assert "CAPEX totale (EUR)" in voci
        assert "Ricavi (EUR/anno)" in voci
        assert "Margine (EUR/anno)" in voci
        assert "Costo livellato (EUR/MWh)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh694_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh694_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.8", "x1.0", "x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh694_sensitivita"](self._ing())
        assert s.loc["x1.0", "x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_crescente_con_spread(self):
        # VAN cresce con lo spread
        s = _F["mh694_sensitivita"](self._ing())
        for colonna in ("x0.8", "x1.0", "x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_crescente_con_utilizzo(self):
        # VAN cresce con l'utilizzo
        s = _F["mh694_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "x0.8"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.2"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il margine resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh694_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh694_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh694_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 21

    def test_csv_contiene_verdetto_e_margine(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh694_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_eur_a" in txt
        assert "costo_livellato_eur_mwh" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "ricavi_eur_a" in txt
        assert "spread_eur_mwh" in txt
        assert "potenza_mw" in txt
        assert "energia_netta_mwh" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh694_csv"](bc, self._ing())
        assert f"ricavi_eur_a;{RICAVI_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"capex_tot_eur;{CAPEX_DEMO}" in txt
        assert f"energia_netta_mwh;{NETTA_DEMO}" in txt
        assert "opex_fisso_eur_a;5000000.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def694["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def694\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 11, ui_keys
        demo_keys = set(_F["mh694_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh694_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh694_demo():")
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
        demo_keys = set(re.findall(r'"([a-z0-9_]+)":', body))
        ui_keys = set(re.findall(r'_def694\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W694 (25/10/2026) - tab694' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh694_num", "mh694_nneg", "mh694_pos",
                     "mh694_int_pos", "mh694_frac_util",
                     "mh694_frac_perdite", "mh694_tol",
                     "mh694_energia_lorda",
                     "mh694_energia_netta", "mh694_capex",
                     "mh694_ricavi", "mh694_margine",
                     "mh694_crf", "mh694_costo_livellato",
                     "mh694_van", "mh694_tir",
                     "mh694_payback", "mh694_verdetto",
                     "_mh694_neutro", "mh694_calcola",
                     "mh694_sensitivita", "mh694_csv",
                     "mh694_demo", "demo_calcoli"):
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
        # l'apply (come w693_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w694_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE694) == 1

    def test_blocco_with_tab694(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab694:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE694

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st694_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 16, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st693_") for k in keys)
        assert not any(k.startswith("st692_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg694" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg694") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg694")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia netta (MWh/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src
        assert "Costo livellato (€/MWh)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd694" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_hvdc_presente(self):
        src = _ui_src()
        assert "HVDC" in src
        assert "convertitori" in src
        assert "sottomarini" in src
        assert "AC" in src
        assert "spread" in src
        assert "energia netta" in src
        assert "3 %" in src or "3%" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi" in src
        assert "Margine" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh694_csv" in src
        assert "interconnessione_hvdc_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh694_sensitivita" in src
        assert "Heatmap" in src
        assert "Spread" in src
        assert "Utilizzo" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st694_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W694 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab694:")
        assert "mh694_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab694" in (_new_dir() / "w694_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w694_helpers.py", "w694_ui.py",
                   "w694_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab693" not in src
        assert "tab692" not in src
        assert "tab691" not in src

    def test_topic_hvdc_non_ac(self):
        # Topic corretto: il titolo e' HVDC in
        # corrente continua, non AC generica
        assert "HVDC" in TITLE694
        assert "corrente continua" in TITLE694.lower()
