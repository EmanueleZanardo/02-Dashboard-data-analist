"""Test tab733 "💧❄️ Idrogeno liquido (LH2): la liquefazione paga?"

Nuova tab tab733 (idrogeno liquido da
liquefazione H2, w734).
Business case deterministico di un impianto
di liquefazione: H2 in ingresso da portata
e giorni, energia di liquefazione da
consumo specifico, costo energia, LH2
venduto dopo il boil-off, CAPEX, costi
annui, ricavo, netto, VAN, TIR, payback,
LCOE, margine sul prezzo, CO2 evitata e
verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
portata 5000 kg/giorno; giorni anno 330
giorni/anno; consumo liquefazione 11
kWh/kg; boil-off 0,03; prezzo elettricita'
0,08 EUR/kWh; CAPEX 4000 EUR/(kg/giorno);
opex variabile 0,30 EUR/kg; opex fisso
300000 EUR/anno; prezzo LH2 5,00 EUR/kg;
diesel sostituito 3,0 L/kg; CO2 diesel
2,68 kg/L; fattore rete 0,35 kg/kWh; WACC
0,05 (5 %); vita 20 anni; tolleranza 0,10
(10 % del CAPEX).

- h2_in_kg_anno = 1650000.0
- energia_liquef_kWh = 18150000.0
- costo_energia_EUR = 1452000.0
- lh2_venduto_kg = 1600500.0
- capex_EUR = 20000000.0
- costi_annui_EUR = 2247000.0
- ricavo_EUR_anno = 8002500.0
- netto_EUR_anno = 5755500.0
- van = 51726251.626488864
- tir = 28.58914958588973
- payback = 4
- lcoe_EUR_kg = 2.0287410184317403
- margine_EUR_kg = 2.9712589815682597
- co2_evitata_t_anno = 6515.52
- verdetto = 'CONVIENTE'

Scomposizione: H2 in 5000 x 330 =
1.650.000 kg/anno; energia 1.650.000 x 11
= 18.150.000 kWh/anno; costo energia
18.150.000 x 0,08 = 1.452.000 EUR/anno;
LH2 venduto 1.650.000 x 0,97 = 1.600.500
kg/anno; CAPEX 5000 x 4000 = 20.000.000
EUR; costi annui 1.452.000 + 1.650.000 x
0,30 + 300.000 = 2.247.000 EUR/anno;
ricavo 1.600.500 x 5 = 8.002.500 EUR/anno;
netto 8.002.500 - 2.247.000 = 5.755.500
EUR/anno; flussi: anno 0 -20.000.000,
anni 1-20 netto 5.755.500 (piatti); VAN
-20.000.000 + 5.755.500 x 12,4622103416
(annuita' 20 anni al 5 %) =
51726251.626488864 EUR; TIR
28.58914958588973 % (il tasso che azzera
il VAN dei flussi); payback 4 (il
cumulato supera lo zero al quarto anno:
-20.000.000 + 4 x 5.755.500 =
3.022.000); LCOE (20.000.000 / 20 +
2.247.000) / 1.600.500 =
2.0287410184317403 EUR/kg; margine 5 -
2.0287410184317403 = 2.9712589815682597
EUR/kg; CO2 evitata (1.600.500 x 3,0 x
2,68 - 18.150.000 x 0,35) / 1000 = 6515.52
t/anno; verdetto CONVIENTE perche' VAN >
0.
"""

import ast
import re
from pathlib import Path
import sys
import textwrap

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w734_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w734_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w734_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w734_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w734_helpers.py: {missing}")
    return out


_F = _load("mh733_num", "mh733_nneg", "mh733_pos",
           "mh733_int_pos", "mh733_frac_01",
           "mh733_frac_boil", "mh733_frac_toll",
           "mh733_h2_in", "mh733_energia_liquef",
           "mh733_costo_energia", "mh733_lh2_venduto",
           "mh733_capex",
           "mh733_costi", "mh733_ricavo",
           "mh733_netto", "mh733_flussi",
           "mh733_van", "mh733_tir", "mh733_payback",
           "mh733_lcoe", "mh733_margine",
           "mh733_co2_evitata", "mh733_verdetto",
           "mh733_valida", "_mh733_neutro",
           "mh733_calcola", "mh733_csv",
           "mh733_demo", "demo_calcoli")

