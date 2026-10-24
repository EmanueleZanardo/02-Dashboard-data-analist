"""Test tab681 "🔋⚡ Celle a combustibile: elettricità + calore senza combustione?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
cella a combustibile da 400 kW a 6000 ore
equivalenti/anno, rendimento elettrico 0,50 e
termico 0,35, rendimento di caldaia 0,90; prezzo
elettricita' 0,22 EUR/kWh, gas 0,09 EUR/kWh,
combustibile 0,09 EUR/kWh; OPEX 30 EUR/kW/anno;
CAPEX 3500 EUR/kW; fattori di emissione 0,35 /
0,20 / 0,20 kg/kWh; vita 15 anni; WACC 5,0 %;
tolleranza 10,0 % del CAPEX.

- e_el_kwh = 2400000.0
- f_kwh = 4800000.0
- q_th_kwh = 1680000.0
- c_base = 696000.0
- c_fc = 444000.0
- risparmio = 252000.0
- co2_evitata_t = 253.33333333333326
- capex_tot = 1400000.0
- crf = 0.09634228760924432
- van = 1215673.8256215109
- tir = 16.076407187550867 (in uscita: percentuale)
- payback = 6
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
    if (p / "w681_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w681_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w681_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w681_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w681_helpers.py: {missing}")
    return out


_F = _load("mh681_num", "mh681_nneg", "mh681_pos",
           "mh681_int_pos", "mh681_quota", "mh681_pct",
           "mh681_eta_el", "mh681_eta_th",
           "mh681_eta_caldaia", "mh681_e_el_kwh",
           "mh681_f_kwh", "mh681_q_th_kwh",
           "mh681_c_base", "mh681_c_fc",
           "mh681_risparmio", "mh681_co2_evitata_t",
           "mh681_capex_tot", "mh681_crf", "mh681_van",
           "mh681_tir", "mh681_payback",
           "mh681_verdetto", "_mh681_neutro",
           "mh681_calcola", "mh681_sensitivita",
           "mh681_csv", "mh681_demo", "demo_calcoli")

TITLE681 = ("🔋⚡ Celle a combustibile: elettricità + "
            "calore senza combustione?")

E_DEMO = 2400000.0
F_DEMO = 4800000.0
Q_DEMO = 1680000.0
CBASE_DEMO = 696000.0
CFC_DEMO = 444000.0
RISP_DEMO = 252000.0
CO2_DEMO = 253.33333333333326
CAPEX_DEMO = 1400000.0
CRF_DEMO = 0.09634228760924432
VAN_DEMO = 1215673.8256215109
TIR_DEMO = 16.076407187550867
PAYBACK_DEMO = 6
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w681_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w681_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh681_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh681_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh681_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh681_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh681_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh681_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh681_int_pos"](15.0, "x") == 15

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh681_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh681_quota"](-0.01, "x")

    def test_quota_accetta_estremi(self):
        assert _F["mh681_quota"](0.0, "x") == 0.0
        assert _F["mh681_quota"](1.0, "x") == 1.0

    def test_pct_rifiuta_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh681_pct"](100.01, "x")

    def test_pct_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh681_pct"](-0.01, "x")

    def test_pct_accetta_estremi(self):
        assert _F["mh681_pct"](0.0, "x") == 0.0
        assert _F["mh681_pct"](100.0, "x") == 100.0
        assert _F["mh681_pct"](5.0, "x") == 5.0

    def test_eta_el_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_el"](0.0, "x")

    def test_eta_el_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_el"](1.0, "x")

    def test_eta_el_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_el"](1.01, "x")

    def test_eta_el_accetta_valori_interni(self):
        assert _F["mh681_eta_el"](0.50, "x") == 0.50
        assert _F["mh681_eta_el"](0.99, "x") == 0.99

    def test_eta_th_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_th"](1.0, "x")

    def test_eta_th_accetta_zero(self):
        assert _F["mh681_eta_th"](0.0, "x") == 0.0
        assert _F["mh681_eta_th"](0.35, "x") == 0.35

    def test_eta_th_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_th"](-0.01, "x")

    def test_eta_caldaia_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_caldaia"](0.0, "x")

    def test_eta_caldaia_accetta_uno(self):
        assert _F["mh681_eta_caldaia"](1.0, "x") == 1.0

    def test_eta_caldaia_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh681_eta_caldaia"](1.01, "x")


class TestFisica:
    def test_e_el_demo(self):
        assert _F["mh681_e_el_kwh"](
            400.0, 6000.0) == pytest.approx(E_DEMO, rel=REL)

    def test_e_el_formula(self):
        assert _F["mh681_e_el_kwh"](
            100.0, 1000.0) == pytest.approx(100000.0,
                                            rel=1e-12)

    def test_e_el_zero_se_ore_zero(self):
        assert _F["mh681_e_el_kwh"](400.0, 0.0) == 0.0

    def test_e_el_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_e_el_kwh"](0.0, 6000.0)

    def test_e_el_rifiuta_ore_negative(self):
        with pytest.raises(ValueError):
            _F["mh681_e_el_kwh"](400.0, -1.0)

    def test_f_demo(self):
        assert _F["mh681_f_kwh"](
            E_DEMO, 0.50) == pytest.approx(F_DEMO, rel=REL)

    def test_f_formula(self):
        assert _F["mh681_f_kwh"](
            100000.0, 0.5) == pytest.approx(200000.0,
                                            rel=1e-12)

    def test_f_cresce_con_eta_el_basso(self):
        assert _F["mh681_f_kwh"](
            E_DEMO, 0.25) == pytest.approx(2.0 * F_DEMO,
                                           rel=REL)

    def test_f_eta_el_uno_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh681_f_kwh"](E_DEMO, 1.0)

    def test_f_rifiuta_elettricita_negativa(self):
        with pytest.raises(ValueError):
            _F["mh681_f_kwh"](-1.0, 0.50)

    def test_q_demo(self):
        assert _F["mh681_q_th_kwh"](
            F_DEMO, 0.35) == pytest.approx(Q_DEMO, rel=REL)

    def test_q_zero_se_eta_th_zero(self):
        assert _F["mh681_q_th_kwh"](F_DEMO, 0.0) == 0.0

    def test_q_rifiuta_eta_th_uno(self):
        with pytest.raises(ValueError):
            _F["mh681_q_th_kwh"](F_DEMO, 1.0)

    def test_q_rifiuta_combustibile_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_q_th_kwh"](-1.0, 0.35)

    def test_c_base_demo(self):
        assert _F["mh681_c_base"](
            E_DEMO, Q_DEMO, 0.90, 0.22,
            0.09) == pytest.approx(CBASE_DEMO, rel=REL)

    def test_c_base_scomposizione(self):
        # elettricita' 528000 + calore da caldaia
        # 1680000/0,90 x 0,09 = 168000
        assert E_DEMO * 0.22 == pytest.approx(528000.0,
                                              rel=REL)
        assert Q_DEMO / 0.90 * 0.09 == pytest.approx(
            168000.0, rel=REL)

    def test_c_base_diviso_per_eta_caldaia(self):
        # caldaia meno efficiente -> piu' gas per lo
        # stesso calore: costo evitato maggiore
        assert _F["mh681_c_base"](
            E_DEMO, Q_DEMO, 0.80, 0.22,
            0.09) > CBASE_DEMO

    def test_c_base_rifiuta_eta_caldaia_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_c_base"](E_DEMO, Q_DEMO, 0.0, 0.22,
                               0.09)

    def test_c_base_rifiuta_prezzi_negativi(self):
        with pytest.raises(ValueError):
            _F["mh681_c_base"](E_DEMO, Q_DEMO, 0.90, -0.01,
                               0.09)
        with pytest.raises(ValueError):
            _F["mh681_c_base"](E_DEMO, Q_DEMO, 0.90, 0.22,
                               -0.01)

    def test_c_fc_demo(self):
        assert _F["mh681_c_fc"](
            F_DEMO, 400.0, 0.09,
            30.0) == pytest.approx(CFC_DEMO, rel=REL)

    def test_c_fc_scomposizione(self):
        # combustibile 432000 + OPEX 12000
        assert F_DEMO * 0.09 == pytest.approx(432000.0,
                                              rel=REL)
        assert 400.0 * 30.0 == 12000.0

    def test_c_fc_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_c_fc"](F_DEMO, 0.0, 0.09, 30.0)

    def test_c_fc_rifiuta_opex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_c_fc"](F_DEMO, 400.0, 0.09, -0.01)

    def test_risparmio_demo(self):
        assert _F["mh681_risparmio"](
            CBASE_DEMO, CFC_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh681_risparmio"](100.0, 200.0) == -100.0

    def test_risparmio_zero_se_costi_uguali(self):
        assert _F["mh681_risparmio"](500.0, 500.0) == 0.0

    def test_co2_demo(self):
        assert _F["mh681_co2_evitata_t"](
            E_DEMO, Q_DEMO, 0.90, 0.35, 0.20, 0.20,
            F_DEMO) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_scomposizione(self):
        # rete 840 t + caldaia 373,33 t - combustibile
        # 960 t = 253,33 t
        assert E_DEMO * 0.35 / 1000.0 == pytest.approx(
            840.0, rel=REL)
        assert Q_DEMO / 0.90 * 0.20 / 1000.0 == pytest.approx(
            373.3333333333333, rel=REL)
        assert F_DEMO * 0.20 / 1000.0 == pytest.approx(
            960.0, rel=REL)

    def test_co2_negativa_se_combustibile_sporco(self):
        # f_comb alto: emissioni del combustibile
        # superano quanto evitato
        assert _F["mh681_co2_evitata_t"](
            E_DEMO, Q_DEMO, 0.90, 0.35, 0.20, 0.50,
            F_DEMO) < 0.0

    def test_co2_zero_se_tutto_zero(self):
        assert _F["mh681_co2_evitata_t"](
            0.0, 0.0, 0.90, 0.35, 0.20, 0.20,
            0.0) == 0.0

    def test_co2_rifiuta_fattori_negativi(self):
        with pytest.raises(ValueError):
            _F["mh681_co2_evitata_t"](
                E_DEMO, Q_DEMO, 0.90, -0.01, 0.20, 0.20,
                F_DEMO)

    def test_capex_demo(self):
        assert _F["mh681_capex_tot"](
            400.0, 3500.0) == pytest.approx(CAPEX_DEMO,
                                            rel=REL)

    def test_capex_zero_se_unitario_zero(self):
        assert _F["mh681_capex_tot"](400.0, 0.0) == 0.0

    def test_capex_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_capex_tot"](0.0, 3500.0)

    def test_capex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_capex_tot"](400.0, -1.0)

    def test_crf_demo(self):
        assert _F["mh681_crf"](
            5.0, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh681_crf"](
            0.0, 15) == pytest.approx(1.0 / 15.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_crf"](-0.01, 15)

    def test_crf_rifiuta_wacc_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh681_crf"](100.01, 15)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh681_crf"](5.0, 0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh681_van"](
            RISP_DEMO, CAPEX_DEMO, 5.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh681_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + RISP_DEMO * 15 == pytest.approx(
            2380000.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh681_van"](RISP_DEMO, -1.0, 5.0, 15)

    def test_tir_demo(self):
        assert _F["mh681_tir"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh681_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh681_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh681_tir"](0.0, RISP_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh681_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh681_payback"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh681_payback"](1000.0, 1000.0, 15) == 1
        assert _F["mh681_payback"](1000.0, 2000.0, 15) == 1

    def test_payback_none_mai(self):
        assert _F["mh681_payback"](CAPEX_DEMO, 1.0, 15) is None

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh681_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh681_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 10.0, RISP_DEMO,
            E_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh681_verdetto"](
            -100000.0, CAPEX_DEMO, 10.0, RISP_DEMO,
            E_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh681_verdetto"](
            -200000.0, CAPEX_DEMO, 10.0, RISP_DEMO,
            E_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh681_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, 0.0,
            E_DEMO) == "NON_CALCOLABILE"
        assert _F["mh681_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, -50.0,
            E_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_e_el_zero(self):
        assert _F["mh681_verdetto"](
            1000.0, CAPEX_DEMO, 10.0, RISP_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh681_verdetto"](
            0.0, 0.0, 10.0, RISP_DEMO,
            E_DEMO) == "CONVIENTE"
        assert _F["mh681_verdetto"](
            1000.0, 0.0, 10.0, RISP_DEMO,
            E_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh681_verdetto"](
            -1.0, 0.0, 10.0, RISP_DEMO,
            E_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh681_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 RISP_DEMO, E_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh681_verdetto"](100.0, CAPEX_DEMO, 100.01,
                                 RISP_DEMO, E_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh681_demo"]()
        d.update(kw)
        return _F["mh681_calcola"](**d)

    def test_potenza_zero_neutro(self):
        n = self._bc(p_el_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["e_el_kwh"] == 0.0
        assert n["risparmio"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(p_el_kw=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_ore_zero_neutro(self):
        n = self._bc(ore_eq=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["e_el_kwh"] == 0.0

    def test_ore_negative_neutro(self):
        n = self._bc(ore_eq=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_el_zero_neutro(self):
        n = self._bc(eta_el=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_el_uno_neutro(self):
        n = self._bc(eta_el=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_el_tende_a_uno_calcolabile(self):
        # eta_el 0,99 con eta_th 0: quasi tutto il
        # combustibile diventa elettricita'
        n = self._bc(eta_el=0.99, eta_th=0.0)
        assert n["valid"] is True
        assert n["f_kwh"] == pytest.approx(
            E_DEMO / 0.99, rel=REL)
        assert n["q_th_kwh"] == 0.0

    def test_eta_th_uno_neutro(self):
        n = self._bc(eta_th=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_th_negativa_neutro(self):
        n = self._bc(eta_th=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_somma_rendimenti_oltre_uno_neutro(self):
        n = self._bc(eta_el=0.70, eta_th=0.35)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_somma_rendimenti_uguale_uno_calcolabile(self):
        # 0,65 + 0,35 = 1,00: tutto l'ingresso esce
        # come elettricita' + calore
        n = self._bc(eta_el=0.65, eta_th=0.35)
        assert n["valid"] is True

    def test_eta_caldaia_zero_neutro(self):
        n = self._bc(eta_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_caldaia_oltre_uno_neutro(self):
        n = self._bc(eta_caldaia=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_negativi_neutro(self):
        for k in ("p_el", "p_gas", "p_comb"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_opex_negativo_neutro(self):
        n = self._bc(opex_eur_kw_a=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_eur_kw=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fattori_negativi_neutro(self):
        for k in ("f_el", "f_gas", "f_comb"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
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
        n = self._bc(p_el=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(p_el_kw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risparmio_non_positivo_neutro(self):
        # combustibile caro: costo cella supera il
        # costo evitato -> risparmio <= 0
        n = self._bc(p_comb=0.30)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -1400000 + 252000 x 15 =
        # 2380000 -> CONVIENTE
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(2380000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_kw=0.0)
        assert n["capex_tot"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"

    def test_solo_elettricita_calcolabile(self):
        # eta_th 0: nessun calore, solo elettricita'
        # evitata; risparmio resta positivo
        n = self._bc(eta_th=0.0)
        assert n["valid"] is True
        assert n["q_th_kwh"] == 0.0
        assert n["c_base"] == pytest.approx(
            E_DEMO * 0.22, rel=REL)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh681_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh681_neutro"]()
        for chiave in ("valid", "e_el_kwh", "f_kwh",
                       "q_th_kwh", "c_base", "c_fc",
                       "risparmio", "co2_evitata_t",
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
        assert "Elettricita' prodotta (kWh/anno)" in voci
        assert "Calore recuperato (kWh/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
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
        return _F["mh681_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh681_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Ore x0.8",
                                   "Ore x1.0",
                                   "Ore x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh681_sensitivita"](self._ing())
        assert s.loc["x1.0", "Ore x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh681_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Ore x1.0"]
        assert s.loc["x1.2", "Ore x1.2"] > centro
        assert s.loc["x0.8", "Ore x0.8"] < centro
        assert s.loc["x1.0", "Ore x1.2"] > centro
        assert s.loc["x1.0", "Ore x0.8"] < centro
        assert s.loc["x1.2", "Ore x1.0"] > centro
        assert s.loc["x0.8", "Ore x1.0"] < centro

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh681_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh681_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "e_el_kwh_anno" in txt
        assert "risparmio_eur_anno" in txt
        assert "eta_el_frazione" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh681_csv"](bc, self._ing())
        assert f"e_el_kwh_anno;{E_DEMO}" in txt
        assert f"risparmio_eur_anno;{RISP_DEMO}" in txt
        assert f"c_base_eur_anno;{CBASE_DEMO}" in txt
        assert f"f_kwh_anno;{F_DEMO}" in txt
        assert f"q_th_kwh_anno;{Q_DEMO}" in txt


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["e_el_kwh"] == pytest.approx(E_DEMO, rel=REL)
        assert c["f_kwh"] == pytest.approx(F_DEMO, rel=REL)
        assert c["q_th_kwh"] == pytest.approx(Q_DEMO, rel=REL)
        assert c["c_base"] == pytest.approx(CBASE_DEMO,
                                            rel=REL)
        assert c["c_fc"] == pytest.approx(CFC_DEMO, rel=REL)
        assert c["risparmio"] == pytest.approx(RISP_DEMO,
                                               rel=REL)
        assert c["co2_evitata_t"] == pytest.approx(
            CO2_DEMO, rel=REL)
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
            "co2_evitata_t"] == _F["demo_calcoli"]()[
            "co2_evitata_t"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh681_calcola(**mh681_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh681_demo"]()
        b = _F["mh681_calcola"](**d)
        coppie = [("e_el_kwh", E_DEMO),
                  ("f_kwh", F_DEMO),
                  ("q_th_kwh", Q_DEMO),
                  ("c_base", CBASE_DEMO),
                  ("c_fc", CFC_DEMO),
                  ("risparmio", RISP_DEMO),
                  ("co2_evitata_t", CO2_DEMO),
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
        d = _F["mh681_demo"]()
        assert d["p_el_kw"] == 400.0
        assert d["ore_eq"] == 6000.0
        assert d["eta_el"] == 0.50
        assert d["eta_th"] == 0.35
        assert d["eta_caldaia"] == 0.90
        assert d["p_el"] == 0.22
        assert d["p_gas"] == 0.09
        assert d["p_comb"] == 0.09
        assert d["opex_eur_kw_a"] == 30.0
        assert d["capex_eur_kw"] == 3500.0
        assert d["f_el"] == 0.35
        assert d["f_gas"] == 0.20
        assert d["f_comb"] == 0.20
        assert d["vita_anni"] == 15
        assert d["wacc_pct"] == 5.0
        assert d["toll_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_el_kwh", "f_kwh", "q_th_kwh",
                       "c_base", "c_fc", "risparmio",
                       "co2_evitata_t", "capex_tot",
                       "crf", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 6" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def681["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def681\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh681_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W681 (24/10/2026) - tab681' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh681_num", "mh681_nneg", "mh681_pos",
                     "mh681_int_pos", "mh681_quota",
                     "mh681_pct", "mh681_eta_el",
                     "mh681_eta_th", "mh681_eta_caldaia",
                     "mh681_e_el_kwh", "mh681_f_kwh",
                     "mh681_q_th_kwh", "mh681_c_base",
                     "mh681_c_fc", "mh681_risparmio",
                     "mh681_co2_evitata_t",
                     "mh681_capex_tot", "mh681_crf",
                     "mh681_van", "mh681_tir",
                     "mh681_payback", "mh681_verdetto",
                     "_mh681_neutro", "mh681_calcola",
                     "mh681_sensitivita", "mh681_csv",
                     "mh681_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE681) == 1

    def test_blocco_with_tab681(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab681:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st681_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 21, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st680_") for k in keys)
        assert not any(k.startswith("st679_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg681" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg681") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg681")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Elettricità prodotta (kWh/anno)" in src
        assert "Risparmio (€/anno)" in src
        assert "VAN (€)" in src
        assert "TIR / Payback" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd681" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_elettricita_calore_presente(self):
        src = _ui_src()
        assert "Elettricità + calore vs sola elettricità" in src
        assert "calore da caldaia" in src

    def test_nota_onesta_idrogeno_verde_presente(self):
        src = _ui_src()
        assert "idrogeno verde" in src.lower()
        assert "f_comb" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo evitato" in src
        assert "Risparmio cella" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src or "mh681_csv" in src
        assert "cella_combustibile_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh681_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo elettricità" in src
        assert "Ore equivalenti" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st681_show_flussi" in src
        assert "st.checkbox" in src

    def test_nessuna_altra_tecnologia_nominata(self):
        # Il frammento parla solo di celle a
        # combustibile: niente altre tecnologie di
        # accumulo/generazione come feature.
        for fn in ("w681_helpers.py", "w681_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            basso = src.lower()
            for parola in ("gravitazionale", "laes",
                           "aria liquida", "volano",
                           "vrfb", "vanadio"):
                assert parola not in basso, (fn, parola)


class TestApplyContract:
    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE681

    def test_ancora_helper_presente(self):
        assert "# W681 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab681:")
        assert "mh681_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab681" in (_new_dir() / "w681_test.py")\
            .read_text(encoding="utf-8")


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w681_helpers.py", "w681_ui.py",
                   "w681_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
