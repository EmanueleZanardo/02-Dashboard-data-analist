"""Test nuova scheda sericoltura:
ventilazione efficiente + illuminazione LED +
riscaldamento da pompa di calore + FV battono
ventilazione tradizionale + illuminazione
tradizionale + riscaldamento a gas?
Repo path: tests/test_w888_sericoltura.py

Business case annuo di una sericoltura,
guidato dalla SUPERFICIE SALE DI ALLEVAMENTO
(demo 500 m2):
ventilazione tradizionale base 500 x 18 =
9.000 kWh/anno; illuminazione tradizionale
500 x 12 = 6.000 kWh/anno; elettricita' base
totale 15.000 kWh/anno, costo energia base 3.300
EUR/anno; gas base 500 x 10 = 5.000 Smc/anno,
costo gas base 4.500 EUR/anno; O&M base 8.000
EUR/anno; costo base 15.800 EUR/anno;
ventilazione efficiente 500 x 8 = 4.000
kWh/anno; illuminazione LED 500 x 4 = 2.000
kWh/anno; pompa di calore riscaldamento 500 x 12
= 6.000 kWh/anno; elettricita'
alternativa 12.000 kWh/anno, gas per riscaldamento
ELIMINATO; kWp = sup FV x kwp per m2
(demo 20 kWp); E_pv 22.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 11.000 kWh/anno); immessa 11.000 kWh/anno;
deficit 1.000 kWh/anno; ricavo immissione 880
EUR/anno; O&M alternativa 6.000 EUR/anno; C_alt
5.340 EUR/anno; risparmio 10.460 EUR/anno; CAPEX
6.000 + 4.000 + 10.000 + 20 x 900 = 38.000 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 13,50
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0,25
t/anno (immessa senza credito CO2); CO2 evitata
13,25 t/anno; LCO base 31,60 EUR/m2 e LCO alt
10,68 EUR/m2 (costi operativi annui per
m2, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato
maggiore o uguale a 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno gas_alt)
in forma chiusa (demo None: rapporto negativo meno
1,192, vince anche a gas gratuito), None se il
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
Distinzione esplicita: NON acquacoltura (li'
si allevano pesci, qui SOLO bachi da seta:
ventilazione + illuminazione + riscaldamento + FV,
NIENTE pesci, NIENTE acquacoltura), NON elicicoltura
(li' si allevano lumache, qui SOLO bachi da seta,
NIENTE lumache, NIENTE elicicoltura), NON porcilaia
(li' si allevano suini, qui SOLO bachi da seta,
NIENTE suini, NIENTE porcilaia), NON pollaio
avicolo (li' si allevano avicoli, qui SOLO bachi da
seta, NIENTE avicoli, NIENTE pollaio), NON stalla
bovina (li' si allevano bovini, qui SOLO bachi da
seta, NIENTE bovini, NIENTE stalla bovina), NON sala
mungitura (li' si munge, qui SOLO bachi da seta,
NIENTE latte, NIENTE mungitura, NIENTE
refrigerazione latte), NON caseificio (li' si
trasforma il latte in formaggio, qui SOLO bachi da
seta, NIENTE latte, NIENTE caseificio), NON vigneto
(li' viti da uva, qui SOLO bachi da seta, NIENTE
uva, NIENTE vigneto), NON frutteto (li' frutta da
albero, qui SOLO bachi da seta, NIENTE frutta,
NIENTE frutteto), NON allevamento ovino (li' ovini e
tosatura, qui SOLO bachi da seta, NIENTE ovini,
NIENTE tosatura), NON coniglicoltura (li' conigli,
qui SOLO bachi da seta, NIENTE conigli, NIENTE
coniglicoltura), NON fungaia (li' funghi, qui SOLO
bachi da seta, NIENTE funghi, NIENTE fungaia),
NON vivaio floricolo (li' fiori in vivaio, qui SOLO
bachi da seta, NIENTE vivaio floricolo), NON fioraio
(li' vendita di fiori, qui SOLO bachi da seta,
NIENTE fioraio), NON maneggio (li' cavalli, qui SOLO
bachi da seta, NIENTE cavalli, NIENTE maneggio); qui
solo sericoltura: ventilazione + illuminazione +
riscaldamento + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w888_helpers import (
        demo_calcoli,
        mh884_c_alt,
        mh884_c_base,
        mh884_calcola,
        mh884_capex_totale,
        mh884_co2_alt,
        mh884_co2_base,
        mh884_co2_evitata,
        mh884_csv,
        mh884_demo,
        mh884_demo_calcoli,
        mh884_e_alt,
        mh884_e_base_totale,
        mh884_e_deficit,
        mh884_e_ventilazione_alt,
        mh884_e_ventilazione_base,
        mh884_e_immessa,
        mh884_e_pdc,
        mh884_e_pv,
        mh884_e_pv_auto,
        mh884_e_illuminazione_alt,
        mh884_e_illuminazione_base,
        mh884_flussi,
        mh884_frazione,
        mh884_gas_base,
        mh884_int_pos,
        mh884_kwp,
        mh884_lco,
        mh884_nneg,
        mh884_num,
        mh884_p_gas_pareggio,
        mh884_payback,
        mh884_pos,
        mh884_ricavo_immissione,
        mh884_risparmio,
        mh884_sensibilita,
        mh884_tir,
        mh884_valida,
        mh884_van,
        mh884_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w888_helpers", os.path.join(_hf, "w888_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh884_c_alt = _mod.mh884_c_alt
    mh884_c_base = _mod.mh884_c_base
    mh884_calcola = _mod.mh884_calcola
    mh884_capex_totale = _mod.mh884_capex_totale
    mh884_co2_alt = _mod.mh884_co2_alt
    mh884_co2_base = _mod.mh884_co2_base
    mh884_co2_evitata = _mod.mh884_co2_evitata
    mh884_csv = _mod.mh884_csv
    mh884_demo = _mod.mh884_demo
    mh884_demo_calcoli = _mod.mh884_demo_calcoli
    mh884_e_alt = _mod.mh884_e_alt
    mh884_e_base_totale = _mod.mh884_e_base_totale
    mh884_e_deficit = _mod.mh884_e_deficit
    mh884_e_ventilazione_alt = _mod.mh884_e_ventilazione_alt
    mh884_e_ventilazione_base = _mod.mh884_e_ventilazione_base
    mh884_e_immessa = _mod.mh884_e_immessa
    mh884_e_pdc = _mod.mh884_e_pdc
    mh884_e_pv = _mod.mh884_e_pv
    mh884_e_pv_auto = _mod.mh884_e_pv_auto
    mh884_e_illuminazione_alt = _mod.mh884_e_illuminazione_alt
    mh884_e_illuminazione_base = _mod.mh884_e_illuminazione_base
    mh884_flussi = _mod.mh884_flussi
    mh884_frazione = _mod.mh884_frazione
    mh884_gas_base = _mod.mh884_gas_base
    mh884_int_pos = _mod.mh884_int_pos
    mh884_kwp = _mod.mh884_kwp
    mh884_lco = _mod.mh884_lco
    mh884_nneg = _mod.mh884_nneg
    mh884_num = _mod.mh884_num
    mh884_p_gas_pareggio = _mod.mh884_p_gas_pareggio
    mh884_payback = _mod.mh884_payback
    mh884_pos = _mod.mh884_pos
    mh884_ricavo_immissione = _mod.mh884_ricavo_immissione
    mh884_risparmio = _mod.mh884_risparmio
    mh884_sensibilita = _mod.mh884_sensibilita
    mh884_tir = _mod.mh884_tir
    mh884_valida = _mod.mh884_valida
    mh884_van = _mod.mh884_van
    mh884_verdetto = _mod.mh884_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w888_helpers.py")
_UI_PATH = _risolvi("w888_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "3"
_VECCHIO_TAB = "tab88" + "3"
_VECCHIO_ST = "st88" + "3_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_ventilazione_base_kwh_anno": 9000.0,
    "e_illuminazione_base_kwh_anno": 6000.0,
    "e_base_kwh_anno": 15000.0,
    "gas_base_smc_anno": 5000.0,
    "c_base_eur_anno": 15800.0,
    "e_ventilazione_alt_kwh_anno": 4000.0,
    "e_illuminazione_alt_kwh_anno": 2000.0,
    "e_pdc_kwh_anno": 6000.0,
    "e_alt_kwh_anno": 12000.0,
    "kwp": 20.0,
    "e_pv_kwh_anno": 22000.0,
    "e_pv_auto_kwh_anno": 11000.0,
    "e_immessa_kwh_anno": 11000.0,
    "e_deficit_kwh_anno": 1000.0,
    "ricavo_immissione_eur_anno": 880.0,
    "c_alt_eur_anno": 5340.0,
    "risparmio_eur_anno": 10460.0,
    "capex_eur": 38000.0,
    "co2_base_t_anno": 13.50,
    "co2_alt_t_anno": 0.25,
    "co2_evitata_t_anno": 13.25,
    "lco_base_eur_m2": 31.60,
    "lco_alt_eur_m2": 10.68,
    "van": 70571.22307936897,
    "tir": 26.73910997466549,
    "payback": 4,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh884_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh884_num(3, "x"), 3.0)
        self.assertEqual(mh884_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh884_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh884_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh884_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh884_pos(0, "x")
        with self.assertRaises(ValueError):
            mh884_pos(-1, "x")
        self.assertEqual(mh884_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh884_int_pos(15, "x"), 15)
        self.assertEqual(mh884_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh884_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh884_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh884_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh884_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh884_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh884_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_ventilazione_illuminazione_base_e_costo_base(self):
        self.assertEqual(mh884_e_ventilazione_base(500, 18), 9000.0)
        self.assertEqual(mh884_e_illuminazione_base(500, 12), 6000.0)
        self.assertEqual(mh884_e_base_totale(9000.0, 6000.0), 15000.0)
        self.assertEqual(mh884_gas_base(500, 10), 5000.0)
        self.assertEqual(mh884_c_base(15000.0, 0.22, 5000.0, 0.90,
                                       8000), 15800.0)

    def test_ventilazione_illuminazione_pdc_somma(self):
        self.assertEqual(mh884_e_ventilazione_alt(500, 8), 4000.0)
        self.assertEqual(mh884_e_illuminazione_alt(500, 4), 2000.0)
        self.assertEqual(mh884_e_pdc(500, 12), 6000.0)
        self.assertEqual(mh884_e_alt(4000.0, 2000.0, 6000.0), 12000.0)
        # La ventilazione efficiente RIDUCE il consumo di
        # ventilazione, non lo azzera: 8 resta sopra zero
        # anche a parita' di base 18.
        self.assertGreater(mh884_e_ventilazione_alt(500, 8), 0.0)
        self.assertLess(mh884_e_ventilazione_alt(500, 8),
                        mh884_e_ventilazione_base(500, 18))
        # L'illuminazione LED RIDUCE il consumo di
        # illuminazione, non lo azzera: 4 resta sopra zero
        # anche a parita' di base 12.
        self.assertGreater(mh884_e_illuminazione_alt(500, 4), 0.0)
        self.assertLess(mh884_e_illuminazione_alt(500, 4),
                        mh884_e_illuminazione_base(500, 12))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh884_kwp(100, 0.20), 20.0)
        self.assertEqual(mh884_e_pv(20.0, 1100), 22000.0)
        self.assertEqual(mh884_e_pv_auto(22000.0, 0.50, 12000.0),
                         11000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh884_e_pv_auto(22000.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh884_e_immessa(22000.0, 11000.0), 11000.0)
        self.assertEqual(mh884_e_deficit(12000.0, 11000.0), 1000.0)
        self.assertEqual(mh884_e_deficit(12000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh884_ricavo_immissione(11000.0, 0.08), 880.0)
        self.assertAlmostEqual(
            mh884_c_alt(1000.0, 0.22, 880.0, 6000.0),
            5340.0)
        self.assertAlmostEqual(mh884_risparmio(15800.0, 5340.0),
                               10460.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh884_capex_totale(6000, 4000, 10000, 20.0,
                                            900),
                         38000.0)
        self.assertEqual(mh884_capex_totale(6000, 4000, 10000, 0.0,
                                            900),
                         20000.0)

    def test_co2_base_e_alt(self):
        cb = mh884_co2_base(5000.0, 1.95, 15000.0, 0.25)
        self.assertAlmostEqual(cb, 13.50, places=4)
        ca = mh884_co2_alt(1000.0, 0.25)
        self.assertAlmostEqual(ca, 0.25, places=4)
        self.assertAlmostEqual(mh884_co2_evitata(cb, ca), 13.25, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh884_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh884_lco(15800.0, 500), 31.60)
        self.assertAlmostEqual(mh884_lco(5340.0, 500), 10.68)
        with self.assertRaises(ValueError):
            mh884_lco(15800.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh884_flussi(38000, 10460.0, 3),
                         [-38000, 10460.0, 10460.0, 10460.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh884_van([-100, 60, 60], 0), 20.0)
        bc = mh884_demo_calcoli()
        self.assertAlmostEqual(mh884_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh884_demo_calcoli()
        tir = mh884_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh884_tir([-100, -10, -10]))
        self.assertIsNone(mh884_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh884_demo_calcoli()
        self.assertEqual(mh884_payback(bc["flussi"]), 4)
        self.assertIsNone(mh884_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh884_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh884_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:4]), -6620.0, places=2)
        self.assertAlmostEqual(sum(flussi[:5]), 3840.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh884_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh884_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh884_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh884_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh884_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh884_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh884_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh884_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -1.192, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh884_p_gas_pareggio(5000.0, 0.0, 15000.0,
                                 0.22, 8000.0, 50000.0),
            7.74, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh884_p_gas_pareggio(5000.0, 0.0, 15000.0,
                                              0.22, 8000.0, 11300.0),
                         0.0)
        self.assertIsNone(mh884_p_gas_pareggio(0.0, 0.0, 15000.0,
                                               0.22, 8000.0, 50000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh884_p_gas_pareggio(5000.0, 5000.0, 15000.0,
                                               0.22, 8000.0, 50000.0))
        self.assertIsNone(mh884_p_gas_pareggio(5000.0, 0.0, 15000.0,
                                               0.22, 8000.0, 5340.0))

    def test_valida_demo_ok(self):
        demo = mh884_demo()
        val = mh884_valida(*[demo[k] for k in (
            "superficie_m2", "e_ventilazione_base_per_m2",
            "e_illuminazione_base_per_m2",
            "p_el", "gas_per_m2",
            "p_gas", "om_base_eur_anno",
            "e_ventilazione_alt_per_m2", "e_illuminazione_alt_per_m2",
            "e_pdc_per_m2", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_ventilazione_eur",
            "capex_illuminazione_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_superficie_zero_no(self):
        kw = _demo_kwargs(superficie_m2=0)
        self.assertRaises(ValueError, mh884_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh884_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh884_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh884_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh884_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("superficie_m2", -1),
                              ("e_ventilazione_base_per_m2", -1),
                              ("p_gas", -0.01),
                              ("capex_ventilazione_eur", -1),
                              ("capex_pdc_eur", -1),
                              ("e_illuminazione_base_per_m2", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh884_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh884_calcola(mh884_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh884_calcola(dict(mh884_demo(), capex_ventilazione_eur=99999),
                           capex_ventilazione_eur=6000)
        self.assertEqual(bc["capex_eur"], 38000.0)


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
        s = mh884_sensibilita(**mh884_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               11360.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               79912.92, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               11076.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               76965.09, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               7160.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               54318.35, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 3)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 20000.0)
        self.assertAlmostEqual(s["senza_ventilazione_efficiente"]["risparmio_eur_anno"],
                               9360.0, places=2)
        self.assertAlmostEqual(s["senza_ventilazione_efficiente"]["van"],
                               59153.60, places=2)
        self.assertEqual(s["senza_ventilazione_efficiente"]["payback"], 5)
        self.assertEqual(s["senza_ventilazione_efficiente"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               32571.22, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 8)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               42769.35, places=2)
        self.assertEqual(s["vita_10"]["payback"], 4)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               118900.0, places=2)

    def test_marginale_con_capex_ventilazione_alto(self):
        # CAPEX totale 113.000 (ventilazione a 81.000):
        # VAN circa meno 4.428,78, entro la tolleranza del 10%
        # (11.300).
        bc = mh884_calcola(**_demo_kwargs(capex_ventilazione_eur=81000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -4428.78, places=2)

    def test_non_convente_con_capex_ventilazione_altissimo(self):
        bc = mh884_calcola(**_demo_kwargs(capex_ventilazione_eur=106000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -29428.78, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh884_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -83540.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh884_csv(bc, mh884_demo())
        for voce in ("superficie_m2", "e_base_kwh_anno",
                     "e_ventilazione_base_kwh_anno", "e_pdc_kwh_anno",
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
                         -38000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie sale di allevamento (m2)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh884_c_alt(12000.0, 0.22, 0.0, 6000.0)
        con = mh884_c_alt(1000.0, 0.22, 880.0, 6000.0)
        self.assertAlmostEqual(senza - con, 11000.0 * 0.22 + 880.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh884_sensibilita(**mh884_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_ventilazione_efficiente",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh884_csv(bc, mh884_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh884_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh884_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh884_calcola(**_demo_kwargs(sup_fv_m2=0))
        self.assertEqual(bc["capex_eur"], 20000.0)
        bc = mh884_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_superficie_zero_non_calcolabile(self):
        # Superficie zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(superficie_m2=0)
        self.assertRaises(ValueError, mh884_calcola, **kw)
        self.assertFalse(mh884_valida(*[kw[k] for k in (
            "superficie_m2", "e_ventilazione_base_per_m2",
            "e_illuminazione_base_per_m2",
            "p_el", "gas_per_m2",
            "p_gas", "om_base_eur_anno",
            "e_ventilazione_alt_per_m2", "e_illuminazione_alt_per_m2",
            "e_pdc_per_m2", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_ventilazione_eur",
            "capex_illuminazione_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh884_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 22000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 12000.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               1760.0)

    def test_prezzo_gas_zero(self):
        bc = mh884_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 11300.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 5960.0)
        self.assertAlmostEqual(bc["van"], 23862.76, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh884_calcola(**_demo_kwargs(capex_ventilazione_eur=0,
                                          capex_illuminazione_eur=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh884_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 118900.0)
        self.assertEqual(bc["payback"], 4)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def884\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh884_demo().keys()), lette - set(mh884_demo().keys()))
        self.assertEqual(lette, set(mh884_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc884\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc884\["([^"]+)"\]', src))
        attese = set(mh884_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_post_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 883 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 896)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab884:"), 1)
        self.assertTrue(src.startswith("    # W888"))

    def test_ui_tab884_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab884:"), 1)
        self.assertIn("def mh884_demo(", src_h)
        self.assertIn("def mh884_calcola(", src_h)
        self.assertIn("tab884", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Sericoltura: ventilazione efficiente + illuminazione LED + riscaldamento da pompa di calore + FV battono ventilazione tradizionale + illuminazione tradizionale + riscaldamento a gas?", src)
        self.assertIn("🐛 Sericoltura: ventilazione efficiente + illuminazione LED + riscaldamento da pompa di calore + FV battono ventilazione tradizionale + illuminazione tradizionale + riscaldamento a gas?", src)
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
        chiavi = re.findall(r'key="(st884_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st884_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st884_calcola"', src)
        self.assertIn('key="st884_csv"', src)
        self.assertIn('key="st884_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg884"), src.index(".paiac("))
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
