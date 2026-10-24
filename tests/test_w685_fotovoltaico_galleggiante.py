"""Test tab685 "🌊☀️ Fotovoltaico galleggiante (FPV): il business case"

Demo calcolata eseguendo demo_calcoli() (non a mano):
5 MWp galleggianti con producibilita' specifica
1300 kWh/kWp/anno e bonus di raffrescamento 5 %
(6825000 kWh/anno di produzione); prezzo energia
90 EUR/MWh; CAPEX 950 EUR/kWp; OPEX 15
EUR/kWp/anno; fattore CO2 0,35 kg/kWh;
evaporazione risparmiata 1500 m3/MWp/anno; vita
25 anni; WACC 0,05 (5 %); tolleranza 0,10 (10 %
del CAPEX).

- produzione_kwh = 6825000.0
- ricavo_eur = 614250.0
- opex_tot_eur = 75000.0
- risparmio_eur = 539250.0
- capex_tot_eur = 4750000.0
- co2_evitata_t = 2388.75
- acqua_risparmiata_m3 = 7500.0
- crf = 0.0709524572992296
- van = 2850159.6072396375
- tir = 10.394540938278249 (in uscita: percentuale)
- payback = 9
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
    if (p / "w685_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w685_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w685_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w685_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w685_helpers.py: {missing}")
    return out


_F = _load("mh685_num", "mh685_nneg", "mh685_pos",
           "mh685_int_pos", "mh685_tol",
           "mh685_produzione", "mh685_ricavo",
           "mh685_opex_tot", "mh685_risparmio",
           "mh685_capex_tot", "mh685_co2_evitata",
           "mh685_acqua_risparmiata", "mh685_crf",
           "mh685_van", "mh685_tir",
           "mh685_payback", "mh685_verdetto",
           "_mh685_neutro", "mh685_calcola",
           "mh685_sensitivita", "mh685_csv",
           "mh685_demo", "demo_calcoli")

TITLE685 = ("🌊☀️ Fotovoltaico galleggiante (FPV): "
            "il business case")

PROD_DEMO = 6825000.0
RIC_DEMO = 614250.0
OPEX_DEMO = 75000.0
RISP_DEMO = 539250.0
CAPEX_DEMO = 4750000.0
CO2_DEMO = 2388.75
ACQUA_DEMO = 7500.0
CRF_DEMO = 0.0709524572992296
VAN_DEMO = 2850159.6072396375
TIR_DEMO = 10.394540938278249
PAYBACK_DEMO = 9
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w685_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w685_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh685_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh685_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh685_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh685_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh685_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh685_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh685_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh685_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh685_int_pos"](25.0, "x") == 25

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh685_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh685_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh685_tol"](0.0, "x") == 0.0
        assert _F["mh685_tol"](1.0, "x") == 1.0


class TestFisica:
    def test_produzione_demo(self):
        assert _F["mh685_produzione"](
            5.0, 1300.0, 0.05) == pytest.approx(PROD_DEMO,
                                                rel=REL)

    def test_produzione_formula(self):
        # 2 MWp x 1000 x 1000 kWh/kWp x 1,10 = 2200000
        assert _F["mh685_produzione"](
            2.0, 1000.0, 0.10) == pytest.approx(2200000.0,
                                                rel=1e-12)

    def test_produzione_senza_bonus(self):
        assert _F["mh685_produzione"](
            5.0, 1300.0, 0.0) == pytest.approx(6500000.0,
                                               rel=1e-12)

    def test_produzione_bonus_aumenta_resa(self):
        assert _F["mh685_produzione"](
            5.0, 1300.0, 0.10) > _F["mh685_produzione"](
            5.0, 1300.0, 0.05)

    def test_produzione_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh685_produzione"](0.0, 1300.0, 0.05)

    def test_produzione_rifiuta_yield_zero(self):
        with pytest.raises(ValueError):
            _F["mh685_produzione"](5.0, 0.0, 0.05)

    def test_produzione_rifiuta_bonus_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh685_produzione"](5.0, 1300.0, 1.01)

    def test_produzione_rifiuta_bonus_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_produzione"](5.0, 1300.0, -0.01)

    def test_ricavo_demo(self):
        assert _F["mh685_ricavo"](
            PROD_DEMO, 90.0) == pytest.approx(RIC_DEMO,
                                              rel=REL)

    def test_ricavo_formula_mwh(self):
        # 1000000 kWh x 100 EUR/MWh / 1000 = 100000 EUR
        assert _F["mh685_ricavo"](
            1000000.0, 100.0) == pytest.approx(100000.0,
                                               rel=1e-12)

    def test_ricavo_zero_se_prezzo_zero(self):
        assert _F["mh685_ricavo"](PROD_DEMO, 0.0) == 0.0

    def test_ricavo_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_ricavo"](PROD_DEMO, -0.01)

    def test_opex_tot_demo(self):
        assert _F["mh685_opex_tot"](
            5.0, 15.0) == pytest.approx(OPEX_DEMO, rel=REL)

    def test_opex_tot_zero_se_unitario_zero(self):
        assert _F["mh685_opex_tot"](5.0, 0.0) == 0.0

    def test_opex_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh685_opex_tot"](5.0, -0.01)
        with pytest.raises(ValueError):
            _F["mh685_opex_tot"](-5.0, 15.0)

    def test_risparmio_demo(self):
        assert _F["mh685_risparmio"](
            RIC_DEMO, OPEX_DEMO) == pytest.approx(RISP_DEMO,
                                                  rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh685_risparmio"](100.0, 250.0) == -150.0

    def test_risparmio_zero_se_pareggio(self):
        assert _F["mh685_risparmio"](1000.0, 1000.0) == 0.0

    def test_capex_tot_demo(self):
        assert _F["mh685_capex_tot"](
            5.0, 950.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_tot_zero_se_unitario_zero(self):
        assert _F["mh685_capex_tot"](5.0, 0.0) == 0.0

    def test_capex_tot_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh685_capex_tot"](0.0, 950.0)

    def test_capex_tot_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_capex_tot"](5.0, -1.0)

    def test_co2_demo(self):
        assert _F["mh685_co2_evitata"](
            PROD_DEMO, 0.35) == pytest.approx(CO2_DEMO,
                                              rel=REL)

    def test_co2_formula(self):
        # 1000000 kWh x 0,35 kg/kWh / 1000 = 350 t
        assert _F["mh685_co2_evitata"](
            1000000.0, 0.35) == pytest.approx(350.0,
                                              rel=1e-12)

    def test_co2_zero_se_fattore_zero(self):
        assert _F["mh685_co2_evitata"](PROD_DEMO, 0.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_co2_evitata"](PROD_DEMO, -0.01)

    def test_acqua_demo(self):
        assert _F["mh685_acqua_risparmiata"](
            5.0, 1500.0) == pytest.approx(ACQUA_DEMO,
                                          rel=REL)

    def test_acqua_scala_con_potenza(self):
        assert _F["mh685_acqua_risparmiata"](
            10.0, 1500.0) == pytest.approx(15000.0,
                                           rel=1e-12)

    def test_acqua_zero_se_evap_zero(self):
        assert _F["mh685_acqua_risparmiata"](5.0, 0.0) == 0.0

    def test_acqua_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh685_acqua_risparmiata"](5.0, -0.01)
        with pytest.raises(ValueError):
            _F["mh685_acqua_risparmiata"](-5.0, 1500.0)

    def test_crf_demo(self):
        assert _F["mh685_crf"](
            0.05, 25) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh685_crf"](
            0.0, 25) == pytest.approx(1.0 / 25.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_crf"](-0.01, 25)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh685_crf"](0.05, 0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh685_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh685_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            25) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 25, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + RISP_DEMO * 25 == pytest.approx(
            8731250.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 25)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh685_van"](RISP_DEMO, -1.0, 0.05, 25)

    def test_tir_demo(self):
        assert _F["mh685_tir"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh685_tir"](CAPEX_DEMO, 0.0, 25) is None
        assert _F["mh685_tir"](CAPEX_DEMO, -100.0, 25) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh685_tir"](0.0, RISP_DEMO, 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh685_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh685_payback"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_ceil_arrotonda_su(self):
        # 1000 / 300 = 3,33... -> 4
        assert _F["mh685_payback"](1000.0, 300.0, 25) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh685_payback"](1000.0, 1000.0, 25) == 1
        assert _F["mh685_payback"](1000.0, 2000.0, 25) == 1

    def test_payback_oltre_vita_ceil_puro(self):
        # ceil puro senza tetto di vita: 4750000/100 = 47500
        assert _F["mh685_payback"](CAPEX_DEMO, 100.0, 25) == 47500

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh685_payback"](0.0, RISP_DEMO, 25) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh685_payback"](CAPEX_DEMO, 0.0, 25) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh685_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, RISP_DEMO,
            PROD_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh685_verdetto"](
            -5000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            PROD_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh685_verdetto"](
            -500000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            PROD_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh685_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            PROD_DEMO) == "NON_CALCOLABILE"
        assert _F["mh685_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0,
            PROD_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_produzione_zero(self):
        assert _F["mh685_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh685_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) == "CONVIENTE"
        assert _F["mh685_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh685_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh685_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh685_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 RISP_DEMO, PROD_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh685_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 RISP_DEMO, PROD_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh685_demo"]()
        d.update(kw)
        return _F["mh685_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["produzione_kwh"] == pytest.approx(PROD_DEMO,
                                                    rel=REL)
        assert c["ricavo_eur"] == pytest.approx(RIC_DEMO,
                                                rel=REL)
        assert c["opex_tot_eur"] == pytest.approx(OPEX_DEMO,
                                                  rel=REL)
        assert c["risparmio_eur"] == pytest.approx(RISP_DEMO,
                                                   rel=REL)
        assert c["capex_tot_eur"] == pytest.approx(CAPEX_DEMO,
                                                   rel=REL)
        assert c["co2_evitata_t"] == pytest.approx(CO2_DEMO,
                                                   rel=REL)
        assert c["acqua_risparmiata_m3"] == pytest.approx(
            ACQUA_DEMO, rel=REL)
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
        """mh685_calcola(**mh685_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh685_demo"]()
        b = _F["mh685_calcola"](**d)
        coppie = [("produzione_kwh", PROD_DEMO),
                  ("ricavo_eur", RIC_DEMO),
                  ("opex_tot_eur", OPEX_DEMO),
                  ("risparmio_eur", RISP_DEMO),
                  ("capex_tot_eur", CAPEX_DEMO),
                  ("co2_evitata_t", CO2_DEMO),
                  ("acqua_risparmiata_m3", ACQUA_DEMO),
                  ("crf", CRF_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh685_demo"]()
        assert d["potenza_mwp"] == 5.0
        assert d["yield_kwh_kwp_a"] == 1300.0
        assert d["bonus_frac"] == 0.05
        assert d["prezzo_eur_mwh"] == 90.0
        assert d["capex_eur_kwp"] == 950.0
        assert d["opex_eur_kwp_a"] == 15.0
        assert d["fattore_co2_kg_kwh"] == 0.35
        assert d["evap_m3_mwp_a"] == 1500.0
        assert d["vita_anni"] == 25
        assert d["wacc"] == 0.05
        assert d["tol_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("produzione_kwh", "ricavo_eur",
                       "opex_tot_eur", "risparmio_eur",
                       "capex_tot_eur", "co2_evitata_t",
                       "acqua_risparmiata_m3", "crf", "van",
                       "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 9" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_mwp=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["produzione_kwh"] == 0.0
        assert n["risparmio_eur"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_mwp=-5.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_yield_zero_neutro(self):
        n = self._bc(yield_kwh_kwp_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bonus_oltre_uno_neutro(self):
        n = self._bc(bonus_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bonus_negativo_neutro(self):
        n = self._bc(bonus_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bonus_zero_calcolabile(self):
        n = self._bc(bonus_frac=0.0)
        assert n["valid"] is True
        assert n["produzione_kwh"] == pytest.approx(6500000.0,
                                                    rel=REL)
        assert n["risparmio_eur"] == pytest.approx(510000.0,
                                                   rel=REL)

    def test_prezzi_negativi_neutro(self):
        for k in ("prezzo_eur_mwh",
                  "fattore_co2_kg_kwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_opex_capex_evap_negativi_neutro(self):
        for k in ("opex_eur_kwp_a", "capex_eur_kwp",
                  "evap_m3_mwp_a"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=24.5)
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
        n = self._bc(prezzo_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(potenza_mwp=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_basso_risparmio_negativo_neutro(self):
        # prezzo 10 EUR/MWh: ricavo 68250 < OPEX 75000
        n = self._bc(prezzo_eur_mwh=10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_prezzo_zero_neutro(self):
        n = self._bc(prezzo_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -4750000 + 539250 x 25 = 8731250
        n = self._bc(wacc=0.0)
        assert n["van"] == pytest.approx(8731250.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_kwp=0.0)
        assert n["capex_tot_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0

    def test_acqua_non_monetizzata(self):
        # l'evaporazione cambia solo l'acqua, mai
        # VAN o risparmio: valore informativo
        base = self._bc()
        var = self._bc(evap_m3_mwp_a=3000.0)
        assert var["acqua_risparmiata_m3"] == pytest.approx(
            15000.0, rel=REL)
        assert var["van"] == pytest.approx(base["van"],
                                            rel=REL)
        assert var["risparmio_eur"] == pytest.approx(
            base["risparmio_eur"], rel=REL)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh685_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh685_neutro"]()
        for chiave in ("valid", "produzione_kwh",
                       "ricavo_eur", "opex_tot_eur",
                       "risparmio_eur", "capex_tot_eur",
                       "co2_evitata_t",
                       "acqua_risparmiata_m3", "crf", "van",
                       "tir", "payback", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 9
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Produzione (kWh/anno)" in voci
        assert "Ricavo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Acqua risparmiata (m3/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh685_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh685_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Yield x0.8",
                                   "Yield x1.0",
                                   "Yield x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh685_sensitivita"](self._ing())
        assert s.loc["x1.0", "Yield x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh685_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Yield x1.0"]
        assert s.loc["x0.8", "Yield x0.8"] < centro
        assert s.loc["x1.0", "Yield x0.8"] < centro
        assert s.loc["x1.2", "Yield x1.0"] > centro
        assert s.loc["x0.8", "Yield x1.0"] < centro
        assert s.loc["x1.2", "Yield x1.2"] > centro

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi i fattori sono senza tetto
        # (prezzo e yield): nessuna cella puo'
        # essere 0,0 per regime degenere
        s = _F["mh685_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_crescente_in_entrambi_i_fattori(self):
        s = _F["mh685_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Yield x0.8"] < \
                s.loc[riga, "Yield x1.0"] < \
                s.loc[riga, "Yield x1.2"]
        for colonna in ("Yield x0.8",
                        "Yield x1.0",
                        "Yield x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_assi_senza_tetto(self):
        # la griglia resta 3x3 anche variando gli
        # assi: prezzo e yield non hanno tetti
        s = _F["mh685_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert len(set(s.index)) == 3
        assert len(set(s.columns)) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh685_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 23

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh685_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_anno" in txt
        assert "acqua_risparmiata_m3_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "produzione_kwh_anno" in txt
        assert "risparmio_eur_anno" in txt
        assert "prezzo_eur_mwh" in txt
        assert "bonus_frac" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh685_csv"](bc, self._ing())
        assert f"produzione_kwh_anno;{PROD_DEMO}" in txt
        assert f"risparmio_eur_anno;{RISP_DEMO}" in txt
        assert f"capex_tot_eur;{CAPEX_DEMO}" in txt
        assert f"co2_evitata_t_anno;{CO2_DEMO}" in txt
        assert f"ricavo_eur_anno;{RIC_DEMO}" in txt
        assert f"acqua_risparmiata_m3_anno;{ACQUA_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def685["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def685\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 11, ui_keys
        demo_keys = set(_F["mh685_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W685 (24/10/2026) - tab685' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh685_num", "mh685_nneg", "mh685_pos",
                     "mh685_int_pos", "mh685_tol",
                     "mh685_produzione", "mh685_ricavo",
                     "mh685_opex_tot", "mh685_risparmio",
                     "mh685_capex_tot", "mh685_co2_evitata",
                     "mh685_acqua_risparmiata", "mh685_crf",
                     "mh685_van", "mh685_tir",
                     "mh685_payback", "mh685_verdetto",
                     "_mh685_neutro", "mh685_calcola",
                     "mh685_sensitivita", "mh685_csv",
                     "mh685_demo", "demo_calcoli"):
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
        # l'apply (come w684_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w685_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE685) == 1

    def test_blocco_with_tab685(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab685:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE685

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st685_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 16, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st684_") for k in keys)
        assert not any(k.startswith("st683_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg685" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg685") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg685")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Produzione (MWh/anno)" in src
        assert "Risparmio (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd685" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_fpv_vs_terra_presente(self):
        src = _ui_src()
        assert "raffrescamento" in src.lower()
        assert "suolo" in src.lower()
        assert "evaporazione" in src.lower()
        assert "ancoragg" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavo energia" in src
        assert "Risparmio annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh685_csv" in src
        assert "fpv_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh685_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo energia" in src
        assert "Producibilità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st685_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W685 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab685:")
        assert "mh685_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab685" in (_new_dir() / "w685_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w685_helpers.py", "w685_ui.py",
                   "w685_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab684" not in src
        assert "tab683" not in src
        assert "tab682" not in src
