"""Test tab701 "🌬️♻️ Recuperatore di calore per ventilazione: l'aria esausta scalda l'aria nuova?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
portata 5000 m3/h; ore di ventilazione 5000
h/anno; temperatura interna 20 °C;
temperatura esterna media 5 °C; rendimento
recuperatore 0,85; potenza ventilatori 2,0
kW; prezzo elettricita' 200 EUR/MWh; OPEX
annuo 500 EUR/anno; rendimento caldaia 0,9;
prezzo gas 100 EUR/MWh; costo specifico 15
EUR/(m3/h); costo fisso 2000 EUR; vita 15
anni; WACC 5 %; tolleranza 10 % del CAPEX;
fattore gas 0,20 tCO2/MWh; fattore
elettricita' 0,35 tCO2/MWh.

- coeff_volumetrico = 0.0003349999999999999
- delta_t_k = 15.0
- perdita_ventilazione_mwh_a = 125.62499999999996
- calore_recuperato_mwh_a = 106.78124999999996
- perdita_residua_mwh_a = 18.843749999999996
- energia_ventilatori_mwh_a = 10.0
- costo_baseline_eur_a = 13958.333333333328
- costo_recupero_eur_a = 4593.75
- risparmio_eur_a = 9364.583333333328
- co2_evitata_t_a = 20.229166666666657
- capex_eur = 77000.0
- van = 20201.172670045344
- tir = 8.665278505908926
- payback = 9
- verdetto = 'CONVIENTE'

Scomposizione: coeff 1,2 x 1,005 / 3600 =
0.0003349999999999999; perdita 5000 x 5000
x 15 x coeff / 1000 = 125.62499999999996;
calore 125.62499999999996 x 0,85 =
106.78124999999996; residua
125.62499999999996 x 0,15 =
18.843749999999996; e_vent 2,0 x 5000 /
1000 = 10.0; c_base 125.62499999999996 /
0,9 x 100 = 13958.333333333328; c_rec
18.843749999999996 / 0,9 x 100 + 10,0 x 200
+ 500 = 4593.75; risparmio
13958.333333333328 - 4593.75 =
9364.583333333328; co2 106.78124999999996 /
0,9 x 0,20 - 10,0 x 0,35 =
20.229166666666657; capex 5000 x 15 + 2000
= 77000.0; VAN -77000,0 +
9364.583333333328 x (1 - 1,05^-15) / 0,05 =
20201.172670045344; TIR per bisezione su
[-0,99, 5,0] dei flussi [-77000,
9364.583333333328 x 15]: 8.665278505908926 %
(VAN a quella TIR ~0); payback: cumulato
anno 8 -2083,3333333333712, anno 9
+7281,25 -> 9.
NOTA: i valori esatti ricalcolati sono
quelli sopra (perdita 125,625 MWh, VAN
20201,17, TIR 8,6653 %) — il test fissa i
valori esatti, non le approssimazioni.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w702_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w702_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w702_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w702_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w702_helpers.py: {missing}")
    return out


_F = _load("mh701_num", "mh701_nneg", "mh701_pos",
           "mh701_int_pos", "mh701_rendimento_valido",
           "mh701_coeff_volumetrico", "mh701_delta_t",
           "mh701_perdita_ventilazione",
           "mh701_calore_recuperato",
           "mh701_perdita_residua",
           "mh701_energia_ventilatori",
           "mh701_costo_baseline", "mh701_costo_recupero",
           "mh701_risparmio", "mh701_co2_evitata",
           "mh701_capex", "mh701_crf", "mh701_van",
           "mh701_tir", "mh701_payback",
           "mh701_verdetto", "mh701_valida",
           "_mh701_neutro", "mh701_calcola",
           "mh701_sensitivita", "mh701_csv",
           "mh701_demo", "demo_calcoli")

TITLE701 = ("🌬️♻️ Recuperatore di calore per ventilazione: "
            "l'aria esausta scalda l'aria nuova?")

COEFF_DEMO = 0.0003349999999999999
DT_DEMO = 15.0
PERDITA_DEMO = 125.62499999999996
CALORE_DEMO = 106.78124999999996
RESIDUA_DEMO = 18.843749999999996
E_VENT_DEMO = 10.0
C_BASE_DEMO = 13958.333333333328
C_REC_DEMO = 4593.75
RISP_DEMO = 9364.583333333328
CO2_DEMO = 20.229166666666657
CAPEX_DEMO = 77000.0
VAN_DEMO = 20201.172670045344
TIR_DEMO = 8.665278505908926
PAYBACK_DEMO = 9
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.09634228760924432

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w702_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w702_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh701_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh701_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh701_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh701_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh701_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh701_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh701_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh701_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh701_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh701_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh701_int_pos"](15.0, "x") == 15

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh701_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh701_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh701_rendimento_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh701_demo"]()
        d.update(kw)
        return _F["mh701_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_delta_t_zero_non_valido(self):
        v = self._val(temp_esterna_c=20.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_delta_t_negativo_non_valido(self):
        v = self._val(temp_esterna_c=25.0)
        assert v["valido"] is False

    def test_temp_esterna_negativa_valida(self):
        v = self._val(temp_esterna_c=-5.0)
        assert v["valido"] is True

    def test_eta_recuperatore_zero_non_valido(self):
        v = self._val(rendimento_recuperatore=0.0)
        assert v["valido"] is False

    def test_eta_recuperatore_sopra_uno_non_valido(self):
        v = self._val(rendimento_recuperatore=1.2)
        assert v["valido"] is False

    def test_eta_recuperatore_uno_valido(self):
        v = self._val(rendimento_recuperatore=1.0)
        assert v["valido"] is True

    def test_rendimento_caldaia_zero_non_valido(self):
        v = self._val(rendimento_caldaia=0.0)
        assert v["valido"] is False

    def test_rendimento_caldaia_sopra_uno_non_valido(self):
        v = self._val(rendimento_caldaia=1.2)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=14.5)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("portata_m3_h", "ore_h_a",
                  "potenza_ventilatori_kw",
                  "prezzo_elettricita_eur_mwh", "opex_annuo",
                  "prezzo_gas_eur_mwh",
                  "costo_specifico_eur_m3h", "costo_fisso_eur",
                  "wacc_pct", "tolleranza_pct",
                  "fattore_gas", "fattore_elettricita"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_nan_non_valido(self):
        v = self._val(rendimento_recuperatore=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(portata_m3_h=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(portata_m3_h=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(rendimento_recuperatore="0.85")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(portata_m3_h=0.0)["valido"] is True
        assert self._val(ore_h_a=0.0)["valido"] is True
        assert self._val(
            prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(potenza_ventilatori_kw=0.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_pct=150.0)["valido"] is True
        assert self._val(tolleranza_pct=150.0)["valido"] is True


class TestFisicaEconomia:
    def test_coeff_volumetrico(self):
        assert _F["mh701_coeff_volumetrico"]() == pytest.approx(
            COEFF_DEMO, rel=REL)

    def test_coeff_formula_chiusa(self):
        assert _F["mh701_coeff_volumetrico"]() == pytest.approx(
            1.2 * 1.005 / 3600.0, rel=1e-12)

    def test_delta_t_demo(self):
        assert _F["mh701_delta_t"](20.0, 5.0) == pytest.approx(
            DT_DEMO, rel=REL)

    def test_delta_t_rifiuta_uguali(self):
        with pytest.raises(ValueError):
            _F["mh701_delta_t"](20.0, 20.0)

    def test_delta_t_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh701_delta_t"](5.0, 20.0)

    def test_delta_t_con_esterna_negativa(self):
        assert _F["mh701_delta_t"](20.0, -5.0) == pytest.approx(
            25.0, rel=REL)

    def test_perdita_demo(self):
        assert _F["mh701_perdita_ventilazione"](
            5000.0, 5000.0, 15.0) == pytest.approx(
            PERDITA_DEMO, rel=REL)

    def test_perdita_portata_zero(self):
        assert _F["mh701_perdita_ventilazione"](
            0.0, 5000.0, 15.0) == 0.0

    def test_perdita_ore_zero(self):
        assert _F["mh701_perdita_ventilazione"](
            5000.0, 0.0, 15.0) == 0.0

    def test_perdita_rifiuta_dt_zero(self):
        with pytest.raises(ValueError):
            _F["mh701_perdita_ventilazione"](5000.0, 5000.0, 0.0)

    def test_perdita_scala_con_portata(self):
        assert _F["mh701_perdita_ventilazione"](
            2500.0, 5000.0, 15.0) == pytest.approx(
            PERDITA_DEMO / 2.0, rel=REL)

    def test_calore_recuperato_demo(self):
        assert _F["mh701_calore_recuperato"](
            PERDITA_DEMO, 0.85) == pytest.approx(
            CALORE_DEMO, rel=REL)

    def test_calore_recuperato_rendimento_uno(self):
        assert _F["mh701_calore_recuperato"](
            PERDITA_DEMO, 1.0) == pytest.approx(
            PERDITA_DEMO, rel=REL)

    def test_calore_recuperato_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh701_calore_recuperato"](PERDITA_DEMO, 0.0)

    def test_perdita_residua_demo(self):
        assert _F["mh701_perdita_residua"](
            PERDITA_DEMO, 0.85) == pytest.approx(
            RESIDUA_DEMO, rel=REL)

    def test_perdita_residua_piu_calore_uguale_perdita(self):
        assert _F["mh701_perdita_residua"](
            PERDITA_DEMO, 0.85) + _F["mh701_calore_recuperato"](
            PERDITA_DEMO, 0.85) == pytest.approx(
            PERDITA_DEMO, rel=REL)

    def test_energia_ventilatori_demo(self):
        assert _F["mh701_energia_ventilatori"](
            2.0, 5000.0) == pytest.approx(E_VENT_DEMO, rel=REL)

    def test_energia_ventilatori_potenza_zero(self):
        assert _F["mh701_energia_ventilatori"](
            0.0, 5000.0) == 0.0

    def test_costo_baseline_demo(self):
        assert _F["mh701_costo_baseline"](
            PERDITA_DEMO, 0.9, 100.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_baseline_rifiuta_rendimento_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh701_costo_baseline"](PERDITA_DEMO, 1.2, 100.0)

    def test_costo_recupero_demo(self):
        assert _F["mh701_costo_recupero"](
            RESIDUA_DEMO, 0.9, 100.0, E_VENT_DEMO, 200.0,
            500.0) == pytest.approx(C_REC_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh701_risparmio"](
            C_BASE_DEMO, C_REC_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh701_risparmio"](
            10000.0, 17593.75) == pytest.approx(
            -7593.75, rel=REL)

    def test_co2_demo(self):
        assert _F["mh701_co2_evitata"](
            CALORE_DEMO, 0.9, 0.20,
            E_VENT_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_puo_essere_negativa(self):
        assert _F["mh701_co2_evitata"](
            CALORE_DEMO, 0.9, 0.05,
            E_VENT_DEMO, 0.90) < 0.0

    def test_capex_demo(self):
        assert _F["mh701_capex"](
            5000.0, 15.0, 2000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh701_capex"](
            0.0, 15.0, 2000.0) == 2000.0

    def test_capex_scala_con_portata(self):
        assert _F["mh701_capex"](
            10000.0, 15.0, 2000.0) == pytest.approx(
            152000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh701_crf"](
            0.05, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh701_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 15 / (1.05 ** 15 - 1.0)
        assert _F["mh701_crf"](0.05, 15) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh701_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-15)) / 0.05
        assert _F["mh701_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh701_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            15) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh701_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 15)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh701_van"](RISP_DEMO, -1.0, 0.05, 15)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh701_tir"](
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
        tir = _F["mh701_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh701_tir"](CAPEX_DEMO, 0.0, 15) is None
        assert _F["mh701_tir"](CAPEX_DEMO, -100.0, 15) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh701_tir"](0.0, RISP_DEMO, 15) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh701_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh701_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 16))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh701_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 8 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 9 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh701_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh701_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh701_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh701_payback"](
            50000000.0, RISP_DEMO, 15) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh701_payback"](0.0, RISP_DEMO, 15) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh701_payback"](CAPEX_DEMO, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh701_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh701_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh701_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 7700 = 10 % di CAPEX 77000
        assert _F["mh701_verdetto"](
            -7700.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh701_verdetto"](
            -7700.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh701_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh701_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh701_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh701_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh701_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh701_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh701_demo"]()
        d.update(kw)
        return _F["mh701_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["perdita_ventilazione_mwh_a"] == pytest.approx(
            PERDITA_DEMO, rel=REL)
        assert c["delta_t_k"] == pytest.approx(
            DT_DEMO, rel=REL)
        assert c["calore_recuperato_mwh_a"] == pytest.approx(
            CALORE_DEMO, rel=REL)
        assert c["perdita_residua_mwh_a"] == pytest.approx(
            RESIDUA_DEMO, rel=REL)
        assert c["energia_ventilatori_mwh_a"] == pytest.approx(
            E_VENT_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_recupero_eur_a"] == pytest.approx(
            C_REC_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
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
        d = _F["mh701_demo"]()
        b = _F["mh701_calcola"](**d)
        coppie = [("perdita_ventilazione_mwh_a", PERDITA_DEMO),
                  ("delta_t_k", DT_DEMO),
                  ("calore_recuperato_mwh_a", CALORE_DEMO),
                  ("perdita_residua_mwh_a", RESIDUA_DEMO),
                  ("energia_ventilatori_mwh_a", E_VENT_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_recupero_eur_a", C_REC_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh701_demo"]()
        assert d["portata_m3_h"] == 5000.0
        assert d["ore_h_a"] == 5000.0
        assert d["temp_interna_c"] == 20.0
        assert d["temp_esterna_c"] == 5.0
        assert d["rendimento_recuperatore"] == 0.85
        assert d["potenza_ventilatori_kw"] == 2.0
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["opex_annuo"] == 500.0
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 100.0
        assert d["costo_specifico_eur_m3h"] == 15.0
        assert d["costo_fisso_eur"] == 2000.0
        assert d["vita_anni"] == 15
        assert d["wacc_pct"] == 5.0
        assert d["tolleranza_pct"] == 10.0
        assert d["fattore_gas"] == 0.20
        assert d["fattore_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("perdita_ventilazione_mwh_a",
                       "delta_t_k",
                       "calore_recuperato_mwh_a",
                       "perdita_residua_mwh_a",
                       "energia_ventilatori_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_recupero_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 9" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_portata_dimezzata(self):
        # Portata 2500 m3/h (ore invariate):
        # perdita 62,8125; calore 53,390625;
        # residua 9,421875; e_vent invariata 10,0
        # (dipende da potenza x ore); c_base
        # 6979,1667; c_rec 3546,875; risparmio
        # 3432,2917; capex 39500,0 -> MARGINALE
        n = self._bc(portata_m3_h=2500.0)
        assert n["valid"] is True
        assert n["perdita_ventilazione_mwh_a"] == pytest.approx(
            62.81249999999998, rel=REL)
        assert n["energia_ventilatori_mwh_a"] == pytest.approx(
            10.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            3432.2916666666642, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            39500.0, rel=REL)
        assert n["verdetto"] == "MARGINALE"

    def test_rendimento_095(self):
        # Eta 0,95: calore 119,34375; residua
        # 6,28125; c_rec 3197,9167; risparmio
        # 10760,4167
        n = self._bc(rendimento_recuperatore=0.95)
        assert n["valid"] is True
        assert n["calore_recuperato_mwh_a"] == pytest.approx(
            119.34374999999996, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            10760.41666666666, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_rendimento_uno(self):
        # Eta 1,0: calore = perdita; residua 0;
        # c_rec 2500,0; risparmio 11458,3333
        n = self._bc(rendimento_recuperatore=1.0)
        assert n["valid"] is True
        assert n["perdita_residua_mwh_a"] == pytest.approx(
            0.0, abs=1e-12)
        assert n["risparmio_eur_a"] == pytest.approx(
            11458.333333333328, rel=REL)

    def test_eta_recuperatore_zero_neutro(self):
        n = self._bc(rendimento_recuperatore=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_recuperatore_sopra_uno_neutro(self):
        n = self._bc(rendimento_recuperatore=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_temp_uguali_neutro(self):
        n = self._bc(temp_esterna_c=20.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["errore"] != ""
        assert n["tir"] is None
        assert n["payback"] is None

    def test_temp_esterna_piu_alta_neutro(self):
        n = self._bc(temp_esterna_c=25.0)
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

    def test_vita_otto_non_conviente(self):
        # VAN circa -16474,71, oltre il 10 % del
        # CAPEX; payback None (cumulato anno 8
        # < CAPEX)
        n = self._bc(vita_anni=8)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_vita_nove_non_conviente(self):
        # VAN circa -10438,21, oltre il 10 % del
        # CAPEX; payback 9
        n = self._bc(vita_anni=9)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 9

    def test_vita_dieci_marginale(self):
        # VAN circa -4689,17, entro il 10 % del
        # CAPEX (7700); payback 9
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 9

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(rendimento_recuperatore=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(portata_m3_h=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(portata_m3_h=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_portata_zero_neutro_via_risparmio(self):
        # Perdita 0, c_base 0, c_rec 2500 (e_vent
        # 10 MWh x 200 + opex 500) -> risparmio < 0
        n = self._bc(portata_m3_h=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["tir"] is None
        assert n["payback"] is None

    def test_ore_zero_neutro_via_risparmio(self):
        # Perdita 0, e_vent 0, c_rec = opex 500
        # -> risparmio -500
        n = self._bc(ore_h_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_gas_zero_neutro_via_risparmio(self):
        n = self._bc(prezzo_gas_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["tir"] is None
        assert n["payback"] is None

    def test_risparmio_negativo_neutro(self):
        # Prezzo elettricita' 1500: c_rec
        # 17593,75 contro c_base 13958,33 ->
        # risparmio < 0
        n = self._bc(prezzo_elettricita_eur_mwh=1500.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_prezzo_elettricita_600_non_conviente(self):
        # Risparmio ancora positivo (5364,58) ma
        # VAN -21317,46: NON_CONVIENTE, non neutro
        n = self._bc(prezzo_elettricita_eur_mwh=600.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 15

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 15, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_specifico_eur_m3h=0.0,
                     costo_fisso_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh701_neutro"]()
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
        n = _F["_mh701_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "perdita_ventilazione_mwh_a",
                       "delta_t_k",
                       "calore_recuperato_mwh_a",
                       "perdita_residua_mwh_a",
                       "energia_ventilatori_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_recupero_eur_a",
                       "risparmio_eur_a",
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
        assert len(b["df_tabella"]) == 25
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Perdita ventilazione (MWh/anno)" in voci
        assert "Calore recuperato (MWh/anno)" in voci
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
        return _F["mh701_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh701_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh701_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_rendimento(self):
        s = _F["mh701_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_prezzo_gas(self):
        s = _F["mh701_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh701_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh701_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_cella_peggiore_ancora_positiva(self):
        # Rendimento x0.9 (0,765) e prezzo gas
        # x0.9 (90): risparmio 7110,31 > 0,
        # quindi VAN non degenere
        s = _F["mh701_sensitivita"](self._ing())
        assert s.loc["x0.9", "x0.9"] != 0.0
        ing = self._ing()
        ing["rendimento_recuperatore"] = 0.85 * 0.9
        ing["prezzo_gas_eur_mwh"] = 100.0 * 0.9
        assert _F["mh701_calcola"](**ing)[
            "risparmio_eur_a"] == pytest.approx(
            7110.312499999997, rel=REL)

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh701_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 31

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh701_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_recupero_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "portata_m3_h" in txt
        assert "calore_recuperato_mwh_a" in txt
        assert "energia_ventilatori_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "rendimento_recuperatore" in txt
        assert "costo_fisso_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh701_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"calore_recuperato_mwh_a;{CALORE_DEMO}" in txt
        assert "opex_annuo;500.0" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def701["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def701\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 17, ui_keys
        demo_keys = set(_F["mh701_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh701_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh701_demo():")
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
        ui_keys = set(re.findall(r'_def701\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W702 (25/10/2026) - tab701' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh701_num", "mh701_nneg", "mh701_pos",
                     "mh701_int_pos", "mh701_rendimento_valido",
                     "mh701_coeff_volumetrico", "mh701_delta_t",
                     "mh701_perdita_ventilazione",
                     "mh701_calore_recuperato",
                     "mh701_perdita_residua",
                     "mh701_energia_ventilatori",
                     "mh701_costo_baseline",
                     "mh701_costo_recupero",
                     "mh701_risparmio", "mh701_co2_evitata",
                     "mh701_capex", "mh701_crf",
                     "mh701_van", "mh701_tir",
                     "mh701_payback", "mh701_verdetto",
                     "mh701_valida", "_mh701_neutro",
                     "mh701_calcola", "mh701_sensitivita",
                     "mh701_csv", "mh701_demo",
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
        ast.parse((_new_dir() / "w702_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE701) == 1

    def test_blocco_with_tab701(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab701:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE701

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st701_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 22, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st701_") for k in keys)

    def test_chiavi_st_input_sono_18(self):
        """Le 18 chiavi di input/bottone del brief
        (17 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st701_[a-z0-9_]+)"', _ui_src())
        attese = ["st701_portata", "st701_ore",
                  "st701_temp_interna", "st701_temp_esterna",
                  "st701_rendimento_recuperatore",
                  "st701_potenza_ventilatori",
                  "st701_prezzo_elettricita", "st701_opex",
                  "st701_rendimento_caldaia", "st701_prezzo_gas",
                  "st701_fattore_gas",
                  "st701_fattore_elettricita",
                  "st701_costo_specifico", "st701_costo_fisso",
                  "st701_vita", "st701_wacc_pct",
                  "st701_tolleranza_pct", "st701_calcola"]
        assert len(attese) == 18
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg701" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg701") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg701")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Calore recuperato (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd701" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_ventilazione_presente(self):
        src = _ui_src().lower()
        assert "ventilazione" in src
        assert "recuperatore" in src
        assert "scambiatore" in src
        assert "ventilatori" in src
        assert "filtri" in src
        assert "pompa di calore" in src
        assert "perdite di carico" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline senza recupero" in src
        assert "Con recuperatore" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh701_csv" in src
        assert "recuperatore_ventilazione_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh701_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento" in src
        assert "Prezzo gas" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st701_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W702 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab701:")
        assert "mh701_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab701" in (_new_dir() / "w702_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w702_helpers.py", "w702_ui.py",
                   "w702_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab701"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "70" + "0"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w702_helpers.py", "w702_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_ventilazione_non_pompa_calore(self):
        assert "ventilazione" in TITLE701.lower()
        assert "esausta" in TITLE701.lower()
