"""Test tab702 "🔥⚡ Pompa di calore ibrida: caldaia + pompa di calore, chi fa cosa?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
fabbisogno termico 200 MWh/anno; quota pompa
di calore 0,80; SCOP 3,0; rendimento caldaia
0,9; prezzo gas 100 EUR/MWh; prezzo
elettricita' 200 EUR/MWh; OPEX annuo 500
EUR/anno; potenza pompa di calore 80 kW;
costo specifico 700 EUR/kW; costo fisso 5000
EUR; vita 15 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del CAPEX); fattore gas
0,20 tCO2/MWh; fattore elettricita' 0,35
tCO2/MWh.

- calore_hp_mwh_a = 160.0
- calore_caldaia_mwh_a = 39.99999999999999
- energia_hp_mwh_a = 53.333333333333336
- gas_caldaia_mwh_a = 44.444444444444436
- costo_baseline_eur_a = 22222.222222222223
- costo_ibrido_eur_a = 15611.111111111111
- risparmio_eur_a = 6611.111111111111
- co2_base_t_a = 44.44444444444445
- co2_ibrida_t_a = 27.555555555555557
- co2_evitata_t_a = 16.888888888888893
- capex_eur = 61000.0
- van = 7621.072585749513
- tir = 6.795232413308154
- payback = 10
- verdetto = 'CONVIENTE'

Scomposizione: Q_hp 200 x 0,80 = 160.0;
Q_cald 200 x 0,20 = 39.99999999999999;
E_hp 160,0 / 3,0 = 53.333333333333336;
F_cald 39.99999999999999 / 0,9 =
44.444444444444436; c_base 200 / 0,9 x 100 =
22222.222222222223; c_ibrida
53.333333333333336 x 200 +
44.444444444444436 x 100 + 500 =
15611.111111111111; risparmio
22222.222222222223 - 15611.111111111111 =
6611.111111111111; co2_base 200 / 0,9 x
0,20 = 44.44444444444445; co2_ibrida
53.333333333333336 x 0,35 +
44.444444444444436 x 0,20 =
27.555555555555557; co2_evitata
44.44444444444445 - 27.555555555555557 =
16.888888888888893; capex 80 x 700 + 5000 =
61000.0; VAN -61000,0 +
6611.111111111111 x (1 - 1,05^-15) / 0,05 =
7621.072585749513; TIR per bisezione su
[-0,99, 5,0] dei flussi [-61000,
6611.111111111111 x 15]: 6.795232413308154 %
(VAN a quella TIR ~0); payback: cumulato
anno 9 -1500.0, anno 10 +5111.1111111111095
-> 10.
NOTA: i valori esatti ricalcolati sono
quelli sopra (VAN 7621,07, TIR 6,7952 %) —
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
    if (p / "w703_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w703_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w703_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w703_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w703_helpers.py: {missing}")
    return out


_F = _load("mh702_num", "mh702_nneg", "mh702_pos",
           "mh702_int_pos", "mh702_rendimento_valido",
           "mh702_quota_valida",
           "mh702_calore_hp", "mh702_calore_caldaia",
           "mh702_energia_hp", "mh702_gas_caldaia",
           "mh702_costo_baseline", "mh702_costo_ibrido",
           "mh702_risparmio", "mh702_co2_base",
           "mh702_co2_ibrida", "mh702_co2_evitata",
           "mh702_capex", "mh702_crf", "mh702_van",
           "mh702_tir", "mh702_payback",
           "mh702_verdetto", "mh702_valida",
           "_mh702_neutro", "mh702_calcola",
           "mh702_sensitivita", "mh702_csv",
           "mh702_demo", "demo_calcoli")

TITLE702 = ("🔥⚡ Pompa di calore ibrida: caldaia + pompa "
            "di calore, chi fa cosa?")

QHP_DEMO = 160.0
QCALD_DEMO = 39.99999999999999
EHP_DEMO = 53.333333333333336
FCALD_DEMO = 44.444444444444436
C_BASE_DEMO = 22222.222222222223
C_IBR_DEMO = 15611.111111111111
RISP_DEMO = 6611.111111111111
CO2_BASE_DEMO = 44.44444444444445
CO2_IBR_DEMO = 27.555555555555557
CO2_EV_DEMO = 16.888888888888893
CAPEX_DEMO = 61000.0
VAN_DEMO = 7621.072585749513
TIR_DEMO = 6.795232413308154
PAYBACK_DEMO = 10
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w703_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w703_ui.py").read_text(encoding="utf-8")


def _app_path():
    return Path.home() / "workspace/repo-dashboard/Dashboard-data-analist/app.py"


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh702_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh702_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh702_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh702_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh702_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh702_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh702_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh702_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh702_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh702_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh702_int_pos"](15.0, "x") == 15

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh702_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh702_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh702_rendimento_valido"](1.0, "x") == 1.0

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh702_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh702_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh702_quota_valida"](0.0, "x") == 0.0
        assert _F["mh702_quota_valida"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh702_demo"]()
        d.update(kw)
        return _F["mh702_valida"](**d)

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

    def test_quota_negativa_non_valida(self):
        v = self._val(quota_hp=-0.1)
        assert v["valido"] is False

    def test_quota_sopra_uno_non_valida(self):
        v = self._val(quota_hp=1.1)
        assert v["valido"] is False

    def test_quota_zero_e_uno_valide(self):
        assert self._val(quota_hp=0.0)["valido"] is True
        assert self._val(quota_hp=1.0)["valido"] is True

    def test_scop_zero_non_valido(self):
        v = self._val(scop=0.0)
        assert v["valido"] is False

    def test_scop_negativo_non_valido(self):
        v = self._val(scop=-3.0)
        assert v["valido"] is False

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
                  "prezzo_elettricita_eur_mwh", "opex_annuo",
                  "potenza_hp_kw", "costo_specifico_eur_kw",
                  "costo_fisso_eur", "wacc_frac",
                  "fattore_gas", "fattore_elettricita"):
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
        v = self._val(scop=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(fabbisogno_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(fabbisogno_mwh_a=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(scop="3.0")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(potenza_hp_kw=0.0)["valido"] is True
        assert self._val(opex_annuo=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_calore_hp_demo(self):
        assert _F["mh702_calore_hp"](
            200.0, 0.80) == pytest.approx(QHP_DEMO, rel=REL)

    def test_calore_hp_quota_zero(self):
        assert _F["mh702_calore_hp"](200.0, 0.0) == 0.0

    def test_calore_hp_quota_uno(self):
        assert _F["mh702_calore_hp"](
            200.0, 1.0) == pytest.approx(200.0, rel=REL)

    def test_calore_hp_rifiuta_quota_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh702_calore_hp"](200.0, 1.2)

    def test_calore_caldaia_demo(self):
        assert _F["mh702_calore_caldaia"](
            200.0, 0.80) == pytest.approx(QCALD_DEMO, rel=REL)

    def test_calore_caldaia_quota_uno_zero(self):
        assert _F["mh702_calore_caldaia"](200.0, 1.0) == 0.0

    def test_calori_sommano_a_fabbisogno(self):
        assert _F["mh702_calore_hp"](200.0, 0.80) + \
            _F["mh702_calore_caldaia"](200.0, 0.80) == pytest.approx(
                200.0, rel=REL)

    def test_energia_hp_demo(self):
        assert _F["mh702_energia_hp"](
            QHP_DEMO, 3.0) == pytest.approx(EHP_DEMO, rel=REL)

    def test_energia_hp_rifiuta_scop_zero(self):
        with pytest.raises(ValueError):
            _F["mh702_energia_hp"](QHP_DEMO, 0.0)

    def test_gas_caldaia_demo(self):
        assert _F["mh702_gas_caldaia"](
            QCALD_DEMO, 0.9) == pytest.approx(FCALD_DEMO, rel=REL)

    def test_gas_caldaia_rifiuta_rendimento_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh702_gas_caldaia"](QCALD_DEMO, 1.2)

    def test_costo_baseline_demo(self):
        assert _F["mh702_costo_baseline"](
            200.0, 0.9, 100.0) == pytest.approx(C_BASE_DEMO, rel=REL)

    def test_costo_ibrido_demo(self):
        assert _F["mh702_costo_ibrido"](
            EHP_DEMO, 200.0, FCALD_DEMO, 100.0,
            500.0) == pytest.approx(C_IBR_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh702_risparmio"](
            C_BASE_DEMO, C_IBR_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh702_risparmio"](
            22222.22, 36944.44) == pytest.approx(
            -14722.22, rel=1e-6)

    def test_co2_base_demo(self):
        assert _F["mh702_co2_base"](
            200.0, 0.9, 0.20) == pytest.approx(
            CO2_BASE_DEMO, rel=REL)

    def test_co2_ibrida_demo(self):
        assert _F["mh702_co2_ibrida"](
            EHP_DEMO, 0.35, FCALD_DEMO,
            0.20) == pytest.approx(CO2_IBR_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh702_co2_evitata"](
            CO2_BASE_DEMO, CO2_IBR_DEMO) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh702_co2_evitata"](
            44.44, 60.0) == pytest.approx(-15.56, rel=1e-6)

    def test_capex_demo(self):
        assert _F["mh702_capex"](
            80.0, 700.0, 5000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh702_capex"](
            0.0, 700.0, 5000.0) == 5000.0

    def test_capex_scala_con_potenza(self):
        assert _F["mh702_capex"](
            160.0, 700.0, 5000.0) == pytest.approx(
            117000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh702_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh702_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 15 / (1.05 ** 15 - 1.0)
        assert _F["mh702_crf"](0.05, 15) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh702_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh702_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh702_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh702_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh702_van"](RISP_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh702_tir"](
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
        tir = _F["mh702_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh702_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh702_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh702_tir"](0.0, RISP_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh702_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh702_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh702_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 9 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 10 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh702_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh702_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh702_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh702_payback"](
            50000000.0, RISP_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh702_payback"](0.0, RISP_DEMO, 15) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh702_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh702_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh702_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh702_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 6100 = 10 % di CAPEX 61000
        assert _F["mh702_verdetto"](
            -6100.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh702_verdetto"](
            -6100.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh702_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh702_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh702_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh702_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh702_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh702_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh702_verdetto"](100.0, CAPEX_DEMO, 1.5, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh702_demo"]()
        d.update(kw)
        return _F["mh702_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["calore_hp_mwh_a"] == pytest.approx(
            QHP_DEMO, rel=REL)
        assert c["calore_caldaia_mwh_a"] == pytest.approx(
            QCALD_DEMO, rel=REL)
        assert c["energia_hp_mwh_a"] == pytest.approx(
            EHP_DEMO, rel=REL)
        assert c["gas_caldaia_mwh_a"] == pytest.approx(
            FCALD_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_ibrido_eur_a"] == pytest.approx(
            C_IBR_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_base_t_a"] == pytest.approx(
            CO2_BASE_DEMO, rel=REL)
        assert c["co2_ibrida_t_a"] == pytest.approx(
            CO2_IBR_DEMO, rel=REL)
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
        d = _F["mh702_demo"]()
        b = _F["mh702_calcola"](**d)
        coppie = [("calore_hp_mwh_a", QHP_DEMO),
                  ("calore_caldaia_mwh_a", QCALD_DEMO),
                  ("energia_hp_mwh_a", EHP_DEMO),
                  ("gas_caldaia_mwh_a", FCALD_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_ibrido_eur_a", C_IBR_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_base_t_a", CO2_BASE_DEMO),
                  ("co2_ibrida_t_a", CO2_IBR_DEMO),
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
        d = _F["mh702_demo"]()
        assert d["fabbisogno_mwh_a"] == 200.0
        assert d["quota_hp"] == 0.80
        assert d["scop"] == 3.0
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 100.0
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["opex_annuo"] == 500.0
        assert d["potenza_hp_kw"] == 80.0
        assert d["costo_specifico_eur_kw"] == 700.0
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
        for chiave in ("calore_hp_mwh_a",
                       "calore_caldaia_mwh_a",
                       "energia_hp_mwh_a",
                       "gas_caldaia_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_ibrido_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_ibrida_t_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 10" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_quota_04_non_conviente(self):
        # Quota 0,40: Q_hp 80, E 26,6667, Q_cald
        # 120, F 133,3333; c_ibr 19166,6667;
        # risparmio 3055,5556; VAN -29284,38
        n = self._bc(quota_hp=0.40)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            3055.5555555555547, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_scop_25_non_conviente(self):
        # SCOP 2,5: E 64,0; c_ibr 17777,7778;
        # risparmio 4477,7778; VAN -14522,20
        n = self._bc(scop=2.5)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            4477.777777777777, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_quota_zero_neutro_via_risparmio(self):
        # Quota 0: c_ibr = 22222,2222 + 500 =
        # 22722,2222 contro c_base 22222,2222 ->
        # risparmio -500
        n = self._bc(quota_hp=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["tir"] is None
        assert n["payback"] is None

    def test_quota_uno_conviente(self):
        # Quota 1: Q_cald 0, F 0; E 66,6667;
        # c_ibr 13833,3333; risparmio 8388,8889
        n = self._bc(quota_hp=1.0)
        assert n["valid"] is True
        assert n["calore_caldaia_mwh_a"] == pytest.approx(
            0.0, abs=1e-12)
        assert n["gas_caldaia_mwh_a"] == pytest.approx(
            0.0, abs=1e-12)
        assert n["risparmio_eur_a"] == pytest.approx(
            8388.888888888889, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_quota_sopra_uno_neutro(self):
        n = self._bc(quota_hp=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_quota_negativa_neutro(self):
        n = self._bc(quota_hp=-0.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fabbisogno_zero_neutro(self):
        n = self._bc(fabbisogno_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_scop_zero_neutro(self):
        n = self._bc(scop=0.0)
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
        # VAN circa -9950,75, oltre il 10 % del
        # CAPEX (6100); payback 10 (cumulato anno
        # 10 = 5111,11 >= 0, ma il VAN a 5 % resta
        # negativo: il payback semplice ignora
        # l'attualizzazione)
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 10

    def test_vita_dieci_tolleranza_uno_marginale(self):
        # Stesso VAN -9950,75 ma tolleranza 1,0:
        # entro il 100 % del CAPEX -> MARGINALE
        n = self._bc(vita_anni=10, tolleranza_frac=1.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"

    def test_vita_venti_conviente(self):
        # VAN circa 21389,06
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
        n = self._bc(scop=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(fabbisogno_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(fabbisogno_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_elettricita_600_neutro_via_risparmio(self):
        # Prezzo elettricita' 600: c_ibr 36944,44
        # contro c_base 22222,22 -> risparmio < 0
        n = self._bc(prezzo_elettricita_eur_mwh=600.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_prezzo_elettricita_250_non_conviente(self):
        # Risparmio 3944,44 ma VAN -20058,02:
        # NON_CONVIENTE, non neutro; payback
        # None (15 x 3944,44 < CAPEX)
        n = self._bc(prezzo_elettricita_eur_mwh=250.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
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
        n = _F["_mh702_neutro"]()
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
        n = _F["_mh702_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "fabbisogno_mwh_a",
                       "quota_hp",
                       "calore_hp_mwh_a",
                       "calore_caldaia_mwh_a",
                       "energia_hp_mwh_a",
                       "gas_caldaia_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_ibrido_eur_a",
                       "risparmio_eur_a",
                       "co2_base_t_a",
                       "co2_ibrida_t_a",
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
        assert len(b["df_tabella"]) == 24
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Fabbisogno termico (MWh/anno)" in voci
        assert "Calore pompa di calore (MWh/anno)" in voci
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
        return _F["mh702_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh702_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh702_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_quota(self):
        s = _F["mh702_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettricita(self):
        s = _F["mh702_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh702_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh702_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # Quota x0.9 (0,72) e prezzo elettricita'
        # x1.1 (220): risparmio 4940,00 > 0,
        # quindi VAN non degenere
        s = _F["mh702_sensitivita"](self._ing())
        assert s.loc["x0.9", "x1.1"] != 0.0
        ing = self._ing()
        ing["quota_hp"] = 0.80 * 0.9
        ing["prezzo_elettricita_eur_mwh"] = 200.0 * 1.1
        assert _F["mh702_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            4939.999999999996, rel=REL)

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh702_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 31

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh702_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_ibrido_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "fabbisogno_mwh_a" in txt
        assert "calore_hp_mwh_a" in txt
        assert "energia_hp_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "quota_hp" in txt
        assert "costo_fisso_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh702_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert "calore_hp_mwh_a;160.0" in txt
        assert "opex_annuo;500.0" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def702["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def702\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh702_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh702_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh702_demo():")
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
        ui_keys = set(re.findall(r'_def702\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W703 (25/10/2026) - tab702' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh702_num", "mh702_nneg", "mh702_pos",
                     "mh702_int_pos", "mh702_rendimento_valido",
                     "mh702_quota_valida",
                     "mh702_calore_hp", "mh702_calore_caldaia",
                     "mh702_energia_hp", "mh702_gas_caldaia",
                     "mh702_costo_baseline",
                     "mh702_costo_ibrido",
                     "mh702_risparmio", "mh702_co2_base",
                     "mh702_co2_ibrida", "mh702_co2_evitata",
                     "mh702_capex", "mh702_crf",
                     "mh702_van", "mh702_tir",
                     "mh702_payback", "mh702_verdetto",
                     "mh702_valida", "_mh702_neutro",
                     "mh702_calcola", "mh702_sensitivita",
                     "mh702_csv", "mh702_demo",
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
        ast.parse((_new_dir() / "w703_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE702) == 1

    def test_blocco_with_tab702(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab702:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE702

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st702_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st702_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone del brief
        (15 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st702_[a-z0-9_]+)"', _ui_src())
        attese = ["st702_fabbisogno", "st702_quota_hp",
                  "st702_scop", "st702_rendimento_caldaia",
                  "st702_prezzo_gas",
                  "st702_prezzo_elettricita", "st702_opex",
                  "st702_potenza_hp", "st702_costo_specifico",
                  "st702_costo_fisso", "st702_fattore_gas",
                  "st702_fattore_elettricita",
                  "st702_vita", "st702_wacc",
                  "st702_tolleranza", "st702_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg702" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg702") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg702")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Quota calore da pompa di calore (%)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd702" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_ibrido_presente(self):
        src = _ui_src().lower()
        assert "carico base" in src
        assert "picchi" in src
        assert "gelo" in src
        assert "backup" in src
        assert "scop reale" in src
        assert "quota" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline tutta-caldaia" in src
        assert "Ibrida" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh702_csv" in src
        assert "pompa_calore_ibrida_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh702_sensitivita" in src
        assert "Heatmap" in src
        assert "Quota pompa" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st702_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W703 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab702:")
        assert "mh702_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab702" in (_new_dir() / "w703_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w703_helpers.py", "w703_ui.py",
                   "w703_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab702"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "1"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w703_helpers.py", "w703_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_ibrido_non_standalone(self):
        assert "ibrida" in TITLE702.lower()
        assert "caldaia" in TITLE702.lower()


class TestRegistryPostApply:
    """Check registry post-apply (pattern dei test
    per-tab precedenti): fallisce finche' l'apply
    di tab702 non e' fatto, perche' il titolo non
    e' ancora nella lista st.tabs di app.py. NON
    e' un fallimento del codice di tab702: dopo
    l'apply questo test deve diventare verde."""

    def test_titolo_in_lista_st_tabs_app(self):
        app = _app_path()
        assert app.exists(), f"app.py non trovato: {app}"
        src = app.read_text(encoding="utf-8")
        assert "st.tabs(" in src
        idx = src.index("st.tabs(")
        assert TITLE702 in src[idx:], \
            "titolo tab702 non ancora nella lista st.tabs " \
            "(atteso prima dell'apply)"
