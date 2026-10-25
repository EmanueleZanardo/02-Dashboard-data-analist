"""Test tab716 "🌊🧂 Energia da gradiente salino: la foce del fiume genera elettricità?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
portata dolce 5 m3/s; temperatura 293 K;
concentrazione mare 600 mol/m3;
concentrazione fiume 10 mol/m3; rendimento
membrana 0,35; rendimento sistema 0,85;
rapporto mare/dolce 1,0; salto pompe
20000 Pa; rendimento pompe 0,75; ore
equivalenti 8000; costo specifico
8000 EUR/kW; costo fisso 500000 EUR; O&M
specifico 150 EUR/kW/anno; O&M fisso 50000
EUR/anno; prezzo energia 0,12 EUR/kWh;
costo membrane 1500 EUR/kW; vita membrane
7 anni; vita di progetto 20 anni; WACC
0,06 (6 %); tolleranza 0,10 (10 % del
|CAPEX|); fattore rete 0,35 t/MWh.

- delta_pi_pa = 2874482.36
- p_teor_w = 14372411.799999999
- p_pompaggio_w = 266666.6666666667
- p_net_w = 4009125.8438333324
- p_net_kw = 4009.1258438333325
- e_annua_kwh = 32073006.75066666
- e_annua_mwh = 32073.00675066666
- capex_eur = 32573006.75066666
- om_eur_a = 651368.8765749999
- ricavo_eur_a = 3848760.810079999
- risparmio_eur_a = 3197391.9335049987
- costo_sostituzione_eur = 6013688.765749998
- anni_sostituzione = [7, 14]
- co2_evitata_t_a = 11225.55236273333
- van = -2558480.0018314943
- tir = 4.9860381440990365
- payback = 13
- verdetto = 'MARGINALE'

Scomposizione: delta_pi 2 x 8,314 x 293 x
(600 - 10) = 2 x 8,314 x 293 x 590 =
2874482.36 Pa; P_teor 2874482.36 x 5 =
14372411.799999999 W; P_pompaggio (5 + 5)
x 20000 / 0,75 = 266666.6666666667 W;
P_net 14372411.799999999 x 0,35 x 0,85 -
266666.6666666667 = 4275792.510166666 -
266666.6666666667 = 4009125.8438333324 W
(4009.1258438333325 kW); E_annua
4009.1258438333325 x 8000 =
32073006.75066666 kWh (32073.00675066666
MWh); CAPEX 4009.1258438333325 x 8000 +
500000 = 32573006.75066666 EUR; O&M
4009.1258438333325 x 150 + 50000 =
651368.8765749999 EUR/anno; ricavo
32073006.75066666 x 0,12 =
3848760.810079999 EUR/anno; risparmio
3848760.810079999 - 651368.8765749999 =
3197391.9335049987 EUR/anno; sostituzione
4009.1258438333325 x 1500 =
6013688.765749998 EUR agli anni 7 e 14
(multipli di floor(7) = 7 con 1 <= anno <
20); flussi [-32573006.75066666,
3197391.9335049987 x 20 con anni 7 e 14 =
-2816296.8322449997]; VAN -2558480.0018314943
a WACC 6 % su 20 anni; TIR
4.9860381440990365 %; payback 13 (cumulato
anno 12 = -217992,32 ancora negativo,
cumulato anno 13 = 2979399,61 >= 0);
CO2 32073.00675066666 x 0,35 =
11225.55236273333 t/anno (informativa,
basata sull'energia annua, non un ricavo);
VAN < 0 ma |VAN| 2558480,00 <= tolleranza
0,10 x 32573006,75 = 3257300,68 ->
MARGINALE.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w717_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w717_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w717_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w717_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w717_helpers.py: {missing}")
    return out


_F = _load("mh716_num", "mh716_nneg", "mh716_pos",
           "mh716_int_pos", "mh716_int_nneg",
           "mh716_eff", "mh716_delta_pi",
           "mh716_p_teorica", "mh716_p_pompaggio",
           "mh716_p_netta", "mh716_energia_annua",
           "mh716_capex", "mh716_om_annuo",
           "mh716_ricavo", "mh716_risparmio",
           "mh716_costo_sostituzione",
           "mh716_anni_sostituzione", "mh716_flussi",
           "mh716_van_flussi", "mh716_tir_flussi",
           "mh716_payback_flussi", "mh716_verdetto",
           "mh716_co2_evitata", "mh716_valida",
           "_mh716_neutro", "mh716_calcola",
           "mh716_sensitivita", "mh716_csv",
           "mh716_demo", "demo_calcoli")

TITLE716 = ("🌊🧂 Energia da gradiente salino: "
            "la foce del fiume genera elettricità?")

DELTA_PI_DEMO = 2874482.36
P_TEOR_DEMO = 14372411.799999999
P_POMP_DEMO = 266666.6666666667
P_NET_DEMO = 4009125.8438333324
P_NET_KW_DEMO = 4009.1258438333325
E_KWH_DEMO = 32073006.75066666
E_MWH_DEMO = 32073.00675066666
CAPEX_DEMO = 32573006.75066666
OM_DEMO = 651368.8765749999
RICAVO_DEMO = 3848760.810079999
RISPARMIO_DEMO = 3197391.9335049987
COSTO_SOST_DEMO = 6013688.765749998
CO2_DEMO = 11225.55236273333
VAN_DEMO = -2558480.0018314943
TIR_DEMO = 4.9860381440990365
PAYBACK_DEMO = 13
VITA_DEMO = 20
VERDETTO_DEMO = "MARGINALE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w717_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w717_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh716_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh716_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh716_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh716_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh716_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh716_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh716_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh716_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh716_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh716_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh716_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero(self):
        assert _F["mh716_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh716_int_nneg"](-1, "x")

    def test_eff_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh716_eff"](0.0, "x")

    def test_eff_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh716_eff"](1.01, "x")

    def test_eff_accetta_uno(self):
        assert _F["mh716_eff"](1.0, "x") == 1.0

    def test_eff_accetta_valore_interno(self):
        assert _F["mh716_eff"](0.35, "x") == 0.35


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh716_demo"]()
        d.update(kw)
        return _F["mh716_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_portata_zero_non_valida(self):
        assert self._val(portata_m3_s=0.0)["valido"] is False

    def test_portata_negativa_non_valida(self):
        assert self._val(portata_m3_s=-1.0)["valido"] is False

    def test_temp_zero_non_valida(self):
        assert self._val(temp_k=0.0)["valido"] is False

    def test_temp_negativa_non_valida(self):
        assert self._val(temp_k=-10.0)["valido"] is False

    def test_c_mare_uguale_c_fiume_non_valida(self):
        assert self._val(c_mare_mol_m3=10.0)["valido"] is False

    def test_c_mare_minore_c_fiume_non_valida(self):
        assert self._val(c_mare_mol_m3=5.0)["valido"] is False

    def test_c_fiume_negativa_non_valida(self):
        assert self._val(c_fiume_mol_m3=-1.0)["valido"] is False

    def test_rendimenti_fuori_intervallo_non_validi(self):
        assert self._val(eta_membrana=0.0)["valido"] is False
        assert self._val(eta_membrana=1.2)["valido"] is False
        assert self._val(eta_sistema=0.0)["valido"] is False
        assert self._val(eta_pompe=1.5)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("rapporto_mare_dolce", "delta_p_pompe_pa",
                  "ore_eq_annue", "c_specifico_eur_kw",
                  "capex_fisso_eur", "om_eur_kw_a",
                  "om_fisso_eur_a", "prezzo_el_eur_kwh",
                  "c_membrane_eur_kw", "wacc_frac",
                  "tolleranza_frac", "f_rete_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_membrane_zero_non_valida(self):
        assert self._val(vita_membrane_anni=0.0)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=19.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        # Brief tab716: tol >= 0 senza tetto
        # superiore (come la tab precedente).
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(temp_k=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(portata_m3_s=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(portata_m3_s=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(temp_k="293")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(c_fiume_mol_m3=0.0)["valido"] is True
        assert self._val(rapporto_mare_dolce=0.0)["valido"] is True
        assert self._val(delta_p_pompe_pa=0.0)["valido"] is True
        assert self._val(ore_eq_annue=0.0)["valido"] is True
        assert self._val(c_specifico_eur_kw=0.0)["valido"] is True
        assert self._val(prezzo_el_eur_kwh=0.0)["valido"] is True
        assert self._val(f_rete_t_mwh=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_delta_pi_demo(self):
        assert _F["mh716_delta_pi"](
            600.0, 10.0, 293.0) == pytest.approx(
            DELTA_PI_DEMO, rel=REL)

    def test_delta_pi_fattore_due_vant_hoff(self):
        # Senza il fattore i = 2 la pressione
        # sarebbe la meta': 1437241,18 Pa.
        assert _F["mh716_delta_pi"](
            600.0, 10.0, 293.0) == pytest.approx(
            2.0 * 8.314 * 293.0 * 590.0, rel=REL)
        assert 2.0 * 8.314 * 293.0 * 590.0 > 2874482.0
        assert 2.0 * 8.314 * 293.0 * 590.0 < 2874483.0

    def test_delta_pi_zero_se_concentrazioni_uguali(self):
        assert _F["mh716_delta_pi"](
            10.0, 10.0, 293.0) == pytest.approx(0.0, abs=1e-9)

    def test_delta_pi_negativo_se_gradiente_invertito(self):
        assert _F["mh716_delta_pi"](
            5.0, 10.0, 293.0) == pytest.approx(
            -24360.02, rel=REL)

    def test_delta_pi_rifiuta_temp_zero(self):
        with pytest.raises(ValueError):
            _F["mh716_delta_pi"](600.0, 10.0, 0.0)

    def test_p_teorica_demo(self):
        assert _F["mh716_p_teorica"](
            DELTA_PI_DEMO, 5.0) == pytest.approx(
            P_TEOR_DEMO, rel=REL)

    def test_p_pompaggio_demo(self):
        assert _F["mh716_p_pompaggio"](
            5.0, 1.0, 20000.0, 0.75) == pytest.approx(
            P_POMP_DEMO, rel=REL)

    def test_p_pompaggio_zero_se_salto_zero(self):
        assert _F["mh716_p_pompaggio"](
            5.0, 1.0, 0.0, 0.75) == pytest.approx(0.0, abs=1e-9)

    def test_p_pompaggio_raddoppia_con_rapporto(self):
        # Rapporto 1 -> 10 m3/s totali;
        # rapporto 3 -> 20 m3/s totali.
        assert _F["mh716_p_pompaggio"](
            5.0, 3.0, 20000.0, 0.75) == pytest.approx(
            2.0 * P_POMP_DEMO, rel=REL)

    def test_p_netta_demo(self):
        assert _F["mh716_p_netta"](
            P_TEOR_DEMO, 0.35, 0.85,
            P_POMP_DEMO) == pytest.approx(
            P_NET_DEMO, rel=REL)

    def test_p_netta_puo_essere_negativa(self):
        assert _F["mh716_p_netta"](
            1000000.0, 0.10, 0.50,
            200000.0) == pytest.approx(-150000.0, rel=REL)

    def test_energia_annua_demo(self):
        assert _F["mh716_energia_annua"](
            P_NET_DEMO, 8000.0) == pytest.approx(
            E_KWH_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh716_capex"](
            P_NET_KW_DEMO, 8000.0, 500000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_om_annuo_demo(self):
        assert _F["mh716_om_annuo"](
            P_NET_KW_DEMO, 150.0, 50000.0) == pytest.approx(
            OM_DEMO, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh716_ricavo"](
            E_KWH_DEMO, 0.12) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh716_risparmio"](
            RICAVO_DEMO, OM_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh716_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_costo_sostituzione_demo(self):
        assert _F["mh716_costo_sostituzione"](
            P_NET_KW_DEMO, 1500.0) == pytest.approx(
            COSTO_SOST_DEMO, rel=REL)

    def test_anni_sostituzione_demo(self):
        assert _F["mh716_anni_sostituzione"](7.0, 20) == [7, 14]

    def test_anni_sostituzione_multipli(self):
        assert _F["mh716_anni_sostituzione"](10, 20) == [10]
        assert _F["mh716_anni_sostituzione"](5, 20) == [5, 10, 15]

    def test_anni_sostituzione_floor_non_intero(self):
        # Vita 7,5 -> floor 7: anni 7 e 14.
        assert _F["mh716_anni_sostituzione"](7.5, 20) == [7, 14]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh716_anni_sostituzione"](0.5, 20) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh716_anni_sostituzione"](20, 20) == []
        assert _F["mh716_anni_sostituzione"](10, 20) == [10]

    def test_co2_evitata_demo(self):
        assert _F["mh716_co2_evitata"](
            E_MWH_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)
        assert CO2_DEMO > 0.0

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh716_co2_evitata"](
            E_MWH_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_co2_evitata_zero_se_energia_zero(self):
        assert _F["mh716_co2_evitata"](
            0.0, 0.35) == pytest.approx(0.0, abs=1e-9)


class TestFinanza:
    def test_van_flussi_demo(self):
        flussi = [-CAPEX_DEMO] + [RISPARMIO_DEMO] * 20
        flussi[7] -= COSTO_SOST_DEMO
        flussi[14] -= COSTO_SOST_DEMO
        assert abs(_F["mh716_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-CAPEX_DEMO] + [RISPARMIO_DEMO] * 20
        flussi[7] -= COSTO_SOST_DEMO
        flussi[14] -= COSTO_SOST_DEMO
        atteso = (-CAPEX_DEMO + RISPARMIO_DEMO * 20
                  - 2.0 * COSTO_SOST_DEMO)
        assert _F["mh716_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh716_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo(self):
        flussi = _F["mh716_flussi"](
            CAPEX_DEMO, RISPARMIO_DEMO,
            COSTO_SOST_DEMO, [7, 14], 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[7] == pytest.approx(
            RISPARMIO_DEMO - COSTO_SOST_DEMO, rel=REL)
        assert flussi[14] == pytest.approx(
            RISPARMIO_DEMO - COSTO_SOST_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_senza_sostituzioni(self):
        flussi = _F["mh716_flussi"](
            CAPEX_DEMO, RISPARMIO_DEMO,
            COSTO_SOST_DEMO, [], 20)
        assert all(f == pytest.approx(RISPARMIO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh716_tir_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh716_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_tredici(self):
        flussi = [-CAPEX_DEMO] + [RISPARMIO_DEMO] * 20
        flussi[7] -= COSTO_SOST_DEMO
        flussi[14] -= COSTO_SOST_DEMO
        assert _F["mh716_payback_flussi"](flussi) == PAYBACK_DEMO
        cum12 = (-CAPEX_DEMO + RISPARMIO_DEMO * 12
                 - COSTO_SOST_DEMO)
        assert cum12 < 0.0
        assert cum12 + RISPARMIO_DEMO >= 0.0

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh716_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai(self):
        assert _F["mh716_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 20) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh716_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) == 0

    def test_verdetto_marginale_demo(self):
        assert _F["mh716_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh716_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh716_verdetto"](
            -100.0, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh716_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh716_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh716_verdetto"](
            -9000000.0, CAPEX_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh716_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh716_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh716_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh716_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh716_verdetto"](100.0, CAPEX_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_accetta_tolleranza_sopra_uno(self):
        assert _F["mh716_verdetto"](
            -100.0, CAPEX_DEMO, 1.5,
            RISPARMIO_DEMO) == "MARGINALE"


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh716_demo"]()
        d.update(kw)
        return _F["mh716_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["delta_pi_pa"] == pytest.approx(
            DELTA_PI_DEMO, rel=REL)
        assert c["p_teor_w"] == pytest.approx(
            P_TEOR_DEMO, rel=REL)
        assert c["p_pompaggio_w"] == pytest.approx(
            P_POMP_DEMO, rel=REL)
        assert c["p_net_w"] == pytest.approx(
            P_NET_DEMO, rel=REL)
        assert c["p_net_kw"] == pytest.approx(
            P_NET_KW_DEMO, rel=REL)
        assert c["e_annua_kwh"] == pytest.approx(
            E_KWH_DEMO, rel=REL)
        assert c["e_annua_mwh"] == pytest.approx(
            E_MWH_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["om_eur_a"] == pytest.approx(
            OM_DEMO, rel=REL)
        assert c["ricavo_eur_a"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["costo_sostituzione_eur"] == pytest.approx(
            COSTO_SOST_DEMO, rel=REL)
        assert c["anni_sostituzione"] == [7, 14]
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh716_demo"]()
        b = _F["mh716_calcola"](**d)
        coppie = [("delta_pi_pa", DELTA_PI_DEMO),
                  ("p_teor_w", P_TEOR_DEMO),
                  ("p_pompaggio_w", P_POMP_DEMO),
                  ("p_net_w", P_NET_DEMO),
                  ("p_net_kw", P_NET_KW_DEMO),
                  ("e_annua_kwh", E_KWH_DEMO),
                  ("e_annua_mwh", E_MWH_DEMO),
                  ("capex_eur", CAPEX_DEMO),
                  ("om_eur_a", OM_DEMO),
                  ("ricavo_eur_a", RICAVO_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("costo_sostituzione_eur", COSTO_SOST_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sostituzione"] == [7, 14]
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh716_demo"]()
        assert d["portata_m3_s"] == 5.0
        assert d["temp_k"] == 293.0
        assert d["c_mare_mol_m3"] == 600.0
        assert d["c_fiume_mol_m3"] == 10.0
        assert d["eta_membrana"] == 0.35
        assert d["eta_sistema"] == 0.85
        assert d["rapporto_mare_dolce"] == 1.0
        assert d["delta_p_pompe_pa"] == 20000.0
        assert d["eta_pompe"] == 0.75
        assert d["ore_eq_annue"] == 8000.0
        assert d["c_specifico_eur_kw"] == 8000.0
        assert d["capex_fisso_eur"] == 500000.0
        assert d["om_eur_kw_a"] == 150.0
        assert d["om_fisso_eur_a"] == 50000.0
        assert d["prezzo_el_eur_kwh"] == 0.12
        assert d["c_membrane_eur_kw"] == 1500.0
        assert d["vita_membrane_anni"] == 7.0
        assert d["vita_progetto_anni"] == 20
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert d["f_rete_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("delta_pi_pa",
                       "p_teor_w",
                       "p_pompaggio_w",
                       "p_net_w",
                       "p_net_kw",
                       "e_annua_kwh",
                       "e_annua_mwh",
                       "capex_eur",
                       "om_eur_a",
                       "ricavo_eur_a",
                       "risparmio_eur_a",
                       "costo_sostituzione_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sostituzione"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 13" in doc
        assert "verdetto = 'MARGINALE'" in doc

    def test_prezzo_alto_conviente(self):
        # Prezzo energia 0,20 EUR/kWh: ricavo
        # 6414601,35, risparmio 5763232,47, VAN
        # 26871508,85, TIR 15,22 %, payback 6.
        n = self._bc(prezzo_el_eur_kwh=0.20)
        assert n["valid"] is True
        assert n["ricavo_eur_a"] == pytest.approx(
            6414601.350133332, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            5763232.473558333, rel=REL)
        assert abs(n["van"] - 26871508.851981167) <= 1.0
        assert abs(n["tir"] - 15.224722017427483) <= 0.01
        assert n["payback"] == 6
        assert n["verdetto"] == "CONVIENTE"

    def test_costo_specifico_alto_non_conviente(self):
        # Costo specifico 9000 EUR/kW: CAPEX
        # 36582132,59, VAN -6567605,85 oltre
        # tolleranza 3658213,26 -> NON_CONVIENTE;
        # TIR 3,63 %, payback 16.
        n = self._bc(c_specifico_eur_kw=9000.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(
            36582132.59449999, rel=REL)
        assert abs(n["van"] - (-6567605.845664827)) <= 1.0
        assert abs(n["tir"] - 3.628384893027542) <= 0.01
        assert n["payback"] == 16
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        # Costi CAPEX a zero -> CAPEX 0, VAN
        # positivo, payback 0, mai MARGINALE.
        n = self._bc(c_specifico_eur_kw=0.0, capex_fisso_eur=0.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0

    def test_pompaggio_alto_potenza_netta_negativa(self):
        # Salto pompe 500000 Pa: pompaggio
        # 6666666,67 W > potenza utile
        # 4275792,51 W -> P_net negativa ->
        # dict neutro NON_CALCOLABILE.
        n = self._bc(delta_p_pompe_pa=500000.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["p_net_w"] == 0.0

    def test_prezzo_basso_risparmio_negativo(self):
        # Prezzo 0,01 EUR/kWh: ricavo 320730,07
        # < O&M 651368,88 -> risparmio negativo
        # -> dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_el_eur_kwh=0.01)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_concentrazioni_uguali_neutro(self):
        n = self._bc(c_mare_mol_m3=10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_portata_zero_neutro(self):
        n = self._bc(portata_m3_s=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_temp_zero_neutro(self):
        n = self._bc(temp_k=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_sopra_uno_neutro(self):
        n = self._bc(eta_membrana=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_membrane_zero_neutro(self):
        n = self._bc(vita_membrane_anni=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(temp_k=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(portata_m3_s=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(portata_m3_s=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -32573006,75 + 3197391,93 x 20 -
        # 2 x 6013688,77 = 19347454,39.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            19347454.387933318, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_vita_membrane_lunga_meno_sostituzioni(self):
        # Vita membrane 10 anni: una sola
        # sostituzione (anno 10), VAN
        # 742814,43 -> CONVIENTE.
        n = self._bc(vita_membrane_anni=10.0)
        assert n["valid"] is True
        assert n["anni_sostituzione"] == [10]
        assert abs(n["van"] - 742814.4347237763) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh716_neutro"]()
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
        n = _F["_mh716_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "portata_m3_s", "temp_k",
                       "c_mare_mol_m3",
                       "c_fiume_mol_m3",
                       "delta_pi_pa",
                       "p_teor_w",
                       "p_pompaggio_w",
                       "p_net_w", "p_net_kw",
                       "e_annua_kwh",
                       "e_annua_mwh",
                       "capex_eur",
                       "om_eur_a",
                       "ricavo_eur_a",
                       "risparmio_eur_a",
                       "costo_sostituzione_eur",
                       "anni_sostituzione",
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
        assert len(b["df_tabella"]) == 33
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Pressione osmotica (Pa)" in voci
        assert "Potenza netta (kW)" in voci
        assert "Energia annua (MWh)" in voci
        assert "CAPEX (EUR)" in voci
        assert "O&M annuo (EUR/anno)" in voci
        assert "Ricavo annuo (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "Costo sostituzione (EUR)" in voci
        assert "CO2 evitata vs rete (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[7] == \
            pytest.approx(RISPARMIO_DEMO - COSTO_SOST_DEMO, rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh716_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh716_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh716_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_decrescente_con_costo_specifico(self):
        s = _F["mh716_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] > \
                s.loc["x1.0", colonna] > \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_prezzo_energia(self):
        s = _F["mh716_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh716_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh716_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh716_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - (-3765677.6548367226)) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 5063319.001307089) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - (-10180279.004970048)) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - (-1351282.3488262456)) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita membrane 10 anni la griglia
        # deve includere la sostituzione anno
        # 10: il centro deve coincidere col VAN
        # del caso con vita membrane 10.
        ing = self._ing()
        ing["vita_membrane_anni"] = 10.0
        s = _F["mh716_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 742814.4347237763) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh716_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 38

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh716_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "risparmio_eur_a" in txt
        assert "ricavo_eur_a" in txt
        assert "om_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "portata_m3_s" in txt
        assert "e_annua_kwh" in txt
        assert "co2_evitata_t_a" in txt
        assert "c_mare_mol_m3" in txt
        assert "capex_eur" in txt
        assert "delta_pi_pa" in txt
        assert "p_net_kw" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh716_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"ricavo_eur_a;{bc['ricavo_eur_a']}" in txt
        assert "portata_m3_s;5.0" in txt
        assert "om_eur_kw_a;150.0" in txt
        assert f"capex_eur;{bc['capex_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def716["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def716\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 21, ui_keys
        demo_keys = set(_F["mh716_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh716_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh716_demo():")
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
        ui_keys = set(re.findall(r'_def716\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W717 (25/10/2026) - tab716' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh716_num", "mh716_nneg", "mh716_pos",
                     "mh716_int_pos", "mh716_int_nneg",
                     "mh716_eff", "mh716_delta_pi",
                     "mh716_p_teorica", "mh716_p_pompaggio",
                     "mh716_p_netta", "mh716_energia_annua",
                     "mh716_capex", "mh716_om_annuo",
                     "mh716_ricavo", "mh716_risparmio",
                     "mh716_costo_sostituzione",
                     "mh716_anni_sostituzione", "mh716_flussi",
                     "mh716_van_flussi", "mh716_tir_flussi",
                     "mh716_payback_flussi", "mh716_verdetto",
                     "mh716_co2_evitata", "mh716_valida",
                     "_mh716_neutro", "mh716_calcola",
                     "mh716_sensitivita", "mh716_csv",
                     "mh716_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        # I frammenti nuovi usano solo mh716 /
        # tab716 / st716: nessun identificatore
        # della numerazione successiva.
        assert "mh717" not in _helpers_src()
        assert "mh717" not in _ui_src()
        assert "st717" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab715 (idrogeno in
        # caverne saline) come punto di confronto
        # (regressione tab675) e la nuova tab e'
        # tab716.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab675" in src
        assert "tab715" in src
        assert "tab716" in src
        assert _ui_src().startswith("    with tab716:")

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w717_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE716) == 1

    def test_blocco_with_tab716(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab716:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE716

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st716_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 26, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st716_") for k in keys)

    def test_chiavi_st_input_sono_22(self):
        """Le 22 chiavi di input/bottone (21 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st716_[a-z0-9_]+)"', _ui_src())
        attese = ["st716_portata", "st716_temp",
                  "st716_c_mare", "st716_c_fiume",
                  "st716_eta_membrana", "st716_eta_sistema",
                  "st716_rapporto", "st716_c_membrane",
                  "st716_delta_p", "st716_eta_pompe",
                  "st716_ore_eq", "st716_c_specifico",
                  "st716_capex_fisso", "st716_prezzo_el",
                  "st716_om_kw", "st716_om_fisso",
                  "st716_vita_membrane", "st716_vita_progetto",
                  "st716_wacc", "st716_tolleranza",
                  "st716_f_rete", "st716_calcola"]
        assert len(attese) == 22
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg716" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg716") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg716")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Potenza netta (kW)" in src
        assert "Energia annua (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver716" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "portata dolce" in src
        assert "basso salto pompe" in src
        assert "informative" in src
        assert "membrane" in src
        assert "sostituzioni" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "O&M annuo" in src
        assert "Ricavo annuo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh716_csv" in src
        assert "gradiente_salino_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh716_sensitivita" in src
        assert "Heatmap" in src
        assert "Costo specifico" in src
        assert "Prezzo energia" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st716_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W717 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab716:")
