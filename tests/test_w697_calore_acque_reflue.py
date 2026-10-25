"""Test tab697 "♨️💧 Calore dalle acque reflue: la fognatura scalda l'edificio?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
portata 20 L/s; salto termico 5 K; ore 4000
h/anno; COP 3,5; prezzo elettricita' 0,22
EUR/kWh; OPEX annuo 15000 EUR/anno;
rendimento caldaia 0,9; prezzo gas 0,09
EUR/kWh; fattore gas 0,20 kgCO2/kWh;
fattore elettricita' 0,35 kgCO2/kWh; costo
specifico PdC 600 EUR/kW erogato; costo rete
e scambiatore 150000 EUR; vita 20 anni; WACC
5 %; tolleranza 10 % del CAPEX.

- potenza_recuperata_kw = 418.6
- potenza_elettrica_kw = 167.44
- potenza_erogata_kw = 586.04
- energia_termica_mwh_a = 2344.16
- energia_elettrica_mwh_a = 669.76
- costo_baseline_eur_a = 234415.99999999997
- costo_pompa_eur_a = 162347.2
- risparmio_eur_a = 72068.79999999996
- co2_evitata_t_a = 286.5084444444445
- capex_eur = 501624.0
- van = 396512.54473444563
- tir = 13.153730756737836
- payback = 7
- verdetto = 'CONVIENTE'

Scomposizione: p_rec 20 x 4,186 x 5 = 418,6;
p_el 418,6 / (3,5 - 1) = 167,44; p_out
418,6 + 167,44 = 586,04; e_out 586,04 x
4000 / 1000 = 2344,16; e_el 167,44 x 4000 /
1000 = 669,76; c_base 2344,16 x 1000 / 0,9 x
0,09 = 234415,99999999997; c_hp 669,76 x 1000
x 0,22 + 15000 = 162347,2; risparmio
234415,99999999997 - 162347,2 =
72068,79999999996; co2 (2344,16 x 1000 / 0,9
x 0,20 - 669,76 x 1000 x 0,35) / 1000 =
286,5084444444445; capex 586,04 x 600 +
150000 = 501624,0; VAN -501624,0 +
72068,79999999996 x (1 - 1,05^-20) / 0,05 =
396512,54473444563; payback: cumulato anno 6
-69211,2, anno 7 +2857,6 -> 7.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w698_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w698_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w698_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w698_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w698_helpers.py: {missing}")
    return out


_F = _load("mh697_num", "mh697_nneg", "mh697_pos",
           "mh697_int_pos", "mh697_pct_range",
           "mh697_cop_valido", "mh697_rendimento_valido",
           "mh697_potenza_recuperata",
           "mh697_potenza_elettrica",
           "mh697_potenza_erogata",
           "mh697_energia_termica",
           "mh697_energia_elettrica",
           "mh697_costo_baseline", "mh697_costo_pompa",
           "mh697_risparmio", "mh697_co2_evitata",
           "mh697_capex", "mh697_crf", "mh697_van",
           "mh697_tir", "mh697_payback",
           "mh697_verdetto", "mh697_valida",
           "_mh697_neutro", "mh697_calcola",
           "mh697_sensitivita", "mh697_csv",
           "mh697_demo", "demo_calcoli")

TITLE697 = ("♨️💧 Calore dalle acque reflue: "
            "la fognatura scalda l'edificio?")

P_REC_DEMO = 418.6
P_EL_DEMO = 167.44
P_OUT_DEMO = 586.04
E_OUT_DEMO = 2344.16
E_EL_DEMO = 669.76
C_BASE_DEMO = 234415.99999999997
C_HP_DEMO = 162347.2
RISP_DEMO = 72068.79999999996
CO2_DEMO = 286.5084444444445
CAPEX_DEMO = 501624.0
VAN_DEMO = 396512.54473444563
TIR_DEMO = 13.153730756737836
PAYBACK_DEMO = 7
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.08024258719069129

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w698_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w698_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh697_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh697_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh697_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh697_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh697_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh697_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh697_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh697_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh697_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh697_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh697_int_pos"](20.0, "x") == 20

    def test_pct_range_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh697_pct_range"](-0.01, "x")

    def test_pct_range_rifiuta_cento(self):
        with pytest.raises(ValueError):
            _F["mh697_pct_range"](100.0, "x")

    def test_pct_range_accetta_zero(self):
        assert _F["mh697_pct_range"](0.0, "x") == 0.0

    def test_pct_range_accetta_99(self):
        assert _F["mh697_pct_range"](99.9, "x") == 99.9

    def test_cop_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh697_cop_valido"](1.0, "x")

    def test_cop_rifiuta_sotto_uno(self):
        with pytest.raises(ValueError):
            _F["mh697_cop_valido"](0.5, "x")

    def test_cop_accetta_sopra_uno(self):
        assert _F["mh697_cop_valido"](3.5, "x") == 3.5

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh697_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh697_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh697_rendimento_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh697_demo"]()
        d.update(kw)
        return _F["mh697_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_portata_zero_non_valida(self):
        v = self._val(portata_l_s=0.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_portata_negativa_non_valida(self):
        v = self._val(portata_l_s=-1.0)
        assert v["valido"] is False

    def test_salto_zero_non_valido(self):
        v = self._val(salto_termico_K=0.0)
        assert v["valido"] is False

    def test_ore_zero_non_valide(self):
        v = self._val(ore_anno=0.0)
        assert v["valido"] is False

    def test_cop_uno_non_valido(self):
        v = self._val(cop=1.0)
        assert v["valido"] is False

    def test_cop_sotto_uno_non_valido(self):
        v = self._val(cop=0.8)
        assert v["valido"] is False

    def test_prezzo_elettricita_zero_non_valido(self):
        v = self._val(prezzo_elettricita=0.0)
        assert v["valido"] is False

    def test_rendimento_zero_non_valido(self):
        v = self._val(rendimento_caldaia=0.0)
        assert v["valido"] is False

    def test_rendimento_sopra_uno_non_valido(self):
        v = self._val(rendimento_caldaia=1.2)
        assert v["valido"] is False

    def test_prezzo_gas_zero_non_valido(self):
        v = self._val(prezzo_gas=0.0)
        assert v["valido"] is False

    def test_prezzi_negativi_non_validi(self):
        for k in ("prezzo_elettricita", "prezzo_gas"):
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
        v = self._val(vita_anni=19.5)
        assert v["valido"] is False

    def test_costi_negativi_non_validi(self):
        for k in ("costo_specifico_pdc",
                  "costo_rete_scambiatore", "opex_annuo"):
            assert self._val(**{k: -1.0})["valido"] is False

    def test_nan_non_valido(self):
        v = self._val(cop=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(portata_l_s=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(portata_l_s=True)
        assert v["valido"] is False


class TestFisicaEconomia:
    def test_potenza_recuperata_demo(self):
        assert _F["mh697_potenza_recuperata"](
            20.0, 5.0) == pytest.approx(P_REC_DEMO, rel=REL)

    def test_potenza_recuperata_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh697_potenza_recuperata"](0.0, 5.0)
        with pytest.raises(ValueError):
            _F["mh697_potenza_recuperata"](20.0, 0.0)

    def test_potenza_elettrica_demo(self):
        assert _F["mh697_potenza_elettrica"](
            P_REC_DEMO, 3.5) == pytest.approx(P_EL_DEMO, rel=REL)

    def test_potenza_elettrica_rifiuta_cop_uno(self):
        with pytest.raises(ValueError):
            _F["mh697_potenza_elettrica"](P_REC_DEMO, 1.0)

    def test_potenza_erogata_demo(self):
        assert _F["mh697_potenza_erogata"](
            P_REC_DEMO, P_EL_DEMO) == pytest.approx(
            P_OUT_DEMO, rel=REL)

    def test_energia_termica_demo(self):
        assert _F["mh697_energia_termica"](
            P_OUT_DEMO, 4000.0) == pytest.approx(
            E_OUT_DEMO, rel=REL)

    def test_energia_elettrica_demo(self):
        assert _F["mh697_energia_elettrica"](
            P_EL_DEMO, 4000.0) == pytest.approx(
            E_EL_DEMO, rel=REL)

    def test_costo_baseline_demo(self):
        assert _F["mh697_costo_baseline"](
            E_OUT_DEMO, 0.9, 0.09) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_baseline_rifiuta_rendimento_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh697_costo_baseline"](E_OUT_DEMO, 1.2, 0.09)

    def test_costo_pompa_demo(self):
        assert _F["mh697_costo_pompa"](
            E_EL_DEMO, 0.22, 15000.0) == pytest.approx(
            C_HP_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh697_risparmio"](
            C_BASE_DEMO, C_HP_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh697_risparmio"](
            100000.0, 162347.2) == pytest.approx(
            -62347.2, rel=REL)

    def test_co2_demo(self):
        assert _F["mh697_co2_evitata"](
            E_OUT_DEMO, 0.9, 0.20,
            E_EL_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_puo_essere_negativa(self):
        assert _F["mh697_co2_evitata"](
            E_OUT_DEMO, 0.9, 0.05,
            E_EL_DEMO, 0.90) < 0.0

    def test_capex_demo(self):
        assert _F["mh697_capex"](
            P_OUT_DEMO, 600.0, 150000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_rete(self):
        assert _F["mh697_capex"](
            P_OUT_DEMO, 0.0, 150000.0) == 150000.0

    def test_crf_demo(self):
        assert _F["mh697_crf"](
            0.05, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh697_crf"](0.0, 20) == pytest.approx(
            0.05, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 20 / (1.05 ** 20 - 1.0)
        assert _F["mh697_crf"](0.05, 20) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh697_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-20)) / 0.05
        assert _F["mh697_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh697_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh697_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh697_van"](RISP_DEMO, -1.0, 0.05, 20)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh697_tir"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh697_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh697_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh697_tir"](0.0, RISP_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh697_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh697_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 21))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh697_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 6 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 7 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh697_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh697_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh697_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh697_payback"](
            50000000.0, RISP_DEMO, 20) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh697_payback"](0.0, RISP_DEMO, 20) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh697_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh697_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh697_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh697_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh697_verdetto"](
            -50162.4, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh697_verdetto"](
            -50162.5, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh697_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh697_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh697_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh697_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh697_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh697_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh697_demo"]()
        d.update(kw)
        return _F["mh697_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_recuperata_kw"] == pytest.approx(
            P_REC_DEMO, rel=REL)
        assert c["potenza_elettrica_kw"] == pytest.approx(
            P_EL_DEMO, rel=REL)
        assert c["potenza_erogata_kw"] == pytest.approx(
            P_OUT_DEMO, rel=REL)
        assert c["energia_termica_mwh_a"] == pytest.approx(
            E_OUT_DEMO, rel=REL)
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
        """mh697_calcola(**mh697_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (VAN ±1 EUR,
        TIR ±0,05 punti), chiave per chiave."""
        d = _F["mh697_demo"]()
        b = _F["mh697_calcola"](**d)
        coppie = [("potenza_recuperata_kw", P_REC_DEMO),
                  ("potenza_elettrica_kw", P_EL_DEMO),
                  ("potenza_erogata_kw", P_OUT_DEMO),
                  ("energia_termica_mwh_a", E_OUT_DEMO),
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
        d = _F["mh697_demo"]()
        assert d["portata_l_s"] == 20.0
        assert d["salto_termico_K"] == 5.0
        assert d["ore_anno"] == 4000.0
        assert d["cop"] == 3.5
        assert d["prezzo_elettricita"] == 0.22
        assert d["opex_annuo"] == 15000.0
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas"] == 0.09
        assert d["fattore_gas"] == 0.20
        assert d["fattore_elettricita"] == 0.35
        assert d["costo_specifico_pdc"] == 600.0
        assert d["costo_rete_scambiatore"] == 150000.0
        assert d["vita_anni"] == 20
        assert d["wacc_pct"] == 5.0
        assert d["tolleranza_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_recuperata_kw",
                       "potenza_elettrica_kw",
                       "potenza_erogata_kw",
                       "energia_termica_mwh_a",
                       "energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 7" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_portata_dimezzata(self):
        # Portata 10 L/s: p_rec 209,3; p_el 83,72;
        # p_out 293,02; e_out 1172,08; e_el 334,88;
        # c_base 117208,0; c_hp 88673,6; risparmio
        # 28534,4; capex 325812,0; VAN positivo
        n = self._bc(portata_l_s=10.0)
        assert n["valid"] is True
        assert n["potenza_recuperata_kw"] == pytest.approx(
            209.3, rel=REL)
        assert n["potenza_elettrica_kw"] == pytest.approx(
            83.72, rel=REL)
        assert n["potenza_erogata_kw"] == pytest.approx(
            293.02, rel=REL)
        assert n["energia_termica_mwh_a"] == pytest.approx(
            1172.08, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            28534.4, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            325812.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_cop_quattro(self):
        # COP 4,0: p_el 139,5333; p_out 558,1333;
        # e_out 2232,5333; e_el 558,1333; c_base
        # 223253,3333; c_hp 137789,3333; risparmio
        # 85464,0; capex 484880,0
        n = self._bc(cop=4.0)
        assert n["valid"] is True
        assert n["potenza_elettrica_kw"] == pytest.approx(
            139.53333333333333, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            85464.0, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            484880.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_portata_zero_neutro(self):
        n = self._bc(portata_l_s=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["errore"] != ""
        assert n["tir"] is None
        assert n["payback"] is None

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
        n = self._bc(vita_anni=19.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -501624 + 72068,8 / 1,05 < 0, oltre
        # tolleranza; payback mai
        n = self._bc(vita_anni=1)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

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
        n = self._bc(portata_l_s=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(portata_l_s=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risparmio_negativo_neutro(self):
        # Prezzo elettricita' 0,60: c_hp 416856,0
        # contro c_base 234416,0 -> risparmio < 0
        n = self._bc(prezzo_elettricita=0.60)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_specifico_pdc=0.0,
                     costo_rete_scambiatore=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh697_neutro"]()
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
        n = _F["_mh697_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "potenza_recuperata_kw",
                       "potenza_elettrica_kw",
                       "potenza_erogata_kw",
                       "energia_termica_mwh_a",
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
        assert len(b["df_tabella"]) == 23
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza recuperata (kW)" in voci
        assert "Energia termica annua (MWh/anno)" in voci
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
        return _F["mh697_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh697_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh697_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cop(self):
        # VAN cresce con il COP: meno elettricita'
        # assorbita e piu' risparmio, a parita'
        # di prezzo
        s = _F["mh697_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettricita(self):
        # VAN cala con il prezzo elettricita':
        # il costo della pompa sale, il risparmio
        # scende
        s = _F["mh697_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il risparmio resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh697_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh697_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh697_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh697_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_pompa_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "portata_l_s" in txt
        assert "potenza_recuperata_kw" in txt
        assert "co2_evitata_t_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh697_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"potenza_recuperata_kw;{P_REC_DEMO}" in txt
        assert f"energia_termica_mwh_a;{E_OUT_DEMO}" in txt
        assert "opex_annuo;15000.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def697["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def697\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh697_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh697_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh697_demo():")
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
        ui_keys = set(re.findall(r'_def697\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W698 (25/10/2026) - tab697' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh697_num", "mh697_nneg", "mh697_pos",
                     "mh697_int_pos", "mh697_pct_range",
                     "mh697_cop_valido",
                     "mh697_rendimento_valido",
                     "mh697_potenza_recuperata",
                     "mh697_potenza_elettrica",
                     "mh697_potenza_erogata",
                     "mh697_energia_termica",
                     "mh697_energia_elettrica",
                     "mh697_costo_baseline",
                     "mh697_costo_pompa",
                     "mh697_risparmio",
                     "mh697_co2_evitata",
                     "mh697_capex", "mh697_crf",
                     "mh697_van", "mh697_tir",
                     "mh697_payback", "mh697_verdetto",
                     "mh697_valida", "_mh697_neutro",
                     "mh697_calcola", "mh697_sensitivita",
                     "mh697_csv", "mh697_demo",
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
        ast.parse((_new_dir() / "w698_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE697) == 1

    def test_blocco_with_tab697(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab697:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE697

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st697_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st697_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone del brief
        (15 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st697_[a-z0-9_]+)"', _ui_src())
        attese = ["st697_portata", "st697_salto",
                  "st697_ore", "st697_cop",
                  "st697_prezzo_elettricita", "st697_opex",
                  "st697_rendimento", "st697_prezzo_gas",
                  "st697_fattore_gas",
                  "st697_fattore_elettricita",
                  "st697_costo_specifico", "st697_costo_rete",
                  "st697_vita", "st697_wacc_pct",
                  "st697_tolleranza_pct", "st697_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg697" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg697") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg697")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia termica annua (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd697" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_reflui_presente(self):
        src = _ui_src()
        assert "10" in src and "20 °C" in src
        assert "waste heat" in src.lower()
        assert "data center" in src.lower()
        assert "gestore della rete fognaria" in src
        assert "igienico-sanitaria" in src
        assert "scambiatore" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline caldaia a gas" in src
        assert "Pompa di calore" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh697_csv" in src
        assert "calore_acque_reflue_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh697_sensitivita" in src
        assert "Heatmap" in src
        assert "COP" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st697_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W698 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab697:")
        assert "mh697_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab697" in (_new_dir() / "w698_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w698_helpers.py", "w698_ui.py",
                   "w698_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab697"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "69" + "6"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w698_helpers.py", "w698_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_reflui_non_data_center(self):
        # Topic corretto: il titolo parla di
        # acque reflue / fognatura, non di
        # data center
        assert "reflue" in TITLE697.lower()
        assert "fognatura" in TITLE697.lower()
