"""Test nuova scheda cava / frantumazione
inerti: frantoi elettrici efficienti +
nastri con inverter + FV battono
frantumazione diesel + nastri
tradizionali?

Business case annuo di una cava /
frantumazione inerti, guidato dalle
TONNELLATE all'anno di inerte
frantumato (demo 200.000 t/anno):
diesel base = t x l/t (demo 200.000 x
0,45 = 90.000 litri/anno), costo diesel
base 153.000 EUR/anno; nastri base
200.000 x 1,2 = 240.000 kWh/anno,
costo energia nastri base 52.800
EUR/anno; O&M base 60.000 EUR/anno;
costo base 265.800 EUR/anno; frantoi
elettrici 200.000 x 1,8 = 360.000
kWh/anno; nastri con inverter 200.000
x 0,7 = 140.000 kWh/anno; elettricita'
alternativa 500.000 kWh/anno; kWp = sup
x kwp/m2 (demo 300 kWp); E_pv 330.000
kWh/anno; E_pv_auto = min(E_pv x
f_autoconsumo, E_alt) (demo 198.000
kWh/anno); immessa 132.000 kWh/anno;
deficit 302.000 kWh/anno; ricavo
immissione 10.560 EUR/anno; O&M
alternativa 45.000 EUR/anno; C_alt
100.880 EUR/anno; risparmio 164.920
EUR/anno; CAPEX 400.000 + 60.000 +
300 x 900 = 730.000 EUR; CO2 base =
(litri x 2,68 + E_nastri_base x 0,35) /
1000 = 325,20 t/anno; CO2 alt =
(deficit x 0,35) / 1000 = 105,70
t/anno (immessa senza credito CO2);
CO2 evitata 219,50 t/anno; flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100
dentro); TIR per bisezione; payback
(primo anno con cumulato >= 0); prezzo
diesel di pareggio p_diesel_star =
(deficit x p_el - ricavo_immissione +
om_alt - E_nastri_base x p_el -
om_base) / litri in forma chiusa (demo
None: rapporto negativo -0,13244,
vince anche a diesel gratuito), None se
il denominatore e' nullo o negativo o
se il rapporto e' negativo. E' una
SOGLIA MINIMA sui soli costi annui
(CAPEX escluso): sopra di essa
l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (tonnellate <= 0, litri per
tonnellata < 0, prezzi < 0, O&M < 0,
superficie < 0, kwp per m2 < 0, resa <
0, f_autoconsumo < 0 o > 1, voci CAPEX <
0, fattori CO2 < 0, WACC < 0, vita <= 0
o non intera, tolleranza < 0) o se
risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON frantoio
oleario (niente olive frante), NON
molino (niente cereali macinati), NON
miniera sotterranea (niente estrazione
in sotterraneo); qui solo frantumazione
/ vagliatura di inerti da cava con
frantoi + nastri + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w873_helpers import (
        demo_calcoli,
        mh869_c_alt,
        mh869_c_base,
        mh869_calcola,
        mh869_capex_totale,
        mh869_co2_alt,
        mh869_co2_base,
        mh869_co2_evitata,
        mh869_csv,
        mh869_demo,
        mh869_demo_calcoli,
        mh869_e_alt,
        mh869_e_frantoi,
        mh869_e_nastri_alt,
        mh869_e_nastri_base,
        mh869_e_deficit,
        mh869_e_immessa,
        mh869_e_pv,
        mh869_e_pv_auto,
        mh869_flussi,
        mh869_frazione,
        mh869_int_pos,
        mh869_kwp,
        mh869_litri_diesel,
        mh869_nneg,
        mh869_num,
        mh869_p_diesel_pareggio,
        mh869_payback,
        mh869_pos,
        mh869_ricavo_immissione,
        mh869_risparmio,
        mh869_sensibilita,
        mh869_tir,
        mh869_valida,
        mh869_van,
        mh869_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w873_helpers", os.path.join(_hf, "w873_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh869_c_alt = _mod.mh869_c_alt
    mh869_c_base = _mod.mh869_c_base
    mh869_calcola = _mod.mh869_calcola
    mh869_capex_totale = _mod.mh869_capex_totale
    mh869_co2_alt = _mod.mh869_co2_alt
    mh869_co2_base = _mod.mh869_co2_base
    mh869_co2_evitata = _mod.mh869_co2_evitata
    mh869_csv = _mod.mh869_csv
    mh869_demo = _mod.mh869_demo
    mh869_demo_calcoli = _mod.mh869_demo_calcoli
    mh869_e_alt = _mod.mh869_e_alt
    mh869_e_frantoi = _mod.mh869_e_frantoi
    mh869_e_nastri_alt = _mod.mh869_e_nastri_alt
    mh869_e_nastri_base = _mod.mh869_e_nastri_base
    mh869_e_deficit = _mod.mh869_e_deficit
    mh869_e_immessa = _mod.mh869_e_immessa
    mh869_e_pv = _mod.mh869_e_pv
    mh869_e_pv_auto = _mod.mh869_e_pv_auto
    mh869_flussi = _mod.mh869_flussi
    mh869_frazione = _mod.mh869_frazione
    mh869_int_pos = _mod.mh869_int_pos
    mh869_kwp = _mod.mh869_kwp
    mh869_litri_diesel = _mod.mh869_litri_diesel
    mh869_nneg = _mod.mh869_nneg
    mh869_num = _mod.mh869_num
    mh869_p_diesel_pareggio = _mod.mh869_p_diesel_pareggio
    mh869_payback = _mod.mh869_payback
    mh869_pos = _mod.mh869_pos
    mh869_ricavo_immissione = _mod.mh869_ricavo_immissione
    mh869_risparmio = _mod.mh869_risparmio
    mh869_sensibilita = _mod.mh869_sensibilita
    mh869_tir = _mod.mh869_tir
    mh869_valida = _mod.mh869_valida
    mh869_van = _mod.mh869_van
    mh869_verdetto = _mod.mh869_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w873_helpers.py")
_UI_PATH = _risolvi("w873_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "8"
_VECCHIO_TAB = "tab86" + "8"
_VECCHIO_ST = "st86" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")
_TITLES_SNAPSHOT = os.path.join(_HF_FALLBACK, "w873_titles.txt")

_DEMO = {
    "litri_diesel_l_anno": 90000.0,
    "e_nastri_base_kwh_anno": 240000.0,
    "c_base_eur_anno": 265800.0,
    "e_frantoi_kwh_anno": 360000.0,
    "e_nastri_alt_kwh_anno": 140000.0,
    "e_alt_kwh_anno": 500000.0,
    "kwp": 300.0,
    "e_pv_kwh_anno": 330000.0,
    "e_pv_auto_kwh_anno": 198000.0,
    "e_immessa_kwh_anno": 132000.0,
    "e_deficit_kwh_anno": 302000.0,
    "ricavo_immissione_eur_anno": 10560.0,
    "c_alt_eur_anno": 100880.0,
    "risparmio_eur_anno": 164920.0,
    "capex_eur": 730000.0,
    "co2_base_t_anno": 325.2,
    "co2_alt_t_anno": 105.7,
    "co2_evitata_t_anno": 219.5,
    "van": 1325267.7296916936,
    "tir": 22.180729357742113,
    "payback": 5,
    "p_diesel_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh869_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh869_num(3, "x"), 3.0)
        self.assertEqual(mh869_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh869_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh869_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh869_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh869_pos(0, "x")
        with self.assertRaises(ValueError):
            mh869_pos(-1, "x")
        self.assertEqual(mh869_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh869_int_pos(20, "x"), 20)
        self.assertEqual(mh869_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh869_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh869_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh869_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh869_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh869_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh869_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_diesel_e_costo_base(self):
        self.assertEqual(mh869_litri_diesel(200000, 0.45), 90000.0)
        self.assertEqual(mh869_e_nastri_base(200000, 1.2), 240000.0)
        self.assertEqual(mh869_c_base(90000.0, 1.70, 240000.0, 0.22,
                                       60000), 265800.0)

    def test_frantoi_nastri_alt_somma(self):
        self.assertEqual(mh869_e_frantoi(200000, 1.8), 360000.0)
        self.assertEqual(mh869_e_nastri_alt(200000, 0.7), 140000.0)
        self.assertEqual(mh869_e_alt(360000.0, 140000.0), 500000.0)
        # L'inverter RIDUCE i nastri, non li azzera:
        # 0,7 resta sopra zero anche a parita' di base 1,2.
        self.assertGreater(mh869_e_nastri_alt(200000, 0.7), 0.0)
        self.assertLess(mh869_e_nastri_alt(200000, 0.7),
                        mh869_e_nastri_base(200000, 1.2))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh869_kwp(1500, 0.20), 300.0)
        self.assertEqual(mh869_e_pv(300.0, 1100), 330000.0)
        self.assertEqual(mh869_e_pv_auto(330000.0, 0.60, 500000.0),
                         198000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh869_e_pv_auto(330000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh869_e_immessa(330000.0, 198000.0), 132000.0)
        self.assertEqual(mh869_e_deficit(500000.0, 198000.0), 302000.0)
        self.assertEqual(mh869_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh869_ricavo_immissione(132000.0, 0.08), 10560.0)
        self.assertAlmostEqual(
            mh869_c_alt(302000.0, 0.22, 10560.0, 45000.0),
            100880.0)
        self.assertAlmostEqual(mh869_risparmio(265800.0, 100880.0),
                               164920.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh869_capex_totale(400000, 60000, 300.0,
                                            900),
                         730000.0)
        self.assertEqual(mh869_capex_totale(400000, 60000, 0.0,
                                            900),
                         460000.0)

    def test_co2_base_e_alt(self):
        cb = mh869_co2_base(90000.0, 2.68, 240000.0, 0.35)
        self.assertAlmostEqual(cb, 325.2, places=4)
        ca = mh869_co2_alt(302000.0, 0.35)
        self.assertAlmostEqual(ca, 105.7, places=4)
        self.assertAlmostEqual(mh869_co2_evitata(cb, ca), 219.5, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh869_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh869_flussi(730000, 164920.0, 3),
                         [-730000, 164920.0, 164920.0, 164920.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh869_van([-100, 60, 60], 0), 20.0)
        bc = mh869_demo_calcoli()
        self.assertAlmostEqual(mh869_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh869_demo_calcoli()
        tir = mh869_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh869_tir([-100, -10, -10]))
        self.assertIsNone(mh869_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh869_demo_calcoli()
        self.assertEqual(mh869_payback(bc["flussi"]), 5)
        self.assertIsNone(mh869_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh869_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh869_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:5]), -70320.0, places=2)
        self.assertAlmostEqual(sum(flussi[:6]), 94600.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh869_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh869_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh869_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh869_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh869_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh869_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh869_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_diesel_pareggio_demo_none_rapporto_negativo(self):
        bc = mh869_demo_calcoli()
        self.assertIsNone(bc["p_diesel_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a diesel gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_nastri_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["litri_diesel_l_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["e_deficit_kwh_anno"] * bc["p_el"]
             - bc["ricavo_immissione_eur_anno"]
             + bc["om_alt_eur_anno"]
             - bc["e_nastri_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["litri_diesel_l_anno"], -0.13244444444444445, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_diesel_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh869_p_diesel_pareggio(90000.0, 240000.0, 302000.0,
                                    0.22, 10560.0, 60000.0, 200000.0),
            1.5897777777777777, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh869_p_diesel_pareggio(90000.0, 240000.0,
                                                302000.0, 0.22, 10560.0,
                                                60000.0, 56920.0),
                         0.0)
        self.assertIsNone(mh869_p_diesel_pareggio(0.0, 240000.0,
                                                  302000.0, 0.22, 10560.0,
                                                  60000.0, 45000.0))
        self.assertIsNone(mh869_p_diesel_pareggio(90000.0, 240000.0,
                                                  302000.0, 0.22, 10560.0,
                                                  60000.0, 45000.0))

    def test_valida_demo_ok(self):
        demo = mh869_demo()
        val = mh869_valida(*[demo[k] for k in (
            "t_anno", "l_diesel_per_t", "p_diesel",
            "e_nastri_base_per_t", "p_el", "om_base_eur_anno",
            "e_frantoi_per_t", "e_nastri_alt_per_t", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_frantoi_eur", "capex_inverter_eur",
            "capex_fv_eur_kwp", "f_co2_diesel_kg_l",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonnellate_zero_no(self):
        kw = _demo_kwargs(t_anno=0)
        self.assertRaises(ValueError, mh869_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh869_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh869_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh869_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_diesel=float("nan"))
        self.assertRaises(ValueError, mh869_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("t_anno", -1),
                              ("l_diesel_per_t", -1),
                              ("p_diesel", -0.01),
                              ("capex_frantoi_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh869_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh869_calcola(mh869_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh869_calcola(dict(mh869_demo(), capex_frantoi_eur=999999),
                           capex_frantoi_eur=400000)
        self.assertEqual(bc["capex_eur"], 730000.0)


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
        self.assertEqual(bc["payback"], 5)

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
            bc["litri_diesel_l_anno"] * bc["p_diesel"]
            + bc["e_nastri_base_kwh_anno"] * bc["p_el"]
            + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["ricavo_immissione_eur_anno"]
            + bc["om_alt_eur_anno"])

    def test_coerenza_p_diesel_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_diesel_pareggio"])
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_nastri_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["litri_diesel_l_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh869_sensibilita(**mh869_demo())
        self.assertAlmostEqual(s["p_diesel_piu20"]["risparmio_eur_anno"],
                               195520.0, places=2)
        self.assertAlmostEqual(s["p_diesel_piu20"]["van"],
                               1706611.37, places=2)
        self.assertEqual(s["p_diesel_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               162192.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               1291270.82, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               110800.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               920812.91, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 5)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 460000.0)
        self.assertAlmostEqual(s["senza_inverter"]["risparmio_eur_anno"],
                               142920.0, places=2)
        self.assertAlmostEqual(s["senza_inverter"]["van"],
                               1051099.10, places=2)
        self.assertEqual(s["senza_inverter"]["payback"], 6)
        self.assertEqual(s["senza_inverter"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               595267.73, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 9)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               543468.52, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               2568400.0, places=2)

    def test_marginale_con_capex_frantoi_alto(self):
        # CAPEX totale 2.230.000 (frantoi a 1.900.000):
        # VAN circa -174.732, entro la tolleranza del 10%
        # (223.000).
        bc = mh869_calcola(**_demo_kwargs(capex_frantoi_eur=1900000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -174732.27, places=2)

    def test_non_convente_con_capex_frantoi_altissimo(self):
        bc = mh869_calcola(**_demo_kwargs(capex_frantoi_eur=2100000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -374732.27, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh869_calcola(**_demo_kwargs(om_alt_eur_anno=400000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -190080.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh869_csv(bc, mh869_demo())
        for voce in ("t_anno", "litri_diesel_l_anno",
                     "e_nastri_base_kwh_anno", "p_diesel_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -730000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (t/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh869_c_alt(500000.0, 0.22, 0.0, 45000.0)
        con = mh869_c_alt(302000.0, 0.22, 10560.0, 45000.0)
        self.assertAlmostEqual(senza - con, 500000.0 * 0.22 - 302000.0 * 0.22 + 10560.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh869_sensibilita(**mh869_demo())
        self.assertEqual(set(s.keys()),
                         {"p_diesel_piu20", "p_el_piu20",
                          "senza_fv", "senza_inverter",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh869_csv(bc, mh869_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("litri_diesel_l_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh869_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh869_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh869_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 460000.0)
        bc = mh869_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def869\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh869_demo().keys()), lette - set(mh869_demo().keys()))
        self.assertEqual(lette, set(mh869_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc869\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc869\["([^"]+)"\]', src))
        attese = set(mh869_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli pre-apply: la copia di
        # lavoro del repo ha questo numero di blocchi
        # scheda prima dell'aggiunta di questa scheda.
        # Dopo l'apply il conteggio sale di uno: il
        # bump dell'apply deve aggiornare anche questo
        # assert, come fa per gli altri test di
        # conteggio, altrimenti il test fallisce
        # contro il repo aggiornato.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 890)
        elif os.path.exists(_TITLES_SNAPSHOT):
            with open(_TITLES_SNAPSHOT, encoding="utf-8") as f:
                self.assertEqual(sum(1 for _ in f), 868)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab869:"), 1)
        self.assertTrue(src.startswith("    # W873"))

    def test_ui_tab869_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab869:"), 1)
        self.assertIn("def mh869_demo(", src_h)
        self.assertIn("def mh869_calcola(", src_h)
        self.assertIn("tab869", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Cava / frantumazione inerti: frantoi elettrici efficienti + nastri con inverter + FV battono frantumazione diesel + nastri tradizionali?", src)
        self.assertIn("⛏️ Cava / frantumazione inerti: frantoi elettrici efficienti + nastri con inverter + FV battono frantumazione diesel + nastri tradizionali?", src)
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
        chiavi = re.findall(r'key="(st869_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st869_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st869_calcola"', src)
        self.assertIn('key="st869_csv"', src)
        self.assertIn('key="st869_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg869"), src.index(".paiac("))
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
