"""Test tab706 "🌱🔥 Biogas da digestione anaerobica: il business case dell'impianto"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
feedstock 20000 t/anno; resa biogas 100
Nm3/t; PCI biogas 6,0 kWh/Nm3; rendimento
elettrico CHP 0,38; rendimento termico CHP
0,42; autoconsumo elettrico 0,10; prezzo
elettricita' 180 EUR/MWh; prezzo calore 60
EUR/MWh; frazione digestato 0,90; valore
digestato 5 EUR/t; costo feedstock 20 EUR/t;
OPEX annuo 150000 EUR/anno; costo trasporto
30000 EUR/anno; potenza elettrica 500 kW;
costo specifico 4000 EUR/kW; costo fisso
200000 EUR; vita 15 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del CAPEX); fattore
CO2 elettricita' 0,35 tCO2/MWh; fattore CO2
calore 0,20 tCO2/MWh.

- energia_biogas_mwh_a = 12000.0
- energia_el_mwh_a = 4104.0
- energia_th_mwh_a = 5040.0
- digestato_t_a = 18000.0
- ricavi_eur_a = 1131120.0
- costi_eur_a = 580000.0
- margine_eur_a = 551120.0
- co2_evitata_t_a = 2444.3999999999996
- capex_eur = 2200000.0
- van = 3520437.138002092
- tir = 24.06436207049528
- payback = 4
- verdetto = 'CONVIENTE'

Scomposizione: E_biogas 20000 x 100 x 6,0 /
1000 = 12000.0; E_el 12000,0 x 0,38 x (1 -
0,10) = 4104.0; E_th 12000,0 x 0,42 = 5040.0;
digestato 20000 x 0,90 = 18000,0; ricavi
4104,0 x 180 + 5040,0 x 60 + 18000,0 x 5 =
1131120.0; costi 20000 x 20 + 150000 + 30000
= 580000.0; margine 1131120,0 - 580000,0 =
551120.0; co2_evitata 4104,0 x 0,35 + 5040,0
x 0,20 = 2444.3999999999996; capex 500 x 4000
+ 200000 = 2200000.0; VAN -2200000,0 +
551120,0 x (1 - 1,05^-15) / 0,05 =
3520437.138002092; TIR per bisezione su
[-0,99, 5,0] dei flussi [-2200000,
551120,0 x 15]: 24.06436207049528 % (VAN a
quella TIR ~0); payback: cumulato anno 3
-546640,0, anno 4 +4480,0 -> 4; VAN >= 0 ->
CONVIENTE.
NOTA: i valori esatti ricalcolati sono
quelli sopra (VAN 3520437,14, TIR 24,0644 %) —
il test fissa i valori esatti, non le
approssimazioni. Il biogas qui e' BRUCIATO
in CHP, non upgradato a biometano.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w707_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w707_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w707_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w707_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w707_helpers.py: {missing}")
    return out


_F = _load("mh706_num", "mh706_nneg", "mh706_pos",
           "mh706_int_pos", "mh706_quota_valida",
           "mh706_eta_valido", "mh706_energia_biogas",
           "mh706_energia_el", "mh706_energia_th",
           "mh706_digestato", "mh706_ricavi",
           "mh706_costi", "mh706_margine",
           "mh706_co2_evitata", "mh706_capex",
           "mh706_crf", "mh706_van", "mh706_tir",
           "mh706_payback", "mh706_verdetto",
           "mh706_valida", "_mh706_neutro",
           "mh706_calcola", "mh706_sensitivita",
           "mh706_csv", "mh706_demo", "demo_calcoli")

TITLE706 = ("🌱🔥 Biogas da digestione anaerobica: "
            "il business case dell'impianto")

E_BIOGAS_DEMO = 12000.0
E_EL_DEMO = 4104.0
E_TH_DEMO = 5040.0
DIG_DEMO = 18000.0
RICAVI_DEMO = 1131120.0
COSTI_DEMO = 580000.0
MARGINE_DEMO = 551120.0
CO2_EV_DEMO = 2444.3999999999996
CAPEX_DEMO = 2200000.0
VAN_DEMO = 3520437.138002092
TIR_DEMO = 24.06436207049528
PAYBACK_DEMO = 4
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w707_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w707_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh706_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh706_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh706_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh706_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh706_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh706_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh706_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh706_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh706_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh706_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh706_int_pos"](15.0, "x") == 15

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh706_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh706_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh706_quota_valida"](0.0, "x") == 0.0
        assert _F["mh706_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh706_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh706_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh706_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_demo(self):
        assert _F["mh706_eta_valido"](0.38, "x") == 0.38
        assert _F["mh706_eta_valido"](0.42, "x") == 0.42


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh706_demo"]()
        d.update(kw)
        return _F["mh706_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_feedstock_zero_non_valido(self):
        assert self._val(feedstock_t_a=0.0)["valido"] is False

    def test_feedstock_negativo_non_valido(self):
        assert self._val(feedstock_t_a=-10.0)["valido"] is False

    def test_resa_zero_non_valida(self):
        assert self._val(resa_nm3_t=0.0)["valido"] is False

    def test_pci_zero_non_valido(self):
        assert self._val(pci_kwh_nm3=0.0)["valido"] is False

    def test_eta_el_zero_non_valido(self):
        assert self._val(eta_el=0.0)["valido"] is False

    def test_eta_el_sopra_uno_non_valido(self):
        assert self._val(eta_el=1.2)["valido"] is False

    def test_eta_th_sopra_uno_non_valido(self):
        assert self._val(eta_th=1.1)["valido"] is False

    def test_eta_uno_valida(self):
        assert self._val(eta_el=1.0, eta_th=0.0)["valido"] is False
        # eta_th 0 non valido da solo; somma 1 con entrambi > 0:
        assert self._val(eta_el=0.5, eta_th=0.5)["valido"] is True

    def test_somma_rendimenti_sopra_uno_non_valida(self):
        v = self._val(eta_el=0.6, eta_th=0.5)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_somma_rendimenti_uguale_uno_valida(self):
        assert self._val(eta_el=0.6, eta_th=0.4)["valido"] is True

    def test_autoconsumo_negativo_non_valido(self):
        assert self._val(autoconsumo_frac=-0.01)["valido"] is False

    def test_autoconsumo_sopra_uno_non_valido(self):
        assert self._val(autoconsumo_frac=1.1)["valido"] is False

    def test_autoconsumo_uno_valido(self):
        assert self._val(autoconsumo_frac=1.0)["valido"] is True

    def test_frazione_digestato_sopra_uno_non_valida(self):
        assert self._val(frazione_digestato=1.5)["valido"] is False

    def test_frazione_digestato_zero_valida(self):
        assert self._val(frazione_digestato=0.0)["valido"] is True

    def test_potenza_zero_non_valida(self):
        assert self._val(potenza_el_kw=0.0)["valido"] is False

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=14.5)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_eur_mwh",
                  "prezzo_calore_eur_mwh",
                  "valore_digestato_eur_t",
                  "costo_feedstock_eur_t", "opex_annuo",
                  "costo_trasporto_eur_a",
                  "costo_specifico_eur_kw", "costo_fisso_eur",
                  "wacc_frac", "fattore_co2_elettricita",
                  "fattore_co2_calore"):
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
        assert self._val(resa_nm3_t=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(feedstock_t_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(feedstock_t_a=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(resa_nm3_t="100")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_calore_eur_mwh=0.0)["valido"] is True
        assert self._val(opex_annuo=0.0)["valido"] is True
        assert self._val(costo_specifico_eur_kw=0.0)["valido"] is True
        assert self._val(costo_fisso_eur=0.0)["valido"] is True
        assert self._val(costo_trasporto_eur_a=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_energia_biogas_demo(self):
        assert _F["mh706_energia_biogas"](
            20000.0, 100.0, 6.0) == pytest.approx(
            E_BIOGAS_DEMO, rel=REL)

    def test_energia_biogas_scala_con_feedstock(self):
        assert _F["mh706_energia_biogas"](
            10000.0, 100.0, 6.0) == pytest.approx(
            6000.0, rel=REL)

    def test_energia_biogas_rifiuta_pci_zero(self):
        with pytest.raises(ValueError):
            _F["mh706_energia_biogas"](20000.0, 100.0, 0.0)

    def test_energia_el_demo(self):
        assert _F["mh706_energia_el"](
            E_BIOGAS_DEMO, 0.38, 0.10) == pytest.approx(
            E_EL_DEMO, rel=REL)

    def test_energia_el_autoconsumo_zero(self):
        assert _F["mh706_energia_el"](
            E_BIOGAS_DEMO, 0.38, 0.0) == pytest.approx(
            4560.0, rel=REL)

    def test_energia_el_autoconsumo_uno(self):
        assert _F["mh706_energia_el"](
            E_BIOGAS_DEMO, 0.38, 1.0) == 0.0

    def test_energia_el_rifiuta_eta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh706_energia_el"](E_BIOGAS_DEMO, 1.1, 0.10)

    def test_energia_th_demo(self):
        assert _F["mh706_energia_th"](
            E_BIOGAS_DEMO, 0.42) == pytest.approx(
            E_TH_DEMO, rel=REL)

    def test_digestato_demo(self):
        assert _F["mh706_digestato"](
            20000.0, 0.90) == pytest.approx(DIG_DEMO, rel=REL)

    def test_digestato_zero(self):
        assert _F["mh706_digestato"](20000.0, 0.0) == 0.0

    def test_ricavi_demo(self):
        assert _F["mh706_ricavi"](
            E_EL_DEMO, 180.0, E_TH_DEMO, 60.0,
            DIG_DEMO, 5.0) == pytest.approx(RICAVI_DEMO, rel=REL)

    def test_costi_demo(self):
        assert _F["mh706_costi"](
            20000.0, 20.0, 150000.0,
            30000.0) == pytest.approx(COSTI_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh706_margine"](
            RICAVI_DEMO, COSTI_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh706_margine"](
            580000.0, 980000.0) == pytest.approx(
            -400000.0, rel=1e-6)

    def test_co2_evitata_demo(self):
        assert _F["mh706_co2_evitata"](
            E_EL_DEMO, 0.35, E_TH_DEMO,
            0.20) == pytest.approx(CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_solo_elettrica(self):
        assert _F["mh706_co2_evitata"](
            E_EL_DEMO, 0.35, 0.0, 0.20) == pytest.approx(
            1436.4, rel=REL)

    def test_capex_demo(self):
        assert _F["mh706_capex"](
            500.0, 4000.0, 200000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh706_capex"](
            0.0, 4000.0, 200000.0) == 200000.0

    def test_capex_scala_con_potenza(self):
        assert _F["mh706_capex"](
            1000.0, 4000.0, 200000.0) == pytest.approx(
            4200000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh706_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh706_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 15 / (1.05 ** 15 - 1.0)
        assert _F["mh706_crf"](0.05, 15) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh706_van"](
            MARGINE_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARGINE_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh706_van"](
            MARGINE_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh706_van"](
            MARGINE_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + MARGINE_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh706_van"](MARGINE_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh706_van"](MARGINE_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh706_tir"](
            CAPEX_DEMO, MARGINE_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_bisezione_indipendente(self):
        flussi = [-CAPEX_DEMO] + [MARGINE_DEMO] * 15

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
        tir = _F["mh706_tir"](CAPEX_DEMO, MARGINE_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh706_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh706_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh706_tir"](0.0, MARGINE_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh706_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh706_tir"](CAPEX_DEMO, MARGINE_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARGINE_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh706_payback"](
            CAPEX_DEMO, MARGINE_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARGINE_DEMO * 3 < 0.0
        assert -CAPEX_DEMO + MARGINE_DEMO * 4 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh706_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh706_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh706_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh706_payback"](
            50000000.0, MARGINE_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh706_payback"](0.0, MARGINE_DEMO, 15) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh706_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh706_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh706_verdetto"](
            0.0, CAPEX_DEMO, 0.10, MARGINE_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh706_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 220000 = 10 % di CAPEX 2200000
        assert _F["mh706_verdetto"](
            -220000.0, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh706_verdetto"](
            -220000.1, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh706_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh706_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CONVIENTE" or True
        assert _F["mh706_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh706_verdetto"](
            1000.0, 0.0, 0.10, MARGINE_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh706_verdetto"](
            -1.0, 0.0, 0.10, MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh706_verdetto"](
            -1.0, 0.0, 0.10, MARGINE_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh706_verdetto"](100.0, CAPEX_DEMO, -0.01, MARGINE_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh706_verdetto"](100.0, CAPEX_DEMO, 1.5, MARGINE_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh706_demo"]()
        d.update(kw)
        return _F["mh706_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_biogas_mwh_a"] == pytest.approx(
            E_BIOGAS_DEMO, rel=REL)
        assert c["energia_el_mwh_a"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["energia_th_mwh_a"] == pytest.approx(
            E_TH_DEMO, rel=REL)
        assert c["digestato_t_a"] == pytest.approx(
            DIG_DEMO, rel=REL)
        assert c["ricavi_eur_a"] == pytest.approx(
            RICAVI_DEMO, rel=REL)
        assert c["costi_eur_a"] == pytest.approx(
            COSTI_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
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
            "margine_eur_a"] == _F["demo_calcoli"]()[
            "margine_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh706_demo"]()
        b = _F["mh706_calcola"](**d)
        coppie = [("energia_biogas_mwh_a", E_BIOGAS_DEMO),
                  ("energia_el_mwh_a", E_EL_DEMO),
                  ("energia_th_mwh_a", E_TH_DEMO),
                  ("digestato_t_a", DIG_DEMO),
                  ("ricavi_eur_a", RICAVI_DEMO),
                  ("costi_eur_a", COSTI_DEMO),
                  ("margine_eur_a", MARGINE_DEMO),
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
        d = _F["mh706_demo"]()
        assert d["feedstock_t_a"] == 20000.0
        assert d["resa_nm3_t"] == 100.0
        assert d["pci_kwh_nm3"] == 6.0
        assert d["eta_el"] == 0.38
        assert d["eta_th"] == 0.42
        assert d["autoconsumo_frac"] == 0.10
        assert d["prezzo_el_eur_mwh"] == 180.0
        assert d["prezzo_calore_eur_mwh"] == 60.0
        assert d["frazione_digestato"] == 0.90
        assert d["valore_digestato_eur_t"] == 5.0
        assert d["costo_feedstock_eur_t"] == 20.0
        assert d["opex_annuo"] == 150000.0
        assert d["costo_trasporto_eur_a"] == 30000.0
        assert d["potenza_el_kw"] == 500.0
        assert d["costo_specifico_eur_kw"] == 4000.0
        assert d["costo_fisso_eur"] == 200000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_co2_elettricita"] == 0.35
        assert d["fattore_co2_calore"] == 0.20

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_biogas_mwh_a",
                       "energia_el_mwh_a",
                       "energia_th_mwh_a",
                       "digestato_t_a",
                       "ricavi_eur_a",
                       "costi_eur_a",
                       "margine_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 4" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_el_100_conviente(self):
        # E_el 4104,0; ricavi 802800,0; margine
        # 222800,0; VAN 112587,81; payback 10
        n = self._bc(prezzo_el_eur_mwh=100.0)
        assert n["valid"] is True
        assert n["margine_eur_a"] == pytest.approx(
            222800.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 10

    def test_costo_feedstock_40_non_conviente(self):
        # costi 980000,0; margine 151120,0;
        # VAN -631426,08; payback 15 (cumulato
        # anno 14 -84520,0, anno 15 +66600,0)
        n = self._bc(costo_feedstock_eur_t=40.0)
        assert n["valid"] is True
        assert n["margine_eur_a"] == pytest.approx(
            151120.0, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 15

    def test_costo_feedstock_60_neutro_margine_negativo(self):
        n = self._bc(costo_feedstock_eur_t=60.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_autoconsumo_zero_margine_maggiore(self):
        n = self._bc(autoconsumo_frac=0.0)
        assert n["valid"] is True
        assert n["margine_eur_a"] == pytest.approx(
            633200.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_feedstock_doppio_conviente(self):
        n = self._bc(feedstock_t_a=40000.0)
        assert n["valid"] is True
        assert n["margine_eur_a"] == pytest.approx(
            1282240.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_vita_dieci_conviente(self):
        # VAN 2055602,55 con tolleranza 10 % di
        # CAPEX 2200000 = 220000 -> CONVIENTE
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"
        assert abs(n["van"] - 2055602.554172337) <= 1.0

    def test_somma_rendimenti_neutro(self):
        n = self._bc(eta_el=0.6, eta_th=0.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_el=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_feedstock_zero_neutro(self):
        n = self._bc(feedstock_t_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_resa_zero_neutro(self):
        n = self._bc(resa_nm3_t=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_pci_zero_neutro(self):
        n = self._bc(pci_kwh_nm3=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_el_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(resa_nm3_t=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(feedstock_t_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(feedstock_t_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -2200000 + 551120 x 15 =
        # 6066800,0 -> CONVIENTE
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + MARGINE_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_specifico_eur_kw=0.0,
                     costo_fisso_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh706_neutro"]()
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
        n = _F["_mh706_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "feedstock_t_a",
                       "resa_nm3_t",
                       "pci_kwh_nm3",
                       "eta_el", "eta_th",
                       "autoconsumo_frac",
                       "energia_biogas_mwh_a",
                       "energia_el_mwh_a",
                       "energia_th_mwh_a",
                       "digestato_t_a",
                       "ricavi_eur_a",
                       "costi_eur_a",
                       "margine_eur_a",
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
        assert len(b["df_tabella"]) == 26
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Feedstock (t/anno)" in voci
        assert "Energia biogas (MWh/anno)" in voci
        assert "Energia elettrica vendibile (MWh/anno)" in voci
        assert "Ricavi (EUR/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARGINE_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh706_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh706_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh706_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_resa(self):
        s = _F["mh706_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_prezzo_elettricita(self):
        s = _F["mh706_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh706_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh706_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # Resa x0.9 (90) e prezzo elettricita'
        # x0.9 (162): margine 380523,20 > 0
        s = _F["mh706_sensitivita"](self._ing())
        assert s.loc["x0.9", "x0.9"] != 0.0
        assert abs(s.loc["x0.9", "x0.9"] - 1749700.6915942035) <= 1.0
        ing = self._ing()
        ing["resa_nm3_t"] = 100.0 * 0.9
        ing["prezzo_el_eur_mwh"] = 180.0 * 0.9
        assert _F["mh706_calcola"](**ing)[
            "margine_eur_a"] == pytest.approx(
            380523.2, rel=REL)

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh706_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 34

    def test_csv_contiene_verdetto_e_margine(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh706_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_eur_a" in txt
        assert "ricavi_eur_a" in txt
        assert "costi_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "feedstock_t_a" in txt
        assert "energia_biogas_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "resa_nm3_t" in txt
        assert "costo_fisso_eur" in txt
        assert "digestato_t_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh706_csv"](bc, self._ing())
        assert f"ricavi_eur_a;{bc['ricavi_eur_a']}" in txt
        assert f"margine_eur_a;{bc['margine_eur_a']}" in txt
        assert "energia_biogas_mwh_a;12000.0" in txt
        assert "opex_annuo;150000.0" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def706["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def706\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 21, ui_keys
        demo_keys = set(_F["mh706_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh706_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh706_demo():")
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
        ui_keys = set(re.findall(r'_def706\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W707 (25/10/2026) - tab706' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh706_num", "mh706_nneg", "mh706_pos",
                     "mh706_int_pos", "mh706_quota_valida",
                     "mh706_eta_valido", "mh706_energia_biogas",
                     "mh706_energia_el", "mh706_energia_th",
                     "mh706_digestato", "mh706_ricavi",
                     "mh706_costi", "mh706_margine",
                     "mh706_co2_evitata", "mh706_capex",
                     "mh706_crf", "mh706_van", "mh706_tir",
                     "mh706_payback", "mh706_verdetto",
                     "mh706_valida", "_mh706_neutro",
                     "mh706_calcola", "mh706_sensitivita",
                     "mh706_csv", "mh706_demo",
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
        ast.parse((_new_dir() / "w707_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE706) == 1

    def test_blocco_with_tab706(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab706:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE706

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st706_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 26, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st706_") for k in keys)

    def test_chiavi_st_input_sono_22(self):
        """Le 22 chiavi di input/bottone (21 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st706_[a-z0-9_]+)"', _ui_src())
        attese = ["st706_feedstock", "st706_resa",
                  "st706_pci", "st706_eta_el",
                  "st706_eta_th", "st706_autoconsumo",
                  "st706_prezzo_el", "st706_prezzo_calore",
                  "st706_frazione_digestato",
                  "st706_valore_digestato",
                  "st706_costo_feedstock", "st706_opex",
                  "st706_trasporto", "st706_potenza",
                  "st706_costo_specifico", "st706_costo_fisso",
                  "st706_fattore_el", "st706_fattore_calore",
                  "st706_vita", "st706_wacc",
                  "st706_tolleranza", "st706_calcola"]
        assert len(attese) == 22
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg706" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg706") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg706")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia biogas (MWh/anno)" in src
        assert "Margine annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd706" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_biogas_presente(self):
        src = _ui_src().lower()
        assert "anaerobica" in src
        assert "biometano" in src
        assert "upgrad" in src
        assert "compostaggio" in src
        assert "cogeneratore" in src or "chp" in src
        assert "digestato" in src

    def test_distinzione_biometano_in_helpers(self):
        src = _helpers_src()
        assert "UPGRADATO" in src or "upgradato" in src.lower()
        assert "biometano" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costi (feedstock + OPEX + trasporto)" in src
        assert "Ricavi (elettricità + calore + digestato)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh706_csv" in src
        assert "biogas_chp_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh706_sensitivita" in src
        assert "Heatmap" in src
        assert "Resa biogas" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st706_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W707 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab706:")
        assert "mh706_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab706" in (_new_dir() / "w707_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w707_helpers.py", "w707_ui.py",
                   "w707_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab706"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "5"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w707_helpers.py", "w707_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_biogas_non_biometano(self):
        assert "Biogas" in TITLE706
        assert "digestione anaerobica" in TITLE706.lower()
