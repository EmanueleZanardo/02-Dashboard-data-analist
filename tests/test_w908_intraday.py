"""Test nuova scheda intraday: l'arbitraggio
intraday con batteria paga?
Repo path: tests/test_w908_intraday.py

Effetto ECONOMICO: una batteria compra energia
nelle aste infragiornaliere MI a prezzo basso e la
rivende in un'asta MI successiva a prezzo piu alto:
lo spread tra prezzo di vendita e prezzo di
acquisto, meno le perdite di round trip, e il
margine per MWh comprato. Compri E_us a p_acq,
rivendi E_us per eta_rt a (p_acq + spread).
Energia usabile E_us = E_mwh * DoD (MWh).
Energia arbitrata E_arb = E_us * cicli_giorno
* giorni_anno (MWh/anno). Margine per MWh
comprato m = eta_rt * spread - (1 - eta_rt)
* p_acq (EUR/MWh). Ricavo lordo = E_arb * m
(EUR/anno). Fee trading = E_arb * fee (EUR/anno,
fee su energia comprata). Margine netto = ricavo
lordo - fee - O&M (EUR/anno). Rendita = (1 -
(1 + r)^-T) / r. Flussi = [-CAPEX, margine
netto * T]; VAN = -CAPEX + margine netto *
rendita. TIR per bisezione sui flussi con
intervallo [-0,9, 5,0] (300 iterazioni, toll
1e-9); payback = primo anno con cumulato netto
>= 0 (None se mai). Breakeven spread S* =
((1 - eta_rt) * p_acq + fee + (O&M + CAPEX /
rendita) / E_arb) / eta_rt (EUR/MWh, spread che
azzera la VAN). Breakeven cicli = E_arb* /
(E_us * giorni_anno) con E_arb* = (O&M + CAPEX /
rendita) / (m - fee) (cicli/giorno, cicli che
azzerano la VAN).
Demo: batteria 10 MW / 20 MWh, mercato MI
italiano. E_mwh 20, DoD 0,90, eta_rt 0,88, cicli
2 al giorno, giorni 350, p_acq 80 EUR/MWh,
spread 65 EUR/MWh, fee 1,5 EUR/MWh, O&M 120.000
EUR/anno, CAPEX 6.000.000 EUR, durata 12 anni,
tasso 0,06 (frazione), tolleranza 0,10
(frazione). E_us = 20 * 0,90 = 18 MWh. E_arb =
18 * 2 * 350 = 12.600 MWh/anno. m = 0,88 * 65 -
0,12 * 80 = 47,60 EUR/MWh. Ricavo lordo =
12.600 * 47,60 = 599.760 EUR/anno. Fee = 12.600
* 1,5 = 18.900 EUR/anno. Margine netto =
599.760 - 18.900 - 120.000 = 460.860 EUR/anno.
Rendita = 8,3838. Margine target = CAPEX /
rendita = 715.662,18 EUR/anno. Flussi
[-6.000.000, 460.860 per 12 anni]; cumulato anno
11 -930.540, anno 12 -469.680, finale -469.680.
VAN = -2.136.221,68 EUR; TIR = -1,23 %;
payback non definito; verdetto NON_CONVIENTE;
breakeven spread = 87,98 EUR/MWh; breakeven
cicli = 2,88 al giorno.
Scenari: base VAN -2.136.221,68, TIR -1,23 %,
payback non definito, NON_CONVIENTE; spread
+30 % (spread 84,50) m 64,76, ricavo lordo
815.976, margine netto 677.076, VAN -323.500,48,
TIR 5,00 %, payback 9, MARGINALE; spread -30 %
(spread 45,50) m 30,44, ricavo lordo 383.544,
margine netto 244.644, VAN -3.948.942,88, TIR
-9,59 %, payback non definito, NON_CONVIENTE;
cicli 3 al giorno E_arb 18.900, ricavo lordo
899.640, fee 28.350, margine netto 751.290, VAN
298.698,11, TIR 6,90 %, payback 8, CONVIENTE;
efficienza 0,80 m 36,00, ricavo lordo 453.600,
margine netto 314.700, VAN -3.361.604,31, TIR
-6,49 %, payback non definito, NON_CONVIENTE.
Confronto: energia usabile 18 contro energia
arbitrata 12.600, margine per MWh 47,60 contro
ricavo lordo 599.760, fee 18.900 contro O&M
120.000, margine netto 460.860 contro CAPEX
6.000.000, rendita 8,3838 contro margine target
715.662,18, VAN -2.136.221,68 contro TIR -1,23 %
contro payback non definito contro breakeven
spread 87,98 contro breakeven cicli 2,88.
Tasso in FRAZIONE (0,06 = 6 %), usato diretto,
NON diviso per 100. Tolleranza in FRAZIONE
(0,10 = 10 % del CAPEX), usata diretta, NON
divisa per 100. Prezzi e spread medi annui
costanti per tutta la durata, SEMPLIFICAZIONE
DICHIARATA (prezzi MI volatili da asta ad asta,
spread che oscilla giorno per giorno, cicli reali
che dipendono dalle opportunita nel mondo reale,
qui valori medi costanti); lo spread puo essere
anche negativo: da margine negativo e quindi
NON_CALCOLABILE, mai un errore di validazione.
Verdetto principale: NON_CONVIENTE.
Verdetto: NON_CALCOLABILE se il margine netto e
minore o uguale a 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV) oppure se un input e
degenere (energia batteria nulla o negativa, DoD
nulla o negativa o sopra 1, efficienza nulla o
negativa o sopra 1, cicli nulli o negativi,
giorni nulli o negativi o sopra 366 o non interi,
prezzo di acquisto negativo, fee negativa, O&M
negativo, CAPEX negativo, durata nulla o negativa
o non intera, tasso nullo o negativo o maggiore o
uguale a 1, tolleranza negativa o sopra 1);
altrimenti CONVIENTE se VAN maggiore di 0,
MARGINALE se VAN minore o uguale a 0 e valore
assoluto della VAN minore o uguale a tolleranza
per CAPEX, NON_CONVIENTE altrimenti.
Casi limite: spread zero (m -9,60, margine netto
-259.860, NON_CALCOLABILE); spread -10 (m -18,40,
margine netto -370.740, NON_CALCOLABILE); spread
al breakeven 87,98 (VAN circa zero, TIR 6,00 %,
payback 9, MARGINALE); cicli al breakeven 2,88
(VAN circa zero, TIR 6,00 %, payback 9,
MARGINALE); CAPEX zero (VAN 3.863.778,32, TIR non
definita, payback 1, CONVIENTE); O&M zero (VAN
-1.130.160,41, TIR 2,39 %, payback 11); durata 1
(VAN -5.565.226,42, TIR non definita perche
-92,32 % fuori dall'intervallo di bisezione,
payback non definito); durata 5 (VAN -4.058.690,03,
TIR -25,27 %, NON_CONVIENTE); tasso 0,10 (VAN
-2.859.841,99, TIR -1,23 %, payback non definito,
NON_CONVIENTE); prezzo di acquisto zero (m 57,20,
VAN -1.122.111,92, TIR 2,41 %, payback 11);
efficienza 0,95 (VAN -1.064.011,88, TIR 2,61 %,
payback 11); cicli 1 (VAN -4.571.141,48, TIR
-13,62 %, NON_CONVIENTE); cicli 4 (VAN
2.733.617,91, TIR 13,61 %, payback 6, CONVIENTE);
giorni 365 (VAN -1.927.514,27, TIR -0,44 %);
DoD 1,0 (VAN -1.595.128,39, TIR 0,77 %, payback
12); durata 20 (VAN -713.972,11, TIR 4,49 %,
payback 14, NON_CONVIENTE); tolleranza zero con
spread +30 % (VAN -323.500,48 diventa
NON_CONVIENTE: la tolleranza decide il confine
MARGINALE).
Distinzione esplicita: qui SOLO l'arbitraggio
intraday con batteria sul mercato MI (compra in
un'asta MI, rivende in un'asta MI successiva,
margine da spread meno perdite di round trip meno
fee meno O&M), NIENTE elenco delle aste MI1 MI7
(la tab277 elenca solo le 7 aste MI1 MI7: qui le
aste sono il mercato dove il trade avviene, non
il conto), NIENTE demand response o UVAM (la
tab669 e un altro meccanismo: li si viene pagati
per ridurre il consumo su chiamata del gestore,
qui si compra e si rivende energia con una
batteria), NIENTE arbitraggio day ahead (li il
prezzo e fissato il giorno prima sul mercato del
giorno prima: qui i prezzi sono quelli
infragiornalieri delle aste MI, piu vicini al
tempo reale), NIENTE vendita di servizi di rete
(li il ricavo e per potenza di riserva o
regolazione: qui il ricavo e solo da
compravendita di energia).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w908_helpers import (
        demo_calcoli,
        mh903_annuity,
        mh903_breakeven_cicli,
        mh903_breakeven_spread,
        mh903_calcola,
        mh903_confronto,
        mh903_csv,
        mh903_demo,
        mh903_demo_calcoli,
        mh903_energia_arbitrata,
        mh903_energia_usabile,
        mh903_fee_annua,
        mh903_flussi,
        mh903_fraz,
        mh903_int_pos,
        mh903_margine_mwh,
        mh903_margine_netto,
        mh903_nneg,
        mh903_num,
        mh903_payback,
        mh903_pos,
        mh903_ricavo_lordo,
        mh903_riga_anno,
        mh903_scenario,
        mh903_sensibilita,
        mh903_serie_annua,
        mh903_tasso,
        mh903_tir,
        mh903_valida,
        mh903_van,
        mh903_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w908_helpers", os.path.join(_hf, "w908_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh903_annuity = _mod.mh903_annuity
    mh903_breakeven_cicli = _mod.mh903_breakeven_cicli
    mh903_breakeven_spread = _mod.mh903_breakeven_spread
    mh903_calcola = _mod.mh903_calcola
    mh903_confronto = _mod.mh903_confronto
    mh903_csv = _mod.mh903_csv
    mh903_demo = _mod.mh903_demo
    mh903_demo_calcoli = _mod.mh903_demo_calcoli
    mh903_energia_arbitrata = _mod.mh903_energia_arbitrata
    mh903_energia_usabile = _mod.mh903_energia_usabile
    mh903_fee_annua = _mod.mh903_fee_annua
    mh903_flussi = _mod.mh903_flussi
    mh903_fraz = _mod.mh903_fraz
    mh903_int_pos = _mod.mh903_int_pos
    mh903_margine_mwh = _mod.mh903_margine_mwh
    mh903_margine_netto = _mod.mh903_margine_netto
    mh903_nneg = _mod.mh903_nneg
    mh903_num = _mod.mh903_num
    mh903_payback = _mod.mh903_payback
    mh903_pos = _mod.mh903_pos
    mh903_ricavo_lordo = _mod.mh903_ricavo_lordo
    mh903_riga_anno = _mod.mh903_riga_anno
    mh903_scenario = _mod.mh903_scenario
    mh903_sensibilita = _mod.mh903_sensibilita
    mh903_serie_annua = _mod.mh903_serie_annua
    mh903_tasso = _mod.mh903_tasso
    mh903_tir = _mod.mh903_tir
    mh903_valida = _mod.mh903_valida
    mh903_van = _mod.mh903_van
    mh903_verdetto = _mod.mh903_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w908_helpers.py")
_UI_PATH = _risolvi("w908_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "2"
_VECCHIO_TAB = "tab90" + "2"
_VECCHIO_ST = "st90" + "2_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "e_us_mwh": 18.0,
    "e_arb_mwh_anno": 12600.0,
    "margine_eur_mwh": 47.6,
    "ricavo_lordo_eur_anno": 599760.0,
    "fee_annua_eur_anno": 18900.0,
    "margine_netto_eur_anno": 460860.0,
    "rendita": 8.383843940383326,
    "margine_target_eur_anno": 715662.1762839813,
    "van": -2136221.681634945,
    "tir": -1.232311081752802,
    "payback": None,
    "breakeven_spread_eur_mwh": 87.97999425360581,
    "breakeven_cicli_giorno": 2.8773273294218273,
}

_DEMO_SCENARI = [
    {"nome": "Base", "spread_eur_mwh": 65.0,
     "cicli_giorno": 2.0, "eta_rt": 0.88,
     "e_us_mwh": 18.0, "e_arb_mwh_anno": 12600.0,
     "margine_eur_mwh": 47.6,
     "ricavo_lordo_eur_anno": 599760.0,
     "fee_annua_eur_anno": 18900.0,
     "margine_netto_eur_anno": 460860.0,
     "van": -2136221.681634945,
     "tir": -1.232311081752802,
     "payback": None, "verdetto": "NON_CONVIENTE",
     "breakeven_spread_eur_mwh": 87.97999425360581,
     "breakeven_cicli_giorno": 2.8773273294218273},
    {"nome": "Spread piu 30 %", "spread_eur_mwh": 84.5,
     "cicli_giorno": 2.0, "eta_rt": 0.88,
     "e_us_mwh": 18.0, "e_arb_mwh_anno": 12600.0,
     "margine_eur_mwh": 64.76,
     "ricavo_lordo_eur_anno": 815976.0000000001,
     "fee_annua_eur_anno": 18900.0,
     "margine_netto_eur_anno": 677076.0000000001,
     "van": -323500.4802210247,
     "tir": 5.003235619186508,
     "payback": 9, "verdetto": "MARGINALE",
     "breakeven_spread_eur_mwh": 87.97999425360581,
     "breakeven_cicli_giorno": 2.0968193153074015},
    {"nome": "Spread meno 30 %", "spread_eur_mwh": 45.5,
     "cicli_giorno": 2.0, "eta_rt": 0.88,
     "e_us_mwh": 18.0, "e_arb_mwh_anno": 12600.0,
     "margine_eur_mwh": 30.439999999999998,
     "ricavo_lordo_eur_anno": 383544.0,
     "fee_annua_eur_anno": 18900.0,
     "margine_netto_eur_anno": 244644.0,
     "van": -3948942.883048864,
     "tir": -9.586141677946397,
     "payback": None, "verdetto": "NON_CONVIENTE",
     "breakeven_spread_eur_mwh": 87.97999425360581,
     "breakeven_cicli_giorno": 4.583441253847486},
    {"nome": "Cicli 3 al giorno", "spread_eur_mwh": 65.0,
     "cicli_giorno": 3.0, "eta_rt": 0.88,
     "e_us_mwh": 18.0, "e_arb_mwh_anno": 18900.0,
     "margine_eur_mwh": 47.6,
     "ricavo_lordo_eur_anno": 899640.0,
     "fee_annua_eur_anno": 28350.0,
     "margine_netto_eur_anno": 751290.0,
     "van": 298698.1139705818,
     "tir": 6.897483720280507,
     "payback": 8, "verdetto": "CONVIENTE",
     "breakeven_spread_eur_mwh": 62.85787495694933,
     "breakeven_cicli_giorno": 2.8773273294218273},
    {"nome": "Efficienza 0,80", "spread_eur_mwh": 65.0,
     "cicli_giorno": 2.0, "eta_rt": 0.80,
     "e_us_mwh": 18.0, "e_arb_mwh_anno": 12600.0,
     "margine_eur_mwh": 36.0,
     "ricavo_lordo_eur_anno": 453600.0,
     "fee_annua_eur_anno": 18900.0,
     "margine_netto_eur_anno": 314700.0,
     "van": -3361604.3119613705,
     "tir": -6.491830766871098,
     "payback": None, "verdetto": "NON_CONVIENTE",
     "breakeven_spread_eur_mwh": 104.7779936789664,
     "breakeven_cicli_giorno": 3.8447765184448186},
]

_DEMO_CONFRONTO = {
    "e_us_mwh": 18.0,
    "e_arb_mwh_anno": 12600.0,
    "margine_eur_mwh": 47.6,
    "ricavo_lordo_eur_anno": 599760.0,
    "fee_annua_eur_anno": 18900.0,
    "opex_eur_anno": 120000.0,
    "margine_netto_eur_anno": 460860.0,
    "capex_eur": 6000000.0,
    "rendita": 8.383843940383326,
    "margine_target_eur_anno": 715662.1762839813,
    "van": -2136221.681634945,
    "tir": -1.232311081752802,
    "payback": None,
    "breakeven_spread_eur_mwh": 87.97999425360581,
    "breakeven_cicli_giorno": 2.8773273294218273,
}

_ORDINE_VALIDA = (
    "e_mwh", "dod", "eta_rt", "cicli_giorno",
    "giorni_anno", "p_acq_eur_mwh", "spread_eur_mwh",
    "fee_eur_mwh", "opex_eur_anno", "capex_eur",
    "t_anni", "r_tasso", "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh903_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh903_num(3, "x"), 3.0)
        self.assertEqual(mh903_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh903_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh903_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh903_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh903_pos(0, "x")
        with self.assertRaises(ValueError):
            mh903_pos(-1, "x")
        self.assertEqual(mh903_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh903_fraz(0, "x"), 0.0)
        self.assertEqual(mh903_fraz(1, "x"), 1.0)
        self.assertEqual(mh903_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh903_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh903_fraz(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh903_int_pos(12, "x"), 12)
        self.assertEqual(mh903_int_pos(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh903_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh903_int_pos(5.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh903_tasso(0.06, "x"), 0.06)
        self.assertEqual(mh903_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh903_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh903_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh903_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh903_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_energia_usabile(self):
        self.assertEqual(mh903_energia_usabile(20.0, 0.90), 18.0)
        self.assertEqual(mh903_energia_usabile(20.0, 1.0), 20.0)
        self.assertEqual(mh903_energia_usabile(40.0, 0.90), 36.0)
        self.assertEqual(mh903_energia_usabile(20.0, 0.5), 10.0)
        with self.assertRaises(ValueError):
            mh903_energia_usabile(0.0, 0.90)
        with self.assertRaises(ValueError):
            mh903_energia_usabile(-1.0, 0.90)
        with self.assertRaises(ValueError):
            mh903_energia_usabile(20.0, 0.0)
        with self.assertRaises(ValueError):
            mh903_energia_usabile(20.0, 1.01)
        with self.assertRaises(ValueError):
            mh903_energia_usabile(20.0, -0.1)

    def test_energia_arbitrata(self):
        self.assertEqual(
            mh903_energia_arbitrata(18.0, 2.0, 350), 12600.0)
        self.assertEqual(
            mh903_energia_arbitrata(18.0, 3.0, 350), 18900.0)
        self.assertEqual(
            mh903_energia_arbitrata(18.0, 1.0, 350), 6300.0)
        self.assertEqual(
            mh903_energia_arbitrata(18.0, 2.0, 365), 13140.0)
        self.assertEqual(
            mh903_energia_arbitrata(18.0, 2.0, 366), 13176.0)
        self.assertEqual(
            mh903_energia_arbitrata(20.0, 2.0, 350), 14000.0)
        self.assertEqual(
            mh903_energia_arbitrata(0.0, 2.0, 350), 0.0)
        with self.assertRaises(ValueError):
            mh903_energia_arbitrata(18.0, 0.0, 350)
        with self.assertRaises(ValueError):
            mh903_energia_arbitrata(18.0, -1.0, 350)
        with self.assertRaises(ValueError):
            mh903_energia_arbitrata(18.0, 2.0, 0)
        with self.assertRaises(ValueError):
            mh903_energia_arbitrata(18.0, 2.0, 367)
        with self.assertRaises(ValueError):
            mh903_energia_arbitrata(18.0, 2.0, 350.5)

    def test_margine_mwh(self):
        self.assertAlmostEqual(
            mh903_margine_mwh(0.88, 65.0, 80.0), 47.60, places=2)
        self.assertAlmostEqual(
            mh903_margine_mwh(0.88, 84.5, 80.0), 64.76, places=2)
        self.assertAlmostEqual(
            mh903_margine_mwh(0.88, 45.5, 80.0), 30.44, places=2)
        self.assertAlmostEqual(
            mh903_margine_mwh(0.80, 65.0, 80.0), 36.00, places=2)
        self.assertAlmostEqual(
            mh903_margine_mwh(0.95, 65.0, 80.0), 57.75, places=2)
        self.assertAlmostEqual(
            mh903_margine_mwh(1.0, 65.0, 80.0), 65.00, places=2)
        # Con spread zero paghi le perdite sul prezzo
        # di acquisto: margine negativo.
        self.assertAlmostEqual(
            mh903_margine_mwh(0.88, 0.0, 80.0), -9.60, places=2)
        # Spread negativo ammesso: margine ancora piu
        # negativo, mai un errore di validazione.
        self.assertAlmostEqual(
            mh903_margine_mwh(0.88, -10.0, 80.0), -18.40,
            places=2)
        # Con prezzo di acquisto zero resta solo lo
        # spread per efficienza.
        self.assertAlmostEqual(
            mh903_margine_mwh(0.88, 65.0, 0.0), 57.20, places=2)
        with self.assertRaises(ValueError):
            mh903_margine_mwh(0.0, 65.0, 80.0)
        with self.assertRaises(ValueError):
            mh903_margine_mwh(1.01, 65.0, 80.0)
        with self.assertRaises(ValueError):
            mh903_margine_mwh(0.88, 65.0, -1.0)

    def test_ricavo_lordo_e_fee(self):
        self.assertEqual(
            mh903_ricavo_lordo(12600.0, 47.6), 599760.0)
        self.assertAlmostEqual(
            mh903_ricavo_lordo(12600.0, 64.76), 815976.0,
            places=2)
        self.assertEqual(
            mh903_ricavo_lordo(18900.0, 47.6), 899640.0)
        self.assertEqual(
            mh903_ricavo_lordo(12600.0, 0.0), 0.0)
        self.assertEqual(
            mh903_ricavo_lordo(12600.0, -9.6), -120960.0)
        self.assertEqual(
            mh903_fee_annua(12600.0, 1.5), 18900.0)
        self.assertEqual(
            mh903_fee_annua(18900.0, 1.5), 28350.0)
        self.assertEqual(
            mh903_fee_annua(12600.0, 0.0), 0.0)
        self.assertEqual(
            mh903_fee_annua(0.0, 1.5), 0.0)
        with self.assertRaises(ValueError):
            mh903_ricavo_lordo(-1.0, 47.6)
        with self.assertRaises(ValueError):
            mh903_fee_annua(12600.0, -1.0)
        with self.assertRaises(ValueError):
            mh903_fee_annua(-1.0, 1.5)

    def test_margine_netto(self):
        self.assertEqual(
            mh903_margine_netto(599760.0, 18900.0, 120000.0),
            460860.0)
        self.assertEqual(
            mh903_margine_netto(815976.0, 18900.0, 120000.0),
            677076.0)
        self.assertEqual(
            mh903_margine_netto(599760.0, 0.0, 120000.0),
            479760.0)
        self.assertEqual(
            mh903_margine_netto(599760.0, 18900.0, 0.0),
            580860.0)
        self.assertEqual(
            mh903_margine_netto(-120960.0, 18900.0, 120000.0),
            -259860.0)
        with self.assertRaises(ValueError):
            mh903_margine_netto(599760.0, 18900.0, -1.0)

    def test_annuity(self):
        self.assertAlmostEqual(
            mh903_annuity(0.06, 12), 8.383843940383326, places=9)
        self.assertAlmostEqual(
            mh903_annuity(0.06, 1), 0.9433962264150943, places=9)
        self.assertAlmostEqual(
            mh903_annuity(0.10, 12), 6.813691822896435, places=9)
        self.assertAlmostEqual(
            mh903_annuity(0.05, 15), 10.3796580381806, places=9)
        with self.assertRaises(ValueError):
            mh903_annuity(0.0, 12)
        with self.assertRaises(ValueError):
            mh903_annuity(1.0, 12)
        with self.assertRaises(ValueError):
            mh903_annuity(0.06, 0)

    def test_riga_anno_e_serie(self):
        riga = mh903_riga_anno(1, 12600.0, 599760.0, 18900.0,
                               460860.0)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["energia_arbitrata"], 12600.0)
        self.assertEqual(riga["ricavo_lordo"], 599760.0)
        self.assertEqual(riga["fee_annua"], 18900.0)
        self.assertEqual(riga["margine_netto"], 460860.0)
        self.assertEqual(riga["flusso"], 460860.0)
        riga = mh903_riga_anno(12, 12600.0, 599760.0, 18900.0,
                               460860.0)
        self.assertEqual(riga["flusso"], 460860.0)
        with self.assertRaises(ValueError):
            mh903_riga_anno(0, 12600.0, 599760.0, 18900.0,
                            460860.0)
        serie = mh903_serie_annua(12600.0, 599760.0, 18900.0,
                                  460860.0, 12)
        self.assertEqual(len(serie), 12)
        self.assertTrue(all(r["flusso"] == 460860.0
                            for r in serie))
        self.assertTrue(all(r["margine_netto"] == 460860.0
                            for r in serie))
        self.assertTrue(all(r["energia_arbitrata"] == 12600.0
                            for r in serie))
        serie = mh903_serie_annua(18900.0, 899640.0, 28350.0,
                                  751290.0, 12)
        self.assertEqual(serie[0]["flusso"], 751290.0)
        with self.assertRaises(ValueError):
            mh903_serie_annua(12600.0, 599760.0, 18900.0,
                              460860.0, 0)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        fl = bc["flussi"]
        self.assertEqual(len(fl), 13)
        self.assertEqual(fl[0], -6000000.0)
        self.assertEqual(fl[1], 460860.0)
        self.assertEqual(fl[12], 460860.0)
        self.assertAlmostEqual(sum(fl), -469680.00, places=2)
        self.assertAlmostEqual(sum(fl[:12]), -930540.00, places=2)
        fl2 = mh903_flussi(bc["serie"], bc["capex_eur"], 12)
        self.assertEqual(fl2, fl)
        self.assertAlmostEqual(mh903_van(fl, 0.06), bc["van"])
        with self.assertRaises(ValueError):
            mh903_flussi(bc["serie"][:11], bc["capex_eur"], 12)

    def test_breakeven_spread(self):
        self.assertAlmostEqual(
            mh903_breakeven_spread(6000000.0, 0.06, 12,
                                   120000.0, 12600.0, 0.88,
                                   80.0, 1.5),
            87.98, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_spread(0.0, 0.06, 12,
                                   120000.0, 12600.0, 0.88,
                                   80.0, 1.5),
            23.44, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_spread(6000000.0, 0.06, 12,
                                   0.0, 12600.0, 0.88,
                                   80.0, 1.5),
            77.16, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_spread(6000000.0, 0.06, 12,
                                   120000.0, 18900.0, 0.88,
                                   80.0, 1.5),
            62.86, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_spread(6000000.0, 0.06, 12,
                                   120000.0, 12600.0, 0.80,
                                   80.0, 1.5),
            104.78, places=2)
        self.assertIsNone(
            mh903_breakeven_spread(6000000.0, 0.06, 12,
                                   120000.0, 0.0, 0.88,
                                   80.0, 1.5))
        # Allo spread di breakeven la VAN e zero, la
        # TIR e uguale al tasso e il verdetto e
        # MARGINALE.
        be = mh903_breakeven_spread(6000000.0, 0.06, 12,
                                    120000.0, 12600.0, 0.88,
                                    80.0, 1.5)
        bc = mh903_calcola(
            **_demo_kwargs(spread_eur_mwh=be))
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               715662.18, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(
            bc["breakeven_cicli_giorno"], 2.00, places=2)
        with self.assertRaises(ValueError):
            mh903_breakeven_spread(6000000.0, 0.06, 12,
                                   120000.0, 12600.0, 0.0,
                                   80.0, 1.5)
        with self.assertRaises(ValueError):
            mh903_breakeven_spread(-1.0, 0.06, 12,
                                   120000.0, 12600.0, 0.88,
                                   80.0, 1.5)

    def test_breakeven_cicli(self):
        self.assertAlmostEqual(
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 18.0, 350,
                                  47.6, 1.5),
            2.88, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 18.0, 350,
                                  64.76, 1.5),
            2.10, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 18.0, 350,
                                  36.0, 1.5),
            3.84, places=2)
        self.assertAlmostEqual(
            mh903_breakeven_cicli(0.0, 0.06, 12,
                                  120000.0, 18.0, 350,
                                  47.6, 1.5),
            0.41, places=2)
        # Se (margine meno fee) e nullo o negativo
        # non esiste un numero di cicli che azzera
        # la VAN: piu cicli peggiorano solo il conto.
        self.assertIsNone(
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 18.0, 350,
                                  1.5, 1.5))
        self.assertIsNone(
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 18.0, 350,
                                  -9.6, 1.5))
        self.assertIsNone(
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 0.0, 350,
                                  47.6, 1.5))
        # Ai cicli di breakeven la VAN e zero, la
        # TIR e uguale al tasso e il verdetto e
        # MARGINALE.
        bec = mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                    120000.0, 18.0, 350,
                                    47.6, 1.5)
        bc = mh903_calcola(
            **_demo_kwargs(cicli_giorno=bec))
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               715662.18, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(
            bc["breakeven_spread_eur_mwh"], 65.00, places=2)
        with self.assertRaises(ValueError):
            mh903_breakeven_cicli(6000000.0, 0.06, 12,
                                  120000.0, 18.0, 367,
                                  47.6, 1.5)

    def test_scenario_singolo(self):
        s = mh903_scenario("Spread piu 30 %", mh903_demo(),
                           {"spread_eur_mwh": 84.5})
        self.assertEqual(s["nome"], "Spread piu 30 %")
        self.assertEqual(s["spread_eur_mwh"], 84.5)
        self.assertAlmostEqual(s["van"], -323500.48, places=2)
        self.assertAlmostEqual(s["tir"], 5.00, places=2)
        self.assertEqual(s["payback"], 9)
        self.assertEqual(s["verdetto"], "MARGINALE")
        # Il breakeven spread e INVARIANTE allo
        # spread corrente: dipende da efficienza,
        # prezzo di acquisto, fee, O&M, CAPEX e
        # rendita, non dallo spread inserito.
        self.assertAlmostEqual(
            s["breakeven_spread_eur_mwh"], 87.98, places=2)
        s = mh903_scenario("Spread meno 30 %", mh903_demo(),
                           {"spread_eur_mwh": 45.5})
        self.assertAlmostEqual(s["van"], -3948942.88, places=2)
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(
            s["breakeven_spread_eur_mwh"], 87.98, places=2)
        s = mh903_scenario("Cicli 3 al giorno", mh903_demo(),
                           {"cicli_giorno": 3.0})
        self.assertAlmostEqual(s["van"], 298698.11, places=2)
        self.assertEqual(s["payback"], 8)
        self.assertEqual(s["e_arb_mwh_anno"], 18900.0)
        # Il breakeven cicli e INVARIANTE ai cicli
        # correnti.
        self.assertAlmostEqual(
            s["breakeven_cicli_giorno"], 2.88, places=2)
        s = mh903_scenario("Efficienza 0,80", mh903_demo(),
                           {"eta_rt": 0.80})
        self.assertAlmostEqual(s["van"], -3361604.31, places=2)
        self.assertAlmostEqual(
            s["breakeven_spread_eur_mwh"], 104.78, places=2)
        with self.assertRaises(ValueError):
            mh903_scenario("", mh903_demo(),
                           {"spread_eur_mwh": 84.5})
        with self.assertRaises(ValueError):
            mh903_scenario("X", mh903_demo(),
                           {"giorni_anno": 367})

    def test_scenario_margine_negativo_non_calcolabile(self):
        s = mh903_scenario("Spread zero", mh903_demo(),
                           {"spread_eur_mwh": 0.0})
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertIsNone(s["breakeven_spread_eur_mwh"])
        self.assertIsNone(s["breakeven_cicli_giorno"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(s["margine_eur_mwh"], -9.6)
        self.assertEqual(s["margine_netto_eur_anno"], -259860.0)

    def test_confronto_formule(self):
        c = mh903_confronto(18.0, 12600.0, 47.6, 599760.0,
                            18900.0, 120000.0, 460860.0,
                            6000000.0, 8.383843940383326,
                            715662.18, -2136221.68, -1.23,
                            None, 87.98, 2.88)
        self.assertEqual(c["e_us_mwh"], 18.0)
        self.assertEqual(c["e_arb_mwh_anno"], 12600.0)
        self.assertEqual(c["margine_eur_mwh"], 47.6)
        self.assertEqual(c["ricavo_lordo_eur_anno"], 599760.0)
        self.assertEqual(c["fee_annua_eur_anno"], 18900.0)
        self.assertEqual(c["opex_eur_anno"], 120000.0)
        self.assertEqual(c["margine_netto_eur_anno"], 460860.0)
        self.assertEqual(c["capex_eur"], 6000000.0)
        self.assertAlmostEqual(c["rendita"], 8.3838, places=4)
        self.assertEqual(c["margine_target_eur_anno"],
                         715662.18)
        self.assertEqual(c["van"], -2136221.68)
        self.assertEqual(c["tir"], -1.23)
        self.assertIsNone(c["payback"])
        self.assertEqual(c["breakeven_spread_eur_mwh"], 87.98)
        self.assertEqual(c["breakeven_cicli_giorno"], 2.88)
        c = mh903_confronto(18.0, 12600.0, -9.6, -120960.0,
                            18900.0, 120000.0, -259860.0,
                            6000000.0, 8.383843940383326,
                            715662.18, None, None, None,
                            None, None)
        self.assertIsNone(c["van"])
        self.assertIsNone(c["tir"])
        self.assertIsNone(c["payback"])
        self.assertIsNone(c["breakeven_spread_eur_mwh"])
        self.assertIsNone(c["breakeven_cicli_giorno"])
        with self.assertRaises(ValueError):
            mh903_confronto(18.0, 12600.0, 47.6, 599760.0,
                            18900.0, -1.0, 460860.0,
                            6000000.0, 8.383843940383326,
                            715662.18, -2136221.68, -1.23,
                            None, 87.98, 2.88)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_sei(self):
        bc = mh903_demo_calcoli()
        self.assertAlmostEqual(
            mh903_van(bc["flussi"], 0.06),
            bc["van"])
        bc_piu = mh903_calcola(
            _scenari=False,
            **dict(mh903_demo(), spread_eur_mwh=84.5))
        self.assertAlmostEqual(
            mh903_van(bc_piu["flussi"], 0.06),
            bc["scenari"][1]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh903_van([-6000000, 460860, 460860], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,06 = 6 per cento):
        # usato diretto, NON diviso per 100. Con 0,06 la
        # VAN demo e' -2136221,68; con 0,50 (cioe' 50
        # per cento) sarebbe tutt'altra; con 6,0 il
        # tasso e' degenere (maggiore o uguale a 1) e
        # solleva ValueError.
        bc = mh903_demo_calcoli()
        self.assertAlmostEqual(
            mh903_van(bc["flussi"], 0.06),
            -2136221.68, places=2)
        self.assertNotAlmostEqual(
            mh903_van(bc["flussi"], 0.50),
            -2136221.68, places=2)
        with self.assertRaises(ValueError):
            mh903_van(bc["flussi"], 6.0)

    def test_tir_demo(self):
        bc = mh903_demo_calcoli()
        tir_v = mh903_tir(bc["flussi"])
        self.assertIsNotNone(tir_v)
        self.assertAlmostEqual(tir_v * 100.0, bc["tir"],
                               places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh903_tir([-100, -10, -10]))
        self.assertIsNone(mh903_tir([100, 10, 10]))
        self.assertIsNone(mh903_tir([0, 10, 10]))
        self.assertIsNone(mh903_tir([-6000000, -460860,
                                     -460860]))
        # Durata 1: la TIR vera (-92,32 %) sta fuori
        # dall'intervallo di bisezione [-0,9, 5,0]:
        # nessun cambio di segno dentro l'intervallo.
        bc = mh903_calcola(**_demo_kwargs(t_anni=1))
        self.assertIsNone(bc["tir"])
        self.assertAlmostEqual(bc["van"], -5565226.42, places=2)

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh903_demo_calcoli()
        self.assertIsNone(mh903_payback(bc["flussi"]))
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh903_payback([-100, 100, 10]), 1)
        self.assertEqual(mh903_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh903_payback([-100, 10, 10]))
        # Con CAPEX zero il payback e l'anno 1.
        self.assertEqual(mh903_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh903_demo_calcoli()
        fl = bc["flussi"]
        self.assertAlmostEqual(sum(fl[:12]), -930540.00, places=2)
        self.assertAlmostEqual(sum(fl), -469680.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(
            mh903_verdetto(100.0, 0.10, 6000000.0), "CONVIENTE")
        self.assertEqual(
            mh903_verdetto(0.0, 0.10, 6000000.0), "MARGINALE")
        self.assertEqual(
            mh903_verdetto(-600000.0, 0.10, 6000000.0),
            "MARGINALE")
        self.assertEqual(
            mh903_verdetto(-600001.0, 0.10, 6000000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh903_verdetto(-1000000.0, 0.10, 6000000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativa e
        # NON_CONVIENTE (VAN zero compresa nel MARGINALE
        # solo perche il valore assoluto zero e minore
        # o uguale a zero).
        self.assertEqual(
            mh903_verdetto(-1.0, 0.0, 6000000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh903_verdetto(0.0, 0.0, 6000000.0), "MARGINALE")
        with self.assertRaises(ValueError):
            mh903_verdetto(100.0, 1.5, 6000000.0)
        with self.assertRaises(ValueError):
            mh903_verdetto(100.0, 0.10, -1.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh903_verdetto(None, 0.10, 6000000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh903_verdetto(None, 0.0, 0.0), "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh903_demo()
        val = mh903_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_spread_negativo_ammesso(self):
        # Lo spread negativo NON e un errore di
        # validazione: e ammesso e da margine netto
        # negativo, quindi NON_CALCOLABILE.
        demo = mh903_demo()
        val = mh903_valida(*[dict(demo, spread_eur_mwh=-10.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh903_calcola(**_demo_kwargs(spread_eur_mwh=-10.0))
        self.assertEqual(bc["margine_eur_mwh"], -18.4)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_durata_zero_e_non_intera_no(self):
        kw = _demo_kwargs(t_anni=0)
        self.assertRaises(ValueError, mh903_calcola, **kw)
        kw = _demo_kwargs(t_anni=12.5)
        self.assertRaises(ValueError, mh903_calcola, **kw)
        kw = _demo_kwargs(t_anni=5)
        bc = mh903_calcola(**kw)
        self.assertEqual(bc["t_anni"], 5)

    def test_valida_giorni_intervallo_e_intero(self):
        with self.assertRaises(ValueError):
            mh903_calcola(**_demo_kwargs(giorni_anno=0))
        with self.assertRaises(ValueError):
            mh903_calcola(**_demo_kwargs(giorni_anno=367))
        with self.assertRaises(ValueError):
            mh903_calcola(**_demo_kwargs(giorni_anno=350.5))
        bc = mh903_calcola(**_demo_kwargs(giorni_anno=366))
        self.assertEqual(bc["giorni_anno"], 366)
        self.assertEqual(bc["e_arb_mwh_anno"], 13176.0)
        bc = mh903_calcola(**_demo_kwargs(giorni_anno=1))
        self.assertEqual(bc["giorni_anno"], 1)

    def test_valida_dod_eta_intervalli(self):
        for campo, valore in (("dod", 0.0), ("dod", 1.01),
                              ("dod", -0.1), ("eta_rt", 0.0),
                              ("eta_rt", 1.01),
                              ("eta_rt", -0.1)):
            with self.assertRaises(ValueError):
                mh903_calcola(**_demo_kwargs(**{campo: valore}))
        bc = mh903_calcola(**_demo_kwargs(dod=1.0))
        self.assertEqual(bc["dod"], 1.0)
        bc = mh903_calcola(**_demo_kwargs(eta_rt=1.0))
        self.assertEqual(bc["eta_rt"], 1.0)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh903_calcola(**_demo_kwargs(r_tasso=tasso))
        bc = mh903_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertEqual(bc["r_tasso"], 0.10)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh903_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh903_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        bc = mh903_calcola(**_demo_kwargs(tol_frazione=1.0))
        self.assertEqual(bc["tol_frazione"], 1.0)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("e_mwh", 0),
                              ("dod", 0),
                              ("eta_rt", 0),
                              ("cicli_giorno", 0),
                              ("giorni_anno", 0),
                              ("t_anni", 0),
                              ("r_tasso", 0)):
            with self.assertRaises(ValueError):
                mh903_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(spread_eur_mwh=float("nan"))
        self.assertRaises(ValueError, mh903_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh903_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_mwh", -1),
                              ("dod", -1),
                              ("eta_rt", -1),
                              ("cicli_giorno", -1),
                              ("giorni_anno", -1),
                              ("p_acq_eur_mwh", -1),
                              ("fee_eur_mwh", -1),
                              ("opex_eur_anno", -1),
                              ("capex_eur", -1),
                              ("t_anni", -1),
                              ("r_tasso", -0.01),
                              ("tol_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh903_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh903_calcola(mh903_demo())
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh903_calcola(dict(mh903_demo(), spread_eur_mwh=999.0),
                           spread_eur_mwh=65.0)
        self.assertEqual(bc["spread_eur_mwh"], 65.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh903_calcola(_scenari=False, **mh903_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -2136221.68, places=2)
        self.assertAlmostEqual(bc["tir"], -1.23, places=2)


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
                if valore is None or isinstance(valore, (int, str)):
                    self.assertEqual(ottenuto, valore)
                else:
                    self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_verdetto_principale(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertLess(bc["van"], 0.0)
        self.assertIsNone(bc["payback"])
        self.assertAlmostEqual(bc["tir"], -1.23, places=2)
        self.assertAlmostEqual(bc["breakeven_spread_eur_mwh"],
                               87.98, places=2)
        self.assertAlmostEqual(bc["breakeven_cicli_giorno"],
                               2.88, places=2)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "NON_CONVIENTE")
        self.assertAlmostEqual(
            bc["margine_target_eur_anno"], 715662.18, places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["e_us_mwh"],
            bc["e_mwh"] * bc["dod"])
        self.assertAlmostEqual(
            bc["e_arb_mwh_anno"],
            bc["e_us_mwh"] * bc["cicli_giorno"]
            * bc["giorni_anno"])
        self.assertAlmostEqual(
            bc["margine_eur_mwh"],
            bc["eta_rt"] * bc["spread_eur_mwh"]
            - (1.0 - bc["eta_rt"]) * bc["p_acq_eur_mwh"])
        self.assertAlmostEqual(
            bc["ricavo_lordo_eur_anno"],
            bc["e_arb_mwh_anno"] * bc["margine_eur_mwh"])
        self.assertAlmostEqual(
            bc["fee_annua_eur_anno"],
            bc["e_arb_mwh_anno"] * bc["fee_eur_mwh"])
        self.assertAlmostEqual(
            bc["margine_netto_eur_anno"],
            bc["ricavo_lordo_eur_anno"]
            - bc["fee_annua_eur_anno"]
            - bc["opex_eur_anno"])
        self.assertAlmostEqual(
            bc["margine_target_eur_anno"],
            bc["capex_eur"]
            / mh903_annuity(bc["r_tasso"], bc["t_anni"]))
        self.assertAlmostEqual(
            bc["breakeven_spread_eur_mwh"],
            ((1.0 - bc["eta_rt"]) * bc["p_acq_eur_mwh"]
             + bc["fee_eur_mwh"]
             + (bc["opex_eur_anno"]
                + bc["margine_target_eur_anno"])
             / bc["e_arb_mwh_anno"]) / bc["eta_rt"])
        self.assertAlmostEqual(
            bc["breakeven_cicli_giorno"],
            ((bc["opex_eur_anno"]
              + bc["margine_target_eur_anno"])
             / (bc["margine_eur_mwh"] - bc["fee_eur_mwh"]))
            / (bc["e_us_mwh"] * bc["giorni_anno"]))
        self.assertAlmostEqual(
            bc["van"],
            mh903_van(bc["flussi"], bc["r_tasso"]))
        self.assertAlmostEqual(
            bc["van"],
            -bc["capex_eur"]
            + bc["margine_netto_eur_anno"] * bc["rendita"])
        for t in range(1, bc["t_anni"] + 1):
            riga = bc["serie"][t - 1]
            with self.subTest(anno=t):
                self.assertAlmostEqual(
                    riga["flusso"],
                    riga["margine_netto"])
        conf = bc["confronto"]
        self.assertEqual(conf["van"], bc["van"])
        self.assertEqual(conf["tir"], bc["tir"])
        self.assertEqual(conf["payback"], bc["payback"])
        self.assertEqual(conf["capex_eur"], bc["capex_eur"])
        self.assertEqual(conf["breakeven_spread_eur_mwh"],
                         bc["breakeven_spread_eur_mwh"])
        self.assertEqual(conf["breakeven_cicli_giorno"],
                         bc["breakeven_cicli_giorno"])

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu spread migliora il caso; meno spread lo
        # peggiora. Il breakeven spread e INVARIANTE
        # allo spread corrente.
        self.assertGreater(bc["scenari"][1]["van"],
                           base["van"])
        self.assertEqual(bc["scenari"][1]["payback"], 9)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["scenari"][1]["breakeven_spread_eur_mwh"],
                         base["breakeven_spread_eur_mwh"])
        self.assertLess(bc["scenari"][2]["van"],
                        base["van"])
        self.assertIsNone(bc["scenari"][2]["payback"])
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][2]["breakeven_spread_eur_mwh"],
                         base["breakeven_spread_eur_mwh"])
        # Piu cicli migliora il caso e lo rende
        # CONVIENTE; il breakeven cicli e INVARIANTE
        # ai cicli correnti.
        self.assertGreater(bc["scenari"][3]["van"], 0.0)
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][3]["payback"], 8)
        self.assertEqual(bc["scenari"][3]["breakeven_cicli_giorno"],
                         base["breakeven_cicli_giorno"])
        self.assertLess(bc["scenari"][3]["breakeven_spread_eur_mwh"],
                        base["breakeven_spread_eur_mwh"])
        # Meno efficienza peggiora il caso e alza
        # entrambi i breakeven.
        self.assertLess(bc["scenari"][4]["van"],
                        base["van"])
        self.assertIsNone(bc["scenari"][4]["payback"])
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "NON_CONVIENTE")
        self.assertGreater(
            bc["scenari"][4]["breakeven_spread_eur_mwh"],
            base["breakeven_spread_eur_mwh"])
        self.assertGreater(
            bc["scenari"][4]["breakeven_cicli_giorno"],
            base["breakeven_cicli_giorno"])

    def test_sensibilita_valori(self):
        s = mh903_sensibilita(**mh903_demo())
        self.assertEqual(set(s.keys()),
                         {"spread_piu30", "spread_meno30",
                          "cicli_003", "eta_080",
                          "capex_zero", "opex_zero",
                          "vita_005", "tasso_010", "spread_000",
                          "p_acq_120", "eta_095", "cicli_001"})
        attesi = {
            "spread_piu30": (-323500.48, 5.00, 9, "MARGINALE"),
            "spread_meno30": (-3948942.88, -9.59, None,
                              "NON_CONVIENTE"),
            "cicli_003": (298698.11, 6.90, 8, "CONVIENTE"),
            "eta_080": (-3361604.31, -6.49, None,
                        "NON_CONVIENTE"),
            "capex_zero": (3863778.32, None, 1, "CONVIENTE"),
            "opex_zero": (-1130160.41, 2.39, 11,
                          "NON_CONVIENTE"),
            "vita_005": (-4058690.03, -25.27, None,
                         "NON_CONVIENTE"),
            "tasso_010": (-2859841.99, -1.23, None,
                          "NON_CONVIENTE"),
            "spread_000": (None, None, None,
                           "NON_CALCOLABILE"),
            "p_acq_120": (-2643276.56, -3.26, None,
                          "NON_CONVIENTE"),
            "eta_095": (-1064011.88, 2.61, 11,
                        "NON_CONVIENTE"),
            "cicli_001": (-4571141.48, -13.62, None,
                          "NON_CONVIENTE"),
        }
        for nome, (vc, tc, pbc, vdc) in attesi.items():
            with self.subTest(variante=nome):
                if vc is None:
                    self.assertIsNone(s[nome]["van"])
                else:
                    self.assertAlmostEqual(s[nome]["van"],
                                           vc, places=2)
                if tc is None:
                    self.assertIsNone(s[nome]["tir"])
                else:
                    self.assertAlmostEqual(s[nome]["tir"],
                                           tc, places=2)
                self.assertEqual(s[nome]["payback"], pbc)
                self.assertEqual(s[nome]["verdetto"], vdc)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)
            self.assertIn("tir", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh903_csv(bc, mh903_demo())
        for voce in ("e_mwh", "dod",
                     "eta_rt", "cicli_giorno",
                     "giorni_anno", "p_acq_eur_mwh",
                     "spread_eur_mwh", "fee_eur_mwh",
                     "opex_eur_anno", "capex_eur",
                     "t_anni", "r_tasso",
                     "tol_frazione",
                     "e_us_mwh", "e_arb_mwh_anno",
                     "margine_eur_mwh",
                     "ricavo_lordo_eur_anno",
                     "fee_annua_eur_anno",
                     "margine_netto_eur_anno",
                     "rendita", "margine_target_eur_anno",
                     "breakeven_spread_eur_mwh",
                     "breakeven_cicli_giorno",
                     "van", "tir", "payback",
                     "scenario_base_van",
                     "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_spread_piu30_van",
                     "scenario_spread_piu30_verdetto",
                     "scenario_spread_meno30_van",
                     "scenario_spread_meno30_verdetto",
                     "scenario_cicli_003_van",
                     "scenario_cicli_003_verdetto",
                     "scenario_eta_080_van",
                     "scenario_eta_080_verdetto",
                     "anno_1_energia_arbitrata",
                     "anno_1_ricavo_lordo",
                     "anno_1_fee_annua",
                     "anno_1_margine_netto",
                     "anno_1_flusso",
                     "anno_12_margine_netto",
                     "anno_12_flusso",
                     "confronto_e_us_mwh",
                     "confronto_e_arb_mwh_anno",
                     "confronto_margine_eur_mwh",
                     "confronto_ricavo_lordo_eur_anno",
                     "confronto_fee_annua_eur_anno",
                     "confronto_opex_eur_anno",
                     "confronto_margine_netto_eur_anno",
                     "confronto_capex_eur",
                     "confronto_rendita",
                     "confronto_margine_target_eur_anno",
                     "confronto_van", "confronto_tir",
                     "confronto_payback",
                     "confronto_breakeven_spread_eur_mwh",
                     "confronto_breakeven_cicli_giorno",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("NON_CONVIENTE", csv)
        self.assertIn("MARGINALE", csv)
        self.assertIn("CONVIENTE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh903_csv(bc, mh903_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_mwh;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh903_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh903_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 12)
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 27)
        self.assertEqual(len(bc["df_ricavi_costi"]), 3)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso (EUR)"].iloc[0],
            460860.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[10],
            -930540.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[-1],
            -469680.00, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Energia usabile (MWh)",
             "Energia arbitrata (MWh/anno)",
             "Margine per MWh comprato (EUR/MWh)",
             "Ricavo lordo (EUR/anno)",
             "Fee trading (EUR/anno)",
             "O&M (EUR/anno)",
             "Margine netto (EUR/anno)",
             "CAPEX (EUR)",
             "Rendita",
             "Margine target (EUR/anno)",
             "VAN (EUR)",
             "TIR (%)",
             "Payback (anni)",
             "Breakeven spread (EUR/MWh)",
             "Breakeven cicli (cicli/giorno)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            18.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[3],
            599760.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Energia batteria (MWh)", voci)
        self.assertIn("Profondita di scarica DoD (frazione)",
                      voci)
        self.assertIn("Breakeven spread (EUR/MWh)", voci)
        self.assertIn("Breakeven cicli (cicli/giorno)", voci)
        self.assertIn("Margine target (EUR/anno)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("TIR (%)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto",
                      set(bc["df_scenari"].columns))
        self.assertIn("Breakeven cicli (cicli/giorno)",
                      set(bc["df_scenari"].columns))
        self.assertEqual(
            list(bc["df_ricavi_costi"]["Voce"]),
            ["Ricavo lordo", "Fee trading", "O&M"])
        self.assertAlmostEqual(
            bc["df_ricavi_costi"]["Importo (EUR/anno)"].iloc[0],
            599760.00, places=2)
        self.assertAlmostEqual(
            bc["df_ricavi_costi"]["Importo (EUR/anno)"].iloc[1],
            18900.00, places=2)
        self.assertAlmostEqual(
            bc["df_ricavi_costi"]["Importo (EUR/anno)"].iloc[2],
            120000.00, places=2)

    def test_zero_ammessi(self):
        bc = mh903_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 3863778.32, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(opex_eur_anno=0.0))
        self.assertEqual(bc["opex_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], -1130160.41, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        self.assertAlmostEqual(bc["van"], -2136221.68, places=2)
        bc = mh903_calcola(**_demo_kwargs(p_acq_eur_mwh=0.0))
        self.assertEqual(bc["p_acq_eur_mwh"], 0.0)
        self.assertAlmostEqual(bc["margine_eur_mwh"], 57.20,
                               places=2)
        self.assertAlmostEqual(bc["van"], -1122111.92, places=2)
        self.assertAlmostEqual(bc["tir"], 2.41, places=2)
        self.assertEqual(bc["payback"], 11)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(fee_eur_mwh=0.0))
        self.assertEqual(bc["fee_eur_mwh"], 0.0)
        self.assertAlmostEqual(bc["van"], -1977767.03, places=2)
        self.assertAlmostEqual(bc["tir"], -0.63, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_spread_zero_margine_negativo_non_calcolabile(self):
        kw = _demo_kwargs(spread_eur_mwh=0.0)
        bc = mh903_calcola(**kw)
        self.assertEqual(bc["margine_eur_mwh"], -9.6)
        self.assertEqual(bc["ricavo_lordo_eur_anno"], -120960.0)
        self.assertEqual(bc["margine_netto_eur_anno"],
                         -259860.0)
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_spread_eur_mwh"])
        self.assertIsNone(bc["breakeven_cicli_giorno"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        # Fisica e prezzi restano calcolati anche nel
        # regime degenere (sono fisica e prezzi, non KPI
        # di ritorno).
        self.assertEqual(bc["e_us_mwh"], 18.0)
        self.assertEqual(bc["e_arb_mwh_anno"], 12600.0)

    def test_spread_negativo_non_calcolabile(self):
        kw = _demo_kwargs(spread_eur_mwh=-10.0)
        bc = mh903_calcola(**kw)
        self.assertEqual(bc["margine_eur_mwh"], -18.4)
        self.assertEqual(bc["margine_netto_eur_anno"],
                         -370740.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_spread_breakeven_marginale(self):
        # Allo spread di breakeven la VAN e zero,
        # la TIR e uguale al tasso e il verdetto e
        # MARGINALE (VAN zero compresa nel MARGINALE).
        be = demo_calcoli()["breakeven_spread_eur_mwh"]
        kw = _demo_kwargs(spread_eur_mwh=be)
        bc = mh903_calcola(**kw)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               715662.18, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["breakeven_cicli_giorno"],
                               2.00, places=2)

    def test_cicli_breakeven_marginale(self):
        bec = demo_calcoli()["breakeven_cicli_giorno"]
        kw = _demo_kwargs(cicli_giorno=bec)
        bc = mh903_calcola(**kw)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               715662.18, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["breakeven_spread_eur_mwh"],
                               65.00, places=2)

    def test_durata_uno_tir_non_definita(self):
        bc = mh903_calcola(**_demo_kwargs(t_anni=1))
        self.assertAlmostEqual(bc["van"], -5565226.42, places=2)
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_durata_cinque_e_tasso_dieci_e_venti(self):
        bc = mh903_calcola(**_demo_kwargs(t_anni=5))
        self.assertAlmostEqual(bc["van"], -4058690.03, places=2)
        self.assertAlmostEqual(bc["tir"], -25.27, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertAlmostEqual(bc["van"], -2859841.99, places=2)
        self.assertAlmostEqual(bc["tir"], -1.23, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(t_anni=20))
        self.assertAlmostEqual(bc["van"], -713972.11, places=2)
        self.assertAlmostEqual(bc["tir"], 4.49, places=2)
        self.assertEqual(bc["payback"], 14)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_tolleranza_zero_spread_piu30_non_conveniente(self):
        # Stessa VAN -323.500,48 del MARGINALE demo con
        # spread +30 %, ma con tolleranza zero il
        # confine si sposta: ogni VAN negativa diventa
        # NON_CONVIENTE.
        bc = mh903_calcola(**_demo_kwargs(spread_eur_mwh=84.5,
                                          tol_frazione=0.0))
        self.assertAlmostEqual(bc["van"], -323500.48, places=2)
        self.assertAlmostEqual(bc["tir"], 5.00, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_energia_doppia_conveniente(self):
        bc = mh903_calcola(**_demo_kwargs(e_mwh=40.0))
        self.assertEqual(bc["e_us_mwh"], 36.0)
        self.assertEqual(bc["e_arb_mwh_anno"], 25200.0)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               1041720.00, places=2)
        self.assertAlmostEqual(bc["van"], 2733617.91, places=2)
        self.assertAlmostEqual(bc["tir"], 13.61, places=2)
        self.assertEqual(bc["payback"], 6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_cicli_uno_e_quattro(self):
        bc = mh903_calcola(**_demo_kwargs(cicli_giorno=1.0))
        self.assertAlmostEqual(bc["van"], -4571141.48, places=2)
        self.assertAlmostEqual(bc["tir"], -13.62, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(cicli_giorno=4.0))
        self.assertAlmostEqual(bc["van"], 2733617.91, places=2)
        self.assertAlmostEqual(bc["tir"], 13.61, places=2)
        self.assertEqual(bc["payback"], 6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_giorni_365_e_dod_uno(self):
        bc = mh903_calcola(**_demo_kwargs(giorni_anno=365))
        self.assertAlmostEqual(bc["van"], -1927514.27, places=2)
        self.assertAlmostEqual(bc["tir"], -0.44, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh903_calcola(**_demo_kwargs(dod=1.0))
        self.assertAlmostEqual(bc["van"], -1595128.39, places=2)
        self.assertAlmostEqual(bc["tir"], 0.77, places=2)
        self.assertEqual(bc["payback"], 12)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_uno(self):
        bc = mh903_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(bc["breakeven_spread_eur_mwh"],
                               23.44, places=2)
        self.assertAlmostEqual(bc["breakeven_cicli_giorno"],
                               0.41, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(e_mwh="20.0")
        self.assertRaises(ValueError, mh903_calcola, **kw)
        kw = _demo_kwargs(e_mwh=True)
        self.assertRaises(ValueError, mh903_calcola, **kw)
        val = mh903_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def903\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh903_demo().keys()), lette - set(mh903_demo().keys()))
        self.assertEqual(lette, set(mh903_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc903\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc903\["([^"]+)"\]', src))
        attese = set(mh903_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 902 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 903.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 904)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab903:"), 1)
        self.assertTrue(src.startswith("    # W908"))

    def test_ui_tab903_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab903:"), 1)
        self.assertIn("def mh903_demo(", src_h)
        self.assertIn("def mh903_calcola(", src_h)
        self.assertIn("tab903", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Mercato infragiornaliero (MI): l'arbitraggio intraday con batteria paga?", src)
        self.assertIn("⏱️⚡ Mercato infragiornaliero (MI): l'arbitraggio intraday con batteria paga?", src)
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
        chiavi = re.findall(r'key="(st903_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st903_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 19)
        self.assertIn('key="st903_calcola"', src)
        self.assertIn('key="st903_csv"', src)
        self.assertIn('key="st903_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg903"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos903", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"st\.slider\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)

    def test_ui_nessun_trattino_lungo(self):
        # Il titolo prescritto della scheda
        # contiene un trattino lungo nella riga
        # h1: quella riga e' esclusa dal controllo,
        # tutto il resto deve esserne privo.
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            righe = [r for r in src.split("\n") if "<h1>" not in r]
            testo = "\n".join(righe)
            self.assertNotIn(chr(8212), testo)
            self.assertNotIn(chr(8211), testo)

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato) e salvo la
        # riga h1 col titolo prescritto (contiene
        # un trattino lungo).
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
                    if "<h1>" in nodo.value:
                        continue
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)


if __name__ == "__main__":
    unittest.main()
