"""Test tab690 "🔌⚡ Grid-forming + inerzia sintetica: la batteria che forma la rete paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
potenza grid-forming 20 MW; capacita' 20 MWh;
inerzia sintetica H 5 s; tempo di risposta
100 ms; prezzo grid-forming 45000 EUR/MW/anno;
disponibilita' 0,97; eventi 60/anno; prezzo
evento 3000 EUR; durata evento 0,25 h; costo
evento 2000 EUR; OPEX fisso 250000 EUR/anno;
CAPEX 5000000 EUR; vita 15 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del CAPEX);
fattore rete 0,35 t/MWh.

- ricavi_gf_eur_a = 873000.0
- ricavi_eventi_eur_a = 180000.0
- ricavi_tot_eur_a = 1053000.0
- costi_eventi_eur_a = 120000.0
- opex_fisso_eur_a = 250000.0
- costi_tot_eur_a = 370000.0
- margine_eur_a = 683000.0
- energia_eventi_mwh_a = 300.0
- energia_inerziale_mj = 100.0
- co2_evitata_t_a = 105.0
- capex_eur = 5000000.0
- van = 2089306.4400773495
- tir = 10.677728941424014
- payback = 8
- verdetto = 'CONVIENTE'

Scomposizione: grid-forming 20 x 45000 x 0,97 =
873000; eventi 60 x 3000 = 180000; ricavi
1053000; costi eventi 60 x 2000 = 120000;
costi 120000 + 250000 = 370000; margine
1053000 - 370000 = 683000; energia eventi
60 x 20 x 0,25 = 300 MWh; energia inerziale
5 x 20 = 100 MJ; CO2 300 x 0,35 = 105 t.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w690_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w690_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w690_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w690_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w690_helpers.py: {missing}")
    return out


_F = _load("mh690_num", "mh690_nneg", "mh690_pos",
           "mh690_int_pos", "mh690_int_nneg",
           "mh690_tol", "mh690_frac",
           "mh690_ricavi_gf", "mh690_ricavi_eventi",
           "mh690_ricavi_tot", "mh690_costi_eventi",
           "mh690_costi_tot", "mh690_margine",
           "mh690_energia_eventi",
           "mh690_energia_inerziale", "mh690_co2",
           "mh690_capex",
           "mh690_van", "mh690_tir",
           "mh690_payback", "mh690_verdetto",
           "_mh690_neutro", "mh690_calcola",
           "mh690_sensitivita", "mh690_csv",
           "mh690_demo", "demo_calcoli")

TITLE690 = ("🔌⚡ Grid-forming + inerzia sintetica: "
            "la batteria che forma la rete paga?")

RG_DEMO = 873000.0
RE_DEMO = 180000.0
RTOT_DEMO = 1053000.0
CE_DEMO = 120000.0
OPEX_DEMO = 250000.0
CTOT_DEMO = 370000.0
MARG_DEMO = 683000.0
EE_DEMO = 300.0
EI_DEMO = 100.0
CO2_DEMO = 105.0
CAPEX_DEMO = 5000000.0
VAN_DEMO = 2089306.4400773495
TIR_DEMO = 10.677728941424014
PAYBACK_DEMO = 8
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w690_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w690_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh690_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh690_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh690_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh690_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh690_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh690_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh690_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh690_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh690_int_pos"](15.0, "x") == 15

    def test_int_nneg_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh690_int_nneg"](2.5, "x")

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_int_nneg"](-1, "x")

    def test_int_nneg_accetta_zero(self):
        assert _F["mh690_int_nneg"](0, "x") == 0

    def test_int_nneg_accetta_float_intero(self):
        assert _F["mh690_int_nneg"](60.0, "x") == 60

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh690_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh690_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh690_tol"](0.0, "x") == 0.0
        assert _F["mh690_tol"](1.0, "x") == 1.0

    def test_frac_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh690_frac"](0.0, "x")

    def test_frac_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh690_frac"](1.01, "x")

    def test_frac_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh690_frac"](-0.01, "x")

    def test_frac_accetta_uno(self):
        assert _F["mh690_frac"](1.0, "x") == 1.0

    def test_frac_accetta_demo(self):
        assert _F["mh690_frac"](0.97, "x") == 0.97


class TestFisicaEconomia:
    def test_ricavi_gf_demo(self):
        assert _F["mh690_ricavi_gf"](
            20.0, 45000.0, 0.97) == pytest.approx(
            RG_DEMO, rel=REL)

    def test_ricavi_gf_formula(self):
        assert _F["mh690_ricavi_gf"](
            10.0, 40000.0, 1.0) == pytest.approx(
            400000.0, rel=1e-12)

    def test_ricavi_gf_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh690_ricavi_gf"](0.0, 45000.0, 0.97)

    def test_ricavi_gf_rifiuta_prezzo_zero(self):
        with pytest.raises(ValueError):
            _F["mh690_ricavi_gf"](20.0, 0.0, 0.97)

    def test_ricavi_gf_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_ricavi_gf"](20.0, -1.0, 0.97)

    def test_ricavi_gf_rifiuta_disponibilita_zero(self):
        with pytest.raises(ValueError):
            _F["mh690_ricavi_gf"](20.0, 45000.0, 0.0)

    def test_ricavi_gf_rifiuta_disponibilita_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh690_ricavi_gf"](20.0, 45000.0, 1.01)

    def test_ricavi_eventi_demo(self):
        assert _F["mh690_ricavi_eventi"](
            60, 3000.0) == pytest.approx(RE_DEMO, rel=REL)

    def test_ricavi_eventi_zero(self):
        assert _F["mh690_ricavi_eventi"](0, 3000.0) == 0.0

    def test_ricavi_tot_demo(self):
        assert _F["mh690_ricavi_tot"](
            RG_DEMO, RE_DEMO) == pytest.approx(
            RTOT_DEMO, rel=REL)

    def test_ricavi_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh690_ricavi_tot"](-1.0, RE_DEMO)

    def test_costi_eventi_demo(self):
        assert _F["mh690_costi_eventi"](
            60, 2000.0) == pytest.approx(CE_DEMO, rel=REL)

    def test_costi_eventi_zero(self):
        assert _F["mh690_costi_eventi"](0, 2000.0) == 0.0
        assert _F["mh690_costi_eventi"](60, 0.0) == 0.0

    def test_costi_tot_demo(self):
        assert _F["mh690_costi_tot"](
            CE_DEMO, OPEX_DEMO) == pytest.approx(
            CTOT_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh690_margine"](
            RTOT_DEMO, CTOT_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh690_margine"](100.0, 200.0) == -100.0

    def test_energia_eventi_demo(self):
        assert _F["mh690_energia_eventi"](
            60, 20.0, 0.25) == pytest.approx(
            EE_DEMO, rel=REL)

    def test_energia_eventi_zero_senza_eventi(self):
        assert _F["mh690_energia_eventi"](0, 20.0, 0.25) == 0.0

    def test_energia_inerziale_demo(self):
        assert _F["mh690_energia_inerziale"](
            5.0, 20.0) == pytest.approx(EI_DEMO, rel=REL)

    def test_energia_inerziale_zero_con_h_zero(self):
        assert _F["mh690_energia_inerziale"](0.0, 20.0) == 0.0

    def test_co2_demo(self):
        assert _F["mh690_co2"](
            EE_DEMO, 0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_zero_se_nessuna_energia(self):
        assert _F["mh690_co2"](0.0, 0.35) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_co2"](EE_DEMO, -0.01)

    def test_capex_demo(self):
        assert _F["mh690_capex"](5000000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh690_capex"](0.0) == 0.0

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_capex"](-1.0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh690_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARG_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh690_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh690_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 15, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 15 == pytest.approx(
            5245000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh690_van"](MARG_DEMO, -1.0, 0.05, 15)

    def test_tir_demo(self):
        assert _F["mh690_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh690_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh690_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh690_tir"](0.0, MARG_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh690_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh690_tir"](CAPEX_DEMO, MARG_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        # Residuo assoluto ~4 EUR su CAPEX 5M: tolleranza
        # relativa al CAPEX (1e-6), non assoluta.
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh690_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARG_DEMO * 7 < 0.0
        assert -CAPEX_DEMO + MARG_DEMO * 8 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh690_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh690_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh690_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        # -11000000 + 683000 x 15 = -755000 < 0 -> None
        assert _F["mh690_payback"](
            11000000.0, MARG_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh690_payback"](0.0, MARG_DEMO, 15) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh690_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh690_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh690_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh690_verdetto"](
            -500000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh690_verdetto"](
            -500001.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh690_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh690_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh690_verdetto"](
            0.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"
        assert _F["mh690_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh690_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh690_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh690_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh690_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 MARG_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh690_demo"]()
        d.update(kw)
        return _F["mh690_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["ricavi_gf_eur_a"] == pytest.approx(
            RG_DEMO, rel=REL)
        assert c["ricavi_eventi_eur_a"] == pytest.approx(
            RE_DEMO, rel=REL)
        assert c["ricavi_tot_eur_a"] == pytest.approx(
            RTOT_DEMO, rel=REL)
        assert c["costi_eventi_eur_a"] == pytest.approx(
            CE_DEMO, rel=REL)
        assert c["costi_tot_eur_a"] == pytest.approx(
            CTOT_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["energia_eventi_mwh_a"] == pytest.approx(
            EE_DEMO, rel=REL)
        assert c["energia_inerziale_mj"] == pytest.approx(
            EI_DEMO, rel=REL)
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
        """mh690_calcola(**mh690_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh690_demo"]()
        b = _F["mh690_calcola"](**d)
        coppie = [("ricavi_gf_eur_a", RG_DEMO),
                  ("ricavi_eventi_eur_a", RE_DEMO),
                  ("ricavi_tot_eur_a", RTOT_DEMO),
                  ("costi_eventi_eur_a", CE_DEMO),
                  ("costi_tot_eur_a", CTOT_DEMO),
                  ("margine_eur_a", MARG_DEMO),
                  ("energia_eventi_mwh_a", EE_DEMO),
                  ("energia_inerziale_mj", EI_DEMO),
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
        d = _F["mh690_demo"]()
        assert d["potenza_mw"] == 20.0
        assert d["capacita_mwh"] == 20.0
        assert d["h_sintetica_s"] == 5.0
        assert d["tempo_risposta_ms"] == 100.0
        assert d["prezzo_gf_eur_mw_a"] == 45000.0
        assert d["disponibilita_frac"] == 0.97
        assert d["n_eventi_a"] == 60
        assert d["prezzo_evento_eur"] == 3000.0
        assert d["durata_evento_h"] == 0.25
        assert d["costo_evento_eur"] == 2000.0
        assert d["opex_fisso_eur_a"] == 250000.0
        assert d["capex_eur"] == 5000000.0
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
        for chiave in ("ricavi_gf_eur_a",
                       "ricavi_eventi_eur_a",
                       "ricavi_tot_eur_a",
                       "costi_eventi_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "energia_eventi_mwh_a",
                       "energia_inerziale_mj",
                       "co2_evitata_t_a",
                       "capex_eur", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 8" in doc
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

    def test_prezzo_gf_zero_neutro(self):
        n = self._bc(prezzo_gf_eur_mw_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_gf_negativo_neutro(self):
        n = self._bc(prezzo_gf_eur_mw_a=-1.0)
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
        assert n["ricavi_gf_eur_a"] == pytest.approx(
            900000.0, rel=REL)

    def test_n_eventi_frazione_neutro(self):
        n = self._bc(n_eventi_a=60.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_n_eventi_negativo_neutro(self):
        n = self._bc(n_eventi_a=-1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nessun_evento_calcolabile(self):
        # 0 eventi: ricavi solo grid-forming 873000,
        # costi 250000, margine 623000 > 0
        n = self._bc(n_eventi_a=0)
        assert n["valid"] is True
        assert n["energia_eventi_mwh_a"] == 0.0
        assert n["co2_evitata_t_a"] == 0.0
        assert n["margine_eur_a"] == pytest.approx(
            623000.0, rel=REL)

    def test_prezzi_costi_negativi_neutro(self):
        for k in ("capacita_mwh",
                  "h_sintetica_s",
                  "tempo_risposta_ms",
                  "prezzo_evento_eur",
                  "durata_evento_h",
                  "costo_evento_eur",
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
        n = self._bc(prezzo_gf_eur_mw_a=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_mw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(potenza_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX fisso enorme: 1053000 - 1370000 < 0
        n = self._bc(opex_fisso_eur_a=1250000.0)
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
        # CAPEX 7100000: VAN = -7100000 + 7089306,44
        # circa -10694, entro il 10 % di 7100000
        n = self._bc(capex_eur=7100000.0)
        assert n["capex_eur"] == pytest.approx(
            7100000.0, rel=REL)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 7100000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(capex_eur=9000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh690_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh690_neutro"]()
        for chiave in ("valid",
                       "ricavi_gf_eur_a",
                       "ricavi_eventi_eur_a",
                       "ricavi_tot_eur_a",
                       "costi_eventi_eur_a",
                       "opex_fisso_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "energia_eventi_mwh_a",
                       "energia_inerziale_mj",
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
        assert len(b["df_tabella"]) == 18
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza grid-forming (MW)" in voci
        assert "Ricavi grid-forming (EUR/anno)" in voci
        assert "Ricavi totali (EUR/anno)" in voci
        assert "Eventi (n/anno)" in voci
        assert "Costi totali (EUR/anno)" in voci
        assert "Margine (EUR/anno)" in voci
        assert "Energia eventi (MWh/anno)" in voci
        assert "Energia inerziale (MJ)" in voci
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
        return _F["mh690_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh690_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Eventi 48",
                                   "Eventi 60",
                                   "Eventi 72"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh690_sensitivita"](self._ing())
        assert s.loc["x1.0", "Eventi 60"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona_prezzo(self):
        # VAN cresce con il prezzo grid-forming
        s = _F["mh690_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Eventi 60"]
        assert s.loc["x0.8", "Eventi 60"] < centro
        assert s.loc["x1.2", "Eventi 60"] > centro

    def test_sensitivita_crescente_con_eventi(self):
        # Ogni evento in piu' rende 3000 ma costa
        # 2000: margine +1000, VAN cresce.
        s = _F["mh690_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Eventi 48"] < \
                s.loc[riga, "Eventi 60"] < \
                s.loc[riga, "Eventi 72"]
        for colonna in ("Eventi 48",
                        "Eventi 60",
                        "Eventi 72"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi variano davvero sulla
        # demo (prezzo senza tetto, eventi 48/60/72):
        # il margine resta positivo su tutta la
        # griglia, nessuna cella puo' essere 0,0
        # per regime degenere
        s = _F["mh690_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh690_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh690_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 30

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh690_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_a" in txt
        assert "ricavi_tot_eur_a" in txt
        assert "margine_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "costi_tot_eur_a" in txt
        assert "prezzo_gf_eur_mw_a" in txt
        assert "n_eventi_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh690_csv"](bc, self._ing())
        assert f"ricavi_tot_eur_a;{RTOT_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"capex_eur;{CAPEX_DEMO}" in txt
        assert "co2_evitata_t_a;105.0" in txt
        assert f"ricavi_gf_eur_a;{RG_DEMO}" in txt
        assert f"costi_tot_eur_a;{CTOT_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def690["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def690\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh690_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W690 (24/10/2026) - tab690' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh690_num", "mh690_nneg", "mh690_pos",
                     "mh690_int_pos", "mh690_int_nneg",
                     "mh690_tol", "mh690_frac",
                     "mh690_ricavi_gf",
                     "mh690_ricavi_eventi",
                     "mh690_ricavi_tot",
                     "mh690_costi_eventi",
                     "mh690_costi_tot",
                     "mh690_margine",
                     "mh690_energia_eventi",
                     "mh690_energia_inerziale",
                     "mh690_co2",
                     "mh690_capex",
                     "mh690_van", "mh690_tir",
                     "mh690_payback", "mh690_verdetto",
                     "_mh690_neutro", "mh690_calcola",
                     "mh690_sensitivita", "mh690_csv",
                     "mh690_demo", "demo_calcoli"):
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
        # l'apply (come w689_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w690_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE690) == 1

    def test_blocco_with_tab690(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab690:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE690

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st690_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 21, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st689_") for k in keys)
        assert not any(k.startswith("st688_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg690" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg690") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg690")
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
        assert "_vd690" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_gridforming_presente(self):
        src = _ui_src()
        assert "FORMA tensione e frequenza da zero" in src
        assert "disponibilità anche se non viene mai chiamato" in src
        assert "riserva di frequenza" in src
        assert "inerzia sintetica" in src
        assert "millisecondi" in src
        assert "breve durata" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi grid-forming" in src
        assert "Margine" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh690_csv" in src
        assert "grid_forming_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh690_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo grid-forming" in src
        assert "Eventi" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st690_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W690 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab690:")
        assert "mh690_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab690" in (_new_dir() / "w690_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w690_helpers.py", "w690_ui.py",
                   "w690_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab689" not in src
        assert "tab688" not in src
        assert "tab687" not in src

    def test_topic_gridforming_non_blackstart(self):
        # Topic corretto: il titolo e' grid-forming
        assert "Grid-forming" in TITLE690
        assert "black start" not in TITLE690.lower()
