"""Test nuova scheda discarica: il biogas da
discarica alimenta un cogeneratore e batte
la torcia?
Repo path: tests/test_w895_discarica_biogas_chp.py

Business case annuo di una discarica attiva
o chiusa, guidato dai RIFIUTI CONFERITI
t/anno (demo 40000) e dagli ANNI DI
CONFERIMENTO (demo 15, vita del caso):
rifiuti totali = 40000 x 15 = 600000 t;
CH4 prodotto = 600000 x 3,5 = 2100000
m3 CH4/anno; CH4 captato = 2100000 x 0,55
= 1155000 m3 CH4/anno; biogas captato =
1155000 diviso 0,50 = 2310000 m3
biogas/anno; energia CH4 = 1155000 x 9,97
= 11515350 kWh/anno; E_el = 11515350 x
0,35 = 4030372,50 kWh/anno (circa 504 kWel
medi a 8000 ore/anno); Q_th = 11515350 x
0,45 x 0,50 = 2590953,75 kWh/anno; ricavi
elettrici = 4030372,50 x 0,12 = 483644,70
EUR/anno; ricavi termici = 2590953,75 x
0,04 = 103638,15 EUR/anno; ricavi totali
587282,85 EUR/anno; costo base = sola O&M
torcia 45000,00 EUR/anno (nessun ricavo);
costo alternativo = 90000 meno 587282,85 =
meno 497282,85 EUR/anno (NEGATIVO perche'
i ricavi superano l'O&M); risparmio
542282,85 EUR/anno; CAPEX 300000 +
250000 + 1100000 + 100000 = 1750000 EUR
(somma verificata a mano); CO2 evitata =
(4030372,50 x 0,35 piu 2590953,75 x 0,20)
diviso 1000 = 1928,82 t/anno, SOLO energia
spiazzata: il metano NON si conta come
evitato (torcia e CHP convertono ENTRAMBI
il CH4 captato in CO2); flussi [CAPEX
negativo, risparmio x vita]; VAN al tasso
(FRAZIONE in ingresso, 0,05 = 5 %, usato
diretto, NON diviso per 100); TIR per
bisezione su intervallo da meno 0,9 a 5,0;
payback (primo anno con cumulato maggiore
o uguale a 0). Tolleranza in PERCENTUALE
(10 = 10 % del CAPEX). La resa annua
piatta e una SEMPLIFICAZIONE DICHIARATA
(profilo reale crescente poi decrescente,
qui valore medio costante). Verdetto:
NON_CALCOLABILE se input degenere
(rifiuti negativi, anni conferimento nulli
o negativi o non interi, resa CH4
negativa, quota captata sotto 0 o sopra 1,
frazione CH4 nulla o negativa o sopra 1,
PCI CH4 nullo o negativo, eta el sotto 0
o sopra 1, eta th sotto 0 o sopra 1,
quota calore sotto 0 o sopra 1, prezzi
negativi, O&M negative, voci CAPEX
negative, tasso negativo, tolleranza
negativa, fattori CO2 negativi) o se
risparmio minore o uguale a 0 (guard
degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN
maggiore di 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: anni conferimento zero o non
interi non calcolabili (ValueError negli
helper, guard NON_CALCOLABILE in UI);
frazione CH4 zero non calcolabile
(divisione); PCI CH4 zero non calcolabile;
quota captata zero (CH4 captato zero,
risparmio meno 45000,00, NON_CALCOLABILE);
prezzo elettricita zero (risparmio
positivo 58638,15 ma VAN negativa,
NON_CONVIENTE, payback None); CAPEX zero
(TIR non definita, payback 0); tasso zero
(VAN uguale alla somma dei flussi).
Distinzione esplicita: qui SOLO gas di
discarica da discarica attiva o chiusa
verso cogeneratore CHP contro torcia,
NIENTE compostaggio, NIENTE biogas da
digestione anaerobica, NIENTE
termovalorizzatore, NIENTE incenerimento
di rifiuti, NIENTE discarica come costo
di smaltimento in altre schede.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w895_helpers import (
        demo_calcoli,
        mh890_biogas_captato,
        mh890_c_alt,
        mh890_c_base,
        mh890_calcola,
        mh890_capex_totale,
        mh890_ch4_captato,
        mh890_ch4_prodotto,
        mh890_co2_evitata,
        mh890_csv,
        mh890_demo,
        mh890_demo_calcoli,
        mh890_e_el,
        mh890_energia_ch4,
        mh890_flussi,
        mh890_frazione,
        mh890_frazione_pos,
        mh890_int_pos,
        mh890_nneg,
        mh890_num,
        mh890_payback,
        mh890_pos,
        mh890_q_th,
        mh890_ricavi_el,
        mh890_ricavi_th,
        mh890_ricavi_tot,
        mh890_rifiuti_totali,
        mh890_risparmio,
        mh890_sensibilita,
        mh890_tir,
        mh890_valida,
        mh890_van,
        mh890_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w895_helpers", os.path.join(_hf, "w895_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh890_biogas_captato = _mod.mh890_biogas_captato
    mh890_c_alt = _mod.mh890_c_alt
    mh890_c_base = _mod.mh890_c_base
    mh890_calcola = _mod.mh890_calcola
    mh890_capex_totale = _mod.mh890_capex_totale
    mh890_ch4_captato = _mod.mh890_ch4_captato
    mh890_ch4_prodotto = _mod.mh890_ch4_prodotto
    mh890_co2_evitata = _mod.mh890_co2_evitata
    mh890_csv = _mod.mh890_csv
    mh890_demo = _mod.mh890_demo
    mh890_demo_calcoli = _mod.mh890_demo_calcoli
    mh890_e_el = _mod.mh890_e_el
    mh890_energia_ch4 = _mod.mh890_energia_ch4
    mh890_flussi = _mod.mh890_flussi
    mh890_frazione = _mod.mh890_frazione
    mh890_frazione_pos = _mod.mh890_frazione_pos
    mh890_int_pos = _mod.mh890_int_pos
    mh890_nneg = _mod.mh890_nneg
    mh890_num = _mod.mh890_num
    mh890_payback = _mod.mh890_payback
    mh890_pos = _mod.mh890_pos
    mh890_q_th = _mod.mh890_q_th
    mh890_ricavi_el = _mod.mh890_ricavi_el
    mh890_ricavi_th = _mod.mh890_ricavi_th
    mh890_ricavi_tot = _mod.mh890_ricavi_tot
    mh890_rifiuti_totali = _mod.mh890_rifiuti_totali
    mh890_risparmio = _mod.mh890_risparmio
    mh890_sensibilita = _mod.mh890_sensibilita
    mh890_tir = _mod.mh890_tir
    mh890_valida = _mod.mh890_valida
    mh890_van = _mod.mh890_van
    mh890_verdetto = _mod.mh890_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w895_helpers.py")
_UI_PATH = _risolvi("w895_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "9"
_VECCHIO_TAB = "tab88" + "9"
_VECCHIO_ST = "st88" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "anni_conferimento": 15,
    "vita_anni": 15,
    "rifiuti_totali_t": 600000.0,
    "ch4_prodotto_m3_anno": 2100000.0,
    "ch4_captato_m3_anno": 1155000.0,
    "biogas_captato_m3_anno": 2310000.0,
    "energia_ch4_kwh_anno": 11515350.0,
    "e_el_kwh_anno": 4030372.4999999995,
    "q_th_kwh_anno": 2590953.75,
    "ricavi_el_eur_anno": 483644.69999999995,
    "ricavi_th_eur_anno": 103638.15000000001,
    "ricavi_tot_eur_anno": 587282.85,
    "c_base_eur_anno": 45000.0,
    "c_alt_eur_anno": -497282.85,
    "risparmio_eur_anno": 542282.85,
    "capex_eur": 1750000.0,
    "co2_evitata_t_anno": 1928.8211249999997,
    "van": 3878710.542969979,
    "tir": 30.410137231369273,
    "payback": 4,
}


def _demo_kwargs(**over):
    kw = dict(mh890_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh890_num(3, "x"), 3.0)
        self.assertEqual(mh890_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh890_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh890_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh890_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh890_pos(0, "x")
        with self.assertRaises(ValueError):
            mh890_pos(-1, "x")
        self.assertEqual(mh890_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh890_int_pos(15, "x"), 15)
        self.assertEqual(mh890_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh890_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh890_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh890_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh890_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh890_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh890_frazione(1.1, "x")

    def test_frazione_pos_intervallo(self):
        self.assertEqual(mh890_frazione_pos(0.5, "x"), 0.5)
        self.assertEqual(mh890_frazione_pos(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh890_frazione_pos(0.0, "x")
        with self.assertRaises(ValueError):
            mh890_frazione_pos(-0.1, "x")
        with self.assertRaises(ValueError):
            mh890_frazione_pos(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_rifiuti_totali_e_ch4(self):
        self.assertEqual(mh890_rifiuti_totali(40000, 15), 600000.0)
        self.assertEqual(mh890_ch4_prodotto(600000.0, 3.5), 2100000.0)
        self.assertEqual(mh890_ch4_captato(2100000.0, 0.55), 1155000.0)
        self.assertEqual(mh890_biogas_captato(1155000.0, 0.50),
                         2310000.0)
        self.assertEqual(mh890_energia_ch4(1155000.0, 9.97),
                         11515350.0)
        with self.assertRaises(ValueError):
            mh890_biogas_captato(1155000.0, 0)
        with self.assertRaises(ValueError):
            mh890_energia_ch4(1155000.0, 0)

    def test_biogas_con_frazione_uno_uguale_ch4(self):
        # Con frazione CH4 uguale a 1 il biogas
        # captato coincide col CH4 captato.
        self.assertEqual(mh890_biogas_captato(1155000.0, 1.0),
                         1155000.0)

    def test_e_el_e_q_th(self):
        self.assertAlmostEqual(mh890_e_el(11515350.0, 0.35),
                               4030372.50, places=2)
        self.assertAlmostEqual(mh890_q_th(11515350.0, 0.45, 0.50),
                               2590953.75, places=2)
        # Il calore NON valorizzato e perso: con
        # quota calore zero il calore valorizzato
        # e zero anche se il CHP produce calore.
        self.assertEqual(mh890_q_th(11515350.0, 0.45, 0.0), 0.0)
        # Con eta el zero non c'e elettricita.
        self.assertEqual(mh890_e_el(11515350.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh890_e_el(11515350.0, 1.1)
        with self.assertRaises(ValueError):
            mh890_q_th(11515350.0, 0.45, 1.1)

    def test_ricavi(self):
        self.assertAlmostEqual(mh890_ricavi_el(4030372.5, 0.12),
                               483644.70, places=2)
        self.assertAlmostEqual(mh890_ricavi_th(2590953.75, 0.04),
                               103638.15, places=2)
        self.assertAlmostEqual(
            mh890_ricavi_tot(483644.7, 103638.15),
            587282.85, places=2)

    def test_costi_e_risparmio(self):
        self.assertEqual(mh890_c_base(45000), 45000.0)
        # Il costo alternativo e NEGATIVO perche'
        # i ricavi superano l'O&M: ed e' corretto
        # cosi', non un errore di segno.
        self.assertAlmostEqual(mh890_c_alt(90000, 587282.85),
                               -497282.85, places=2)
        self.assertAlmostEqual(
            mh890_risparmio(45000.0, -497282.85),
            542282.85, places=2)

    def test_capex_totale_voci(self):
        self.assertEqual(mh890_capex_totale(300000, 250000,
                                            1100000, 100000),
                         1750000.0)
        self.assertEqual(mh890_capex_totale(300000, 250000,
                                            0, 100000),
                         650000.0)

    def test_co2_solo_energia_spiazzata(self):
        co2 = mh890_co2_evitata(4030372.5, 0.35, 2590953.75, 0.20)
        self.assertAlmostEqual(co2, 1928.82, places=2)
        # Con fattori zero la CO2 evitata e zero
        # anche se il CH4 viene captato e bruciato:
        # il metano NON si conta come evitato,
        # perche' torcia e CHP lo convertono
        # ENTRAMBI in CO2.
        self.assertEqual(mh890_co2_evitata(4030372.5, 0.0,
                                           2590953.75, 0.0), 0.0)
        self.assertAlmostEqual(
            mh890_co2_evitata(4030372.5, 0.35, 0.0, 0.20),
            1410.63, places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh890_flussi(1750000, 542282.85, 3),
                         [-1750000, 542282.85, 542282.85, 542282.85])

    def test_van_tasso_zero_e_cinque(self):
        self.assertAlmostEqual(mh890_van([-100, 60, 60], 0), 20.0)
        bc = mh890_demo_calcoli()
        self.assertAlmostEqual(mh890_van(bc["flussi"], 0.05), bc["van"])

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 3878710,54; con 5,0 (cioe' 500 % se
        # letto come frazione) sarebbe tutt'altra.
        bc = mh890_demo_calcoli()
        self.assertAlmostEqual(mh890_van(bc["flussi"], 0.05),
                               3878710.54, places=2)
        self.assertNotAlmostEqual(mh890_van(bc["flussi"], 5.0),
                                  3878710.54, places=2)

    def test_tir_demo(self):
        bc = mh890_demo_calcoli()
        tir = mh890_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh890_tir([-100, -10, -10]))
        self.assertIsNone(mh890_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh890_demo_calcoli()
        self.assertEqual(mh890_payback(bc["flussi"]), 4)
        self.assertIsNone(mh890_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh890_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh890_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:4]), -123151.45, places=2)
        self.assertAlmostEqual(sum(flussi[:5]), 419131.40, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh890_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh890_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh890_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh890_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh890_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh890_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh890_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh890_demo()
        val = mh890_valida(*[demo[k] for k in (
            "rifiuti_t_anno", "anni_conferimento", "resa_ch4",
            "quota_captata", "fraz_ch4", "pci_ch4", "eta_el",
            "eta_th", "quota_calore", "p_el", "p_calore",
            "om_chp", "om_torcia", "capex_pozzi", "capex_rete",
            "capex_chp", "capex_allaccio", "tasso",
            "tolleranza_pct", "f_co2_rete", "f_co2_gas")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_anni_zero_e_non_interi_no(self):
        kw = _demo_kwargs(anni_conferimento=0)
        self.assertRaises(ValueError, mh890_calcola, **kw)
        kw = _demo_kwargs(anni_conferimento=15.5)
        self.assertRaises(ValueError, mh890_calcola, **kw)
        kw = _demo_kwargs(anni_conferimento=10)
        bc = mh890_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 10)

    def test_valida_frazione_ch4_e_pci_zero_no(self):
        kw = _demo_kwargs(fraz_ch4=0)
        self.assertRaises(ValueError, mh890_calcola, **kw)
        kw = _demo_kwargs(pci_ch4=0)
        self.assertRaises(ValueError, mh890_calcola, **kw)

    def test_valida_frazioni_sopra_uno_no(self):
        for campo, valore in (("quota_captata", 1.1),
                              ("fraz_ch4", 1.1),
                              ("eta_el", 1.1),
                              ("eta_th", 1.1),
                              ("quota_calore", 1.1)):
            with self.assertRaises(ValueError):
                mh890_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh890_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("rifiuti_t_anno", -1),
                              ("resa_ch4", -0.1),
                              ("p_el", -0.01),
                              ("p_calore", -0.01),
                              ("om_chp", -1),
                              ("om_torcia", -1),
                              ("capex_pozzi", -1),
                              ("capex_chp", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1),
                              ("f_co2_rete", -0.01),
                              ("f_co2_gas", -0.01)):
            with self.assertRaises(ValueError):
                mh890_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh890_calcola(mh890_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh890_calcola(dict(mh890_demo(), capex_chp=99999),
                           capex_chp=1100000)
        self.assertEqual(bc["capex_eur"], 1750000.0)


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
        self.assertEqual(bc["payback"], 4)

    def test_coerenza_costi_e_co2(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["om_chp"] - bc["ricavi_tot_eur_anno"])
        self.assertAlmostEqual(
            bc["ricavi_tot_eur_anno"],
            bc["ricavi_el_eur_anno"] + bc["ricavi_th_eur_anno"])
        self.assertAlmostEqual(
            bc["ricavi_el_eur_anno"],
            bc["e_el_kwh_anno"] * bc["p_el"])
        self.assertAlmostEqual(
            bc["ricavi_th_eur_anno"],
            bc["q_th_kwh_anno"] * bc["p_calore"])
        self.assertAlmostEqual(
            bc["e_el_kwh_anno"],
            bc["energia_ch4_kwh_anno"] * bc["eta_el"])
        self.assertAlmostEqual(
            bc["q_th_kwh_anno"],
            bc["energia_ch4_kwh_anno"] * bc["eta_th"]
            * bc["quota_calore"])
        self.assertAlmostEqual(
            bc["energia_ch4_kwh_anno"],
            bc["ch4_captato_m3_anno"] * bc["pci_ch4"])
        self.assertAlmostEqual(
            bc["biogas_captato_m3_anno"],
            bc["ch4_captato_m3_anno"] / bc["fraz_ch4"])
        self.assertAlmostEqual(
            bc["ch4_captato_m3_anno"],
            bc["ch4_prodotto_m3_anno"] * bc["quota_captata"])
        self.assertAlmostEqual(
            bc["ch4_prodotto_m3_anno"],
            bc["rifiuti_totali_t"] * bc["resa_ch4"])
        self.assertAlmostEqual(
            bc["rifiuti_totali_t"],
            bc["rifiuti_t_anno"] * bc["anni_conferimento"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            (bc["e_el_kwh_anno"] * bc["f_co2_rete"]
             + bc["q_th_kwh_anno"] * bc["f_co2_gas"]) / 1000.0)
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["capex_pozzi"] + bc["capex_rete"]
            + bc["capex_chp"] + bc["capex_allaccio"])

    def test_sensibilita_valori(self):
        s = mh890_sensibilita(**mh890_demo())
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               639011.79, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               4882723.86, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 3)
        self.assertAlmostEqual(s["p_calore_piu20"]["risparmio_eur_anno"],
                               563010.48, places=2)
        self.assertAlmostEqual(s["p_calore_piu20"]["van"],
                               4093856.25, places=2)
        self.assertEqual(s["p_calore_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["senza_calore"]["risparmio_eur_anno"],
                               438644.70, places=2)
        self.assertAlmostEqual(s["senza_calore"]["van"],
                               2802981.99, places=2)
        self.assertEqual(s["senza_calore"]["payback"], 4)
        self.assertEqual(s["senza_calore"]["verdetto"], "CONVIENTE")
        # Senza calore la quota calore e zero ma il
        # CAPEX CHP forfettario resta nel totale:
        # la variante isola l'effetto del calore
        # valorizzato, non del CAPEX.
        self.assertEqual(s["senza_calore"]["capex_eur"], 1750000.0)
        self.assertAlmostEqual(s["captata_040"]["risparmio_eur_anno"],
                               382114.80, places=2)
        self.assertAlmostEqual(s["captata_040"]["van"],
                               2216220.96, places=2)
        self.assertEqual(s["captata_040"]["payback"], 5)
        self.assertEqual(s["captata_040"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               2128710.54, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 7)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["capex_eur"], 3500000.0)
        self.assertAlmostEqual(s["vita_10"]["risparmio_eur_anno"],
                               346521.90, places=2)
        self.assertAlmostEqual(s["vita_10"]["van"],
                               925750.26, places=2)
        self.assertEqual(s["vita_10"]["payback"], 6)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["tasso_0"]["van"],
                               6384242.75, places=2)

    def test_marginale_con_capex_chp_alto(self):
        # CAPEX totale 5700000 (cogeneratore a
        # 5050000): VAN circa meno 71289,46, entro
        # la tolleranza del 10% (570000).
        bc = mh890_calcola(**_demo_kwargs(capex_chp=5050000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -71289.46, places=2)
        self.assertEqual(bc["payback"], 11)

    def test_non_convente_con_capex_chp_altissimo(self):
        bc = mh890_calcola(**_demo_kwargs(capex_chp=6000000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -1021289.46, places=2)
        self.assertEqual(bc["payback"], 13)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh890_calcola(**_demo_kwargs(om_chp=700000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -67717.15,
                               places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh890_csv(bc, mh890_demo())
        for voce in ("rifiuti_t_anno", "anni_conferimento",
                     "resa_ch4", "quota_captata", "fraz_ch4",
                     "pci_ch4", "ch4_prodotto_m3_anno",
                     "ch4_captato_m3_anno",
                     "biogas_captato_m3_anno",
                     "energia_ch4_kwh_anno", "e_el_kwh_anno",
                     "q_th_kwh_anno", "ricavi_tot_eur_anno",
                     "risparmio_eur_anno", "verdetto",
                     "co2_evitata_t_anno"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -1750000.0)
        self.assertEqual(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Rifiuti conferiti (t/anno)", voci)
        self.assertIn("CH4 captato (m3/anno)", voci)
        self.assertIn("Biogas captato (m3/anno)", voci)
        self.assertIn("CAPEX cogeneratore (EUR)", voci)

    def test_c_alt_senza_elettricita_piu_caro(self):
        senza = mh890_c_alt(90000, 103638.15)
        con = mh890_c_alt(90000, 587282.85)
        self.assertAlmostEqual(senza - con, 483644.70, places=2)

    def test_sensibilita_chiavi_complete(self):
        s = mh890_sensibilita(**mh890_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_piu20", "p_calore_piu20",
                          "senza_calore", "captata_040",
                          "capex_doppio", "vita_10", "tasso_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh890_csv(bc, mh890_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("ch4_captato_m3_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh890_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh890_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh890_calcola(**_demo_kwargs(quota_calore=0))
        self.assertEqual(bc["q_th_kwh_anno"], 0.0)
        self.assertEqual(bc["ricavi_th_eur_anno"], 0.0)
        bc = mh890_calcola(**_demo_kwargs(eta_el=0))
        self.assertEqual(bc["e_el_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 58638.15,
                               places=2)


class TestCasiLimite(unittest.TestCase):
    def test_anni_zero_non_calcolabile(self):
        # Anni conferimento zero: non calcolabile
        # negli helper (ValueError) e guard
        # NON_CALCOLABILE in UI.
        kw = _demo_kwargs(anni_conferimento=0)
        self.assertRaises(ValueError, mh890_calcola, **kw)
        self.assertFalse(mh890_valida(*[kw[k] for k in (
            "rifiuti_t_anno", "anni_conferimento", "resa_ch4",
            "quota_captata", "fraz_ch4", "pci_ch4", "eta_el",
            "eta_th", "quota_calore", "p_el", "p_calore",
            "om_chp", "om_torcia", "capex_pozzi", "capex_rete",
            "capex_chp", "capex_allaccio", "tasso",
            "tolleranza_pct", "f_co2_rete", "f_co2_gas")])["valido"])

    def test_anni_non_interi_non_calcolabile(self):
        kw = _demo_kwargs(anni_conferimento=15.5)
        self.assertRaises(ValueError, mh890_calcola, **kw)

    def test_quota_captata_zero(self):
        # Quota captata zero: CH4 captato zero,
        # energia elettrica zero e risparmio meno
        # 45000,00 (sola O&M torcia persa):
        # verdetto NON_CALCOLABILE.
        bc = mh890_calcola(**_demo_kwargs(quota_captata=0))
        self.assertEqual(bc["ch4_captato_m3_anno"], 0.0)
        self.assertEqual(bc["e_el_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -45000.00,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_elettricita_zero_risparmio_positivo_ma_van_negativa(self):
        # A prezzo elettricita zero il risparmio
        # resta positivo (58638,15: il calore da
        # solo copre O&M CHP e torcia) ma la VAN
        # e negativa oltre la tolleranza:
        # NON_CONVIENTE, non NON_CALCOLABILE.
        bc = mh890_calcola(**_demo_kwargs(p_el=0.0))
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 58638.15,
                               places=2)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(bc["payback"])

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh890_calcola(**_demo_kwargs(capex_pozzi=0,
                                          capex_rete=0,
                                          capex_chp=0,
                                          capex_allaccio=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero(self):
        bc = mh890_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(bc["van"], 6384242.75, places=2)
        self.assertEqual(bc["payback"], 4)

    def test_frazione_ch4_zero_non_calcolabile(self):
        kw = _demo_kwargs(fraz_ch4=0)
        self.assertRaises(ValueError, mh890_calcola, **kw)

    def test_pci_zero_non_calcolabile(self):
        kw = _demo_kwargs(pci_ch4=0)
        self.assertRaises(ValueError, mh890_calcola, **kw)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def890\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh890_demo().keys()), lette - set(mh890_demo().keys()))
        self.assertEqual(lette, set(mh890_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc890\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc890\["([^"]+)"\]', src))
        attese = set(mh890_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 889 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 890.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 893)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab890:"), 1)
        self.assertTrue(src.startswith("    # W895"))

    def test_ui_tab890_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab890:"), 1)
        self.assertIn("def mh890_demo(", src_h)
        self.assertIn("def mh890_calcola(", src_h)
        self.assertIn("tab890", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Discarica: il biogas da discarica alimenta un cogeneratore e batte la torcia?", src)
        self.assertIn("🗑️ Discarica: il biogas da discarica alimenta un cogeneratore e batte la torcia?", src)
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
        chiavi = re.findall(r'key="(st890_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st890_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st890_calcola"', src)
        self.assertIn('key="st890_csv"', src)
        self.assertIn('key="st890_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg890"), src.index(".paiac("))
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
