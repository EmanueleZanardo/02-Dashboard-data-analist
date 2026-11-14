"""Test nuova scheda Bitcoin mining: il miner come carico flessibile
monetizza l'energia in eccesso?
Repo path: tests/test_w900_bitcoin_mining.py

Effetto ECONOMICO (non solo elettrico): il miner e' un carico
flessibile che trasforma energia in eccesso (anche a prezzo nullo
o negativo, curtailment) in ricavo da hashprice. Flotta di 100 miner
(demo), 200 TH/s per miner, 20 J/TH: P = 100 per 200 per 20 diviso
1000 = 400 kW; H = 100 per 200 diviso 1000 = 20 PH/s; ricavo al
giorno = 20 per 55 = 1100 EUR; ore operative = 6000 piu 2760 =
8760 h; ricavo annuo = 1100 per 365 = 401500 EUR; costo energia =
400 per (6000 per 0,09 piu 2760 per 0,01) = 227040 EUR; O&M 20000
EUR/anno; CAPEX = 100 per 3000 = 300000 EUR; margine = 401500 meno
227040 meno 20000 = 154460 EUR/anno; vita 5 anni; tasso 0,05
(frazione); fattore di rendita a = (1 meno 1,05 elevato a meno 5)
diviso 0,05 = 4,3295; VAN = 154460 per 4,3295 meno 300000 =
368730,97 EUR; TIR per bisezione su flussi [meno 300000, 154460
per 5] con intervallo da meno 0,9 a 5,0 (42,82 %); payback (primo
anno con cumulato maggiore o uguale a 0) = 2 anni; breakeven prezzo
energia p_be = (1100 diviso 9600) per 1000 = 114,58 EUR/MWh.
Scenari hashprice: HP per 0,7 (38,50): ricavo annuo 281050,00,
margine 34010,00, VAN meno 152754,50, TIR meno 16,36 %, payback
nessuno, NON_CONVIENTE; HP (55,00): VAN 368730,97, TIR 42,82 %,
payback 2, CONVIENTE; HP per 1,3 (71,50): ricavo annuo 521950,00,
margine 274910,00, VAN 890216,43, TIR 87,70 %, payback 2,
CONVIENTE.
Confronto ore in eccesso: ricavo mining = 20 per 55 per 115 =
126500 EUR/anno; ricavo vendita spot = 400 per 2760 per 0,01 =
11040 EUR/anno; costo energia eccesso = 11040 EUR/anno; delta =
126500 meno 11040 meno 11040 = 104420 EUR/anno (il mining sulle
ore in eccesso conviene). Energia 3504,00 MWh/anno, CO2 1226,40
t/anno (INFORMATIVA, mai nel conto economico).
Tolleranza in PERCENTUALE (10 = 10 % del CAPEX). Il tasso e in
FRAZIONE (0,05 = 5 %), usato diretto, NON diviso per 100. I flussi
piatti sono una SEMPLIFICAZIONE DICHIARATA (difficolta' di rete,
prezzo di Bitcoin, halving, prezzi energia variano nel mondo reale,
qui valore medio costante); l'hashprice e' un'ipotesi esplicita e
costante negli scenari, non una previsione di mercato. Verdetto
principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se margine minore o uguale a 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV) oppure se un input
e degenere (N nullo o negativo o non intero, hashrate nullo o
negativo, efficienza nulla o negativa, hashprice negativo, ore
pieno negative, prezzo pieno negativo, ore eccesso negative, O&M
negativo, costo miner negativo, vita nulla o negativa o non
intera, tasso nullo o negativo o maggiore o uguale a 1, tolleranza
negativa, fattore CO2 negativo, ore operative nulle o negative o
sopra 8760); altrimenti CONVIENTE se VAN maggiore di 0, MARGINALE
se VAN negativa entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: hashprice 43 (VAN meno 10531,19, TIR 3,72 %, payback
5, MARGINALE); hashprice zero (margine meno 247040,00, VAN None,
NON_CALCOLABILE); prezzo eccesso meno 0,02 (VAN 512123,23, TIR
55,69 %, payback 2, delta eccesso 170660,00); prezzo eccesso zero
(VAN 416528,39, TIR 47,18 %, payback 2, delta eccesso 126500,00);
ore eccesso zero (margine 39000,00, VAN meno 131150,41, TIR meno
12,83 %, payback nessuno, delta eccesso 0,00, non conviene);
costo miner zero (VAN 668730,97, TIR non definita, payback 0);
O&M zero (VAN 455320,50, TIR 50,66 %, payback 2); vita 3 (VAN
120632,89, TIR 25,34 %, payback 2); tasso 0,10 (VAN 285524,92,
TIR 42,82 %, payback 2); prezzo pieno 0,15 (VAN meno 254713,67,
TIR meno 39,49 %, payback nessuno, NON_CONVIENTE); ore operative
sopra 8760 (ValueError); N non intero (ValueError).
Distinzione esplicita: qui SOLO il miner come carico flessibile
che monetizza l'energia in eccesso (hashprice contro prezzo
energia, con confronto mining contro vendita spot sulle ore in
eccesso), NIENTE arbitraggio batteria (li lo spostamento di
energia nel tempo con carica e scarica: qui il miner consuma e
basta, non restituisce energia), NIENTE demand response generico
(li la flessibilita' di un carico qualsiasi: qui il ricavo e' da
hashprice, non da pagamento per flessibilita'), NIENTE LCOE di un
impianto di generazione (li il costo livellato dell'energia
prodotta: qui il costo e' l'energia comprata per minare).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w900_helpers import (
        demo_calcoli,
        mh895_breakeven,
        mh895_calcola,
        mh895_capex,
        mh895_co2,
        mh895_confronto,
        mh895_costo_energia,
        mh895_csv,
        mh895_demo,
        mh895_demo_calcoli,
        mh895_fattore_rendita,
        mh895_flussi,
        mh895_hashrate_phs,
        mh895_int_pos,
        mh895_margine,
        mh895_nneg,
        mh895_num,
        mh895_ore_operative,
        mh895_payback,
        mh895_pos,
        mh895_potenza_kw,
        mh895_ricavo_anno,
        mh895_ricavo_giorno,
        mh895_scenario,
        mh895_sensibilita,
        mh895_tasso,
        mh895_tir,
        mh895_valida,
        mh895_van,
        mh895_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w900_helpers", os.path.join(_hf, "w900_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh895_breakeven = _mod.mh895_breakeven
    mh895_calcola = _mod.mh895_calcola
    mh895_capex = _mod.mh895_capex
    mh895_co2 = _mod.mh895_co2
    mh895_confronto = _mod.mh895_confronto
    mh895_costo_energia = _mod.mh895_costo_energia
    mh895_csv = _mod.mh895_csv
    mh895_demo = _mod.mh895_demo
    mh895_demo_calcoli = _mod.mh895_demo_calcoli
    mh895_fattore_rendita = _mod.mh895_fattore_rendita
    mh895_flussi = _mod.mh895_flussi
    mh895_hashrate_phs = _mod.mh895_hashrate_phs
    mh895_int_pos = _mod.mh895_int_pos
    mh895_margine = _mod.mh895_margine
    mh895_nneg = _mod.mh895_nneg
    mh895_num = _mod.mh895_num
    mh895_ore_operative = _mod.mh895_ore_operative
    mh895_payback = _mod.mh895_payback
    mh895_pos = _mod.mh895_pos
    mh895_potenza_kw = _mod.mh895_potenza_kw
    mh895_ricavo_anno = _mod.mh895_ricavo_anno
    mh895_ricavo_giorno = _mod.mh895_ricavo_giorno
    mh895_scenario = _mod.mh895_scenario
    mh895_sensibilita = _mod.mh895_sensibilita
    mh895_tasso = _mod.mh895_tasso
    mh895_tir = _mod.mh895_tir
    mh895_valida = _mod.mh895_valida
    mh895_van = _mod.mh895_van
    mh895_verdetto = _mod.mh895_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w900_helpers.py")
_UI_PATH = _risolvi("w900_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "4"
_VECCHIO_TAB = "tab89" + "4"
_VECCHIO_ST = "st89" + "4_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "potenza_kw": 400.0,
    "hashrate_phs": 20.0,
    "ore_operative": 8760,
    "ricavo_giorno": 1100.0,
    "ricavo_anno": 401500.0,
    "costo_energia": 227040.0,
    "costo_energia_pieno": 216000.0,
    "costo_energia_eccesso": 11040.0,
    "margine": 154460.0,
    "capex_eur": 300000.0,
    "fattore_rendita": 4.3294766706308225,
    "energia_mwh_anno": 3504.0,
    "co2_t_anno": 1226.3999999999999,
    "p_be": 114.58333333333333,
    "van": 368730.9665456369,
    "tir": 42.82293456476223,
    "payback": 2,
}

_DEMO_SCENARI = [
    {"fattore": 0.7, "hashprice": 38.5,
     "ricavo_giorno": 770.0, "ricavo_anno": 281050.0,
     "margine": 34010.0, "van": -152754.4984318457,
     "tir": -16.36119115460758, "payback": None,
     "verdetto": "NON_CONVIENTE"},
    {"fattore": 1.0, "hashprice": 55.0,
     "ricavo_giorno": 1100.0, "ricavo_anno": 401500.0,
     "margine": 154460.0, "van": 368730.9665456369,
     "tir": 42.82293456476223, "payback": 2,
     "verdetto": "CONVIENTE"},
    {"fattore": 1.3, "hashprice": 71.5,
     "ricavo_giorno": 1430.0, "ricavo_anno": 521950.0,
     "margine": 274910.0, "van": 890216.4315231193,
     "tir": 87.703853249879, "payback": 2,
     "verdetto": "CONVIENTE"},
]

_DEMO_CONFRONTO = {
    "ricavo_mining_eccesso": 126500.0,
    "ricavo_vendita_eccesso": 11040.0,
    "costo_energia_eccesso": 11040.0,
    "delta": 104420.0,
    "conviene": True,
}

_ORDINE_VALIDA = (
    "n_miner", "h_ths", "eff_j_th", "hashprice", "ore_pieno",
    "p_pieno", "ore_eccesso", "p_eccesso", "om_eur_anno",
    "costo_miner", "vita_anni", "tasso", "tolleranza_pct",
    "co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh895_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh895_num(3, "x"), 3.0)
        self.assertEqual(mh895_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh895_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh895_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh895_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh895_pos(0, "x")
        with self.assertRaises(ValueError):
            mh895_pos(-1, "x")
        self.assertEqual(mh895_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh895_int_pos(100, "x"), 100)
        self.assertEqual(mh895_int_pos(100.0, "x"), 100)
        with self.assertRaises(ValueError):
            mh895_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh895_int_pos(100.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh895_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh895_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh895_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh895_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh895_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh895_tasso(-0.01, "x")

    def test_ore_operative_somma(self):
        self.assertEqual(mh895_ore_operative(6000, 2760), 8760.0)
        self.assertEqual(mh895_ore_operative(0, 8760), 8760.0)
        self.assertEqual(mh895_ore_operative(8760, 0), 8760.0)
        with self.assertRaises(ValueError):
            mh895_ore_operative(0, 0)
        with self.assertRaises(ValueError):
            mh895_ore_operative(6000, 2761)
        with self.assertRaises(ValueError):
            mh895_ore_operative(-1, 100)
        with self.assertRaises(ValueError):
            mh895_ore_operative(4380, -1)


class TestFisica(unittest.TestCase):
    def test_potenza_e_hashrate(self):
        self.assertEqual(mh895_potenza_kw(100, 200, 20), 400.0)
        self.assertEqual(mh895_potenza_kw(1, 100, 30), 3.0)
        self.assertEqual(mh895_potenza_kw(10, 150, 25), 37.5)
        self.assertEqual(mh895_hashrate_phs(100, 200), 20.0)
        self.assertEqual(mh895_hashrate_phs(1, 100), 0.1)
        with self.assertRaises(ValueError):
            mh895_potenza_kw(0, 200, 20)
        with self.assertRaises(ValueError):
            mh895_potenza_kw(100.5, 200, 20)
        with self.assertRaises(ValueError):
            mh895_potenza_kw(100, 0, 20)
        with self.assertRaises(ValueError):
            mh895_potenza_kw(100, 200, 0)
        with self.assertRaises(ValueError):
            mh895_hashrate_phs(100, -5)

    def test_ricavo_giorno_e_anno(self):
        self.assertEqual(mh895_ricavo_giorno(20, 55), 1100.0)
        self.assertEqual(mh895_ricavo_giorno(20, 0), 0.0)
        self.assertEqual(mh895_ricavo_anno(1100, 8760), 401500.0)
        self.assertEqual(mh895_ricavo_anno(1100, 4380), 200750.0)
        with self.assertRaises(ValueError):
            mh895_ricavo_giorno(20, -1)
        with self.assertRaises(ValueError):
            mh895_ricavo_giorno(0, 55)
        with self.assertRaises(ValueError):
            mh895_ricavo_anno(1100, 0)

    def test_costo_energia(self):
        self.assertEqual(
            mh895_costo_energia(400, 6000, 0.09, 2760, 0.01), 227040.0)
        self.assertEqual(
            mh895_costo_energia(400, 6000, 0.09, 2760, 0.0), 216000.0)
        # Prezzo eccesso negativo: il costo sulle ore in
        # eccesso e' negativo (si viene pagati per consumare).
        self.assertEqual(
            mh895_costo_energia(400, 6000, 0.09, 2760, -0.02),
            193920.0)
        self.assertEqual(
            mh895_costo_energia(400, 8760, 0.09, 0, 0.01), 315360.0)
        with self.assertRaises(ValueError):
            mh895_costo_energia(0, 6000, 0.09, 2760, 0.01)
        with self.assertRaises(ValueError):
            mh895_costo_energia(400, 6000, -0.01, 2760, 0.01)
        with self.assertRaises(ValueError):
            mh895_costo_energia(400, -1, 0.09, 2760, 0.01)

    def test_capex_e_margine(self):
        self.assertEqual(mh895_capex(100, 3000), 300000.0)
        self.assertEqual(mh895_capex(100, 0), 0.0)
        self.assertEqual(mh895_margine(401500, 227040, 20000), 154460.0)
        # Margine negativo: la funzione lo calcola, il
        # verdetto NON_CALCOLABILE arriva a livello calcola.
        self.assertEqual(mh895_margine(100000, 227040, 20000), -147040.0)
        with self.assertRaises(ValueError):
            mh895_capex(0, 3000)
        with self.assertRaises(ValueError):
            mh895_capex(100, -1)
        with self.assertRaises(ValueError):
            mh895_margine(401500, 227040, -1)

    def test_fattore_rendita(self):
        self.assertAlmostEqual(mh895_fattore_rendita(0.05, 5),
                               4.3295, places=4)
        self.assertAlmostEqual(mh895_fattore_rendita(0.10, 5),
                               3.7908, places=4)
        self.assertAlmostEqual(mh895_fattore_rendita(0.05, 1), 0.9524,
                               places=4)
        with self.assertRaises(ValueError):
            mh895_fattore_rendita(0.0, 5)
        with self.assertRaises(ValueError):
            mh895_fattore_rendita(0.05, 0)

    def test_breakeven(self):
        self.assertAlmostEqual(mh895_breakeven(1100, 400), 114.58,
                               places=2)
        self.assertAlmostEqual(mh895_breakeven(770, 400), 80.21,
                               places=2)
        self.assertEqual(mh895_breakeven(0, 400), 0.0)
        # Con potenza doppia a parita' di ricavo il
        # breakeven si dimezza.
        self.assertAlmostEqual(mh895_breakeven(1100, 800), 57.29,
                               places=2)
        with self.assertRaises(ValueError):
            mh895_breakeven(1100, 0)

    def test_scenario_singolo(self):
        bc = demo_calcoli()
        s = mh895_scenario(0.7, bc["hashprice"], bc["hashrate_phs"],
                           bc["ore_operative"], bc["costo_energia"],
                           bc["om_eur_anno"], bc["capex_eur"],
                           bc["fattore_rendita"], bc["vita_anni"],
                           bc["tolleranza_pct"])
        self.assertAlmostEqual(s["hashprice"], 38.5)
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(s["flussi"]), 6)
        s = mh895_scenario(1.3, bc["hashprice"], bc["hashrate_phs"],
                           bc["ore_operative"], bc["costo_energia"],
                           bc["om_eur_anno"], bc["capex_eur"],
                           bc["fattore_rendita"], bc["vita_anni"],
                           bc["tolleranza_pct"])
        self.assertAlmostEqual(s["van"], 890216.43, places=2)
        self.assertEqual(s["payback"], 2)
        self.assertEqual(s["verdetto"], "CONVIENTE")

    def test_scenario_margine_negativo_non_calcolabile(self):
        bc = demo_calcoli()
        s = mh895_scenario(0.7, 30.0, bc["hashrate_phs"],
                           bc["ore_operative"], bc["costo_energia"],
                           bc["om_eur_anno"], bc["capex_eur"],
                           bc["fattore_rendita"], bc["vita_anni"],
                           bc["tolleranza_pct"])
        self.assertLess(s["margine"], 0.0)
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")
        with self.assertRaises(ValueError):
            mh895_scenario(-0.5, bc["hashprice"], bc["hashrate_phs"],
                           bc["ore_operative"], bc["costo_energia"],
                           bc["om_eur_anno"], bc["capex_eur"],
                           bc["fattore_rendita"], bc["vita_anni"],
                           bc["tolleranza_pct"])

    def test_confronto_formule(self):
        c = mh895_confronto(20, 55, 2760, 400, 0.01)
        self.assertEqual(c["ricavo_mining_eccesso"], 126500.0)
        self.assertEqual(c["ricavo_vendita_eccesso"], 11040.0)
        self.assertEqual(c["costo_energia_eccesso"], 11040.0)
        self.assertEqual(c["delta"], 104420.0)
        self.assertTrue(c["conviene"])
        # Prezzo eccesso negativo: vendita spot e costo
        # sono negativi, il delta cresce.
        c = mh895_confronto(20, 55, 2760, 400, -0.02)
        self.assertEqual(c["ricavo_vendita_eccesso"], -22080.0)
        self.assertEqual(c["costo_energia_eccesso"], -22080.0)
        self.assertEqual(c["delta"], 170660.0)
        self.assertTrue(c["conviene"])
        # Ore eccesso zero: delta zero, non conviene
        # (non c'e' nulla da confrontare).
        c = mh895_confronto(20, 55, 0, 400, 0.01)
        self.assertEqual(c["delta"], 0.0)
        self.assertFalse(c["conviene"])
        # Hashprice zero: il mining in eccesso perde
        # vendita e costo.
        c = mh895_confronto(20, 0, 2760, 400, 0.01)
        self.assertEqual(c["delta"], -22080.0)
        self.assertFalse(c["conviene"])

    def test_co2_informativa(self):
        self.assertAlmostEqual(mh895_co2(400, 8760, 0.35), 1226.40,
                               places=2)
        self.assertEqual(mh895_co2(400, 8760, 0.0), 0.0)
        self.assertAlmostEqual(mh895_co2(400, 4380, 0.35), 613.20,
                               places=2)
        with self.assertRaises(ValueError):
            mh895_co2(400, 8760, -0.1)
        with self.assertRaises(ValueError):
            mh895_co2(0, 8760, 0.35)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh895_flussi(300000, 154460.0, 3),
                         [-300000, 154460.0, 154460.0, 154460.0])

    def test_van_tasso_cinque(self):
        bc = mh895_demo_calcoli()
        self.assertAlmostEqual(
            mh895_van(bc["flussi"], 0.05),
            bc["van"])
        self.assertAlmostEqual(
            mh895_van(bc["scenari"][0]["flussi"], 0.05),
            bc["scenari"][0]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh895_van([-300000, 154460.0, 154460.0], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 368730,97; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh895_demo_calcoli()
        self.assertAlmostEqual(
            mh895_van(bc["flussi"], 0.05),
            368730.97, places=2)
        self.assertNotAlmostEqual(
            mh895_van(bc["flussi"], 0.50),
            368730.97, places=2)
        with self.assertRaises(ValueError):
            mh895_van(bc["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh895_demo_calcoli()
        tir = mh895_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh895_tir([-100, -10, -10]))
        self.assertIsNone(mh895_tir([100, 10, 10]))
        self.assertIsNone(mh895_tir([0, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh895_demo_calcoli()
        self.assertEqual(mh895_payback(bc["flussi"]), 2)
        self.assertIsNone(mh895_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh895_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh895_demo_calcoli()
        f0 = bc["flussi"]
        self.assertAlmostEqual(sum(f0[:2]), -145540.00, places=2)
        self.assertAlmostEqual(sum(f0[:3]), 8920.00, places=2)
        self.assertAlmostEqual(sum(f0), 472300.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(mh895_verdetto(100.0, 300000, 10), "CONVIENTE")
        self.assertEqual(mh895_verdetto(-20000.0, 300000, 10),
                         "MARGINALE")
        self.assertEqual(mh895_verdetto(-40000.0, 300000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh895_verdetto(0.0, 300000, 10), "MARGINALE")
        # VAN esattamente alla tolleranza: MARGINALE (inclusa).
        self.assertEqual(mh895_verdetto(-30000.0, 300000, 10),
                         "MARGINALE")
        self.assertEqual(mh895_verdetto(-30000.01, 300000, 10),
                         "NON_CONVIENTE")
        # Con tolleranza zero solo VAN zero e' MARGINALE.
        self.assertEqual(mh895_verdetto(-1.0, 300000, 0),
                         "NON_CONVIENTE")
        self.assertEqual(mh895_verdetto(0.0, 300000, 0), "MARGINALE")

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(mh895_verdetto(None, 300000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh895_demo()
        val = mh895_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(vita_anni=5.5)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(vita_anni=3)
        bc = mh895_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 3)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh895_calcola(**_demo_kwargs(tasso=tasso))
        bc = mh895_calcola(**_demo_kwargs(tasso=0.10))
        self.assertEqual(bc["tasso"], 0.10)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("n_miner", 0),
                              ("h_ths", 0),
                              ("eff_j_th", 0)):
            with self.assertRaises(ValueError):
                mh895_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_ore_operative_no(self):
        kw = _demo_kwargs(ore_pieno=0, ore_eccesso=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(ore_pieno=6000, ore_eccesso=2761)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(ore_pieno=8760, ore_eccesso=0)
        bc = mh895_calcola(**kw)
        self.assertEqual(bc["ore_operative"], 8760)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(hashprice=float("nan"))
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(p_eccesso=float("inf"))
        self.assertRaises(ValueError, mh895_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("n_miner", -1),
                              ("h_ths", -1),
                              ("eff_j_th", -1),
                              ("hashprice", -1),
                              ("ore_pieno", -1),
                              ("p_pieno", -0.01),
                              ("ore_eccesso", -1),
                              ("om_eur_anno", -1),
                              ("costo_miner", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh895_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_p_eccesso_negativo_ok(self):
        # Il prezzo eccesso negativo e' ammesso: energia
        # in eccesso o curtailment, si viene pagati per
        # consumare.
        bc = mh895_calcola(**_demo_kwargs(p_eccesso=-0.02))
        self.assertEqual(bc["p_eccesso"], -0.02)
        self.assertAlmostEqual(bc["van"], 512123.23, places=2)

    def test_valida_n_non_intero_no(self):
        kw = _demo_kwargs(n_miner=100.5)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(n_miner=100.0)
        bc = mh895_calcola(**kw)
        self.assertEqual(bc["n_miner"], 100)

    def test_calcola_accetta_dict(self):
        bc = mh895_calcola(mh895_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 3)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh895_calcola(dict(mh895_demo(), costo_miner=9999),
                           costo_miner=3000)
        self.assertEqual(bc["capex_eur"], 300000.0)


class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo_scalari(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO_SCALARI.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, int):
                    self.assertEqual(ottenuto, atteso)
                else:
                    self.assertLess(_rel(ottenuto, atteso), 1e-9)

    def test_demo_scenari(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["scenari"]), len(_DEMO_SCENARI))
        for i, atteso in enumerate(_DEMO_SCENARI):
            for chiave, valore in atteso.items():
                with self.subTest(scenario=i, chiave=chiave):
                    ottenuto = bc["scenari"][i][chiave]
                    if valore is None or isinstance(valore, (int, str)):
                        self.assertEqual(ottenuto, valore)
                    else:
                        self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_confronto(self):
        bc = demo_calcoli()
        for chiave, valore in _DEMO_CONFRONTO.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc["confronto"][chiave]
                if isinstance(valore, bool):
                    self.assertEqual(ottenuto, valore)
                else:
                    self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_verdetto_principale(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(bc["scenario_base"]["verdetto"], "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 2)
        self.assertAlmostEqual(bc["tir"], 42.82, places=2)
        self.assertAlmostEqual(bc["p_be"], 114.58, places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["potenza_kw"],
            bc["n_miner"] * bc["h_ths"] * bc["eff_j_th"] / 1000.0)
        self.assertAlmostEqual(
            bc["hashrate_phs"],
            bc["n_miner"] * bc["h_ths"] / 1000.0)
        self.assertAlmostEqual(
            bc["ore_operative"],
            bc["ore_pieno"] + bc["ore_eccesso"])
        self.assertAlmostEqual(
            bc["ricavo_giorno"],
            bc["hashrate_phs"] * bc["hashprice"])
        self.assertAlmostEqual(
            bc["ricavo_anno"],
            bc["ricavo_giorno"] * bc["ore_operative"] / 24.0)
        self.assertAlmostEqual(
            bc["costo_energia"],
            bc["potenza_kw"] * (bc["ore_pieno"] * bc["p_pieno"]
                                + bc["ore_eccesso"] * bc["p_eccesso"]))
        self.assertAlmostEqual(
            bc["costo_energia_pieno"] + bc["costo_energia_eccesso"],
            bc["costo_energia"])
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["n_miner"] * bc["costo_miner"])
        self.assertAlmostEqual(
            bc["margine"],
            bc["ricavo_anno"] - bc["costo_energia"]
            - bc["om_eur_anno"])
        self.assertAlmostEqual(
            bc["van"],
            bc["margine"] * bc["fattore_rendita"] - bc["capex_eur"])
        self.assertAlmostEqual(
            bc["energia_mwh_anno"],
            bc["potenza_kw"] * bc["ore_operative"] / 1000.0)
        self.assertAlmostEqual(
            bc["co2_t_anno"],
            bc["energia_mwh_anno"] * bc["co2_t_mwh"])
        self.assertAlmostEqual(
            bc["p_be"],
            (bc["ricavo_giorno"] / (bc["potenza_kw"] * 24.0)) * 1000.0)
        for s in bc["scenari"]:
            self.assertAlmostEqual(
                s["hashprice"], bc["hashprice"] * s["fattore"])
            self.assertAlmostEqual(
                s["ricavo_anno"],
                s["ricavo_giorno"] * bc["ore_operative"] / 24.0)
            self.assertAlmostEqual(
                s["margine"],
                s["ricavo_anno"] - bc["costo_energia"]
                - bc["om_eur_anno"])
            self.assertEqual(len(s["flussi"]), bc["vita_anni"] + 1)
        conf = bc["confronto"]
        self.assertAlmostEqual(
            conf["ricavo_mining_eccesso"],
            bc["hashrate_phs"] * bc["hashprice"]
            * bc["ore_eccesso"] / 24.0)
        self.assertAlmostEqual(
            conf["ricavo_vendita_eccesso"],
            bc["potenza_kw"] * bc["ore_eccesso"] * bc["p_eccesso"])
        self.assertAlmostEqual(
            conf["delta"],
            conf["ricavo_mining_eccesso"]
            - conf["ricavo_vendita_eccesso"]
            - conf["costo_energia_eccesso"])

    def test_monotonia_scenari(self):
        bc = demo_calcoli()
        hps = [s["hashprice"] for s in bc["scenari"]]
        rics = [s["ricavo_anno"] for s in bc["scenari"]]
        margs = [s["margine"] for s in bc["scenari"]]
        vans = [s["van"] for s in bc["scenari"]]
        for prima, dopo in zip(hps, hps[1:]):
            self.assertLess(prima, dopo)
        for prima, dopo in zip(rics, rics[1:]):
            self.assertLess(prima, dopo)
        for prima, dopo in zip(margs, margs[1:]):
            self.assertLess(prima, dopo)
        for prima, dopo in zip(vans, vans[1:]):
            self.assertLess(prima, dopo)

    def test_sensibilita_valori(self):
        s = mh895_sensibilita(**mh895_demo())
        self.assertEqual(set(s.keys()),
                         {"hp_385", "hp_715", "p_pieno_015",
                          "p_eccesso_zero", "p_eccesso_neg",
                          "vita_3", "tasso_010", "costo_miner_5000",
                          "om_100000"})
        attesi = {
            "hp_385": (-152754.50, -16.36, None, "NON_CONVIENTE"),
            "hp_715": (890216.43, 87.70, 2, "CONVIENTE"),
            "p_pieno_015": (-254713.67, -39.49, None, "NON_CONVIENTE"),
            "p_eccesso_zero": (416528.39, 47.18, 2, "CONVIENTE"),
            "p_eccesso_neg": (512123.23, 55.69, 2, "CONVIENTE"),
            "vita_3": (120632.89, 25.34, 2, "CONVIENTE"),
            "tasso_010": (285524.92, 42.82, 2, "CONVIENTE"),
            "costo_miner_5000": (168730.97, 16.49, 4, "CONVIENTE"),
            "om_100000": (22372.83, 7.66, 5, "CONVIENTE"),
        }
        for nome, (van, tir, pb, verd) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(s[nome]["van"], van, places=2)
                self.assertAlmostEqual(s[nome]["tir"], tir, places=2)
                self.assertEqual(s[nome]["payback"], pb)
                self.assertEqual(s[nome]["verdetto"], verd)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)

    def test_hashprice_43_marginale(self):
        bc = mh895_calcola(**_demo_kwargs(hashprice=43))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -10531.19, places=2)
        self.assertAlmostEqual(bc["tir"], 3.72, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertAlmostEqual(bc["margine"], 66860.00, places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh895_csv(bc, mh895_demo())
        for voce in ("n_miner", "h_ths", "eff_j_th",
                     "hashprice", "ore_pieno", "p_pieno",
                     "ore_eccesso", "p_eccesso", "om_eur_anno",
                     "costo_miner", "vita_anni", "tasso",
                     "tolleranza_pct", "co2_t_mwh",
                     "potenza_kw", "hashrate_phs",
                     "ore_operative", "ricavo_giorno",
                     "ricavo_anno", "costo_energia",
                     "costo_energia_pieno", "costo_energia_eccesso",
                     "capex_eur", "margine", "fattore_rendita",
                     "energia_mwh_anno", "co2_t_anno", "p_be",
                     "van", "tir", "payback",
                     "scenario_70_hashprice", "scenario_70_van",
                     "scenario_70_verdetto",
                     "scenario_100_hashprice", "scenario_100_van",
                     "scenario_130_hashprice", "scenario_130_van",
                     "scenario_130_verdetto",
                     "confronto_ricavo_mining_eccesso",
                     "confronto_ricavo_vendita_eccesso",
                     "confronto_costo_energia_eccesso",
                     "confronto_delta", "confronto_conviene",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)
        self.assertIn("NON_CONVIENTE", csv)

    def test_df_scenari_bilancio_flussi_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 3)
        self.assertEqual(len(bc["df_bilancio"]), 4)
        self.assertEqual(len(bc["df_flussi"]), 6)
        self.assertEqual(len(bc["df_tabella"]), 36)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -300000.0)
        self.assertAlmostEqual(
            bc["df_flussi"]["Cumulato (EUR)"].iloc[-1], 472300.00,
            places=2)
        self.assertEqual(
            list(bc["df_bilancio"]["Voce"]),
            ["Ricavo", "Costo energia", "O&M", "Margine"])
        self.assertAlmostEqual(
            bc["df_bilancio"]["EUR/anno"].iloc[0], 401500.00)
        self.assertAlmostEqual(
            bc["df_bilancio"]["EUR/anno"].iloc[-1], 154460.00)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Potenza (kW)", voci)
        self.assertIn("Hashrate totale (PH/s)", voci)
        self.assertIn("Breakeven prezzo energia (EUR/MWh)", voci)
        self.assertIn("Delta mining ore eccesso (EUR/anno)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("Hashprice (EUR/PH/s/giorno)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh895_csv(bc, mh895_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("potenza_kw;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh895_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh895_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh895_calcola(**_demo_kwargs(costo_miner=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 668730.97, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh895_calcola(**_demo_kwargs(om_eur_anno=0))
        self.assertEqual(bc["om_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 455320.50, places=2)
        self.assertGreater(bc["van"], 368730.97)
        bc = mh895_calcola(**_demo_kwargs(co2_t_mwh=0))
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_hashprice_zero_non_calcolabile(self):
        # Hashprice zero: ricavo zero, margine meno
        # 247040,00: non calcolabile negli helper
        # (VAN None) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(hashprice=0)
        bc = mh895_calcola(**kw)
        self.assertEqual(bc["margine"], -247040.0)
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "NON_CALCOLABILE")

    def test_margine_zero_non_calcolabile(self):
        # Hashprice al pareggio del margine: margine
        # circa zero (meno 2,9e-11 per arrotondamento),
        # verdetto NON_CALCOLABILE.
        kw = _demo_kwargs(hashprice=33.841095890410955)
        bc = mh895_calcola(**kw)
        self.assertAlmostEqual(bc["margine"], 0.0, places=6)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_margine_negativo_non_calcolabile(self):
        kw = _demo_kwargs(hashprice=30)
        bc = mh895_calcola(**kw)
        self.assertLess(bc["margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        csv = mh895_csv(bc, mh895_demo())
        self.assertIn("NON_CALCOLABILE", csv)

    def test_vita_zero_non_calcolabile(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        self.assertFalse(mh895_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_vita_non_intera_non_calcolabile(self):
        kw = _demo_kwargs(vita_anni=5.5)
        self.assertRaises(ValueError, mh895_calcola, **kw)

    def test_n_miner_zero_e_non_intero_non_calcolabili(self):
        kw = _demo_kwargs(n_miner=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(n_miner=100.5)
        self.assertRaises(ValueError, mh895_calcola, **kw)

    def test_hashrate_e_efficienza_zero_non_calcolabili(self):
        kw = _demo_kwargs(h_ths=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(eff_j_th=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)

    def test_tasso_zero_e_uno_non_calcolabili(self):
        kw = _demo_kwargs(tasso=0.0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(tasso=1.0)
        self.assertRaises(ValueError, mh895_calcola, **kw)

    def test_ore_operative_zero_e_sopra_tetto_non_calcolabili(self):
        kw = _demo_kwargs(ore_pieno=0, ore_eccesso=0)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(ore_pieno=6000, ore_eccesso=2761)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(ore_pieno=8760, ore_eccesso=1)
        self.assertRaises(ValueError, mh895_calcola, **kw)

    def test_ore_pieno_zero_calcolabile(self):
        # Solo ore in eccesso: 2760 h a 0,01 EUR/kWh,
        # margine 95460,00, VAN 113291,84, CONVIENTE.
        bc = mh895_calcola(**_demo_kwargs(ore_pieno=0))
        self.assertEqual(bc["ore_operative"], 2760)
        self.assertAlmostEqual(bc["margine"], 95460.00, places=2)
        self.assertAlmostEqual(bc["van"], 113291.84, places=2)
        self.assertAlmostEqual(bc["tir"], 17.78, places=2)
        self.assertEqual(bc["payback"], 4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_ore_eccesso_zero(self):
        # Senza ore in eccesso: margine 39000,00, VAN
        # meno 131150,41, TIR meno 12,83 %, payback
        # nessuno, delta eccesso 0,00, non conviene.
        bc = mh895_calcola(**_demo_kwargs(ore_eccesso=0))
        self.assertEqual(bc["ore_operative"], 6000)
        self.assertAlmostEqual(bc["margine"], 39000.00, places=2)
        self.assertAlmostEqual(bc["van"], -131150.41, places=2)
        self.assertAlmostEqual(bc["tir"], -12.83, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["confronto"]["delta"], 0.0)
        self.assertFalse(bc["confronto"]["conviene"])

    def test_prezzo_eccesso_negativo(self):
        # Con prezzo eccesso meno 0,02 si viene pagati
        # per consumare: VAN 512123,23, TIR 55,69 %,
        # payback 2, delta eccesso 170660,00.
        bc = mh895_calcola(**_demo_kwargs(p_eccesso=-0.02))
        self.assertAlmostEqual(bc["van"], 512123.23, places=2)
        self.assertAlmostEqual(bc["tir"], 55.69, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["confronto"]["delta"], 170660.00,
                               places=2)
        self.assertTrue(bc["confronto"]["conviene"])

    def test_prezzo_eccesso_zero(self):
        # Con prezzo eccesso zero le ore in eccesso
        # costano zero: VAN 416528,39, delta 126500,00.
        bc = mh895_calcola(**_demo_kwargs(p_eccesso=0.0))
        self.assertAlmostEqual(bc["van"], 416528.39, places=2)
        self.assertAlmostEqual(bc["tir"], 47.18, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertAlmostEqual(bc["confronto"]["delta"], 126500.00,
                               places=2)

    def test_prezzo_pieno_alto_non_convente(self):
        # Con prezzo pieno 0,15 EUR/kWh il margine
        # crolla a 10460,00: VAN meno 254713,67, TIR
        # meno 39,49 %, payback nessuno.
        bc = mh895_calcola(**_demo_kwargs(p_pieno=0.15))
        self.assertAlmostEqual(bc["margine"], 10460.00, places=2)
        self.assertAlmostEqual(bc["van"], -254713.67, places=2)
        self.assertAlmostEqual(bc["tir"], -39.49, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_tolleranza_zero_bordo(self):
        # Con tolleranza zero ogni VAN negativa e'
        # NON_CONVIENTE, anche quella a hashprice 43.
        bc = mh895_calcola(**_demo_kwargs(hashprice=43,
                                          tolleranza_pct=0))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "NON_CONVIENTE")
        bc = mh895_calcola(**_demo_kwargs(tolleranza_pct=0))
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_costo_miner_zero_tir_non_definita_payback_zero(self):
        bc = mh895_calcola(**_demo_kwargs(costo_miner=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(n_miner="100")
        self.assertRaises(ValueError, mh895_calcola, **kw)
        kw = _demo_kwargs(n_miner=True)
        self.assertRaises(ValueError, mh895_calcola, **kw)
        val = mh895_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def895\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh895_demo().keys()), lette - set(mh895_demo().keys()))
        self.assertEqual(lette, set(mh895_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc895\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc895\["([^"]+)"\]', src))
        attese = set(mh895_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 894 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 895.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 897)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab895:"), 1)
        self.assertTrue(src.startswith("    # W900"))

    def test_ui_tab895_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab895:"), 1)
        self.assertIn("def mh895_demo(", src_h)
        self.assertIn("def mh895_calcola(", src_h)
        self.assertIn("tab895", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Bitcoin mining: il miner come carico flessibile monetizza l'energia in eccesso?", src)
        self.assertIn("⛏️💰 Bitcoin mining: il miner come carico flessibile monetizza l'energia in eccesso?", src)
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
        chiavi = re.findall(r'key="(st895_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st895_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st895_calcola"', src)
        self.assertIn('key="st895_csv"', src)
        self.assertIn('key="st895_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg895"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("_marg895 <= 0.0", src)

    def test_ui_tutti_gli_slider_minimo_zero_tranne_prezzo_eccesso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"st\.slider\(", src):
            finestra = src[m.start():m.start() + 400]
            if "Prezzo eccesso" in finestra:
                self.assertIn("min_value=-0.10", finestra)
            else:
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
