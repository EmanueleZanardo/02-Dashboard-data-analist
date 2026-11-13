"""Test nuova scheda Cannibalizzazione FV: il prezzo catturato crolla
con la penetrazione solare?
Repo path: tests/test_w899_cannibalizzazione.py

Effetto SISTEMA (non profilo singolo): il prezzo catturato stesso cade
al crescere della penetrazione solare nel sistema (cannibalizzazione,
value factor). Impianto FV nuovo da 10000 kWp con 1050 h/anno: E =
10000 per 1050 diviso 1000 = 10500 MWh/anno; CAPEX = 10000 per 800 =
8000000 EUR; OPEX = 10000 per 15 = 150000 EUR/anno; vita 25 anni;
tasso 0,05 (frazione); CRF = 0,05 per 1,05 elevato a 25 diviso (1,05
elevato a 25 meno 1) = 0,07095; fattore di rendita a = (1 meno 1,05
elevato a meno 25) diviso 0,05 = 14,0939; LCOE = (8000000 per 0,07095
piu 150000) diviso 10500 = 68,34 EUR/MWh. Prezzo base 90 EUR/MWh
(ipotesi esplicita, costante negli scenari); k = 1,5 (elasticita
cannibalizzazione, ipotesi esplicita); VF(pi) = 1 meno k per pi;
p_cap(pi) = 90 per VF(pi); R(pi) = 10500 per p_cap(pi); margine =
p_cap meno LCOE; VAN(pi) = (R(pi) meno 150000) per 14,0939 meno
8000000; TIR per bisezione su flussi [meno 8000000, (R meno 150000)
per 25] con intervallo da meno 0,9 a 5,0; payback (primo anno con
cumulato maggiore o uguale a 0); pi_star = (1 meno 68,34 diviso 90)
diviso 1,5 = 0,1604 (16,04 %).
Scenari demo: pi 0,10: VF 0,85, p_cap 76,50, R 803250,00, margine
8,16, VAN 1206869,29, TIR 6,46 %, payback 13, CONVIENTE; pi 0,20: VF
0,70, p_cap 63,00, R 661500,00, margine meno 5,34, VAN meno 790947,35,
TIR 3,99 %, payback 16, MARGINALE (valore assoluto VAN 790947,35
entro 10 % del CAPEX, 800000,00 EUR); pi 0,30: VF 0,55, p_cap 49,50,
R 519750,00, margine meno 18,84, VAN meno 2788764,00, TIR 1,14 %,
payback 22, NON_CONVIENTE; pi 0,40: VF 0,40, p_cap 36,00, R
378000,00, margine meno 32,34, VAN meno 4786580,64, TIR meno 2,45 %,
payback nessuno, NON_CONVIENTE.
Mitigazioni a pi 0,30 (p_cap base 49,50): batteria 5 MWh, quota
shiftata 15 %, uplift piu 30 EUR/MWh su quella quota (p_cap 54,00,
R 567000,00, CAPEX totale 9500000,00, OPEX totale 180000,00, VAN
meno 4045643,45, TIR 0,14 %, payback 25, NON_CONVIENTE: la batteria
non ripaga il suo CAPEX); PPA fisso 75 EUR/MWh (R 787500,00, VAN
984889,66, TIR 6,20 %, payback 13, CONVIENTE); est ovest (E 9660,00,
p_cap 54,45, R 525987,00, VAN meno 2700860,06, TIR 1,28 %, payback
22, NON_CONVIENTE).
Tolleranza in PERCENTUALE (10 = 10 % del CAPEX). Il tasso e in
FRAZIONE (0,05 = 5 %), usato diretto, NON diviso per 100. I flussi
piatti sono una SEMPLIFICAZIONE DICHIARATA (profilo reale variabile
con clima, carico e prezzi, qui valore medio costante); la taglia
batteria in MWh non entra nella formula (conta la quota di energia
spostata). Verdetto principale a penetrazione mitigazioni 0,30:
NON_CONVIENTE.
Verdetto: NON_CALCOLABILE se input degenere (potenza nulla o
negativa, ore equivalenti nulle o negative, CAPEX o OPEX specifici
negativi, vita nulla o negativa o non intera, tasso nullo o negativo
o maggiore o uguale a 1, prezzo base nullo o negativo, k nullo o
negativo, penetrazione sotto 0 o sopra 0,66, tolleranza negativa,
batteria negativa, quota shiftata sotto 0 o sopra 1, uplift negativo,
CAPEX o OPEX batteria negativi, prezzo PPA negativo, fattori est
ovest nulli o negativi, penetrazione mitigazioni sotto 0 o sopra
0,66) (guard degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN maggiore di 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX, NON_CONVIENTE altrimenti.
Casi limite: pi zero (p_cap 90,00, VAN 3204685,93, TIR 8,70 %,
payback 11, CONVIENTE); pi 0,66 (p_cap 0,90, VAN meno 9980903,91,
TIR non definita, payback nessuno); k 3 con pi 0,50 (VF meno 0,50,
p_cap meno 45,00, VAN meno 16773480,49, TIR non definita: il modello
resta calcolabile, verdetto NON_CONVIENTE); batteria con quota zero
(p_cap 49,50, VAN meno 4711582,33, TIR meno 0,84 %, payback nessuno);
PPA zero (VAN meno 10114091,68, TIR non definita); est ovest con
fattori 1,0 (uguale allo scenario base a pi 0,30); CAPEX zero (TIR
non definita, payback 0, VAN 9206869,29 a pi 0,10); tasso zero
degenere (ValueError negli helper, guard NON_CALCOLABILE in UI);
p_base uguale a LCOE (pi_star zero).
Distinzione esplicita: qui SOLO la curva di valore contro
penetrazione solare di SISTEMA (prezzo catturato che cade con pi,
value factor VF = 1 meno k per pi), NIENTE price capture di UN
profilo contro lo spot orario (li il profilo e dato), NIENTE prezzi
negativi (li il fenomeno orario, ore sotto soglia), NIENTE matching
PPA (li il contratto: qui il PPA e solo una mitigazione), NIENTE
LCOE da solo (li il costo livellato: qui LCOE contro prezzo
catturato che cade, con VAN e TIR per scenario).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w899_helpers import (
        demo_calcoli,
        mh894_calcola,
        mh894_capex,
        mh894_crf,
        mh894_csv,
        mh894_demo,
        mh894_demo_calcoli,
        mh894_energia,
        mh894_fattore_rendita,
        mh894_flussi,
        mh894_frazione,
        mh894_int_pos,
        mh894_lcoe,
        mh894_mitigazioni,
        mh894_nneg,
        mh894_num,
        mh894_opex,
        mh894_payback,
        mh894_pi,
        mh894_pi_star,
        mh894_p_cap,
        mh894_pos,
        mh894_ricavo,
        mh894_scenario,
        mh894_sensibilita,
        mh894_tasso,
        mh894_tir,
        mh894_valida,
        mh894_van,
        mh894_van_scenario,
        mh894_verdetto,
        mh894_vf,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w899_helpers", os.path.join(_hf, "w899_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh894_calcola = _mod.mh894_calcola
    mh894_capex = _mod.mh894_capex
    mh894_crf = _mod.mh894_crf
    mh894_csv = _mod.mh894_csv
    mh894_demo = _mod.mh894_demo
    mh894_demo_calcoli = _mod.mh894_demo_calcoli
    mh894_energia = _mod.mh894_energia
    mh894_fattore_rendita = _mod.mh894_fattore_rendita
    mh894_flussi = _mod.mh894_flussi
    mh894_frazione = _mod.mh894_frazione
    mh894_int_pos = _mod.mh894_int_pos
    mh894_lcoe = _mod.mh894_lcoe
    mh894_mitigazioni = _mod.mh894_mitigazioni
    mh894_nneg = _mod.mh894_nneg
    mh894_num = _mod.mh894_num
    mh894_opex = _mod.mh894_opex
    mh894_payback = _mod.mh894_payback
    mh894_pi = _mod.mh894_pi
    mh894_pi_star = _mod.mh894_pi_star
    mh894_p_cap = _mod.mh894_p_cap
    mh894_pos = _mod.mh894_pos
    mh894_ricavo = _mod.mh894_ricavo
    mh894_scenario = _mod.mh894_scenario
    mh894_sensibilita = _mod.mh894_sensibilita
    mh894_tasso = _mod.mh894_tasso
    mh894_tir = _mod.mh894_tir
    mh894_valida = _mod.mh894_valida
    mh894_van = _mod.mh894_van
    mh894_van_scenario = _mod.mh894_van_scenario
    mh894_verdetto = _mod.mh894_verdetto
    mh894_vf = _mod.mh894_vf

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w899_helpers.py")
_UI_PATH = _risolvi("w899_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "3"
_VECCHIO_TAB = "tab89" + "3"
_VECCHIO_ST = "st89" + "3_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "energia_mwh_anno": 10500.0,
    "capex_eur": 8000000.0,
    "opex_eur_anno": 150000.0,
    "crf": 0.0709524572992296,
    "fattore_rendita": 14.093944566044762,
    "lcoe": 68.3447293708416,
    "pi_star": 0.16040941206783996,
    "p_cap_pi_mitigazione": 49.50000000000001,
    "van_pi_mitigazione": -2788763.996704948,
    "tir_pi_mitigazione": 1.1439370295698799,
    "payback_pi_mitigazione": 22,
}

_DEMO_SCENARI = [
    {"pi": 0.10, "vf": 0.85, "p_cap": 76.5,
     "ricavo": 803250.0, "margine_unitario": 8.155270629158395,
     "netto_annuo": 653250.0, "van": 1206869.2877687402,
     "tir": 6.457084829003746, "payback": 13,
     "verdetto": "CONVIENTE"},
    {"pi": 0.20, "vf": 0.7, "p_cap": 62.99999999999999,
     "ricavo": 661499.9999999999, "margine_unitario": -5.344729370841613,
     "netto_annuo": 511499.9999999999, "van": -790947.3544681063,
     "tir": 3.988991196327444, "payback": 16,
     "verdetto": "MARGINALE"},
    {"pi": 0.30, "vf": 0.55, "p_cap": 49.50000000000001,
     "ricavo": 519750.00000000006, "margine_unitario": -18.8447293708416,
     "netto_annuo": 369750.00000000006, "van": -2788763.996704948,
     "tir": 1.1439370295698799, "payback": 22,
     "verdetto": "NON_CONVIENTE"},
    {"pi": 0.40, "vf": 0.3999999999999999, "p_cap": 35.99999999999999,
     "ricavo": 377999.99999999994, "margine_unitario": -32.34472937084161,
     "netto_annuo": 227999.99999999994, "van": -4786580.638941795,
     "tir": -2.4538398402881993, "payback": None,
     "verdetto": "NON_CONVIENTE"},
]

_DEMO_MITIGAZIONI = {
    "batteria": {"p_cap": 54.0, "energia_mwh_anno": 10500.0,
                 "ricavo": 567000.0, "capex_totale": 9500000.0,
                 "opex_totale": 180000.0, "netto_annuo": 387000.0,
                 "van": -4045643.4529406773,
                 "tir": 0.14090679129992284, "payback": 25,
                 "verdetto": "NON_CONVIENTE"},
    "ppa": {"p_cap": 75.0, "energia_mwh_anno": 10500.0,
            "ricavo": 787500.0, "capex_totale": 8000000.0,
            "opex_totale": 150000.0, "netto_annuo": 637500.0,
            "van": 984889.6608535349,
            "tir": 6.195728589007668, "payback": 13,
            "verdetto": "CONVIENTE"},
    "est_ovest": {"p_cap": 54.45000000000001,
                  "energia_mwh_anno": 9660.0,
                  "ricavo": 525987.0000000001,
                  "capex_totale": 8000000.0,
                  "opex_totale": 150000.0, "netto_annuo": 375987.0000000001,
                  "van": -2700860.0644465266,
                  "tir": 1.2807545752053748, "payback": 22,
                  "verdetto": "NON_CONVIENTE"},
}

_ORDINE_VALIDA = (
    "p_kwp", "h_eq", "capex_eur_kwp", "opex_eur_kwp",
    "vita_anni", "tasso", "p_base", "k", "penetrazioni",
    "tolleranza_pct", "batt_mwh", "quota_shift", "uplift_batt",
    "capex_batt", "opex_batt", "p_ppa", "fattore_ew_energia",
    "fattore_ew_prezzo", "pi_mitigazione")


def _demo_kwargs(**over):
    kw = dict(mh894_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh894_num(3, "x"), 3.0)
        self.assertEqual(mh894_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh894_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh894_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh894_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh894_pos(0, "x")
        with self.assertRaises(ValueError):
            mh894_pos(-1, "x")
        self.assertEqual(mh894_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh894_int_pos(25, "x"), 25)
        self.assertEqual(mh894_int_pos(25.0, "x"), 25)
        with self.assertRaises(ValueError):
            mh894_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh894_int_pos(25.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh894_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh894_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh894_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh894_frazione(1.1, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh894_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh894_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh894_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh894_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh894_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh894_tasso(-0.01, "x")

    def test_pi_intervallo(self):
        self.assertEqual(mh894_pi(0.0, "x"), 0.0)
        self.assertEqual(mh894_pi(0.66, "x"), 0.66)
        self.assertEqual(mh894_pi(0.30, "x"), 0.30)
        with self.assertRaises(ValueError):
            mh894_pi(-0.01, "x")
        with self.assertRaises(ValueError):
            mh894_pi(0.67, "x")
        with self.assertRaises(ValueError):
            mh894_pi(1.0, "x")


class TestFisica(unittest.TestCase):
    def test_energia_capex_opex(self):
        self.assertEqual(mh894_energia(10000, 1050), 10500.0)
        self.assertEqual(mh894_energia(5000, 1000), 5000.0)
        self.assertEqual(mh894_capex(10000, 800), 8000000.0)
        self.assertEqual(mh894_capex(10000, 0), 0.0)
        self.assertEqual(mh894_opex(10000, 15), 150000.0)
        self.assertEqual(mh894_opex(10000, 0), 0.0)
        with self.assertRaises(ValueError):
            mh894_energia(0, 1050)
        with self.assertRaises(ValueError):
            mh894_energia(10000, 0)
        with self.assertRaises(ValueError):
            mh894_capex(10000, -1)

    def test_crf_e_fattore_rendita(self):
        self.assertAlmostEqual(mh894_crf(0.05, 25), 0.07095, places=5)
        self.assertAlmostEqual(mh894_fattore_rendita(0.05, 25),
                               14.0939, places=4)
        # CRF per fattore di rendita = 1: identita'
        # finanziaria (CRF = 1 diviso a, con a fattore di rendita).
        self.assertAlmostEqual(
            mh894_crf(0.05, 25) * mh894_fattore_rendita(0.05, 25),
            1.0, places=9)
        self.assertAlmostEqual(mh894_crf(0.10, 10), 0.16275, places=5)
        self.assertAlmostEqual(mh894_fattore_rendita(0.10, 10),
                               6.1446, places=4)
        with self.assertRaises(ValueError):
            mh894_crf(0.0, 25)
        with self.assertRaises(ValueError):
            mh894_fattore_rendita(1.0, 25)

    def test_lcoe(self):
        self.assertAlmostEqual(
            mh894_lcoe(8000000, 150000, 10500, 0.0709524572992296),
            68.34, places=2)
        self.assertAlmostEqual(
            mh894_lcoe(8000000, 150000, 10500,
                       mh894_crf(0.05, 25)),
            68.3447293708416, places=9)
        # Con CAPEX zero l'LCOE e' solo OPEX diviso energia.
        self.assertAlmostEqual(mh894_lcoe(0, 150000, 10500,
                                          mh894_crf(0.05, 25)),
                               14.2857, places=4)
        with self.assertRaises(ValueError):
            mh894_lcoe(8000000, 150000, 0, 0.07095)

    def test_vf_decrescente_in_pi(self):
        self.assertAlmostEqual(mh894_vf(0.10, 1.5), 0.85)
        self.assertAlmostEqual(mh894_vf(0.20, 1.5), 0.70)
        self.assertAlmostEqual(mh894_vf(0.30, 1.5), 0.55)
        self.assertAlmostEqual(mh894_vf(0.40, 1.5), 0.40)
        self.assertEqual(mh894_vf(0.0, 1.5), 1.0)
        self.assertAlmostEqual(mh894_vf(0.66, 1.5), 0.01)
        # Con k 1,0 la caduta e' piu' lenta; con k 2,0 piu' ripida.
        self.assertAlmostEqual(mh894_vf(0.30, 1.0), 0.70)
        self.assertAlmostEqual(mh894_vf(0.30, 2.0), 0.40)
        # Con k 3,0 e pi 0,50 il fattore di valore diventa negativo:
        # il modello resta calcolabile, non solleva.
        self.assertAlmostEqual(mh894_vf(0.50, 3.0), -0.50)
        with self.assertRaises(ValueError):
            mh894_vf(0.10, 0)
        with self.assertRaises(ValueError):
            mh894_vf(0.67, 1.5)

    def test_p_cap_e_ricavo(self):
        self.assertAlmostEqual(mh894_p_cap(90, 0.85), 76.50)
        self.assertAlmostEqual(mh894_p_cap(90, 0.55), 49.50)
        self.assertEqual(mh894_p_cap(90, 1.0), 90.0)
        self.assertEqual(mh894_p_cap(90, 0.0), 0.0)
        self.assertEqual(mh894_ricavo(10500, 76.5), 803250.0)
        self.assertEqual(mh894_ricavo(10500, 49.5), 519750.0)
        with self.assertRaises(ValueError):
            mh894_p_cap(0, 0.85)
        with self.assertRaises(ValueError):
            mh894_ricavo(0, 76.5)

    def test_van_scenario(self):
        self.assertAlmostEqual(
            mh894_van_scenario(803250.0, 150000, 14.093944566044762,
                               8000000),
            1206869.29, places=2)
        self.assertAlmostEqual(
            mh894_van_scenario(519750.0, 150000, 14.093944566044762,
                               8000000),
            -2788764.00, places=2)
        # Con ricavo uguale a OPEX la VAN e' meno CAPEX.
        self.assertAlmostEqual(
            mh894_van_scenario(150000, 150000, 14.093944566044762,
                               8000000),
            -8000000.0, places=2)

    def test_pi_star(self):
        self.assertAlmostEqual(
            mh894_pi_star(68.3447293708416, 90, 1.5),
            0.1604, places=4)
        # Con prezzo base uguale a LCOE la pareggio e' zero.
        self.assertAlmostEqual(
            mh894_pi_star(68.3447293708416, 68.3447293708416, 1.5),
            0.0, places=9)
        # Con LCOE sopra il prezzo base la pareggio e' negativa:
        # mai conveniente, nemmeno a penetrazione zero.
        self.assertLess(mh894_pi_star(100.0, 90, 1.5), 0.0)
        # Con k piu' basso la pareggio si sposta piu' in alto.
        self.assertAlmostEqual(
            mh894_pi_star(68.3447293708416, 90, 1.0),
            0.2406, places=4)
        with self.assertRaises(ValueError):
            mh894_pi_star(68.34, 0, 1.5)
        with self.assertRaises(ValueError):
            mh894_pi_star(68.34, 90, 0)

    def test_scenario_singolo(self):
        bc = demo_calcoli()
        s = mh894_scenario(0.10, bc["energia_mwh_anno"],
                           bc["p_base"], bc["k"], bc["capex_eur"],
                           bc["opex_eur_anno"],
                           bc["fattore_rendita"], bc["vita_anni"],
                           bc["tolleranza_pct"], bc["lcoe"])
        self.assertAlmostEqual(s["p_cap"], 76.50)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertEqual(len(s["flussi"]), 26)
        s = mh894_scenario(0.40, bc["energia_mwh_anno"],
                           bc["p_base"], bc["k"], bc["capex_eur"],
                           bc["opex_eur_anno"],
                           bc["fattore_rendita"], bc["vita_anni"],
                           bc["tolleranza_pct"], bc["lcoe"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")

    def test_mitigazioni_formule(self):
        bc = demo_calcoli()
        mit = mh894_mitigazioni(
            49.50000000000001, bc["energia_mwh_anno"],
            bc["capex_eur"], bc["opex_eur_anno"],
            bc["fattore_rendita"], bc["vita_anni"],
            bc["tolleranza_pct"], 5, 0.15, 30, 1500000, 30000, 75,
            0.92, 1.10)
        self.assertAlmostEqual(mit["batteria"]["p_cap"], 54.00)
        self.assertEqual(mit["batteria"]["capex_totale"], 9500000.0)
        self.assertEqual(mit["batteria"]["opex_totale"], 180000.0)
        self.assertAlmostEqual(mit["ppa"]["p_cap"], 75.0)
        self.assertEqual(mit["ppa"]["capex_totale"], 8000000.0)
        self.assertAlmostEqual(mit["est_ovest"]["energia_mwh_anno"],
                               9660.0)
        self.assertAlmostEqual(mit["est_ovest"]["p_cap"], 54.45)
        self.assertEqual(mit["est_ovest"]["capex_totale"], 8000000.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh894_flussi(8000000, 653250.0, 3),
                         [-8000000, 653250.0, 653250.0, 653250.0])

    def test_van_tasso_cinque(self):
        bc = mh894_demo_calcoli()
        self.assertAlmostEqual(
            mh894_van(bc["scenari"][0]["flussi"], 0.05),
            bc["scenari"][0]["van"])
        self.assertAlmostEqual(
            mh894_van(bc["scenari"][2]["flussi"], 0.05),
            bc["scenari"][2]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh894_van([-8000000, 653250.0, 653250.0], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # a pi 0,10 e' 1206869,29; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh894_demo_calcoli()
        self.assertAlmostEqual(
            mh894_van(bc["scenari"][0]["flussi"], 0.05),
            1206869.29, places=2)
        self.assertNotAlmostEqual(
            mh894_van(bc["scenari"][0]["flussi"], 0.50),
            1206869.29, places=2)
        with self.assertRaises(ValueError):
            mh894_van(bc["scenari"][0]["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh894_demo_calcoli()
        tir = mh894_tir(bc["scenari"][0]["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0,
                               bc["scenari"][0]["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh894_tir([-100, -10, -10]))
        self.assertIsNone(mh894_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh894_demo_calcoli()
        self.assertEqual(mh894_payback(bc["scenari"][0]["flussi"]), 13)
        self.assertIsNone(mh894_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh894_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh894_demo_calcoli()
        f0 = bc["scenari"][0]["flussi"]
        self.assertAlmostEqual(sum(f0[:13]), -161000.00, places=2)
        self.assertAlmostEqual(sum(f0[:14]), 492250.00, places=2)
        f1 = bc["scenari"][1]["flussi"]
        self.assertAlmostEqual(sum(f1[:16]), -327500.00, places=2)
        self.assertAlmostEqual(sum(f1[:17]), 184000.00, places=2)
        f2 = bc["scenari"][2]["flussi"]
        self.assertAlmostEqual(sum(f2[:22]), -235250.00, places=2)
        self.assertAlmostEqual(sum(f2[:23]), 134500.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(mh894_verdetto(100.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh894_verdetto(-50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh894_verdetto(-150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh894_verdetto(0.0, 1000, 10), "MARGINALE")
        # VAN esattamente alla tolleranza: MARGINALE (inclusa).
        self.assertEqual(mh894_verdetto(-100.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh894_verdetto(-100.01, 1000, 10),
                         "NON_CONVIENTE")
        # Con tolleranza zero solo VAN zero e' MARGINALE.
        self.assertEqual(mh894_verdetto(-1.0, 1000, 0), "NON_CONVIENTE")
        self.assertEqual(mh894_verdetto(0.0, 1000, 0), "MARGINALE")

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(mh894_verdetto(None, 8000000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh894_demo()
        val = mh894_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(vita_anni=25.5)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10)
        bc = mh894_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh894_calcola(**_demo_kwargs(tasso=tasso))
        bc = mh894_calcola(**_demo_kwargs(tasso=0.10))
        self.assertEqual(bc["tasso"], 0.10)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("p_kwp", 0),
                              ("h_eq", 0),
                              ("p_base", 0),
                              ("k", 0),
                              ("fattore_ew_energia", 0),
                              ("fattore_ew_prezzo", 0)):
            with self.assertRaises(ValueError):
                mh894_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_pi_sopra_tetto_no(self):
        kw = _demo_kwargs(penetrazioni=[0.67])
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(penetrazioni=[-0.01])
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(pi_mitigazione=0.67)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(pi_mitigazione=-0.01)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_valida_penetrazioni_non_lista_e_vuota_no(self):
        kw = _demo_kwargs(penetrazioni=0.30)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(penetrazioni=[])
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(penetrazioni=[0.30, float("nan")])
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_valida_quota_sopra_uno_no(self):
        kw = _demo_kwargs(quota_shift=1.1)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(quota_shift=-0.1)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_base=float("nan"))
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("p_kwp", -1),
                              ("h_eq", -1),
                              ("capex_eur_kwp", -1),
                              ("opex_eur_kwp", -1),
                              ("tasso", -0.01),
                              ("p_base", -1),
                              ("k", -1),
                              ("tolleranza_pct", -1),
                              ("batt_mwh", -1),
                              ("quota_shift", -0.1),
                              ("uplift_batt", -1),
                              ("capex_batt", -1),
                              ("opex_batt", -1),
                              ("p_ppa", -1),
                              ("fattore_ew_energia", -1),
                              ("fattore_ew_prezzo", -1),
                              ("pi_mitigazione", -0.01)):
            with self.assertRaises(ValueError):
                mh894_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh894_calcola(mh894_demo())
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 4)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh894_calcola(dict(mh894_demo(), capex_eur_kwp=9999),
                           capex_eur_kwp=800)
        self.assertEqual(bc["capex_eur"], 8000000.0)


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

    def test_demo_mitigazioni(self):
        bc = demo_calcoli()
        for nome, atteso in _DEMO_MITIGAZIONI.items():
            for chiave, valore in atteso.items():
                with self.subTest(mitigazione=nome, chiave=chiave):
                    ottenuto = bc["mitigazioni"][nome][chiave]
                    if valore is None or isinstance(valore, (int, str)):
                        self.assertEqual(ottenuto, valore)
                    else:
                        self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_verdetto_principale(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenario_pi_mitigazione"]["verdetto"],
                         "NON_CONVIENTE")
        self.assertLess(bc["van_pi_mitigazione"], 0.0)
        self.assertGreater(abs(bc["van_pi_mitigazione"]),
                           bc["tolleranza_pct"] / 100.0
                           * bc["capex_eur"])
        self.assertEqual(bc["payback_pi_mitigazione"], 22)
        self.assertAlmostEqual(bc["tir_pi_mitigazione"], 1.14, places=2)
        self.assertAlmostEqual(bc["pi_star"], 0.16, places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["energia_mwh_anno"],
            bc["p_kwp"] * bc["h_eq"] / 1000.0)
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["p_kwp"] * bc["capex_eur_kwp"])
        self.assertAlmostEqual(
            bc["opex_eur_anno"],
            bc["p_kwp"] * bc["opex_eur_kwp"])
        self.assertAlmostEqual(
            bc["lcoe"],
            (bc["capex_eur"] * bc["crf"] + bc["opex_eur_anno"])
            / bc["energia_mwh_anno"])
        self.assertAlmostEqual(
            bc["pi_star"],
            (1.0 - bc["lcoe"] / bc["p_base"]) / bc["k"])
        for s in bc["scenari"]:
            self.assertAlmostEqual(s["vf"], 1.0 - bc["k"] * s["pi"])
            self.assertAlmostEqual(s["p_cap"], bc["p_base"] * s["vf"])
            self.assertAlmostEqual(
                s["ricavo"], bc["energia_mwh_anno"] * s["p_cap"])
            self.assertAlmostEqual(
                s["margine_unitario"], s["p_cap"] - bc["lcoe"])
            self.assertAlmostEqual(
                s["van"],
                (s["ricavo"] - bc["opex_eur_anno"])
                * bc["fattore_rendita"] - bc["capex_eur"])
            self.assertAlmostEqual(
                s["netto_annuo"], s["ricavo"] - bc["opex_eur_anno"])
            self.assertEqual(len(s["flussi"]), bc["vita_anni"] + 1)
        mit = bc["mitigazioni"]
        self.assertAlmostEqual(
            mit["batteria"]["p_cap"],
            0.85 * bc["p_cap_pi_mitigazione"]
            + 0.15 * (bc["p_cap_pi_mitigazione"] + 30))
        self.assertAlmostEqual(mit["ppa"]["p_cap"], 75.0)
        self.assertAlmostEqual(
            mit["est_ovest"]["energia_mwh_anno"],
            0.92 * bc["energia_mwh_anno"])
        self.assertAlmostEqual(
            mit["est_ovest"]["p_cap"],
            1.10 * bc["p_cap_pi_mitigazione"])

    def test_monotonia_prezzo_catturato_e_van(self):
        bc = demo_calcoli()
        p_caps = [s["p_cap"] for s in bc["scenari"]]
        vfs = [s["vf"] for s in bc["scenari"]]
        vans = [s["van"] for s in bc["scenari"]]
        for prima, dopo in zip(p_caps, p_caps[1:]):
            self.assertGreater(prima, dopo)
        for prima, dopo in zip(vfs, vfs[1:]):
            self.assertGreater(prima, dopo)
        for prima, dopo in zip(vans, vans[1:]):
            self.assertGreater(prima, dopo)

    def test_sensibilita_valori(self):
        s = mh894_sensibilita(**mh894_demo())
        self.assertEqual(set(s.keys()),
                         {"p_base_108", "k_100", "k_200",
                          "vita_10", "tasso_010", "capex_doppio"})
        attesi = {
            "p_base_108": (3471061.48, 8.99, 10,
                           -1323698.46, 3.28, 17),
            "k_100": (1872808.17, 7.23, 12,
                      -790947.35, 3.99, 16),
            "k_200": (540930.41, 5.66, 14,
                      -4786580.64, -2.45, None),
            "vita_10": (-2955776.66, -3.52, None,
                        -5144888.51, -12.03, None),
            "tasso_010": (-2070423.61, 6.46, 13,
                          -4643764.45, 1.14, 22),
            "capex_doppio": (-6793130.71, 0.16, 25,
                             -10788764.00, -3.84, None),
        }
        for nome, (van10, tir10, pb10, van30, tir30, pb30) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(
                    s[nome]["scenari"][0]["van"], van10, places=2)
                self.assertAlmostEqual(
                    s[nome]["scenari"][0]["tir"], tir10, places=2)
                self.assertEqual(s[nome]["scenari"][0]["payback"], pb10)
                self.assertAlmostEqual(
                    s[nome]["scenari"][2]["van"], van30, places=2)
                self.assertAlmostEqual(
                    s[nome]["scenari"][2]["tir"], tir30, places=2)
                self.assertEqual(s[nome]["scenari"][2]["payback"], pb30)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van_pi_mitigazione", caso)
            self.assertIn("mitigazioni", caso)

    def test_convente_con_pi_zero(self):
        bc = mh894_calcola(**_demo_kwargs(penetrazioni=[0.0]))
        s = bc["scenari"][0]
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["p_cap"], 90.00, places=2)
        self.assertAlmostEqual(s["van"], 3204685.93, places=2)
        self.assertAlmostEqual(s["tir"], 8.70, places=2)
        self.assertEqual(s["payback"], 11)

    def test_non_convente_con_capex_doppio(self):
        bc = mh894_calcola(**_demo_kwargs(capex_eur_kwp=1600))
        self.assertEqual(bc["scenari"][0]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["scenari"][0]["van"], -6793130.71,
                               places=2)
        self.assertEqual(bc["scenari"][0]["payback"], 25)
        self.assertAlmostEqual(bc["scenari"][2]["van"], -10788764.00,
                               places=2)
        self.assertIsNone(bc["scenari"][2]["payback"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh894_csv(bc, mh894_demo())
        for voce in ("p_kwp", "h_eq", "capex_eur_kwp",
                     "opex_eur_kwp", "vita_anni", "tasso",
                     "p_base", "k", "penetrazioni",
                     "tolleranza_pct", "batt_mwh", "quota_shift",
                     "uplift_batt", "capex_batt", "opex_batt",
                     "p_ppa", "fattore_ew_energia",
                     "fattore_ew_prezzo", "pi_mitigazione",
                     "energia_mwh_anno", "capex_eur",
                     "opex_eur_anno", "crf", "fattore_rendita",
                     "lcoe", "pi_star",
                     "p_cap_pi_mitigazione", "van_pi_mitigazione",
                     "tir_pi_mitigazione", "payback_pi_mitigazione",
                     "scenario_10_vf", "scenario_10_p_cap",
                     "scenario_10_van", "scenario_10_verdetto",
                     "scenario_20_van", "scenario_30_van",
                     "scenario_40_van",
                     "mit_batteria_p_cap", "mit_batteria_van",
                     "mit_ppa_p_cap", "mit_ppa_van",
                     "mit_est_ovest_p_cap", "mit_est_ovest_van",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("NON_CONVIENTE", csv)
        self.assertIn("CONVIENTE", csv)
        self.assertIn("MARGINALE", csv)

    def test_df_scenari_mitigazioni_curva_flussi_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 4)
        self.assertEqual(len(bc["df_mitigazioni"]), 3)
        self.assertEqual(len(bc["df_curva"]), 34)
        self.assertEqual(len(bc["df_flussi"]), 26)
        self.assertEqual(len(bc["df_tabella"]), 27)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -8000000.0)
        self.assertAlmostEqual(
            bc["df_curva"]["Prezzo catturato (EUR/MWh)"].iloc[0], 90.0)
        self.assertAlmostEqual(
            bc["df_curva"]["Prezzo catturato (EUR/MWh)"].iloc[-1], 0.90,
            places=2)
        self.assertAlmostEqual(
            bc["df_curva"]["Penetrazione"].iloc[-1], 0.66)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Potenza (kWp)", voci)
        self.assertIn("LCOE (EUR/MWh)", voci)
        self.assertIn("Penetrazione di pareggio", voci)
        self.assertIn("Verdetto a penetrazione mitigazioni", voci)
        self.assertIn("Prezzo catturato (EUR/MWh)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Mitigazione",
                      set(bc["df_mitigazioni"].columns))

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh894_csv(bc, mh894_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("energia_mwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh894_demo_calcoli()["lcoe"],
                         demo_calcoli()["lcoe"])
        self.assertEqual(mh894_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh894_calcola(**_demo_kwargs(capex_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["scenari"][0]["van"], 9206869.29,
                               places=2)
        self.assertIsNone(bc["scenari"][0]["tir"])
        self.assertEqual(bc["scenari"][0]["payback"], 0)
        self.assertEqual(bc["scenari"][0]["verdetto"], "CONVIENTE")
        bc = mh894_calcola(**_demo_kwargs(opex_eur_kwp=0))
        self.assertEqual(bc["opex_eur_anno"], 0.0)
        self.assertGreater(bc["scenari"][0]["van"], 1206869.29)


class TestCasiLimite(unittest.TestCase):
    def test_vita_zero_non_calcolabile(self):
        # Vita zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        self.assertFalse(mh894_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_vita_non_intera_non_calcolabile(self):
        kw = _demo_kwargs(vita_anni=25.5)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_potenza_e_ore_zero_non_calcolabili(self):
        kw = _demo_kwargs(p_kwp=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(h_eq=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_tasso_zero_e_uno_non_calcolabili(self):
        kw = _demo_kwargs(tasso=0.0)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(tasso=1.0)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_p_base_e_k_zero_non_calcolabili(self):
        kw = _demo_kwargs(p_base=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(k=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_pi_fuori_tetto_non_calcolabile(self):
        kw = _demo_kwargs(penetrazioni=[0.10, 0.67])
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(pi_mitigazione=0.67)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_quota_sopra_uno_non_calcolabile(self):
        kw = _demo_kwargs(quota_shift=1.1)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_fattori_ew_zero_non_calcolabili(self):
        kw = _demo_kwargs(fattore_ew_energia=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)
        kw = _demo_kwargs(fattore_ew_prezzo=0)
        self.assertRaises(ValueError, mh894_calcola, **kw)

    def test_pi_zero_convente(self):
        # Con pi zero il prezzo catturato e' il prezzo
        # base (90) e la VAN 3204685,93: CONVIENTE.
        bc = mh894_calcola(**_demo_kwargs(penetrazioni=[0.0]))
        s = bc["scenari"][0]
        self.assertAlmostEqual(s["vf"], 1.0)
        self.assertAlmostEqual(s["p_cap"], 90.00, places=2)
        self.assertAlmostEqual(s["ricavo"], 945000.00, places=2)
        self.assertAlmostEqual(s["van"], 3204685.93, places=2)
        self.assertAlmostEqual(s["tir"], 8.70, places=2)
        self.assertEqual(s["payback"], 11)
        self.assertEqual(s["verdetto"], "CONVIENTE")

    def test_pi_066_prezzo_quasi_zero(self):
        # Con pi 0,66 il fattore di valore e' 0,01 e il
        # prezzo catturato 0,90: VAN meno 9980903,91,
        # TIR non definita, payback nessuno.
        bc = mh894_calcola(**_demo_kwargs(penetrazioni=[0.66]))
        s = bc["scenari"][0]
        self.assertAlmostEqual(s["vf"], 0.01, places=2)
        self.assertAlmostEqual(s["p_cap"], 0.90, places=2)
        self.assertAlmostEqual(s["ricavo"], 9450.00, places=2)
        self.assertAlmostEqual(s["van"], -9980903.91, places=2)
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")

    def test_k_alto_vf_negativo_calcolabile(self):
        # Con k 3,0 e pi 0,50 il fattore di valore e'
        # meno 0,50 e il prezzo catturato meno 45,00:
        # il modello resta calcolabile, verdetto
        # NON_CONVIENTE, TIR non definita.
        bc = mh894_calcola(**_demo_kwargs(k=3.0, penetrazioni=[0.5]))
        s = bc["scenari"][0]
        self.assertAlmostEqual(s["vf"], -0.50)
        self.assertAlmostEqual(s["p_cap"], -45.00)
        self.assertAlmostEqual(s["ricavo"], -472500.00, places=2)
        self.assertAlmostEqual(s["van"], -16773480.49, places=2)
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")

    def test_batteria_quota_zero(self):
        # Con quota shiftata zero la batteria non
        # alza il prezzo catturato (49,50) ma aggiunge
        # CAPEX e OPEX: VAN meno 4711582,33, TIR
        # meno 0,84 %, payback nessuno.
        bc = mh894_calcola(**_demo_kwargs(quota_shift=0.0))
        m = bc["mitigazioni"]["batteria"]
        self.assertAlmostEqual(m["p_cap"], 49.50, places=2)
        self.assertAlmostEqual(m["van"], -4711582.33, places=2)
        self.assertAlmostEqual(m["tir"], -0.84, places=2)
        self.assertIsNone(m["payback"])
        self.assertEqual(m["verdetto"], "NON_CONVIENTE")

    def test_ppa_zero(self):
        # Con PPA zero il ricavo e' zero e la VAN
        # meno 10114091,68, TIR non definita.
        bc = mh894_calcola(**_demo_kwargs(p_ppa=0.0))
        m = bc["mitigazioni"]["ppa"]
        self.assertEqual(m["p_cap"], 0.0)
        self.assertEqual(m["ricavo"], 0.0)
        self.assertAlmostEqual(m["van"], -10114091.68, places=2)
        self.assertIsNone(m["tir"])
        self.assertIsNone(m["payback"])

    def test_ew_fattori_uno_uguale_scenario_base(self):
        # Con fattori est ovest 1,0 la mitigazione
        # coincide con lo scenario base a pi 0,30.
        bc = mh894_calcola(**_demo_kwargs(
            fattore_ew_energia=1.0, fattore_ew_prezzo=1.0))
        m = bc["mitigazioni"]["est_ovest"]
        s = bc["scenario_pi_mitigazione"]
        self.assertAlmostEqual(m["p_cap"], s["p_cap"])
        self.assertAlmostEqual(m["ricavo"], s["ricavo"])
        self.assertAlmostEqual(m["van"], s["van"])
        self.assertEqual(m["verdetto"], s["verdetto"])

    def test_p_base_uguale_lcoe_pi_star_zero(self):
        # Con prezzo base uguale a LCOE la
        # penetrazione di pareggio e' zero.
        bc = mh894_calcola(
            **_demo_kwargs(p_base=68.3447293708416))
        self.assertAlmostEqual(bc["pi_star"], 0.0, places=9)

    def test_tolleranza_zero_bordo(self):
        # Con tolleranza zero ogni VAN negativa e'
        # NON_CONVIENTE, anche quella a pi 0,20.
        bc = mh894_calcola(**_demo_kwargs(tolleranza_pct=0))
        self.assertEqual(bc["scenari"][1]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][0]["verdetto"], "CONVIENTE")
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh894_calcola(**_demo_kwargs(capex_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["scenari"][0]["tir"])
        self.assertEqual(bc["scenari"][0]["payback"], 0)
        self.assertEqual(bc["scenari"][0]["verdetto"], "CONVIENTE")


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def894\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh894_demo().keys()), lette - set(mh894_demo().keys()))
        self.assertEqual(lette, set(mh894_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc894\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc894\["([^"]+)"\]', src))
        attese = set(mh894_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 893 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 894.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 896)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab894:"), 1)
        self.assertTrue(src.startswith("    # W899"))

    def test_ui_tab894_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab894:"), 1)
        self.assertIn("def mh894_demo(", src_h)
        self.assertIn("def mh894_calcola(", src_h)
        self.assertIn("tab894", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Cannibalizzazione FV: il prezzo catturato crolla con la penetrazione solare?", src)
        self.assertIn("☀️📉 Cannibalizzazione FV: il prezzo catturato crolla con la penetrazione solare?", src)
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
        chiavi = re.findall(r'key="(st894_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st894_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st894_calcola"', src)
        self.assertIn('key="st894_csv"', src)
        self.assertIn('key="st894_csv_mitigazioni"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg894"), src.index(".paiac("))
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
