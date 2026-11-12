"""Test nuova scheda olivicoltura:
irrigazione a goccia + frantoio efficiente +
pompa di calore + FV battono
irrigazione tradizionale + frantoio tradizionale +
riscaldamento a gas?
Repo path: tests/test_w890_olivicoltura.py

Business case annuo di una olivicoltura,
guidato dagli ETTARI DI OLIVETO
(demo 3 ha):
irrigazione tradizionale base 3 x 2000 =
6000 kWh/anno; frantoio tradizionale
3 x 2800 = 8400 kWh/anno; elettricita' base
totale 14400 kWh/anno, costo energia base 3168
EUR/anno; gas base 3 x 600 = 1800 Smc/anno,
costo gas base 1620 EUR/anno; O&M base 7000
EUR/anno; costo base 11788 EUR/anno;
irrigazione a goccia 3 x 1000 = 3000
kWh/anno; frantoio efficiente 3 x 1400 = 4200
kWh/anno; pompa di calore riscaldamento 3 x 1200
= 3600 kWh/anno; elettricita'
alternativa 10800 kWh/anno, gas per riscaldamento
ELIMINATO; kWp = sup FV x kwp per m2
(demo 24 kWp); E_pv 26400 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 10560 kWh/anno); immessa 15840 kWh/anno;
deficit 240 kWh/anno; ricavo immissione 1267,20
EUR/anno; O&M alternativa 5000 EUR/anno; C_alt
3785,60 EUR/anno; risparmio 8002,40 EUR/anno; CAPEX
6000 + 18000 + 12000 + 24 x 900 = 57600 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 7,11
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0,06
t/anno (immessa senza credito CO2); CO2 evitata
7,05 t/anno; LCO base 3929,3333 EUR/ha e LCO alt
1261,8667 EUR/ha (costi operativi annui per
ha, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato
maggiore o uguale a 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno gas_alt)
in forma chiusa (demo None: rapporto negativo meno
3,5458, vince anche a gas gratuito), None se il
denominatore e' nullo o negativo o se il rapporto e'
negativo. L'alternativa non usa gas, quindi gas_alt
= 0 e il denominatore e' gas_base.
E' una SOGLIA MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa vince, sotto
perde. Verdetto: NON_CALCOLABILE se input degenere
(ettari minori o uguali a 0, kWh per ha minori
di 0, prezzi minori di 0, O&M minori di 0,
superficie FV minore di 0, kwp per m2 minore di 0,
resa minore di 0, f_autoconsumo minore di 0 o
maggiore di 1, voci CAPEX minori di 0,
fattori CO2 minori di 0, WACC minore di 0, vita
minore o uguale a 0 o non intera,
tolleranza minore di 0) o se risparmio minore o
uguale a 0 (guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN
maggiore di 0, MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: ettari zero non calcolabile
(ValueError negli helper, guard NON_CALCOLABILE in
UI); frazione autoconsumo zero (autoconsumo zero);
prezzo gas zero (ancora calcolabile, risparmio
positivo, VAN positiva: CONVIENTE);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: qui SOLO olive e olio da
olive, NIENTE altri raccolti, NIENTE altri settori
agricoli, NIENTE allevamenti, NIENTE latte, NIENTE
trasformazione del latte; qui solo olivicoltura:
irrigazione + frantoio + riscaldamento + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w890_helpers import (
        demo_calcoli,
        mh886_c_alt,
        mh886_c_base,
        mh886_calcola,
        mh886_capex_totale,
        mh886_co2_alt,
        mh886_co2_base,
        mh886_co2_evitata,
        mh886_csv,
        mh886_demo,
        mh886_demo_calcoli,
        mh886_e_alt,
        mh886_e_base_totale,
        mh886_e_deficit,
        mh886_e_irrigazione_alt,
        mh886_e_irrigazione_base,
        mh886_e_immessa,
        mh886_e_pdc,
        mh886_e_pv,
        mh886_e_pv_auto,
        mh886_e_frantoio_alt,
        mh886_e_frantoio_base,
        mh886_flussi,
        mh886_frazione,
        mh886_gas_base,
        mh886_int_pos,
        mh886_kwp,
        mh886_lco,
        mh886_nneg,
        mh886_num,
        mh886_p_gas_pareggio,
        mh886_payback,
        mh886_pos,
        mh886_ricavo_immissione,
        mh886_risparmio,
        mh886_sensibilita,
        mh886_tir,
        mh886_valida,
        mh886_van,
        mh886_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w890_helpers", os.path.join(_hf, "w890_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh886_c_alt = _mod.mh886_c_alt
    mh886_c_base = _mod.mh886_c_base
    mh886_calcola = _mod.mh886_calcola
    mh886_capex_totale = _mod.mh886_capex_totale
    mh886_co2_alt = _mod.mh886_co2_alt
    mh886_co2_base = _mod.mh886_co2_base
    mh886_co2_evitata = _mod.mh886_co2_evitata
    mh886_csv = _mod.mh886_csv
    mh886_demo = _mod.mh886_demo
    mh886_demo_calcoli = _mod.mh886_demo_calcoli
    mh886_e_alt = _mod.mh886_e_alt
    mh886_e_base_totale = _mod.mh886_e_base_totale
    mh886_e_deficit = _mod.mh886_e_deficit
    mh886_e_irrigazione_alt = _mod.mh886_e_irrigazione_alt
    mh886_e_irrigazione_base = _mod.mh886_e_irrigazione_base
    mh886_e_immessa = _mod.mh886_e_immessa
    mh886_e_pdc = _mod.mh886_e_pdc
    mh886_e_pv = _mod.mh886_e_pv
    mh886_e_pv_auto = _mod.mh886_e_pv_auto
    mh886_e_frantoio_alt = _mod.mh886_e_frantoio_alt
    mh886_e_frantoio_base = _mod.mh886_e_frantoio_base
    mh886_flussi = _mod.mh886_flussi
    mh886_frazione = _mod.mh886_frazione
    mh886_gas_base = _mod.mh886_gas_base
    mh886_int_pos = _mod.mh886_int_pos
    mh886_kwp = _mod.mh886_kwp
    mh886_lco = _mod.mh886_lco
    mh886_nneg = _mod.mh886_nneg
    mh886_num = _mod.mh886_num
    mh886_p_gas_pareggio = _mod.mh886_p_gas_pareggio
    mh886_payback = _mod.mh886_payback
    mh886_pos = _mod.mh886_pos
    mh886_ricavo_immissione = _mod.mh886_ricavo_immissione
    mh886_risparmio = _mod.mh886_risparmio
    mh886_sensibilita = _mod.mh886_sensibilita
    mh886_tir = _mod.mh886_tir
    mh886_valida = _mod.mh886_valida
    mh886_van = _mod.mh886_van
    mh886_verdetto = _mod.mh886_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w890_helpers.py")
_UI_PATH = _risolvi("w890_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "9"
_VECCHIO_MH_TAB = "mh88" + "5"
_VECCHIO_TAB = "tab88" + "5"
_VECCHIO_ST = "st88" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_irrigazione_base_kwh_anno": 6000.0,
    "e_frantoio_base_kwh_anno": 8400.0,
    "e_base_kwh_anno": 14400.0,
    "gas_base_smc_anno": 1800.0,
    "c_base_eur_anno": 11788.0,
    "e_irrigazione_alt_kwh_anno": 3000.0,
    "e_frantoio_alt_kwh_anno": 4200.0,
    "e_pdc_kwh_anno": 3600.0,
    "e_alt_kwh_anno": 10800.0,
    "kwp": 24.0,
    "e_pv_kwh_anno": 26400.0,
    "e_pv_auto_kwh_anno": 10560.0,
    "e_immessa_kwh_anno": 15840.0,
    "e_deficit_kwh_anno": 240.0,
    "ricavo_immissione_eur_anno": 1267.2,
    "c_alt_eur_anno": 3785.6,
    "risparmio_eur_anno": 8002.4,
    "capex_eur": 57600.0,
    "co2_base_t_anno": 7.11,
    "co2_alt_t_anno": 0.06,
    "co2_evitata_t_anno": 7.05,
    "lco_base_eur_ha": 3929.3333333333335,
    "lco_alt_eur_ha": 1261.8666666666666,
    "van": 25462.175484736355,
    "tir": 10.982452207078094,
    "payback": 8,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh886_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh886_num(3, "x"), 3.0)
        self.assertEqual(mh886_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh886_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh886_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh886_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh886_pos(0, "x")
        with self.assertRaises(ValueError):
            mh886_pos(-1, "x")
        self.assertEqual(mh886_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh886_int_pos(15, "x"), 15)
        self.assertEqual(mh886_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh886_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh886_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh886_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh886_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh886_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh886_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_irrigazione_frantoio_base_e_costo_base(self):
        self.assertEqual(mh886_e_irrigazione_base(3, 2000), 6000.0)
        self.assertEqual(mh886_e_frantoio_base(3, 2800), 8400.0)
        self.assertEqual(mh886_e_base_totale(6000.0, 8400.0), 14400.0)
        self.assertEqual(mh886_gas_base(3, 600), 1800.0)
        self.assertEqual(mh886_c_base(14400.0, 0.22, 1800.0, 0.90,
                                       7000), 11788.0)

    def test_irrigazione_frantoio_pdc_somma(self):
        self.assertEqual(mh886_e_irrigazione_alt(3, 1000), 3000.0)
        self.assertEqual(mh886_e_frantoio_alt(3, 1400), 4200.0)
        self.assertEqual(mh886_e_pdc(3, 1200), 3600.0)
        self.assertEqual(mh886_e_alt(3000.0, 4200.0, 3600.0), 10800.0)
        # L'irrigazione a goccia RIDUCE il consumo di
        # irrigazione, non lo azzera: 1000 resta sopra zero
        # anche a parita' di base 2000.
        self.assertGreater(mh886_e_irrigazione_alt(3, 1000), 0.0)
        self.assertLess(mh886_e_irrigazione_alt(3, 1000),
                        mh886_e_irrigazione_base(3, 2000))
        # Il frantoio efficiente RIDUCE il consumo di
        # frantoio, non lo azzera: 1400 resta sopra zero
        # anche a parita' di base 2800.
        self.assertGreater(mh886_e_frantoio_alt(3, 1400), 0.0)
        self.assertLess(mh886_e_frantoio_alt(3, 1400),
                        mh886_e_frantoio_base(3, 2800))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh886_kwp(120, 0.20), 24.0)
        self.assertEqual(mh886_e_pv(24.0, 1100), 26400.0)
        self.assertEqual(mh886_e_pv_auto(26400.0, 0.40, 10800.0),
                         10560.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh886_e_pv_auto(26400.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh886_e_immessa(26400.0, 10560.0), 15840.0)
        self.assertEqual(mh886_e_deficit(10800.0, 10560.0), 240.0)
        self.assertEqual(mh886_e_deficit(10800.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh886_ricavo_immissione(15840.0, 0.08), 1267.2)
        self.assertAlmostEqual(
            mh886_c_alt(240.0, 0.22, 1267.2, 5000.0),
            3785.6)
        self.assertAlmostEqual(mh886_risparmio(11788.0, 3785.6),
                               8002.4)

    def test_capex_totale_voci(self):
        self.assertEqual(mh886_capex_totale(6000, 18000, 12000, 24.0,
                                            900),
                         57600.0)
        self.assertEqual(mh886_capex_totale(6000, 18000, 12000, 0.0,
                                            900),
                         36000.0)

    def test_co2_base_e_alt(self):
        cb = mh886_co2_base(1800.0, 1.95, 14400.0, 0.25)
        self.assertAlmostEqual(cb, 7.11, places=4)
        ca = mh886_co2_alt(240.0, 0.25)
        self.assertAlmostEqual(ca, 0.06, places=4)
        self.assertAlmostEqual(mh886_co2_evitata(cb, ca), 7.05, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh886_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh886_lco(11788.0, 3), 3929.3333333333335)
        self.assertAlmostEqual(mh886_lco(3785.6, 3), 1261.8666666666666)
        with self.assertRaises(ValueError):
            mh886_lco(11788.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh886_flussi(57600, 8002.4, 3),
                         [-57600, 8002.4, 8002.4, 8002.4])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh886_van([-100, 60, 60], 0), 20.0)
        bc = mh886_demo_calcoli()
        self.assertAlmostEqual(mh886_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh886_demo_calcoli()
        tir = mh886_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh886_tir([-100, -10, -10]))
        self.assertIsNone(mh886_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh886_demo_calcoli()
        self.assertEqual(mh886_payback(bc["flussi"]), 8)
        self.assertIsNone(mh886_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh886_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh886_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:8]), -1583.2, places=2)
        self.assertAlmostEqual(sum(flussi[:9]), 6419.2, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh886_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh886_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh886_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh886_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh886_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh886_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh886_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh886_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["c_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], -3.5457777777777775, places=6)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh886_p_gas_pareggio(1800.0, 0.0, 14400.0,
                                 0.22, 7000.0, 20000.0),
            5.462222222222222, places=6)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh886_p_gas_pareggio(1800.0, 0.0, 14400.0,
                                              0.22, 7000.0, 10168.0),
                         0.0)
        self.assertIsNone(mh886_p_gas_pareggio(0.0, 0.0, 14400.0,
                                               0.22, 7000.0, 20000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh886_p_gas_pareggio(1800.0, 1800.0, 14400.0,
                                               0.22, 7000.0, 20000.0))
        self.assertIsNone(mh886_p_gas_pareggio(1800.0, 0.0, 14400.0,
                                               0.22, 7000.0, 3785.6))

    def test_valida_demo_ok(self):
        demo = mh886_demo()
        val = mh886_valida(*[demo[k] for k in (
            "ettari_ha", "e_irrigazione_base_per_ha",
            "e_frantoio_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_irrigazione_alt_per_ha", "e_frantoio_alt_per_ha",
            "e_pdc_per_ha", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_irrigazione_eur",
            "capex_frantoio_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_ettari_zero_no(self):
        kw = _demo_kwargs(ettari_ha=0)
        self.assertRaises(ValueError, mh886_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh886_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh886_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh886_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh886_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("ettari_ha", -1),
                              ("e_irrigazione_base_per_ha", -1),
                              ("p_gas", -0.01),
                              ("capex_irrigazione_eur", -1),
                              ("capex_pdc_eur", -1),
                              ("e_frantoio_base_per_ha", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh886_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh886_calcola(mh886_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh886_calcola(dict(mh886_demo(), capex_irrigazione_eur=99999),
                           capex_irrigazione_eur=6000)
        self.assertEqual(bc["capex_eur"], 57600.0)


class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, int):
                    self.assertEqual(ottenuto, atteso)
                else:
                    self.assertLess(_rel(ottenuto, atteso), 1e-9)

    def test_demo_verdetto_convente(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 8)

    def test_coerenza_costi_e_co2(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(
            bc["c_base_eur_anno"],
            bc["e_base_kwh_anno"] * bc["p_el"]
            + bc["gas_base_smc_anno"] * bc["p_gas"]
            + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["ricavo_immissione_eur_anno"]
            + bc["om_alt_eur_anno"])
        self.assertAlmostEqual(
            bc["lco_base_eur_ha"],
            bc["c_base_eur_anno"] / bc["ettari_ha"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_ha"],
            bc["c_alt_eur_anno"] / bc["ettari_ha"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh886_sensibilita(**mh886_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               8326.4, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               28825.18, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 7)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               8625.44, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               31929.12, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 7)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               4412.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               9795.05, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 9)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 36000.0)
        self.assertAlmostEqual(s["senza_irrigazione_goccia"]["risparmio_eur_anno"],
                               7342.4, places=2)
        self.assertAlmostEqual(s["senza_irrigazione_goccia"]["van"],
                               18611.60, places=2)
        self.assertEqual(s["senza_irrigazione_goccia"]["payback"], 8)
        self.assertEqual(s["senza_irrigazione_goccia"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -32137.82, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 15)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               4192.41, places=2)
        self.assertEqual(s["vita_10"]["payback"], 8)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               62436.0, places=2)

    def test_marginale_con_capex_frantoio_alto(self):
        # CAPEX totale 87600 (frantoio a 48000):
        # VAN circa meno 4537,82, entro la tolleranza del 10%
        # (8760).
        bc = mh886_calcola(**_demo_kwargs(capex_frantoio_eur=48000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -4537.82, places=2)

    def test_non_convente_con_capex_frantoio_altissimo(self):
        bc = mh886_calcola(**_demo_kwargs(capex_frantoio_eur=90000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -46537.82, places=2)
        self.assertIsNone(bc["payback"])

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh886_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -86997.6)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh886_csv(bc, mh886_demo())
        for voce in ("ettari_ha", "e_base_kwh_anno",
                     "e_irrigazione_base_kwh_anno", "e_pdc_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_ha", "lco_alt_eur_ha"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -57600.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Ettari di oliveto (ha)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh886_c_alt(10800.0, 0.22, 0.0, 5000.0)
        con = mh886_c_alt(240.0, 0.22, 1267.2, 5000.0)
        self.assertAlmostEqual(senza - con, 10560.0 * 0.22 + 1267.2)

    def test_sensibilita_chiavi_complete(self):
        s = mh886_sensibilita(**mh886_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_irrigazione_goccia",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh886_csv(bc, mh886_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh886_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh886_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh886_calcola(**_demo_kwargs(sup_fv_m2=0))
        self.assertEqual(bc["capex_eur"], 36000.0)
        bc = mh886_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_ettari_zero_non_calcolabile(self):
        # Ettari zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(ettari_ha=0)
        self.assertRaises(ValueError, mh886_calcola, **kw)
        self.assertFalse(mh886_valida(*[kw[k] for k in (
            "ettari_ha", "e_irrigazione_base_per_ha",
            "e_frantoio_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_irrigazione_alt_per_ha", "e_frantoio_alt_per_ha",
            "e_pdc_per_ha", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_irrigazione_eur",
            "capex_frantoio_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh886_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 26400.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 10800.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               2112.0)

    def test_prezzo_gas_zero(self):
        bc = mh886_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 10168.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 6382.4)
        self.assertAlmostEqual(bc["van"], 8647.13, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh886_calcola(**_demo_kwargs(capex_irrigazione_eur=0,
                                          capex_frantoio_eur=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh886_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 62436.0)
        self.assertEqual(bc["payback"], 8)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def886\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh886_demo().keys()), lette - set(mh886_demo().keys()))
        self.assertEqual(lette, set(mh886_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc886\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc886\["([^"]+)"\]', src))
        attese = set(mh886_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_post_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 885 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 895)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab886:"), 1)
        self.assertTrue(src.startswith("    # W890"))

    def test_ui_tab886_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab886:"), 1)
        self.assertIn("def mh886_demo(", src_h)
        self.assertIn("def mh886_calcola(", src_h)
        self.assertIn("tab886", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Olivicoltura: irrigazione a goccia + frantoio efficiente + pompa di calore + FV battono irrigazione tradizionale + frantoio tradizionale + riscaldamento a gas?", src)
        self.assertIn("🫒 Olivicoltura: irrigazione a goccia + frantoio efficiente + pompa di calore + FV battono irrigazione tradizionale + frantoio tradizionale + riscaldamento a gas?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        for vecchio in (_VECCHIO_MH, _VECCHIO_MH_TAB):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st886_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st886_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st886_calcola"', src)
        self.assertIn('key="st886_csv"', src)
        self.assertIn('key="st886_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg886"), src.index(".paiac("))
        self.assertLess(src.index("risparmio_eur_anno'] <= 0.0"), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)

    def test_ui_nessun_trattino_lungo(self):
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            self.assertNotIn(chr(8212), src)
            self.assertNotIn(chr(8211), src)

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato).
        import textwrap as _tw
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            if percorso == _UI_PATH:
                src = _tw.dedent(src)
            tree = ast.parse(src)
            for nodo in ast.walk(tree):
                if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                    if nodo.value == "utf-8":
                        continue
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)


if __name__ == "__main__":
    unittest.main()
