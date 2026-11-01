"""Test nuova scheda magazzino automatizzato: LED +
sensoristica + trasloelevatori/AGV elettrici +
FV su tetto battono magazzino tradizionale con
illuminazione sempre accesa e carrelli termici?

Business case annuo di un magazzino
automatizzato, guidato da SUPERFICIE (m2),
ORE DI ATTIVITA' (ore/anno) e POSTI PALLET
(che guidano solo il CAPEX di automazione,
non la superficie): E_light_base = sup x
w_light_base / 1000 x ore (demo 720.000
kWh/anno); E_hvac_base = sup x
w_hvac_base / 1000 x ore (demo 300.000
kWh/anno); E_mov_base = n_carrelli x
kwh_carrello (demo 15 x 8.000 = 120.000
kWh/anno, driver ESPLICITO, non una quota
dei posti pallet); domanda base 1.140.000
kWh/anno, costo base 319.200 EUR/anno;
E_led = sup x w_led / 1000 x ore (demo
240.000 kWh/anno); E_hvac_alt =
E_hvac_base x f_hvac_alt (demo 210.000
kWh/anno); automazione elettrica FISSA
(demo 200.000 kWh/anno, NON scalata con i
posti pallet); domanda alt 650.000
kWh/anno; kWp = sup x quota_fv x
kwp_per_m2 (demo 1.200 kWp); E_pv = kWp x
resa (demo 1.320.000 kWh/anno); E_pv_auto
= min(E_pv x f_autoconsumo, domanda alt)
(demo 650.000 kWh/anno, cappata alla
domanda); E_immessa = E_pv - E_pv_auto
(demo 670.000 kWh/anno); E_deficit =
max(0, domanda alt - E_pv_auto) (demo 0);
ricavo immissione = E_immessa x
p_immissione (demo 53.600 EUR/anno);
C_alt = deficit x p_el - ricavo
immissione (demo -53.600 EUR/anno,
ricavo netto); risparmio = C_base - C_alt
(demo 372.800 EUR/anno); CAPEX = sup x
capex_led_m2 + n_pallet x
capex_auto_pallet + kWp x capex_fv
(demo 2.580.000 EUR); CO2 base =
domanda base / 1000 x 0,25 (demo 285,00
t/anno, fattore in t/MWh); CO2 alt =
deficit / 1000 x 0,25 (demo 0, immessa
senza credito CO2); CO2 evitata =
base - alt (segno libero); flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo elettrico di
pareggio p_el_star = (-E_immessa x
p_immissione) / (E_domanda_base -
E_deficit) in forma chiusa (demo None:
rapporto negativo -0,047018, vince anche
a elettricita' gratuita), None se il
denominatore e' nullo o se il rapporto e'
negativo. Con ricavi non negativi il
numeratore non puo' essere positivo: gli
unici casi non-None sono 0,0 (ricavi
nulli). E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (superficie <= 0, ore <= 0,
n_pallet <= 0 o non intero, potenze < 0,
f_hvac_alt/quota_fv/f_autoconsumo < 0 o
> 1, n_carrelli < 0 o non intero,
kwh_carrello < 0, e_automazione < 0,
prezzi < 0, kwp_per_m2 < 0, resa < 0,
voci CAPEX < 0, fattore CO2 < 0, WACC
< 0, vita <= 0 o non intera, tolleranza
< 0) o se risparmio <= 0 (guard degenere:
UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON magazzino
manuale tradizionale (movimentazione a
mano o con carrelli termici senza
automazione: qui il confronto e' proprio
contro quel magazzino), NON centro di
distribuzione con celle frigorifere
(niente fabbisogno frigo in questo
modello, solo HVAC di ambiente chiuso),
NON deposito all'aperto (niente FV su
tetto e niente HVAC di ambiente chiuso).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w867_helpers import (
        demo_calcoli,
        mh863_c_alt,
        mh863_c_base,
        mh863_calcola,
        mh863_capex_totale,
        mh863_co2_alt,
        mh863_co2_base,
        mh863_co2_evitata,
        mh863_csv,
        mh863_demo,
        mh863_demo_calcoli,
        mh863_e_deficit,
        mh863_e_domanda_alt,
        mh863_e_domanda_base,
        mh863_e_hvac_alt,
        mh863_e_hvac_base,
        mh863_e_immessa,
        mh863_e_led,
        mh863_e_light_base,
        mh863_e_mov_base,
        mh863_e_pv,
        mh863_e_pv_auto,
        mh863_flussi,
        mh863_frazione,
        mh863_int_nneg,
        mh863_int_pos,
        mh863_kwp,
        mh863_nneg,
        mh863_num,
        mh863_p_el_pareggio,
        mh863_payback,
        mh863_pos,
        mh863_ricavo_immissione,
        mh863_risparmio,
        mh863_sensibilita,
        mh863_tir,
        mh863_valida,
        mh863_van,
        mh863_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w867_helpers", os.path.join(_hf, "w867_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh863_c_alt = _mod.mh863_c_alt
    mh863_c_base = _mod.mh863_c_base
    mh863_calcola = _mod.mh863_calcola
    mh863_capex_totale = _mod.mh863_capex_totale
    mh863_co2_alt = _mod.mh863_co2_alt
    mh863_co2_base = _mod.mh863_co2_base
    mh863_co2_evitata = _mod.mh863_co2_evitata
    mh863_csv = _mod.mh863_csv
    mh863_demo = _mod.mh863_demo
    mh863_demo_calcoli = _mod.mh863_demo_calcoli
    mh863_e_deficit = _mod.mh863_e_deficit
    mh863_e_domanda_alt = _mod.mh863_e_domanda_alt
    mh863_e_domanda_base = _mod.mh863_e_domanda_base
    mh863_e_hvac_alt = _mod.mh863_e_hvac_alt
    mh863_e_hvac_base = _mod.mh863_e_hvac_base
    mh863_e_immessa = _mod.mh863_e_immessa
    mh863_e_led = _mod.mh863_e_led
    mh863_e_light_base = _mod.mh863_e_light_base
    mh863_e_mov_base = _mod.mh863_e_mov_base
    mh863_e_pv = _mod.mh863_e_pv
    mh863_e_pv_auto = _mod.mh863_e_pv_auto
    mh863_flussi = _mod.mh863_flussi
    mh863_frazione = _mod.mh863_frazione
    mh863_int_nneg = _mod.mh863_int_nneg
    mh863_int_pos = _mod.mh863_int_pos
    mh863_kwp = _mod.mh863_kwp
    mh863_nneg = _mod.mh863_nneg
    mh863_num = _mod.mh863_num
    mh863_p_el_pareggio = _mod.mh863_p_el_pareggio
    mh863_payback = _mod.mh863_payback
    mh863_pos = _mod.mh863_pos
    mh863_ricavo_immissione = _mod.mh863_ricavo_immissione
    mh863_risparmio = _mod.mh863_risparmio
    mh863_sensibilita = _mod.mh863_sensibilita
    mh863_tir = _mod.mh863_tir
    mh863_valida = _mod.mh863_valida
    mh863_van = _mod.mh863_van
    mh863_verdetto = _mod.mh863_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w867_helpers.py")
_UI_PATH = _risolvi("w867_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "2"
_VECCHIO_TAB = "tab86" + "2"
_VECCHIO_ST = "st86" + "2_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "sup_m2": 10000.0,
    "e_light_base_kwh_anno": 720000.0,
    "e_hvac_base_kwh_anno": 300000.0,
    "e_mov_base_kwh_anno": 120000.0,
    "e_domanda_base_kwh_anno": 1140000.0,
    "c_base_eur_anno": 319200.0,
    "e_led_kwh_anno": 240000.0,
    "e_hvac_alt_kwh_anno": 210000.0,
    "e_domanda_alt_kwh_anno": 650000.0,
    "kwp": 1200.0,
    "e_pv_kwh_anno": 1320000.0,
    "e_pv_auto_kwh_anno": 650000.0,
    "e_immessa_kwh_anno": 670000.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_immissione_eur_anno": 53600.0,
    "c_alt_eur_anno": -53600.0,
    "risparmio_eur_anno": 372800.0,
    "capex_eur": 2580000.0,
    "co2_base_t_anno": 285.0,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 285.0,
    "van": 2065912.0156989056,
    "tir": 13.249821115758941,
    "payback": 7,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh863_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh863_num(3, "x"), 3.0)
        self.assertEqual(mh863_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh863_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh863_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh863_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh863_pos(0, "x")
        with self.assertRaises(ValueError):
            mh863_pos(-1, "x")
        self.assertEqual(mh863_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh863_int_pos(8000, "x"), 8000)
        self.assertEqual(mh863_int_pos(8000.0, "x"), 8000)
        with self.assertRaises(ValueError):
            mh863_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh863_int_pos(8000.5, "x")

    def test_int_nneg(self):
        self.assertEqual(mh863_int_nneg(0, "x"), 0)
        self.assertEqual(mh863_int_nneg(15, "x"), 15)
        with self.assertRaises(ValueError):
            mh863_int_nneg(-1, "x")
        with self.assertRaises(ValueError):
            mh863_int_nneg(2.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh863_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh863_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh863_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh863_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_luce_hvac_mov_base_e_domanda_base(self):
        self.assertEqual(mh863_e_light_base(10000, 12, 6000), 720000.0)
        self.assertEqual(mh863_e_hvac_base(10000, 5, 6000), 300000.0)
        self.assertEqual(mh863_e_mov_base(15, 8000), 120000.0)
        # I carrelli sono un driver esplicito, non una quota dei posti pallet.
        self.assertNotEqual(mh863_e_mov_base(15, 8000), 8000 * 0.10 * 8000)
        self.assertEqual(mh863_e_domanda_base(720000.0, 300000.0, 120000.0),
                         1140000.0)
        self.assertAlmostEqual(mh863_c_base(1140000.0, 0.28), 319200.0)

    def test_led_hvac_sensoristica_domanda_alt(self):
        self.assertEqual(mh863_e_led(10000, 4, 6000), 240000.0)
        self.assertEqual(mh863_e_hvac_alt(300000.0, 0.70), 210000.0)
        # L'automazione e' una domanda fissa, non scalata con i posti pallet.
        self.assertEqual(mh863_e_domanda_alt(240000.0, 210000.0, 200000.0),
                         650000.0)
        with self.assertRaises(ValueError):
            mh863_e_hvac_alt(300000.0, 1.1)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh863_kwp(10000, 0.60, 0.20), 1200.0)
        self.assertEqual(mh863_e_pv(1200.0, 1100), 1320000.0)
        self.assertEqual(mh863_e_pv_auto(1320000.0, 0.55, 650000.0),
                         650000.0)
        # Cap alla domanda: autoconsumo non supera la domanda.
        self.assertEqual(mh863_e_pv_auto(1320000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh863_e_immessa(1320000.0, 650000.0), 670000.0)
        self.assertEqual(mh863_e_deficit(650000.0, 650000.0), 0.0)
        self.assertEqual(mh863_e_deficit(20000.0, 25000.0), 0.0)

    def test_c_alt_con_ricavo_immissione(self):
        self.assertEqual(mh863_ricavo_immissione(670000.0, 0.08), 53600.0)
        self.assertAlmostEqual(mh863_c_alt(0.0, 0.28, 53600.0), -53600.0)
        self.assertAlmostEqual(mh863_risparmio(319200.0, -53600.0),
                               372800.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh863_capex_totale(10000, 6, 8000, 150, 1200.0,
                                            1100),
                         2580000.0)
        self.assertEqual(mh863_capex_totale(10000, 6, 8000, 150, 0.0,
                                            1100),
                         1260000.0)

    def test_co2_con_fattore_t_mwh_senza_credito_immessa(self):
        cb = mh863_co2_base(1140000.0, 0.25)
        self.assertAlmostEqual(cb, 285.0, places=4)
        ca = mh863_co2_alt(0.0, 0.25)
        self.assertEqual(ca, 0.0)
        self.assertAlmostEqual(mh863_co2_evitata(cb, ca), 285.0, places=4)
        # L'immessa non sottrae CO2: alt conta solo il deficit.
        self.assertEqual(mh863_co2_alt(0.0, 0.25), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh863_flussi(2580000, 372800.0, 3),
                         [-2580000, 372800.0, 372800.0, 372800.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh863_van([-100, 60, 60], 0), 20.0)
        bc = mh863_demo_calcoli()
        self.assertAlmostEqual(mh863_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh863_demo_calcoli()
        tir = mh863_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh863_tir([-100, -10, -10]))
        self.assertIsNone(mh863_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh863_demo_calcoli()
        self.assertEqual(mh863_payback(bc["flussi"]), 7)
        self.assertIsNone(mh863_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh863_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh863_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:7]), -343200.0, places=2)
        self.assertAlmostEqual(sum(flussi[:8]), 29600.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh863_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh863_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh863_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh863_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh863_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh863_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh863_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_el_pareggio_demo_none_rapporto_negativo(self):
        bc = mh863_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a elettricita' gratuita, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((-bc["e_immessa_kwh_anno"] * bc["p_immissione"])
                        / (bc["e_domanda_base_kwh_anno"]
                           - bc["e_deficit_kwh_anno"]), 0.0)
        self.assertAlmostEqual(
            (-bc["e_immessa_kwh_anno"] * bc["p_immissione"])
            / (bc["e_domanda_base_kwh_anno"]
               - bc["e_deficit_kwh_anno"]), -0.047017543859649125,
            places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_el_pareggio_ricavi_nulli_zero(self):
        # Senza ricavi (immessa nulla) il numeratore e' nullo:
        # pareggio a prezzo zero, non None.
        self.assertEqual(mh863_p_el_pareggio(0.0, 0.08,
                                            1140000.0, 650000.0), 0.0)

    def test_p_el_pareggio_denominatore_nullo_none(self):
        self.assertIsNone(mh863_p_el_pareggio(100.0, 0.08,
                                             500000.0, 500000.0))

    def test_p_el_pareggio_negativo_none(self):
        self.assertIsNone(mh863_p_el_pareggio(670000.0, 0.08,
                                             1140000.0, 0.0))

    def test_valida_demo_ok(self):
        demo = mh863_demo()
        val = mh863_valida(*[demo[k] for k in (
            "sup_m2", "ore_anno", "n_pallet", "w_light_base",
            "w_hvac_base", "n_carrelli", "kwh_carrello", "w_led",
            "f_hvac_alt", "e_automazione", "p_el", "quota_fv",
            "kwp_per_m2", "resa_fv", "f_autoconsumo", "p_immissione",
            "capex_led_m2", "capex_auto_pallet", "capex_fv_eur_kwp",
            "f_co2_el_t_mwh", "wacc_pct", "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_sup_ore_pallet_zero_no(self):
        kw = _demo_kwargs(sup_m2=0)
        self.assertRaises(ValueError, mh863_calcola, **kw)
        kw = _demo_kwargs(ore_anno=0)
        self.assertRaises(ValueError, mh863_calcola, **kw)
        kw = _demo_kwargs(n_pallet=0)
        self.assertRaises(ValueError, mh863_calcola, **kw)

    def test_valida_quote_sopra_uno_no(self):
        kw = _demo_kwargs(f_hvac_alt=1.1)
        self.assertRaises(ValueError, mh863_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh863_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh863_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh863_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh863_calcola, **kw)

    def test_valida_carrelli_non_interi_no(self):
        kw = _demo_kwargs(n_carrelli=2.5)
        self.assertRaises(ValueError, mh863_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh863_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("ore_anno", -1),
                              ("w_light_base", -1),
                              ("p_el", -0.01),
                              ("capex_auto_pallet", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh863_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh863_calcola(mh863_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh863_calcola(dict(mh863_demo(), capex_auto_pallet=999999),
                           capex_auto_pallet=150)
        self.assertEqual(bc["capex_eur"], 2580000.0)


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
        self.assertEqual(bc["payback"], 7)

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
            bc["e_domanda_base_kwh_anno"] * bc["p_el"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["e_immessa_kwh_anno"] * bc["p_immissione"])

    def test_coerenza_p_el_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertLess((-bc["e_immessa_kwh_anno"] * bc["p_immissione"])
                        / (bc["e_domanda_base_kwh_anno"]
                           - bc["e_deficit_kwh_anno"]), 0.0)

    def test_sensibilita_valori(self):
        s = mh863_sensibilita(**mh863_demo())
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               436640.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               2861499.52, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               137200.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               449815.26, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 1260000.0)
        self.assertAlmostEqual(s["hvac_sempre_acceso"]["risparmio_eur_anno"],
                               362800.0, places=2)
        self.assertAlmostEqual(s["hvac_sempre_acceso"]["van"],
                               1941289.91, places=2)
        self.assertEqual(s["hvac_sempre_acceso"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -514087.98, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 14)
        self.assertEqual(s["capex_doppio"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               298662.78, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               4876000.0, places=2)

    def test_marginale_con_capex_fv_alto(self):
        # CAPEX totale 4.860.000 (FV a 3.000 EUR/kWp):
        # VAN circa -214.088, entro la tolleranza del 10%
        # (486.000).
        bc = mh863_calcola(**_demo_kwargs(capex_fv_eur_kwp=3000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -214087.98, places=2)

    def test_non_convente_con_capex_fv_altissimo(self):
        bc = mh863_calcola(**_demo_kwargs(capex_fv_eur_kwp=4000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -1414087.98, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh863_calcola(**_demo_kwargs(quota_fv=0, w_led=12,
                                          f_hvac_alt=1.0))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -22400.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh863_csv(bc, mh863_demo())
        for voce in ("sup_m2", "e_light_base_kwh_anno",
                     "e_domanda_base_kwh_anno", "p_el_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -2580000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie (m2)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh863_c_alt(650000.0, 0.28, 0.0)
        con = mh863_c_alt(0.0, 0.28, 53600.0)
        self.assertAlmostEqual(senza - con, 650000.0 * 0.28 + 53600.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh863_sensibilita(**mh863_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_piu20", "senza_fv",
                          "hvac_sempre_acceso", "capex_doppio",
                          "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh863_csv(bc, mh863_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_light_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh863_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh863_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh863_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["capex_eur"], 1260000.0)
        bc = mh863_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def863\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh863_demo().keys()), lette - set(mh863_demo().keys()))
        self.assertEqual(lette, set(mh863_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc863\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc863\["([^"]+)"\]', src))
        attese = set(mh863_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab863:"), 1)
        self.assertTrue(src.startswith("    # W867"))

    def test_ui_tab863_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab863:"), 1)
        self.assertIn("def mh863_demo(", src_h)
        self.assertIn("def mh863_calcola(", src_h)
        self.assertIn("tab863", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Magazzino automatizzato: LED + sensoristica + trasloelevatori/AGV elettrici + FV su tetto battono magazzino tradizionale con illuminazione sempre accesa e carrelli termici?", src)
        self.assertIn("🤖 Magazzino automatizzato: LED + sensoristica + trasloelevatori/AGV elettrici + FV su tetto battono magazzino tradizionale con illuminazione sempre accesa e carrelli termici?", src)
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
        chiavi = re.findall(r'key="(st863_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st863_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st863_calcola"', src)
        self.assertIn('key="st863_csv"', src)
        self.assertIn('key="st863_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg863"), src.index(".paiac("))
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
            self.assertNotIn("—", src)
            self.assertNotIn("–", src)


if __name__ == "__main__":
    unittest.main()
