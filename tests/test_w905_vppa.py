"""Test nuova scheda VPPA (Virtual PPA): il prezzo fisso
rinnovabile senza ritirare l'energia paga davvero?
Repo path: tests/test_w905_vppa.py

Effetto ECONOMICO: un VPPA e un contratto finanziario per
differenza (CfD) su energia rinnovabile, senza ritiro
fisico dell'energia. Il consumatore continua a comprare la
fornitura fisica al prezzo di fornitura e regola col
produttore solo la differenza tra prezzo di mercato e
prezzo fisso, sull'energia coperta. Settlement annuo =
(prezzo di mercato meno prezzo fisso) per energia coperta.
Il risparmio annuo e la differenza tra costo merchant e
costo con VPPA ed e IDENTICO al settlement: il VPPA sposta
il prezzo della quota coperta dal prezzo di fornitura al
prezzo fisso piu basis. Insight chiave: il VPPA fissa il
prezzo a prezzo fisso piu basis, NON a prezzo fisso.
Demo: energia consumata 20.000 MWh/anno, energia coperta
12.000 MWh/anno, prezzo fisso 65 EUR/MWh, prezzo di
mercato 85 EUR/MWh, prezzo di fornitura 90 EUR/MWh,
basis 5 EUR/MWh, costo iniziale 250.000 EUR, costo annuo
5.000 EUR/anno, durata 10 anni, tasso 0,05 (frazione),
tolleranza 0,10 (frazione), fattore CO2 di rete
0,25 t/MWh. Settlement = (85 meno 65) per 12.000 =
240.000 EUR/anno. Costo merchant = 20.000 per 90 =
1.800.000 EUR/anno. Costo con VPPA = 8.000 per 90 piu
12.000 per 70 = 1.560.000 EUR/anno. Risparmio =
1.800.000 meno 1.560.000 = 240.000 EUR/anno, uguale al
settlement. Prezzo medio = 1.560.000 diviso 20.000 = 78
EUR/MWh. Prezzo coperto = 65 piu 5 = 70 EUR/MWh. Flussi
[meno 250.000, 235.000 per 10 anni]; cumulato anno 1
meno 15.000, anno 2 220.000, finale 2.100.000.
VAN = 1.564.607,71 EUR; TIR per bisezione su flussi con
intervallo da meno 0,9 a 5,0 (93,87 %); payback (primo anno
con cumulato netto maggiore o uguale a 0) = 2; breakeven
prezzo di mercato = prezzo fisso piu costo annuo diviso
energia coperta = 65,42 EUR/MWh (pareggio annuo, NON il
prezzo che azzera la VAN); breakeven basis = prezzo di
fornitura meno prezzo fisso = 25 EUR/MWh (risparmio zero).
CO2 evitata anno = energia coperta per fattore di rete =
3.000 t/anno (INFORMATIVA, mai nel conto economico); CO2
evitata vita = 30.000 t.
Scenari: base VAN 1.564.607,71, TIR 93,87 %, payback 2,
CONVIENTE; mercato piu 20 % VAN 3.139.841,63, TIR 175,59 %,
payback 1, CONVIENTE; mercato meno 20 % VAN meno
10.626,22, TIR 4,12 %, payback 9, MARGINALE; produzione
meno 20 % VAN 1.193.964,43, TIR 74,51 %, payback 2,
CONVIENTE; basis piu 10 EUR/MWh VAN INVARIATA
1.564.607,71, TIR 93,87 %, payback 2, CONVIENTE, prezzo
coperto 80, prezzo medio 88; prezzo fisso piu 10 VAN
637.999,52, TIR 44,87 %, payback 3, CONVIENTE.
Confronto: costo merchant 1.800.000 contro costo con VPPA
1.560.000, risparmio 240.000, settlement 240.000, basis 5,
prezzo medio 78, prezzo coperto 70, costo iniziale
250.000, VAN 1.564.607,71, CO2 evitata 3.000 t/anno.
Tasso in FRAZIONE (0,05 = 5 %), usato diretto, NON diviso
per 100. Tolleranza in FRAZIONE (0,10 = 10 % del costo
iniziale), usata diretta, NON divisa per 100. Prezzi,
energia coperta e fattori restano costanti per tutta la
durata, SEMPLIFICAZIONE DICHIARATA (prezzo di mercato
volatile, produzione rinnovabile che oscilla, basis che
si muove, costi reali variano nel mondo reale, qui valore
medio costante); la basis NON cambia risparmio e VAN.
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il risparmio e minore o
uguale a 0 (guard degenere: UI salta KPI, grafico, tabella
e CSV) oppure se un input e degenere (energia consumata
nulla o negativa, energia coperta negativa o sopra
l'energia consumata, prezzo fisso negativo, prezzo di
mercato negativo, prezzo di fornitura negativo, costo
iniziale negativo, costo annuo negativo, durata nulla o
negativa o non intera, tasso nullo o negativo o maggiore
o uguale a 1, tolleranza negativa o sopra 1, fattore CO2
negativo); altrimenti CONVIENTE se VAN maggiore di 0,
MARGINALE se VAN minore o uguale a 0 e valore assoluto
della VAN minore o uguale a tolleranza per costo iniziale,
NON_CONVIENTE altrimenti.
Casi limite: prezzo di mercato 65 (risparmio zero in tutti
gli anni, VAN None, NON_CALCOLABILE); prezzo di mercato
60 (risparmio meno 60.000, NON_CALCOLABILE); energia
coperta zero (risparmio zero, NON_CALCOLABILE); energia
coperta 20.000 (VAN 2.800.085,30, TIR 157,99 %, payback 1);
costo iniziale zero (VAN 1.814.607,71, TIR non definita,
payback 1); costo annuo zero (VAN 1.603.216,38, TIR
95,88 %, payback 2); durata 5 (VAN 767.427,02, TIR
90,23 %, payback 2); tasso 0,10 (VAN 1.193.973,27, TIR
93,87 %, payback 2); mercato meno 20 % con tolleranza
zero (VAN meno 10.626,22, NON_CONVIENTE: la tolleranza
decide il confine MARGINALE).
Distinzione esplicita: qui SOLO il VPPA come CfD
finanziario senza ritiro fisico dell'energia (VAN sul
RISPARMIO da settlement con costo iniziale di setup e
garanzia), NIENTE PPA fisico (li l'energia viene ritirata
e consegnata: qui solo cassa), NIENTE acquisto di energia
verde con certificati (li il costo e un premio sulle
garanzie di origine: qui un contratto per differenza sul
prezzo), NIENTE autoproduzione con fotovoltaico proprio
(li il risparmio e sull'autoconsumo elettrico: qui solo
il prezzo della quota coperta), NIENTE hedging con
future di borsa (li il sottostante e un future
standardizzato: qui un CfD bilaterale di lungo periodo).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w905_helpers import (
        demo_calcoli,
        mh900_basis,
        mh900_breakeven_basis,
        mh900_breakeven_prezzo_mercato,
        mh900_calcola,
        mh900_confronto,
        mh900_co2_evitata_anno,
        mh900_co2_evitata_vita,
        mh900_costo_merchant,
        mh900_costo_vppa,
        mh900_csv,
        mh900_demo,
        mh900_demo_calcoli,
        mh900_flussi,
        mh900_fraz,
        mh900_int_pos,
        mh900_nneg,
        mh900_num,
        mh900_payback,
        mh900_pos,
        mh900_prezzo_coperto,
        mh900_prezzo_medio,
        mh900_riga_anno,
        mh900_risparmio,
        mh900_scenario,
        mh900_sensibilita,
        mh900_serie_annua,
        mh900_settlement,
        mh900_tasso,
        mh900_tir,
        mh900_valida,
        mh900_van,
        mh900_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w905_helpers", os.path.join(_hf, "w905_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh900_basis = _mod.mh900_basis
    mh900_breakeven_basis = _mod.mh900_breakeven_basis
    mh900_breakeven_prezzo_mercato = _mod.mh900_breakeven_prezzo_mercato
    mh900_calcola = _mod.mh900_calcola
    mh900_confronto = _mod.mh900_confronto
    mh900_co2_evitata_anno = _mod.mh900_co2_evitata_anno
    mh900_co2_evitata_vita = _mod.mh900_co2_evitata_vita
    mh900_costo_merchant = _mod.mh900_costo_merchant
    mh900_costo_vppa = _mod.mh900_costo_vppa
    mh900_csv = _mod.mh900_csv
    mh900_demo = _mod.mh900_demo
    mh900_demo_calcoli = _mod.mh900_demo_calcoli
    mh900_flussi = _mod.mh900_flussi
    mh900_fraz = _mod.mh900_fraz
    mh900_int_pos = _mod.mh900_int_pos
    mh900_nneg = _mod.mh900_nneg
    mh900_num = _mod.mh900_num
    mh900_payback = _mod.mh900_payback
    mh900_pos = _mod.mh900_pos
    mh900_prezzo_coperto = _mod.mh900_prezzo_coperto
    mh900_prezzo_medio = _mod.mh900_prezzo_medio
    mh900_riga_anno = _mod.mh900_riga_anno
    mh900_risparmio = _mod.mh900_risparmio
    mh900_scenario = _mod.mh900_scenario
    mh900_sensibilita = _mod.mh900_sensibilita
    mh900_serie_annua = _mod.mh900_serie_annua
    mh900_settlement = _mod.mh900_settlement
    mh900_tasso = _mod.mh900_tasso
    mh900_tir = _mod.mh900_tir
    mh900_valida = _mod.mh900_valida
    mh900_van = _mod.mh900_van
    mh900_verdetto = _mod.mh900_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w905_helpers.py")
_UI_PATH = _risolvi("w905_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "9"
_VECCHIO_TAB = "tab89" + "9"
_VECCHIO_ST = "st89" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "basis_eur_mwh": 5.0,
    "settlement_eur_anno": 240000.0,
    "costo_merchant_eur_anno": 1800000.0,
    "costo_vppa_eur_anno": 1560000.0,
    "risparmio_eur_anno": 240000.0,
    "prezzo_medio_eur_mwh": 78.0,
    "prezzo_coperto_eur_mwh": 70.0,
    "breakeven_prezzo_mercato": 65.41666666666667,
    "breakeven_basis": 25.0,
    "co2_evitata_t_anno": 3000.0,
    "co2_evitata_t_vita": 30000.0,
    "van": 1564607.7083584303,
    "tir": 93.87471004865404,
    "payback": 2,
}

_DEMO_SCENARI = [
    {"nome": "Base", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 90.0,
     "e_vppa_mwh_anno": 12000.0, "basis_eur_mwh": 5.0,
     "risparmio_eur_anno": 240000.0,
     "van": 1564607.7083584303, "tir": 93.87471004865404,
     "payback": 2, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 78.0,
     "prezzo_coperto_eur_mwh": 70.0,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Mercato piu 20%", "p_mkt_eur_mwh": 102.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 90.0,
     "e_vppa_mwh_anno": 12000.0, "basis_eur_mwh": -12.0,
     "risparmio_eur_anno": 444000.0,
     "van": 3139841.633912132, "tir": 175.5930522871228,
     "payback": 1, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 67.8,
     "prezzo_coperto_eur_mwh": 53.0,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Mercato meno 20%", "p_mkt_eur_mwh": 68.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 90.0,
     "e_vppa_mwh_anno": 12000.0, "basis_eur_mwh": 22.0,
     "risparmio_eur_anno": 36000.0,
     "van": -10626.217195270856, "tir": 4.115360693779733,
     "payback": 9, "verdetto": "MARGINALE",
     "prezzo_medio_eur_mwh": 88.2,
     "prezzo_coperto_eur_mwh": 87.0,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Produzione meno 20%", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 90.0,
     "e_vppa_mwh_anno": 9600.0, "basis_eur_mwh": 5.0,
     "risparmio_eur_anno": 192000.0,
     "van": 1193964.4317575598, "tir": 74.5145131574435,
     "payback": 2, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 80.4,
     "prezzo_coperto_eur_mwh": 70.0,
     "co2_evitata_t_anno": 2400.0},
    {"nome": "Basis piu 10", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 65.0, "p_supply_eur_mwh": 100.0,
     "e_vppa_mwh_anno": 12000.0, "basis_eur_mwh": 15.0,
     "risparmio_eur_anno": 240000.0,
     "van": 1564607.7083584303, "tir": 93.87471004865404,
     "payback": 2, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 88.0,
     "prezzo_coperto_eur_mwh": 80.0,
     "co2_evitata_t_anno": 3000.0},
    {"nome": "Prezzo fisso piu 10", "p_mkt_eur_mwh": 85.0,
     "p_fix_eur_mwh": 75.0, "p_supply_eur_mwh": 90.0,
     "e_vppa_mwh_anno": 12000.0, "basis_eur_mwh": 5.0,
     "risparmio_eur_anno": 120000.0,
     "van": 637999.5168562533, "tir": 44.87029687329084,
     "payback": 3, "verdetto": "CONVIENTE",
     "prezzo_medio_eur_mwh": 84.0,
     "prezzo_coperto_eur_mwh": 80.0,
     "co2_evitata_t_anno": 3000.0},
]

_DEMO_CONFRONTO = {
    "costo_merchant": 1800000.0,
    "costo_vppa": 1560000.0,
    "risparmio": 240000.0,
    "settlement": 240000.0,
    "basis": 5.0,
    "prezzo_medio": 78.0,
    "prezzo_coperto": 70.0,
    "c0": 250000.0,
    "c_ann": 5000.0,
    "van": 1564607.7083584303,
    "co2_evitata_t_anno": 3000.0,
    "co2_evitata_t_vita": 30000.0,
    "breakeven_prezzo_mercato": 65.41666666666667,
    "breakeven_basis": 25.0,
    "tir": 93.87471004865404,
    "payback": 2,
}

_ORDINE_VALIDA = (
    "e_cons_mwh_anno", "e_vppa_mwh_anno",
    "p_fix_eur_mwh", "p_mkt_eur_mwh",
    "p_supply_eur_mwh", "c0_eur", "c_ann_eur_anno",
    "t_anni", "r_tasso", "tol_frazione",
    "f_co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh900_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))

class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh900_num(3, "x"), 3.0)
        self.assertEqual(mh900_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh900_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh900_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh900_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh900_pos(0, "x")
        with self.assertRaises(ValueError):
            mh900_pos(-1, "x")
        self.assertEqual(mh900_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh900_fraz(0, "x"), 0.0)
        self.assertEqual(mh900_fraz(1, "x"), 1.0)
        self.assertEqual(mh900_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh900_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh900_fraz(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh900_int_pos(10, "x"), 10)
        self.assertEqual(mh900_int_pos(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh900_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh900_int_pos(5.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh900_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh900_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh900_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh900_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh900_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh900_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_basis_e_settlement(self):
        self.assertEqual(mh900_basis(90.0, 85.0), 5.0)
        self.assertEqual(mh900_basis(100.0, 85.0), 15.0)
        self.assertEqual(mh900_basis(85.0, 102.0), -17.0)
        self.assertEqual(mh900_basis(90.0, 90.0), 0.0)
        self.assertEqual(
            mh900_settlement(85.0, 65.0, 12000.0), 240000.0)
        self.assertEqual(
            mh900_settlement(102.0, 65.0, 12000.0), 444000.0)
        self.assertEqual(
            mh900_settlement(68.0, 65.0, 12000.0), 36000.0)
        self.assertEqual(
            mh900_settlement(65.0, 65.0, 12000.0), 0.0)
        self.assertEqual(
            mh900_settlement(60.0, 65.0, 12000.0), -60000.0)
        self.assertEqual(
            mh900_settlement(85.0, 65.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh900_basis(-1.0, 85.0)
        with self.assertRaises(ValueError):
            mh900_basis(90.0, -1.0)
        with self.assertRaises(ValueError):
            mh900_settlement(85.0, 65.0, -1.0)

    def test_costo_merchant_e_vppa(self):
        self.assertEqual(
            mh900_costo_merchant(20000.0, 90.0), 1800000.0)
        self.assertEqual(
            mh900_costo_merchant(20000.0, 100.0), 2000000.0)
        self.assertEqual(mh900_costo_merchant(20000.0, 0.0), 0.0)
        self.assertEqual(
            mh900_costo_vppa(20000.0, 12000.0, 90.0, 65.0, 5.0),
            1560000.0)
        self.assertEqual(
            mh900_costo_vppa(20000.0, 0.0, 90.0, 65.0, 5.0),
            1800000.0)
        self.assertEqual(
            mh900_costo_vppa(20000.0, 20000.0, 90.0, 65.0, 5.0),
            1400000.0)
        self.assertEqual(
            mh900_costo_vppa(20000.0, 12000.0, 100.0, 65.0,
                             15.0),
            1760000.0)
        with self.assertRaises(ValueError):
            mh900_costo_merchant(0, 90.0)
        with self.assertRaises(ValueError):
            mh900_costo_merchant(20000.0, -1.0)
        with self.assertRaises(ValueError):
            mh900_costo_vppa(20000.0, 20001.0, 90.0, 65.0, 5.0)
        with self.assertRaises(ValueError):
            mh900_costo_vppa(20000.0, -1.0, 90.0, 65.0, 5.0)

    def test_risparmio_identico_a_settlement(self):
        self.assertEqual(
            mh900_risparmio(1800000.0, 1560000.0), 240000.0)
        self.assertEqual(
            mh900_risparmio(1800000.0, 1560000.0),
            mh900_settlement(85.0, 65.0, 12000.0))
        self.assertEqual(
            mh900_risparmio(2000000.0, 1760000.0), 240000.0)
        self.assertEqual(
            mh900_risparmio(1800000.0, 1800000.0), 0.0)
        self.assertEqual(
            mh900_risparmio(1800000.0, 1860000.0), -60000.0)
        with self.assertRaises(ValueError):
            mh900_risparmio(-1.0, 1560000.0)
        with self.assertRaises(ValueError):
            mh900_risparmio(1800000.0, -1.0)

    def test_prezzi_medio_e_coperto(self):
        self.assertEqual(
            mh900_prezzo_medio(1560000.0, 20000.0), 78.0)
        self.assertEqual(
            mh900_prezzo_medio(1760000.0, 20000.0), 88.0)
        self.assertEqual(
            mh900_prezzo_medio(1356000.0, 20000.0), 67.8)
        self.assertEqual(mh900_prezzo_coperto(65.0, 5.0), 70.0)
        self.assertEqual(mh900_prezzo_coperto(65.0, 15.0), 80.0)
        self.assertEqual(mh900_prezzo_coperto(65.0, -12.0), 53.0)
        self.assertEqual(mh900_prezzo_coperto(65.0, 0.0), 65.0)
        with self.assertRaises(ValueError):
            mh900_prezzo_medio(1560000.0, 0)
        with self.assertRaises(ValueError):
            mh900_prezzo_coperto(-1.0, 5.0)

    def test_riga_anno(self):
        riga = mh900_riga_anno(1, 240000.0, 5000.0, 3000.0)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["risparmio"], 240000.0)
        self.assertEqual(riga["settlement"], 240000.0)
        self.assertEqual(riga["costo_annuo"], 5000.0)
        self.assertEqual(riga["flusso"], 235000.0)
        self.assertEqual(riga["co2_evitata"], 3000.0)
        riga = mh900_riga_anno(10, 240000.0, 5000.0, 3000.0)
        self.assertEqual(riga["flusso"], 235000.0)
        with self.assertRaises(ValueError):
            mh900_riga_anno(0, 240000.0, 5000.0, 3000.0)

    def test_serie_annua(self):
        serie = mh900_serie_annua(240000.0, 5000.0, 10, 3000.0)
        self.assertEqual(len(serie), 10)
        self.assertTrue(all(r["flusso"] == 235000.0
                            for r in serie))
        self.assertTrue(all(r["settlement"] == 240000.0
                            for r in serie))
        self.assertTrue(all(r["co2_evitata"] == 3000.0
                            for r in serie))
        serie = mh900_serie_annua(36000.0, 5000.0, 10, 3000.0)
        self.assertEqual(serie[0]["flusso"], 31000.0)
        with self.assertRaises(ValueError):
            mh900_serie_annua(240000.0, 5000.0, 0, 3000.0)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        flussi = bc["flussi"]
        self.assertEqual(len(flussi), 11)
        self.assertEqual(flussi[0], -250000.0)
        self.assertEqual(flussi[1], 235000.0)
        self.assertEqual(flussi[10], 235000.0)
        self.assertAlmostEqual(sum(flussi), 2100000.00, places=2)
        self.assertAlmostEqual(sum(flussi[:2]), -15000.00, places=2)
        self.assertAlmostEqual(sum(flussi[:3]), 220000.00, places=2)
        self.assertLess(sum(flussi[:2]), 0.0)
        flussi2 = mh900_flussi(bc["serie"], bc["c0_eur"], 10)
        self.assertEqual(flussi2, flussi)
        self.assertAlmostEqual(mh900_van(flussi, 0.05), bc["van"])
        with self.assertRaises(ValueError):
            mh900_flussi(bc["serie"][:9], bc["c0_eur"], 10)

    def test_breakeven_prezzo_mercato(self):
        self.assertAlmostEqual(
            mh900_breakeven_prezzo_mercato(65.0, 5000.0,
                                           12000.0),
            65.42, places=2)
        self.assertEqual(
            mh900_breakeven_prezzo_mercato(65.0, 0.0, 12000.0),
            65.0)
        self.assertAlmostEqual(
            mh900_breakeven_prezzo_mercato(75.0, 5000.0,
                                           12000.0),
            75.42, places=2)
        self.assertIsNone(
            mh900_breakeven_prezzo_mercato(65.0, 5000.0, 0.0))
        # Al breakeven il flusso annuo e zero e la VAN
        # resta meno il costo iniziale: pareggio annuo,
        # NON VAN zero.
        be = mh900_breakeven_prezzo_mercato(65.0, 5000.0,
                                           12000.0)
        self.assertAlmostEqual(
            mh900_settlement(be, 65.0, 12000.0), 5000.0,
            places=2)
        bc = mh900_calcola(
            **_demo_kwargs(p_mkt_eur_mwh=be))
        self.assertEqual(bc["risparmio_eur_anno"], 5000.0)
        self.assertAlmostEqual(bc["van"], -250000.0, places=2)
        with self.assertRaises(ValueError):
            mh900_breakeven_prezzo_mercato(65.0, 5000.0, -1.0)

    def test_breakeven_basis(self):
        self.assertEqual(mh900_breakeven_basis(90.0, 65.0), 25.0)
        self.assertEqual(mh900_breakeven_basis(100.0, 65.0), 35.0)
        self.assertEqual(mh900_breakeven_basis(65.0, 65.0), 0.0)
        self.assertEqual(mh900_breakeven_basis(60.0, 65.0), -5.0)
        # Alla basis di breakeven il prezzo coperto
        # eguaglia il prezzo di fornitura e il
        # risparmio si azzera.
        be = mh900_breakeven_basis(90.0, 65.0)
        self.assertEqual(mh900_prezzo_coperto(65.0, be), 90.0)
        with self.assertRaises(ValueError):
            mh900_breakeven_basis(-1.0, 65.0)

    def test_co2_evitata_informativa(self):
        self.assertEqual(
            mh900_co2_evitata_anno(12000.0, 0.25), 3000.0)
        self.assertEqual(
            mh900_co2_evitata_anno(9600.0, 0.25), 2400.0)
        self.assertEqual(
            mh900_co2_evitata_anno(12000.0, 0.0), 0.0)
        self.assertEqual(
            mh900_co2_evitata_vita(3000.0, 10), 30000.0)
        self.assertEqual(
            mh900_co2_evitata_vita(3000.0, 5), 15000.0)
        with self.assertRaises(ValueError):
            mh900_co2_evitata_anno(12000.0, -0.1)
        with self.assertRaises(ValueError):
            mh900_co2_evitata_anno(-1.0, 0.25)
        with self.assertRaises(ValueError):
            mh900_co2_evitata_vita(3000.0, 0)

    def test_scenario_singolo(self):
        s = mh900_scenario("Mercato piu 20%", mh900_demo(),
                           {"p_mkt_eur_mwh": 102.0})
        self.assertEqual(s["nome"], "Mercato piu 20%")
        self.assertEqual(s["p_mkt_eur_mwh"], 102.0)
        self.assertAlmostEqual(s["van"], 3139841.63, places=2)
        self.assertEqual(s["payback"], 1)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh900_scenario("Mercato meno 20%", mh900_demo(),
                           {"p_mkt_eur_mwh": 68.0})
        self.assertAlmostEqual(s["van"], -10626.22, places=2)
        self.assertEqual(s["verdetto"], "MARGINALE")
        s = mh900_scenario("Basis piu 10", mh900_demo(),
                           {"p_supply_eur_mwh": 100.0})
        self.assertAlmostEqual(s["van"], 1564607.71, places=2)
        self.assertEqual(s["prezzo_coperto_eur_mwh"], 80.0)
        self.assertEqual(s["prezzo_medio_eur_mwh"], 88.0)
        with self.assertRaises(ValueError):
            mh900_scenario("", mh900_demo(),
                           {"p_mkt_eur_mwh": 102.0})
        with self.assertRaises(ValueError):
            mh900_scenario("X", mh900_demo(),
                           {"e_vppa_mwh_anno": 99999.0})

    def test_scenario_basis_van_invariata(self):
        # La basis NON cambia risparmio e VAN: alza di
        # pari importo costo merchant e costo con VPPA.
        base = mh900_scenario("Base", mh900_demo(), {})
        s = mh900_scenario("Basis piu 10", mh900_demo(),
                           {"p_supply_eur_mwh": 100.0})
        self.assertEqual(s["van"], base["van"])
        self.assertEqual(s["tir"], base["tir"])
        self.assertEqual(s["payback"], base["payback"])
        self.assertEqual(s["risparmio_eur_anno"],
                         base["risparmio_eur_anno"])
        self.assertNotEqual(s["prezzo_coperto_eur_mwh"],
                            base["prezzo_coperto_eur_mwh"])
        self.assertNotEqual(s["prezzo_medio_eur_mwh"],
                            base["prezzo_medio_eur_mwh"])

    def test_scenario_risparmio_negativo_non_calcolabile(self):
        s = mh900_scenario("Mercato basso", mh900_demo(),
                           {"p_mkt_eur_mwh": 60.0})
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh900_confronto(1800000.0, 1560000.0, 240000.0,
                            240000.0, 5.0, 78.0, 70.0,
                            250000.0, 5000.0, 1564607.71,
                            3000.0, 30000.0, 65.42, 25.0,
                            93.87, 2)
        self.assertEqual(c["costo_merchant"], 1800000.0)
        self.assertEqual(c["costo_vppa"], 1560000.0)
        self.assertEqual(c["risparmio"], 240000.0)
        self.assertEqual(c["settlement"], 240000.0)
        self.assertEqual(c["basis"], 5.0)
        self.assertEqual(c["prezzo_medio"], 78.0)
        self.assertEqual(c["prezzo_coperto"], 70.0)
        self.assertEqual(c["c0"], 250000.0)
        self.assertEqual(c["c_ann"], 5000.0)
        self.assertEqual(c["van"], 1564607.71)
        self.assertEqual(c["co2_evitata_t_anno"], 3000.0)
        self.assertEqual(c["co2_evitata_t_vita"], 30000.0)
        self.assertEqual(c["breakeven_prezzo_mercato"], 65.42)
        self.assertEqual(c["breakeven_basis"], 25.0)
        self.assertEqual(c["tir"], 93.87)
        self.assertEqual(c["payback"], 2)
        c = mh900_confronto(1800000.0, 1860000.0, -60000.0,
                            -60000.0, 5.0, 93.0, 70.0,
                            250000.0, 5000.0, 0.0,
                            3000.0, 30000.0, None, None,
                            None, None)
        self.assertIsNone(c["breakeven_prezzo_mercato"])
        self.assertIsNone(c["breakeven_basis"])
        self.assertIsNone(c["tir"])
        self.assertIsNone(c["payback"])
        with self.assertRaises(ValueError):
            mh900_confronto(-1.0, 1560000.0, 240000.0,
                            240000.0, 5.0, 78.0, 70.0,
                            250000.0, 5000.0, 1564607.71,
                            3000.0, 30000.0, 65.42, 25.0,
                            93.87, 2)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_cinque(self):
        bc = mh900_demo_calcoli()
        self.assertAlmostEqual(
            mh900_van(bc["flussi"], 0.05),
            bc["van"])
        bc_basso = mh900_calcola(
            _scenari=False,
            **dict(mh900_demo(), p_mkt_eur_mwh=68.0))
        self.assertAlmostEqual(
            mh900_van(bc_basso["flussi"], 0.05),
            bc["scenari"][2]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh900_van([-250000, 235000, 235000], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 1564607,71; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh900_demo_calcoli()
        self.assertAlmostEqual(
            mh900_van(bc["flussi"], 0.05),
            1564607.71, places=2)
        self.assertNotAlmostEqual(
            mh900_van(bc["flussi"], 0.50),
            1564607.71, places=2)
        with self.assertRaises(ValueError):
            mh900_van(bc["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh900_demo_calcoli()
        tir = mh900_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh900_tir([-100, -10, -10]))
        self.assertIsNone(mh900_tir([100, 10, 10]))
        self.assertIsNone(mh900_tir([0, 10, 10]))

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh900_demo_calcoli()
        self.assertEqual(mh900_payback(bc["flussi"]), 2)
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh900_payback([-100, 100, 10]), 1)
        self.assertEqual(mh900_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh900_payback([-100, 10, 10]))
        # Con costo iniziale zero il payback e l'anno 1.
        self.assertEqual(mh900_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh900_demo_calcoli()
        f0 = bc["flussi"]
        self.assertAlmostEqual(sum(f0[:2]), -15000.00, places=2)
        self.assertAlmostEqual(sum(f0[:3]), 220000.00, places=2)
        self.assertAlmostEqual(sum(f0), 2100000.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(
            mh900_verdetto(100.0, 0.10, 250000.0), "CONVIENTE")
        self.assertEqual(
            mh900_verdetto(0.0, 0.10, 250000.0), "MARGINALE")
        self.assertEqual(
            mh900_verdetto(-25000.0, 0.10, 250000.0),
            "MARGINALE")
        self.assertEqual(
            mh900_verdetto(-25001.0, 0.10, 250000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh900_verdetto(-100000.0, 0.10, 250000.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativa e
        # NON_CONVIENTE (VAN zero compresa nel MARGINALE
        # solo perche il valore assoluto zero e minore
        # o uguale a zero).
        self.assertEqual(
            mh900_verdetto(-1.0, 0.0, 250000.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh900_verdetto(0.0, 0.0, 250000.0), "MARGINALE")
        with self.assertRaises(ValueError):
            mh900_verdetto(100.0, 1.5, 250000.0)
        with self.assertRaises(ValueError):
            mh900_verdetto(100.0, 0.10, -1.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh900_verdetto(None, 0.10, 250000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh900_verdetto(None, 0.0, 0.0), "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh900_demo()
        val = mh900_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_durata_zero_e_non_intera_no(self):
        kw = _demo_kwargs(t_anni=0)
        self.assertRaises(ValueError, mh900_calcola, **kw)
        kw = _demo_kwargs(t_anni=10.5)
        self.assertRaises(ValueError, mh900_calcola, **kw)
        kw = _demo_kwargs(t_anni=5)
        bc = mh900_calcola(**kw)
        self.assertEqual(bc["t_anni"], 5)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh900_calcola(**_demo_kwargs(r_tasso=tasso))
        bc = mh900_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertEqual(bc["r_tasso"], 0.10)

    def test_valida_energia_coperta_sopra_consumata_no(self):
        with self.assertRaises(ValueError):
            mh900_calcola(**_demo_kwargs(e_vppa_mwh_anno=20001.0))
        bc = mh900_calcola(**_demo_kwargs(e_vppa_mwh_anno=20000.0))
        self.assertEqual(bc["e_vppa_mwh_anno"], 20000.0)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh900_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh900_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("e_cons_mwh_anno", 0),
                              ("t_anni", 0),
                              ("r_tasso", 0)):
            with self.assertRaises(ValueError):
                mh900_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_mkt_eur_mwh=float("nan"))
        self.assertRaises(ValueError, mh900_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh900_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_cons_mwh_anno", -1),
                              ("e_vppa_mwh_anno", -1),
                              ("p_fix_eur_mwh", -1),
                              ("p_mkt_eur_mwh", -1),
                              ("p_supply_eur_mwh", -1),
                              ("c0_eur", -1),
                              ("c_ann_eur_anno", -1),
                              ("t_anni", -1),
                              ("r_tasso", -0.01),
                              ("tol_frazione", -0.1),
                              ("f_co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh900_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh900_calcola(mh900_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 6)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh900_calcola(dict(mh900_demo(), p_mkt_eur_mwh=999.0),
                           p_mkt_eur_mwh=85.0)
        self.assertEqual(bc["p_mkt_eur_mwh"], 85.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh900_calcola(_scenari=False, **mh900_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van"], 1564607.71, places=2)

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
        self.assertEqual(bc["payback"], 2)
        self.assertAlmostEqual(bc["tir"], 93.87, places=2)
        self.assertAlmostEqual(bc["breakeven_prezzo_mercato"],
                               65.42, places=2)
        self.assertAlmostEqual(bc["breakeven_basis"], 25.0,
                               places=2)
        self.assertAlmostEqual(bc["prezzo_medio_eur_mwh"], 78.0,
                               places=2)
        self.assertAlmostEqual(bc["prezzo_coperto_eur_mwh"], 70.0,
                               places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["basis_eur_mwh"],
            bc["p_supply_eur_mwh"] - bc["p_mkt_eur_mwh"])
        self.assertAlmostEqual(
            bc["settlement_eur_anno"],
            (bc["p_mkt_eur_mwh"] - bc["p_fix_eur_mwh"])
            * bc["e_vppa_mwh_anno"])
        self.assertAlmostEqual(
            bc["costo_merchant_eur_anno"],
            bc["e_cons_mwh_anno"] * bc["p_supply_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_vppa_eur_anno"],
            (bc["e_cons_mwh_anno"] - bc["e_vppa_mwh_anno"])
            * bc["p_supply_eur_mwh"]
            + bc["e_vppa_mwh_anno"]
            * bc["prezzo_coperto_eur_mwh"])
        # Identita chiave del modello: risparmio =
        # settlement, perche il VPPA sposta solo il
        # prezzo della quota coperta.
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["settlement_eur_anno"])
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["costo_merchant_eur_anno"]
            - bc["costo_vppa_eur_anno"])
        self.assertAlmostEqual(
            bc["prezzo_medio_eur_mwh"],
            bc["costo_vppa_eur_anno"] / bc["e_cons_mwh_anno"])
        self.assertAlmostEqual(
            bc["prezzo_coperto_eur_mwh"],
            bc["p_fix_eur_mwh"] + bc["basis_eur_mwh"])
        self.assertAlmostEqual(
            bc["breakeven_prezzo_mercato"],
            bc["p_fix_eur_mwh"] + bc["c_ann_eur_anno"]
            / bc["e_vppa_mwh_anno"])
        self.assertAlmostEqual(
            bc["breakeven_basis"],
            bc["p_supply_eur_mwh"] - bc["p_fix_eur_mwh"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["e_vppa_mwh_anno"] * bc["f_co2_t_mwh"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_vita"],
            bc["co2_evitata_t_anno"] * bc["t_anni"])
        self.assertAlmostEqual(
            bc["van"],
            mh900_van(bc["flussi"], bc["r_tasso"]))
        for t in range(1, bc["t_anni"] + 1):
            riga = bc["serie"][t - 1]
            with self.subTest(anno=t):
                self.assertAlmostEqual(
                    riga["flusso"],
                    riga["risparmio"] - riga["costo_annuo"])
                self.assertEqual(riga["settlement"],
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
        # mercato meno 20 % peggiora e diventa MARGINALE
        # con VAN appena negativa; la produzione meno 20 %
        # peggiora ma resta CONVIENTE; la basis piu 10
        # lascia VAN, TIR e payback INVARIATI e alza solo
        # i prezzi effettivi; il prezzo fisso piu 10
        # peggiora ma resta CONVIENTE.
        self.assertGreater(bc["scenari"][1]["van"], base["van"])
        self.assertGreater(bc["scenari"][1]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][1]["payback"], 1)
        self.assertLess(bc["scenari"][2]["van"], 0.0)
        self.assertGreater(bc["scenari"][2]["van"], -25000.0)
        self.assertEqual(bc["scenari"][2]["verdetto"], "MARGINALE")
        self.assertEqual(bc["scenari"][2]["payback"], 9)
        self.assertLess(bc["scenari"][3]["van"], base["van"])
        self.assertEqual(bc["scenari"][3]["verdetto"], "CONVIENTE")
        self.assertEqual(bc["scenari"][4]["van"], base["van"])
        self.assertEqual(bc["scenari"][4]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][4]["payback"],
                         base["payback"])
        self.assertEqual(bc["scenari"][4]["prezzo_coperto_eur_mwh"],
                         80.0)
        self.assertEqual(bc["scenari"][4]["prezzo_medio_eur_mwh"],
                         88.0)
        self.assertLess(bc["scenari"][5]["van"], base["van"])
        self.assertEqual(bc["scenari"][5]["payback"], 3)
        self.assertEqual(bc["scenari"][5]["verdetto"], "CONVIENTE")

    def test_sensibilita_valori(self):
        s = mh900_sensibilita(**mh900_demo())
        self.assertEqual(set(s.keys()),
                         {"mkt_piu20", "mkt_meno20",
                          "prod_meno20", "basis_piu10",
                          "fix_piu10", "c0_zero", "cann_zero",
                          "vita_005", "tasso_010", "evppa_20000",
                          "pmkt_065"})
        attesi = {
            "mkt_piu20": (3139841.63, 175.59, 1, "CONVIENTE"),
            "mkt_meno20": (-10626.22, 4.12, 9, "MARGINALE"),
            "prod_meno20": (1193964.43, 74.51, 2, "CONVIENTE"),
            "basis_piu10": (1564607.71, 93.87, 2, "CONVIENTE"),
            "fix_piu10": (637999.52, 44.87, 3, "CONVIENTE"),
            "c0_zero": (1814607.71, None, 1, "CONVIENTE"),
            "cann_zero": (1603216.38, 95.88, 2, "CONVIENTE"),
            "vita_005": (767427.02, 90.23, 2, "CONVIENTE"),
            "tasso_010": (1193973.27, 93.87, 2, "CONVIENTE"),
            "evppa_20000": (2800085.30, 157.99, 1, "CONVIENTE"),
            "pmkt_065": (None, None, None, "NON_CALCOLABILE"),
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
        csv = mh900_csv(bc, mh900_demo())
        for voce in ("e_cons_mwh_anno", "e_vppa_mwh_anno",
                     "p_fix_eur_mwh", "p_mkt_eur_mwh",
                     "p_supply_eur_mwh", "c0_eur",
                     "c_ann_eur_anno", "t_anni", "r_tasso",
                     "tol_frazione", "f_co2_t_mwh",
                     "basis_eur_mwh", "settlement_eur_anno",
                     "costo_merchant_eur_anno",
                     "costo_vppa_eur_anno",
                     "risparmio_eur_anno",
                     "prezzo_medio_eur_mwh",
                     "prezzo_coperto_eur_mwh",
                     "breakeven_prezzo_mercato",
                     "breakeven_basis",
                     "co2_evitata_t_anno", "co2_evitata_t_vita",
                     "van", "tir", "payback",
                     "scenario_base_van", "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_mercato_piu20_van",
                     "scenario_mercato_piu20_verdetto",
                     "scenario_mercato_meno20_van",
                     "scenario_mercato_meno20_verdetto",
                     "scenario_produzione_meno20_van",
                     "scenario_produzione_meno20_verdetto",
                     "scenario_basis_piu10_van",
                     "scenario_basis_piu10_verdetto",
                     "scenario_fisso_piu10_van",
                     "scenario_fisso_piu10_verdetto",
                     "anno_1_costo_merchant",
                     "anno_1_costo_vppa",
                     "anno_1_risparmio", "anno_1_settlement",
                     "anno_1_costo_annuo", "anno_1_flusso",
                     "anno_1_co2_evitata",
                     "anno_10_costo_merchant",
                     "anno_10_risparmio",
                     "anno_10_settlement", "anno_10_flusso",
                     "confronto_costo_merchant",
                     "confronto_costo_vppa",
                     "confronto_risparmio",
                     "confronto_settlement",
                     "confronto_basis",
                     "confronto_prezzo_medio",
                     "confronto_prezzo_coperto",
                     "confronto_c0", "confronto_c_ann",
                     "confronto_van",
                     "confronto_co2_evitata_t_anno",
                     "confronto_co2_evitata_t_vita",
                     "confronto_breakeven_prezzo_mercato",
                     "confronto_breakeven_basis",
                     "confronto_tir", "confronto_payback",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 10)
        self.assertEqual(len(bc["df_scenari"]), 6)
        self.assertEqual(len(bc["df_confronto"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 26)
        self.assertEqual(len(bc["df_costi"]), 2)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso (EUR)"].iloc[0],
            235000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[0],
            -15000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[1],
            220000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[-1],
            2100000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Risparmio (EUR/anno)"].iloc[0],
            240000.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Settlement CfD (EUR/anno)"].iloc[0],
            240000.00, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Costo merchant (EUR/anno)",
             "Costo con VPPA (EUR/anno)",
             "Risparmio (EUR/anno)",
             "Settlement CfD (EUR/anno)",
             "Basis (EUR/MWh)",
             "Prezzo medio (EUR/MWh)",
             "Prezzo coperto (EUR/MWh)",
             "Costo iniziale (EUR)",
             "Costo annuo (EUR/anno)",
             "VAN (EUR)",
             "TIR (%)",
             "Payback (anni)",
             "Breakeven prezzo mercato (EUR/MWh)",
             "Breakeven basis (EUR/MWh)",
             "CO2 evitata (t/anno)",
             "CO2 evitata vita (t)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            1800000.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[2],
            240000.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Energia consumata (MWh/anno)", voci)
        self.assertIn("Costo merchant (EUR/anno)", voci)
        self.assertIn("Prezzo coperto (EUR/MWh)", voci)
        self.assertIn("CO2 evitata vita (t)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))
        self.assertEqual(
            list(bc["df_costi"]["Voce"]),
            ["Merchant", "Con VPPA"])
        self.assertAlmostEqual(
            bc["df_costi"]["Costo (EUR/anno)"].iloc[0],
            1800000.00, places=2)
        self.assertAlmostEqual(
            bc["df_costi"]["Costo (EUR/anno)"].iloc[1],
            1560000.00, places=2)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh900_csv(bc, mh900_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_cons_mwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh900_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh900_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh900_calcola(**_demo_kwargs(c0_eur=0.0))
        self.assertEqual(bc["c0_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 1814607.71, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh900_calcola(**_demo_kwargs(c_ann_eur_anno=0.0))
        self.assertEqual(bc["c_ann_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 1603216.38, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh900_calcola(**_demo_kwargs(f_co2_t_mwh=0.0))
        self.assertEqual(bc["co2_evitata_t_anno"], 0.0)
        self.assertEqual(bc["co2_evitata_t_vita"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh900_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)
        self.assertAlmostEqual(bc["van"], 1564607.71, places=2)


class TestCasiLimite(unittest.TestCase):
    def test_mercato_uguale_fisso_non_calcolabile(self):
        # Prezzo di mercato 65: il risparmio e zero in
        # tutti gli anni, VAN None, NON_CALCOLABILE negli
        # helper e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(p_mkt_eur_mwh=65.0)
        bc = mh900_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["settlement_eur_anno"], 0.0)
        self.assertTrue(all(r["risparmio"] <= 0.0
                            for r in bc["serie"]))
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_prezzo_mercato"])
        self.assertIsNone(bc["breakeven_basis"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        # Basis e prezzo coperto restano calcolati anche
        # nel regime degenere (sono prezzi, non KPI di
        # ritorno).
        self.assertEqual(bc["basis_eur_mwh"], 25.0)
        self.assertEqual(bc["prezzo_coperto_eur_mwh"], 90.0)

    def test_mercato_sotto_fisso_non_calcolabile(self):
        kw = _demo_kwargs(p_mkt_eur_mwh=60.0)
        bc = mh900_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"], -60000.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_energia_coperta_zero_non_calcolabile(self):
        kw = _demo_kwargs(e_vppa_mwh_anno=0.0)
        bc = mh900_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["costo_vppa_eur_anno"],
                         bc["costo_merchant_eur_anno"])
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_mercato_meno_20_tolleranza_zero_non_conveniente(self):
        # Stessa VAN meno 10.626,22 del MARGINALE demo,
        # ma con tolleranza zero il confine si sposta:
        # ogni VAN negativa diventa NON_CONVIENTE.
        bc = mh900_calcola(
            **_demo_kwargs(p_mkt_eur_mwh=68.0,
                           tol_frazione=0.0))
        self.assertAlmostEqual(bc["van"], -10626.22, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_energia_coperta_totale_conveniente(self):
        bc = mh900_calcola(**_demo_kwargs(e_vppa_mwh_anno=20000.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 400000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 2800085.30, places=2)
        self.assertAlmostEqual(bc["tir"], 157.99, places=2)
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["prezzo_medio_eur_mwh"], 70.0,
                               places=2)

    def test_costo_iniziale_zero_tir_non_definita_payback_uno(self):
        bc = mh900_calcola(**_demo_kwargs(c0_eur=0.0))
        self.assertEqual(bc["c0_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(bc["breakeven_prezzo_mercato"],
                               65.42, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_durata_cinque_e_tasso_dieci(self):
        bc = mh900_calcola(**_demo_kwargs(t_anni=5))
        self.assertAlmostEqual(bc["van"], 767427.02, places=2)
        self.assertAlmostEqual(bc["tir"], 90.23, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh900_calcola(**_demo_kwargs(r_tasso=0.10))
        self.assertAlmostEqual(bc["van"], 1193973.27, places=2)
        self.assertAlmostEqual(bc["tir"], 93.87, places=2)
        self.assertEqual(bc["payback"], 2)

    def test_prezzo_fisso_alto_conveniente(self):
        bc = mh900_calcola(**_demo_kwargs(p_fix_eur_mwh=75.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 120000.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 637999.52, places=2)
        self.assertAlmostEqual(bc["tir"], 44.87, places=2)
        self.assertEqual(bc["payback"], 3)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(e_cons_mwh_anno="20000.0")
        self.assertRaises(ValueError, mh900_calcola, **kw)
        kw = _demo_kwargs(e_cons_mwh_anno=True)
        self.assertRaises(ValueError, mh900_calcola, **kw)
        val = mh900_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def900\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh900_demo().keys()), lette - set(mh900_demo().keys()))
        self.assertEqual(lette, set(mh900_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc900\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc900\["([^"]+)"\]', src))
        attese = set(mh900_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 899 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 900.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 906)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab900:"), 1)
        self.assertTrue(src.startswith("    # W905"))

    def test_ui_tab900_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab900:"), 1)
        self.assertIn("def mh900_demo(", src_h)
        self.assertIn("def mh900_calcola(", src_h)
        self.assertIn("tab900", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("VPPA (Virtual PPA): il prezzo fisso rinnovabile senza ritirare l'energia paga?", src)
        self.assertIn("🤝🌐 VPPA (Virtual PPA): il prezzo fisso rinnovabile senza ritirare l'energia paga?", src)
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
        chiavi = re.findall(r'key="(st900_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st900_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 17)
        self.assertIn('key="st900_calcola"', src)
        self.assertIn('key="st900_csv"', src)
        self.assertIn('key="st900_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg900"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos900", src)

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
