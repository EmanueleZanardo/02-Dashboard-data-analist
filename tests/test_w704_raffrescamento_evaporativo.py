"""Test tab704 "💧 Raffrescamento evaporativo (adiabatico): il freddo dall'acqua senza compressore paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda freddo 500 MWh/anno; EER baseline
3,0; EER evaporativo 12,0; prezzo
elettricita' 200 EUR/MWh; consumo specifico
acqua 1,8 m3/MWh_f; prezzo acqua 2,0 EUR/m3;
OPEX annuo 3000 EUR/anno; potenza freddo
200 kW; costo specifico 250 EUR/kW; costo
fisso 5000 EUR; vita 15 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del CAPEX);
fattore CO2 rete 0,35 tCO2/MWh.

- energia_base_mwh_a = 166.66666666666666
- energia_evap_mwh_a = 41.666666666666664
- volume_acqua_m3_a = 900.0
- costo_baseline_eur_a = 33333.33333333333
- costo_evap_eur_a = 13133.333333333332
- risparmio_eur_a = 20199.999999999996
- co2_base_t_a = 58.33333333333333
- co2_evap_t_a = 14.583333333333332
- co2_evitata_t_a = 43.75
- capex_eur = 55000.0
- van = 154669.09237124806
- tir = 36.377448179456614
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: E_base 500 / 3,0 =
166.66666666666666; E_evap 500 / 12,0 =
41.666666666666664; V_acqua 500 x 1,8 =
900.0; c_base 166.66666666666666 x 200 =
33333.33333333333; c_evap
41.666666666666664 x 200 + 900.0 x 2,0 +
3000 = 13133.333333333332; risparmio
33333.33333333333 - 13133.333333333332 =
20199.999999999996; co2_base
166.66666666666666 x 0,35 =
58.33333333333333; co2_evap
41.666666666666664 x 0,35 =
14.583333333333332; co2_evitata
58.33333333333333 - 14.583333333333332 =
43.75; capex 200 x 250 + 5000 = 55000.0; VAN
-55000,0 + 20199.999999999996 x
(1 - 1,05^-15) / 0,05 = 154669.09237124806;
TIR per bisezione su [-0,99, 5,0] dei flussi
[-55000, 20199.999999999996 x 15]:
36.377448179456614 % (VAN a quella TIR ~0);
payback: cumulato anno 2 -14600,0, anno 3
+5600,0 -> 3; VAN >= 0 -> CONVIENTE.
NOTA: i valori esatti ricalcolati sono
quelli sopra (VAN 154669,09, TIR 36,3774 %) —
il test fissa i valori esatti, non le
approssimazioni (il risparmio demo e'
20199,999999999996 in virgola mobile, cioe'
20200,00 EUR/anno arrotondato).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w705_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w705_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w705_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w705_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w705_helpers.py: {missing}")
    return out


_F = _load("mh704_num", "mh704_nneg", "mh704_pos",
           "mh704_int_pos", "mh704_quota_valida",
           "mh704_eer_valido", "mh704_energia_base",
           "mh704_energia_evap", "mh704_volume_acqua",
           "mh704_costo_baseline", "mh704_costo_evap",
           "mh704_risparmio", "mh704_co2_base",
           "mh704_co2_evap", "mh704_co2_evitata",
           "mh704_capex", "mh704_crf", "mh704_van",
           "mh704_tir", "mh704_payback",
           "mh704_verdetto", "mh704_valida",
           "_mh704_neutro", "mh704_calcola",
           "mh704_sensitivita", "mh704_csv",
           "mh704_demo", "demo_calcoli")

TITLE704 = ("💧 Raffrescamento evaporativo (adiabatico): il freddo "
            "dall'acqua senza compressore paga?")

EBASE_DEMO = 166.66666666666666
EEVAP_DEMO = 41.666666666666664
VACQUA_DEMO = 900.0
C_BASE_DEMO = 33333.33333333333
C_EVAP_DEMO = 13133.333333333332
RISP_DEMO = 20199.999999999996
CO2_BASE_DEMO = 58.33333333333333
CO2_EVAP_DEMO = 14.583333333333332
CO2_EV_DEMO = 43.75
CAPEX_DEMO = 55000.0
VAN_DEMO = 154669.09237124806
TIR_DEMO = 36.377448179456614
PAYBACK_DEMO = 3
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w705_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w705_ui.py").read_text(encoding="utf-8")


def _app_path():
    return Path.home() / "workspace/repo-dashboard/Dashboard-data-analist/app.py"


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh704_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh704_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh704_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh704_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh704_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh704_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh704_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh704_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh704_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh704_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh704_int_pos"](15.0, "x") == 15

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh704_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh704_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh704_quota_valida"](0.0, "x") == 0.0
        assert _F["mh704_quota_valida"](1.0, "x") == 1.0

    def test_eer_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh704_eer_valido"](0.0, "x")

    def test_eer_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh704_eer_valido"](-1.5, "x")

    def test_eer_accetta_valori_alti(self):
        # L'evaporativo non ha tetto superiore:
        # 12,0 demo, 30,0 e oltre sono validi.
        assert _F["mh704_eer_valido"](12.0, "x") == 12.0
        assert _F["mh704_eer_valido"](30.0, "x") == 30.0
        assert _F["mh704_eer_valido"](100.0, "x") == 100.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh704_demo"]()
        d.update(kw)
        return _F["mh704_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        v = self._val(domanda_freddo_mwh_a=0.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_domanda_negativa_non_valida(self):
        v = self._val(domanda_freddo_mwh_a=-10.0)
        assert v["valido"] is False

    def test_eer_base_zero_non_valido(self):
        v = self._val(eer_base=0.0)
        assert v["valido"] is False

    def test_eer_evap_zero_non_valido(self):
        v = self._val(eer_evap=0.0)
        assert v["valido"] is False

    def test_eer_evap_negativo_non_valido(self):
        v = self._val(eer_evap=-12.0)
        assert v["valido"] is False

    def test_eer_evap_alto_valido(self):
        assert self._val(eer_evap=30.0)["valido"] is True

    def test_potenza_zero_non_valida(self):
        # Differenza dal brief tab703: qui la
        # potenza freddo deve essere > 0.
        v = self._val(potenza_freddo_kw=0.0)
        assert v["valido"] is False

    def test_potenza_negativa_non_valida(self):
        v = self._val(potenza_freddo_kw=-10.0)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=14.5)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_elettricita_eur_mwh",
                  "consumo_acqua_specifico_m3_mwh",
                  "prezzo_acqua_eur_m3", "opex_annuo",
                  "costo_specifico_eur_kw", "costo_fisso_eur",
                  "wacc_frac", "fattore_co2_elettricita"):
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
        v = self._val(eer_evap=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(domanda_freddo_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(domanda_freddo_mwh_a=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eer_evap="12.0")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_acqua_eur_m3=0.0)["valido"] is True
        assert self._val(consumo_acqua_specifico_m3_mwh=0.0)["valido"] is True
        assert self._val(opex_annuo=0.0)["valido"] is True
        assert self._val(costo_specifico_eur_kw=0.0)["valido"] is True
        assert self._val(costo_fisso_eur=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_energia_base_demo(self):
        assert _F["mh704_energia_base"](
            500.0, 3.0) == pytest.approx(EBASE_DEMO, rel=REL)

    def test_energia_evap_demo(self):
        assert _F["mh704_energia_evap"](
            500.0, 12.0) == pytest.approx(EEVAP_DEMO, rel=REL)

    def test_energia_evap_eer_alto(self):
        assert _F["mh704_energia_evap"](
            500.0, 25.0) == pytest.approx(20.0, rel=REL)

    def test_energia_rifiuta_eer_zero(self):
        with pytest.raises(ValueError):
            _F["mh704_energia_evap"](500.0, 0.0)

    def test_volume_acqua_demo(self):
        assert _F["mh704_volume_acqua"](
            500.0, 1.8) == pytest.approx(VACQUA_DEMO, rel=REL)

    def test_volume_acqua_zero(self):
        assert _F["mh704_volume_acqua"](500.0, 0.0) == 0.0

    def test_volume_acqua_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh704_volume_acqua"](500.0, -0.1)

    def test_costo_baseline_demo(self):
        assert _F["mh704_costo_baseline"](
            EBASE_DEMO, 200.0) == pytest.approx(C_BASE_DEMO, rel=REL)

    def test_costo_evap_demo(self):
        assert _F["mh704_costo_evap"](
            EEVAP_DEMO, 200.0, VACQUA_DEMO, 2.0,
            3000.0) == pytest.approx(C_EVAP_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh704_risparmio"](
            C_BASE_DEMO, C_EVAP_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh704_risparmio"](
            33333.33, 38133.33) == pytest.approx(
            -4800.0, rel=1e-6)

    def test_co2_base_demo(self):
        assert _F["mh704_co2_base"](
            EBASE_DEMO, 0.35) == pytest.approx(
            CO2_BASE_DEMO, rel=REL)

    def test_co2_evap_demo(self):
        assert _F["mh704_co2_evap"](
            EEVAP_DEMO, 0.35) == pytest.approx(
            CO2_EVAP_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh704_co2_evitata"](
            CO2_BASE_DEMO, CO2_EVAP_DEMO) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh704_co2_evitata"](
            14.58, 58.33) == pytest.approx(-43.75, rel=1e-6)

    def test_capex_demo(self):
        assert _F["mh704_capex"](
            200.0, 250.0, 5000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh704_capex"](
            0.0, 250.0, 5000.0) == 5000.0

    def test_capex_scala_con_potenza(self):
        assert _F["mh704_capex"](
            400.0, 250.0, 5000.0) == pytest.approx(
            105000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh704_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh704_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 15 / (1.05 ** 15 - 1.0)
        assert _F["mh704_crf"](0.05, 15) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh704_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh704_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh704_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh704_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh704_van"](RISP_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh704_tir"](
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
        tir = _F["mh704_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh704_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh704_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh704_tir"](0.0, RISP_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh704_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh704_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh704_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 2 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 3 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh704_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh704_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh704_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh704_payback"](
            50000000.0, RISP_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh704_payback"](0.0, RISP_DEMO, 15) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh704_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh704_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh704_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh704_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 5500 = 10 % di CAPEX 55000
        assert _F["mh704_verdetto"](
            -5500.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh704_verdetto"](
            -5500.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh704_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh704_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh704_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh704_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh704_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh704_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh704_verdetto"](100.0, CAPEX_DEMO, 1.5, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh704_demo"]()
        d.update(kw)
        return _F["mh704_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_base_mwh_a"] == pytest.approx(
            EBASE_DEMO, rel=REL)
        assert c["energia_evap_mwh_a"] == pytest.approx(
            EEVAP_DEMO, rel=REL)
        assert c["volume_acqua_m3_a"] == pytest.approx(
            VACQUA_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_evap_eur_a"] == pytest.approx(
            C_EVAP_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_base_t_a"] == pytest.approx(
            CO2_BASE_DEMO, rel=REL)
        assert c["co2_evap_t_a"] == pytest.approx(
            CO2_EVAP_DEMO, rel=REL)
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
        d = _F["mh704_demo"]()
        b = _F["mh704_calcola"](**d)
        coppie = [("energia_base_mwh_a", EBASE_DEMO),
                  ("energia_evap_mwh_a", EEVAP_DEMO),
                  ("volume_acqua_m3_a", VACQUA_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_evap_eur_a", C_EVAP_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_base_t_a", CO2_BASE_DEMO),
                  ("co2_evap_t_a", CO2_EVAP_DEMO),
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
        d = _F["mh704_demo"]()
        assert d["domanda_freddo_mwh_a"] == 500.0
        assert d["eer_base"] == 3.0
        assert d["eer_evap"] == 12.0
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["consumo_acqua_specifico_m3_mwh"] == 1.8
        assert d["prezzo_acqua_eur_m3"] == 2.0
        assert d["opex_annuo"] == 3000.0
        assert d["potenza_freddo_kw"] == 200.0
        assert d["costo_specifico_eur_kw"] == 250.0
        assert d["costo_fisso_eur"] == 5000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_co2_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_base_mwh_a",
                       "energia_evap_mwh_a",
                       "volume_acqua_m3_a",
                       "costo_baseline_eur_a",
                       "costo_evap_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_evap_t_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_eer_evap_sei_conviente(self):
        # EER 6,0: E_evap 83,3333; c_evap
        # 21466,6667; risparmio 11866,6667;
        # VAN 68171,94; payback 5
        n = self._bc(eer_evap=6.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            11866.666666666664, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 5

    def test_eer_evap_ventiquattro_conviente(self):
        # EER 24,0: E_evap 20,8333; c_evap
        # 8966,6667; risparmio 24366,6667;
        # VAN 197917,67; payback 3
        n = self._bc(eer_evap=24.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            24366.666666666664, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 3

    def test_eer_evap_tre_neutro_via_risparmio(self):
        # EER 3,0 = EER baseline: E_evap
        # 166,6667; c_evap 38133,3333 contro
        # c_base 33333,3333 -> risparmio
        # negativo -> dict neutro
        n = self._bc(eer_evap=3.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["tir"] is None
        assert n["payback"] is None

    def test_eer_evap_zero_neutro(self):
        n = self._bc(eer_evap=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eer_base_zero_neutro(self):
        n = self._bc(eer_base=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_freddo_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=14.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_dieci_conviente(self):
        # VAN circa 100979,05; payback 3
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 3

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eer_evap=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_elettricita_100_conviente(self):
        # c_base 16666,6667; c_evap 8966,6667;
        # risparmio 7700,0; VAN 24923,37;
        # payback 8
        n = self._bc(prezzo_elettricita_eur_mwh=100.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            7699.999999999998, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 8

    def test_prezzo_elettricita_300_conviente(self):
        # c_base 50000,0; c_evap 17300,0;
        # risparmio 32700,0; VAN 284414,82
        n = self._bc(prezzo_elettricita_eur_mwh=300.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            32700.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_prezzo_acqua_20_non_conviente(self):
        # c_evap 29333,3333; risparmio 4000,0;
        # VAN -13481,37: NON_CONVIENTE, non
        # neutro; payback 14 (13 x 4000 = 52000
        # < CAPEX, 14 x 4000 = 56000 >= CAPEX)
        n = self._bc(prezzo_acqua_eur_m3=20.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            3999.9999999999964, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 14

    def test_prezzo_acqua_20_tolleranza_uno_marginale(self):
        # Stesso VAN -13481,37 ma tolleranza 1,0:
        # entro il 100 % del CAPEX -> MARGINALE
        n = self._bc(prezzo_acqua_eur_m3=20.0,
                     tolleranza_frac=1.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"

    def test_consumo_acqua_zero_conviente(self):
        # V 0; c_evap 11333,3333; risparmio
        # 22000,0 -> CONVIENTE
        n = self._bc(consumo_acqua_specifico_m3_mwh=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            22000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -55000 + 20200 x 15 =
        # 248000,0 -> CONVIENTE (non MARGINALE)
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
        n = _F["_mh704_neutro"]()
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
        n = _F["_mh704_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_freddo_mwh_a",
                       "eer_base", "eer_evap",
                       "energia_base_mwh_a",
                       "energia_evap_mwh_a",
                       "volume_acqua_m3_a",
                       "costo_baseline_eur_a",
                       "costo_evap_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_evap_t_a",
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
        assert "Domanda freddo (MWh/anno)" in voci
        assert "Energia evaporativo (MWh/anno)" in voci
        assert "Volume acqua (m3/anno)" in voci
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
        return _F["mh704_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh704_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh704_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_eer(self):
        s = _F["mh704_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_prezzo_elettricita(self):
        s = _F["mh704_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh704_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh704_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # EER x0.9 (10,8) e prezzo elettricita'
        # x0.9 (180): risparmio 16866,6667 > 0,
        # quindi VAN non degenere
        s = _F["mh704_sensitivita"](self._ing())
        assert s.loc["x0.9", "x0.9"] != 0.0
        ing = self._ing()
        ing["eer_evap"] = 12.0 * 0.9
        ing["prezzo_elettricita_eur_mwh"] = 200.0 * 0.9
        assert _F["mh704_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            16866.666666666668, rel=REL)

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh704_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh704_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_evap_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_freddo_mwh_a" in txt
        assert "energia_evap_mwh_a" in txt
        assert "volume_acqua_m3_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "eer_evap" in txt
        assert "costo_fisso_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh704_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert "energia_evap_mwh_a;41.666666666666664" in txt
        assert "opex_annuo;3000.0" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def704["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def704\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh704_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh704_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh704_demo():")
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
        ui_keys = set(re.findall(r'_def704\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W705 (25/10/2026) - tab704' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh704_num", "mh704_nneg", "mh704_pos",
                     "mh704_int_pos", "mh704_quota_valida",
                     "mh704_eer_valido", "mh704_energia_base",
                     "mh704_energia_evap", "mh704_volume_acqua",
                     "mh704_costo_baseline", "mh704_costo_evap",
                     "mh704_risparmio", "mh704_co2_base",
                     "mh704_co2_evap", "mh704_co2_evitata",
                     "mh704_capex", "mh704_crf",
                     "mh704_van", "mh704_tir",
                     "mh704_payback", "mh704_verdetto",
                     "mh704_valida", "_mh704_neutro",
                     "mh704_calcola", "mh704_sensitivita",
                     "mh704_csv", "mh704_demo",
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
        ast.parse((_new_dir() / "w705_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE704) == 1

    def test_blocco_with_tab704(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab704:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE704

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st704_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st704_") for k in keys)

    def test_chiavi_st_input_sono_15(self):
        """Le 15 chiavi di input/bottone del brief
        (14 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st704_[a-z0-9_]+)"', _ui_src())
        attese = ["st704_domanda", "st704_eer_base",
                  "st704_eer_evap",
                  "st704_prezzo_elettricita",
                  "st704_consumo_acqua",
                  "st704_prezzo_acqua", "st704_opex",
                  "st704_potenza",
                  "st704_costo_specifico",
                  "st704_costo_fisso", "st704_fattore_co2",
                  "st704_vita", "st704_wacc",
                  "st704_tolleranza", "st704_calcola"]
        assert len(attese) == 15
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg704" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg704") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg704")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "EER evaporativo" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd704" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_evaporativo_presente(self):
        src = _ui_src().lower()
        assert "evaporazione" in src
        assert "bulbo umido" in src
        assert "climi secchi" in src
        assert "backup" in src
        assert "acqua" in src
        assert "senza compressore" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline chiller" in src
        assert "Evaporativo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh704_csv" in src
        assert "raffrescamento_evaporativo_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh704_sensitivita" in src
        assert "Heatmap" in src
        assert "EER evaporativo" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st704_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W705 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab704:")
        assert "mh704_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab704" in (_new_dir() / "w705_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w705_helpers.py", "w705_ui.py",
                   "w705_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab704"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "3"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w705_helpers.py", "w705_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_evaporativo_non_chiller(self):
        assert "evaporativo" in TITLE704.lower()
        assert "adiabatico" in TITLE704.lower()


class TestRegistryPostApply:
    """Check registry/count post-apply (pattern dei test
    per-tab precedenti): fallisce finche' l'apply
    di tab704 non e' fatto, perche' il titolo non
    e' ancora nella lista st.tabs di app.py e il
    conteggio delle tab e' ancora 703. NON e' un
    fallimento del codice di tab704: dopo
    l'apply questo test deve diventare verde."""

    def test_registry_count_704_e_titolo_in_st_tabs(self):
        app = _app_path()
        assert app.exists(), f"app.py non trovato: {app}"
        src = app.read_text(encoding="utf-8")
        assert "st.tabs(" in src
        m = re.search(
            r"((?:tab\d+\s*,\s*)*tab\d+)\s*=\s*st\.tabs\(",
            src)
        assert m is not None, "riga unpack st.tabs non trovata"
        n_tab = len(re.findall(r"tab\d+", m.group(1)))
        assert n_tab == 819, \
            f"conteggio tab {n_tab} != 704 (atteso post-apply)"
        idx = src.index("st.tabs(")
        assert TITLE704 in src[idx:], \
            "titolo tab704 non ancora nella lista st.tabs " \
            "(atteso prima dell'apply)"
