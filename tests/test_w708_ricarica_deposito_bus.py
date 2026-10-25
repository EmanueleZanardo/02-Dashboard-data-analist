"""Test tab708 "🚌🔌 Ricarica in deposito per bus elettrici: la gestione intelligente della potenza paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
flotta 40 bus; 180 kWh/giorno per bus; 300
giorni operativi; finestra notturna 8 h;
colonnina 60 kW; rendimento ricarica 0,92;
prezzo notte 0,12 EUR/kWh; prezzo giorno
0,28 EUR/kWh; onere di potenza 8 EUR/kW/mese;
allacciamento fisso 20000 EUR + 150 EUR/kW;
EMS 30000 EUR; opex EMS 5000 EUR/anno; vita
12 anni; WACC 0,05 (5 %); tolleranza 0,10
(10 % del |CAPEX delta|); 60000 km/bus/anno;
diesel 35 l/100km; fattore diesel 2,68 kg/l;
fattore elettrico 0,35 t/MWh.

- energia_giorno_rete_kwh = 7826.086956521739
- potenza_non_gestita_kw = 2400.0
- potenza_gestita_kw = 978.2608695652174
- picco_evitato_kw = 1421.7391304347825
- energia_annua_mwh_a = 2160.0
- costo_non_gestita_eur_a = 835200.0
- costo_gestita_eur_a = 358113.04347826086
- risparmio_eur_a = 477086.95652173914
- allaccio_non_gestita_eur = 380000.0
- allaccio_gestita_eur = 166739.1304347826
- capex_delta_eur = -183260.8695652174
- co2_diesel_t_a = 2251.2
- co2_elettrica_t_a = 756.0
- co2_evitata_t_a = 1495.1999999999998
- van = 4411802.617684906
- tir = None
- payback = 0
- verdetto = 'CONVIENTE'

Scomposizione: E_giorno 40 x 180 / 0,92 =
7826.086956521739; P_non_gestita 40 x 60 =
2400.0; P_gestita 7826.086956521739 / 8 =
978.2608695652174 (<= 2400.0: finestra
sufficiente); picco evitato 2400.0 -
978.2608695652174 = 1421.7391304347825;
E_annua 40 x 180 x 300 / 1000 = 2160.0 MWh
(2160000 kWh); C_non_gestita 2160000 x 0,28
+ 2400 x 8 x 12 = 604800 + 230400 =
835200.0; C_gestita 2160000 x 0,12 +
978.2608695652174 x 8 x 12 + 5000 =
259200 + 93913.04347826086 + 5000 =
358113.04347826086; risparmio 835200.0 -
358113.04347826086 = 477086.95652173914;
allaccio non gestita 20000 + 2400 x 150 =
380000.0; allaccio gestita 20000 +
978.2608695652174 x 150 = 166739.1304347826;
CAPEX delta (166739.1304347826 + 30000) -
380000.0 = -183260.8695652174 (NEGATIVO:
la gestita evita potenziamento di rete e
costa meno gia' all'anno 0, NON clampato
a zero); VAN -(-183260.8695652174) +
477086.95652173914 x (1 - 1,05^-12) / 0,05
= 4411802.617684906; TIR None per
costruzione (flusso anno 0 = +183260.87 >=
0, nessun cambio di segno: non c'e'
investimento netto da remunerare); payback 0
per costruzione (cumulato anno 0 gia' >= 0:
investimento gia' ripagato); VAN >= 0 ->
CONVIENTE. CO2: diesel 40 x 60000 x 35/100
x 2,68 / 1000 = 2251.2 t/anno; elettrica
2160.0 x 0,35 = 756.0; evitata 2251.2 -
756.0 = 1495.1999999999998 t/anno.
NOTA: la stima approssimativa del brief
(2246,4 t diesel) era leggermente bassa:
il calcolo esatto da' 2251,2 t (840000 l x
2,68 kg/l / 1000). I valori esatti
ricalcolati sono quelli sopra.
Artefatti float (valori arrotondati tra
parentesi): co2_evitata_t_a =
1495.1999999999998 (1495,2).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w709_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w709_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w709_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w709_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w709_helpers.py: {missing}")
    return out


_F = _load("mh708_num", "mh708_nneg", "mh708_pos",
           "mh708_int_pos", "mh708_int_nneg",
           "mh708_quota_valida", "mh708_eta_valido",
           "mh708_energia_giorno_rete",
           "mh708_potenza_non_gestita",
           "mh708_potenza_gestita",
           "mh708_energia_annua_mwh",
           "mh708_costo_non_gestita",
           "mh708_costo_gestita", "mh708_risparmio",
           "mh708_allaccio", "mh708_capex_delta",
           "mh708_co2_diesel", "mh708_co2_elettrica",
           "mh708_co2_evitata", "mh708_crf",
           "mh708_van", "mh708_tir", "mh708_payback",
           "mh708_verdetto", "mh708_valida",
           "_mh708_neutro", "mh708_calcola",
           "mh708_sensitivita", "mh708_csv",
           "mh708_demo", "demo_calcoli")

TITLE708 = ("🚌🔌 Ricarica in deposito per bus elettrici: "
            "la gestione intelligente della potenza paga?")

E_GIORNO_DEMO = 7826.086956521739
P_NG_DEMO = 2400.0
P_G_DEMO = 978.2608695652174
PICCO_DEMO = 1421.7391304347825
E_ANNUA_DEMO = 2160.0
C_NG_DEMO = 835200.0
C_G_DEMO = 358113.04347826086
RISPARMIO_DEMO = 477086.95652173914
A_NG_DEMO = 380000.0
A_G_DEMO = 166739.1304347826
DELTA_DEMO = -183260.8695652174
CO2_D_DEMO = 2251.2
CO2_E_DEMO = 756.0
CO2_EV_DEMO = 1495.1999999999998
VAN_DEMO = 4411802.617684906
TIR_DEMO = None
PAYBACK_DEMO = 0
VITA_DEMO = 12
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.11282541002081534

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w709_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w709_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh708_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh708_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh708_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh708_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh708_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh708_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh708_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh708_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh708_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh708_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh708_int_pos"](40.0, "x") == 40

    def test_int_nneg_accetta_zero(self):
        assert _F["mh708_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh708_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh708_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh708_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh708_quota_valida"](0.0, "x") == 0.0
        assert _F["mh708_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh708_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh708_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh708_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_demo(self):
        assert _F["mh708_eta_valido"](0.92, "x") == 0.92


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh708_demo"]()
        d.update(kw)
        return _F["mh708_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_n_bus_zero_non_valido(self):
        assert self._val(n_bus=0)["valido"] is False

    def test_n_bus_negativo_non_valido(self):
        assert self._val(n_bus=-1)["valido"] is False

    def test_n_bus_non_intero_non_valido(self):
        assert self._val(n_bus=40.5)["valido"] is False

    def test_e_bus_zero_non_valido(self):
        assert self._val(e_bus_kwh_giorno=0.0)["valido"] is False

    def test_giorni_zero_non_valido(self):
        assert self._val(giorni_a=0)["valido"] is False

    def test_giorni_non_interi_non_validi(self):
        assert self._val(giorni_a=300.5)["valido"] is False

    def test_finestra_zero_non_valida(self):
        assert self._val(finestra_h=0.0)["valido"] is False

    def test_p_col_zero_non_valida(self):
        assert self._val(potenza_col_kw=0.0)["valido"] is False

    def test_eta_zero_non_valido(self):
        assert self._val(eta=0.0)["valido"] is False

    def test_eta_sopra_uno_non_valido(self):
        assert self._val(eta=1.1)["valido"] is False

    def test_eta_uno_valido(self):
        assert self._val(eta=1.0)["valido"] is True

    def test_finestra_insufficiente_non_valida(self):
        # Finestra 2 h: P_gestita 3913,04 kW > 2400 kW
        v = self._val(finestra_h=2.0)
        assert v["valido"] is False
        assert "finestra" in v["errore"]

    def test_finestra_3h_insufficiente(self):
        # P_gestita 2608,70 kW > 2400 kW
        assert self._val(finestra_h=3.0)["valido"] is False

    def test_finestra_33h_sufficiente(self):
        # P_gestita 2371,09 kW < 2400 kW
        assert self._val(finestra_h=3.3)["valido"] is True

    def test_finestra_al_limite_valida(self):
        # Finestra = E_giorno / P_non_gestita =
        # 7826,09 / 2400 = 3,2608695652 h: P_gestita
        # == P_non_gestita, finestra sufficiente
        assert self._val(
            finestra_h=7826.086956521739 / 2400.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("prezzo_notte_eur_kwh",
                  "prezzo_giorno_eur_kwh",
                  "costo_potenza_eur_kw_mese",
                  "allaccio_fisso_eur",
                  "allaccio_costo_eur_kw", "ems_costo_eur",
                  "ems_opex_eur_a", "wacc_frac",
                  "km_bus_a", "consumo_diesel_l_100km",
                  "fattore_diesel_kg_l",
                  "fattore_elettrico_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=11.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(e_bus_kwh_giorno=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(n_bus=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta="0.92")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_notte_eur_kwh=0.0)["valido"] is True
        assert self._val(prezzo_giorno_eur_kwh=0.0)["valido"] is True
        assert self._val(ems_costo_eur=0.0)["valido"] is True
        assert self._val(ems_opex_eur_a=0.0)["valido"] is True
        assert self._val(allaccio_fisso_eur=0.0)["valido"] is True
        assert self._val(costo_potenza_eur_kw_mese=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_energia_giorno_demo(self):
        assert _F["mh708_energia_giorno_rete"](
            40, 180.0, 0.92) == pytest.approx(
            E_GIORNO_DEMO, rel=REL)

    def test_energia_giorno_eta_uno(self):
        assert _F["mh708_energia_giorno_rete"](
            40, 180.0, 1.0) == pytest.approx(7200.0, rel=REL)

    def test_energia_giorno_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh708_energia_giorno_rete"](40, 180.0, 0.0)

    def test_potenza_non_gestita_demo(self):
        assert _F["mh708_potenza_non_gestita"](
            40, 60.0) == pytest.approx(P_NG_DEMO, rel=REL)

    def test_potenza_gestita_demo(self):
        assert _F["mh708_potenza_gestita"](
            E_GIORNO_DEMO, 8.0) == pytest.approx(
            P_G_DEMO, rel=REL)

    def test_potenza_gestita_rifiuta_finestra_zero(self):
        with pytest.raises(ValueError):
            _F["mh708_potenza_gestita"](E_GIORNO_DEMO, 0.0)

    def test_energia_annua_demo(self):
        assert _F["mh708_energia_annua_mwh"](
            40, 180.0, 300) == pytest.approx(
            E_ANNUA_DEMO, rel=REL)

    def test_costo_non_gestita_demo(self):
        assert _F["mh708_costo_non_gestita"](
            2160000.0, 0.28, P_NG_DEMO,
            8.0) == pytest.approx(C_NG_DEMO, rel=REL)

    def test_costo_gestita_demo(self):
        assert _F["mh708_costo_gestita"](
            2160000.0, 0.12, P_G_DEMO, 8.0,
            5000.0) == pytest.approx(C_G_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh708_risparmio"](
            C_NG_DEMO, C_G_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh708_risparmio"](
            100000.0, 150000.0) == pytest.approx(
            -50000.0, rel=REL)

    def test_allaccio_non_gestita_demo(self):
        assert _F["mh708_allaccio"](
            20000.0, P_NG_DEMO, 150.0) == pytest.approx(
            A_NG_DEMO, rel=REL)

    def test_allaccio_gestita_demo(self):
        assert _F["mh708_allaccio"](
            20000.0, P_G_DEMO, 150.0) == pytest.approx(
            A_G_DEMO, rel=REL)

    def test_capex_delta_demo_negativo(self):
        # NON clampato a zero: il segno negativo
        # e' il punto di vendita onesto del caso.
        assert _F["mh708_capex_delta"](
            A_G_DEMO, 30000.0, A_NG_DEMO) == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert DELTA_DEMO < 0.0

    def test_capex_delta_puo_essere_positivo(self):
        assert _F["mh708_capex_delta"](
            A_G_DEMO, 400000.0, A_NG_DEMO) == pytest.approx(
            186739.1304347826, rel=REL)

    def test_co2_diesel_demo(self):
        assert _F["mh708_co2_diesel"](
            40, 60000.0, 35.0, 2.68) == pytest.approx(
            CO2_D_DEMO, rel=REL)

    def test_co2_elettrica_demo(self):
        assert _F["mh708_co2_elettrica"](
            E_ANNUA_DEMO, 0.35) == pytest.approx(
            CO2_E_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh708_co2_evitata"](
            CO2_D_DEMO, CO2_E_DEMO) == pytest.approx(
            CO2_EV_DEMO, rel=REL)

    def test_co2_evitata_unita_diesel(self):
        # 1 bus, 60000 km, 35 l/100km = 21000 l;
        # 21000 x 2,68 / 1000 = 56,28 t (non kg).
        assert _F["mh708_co2_diesel"](
            1, 60000.0, 35.0, 2.68) == pytest.approx(
            56.28, rel=REL)

    def test_crf_demo(self):
        assert _F["mh708_crf"](
            0.05, 12) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh708_crf"](0.0, 12) == pytest.approx(
            1.0 / 12.0, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh708_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-12)) / 0.05
        assert _F["mh708_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh708_van"](
            RISPARMIO_DEMO, DELTA_DEMO, 0.0,
            12) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 12, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh708_van"](RISPARMIO_DEMO, DELTA_DEMO, -0.01, 12)

    def test_van_accetta_delta_negativo(self):
        # -CAPEX_delta negativo = beneficio anno 0.
        assert _F["mh708_van"](
            100000.0, -50000.0, 0.05, 1) == pytest.approx(
            50000.0 + 100000.0 / 1.05, rel=1e-12)

    def test_tir_none_demo_delta_negativo(self):
        # Flusso anno 0 >= 0, nessun cambio di
        # segno: TIR None per costruzione, non
        # un errore.
        assert _F["mh708_tir"](
            DELTA_DEMO, RISPARMIO_DEMO, VITA_DEMO) is None

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh708_tir"](DELTA_DEMO, 0.0, 12) is None
        assert _F["mh708_tir"](186739.1304347826, -100.0, 12) is None

    def test_tir_none_se_delta_zero(self):
        assert _F["mh708_tir"](0.0, RISPARMIO_DEMO, 12) is None

    def test_tir_none_se_delta_negativo(self):
        assert _F["mh708_tir"](-1000.0, 5000.0, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh708_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_bisezione_indipendente_delta_positivo(self):
        delta = 186739.1304347826
        flussi = [-delta] + [RISPARMIO_DEMO] * 12

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
        assert abs(tir_ind * 100.0 - 255.4830571681969) <= 0.05
        tir = _F["mh708_tir"](delta, RISPARMIO_DEMO, 12)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_verifica_npv_zero_delta_positivo(self):
        delta = 186739.1304347826
        tir = _F["mh708_tir"](delta, RISPARMIO_DEMO, 12)
        npv = -delta + sum(
            RISPARMIO_DEMO / (1.0 + tir) ** i
            for i in range(1, 13))
        assert abs(npv) <= 1e-6 * delta

    def test_payback_demo_zero_delta_negativo(self):
        # RAMO ESPLICITO: CAPEX delta <= 0 ->
        # cumulato anno 0 gia' >= 0 -> payback 0
        # (investimento gia' ripagato).
        assert _F["mh708_payback"](
            DELTA_DEMO, RISPARMIO_DEMO, VITA_DEMO) == 0

    def test_payback_zero_se_delta_zero(self):
        assert _F["mh708_payback"](0.0, RISPARMIO_DEMO, 12) == 0

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh708_payback"](1000.0, 300.0, 10) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_anno_1_se_risparmio_ge_delta(self):
        assert _F["mh708_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh708_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh708_payback"](
            50000000.0, RISPARMIO_DEMO, 12) is None

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh708_payback"](DELTA_DEMO, 0.0, 12) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh708_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh708_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh708_verdetto"](
            -100.0, 186739.1304347826, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 18673,91304347826 = 10 % di
        # |CAPEX delta| 186739,1304347826
        assert _F["mh708_verdetto"](
            -18673.91304347826, 186739.1304347826, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh708_verdetto"](
            -18673.91304347827, 186739.1304347826, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_negativo_usa_valore_assoluto(self):
        # |VAN| 100 <= 10 % di |delta| 183260,87
        assert _F["mh708_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"
        assert _F["mh708_verdetto"](
            -20000.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh708_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh708_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh708_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh708_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_zero_mai_marginale(self):
        assert _F["mh708_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh708_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh708_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh708_demo"]()
        d.update(kw)
        return _F["mh708_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_giorno_rete_kwh"] == pytest.approx(
            E_GIORNO_DEMO, rel=REL)
        assert c["potenza_non_gestita_kw"] == pytest.approx(
            P_NG_DEMO, rel=REL)
        assert c["potenza_gestita_kw"] == pytest.approx(
            P_G_DEMO, rel=REL)
        assert c["picco_evitato_kw"] == pytest.approx(
            PICCO_DEMO, rel=REL)
        assert c["energia_annua_mwh_a"] == pytest.approx(
            E_ANNUA_DEMO, rel=REL)
        assert c["costo_non_gestita_eur_a"] == pytest.approx(
            C_NG_DEMO, rel=REL)
        assert c["costo_gestita_eur_a"] == pytest.approx(
            C_G_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["allaccio_non_gestita_eur"] == pytest.approx(
            A_NG_DEMO, rel=REL)
        assert c["allaccio_gestita_eur"] == pytest.approx(
            A_G_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["co2_diesel_t_a"] == pytest.approx(
            CO2_D_DEMO, rel=REL)
        assert c["co2_elettrica_t_a"] == pytest.approx(
            CO2_E_DEMO, rel=REL)
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
        d = _F["mh708_demo"]()
        b = _F["mh708_calcola"](**d)
        coppie = [("energia_giorno_rete_kwh", E_GIORNO_DEMO),
                  ("potenza_non_gestita_kw", P_NG_DEMO),
                  ("potenza_gestita_kw", P_G_DEMO),
                  ("picco_evitato_kw", PICCO_DEMO),
                  ("energia_annua_mwh_a", E_ANNUA_DEMO),
                  ("costo_non_gestita_eur_a", C_NG_DEMO),
                  ("costo_gestita_eur_a", C_G_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("allaccio_non_gestita_eur", A_NG_DEMO),
                  ("allaccio_gestita_eur", A_G_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_diesel_t_a", CO2_D_DEMO),
                  ("co2_elettrica_t_a", CO2_E_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert b["tir"] is None
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh708_demo"]()
        assert d["n_bus"] == 40
        assert d["e_bus_kwh_giorno"] == 180.0
        assert d["giorni_a"] == 300
        assert d["finestra_h"] == 8.0
        assert d["potenza_col_kw"] == 60.0
        assert d["eta"] == 0.92
        assert d["prezzo_notte_eur_kwh"] == 0.12
        assert d["prezzo_giorno_eur_kwh"] == 0.28
        assert d["costo_potenza_eur_kw_mese"] == 8.0
        assert d["allaccio_fisso_eur"] == 20000.0
        assert d["allaccio_costo_eur_kw"] == 150.0
        assert d["ems_costo_eur"] == 30000.0
        assert d["ems_opex_eur_a"] == 5000.0
        assert d["vita_anni"] == 12
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["km_bus_a"] == 60000.0
        assert d["consumo_diesel_l_100km"] == 35.0
        assert d["fattore_diesel_kg_l"] == 2.68
        assert d["fattore_elettrico_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_giorno_rete_kwh",
                       "potenza_non_gestita_kw",
                       "potenza_gestita_kw",
                       "picco_evitato_kw",
                       "energia_annua_mwh_a",
                       "costo_non_gestita_eur_a",
                       "costo_gestita_eur_a",
                       "risparmio_eur_a",
                       "allaccio_non_gestita_eur",
                       "allaccio_gestita_eur",
                       "capex_delta_eur",
                       "co2_diesel_t_a",
                       "co2_elettrica_t_a",
                       "co2_evitata_t_a",
                       "van"):
            assert repr(c[chiave]) in doc, chiave
        assert "tir = None" in doc
        assert "payback = 0" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_finestra_insufficiente_neutro(self):
        # Finestra 2 h: P_gestita 3913,04 > 2400
        n = self._bc(finestra_h=2.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert "finestra" in n["errore"]
        assert n["tir"] is None
        assert n["payback"] is None

    def test_prezzo_notte_alto_neutro_risparmio_negativo(self):
        # Prezzo notte 0,40 > prezzo giorno 0,28:
        # C_gestita 962913,04 > C_non_gestita 835200
        n = self._bc(prezzo_notte_eur_kwh=0.40)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_opex_ems_alto_riduce_risparmio(self):
        # Opex 100000: risparmio 382086,96; VAN
        # ancora positivo; CONVIENTE; payback 0
        # (delta ancora negativo)
        n = self._bc(ems_opex_eur_a=100000.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            382086.95652173914, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["payback"] == 0

    def test_capex_delta_zero_mai_marginale(self):
        # EMS 213260,8695652174: allaccio gestita
        # + EMS == allaccio non gestita -> delta 0
        n = self._bc(ems_costo_eur=213260.8695652174)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_capex_delta_positivo_payback_e_tir(self):
        # EMS 400000: delta 186739,1304347826;
        # VAN 4041802,617684906; TIR 255,483... %;
        # payback 1; CONVIENTE
        n = self._bc(ems_costo_eur=400000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            186739.1304347826, rel=REL)
        assert abs(n["van"] - 4041802.617684906) <= 1.0
        assert abs(n["tir"] - 255.4830571681969) <= 0.05
        assert n["payback"] == 1
        assert n["verdetto"] == "CONVIENTE"

    def test_marginale_ad_hoc(self):
        # EMS 363260,8695652174, prezzo notte
        # 0,27, vita 1, WACC 0,12: delta 150000,0;
        # risparmio 153086,95652173914; VAN
        # -13315,217391304264 entro tolleranza
        # 15000 -> MARGINALE; payback 1
        n = self._bc(ems_costo_eur=363260.8695652174,
                     prezzo_notte_eur_kwh=0.27,
                     vita_anni=1, wacc_frac=0.12)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            150000.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            153086.95652173914, rel=REL)
        assert abs(n["van"] - (-13315.217391304264)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 1

    def test_eta_uno_potenza_gestita_900(self):
        n = self._bc(eta=1.0)
        assert n["valid"] is True
        assert n["potenza_gestita_kw"] == pytest.approx(
            900.0, rel=REL)

    def test_eta_zero_neutro(self):
        n = self._bc(eta=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_n_bus_zero_neutro(self):
        n = self._bc(n_bus=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=11.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_non_interi_neutro(self):
        n = self._bc(giorni_a=300.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(e_bus_kwh_giorno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(n_bus=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -delta + risparmio x 12 =
        # 183260,8695652174 + 5725043,47826087 =
        # 5908304,347826087 -> CONVIENTE
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 12, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh708_neutro"]()
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
        n = _F["_mh708_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "n_bus",
                       "e_bus_kwh_giorno",
                       "giorni_a",
                       "finestra_h",
                       "potenza_col_kw",
                       "eta",
                       "energia_giorno_rete_kwh",
                       "potenza_non_gestita_kw",
                       "potenza_gestita_kw",
                       "picco_evitato_kw",
                       "energia_annua_mwh_a",
                       "costo_non_gestita_eur_a",
                       "costo_gestita_eur_a",
                       "risparmio_eur_a",
                       "allaccio_non_gestita_eur",
                       "allaccio_gestita_eur",
                       "capex_delta_eur",
                       "co2_diesel_t_a",
                       "co2_elettrica_t_a",
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
        assert len(b["df_tabella"]) == 32
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia giornaliera da rete (kWh/giorno)" in voci
        assert "Potenza non gestita (kW)" in voci
        assert "Potenza gestita (kW)" in voci
        assert "Potenza di picco evitata (kW)" in voci
        assert "Energia annua ricaricata (MWh/anno)" in voci
        assert "Costo annuo non gestita (EUR/anno)" in voci
        assert "Costo annuo gestita (EUR/anno)" in voci
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
        return _F["mh708_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh708_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh708_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_onere_potenza(self):
        s = _F["mh708_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_notte(self):
        s = _F["mh708_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh708_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh708_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # Onere potenza x0.9 e prezzo notte x1.1:
        # risparmio 437518,26 > 0, VAN
        # 4061095,31119363
        s = _F["mh708_sensitivita"](self._ing())
        assert s.loc["x0.9", "x1.1"] != 0.0
        assert abs(s.loc["x0.9", "x1.1"] - 4061095.31119363) <= 1.0
        ing = self._ing()
        ing["costo_potenza_eur_kw_mese"] = 8.0 * 0.9
        ing["prezzo_notte_eur_kwh"] = 0.12 * 1.1
        assert _F["mh708_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            437518.2608695652, rel=REL)

    def test_sensitivita_angoli(self):
        s = _F["mh708_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 4520566.276027137) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 4762509.924176182) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 4303038.959342675) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh708_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 37

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh708_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_non_gestita_eur_a" in txt
        assert "costo_gestita_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "n_bus" in txt
        assert "energia_giorno_rete_kwh" in txt
        assert "co2_evitata_t_a" in txt
        assert "finestra_h" in txt
        assert "ems_costo_eur" in txt
        assert "capex_delta_eur" in txt
        assert "picco_evitato_kw" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh708_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_non_gestita_eur_a;{bc['costo_non_gestita_eur_a']}" in txt
        assert "energia_annua_mwh_a;2160.0" in txt
        assert "ems_opex_eur_a;5000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def708["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def708\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 20, ui_keys
        demo_keys = set(_F["mh708_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh708_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh708_demo():")
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
        ui_keys = set(re.findall(r'_def708\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W709 (25/10/2026) - tab708' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh708_num", "mh708_nneg", "mh708_pos",
                     "mh708_int_pos", "mh708_int_nneg",
                     "mh708_quota_valida", "mh708_eta_valido",
                     "mh708_energia_giorno_rete",
                     "mh708_potenza_non_gestita",
                     "mh708_potenza_gestita",
                     "mh708_energia_annua_mwh",
                     "mh708_costo_non_gestita",
                     "mh708_costo_gestita", "mh708_risparmio",
                     "mh708_allaccio", "mh708_capex_delta",
                     "mh708_co2_diesel", "mh708_co2_elettrica",
                     "mh708_co2_evitata", "mh708_crf",
                     "mh708_van", "mh708_tir", "mh708_payback",
                     "mh708_verdetto", "mh708_valida",
                     "_mh708_neutro", "mh708_calcola",
                     "mh708_sensitivita", "mh708_csv",
                     "mh708_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        assert "mh707" not in _helpers_src()
        assert "tab707" not in _helpers_src()
        assert "mh707" not in _ui_src()
        assert "tab707" not in _ui_src()

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w709_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE708) == 1

    def test_blocco_with_tab708(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab708:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE708

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st708_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 25, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st708_") for k in keys)

    def test_chiavi_st_input_sono_21(self):
        """Le 21 chiavi di input/bottone (20 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st708_[a-z0-9_]+)"', _ui_src())
        attese = ["st708_n_bus", "st708_e_bus",
                  "st708_giorni", "st708_finestra",
                  "st708_p_col", "st708_eta",
                  "st708_p_notte", "st708_p_giorno",
                  "st708_c_pot", "st708_allaccio_fisso",
                  "st708_allaccio_kw", "st708_ems",
                  "st708_ems_opex", "st708_vita",
                  "st708_wacc", "st708_tolleranza",
                  "st708_km", "st708_consumo",
                  "st708_f_diesel", "st708_f_el",
                  "st708_calcola"]
        assert len(attese) == 21
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg708" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg708") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg708")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia annua ricaricata (MWh/anno)" in src
        assert "Potenza di picco evitata (kW)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver708" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "potenza impegnata" in src
        assert "tco" in src
        assert "colonnine pubbliche" in src
        assert "finestra" in src
        assert "ems" in src
        assert "demand" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "potenza impegnata" in src.lower()
        assert "tco" in src.lower()
        assert "colonnine" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo non gestita" in src
        assert "Costo annuo gestita" in src
        assert "Risparmio annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh708_csv" in src
        assert "ricarica_deposito_bus_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh708_sensitivita" in src
        assert "Heatmap" in src
        assert "Onere di potenza" in src
        assert "Prezzo notte" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st708_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W709 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab708:")
