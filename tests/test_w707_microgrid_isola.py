"""Test tab707 "🏝️ Microgrid in isola: PV + batteria + generatore, quanto costa l'autonomia?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
carico sito 800 MWh/anno; PV 300 kW, resa
1100 kWh/kWp/anno; frazione autoconsumo
0,60; batteria 500 kWh, DoD 0,90, cicli 250
/anno, eta_rt 0,90; prezzo rete 220 EUR/MWh;
prezzo export 80 EUR/MWh; carico in isola
150 kW; eventi 12/anno, durata 4 h;
generatore 200 kW, consumo 0,30 l/kWh,
carburante 1,60 EUR/l; VoLL 5000 EUR/MWh;
OPEX 15000 EUR/anno; costo PV 1000 EUR/kW,
costo batteria 600 EUR/kWh, costo generatore
400 EUR/kW, costo fisso 50000 EUR; vita 15
anni; WACC 0,05 (5 %); tolleranza 0,10 (10 %
del CAPEX); fattore CO2 rete 0,35 t/MWh;
fattore CO2 generatore 0,80 kg/kWh elettrico.

- energia_pv_mwh_a = 330.0
- energia_auto_mwh_a = 198.0
- energia_export0_mwh_a = 132.0
- energia_shift_mwh_a = 101.25
- energia_export_mwh_a = 19.5
- energia_rete_mwh_a = 500.75
- ore_isola_h_a = 48
- energia_isola_mwh_a = 7.2
- energia_batt_evento_mwh = 0.45
- energia_gen_evento_mwh = 0.15
- energia_gen_mwh_a = 1.8
- litri_carburante_l_a = 540.0
- costo_carburante_eur_a = 864.0
- ens_mwh_a = 0.0
- costo_base_eur_a = 212000.0
- costo_microgrid_eur_a = 124469.0
- risparmio_eur_a = 87531.0
- co2_evitata_t_a = 103.2975
- capex_eur = 730000.0
- van = 178541.8477399859
- tir = 8.428701752435297
- payback = 9
- verdetto = 'CONVIENTE'

Scomposizione: E_pv 300 x 1100 / 1000 =
330.0; E_auto min(330,0 x 0,60, 800) = 198.0;
E_exp0 330,0 - 198,0 = 132.0; E_shift
min(132,0, 500 x 0,90 x 250 / 1000 = 112,5)
x 0,90 = 101.25; E_exp 132,0 - 112,5 = 19.5;
E_grid 800 - 198,0 - 101,25 = 500.75;
h_isola 12 x 4 = 48; E_isola 150 x 48 / 1000
= 7.2; E_batt_ev 500 x 0,90 / 1000 = 0.45;
E_gen_ev 150 x 4 / 1000 - 0,45 = 0.15;
E_gen 0,15 x 12 = 1.8; litri 1,8 x 1000 x
0,30 = 540.0; C_fuel 540,0 x 1,60 = 864.0;
ENS_mg max(0, 150 - 200) x 48 / 1000 = 0.0;
C_base 800 x 220 + 7,2 x 5000 = 212000.0;
C_mg 500,75 x 220 - 19,5 x 80 + 864,0 +
15000 = 124469.0; risparmio 212000,0 -
124469,0 = 87531.0; CAPEX 300 x 1000 + 500
x 600 + 200 x 400 + 50000 = 730000.0; VAN
-730000,0 + 87531,0 x (1 - 1,05^-15) / 0,05
= 178541.8477399859; TIR per bisezione su
[-0,99, 5,0] dei flussi [-730000,
87531,0 x 15]: 8.428701752435297 % (VAN a
quella TIR ~0); payback: cumulato anno 8
-29752,0, anno 9 +57779,0 -> 9; VAN >= 0 ->
CONVIENTE. CO2: (198,0 + 101,25) x 0,35 -
1,8 x 0,80 = 103.2975 t/anno (il secondo
termine e' MWh x 1000 kWh/MWh x kg/kWh =
t, senza ulteriori divisioni).
Artefatti float (valori arrotondati tra
parentesi): energia_gen_evento_mwh =
0.14999999999999997 (0,15); energia_gen_mwh_a
= 1.7999999999999996 (1,8);
litri_carburante_l_a = 539.9999999999999
(540,0); costo_carburante_eur_a =
863.9999999999999 (864,0).
NOTA: i valori esatti ricalcolati sono
quelli sopra (VAN 178541,85, TIR 8,4287 %) —
il test fissa i valori esatti, non le
approssimazioni. La microgrid qui e'
COORDINATA (PV + batteria + generatore),
non un generatore da solo e non un
black-start.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w708_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w708_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w708_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w708_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w708_helpers.py: {missing}")
    return out


_F = _load("mh707_num", "mh707_nneg", "mh707_pos",
           "mh707_int_pos", "mh707_int_nneg",
           "mh707_quota_valida", "mh707_eta_valido",
           "mh707_energia_pv", "mh707_autoconsumo",
           "mh707_energia_shift", "mh707_export_residuo",
           "mh707_energia_rete", "mh707_ore_isola",
           "mh707_energia_isola", "mh707_energia_batt_evento",
           "mh707_energia_gen_evento",
           "mh707_litri_carburante", "mh707_costo_carburante",
           "mh707_ens", "mh707_costo_base",
           "mh707_costo_microgrid", "mh707_risparmio",
           "mh707_capex_microgrid", "mh707_co2_evitata",
           "mh707_crf", "mh707_van", "mh707_tir",
           "mh707_payback", "mh707_verdetto",
           "mh707_valida", "_mh707_neutro",
           "mh707_calcola", "mh707_sensitivita",
           "mh707_csv", "mh707_demo", "demo_calcoli")

TITLE707 = ("🏝️ Microgrid in isola: PV + batteria + "
            "generatore, quanto costa l'autonomia?")

E_PV_DEMO = 330.0
E_AUTO_DEMO = 198.0
E_EXP0_DEMO = 132.0
E_SHIFT_DEMO = 101.25
E_EXP_DEMO = 19.5
E_GRID_DEMO = 500.75
H_ISOLA_DEMO = 48
E_ISOLA_DEMO = 7.2
E_BATT_EV_DEMO = 0.45
E_GEN_EV_DEMO = 0.15
E_GEN_DEMO = 1.8
LITRI_DEMO = 540.0
C_FUEL_DEMO = 864.0
ENS_DEMO = 0.0
C_BASE_DEMO = 212000.0
C_MG_DEMO = 124469.0
RISPARMIO_DEMO = 87531.0
CO2_EV_DEMO = 103.2975
CAPEX_DEMO = 730000.0
VAN_DEMO = 178541.8477399859
TIR_DEMO = 8.428701752435297
PAYBACK_DEMO = 9
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w708_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w708_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh707_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh707_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh707_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh707_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh707_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh707_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh707_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh707_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh707_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh707_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh707_int_pos"](15.0, "x") == 15

    def test_int_nneg_accetta_zero(self):
        assert _F["mh707_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh707_int_nneg"](-1, "x")

    def test_int_nneg_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh707_int_nneg"](2.5, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh707_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh707_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh707_quota_valida"](0.0, "x") == 0.0
        assert _F["mh707_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh707_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh707_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh707_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_demo(self):
        assert _F["mh707_eta_valido"](0.90, "x") == 0.90


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh707_demo"]()
        d.update(kw)
        return _F["mh707_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_carico_zero_non_valido(self):
        assert self._val(carico_mwh_a=0.0)["valido"] is False

    def test_carico_negativo_non_valido(self):
        assert self._val(carico_mwh_a=-10.0)["valido"] is False

    def test_pv_zero_valido(self):
        assert self._val(potenza_pv_kw=0.0)["valido"] is True

    def test_pv_negativo_non_valido(self):
        assert self._val(potenza_pv_kw=-1.0)["valido"] is False

    def test_resa_negativa_non_valida(self):
        assert self._val(resa_kwh_kwp_a=-1.0)["valido"] is False

    def test_f_auto_negativa_non_valida(self):
        assert self._val(f_autoconsumo=-0.01)["valido"] is False

    def test_f_auto_sopra_uno_non_valida(self):
        assert self._val(f_autoconsumo=1.1)["valido"] is False

    def test_f_auto_uno_valida(self):
        assert self._val(f_autoconsumo=1.0)["valido"] is True

    def test_batteria_negativa_non_valida(self):
        assert self._val(batteria_kwh=-1.0)["valido"] is False

    def test_dod_negativa_non_valida(self):
        assert self._val(dod_frac=-0.01)["valido"] is False

    def test_dod_sopra_uno_non_valida(self):
        assert self._val(dod_frac=1.1)["valido"] is False

    def test_dod_uno_valida(self):
        assert self._val(dod_frac=1.0)["valido"] is True

    def test_eta_rt_zero_non_valido(self):
        assert self._val(eta_rt=0.0)["valido"] is False

    def test_eta_rt_sopra_uno_non_valido(self):
        assert self._val(eta_rt=1.1)["valido"] is False

    def test_eta_rt_uno_valido(self):
        assert self._val(eta_rt=1.0)["valido"] is True

    def test_eventi_negativi_non_validi(self):
        assert self._val(n_eventi_a=-1)["valido"] is False

    def test_eventi_non_interi_non_validi(self):
        assert self._val(n_eventi_a=2.5)["valido"] is False

    def test_eventi_zero_validi(self):
        assert self._val(n_eventi_a=0)["valido"] is True

    def test_durata_negativa_non_valida(self):
        assert self._val(durata_h=-1.0)["valido"] is False

    def test_gen_negativo_non_valido(self):
        assert self._val(potenza_gen_kw=-1.0)["valido"] is False

    def test_gen_zero_valido(self):
        assert self._val(potenza_gen_kw=0.0)["valido"] is True

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=14.5)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_rete_eur_mwh",
                  "prezzo_export_eur_mwh",
                  "carico_isola_kw", "consumo_l_kwh",
                  "prezzo_carburante_eur_l", "voll_eur_mwh",
                  "opex_eur_a", "costo_pv_eur_kw",
                  "costo_batt_eur_kwh", "costo_gen_eur_kw",
                  "costo_fisso_eur", "wacc_frac",
                  "fattore_co2_rete",
                  "fattore_co2_gen_kg_kwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(resa_kwh_kwp_a=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(carico_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(carico_mwh_a=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(resa_kwh_kwp_a="1100")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_rete_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_export_eur_mwh=0.0)["valido"] is True
        assert self._val(opex_eur_a=0.0)["valido"] is True
        assert self._val(costo_pv_eur_kw=0.0)["valido"] is True
        assert self._val(costo_fisso_eur=0.0)["valido"] is True
        assert self._val(voll_eur_mwh=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_energia_pv_demo(self):
        assert _F["mh707_energia_pv"](
            300.0, 1100.0) == pytest.approx(
            E_PV_DEMO, rel=REL)

    def test_energia_pv_zero(self):
        assert _F["mh707_energia_pv"](0.0, 1100.0) == 0.0

    def test_energia_pv_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh707_energia_pv"](-1.0, 1100.0)

    def test_autoconsumo_demo(self):
        assert _F["mh707_autoconsumo"](
            E_PV_DEMO, 0.60, 800.0) == pytest.approx(
            E_AUTO_DEMO, rel=REL)

    def test_autoconsumo_cappato_dal_carico(self):
        assert _F["mh707_autoconsumo"](
            1000.0, 0.60, 500.0) == pytest.approx(
            500.0, rel=REL)

    def test_autoconsumo_zero(self):
        assert _F["mh707_autoconsumo"](
            E_PV_DEMO, 0.0, 800.0) == 0.0

    def test_shift_demo(self):
        assert _F["mh707_energia_shift"](
            E_EXP0_DEMO, 500.0, 0.90, 250.0,
            0.90) == pytest.approx(E_SHIFT_DEMO, rel=REL)

    def test_shift_cappato_dall_eccedenza(self):
        assert _F["mh707_energia_shift"](
            10.0, 500.0, 0.90, 250.0, 0.90) == pytest.approx(
            9.0, rel=REL)

    def test_shift_zero_senza_batteria(self):
        assert _F["mh707_energia_shift"](
            E_EXP0_DEMO, 0.0, 0.90, 250.0,
            0.90) == 0.0

    def test_shift_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh707_energia_shift"](
                E_EXP0_DEMO, 500.0, 0.90, 250.0, 0.0)

    def test_export_residuo_demo(self):
        assert _F["mh707_export_residuo"](
            E_EXP0_DEMO, E_SHIFT_DEMO, 0.90) == pytest.approx(
            E_EXP_DEMO, rel=REL)

    def test_export_residuo_eta_uno(self):
        assert _F["mh707_export_residuo"](
            132.0, 101.25, 1.0) == pytest.approx(
            30.75, rel=REL)

    def test_energia_rete_demo(self):
        assert _F["mh707_energia_rete"](
            800.0, E_AUTO_DEMO, E_SHIFT_DEMO) == pytest.approx(
            E_GRID_DEMO, rel=REL)

    def test_energia_rete_floor_zero(self):
        assert _F["mh707_energia_rete"](
            100.0, 90.0, 50.0) == 0.0

    def test_ore_isola_demo(self):
        assert _F["mh707_ore_isola"](12, 4.0) == 48

    def test_ore_isola_zero_eventi(self):
        assert _F["mh707_ore_isola"](0, 4.0) == 0

    def test_energia_isola_demo(self):
        assert _F["mh707_energia_isola"](
            150.0, 48.0) == pytest.approx(
            E_ISOLA_DEMO, rel=REL)

    def test_batt_evento_demo(self):
        assert _F["mh707_energia_batt_evento"](
            500.0, 0.90) == pytest.approx(
            E_BATT_EV_DEMO, rel=REL)

    def test_gen_evento_demo(self):
        assert _F["mh707_energia_gen_evento"](
            150.0, 4.0, 500.0, 0.90) == pytest.approx(
            E_GEN_EV_DEMO, rel=REL)

    def test_gen_evento_zero_se_batteria_copre(self):
        assert _F["mh707_energia_gen_evento"](
            100.0, 4.0, 500.0, 0.90) == 0.0

    def test_litri_demo(self):
        assert _F["mh707_litri_carburante"](
            E_GEN_DEMO, 0.30) == pytest.approx(
            LITRI_DEMO, rel=REL)

    def test_costo_carburante_demo(self):
        assert _F["mh707_costo_carburante"](
            E_GEN_DEMO, 0.30, 1.60) == pytest.approx(
            C_FUEL_DEMO, rel=REL)

    def test_ens_zero_gen_adeguato(self):
        assert _F["mh707_ens"](150.0, 200.0, 48.0) == 0.0

    def test_ens_positivo_gen_sottodimensionato(self):
        assert _F["mh707_ens"](150.0, 100.0, 48.0) == pytest.approx(
            2.4, rel=REL)

    def test_ens_zero_senza_isola(self):
        assert _F["mh707_ens"](150.0, 100.0, 0.0) == 0.0

    def test_costo_base_demo(self):
        assert _F["mh707_costo_base"](
            800.0, 220.0, E_ISOLA_DEMO,
            5000.0) == pytest.approx(C_BASE_DEMO, rel=REL)

    def test_costo_microgrid_demo(self):
        assert _F["mh707_costo_microgrid"](
            E_GRID_DEMO, 220.0, E_EXP_DEMO, 80.0,
            C_FUEL_DEMO, 15000.0, ENS_DEMO,
            5000.0) == pytest.approx(C_MG_DEMO, rel=REL)

    def test_costo_microgrid_con_ens(self):
        assert _F["mh707_costo_microgrid"](
            E_GRID_DEMO, 220.0, E_EXP_DEMO, 80.0,
            C_FUEL_DEMO, 15000.0, 2.4,
            5000.0) == pytest.approx(
            C_MG_DEMO + 12000.0, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh707_risparmio"](
            C_BASE_DEMO, C_MG_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh707_risparmio"](
            100000.0, 150000.0) == pytest.approx(
            -50000.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh707_capex_microgrid"](
            300.0, 1000.0, 500.0, 600.0, 200.0, 400.0,
            50000.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh707_capex_microgrid"](
            0.0, 1000.0, 0.0, 600.0, 0.0, 400.0,
            50000.0) == 50000.0

    def test_co2_demo(self):
        assert _F["mh707_co2_evitata"](
            E_AUTO_DEMO, E_SHIFT_DEMO, 0.35,
            E_GEN_DEMO, 0.80) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_unita_f_gen_senza_divisione(self):
        # 1,8 MWh x 0,80 kg/kWh = 1,44 t (non
        # 0,00144 t): il fattore e' gia' in t per
        # MWh numericamente, per la cancellazione
        # MWh x 1000 kWh/MWh x kg/kWh / 1000 kg/t.
        assert _F["mh707_co2_evitata"](
            0.0, 0.0, 0.35, 1.8, 0.80) == pytest.approx(
            -1.44, rel=REL)

    def test_co2_solo_spostata(self):
        assert _F["mh707_co2_evitata"](
            0.0, E_SHIFT_DEMO, 0.35, 0.0,
            0.80) == pytest.approx(35.4375, rel=REL)

    def test_crf_demo(self):
        assert _F["mh707_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh707_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh707_van"](
            RISPARMIO_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh707_van"](
            RISPARMIO_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh707_van"](
            RISPARMIO_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISPARMIO_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh707_van"](RISPARMIO_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh707_van"](RISPARMIO_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh707_tir"](
            CAPEX_DEMO, RISPARMIO_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_bisezione_indipendente(self):
        flussi = [-CAPEX_DEMO] + [RISPARMIO_DEMO] * 15

        def _npv(x):
            return sum(f / (1.0 + x) ** i
                       for i, f in enumerate(flussi))

        lo, hi = -0.99, 5.0
        n_lo = _npv(lo)
        for _ in range(200):
            mid = (lo + hi) / 2.0
            n_mid = _npv(mid)
            if (n_lo > 0.0) == (n_mid > 0.0):
                lo, n_lo = mid, n_mid
            else:
                hi = mid
            if hi - lo < 1e-12:
                break
        tir_ind = (lo + hi) / 2.0
        assert abs(tir_ind * 100.0 - TIR_DEMO) <= 0.05
        tir = _F["mh707_tir"](CAPEX_DEMO, RISPARMIO_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh707_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh707_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh707_tir"](0.0, RISPARMIO_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh707_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh707_tir"](CAPEX_DEMO, RISPARMIO_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISPARMIO_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh707_payback"](
            CAPEX_DEMO, RISPARMIO_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISPARMIO_DEMO * 8 < 0.0
        assert -CAPEX_DEMO + RISPARMIO_DEMO * 9 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh707_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh707_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh707_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh707_payback"](
            50000000.0, RISPARMIO_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh707_payback"](0.0, RISPARMIO_DEMO, 15) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh707_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh707_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh707_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh707_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 73000 = 10 % di CAPEX 730000
        assert _F["mh707_verdetto"](
            -73000.0, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh707_verdetto"](
            -73000.1, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh707_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh707_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh707_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh707_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh707_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh707_verdetto"](100.0, CAPEX_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh707_verdetto"](100.0, CAPEX_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh707_demo"]()
        d.update(kw)
        return _F["mh707_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_pv_mwh_a"] == pytest.approx(
            E_PV_DEMO, rel=REL)
        assert c["energia_auto_mwh_a"] == pytest.approx(
            E_AUTO_DEMO, rel=REL)
        assert c["energia_export0_mwh_a"] == pytest.approx(
            E_EXP0_DEMO, rel=REL)
        assert c["energia_shift_mwh_a"] == pytest.approx(
            E_SHIFT_DEMO, rel=REL)
        assert c["energia_export_mwh_a"] == pytest.approx(
            E_EXP_DEMO, rel=REL)
        assert c["energia_rete_mwh_a"] == pytest.approx(
            E_GRID_DEMO, rel=REL)
        assert c["ore_isola_h_a"] == H_ISOLA_DEMO
        assert c["energia_isola_mwh_a"] == pytest.approx(
            E_ISOLA_DEMO, rel=REL)
        assert c["energia_batt_evento_mwh"] == pytest.approx(
            E_BATT_EV_DEMO, rel=REL)
        assert c["energia_gen_evento_mwh"] == pytest.approx(
            E_GEN_EV_DEMO, rel=REL)
        assert c["energia_gen_mwh_a"] == pytest.approx(
            E_GEN_DEMO, rel=REL)
        assert c["litri_carburante_l_a"] == pytest.approx(
            LITRI_DEMO, rel=REL)
        assert c["costo_carburante_eur_a"] == pytest.approx(
            C_FUEL_DEMO, rel=REL)
        assert c["ens_mwh_a"] == pytest.approx(
            ENS_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_microgrid_eur_a"] == pytest.approx(
            C_MG_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
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
        d = _F["mh707_demo"]()
        b = _F["mh707_calcola"](**d)
        coppie = [("energia_pv_mwh_a", E_PV_DEMO),
                  ("energia_auto_mwh_a", E_AUTO_DEMO),
                  ("energia_export0_mwh_a", E_EXP0_DEMO),
                  ("energia_shift_mwh_a", E_SHIFT_DEMO),
                  ("energia_export_mwh_a", E_EXP_DEMO),
                  ("energia_rete_mwh_a", E_GRID_DEMO),
                  ("energia_isola_mwh_a", E_ISOLA_DEMO),
                  ("energia_gen_mwh_a", E_GEN_DEMO),
                  ("litri_carburante_l_a", LITRI_DEMO),
                  ("costo_carburante_eur_a", C_FUEL_DEMO),
                  ("ens_mwh_a", ENS_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_microgrid_eur_a", C_MG_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO),
                  ("capex_eur", CAPEX_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh707_demo"]()
        assert d["carico_mwh_a"] == 800.0
        assert d["potenza_pv_kw"] == 300.0
        assert d["resa_kwh_kwp_a"] == 1100.0
        assert d["f_autoconsumo"] == 0.60
        assert d["batteria_kwh"] == 500.0
        assert d["dod_frac"] == 0.90
        assert d["cicli_a"] == 250.0
        assert d["eta_rt"] == 0.90
        assert d["prezzo_rete_eur_mwh"] == 220.0
        assert d["prezzo_export_eur_mwh"] == 80.0
        assert d["carico_isola_kw"] == 150.0
        assert d["n_eventi_a"] == 12
        assert d["durata_h"] == 4.0
        assert d["potenza_gen_kw"] == 200.0
        assert d["consumo_l_kwh"] == 0.30
        assert d["prezzo_carburante_eur_l"] == 1.60
        assert d["voll_eur_mwh"] == 5000.0
        assert d["opex_eur_a"] == 15000.0
        assert d["costo_pv_eur_kw"] == 1000.0
        assert d["costo_batt_eur_kwh"] == 600.0
        assert d["costo_gen_eur_kw"] == 400.0
        assert d["costo_fisso_eur"] == 50000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_co2_rete"] == 0.35
        assert d["fattore_co2_gen_kg_kwh"] == 0.80

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_pv_mwh_a",
                       "energia_auto_mwh_a",
                       "energia_export0_mwh_a",
                       "energia_shift_mwh_a",
                       "energia_export_mwh_a",
                       "energia_rete_mwh_a",
                       "energia_isola_mwh_a",
                       "energia_batt_evento_mwh",
                       "energia_gen_evento_mwh",
                       "energia_gen_mwh_a",
                       "litri_carburante_l_a",
                       "costo_carburante_eur_a",
                       "ens_mwh_a",
                       "costo_base_eur_a",
                       "costo_microgrid_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 9" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_rete_150_marginale(self):
        # C_base 156000,0; C_mg 89416,50;
        # risparmio 66583,50; VAN -38886,04 entro
        # tolleranza 73000 -> MARGINALE; payback 11
        n = self._bc(prezzo_rete_eur_mwh=150.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            66583.5, rel=REL)
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 11

    def test_opex_37531_marginale(self):
        # risparmio 65000,0; VAN -55322,23 entro
        # tolleranza 73000 -> MARGINALE; payback 12
        n = self._bc(opex_eur_a=37531.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            65000.0, rel=REL)
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 12

    def test_vita_dieci_marginale(self):
        # VAN -54108,82 entro tolleranza 73000
        # -> MARGINALE; payback 9
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert abs(n["van"] - (-54108.81991352362)) <= 1.0
        assert n["payback"] == 9

    def test_gen_sottodimensionato_ens_positivo(self):
        # ENS 2,4 MWh/anno; C_mg +12000; risparmio
        # 75531,0; CAPEX 690000; VAN 93985,95;
        # payback 10; CONVIENTE
        n = self._bc(potenza_gen_kw=100.0)
        assert n["valid"] is True
        assert n["ens_mwh_a"] == pytest.approx(2.4, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            75531.0, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            690000.0, rel=REL)
        assert abs(n["van"] - 93985.9512818188) <= 1.0
        assert n["payback"] == 10
        assert n["verdetto"] == "CONVIENTE"

    def test_pv_zero_ancora_calcolabile(self):
        # E_pv 0; risparmio 20136,0; VAN
        # -220995,21; payback None (mai entro
        # 15 anni); NON_CONVIENTE
        n = self._bc(potenza_pv_kw=0.0)
        assert n["valid"] is True
        assert n["energia_pv_mwh_a"] == 0.0
        assert n["energia_rete_mwh_a"] == pytest.approx(
            800.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            20136.0, rel=REL)
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_opex_200000_neutro_risparmio_negativo(self):
        n = self._bc(opex_eur_a=200000.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_f_auto_zero_risparmio_minore(self):
        n = self._bc(f_autoconsumo=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            59811.0, rel=REL)
        assert n["energia_export_mwh_a"] == pytest.approx(
            217.5, rel=REL)

    def test_voll_zero_risparmio_minore(self):
        # C_base 176000,0; risparmio 51531,0;
        # payback 15; NON_CONVIENTE
        n = self._bc(voll_eur_mwh=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            51531.0, rel=REL)
        assert n["payback"] == 15
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_eventi_zero_senza_isola(self):
        n = self._bc(n_eventi_a=0)
        assert n["valid"] is True
        assert n["ore_isola_h_a"] == 0
        assert n["energia_gen_mwh_a"] == 0.0
        assert n["litri_carburante_l_a"] == 0.0
        assert n["risparmio_eur_a"] == pytest.approx(
            52395.0, rel=REL)

    def test_eta_rt_zero_neutro(self):
        n = self._bc(eta_rt=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_rt_sopra_uno_neutro(self):
        n = self._bc(eta_rt=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_carico_zero_neutro(self):
        n = self._bc(carico_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eventi_non_interi_neutro(self):
        n = self._bc(n_eventi_a=2.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(resa_kwh_kwp_a=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(carico_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(carico_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -730000 + 87531 x 15 =
        # 582965,0 -> CONVIENTE
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISPARMIO_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_pv_eur_kw=0.0,
                     costo_batt_eur_kwh=0.0,
                     costo_gen_eur_kw=0.0,
                     costo_fisso_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh707_neutro"]()
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
        n = _F["_mh707_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "carico_mwh_a",
                       "potenza_pv_kw",
                       "resa_kwh_kwp_a",
                       "f_autoconsumo",
                       "batteria_kwh",
                       "dod_frac",
                       "cicli_a",
                       "eta_rt",
                       "energia_pv_mwh_a",
                       "energia_auto_mwh_a",
                       "energia_shift_mwh_a",
                       "energia_export_mwh_a",
                       "energia_rete_mwh_a",
                       "ore_isola_h_a",
                       "energia_isola_mwh_a",
                       "energia_gen_mwh_a",
                       "litri_carburante_l_a",
                       "costo_carburante_eur_a",
                       "ens_mwh_a",
                       "costo_base_eur_a",
                       "costo_microgrid_eur_a",
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
        assert len(b["df_tabella"]) == 42
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia PV (MWh/anno)" in voci
        assert "Autoconsumo diretto (MWh/anno)" in voci
        assert "Energia spostata batteria (MWh/anno)" in voci
        assert "Export residuo (MWh/anno)" in voci
        assert "Energia da rete (MWh/anno)" in voci
        assert "Energia in isola (MWh/anno)" in voci
        assert "ENS microgrid (MWh/anno)" in voci
        assert "Costo baseline (EUR/anno)" in voci
        assert "Costo microgrid (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISPARMIO_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh707_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh707_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh707_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo_rete(self):
        s = _F["mh707_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_voll(self):
        s = _F["mh707_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh707_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh707_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # Prezzo rete x0.9 (198) e VoLL x0.9
        # (4500): risparmio 77347,50 > 0, VAN
        # 72840,60
        s = _F["mh707_sensitivita"](self._ing())
        assert s.loc["x0.9", "x0.9"] != 0.0
        assert abs(s.loc["x0.9", "x0.9"] - 72840.60010817391) <= 1.0
        ing = self._ing()
        ing["prezzo_rete_eur_mwh"] = 220.0 * 0.9
        ing["voll_eur_mwh"] = 5000.0 * 0.9
        assert _F["mh707_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            77347.5, rel=REL)

    def test_sensitivita_angoli(self):
        s = _F["mh707_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x1.1"] - 147574.13798307418) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 209509.55749689788) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 284243.09537179815) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh707_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 49

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh707_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_microgrid_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "carico_mwh_a" in txt
        assert "energia_pv_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "resa_kwh_kwp_a" in txt
        assert "costo_fisso_eur" in txt
        assert "ens_mwh_a" in txt
        assert "energia_gen_mwh_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh707_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "energia_pv_mwh_a;330.0" in txt
        assert "opex_eur_a;15000.0" in txt
        assert f"litri_carburante_l_a;{bc['litri_carburante_l_a']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def707["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def707\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 27, ui_keys
        demo_keys = set(_F["mh707_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh707_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh707_demo():")
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
        ui_keys = set(re.findall(r'_def707\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W708 (25/10/2026) - tab707' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh707_num", "mh707_nneg", "mh707_pos",
                     "mh707_int_pos", "mh707_int_nneg",
                     "mh707_quota_valida", "mh707_eta_valido",
                     "mh707_energia_pv", "mh707_autoconsumo",
                     "mh707_energia_shift",
                     "mh707_export_residuo", "mh707_energia_rete",
                     "mh707_ore_isola", "mh707_energia_isola",
                     "mh707_energia_batt_evento",
                     "mh707_energia_gen_evento",
                     "mh707_litri_carburante",
                     "mh707_costo_carburante", "mh707_ens",
                     "mh707_costo_base", "mh707_costo_microgrid",
                     "mh707_risparmio", "mh707_capex_microgrid",
                     "mh707_co2_evitata", "mh707_crf",
                     "mh707_van", "mh707_tir", "mh707_payback",
                     "mh707_verdetto", "mh707_valida",
                     "_mh707_neutro", "mh707_calcola",
                     "mh707_sensitivita", "mh707_csv",
                     "mh707_demo", "demo_calcoli"):
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
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w708_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE707) == 1

    def test_blocco_with_tab707(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab707:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE707

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st707_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 32, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st707_") for k in keys)

    def test_chiavi_st_input_sono_28(self):
        """Le 28 chiavi di input/bottone (27 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st707_[a-z0-9_]+)"', _ui_src())
        attese = ["st707_carico", "st707_pv",
                  "st707_resa", "st707_f_auto",
                  "st707_batteria", "st707_dod",
                  "st707_cicli", "st707_eta",
                  "st707_carico_isola", "st707_eventi",
                  "st707_durata", "st707_gen",
                  "st707_consumo", "st707_carburante",
                  "st707_voll", "st707_prezzo_rete",
                  "st707_prezzo_export", "st707_opex",
                  "st707_costo_pv", "st707_costo_batt",
                  "st707_costo_gen", "st707_costo_fisso",
                  "st707_fattore_rete", "st707_fattore_gen",
                  "st707_vita", "st707_wacc",
                  "st707_tolleranza", "st707_calcola"]
        assert len(attese) == 28
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg707" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg707") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg707")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia PV (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver707" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_microgrid_presente(self):
        src = _ui_src().lower()
        assert "isola" in src
        assert "batteria" in src
        assert "generatore" in src
        assert "black-start" in src
        assert "coordin" in src
        assert "voll" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "black-start" in src.lower()
        assert "genset" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo baseline (sola rete + danno blackout)" in src
        assert "Costo microgrid (rete + carburante + OPEX + ENS)" in src
        assert "Risparmio annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh707_csv" in src
        assert "microgrid_isola_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh707_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo rete" in src
        assert "VoLL" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st707_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W708 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab707:")
        assert "mh707_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab707" in (_new_dir() / "w708_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w708_helpers.py", "w708_ui.py",
                   "w708_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab707"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "6"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w708_helpers.py", "w708_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_microgrid_isola(self):
        assert "Microgrid" in TITLE707
        assert "isola" in TITLE707.lower()
