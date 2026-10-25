"""Test tab695 "🔋🌊 Batterie a flusso redox: potenza ed energia separate pagano?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
potenza 1000 kW; durata 8 ore; DoD 1,0;
eta round-trip 0,75; cicli 300/anno; prezzo
acquisto 50 EUR/MWh; prezzo vendita 180
EUR/MWh; costo potenza 400 EUR/kW; costo
energia 300 EUR/kWh; CAPEX fisso 0 EUR;
OPEX fisso 20000 EUR/anno; vita 20 anni;
WACC 0,05 (5 %); tolleranza 0,10 (10 %
del CAPEX).

- energia_nominale_kwh = 8000.0
- energia_erogata_mwh_a = 2400.0
- energia_caricata_mwh_a = 3200.0
- capex_tot_eur = 2800000.0
- ricavi_eur_a = 432000.0
- costo_energia_eur_a = 160000.0
- margine_eur_a = 252000.0
- lcos_eur_mwh = 168.61635172247315
- van = 340477.0063200779
- tir = 6.394877709258562
- payback = 12
- verdetto = 'CONVIENTE'

Scomposizione: nominale 1000 x 8 = 8000;
erogata 1000 x 8 x 1,0 x 300 / 1000 =
2400; caricata 2400 / 0,75 = 3200; CAPEX
1000 x 400 + 8000 x 300 + 0 = 2800000;
ricavi 2400 x 180 = 432000; costo energia
3200 x 50 = 160000; margine 432000 -
160000 - 20000 = 252000; CRF 0,05 x
1,05^20 / (1,05^20 - 1) =
0,08024258719069129; LCOS (2800000 x
CRF + 20000 + 160000) / 2400 =
168,61635172247315; VAN -2800000 + 252000
x (1 - 1,05^-20) / 0,05 = 340477,0063200779.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w695_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w695_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w695_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w695_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w695_helpers.py: {missing}")
    return out


_F = _load("mh695_num", "mh695_nneg", "mh695_pos",
           "mh695_int_pos", "mh695_frac_util",
           "mh695_tol", "mh695_energia_nominale",
           "mh695_energia_erogata",
           "mh695_energia_caricata", "mh695_capex",
           "mh695_ricavi", "mh695_costo_energia",
           "mh695_margine", "mh695_crf", "mh695_lcos",
           "mh695_van", "mh695_tir",
           "mh695_payback", "mh695_verdetto",
           "_mh695_neutro", "mh695_calcola",
           "mh695_sensitivita", "mh695_csv",
           "mh695_demo", "demo_calcoli")

TITLE695 = ("🔋🌊 Batterie a flusso redox: "
            "potenza ed energia separate pagano?")

NOMINALE_DEMO = 8000.0
EROGATA_DEMO = 2400.0
CARICATA_DEMO = 3200.0
CAPEX_DEMO = 2800000.0
RICAVI_DEMO = 432000.0
COSTO_EN_DEMO = 160000.0
MARG_DEMO = 252000.0
LCOS_DEMO = 168.61635172247315
VAN_DEMO = 340477.0063200779
TIR_DEMO = 6.394877709258562
PAYBACK_DEMO = 12
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.08024258719069129

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w695_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w695_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh695_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh695_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh695_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh695_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh695_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh695_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh695_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh695_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh695_int_pos"](20.0, "x") == 20

    def test_frac_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_frac_util"](0.0, "x")

    def test_frac_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh695_frac_util"](1.01, "x")

    def test_frac_accetta_uno(self):
        assert _F["mh695_frac_util"](1.0, "x") == 1.0

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh695_tol"](-0.01, "x")

    def test_tol_accetta_zero_e_oltre_uno(self):
        # Spec tab695: tolleranza >= 0, senza tetto.
        assert _F["mh695_tol"](0.0, "x") == 0.0
        assert _F["mh695_tol"](1.5, "x") == 1.5


class TestFisicaEconomia:
    def test_energia_nominale_demo(self):
        assert _F["mh695_energia_nominale"](
            1000.0, 8.0) == pytest.approx(NOMINALE_DEMO,
                                          rel=REL)

    def test_energia_nominale_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_nominale"](0.0, 8.0)

    def test_energia_nominale_rifiuta_durata_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_nominale"](1000.0, 0.0)

    def test_energia_erogata_demo(self):
        assert _F["mh695_energia_erogata"](
            1000.0, 8.0, 1.0, 300.0) == pytest.approx(
            EROGATA_DEMO, rel=REL)

    def test_energia_erogata_dod_meta(self):
        assert _F["mh695_energia_erogata"](
            1000.0, 8.0, 0.5, 300.0) == pytest.approx(
            1200.0, rel=REL)

    def test_energia_erogata_cicli_zero(self):
        assert _F["mh695_energia_erogata"](
            1000.0, 8.0, 1.0, 0.0) == 0.0

    def test_energia_erogata_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_erogata"](0.0, 8.0, 1.0, 300.0)

    def test_energia_erogata_rifiuta_dod_zero(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_erogata"](1000.0, 8.0, 0.0, 300.0)

    def test_energia_erogata_rifiuta_dod_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_erogata"](1000.0, 8.0, 1.01, 300.0)

    def test_energia_erogata_rifiuta_cicli_negativi(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_erogata"](1000.0, 8.0, 1.0, -1.0)

    def test_energia_caricata_demo(self):
        assert _F["mh695_energia_caricata"](
            EROGATA_DEMO, 0.75) == pytest.approx(
            CARICATA_DEMO, rel=REL)

    def test_energia_caricata_eta_uno(self):
        assert _F["mh695_energia_caricata"](
            EROGATA_DEMO, 1.0) == EROGATA_DEMO

    def test_energia_caricata_none_se_eta_zero(self):
        assert _F["mh695_energia_caricata"](
            EROGATA_DEMO, 0.0) is None

    def test_energia_caricata_none_se_eta_negativa(self):
        assert _F["mh695_energia_caricata"](
            EROGATA_DEMO, -0.5) is None

    def test_energia_caricata_rifiuta_eta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh695_energia_caricata"](EROGATA_DEMO, 1.01)

    def test_capex_demo(self):
        assert _F["mh695_capex"](
            1000.0, 400.0, 8000.0, 300.0,
            0.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_solo_potenza(self):
        assert _F["mh695_capex"](
            1000.0, 400.0, 8000.0, 0.0, 0.0) == 400000.0

    def test_capex_solo_energia(self):
        assert _F["mh695_capex"](
            1000.0, 0.0, 8000.0, 300.0, 0.0) == 2400000.0

    def test_capex_zero(self):
        assert _F["mh695_capex"](0.0, 0.0, 0.0, 0.0, 0.0) == 0.0

    def test_capex_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh695_capex"](-1.0, 400.0, 8000.0, 300.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh695_capex"](1000.0, -1.0, 8000.0, 300.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh695_capex"](1000.0, 400.0, -1.0, 300.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh695_capex"](1000.0, 400.0, 8000.0, -1.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh695_capex"](1000.0, 400.0, 8000.0, 300.0, -1.0)

    def test_ricavi_demo(self):
        assert _F["mh695_ricavi"](
            EROGATA_DEMO, 180.0) == pytest.approx(
            RICAVI_DEMO, rel=REL)

    def test_ricavi_prezzo_zero(self):
        assert _F["mh695_ricavi"](EROGATA_DEMO, 0.0) == 0.0

    def test_costo_energia_demo(self):
        assert _F["mh695_costo_energia"](
            CARICATA_DEMO, 50.0) == pytest.approx(
            COSTO_EN_DEMO, rel=REL)

    def test_costo_energia_prezzo_zero(self):
        assert _F["mh695_costo_energia"](CARICATA_DEMO, 0.0) == 0.0

    def test_margine_demo(self):
        assert _F["mh695_margine"](
            RICAVI_DEMO, COSTO_EN_DEMO,
            20000.0) == pytest.approx(MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh695_margine"](100.0, 200.0, 50.0) == -150.0

    def test_crf_demo(self):
        assert _F["mh695_crf"](
            0.05, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh695_crf"](0.0, 20) == pytest.approx(
            0.05, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 20 / (1.05 ** 20 - 1.0)
        assert _F["mh695_crf"](0.05, 20) == pytest.approx(
            atteso, rel=1e-12)

    def test_lcos_demo(self):
        assert _F["mh695_lcos"](
            CAPEX_DEMO, CRF_DEMO, 20000.0,
            COSTO_EN_DEMO,
            EROGATA_DEMO) == pytest.approx(LCOS_DEMO,
                                           rel=REL)

    def test_lcos_none_se_erogata_zero(self):
        assert _F["mh695_lcos"](
            CAPEX_DEMO, CRF_DEMO, 20000.0,
            COSTO_EN_DEMO, 0.0) is None

    def test_lcos_none_se_erogata_negativa(self):
        assert _F["mh695_lcos"](
            CAPEX_DEMO, CRF_DEMO, 20000.0,
            COSTO_EN_DEMO, -1.0) is None


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh695_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARG_DEMO * (
            1.0 - 1.05 ** (-20)) / 0.05
        assert _F["mh695_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh695_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 20, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 20 == pytest.approx(
            2240000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh695_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh695_van"](MARG_DEMO, -1.0, 0.05, 20)

    def test_tir_demo(self):
        assert _F["mh695_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh695_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh695_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh695_tir"](0.0, MARG_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh695_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh695_tir"](CAPEX_DEMO, MARG_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 21))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh695_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARG_DEMO * 11 < 0.0
        assert -CAPEX_DEMO + MARG_DEMO * 12 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh695_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh695_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh695_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh695_payback"](
            50000000.0, MARG_DEMO, 20) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh695_payback"](0.0, MARG_DEMO, 20) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh695_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh695_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO, EROGATA_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        # Spec tab695: CONVIENTE se VAN >= 0.
        assert _F["mh695_verdetto"](
            0.0, CAPEX_DEMO, 0.10,
            MARG_DEMO, EROGATA_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh695_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO, EROGATA_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh695_verdetto"](
            -280000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO, EROGATA_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh695_verdetto"](
            -280001.0, CAPEX_DEMO, 0.10,
            MARG_DEMO, EROGATA_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh695_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            EROGATA_DEMO) == "NON_CALCOLABILE"
        assert _F["mh695_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0,
            EROGATA_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_erogata_zero(self):
        assert _F["mh695_verdetto"](
            1000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO, 0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh695_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO,
            EROGATA_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh695_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO,
            EROGATA_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh695_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO,
            EROGATA_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh695_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO, EROGATA_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh695_demo"]()
        d.update(kw)
        return _F["mh695_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["energia_nominale_kwh"] == pytest.approx(
            NOMINALE_DEMO, rel=REL)
        assert c["energia_erogata_mwh_a"] == pytest.approx(
            EROGATA_DEMO, rel=REL)
        assert c["energia_caricata_mwh_a"] == pytest.approx(
            CARICATA_DEMO, rel=REL)
        assert c["capex_tot_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["ricavi_eur_a"] == pytest.approx(
            RICAVI_DEMO, rel=REL)
        assert c["costo_energia_eur_a"] == pytest.approx(
            COSTO_EN_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["lcos_eur_mwh"] == pytest.approx(
            LCOS_DEMO, rel=REL)
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
        """mh695_calcola(**mh695_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh695_demo"]()
        b = _F["mh695_calcola"](**d)
        coppie = [("energia_nominale_kwh", NOMINALE_DEMO),
                  ("energia_erogata_mwh_a", EROGATA_DEMO),
                  ("energia_caricata_mwh_a", CARICATA_DEMO),
                  ("capex_tot_eur", CAPEX_DEMO),
                  ("ricavi_eur_a", RICAVI_DEMO),
                  ("costo_energia_eur_a", COSTO_EN_DEMO),
                  ("margine_eur_a", MARG_DEMO),
                  ("lcos_eur_mwh", LCOS_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh695_demo"]()
        assert d["potenza_kw"] == 1000.0
        assert d["durata_h"] == 8.0
        assert d["dod_frac"] == 1.0
        assert d["eta_rt_frac"] == 0.75
        assert d["cicli_annui"] == 300.0
        assert d["prezzo_acquisto_eur_mwh"] == 50.0
        assert d["prezzo_vendita_eur_mwh"] == 180.0
        assert d["costo_potenza_eur_kw"] == 400.0
        assert d["costo_energia_eur_kwh"] == 300.0
        assert d["capex_fisso_eur"] == 0.0
        assert d["opex_fisso_eur_a"] == 20000.0
        assert d["vita_anni"] == 20
        assert d["wacc_frac"] == 0.05
        assert d["toll_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_nominale_kwh",
                       "energia_erogata_mwh_a",
                       "energia_caricata_mwh_a",
                       "capex_tot_eur",
                       "ricavi_eur_a",
                       "costo_energia_eur_a",
                       "margine_eur_a",
                       "lcos_eur_mwh",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 12" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_eta_uno_calcolabile(self):
        # Eta 1,0: caricata 2400, costo energia
        # 120000, margine 292000
        n = self._bc(eta_rt_frac=1.0)
        assert n["valid"] is True
        assert n["energia_caricata_mwh_a"] == pytest.approx(
            2400.0, rel=REL)
        assert n["costo_energia_eur_a"] == pytest.approx(
            120000.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            292000.0, rel=REL)

    def test_dod_meta_calcolabile(self):
        # DoD 0,5: erogata 1200, caricata 1600,
        # ricavi 216000, costo energia 80000,
        # margine 116000
        n = self._bc(dod_frac=0.5)
        assert n["valid"] is True
        assert n["energia_erogata_mwh_a"] == pytest.approx(
            1200.0, rel=REL)
        assert n["energia_caricata_mwh_a"] == pytest.approx(
            1600.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            116000.0, rel=REL)

    def test_cicli_zero_neutro(self):
        n = self._bc(cicli_annui=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["energia_erogata_mwh_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_eta_zero_neutro(self):
        n = self._bc(eta_rt_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_oltre_uno_neutro(self):
        n = self._bc(eta_rt_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dod_zero_neutro(self):
        n = self._bc(dod_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dod_oltre_uno_neutro(self):
        n = self._bc(dod_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_vendita_zero_neutro(self):
        # Ricavi 0, margine -180000
        n = self._bc(prezzo_vendita_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_kw=-10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_durata_zero_neutro(self):
        n = self._bc(durata_h=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_durata_negativa_neutro(self):
        n = self._bc(durata_h=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costi_negativi_neutro(self):
        for k in ("costo_potenza_eur_kw",
                  "costo_energia_eur_kwh",
                  "capex_fisso_eur",
                  "opex_fisso_eur_a"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_prezzi_negativi_neutro(self):
        for k in ("prezzo_acquisto_eur_mwh",
                  "prezzo_vendita_eur_mwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=19.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -2800000 + 252000 / 1,05 < 0,
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
        n = self._bc(prezzo_vendita_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(potenza_kw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX fisso enorme: 432000 - 160000 -
        # 500000 < 0
        n = self._bc(opex_fisso_eur_a=500000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 20, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(costo_potenza_eur_kw=0.0,
                     costo_energia_eur_kwh=0.0,
                     capex_fisso_eur=0.0)
        assert n["capex_tot_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # Costo energia 350 EUR/kWh: CAPEX
        # 3200000, VAN circa -59522,99, entro
        # il 10 % di 3200000
        n = self._bc(costo_energia_eur_kwh=350.0)
        assert n["capex_tot_eur"] == pytest.approx(
            3200000.0, rel=REL)
        assert n["van"] == pytest.approx(
            -59522.993679922074, rel=1e-9)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 3200000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(costo_energia_eur_kwh=400.0)
        assert n["capex_tot_eur"] == pytest.approx(
            3600000.0, rel=REL)
        assert n["van"] == pytest.approx(
            -459522.9936799221, rel=1e-9)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh695_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh695_neutro"]()
        for chiave in ("valid",
                       "energia_nominale_kwh",
                       "energia_erogata_mwh_a",
                       "energia_caricata_mwh_a",
                       "capex_tot_eur",
                       "ricavi_eur_a",
                       "costo_energia_eur_a",
                       "margine_eur_a",
                       "lcos_eur_mwh",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["lcos_eur_mwh"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 20
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia nominale (kWh)" in voci
        assert "Energia erogata (MWh/anno)" in voci
        assert "Energia caricata (MWh/anno)" in voci
        assert "CAPEX totale (EUR)" in voci
        assert "Ricavi (EUR/anno)" in voci
        assert "Costo energia (EUR/anno)" in voci
        assert "Margine (EUR/anno)" in voci
        assert "LCOS (EUR/MWh)" in voci
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
        return _F["mh695_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh695_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.8", "x1.0", "x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh695_sensitivita"](self._ing())
        assert s.loc["x1.0", "x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_crescente_con_prezzo_vendita(self):
        # VAN cresce con il prezzo di vendita
        s = _F["mh695_sensitivita"](self._ing())
        for colonna in ("x0.8", "x1.0", "x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_crescente_con_cicli(self):
        # VAN cresce con i cicli annui
        s = _F["mh695_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "x0.8"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.2"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il margine resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh695_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh695_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh695_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 26

    def test_csv_contiene_verdetto_e_margine(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh695_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_eur_a" in txt
        assert "lcos_eur_mwh" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "ricavi_eur_a" in txt
        assert "prezzo_vendita_eur_mwh" in txt
        assert "potenza_kw" in txt
        assert "energia_erogata_mwh_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh695_csv"](bc, self._ing())
        assert f"ricavi_eur_a;{RICAVI_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"capex_tot_eur;{CAPEX_DEMO}" in txt
        assert f"energia_erogata_mwh_a;{EROGATA_DEMO}" in txt
        assert "opex_fisso_eur_a;20000.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def695["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def695\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh695_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh695_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh695_demo():")
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
        ui_keys = set(re.findall(r'_def695\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W695 (25/10/2026) - tab695' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh695_num", "mh695_nneg", "mh695_pos",
                     "mh695_int_pos", "mh695_frac_util",
                     "mh695_tol", "mh695_energia_nominale",
                     "mh695_energia_erogata",
                     "mh695_energia_caricata", "mh695_capex",
                     "mh695_ricavi", "mh695_costo_energia",
                     "mh695_margine", "mh695_crf", "mh695_lcos",
                     "mh695_van", "mh695_tir",
                     "mh695_payback", "mh695_verdetto",
                     "_mh695_neutro", "mh695_calcola",
                     "mh695_sensitivita", "mh695_csv",
                     "mh695_demo", "demo_calcoli"):
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
        ast.parse((_new_dir() / "w695_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE695) == 1

    def test_blocco_with_tab695(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab695:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE695

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st695_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st695_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg695" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg695") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg695")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia erogata (MWh/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src
        assert "LCOS (€/MWh)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd695" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_flusso_presente(self):
        src = _ui_src()
        assert "flusso" in src.lower()
        assert "serbatoi" in src
        assert "litio" in src.lower()
        assert "degrada" in src.lower()
        assert "disaccoppiate" in src.lower()
        assert "round-trip" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi" in src
        assert "Margine" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh695_csv" in src
        assert "batteria_flusso_redox_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh695_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo vendita" in src
        assert "Cicli" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st695_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W695 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab695:")
        assert "mh695_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab695" in (_new_dir() / "w695_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w695_helpers.py", "w695_ui.py",
                   "w695_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab695"}, tabs

    def test_topic_flusso_non_litio(self):
        # Topic corretto: il titolo e' flusso redox,
        # non litio generico
        assert "flusso redox" in TITLE695.lower()
        assert "separate" in TITLE695.lower()
