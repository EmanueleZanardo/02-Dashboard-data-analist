"""Test tab730 "🌿⚗️ Ammoniaca verde: Haber-Bosch da H2 verde — il prezzo dell'NH3 paga?"

Nuova tab tab730 (ammoniaca verde, w731).
Business case di un impianto che produce NH3
verde da H2 verde (elettrolisi) piu' N2 da
ASU, con loop Haber-Bosch: l'H2 e' un
intermedio, il prodotto venduto e' l'NH3.
Stechiometria 3H2 + N2 -> 2NH3, energia
elettrolisi piu' energia sintesi, CAPEX
elettrolizzatore piu' CAPEX sintesi, VAN,
TIR, payback, LCOA, margine sul prezzo NH3,
CO2 evitata e verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
capacita' 100.000 t/anno; ore 8000
ore/anno; consumo specifico 50 kWh/kg;
prezzo elettricita' 60 EUR/MWh; consumo
sintesi 1,2 kWh/kg NH3; CAPEX
elettrolizzatore 800 EUR/kW; CAPEX sintesi
1500 EUR/(t/anno); O&M 40 EUR/t; prezzo NH3
900 EUR/t; WACC 0,06 (6 %); vita 20 anni;
tolleranza 0,10 (10 % del CAPEX).

- h2_per_nh3 = 0.1775585696670777
- nh3_kg_anno = 100000000.0
- h2_kg_anno = 17755856.96670777
- e_el_kwh_anno = 887792848.3353885
- pot_kw = 110974.10604192357
- e_sint_kwh_anno = 120000000.0
- e_tot_kwh_anno = 1007792848.3353885
- costo_el_eur_anno = 60467570.90012331
- capex_eur = 238779284.83353886
- om_eur_anno = 4000000.0
- ricavo_eur_anno = 90000000.0
- netto_eur_anno = 25532429.099876687
- van = 54075665.460649624
- tir = 8.663096120362464
- payback = 10
- lcoa_eur_t = 764.0653514180026
- margine_eur_t = 135.9346485819974
- co2_evitata_t_anno = 180000.0
- verdetto = 'CONVIENTE'

Scomposizione: H2 per NH3 (3 x 2,016) /
(2 x 17,031) = 0,1775585696670777 kg/kg;
NH3 100.000 x 1000 = 100.000.000 kg/anno;
H2 100.000.000 x 0,1775585696670777 =
17.755.856,96670777 kg/anno; energia
elettrolisi 17.755.856,96670777 x 50 =
887.792.848,3353885 kWh/anno; potenza
887.792.848,3353885 / 8000 =
110.974,10604192357 kW; energia sintesi
100.000.000 x 1,2 = 120.000.000 kWh/anno;
energia totale 887.792.848,3353885 +
120.000.000 = 1.007.792.848,3353885
kWh/anno; costo elettricita'
1.007.792.848,3353885 / 1000 x 60 =
60.467.570,90012331 EUR/anno; CAPEX
110.974,10604192357 x 800 + 100.000 x
1500 = 238.779.284,83353886 EUR; O&M 40 x
100.000 = 4.000.000 EUR/anno; ricavo
100.000 x 900 = 90.000.000 EUR/anno;
netto 90.000.000 - 60.467.570,90012331 -
4.000.000 = 25.532.429,099876687 EUR/anno;
flussi: anno 0 -238.779.284,83353886, anni
1-20 netto 25.532.429,099876687 (piatti);
VAN -238.779.284,83353886 +
25.532.429,099876687 x 11,469921218565263
(annuita' 20 anni al 6 %) =
54.075.665,460649624 EUR; TIR
8,663096120362464 % (il tasso che azzera
il VAN dei flussi); payback 10 (il
cumulato supera lo zero al decimo anno:
-238.779.284,83353886 + 10 x
25.532.429,099876687 = 16.544.006,16522801);
LCOA (238.779.284,83353886 / 20 +
4.000.000 + 60.467.570,90012331) / 100.000
= 764,0653514180026 EUR/t; margine 900 -
764,0653514180026 = 135,9346485819974
EUR/t; CO2 evitata 100.000 x 1,8 = 180.000
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
    if (p / "w731_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w731_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w731_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w731_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w731_helpers.py: {missing}")
    return out


_F = _load("mh730_num", "mh730_nneg", "mh730_pos",
           "mh730_int_pos", "mh730_frac_01",
           "mh730_frac_toll", "mh730_h2_per_nh3",
           "mh730_nh3_kg", "mh730_h2_kg",
           "mh730_e_el", "mh730_pot_kw",
           "mh730_e_sint", "mh730_e_tot",
           "mh730_costo_el", "mh730_capex",
           "mh730_om", "mh730_ricavo",
           "mh730_netto", "mh730_flussi",
           "mh730_van", "mh730_tir", "mh730_payback",
           "mh730_lcoa", "mh730_margine",
           "mh730_co2_evitata", "mh730_verdetto",
           "mh730_valida", "_mh730_neutro",
           "mh730_calcola", "mh730_csv",
           "mh730_demo", "demo_calcoli")

TITLE730 = ("🌿⚗️ Ammoniaca verde: Haber-Bosch "
            "da H2 verde — il prezzo dell'NH3 paga?")

H2_PER_NH3_DEMO = 0.1775585696670777
NH3_DEMO = 100000000.0
H2_DEMO = 17755856.96670777
E_EL_DEMO = 887792848.3353885
POT_DEMO = 110974.10604192357
E_SINT_DEMO = 120000000.0
E_TOT_DEMO = 1007792848.3353885
COSTO_EL_DEMO = 60467570.90012331
CAPEX_DEMO = 238779284.83353886
OM_DEMO = 4000000.0
RICAVO_DEMO = 90000000.0
NETTO_DEMO = 25532429.099876687
VAN_DEMO = 54075665.460649624
TIR_DEMO = 8.663096120362464
PAYBACK_DEMO = 10
LCOA_DEMO = 764.0653514180026
MARGINE_DEMO = 135.9346485819974
CO2_DEMO = 180000.0
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "capacita_t_anno": 100000.0,
    "ore_anno": 8000,
    "consumo_spec_kwh_kg": 50.0,
    "prezzo_el_eur_mwh": 60.0,
    "consumo_sintesi_kwh_kg_nh3": 1.2,
    "capex_el_eur_kw": 800.0,
    "capex_sintesi_eur_per_t_anno": 1500.0,
    "om_eur_per_t": 40.0,
    "prezzo_nh3_eur_t": 900.0,
    "wacc_frac": 0.06,
    "vita_anni": 20,
    "tolleranza_frac": 0.10,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w731_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w731_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh730_demo"]()
        d.update(kw)
        return _F["mh730_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh730_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh730_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh730_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh730_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh730_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh730_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh730_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh730_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh730_int_pos"](20.0, "x") == 20

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh730_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh730_frac_01"](1.0, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh730_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh730_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh730_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_capacita_zero_non_valida(self):
        assert self._val(capacita_t_anno=0.0)["valido"] is False

    def test_ore_zero_e_frazione_non_valide(self):
        assert self._val(ore_anno=0)["valido"] is False
        assert self._val(ore_anno=8000.5)["valido"] is False

    def test_consumi_zero_non_validi(self):
        for k in ("consumo_spec_kwh_kg",
                  "consumo_sintesi_kwh_kg_nh3"):
            assert self._val(**{k: 0.0})["valido"] is False, k

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_eur_mwh",
                  "capex_el_eur_kw",
                  "capex_sintesi_eur_per_t_anno",
                  "om_eur_per_t", "prezzo_nh3_eur_t"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=20.5)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.06)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(capacita_t_anno=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(capacita_t_anno=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(capacita_t_anno="100000")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_nh3_eur_t=0.0)["valido"] is True
        assert self._val(capex_el_eur_kw=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_stechiometria(self):
        assert _F["mh730_h2_per_nh3"]() == pytest.approx(
            (3 * 2.016) / (2 * 17.031), rel=1e-12)
        assert _F["mh730_h2_per_nh3"]() == pytest.approx(
            H2_PER_NH3_DEMO, rel=REL)

    def test_nh3_kg_demo(self):
        assert _F["mh730_nh3_kg"](100000.0) == pytest.approx(
            NH3_DEMO, rel=REL)

    def test_h2_kg_demo(self):
        assert _F["mh730_h2_kg"](
            NH3_DEMO, H2_PER_NH3_DEMO) == pytest.approx(
            H2_DEMO, rel=REL)

    def test_e_el_demo(self):
        assert _F["mh730_e_el"](
            H2_DEMO, 50.0) == pytest.approx(
            E_EL_DEMO, rel=REL)

    def test_pot_kw_demo(self):
        assert _F["mh730_pot_kw"](
            E_EL_DEMO, 8000) == pytest.approx(
            POT_DEMO, rel=REL)

    def test_e_sint_demo(self):
        assert _F["mh730_e_sint"](
            NH3_DEMO, 1.2) == pytest.approx(
            E_SINT_DEMO, rel=REL)

    def test_e_tot_demo(self):
        assert _F["mh730_e_tot"](
            E_EL_DEMO, E_SINT_DEMO) == pytest.approx(
            E_TOT_DEMO, rel=REL)

    def test_costo_el_demo(self):
        assert _F["mh730_costo_el"](
            E_TOT_DEMO, 60.0) == pytest.approx(
            COSTO_EL_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh730_capex"](
            POT_DEMO, 800.0, 100000.0,
            1500.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_formula_indipendente(self):
        assert _F["mh730_capex"](
            1000.0, 800.0, 50000.0,
            1500.0) == pytest.approx(
            1000.0 * 800.0 + 50000.0 * 1500.0, rel=REL)

    def test_om_demo(self):
        assert _F["mh730_om"](
            40.0, 100000.0) == pytest.approx(OM_DEMO, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh730_ricavo"](
            100000.0, 900.0) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh730_netto"](
            RICAVO_DEMO, COSTO_EL_DEMO,
            OM_DEMO) == pytest.approx(NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh730_netto"](
            1000000.0, 60467570.90012331,
            4000000.0) == pytest.approx(
            -63467570.90012331, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh730_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh730_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        assert abs(_F["mh730_van"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh730_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 20
        assert _F["mh730_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh730_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh730_flussi"](CAPEX_DEMO, -1000.0, 20)
        assert _F["mh730_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh730_tir"](
            [0.0] + [NETTO_DEMO] * 20) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh730_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh730_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh730_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh730_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        tir = _F["mh730_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh730_flussi"](CAPEX_DEMO, NETTO_DEMO, 20)
        assert _F["mh730_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh730_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh730_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh730_payback"](
            [-1000000000.0] + [NETTO_DEMO] * 20) is None

    def test_lcoa_demo(self):
        assert _F["mh730_lcoa"](
            CAPEX_DEMO, 20, OM_DEMO, COSTO_EL_DEMO,
            100000.0) == pytest.approx(LCOA_DEMO, rel=REL)

    def test_lcoa_none_se_capacita_zero(self):
        assert _F["mh730_lcoa"](
            1000.0, 10, 100.0, 50.0, 0.0) is None

    def test_lcoa_formula_indipendente(self):
        assert _F["mh730_lcoa"](
            120000.0, 10, 5000.0, 10000.0,
            1000.0) == pytest.approx(
            (12000.0 + 5000.0 + 10000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh730_margine"](
            900.0, LCOA_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcoa_none(self):
        assert _F["mh730_margine"](900.0, None) is None

    def test_co2_demo(self):
        assert _F["mh730_co2_evitata"](
            100000.0) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_fattore_letterale(self):
        assert _F["mh730_co2_evitata"](
            50000.0) == pytest.approx(90000.0, rel=REL)

    def test_verdetto_demo(self):
        assert _F["mh730_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, H2_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh730_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, H2_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh730_verdetto"](
            0.0, CAPEX_DEMO, 0.10, H2_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh730_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            H2_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh730_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            H2_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh730_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, H2_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_h2_zero(self):
        assert _F["mh730_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh730_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, H2_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh730_demo"]()
        d.update(kw)
        return _F["mh730_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["h2_per_nh3"] == pytest.approx(
            H2_PER_NH3_DEMO, rel=REL)
        assert c["nh3_kg_anno"] == pytest.approx(
            NH3_DEMO, rel=REL)
        assert c["h2_kg_anno"] == pytest.approx(
            H2_DEMO, rel=REL)
        assert c["e_el_kwh_anno"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["pot_kw"] == pytest.approx(
            POT_DEMO, rel=REL)
        assert c["e_sint_kwh_anno"] == pytest.approx(
            E_SINT_DEMO, rel=REL)
        assert c["e_tot_kwh_anno"] == pytest.approx(
            E_TOT_DEMO, rel=REL)
        assert c["costo_el_eur_anno"] == pytest.approx(
            COSTO_EL_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["om_eur_anno"] == pytest.approx(
            OM_DEMO, rel=REL)
        assert c["ricavo_eur_anno"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["netto_eur_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["lcoa_eur_t"] == pytest.approx(
            LCOA_DEMO, rel=REL)
        assert c["margine_eur_t"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 21

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcoa_eur_t"] == \
            _F["demo_calcoli"]()["lcoa_eur_t"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh730_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 12

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("h2_per_nh3",
                       "nh3_kg_anno",
                       "h2_kg_anno",
                       "e_el_kwh_anno",
                       "pot_kw",
                       "e_sint_kwh_anno",
                       "e_tot_kwh_anno",
                       "costo_el_eur_anno",
                       "capex_eur",
                       "om_eur_anno",
                       "ricavo_eur_anno",
                       "netto_eur_anno",
                       "van",
                       "tir",
                       "lcoa_eur_t",
                       "margine_eur_t",
                       "co2_evitata_t_anno"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 10" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_nh3_850_marginale(self):
        # Prezzo NH3 850 EUR/t: netto circa
        # 20.532.429 EUR/anno, VAN circa
        # -3.276.000 EUR, entro la tolleranza
        # 10 % di 238.779.285 = 23.877.928 ->
        # MARGINALE.
        n = self._bc(prezzo_nh3_eur_t=850.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert -23877928.483353887 < n["van"] < 0.0

    def test_prezzo_nh3_800_non_conviente(self):
        # Prezzo NH3 800 EUR/t: netto
        # 15.532.429 EUR/anno, VAN circa
        # -60.623.547 EUR, oltre la tolleranza
        # 23.877.928 EUR -> NON_CONVIENTE.
        n = self._bc(prezzo_nh3_eur_t=800.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -23877928.483353887

    def test_prezzo_el_alto_non_conviente(self):
        # Prezzo elettricita' 120 EUR/MWh:
        # costo elettricita' raddoppia circa,
        # netto negativo, VAN negativa oltre
        # tolleranza -> NON_CONVIENTE.
        n = self._bc(prezzo_el_eur_mwh=120.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero (capex el e sintesi zero)
        # e prezzo NH3 900: tutti i flussi
        # >= 0 -> TIR None, payback 0, VAN
        # positiva -> CONVIENTE.
        n = self._bc(capex_el_eur_kw=0.0,
                     capex_sintesi_eur_per_t_anno=0.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_capacita_zero_neutro(self):
        n = self._bc(capacita_t_anno=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoa_eur_t"] is None

    def test_consumo_zero_neutro(self):
        for k in ("consumo_spec_kwh_kg",
                  "consumo_sintesi_kwh_kg_nh3"):
            n = self._bc(**{k: 0.0})
            assert n["verdetto"] == "NON_CALCOLABILE", k
            assert n["valid"] is False, k

    def test_consumo_negativo_neutro(self):
        n = self._bc(consumo_spec_kwh_kg=-5.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

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
        n = self._bc(capacita_t_anno=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(capacita_t_anno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(capacita_t_anno="100000")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_el_negativo_neutro(self):
        n = self._bc(prezzo_el_eur_mwh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh730_neutro"]()
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
        assert n["lcoa_eur_t"] is None
        assert n["margine_eur_t"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh730_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "capacita_t_anno", "ore_anno",
                       "consumo_spec_kwh_kg",
                       "prezzo_el_eur_mwh",
                       "consumo_sintesi_kwh_kg_nh3",
                       "capex_el_eur_kw",
                       "capex_sintesi_eur_per_t_anno",
                       "om_eur_per_t", "prezzo_nh3_eur_t",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "h2_per_nh3", "nh3_kg_anno",
                       "h2_kg_anno", "e_el_kwh_anno",
                       "pot_kw", "e_sint_kwh_anno",
                       "e_tot_kwh_anno",
                       "costo_el_eur_anno", "capex_eur",
                       "om_eur_anno", "ricavo_eur_anno",
                       "netto_eur_anno", "flussi", "van",
                       "tir", "payback", "lcoa_eur_t",
                       "margine_eur_t",
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
        assert len(b["df_tabella"]) == 31
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia totale (kWh/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOA (EUR/t)" in voci
        assert "Margine (EUR/t)" in voci
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
        return _F["mh730_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh730_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 32

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh730_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "costo_el_eur_anno" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcoa_eur_t" in txt
        assert "margine_eur_t" in txt
        assert "co2_evitata_t_anno" in txt
        assert "capacita_t_anno" in txt
        assert "e_tot_kwh_anno" in txt
        assert "capex_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh730_csv"](bc, self._ing())
        assert f"netto_eur_anno;{bc['netto_eur_anno']}" in txt
        assert f"e_tot_kwh_anno;{bc['e_tot_kwh_anno']}" in txt
        assert "capacita_t_anno;100000.0" in txt
        assert "capex_el_eur_kw;800.0" in txt
        assert f"lcoa_eur_t;{bc['lcoa_eur_t']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def730["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def730\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 12, ui_keys
        demo_keys = set(_F["mh730_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh730_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh730_demo():")
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
        ui_keys = set(re.findall(r'_def730\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W731 (26/10/2026) - tab730' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh730_num", "mh730_nneg", "mh730_pos",
                     "mh730_int_pos", "mh730_frac_01",
                     "mh730_frac_toll", "mh730_h2_per_nh3",
                     "mh730_nh3_kg", "mh730_h2_kg",
                     "mh730_e_el", "mh730_pot_kw",
                     "mh730_e_sint", "mh730_e_tot",
                     "mh730_costo_el", "mh730_capex",
                     "mh730_om", "mh730_ricavo",
                     "mh730_netto", "mh730_flussi",
                     "mh730_van", "mh730_tir",
                     "mh730_payback", "mh730_lcoa",
                     "mh730_margine", "mh730_co2_evitata",
                     "mh730_verdetto", "mh730_valida",
                     "_mh730_neutro", "mh730_calcola",
                     "mh730_csv", "mh730_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_729(self):
        assert "mh729" not in _helpers_src()
        assert "mh729" not in _ui_src()
        assert "st729" not in _ui_src()
        assert "tab729" not in _ui_src()
        assert "W730" not in _helpers_src()
        assert "W730" not in _ui_src()
        assert "mh730" in _helpers_src()
        assert "st730" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w731_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE730) == 1

    def test_blocco_with_tab730(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab730:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE730

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st730_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 15, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st730_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st730_[a-z0-9_]+)"', _ui_src())
        attese = ["st730_capacita", "st730_ore",
                  "st730_consumo_spec", "st730_prezzo_el",
                  "st730_consumo_sintesi", "st730_capex_el",
                  "st730_capex_sintesi", "st730_om",
                  "st730_prezzo_nh3", "st730_vita",
                  "st730_wacc", "st730_tolleranza",
                  "st730_calcola"]
        assert len(attese) == 13
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg730" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg730") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg730")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOA (EUR/t)" in src
        assert "Margine (EUR/t)" in src
        assert "VAN (EUR)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "elettrolizzatori a confronto" in src
        assert "bunker" in src
        assert "power-to-X" in src
        assert "metanolo" in src
        assert "reforming" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "elettrolizzatori a confronto" in src
        assert "bunker" in src
        assert "power-to-X" in src
        assert "metanolo" in src
        assert "reforming" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "887.792.848" in src
        assert "17.755.857" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati730" in src
        assert '"EUR/t"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh730_csv" in src
        assert "ammoniaca_verde.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st730_show_flussi" in src
        assert "st.checkbox" in src

    def test_em_dash_solo_nel_titolo_e_niente_nome(self):
        # Il trattino lungo e' ammesso SOLO nel
        # titolo della tab (richiesto dal brief):
        # 1 occorrenza nell'header helper, 2 in UI
        # (h1 + titolo edu). Niente nome altrove.
        assert _helpers_src().count("—") == 1
        assert _ui_src().count("—") == 2
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W731 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab730:")
