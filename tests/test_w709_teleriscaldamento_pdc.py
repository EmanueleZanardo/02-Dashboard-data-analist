"""Test tab709 "🏭🌡️ Teleriscaldamento con pompa di calore di rete: la PdC distrettuale paga contro la caldaia a gas?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda termica 5000 MWh/anno; ore
equivalenti 2000 h/anno; SCOP 3,0;
rendimento caldaia 0,90; prezzo gas 80
EUR/MWh; prezzo elettricita' 90 EUR/MWh;
opex caldaia 30000 EUR/anno; opex PdC 60000
EUR/anno; CAPEX PdC 900 EUR/kW termico;
CAPEX caldaia 150 EUR/kW termico; vita 20
anni; WACC 0,05 (5 %); tolleranza 0,10
(10 % del |CAPEX delta|); fattore gas 0,202
t/MWh; fattore elettrico 0,25 t/MWh.

- potenza_th_kw = 2500.0
- potenza_el_kw = 833.3333333333334
- gas_mwh_a = 5555.555555555556
- elettricita_mwh_a = 1666.6666666666667
- costo_base_eur_a = 474444.44444444444
- costo_alt_eur_a = 210000.0
- risparmio_eur_a = 264444.44444444444
- capex_pdc_eur = 2250000.0
- capex_caldaia_eur = 375000.0
- capex_delta_eur = 1875000.0
- co2_gas_t_a = 1122.2222222222224
- co2_el_t_a = 416.6666666666667
- co2_evitata_t_a = 705.5555555555557
- van = 1420562.2905827975
- tir = 12.845882801580434
- payback = 8
- verdetto = 'CONVIENTE'

Scomposizione: P_th 5000 x 1000 / 2000 =
2500.0 kW; P_el 2500.0 / 3,0 =
833.3333333333334 kW; gas 5000 / 0,90 =
5555.555555555556 MWh; elettricita' 5000 /
3,0 = 1666.6666666666667 MWh; C_base
5555.555555555556 x 80 + 30000 =
474444.44444444444; C_alt
1666.6666666666667 x 90 + 60000 = 210000.0;
risparmio 474444.44444444444 - 210000.0 =
264444.44444444444; CAPEX PdC 2500.0 x 900
= 2250000.0; CAPEX caldaia 2500.0 x 150 =
375000.0; CAPEX delta 2250000.0 - 375000.0
= 1875000.0; VAN -1875000.0 +
264444.44444444444 x (1 - 1,05^-20) / 0,05
= 1420562.2905827975; TIR 12,845882801580434
% (flussi [-1875000, 264444,44 x 20]: VAN
zero al 12,85 % circa); payback 8 (cumulato
anno 7 = -1875000 + 264444,44 x 7 =
-23888,89 < 0; anno 8 = 240555,56 >= 0);
VAN >= 0 -> CONVIENTE. CO2: gas
5555.555555555556 x 0,202 =
1122.2222222222224 t/anno; elettrica
1666.6666666666667 x 0,25 =
416.6666666666667; evitata 1122.2222222222224
- 416.6666666666667 = 705.5555555555557
t/anno. Prezzi termici di confronto: gas
80 / 0,90 = 88,888... EUR/MWh termico
contro elettricita' 90 / 3,0 = 30,0
EUR/MWh termico: e' li' che la PdC vince.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w710_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w710_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w710_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w710_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w710_helpers.py: {missing}")
    return out


_F = _load("mh709_num", "mh709_nneg", "mh709_pos",
           "mh709_int_pos", "mh709_int_nneg",
           "mh709_quota_valida", "mh709_eta_valido",
           "mh709_potenza_termica",
           "mh709_potenza_elettrica",
           "mh709_gas_mwh", "mh709_elettricita_mwh",
           "mh709_costo_base", "mh709_costo_alt",
           "mh709_risparmio", "mh709_capex",
           "mh709_capex_delta", "mh709_co2_gas",
           "mh709_co2_el", "mh709_co2_evitata",
           "mh709_crf", "mh709_van", "mh709_tir",
           "mh709_payback", "mh709_verdetto",
           "mh709_valida", "_mh709_neutro",
           "mh709_calcola", "mh709_sensitivita",
           "mh709_csv", "mh709_demo", "demo_calcoli")

TITLE709 = ("🏭🌡️ Teleriscaldamento con pompa di calore di rete: "
            "la PdC distrettuale paga contro la caldaia a gas?")

P_TH_DEMO = 2500.0
P_EL_DEMO = 833.3333333333334
GAS_DEMO = 5555.555555555556
EL_DEMO = 1666.6666666666667
C_BASE_DEMO = 474444.44444444444
C_ALT_DEMO = 210000.0
RISPARMIO_DEMO = 264444.44444444444
CX_PDC_DEMO = 2250000.0
CX_CAL_DEMO = 375000.0
DELTA_DEMO = 1875000.0
CO2_G_DEMO = 1122.2222222222224
CO2_E_DEMO = 416.6666666666667
CO2_EV_DEMO = 705.5555555555557
VAN_DEMO = 1420562.2905827975
TIR_DEMO = 12.845882801580434
PAYBACK_DEMO = 8
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.08024258719069129

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w710_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w710_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh709_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh709_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh709_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh709_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh709_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh709_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh709_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh709_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh709_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh709_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh709_int_pos"](5000.0, "x") == 5000

    def test_int_nneg_accetta_zero(self):
        assert _F["mh709_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh709_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh709_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh709_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh709_quota_valida"](0.0, "x") == 0.0
        assert _F["mh709_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh709_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh709_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh709_eta_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh709_demo"]()
        d.update(kw)
        return _F["mh709_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        assert self._val(domanda_th_mwh_a=0.0)["valido"] is False

    def test_domanda_negativa_non_valida(self):
        assert self._val(domanda_th_mwh_a=-1.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_eq_h=0.0)["valido"] is False

    def test_scop_zero_non_valido(self):
        assert self._val(scop=0.0)["valido"] is False

    def test_scop_negativo_non_valido(self):
        assert self._val(scop=-1.0)["valido"] is False

    def test_eta_zero_non_valido(self):
        assert self._val(eta_caldaia=0.0)["valido"] is False

    def test_eta_sopra_uno_non_valido(self):
        assert self._val(eta_caldaia=1.1)["valido"] is False

    def test_eta_uno_valido(self):
        assert self._val(eta_caldaia=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh",
                  "prezzo_el_eur_mwh",
                  "opex_caldaia_eur_a", "opex_pdc_eur_a",
                  "capex_pdc_eur_kw_th",
                  "capex_caldaia_eur_kw_th", "wacc_frac",
                  "fattore_gas_t_mwh", "fattore_el_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=19.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(scop=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(domanda_th_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(domanda_th_mwh_a=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(scop="3.0")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(capex_pdc_eur_kw_th=0.0)["valido"] is True
        assert self._val(opex_pdc_eur_a=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_potenza_termica_demo(self):
        assert _F["mh709_potenza_termica"](
            5000.0, 2000.0) == pytest.approx(P_TH_DEMO, rel=REL)

    def test_potenza_termica_rifiuta_ore_zero(self):
        with pytest.raises(ValueError):
            _F["mh709_potenza_termica"](5000.0, 0.0)

    def test_potenza_elettrica_demo(self):
        assert _F["mh709_potenza_elettrica"](
            P_TH_DEMO, 3.0) == pytest.approx(P_EL_DEMO, rel=REL)

    def test_potenza_elettrica_rifiuta_scop_zero(self):
        with pytest.raises(ValueError):
            _F["mh709_potenza_elettrica"](P_TH_DEMO, 0.0)

    def test_gas_demo(self):
        assert _F["mh709_gas_mwh"](
            5000.0, 0.90) == pytest.approx(GAS_DEMO, rel=REL)

    def test_gas_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh709_gas_mwh"](5000.0, 0.0)

    def test_elettricita_demo(self):
        assert _F["mh709_elettricita_mwh"](
            5000.0, 3.0) == pytest.approx(EL_DEMO, rel=REL)

    def test_costo_base_demo(self):
        assert _F["mh709_costo_base"](
            GAS_DEMO, 80.0, 30000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_alt_demo(self):
        assert _F["mh709_costo_alt"](
            EL_DEMO, 90.0, 60000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh709_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh709_risparmio"](
            100000.0, 150000.0) == pytest.approx(
            -50000.0, rel=REL)

    def test_capex_pdc_demo(self):
        assert _F["mh709_capex"](
            P_TH_DEMO, 900.0) == pytest.approx(
            CX_PDC_DEMO, rel=REL)

    def test_capex_caldaia_demo(self):
        assert _F["mh709_capex"](
            P_TH_DEMO, 150.0) == pytest.approx(
            CX_CAL_DEMO, rel=REL)

    def test_capex_delta_demo(self):
        assert _F["mh709_capex_delta"](
            CX_PDC_DEMO, CX_CAL_DEMO) == pytest.approx(
            DELTA_DEMO, rel=REL)

    def test_capex_delta_puo_essere_negativo(self):
        assert _F["mh709_capex_delta"](
            100000.0, 375000.0) == pytest.approx(
            -275000.0, rel=REL)

    def test_co2_gas_demo(self):
        assert _F["mh709_co2_gas"](
            GAS_DEMO, 0.202) == pytest.approx(
            CO2_G_DEMO, rel=REL)

    def test_co2_el_demo(self):
        assert _F["mh709_co2_el"](
            EL_DEMO, 0.25) == pytest.approx(
            CO2_E_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh709_co2_evitata"](
            CO2_G_DEMO, CO2_E_DEMO) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_unita_gas(self):
        # 5555,555... MWh x 0,202 = 1122,22 t
        # (non kg): il fattore e' gia' in t/MWh.
        assert _F["mh709_co2_gas"](
            1000.0, 0.202) == pytest.approx(202.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh709_crf"](
            0.05, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh709_crf"](0.0, 20) == pytest.approx(
            1.0 / 20.0, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh709_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-20)) / 0.05
        assert _F["mh709_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh709_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.0,
            20) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 20, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh709_van"](RISPARMIO_DEMO, DELTA_DEMO, -0.01, 20)

    def test_van_accetta_delta_negativo(self):
        assert _F["mh709_van"](
            100000.0, -50000.0, 0.05, 1) == pytest.approx(
            50000.0 + 100000.0 / 1.05, rel=1e-12)

    def test_tir_demo(self):
        assert abs(_F["mh709_tir"](
            DELTA_DEMO, RISPARMIO_DEMO,
            VITA_DEMO) * 100.0 - TIR_DEMO) <= 0.05

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh709_tir"](DELTA_DEMO, 0.0, 20) is None
        assert _F["mh709_tir"](DELTA_DEMO, -100.0, 20) is None

    def test_tir_none_se_delta_zero(self):
        assert _F["mh709_tir"](0.0, RISPARMIO_DEMO, 20) is None

    def test_tir_none_se_delta_negativo(self):
        assert _F["mh709_tir"](-1000.0, 5000.0, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh709_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_bisezione_indipendente_delta_pos(self):
        delta = 625000.0
        flussi = [-delta] + [RISPARMIO_DEMO] * 20

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
        assert abs(tir_ind * 100.0 - 42.274474556623595) <= 0.05
        tir = _F["mh709_tir"](delta, RISPARMIO_DEMO, 20)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh709_tir"](DELTA_DEMO, RISPARMIO_DEMO, 20)
        npv = -DELTA_DEMO + sum(
            RISPARMIO_DEMO / (1.0 + tir) ** i
            for i in range(1, 21))
        assert abs(npv) <= 1e-6 * DELTA_DEMO

    def test_payback_demo_otto(self):
        assert _F["mh709_payback"](
            DELTA_DEMO, RISPARMIO_DEMO, VITA_DEMO) == 8
        assert -DELTA_DEMO + RISPARMIO_DEMO * 7 < 0.0
        assert -DELTA_DEMO + RISPARMIO_DEMO * 8 >= 0.0

    def test_payback_zero_se_delta_zero(self):
        assert _F["mh709_payback"](0.0, RISPARMIO_DEMO, 20) == 0

    def test_payback_zero_se_delta_negativo(self):
        assert _F["mh709_payback"](-125000.0, RISPARMIO_DEMO, 20) == 0

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh709_payback"](1000.0, 300.0, 10) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh709_payback"](
            50000000.0, RISPARMIO_DEMO, 20) is None

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh709_payback"](DELTA_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh709_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh709_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh709_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh709_verdetto"](
            -187500.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh709_verdetto"](
            -187500.0000001, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_negativo_usa_valore_assoluto(self):
        assert _F["mh709_verdetto"](
            -100.0, -125000.0, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"
        assert _F["mh709_verdetto"](
            -20000.0, -125000.0, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh709_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh709_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh709_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh709_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_zero_mai_marginale(self):
        assert _F["mh709_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh709_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh709_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh709_demo"]()
        d.update(kw)
        return _F["mh709_calcola"](**d)

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
        assert c["elettricita_mwh_a"] == pytest.approx(
            EL_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_pdc_eur"] == pytest.approx(
            CX_PDC_DEMO, rel=REL)
        assert c["capex_caldaia_eur"] == pytest.approx(
            CX_CAL_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["co2_gas_t_a"] == pytest.approx(
            CO2_G_DEMO, rel=REL)
        assert c["co2_el_t_a"] == pytest.approx(
            CO2_E_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
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
        d = _F["mh709_demo"]()
        b = _F["mh709_calcola"](**d)
        coppie = [("potenza_th_kw", P_TH_DEMO),
                  ("potenza_el_kw", P_EL_DEMO),
                  ("gas_mwh_a", GAS_DEMO),
                  ("elettricita_mwh_a", EL_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_pdc_eur", CX_PDC_DEMO),
                  ("capex_caldaia_eur", CX_CAL_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_gas_t_a", CO2_G_DEMO),
                  ("co2_el_t_a", CO2_E_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh709_demo"]()
        assert d["domanda_th_mwh_a"] == 5000.0
        assert d["ore_eq_h"] == 2000.0
        assert d["scop"] == 3.0
        assert d["eta_caldaia"] == 0.90
        assert d["prezzo_gas_eur_mwh"] == 80.0
        assert d["prezzo_el_eur_mwh"] == 90.0
        assert d["opex_caldaia_eur_a"] == 30000.0
        assert d["opex_pdc_eur_a"] == 60000.0
        assert d["capex_pdc_eur_kw_th"] == 900.0
        assert d["capex_caldaia_eur_kw_th"] == 150.0
        assert d["vita_anni"] == 20
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_gas_t_mwh"] == 0.202
        assert d["fattore_el_t_mwh"] == 0.25

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_th_kw", "potenza_el_kw",
                       "gas_mwh_a", "elettricita_mwh_a",
                       "costo_base_eur_a", "costo_alt_eur_a",
                       "risparmio_eur_a", "capex_pdc_eur",
                       "capex_caldaia_eur", "capex_delta_eur",
                       "co2_gas_t_a", "co2_el_t_a",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert "tir = 12.845882801580434" in doc
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_el_alto_neutro_risparmio_negativo(self):
        # Prezzo elettricita' 300: C_alt 560000 >
        # C_base 474444,44 -> risparmio negativo
        n = self._bc(prezzo_el_eur_mwh=300.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_opex_pdc_alto_riduce_risparmio(self):
        # Opex PdC 100000: C_alt 250000, risparmio
        # 224444,44; VAN ancora positivo; CONVIENTE
        # (con opex 200000 il VAN diventerebbe
        # negativo: 124444,44 x 12,4622 < 1875000)
        n = self._bc(opex_pdc_eur_a=100000.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            224444.44444444444, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_delta_zero_mai_marginale(self):
        # CAPEX PdC 150 = CAPEX caldaia -> delta 0
        n = self._bc(capex_pdc_eur_kw_th=150.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_capex_delta_negativo_payback_zero_tir_none(self):
        # CAPEX PdC 100 < caldaia: delta -125000
        n = self._bc(capex_pdc_eur_kw_th=100.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            -125000.0, rel=REL)
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_delta_positivo_payback_e_tir(self):
        # CAPEX PdC 400: delta 625000; VAN
        # 2670562,2905827975; TIR 42,274... %;
        # payback 3; CONVIENTE
        n = self._bc(capex_pdc_eur_kw_th=400.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            625000.0, rel=REL)
        assert abs(n["van"] - 2670562.2905827975) <= 1.0
        assert abs(n["tir"] - 42.274474556623595) <= 0.05
        assert n["payback"] == 3
        assert n["verdetto"] == "CONVIENTE"

    def test_marginale_ad_hoc(self):
        # CAPEX PdC 190, vita 1, WACC 0,12,
        # prezzo elettricita' 185: delta 100000;
        # risparmio 106111,11; VAN -5257,94
        # entro tolleranza 10000 -> MARGINALE;
        # payback 1; TIR 6,11 %
        n = self._bc(capex_pdc_eur_kw_th=190.0,
                     vita_anni=1, wacc_frac=0.12,
                     prezzo_el_eur_mwh=185.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            100000.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            106111.11111111107, rel=REL)
        assert abs(n["van"] - (-5257.936507936494)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 1

    def test_scop_due_potenza_elettrica_1250(self):
        # SCOP 2,0 (non 1,0: con SCOP 1,0 la PdC
        # costerebbe 510000 > base 474444 e il
        # caso diventerebbe NON_CALCOLABILE)
        n = self._bc(scop=2.0)
        assert n["valid"] is True
        assert n["potenza_el_kw"] == pytest.approx(
            1250.0, rel=REL)

    def test_scop_zero_neutro(self):
        n = self._bc(scop=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_caldaia=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_th_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=19.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

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
        n = self._bc(domanda_th_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(domanda_th_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -delta + risparmio x 20 =
        # -1875000 + 5288888,888888889 =
        # 3413888,888888889 -> CONVIENTE
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 20, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh709_neutro"]()
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
        n = _F["_mh709_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_th_mwh_a",
                       "ore_eq_h", "scop",
                       "eta_caldaia",
                       "potenza_th_kw",
                       "potenza_el_kw",
                       "gas_mwh_a",
                       "elettricita_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_pdc_eur",
                       "capex_caldaia_eur",
                       "capex_delta_eur",
                       "co2_gas_t_a",
                       "co2_el_t_a",
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
        assert len(b["df_tabella"]) == 26
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza termica (kW)" in voci
        assert "Gas annuo (MWh/anno)" in voci
        assert "Elettricita' annua (MWh/anno)" in voci
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
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-DELTA_DEMO + RISPARMIO_DEMO * VITA_DEMO,
                          rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-DELTA_DEMO, rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh709_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh709_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh709_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo_gas(self):
        s = _F["mh709_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_el(self):
        s = _F["mh709_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh709_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh709_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # Prezzo gas x0.9 e prezzo elettricita'
        # x1.1: risparmio 205000,00 > 0, VAN
        # 679753,120220698
        s = _F["mh709_sensitivita"](self._ing())
        assert s.loc["x0.9", "x1.1"] != 0.0
        assert abs(s.loc["x0.9", "x1.1"] - 679753.120220698) <= 1.0
        ing = self._ing()
        ing["prezzo_gas_eur_mwh"] = 80.0 * 0.9
        ing["prezzo_el_eur_mwh"] = 90.0 * 1.1
        assert _F["mh709_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            205000.0, rel=REL)

    def test_sensitivita_angoli(self):
        s = _F["mh709_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 1053619.430496898) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 2161371.460944897) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 1787505.150668697) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh709_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 31

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh709_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_th_mwh_a" in txt
        assert "potenza_th_kw" in txt
        assert "co2_evitata_t_a" in txt
        assert "scop" in txt
        assert "capex_pdc_eur" in txt
        assert "capex_delta_eur" in txt
        assert "gas_mwh_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh709_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "domanda_th_mwh_a;5000.0" in txt
        assert "opex_pdc_eur_a;60000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def709["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def709\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh709_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh709_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh709_demo():")
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
        ui_keys = set(re.findall(r'_def709\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W710 (25/10/2026) - tab709' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh709_num", "mh709_nneg", "mh709_pos",
                     "mh709_int_pos", "mh709_int_nneg",
                     "mh709_quota_valida", "mh709_eta_valido",
                     "mh709_potenza_termica",
                     "mh709_potenza_elettrica",
                     "mh709_gas_mwh", "mh709_elettricita_mwh",
                     "mh709_costo_base", "mh709_costo_alt",
                     "mh709_risparmio", "mh709_capex",
                     "mh709_capex_delta", "mh709_co2_gas",
                     "mh709_co2_el", "mh709_co2_evitata",
                     "mh709_crf", "mh709_van", "mh709_tir",
                     "mh709_payback", "mh709_verdetto",
                     "mh709_valida", "_mh709_neutro",
                     "mh709_calcola", "mh709_sensitivita",
                     "mh709_csv", "mh709_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        assert "mh708" not in _helpers_src()
        assert "tab708" not in _helpers_src()
        assert "mh708" not in _ui_src()
        assert "tab708" not in _ui_src()

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w710_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE709) == 1

    def test_blocco_with_tab709(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab709:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE709

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st709_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st709_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone (15 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st709_[a-z0-9_]+)"', _ui_src())
        attese = ["st709_domanda", "st709_ore",
                  "st709_scop", "st709_eta",
                  "st709_p_gas", "st709_p_el",
                  "st709_opex_caldaia", "st709_opex_pdc",
                  "st709_capex_pdc", "st709_capex_caldaia",
                  "st709_vita", "st709_wacc",
                  "st709_tolleranza", "st709_f_gas",
                  "st709_f_el", "st709_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg709" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg709") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg709")
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
        assert "_ver709" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "teleriscaldamento" in src
        assert "caldaia" in src
        assert "data center" in src
        assert "edificio" in src
        assert "scop" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "teleriscaldamento" in src.lower()
        assert "caldaia" in src.lower()
        assert "data center" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src
        assert "Risparmio annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh709_csv" in src
        assert "pdc_rete_teleriscaldamento_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh709_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo gas" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st709_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W710 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab709:")
