"""Test nuova scheda Ibrido FV piu accumulo colocato: un solo
allaccio, due ricavi, il sizing della batteria paga?
Repo path: tests/test_w901_ibrido_fv.py

Effetto ECONOMICO (non solo elettrico): un impianto FV con
accumulo colocato usa UN SOLO allaccio alla rete: la potenza di
connessione limita quanta energia puo uscire verso la rete,
quindi una quota q_curt della produzione FV viene curtailata
(persa) senza batteria. La batteria recupera una parte di quel
curtailment (carica da curtailment) e in piu fa arbitraggio
(carica produzione normale e scarica nelle ore di prezzo peak).
Il sizing della batteria paga solo se il delta ricavo supera
O&M batteria e ripaga il CAPEX batteria.
Demo: FV 5,0 MWp, resa 1150 kWh/kWp: E_fv = 5,0 per 1000 per
1150 diviso 1000 = 5750,00 MWh/anno; q_curt 0,12: E_curt =
5750 per 0,12 = 690,00 MWh/anno; batteria 2,0 MW e 4,0 MWh,
RTE 0,88, DoD 0,92, cicli 350: E_ch_max = 350 per 4,0 per 0,92
= 1288,00 MWh/anno; recupero 0,80: E_ch_curt = min(690 per
0,80, 1288) = 552,00 MWh/anno; q_arb 0,15: E_ch_arb = min(0,15
per 5750, 1288 meno 552) = 736,00 MWh/anno; E_ch_tot = 552 piu
736 = 1288,00 MWh/anno; E_dis = 1288 per 0,88 = 1133,44
MWh/anno; E_diretta = 5750 meno 690 meno 736 = 4324,00
MWh/anno; E_venduta = 4324 piu 1133,44 = 5457,44 MWh/anno;
p_base 75,00 EUR/MWh, p_peak 130,00 EUR/MWh: ricavo base =
(5750 meno 690) per 75 = 379500,00 EUR/anno; ricavo ibrido =
4324 per 75 piu 1133,44 per 130 = 471647,20 EUR/anno; delta
ricavo = 92147,20 EUR/anno; O&M batteria = 4,0 per 1000 per 8
= 32000,00 EUR/anno; delta margine = 92147,20 meno 32000,00 =
60147,20 EUR/anno; CAPEX batteria = 4,0 per 1000 per 250 =
1000000,00 EUR; CAPEX FV = 5,0 per 1000 per 650 = 3250000,00
EUR; O&M FV = 5,0 per 1000 per 15 = 75000,00 EUR/anno;
margine base = 379500 meno 75000 = 304500,00 EUR/anno;
margine ibrido = 471647,20 meno 75000 meno 32000 = 364647,20
EUR/anno; vita 15 anni; tasso 0,05 (frazione); fattore di
rendita a = (1 meno 1,05 elevato a meno 15) diviso 0,05 =
10,3797; VAN delta = 60147,20 per 10,3797 meno 1000000 =
meno 375692,63 EUR; TIR per bisezione su flussi delta [meno
1000000, 60147,20 per 15] con intervallo da meno 0,9 a 5,0
(meno 1,26 %); payback (primo anno con cumulato maggiore o
uguale a 0) = nessuno (cumulato a 15 anni meno 97792,00 EUR);
breakeven CAPEX batteria = 60147,20 per 10,3797 diviso 4000 =
156,08 EUR/kWh; breakeven p_peak = (1000000 diviso 10,3797
piu 32000 piu 736 per 75) diviso 1133,44 = 161,93 EUR/MWh.
Scenari: base VAN meno 375692,63, TIR meno 1,26 %, payback
nessuno, NON_CONVIENTE; spread alto (p_peak 180) VAN piu
212543,35, TIR 8,00 %, payback 9, CONVIENTE (delta margine
116819,20); batteria economica (capex batt 150) VAN piu
24307,37, TIR 5,59 %, payback 10, CONVIENTE (CAPEX
600000,00); curtailment alto (q_curt 0,20) VAN meno 89214,07,
TIR 3,65 %, payback 12, MARGINALE (delta margine 87747,20).
Confronto FV solo contro FV piu batteria: ricavo 379500,00
contro 471647,20, O&M 75000,00 contro 107000,00, margine
304500,00 contro 364647,20, CAPEX 3250000,00 contro
4250000,00, VAN delta meno 375692,63.
CO2 ibrido 1364,36 t/anno (5457,44 per 0,25), CO2 base
1265,00 t/anno (5060,00 per 0,25), delta CO2 piu 99,36
t/anno (INFORMATIVA, mai nel conto economico); curtailment
persa 138,00 MWh/anno (690 meno 552).
Tolleranza in PERCENTUALE (10 = 10 % del CAPEX batteria).
Il tasso e in FRAZIONE (0,05 = 5 %), usato diretto, NON
diviso per 100. I flussi delta piatti sono una
SEMPLIFICAZIONE DICHIARATA (prezzi spot, degrado batteria,
cicli reali e curtailment reale variano nel mondo reale, qui
valore medio costante); la quota di curtailment e un'ipotesi
esplicita e costante negli scenari, non una misura di rete.
P_conn e P_batt sono INFORMATIVE (non entrano nelle formule
energetiche): il modello usa quote di energia e capacita
annua di carica, non il profilo orario di potenza.
Verdetto principale: NON_CONVIENTE.
Verdetto: NON_CALCOLABILE se delta margine minore o uguale
a 0 (guard degenere: UI salta KPI, grafico, tabella e CSV)
oppure se un input e degenere (P_fv nulla o negativa, resa
nulla o negativa, q_curt negativa o sopra 1, P_batt
negativa, E_batt nulla o negativa, RTE nulla o negativa o
sopra 1, DoD nulla o negativa o sopra 1, cicli negativi,
recupero negativo o sopra 1, q_arb negativo o sopra 1,
p_base negativo, p_peak negativo, CAPEX negativi, O&M
negativi, vita nulla o negativa o non intera, tasso nullo o
negativo o maggiore o uguale a 1, tolleranza negativa,
fattore CO2 negativo, E_ch_max nulla o negativa);
altrimenti CONVIENTE se VAN maggiore o uguale a 0,
MARGINALE se VAN negativa entro tolleranza PERCENTUALE del
CAPEX batteria, NON_CONVIENTE altrimenti.
Casi limite: p_peak uguale a p_base (delta margine meno
2192,00, VAN None, NON_CALCOLABILE); p_peak zero (delta
margine meno 87200,00, NON_CALCOLABILE); q_curt zero (delta
margine 1982,50, VAN meno 979422,33, TIR meno 28,17 %,
payback nessuno); q_curt 1,0 (delta margine 115347,20, VAN
piu 197264,49, TIR 7,79 %, payback 9, CONVIENTE); cicli
zero (ValueError); RTE 1,0 (VAN meno 167136,24, TIR 2,41 %,
payback 13); CAPEX batteria zero (VAN piu 624307,37, TIR non
definita, payback 0); O&M batteria zero (VAN meno 43543,57,
TIR 4,35 %, payback 11, MARGINALE); vita 10 (VAN meno
535559,26, TIR meno 8,32 %, payback nessuno); tasso 0,10
(VAN meno 542515,61, TIR meno 1,26 %, payback nessuno).
Distinzione esplicita: qui SOLO l'ibrido FV piu accumulo
colocato con un solo allaccio (curtailment recuperato piu
arbitraggio contro CAPEX batteria, VAN sul DELTA), NIENTE
arbitraggio puro di rete (li la batteria compra e vende
energia di rete senza FV: qui la carica arriva da produzione
FV propria), NIENTE LCOE di un impianto di generazione (li
il costo livellato dell'energia prodotta: qui il conto e sul
delta della batteria), NIENTE dimensionamento orario con
profilo di carico (li la simulazione ora per ora: qui quote
annue medie).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w901_helpers import (
        demo_calcoli,
        mh896_breakeven_capex,
        mh896_breakeven_p_peak,
        mh896_calcola,
        mh896_capex_batt,
        mh896_capex_fv,
        mh896_co2,
        mh896_confronto,
        mh896_csv,
        mh896_demo,
        mh896_demo_calcoli,
        mh896_e_ch_arb,
        mh896_e_ch_curt,
        mh896_e_ch_max,
        mh896_e_curt,
        mh896_e_diretta,
        mh896_e_dis,
        mh896_e_fv,
        mh896_fattore_rendita,
        mh896_flussi,
        mh896_fraz,
        mh896_fraz_pos,
        mh896_int_pos,
        mh896_nneg,
        mh896_num,
        mh896_om_batt,
        mh896_om_fv,
        mh896_payback,
        mh896_pos,
        mh896_ricavo_base,
        mh896_ricavo_ibrido,
        mh896_scenario,
        mh896_sensibilita,
        mh896_tasso,
        mh896_tir,
        mh896_valida,
        mh896_van,
        mh896_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w901_helpers", os.path.join(_hf, "w901_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh896_breakeven_capex = _mod.mh896_breakeven_capex
    mh896_breakeven_p_peak = _mod.mh896_breakeven_p_peak
    mh896_calcola = _mod.mh896_calcola
    mh896_capex_batt = _mod.mh896_capex_batt
    mh896_capex_fv = _mod.mh896_capex_fv
    mh896_co2 = _mod.mh896_co2
    mh896_confronto = _mod.mh896_confronto
    mh896_csv = _mod.mh896_csv
    mh896_demo = _mod.mh896_demo
    mh896_demo_calcoli = _mod.mh896_demo_calcoli
    mh896_e_ch_arb = _mod.mh896_e_ch_arb
    mh896_e_ch_curt = _mod.mh896_e_ch_curt
    mh896_e_ch_max = _mod.mh896_e_ch_max
    mh896_e_curt = _mod.mh896_e_curt
    mh896_e_diretta = _mod.mh896_e_diretta
    mh896_e_dis = _mod.mh896_e_dis
    mh896_e_fv = _mod.mh896_e_fv
    mh896_fattore_rendita = _mod.mh896_fattore_rendita
    mh896_flussi = _mod.mh896_flussi
    mh896_fraz = _mod.mh896_fraz
    mh896_fraz_pos = _mod.mh896_fraz_pos
    mh896_int_pos = _mod.mh896_int_pos
    mh896_nneg = _mod.mh896_nneg
    mh896_num = _mod.mh896_num
    mh896_om_batt = _mod.mh896_om_batt
    mh896_om_fv = _mod.mh896_om_fv
    mh896_payback = _mod.mh896_payback
    mh896_pos = _mod.mh896_pos
    mh896_ricavo_base = _mod.mh896_ricavo_base
    mh896_ricavo_ibrido = _mod.mh896_ricavo_ibrido
    mh896_scenario = _mod.mh896_scenario
    mh896_sensibilita = _mod.mh896_sensibilita
    mh896_tasso = _mod.mh896_tasso
    mh896_tir = _mod.mh896_tir
    mh896_valida = _mod.mh896_valida
    mh896_van = _mod.mh896_van
    mh896_verdetto = _mod.mh896_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w901_helpers.py")
_UI_PATH = _risolvi("w901_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "5"
_VECCHIO_TAB = "tab89" + "5"
_VECCHIO_ST = "st89" + "5_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "e_fv_mwh": 5750.0,
    "e_curt_mwh": 690.0,
    "e_ch_max_mwh": 1288.0,
    "e_ch_curt_mwh": 552.0,
    "e_ch_arb_mwh": 736.0,
    "e_ch_tot_mwh": 1288.0,
    "e_dis_mwh": 1133.44,
    "e_diretta_mwh": 4324.0,
    "e_venduta_mwh": 5457.4400000000005,
    "ricavo_base": 379500.0,
    "ricavo_ibrido": 471647.2,
    "delta_ricavo": 92147.20000000001,
    "om_batt": 32000.0,
    "delta_margine": 60147.20000000001,
    "capex_batt": 1000000.0,
    "capex_fv": 3250000.0,
    "om_fv": 75000.0,
    "margine_base": 304500.0,
    "margine_ibrido": 364647.2,
    "fattore_rendita": 10.3796580381806,
    "van": -375692.63204594376,
    "tir": -1.2596351710629996,
    "payback": None,
    "co2_ibrido_t_anno": 1364.3600000000001,
    "co2_base_t_anno": 1265.0,
    "delta_co2_t_anno": 99.36000000000013,
    "curt_persa_mwh": 138.0,
    "be_capex_batt_eur_kwh": 156.07684198851405,
    "be_p_peak_eur_mwh": 161.93383647060656,
}

_DEMO_SCENARI = [
    {"nome": "Base", "p_peak": 130.0,
     "capex_batt_eur_kwh": 250.0, "q_curt": 0.12,
     "ricavo_ibrido": 471647.2,
     "delta_margine": 60147.20000000001,
     "margine_ibrido": 364647.2,
     "capex_batt": 1000000.0,
     "van": -375692.63204594376,
     "tir": -1.2596351710629996, "payback": None,
     "verdetto": "NON_CONVIENTE"},
    {"nome": "Spread alto", "p_peak": 180.0,
     "capex_batt_eur_kwh": 250.0, "q_curt": 0.12,
     "ricavo_ibrido": 528319.2,
     "delta_margine": 116819.19999999995,
     "margine_ibrido": 421319.19999999995,
     "capex_batt": 1000000.0,
     "van": 212543.34829382668,
     "tir": 7.998549798992935, "payback": 9,
     "verdetto": "CONVIENTE"},
    {"nome": "Batteria economica", "p_peak": 130.0,
     "capex_batt_eur_kwh": 150.0, "q_curt": 0.12,
     "ricavo_ibrido": 471647.2,
     "delta_margine": 60147.20000000001,
     "margine_ibrido": 364647.2,
     "capex_batt": 600000.0,
     "van": 24307.367954056244,
     "tir": 5.593462314487281, "payback": 10,
     "verdetto": "CONVIENTE"},
    {"nome": "Curtailment alto", "p_peak": 130.0,
     "capex_batt_eur_kwh": 250.0, "q_curt": 0.20,
     "ricavo_ibrido": 464747.2,
     "delta_margine": 87747.20000000001,
     "margine_ibrido": 357747.2,
     "capex_batt": 1000000.0,
     "van": -89214.07019215915,
     "tir": 3.648924918547319, "payback": 12,
     "verdetto": "MARGINALE"},
]

_DEMO_CONFRONTO = {
    "ricavo_base": 379500.0,
    "ricavo_ibrido": 471647.2,
    "delta_ricavo": 92147.20000000001,
    "om_base": 75000.0,
    "om_ibrido": 107000.0,
    "margine_base": 304500.0,
    "margine_ibrido": 364647.2,
    "capex_base": 3250000.0,
    "capex_ibrido": 4250000.0,
    "van_delta": -375692.63204594376,
}

_ORDINE_VALIDA = (
    "p_fv_mwp", "resa_kwh_kwp", "p_conn_mw", "q_curt",
    "p_batt_mw", "e_batt_mwh", "rte", "dod", "cicli",
    "recupero", "q_arb", "p_base", "p_peak",
    "capex_fv_eur_kwp", "capex_batt_eur_kwh",
    "om_fv_eur_kwp", "om_batt_eur_kwh", "tasso",
    "vita_anni", "tolleranza_pct", "co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh896_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh896_num(3, "x"), 3.0)
        self.assertEqual(mh896_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh896_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh896_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh896_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh896_pos(0, "x")
        with self.assertRaises(ValueError):
            mh896_pos(-1, "x")
        self.assertEqual(mh896_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh896_fraz(0, "x"), 0.0)
        self.assertEqual(mh896_fraz(1, "x"), 1.0)
        self.assertEqual(mh896_fraz(0.12, "x"), 0.12)
        with self.assertRaises(ValueError):
            mh896_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh896_fraz(1.01, "x")

    def test_fraz_pos_zero_no_uno_ok(self):
        self.assertEqual(mh896_fraz_pos(1, "x"), 1.0)
        self.assertEqual(mh896_fraz_pos(0.88, "x"), 0.88)
        with self.assertRaises(ValueError):
            mh896_fraz_pos(0, "x")
        with self.assertRaises(ValueError):
            mh896_fraz_pos(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh896_int_pos(15, "x"), 15)
        self.assertEqual(mh896_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh896_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh896_int_pos(15.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh896_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh896_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh896_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh896_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh896_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh896_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_e_fv(self):
        self.assertEqual(mh896_e_fv(5.0, 1150.0), 5750.0)
        self.assertEqual(mh896_e_fv(1.0, 1000.0), 1000.0)
        self.assertEqual(mh896_e_fv(2.5, 1200.0), 3000.0)
        with self.assertRaises(ValueError):
            mh896_e_fv(0, 1150.0)
        with self.assertRaises(ValueError):
            mh896_e_fv(5.0, 0)

    def test_e_curt(self):
        self.assertEqual(mh896_e_curt(5750.0, 0.12), 690.0)
        self.assertEqual(mh896_e_curt(5750.0, 0.0), 0.0)
        self.assertEqual(mh896_e_curt(5750.0, 1.0), 5750.0)
        with self.assertRaises(ValueError):
            mh896_e_curt(5750.0, 1.2)
        with self.assertRaises(ValueError):
            mh896_e_curt(5750.0, -0.1)

    def test_e_ch_max(self):
        self.assertEqual(mh896_e_ch_max(350, 4.0, 0.92), 1288.0)
        self.assertEqual(mh896_e_ch_max(0, 4.0, 0.92), 0.0)
        self.assertEqual(mh896_e_ch_max(365, 10.0, 1.0), 3650.0)
        with self.assertRaises(ValueError):
            mh896_e_ch_max(350, 0, 0.92)
        with self.assertRaises(ValueError):
            mh896_e_ch_max(350, 4.0, 0)
        with self.assertRaises(ValueError):
            mh896_e_ch_max(350, 4.0, 1.1)
        with self.assertRaises(ValueError):
            mh896_e_ch_max(-1, 4.0, 0.92)

    def test_e_ch_curt(self):
        self.assertEqual(mh896_e_ch_curt(690.0, 0.80, 1288.0), 552.0)
        self.assertEqual(mh896_e_ch_curt(690.0, 0.80, 100.0), 100.0)
        self.assertEqual(mh896_e_ch_curt(690.0, 0.0, 1288.0), 0.0)
        self.assertEqual(mh896_e_ch_curt(0.0, 0.80, 1288.0), 0.0)
        with self.assertRaises(ValueError):
            mh896_e_ch_curt(690.0, 1.2, 1288.0)
        with self.assertRaises(ValueError):
            mh896_e_ch_curt(690.0, 0.80, -1.0)

    def test_e_ch_arb(self):
        self.assertEqual(mh896_e_ch_arb(0.15, 5750.0, 1288.0, 552.0),
                         736.0)
        # Capacita residua minore della domanda: la
        # carica da arbitraggio si ferma al residuo.
        self.assertEqual(mh896_e_ch_arb(0.15, 5750.0, 600.0, 552.0),
                         48.0)
        self.assertEqual(mh896_e_ch_arb(0.0, 5750.0, 1288.0, 552.0),
                         0.0)
        # Carica da curtailment sopra la capacita
        # annua: input incoerente, solleva.
        with self.assertRaises(ValueError):
            mh896_e_ch_arb(0.15, 5750.0, 500.0, 552.0)
        with self.assertRaises(ValueError):
            mh896_e_ch_arb(1.2, 5750.0, 1288.0, 552.0)

    def test_e_dis_e_diretta(self):
        self.assertEqual(mh896_e_dis(1288.0, 0.88), 1133.44)
        self.assertEqual(mh896_e_dis(1288.0, 1.0), 1288.0)
        self.assertEqual(mh896_e_dis(0.0, 0.88), 0.0)
        self.assertEqual(mh896_e_diretta(5750.0, 690.0, 736.0), 4324.0)
        self.assertEqual(mh896_e_diretta(5750.0, 0.0, 0.0), 5750.0)
        with self.assertRaises(ValueError):
            mh896_e_dis(1288.0, 0)
        with self.assertRaises(ValueError):
            mh896_e_dis(1288.0, 1.1)
        with self.assertRaises(ValueError):
            mh896_e_diretta(5750.0, 690.0, -1.0)

    def test_ricavi(self):
        self.assertEqual(mh896_ricavo_base(5750.0, 690.0, 75.0),
                         379500.0)
        self.assertEqual(mh896_ricavo_base(5750.0, 0.0, 75.0),
                         431250.0)
        self.assertEqual(mh896_ricavo_ibrido(4324.0, 75.0, 1133.44,
                                             130.0),
                         471647.2)
        self.assertEqual(mh896_ricavo_ibrido(4324.0, 75.0, 0.0, 130.0),
                         324300.0)
        with self.assertRaises(ValueError):
            mh896_ricavo_base(5750.0, 690.0, -1.0)
        with self.assertRaises(ValueError):
            mh896_ricavo_ibrido(4324.0, 75.0, 1133.44, -1.0)

    def test_om_e_capex(self):
        self.assertEqual(mh896_om_batt(4.0, 8.0), 32000.0)
        self.assertEqual(mh896_om_batt(4.0, 0.0), 0.0)
        self.assertEqual(mh896_capex_batt(4.0, 250.0), 1000000.0)
        self.assertEqual(mh896_capex_batt(4.0, 150.0), 600000.0)
        self.assertEqual(mh896_capex_fv(5.0, 650.0), 3250000.0)
        self.assertEqual(mh896_om_fv(5.0, 15.0), 75000.0)
        self.assertEqual(mh896_om_fv(5.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh896_om_batt(0, 8.0)
        with self.assertRaises(ValueError):
            mh896_capex_batt(4.0, -1.0)
        with self.assertRaises(ValueError):
            mh896_capex_fv(0, 650.0)
        with self.assertRaises(ValueError):
            mh896_om_fv(5.0, -1.0)

    def test_fattore_rendita(self):
        self.assertAlmostEqual(mh896_fattore_rendita(0.05, 15),
                               10.3797, places=4)
        self.assertAlmostEqual(mh896_fattore_rendita(0.10, 15),
                               7.6061, places=4)
        self.assertAlmostEqual(mh896_fattore_rendita(0.05, 1), 0.9524,
                               places=4)
        with self.assertRaises(ValueError):
            mh896_fattore_rendita(0.0, 15)
        with self.assertRaises(ValueError):
            mh896_fattore_rendita(0.05, 0)

    def test_breakeven_capex(self):
        self.assertAlmostEqual(
            mh896_breakeven_capex(60147.2, 10.3796580381806, 4.0),
            156.08, places=2)
        # Con delta margine doppio a parita di
        # batteria il breakeven raddoppia.
        self.assertAlmostEqual(
            mh896_breakeven_capex(120294.4, 10.3796580381806, 4.0),
            312.15, places=2)
        with self.assertRaises(ValueError):
            mh896_breakeven_capex(0, 10.3796580381806, 4.0)
        with self.assertRaises(ValueError):
            mh896_breakeven_capex(60147.2, 10.3796580381806, 0)

    def test_breakeven_p_peak(self):
        self.assertAlmostEqual(
            mh896_breakeven_p_peak(1000000.0, 10.3796580381806,
                                   32000.0, 736.0, 75.0, 1133.44),
            161.93, places=2)
        # Con CAPEX batteria dimezzato il
        # breakeven scende di molto.
        self.assertAlmostEqual(
            mh896_breakeven_p_peak(500000.0, 10.3796580381806,
                                   32000.0, 736.0, 75.0, 1133.44),
            119.43, places=2)
        with self.assertRaises(ValueError):
            mh896_breakeven_p_peak(1000000.0, 10.3796580381806,
                                   32000.0, 736.0, 75.0, 0.0)

    def test_scenario_singolo(self):
        bc = demo_calcoli()
        s = mh896_scenario("Spread alto", mh896_demo(),
                           {"p_peak": 180.0})
        self.assertEqual(s["nome"], "Spread alto")
        self.assertEqual(s["p_peak"], 180.0)
        self.assertAlmostEqual(s["van"], 212543.35, places=2)
        self.assertEqual(s["payback"], 9)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh896_scenario("Curtailment alto", mh896_demo(),
                           {"q_curt": 0.20})
        self.assertAlmostEqual(s["van"], -89214.07, places=2)
        self.assertEqual(s["payback"], 12)
        self.assertEqual(s["verdetto"], "MARGINALE")
        with self.assertRaises(ValueError):
            mh896_scenario("", mh896_demo(), {"p_peak": 180.0})
        with self.assertRaises(ValueError):
            mh896_scenario("X", mh896_demo(), {"q_curt": 1.5})

    def test_scenario_delta_margine_negativo_non_calcolabile(self):
        s = mh896_scenario("Senza spread", mh896_demo(),
                           {"p_peak": 75.0})
        self.assertLess(s["delta_margine"], 0.0)
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh896_confronto(379500.0, 471647.2, 75000.0, 32000.0,
                            3250000.0, 1000000.0, -375692.63)
        self.assertEqual(c["ricavo_base"], 379500.0)
        self.assertEqual(c["ricavo_ibrido"], 471647.2)
        self.assertAlmostEqual(c["delta_ricavo"], 92147.2)
        self.assertEqual(c["om_base"], 75000.0)
        self.assertEqual(c["om_ibrido"], 107000.0)
        self.assertEqual(c["margine_base"], 304500.0)
        self.assertAlmostEqual(c["margine_ibrido"], 364647.2)
        self.assertEqual(c["capex_base"], 3250000.0)
        self.assertEqual(c["capex_ibrido"], 4250000.0)
        self.assertEqual(c["van_delta"], -375692.63)
        with self.assertRaises(ValueError):
            mh896_confronto(379500.0, 471647.2, 75000.0, -1.0,
                            3250000.0, 1000000.0, -375692.63)

    def test_co2_informativa(self):
        self.assertAlmostEqual(mh896_co2(5457.44, 0.25), 1364.36,
                               places=2)
        self.assertEqual(mh896_co2(5457.44, 0.0), 0.0)
        self.assertAlmostEqual(mh896_co2(5060.0, 0.25), 1265.00,
                               places=2)
        with self.assertRaises(ValueError):
            mh896_co2(5457.44, -0.1)
        with self.assertRaises(ValueError):
            mh896_co2(-1.0, 0.25)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh896_flussi(1000000, 60147.2, 3),
                         [-1000000, 60147.2, 60147.2, 60147.2])

    def test_van_tasso_cinque(self):
        bc = mh896_demo_calcoli()
        self.assertAlmostEqual(
            mh896_van(bc["flussi"], 0.05),
            bc["van"])
        # La VAN dello scenario spread alto si
        # ritrova dai suoi flussi ricostruiti.
        spread = bc["scenari"][1]
        flussi_spread = mh896_flussi(
            spread["capex_batt"], spread["delta_margine"],
            bc["vita_anni"])
        self.assertAlmostEqual(
            mh896_van(flussi_spread, 0.05),
            spread["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh896_van([-1000000, 60147.2, 60147.2], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' meno 375692,63; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh896_demo_calcoli()
        self.assertAlmostEqual(
            mh896_van(bc["flussi"], 0.05),
            -375692.63, places=2)
        self.assertNotAlmostEqual(
            mh896_van(bc["flussi"], 0.50),
            -375692.63, places=2)
        with self.assertRaises(ValueError):
            mh896_van(bc["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh896_demo_calcoli()
        tir = mh896_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh896_tir([-100, -10, -10]))
        self.assertIsNone(mh896_tir([100, 10, 10]))
        self.assertIsNone(mh896_tir([0, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh896_demo_calcoli()
        self.assertIsNone(mh896_payback(bc["flussi"]))
        self.assertIsNone(mh896_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh896_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh896_demo_calcoli()
        f0 = bc["flussi"]
        self.assertAlmostEqual(sum(f0[:2]), -939852.80, places=2)
        self.assertAlmostEqual(sum(f0), -97792.00, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(mh896_verdetto(100.0, 1000000, 10),
                         "CONVIENTE")
        self.assertEqual(mh896_verdetto(-50000.0, 1000000, 10),
                         "MARGINALE")
        self.assertEqual(mh896_verdetto(-200000.0, 1000000, 10),
                         "NON_CONVIENTE")
        # VAN zero: CONVIENTE in questa scheda (VAN
        # maggiore o uguale a 0, come da brief).
        self.assertEqual(mh896_verdetto(0.0, 1000000, 10),
                         "CONVIENTE")
        # VAN esattamente alla tolleranza: MARGINALE (inclusa).
        self.assertEqual(mh896_verdetto(-100000.0, 1000000, 10),
                         "MARGINALE")
        self.assertEqual(mh896_verdetto(-100000.01, 1000000, 10),
                         "NON_CONVIENTE")
        # Con tolleranza zero solo VAN zero e' CONVIENTE.
        self.assertEqual(mh896_verdetto(-1.0, 1000000, 0),
                         "NON_CONVIENTE")
        self.assertEqual(mh896_verdetto(0.0, 1000000, 0),
                         "CONVIENTE")

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(mh896_verdetto(None, 1000000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh896_demo()
        val = mh896_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        kw = _demo_kwargs(vita_anni=15.5)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10)
        bc = mh896_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh896_calcola(**_demo_kwargs(tasso=tasso))
        bc = mh896_calcola(**_demo_kwargs(tasso=0.10))
        self.assertEqual(bc["tasso"], 0.10)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("p_fv_mwp", 0),
                              ("resa_kwh_kwp", 0),
                              ("e_batt_mwh", 0),
                              ("rte", 0),
                              ("dod", 0)):
            with self.assertRaises(ValueError):
                mh896_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_cicli_zero_e_ch_max_zero_no(self):
        kw = _demo_kwargs(cicli=0)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        self.assertFalse(mh896_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_peak=float("nan"))
        self.assertRaises(ValueError, mh896_calcola, **kw)
        kw = _demo_kwargs(q_curt=float("inf"))
        self.assertRaises(ValueError, mh896_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("p_fv_mwp", -1),
                              ("resa_kwh_kwp", -1),
                              ("p_conn_mw", -1),
                              ("q_curt", -0.1),
                              ("p_batt_mw", -1),
                              ("e_batt_mwh", -1),
                              ("rte", -0.1),
                              ("dod", -0.1),
                              ("cicli", -1),
                              ("recupero", -0.1),
                              ("q_arb", -0.1),
                              ("p_base", -1),
                              ("p_peak", -1),
                              ("capex_fv_eur_kwp", -1),
                              ("capex_batt_eur_kwh", -1),
                              ("om_fv_eur_kwp", -1),
                              ("om_batt_eur_kwh", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh896_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_frazioni_sopra_uno_no(self):
        for campo in ("q_curt", "rte", "dod", "recupero", "q_arb"):
            with self.assertRaises(ValueError):
                mh896_calcola(**_demo_kwargs(**{campo: 1.5}))

    def test_calcola_accetta_dict(self):
        bc = mh896_calcola(mh896_demo())
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 4)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh896_calcola(dict(mh896_demo(), p_peak=999.0),
                           p_peak=130.0)
        self.assertEqual(bc["p_peak"], 130.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh896_calcola(_scenari=False, **mh896_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -375692.63, places=2)


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
        self.assertAlmostEqual(bc["tir"], -1.26, places=2)
        self.assertAlmostEqual(bc["be_capex_batt_eur_kwh"], 156.08,
                               places=2)
        self.assertAlmostEqual(bc["be_p_peak_eur_mwh"], 161.93,
                               places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["e_fv_mwh"],
            bc["p_fv_mwp"] * 1000.0 * bc["resa_kwh_kwp"] / 1000.0)
        self.assertAlmostEqual(
            bc["e_curt_mwh"], bc["e_fv_mwh"] * bc["q_curt"])
        self.assertAlmostEqual(
            bc["e_ch_max_mwh"],
            bc["cicli"] * bc["e_batt_mwh"] * bc["dod"])
        self.assertAlmostEqual(
            bc["e_ch_curt_mwh"],
            min(bc["e_curt_mwh"] * bc["recupero"],
                bc["e_ch_max_mwh"]))
        self.assertAlmostEqual(
            bc["e_ch_arb_mwh"],
            min(bc["q_arb"] * bc["e_fv_mwh"],
                bc["e_ch_max_mwh"] - bc["e_ch_curt_mwh"]))
        self.assertAlmostEqual(
            bc["e_ch_tot_mwh"],
            bc["e_ch_curt_mwh"] + bc["e_ch_arb_mwh"])
        self.assertAlmostEqual(
            bc["e_dis_mwh"], bc["e_ch_tot_mwh"] * bc["rte"])
        self.assertAlmostEqual(
            bc["e_diretta_mwh"],
            bc["e_fv_mwh"] - bc["e_curt_mwh"]
            - bc["e_ch_arb_mwh"])
        self.assertAlmostEqual(
            bc["e_venduta_mwh"],
            bc["e_diretta_mwh"] + bc["e_dis_mwh"])
        self.assertAlmostEqual(
            bc["ricavo_base"],
            (bc["e_fv_mwh"] - bc["e_curt_mwh"]) * bc["p_base"])
        self.assertAlmostEqual(
            bc["ricavo_ibrido"],
            bc["e_diretta_mwh"] * bc["p_base"]
            + bc["e_dis_mwh"] * bc["p_peak"])
        self.assertAlmostEqual(
            bc["delta_ricavo"],
            bc["ricavo_ibrido"] - bc["ricavo_base"])
        self.assertAlmostEqual(
            bc["om_batt"],
            bc["e_batt_mwh"] * 1000.0 * bc["om_batt_eur_kwh"])
        self.assertAlmostEqual(
            bc["delta_margine"],
            bc["delta_ricavo"] - bc["om_batt"])
        self.assertAlmostEqual(
            bc["capex_batt"],
            bc["e_batt_mwh"] * 1000.0
            * bc["capex_batt_eur_kwh"])
        self.assertAlmostEqual(
            bc["capex_fv"],
            bc["p_fv_mwp"] * 1000.0 * bc["capex_fv_eur_kwp"])
        self.assertAlmostEqual(
            bc["om_fv"],
            bc["p_fv_mwp"] * 1000.0 * bc["om_fv_eur_kwp"])
        self.assertAlmostEqual(
            bc["margine_base"],
            bc["ricavo_base"] - bc["om_fv"])
        self.assertAlmostEqual(
            bc["margine_ibrido"],
            bc["ricavo_ibrido"] - bc["om_fv"] - bc["om_batt"])
        self.assertAlmostEqual(
            bc["van"],
            bc["delta_margine"] * bc["fattore_rendita"]
            - bc["capex_batt"])
        self.assertAlmostEqual(
            bc["co2_ibrido_t_anno"],
            bc["e_venduta_mwh"] * bc["co2_t_mwh"])
        self.assertAlmostEqual(
            bc["co2_base_t_anno"],
            (bc["e_fv_mwh"] - bc["e_curt_mwh"])
            * bc["co2_t_mwh"])
        self.assertAlmostEqual(
            bc["delta_co2_t_anno"],
            bc["co2_ibrido_t_anno"] - bc["co2_base_t_anno"])
        self.assertAlmostEqual(
            bc["curt_persa_mwh"],
            bc["e_curt_mwh"] - bc["e_ch_curt_mwh"])
        self.assertAlmostEqual(
            bc["be_capex_batt_eur_kwh"],
            bc["delta_margine"] * bc["fattore_rendita"]
            / (bc["e_batt_mwh"] * 1000.0))
        self.assertAlmostEqual(
            bc["be_p_peak_eur_mwh"],
            (bc["capex_batt"] / bc["fattore_rendita"]
             + bc["om_batt"]
             + bc["e_ch_arb_mwh"] * bc["p_base"])
            / bc["e_dis_mwh"])
        for s in bc["scenari"]:
            self.assertEqual(len(s["nome"]) > 0, True)
            # Il ricavo base dello scenario dipende
            # dalla sua q_curt (il curtailment alto
            # abbassa anche il ricavo base).
            ric_base_scen = (bc["e_fv_mwh"]
                             * (1.0 - s["q_curt"])
                             * bc["p_base"])
            self.assertAlmostEqual(
                s["delta_margine"],
                s["ricavo_ibrido"] - ric_base_scen
                - bc["om_batt"])
        conf = bc["confronto"]
        self.assertAlmostEqual(
            conf["delta_ricavo"],
            conf["ricavo_ibrido"] - conf["ricavo_base"])
        self.assertAlmostEqual(
            conf["margine_ibrido"],
            conf["ricavo_ibrido"] - conf["om_ibrido"])
        self.assertAlmostEqual(
            conf["capex_ibrido"],
            conf["capex_base"] + conf["capex_batt"])

    def test_scenari_migliorano_sul_base(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        for s in bc["scenari"][1:]:
            self.assertGreater(s["van"], base["van"])
            self.assertGreater(s["tir"], base["tir"])

    def test_sensibilita_valori(self):
        s = mh896_sensibilita(**mh896_demo())
        self.assertEqual(set(s.keys()),
                         {"p_peak_180", "capex_batt_150",
                          "q_curt_020", "rte_095", "vita_10",
                          "tasso_010", "om_batt_000", "q_arb_000",
                          "recupero_100"})
        attesi = {
            "p_peak_180": (212543.35, 8.00, 9, "CONVIENTE"),
            "capex_batt_150": (24307.37, 5.59, 10, "CONVIENTE"),
            "q_curt_020": (-89214.07, 3.65, 12, "MARGINALE"),
            "rte_095": (-254034.74, 0.95, 14, "NON_CONVIENTE"),
            "vita_10": (-535559.26, -8.32, None, "NON_CONVIENTE"),
            "tasso_010": (-542515.61, -1.26, None, "NON_CONVIENTE"),
            "om_batt_000": (-43543.57, 4.35, 11, "MARGINALE"),
            "q_arb_000": (-676686.11, -8.29, None, "NON_CONVIENTE"),
            "recupero_100": (-268263.17, 0.71, 15, "NON_CONVIENTE"),
        }
        for nome, (van, tir, pb, verd) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(s[nome]["van"], van, places=2)
                self.assertAlmostEqual(s[nome]["tir"], tir, places=2)
                self.assertEqual(s[nome]["payback"], pb)
                self.assertEqual(s[nome]["verdetto"], verd)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh896_csv(bc, mh896_demo())
        for voce in ("p_fv_mwp", "resa_kwh_kwp", "p_conn_mw",
                     "q_curt", "p_batt_mw", "e_batt_mwh",
                     "rte", "dod", "cicli", "recupero",
                     "q_arb", "p_base", "p_peak",
                     "capex_fv_eur_kwp", "capex_batt_eur_kwh",
                     "om_fv_eur_kwp", "om_batt_eur_kwh",
                     "tasso", "vita_anni", "tolleranza_pct",
                     "co2_t_mwh", "e_fv_mwh", "e_curt_mwh",
                     "e_ch_max_mwh", "e_ch_curt_mwh",
                     "e_ch_arb_mwh", "e_ch_tot_mwh",
                     "e_dis_mwh", "e_diretta_mwh",
                     "e_venduta_mwh", "ricavo_base",
                     "ricavo_ibrido", "delta_ricavo",
                     "om_batt", "delta_margine", "capex_batt",
                     "capex_fv", "om_fv", "margine_base",
                     "margine_ibrido", "fattore_rendita",
                     "van", "tir", "payback",
                     "be_capex_batt_eur_kwh",
                     "be_p_peak_eur_mwh",
                     "co2_base_t_anno", "co2_ibrido_t_anno",
                     "delta_co2_t_anno", "curt_persa_mwh",
                     "scenario_base_van", "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_spread_alto_van",
                     "scenario_spread_alto_verdetto",
                     "scenario_batteria_economica_van",
                     "scenario_batteria_economica_verdetto",
                     "scenario_curtailment_alto_van",
                     "scenario_curtailment_alto_verdetto",
                     "confronto_ricavo_base",
                     "confronto_ricavo_ibrido",
                     "confronto_om_base",
                     "confronto_om_ibrido",
                     "confronto_margine_base",
                     "confronto_margine_ibrido",
                     "confronto_capex_base",
                     "confronto_capex_ibrido",
                     "confronto_van_delta",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("NON_CONVIENTE", csv)
        self.assertIn("CONVIENTE", csv)
        self.assertIn("MARGINALE", csv)

    def test_df_scenari_bilancio_confronto_flussi_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 4)
        self.assertEqual(len(bc["df_bilancio"]), 6)
        self.assertEqual(len(bc["df_confronto"]), 4)
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 51)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso delta (EUR/anno)"].iloc[0],
                         -1000000.0)
        self.assertAlmostEqual(
            bc["df_flussi"]["Cumulato (EUR)"].iloc[-1], -97792.00,
            places=2)
        self.assertEqual(
            list(bc["df_bilancio"]["Voce"]),
            ["Produzione FV", "Curtailment totale",
             "Carica batteria", "Scarica batteria",
             "Vendita diretta", "Vendita totale"])
        self.assertAlmostEqual(
            bc["df_bilancio"]["MWh/anno"].iloc[0], 5750.00)
        self.assertAlmostEqual(
            bc["df_bilancio"]["MWh/anno"].iloc[-1], 5457.44)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Ricavo (EUR/anno)", "O&M (EUR/anno)",
             "Margine (EUR/anno)", "CAPEX (EUR)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["FV solo"].iloc[0], 379500.00)
        self.assertAlmostEqual(
            bc["df_confronto"]["FV piu batteria"].iloc[0], 471647.20)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Energia FV (MWh/anno)", voci)
        self.assertIn("Energia scaricata (MWh/anno)", voci)
        self.assertIn("Breakeven CAPEX batteria (EUR/kWh)", voci)
        self.assertIn("Breakeven prezzo peak (EUR/MWh)", voci)
        self.assertIn("Delta CO2 (t/anno)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN delta (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh896_csv(bc, mh896_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_fv_mwh;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh896_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh896_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh896_calcola(**_demo_kwargs(capex_batt_eur_kwh=0))
        self.assertEqual(bc["capex_batt"], 0.0)
        self.assertAlmostEqual(bc["van"], 624307.37, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh896_calcola(**_demo_kwargs(om_batt_eur_kwh=0))
        self.assertEqual(bc["om_batt"], 0.0)
        self.assertAlmostEqual(bc["van"], -43543.57, places=2)
        self.assertEqual(bc["verdetto"], "MARGINALE")
        bc = mh896_calcola(**_demo_kwargs(co2_t_mwh=0))
        self.assertEqual(bc["co2_ibrido_t_anno"], 0.0)
        self.assertEqual(bc["co2_base_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh896_calcola(**_demo_kwargs(p_batt_mw=0))
        self.assertEqual(bc["p_batt_mw"], 0.0)
        self.assertAlmostEqual(bc["van"], -375692.63, places=2)


class TestCasiLimite(unittest.TestCase):
    def test_p_peak_uguale_p_base_non_calcolabile(self):
        # Prezzo peak uguale al prezzo base: lo
        # spread sparisce, il delta margine diventa
        # meno 2192,00: non calcolabile negli helper
        # (VAN None) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(p_peak=75.0)
        bc = mh896_calcola(**kw)
        self.assertEqual(bc["delta_margine"], -2192.0)
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")

    def test_p_peak_zero_non_calcolabile(self):
        kw = _demo_kwargs(p_peak=0.0)
        bc = mh896_calcola(**kw)
        self.assertEqual(bc["delta_margine"], -87200.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_q_curt_zero(self):
        # Senza curtailment resta solo
        # l'arbitraggio: delta margine 1982,50,
        # VAN meno 979422,33, TIR meno 28,17 %,
        # payback nessuno.
        bc = mh896_calcola(**_demo_kwargs(q_curt=0.0))
        self.assertEqual(bc["e_curt_mwh"], 0.0)
        self.assertEqual(bc["e_ch_curt_mwh"], 0.0)
        self.assertEqual(bc["e_ch_arb_mwh"], 862.5)
        self.assertEqual(bc["e_dis_mwh"], 759.0)
        self.assertAlmostEqual(bc["delta_margine"], 1982.50,
                               places=2)
        self.assertAlmostEqual(bc["van"], -979422.33, places=2)
        self.assertAlmostEqual(bc["tir"], -28.17, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_q_curt_uno_convente(self):
        # Tutto curtailato: la batteria carica
        # solo curtailment, E_venduta = E_dis.
        bc = mh896_calcola(**_demo_kwargs(q_curt=1.0))
        self.assertEqual(bc["e_curt_mwh"], 5750.0)
        self.assertEqual(bc["e_venduta_mwh"], 1133.44)
        self.assertAlmostEqual(bc["delta_margine"], 115347.20,
                               places=2)
        self.assertAlmostEqual(bc["van"], 197264.49, places=2)
        self.assertAlmostEqual(bc["tir"], 7.79, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_recupero_zero(self):
        # Senza recupero di curtailment la carica
        # arriva solo da arbitraggio: stessi numeri
        # del caso q_curt zero sul delta margine.
        bc = mh896_calcola(**_demo_kwargs(recupero=0.0))
        self.assertEqual(bc["e_ch_curt_mwh"], 0.0)
        self.assertAlmostEqual(bc["delta_margine"], 1982.50,
                               places=2)
        self.assertAlmostEqual(bc["van"], -979422.33, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_rte_uno(self):
        # RTE perfetta: nessuna perdita in
        # scarica, VAN meno 167136,24, TIR 2,41 %,
        # payback 13.
        bc = mh896_calcola(**_demo_kwargs(rte=1.0))
        self.assertEqual(bc["e_dis_mwh"], 1288.0)
        self.assertAlmostEqual(bc["van"], -167136.24, places=2)
        self.assertAlmostEqual(bc["tir"], 2.41, places=2)
        self.assertEqual(bc["payback"], 13)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_cicli_zero_non_calcolabile(self):
        kw = _demo_kwargs(cicli=0)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        self.assertFalse(mh896_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_vita_zero_e_non_intera_non_calcolabili(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        kw = _demo_kwargs(vita_anni=15.5)
        self.assertRaises(ValueError, mh896_calcola, **kw)

    def test_p_fv_e_resa_e_batt_zero_non_calcolabili(self):
        for campo in ("p_fv_mwp", "resa_kwh_kwp", "e_batt_mwh"):
            kw = _demo_kwargs(**{campo: 0})
            self.assertRaises(ValueError, mh896_calcola, **kw)

    def test_rte_e_dod_zero_non_calcolabili(self):
        for campo in ("rte", "dod"):
            kw = _demo_kwargs(**{campo: 0})
            self.assertRaises(ValueError, mh896_calcola, **kw)

    def test_tasso_zero_e_uno_non_calcolabili(self):
        kw = _demo_kwargs(tasso=0.0)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        kw = _demo_kwargs(tasso=1.0)
        self.assertRaises(ValueError, mh896_calcola, **kw)

    def test_vita_dieci_e_tasso_dieci(self):
        bc = mh896_calcola(**_demo_kwargs(vita_anni=10))
        self.assertAlmostEqual(bc["van"], -535559.26, places=2)
        self.assertAlmostEqual(bc["tir"], -8.32, places=2)
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh896_calcola(**_demo_kwargs(tasso=0.10))
        self.assertAlmostEqual(bc["van"], -542515.61, places=2)
        self.assertAlmostEqual(bc["tir"], -1.26, places=2)
        self.assertIsNone(bc["payback"])

    def test_tolleranza_zero_bordo(self):
        # Con tolleranza zero ogni VAN negativa e'
        # NON_CONVIENTE, anche quella dello scenario
        # curtailment alto.
        bc = mh896_calcola(**_demo_kwargs(tolleranza_pct=0))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "NON_CONVIENTE")
        bc = mh896_calcola(**_demo_kwargs(p_peak=180.0,
                                          tolleranza_pct=0))
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_batt_zero_tir_non_definita_payback_zero(self):
        bc = mh896_calcola(**_demo_kwargs(capex_batt_eur_kwh=0))
        self.assertEqual(bc["capex_batt"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(p_fv_mwp="5.0")
        self.assertRaises(ValueError, mh896_calcola, **kw)
        kw = _demo_kwargs(p_fv_mwp=True)
        self.assertRaises(ValueError, mh896_calcola, **kw)
        val = mh896_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def896\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh896_demo().keys()), lette - set(mh896_demo().keys()))
        self.assertEqual(lette, set(mh896_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc896\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc896\["([^"]+)"\]', src))
        attese = set(mh896_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 895 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 896.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 897)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab896:"), 1)
        self.assertTrue(src.startswith("    # W901"))

    def test_ui_tab896_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab896:"), 1)
        self.assertIn("def mh896_demo(", src_h)
        self.assertIn("def mh896_calcola(", src_h)
        self.assertIn("tab896", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Ibrido FV + accumulo colocato: un solo allaccio, due ricavi, il sizing della batteria paga?", src)
        self.assertIn("☀️🔋 Ibrido FV + accumulo co-locato: un solo allaccio, due ricavi — il sizing della batteria paga?", src)
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
        chiavi = re.findall(r'key="(st896_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st896_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 27)
        self.assertIn('key="st896_calcola"', src)
        self.assertIn('key="st896_csv"', src)
        self.assertIn('key="st896_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg896"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("_delta_marg896 <= 0.0", src)

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
        # "co-locato" e un trattino lungo).
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
