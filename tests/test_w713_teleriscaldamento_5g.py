"""Test tab713 "🔥♻️ Teleriscaldamento 5G: l'anello a bassa temperatura paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
calore utile annuo 10000 MWh_th/anno; COP
medio 3,5; rendimento caldaia 0,90; quota
ausiliaria 0,02 MWh_e/MWh_th; prezzo del gas
80 EUR/MWh; prezzo elettrico 90 EUR/MWh;
potenza di picco 5 MW_th; costo rete 800
EUR/kW_th; costo fisso rete 300000 EUR;
costo fisso caldaia 400000 EUR; opex rete
80000 EUR/anno; opex caldaia 50000 EUR/anno;
vita in anni rete 25; vita in anni caldaia
15; vita di progetto 25 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del |CAPEX
delta|); fattore gas 0,20 t/MWh; fattore
elettrico 0,10 t/MWh.

- e_gas_mwh_a = 11111.111111111111
- e_pdc_mwh_a = 2857.1428571428573
- e_aux_mwh_a = 200.0
- e_alt_mwh_a = 3057.1428571428573
- costo_base_eur_a = 938888.8888888889
- costo_alt_eur_a = 355142.85714285716
- risparmio_eur_a = 583746.0317460317
- capex_rete_eur = 4300000.0
- capex_caldaia_eur = 400000.0
- capex_delta_eur = 3900000.0
- anni_sost_rete = []
- anni_sost_caldaia = [15]
- co2_evitata_t_a = 1916.5079365079364
- van = 4519691.051313556
- tir = 14.672589542480575
- payback = 7
- verdetto = 'CONVIENTE'

Scomposizione: E_gas 10000 / 0,90 =
11111.111111111111 MWh/anno; E_pdc 10000 /
3,5 = 2857.1428571428573 MWh_e/anno; E_aux
10000 x 0,02 = 200.0 MWh_e/anno; E_alt
2857.1428571428573 + 200.0 =
3057.1428571428573 MWh_e/anno; C_base
11111.111111111111 x 80 + 50000 =
938888.8888888889; C_alt 3057.1428571428573
x 90 + 80000 = 355142.85714285716;
risparmio 938888.8888888889 -
355142.85714285716 = 583746.0317460317;
CAPEX rete 5 x 1000 x 800 + 300000 =
4300000.0; CAPEX caldaia 400000.0; CAPEX
delta 4300000.0 - 400000.0 = 3900000.0;
vite 25 anni rete e 15 anni caldaia:
nessuna sostituzione rete entro 25 anni e
sostituzione caldaia all'anno 15; flussi
[-3900000.0, 583746.0317460317 x 25 con
flusso anno 15 = 983746.0317460317]; VAN
4519691.051313556 a WACC 5 % su 25 anni;
TIR 14.672589542480575 % (il VAN si azzera
a quel tasso); payback 7 (cumulato anno 6
= -397523,81 < 0, cumulato anno 7 =
186222,22 >= 0); VAN >= 0 -> CONVIENTE.
CO2: 11111.111111111111 x 0,20 -
3057.1428571428573 x 0,10 =
1916.5079365079364 t/anno (positiva: il
gas evitato pesa piu' dell'elettricita'
delle PdC, ma puo' diventare negativa con
elettricita' sporca).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w714_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w714_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w714_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w714_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w714_helpers.py: {missing}")
    return out


_F = _load("mh713_num", "mh713_nneg", "mh713_pos",
           "mh713_int_pos", "mh713_int_nneg",
           "mh713_quota_valida", "mh713_eta_valido",
           "mh713_cop_valido",
           "mh713_e_gas", "mh713_e_alt", "mh713_capex_rete",
           "mh713_costo_annuo",
           "mh713_risparmio", "mh713_anni_sostituzione",
           "mh713_flussi",
           "mh713_van_flussi", "mh713_tir_flussi",
           "mh713_payback_flussi", "mh713_verdetto",
           "mh713_co2_evitata", "mh713_valida",
           "_mh713_neutro", "mh713_calcola",
           "mh713_sensitivita", "mh713_csv",
           "mh713_demo", "demo_calcoli")

TITLE713 = ("🔥♻️ Teleriscaldamento 5G: l'anello "
            "a bassa temperatura paga?")

E_GAS_DEMO = 11111.111111111111
E_PDC_DEMO = 2857.1428571428573
E_AUX_DEMO = 200.0
E_ALT_DEMO = 3057.1428571428573
C_BASE_DEMO = 938888.8888888889
C_ALT_DEMO = 355142.85714285716
RISPARMIO_DEMO = 583746.0317460317
CX_RETE_DEMO = 4300000.0
CX_CALDAIA_DEMO = 400000.0
DELTA_DEMO = 3900000.0
CO2_EV_DEMO = 1916.5079365079364
VAN_DEMO = 4519691.051313556
TIR_DEMO = 14.672589542480575
PAYBACK_DEMO = 7
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w714_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w714_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh713_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh713_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh713_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh713_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh713_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh713_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh713_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh713_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh713_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh713_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh713_int_pos"](25.0, "x") == 25

    def test_int_nneg_accetta_zero(self):
        assert _F["mh713_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh713_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh713_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh713_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh713_quota_valida"](0.0, "x") == 0.0
        assert _F["mh713_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh713_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh713_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh713_eta_valido"](1.0, "x") == 1.0

    def test_cop_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh713_cop_valido"](0.0, "x")

    def test_cop_rifiuta_sopra_dieci(self):
        with pytest.raises(ValueError):
            _F["mh713_cop_valido"](10.1, "x")

    def test_cop_accetta_sopra_uno_e_dieci(self):
        assert _F["mh713_cop_valido"](3.5, "x") == 3.5
        assert _F["mh713_cop_valido"](10.0, "x") == 10.0

    def test_cop_distinto_da_rendimento(self):
        # Un COP puo' superare 1 (a differenza di
        # un rendimento): 3,5 e' valido qui ma
        # non lo sarebbe per mh713_eta_valido.
        assert _F["mh713_cop_valido"](3.5, "x") == 3.5
        with pytest.raises(ValueError):
            _F["mh713_eta_valido"](3.5, "x")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh713_demo"]()
        d.update(kw)
        return _F["mh713_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_q_zero_non_valido(self):
        assert self._val(q_anno_mwh_a=0.0)["valido"] is False

    def test_q_negativo_non_valido(self):
        assert self._val(q_anno_mwh_a=-1.0)["valido"] is False

    def test_cop_zero_non_valido(self):
        assert self._val(cop_medio=0.0)["valido"] is False

    def test_cop_sopra_dieci_non_valido(self):
        assert self._val(cop_medio=10.1)["valido"] is False

    def test_cop_dieci_valido(self):
        assert self._val(cop_medio=10.0)["valido"] is True

    def test_eta_caldaia_zero_non_valido(self):
        assert self._val(eta_caldaia=0.0)["valido"] is False

    def test_eta_caldaia_sopra_uno_non_valido(self):
        assert self._val(eta_caldaia=1.1)["valido"] is False

    def test_eta_caldaia_uno_valida(self):
        assert self._val(eta_caldaia=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("quota_aux", "p_gas_eur_mwh",
                  "p_elettrica_eur_mwh", "c_rete_eur_kw",
                  "fisso_rete_eur", "fisso_caldaia_eur",
                  "opex_rete_eur_a", "opex_caldaia_eur_a",
                  "wacc_frac", "f_gas_t_mwh",
                  "f_elettrica_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_picco_zero_non_valido(self):
        assert self._val(p_picco_mw=0.0)["valido"] is False

    def test_vita_anni_zero_non_valida(self):
        assert self._val(vita_anni_rete=0)["valido"] is False
        assert self._val(vita_anni_caldaia=0)["valido"] is False

    def test_vita_anni_non_intera_non_valida(self):
        assert self._val(vita_anni_rete=24.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=24.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(cop_medio=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(q_anno_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(q_anno_mwh_a=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(cop_medio="3.5")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(p_elettrica_eur_mwh=0.0)["valido"] is True
        assert self._val(c_rete_eur_kw=0.0)["valido"] is True
        assert self._val(opex_rete_eur_a=0.0)["valido"] is True
        assert self._val(fisso_rete_eur=0.0)["valido"] is True
        assert self._val(quota_aux=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_e_gas_demo(self):
        assert _F["mh713_e_gas"](
            10000.0, 0.90) == pytest.approx(E_GAS_DEMO, rel=REL)

    def test_e_gas_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh713_e_gas"](10000.0, 0.0)

    def test_e_alt_demo(self):
        assert _F["mh713_e_alt"](
            10000.0, 3.5, 0.02) == pytest.approx(
            E_ALT_DEMO, rel=REL)

    def test_e_alt_senza_ausiliari(self):
        assert _F["mh713_e_alt"](
            10000.0, 3.5, 0.0) == pytest.approx(
            E_PDC_DEMO, rel=REL)

    def test_e_alt_rifiuta_cop_zero(self):
        with pytest.raises(ValueError):
            _F["mh713_e_alt"](10000.0, 0.0, 0.02)

    def test_capex_rete_demo(self):
        assert _F["mh713_capex_rete"](
            5.0, 800.0, 300000.0) == pytest.approx(
            CX_RETE_DEMO, rel=REL)

    def test_capex_rete_conversione_mw_kw(self):
        # 1 MW x 1000 = 1000 kW: il fattore 1000
        # deve esserci (senza, il CAPEX sarebbe
        # 1000 volte piu' piccolo).
        assert _F["mh713_capex_rete"](
            1.0, 800.0, 0.0) == pytest.approx(800000.0, rel=REL)

    def test_costo_base_demo(self):
        assert _F["mh713_costo_annuo"](
            E_GAS_DEMO, 80.0, 50000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_alt_demo(self):
        assert _F["mh713_costo_annuo"](
            E_ALT_DEMO, 90.0, 80000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh713_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh713_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_anni_sostituzione_demo(self):
        assert _F["mh713_anni_sostituzione"](25, 25) == []
        assert _F["mh713_anni_sostituzione"](15, 25) == [15]

    def test_anni_sostituzione_multipli(self):
        assert _F["mh713_anni_sostituzione"](5, 25) == [5, 10, 15, 20]
        assert _F["mh713_anni_sostituzione"](10, 25) == [10, 20]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh713_anni_sostituzione"](0.5, 25) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh713_anni_sostituzione"](25, 25) == []

    def test_co2_evitata_demo_positiva(self):
        assert _F["mh713_co2_evitata"](
            E_GAS_DEMO, E_ALT_DEMO,
            0.20, 0.10) == pytest.approx(CO2_EV_DEMO, rel=REL)
        assert CO2_EV_DEMO > 0.0

    def test_co2_evitata_negativa_se_elettricita_sporca(self):
        assert _F["mh713_co2_evitata"](
            E_GAS_DEMO, E_ALT_DEMO,
            0.20, 0.80) == pytest.approx(-223.4920634920636, rel=REL)


class TestFinanza:
    def test_van_flussi_demo_con_sostituzione(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        flussi[15] = RISPARMIO_DEMO + CX_CALDAIA_DEMO
        assert abs(_F["mh713_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_formula_chiusa_senza_sostituzioni(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-25)) / 0.05
        assert _F["mh713_van_flussi"](
            flussi, 0.05) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        assert _F["mh713_van_flussi"](
            flussi, 0.0) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 25, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh713_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_con_sostituzione_caldaia(self):
        flussi = _F["mh713_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_CALDAIA_DEMO, CX_RETE_DEMO, [15], [], 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[15] == pytest.approx(
            983746.0317460317, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_con_sostituzione_entrambi(self):
        flussi = _F["mh713_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_CALDAIA_DEMO, CX_RETE_DEMO, [15], [10, 20], 25)
        assert flussi[10] == pytest.approx(
            -3716253.9682539683, rel=REL)
        assert flussi[15] == pytest.approx(
            983746.0317460317, rel=REL)

    def test_tir_demo_verifica_npv_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        flussi[15] = RISPARMIO_DEMO + CX_CALDAIA_DEMO
        tir = _F["mh713_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)
        npv = -DELTA_DEMO + sum(
            flussi[i] / (1.0 + tir) ** i
            for i in range(1, 26))
        assert abs(npv) <= 1e-6 * DELTA_DEMO

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh713_tir_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh713_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_sette(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        flussi[15] = RISPARMIO_DEMO + CX_CALDAIA_DEMO
        assert _F["mh713_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh713_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai(self):
        assert _F["mh713_payback_flussi"](
            [-50000000.0] + [RISPARMIO_DEMO] * 25) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh713_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh713_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh713_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh713_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh713_verdetto"](
            -390000.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh713_verdetto"](
            -390001.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh713_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh713_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh713_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh713_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"
        assert _F["mh713_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh713_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh713_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh713_demo"]()
        d.update(kw)
        return _F["mh713_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_gas_mwh_a"] == pytest.approx(
            E_GAS_DEMO, rel=REL)
        assert c["e_pdc_mwh_a"] == pytest.approx(
            E_PDC_DEMO, rel=REL)
        assert c["e_aux_mwh_a"] == pytest.approx(
            E_AUX_DEMO, rel=REL)
        assert c["e_alt_mwh_a"] == pytest.approx(
            E_ALT_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_rete_eur"] == pytest.approx(
            CX_RETE_DEMO, rel=REL)
        assert c["capex_caldaia_eur"] == pytest.approx(
            CX_CALDAIA_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_sost_rete"] == []
        assert c["anni_sost_caldaia"] == [15]
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=1e-9)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh713_demo"]()
        b = _F["mh713_calcola"](**d)
        coppie = [("e_gas_mwh_a", E_GAS_DEMO),
                  ("e_pdc_mwh_a", E_PDC_DEMO),
                  ("e_aux_mwh_a", E_AUX_DEMO),
                  ("e_alt_mwh_a", E_ALT_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_rete_eur", CX_RETE_DEMO),
                  ("capex_caldaia_eur", CX_CALDAIA_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert b["tir"] == pytest.approx(TIR_DEMO, rel=1e-9)
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh713_demo"]()
        assert d["q_anno_mwh_a"] == 10000.0
        assert d["cop_medio"] == 3.5
        assert d["eta_caldaia"] == 0.90
        assert d["quota_aux"] == 0.02
        assert d["p_gas_eur_mwh"] == 80.0
        assert d["p_elettrica_eur_mwh"] == 90.0
        assert d["p_picco_mw"] == 5.0
        assert d["c_rete_eur_kw"] == 800.0
        assert d["fisso_rete_eur"] == 300000.0
        assert d["fisso_caldaia_eur"] == 400000.0
        assert d["opex_rete_eur_a"] == 80000.0
        assert d["opex_caldaia_eur_a"] == 50000.0
        assert d["vita_anni_rete"] == 25
        assert d["vita_anni_caldaia"] == 15
        assert d["vita_progetto_anni"] == 25
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["f_gas_t_mwh"] == 0.20
        assert d["f_elettrica_t_mwh"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_gas_mwh_a",
                       "e_pdc_mwh_a", "e_aux_mwh_a",
                       "e_alt_mwh_a",
                       "costo_base_eur_a", "costo_alt_eur_a",
                       "risparmio_eur_a", "capex_rete_eur",
                       "capex_caldaia_eur", "capex_delta_eur",
                       "co2_evitata_t_a", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 7" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_cop_basso_marginale(self):
        # COP 1,5: E_alt 6866,67, C_alt 698000,
        # risparmio 240888,89; VAN -312518,51
        # entro tolleranza 390000 -> MARGINALE
        n = self._bc(cop_medio=1.5)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            240888.88888888888, rel=REL)
        assert abs(n["van"] - (-312518.5141874995)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 15

    def test_prezzo_elettrico_alto_non_conviente(self):
        # Prezzo elettrico 250: C_alt 844285,71,
        # risparmio 94603,17; VAN -2374261,26;
        # payback mai entro 25 anni
        n = self._bc(p_elettrica_eur_mwh=250.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            94603.17460317456, rel=REL)
        assert abs(n["van"] - (-2374261.2621346167)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_opex_rete_alto_non_conviente(self):
        # Opex rete 600000: risparmio 63746,03;
        # VAN -2809160,12 -> NON_CONVIENTE
        n = self._bc(opex_rete_eur_a=600000.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            63746.03174603172, rel=REL)
        assert abs(n["van"] - (-2809160.1230297117)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_rete_marginale(self):
        # Costo rete 1720 EUR/kW_th: delta
        # 8500000; VAN -80308,95 entro
        # tolleranza 850000 -> MARGINALE;
        # payback 15
        n = self._bc(c_rete_eur_kw=1720.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            8500000.0, rel=REL)
        assert abs(n["van"] - (-80308.94868644353)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 15

    def test_costo_rete_non_conviente(self):
        # Costo rete 1900 EUR/kW_th: delta
        # 9400000; VAN -980308,95 oltre
        # tolleranza 940000 -> NON_CONVIENTE;
        # payback 16
        n = self._bc(c_rete_eur_kw=1900.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            9400000.0, rel=REL)
        assert abs(n["van"] - (-980308.948686443)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 16

    def test_capex_delta_zero_mai_marginale(self):
        # Tutti i costi CAPEX a zero -> delta 0
        n = self._bc(c_rete_eur_kw=0.0, fisso_rete_eur=0.0,
                     fisso_caldaia_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_sostituzione_rete(self):
        # Vita anni rete 10: sostituzioni 10,
        # 20; flusso anno 10 = -3716253,97;
        # VAN 259239,28 circa
        n = self._bc(vita_anni_rete=10)
        assert n["valid"] is True
        assert n["anni_sost_rete"] == [10, 20]
        assert n["anni_sost_caldaia"] == [15]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-3716253.9682539683, rel=REL)
        assert abs(n["van"] - 259239.28473439103) <= 1.0

    def test_cop_zero_neutro(self):
        n = self._bc(cop_medio=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cop_sopra_dieci_neutro(self):
        n = self._bc(cop_medio=10.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_q_zero_neutro(self):
        n = self._bc(q_anno_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_anni_zero_neutro(self):
        n = self._bc(vita_anni_rete=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(cop_medio=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(q_anno_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(q_anno_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -3900000 + 583746,03 x 25
        # + 400000 (sostituzione caldaia anno 15
        # non scontata) = 11093650,79
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            11093650.793650793, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh713_neutro"]()
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
        n = _F["_mh713_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "q_anno_mwh_a", "cop_medio",
                       "eta_caldaia", "quota_aux",
                       "e_gas_mwh_a", "e_pdc_mwh_a",
                       "e_aux_mwh_a", "e_alt_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_rete_eur",
                       "capex_caldaia_eur",
                       "capex_delta_eur",
                       "anni_sost_rete",
                       "anni_sost_caldaia",
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
        assert "Energia gas (MWh/anno)" in voci
        assert "Energia PdC (MWh_e/anno)" in voci
        assert "Energia ausiliaria (MWh_e/anno)" in voci
        assert "Energia alternativa (MWh_e/anno)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[15] == \
            pytest.approx(983746.0317460317, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-DELTA_DEMO, rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh713_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh713_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh713_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cop(self):
        s = _F["mh713_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettrico(self):
        s = _F["mh713_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_diagonale_non_uguale_centro(self):
        # A differenza di tab712, qui il termine
        # ausiliario Q x quota_aux non scala col
        # COP: sulla diagonale il VAN NON resta
        # quello del centro (proprieta'
        # strutturale, non errore).
        s = _F["mh713_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) > 1.0
        assert abs(s.loc["x1.1", "x1.1"] - VAN_DEMO) > 1.0

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh713_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh713_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh713_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 4545060.151532439) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 3688953.690177835) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 5203997.81955531) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 4494321.951094679) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita anni rete 10 la griglia deve
        # includere le sostituzioni: il centro
        # deve coincidere col VAN del caso con
        # sostituzione rete
        ing = self._ing()
        ing["vita_anni_rete"] = 10
        s = _F["mh713_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 259239.28473439103) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh713_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 35

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh713_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "q_anno_mwh_a" in txt
        assert "e_alt_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "cop_medio" in txt
        assert "capex_rete_eur" in txt
        assert "capex_delta_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh713_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "q_anno_mwh_a;10000.0" in txt
        assert "opex_rete_eur_a;80000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def713["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def713\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh713_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh713_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh713_demo():")
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
        ui_keys = set(re.findall(r'_def713\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W714 (25/10/2026) - tab713' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh713_num", "mh713_nneg", "mh713_pos",
                     "mh713_int_pos", "mh713_int_nneg",
                     "mh713_quota_valida", "mh713_eta_valido",
                     "mh713_cop_valido",
                     "mh713_e_gas", "mh713_e_alt",
                     "mh713_capex_rete", "mh713_costo_annuo",
                     "mh713_risparmio", "mh713_anni_sostituzione",
                     "mh713_flussi",
                     "mh713_van_flussi", "mh713_tir_flussi",
                     "mh713_payback_flussi", "mh713_verdetto",
                     "mh713_co2_evitata", "mh713_valida",
                     "_mh713_neutro", "mh713_calcola",
                     "mh713_sensitivita", "mh713_csv",
                     "mh713_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        # La tab precedente e' la tab712 (batteria
        # a sabbia): i frammenti nuovi non devono
        # contenere i suoi identificatori.
        assert "mh712" not in _helpers_src()
        assert "tab712" not in _helpers_src()
        assert "mh712" not in _ui_src()
        assert "tab712" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Catena: questo file test fa riferimento
        # alla tab precedente tab712 come punto di
        # confronto (test residuo sopra) e la
        # nuova tab e' tab713.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab712" in src
        assert "tab713" in src
        assert _ui_src().startswith("    with tab713:")

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w714_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE713) == 1

    def test_blocco_with_tab713(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab713:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE713

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st713_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st713_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st713_[a-z0-9_]+)"', _ui_src())
        attese = ["st713_q_anno", "st713_cop",
                  "st713_eta_caldaia", "st713_quota_aux",
                  "st713_p_gas", "st713_p_elettrica",
                  "st713_p_picco", "st713_c_rete",
                  "st713_fisso_rete", "st713_fisso_caldaia",
                  "st713_opex_rete", "st713_opex_caldaia",
                  "st713_vita_rete", "st713_vita_caldaia",
                  "st713_vita_progetto", "st713_wacc",
                  "st713_tolleranza", "st713_f_gas",
                  "st713_f_elettrica", "st713_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg713" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg713") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg713")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia elettrica alternativa (MWh_e/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver713" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "tradizionale" in src
        assert "centralizzata" in src
        assert "stagionale" in src
        assert "sabbia" in src
        assert "geotermia" in src
        assert "negativa" in src
        assert "capex" in src
        assert "anello" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "tradizionale" in src.lower()
        assert "centralizzata" in src.lower()
        assert "stagionale" in src.lower()
        assert "sabbia" in src.lower()
        assert "geotermia" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh713_csv" in src
        assert "teleriscaldamento_5g_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh713_sensitivita" in src
        assert "Heatmap" in src
        assert "COP medio" in src
        assert "Prezzo elettrico" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st713_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W714 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab713:")
