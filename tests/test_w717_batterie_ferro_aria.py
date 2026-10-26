"""Test tab717 "🔋⚙️ Batterie ferro-aria: l'accumulo multi-giorno paga?"

Tab precedente tab716 (gradiente salino, w717);
nuova tab tab717 (ferro-aria, w718). La tab717
replica ESATTAMENTE la semantica economica
della tab711 (sodio-ione), adattata alla
chimica ferro-aria vs LFP: due rami che
erogano la STESSA energia utile per ciclo,
stessi cicli/anno, carica a prezzo di
mercato.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
energia utile 500 kWh/ciclo; cicli 150/anno;
rendimento LFP 0,92; rendimento ferro-aria
0,55; DoD LFP 0,90; DoD ferro-aria 0,95;
costo LFP 220 EUR/kWh; costo ferro-aria 60
EUR/kWh; costo fisso 5000 EUR per entrambi
i rami; prezzo di carica 20 EUR/MWh; opex
LFP 3000 EUR/anno; opex ferro-aria 1000
EUR/anno; vita in cicli LFP 6000; vita in
cicli ferro-aria 10000; vita di progetto 20
anni; WACC 0,05 (5 %); tolleranza 0,10 (10 %
del |CAPEX_delta|); fattore di carica
0,35 t/MWh.

- cap_nom_lfp_kwh = 555.5555555555555
- cap_nom_fe_kwh = 526.3157894736843
- e_carica_lfp_kwh_ciclo = 543.4782608695652
- e_carica_fe_kwh_ciclo = 909.090909090909
- costo_base_eur_a = 4630.434782608696
- costo_alt_eur_a = 3727.272727272727
- risparmio_eur_a = 903.162055335969
- capex_lfp_eur = 127222.22222222222
- capex_fe_eur = 36578.94736842105
- capex_delta_eur = -90643.27485380117
- anni_vita_lfp = 40.0
- anni_vita_fe = 66.66666666666667
- anni_sost_lfp = []
- anni_sost_fe = []
- co2_evitata_t_a = -19.194664031620547
- van = 101898.67036079873
- tir = None
- payback = 0
- verdetto = 'CONVIENTE'

Scomposizione: Cap_LFP 500 / 0,90 =
555.5555555555555 kWh; Cap_Fe 500 / 0,95 =
526.3157894736843 kWh; E_carica_LFP 500 /
0,92 = 543.4782608695652 kWh/ciclo;
E_carica_Fe 500 / 0,55 = 909.090909090909
kWh/ciclo; C_base 150 x 543.4782608695652 /
1000 x 20 + 3000 = 4630.434782608696
EUR/anno; C_alt 150 x 909.090909090909 /
1000 x 20 + 1000 = 3727.272727272727
EUR/anno; risparmio 4630.434782608696 -
3727.272727272727 = 903.162055335969
EUR/anno (positivo ma piccolo: l'opex
risparmiato, 2000 EUR/anno, supera di poco
il maggior costo di carica, 1096,84
EUR/anno); CAPEX_LFP 555.5555555555555 x
220 + 5000 = 127222.22222222222 EUR;
CAPEX_Fe 526.3157894736843 x 60 + 5000 =
36578.94736842105 EUR; CAPEX_delta
36578.94736842105 - 127222.22222222222 =
-90643.27485380117 EUR (NEGATIVO, non
clampato: il ferro-aria costa meno
dell'LFP gia' all'anno 0); anni di vita
6000 / 150 = 40,0 e 10000 / 150 =
66.66666666666667: floor 40 e 66, entrambi
>= 20, quindi NESSUNA sostituzione entro
la vita di progetto; flussi [90643.27485380117
all'anno 0 (cioe' -CAPEX_delta), poi
903.162055335969 EUR/anno per 20 anni];
VAN 101898.67036079873 a WACC 5 % su 20
anni; TIR None (tutti i flussi >= 0:
nessun tasso azzera un VAN sempre
positivo); payback 0 (il cumulato
all'anno 0 e' gia' >= 0); CO2 150 x
(543.4782608695652 - 909.090909090909) /
1000 x 0,35 = -19.194664031620547 t/anno
(NEGATIVA e INFORMATIVA: il ferro-aria,
meno efficiente, carica piu' energia a
parita' di energia utile); VAN >= 0 ->
CONVIENTE.

Formula flussi negli anni di sostituzione
(ESATTA della tab711, copiata): flusso_0 =
-CAPEX_delta; flusso_t (t >= 1) = risparmio
- (CAPEX_Fe se t e' anno di sostituzione
Fe) + (CAPEX_LFP se t e' anno di
sostituzione LFP).
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
    if (p / "w718_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w718_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w718_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w718_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w718_helpers.py: {missing}")
    return out


_F = _load("mh717_num", "mh717_nneg", "mh717_pos",
           "mh717_int_pos", "mh717_int_nneg",
           "mh717_eta_valido", "mh717_cap_nom",
           "mh717_capex", "mh717_e_carica",
           "mh717_costo_annuo", "mh717_risparmio",
           "mh717_anni_vita", "mh717_anni_sostituzione",
           "mh717_flussi", "mh717_van_flussi",
           "mh717_tir_flussi", "mh717_payback_flussi",
           "mh717_verdetto", "mh717_co2_evitata",
           "mh717_valida", "_mh717_neutro",
           "mh717_calcola", "mh717_sensitivita",
           "mh717_csv", "mh717_demo", "demo_calcoli")

TITLE717 = ("🔋⚙️ Batterie ferro-aria: "
            "l'accumulo multi-giorno paga?")

CAP_LFP_DEMO = 555.5555555555555
CAP_FE_DEMO = 526.3157894736843
E_LFP_DEMO = 543.4782608695652
E_FE_DEMO = 909.090909090909
C_BASE_DEMO = 4630.434782608696
C_ALT_DEMO = 3727.272727272727
RISPARMIO_DEMO = 903.162055335969
CAPEX_LFP_DEMO = 127222.22222222222
CAPEX_FE_DEMO = 36578.94736842105
DELTA_DEMO = -90643.27485380117
ANNI_VITA_LFP_DEMO = 40.0
ANNI_VITA_FE_DEMO = 66.66666666666667
CO2_DEMO = -19.194664031620547
VAN_DEMO = 101898.67036079873
PAYBACK_DEMO = 0
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w718_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w718_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh717_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh717_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh717_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh717_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh717_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh717_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh717_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh717_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh717_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh717_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh717_int_pos"](150.0, "x") == 150

    def test_int_nneg_accetta_zero(self):
        assert _F["mh717_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh717_int_nneg"](-1, "x")

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh717_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh717_eta_valido"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh717_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_valore_interno(self):
        assert _F["mh717_eta_valido"](0.55, "x") == 0.55


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh717_demo"]()
        d.update(kw)
        return _F["mh717_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_e_uso_zero_non_valida(self):
        assert self._val(e_uso_kwh_ciclo=0.0)["valido"] is False

    def test_e_uso_negativa_non_valida(self):
        assert self._val(e_uso_kwh_ciclo=-1.0)["valido"] is False

    def test_cicli_zero_non_validi(self):
        assert self._val(cicli_anno=0)["valido"] is False

    def test_cicli_non_interi_non_validi(self):
        assert self._val(cicli_anno=150.5)["valido"] is False

    def test_rendimenti_fuori_intervallo_non_validi(self):
        assert self._val(eta_lfp=0.0)["valido"] is False
        assert self._val(eta_lfp=1.2)["valido"] is False
        assert self._val(eta_fe=0.0)["valido"] is False
        assert self._val(eta_fe=1.2)["valido"] is False

    def test_dod_fuori_intervallo_non_validi(self):
        assert self._val(dod_lfp=0.0)["valido"] is False
        assert self._val(dod_lfp=1.2)["valido"] is False
        assert self._val(dod_fe=0.0)["valido"] is False
        assert self._val(dod_fe=1.2)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("costo_lfp_eur_kwh", "costo_fe_eur_kwh",
                  "fisso_lfp_eur", "fisso_fe_eur",
                  "prezzo_carica_eur_mwh", "opex_lfp_eur_a",
                  "opex_fe_eur_a", "wacc_frac",
                  "tolleranza_frac", "fattore_carica_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_cicli_zero_non_valida(self):
        assert self._val(vita_cicli_lfp=0)["valido"] is False
        assert self._val(vita_cicli_fe=0)["valido"] is False

    def test_vita_cicli_non_intera_non_valida(self):
        assert self._val(vita_cicli_lfp=6000.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=19.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        # Brief tab717: tol >= 0 senza tetto
        # superiore (come la tab precedente).
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_fe=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(e_uso_kwh_ciclo=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(cicli_anno=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_fe="0.55")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(costo_fe_eur_kwh=0.0)["valido"] is True
        assert self._val(fisso_fe_eur=0.0)["valido"] is True
        assert self._val(prezzo_carica_eur_mwh=0.0)["valido"] is True
        assert self._val(opex_fe_eur_a=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_carica_t_mwh=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_cap_nom_demo(self):
        assert _F["mh717_cap_nom"](
            500.0, 0.90) == pytest.approx(CAP_LFP_DEMO, rel=REL)
        assert _F["mh717_cap_nom"](
            500.0, 0.95) == pytest.approx(CAP_FE_DEMO, rel=REL)

    def test_cap_nom_cresce_con_dod_basso(self):
        assert _F["mh717_cap_nom"](
            500.0, 0.50) == pytest.approx(1000.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh717_capex"](
            CAP_LFP_DEMO, 220.0, 5000.0) == pytest.approx(
            CAPEX_LFP_DEMO, rel=REL)
        assert _F["mh717_capex"](
            CAP_FE_DEMO, 60.0, 5000.0) == pytest.approx(
            CAPEX_FE_DEMO, rel=REL)

    def test_capex_delta_demo_negativo_non_clampato(self):
        delta = _F["mh717_capex"](
            CAP_FE_DEMO, 60.0, 5000.0) - _F["mh717_capex"](
            CAP_LFP_DEMO, 220.0, 5000.0)
        assert delta == pytest.approx(DELTA_DEMO, rel=REL)
        assert delta < 0.0

    def test_e_carica_demo(self):
        assert _F["mh717_e_carica"](
            500.0, 0.92) == pytest.approx(E_LFP_DEMO, rel=REL)
        assert _F["mh717_e_carica"](
            500.0, 0.55) == pytest.approx(E_FE_DEMO, rel=REL)

    def test_e_carica_cresce_con_rendimento_basso(self):
        assert _F["mh717_e_carica"](
            500.0, 0.55) > _F["mh717_e_carica"](500.0, 0.92)

    def test_costo_annuo_demo(self):
        assert _F["mh717_costo_annuo"](
            150, E_LFP_DEMO, 20.0, 3000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert _F["mh717_costo_annuo"](
            150, E_FE_DEMO, 20.0, 1000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh717_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh717_risparmio"](
            10000.0, 15000.0) == pytest.approx(-5000.0, rel=REL)

    def test_anni_vita_demo(self):
        assert _F["mh717_anni_vita"](
            6000, 150) == pytest.approx(ANNI_VITA_LFP_DEMO, rel=REL)
        assert _F["mh717_anni_vita"](
            10000, 150) == pytest.approx(ANNI_VITA_FE_DEMO, rel=REL)

    def test_anni_sostituzione_demo_vuoti(self):
        assert _F["mh717_anni_sostituzione"](40.0, 20) == []
        assert _F["mh717_anni_sostituzione"](
            66.66666666666667, 20) == []

    def test_anni_sostituzione_multipli(self):
        assert _F["mh717_anni_sostituzione"](10.0, 20) == [10]
        assert _F["mh717_anni_sostituzione"](5.0, 20) == [5, 10, 15]

    def test_anni_sostituzione_floor_non_intero(self):
        # Vita 10,5 anni -> floor 10: anno 10.
        assert _F["mh717_anni_sostituzione"](10.5, 20) == [10]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh717_anni_sostituzione"](0.5, 20) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh717_anni_sostituzione"](20.0, 20) == []
        assert _F["mh717_anni_sostituzione"](10.0, 20) == [10]

    def test_co2_evitata_demo_negativa(self):
        assert _F["mh717_co2_evitata"](
            150, E_LFP_DEMO, E_FE_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)
        assert CO2_DEMO < 0.0

    def test_co2_evitata_puo_essere_positiva(self):
        assert _F["mh717_co2_evitata"](
            100, 600.0, 500.0, 0.5) == pytest.approx(5.0, rel=REL)

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh717_co2_evitata"](
            150, E_LFP_DEMO, E_FE_DEMO, 0.0) == pytest.approx(
            0.0, abs=1e-9)

    def test_co2_evitata_zero_se_energie_uguali(self):
        assert _F["mh717_co2_evitata"](
            150, 500.0, 500.0, 0.35) == pytest.approx(
            0.0, abs=1e-9)


class TestFinanza:
    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        assert abs(_F["mh717_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * 20
        assert _F["mh717_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh717_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_senza_sostituzioni(self):
        flussi = _F["mh717_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_LFP_DEMO, CAPEX_FE_DEMO, [], [], 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_tab711_sostituzione_fe(self):
        # Formula ESATTA tab711: anno di
        # sostituzione Fe -> risparmio - CAPEX_Fe.
        flussi = _F["mh717_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_LFP_DEMO, CAPEX_FE_DEMO, [], [10], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_FE_DEMO, rel=REL)
        assert flussi[9] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_tab711_sostituzione_lfp(self):
        # Formula ESATTA tab711: anno di
        # sostituzione LFP -> risparmio + CAPEX_LFP.
        flussi = _F["mh717_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_LFP_DEMO, CAPEX_FE_DEMO, [10], [], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_LFP_DEMO, rel=REL)

    def test_flussi_formula_tab711_sostituzione_entrambi(self):
        # Stesso anno per entrambi i rami: i due
        # termini si sommano.
        flussi = _F["mh717_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_LFP_DEMO, CAPEX_FE_DEMO, [10], [10], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_FE_DEMO + CAPEX_LFP_DEMO,
            rel=REL)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh717_tir_flussi"](
            [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh717_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        assert _F["mh717_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh717_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4

    def test_payback_none_se_mai(self):
        assert _F["mh717_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 20) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh717_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh717_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh717_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh717_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh717_verdetto"](
            -0.10 * abs(DELTA_DEMO), DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh717_verdetto"](
            -0.10 * abs(DELTA_DEMO) - 1.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh717_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh717_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh717_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh717_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh717_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_accetta_tolleranza_sopra_uno(self):
        assert _F["mh717_verdetto"](
            -100.0, DELTA_DEMO, 1.5,
            RISPARMIO_DEMO) == "MARGINALE"


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh717_demo"]()
        d.update(kw)
        return _F["mh717_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["cap_nom_lfp_kwh"] == pytest.approx(
            CAP_LFP_DEMO, rel=REL)
        assert c["cap_nom_fe_kwh"] == pytest.approx(
            CAP_FE_DEMO, rel=REL)
        assert c["e_carica_lfp_kwh_ciclo"] == pytest.approx(
            E_LFP_DEMO, rel=REL)
        assert c["e_carica_fe_kwh_ciclo"] == pytest.approx(
            E_FE_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_lfp_eur"] == pytest.approx(
            CAPEX_LFP_DEMO, rel=REL)
        assert c["capex_fe_eur"] == pytest.approx(
            CAPEX_FE_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_vita_lfp"] == pytest.approx(
            ANNI_VITA_LFP_DEMO, rel=REL)
        assert c["anni_vita_fe"] == pytest.approx(
            ANNI_VITA_FE_DEMO, rel=REL)
        assert c["anni_sost_lfp"] == []
        assert c["anni_sost_fe"] == []
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] is None
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh717_demo"]()
        b = _F["mh717_calcola"](**d)
        coppie = [("cap_nom_lfp_kwh", CAP_LFP_DEMO),
                  ("cap_nom_fe_kwh", CAP_FE_DEMO),
                  ("e_carica_lfp_kwh_ciclo", E_LFP_DEMO),
                  ("e_carica_fe_kwh_ciclo", E_FE_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_lfp_eur", CAPEX_LFP_DEMO),
                  ("capex_fe_eur", CAPEX_FE_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sost_lfp"] == []
        assert b["anni_sost_fe"] == []
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert b["tir"] is None
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh717_demo"]()
        assert d["e_uso_kwh_ciclo"] == 500.0
        assert d["cicli_anno"] == 150
        assert d["eta_lfp"] == 0.92
        assert d["eta_fe"] == 0.55
        assert d["dod_lfp"] == 0.90
        assert d["dod_fe"] == 0.95
        assert d["costo_lfp_eur_kwh"] == 220.0
        assert d["costo_fe_eur_kwh"] == 60.0
        assert d["fisso_lfp_eur"] == 5000.0
        assert d["fisso_fe_eur"] == 5000.0
        assert d["prezzo_carica_eur_mwh"] == 20.0
        assert d["opex_lfp_eur_a"] == 3000.0
        assert d["opex_fe_eur_a"] == 1000.0
        assert d["vita_cicli_lfp"] == 6000
        assert d["vita_cicli_fe"] == 10000
        assert d["vita_progetto_anni"] == 20
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_carica_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("cap_nom_lfp_kwh",
                       "cap_nom_fe_kwh",
                       "e_carica_lfp_kwh_ciclo",
                       "e_carica_fe_kwh_ciclo",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_lfp_eur",
                       "capex_fe_eur",
                       "capex_delta_eur",
                       "anni_vita_lfp",
                       "anni_vita_fe",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sost_lfp"]) in doc
        assert repr(c["anni_sost_fe"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 0" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_carica_zero_risparmio_opex(self):
        # Prezzo 0: il costo di carica sparisce,
        # resta solo la differenza opex: risparmio
        # 3000 - 1000 = 2000 EUR/anno.
        n = self._bc(prezzo_carica_eur_mwh=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            2000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_prezzo_carica_alto_risparmio_negativo(self):
        # Prezzo 200 EUR/MWh: C_base 19304,35
        # < C_alt 28272,73 -> risparmio negativo
        # -> dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_carica_eur_mwh=200.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_costo_fe_alto_non_conviente(self):
        # Costo ferro-aria 400 EUR/kWh: CAPEX_delta
        # 88304,09, VAN -77048,70, TIR -11,92 %,
        # payback None -> NON_CONVIENTE.
        n = self._bc(costo_fe_eur_kwh=400.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            88304.09356725149, rel=REL)
        assert abs(n["van"] - (-77048.69806025393)) <= 1.0
        assert abs(n["tir"] - (-11.916757229234749)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_fe_marginale(self):
        # Costo ferro-aria 255,5 EUR/kWh: CAPEX_delta
        # 12251,46, VAN -996,07 entro la tolleranza
        # 1225,15 -> MARGINALE.
        n = self._bc(costo_fe_eur_kwh=255.5)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            12251.461988304101, rel=REL)
        assert abs(n["van"] - (-996.0664813065209)) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_vite_corte_sostituzione_lfp(self):
        # Vita LFP 1500 cicli (10 anni), Fe 3000
        # (20 anni): sost LFP [10], Fe []; flusso
        # anno 10 = risparmio + CAPEX_LFP; VAN
        # 180002,08 -> CONVIENTE, payback 0.
        n = self._bc(vita_cicli_lfp=1500, vita_cicli_fe=3000)
        assert n["valid"] is True
        assert n["anni_sost_lfp"] == [10]
        assert n["anni_sost_fe"] == []
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(128125.38427755819, rel=REL)
        assert abs(n["van"] - 180002.07872792863) <= 1.0
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_vite_invertite_sostituzione_fe(self):
        # Vita LFP 3000 cicli (20 anni), Fe 1500
        # (10 anni): sost Fe [10]; flusso anno
        # 10 = risparmio - CAPEX_Fe; VAN
        # 79442,37 -> CONVIENTE, payback 0.
        n = self._bc(vita_cicli_lfp=3000, vita_cicli_fe=1500)
        assert n["valid"] is True
        assert n["anni_sost_lfp"] == []
        assert n["anni_sost_fe"] == [10]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-35675.785313085085, rel=REL)
        assert abs(n["van"] - 79442.36977075518) <= 1.0
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_sostituzione_entrambi_stesso_anno(self):
        # Vita 1500 cicli per entrambi (10 anni):
        # sost [10] per entrambi; flusso anno 10
        # = risparmio - CAPEX_Fe + CAPEX_LFP.
        n = self._bc(vita_cicli_lfp=1500, vita_cicli_fe=1500)
        assert n["anni_sost_lfp"] == [10]
        assert n["anni_sost_fe"] == [10]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(91546.43690913713, rel=REL)
        assert abs(n["van"] - 157545.77813788506) <= 1.0

    def test_capex_delta_zero_mai_marginale(self):
        # Costi ferro-aria a 0 e fissi uguali non
        # azzerano il delta da soli: il caso
        # delta == 0 si verifica con costo Fe
        # tale che CAPEX_Fe == CAPEX_LFP; qui si
        # testa il verdetto a delta zero, non
        # l'orchestratore: vedi TestFinanza.
        n = self._bc(costo_fe_eur_kwh=0.0, fisso_fe_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] < 0.0
        assert n["verdetto"] == "CONVIENTE"

    def test_e_uso_zero_neutro(self):
        n = self._bc(e_uso_kwh_ciclo=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_sopra_uno_neutro(self):
        n = self._bc(eta_fe=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_cicli_zero_neutro(self):
        n = self._bc(vita_cicli_fe=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta_fe=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(e_uso_kwh_ciclo=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(cicli_anno=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # 90643,27 + 903,16 x 20 = 108706,52.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            108706.51596052053, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh717_neutro"]()
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
        n = _F["_mh717_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "e_uso_kwh_ciclo", "cicli_anno",
                       "eta_lfp", "eta_fe",
                       "dod_lfp", "dod_fe",
                       "cap_nom_lfp_kwh",
                       "cap_nom_fe_kwh",
                       "e_carica_lfp_kwh_ciclo",
                       "e_carica_fe_kwh_ciclo",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_lfp_eur",
                       "capex_fe_eur",
                       "capex_delta_eur",
                       "anni_vita_lfp",
                       "anni_vita_fe",
                       "anni_sost_lfp",
                       "anni_sost_fe",
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
        assert len(b["df_tabella"]) == 30
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Capacita' nominale ferro-aria (kWh)" in voci
        assert "Energia di carica ferro-aria (kWh/ciclo)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX ferro-aria (EUR)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "Anni di vita ferro-aria" in voci
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


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh717_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh717_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh717_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_rendimento_fe(self):
        s = _F["mh717_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_carica(self):
        # Il ferro-aria carica piu' energia:
        # un prezzo piu' alto riduce il risparmio.
        s = _F["mh717_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh717_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh717_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh717_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 99866.78823973244) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 96377.69772881054) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 106046.39667404979) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 103930.55248186504) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita LFP 1500 cicli la griglia
        # deve includere la sostituzione anno
        # 10: il centro deve coincidere col VAN
        # del caso con vita LFP 1500 cicli.
        ing = self._ing()
        ing["vita_cicli_lfp"] = 1500
        s = _F["mh717_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 180002.07872792863) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh717_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 34

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh717_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "e_uso_kwh_ciclo" in txt
        assert "cap_nom_fe_kwh" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_fe" in txt
        assert "capex_delta_eur" in txt
        assert "dod_fe" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh717_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "e_uso_kwh_ciclo;500.0" in txt
        assert "opex_lfp_eur_a;3000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def717["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def717\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh717_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh717_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh717_demo():")
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
        ui_keys = set(re.findall(r'_def717\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W718 (26/10/2026) - tab717' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh717_num", "mh717_nneg", "mh717_pos",
                     "mh717_int_pos", "mh717_int_nneg",
                     "mh717_eta_valido", "mh717_cap_nom",
                     "mh717_capex", "mh717_e_carica",
                     "mh717_costo_annuo", "mh717_risparmio",
                     "mh717_anni_vita", "mh717_anni_sostituzione",
                     "mh717_flussi", "mh717_van_flussi",
                     "mh717_tir_flussi", "mh717_payback_flussi",
                     "mh717_verdetto", "mh717_co2_evitata",
                     "mh717_valida", "_mh717_neutro",
                     "mh717_calcola", "mh717_sensitivita",
                     "mh717_csv", "mh717_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        # I frammenti nuovi usano solo mh717 /
        # tab717 / st717: nessun identificatore
        # della numerazione successiva.
        assert "mh718" not in _helpers_src()
        assert "mh718" not in _ui_src()
        assert "st718" not in _ui_src()
        assert "tab718" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab716 (gradiente salino)
        # come punto di confronto (regressione
        # tab675) e la nuova tab e' tab717.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab716" in src
        assert "tab717" in src
        assert _ui_src().startswith("    with tab717:")

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w718_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE717) == 1

    def test_blocco_with_tab717(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab717:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE717

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st717_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st717_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st717_[a-z0-9_]+)"', _ui_src())
        attese = ["st717_e_uso", "st717_cicli",
                  "st717_eta_lfp", "st717_eta_fe",
                  "st717_dod_lfp", "st717_dod_fe",
                  "st717_costo_lfp", "st717_costo_fe",
                  "st717_fisso_lfp", "st717_fisso_fe",
                  "st717_prezzo_carica", "st717_opex_lfp",
                  "st717_opex_fe", "st717_vita_cicli_lfp",
                  "st717_vita_cicli_fe", "st717_vita_progetto",
                  "st717_wacc", "st717_tolleranza",
                  "st717_f_carica", "st717_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg717" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg717") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg717")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Capacità nominale ferro-aria (kWh)" in src
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
        assert "basso costo" in src
        assert "cicli sono pochi" in src
        assert "non sull'efficienza" in src
        assert "informative" in src
        assert "negativa" in src
        assert "sodio-ione" in src
        assert "flusso redox" in src
        assert "second-life" in src
        assert "sabbia" in src
        assert "pcm" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline (LFP)" in src
        assert "Costo annuo alternativa (ferro-aria)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh717_csv" in src
        assert "ferro_aria_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh717_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento ferro-aria" in src
        assert "Prezzo di carica" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st717_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W718 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab717:")
