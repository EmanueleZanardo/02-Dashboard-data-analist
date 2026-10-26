"""Test tab718 "🌊🔥 Pompa di calore ad acqua di mare: il mare scalda la città?"

Tab precedente tab717 (ferro-aria, w718);
nuova tab tab718 (acqua di mare, w719). La tab718
replica ESATTAMENTE la semantica economica
delle tab650-717: flussi [-CAPEX_delta,
risparmio con sostituzioni], VAN/TIR (bisezione
[-99 %, +500 %], None se risparmio <= 0 o nessun
cambio di segno incl. tutti flussi >= 0)/payback
(0 se cumulato anno 0 >= 0), verdetto CONVIENTE
(VAN >= 0)/MARGINALE (VAN < 0 entro toll % di
|CAPEX_delta|; CAPEX_delta == 0 mai MARGINALE)/
NON_CONVIENTE/NON_CALCOLABILE (validazione
fallita o risparmio <= 0), sostituzioni multipli
interi di floor(vita_anni) con 1 <= anno < vita
progetto, flusso anno sostituzione = risparmio -
CAPEX_alt + CAPEX_base.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda termica 10000 MWh/a; ore equivalenti
2000 h; SCOP ad acqua di mare 3,2; rendimento
caldaia 0,90; prezzo gas 80 EUR/MWh; prezzo
elettricita' 110 EUR/MWh; costo pompa di calore
700 EUR/kW_th; costo fisso presa a mare 800000
EUR; costo caldaia 150 EUR/kW_th; costo fisso
caldaia 100000 EUR; opex pompa di calore 120000
EUR/anno; opex caldaia 60000 EUR/anno; vita
pompa di calore 20 anni; vita caldaia 15 anni;
vita di progetto 25 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del |CAPEX_delta|);
fattore gas 0,20 t/MWh; fattore elettricita'
0,25 t/MWh.

- potenza_th_kw = 5000.0
- potenza_el_kw = 1562.5
- gas_mwh_a = 11111.111111111111
- el_mwh_a = 3125.0
- costo_base_eur_a = 948888.8888888889
- costo_alt_eur_a = 463750.0
- risparmio_eur_a = 485138.8888888889
- capex_hp_eur = 4300000.0
- capex_boiler_eur = 850000.0
- capex_delta_eur = 3450000.0
- anni_sost_hp = [20]
- anni_sost_boiler = [15]
- co2_evitata_t_a = 1440.9722222222222
- van = 2175760.363855966
- tir = 12.319345248865881
- payback = 8
- verdetto = 'CONVIENTE'

Scomposizione: P_th 10000 x 1000 / 2000 =
5000.0 kW; P_el 5000.0 / 3,2 = 1562.5 kW;
gas 10000 / 0,90 = 11111.111111111111 MWh/a;
el 10000 / 3,2 = 3125.0 MWh/a; C_base
11111.111111111111 x 80 + 60000 =
948888.8888888889 EUR/anno; C_alt 3125.0 x
110 + 120000 = 463750.0 EUR/anno; risparmio
948888.8888888889 - 463750.0 =
485138.8888888889 EUR/anno; CAPEX_hp 5000.0
x 700 + 800000 = 4300000.0 EUR; CAPEX_boiler
5000.0 x 150 + 100000 = 850000.0 EUR;
CAPEX_delta 4300000.0 - 850000.0 = 3450000.0
EUR; sostituzioni: floor(20) = 20, multipli
20 < 25 -> [20] per la pompa di calore;
floor(15) = 15, multipli 15 < 25 -> [15]
per la caldaia; flussi: anno 0 -3450000.0,
anni 1-14 e 16-19 e 21-25 risparmio
485138.8888888889, anno 15 risparmio +
CAPEX_boiler = 1335138.888888889, anno 20
risparmio - CAPEX_hp = -3814861.111111111;
VAN 2175760.363855966 a WACC 5 % su 25
anni; TIR 12.319345248865881 % (il tasso che
azzera il VAN dei flussi sopra); payback 8
(il cumulato diventa positivo all'anno 8:
-3450000.0 + 7 x 485138.8888888889 =
-54027.7777777778 all'anno 7, poi +485138.8888888889
all'anno 8 = 431111.1111111111 >= 0); CO2
11111.111111111111 x 0,20 - 3125.0 x 0,25 =
1440.9722222222222 t/anno (positiva e
INFORMATIVA: il gas risparmiato pesa piu'
dell'elettricita' consumata); VAN >= 0 ->
CONVIENTE.

Formula flussi negli anni di sostituzione
(ESATTA delle tab precedenti, copiata):
flusso_0 = -CAPEX_delta; flusso_t (t >= 1) =
risparmio - (CAPEX_alt se t e' anno di
sostituzione alt) + (CAPEX_base se t e' anno
di sostituzione base).
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
    if (p / "w719_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w719_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w719_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w719_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w719_helpers.py: {missing}")
    return out


_F = _load("mh718_num", "mh718_nneg", "mh718_pos",
           "mh718_int_pos", "mh718_int_nneg",
           "mh718_eta_valido", "mh718_potenza_th",
           "mh718_energia_gas", "mh718_energia_el",
           "mh718_costo_annuo", "mh718_risparmio",
           "mh718_capex", "mh718_anni_sostituzione",
           "mh718_flussi", "mh718_van_flussi",
           "mh718_tir_flussi", "mh718_payback_flussi",
           "mh718_verdetto", "mh718_co2_evitata",
           "mh718_valida", "_mh718_neutro",
           "mh718_calcola", "mh718_sensitivita",
           "mh718_csv", "mh718_demo", "demo_calcoli")

TITLE718 = ("🌊🔥 Pompa di calore ad acqua di mare: "
            "il mare scalda la città?")

P_TH_DEMO = 5000.0
P_EL_DEMO = 1562.5
GAS_DEMO = 11111.111111111111
EL_DEMO = 3125.0
C_BASE_DEMO = 948888.8888888889
C_ALT_DEMO = 463750.0
RISPARMIO_DEMO = 485138.8888888889
CAPEX_HP_DEMO = 4300000.0
CAPEX_BOILER_DEMO = 850000.0
DELTA_DEMO = 3450000.0
CO2_DEMO = 1440.9722222222222
VAN_DEMO = 2175760.363855966
TIR_DEMO = 12.319345248865881
PAYBACK_DEMO = 8
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w719_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w719_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh718_demo"]()
        d.update(kw)
        return _F["mh718_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh718_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh718_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh718_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh718_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh718_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh718_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh718_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh718_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh718_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh718_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh718_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero(self):
        assert _F["mh718_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh718_int_nneg"](-1, "x")

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh718_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh718_eta_valido"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh718_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_valore_interno(self):
        assert _F["mh718_eta_valido"](0.90, "x") == 0.90

    def test_scop_senza_tetto_superiore(self):
        # Brief tab718: SCOP > 0 senza tetto
        # (e' un coefficiente di prestazione,
        # non un rendimento).
        assert _F["mh718_pos"](5.5, "x") == 5.5
        assert self._val(scop_mare=5.5)["valido"] is True
        assert self._val(scop_mare=8.0)["valido"] is True

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        assert self._val(domanda_mwh_a=0.0)["valido"] is False

    def test_domanda_negativa_non_valida(self):
        assert self._val(domanda_mwh_a=-1.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_eq=0.0)["valido"] is False

    def test_scop_zero_non_valido(self):
        assert self._val(scop_mare=0.0)["valido"] is False

    def test_scop_negativo_non_valido(self):
        assert self._val(scop_mare=-1.0)["valido"] is False

    def test_eta_fuori_intervallo_non_valida(self):
        assert self._val(eta_caldaia=0.0)["valido"] is False
        assert self._val(eta_caldaia=1.2)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh", "prezzo_el_eur_mwh",
                  "costo_hp_eur_kw", "fisso_mare_eur",
                  "costo_boiler_eur_kw", "fisso_boiler_eur",
                  "opex_hp_eur_a", "opex_boiler_eur_a",
                  "wacc_frac", "tolleranza_frac",
                  "fattore_gas_t_mwh", "fattore_el_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vite_zero_non_valide(self):
        assert self._val(vita_hp_anni=0)["valido"] is False
        assert self._val(vita_boiler_anni=0)["valido"] is False

    def test_vite_non_intere_non_valide(self):
        assert self._val(vita_hp_anni=20.5)["valido"] is False
        assert self._val(vita_boiler_anni=15.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=24.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        # Brief tab718: toll >= 0 senza tetto
        # superiore (come le tab precedenti).
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(scop_mare=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(domanda_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_hp_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(scop_mare="3.2")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(costo_hp_eur_kw=0.0)["valido"] is True
        assert self._val(fisso_mare_eur=0.0)["valido"] is True
        assert self._val(opex_hp_eur_a=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_el_t_mwh=0.0)["valido"] is True


class TestFunzioni:
    def test_potenza_th_demo(self):
        assert _F["mh718_potenza_th"](
            10000.0, 2000.0) == pytest.approx(P_TH_DEMO, rel=REL)

    def test_potenza_th_cresce_con_domanda(self):
        assert _F["mh718_potenza_th"](
            20000.0, 2000.0) == pytest.approx(10000.0, rel=REL)

    def test_energia_gas_demo(self):
        assert _F["mh718_energia_gas"](
            10000.0, 0.90) == pytest.approx(GAS_DEMO, rel=REL)

    def test_energia_el_demo(self):
        assert _F["mh718_energia_el"](
            10000.0, 3.2) == pytest.approx(EL_DEMO, rel=REL)

    def test_energia_el_cresce_con_scop_basso(self):
        assert _F["mh718_energia_el"](
            10000.0, 1.5) > _F["mh718_energia_el"](10000.0, 3.2)

    def test_costo_annuo_demo(self):
        assert _F["mh718_costo_annuo"](
            GAS_DEMO, 80.0, 60000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert _F["mh718_costo_annuo"](
            EL_DEMO, 110.0, 120000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh718_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh718_risparmio"](
            100000.0, 150000.0) == pytest.approx(-50000.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh718_capex"](
            P_TH_DEMO, 700.0, 800000.0) == pytest.approx(
            CAPEX_HP_DEMO, rel=REL)
        assert _F["mh718_capex"](
            P_TH_DEMO, 150.0, 100000.0) == pytest.approx(
            CAPEX_BOILER_DEMO, rel=REL)

    def test_capex_delta_demo(self):
        delta = _F["mh718_capex"](
            P_TH_DEMO, 700.0, 800000.0) - _F["mh718_capex"](
            P_TH_DEMO, 150.0, 100000.0)
        assert delta == pytest.approx(DELTA_DEMO, rel=REL)

    def test_anni_sostituzione_demo(self):
        assert _F["mh718_anni_sostituzione"](20, 25) == [20]
        assert _F["mh718_anni_sostituzione"](15, 25) == [15]

    def test_anni_sostituzione_multipli(self):
        assert _F["mh718_anni_sostituzione"](10, 25) == [10, 20]
        assert _F["mh718_anni_sostituzione"](5, 25) == [5, 10, 15, 20]

    def test_anni_sostituzione_floor_non_intero(self):
        # Vita 10,5 anni -> floor 10: anni 10, 20.
        assert _F["mh718_anni_sostituzione"](10.5, 25) == [10, 20]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh718_anni_sostituzione"](0.5, 25) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh718_anni_sostituzione"](25, 25) == []
        assert _F["mh718_anni_sostituzione"](20, 25) == [20]

    def test_co2_evitata_demo(self):
        assert _F["mh718_co2_evitata"](
            GAS_DEMO, EL_DEMO, 0.20, 0.25) == pytest.approx(
            CO2_DEMO, rel=REL)
        assert CO2_DEMO > 0.0

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh718_co2_evitata"](
            5000.0, 10000.0, 0.20, 0.25) == pytest.approx(
            -1500.0, rel=REL)

    def test_co2_evitata_zero_se_fattori_zero(self):
        assert _F["mh718_co2_evitata"](
            GAS_DEMO, EL_DEMO, 0.0, 0.0) == pytest.approx(
            0.0, abs=1e-9)

    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 14 + \
            [RISPARMIO_DEMO + CAPEX_BOILER_DEMO] + \
            [RISPARMIO_DEMO] * 4 + \
            [RISPARMIO_DEMO - CAPEX_HP_DEMO] + \
            [RISPARMIO_DEMO] * 5
        assert len(flussi) == 26
        assert abs(_F["mh718_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * 25
        assert _F["mh718_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh718_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_con_sostituzioni(self):
        flussi = _F["mh718_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_BOILER_DEMO, CAPEX_HP_DEMO, [15], [20], 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[14] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[15] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_BOILER_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_HP_DEMO, rel=REL)
        assert flussi[25] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_hp(self):
        # Anno di sostituzione HP -> risparmio - CAPEX_hp.
        flussi = _F["mh718_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_BOILER_DEMO, CAPEX_HP_DEMO, [], [20], 25)
        assert flussi[20] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_HP_DEMO, rel=REL)
        assert flussi[19] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_boiler(self):
        # Anno di sostituzione caldaia -> risparmio + CAPEX_boiler.
        flussi = _F["mh718_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_BOILER_DEMO, CAPEX_HP_DEMO, [15], [], 25)
        assert flussi[15] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_BOILER_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_entrambi(self):
        # Stesso anno per entrambi i rami: i due
        # termini si sommano.
        flussi = _F["mh718_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_BOILER_DEMO, CAPEX_HP_DEMO, [10], [10], 25)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_HP_DEMO + CAPEX_BOILER_DEMO,
            rel=REL)

    def test_tir_demo(self):
        flussi = _F["mh718_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_BOILER_DEMO, CAPEX_HP_DEMO, [15], [20], 25)
        tir = _F["mh718_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh718_tir_flussi"](
            [1000.0] + [100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh718_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_otto(self):
        flussi = _F["mh718_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_BOILER_DEMO, CAPEX_HP_DEMO, [15], [20], 25)
        assert _F["mh718_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh718_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4

    def test_payback_none_se_mai(self):
        assert _F["mh718_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 25) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh718_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh718_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh718_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh718_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh718_verdetto"](
            -0.10 * abs(DELTA_DEMO), DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh718_verdetto"](
            -0.10 * abs(DELTA_DEMO) - 1.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh718_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh718_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh718_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh718_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh718_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_accetta_tolleranza_sopra_uno(self):
        assert _F["mh718_verdetto"](
            -100.0, DELTA_DEMO, 1.5,
            RISPARMIO_DEMO) == "MARGINALE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh718_demo"]()
        d.update(kw)
        return _F["mh718_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_th_kw"] == pytest.approx(
            P_TH_DEMO, rel=REL)
        assert c["potenza_el_kw"] == pytest.approx(
            P_EL_DEMO, rel=REL)
        assert c["gas_mwh_a"] == pytest.approx(
            GAS_DEMO, rel=REL)
        assert c["el_mwh_a"] == pytest.approx(
            EL_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_hp_eur"] == pytest.approx(
            CAPEX_HP_DEMO, rel=REL)
        assert c["capex_boiler_eur"] == pytest.approx(
            CAPEX_BOILER_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_sost_hp"] == [20]
        assert c["anni_sost_boiler"] == [15]
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh718_demo"]()
        b = _F["mh718_calcola"](**d)
        coppie = [("potenza_th_kw", P_TH_DEMO),
                  ("potenza_el_kw", P_EL_DEMO),
                  ("gas_mwh_a", GAS_DEMO),
                  ("el_mwh_a", EL_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_hp_eur", CAPEX_HP_DEMO),
                  ("capex_boiler_eur", CAPEX_BOILER_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sost_hp"] == [20]
        assert b["anni_sost_boiler"] == [15]
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh718_demo"]()
        assert d["domanda_mwh_a"] == 10000.0
        assert d["ore_eq"] == 2000.0
        assert d["scop_mare"] == 3.2
        assert d["eta_caldaia"] == 0.90
        assert d["prezzo_gas_eur_mwh"] == 80.0
        assert d["prezzo_el_eur_mwh"] == 110.0
        assert d["costo_hp_eur_kw"] == 700.0
        assert d["fisso_mare_eur"] == 800000.0
        assert d["costo_boiler_eur_kw"] == 150.0
        assert d["fisso_boiler_eur"] == 100000.0
        assert d["opex_hp_eur_a"] == 120000.0
        assert d["opex_boiler_eur_a"] == 60000.0
        assert d["vita_hp_anni"] == 20
        assert d["vita_boiler_anni"] == 15
        assert d["vita_progetto_anni"] == 25
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_gas_t_mwh"] == 0.20
        assert d["fattore_el_t_mwh"] == 0.25
        assert len(d) == 19

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_th_kw",
                       "potenza_el_kw",
                       "gas_mwh_a",
                       "el_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_hp_eur",
                       "capex_boiler_eur",
                       "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sost_hp"]) in doc
        assert repr(c["anni_sost_boiler"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_el_alto_risparmio_negativo(self):
        # Prezzo elettricita' 300 EUR/MWh: C_alt
        # 1057500 > C_base 948888,89 -> risparmio
        # negativo -> dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_el_eur_mwh=300.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_prezzo_gas_basso_risparmio_negativo(self):
        # Prezzo gas 30 EUR/MWh: C_base 393333,33
        # < C_alt 463750 -> risparmio negativo
        # -> dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_gas_eur_mwh=30.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_scop_basso_non_conviente(self):
        # SCOP 1,5: risparmio 95555,56, VAN
        # -3315005,54, TIR -45,13 %, payback None
        # -> NON_CONVIENTE.
        n = self._bc(scop_mare=1.5)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            95555.5555555555, rel=REL)
        assert abs(n["van"] - (-3315005.539998968)) <= 1.0
        assert abs(n["tir"] - (-45.132164551691226)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_hp_alto_non_conviente(self):
        # Costo pompa di calore 1500 EUR/kW_th:
        # CAPEX_delta 7450000, VAN -3331797,57,
        # TIR -24,76 %, payback 15 -> NON_CONVIENTE.
        n = self._bc(costo_hp_eur_kw=1500.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            7450000.0, rel=REL)
        assert abs(n["van"] - (-3331797.567636036)) <= 1.0
        assert abs(n["tir"] - (-24.764590811335385)) <= 0.01
        assert n["payback"] == 15
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_hp_marginale(self):
        # Costo pompa di calore 1050 EUR/kW_th:
        # CAPEX_delta 5200000, VAN -233796,23 entro
        # la tolleranza 520000 -> MARGINALE.
        n = self._bc(costo_hp_eur_kw=1050.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            5200000.0, rel=REL)
        assert abs(n["van"] - (-233796.23117178472)) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_prezzo_el_medio_non_conviente(self):
        # Prezzo elettricita' 200 EUR/MWh:
        # risparmio 203888,89, VAN -1788161,55,
        # TIR -30,77 %, payback 15 -> NON_CONVIENTE.
        n = self._bc(prezzo_el_eur_mwh=200.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            203888.88888888888, rel=REL)
        assert abs(n["van"] - (-1788161.54534412)) <= 1.0
        assert abs(n["tir"] - (-30.774702578168977)) <= 0.01
        assert n["payback"] == 15
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_vite_corte_sostituzioni_entrambi(self):
        # Vita 10 anni per entrambi: sost [10, 20]
        # per entrambi; flusso anno 10 = risparmio
        # - CAPEX_hp + CAPEX_boiler; VAN -30748,83,
        # TIR 4,87 %, payback 8 -> MARGINALE.
        n = self._bc(vita_hp_anni=10, vita_boiler_anni=10)
        assert n["valid"] is True
        assert n["anni_sost_hp"] == [10, 20]
        assert n["anni_sost_boiler"] == [10, 20]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-2964861.111111111, rel=REL)
        assert abs(n["van"] - (-30748.83379492702)) <= 1.0
        assert abs(n["tir"] - 4.8708919611270245) <= 0.01
        assert n["payback"] == 8
        assert n["verdetto"] == "MARGINALE"

    def test_vite_diverse_sostituzioni(self):
        # Vita HP 12 anni, caldaia 8 anni: sost HP
        # [12, 24], caldaia [8, 16, 24]; VAN
        # 888093,67 -> CONVIENTE.
        n = self._bc(vita_hp_anni=12, vita_boiler_anni=8)
        assert n["anni_sost_hp"] == [12, 24]
        assert n["anni_sost_boiler"] == [8, 16, 24]
        assert abs(n["van"] - 888093.6696109702) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_caldaia=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_scop_zero_neutro(self):
        n = self._bc(scop_mare=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(scop_mare=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_hp_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -3450000 + 485138,89 x 25 + 850000 -
        # 4300000 = 5228472,22.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            5228472.222222224, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh718_neutro"]()
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
        n = _F["_mh718_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_mwh_a", "ore_eq",
                       "scop_mare", "eta_caldaia",
                       "potenza_th_kw", "potenza_el_kw",
                       "gas_mwh_a", "el_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_hp_eur",
                       "capex_boiler_eur",
                       "capex_delta_eur",
                       "anni_sost_hp",
                       "anni_sost_boiler",
                       "co2_evitata_t_a",
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
        assert len(b["df_tabella"]) == 28
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza termica (kW)" in voci
        assert "Gas consumato (MWh/a)" in voci
        assert "Elettricita' consumata (MWh/a)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX pompa di calore (EUR)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-DELTA_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[15] == \
            pytest.approx(RISPARMIO_DEMO + CAPEX_BOILER_DEMO,
                          rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[20] == \
            pytest.approx(RISPARMIO_DEMO - CAPEX_HP_DEMO,
                          rel=REL)


class TestSensitivita:
    def _ing(self):
        return _F["mh718_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh718_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh718_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_scop(self):
        s = _F["mh718_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_el(self):
        # Un prezzo dell'elettricita' piu' alto
        # alza il costo della pompa di calore e
        # riduce il risparmio.
        s = _F["mh718_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh718_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh718_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh718_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 2175760.363855967) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 1099139.5983942137) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 3056631.899233764) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 2175760.363855966) <= 1.0

    def test_sensitivita_diagonale_simmetrica(self):
        # SCOP e prezzo variati dello stesso
        # fattore si compensano (el x prezzo
        # invariato): la diagonale x0.9/x0.9 e
        # x1.1/x1.1 coincide col centro.
        s = _F["mh718_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - VAN_DEMO) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vite 10 anni per entrambi la griglia
        # deve includere le sostituzioni anni 10
        # e 20: il centro deve coincidere col VAN
        # del caso con vite 10 anni.
        ing = self._ing()
        ing["vita_hp_anni"] = 10
        ing["vita_boiler_anni"] = 10
        s = _F["mh718_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - (-30748.83379492702)) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh718_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh718_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 34

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh718_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_mwh_a" in txt
        assert "potenza_th_kw" in txt
        assert "co2_evitata_t_a" in txt
        assert "scop_mare" in txt
        assert "capex_delta_eur" in txt
        assert "fisso_mare_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh718_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "domanda_mwh_a;10000.0" in txt
        assert "opex_hp_eur_a;120000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def718["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def718\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh718_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh718_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh718_demo():")
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
        ui_keys = set(re.findall(r'_def718\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W719 (26/10/2026) - tab718' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh718_num", "mh718_nneg", "mh718_pos",
                     "mh718_int_pos", "mh718_int_nneg",
                     "mh718_eta_valido", "mh718_potenza_th",
                     "mh718_energia_gas", "mh718_energia_el",
                     "mh718_costo_annuo", "mh718_risparmio",
                     "mh718_capex", "mh718_anni_sostituzione",
                     "mh718_flussi", "mh718_van_flussi",
                     "mh718_tir_flussi", "mh718_payback_flussi",
                     "mh718_verdetto", "mh718_co2_evitata",
                     "mh718_valida", "_mh718_neutro",
                     "mh718_calcola", "mh718_sensitivita",
                     "mh718_csv", "mh718_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        # I frammenti nuovi usano solo mh718 /
        # tab718 / st718: nessun identificatore
        # della numerazione successiva.
        assert "mh719" not in _helpers_src()
        assert "mh719" not in _ui_src()
        assert "st719" not in _ui_src()
        assert "tab719" not in _ui_src()

    def test_nessun_residuo_tab_precedente(self):
        # Niente residui della tab precedente
        # (mh717 / tab717 / st717) in helpers/UI:
        # il test puo' citare tab717 come tab
        # precedente, i frammenti no.
        assert "mh717" not in _helpers_src()
        assert "mh717" not in _ui_src()
        assert "st717" not in _ui_src()
        assert "tab717" not in _helpers_src()
        assert "tab717" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab717 (ferro-aria)
        # come punto di confronto e la nuova tab
        # e' tab718.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab717" in src
        assert "tab718" in src
        assert _ui_src().startswith("    with tab718:")

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w719_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE718) == 1

    def test_blocco_with_tab718(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab718:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE718

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st718_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st718_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st718_[a-z0-9_]+)"', _ui_src())
        attese = ["st718_domanda", "st718_ore",
                  "st718_scop", "st718_eta",
                  "st718_p_gas", "st718_p_el",
                  "st718_c_hp", "st718_fisso_mare",
                  "st718_c_boiler", "st718_fisso_boiler",
                  "st718_opex_hp", "st718_opex_boiler",
                  "st718_vita_hp", "st718_vita_boiler",
                  "st718_vita_progetto", "st718_wacc",
                  "st718_tolleranza", "st718_f_gas",
                  "st718_f_el", "st718_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg718" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg718") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg718")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Potenza termica (kW)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "acqua di mare" in src
        assert "sorgente" in src
        assert "presa a mare" in src
        assert "aerotermica" in src
        assert "falda" in src
        assert "sonde" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline (caldaia a gas)" in src
        assert "Costo annuo alternativa (pompa di calore ad acqua di mare)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh718_csv" in src
        assert "pompa_calore_acqua_mare_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh718_sensitivita" in src
        assert "Heatmap" in src
        assert "SCOP" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st718_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W719 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab718:")
