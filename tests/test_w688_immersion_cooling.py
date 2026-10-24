"""Test tab688 "💧🖥️ Immersion cooling: il raffreddamento a liquido del data center paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
potenza IT 500 kW; PUE base 1,50; PUE immersione
1,10; prezzo elettricita' 0,12 EUR/kWh; WUE base
1,5 L/kWh_IT; WUE immersione 0,1 L/kWh_IT; prezzo
acqua 1,50 EUR/m3; OPEX extra 25000 EUR/anno;
retrofit 500 EUR/kW; fluido iniziale 30000 EUR;
vita 10 anni; WACC 0,05 (5 %); tolleranza 0,10
(10 % del CAPEX); fattore CO2 0,35 kg/kWh.

- e_it_mwh = 4380.0
- e_base_mwh = 6570.0
- e_imm_mwh = 4818.0
- risparmio_el_mwh = 1752.0
- acqua_base_m3 = 6570.0
- acqua_imm_m3 = 438.0
- acqua_risp_m3 = 6132.0
- risparmio_lordo_eur_a = 219438.0
- opex_extra_eur_a = 25000.0
- risparmio_netto_eur_a = 194438.0
- capex_eur = 280000.0
- co2_evitata_t_a = 613.1999999999999
  (1752 x 0,35 in virgola mobile; arrotondato 613.2 t)
- van = 1221398.6961608375
- tir = 69.0784450671365 (in uscita: percentuale)
- payback = 2
- verdetto = 'CONVIENTE'

NOTA CO2: il brief scrive "risparmio x fattore /
1000" ma il suo atteso a mano e' 613.2 t: con
l'energia in MWh la conversione MWh -> kWh
(x1000) e kg -> t (/1000) si cancellano, quindi
t = MWh x kg/kWh = 1752 x 0,35 = 613.2 t. La
forma "/ 1000" darebbe 0,6132 t, incompatibile
con l'atteso e con la fisica.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w688_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w688_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w688_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w688_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w688_helpers.py: {missing}")
    return out


_F = _load("mh688_num", "mh688_nneg", "mh688_pos",
           "mh688_int_pos", "mh688_tol",
           "mh688_e_it", "mh688_energia",
           "mh688_risparmio_el", "mh688_acqua",
           "mh688_acqua_risp", "mh688_lordo",
           "mh688_risparmio_netto", "mh688_capex",
           "mh688_co2_evitata",
           "mh688_van", "mh688_tir",
           "mh688_payback", "mh688_verdetto",
           "_mh688_neutro", "mh688_calcola",
           "mh688_sensitivita", "mh688_csv",
           "mh688_demo", "demo_calcoli")

TITLE688 = ("💧🖥️ Immersion cooling: il raffreddamento "
            "a liquido del data center paga?")

EIT_DEMO = 4380.0
EBASE_DEMO = 6570.0
EIMM_DEMO = 4818.0
REL_DEMO = 1752.0
ACQB_DEMO = 6570.0
ACQI_DEMO = 438.0
ACQR_DEMO = 6132.0
LORDO_DEMO = 219438.0
OPEX_DEMO = 25000.0
NETTO_DEMO = 194438.0
CAPEX_DEMO = 280000.0
CO2_DEMO = 613.2
VAN_DEMO = 1221398.6961608375
TIR_DEMO = 69.0784450671365
PAYBACK_DEMO = 2
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w688_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w688_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh688_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh688_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh688_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh688_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh688_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh688_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh688_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh688_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh688_int_pos"](10.0, "x") == 10

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh688_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh688_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh688_tol"](0.0, "x") == 0.0
        assert _F["mh688_tol"](1.0, "x") == 1.0


class TestFisica:
    def test_e_it_demo(self):
        assert _F["mh688_e_it"](500.0) == pytest.approx(
            EIT_DEMO, rel=REL)

    def test_e_it_formula(self):
        assert _F["mh688_e_it"](1000.0) == pytest.approx(
            8760.0, rel=1e-12)

    def test_e_it_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh688_e_it"](0.0)

    def test_energia_base_demo(self):
        assert _F["mh688_energia"](
            500.0, 1.50) == pytest.approx(EBASE_DEMO, rel=REL)

    def test_energia_imm_demo(self):
        assert _F["mh688_energia"](
            500.0, 1.10) == pytest.approx(EIMM_DEMO, rel=REL)

    def test_energia_rifiuta_pue_zero(self):
        with pytest.raises(ValueError):
            _F["mh688_energia"](500.0, 0.0)

    def test_energia_rifiuta_pue_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_energia"](500.0, -1.10)

    def test_risparmio_el_demo(self):
        assert _F["mh688_risparmio_el"](
            EBASE_DEMO, EIMM_DEMO) == pytest.approx(
            REL_DEMO, rel=REL)

    def test_risparmio_el_negativo_se_pue_imm_maggiore(self):
        # pue_imm 1,60 > pue_base 1,50 -> -438 MWh
        assert _F["mh688_risparmio_el"](
            6570.0, 7008.0) == pytest.approx(-438.0, rel=1e-12)

    def test_risparmio_el_zero_se_pue_uguali(self):
        assert _F["mh688_risparmio_el"](
            6570.0, 6570.0) == 0.0

    def test_acqua_base_demo(self):
        assert _F["mh688_acqua"](
            EIT_DEMO, 1.5) == pytest.approx(ACQB_DEMO, rel=REL)

    def test_acqua_imm_demo(self):
        assert _F["mh688_acqua"](
            EIT_DEMO, 0.1) == pytest.approx(ACQI_DEMO, rel=REL)

    def test_acqua_formula(self):
        # e_it x 1000 x wue / 1000 = e_it x wue
        assert _F["mh688_acqua"](
            1000.0, 2.0) == pytest.approx(2000.0, rel=1e-12)

    def test_acqua_zero_se_wue_zero(self):
        assert _F["mh688_acqua"](EIT_DEMO, 0.0) == 0.0

    def test_acqua_rifiuta_wue_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_acqua"](EIT_DEMO, -0.1)

    def test_acqua_risp_demo(self):
        assert _F["mh688_acqua_risp"](
            ACQB_DEMO, ACQI_DEMO) == pytest.approx(
            ACQR_DEMO, rel=REL)

    def test_acqua_risp_negativa_se_wue_imm_maggiore(self):
        assert _F["mh688_acqua_risp"](
            438.0, 6570.0) == pytest.approx(-6132.0, rel=1e-12)

    def test_lordo_demo(self):
        assert _F["mh688_lordo"](
            REL_DEMO, 0.12, ACQR_DEMO,
            1.50) == pytest.approx(LORDO_DEMO, rel=REL)

    def test_lordo_scomposizione(self):
        # 1752 x 1000 x 0,12 = 210240; 6132 x 1,50 = 9198
        assert 1752.0 * 1000.0 * 0.12 == pytest.approx(
            210240.0, rel=1e-12)
        assert 6132.0 * 1.50 == pytest.approx(9198.0, rel=1e-12)

    def test_lordo_rifiuta_prezzi_negativi(self):
        with pytest.raises(ValueError):
            _F["mh688_lordo"](REL_DEMO, -0.01, ACQR_DEMO, 1.50)
        with pytest.raises(ValueError):
            _F["mh688_lordo"](REL_DEMO, 0.12, ACQR_DEMO, -0.01)

    def test_netto_demo(self):
        assert _F["mh688_risparmio_netto"](
            LORDO_DEMO, OPEX_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh688_risparmio_netto"](
            100.0, 200.0) == -100.0

    def test_netto_rifiuta_opex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_risparmio_netto"](LORDO_DEMO, -1.0)

    def test_capex_demo(self):
        assert _F["mh688_capex"](
            500.0, 500.0, 30000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh688_capex"](500.0, 0.0, 0.0) == 0.0

    def test_capex_rifiuta_costi_negativi(self):
        with pytest.raises(ValueError):
            _F["mh688_capex"](500.0, -1.0, 30000.0)
        with pytest.raises(ValueError):
            _F["mh688_capex"](500.0, 500.0, -1.0)

    def test_co2_demo(self):
        assert _F["mh688_co2_evitata"](
            REL_DEMO, 0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_formula_mwh(self):
        # 1000 MWh x 0,35 kg/kWh = 350 t
        assert _F["mh688_co2_evitata"](
            1000.0, 0.35) == pytest.approx(350.0, rel=1e-12)

    def test_co2_zero_se_risparmio_non_positivo(self):
        assert _F["mh688_co2_evitata"](0.0, 0.35) == 0.0
        assert _F["mh688_co2_evitata"](-438.0, 0.35) == 0.0

    def test_co2_zero_se_fattore_zero(self):
        assert _F["mh688_co2_evitata"](REL_DEMO, 0.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_co2_evitata"](REL_DEMO, -0.01)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh688_van"](
            NETTO_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + NETTO_DEMO * (
            1.0 - 1.05 ** (-10)) / 0.05
        assert _F["mh688_van"](
            NETTO_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh688_van"](
            NETTO_DEMO, CAPEX_DEMO, 0.0,
            10) == pytest.approx(
            -CAPEX_DEMO + NETTO_DEMO * 10, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + NETTO_DEMO * 10 == pytest.approx(
            1664380.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_van"](NETTO_DEMO, CAPEX_DEMO, -0.01, 10)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh688_van"](NETTO_DEMO, -1.0, 0.05, 10)

    def test_tir_demo(self):
        assert _F["mh688_tir"](
            CAPEX_DEMO, NETTO_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh688_tir"](CAPEX_DEMO, 0.0, 10) is None
        assert _F["mh688_tir"](CAPEX_DEMO, -100.0, 10) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh688_tir"](0.0, NETTO_DEMO, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh688_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh688_tir"](CAPEX_DEMO, NETTO_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            NETTO_DEMO / (1.0 + tir) ** i
            for i in range(1, 11))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_payback_demo(self):
        assert _F["mh688_payback"](
            CAPEX_DEMO, NETTO_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        # anno 1: -280000 + 194438 < 0; anno 2 >= 0
        assert -CAPEX_DEMO + NETTO_DEMO * 1 < 0.0
        assert -CAPEX_DEMO + NETTO_DEMO * 2 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh688_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh688_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh688_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        # -2000000 + 194438 x 10 < 0 -> None
        assert _F["mh688_payback"](
            2000000.0, NETTO_DEMO, 10) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh688_payback"](0.0, NETTO_DEMO, 10) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh688_payback"](CAPEX_DEMO, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh688_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh688_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 28000 = 10 % di 280000 -> MARGINALE
        assert _F["mh688_verdetto"](
            -28000.0, CAPEX_DEMO, 0.10,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh688_verdetto"](
            -28001.0, CAPEX_DEMO, 0.10,
            NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh688_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh688_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh688_verdetto"](
            0.0, 0.0, 0.10, NETTO_DEMO) == "CONVIENTE"
        assert _F["mh688_verdetto"](
            1000.0, 0.0, 0.10, NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh688_verdetto"](
            -1.0, 0.0, 0.10, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh688_verdetto"](
            -1.0, 0.0, 0.10, NETTO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh688_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 NETTO_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh688_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 NETTO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh688_demo"]()
        d.update(kw)
        return _F["mh688_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["e_it_mwh"] == pytest.approx(EIT_DEMO, rel=REL)
        assert c["e_base_mwh"] == pytest.approx(
            EBASE_DEMO, rel=REL)
        assert c["e_imm_mwh"] == pytest.approx(
            EIMM_DEMO, rel=REL)
        assert c["risparmio_el_mwh"] == pytest.approx(
            REL_DEMO, rel=REL)
        assert c["acqua_base_m3"] == pytest.approx(
            ACQB_DEMO, rel=REL)
        assert c["acqua_imm_m3"] == pytest.approx(
            ACQI_DEMO, rel=REL)
        assert c["acqua_risp_m3"] == pytest.approx(
            ACQR_DEMO, rel=REL)
        assert c["risparmio_lordo_eur_a"] == pytest.approx(
            LORDO_DEMO, rel=REL)
        assert c["risparmio_netto_eur_a"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
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
        """mh688_calcola(**mh688_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh688_demo"]()
        b = _F["mh688_calcola"](**d)
        coppie = [("e_it_mwh", EIT_DEMO),
                  ("e_base_mwh", EBASE_DEMO),
                  ("e_imm_mwh", EIMM_DEMO),
                  ("risparmio_el_mwh", REL_DEMO),
                  ("acqua_base_m3", ACQB_DEMO),
                  ("acqua_imm_m3", ACQI_DEMO),
                  ("acqua_risp_m3", ACQR_DEMO),
                  ("risparmio_lordo_eur_a", LORDO_DEMO),
                  ("risparmio_netto_eur_a", NETTO_DEMO),
                  ("capex_eur", CAPEX_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh688_demo"]()
        assert d["pot_it_kw"] == 500.0
        assert d["pue_base"] == 1.50
        assert d["pue_imm"] == 1.10
        assert d["prezzo_el_eur_kwh"] == 0.12
        assert d["wue_base_l_kwh"] == 1.5
        assert d["wue_imm_l_kwh"] == 0.1
        assert d["prezzo_acqua_eur_m3"] == 1.50
        assert d["opex_extra_eur_a"] == 25000.0
        assert d["costo_retrofit_eur_kw"] == 500.0
        assert d["costo_fluido_iniziale_eur"] == 30000.0
        assert d["vita_anni"] == 10
        assert d["wacc"] == 0.05
        assert d["tol_frac"] == 0.10
        assert d["fattore_co2_kg_kwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_it_mwh", "e_base_mwh",
                       "e_imm_mwh", "risparmio_el_mwh",
                       "acqua_base_m3", "acqua_imm_m3",
                       "acqua_risp_m3",
                       "risparmio_lordo_eur_a",
                       "risparmio_netto_eur_a",
                       "capex_eur", "co2_evitata_t_a",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 2" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_pot_it_zero_neutro(self):
        n = self._bc(pot_it_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["e_it_mwh"] == 0.0
        assert n["risparmio_netto_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_pue_zero_neutro(self):
        for k in ("pue_base", "pue_imm"):
            n = self._bc(**{k: 0.0})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_pue_negativo_neutro(self):
        n = self._bc(pue_imm=-1.10)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_pue_imm_uguale_base_netto_positivo_co2_zero(self):
        # rel = 0, acqua risp 6132 x 10 = 61320,
        # OPEX 0 -> netto 61320 > 0, ma CO2 = 0
        n = self._bc(pue_imm=1.50,
                     prezzo_acqua_eur_m3=10.0,
                     opex_extra_eur_a=0.0)
        assert n["valid"] is True
        assert n["risparmio_el_mwh"] == 0.0
        assert n["co2_evitata_t_a"] == 0.0
        assert n["risparmio_netto_eur_a"] > 0.0

    def test_pue_imm_maggiore_base_netto_positivo_co2_zero(self):
        # rel = -438 MWh, lordo -52560 + 61320 = 8760
        n = self._bc(pue_imm=1.60,
                     prezzo_acqua_eur_m3=10.0,
                     opex_extra_eur_a=0.0)
        assert n["valid"] is True
        assert n["risparmio_el_mwh"] == pytest.approx(
            -438.0, rel=REL)
        assert n["co2_evitata_t_a"] == 0.0

    def test_pue_imm_maggiore_base_demo_neutro(self):
        # con i prezzi demo il netto resta negativo
        n = self._bc(pue_imm=1.60)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_wue_negativi_neutro(self):
        for k in ("prezzo_el_eur_kwh", "wue_base_l_kwh",
                  "wue_imm_l_kwh", "prezzo_acqua_eur_m3",
                  "fattore_co2_kg_kwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_costi_negativi_neutro(self):
        for k in ("opex_extra_eur_a",
                  "costo_retrofit_eur_kw",
                  "costo_fluido_iniziale_eur"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=9.5)
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
        n = self._bc(prezzo_el_eur_kwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_netto_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(pot_it_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(pot_it_kw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risparmio_negativo_neutro(self):
        # OPEX extra enorme: lordo 219438 - 500000 < 0
        n = self._bc(opex_extra_eur_a=500000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_netto_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -280000 + 194438 x 10
        n = self._bc(wacc=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + NETTO_DEMO * 10, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(costo_retrofit_eur_kw=0.0,
                     costo_fluido_iniziale_eur=0.0)
        assert n["capex_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 1510000: VAN = -1510000 + 1501398,70
        # = circa -8601, entro il 10 % di 1510000
        n = self._bc(costo_fluido_iniziale_eur=1260000.0)
        assert n["capex_eur"] == pytest.approx(
            1510000.0, rel=REL)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 1510000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(costo_fluido_iniziale_eur=3000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh688_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh688_neutro"]()
        for chiave in ("valid", "e_it_mwh",
                       "e_base_mwh", "e_imm_mwh",
                       "risparmio_el_mwh",
                       "acqua_base_m3", "acqua_imm_m3",
                       "acqua_risp_m3",
                       "risparmio_lordo_eur_a",
                       "opex_extra_eur_a",
                       "risparmio_netto_eur_a",
                       "capex_eur", "co2_evitata_t_a",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 13
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia IT (MWh/anno)" in voci
        assert "Energia base (MWh/anno)" in voci
        assert "Energia immersione (MWh/anno)" in voci
        assert "Risparmio elettrico (MWh/anno)" in voci
        assert "Acqua base (m3/anno)" in voci
        assert "Acqua risparmiata (m3/anno)" in voci
        assert "Risparmio lordo (EUR/anno)" in voci
        assert "Risparmio netto (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + NETTO_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh688_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh688_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["PUE 1.045",
                                   "PUE 1.100",
                                   "PUE 1.155"]
        assert list(s.index) == ["x0.7", "x1.0", "x1.3"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh688_sensitivita"](self._ing())
        assert s.loc["x1.0", "PUE 1.100"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh688_sensitivita"](self._ing())
        centro = s.loc["x1.0", "PUE 1.100"]
        assert s.loc["x0.7", "PUE 1.155"] < centro
        assert s.loc["x1.0", "PUE 1.155"] < centro
        assert s.loc["x1.3", "PUE 1.100"] > centro
        assert s.loc["x0.7", "PUE 1.100"] < centro
        assert s.loc["x1.3", "PUE 1.045"] > centro

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi variano davvero sulla
        # demo (prezzo senza tetto, PUE assoluti
        # 1.045/1.100/1.155 sotto il PUE base 1,50):
        # nessuna cella puo' essere 0,0 per regime
        # degenere
        s = _F["mh688_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_crescente_prezzo_decrescente_pue(self):
        s = _F["mh688_sensitivita"](self._ing())
        for riga in ("x0.7", "x1.0", "x1.3"):
            assert s.loc[riga, "PUE 1.045"] > \
                s.loc[riga, "PUE 1.100"] > \
                s.loc[riga, "PUE 1.155"]
        for colonna in ("PUE 1.045", "PUE 1.100",
                        "PUE 1.155"):
            assert s.loc["x0.7", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.3", colonna]

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh688_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh688_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 30

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh688_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_a" in txt
        assert "risparmio_el_mwh" in txt
        assert "risparmio_netto_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "acqua_risp_m3" in txt
        assert "risparmio_lordo_eur_a" in txt
        assert "prezzo_el_eur_kwh" in txt
        assert "pue_imm" in txt
        assert "wue_base_l_kwh" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh688_csv"](bc, self._ing())
        assert f"risparmio_el_mwh;{REL_DEMO}" in txt
        assert f"risparmio_netto_eur_a;{NETTO_DEMO}" in txt
        assert f"capex_eur;{CAPEX_DEMO}" in txt
        assert "co2_evitata_t_a;613.1999999999999" in txt
        assert f"risparmio_lordo_eur_a;{LORDO_DEMO}" in txt
        assert f"acqua_risp_m3;{ACQR_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def688["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def688\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh688_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W688 (24/10/2026) - tab688' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh688_num", "mh688_nneg", "mh688_pos",
                     "mh688_int_pos", "mh688_tol",
                     "mh688_e_it", "mh688_energia",
                     "mh688_risparmio_el", "mh688_acqua",
                     "mh688_acqua_risp", "mh688_lordo",
                     "mh688_risparmio_netto", "mh688_capex",
                     "mh688_co2_evitata",
                     "mh688_van", "mh688_tir",
                     "mh688_payback", "mh688_verdetto",
                     "_mh688_neutro", "mh688_calcola",
                     "mh688_sensitivita", "mh688_csv",
                     "mh688_demo", "demo_calcoli"):
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
        # l'apply (come w687_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w688_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE688) == 1

    def test_blocco_with_tab688(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab688:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE688

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st688_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 18, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st687_") for k in keys)
        assert not any(k.startswith("st686_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg688" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg688") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg688")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia risparmiata (MWh/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd688" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_immersion_presente(self):
        src = _ui_src()
        assert "liquido dielettrico" in src
        assert "direttamente dai server" in src
        assert "1.05-1.10" in src
        assert "dipende dal WUE" in src
        assert "CO2 solo sull'elettricita' risparmiata" in src
        assert "free cooling" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Risparmio elettrico" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh688_csv" in src
        assert "immersion_cooling_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh688_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo elettricità" in src
        assert "PUE immersione" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st688_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W688 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab688:")
        assert "mh688_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab688" in (_new_dir() / "w688_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w688_helpers.py", "w688_ui.py",
                   "w688_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab687" not in src
        assert "tab686" not in src
        assert "tab685" not in src
