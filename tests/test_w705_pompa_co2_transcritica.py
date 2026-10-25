"""Test tab705 "❄️🔥 Pompa di calore a CO2 transcritica: alta temperatura senza gas?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda calore 200 MWh/anno; COP 3,2;
rendimento caldaia 0,9; prezzo gas 100
EUR/MWh; prezzo elettricita' 200 EUR/MWh;
OPEX annuo 800 EUR/anno; potenza termica
100 kW; costo specifico 900 EUR/kW; costo
fisso 5000 EUR; vita 15 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del CAPEX);
fattore CO2 gas 0,20 tCO2/MWh; fattore CO2
rete 0,35 tCO2/MWh.

- energia_hp_mwh_a = 62.5
- costo_baseline_eur_a = 22222.222222222223
- costo_hp_eur_a = 13300.0
- risparmio_eur_a = 8922.222222222223
- co2_base_t_a = 44.44444444444445
- co2_hp_t_a = 21.875
- co2_evitata_t_a = 22.56944444444445
- capex_eur = 95000.0
- van = -2390.3843926775444
- tir = 4.6253722131623904
- payback = 11
- verdetto = 'MARGINALE'

Scomposizione: E_hp 200 / 3,2 = 62.5;
c_base 200 / 0,9 x 100 =
22222.222222222223; c_hp 62.5 x 200 + 800 =
13300.0; risparmio 22222.222222222223 -
13300.0 = 8922.222222222223; co2_base 200 /
0,9 x 0,20 = 44.44444444444445; co2_hp 62.5
x 0,35 = 21.875; co2_evitata
44.44444444444445 - 21.875 =
22.56944444444445; capex 100 x 900 + 5000 =
95000.0; VAN -95000,0 + 8922.222222222223 x
(1 - 1,05^-15) / 0,05 = -2390.3843926775444;
TIR per bisezione su [-0,99, 5,0] dei flussi
[-95000, 8922.222222222223 x 15]:
4.6253722131623904 % (VAN a quella TIR ~0);
payback: cumulato anno 10 -5777,7778, anno
11 +3144,4444 -> 11; VAN < 0 ma |VAN| =
2390,38 <= 10 % di CAPEX 95000 = 9500 ->
MARGINALE (non CONVIENTE, non
NON_CONVIENTE).
NOTA: i valori esatti ricalcolati sono
quelli sopra (VAN -2390,38, TIR 4,6254 %) —
il test fissa i valori esatti, non le
approssimazioni.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w706_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w706_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w706_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w706_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w706_helpers.py: {missing}")
    return out


_F = _load("mh705_num", "mh705_nneg", "mh705_pos",
           "mh705_int_pos", "mh705_quota_valida",
           "mh705_cop_valido", "mh705_eta_valido",
           "mh705_energia_hp", "mh705_costo_baseline",
           "mh705_costo_hp", "mh705_risparmio",
           "mh705_co2_base", "mh705_co2_hp",
           "mh705_co2_evitata", "mh705_capex",
           "mh705_crf", "mh705_van", "mh705_tir",
           "mh705_payback", "mh705_verdetto",
           "mh705_valida", "_mh705_neutro",
           "mh705_calcola", "mh705_sensitivita",
           "mh705_csv", "mh705_demo", "demo_calcoli")

TITLE705 = ("❄️🔥 Pompa di calore a CO2 transcritica: "
            "alta temperatura senza gas?")

EHP_DEMO = 62.5
C_BASE_DEMO = 22222.222222222223
C_HP_DEMO = 13300.0
RISP_DEMO = 8922.222222222223
CO2_BASE_DEMO = 44.44444444444445
CO2_HP_DEMO = 21.875
CO2_EV_DEMO = 22.56944444444445
CAPEX_DEMO = 95000.0
VAN_DEMO = -2390.3843926775444
TIR_DEMO = 4.6253722131623904
PAYBACK_DEMO = 11
VITA_DEMO = 15
VERDETTO_DEMO = "MARGINALE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w706_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w706_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh705_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh705_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh705_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh705_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh705_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh705_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh705_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh705_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh705_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh705_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh705_int_pos"](15.0, "x") == 15

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh705_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh705_quota_valida"](0.0, "x") == 0.0
        assert _F["mh705_quota_valida"](1.0, "x") == 1.0

    def test_cop_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_cop_valido"](1.0, "x")

    def test_cop_rifiuta_sotto_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_cop_valido"](0.5, "x")

    def test_cop_rifiuta_sopra_dieci(self):
        with pytest.raises(ValueError):
            _F["mh705_cop_valido"](10.5, "x")

    def test_cop_accetta_dieci(self):
        assert _F["mh705_cop_valido"](10.0, "x") == 10.0

    def test_cop_accetta_demo(self):
        assert _F["mh705_cop_valido"](3.2, "x") == 3.2

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh705_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh705_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_demo(self):
        assert _F["mh705_eta_valido"](0.9, "x") == 0.9


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh705_demo"]()
        d.update(kw)
        return _F["mh705_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        v = self._val(domanda_calore_mwh_a=0.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_domanda_negativa_non_valida(self):
        v = self._val(domanda_calore_mwh_a=-10.0)
        assert v["valido"] is False

    def test_cop_uno_non_valido(self):
        v = self._val(cop=1.0)
        assert v["valido"] is False

    def test_cop_sotto_uno_non_valido(self):
        v = self._val(cop=0.8)
        assert v["valido"] is False

    def test_cop_sopra_dieci_non_valido(self):
        v = self._val(cop=11.0)
        assert v["valido"] is False

    def test_cop_dieci_valido(self):
        assert self._val(cop=10.0)["valido"] is True

    def test_eta_zero_non_valido(self):
        v = self._val(eta_caldaia=0.0)
        assert v["valido"] is False

    def test_eta_sopra_uno_non_valido(self):
        v = self._val(eta_caldaia=1.2)
        assert v["valido"] is False

    def test_eta_uno_valido(self):
        assert self._val(eta_caldaia=1.0)["valido"] is True

    def test_potenza_zero_non_valida(self):
        v = self._val(potenza_termica_kw=0.0)
        assert v["valido"] is False

    def test_potenza_negativa_non_valida(self):
        v = self._val(potenza_termica_kw=-10.0)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=14.5)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh",
                  "prezzo_elettricita_eur_mwh",
                  "opex_annuo", "costo_specifico_eur_kw",
                  "costo_fisso_eur", "wacc_frac",
                  "fattore_co2_gas",
                  "fattore_co2_elettricita"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_tolleranza_negativa_non_valida(self):
        v = self._val(tolleranza_frac=-0.01)
        assert v["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        v = self._val(tolleranza_frac=1.5)
        assert v["valido"] is False

    def test_tolleranza_uno_valida(self):
        v = self._val(tolleranza_frac=1.0)
        assert v["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        v = self._val(cop=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(domanda_calore_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(domanda_calore_mwh_a=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(cop="3.2")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(opex_annuo=0.0)["valido"] is True
        assert self._val(costo_specifico_eur_kw=0.0)["valido"] is True
        assert self._val(costo_fisso_eur=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_energia_hp_demo(self):
        assert _F["mh705_energia_hp"](
            200.0, 3.2) == pytest.approx(EHP_DEMO, rel=REL)

    def test_energia_hp_cop_alto(self):
        assert _F["mh705_energia_hp"](
            200.0, 4.0) == pytest.approx(50.0, rel=REL)

    def test_energia_hp_rifiuta_cop_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_energia_hp"](200.0, 1.0)

    def test_energia_hp_rifiuta_cop_sopra_dieci(self):
        with pytest.raises(ValueError):
            _F["mh705_energia_hp"](200.0, 10.5)

    def test_costo_baseline_demo(self):
        assert _F["mh705_costo_baseline"](
            200.0, 0.9, 100.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_baseline_rifiuta_eta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_costo_baseline"](200.0, 1.1, 100.0)

    def test_costo_hp_demo(self):
        assert _F["mh705_costo_hp"](
            EHP_DEMO, 200.0, 800.0) == pytest.approx(
            C_HP_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh705_risparmio"](
            C_BASE_DEMO, C_HP_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh705_risparmio"](
            22222.22, 26222.22) == pytest.approx(
            -4000.0, rel=1e-6)

    def test_co2_base_demo(self):
        assert _F["mh705_co2_base"](
            200.0, 0.9, 0.20) == pytest.approx(
            CO2_BASE_DEMO, rel=REL)

    def test_co2_hp_demo(self):
        assert _F["mh705_co2_hp"](
            EHP_DEMO, 0.35) == pytest.approx(
            CO2_HP_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh705_co2_evitata"](
            CO2_BASE_DEMO, CO2_HP_DEMO) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh705_co2_evitata"](
            21.875, 44.44) == pytest.approx(-22.565, rel=1e-6)

    def test_capex_demo(self):
        assert _F["mh705_capex"](
            100.0, 900.0, 5000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh705_capex"](
            0.0, 900.0, 5000.0) == 5000.0

    def test_capex_scala_con_potenza(self):
        assert _F["mh705_capex"](
            200.0, 900.0, 5000.0) == pytest.approx(
            185000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh705_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh705_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 15 / (1.05 ** 15 - 1.0)
        assert _F["mh705_crf"](0.05, 15) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh705_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh705_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh705_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh705_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh705_van"](RISP_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh705_tir"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_bisezione_indipendente(self):
        flussi = [-CAPEX_DEMO] + [RISP_DEMO] * 15

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
        tir = _F["mh705_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh705_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh705_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh705_tir"](0.0, RISP_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh705_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh705_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh705_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 10 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 11 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh705_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh705_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh705_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh705_payback"](
            50000000.0, RISP_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh705_payback"](0.0, RISP_DEMO, 15) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh705_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_marginale_demo(self):
        assert _F["mh705_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh705_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh705_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 9500 = 10 % di CAPEX 95000
        assert _F["mh705_verdetto"](
            -9500.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh705_verdetto"](
            -9500.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh705_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh705_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh705_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh705_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh705_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh705_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh705_verdetto"](100.0, CAPEX_DEMO, 1.5, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh705_demo"]()
        d.update(kw)
        return _F["mh705_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_hp_mwh_a"] == pytest.approx(
            EHP_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_hp_eur_a"] == pytest.approx(
            C_HP_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_base_t_a"] == pytest.approx(
            CO2_BASE_DEMO, rel=REL)
        assert c["co2_hp_t_a"] == pytest.approx(
            CO2_HP_DEMO, rel=REL)
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
        d = _F["mh705_demo"]()
        b = _F["mh705_calcola"](**d)
        coppie = [("energia_hp_mwh_a", EHP_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_hp_eur_a", C_HP_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_base_t_a", CO2_BASE_DEMO),
                  ("co2_hp_t_a", CO2_HP_DEMO),
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
        d = _F["mh705_demo"]()
        assert d["domanda_calore_mwh_a"] == 200.0
        assert d["cop"] == 3.2
        assert d["eta_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 100.0
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["opex_annuo"] == 800.0
        assert d["potenza_termica_kw"] == 100.0
        assert d["costo_specifico_eur_kw"] == 900.0
        assert d["costo_fisso_eur"] == 5000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_co2_gas"] == 0.20
        assert d["fattore_co2_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_hp_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_hp_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_hp_t_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 11" in doc
        assert "verdetto = 'MARGINALE'" in doc

    def test_cop_quattro_conviente(self):
        # COP 4,0: E_hp 50,0; c_hp 10800,0;
        # risparmio 11422,2222; VAN 23558,76;
        # payback 9
        n = self._bc(cop=4.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            11422.222222222223, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 9

    def test_cop_due_non_conviente(self):
        # COP 2,0: E_hp 100,0; c_hp 20800,0;
        # risparmio 1422,2222; VAN -80237,82;
        # payback None
        n = self._bc(cop=2.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            1422.2222222222226, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_cop_uno_neutro(self):
        n = self._bc(cop=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cop_sopra_dieci_neutro(self):
        n = self._bc(cop=10.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_caldaia=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_zero_neutro(self):
        n = self._bc(eta_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_calore_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_termica_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_dieci_non_conviente(self):
        # VAN -26104,97 con tolleranza 10 % di
        # CAPEX 95000 = 9500 -> NON_CONVIENTE
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(cop=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_calore_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(domanda_calore_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_elettricita_260_non_conviente(self):
        # c_hp 17050,0; risparmio 5172,2222;
        # VAN -41314,10; payback None
        n = self._bc(prezzo_elettricita_eur_mwh=260.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            5172.222222222223, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_prezzo_gas_150_conviente(self):
        # c_base 33333,3333; risparmio
        # 20033,3333; VAN 112939,15; payback 5
        n = self._bc(prezzo_gas_eur_mwh=150.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            20033.333333333336, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 5

    def test_prezzo_elettricita_100_conviente(self):
        # c_hp 7050,0; risparmio 15172,2222;
        # VAN 62472,64; payback 7
        n = self._bc(prezzo_elettricita_eur_mwh=100.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            15172.222222222223, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 7

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -95000 + 8922,2222 x 15 =
        # 38833,33 -> CONVIENTE
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_specifico_eur_kw=0.0,
                     costo_fisso_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh705_neutro"]()
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
        n = _F["_mh705_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_calore_mwh_a",
                       "cop", "eta_caldaia",
                       "energia_hp_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_hp_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_hp_t_a",
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
        assert len(b["df_tabella"]) == 20
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Domanda calore (MWh/anno)" in voci
        assert "Energia pompa di calore (MWh/anno)" in voci
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
        return _F["mh705_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh705_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh705_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cop(self):
        s = _F["mh705_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettricita(self):
        s = _F["mh705_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh705_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh705_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # COP x0.9 (2,88) e prezzo elettricita'
        # x0.9 (180): E_hp sale di 1/0,9 mentre
        # il prezzo scende di 0,9, quindi il
        # costo elettrico resta 12500,0 e il
        # risparmio resta 8922,2222 > 0
        s = _F["mh705_sensitivita"](self._ing())
        assert s.loc["x0.9", "x0.9"] != 0.0
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) <= 1.0
        ing = self._ing()
        ing["cop"] = 3.2 * 0.9
        ing["prezzo_elettricita_eur_mwh"] = 200.0 * 0.9
        assert _F["mh705_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh705_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 27

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh705_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_hp_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_calore_mwh_a" in txt
        assert "energia_hp_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "cop" in txt
        assert "costo_fisso_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh705_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert "energia_hp_mwh_a;62.5" in txt
        assert "opex_annuo;800.0" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def705["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def705\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh705_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh705_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh705_demo():")
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
        ui_keys = set(re.findall(r'_def705\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W706 (25/10/2026) - tab705' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh705_num", "mh705_nneg", "mh705_pos",
                     "mh705_int_pos", "mh705_quota_valida",
                     "mh705_cop_valido", "mh705_eta_valido",
                     "mh705_energia_hp", "mh705_costo_baseline",
                     "mh705_costo_hp", "mh705_risparmio",
                     "mh705_co2_base", "mh705_co2_hp",
                     "mh705_co2_evitata", "mh705_capex",
                     "mh705_crf", "mh705_van", "mh705_tir",
                     "mh705_payback", "mh705_verdetto",
                     "mh705_valida", "_mh705_neutro",
                     "mh705_calcola", "mh705_sensitivita",
                     "mh705_csv", "mh705_demo",
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
        ast.parse((_new_dir() / "w706_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE705) == 1

    def test_blocco_with_tab705(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab705:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE705

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st705_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st705_") for k in keys)

    def test_chiavi_st_input_sono_15(self):
        """Le 15 chiavi di input/bottone del brief
        (14 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st705_[a-z0-9_]+)"', _ui_src())
        attese = ["st705_domanda", "st705_cop",
                  "st705_eta", "st705_prezzo_gas",
                  "st705_prezzo_elettricita",
                  "st705_opex", "st705_potenza",
                  "st705_costo_specifico",
                  "st705_costo_fisso", "st705_fattore_gas",
                  "st705_fattore_elettricita",
                  "st705_vita", "st705_wacc",
                  "st705_tolleranza", "st705_calcola"]
        assert len(attese) == 15
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg705" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg705") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg705")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert '"COP"' in src or "COP" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd705" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_co2_presente(self):
        src = _ui_src().lower()
        assert "gas-cooler" in src
        assert "transcritic" in src
        assert "compressore" in src
        assert "assorbimento" in src
        assert "ibrid" in src
        assert "70-90" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline caldaia a gas" in src
        assert "Pompa di calore CO2" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh705_csv" in src
        assert "pompa_calore_co2_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh705_sensitivita" in src
        assert "Heatmap" in src
        assert "COP" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st705_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W706 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab705:")
        assert "mh705_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab705" in (_new_dir() / "w706_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w706_helpers.py", "w706_ui.py",
                   "w706_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab705"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "4"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w706_helpers.py", "w706_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_co2_non_assorbimento(self):
        assert "CO2" in TITLE705
        assert "transcritica" in TITLE705.lower()
