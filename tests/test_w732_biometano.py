"""Test tab732 "🌿⛽ Biometano da upgrading del biogas: il metano pulito paga?"

Nuova tab tab732 (biometano da upgrading
del biogas, w733).
Business case di un impianto di upgrading:
biogas annuo da portata e ore, CH4 grezzo
da frazione CH4, biometano da recupero di
metano, slip, energia con PCI CH4 9,94
kWh/Nm3, CAPEX, costi annui, ricavo,
netto, VAN, TIR, payback, LCOE, margine
sul prezzo, CO2 evitata e verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
portata biogas 500 Nm3/h; frazione CH4
0,55; ore anno 8000 ore/anno; recupero
metano 0,98; CAPEX 1200 EUR/(Nm3/h);
costo upgrading 0,06 EUR/Nm3; O&M fisso
50000 EUR/anno; prezzo biometano 90
EUR/MWh; fattore gas 0,20 kg/kWh; WACC
0,05 (5 %); vita 15 anni; tolleranza 0,10
(10 % del CAPEX).

- biogas_Nm3_anno = 4000000.0
- ch4_grezzo_Nm3 = 2200000.0
- biometano_Nm3 = 2156000.0
- slip_Nm3 = 44000.0
- energia_kWh = 21430640.0
- energia_MWh = 21430.64
- capex_EUR = 600000.0
- costi_annui_EUR = 290000.0
- ricavo_EUR_anno = 1928757.5999999999
- netto_EUR_anno = 1638757.5999999999
- van = 16409743.495469531
- tir = 273.12626594465365
- payback = 1
- lcoe_EUR_MWh = 15.398513530160555
- margine_EUR_MWh = 74.60148646983944
- co2_evitata_t_anno = 4286.128
- verdetto = 'CONVIENTE'

Scomposizione: biogas 500 x 8000 =
4.000.000 Nm3/anno; CH4 grezzo 4.000.000
x 0,55 = 2.200.000 Nm3/anno; biometano
2.200.000 x 0,98 = 2.156.000 Nm3/anno;
slip 2.200.000 - 2.156.000 = 44.000
Nm3/anno; energia 2.156.000 x 9,94 =
21.430.640 kWh/anno = 21.430,64 MWh/anno;
CAPEX 500 x 1200 = 600.000 EUR; costi
annui 4.000.000 x 0,06 + 50.000 = 290.000
EUR/anno; ricavo 21.430,64 x 90 =
1.928.757,6 EUR/anno; netto 1.928.757,6 -
290.000 = 1.638.757,6 EUR/anno; flussi:
anno 0 -600.000, anni 1-15 netto
1.638.757,6 (piatti); VAN -600.000 +
1.638.757,6 x 10,37965803818059
(annuita' 15 anni al 5 %) =
16409743.495469531 EUR; TIR
273.12626594465365 % (il tasso che azzera
il VAN dei flussi); payback 1 (il
cumulato supera lo zero al primo anno:
-600.000 + 1.638.757,6 =
1.038.757,6); LCOE (600.000 / 15 +
290.000) / 21.430,64 = 15.398513530160555
EUR/MWh; margine 90 - 15.398513530160555
= 74.60148646983944 EUR/MWh; CO2 evitata
21.430.640 x 0,20 / 1000 = 4286.128
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
    if (p / "w733_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w733_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w733_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w733_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w733_helpers.py: {missing}")
    return out


_F = _load("mh732_num", "mh732_nneg", "mh732_pos",
           "mh732_int_pos", "mh732_frac_01",
           "mh732_frac_rec", "mh732_frac_toll",
           "mh732_biogas", "mh732_ch4_grezzo",
           "mh732_biometano", "mh732_slip",
           "mh732_energia", "mh732_capex",
           "mh732_costi", "mh732_ricavo",
           "mh732_netto", "mh732_flussi",
           "mh732_van", "mh732_tir", "mh732_payback",
           "mh732_lcoe", "mh732_margine",
           "mh732_co2_evitata", "mh732_verdetto",
           "mh732_valida", "_mh732_neutro",
           "mh732_calcola", "mh732_csv",
           "mh732_demo", "demo_calcoli")

TITLE732 = ("🌿⛽ Biometano da upgrading del biogas: "
            "il metano pulito paga?")

BIOGAS_DEMO = 4000000.0
CH4_DEMO = 2200000.0
BIOMETANO_DEMO = 2156000.0
SLIP_DEMO = 44000.0
ENE_KWH_DEMO = 21430640.0
ENE_MWH_DEMO = 21430.64
CAPEX_DEMO = 600000.0
COSTI_DEMO = 290000.0
RICAVO_DEMO = 1928757.5999999999
NETTO_DEMO = 1638757.5999999999
VAN_DEMO = 16409743.495469531
TIR_DEMO = 273.12626594465365
PAYBACK_DEMO = 1
LCOE_DEMO = 15.398513530160555
MARGINE_DEMO = 74.60148646983944
CO2_DEMO = 4286.128
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "portata_biogas_Nm3h": 500.0,
    "frazione_ch4": 0.55,
    "ore_anno": 8000,
    "recupero_metano": 0.98,
    "capex_EUR_per_Nm3h": 1200.0,
    "costo_upgrading_EUR_Nm3": 0.06,
    "om_fisso_EUR_anno": 50000.0,
    "prezzo_biometano_EUR_MWh": 90.0,
    "fattore_gas_kg_kWh": 0.20,
    "wacc_frac": 0.05,
    "vita_anni": 15,
    "tolleranza_frac": 0.10,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w733_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w733_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh732_demo"]()
        d.update(kw)
        return _F["mh732_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh732_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh732_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh732_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh732_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh732_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh732_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh732_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh732_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh732_int_pos"](15.0, "x") == 15

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh732_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh732_frac_01"](1.0, "x")

    def test_frac_rec_accetta_uno_rifiuta_zero_e_oltre(self):
        assert _F["mh732_frac_rec"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh732_frac_rec"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh732_frac_rec"](1.01, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh732_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh732_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh732_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_portata_zero_e_negativa_non_valide(self):
        assert self._val(portata_biogas_Nm3h=0.0)["valido"] is False
        assert self._val(portata_biogas_Nm3h=-1.0)["valido"] is False

    def test_frazione_zero_uno_e_oltre_non_valide(self):
        assert self._val(frazione_ch4=0.0)["valido"] is False
        assert self._val(frazione_ch4=1.0)["valido"] is False
        assert self._val(frazione_ch4=1.2)["valido"] is False

    def test_ore_zero_frazione_e_oltre_8760_non_valide(self):
        assert self._val(ore_anno=0)["valido"] is False
        assert self._val(ore_anno=8000.5)["valido"] is False
        assert self._val(ore_anno=8761)["valido"] is False
        assert self._val(ore_anno=8760)["valido"] is True

    def test_recupero_zero_e_oltre_uno_non_validi_uno_valido(self):
        assert self._val(recupero_metano=0.0)["valido"] is False
        assert self._val(recupero_metano=1.01)["valido"] is False
        assert self._val(recupero_metano=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("capex_EUR_per_Nm3h",
                  "costo_upgrading_EUR_Nm3",
                  "om_fisso_EUR_anno",
                  "prezzo_biometano_EUR_MWh",
                  "fattore_gas_kg_kWh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=15.5)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.05)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(portata_biogas_Nm3h=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(portata_biogas_Nm3h=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(portata_biogas_Nm3h="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_biometano_EUR_MWh=0.0)["valido"] is True
        assert self._val(capex_EUR_per_Nm3h=0.0)["valido"] is True
        assert self._val(fattore_gas_kg_kWh=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_biogas_demo(self):
        assert _F["mh732_biogas"](
            500.0, 8000) == pytest.approx(
            BIOGAS_DEMO, rel=REL)

    def test_biogas_rifiuta_oltre_8760(self):
        with pytest.raises(ValueError):
            _F["mh732_biogas"](500.0, 8761)

    def test_ch4_grezzo_demo(self):
        assert _F["mh732_ch4_grezzo"](
            BIOGAS_DEMO, 0.55) == pytest.approx(
            CH4_DEMO, rel=REL)

    def test_ch4_rifiuta_frazione_uno(self):
        with pytest.raises(ValueError):
            _F["mh732_ch4_grezzo"](BIOGAS_DEMO, 1.0)

    def test_biometano_demo(self):
        assert _F["mh732_biometano"](
            CH4_DEMO, 0.98) == pytest.approx(
            BIOMETANO_DEMO, rel=REL)

    def test_biometano_recupero_uno(self):
        assert _F["mh732_biometano"](
            CH4_DEMO, 1.0) == pytest.approx(
            CH4_DEMO, rel=REL)

    def test_biometano_rifiuta_recupero_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh732_biometano"](CH4_DEMO, 1.01)

    def test_slip_demo(self):
        assert _F["mh732_slip"](
            CH4_DEMO, BIOMETANO_DEMO) == pytest.approx(
            SLIP_DEMO, rel=REL)

    def test_slip_zero_con_recupero_uno(self):
        assert _F["mh732_slip"](
            CH4_DEMO, CH4_DEMO) == pytest.approx(0.0, abs=1e-9)

    def test_energia_demo(self):
        assert _F["mh732_energia"](
            BIOMETANO_DEMO) == pytest.approx(
            ENE_KWH_DEMO, rel=REL)

    def test_energia_formula_letterale(self):
        assert _F["mh732_energia"](
            1000.0) == pytest.approx(9940.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh732_capex"](
            500.0, 1200.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_formula_indipendente(self):
        assert _F["mh732_capex"](
            1000.0, 1200.0) == pytest.approx(
            1200000.0, rel=REL)

    def test_costi_demo(self):
        assert _F["mh732_costi"](
            BIOGAS_DEMO, 0.06,
            50000.0) == pytest.approx(COSTI_DEMO, rel=REL)

    def test_costi_solo_fisso(self):
        assert _F["mh732_costi"](
            BIOGAS_DEMO, 0.0,
            50000.0) == pytest.approx(50000.0, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh732_ricavo"](
            ENE_MWH_DEMO, 90.0) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh732_netto"](
            RICAVO_DEMO, COSTI_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh732_netto"](
            1000.0, COSTI_DEMO) == pytest.approx(
            -289000.0, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh732_flussi"](CAPEX_DEMO, NETTO_DEMO, 15)
        assert len(flussi) == 16
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh732_flussi"](CAPEX_DEMO, NETTO_DEMO, 15)
        assert abs(_F["mh732_van"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh732_flussi"](CAPEX_DEMO, NETTO_DEMO, 15)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 15
        assert _F["mh732_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh732_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh732_flussi"](CAPEX_DEMO, -1000.0, 15)
        assert _F["mh732_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh732_tir"](
            [0.0] + [NETTO_DEMO] * 15) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh732_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh732_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh732_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh732_flussi"](CAPEX_DEMO, NETTO_DEMO, 15)
        tir = _F["mh732_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh732_flussi"](CAPEX_DEMO, NETTO_DEMO, 15)
        assert _F["mh732_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh732_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh732_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh732_payback"](
            [-1000000000.0] + [NETTO_DEMO] * 15) is None

    def test_lcoe_demo(self):
        assert _F["mh732_lcoe"](
            CAPEX_DEMO, 15, COSTI_DEMO,
            ENE_MWH_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_none_se_energia_zero(self):
        assert _F["mh732_lcoe"](
            600000.0, 15, 290000.0, 0.0) is None

    def test_lcoe_formula_indipendente(self):
        assert _F["mh732_lcoe"](
            120000.0, 10, 5000.0,
            1000.0) == pytest.approx(
            (12000.0 + 5000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh732_margine"](
            90.0, LCOE_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcoe_none(self):
        assert _F["mh732_margine"](90.0, None) is None

    def test_co2_demo(self):
        assert _F["mh732_co2_evitata"](
            ENE_KWH_DEMO, 0.20) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_fattore_zero(self):
        assert _F["mh732_co2_evitata"](
            ENE_KWH_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_verdetto_demo(self):
        assert _F["mh732_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, ENE_KWH_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh732_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, ENE_KWH_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh732_verdetto"](
            0.0, CAPEX_DEMO, 0.10, ENE_KWH_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh732_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            ENE_KWH_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh732_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            ENE_KWH_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh732_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, ENE_KWH_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_energia_zero(self):
        assert _F["mh732_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh732_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, ENE_KWH_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh732_demo"]()
        d.update(kw)
        return _F["mh732_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["biogas_Nm3_anno"] == pytest.approx(
            BIOGAS_DEMO, rel=REL)
        assert c["ch4_grezzo_Nm3"] == pytest.approx(
            CH4_DEMO, rel=REL)
        assert c["biometano_Nm3"] == pytest.approx(
            BIOMETANO_DEMO, rel=REL)
        assert c["slip_Nm3"] == pytest.approx(
            SLIP_DEMO, rel=REL)
        assert c["energia_kWh"] == pytest.approx(
            ENE_KWH_DEMO, rel=REL)
        assert c["energia_MWh"] == pytest.approx(
            ENE_MWH_DEMO, rel=REL)
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
        assert c["lcoe_EUR_MWh"] == pytest.approx(
            LCOE_DEMO, rel=REL)
        assert c["margine_EUR_MWh"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 16

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcoe_EUR_MWh"] == \
            _F["demo_calcoli"]()["lcoe_EUR_MWh"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh732_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 12

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("biogas_Nm3_anno",
                       "ch4_grezzo_Nm3",
                       "biometano_Nm3",
                       "slip_Nm3",
                       "energia_kWh",
                       "energia_MWh",
                       "capex_EUR",
                       "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno",
                       "van",
                       "tir",
                       "lcoe_EUR_MWh",
                       "margine_EUR_MWh",
                       "co2_evitata_t_anno"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_16_marginale(self):
        # Prezzo 16 EUR/MWh: netto 52.890,24
        # EUR/anno, VAN circa -51.017 EUR,
        # entro la tolleranza 10 % di
        # 600.000 = 60.000 -> MARGINALE.
        n = self._bc(prezzo_biometano_EUR_MWh=16.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert -60000.0 < n["van"] < 0.0

    def test_prezzo_15_non_conviente(self):
        # Prezzo 15 EUR/MWh: netto 31.459,60
        # EUR/anno, VAN circa -273.460 EUR,
        # oltre la tolleranza 60.000 EUR
        # -> NON_CONVIENTE.
        n = self._bc(prezzo_biometano_EUR_MWh=15.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -60000.0

    def test_prezzo_zero_non_conviente(self):
        # Prezzo 0: ricavo zero, netto negativo
        # pari a -costi annui, VAN negativa oltre
        # tolleranza -> NON_CONVIENTE.
        n = self._bc(prezzo_biometano_EUR_MWh=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero e prezzo 90: tutti i flussi
        # >= 0 -> TIR None, payback 0, VAN
        # positiva -> CONVIENTE.
        n = self._bc(capex_EUR_per_Nm3h=0.0)
        assert n["valid"] is True
        assert n["capex_EUR"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_recupero_uno_biometano_uguale_ch4(self):
        n = self._bc(recupero_metano=1.0)
        assert n["valid"] is True
        assert n["biometano_Nm3"] == pytest.approx(
            CH4_DEMO, rel=REL)
        assert n["slip_Nm3"] == pytest.approx(0.0, abs=1e-9)

    def test_portata_zero_neutro(self):
        n = self._bc(portata_biogas_Nm3h=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoe_EUR_MWh"] is None

    def test_frazione_zero_neutro(self):
        n = self._bc(frazione_ch4=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_frazione_uno_neutro(self):
        n = self._bc(frazione_ch4=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_recupero_zero_neutro(self):
        n = self._bc(recupero_metano=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_recupero_oltre_uno_neutro(self):
        n = self._bc(recupero_metano=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_oltre_8760_neutro(self):
        n = self._bc(ore_anno=8761)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_zero_neutro(self):
        n = self._bc(ore_anno=0)
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
        n = self._bc(portata_biogas_Nm3h=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_EUR_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(portata_biogas_Nm3h=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(portata_biogas_Nm3h="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_EUR_per_Nm3h=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh732_neutro"]()
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
        assert n["lcoe_EUR_MWh"] is None
        assert n["margine_EUR_MWh"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh732_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "portata_biogas_Nm3h", "frazione_ch4",
                       "ore_anno", "recupero_metano",
                       "capex_EUR_per_Nm3h",
                       "costo_upgrading_EUR_Nm3",
                       "om_fisso_EUR_anno",
                       "prezzo_biometano_EUR_MWh",
                       "fattore_gas_kg_kWh",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "biogas_Nm3_anno", "ch4_grezzo_Nm3",
                       "biometano_Nm3", "slip_Nm3",
                       "energia_kWh", "energia_MWh",
                       "capex_EUR", "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno", "flussi", "van",
                       "tir", "payback", "lcoe_EUR_MWh",
                       "margine_EUR_MWh",
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
        assert len(b["df_tabella"]) == 29
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia (kWh/anno)" in voci
        assert "Energia (MWh/anno)" in voci
        assert "Biometano (Nm3/anno)" in voci
        assert "Slip (Nm3/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOE (EUR/MWh)" in voci
        assert "Margine (EUR/MWh)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 16
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh732_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh732_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 30

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh732_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_EUR" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcoe_EUR_MWh" in txt
        assert "margine_EUR_MWh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "portata_biogas_Nm3h" in txt
        assert "energia_kWh" in txt
        assert "biometano_Nm3" in txt
        assert "slip_Nm3" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh732_csv"](bc, self._ing())
        assert f"netto_EUR_anno;{bc['netto_EUR_anno']}" in txt
        assert f"energia_kWh;{bc['energia_kWh']}" in txt
        assert "portata_biogas_Nm3h;500.0" in txt
        assert "capex_EUR_per_Nm3h;1200.0" in txt
        assert f"lcoe_EUR_MWh;{bc['lcoe_EUR_MWh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def732["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def732\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 12, ui_keys
        demo_keys = set(_F["mh732_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh732_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh732_demo():")
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
        ui_keys = set(re.findall(r'_def732\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W733 (26/10/2026) - tab732' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh732_num", "mh732_nneg", "mh732_pos",
                     "mh732_int_pos", "mh732_frac_01",
                     "mh732_frac_rec", "mh732_frac_toll",
                     "mh732_biogas", "mh732_ch4_grezzo",
                     "mh732_biometano", "mh732_slip",
                     "mh732_energia", "mh732_capex",
                     "mh732_costi", "mh732_ricavo",
                     "mh732_netto", "mh732_flussi",
                     "mh732_van", "mh732_tir",
                     "mh732_payback", "mh732_lcoe",
                     "mh732_margine", "mh732_co2_evitata",
                     "mh732_verdetto", "mh732_valida",
                     "_mh732_neutro", "mh732_calcola",
                     "mh732_csv", "mh732_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_731(self):
        assert "mh731" not in _helpers_src()
        assert "mh731" not in _ui_src()
        assert "st731" not in _ui_src()
        assert "tab731" not in _ui_src()
        assert "W732" not in _helpers_src()
        assert "W732" not in _ui_src()
        assert "mh732" in _helpers_src()
        assert "st732" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w733_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE732) == 1

    def test_blocco_with_tab732(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab732:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE732

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st732_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 15, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st732_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st732_[a-z0-9_]+)"', _ui_src())
        attese = ["st732_portata", "st732_frazione",
                  "st732_ore", "st732_recupero",
                  "st732_capex", "st732_costo",
                  "st732_om", "st732_prezzo",
                  "st732_fattore", "st732_vita",
                  "st732_wacc", "st732_tolleranza",
                  "st732_calcola"]
        assert len(attese) == 13
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg732" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg732") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg732")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOE (EUR/MWh)" in src
        assert "Margine (EUR/MWh)" in src
        assert "VAN (EUR)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "sul biogas" in src
        assert "bunker-fuel" in src
        assert "ammoniaca" in src
        assert "metanolo" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "sul biogas" in src
        assert "bunker-fuel" in src
        assert "ammoniaca" in src
        assert "metanolo" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "4.000.000" in src
        assert "2.156.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati732" in src
        assert '"EUR/MWh"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh732_csv" in src
        assert "biometano.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st732_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W733 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab732:")
