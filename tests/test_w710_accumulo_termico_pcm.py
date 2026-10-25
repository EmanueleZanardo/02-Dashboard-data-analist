"""Test tab710 "🧱🔥 Accumulo termico a cambiamento di fase (PCM): il calore latente paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
calore per ciclo 500 kWh; cicli 300/anno;
calore latente 55 Wh/kg; densita' PCM 900
kg/m3; salto termico utile 10 K; rendimento
PCM 0,96; rendimento acqua 0,88; prezzo di
carica 120 EUR/MWh; opex PCM 800 EUR/anno;
opex acqua 400 EUR/anno; costo PCM 1,5
EUR/kg; costo acqua 200 EUR/m3; costo fisso
PCM 4000 EUR; costo fisso acqua 2000 EUR;
vita 15 anni; WACC 0,05 (5 %); tolleranza
0,10 (10 % del |CAPEX delta|); fattore di
carica 0,35 t/MWh.

- q_annua_kwh_a = 150000.0
- massa_pcm_kg = 9090.90909090909
- volume_pcm_m3 = 10.1010101010101
- volume_acqua_m3 = 42.99226139294927
- e_carica_pcm_kwh_ciclo = 520.8333333333334
- e_carica_acqua_kwh_ciclo = 568.1818181818181
- costo_base_eur_a = 20854.545454545452
- costo_alt_eur_a = 19550.0
- risparmio_eur_a = 1304.5454545454522
- capex_pcm_eur = 17636.363636363636
- capex_acqua_eur = 10598.452278589853
- capex_delta_eur = 7037.911357773783
- co2_evitata_t_a = 4.971590909090899
- van = 6502.824355670884
- tir = 16.710551026105524
- payback = 6
- verdetto = 'CONVIENTE'

Scomposizione: Q_annua 500 x 300 =
150000.0 kWh/anno; m_pcm 500 x 1000 / 55 =
9090.90909090909 kg; V_pcm 9090.90909090909
/ 900 = 10.1010101010101 m3; V_acqua 500 /
(1,163 x 10) = 42.99226139294927 m3;
E_pcm 500 / 0,96 = 520.8333333333334
kWh/ciclo; E_acqua 500 / 0,88 =
568.1818181818181 kWh/ciclo; C_base 300 x
568.1818181818181 / 1000 x 120 + 400 =
20854.545454545452; C_alt 300 x
520.8333333333334 / 1000 x 120 + 800 =
19550.0; risparmio 20854.545454545452 -
19550.0 = 1304.5454545454522; CAPEX PCM
9090.90909090909 x 1,5 + 4000 =
17636.363636363636; CAPEX acqua
42.99226139294927 x 200 + 2000 =
10598.452278589853; CAPEX delta
17636.363636363636 - 10598.452278589853 =
7037.911357773783; VAN -7037.911357773783 +
1304.5454545454522 x (1 - 1,05^-15) / 0,05
= 6502.824355670884; TIR 16.710551026105524
% (flussi [-7037,91, 1304,55 x 15]: VAN
zero al 16,71 % circa); payback 6 (cumulato
anno 5 = -7037,91 + 1304,55 x 5 = -515,14
< 0; anno 6 = 789,41 >= 0);
VAN >= 0 -> CONVIENTE. CO2: 300 x
(568.1818181818181 - 520.8333333333334) /
1000 x 0,35 = 4.971590909090899 t/anno.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w711_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w711_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w711_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w711_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w711_helpers.py: {missing}")
    return out


_F = _load("mh710_num", "mh710_nneg", "mh710_pos",
           "mh710_int_pos", "mh710_int_nneg",
           "mh710_quota_valida", "mh710_eta_valido",
           "mh710_q_annua", "mh710_massa_pcm",
           "mh710_volume_pcm", "mh710_volume_acqua",
           "mh710_energia_carica", "mh710_costo_base",
           "mh710_costo_alt", "mh710_risparmio",
           "mh710_capex_pcm", "mh710_capex_acqua",
           "mh710_capex_delta", "mh710_co2_evitata",
           "mh710_crf", "mh710_van", "mh710_tir",
           "mh710_payback", "mh710_verdetto",
           "mh710_valida", "_mh710_neutro",
           "mh710_calcola", "mh710_sensitivita",
           "mh710_csv", "mh710_demo", "demo_calcoli")

TITLE710 = ("🧱🔥 Accumulo termico a cambiamento di fase (PCM): "
            "il calore latente paga?")

Q_ANNUA_DEMO = 150000.0
MASSA_DEMO = 9090.90909090909
V_PCM_DEMO = 10.1010101010101
V_ACQUA_DEMO = 42.99226139294927
E_PCM_DEMO = 520.8333333333334
E_ACQUA_DEMO = 568.1818181818181
C_BASE_DEMO = 20854.545454545452
C_ALT_DEMO = 19550.0
RISPARMIO_DEMO = 1304.5454545454522
CX_PCM_DEMO = 17636.363636363636
CX_ACQUA_DEMO = 10598.452278589853
DELTA_DEMO = 7037.911357773783
CO2_EV_DEMO = 4.971590909090899
VAN_DEMO = 6502.824355670884
TIR_DEMO = 16.710551026105524
PAYBACK_DEMO = 6
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w711_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w711_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh710_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh710_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh710_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh710_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh710_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh710_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh710_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh710_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh710_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh710_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh710_int_pos"](300.0, "x") == 300

    def test_int_nneg_accetta_zero(self):
        assert _F["mh710_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh710_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh710_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh710_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh710_quota_valida"](0.0, "x") == 0.0
        assert _F["mh710_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh710_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh710_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh710_eta_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh710_demo"]()
        d.update(kw)
        return _F["mh710_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_q_zero_non_valido(self):
        assert self._val(q_ciclo_kwh=0.0)["valido"] is False

    def test_q_negativo_non_valido(self):
        assert self._val(q_ciclo_kwh=-1.0)["valido"] is False

    def test_cicli_zero_non_validi(self):
        assert self._val(cicli_anno=0)["valido"] is False

    def test_cicli_non_interi_non_validi(self):
        assert self._val(cicli_anno=299.5)["valido"] is False

    def test_latente_zero_non_valido(self):
        assert self._val(calore_latente_wh_kg=0.0)["valido"] is False

    def test_rho_zero_non_valido(self):
        assert self._val(rho_pcm_kg_m3=0.0)["valido"] is False

    def test_dt_zero_non_valido(self):
        assert self._val(dt_k=0.0)["valido"] is False

    def test_eta_pcm_zero_non_valido(self):
        assert self._val(eta_pcm=0.0)["valido"] is False

    def test_eta_pcm_sopra_uno_non_valido(self):
        assert self._val(eta_pcm=1.1)["valido"] is False

    def test_eta_acqua_sopra_uno_non_valido(self):
        assert self._val(eta_acqua=1.1)["valido"] is False

    def test_eta_uno_valida(self):
        assert self._val(eta_pcm=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("prezzo_carica_eur_mwh",
                  "opex_pcm_eur_a", "opex_acqua_eur_a",
                  "costo_pcm_eur_kg", "costo_acqua_eur_m3",
                  "fisso_pcm_eur", "fisso_acqua_eur",
                  "wacc_frac", "fattore_carica_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=14.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_pcm=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(q_ciclo_kwh=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(q_ciclo_kwh=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_pcm="0.96")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_carica_eur_mwh=0.0)["valido"] is True
        assert self._val(costo_pcm_eur_kg=0.0)["valido"] is True
        assert self._val(opex_pcm_eur_a=0.0)["valido"] is True
        assert self._val(fisso_pcm_eur=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_q_annua_demo(self):
        assert _F["mh710_q_annua"](
            500.0, 300) == pytest.approx(Q_ANNUA_DEMO, rel=REL)

    def test_massa_pcm_demo(self):
        assert _F["mh710_massa_pcm"](
            500.0, 55.0) == pytest.approx(MASSA_DEMO, rel=REL)

    def test_massa_pcm_rifiuta_latente_zero(self):
        with pytest.raises(ValueError):
            _F["mh710_massa_pcm"](500.0, 0.0)

    def test_volume_pcm_demo(self):
        assert _F["mh710_volume_pcm"](
            MASSA_DEMO, 900.0) == pytest.approx(V_PCM_DEMO, rel=REL)

    def test_volume_acqua_demo(self):
        assert _F["mh710_volume_acqua"](
            500.0, 10.0) == pytest.approx(V_ACQUA_DEMO, rel=REL)

    def test_volume_acqua_rifiuta_dt_zero(self):
        with pytest.raises(ValueError):
            _F["mh710_volume_acqua"](500.0, 0.0)

    def test_volume_acqua_dt_grande_piu_piccolo(self):
        # dT 20 K dimezza il volume rispetto a dT 10 K
        assert _F["mh710_volume_acqua"](
            500.0, 20.0) == pytest.approx(V_ACQUA_DEMO / 2.0,
                                         rel=REL)

    def test_energia_carica_pcm_demo(self):
        assert _F["mh710_energia_carica"](
            500.0, 0.96) == pytest.approx(E_PCM_DEMO, rel=REL)

    def test_energia_carica_acqua_demo(self):
        assert _F["mh710_energia_carica"](
            500.0, 0.88) == pytest.approx(E_ACQUA_DEMO, rel=REL)

    def test_energia_carica_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh710_energia_carica"](500.0, 0.0)

    def test_costo_base_demo(self):
        assert _F["mh710_costo_base"](
            300, E_ACQUA_DEMO, 120.0, 400.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_alt_demo(self):
        assert _F["mh710_costo_alt"](
            300, E_PCM_DEMO, 120.0, 800.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh710_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh710_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_capex_pcm_demo(self):
        assert _F["mh710_capex_pcm"](
            MASSA_DEMO, 1.5, 4000.0) == pytest.approx(
            CX_PCM_DEMO, rel=REL)

    def test_capex_acqua_demo(self):
        assert _F["mh710_capex_acqua"](
            V_ACQUA_DEMO, 200.0, 2000.0) == pytest.approx(
            CX_ACQUA_DEMO, rel=REL)

    def test_capex_delta_demo(self):
        assert _F["mh710_capex_delta"](
            CX_PCM_DEMO, CX_ACQUA_DEMO) == pytest.approx(
            DELTA_DEMO, rel=REL)

    def test_capex_delta_puo_essere_negativo(self):
        assert _F["mh710_capex_delta"](
            5000.0, 10598.452278589853) == pytest.approx(
            -5598.452278589853, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh710_co2_evitata"](
            300, E_ACQUA_DEMO, E_PCM_DEMO,
            0.35) == pytest.approx(CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_unita(self):
        # 300 cicli x 47,348 kWh / 1000 x 0,35
        assert _F["mh710_co2_evitata"](
            300, E_ACQUA_DEMO, E_PCM_DEMO,
            0.35) == pytest.approx(4.971590909090899, rel=REL)

    def test_crf_demo(self):
        assert _F["mh710_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh710_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh710_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh710_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh710_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.0,
            15) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh710_van"](RISPARMIO_DEMO, DELTA_DEMO, -0.01, 15)

    def test_van_accetta_delta_negativo(self):
        assert _F["mh710_van"](
            1000.0, -500.0, 0.05, 1) == pytest.approx(
            500.0 + 1000.0 / 1.05, rel=1e-12)

    def test_tir_demo(self):
        assert abs(_F["mh710_tir"](
            DELTA_DEMO, RISPARMIO_DEMO,
            VITA_DEMO) * 100.0 - TIR_DEMO) <= 0.05

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh710_tir"](DELTA_DEMO, 0.0, 15) is None
        assert _F["mh710_tir"](DELTA_DEMO, -100.0, 15) is None

    def test_tir_none_se_delta_zero(self):
        assert _F["mh710_tir"](0.0, RISPARMIO_DEMO, 15) is None

    def test_tir_none_se_delta_negativo(self):
        assert _F["mh710_tir"](-1000.0, 5000.0, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh710_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh710_tir"](DELTA_DEMO, RISPARMIO_DEMO, 15)
        npv = -DELTA_DEMO + sum(
            RISPARMIO_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * DELTA_DEMO

    def test_payback_demo_sei(self):
        assert _F["mh710_payback"](
            DELTA_DEMO, RISPARMIO_DEMO, VITA_DEMO) == 6
        assert -DELTA_DEMO + RISPARMIO_DEMO * 5 < 0.0
        assert -DELTA_DEMO + RISPARMIO_DEMO * 6 >= 0.0

    def test_payback_zero_se_delta_zero(self):
        assert _F["mh710_payback"](0.0, RISPARMIO_DEMO, 15) == 0

    def test_payback_zero_se_delta_negativo(self):
        assert _F["mh710_payback"](-1250.0, RISPARMIO_DEMO, 15) == 0

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh710_payback"](1000.0, 300.0, 10) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh710_payback"](
            500000.0, RISPARMIO_DEMO, 15) is None

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh710_payback"](DELTA_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh710_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh710_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh710_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh710_verdetto"](
            -703.7911357773783, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh710_verdetto"](
            -703.7911357773784, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_negativo_usa_valore_assoluto(self):
        assert _F["mh710_verdetto"](
            -100.0, -1250.0, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"
        assert _F["mh710_verdetto"](
            -200.0, -1250.0, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh710_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh710_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh710_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh710_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_zero_mai_marginale(self):
        assert _F["mh710_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh710_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh710_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh710_demo"]()
        d.update(kw)
        return _F["mh710_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["q_annua_kwh_a"] == pytest.approx(
            Q_ANNUA_DEMO, rel=REL)
        assert c["massa_pcm_kg"] == pytest.approx(
            MASSA_DEMO, rel=REL)
        assert c["volume_pcm_m3"] == pytest.approx(
            V_PCM_DEMO, rel=REL)
        assert c["volume_acqua_m3"] == pytest.approx(
            V_ACQUA_DEMO, rel=REL)
        assert c["e_carica_pcm_kwh_ciclo"] == pytest.approx(
            E_PCM_DEMO, rel=REL)
        assert c["e_carica_acqua_kwh_ciclo"] == pytest.approx(
            E_ACQUA_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_pcm_eur"] == pytest.approx(
            CX_PCM_DEMO, rel=REL)
        assert c["capex_acqua_eur"] == pytest.approx(
            CX_ACQUA_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
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
        d = _F["mh710_demo"]()
        b = _F["mh710_calcola"](**d)
        coppie = [("q_annua_kwh_a", Q_ANNUA_DEMO),
                  ("massa_pcm_kg", MASSA_DEMO),
                  ("volume_pcm_m3", V_PCM_DEMO),
                  ("volume_acqua_m3", V_ACQUA_DEMO),
                  ("e_carica_pcm_kwh_ciclo", E_PCM_DEMO),
                  ("e_carica_acqua_kwh_ciclo", E_ACQUA_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_pcm_eur", CX_PCM_DEMO),
                  ("capex_acqua_eur", CX_ACQUA_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh710_demo"]()
        assert d["q_ciclo_kwh"] == 500.0
        assert d["cicli_anno"] == 300
        assert d["calore_latente_wh_kg"] == 55.0
        assert d["rho_pcm_kg_m3"] == 900.0
        assert d["dt_k"] == 10.0
        assert d["eta_pcm"] == 0.96
        assert d["eta_acqua"] == 0.88
        assert d["prezzo_carica_eur_mwh"] == 120.0
        assert d["opex_pcm_eur_a"] == 800.0
        assert d["opex_acqua_eur_a"] == 400.0
        assert d["costo_pcm_eur_kg"] == 1.5
        assert d["costo_acqua_eur_m3"] == 200.0
        assert d["fisso_pcm_eur"] == 4000.0
        assert d["fisso_acqua_eur"] == 2000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_carica_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_annua_kwh_a", "massa_pcm_kg",
                       "volume_pcm_m3", "volume_acqua_m3",
                       "e_carica_pcm_kwh_ciclo",
                       "e_carica_acqua_kwh_ciclo",
                       "costo_base_eur_a", "costo_alt_eur_a",
                       "risparmio_eur_a", "capex_pcm_eur",
                       "capex_acqua_eur", "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert "tir = 16.710551026105524" in doc
        assert "payback = 6" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_eta_pcm_basso_neutro_risparmio_negativo(self):
        # Eta PCM 0,80 < acqua 0,88: E_pcm 625 >
        # E_acqua 568,18, C_alt 23300 > C_base
        # 20854,55 -> risparmio negativo
        n = self._bc(eta_pcm=0.80)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_opex_pcm_alto_riduce_risparmio(self):
        # Opex PCM 1500: C_alt 20250, risparmio
        # 604,55; VAN -1415,79 circa -> MARGINALE
        # (entro tolleranza 703,79? No: 1415,79 >
        # 703,79 -> NON_CONVIENTE); verifica con
        # opex 1000: C_alt 19750, risparmio
        # 1104,55, VAN 4452,82 -> CONVIENTE
        n = self._bc(opex_pcm_eur_a=1000.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            1104.5454545454522, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_delta_zero_mai_marginale(self):
        # Tutti i costi CAPEX a zero -> delta 0
        n = self._bc(costo_pcm_eur_kg=0.0, fisso_pcm_eur=0.0,
                     costo_acqua_eur_m3=0.0, fisso_acqua_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_capex_delta_negativo_payback_zero_tir_none(self):
        # Costo PCM 0,5 EUR/kg: delta -2052,997...
        n = self._bc(costo_pcm_eur_kg=0.5)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            -2052.9977331353093, rel=REL)
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_delta_positivo_payback_e_tir(self):
        # Costo fisso PCM 8000: delta 11037,91;
        # VAN 2502,82; payback 9; CONVIENTE
        n = self._bc(fisso_pcm_eur=8000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            11037.911357773783, rel=REL)
        assert abs(n["van"] - 2502.824355670884) <= 1.0
        assert n["payback"] == 9
        assert n["verdetto"] == "CONVIENTE"

    def test_marginale_ad_hoc(self):
        # Costo fisso PCM 12000: delta 15037,91;
        # VAN -1497,18 entro tolleranza 1503,79
        # -> MARGINALE; payback 12
        n = self._bc(fisso_pcm_eur=12000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            15037.911357773783, rel=REL)
        assert abs(n["van"] - (-1497.175644329116)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 12

    def test_dt_grande_riduce_volume_acqua(self):
        # dT 20 K: V_acqua dimezzato, CAPEX acqua
        # 6298,45 circa, delta piu' alto
        n = self._bc(dt_k=20.0)
        assert n["valid"] is True
        assert n["volume_acqua_m3"] == pytest.approx(
            V_ACQUA_DEMO / 2.0, rel=REL)

    def test_eta_zero_neutro(self):
        n = self._bc(eta_pcm=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_pcm=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_q_zero_neutro(self):
        n = self._bc(q_ciclo_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_non_interi_neutro(self):
        n = self._bc(cicli_anno=299.5)
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
        n = self._bc(eta_pcm=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(q_ciclo_kwh=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(q_ciclo_kwh=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -delta + risparmio x 15 =
        # -7037,91 + 19568,18 = 12530,27
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh710_neutro"]()
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
        n = _F["_mh710_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "q_ciclo_kwh", "cicli_anno",
                       "calore_latente_wh_kg",
                       "rho_pcm_kg_m3", "dt_k",
                       "eta_pcm", "eta_acqua",
                       "q_annua_kwh_a",
                       "massa_pcm_kg",
                       "volume_pcm_m3",
                       "volume_acqua_m3",
                       "e_carica_pcm_kwh_ciclo",
                       "e_carica_acqua_kwh_ciclo",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_pcm_eur",
                       "capex_acqua_eur",
                       "capex_delta_eur",
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
        assert len(b["df_tabella"]) == 29
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Massa PCM (kg)" in voci
        assert "Volume PCM (m3)" in voci
        assert "Volume acqua (m3)" in voci
        assert "Energia di carica PCM (kWh/ciclo)" in voci
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
        return _F["mh710_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh710_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh710_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_rendimento_pcm(self):
        s = _F["mh710_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_riga_peggiore_negativa(self):
        # Eta PCM x0,9 = 0,864 < acqua 0,88: il PCM
        # consuma piu' energia dell'acqua, VAN
        # grezzo negativo su tutta la riga
        s = _F["mh710_sensitivita"](self._ing())
        assert (s.loc["x0.9"] < 0.0).all()
        assert abs(s.loc["x0.9", "x1.0"] - (-15121.463224)) <= 1.0

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh710_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh710_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh710_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - (-14728.294359)) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - (-15514.632089)) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 20656.903499) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 27733.943070) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh710_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 35

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh710_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "q_ciclo_kwh" in txt
        assert "massa_pcm_kg" in txt
        assert "volume_pcm_m3" in txt
        assert "volume_acqua_m3" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_pcm" in txt
        assert "capex_pcm_eur" in txt
        assert "capex_delta_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh710_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "q_ciclo_kwh;500.0" in txt
        assert "opex_pcm_eur_a;800.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def710["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def710\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 18, ui_keys
        demo_keys = set(_F["mh710_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh710_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh710_demo():")
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
        ui_keys = set(re.findall(r'_def710\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W711 (25/10/2026) - tab710' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh710_num", "mh710_nneg", "mh710_pos",
                     "mh710_int_pos", "mh710_int_nneg",
                     "mh710_quota_valida", "mh710_eta_valido",
                     "mh710_q_annua", "mh710_massa_pcm",
                     "mh710_volume_pcm", "mh710_volume_acqua",
                     "mh710_energia_carica", "mh710_costo_base",
                     "mh710_costo_alt", "mh710_risparmio",
                     "mh710_capex_pcm", "mh710_capex_acqua",
                     "mh710_capex_delta", "mh710_co2_evitata",
                     "mh710_crf", "mh710_van", "mh710_tir",
                     "mh710_payback", "mh710_verdetto",
                     "mh710_valida", "_mh710_neutro",
                     "mh710_calcola", "mh710_sensitivita",
                     "mh710_csv", "mh710_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        assert "mh709" not in _helpers_src()
        assert "tab709" not in _helpers_src()
        assert "mh709" not in _ui_src()
        assert "tab709" not in _ui_src()

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w711_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE710) == 1

    def test_blocco_with_tab710(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab710:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE710

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st710_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 23, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st710_") for k in keys)

    def test_chiavi_st_input_sono_19(self):
        """Le 19 chiavi di input/bottone (18 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st710_[a-z0-9_]+)"', _ui_src())
        attese = ["st710_q_ciclo", "st710_cicli",
                  "st710_latente", "st710_rho",
                  "st710_dt", "st710_eta_pcm",
                  "st710_eta_acqua", "st710_p_carica",
                  "st710_opex_pcm", "st710_opex_acqua",
                  "st710_c_pcm", "st710_c_acqua",
                  "st710_fisso_pcm", "st710_fisso_acqua",
                  "st710_vita", "st710_wacc",
                  "st710_tolleranza", "st710_f_carica",
                  "st710_calcola"]
        assert len(attese) == 19
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg710" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg710") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg710")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Volume PCM (m3)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver710" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "stagionale" in src
        assert "solare termico" in src
        assert "latente" in src
        assert "sensibile" in src
        assert "volume" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "stagionale" in src.lower()
        assert "solare termico" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh710_csv" in src
        assert "accumulo_pcm_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh710_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento PCM" in src
        assert "Prezzo di carica" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st710_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W711 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab710:")