TITLE733 = ("💧❄️ Idrogeno liquido (LH2): "
            "la liquefazione paga?")

H2_IN_DEMO = 1650000.0
ENE_DEMO = 18150000.0
COSTO_ENE_DEMO = 1452000.0
LH2_DEMO = 1600500.0
CAPEX_DEMO = 20000000.0
COSTI_DEMO = 2247000.0
RICAVO_DEMO = 8002500.0
NETTO_DEMO = 5755500.0
VAN_DEMO = 51726251.626488864
TIR_DEMO = 28.58914958588973
PAYBACK_DEMO = 4
LCOE_DEMO = 2.0287410184317403
MARGINE_DEMO = 2.9712589815682597
CO2_DEMO = 6515.52
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "portata_kg_giorno": 5000.0,
    "giorni_anno": 330,
    "consumo_kWh_per_kg": 11.0,
    "boiloff_frazione": 0.03,
    "prezzo_el_EUR_kWh": 0.08,
    "capex_EUR_per_kg_giorno": 4000.0,
    "opex_var_EUR_kg": 0.30,
    "opex_fisso_EUR_anno": 300000.0,
    "prezzo_lh2_EUR_kg": 5.00,
    "diesel_L_per_kg": 3.0,
    "co2_diesel_kg_per_L": 2.68,
    "fattore_rete_kg_kWh": 0.35,
    "wacc_frac": 0.05,
    "vita_anni": 20,
    "tolleranza_frac": 0.10,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w734_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w734_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh733_demo"]()
        d.update(kw)
        return _F["mh733_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh733_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh733_num"]("5000", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh733_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh733_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh733_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh733_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh733_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh733_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh733_int_pos"](20.0, "x") == 20

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh733_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh733_frac_01"](1.0, "x")

    def test_frac_boil_accetta_zero_rifiuta_uno_e_oltre(self):
        assert _F["mh733_frac_boil"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh733_frac_boil"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh733_frac_boil"](1.01, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh733_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh733_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh733_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_portata_zero_e_negativa_non_valide(self):
        assert self._val(portata_kg_giorno=0.0)["valido"] is False
        assert self._val(portata_kg_giorno=-1.0)["valido"] is False

    def test_giorni_zero_frazione_e_oltre_365_non_validi(self):
        assert self._val(giorni_anno=0)["valido"] is False
        assert self._val(giorni_anno=330.5)["valido"] is False
        assert self._val(giorni_anno=366)["valido"] is False
        assert self._val(giorni_anno=365)["valido"] is True

    def test_boiloff_uno_e_oltre_non_validi_zero_valido(self):
        assert self._val(boiloff_frazione=1.0)["valido"] is False
        assert self._val(boiloff_frazione=1.01)["valido"] is False
        assert self._val(boiloff_frazione=0.0)["valido"] is True

    def test_consumo_zero_e_negativo_non_validi(self):
        assert self._val(consumo_kWh_per_kg=0.0)["valido"] is False
        assert self._val(consumo_kWh_per_kg=-1.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_EUR_kWh",
                  "capex_EUR_per_kg_giorno",
                  "opex_var_EUR_kg",
                  "opex_fisso_EUR_anno",
                  "prezzo_lh2_EUR_kg",
                  "diesel_L_per_kg",
                  "co2_diesel_kg_per_L",
                  "fattore_rete_kg_kWh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=20.5)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.05)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(portata_kg_giorno=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(portata_kg_giorno=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(portata_kg_giorno="5000")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_lh2_EUR_kg=0.0)["valido"] is True
        assert self._val(capex_EUR_per_kg_giorno=0.0)["valido"] is True
        assert self._val(fattore_rete_kg_kWh=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(boiloff_frazione=0.0)["valido"] is True


class TestFunzioni:
    def test_h2_in_demo(self):
        assert _F["mh733_h2_in"](
            5000.0, 330) == pytest.approx(
            H2_IN_DEMO, rel=REL)

    def test_h2_in_rifiuta_oltre_365(self):
        with pytest.raises(ValueError):
            _F["mh733_h2_in"](5000.0, 366)

    def test_energia_liquef_demo(self):
        assert _F["mh733_energia_liquef"](
            H2_IN_DEMO, 11.0) == pytest.approx(
            ENE_DEMO, rel=REL)

    def test_energia_formula_letterale(self):
        assert _F["mh733_energia_liquef"](
            1000.0, 11.0) == pytest.approx(11000.0, rel=REL)

    def test_energia_rifiuta_consumo_zero(self):
        with pytest.raises(ValueError):
            _F["mh733_energia_liquef"](H2_IN_DEMO, 0.0)

    def test_costo_energia_demo(self):
        assert _F["mh733_costo_energia"](
            ENE_DEMO, 0.08) == pytest.approx(
            COSTO_ENE_DEMO, rel=REL)

    def test_lh2_venduto_demo(self):
        assert _F["mh733_lh2_venduto"](
            H2_IN_DEMO, 0.03) == pytest.approx(
            LH2_DEMO, rel=REL)

    def test_lh2_venduto_boiloff_zero(self):
        assert _F["mh733_lh2_venduto"](
            H2_IN_DEMO, 0.0) == pytest.approx(
            H2_IN_DEMO, rel=REL)

    def test_lh2_venduto_rifiuta_boiloff_uno(self):
        with pytest.raises(ValueError):
            _F["mh733_lh2_venduto"](H2_IN_DEMO, 1.0)

    def test_capex_demo(self):
        assert _F["mh733_capex"](
            5000.0, 4000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_formula_indipendente(self):
        assert _F["mh733_capex"](
            1000.0, 4000.0) == pytest.approx(
            4000000.0, rel=REL)

    def test_costi_demo(self):
        assert _F["mh733_costi"](
            COSTO_ENE_DEMO, H2_IN_DEMO, 0.30,
            300000.0) == pytest.approx(COSTI_DEMO, rel=REL)

    def test_costi_solo_fisso(self):
        assert _F["mh733_costi"](
            0.0, H2_IN_DEMO, 0.0,
            300000.0) == pytest.approx(300000.0, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh733_ricavo"](
            LH2_DEMO, 5.00) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh733_netto"](
            RICAVO_DEMO, COSTI_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh733_netto"](
            1000.0, COSTI_DEMO) == pytest.approx(
            -2246000.0, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh733_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh733_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        assert abs(_F["mh733_van"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh733_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 20
        assert _F["mh733_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh733_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh733_flussi"](CAPEX_DEMO, -1000.0, 20)
        assert _F["mh733_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh733_tir"](
            [0.0] + [NETTO_DEMO] * 20) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh733_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh733_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh733_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh733_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        tir = _F["mh733_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh733_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        assert _F["mh733_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh733_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh733_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh733_payback"](
            [-1000000000.0] + [NETTO_DEMO] * 20) is None

    def test_lcoe_demo(self):
        assert _F["mh733_lcoe"](
            CAPEX_DEMO, 20, COSTI_DEMO,
            LH2_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_none_se_lh2_zero(self):
        assert _F["mh733_lcoe"](
            20000000.0, 20, 2247000.0, 0.0) is None

    def test_lcoe_formula_indipendente(self):
        assert _F["mh733_lcoe"](
            120000.0, 10, 5000.0,
            1000.0) == pytest.approx(
            (12000.0 + 5000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh733_margine"](
            5.00, LCOE_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcoe_none(self):
        assert _F["mh733_margine"](5.00, None) is None

    def test_co2_demo(self):
        assert _F["mh733_co2_evitata"](
            LH2_DEMO, 3.0, 2.68, ENE_DEMO,
            0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_rete_sporca_puo_essere_negativa(self):
        assert _F["mh733_co2_evitata"](
            LH2_DEMO, 0.0, 2.68, ENE_DEMO,
            0.35) == pytest.approx(
            -ENE_DEMO * 0.35 / 1000.0, rel=REL)

    def test_co2_fattore_zero(self):
        assert _F["mh733_co2_evitata"](
            LH2_DEMO, 3.0, 2.68, ENE_DEMO,
            0.0) == pytest.approx(
            LH2_DEMO * 3.0 * 2.68 / 1000.0, rel=REL)

    def test_verdetto_demo(self):
        assert _F["mh733_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, LH2_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh733_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, LH2_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh733_verdetto"](
            0.0, CAPEX_DEMO, 0.10, LH2_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh733_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            LH2_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh733_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            LH2_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh733_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, LH2_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_lh2_zero(self):
        assert _F["mh733_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh733_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, LH2_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh733_demo"]()
        d.update(kw)
        return _F["mh733_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["h2_in_kg_anno"] == pytest.approx(
            H2_IN_DEMO, rel=REL)
        assert c["energia_liquef_kWh"] == pytest.approx(
            ENE_DEMO, rel=REL)
        assert c["costo_energia_EUR"] == pytest.approx(
            COSTO_ENE_DEMO, rel=REL)
        assert c["lh2_venduto_kg"] == pytest.approx(
            LH2_DEMO, rel=REL)
        assert c["capex_EUR"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["costi_annui_EUR"] == pytest.approx(
            COSTI_DEMO, rel=REL)
        assert c["ricavo_EUR_anno"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["netto_EUR_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["lcoe_EUR_kg"] == pytest.approx(
            LCOE_DEMO, rel=REL)
        assert c["margine_EUR_kg"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 21

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcoe_EUR_kg"] == \
            _F["demo_calcoli"]()["lcoe_EUR_kg"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh733_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 15

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("h2_in_kg_anno",
                       "energia_liquef_kWh",
                       "costo_energia_EUR",
                       "lh2_venduto_kg",
                       "capex_EUR",
                       "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno",
                       "van",
                       "tir",
                       "lcoe_EUR_kg",
                       "margine_EUR_kg",
                       "co2_evitata_t_anno"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 4" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_235_marginale(self):
        # Prezzo 2,35 EUR/kg: netto 1.514.175
        # EUR/anno, VAN circa -1.130.033 EUR,
        # entro la tolleranza 10 % di
        # 20.000.000 = 2.000.000 -> MARGINALE.
        n = self._bc(prezzo_lh2_EUR_kg=2.35)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert -2000000.0 < n["van"] < 0.0

    def test_prezzo_203_non_conviente(self):
        # Prezzo 2,03 EUR/kg: netto 1.002.015
        # EUR/anno, VAN circa -7.512.678 EUR,
        # oltre la tolleranza 2.000.000 EUR
        # -> NON_CONVIENTE.
        n = self._bc(prezzo_lh2_EUR_kg=2.03)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -2000000.0

    def test_prezzo_zero_non_conviente(self):
        # Prezzo 0: ricavo zero, netto negativo
        # pari a -costi annui, VAN negativa oltre
        # tolleranza -> NON_CONVIENTE.
        n = self._bc(prezzo_lh2_EUR_kg=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero e prezzo 5: tutti i flussi
        # >= 0 -> TIR None, payback 0, VAN
        # positiva -> CONVIENTE.
        n = self._bc(capex_EUR_per_kg_giorno=0.0)
        assert n["valid"] is True
        assert n["capex_EUR"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_boiloff_zero_lh2_uguale_h2_in(self):
        n = self._bc(boiloff_frazione=0.0)
        assert n["valid"] is True
        assert n["lh2_venduto_kg"] == pytest.approx(
            H2_IN_DEMO, rel=REL)

    def test_portata_zero_neutro(self):
        n = self._bc(portata_kg_giorno=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoe_EUR_kg"] is None

    def test_giorni_zero_neutro(self):
        n = self._bc(giorni_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_oltre_365_neutro(self):
        n = self._bc(giorni_anno=366)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_consumo_zero_neutro(self):
        n = self._bc(consumo_kWh_per_kg=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_boiloff_uno_neutro(self):
        n = self._bc(boiloff_frazione=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_e_uno_neutri(self):
        assert self._bc(wacc_frac=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=1.0)["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(portata_kg_giorno=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_EUR_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(portata_kg_giorno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(portata_kg_giorno="5000")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_EUR_per_kg_giorno=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh733_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi"] == []
        assert n["tir"] is None
        assert n["payback"] is None
        assert n["lcoe_EUR_kg"] is None
        assert n["margine_EUR_kg"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh733_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "portata_kg_giorno", "giorni_anno",
                       "consumo_kWh_per_kg",
                       "boiloff_frazione",
                       "prezzo_el_EUR_kWh",
                       "capex_EUR_per_kg_giorno",
                       "opex_var_EUR_kg",
                       "opex_fisso_EUR_anno",
                       "prezzo_lh2_EUR_kg",
                       "diesel_L_per_kg",
                       "co2_diesel_kg_per_L",
                       "fattore_rete_kg_kWh",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "h2_in_kg_anno",
                       "energia_liquef_kWh",
                       "costo_energia_EUR",
                       "lh2_venduto_kg",
                       "capex_EUR", "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno", "flussi", "van",
                       "tir", "payback", "lcoe_EUR_kg",
                       "margine_EUR_kg",
                       "co2_evitata_t_anno", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 30
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia liquefazione (kWh/anno)" in voci
        assert "Costo energia (EUR/anno)" in voci
        assert "LH2 venduto (kg/anno)" in voci
        assert "H2 in ingresso (kg/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOE (EUR/kg)" in voci
        assert "Margine (EUR/kg)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 21
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh733_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh733_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 31

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh733_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_EUR" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcoe_EUR_kg" in txt
        assert "margine_EUR_kg" in txt
        assert "co2_evitata_t_anno" in txt
        assert "portata_kg_giorno" in txt
        assert "energia_liquef_kWh" in txt
        assert "lh2_venduto_kg" in txt
        assert "costo_energia_EUR" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh733_csv"](bc, self._ing())
        assert f"netto_EUR_anno;{bc['netto_EUR_anno']}" in txt
        assert f"energia_liquef_kWh;{bc['energia_liquef_kWh']}" in txt
        assert "portata_kg_giorno;5000.0" in txt
        assert "capex_EUR_per_kg_giorno;4000.0" in txt
        assert f"lcoe_EUR_kg;{bc['lcoe_EUR_kg']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def733["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def733\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh733_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh733_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh733_demo():")
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
        ui_keys = set(re.findall(r'_def733\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W734 (26/10/2026) - tab733' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh733_num", "mh733_nneg", "mh733_pos",
                     "mh733_int_pos", "mh733_frac_01",
                     "mh733_frac_boil", "mh733_frac_toll",
                     "mh733_h2_in", "mh733_energia_liquef",
                     "mh733_costo_energia", "mh733_lh2_venduto",
                     "mh733_capex", "mh733_costi",
                     "mh733_ricavo", "mh733_netto",
                     "mh733_flussi", "mh733_van",
                     "mh733_tir", "mh733_payback",
                     "mh733_lcoe", "mh733_margine",
                     "mh733_co2_evitata", "mh733_verdetto",
                     "mh733_valida", "_mh733_neutro",
                     "mh733_calcola", "mh733_csv",
                     "mh733_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_732(self):
        assert "mh732" not in _helpers_src()
        assert "mh732" not in _ui_src()
        assert "st732" not in _ui_src()
        assert "tab732" not in _ui_src()
        assert "W733" not in _helpers_src()
        assert "W733" not in _ui_src()
        assert "mh733" in _helpers_src()
        assert "st733" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w734_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE733) == 1

    def test_blocco_with_tab733(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab733:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE733

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st733_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 18, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st733_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st733_[a-z0-9_]+)"', _ui_src())
        attese = ["st733_portata", "st733_giorni",
                  "st733_consumo", "st733_boiloff",
                  "st733_capex", "st733_opex_var",
                  "st733_opex_fisso", "st733_prezzo_el",
                  "st733_prezzo_lh2", "st733_diesel",
                  "st733_co2", "st733_fattore",
                  "st733_vita", "st733_wacc",
                  "st733_tolleranza", "st733_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg733" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg733") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg733")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOE (EUR/kg)" in src
        assert "Margine (EUR/kg)" in src
        assert "VAN (EUR)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "Trasporto H2" in src
        assert "ammoniaca" in src
        assert "metanolo" in src
        assert "biometano" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "Trasporto H2" in src
        assert "ammoniaca" in src
        assert "metanolo" in src
        assert "biometano" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "1.650.000" in src
        assert "1.600.500" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati733" in src
        assert '"EUR/kg"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh733_csv" in src
        assert "lh2.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st733_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W734 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab733:")
