"""Test tab703 "🔥 Pompa di calore ad assorbimento: il calore dal gas senza compressore paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
fabbisogno termico 200 MWh/anno; COP termico
1,5; rendimento caldaia 0,9; prezzo gas 100
EUR/MWh; prezzo elettricita' 200 EUR/MWh;
coefficiente ausiliari 0,01 MWh_e/MWh_th;
OPEX annuo 500 EUR/anno; potenza termica
100 kW; costo specifico 800 EUR/kW; costo
fisso 5000 EUR; vita 15 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del CAPEX);
fattore gas 0,20 tCO2/MWh; fattore
elettricita' 0,35 tCO2/MWh.

- gas_ass_mwh_a = 133.33333333333334
- energia_aux_mwh_a = 2.0
- costo_baseline_eur_a = 22222.222222222223
- costo_assorbimento_eur_a = 14233.333333333334
- risparmio_eur_a = 7988.888888888889
- co2_base_t_a = 44.44444444444445
- co2_assorbimento_t_a = 27.36666666666667
- co2_evitata_t_a = 17.07777777777778
- capex_eur = 85000.0
- van = -2078.065228312771
- tir = 4.636070980936037
- payback = 11
- verdetto = 'MARGINALE'

Scomposizione: gas_ass 200 / 1,5 =
133.33333333333334; E_aux 200 x 0,01 = 2.0;
c_base 200 / 0,9 x 100 =
22222.222222222223; c_ass
133.33333333333334 x 100 + 2.0 x 200 + 500 =
14233.333333333334; risparmio
22222.222222222223 - 14233.333333333334 =
7988.888888888889; co2_base 200 / 0,9 x
0,20 = 44.44444444444445; co2_ass
133.33333333333334 x 0,20 + 2.0 x 0,35 =
27.36666666666667; co2_evitata
44.44444444444445 - 27.36666666666667 =
17.07777777777778; capex 100 x 800 + 5000 =
85000.0; VAN -85000,0 +
7988.888888888889 x (1 - 1,05^-15) / 0,05 =
-2078.065228312771; TIR per bisezione su
[-0,99, 5,0] dei flussi [-85000,
7988.888888888889 x 15]: 4.636070980936037 %
(VAN a quella TIR ~0); payback: cumulato
anno 10 -5111,111111111109, anno 11
+2877,77777777778 -> 11; VAN negativo ma
|VAN| 2078,07 <= 10 % di CAPEX (8500) ->
MARGINALE.
NOTA: i valori esatti ricalcolati sono
quelli sopra (VAN -2078,07, TIR 4,6361 %) —
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
    if (p / "w704_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w704_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w704_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w704_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w704_helpers.py: {missing}")
    return out


_F = _load("mh703_num", "mh703_nneg", "mh703_pos",
           "mh703_int_pos", "mh703_rendimento_valido",
           "mh703_quota_valida", "mh703_cop_valido",
           "mh703_gas_assorbimento", "mh703_energia_aux",
           "mh703_costo_baseline", "mh703_costo_assorbimento",
           "mh703_risparmio", "mh703_co2_base",
           "mh703_co2_assorbimento", "mh703_co2_evitata",
           "mh703_capex", "mh703_crf", "mh703_van",
           "mh703_tir", "mh703_payback",
           "mh703_verdetto", "mh703_valida",
           "_mh703_neutro", "mh703_calcola",
           "mh703_sensitivita", "mh703_csv",
           "mh703_demo", "demo_calcoli")

TITLE703 = ("🔥 Pompa di calore ad assorbimento: il calore "
            "dal gas senza compressore paga?")

GAS_ASS_DEMO = 133.33333333333334
EAUX_DEMO = 2.0
C_BASE_DEMO = 22222.222222222223
C_ASS_DEMO = 14233.333333333334
RISP_DEMO = 7988.888888888889
CO2_BASE_DEMO = 44.44444444444445
CO2_ASS_DEMO = 27.36666666666667
CO2_EV_DEMO = 17.07777777777778
CAPEX_DEMO = 85000.0
VAN_DEMO = -2078.065228312771
TIR_DEMO = 4.636070980936037
PAYBACK_DEMO = 11
VITA_DEMO = 15
VERDETTO_DEMO = "MARGINALE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w704_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w704_ui.py").read_text(encoding="utf-8")


def _app_path():
    return Path.home() / "workspace/repo-dashboard/Dashboard-data-analist/app.py"


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh703_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh703_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh703_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh703_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh703_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh703_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh703_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh703_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh703_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh703_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh703_int_pos"](15.0, "x") == 15

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh703_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh703_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh703_rendimento_valido"](1.0, "x") == 1.0

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh703_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh703_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh703_quota_valida"](0.0, "x") == 0.0
        assert _F["mh703_quota_valida"](1.0, "x") == 1.0

    def test_cop_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh703_cop_valido"](0.0, "x")

    def test_cop_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh703_cop_valido"](-1.5, "x")

    def test_cop_rifiuta_sopra_due(self):
        with pytest.raises(ValueError):
            _F["mh703_cop_valido"](2.1, "x")

    def test_cop_accetta_due(self):
        assert _F["mh703_cop_valido"](2.0, "x") == 2.0

    def test_cop_accetta_valori_intermedi(self):
        assert _F["mh703_cop_valido"](1.5, "x") == 1.5


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh703_demo"]()
        d.update(kw)
        return _F["mh703_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_fabbisogno_zero_non_valido(self):
        v = self._val(fabbisogno_mwh_a=0.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_fabbisogno_negativo_non_valido(self):
        v = self._val(fabbisogno_mwh_a=-10.0)
        assert v["valido"] is False

    def test_cop_zero_non_valido(self):
        v = self._val(cop_th=0.0)
        assert v["valido"] is False

    def test_cop_negativo_non_valido(self):
        v = self._val(cop_th=-1.5)
        assert v["valido"] is False

    def test_cop_sopra_due_non_valido(self):
        v = self._val(cop_th=2.1)
        assert v["valido"] is False

    def test_cop_due_valido(self):
        assert self._val(cop_th=2.0)["valido"] is True

    def test_rendimento_caldaia_zero_non_valido(self):
        v = self._val(rendimento_caldaia=0.0)
        assert v["valido"] is False

    def test_rendimento_caldaia_sopra_uno_non_valido(self):
        v = self._val(rendimento_caldaia=1.2)
        assert v["valido"] is False

    def test_rendimento_caldaia_uno_valido(self):
        v = self._val(rendimento_caldaia=1.0)
        assert v["valido"] is True

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=14.5)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh",
                  "prezzo_elettricita_eur_mwh", "k_aux",
                  "opex_annuo", "potenza_th_kw",
                  "costo_specifico_eur_kw", "costo_fisso_eur",
                  "wacc_frac", "fattore_gas",
                  "fattore_elettricita"):
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
        v = self._val(cop_th=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(fabbisogno_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(fabbisogno_mwh_a=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(cop_th="1.5")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(potenza_th_kw=0.0)["valido"] is True
        assert self._val(opex_annuo=0.0)["valido"] is True
        assert self._val(k_aux=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_gas_assorbimento_demo(self):
        assert _F["mh703_gas_assorbimento"](
            200.0, 1.5) == pytest.approx(GAS_ASS_DEMO, rel=REL)

    def test_gas_assorbimento_cop_due(self):
        assert _F["mh703_gas_assorbimento"](
            200.0, 2.0) == pytest.approx(100.0, rel=REL)

    def test_gas_assorbimento_rifiuta_cop_sopra_due(self):
        with pytest.raises(ValueError):
            _F["mh703_gas_assorbimento"](200.0, 2.1)

    def test_gas_assorbimento_rifiuta_cop_zero(self):
        with pytest.raises(ValueError):
            _F["mh703_gas_assorbimento"](200.0, 0.0)

    def test_energia_aux_demo(self):
        assert _F["mh703_energia_aux"](
            200.0, 0.01) == pytest.approx(EAUX_DEMO, rel=REL)

    def test_energia_aux_zero(self):
        assert _F["mh703_energia_aux"](200.0, 0.0) == 0.0

    def test_energia_aux_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh703_energia_aux"](200.0, -0.01)

    def test_costo_baseline_demo(self):
        assert _F["mh703_costo_baseline"](
            200.0, 0.9, 100.0) == pytest.approx(C_BASE_DEMO, rel=REL)

    def test_costo_assorbimento_demo(self):
        assert _F["mh703_costo_assorbimento"](
            GAS_ASS_DEMO, 100.0, EAUX_DEMO, 200.0,
            500.0) == pytest.approx(C_ASS_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh703_risparmio"](
            C_BASE_DEMO, C_ASS_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh703_risparmio"](
            22222.22, 23122.22) == pytest.approx(
            -900.0, rel=1e-6)

    def test_co2_base_demo(self):
        assert _F["mh703_co2_base"](
            200.0, 0.9, 0.20) == pytest.approx(
            CO2_BASE_DEMO, rel=REL)

    def test_co2_assorbimento_demo(self):
        assert _F["mh703_co2_assorbimento"](
            GAS_ASS_DEMO, 0.20, EAUX_DEMO,
            0.35) == pytest.approx(CO2_ASS_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh703_co2_evitata"](
            CO2_BASE_DEMO, CO2_ASS_DEMO) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh703_co2_evitata"](
            44.44, 60.0) == pytest.approx(-15.56, rel=1e-6)

    def test_capex_demo(self):
        assert _F["mh703_capex"](
            100.0, 800.0, 5000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh703_capex"](
            0.0, 800.0, 5000.0) == 5000.0

    def test_capex_scala_con_potenza(self):
        assert _F["mh703_capex"](
            200.0, 800.0, 5000.0) == pytest.approx(
            165000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh703_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh703_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 15 / (1.05 ** 15 - 1.0)
        assert _F["mh703_crf"](0.05, 15) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh703_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh703_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh703_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh703_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh703_van"](RISP_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh703_tir"](
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
        tir = _F["mh703_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh703_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh703_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh703_tir"](0.0, RISP_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh703_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh703_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh703_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 10 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 11 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh703_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh703_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh703_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh703_payback"](
            50000000.0, RISP_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh703_payback"](0.0, RISP_DEMO, 15) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh703_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_marginale_demo(self):
        assert _F["mh703_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh703_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh703_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 8500 = 10 % di CAPEX 85000
        assert _F["mh703_verdetto"](
            -8500.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh703_verdetto"](
            -8500.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh703_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh703_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh703_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh703_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh703_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh703_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh703_verdetto"](100.0, CAPEX_DEMO, 1.5, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh703_demo"]()
        d.update(kw)
        return _F["mh703_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["gas_ass_mwh_a"] == pytest.approx(
            GAS_ASS_DEMO, rel=REL)
        assert c["energia_aux_mwh_a"] == pytest.approx(
            EAUX_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_assorbimento_eur_a"] == pytest.approx(
            C_ASS_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_base_t_a"] == pytest.approx(
            CO2_BASE_DEMO, rel=REL)
        assert c["co2_assorbimento_t_a"] == pytest.approx(
            CO2_ASS_DEMO, rel=REL)
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
        d = _F["mh703_demo"]()
        b = _F["mh703_calcola"](**d)
        coppie = [("gas_ass_mwh_a", GAS_ASS_DEMO),
                  ("energia_aux_mwh_a", EAUX_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_assorbimento_eur_a", C_ASS_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_base_t_a", CO2_BASE_DEMO),
                  ("co2_assorbimento_t_a", CO2_ASS_DEMO),
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
        d = _F["mh703_demo"]()
        assert d["fabbisogno_mwh_a"] == 200.0
        assert d["cop_th"] == 1.5
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 100.0
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["k_aux"] == 0.01
        assert d["opex_annuo"] == 500.0
        assert d["potenza_th_kw"] == 100.0
        assert d["costo_specifico_eur_kw"] == 800.0
        assert d["costo_fisso_eur"] == 5000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_gas"] == 0.20
        assert d["fattore_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("gas_ass_mwh_a",
                       "energia_aux_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_assorbimento_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_assorbimento_t_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 11" in doc
        assert "verdetto = 'MARGINALE'" in doc

    def test_cop_uno_non_conviente(self):
        # COP 1,0: gas 200,0; c_ass 20900,0;
        # risparmio 1322,2222; VAN -71275,79
        n = self._bc(cop_th=1.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            1322.2222222222226, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_cop_due_conviente(self):
        # COP 2,0: gas 100,0; c_ass 10900,0;
        # risparmio 11322,2222; VAN 32520,79
        n = self._bc(cop_th=2.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            11322.222222222223, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 8

    def test_cop_zero_nove_neutro_via_risparmio(self):
        # COP 0,9: gas 222,2222; c_ass 23122,2222
        # contro c_base 22222,2222 -> risparmio
        # negativo -> dict neutro
        n = self._bc(cop_th=0.9)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["tir"] is None
        assert n["payback"] is None

    def test_cop_sopra_due_neutro(self):
        n = self._bc(cop_th=2.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cop_zero_neutro(self):
        n = self._bc(cop_th=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fabbisogno_zero_neutro(self):
        n = self._bc(fabbisogno_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_caldaia_sopra_uno_neutro(self):
        n = self._bc(rendimento_caldaia=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_caldaia_zero_neutro(self):
        n = self._bc(rendimento_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_dieci_non_conviente(self):
        # VAN circa -23311,92; payback None
        # (10 x 7988,89 < CAPEX 85000)
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_vita_dieci_tolleranza_uno_marginale(self):
        # Stesso VAN -23311,92 ma tolleranza 1,0:
        # entro il 100 % del CAPEX -> MARGINALE
        n = self._bc(vita_anni=10, tolleranza_frac=1.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"

    def test_vita_venti_conviente(self):
        # VAN circa 14559,21
        n = self._bc(vita_anni=20)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(cop_th=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(fabbisogno_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(fabbisogno_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_gas_200_conviente(self):
        # c_base 44444,4444; c_ass 27566,6667;
        # risparmio 16877,7778; VAN 90185,56
        n = self._bc(prezzo_gas_eur_mwh=200.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            16877.777777777777, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_prezzo_gas_50_non_conviente(self):
        # Risparmio 3544,4444 ma VAN -48209,88:
        # NON_CONVIENTE, non neutro; payback
        # None (15 x 3544,44 < CAPEX)
        n = self._bc(prezzo_gas_eur_mwh=50.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_k_aux_alto_non_conviente(self):
        # k_aux 0,05: E_aux 10,0; c_ass
        # 15833,3333; risparmio 6388,8889;
        # VAN -18685,52
        n = self._bc(k_aux=0.05)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            6388.888888888889, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -85000 + 7988,8889 x 15 =
        # 34833,3333 -> CONVIENTE (non MARGINALE)
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
        n = _F["_mh703_neutro"]()
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
        n = _F["_mh703_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "fabbisogno_mwh_a",
                       "cop_th",
                       "gas_ass_mwh_a",
                       "energia_aux_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_assorbimento_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_assorbimento_t_a",
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
        assert len(b["df_tabella"]) == 22
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Fabbisogno termico (MWh/anno)" in voci
        assert "Gas assorbimento (MWh/anno)" in voci
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
        return _F["mh703_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh703_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh703_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cop(self):
        s = _F["mh703_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_prezzo_gas(self):
        s = _F["mh703_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh703_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh703_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # COP x0.9 (1,35) e prezzo gas x0.9 (90):
        # risparmio 5766,6667 > 0, quindi VAN
        # non degenere
        s = _F["mh703_sensitivita"](self._ing())
        assert s.loc["x0.9", "x0.9"] != 0.0
        ing = self._ing()
        ing["cop_th"] = 1.5 * 0.9
        ing["prezzo_gas_eur_mwh"] = 100.0 * 0.9
        assert _F["mh703_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            5766.666666666666, rel=REL)

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh703_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh703_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_assorbimento_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "fabbisogno_mwh_a" in txt
        assert "gas_ass_mwh_a" in txt
        assert "energia_aux_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "cop_th" in txt
        assert "costo_fisso_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh703_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert "gas_ass_mwh_a;133.33333333333334" in txt
        assert "opex_annuo;500.0" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def703["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def703\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh703_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh703_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh703_demo():")
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
        ui_keys = set(re.findall(r'_def703\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W704 (25/10/2026) - tab703' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh703_num", "mh703_nneg", "mh703_pos",
                     "mh703_int_pos", "mh703_rendimento_valido",
                     "mh703_quota_valida", "mh703_cop_valido",
                     "mh703_gas_assorbimento", "mh703_energia_aux",
                     "mh703_costo_baseline",
                     "mh703_costo_assorbimento",
                     "mh703_risparmio", "mh703_co2_base",
                     "mh703_co2_assorbimento", "mh703_co2_evitata",
                     "mh703_capex", "mh703_crf",
                     "mh703_van", "mh703_tir",
                     "mh703_payback", "mh703_verdetto",
                     "mh703_valida", "_mh703_neutro",
                     "mh703_calcola", "mh703_sensitivita",
                     "mh703_csv", "mh703_demo",
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
        ast.parse((_new_dir() / "w704_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE703) == 1

    def test_blocco_with_tab703(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab703:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE703

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st703_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st703_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone del brief
        (15 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st703_[a-z0-9_]+)"', _ui_src())
        attese = ["st703_fabbisogno", "st703_cop_th",
                  "st703_rendimento_caldaia",
                  "st703_prezzo_gas",
                  "st703_prezzo_elettricita", "st703_k_aux",
                  "st703_opex", "st703_potenza_th",
                  "st703_costo_specifico",
                  "st703_costo_fisso", "st703_fattore_gas",
                  "st703_fattore_elettricita",
                  "st703_vita", "st703_wacc",
                  "st703_tolleranza", "st703_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg703" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg703") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg703")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "COP termico" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd703" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_assorbimento_presente(self):
        src = _ui_src().lower()
        assert "senza compressore" in src
        assert "calore ambientale" in src
        assert "di scarto" in src
        assert "mandata" in src
        assert "gas" in src
        assert "cop" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline caldaia" in src
        assert "Assorbimento" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh703_csv" in src
        assert "pompa_calore_assorbimento_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh703_sensitivita" in src
        assert "Heatmap" in src
        assert "COP termico" in src
        assert "Prezzo gas" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st703_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W704 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab703:")
        assert "mh703_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab703" in (_new_dir() / "w704_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w704_helpers.py", "w704_ui.py",
                   "w704_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab703"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "2"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w704_helpers.py", "w704_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_assorbimento_non_ibrido(self):
        assert "assorbimento" in TITLE703.lower()
        assert "compressore" in TITLE703.lower()


class TestRegistryPostApply:
    """Check registry/count post-apply (pattern dei test
    per-tab precedenti): fallisce finche' l'apply
    di tab703 non e' fatto, perche' il titolo non
    e' ancora nella lista st.tabs di app.py e il
    conteggio delle tab e' ancora 702. NON e' un
    fallimento del codice di tab703: dopo
    l'apply questo test deve diventare verde."""

    def test_registry_count_703_e_titolo_in_st_tabs(self):
        app = _app_path()
        assert app.exists(), f"app.py non trovato: {app}"
        src = app.read_text(encoding="utf-8")
        assert "st.tabs(" in src
        m = re.search(
            r"((?:tab\d+\s*,\s*)*tab\d+)\s*=\s*st\.tabs\(",
            src)
        assert m is not None, "riga unpack st.tabs non trovata"
        n_tab = len(re.findall(r"tab\d+", m.group(1)))
        assert n_tab == 706, \
            f"conteggio tab {n_tab} != 703 (atteso post-apply)"
        idx = src.index("st.tabs(")
        assert TITLE703 in src[idx:], \
            "titolo tab703 non ancora nella lista st.tabs " \
            "(atteso prima dell'apply)"
