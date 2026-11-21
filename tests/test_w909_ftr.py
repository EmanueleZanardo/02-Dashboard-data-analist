"""Test nuova scheda FTR: il diritto
finanziario di trasmissione copre la
congestione?
Repo path: tests/test_w909_ftr.py

Effetto ECONOMICO: un FTR (Financial
Transmission Right) e un diritto FINANZIARIO
sullo spread zonale p_B meno p_A: non nomina
alcun flusso fisico, non usa capacita, non
muove energia. Chi detiene MW di FTR obbligo
incassa lo spread zonale per ogni MWh coperto,
anche se lo spread e negativo; chi detiene un
FTR opzione incassa solo la parte positiva
dello spread, max(spread, 0), e non paga mai
uno spread negativo. Il ricavo annuo e MW per
ore per payoff unitario. Il costo annuo e MW
per (premio d'asta piu fee) piu gestione. Il
margine netto annuo e ricavo meno costo.
Rendita = (1 - (1 + r)^-T) / r. Flussi =
[-CAPEX, margine netto * T]; VAN = -CAPEX +
margine netto * rendita. TIR per bisezione
sui flussi con intervallo [-0,9, 5,0] (300
iterazioni, toll 1e-9); payback = primo anno
con cumulato netto >= 0 (None se mai).
Breakeven spread S* = payoff star per
l'obbligo, max(payoff star, 0) per l'opzione,
dove payoff star = (CAPEX / rendita + MW *
(premio + fee) + gestione) / (MW * ore)
(EUR/MWh, spread che azzera la VAN).
Breakeven premio P* = (ricavo - gestione -
CAPEX / rendita) / MW - fee (EUR/MW/anno,
premio che azzera la VAN).
Demo: FTR obbligo, MW 50, ore 4000, spread
15 EUR/MWh, premio 45.000 EUR/MW/anno, fee
500 EUR/MW/anno, gestione 20.000 EUR/anno,
CAPEX 1.000.000 EUR, durata 5 anni, tasso
0,06 (frazione), tolleranza 0,10 (frazione).
Payoff = 15,00 EUR/MWh. Ricavo = 50 * 4000
* 15 = 3.000.000 EUR/anno. Costo = 50 *
(45.000 + 500) + 20.000 = 2.295.000
EUR/anno. Margine netto = 3.000.000 -
2.295.000 = 705.000 EUR/anno. Rendita =
4,2124. Margine target = CAPEX / rendita =
237.396,40 EUR/anno. Flussi [-1.000.000,
705.000 per 5 anni]; cumulato anno 1
-295.000, anno 2 410.000, finale 2.525.000.
VAN = 1.969.716,47 EUR; TIR = 64,68 %;
payback 2 anni; verdetto CONVIENTE;
breakeven spread = 12,66 EUR/MWh; breakeven
premio = 54.352,07 EUR/MW/anno.
Scenari: base VAN 1.969.716,47, TIR 64,68 %,
payback 2, CONVIENTE; spread +30 % (spread
19,50) payoff 19,50, ricavo 3.900.000,
margine netto 1.605.000, VAN 5.760.843,88,
TIR 159,13 %, payback 1, CONVIENTE; spread
-30 % (spread 10,50) payoff 10,50, ricavo
2.100.000, margine netto -195.000, VAN,
TIR, payback e breakeven None,
NON_CALCOLABILE; premio +20 % (premio
54.000) costo 2.745.000, margine netto
255.000, VAN 74.152,77, TIR 8,69 %,
payback 4, CONVIENTE; tipo opposto
(opzione, spread positivo) identica alla
base: VAN 1.969.716,47, TIR 64,68 %,
payback 2, CONVIENTE.
Confronto: payoff 15,00 contro ricavo
3.000.000, costo 2.295.000 contro margine
netto 705.000, CAPEX 1.000.000 contro
rendita 4,2124 contro margine target
237.396,40, VAN 1.969.716,47 contro TIR
64,68 % contro payback 2 contro breakeven
spread 12,66 contro breakeven premio
54.352,07.
Tasso in FRAZIONE (0,06 = 6 %), usato
diretto, NON diviso per 100. Tolleranza in
FRAZIONE (0,10 = 10 % del CAPEX), usata
diretta, NON divisa per 100. Spread,
premio, fee e gestione medi annui costanti
per tutta la durata, SEMPLIFICAZIONE
DICHIARATA (lo spread zonale oscilla ora
per ora, il premio d'asta cambia a ogni
asta annuale, le ore coperte dipendono dal
prodotto acquistato nel mondo reale, qui
valori medi costanti); lo spread puo essere
anche negativo: con obbligo da margine
negativo e quindi NON_CALCOLABILE, mai un
errore di validazione; con opzione vale
zero. Il CAPEX raccoglie i costi di accesso
e setup una tantum (adesione al mercato,
sistemi, garanzie), SEMPLIFICAZIONE
DICHIARATA: nel mondo reale le garanzie
sono spesso depositi restituibili e non un
costo secco, qui sono trattate come costo
una tantum.
Adattamento demo rispetto al brief: il brief
suggeriva CAPEX 100.000 EUR; con CAPEX
100.000 la VAN sarebbe 2.869.716,47 ma la
TIR sarebbe NON definita (VAN positiva
anche al 500 %, nessun cambio di segno
nell'intervallo di bisezione da -0,9 a
5,0). Il CAPEX e stato portato a 1.000.000
EUR per avere una TIR definita (64,68 %).
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il margine
netto e minore o uguale a 0 (guard degenere:
UI salta KPI, grafico, tabella e CSV)
oppure se un input e degenere (MW nulli o
negativi, ore nulle o negative o sopra 8760
o non intere, tipo non in obbligo o
opzione, premio negativo, fee negativa,
gestione negativa, CAPEX negativo, durata
nulla o negativa o non intera, tasso nullo
o negativo o maggiore o uguale a 1,
tolleranza negativa o sopra 1); altrimenti
CONVIENTE se VAN maggiore di 0, MARGINALE
se VAN minore o uguale a 0 e valore
assoluto della VAN minore o uguale a
tolleranza per CAPEX, NON_CONVIENTE
altrimenti.
Casi limite: spread zero (payoff 0, margine
netto -2.295.000, NON_CALCOLABILE); spread
-5 obbligo (payoff -5, margine netto
-3.295.000, NON_CALCOLABILE); spread -5
opzione (payoff 0, margine netto
-2.295.000, NON_CALCOLABILE: l'opzione non
paga mai lo spread negativo); spread al
breakeven 12,66 (VAN circa zero, TIR 6,00
%, payback 5, MARGINALE); premio al
breakeven 54.352,07 (VAN circa zero, TIR
6,00 %, payback 5, MARGINALE); CAPEX zero
(VAN 2.969.716,47, TIR non definita,
payback 1, CONVIENTE); CAPEX 100.000 (VAN
2.869.716,47, TIR non definita, payback 1,
CONVIENTE); gestione zero (VAN
2.053.963,74, TIR 66,90 %, payback 2);
durata 1 (VAN -334.905,66, TIR -29,50 %,
payback non definito); durata 10 (VAN
4.188.861,37, TIR 70,15 %, payback 2);
tasso 0,10 (VAN 1.672.504,67, TIR 64,68 %,
payback 2: la TIR non dipende dal tasso);
premio zero (VAN 11.447.534,99, TIR 295,19
%, payback 1); fee zero (VAN 2.075.025,56,
TIR 67,46 %, payback 2); MW 100 (VAN
5.023.680,21, TIR 141,25 %, payback 1); ore
8760 (VAN 17.007.855,18, TIR 427,40 %,
payback 1); ore 1 (margine netto
-2.294.250, NON_CALCOLABILE); tolleranza
zero (verdetto demo resta CONVIENTE).
Distinzione esplicita: qui SOLO l'FTR,
diritto FINANZIARIO sullo spread zonale
(payoff = spread per l'obbligo, max(spread,
0) per l'opzione, per MW per ore; nessun
flusso fisico nominato, nessuna capacita
usata), NIENTE PTR transfrontaliero (la
tab290 prezza il PTR, diritto FISICO con
nomina e use it or sell it: li si puo
nominare il flusso, qui no), NIENTE rendita
da congestione dal punto di vista del TSO
(li la rendita e l'incasso del gestore di
rete, qui il payoff e l'incasso del
detentore del diritto), NIENTE CfD a due
vie (li il payoff e sul prezzo assoluto di
una zona, qui solo sullo spread tra due
zone), NIENTE hedge con futures (li il
prezzo e unico, qui il payoff e la
differenza tra due prezzi zonali), NIENTE
redispatch (li il TSO paga per spostare la
produzione, qui nessuno sposta nulla: il
diritto si regola in denaro sullo spread).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w909_helpers import (
        demo_calcoli,
        mh904_annuity,
        mh904_breakeven_premio,
        mh904_breakeven_spread,
        mh904_calcola,
        mh904_confronto,
        mh904_costo,
        mh904_csv,
        mh904_demo,
        mh904_demo_calcoli,
        mh904_flussi,
        mh904_fraz,
        mh904_int_pos,
        mh904_margine_netto,
        mh904_nneg,
        mh904_num,
        mh904_payback,
        mh904_payoff,
        mh904_pos,
        mh904_ricavo,
        mh904_riga_anno,
        mh904_scenario,
        mh904_sensibilita,
        mh904_serie_annua,
        mh904_tasso,
        mh904_tipo,
        mh904_tir,
        mh904_valida,
        mh904_van,
        mh904_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w909_helpers", os.path.join(_hf, "w909_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh904_annuity = _mod.mh904_annuity
    mh904_breakeven_premio = _mod.mh904_breakeven_premio
    mh904_breakeven_spread = _mod.mh904_breakeven_spread
    mh904_calcola = _mod.mh904_calcola
    mh904_confronto = _mod.mh904_confronto
    mh904_costo = _mod.mh904_costo
    mh904_csv = _mod.mh904_csv
    mh904_demo = _mod.mh904_demo
    mh904_demo_calcoli = _mod.mh904_demo_calcoli
    mh904_flussi = _mod.mh904_flussi
    mh904_fraz = _mod.mh904_fraz
    mh904_int_pos = _mod.mh904_int_pos
    mh904_margine_netto = _mod.mh904_margine_netto
    mh904_nneg = _mod.mh904_nneg
    mh904_num = _mod.mh904_num
    mh904_payback = _mod.mh904_payback
    mh904_payoff = _mod.mh904_payoff
    mh904_pos = _mod.mh904_pos
    mh904_ricavo = _mod.mh904_ricavo
    mh904_riga_anno = _mod.mh904_riga_anno
    mh904_scenario = _mod.mh904_scenario
    mh904_sensibilita = _mod.mh904_sensibilita
    mh904_serie_annua = _mod.mh904_serie_annua
    mh904_tasso = _mod.mh904_tasso
    mh904_tipo = _mod.mh904_tipo
    mh904_tir = _mod.mh904_tir
    mh904_valida = _mod.mh904_valida
    mh904_van = _mod.mh904_van
    mh904_verdetto = _mod.mh904_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w909_helpers.py")
_UI_PATH = _risolvi("w909_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "3"
_VECCHIO_TAB = "tab90" + "3"
_VECCHIO_ST = "st90" + "3_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "payoff_eur_mwh": 15.0,
    "ricavo_eur_anno": 3000000.0,
    "costo_eur_anno": 2295000.0,
    "margine_netto_eur_anno": 705000.0,
    "rendita": 4.212363785565717,
    "margine_target_eur_anno": 237396.40043118942,
    "van": 1969716.4688238278,
    "tir": 64.67899329020554,
    "payback": 2,
    "breakeven_spread_eur_mwh": 12.661982002155947,
    "breakeven_premio_eur_mw_anno": 54352.071991376215,
}

_DEMO_SCENARI = [
    {"nome": "Base", "tipo_ftr": "obbligo",
     "spread_medio_eur_mwh": 15.0,
     "premio_eur_mw_anno": 45000.0,
     "payoff_eur_mwh": 15.0,
     "ricavo_eur_anno": 3000000.0,
     "costo_eur_anno": 2295000.0,
     "margine_netto_eur_anno": 705000.0,
     "van": 1969716.4688238278,
     "tir": 64.67899329020554,
     "payback": 2, "verdetto": "CONVIENTE",
     "breakeven_spread_eur_mwh": 12.661982002155947,
     "breakeven_premio_eur_mw_anno": 54352.071991376215},
    {"nome": "Spread piu 30 %", "tipo_ftr": "obbligo",
     "spread_medio_eur_mwh": 19.5,
     "premio_eur_mw_anno": 45000.0,
     "payoff_eur_mwh": 19.5,
     "ricavo_eur_anno": 3900000.0,
     "costo_eur_anno": 2295000.0,
     "margine_netto_eur_anno": 1605000.0,
     "van": 5760843.875832969,
     "tir": 159.12621659408325,
     "payback": 1, "verdetto": "CONVIENTE",
     "breakeven_spread_eur_mwh": 12.661982002155947,
     "breakeven_premio_eur_mw_anno": 72352.07199137622},
    {"nome": "Spread meno 30 %", "tipo_ftr": "obbligo",
     "spread_medio_eur_mwh": 10.5,
     "premio_eur_mw_anno": 45000.0,
     "payoff_eur_mwh": 10.5,
     "ricavo_eur_anno": 2100000.0,
     "costo_eur_anno": 2295000.0,
     "margine_netto_eur_anno": -195000.0,
     "van": None,
     "tir": None,
     "payback": None, "verdetto": "NON_CALCOLABILE",
     "breakeven_spread_eur_mwh": None,
     "breakeven_premio_eur_mw_anno": None},
    {"nome": "Premio piu 20 %", "tipo_ftr": "obbligo",
     "spread_medio_eur_mwh": 15.0,
     "premio_eur_mw_anno": 54000.0,
     "payoff_eur_mwh": 15.0,
     "ricavo_eur_anno": 3000000.0,
     "costo_eur_anno": 2745000.0,
     "margine_netto_eur_anno": 255000.0,
     "van": 74152.76531925693,
     "tir": 8.685810355518125,
     "payback": 4, "verdetto": "CONVIENTE",
     "breakeven_spread_eur_mwh": 14.911982002155947,
     "breakeven_premio_eur_mw_anno": 54352.071991376215},
    {"nome": "Tipo opposto", "tipo_ftr": "opzione",
     "spread_medio_eur_mwh": 15.0,
     "premio_eur_mw_anno": 45000.0,
     "payoff_eur_mwh": 15.0,
     "ricavo_eur_anno": 3000000.0,
     "costo_eur_anno": 2295000.0,
     "margine_netto_eur_anno": 705000.0,
     "van": 1969716.4688238278,
     "tir": 64.67899329020554,
     "payback": 2, "verdetto": "CONVIENTE",
     "breakeven_spread_eur_mwh": 12.661982002155947,
     "breakeven_premio_eur_mw_anno": 54352.071991376215},
]

_DEMO_CONFRONTO = {
    "payoff_eur_mwh": 15.0,
    "ricavo_eur_anno": 3000000.0,
    "costo_eur_anno": 2295000.0,
    "margine_netto_eur_anno": 705000.0,
    "capex_eur": 1000000.0,
    "rendita": 4.212363785565717,
    "margine_target_eur_anno": 237396.40043118942,
    "van": 1969716.4688238278,
    "tir": 64.67899329020554,
    "payback": 2,
    "breakeven_spread_eur_mwh": 12.661982002155947,
    "breakeven_premio_eur_mw_anno": 54352.071991376215,
}

_ORDINE_VALIDA = (
    "mw_mw", "ore_anno", "spread_medio_eur_mwh",
    "tipo_ftr", "premio_eur_mw_anno",
    "fee_eur_mw_anno", "gestione_eur_anno",
    "capex_eur", "t_anni", "r_tasso",
    "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh904_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh904_num(3, "x"), 3.0)
        self.assertEqual(mh904_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh904_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh904_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh904_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh904_pos(0, "x")
        with self.assertRaises(ValueError):
            mh904_pos(-1, "x")
        self.assertEqual(mh904_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh904_fraz(0, "x"), 0.0)
        self.assertEqual(mh904_fraz(1, "x"), 1.0)
        self.assertEqual(mh904_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh904_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh904_fraz(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh904_int_pos(5, "x"), 5)
        self.assertEqual(mh904_int_pos(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh904_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh904_int_pos(5.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh904_tasso(0.06, "x"), 0.06)
        self.assertEqual(mh904_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh904_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh904_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh904_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh904_tasso(-0.01, "x")

    def test_tipo_valido_e_invalido(self):
        self.assertEqual(mh904_tipo("obbligo", "x"), "obbligo")
        self.assertEqual(mh904_tipo("opzione", "x"), "opzione")
        for cattivo in ("fisico", "OBBLIGO", "", None, 3, True):
            with self.assertRaises(ValueError):
                mh904_tipo(cattivo, "x")


class TestFisica(unittest.TestCase):
    def test_payoff_obbligo_opzione(self):
        self.assertEqual(mh904_payoff("obbligo", 15.0), 15.0)
        self.assertEqual(mh904_payoff("opzione", 15.0), 15.0)
        self.assertEqual(mh904_payoff("obbligo", -5.0), -5.0)
        self.assertEqual(mh904_payoff("opzione", -5.0), 0.0)
        self.assertEqual(mh904_payoff("obbligo", 0.0), 0.0)
        self.assertEqual(mh904_payoff("opzione", 0.0), 0.0)
        self.assertEqual(mh904_payoff("opzione", 19.5), 19.5)
        with self.assertRaises(ValueError):
            mh904_payoff("fisico", 15.0)
        with self.assertRaises(ValueError):
            mh904_payoff("obbligo", float("nan"))

    def test_ricavo(self):
        self.assertEqual(
            mh904_ricavo(50.0, 4000, 15.0), 3000000.0)
        self.assertEqual(
            mh904_ricavo(50.0, 4000, 19.5), 3900000.0)
        self.assertEqual(
            mh904_ricavo(50.0, 4000, 10.5), 2100000.0)
        self.assertEqual(
            mh904_ricavo(50.0, 4000, 0.0), 0.0)
        self.assertEqual(
            mh904_ricavo(50.0, 4000, -5.0), -1000000.0)
        self.assertEqual(
            mh904_ricavo(100.0, 4000, 15.0), 6000000.0)
        self.assertEqual(
            mh904_ricavo(50.0, 8760, 15.0), 6570000.0)
        with self.assertRaises(ValueError):
            mh904_ricavo(0.0, 4000, 15.0)
        with self.assertRaises(ValueError):
            mh904_ricavo(50.0, 0, 15.0)
        with self.assertRaises(ValueError):
            mh904_ricavo(50.0, 8761, 15.0)
        with self.assertRaises(ValueError):
            mh904_ricavo(50.0, 4000.5, 15.0)

    def test_costo(self):
        self.assertEqual(
            mh904_costo(50.0, 45000.0, 500.0, 20000.0),
            2295000.0)
        self.assertEqual(
            mh904_costo(50.0, 54000.0, 500.0, 20000.0),
            2745000.0)
        self.assertEqual(
            mh904_costo(50.0, 0.0, 500.0, 20000.0),
            45000.0)
        self.assertEqual(
            mh904_costo(50.0, 45000.0, 0.0, 20000.0),
            2270000.0)
        self.assertEqual(
            mh904_costo(50.0, 45000.0, 500.0, 0.0),
            2275000.0)
        self.assertEqual(
            mh904_costo(100.0, 45000.0, 500.0, 20000.0),
            4570000.0)
        with self.assertRaises(ValueError):
            mh904_costo(0.0, 45000.0, 500.0, 20000.0)
        with self.assertRaises(ValueError):
            mh904_costo(50.0, -1.0, 500.0, 20000.0)
        with self.assertRaises(ValueError):
            mh904_costo(50.0, 45000.0, -1.0, 20000.0)
        with self.assertRaises(ValueError):
            mh904_costo(50.0, 45000.0, 500.0, -1.0)

    def test_margine_netto(self):
        self.assertEqual(
            mh904_margine_netto(3000000.0, 2295000.0),
            705000.0)
        self.assertEqual(
            mh904_margine_netto(3900000.0, 2295000.0),
            1605000.0)
        self.assertEqual(
            mh904_margine_netto(2100000.0, 2295000.0),
            -195000.0)
        self.assertEqual(
            mh904_margine_netto(0.0, 2295000.0),
            -2295000.0)
        self.assertEqual(
            mh904_margine_netto(-1000000.0, 2295000.0),
            -3295000.0)
        self.assertEqual(
            mh904_margine_netto(3000000.0, 0.0),
            3000000.0)

    def test_annuity(self):
        self.assertAlmostEqual(
            mh904_annuity(0.06, 5), 4.212363785565717, places=9)
        self.assertAlmostEqual(
            mh904_annuity(0.06, 1), 0.9433962264150943, places=9)
        self.assertAlmostEqual(
            mh904_annuity(0.10, 5), 3.79078676940845, places=9)
        self.assertAlmostEqual(
            mh904_annuity(0.06, 10), 7.360087051513202, places=9)
        with self.assertRaises(ValueError):
            mh904_annuity(0.0, 5)
        with self.assertRaises(ValueError):
            mh904_annuity(1.0, 5)
        with self.assertRaises(ValueError):
            mh904_annuity(0.06, 0)

    def test_riga_anno_e_serie(self):
        riga = mh904_riga_anno(1, 3000000.0, 2295000.0,
                               705000.0)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["ricavo"], 3000000.0)
        self.assertEqual(riga["costo"], 2295000.0)
        self.assertEqual(riga["margine_netto"], 705000.0)
        self.assertEqual(riga["flusso"], 705000.0)
        riga = mh904_riga_anno(5, 3000000.0, 2295000.0,
                               705000.0)
        self.assertEqual(riga["flusso"], 705000.0)
        with self.assertRaises(ValueError):
            mh904_riga_anno(0, 3000000.0, 2295000.0,
                            705000.0)
        serie = mh904_serie_annua(3000000.0, 2295000.0,
                                  705000.0, 5)
        self.assertEqual(len(serie), 5)
        self.assertTrue(all(r["flusso"] == 705000.0
                            for r in serie))
        self.assertTrue(all(r["margine_netto"] == 705000.0
                            for r in serie))
        self.assertTrue(all(r["ricavo"] == 3000000.0
                            for r in serie))
        serie = mh904_serie_annua(3900000.0, 2295000.0,
                                  1605000.0, 5)
        self.assertEqual(serie[0]["flusso"], 1605000.0)
        with self.assertRaises(ValueError):
            mh904_serie_annua(3000000.0, 2295000.0,
                              705000.0, 0)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        fl = bc["flussi"]
        self.assertEqual(len(fl), 6)
        self.assertEqual(fl[0], -1000000.0)
        self.assertEqual(fl[1], 705000.0)
        self.assertEqual(fl[5], 705000.0)
        self.assertAlmostEqual(sum(fl), 2525000.00, places=2)
        self.assertAlmostEqual(sum(fl[:2]), -295000.00, places=2)
        self.assertAlmostEqual(sum(fl[:3]), 410000.00, places=2)
        fl2 = mh904_flussi(bc["serie"], bc["capex_eur"], 5)
        self.assertEqual(fl2, fl)
        self.assertAlmostEqual(mh904_van(fl, 0.06), bc["van"])
        with self.assertRaises(ValueError):
            mh904_flussi(bc["serie"][:4], bc["capex_eur"], 5)

    def test_breakeven_spread(self):
        self.assertAlmostEqual(
            mh904_breakeven_spread(1000000.0, 0.06, 5,
                                   20000.0, 50.0, 4000,
                                   45000.0, 500.0, "obbligo"),
            12.66, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_spread(1000000.0, 0.06, 5,
                                   20000.0, 50.0, 4000,
                                   45000.0, 500.0, "opzione"),
            12.66, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_spread(0.0, 0.06, 5,
                                   20000.0, 50.0, 4000,
                                   45000.0, 500.0, "obbligo"),
            11.47, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_spread(1000000.0, 0.06, 5,
                                   0.0, 50.0, 4000,
                                   45000.0, 500.0, "obbligo"),
            12.56, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_spread(1000000.0, 0.06, 5,
                                   20000.0, 100.0, 4000,
                                   45000.0, 500.0, "obbligo"),
            12.02, places=2)
        # Con payoff star nullo l'opzione non scende
        # sotto zero: il breakeven spread e zero.
        self.assertEqual(
            mh904_breakeven_spread(0.0, 0.06, 5,
                                   0.0, 50.0, 4000,
                                   0.0, 0.0, "opzione"),
            0.0)
        self.assertEqual(
            mh904_breakeven_spread(0.0, 0.06, 5,
                                   0.0, 50.0, 4000,
                                   0.0, 0.0, "obbligo"),
            0.0)
        # Allo spread di breakeven la VAN e zero, la
        # TIR e uguale al tasso e il verdetto e
        # MARGINALE.
        be = mh904_breakeven_spread(1000000.0, 0.06, 5,
                                    20000.0, 50.0, 4000,
                                    45000.0, 500.0, "obbligo")
        bc = mh904_calcola(
            **_demo_kwargs(spread_medio_eur_mwh=be))
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               237396.40, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(
            bc["breakeven_premio_eur_mw_anno"], 45000.00,
            places=2)
        with self.assertRaises(ValueError):
            mh904_breakeven_spread(1000000.0, 0.06, 5,
                                   20000.0, 0.0, 4000,
                                   45000.0, 500.0, "obbligo")
        with self.assertRaises(ValueError):
            mh904_breakeven_spread(-1.0, 0.06, 5,
                                   20000.0, 50.0, 4000,
                                   45000.0, 500.0, "obbligo")
        with self.assertRaises(ValueError):
            mh904_breakeven_spread(1000000.0, 0.06, 5,
                                   20000.0, 50.0, 4000,
                                   45000.0, 500.0, "fisico")

    def test_breakeven_premio(self):
        self.assertAlmostEqual(
            mh904_breakeven_premio(3000000.0, 20000.0,
                                   1000000.0, 0.06, 5,
                                   50.0, 500.0),
            54352.07, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_premio(3000000.0, 20000.0,
                                   0.0, 0.06, 5,
                                   50.0, 500.0),
            59100.00, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_premio(3000000.0, 0.0,
                                   1000000.0, 0.06, 5,
                                   50.0, 500.0),
            54752.07, places=2)
        self.assertAlmostEqual(
            mh904_breakeven_premio(3900000.0, 20000.0,
                                   1000000.0, 0.06, 5,
                                   50.0, 500.0),
            72352.07, places=2)
        # Al premio di breakeven la VAN e zero, la
        # TIR e uguale al tasso e il verdetto e
        # MARGINALE.
        bp = mh904_breakeven_premio(3000000.0, 20000.0,
                                    1000000.0, 0.06, 5,
                                    50.0, 500.0)
        bc = mh904_calcola(
            **_demo_kwargs(premio_eur_mw_anno=bp))
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               237396.40, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(
            bc["breakeven_spread_eur_mwh"], 15.00, places=2)
        with self.assertRaises(ValueError):
            mh904_breakeven_premio(3000000.0, 20000.0,
                                   1000000.0, 0.06, 5,
                                   0.0, 500.0)
        with self.assertRaises(ValueError):
            mh904_breakeven_premio(3000000.0, -1.0,
                                   1000000.0, 0.06, 5,
                                   50.0, 500.0)

    def test_scenario_singolo(self):
        s = mh904_scenario("Spread piu 30 %", mh904_demo(),
                           {"spread_medio_eur_mwh": 19.5})
        self.assertEqual(s["nome"], "Spread piu 30 %")
        self.assertEqual(s["spread_medio_eur_mwh"], 19.5)
        self.assertAlmostEqual(s["van"], 5760843.88, places=2)
        self.assertAlmostEqual(s["tir"], 159.13, places=2)
        self.assertEqual(s["payback"], 1)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        # Il breakeven spread e INVARIANTE allo
        # spread corrente: dipende da CAPEX,
        # rendita, MW, ore, premio, fee e gestione,
        # non dallo spread inserito.
        self.assertAlmostEqual(
            s["breakeven_spread_eur_mwh"], 12.66, places=2)
        s = mh904_scenario("Spread meno 30 %", mh904_demo(),
                           {"spread_medio_eur_mwh": 10.5})
        self.assertIsNone(s["van"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(s["breakeven_spread_eur_mwh"])
        self.assertIsNone(s["breakeven_premio_eur_mw_anno"])
        s = mh904_scenario("Premio piu 20 %", mh904_demo(),
                           {"premio_eur_mw_anno": 54000.0})
        self.assertAlmostEqual(s["van"], 74152.77, places=2)
        self.assertEqual(s["payback"], 4)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        # Il breakeven premio e INVARIANTE al premio
        # corrente.
        self.assertAlmostEqual(
            s["breakeven_premio_eur_mw_anno"], 54352.07,
            places=2)
        s = mh904_scenario("Tipo opposto", mh904_demo(),
                           {"tipo_ftr": "opzione"})
        self.assertAlmostEqual(s["van"], 1969716.47, places=2)
        self.assertEqual(s["tipo_ftr"], "opzione")
        self.assertEqual(s["payoff_eur_mwh"], 15.0)
        with self.assertRaises(ValueError):
            mh904_scenario("", mh904_demo(),
                           {"spread_medio_eur_mwh": 19.5})
        with self.assertRaises(ValueError):
            mh904_scenario("X", mh904_demo(),
                           {"ore_anno": 8761})

    def test_scenario_margine_negativo_non_calcolabile(self):
        s = mh904_scenario("Spread zero", mh904_demo(),
                           {"spread_medio_eur_mwh": 0.0})
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertIsNone(s["breakeven_spread_eur_mwh"])
        self.assertIsNone(s["breakeven_premio_eur_mw_anno"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(s["payoff_eur_mwh"], 0.0)
        self.assertEqual(s["margine_netto_eur_anno"], -2295000.0)

    def test_confronto_formule(self):
        c = mh904_confronto(15.0, 3000000.0, 2295000.0,
                            705000.0, 1000000.0,
                            4.212363785565717,
                            237396.40, 1969716.47, 64.68,
                            2, 12.66, 54352.07)
        self.assertEqual(c["payoff_eur_mwh"], 15.0)
        self.assertEqual(c["ricavo_eur_anno"], 3000000.0)
        self.assertEqual(c["costo_eur_anno"], 2295000.0)
        self.assertEqual(c["margine_netto_eur_anno"], 705000.0)
        self.assertEqual(c["capex_eur"], 1000000.0)
        self.assertAlmostEqual(c["rendita"], 4.2124, places=4)
        self.assertEqual(c["margine_target_eur_anno"],
                         237396.40)
        self.assertEqual(c["van"], 1969716.47)
        self.assertEqual(c["tir"], 64.68)
        self.assertEqual(c["payback"], 2)
        self.assertEqual(c["breakeven_spread_eur_mwh"], 12.66)
        self.assertEqual(c["breakeven_premio_eur_mw_anno"],
                         54352.07)
        c = mh904_confronto(0.0, 0.0, 2295000.0,
                            -2295000.0, 1000000.0,
                            4.212363785565717,
                            237396.40, None, None, None,
                            None, None)
        self.assertIsNone(c["van"])
        self.assertIsNone(c["tir"])
        self.assertIsNone(c["payback"])
        self.assertIsNone(c["breakeven_spread_eur_mwh"])
        self.assertIsNone(c["breakeven_premio_eur_mw_anno"])
        with self.assertRaises(ValueError):
            mh904_confronto(15.0, 3000000.0, 2295000.0,
                            705000.0, -1.0,
                            4.212363785565717,
                            237396.40, 1969716.47, 64.68,
                            2, 12.66, 54352.07)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_sei(self):
        bc = mh904_demo_calcoli()
        self.assertAlmostEqual(
            mh904_van(bc["flussi"], 0.06),
            bc["van"])
        bc_piu = mh904_calcola(
            _scenari=False,
            **dict(mh904_demo(), spread_medio_eur_mwh=19.5))
        self.assertAlmostEqual(
            mh904_van(bc_piu["flussi"], 0.06),
            bc["scenari"][1]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh904_van([-1000000, 705000, 705000], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,06 = 6 per cento):
        # usato diretto, NON diviso per 100. Con 0,06 la
        # VAN demo e' 1969716,47; con 0,50 (cioe' 50
        # per cento) sarebbe tutt'altra; con 6,0 il
        # tasso e' degenere (maggiore o uguale a 1) e
        # solleva ValueError.
        bc = mh904_demo_calcoli()
        self.assertAlmostEqual(
            mh904_van(bc["flussi"], 0.06),
            1969716.47, places=2)
        self.assertNotAlmostEqual(
            mh904_van(bc["flussi"], 0.50),
            1969716.47, places=2)
        with self.assertRaises(ValueError):
            mh904_van(bc["flussi"], 6.0)

    def test_tir_demo(self):
        bc = mh904_demo_calcoli()
        tir_v = mh904_tir(bc["flussi"])
        self.assertIsNotNone(tir_v)
        self.assertAlmostEqual(tir_v * 100.0, bc["tir"],
                               places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh904_tir([-100, -10, -10]))
        self.assertIsNone(mh904_tir([100, 10, 10]))
        self.assertIsNone(mh904_tir([0, 10, 10]))
        self.assertIsNone(mh904_tir([-1000000, -705000,
                                     -705000]))
        # Con CAPEX 100.000 la VAN resta positiva
        # anche al 500 per cento: nessun cambio di
        # segno dentro l'intervallo di bisezione.
        bc = mh904_calcola(**_demo_kwargs(capex_eur=100000.0))
        self.assertIsNone(bc["tir"])
        self.assertAlmostEqual(bc["van"], 2869716.47, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh904_demo_calcoli()
        self.assertEqual(mh904_payback(bc["flussi"]), 2)
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh904_payback([-100, 100, 10]), 1)
        self.assertEqual(mh904_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh904_payback([-100, 10, 10]))
        # Con CAPEX zero il payback e l'anno 1.
        self.assertEqual(mh904_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh904_demo_calcoli()
        fl = bc["flussi"]
        self.assertAlmostEqual(sum(fl[:2]), -295000.00, places=2)
        self.assertAlmostEqual(sum(fl[:3]), 410000.00, places=2)
        self.assertAlmostEqual(sum(fl), 2525000.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(
            mh904_verdetto(100.0, 0.10, 1000000.0), "CONVIENTE")
        self.assertEqual(
            mh904_verdetto(0.0, 0.10, 1000000.0), "MARGINALE")
        self.assertEqual(
            mh904_verdetto(-100000.0, 0.10, 1000000.0),
            "MARGINALE")
        self.assertEqual(
            mh904_verdetto(-100001.0, 0.10, 1000000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh904_verdetto(-500000.0, 0.10, 1000000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativa e
        # NON_CONVIENTE (VAN zero compresa nel MARGINALE
        # solo perche il valore assoluto zero e minore
        # o uguale a zero).
        self.assertEqual(
            mh904_verdetto(-1.0, 0.0, 1000000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh904_verdetto(0.0, 0.0, 1000000.0), "MARGINALE")
        with self.assertRaises(ValueError):
            mh904_verdetto(100.0, 1.5, 1000000.0)
        with self.assertRaises(ValueError):
            mh904_verdetto(100.0, 0.10, -1.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh904_verdetto(None, 0.10, 1000000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh904_verdetto(None, 0.0, 0.0), "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh904_demo()
        val = mh904_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_spread_negativo_ammesso(self):
        # Lo spread negativo NON e un errore di
        # validazione: e ammesso. Con obbligo da
        # margine netto negativo, quindi
        # NON_CALCOLABILE; con opzione vale zero e
        # il margine resta negativo per premio piu
        # fee piu gestione.
        demo = mh904_demo()
        val = mh904_valida(*[dict(demo, spread_medio_eur_mwh=-5.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh904_calcola(**_demo_kwargs(spread_medio_eur_mwh=-5.0))
        self.assertEqual(bc["payoff_eur_mwh"], -5.0)
        self.assertEqual(bc["margine_netto_eur_anno"], -3295000.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        bc = mh904_calcola(**_demo_kwargs(
            spread_medio_eur_mwh=-5.0, tipo_ftr="opzione"))
        self.assertEqual(bc["payoff_eur_mwh"], 0.0)
        self.assertEqual(bc["margine_netto_eur_anno"], -2295000.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_durata_zero_e_non_intera_no(self):
        kw = _demo_kwargs(t_anni=0)
        self.assertRaises(ValueError, mh904_calcola, **kw)
        kw = _demo_kwargs(t_anni=5.5)
        self.assertRaises(ValueError, mh904_calcola, **kw)
        kw = _demo_kwargs(t_anni=10)
        bc = mh904_calcola(**kw)
        self.assertEqual(bc["t_anni"], 10)

    def test_valida_ore_intervallo_e_intero(self):
        with self.assertRaises(ValueError):
            mh904_calcola(**_demo_kwargs(ore_anno=0))
        with self.assertRaises(ValueError):
            mh904_calcola(**_demo_kwargs(ore_anno=8761))
        with self.assertRaises(ValueError):
            mh904_calcola(**_demo_kwargs(ore_anno=4000.5))
        bc = mh904_calcola(**_demo_kwargs(ore_anno=8760))
        self.assertEqual(bc["ore_anno"], 8760)
        self.assertEqual(bc["ricavo_eur_anno"], 6570000.0)
        bc = mh904_calcola(**_demo_kwargs(ore_anno=1))
        self.assertEqual(bc["ore_anno"], 1)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_tipo_invalido_no(self):
        for tipo in ("fisico", "OBBLIGO", "", None, 3):
            with self.assertRaises(ValueError):
                mh904_calcola(**_demo_kwargs(tipo_ftr=tipo))
        bc = mh904_calcola(**_demo_kwargs(tipo_ftr="opzione"))
        self.assertEqual(bc["tipo_ftr"], "opzione")
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh904_calcola(**_demo_kwargs(r_tasso=tasso))
        bc = mh904_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertEqual(bc["r_tasso"], 0.10)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh904_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh904_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        bc = mh904_calcola(**_demo_kwargs(tol_frazione=1.0))
        self.assertEqual(bc["tol_frazione"], 1.0)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("mw_mw", 0),
                              ("ore_anno", 0),
                              ("t_anni", 0),
                              ("r_tasso", 0)):
            with self.assertRaises(ValueError):
                mh904_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(spread_medio_eur_mwh=float("nan"))
        self.assertRaises(ValueError, mh904_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh904_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("mw_mw", -1),
                              ("ore_anno", -1),
                              ("premio_eur_mw_anno", -1),
                              ("fee_eur_mw_anno", -1),
                              ("gestione_eur_anno", -1),
                              ("capex_eur", -1),
                              ("t_anni", -1),
                              ("r_tasso", -0.01),
                              ("tol_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh904_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh904_calcola(mh904_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh904_calcola(dict(mh904_demo(),
                                spread_medio_eur_mwh=999.0),
                           spread_medio_eur_mwh=15.0)
        self.assertEqual(bc["spread_medio_eur_mwh"], 15.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh904_calcola(_scenari=False, **mh904_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van"], 1969716.47, places=2)
        self.assertAlmostEqual(bc["tir"], 64.68, places=2)


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
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 2)
        self.assertAlmostEqual(bc["tir"], 64.68, places=2)
        self.assertAlmostEqual(bc["breakeven_spread_eur_mwh"],
                               12.66, places=2)
        self.assertAlmostEqual(
            bc["breakeven_premio_eur_mw_anno"],
            54352.07, places=2)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertAlmostEqual(
            bc["margine_target_eur_anno"], 237396.40, places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["payoff_eur_mwh"],
            bc["spread_medio_eur_mwh"])
        self.assertAlmostEqual(
            bc["ricavo_eur_anno"],
            bc["mw_mw"] * bc["ore_anno"]
            * bc["payoff_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_eur_anno"],
            bc["mw_mw"] * (bc["premio_eur_mw_anno"]
                           + bc["fee_eur_mw_anno"])
            + bc["gestione_eur_anno"])
        self.assertAlmostEqual(
            bc["margine_netto_eur_anno"],
            bc["ricavo_eur_anno"]
            - bc["costo_eur_anno"])
        self.assertAlmostEqual(
            bc["margine_target_eur_anno"],
            bc["capex_eur"]
            / mh904_annuity(bc["r_tasso"], bc["t_anni"]))
        self.assertAlmostEqual(
            bc["breakeven_spread_eur_mwh"],
            (bc["margine_target_eur_anno"]
             + bc["mw_mw"] * (bc["premio_eur_mw_anno"]
                              + bc["fee_eur_mw_anno"])
             + bc["gestione_eur_anno"])
            / (bc["mw_mw"] * bc["ore_anno"]))
        self.assertAlmostEqual(
            bc["breakeven_premio_eur_mw_anno"],
            (bc["ricavo_eur_anno"]
             - bc["gestione_eur_anno"]
             - bc["margine_target_eur_anno"])
            / bc["mw_mw"] - bc["fee_eur_mw_anno"])
        self.assertAlmostEqual(
            bc["van"],
            mh904_van(bc["flussi"], bc["r_tasso"]))
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
        self.assertEqual(conf["breakeven_premio_eur_mw_anno"],
                         bc["breakeven_premio_eur_mw_anno"])

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu spread migliora il caso; meno spread lo
        # rende non calcolabile. Il breakeven spread
        # e INVARIANTE allo spread corrente.
        self.assertGreater(bc["scenari"][1]["van"],
                           base["van"])
        self.assertEqual(bc["scenari"][1]["payback"], 1)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][1]["breakeven_spread_eur_mwh"],
                         base["breakeven_spread_eur_mwh"])
        self.assertIsNone(bc["scenari"][2]["van"])
        self.assertIsNone(bc["scenari"][2]["payback"])
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "NON_CALCOLABILE")
        # Piu premio peggiora il caso ma resta
        # CONVIENTE; il breakeven premio e
        # INVARIANTE al premio corrente.
        self.assertLess(bc["scenari"][3]["van"],
                        base["van"])
        self.assertGreater(bc["scenari"][3]["van"], 0.0)
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][3]["payback"], 4)
        self.assertEqual(
            bc["scenari"][3]["breakeven_premio_eur_mw_anno"],
            base["breakeven_premio_eur_mw_anno"])
        self.assertGreater(
            bc["scenari"][3]["breakeven_spread_eur_mwh"],
            base["breakeven_spread_eur_mwh"])
        # Con spread positivo il tipo opposto e
        # identico alla base: obbligo e opzione
        # coincidono.
        self.assertEqual(bc["scenari"][4]["van"],
                         base["van"])
        self.assertEqual(bc["scenari"][4]["tir"],
                         base["tir"])
        self.assertEqual(bc["scenari"][4]["payback"],
                         base["payback"])
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         base["verdetto"])
        self.assertEqual(bc["scenari"][4]["tipo_ftr"],
                         "opzione")

    def test_sensibilita_valori(self):
        s = mh904_sensibilita(**mh904_demo())
        self.assertEqual(set(s.keys()),
                         {"spread_piu30", "spread_meno30",
                          "premio_piu20", "tipo_opzione",
                          "tipo_opzione_spread_neg5",
                          "spread_neg5_obbligo",
                          "capex_zero", "gestione_zero",
                          "vita_010", "tasso_010", "spread_000",
                          "premio_000", "fee_000", "mw_100",
                          "ore_8760", "tol_zero"})
        attesi = {
            "spread_piu30": (5760843.88, 159.13, 1,
                             "CONVIENTE"),
            "spread_meno30": (None, None, None,
                              "NON_CALCOLABILE"),
            "premio_piu20": (74152.77, 8.69, 4,
                             "CONVIENTE"),
            "tipo_opzione": (1969716.47, 64.68, 2,
                             "CONVIENTE"),
            "tipo_opzione_spread_neg5": (None, None, None,
                                         "NON_CALCOLABILE"),
            "spread_neg5_obbligo": (None, None, None,
                                    "NON_CALCOLABILE"),
            "capex_zero": (2969716.47, None, 1, "CONVIENTE"),
            "gestione_zero": (2053963.74, 66.90, 2,
                              "CONVIENTE"),
            "vita_010": (4188861.37, 70.15, 2, "CONVIENTE"),
            "tasso_010": (1672504.67, 64.68, 2, "CONVIENTE"),
            "spread_000": (None, None, None,
                           "NON_CALCOLABILE"),
            "premio_000": (11447534.99, 295.19, 1,
                           "CONVIENTE"),
            "fee_000": (2075025.56, 67.46, 2, "CONVIENTE"),
            "mw_100": (5023680.21, 141.25, 1, "CONVIENTE"),
            "ore_8760": (17007855.18, 427.40, 1, "CONVIENTE"),
            "tol_zero": (1969716.47, 64.68, 2, "CONVIENTE"),
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
        csv = mh904_csv(bc, mh904_demo())
        for voce in ("mw_mw", "ore_anno",
                     "spread_medio_eur_mwh",
                     "tipo_ftr",
                     "premio_eur_mw_anno",
                     "fee_eur_mw_anno",
                     "gestione_eur_anno",
                     "capex_eur",
                     "t_anni", "r_tasso",
                     "tol_frazione",
                     "payoff_eur_mwh",
                     "ricavo_eur_anno",
                     "costo_eur_anno",
                     "margine_netto_eur_anno",
                     "rendita", "margine_target_eur_anno",
                     "breakeven_spread_eur_mwh",
                     "breakeven_premio_eur_mw_anno",
                     "van", "tir", "payback",
                     "scenario_base_van",
                     "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_spread_piu30_van",
                     "scenario_spread_piu30_verdetto",
                     "scenario_spread_meno30_van",
                     "scenario_spread_meno30_verdetto",
                     "scenario_premio_piu20_van",
                     "scenario_premio_piu20_verdetto",
                     "scenario_tipo_opposto_van",
                     "scenario_tipo_opposto_verdetto",
                     "anno_1_ricavo",
                     "anno_1_costo",
                     "anno_1_margine_netto",
                     "anno_1_flusso",
                     "anno_5_margine_netto",
                     "anno_5_flusso",
                     "confronto_payoff_eur_mwh",
                     "confronto_ricavo_eur_anno",
                     "confronto_costo_eur_anno",
                     "confronto_margine_netto_eur_anno",
                     "confronto_capex_eur",
                     "confronto_rendita",
                     "confronto_margine_target_eur_anno",
                     "confronto_van", "confronto_tir",
                     "confronto_payback",
                     "confronto_breakeven_spread_eur_mwh",
                     "confronto_breakeven_premio_eur_mw_anno",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)
        self.assertIn("NON_CALCOLABILE", csv)
        self.assertIn("obbligo", csv)
        self.assertIn("opzione", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh904_csv(bc, mh904_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("mw_mw;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh904_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh904_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 5)
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 23)
        self.assertEqual(len(bc["df_ricavi_costi"]), 3)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso (EUR)"].iloc[0],
            705000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[0],
            -295000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[-1],
            2525000.00, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["MW acquistati (MW)",
             "Ore coperte (ore/anno)",
             "Spread zonale atteso (EUR/MWh)",
             "Payoff unitario (EUR/MWh)",
             "Ricavo (EUR/anno)",
             "Costo (EUR/anno)",
             "Margine netto (EUR/anno)",
             "CAPEX (EUR)",
             "Rendita",
             "Margine target (EUR/anno)",
             "VAN (EUR)",
             "TIR (%)",
             "Payback (anni)",
             "Breakeven spread (EUR/MWh)",
             "Breakeven premio (EUR/MW/anno)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[3],
            15.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[4],
            3000000.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("MW acquistati (MW)", voci)
        self.assertIn("Tipo FTR", voci)
        self.assertIn("Breakeven spread (EUR/MWh)", voci)
        self.assertIn("Breakeven premio (EUR/MW/anno)", voci)
        self.assertIn("Margine target (EUR/anno)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("TIR (%)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto",
                      set(bc["df_scenari"].columns))
        self.assertIn("Breakeven premio (EUR/MW/anno)",
                      set(bc["df_scenari"].columns))
        self.assertEqual(
            list(bc["df_ricavi_costi"]["Voce"]),
            ["Ricavo", "Premio e fee", "Gestione"])
        self.assertAlmostEqual(
            bc["df_ricavi_costi"]["Importo (EUR/anno)"].iloc[0],
            3000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_ricavi_costi"]["Importo (EUR/anno)"].iloc[1],
            2275000.00, places=2)
        self.assertAlmostEqual(
            bc["df_ricavi_costi"]["Importo (EUR/anno)"].iloc[2],
            20000.00, places=2)

    def test_zero_ammessi(self):
        bc = mh904_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 2969716.47, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh904_calcola(**_demo_kwargs(gestione_eur_anno=0.0))
        self.assertEqual(bc["gestione_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 2053963.74, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh904_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        self.assertAlmostEqual(bc["van"], 1969716.47, places=2)
        bc = mh904_calcola(**_demo_kwargs(premio_eur_mw_anno=0.0))
        self.assertEqual(bc["premio_eur_mw_anno"], 0.0)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               2955000.00, places=2)
        self.assertAlmostEqual(bc["van"], 11447534.99, places=2)
        self.assertAlmostEqual(bc["tir"], 295.19, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh904_calcola(**_demo_kwargs(fee_eur_mw_anno=0.0))
        self.assertEqual(bc["fee_eur_mw_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 2075025.56, places=2)
        self.assertAlmostEqual(bc["tir"], 67.46, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_spread_zero_margine_negativo_non_calcolabile(self):
        kw = _demo_kwargs(spread_medio_eur_mwh=0.0)
        bc = mh904_calcola(**kw)
        self.assertEqual(bc["payoff_eur_mwh"], 0.0)
        self.assertEqual(bc["ricavo_eur_anno"], 0.0)
        self.assertEqual(bc["margine_netto_eur_anno"],
                         -2295000.0)
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_spread_eur_mwh"])
        self.assertIsNone(bc["breakeven_premio_eur_mw_anno"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        # Fisica e prezzi restano calcolati anche nel
        # regime degenere (sono fisica e prezzi, non KPI
        # di ritorno).
        self.assertEqual(bc["mw_mw"], 50.0)
        self.assertEqual(bc["ore_anno"], 4000)

    def test_spread_negativo_obbligo_vs_opzione(self):
        # Con spread meno 5 l'obbligo perde anche lo
        # spread, l'opzione solo premio piu fee piu
        # gestione: la differenza e 1.000.000 EUR/anno.
        bc_obl = mh904_calcola(
            **_demo_kwargs(spread_medio_eur_mwh=-5.0))
        bc_opz = mh904_calcola(
            **_demo_kwargs(spread_medio_eur_mwh=-5.0,
                           tipo_ftr="opzione"))
        self.assertEqual(bc_obl["payoff_eur_mwh"], -5.0)
        self.assertEqual(bc_opz["payoff_eur_mwh"], 0.0)
        self.assertEqual(bc_obl["margine_netto_eur_anno"],
                         -3295000.0)
        self.assertEqual(bc_opz["margine_netto_eur_anno"],
                         -2295000.0)
        self.assertEqual(
            bc_opz["margine_netto_eur_anno"]
            - bc_obl["margine_netto_eur_anno"],
            1000000.0)
        self.assertEqual(bc_obl["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(bc_opz["verdetto"], "NON_CALCOLABILE")

    def test_spread_breakeven_marginale(self):
        # Allo spread di breakeven la VAN e zero,
        # la TIR e uguale al tasso e il verdetto e
        # MARGINALE (VAN zero compresa nel MARGINALE).
        be = demo_calcoli()["breakeven_spread_eur_mwh"]
        kw = _demo_kwargs(spread_medio_eur_mwh=be)
        bc = mh904_calcola(**kw)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               237396.40, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["breakeven_premio_eur_mw_anno"],
                               45000.00, places=2)

    def test_premio_breakeven_marginale(self):
        bp = demo_calcoli()["breakeven_premio_eur_mw_anno"]
        kw = _demo_kwargs(premio_eur_mw_anno=bp)
        bc = mh904_calcola(**kw)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               237396.40, places=2)
        self.assertAlmostEqual(bc["van"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir"], 6.00, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["breakeven_spread_eur_mwh"],
                               15.00, places=2)

    def test_durata_uno_e_dieci(self):
        bc = mh904_calcola(**_demo_kwargs(t_anni=1))
        self.assertAlmostEqual(bc["van"], -334905.66, places=2)
        self.assertAlmostEqual(bc["tir"], -29.50, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh904_calcola(**_demo_kwargs(t_anni=10))
        self.assertAlmostEqual(bc["van"], 4188861.37, places=2)
        self.assertAlmostEqual(bc["tir"], 70.15, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_dieci_tir_invariata(self):
        # La TIR non dipende dal tasso di
        # attualizzazione: con tasso 0,10 la TIR
        # resta 64,68 %, cambia solo la VAN.
        bc = mh904_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertAlmostEqual(bc["van"], 1672504.67, places=2)
        self.assertAlmostEqual(bc["tir"], 64.68, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tolleranza_zero_demo_resta_conveniente(self):
        # Con VAN positiva la tolleranza non decide
        # nulla: il demo resta CONVIENTE anche a
        # tolleranza zero.
        bc = mh904_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["van"], 1969716.47, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_mw_cento_e_ore_8760(self):
        bc = mh904_calcola(**_demo_kwargs(mw_mw=100.0))
        self.assertEqual(bc["mw_mw"], 100.0)
        self.assertEqual(bc["ricavo_eur_anno"], 6000000.0)
        self.assertAlmostEqual(bc["margine_netto_eur_anno"],
                               1430000.00, places=2)
        self.assertAlmostEqual(bc["van"], 5023680.21, places=2)
        self.assertAlmostEqual(bc["tir"], 141.25, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh904_calcola(**_demo_kwargs(ore_anno=8760))
        self.assertEqual(bc["ricavo_eur_anno"], 6570000.0)
        self.assertAlmostEqual(bc["van"], 17007855.18, places=2)
        self.assertAlmostEqual(bc["tir"], 427.40, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_ore_uno_non_calcolabile(self):
        bc = mh904_calcola(**_demo_kwargs(ore_anno=1))
        self.assertEqual(bc["ricavo_eur_anno"], 750.0)
        self.assertEqual(bc["margine_netto_eur_anno"],
                         -2294250.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_capex_zero_tir_non_definita_payback_uno(self):
        bc = mh904_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(bc["breakeven_spread_eur_mwh"],
                               11.47, places=2)
        self.assertAlmostEqual(
            bc["breakeven_premio_eur_mw_anno"],
            59100.00, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_100000_tir_non_definita(self):
        # Caso del brief originale: con CAPEX
        # 100.000 la VAN e 2.869.716,47 ma la TIR
        # e non definita (VAN positiva anche al
        # 500 per cento, nessun cambio di segno
        # nell'intervallo di bisezione).
        bc = mh904_calcola(**_demo_kwargs(capex_eur=100000.0))
        self.assertAlmostEqual(bc["van"], 2869716.47, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(mw_mw="50.0")
        self.assertRaises(ValueError, mh904_calcola, **kw)
        kw = _demo_kwargs(mw_mw=True)
        self.assertRaises(ValueError, mh904_calcola, **kw)
        val = mh904_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def904\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh904_demo().keys()), lette - set(mh904_demo().keys()))
        self.assertEqual(lette, set(mh904_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc904\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc904\["([^"]+)"\]', src))
        attese = set(mh904_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 903 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 904.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 904)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab904:"), 1)
        self.assertTrue(src.startswith("    # W909"))

    def test_ui_tab904_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab904:"), 1)
        self.assertIn("def mh904_demo(", src_h)
        self.assertIn("def mh904_calcola(", src_h)
        self.assertIn("tab904", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("FTR: il diritto finanziario di trasmissione copre la congestione?", src)
        self.assertIn("🔀📜 FTR: il diritto finanziario di trasmissione copre la congestione?", src)
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
        chiavi = re.findall(r'key="(st904_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st904_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 19)
        self.assertIn('key="st904_calcola"', src)
        self.assertIn('key="st904_csv"', src)
        self.assertIn('key="st904_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg904"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos904", src)

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
