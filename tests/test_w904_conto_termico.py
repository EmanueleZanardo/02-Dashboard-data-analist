"""Test nuova scheda Conto Termico: l'incentivo GSE sul calore
rinnovabile paga davvero?
Repo path: tests/test_w904_conto_termico.py

Effetto ECONOMICO (non solo climatico): sostituire una caldaia
a gas con una pompa di calore aria acqua costa un CAPEX e
sposta il costo del calore dal gas (caro per kWh termico,
rendimento sotto 1) all'elettricita (COP sopra 1, quindi
meno kWh elettrici che kWh termici). Il risparmio annuo e la
differenza tra costo gas e costo elettrico meno l'eventuale
delta manutenzione, e ripaga il CAPEX solo se la VAN dei
flussi attualizzati supera quel CAPEX. Il Conto Termico 2.0
del GSE rimborsa una frazione del CAPEX in rate annuali
uguali (5 rate in demo): le rate entrano nei flussi degli
anni 1..5 e accorciano il payback, ma l'investimento resta
conveniente solo se il risparmio termico da solo regge il
confronto.
Demo: domanda termica 22.000 kWh/anno, rendimento caldaia
0,90, prezzo gas 0,12 EUR/kWh, COP 3,0, prezzo elettricita
0,25 EUR/kWh, CAPEX pompa di calore 10.000 EUR, incentivo
Conto Termico 0,40 in 5 rate annuali, tasso 0,05 (frazione),
vita 15 anni, fattore CO2 gas 0,202 kg/kWh, fattore CO2
elettricita 0,25 kg/kWh, delta manutenzione 0 EUR/anno.
Costo gas = 22.000 diviso 0,90 per 0,12 = 2.933,33 EUR/anno;
costo pompa di calore = 22.000 diviso 3,0 per 0,25 =
1.833,33 EUR/anno; risparmio = 2.933,33 meno 1.833,33 meno
0 = 1.100,00 EUR/anno; rata incentivo = 10.000 per 0,40
diviso 5 = 800,00 EUR/anno; incentivo totale = 4.000,00 EUR.
Flussi [meno 10.000, 1.900,00 per 5 anni, 1.100,00 per 10
anni]; cumulato anno 5 meno 500,00, anno 6 600,00, finale
10.500,00.
VAN = 4.881,21 EUR; TIR per bisezione su flussi con
intervallo da meno 0,9 a 5,0 (12,82 %); payback (primo anno con
cumulato netto maggiore o uguale a 0) = 6; breakeven prezzo
gas per bisezione su VAN(prezzo gas) = 0 tra 0 e 1 EUR/kWh =
0,10 EUR/kWh; costo calore livellato pompa di calore =
(CAPEX per CRF piu costo elettrico piu delta manutenzione)
diviso domanda = 0,13 EUR/kWh; costo calore livellato gas =
prezzo gas diviso rendimento = 0,13 EUR/kWh; CRF = 0,096342.
CO2 evitata anno = domanda per (fattore gas diviso rendimento
meno fattore elettricita diviso COP) diviso 1000 = 3,10
t/anno (INFORMATIVA, mai nel conto economico); CO2 evitata
vita = 46,57 t.
Scenari: base VAN 4.881,21, TIR 12,82 %, payback 6,
CONVIENTE; incentivo 65 % VAN 7.045,94, TIR 17,04 %,
payback 5, CONVIENTE; COP 2,5 VAN 1.075,33, TIR 6,92 %,
payback 9, MARGINALE; gas piu 30 % VAN 14.015,30, TIR
24,36 %, payback 4, CONVIENTE; elettricita piu 20 % VAN
1.075,33, TIR 6,92 %, payback 9, MARGINALE (in demo COP 2,5
e elettricita piu 20 % danno lo stesso risparmio, perche
entrambi moltiplicano il costo elettrico per 1,2).
Confronto: costo gas 2.933,33 contro costo pompa di calore
1.833,33, risparmio 1.100,00, rata incentivo 800,00,
incentivo totale 4.000,00, CAPEX 10.000,00, VAN 4.881,21,
CO2 evitata 3,10 t/anno.
Tasso in FRAZIONE (0,05 = 5 %), usato diretto, NON diviso
per 100. Incentivo in FRAZIONE (0,40 = 40 % del CAPEX),
usato diretto, NON diviso per 100. Prezzi, COP, rendimento
e fattori restano costanti per tutta la vita,
SEMPLIFICAZIONE DICHIARATA (prezzo gas volatile, COP reale
che scende col freddo, rendimento reale e manutenzione
reale variano nel mondo reale, qui valore medio costante);
l'incentivo entra solo nei flussi, quindi in VAN, TIR e
payback, e non entra nel costo del calore livellato.
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il risparmio e minore o
uguale a 0 (guard degenere: UI salta KPI, grafico, tabella
e CSV) oppure se un input e degenere (domanda nulla o
negativa, rendimento nullo o negativo o sopra 1, prezzo
gas negativo, COP nullo o negativo, prezzo elettricita
negativo, CAPEX negativo, incentivo negativo o sopra 1,
rate nulle o negative o non intere, tasso nullo o negativo
o maggiore o uguale a 1, vita nulla o negativa o non
intera, fattore CO2 gas negativo, fattore CO2 elettricita
negativo, delta manutenzione negativo); altrimenti
CONVIENTE se VAN maggiore di 0 e payback minore o uguale
a 7, MARGINALE se VAN maggiore di 0 e payback maggiore di
7, NON_CONVIENTE se VAN minore o uguale a 0.
Casi limite: COP 1,5 (risparmio meno 733,33 in tutti gli
anni, VAN None, NON_CALCOLABILE); prezzo gas zero (risparmio
meno 1.833,33, NON_CALCOLABILE); prezzo gas 0,08 (VAN meno
5.267,79, TIR meno 9,63 %, payback nessuno, NON_CONVIENTE);
incentivo zero (VAN 1.417,62, TIR 7,03 %, payback 10,
MARGINALE); domanda 10.000 (VAN meno 1.346,59, TIR 2,34 %,
payback 13, NON_CONVIENTE); delta manutenzione 500 (VAN
meno 308,62, TIR 4,42 %, payback 10, NON_CONVIENTE);
CAPEX zero (VAN 11.417,62, TIR non definita, payback 1,
livellato pompa di calore 0,08, breakeven 0,08); vita 10
(VAN 1.957,49, TIR 9,44 %, payback 6); tasso 0,10 (VAN
1.399,32, TIR 12,82 %, payback 6); COP 4,0 (VAN 9.638,55,
TIR 19,12 %, payback 5).
Distinzione esplicita: qui SOLO la sostituzione della
caldaia a gas con pompa di calore aria acqua e l'incentivo
Conto Termico 2.0 del GSE in rate annuali (VAN sul RISPARMIO
con CAPEX della pompa di calore), NIENTE Ecobonus o
detrazione fiscale (li il beneficio e una detrazione
d'imposta in 10 anni: qui un contributo GSE in 5 rate),
NIENTE pompa di calore senza incentivo (li il risparmio da
solo deve ripagare il CAPEX: qui le rate aiutano ma il
risparmio resta il driver), NIENTE fotovoltaico piu
accumulo (li il risparmio e sull'autoconsumo elettrico:
qui solo il calore), NIENTE biomassa (li il combustibile
e legna o pellet: qui gas contro elettricita).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w904_helpers import (
        demo_calcoli,
        mh899_breakeven_prezzo_gas,
        mh899_calcola,
        mh899_confronto,
        mh899_co2_evitata_anno,
        mh899_co2_evitata_vita,
        mh899_costo_calore_livellato_gas,
        mh899_costo_calore_livellato_pdc,
        mh899_costo_gas,
        mh899_costo_pdc,
        mh899_crf,
        mh899_csv,
        mh899_demo,
        mh899_demo_calcoli,
        mh899_flussi,
        mh899_fraz,
        mh899_fraz_pos,
        mh899_int_pos,
        mh899_nneg,
        mh899_num,
        mh899_payback,
        mh899_pos,
        mh899_rata_incentivo,
        mh899_riga_anno,
        mh899_risparmio,
        mh899_scenario,
        mh899_sensibilita,
        mh899_serie_annua,
        mh899_tasso,
        mh899_tir,
        mh899_valida,
        mh899_van,
        mh899_van_a_prezzo_gas,
        mh899_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w904_helpers", os.path.join(_hf, "w904_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh899_breakeven_prezzo_gas = _mod.mh899_breakeven_prezzo_gas
    mh899_calcola = _mod.mh899_calcola
    mh899_confronto = _mod.mh899_confronto
    mh899_co2_evitata_anno = _mod.mh899_co2_evitata_anno
    mh899_co2_evitata_vita = _mod.mh899_co2_evitata_vita
    mh899_costo_calore_livellato_gas = _mod.mh899_costo_calore_livellato_gas
    mh899_costo_calore_livellato_pdc = _mod.mh899_costo_calore_livellato_pdc
    mh899_costo_gas = _mod.mh899_costo_gas
    mh899_costo_pdc = _mod.mh899_costo_pdc
    mh899_crf = _mod.mh899_crf
    mh899_csv = _mod.mh899_csv
    mh899_demo = _mod.mh899_demo
    mh899_demo_calcoli = _mod.mh899_demo_calcoli
    mh899_flussi = _mod.mh899_flussi
    mh899_fraz = _mod.mh899_fraz
    mh899_fraz_pos = _mod.mh899_fraz_pos
    mh899_int_pos = _mod.mh899_int_pos
    mh899_nneg = _mod.mh899_nneg
    mh899_num = _mod.mh899_num
    mh899_payback = _mod.mh899_payback
    mh899_pos = _mod.mh899_pos
    mh899_rata_incentivo = _mod.mh899_rata_incentivo
    mh899_riga_anno = _mod.mh899_riga_anno
    mh899_risparmio = _mod.mh899_risparmio
    mh899_scenario = _mod.mh899_scenario
    mh899_sensibilita = _mod.mh899_sensibilita
    mh899_serie_annua = _mod.mh899_serie_annua
    mh899_tasso = _mod.mh899_tasso
    mh899_tir = _mod.mh899_tir
    mh899_valida = _mod.mh899_valida
    mh899_van = _mod.mh899_van
    mh899_van_a_prezzo_gas = _mod.mh899_van_a_prezzo_gas
    mh899_verdetto = _mod.mh899_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w904_helpers.py")
_UI_PATH = _risolvi("w904_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "8"
_VECCHIO_TAB = "tab89" + "8"
_VECCHIO_ST = "st89" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "costo_gas_eur_anno": 2933.3333333333335,
    "costo_pdc_eur_anno": 1833.3333333333333,
    "risparmio_eur_anno": 1100.0000000000002,
    "rata_incentivo_eur_anno": 800.0,
    "incentivo_totale_eur": 4000.0,
    "crf": 0.09634228760924432,
    "costo_calore_livellato_pdc": 0.1271252822466262,
    "costo_calore_livellato_gas": 0.13333333333333333,
    "breakeven_prezzo_gas": 0.10076182609691386,
    "co2_evitata_t_anno": 3.104444444444445,
    "co2_evitata_t_vita": 46.56666666666667,
    "van": 4881.205178503305,
    "tir": 12.823192098508684,
    "payback": 6,
}

_DEMO_SCENARI = [
    {"nome": "Base", "incentivo_frazione": 0.4,
     "cop_pdc": 3.0, "prezzo_gas_eur_kwh": 0.12,
     "prezzo_elettricita_eur_kwh": 0.25,
     "risparmio_eur_anno": 1100.0000000000002,
     "van": 4881.205178503305, "tir": 12.823192098508684,
     "payback": 6, "verdetto": "CONVIENTE",
     "breakeven_prezzo_gas": 0.10076182609691386,
     "costo_calore_livellato_pdc": 0.1271252822466262},
    {"nome": "Incentivo 65%", "incentivo_frazione": 0.65,
     "cop_pdc": 3.0, "prezzo_gas_eur_kwh": 0.12,
     "prezzo_elettricita_eur_kwh": 0.25,
     "risparmio_eur_anno": 1100.0000000000002,
     "van": 7045.943513818715, "tir": 17.04366167423757,
     "payback": 5, "verdetto": "CONVIENTE",
     "breakeven_prezzo_gas": 0.09222999614348737,
     "costo_calore_livellato_pdc": 0.1271252822466262},
    {"nome": "COP 2,5", "incentivo_frazione": 0.4,
     "cop_pdc": 2.5, "prezzo_gas_eur_kwh": 0.12,
     "prezzo_elettricita_eur_kwh": 0.25,
     "risparmio_eur_anno": 733.3333333333335,
     "van": 1075.3305645037574, "tir": 6.920416292435333,
     "payback": 9, "verdetto": "MARGINALE",
     "breakeven_prezzo_gas": 0.11576182609724128,
     "costo_calore_livellato_pdc": 0.1437919489132929},
    {"nome": "Gas piu 30%", "incentivo_frazione": 0.4,
     "cop_pdc": 3.0, "prezzo_gas_eur_kwh": 0.156,
     "prezzo_elettricita_eur_kwh": 0.25,
     "risparmio_eur_anno": 1980.0000000000002,
     "van": 14015.304252102227, "tir": 24.357500925360114,
     "payback": 4, "verdetto": "CONVIENTE",
     "breakeven_prezzo_gas": 0.10076182609691386,
     "costo_calore_livellato_pdc": 0.1271252822466262},
    {"nome": "Elettricita piu 20%", "incentivo_frazione": 0.4,
     "cop_pdc": 3.0, "prezzo_gas_eur_kwh": 0.12,
     "prezzo_elettricita_eur_kwh": 0.3,
     "risparmio_eur_anno": 733.3333333333335,
     "van": 1075.3305645037574, "tir": 6.920416292435333,
     "payback": 9, "verdetto": "MARGINALE",
     "breakeven_prezzo_gas": 0.11576182609724128,
     "costo_calore_livellato_pdc": 0.1437919489132929},
]

_DEMO_CONFRONTO = {
    "costo_gas": 2933.3333333333335,
    "costo_pdc": 1833.3333333333333,
    "risparmio": 1100.0000000000002,
    "rata_incentivo": 800.0,
    "incentivo_totale": 4000.0,
    "van": 4881.205178503305,
    "capex": 10000.0,
    "co2_evitata_t_anno": 3.104444444444445,
    "co2_evitata_t_vita": 46.56666666666667,
    "costo_calore_livellato_pdc": 0.1271252822466262,
    "costo_calore_livellato_gas": 0.13333333333333333,
    "breakeven_prezzo_gas": 0.10076182609691386,
    "tir": 12.823192098508684,
    "payback": 6,
}

_ORDINE_VALIDA = (
    "domanda_kwh_anno", "rendimento_caldaia",
    "prezzo_gas_eur_kwh", "cop_pdc",
    "prezzo_elettricita_eur_kwh", "capex_eur",
    "incentivo_frazione", "anni_incentivo", "tasso",
    "vita_anni", "fattore_co2_gas",
    "fattore_co2_elettricita",
    "delta_manutenzione_eur_anno")


def _demo_kwargs(**over):
    kw = dict(mh899_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh899_num(3, "x"), 3.0)
        self.assertEqual(mh899_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh899_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh899_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh899_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh899_pos(0, "x")
        with self.assertRaises(ValueError):
            mh899_pos(-1, "x")
        self.assertEqual(mh899_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh899_fraz(0, "x"), 0.0)
        self.assertEqual(mh899_fraz(1, "x"), 1.0)
        self.assertEqual(mh899_fraz(0.40, "x"), 0.40)
        with self.assertRaises(ValueError):
            mh899_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh899_fraz(1.01, "x")

    def test_fraz_pos_zero_no_uno_ok(self):
        self.assertEqual(mh899_fraz_pos(1, "x"), 1.0)
        self.assertEqual(mh899_fraz_pos(0.90, "x"), 0.90)
        with self.assertRaises(ValueError):
            mh899_fraz_pos(0, "x")
        with self.assertRaises(ValueError):
            mh899_fraz_pos(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh899_int_pos(15, "x"), 15)
        self.assertEqual(mh899_int_pos(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh899_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh899_int_pos(5.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh899_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh899_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh899_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh899_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh899_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh899_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_costo_gas(self):
        self.assertAlmostEqual(
            mh899_costo_gas(22000.0, 0.90, 0.12), 2933.33,
            places=2)
        self.assertAlmostEqual(
            mh899_costo_gas(22000.0, 1.0, 0.12), 2640.00,
            places=2)
        self.assertEqual(mh899_costo_gas(22000.0, 0.90, 0.0),
                         0.0)
        self.assertEqual(mh899_costo_gas(10000.0, 0.90, 0.12),
                         1333.3333333333333)
        with self.assertRaises(ValueError):
            mh899_costo_gas(0, 0.90, 0.12)
        with self.assertRaises(ValueError):
            mh899_costo_gas(22000.0, 0, 0.12)
        with self.assertRaises(ValueError):
            mh899_costo_gas(22000.0, 1.1, 0.12)
        with self.assertRaises(ValueError):
            mh899_costo_gas(22000.0, 0.90, -0.01)

    def test_costo_pdc(self):
        self.assertAlmostEqual(
            mh899_costo_pdc(22000.0, 3.0, 0.25), 1833.33,
            places=2)
        self.assertAlmostEqual(
            mh899_costo_pdc(22000.0, 2.5, 0.25), 2200.00,
            places=2)
        self.assertAlmostEqual(
            mh899_costo_pdc(22000.0, 4.0, 0.25), 1375.00,
            places=2)
        self.assertEqual(mh899_costo_pdc(22000.0, 3.0, 0.0),
                         0.0)
        with self.assertRaises(ValueError):
            mh899_costo_pdc(0, 3.0, 0.25)
        with self.assertRaises(ValueError):
            mh899_costo_pdc(22000.0, 0, 0.25)
        with self.assertRaises(ValueError):
            mh899_costo_pdc(22000.0, 3.0, -0.01)

    def test_risparmio_e_rata(self):
        self.assertAlmostEqual(
            mh899_risparmio(2933.33, 1833.33, 0.0), 1100.00,
            places=2)
        self.assertEqual(
            mh899_risparmio(2933.3333333333335,
                            1833.3333333333333, 0.0),
            1100.0000000000002)
        self.assertEqual(
            mh899_risparmio(2933.33, 1833.33, 500.0), 600.00)
        self.assertEqual(
            mh899_risparmio(1000.0, 2000.0, 0.0), -1000.0)
        self.assertEqual(
            mh899_rata_incentivo(10000.0, 0.40, 5), 800.0)
        self.assertEqual(
            mh899_rata_incentivo(10000.0, 0.65, 5), 1300.0)
        self.assertEqual(
            mh899_rata_incentivo(10000.0, 0.0, 5), 0.0)
        self.assertEqual(
            mh899_rata_incentivo(0.0, 0.40, 5), 0.0)
        with self.assertRaises(ValueError):
            mh899_risparmio(-1.0, 1833.33, 0.0)
        with self.assertRaises(ValueError):
            mh899_risparmio(2933.33, 1833.33, -1.0)
        with self.assertRaises(ValueError):
            mh899_rata_incentivo(10000.0, 1.5, 5)
        with self.assertRaises(ValueError):
            mh899_rata_incentivo(10000.0, 0.40, 0)

    def test_riga_anno(self):
        riga = mh899_riga_anno(1, 1100.0, 800.0, 5, 3.10)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["risparmio"], 1100.0)
        self.assertEqual(riga["incentivo"], 800.0)
        self.assertEqual(riga["flusso"], 1900.0)
        self.assertEqual(riga["co2_evitata"], 3.10)
        riga = mh899_riga_anno(6, 1100.0, 800.0, 5, 3.10)
        self.assertEqual(riga["incentivo"], 0.0)
        self.assertEqual(riga["flusso"], 1100.0)
        # Anno 5: ultima rata.
        riga = mh899_riga_anno(5, 1100.0, 800.0, 5, 3.10)
        self.assertEqual(riga["incentivo"], 800.0)
        with self.assertRaises(ValueError):
            mh899_riga_anno(0, 1100.0, 800.0, 5, 3.10)

    def test_serie_annua(self):
        serie = mh899_serie_annua(1100.0, 800.0, 5, 15, 3.10)
        self.assertEqual(len(serie), 15)
        self.assertEqual(serie[0]["flusso"], 1900.0)
        self.assertEqual(serie[4]["flusso"], 1900.0)
        self.assertEqual(serie[5]["flusso"], 1100.0)
        self.assertEqual(serie[14]["flusso"], 1100.0)
        self.assertTrue(all(r["co2_evitata"] == 3.10
                            for r in serie))
        # Con una sola rata l'incentivo c'e solo l'anno 1.
        serie = mh899_serie_annua(1100.0, 4000.0, 1, 3, 3.10)
        self.assertEqual(serie[0]["incentivo"], 4000.0)
        self.assertEqual(serie[1]["incentivo"], 0.0)
        with self.assertRaises(ValueError):
            mh899_serie_annua(1100.0, 800.0, 5, 0, 3.10)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        flussi = bc["flussi"]
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -10000.0)
        self.assertEqual(flussi[1], 1900.0000000000002)
        self.assertEqual(flussi[5], 1900.0000000000002)
        self.assertEqual(flussi[6], 1100.0000000000002)
        self.assertAlmostEqual(sum(flussi), 10500.00, places=2)
        # Cumulato anno 5 negativo, anno 6 positivo: payback 6.
        self.assertAlmostEqual(sum(flussi[:6]), -500.00, places=2)
        self.assertAlmostEqual(sum(flussi[:7]), 600.00, places=2)
        self.assertLess(sum(flussi[:6]), 0.0)
        flussi2 = mh899_flussi(bc["serie"], bc["capex_eur"], 15)
        self.assertEqual(flussi2, flussi)
        self.assertAlmostEqual(mh899_van(flussi, 0.05), bc["van"])
        with self.assertRaises(ValueError):
            mh899_flussi(bc["serie"][:14], bc["capex_eur"], 15)

    def test_crf_e_livellati(self):
        self.assertAlmostEqual(mh899_crf(0.05, 15), 0.096342,
                               places=6)
        self.assertAlmostEqual(mh899_crf(0.10, 15), 0.131474,
                               places=6)
        self.assertAlmostEqual(mh899_crf(0.05, 10), 0.129505,
                               places=6)
        self.assertAlmostEqual(
            mh899_costo_calore_livellato_pdc(
                10000.0, 0.09634228760924432, 1833.3333333333333,
                0.0, 22000.0),
            0.13, places=2)
        self.assertAlmostEqual(
            mh899_costo_calore_livellato_pdc(
                0.0, 0.09634228760924432, 1833.3333333333333,
                0.0, 22000.0),
            0.08, places=2)
        self.assertAlmostEqual(
            mh899_costo_calore_livellato_gas(0.12, 0.90),
            0.13, places=2)
        self.assertAlmostEqual(
            mh899_costo_calore_livellato_gas(0.0, 0.90),
            0.0, places=2)
        with self.assertRaises(ValueError):
            mh899_costo_calore_livellato_pdc(
                10000.0, 0.096342, 1833.33, 0.0, 0.0)
        with self.assertRaises(ValueError):
            mh899_costo_calore_livellato_gas(0.12, 0.0)
        with self.assertRaises(ValueError):
            mh899_crf(0.0, 15)
        with self.assertRaises(ValueError):
            mh899_crf(0.05, 0)

    def test_breakeven_prezzo_gas(self):
        self.assertAlmostEqual(
            mh899_breakeven_prezzo_gas(mh899_demo()), 0.10,
            places=2)
        # Con incentivo zero il breakeven sale.
        self.assertAlmostEqual(
            mh899_breakeven_prezzo_gas(
                dict(mh899_demo(), incentivo_frazione=0.0)),
            0.11, places=2)
        # Con COP 4,0 il breakeven scende.
        self.assertAlmostEqual(
            mh899_breakeven_prezzo_gas(
                dict(mh899_demo(), cop_pdc=4.0)),
            0.08, places=2)
        # VAN al breakeven esatto circa zero; VAN(0,12)
        # positiva; VAN(0) negativa.
        be = mh899_breakeven_prezzo_gas(mh899_demo())
        self.assertAlmostEqual(
            mh899_van_a_prezzo_gas(be, mh899_demo()), 0.0,
            places=0)
        self.assertGreater(
            mh899_van_a_prezzo_gas(0.12, mh899_demo()), 0.0)
        self.assertLess(
            mh899_van_a_prezzo_gas(0.0, mh899_demo()), 0.0)
        with self.assertRaises(ValueError):
            mh899_breakeven_prezzo_gas("non un dict")
        with self.assertRaises(ValueError):
            mh899_van_a_prezzo_gas(-0.01, mh899_demo())

    def test_co2_evitata_informativa(self):
        self.assertAlmostEqual(
            mh899_co2_evitata_anno(22000.0, 0.90, 0.202, 3.0,
                                   0.25),
            3.10, places=2)
        self.assertAlmostEqual(
            mh899_co2_evitata_anno(22000.0, 0.90, 0.202, 4.0,
                                   0.25),
            3.56, places=2)
        self.assertEqual(
            mh899_co2_evitata_anno(22000.0, 0.90, 0.202, 3.0,
                                   0.0),
            22000.0 * (0.202 / 0.90) / 1000.0)
        self.assertAlmostEqual(
            mh899_co2_evitata_vita(3.104444444444445, 15),
            46.57, places=2)
        self.assertAlmostEqual(
            mh899_co2_evitata_vita(3.104444444444445, 10),
            31.04, places=2)
        with self.assertRaises(ValueError):
            mh899_co2_evitata_anno(22000.0, 0.90, -0.1, 3.0,
                                   0.25)
        with self.assertRaises(ValueError):
            mh899_co2_evitata_anno(0, 0.90, 0.202, 3.0, 0.25)
        with self.assertRaises(ValueError):
            mh899_co2_evitata_vita(3.10, 0)

    def test_scenario_singolo(self):
        s = mh899_scenario("Incentivo 65%", mh899_demo(),
                           {"incentivo_frazione": 0.65})
        self.assertEqual(s["nome"], "Incentivo 65%")
        self.assertEqual(s["incentivo_frazione"], 0.65)
        self.assertAlmostEqual(s["van"], 7045.94, places=2)
        self.assertEqual(s["payback"], 5)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh899_scenario("COP 2,5", mh899_demo(),
                           {"cop_pdc": 2.5})
        self.assertAlmostEqual(s["van"], 1075.33, places=2)
        self.assertEqual(s["verdetto"], "MARGINALE")
        s = mh899_scenario("Gas piu 30%", mh899_demo(),
                           {"prezzo_gas_eur_kwh": 0.156})
        self.assertAlmostEqual(s["van"], 14015.30, places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        with self.assertRaises(ValueError):
            mh899_scenario("", mh899_demo(),
                           {"cop_pdc": 2.5})
        with self.assertRaises(ValueError):
            mh899_scenario("X", mh899_demo(),
                           {"rendimento_caldaia": 1.5})

    def test_scenario_risparmio_negativo_non_calcolabile(self):
        s = mh899_scenario("COP basso", mh899_demo(),
                           {"cop_pdc": 1.5})
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh899_confronto(2933.33, 1833.33, 1100.00, 800.00,
                            4000.00, 4881.21, 10000.0, 3.10,
                            46.57, 0.13, 0.13, 0.10, 12.82, 6)
        self.assertEqual(c["costo_gas"], 2933.33)
        self.assertEqual(c["costo_pdc"], 1833.33)
        self.assertEqual(c["risparmio"], 1100.00)
        self.assertEqual(c["rata_incentivo"], 800.00)
        self.assertEqual(c["incentivo_totale"], 4000.00)
        self.assertEqual(c["van"], 4881.21)
        self.assertEqual(c["capex"], 10000.0)
        self.assertEqual(c["co2_evitata_t_anno"], 3.10)
        self.assertEqual(c["co2_evitata_t_vita"], 46.57)
        self.assertEqual(c["costo_calore_livellato_pdc"], 0.13)
        self.assertEqual(c["costo_calore_livellato_gas"], 0.13)
        self.assertEqual(c["breakeven_prezzo_gas"], 0.10)
        self.assertEqual(c["tir"], 12.82)
        self.assertEqual(c["payback"], 6)
        c = mh899_confronto(2933.33, 1833.33, -733.33, 800.00,
                            4000.00, 0.0, 10000.0, 1.27,
                            19.07, 0.21, 0.13, None, None, None)
        self.assertIsNone(c["breakeven_prezzo_gas"])
        self.assertIsNone(c["tir"])
        self.assertIsNone(c["payback"])
        with self.assertRaises(ValueError):
            mh899_confronto(-1.0, 1833.33, 1100.00, 800.00,
                            4000.00, 4881.21, 10000.0, 3.10,
                            46.57, 0.13, 0.13, 0.10, 12.82, 6)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_cinque(self):
        bc = mh899_demo_calcoli()
        self.assertAlmostEqual(
            mh899_van(bc["flussi"], 0.05),
            bc["van"])
        bc_basso = mh899_calcola(
            _scenari=False,
            **dict(mh899_demo(), cop_pdc=2.5))
        self.assertAlmostEqual(
            mh899_van(bc_basso["flussi"], 0.05),
            bc["scenari"][2]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh899_van([-10000, 1900, 1900], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 4881,21; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh899_demo_calcoli()
        self.assertAlmostEqual(
            mh899_van(bc["flussi"], 0.05),
            4881.21, places=2)
        self.assertNotAlmostEqual(
            mh899_van(bc["flussi"], 0.50),
            4881.21, places=2)
        with self.assertRaises(ValueError):
            mh899_van(bc["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh899_demo_calcoli()
        tir = mh899_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh899_tir([-100, -10, -10]))
        self.assertIsNone(mh899_tir([100, 10, 10]))
        self.assertIsNone(mh899_tir([0, 10, 10]))

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh899_demo_calcoli()
        self.assertEqual(mh899_payback(bc["flussi"]), 6)
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh899_payback([-100, 100, 10]), 1)
        self.assertEqual(mh899_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh899_payback([-100, 10, 10]))
        # Con CAPEX zero il payback e l'anno 1.
        self.assertEqual(mh899_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh899_demo_calcoli()
        f0 = bc["flussi"]
        self.assertAlmostEqual(sum(f0[:6]), -500.00, places=2)
        self.assertAlmostEqual(sum(f0[:7]), 600.00, places=2)
        self.assertAlmostEqual(sum(f0), 10500.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(mh899_verdetto(100.0, 6), "CONVIENTE")
        self.assertEqual(mh899_verdetto(100.0, 7), "CONVIENTE")
        self.assertEqual(mh899_verdetto(100.0, 8), "MARGINALE")
        self.assertEqual(mh899_verdetto(100.0, None), "MARGINALE")
        self.assertEqual(mh899_verdetto(-1.0, 6),
                         "NON_CONVIENTE")
        # VAN zero: NON_CONVIENTE in questa scheda (VAN
        # maggiore di 0 per convenire, come da brief).
        self.assertEqual(mh899_verdetto(0.0, 6),
                         "NON_CONVIENTE")
        self.assertEqual(mh899_verdetto(0.0, None),
                         "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh899_verdetto(100.0, 0)
        with self.assertRaises(ValueError):
            mh899_verdetto(100.0, -1)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(mh899_verdetto(None, 6),
                         "NON_CALCOLABILE")
        self.assertEqual(mh899_verdetto(None, None),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh899_demo()
        val = mh899_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh899_calcola, **kw)
        kw = _demo_kwargs(vita_anni=15.5)
        self.assertRaises(ValueError, mh899_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10)
        bc = mh899_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_rate_zero_e_non_intere_no(self):
        for rate in (0, 5.5):
            with self.assertRaises(ValueError):
                mh899_calcola(**_demo_kwargs(anni_incentivo=rate))
        bc = mh899_calcola(**_demo_kwargs(anni_incentivo=1))
        self.assertEqual(bc["anni_incentivo"], 1)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh899_calcola(**_demo_kwargs(tasso=tasso))
        bc = mh899_calcola(**_demo_kwargs(tasso=0.10))
        self.assertEqual(bc["tasso"], 0.10)

    def test_valida_rendimento_bordi_no(self):
        for rend in (0, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh899_calcola(
                    **_demo_kwargs(rendimento_caldaia=rend))
        bc = mh899_calcola(**_demo_kwargs(rendimento_caldaia=1.0))
        self.assertEqual(bc["rendimento_caldaia"], 1.0)

    def test_valida_cop_zero_no(self):
        with self.assertRaises(ValueError):
            mh899_calcola(**_demo_kwargs(cop_pdc=0))
        bc = mh899_calcola(**_demo_kwargs(cop_pdc=4.0))
        self.assertEqual(bc["cop_pdc"], 4.0)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("domanda_kwh_anno", 0),
                              ("rendimento_caldaia", 0),
                              ("cop_pdc", 0),
                              ("anni_incentivo", 0),
                              ("vita_anni", 0),
                              ("tasso", 0)):
            with self.assertRaises(ValueError):
                mh899_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_gas_eur_kwh=float("nan"))
        self.assertRaises(ValueError, mh899_calcola, **kw)
        kw = _demo_kwargs(incentivo_frazione=float("inf"))
        self.assertRaises(ValueError, mh899_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("domanda_kwh_anno", -1),
                              ("rendimento_caldaia", -0.1),
                              ("prezzo_gas_eur_kwh", -1),
                              ("cop_pdc", -1),
                              ("prezzo_elettricita_eur_kwh", -1),
                              ("capex_eur", -1),
                              ("incentivo_frazione", -0.1),
                              ("anni_incentivo", -1),
                              ("tasso", -0.01),
                              ("vita_anni", -1),
                              ("fattore_co2_gas", -0.1),
                              ("fattore_co2_elettricita", -0.1),
                              ("delta_manutenzione_eur_anno", -1)):
            with self.assertRaises(ValueError):
                mh899_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_frazioni_sopra_uno_no(self):
        for campo in ("rendimento_caldaia",
                      "incentivo_frazione"):
            with self.assertRaises(ValueError):
                mh899_calcola(**_demo_kwargs(**{campo: 1.5}))

    def test_calcola_accetta_dict(self):
        bc = mh899_calcola(mh899_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh899_calcola(dict(mh899_demo(), cop_pdc=99.0),
                           cop_pdc=3.0)
        self.assertEqual(bc["cop_pdc"], 3.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh899_calcola(_scenari=False, **mh899_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van"], 4881.21, places=2)


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
        self.assertEqual(bc["payback"], 6)
        self.assertAlmostEqual(bc["tir"], 12.82, places=2)
        self.assertAlmostEqual(bc["breakeven_prezzo_gas"], 0.10,
                               places=2)
        self.assertAlmostEqual(
            bc["costo_calore_livellato_pdc"], 0.13, places=2)
        self.assertAlmostEqual(
            bc["costo_calore_livellato_gas"], 0.13, places=2)
        self.assertAlmostEqual(bc["crf"], 0.096342, places=6)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["costo_gas_eur_anno"],
            bc["domanda_kwh_anno"] / bc["rendimento_caldaia"]
            * bc["prezzo_gas_eur_kwh"])
        self.assertAlmostEqual(
            bc["costo_pdc_eur_anno"],
            bc["domanda_kwh_anno"] / bc["cop_pdc"]
            * bc["prezzo_elettricita_eur_kwh"])
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["costo_gas_eur_anno"]
            - bc["costo_pdc_eur_anno"]
            - bc["delta_manutenzione_eur_anno"])
        self.assertAlmostEqual(
            bc["rata_incentivo_eur_anno"],
            bc["capex_eur"] * bc["incentivo_frazione"]
            / bc["anni_incentivo"])
        self.assertAlmostEqual(
            bc["incentivo_totale_eur"],
            bc["capex_eur"] * bc["incentivo_frazione"])
        self.assertAlmostEqual(
            bc["costo_calore_livellato_pdc"],
            (bc["capex_eur"] * bc["crf"]
             + bc["costo_pdc_eur_anno"]
             + bc["delta_manutenzione_eur_anno"])
            / bc["domanda_kwh_anno"])
        self.assertAlmostEqual(
            bc["costo_calore_livellato_gas"],
            bc["prezzo_gas_eur_kwh"]
            / bc["rendimento_caldaia"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["domanda_kwh_anno"]
            * (bc["fattore_co2_gas"] / bc["rendimento_caldaia"]
               - bc["fattore_co2_elettricita"] / bc["cop_pdc"])
            / 1000.0)
        self.assertAlmostEqual(
            bc["co2_evitata_t_vita"],
            bc["co2_evitata_t_anno"] * bc["vita_anni"])
        self.assertAlmostEqual(
            bc["van"],
            mh899_van(bc["flussi"], bc["tasso"]))
        self.assertAlmostEqual(
            bc["breakeven_prezzo_gas"],
            mh899_breakeven_prezzo_gas(mh899_demo()))
        for t in range(1, bc["vita_anni"] + 1):
            riga = bc["serie"][t - 1]
            with self.subTest(anno=t):
                self.assertAlmostEqual(
                    riga["flusso"],
                    riga["risparmio"] + riga["incentivo"])
                if t <= bc["anni_incentivo"]:
                    self.assertEqual(
                        riga["incentivo"],
                        bc["rata_incentivo_eur_anno"])
                else:
                    self.assertEqual(riga["incentivo"], 0.0)
        conf = bc["confronto"]
        self.assertEqual(conf["van"], bc["van"])
        self.assertEqual(conf["capex"], bc["capex_eur"])
        self.assertEqual(conf["tir"], bc["tir"])
        self.assertEqual(conf["payback"], bc["payback"])

    def test_scenari_ordinamento(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # L'incentivo 65 % migliora sul base, il COP 2,5
        # peggiora e diventa MARGINALE, il gas piu 30 %
        # migliora piu di tutti, l'elettricita piu 20 %
        # coincide col COP 2,5 (stesso fattore 1,2 sul
        # costo elettrico in demo).
        self.assertGreater(bc["scenari"][1]["van"], base["van"])
        self.assertGreater(bc["scenari"][1]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][1]["payback"], 5)
        self.assertLess(bc["scenari"][2]["van"], base["van"])
        self.assertLess(bc["scenari"][2]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][2]["payback"], 9)
        self.assertEqual(bc["scenari"][2]["verdetto"], "MARGINALE")
        self.assertGreater(bc["scenari"][3]["van"],
                           bc["scenari"][1]["van"])
        self.assertEqual(bc["scenari"][3]["payback"], 4)
        self.assertEqual(bc["scenari"][4]["van"],
                         bc["scenari"][2]["van"])
        self.assertEqual(bc["scenari"][4]["tir"],
                         bc["scenari"][2]["tir"])
        self.assertEqual(bc["scenari"][4]["payback"],
                         bc["scenari"][2]["payback"])
        self.assertEqual(bc["scenari"][4]["verdetto"], "MARGINALE")

    def test_sensibilita_valori(self):
        s = mh899_sensibilita(**mh899_demo())
        self.assertEqual(set(s.keys()),
                         {"incentivo_065", "cop_025", "gas_piu30",
                          "elec_piu20", "vita_010", "tasso_010",
                          "capex_000", "incentivo_000",
                          "domanda_10000", "cop_040", "delta_500"})
        attesi = {
            "incentivo_065": (7045.94, 17.04, 5, "CONVIENTE"),
            "cop_025": (1075.33, 6.92, 9, "MARGINALE"),
            "gas_piu30": (14015.30, 24.36, 4, "CONVIENTE"),
            "elec_piu20": (1075.33, 6.92, 9, "MARGINALE"),
            "vita_010": (1957.49, 9.44, 6, "CONVIENTE"),
            "tasso_010": (1399.32, 12.82, 6, "CONVIENTE"),
            "capex_000": (11417.62, None, 1, "CONVIENTE"),
            "incentivo_000": (1417.62, 7.03, 10, "MARGINALE"),
            "domanda_10000": (-1346.59, 2.34, 13, "NON_CONVIENTE"),
            "cop_040": (9638.55, 19.12, 5, "CONVIENTE"),
            "delta_500": (-308.62, 4.42, 10, "NON_CONVIENTE"),
        }
        for nome, (van, tir, pb, verd) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(s[nome]["van"], van, places=2)
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
        csv = mh899_csv(bc, mh899_demo())
        for voce in ("domanda_kwh_anno", "rendimento_caldaia",
                     "prezzo_gas_eur_kwh", "cop_pdc",
                     "prezzo_elettricita_eur_kwh", "capex_eur",
                     "incentivo_frazione", "anni_incentivo",
                     "tasso", "vita_anni", "fattore_co2_gas",
                     "fattore_co2_elettricita",
                     "delta_manutenzione_eur_anno",
                     "costo_gas_eur_anno", "costo_pdc_eur_anno",
                     "risparmio_eur_anno",
                     "rata_incentivo_eur_anno",
                     "incentivo_totale_eur", "crf",
                     "costo_calore_livellato_pdc",
                     "costo_calore_livellato_gas",
                     "breakeven_prezzo_gas",
                     "co2_evitata_t_anno", "co2_evitata_t_vita",
                     "van", "tir", "payback",
                     "scenario_base_van", "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_incentivo_65_van",
                     "scenario_incentivo_65_verdetto",
                     "scenario_cop_25_van",
                     "scenario_cop_25_verdetto",
                     "scenario_gas_piu30_van",
                     "scenario_gas_piu30_verdetto",
                     "scenario_elettricita_piu20_van",
                     "scenario_elettricita_piu20_verdetto",
                     "anno_1_costo_gas", "anno_1_costo_pdc",
                     "anno_1_risparmio", "anno_1_incentivo",
                     "anno_1_flusso", "anno_1_co2_evitata",
                     "anno_15_costo_gas", "anno_15_risparmio",
                     "anno_15_incentivo", "anno_15_flusso",
                     "confronto_costo_gas",
                     "confronto_costo_pdc",
                     "confronto_risparmio",
                     "confronto_rata_incentivo",
                     "confronto_incentivo_totale",
                     "confronto_van", "confronto_capex",
                     "confronto_co2_evitata_t_anno",
                     "confronto_co2_evitata_t_vita",
                     "confronto_costo_calore_livellato_pdc",
                     "confronto_costo_calore_livellato_gas",
                     "confronto_breakeven_prezzo_gas",
                     "confronto_tir", "confronto_payback",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 15)
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 14)
        self.assertEqual(len(bc["df_tabella"]), 28)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso (EUR)"].iloc[0],
            1900.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[4],
            -500.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[5],
            600.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[-1],
            10500.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Risparmio (EUR/anno)"].iloc[0],
            1100.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Incentivo (EUR/anno)"].iloc[0],
            800.00, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Incentivo (EUR/anno)"].iloc[5],
            0.00, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Costo gas (EUR/anno)",
             "Costo pompa di calore (EUR/anno)",
             "Risparmio (EUR/anno)",
             "Rata incentivo (EUR/anno)",
             "Incentivo totale (EUR)",
             "CAPEX pompa di calore (EUR)",
             "VAN (EUR)",
             "TIR (%)",
             "Payback (anni)",
             "Breakeven prezzo gas (EUR/kWh)",
             "Costo calore livellato PdC (EUR/kWh)",
             "Costo calore livellato gas (EUR/kWh)",
             "CO2 evitata (t/anno)",
             "CO2 evitata vita (t)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            2933.33, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[2],
            1100.00, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Domanda termica (kWh/anno)", voci)
        self.assertIn("Costo gas (EUR/anno)", voci)
        self.assertIn("Costo calore livellato PdC (EUR/kWh)", voci)
        self.assertIn("CO2 evitata vita (t)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh899_csv(bc, mh899_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("domanda_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh899_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh899_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh899_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 11417.62, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh899_calcola(**_demo_kwargs(incentivo_frazione=0.0))
        self.assertEqual(bc["incentivo_frazione"], 0.0)
        self.assertAlmostEqual(bc["van"], 1417.62, places=2)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        bc = mh899_calcola(
            **_demo_kwargs(prezzo_elettricita_eur_kwh=0.0))
        self.assertAlmostEqual(bc["van"], 23910.58, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh899_calcola(
            **_demo_kwargs(delta_manutenzione_eur_anno=0.0))
        self.assertEqual(bc["delta_manutenzione_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 4881.21, places=2)
        bc = mh899_calcola(**_demo_kwargs(fattore_co2_gas=0.0))
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], -1.83,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_cop_basso_non_calcolabile(self):
        # COP 1,5: il risparmio e meno 733,33 in tutti
        # gli anni, VAN None, NON_CALCOLABILE negli
        # helper e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(cop_pdc=1.5)
        bc = mh899_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"], -733.333333333333)
        self.assertTrue(all(r["risparmio"] <= 0.0
                            for r in bc["serie"]))
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_prezzo_gas"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        # Il costo calore livellato resta calcolato
        # anche nel regime degenere (e un costo, non
        # un KPI di ritorno).
        self.assertAlmostEqual(
            bc["costo_calore_livellato_pdc"], 0.21, places=2)

    def test_prezzo_gas_zero_non_calcolabile(self):
        kw = _demo_kwargs(prezzo_gas_eur_kwh=0.0)
        bc = mh899_calcola(**kw)
        self.assertEqual(bc["risparmio_eur_anno"],
                         -1833.3333333333333)
        self.assertEqual(bc["costo_gas_eur_anno"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_gas_basso_non_conveniente(self):
        # Prezzo gas 0,08: risparmio 122,22, VAN meno
        # 5.267,79, TIR meno 9,63 %, payback nessuno.
        bc = mh899_calcola(
            **_demo_kwargs(prezzo_gas_eur_kwh=0.08))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 122.22,
                               places=2)
        self.assertAlmostEqual(bc["van"], -5267.79, places=2)
        self.assertAlmostEqual(bc["tir"], -9.63, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_incentivo_zero_marginale(self):
        # Senza incentivo il payback sale a 10 e il
        # verdetto diventa MARGINALE.
        bc = mh899_calcola(
            **_demo_kwargs(incentivo_frazione=0.0))
        self.assertEqual(bc["rata_incentivo_eur_anno"], 0.0)
        self.assertEqual(bc["incentivo_totale_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 1417.62, places=2)
        self.assertAlmostEqual(bc["tir"], 7.03, places=2)
        self.assertEqual(bc["payback"], 10)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_domanda_piccola_non_conveniente(self):
        # Domanda 10.000: il risparmio dimezza ma il
        # CAPEX resta, VAN meno 1.346,59.
        bc = mh899_calcola(
            **_demo_kwargs(domanda_kwh_anno=10000.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 500.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], -1346.59, places=2)
        self.assertAlmostEqual(bc["tir"], 2.34, places=2)
        self.assertEqual(bc["payback"], 13)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_delta_manutenzione_non_conveniente(self):
        # Delta manutenzione 500: il risparmio scende a
        # 600,00, VAN meno 308,62.
        bc = mh899_calcola(
            **_demo_kwargs(delta_manutenzione_eur_anno=500.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 600.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], -308.62, places=2)
        self.assertAlmostEqual(bc["tir"], 4.42, places=2)
        self.assertEqual(bc["payback"], 10)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_uno(self):
        bc = mh899_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(
            bc["costo_calore_livellato_pdc"], 0.08, places=2)
        self.assertAlmostEqual(bc["breakeven_prezzo_gas"], 0.08,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_vita_dieci_e_tasso_dieci(self):
        bc = mh899_calcola(**_demo_kwargs(vita_anni=10))
        self.assertAlmostEqual(bc["van"], 1957.49, places=2)
        self.assertAlmostEqual(bc["tir"], 9.44, places=2)
        self.assertEqual(bc["payback"], 6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh899_calcola(**_demo_kwargs(tasso=0.10))
        self.assertAlmostEqual(bc["van"], 1399.32, places=2)
        self.assertAlmostEqual(bc["tir"], 12.82, places=2)
        self.assertEqual(bc["payback"], 6)

    def test_cop_quattro_conveniente(self):
        bc = mh899_calcola(**_demo_kwargs(cop_pdc=4.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 1558.33,
                               places=2)
        self.assertAlmostEqual(bc["van"], 9638.55, places=2)
        self.assertAlmostEqual(bc["tir"], 19.12, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(domanda_kwh_anno="22000.0")
        self.assertRaises(ValueError, mh899_calcola, **kw)
        kw = _demo_kwargs(domanda_kwh_anno=True)
        self.assertRaises(ValueError, mh899_calcola, **kw)
        val = mh899_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def899\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh899_demo().keys()), lette - set(mh899_demo().keys()))
        self.assertEqual(lette, set(mh899_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc899\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc899\["([^"]+)"\]', src))
        attese = set(mh899_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 898 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 899.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 907)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab899:"), 1)
        self.assertTrue(src.startswith("    # W904"))

    def test_ui_tab899_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab899:"), 1)
        self.assertIn("def mh899_demo(", src_h)
        self.assertIn("def mh899_calcola(", src_h)
        self.assertIn("tab899", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Conto Termico: l'incentivo GSE sul calore rinnovabile paga davvero?", src)
        self.assertIn("♨️🏛️ Conto Termico: l'incentivo GSE sul calore rinnovabile paga davvero?", src)
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
        chiavi = re.findall(r'key="(st899_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st899_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 19)
        self.assertIn('key="st899_calcola"', src)
        self.assertIn('key="st899_csv"', src)
        self.assertIn('key="st899_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg899"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos899", src)

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
