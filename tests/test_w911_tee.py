"""Test nuova scheda TEE: il risparmio
energetico si vende?
Repo path: tests/test_w911_tee.py

Effetto ECONOMICO: un Certificato Bianco
(TEE, Titolo di Efficienza Energetica)
certifica 1 tep di energia risparmiata:
1 TEE = 1 tep risparmiato e 1 tep =
11,63 MWh, quindi i TEE annui sono il
risparmio in MWh diviso 11,63. Chi
realizza un intervento di efficienza
vende i TEE sul mercato a prezzo TEE e
incassa il ricavo annuo; paga O&M e
certificazione/audit ogni anno e il
CAPEX una volta sola all'anno zero. Il
margine netto annuo e ricavo meno costo
annuo: se e positivo, il progetto genera
cassa ogni anno incentivato; se e zero o
negativo, il progetto non si ripaga mai
e il verdetto e NON_CALCOLABILE. Il VAN
e meno CAPEX piu margine per
l'annualita a tasso dato sugli anni
incentivati; la TIR e il tasso che
azzera il VAN (bisezione); il payback e
il primo anno in cui il cumulato del
margine raggiunge il CAPEX. Il
breakeven prezzo TEE e costo annuo
diviso TEE annui: e il prezzo TEE che
azzera il margine, NON il prezzo che
azzera il VAN (a margine zero il VAN
resta meno CAPEX). Il breakeven
risparmio e costo annuo per 11,63
diviso prezzo TEE: e il risparmio che
azzera il margine. La CO2 evitata e
risparmio per fattore CO2 in t/anno:
0,25 t/MWh per MWh danno t, senza
divisioni per 1000.
Demo: risparmio 2326 MWh/anno (200 tep),
prezzo TEE 260 EUR/TEE, durata 5 anni,
CAPEX 120.000 EUR, O&M 5.000 EUR/anno,
certificazione 3.000 EUR/anno, tasso
0,05, tolleranza 0,10, fattore CO2 0,25
t/MWh. TEE annui = 2326 diviso 11,63 =
200. Ricavo annuo = 200 per 260 =
52.000 EUR. Costo annuo = 5.000 piu
3.000 = 8.000 EUR. Margine netto annuo
= 52.000 meno 8.000 = 44.000 EUR.
Annualita 5 anni al 5 per cento =
4,3294766706. VAN = meno 120.000 piu
44.000 per 4,3294766706 = 70.496,97 EUR.
TIR = 24,32 per cento. Payback = 3 anni
(cumulato anno 2 = 88.000 sotto CAPEX,
anno 3 = 132.000 sopra CAPEX;
frazionale 2,73 anni). Breakeven prezzo
TEE = 8.000 diviso 200 = 40 EUR/TEE.
Breakeven risparmio = 8.000 per 11,63
diviso 260 = 357,85 MWh/anno. CO2
evitata = 2326 per 0,25 = 581,5 t/anno.
Verdetto CONVIENTE.
Scenari: base TEE 200, ricavo 52.000,
margine 44.000, VAN 70.496,97, TIR
24,32 per cento, payback 3 anni,
breakeven prezzo 40, breakeven risparmio
357,85, CONVIENTE; TEE piu 30 per cento
(prezzo 338) ricavo 67.600, margine
59.600, VAN 138.036,81, TIR 40,64 per
cento, payback 3 anni, breakeven
risparmio 275,27, CONVIENTE; TEE meno
30 per cento (prezzo 182) ricavo 36.400,
margine 28.400, VAN 2.957,14, TIR 5,89
per cento, payback 5 anni, breakeven
risparmio 511,21, CONVIENTE; risparmio
meno 20 per cento (1860,8 MWh) TEE 160,
ricavo 41.600, margine 33.600, VAN
25.470,42, TIR 12,38 per cento, payback
4 anni, breakeven prezzo 50, CO2 465,2
t/anno, CONVIENTE; durata 3 anni TEE
200, ricavo 52.000, margine 44.000, VAN
meno 177,09, TIR 4,92 per cento,
payback 3 anni, MARGINALE.
Confronto: TEE annui 200 contro ricavo
52.000, costo annuo 8.000 contro
margine 44.000, VAN 70.496,97 contro
TIR 24,32 per cento, payback 3 anni
contro breakeven prezzo 40, breakeven
risparmio 357,85 contro CO2 581,5
t/anno.
Tolleranza in FRAZIONE (0,10 = 10 % del
CAPEX), usata diretta, NON divisa
per 100. Prezzo TEE, O&M e
certificazione medi annui costanti,
SEMPLIFICAZIONE DICHIARATA (il prezzo
TEE oscilla con domanda e offerta di
titoli, il risparmio reale puo
scostarsi dalla stima, O&M e
certificazione possono crescere nel
mondo reale, qui valori medi costanti);
i flussi sono solo sugli anni
incentivati, SEMPLIFICAZIONE DICHIARATA
(dopo la fine dell'incentivo il
risparmio continua ma senza ricavo TEE).
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il margine
netto annuo e zero o negativo oppure se
un input e degenere (risparmio negativo,
prezzo TEE negativo, durata negativa o
non intera, CAPEX negativo, O&M
negativo, certificazione negativa, tasso
negativo o sopra 1, tolleranza negativa
o sopra 1, fattore CO2 negativo);
altrimenti CONVIENTE se il VAN e
maggiore di 0, MARGINALE se il VAN e
minore o uguale a 0 e il suo valore
assoluto e minore o uguale a tolleranza
per CAPEX, NON_CONVIENTE altrimenti.
La durata zero NON e degenere: da VAN
meno CAPEX, TIR None, payback None e
verdetto NON_CONVIENTE. Il CAPEX zero
NON e degenere: da VAN positivo, TIR
None, payback 0 e verdetto CONVIENTE.
Il risparmio zero NON e degenere: da
TEE zero, ricavo zero, margine meno
costo annuo e verdetto NON_CALCOLABILE,
con breakeven prezzo TEE None. Il
prezzo TEE zero NON e degenere: da
ricavo zero, margine meno costo annuo e
verdetto NON_CALCOLABILE, con breakeven
risparmio None.
Casi limite: risparmio zero (TEE 0,
ricavo 0, margine meno 8000, VAN meno
154.635,81, NON_CALCOLABILE); prezzo
TEE zero (ricavo 0, margine meno 8000,
VAN meno 154.635,81, NON_CALCOLABILE);
margine zero, prezzo 40 (ricavo 8000,
margine 0, VAN meno 120.000,
NON_CALCOLABILE); margine negativo,
prezzo 30 (margine meno 2000, VAN meno
128.658,95, NON_CALCOLABILE); durata
zero (VAN meno 120.000, TIR None,
payback None, NON_CONVIENTE); CAPEX
zero (VAN 190.496,97, TIR None,
payback 0, CONVIENTE).
Distinzione esplicita: qui SOLO i TEE,
i titoli sul risparmio energetico
certificato (1 TEE = 1 tep risparmiato
= 11,63 MWh risparmiati, con baseline
contro post intervento e risparmio
ADDIZIONALE certificato, niente double
counting), NIENTE GO (la GO certifica
l'origine rinnovabile dell'energia, il
TEE certifica il risparmio: una GO non
e un risparmio e un MWh rinnovabile non
e un MWh risparmiato), NIENTE EU ETS
(l'ETS e un costo sulla CO2 emessa, il
TEE e un ricavo dal risparmio: l'ETS si
paga, il TEE si vende), NIENTE Conto
Termico (il Conto Termico e un
contributo in conto capitale sul calore
rinnovabile, non un titolo negoziabile
sul risparmio).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w911_helpers import (
        demo_calcoli,
        mh906_annuity,
        mh906_be_prezzo,
        mh906_be_risparmio,
        mh906_calcola,
        mh906_co2,
        mh906_confronto,
        mh906_costo_annuo,
        mh906_csv,
        mh906_demo,
        mh906_demo_calcoli,
        mh906_durata,
        mh906_fraz,
        mh906_margine,
        mh906_mwh_a_tep,
        mh906_nneg,
        mh906_num,
        mh906_payback,
        mh906_payback_fraz,
        mh906_pos,
        mh906_ricavo,
        mh906_scenario,
        mh906_sensibilita,
        mh906_tee_annui,
        mh906_tep_a_mwh,
        mh906_tir,
        mh906_valida,
        mh906_van,
        mh906_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w911_helpers", os.path.join(_hf, "w911_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh906_annuity = _mod.mh906_annuity
    mh906_be_prezzo = _mod.mh906_be_prezzo
    mh906_be_risparmio = _mod.mh906_be_risparmio
    mh906_calcola = _mod.mh906_calcola
    mh906_co2 = _mod.mh906_co2
    mh906_confronto = _mod.mh906_confronto
    mh906_costo_annuo = _mod.mh906_costo_annuo
    mh906_csv = _mod.mh906_csv
    mh906_demo = _mod.mh906_demo
    mh906_demo_calcoli = _mod.mh906_demo_calcoli
    mh906_durata = _mod.mh906_durata
    mh906_fraz = _mod.mh906_fraz
    mh906_margine = _mod.mh906_margine
    mh906_mwh_a_tep = _mod.mh906_mwh_a_tep
    mh906_nneg = _mod.mh906_nneg
    mh906_num = _mod.mh906_num
    mh906_payback = _mod.mh906_payback
    mh906_payback_fraz = _mod.mh906_payback_fraz
    mh906_pos = _mod.mh906_pos
    mh906_ricavo = _mod.mh906_ricavo
    mh906_scenario = _mod.mh906_scenario
    mh906_sensibilita = _mod.mh906_sensibilita
    mh906_tee_annui = _mod.mh906_tee_annui
    mh906_tep_a_mwh = _mod.mh906_tep_a_mwh
    mh906_tir = _mod.mh906_tir
    mh906_valida = _mod.mh906_valida
    mh906_van = _mod.mh906_van
    mh906_verdetto = _mod.mh906_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w911_helpers.py")
_UI_PATH = _risolvi("w911_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "5"
_VECCHIO_TAB = "tab90" + "5"
_VECCHIO_ST = "st90" + "5_"
_VECCHIO_SIGLA = "go" + "orig"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "tee_annui": 200.0,
    "risparmio_tep": 200.0,
    "ricavo_eur_anno": 52000.0,
    "costo_annuo_eur": 8000.0,
    "margine_eur_anno": 44000.0,
    "van_eur": 70496.97350775619,
    "tir_frazione": 0.24319056868820854,
    "payback_anni": 3,
    "payback_fraz_anni": 2.727272727272727,
    "be_prezzo_eur_tee": 40.0,
    "be_risparmio_mwh_anno": 357.84615384615387,
    "co2_t_anno": 581.5,
    "verdetto": "CONVIENTE",
}

_DEMO_SCENARI = [
    {"nome": "Base", "risparmio_mwh": 2326.0,
     "prezzo_tee_eur": 260.0, "durata_anni": 5,
     "tee_annui": 200.0, "ricavo_eur_anno": 52000.0,
     "margine_eur_anno": 44000.0,
     "van_eur": 70496.97350775619,
     "tir_frazione": 0.24319056868820854,
     "payback_anni": 3,
     "payback_fraz_anni": 2.727272727272727,
     "be_prezzo_eur_tee": 40.0,
     "be_risparmio_mwh_anno": 357.84615384615387,
     "co2_t_anno": 581.5, "verdetto": "CONVIENTE"},
    {"nome": "TEE piu 30 %", "risparmio_mwh": 2326.0,
     "prezzo_tee_eur": 338.0, "durata_anni": 5,
     "tee_annui": 200.0, "ricavo_eur_anno": 67600.0,
     "margine_eur_anno": 59600.0,
     "van_eur": 138036.809569597,
     "tir_frazione": 0.40640204457733986,
     "payback_anni": 3,
     "payback_fraz_anni": 2.0134228187919465,
     "be_prezzo_eur_tee": 40.0,
     "be_risparmio_mwh_anno": 275.26627218934914,
     "co2_t_anno": 581.5, "verdetto": "CONVIENTE"},
    {"nome": "TEE meno 30 %", "risparmio_mwh": 2326.0,
     "prezzo_tee_eur": 182.0, "durata_anni": 5,
     "tee_annui": 200.0, "ricavo_eur_anno": 36400.0,
     "margine_eur_anno": 28400.0,
     "van_eur": 2957.1374459153594,
     "tir_frazione": 0.05886933809040863,
     "payback_anni": 5,
     "payback_fraz_anni": 4.225352112676056,
     "be_prezzo_eur_tee": 40.0,
     "be_risparmio_mwh_anno": 511.2087912087912,
     "co2_t_anno": 581.5, "verdetto": "CONVIENTE"},
    {"nome": "Risparmio meno 20 %", "risparmio_mwh": 1860.8,
     "prezzo_tee_eur": 260.0, "durata_anni": 5,
     "tee_annui": 160.0, "ricavo_eur_anno": 41600.0,
     "margine_eur_anno": 33600.0,
     "van_eur": 25470.416133195627,
     "tir_frazione": 0.1237624145686757,
     "payback_anni": 4,
     "payback_fraz_anni": 3.5714285714285716,
     "be_prezzo_eur_tee": 50.0,
     "be_risparmio_mwh_anno": 357.84615384615387,
     "co2_t_anno": 465.20000000000005,
     "verdetto": "CONVIENTE"},
    {"nome": "Durata 3 anni", "risparmio_mwh": 2326.0,
     "prezzo_tee_eur": 260.0, "durata_anni": 3,
     "tee_annui": 200.0, "ricavo_eur_anno": 52000.0,
     "margine_eur_anno": 44000.0,
     "van_eur": -177.08670769889432,
     "tir_frazione": 0.04921225642348716,
     "payback_anni": 3,
     "payback_fraz_anni": 2.727272727272727,
     "be_prezzo_eur_tee": 40.0,
     "be_risparmio_mwh_anno": 357.84615384615387,
     "co2_t_anno": 581.5, "verdetto": "MARGINALE"},
]

_DEMO_CONFRONTO = {
    "tee_annui": 200.0,
    "ricavo_eur_anno": 52000.0,
    "costo_annuo_eur": 8000.0,
    "margine_eur_anno": 44000.0,
    "van_eur": 70496.97350775619,
    "tir_frazione": 0.24319056868820854,
    "payback_anni": 3,
    "be_prezzo_eur_tee": 40.0,
    "be_risparmio_mwh_anno": 357.84615384615387,
    "co2_t_anno": 581.5,
    "verdetto": "CONVIENTE",
}

_ORDINE_VALIDA = (
    "risparmio_mwh", "prezzo_tee_eur", "durata_anni",
    "capex_eur", "om_eur_anno", "certificazione_eur_anno",
    "tasso_frazione", "tol_frazione", "fattore_co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh906_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh906_num(3, "x"), 3.0)
        self.assertEqual(mh906_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh906_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh906_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh906_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh906_pos(0, "x")
        with self.assertRaises(ValueError):
            mh906_pos(-1, "x")
        self.assertEqual(mh906_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh906_fraz(0, "x"), 0.0)
        self.assertEqual(mh906_fraz(1, "x"), 1.0)
        self.assertEqual(mh906_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh906_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh906_fraz(1.01, "x")

    def test_durata_bordi(self):
        self.assertEqual(mh906_durata(0, "x"), 0)
        self.assertEqual(mh906_durata(5, "x"), 5)
        self.assertEqual(mh906_durata(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh906_durata(-1, "x")
        with self.assertRaises(ValueError):
            mh906_durata(2.5, "x")
        with self.assertRaises(ValueError):
            mh906_durata(float("nan"), "x")


class TestFisica(unittest.TestCase):
    def test_conversioni_tep_mwh(self):
        self.assertEqual(mh906_tep_a_mwh(200.0), 2326.0)
        self.assertEqual(mh906_tep_a_mwh(0.0), 0.0)
        self.assertAlmostEqual(mh906_tep_a_mwh(160.0), 1860.8,
                               places=9)
        self.assertEqual(mh906_mwh_a_tep(2326.0), 200.0)
        self.assertEqual(mh906_mwh_a_tep(0.0), 0.0)
        self.assertAlmostEqual(mh906_mwh_a_tep(1860.8), 160.0,
                               places=9)
        with self.assertRaises(ValueError):
            mh906_tep_a_mwh(-1.0)
        with self.assertRaises(ValueError):
            mh906_mwh_a_tep(-1.0)

    def test_tee_annui(self):
        self.assertEqual(mh906_tee_annui(2326.0), 200.0)
        self.assertAlmostEqual(mh906_tee_annui(1860.8), 160.0,
                               places=9)
        self.assertEqual(mh906_tee_annui(0.0), 0.0)
        self.assertEqual(mh906_tee_annui(1163.0), 100.0)
        self.assertEqual(mh906_tee_annui(357.84615384615387),
                         30.76923076923077)
        with self.assertRaises(ValueError):
            mh906_tee_annui(-1.0)

    def test_ricavo(self):
        self.assertEqual(mh906_ricavo(200.0, 260.0), 52000.0)
        self.assertEqual(mh906_ricavo(200.0, 338.0), 67600.0)
        self.assertEqual(mh906_ricavo(200.0, 182.0), 36400.0)
        self.assertEqual(mh906_ricavo(160.0, 260.0), 41600.0)
        self.assertEqual(mh906_ricavo(0.0, 260.0), 0.0)
        self.assertEqual(mh906_ricavo(200.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh906_ricavo(-1.0, 260.0)
        with self.assertRaises(ValueError):
            mh906_ricavo(200.0, -1.0)

    def test_costo_annuo(self):
        self.assertEqual(mh906_costo_annuo(5000.0, 3000.0), 8000.0)
        self.assertEqual(mh906_costo_annuo(0.0, 3000.0), 3000.0)
        self.assertEqual(mh906_costo_annuo(5000.0, 0.0), 5000.0)
        self.assertEqual(mh906_costo_annuo(0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh906_costo_annuo(-1.0, 3000.0)
        with self.assertRaises(ValueError):
            mh906_costo_annuo(5000.0, -1.0)

    def test_margine(self):
        self.assertEqual(mh906_margine(52000.0, 8000.0), 44000.0)
        self.assertEqual(mh906_margine(67600.0, 8000.0), 59600.0)
        self.assertEqual(mh906_margine(36400.0, 8000.0), 28400.0)
        self.assertEqual(mh906_margine(8000.0, 8000.0), 0.0)
        self.assertEqual(mh906_margine(6000.0, 8000.0), -2000.0)
        self.assertEqual(mh906_margine(0.0, 8000.0), -8000.0)

    def test_annuity(self):
        self.assertAlmostEqual(mh906_annuity(5, 0.05),
                               4.3294766706308225, places=9)
        self.assertAlmostEqual(mh906_annuity(3, 0.05),
                               2.723248029370478, places=9)
        self.assertEqual(mh906_annuity(5, 0.0), 5.0)
        self.assertEqual(mh906_annuity(0, 0.05), 0.0)
        self.assertEqual(mh906_annuity(0, 0.0), 0.0)
        self.assertAlmostEqual(mh906_annuity(5, 0.10),
                               3.79078676940845, places=9)
        with self.assertRaises(ValueError):
            mh906_annuity(-1, 0.05)
        with self.assertRaises(ValueError):
            mh906_annuity(2.5, 0.05)

    def test_van(self):
        self.assertAlmostEqual(
            mh906_van(120000.0, 44000.0, 5, 0.05),
            70496.97350775619, places=2)
        self.assertAlmostEqual(
            mh906_van(120000.0, 59600.0, 5, 0.05),
            138036.809569597, places=2)
        self.assertAlmostEqual(
            mh906_van(120000.0, 28400.0, 5, 0.05),
            2957.1374459153594, places=2)
        self.assertAlmostEqual(
            mh906_van(120000.0, 44000.0, 3, 0.05),
            -177.08670769889432, places=2)
        self.assertEqual(mh906_van(120000.0, 44000.0, 0, 0.05),
                         -120000.0)
        self.assertAlmostEqual(
            mh906_van(0.0, 44000.0, 5, 0.05),
            190496.97350775619, places=2)
        self.assertAlmostEqual(
            mh906_van(120000.0, 44000.0, 5, 0.0),
            100000.0, places=2)
        self.assertAlmostEqual(
            mh906_van(120000.0, -8000.0, 5, 0.05),
            -154635.81356504658, places=2)

    def test_tir(self):
        self.assertAlmostEqual(mh906_tir(120000.0, 44000.0, 5),
                               0.24319056868820854, places=4)
        self.assertAlmostEqual(mh906_tir(120000.0, 59600.0, 5),
                               0.40640204457733986, places=4)
        self.assertAlmostEqual(mh906_tir(120000.0, 28400.0, 5),
                               0.05886933809040863, places=4)
        self.assertAlmostEqual(mh906_tir(120000.0, 44000.0, 3),
                               0.04921225642348716, places=4)
        self.assertIsNone(mh906_tir(0.0, 44000.0, 5))
        self.assertIsNone(mh906_tir(120000.0, 0.0, 5))
        self.assertIsNone(mh906_tir(120000.0, -2000.0, 5))
        self.assertIsNone(mh906_tir(120000.0, 44000.0, 0))
        # Alla TIR il VAN e zero.
        tir = mh906_tir(120000.0, 44000.0, 5)
        self.assertAlmostEqual(
            mh906_van(120000.0, 44000.0, 5, tir), 0.0, places=2)

    def test_payback(self):
        self.assertEqual(mh906_payback(120000.0, 44000.0, 5), 3)
        self.assertEqual(mh906_payback(120000.0, 59600.0, 5), 3)
        self.assertEqual(mh906_payback(120000.0, 28400.0, 5), 5)
        self.assertEqual(mh906_payback(120000.0, 33600.0, 5), 4)
        self.assertEqual(mh906_payback(120000.0, 44000.0, 3), 3)
        self.assertEqual(mh906_payback(0.0, 44000.0, 5), 0)
        self.assertIsNone(mh906_payback(120000.0, 0.0, 5))
        self.assertIsNone(mh906_payback(120000.0, -2000.0, 5))
        self.assertIsNone(mh906_payback(120000.0, 44000.0, 0))
        # Margine troppo piccolo: mai entro la durata.
        self.assertIsNone(mh906_payback(120000.0, 10000.0, 5))
        self.assertEqual(mh906_payback(120000.0, 10000.0, 12),
                         12)

    def test_payback_fraz(self):
        self.assertAlmostEqual(
            mh906_payback_fraz(120000.0, 44000.0, 5),
            2.727272727272727, places=9)
        self.assertAlmostEqual(
            mh906_payback_fraz(120000.0, 59600.0, 5),
            2.0134228187919465, places=9)
        self.assertEqual(mh906_payback_fraz(0.0, 44000.0, 5),
                         0.0)
        self.assertIsNone(mh906_payback_fraz(120000.0, 0.0, 5))
        self.assertIsNone(
            mh906_payback_fraz(120000.0, -2000.0, 5))
        self.assertIsNone(
            mh906_payback_fraz(120000.0, 44000.0, 0))

    def test_be_prezzo(self):
        self.assertEqual(mh906_be_prezzo(8000.0, 200.0), 40.0)
        self.assertEqual(mh906_be_prezzo(8000.0, 160.0), 50.0)
        self.assertEqual(mh906_be_prezzo(3000.0, 200.0), 15.0)
        self.assertEqual(mh906_be_prezzo(5000.0, 200.0), 25.0)
        self.assertEqual(mh906_be_prezzo(0.0, 200.0), 0.0)
        self.assertIsNone(mh906_be_prezzo(8000.0, 0.0))
        with self.assertRaises(ValueError):
            mh906_be_prezzo(-1.0, 200.0)
        # Al prezzo TEE di breakeven il margine e zero
        # e il verdetto e NON_CALCOLABILE.
        be = mh906_be_prezzo(8000.0, 200.0)
        bc = mh906_calcola(
            **_demo_kwargs(prezzo_tee_eur=be))
        self.assertAlmostEqual(bc["margine_eur_anno"], 0.0,
                               places=2)
        self.assertAlmostEqual(bc["van_eur"], -120000.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_be_risparmio(self):
        self.assertAlmostEqual(
            mh906_be_risparmio(8000.0, 260.0),
            357.84615384615387, places=2)
        self.assertAlmostEqual(
            mh906_be_risparmio(8000.0, 338.0),
            275.26627218934914, places=2)
        self.assertAlmostEqual(
            mh906_be_risparmio(8000.0, 182.0),
            511.2087912087912, places=2)
        self.assertAlmostEqual(
            mh906_be_risparmio(3000.0, 260.0),
            134.19230769230768, places=2)
        self.assertAlmostEqual(
            mh906_be_risparmio(5000.0, 260.0),
            223.65384615384616, places=2)
        self.assertIsNone(mh906_be_risparmio(8000.0, 0.0))
        with self.assertRaises(ValueError):
            mh906_be_risparmio(-1.0, 260.0)
        # Al risparmio di breakeven il margine e
        # zero e il verdetto e NON_CALCOLABILE.
        br = mh906_be_risparmio(8000.0, 260.0)
        bc = mh906_calcola(**_demo_kwargs(risparmio_mwh=br))
        self.assertAlmostEqual(bc["margine_eur_anno"], 0.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_be_prezzo_invariante_prezzo_corrente(self):
        # Il breakeven prezzo TEE e INVARIANTE al
        # prezzo TEE corrente.
        bc0 = demo_calcoli()
        bc = mh906_calcola(
            **_demo_kwargs(prezzo_tee_eur=338.0))
        self.assertEqual(bc["be_prezzo_eur_tee"],
                         bc0["be_prezzo_eur_tee"])
        self.assertEqual(bc["be_prezzo_eur_tee"], 40.0)

    def test_be_risparmio_invariante_risparmio_corrente(self):
        # Il breakeven risparmio e INVARIANTE al
        # risparmio corrente.
        bc0 = demo_calcoli()
        bc = mh906_calcola(
            **_demo_kwargs(risparmio_mwh=1860.8))
        self.assertEqual(bc["be_risparmio_mwh_anno"],
                         bc0["be_risparmio_mwh_anno"])
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               357.84615384615387, places=2)

    def test_co2(self):
        self.assertEqual(mh906_co2(2326.0, 0.25), 581.5)
        self.assertEqual(mh906_co2(1860.8, 0.25), 465.2)
        self.assertEqual(mh906_co2(0.0, 0.25), 0.0)
        self.assertEqual(mh906_co2(2326.0, 0.0), 0.0)
        self.assertEqual(mh906_co2(1000.0, 0.25), 250.0)
        with self.assertRaises(ValueError):
            mh906_co2(-1.0, 0.25)
        with self.assertRaises(ValueError):
            mh906_co2(2326.0, -0.1)

    def test_scenario_singolo(self):
        s = mh906_scenario("TEE piu 30 %", mh906_demo(),
                           {"prezzo_tee_eur": 338.0})
        self.assertEqual(s["nome"], "TEE piu 30 %")
        self.assertEqual(s["prezzo_tee_eur"], 338.0)
        self.assertAlmostEqual(s["van_eur"], 138036.81,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["be_prezzo_eur_tee"], 40.0,
                               places=2)
        self.assertAlmostEqual(s["be_risparmio_mwh_anno"],
                               275.27, places=2)
        s = mh906_scenario("TEE meno 30 %", mh906_demo(),
                           {"prezzo_tee_eur": 182.0})
        self.assertAlmostEqual(s["van_eur"], 2957.14, places=2)
        self.assertEqual(s["payback_anni"], 5)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh906_scenario("Risparmio meno 20 %", mh906_demo(),
                           {"risparmio_mwh": 1860.8})
        self.assertAlmostEqual(s["tee_annui"], 160.0, places=9)
        self.assertAlmostEqual(s["van_eur"], 25470.42, places=2)
        self.assertAlmostEqual(s["be_prezzo_eur_tee"], 50.0,
                               places=2)
        s = mh906_scenario("Durata 3 anni", mh906_demo(),
                           {"durata_anni": 3})
        self.assertAlmostEqual(s["van_eur"], -177.09, places=2)
        self.assertEqual(s["verdetto"], "MARGINALE")
        with self.assertRaises(ValueError):
            mh906_scenario("", mh906_demo(),
                           {"prezzo_tee_eur": 338.0})
        with self.assertRaises(ValueError):
            mh906_scenario("X", mh906_demo(),
                           {"durata_anni": -1})

    def test_scenario_risparmio_zero(self):
        s = mh906_scenario("Risparmio 0", mh906_demo(),
                           {"risparmio_mwh": 0.0})
        self.assertEqual(s["tee_annui"], 0.0)
        self.assertEqual(s["ricavo_eur_anno"], 0.0)
        self.assertEqual(s["margine_eur_anno"], -8000.0)
        self.assertIsNone(s["be_prezzo_eur_tee"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh906_confronto(200.0, 52000.0, 8000.0, 44000.0,
                            70496.97350775619,
                            0.24319056868820854, 3, 40.0,
                            357.84615384615387, 581.5,
                            "CONVIENTE")
        self.assertEqual(c["tee_annui"], 200.0)
        self.assertEqual(c["ricavo_eur_anno"], 52000.0)
        self.assertEqual(c["costo_annuo_eur"], 8000.0)
        self.assertEqual(c["margine_eur_anno"], 44000.0)
        self.assertEqual(c["van_eur"], 70496.97350775619)
        self.assertEqual(c["tir_frazione"],
                         0.24319056868820854)
        self.assertEqual(c["payback_anni"], 3)
        self.assertEqual(c["be_prezzo_eur_tee"], 40.0)
        self.assertEqual(c["be_risparmio_mwh_anno"],
                         357.84615384615387)
        self.assertEqual(c["co2_t_anno"], 581.5)
        self.assertEqual(c["verdetto"], "CONVIENTE")
        c = mh906_confronto(0.0, 0.0, 8000.0, -8000.0,
                            -154635.81356504658, None, None,
                            None, 357.84615384615387, 0.0,
                            "NON_CALCOLABILE")
        self.assertIsNone(c["tir_frazione"])
        self.assertIsNone(c["payback_anni"])
        self.assertIsNone(c["be_prezzo_eur_tee"])
        self.assertEqual(c["verdetto"], "NON_CALCOLABILE")
        with self.assertRaises(ValueError):
            mh906_confronto(200.0, 52000.0, 8000.0, 44000.0,
                            70496.97350775619,
                            0.24319056868820854, 3, 40.0,
                            357.84615384615387, 581.5, "FORSE")
        with self.assertRaises(ValueError):
            mh906_confronto(200.0, -1.0, 8000.0, 44000.0,
                            70496.97350775619,
                            0.24319056868820854, 3, 40.0,
                            357.84615384615387, 581.5,
                            "CONVIENTE")


class TestFinanza(unittest.TestCase):
    def test_verdetto_bordi(self):
        self.assertEqual(
            mh906_verdetto(100.0, 0.10, 120000.0, 44000.0),
            "CONVIENTE")
        self.assertEqual(
            mh906_verdetto(0.0, 0.10, 120000.0, 44000.0),
            "MARGINALE")
        self.assertEqual(
            mh906_verdetto(-12000.0, 0.10, 120000.0, 44000.0),
            "MARGINALE")
        self.assertEqual(
            mh906_verdetto(-12001.0, 0.10, 120000.0, 44000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh906_verdetto(-50000.0, 0.10, 120000.0, 44000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativo
        # e NON_CONVIENTE (VAN zero compreso nel
        # MARGINALE solo perche il valore assoluto
        # zero e minore o uguale a zero).
        self.assertEqual(
            mh906_verdetto(-1.0, 0.0, 120000.0, 44000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh906_verdetto(0.0, 0.0, 120000.0, 44000.0),
            "MARGINALE")
        with self.assertRaises(ValueError):
            mh906_verdetto(100.0, 1.5, 120000.0, 44000.0)
        with self.assertRaises(ValueError):
            mh906_verdetto(100.0, 0.10, -1.0, 44000.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh906_verdetto(None, 0.10, 120000.0, 44000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh906_verdetto(None, 0.0, 0.0, 44000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh906_verdetto(100.0, 0.10, 120000.0, None),
            "NON_CALCOLABILE")

    def test_verdetto_margine_zero_negativo_non_calcolabile(self):
        self.assertEqual(
            mh906_verdetto(-120000.0, 0.10, 120000.0, 0.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh906_verdetto(-128658.95, 0.10, 120000.0, -2000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh906_verdetto(70496.97, 0.10, 120000.0, 44000.0),
            "CONVIENTE")

    def test_verdetto_capex_zero(self):
        # Con CAPEX zero la tolleranza non copre
        # nulla: ogni VAN negativo e NON_CONVIENTE.
        self.assertEqual(
            mh906_verdetto(-1.0, 0.10, 0.0, 44000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh906_verdetto(0.0, 0.10, 0.0, 44000.0),
            "MARGINALE")

    def test_valida_demo_ok(self):
        demo = mh906_demo()
        val = mh906_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_durata_intervallo(self):
        with self.assertRaises(ValueError):
            mh906_calcola(**_demo_kwargs(durata_anni=-1))
        with self.assertRaises(ValueError):
            mh906_calcola(**_demo_kwargs(durata_anni=2.5))
        bc = mh906_calcola(**_demo_kwargs(durata_anni=0))
        self.assertEqual(bc["durata_anni"], 0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh906_calcola(**_demo_kwargs(durata_anni=3))
        self.assertEqual(bc["durata_anni"], 3)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_valida_risparmio_zero_ammesso(self):
        demo = mh906_demo()
        val = mh906_valida(*[dict(demo, risparmio_mwh=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh906_calcola(**_demo_kwargs(risparmio_mwh=0.0))
        self.assertEqual(bc["tee_annui"], 0.0)
        self.assertIsNone(bc["be_prezzo_eur_tee"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_prezzo_zero_ammesso(self):
        demo = mh906_demo()
        val = mh906_valida(*[dict(demo, prezzo_tee_eur=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh906_calcola(**_demo_kwargs(prezzo_tee_eur=0.0))
        self.assertEqual(bc["ricavo_eur_anno"], 0.0)
        self.assertIsNone(bc["be_risparmio_mwh_anno"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_capex_zero_ammesso(self):
        demo = mh906_demo()
        val = mh906_valida(*[dict(demo, capex_eur=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh906_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["payback_anni"], 0)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_tasso_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh906_calcola(**_demo_kwargs(tasso_frazione=1.5))
        bc = mh906_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertEqual(bc["tasso_frazione"], 0.0)
        bc = mh906_calcola(**_demo_kwargs(tasso_frazione=1.0))
        self.assertEqual(bc["tasso_frazione"], 1.0)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh906_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh906_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_tee_eur=float("nan"))
        self.assertRaises(ValueError, mh906_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh906_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("risparmio_mwh", -1),
                              ("prezzo_tee_eur", -1),
                              ("durata_anni", -1),
                              ("capex_eur", -1),
                              ("om_eur_anno", -1),
                              ("certificazione_eur_anno", -1),
                              ("tasso_frazione", -0.1),
                              ("tol_frazione", -0.1),
                              ("fattore_co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh906_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh906_calcola(mh906_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh906_calcola(dict(mh906_demo(),
                                prezzo_tee_eur=999.0),
                           prezzo_tee_eur=260.0)
        self.assertEqual(bc["prezzo_tee_eur"], 260.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh906_calcola(_scenari=False, **mh906_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van_eur"], 70496.97, places=2)
        self.assertAlmostEqual(bc["be_prezzo_eur_tee"], 40.0,
                               places=2)


class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo_scalari(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO_SCALARI.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, (int, str)):
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
        self.assertGreater(bc["van_eur"], 0.0)
        self.assertAlmostEqual(bc["tir_frazione"], 0.2432,
                               places=4)
        self.assertAlmostEqual(bc["be_prezzo_eur_tee"], 40.0,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               357.85, places=2)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["payback_anni"], 3)
        self.assertAlmostEqual(bc["co2_t_anno"], 581.5,
                               places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["tee_annui"],
            bc["risparmio_mwh"] / 11.63)
        self.assertAlmostEqual(
            bc["risparmio_tep"],
            bc["risparmio_mwh"] / 11.63)
        self.assertAlmostEqual(
            bc["ricavo_eur_anno"],
            bc["tee_annui"] * bc["prezzo_tee_eur"])
        self.assertAlmostEqual(
            bc["costo_annuo_eur"],
            bc["om_eur_anno"]
            + bc["certificazione_eur_anno"])
        self.assertAlmostEqual(
            bc["margine_eur_anno"],
            bc["ricavo_eur_anno"] - bc["costo_annuo_eur"])
        self.assertAlmostEqual(
            bc["van_eur"],
            -bc["capex_eur"] + bc["margine_eur_anno"]
            * mh906_annuity(bc["durata_anni"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["be_prezzo_eur_tee"],
            bc["costo_annuo_eur"] / bc["tee_annui"])
        self.assertAlmostEqual(
            bc["be_risparmio_mwh_anno"],
            bc["costo_annuo_eur"] * 11.63
            / bc["prezzo_tee_eur"])
        self.assertAlmostEqual(
            bc["co2_t_anno"],
            bc["risparmio_mwh"]
            * bc["fattore_co2_t_mwh"])
        self.assertAlmostEqual(
            bc["payback_fraz_anni"],
            bc["capex_eur"] / bc["margine_eur_anno"])
        conf = bc["confronto"]
        self.assertEqual(conf["van_eur"], bc["van_eur"])
        self.assertEqual(conf["tir_frazione"],
                         bc["tir_frazione"])
        self.assertEqual(conf["payback_anni"],
                         bc["payback_anni"])
        self.assertEqual(conf["verdetto"], bc["verdetto"])
        # Flussi: anno zero meno CAPEX, poi margine
        # per ogni anno incentivato; il cumulato
        # supera il CAPEX al terzo anno.
        fl = bc["df_flussi"]
        self.assertEqual(len(fl), 6)
        self.assertEqual(fl["Flusso (EUR)"].iloc[0], -120000.0)
        self.assertEqual(fl["Flusso (EUR)"].iloc[1], 44000.0)
        self.assertEqual(fl["Cumulato (EUR)"].iloc[2], -32000.0)
        self.assertEqual(fl["Cumulato (EUR)"].iloc[3], 12000.0)
        self.assertEqual(fl["Cumulato (EUR)"].iloc[5], 100000.0)

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu prezzo TEE migliora il caso e resta
        # CONVIENTE; il breakeven prezzo TEE e
        # INVARIANTE al prezzo TEE corrente.
        self.assertGreater(
            bc["scenari"][1]["van_eur"], base["van_eur"])
        self.assertGreater(bc["scenari"][1]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][1]["be_prezzo_eur_tee"],
                         base["be_prezzo_eur_tee"])
        self.assertLess(
            bc["scenari"][1]["be_risparmio_mwh_anno"],
            base["be_risparmio_mwh_anno"])
        # Meno prezzo TEE peggiora il caso ma resta
        # CONVIENTE, con payback piu lungo.
        self.assertLess(bc["scenari"][2]["van_eur"],
                        base["van_eur"])
        self.assertGreater(bc["scenari"][2]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][2]["payback_anni"], 5)
        self.assertEqual(bc["scenari"][2]["be_prezzo_eur_tee"],
                         base["be_prezzo_eur_tee"])
        # Risparmio meno 20 per cento dimezza quasi
        # il VAN ma resta CONVIENTE.
        self.assertAlmostEqual(bc["scenari"][3]["tee_annui"],
                               160.0, places=9)
        self.assertAlmostEqual(bc["scenari"][3]["co2_t_anno"],
                               465.2, places=2)
        self.assertLess(bc["scenari"][3]["van_eur"],
                        base["van_eur"])
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][3]["payback_anni"], 4)
        # Durata 3 anni: VAN appena negativo e
        # verdetto MARGINALE.
        self.assertLess(bc["scenari"][4]["van_eur"], 0.0)
        self.assertGreater(bc["scenari"][4]["van_eur"], -1000.0)
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["scenari"][4]["payback_anni"], 3)

    def test_sensibilita_valori(self):
        s = mh906_sensibilita(**mh906_demo())
        self.assertEqual(set(s.keys()),
                         {"tee_piu30", "tee_meno30",
                          "risp_meno20", "durata_3",
                          "prezzo_be", "prezzo_030",
                          "risp_000", "prezzo_000",
                          "durata_0", "capex_0",
                          "om_zero", "cert_zero",
                          "tasso_0", "tasso_10",
                          "tol_zero", "co2_zero"})
        attesi = {
            "tee_piu30": (138036.81, 40.64, 3, 40.0, 275.27,
                          "CONVIENTE"),
            "tee_meno30": (2957.14, 5.89, 5, 40.0, 511.21,
                           "CONVIENTE"),
            "risp_meno20": (25470.42, 12.38, 4, 50.0, 357.85,
                            "CONVIENTE"),
            "durata_3": (-177.09, 4.92, 3, 40.0, 357.85,
                         "MARGINALE"),
            "prezzo_be": (-120000.0, None, None, 40.0, 2326.0,
                          "NON_CALCOLABILE"),
            "prezzo_030": (-128658.95, None, None, 40.0, 3101.33,
                           "NON_CALCOLABILE"),
            "risp_000": (-154635.81, None, None, None, 357.85,
                         "NON_CALCOLABILE"),
            "prezzo_000": (-154635.81, None, None, 40.0, None,
                           "NON_CALCOLABILE"),
            "durata_0": (-120000.0, None, None, 40.0, 357.85,
                         "NON_CONVIENTE"),
            "capex_0": (190496.97, None, 0, 40.0, 357.85,
                        "CONVIENTE"),
            "om_zero": (92144.36, 29.71, 3, 15.0, 134.19,
                        "CONVIENTE"),
            "cert_zero": (83485.40, 27.58, 3, 25.0, 223.65,
                          "CONVIENTE"),
            "tasso_0": (100000.0, 24.32, 3, 40.0, 357.85,
                        "CONVIENTE"),
            "tasso_10": (46794.62, 24.32, 3, 40.0, 357.85,
                         "CONVIENTE"),
            "tol_zero": (70496.97, 24.32, 3, 40.0, 357.85,
                         "CONVIENTE"),
            "co2_zero": (70496.97, 24.32, 3, 40.0, 357.85,
                         "CONVIENTE"),
        }
        for nome, (van, tirp, pb, bp, br, vdc) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(s[nome]["van_eur"], van,
                                       places=2)
                if tirp is None:
                    self.assertIsNone(s[nome]["tir_frazione"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["tir_frazione"] * 100.0, tirp,
                        places=2)
                self.assertEqual(s[nome]["payback_anni"], pb)
                if bp is None:
                    self.assertIsNone(
                        s[nome]["be_prezzo_eur_tee"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_prezzo_eur_tee"], bp,
                        places=2)
                if br is None:
                    self.assertIsNone(
                        s[nome]["be_risparmio_mwh_anno"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_risparmio_mwh_anno"], br,
                        places=2)
                self.assertEqual(s[nome]["verdetto"], vdc)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van_eur", caso)
            self.assertIn("tir_frazione", caso)
            self.assertIn("payback_anni", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)


class TestCasiLimite(unittest.TestCase):
    def test_risparmio_zero_non_calcolabile(self):
        bc = mh906_calcola(**_demo_kwargs(risparmio_mwh=0.0))
        self.assertEqual(bc["tee_annui"], 0.0)
        self.assertEqual(bc["ricavo_eur_anno"], 0.0)
        self.assertEqual(bc["costo_annuo_eur"], 8000.0)
        self.assertEqual(bc["margine_eur_anno"], -8000.0)
        self.assertAlmostEqual(bc["van_eur"], -154635.81,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["be_prezzo_eur_tee"])
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               357.85, places=2)
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_zero_non_calcolabile(self):
        bc = mh906_calcola(**_demo_kwargs(prezzo_tee_eur=0.0))
        self.assertEqual(bc["tee_annui"], 200.0)
        self.assertEqual(bc["ricavo_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], -8000.0)
        self.assertAlmostEqual(bc["van_eur"], -154635.81,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertAlmostEqual(bc["be_prezzo_eur_tee"], 40.0,
                               places=2)
        self.assertIsNone(bc["be_risparmio_mwh_anno"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_margine_zero_non_calcolabile(self):
        bc = mh906_calcola(**_demo_kwargs(prezzo_tee_eur=40.0))
        self.assertEqual(bc["ricavo_eur_anno"], 8000.0)
        self.assertEqual(bc["margine_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van_eur"], -120000.0,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               2326.0, places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_margine_negativo_non_calcolabile(self):
        bc = mh906_calcola(**_demo_kwargs(prezzo_tee_eur=30.0))
        self.assertEqual(bc["ricavo_eur_anno"], 6000.0)
        self.assertEqual(bc["margine_eur_anno"], -2000.0)
        self.assertAlmostEqual(bc["van_eur"], -128658.95,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               3101.33, places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_durata_zero_non_conviente(self):
        bc = mh906_calcola(**_demo_kwargs(durata_anni=0))
        self.assertEqual(bc["tee_annui"], 200.0)
        self.assertEqual(bc["margine_eur_anno"], 44000.0)
        self.assertEqual(bc["van_eur"], -120000.0)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["df_flussi"]), 1)

    def test_capex_zero_conviente_payback_zero(self):
        bc = mh906_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["margine_eur_anno"], 44000.0)
        self.assertAlmostEqual(bc["van_eur"], 190496.97,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["payback_anni"], 0)
        self.assertEqual(bc["payback_fraz_anni"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_om_zero_e_cert_zero(self):
        bc = mh906_calcola(**_demo_kwargs(om_eur_anno=0.0))
        self.assertEqual(bc["costo_annuo_eur"], 3000.0)
        self.assertEqual(bc["margine_eur_anno"], 49000.0)
        self.assertAlmostEqual(bc["van_eur"], 92144.36,
                               places=2)
        self.assertAlmostEqual(bc["be_prezzo_eur_tee"], 15.0,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               134.19, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh906_calcola(
            **_demo_kwargs(certificazione_eur_anno=0.0))
        self.assertEqual(bc["costo_annuo_eur"], 5000.0)
        self.assertEqual(bc["margine_eur_anno"], 47000.0)
        self.assertAlmostEqual(bc["van_eur"], 83485.40,
                               places=2)
        self.assertAlmostEqual(bc["be_prezzo_eur_tee"], 25.0,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_mwh_anno"],
                               223.65, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero_e_dieci(self):
        bc = mh906_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 100000.0,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.2432,
                               places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh906_calcola(**_demo_kwargs(tasso_frazione=0.10))
        self.assertAlmostEqual(bc["van_eur"], 46794.62,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.2432,
                               places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tolleranza_zero_demo_resta_conveniente(self):
        # Con VAN positivo la tolleranza non
        # decide nulla: il demo resta CONVIENTE
        # anche a tolleranza zero.
        bc = mh906_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 70496.97,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_van_invarianze(self):
        # Il VAN non dipende dal fattore CO2: la
        # CO2 non entra nell'economia.
        bc = demo_calcoli()
        bc_c = mh906_calcola(
            **_demo_kwargs(fattore_co2_t_mwh=0.0))
        self.assertEqual(bc_c["van_eur"], bc["van_eur"])
        self.assertEqual(bc_c["co2_t_anno"], 0.0)
        # Il VAN non dipende dalla tolleranza.
        bc_t = mh906_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc_t["van_eur"], bc["van_eur"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh906_csv(bc, mh906_demo())
        for voce in ("risparmio_mwh",
                     "prezzo_tee_eur",
                     "durata_anni",
                     "capex_eur",
                     "om_eur_anno",
                     "certificazione_eur_anno",
                     "tasso_frazione",
                     "tol_frazione",
                     "fattore_co2_t_mwh",
                     "tee_annui",
                     "risparmio_tep",
                     "ricavo_eur_anno",
                     "costo_annuo_eur",
                     "margine_eur_anno",
                     "van_eur",
                     "tir_frazione",
                     "payback_anni",
                     "payback_fraz_anni",
                     "be_prezzo_eur_tee",
                     "be_risparmio_mwh_anno",
                     "co2_t_anno",
                     "scenario_base_tee_annui",
                     "scenario_base_van_eur",
                     "scenario_base_verdetto",
                     "scenario_tee_piu30_van_eur",
                     "scenario_tee_piu30_verdetto",
                     "scenario_tee_meno30_van_eur",
                     "scenario_tee_meno30_verdetto",
                     "scenario_risp_meno20_van_eur",
                     "scenario_risp_meno20_verdetto",
                     "scenario_durata_3_van_eur",
                     "scenario_durata_3_verdetto",
                     "confronto_tee_annui",
                     "confronto_ricavo_eur_anno",
                     "confronto_costo_annuo_eur",
                     "confronto_margine_eur_anno",
                     "confronto_van_eur",
                     "confronto_tir_frazione",
                     "confronto_payback_anni",
                     "confronto_be_prezzo_eur_tee",
                     "confronto_be_risparmio_mwh_anno",
                     "confronto_co2_t_anno",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh906_csv(bc, mh906_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("risparmio_mwh;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh906_demo_calcoli()["van_eur"],
                         demo_calcoli()["van_eur"])
        self.assertEqual(mh906_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_scenari_confronto_tabella_flussi(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 11)
        self.assertEqual(len(bc["df_tabella"]), 22)
        self.assertEqual(len(bc["df_flussi"]), 6)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["TEE annui",
             "Ricavo annuo (EUR/anno)",
             "Costo annuo (EUR/anno)",
             "Margine netto annuo (EUR/anno)",
             "VAN (EUR)",
             "TIR (frazione)",
             "Payback (anni)",
             "Breakeven prezzo TEE (EUR/TEE)",
             "Breakeven risparmio (MWh/anno)",
             "CO2 evitata (t/anno)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            200.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[4],
            70496.97, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Risparmio energetico (MWh/anno)", voci)
        self.assertIn("Prezzo TEE (EUR/TEE)", voci)
        self.assertIn("Breakeven prezzo TEE (EUR/TEE)", voci)
        self.assertIn("Breakeven risparmio (MWh/anno)", voci)
        self.assertIn("VAN (EUR)", voci)
        self.assertIn("TIR (frazione)", voci)
        self.assertIn("Payback (anni)", voci)
        self.assertIn("CO2 evitata (t/anno)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("TIR (%)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto",
                      set(bc["df_scenari"].columns))
        self.assertIn("Payback (anni)",
                      set(bc["df_scenari"].columns))
        self.assertAlmostEqual(
            bc["df_scenari"]["VAN (EUR)"].iloc[0],
            70496.97, places=2)
        self.assertAlmostEqual(
            bc["df_scenari"]["TIR (%)"].iloc[0],
            24.32, places=2)
        self.assertEqual(
            list(bc["df_flussi"].columns),
            ["Anno", "Flusso (EUR)", "Cumulato (EUR)"])

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(risparmio_mwh="2326.0")
        self.assertRaises(ValueError, mh906_calcola, **kw)
        kw = _demo_kwargs(risparmio_mwh=True)
        self.assertRaises(ValueError, mh906_calcola, **kw)
        val = mh906_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def906\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh906_demo().keys()), lette - set(mh906_demo().keys()))
        self.assertEqual(lette, set(mh906_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc906\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc906\["([^"]+)"\]', src))
        attese = set(mh906_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 905 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 906.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 910)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab906:"), 1)
        self.assertTrue(src.startswith("    # W911"))

    def test_ui_tab906_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab906:"), 1)
        self.assertIn("def mh906_demo(", src_h)
        self.assertIn("def mh906_calcola(", src_h)
        self.assertIn("tab906", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Certificati Bianchi (TEE): il risparmio energetico si vende?", src)
        self.assertIn("🤍📜 Certificati Bianchi (TEE): il risparmio energetico si vende?", src)
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
        chiavi = re.findall(r'key="(st906_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st906_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 16)
        self.assertIn('key="st906_calcola"', src)
        self.assertIn('key="st906_csv"', src)
        self.assertIn('key="st906_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg906"), src.index(".paiac("))
        self.assertIn("st.stop()", src)

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

    def test_ui_nessun_residuo_sigla_vecchia(self):
        # Niente residui della sigla della scheda
        # precedente in helper e UI.
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            self.assertNotIn(_VECCHIO_SIGLA, src.lower())
            self.assertNotIn(_VECCHIO_SIGLA.upper(), src)


if __name__ == "__main__":
    unittest.main()
