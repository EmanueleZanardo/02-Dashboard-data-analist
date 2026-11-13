"""Test nuova scheda teleriscaldamento a
biomassa: la caldaia a cippato di rete
batte le caldaie a gas dei singoli edifici?
Repo path: tests/test_w896_teleriscaldamento_biomassa.py

Business case annuo di una rete di
teleriscaldamento a biomassa per un
quartiere, guidato dal FABBISOGNO TERMICO
TOTALE Q_domanda (demo 3000 MWh/anno) e
dal NUMERO DI EDIFICI (demo 40, rete 1500
m): Q_prodotta = 3000 diviso (1 meno 0,08)
= 3260,87 MWh/anno; F_biomassa = 3260,87
diviso 0,88 = 3705,53 MWh/anno; costo
combustibile = 3705,53 per 1000 per 0,035
= 129693,68 EUR/anno; C_alt = 129693,68
piu 45000 = 174693,68 EUR/anno; F_gas =
3000 diviso 0,90 = 3333,33 MWh/anno;
C_base = 3333,33 per 1000 per 0,09 piu
15000 = 315000,00 EUR/anno; risparmio
140306,32 EUR/anno; CAPEX 350000 piu 1500
per 600 piu 40 per 8000 = 1570000 EUR
(somma verificata a mano); CO2 evitata =
(3333,33 per 1000 per 0,20 meno 3705,53
per 1000 per 0,015) diviso 1000 = 611,08
t/anno, fattore biomassa piccolo ma NON
zero (raccolta, cippatura e trasporto
emettono CO2); flussi [CAPEX negativo,
risparmio per vita]; VAN al tasso
(FRAZIONE in ingresso, 0,05 = 5 %, usato
diretto, NON diviso per 100); TIR per
bisezione su intervallo da meno 0,9 a 5,0;
payback (primo anno con cumulato maggiore
o uguale a 0). Tolleranza in PERCENTUALE
(10 = 10 % del CAPEX). I flussi piatti
sono una SEMPLIFICAZIONE DICHIARATA
(profilo reale variabile con clima e
prezzi, qui valore medio costante).
Verdetto: NON_CALCOLABILE se input
degenere (fabbisogno negativo, perdite
rete sotto 0 o uguali o sopra 1, eta
cippato nulla o negativa o sopra 1, prezzo
cippato negativo, O&M rete e caldaia
negativa, eta gas nulla o negativa o sopra
1, prezzo gas negativo, O&M caldaie gas
negativa, capex caldaia negativo,
lunghezza rete negativa, costo rete
negativo, n edifici nullo o negativo o non
intero, costo sottostazione negativo,
fattori CO2 negativi, tasso negativo, vita
nulla o negativa o non intera, tolleranza
negativa) o se risparmio minore o uguale
a 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti
CONVIENTE se VAN maggiore di 0, MARGINALE
se VAN negativa entro tolleranza
PERCENTUALE del CAPEX, NON_CONVIENTE
altrimenti.
Casi limite: perdite rete 1 non
calcolabili (divisione); eta cippato o eta
gas zero non calcolabili (divisione); vita
zero o non intera non calcolabile
(ValueError negli helper, guard
NON_CALCOLABILE in UI); n edifici zero non
calcolabile; fabbisogno zero (risparmio
meno 30000,00, NON_CALCOLABILE); prezzo
cippato 0,06 (risparmio positivo 47667,98
ma VAN negativa, NON_CONVIENTE, payback
None); CAPEX zero (TIR non definita,
payback 0); tasso zero (VAN uguale alla
somma dei flussi).
Distinzione esplicita: qui SOLO
teleriscaldamento a biomassa (caldaia
centrale a cippato piu rete interrata
verso caldaie a gas individuali), NIENTE
teleriscaldamento generico contro caldaia
(altra scheda), NIENTE biomassa legnosa
in CHP (altra scheda, li c'e' anche
elettricita'), NIENTE teleriscaldamento
con pompa di calore di rete, NIENTE
teleriscaldamento 5G, NIENTE accumulo
termico o sali fusi.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w896_helpers import (
        demo_calcoli,
        mh891_c_alt,
        mh891_c_base,
        mh891_calcola,
        mh891_capex_totale,
        mh891_co2_evitata,
        mh891_costo_combustibile,
        mh891_csv,
        mh891_demo,
        mh891_demo_calcoli,
        mh891_f_biomassa,
        mh891_f_gas,
        mh891_flussi,
        mh891_frazione,
        mh891_frazione_pos,
        mh891_frazione_sotto_uno,
        mh891_int_pos,
        mh891_nneg,
        mh891_num,
        mh891_payback,
        mh891_pos,
        mh891_q_prodotta,
        mh891_risparmio,
        mh891_sensibilita,
        mh891_tir,
        mh891_valida,
        mh891_van,
        mh891_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w896_helpers", os.path.join(_hf, "w896_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh891_c_alt = _mod.mh891_c_alt
    mh891_c_base = _mod.mh891_c_base
    mh891_calcola = _mod.mh891_calcola
    mh891_capex_totale = _mod.mh891_capex_totale
    mh891_co2_evitata = _mod.mh891_co2_evitata
    mh891_costo_combustibile = _mod.mh891_costo_combustibile
    mh891_csv = _mod.mh891_csv
    mh891_demo = _mod.mh891_demo
    mh891_demo_calcoli = _mod.mh891_demo_calcoli
    mh891_f_biomassa = _mod.mh891_f_biomassa
    mh891_f_gas = _mod.mh891_f_gas
    mh891_flussi = _mod.mh891_flussi
    mh891_frazione = _mod.mh891_frazione
    mh891_frazione_pos = _mod.mh891_frazione_pos
    mh891_frazione_sotto_uno = _mod.mh891_frazione_sotto_uno
    mh891_int_pos = _mod.mh891_int_pos
    mh891_nneg = _mod.mh891_nneg
    mh891_num = _mod.mh891_num
    mh891_payback = _mod.mh891_payback
    mh891_pos = _mod.mh891_pos
    mh891_q_prodotta = _mod.mh891_q_prodotta
    mh891_risparmio = _mod.mh891_risparmio
    mh891_sensibilita = _mod.mh891_sensibilita
    mh891_tir = _mod.mh891_tir
    mh891_valida = _mod.mh891_valida
    mh891_van = _mod.mh891_van
    mh891_verdetto = _mod.mh891_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w896_helpers.py")
_UI_PATH = _risolvi("w896_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "0"
_VECCHIO_TAB = "tab89" + "0"
_VECCHIO_ST = "st89" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "vita_anni": 20,
    "q_prodotta_mwh_anno": 3260.869565217391,
    "f_biomassa_mwh_anno": 3705.5335968379445,
    "costo_combustibile_eur_anno": 129693.67588932806,
    "f_gas_mwh_anno": 3333.333333333333,
    "c_base_eur_anno": 314999.99999999994,
    "c_alt_eur_anno": 174693.67588932806,
    "risparmio_eur_anno": 140306.32411067188,
    "capex_eur": 1570000.0,
    "co2_evitata_t_anno": 611.0836627140974,
    "van": 178526.92345578168,
    "tir": 6.306607725757088,
    "payback": 12,
}


def _demo_kwargs(**over):
    kw = dict(mh891_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh891_num(3, "x"), 3.0)
        self.assertEqual(mh891_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh891_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh891_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh891_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh891_pos(0, "x")
        with self.assertRaises(ValueError):
            mh891_pos(-1, "x")
        self.assertEqual(mh891_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh891_int_pos(40, "x"), 40)
        self.assertEqual(mh891_int_pos(40.0, "x"), 40)
        with self.assertRaises(ValueError):
            mh891_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh891_int_pos(40.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh891_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh891_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh891_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh891_frazione(1.1, "x")

    def test_frazione_pos_intervallo(self):
        self.assertEqual(mh891_frazione_pos(0.88, "x"), 0.88)
        self.assertEqual(mh891_frazione_pos(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh891_frazione_pos(0.0, "x")
        with self.assertRaises(ValueError):
            mh891_frazione_pos(-0.1, "x")
        with self.assertRaises(ValueError):
            mh891_frazione_pos(1.1, "x")

    def test_frazione_sotto_uno_intervallo(self):
        self.assertEqual(mh891_frazione_sotto_uno(0.0, "x"), 0.0)
        self.assertEqual(mh891_frazione_sotto_uno(0.08, "x"), 0.08)
        with self.assertRaises(ValueError):
            mh891_frazione_sotto_uno(1.0, "x")
        with self.assertRaises(ValueError):
            mh891_frazione_sotto_uno(-0.1, "x")
        with self.assertRaises(ValueError):
            mh891_frazione_sotto_uno(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_q_prodotta_e_f_biomassa(self):
        self.assertAlmostEqual(mh891_q_prodotta(3000, 0.08),
                               3260.87, places=2)
        self.assertAlmostEqual(mh891_f_biomassa(3260.869565217391, 0.88),
                               3705.53, places=2)
        # Senza perdite di rete il calore prodotto
        # coincide col fabbisogno.
        self.assertEqual(mh891_q_prodotta(3000, 0), 3000.0)
        with self.assertRaises(ValueError):
            mh891_q_prodotta(3000, 1.0)
        with self.assertRaises(ValueError):
            mh891_f_biomassa(3260.87, 0)

    def test_eta_uno_combustibile_uguale_calore(self):
        # Con rendimento 1 il combustibile coincide
        # col calore prodotto.
        self.assertEqual(mh891_f_biomassa(3260.87, 1.0), 3260.87)

    def test_costo_combustibile_e_costi(self):
        self.assertAlmostEqual(
            mh891_costo_combustibile(3705.5335968379445, 0.035),
            129693.68, places=2)
        self.assertAlmostEqual(
            mh891_c_alt(129693.67588932806, 45000),
            174693.68, places=2)
        self.assertAlmostEqual(
            mh891_f_gas(3000, 0.90), 3333.33, places=2)
        self.assertAlmostEqual(
            mh891_c_base(3333.333333333333, 0.09, 15000),
            315000.00, places=2)
        self.assertAlmostEqual(
            mh891_risparmio(315000.0, 174693.67588932806),
            140306.32, places=2)

    def test_capex_totale_voci(self):
        self.assertEqual(mh891_capex_totale(350000, 1500, 600, 40, 8000),
                         1570000.0)
        self.assertEqual(mh891_capex_totale(350000, 0, 600, 40, 8000),
                         670000.0)
        self.assertEqual(mh891_capex_totale(350000, 1500, 600, 1, 8000),
                         1258000.0)
        with self.assertRaises(ValueError):
            mh891_capex_totale(350000, 1500, 600, 0, 8000)

    def test_co2_gas_spiazzato_meno_biomassa(self):
        co2 = mh891_co2_evitata(3333.333333333333, 0.20,
                                3705.5335968379445, 0.015)
        self.assertAlmostEqual(co2, 611.08, places=2)
        # Con fattori zero la CO2 evitata e zero.
        self.assertEqual(mh891_co2_evitata(3333.33, 0.0,
                                           3705.53, 0.0), 0.0)
        # Solo gas spiazzato, senza biomassa:
        # 666,67 t/anno.
        self.assertAlmostEqual(
            mh891_co2_evitata(3333.333333333333, 0.20, 0.0, 0.015),
            666.67, places=2)
        # Il fattore biomassa NON e zero: con lo
        # stesso fattore del gas la CO2 evitata
        # crolla perche' la biomassa brucia piu'
        # MWh del gas che spiazza.
        self.assertAlmostEqual(
            mh891_co2_evitata(3333.333333333333, 0.20,
                              3705.5335968379445, 0.20),
            -74.44, places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh891_flussi(1570000, 140306.32, 3),
                         [-1570000, 140306.32, 140306.32, 140306.32])

    def test_van_tasso_zero_e_cinque(self):
        self.assertAlmostEqual(mh891_van([-100, 60, 60], 0), 20.0)
        bc = mh891_demo_calcoli()
        self.assertAlmostEqual(mh891_van(bc["flussi"], 0.05), bc["van"])

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 178526,92; con 5,0 (cioe' 500 % se
        # letto come frazione) sarebbe tutt'altra.
        bc = mh891_demo_calcoli()
        self.assertAlmostEqual(mh891_van(bc["flussi"], 0.05),
                               178526.92, places=2)
        self.assertNotAlmostEqual(mh891_van(bc["flussi"], 5.0),
                                  178526.92, places=2)

    def test_tir_demo(self):
        bc = mh891_demo_calcoli()
        tir = mh891_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh891_tir([-100, -10, -10]))
        self.assertIsNone(mh891_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh891_demo_calcoli()
        self.assertEqual(mh891_payback(bc["flussi"]), 12)
        self.assertIsNone(mh891_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh891_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh891_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:12]), -26630.43, places=2)
        self.assertAlmostEqual(sum(flussi[:13]), 113675.89, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh891_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh891_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh891_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh891_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh891_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh891_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh891_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh891_demo()
        val = mh891_valida(*[demo[k] for k in (
            "q_domanda", "p_rete", "eta_cippato", "p_cippato",
            "om_alt", "eta_gas", "p_gas", "om_base",
            "capex_caldaia", "lunghezza_rete_m",
            "costo_rete_eur_m", "n_edifici",
            "costo_sottostazione", "f_gas", "f_biomassa",
            "tasso", "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)
        kw = _demo_kwargs(vita_anni=20.5)
        self.assertRaises(ValueError, mh891_calcola, **kw)
        kw = _demo_kwargs(vita_anni=15)
        bc = mh891_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 15)

    def test_valida_perdite_uno_e_eta_zero_no(self):
        kw = _demo_kwargs(p_rete=1.0)
        self.assertRaises(ValueError, mh891_calcola, **kw)
        kw = _demo_kwargs(eta_cippato=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)
        kw = _demo_kwargs(eta_gas=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)

    def test_valida_n_edifici_zero_no(self):
        kw = _demo_kwargs(n_edifici=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)

    def test_valida_frazioni_sopra_uno_no(self):
        for campo, valore in (("p_rete", 1.0),
                              ("eta_cippato", 1.1),
                              ("eta_gas", 1.1)):
            with self.assertRaises(ValueError):
                mh891_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh891_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("q_domanda", -1),
                              ("p_cippato", -0.01),
                              ("om_alt", -1),
                              ("p_gas", -0.01),
                              ("om_base", -1),
                              ("capex_caldaia", -1),
                              ("lunghezza_rete_m", -1),
                              ("costo_rete_eur_m", -1),
                              ("costo_sottostazione", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("f_gas", -0.01),
                              ("f_biomassa", -0.01)):
            with self.assertRaises(ValueError):
                mh891_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh891_calcola(mh891_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh891_calcola(dict(mh891_demo(), capex_caldaia=99999),
                           capex_caldaia=350000)
        self.assertEqual(bc["capex_eur"], 1570000.0)


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

    def test_demo_verdetto_convente(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 12)

    def test_coerenza_costi_e_co2(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["costo_combustibile_eur_anno"] + bc["om_alt"])
        self.assertAlmostEqual(
            bc["c_base_eur_anno"],
            bc["f_gas_mwh_anno"] * 1000.0 * bc["p_gas"]
            + bc["om_base"])
        self.assertAlmostEqual(
            bc["costo_combustibile_eur_anno"],
            bc["f_biomassa_mwh_anno"] * 1000.0 * bc["p_cippato"])
        self.assertAlmostEqual(
            bc["f_biomassa_mwh_anno"],
            bc["q_prodotta_mwh_anno"] / bc["eta_cippato"])
        self.assertAlmostEqual(
            bc["q_prodotta_mwh_anno"],
            bc["q_domanda"] / (1.0 - bc["p_rete"]))
        self.assertAlmostEqual(
            bc["f_gas_mwh_anno"],
            bc["q_domanda"] / bc["eta_gas"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            (bc["f_gas_mwh_anno"] * 1000.0 * bc["f_gas"]
             - bc["f_biomassa_mwh_anno"] * 1000.0
             * bc["f_biomassa"]) / 1000.0)
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["capex_caldaia"]
            + bc["lunghezza_rete_m"] * bc["costo_rete_eur_m"]
            + bc["n_edifici"] * bc["costo_sottostazione"])

    def test_sensibilita_valori(self):
        s = mh891_sensibilita(**mh891_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               200306.32, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               926259.54, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 8)
        self.assertAlmostEqual(s["p_cippato_piu20"]["risparmio_eur_anno"],
                               114367.59, places=2)
        self.assertAlmostEqual(s["p_cippato_piu20"]["van"],
                               -144727.05, places=2)
        self.assertEqual(s["p_cippato_piu20"]["payback"], 14)
        # VAN negativa ma entro la tolleranza del
        # 10 % del CAPEX (157000): MARGINALE, non
        # NON_CONVIENTE.
        self.assertEqual(s["p_cippato_piu20"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["senza_perdite"]["risparmio_eur_anno"],
                               150681.82, places=2)
        self.assertAlmostEqual(s["senza_perdite"]["van"],
                               307828.51, places=2)
        self.assertEqual(s["senza_perdite"]["payback"], 11)
        self.assertAlmostEqual(s["eta_cippato_080"]["risparmio_eur_anno"],
                               127336.96, places=2)
        self.assertAlmostEqual(s["eta_cippato_080"]["van"],
                               16899.94, places=2)
        self.assertEqual(s["eta_cippato_080"]["payback"], 13)
        self.assertEqual(s["eta_cippato_080"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -1391473.08, places=2)
        self.assertIsNone(s["capex_doppio"]["payback"])
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["capex_eur"], 3140000.0)
        self.assertAlmostEqual(s["vita_15"]["risparmio_eur_anno"],
                               140306.32, places=2)
        self.assertAlmostEqual(s["vita_15"]["van"],
                               -113668.34, places=2)
        self.assertEqual(s["vita_15"]["payback"], 12)
        self.assertEqual(s["vita_15"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["tasso_0"]["van"],
                               1236126.48, places=2)

    def test_marginale_con_capex_caldaia_alto(self):
        # CAPEX totale 1820000 (caldaia a 600000):
        # VAN circa meno 71473,08, entro la
        # tolleranza del 10 % (182000).
        bc = mh891_calcola(**_demo_kwargs(capex_caldaia=600000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -71473.08, places=2)
        self.assertEqual(bc["payback"], 13)

    def test_non_convente_con_capex_caldaia_altissimo(self):
        bc = mh891_calcola(**_demo_kwargs(capex_caldaia=2000000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -1471473.08, places=2)
        self.assertIsNone(bc["payback"])

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh891_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -14693.68,
                               places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh891_csv(bc, mh891_demo())
        for voce in ("q_domanda", "p_rete",
                     "eta_cippato", "p_cippato", "om_alt",
                     "eta_gas", "p_gas", "om_base",
                     "capex_caldaia", "lunghezza_rete_m",
                     "costo_rete_eur_m", "n_edifici",
                     "costo_sottostazione", "f_gas",
                     "f_biomassa", "q_prodotta_mwh_anno",
                     "f_biomassa_mwh_anno",
                     "costo_combustibile_eur_anno",
                     "f_gas_mwh_anno",
                     "risparmio_eur_anno", "verdetto",
                     "co2_evitata_t_anno"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -1570000.0)
        self.assertEqual(len(bc["df_tabella"]), 30)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Fabbisogno termico edifici (MWh/anno)", voci)
        self.assertIn("Calore prodotto (MWh/anno)", voci)
        self.assertIn("Combustibile biomassa (MWh/anno)", voci)
        self.assertIn("CAPEX caldaia (EUR)", voci)

    def test_c_alt_piu_caro_con_cippato_caro(self):
        senza = mh891_c_alt(129693.68, 45000)
        con = mh891_c_alt(200000.0, 45000)
        self.assertAlmostEqual(con - senza, 70306.32, places=2)

    def test_sensibilita_chiavi_complete(self):
        s = mh891_sensibilita(**mh891_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_cippato_piu20",
                          "senza_perdite", "eta_cippato_080",
                          "capex_doppio", "vita_15", "tasso_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh891_csv(bc, mh891_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("q_prodotta_mwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh891_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh891_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh891_calcola(**_demo_kwargs(p_rete=0))
        self.assertEqual(bc["q_prodotta_mwh_anno"], 3000.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 150681.82,
                               places=2)
        bc = mh891_calcola(**_demo_kwargs(f_biomassa=0))
        self.assertEqual(bc["co2_evitata_t_anno"], 666.6666666666666)


class TestCasiLimite(unittest.TestCase):
    def test_vita_zero_non_calcolabile(self):
        # Vita zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)
        self.assertFalse(mh891_valida(*[kw[k] for k in (
            "q_domanda", "p_rete", "eta_cippato", "p_cippato",
            "om_alt", "eta_gas", "p_gas", "om_base",
            "capex_caldaia", "lunghezza_rete_m",
            "costo_rete_eur_m", "n_edifici",
            "costo_sottostazione", "f_gas", "f_biomassa",
            "tasso", "vita_anni", "tolleranza_pct")])["valido"])

    def test_vita_non_intera_non_calcolabile(self):
        kw = _demo_kwargs(vita_anni=20.5)
        self.assertRaises(ValueError, mh891_calcola, **kw)

    def test_fabbisogno_zero(self):
        # Fabbisogno zero: costo base 15000 (sola
        # O&M caldaie gas) e costo alternativo
        # 45000 (sola O&M rete e caldaia):
        # risparmio meno 30000,00, verdetto
        # NON_CALCOLABILE.
        bc = mh891_calcola(**_demo_kwargs(q_domanda=0))
        self.assertEqual(bc["q_prodotta_mwh_anno"], 0.0)
        self.assertEqual(bc["f_biomassa_mwh_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -30000.00,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_cippato_alto_risparmio_positivo_ma_van_negativa(self):
        # A prezzo cippato 0,06 il risparmio resta
        # positivo (47667,98) ma la VAN e negativa
        # oltre la tolleranza: NON_CONVIENTE, non
        # NON_CALCOLABILE.
        bc = mh891_calcola(**_demo_kwargs(p_cippato=0.06))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 47667.98,
                               places=2)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(bc["payback"])

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh891_calcola(**_demo_kwargs(capex_caldaia=0,
                                          costo_rete_eur_m=0,
                                          costo_sottostazione=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero(self):
        bc = mh891_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(bc["van"], 1236126.48, places=2)
        self.assertEqual(bc["payback"], 12)

    def test_perdite_uno_non_calcolabile(self):
        kw = _demo_kwargs(p_rete=1.0)
        self.assertRaises(ValueError, mh891_calcola, **kw)

    def test_eta_zero_non_calcolabile(self):
        kw = _demo_kwargs(eta_cippato=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)
        kw = _demo_kwargs(eta_gas=0)
        self.assertRaises(ValueError, mh891_calcola, **kw)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def891\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh891_demo().keys()), lette - set(mh891_demo().keys()))
        self.assertEqual(lette, set(mh891_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc891\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc891\["([^"]+)"\]', src))
        attese = set(mh891_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 890 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 891.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 896)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab891:"), 1)
        self.assertTrue(src.startswith("    # W896"))

    def test_ui_tab891_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab891:"), 1)
        self.assertIn("def mh891_demo(", src_h)
        self.assertIn("def mh891_calcola(", src_h)
        self.assertIn("tab891", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Teleriscaldamento a biomassa: la caldaia a cippato di rete batte le caldaie a gas dei singoli edifici?", src)
        self.assertIn("🔥🌲 Teleriscaldamento a biomassa: la caldaia a cippato di rete batte le caldaie a gas dei singoli edifici?", src)
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
        chiavi = re.findall(r'key="(st891_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st891_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st891_calcola"', src)
        self.assertIn('key="st891_csv"', src)
        self.assertIn('key="st891_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg891"), src.index(".paiac("))
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
