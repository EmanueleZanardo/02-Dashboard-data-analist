"""Test tab700 "💧🔥 Pompa di calore ad acqua di falda: l'acqua del sottosuolo scalda l'edificio?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda 300 MWh/anno; picco 150 kW; salto
termico 5 K; COP 4,0; prevalenza 20 m;
rendimento pompa 0,6; prezzo elettricita'
200 EUR/MWh; OPEX annuo 1500 EUR/anno;
rendimento caldaia 0,9; prezzo gas 100
EUR/MWh; costo specifico 800 EUR/kW; costo
pozzi 30000 EUR; costo fisso 5000 EUR; vita
20 anni; WACC 5 %; tolleranza 10 % del CAPEX;
fattore gas 0,20 tCO2/MWh; fattore
elettricita' 0,35 tCO2/MWh.

- portata_l_s = 7.16674629718108
- ore_equivalenti_h = 2000.0
- potenza_pompa_kw = 2.3435260391782133
- energia_pompa_mwh_a = 4.687052078356427
- energia_compressore_mwh_a = 75.0
- energia_elettrica_mwh_a = 79.68705207835643
- costo_baseline_eur_a = 33333.33333333333
- costo_pompa_eur_a = 17437.410415671286
- risparmio_eur_a = 15895.922917662043
- co2_evitata_t_a = 38.776198439241924
- capex_eur = 155000.0
- van = 43098.334988706396
- tir = 8.092503945258441
- payback = 10
- verdetto = 'CONVIENTE'

Scomposizione: portata 150 / (4,186 x 5) =
7.16674629718108; ore 300 x 1000 / 150 =
2000.0; p_pomp 7.16674629718108 x 9,81 x 20 /
(1000 x 0,6) = 2.3435260391782133; e_pomp
2.3435260391782133 x 2000 / 1000 =
4.687052078356427; e_comp 300 / 4,0 = 75.0;
e_tot 75.0 + 4.687052078356427 =
79.68705207835643; c_hp 79.68705207835643 x
200 + 1500 = 17437.410415671286; c_base 300 /
0,9 x 100 = 33333.33333333333; risparmio
33333.33333333333 - 17437.410415671286 =
15895.922917662043; co2 300 / 0,9 x 0,20 -
79.68705207835643 x 0,35 = 38.776198439241924;
capex 150 x 800 + 30000 + 5000 = 155000.0;
VAN -155000,0 + 15895.922917662043 x
(1 - 1,05^-20) / 0,05 = 43098.334988706396;
TIR per bisezione su [-0,99, 5,0] dei flussi
[-155000, 15895.922917662043 x 20]:
8.092503945258441 % (VAN a quella TIR ~0);
payback: cumulato anno 9 -11937.30574196062,
anno 10 +3958.617175701423 -> 10.
NOTA: il brief indicava portata 7,165 L/s,
p_pomp 2,343 kW, e_pomp 4,686 MWh, e_el_tot
~79,69 MWh, c_hp ~17437 EUR, risparmio
~15896 EUR/a, CO2 ~38,78 t/a, VAN ~+43100 EUR
e TIR ~8,1 %: i valori esatti ricalcolati
sono quelli sopra (portata 7,1667, VAN
43098,33, TIR 8,0925 %) — il test fissa i
valori esatti, non le approssimazioni del
brief.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w701_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w701_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w701_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w701_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w701_helpers.py: {missing}")
    return out


_F = _load("mh700_num", "mh700_nneg", "mh700_pos",
           "mh700_int_pos", "mh700_cop_valido",
           "mh700_rendimento_valido",
           "mh700_portata", "mh700_ore_equivalenti",
           "mh700_potenza_pompa", "mh700_energia_pompa",
           "mh700_energia_compressore",
           "mh700_costo_baseline", "mh700_costo_pompa",
           "mh700_risparmio", "mh700_co2_evitata",
           "mh700_capex", "mh700_crf", "mh700_van",
           "mh700_tir", "mh700_payback",
           "mh700_verdetto", "mh700_valida",
           "_mh700_neutro", "mh700_calcola",
           "mh700_sensitivita", "mh700_csv",
           "mh700_demo", "demo_calcoli")

TITLE700 = ("💧🔥 Pompa di calore ad acqua di falda: "
            "l'acqua del sottosuolo scalda "
            "l'edificio?")

PORTATA_DEMO = 7.16674629718108
ORE_DEMO = 2000.0
P_POMP_DEMO = 2.3435260391782133
E_POMP_DEMO = 4.687052078356427
E_COMP_DEMO = 75.0
E_EL_DEMO = 79.68705207835643
C_BASE_DEMO = 33333.33333333333
C_HP_DEMO = 17437.410415671286
RISP_DEMO = 15895.922917662043
CO2_DEMO = 38.776198439241924
CAPEX_DEMO = 155000.0
VAN_DEMO = 43098.334988706396
TIR_DEMO = 8.092503945258441
PAYBACK_DEMO = 10
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.08024258719069129

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w701_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w701_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh700_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh700_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh700_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh700_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh700_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh700_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh700_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh700_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh700_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh700_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh700_int_pos"](20.0, "x") == 20

    def test_cop_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh700_cop_valido"](1.0, "x")

    def test_cop_rifiuta_sotto_uno(self):
        with pytest.raises(ValueError):
            _F["mh700_cop_valido"](0.5, "x")

    def test_cop_accetta_sopra_uno(self):
        assert _F["mh700_cop_valido"](4.0, "x") == 4.0

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh700_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh700_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh700_rendimento_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh700_demo"]()
        d.update(kw)
        return _F["mh700_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_cop_uno_non_valido(self):
        v = self._val(cop=1.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_cop_sotto_uno_non_valido(self):
        v = self._val(cop=0.8)
        assert v["valido"] is False

    def test_delta_t_zero_non_valido(self):
        v = self._val(delta_t_k=0.0)
        assert v["valido"] is False

    def test_delta_t_negativo_non_valido(self):
        v = self._val(delta_t_k=-1.0)
        assert v["valido"] is False

    def test_eta_pompa_zero_non_valida(self):
        v = self._val(eta_pompa=0.0)
        assert v["valido"] is False

    def test_eta_pompa_sopra_uno_non_valida(self):
        v = self._val(eta_pompa=1.2)
        assert v["valido"] is False

    def test_rendimento_caldaia_zero_non_valido(self):
        v = self._val(rendimento_caldaia=0.0)
        assert v["valido"] is False

    def test_rendimento_caldaia_sopra_uno_non_valido(self):
        v = self._val(rendimento_caldaia=1.2)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=19.5)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("domanda_mwh_a", "potenza_picco_kw",
                  "prevalenza_m",
                  "prezzo_elettricita_eur_mwh", "opex_annuo",
                  "prezzo_gas_eur_mwh",
                  "costo_specifico_eur_kw", "costo_pozzi_eur",
                  "costo_fisso_eur",
                  "wacc_pct", "tolleranza_pct",
                  "fattore_gas", "fattore_elettricita"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_nan_non_valido(self):
        v = self._val(cop=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(domanda_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(domanda_mwh_a=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(cop="4.0")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(domanda_mwh_a=0.0)["valido"] is True
        assert self._val(potenza_picco_kw=0.0)["valido"] is True
        assert self._val(
            prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(prevalenza_m=0.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_pct=150.0)["valido"] is True
        assert self._val(tolleranza_pct=150.0)["valido"] is True


class TestFisicaEconomia:
    def test_portata_demo(self):
        assert _F["mh700_portata"](
            150.0, 5.0) == pytest.approx(PORTATA_DEMO, rel=REL)

    def test_portata_picco_zero(self):
        assert _F["mh700_portata"](0.0, 5.0) == 0.0

    def test_portata_rifiuta_dt_zero(self):
        with pytest.raises(ValueError):
            _F["mh700_portata"](150.0, 0.0)

    def test_portata_dimezza_con_dt_doppio(self):
        assert _F["mh700_portata"](
            150.0, 10.0) == pytest.approx(PORTATA_DEMO / 2.0,
                                          rel=REL)

    def test_ore_equivalenti_demo(self):
        assert _F["mh700_ore_equivalenti"](
            300.0, 150.0) == pytest.approx(ORE_DEMO, rel=REL)

    def test_ore_equivalenti_picco_zero(self):
        assert _F["mh700_ore_equivalenti"](300.0, 0.0) == 0.0

    def test_potenza_pompa_demo(self):
        assert _F["mh700_potenza_pompa"](
            PORTATA_DEMO, 20.0, 0.6) == pytest.approx(
            P_POMP_DEMO, rel=REL)

    def test_potenza_pompa_prevalenza_zero(self):
        assert _F["mh700_potenza_pompa"](
            PORTATA_DEMO, 0.0, 0.6) == 0.0

    def test_potenza_pompa_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh700_potenza_pompa"](PORTATA_DEMO, 20.0, 0.0)

    def test_energia_pompa_demo(self):
        assert _F["mh700_energia_pompa"](
            P_POMP_DEMO, ORE_DEMO) == pytest.approx(
            E_POMP_DEMO, rel=REL)

    def test_energia_compressore_demo(self):
        assert _F["mh700_energia_compressore"](
            300.0, 4.0) == pytest.approx(E_COMP_DEMO, rel=REL)

    def test_energia_compressore_rifiuta_cop_uno(self):
        with pytest.raises(ValueError):
            _F["mh700_energia_compressore"](300.0, 1.0)

    def test_costo_baseline_demo(self):
        assert _F["mh700_costo_baseline"](
            300.0, 0.9, 100.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_baseline_rifiuta_rendimento_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh700_costo_baseline"](300.0, 1.2, 100.0)

    def test_costo_pompa_demo(self):
        assert _F["mh700_costo_pompa"](
            E_EL_DEMO, 200.0, 1500.0) == pytest.approx(
            C_HP_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh700_risparmio"](
            C_BASE_DEMO, C_HP_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh700_risparmio"](
            10000.0, 17437.410415671286) == pytest.approx(
            -7437.410415671286, rel=REL)

    def test_co2_demo(self):
        assert _F["mh700_co2_evitata"](
            300.0, 0.9, 0.20,
            E_EL_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_puo_essere_negativa(self):
        assert _F["mh700_co2_evitata"](
            300.0, 0.9, 0.05,
            E_EL_DEMO, 0.90) < 0.0

    def test_capex_demo(self):
        assert _F["mh700_capex"](
            150.0, 800.0, 30000.0, 5000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_pozzi_e_fisso(self):
        assert _F["mh700_capex"](
            0.0, 800.0, 30000.0, 5000.0) == 35000.0

    def test_capex_scala_con_picco(self):
        assert _F["mh700_capex"](
            300.0, 800.0, 30000.0, 5000.0) == pytest.approx(
            275000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh700_crf"](
            0.05, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh700_crf"](0.0, 20) == pytest.approx(
            0.05, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 20 / (1.05 ** 20 - 1.0)
        assert _F["mh700_crf"](0.05, 20) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh700_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-20)) / 0.05
        assert _F["mh700_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh700_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh700_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh700_van"](RISP_DEMO, -1.0, 0.05, 20)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh700_tir"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_bisezione_indipendente(self):
        flussi = [-CAPEX_DEMO] + [RISP_DEMO] * 20

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
        tir = _F["mh700_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh700_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh700_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh700_tir"](0.0, RISP_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh700_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh700_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 21))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh700_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 9 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 10 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh700_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh700_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh700_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh700_payback"](
            50000000.0, RISP_DEMO, 20) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh700_payback"](0.0, RISP_DEMO, 20) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh700_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh700_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh700_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh700_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 15500 = 10 % di CAPEX 155000
        assert _F["mh700_verdetto"](
            -15500.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh700_verdetto"](
            -15500.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh700_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh700_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh700_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh700_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh700_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh700_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh700_demo"]()
        d.update(kw)
        return _F["mh700_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["portata_l_s"] == pytest.approx(
            PORTATA_DEMO, rel=REL)
        assert c["ore_equivalenti_h"] == pytest.approx(
            ORE_DEMO, rel=REL)
        assert c["potenza_pompa_kw"] == pytest.approx(
            P_POMP_DEMO, rel=REL)
        assert c["energia_pompa_mwh_a"] == pytest.approx(
            E_POMP_DEMO, rel=REL)
        assert c["energia_compressore_mwh_a"] == pytest.approx(
            E_COMP_DEMO, rel=REL)
        assert c["energia_elettrica_mwh_a"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_pompa_eur_a"] == pytest.approx(
            C_HP_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
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
        d = _F["mh700_demo"]()
        b = _F["mh700_calcola"](**d)
        coppie = [("portata_l_s", PORTATA_DEMO),
                  ("ore_equivalenti_h", ORE_DEMO),
                  ("potenza_pompa_kw", P_POMP_DEMO),
                  ("energia_pompa_mwh_a", E_POMP_DEMO),
                  ("energia_compressore_mwh_a", E_COMP_DEMO),
                  ("energia_elettrica_mwh_a", E_EL_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_pompa_eur_a", C_HP_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh700_demo"]()
        assert d["domanda_mwh_a"] == 300.0
        assert d["potenza_picco_kw"] == 150.0
        assert d["delta_t_k"] == 5.0
        assert d["cop"] == 4.0
        assert d["prevalenza_m"] == 20.0
        assert d["eta_pompa"] == 0.6
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["opex_annuo"] == 1500.0
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 100.0
        assert d["costo_specifico_eur_kw"] == 800.0
        assert d["costo_pozzi_eur"] == 30000.0
        assert d["costo_fisso_eur"] == 5000.0
        assert d["vita_anni"] == 20
        assert d["wacc_pct"] == 5.0
        assert d["tolleranza_pct"] == 10.0
        assert d["fattore_gas"] == 0.20
        assert d["fattore_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("portata_l_s",
                       "ore_equivalenti_h",
                       "potenza_pompa_kw",
                       "energia_pompa_mwh_a",
                       "energia_compressore_mwh_a",
                       "energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 10" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_domanda_dimezzata(self):
        # Domanda 150 MWh/a (picco invariato):
        # ore 1000; e_comp 37,5; e_pomp 2,3435;
        # e_tot 39,8435; c_base 16666,6667; c_hp
        # 9468,7052; risparmio 7197,9615; co2
        # 19,3881; capex invariato 155000,0
        n = self._bc(domanda_mwh_a=150.0)
        assert n["valid"] is True
        assert n["ore_equivalenti_h"] == pytest.approx(
            1000.0, rel=REL)
        assert n["energia_elettrica_mwh_a"] == pytest.approx(
            39.843526039178215, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            7197.961458831021, rel=REL)
        assert n["co2_evitata_t_a"] == pytest.approx(
            19.388099219620962, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_cop_cinque(self):
        # COP 5,0: e_comp 60,0; e_tot 64,6871;
        # c_hp 14437,4104; risparmio 18895,9229
        n = self._bc(cop=5.0)
        assert n["valid"] is True
        assert n["energia_compressore_mwh_a"] == pytest.approx(
            60.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            18895.922917662043, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_cop_uno_neutro(self):
        n = self._bc(cop=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["errore"] != ""
        assert n["tir"] is None
        assert n["payback"] is None

    def test_cop_sotto_uno_neutro(self):
        n = self._bc(cop=0.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_delta_t_zero_neutro(self):
        n = self._bc(delta_t_k=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_pompa_zero_neutro(self):
        n = self._bc(eta_pompa=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_sopra_uno_neutro(self):
        n = self._bc(rendimento_caldaia=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_zero_neutro(self):
        n = self._bc(rendimento_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=19.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        n = self._bc(vita_anni=1)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_vita_tredici_marginale(self):
        # VAN circa -5680,49, entro il 10 % del
        # CAPEX (15500); payback 10
        n = self._bc(vita_anni=13)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 10

    def test_vita_undici_non_conviente(self):
        # VAN circa -22961,88, oltre il 10 % del
        # CAPEX; payback 10 (ma VAN negativo)
        n = self._bc(vita_anni=11)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 10

    def test_vita_quattordici_conviente(self):
        n = self._bc(vita_anni=14)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(cop=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(domanda_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_zero_neutro_via_risparmio(self):
        n = self._bc(domanda_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["tir"] is None
        assert n["payback"] is None

    def test_risparmio_negativo_neutro(self):
        # Prezzo elettricita' 600: c_hp 49312,23
        # contro c_base 33333,33 -> risparmio < 0
        n = self._bc(prezzo_elettricita_eur_mwh=600.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_specifico_eur_kw=0.0,
                     costo_pozzi_eur=0.0,
                     costo_fisso_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh700_neutro"]()
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
        n = _F["_mh700_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "portata_l_s", "ore_equivalenti_h",
                       "potenza_pompa_kw",
                       "energia_pompa_mwh_a",
                       "energia_compressore_mwh_a",
                       "energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
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
        assert len(b["df_tabella"]) == 27
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Portata di falda (L/s)" in voci
        assert "Energia elettrica totale (MWh/anno)" in voci
        assert "Costo baseline (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh700_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh700_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh700_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cop(self):
        s = _F["mh700_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettricita(self):
        s = _F["mh700_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh700_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh700_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # COP x0.9 (3,6) e prezzo x1.1 (220):
        # risparmio 12468,85 > 0, quindi VAN
        # non degenere
        s = _F["mh700_sensitivita"](self._ing())
        assert s.loc["x0.9", "x1.1"] != 0.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh700_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 33

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh700_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_pompa_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_mwh_a" in txt
        assert "portata_l_s" in txt
        assert "energia_elettrica_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "cop" in txt
        assert "costo_pozzi_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh700_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"portata_l_s;{PORTATA_DEMO}" in txt
        assert "opex_annuo;1500.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def700["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def700\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 18, ui_keys
        demo_keys = set(_F["mh700_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh700_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh700_demo():")
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
        ui_keys = set(re.findall(r'_def700\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W701 (25/10/2026) - tab700' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh700_num", "mh700_nneg", "mh700_pos",
                     "mh700_int_pos", "mh700_cop_valido",
                     "mh700_rendimento_valido",
                     "mh700_portata", "mh700_ore_equivalenti",
                     "mh700_potenza_pompa", "mh700_energia_pompa",
                     "mh700_energia_compressore",
                     "mh700_costo_baseline",
                     "mh700_costo_pompa",
                     "mh700_risparmio", "mh700_co2_evitata",
                     "mh700_capex", "mh700_crf",
                     "mh700_van", "mh700_tir",
                     "mh700_payback", "mh700_verdetto",
                     "mh700_valida", "_mh700_neutro",
                     "mh700_calcola", "mh700_sensitivita",
                     "mh700_csv", "mh700_demo",
                     "demo_calcoli"):
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
        ast.parse((_new_dir() / "w701_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE700) == 1

    def test_blocco_with_tab700(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab700:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE700

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st700_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 23, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st700_") for k in keys)

    def test_chiavi_st_input_sono_19(self):
        """Le 19 chiavi di input/bottone del brief
        (18 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st700_[a-z0-9_]+)"', _ui_src())
        attese = ["st700_domanda", "st700_picco",
                  "st700_delta_t", "st700_cop",
                  "st700_prevalenza", "st700_eta_pompa",
                  "st700_prezzo_elettricita", "st700_opex",
                  "st700_rendimento", "st700_prezzo_gas",
                  "st700_fattore_gas",
                  "st700_fattore_elettricita",
                  "st700_costo_specifico", "st700_costo_pozzi",
                  "st700_costo_fisso",
                  "st700_vita", "st700_wacc_pct",
                  "st700_tolleranza_pct", "st700_calcola"]
        assert len(attese) == 19
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg700" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg700") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg700")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia elettrica annua (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd700" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_acqua_falda_presente(self):
        src = _ui_src().lower()
        assert "falda" in src
        assert "pozzo" in src
        assert "reimmissione" in src
        assert "autorizzazione" in src
        assert "cop" in src
        assert "aerotermica" in src
        assert "sonde" in src
        assert "10" in src
        assert "prevalenza" in src
        assert "salto termico" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline caldaia a gas" in src
        assert "Pompa di calore" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh700_csv" in src
        assert "pompa_calore_acqua_falda_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh700_sensitivita" in src
        assert "Heatmap" in src
        assert "COP" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st700_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W701 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab700:")
        assert "mh700_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab700" in (_new_dir() / "w701_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w701_helpers.py", "w701_ui.py",
                   "w701_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab700"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "69" + "9"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w701_helpers.py", "w701_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_acqua_falda_non_aerotermica(self):
        assert "acqua di falda" in TITLE700.lower()
        assert "sottosuolo" in TITLE700.lower()
