"""Test nuova scheda NZEB: l'edificio a
energia quasi zero paga?
Repo path: tests/test_w898_nzeb.py

Business case retrofit integrato verso
NZEB (edificio a energia quasi zero)
contro baseline caldaia a gas piu rete
elettrica: involucro piu pompa di calore
piu fotovoltaico piu ventilazione,
valutati INSIEME come un solo intervento,
con verifica dello standard NZEB intero
edificio (energia primaria non
rinnovabile entro soglia e quota FER
almeno soglia). Driver: superficie S
(demo 1000 m2), fabbisogno termico
specifico pre e post q_pre e q_post
(demo 120 e 35 kWh/m2/anno), usi
elettrici e_el (demo 25 kWh/m2/anno),
SCOP (demo 3,5), potenza FV P_fv (demo
40 kWp) e resa y_fv (demo 1100
kWh/kWp/anno): Q_pre = 1000 per 120 =
120000 kWh/anno; Q_post = 1000 per 35 =
35000 kWh/anno; E_usi = 1000 per 25 =
25000 kWh/anno; F_gas_pre = 120000
diviso 0,90 = 133333,33 kWh/anno; E_fv
= 40 per 1100 = 44000 kWh/anno; E_pdc
= 35000 diviso 3,5 = 10000 kWh/anno;
E_fv_ac = minimo tra 44000 per 0,70 =
30800 e 25000 piu 10000 = 35000, quindi
30800 kWh/anno; E_fv_exp = 44000 meno
30800 = 13200 kWh/anno; E_prelievo =
25000 piu 10000 meno 30800 = 4200
kWh/anno; C_base = 133333,33 per 0,09
piu 25000 per 0,25 = 18250 EUR/anno;
C_post = 4200 per 0,25 piu 2000 meno
13200 per 0,08 = 1994 EUR/anno;
risparmio 16256 EUR/anno; EP_nren_pre
= (133333,33 per 1,05 piu 25000 per
1,95) diviso 1000 = 188,75 kWh/m2/anno;
EP_nren_post = 4200 per 1,95 diviso
1000 = 8,19 kWh/m2/anno; Q_amb = 35000
meno 10000 = 25000 kWh/anno; EP_ren_post
= (30800 piu 25000) diviso 1000 = 55,80
kWh/m2/anno; quota FER = 100 per 55,80
diviso 63,99 = 87,20 %; CO2 pre =
(133333,33 per 0,20 piu 25000 per 0,35)
diviso 1000 = 35,42 t/anno; CO2 post =
4200 per 0,35 diviso 1000 = 1,47 t/anno;
CO2 evitata 33,95 t/anno; CAPEX 150000
piu 35000 piu 40000 piu 20000 = 245000
EUR (somma verificata a mano); flussi
[CAPEX negativo, risparmio per vita];
VAN al tasso (FRAZIONE in ingresso, 0,05
= 5 %, usato diretto, NON diviso per
100); TIR per bisezione su intervallo da
meno 0,9 a 5,0; payback (primo anno con
cumulato maggiore o uguale a 0).
Tolleranza in PERCENTUALE (10 = 10 % del
CAPEX). I flussi piatti sono una
SEMPLIFICAZIONE DICHIARATA (profilo
reale variabile con clima, carico e
prezzi, qui valore medio costante);
fattori di energia primaria fissi (gas
1,05, elettricita 1,95, DM 26/06/2015
stile UNI TS 11300); quota FER da
energia primaria (EP_ren diviso somma
EP). NZEB RAGGIUNTO se EP_nren_post
entro soglia_ep_nren (demo 40) e quota
FER almeno soglia_fer_pct (demo 50):
demo 8,19 entro 40 e 87,20 almeno 50,
quindi RAGGIUNTO. Lo stato NZEB NON
entra nel verdetto economico.
Verdetto: NON_CALCOLABILE se input
degenere (superficie nulla o negativa,
fabbisogno pre nullo o negativo,
fabbisogno post nullo o negativo, usi
elettrici negativi, eta caldaia nulla o
negativa o sopra 1, SCOP nullo o
negativo, potenza FV negativa, resa FV
negativa, quota autoconsumo sotto 0 o
sopra 1, prezzi negativi, fattori CO2
negativi, fattori energia primaria nulli
o negativi, CAPEX negativi, O&M
negativa, tasso negativo, vita nulla o
negativa o non intera, tolleranza
negativa, soglie nulle o negative) o se
risparmio minore o uguale a 0 (guard
degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN
maggiore di 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: superficie o fabbisogni o
eta caldaia o SCOP o fattori energia
primaria o soglie a zero non calcolabili
(divisione o soglia); vita zero o non
intera non calcolabile (ValueError negli
helper, guard NON_CALCOLABILE in UI);
quota autoconsumo zero (risparmio
11020,00 ma quota FER 26,81 %: NZEB NON
RAGGIUNTO); FV zero (risparmio 7500,00,
quota FER 26,81 %: NZEB NON RAGGIUNTO);
usi elettrici zero (prelievo zero, quota
FER 100 %); O&M 20000 (risparmio
negativo meno 1744,00, NON_CALCOLABILE);
CAPEX zero (TIR non definita, payback 0);
tasso zero (VAN uguale alla somma dei
flussi).
Distinzione esplicita: qui SOLO retrofit
integrato verso NZEB intero edificio
(involucro piu pompa di calore piu
fotovoltaico piu ventilazione, con
verifica EP non rinnovabile e quota FER),
NIENTE cappotto termico da solo (tab652,
li solo involucro), NIENTE serramenti da
soli (li solo infissi), NIENTE
teleriscaldamento (li calore da rete
esterna), NIENTE pompe di calore singole
(li solo generatore), NIENTE fotovoltaico
singolo (li solo produzione elettrica),
NIENTE cogenerazione CAR (tab727, li
certificati e risparmio di energia
primaria).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w898_helpers import (
        demo_calcoli,
        mh893_c_base,
        mh893_c_post,
        mh893_calcola,
        mh893_capex,
        mh893_co2_post,
        mh893_co2_pre,
        mh893_csv,
        mh893_demo,
        mh893_demo_calcoli,
        mh893_e_fv,
        mh893_e_fv_ac,
        mh893_e_pdc,
        mh893_e_prelievo,
        mh893_e_usi,
        mh893_ep_nren_post,
        mh893_ep_nren_pre,
        mh893_ep_ren_post,
        mh893_f_gas,
        mh893_flussi,
        mh893_frazione,
        mh893_frazione_pos,
        mh893_int_pos,
        mh893_nneg,
        mh893_num,
        mh893_nzeb,
        mh893_payback,
        mh893_pos,
        mh893_q,
        mh893_quota_fer,
        mh893_risparmio,
        mh893_sensibilita,
        mh893_tir,
        mh893_valida,
        mh893_van,
        mh893_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w898_helpers", os.path.join(_hf, "w898_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh893_c_base = _mod.mh893_c_base
    mh893_c_post = _mod.mh893_c_post
    mh893_calcola = _mod.mh893_calcola
    mh893_capex = _mod.mh893_capex
    mh893_co2_post = _mod.mh893_co2_post
    mh893_co2_pre = _mod.mh893_co2_pre
    mh893_csv = _mod.mh893_csv
    mh893_demo = _mod.mh893_demo
    mh893_demo_calcoli = _mod.mh893_demo_calcoli
    mh893_e_fv = _mod.mh893_e_fv
    mh893_e_fv_ac = _mod.mh893_e_fv_ac
    mh893_e_pdc = _mod.mh893_e_pdc
    mh893_e_prelievo = _mod.mh893_e_prelievo
    mh893_e_usi = _mod.mh893_e_usi
    mh893_ep_nren_post = _mod.mh893_ep_nren_post
    mh893_ep_nren_pre = _mod.mh893_ep_nren_pre
    mh893_ep_ren_post = _mod.mh893_ep_ren_post
    mh893_f_gas = _mod.mh893_f_gas
    mh893_flussi = _mod.mh893_flussi
    mh893_frazione = _mod.mh893_frazione
    mh893_frazione_pos = _mod.mh893_frazione_pos
    mh893_int_pos = _mod.mh893_int_pos
    mh893_nneg = _mod.mh893_nneg
    mh893_num = _mod.mh893_num
    mh893_nzeb = _mod.mh893_nzeb
    mh893_payback = _mod.mh893_payback
    mh893_pos = _mod.mh893_pos
    mh893_q = _mod.mh893_q
    mh893_quota_fer = _mod.mh893_quota_fer
    mh893_risparmio = _mod.mh893_risparmio
    mh893_sensibilita = _mod.mh893_sensibilita
    mh893_tir = _mod.mh893_tir
    mh893_valida = _mod.mh893_valida
    mh893_van = _mod.mh893_van
    mh893_verdetto = _mod.mh893_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w898_helpers.py")
_UI_PATH = _risolvi("w898_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "2"
_VECCHIO_TAB = "tab89" + "2"
_VECCHIO_ST = "st89" + "2_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "q_pre_kwh_anno": 120000.0,
    "q_post_kwh_anno": 35000.0,
    "e_usi_kwh_anno": 25000.0,
    "f_gas_kwh_anno": 133333.33333333334,
    "e_fv_kwh_anno": 44000.0,
    "e_fv_ac_kwh_anno": 30799.999999999996,
    "e_fv_exp_kwh_anno": 13200.000000000004,
    "e_pdc_kwh_anno": 10000.0,
    "e_prelievo_kwh_anno": 4200.000000000004,
    "c_base_eur_anno": 18250.0,
    "c_post_eur_anno": 1994.0000000000007,
    "risparmio_eur_anno": 16256.0,
    "ep_nren_pre": 188.75000000000003,
    "ep_nren_post": 8.190000000000007,
    "q_amb_kwh_anno": 25000.0,
    "ep_ren_post": 55.8,
    "quota_fer_pct": 87.20112517580871,
    "co2_pre_t_anno": 35.41666666666667,
    "co2_post_t_anno": 1.470000000000001,
    "co2_evitata_t_anno": 33.94666666666667,
    "capex_eur": 245000.0,
    "van": -15888.837134376541,
    "tir": 4.342640761744288,
    "payback": 16,
}

_ORDINE_VALIDA = (
    "superficie_m2", "q_pre", "q_post", "e_el",
    "eta_caldaia", "scop", "p_fv_kwp", "y_fv",
    "quota_autoconsumo", "p_gas", "p_el", "p_vendita",
    "f_gas", "f_el", "fp_nren_gas", "fp_nren_el", "fp_ren",
    "capex_involucro", "capex_pdc", "capex_fv", "capex_vent",
    "om_eur_anno", "tasso", "vita_anni", "tolleranza_pct",
    "soglia_ep_nren", "soglia_fer_pct")


def _demo_kwargs(**over):
    kw = dict(mh893_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh893_num(3, "x"), 3.0)
        self.assertEqual(mh893_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh893_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh893_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh893_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh893_pos(0, "x")
        with self.assertRaises(ValueError):
            mh893_pos(-1, "x")
        self.assertEqual(mh893_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh893_int_pos(25, "x"), 25)
        self.assertEqual(mh893_int_pos(25.0, "x"), 25)
        with self.assertRaises(ValueError):
            mh893_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh893_int_pos(25.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh893_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh893_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh893_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh893_frazione(1.1, "x")

    def test_frazione_pos_intervallo(self):
        self.assertEqual(mh893_frazione_pos(0.90, "x"), 0.90)
        self.assertEqual(mh893_frazione_pos(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh893_frazione_pos(0.0, "x")
        with self.assertRaises(ValueError):
            mh893_frazione_pos(-0.1, "x")
        with self.assertRaises(ValueError):
            mh893_frazione_pos(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_fabbisogni_e_usi(self):
        self.assertEqual(mh893_q(1000, 120), 120000)
        self.assertEqual(mh893_q(1000, 35), 35000)
        self.assertEqual(mh893_e_usi(1000, 25), 25000)
        self.assertEqual(mh893_e_usi(1000, 0), 0)
        with self.assertRaises(ValueError):
            mh893_q(0, 120)
        with self.assertRaises(ValueError):
            mh893_q(1000, 0)

    def test_gas_pre_e_fotovoltaico_e_pdc(self):
        self.assertAlmostEqual(mh893_f_gas(120000, 0.90),
                               133333.33, places=2)
        self.assertEqual(mh893_f_gas(120000, 1.0), 120000.0)
        self.assertEqual(mh893_e_fv(40, 1100), 44000)
        self.assertEqual(mh893_e_fv(0, 1100), 0)
        self.assertEqual(mh893_e_pdc(35000, 3.5), 10000.0)
        # Con SCOP 1 tutta l'energia termica
        # post e' elettricita'.
        self.assertEqual(mh893_e_pdc(35000, 1.0), 35000.0)
        with self.assertRaises(ValueError):
            mh893_f_gas(120000, 0)
        with self.assertRaises(ValueError):
            mh893_e_pdc(35000, 0)

    def test_autoconsumo_minimo_tra_produzione_e_domanda(self):
        self.assertAlmostEqual(
            mh893_e_fv_ac(44000, 0.70, 25000, 10000), 30800.0)
        # Con quota 1 la domanda (35000) limita
        # l'autoconsumo: il resto e' eccedenza.
        self.assertEqual(mh893_e_fv_ac(44000, 1.0, 25000, 10000),
                         35000.0)
        # Con produzione bassa tutta la produzione
        # viene autoconsumata.
        self.assertEqual(mh893_e_fv_ac(10000, 1.0, 25000, 10000),
                         10000.0)
        # Con quota 0 niente autoconsumo.
        self.assertEqual(mh893_e_fv_ac(44000, 0.0, 25000, 10000), 0.0)
        with self.assertRaises(ValueError):
            mh893_e_fv_ac(44000, 1.1, 25000, 10000)

    def test_prelievo(self):
        self.assertEqual(mh893_e_prelievo(25000, 10000, 30800), 4200)
        self.assertEqual(mh893_e_prelievo(25000, 10000, 35000), 0)
        with self.assertRaises(ValueError):
            mh893_e_prelievo(25000, 10000, -1)

    def test_costi_base_e_post(self):
        self.assertAlmostEqual(
            mh893_c_base(133333.33333333334, 0.09, 25000, 0.25),
            18250.0, places=2)
        self.assertAlmostEqual(
            mh893_c_post(4200, 0.25, 2000, 13200, 0.08),
            1994.0, places=2)
        self.assertAlmostEqual(
            mh893_risparmio(18250.0, 1994.0), 16256.0, places=2)
        # Con vendita zero il costo post sale
        # di 1056 EUR/anno (13200 per 0,08).
        self.assertAlmostEqual(
            mh893_c_post(4200, 0.25, 2000, 13200, 0.0),
            3050.0, places=2)

    def test_energia_primaria(self):
        self.assertAlmostEqual(
            mh893_ep_nren_pre(133333.33333333334, 1.05, 25000, 1.95,
                              1000),
            188.75, places=2)
        self.assertAlmostEqual(
            mh893_ep_nren_post(4200, 1.95, 1000), 8.19, places=2)
        self.assertEqual(mh893_ep_nren_post(0, 1.95, 1000), 0.0)
        self.assertAlmostEqual(
            mh893_ep_ren_post(30800, 25000, 1.00, 1000), 55.80,
            places=2)
        # Con fattore rinnovabile 2 il valore
        # raddoppia: il fattore pesa su
        # autoconsumo e calore ambiente.
        self.assertAlmostEqual(
            mh893_ep_ren_post(30800, 25000, 2.00, 1000), 111.60,
            places=2)
        with self.assertRaises(ValueError):
            mh893_ep_nren_pre(133333.33, 0, 25000, 1.95, 1000)
        with self.assertRaises(ValueError):
            mh893_ep_ren_post(30800, 25000, 0, 1000)

    def test_quota_fer(self):
        self.assertAlmostEqual(mh893_quota_fer(55.8, 8.19), 87.20,
                               places=2)
        self.assertEqual(mh893_quota_fer(60.0, 0.0), 100.0)
        self.assertEqual(mh893_quota_fer(0.0, 68.25), 0.0)
        self.assertEqual(mh893_quota_fer(0.0, 0.0), 0.0)

    def test_co2_pre_e_post(self):
        self.assertAlmostEqual(
            mh893_co2_pre(133333.33333333334, 0.20, 25000, 0.35),
            35.42, places=2)
        self.assertAlmostEqual(mh893_co2_post(4200, 0.35), 1.47,
                               places=2)
        self.assertEqual(mh893_co2_post(0, 0.35), 0.0)
        # Con fattori zero la CO2 pre e' zero.
        self.assertEqual(mh893_co2_pre(133333.33, 0.0, 25000, 0.0),
                         0.0)

    def test_capex_somma_quattro(self):
        self.assertEqual(mh893_capex(150000, 35000, 40000, 20000),
                         245000.0)
        self.assertEqual(mh893_capex(0, 0, 0, 0), 0.0)
        self.assertEqual(mh893_capex(150000, 0, 0, 0), 150000.0)
        with self.assertRaises(ValueError):
            mh893_capex(-1, 35000, 40000, 20000)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh893_flussi(245000, 16256.0, 3),
                         [-245000, 16256.0, 16256.0, 16256.0])

    def test_van_tasso_zero_e_cinque(self):
        self.assertAlmostEqual(mh893_van([-100, 60, 60], 0), 20.0)
        bc = mh893_demo_calcoli()
        self.assertAlmostEqual(mh893_van(bc["flussi"], 0.05), bc["van"])

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' meno 15888,84; con 5,0 (cioe' 500 %
        # se letto come frazione) sarebbe tutt'altra.
        bc = mh893_demo_calcoli()
        self.assertAlmostEqual(mh893_van(bc["flussi"], 0.05),
                               -15888.84, places=2)
        self.assertNotAlmostEqual(mh893_van(bc["flussi"], 5.0),
                                  -15888.84, places=2)

    def test_tir_demo(self):
        bc = mh893_demo_calcoli()
        tir = mh893_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh893_tir([-100, -10, -10]))
        self.assertIsNone(mh893_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh893_demo_calcoli()
        self.assertEqual(mh893_payback(bc["flussi"]), 16)
        self.assertIsNone(mh893_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh893_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh893_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:16]), -1160.00, places=2)
        self.assertAlmostEqual(sum(flussi[:17]), 15096.00, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh893_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh893_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh893_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh893_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh893_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh893_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh893_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_nzeb_funzione(self):
        self.assertTrue(mh893_nzeb(8.19, 87.20, 40, 50))
        self.assertTrue(mh893_nzeb(40.0, 50.0, 40, 50))
        self.assertFalse(mh893_nzeb(8.19, 49.0, 40, 50))
        self.assertFalse(mh893_nzeb(41.0, 87.20, 40, 50))
        self.assertFalse(mh893_nzeb(0.0, 0.0, 40, 50))
        with self.assertRaises(ValueError):
            mh893_nzeb(8.19, 87.20, 0, 50)
        with self.assertRaises(ValueError):
            mh893_nzeb(8.19, 87.20, 40, 0)

    def test_valida_demo_ok(self):
        demo = mh893_demo()
        val = mh893_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)
        kw = _demo_kwargs(vita_anni=25.5)
        self.assertRaises(ValueError, mh893_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10)
        bc = mh893_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("superficie_m2", 0),
                              ("q_pre", 0),
                              ("q_post", 0),
                              ("eta_caldaia", 0),
                              ("scop", 0),
                              ("fp_nren_gas", 0),
                              ("fp_nren_el", 0),
                              ("fp_ren", 0),
                              ("soglia_ep_nren", 0),
                              ("soglia_fer_pct", 0)):
            with self.assertRaises(ValueError):
                mh893_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_quota_sopra_uno_no(self):
        kw = _demo_kwargs(quota_autoconsumo=1.1)
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_valida_frazioni_sopra_uno_no(self):
        for campo, valore in (("eta_caldaia", 1.1),):
            with self.assertRaises(ValueError):
                mh893_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("superficie_m2", -1),
                              ("q_pre", -1),
                              ("q_post", -1),
                              ("e_el", -1),
                              ("eta_caldaia", -0.1),
                              ("scop", -1),
                              ("p_fv_kwp", -1),
                              ("y_fv", -1),
                              ("quota_autoconsumo", -0.1),
                              ("p_gas", -0.01),
                              ("p_el", -0.01),
                              ("p_vendita", -0.01),
                              ("f_gas", -0.01),
                              ("f_el", -0.01),
                              ("fp_nren_gas", -0.01),
                              ("fp_nren_el", -0.01),
                              ("fp_ren", -0.01),
                              ("capex_involucro", -1),
                              ("capex_pdc", -1),
                              ("capex_fv", -1),
                              ("capex_vent", -1),
                              ("om_eur_anno", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("soglia_ep_nren", -1),
                              ("soglia_fer_pct", -1)):
            with self.assertRaises(ValueError):
                mh893_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh893_calcola(mh893_demo())
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertTrue(bc["nzeb_raggiunto"])

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh893_calcola(dict(mh893_demo(), capex_involucro=999999),
                           capex_involucro=150000)
        self.assertEqual(bc["capex_eur"], 245000.0)


class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, int):
                    self.assertEqual(ottenuto, atteso)
                else:
                    self.assertLess(_rel(ottenuto, atteso), 1e-9)

    def test_demo_verdetto_marginale_e_nzeb(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertTrue(bc["nzeb_raggiunto"])
        self.assertTrue(bc["nzeb"])
        self.assertLess(bc["van"], 0.0)
        self.assertLessEqual(abs(bc["van"]),
                            bc["tolleranza_pct"] / 100.0
                            * bc["capex_eur"])
        self.assertEqual(bc["payback"], 16)
        self.assertAlmostEqual(bc["tir"], 4.34, places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_post_eur_anno"])
        self.assertAlmostEqual(
            bc["q_pre_kwh_anno"],
            bc["superficie_m2"] * bc["q_pre"])
        self.assertAlmostEqual(
            bc["q_post_kwh_anno"],
            bc["superficie_m2"] * bc["q_post"])
        self.assertAlmostEqual(
            bc["e_usi_kwh_anno"],
            bc["superficie_m2"] * bc["e_el"])
        self.assertAlmostEqual(
            bc["f_gas_kwh_anno"],
            bc["q_pre_kwh_anno"] / bc["eta_caldaia"])
        self.assertAlmostEqual(
            bc["e_fv_kwh_anno"],
            bc["p_fv_kwp"] * bc["y_fv"])
        self.assertAlmostEqual(
            bc["e_pdc_kwh_anno"],
            bc["q_post_kwh_anno"] / bc["scop"])
        self.assertAlmostEqual(
            bc["e_fv_ac_kwh_anno"],
            min(bc["e_fv_kwh_anno"] * bc["quota_autoconsumo"],
                bc["e_usi_kwh_anno"] + bc["e_pdc_kwh_anno"]))
        self.assertAlmostEqual(
            bc["e_fv_exp_kwh_anno"],
            bc["e_fv_kwh_anno"] - bc["e_fv_ac_kwh_anno"])
        self.assertAlmostEqual(
            bc["e_prelievo_kwh_anno"],
            bc["e_usi_kwh_anno"] + bc["e_pdc_kwh_anno"]
            - bc["e_fv_ac_kwh_anno"])
        self.assertAlmostEqual(
            bc["c_base_eur_anno"],
            bc["f_gas_kwh_anno"] * bc["p_gas"]
            + bc["e_usi_kwh_anno"] * bc["p_el"])
        self.assertAlmostEqual(
            bc["c_post_eur_anno"],
            bc["e_prelievo_kwh_anno"] * bc["p_el"]
            + bc["om_eur_anno"]
            - bc["e_fv_exp_kwh_anno"] * bc["p_vendita"])
        self.assertAlmostEqual(
            bc["ep_nren_pre"],
            (bc["f_gas_kwh_anno"] * bc["fp_nren_gas"]
             + bc["e_usi_kwh_anno"] * bc["fp_nren_el"])
            / bc["superficie_m2"])
        self.assertAlmostEqual(
            bc["ep_nren_post"],
            bc["e_prelievo_kwh_anno"] * bc["fp_nren_el"]
            / bc["superficie_m2"])
        self.assertAlmostEqual(
            bc["q_amb_kwh_anno"],
            bc["q_post_kwh_anno"] - bc["e_pdc_kwh_anno"])
        self.assertAlmostEqual(
            bc["ep_ren_post"],
            (bc["e_fv_ac_kwh_anno"] * bc["fp_ren"]
             + bc["q_amb_kwh_anno"] * bc["fp_ren"])
            / bc["superficie_m2"])
        self.assertAlmostEqual(
            bc["quota_fer_pct"],
            100.0 * bc["ep_ren_post"]
            / (bc["ep_ren_post"] + bc["ep_nren_post"]))
        self.assertAlmostEqual(
            bc["co2_pre_t_anno"],
            (bc["f_gas_kwh_anno"] * bc["f_gas"]
             + bc["e_usi_kwh_anno"] * bc["f_el"]) / 1000.0)
        self.assertAlmostEqual(
            bc["co2_post_t_anno"],
            bc["e_prelievo_kwh_anno"] * bc["f_el"] / 1000.0)
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["co2_pre_t_anno"] - bc["co2_post_t_anno"])
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["capex_involucro"] + bc["capex_pdc"]
            + bc["capex_fv"] + bc["capex_vent"])

    def test_sensibilita_valori(self):
        s = mh893_sensibilita(**mh893_demo())
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               17296.00, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               -1231.13, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 15)
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               18656.00, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               17936.63, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 14)
        self.assertEqual(s["p_gas_piu20"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["quota_100"]["risparmio_eur_anno"],
                               16970.00, places=2)
        self.assertAlmostEqual(s["quota_100"]["van"],
                               -5825.76, places=2)
        self.assertEqual(s["quota_100"]["payback"], 15)
        self.assertAlmostEqual(s["quota_100"]["co2_evitata_t_anno"],
                               35.42, places=2)
        self.assertAlmostEqual(s["quota_100"]["quota_fer_pct"],
                               100.00, places=2)
        self.assertEqual(s["quota_100"]["e_prelievo_kwh_anno"], 0.0)
        self.assertAlmostEqual(s["quota_100"]["e_fv_exp_kwh_anno"],
                               9000.00, places=2)
        self.assertAlmostEqual(s["scop_450"]["risparmio_eur_anno"],
                               16811.56, places=2)
        self.assertAlmostEqual(s["scop_450"]["van"],
                               -8058.87, places=2)
        self.assertEqual(s["scop_450"]["payback"], 15)
        self.assertAlmostEqual(s["scop_450"]["co2_evitata_t_anno"],
                               34.72, places=2)
        self.assertAlmostEqual(s["scop_450"]["quota_fer_pct"],
                               93.77, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -260888.84, places=2)
        self.assertIsNone(s["capex_doppio"]["payback"])
        self.assertEqual(s["capex_doppio"]["verdetto"],
                         "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["capex_eur"], 490000.0)
        self.assertAlmostEqual(s["vita_10"]["risparmio_eur_anno"],
                               16256.00, places=2)
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -119475.48, places=2)
        self.assertIsNone(s["vita_10"]["payback"])
        self.assertAlmostEqual(s["tasso_0"]["van"],
                               161400.00, places=2)

    def test_convente_con_gas_caro(self):
        bc = mh893_calcola(**_demo_kwargs(p_gas=0.15))
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 24256.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], 96862.72, places=2)
        self.assertEqual(bc["payback"], 11)
        self.assertTrue(bc["nzeb_raggiunto"])

    def test_non_convente_con_capex_doppio(self):
        bc = mh893_calcola(**_demo_kwargs(
            capex_involucro=300000, capex_pdc=70000,
            capex_fv=80000, capex_vent=40000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -260888.84, places=2)
        self.assertIsNone(bc["payback"])

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh893_calcola(**_demo_kwargs(om_eur_anno=20000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -1744.00,
                               places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh893_csv(bc, mh893_demo())
        for voce in ("superficie_m2", "q_pre", "q_post",
                     "e_el", "eta_caldaia", "scop",
                     "p_fv_kwp", "y_fv", "quota_autoconsumo",
                     "p_gas", "p_el", "p_vendita",
                     "f_gas", "f_el",
                     "fp_nren_gas", "fp_nren_el", "fp_ren",
                     "capex_involucro", "capex_pdc",
                     "capex_fv", "capex_vent",
                     "om_eur_anno", "tasso", "vita_anni",
                     "tolleranza_pct",
                     "soglia_ep_nren", "soglia_fer_pct",
                     "q_pre_kwh_anno", "q_post_kwh_anno",
                     "e_usi_kwh_anno", "f_gas_kwh_anno",
                     "e_fv_kwh_anno", "e_fv_ac_kwh_anno",
                     "e_fv_exp_kwh_anno", "e_pdc_kwh_anno",
                     "e_prelievo_kwh_anno",
                     "c_base_eur_anno", "c_post_eur_anno",
                     "risparmio_eur_anno",
                     "ep_nren_pre", "ep_nren_post",
                     "ep_ren_post", "quota_fer_pct",
                     "co2_pre_t_anno", "co2_post_t_anno",
                     "co2_evitata_t_anno",
                     "nzeb_raggiunto", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("MARGINALE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 26)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -245000.0)
        self.assertEqual(len(bc["df_tabella"]), 53)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie (m2)", voci)
        self.assertIn("Fabbisogno pre (kWh/anno)", voci)
        self.assertIn("Energia FV autoconsumata (kWh/anno)", voci)
        self.assertIn("Prelievo da rete (kWh/anno)", voci)
        self.assertIn("EP non rinnovabile post (kWh/m2/anno)", voci)
        self.assertIn("Quota FER post (%)", voci)
        self.assertIn("CO2 evitata (t/anno)", voci)
        self.assertIn("NZEB raggiunto", voci)

    def test_c_post_piu_caro_con_om_alto(self):
        senza = mh893_c_post(4200, 0.25, 2000, 13200, 0.08)
        con = mh893_c_post(4200, 0.25, 6000, 13200, 0.08)
        self.assertAlmostEqual(con - senza, 4000.0, places=2)

    def test_sensibilita_chiavi_complete(self):
        s = mh893_sensibilita(**mh893_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_piu20", "p_gas_piu20",
                          "quota_100", "scop_450",
                          "capex_doppio", "vita_10", "tasso_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)
            self.assertIn("nzeb_raggiunto", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh893_csv(bc, mh893_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("q_pre_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh893_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh893_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh893_calcola(**_demo_kwargs(e_el=0))
        self.assertEqual(bc["e_usi_kwh_anno"], 0.0)
        self.assertEqual(bc["e_prelievo_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 12720.00,
                               places=2)
        bc = mh893_calcola(**_demo_kwargs(f_el=0))
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], 26.67,
                               places=2)


class TestCasiLimite(unittest.TestCase):
    def test_vita_zero_non_calcolabile(self):
        # Vita zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)
        self.assertFalse(mh893_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_vita_non_intera_non_calcolabile(self):
        kw = _demo_kwargs(vita_anni=25.5)
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_superficie_zero_non_calcolabile(self):
        kw = _demo_kwargs(superficie_m2=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_fabbisogni_zero_non_calcolabili(self):
        kw = _demo_kwargs(q_pre=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)
        kw = _demo_kwargs(q_post=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_eta_e_scop_zero_non_calcolabili(self):
        kw = _demo_kwargs(eta_caldaia=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)
        kw = _demo_kwargs(scop=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_fattori_energia_primaria_zero_non_calcolabili(self):
        for campo in ("fp_nren_gas", "fp_nren_el", "fp_ren"):
            kw = _demo_kwargs(**{campo: 0})
            with self.assertRaises(ValueError):
                mh893_calcola(**kw)

    def test_soglie_zero_non_calcolabili(self):
        kw = _demo_kwargs(soglia_ep_nren=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)
        kw = _demo_kwargs(soglia_fer_pct=0)
        self.assertRaises(ValueError, mh893_calcola, **kw)

    def test_quota_zero_fer_crolla_nzeb_no(self):
        # Con quota autoconsumo zero il risparmio
        # resta positivo (11020,00) ma la quota
        # FER crolla a 26,81 %: NZEB NON RAGGIUNTO,
        # mentre il verdetto resta economico.
        bc = mh893_calcola(**_demo_kwargs(quota_autoconsumo=0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 11020.00,
                               places=2)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["e_fv_ac_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["e_prelievo_kwh_anno"], 35000.00,
                               places=2)
        self.assertAlmostEqual(bc["ep_nren_post"], 68.25, places=2)
        self.assertAlmostEqual(bc["ep_ren_post"], 25.00, places=2)
        self.assertAlmostEqual(bc["quota_fer_pct"], 26.81, places=2)
        self.assertFalse(bc["nzeb_raggiunto"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_fv_zero_nzeb_no(self):
        # Senza fotovoltaico il risparmio e'
        # 7500,00 e la quota FER resta 26,81 %:
        # NZEB NON RAGGIUNTO.
        bc = mh893_calcola(**_demo_kwargs(p_fv_kwp=0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 7500.00,
                               places=2)
        self.assertEqual(bc["e_fv_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["quota_fer_pct"], 26.81, places=2)
        self.assertFalse(bc["nzeb_raggiunto"])

    def test_usi_elettrici_zero_prelievo_zero_fer_cento(self):
        # Con usi elettrici zero il prelievo e'
        # zero (l'autoconsumo copre la pompa di
        # calore) e la quota FER e' 100 %.
        bc = mh893_calcola(**_demo_kwargs(e_el=0))
        self.assertEqual(bc["e_prelievo_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["quota_fer_pct"], 100.00, places=2)
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], 26.67,
                               places=2)
        self.assertTrue(bc["nzeb_raggiunto"])

    def test_scop_basso(self):
        # Con SCOP 2,0 la pompa di calore consuma
        # 17500 kWh/anno: risparmio 14381,00,
        # VAN meno 42314,98, payback 18, quota
        # FER 67,92 %: NZEB RAGGIUNTO comunque.
        bc = mh893_calcola(**_demo_kwargs(scop=2.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 14381.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], -42314.98, places=2)
        self.assertEqual(bc["payback"], 18)
        self.assertAlmostEqual(bc["ep_nren_post"], 22.82, places=2)
        self.assertAlmostEqual(bc["ep_ren_post"], 48.30, places=2)
        self.assertAlmostEqual(bc["quota_fer_pct"], 67.92, places=2)
        self.assertTrue(bc["nzeb_raggiunto"])

    def test_soglie_severe_nzeb_no_verdetto_invariato(self):
        # Lo stato NZEB NON entra nel verdetto:
        # con soglia EP 5 o soglia FER 95 il
        # NZEB diventa NON RAGGIUNTO ma il
        # verdetto resta MARGINALE.
        bc = mh893_calcola(**_demo_kwargs(soglia_ep_nren=5))
        self.assertFalse(bc["nzeb_raggiunto"])
        self.assertEqual(bc["verdetto"], "MARGINALE")
        bc = mh893_calcola(**_demo_kwargs(soglia_fer_pct=95))
        self.assertFalse(bc["nzeb_raggiunto"])
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_fabbisogno_post_alto_nzeb_no(self):
        # Con q_post 120 (nessun miglioramento
        # dell'involucro) la quota FER e' 67,72 %
        # ma EP_nren_post sale a 55,55: NZEB NON
        # RAGGIUNTO.
        bc = mh893_calcola(**_demo_kwargs(q_post=120))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 10184.57,
                               places=2)
        self.assertAlmostEqual(bc["van"], -101459.21, places=2)
        self.assertEqual(bc["payback"], 25)
        self.assertAlmostEqual(bc["ep_nren_post"], 55.55, places=2)
        self.assertAlmostEqual(bc["quota_fer_pct"], 67.72, places=2)
        self.assertFalse(bc["nzeb_raggiunto"])

    def test_eta_caldaia_uno(self):
        # Con caldaia a rendimento 1 il gas pre
        # scende a 120000 kWh e il risparmio a
        # 15056,00, CO2 evitata 31,28 t/anno.
        bc = mh893_calcola(**_demo_kwargs(eta_caldaia=1.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 15056.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], -32801.57, places=2)
        self.assertEqual(bc["payback"], 17)
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], 31.28,
                               places=2)

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh893_calcola(**_demo_kwargs(
            capex_involucro=0, capex_pdc=0, capex_fv=0,
            capex_vent=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero(self):
        bc = mh893_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(bc["van"], 161400.00, places=2)
        self.assertEqual(bc["payback"], 16)

    def test_vendita_zero(self):
        bc = mh893_calcola(**_demo_kwargs(p_vendita=0.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 15200.00,
                               places=2)
        self.assertAlmostEqual(bc["van"], -30772.04, places=2)
        self.assertEqual(bc["payback"], 17)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def893\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh893_demo().keys()), lette - set(mh893_demo().keys()))
        self.assertEqual(lette, set(mh893_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc893\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc893\["([^"]+)"\]', src))
        attese = set(mh893_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 892 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 893.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 895)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab893:"), 1)
        self.assertTrue(src.startswith("    # W898"))

    def test_ui_tab893_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab893:"), 1)
        self.assertIn("def mh893_demo(", src_h)
        self.assertIn("def mh893_calcola(", src_h)
        self.assertIn("tab893", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("NZEB: l'edificio a energia quasi zero paga?", src)
        self.assertIn("🏠 NZEB: l'edificio a energia quasi zero paga?", src)
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
        chiavi = re.findall(r'key="(st893_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st893_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st893_calcola"', src)
        self.assertIn('key="st893_csv"', src)
        self.assertIn('key="st893_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg893"), src.index(".paiac("))
        self.assertLess(src.index("risparmio_eur_anno'] <= 0.0"), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)

    def test_ui_nessun_trattino_lungo(self):
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            self.assertNotIn(chr(8212), src)
            self.assertNotIn(chr(8211), src)

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato).
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
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)


if __name__ == "__main__":
    unittest.main()
