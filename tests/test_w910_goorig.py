"""Test nuova scheda GO: il certificato
rinnovabile paga?
Repo path: tests/test_w910_goorig.py

Effetto ECONOMICO: una Garanzia di Origine
(GO) e un certificato che attesta che 1 MWh
di energia elettrica e stato prodotto da
fonte rinnovabile. La GO certifica l'origine
ma NON consegna energia: chi compra GO
compra solo il certificato, non i MWh fisici.
Chi copre il consumo con GO compra energia
grigia a prezzo grigio e GO separate a
prezzo GO, piu gestione; chi compra energia
verde bundled paga un prezzo verde unico,
piu gestione. Il costo della copertura
separata e costo grigio piu costo GO piu
gestione. Il costo bundled e consumo per
prezzo verde piu gestione. Il delta bundled
e costo bundled meno costo copertura:
positivo quando la separata conviene,
negativo quando il bundled conviene. La
sanzione evitata e GO necessarie per
sanzione. Il beneficio netto e sanzione
evitata meno costo GO meno gestione: se e
positivo, comprare GO paga. Il breakeven
prezzo GO e sanzione meno gestione diviso
GO necessarie: e il prezzo GO che azzera il
beneficio netto. Il breakeven prezzo verde
e prezzo grigio piu costo GO diviso consumo:
e il prezzo verde che azzera il delta
bundled; la gestione NON compare perche
compare sia nel bundled sia nella copertura
e si annulla nel delta.
Demo: consumo 10000 MWh, quota 100 per
cento, prezzo GO 4,50 EUR/MWh, prezzo
grigio 85,00 EUR/MWh, prezzo verde 92,00
EUR/MWh, gestione 5000 EUR/anno, sanzione
10,00 EUR/MWh, tolleranza 0,10 (frazione).
GO necessarie = 10000 per 100 diviso 100 =
10000 MWh. Costo GO = 10000 per 4,50 =
45.000 EUR. Costo grigio = 10000 per 85 =
850.000 EUR. Costo copertura = 850.000 piu
45.000 piu 5000 = 900.000 EUR. Costo bundled
= 10000 per 92 piu 5000 = 925.000 EUR.
Delta bundled = 925.000 meno 900.000 =
25.000 EUR (la separata conviene). Costo GO
per MWh = 45.000 diviso 10000 = 4,50
EUR/MWh. Premium verde = (45.000 piu 5000)
diviso 10000 = 5,00 EUR/MWh. Sanzione
evitata = 10000 per 10 = 100.000 EUR.
Beneficio netto = 100.000 meno 45.000 meno
5000 = 50.000 EUR. Breakeven prezzo GO = 10
meno 5000 diviso 10000 = 9,50 EUR/MWh.
Breakeven prezzo verde = 85 piu 45.000
diviso 10000 = 89,50 EUR/MWh. Grigia piu
sanzione = 850.000 piu 100.000 = 950.000
EUR. Verdetto CONVIENTE.
Scenari: base beneficio 50.000, breakeven
prezzo GO 9,50, breakeven prezzo verde
89,50, CONVIENTE; GO piu 50 % (prezzo GO
6,75) costo GO 67.500, costo copertura
922.500, delta bundled 2500, beneficio
27.500, breakeven prezzo verde 91,75,
CONVIENTE; GO meno 50 % (prezzo GO 2,25)
costo GO 22.500, costo copertura 877.500,
delta bundled 47.500, beneficio 72.500,
breakeven prezzo verde 87,25, CONVIENTE;
quota 50 % (GO necessarie 5000) costo GO
22.500, costo copertura 877.500, delta
bundled 47.500, sanzione evitata 50.000,
beneficio 22.500, breakeven prezzo GO 9,00,
breakeven prezzo verde 87,25, CONVIENTE;
prezzo verde 87 (bundled 875.000) delta
bundled meno 25.000 (il bundled conviene),
beneficio 50.000, breakeven prezzo verde
89,50, CONVIENTE.
Confronto: GO necessarie 10000 contro
costo GO 45.000, costo grigio 850.000
contro costo copertura 900.000, costo
bundled 925.000 contro delta bundled 25.000,
costo GO per MWh 4,50 contro premium verde
5,00, sanzione evitata 100.000 contro
beneficio netto 50.000, breakeven prezzo GO
9,50 contro breakeven prezzo verde 89,50.
Tolleranza in FRAZIONE (0,10 = 10 % della
sanzione evitata), usata diretta, NON divisa
per 100. Prezzo GO, prezzo grigio, prezzo
verde e sanzione medi annui costanti,
SEMPLIFICAZIONE DICHIARATA (il prezzo GO
oscilla con domanda e offerta di
certificati, il prezzo grigio segue il
mercato elettrico ora per ora, la sanzione
puo cambiare con la regolazione nel mondo
reale, qui valori medi costanti); la
gestione raccoglie i costi amministrativi
annui (registro, contrattualistica,
reportistica), SEMPLIFICAZIONE DICHIARATA.
Correzione rispetto al brief: il brief
indicava breakeven prezzo verde 90,00 con
la gestione nel conto; a 90,00 il delta
bundled e piu 5000, non zero, perche la
gestione compare sia nel bundled sia nella
copertura e si annulla nel delta: il valore
verificato e 89,50, e a 89,50 il delta e
zero (bundled 900.000 uguale alla
copertura). Tutti gli altri numeri del brief
sono confermati dal ricalcolo.
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se un input e
degenere (consumo nullo o negativo, quota
sotto 0 o sopra 100, prezzi negativi,
gestione negativa, sanzione negativa,
tolleranza negativa o sopra 1); altrimenti
CONVIENTE se il beneficio netto e maggiore
di 0, MARGINALE se il beneficio netto e
minore o uguale a 0 e il suo valore assoluto
e minore o uguale a tolleranza per sanzione
evitata, NON_CONVIENTE altrimenti. La quota
zero NON e degenere: da GO necessarie zero,
costo per MWh e breakeven prezzo GO None,
beneficio netto meno gestione e verdetto
NON_CONVIENTE.
Casi limite: quota zero (GO necessarie 0,
costo GO 0, sanzione evitata 0, beneficio
netto meno 5000, NON_CONVIENTE); sanzione
zero (sanzione evitata 0, beneficio netto
meno 50.000, breakeven prezzo GO meno 0,50,
NON_CONVIENTE); sanzione 5 (beneficio netto
0, breakeven prezzo GO 4,50, MARGINALE);
prezzo GO al breakeven 9,50 (beneficio netto
0, MARGINALE, breakeven prezzo verde 94,50);
prezzo verde al breakeven 89,50 (delta
bundled 0, beneficio netto 50.000,
CONVIENTE); gestione zero (beneficio netto
55.000, breakeven prezzo GO 10,00,
CONVIENTE); prezzo GO zero (beneficio netto
95.000, breakeven prezzo verde 85,00,
CONVIENTE); consumo 20000 (beneficio netto
105.000, breakeven prezzo GO 9,75,
CONVIENTE); consumo 1000 (beneficio netto
500, breakeven prezzo GO 5,00, CONVIENTE);
grigio 100 (delta bundled meno 125.000,
beneficio netto 50.000, CONVIENTE); grigio
70 (delta bundled 175.000, beneficio netto
50.000, CONVIENTE); tolleranza zero
(verdetto demo resta CONVIENTE).
Distinzione esplicita: qui SOLO la GO, il
certificato di origine (1 GO = 1 MWh
rinnovabile certificato, senza consegna di
energia; qui si comprano GO separate piu
energia grigia, oppure energia verde bundled
a prezzo unico), NIENTE VPPA (li il prezzo
fisso e su un contratto finanziario con
settlement sul mercato, qui si compra solo
il certificato), NIENTE PPA fisico (li si
ritira energia rinnovabile vera a prezzo
fisso, qui no: la GO non consegna energia),
NIENTE EAC o REC esteri (li i certificati
sono di altri sistemi e mercati, qui GO
europee), NIENTE GSE come controparte (il
GSE e il registro italiano che emette e
annulla le GO, qui il conto e dal lato di
chi compra le GO, non del registro).
Cancellazione e annullamento entro 12 mesi,
niente double counting: ogni MWh
rinnovabile puo generare una sola GO e una
GO annullata non si riusa.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w910_helpers import (
        demo_calcoli,
        mh905_be_go,
        mh905_be_verde,
        mh905_beneficio_netto,
        mh905_calcola,
        mh905_confronto,
        mh905_costo_bundled,
        mh905_costo_copertura,
        mh905_costo_go,
        mh905_costo_grigio,
        mh905_costo_per_mwh,
        mh905_csv,
        mh905_delta_bundled,
        mh905_demo,
        mh905_demo_calcoli,
        mh905_fraz,
        mh905_go_nec,
        mh905_nneg,
        mh905_num,
        mh905_pos,
        mh905_premium_verde,
        mh905_quota,
        mh905_sanzione_evitata,
        mh905_scenario,
        mh905_sensibilita,
        mh905_valida,
        mh905_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w910_helpers", os.path.join(_hf, "w910_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh905_be_go = _mod.mh905_be_go
    mh905_be_verde = _mod.mh905_be_verde
    mh905_beneficio_netto = _mod.mh905_beneficio_netto
    mh905_calcola = _mod.mh905_calcola
    mh905_confronto = _mod.mh905_confronto
    mh905_costo_bundled = _mod.mh905_costo_bundled
    mh905_costo_copertura = _mod.mh905_costo_copertura
    mh905_costo_go = _mod.mh905_costo_go
    mh905_costo_grigio = _mod.mh905_costo_grigio
    mh905_costo_per_mwh = _mod.mh905_costo_per_mwh
    mh905_csv = _mod.mh905_csv
    mh905_delta_bundled = _mod.mh905_delta_bundled
    mh905_demo = _mod.mh905_demo
    mh905_demo_calcoli = _mod.mh905_demo_calcoli
    mh905_fraz = _mod.mh905_fraz
    mh905_go_nec = _mod.mh905_go_nec
    mh905_nneg = _mod.mh905_nneg
    mh905_num = _mod.mh905_num
    mh905_pos = _mod.mh905_pos
    mh905_premium_verde = _mod.mh905_premium_verde
    mh905_quota = _mod.mh905_quota
    mh905_sanzione_evitata = _mod.mh905_sanzione_evitata
    mh905_scenario = _mod.mh905_scenario
    mh905_sensibilita = _mod.mh905_sensibilita
    mh905_valida = _mod.mh905_valida
    mh905_verdetto = _mod.mh905_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w910_helpers.py")
_UI_PATH = _risolvi("w910_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "4"
_VECCHIO_TAB = "tab90" + "4"
_VECCHIO_ST = "st90" + "4_"
_VECCHIO_SIGLA = "ft" + "r"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "go_nec_mwh": 10000.0,
    "costo_go_eur": 45000.0,
    "costo_grigio_eur": 850000.0,
    "costo_copertura_eur": 900000.0,
    "costo_bundled_eur": 925000.0,
    "delta_bundled_eur": 25000.0,
    "costo_per_mwh_eur_mwh": 4.5,
    "premium_verde_eur_mwh": 5.0,
    "sanzione_evitata_eur": 100000.0,
    "beneficio_netto_eur": 50000.0,
    "be_go_eur_mwh": 9.5,
    "be_verde_eur_mwh": 89.5,
    "grigia_piu_sanzione_eur": 950000.0,
    "verdetto": "CONVIENTE",
}

_DEMO_SCENARI = [
    {"nome": "Base", "quota_pct": 100.0,
     "prezzo_go_eur_mwh": 4.5,
     "prezzo_verde_eur_mwh": 92.0,
     "go_nec_mwh": 10000.0,
     "costo_go_eur": 45000.0,
     "costo_copertura_eur": 900000.0,
     "costo_bundled_eur": 925000.0,
     "delta_bundled_eur": 25000.0,
     "sanzione_evitata_eur": 100000.0,
     "beneficio_netto_eur": 50000.0,
     "be_go_eur_mwh": 9.5,
     "be_verde_eur_mwh": 89.5,
     "verdetto": "CONVIENTE"},
    {"nome": "GO piu 50 %", "quota_pct": 100.0,
     "prezzo_go_eur_mwh": 6.75,
     "prezzo_verde_eur_mwh": 92.0,
     "go_nec_mwh": 10000.0,
     "costo_go_eur": 67500.0,
     "costo_copertura_eur": 922500.0,
     "costo_bundled_eur": 925000.0,
     "delta_bundled_eur": 2500.0,
     "sanzione_evitata_eur": 100000.0,
     "beneficio_netto_eur": 27500.0,
     "be_go_eur_mwh": 9.5,
     "be_verde_eur_mwh": 91.75,
     "verdetto": "CONVIENTE"},
    {"nome": "GO meno 50 %", "quota_pct": 100.0,
     "prezzo_go_eur_mwh": 2.25,
     "prezzo_verde_eur_mwh": 92.0,
     "go_nec_mwh": 10000.0,
     "costo_go_eur": 22500.0,
     "costo_copertura_eur": 877500.0,
     "costo_bundled_eur": 925000.0,
     "delta_bundled_eur": 47500.0,
     "sanzione_evitata_eur": 100000.0,
     "beneficio_netto_eur": 72500.0,
     "be_go_eur_mwh": 9.5,
     "be_verde_eur_mwh": 87.25,
     "verdetto": "CONVIENTE"},
    {"nome": "Quota 50 %", "quota_pct": 50.0,
     "prezzo_go_eur_mwh": 4.5,
     "prezzo_verde_eur_mwh": 92.0,
     "go_nec_mwh": 5000.0,
     "costo_go_eur": 22500.0,
     "costo_copertura_eur": 877500.0,
     "costo_bundled_eur": 925000.0,
     "delta_bundled_eur": 47500.0,
     "sanzione_evitata_eur": 50000.0,
     "beneficio_netto_eur": 22500.0,
     "be_go_eur_mwh": 9.0,
     "be_verde_eur_mwh": 87.25,
     "verdetto": "CONVIENTE"},
    {"nome": "Verde 87", "quota_pct": 100.0,
     "prezzo_go_eur_mwh": 4.5,
     "prezzo_verde_eur_mwh": 87.0,
     "go_nec_mwh": 10000.0,
     "costo_go_eur": 45000.0,
     "costo_copertura_eur": 900000.0,
     "costo_bundled_eur": 875000.0,
     "delta_bundled_eur": -25000.0,
     "sanzione_evitata_eur": 100000.0,
     "beneficio_netto_eur": 50000.0,
     "be_go_eur_mwh": 9.5,
     "be_verde_eur_mwh": 89.5,
     "verdetto": "CONVIENTE"},
]

_DEMO_CONFRONTO = {
    "go_nec_mwh": 10000.0,
    "costo_go_eur": 45000.0,
    "costo_grigio_eur": 850000.0,
    "costo_copertura_eur": 900000.0,
    "costo_bundled_eur": 925000.0,
    "delta_bundled_eur": 25000.0,
    "costo_per_mwh_eur_mwh": 4.5,
    "premium_verde_eur_mwh": 5.0,
    "sanzione_evitata_eur": 100000.0,
    "beneficio_netto_eur": 50000.0,
    "be_go_eur_mwh": 9.5,
    "be_verde_eur_mwh": 89.5,
    "verdetto": "CONVIENTE",
}

_ORDINE_VALIDA = (
    "consumo_mwh", "quota_pct", "prezzo_go_eur_mwh",
    "prezzo_grigio_eur_mwh", "prezzo_verde_eur_mwh",
    "gestione_eur_anno", "sanzione_eur_mwh",
    "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh905_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh905_num(3, "x"), 3.0)
        self.assertEqual(mh905_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh905_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh905_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh905_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh905_pos(0, "x")
        with self.assertRaises(ValueError):
            mh905_pos(-1, "x")
        self.assertEqual(mh905_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh905_fraz(0, "x"), 0.0)
        self.assertEqual(mh905_fraz(1, "x"), 1.0)
        self.assertEqual(mh905_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh905_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh905_fraz(1.01, "x")

    def test_quota_bordi(self):
        self.assertEqual(mh905_quota(0, "x"), 0.0)
        self.assertEqual(mh905_quota(100, "x"), 100.0)
        self.assertEqual(mh905_quota(50.0, "x"), 50.0)
        self.assertEqual(mh905_quota(100.0, "x"), 100.0)
        with self.assertRaises(ValueError):
            mh905_quota(-0.01, "x")
        with self.assertRaises(ValueError):
            mh905_quota(100.01, "x")

    def test_quota_sopra_100_no(self):
        with self.assertRaises(ValueError):
            mh905_quota(101, "x")
        with self.assertRaises(ValueError):
            mh905_quota(150, "x")
        with self.assertRaises(ValueError):
            mh905_quota(float("nan"), "x")


class TestFisica(unittest.TestCase):
    def test_go_nec(self):
        self.assertEqual(mh905_go_nec(10000.0, 100.0), 10000.0)
        self.assertEqual(mh905_go_nec(10000.0, 50.0), 5000.0)
        self.assertEqual(mh905_go_nec(10000.0, 0.0), 0.0)
        self.assertEqual(mh905_go_nec(20000.0, 100.0), 20000.0)
        self.assertEqual(mh905_go_nec(1000.0, 100.0), 1000.0)
        self.assertEqual(mh905_go_nec(10000.0, 25.0), 2500.0)
        with self.assertRaises(ValueError):
            mh905_go_nec(0.0, 100.0)
        with self.assertRaises(ValueError):
            mh905_go_nec(10000.0, 101.0)
        with self.assertRaises(ValueError):
            mh905_go_nec(10000.0, -1.0)

    def test_costo_go(self):
        self.assertEqual(mh905_costo_go(10000.0, 4.5), 45000.0)
        self.assertEqual(mh905_costo_go(10000.0, 6.75), 67500.0)
        self.assertEqual(mh905_costo_go(10000.0, 2.25), 22500.0)
        self.assertEqual(mh905_costo_go(5000.0, 4.5), 22500.0)
        self.assertEqual(mh905_costo_go(0.0, 4.5), 0.0)
        self.assertEqual(mh905_costo_go(10000.0, 0.0), 0.0)
        self.assertEqual(mh905_costo_go(20000.0, 4.5), 90000.0)
        with self.assertRaises(ValueError):
            mh905_costo_go(-1.0, 4.5)
        with self.assertRaises(ValueError):
            mh905_costo_go(10000.0, -1.0)

    def test_costo_grigio(self):
        self.assertEqual(mh905_costo_grigio(10000.0, 85.0), 850000.0)
        self.assertEqual(mh905_costo_grigio(10000.0, 100.0), 1000000.0)
        self.assertEqual(mh905_costo_grigio(10000.0, 70.0), 700000.0)
        self.assertEqual(mh905_costo_grigio(20000.0, 85.0), 1700000.0)
        self.assertEqual(mh905_costo_grigio(10000.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh905_costo_grigio(0.0, 85.0)
        with self.assertRaises(ValueError):
            mh905_costo_grigio(10000.0, -1.0)

    def test_costo_copertura(self):
        self.assertEqual(
            mh905_costo_copertura(850000.0, 45000.0, 5000.0),
            900000.0)
        self.assertEqual(
            mh905_costo_copertura(850000.0, 67500.0, 5000.0),
            922500.0)
        self.assertEqual(
            mh905_costo_copertura(850000.0, 22500.0, 5000.0),
            877500.0)
        self.assertEqual(
            mh905_costo_copertura(850000.0, 45000.0, 0.0),
            895000.0)
        self.assertEqual(
            mh905_costo_copertura(1000000.0, 45000.0, 5000.0),
            1050000.0)
        with self.assertRaises(ValueError):
            mh905_costo_copertura(-1.0, 45000.0, 5000.0)
        with self.assertRaises(ValueError):
            mh905_costo_copertura(850000.0, 45000.0, -1.0)

    def test_costo_bundled(self):
        self.assertEqual(
            mh905_costo_bundled(10000.0, 92.0, 5000.0), 925000.0)
        self.assertEqual(
            mh905_costo_bundled(10000.0, 87.0, 5000.0), 875000.0)
        self.assertEqual(
            mh905_costo_bundled(10000.0, 89.5, 5000.0), 900000.0)
        self.assertEqual(
            mh905_costo_bundled(10000.0, 92.0, 0.0), 920000.0)
        self.assertEqual(
            mh905_costo_bundled(20000.0, 92.0, 5000.0), 1845000.0)
        with self.assertRaises(ValueError):
            mh905_costo_bundled(0.0, 92.0, 5000.0)
        with self.assertRaises(ValueError):
            mh905_costo_bundled(10000.0, -1.0, 5000.0)

    def test_delta_bundled(self):
        self.assertEqual(
            mh905_delta_bundled(925000.0, 900000.0), 25000.0)
        self.assertEqual(
            mh905_delta_bundled(875000.0, 900000.0), -25000.0)
        self.assertEqual(
            mh905_delta_bundled(900000.0, 900000.0), 0.0)
        self.assertEqual(
            mh905_delta_bundled(925000.0, 922500.0), 2500.0)
        self.assertEqual(
            mh905_delta_bundled(925000.0, 877500.0), 47500.0)
        self.assertEqual(
            mh905_delta_bundled(925000.0, 1050000.0), -125000.0)

    def test_costo_per_mwh(self):
        self.assertEqual(mh905_costo_per_mwh(45000.0, 10000.0), 4.5)
        self.assertEqual(mh905_costo_per_mwh(67500.0, 10000.0), 6.75)
        self.assertEqual(mh905_costo_per_mwh(22500.0, 10000.0), 2.25)
        self.assertEqual(mh905_costo_per_mwh(0.0, 10000.0), 0.0)
        self.assertIsNone(mh905_costo_per_mwh(0.0, 0.0))
        self.assertIsNone(mh905_costo_per_mwh(45000.0, 0.0))
        with self.assertRaises(ValueError):
            mh905_costo_per_mwh(-1.0, 10000.0)

    def test_premium_verde(self):
        self.assertEqual(
            mh905_premium_verde(45000.0, 5000.0, 10000.0), 5.0)
        self.assertEqual(
            mh905_premium_verde(67500.0, 5000.0, 10000.0), 7.25)
        self.assertEqual(
            mh905_premium_verde(22500.0, 5000.0, 10000.0), 2.75)
        self.assertEqual(
            mh905_premium_verde(45000.0, 0.0, 10000.0), 4.5)
        self.assertEqual(
            mh905_premium_verde(0.0, 5000.0, 10000.0), 0.5)
        self.assertEqual(
            mh905_premium_verde(90000.0, 5000.0, 20000.0), 4.75)
        self.assertEqual(
            mh905_premium_verde(4500.0, 5000.0, 1000.0), 9.5)
        with self.assertRaises(ValueError):
            mh905_premium_verde(45000.0, 5000.0, 0.0)

    def test_premium_con_gestione_zero(self):
        # Con gestione zero il premium e solo il
        # prezzo GO: 4,50.
        self.assertEqual(
            mh905_premium_verde(45000.0, 0.0, 10000.0), 4.5)
        self.assertEqual(
            mh905_premium_verde(0.0, 0.0, 10000.0), 0.0)

    def test_sanzione_evitata(self):
        self.assertEqual(
            mh905_sanzione_evitata(10000.0, 10.0), 100000.0)
        self.assertEqual(
            mh905_sanzione_evitata(5000.0, 10.0), 50000.0)
        self.assertEqual(
            mh905_sanzione_evitata(10000.0, 5.0), 50000.0)
        self.assertEqual(
            mh905_sanzione_evitata(10000.0, 0.0), 0.0)
        self.assertEqual(
            mh905_sanzione_evitata(0.0, 10.0), 0.0)
        self.assertEqual(
            mh905_sanzione_evitata(20000.0, 10.0), 200000.0)
        with self.assertRaises(ValueError):
            mh905_sanzione_evitata(10000.0, -1.0)

    def test_beneficio_netto(self):
        self.assertEqual(
            mh905_beneficio_netto(100000.0, 45000.0, 5000.0),
            50000.0)
        self.assertEqual(
            mh905_beneficio_netto(100000.0, 67500.0, 5000.0),
            27500.0)
        self.assertEqual(
            mh905_beneficio_netto(100000.0, 22500.0, 5000.0),
            72500.0)
        self.assertEqual(
            mh905_beneficio_netto(50000.0, 22500.0, 5000.0),
            22500.0)
        self.assertEqual(
            mh905_beneficio_netto(0.0, 45000.0, 5000.0),
            -50000.0)
        self.assertEqual(
            mh905_beneficio_netto(0.0, 0.0, 5000.0),
            -5000.0)
        self.assertEqual(
            mh905_beneficio_netto(50000.0, 45000.0, 5000.0),
            0.0)

    def test_be_go(self):
        self.assertAlmostEqual(
            mh905_be_go(10.0, 5000.0, 10000.0), 9.50, places=2)
        self.assertAlmostEqual(
            mh905_be_go(10.0, 5000.0, 5000.0), 9.00, places=2)
        self.assertAlmostEqual(
            mh905_be_go(5.0, 5000.0, 10000.0), 4.50, places=2)
        self.assertAlmostEqual(
            mh905_be_go(10.0, 0.0, 10000.0), 10.00, places=2)
        self.assertAlmostEqual(
            mh905_be_go(0.0, 5000.0, 10000.0), -0.50, places=2)
        self.assertAlmostEqual(
            mh905_be_go(10.0, 5000.0, 20000.0), 9.75, places=2)
        self.assertAlmostEqual(
            mh905_be_go(10.0, 5000.0, 1000.0), 5.00, places=2)
        self.assertIsNone(mh905_be_go(10.0, 5000.0, 0.0))
        with self.assertRaises(ValueError):
            mh905_be_go(-1.0, 5000.0, 10000.0)
        # Al prezzo GO di breakeven il beneficio
        # netto e zero e il verdetto e MARGINALE.
        be = mh905_be_go(10.0, 5000.0, 10000.0)
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_go_eur_mwh=be))
        self.assertAlmostEqual(bc["beneficio_netto_eur"], 0.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 94.50,
                               places=2)

    def test_be_verde(self):
        self.assertAlmostEqual(
            mh905_be_verde(85.0, 45000.0, 10000.0), 89.50,
            places=2)
        self.assertAlmostEqual(
            mh905_be_verde(85.0, 67500.0, 10000.0), 91.75,
            places=2)
        self.assertAlmostEqual(
            mh905_be_verde(85.0, 22500.0, 10000.0), 87.25,
            places=2)
        self.assertAlmostEqual(
            mh905_be_verde(100.0, 45000.0, 10000.0), 104.50,
            places=2)
        self.assertAlmostEqual(
            mh905_be_verde(70.0, 45000.0, 10000.0), 74.50,
            places=2)
        self.assertAlmostEqual(
            mh905_be_verde(85.0, 0.0, 10000.0), 85.00,
            places=2)
        self.assertAlmostEqual(
            mh905_be_verde(85.0, 90000.0, 20000.0), 89.50,
            places=2)
        with self.assertRaises(ValueError):
            mh905_be_verde(85.0, 45000.0, 0.0)
        with self.assertRaises(ValueError):
            mh905_be_verde(-1.0, 45000.0, 10000.0)
        # Al prezzo verde di breakeven il delta
        # bundled e zero e il beneficio netto resta
        # 50.000 con verdetto CONVIENTE.
        bv = mh905_be_verde(85.0, 45000.0, 10000.0)
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_verde_eur_mwh=bv))
        self.assertAlmostEqual(bc["delta_bundled_eur"], 0.0,
                               places=2)
        self.assertAlmostEqual(bc["costo_bundled_eur"],
                               bc["costo_copertura_eur"])
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               50000.00, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_be_verde_senza_gestione(self):
        # La gestione NON compare nel breakeven
        # prezzo verde: con gestione zero e con
        # gestione 5000 il valore e lo stesso
        # 89,50, perche la gestione si annulla
        # nel delta bundled.
        bc0 = mh905_calcola(**_demo_kwargs(gestione_eur_anno=0.0))
        bc = demo_calcoli()
        self.assertAlmostEqual(bc0["be_verde_eur_mwh"],
                               bc["be_verde_eur_mwh"])
        self.assertAlmostEqual(bc0["be_verde_eur_mwh"], 89.50,
                               places=2)
        # CORREZIONE BRIEF: con la formula del
        # brief (con gestione) il valore sarebbe
        # 90,00, ma a 90,00 il delta e piu 5000.
        bc90 = mh905_calcola(
            **_demo_kwargs(prezzo_verde_eur_mwh=90.0))
        self.assertAlmostEqual(bc90["delta_bundled_eur"],
                               5000.00, places=2)
        self.assertNotAlmostEqual(bc90["delta_bundled_eur"],
                                  0.0, places=2)

    def test_be_go_negativo_sanzione_zero(self):
        # Con sanzione zero il breakeven prezzo GO
        # e negativo (meno 0,50): nemmeno con GO
        # gratis il beneficio diventa positivo.
        self.assertAlmostEqual(
            mh905_be_go(0.0, 5000.0, 10000.0), -0.50, places=2)
        bc = mh905_calcola(**_demo_kwargs(sanzione_eur_mwh=0.0))
        self.assertAlmostEqual(bc["be_go_eur_mwh"], -0.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_scenario_singolo(self):
        s = mh905_scenario("GO piu 50 %", mh905_demo(),
                           {"prezzo_go_eur_mwh": 6.75})
        self.assertEqual(s["nome"], "GO piu 50 %")
        self.assertEqual(s["prezzo_go_eur_mwh"], 6.75)
        self.assertAlmostEqual(s["beneficio_netto_eur"],
                               27500.00, places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        # Il breakeven prezzo GO e INVARIANTE al
        # prezzo GO corrente.
        self.assertAlmostEqual(s["be_go_eur_mwh"], 9.50,
                               places=2)
        self.assertAlmostEqual(s["be_verde_eur_mwh"], 91.75,
                               places=2)
        s = mh905_scenario("GO meno 50 %", mh905_demo(),
                           {"prezzo_go_eur_mwh": 2.25})
        self.assertAlmostEqual(s["beneficio_netto_eur"],
                               72500.00, places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh905_scenario("Quota 50 %", mh905_demo(),
                           {"quota_pct": 50.0})
        self.assertEqual(s["go_nec_mwh"], 5000.0)
        self.assertAlmostEqual(s["beneficio_netto_eur"],
                               22500.00, places=2)
        self.assertAlmostEqual(s["be_go_eur_mwh"], 9.00,
                               places=2)
        s = mh905_scenario("Verde 87", mh905_demo(),
                           {"prezzo_verde_eur_mwh": 87.0})
        self.assertAlmostEqual(s["delta_bundled_eur"],
                               -25000.00, places=2)
        self.assertAlmostEqual(s["beneficio_netto_eur"],
                               50000.00, places=2)
        # Il breakeven prezzo verde e INVARIANTE
        # al prezzo verde corrente.
        self.assertAlmostEqual(s["be_verde_eur_mwh"], 89.50,
                               places=2)
        with self.assertRaises(ValueError):
            mh905_scenario("", mh905_demo(),
                           {"prezzo_go_eur_mwh": 6.75})
        with self.assertRaises(ValueError):
            mh905_scenario("X", mh905_demo(),
                           {"quota_pct": 101.0})

    def test_scenario_quota_zero(self):
        s = mh905_scenario("Quota 0", mh905_demo(),
                           {"quota_pct": 0.0})
        self.assertEqual(s["go_nec_mwh"], 0.0)
        self.assertEqual(s["costo_go_eur"], 0.0)
        self.assertEqual(s["sanzione_evitata_eur"], 0.0)
        self.assertEqual(s["beneficio_netto_eur"], -5000.0)
        self.assertIsNone(s["costo_per_mwh_eur_mwh"])
        self.assertIsNone(s["be_go_eur_mwh"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")

    def test_confronto_formule(self):
        c = mh905_confronto(10000.0, 45000.0, 850000.0,
                            900000.0, 925000.0, 25000.0,
                            4.5, 5.0, 100000.0, 50000.0,
                            9.5, 89.5, "CONVIENTE")
        self.assertEqual(c["go_nec_mwh"], 10000.0)
        self.assertEqual(c["costo_go_eur"], 45000.0)
        self.assertEqual(c["costo_grigio_eur"], 850000.0)
        self.assertEqual(c["costo_copertura_eur"], 900000.0)
        self.assertEqual(c["costo_bundled_eur"], 925000.0)
        self.assertEqual(c["delta_bundled_eur"], 25000.0)
        self.assertEqual(c["costo_per_mwh_eur_mwh"], 4.5)
        self.assertEqual(c["premium_verde_eur_mwh"], 5.0)
        self.assertEqual(c["sanzione_evitata_eur"], 100000.0)
        self.assertEqual(c["beneficio_netto_eur"], 50000.0)
        self.assertEqual(c["be_go_eur_mwh"], 9.5)
        self.assertEqual(c["be_verde_eur_mwh"], 89.5)
        self.assertEqual(c["verdetto"], "CONVIENTE")
        c = mh905_confronto(0.0, 0.0, 850000.0,
                            855000.0, 925000.0, 70000.0,
                            None, 0.5, 0.0, -5000.0,
                            None, 85.0, "NON_CONVIENTE")
        self.assertIsNone(c["costo_per_mwh_eur_mwh"])
        self.assertIsNone(c["be_go_eur_mwh"])
        self.assertEqual(c["verdetto"], "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh905_confronto(10000.0, 45000.0, 850000.0,
                            900000.0, 925000.0, 25000.0,
                            4.5, 5.0, 100000.0, 50000.0,
                            9.5, 89.5, "FORSE")
        with self.assertRaises(ValueError):
            mh905_confronto(10000.0, -1.0, 850000.0,
                            900000.0, 925000.0, 25000.0,
                            4.5, 5.0, 100000.0, 50000.0,
                            9.5, 89.5, "CONVIENTE")


class TestFinanza(unittest.TestCase):
    def test_verdetto_bordi(self):
        self.assertEqual(
            mh905_verdetto(100.0, 0.10, 100000.0), "CONVIENTE")
        self.assertEqual(
            mh905_verdetto(0.0, 0.10, 100000.0), "MARGINALE")
        self.assertEqual(
            mh905_verdetto(-10000.0, 0.10, 100000.0),
            "MARGINALE")
        self.assertEqual(
            mh905_verdetto(-10001.0, 0.10, 100000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh905_verdetto(-50000.0, 0.10, 100000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni beneficio
        # negativo e NON_CONVIENTE (beneficio zero
        # compreso nel MARGINALE solo perche il
        # valore assoluto zero e minore o uguale
        # a zero).
        self.assertEqual(
            mh905_verdetto(-1.0, 0.0, 100000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh905_verdetto(0.0, 0.0, 100000.0), "MARGINALE")
        with self.assertRaises(ValueError):
            mh905_verdetto(100.0, 1.5, 100000.0)
        with self.assertRaises(ValueError):
            mh905_verdetto(100.0, 0.10, -1.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh905_verdetto(None, 0.10, 100000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh905_verdetto(None, 0.0, 0.0), "NON_CALCOLABILE")

    def test_verdetto_sanzione_zero(self):
        # Con sanzione evitata zero la tolleranza
        # non copre nulla: ogni beneficio negativo
        # e NON_CONVIENTE, il beneficio zero e
        # MARGINALE.
        self.assertEqual(
            mh905_verdetto(-5000.0, 0.10, 0.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh905_verdetto(0.0, 0.10, 0.0), "MARGINALE")
        self.assertEqual(
            mh905_verdetto(-50000.0, 1.0, 0.0),
            "NON_CONVIENTE")

    def test_valida_demo_ok(self):
        demo = mh905_demo()
        val = mh905_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_quota_intervallo(self):
        with self.assertRaises(ValueError):
            mh905_calcola(**_demo_kwargs(quota_pct=-1.0))
        with self.assertRaises(ValueError):
            mh905_calcola(**_demo_kwargs(quota_pct=101.0))
        bc = mh905_calcola(**_demo_kwargs(quota_pct=0.0))
        self.assertEqual(bc["quota_pct"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh905_calcola(**_demo_kwargs(quota_pct=100.0))
        self.assertEqual(bc["quota_pct"], 100.0)
        bc = mh905_calcola(**_demo_kwargs(quota_pct=50.0))
        self.assertEqual(bc["go_nec_mwh"], 5000.0)

    def test_valida_quota_zero_ammessa(self):
        # La quota zero NON e degenere: e ammessa
        # in validazione e in calcolo.
        demo = mh905_demo()
        val = mh905_valida(*[dict(demo, quota_pct=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh905_calcola(**_demo_kwargs(quota_pct=0.0))
        self.assertIsNone(bc["costo_per_mwh_eur_mwh"])
        self.assertIsNone(bc["be_go_eur_mwh"])

    def test_valida_sanzione_zero_ammessa(self):
        demo = mh905_demo()
        val = mh905_valida(*[dict(demo, sanzione_eur_mwh=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh905_calcola(**_demo_kwargs(sanzione_eur_mwh=0.0))
        self.assertEqual(bc["sanzione_evitata_eur"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh905_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh905_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        bc = mh905_calcola(**_demo_kwargs(tol_frazione=1.0))
        self.assertEqual(bc["tol_frazione"], 1.0)

    def test_valida_consumo_zero_no(self):
        with self.assertRaises(ValueError):
            mh905_calcola(**_demo_kwargs(consumo_mwh=0.0))
        with self.assertRaises(ValueError):
            mh905_calcola(**_demo_kwargs(consumo_mwh=-100.0))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_go_eur_mwh=float("nan"))
        self.assertRaises(ValueError, mh905_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh905_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("consumo_mwh", -1),
                              ("quota_pct", -1),
                              ("prezzo_go_eur_mwh", -1),
                              ("prezzo_grigio_eur_mwh", -1),
                              ("prezzo_verde_eur_mwh", -1),
                              ("gestione_eur_anno", -1),
                              ("sanzione_eur_mwh", -1),
                              ("tol_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh905_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh905_calcola(mh905_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh905_calcola(dict(mh905_demo(),
                                prezzo_go_eur_mwh=999.0),
                           prezzo_go_eur_mwh=4.5)
        self.assertEqual(bc["prezzo_go_eur_mwh"], 4.5)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh905_calcola(_scenari=False, **mh905_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               50000.00, places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 89.50,
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
        self.assertGreater(bc["beneficio_netto_eur"], 0.0)
        self.assertAlmostEqual(bc["be_go_eur_mwh"], 9.50,
                               places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 89.50,
                               places=2)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertAlmostEqual(bc["delta_bundled_eur"],
                               25000.00, places=2)
        self.assertAlmostEqual(bc["grigia_piu_sanzione_eur"],
                               950000.00, places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["go_nec_mwh"],
            bc["consumo_mwh"] * bc["quota_pct"] / 100.0)
        self.assertAlmostEqual(
            bc["costo_go_eur"],
            bc["go_nec_mwh"] * bc["prezzo_go_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_grigio_eur"],
            bc["consumo_mwh"] * bc["prezzo_grigio_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_copertura_eur"],
            bc["costo_grigio_eur"] + bc["costo_go_eur"]
            + bc["gestione_eur_anno"])
        self.assertAlmostEqual(
            bc["costo_bundled_eur"],
            bc["consumo_mwh"] * bc["prezzo_verde_eur_mwh"]
            + bc["gestione_eur_anno"])
        self.assertAlmostEqual(
            bc["delta_bundled_eur"],
            bc["costo_bundled_eur"]
            - bc["costo_copertura_eur"])
        self.assertAlmostEqual(
            bc["costo_per_mwh_eur_mwh"],
            bc["costo_go_eur"] / bc["go_nec_mwh"])
        self.assertAlmostEqual(
            bc["premium_verde_eur_mwh"],
            (bc["costo_go_eur"] + bc["gestione_eur_anno"])
            / bc["consumo_mwh"])
        self.assertAlmostEqual(
            bc["sanzione_evitata_eur"],
            bc["go_nec_mwh"] * bc["sanzione_eur_mwh"])
        self.assertAlmostEqual(
            bc["beneficio_netto_eur"],
            bc["sanzione_evitata_eur"] - bc["costo_go_eur"]
            - bc["gestione_eur_anno"])
        self.assertAlmostEqual(
            bc["be_go_eur_mwh"],
            bc["sanzione_eur_mwh"]
            - bc["gestione_eur_anno"] / bc["go_nec_mwh"])
        self.assertAlmostEqual(
            bc["be_verde_eur_mwh"],
            bc["prezzo_grigio_eur_mwh"]
            + bc["costo_go_eur"] / bc["consumo_mwh"])
        self.assertAlmostEqual(
            bc["grigia_piu_sanzione_eur"],
            bc["costo_grigio_eur"]
            + bc["sanzione_evitata_eur"])
        conf = bc["confronto"]
        self.assertEqual(conf["beneficio_netto_eur"],
                         bc["beneficio_netto_eur"])
        self.assertEqual(conf["be_go_eur_mwh"],
                         bc["be_go_eur_mwh"])
        self.assertEqual(conf["be_verde_eur_mwh"],
                         bc["be_verde_eur_mwh"])
        self.assertEqual(conf["verdetto"], bc["verdetto"])

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu prezzo GO peggiora il caso ma resta
        # CONVIENTE; il breakeven prezzo GO e
        # INVARIANTE al prezzo GO corrente.
        self.assertLess(bc["scenari"][1]["beneficio_netto_eur"],
                        base["beneficio_netto_eur"])
        self.assertGreater(bc["scenari"][1]["beneficio_netto_eur"],
                           0.0)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][1]["be_go_eur_mwh"],
                         base["be_go_eur_mwh"])
        self.assertGreater(
            bc["scenari"][1]["be_verde_eur_mwh"],
            base["be_verde_eur_mwh"])
        # Meno prezzo GO migliora il caso.
        self.assertGreater(
            bc["scenari"][2]["beneficio_netto_eur"],
            base["beneficio_netto_eur"])
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][2]["be_go_eur_mwh"],
                         base["be_go_eur_mwh"])
        # Quota 50 dimezza GO e sanzione evitata.
        self.assertEqual(bc["scenari"][3]["go_nec_mwh"], 5000.0)
        self.assertEqual(
            bc["scenari"][3]["sanzione_evitata_eur"], 50000.0)
        self.assertLess(bc["scenari"][3]["beneficio_netto_eur"],
                        base["beneficio_netto_eur"])
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        # Verde 87: il bundled conviene (delta
        # negativo) ma il beneficio netto non
        # cambia e resta CONVIENTE; il breakeven
        # prezzo verde e INVARIANTE al prezzo
        # verde corrente.
        self.assertLess(bc["scenari"][4]["delta_bundled_eur"],
                        0.0)
        self.assertEqual(bc["scenari"][4]["beneficio_netto_eur"],
                         base["beneficio_netto_eur"])
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][4]["be_verde_eur_mwh"],
                         base["be_verde_eur_mwh"])

    def test_scenario_verde87_delta_negativo(self):
        bc = demo_calcoli()
        verde87 = bc["scenari"][4]
        self.assertEqual(verde87["costo_bundled_eur"], 875000.0)
        self.assertEqual(verde87["costo_copertura_eur"],
                         900000.0)
        self.assertEqual(verde87["delta_bundled_eur"], -25000.0)
        self.assertEqual(verde87["prezzo_verde_eur_mwh"], 87.0)

    def test_sensibilita_valori(self):
        s = mh905_sensibilita(**mh905_demo())
        self.assertEqual(set(s.keys()),
                         {"go_piu50", "go_meno50",
                          "quota_050", "verde_087",
                          "grigio_100", "grigio_070",
                          "sanzione_005", "sanzione_000",
                          "gestione_zero", "prezzo_go_000",
                          "consumo_20000", "consumo_1000",
                          "quota_000", "tol_zero",
                          "go_be", "verde_be"})
        attesi = {
            "go_piu50": (27500.0, 9.5, 91.75, "CONVIENTE"),
            "go_meno50": (72500.0, 9.5, 87.25, "CONVIENTE"),
            "quota_050": (22500.0, 9.0, 87.25, "CONVIENTE"),
            "verde_087": (50000.0, 9.5, 89.5, "CONVIENTE"),
            "grigio_100": (50000.0, 9.5, 104.5, "CONVIENTE"),
            "grigio_070": (50000.0, 9.5, 74.5, "CONVIENTE"),
            "sanzione_005": (0.0, 4.5, 89.5, "MARGINALE"),
            "sanzione_000": (-50000.0, -0.5, 89.5,
                             "NON_CONVIENTE"),
            "gestione_zero": (55000.0, 10.0, 89.5, "CONVIENTE"),
            "prezzo_go_000": (95000.0, 9.5, 85.0, "CONVIENTE"),
            "consumo_20000": (105000.0, 9.75, 89.5,
                              "CONVIENTE"),
            "consumo_1000": (500.0, 5.0, 89.5, "CONVIENTE"),
            "quota_000": (-5000.0, None, 85.0, "NON_CONVIENTE"),
            "tol_zero": (50000.0, 9.5, 89.5, "CONVIENTE"),
            "go_be": (0.0, 9.5, 94.5, "MARGINALE"),
            "verde_be": (50000.0, 9.5, 89.5, "CONVIENTE"),
        }
        for nome, (ben, bg, bv, vdc) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(
                    s[nome]["beneficio_netto_eur"], ben, places=2)
                if bg is None:
                    self.assertIsNone(s[nome]["be_go_eur_mwh"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_go_eur_mwh"], bg, places=2)
                self.assertAlmostEqual(
                    s[nome]["be_verde_eur_mwh"], bv, places=2)
                self.assertEqual(s[nome]["verdetto"], vdc)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("beneficio_netto_eur", caso)
            self.assertIn("be_go_eur_mwh", caso)
            self.assertIn("be_verde_eur_mwh", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)


class TestCasiLimite(unittest.TestCase):
    def test_quota_zero_beneficio_negativo_non_conviente(self):
        bc = mh905_calcola(**_demo_kwargs(quota_pct=0.0))
        self.assertEqual(bc["go_nec_mwh"], 0.0)
        self.assertEqual(bc["costo_go_eur"], 0.0)
        self.assertEqual(bc["costo_copertura_eur"], 855000.0)
        self.assertEqual(bc["costo_bundled_eur"], 925000.0)
        self.assertEqual(bc["delta_bundled_eur"], 70000.0)
        self.assertIsNone(bc["costo_per_mwh_eur_mwh"])
        self.assertIsNone(bc["be_go_eur_mwh"])
        self.assertEqual(bc["sanzione_evitata_eur"], 0.0)
        self.assertEqual(bc["beneficio_netto_eur"], -5000.0)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 85.00,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        # Fisica e prezzi restano calcolati anche
        # nel regime di quota zero (sono fisica e
        # prezzi, non KPI di ritorno).
        self.assertEqual(bc["consumo_mwh"], 10000.0)
        self.assertEqual(bc["quota_pct"], 0.0)

    def test_sanzione_zero_non_conviente(self):
        bc = mh905_calcola(**_demo_kwargs(sanzione_eur_mwh=0.0))
        self.assertEqual(bc["sanzione_evitata_eur"], 0.0)
        self.assertEqual(bc["beneficio_netto_eur"], -50000.0)
        self.assertAlmostEqual(bc["be_go_eur_mwh"], -0.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_sanzione_cinque_marginale(self):
        bc = mh905_calcola(**_demo_kwargs(sanzione_eur_mwh=5.0))
        self.assertEqual(bc["sanzione_evitata_eur"], 50000.0)
        self.assertEqual(bc["beneficio_netto_eur"], 0.0)
        self.assertAlmostEqual(bc["be_go_eur_mwh"], 4.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_go_be_marginale(self):
        be = demo_calcoli()["be_go_eur_mwh"]
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_go_eur_mwh=be))
        self.assertAlmostEqual(bc["beneficio_netto_eur"], 0.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 94.50,
                               places=2)
        self.assertAlmostEqual(bc["costo_go_eur"], 95000.00,
                               places=2)

    def test_verde_be_delta_zero(self):
        bv = demo_calcoli()["be_verde_eur_mwh"]
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_verde_eur_mwh=bv))
        self.assertAlmostEqual(bc["delta_bundled_eur"], 0.0,
                               places=2)
        self.assertAlmostEqual(bc["costo_bundled_eur"],
                               bc["costo_copertura_eur"])
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               50000.00, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_gestione_zero(self):
        bc = mh905_calcola(**_demo_kwargs(gestione_eur_anno=0.0))
        self.assertEqual(bc["gestione_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["costo_copertura_eur"],
                               895000.00, places=2)
        self.assertAlmostEqual(bc["costo_bundled_eur"],
                               920000.00, places=2)
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               55000.00, places=2)
        self.assertAlmostEqual(bc["be_go_eur_mwh"], 10.00,
                               places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 89.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_prezzo_go_zero(self):
        bc = mh905_calcola(**_demo_kwargs(prezzo_go_eur_mwh=0.0))
        self.assertEqual(bc["costo_go_eur"], 0.0)
        self.assertAlmostEqual(bc["costo_copertura_eur"],
                               855000.00, places=2)
        self.assertAlmostEqual(bc["delta_bundled_eur"],
                               70000.00, places=2)
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               95000.00, places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 85.00,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_consumo_20000_e_1000(self):
        bc = mh905_calcola(**_demo_kwargs(consumo_mwh=20000.0))
        self.assertEqual(bc["go_nec_mwh"], 20000.0)
        self.assertEqual(bc["costo_go_eur"], 90000.0)
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               105000.00, places=2)
        self.assertAlmostEqual(bc["be_go_eur_mwh"], 9.75,
                               places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 89.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh905_calcola(**_demo_kwargs(consumo_mwh=1000.0))
        self.assertEqual(bc["go_nec_mwh"], 1000.0)
        self.assertEqual(bc["costo_go_eur"], 4500.0)
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               500.00, places=2)
        self.assertAlmostEqual(bc["be_go_eur_mwh"], 5.00,
                               places=2)
        self.assertAlmostEqual(bc["premium_verde_eur_mwh"],
                               9.50, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_grigio_100_e_70(self):
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_grigio_eur_mwh=100.0))
        self.assertEqual(bc["costo_grigio_eur"], 1000000.0)
        self.assertAlmostEqual(bc["delta_bundled_eur"],
                               -125000.00, places=2)
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               50000.00, places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 104.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_grigio_eur_mwh=70.0))
        self.assertEqual(bc["costo_grigio_eur"], 700000.0)
        self.assertAlmostEqual(bc["delta_bundled_eur"],
                               175000.00, places=2)
        self.assertAlmostEqual(bc["be_verde_eur_mwh"], 74.50,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_delta_segno_verde_basso(self):
        # Con prezzo verde sotto il breakeven il
        # delta e negativo: il bundled conviene.
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_verde_eur_mwh=80.0))
        self.assertLess(bc["delta_bundled_eur"], 0.0)
        self.assertAlmostEqual(bc["delta_bundled_eur"],
                               -95000.00, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh905_calcola(
            **_demo_kwargs(prezzo_verde_eur_mwh=100.0))
        self.assertGreater(bc["delta_bundled_eur"], 0.0)
        self.assertAlmostEqual(bc["delta_bundled_eur"],
                               105000.00, places=2)

    def test_tolleranza_zero_demo_resta_conveniente(self):
        # Con beneficio positivo la tolleranza non
        # decide nulla: il demo resta CONVIENTE
        # anche a tolleranza zero.
        bc = mh905_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["beneficio_netto_eur"],
                               50000.00, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_beneficio_invarianze_prezzi(self):
        # Il beneficio netto non dipende dal prezzo
        # verde ne dal prezzo grigio: il bundled e
        # il grigio non entrano nel beneficio.
        bc = demo_calcoli()
        bc_v = mh905_calcola(
            **_demo_kwargs(prezzo_verde_eur_mwh=87.0))
        self.assertEqual(bc_v["beneficio_netto_eur"],
                         bc["beneficio_netto_eur"])
        bc_g = mh905_calcola(
            **_demo_kwargs(prezzo_grigio_eur_mwh=100.0))
        self.assertEqual(bc_g["beneficio_netto_eur"],
                         bc["beneficio_netto_eur"])
        # Il delta bundled invece dipende da
        # entrambi.
        self.assertNotEqual(bc_v["delta_bundled_eur"],
                            bc["delta_bundled_eur"])
        self.assertNotEqual(bc_g["delta_bundled_eur"],
                            bc["delta_bundled_eur"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh905_csv(bc, mh905_demo())
        for voce in ("consumo_mwh", "quota_pct",
                     "prezzo_go_eur_mwh",
                     "prezzo_grigio_eur_mwh",
                     "prezzo_verde_eur_mwh",
                     "gestione_eur_anno",
                     "sanzione_eur_mwh",
                     "tol_frazione",
                     "go_nec_mwh",
                     "costo_go_eur",
                     "costo_grigio_eur",
                     "costo_copertura_eur",
                     "costo_bundled_eur",
                     "delta_bundled_eur",
                     "costo_per_mwh_eur_mwh",
                     "premium_verde_eur_mwh",
                     "sanzione_evitata_eur",
                     "beneficio_netto_eur",
                     "be_go_eur_mwh",
                     "be_verde_eur_mwh",
                     "grigia_piu_sanzione_eur",
                     "scenario_base_quota_pct",
                     "scenario_base_beneficio_netto_eur",
                     "scenario_base_verdetto",
                     "scenario_go_piu50_beneficio_netto_eur",
                     "scenario_go_piu50_verdetto",
                     "scenario_go_meno50_beneficio_netto_eur",
                     "scenario_go_meno50_verdetto",
                     "scenario_quota_050_beneficio_netto_eur",
                     "scenario_quota_050_verdetto",
                     "scenario_verde_087_beneficio_netto_eur",
                     "scenario_verde_087_verdetto",
                     "confronto_go_nec_mwh",
                     "confronto_costo_go_eur",
                     "confronto_costo_grigio_eur",
                     "confronto_costo_copertura_eur",
                     "confronto_delta_bundled_eur",
                     "confronto_beneficio_netto_eur",
                     "confronto_be_go_eur_mwh",
                     "confronto_be_verde_eur_mwh",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh905_csv(bc, mh905_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("consumo_mwh;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh905_demo_calcoli()["beneficio_netto_eur"],
                         demo_calcoli()["beneficio_netto_eur"])
        self.assertEqual(mh905_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_scenari_confronto_tabella_costi(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 13)
        self.assertEqual(len(bc["df_tabella"]), 21)
        self.assertEqual(len(bc["df_costi"]), 3)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["GO necessarie (MWh)",
             "Costo GO (EUR)",
             "Costo energia grigia (EUR)",
             "Costo copertura (EUR)",
             "Costo bundled verde (EUR)",
             "Delta bundled (EUR)",
             "Costo GO per MWh (EUR/MWh)",
             "Premium verde (EUR/MWh)",
             "Sanzione evitata (EUR)",
             "Beneficio netto (EUR)",
             "Breakeven prezzo GO (EUR/MWh)",
             "Breakeven prezzo verde (EUR/MWh)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            10000.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[9],
            50000.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Consumo annuo (MWh)", voci)
        self.assertIn("Quota coperta da GO (%)", voci)
        self.assertIn("Breakeven prezzo GO (EUR/MWh)", voci)
        self.assertIn("Breakeven prezzo verde (EUR/MWh)", voci)
        self.assertIn("Beneficio netto (EUR)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("Beneficio netto (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto",
                      set(bc["df_scenari"].columns))
        self.assertIn("Breakeven prezzo verde (EUR/MWh)",
                      set(bc["df_scenari"].columns))
        self.assertEqual(
            list(bc["df_costi"]["Voce"]),
            ["Copertura (grigia + GO + gestione)",
             "Bundled verde",
             "Grigia + sanzione"])
        self.assertAlmostEqual(
            bc["df_costi"]["Importo (EUR/anno)"].iloc[0],
            900000.00, places=2)
        self.assertAlmostEqual(
            bc["df_costi"]["Importo (EUR/anno)"].iloc[1],
            925000.00, places=2)
        self.assertAlmostEqual(
            bc["df_costi"]["Importo (EUR/anno)"].iloc[2],
            950000.00, places=2)

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(consumo_mwh="10000.0")
        self.assertRaises(ValueError, mh905_calcola, **kw)
        kw = _demo_kwargs(consumo_mwh=True)
        self.assertRaises(ValueError, mh905_calcola, **kw)
        val = mh905_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def905\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh905_demo().keys()), lette - set(mh905_demo().keys()))
        self.assertEqual(lette, set(mh905_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc905\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc905\["([^"]+)"\]', src))
        attese = set(mh905_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 904 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 905.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 910)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab905:"), 1)
        self.assertTrue(src.startswith("    # W910"))

    def test_ui_tab905_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab905:"), 1)
        self.assertIn("def mh905_demo(", src_h)
        self.assertIn("def mh905_calcola(", src_h)
        self.assertIn("tab905", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Garanzie di Origine (GO): il certificato rinnovabile paga?", src)
        self.assertIn("🌱📜 Garanzie di Origine (GO): il certificato rinnovabile paga?", src)
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
        chiavi = re.findall(r'key="(st905_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st905_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 15)
        self.assertIn('key="st905_calcola"', src)
        self.assertIn('key="st905_csv"', src)
        self.assertIn('key="st905_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg905"), src.index(".paiac("))
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
