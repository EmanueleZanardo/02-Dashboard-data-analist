"""Test nuova scheda Degradazione batteria: l'accumulo invecchia,
augmentation o sostituzione?
Repo path: tests/test_w902_degradazione_batteria.py

Effetto ECONOMICO (non solo elettrico): una batteria perde
capacita ogni anno (degrado calendarico piu degrado da cicli),
quindi a parita di cicli carica e scarica sempre meno energia
e il margine annuo cala; a fine vita (SOH sotto soglia 0,70)
il margine va a zero. L'augmentation all'anno T_aug aggiunge
la capacita persa (Delta E) e riporta la capacita utile a
E_batt, ma costa CAPEX_aug: conviene solo se il delta margine
attualizzato ripaga quel CAPEX.
Demo: batteria 4,0 MWh, potenza 2,0 MW informativa, DoD 0,92,
RTE 0,88, cicli 350/anno, k_cal 0,010/anno, k_cyc 0,000050/ciclo,
soglia 0,70, p_carica 75,00 EUR/MWh, p_scarica 130,00 EUR/MWh,
O&M 8 EUR/kWh/anno, capex batt 250 EUR/kWh, T_aug 5, vita 15
anni, tasso 0,05 (frazione), tolleranza 10 %, fattore CO2
0,25 t/MWh.
Degrado annuo = 0,010 piu 0,000050 per 350 = 0,0275; SOH(t) =
max(0, 1 meno 0,0275 per t); SOH(10) = 0,725; SOH(4) = 0,89;
fine vita anno 11 (SOH(11) = 0,6975 sotto 0,70).
Anno 1 base e aug uguali: SOH media 0,98625, E_ch 1270,29 MWh,
E_dis 1117,86 MWh, ricavo 50049,43 EUR, margine 18049,43 EUR.
Anno 5 base: E_ch 1128,61, E_dis 993,18, margine 12467,23;
anno 5 aug (restart): 1270,29, 1117,86, 18049,43. Anno 10
base: E_ch 951,51, E_dis 837,33, margine 5489,49. Anno 11
base 0 (fine vita); anno 11 aug: E_ch 1057,77, E_dis 930,84,
margine 9676,14. Anno 14 aug: E_ch 951,51, E_dis 837,33,
margine 5489,49; anno 15 aug 0.
E_ch totale vita base 11109,00 MWh, aug 15977,64 MWh; E_dis
totale base 9775,92 MWh, aug 14060,32 MWh, sostituzione
15053,50 MWh. Margine totale vita base 117694,60 EUR, aug
181519,02 EUR, sostituzione 193986,25 EUR.
Delta E = 4,0 per (1 meno 0,89) = 0,44 MWh; CAPEX_aug =
0,44 per 1000 per 250 = 110000,00 EUR; CAPEX_new =
1000000,00 EUR all'anno 11.
Flussi delta [0, 0, 0, 0, 0, meno 104417,81, 5582,19 per 5,
9676,14, 8280,59, 6885,04, 5489,49, 0]; cumulato finale meno
46175,58 EUR; somma attualizzata delta margine 40002,26 EUR.
VAN delta = meno 46185,62 EUR; TIR per bisezione su flussi
delta con intervallo da meno 0,9 a 5,0 (meno 10,00 %);
payback (primo anno maggiore o uguale a T_aug con cumulato
maggiore o uguale a 0) = nessuno; breakeven CAPEX aug =
40002,26 per 1,05 elevato a 5 diviso 440 = 116,03 EUR/kWh.
Scenari: base VAN meno 46185,62, TIR meno 10,00 %, payback
nessuno, NON_CONVIENTE; degrado alto (k_cal e k_cyc per 1,5:
degrado 0,04125, EOL anno 8, Delta E 0,66 MWh, CAPEX_aug
165000,00) VAN meno 89333,18, TIR meno 26,81 %, payback
nessuno, NON_CONVIENTE; augmentation economica (capex batt
150, CAPEX_aug 66000,00) VAN meno 11710,46, TIR meno 0,70 %,
payback nessuno, NON_CONVIENTE; spread alto (p_scarica 180)
VAN piu 76280,96, TIR 18,08 %, payback 11, CONVIENTE.
Confronto lascia degradare contro augmentation contro
sostituzione: margine totale 117694,60 contro 181519,02
contro 193986,25 EUR, E_dis totale 9775,92 contro 14060,32
contro 15053,50 MWh, CAPEX strategia 0 contro 110000,00
contro 1000000,00 EUR, VAN delta meno 46185,62.
CO2 base 2443,98 t, aug 3515,08 t, sostituzione 3763,38 t,
delta piu 1071,10 t (INFORMATIVA, mai nel conto economico;
anno 1 base 279,46 t/anno).
Tolleranza in PERCENTUALE (10 = 10 % del CAPEX_aug).
Il tasso e in FRAZIONE (0,05 = 5 %), usato diretto, NON
diviso per 100. I flussi delta sono zero fino a T_aug e
prezzi, costi, cicli e degrado restano costanti per tutta
la vita, SEMPLIFICAZIONE DICHIARATA (prezzi spot, degrado
reale non lineare, cicli reali e temperatura variano nel
mondo reale, qui valore medio costante); dopo l'augmentation
la SOH riparte da 1,0 con la STESSA pendenza, SEMPLIFICAZIONE
DICHIARATA (nella realta le celle vecchie e nuove degradano
insieme); la sostituzione avviene all'inizio dell'anno di
fine vita e costa una batteria nuova intera, solo informativa
di confronto; P_batt e INFORMATIVA (non entra nelle formule).
Verdetto principale: NON_CONVIENTE.
Verdetto: NON_CALCOLABILE se la somma attualizzata del delta
margine e minore o uguale a 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV) oppure se un input e degenere
(E_batt nulla o negativa, P_batt negativa, DoD nulla o
negativa o sopra 1, RTE nulla o negativa o sopra 1, cicli
negativi, k_cal negativo o sopra 1, k_cyc negativo o sopra
0,01, soglia negativa o sopra 1, p_carica negativo, p_scarica
negativo, O&M negativo, CAPEX batt negativo, T_aug nullo o
negativo o non intero o sopra vita, vita nulla o negativa o
non intera, tasso nullo o negativo o maggiore o uguale a 1,
tolleranza negativa, fattore CO2 negativo); altrimenti
CONVIENTE se VAN maggiore o uguale a 0, MARGINALE se VAN
negativa entro tolleranza PERCENTUALE del CAPEX_aug,
NON_CONVIENTE altrimenti.
Casi limite: p_scarica uguale a p_carica (somma attualizzata
delta margine negativa, VAN None, NON_CALCOLABILE); p_scarica
zero (NON_CALCOLABILE); k_cal e k_cyc zero insieme (Delta E
zero, somma attualizzata zero, NON_CALCOLABILE); cicli zero
(NON_CALCOLABILE, margine base uguale a margine aug uguale a
meno O&M); T_aug 1 (Delta E zero, NON_CALCOLABILE); T_aug 15
(VAN meno 176509,50, TIR non definita, payback nessuno);
CAPEX batt zero (VAN piu 40002,26, TIR non definita, payback
5, CONVIENTE); O&M batt zero (VAN piu 23475,38, TIR 9,16 %,
payback 12, CONVIENTE); RTE 1,0 (VAN meno 2765,65, TIR
4,37 %, payback 13, MARGINALE); soglia 0 (VAN meno 48040,81,
TIR meno 10,02 %, EOL nessuno); soglia 1,0 (EOL anno 1,
NON_CALCOLABILE); vita 10 (VAN meno 62877,85, TIR meno
32,33 %, payback nessuno); tasso 0,10 (VAN meno 42226,20,
TIR meno 10,00 %, payback nessuno); cicli 250 (VAN meno
55284,15, TIR non definita perche i flussi delta cambiano
segno due volte, payback nessuno).
Distinzione esplicita: qui SOLO la degradazione della
batteria e il confronto augmentation contro lascia degradare
(VAN sul DELTA con CAPEX_aug), NIENTE arbitraggio puro di
rete (li la batteria compra e vende energia di rete: qui il
margine e ricavo da scarica meno costo di carica con prezzi
fissi, senza FV), NIENTE ibrido FV piu accumulo colocato
(li il recupero del curtailment FV: qui non c'e FV), NIENTE
LCOE di un impianto di generazione (li il costo livellato
dell'energia prodotta: qui il conto e sul delta
dell'augmentation).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w902_helpers import (
        demo_calcoli,
        mh897_breakeven_capex_aug,
        mh897_calcola,
        mh897_capex_aug,
        mh897_capex_batt,
        mh897_co2,
        mh897_confronto,
        mh897_csv,
        mh897_degrado_annuo,
        mh897_delta_e,
        mh897_demo,
        mh897_demo_calcoli,
        mh897_e_ch,
        mh897_e_dis,
        mh897_eol,
        mh897_flussi_delta,
        mh897_fraz,
        mh897_fraz_pos,
        mh897_int_pos,
        mh897_k_cyc,
        mh897_nneg,
        mh897_num,
        mh897_om,
        mh897_payback,
        mh897_pos,
        mh897_ricavo,
        mh897_riga_anno,
        mh897_scenario,
        mh897_sensibilita,
        mh897_serie_annua,
        mh897_soh,
        mh897_soh_media,
        mh897_somma_attualizzata_delta,
        mh897_tasso,
        mh897_tir,
        mh897_valida,
        mh897_van,
        mh897_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w902_helpers", os.path.join(_hf, "w902_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh897_breakeven_capex_aug = _mod.mh897_breakeven_capex_aug
    mh897_calcola = _mod.mh897_calcola
    mh897_capex_aug = _mod.mh897_capex_aug
    mh897_capex_batt = _mod.mh897_capex_batt
    mh897_co2 = _mod.mh897_co2
    mh897_confronto = _mod.mh897_confronto
    mh897_csv = _mod.mh897_csv
    mh897_degrado_annuo = _mod.mh897_degrado_annuo
    mh897_delta_e = _mod.mh897_delta_e
    mh897_demo = _mod.mh897_demo
    mh897_demo_calcoli = _mod.mh897_demo_calcoli
    mh897_e_ch = _mod.mh897_e_ch
    mh897_e_dis = _mod.mh897_e_dis
    mh897_eol = _mod.mh897_eol
    mh897_flussi_delta = _mod.mh897_flussi_delta
    mh897_fraz = _mod.mh897_fraz
    mh897_fraz_pos = _mod.mh897_fraz_pos
    mh897_int_pos = _mod.mh897_int_pos
    mh897_k_cyc = _mod.mh897_k_cyc
    mh897_nneg = _mod.mh897_nneg
    mh897_num = _mod.mh897_num
    mh897_om = _mod.mh897_om
    mh897_payback = _mod.mh897_payback
    mh897_pos = _mod.mh897_pos
    mh897_ricavo = _mod.mh897_ricavo
    mh897_riga_anno = _mod.mh897_riga_anno
    mh897_scenario = _mod.mh897_scenario
    mh897_sensibilita = _mod.mh897_sensibilita
    mh897_serie_annua = _mod.mh897_serie_annua
    mh897_soh = _mod.mh897_soh
    mh897_soh_media = _mod.mh897_soh_media
    mh897_somma_attualizzata_delta = _mod.mh897_somma_attualizzata_delta
    mh897_tasso = _mod.mh897_tasso
    mh897_tir = _mod.mh897_tir
    mh897_valida = _mod.mh897_valida
    mh897_van = _mod.mh897_van
    mh897_verdetto = _mod.mh897_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w902_helpers.py")
_UI_PATH = _risolvi("w902_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "6"
_VECCHIO_TAB = "tab89" + "6"
_VECCHIO_ST = "st89" + "6_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "degrado_annuo": 0.027500000000000004,
    "soh_10": 0.725,
    "eol_base": 11,
    "eol_aug": 15,
    "delta_e_mwh": 0.43999999999999995,
    "capex_aug": 109999.99999999999,
    "capex_sostituzione": 1000000.0,
    "anno_sostituzione": 11,
    "om_batt": 32000.0,
    "e_ch_anno1": 1270.2900000000002,
    "e_dis_anno1": 1117.8552000000002,
    "margine_anno1_base": 18049.42600000002,
    "margine_anno1_aug": 18049.42600000002,
    "e_ch_totale_base": 11109.0,
    "e_ch_totale_aug": 15977.64,
    "e_dis_totale_base": 9775.92,
    "e_dis_totale_aug": 14060.323199999999,
    "e_dis_totale_sostituzione": 15053.5,
    "margine_totale_base": 117694.59999999999,
    "margine_totale_aug": 181519.016,
    "margine_totale_sostituzione": 193986.25,
    "somma_attualizzata_delta_margine": 40002.26252486488,
    "van": -46185.61578666559,
    "tir": -10.003113046602156,
    "payback": None,
    "be_capex_aug_eur_kwh": 116.03215936084035,
    "co2_base_t": 2443.98,
    "co2_aug_t": 3515.0807999999997,
    "co2_sost_t": 3763.375,
    "delta_co2_t": 1071.1007999999997,
    "co2_anno1_base_t_anno": 279.46380000000005,
}

_DEMO_SCENARI = [
    {"nome": "Base", "degrado_annuo": 0.027500000000000004,
     "k_cal": 0.01, "k_cyc": 5e-05, "p_scarica": 130.0,
     "capex_batt_eur_kwh": 250.0,
     "delta_e_mwh": 0.43999999999999995,
     "capex_aug": 109999.99999999999, "eol_base": 11,
     "margine_anno1_base": 18049.42600000002,
     "van": -46185.61578666559, "tir": -10.003113046602156,
     "payback": None, "verdetto": "NON_CONVIENTE",
     "be_capex_aug_eur_kwh": 116.03215936084035},
    {"nome": "Degrado alto", "degrado_annuo": 0.04125,
     "k_cal": 0.015, "k_cyc": 7.500000000000001e-05,
     "p_scarica": 130.0, "capex_batt_eur_kwh": 250.0,
     "delta_e_mwh": 0.6600000000000001,
     "capex_aug": 165000.00000000003, "eol_base": 8,
     "margine_anno1_base": 17700.53899999999,
     "van": -89333.17750421507, "tir": -26.813902754677777,
     "payback": None, "verdetto": "NON_CONVIENTE",
     "be_capex_aug_eur_kwh": 77.25107974519779},
    {"nome": "Augmentation economica",
     "degrado_annuo": 0.027500000000000004,
     "k_cal": 0.01, "k_cyc": 5e-05, "p_scarica": 130.0,
     "capex_batt_eur_kwh": 150.0,
     "delta_e_mwh": 0.43999999999999995,
     "capex_aug": 65999.99999999999, "eol_base": 11,
     "margine_anno1_base": 18049.42600000002,
     "van": -11710.464462053385, "tir": -0.6967522723954322,
     "payback": None, "verdetto": "NON_CONVIENTE",
     "be_capex_aug_eur_kwh": 116.03215936084035},
    {"nome": "Spread alto", "degrado_annuo": 0.027500000000000004,
     "k_cal": 0.01, "k_cyc": 5e-05, "p_scarica": 180.0,
     "capex_batt_eur_kwh": 250.0,
     "delta_e_mwh": 0.43999999999999995,
     "capex_aug": 109999.99999999999, "eol_base": 11,
     "margine_anno1_base": 73942.18600000003,
     "van": 76280.96326023863, "tir": 18.08134950735905,
     "payback": 11, "verdetto": "CONVIENTE",
     "be_capex_aug_eur_kwh": 471.2636067699601},
]

_DEMO_CONFRONTO = {
    "margine_tot_base": 117694.59999999999,
    "margine_tot_aug": 181519.016,
    "margine_tot_sost": 193986.25,
    "delta_margine_tot_aug": 63824.41600000001,
    "delta_margine_tot_sost": 76291.65000000001,
    "e_dis_tot_base": 9775.92,
    "e_dis_tot_aug": 14060.323199999999,
    "e_dis_tot_sost": 15053.5,
    "capex_base": 0.0,
    "capex_aug": 109999.99999999999,
    "capex_sost": 1000000.0,
    "co2_base": 2443.98,
    "co2_aug": 3515.0807999999997,
    "co2_sost": 3763.375,
    "van_delta": -46185.61578666559,
}

_ORDINE_VALIDA = (
    "e_batt_mwh", "p_batt_mw", "dod", "rte", "cicli",
    "k_cal", "k_cyc", "soglia_soh", "p_carica",
    "p_scarica", "om_batt_eur_kwh",
    "capex_batt_eur_kwh", "t_aug", "vita_anni", "tasso",
    "tolleranza_pct", "co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh897_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh897_num(3, "x"), 3.0)
        self.assertEqual(mh897_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh897_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh897_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh897_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh897_pos(0, "x")
        with self.assertRaises(ValueError):
            mh897_pos(-1, "x")
        self.assertEqual(mh897_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh897_fraz(0, "x"), 0.0)
        self.assertEqual(mh897_fraz(1, "x"), 1.0)
        self.assertEqual(mh897_fraz(0.70, "x"), 0.70)
        with self.assertRaises(ValueError):
            mh897_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh897_fraz(1.01, "x")

    def test_fraz_pos_zero_no_uno_ok(self):
        self.assertEqual(mh897_fraz_pos(1, "x"), 1.0)
        self.assertEqual(mh897_fraz_pos(0.88, "x"), 0.88)
        with self.assertRaises(ValueError):
            mh897_fraz_pos(0, "x")
        with self.assertRaises(ValueError):
            mh897_fraz_pos(1.01, "x")

    def test_k_cyc_bordi(self):
        self.assertEqual(mh897_k_cyc(0, "x"), 0.0)
        self.assertEqual(mh897_k_cyc(0.01, "x"), 0.01)
        self.assertEqual(mh897_k_cyc(0.00005, "x"), 0.00005)
        with self.assertRaises(ValueError):
            mh897_k_cyc(-0.00001, "x")
        with self.assertRaises(ValueError):
            mh897_k_cyc(0.02, "x")

    def test_int_pos(self):
        self.assertEqual(mh897_int_pos(15, "x"), 15)
        self.assertEqual(mh897_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh897_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh897_int_pos(15.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh897_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh897_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh897_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh897_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh897_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh897_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_degrado_annuo(self):
        self.assertAlmostEqual(
            mh897_degrado_annuo(0.010, 0.00005, 350), 0.0275)
        self.assertEqual(mh897_degrado_annuo(0.0, 0.0, 350), 0.0)
        self.assertAlmostEqual(
            mh897_degrado_annuo(0.015, 0.000075, 350), 0.04125)
        self.assertEqual(mh897_degrado_annuo(0.010, 0.00005, 0),
                         0.010)
        with self.assertRaises(ValueError):
            mh897_degrado_annuo(-0.01, 0.00005, 350)
        with self.assertRaises(ValueError):
            mh897_degrado_annuo(0.010, 0.02, 350)
        with self.assertRaises(ValueError):
            mh897_degrado_annuo(0.010, 0.00005, -1)

    def test_soh(self):
        self.assertEqual(mh897_soh(0, 0.0275), 1.0)
        self.assertEqual(mh897_soh(10, 0.0275), 0.725)
        self.assertEqual(mh897_soh(11, 0.0275), 0.6975)
        self.assertEqual(mh897_soh(40, 0.0275), 0.0)
        self.assertEqual(mh897_soh(4, 0.0275), 0.89)
        with self.assertRaises(ValueError):
            mh897_soh(-1, 0.0275)
        with self.assertRaises(ValueError):
            mh897_soh(10, -0.01)

    def test_soh_media(self):
        self.assertAlmostEqual(mh897_soh_media(1.0, 0.9725), 0.98625)
        self.assertAlmostEqual(mh897_soh_media(0.89, 0.8625), 0.87625)
        self.assertEqual(mh897_soh_media(1.0, 1.0), 1.0)
        with self.assertRaises(ValueError):
            mh897_soh_media(1.1, 0.9725)

    def test_e_ch_e_dis(self):
        self.assertAlmostEqual(
            mh897_e_ch(350, 4.0, 0.92, 0.98625), 1270.29, places=2)
        self.assertEqual(mh897_e_ch(350, 4.0, 0.92, 1.0), 1288.0)
        self.assertEqual(mh897_e_ch(0, 4.0, 0.92, 0.98625), 0.0)
        self.assertEqual(mh897_e_ch(350, 4.0, 0.92, 0.0), 0.0)
        self.assertAlmostEqual(
            mh897_e_dis(1270.29, 0.88), 1117.86, places=2)
        self.assertEqual(mh897_e_dis(1288.0, 1.0), 1288.0)
        self.assertEqual(mh897_e_dis(0.0, 0.88), 0.0)
        with self.assertRaises(ValueError):
            mh897_e_ch(350, 0, 0.92, 0.98625)
        with self.assertRaises(ValueError):
            mh897_e_ch(350, 4.0, 0, 0.98625)
        with self.assertRaises(ValueError):
            mh897_e_dis(1270.29, 0)
        with self.assertRaises(ValueError):
            mh897_e_dis(1270.29, 1.1)

    def test_ricavo_e_om(self):
        self.assertAlmostEqual(
            mh897_ricavo(1117.8552, 130.0, 1270.29, 75.0),
            50049.43, places=2)
        self.assertAlmostEqual(
            mh897_ricavo(0.0, 130.0, 0.0, 75.0), 0.0, places=2)
        # Con prezzo scarica uguale al prezzo carica
        # il ricavo e negativo per le perdite RTE.
        self.assertAlmostEqual(
            mh897_ricavo(1117.8552, 75.0, 1270.29, 75.0),
            -11432.61, places=2)
        self.assertEqual(mh897_om(4.0, 8.0), 32000.0)
        self.assertEqual(mh897_om(4.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh897_ricavo(1117.86, 130.0, 1270.29, -1.0)
        with self.assertRaises(ValueError):
            mh897_om(0, 8.0)
        with self.assertRaises(ValueError):
            mh897_om(4.0, -1.0)

    def test_delta_e_e_capex(self):
        self.assertAlmostEqual(mh897_delta_e(4.0, 0.89), 0.44,
                               places=2)
        self.assertEqual(mh897_delta_e(4.0, 1.0), 0.0)
        self.assertEqual(mh897_delta_e(4.0, 0.0), 4.0)
        self.assertEqual(mh897_capex_aug(0.44, 250.0), 110000.0)
        self.assertEqual(mh897_capex_aug(0.44, 150.0), 66000.0)
        self.assertEqual(mh897_capex_aug(0.0, 250.0), 0.0)
        self.assertEqual(mh897_capex_batt(4.0, 250.0), 1000000.0)
        self.assertEqual(mh897_capex_batt(4.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh897_delta_e(0, 0.89)
        with self.assertRaises(ValueError):
            mh897_delta_e(4.0, 1.1)
        with self.assertRaises(ValueError):
            mh897_capex_aug(-0.1, 250.0)
        with self.assertRaises(ValueError):
            mh897_capex_batt(4.0, -1.0)

    def test_riga_anno(self):
        riga = mh897_riga_anno(1.0, 0.9725, 0.70, 350, 4.0, 0.92,
                               0.88, 75.0, 130.0, 8.0)
        self.assertAlmostEqual(riga["soh_media"], 0.98625)
        self.assertAlmostEqual(riga["e_ch"], 1270.29, places=2)
        self.assertAlmostEqual(riga["e_dis"], 1117.86, places=2)
        self.assertAlmostEqual(riga["ricavo"], 50049.43, places=2)
        self.assertAlmostEqual(riga["margine"], 18049.43, places=2)
        # Anno morto: SOH fine sotto soglia, tutto zero.
        riga = mh897_riga_anno(0.725, 0.6975, 0.70, 350, 4.0, 0.92,
                               0.88, 75.0, 130.0, 8.0)
        self.assertEqual(riga["e_ch"], 0.0)
        self.assertEqual(riga["e_dis"], 0.0)
        self.assertEqual(riga["ricavo"], 0.0)
        self.assertEqual(riga["margine"], 0.0)
        # Margine negativo: poca energia, O&M fisso.
        riga = mh897_riga_anno(0.7975, 0.775, 0.70, 250, 4.0, 0.92,
                               0.88, 75.0, 130.0, 8.0)
        self.assertAlmostEqual(riga["e_ch"], 723.35, places=2)
        self.assertAlmostEqual(riga["margine"], -3500.01, places=2)
        with self.assertRaises(ValueError):
            mh897_riga_anno(1.0, 0.9725, 1.5, 350, 4.0, 0.92,
                            0.88, 75.0, 130.0, 8.0)

    def test_serie_annua_base_e_aug(self):
        sb = mh897_serie_annua(4.0, 0.92, 0.88, 350, 0.010,
                               0.00005, 0.70, 75.0, 130.0, 8.0,
                               None, 15)
        sa = mh897_serie_annua(4.0, 0.92, 0.88, 350, 0.010,
                               0.00005, 0.70, 75.0, 130.0, 8.0,
                               5, 15)
        self.assertEqual(len(sb), 15)
        self.assertEqual(len(sa), 15)
        # Primi 4 anni aug uguali alla base.
        self.assertEqual(sa[:4], sb[:4])
        # Anno 5 aug uguale all'anno 1 base (valori,
        # non numero anno).
        for chiave in ("soh_fine", "soh_media", "e_ch", "e_dis",
                       "ricavo", "margine"):
            self.assertAlmostEqual(sa[4][chiave], sb[0][chiave])
        # Anno 11 base morto, aug vivo.
        self.assertEqual(sb[10]["margine"], 0.0)
        self.assertAlmostEqual(sa[10]["margine"], 9676.14, places=2)
        # Anno 15 aug morto.
        self.assertEqual(sa[14]["margine"], 0.0)
        self.assertEqual(sb[14]["margine"], 0.0)
        with self.assertRaises(ValueError):
            mh897_serie_annua(4.0, 0.92, 0.88, 350, 0.010,
                              0.00005, 0.70, 75.0, 130.0, 8.0,
                              0, 15)
        with self.assertRaises(ValueError):
            mh897_serie_annua(4.0, 0.92, 0.88, 350, 0.010,
                              0.00005, 0.70, 75.0, 130.0, 8.0,
                              16, 15)

    def test_eol(self):
        sb = mh897_serie_annua(4.0, 0.92, 0.88, 350, 0.010,
                               0.00005, 0.70, 75.0, 130.0, 8.0,
                               None, 15)
        sa = mh897_serie_annua(4.0, 0.92, 0.88, 350, 0.010,
                               0.00005, 0.70, 75.0, 130.0, 8.0,
                               5, 15)
        self.assertEqual(mh897_eol(sb, 0.70), 11)
        self.assertEqual(mh897_eol(sa, 0.70), 15)
        # Con soglia 0 nessuna fine vita entro la vita.
        self.assertIsNone(mh897_eol(sb, 0.0))
        # Con soglia 0,80 fine vita anno 8.
        self.assertEqual(mh897_eol(sb, 0.80), 8)
        with self.assertRaises(ValueError):
            mh897_eol(sb, 1.5)

    def test_flussi_delta_e_somma_attualizzata(self):
        bc = demo_calcoli()
        flussi = bc["flussi_delta"]
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], 0.0)
        self.assertEqual(flussi[1], 0.0)
        self.assertEqual(flussi[4], 0.0)
        self.assertAlmostEqual(flussi[5], -104417.81, places=2)
        self.assertAlmostEqual(flussi[6], 5582.19, places=2)
        self.assertAlmostEqual(flussi[10], 5582.19, places=2)
        self.assertAlmostEqual(flussi[11], 9676.14, places=2)
        self.assertAlmostEqual(flussi[14], 5489.49, places=2)
        self.assertEqual(flussi[15], 0.0)
        self.assertAlmostEqual(sum(flussi), -46175.58, places=2)
        self.assertAlmostEqual(
            bc["somma_attualizzata_delta_margine"], 40002.26,
            places=2)
        # La VAN si ritrova dai flussi delta.
        self.assertAlmostEqual(mh897_van(flussi, 0.05), bc["van"])
        # Flussi ricostruiti a mano dalla serie.
        flussi2 = mh897_flussi_delta(bc["serie_base"],
                                     bc["serie_aug"],
                                     bc["capex_aug"], 5, 15)
        self.assertEqual(flussi2, flussi)
        self.assertAlmostEqual(
            mh897_somma_attualizzata_delta(
                bc["serie_base"], bc["serie_aug"], 0.05, 15),
            40002.26, places=2)
        with self.assertRaises(ValueError):
            mh897_flussi_delta(bc["serie_base"][:10],
                               bc["serie_aug"], bc["capex_aug"],
                               5, 15)

    def test_breakeven_capex_aug(self):
        self.assertAlmostEqual(
            mh897_breakeven_capex_aug(40002.26252486488, 0.05, 5,
                                      0.44),
            116.03, places=2)
        # Con somma attualizzata doppia a parita di
        # Delta E il breakeven raddoppia.
        self.assertAlmostEqual(
            mh897_breakeven_capex_aug(80004.52504972976, 0.05, 5,
                                      0.44),
            232.06, places=2)
        with self.assertRaises(ValueError):
            mh897_breakeven_capex_aug(0, 0.05, 5, 0.44)
        with self.assertRaises(ValueError):
            mh897_breakeven_capex_aug(40002.26, 0.05, 5, 0)
        with self.assertRaises(ValueError):
            mh897_breakeven_capex_aug(40002.26, 0.0, 5, 0.44)

    def test_scenario_singolo(self):
        s = mh897_scenario("Spread alto", mh897_demo(),
                           {"p_scarica": 180.0})
        self.assertEqual(s["nome"], "Spread alto")
        self.assertEqual(s["p_scarica"], 180.0)
        self.assertAlmostEqual(s["van"], 76280.96, places=2)
        self.assertEqual(s["payback"], 11)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh897_scenario("Degrado alto", mh897_demo(),
                           {"k_cal": 0.015, "k_cyc": 0.000075})
        self.assertAlmostEqual(s["van"], -89333.18, places=2)
        self.assertEqual(s["eol_base"], 8)
        self.assertAlmostEqual(s["delta_e_mwh"], 0.66, places=2)
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh897_scenario("", mh897_demo(), {"p_scarica": 180.0})
        with self.assertRaises(ValueError):
            mh897_scenario("X", mh897_demo(), {"k_cyc": 0.02})

    def test_scenario_delta_margine_negativo_non_calcolabile(self):
        s = mh897_scenario("Senza spread", mh897_demo(),
                           {"p_scarica": 75.0})
        self.assertLess(
            mh897_calcola(_scenari=False,
                          **dict(mh897_demo(), p_scarica=75.0))[
                              "somma_attualizzata_delta_margine"],
            0.0)
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh897_confronto(117694.60, 181519.02, 193986.25,
                            9775.92, 14060.32, 15053.50,
                            110000.0, 1000000.0,
                            2443.98, 3515.08, 3763.38,
                            -46185.62)
        self.assertEqual(c["margine_tot_base"], 117694.60)
        self.assertEqual(c["margine_tot_aug"], 181519.02)
        self.assertEqual(c["margine_tot_sost"], 193986.25)
        self.assertAlmostEqual(c["delta_margine_tot_aug"], 63824.42,
                               places=2)
        self.assertAlmostEqual(c["delta_margine_tot_sost"], 76291.65,
                               places=2)
        self.assertEqual(c["capex_base"], 0.0)
        self.assertEqual(c["capex_aug"], 110000.0)
        self.assertEqual(c["capex_sost"], 1000000.0)
        self.assertEqual(c["van_delta"], -46185.62)
        with self.assertRaises(ValueError):
            mh897_confronto(117694.60, 181519.02, 193986.25,
                            9775.92, 14060.32, 15053.50,
                            -1.0, 1000000.0,
                            2443.98, 3515.08, 3763.38,
                            -46185.62)

    def test_co2_informativa(self):
        self.assertAlmostEqual(mh897_co2(9775.92, 0.25), 2443.98,
                               places=2)
        self.assertAlmostEqual(mh897_co2(14060.32, 0.25), 3515.08,
                               places=2)
        self.assertEqual(mh897_co2(9775.92, 0.0), 0.0)
        self.assertAlmostEqual(mh897_co2(1117.86, 0.25), 279.46,
                               places=2)
        with self.assertRaises(ValueError):
            mh897_co2(9775.92, -0.1)
        with self.assertRaises(ValueError):
            mh897_co2(-1.0, 0.25)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_cinque(self):
        bc = mh897_demo_calcoli()
        self.assertAlmostEqual(
            mh897_van(bc["flussi_delta"], 0.05),
            bc["van"])
        spread = bc["scenari"][3]
        bc_spread = mh897_calcola(
            _scenari=False, **dict(mh897_demo(), p_scarica=180.0))
        self.assertAlmostEqual(
            mh897_van(bc_spread["flussi_delta"], 0.05),
            spread["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh897_van([0, 0, 0, 0, 0, -100, 10, 10], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' meno 46185,62; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh897_demo_calcoli()
        self.assertAlmostEqual(
            mh897_van(bc["flussi_delta"], 0.05),
            -46185.62, places=2)
        self.assertNotAlmostEqual(
            mh897_van(bc["flussi_delta"], 0.50),
            -46185.62, places=2)
        with self.assertRaises(ValueError):
            mh897_van(bc["flussi_delta"], 5.0)

    def test_tir_demo(self):
        bc = mh897_demo_calcoli()
        tir = mh897_tir(bc["flussi_delta"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh897_tir([-100, -10, -10]))
        self.assertIsNone(mh897_tir([100, 10, 10]))
        self.assertIsNone(mh897_tir([0, 10, 10]))

    def test_tir_none_doppio_cambio_segno(self):
        # Flussi delta con due cambi di segno (caso
        # 250 cicli/anno): la TIR non e definita.
        bc = mh897_calcola(**_demo_kwargs(cicli=250))
        self.assertIsNone(mh897_tir(bc["flussi_delta"]))
        self.assertIsNone(bc["tir"])

    def test_payback_demo_e_regola_t_aug(self):
        bc = mh897_demo_calcoli()
        self.assertIsNone(mh897_payback(bc["flussi_delta"], 5))
        # Gli anni prima di T_aug non contano: il
        # cumulato e zero fino all'anno 5, ma il
        # payback non puo' essere prima di T_aug.
        self.assertIsNone(mh897_payback([0, 0, 0, 0, 0, -100, 10],
                                        5))
        self.assertEqual(mh897_payback([0, 0, 0, 0, 0, -100, 60, 60],
                                       5), 7)
        # Con CAPEX_aug zero il payback e T_aug.
        self.assertEqual(mh897_payback([0, 0, 0, 0, 0, 50, 10], 5),
                         5)
        # Spread alto: payback 11.
        bc_spread = mh897_calcola(
            _scenari=False, **dict(mh897_demo(), p_scarica=180.0))
        self.assertEqual(
            mh897_payback(bc_spread["flussi_delta"], 5), 11)

    def test_payback_demo_cumulati(self):
        bc = mh897_demo_calcoli()
        f0 = bc["flussi_delta"]
        self.assertAlmostEqual(sum(f0[:6]), -104417.81, places=2)
        self.assertAlmostEqual(sum(f0), -46175.58, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(mh897_verdetto(100.0, 110000, 10),
                         "CONVIENTE")
        self.assertEqual(mh897_verdetto(-5000.0, 110000, 10),
                         "MARGINALE")
        self.assertEqual(mh897_verdetto(-20000.0, 110000, 10),
                         "NON_CONVIENTE")
        # VAN zero: CONVIENTE in questa scheda (VAN
        # maggiore o uguale a 0, come da brief).
        self.assertEqual(mh897_verdetto(0.0, 110000, 10),
                         "CONVIENTE")
        # VAN esattamente alla tolleranza: MARGINALE (inclusa).
        self.assertEqual(mh897_verdetto(-11000.0, 110000, 10),
                         "MARGINALE")
        self.assertEqual(mh897_verdetto(-11000.01, 110000, 10),
                         "NON_CONVIENTE")
        # Con tolleranza zero solo VAN zero e' CONVIENTE.
        self.assertEqual(mh897_verdetto(-1.0, 110000, 0),
                         "NON_CONVIENTE")
        self.assertEqual(mh897_verdetto(0.0, 110000, 0),
                         "CONVIENTE")

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(mh897_verdetto(None, 110000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh897_demo()
        val = mh897_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh897_calcola, **kw)
        kw = _demo_kwargs(vita_anni=15.5)
        self.assertRaises(ValueError, mh897_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10)
        bc = mh897_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh897_calcola(**_demo_kwargs(tasso=tasso))
        bc = mh897_calcola(**_demo_kwargs(tasso=0.10))
        self.assertEqual(bc["tasso"], 0.10)

    def test_valida_t_aug_fuori_vita_no(self):
        for taug in (0, 16, 5.5, -1):
            with self.assertRaises(ValueError):
                mh897_calcola(**_demo_kwargs(t_aug=taug))
        bc = mh897_calcola(**_demo_kwargs(t_aug=3))
        self.assertEqual(bc["t_aug"], 3)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("e_batt_mwh", 0),
                              ("dod", 0),
                              ("rte", 0)):
            with self.assertRaises(ValueError):
                mh897_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_k_cyc_sopra_limite_no(self):
        kw = _demo_kwargs(k_cyc=0.02)
        self.assertRaises(ValueError, mh897_calcola, **kw)
        self.assertFalse(mh897_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_scarica=float("nan"))
        self.assertRaises(ValueError, mh897_calcola, **kw)
        kw = _demo_kwargs(k_cal=float("inf"))
        self.assertRaises(ValueError, mh897_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_batt_mwh", -1),
                              ("p_batt_mw", -1),
                              ("dod", -0.1),
                              ("rte", -0.1),
                              ("cicli", -1),
                              ("k_cal", -0.01),
                              ("k_cyc", -0.00001),
                              ("soglia_soh", -0.1),
                              ("p_carica", -1),
                              ("p_scarica", -1),
                              ("om_batt_eur_kwh", -1),
                              ("capex_batt_eur_kwh", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh897_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_frazioni_sopra_uno_no(self):
        for campo in ("dod", "rte", "k_cal", "soglia_soh"):
            with self.assertRaises(ValueError):
                mh897_calcola(**_demo_kwargs(**{campo: 1.5}))

    def test_calcola_accetta_dict(self):
        bc = mh897_calcola(mh897_demo())
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 4)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh897_calcola(dict(mh897_demo(), p_scarica=999.0),
                           p_scarica=130.0)
        self.assertEqual(bc["p_scarica"], 130.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh897_calcola(_scenari=False, **mh897_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -46185.62, places=2)


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
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "NON_CONVIENTE")
        self.assertLess(bc["van"], 0.0)
        self.assertIsNone(bc["payback"])
        self.assertAlmostEqual(bc["tir"], -10.00, places=2)
        self.assertAlmostEqual(bc["be_capex_aug_eur_kwh"], 116.03,
                               places=2)
        self.assertEqual(bc["eol_base"], 11)
        self.assertEqual(bc["eol_aug"], 15)
        self.assertAlmostEqual(bc["soh_10"], 0.725, places=4)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["degrado_annuo"],
            bc["k_cal"] + bc["k_cyc"] * bc["cicli"])
        self.assertAlmostEqual(
            bc["soh_10"],
            max(0.0, 1.0 - bc["degrado_annuo"] * 10))
        self.assertAlmostEqual(
            bc["delta_e_mwh"],
            bc["e_batt_mwh"] * (1.0 - max(
                0.0, 1.0 - bc["degrado_annuo"] * (bc["t_aug"] - 1))))
        self.assertAlmostEqual(
            bc["capex_aug"],
            bc["delta_e_mwh"] * 1000.0
            * bc["capex_batt_eur_kwh"])
        self.assertAlmostEqual(
            bc["capex_sostituzione"],
            bc["e_batt_mwh"] * 1000.0
            * bc["capex_batt_eur_kwh"])
        self.assertAlmostEqual(
            bc["om_batt"],
            bc["e_batt_mwh"] * 1000.0 * bc["om_batt_eur_kwh"])
        self.assertAlmostEqual(
            bc["e_ch_anno1"],
            bc["cicli"] * bc["e_batt_mwh"] * bc["dod"]
            * (1.0 + max(0.0, 1.0 - bc["degrado_annuo"])) / 2.0)
        self.assertAlmostEqual(
            bc["e_dis_anno1"], bc["e_ch_anno1"] * bc["rte"])
        self.assertAlmostEqual(
            bc["margine_anno1_base"],
            bc["e_dis_anno1"] * bc["p_scarica"]
            - bc["e_ch_anno1"] * bc["p_carica"] - bc["om_batt"])
        self.assertEqual(bc["margine_anno1_aug"],
                         bc["margine_anno1_base"])
        self.assertAlmostEqual(
            bc["e_ch_totale_base"],
            sum(r["e_ch"] for r in bc["serie_base"]))
        self.assertAlmostEqual(
            bc["e_dis_totale_aug"],
            sum(r["e_dis"] for r in bc["serie_aug"]))
        self.assertAlmostEqual(
            bc["e_dis_totale_aug"],
            bc["e_ch_totale_aug"] * bc["rte"])
        self.assertAlmostEqual(
            bc["margine_totale_base"],
            sum(r["margine"] for r in bc["serie_base"]))
        self.assertAlmostEqual(
            bc["margine_totale_aug"],
            sum(r["margine"] for r in bc["serie_aug"]))
        self.assertAlmostEqual(
            bc["van"],
            mh897_van(bc["flussi_delta"], bc["tasso"]))
        self.assertAlmostEqual(
            bc["co2_base_t"],
            bc["e_dis_totale_base"] * bc["co2_t_mwh"])
        self.assertAlmostEqual(
            bc["co2_aug_t"],
            bc["e_dis_totale_aug"] * bc["co2_t_mwh"])
        self.assertAlmostEqual(
            bc["delta_co2_t"],
            bc["co2_aug_t"] - bc["co2_base_t"])
        self.assertAlmostEqual(
            bc["be_capex_aug_eur_kwh"],
            bc["somma_attualizzata_delta_margine"]
            * (1.0 + bc["tasso"]) ** bc["t_aug"]
            / (bc["delta_e_mwh"] * 1000.0))
        for t in range(1, bc["vita_anni"] + 1):
            riga_b = bc["serie_base"][t - 1]
            riga_a = bc["serie_aug"][t - 1]
            with self.subTest(anno=t):
                if t < bc["t_aug"]:
                    self.assertEqual(riga_a, riga_b)
                if riga_b["soh_fine"] < bc["soglia_soh"]:
                    self.assertEqual(riga_b["margine"], 0.0)
                    self.assertEqual(riga_b["e_ch"], 0.0)
        conf = bc["confronto"]
        self.assertAlmostEqual(
            conf["delta_margine_tot_aug"],
            conf["margine_tot_aug"] - conf["margine_tot_base"])
        self.assertAlmostEqual(
            conf["delta_margine_tot_sost"],
            conf["margine_tot_sost"] - conf["margine_tot_base"])
        self.assertAlmostEqual(
            conf["capex_sost"],
            bc["capex_sostituzione"])

    def test_scenari_ordinamento(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Lo spread alto migliora sul base, il degrado
        # alto peggiora, l'augmentation economica migliora
        # sul base ma resta non conveniente.
        self.assertGreater(bc["scenari"][3]["van"], base["van"])
        self.assertGreater(bc["scenari"][3]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][3]["payback"], 11)
        self.assertLess(bc["scenari"][1]["van"], base["van"])
        self.assertLess(bc["scenari"][1]["tir"], base["tir"])
        self.assertGreater(bc["scenari"][2]["van"], base["van"])
        self.assertAlmostEqual(bc["scenari"][2]["capex_aug"], 66000.0)

    def test_sensibilita_valori(self):
        s = mh897_sensibilita(**mh897_demo())
        self.assertEqual(set(s.keys()),
                         {"p_scarica_180", "capex_batt_150",
                          "degrado_alto", "rte_095", "vita_10",
                          "tasso_010", "om_batt_000", "cicli_250",
                          "t_aug_003", "t_aug_008",
                          "soglia_080"})
        attesi = {
            "p_scarica_180": (76280.96, 18.08, 11, "CONVIENTE"),
            "capex_batt_150": (-11710.46, -0.70, None,
                               "NON_CONVIENTE"),
            "degrado_alto": (-89333.18, -26.81, None,
                             "NON_CONVIENTE"),
            "rte_095": (-20857.30, -0.31, None, "NON_CONVIENTE"),
            "vita_10": (-62877.85, -32.33, None, "NON_CONVIENTE"),
            "tasso_010": (-42226.20, -10.00, None,
                          "NON_CONVIENTE"),
            "om_batt_000": (23475.38, 9.16, 12, "CONVIENTE"),
            "cicli_250": (-55284.15, None, None, "NON_CONVIENTE"),
            "t_aug_003": (-24066.46, -7.86, None,
                          "NON_CONVIENTE"),
            "t_aug_008": (-81596.08, -18.86, None,
                          "NON_CONVIENTE"),
            "soglia_080": (-43807.55, -13.67, None,
                           "NON_CONVIENTE"),
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
        csv = mh897_csv(bc, mh897_demo())
        for voce in ("e_batt_mwh", "p_batt_mw", "dod", "rte",
                     "cicli", "k_cal", "k_cyc", "soglia_soh",
                     "p_carica", "p_scarica", "om_batt_eur_kwh",
                     "capex_batt_eur_kwh", "t_aug", "vita_anni",
                     "tasso", "tolleranza_pct", "co2_t_mwh",
                     "degrado_annuo", "soh_10", "eol_base",
                     "eol_aug", "delta_e_mwh", "capex_aug",
                     "capex_sostituzione", "anno_sostituzione",
                     "om_batt", "e_ch_anno1", "e_dis_anno1",
                     "margine_anno1_base", "margine_anno1_aug",
                     "e_ch_totale_base", "e_ch_totale_aug",
                     "e_dis_totale_base", "e_dis_totale_aug",
                     "e_dis_totale_sostituzione",
                     "margine_totale_base", "margine_totale_aug",
                     "margine_totale_sostituzione",
                     "somma_attualizzata_delta_margine",
                     "van", "tir", "payback",
                     "be_capex_aug_eur_kwh",
                     "co2_anno1_base_t_anno", "co2_base_t",
                     "co2_aug_t", "co2_sost_t", "delta_co2_t",
                     "scenario_base_van", "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_degrado_alto_van",
                     "scenario_degrado_alto_verdetto",
                     "scenario_augmentation_economica_van",
                     "scenario_augmentation_economica_verdetto",
                     "scenario_spread_alto_van",
                     "scenario_spread_alto_verdetto",
                     "anno_1_soh_fine_base", "anno_1_e_ch_base",
                     "anno_1_margine_base", "anno_5_margine_aug",
                     "anno_11_margine_base",
                     "anno_11_margine_aug",
                     "anno_15_margine_aug",
                     "confronto_margine_tot_base",
                     "confronto_margine_tot_aug",
                     "confronto_margine_tot_sost",
                     "confronto_e_dis_tot_base",
                     "confronto_e_dis_tot_aug",
                     "confronto_e_dis_tot_sost",
                     "confronto_capex_base",
                     "confronto_capex_aug",
                     "confronto_capex_sost",
                     "confronto_van_delta",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("NON_CONVIENTE", csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_annua_soh_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 15)
        self.assertEqual(len(bc["df_soh"]), 15)
        self.assertEqual(len(bc["df_scenari"]), 4)
        self.assertEqual(len(bc["df_confronto"]), 4)
        self.assertEqual(len(bc["df_tabella"]), 49)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso delta (EUR)"].iloc[4],
            -104417.81, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato delta (EUR)"].iloc[4],
            -104417.81, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato delta (EUR)"].iloc[-1],
            -46175.58, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Margine base (EUR/anno)"].iloc[10],
            0.0, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Margine aug (EUR/anno)"].iloc[10],
            9676.14, places=2)
        self.assertAlmostEqual(
            bc["df_soh"]["SOH base"].iloc[9], 0.725, places=4)
        self.assertAlmostEqual(
            bc["df_soh"]["SOH aug"].iloc[4], 0.9725, places=4)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Margine totale vita (EUR)",
             "E_dis totale vita (MWh)",
             "CAPEX strategia (EUR)",
             "CO2 totale vita (t)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Lascia degradare"].iloc[0],
            117694.60, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Augmentation"].iloc[0],
            181519.02, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Sostituzione"].iloc[0],
            193986.25, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Degrado annuo", voci)
        self.assertIn("Delta E augmentation (MWh)", voci)
        self.assertIn("CAPEX augmentation (EUR)", voci)
        self.assertIn("Breakeven CAPEX aug (EUR/kWh)", voci)
        self.assertIn("CO2 aug totale vita (t)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN delta (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh897_csv(bc, mh897_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_batt_mwh;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh897_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh897_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh897_calcola(**_demo_kwargs(capex_batt_eur_kwh=0))
        self.assertEqual(bc["capex_aug"], 0.0)
        self.assertAlmostEqual(bc["van"], 40002.26, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh897_calcola(**_demo_kwargs(om_batt_eur_kwh=0))
        self.assertEqual(bc["om_batt"], 0.0)
        self.assertAlmostEqual(bc["van"], 23475.38, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh897_calcola(**_demo_kwargs(co2_t_mwh=0))
        self.assertEqual(bc["co2_aug_t"], 0.0)
        self.assertEqual(bc["co2_base_t"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh897_calcola(**_demo_kwargs(p_batt_mw=0))
        self.assertEqual(bc["p_batt_mw"], 0.0)
        self.assertAlmostEqual(bc["van"], -46185.62, places=2)
        bc = mh897_calcola(**_demo_kwargs(soglia_soh=0))
        self.assertIsNone(bc["eol_base"])
        self.assertAlmostEqual(bc["van"], -48040.81, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")


class TestCasiLimite(unittest.TestCase):
    def test_p_scarica_uguale_p_carica_non_calcolabile(self):
        # Prezzo scarica uguale al prezzo carica: lo
        # spread sparisce, la somma attualizzata del
        # delta margine diventa negativa: non calcolabile
        # negli helper (VAN None) e guard NON_CALCOLABILE
        # in UI.
        kw = _demo_kwargs(p_scarica=75.0)
        bc = mh897_calcola(**kw)
        self.assertLess(
            bc["somma_attualizzata_delta_margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")

    def test_p_scarica_zero_non_calcolabile(self):
        kw = _demo_kwargs(p_scarica=0.0)
        bc = mh897_calcola(**kw)
        self.assertLess(
            bc["somma_attualizzata_delta_margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_k_zero_non_calcolabile(self):
        # Senza degrado non c'e nulla da aumentare:
        # Delta E zero, somma attualizzata zero.
        kw = _demo_kwargs(k_cal=0.0, k_cyc=0.0)
        bc = mh897_calcola(**kw)
        self.assertEqual(bc["degrado_annuo"], 0.0)
        self.assertEqual(bc["delta_e_mwh"], 0.0)
        self.assertEqual(bc["capex_aug"], 0.0)
        self.assertEqual(
            bc["somma_attualizzata_delta_margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_cicli_zero_non_calcolabile(self):
        # Senza cicli non si carica nulla: margine base
        # uguale a margine aug uguale a meno O&M, delta
        # zero, somma attualizzata zero.
        kw = _demo_kwargs(cicli=0)
        bc = mh897_calcola(**kw)
        self.assertEqual(bc["e_ch_anno1"], 0.0)
        self.assertEqual(bc["margine_anno1_base"], -32000.0)
        self.assertEqual(bc["margine_anno1_aug"], -32000.0)
        self.assertEqual(
            bc["somma_attualizzata_delta_margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_t_aug_uno_non_calcolabile(self):
        # Augmentation all'anno 1: SOH(0) = 1, Delta E
        # zero, somma attualizzata zero.
        kw = _demo_kwargs(t_aug=1)
        bc = mh897_calcola(**kw)
        self.assertEqual(bc["delta_e_mwh"], 0.0)
        self.assertEqual(
            bc["somma_attualizzata_delta_margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_t_aug_quindici(self):
        # Augmentation all'ultimo anno: quasi nessun
        # beneficio, VAN meno 176509,50, TIR non definita.
        bc = mh897_calcola(**_demo_kwargs(t_aug=15))
        self.assertAlmostEqual(bc["delta_e_mwh"], 1.54, places=2)
        self.assertAlmostEqual(bc["van"], -176509.50, places=2)
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_t_aug_due(self):
        bc = mh897_calcola(**_demo_kwargs(t_aug=2))
        self.assertAlmostEqual(bc["delta_e_mwh"], 0.11, places=2)
        self.assertAlmostEqual(bc["van"], -12286.76, places=2)
        self.assertAlmostEqual(bc["tir"], -6.93, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_soglia_uno_non_calcolabile(self):
        # Soglia 1,0: fine vita anno 1, tutto zero, delta
        # zero, somma attualizzata zero.
        kw = _demo_kwargs(soglia_soh=1.0)
        bc = mh897_calcola(**kw)
        self.assertEqual(bc["eol_base"], 1)
        self.assertEqual(
            bc["somma_attualizzata_delta_margine"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_rte_uno_marginale(self):
        # RTE perfetta: nessuna perdita in scarica, VAN
        # meno 2765,65, TIR 4,37 %, payback 13, MARGINALE.
        bc = mh897_calcola(**_demo_kwargs(rte=1.0))
        self.assertAlmostEqual(bc["van"], -2765.65, places=2)
        self.assertAlmostEqual(bc["tir"], 4.37, places=2)
        self.assertEqual(bc["payback"], 13)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_p_carica_zero_convente(self):
        # Carica gratis: il margine esplode, VAN piu
        # 162564,23, TIR 28,56 %, payback 11, CONVIENTE.
        bc = mh897_calcola(**_demo_kwargs(p_carica=0.0))
        self.assertAlmostEqual(bc["van"], 162564.23, places=2)
        self.assertAlmostEqual(bc["tir"], 28.56, places=2)
        self.assertEqual(bc["payback"], 11)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_k_cal_zero_e_k_cyc_zero_singoli(self):
        # Solo k_cal zero: degrado solo da cicli, EOL
        # oltre la vita, VAN meno 30571,43.
        bc = mh897_calcola(**_demo_kwargs(k_cal=0.0))
        self.assertAlmostEqual(bc["degrado_annuo"], 0.0175)
        self.assertIsNone(bc["eol_base"])
        self.assertAlmostEqual(bc["van"], -30571.43, places=2)
        self.assertAlmostEqual(bc["tir"], -10.02, places=2)
        # Solo k_cyc zero: degrado solo calendarico, EOL
        # oltre la vita, VAN meno 17469,39.
        bc = mh897_calcola(**_demo_kwargs(k_cyc=0.0))
        self.assertAlmostEqual(bc["degrado_annuo"], 0.010)
        self.assertIsNone(bc["eol_base"])
        self.assertAlmostEqual(bc["van"], -17469.39, places=2)
        self.assertAlmostEqual(bc["tir"], -10.02, places=2)

    def test_capex_batt_zero_tir_non_definita_payback_cinque(self):
        bc = mh897_calcola(**_demo_kwargs(capex_batt_eur_kwh=0))
        self.assertEqual(bc["capex_aug"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_vita_dieci_e_tasso_dieci(self):
        bc = mh897_calcola(**_demo_kwargs(vita_anni=10))
        self.assertAlmostEqual(bc["van"], -62877.85, places=2)
        self.assertAlmostEqual(bc["tir"], -32.33, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(bc["eol_base"])
        bc = mh897_calcola(**_demo_kwargs(tasso=0.10))
        self.assertAlmostEqual(bc["van"], -42226.20, places=2)
        self.assertAlmostEqual(bc["tir"], -10.00, places=2)
        self.assertIsNone(bc["payback"])

    def test_tolleranza_zero_bordo(self):
        # Con tolleranza zero ogni VAN negativa e'
        # NON_CONVIENTE, anche quella dello scenario
        # spread alto resta CONVIENTE.
        bc = mh897_calcola(**_demo_kwargs(tolleranza_pct=0))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        bc = mh897_calcola(**_demo_kwargs(p_scarica=180.0,
                                          tolleranza_pct=0))
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(e_batt_mwh="4.0")
        self.assertRaises(ValueError, mh897_calcola, **kw)
        kw = _demo_kwargs(e_batt_mwh=True)
        self.assertRaises(ValueError, mh897_calcola, **kw)
        val = mh897_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def897\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh897_demo().keys()), lette - set(mh897_demo().keys()))
        self.assertEqual(lette, set(mh897_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc897\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc897\["([^"]+)"\]', src))
        attese = set(mh897_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 896 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 897.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 897)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab897:"), 1)
        self.assertTrue(src.startswith("    # W902"))

    def test_ui_tab897_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab897:"), 1)
        self.assertIn("def mh897_demo(", src_h)
        self.assertIn("def mh897_calcola(", src_h)
        self.assertIn("tab897", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Degradazione batteria: l'accumulo invecchia, augmentation o sostituzione?", src)
        self.assertIn("🔋📉 Degradazione batteria: l'accumulo invecchia — augmentation o sostituzione?", src)
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
        chiavi = re.findall(r'key="(st897_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st897_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 23)
        self.assertIn('key="st897_calcola"', src)
        self.assertIn('key="st897_csv"', src)
        self.assertIn('key="st897_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg897"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("_disc_delta897 <= 0.0", src)

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
