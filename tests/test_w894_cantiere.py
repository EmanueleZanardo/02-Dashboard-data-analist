"""Test nuova scheda cantiere edile:
gruppo elettrogeno diesel + riscaldamento a
gasolio battono allaccio rete + batteria +
FV + pompa di calore + LED?
Repo path: tests/test_w894_cantiere_edile.py

Business case annuo di un cantiere edile
temporaneo, guidato dalla DURATA DEL
CANTIERE IN MESI (demo 60 mesi = 5 anni)
e dal CONSUMO ELETTRICO MENSILE (demo
12000 kWh/mese):
anni = 60 diviso 12 = 5; E_anno = 12000 x 12
= 144000 kWh/anno; E_ill_anno = 2000 x 12 =
24000 kWh/anno; Q_term_anno = 300 x 60 x 8 =
144000 kWh termici/anno; diesel elettrico =
144000 x 0,28 = 40320,00 l/anno; diesel
termico = 144000 diviso 0,85 x 0,10 =
16941,18 l/anno; diesel totale 57261,18
l/anno; costo base 57261,18 x 1,70 =
97344,00 EUR/anno (senza O&M base); E_hp =
144000 diviso 3,0 = 48000 kWh/anno;
illuminazione alternativa = 24000 x (1 meno
0,50) = 12000 kWh/anno; E_FV = 50 x 1100 x
0,80 = 44000 kWh/anno; E_rete = 144000 meno
24000 piu 12000 piu 48000 meno 44000 =
136000 kWh/anno; costo alternativo = 136000
x 0,25 piu 3000 = 37000,00 EUR/anno;
risparmio 60344,00 EUR/anno; CAPEX 15000 +
45000 + 55000 + 20000 + 5000 = 140000 EUR
(somma verificata a mano); CO2 base =
57261,18 x 2,68 / 1000 = 153,46 t/anno; CO2
alt = 136000 x 0,35 / 1000 = 47,60 t/anno;
CO2 evitata 105,86 t/anno; costo mese base
97344,00 diviso 12 = 8112,00 EUR/mese e
costo mese alt 37000,00 diviso 12 = 3083,33
EUR/mese (costi operativi annui divisi per
12, CAPEX escluso); flussi [CAPEX negativo,
risparmio x vita]; VAN al tasso (FRAZIONE in
ingresso, 0,05 = 5 %, usato diretto, NON
diviso per 100); TIR per bisezione su
intervallo da meno 0,9 a 5,0; payback (primo
anno con cumulato maggiore o uguale a 0).
Tolleranza in PERCENTUALE (10 = 10 % del
CAPEX). La batteria serve per i picchi e
per l'autoconsumo (gia riflesso nello 0,80):
NON cambia il bilancio energetico annuo.
Verdetto: NON_CALCOLABILE se input degenere
(durata nulla o negativa o non multipla di
12, consumi mensili negativi, superficie
negativa, q_risc negativo, mesi
riscaldamento negativi o sopra 12 o non
interi, consumo specifico negativo, eta
caldaia nulla o negativa, litri per kWh
termico negativi, prezzo gasolio negativo,
fattore CO2 gasolio negativo, COP nullo o
negativo, risparmio LED sotto 0 o sopra 1,
potenza FV negativa, resa FV negativa,
autoconsumo FV sotto 0 o sopra 1, prezzo
rete negativo, O&M alternativa negativa,
fattore CO2 rete negativo, voci CAPEX
negative, tasso negativo, tolleranza
negativa) o se risparmio minore o uguale a
0 (guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN
maggiore di 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: durata zero o non multipla di 12
non calcolabile (ValueError negli helper,
guard NON_CALCOLABILE in UI); mesi
riscaldamento zero (fabbisogno termico zero,
E_hp zero, diesel termico zero); FV grande
(energia da rete a zero, mai negativa);
prezzo gasolio zero (costo base zero,
risparmio meno 37000,00, NON_CALCOLABILE);
autoconsumo FV zero (E_FV zero); CAPEX zero
(TIR non definita, payback 0); tasso zero
(VAN uguale alla somma dei flussi).
Distinzione esplicita: qui SOLO energia di
un cantiere edile temporaneo (elettricita
per gru e utensili e illuminazione e
baracche piu riscaldamento delle baracche
piu FV temporaneo piu batteria per picchi),
NIENTE backup e NIENTE anti blackout
(tab262), NIENTE impianto di betonaggio,
NIENTE asfalto, NIENTE segheria, NIENTE
edifici permanenti, NIENTE altri settori;
qui solo cantiere edile temporaneo: genset
diesel e gasolio contro rete e batteria e
FV e pompa di calore e LED.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w894_helpers import (
        demo_calcoli,
        mh889_anni,
        mh889_c_alt,
        mh889_c_base,
        mh889_calcola,
        mh889_capex_totale,
        mh889_co2_alt,
        mh889_co2_base,
        mh889_co2_evitata,
        mh889_costo_mese,
        mh889_csv,
        mh889_demo,
        mh889_demo_calcoli,
        mh889_diesel_el,
        mh889_diesel_term,
        mh889_diesel_tot,
        mh889_durata_mesi,
        mh889_e_anno,
        mh889_e_fv,
        mh889_e_hp,
        mh889_e_ill_alt,
        mh889_e_ill_anno,
        mh889_e_rete,
        mh889_flussi,
        mh889_frazione,
        mh889_int_pos,
        mh889_mesi_risc_anno,
        mh889_nneg,
        mh889_num,
        mh889_payback,
        mh889_pos,
        mh889_q_term_anno,
        mh889_risparmio,
        mh889_sensibilita,
        mh889_tir,
        mh889_valida,
        mh889_van,
        mh889_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w894_helpers", os.path.join(_hf, "w894_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh889_anni = _mod.mh889_anni
    mh889_c_alt = _mod.mh889_c_alt
    mh889_c_base = _mod.mh889_c_base
    mh889_calcola = _mod.mh889_calcola
    mh889_capex_totale = _mod.mh889_capex_totale
    mh889_co2_alt = _mod.mh889_co2_alt
    mh889_co2_base = _mod.mh889_co2_base
    mh889_co2_evitata = _mod.mh889_co2_evitata
    mh889_costo_mese = _mod.mh889_costo_mese
    mh889_csv = _mod.mh889_csv
    mh889_demo = _mod.mh889_demo
    mh889_demo_calcoli = _mod.mh889_demo_calcoli
    mh889_diesel_el = _mod.mh889_diesel_el
    mh889_diesel_term = _mod.mh889_diesel_term
    mh889_diesel_tot = _mod.mh889_diesel_tot
    mh889_durata_mesi = _mod.mh889_durata_mesi
    mh889_e_anno = _mod.mh889_e_anno
    mh889_e_fv = _mod.mh889_e_fv
    mh889_e_hp = _mod.mh889_e_hp
    mh889_e_ill_alt = _mod.mh889_e_ill_alt
    mh889_e_ill_anno = _mod.mh889_e_ill_anno
    mh889_e_rete = _mod.mh889_e_rete
    mh889_flussi = _mod.mh889_flussi
    mh889_frazione = _mod.mh889_frazione
    mh889_int_pos = _mod.mh889_int_pos
    mh889_mesi_risc_anno = _mod.mh889_mesi_risc_anno
    mh889_nneg = _mod.mh889_nneg
    mh889_num = _mod.mh889_num
    mh889_payback = _mod.mh889_payback
    mh889_pos = _mod.mh889_pos
    mh889_q_term_anno = _mod.mh889_q_term_anno
    mh889_risparmio = _mod.mh889_risparmio
    mh889_sensibilita = _mod.mh889_sensibilita
    mh889_tir = _mod.mh889_tir
    mh889_valida = _mod.mh889_valida
    mh889_van = _mod.mh889_van
    mh889_verdetto = _mod.mh889_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w894_helpers.py")
_UI_PATH = _risolvi("w894_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "8"
_VECCHIO_TAB = "tab88" + "8"
_VECCHIO_ST = "st88" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "anni": 5,
    "e_anno_kwh": 144000.0,
    "e_ill_anno_kwh": 24000.0,
    "q_term_anno_kwh": 144000.0,
    "diesel_el_l_anno": 40320.00000000001,
    "diesel_term_l_anno": 16941.176470588234,
    "diesel_tot_l_anno": 57261.17647058824,
    "e_hp_kwh_anno": 48000.0,
    "e_ill_alt_kwh_anno": 12000.0,
    "e_fv_kwh_anno": 44000.0,
    "e_rete_kwh_anno": 136000.0,
    "c_base_eur_anno": 97344.0,
    "c_alt_eur_anno": 37000.0,
    "risparmio_eur_anno": 60344.0,
    "capex_eur": 140000.0,
    "co2_base_t_anno": 153.45995294117648,
    "co2_alt_t_anno": 47.6,
    "co2_evitata_t_anno": 105.85995294117649,
    "costo_mese_base_eur": 8112.0,
    "costo_mese_alt_eur": 3083.3333333333335,
    "van": 121257.94021254612,
    "tir": 32.58071055693163,
    "payback": 3,
}


def _demo_kwargs(**over):
    kw = dict(mh889_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh889_num(3, "x"), 3.0)
        self.assertEqual(mh889_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh889_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh889_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh889_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh889_pos(0, "x")
        with self.assertRaises(ValueError):
            mh889_pos(-1, "x")
        self.assertEqual(mh889_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh889_int_pos(60, "x"), 60)
        self.assertEqual(mh889_int_pos(60.0, "x"), 60)
        with self.assertRaises(ValueError):
            mh889_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh889_int_pos(60.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh889_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh889_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh889_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh889_frazione(1.1, "x")

    def test_durata_mesi_multipla_di_dodici(self):
        self.assertEqual(mh889_durata_mesi(60, "x"), 60)
        self.assertEqual(mh889_durata_mesi(12, "x"), 12)
        self.assertEqual(mh889_durata_mesi(120, "x"), 120)
        with self.assertRaises(ValueError):
            mh889_durata_mesi(50, "x")
        with self.assertRaises(ValueError):
            mh889_durata_mesi(0, "x")
        with self.assertRaises(ValueError):
            mh889_durata_mesi(60.5, "x")

    def test_mesi_risc_intervallo(self):
        self.assertEqual(mh889_mesi_risc_anno(8, "x"), 8)
        self.assertEqual(mh889_mesi_risc_anno(0, "x"), 0)
        self.assertEqual(mh889_mesi_risc_anno(12, "x"), 12)
        with self.assertRaises(ValueError):
            mh889_mesi_risc_anno(13, "x")
        with self.assertRaises(ValueError):
            mh889_mesi_risc_anno(-1, "x")
        with self.assertRaises(ValueError):
            mh889_mesi_risc_anno(8.5, "x")


class TestFisica(unittest.TestCase):
    def test_anni_e_annualizzazione(self):
        self.assertEqual(mh889_anni(60), 5)
        self.assertEqual(mh889_anni(36), 3)
        self.assertEqual(mh889_e_anno(12000), 144000.0)
        self.assertEqual(mh889_e_ill_anno(2000), 24000.0)
        self.assertEqual(mh889_q_term_anno(300, 60, 8), 144000.0)

    def test_diesel_el_term_tot(self):
        self.assertAlmostEqual(mh889_diesel_el(144000.0, 0.28),
                               40320.00, places=2)
        self.assertAlmostEqual(
            mh889_diesel_term(144000.0, 0.85, 0.10),
            16941.18, places=2)
        self.assertAlmostEqual(
            mh889_diesel_tot(40320.0, 16941.176470588234),
            57261.18, places=2)
        with self.assertRaises(ValueError):
            mh889_diesel_term(144000.0, 0, 0.10)

    def test_pompa_converte_non_azzera(self):
        # La pompa di calore converte il
        # riscaldamento in elettricita', non lo
        # azzera: E_hp resta sopra zero e sotto
        # il fabbisogno termico.
        self.assertGreater(mh889_e_hp(144000.0, 3.0), 0.0)
        self.assertLess(mh889_e_hp(144000.0, 3.0), 144000.0)
        self.assertAlmostEqual(mh889_e_hp(144000.0, 3.0), 48000.0,
                               places=2)
        with self.assertRaises(ValueError):
            mh889_e_hp(144000.0, 0)

    def test_led_riducono_non_azzerano(self):
        # I LED RIDUCONO l'illuminazione, non
        # l'azzerano: 12000 resta sopra zero e
        # sotto i 24000 di partenza.
        self.assertAlmostEqual(mh889_e_ill_alt(24000.0, 0.50),
                               12000.0, places=2)
        self.assertGreater(mh889_e_ill_alt(24000.0, 0.50), 0.0)
        self.assertLess(mh889_e_ill_alt(24000.0, 0.50), 24000.0)
        self.assertEqual(mh889_e_ill_alt(24000.0, 0.0), 24000.0)
        self.assertEqual(mh889_e_ill_alt(24000.0, 1.0), 0.0)

    def test_fv_e_rete(self):
        self.assertEqual(mh889_e_fv(50, 1100, 0.80), 44000.0)
        self.assertAlmostEqual(
            mh889_e_rete(144000.0, 24000.0, 12000.0, 48000.0,
                         44000.0),
            136000.0, places=2)
        # L'energia da rete non scende mai sotto
        # zero: con FV enorme il max con 0
        # scatta e la rete e zero.
        self.assertEqual(
            mh889_e_rete(144000.0, 24000.0, 12000.0, 48000.0,
                         440000.0),
            0.0)

    def test_costi_e_risparmio(self):
        self.assertAlmostEqual(
            mh889_c_base(57261.17647058824, 1.70), 97344.00, places=2)
        self.assertAlmostEqual(
            mh889_c_alt(136000.0, 0.25, 3000), 37000.00, places=2)
        self.assertAlmostEqual(
            mh889_risparmio(97344.0, 37000.0), 60344.00, places=2)

    def test_capex_totale_voci(self):
        self.assertEqual(mh889_capex_totale(15000, 45000, 55000,
                                            20000, 5000),
                         140000.0)
        self.assertEqual(mh889_capex_totale(15000, 45000, 0,
                                            20000, 5000),
                         85000.0)

    def test_co2_base_e_alt(self):
        cb = mh889_co2_base(57261.17647058824, 2.68)
        self.assertAlmostEqual(cb, 153.46, places=2)
        ca = mh889_co2_alt(136000.0, 0.35)
        self.assertAlmostEqual(ca, 47.60, places=2)
        self.assertAlmostEqual(mh889_co2_evitata(cb, ca), 105.86,
                               places=2)
        self.assertEqual(mh889_co2_alt(0.0, 0.35), 0.0)

    def test_costo_mese_base_e_alt(self):
        self.assertAlmostEqual(mh889_costo_mese(97344.0), 8112.00,
                               places=2)
        self.assertAlmostEqual(mh889_costo_mese(37000.0), 3083.33,
                               places=2)
        # Il costo mese e il costo annuo diviso
        # per 12, NON diviso per la durata in
        # mesi: 97344 diviso 60 sarebbe 1622,40
        # e sarebbe sbagliato.
        self.assertNotAlmostEqual(mh889_costo_mese(97344.0),
                                  1622.40, places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh889_flussi(140000, 60344.0, 3),
                         [-140000, 60344.0, 60344.0, 60344.0])

    def test_van_tasso_zero_e_cinque(self):
        self.assertAlmostEqual(mh889_van([-100, 60, 60], 0), 20.0)
        bc = mh889_demo_calcoli()
        self.assertAlmostEqual(mh889_van(bc["flussi"], 0.05), bc["van"])

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 121257,94; con 5,0 (cioe' 500 % se
        # letto come frazione) sarebbe tutt'altra.
        bc = mh889_demo_calcoli()
        self.assertAlmostEqual(mh889_van(bc["flussi"], 0.05),
                               121257.94, places=2)
        self.assertNotAlmostEqual(mh889_van(bc["flussi"], 5.0),
                                  121257.94, places=2)

    def test_tir_demo(self):
        bc = mh889_demo_calcoli()
        tir = mh889_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh889_tir([-100, -10, -10]))
        self.assertIsNone(mh889_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh889_demo_calcoli()
        self.assertEqual(mh889_payback(bc["flussi"]), 3)
        self.assertIsNone(mh889_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh889_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh889_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:3]), -19312.00, places=2)
        self.assertAlmostEqual(sum(flussi[:4]), 41032.00, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh889_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh889_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh889_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh889_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh889_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh889_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh889_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh889_demo()
        val = mh889_valida(*[demo[k] for k in (
            "durata_mesi", "e_mese_kwh", "ill_mese_kwh",
            "sup_baracche_m2", "q_risc", "mesi_risc_anno",
            "cons_specifico", "eta_caldaia", "l_per_kwh_t",
            "prezzo_gasolio", "f_co2_gasolio", "cop_hp",
            "risparmio_led", "fv_kwp", "fv_resa",
            "fv_autoconsumo", "prezzo_rete", "om_alt",
            "f_co2_rete", "capex_allaccio", "capex_batteria",
            "capex_fv", "capex_hp", "capex_led", "tasso",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_durata_zero_e_non_multipla_no(self):
        kw = _demo_kwargs(durata_mesi=0)
        self.assertRaises(ValueError, mh889_calcola, **kw)
        kw = _demo_kwargs(durata_mesi=50)
        self.assertRaises(ValueError, mh889_calcola, **kw)
        kw = _demo_kwargs(durata_mesi=36)
        bc = mh889_calcola(**kw)
        self.assertEqual(bc["anni"], 3)

    def test_valida_eta_e_cop_zero_no(self):
        kw = _demo_kwargs(eta_caldaia=0)
        self.assertRaises(ValueError, mh889_calcola, **kw)
        kw = _demo_kwargs(cop_hp=0)
        self.assertRaises(ValueError, mh889_calcola, **kw)

    def test_valida_mesi_risc_sopra_dodici_no(self):
        kw = _demo_kwargs(mesi_risc_anno=13)
        self.assertRaises(ValueError, mh889_calcola, **kw)
        kw = _demo_kwargs(mesi_risc_anno=8.5)
        self.assertRaises(ValueError, mh889_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(fv_autoconsumo=1.1)
        self.assertRaises(ValueError, mh889_calcola, **kw)
        kw = _demo_kwargs(risparmio_led=1.1)
        self.assertRaises(ValueError, mh889_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_gasolio=float("nan"))
        self.assertRaises(ValueError, mh889_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_mese_kwh", -1),
                              ("sup_baracche_m2", -1),
                              ("cons_specifico", -0.01),
                              ("prezzo_gasolio", -0.01),
                              ("capex_batteria", -1),
                              ("capex_fv", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh889_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh889_calcola(mh889_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh889_calcola(dict(mh889_demo(), capex_fv=99999),
                           capex_fv=55000)
        self.assertEqual(bc["capex_eur"], 140000.0)


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
        self.assertEqual(bc["payback"], 3)

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
            bc["diesel_tot_l_anno"] * bc["prezzo_gasolio"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_rete_kwh_anno"] * bc["prezzo_rete"]
            + bc["om_alt"])
        self.assertAlmostEqual(
            bc["costo_mese_base_eur"],
            bc["c_base_eur_anno"] / 12.0)
        self.assertAlmostEqual(
            bc["costo_mese_alt_eur"],
            bc["c_alt_eur_anno"] / 12.0)
        self.assertAlmostEqual(
            bc["diesel_tot_l_anno"],
            bc["diesel_el_l_anno"] + bc["diesel_term_l_anno"])
        self.assertAlmostEqual(
            bc["e_rete_kwh_anno"],
            bc["e_anno_kwh"] - bc["e_ill_anno_kwh"]
            + bc["e_ill_alt_kwh_anno"] + bc["e_hp_kwh_anno"]
            - bc["e_fv_kwh_anno"])

    def test_sensibilita_valori(self):
        s = mh889_sensibilita(**mh889_demo())
        self.assertAlmostEqual(s["p_gasolio_piu20"]["risparmio_eur_anno"],
                               79812.80, places=2)
        self.assertAlmostEqual(s["p_gasolio_piu20"]["van"],
                               205547.66, places=2)
        self.assertEqual(s["p_gasolio_piu20"]["payback"], 2)
        self.assertAlmostEqual(s["p_rete_piu20"]["risparmio_eur_anno"],
                               53544.00, places=2)
        self.assertAlmostEqual(s["p_rete_piu20"]["van"],
                               91817.50, places=2)
        self.assertEqual(s["p_rete_piu20"]["payback"], 3)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               49344.00, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               73633.70, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 3)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        # Senza FV la potenza e zero ma il CAPEX FV
        # forfettario resta nel totale: la variante
        # isola l'effetto della produzione, non
        # del CAPEX.
        self.assertEqual(s["senza_fv"]["capex_eur"], 140000.0)
        self.assertAlmostEqual(s["senza_led"]["risparmio_eur_anno"],
                               57344.00, places=2)
        self.assertAlmostEqual(s["senza_led"]["van"],
                               108269.51, places=2)
        self.assertEqual(s["senza_led"]["payback"], 3)
        self.assertEqual(s["senza_led"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -18742.06, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 5)
        self.assertEqual(s["capex_doppio"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["durata_36"]["van"],
                               24331.68, places=2)
        self.assertEqual(s["durata_36"]["payback"], 3)
        self.assertEqual(s["durata_36"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["tasso_0"]["van"],
                               161720.00, places=2)

    def test_marginale_con_capex_allaccio_alto(self):
        # CAPEX totale 270000 (allaccio a 145000):
        # VAN circa meno 8742,06, entro la tolleranza
        # del 10% (27000).
        bc = mh889_calcola(**_demo_kwargs(capex_allaccio=145000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -8742.06, places=2)
        self.assertEqual(bc["payback"], 5)

    def test_non_convente_con_capex_allaccio_altissimo(self):
        bc = mh889_calcola(**_demo_kwargs(capex_allaccio=300000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -163742.06, places=2)
        self.assertIsNone(bc["payback"])

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh889_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -136656.00,
                               places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh889_csv(bc, mh889_demo())
        for voce in ("durata_mesi", "e_mese_kwh",
                     "diesel_tot_l_anno", "e_hp_kwh_anno",
                     "e_ill_alt_kwh_anno", "e_fv_kwh_anno",
                     "e_rete_kwh_anno",
                     "risparmio_eur_anno", "verdetto",
                     "costo_mese_base_eur", "costo_mese_alt_eur"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 6)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -140000.0)
        self.assertEqual(len(bc["df_tabella"]), 55)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Durata cantiere (mesi)", voci)
        self.assertIn("Gasolio totale (l/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh889_c_alt(180000.0, 0.25, 3000)
        con = mh889_c_alt(136000.0, 0.25, 3000)
        self.assertAlmostEqual(senza - con, 11000.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh889_sensibilita(**mh889_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gasolio_piu20", "p_rete_piu20",
                          "senza_fv", "senza_led",
                          "capex_doppio", "durata_36", "tasso_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh889_csv(bc, mh889_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("diesel_tot_l_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh889_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh889_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh889_calcola(**_demo_kwargs(fv_kwp=0))
        self.assertEqual(bc["e_fv_kwh_anno"], 0.0)
        bc = mh889_calcola(**_demo_kwargs(fv_autoconsumo=0))
        self.assertEqual(bc["e_fv_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["e_rete_kwh_anno"], 180000.0)


class TestCasiLimite(unittest.TestCase):
    def test_durata_zero_non_calcolabile(self):
        # Durata zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(durata_mesi=0)
        self.assertRaises(ValueError, mh889_calcola, **kw)
        self.assertFalse(mh889_valida(*[kw[k] for k in (
            "durata_mesi", "e_mese_kwh", "ill_mese_kwh",
            "sup_baracche_m2", "q_risc", "mesi_risc_anno",
            "cons_specifico", "eta_caldaia", "l_per_kwh_t",
            "prezzo_gasolio", "f_co2_gasolio", "cop_hp",
            "risparmio_led", "fv_kwp", "fv_resa",
            "fv_autoconsumo", "prezzo_rete", "om_alt",
            "f_co2_rete", "capex_allaccio", "capex_batteria",
            "capex_fv", "capex_hp", "capex_led", "tasso",
            "tolleranza_pct")])["valido"])

    def test_durata_non_multipla_non_calcolabile(self):
        kw = _demo_kwargs(durata_mesi=50)
        self.assertRaises(ValueError, mh889_calcola, **kw)

    def test_mesi_risc_zero(self):
        # Zero mesi di riscaldamento: fabbisogno
        # termico zero, E_hp zero, diesel termico
        # zero.
        bc = mh889_calcola(**_demo_kwargs(mesi_risc_anno=0))
        self.assertEqual(bc["q_term_anno_kwh"], 0.0)
        self.assertEqual(bc["e_hp_kwh_anno"], 0.0)
        self.assertEqual(bc["diesel_term_l_anno"], 0.0)

    def test_fv_grande_rete_zero_mai_negativa(self):
        # Con FV molto grande (500 kWp) l'energia
        # da rete va a zero, mai negativa: costo
        # alternativo uguale alla sola O&M.
        bc = mh889_calcola(**_demo_kwargs(fv_kwp=500))
        self.assertEqual(bc["e_rete_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 3000.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 94344.0)

    def test_prezzo_gasolio_zero(self):
        # A gasolio gratuito il costo base e zero
        # e il risparmio diventa meno 37000,00:
        # verdetto NON_CALCOLABILE.
        bc = mh889_calcola(**_demo_kwargs(prezzo_gasolio=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -37000.00,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh889_calcola(**_demo_kwargs(capex_allaccio=0,
                                          capex_batteria=0,
                                          capex_fv=0,
                                          capex_hp=0,
                                          capex_led=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero(self):
        bc = mh889_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(bc["van"], 161720.00, places=2)
        self.assertEqual(bc["payback"], 3)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def889\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh889_demo().keys()), lette - set(mh889_demo().keys()))
        self.assertEqual(lette, set(mh889_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc889\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc889\["([^"]+)"\]', src))
        attese = set(mh889_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 888 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 889.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 892)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab889:"), 1)
        self.assertTrue(src.startswith("    # W894"))

    def test_ui_tab889_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab889:"), 1)
        self.assertIn("def mh889_demo(", src_h)
        self.assertIn("def mh889_calcola(", src_h)
        self.assertIn("tab889", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Cantiere edile: gruppo elettrogeno diesel + riscaldamento a gasolio battono allaccio rete + batteria + FV + pompa di calore + LED?", src)
        self.assertIn("🏗️ Cantiere edile: gruppo elettrogeno diesel + riscaldamento a gasolio battono allaccio rete + batteria + FV + pompa di calore + LED?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st889_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st889_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st889_calcola"', src)
        self.assertIn('key="st889_csv"', src)
        self.assertIn('key="st889_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg889"), src.index(".paiac("))
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
