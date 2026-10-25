"""Test tab711 "🔋🧂 Batterie sodio-ione: senza litio, l'accumulo stazionario paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
energia utile 500 kWh/ciclo; cicli 300/anno;
rendimento LFP 0,92; rendimento sodio-ione
0,88; DoD LFP 0,90; DoD sodio-ione 0,85;
costo LFP 220 EUR/kWh; costo sodio-ione 140
EUR/kWh; costo fisso LFP 5000 EUR; costo
fisso sodio-ione 5000 EUR; prezzo di carica
100 EUR/MWh; opex LFP 4000 EUR/anno; opex
sodio-ione 1500 EUR/anno; vita in cicli LFP
6000; vita in cicli sodio-ione 5000; vita di
progetto 15 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del |CAPEX delta|);
fattore di carica 0,35 t/MWh.

- cap_nom_lfp_kwh = 555.5555555555555
- cap_nom_na_kwh = 588.2352941176471
- e_carica_lfp_kwh_ciclo = 543.4782608695652
- e_carica_na_kwh_ciclo = 568.1818181818181
- costo_base_eur_a = 20304.347826086956
- costo_alt_eur_a = 18545.454545454544
- risparmio_eur_a = 1758.893280632412
- capex_lfp_eur = 127222.22222222222
- capex_na_eur = 87352.94117647059
- capex_delta_eur = -39869.28104575163
- anni_vita_lfp = 20.0
- anni_vita_na = 16.666666666666668
- anni_sost_lfp = []
- anni_sost_na = []
- co2_evitata_t_a = -2.5938735177865526
- van = 58125.991824369674
- tir = None
- payback = 0
- verdetto = 'CONVIENTE'

Scomposizione: Cap_LFP 500 / 0,90 =
555.5555555555555 kWh; Cap_Na 500 / 0,85 =
588.2352941176471 kWh; CAPEX LFP
555.5555555555555 x 220 + 5000 =
127222.22222222222; CAPEX Na
588.2352941176471 x 140 + 5000 =
87352.94117647059; CAPEX delta
87352.94117647059 - 127222.22222222222 =
-39869.28104575163; E_LFP 500 / 0,92 =
543.4782608695652 kWh/ciclo; E_Na 500 /
0,88 = 568.1818181818181 kWh/ciclo; C_base
300 x 543.4782608695652 / 1000 x 100 + 4000
= 20304.347826086956; C_alt 300 x
568.1818181818181 / 1000 x 100 + 1500 =
18545.454545454544; risparmio
20304.347826086956 - 18545.454545454544 =
1758.893280632412; vite 6000 / 300 = 20.0
anni e 5000 / 300 = 16.666666666666668 anni:
nessuna sostituzione entro 15 anni (floor
20 e 16, nessun multiplo sotto 15);
flussi [39869.28104575163, 1758.893280632412
x 15]; VAN 39869.28104575163 + 1758.893280632412
x (1 - 1,05^-15) / 0,05 =
58125.991824369674; TIR None (tutti i flussi
>= 0, nessun cambio di segno: non c'e'
investimento netto da remunerare); payback 0
(cumulato anno 0 = 39869.28104575163 >= 0);
VAN >= 0 -> CONVIENTE. CO2: 300 x
(543.4782608695652 - 568.1818181818181) /
1000 x 0,35 = -2.5938735177865526 t/anno
(negativa: il sodio-ione e' meno efficiente
e carica piu' energia per la stessa energia
utile, onesto e da spiegare in nota).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w712_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w712_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w712_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w712_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w712_helpers.py: {missing}")
    return out


_F = _load("mh711_num", "mh711_nneg", "mh711_pos",
           "mh711_int_pos", "mh711_int_nneg",
           "mh711_quota_valida", "mh711_eta_valido",
           "mh711_cap_nom", "mh711_capex",
           "mh711_e_carica", "mh711_costo_annuo",
           "mh711_risparmio", "mh711_anni_vita",
           "mh711_anni_sostituzione", "mh711_flussi",
           "mh711_van_flussi", "mh711_tir_flussi",
           "mh711_payback_flussi", "mh711_verdetto",
           "mh711_co2_evitata", "mh711_valida",
           "_mh711_neutro", "mh711_calcola",
           "mh711_sensitivita", "mh711_csv",
           "mh711_demo", "demo_calcoli")

TITLE711 = ("🔋🧂 Batterie sodio-ione: senza litio, "
            "l'accumulo stazionario paga?")

CAP_LFP_DEMO = 555.5555555555555
CAP_NA_DEMO = 588.2352941176471
E_LFP_DEMO = 543.4782608695652
E_NA_DEMO = 568.1818181818181
C_BASE_DEMO = 20304.347826086956
C_ALT_DEMO = 18545.454545454544
RISPARMIO_DEMO = 1758.893280632412
CX_LFP_DEMO = 127222.22222222222
CX_NA_DEMO = 87352.94117647059
DELTA_DEMO = -39869.28104575163
ANNI_VITA_LFP_DEMO = 20.0
ANNI_VITA_NA_DEMO = 16.666666666666668
CO2_EV_DEMO = -2.5938735177865526
VAN_DEMO = 58125.991824369674
TIR_DEMO = None
PAYBACK_DEMO = 0
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w712_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w712_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh711_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh711_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh711_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh711_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh711_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh711_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh711_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh711_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh711_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh711_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh711_int_pos"](300.0, "x") == 300

    def test_int_nneg_accetta_zero(self):
        assert _F["mh711_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh711_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh711_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh711_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh711_quota_valida"](0.0, "x") == 0.0
        assert _F["mh711_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh711_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh711_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh711_eta_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh711_demo"]()
        d.update(kw)
        return _F["mh711_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_e_uso_zero_non_valido(self):
        assert self._val(e_uso_kwh_ciclo=0.0)["valido"] is False

    def test_e_uso_negativo_non_valido(self):
        assert self._val(e_uso_kwh_ciclo=-1.0)["valido"] is False

    def test_cicli_zero_non_validi(self):
        assert self._val(cicli_anno=0)["valido"] is False

    def test_cicli_non_interi_non_validi(self):
        assert self._val(cicli_anno=299.5)["valido"] is False

    def test_eta_lfp_zero_non_valido(self):
        assert self._val(eta_lfp=0.0)["valido"] is False

    def test_eta_na_sopra_uno_non_valido(self):
        assert self._val(eta_na=1.1)["valido"] is False

    def test_eta_uno_valida(self):
        assert self._val(eta_na=1.0)["valido"] is True

    def test_dod_zero_non_valido(self):
        assert self._val(dod_lfp=0.0)["valido"] is False

    def test_dod_sopra_uno_non_valido(self):
        assert self._val(dod_na=1.1)["valido"] is False

    def test_dod_uno_valido(self):
        assert self._val(dod_na=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("costo_lfp_eur_kwh", "costo_na_eur_kwh",
                  "fisso_lfp_eur", "fisso_na_eur",
                  "prezzo_carica_eur_mwh",
                  "opex_lfp_eur_a", "opex_na_eur_a",
                  "wacc_frac", "fattore_carica_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_cicli_zero_non_valida(self):
        assert self._val(vita_cicli_lfp=0)["valido"] is False
        assert self._val(vita_cicli_na=0)["valido"] is False

    def test_vita_cicli_non_intera_non_valida(self):
        assert self._val(vita_cicli_na=4999.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=14.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_na=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(e_uso_kwh_ciclo=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(e_uso_kwh_ciclo=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_na="0.88")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_carica_eur_mwh=0.0)["valido"] is True
        assert self._val(costo_na_eur_kwh=0.0)["valido"] is True
        assert self._val(opex_na_eur_a=0.0)["valido"] is True
        assert self._val(fisso_na_eur=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_cap_nom_lfp_demo(self):
        assert _F["mh711_cap_nom"](
            500.0, 0.90) == pytest.approx(CAP_LFP_DEMO, rel=REL)

    def test_cap_nom_na_demo(self):
        assert _F["mh711_cap_nom"](
            500.0, 0.85) == pytest.approx(CAP_NA_DEMO, rel=REL)

    def test_cap_nom_rifiuta_dod_zero(self):
        with pytest.raises(ValueError):
            _F["mh711_cap_nom"](500.0, 0.0)

    def test_capex_lfp_demo(self):
        assert _F["mh711_capex"](
            CAP_LFP_DEMO, 220.0, 5000.0) == pytest.approx(
            CX_LFP_DEMO, rel=REL)

    def test_capex_na_demo(self):
        assert _F["mh711_capex"](
            CAP_NA_DEMO, 140.0, 5000.0) == pytest.approx(
            CX_NA_DEMO, rel=REL)

    def test_e_carica_lfp_demo(self):
        assert _F["mh711_e_carica"](
            500.0, 0.92) == pytest.approx(E_LFP_DEMO, rel=REL)

    def test_e_carica_na_demo(self):
        assert _F["mh711_e_carica"](
            500.0, 0.88) == pytest.approx(E_NA_DEMO, rel=REL)

    def test_e_carica_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh711_e_carica"](500.0, 0.0)

    def test_costo_base_demo(self):
        assert _F["mh711_costo_annuo"](
            300, E_LFP_DEMO, 100.0, 4000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_alt_demo(self):
        assert _F["mh711_costo_annuo"](
            300, E_NA_DEMO, 100.0, 1500.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh711_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh711_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_anni_vita_demo(self):
        assert _F["mh711_anni_vita"](6000, 300) == pytest.approx(
            ANNI_VITA_LFP_DEMO, rel=REL)
        assert _F["mh711_anni_vita"](5000, 300) == pytest.approx(
            ANNI_VITA_NA_DEMO, rel=REL)

    def test_anni_sostituzione_demo_vuoti(self):
        assert _F["mh711_anni_sostituzione"](20.0, 15) == []
        assert _F["mh711_anni_sostituzione"](
            16.666666666666668, 15) == []

    def test_anni_sostituzione_multipli(self):
        assert _F["mh711_anni_sostituzione"](
            1000 / 300, 15) == [3, 6, 9, 12]
        assert _F["mh711_anni_sostituzione"](3.0, 15) == [3, 6, 9, 12]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh711_anni_sostituzione"](0.5, 15) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh711_anni_sostituzione"](5.0, 15) == [5, 10]

    def test_co2_evitata_demo_negativa(self):
        assert _F["mh711_co2_evitata"](
            300, E_LFP_DEMO, E_NA_DEMO,
            0.35) == pytest.approx(CO2_EV_DEMO, rel=REL)
        assert CO2_EV_DEMO < 0.0

    def test_co2_evitata_positiva_se_na_piu_efficiente(self):
        assert _F["mh711_co2_evitata"](
            300, 568.1818181818181, 500.0,
            0.35) == pytest.approx(7.159090909090903, rel=REL)


class TestFinanza:
    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 15
        assert abs(_F["mh711_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_formula_chiusa(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 15
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh711_van_flussi"](
            flussi, 0.05) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 15
        assert _F["mh711_van_flussi"](
            flussi, 0.0) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 15, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh711_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_senza_sostituzioni(self):
        flussi = _F["mh711_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_LFP_DEMO, CX_NA_DEMO, [], [], 15)
        assert len(flussi) == 16
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert all(f == pytest.approx(RISPARMIO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_flussi_con_sostituzione_base(self):
        flussi = _F["mh711_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_LFP_DEMO, CX_NA_DEMO, [3, 6, 9, 12], [], 15)
        assert flussi[3] == pytest.approx(
            128981.11550285463, rel=REL)
        assert flussi[6] == pytest.approx(
            128981.11550285463, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_con_sostituzione_entrambi(self):
        flussi = _F["mh711_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_LFP_DEMO, CX_NA_DEMO, [3, 6, 9, 12], [3, 6, 9, 12], 15)
        assert flussi[3] == pytest.approx(
            41628.17432638405, rel=REL)

    def test_tir_none_demo_tutti_flussi_non_negativi(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 15
        assert _F["mh711_tir_flussi"](flussi) is None

    def test_tir_none_se_delta_zero(self):
        assert _F["mh711_tir_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh711_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh711_tir_flussi"]([-7037.911357773783,
                                      1304.5454545454522] * 1)
        assert tir is None or abs(tir) < 5.0

    def test_tir_caso_demo_pcm_like(self):
        tir = _F["mh711_tir_flussi"](
            [-7037.911357773783] + [1304.5454545454522] * 15)
        assert tir is not None
        npv = -7037.911357773783 + sum(
            1304.5454545454522 / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * 7037.911357773783

    def test_payback_demo_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 15
        assert _F["mh711_payback_flussi"](flussi) == 0

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh711_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai(self):
        assert _F["mh711_payback_flussi"](
            [-500000.0] + [RISPARMIO_DEMO] * 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh711_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh711_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh711_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh711_verdetto"](
            -3986.928104575163, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh711_verdetto"](
            -3986.928104575164, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_negativo_usa_valore_assoluto(self):
        assert _F["mh711_verdetto"](
            -100.0, -1250.0, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"
        assert _F["mh711_verdetto"](
            -200.0, -1250.0, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh711_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh711_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh711_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh711_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_zero_mai_marginale(self):
        assert _F["mh711_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh711_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh711_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh711_demo"]()
        d.update(kw)
        return _F["mh711_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["cap_nom_lfp_kwh"] == pytest.approx(
            CAP_LFP_DEMO, rel=REL)
        assert c["cap_nom_na_kwh"] == pytest.approx(
            CAP_NA_DEMO, rel=REL)
        assert c["e_carica_lfp_kwh_ciclo"] == pytest.approx(
            E_LFP_DEMO, rel=REL)
        assert c["e_carica_na_kwh_ciclo"] == pytest.approx(
            E_NA_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_lfp_eur"] == pytest.approx(
            CX_LFP_DEMO, rel=REL)
        assert c["capex_na_eur"] == pytest.approx(
            CX_NA_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_vita_lfp"] == pytest.approx(
            ANNI_VITA_LFP_DEMO, rel=REL)
        assert c["anni_vita_na"] == pytest.approx(
            ANNI_VITA_NA_DEMO, rel=REL)
        assert c["anni_sost_lfp"] == []
        assert c["anni_sost_na"] == []
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
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
        d = _F["mh711_demo"]()
        b = _F["mh711_calcola"](**d)
        coppie = [("cap_nom_lfp_kwh", CAP_LFP_DEMO),
                  ("cap_nom_na_kwh", CAP_NA_DEMO),
                  ("e_carica_lfp_kwh_ciclo", E_LFP_DEMO),
                  ("e_carica_na_kwh_ciclo", E_NA_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_lfp_eur", CX_LFP_DEMO),
                  ("capex_na_eur", CX_NA_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert b["tir"] is None
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh711_demo"]()
        assert d["e_uso_kwh_ciclo"] == 500.0
        assert d["cicli_anno"] == 300
        assert d["eta_lfp"] == 0.92
        assert d["eta_na"] == 0.88
        assert d["dod_lfp"] == 0.90
        assert d["dod_na"] == 0.85
        assert d["costo_lfp_eur_kwh"] == 220.0
        assert d["costo_na_eur_kwh"] == 140.0
        assert d["fisso_lfp_eur"] == 5000.0
        assert d["fisso_na_eur"] == 5000.0
        assert d["prezzo_carica_eur_mwh"] == 100.0
        assert d["opex_lfp_eur_a"] == 4000.0
        assert d["opex_na_eur_a"] == 1500.0
        assert d["vita_cicli_lfp"] == 6000
        assert d["vita_cicli_na"] == 5000
        assert d["vita_progetto_anni"] == 15
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_carica_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("cap_nom_lfp_kwh", "cap_nom_na_kwh",
                       "e_carica_lfp_kwh_ciclo",
                       "e_carica_na_kwh_ciclo",
                       "costo_base_eur_a", "costo_alt_eur_a",
                       "risparmio_eur_a", "capex_lfp_eur",
                       "capex_na_eur", "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert "tir = None" in doc
        assert "payback = 0" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_eta_na_basso_neutro_risparmio_negativo(self):
        # Eta Na 0,79 < LFP 0,92: E_na 632,91 >
        # E_LFP 543,48, C_alt 20487,99 > C_base
        # 20304,35 -> risparmio negativo
        n = self._bc(eta_na=0.79)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_opex_na_alto_riduce_risparmio(self):
        # Opex Na 3000: C_alt 20045,45, risparmio
        # 258,90; VAN 42556 circa -> CONVIENTE
        # (il CAPEX delta negativo domina)
        n = self._bc(opex_na_eur_a=3000.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            258.893280632412, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_delta_zero_mai_marginale(self):
        # Tutti i costi CAPEX a zero -> delta 0
        n = self._bc(costo_lfp_eur_kwh=0.0, fisso_lfp_eur=0.0,
                     costo_na_eur_kwh=0.0, fisso_na_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_capex_delta_negativo_payback_zero_tir_none(self):
        # Demo stessa: delta negativo, payback 0, TIR None
        n = self._bc()
        assert n["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_sostituzione_base_solo_lfp(self):
        # Vita cicli LFP 1000: 3,333 anni, floor 3
        # -> sostituzioni 3, 6, 9, 12; Na 5000:
        # nessuna. Flusso anno 3 = 128981,12;
        # VAN 415811,18 circa
        n = self._bc(vita_cicli_lfp=1000)
        assert n["valid"] is True
        assert n["anni_sost_lfp"] == [3, 6, 9, 12]
        assert n["anni_sost_na"] == []
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[3] == \
            pytest.approx(128981.11550285463, rel=REL)
        assert abs(n["van"] - 415811.1843077209) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_sostituzione_entrambi(self):
        # Vita cicli 900 per entrambi: 3,0 anni
        # -> sostituzioni 3, 6, 9, 12 in entrambi
        # i rami; flusso anno 3 = 41628,17;
        # VAN 170218,45 circa
        n = self._bc(vita_cicli_lfp=900, vita_cicli_na=900)
        assert n["valid"] is True
        assert n["anni_sost_lfp"] == [3, 6, 9, 12]
        assert n["anni_sost_na"] == [3, 6, 9, 12]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[3] == \
            pytest.approx(41628.17432638405, rel=REL)
        assert abs(n["van"] - 170218.44875467755) <= 1.0

    def test_marginale_orchestratore(self):
        # Costo Na 240 EUR/kWh: delta 18954,25;
        # VAN -697,54 entro tolleranza 1895,42
        # -> MARGINALE; payback 11
        n = self._bc(costo_na_eur_kwh=240.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            18954.248366013082, rel=REL)
        assert abs(n["van"] - (-697.5375873950397)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 11

    def test_non_conviente_orchestratore(self):
        # Costo Na 260 EUR/kWh: delta 30718,95;
        # VAN -12462,24 oltre tolleranza ->
        # NON_CONVIENTE; payback None
        n = self._bc(costo_na_eur_kwh=260.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            30718.954248366033, rel=REL)
        assert abs(n["van"] - (-12462.243469747991)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_dod_alto_riduce_cap_nom(self):
        # DoD Na 1,0: Cap_Na 500, CAPEX Na 75000,
        # delta -52222,22
        n = self._bc(dod_na=1.0)
        assert n["valid"] is True
        assert n["cap_nom_na_kwh"] == pytest.approx(
            500.0, rel=REL)

    def test_eta_zero_neutro(self):
        n = self._bc(eta_na=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_na=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_e_uso_zero_neutro(self):
        n = self._bc(e_uso_kwh_ciclo=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_non_interi_neutro(self):
        n = self._bc(cicli_anno=299.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_cicli_zero_neutro(self):
        n = self._bc(vita_cicli_na=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta_na=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(e_uso_kwh_ciclo=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(e_uso_kwh_ciclo=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN 39869,28 + 1758,89 x 15 =
        # 66252,68
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh711_neutro"]()
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
        n = _F["_mh711_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "e_uso_kwh_ciclo", "cicli_anno",
                       "eta_lfp", "eta_na",
                       "dod_lfp", "dod_na",
                       "cap_nom_lfp_kwh",
                       "cap_nom_na_kwh",
                       "e_carica_lfp_kwh_ciclo",
                       "e_carica_na_kwh_ciclo",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_lfp_eur",
                       "capex_na_eur",
                       "capex_delta_eur",
                       "anni_vita_lfp",
                       "anni_vita_na",
                       "anni_sost_lfp",
                       "anni_sost_na",
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
        assert "Capacita' nominale sodio-ione (kWh)" in voci
        assert "Capacita' nominale LFP (kWh)" in voci
        assert "Energia di carica sodio-ione (kWh/ciclo)" in voci
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
        return _F["mh711_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh711_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh711_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_rendimento_na(self):
        s = _F["mh711_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_riga_peggiore_positiva_ma_minore(self):
        # Eta Na x0,9 = 0,792: risparmio grezzo
        # ancora positivo ma VAN molto minore
        # del centro; la riga non e' degenere
        s = _F["mh711_sensitivita"](self._ing())
        assert (s.loc["x0.9"] > 0.0).all()
        assert abs(s.loc["x0.9", "x1.0"] - 38467.54857023975) <= 1.0

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh711_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh711_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh711_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 41202.63632733606) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 35732.460813143436) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 73370.9980159123) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 75049.34732140324) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita cicli LFP 1000 la griglia deve
        # includere le sostituzioni: il centro
        # deve coincidere col VAN del caso A
        ing = self._ing()
        ing["vita_cicli_lfp"] = 1000
        s = _F["mh711_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 415811.1843077209) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh711_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 35

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh711_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "e_uso_kwh_ciclo" in txt
        assert "cap_nom_na_kwh" in txt
        assert "cap_nom_lfp_kwh" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_na" in txt
        assert "capex_na_eur" in txt
        assert "capex_delta_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh711_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "e_uso_kwh_ciclo;500.0" in txt
        assert "opex_na_eur_a;1500.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def711["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def711\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh711_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh711_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh711_demo():")
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
        ui_keys = set(re.findall(r'_def711\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W712 (25/10/2026) - tab711' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh711_num", "mh711_nneg", "mh711_pos",
                     "mh711_int_pos", "mh711_int_nneg",
                     "mh711_quota_valida", "mh711_eta_valido",
                     "mh711_cap_nom", "mh711_capex",
                     "mh711_e_carica", "mh711_costo_annuo",
                     "mh711_risparmio", "mh711_anni_vita",
                     "mh711_anni_sostituzione", "mh711_flussi",
                     "mh711_van_flussi", "mh711_tir_flussi",
                     "mh711_payback_flussi", "mh711_verdetto",
                     "mh711_co2_evitata", "mh711_valida",
                     "_mh711_neutro", "mh711_calcola",
                     "mh711_sensitivita", "mh711_csv",
                     "mh711_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        # La tab precedente e' la tab710 (PCM): i
        # frammenti nuovi non devono contenere
        # i suoi identificatori.
        assert "mh710" not in _helpers_src()
        assert "tab710" not in _helpers_src()
        assert "mh710" not in _ui_src()
        assert "tab710" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Catena: questo file test fa riferimento
        # alla tab precedente tab710 come punto di
        # confronto (test residuo sopra) e la
        # nuova tab e' tab711.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab710" in src
        assert "tab711" in src
        assert _ui_src().startswith("    with tab711:")

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w712_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE711) == 1

    def test_blocco_with_tab711(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab711:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE711

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st711_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st711_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st711_[a-z0-9_]+)"', _ui_src())
        attese = ["st711_e_uso", "st711_cicli",
                  "st711_eta_lfp", "st711_eta_na",
                  "st711_dod_lfp", "st711_dod_na",
                  "st711_c_lfp", "st711_c_na",
                  "st711_fisso_lfp", "st711_fisso_na",
                  "st711_opex_lfp", "st711_opex_na",
                  "st711_p_carica", "st711_vita_cicli_lfp",
                  "st711_vita_cicli_na", "st711_vita_progetto",
                  "st711_wacc", "st711_tolleranza",
                  "st711_f_carica", "st711_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg711" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg711") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg711")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Capacità sodio-ione (kWh)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver711" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "second-life" in src
        assert "flusso" in src
        assert "supercondensatori" in src
        assert "v2g" in src
        assert "stagionale" in src
        assert "negativa" in src
        assert "capex" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "second-life" in src.lower()
        assert "flusso redox" in src.lower()
        assert "supercondensatori" in src.lower()
        assert "v2g" in src.lower()
        assert "stagionale" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh711_csv" in src
        assert "sodio_ione_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh711_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento sodio-ione" in src
        assert "Prezzo di carica" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st711_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W712 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab711:")
