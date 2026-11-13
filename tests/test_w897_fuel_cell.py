"""Test nuova scheda cogenerazione a fuel
cell: l'elettricita' piu calore senza
combustione paga?
Repo path: tests/test_w897_fuel_cell.py

Business case annuo di una cogenerazione
stazionaria a fuel cell SOFC a gas
naturale, guidato dalla POTENZA ELETTRICA
P_el (demo 100 kWe) e dalle ORE ANNUE h
(demo 8000 h/anno): E_el = 100 per 8000
= 800000 kWh/anno; F = 800000 diviso
0,55 = 1454545,45 kWh PCI/anno; Q_th =
1454545,45 per 0,35 = 509090,91
kWh_t/anno; Q_val = 509090,91 per 0,80
= 407272,73 kWh/anno; C_base = 800000
per 0,22 piu 407272,73 diviso 0,90 per
0,08 = 212202,02 EUR/anno; C_fc =
1454545,45 per 0,08 piu 800000 per 0,03
= 140363,64 EUR/anno; risparmio
71838,38 EUR/anno; CAPEX 100 per 4500
= 450000 EUR (somma verificata a mano);
CO2 evitata = (800000 per 0,35 piu
407272,73 diviso 0,90 per 0,20 meno
1454545,45 per 0,20) diviso 1000 = 79,60
t/anno, la cella NON e' a emissioni zero
(il gas in ingresso emette CO2 e va
sottratto); flussi [CAPEX negativo,
risparmio per vita]; VAN al tasso
(FRAZIONE in ingresso, 0,05 = 5 %, usato
diretto, NON diviso per 100); TIR per
bisezione su intervallo da meno 0,9 a 5,0;
payback (primo anno con cumulato maggiore
o uguale a 0). Tolleranza in PERCENTUALE
(10 = 10 % del CAPEX). I flussi piatti
sono una SEMPLIFICAZIONE DICHIARATA
(profilo reale variabile con carico e
prezzi, qui valore medio costante; lo
stack si degrada e va sostituito, qui il
costo e' dentro O&M come quota annua
media).
Verdetto: NON_CALCOLABILE se input
degenere (potenza negativa, ore negative,
eta elettrica nulla o negativa o sopra 1,
eta termica nulla o negativa o sopra 1,
quota valorizzata sotto 0 o sopra 1, eta
caldaia nulla o negativa o sopra 1,
prezzo gas negativo, prezzo elettricita'
negativo, O&M negativa, CAPEX specifico
negativo, fattori CO2 negativi, tasso
negativo, vita nulla o negativa o non
intera, tolleranza negativa) o se
risparmio minore o uguale a 0 (guard
degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN
maggiore di 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: eta elettrica o eta termica
o eta caldaia zero non calcolabili
(divisione); vita zero o non intera non
calcolabile (ValueError negli helper,
guard NON_CALCOLABILE in UI); ore zero
(risparmio zero, NON_CALCOLABILE);
potenza zero (risparmio zero,
NON_CALCOLABILE); quota calore zero
(risparmio positivo 35636,36 ma CO2
evitata negativa meno 10,91: senza calore
valorizzato la cella emette piu CO2 di
quanta ne spiazzi); O&M 0,12
(risparmio negativo meno 161,62,
NON_CALCOLABILE); CAPEX zero (TIR non
definita, payback 0); tasso zero (VAN
uguale alla somma dei flussi).
Distinzione esplicita: qui SOLO
cogenerazione stazionaria a fuel cell
SOFC a gas naturale (conversione
elettrochimica senza combustione, solo
elettricita' piu calore), NIENTE
cogenerazione CHP a gas (tab189, li
combustione in motore o turbina),
NIENTE trigenerazione CCHP (tab653, li
anche freddo da assorbitore), NIENTE
cogenerazione CAR (tab727, li certificati
e risparmio di energia primaria), NIENTE
biogas CHP da depuratore (tab815, li
substrato biogas da depurazione), NIENTE
camion o treno a idrogeno fuel cell
(tab726 e tab750, li trazione veicolare),
NIENTE elettrolizzatori (tab729, li
produzione di idrogeno: qui consumo di
gas per elettricita' piu calore).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w897_helpers import (
        demo_calcoli,
        mh892_c_base,
        mh892_c_fc,
        mh892_calcola,
        mh892_capex,
        mh892_co2_evitata,
        mh892_csv,
        mh892_demo,
        mh892_demo_calcoli,
        mh892_e_el,
        mh892_f_combustibile,
        mh892_flussi,
        mh892_frazione,
        mh892_frazione_pos,
        mh892_int_pos,
        mh892_nneg,
        mh892_num,
        mh892_payback,
        mh892_pos,
        mh892_q_th,
        mh892_q_val,
        mh892_risparmio,
        mh892_sensibilita,
        mh892_tir,
        mh892_valida,
        mh892_van,
        mh892_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w897_helpers", os.path.join(_hf, "w897_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh892_c_base = _mod.mh892_c_base
    mh892_c_fc = _mod.mh892_c_fc
    mh892_calcola = _mod.mh892_calcola
    mh892_capex = _mod.mh892_capex
    mh892_co2_evitata = _mod.mh892_co2_evitata
    mh892_csv = _mod.mh892_csv
    mh892_demo = _mod.mh892_demo
    mh892_demo_calcoli = _mod.mh892_demo_calcoli
    mh892_e_el = _mod.mh892_e_el
    mh892_f_combustibile = _mod.mh892_f_combustibile
    mh892_flussi = _mod.mh892_flussi
    mh892_frazione = _mod.mh892_frazione
    mh892_frazione_pos = _mod.mh892_frazione_pos
    mh892_int_pos = _mod.mh892_int_pos
    mh892_nneg = _mod.mh892_nneg
    mh892_num = _mod.mh892_num
    mh892_payback = _mod.mh892_payback
    mh892_pos = _mod.mh892_pos
    mh892_q_th = _mod.mh892_q_th
    mh892_q_val = _mod.mh892_q_val
    mh892_risparmio = _mod.mh892_risparmio
    mh892_sensibilita = _mod.mh892_sensibilita
    mh892_tir = _mod.mh892_tir
    mh892_valida = _mod.mh892_valida
    mh892_van = _mod.mh892_van
    mh892_verdetto = _mod.mh892_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w897_helpers.py")
_UI_PATH = _risolvi("w897_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "1"
_VECCHIO_TAB = "tab89" + "1"
_VECCHIO_ST = "st89" + "1_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "vita_anni": 15,
    "e_el_kwh_anno": 800000.0,
    "f_kwh_pci_anno": 1454545.4545454544,
    "q_th_kwh_anno": 509090.909090909,
    "q_val_kwh_anno": 407272.72727272724,
    "c_base_eur_anno": 212202.02020202018,
    "c_fc_eur_anno": 140363.63636363635,
    "risparmio_eur_anno": 71838.38383838383,
    "capex_eur": 450000.0,
    "co2_evitata_t_anno": 79.59595959595963,
    "van": 295657.85825798335,
    "tir": 13.609422233977863,
    "payback": 7,
}


def _demo_kwargs(**over):
    kw = dict(mh892_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh892_num(3, "x"), 3.0)
        self.assertEqual(mh892_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh892_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh892_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh892_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh892_pos(0, "x")
        with self.assertRaises(ValueError):
            mh892_pos(-1, "x")
        self.assertEqual(mh892_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh892_int_pos(15, "x"), 15)
        self.assertEqual(mh892_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh892_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh892_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh892_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh892_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh892_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh892_frazione(1.1, "x")

    def test_frazione_pos_intervallo(self):
        self.assertEqual(mh892_frazione_pos(0.55, "x"), 0.55)
        self.assertEqual(mh892_frazione_pos(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh892_frazione_pos(0.0, "x")
        with self.assertRaises(ValueError):
            mh892_frazione_pos(-0.1, "x")
        with self.assertRaises(ValueError):
            mh892_frazione_pos(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_e_el_e_f_combustibile(self):
        self.assertEqual(mh892_e_el(100, 8000), 800000)
        self.assertAlmostEqual(mh892_f_combustibile(800000, 0.55),
                               1454545.45, places=2)
        # Con eta elettrica 1 il gas in ingresso
        # coincide con l'energia elettrica.
        self.assertEqual(mh892_f_combustibile(800000, 1.0), 800000.0)
        with self.assertRaises(ValueError):
            mh892_f_combustibile(800000, 0)

    def test_q_th_e_q_val(self):
        self.assertAlmostEqual(
            mh892_q_th(1454545.4545454544, 0.35), 509090.91, places=2)
        self.assertAlmostEqual(
            mh892_q_val(509090.909090909, 0.80), 407272.73, places=2)
        # Con quota 1 tutto il calore prodotto
        # viene valorizzato.
        self.assertEqual(mh892_q_val(509090.91, 1.0), 509090.91)
        # Con quota 0 niente calore valorizzato.
        self.assertEqual(mh892_q_val(509090.91, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh892_q_th(1454545.45, 0)
        with self.assertRaises(ValueError):
            mh892_q_val(509090.91, 1.1)

    def test_costi_base_e_fuel_cell(self):
        self.assertAlmostEqual(
            mh892_c_base(800000, 407272.72727272724, 0.90, 0.22, 0.08),
            212202.02, places=2)
        self.assertAlmostEqual(
            mh892_c_fc(1454545.4545454544, 0.08, 800000, 0.03),
            140363.64, places=2)
        self.assertAlmostEqual(
            mh892_risparmio(212202.02020202018, 140363.63636363635),
            71838.38, places=2)
        # Con caldaia a rendimento 1 il gas per il
        # calore valorizzato e Q_val per p_gas.
        self.assertAlmostEqual(
            mh892_c_base(800000, 407272.73, 1.0, 0.22, 0.08),
            208581.82, places=2)

    def test_capex_potenza_per_specifico(self):
        self.assertEqual(mh892_capex(100, 4500), 450000.0)
        self.assertEqual(mh892_capex(0, 4500), 0.0)
        self.assertEqual(mh892_capex(100, 0), 0.0)
        with self.assertRaises(ValueError):
            mh892_capex(-1, 4500)

    def test_co2_elettricita_piu_calore_meno_gas(self):
        co2 = mh892_co2_evitata(800000, 0.35, 407272.72727272724,
                                0.90, 0.20, 1454545.4545454544)
        self.assertAlmostEqual(co2, 79.60, places=2)
        # Con fattori zero la CO2 evitata e zero.
        self.assertEqual(mh892_co2_evitata(800000, 0.0, 407272.73,
                                           0.90, 0.0, 1454545.45), 0.0)
        # Solo elettricita' spiazzata, senza calore
        # e senza gas in ingresso: 280 t/anno.
        self.assertAlmostEqual(
            mh892_co2_evitata(800000, 0.35, 0.0, 0.90, 0.20, 0.0),
            280.0, places=2)
        # La cella NON e' a emissioni zero: con
        # fattore gas uguale a quello elettrico e
        # senza calore valorizzato la CO2 evitata
        # e negativa perche' il gas in ingresso
        # supera l'elettricita' prodotta.
        self.assertAlmostEqual(
            mh892_co2_evitata(800000, 0.20, 0.0, 0.90, 0.20,
                              1454545.4545454544),
            -130.91, places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh892_flussi(450000, 71838.38, 3),
                         [-450000, 71838.38, 71838.38, 71838.38])

    def test_van_tasso_zero_e_cinque(self):
        self.assertAlmostEqual(mh892_van([-100, 60, 60], 0), 20.0)
        bc = mh892_demo_calcoli()
        self.assertAlmostEqual(mh892_van(bc["flussi"], 0.05), bc["van"])

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 295657,86; con 5,0 (cioe' 500 % se
        # letto come frazione) sarebbe tutt'altra.
        bc = mh892_demo_calcoli()
        self.assertAlmostEqual(mh892_van(bc["flussi"], 0.05),
                               295657.86, places=2)
        self.assertNotAlmostEqual(mh892_van(bc["flussi"], 5.0),
                                  295657.86, places=2)

    def test_tir_demo(self):
        bc = mh892_demo_calcoli()
        tir = mh892_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh892_tir([-100, -10, -10]))
        self.assertIsNone(mh892_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh892_demo_calcoli()
        self.assertEqual(mh892_payback(bc["flussi"]), 7)
        self.assertIsNone(mh892_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh892_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh892_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:7]), -18969.70, places=2)
        self.assertAlmostEqual(sum(flussi[:8]), 52868.69, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh892_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh892_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh892_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh892_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh892_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh892_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh892_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh892_demo()
        val = mh892_valida(*[demo[k] for k in (
            "p_el_kw", "ore_anno", "eta_el", "eta_th",
            "quota_valorizzata", "eta_caldaia", "p_gas", "p_el",
            "om_eur_kwh", "capex_specifico", "f_gas", "f_el",
            "tasso", "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        kw = _demo_kwargs(vita_anni=15.5)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10)
        bc = mh892_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_eta_zero_no(self):
        kw = _demo_kwargs(eta_el=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        kw = _demo_kwargs(eta_th=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        kw = _demo_kwargs(eta_caldaia=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)

    def test_valida_quota_sopra_uno_no(self):
        kw = _demo_kwargs(quota_valorizzata=1.1)
        self.assertRaises(ValueError, mh892_calcola, **kw)

    def test_valida_frazioni_sopra_uno_no(self):
        for campo, valore in (("eta_el", 1.1),
                              ("eta_th", 1.1),
                              ("eta_caldaia", 1.1)):
            with self.assertRaises(ValueError):
                mh892_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh892_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("p_el_kw", -1),
                              ("ore_anno", -1),
                              ("p_gas", -0.01),
                              ("p_el", -0.01),
                              ("om_eur_kwh", -0.01),
                              ("capex_specifico", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("f_gas", -0.01),
                              ("f_el", -0.01)):
            with self.assertRaises(ValueError):
                mh892_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh892_calcola(mh892_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh892_calcola(dict(mh892_demo(), capex_specifico=9999),
                           capex_specifico=4500)
        self.assertEqual(bc["capex_eur"], 450000.0)


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
        self.assertEqual(bc["payback"], 7)

    def test_coerenza_costi_e_co2(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_fc_eur_anno"])
        self.assertAlmostEqual(
            bc["c_base_eur_anno"],
            bc["e_el_kwh_anno"] * bc["p_el"]
            + bc["q_val_kwh_anno"] / bc["eta_caldaia"] * bc["p_gas"])
        self.assertAlmostEqual(
            bc["c_fc_eur_anno"],
            bc["f_kwh_pci_anno"] * bc["p_gas"]
            + bc["e_el_kwh_anno"] * bc["om_eur_kwh"])
        self.assertAlmostEqual(
            bc["e_el_kwh_anno"],
            bc["p_el_kw"] * bc["ore_anno"])
        self.assertAlmostEqual(
            bc["f_kwh_pci_anno"],
            bc["e_el_kwh_anno"] / bc["eta_el"])
        self.assertAlmostEqual(
            bc["q_th_kwh_anno"],
            bc["f_kwh_pci_anno"] * bc["eta_th"])
        self.assertAlmostEqual(
            bc["q_val_kwh_anno"],
            bc["q_th_kwh_anno"] * bc["quota_valorizzata"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            (bc["e_el_kwh_anno"] * bc["f_el"]
             + bc["q_val_kwh_anno"] / bc["eta_caldaia"] * bc["f_gas"]
             - bc["f_kwh_pci_anno"] * bc["f_gas"]) / 1000.0)
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["p_el_kw"] * bc["capex_specifico"])

    def test_sensibilita_valori(self):
        s = mh892_sensibilita(**mh892_demo())
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               107038.38, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               661021.82, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               55806.06, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               129247.83, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 9)
        self.assertAlmostEqual(s["quota_100"]["risparmio_eur_anno"],
                               80888.89, places=2)
        self.assertAlmostEqual(s["quota_100"]["van"],
                               389599.01, places=2)
        self.assertEqual(s["quota_100"]["payback"], 6)
        self.assertAlmostEqual(s["quota_100"]["co2_evitata_t_anno"],
                               102.22, places=2)
        self.assertAlmostEqual(s["eta_el_060"]["risparmio_eur_anno"],
                               78518.52, places=2)
        self.assertAlmostEqual(s["eta_el_060"]["van"],
                               364995.37, places=2)
        self.assertEqual(s["eta_el_060"]["payback"], 6)
        self.assertAlmostEqual(s["eta_el_060"]["co2_evitata_t_anno"],
                               96.30, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -154342.14, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 13)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["capex_eur"], 900000.0)
        self.assertAlmostEqual(s["vita_10"]["risparmio_eur_anno"],
                               71838.38, places=2)
        self.assertAlmostEqual(s["vita_10"]["van"],
                               104716.96, places=2)
        self.assertEqual(s["vita_10"]["payback"], 7)
        self.assertAlmostEqual(s["tasso_0"]["van"],
                               627575.76, places=2)

    def test_marginale_con_capex_specifico_alto(self):
        # CAPEX totale 800000 (specifico a 8000):
        # VAN circa meno 54342,14, entro la
        # tolleranza del 10 % (80000).
        bc = mh892_calcola(**_demo_kwargs(capex_specifico=8000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -54342.14, places=2)
        self.assertEqual(bc["payback"], 12)

    def test_non_convente_con_capex_specifico_altissimo(self):
        bc = mh892_calcola(**_demo_kwargs(capex_specifico=9000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -154342.14, places=2)
        self.assertEqual(bc["payback"], 13)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh892_calcola(**_demo_kwargs(om_eur_kwh=0.12))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -161.62,
                               places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh892_csv(bc, mh892_demo())
        for voce in ("p_el_kw", "ore_anno",
                     "eta_el", "eta_th", "quota_valorizzata",
                     "eta_caldaia", "p_gas", "p_el",
                     "om_eur_kwh", "capex_specifico",
                     "f_gas", "f_el",
                     "e_el_kwh_anno", "f_kwh_pci_anno",
                     "q_th_kwh_anno", "q_val_kwh_anno",
                     "c_base_eur_anno", "c_fc_eur_anno",
                     "risparmio_eur_anno", "verdetto",
                     "co2_evitata_t_anno"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -450000.0)
        self.assertEqual(len(bc["df_tabella"]), 28)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Potenza elettrica (kW)", voci)
        self.assertIn("Energia elettrica (kWh/anno)", voci)
        self.assertIn("Gas in ingresso (kWh PCI/anno)", voci)
        self.assertIn("Calore valorizzato (kWh/anno)", voci)
        self.assertIn("Costo fuel cell (EUR/anno)", voci)

    def test_c_fc_piu_caro_con_om_alto(self):
        senza = mh892_c_fc(1454545.45, 0.08, 800000, 0.03)
        con = mh892_c_fc(1454545.45, 0.08, 800000, 0.06)
        self.assertAlmostEqual(con - senza, 24000.0, places=2)

    def test_sensibilita_chiavi_complete(self):
        s = mh892_sensibilita(**mh892_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_piu20", "p_gas_piu20",
                          "quota_100", "eta_el_060",
                          "capex_doppio", "vita_10", "tasso_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh892_csv(bc, mh892_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_el_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh892_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh892_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh892_calcola(**_demo_kwargs(quota_valorizzata=0))
        self.assertEqual(bc["q_val_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 35636.36,
                               places=2)
        bc = mh892_calcola(**_demo_kwargs(f_el=0))
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], -200.40,
                               places=2)


class TestCasiLimite(unittest.TestCase):
    def test_vita_zero_non_calcolabile(self):
        # Vita zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        self.assertFalse(mh892_valida(*[kw[k] for k in (
            "p_el_kw", "ore_anno", "eta_el", "eta_th",
            "quota_valorizzata", "eta_caldaia", "p_gas", "p_el",
            "om_eur_kwh", "capex_specifico", "f_gas", "f_el",
            "tasso", "vita_anni", "tolleranza_pct")])["valido"])

    def test_vita_non_intera_non_calcolabile(self):
        kw = _demo_kwargs(vita_anni=15.5)
        self.assertRaises(ValueError, mh892_calcola, **kw)

    def test_ore_zero(self):
        # Ore zero: energia elettrica zero, gas
        # zero, costi zero, risparmio zero,
        # verdetto NON_CALCOLABILE.
        bc = mh892_calcola(**_demo_kwargs(ore_anno=0))
        self.assertEqual(bc["e_el_kwh_anno"], 0.0)
        self.assertEqual(bc["f_kwh_pci_anno"], 0.0)
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(bc["van"], -450000.0)
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])

    def test_potenza_zero(self):
        # Potenza zero: come ore zero, risparmio
        # zero e verdetto NON_CALCOLABILE.
        bc = mh892_calcola(**_demo_kwargs(p_el_kw=0))
        self.assertEqual(bc["e_el_kwh_anno"], 0.0)
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_quota_zero_co2_negativa(self):
        # Con quota calore zero il risparmio resta
        # positivo (35636,36) ma la CO2 evitata
        # diventa negativa (meno 10,91 t/anno):
        # senza calore valorizzato la cella
        # emette piu CO2 di quanta ne spiazzi.
        bc = mh892_calcola(**_demo_kwargs(quota_valorizzata=0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 35636.36,
                               places=2)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], -10.91,
                               places=2)
        self.assertLess(bc["co2_evitata_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_prezzo_elettricita_basso_risparmio_negativo(self):
        # A prezzo elettricita' 0,10 il risparmio
        # diventa negativo (meno 24161,62):
        # NON_CALCOLABILE, non NON_CONVIENTE.
        bc = mh892_calcola(**_demo_kwargs(p_el=0.10))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -24161.62,
                               places=2)
        self.assertLess(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh892_calcola(**_demo_kwargs(capex_specifico=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero(self):
        bc = mh892_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(bc["van"], 627575.76, places=2)
        self.assertEqual(bc["payback"], 7)

    def test_eta_zero_non_calcolabile(self):
        kw = _demo_kwargs(eta_el=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        kw = _demo_kwargs(eta_th=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)
        kw = _demo_kwargs(eta_caldaia=0)
        self.assertRaises(ValueError, mh892_calcola, **kw)

    def test_eta_el_bassa_risparmio_minore(self):
        # Con eta elettrica 0,50 il gas in ingresso
        # sale a 1600000 kWh e il risparmio scende
        # a 63822,22, ma il verdetto resta
        # CONVIENTE.
        bc = mh892_calcola(**_demo_kwargs(eta_el=0.50))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 63822.22,
                               places=2)
        self.assertAlmostEqual(bc["van"], 212452.84, places=2)
        self.assertEqual(bc["payback"], 8)
        self.assertAlmostEqual(bc["co2_evitata_t_anno"], 59.56,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def892\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh892_demo().keys()), lette - set(mh892_demo().keys()))
        self.assertEqual(lette, set(mh892_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc892\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc892\["([^"]+)"\]', src))
        attese = set(mh892_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 891 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 892.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 896)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab892:"), 1)
        self.assertTrue(src.startswith("    # W897"))

    def test_ui_tab892_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab892:"), 1)
        self.assertIn("def mh892_demo(", src_h)
        self.assertIn("def mh892_calcola(", src_h)
        self.assertIn("tab892", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Cogenerazione a fuel cell: l'elettricità + calore senza combustione paga?", src)
        self.assertIn("⚡🔋 Cogenerazione a fuel cell: l'elettricità + calore senza combustione paga?", src)
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
        chiavi = re.findall(r'key="(st892_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st892_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st892_calcola"', src)
        self.assertIn('key="st892_csv"', src)
        self.assertIn('key="st892_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg892"), src.index(".paiac("))
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
