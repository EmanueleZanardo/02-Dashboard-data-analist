"""Test nuova scheda autonoleggio: flotta
elettrica + ricarica in sede batte la
flotta diesel?

Business case annuo di una societa' di
autonoleggio, guidato dai GIORNI DI
NOLEGGIO VENDUTI ALL'ANNO (n_auto x gg)
e dai KM AL GIORNO PER AUTO (non camion
elettrico merci, non treno/traghetto di
linea, non auto privata): giorni_auto =
n_auto x gg; km_anno = giorni_auto x
km_giorno; litri = km_anno x cons_diesel
/ 100; C_carb = litri x p_diesel;
C_manut_base = km_anno x manut_diesel;
C_base = somma; kWh_anno = km_anno x
cons_ev / 100; p_medio = q_sede x p_sede
+ (1 - q_sede) x p_pub; C_energia =
kWh_anno x p_medio; C_manut_alt =
km_anno x manut_ev; C_alt = somma;
risparmio = C_base - C_alt; CAPEX =
n_colonnine x capex_colonnina +
capex_adeguamento + n_auto x
sovrapprezzo_ev_auto (demo 315.000);
CO2 base = litri x 2,68 / 1000; CO2 alt
= kWh_anno x 0,25 / 1000; CO2 evitata =
base - alt (segno libero); flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo medio di
ricarica di pareggio p_medio_star =
(C_base - C_manut_alt) / kWh_anno in
forma chiusa (demo 0,7867647058823529
EUR/kWh), None se kWh_anno nullo o se
il rapporto e' negativo. E' una SOGLIA
MASSIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'elettrico
perde, sotto vince.
Verdetto: NON_CALCOLABILE se input
degenere (n_auto <= 0 o non intero,
gg <= 0 o non intero, km_giorno < 0,
consumi < 0, prezzi < 0, manutenzioni
< 0, q_sede < 0 o > 1, n_colonnine < 0
o non intero, voci CAPEX < 0, fattori
CO2 < 0, WACC < 0, vita <= 0 o non
intera, tolleranza < 0) o se risparmio
<= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza PERCENTUALE
del CAPEX, NON_CONVIENTE altrimenti.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w863_helpers import (
        demo_calcoli,
        mh859_c_alt,
        mh859_c_base,
        mh859_c_carb,
        mh859_c_energia,
        mh859_c_manut_alt,
        mh859_c_manut_base,
        mh859_calcola,
        mh859_capex_totale,
        mh859_co2_alt,
        mh859_co2_base,
        mh859_co2_evitata,
        mh859_csv,
        mh859_demo,
        mh859_demo_calcoli,
        mh859_flussi,
        mh859_frazione,
        mh859_giorni_auto_anno,
        mh859_int_nneg,
        mh859_int_pos,
        mh859_km_anno,
        mh859_kwh_anno,
        mh859_litri,
        mh859_nneg,
        mh859_num,
        mh859_p_medio,
        mh859_p_medio_pareggio,
        mh859_payback,
        mh859_pos,
        mh859_risparmio,
        mh859_sensibilita,
        mh859_tir,
        mh859_valida,
        mh859_van,
        mh859_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w863_helpers", os.path.join(_hf, "w863_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh859_c_alt = _mod.mh859_c_alt
    mh859_c_base = _mod.mh859_c_base
    mh859_c_carb = _mod.mh859_c_carb
    mh859_c_energia = _mod.mh859_c_energia
    mh859_c_manut_alt = _mod.mh859_c_manut_alt
    mh859_c_manut_base = _mod.mh859_c_manut_base
    mh859_calcola = _mod.mh859_calcola
    mh859_capex_totale = _mod.mh859_capex_totale
    mh859_co2_alt = _mod.mh859_co2_alt
    mh859_co2_base = _mod.mh859_co2_base
    mh859_co2_evitata = _mod.mh859_co2_evitata
    mh859_csv = _mod.mh859_csv
    mh859_demo = _mod.mh859_demo
    mh859_demo_calcoli = _mod.mh859_demo_calcoli
    mh859_flussi = _mod.mh859_flussi
    mh859_frazione = _mod.mh859_frazione
    mh859_giorni_auto_anno = _mod.mh859_giorni_auto_anno
    mh859_int_nneg = _mod.mh859_int_nneg
    mh859_int_pos = _mod.mh859_int_pos
    mh859_km_anno = _mod.mh859_km_anno
    mh859_kwh_anno = _mod.mh859_kwh_anno
    mh859_litri = _mod.mh859_litri
    mh859_nneg = _mod.mh859_nneg
    mh859_num = _mod.mh859_num
    mh859_p_medio = _mod.mh859_p_medio
    mh859_p_medio_pareggio = _mod.mh859_p_medio_pareggio
    mh859_payback = _mod.mh859_payback
    mh859_pos = _mod.mh859_pos
    mh859_risparmio = _mod.mh859_risparmio
    mh859_sensibilita = _mod.mh859_sensibilita
    mh859_tir = _mod.mh859_tir
    mh859_valida = _mod.mh859_valida
    mh859_van = _mod.mh859_van
    mh859_verdetto = _mod.mh859_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w863_helpers.py")
_UI_PATH = _risolvi("w863_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "8"
_VECCHIO_TAB = "tab85" + "8"
_VECCHIO_ST = "st85" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "giorni_auto_anno": 9600,
    "km_anno": 1152000.0,
    "litri_diesel_anno": 74880.0,
    "c_carb_eur_anno": 131040.0,
    "c_manut_base_eur_anno": 51840.0,
    "c_base_eur_anno": 182880.0,
    "kwh_anno": 195840.0,
    "p_medio_eur_kwh": 0.319,
    "c_energia_eur_anno": 62472.96,
    "c_manut_alt_eur_anno": 28800.0,
    "c_alt_eur_anno": 91272.96,
    "risparmio_eur_anno": 91607.04,
    "capex_eur": 315000.0,
    "co2_base_t_anno": 200.6784,
    "co2_alt_t_anno": 48.96,
    "co2_evitata_t_anno": 151.7184,
    "van": 277075.7897812713,
    "tir": 23.81680342131863,
    "payback": 4,
    "p_medio_pareggio": 0.7867647058823529,
}


def _demo_kwargs(**over):
    kw = dict(mh859_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh859_num(3, "x"), 3.0)
        self.assertEqual(mh859_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh859_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh859_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh859_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh859_pos(0, "x")
        with self.assertRaises(ValueError):
            mh859_pos(-1, "x")
        self.assertEqual(mh859_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh859_int_pos(15, "x"), 15)
        self.assertEqual(mh859_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh859_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh859_int_pos(15.5, "x")

    def test_int_nneg(self):
        self.assertEqual(mh859_int_nneg(0, "x"), 0)
        self.assertEqual(mh859_int_nneg(10, "x"), 10)
        with self.assertRaises(ValueError):
            mh859_int_nneg(-1, "x")
        with self.assertRaises(ValueError):
            mh859_int_nneg(2.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh859_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh859_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh859_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh859_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_giorni_e_km(self):
        self.assertEqual(mh859_giorni_auto_anno(40, 240), 9600)
        self.assertEqual(mh859_km_anno(9600, 120), 1152000.0)
        with self.assertRaises(ValueError):
            mh859_giorni_auto_anno(0, 240)
        with self.assertRaises(ValueError):
            mh859_giorni_auto_anno(40, 0)

    def test_litri_e_costi_base(self):
        self.assertEqual(mh859_litri(1152000.0, 6.5), 74880.0)
        self.assertEqual(mh859_c_carb(74880.0, 1.75), 131040.0)
        self.assertEqual(mh859_c_manut_base(1152000.0, 0.045), 51840.0)
        self.assertEqual(mh859_c_base(131040.0, 51840.0), 182880.0)

    def test_kwh_p_medio_e_costi_alt(self):
        self.assertEqual(mh859_kwh_anno(1152000.0, 17.0), 195840.0)
        self.assertAlmostEqual(mh859_p_medio(0.70, 0.22, 0.55), 0.319)
        self.assertAlmostEqual(mh859_c_energia(195840.0, 0.319), 62472.96)
        self.assertEqual(mh859_c_manut_alt(1152000.0, 0.025), 28800.0)
        self.assertAlmostEqual(mh859_c_alt(62472.96, 28800.0), 91272.96)
        self.assertAlmostEqual(
            mh859_risparmio(182880.0, 91272.96), 91607.04)

    def test_p_medio_estremi_quota(self):
        self.assertEqual(mh859_p_medio(0.0, 0.22, 0.55), 0.55)
        self.assertEqual(mh859_p_medio(1.0, 0.22, 0.55), 0.22)

    def test_capex_totale_voci(self):
        self.assertEqual(mh859_capex_totale(10, 3500, 40000, 40, 6000),
                         315000.0)
        self.assertEqual(mh859_capex_totale(0, 3500, 40000, 40, 6000),
                         280000.0)

    def test_co2_con_divisione_per_mille(self):
        cb = mh859_co2_base(74880.0, 2.68)
        self.assertAlmostEqual(cb, 200.6784, places=4)
        ca = mh859_co2_alt(195840.0, 0.25)
        self.assertAlmostEqual(ca, 48.96, places=4)
        self.assertAlmostEqual(mh859_co2_evitata(cb, ca), 151.7184,
                               places=4)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh859_flussi(315000, 91607.04, 3),
                         [-315000, 91607.04, 91607.04, 91607.04])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh859_van([-100, 60, 60], 0), 20.0)
        bc = mh859_demo_calcoli()
        self.assertAlmostEqual(mh859_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh859_demo_calcoli()
        tir = mh859_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh859_tir([-100, -10, -10]))
        self.assertIsNone(mh859_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh859_demo_calcoli()
        self.assertEqual(mh859_payback(bc["flussi"]), 4)
        self.assertIsNone(mh859_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh859_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh859_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:4]), -40178.88, places=2)
        self.assertAlmostEqual(sum(flussi[:5]), 51428.16, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh859_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh859_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh859_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh859_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh859_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh859_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh859_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_medio_pareggio_demo_soglia_massima(self):
        bc = mh859_demo_calcoli()
        self.assertAlmostEqual(bc["p_medio_pareggio"],
                               0.7867647058823529, places=12)
        self.assertAlmostEqual(mh859_p_medio_pareggio(
            bc["c_base_eur_anno"], bc["c_manut_alt_eur_anno"],
            bc["kwh_anno"]),
            0.7867647058823529, places=12)
        # Soglia MASSIMA: sopra perde, sotto vince.
        self.assertGreater(bc["p_medio_eur_kwh"], 0.0)
        self.assertLess(bc["p_medio_eur_kwh"], bc["p_medio_pareggio"])

    def test_p_medio_pareggio_kwh_nullo_none(self):
        self.assertIsNone(mh859_p_medio_pareggio(182880.0, 28800.0, 0.0))

    def test_p_medio_pareggio_negativo_none(self):
        # Costo base sotto la manutenzione alt: il rapporto
        # e' negativo, l'alternativa vince anche a ricarica
        # gratuita.
        self.assertIsNone(mh859_p_medio_pareggio(10000.0, 28800.0,
                                                195840.0))

    def test_p_medio_pareggio_caso_limite_zero(self):
        self.assertEqual(mh859_p_medio_pareggio(28800.0, 28800.0,
                                               195840.0), 0.0)

    def test_valida_demo_ok(self):
        demo = mh859_demo()
        val = mh859_valida(*[demo[k] for k in (
            "n_auto", "gg_noleggio_auto_anno", "km_giorno",
            "cons_diesel_l_100km", "p_diesel",
            "manut_diesel_eur_km", "cons_ev_kwh_100km",
            "q_sede", "p_sede", "p_pub", "manut_ev_eur_km",
            "n_colonnine", "capex_colonnina",
            "capex_adeguamento", "sovrapprezzo_ev_auto",
            "f_co2_diesel_kg_l", "f_co2_el_kg_kwh",
            "wacc_pct", "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_n_auto_zero_no(self):
        kw = _demo_kwargs(n_auto=0)
        self.assertRaises(ValueError, mh859_calcola, **kw)

    def test_valida_gg_zero_no(self):
        kw = _demo_kwargs(gg_noleggio_auto_anno=0)
        self.assertRaises(ValueError, mh859_calcola, **kw)

    def test_valida_quota_sopra_uno_no(self):
        kw = _demo_kwargs(q_sede=1.1)
        self.assertRaises(ValueError, mh859_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh859_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh859_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_pub=float("nan"))
        self.assertRaises(ValueError, mh859_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("km_giorno", -1),
                              ("p_diesel", -0.01),
                              ("capex_adeguamento", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh859_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh859_calcola(mh859_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh859_calcola(dict(mh859_demo(), capex_adeguamento=999999),
                           capex_adeguamento=40000)
        self.assertEqual(bc["capex_eur"], 315000.0)


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
            bc["co2_evitata_t_anno"],
            bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(
            bc["c_base_eur_anno"],
            bc["c_carb_eur_anno"] + bc["c_manut_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["c_energia_eur_anno"] + bc["c_manut_alt_eur_anno"])

    def test_coerenza_p_medio(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["p_medio_eur_kwh"],
            0.70 * 0.22 + 0.30 * 0.55)
        self.assertAlmostEqual(
            bc["p_medio_pareggio"],
            (bc["c_base_eur_anno"] - bc["c_manut_alt_eur_anno"])
            / bc["kwh_anno"])

    def test_sensibilita_valori(self):
        s = mh859_sensibilita(**mh859_demo())
        self.assertAlmostEqual(s["p_pub_piu20"]["risparmio_eur_anno"],
                               85144.32, places=2)
        self.assertAlmostEqual(s["p_pub_piu20"]["van"],
                               235305.86, places=2)
        self.assertAlmostEqual(s["p_diesel_meno20"]["risparmio_eur_anno"],
                               65399.04, places=2)
        self.assertAlmostEqual(s["p_diesel_meno20"]["van"],
                               107687.91, places=2)
        self.assertAlmostEqual(s["solo_pubblico"]["risparmio_eur_anno"],
                               46368.0, places=2)
        self.assertAlmostEqual(s["solo_pubblico"]["van"],
                               -15313.75, places=2)
        self.assertEqual(s["solo_pubblico"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["q_sede_100"]["risparmio_eur_anno"],
                               110995.2, places=2)
        self.assertAlmostEqual(s["q_sede_100"]["van"],
                               402385.59, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -37924.21, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "MARGINALE")
        self.assertEqual(s["capex_doppio"]["payback"], 7)
        self.assertAlmostEqual(s["vita_4"]["van"],
                               9834.03, places=2)
        self.assertEqual(s["vita_4"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               417856.32, places=2)

    def test_marginale_con_capex_adeguamento_alto(self):
        # CAPEX totale 595.000 (adeguamento 320.000):
        # VAN negativa entro la tolleranza del 10%.
        bc = mh859_calcola(**_demo_kwargs(capex_adeguamento=320000))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_adeguamento_altissimo(self):
        bc = mh859_calcola(**_demo_kwargs(capex_adeguamento=500000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh859_calcola(**_demo_kwargs(p_diesel=0.0,
                                          manut_diesel_eur_km=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_km_giorno_zero_pareggio_none(self):
        bc = mh859_calcola(**_demo_kwargs(km_giorno=0))
        self.assertEqual(bc["km_anno"], 0.0)
        self.assertIsNone(bc["p_medio_pareggio"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh859_csv(bc, mh859_demo())
        for voce in ("n_auto", "km_anno",
                     "litri_diesel_anno", "p_medio_eur_kwh",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 9)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -315000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Giorni auto all'anno", voci)
        self.assertIn("Prezzo medio di ricarica (EUR/kWh)", voci)

    def test_km_scala_lineare_con_giorni(self):
        self.assertAlmostEqual(mh859_km_anno(2000.0, 120.0),
                               2.0 * mh859_km_anno(1000.0, 120.0))

    def test_c_alt_solo_pubblico_piu_cara(self):
        senza = mh859_c_alt(195840.0 * 0.22, 28800.0)
        con = mh859_c_alt(195840.0 * 0.55, 28800.0)
        self.assertAlmostEqual(con - senza, 195840.0 * 0.33)

    def test_sensibilita_chiavi_complete(self):
        s = mh859_sensibilita(**mh859_demo())
        self.assertEqual(set(s.keys()),
                         {"p_pub_piu20", "p_diesel_meno20", "solo_pubblico",
                          "q_sede_100", "capex_doppio", "vita_4",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh859_csv(bc, mh859_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("km_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh859_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh859_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh859_calcola(**_demo_kwargs(n_colonnine=0))
        self.assertEqual(bc["capex_eur"], 280000.0)
        bc = mh859_calcola(**_demo_kwargs(q_sede=0))
        self.assertEqual(bc["p_medio_eur_kwh"], 0.55)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def859\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh859_demo().keys()), lette - set(mh859_demo().keys()))
        self.assertEqual(lette, set(mh859_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc859\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc859\["([^"]+)"\]', src))
        attese = set(mh859_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab859:"), 1)
        self.assertTrue(src.startswith("    # W863"))

    def test_ui_tab859_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab859:"), 1)
        self.assertIn("def mh859_demo(", src_h)
        self.assertIn("def mh859_calcola(", src_h)
        self.assertIn("tab859", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Autonoleggio: flotta elettrica + ricarica in sede batte la flotta diesel?", src)
        self.assertIn("🚗 Autonoleggio: flotta elettrica + ricarica in sede batte la flotta diesel?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        for vecchio in (_VECCHIO_MH,):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st859_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st859_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st859_calcola"', src)
        self.assertIn('key="st859_csv"', src)
        self.assertIn('key="st859_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg859"), src.index(".paiac("))
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
            self.assertNotIn("—", src)
            self.assertNotIn("–", src)


if __name__ == "__main__":
    unittest.main()
