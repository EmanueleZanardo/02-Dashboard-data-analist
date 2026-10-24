"""Test tab687 "🔌🏠 Vehicle-to-home (V2H): la batteria dell'auto alimenta la casa?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
batteria 75 kWh con DoD 0,60 (60 %); consumo casa
20 kWh/giorno con quota serale 0,50 (50 %);
250 giorni V2H all'anno; prezzo rete 0,30
EUR/kWh; prezzo ricarica 0,10 EUR/kWh;
efficienza ciclo 0,90 (90 %); costo degrado
0,05 EUR/kWh; OPEX caricatore 50 EUR/anno;
CAPEX caricatore bidirezionale 1500 EUR;
vita 10 anni; WACC 0,05 (5 %); tolleranza
0,10 (10 % del CAPEX); fattore CO2 0,35 kg/kWh.

- energia_disponibile_giorno_kwh = 45.0
- consumo_serale_giorno_kwh = 10.0
- energia_v2h_giorno_kwh = 10.0
- energia_v2h_anno_kwh = 2500.0
- risparmio_lordo_eur_a = 750.0
- energia_ricarica_anno_kwh = 2777.777777777778
- costo_ricarica_eur_a = 277.77777777777777
- costo_degrado_eur_a = 125.0
- opex_caricatore_eur_a = 50.0
- risparmio_netto_eur_a = 297.22222222222223
- capex_tot_eur = 1500.0
- co2_evitata_t_a = 0.875
- van = 795.0712150632653
- tir = 14.854487495034018 (in uscita: percentuale)
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
    if (p / "w687_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w687_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w687_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w687_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w687_helpers.py: {missing}")
    return out


_F = _load("mh687_num", "mh687_nneg", "mh687_pos",
           "mh687_int_pos", "mh687_tol",
           "mh687_frac_pos", "mh687_giorni",
           "mh687_disponibile", "mh687_serale",
           "mh687_v2h_giorno", "mh687_v2h_anno",
           "mh687_lordo", "mh687_ricarica_kwh",
           "mh687_costo_ricarica", "mh687_degrado",
           "mh687_risparmio_netto", "mh687_capex_tot",
           "mh687_co2_evitata",
           "mh687_van", "mh687_tir",
           "mh687_payback", "mh687_verdetto",
           "_mh687_neutro", "mh687_calcola",
           "mh687_sensitivita", "mh687_csv",
           "mh687_demo", "demo_calcoli")

TITLE687 = ("🔌🏠 Vehicle-to-home (V2H): la batteria "
            "dell'auto alimenta la casa?")

DISP_DEMO = 45.0
SER_DEMO = 10.0
V2HG_DEMO = 10.0
V2HA_DEMO = 2500.0
LORDO_DEMO = 750.0
RIC_DEMO = 2777.777777777778
CRIC_DEMO = 277.77777777777777
DEGR_DEMO = 125.0
OPEX_DEMO = 50.0
NETTO_DEMO = 297.22222222222223
CAPEX_DEMO = 1500.0
CO2_DEMO = 0.875
VAN_DEMO = 795.0712150632653
TIR_DEMO = 14.854487495034018
PAYBACK_DEMO = 6
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w687_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w687_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh687_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh687_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh687_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh687_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh687_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh687_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh687_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh687_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh687_int_pos"](10.0, "x") == 10

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh687_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh687_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh687_tol"](0.0, "x") == 0.0
        assert _F["mh687_tol"](1.0, "x") == 1.0

    def test_frac_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh687_frac_pos"](0.0, "x")

    def test_frac_pos_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh687_frac_pos"](1.01, "x")

    def test_frac_pos_accetta_uno(self):
        assert _F["mh687_frac_pos"](1.0, "x") == 1.0

    def test_frac_pos_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh687_frac_pos"](-0.01, "x")

    def test_giorni_rifiuta_oltre_365(self):
        with pytest.raises(ValueError):
            _F["mh687_giorni"](366, "x")

    def test_giorni_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_giorni"](-1, "x")

    def test_giorni_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh687_giorni"](100.5, "x")

    def test_giorni_accetta_estremi(self):
        assert _F["mh687_giorni"](0, "x") == 0
        assert _F["mh687_giorni"](365, "x") == 365
        assert _F["mh687_giorni"](250.0, "x") == 250


class TestFisica:
    def test_disponibile_demo(self):
        assert _F["mh687_disponibile"](
            75.0, 0.60) == pytest.approx(DISP_DEMO, rel=REL)

    def test_disponibile_formula(self):
        assert _F["mh687_disponibile"](
            100.0, 0.50) == pytest.approx(50.0, rel=1e-12)

    def test_disponibile_dod_uno(self):
        assert _F["mh687_disponibile"](
            75.0, 1.0) == pytest.approx(75.0, rel=1e-12)

    def test_disponibile_rifiuta_capacita_zero(self):
        with pytest.raises(ValueError):
            _F["mh687_disponibile"](0.0, 0.60)

    def test_disponibile_rifiuta_dod_zero(self):
        with pytest.raises(ValueError):
            _F["mh687_disponibile"](75.0, 0.0)

    def test_disponibile_rifiuta_dod_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh687_disponibile"](75.0, 1.01)

    def test_serale_demo(self):
        assert _F["mh687_serale"](
            20.0, 0.50) == pytest.approx(SER_DEMO, rel=REL)

    def test_serale_zero_se_quota_zero(self):
        assert _F["mh687_serale"](20.0, 0.0) == 0.0

    def test_serale_pieno_se_quota_uno(self):
        assert _F["mh687_serale"](
            20.0, 1.0) == pytest.approx(20.0, rel=1e-12)

    def test_serale_rifiuta_quota_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh687_serale"](20.0, 1.01)

    def test_serale_rifiuta_consumo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_serale"](-1.0, 0.50)

    def test_v2h_giorno_demo(self):
        assert _F["mh687_v2h_giorno"](
            DISP_DEMO, SER_DEMO) == pytest.approx(
            V2HG_DEMO, rel=REL)

    def test_v2h_giorno_cappato_dalla_batteria(self):
        # min(10, 30) = 10
        assert _F["mh687_v2h_giorno"](
            10.0, 30.0) == pytest.approx(10.0, rel=1e-12)

    def test_v2h_giorno_cappato_dal_serale(self):
        # min(45, 8) = 8
        assert _F["mh687_v2h_giorno"](
            45.0, 8.0) == pytest.approx(8.0, rel=1e-12)

    def test_v2h_giorno_zero_se_serale_zero(self):
        assert _F["mh687_v2h_giorno"](DISP_DEMO, 0.0) == 0.0

    def test_v2h_giorno_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh687_v2h_giorno"](-1.0, 10.0)
        with pytest.raises(ValueError):
            _F["mh687_v2h_giorno"](45.0, -1.0)

    def test_v2h_anno_demo(self):
        assert _F["mh687_v2h_anno"](
            V2HG_DEMO, 250) == pytest.approx(
            V2HA_DEMO, rel=REL)

    def test_v2h_anno_zero_se_giorni_zero(self):
        assert _F["mh687_v2h_anno"](V2HG_DEMO, 0) == 0.0

    def test_v2h_anno_rifiuta_giorni_oltre_365(self):
        with pytest.raises(ValueError):
            _F["mh687_v2h_anno"](V2HG_DEMO, 366)

    def test_lordo_demo(self):
        assert _F["mh687_lordo"](
            V2HA_DEMO, 0.30) == pytest.approx(
            LORDO_DEMO, rel=REL)

    def test_lordo_formula(self):
        assert _F["mh687_lordo"](
            1000.0, 0.25) == pytest.approx(250.0, rel=1e-12)

    def test_lordo_zero_se_prezzo_zero(self):
        assert _F["mh687_lordo"](V2HA_DEMO, 0.0) == 0.0

    def test_lordo_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_lordo"](V2HA_DEMO, -0.01)

    def test_ricarica_demo(self):
        assert _F["mh687_ricarica_kwh"](
            V2HA_DEMO, 0.90) == pytest.approx(
            RIC_DEMO, rel=REL)

    def test_ricarica_uguale_se_efficienza_uno(self):
        assert _F["mh687_ricarica_kwh"](
            V2HA_DEMO, 1.0) == pytest.approx(
            V2HA_DEMO, rel=1e-12)

    def test_ricarica_rifiuta_efficienza_zero(self):
        with pytest.raises(ValueError):
            _F["mh687_ricarica_kwh"](V2HA_DEMO, 0.0)

    def test_costo_ricarica_demo(self):
        assert _F["mh687_costo_ricarica"](
            RIC_DEMO, 0.10) == pytest.approx(
            CRIC_DEMO, rel=REL)

    def test_costo_ricarica_zero_se_prezzo_zero(self):
        assert _F["mh687_costo_ricarica"](RIC_DEMO, 0.0) == 0.0

    def test_degrado_demo(self):
        assert _F["mh687_degrado"](
            V2HA_DEMO, 0.05) == pytest.approx(
            DEGR_DEMO, rel=REL)

    def test_degrado_zero_se_costo_zero(self):
        assert _F["mh687_degrado"](V2HA_DEMO, 0.0) == 0.0

    def test_degrado_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_degrado"](V2HA_DEMO, -0.01)

    def test_risparmio_netto_demo(self):
        assert _F["mh687_risparmio_netto"](
            LORDO_DEMO, CRIC_DEMO, DEGR_DEMO,
            OPEX_DEMO) == pytest.approx(NETTO_DEMO, rel=REL)

    def test_risparmio_netto_puo_essere_negativo(self):
        assert _F["mh687_risparmio_netto"](
            100.0, 200.0, 50.0, 50.0) == -200.0

    def test_risparmio_netto_ordine_sottrazioni(self):
        # 750 - 277.777... - 125 - 50
        assert _F["mh687_risparmio_netto"](
            750.0, 277.77777777777777, 125.0,
            50.0) == pytest.approx(NETTO_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh687_capex_tot"](
            1500.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh687_capex_tot"](0.0) == 0.0

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_capex_tot"](-1.0)

    def test_co2_demo(self):
        assert _F["mh687_co2_evitata"](
            V2HA_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_formula(self):
        assert _F["mh687_co2_evitata"](
            10000.0, 0.35) == pytest.approx(3.5, rel=1e-12)

    def test_co2_zero_se_fattore_zero(self):
        assert _F["mh687_co2_evitata"](V2HA_DEMO, 0.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_co2_evitata"](V2HA_DEMO, -0.01)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh687_van"](
            NETTO_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        # -1500 + 297.222... x (1-1.05^-10)/0.05
        atteso = -CAPEX_DEMO + NETTO_DEMO * (
            1.0 - 1.05 ** (-10)) / 0.05
        assert _F["mh687_van"](
            NETTO_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh687_van"](
            NETTO_DEMO, CAPEX_DEMO, 0.0,
            10) == pytest.approx(
            -CAPEX_DEMO + NETTO_DEMO * 10, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + NETTO_DEMO * 10 == pytest.approx(
            1472.2222222222223, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_van"](NETTO_DEMO, CAPEX_DEMO, -0.01, 10)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh687_van"](NETTO_DEMO, -1.0, 0.05, 10)

    def test_tir_demo(self):
        assert _F["mh687_tir"](
            CAPEX_DEMO, NETTO_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh687_tir"](CAPEX_DEMO, 0.0, 10) is None
        assert _F["mh687_tir"](CAPEX_DEMO, -100.0, 10) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh687_tir"](0.0, NETTO_DEMO, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh687_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh687_tir"](CAPEX_DEMO, NETTO_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            NETTO_DEMO / (1.0 + tir) ** i
            for i in range(1, 11))
        assert npv == pytest.approx(0.0, abs=1e-6)

    def test_payback_demo(self):
        assert _F["mh687_payback"](
            CAPEX_DEMO, NETTO_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_ceil_arrotonda_su(self):
        assert _F["mh687_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh687_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh687_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_oltre_vita_ceil_puro(self):
        assert _F["mh687_payback"](CAPEX_DEMO, 100.0, 10) == 15

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh687_payback"](0.0, NETTO_DEMO, 10) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh687_payback"](CAPEX_DEMO, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh687_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, NETTO_DEMO,
            V2HA_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh687_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, NETTO_DEMO,
            V2HA_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 150 = 10 % di 1500 -> MARGINALE
        assert _F["mh687_verdetto"](
            -150.0, CAPEX_DEMO, 0.10, NETTO_DEMO,
            V2HA_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh687_verdetto"](
            -500.0, CAPEX_DEMO, 0.10, NETTO_DEMO,
            V2HA_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh687_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            V2HA_DEMO) == "NON_CALCOLABILE"
        assert _F["mh687_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0,
            V2HA_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_v2h_zero(self):
        assert _F["mh687_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, NETTO_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh687_verdetto"](
            0.0, 0.0, 0.10, NETTO_DEMO,
            V2HA_DEMO) == "CONVIENTE"
        assert _F["mh687_verdetto"](
            1000.0, 0.0, 0.10, NETTO_DEMO,
            V2HA_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh687_verdetto"](
            -1.0, 0.0, 0.10, NETTO_DEMO,
            V2HA_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh687_verdetto"](
            -1.0, 0.0, 0.10, NETTO_DEMO,
            V2HA_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh687_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 NETTO_DEMO, V2HA_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh687_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 NETTO_DEMO, V2HA_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh687_demo"]()
        d.update(kw)
        return _F["mh687_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["energia_disponibile_giorno_kwh"] == \
            pytest.approx(DISP_DEMO, rel=REL)
        assert c["consumo_serale_giorno_kwh"] == \
            pytest.approx(SER_DEMO, rel=REL)
        assert c["energia_v2h_giorno_kwh"] == \
            pytest.approx(V2HG_DEMO, rel=REL)
        assert c["energia_v2h_anno_kwh"] == \
            pytest.approx(V2HA_DEMO, rel=REL)
        assert c["risparmio_lordo_eur_a"] == \
            pytest.approx(LORDO_DEMO, rel=REL)
        assert c["energia_ricarica_anno_kwh"] == \
            pytest.approx(RIC_DEMO, rel=REL)
        assert c["costo_ricarica_eur_a"] == \
            pytest.approx(CRIC_DEMO, rel=REL)
        assert c["costo_degrado_eur_a"] == \
            pytest.approx(DEGR_DEMO, rel=REL)
        assert c["risparmio_netto_eur_a"] == \
            pytest.approx(NETTO_DEMO, rel=REL)
        assert c["capex_tot_eur"] == pytest.approx(
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
        """mh687_calcola(**mh687_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh687_demo"]()
        b = _F["mh687_calcola"](**d)
        coppie = [("energia_disponibile_giorno_kwh",
                   DISP_DEMO),
                  ("consumo_serale_giorno_kwh", SER_DEMO),
                  ("energia_v2h_giorno_kwh", V2HG_DEMO),
                  ("energia_v2h_anno_kwh", V2HA_DEMO),
                  ("risparmio_lordo_eur_a", LORDO_DEMO),
                  ("energia_ricarica_anno_kwh", RIC_DEMO),
                  ("costo_ricarica_eur_a", CRIC_DEMO),
                  ("costo_degrado_eur_a", DEGR_DEMO),
                  ("risparmio_netto_eur_a", NETTO_DEMO),
                  ("capex_tot_eur", CAPEX_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh687_demo"]()
        assert d["capacita_batteria_kwh"] == 75.0
        assert d["dod_frac"] == 0.60
        assert d["consumo_casa_kwh_giorno"] == 20.0
        assert d["quota_serale_frac"] == 0.50
        assert d["giorni_v2h_anno"] == 250
        assert d["prezzo_rete_eur_kwh"] == 0.30
        assert d["prezzo_ricarica_eur_kwh"] == 0.10
        assert d["eff_ciclo_frac"] == 0.90
        assert d["costo_degrado_eur_kwh"] == 0.05
        assert d["opex_caricatore_eur_a"] == 50.0
        assert d["costo_caricatore_bidir_eur"] == 1500.0
        assert d["fattore_co2_kg_kwh"] == 0.35
        assert d["vita_anni"] == 10
        assert d["wacc"] == 0.05
        assert d["tol_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_disponibile_giorno_kwh",
                       "consumo_serale_giorno_kwh",
                       "energia_v2h_giorno_kwh",
                       "energia_v2h_anno_kwh",
                       "risparmio_lordo_eur_a",
                       "energia_ricarica_anno_kwh",
                       "costo_ricarica_eur_a",
                       "costo_degrado_eur_a",
                       "risparmio_netto_eur_a",
                       "capex_tot_eur",
                       "co2_evitata_t_a",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 6" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_capacita_zero_neutro(self):
        n = self._bc(capacita_batteria_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["energia_v2h_anno_kwh"] == 0.0
        assert n["risparmio_netto_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dod_zero_neutro(self):
        n = self._bc(dod_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dod_oltre_uno_neutro(self):
        n = self._bc(dod_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dod_uno_calcolabile(self):
        # DoD 1.0: disponibile 75, serale 10 -> V2H
        # invariato a 10/giorno
        n = self._bc(dod_frac=1.0)
        assert n["valid"] is True
        assert n["energia_disponibile_giorno_kwh"] == \
            pytest.approx(75.0, rel=REL)
        assert n["energia_v2h_anno_kwh"] == \
            pytest.approx(V2HA_DEMO, rel=REL)

    def test_quota_serale_zero_neutro(self):
        # serale 0 -> V2H 0 -> neutro
        n = self._bc(quota_serale_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_quota_serale_uno_calcolabile(self):
        # serale 20, disponibile 45 -> V2H 20/giorno
        n = self._bc(quota_serale_frac=1.0)
        assert n["valid"] is True
        assert n["energia_v2h_anno_kwh"] == \
            pytest.approx(5000.0, rel=REL)

    def test_giorni_zero_neutro(self):
        n = self._bc(giorni_v2h_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_365_calcolabile(self):
        n = self._bc(giorni_v2h_anno=365)
        assert n["valid"] is True
        assert n["energia_v2h_anno_kwh"] == \
            pytest.approx(3650.0, rel=REL)

    def test_giorni_oltre_365_neutro(self):
        n = self._bc(giorni_v2h_anno=366)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_non_intero_neutro(self):
        n = self._bc(giorni_v2h_anno=250.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eff_zero_neutro(self):
        n = self._bc(eff_ciclo_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eff_uno_calcolabile(self):
        n = self._bc(eff_ciclo_frac=1.0)
        assert n["valid"] is True
        assert n["energia_ricarica_anno_kwh"] == \
            pytest.approx(V2HA_DEMO, rel=REL)

    def test_prezzi_negativi_neutro(self):
        for k in ("prezzo_rete_eur_kwh",
                  "prezzo_ricarica_eur_kwh",
                  "costo_degrado_eur_kwh",
                  "fattore_co2_kg_kwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_opex_capex_negativi_neutro(self):
        for k in ("opex_caricatore_eur_a",
                  "costo_caricatore_bidir_eur"):
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
        n = self._bc(prezzo_rete_eur_kwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_netto_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(capacita_batteria_kwh=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(capacita_batteria_kwh=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risparmio_negativo_neutro(self):
        # prezzo rete basso + ricarica cara: lordo
        # 250, ricarica 277.78, degrado 125, OPEX 50
        n = self._bc(prezzo_rete_eur_kwh=0.10,
                     prezzo_ricarica_eur_kwh=0.10)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_netto_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -1500 + 297.222... x 10
        n = self._bc(wacc=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + NETTO_DEMO * 10, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(costo_caricatore_bidir_eur=0.0)
        assert n["capex_tot_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 2395: VAN = -2395 + 2295.07 = circa
        # -100, entro il 10 % di 2395 -> MARGINALE
        n = self._bc(costo_caricatore_bidir_eur=2395.0)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 2395.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(costo_caricatore_bidir_eur=5000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh687_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh687_neutro"]()
        for chiave in ("valid",
                       "energia_disponibile_giorno_kwh",
                       "consumo_serale_giorno_kwh",
                       "energia_v2h_giorno_kwh",
                       "energia_v2h_anno_kwh",
                       "risparmio_lordo_eur_a",
                       "energia_ricarica_anno_kwh",
                       "costo_ricarica_eur_a",
                       "costo_degrado_eur_a",
                       "opex_caricatore_eur_a",
                       "risparmio_netto_eur_a",
                       "capex_tot_eur",
                       "co2_evitata_t_a", "van",
                       "tir", "payback", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 13
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia disponibile (kWh/giorno)" in voci
        assert "Consumo serale (kWh/giorno)" in voci
        assert "Energia V2H (kWh/anno)" in voci
        assert "Risparmio lordo (EUR/anno)" in voci
        assert "Costo ricarica (EUR/anno)" in voci
        assert "Costo degrado (EUR/anno)" in voci
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
        return _F["mh687_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh687_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["200 giorni",
                                   "250 giorni",
                                   "300 giorni"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh687_sensitivita"](self._ing())
        assert s.loc["x1.0", "250 giorni"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh687_sensitivita"](self._ing())
        centro = s.loc["x1.0", "250 giorni"]
        assert s.loc["x0.8", "200 giorni"] < centro
        assert s.loc["x1.0", "200 giorni"] < centro
        assert s.loc["x1.2", "250 giorni"] > centro
        assert s.loc["x0.8", "250 giorni"] < centro
        assert s.loc["x1.2", "300 giorni"] > centro

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi variano davvero sulla
        # demo (prezzo senza tetto, giorni 200/250/
        # 300 in dominio): nessuna cella puo'
        # essere 0,0 per regime degenere
        s = _F["mh687_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_crescente_in_entrambi_i_fattori(self):
        s = _F["mh687_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "200 giorni"] < \
                s.loc[riga, "250 giorni"] < \
                s.loc[riga, "300 giorni"]
        for colonna in ("200 giorni",
                        "250 giorni",
                        "300 giorni"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh687_sensitivita"](self._ing())
        # ogni riga varia lungo le colonne e ogni
        # colonna varia lungo le righe: nessun asse
        # piatto per costruzione
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh687_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 31

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh687_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_a" in txt
        assert "energia_v2h_anno_kwh" in txt
        assert "risparmio_netto_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "energia_v2h_giorno_kwh" in txt
        assert "risparmio_lordo_eur_a" in txt
        assert "prezzo_rete_eur_kwh" in txt
        assert "dod_frac" in txt
        assert "giorni_v2h_anno" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh687_csv"](bc, self._ing())
        assert f"energia_v2h_anno_kwh;{V2HA_DEMO}" in txt
        assert f"risparmio_netto_eur_a;{NETTO_DEMO}" in txt
        assert f"capex_tot_eur;{CAPEX_DEMO}" in txt
        assert f"co2_evitata_t_a;{CO2_DEMO}" in txt
        assert f"risparmio_lordo_eur_a;{LORDO_DEMO}" in txt
        assert f"costo_ricarica_eur_a;{CRIC_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def687["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def687\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh687_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W687 (24/10/2026) - tab687' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh687_num", "mh687_nneg", "mh687_pos",
                     "mh687_int_pos", "mh687_tol",
                     "mh687_frac_pos", "mh687_giorni",
                     "mh687_disponibile", "mh687_serale",
                     "mh687_v2h_giorno", "mh687_v2h_anno",
                     "mh687_lordo", "mh687_ricarica_kwh",
                     "mh687_costo_ricarica", "mh687_degrado",
                     "mh687_risparmio_netto",
                     "mh687_capex_tot",
                     "mh687_co2_evitata",
                     "mh687_van", "mh687_tir",
                     "mh687_payback", "mh687_verdetto",
                     "_mh687_neutro", "mh687_calcola",
                     "mh687_sensitivita", "mh687_csv",
                     "mh687_demo", "demo_calcoli"):
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
        # l'apply (come w686_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w687_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE687) == 1

    def test_blocco_with_tab687(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab687:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE687

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st687_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st686_") for k in keys)
        assert not any(k.startswith("st685_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg687" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg687") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg687")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia V2H (kWh/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd687" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_v2h_presente(self):
        src = _ui_src()
        assert "V2H ≠ V2G" in src
        assert "non viene venduta in rete" in src
        assert "prezzo rete meno costo ricarica meno degrado" in src
        assert "surplus FV" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Risparmio lordo" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh687_csv" in src
        assert "v2h_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh687_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo rete" in src
        assert "Giorni V2H" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st687_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W687 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab687:")
        assert "mh687_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab687" in (_new_dir() / "w687_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w687_helpers.py", "w687_ui.py",
                   "w687_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab686" not in src
        assert "tab685" not in src
        assert "tab684" not in src
