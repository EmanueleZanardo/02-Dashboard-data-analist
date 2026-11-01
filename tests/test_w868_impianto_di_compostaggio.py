"""Test nuova scheda impianto di compostaggio:
aerazione forzata + biofiltro + recupero
calore + FV battono compostaggio
tradizionale in cumuli aperti con
rivoltamento diesel?

Business case annuo di un impianto di
compostaggio, guidato dalle TONNELLATE
all'anno di frazione organica (demo
20.000 t/anno): diesel = t x L/t (demo
20.000 x 4,0 = 80.000 L/anno), costo
diesel 136.000 EUR/anno, O&M base
200.000 EUR/anno, costo base 336.000
EUR/anno; aerazione 300.000 kWh/anno,
biofiltro 60.000 kWh/anno, domanda alt
360.000 kWh/anno; kWp = sup x quota x
kwp/m2 (demo 960 kWp); E_pv 1.056.000
kWh/anno; E_pv_auto = min(E_pv x
f_autoconsumo, domanda alt) (demo
316.800 kWh/anno); immessa 739.200
kWh/anno; deficit 43.200 kWh/anno;
ricavo immissione 59.136 EUR/anno;
calore recuperato 400.000 kWh
termici/anno, ricavo termico 24.000
EUR/anno; O&M alternativa 180.000
EUR/anno; C_alt 108.960 EUR/anno;
risparmio 227.040 EUR/anno; CAPEX
500.000 + 400.000 + 960 x 1.100 =
1.956.000 EUR; CO2 base solo diesel =
80.000 x 2,68 / 1000 = 214,40 t/anno;
CO2 alt = deficit / 1000 x 0,25 = 10,80
t/anno (immessa senza credito CO2);
CO2 evitata 203,60 t/anno; flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo diesel di
pareggio p_diesel_star = (C_alt -
t x om_base_per_t) / diesel_l in forma
chiusa (demo None: rapporto negativo
-1,138, vince anche a diesel gratuito),
None se il denominatore e' nullo o se
il rapporto e' negativo. E' una SOGLIA
MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa
vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (tonnellate <= 0, diesel per
tonnellata < 0, prezzi < 0, O&M < 0,
kWh per tonnellata < 0, superficie < 0,
quota_fv/f_autoconsumo < 0 o > 1,
kwp_per_m2 < 0, resa < 0, kWh termici
< 0, prezzo calore < 0, voci CAPEX < 0,
fattori CO2 < 0, WACC < 0, vita <= 0 o
non intera, tolleranza < 0) o se
risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON compostaggio
domestico (chilogrammi senza aerazione
forzata industriale, biofiltro o FV),
NON digestione anaerobica/biogas
(niente metano prodotto, solo aerobico),
NON discarica (due modi di compostare,
non di smaltire).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w868_helpers import (
        demo_calcoli,
        mh864_c_alt,
        mh864_c_base,
        mh864_c_diesel,
        mh864_calcola,
        mh864_capex_totale,
        mh864_co2_alt,
        mh864_co2_base,
        mh864_co2_evitata,
        mh864_csv,
        mh864_demo,
        mh864_demo_calcoli,
        mh864_diesel_l,
        mh864_e_aer,
        mh864_e_bio,
        mh864_e_deficit,
        mh864_e_domanda_alt,
        mh864_e_immessa,
        mh864_e_pv,
        mh864_e_pv_auto,
        mh864_e_th_rec,
        mh864_flussi,
        mh864_frazione,
        mh864_int_pos,
        mh864_kwp,
        mh864_nneg,
        mh864_num,
        mh864_om_totale,
        mh864_p_diesel_pareggio,
        mh864_payback,
        mh864_pos,
        mh864_ricavo_immissione,
        mh864_ricavo_termico,
        mh864_risparmio,
        mh864_sensibilita,
        mh864_tir,
        mh864_valida,
        mh864_van,
        mh864_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w868_helpers", os.path.join(_hf, "w868_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh864_c_alt = _mod.mh864_c_alt
    mh864_c_base = _mod.mh864_c_base
    mh864_c_diesel = _mod.mh864_c_diesel
    mh864_calcola = _mod.mh864_calcola
    mh864_capex_totale = _mod.mh864_capex_totale
    mh864_co2_alt = _mod.mh864_co2_alt
    mh864_co2_base = _mod.mh864_co2_base
    mh864_co2_evitata = _mod.mh864_co2_evitata
    mh864_csv = _mod.mh864_csv
    mh864_demo = _mod.mh864_demo
    mh864_demo_calcoli = _mod.mh864_demo_calcoli
    mh864_diesel_l = _mod.mh864_diesel_l
    mh864_e_aer = _mod.mh864_e_aer
    mh864_e_bio = _mod.mh864_e_bio
    mh864_e_deficit = _mod.mh864_e_deficit
    mh864_e_domanda_alt = _mod.mh864_e_domanda_alt
    mh864_e_immessa = _mod.mh864_e_immessa
    mh864_e_pv = _mod.mh864_e_pv
    mh864_e_pv_auto = _mod.mh864_e_pv_auto
    mh864_e_th_rec = _mod.mh864_e_th_rec
    mh864_flussi = _mod.mh864_flussi
    mh864_frazione = _mod.mh864_frazione
    mh864_int_pos = _mod.mh864_int_pos
    mh864_kwp = _mod.mh864_kwp
    mh864_nneg = _mod.mh864_nneg
    mh864_num = _mod.mh864_num
    mh864_om_totale = _mod.mh864_om_totale
    mh864_p_diesel_pareggio = _mod.mh864_p_diesel_pareggio
    mh864_payback = _mod.mh864_payback
    mh864_pos = _mod.mh864_pos
    mh864_ricavo_immissione = _mod.mh864_ricavo_immissione
    mh864_ricavo_termico = _mod.mh864_ricavo_termico
    mh864_risparmio = _mod.mh864_risparmio
    mh864_sensibilita = _mod.mh864_sensibilita
    mh864_tir = _mod.mh864_tir
    mh864_valida = _mod.mh864_valida
    mh864_van = _mod.mh864_van
    mh864_verdetto = _mod.mh864_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w868_helpers.py")
_UI_PATH = _risolvi("w868_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "3"
_VECCHIO_TAB = "tab86" + "3"
_VECCHIO_ST = "st86" + "3_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "t_anno": 20000.0,
    "diesel_l_anno": 80000.0,
    "c_diesel_eur_anno": 136000.0,
    "om_base_eur_anno": 200000.0,
    "c_base_eur_anno": 336000.0,
    "e_aer_kwh_anno": 300000.0,
    "e_bio_kwh_anno": 60000.0,
    "e_domanda_alt_kwh_anno": 360000.0,
    "kwp": 960.0,
    "e_pv_kwh_anno": 1056000.0,
    "e_pv_auto_kwh_anno": 316800.0,
    "e_immessa_kwh_anno": 739200.0,
    "e_deficit_kwh_anno": 43200.0,
    "ricavo_immissione_eur_anno": 59136.0,
    "e_th_rec_kwh_anno": 400000.0,
    "ricavo_termico_eur_anno": 24000.0,
    "om_alt_eur_anno": 180000.0,
    "c_alt_eur_anno": 108960.0,
    "risparmio_eur_anno": 227040.0,
    "capex_eur": 1956000.0,
    "co2_base_t_anno": 214.4,
    "co2_alt_t_anno": 10.8,
    "co2_evitata_t_anno": 203.6,
    "van": 873420.2361702773,
    "tir": 9.826740302247625,
    "payback": 9,
    "p_diesel_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh864_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh864_num(3, "x"), 3.0)
        self.assertEqual(mh864_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh864_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh864_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh864_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh864_pos(0, "x")
        with self.assertRaises(ValueError):
            mh864_pos(-1, "x")
        self.assertEqual(mh864_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh864_int_pos(20, "x"), 20)
        self.assertEqual(mh864_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh864_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh864_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh864_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh864_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh864_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh864_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_diesel_e_costo_base(self):
        self.assertEqual(mh864_diesel_l(20000, 4.0), 80000.0)
        self.assertEqual(mh864_c_diesel(80000.0, 1.70), 136000.0)
        self.assertEqual(mh864_om_totale(20000, 10), 200000.0)
        self.assertEqual(mh864_c_base(136000.0, 200000.0), 336000.0)

    def test_aer_bio_domanda_alt(self):
        self.assertEqual(mh864_e_aer(20000, 15), 300000.0)
        self.assertEqual(mh864_e_bio(20000, 3), 60000.0)
        self.assertEqual(mh864_e_domanda_alt(300000.0, 60000.0),
                         360000.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh864_kwp(8000, 0.60, 0.20), 960.0)
        self.assertEqual(mh864_e_pv(960.0, 1100), 1056000.0)
        self.assertEqual(mh864_e_pv_auto(1056000.0, 0.30, 360000.0),
                         316800.0)
        self.assertEqual(mh864_e_pv_auto(1056000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh864_e_immessa(1056000.0, 316800.0), 739200.0)
        self.assertEqual(mh864_e_deficit(360000.0, 316800.0), 43200.0)
        self.assertEqual(mh864_e_deficit(20000.0, 25000.0), 0.0)

    def test_recupero_termico_e_c_alt(self):
        self.assertEqual(mh864_e_th_rec(20000, 20), 400000.0)
        self.assertEqual(mh864_ricavo_termico(400000.0, 0.06), 24000.0)
        self.assertEqual(mh864_ricavo_immissione(739200.0, 0.08), 59136.0)
        self.assertAlmostEqual(
            mh864_c_alt(43200.0, 0.28, 59136.0, 24000.0, 180000.0),
            108960.0)
        self.assertAlmostEqual(mh864_risparmio(336000.0, 108960.0),
                               227040.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh864_capex_totale(500000, 400000, 960.0,
                                            1100),
                         1956000.0)
        self.assertEqual(mh864_capex_totale(500000, 400000, 0.0,
                                            1100),
                         900000.0)

    def test_co2_base_solo_diesel_alt_solo_deficit(self):
        cb = mh864_co2_base(80000.0, 2.68)
        self.assertAlmostEqual(cb, 214.4, places=4)
        ca = mh864_co2_alt(43200.0, 0.25)
        self.assertAlmostEqual(ca, 10.8, places=4)
        self.assertAlmostEqual(mh864_co2_evitata(cb, ca), 203.6, places=4)
        # L'immessa non sottrae CO2: alt conta solo il deficit.
        self.assertEqual(mh864_co2_alt(0.0, 0.25), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh864_flussi(1956000, 227040.0, 3),
                         [-1956000, 227040.0, 227040.0, 227040.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh864_van([-100, 60, 60], 0), 20.0)
        bc = mh864_demo_calcoli()
        self.assertAlmostEqual(mh864_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh864_demo_calcoli()
        tir = mh864_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh864_tir([-100, -10, -10]))
        self.assertIsNone(mh864_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh864_demo_calcoli()
        self.assertEqual(mh864_payback(bc["flussi"]), 9)
        self.assertIsNone(mh864_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh864_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh864_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:9]), -139680.0, places=2)
        self.assertAlmostEqual(sum(flussi[:10]), 87360.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh864_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh864_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh864_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh864_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh864_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh864_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh864_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_diesel_pareggio_demo_none_rapporto_negativo(self):
        bc = mh864_demo_calcoli()
        self.assertIsNone(bc["p_diesel_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a diesel gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["c_alt_eur_anno"] - bc["om_base_eur_anno"])
                        / bc["diesel_l_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["c_alt_eur_anno"] - bc["om_base_eur_anno"])
            / bc["diesel_l_anno"], -1.138, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_diesel_pareggio_positivo_zero_denominatore(self):
        self.assertEqual(mh864_p_diesel_pareggio(80000.0, 250000.0,
                                                200000.0), 0.625)
        self.assertEqual(mh864_p_diesel_pareggio(80000.0, 200000.0,
                                                200000.0), 0.0)
        self.assertIsNone(mh864_p_diesel_pareggio(0.0, 250000.0,
                                                 200000.0))
        self.assertIsNone(mh864_p_diesel_pareggio(80000.0, 108960.0,
                                                 200000.0))

    def test_valida_demo_ok(self):
        demo = mh864_demo()
        val = mh864_valida(*[demo[k] for k in (
            "t_anno", "diesel_l_per_t", "p_diesel", "om_base_per_t",
            "kwh_aer_per_t", "kwh_bio_per_t", "p_el", "sup_m2",
            "quota_fv", "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "kwh_th_per_t", "p_heat", "om_alt_per_t",
            "capex_capannone_eur", "capex_aer_bio_eur",
            "capex_fv_eur_kwp", "f_co2_el_t_mwh",
            "f_co2_diesel_kg_l", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonnellate_zero_no(self):
        kw = _demo_kwargs(t_anno=0)
        self.assertRaises(ValueError, mh864_calcola, **kw)

    def test_valida_quote_sopra_uno_no(self):
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh864_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh864_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh864_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh864_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_diesel=float("nan"))
        self.assertRaises(ValueError, mh864_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("t_anno", -1),
                              ("diesel_l_per_t", -1),
                              ("p_el", -0.01),
                              ("capex_aer_bio_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh864_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh864_calcola(mh864_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh864_calcola(dict(mh864_demo(), capex_aer_bio_eur=999999),
                           capex_aer_bio_eur=400000)
        self.assertEqual(bc["capex_eur"], 1956000.0)


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
        self.assertEqual(bc["payback"], 9)

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
            bc["c_diesel_eur_anno"] + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["e_immessa_kwh_anno"] * bc["p_immissione"]
            - bc["ricavo_termico_eur_anno"]
            + bc["om_alt_eur_anno"])

    def test_coerenza_p_diesel_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_diesel_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"] - bc["om_base_eur_anno"])
                        / bc["diesel_l_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh864_sensibilita(**mh864_demo())
        self.assertAlmostEqual(s["p_diesel_piu20"]["risparmio_eur_anno"],
                               254240.0, places=2)
        self.assertAlmostEqual(s["p_diesel_piu20"]["van"],
                               1212392.36, places=2)
        self.assertEqual(s["p_diesel_piu20"]["payback"], 8)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               79200.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               87007.06, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 12)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 900000.0)
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               203040.0, places=2)
        self.assertAlmostEqual(s["senza_recupero"]["van"],
                               574327.19, places=2)
        self.assertEqual(s["senza_recupero"]["payback"], 10)
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -1082579.76, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 18)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -202857.30, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               2584800.0, places=2)

    def test_marginale_con_capex_fv_alto(self):
        # CAPEX totale 2.916.000 (FV a 2.100 EUR/kWp):
        # VAN circa -86.580, entro la tolleranza del 10%
        # (291.600).
        bc = mh864_calcola(**_demo_kwargs(capex_fv_eur_kwp=2100))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -86579.76, places=2)

    def test_non_convente_con_capex_fv_altissimo(self):
        bc = mh864_calcola(**_demo_kwargs(capex_fv_eur_kwp=3000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -950579.76, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh864_calcola(**_demo_kwargs(quota_fv=0, kwh_aer_per_t=40,
                                          kwh_bio_per_t=10))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -100000.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh864_csv(bc, mh864_demo())
        for voce in ("t_anno", "diesel_l_anno",
                     "e_domanda_alt_kwh_anno", "p_diesel_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -1956000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (t/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh864_c_alt(360000.0, 0.28, 0.0, 24000.0, 180000.0)
        con = mh864_c_alt(43200.0, 0.28, 59136.0, 24000.0, 180000.0)
        self.assertAlmostEqual(senza - con, 360000.0 * 0.28 - 43200.0 * 0.28 + 59136.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh864_sensibilita(**mh864_demo())
        self.assertEqual(set(s.keys()),
                         {"p_diesel_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio",
                          "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh864_csv(bc, mh864_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("diesel_l_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh864_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh864_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh864_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["capex_eur"], 900000.0)
        bc = mh864_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def864\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh864_demo().keys()), lette - set(mh864_demo().keys()))
        self.assertEqual(lette, set(mh864_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc864\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc864\["([^"]+)"\]', src))
        attese = set(mh864_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab864:"), 1)
        self.assertTrue(src.startswith("    # W868"))

    def test_ui_tab864_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab864:"), 1)
        self.assertIn("def mh864_demo(", src_h)
        self.assertIn("def mh864_calcola(", src_h)
        self.assertIn("tab864", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Impianto di compostaggio: aerazione forzata + biofiltro + recupero calore + FV batte compostaggio tradizionale in cumuli aperti con rivoltamento diesel?", src)
        self.assertIn("♻️ Impianto di compostaggio: aerazione forzata + biofiltro + recupero calore + FV batte compostaggio tradizionale in cumuli aperti con rivoltamento diesel?", src)
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
        chiavi = re.findall(r'key="(st864_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st864_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st864_calcola"', src)
        self.assertIn('key="st864_csv"', src)
        self.assertIn('key="st864_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg864"), src.index(".paiac("))
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
