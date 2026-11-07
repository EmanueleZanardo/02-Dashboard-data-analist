"""Test nuova scheda elicicoltura:
irrigazione efficiente + ventilazione efficiente +
riscaldamento da pompa di calore + FV battono
irrigazione tradizionale + ventilazione tradizionale +
riscaldamento a gas?
Repo path: tests/test_w887_elicicoltura.py

Business case annuo di una elicicoltura,
guidato dalla SUPERFICIE RECINTI (demo 1000 m2):
irrigazione tradizionale base 1000 x 25 =
25.000 kWh/anno; ventilazione tradizionale
1000 x 10 = 10.000 kWh/anno; elettricita' base
totale 35.000 kWh/anno, costo energia base 7.700
EUR/anno; gas base 1000 x 8 = 8.000 Smc/anno,
costo gas base 7.200 EUR/anno; O&M base 15.000
EUR/anno; costo base 29.900 EUR/anno;
irrigazione efficiente 1000 x 12 = 12.000
kWh/anno; ventilazione efficiente 1000 x 5 = 5.000
kWh/anno; pompa di calore riscaldamento 1000 x 10
= 10.000 kWh/anno; elettricita'
alternativa 27.000 kWh/anno, gas per riscaldamento
ELIMINATO; kWp = sup FV x kwp per m2
(demo 40 kWp); E_pv 44.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 26.400 kWh/anno); immessa 17.600 kWh/anno;
deficit 600 kWh/anno; ricavo immissione 1.408
EUR/anno; O&M alternativa 12.000 EUR/anno; C_alt
10.724 EUR/anno; risparmio 19.176 EUR/anno; CAPEX
12.000 + 8.000 + 18.000 + 40 x 900 = 74.000 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 24,35
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0,15
t/anno (immessa senza credito CO2); CO2 evitata
24,20 t/anno; LCO base 29,90 EUR/m2 e LCO alt
10,724 EUR/m2 (costi operativi annui per
m2, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato
maggiore o uguale a 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno gas_alt)
in forma chiusa (demo None: rapporto negativo meno
1,497, vince anche a gas gratuito), None se il
denominatore e' nullo o negativo o se il rapporto e'
negativo. L'alternativa non usa gas, quindi gas_alt
= 0 e il denominatore e' gas_base.
E' una SOGLIA MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa vince, sotto
perde. Verdetto: NON_CALCOLABILE se input degenere
(superficie minore o uguale a 0, kWh per m2 minori
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
Casi limite: superficie zero non calcolabile
(ValueError negli helper, guard NON_CALCOLABILE in
UI); frazione autoconsumo zero (autoconsumo zero);
prezzo gas zero (ancora calcolabile, risparmio
positivo, VAN positiva: CONVIENTE);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: NON porcilaia (li'
si allevano suini, qui SOLO lumache:
irrigazione + ventilazione + riscaldamento + FV,
NIENTE suini, NIENTE porcilaia), NON pollaio
avicolo (li' si allevano avicoli, qui SOLO lumache,
NIENTE avicoli, NIENTE pollaio), NON stalla bovina
(li' si allevano bovini, qui SOLO lumache, NIENTE
bovini, NIENTE stalla bovina), NON sala mungitura
(li' si munge, qui SOLO lumache, NIENTE latte,
NIENTE mungitura, NIENTE refrigerazione latte),
NON caseificio (li' si trasforma il latte in
formaggio, qui SOLO lumache, NIENTE latte, NIENTE
caseificio), NON vigneto (li' viti da uva, qui
SOLO lumache, NIENTE uva, NIENTE vigneto), NON
frutteto (li' frutta da albero, qui SOLO lumache,
NIENTE frutta, NIENTE frutteto), NON allevamento
ovino (li' ovini e tosatura, qui SOLO lumache,
NIENTE ovini, NIENTE tosatura), NON coniglicoltura
(li' conigli, qui SOLO lumache, NIENTE conigli,
NIENTE coniglicoltura), NON fungaia (li' funghi,
qui SOLO lumache, NIENTE funghi, NIENTE fungaia),
NON vivaio floricolo (li' fiori in vivaio, qui SOLO
lumache, NIENTE vivaio floricolo), NON fioraio (li'
vendita di fiori, qui SOLO lumache, NIENTE
fioraio), NON maneggio (li' cavalli, qui SOLO
lumache, NIENTE cavalli, NIENTE maneggio); qui solo
elicicoltura: irrigazione + ventilazione +
riscaldamento + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w887_helpers import (
        demo_calcoli,
        mh883_c_alt,
        mh883_c_base,
        mh883_calcola,
        mh883_capex_totale,
        mh883_co2_alt,
        mh883_co2_base,
        mh883_co2_evitata,
        mh883_csv,
        mh883_demo,
        mh883_demo_calcoli,
        mh883_e_alt,
        mh883_e_base_totale,
        mh883_e_deficit,
        mh883_e_irrigazione_alt,
        mh883_e_irrigazione_base,
        mh883_e_immessa,
        mh883_e_pdc,
        mh883_e_pv,
        mh883_e_pv_auto,
        mh883_e_ventilazione_alt,
        mh883_e_ventilazione_base,
        mh883_flussi,
        mh883_frazione,
        mh883_gas_base,
        mh883_int_pos,
        mh883_kwp,
        mh883_lco,
        mh883_nneg,
        mh883_num,
        mh883_p_gas_pareggio,
        mh883_payback,
        mh883_pos,
        mh883_ricavo_immissione,
        mh883_risparmio,
        mh883_sensibilita,
        mh883_tir,
        mh883_valida,
        mh883_van,
        mh883_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w887_helpers", os.path.join(_hf, "w887_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh883_c_alt = _mod.mh883_c_alt
    mh883_c_base = _mod.mh883_c_base
    mh883_calcola = _mod.mh883_calcola
    mh883_capex_totale = _mod.mh883_capex_totale
    mh883_co2_alt = _mod.mh883_co2_alt
    mh883_co2_base = _mod.mh883_co2_base
    mh883_co2_evitata = _mod.mh883_co2_evitata
    mh883_csv = _mod.mh883_csv
    mh883_demo = _mod.mh883_demo
    mh883_demo_calcoli = _mod.mh883_demo_calcoli
    mh883_e_alt = _mod.mh883_e_alt
    mh883_e_base_totale = _mod.mh883_e_base_totale
    mh883_e_deficit = _mod.mh883_e_deficit
    mh883_e_irrigazione_alt = _mod.mh883_e_irrigazione_alt
    mh883_e_irrigazione_base = _mod.mh883_e_irrigazione_base
    mh883_e_immessa = _mod.mh883_e_immessa
    mh883_e_pdc = _mod.mh883_e_pdc
    mh883_e_pv = _mod.mh883_e_pv
    mh883_e_pv_auto = _mod.mh883_e_pv_auto
    mh883_e_ventilazione_alt = _mod.mh883_e_ventilazione_alt
    mh883_e_ventilazione_base = _mod.mh883_e_ventilazione_base
    mh883_flussi = _mod.mh883_flussi
    mh883_frazione = _mod.mh883_frazione
    mh883_gas_base = _mod.mh883_gas_base
    mh883_int_pos = _mod.mh883_int_pos
    mh883_kwp = _mod.mh883_kwp
    mh883_lco = _mod.mh883_lco
    mh883_nneg = _mod.mh883_nneg
    mh883_num = _mod.mh883_num
    mh883_p_gas_pareggio = _mod.mh883_p_gas_pareggio
    mh883_payback = _mod.mh883_payback
    mh883_pos = _mod.mh883_pos
    mh883_ricavo_immissione = _mod.mh883_ricavo_immissione
    mh883_risparmio = _mod.mh883_risparmio
    mh883_sensibilita = _mod.mh883_sensibilita
    mh883_tir = _mod.mh883_tir
    mh883_valida = _mod.mh883_valida
    mh883_van = _mod.mh883_van
    mh883_verdetto = _mod.mh883_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w887_helpers.py")
_UI_PATH = _risolvi("w887_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "2"
_VECCHIO_TAB = "tab88" + "2"
_VECCHIO_ST = "st88" + "2_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_irrigazione_base_kwh_anno": 25000.0,
    "e_ventilazione_base_kwh_anno": 10000.0,
    "e_base_kwh_anno": 35000.0,
    "gas_base_smc_anno": 8000.0,
    "c_base_eur_anno": 29900.0,
    "e_irrigazione_alt_kwh_anno": 12000.0,
    "e_ventilazione_alt_kwh_anno": 5000.0,
    "e_pdc_kwh_anno": 10000.0,
    "e_alt_kwh_anno": 27000.0,
    "kwp": 40.0,
    "e_pv_kwh_anno": 44000.0,
    "e_pv_auto_kwh_anno": 26400.0,
    "e_immessa_kwh_anno": 17600.0,
    "e_deficit_kwh_anno": 600.0,
    "ricavo_immissione_eur_anno": 1408.0,
    "c_alt_eur_anno": 10724.0,
    "risparmio_eur_anno": 19176.0,
    "capex_eur": 74000.0,
    "co2_base_t_anno": 24.35,
    "co2_alt_t_anno": 0.15,
    "co2_evitata_t_anno": 24.20,
    "lco_base_eur_m2": 29.90,
    "lco_alt_eur_m2": 10.724,
    "van": 125040.32254015098,
    "tir": 25.001979344774604,
    "payback": 4,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh883_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh883_num(3, "x"), 3.0)
        self.assertEqual(mh883_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh883_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh883_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh883_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh883_pos(0, "x")
        with self.assertRaises(ValueError):
            mh883_pos(-1, "x")
        self.assertEqual(mh883_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh883_int_pos(15, "x"), 15)
        self.assertEqual(mh883_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh883_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh883_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh883_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh883_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh883_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh883_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_irrigazione_ventilazione_base_e_costo_base(self):
        self.assertEqual(mh883_e_irrigazione_base(1000, 25), 25000.0)
        self.assertEqual(mh883_e_ventilazione_base(1000, 10), 10000.0)
        self.assertEqual(mh883_e_base_totale(25000.0, 10000.0), 35000.0)
        self.assertEqual(mh883_gas_base(1000, 8), 8000.0)
        self.assertEqual(mh883_c_base(35000.0, 0.22, 8000.0, 0.90,
                                       15000), 29900.0)

    def test_irrigazione_ventilazione_pdc_somma(self):
        self.assertEqual(mh883_e_irrigazione_alt(1000, 12), 12000.0)
        self.assertEqual(mh883_e_ventilazione_alt(1000, 5), 5000.0)
        self.assertEqual(mh883_e_pdc(1000, 10), 10000.0)
        self.assertEqual(mh883_e_alt(12000.0, 5000.0, 10000.0), 27000.0)
        # L'irrigazione efficiente RIDUCE il consumo di
        # irrigazione, non lo azzera: 12 resta sopra zero
        # anche a parita' di base 25.
        self.assertGreater(mh883_e_irrigazione_alt(1000, 12), 0.0)
        self.assertLess(mh883_e_irrigazione_alt(1000, 12),
                        mh883_e_irrigazione_base(1000, 25))
        # La ventilazione efficiente RIDUCE il consumo di
        # ventilazione, non lo azzera: 5 resta sopra zero
        # anche a parita' di base 10.
        self.assertGreater(mh883_e_ventilazione_alt(1000, 5), 0.0)
        self.assertLess(mh883_e_ventilazione_alt(1000, 5),
                        mh883_e_ventilazione_base(1000, 10))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh883_kwp(200, 0.20), 40.0)
        self.assertEqual(mh883_e_pv(40.0, 1100), 44000.0)
        self.assertEqual(mh883_e_pv_auto(44000.0, 0.60, 27000.0),
                         26400.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh883_e_pv_auto(44000.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh883_e_immessa(44000.0, 26400.0), 17600.0)
        self.assertEqual(mh883_e_deficit(27000.0, 26400.0), 600.0)
        self.assertEqual(mh883_e_deficit(27000.0, 30000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh883_ricavo_immissione(17600.0, 0.08), 1408.0)
        self.assertAlmostEqual(
            mh883_c_alt(600.0, 0.22, 1408.0, 12000.0),
            10724.0)
        self.assertAlmostEqual(mh883_risparmio(29900.0, 10724.0),
                               19176.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh883_capex_totale(12000, 8000, 18000, 40.0,
                                            900),
                         74000.0)
        self.assertEqual(mh883_capex_totale(12000, 8000, 18000, 0.0,
                                            900),
                         38000.0)

    def test_co2_base_e_alt(self):
        cb = mh883_co2_base(8000.0, 1.95, 35000.0, 0.25)
        self.assertAlmostEqual(cb, 24.35, places=4)
        ca = mh883_co2_alt(600.0, 0.25)
        self.assertAlmostEqual(ca, 0.15, places=4)
        self.assertAlmostEqual(mh883_co2_evitata(cb, ca), 24.20, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh883_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh883_lco(29900.0, 1000), 29.90)
        self.assertAlmostEqual(mh883_lco(10724.0, 1000), 10.724)
        with self.assertRaises(ValueError):
            mh883_lco(29900.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh883_flussi(74000, 19176.0, 3),
                         [-74000, 19176.0, 19176.0, 19176.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh883_van([-100, 60, 60], 0), 20.0)
        bc = mh883_demo_calcoli()
        self.assertAlmostEqual(mh883_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh883_demo_calcoli()
        tir = mh883_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh883_tir([-100, -10, -10]))
        self.assertIsNone(mh883_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh883_demo_calcoli()
        self.assertEqual(mh883_payback(bc["flussi"]), 4)
        self.assertIsNone(mh883_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh883_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh883_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:4]), -16472.0, places=2)
        self.assertAlmostEqual(sum(flussi[:5]), 2704.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh883_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh883_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh883_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh883_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh883_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh883_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh883_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh883_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -1.497, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh883_p_gas_pareggio(8000.0, 0.0, 35000.0,
                                 0.22, 15000.0, 50000.0),
            3.4125, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh883_p_gas_pareggio(8000.0, 0.0, 35000.0,
                                              0.22, 15000.0, 22700.0),
                         0.0)
        self.assertIsNone(mh883_p_gas_pareggio(0.0, 0.0, 35000.0,
                                               0.22, 15000.0, 50000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh883_p_gas_pareggio(8000.0, 8000.0, 35000.0,
                                               0.22, 15000.0, 50000.0))
        self.assertIsNone(mh883_p_gas_pareggio(8000.0, 0.0, 35000.0,
                                               0.22, 15000.0, 10724.0))

    def test_valida_demo_ok(self):
        demo = mh883_demo()
        val = mh883_valida(*[demo[k] for k in (
            "superficie_m2", "e_irrigazione_base_per_m2",
            "e_ventilazione_base_per_m2",
            "p_el", "gas_per_m2",
            "p_gas", "om_base_eur_anno",
            "e_irrigazione_alt_per_m2", "e_ventilazione_alt_per_m2",
            "e_pdc_per_m2", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_irrigazione_eur",
            "capex_ventilazione_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_superficie_zero_no(self):
        kw = _demo_kwargs(superficie_m2=0)
        self.assertRaises(ValueError, mh883_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh883_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh883_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh883_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh883_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("superficie_m2", -1),
                              ("e_irrigazione_base_per_m2", -1),
                              ("p_gas", -0.01),
                              ("capex_irrigazione_eur", -1),
                              ("capex_pdc_eur", -1),
                              ("e_ventilazione_base_per_m2", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh883_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh883_calcola(mh883_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh883_calcola(dict(mh883_demo(), capex_irrigazione_eur=99999),
                           capex_irrigazione_eur=12000)
        self.assertEqual(bc["capex_eur"], 74000.0)


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
        self.assertEqual(bc["payback"], 4)

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
            bc["lco_base_eur_m2"],
            bc["c_base_eur_anno"] / bc["superficie_m2"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_m2"],
            bc["c_alt_eur_anno"] / bc["superficie_m2"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh883_sensibilita(**mh883_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               20616.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               139987.03, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               20689.6, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               140750.97, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               11960.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               86140.71, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 4)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 38000.0)
        self.assertAlmostEqual(s["senza_ventilazione_efficiente"]["risparmio_eur_anno"],
                               18076.0, places=2)
        self.assertAlmostEqual(s["senza_ventilazione_efficiente"]["van"],
                               113622.70, places=2)
        self.assertEqual(s["senza_ventilazione_efficiente"]["payback"], 5)
        self.assertEqual(s["senza_ventilazione_efficiente"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               51040.32, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 8)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               74071.99, places=2)
        self.assertEqual(s["vita_10"]["payback"], 4)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               213640.0, places=2)

    def test_marginale_con_capex_irrigazione_alto(self):
        # CAPEX totale 204.000 (irrigazione a 142.000):
        # VAN circa meno 4.959,68, entro la tolleranza del 10%
        # (20.400).
        bc = mh883_calcola(**_demo_kwargs(capex_irrigazione_eur=142000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -4959.68, places=2)

    def test_non_convente_con_capex_irrigazione_altissimo(self):
        bc = mh883_calcola(**_demo_kwargs(capex_irrigazione_eur=180000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -42959.68, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh883_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -68824.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh883_csv(bc, mh883_demo())
        for voce in ("superficie_m2", "e_base_kwh_anno",
                     "e_irrigazione_base_kwh_anno", "e_pdc_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_m2", "lco_alt_eur_m2"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -74000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie recinti (m2)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh883_c_alt(27000.0, 0.22, 0.0, 12000.0)
        con = mh883_c_alt(600.0, 0.22, 1408.0, 12000.0)
        self.assertAlmostEqual(senza - con, 26400.0 * 0.22 + 1408.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh883_sensibilita(**mh883_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_ventilazione_efficiente",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh883_csv(bc, mh883_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh883_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh883_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh883_calcola(**_demo_kwargs(sup_fv_m2=0))
        self.assertEqual(bc["capex_eur"], 38000.0)
        bc = mh883_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_superficie_zero_non_calcolabile(self):
        # Superficie zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(superficie_m2=0)
        self.assertRaises(ValueError, mh883_calcola, **kw)
        self.assertFalse(mh883_valida(*[kw[k] for k in (
            "superficie_m2", "e_irrigazione_base_per_m2",
            "e_ventilazione_base_per_m2",
            "p_el", "gas_per_m2",
            "p_gas", "om_base_eur_anno",
            "e_irrigazione_alt_per_m2", "e_ventilazione_alt_per_m2",
            "e_pdc_per_m2", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_irrigazione_eur",
            "capex_ventilazione_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh883_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 44000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 27000.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               3520.0)

    def test_prezzo_gas_zero(self):
        bc = mh883_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 22700.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 11976.0)
        self.assertAlmostEqual(bc["van"], 50306.78, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh883_calcola(**_demo_kwargs(capex_irrigazione_eur=0,
                                          capex_ventilazione_eur=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh883_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 213640.0)
        self.assertEqual(bc["payback"], 4)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def883\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh883_demo().keys()), lette - set(mh883_demo().keys()))
        self.assertEqual(lette, set(mh883_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc883\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc883\["([^"]+)"\]', src))
        attese = set(mh883_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_post_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 882 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 890)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab883:"), 1)
        self.assertTrue(src.startswith("    # W887"))

    def test_ui_tab883_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab883:"), 1)
        self.assertIn("def mh883_demo(", src_h)
        self.assertIn("def mh883_calcola(", src_h)
        self.assertIn("tab883", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Elicicoltura: irrigazione efficiente + ventilazione efficiente + riscaldamento da pompa di calore + FV battono irrigazione tradizionale + ventilazione tradizionale + riscaldamento a gas?", src)
        self.assertIn("🐌 Elicicoltura: irrigazione efficiente + ventilazione efficiente + riscaldamento da pompa di calore + FV battono irrigazione tradizionale + ventilazione tradizionale + riscaldamento a gas?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        for vecchio in (_VECCHIO_MH,):
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
        chiavi = re.findall(r'key="(st883_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st883_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st883_calcola"', src)
        self.assertIn('key="st883_csv"', src)
        self.assertIn('key="st883_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg883"), src.index(".paiac("))
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
