"""Test nuova scheda PPA fisico: l'energia rinnovabile
ritirata davvero a prezzo fisso paga?
Repo path: tests/test_w906_ppa_fisico.py

Effetto ECONOMICO: un PPA fisico e un contratto di lungo
periodo in cui il consumatore RITIRA davvero l'energia
rinnovabile del produttore: una quota del consumo e
coperta a prezzo fisso, il resto si compra dal fornitore
al prezzo di fornitura. L'energia PPA segue un profilo:
solo la parte che coincide in tempo col consumo (matching
orario) evita l'acquisto dal fornitore; la parte non
matchata (eccesso) viene venduta sul mercato al prezzo di
mercato e paga il costo di sbilanciamento.
Energia matchata = energia PPA per matching.
Eccesso = energia PPA meno matchata.
Energia residua = energia consumata meno matchata.
Costo PPA energia = energia PPA per prezzo fisso.
Sbilanciamento = eccesso per costo sbilanciamento.
Costo con PPA = costo PPA energia piu energia residua
per prezzo di fornitura meno eccesso per prezzo di
mercato piu sbilanciamento piu gestione annua (gestione
DENTRO: il risparmio e gia netto, il flusso annuo e il
risparmio, NON risparmio meno gestione).
Costo merchant = energia consumata per prezzo di
fornitura. Risparmio = costo merchant meno costo con
PPA. Prezzo medio = costo con PPA diviso energia
consumata. Prezzo coperto = (costo PPA energia piu
sbilanciamento) diviso energia PPA.
Demo: energia consumata 20.000 MWh/anno, energia PPA
12.000 MWh/anno, matching 0,75, prezzo fisso 65
EUR/MWh, prezzo di mercato 85 EUR/MWh, prezzo di
fornitura 90 EUR/MWh, costo iniziale 250.000 EUR,
costo annuo 5.000 EUR/anno, costo sbilanciamento 3
EUR/MWh, durata 10 anni, tasso 0,05 (frazione),
tolleranza 0,10 (frazione), fattore CO2 di rete
0,25 t/MWh. Energia matchata = 12.000 per 0,75 =
9.000 MWh/anno. Eccesso = 12.000 meno 9.000 = 3.000
MWh/anno. Energia residua = 20.000 meno 9.000 =
11.000 MWh/anno. Costo PPA energia = 12.000 per 65 =
780.000 EUR/anno. Sbilanciamento = 3.000 per 3 =
9.000 EUR/anno. Costo con PPA = 780.000 piu 11.000
per 90 meno 3.000 per 85 piu 9.000 piu 5.000 =
1.529.000 EUR/anno. Costo merchant = 20.000 per 90 =
1.800.000 EUR/anno. Risparmio = 1.800.000 meno
1.529.000 = 271.000 EUR/anno, GIA NETTO di gestione.
Prezzo medio = 1.529.000 diviso 20.000 = 76,45
EUR/MWh. Prezzo coperto = (780.000 piu 9.000) diviso
12.000 = 65,75 EUR/MWh. Flussi [meno 250.000,
271.000 per 10 anni]; cumulato anno 1 21.000, anno 2
292.000, finale 2.460.000.
VAN = 1.842.590,17 EUR; TIR per bisezione su flussi con
intervallo da meno 0,9 a 5,0 (108,33 %); payback (primo
anno con cumulato netto maggiore o uguale a 0) = 1;
breakeven prezzo PPA = (costo merchant meno energia
residua per prezzo di fornitura piu eccesso per prezzo
di mercato meno sbilanciamento meno gestione) diviso
energia PPA = 87,58 EUR/MWh (pareggio annuo, NON il
prezzo che azzera la VAN: a 87,58 il flusso annuo e
zero e la VAN resta meno 250.000, pari al costo
iniziale). CO2 evitata anno = energia PPA per fattore
di rete = 3.000 t/anno (INFORMATIVA, mai nel conto
economico); CO2 evitata vita = 30.000 t.
Scenari: base VAN 1.842.590,17, TIR 108,33 %, payback 1,
CONVIENTE; mercato piu 20 % (mercato e fornitura piu
20 %) VAN 3.487.319,71, TIR 193,60 %, payback 1,
CONVIENTE; mercato meno 20 % (mercato e fornitura meno
20 %) VAN 197.860,63, TIR 19,19 %, payback 5,
CONVIENTE; matching 0,60 VAN 1.731.397,18, TIR 102,55 %,
payback 1, CONVIENTE; prezzo PPA piu 10 % VAN
1.240.294,84, TIR 76,94 %, payback 2, CONVIENTE.
Confronto: costo merchant 1.800.000 contro costo con
PPA 1.529.000, risparmio 271.000, matchata 9.000,
eccesso 3.000, residua 11.000, prezzo medio 76,45,
prezzo coperto 65,75, costo iniziale 250.000, VAN
1.842.590,17, CO2 evitata 3.000 t/anno.
Tasso in FRAZIONE (0,05 = 5 %), usato diretto, NON
diviso per 100. Tolleranza in FRAZIONE (0,10 = 10 %
del costo iniziale), usata diretta, NON divisa per 100.
Matching in FRAZIONE (0,75 = 75 %), usato diretto, NON
diviso per 100. Prezzi, matching e fattori restano
costanti per tutta la durata, SEMPLIFICAZIONE
DICHIARATA (prezzo di mercato volatile, profilo
rinnovabile che oscilla anno per anno, matching che
si muove, costi di gestione reali variano nel mondo
reale, qui valore medio costante); la gestione annua
e DENTRO il costo con PPA, quindi il flusso annuo e
il risparmio: sottrarla di nuovo sarebbe un doppio
conteggio.
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il risparmio e minore o
uguale a 0 (guard degenere: UI salta KPI, grafico,
tabella e CSV) oppure se un input e degenere (energia
consumata nulla o negativa, energia PPA negativa o
sopra l'energia consumata, matching negativo o sopra
1, prezzo fisso negativo, prezzo di mercato negativo,
prezzo di fornitura negativo, costo iniziale negativo,
costo annuo negativo, costo sbilanciamento negativo,
durata nulla o negativa o non intera, tasso nullo o
negativo o maggiore o uguale a 1, tolleranza negativa
o sopra 1, fattore CO2 negativo); altrimenti CONVIENTE
se VAN maggiore di 0, MARGINALE se VAN minore o
uguale a 0 e valore assoluto della VAN minore o
uguale a tolleranza per costo iniziale, NON_CONVIENTE
altrimenti.
Casi limite: prezzo fisso 90 (risparmio meno 29.000,
VAN None, NON_CALCOLABILE); prezzo fisso al
breakeven 87,58 (risparmio zero, VAN None,
NON_CALCOLABILE); energia PPA zero (risparmio meno
5.000, NON_CALCOLABILE); prezzo fisso 85 (VAN meno
10.626,22, MARGINALE; con tolleranza zero
NON_CONVIENTE: la tolleranza decide il confine
MARGINALE); matching 0 (VAN 1.286.625,25, TIR 79,37 %,
payback 2, CONVIENTE: il prezzo fisso e sotto il
prezzo di mercato, quindi il PPA resta conveniente
come pura vendita a mercato); matching 1,0 (VAN
2.027.911,80, TIR 117,95 %, payback 1); energia PPA
20.000 (VAN 3.263.389,39, TIR 181,99 %, payback 1);
costo iniziale zero (VAN 2.092.590,17, TIR non
definita, payback 1); costo annuo zero (VAN
1.881.198,84, TIR 110,33 %, payback 1); durata 5
(VAN 923.288,18, TIR 105,44 %, payback 1); tasso 0,10
(VAN 1.415.177,69, TIR 108,33 %, payback 1); prezzo
di mercato 65 (VAN 1.379.286,07, TIR 84,21 %, payback
2, CONVIENTE: qui il prezzo di mercato tocca solo
la vendita dell'eccesso).
Distinzione esplicita: qui SOLO il PPA fisico con
ritiro dell'energia e matching orario (VAN sul
RISPARMIO da ritiro fisico con costo iniziale di
setup e garanzia), NIENTE VPPA (li il settlement e
finanziario senza ritiro: qui l'energia si ritira e
si vende l'eccesso a mercato con sbilanciamento),
NIENTE PPA on site (li l'energia e locale dietro
contatore: qui l'energia arriva da rete con profilo
e matching), NIENTE merchant puro (li tutto il
consumo si compra a prezzo di fornitura: qui la
quota PPA e a prezzo fisso), NIENTE acquisto di
energia verde con certificati (li il costo e un
premio sulle garanzie di origine: qui un contratto
di fornitura fisica di lungo periodo).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w906_helpers import (
        demo_calcoli,
        mh901_breakeven_p_ppa,
        mh901_calcola,
        mh901_confronto,
        mh901_co2_evitata_anno,
        mh901_co2_evitata_vita,
        mh901_costo_merchant,
        mh901_costo_ppa,
        mh901_costo_ppa_energia,
        mh901_csv,
        mh901_demo,
        mh901_demo_calcoli,
        mh901_eccesso,
        mh901_flussi,
        mh901_fraz,
        mh901_int_pos,
        mh901_matchata,
        mh901_nneg,
        mh901_num,
        mh901_payback,
        mh901_pos,
        mh901_prezzo_coperto,
        mh901_prezzo_medio,
        mh901_residua,
        mh901_riga_anno,
        mh901_risparmio,
        mh901_sbilanciamento,
        mh901_scenario,
        mh901_sensibilita,
        mh901_serie_annua,
        mh901_tasso,
        mh901_tir,
        mh901_valida,
        mh901_van,
        mh901_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w906_helpers", os.path.join(_hf, "w906_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh901_breakeven_p_ppa = _mod.mh901_breakeven_p_ppa
    mh901_calcola = _mod.mh901_calcola
    mh901_confronto = _mod.mh901_confronto
    mh901_co2_evitata_anno = _mod.mh901_co2_evitata_anno
    mh901_co2_evitata_vita = _mod.mh901_co2_evitata_vita
    mh901_costo_merchant = _mod.mh901_costo_merchant
    mh901_costo_ppa = _mod.mh901_costo_ppa
    mh901_costo_ppa_energia = _mod.mh901_costo_ppa_energia
    mh901_csv = _mod.mh901_csv
    mh901_demo = _mod.mh901_demo
    mh901_demo_calcoli = _mod.mh901_demo_calcoli
    mh901_eccesso = _mod.mh901_eccesso
    mh901_flussi = _mod.mh901_flussi
    mh901_fraz = _mod.mh901_fraz
    mh901_int_pos = _mod.mh901_int_pos
    mh901_matchata = _mod.mh901_matchata
    mh901_nneg = _mod.mh901_nneg
    mh901_num = _mod.mh901_num
    mh901_payback = _mod.mh901_payback
    mh901_pos = _mod.mh901_pos
    mh901_prezzo_coperto = _mod.mh901_prezzo_coperto
    mh901_prezzo_medio = _mod.mh901_prezzo_medio
    mh901_residua = _mod.mh901_residua
    mh901_riga_anno = _mod.mh901_riga_anno
    mh901_risparmio = _mod.mh901_risparmio
    mh901_sbilanciamento = _mod.mh901_sbilanciamento
    mh901_scenario = _mod.mh901_scenario
    mh901_sensibilita = _mod.mh901_sensibilita
    mh901_serie_annua = _mod.mh901_serie_annua
    mh901_tasso = _mod.mh901_tasso
    mh901_tir = _mod.mh901_tir
    mh901_valida = _mod.mh901_valida
    mh901_van = _mod.mh901_van
    mh901_verdetto = _mod.mh901_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w906_helpers.py")
_UI_PATH = _risolvi("w906_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "0"
_VECCHIO_TAB = "tab90" + "0"
_VECCHIO_ST = "st90" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "matchata_mwh_anno": 9000.0,
    "eccesso_mwh_anno": 3000.0,
    "residua_mwh_anno": 11000.0,
    "costo_ppa_energia_eur_anno": 780000.0,
    "sbilanciamento_eur_anno": 9000.0,
    "costo_merchant_eur_anno": 1800000.0,
    "costo_ppa_eur_anno": 1529000.0,
    "risparmio_eur_anno": 271000.0,
    "prezzo_medio_eur_mwh": 76.45,
    "prezzo_coperto_eur_mwh": 65.75,
    "breakeven_p_ppa": 87.58333333333333,
    "co2_evitata_t_anno": 3000.0,
    "co2_evitata_t_vita": 30000.0,
    "van": 1842590.1658090837,
    "tir": 108.32960864877941,
    "payback": 1,
}

_DEMO_SCENARI = [
    {"nome": "Base", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 90.0,
     "e_ppa_mwh_anno": 12000.0, "matching_frazione": 0.75,
     "risparmio_eur_anno": 271000.0,
     "van": 1842590.1658090837, "tir": 108.32960864877941,
     "payback": 1, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 76.45,
     "prezzo_coperto_eur_mwh": 65.75,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Mercato piu 20 %", "p_mkt_eur_mwh": 102.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 108.0,
     "e_ppa_mwh_anno": 12000.0, "matching_frazione": 0.75,
     "risparmio_eur_anno": 484000.0,
     "van": 3487319.7057254487, "tir": 193.59593177449415,
     "payback": 1, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 83.8,
     "prezzo_coperto_eur_mwh": 65.75,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Mercato meno 20 %", "p_mkt_eur_mwh": 68.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 72.0,
     "e_ppa_mwh_anno": 12000.0, "matching_frazione": 0.75,
     "risparmio_eur_anno": 58000.0,
     "van": 197860.62589271902, "tir": 19.190759438753524,
     "payback": 5, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 69.1,
     "prezzo_coperto_eur_mwh": 65.75,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Matching 0,60", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 90.0,
     "e_ppa_mwh_anno": 12000.0, "matching_frazione": 0.60,
     "risparmio_eur_anno": 256600.0,
     "van": 1731397.1828288224, "tir": 102.55170060967092,
     "payback": 1, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 77.17,
     "prezzo_coperto_eur_mwh": 66.2,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Prezzo PPA piu 10 %", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 71.5, "p_supply_eur_mwh": 90.0,
     "e_ppa_mwh_anno": 12000.0, "matching_frazione": 0.75,
     "risparmio_eur_anno": 193000.0,
     "van": 1240294.8413326684, "tir": 76.94338982704541,
     "payback": 2, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 80.35,
     "prezzo_coperto_eur_mwh": 72.25,
     "co2_evitata_t_anno": 3000.0},
]

_DEMO_CONFRONTO = {
    "costo_merchant": 1800000.0,
    "costo_ppa": 1529000.0,
    "risparmio": 271000.0,
    "matchata": 9000.0,
    "eccesso": 3000.0,
    "residua": 11000.0,
    "prezzo_medio": 76.45,
    "prezzo_coperto": 65.75,
    "c0": 250000.0,
    "c_ann": 5000.0,
    "van": 1842590.1658090837,
    "co2_evitata_t_anno": 3000.0,
    "co2_evitata_t_vita": 30000.0,
    "breakeven_p_ppa": 87.58333333333333,
    "tir": 108.32960864877941,
    "payback": 1,
}

_ORDINE_VALIDA = (
    "e_cons_mwh_anno", "e_ppa_mwh_anno",
    "matching_frazione", "p_fix_eur_mwh",
    "p_mkt_eur_mwh", "p_supply_eur_mwh",
    "c0_eur", "c_ann_eur_anno",
    "c_sbil_eur_mwh", "t_anni", "r_tasso",
    "tol_frazione", "f_co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh901_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))

class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh901_num(3, "x"), 3.0)
        self.assertEqual(mh901_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh901_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh901_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh901_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh901_pos(0, "x")
        with self.assertRaises(ValueError):
            mh901_pos(-1, "x")
        self.assertEqual(mh901_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh901_fraz(0, "x"), 0.0)
        self.assertEqual(mh901_fraz(1, "x"), 1.0)
        self.assertEqual(mh901_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh901_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh901_fraz(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh901_int_pos(10, "x"), 10)
        self.assertEqual(mh901_int_pos(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh901_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh901_int_pos(5.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh901_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh901_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh901_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh901_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh901_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh901_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_matchata_eccesso_residua(self):
        self.assertEqual(mh901_matchata(12000.0, 0.75), 9000.0)
        self.assertEqual(mh901_matchata(12000.0, 0.60), 7200.0)
        self.assertEqual(mh901_matchata(12000.0, 0.0), 0.0)
        self.assertEqual(mh901_matchata(12000.0, 1.0), 12000.0)
        self.assertEqual(mh901_matchata(0.0, 0.75), 0.0)
        with self.assertRaises(ValueError):
            mh901_matchata(12000.0, 1.01)
        with self.assertRaises(ValueError):
            mh901_matchata(12000.0, -0.01)
        with self.assertRaises(ValueError):
            mh901_matchata(-1.0, 0.75)
        self.assertEqual(mh901_eccesso(12000.0, 9000.0), 3000.0)
        self.assertEqual(mh901_eccesso(12000.0, 7200.0), 4800.0)
        self.assertEqual(mh901_eccesso(12000.0, 12000.0), 0.0)
        self.assertEqual(mh901_eccesso(0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh901_eccesso(12000.0, 12001.0)
        with self.assertRaises(ValueError):
            mh901_eccesso(-1.0, 0.0)
        self.assertEqual(mh901_residua(20000.0, 9000.0), 11000.0)
        self.assertEqual(mh901_residua(20000.0, 7200.0), 12800.0)
        self.assertEqual(mh901_residua(20000.0, 0.0), 20000.0)
        with self.assertRaises(ValueError):
            mh901_residua(20000.0, 20001.0)
        with self.assertRaises(ValueError):
            mh901_residua(0, 0.0)

    def test_costo_ppa_energia_e_sbilanciamento(self):
        self.assertEqual(
            mh901_costo_ppa_energia(12000.0, 65.0), 780000.0)
        self.assertEqual(
            mh901_costo_ppa_energia(12000.0, 71.5), 858000.0)
        self.assertEqual(
            mh901_costo_ppa_energia(0.0, 65.0), 0.0)
        self.assertEqual(mh901_sbilanciamento(3000.0, 3.0),
                         9000.0)
        self.assertEqual(mh901_sbilanciamento(4800.0, 3.0),
                         14400.0)
        self.assertEqual(mh901_sbilanciamento(3000.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh901_costo_ppa_energia(-1.0, 65.0)
        with self.assertRaises(ValueError):
            mh901_costo_ppa_energia(12000.0, -1.0)
        with self.assertRaises(ValueError):
            mh901_sbilanciamento(-1.0, 3.0)
        with self.assertRaises(ValueError):
            mh901_sbilanciamento(3000.0, -1.0)

    def test_costo_ppa_gestione_dentro(self):
        self.assertEqual(
            mh901_costo_ppa(780000.0, 11000.0, 90.0, 3000.0,
                            85.0, 9000.0, 5000.0),
            1529000.0)
        self.assertEqual(
            mh901_costo_ppa(780000.0, 12800.0, 90.0, 4800.0,
                            85.0, 14400.0, 5000.0),
            1543400.0)
        self.assertEqual(
            mh901_costo_ppa(780000.0, 11000.0, 90.0, 3000.0,
                            85.0, 9000.0, 0.0),
            1524000.0)
        self.assertEqual(
            mh901_costo_ppa(0.0, 20000.0, 90.0, 0.0, 85.0,
                            0.0, 5000.0),
            1805000.0)
        with self.assertRaises(ValueError):
            mh901_costo_ppa(-1.0, 11000.0, 90.0, 3000.0, 85.0,
                            9000.0, 5000.0)
        with self.assertRaises(ValueError):
            mh901_costo_ppa(780000.0, 11000.0, -1.0, 3000.0,
                            85.0, 9000.0, 5000.0)

    def test_costo_merchant(self):
        self.assertEqual(
            mh901_costo_merchant(20000.0, 90.0), 1800000.0)
        self.assertEqual(
            mh901_costo_merchant(20000.0, 108.0), 2160000.0)
        self.assertEqual(mh901_costo_merchant(20000.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh901_costo_merchant(0, 90.0)
        with self.assertRaises(ValueError):
            mh901_costo_merchant(20000.0, -1.0)

    def test_risparmio_netto_di_gestione(self):
        self.assertEqual(
            mh901_risparmio(1800000.0, 1529000.0), 271000.0)
        self.assertEqual(
            mh901_risparmio(1800000.0, 1800000.0), 0.0)
        self.assertEqual(
            mh901_risparmio(1800000.0, 1829000.0), -29000.0)
        self.assertEqual(
            mh901_risparmio(1800000.0, 1805000.0), -5000.0)
        with self.assertRaises(ValueError):
            mh901_risparmio(-1.0, 1529000.0)
        with self.assertRaises(ValueError):
            mh901_risparmio(1800000.0, -1.0)

    def test_prezzi_medio_e_coperto(self):
        self.assertEqual(
            mh901_prezzo_medio(1529000.0, 20000.0), 76.45)
        self.assertEqual(
            mh901_prezzo_medio(1676000.0, 20000.0), 83.8)
        self.assertEqual(
            mh901_prezzo_medio(1543400.0, 20000.0), 77.17)
        self.assertEqual(
            mh901_prezzo_coperto(780000.0, 9000.0, 12000.0),
            65.75)
        self.assertEqual(
            mh901_prezzo_coperto(780000.0, 14400.0, 12000.0),
            66.2)
        self.assertEqual(
            mh901_prezzo_coperto(858000.0, 9000.0, 12000.0),
            72.25)
        self.assertEqual(
            mh901_prezzo_coperto(780000.0, 0.0, 12000.0),
            65.0)
        self.assertIsNone(
            mh901_prezzo_coperto(780000.0, 9000.0, 0.0))
        self.assertIsNone(
            mh901_prezzo_coperto(0.0, 0.0, 0.0))
        with self.assertRaises(ValueError):
            mh901_prezzo_medio(1529000.0, 0)
        with self.assertRaises(ValueError):
            mh901_prezzo_coperto(-1.0, 9000.0, 12000.0)
        with self.assertRaises(ValueError):
            mh901_prezzo_coperto(780000.0, -1.0, 12000.0)
        with self.assertRaises(ValueError):
            mh901_prezzo_coperto(780000.0, 9000.0, -1.0)

    def test_riga_anno_flusso_uguale_risparmio(self):
        # La gestione e DENTRO il costo con PPA, quindi
        # il flusso annuo e il risparmio, NON risparmio
        # meno gestione: sottrarla di nuovo sarebbe un
        # doppio conteggio.
        riga = mh901_riga_anno(1, 271000.0, 3000.0)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["risparmio"], 271000.0)
        self.assertEqual(riga["flusso"], 271000.0)
        self.assertEqual(riga["co2_evitata"], 3000.0)
        riga = mh901_riga_anno(10, 271000.0, 3000.0)
        self.assertEqual(riga["flusso"], 271000.0)
        with self.assertRaises(ValueError):
            mh901_riga_anno(0, 271000.0, 3000.0)

    def test_serie_annua(self):
        serie = mh901_serie_annua(271000.0, 10, 3000.0)
        self.assertEqual(len(serie), 10)
        self.assertTrue(all(r["flusso"] == 271000.0
                            for r in serie))
        self.assertTrue(all(r["risparmio"] == 271000.0
                            for r in serie))
        self.assertTrue(all(r["co2_evitata"] == 3000.0
                            for r in serie))
        serie = mh901_serie_annua(58000.0, 10, 3000.0)
        self.assertEqual(serie[0]["flusso"], 58000.0)
        with self.assertRaises(ValueError):
            mh901_serie_annua(271000.0, 0, 3000.0)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        flussi = bc["flussi"]
        self.assertEqual(len(flussi), 11)
        self.assertEqual(flussi[0], -250000.0)
        self.assertEqual(flussi[1], 271000.0)
        self.assertEqual(flussi[10], 271000.0)
        self.assertAlmostEqual(sum(flussi), 2460000.00, places=2)
        self.assertAlmostEqual(sum(flussi[:2]), 21000.00, places=2)
        self.assertAlmostEqual(sum(flussi[:3]), 292000.00, places=2)
        self.assertGreater(sum(flussi[:2]), 0.0)
        flussi2 = mh901_flussi(bc["serie"], bc["c0_eur"], 10)
        self.assertEqual(flussi2, flussi)
        self.assertAlmostEqual(mh901_van(flussi, 0.05), bc["van"])
        with self.assertRaises(ValueError):
            mh901_flussi(bc["serie"][:9], bc["c0_eur"], 10)

    def test_breakeven_p_ppa(self):
        self.assertAlmostEqual(
            mh901_breakeven_p_ppa(1800000.0, 11000.0, 90.0,
                                  3000.0, 85.0, 9000.0,
                                  5000.0, 12000.0),
            87.58, places=2)
        self.assertEqual(
            mh901_breakeven_p_ppa(1800000.0, 11000.0, 90.0,
                                  3000.0, 85.0, 9000.0,
                                  0.0, 12000.0),
            88.0)
        self.assertIsNone(
            mh901_breakeven_p_ppa(1800000.0, 11000.0, 90.0,
                                  3000.0, 85.0, 9000.0,
                                  5000.0, 0.0))
        # Al breakeven il risparmio si azzera, il flusso
        # annuo e zero e la VAN resta meno il costo
        # iniziale: pareggio annuo, NON VAN zero.
        be = mh901_breakeven_p_ppa(1800000.0, 11000.0, 90.0,
                                   3000.0, 85.0, 9000.0,
                                   5000.0, 12000.0)
        bc = mh901_calcola(
            **_demo_kwargs(p_fix_eur_mwh=be))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 0.0,
                               places=2)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(
            mh901_van([-250000.0] + [0.0] * 10, 0.05),
            -250000.0, places=2)
        with self.assertRaises(ValueError):
            mh901_breakeven_p_ppa(1800000.0, 11000.0, 90.0,
                                  3000.0, 85.0, 9000.0,
                                  5000.0, -1.0)

    def test_co2_evitata_informativa(self):
        self.assertEqual(
            mh901_co2_evitata_anno(12000.0, 0.25), 3000.0)
        self.assertEqual(
            mh901_co2_evitata_anno(12000.0, 0.0), 0.0)
        self.assertEqual(
            mh901_co2_evitata_vita(3000.0, 10), 30000.0)
        self.assertEqual(
            mh901_co2_evitata_vita(3000.0, 5), 15000.0)
        with self.assertRaises(ValueError):
            mh901_co2_evitata_anno(12000.0, -0.1)
        with self.assertRaises(ValueError):
            mh901_co2_evitata_anno(-1.0, 0.25)
        with self.assertRaises(ValueError):
            mh901_co2_evitata_vita(3000.0, 0)

    def test_scenario_singolo(self):
        s = mh901_scenario("Mercato piu 20 %", mh901_demo(),
                           {"p_mkt_eur_mwh": 102.0,
                            "p_supply_eur_mwh": 108.0})
        self.assertEqual(s["nome"], "Mercato piu 20 %")
        self.assertEqual(s["p_mkt_eur_mwh"], 102.0)
        self.assertEqual(s["p_supply_eur_mwh"], 108.0)
        self.assertAlmostEqual(s["van"], 3487319.71, places=2)
        self.assertEqual(s["payback"], 1)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh901_scenario("Mercato meno 20 %", mh901_demo(),
                           {"p_mkt_eur_mwh": 68.0,
                            "p_supply_eur_mwh": 72.0})
        self.assertAlmostEqual(s["van"], 197860.63, places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh901_scenario("Matching 0,60", mh901_demo(),
                           {"matching_frazione": 0.60})
        self.assertAlmostEqual(s["van"], 1731397.18, places=2)
        self.assertEqual(s["prezzo_coperto_eur_mwh"], 66.2)
        self.assertEqual(s["prezzo_medio_eur_mwh"], 77.17)
        s = mh901_scenario("Prezzo PPA piu 10 %", mh901_demo(),
                           {"p_fix_eur_mwh": 71.5})
        self.assertAlmostEqual(s["van"], 1240294.84, places=2)
        self.assertEqual(s["prezzo_coperto_eur_mwh"], 72.25)
        self.assertEqual(s["prezzo_medio_eur_mwh"], 80.35)
        with self.assertRaises(ValueError):
            mh901_scenario("", mh901_demo(),
                           {"p_mkt_eur_mwh": 102.0})
        with self.assertRaises(ValueError):
            mh901_scenario("X", mh901_demo(),
                           {"e_ppa_mwh_anno": 99999.0})

    def test_scenario_risparmio_negativo_non_calcolabile(self):
        s = mh901_scenario("Prezzo fisso alto", mh901_demo(),
                           {"p_fix_eur_mwh": 90.0})
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh901_confronto(1800000.0, 1529000.0, 271000.0,
                            9000.0, 3000.0, 11000.0,
                            76.45, 65.75,
                            250000.0, 5000.0, 1842590.17,
                            3000.0, 30000.0, 87.58,
                            108.33, 1)
        self.assertEqual(c["costo_merchant"], 1800000.0)
        self.assertEqual(c["costo_ppa"], 1529000.0)
        self.assertEqual(c["risparmio"], 271000.0)
        self.assertEqual(c["matchata"], 9000.0)
        self.assertEqual(c["eccesso"], 3000.0)
        self.assertEqual(c["residua"], 11000.0)
        self.assertEqual(c["prezzo_medio"], 76.45)
        self.assertEqual(c["prezzo_coperto"], 65.75)
        self.assertEqual(c["c0"], 250000.0)
        self.assertEqual(c["c_ann"], 5000.0)
        self.assertEqual(c["van"], 1842590.17)
        self.assertEqual(c["co2_evitata_t_anno"], 3000.0)
        self.assertEqual(c["co2_evitata_t_vita"], 30000.0)
        self.assertEqual(c["breakeven_p_ppa"], 87.58)
        self.assertEqual(c["tir"], 108.33)
        self.assertEqual(c["payback"], 1)
        c = mh901_confronto(1800000.0, 1829000.0, -29000.0,
                            9000.0, 3000.0, 11000.0,
                            91.45, 90.75,
                            250000.0, 5000.0, 0.0,
                            3000.0, 30000.0, None,
                            None, None)
        self.assertIsNone(c["breakeven_p_ppa"])
        self.assertIsNone(c["tir"])
        self.assertIsNone(c["payback"])
        c = mh901_confronto(1800000.0, 1805000.0, -5000.0,
                            0.0, 0.0, 20000.0,
                            90.25, None,
                            250000.0, 5000.0, 0.0,
                            0.0, 0.0, None,
                            None, None)
        self.assertIsNone(c["prezzo_coperto"])
        with self.assertRaises(ValueError):
            mh901_confronto(-1.0, 1529000.0, 271000.0,
                            9000.0, 3000.0, 11000.0,
                            76.45, 65.75,
                            250000.0, 5000.0, 1842590.17,
                            3000.0, 30000.0, 87.58,
                            108.33, 1)

class TestFinanza(unittest.TestCase):
    def test_van_tasso_cinque(self):
        bc = mh901_demo_calcoli()
        self.assertAlmostEqual(
            mh901_van(bc["flussi"], 0.05),
            bc["van"])
        bc_basso = mh901_calcola(
            _scenari=False,
            **dict(mh901_demo(), p_mkt_eur_mwh=68.0,
                   p_supply_eur_mwh=72.0))
        self.assertAlmostEqual(
            mh901_van(bc_basso["flussi"], 0.05),
            bc["scenari"][2]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh901_van([-250000, 271000, 271000], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 1842590,17; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh901_demo_calcoli()
        self.assertAlmostEqual(
            mh901_van(bc["flussi"], 0.05),
            1842590.17, places=2)
        self.assertNotAlmostEqual(
            mh901_van(bc["flussi"], 0.50),
            1842590.17, places=2)
        with self.assertRaises(ValueError):
            mh901_van(bc["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh901_demo_calcoli()
        tir = mh901_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh901_tir([-100, -10, -10]))
        self.assertIsNone(mh901_tir([100, 10, 10]))
        self.assertIsNone(mh901_tir([0, 10, 10]))

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh901_demo_calcoli()
        self.assertEqual(mh901_payback(bc["flussi"]), 1)
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh901_payback([-100, 100, 10]), 1)
        self.assertEqual(mh901_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh901_payback([-100, 10, 10]))
        # Con costo iniziale zero il payback e l'anno 1.
        self.assertEqual(mh901_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh901_demo_calcoli()
        f0 = bc["flussi"]
        self.assertAlmostEqual(sum(f0[:2]), 21000.00, places=2)
        self.assertAlmostEqual(sum(f0[:3]), 292000.00, places=2)
        self.assertAlmostEqual(sum(f0), 2460000.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(
            mh901_verdetto(100.0, 0.10, 250000.0), "CONVIENTE")
        self.assertEqual(
            mh901_verdetto(0.0, 0.10, 250000.0), "MARGINALE")
        self.assertEqual(
            mh901_verdetto(-25000.0, 0.10, 250000.0),
            "MARGINALE")
        self.assertEqual(
            mh901_verdetto(-25001.0, 0.10, 250000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh901_verdetto(-100000.0, 0.10, 250000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativa e
        # NON_CONVIENTE (VAN zero compresa nel MARGINALE
        # solo perche il valore assoluto zero e minore
        # o uguale a zero).
        self.assertEqual(
            mh901_verdetto(-1.0, 0.0, 250000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh901_verdetto(0.0, 0.0, 250000.0), "MARGINALE")
        with self.assertRaises(ValueError):
            mh901_verdetto(100.0, 1.5, 250000.0)
        with self.assertRaises(ValueError):
            mh901_verdetto(100.0, 0.10, -1.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh901_verdetto(None, 0.10, 250000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh901_verdetto(None, 0.0, 0.0), "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh901_demo()
        val = mh901_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_durata_zero_e_non_intera_no(self):
        kw = _demo_kwargs(t_anni=0)
        self.assertRaises(ValueError, mh901_calcola, **kw)
        kw = _demo_kwargs(t_anni=10.5)
        self.assertRaises(ValueError, mh901_calcola, **kw)
        kw = _demo_kwargs(t_anni=5)
        bc = mh901_calcola(**kw)
        self.assertEqual(bc["t_anni"], 5)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh901_calcola(**_demo_kwargs(r_tasso=tasso))
        bc = mh901_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertEqual(bc["r_tasso"], 0.10)

    def test_valida_matching_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh901_calcola(**_demo_kwargs(matching_frazione=1.01))
        with self.assertRaises(ValueError):
            mh901_calcola(**_demo_kwargs(matching_frazione=-0.01))
        bc = mh901_calcola(**_demo_kwargs(matching_frazione=1.0))
        self.assertEqual(bc["matching_frazione"], 1.0)
        bc = mh901_calcola(**_demo_kwargs(matching_frazione=0.0))
        self.assertEqual(bc["matching_frazione"], 0.0)

    def test_valida_energia_ppa_sopra_consumata_no(self):
        with self.assertRaises(ValueError):
            mh901_calcola(**_demo_kwargs(e_ppa_mwh_anno=20001.0))
        bc = mh901_calcola(**_demo_kwargs(e_ppa_mwh_anno=20000.0))
        self.assertEqual(bc["e_ppa_mwh_anno"], 20000.0)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh901_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh901_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("e_cons_mwh_anno", 0),
                              ("t_anni", 0),
                              ("r_tasso", 0)):
            with self.assertRaises(ValueError):
                mh901_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_mkt_eur_mwh=float("nan"))
        self.assertRaises(ValueError, mh901_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh901_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_cons_mwh_anno", -1),
                              ("e_ppa_mwh_anno", -1),
                              ("matching_frazione", -0.1),
                              ("p_fix_eur_mwh", -1),
                              ("p_mkt_eur_mwh", -1),
                              ("p_supply_eur_mwh", -1),
                              ("c0_eur", -1),
                              ("c_ann_eur_anno", -1),
                              ("c_sbil_eur_mwh", -1),
                              ("t_anni", -1),
                              ("r_tasso", -0.01),
                              ("tol_frazione", -0.1),
                              ("f_co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh901_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh901_calcola(mh901_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh901_calcola(dict(mh901_demo(), p_mkt_eur_mwh=999.0),
                           p_mkt_eur_mwh=85.0)
        self.assertEqual(bc["p_mkt_eur_mwh"], 85.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh901_calcola(_scenari=False, **mh901_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van"], 1842590.17, places=2)


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
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(bc["tir"], 108.33, places=2)
        self.assertAlmostEqual(bc["breakeven_p_ppa"],
                               87.58, places=2)
        self.assertAlmostEqual(bc["prezzo_medio_eur_mwh"], 76.45,
                               places=2)
        self.assertAlmostEqual(bc["prezzo_coperto_eur_mwh"], 65.75,
                               places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["matchata_mwh_anno"],
            bc["e_ppa_mwh_anno"] * bc["matching_frazione"])
        self.assertAlmostEqual(
            bc["eccesso_mwh_anno"],
            bc["e_ppa_mwh_anno"] - bc["matchata_mwh_anno"])
        self.assertAlmostEqual(
            bc["residua_mwh_anno"],
            bc["e_cons_mwh_anno"] - bc["matchata_mwh_anno"])
        self.assertAlmostEqual(
            bc["costo_ppa_energia_eur_anno"],
            bc["e_ppa_mwh_anno"] * bc["p_fix_eur_mwh"])
        self.assertAlmostEqual(
            bc["sbilanciamento_eur_anno"],
            bc["eccesso_mwh_anno"] * bc["c_sbil_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_merchant_eur_anno"],
            bc["e_cons_mwh_anno"] * bc["p_supply_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_ppa_eur_anno"],
            bc["costo_ppa_energia_eur_anno"]
            + bc["residua_mwh_anno"] * bc["p_supply_eur_mwh"]
            - bc["eccesso_mwh_anno"] * bc["p_mkt_eur_mwh"]
            + bc["sbilanciamento_eur_anno"]
            + bc["c_ann_eur_anno"])
        # Identita chiave del modello: il risparmio e
        # GIA NETTO di gestione, perche la gestione e
        # DENTRO il costo con PPA.
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["costo_merchant_eur_anno"]
            - bc["costo_ppa_eur_anno"])
        self.assertAlmostEqual(
            bc["prezzo_medio_eur_mwh"],
            bc["costo_ppa_eur_anno"] / bc["e_cons_mwh_anno"])
        self.assertAlmostEqual(
            bc["prezzo_coperto_eur_mwh"],
            (bc["costo_ppa_energia_eur_anno"]
             + bc["sbilanciamento_eur_anno"])
            / bc["e_ppa_mwh_anno"])
        self.assertAlmostEqual(
            bc["breakeven_p_ppa"],
            (bc["costo_merchant_eur_anno"]
             - bc["residua_mwh_anno"] * bc["p_supply_eur_mwh"]
             + bc["eccesso_mwh_anno"] * bc["p_mkt_eur_mwh"]
             - bc["sbilanciamento_eur_anno"]
             - bc["c_ann_eur_anno"])
            / bc["e_ppa_mwh_anno"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["e_ppa_mwh_anno"] * bc["f_co2_t_mwh"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_vita"],
            bc["co2_evitata_t_anno"] * bc["t_anni"])
        self.assertAlmostEqual(
            bc["van"],
            mh901_van(bc["flussi"], bc["r_tasso"]))
        for t in range(1, bc["t_anni"] + 1):
            riga = bc["serie"][t - 1]
            with self.subTest(anno=t):
                self.assertAlmostEqual(
                    riga["flusso"],
                    riga["risparmio"])
        conf = bc["confronto"]
        self.assertEqual(conf["van"], bc["van"])
        self.assertEqual(conf["c0"], bc["c0_eur"])
        self.assertEqual(conf["tir"], bc["tir"])
        self.assertEqual(conf["payback"], bc["payback"])

    def test_scenari_ordinamento(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Il mercato piu 20 % migliora su tutto; il
        # mercato meno 20 % peggiora ma resta CONVIENTE
        # con VAN positiva; il matching 0,60 peggiora ma
        # resta CONVIENTE; il prezzo PPA piu 10 %
        # peggiora ma resta CONVIENTE con payback 2.
        self.assertGreater(bc["scenari"][1]["van"], base["van"])
        self.assertGreater(bc["scenari"][1]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][1]["payback"], 1)
        self.assertLess(bc["scenari"][2]["van"], base["van"])
        self.assertGreater(bc["scenari"][2]["van"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto"], "CONVIENTE")
        self.assertEqual(bc["scenari"][2]["payback"], 5)
        self.assertLess(bc["scenari"][3]["van"], base["van"])
        self.assertEqual(bc["scenari"][3]["verdetto"], "CONVIENTE")
        self.assertEqual(bc["scenari"][3]["payback"], 1)
        self.assertLess(bc["scenari"][4]["van"], base["van"])
        self.assertEqual(bc["scenari"][4]["payback"], 2)
        self.assertEqual(bc["scenari"][4]["verdetto"], "CONVIENTE")

    def test_sensibilita_valori(self):
        s = mh901_sensibilita(**mh901_demo())
        self.assertEqual(set(s.keys()),
                         {"mkt_piu20", "mkt_meno20",
                          "matching_060", "fix_piu10",
                          "c0_zero", "cann_zero",
                          "vita_005", "tasso_010", "eppa_20000",
                          "pmkt_065", "matching_100"})
        attesi = {
            "mkt_piu20": (3487319.71, 193.60, 1, "CONVIENTE"),
            "mkt_meno20": (197860.63, 19.19, 5, "CONVIENTE"),
            "matching_060": (1731397.18, 102.55, 1, "CONVIENTE"),
            "fix_piu10": (1240294.84, 76.94, 2, "CONVIENTE"),
            "c0_zero": (2092590.17, None, 1, "CONVIENTE"),
            "cann_zero": (1881198.84, 110.33, 1, "CONVIENTE"),
            "vita_005": (923288.18, 105.44, 1, "CONVIENTE"),
            "tasso_010": (1415177.69, 108.33, 1, "CONVIENTE"),
            "eppa_20000": (3263389.39, 181.99, 1, "CONVIENTE"),
            "pmkt_065": (1379286.07, 84.21, 2, "CONVIENTE"),
            "matching_100": (2027911.80, 117.95, 1, "CONVIENTE"),
        }
        for nome, (van, tir, pb, verd) in attesi.items():
            with self.subTest(variante=nome):
                if van is None:
                    self.assertIsNone(s[nome]["van"])
                else:
                    self.assertAlmostEqual(s[nome]["van"], van,
                                           places=2)
                if tir is None:
                    self.assertIsNone(s[nome]["tir"])
                else:
                    self.assertAlmostEqual(s[nome]["tir"], tir,
                                           places=2)
                self.assertEqual(s[nome]["payback"], pb)
                self.assertEqual(s[nome]["verdetto"], verd)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh901_csv(bc, mh901_demo())
        for voce in ("e_cons_mwh_anno", "e_ppa_mwh_anno",
                     "matching_frazione",
                     "p_fix_eur_mwh", "p_mkt_eur_mwh",
                     "p_supply_eur_mwh", "c0_eur",
                     "c_ann_eur_anno", "c_sbil_eur_mwh",
                     "t_anni", "r_tasso",
                     "tol_frazione", "f_co2_t_mwh",
                     "matchata_mwh_anno", "eccesso_mwh_anno",
                     "residua_mwh_anno",
                     "costo_ppa_energia_eur_anno",
                     "sbilanciamento_eur_anno",
                     "costo_merchant_eur_anno",
                     "costo_ppa_eur_anno",
                     "risparmio_eur_anno",
                     "prezzo_medio_eur_mwh",
                     "prezzo_coperto_eur_mwh",
                     "breakeven_p_ppa",
                     "co2_evitata_t_anno", "co2_evitata_t_vita",
                     "van", "tir", "payback",
                     "scenario_base_van", "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_mercato_piu20_van",
                     "scenario_mercato_piu20_verdetto",
                     "scenario_mercato_meno20_van",
                     "scenario_mercato_meno20_verdetto",
                     "scenario_matching_060_van",
                     "scenario_matching_060_verdetto",
                     "scenario_fix_piu10_van",
                     "scenario_fix_piu10_verdetto",
                     "anno_1_costo_merchant",
                     "anno_1_costo_ppa",
                     "anno_1_risparmio", "anno_1_flusso",
                     "anno_1_co2_evitata",
                     "anno_10_costo_merchant",
                     "anno_10_risparmio",
                     "anno_10_flusso",
                     "confronto_costo_merchant",
                     "confronto_costo_ppa",
                     "confronto_risparmio",
                     "confronto_matchata",
                     "confronto_eccesso",
                     "confronto_residua",
                     "confronto_prezzo_medio",
                     "confronto_prezzo_coperto",
                     "confronto_c0", "confronto_c_ann",
                     "confronto_van",
                     "confronto_co2_evitata_t_anno",
                     "confronto_co2_evitata_t_vita",
                     "confronto_breakeven_p_ppa",
                     "confronto_tir", "confronto_payback",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 10)
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 30)
        self.assertEqual(len(bc["df_costi"]), 2)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso (EUR)"].iloc[0],
            271000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[0],
            21000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[1],
            292000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[-1],
            2460000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Risparmio (EUR/anno)"].iloc[0],
            271000.00, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Costo merchant (EUR/anno)",
             "Costo con PPA (EUR/anno)",
             "Risparmio (EUR/anno)",
             "Energia matchata (MWh/anno)",
             "Eccesso venduto a mercato (MWh/anno)",
             "Energia residua (MWh/anno)",
             "Prezzo medio (EUR/MWh)",
             "Prezzo coperto (EUR/MWh)",
             "Costo iniziale (EUR)",
             "Costo annuo (EUR/anno)",
             "VAN (EUR)",
             "TIR (%)",
             "Payback (anni)",
             "Breakeven prezzo PPA (EUR/MWh)",
             "CO2 evitata (t/anno)",
             "CO2 evitata vita (t)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            1800000.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[2],
            271000.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Energia consumata (MWh/anno)", voci)
        self.assertIn("Matching (frazione)", voci)
        self.assertIn("Costo sbilanciamento (EUR/MWh)", voci)
        self.assertIn("Costo merchant (EUR/anno)", voci)
        self.assertIn("Prezzo coperto (EUR/MWh)", voci)
        self.assertIn("CO2 evitata vita (t)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))
        self.assertEqual(
            list(bc["df_costi"]["Voce"]),
            ["Merchant", "Con PPA"])
        self.assertAlmostEqual(
            bc["df_costi"]["Costo (EUR/anno)"].iloc[0],
            1800000.00, places=2)
        self.assertAlmostEqual(
            bc["df_costi"]["Costo (EUR/anno)"].iloc[1],
            1529000.00, places=2)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh901_csv(bc, mh901_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_cons_mwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh901_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh901_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh901_calcola(**_demo_kwargs(c0_eur=0.0))
        self.assertEqual(bc["c0_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 2092590.17, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh901_calcola(**_demo_kwargs(c_ann_eur_anno=0.0))
        self.assertEqual(bc["c_ann_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 1881198.84, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh901_calcola(**_demo_kwargs(f_co2_t_mwh=0.0))
        self.assertEqual(bc["co2_evitata_t_anno"], 0.0)
        self.assertEqual(bc["co2_evitata_t_vita"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh901_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        self.assertAlmostEqual(bc["van"], 1842590.17, places=2)
        bc = mh901_calcola(**_demo_kwargs(matching_frazione=0.0))
        self.assertEqual(bc["matching_frazione"], 0.0)
        self.assertAlmostEqual(bc["van"], 1286625.25, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh901_calcola(**_demo_kwargs(c_sbil_eur_mwh=0.0))
        self.assertEqual(bc["c_sbil_eur_mwh"], 0.0)
        self.assertAlmostEqual(bc["van"], 1912085.78, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_prezzo_fisso_alto_non_calcolabile(self):
        kw = _demo_kwargs(p_fix_eur_mwh=90.0)
        bc = mh901_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"], -29000.0)
        self.assertTrue(all(r["risparmio"] <= 0.0
                            for r in bc["serie"]))
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_p_ppa"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        # Matchata e prezzo coperto restano calcolati anche
        # nel regime degenere (sono fisica e prezzi, non
        # KPI di ritorno).
        self.assertEqual(bc["matchata_mwh_anno"], 9000.0)
        self.assertEqual(bc["prezzo_coperto_eur_mwh"], 90.75)

    def test_prezzo_fisso_breakeven_non_calcolabile(self):
        # Al breakeven il risparmio e zero in tutti gli
        # anni, VAN None, NON_CALCOLABILE negli helper e
        # guard NON_CALCOLABILE in UI.
        be = demo_calcoli()["breakeven_p_ppa"]
        kw = _demo_kwargs(p_fix_eur_mwh=be)
        bc = mh901_calcola(**kw)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 0.0,
                               places=2)
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_p_ppa"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_energia_ppa_zero_non_calcolabile(self):
        kw = _demo_kwargs(e_ppa_mwh_anno=0.0)
        bc = mh901_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"], -5000.0)
        self.assertEqual(bc["costo_ppa_eur_anno"],
                         1805000.0)
        self.assertEqual(bc["matchata_mwh_anno"], 0.0)
        self.assertEqual(bc["eccesso_mwh_anno"], 0.0)
        self.assertIsNone(bc["prezzo_coperto_eur_mwh"])
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_fisso_85_marginale_e_tolleranza_zero(self):
        # Stessa VAN meno 10.626,22 del MARGINALE demo,
        # ma con tolleranza zero il confine si sposta:
        # ogni VAN negativa diventa NON_CONVIENTE.
        bc = mh901_calcola(**_demo_kwargs(p_fix_eur_mwh=85.0))
        self.assertAlmostEqual(bc["van"], -10626.22, places=2)
        self.assertAlmostEqual(bc["tir"], 4.12, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        bc = mh901_calcola(
            **_demo_kwargs(p_fix_eur_mwh=85.0,
                           tol_frazione=0.0))
        self.assertAlmostEqual(bc["van"], -10626.22, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_matching_zero_conveniente(self):
        # Con matching 0 il risparmio resta positivo:
        # il prezzo fisso e sotto il prezzo di mercato,
        # quindi il PPA resta conveniente come pura
        # vendita a mercato.
        bc = mh901_calcola(**_demo_kwargs(matching_frazione=0.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 199000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 1286625.25, places=2)
        self.assertAlmostEqual(bc["tir"], 79.37, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["prezzo_medio_eur_mwh"], 80.05,
                               places=2)

    def test_matching_uno_conveniente(self):
        bc = mh901_calcola(**_demo_kwargs(matching_frazione=1.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 295000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 2027911.80, places=2)
        self.assertAlmostEqual(bc["tir"], 117.95, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_energia_ppa_totale_conveniente(self):
        bc = mh901_calcola(**_demo_kwargs(e_ppa_mwh_anno=20000.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 455000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 3263389.39, places=2)
        self.assertAlmostEqual(bc["tir"], 181.99, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["prezzo_medio_eur_mwh"], 67.25,
                               places=2)

    def test_costo_iniziale_zero_tir_non_definita_payback_uno(self):
        bc = mh901_calcola(**_demo_kwargs(c0_eur=0.0))
        self.assertEqual(bc["c0_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(bc["breakeven_p_ppa"],
                               87.58, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_durata_cinque_e_tasso_dieci(self):
        bc = mh901_calcola(**_demo_kwargs(t_anni=5))
        self.assertAlmostEqual(bc["van"], 923288.18, places=2)
        self.assertAlmostEqual(bc["tir"], 105.44, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh901_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertAlmostEqual(bc["van"], 1415177.69, places=2)
        self.assertAlmostEqual(bc["tir"], 108.33, places=2)
        self.assertEqual(bc["payback"], 1)

    def test_prezzo_fisso_piu10_conveniente(self):
        bc = mh901_calcola(**_demo_kwargs(p_fix_eur_mwh=71.5))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 193000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 1240294.84, places=2)
        self.assertAlmostEqual(bc["tir"], 76.94, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_prezzo_mercato_65_conveniente(self):
        # Con prezzo di mercato 65 il risparmio resta
        # positivo: il prezzo di mercato tocca solo la
        # vendita dell'eccesso, non il prezzo fisso.
        bc = mh901_calcola(**_demo_kwargs(p_mkt_eur_mwh=65.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 211000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 1379286.07, places=2)
        self.assertAlmostEqual(bc["tir"], 84.21, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(e_cons_mwh_anno="20000.0")
        self.assertRaises(ValueError, mh901_calcola, **kw)
        kw = _demo_kwargs(e_cons_mwh_anno=True)
        self.assertRaises(ValueError, mh901_calcola, **kw)
        val = mh901_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def901\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh901_demo().keys()), lette - set(mh901_demo().keys()))
        self.assertEqual(lette, set(mh901_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc901\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc901\["([^"]+)"\]', src))
        attese = set(mh901_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 900 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 901.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 908)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab901:"), 1)
        self.assertTrue(src.startswith("    # W906"))

    def test_ui_tab901_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab901:"), 1)
        self.assertIn("def mh901_demo(", src_h)
        self.assertIn("def mh901_calcola(", src_h)
        self.assertIn("tab901", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("PPA fisico: l'energia rinnovabile ritirata davvero a prezzo fisso paga?", src)
        self.assertIn("⚡🤝 PPA fisico: l'energia rinnovabile ritirata davvero a prezzo fisso paga?", src)
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
        chiavi = re.findall(r'key="(st901_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st901_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 19)
        self.assertIn('key="st901_calcola"', src)
        self.assertIn('key="st901_csv"', src)
        self.assertIn('key="st901_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg901"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos901", src)

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
