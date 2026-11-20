"""Test nuova scheda CCfD: il prezzo CO2 garantito
sblocca la decarbonizzazione industriale?
Repo path: tests/test_w907_ccfd.py

Effetto ECONOMICO: un CCfD e un contratto con cui lo
Stato garantisce a un impianto industriale un prezzo
fisso per la CO2 evitata (strike price): se il prezzo
ETS sta sotto lo strike, lo Stato paga la differenza
per ogni tonnellata abbattuta; se sta sopra, l'impianto
rimborsa la differenza allo Stato (contratto a due
vie, payout anche negativo). Il beneficio annuo CON
CCfD e strike per CO2 abbattuta meno OPEX extra: e
GARANTITO, indipendente dal prezzo ETS. Il beneficio
annuo SENZA CCfD e prezzo ETS per CO2 abbattuta meno
OPEX extra: dipende dal prezzo ETS.
Payout CCfD = (strike meno prezzo ETS) per CO2
abbattuta. Costo CO2 evitato = prezzo ETS per CO2
abbattuta. Beneficio con CCfD = strike per CO2
abbattuta meno OPEX extra. Beneficio senza CCfD =
prezzo ETS per CO2 abbattuta meno OPEX extra.
Rendita = (1 meno (1 piu tasso) elevato a meno
durata) diviso tasso. Flussi con CCfD = [meno CAPEX,
beneficio garantito per gli anni 1..T]; flussi senza
CCfD analoghi. Breakeven strike = (CAPEX diviso
rendita piu OPEX extra) diviso CO2 abbattuta: il
prezzo che azzera la VAN con CCfD. Costo di
abbattimento livellato = breakeven strike. Valore del
derisking = VAN con CCfD meno VAN senza CCfD.
Demo: cementificio con cattura CO2. Emissioni
baseline 500.000 t/anno, CO2 abbattuta 400.000
t/anno (80 per cento), strike 120 EUR/t, prezzo ETS
85 EUR/t, CAPEX 250.000.000 EUR, OPEX extra
10.000.000 EUR/anno, durata 15 anni, tasso 0,05
(frazione), tolleranza 0,10 (frazione). Payout CCfD
= (120 meno 85) per 400.000 = 14.000.000 EUR/anno.
Costo CO2 evitato = 85 per 400.000 = 34.000.000
EUR/anno. Beneficio garantito = 120 per 400.000
meno 10.000.000 = 38.000.000 EUR/anno. Beneficio
senza CCfD = 85 per 400.000 meno 10.000.000 =
24.000.000 EUR/anno. Flussi con CCfD [meno
250.000.000, 38.000.000 per 15 anni]; cumulato anno
6 meno 22.000.000, anno 7 16.000.000, finale
320.000.000. Flussi senza CCfD [meno 250.000.000,
24.000.000 per 15 anni]; cumulato anno 10 meno
10.000.000, anno 11 14.000.000, finale 110.000.000.
VAN con CCfD = 144.427.005,45 EUR; VAN senza CCfD =
meno 888.207,08 EUR; TIR per bisezione su flussi con
intervallo da meno 0,9 a 5,0 (con CCfD 12,66 per
cento, senza CCfD 4,95 per cento); payback con CCfD
(primo anno con cumulato netto maggiore o uguale a
0) = 7; payback senza CCfD = 11; breakeven strike =
(CAPEX diviso rendita piu OPEX extra) diviso CO2
abbattuta = 85,21 EUR/t (prezzo che azzera la VAN
con CCfD, NON il prezzo che azzera il beneficio
annuo: quello sarebbe OPEX extra diviso CO2
abbattuta, cioe 25 EUR/t in demo); costo di
abbattimento livellato = 85,21 EUR/t; valore del
derisking = 145.315.212,53 EUR; CO2 evitata anno =
CO2 abbattuta = 400.000 t/anno (INFORMATIVA, mai nel
conto economico); CO2 evitata vita = 6.000.000 t.
Scenari: base VAN con 144.427.005,45, VAN senza meno
888.207,08, TIR con 12,66 per cento, TIR senza 4,95
per cento, payback con 7, payback senza 11,
CONVIENTE contro MARGINALE; ETS piu 30 per cento
(prezzo ETS 110,50) VAN con INVARIATA
144.427.005,45, VAN senza 104.984.304,91, TIR senza
10,70 per cento, payback senza 8, CONVIENTE contro
CONVIENTE; ETS meno 30 per cento (prezzo ETS 59,50)
VAN con INVARIATA 144.427.005,45, VAN senza meno
106.760.719,07, TIR senza meno 2,27 per cento,
payback senza non definito, CONVIENTE contro
NON_CONVIENTE; strike piu 10 per cento (strike 132)
VAN con 194.249.364,03, TIR con 15,02 per cento,
payback con 6, VAN senza meno 888.207,08, CONVIENTE
contro MARGINALE; abbattimento 80 per cento (CO2
abbattuta 320.000) VAN con 44.782.288,28, TIR con
7,54 per cento, payback con 9, VAN senza meno
71.469.881,74, TIR senza 0,40 per cento, payback
senza 15, CONVIENTE contro NON_CONVIENTE.
Confronto: payout 14.000.000 contro costo CO2
evitato 34.000.000, beneficio con 38.000.000 contro
beneficio senza 24.000.000, CAPEX 250.000.000, OPEX
extra 10.000.000, VAN con 144.427.005,45 contro VAN
senza meno 888.207,08, TIR con 12,66 per cento
contro TIR senza 4,95 per cento, payback con 7
contro payback senza 11, breakeven strike 85,21,
costo di abbattimento livellato 85,21, valore del
derisking 145.315.212,53, CO2 evitata 400.000
t/anno.
Tasso in FRAZIONE (0,05 = 5 per cento), usato
diretto, NON diviso per 100. Tolleranza in FRAZIONE
(0,10 = 10 per cento del CAPEX), usata diretta, NON
divisa per 100. Prezzi, strike e prezzo ETS restano
costanti per tutta la durata, SEMPLIFICAZIONE
DICHIARATA (prezzo ETS volatile, costi reali che si
muovono, abbattimento che oscilla anno per anno nel
mondo reale, qui valore medio costante); il payout e
a due vie senza tetto e senza pavimento.
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il beneficio garantito
e minore o uguale a 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV) oppure se un input e
degenere (emissioni baseline nulle o negative, CO2
abbattuta negativa o sopra le emissioni baseline,
strike negativo, prezzo ETS negativo, CAPEX
negativo, OPEX extra negativo, durata nulla o
negativa o non intera, tasso nullo o negativo o
maggiore o uguale a 1, tolleranza negativa o sopra
1); altrimenti CONVIENTE se VAN maggiore di 0,
MARGINALE se VAN minore o uguale a 0 e valore
assoluto della VAN minore o uguale a tolleranza per
CAPEX, NON_CONVIENTE altrimenti; il verdetto senza
CCfD usa la stessa regola sulla VAN senza CCfD.
Casi limite: strike 60 (clawback: payout meno
10.000.000, beneficio garantito 14.000.000, VAN con
meno 104.684.787,47, TIR meno 2,10 per cento,
payback non definito, NON_CONVIENTE; VAN senza meno
888.207,08, MARGINALE); prezzo ETS 120 uguale allo
strike (payout zero, benefici e VAN uguali);
prezzo ETS zero (VAN con invariata, VAN senza meno
353.796.580,38, TIR senza non definita, payback
senza non definito, NON_CONVIENTE); strike 25
(beneficio garantito zero, VAN None, NON_CALCOLABILE);
CO2 abbattuta zero (beneficio garantito meno
10.000.000, NON_CALCOLABILE); strike al breakeven
85,21 (VAN con circa zero, TIR 5,00 per cento,
payback 11, MARGINALE); durata 1 (VAN con meno
213.809.523,81, TIR meno 84,80 per cento, payback
non definito); durata 5 (VAN con meno
85.479.886,52, TIR meno 8,50 per cento,
NON_CONVIENTE); tasso 0,10 (VAN con 39.031.021,24,
TIR 12,66 per cento, payback 7, CONVIENTE; VAN
senza meno 67.454.091,85, NON_CONVIENTE); CAPEX
zero (VAN con 394.427.005,45, TIR non definita,
payback 1); OPEX extra zero (VAN con
248.223.585,83, TIR 17,49 per cento, payback 6);
abbattimento 50 per cento (VAN con meno
104.684.787,47, TIR meno 2,10 per cento,
NON_CONVIENTE); tolleranza zero (VAN senza meno
888.207,08 diventa NON_CONVIENTE: la tolleranza
decide il confine MARGINALE).
Distinzione esplicita: qui SOLO il CCfD con strike
garantito e payout a due vie (VAN sul BENEFICIO
GARANTITO con CAPEX e OPEX extra), NIENTE EU ETS
puro (li il prezzo CO2 e solo di mercato e il
beneficio dipende dal prezzo ETS: qui lo strike
garantisce il ricavo per tonnellata abbattuta),
NIENTE CCS da solo (li si valuta la cattura CO2
senza garanzia di prezzo: qui la cattura c'e ma il
conto e sul prezzo garantito), NIENTE sussidio a
fondo perduto (li il sostegno e un trasferimento
una tantum: qui il sostegno e un prezzo per
tonnellata per tutta la durata), NIENTE PPA o
contratto energia (li il prezzo fisso e
sull'energia: qui il prezzo fisso e sulla CO2
evitata).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w907_helpers import (
        demo_calcoli,
        mh902_annuity,
        mh902_beneficio_con,
        mh902_beneficio_senza,
        mh902_breakeven_strike,
        mh902_calcola,
        mh902_co2_evitata_anno,
        mh902_co2_evitata_vita,
        mh902_confronto,
        mh902_costo_co2_evitato,
        mh902_csv,
        mh902_demo,
        mh902_demo_calcoli,
        mh902_flussi,
        mh902_fraz,
        mh902_int_pos,
        mh902_nneg,
        mh902_num,
        mh902_payback,
        mh902_payout,
        mh902_pos,
        mh902_riga_anno,
        mh902_scenario,
        mh902_sensibilita,
        mh902_serie_annua,
        mh902_tasso,
        mh902_tir,
        mh902_valida,
        mh902_valore_derisking,
        mh902_van,
        mh902_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w907_helpers", os.path.join(_hf, "w907_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh902_annuity = _mod.mh902_annuity
    mh902_beneficio_con = _mod.mh902_beneficio_con
    mh902_beneficio_senza = _mod.mh902_beneficio_senza
    mh902_breakeven_strike = _mod.mh902_breakeven_strike
    mh902_calcola = _mod.mh902_calcola
    mh902_co2_evitata_anno = _mod.mh902_co2_evitata_anno
    mh902_co2_evitata_vita = _mod.mh902_co2_evitata_vita
    mh902_confronto = _mod.mh902_confronto
    mh902_costo_co2_evitato = _mod.mh902_costo_co2_evitato
    mh902_csv = _mod.mh902_csv
    mh902_demo = _mod.mh902_demo
    mh902_demo_calcoli = _mod.mh902_demo_calcoli
    mh902_flussi = _mod.mh902_flussi
    mh902_fraz = _mod.mh902_fraz
    mh902_int_pos = _mod.mh902_int_pos
    mh902_nneg = _mod.mh902_nneg
    mh902_num = _mod.mh902_num
    mh902_payback = _mod.mh902_payback
    mh902_payout = _mod.mh902_payout
    mh902_pos = _mod.mh902_pos
    mh902_riga_anno = _mod.mh902_riga_anno
    mh902_scenario = _mod.mh902_scenario
    mh902_sensibilita = _mod.mh902_sensibilita
    mh902_serie_annua = _mod.mh902_serie_annua
    mh902_tasso = _mod.mh902_tasso
    mh902_tir = _mod.mh902_tir
    mh902_valida = _mod.mh902_valida
    mh902_valore_derisking = _mod.mh902_valore_derisking
    mh902_van = _mod.mh902_van
    mh902_verdetto = _mod.mh902_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w907_helpers.py")
_UI_PATH = _risolvi("w907_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "1"
_VECCHIO_TAB = "tab90" + "1"
_VECCHIO_ST = "st90" + "1_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "payout_eur_anno": 14000000.0,
    "costo_co2_evitato_eur_anno": 34000000.0,
    "beneficio_con_eur_anno": 38000000.0,
    "beneficio_senza_eur_anno": 24000000.0,
    "breakeven_strike_eur_t": 85.21392975577771,
    "costo_abbattimento_livellato_eur_t": 85.21392975577771,
    "co2_evitata_t_anno": 400000.0,
    "co2_evitata_t_vita": 6000000.0,
    "van_con": 144427005.45086244,
    "van_senza": -888207.0836658347,
    "tir_con": 12.65589744912522,
    "tir_senza": 4.947391649132149,
    "payback_con": 7,
    "payback_senza": 11,
    "valore_derisking_eur": 145315212.5345283,
}

_DEMO_SCENARI = [
    {"nome": "Base", "strike_eur_t": 120.0,
     "p_ets_eur_t": 85.0, "co2_abbattuta_t_anno": 400000.0,
     "payout_eur_anno": 14000000.0,
     "costo_co2_evitato_eur_anno": 34000000.0,
     "beneficio_con_eur_anno": 38000000.0,
     "beneficio_senza_eur_anno": 24000000.0,
     "van_con": 144427005.45086244,
     "van_senza": -888207.0836658347,
     "tir_con": 12.65589744912522,
     "tir_senza": 4.947391649132149,
     "payback_con": 7, "payback_senza": 11,
     "verdetto_con": "CONVIENTE",
     "verdetto_senza": "MARGINALE",
     "valore_derisking_eur": 145315212.5345283,
     "breakeven_strike_eur_t": 85.21392975577771,
     "co2_evitata_t_anno": 400000.0},
    {"nome": "ETS piu 30 %", "strike_eur_t": 120.0,
     "p_ets_eur_t": 110.5, "co2_abbattuta_t_anno": 400000.0,
     "payout_eur_anno": 3800000.0,
     "costo_co2_evitato_eur_anno": 44200000.0,
     "beneficio_con_eur_anno": 38000000.0,
     "beneficio_senza_eur_anno": 34200000.0,
     "van_con": 144427005.45086244,
     "van_senza": 104984304.90577619,
     "tir_con": 12.65589744912522,
     "tir_senza": 10.703960135709057,
     "payback_con": 7, "payback_senza": 8,
     "verdetto_con": "CONVIENTE",
     "verdetto_senza": "CONVIENTE",
     "valore_derisking_eur": 39442700.54508625,
     "breakeven_strike_eur_t": 85.21392975577771,
     "co2_evitata_t_anno": 400000.0},
    {"nome": "ETS meno 30 %", "strike_eur_t": 120.0,
     "p_ets_eur_t": 59.5, "co2_abbattuta_t_anno": 400000.0,
     "payout_eur_anno": 24200000.0,
     "costo_co2_evitato_eur_anno": 23800000.0,
     "beneficio_con_eur_anno": 38000000.0,
     "beneficio_senza_eur_anno": 13800000.0,
     "van_con": 144427005.45086244,
     "van_senza": -106760719.07310785,
     "tir_con": 12.65589744912522,
     "tir_senza": -2.2715450704238025,
     "payback_con": 7, "payback_senza": None,
     "verdetto_con": "CONVIENTE",
     "verdetto_senza": "NON_CONVIENTE",
     "valore_derisking_eur": 251187724.5239703,
     "breakeven_strike_eur_t": 85.21392975577771,
     "co2_evitata_t_anno": 400000.0},
    {"nome": "Strike piu 10 %", "strike_eur_t": 132.0,
     "p_ets_eur_t": 85.0, "co2_abbattuta_t_anno": 400000.0,
     "payout_eur_anno": 18800000.0,
     "costo_co2_evitato_eur_anno": 34000000.0,
     "beneficio_con_eur_anno": 42800000.0,
     "beneficio_senza_eur_anno": 24000000.0,
     "van_con": 194249364.03412926,
     "van_senza": -888207.0836658347,
     "tir_con": 15.022102717801012,
     "tir_senza": 4.947391649132149,
     "payback_con": 6, "payback_senza": 11,
     "verdetto_con": "CONVIENTE",
     "verdetto_senza": "MARGINALE",
     "valore_derisking_eur": 195137571.1177951,
     "breakeven_strike_eur_t": 85.21392975577771,
     "co2_evitata_t_anno": 400000.0},
    {"nome": "Abbattimento 80 %", "strike_eur_t": 120.0,
     "p_ets_eur_t": 85.0, "co2_abbattuta_t_anno": 320000.0,
     "payout_eur_anno": 11200000.0,
     "costo_co2_evitato_eur_anno": 27200000.0,
     "beneficio_con_eur_anno": 28400000.0,
     "beneficio_senza_eur_anno": 17200000.0,
     "van_con": 44782288.28432876,
     "van_senza": -71469881.74329385,
     "tir_con": 7.544428599551322,
     "tir_senza": 0.3963420954767538,
     "payback_con": 9, "payback_senza": 15,
     "verdetto_con": "CONVIENTE",
     "verdetto_senza": "NON_CONVIENTE",
     "valore_derisking_eur": 116252170.02762261,
     "breakeven_strike_eur_t": 106.51741219472214,
     "co2_evitata_t_anno": 320000.0},
]

_DEMO_CONFRONTO = {
    "payout": 14000000.0,
    "costo_co2_evitato": 34000000.0,
    "beneficio_con": 38000000.0,
    "beneficio_senza": 24000000.0,
    "capex": 250000000.0,
    "opex_extra": 10000000.0,
    "van_con": 144427005.45086244,
    "van_senza": -888207.0836658347,
    "tir_con": 12.65589744912522,
    "tir_senza": 4.947391649132149,
    "payback_con": 7,
    "payback_senza": 11,
    "breakeven_strike": 85.21392975577771,
    "costo_abbattimento_livellato": 85.21392975577771,
    "valore_derisking": 145315212.5345283,
    "co2_evitata_t_anno": 400000.0,
    "co2_evitata_t_vita": 6000000.0,
}

_ORDINE_VALIDA = (
    "e0_t_anno", "co2_abbattuta_t_anno",
    "strike_eur_t", "p_ets_eur_t",
    "capex_eur", "opex_extra_eur_anno",
    "t_anni", "r_tasso", "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh902_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh902_num(3, "x"), 3.0)
        self.assertEqual(mh902_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh902_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh902_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh902_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh902_pos(0, "x")
        with self.assertRaises(ValueError):
            mh902_pos(-1, "x")
        self.assertEqual(mh902_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh902_fraz(0, "x"), 0.0)
        self.assertEqual(mh902_fraz(1, "x"), 1.0)
        self.assertEqual(mh902_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh902_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh902_fraz(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh902_int_pos(15, "x"), 15)
        self.assertEqual(mh902_int_pos(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh902_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh902_int_pos(5.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh902_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh902_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh902_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh902_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh902_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh902_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_payout_a_due_vie(self):
        self.assertEqual(
            mh902_payout(120.0, 85.0, 400000.0), 14000000.0)
        self.assertEqual(
            mh902_payout(120.0, 110.5, 400000.0), 3800000.0)
        self.assertEqual(
            mh902_payout(120.0, 59.5, 400000.0), 24200000.0)
        self.assertEqual(
            mh902_payout(132.0, 85.0, 400000.0), 18800000.0)
        # Clawback: prezzo ETS sopra lo strike, payout
        # negativo (rimborso allo Stato).
        self.assertEqual(
            mh902_payout(60.0, 85.0, 400000.0), -10000000.0)
        # Prezzo ETS uguale allo strike: payout zero.
        self.assertEqual(
            mh902_payout(120.0, 120.0, 400000.0), 0.0)
        self.assertEqual(
            mh902_payout(120.0, 85.0, 0.0), 0.0)
        self.assertEqual(
            mh902_payout(0.0, 0.0, 400000.0), 0.0)
        with self.assertRaises(ValueError):
            mh902_payout(-1.0, 85.0, 400000.0)
        with self.assertRaises(ValueError):
            mh902_payout(120.0, -1.0, 400000.0)
        with self.assertRaises(ValueError):
            mh902_payout(120.0, 85.0, -1.0)

    def test_costo_co2_evitato(self):
        self.assertEqual(
            mh902_costo_co2_evitato(85.0, 400000.0), 34000000.0)
        self.assertEqual(
            mh902_costo_co2_evitato(110.5, 400000.0), 44200000.0)
        self.assertEqual(
            mh902_costo_co2_evitato(59.5, 400000.0), 23800000.0)
        self.assertEqual(
            mh902_costo_co2_evitato(0.0, 400000.0), 0.0)
        self.assertEqual(
            mh902_costo_co2_evitato(85.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh902_costo_co2_evitato(-1.0, 400000.0)
        with self.assertRaises(ValueError):
            mh902_costo_co2_evitato(85.0, -1.0)

    def test_benefici_con_e_senza(self):
        self.assertEqual(
            mh902_beneficio_con(120.0, 400000.0, 10000000.0),
            38000000.0)
        self.assertEqual(
            mh902_beneficio_con(132.0, 400000.0, 10000000.0),
            42800000.0)
        self.assertEqual(
            mh902_beneficio_con(60.0, 400000.0, 10000000.0),
            14000000.0)
        self.assertEqual(
            mh902_beneficio_con(120.0, 320000.0, 10000000.0),
            28400000.0)
        self.assertEqual(
            mh902_beneficio_con(25.0, 400000.0, 10000000.0),
            0.0)
        self.assertEqual(
            mh902_beneficio_con(120.0, 400000.0, 0.0),
            48000000.0)
        self.assertEqual(
            mh902_beneficio_senza(85.0, 400000.0, 10000000.0),
            24000000.0)
        self.assertEqual(
            mh902_beneficio_senza(110.5, 400000.0, 10000000.0),
            34200000.0)
        self.assertEqual(
            mh902_beneficio_senza(59.5, 400000.0, 10000000.0),
            13800000.0)
        self.assertEqual(
            mh902_beneficio_senza(0.0, 400000.0, 10000000.0),
            -10000000.0)
        self.assertEqual(
            mh902_beneficio_senza(120.0, 400000.0, 10000000.0),
            38000000.0)
        with self.assertRaises(ValueError):
            mh902_beneficio_con(-1.0, 400000.0, 10000000.0)
        with self.assertRaises(ValueError):
            mh902_beneficio_con(120.0, -1.0, 10000000.0)
        with self.assertRaises(ValueError):
            mh902_beneficio_con(120.0, 400000.0, -1.0)
        with self.assertRaises(ValueError):
            mh902_beneficio_senza(-1.0, 400000.0, 10000000.0)

    def test_annuity(self):
        self.assertAlmostEqual(
            mh902_annuity(0.05, 15), 10.3796580381806, places=9)
        self.assertAlmostEqual(
            mh902_annuity(0.05, 1), 0.9523809523809523, places=9)
        self.assertAlmostEqual(
            mh902_annuity(0.10, 15), 7.606079506308659, places=9)
        self.assertAlmostEqual(
            mh902_annuity(0.05, 5), 4.329476670630823, places=9)
        with self.assertRaises(ValueError):
            mh902_annuity(0.0, 15)
        with self.assertRaises(ValueError):
            mh902_annuity(1.0, 15)
        with self.assertRaises(ValueError):
            mh902_annuity(0.05, 0)

    def test_riga_anno_flussi_uguali_benefici(self):
        riga = mh902_riga_anno(1, 38000000.0, 24000000.0, 400000.0)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["beneficio_con"], 38000000.0)
        self.assertEqual(riga["beneficio_senza"], 24000000.0)
        self.assertEqual(riga["flusso_con"], 38000000.0)
        self.assertEqual(riga["flusso_senza"], 24000000.0)
        self.assertEqual(riga["co2_evitata"], 400000.0)
        riga = mh902_riga_anno(15, 38000000.0, 24000000.0, 400000.0)
        self.assertEqual(riga["flusso_con"], 38000000.0)
        with self.assertRaises(ValueError):
            mh902_riga_anno(0, 38000000.0, 24000000.0, 400000.0)

    def test_serie_annua(self):
        serie = mh902_serie_annua(38000000.0, 24000000.0, 15,
                                  400000.0)
        self.assertEqual(len(serie), 15)
        self.assertTrue(all(r["flusso_con"] == 38000000.0
                            for r in serie))
        self.assertTrue(all(r["flusso_senza"] == 24000000.0
                            for r in serie))
        self.assertTrue(all(r["beneficio_con"] == 38000000.0
                            for r in serie))
        self.assertTrue(all(r["co2_evitata"] == 400000.0
                            for r in serie))
        serie = mh902_serie_annua(28400000.0, 17200000.0, 15,
                                  320000.0)
        self.assertEqual(serie[0]["flusso_con"], 28400000.0)
        with self.assertRaises(ValueError):
            mh902_serie_annua(38000000.0, 24000000.0, 0, 400000.0)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        flc = bc["flussi_con"]
        fls = bc["flussi_senza"]
        self.assertEqual(len(flc), 16)
        self.assertEqual(len(fls), 16)
        self.assertEqual(flc[0], -250000000.0)
        self.assertEqual(flc[1], 38000000.0)
        self.assertEqual(flc[15], 38000000.0)
        self.assertEqual(fls[0], -250000000.0)
        self.assertEqual(fls[1], 24000000.0)
        self.assertEqual(fls[15], 24000000.0)
        self.assertAlmostEqual(sum(flc), 320000000.00, places=2)
        self.assertAlmostEqual(sum(fls), 110000000.00, places=2)
        self.assertAlmostEqual(sum(flc[:7]), -22000000.00, places=2)
        self.assertAlmostEqual(sum(flc[:8]), 16000000.00, places=2)
        self.assertAlmostEqual(sum(fls[:11]), -10000000.00, places=2)
        self.assertAlmostEqual(sum(fls[:12]), 14000000.00, places=2)
        flc2 = mh902_flussi(bc["serie"], bc["capex_eur"], 15,
                            "flusso_con")
        fls2 = mh902_flussi(bc["serie"], bc["capex_eur"], 15,
                            "flusso_senza")
        self.assertEqual(flc2, flc)
        self.assertEqual(fls2, fls)
        self.assertAlmostEqual(mh902_van(flc, 0.05), bc["van_con"])
        self.assertAlmostEqual(mh902_van(fls, 0.05), bc["van_senza"])
        with self.assertRaises(ValueError):
            mh902_flussi(bc["serie"][:14], bc["capex_eur"], 15,
                         "flusso_con")
        with self.assertRaises(ValueError):
            mh902_flussi(bc["serie"], bc["capex_eur"], 15,
                         "flusso")
        with self.assertRaises(ValueError):
            mh902_flussi(bc["serie"], bc["capex_eur"], 15, "")

    def test_breakeven_strike(self):
        self.assertAlmostEqual(
            mh902_breakeven_strike(250000000.0, 0.05, 15,
                                   10000000.0, 400000.0),
            85.21, places=2)
        self.assertAlmostEqual(
            mh902_breakeven_strike(250000000.0, 0.05, 15,
                                   0.0, 400000.0),
            60.21, places=2)
        self.assertAlmostEqual(
            mh902_breakeven_strike(0.0, 0.05, 15,
                                   10000000.0, 400000.0),
            25.0, places=2)
        self.assertAlmostEqual(
            mh902_breakeven_strike(250000000.0, 0.05, 15,
                                   10000000.0, 320000.0),
            106.52, places=2)
        self.assertIsNone(
            mh902_breakeven_strike(250000000.0, 0.05, 15,
                                   10000000.0, 0.0))
        # Al breakeven la VAN con CCfD e zero, la TIR con
        # e uguale al tasso e il verdetto e MARGINALE.
        be = mh902_breakeven_strike(250000000.0, 0.05, 15,
                                    10000000.0, 400000.0)
        bc = mh902_calcola(
            **_demo_kwargs(strike_eur_t=be))
        self.assertAlmostEqual(bc["beneficio_con_eur_anno"],
                               24085571.90, places=2)
        self.assertAlmostEqual(bc["van_con"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir_con"], 5.00, places=2)
        self.assertEqual(bc["payback_con"], 11)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        with self.assertRaises(ValueError):
            mh902_breakeven_strike(250000000.0, 0.05, 15,
                                   10000000.0, -1.0)
        with self.assertRaises(ValueError):
            mh902_breakeven_strike(-1.0, 0.05, 15,
                                   10000000.0, 400000.0)

    def test_co2_evitata_informativa(self):
        self.assertEqual(
            mh902_co2_evitata_anno(400000.0), 400000.0)
        self.assertEqual(
            mh902_co2_evitata_anno(320000.0), 320000.0)
        self.assertEqual(
            mh902_co2_evitata_anno(0.0), 0.0)
        self.assertEqual(
            mh902_co2_evitata_vita(400000.0, 15), 6000000.0)
        self.assertEqual(
            mh902_co2_evitata_vita(400000.0, 5), 2000000.0)
        self.assertEqual(
            mh902_co2_evitata_vita(320000.0, 15), 4800000.0)
        with self.assertRaises(ValueError):
            mh902_co2_evitata_anno(-1.0)
        with self.assertRaises(ValueError):
            mh902_co2_evitata_vita(400000.0, 0)

    def test_valore_derisking(self):
        self.assertAlmostEqual(
            mh902_valore_derisking(144427005.45, -888207.08),
            145315212.53, places=2)
        self.assertAlmostEqual(
            mh902_valore_derisking(144427005.45, 104984304.91),
            39442700.54, places=2)
        self.assertEqual(
            mh902_valore_derisking(100.0, 100.0), 0.0)
        self.assertIsNone(mh902_valore_derisking(None, 100.0))
        self.assertIsNone(mh902_valore_derisking(100.0, None))
        self.assertIsNone(mh902_valore_derisking(None, None))

    def test_scenario_singolo(self):
        s = mh902_scenario("ETS piu 30 %", mh902_demo(),
                           {"p_ets_eur_t": 110.5})
        self.assertEqual(s["nome"], "ETS piu 30 %")
        self.assertEqual(s["p_ets_eur_t"], 110.5)
        # La VAN con CCfD e INVARIATA al prezzo ETS:
        # prova del derisking.
        self.assertAlmostEqual(s["van_con"], 144427005.45,
                               places=2)
        self.assertAlmostEqual(s["van_senza"], 104984304.91,
                               places=2)
        self.assertEqual(s["payback_con"], 7)
        self.assertEqual(s["payback_senza"], 8)
        self.assertEqual(s["verdetto_con"], "CONVIENTE")
        self.assertEqual(s["verdetto_senza"], "CONVIENTE")
        s = mh902_scenario("ETS meno 30 %", mh902_demo(),
                           {"p_ets_eur_t": 59.5})
        self.assertAlmostEqual(s["van_con"], 144427005.45,
                               places=2)
        self.assertAlmostEqual(s["van_senza"], -106760719.07,
                               places=2)
        self.assertIsNone(s["payback_senza"])
        self.assertEqual(s["verdetto_senza"], "NON_CONVIENTE")
        s = mh902_scenario("Strike piu 10 %", mh902_demo(),
                           {"strike_eur_t": 132.0})
        self.assertAlmostEqual(s["van_con"], 194249364.03,
                               places=2)
        self.assertEqual(s["payback_con"], 6)
        s = mh902_scenario("Abbattimento 80 %", mh902_demo(),
                           {"co2_abbattuta_t_anno": 320000.0})
        self.assertAlmostEqual(s["van_con"], 44782288.28,
                               places=2)
        self.assertAlmostEqual(
            s["breakeven_strike_eur_t"], 106.52, places=2)
        self.assertEqual(s["co2_evitata_t_anno"], 320000.0)
        with self.assertRaises(ValueError):
            mh902_scenario("", mh902_demo(),
                           {"p_ets_eur_t": 110.5})
        with self.assertRaises(ValueError):
            mh902_scenario("X", mh902_demo(),
                           {"co2_abbattuta_t_anno": 999999.0})

    def test_scenario_beneficio_nullo_non_calcolabile(self):
        s = mh902_scenario("Strike basso", mh902_demo(),
                           {"strike_eur_t": 25.0})
        self.assertIsNone(s["van_con"])
        self.assertIsNone(s["van_senza"])
        self.assertIsNone(s["tir_con"])
        self.assertIsNone(s["tir_senza"])
        self.assertIsNone(s["payback_con"])
        self.assertIsNone(s["payback_senza"])
        self.assertIsNone(s["breakeven_strike_eur_t"])
        self.assertIsNone(s["valore_derisking_eur"])
        self.assertEqual(s["verdetto_con"], "NON_CALCOLABILE")
        self.assertEqual(s["verdetto_senza"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh902_confronto(14000000.0, 34000000.0,
                            38000000.0, 24000000.0,
                            250000000.0, 10000000.0,
                            144427005.45, -888207.08,
                            12.66, 4.95, 7, 11,
                            85.21, 145315212.53,
                            400000.0, 6000000.0)
        self.assertEqual(c["payout"], 14000000.0)
        self.assertEqual(c["costo_co2_evitato"], 34000000.0)
        self.assertEqual(c["beneficio_con"], 38000000.0)
        self.assertEqual(c["beneficio_senza"], 24000000.0)
        self.assertEqual(c["capex"], 250000000.0)
        self.assertEqual(c["opex_extra"], 10000000.0)
        self.assertEqual(c["van_con"], 144427005.45)
        self.assertEqual(c["van_senza"], -888207.08)
        self.assertEqual(c["tir_con"], 12.66)
        self.assertEqual(c["tir_senza"], 4.95)
        self.assertEqual(c["payback_con"], 7)
        self.assertEqual(c["payback_senza"], 11)
        self.assertEqual(c["breakeven_strike"], 85.21)
        self.assertEqual(c["costo_abbattimento_livellato"], 85.21)
        self.assertEqual(c["valore_derisking"], 145315212.53)
        self.assertEqual(c["co2_evitata_t_anno"], 400000.0)
        self.assertEqual(c["co2_evitata_t_vita"], 6000000.0)
        c = mh902_confronto(0.0, 0.0, 0.0, -10000000.0,
                            250000000.0, 10000000.0,
                            0.0, 0.0, None, None, None, None,
                            None, None, 0.0, 0.0)
        self.assertIsNone(c["breakeven_strike"])
        self.assertIsNone(c["costo_abbattimento_livellato"])
        self.assertIsNone(c["valore_derisking"])
        self.assertIsNone(c["tir_con"])
        self.assertIsNone(c["tir_senza"])
        self.assertIsNone(c["payback_con"])
        self.assertIsNone(c["payback_senza"])
        with self.assertRaises(ValueError):
            mh902_confronto(14000000.0, -1.0,
                            38000000.0, 24000000.0,
                            250000000.0, 10000000.0,
                            144427005.45, -888207.08,
                            12.66, 4.95, 7, 11,
                            85.21, 145315212.53,
                            400000.0, 6000000.0)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_cinque(self):
        bc = mh902_demo_calcoli()
        self.assertAlmostEqual(
            mh902_van(bc["flussi_con"], 0.05),
            bc["van_con"])
        self.assertAlmostEqual(
            mh902_van(bc["flussi_senza"], 0.05),
            bc["van_senza"])
        bc_basso = mh902_calcola(
            _scenari=False,
            **dict(mh902_demo(), p_ets_eur_t=59.5))
        self.assertAlmostEqual(
            mh902_van(bc_basso["flussi_senza"], 0.05),
            bc["scenari"][2]["van_senza"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh902_van([-250000000, 38000000, 38000000], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 per cento):
        # usato diretto, NON diviso per 100. Con 0,05 la
        # VAN con demo e' 144427005,45; con 0,50 (cioe'
        # 50 per cento) sarebbe tutt'altra; con 5,0 il
        # tasso e' degenere (maggiore o uguale a 1) e
        # solleva ValueError.
        bc = mh902_demo_calcoli()
        self.assertAlmostEqual(
            mh902_van(bc["flussi_con"], 0.05),
            144427005.45, places=2)
        self.assertNotAlmostEqual(
            mh902_van(bc["flussi_con"], 0.50),
            144427005.45, places=2)
        with self.assertRaises(ValueError):
            mh902_van(bc["flussi_con"], 5.0)

    def test_tir_demo(self):
        bc = mh902_demo_calcoli()
        tir_c = mh902_tir(bc["flussi_con"])
        tir_s = mh902_tir(bc["flussi_senza"])
        self.assertIsNotNone(tir_c)
        self.assertIsNotNone(tir_s)
        self.assertAlmostEqual(tir_c * 100.0, bc["tir_con"],
                               places=6)
        self.assertAlmostEqual(tir_s * 100.0, bc["tir_senza"],
                               places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh902_tir([-100, -10, -10]))
        self.assertIsNone(mh902_tir([100, 10, 10]))
        self.assertIsNone(mh902_tir([0, 10, 10]))
        self.assertIsNone(mh902_tir([-250000000, -10000000,
                                     -10000000]))

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh902_demo_calcoli()
        self.assertEqual(mh902_payback(bc["flussi_con"]), 7)
        self.assertEqual(mh902_payback(bc["flussi_senza"]), 11)
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh902_payback([-100, 100, 10]), 1)
        self.assertEqual(mh902_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh902_payback([-100, 10, 10]))
        # Con CAPEX zero il payback e l'anno 1.
        self.assertEqual(mh902_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh902_demo_calcoli()
        fc = bc["flussi_con"]
        fs = bc["flussi_senza"]
        self.assertAlmostEqual(sum(fc[:7]), -22000000.00, places=2)
        self.assertAlmostEqual(sum(fc[:8]), 16000000.00, places=2)
        self.assertAlmostEqual(sum(fc), 320000000.00, places=2)
        self.assertAlmostEqual(sum(fs[:11]), -10000000.00, places=2)
        self.assertAlmostEqual(sum(fs[:12]), 14000000.00, places=2)
        self.assertAlmostEqual(sum(fs), 110000000.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(
            mh902_verdetto(100.0, 0.10, 250000000.0), "CONVIENTE")
        self.assertEqual(
            mh902_verdetto(0.0, 0.10, 250000000.0), "MARGINALE")
        self.assertEqual(
            mh902_verdetto(-25000000.0, 0.10, 250000000.0),
            "MARGINALE")
        self.assertEqual(
            mh902_verdetto(-25000001.0, 0.10, 250000000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh902_verdetto(-100000000.0, 0.10, 250000000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativa e
        # NON_CONVIENTE (VAN zero compresa nel MARGINALE
        # solo perche il valore assoluto zero e minore
        # o uguale a zero).
        self.assertEqual(
            mh902_verdetto(-1.0, 0.0, 250000000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh902_verdetto(0.0, 0.0, 250000000.0), "MARGINALE")
        with self.assertRaises(ValueError):
            mh902_verdetto(100.0, 1.5, 250000000.0)
        with self.assertRaises(ValueError):
            mh902_verdetto(100.0, 0.10, -1.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh902_verdetto(None, 0.10, 250000000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh902_verdetto(None, 0.0, 0.0), "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh902_demo()
        val = mh902_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_durata_zero_e_non_intera_no(self):
        kw = _demo_kwargs(t_anni=0)
        self.assertRaises(ValueError, mh902_calcola, **kw)
        kw = _demo_kwargs(t_anni=15.5)
        self.assertRaises(ValueError, mh902_calcola, **kw)
        kw = _demo_kwargs(t_anni=5)
        bc = mh902_calcola(**kw)
        self.assertEqual(bc["t_anni"], 5)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh902_calcola(**_demo_kwargs(r_tasso=tasso))
        bc = mh902_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertEqual(bc["r_tasso"], 0.10)

    def test_valida_abbattuta_sopra_baseline_no(self):
        with self.assertRaises(ValueError):
            mh902_calcola(
                **_demo_kwargs(co2_abbattuta_t_anno=500001.0))
        bc = mh902_calcola(
            **_demo_kwargs(co2_abbattuta_t_anno=500000.0))
        self.assertEqual(bc["co2_abbattuta_t_anno"], 500000.0)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh902_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh902_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("e0_t_anno", 0),
                              ("t_anni", 0),
                              ("r_tasso", 0)):
            with self.assertRaises(ValueError):
                mh902_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_ets_eur_t=float("nan"))
        self.assertRaises(ValueError, mh902_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh902_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e0_t_anno", -1),
                              ("co2_abbattuta_t_anno", -1),
                              ("strike_eur_t", -1),
                              ("p_ets_eur_t", -1),
                              ("capex_eur", -1),
                              ("opex_extra_eur_anno", -1),
                              ("t_anni", -1),
                              ("r_tasso", -0.01),
                              ("tol_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh902_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh902_calcola(mh902_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(bc["verdetto_senza"], "MARGINALE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh902_calcola(dict(mh902_demo(), p_ets_eur_t=999.0),
                           p_ets_eur_t=85.0)
        self.assertEqual(bc["p_ets_eur_t"], 85.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh902_calcola(_scenari=False, **mh902_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van_con"], 144427005.45,
                               places=2)
        self.assertAlmostEqual(bc["van_senza"], -888207.08,
                               places=2)


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
        self.assertEqual(bc["verdetto_con"], "CONVIENTE")
        self.assertEqual(bc["verdetto_senza"], "MARGINALE")
        self.assertEqual(bc["scenario_base"]["verdetto_con"],
                         "CONVIENTE")
        self.assertEqual(bc["scenario_base"]["verdetto_senza"],
                         "MARGINALE")
        self.assertGreater(bc["van_con"], 0.0)
        self.assertLess(bc["van_senza"], 0.0)
        self.assertEqual(bc["payback_con"], 7)
        self.assertEqual(bc["payback_senza"], 11)
        self.assertAlmostEqual(bc["tir_con"], 12.66, places=2)
        self.assertAlmostEqual(bc["tir_senza"], 4.95, places=2)
        self.assertAlmostEqual(bc["breakeven_strike_eur_t"],
                               85.21, places=2)
        self.assertAlmostEqual(
            bc["costo_abbattimento_livellato_eur_t"],
            bc["breakeven_strike_eur_t"])

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["payout_eur_anno"],
            (bc["strike_eur_t"] - bc["p_ets_eur_t"])
            * bc["co2_abbattuta_t_anno"])
        self.assertAlmostEqual(
            bc["costo_co2_evitato_eur_anno"],
            bc["p_ets_eur_t"] * bc["co2_abbattuta_t_anno"])
        self.assertAlmostEqual(
            bc["beneficio_con_eur_anno"],
            bc["strike_eur_t"] * bc["co2_abbattuta_t_anno"]
            - bc["opex_extra_eur_anno"])
        self.assertAlmostEqual(
            bc["beneficio_senza_eur_anno"],
            bc["p_ets_eur_t"] * bc["co2_abbattuta_t_anno"]
            - bc["opex_extra_eur_anno"])
        self.assertAlmostEqual(
            bc["valore_derisking_eur"],
            bc["van_con"] - bc["van_senza"])
        self.assertAlmostEqual(
            bc["breakeven_strike_eur_t"],
            (bc["capex_eur"]
             / mh902_annuity(bc["r_tasso"], bc["t_anni"])
             + bc["opex_extra_eur_anno"])
            / bc["co2_abbattuta_t_anno"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["co2_abbattuta_t_anno"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_vita"],
            bc["co2_evitata_t_anno"] * bc["t_anni"])
        self.assertAlmostEqual(
            bc["van_con"],
            mh902_van(bc["flussi_con"], bc["r_tasso"]))
        self.assertAlmostEqual(
            bc["van_senza"],
            mh902_van(bc["flussi_senza"], bc["r_tasso"]))
        for t in range(1, bc["t_anni"] + 1):
            riga = bc["serie"][t - 1]
            with self.subTest(anno=t):
                self.assertAlmostEqual(
                    riga["flusso_con"],
                    riga["beneficio_con"])
                self.assertAlmostEqual(
                    riga["flusso_senza"],
                    riga["beneficio_senza"])
        conf = bc["confronto"]
        self.assertEqual(conf["van_con"], bc["van_con"])
        self.assertEqual(conf["van_senza"], bc["van_senza"])
        self.assertEqual(conf["capex"], bc["capex_eur"])
        self.assertEqual(conf["tir_con"], bc["tir_con"])
        self.assertEqual(conf["tir_senza"], bc["tir_senza"])
        self.assertEqual(conf["payback_con"], bc["payback_con"])
        self.assertEqual(conf["payback_senza"],
                         bc["payback_senza"])

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # La VAN con CCfD e INVARIANTE al prezzo ETS:
        # gli scenari ETS muovono solo la VAN senza.
        self.assertEqual(bc["scenari"][1]["van_con"],
                         base["van_con"])
        self.assertEqual(bc["scenari"][2]["van_con"],
                         base["van_con"])
        self.assertEqual(bc["scenari"][1]["tir_con"],
                         base["tir_con"])
        self.assertEqual(bc["scenari"][2]["tir_con"],
                         base["tir_con"])
        self.assertEqual(bc["scenari"][1]["payback_con"], 7)
        self.assertEqual(bc["scenari"][2]["payback_con"], 7)
        self.assertGreater(bc["scenari"][1]["van_senza"],
                           base["van_senza"])
        self.assertGreater(bc["scenari"][1]["van_senza"], 0.0)
        self.assertEqual(bc["scenari"][1]["verdetto_senza"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][1]["payback_senza"], 8)
        self.assertLess(bc["scenari"][2]["van_senza"],
                        base["van_senza"])
        self.assertLess(bc["scenari"][2]["van_senza"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto_senza"],
                         "NON_CONVIENTE")
        self.assertIsNone(bc["scenari"][2]["payback_senza"])
        # Lo strike piu alto migliora solo la gamba con
        # CCfD; la VAN senza resta identica alla base.
        self.assertGreater(bc["scenari"][3]["van_con"],
                           base["van_con"])
        self.assertEqual(bc["scenari"][3]["van_senza"],
                         base["van_senza"])
        self.assertEqual(bc["scenari"][3]["payback_con"], 6)
        # Meno abbattimento peggiora entrambe le gambe.
        self.assertLess(bc["scenari"][4]["van_con"],
                        base["van_con"])
        self.assertLess(bc["scenari"][4]["van_senza"],
                        base["van_senza"])
        self.assertEqual(bc["scenari"][4]["payback_con"], 9)
        self.assertEqual(bc["scenari"][4]["payback_senza"], 15)
        self.assertEqual(bc["scenari"][4]["verdetto_senza"],
                         "NON_CONVIENTE")

    def test_sensibilita_valori(self):
        s = mh902_sensibilita(**mh902_demo())
        self.assertEqual(set(s.keys()),
                         {"ets_piu30", "ets_meno30",
                          "strike_piu10", "abb_080",
                          "capex_zero", "opex_zero",
                          "vita_005", "tasso_010", "strike_060",
                          "p_ets_120", "abb_050"})
        attesi = {
            "ets_piu30": (144427005.45, 12.66, 7,
                          104984304.91, 10.70, 8,
                          "CONVIENTE", "CONVIENTE"),
            "ets_meno30": (144427005.45, 12.66, 7,
                           -106760719.07, -2.27, None,
                           "CONVIENTE", "NON_CONVIENTE"),
            "strike_piu10": (194249364.03, 15.02, 6,
                             -888207.08, 4.95, 11,
                             "CONVIENTE", "MARGINALE"),
            "abb_080": (44782288.28, 7.54, 9,
                        -71469881.74, 0.40, 15,
                        "CONVIENTE", "NON_CONVIENTE"),
            "capex_zero": (394427005.45, None, 1,
                           249111792.92, None, 1,
                           "CONVIENTE", "CONVIENTE"),
            "opex_zero": (248223585.83, 17.49, 6,
                          102908373.30, 10.60, 8,
                          "CONVIENTE", "CONVIENTE"),
            "vita_005": (-85479886.52, -8.50, None,
                         -146092559.90, -20.35, None,
                         "NON_CONVIENTE", "NON_CONVIENTE"),
            "tasso_010": (39031021.24, 12.66, 7,
                          -67454091.85, 4.95, 11,
                          "CONVIENTE", "NON_CONVIENTE"),
            "strike_060": (-104684787.47, -2.10, None,
                           -888207.08, 4.95, 11,
                           "NON_CONVIENTE", "MARGINALE"),
            "p_ets_120": (144427005.45, 12.66, 7,
                          144427005.45, 12.66, 7,
                          "CONVIENTE", "CONVIENTE"),
            "abb_050": (-104684787.47, -2.10, None,
                        -177342393.73, -9.29, None,
                        "NON_CONVIENTE", "NON_CONVIENTE"),
        }
        for nome, (vc, tc, pbc, vs, ts, pbs, vdc,
                   vds) in attesi.items():
            with self.subTest(variante=nome):
                if vc is None:
                    self.assertIsNone(s[nome]["van_con"])
                else:
                    self.assertAlmostEqual(s[nome]["van_con"],
                                           vc, places=2)
                if tc is None:
                    self.assertIsNone(s[nome]["tir_con"])
                else:
                    self.assertAlmostEqual(s[nome]["tir_con"],
                                           tc, places=2)
                self.assertEqual(s[nome]["payback_con"], pbc)
                if vs is None:
                    self.assertIsNone(s[nome]["van_senza"])
                else:
                    self.assertAlmostEqual(s[nome]["van_senza"],
                                           vs, places=2)
                if ts is None:
                    self.assertIsNone(s[nome]["tir_senza"])
                else:
                    self.assertAlmostEqual(s[nome]["tir_senza"],
                                           ts, places=2)
                self.assertEqual(s[nome]["payback_senza"], pbs)
                self.assertEqual(s[nome]["verdetto"], vdc)
                self.assertEqual(s[nome]["verdetto_senza"], vds)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van_con", caso)
            self.assertIn("van_senza", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh902_csv(bc, mh902_demo())
        for voce in ("e0_t_anno", "co2_abbattuta_t_anno",
                     "strike_eur_t", "p_ets_eur_t",
                     "capex_eur", "opex_extra_eur_anno",
                     "t_anni", "r_tasso",
                     "tol_frazione",
                     "payout_eur_anno",
                     "costo_co2_evitato_eur_anno",
                     "beneficio_con_eur_anno",
                     "beneficio_senza_eur_anno",
                     "breakeven_strike_eur_t",
                     "costo_abbattimento_livellato_eur_t",
                     "co2_evitata_t_anno", "co2_evitata_t_vita",
                     "van_con", "van_senza",
                     "tir_con", "tir_senza",
                     "payback_con", "payback_senza",
                     "valore_derisking_eur",
                     "scenario_base_van_con",
                     "scenario_base_van_senza",
                     "scenario_base_tir_con",
                     "scenario_base_verdetto_con",
                     "scenario_base_verdetto_senza",
                     "scenario_ets_piu30_van_con",
                     "scenario_ets_piu30_van_senza",
                     "scenario_ets_piu30_verdetto_senza",
                     "scenario_ets_meno30_van_con",
                     "scenario_ets_meno30_van_senza",
                     "scenario_ets_meno30_verdetto_senza",
                     "scenario_strike_piu10_van_con",
                     "scenario_strike_piu10_verdetto_con",
                     "scenario_abbattimento_080_van_con",
                     "scenario_abbattimento_080_verdetto_senza",
                     "anno_1_payout",
                     "anno_1_beneficio_con",
                     "anno_1_beneficio_senza",
                     "anno_1_flusso_con",
                     "anno_1_flusso_senza",
                     "anno_1_co2_evitata",
                     "anno_15_beneficio_con",
                     "anno_15_flusso_con",
                     "anno_15_flusso_senza",
                     "confronto_payout",
                     "confronto_costo_co2_evitato",
                     "confronto_beneficio_con",
                     "confronto_beneficio_senza",
                     "confronto_capex", "confronto_opex_extra",
                     "confronto_van_con", "confronto_van_senza",
                     "confronto_tir_con", "confronto_tir_senza",
                     "confronto_payback_con",
                     "confronto_payback_senza",
                     "confronto_breakeven_strike",
                     "confronto_costo_abbattimento_livellato",
                     "confronto_valore_derisking",
                     "confronto_co2_evitata_t_anno",
                     "confronto_co2_evitata_t_vita",
                     "verdetto", "verdetto_senza"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)
        self.assertIn("MARGINALE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh902_csv(bc, mh902_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e0_t_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh902_demo_calcoli()["van_con"],
                         demo_calcoli()["van_con"])
        self.assertEqual(mh902_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 15)
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 17)
        self.assertEqual(len(bc["df_tabella"]), 26)
        self.assertEqual(len(bc["df_benefici"]), 2)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso con CCfD (EUR)"].iloc[0],
            38000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso senza CCfD (EUR)"].iloc[0],
            24000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato con CCfD (EUR)"].iloc[5],
            -22000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato con CCfD (EUR)"].iloc[6],
            16000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato con CCfD (EUR)"].iloc[-1],
            320000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato senza CCfD (EUR)"].iloc[9],
            -10000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato senza CCfD (EUR)"].iloc[10],
            14000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato senza CCfD (EUR)"].iloc[-1],
            110000000.00, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Payout CCfD (EUR/anno)",
             "Costo CO2 evitato (EUR/anno)",
             "Beneficio con CCfD (EUR/anno)",
             "Beneficio senza CCfD (EUR/anno)",
             "CAPEX (EUR)",
             "OPEX extra (EUR/anno)",
             "VAN con CCfD (EUR)",
             "VAN senza CCfD (EUR)",
             "TIR con CCfD (%)",
             "TIR senza CCfD (%)",
             "Payback con CCfD (anni)",
             "Payback senza CCfD (anni)",
             "Breakeven strike (EUR/t)",
             "Costo abbattimento livellato (EUR/t)",
             "Valore derisking (EUR)",
             "CO2 evitata (t/anno)",
             "CO2 evitata vita (t)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            14000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[2],
            38000000.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Emissioni baseline (t/anno)", voci)
        self.assertIn("CO2 abbattuta (t/anno)", voci)
        self.assertIn("Strike (EUR/t)", voci)
        self.assertIn("Prezzo ETS (EUR/t)", voci)
        self.assertIn("Breakeven strike (EUR/t)", voci)
        self.assertIn("Costo abbattimento livellato (EUR/t)", voci)
        self.assertIn("CO2 evitata vita (t)", voci)
        self.assertIn("Verdetto con CCfD", voci)
        self.assertIn("Verdetto senza CCfD", voci)
        self.assertIn("VAN con CCfD (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("VAN senza CCfD (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto con CCfD",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto senza CCfD",
                      set(bc["df_scenari"].columns))
        self.assertEqual(
            list(bc["df_benefici"]["Voce"]),
            ["Beneficio con CCfD", "Beneficio senza CCfD"])
        self.assertAlmostEqual(
            bc["df_benefici"]["Beneficio (EUR/anno)"].iloc[0],
            38000000.00, places=2)
        self.assertAlmostEqual(
            bc["df_benefici"]["Beneficio (EUR/anno)"].iloc[1],
            24000000.00, places=2)

    def test_zero_ammessi(self):
        bc = mh902_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["van_con"], 394427005.45,
                               places=2)
        self.assertIsNone(bc["tir_con"])
        self.assertEqual(bc["payback_con"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh902_calcola(**_demo_kwargs(opex_extra_eur_anno=0.0))
        self.assertEqual(bc["opex_extra_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van_con"], 248223585.83,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh902_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        self.assertAlmostEqual(bc["van_con"], 144427005.45,
                               places=2)
        bc = mh902_calcola(**_demo_kwargs(p_ets_eur_t=0.0))
        self.assertEqual(bc["p_ets_eur_t"], 0.0)
        self.assertAlmostEqual(bc["van_con"], 144427005.45,
                               places=2)
        self.assertAlmostEqual(bc["van_senza"], -353796580.38,
                               places=2)
        self.assertIsNone(bc["tir_senza"])
        self.assertIsNone(bc["payback_senza"])
        self.assertEqual(bc["verdetto_senza"], "NON_CONVIENTE")
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_strike_25_beneficio_zero_non_calcolabile(self):
        kw = _demo_kwargs(strike_eur_t=25.0)
        bc = mh902_calcola(**kw)
        self.assertEqual(bc["beneficio_con_eur_anno"], 0.0)
        self.assertTrue(all(r["beneficio_con"] <= 0.0
                            for r in bc["serie"]))
        self.assertIsNone(bc["van_con"])
        self.assertIsNone(bc["van_senza"])
        self.assertIsNone(bc["tir_con"])
        self.assertIsNone(bc["tir_senza"])
        self.assertIsNone(bc["payback_con"])
        self.assertIsNone(bc["payback_senza"])
        self.assertIsNone(bc["breakeven_strike_eur_t"])
        self.assertIsNone(bc["valore_derisking_eur"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(bc["verdetto_senza"], "NON_CALCOLABILE")
        # Payout e benefici restano calcolati anche nel
        # regime degenere (sono fisica e prezzi, non KPI
        # di ritorno).
        self.assertEqual(bc["payout_eur_anno"], -24000000.0)
        self.assertEqual(bc["beneficio_senza_eur_anno"],
                         24000000.0)

    def test_strike_24_beneficio_negativo_non_calcolabile(self):
        kw = _demo_kwargs(strike_eur_t=24.0)
        bc = mh902_calcola(**kw)
        self.assertEqual(bc["beneficio_con_eur_anno"], -400000.0)
        self.assertIsNone(bc["van_con"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_abbattuta_zero_non_calcolabile(self):
        kw = _demo_kwargs(co2_abbattuta_t_anno=0.0)
        bc = mh902_calcola(**kw)
        self.assertEqual(bc["beneficio_con_eur_anno"],
                         -10000000.0)
        self.assertEqual(bc["beneficio_senza_eur_anno"],
                         -10000000.0)
        self.assertEqual(bc["payout_eur_anno"], 0.0)
        self.assertEqual(bc["co2_evitata_t_anno"], 0.0)
        self.assertEqual(bc["co2_evitata_t_vita"], 0.0)
        self.assertIsNone(bc["breakeven_strike_eur_t"])
        self.assertIsNone(bc["van_con"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_strike_60_clawback_non_conveniente(self):
        # Clawback: prezzo ETS sopra lo strike, payout
        # negativo (rimborso allo Stato); il beneficio
        # garantito resta positivo ma basso.
        bc = mh902_calcola(**_demo_kwargs(strike_eur_t=60.0))
        self.assertEqual(bc["payout_eur_anno"], -10000000.0)
        self.assertEqual(bc["beneficio_con_eur_anno"],
                         14000000.0)
        self.assertAlmostEqual(bc["van_con"], -104684787.47,
                               places=2)
        self.assertAlmostEqual(bc["tir_con"], -2.10, places=2)
        self.assertIsNone(bc["payback_con"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van_senza"], -888207.08,
                               places=2)
        self.assertEqual(bc["verdetto_senza"], "MARGINALE")

    def test_prezzo_ets_uguale_strike_payout_zero(self):
        # Con prezzo ETS uguale allo strike il payout e
        # zero e le due gambe coincidono.
        bc = mh902_calcola(**_demo_kwargs(p_ets_eur_t=120.0))
        self.assertEqual(bc["payout_eur_anno"], 0.0)
        self.assertEqual(bc["beneficio_con_eur_anno"],
                         bc["beneficio_senza_eur_anno"])
        self.assertEqual(bc["van_con"], bc["van_senza"])
        self.assertEqual(bc["tir_con"], bc["tir_senza"])
        self.assertEqual(bc["payback_con"], bc["payback_senza"])
        self.assertAlmostEqual(bc["van_con"], 144427005.45,
                               places=2)

    def test_prezzo_ets_zero_conveniente(self):
        # Con prezzo ETS zero il beneficio garantito resta
        # positivo (lo strike lo garantisce) mentre il
        # beneficio senza CCfD va in negativo.
        bc = mh902_calcola(**_demo_kwargs(p_ets_eur_t=0.0))
        self.assertEqual(bc["payout_eur_anno"], 48000000.0)
        self.assertEqual(bc["costo_co2_evitato_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van_con"], 144427005.45,
                               places=2)
        self.assertAlmostEqual(bc["van_senza"], -353796580.38,
                               places=2)
        self.assertIsNone(bc["tir_senza"])
        self.assertIsNone(bc["payback_senza"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(bc["verdetto_senza"], "NON_CONVIENTE")

    def test_strike_breakeven_marginale(self):
        # Allo strike di breakeven la VAN con CCfD e zero,
        # la TIR con e uguale al tasso e il verdetto e
        # MARGINALE (VAN zero compresa nel MARGINALE).
        be = demo_calcoli()["breakeven_strike_eur_t"]
        kw = _demo_kwargs(strike_eur_t=be)
        bc = mh902_calcola(**kw)
        self.assertAlmostEqual(bc["beneficio_con_eur_anno"],
                               24085571.90, places=2)
        self.assertAlmostEqual(bc["van_con"], 0.0, places=2)
        self.assertAlmostEqual(bc["tir_con"], 5.00, places=2)
        self.assertEqual(bc["payback_con"], 11)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_durata_uno_non_conveniente(self):
        bc = mh902_calcola(**_demo_kwargs(t_anni=1))
        self.assertAlmostEqual(bc["van_con"], -213809523.81,
                               places=2)
        self.assertAlmostEqual(bc["tir_con"], -84.80, places=2)
        self.assertIsNone(bc["payback_con"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(bc["tir_senza"])
        self.assertIsNone(bc["payback_senza"])

    def test_durata_cinque_e_tasso_dieci(self):
        bc = mh902_calcola(**_demo_kwargs(t_anni=5))
        self.assertAlmostEqual(bc["van_con"], -85479886.52,
                               places=2)
        self.assertAlmostEqual(bc["tir_con"], -8.50, places=2)
        self.assertIsNone(bc["payback_con"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh902_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertAlmostEqual(bc["van_con"], 39031021.24,
                               places=2)
        self.assertAlmostEqual(bc["tir_con"], 12.66, places=2)
        self.assertEqual(bc["payback_con"], 7)
        self.assertAlmostEqual(bc["van_senza"], -67454091.85,
                               places=2)
        self.assertEqual(bc["verdetto_senza"], "NON_CONVIENTE")

    def test_tolleranza_zero_senza_non_conveniente(self):
        # Stessa VAN senza meno 888.207,08 del MARGINALE
        # demo, ma con tolleranza zero il confine si
        # sposta: ogni VAN negativa diventa NON_CONVIENTE.
        bc = mh902_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["van_senza"], -888207.08,
                               places=2)
        self.assertAlmostEqual(bc["tir_senza"], 4.95, places=2)
        self.assertEqual(bc["payback_senza"], 11)
        self.assertEqual(bc["verdetto_senza"], "NON_CONVIENTE")
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_abbattuta_totale_conveniente(self):
        bc = mh902_calcola(
            **_demo_kwargs(co2_abbattuta_t_anno=500000.0))
        self.assertAlmostEqual(bc["beneficio_con_eur_anno"],
                               50000000.00, places=2)
        self.assertAlmostEqual(bc["van_con"], 268982901.91,
                               places=2)
        self.assertAlmostEqual(bc["tir_con"], 18.42, places=2)
        self.assertEqual(bc["payback_con"], 5)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van_senza"], 87338886.24,
                               places=2)
        self.assertAlmostEqual(bc["tir_senza"], 9.80, places=2)
        self.assertEqual(bc["payback_senza"], 8)

    def test_abbattuta_meta_non_conveniente(self):
        bc = mh902_calcola(
            **_demo_kwargs(co2_abbattuta_t_anno=200000.0))
        self.assertAlmostEqual(bc["beneficio_con_eur_anno"],
                               14000000.00, places=2)
        self.assertAlmostEqual(bc["van_con"], -104684787.47,
                               places=2)
        self.assertAlmostEqual(bc["tir_con"], -2.10, places=2)
        self.assertIsNone(bc["payback_con"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_uno(self):
        bc = mh902_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir_con"])
        self.assertIsNone(bc["tir_senza"])
        self.assertEqual(bc["payback_con"], 1)
        self.assertEqual(bc["payback_senza"], 1)
        self.assertAlmostEqual(bc["breakeven_strike_eur_t"],
                               25.00, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(e0_t_anno="500000.0")
        self.assertRaises(ValueError, mh902_calcola, **kw)
        kw = _demo_kwargs(e0_t_anno=True)
        self.assertRaises(ValueError, mh902_calcola, **kw)
        val = mh902_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def902\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh902_demo().keys()), lette - set(mh902_demo().keys()))
        self.assertEqual(lette, set(mh902_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc902\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc902\["([^"]+)"\]', src))
        attese = set(mh902_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 901 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 902.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 903)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab902:"), 1)
        self.assertTrue(src.startswith("    # W907"))

    def test_ui_tab902_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab902:"), 1)
        self.assertIn("def mh902_demo(", src_h)
        self.assertIn("def mh902_calcola(", src_h)
        self.assertIn("tab902", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("CCfD (Carbon Contract for Difference): il prezzo CO2 garantito sblocca la decarbonizzazione industriale?", src)
        self.assertIn("📜💶 CCfD (Carbon Contract for Difference): il prezzo CO2 garantito sblocca la decarbonizzazione industriale?", src)
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
        chiavi = re.findall(r'key="(st902_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st902_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 15)
        self.assertIn('key="st902_calcola"', src)
        self.assertIn('key="st902_csv"', src)
        self.assertIn('key="st902_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg902"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos902", src)

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
