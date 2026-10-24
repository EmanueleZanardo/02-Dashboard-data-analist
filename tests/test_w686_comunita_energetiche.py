"""Test tab686 "🏘️⚡ Comunità energetiche rinnovabili (CER): l'energia condivisa paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
200 kWp con producibilita' specifica 1200
kWh/kWp/anno (240000 kWh/anno di produzione);
consumo aggregato della comunita' 300000
kWh/anno; fattore di contemporaneita' 0,60
(60 %); tariffa premio 110 EUR/MWh
sull'energia condivisa; prezzo vendita
eccedente 80 EUR/MWh; CAPEX 1100 EUR/kWp;
OPEX 20 EUR/kWp/anno; fattore CO2 0,35
kg/kWh; vita 20 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del CAPEX).

- produzione_kwh = 240000.0
- condivisa_kwh = 144000.0
- eccedente_kwh = 96000.0
- incentivo_eur = 15840.0
- vendita_eur = 7680.0
- ricavo_tot_eur = 23520.0
- opex_tot_eur = 4000.0
- risparmio_eur = 19520.0
- capex_tot_eur = 220000.0
- co2_evitata_t = 84.0
- crf = 0.08024258719069129
- van = 23262.345886380645
- tir = 6.217085144386055 (in uscita: percentuale)
- payback = 12
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
    if (p / "w686_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w686_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w686_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w686_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w686_helpers.py: {missing}")
    return out


_F = _load("mh686_num", "mh686_nneg", "mh686_pos",
           "mh686_int_pos", "mh686_tol",
           "mh686_produzione", "mh686_condivisa",
           "mh686_eccedente", "mh686_incentivo",
           "mh686_vendita", "mh686_ricavo_tot",
           "mh686_opex_tot", "mh686_risparmio",
           "mh686_capex_tot", "mh686_co2_evitata",
           "mh686_crf",
           "mh686_van", "mh686_tir",
           "mh686_payback", "mh686_verdetto",
           "_mh686_neutro", "mh686_calcola",
           "mh686_sensitivita", "mh686_csv",
           "mh686_demo", "demo_calcoli")

TITLE686 = ("🏘️⚡ Comunità energetiche rinnovabili (CER): "
            "l'energia condivisa paga?")

PROD_DEMO = 240000.0
COND_DEMO = 144000.0
ECC_DEMO = 96000.0
INC_DEMO = 15840.0
VEND_DEMO = 7680.0
RIC_DEMO = 23520.0
OPEX_DEMO = 4000.0
RISP_DEMO = 19520.0
CAPEX_DEMO = 220000.0
CO2_DEMO = 84.0
CRF_DEMO = 0.08024258719069129
VAN_DEMO = 23262.345886380645
TIR_DEMO = 6.217085144386055
PAYBACK_DEMO = 12
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w686_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w686_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh686_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh686_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh686_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh686_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh686_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh686_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh686_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh686_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh686_int_pos"](20.0, "x") == 20

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh686_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh686_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh686_tol"](0.0, "x") == 0.0
        assert _F["mh686_tol"](1.0, "x") == 1.0


class TestFisica:
    def test_produzione_demo(self):
        assert _F["mh686_produzione"](
            200.0, 1200.0) == pytest.approx(PROD_DEMO,
                                            rel=REL)

    def test_produzione_formula(self):
        # 100 kWp x 1000 kWh/kWp = 100000
        assert _F["mh686_produzione"](
            100.0, 1000.0) == pytest.approx(100000.0,
                                            rel=1e-12)

    def test_produzione_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh686_produzione"](0.0, 1200.0)

    def test_produzione_rifiuta_yield_zero(self):
        with pytest.raises(ValueError):
            _F["mh686_produzione"](200.0, 0.0)

    def test_condivisa_demo(self):
        assert _F["mh686_condivisa"](
            PROD_DEMO, 300000.0, 0.60) == pytest.approx(
            COND_DEMO, rel=REL)

    def test_condivisa_cappata_dal_consumo(self):
        # min(200000, 100000) x 0,50 = 50000
        assert _F["mh686_condivisa"](
            200000.0, 100000.0, 0.50) == pytest.approx(
            50000.0, rel=1e-12)

    def test_condivisa_cappata_dalla_produzione(self):
        # min(100000, 300000) x 0,50 = 50000
        assert _F["mh686_condivisa"](
            100000.0, 300000.0, 0.50) == pytest.approx(
            50000.0, rel=1e-12)

    def test_condivisa_zero_se_sync_zero(self):
        assert _F["mh686_condivisa"](
            PROD_DEMO, 300000.0, 0.0) == 0.0

    def test_condivisa_zero_se_consumo_zero(self):
        assert _F["mh686_condivisa"](
            PROD_DEMO, 0.0, 0.60) == 0.0

    def test_condivisa_piena_se_sync_uno(self):
        assert _F["mh686_condivisa"](
            PROD_DEMO, 300000.0, 1.0) == pytest.approx(
            PROD_DEMO, rel=1e-12)

    def test_condivisa_rifiuta_sync_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh686_condivisa"](PROD_DEMO, 300000.0, 1.01)

    def test_condivisa_rifiuta_sync_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_condivisa"](PROD_DEMO, 300000.0, -0.01)

    def test_condivisa_rifiuta_consumo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_condivisa"](PROD_DEMO, -1.0, 0.60)

    def test_eccedente_demo(self):
        assert _F["mh686_eccedente"](
            PROD_DEMO, COND_DEMO) == pytest.approx(
            ECC_DEMO, rel=REL)

    def test_eccedente_zero_se_tutto_condiviso(self):
        assert _F["mh686_eccedente"](100000.0, 100000.0) == 0.0

    def test_eccedente_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh686_eccedente"](-1.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh686_eccedente"](PROD_DEMO, -1.0)

    def test_incentivo_demo(self):
        assert _F["mh686_incentivo"](
            COND_DEMO, 110.0) == pytest.approx(INC_DEMO,
                                               rel=REL)

    def test_incentivo_formula_mwh(self):
        # 100000 kWh x 100 EUR/MWh / 1000 = 10000 EUR
        assert _F["mh686_incentivo"](
            100000.0, 100.0) == pytest.approx(10000.0,
                                              rel=1e-12)

    def test_incentivo_zero_se_tariffa_zero(self):
        assert _F["mh686_incentivo"](COND_DEMO, 0.0) == 0.0

    def test_incentivo_rifiuta_tariffa_negativa(self):
        with pytest.raises(ValueError):
            _F["mh686_incentivo"](COND_DEMO, -0.01)

    def test_vendita_demo(self):
        assert _F["mh686_vendita"](
            ECC_DEMO, 80.0) == pytest.approx(VEND_DEMO,
                                             rel=REL)

    def test_vendita_formula_mwh(self):
        assert _F["mh686_vendita"](
            100000.0, 100.0) == pytest.approx(10000.0,
                                              rel=1e-12)

    def test_vendita_zero_se_prezzo_zero(self):
        assert _F["mh686_vendita"](ECC_DEMO, 0.0) == 0.0

    def test_vendita_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_vendita"](ECC_DEMO, -0.01)

    def test_ricavo_tot_demo(self):
        assert _F["mh686_ricavo_tot"](
            INC_DEMO, VEND_DEMO) == pytest.approx(
            RIC_DEMO, rel=REL)

    def test_opex_tot_demo(self):
        assert _F["mh686_opex_tot"](
            200.0, 20.0) == pytest.approx(OPEX_DEMO, rel=REL)

    def test_opex_tot_zero_se_unitario_zero(self):
        assert _F["mh686_opex_tot"](200.0, 0.0) == 0.0

    def test_opex_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh686_opex_tot"](200.0, -0.01)
        with pytest.raises(ValueError):
            _F["mh686_opex_tot"](-200.0, 20.0)

    def test_risparmio_demo(self):
        assert _F["mh686_risparmio"](
            RIC_DEMO, OPEX_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh686_risparmio"](100.0, 250.0) == -150.0

    def test_capex_tot_demo(self):
        assert _F["mh686_capex_tot"](
            200.0, 1100.0) == pytest.approx(CAPEX_DEMO,
                                            rel=REL)

    def test_capex_tot_zero_se_unitario_zero(self):
        assert _F["mh686_capex_tot"](200.0, 0.0) == 0.0

    def test_capex_tot_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh686_capex_tot"](0.0, 1100.0)

    def test_capex_tot_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_capex_tot"](200.0, -1.0)

    def test_co2_demo(self):
        assert _F["mh686_co2_evitata"](
            PROD_DEMO, 0.35) == pytest.approx(CO2_DEMO,
                                              rel=REL)

    def test_co2_formula(self):
        # 1000000 kWh x 0,35 kg/kWh / 1000 = 350 t
        assert _F["mh686_co2_evitata"](
            1000000.0, 0.35) == pytest.approx(350.0,
                                             rel=1e-12)

    def test_co2_zero_se_fattore_zero(self):
        assert _F["mh686_co2_evitata"](PROD_DEMO, 0.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_co2_evitata"](PROD_DEMO, -0.01)

    def test_crf_demo(self):
        assert _F["mh686_crf"](
            0.05, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh686_crf"](
            0.0, 20) == pytest.approx(1.0 / 20.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_crf"](-0.01, 20)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh686_crf"](0.05, 0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh686_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh686_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + RISP_DEMO * 20 == pytest.approx(
            170400.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh686_van"](RISP_DEMO, -1.0, 0.05, 20)

    def test_tir_demo(self):
        assert _F["mh686_tir"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh686_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh686_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh686_tir"](0.0, RISP_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh686_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh686_payback"](
            CAPEX_DEMO, RISP_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_ceil_arrotonda_su(self):
        # 1000 / 300 = 3,33... -> 4
        assert _F["mh686_payback"](1000.0, 300.0, 20) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh686_payback"](1000.0, 1000.0, 20) == 1
        assert _F["mh686_payback"](1000.0, 2000.0, 20) == 1

    def test_payback_oltre_vita_ceil_puro(self):
        # ceil puro senza tetto di vita: 220000/100 = 2200
        assert _F["mh686_payback"](CAPEX_DEMO, 100.0, 20) == 2200

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh686_payback"](0.0, RISP_DEMO, 20) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh686_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh686_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, RISP_DEMO,
            PROD_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh686_verdetto"](
            -5000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            PROD_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh686_verdetto"](
            -50000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            PROD_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh686_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            PROD_DEMO) == "NON_CALCOLABILE"
        assert _F["mh686_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0,
            PROD_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_produzione_zero(self):
        assert _F["mh686_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, RISP_DEMO,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh686_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) == "CONVIENTE"
        assert _F["mh686_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh686_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh686_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO,
            PROD_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh686_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 RISP_DEMO, PROD_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh686_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 RISP_DEMO, PROD_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh686_demo"]()
        d.update(kw)
        return _F["mh686_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["produzione_kwh"] == pytest.approx(PROD_DEMO,
                                                    rel=REL)
        assert c["condivisa_kwh"] == pytest.approx(COND_DEMO,
                                                   rel=REL)
        assert c["eccedente_kwh"] == pytest.approx(ECC_DEMO,
                                                   rel=REL)
        assert c["incentivo_eur"] == pytest.approx(INC_DEMO,
                                                   rel=REL)
        assert c["vendita_eur"] == pytest.approx(VEND_DEMO,
                                                 rel=REL)
        assert c["ricavo_tot_eur"] == pytest.approx(RIC_DEMO,
                                                    rel=REL)
        assert c["opex_tot_eur"] == pytest.approx(OPEX_DEMO,
                                                  rel=REL)
        assert c["risparmio_eur"] == pytest.approx(RISP_DEMO,
                                                   rel=REL)
        assert c["capex_tot_eur"] == pytest.approx(CAPEX_DEMO,
                                                   rel=REL)
        assert c["co2_evitata_t"] == pytest.approx(CO2_DEMO,
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
        """mh686_calcola(**mh686_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh686_demo"]()
        b = _F["mh686_calcola"](**d)
        coppie = [("produzione_kwh", PROD_DEMO),
                  ("condivisa_kwh", COND_DEMO),
                  ("eccedente_kwh", ECC_DEMO),
                  ("incentivo_eur", INC_DEMO),
                  ("vendita_eur", VEND_DEMO),
                  ("ricavo_tot_eur", RIC_DEMO),
                  ("opex_tot_eur", OPEX_DEMO),
                  ("risparmio_eur", RISP_DEMO),
                  ("capex_tot_eur", CAPEX_DEMO),
                  ("co2_evitata_t", CO2_DEMO),
                  ("crf", CRF_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh686_demo"]()
        assert d["potenza_kwp"] == 200.0
        assert d["yield_kwh_kwp_a"] == 1200.0
        assert d["consumo_kwh_a"] == 300000.0
        assert d["sync_frac"] == 0.60
        assert d["tariffa_premio_eur_mwh"] == 110.0
        assert d["prezzo_vendita_eur_mwh"] == 80.0
        assert d["capex_eur_kwp"] == 1100.0
        assert d["opex_eur_kwp_a"] == 20.0
        assert d["fattore_co2_kg_kwh"] == 0.35
        assert d["vita_anni"] == 20
        assert d["wacc"] == 0.05
        assert d["tol_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("produzione_kwh", "condivisa_kwh",
                       "eccedente_kwh", "incentivo_eur",
                       "vendita_eur", "ricavo_tot_eur",
                       "opex_tot_eur", "risparmio_eur",
                       "capex_tot_eur", "co2_evitata_t",
                       "crf", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 12" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_kwp=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["produzione_kwh"] == 0.0
        assert n["risparmio_eur"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_kwp=-5.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_yield_zero_neutro(self):
        n = self._bc(yield_kwh_kwp_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_sync_oltre_uno_neutro(self):
        n = self._bc(sync_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_sync_negativo_neutro(self):
        n = self._bc(sync_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_sync_zero_calcolabile_solo_vendita(self):
        # sync 0: condivisa 0, tutto venduto a 80
        # EUR/MWh: ricavo 19200, risparmio 15200
        n = self._bc(sync_frac=0.0)
        assert n["valid"] is True
        assert n["condivisa_kwh"] == 0.0
        assert n["eccedente_kwh"] == pytest.approx(
            PROD_DEMO, rel=REL)
        assert n["risparmio_eur"] == pytest.approx(
            15200.0, rel=REL)

    def test_consumo_zero_calcolabile_solo_vendita(self):
        n = self._bc(consumo_kwh_a=0.0)
        assert n["valid"] is True
        assert n["condivisa_kwh"] == 0.0
        assert n["risparmio_eur"] == pytest.approx(
            15200.0, rel=REL)

    def test_consumo_negativo_neutro(self):
        n = self._bc(consumo_kwh_a=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_negativi_neutro(self):
        for k in ("tariffa_premio_eur_mwh",
                  "prezzo_vendita_eur_mwh",
                  "fattore_co2_kg_kwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_opex_capex_negativi_neutro(self):
        for k in ("opex_eur_kwp_a", "capex_eur_kwp"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=19.5)
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
        n = self._bc(tariffa_premio_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(potenza_kwp=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_zero_risparmio_negativo_neutro(self):
        # tariffa 0 e prezzo 0: ricavo 0 < OPEX 4000
        n = self._bc(tariffa_premio_eur_mwh=0.0,
                     prezzo_vendita_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -220000 + 19520 x 20 = 170400
        n = self._bc(wacc=0.0)
        assert n["van"] == pytest.approx(170400.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_kwp=0.0)
        assert n["capex_tot_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh686_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh686_neutro"]()
        for chiave in ("valid", "produzione_kwh",
                       "condivisa_kwh", "eccedente_kwh",
                       "incentivo_eur", "vendita_eur",
                       "ricavo_tot_eur", "opex_tot_eur",
                       "risparmio_eur", "capex_tot_eur",
                       "co2_evitata_t", "crf", "van",
                       "tir", "payback", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 12
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Produzione (kWh/anno)" in voci
        assert "Energia condivisa (kWh/anno)" in voci
        assert "Eccedente (kWh/anno)" in voci
        assert "Incentivo (EUR/anno)" in voci
        assert "Vendita eccedente (EUR/anno)" in voci
        assert "Ricavo totale (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
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
        return _F["mh686_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh686_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Sync x0.8",
                                   "Sync x1.0",
                                   "Sync x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh686_sensitivita"](self._ing())
        assert s.loc["x1.0", "Sync x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        s = _F["mh686_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Sync x1.0"]
        assert s.loc["x0.8", "Sync x0.8"] < centro
        assert s.loc["x1.0", "Sync x0.8"] < centro
        assert s.loc["x1.2", "Sync x1.0"] > centro
        assert s.loc["x0.8", "Sync x1.0"] < centro
        assert s.loc["x1.2", "Sync x1.2"] > centro

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi restano nel dominio
        # valido (tariffa senza tetto, sync con
        # tetto a 1.0): nessuna cella puo'
        # essere 0,0 per regime degenere sulla demo
        s = _F["mh686_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_crescente_in_entrambi_i_fattori(self):
        s = _F["mh686_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "Sync x0.8"] < \
                s.loc[riga, "Sync x1.0"] < \
                s.loc[riga, "Sync x1.2"]
        for colonna in ("Sync x0.8",
                        "Sync x1.0",
                        "Sync x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_assi_senza_colonna_degenere(self):
        # la griglia resta 3x3 anche con sync alto:
        # il tetto a 1.0 evita la colonna degenere
        ing = self._ing()
        ing["sync_frac"] = 1.0
        s = _F["mh686_sensitivita"](ing)
        assert s.shape == (3, 3)
        assert len(set(s.index)) == 3
        # con sync = 1.0 le colonne x1.0 e x1.2
        # coincidono (tetto), ma restano valide
        assert s.loc["x1.0", "Sync x1.0"] == \
            s.loc["x1.0", "Sync x1.2"]

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh686_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 27

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh686_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_anno" in txt
        assert "condivisa_kwh_anno" in txt
        assert "incentivo_eur_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "produzione_kwh_anno" in txt
        assert "risparmio_eur_anno" in txt
        assert "tariffa_premio_eur_mwh" in txt
        assert "sync_frac" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh686_csv"](bc, self._ing())
        assert f"produzione_kwh_anno;{PROD_DEMO}" in txt
        assert f"condivisa_kwh_anno;{COND_DEMO}" in txt
        assert f"risparmio_eur_anno;{RISP_DEMO}" in txt
        assert f"capex_tot_eur;{CAPEX_DEMO}" in txt
        assert f"co2_evitata_t_anno;{CO2_DEMO}" in txt
        assert f"ricavo_tot_eur_anno;{RIC_DEMO}" in txt
        assert f"incentivo_eur_anno;{INC_DEMO}" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def686["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def686\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 12, ui_keys
        demo_keys = set(_F["mh686_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W686 (24/10/2026) - tab686' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh686_num", "mh686_nneg", "mh686_pos",
                     "mh686_int_pos", "mh686_tol",
                     "mh686_produzione", "mh686_condivisa",
                     "mh686_eccedente", "mh686_incentivo",
                     "mh686_vendita", "mh686_ricavo_tot",
                     "mh686_opex_tot", "mh686_risparmio",
                     "mh686_capex_tot", "mh686_co2_evitata",
                     "mh686_crf",
                     "mh686_van", "mh686_tir",
                     "mh686_payback", "mh686_verdetto",
                     "_mh686_neutro", "mh686_calcola",
                     "mh686_sensitivita", "mh686_csv",
                     "mh686_demo", "demo_calcoli"):
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
        # l'apply (come w685_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w686_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE686) == 1

    def test_blocco_with_tab686(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab686:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE686

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st686_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 17, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st685_") for k in keys)
        assert not any(k.startswith("st684_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg686" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg686") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg686")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Produzione (MWh/anno)" in src
        assert "Energia condivisa (MWh/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd686" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_cer_presente(self):
        src = _ui_src()
        assert "contemporane" in src.lower()
        assert "premio" in src.lower()
        assert "eccedente" in src.lower()
        assert "comunit" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Incentivo energia condivisa" in src
        assert "Risparmio annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh686_csv" in src
        assert "cer_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh686_sensitivita" in src
        assert "Heatmap" in src
        assert "Tariffa premio" in src
        assert "contemporane" in src.lower()

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st686_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W686 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab686:")
        assert "mh686_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab686" in (_new_dir() / "w686_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w686_helpers.py", "w686_ui.py",
                   "w686_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab685" not in src
        assert "tab684" not in src
        assert "tab683" not in src
