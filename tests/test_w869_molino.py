"""Test nuova scheda molino: motori
efficienti + inverter + aspirazione
efficiente + FV battono molino
tradizionale con motori vecchi +
aspirazione sempre accesa?

Business case annuo di un molino,
guidato dalle TONNELLATE all'anno di
cereale macinato (demo 12.000 t/anno):
motori vecchi = t x kWh/t (demo
12.000 x 55 = 660.000 kWh/anno),
aspirazione base 180.000 kWh/anno,
domanda base 840.000 kWh/anno, costo
base 244.800 EUR/anno; motori
efficienti 504.000 kWh/anno,
aspirazione efficiente 90.000
kWh/anno, domanda alt 594.000
kWh/anno; kWp = sup x kwp/m2 (demo
400 kWp); E_pv 440.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
domanda alt) (demo 264.000 kWh/anno);
immessa 176.000 kWh/anno; deficit
330.000 kWh/anno; ricavo immissione
14.080 EUR/anno; O&M alternativa
45.000 EUR/anno; C_alt 103.520
EUR/anno; risparmio 141.280 EUR/anno;
CAPEX 320.000 + 120.000 + 400 x 450 =
620.000 EUR; CO2 base = domanda base
x 0,30 / 1000 = 252,00 t/anno; CO2 alt
= deficit / 1000 x 0,30 = 99,00
t/anno (immessa senza credito CO2);
CO2 evitata 153,00 t/anno; flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo elettrico di
pareggio p_el_star = (om_alt -
ricavo_immissione - om_base) /
(E_base_tot - E_deficit) in forma
chiusa (demo None: rapporto negativo
-0,05701961, vince anche a elettricita'
gratuita), None se il denominatore e'
nullo o se il rapporto e' negativo. E'
una SOGLIA MINIMA sui soli costi annui
(CAPEX escluso): sopra di essa
l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (tonnellate <= 0, kWh per
tonnellata < 0, aspirazioni < 0, prezzi
< 0, O&M < 0, superficie < 0, kwp per
m2 < 0, resa < 0, f_autoconsumo < 0 o
> 1, voci CAPEX < 0, fattore CO2 < 0,
WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON pastificio
(niente essiccazione di pasta), NON
oleificio/frantoio (niente olio
estratto), NON mangimificio (niente
essiccazione di mangime); qui solo
macinazione di cereale.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w869_helpers import (
        demo_calcoli,
        mh865_c_alt,
        mh865_c_base,
        mh865_calcola,
        mh865_capex_totale,
        mh865_co2_alt,
        mh865_co2_base,
        mh865_co2_evitata,
        mh865_csv,
        mh865_demo,
        mh865_demo_calcoli,
        mh865_e_alt,
        mh865_e_base,
        mh865_e_base_tot,
        mh865_e_deficit,
        mh865_e_domanda_alt,
        mh865_e_immessa,
        mh865_e_pv,
        mh865_e_pv_auto,
        mh865_flussi,
        mh865_frazione,
        mh865_int_pos,
        mh865_kwp,
        mh865_nneg,
        mh865_num,
        mh865_p_el_pareggio,
        mh865_payback,
        mh865_pos,
        mh865_ricavo_immissione,
        mh865_risparmio,
        mh865_sensibilita,
        mh865_tir,
        mh865_valida,
        mh865_van,
        mh865_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w869_helpers", os.path.join(_hf, "w869_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh865_c_alt = _mod.mh865_c_alt
    mh865_c_base = _mod.mh865_c_base
    mh865_calcola = _mod.mh865_calcola
    mh865_capex_totale = _mod.mh865_capex_totale
    mh865_co2_alt = _mod.mh865_co2_alt
    mh865_co2_base = _mod.mh865_co2_base
    mh865_co2_evitata = _mod.mh865_co2_evitata
    mh865_csv = _mod.mh865_csv
    mh865_demo = _mod.mh865_demo
    mh865_demo_calcoli = _mod.mh865_demo_calcoli
    mh865_e_alt = _mod.mh865_e_alt
    mh865_e_base = _mod.mh865_e_base
    mh865_e_base_tot = _mod.mh865_e_base_tot
    mh865_e_deficit = _mod.mh865_e_deficit
    mh865_e_domanda_alt = _mod.mh865_e_domanda_alt
    mh865_e_immessa = _mod.mh865_e_immessa
    mh865_e_pv = _mod.mh865_e_pv
    mh865_e_pv_auto = _mod.mh865_e_pv_auto
    mh865_flussi = _mod.mh865_flussi
    mh865_frazione = _mod.mh865_frazione
    mh865_int_pos = _mod.mh865_int_pos
    mh865_kwp = _mod.mh865_kwp
    mh865_nneg = _mod.mh865_nneg
    mh865_num = _mod.mh865_num
    mh865_p_el_pareggio = _mod.mh865_p_el_pareggio
    mh865_payback = _mod.mh865_payback
    mh865_pos = _mod.mh865_pos
    mh865_ricavo_immissione = _mod.mh865_ricavo_immissione
    mh865_risparmio = _mod.mh865_risparmio
    mh865_sensibilita = _mod.mh865_sensibilita
    mh865_tir = _mod.mh865_tir
    mh865_valida = _mod.mh865_valida
    mh865_van = _mod.mh865_van
    mh865_verdetto = _mod.mh865_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w869_helpers.py")
_UI_PATH = _risolvi("w869_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "4"
_VECCHIO_TAB = "tab86" + "4"
_VECCHIO_ST = "st86" + "4_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "e_base_kwh_anno": 660000.0,
    "e_base_tot_kwh_anno": 840000.0,
    "c_base_eur_anno": 244800.0,
    "e_alt_kwh_anno": 504000.0,
    "e_domanda_alt_kwh_anno": 594000.0,
    "kwp": 400.0,
    "e_pv_kwh_anno": 440000.0,
    "e_pv_auto_kwh_anno": 264000.0,
    "e_immessa_kwh_anno": 176000.0,
    "e_deficit_kwh_anno": 330000.0,
    "ricavo_immissione_eur_anno": 14080.0,
    "c_alt_eur_anno": 103520.0,
    "risparmio_eur_anno": 141280.0,
    "capex_eur": 620000.0,
    "co2_base_t_anno": 252.0,
    "co2_alt_t_anno": 99.0,
    "co2_evitata_t_anno": 153.0,
    "van": 1140661.0771940486,
    "tir": 22.386192664907234,
    "payback": 5,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh865_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh865_num(3, "x"), 3.0)
        self.assertEqual(mh865_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh865_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh865_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh865_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh865_pos(0, "x")
        with self.assertRaises(ValueError):
            mh865_pos(-1, "x")
        self.assertEqual(mh865_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh865_int_pos(20, "x"), 20)
        self.assertEqual(mh865_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh865_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh865_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh865_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh865_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh865_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh865_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_motori_e_costo_base(self):
        self.assertEqual(mh865_e_base(12000, 55), 660000.0)
        self.assertEqual(mh865_e_base_tot(660000.0, 180000.0), 840000.0)
        self.assertEqual(mh865_c_base(840000.0, 0.22, 60000), 244800.0)

    def test_motori_alt_e_domanda_alt(self):
        self.assertEqual(mh865_e_alt(12000, 42), 504000.0)
        self.assertEqual(mh865_e_domanda_alt(504000.0, 90000.0),
                         594000.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh865_kwp(2000, 0.20), 400.0)
        self.assertEqual(mh865_e_pv(400.0, 1100), 440000.0)
        self.assertEqual(mh865_e_pv_auto(440000.0, 0.60, 594000.0),
                         264000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh865_e_pv_auto(440000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh865_e_immessa(440000.0, 264000.0), 176000.0)
        self.assertEqual(mh865_e_deficit(594000.0, 264000.0), 330000.0)
        self.assertEqual(mh865_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh865_ricavo_immissione(176000.0, 0.08), 14080.0)
        self.assertAlmostEqual(
            mh865_c_alt(330000.0, 0.22, 14080.0, 45000.0),
            103520.0)
        self.assertAlmostEqual(mh865_risparmio(244800.0, 103520.0),
                               141280.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh865_capex_totale(320000, 120000, 400.0,
                                            450),
                         620000.0)
        self.assertEqual(mh865_capex_totale(320000, 120000, 0.0,
                                            450),
                         440000.0)

    def test_co2_base_su_domanda_alt_solo_deficit(self):
        cb = mh865_co2_base(840000.0, 0.30)
        self.assertAlmostEqual(cb, 252.0, places=4)
        ca = mh865_co2_alt(330000.0, 0.30)
        self.assertAlmostEqual(ca, 99.0, places=4)
        self.assertAlmostEqual(mh865_co2_evitata(cb, ca), 153.0, places=4)
        # L'immessa non sottrae CO2: alt conta solo il deficit.
        self.assertEqual(mh865_co2_alt(0.0, 0.30), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh865_flussi(620000, 141280.0, 3),
                         [-620000, 141280.0, 141280.0, 141280.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh865_van([-100, 60, 60], 0), 20.0)
        bc = mh865_demo_calcoli()
        self.assertAlmostEqual(mh865_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh865_demo_calcoli()
        tir = mh865_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh865_tir([-100, -10, -10]))
        self.assertIsNone(mh865_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh865_demo_calcoli()
        self.assertEqual(mh865_payback(bc["flussi"]), 5)
        self.assertIsNone(mh865_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh865_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh865_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:5]), -54880.0, places=2)
        self.assertAlmostEqual(sum(flussi[:6]), 86400.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh865_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh865_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh865_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh865_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh865_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh865_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh865_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_el_pareggio_demo_none_rapporto_negativo(self):
        bc = mh865_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a elettricita' gratuita, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["om_alt_eur_anno"]
                         - bc["ricavo_immissione_eur_anno"]
                         - bc["om_base_eur_anno"])
                        / (bc["e_base_tot_kwh_anno"]
                           - bc["e_deficit_kwh_anno"]), 0.0)
        self.assertAlmostEqual(
            (bc["om_alt_eur_anno"]
             - bc["ricavo_immissione_eur_anno"]
             - bc["om_base_eur_anno"])
            / (bc["e_base_tot_kwh_anno"]
               - bc["e_deficit_kwh_anno"]), -0.05701961, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_el_pareggio_positivo_zero_denominatore(self):
        self.assertEqual(mh865_p_el_pareggio(840000.0, 330000.0,
                                            60000.0, 200000.0,
                                            14080.0), 0.24690196078431373)
        # Rapporto zero: om_alt - ricavo - om_base = 0.
        self.assertEqual(mh865_p_el_pareggio(840000.0, 330000.0,
                                            60000.0, 74080.0,
                                            14080.0), 0.0)
        self.assertIsNone(mh865_p_el_pareggio(330000.0, 330000.0,
                                             60000.0, 45000.0,
                                             14080.0))
        self.assertIsNone(mh865_p_el_pareggio(840000.0, 330000.0,
                                             60000.0, 45000.0,
                                             14080.0))

    def test_valida_demo_ok(self):
        demo = mh865_demo()
        val = mh865_valida(*[demo[k] for k in (
            "t_anno", "kwh_base_per_t", "asp_base_kwh_anno", "p_el",
            "om_base_eur_anno", "kwh_alt_per_t", "asp_alt_kwh_anno",
            "sup_m2", "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno", "capex_motori_eur",
            "capex_asp_eur", "capex_fv_eur_kwp", "f_co2_el_kg_kwh",
            "wacc_pct", "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonnellate_zero_no(self):
        kw = _demo_kwargs(t_anno=0)
        self.assertRaises(ValueError, mh865_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh865_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh865_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh865_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh865_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("t_anno", -1),
                              ("kwh_base_per_t", -1),
                              ("p_el", -0.01),
                              ("capex_asp_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh865_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh865_calcola(mh865_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh865_calcola(dict(mh865_demo(), capex_asp_eur=999999),
                           capex_asp_eur=120000)
        self.assertEqual(bc["capex_eur"], 620000.0)


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
            bc["e_base_tot_kwh_anno"] * bc["p_el"]
            + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["ricavo_immissione_eur_anno"]
            + bc["om_alt_eur_anno"])

    def test_coerenza_p_el_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertLess((bc["om_alt_eur_anno"]
                         - bc["ricavo_immissione_eur_anno"]
                         - bc["om_base_eur_anno"])
                        / (bc["e_base_tot_kwh_anno"]
                           - bc["e_deficit_kwh_anno"]), 0.0)

    def test_sensibilita_valori(self):
        s = mh865_sensibilita(**mh865_demo())
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               163720.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               1420313.08, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               69120.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               421387.98, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 7)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 440000.0)
        self.assertAlmostEqual(s["kwh_alt_55"]["risparmio_eur_anno"],
                               106960.0, places=2)
        self.assertAlmostEqual(s["kwh_alt_55"]["van"],
                               712958.02, places=2)
        self.assertEqual(s["kwh_alt_55"]["payback"], 6)
        self.assertEqual(s["kwh_alt_55"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               520661.08, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 9)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               470926.71, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               2205600.0, places=2)

    def test_marginale_con_capex_motori_alto(self):
        # CAPEX totale 1.800.000 (motori a 1.500.000):
        # VAN circa -39.339, entro la tolleranza del 10%
        # (180.000).
        bc = mh865_calcola(**_demo_kwargs(capex_motori_eur=1500000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -39338.92, places=2)

    def test_non_convente_con_capex_motori_altissimo(self):
        bc = mh865_calcola(**_demo_kwargs(capex_motori_eur=2500000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -1039338.92, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh865_calcola(**_demo_kwargs(om_alt_eur_anno=300000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -113720.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh865_csv(bc, mh865_demo())
        for voce in ("t_anno", "e_base_tot_kwh_anno",
                     "e_domanda_alt_kwh_anno", "p_el_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -620000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (t/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh865_c_alt(594000.0, 0.22, 0.0, 45000.0)
        con = mh865_c_alt(330000.0, 0.22, 14080.0, 45000.0)
        self.assertAlmostEqual(senza - con, 594000.0 * 0.22 - 330000.0 * 0.22 + 14080.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh865_sensibilita(**mh865_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_piu20", "senza_fv",
                          "kwh_alt_55", "capex_doppio",
                          "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh865_csv(bc, mh865_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_tot_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh865_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh865_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh865_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 440000.0)
        bc = mh865_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def865\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh865_demo().keys()), lette - set(mh865_demo().keys()))
        self.assertEqual(lette, set(mh865_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc865\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc865\["([^"]+)"\]', src))
        attese = set(mh865_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab865:"), 1)
        self.assertTrue(src.startswith("    # W869"))

    def test_ui_tab865_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab865:"), 1)
        self.assertIn("def mh865_demo(", src_h)
        self.assertIn("def mh865_calcola(", src_h)
        self.assertIn("tab865", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Molino: motori efficienti + inverter + aspirazione efficiente + FV battono molino tradizionale con motori vecchi + aspirazione sempre accesa?", src)
        self.assertIn("🌾 Molino: motori efficienti + inverter + aspirazione efficiente + FV battono molino tradizionale con motori vecchi + aspirazione sempre accesa?", src)
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
        chiavi = re.findall(r'key="(st865_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st865_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st865_calcola"', src)
        self.assertIn('key="st865_csv"', src)
        self.assertIn('key="st865_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg865"), src.index(".paiac("))
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
