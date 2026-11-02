"""Test nuova scheda stampaggio plastica a
iniezione: presse servo-elettriche +
free-cooling stampi + FV battono presse
idrauliche tradizionali + essiccazione a
gas?

Business case annuo di uno stampaggio
plastica a iniezione, guidato dalle
TONNELLATE all'anno di granulo stampato
(demo 1.200 t/anno): elettricita' base =
t x kWh/t (demo 1.200 x 800 = 960.000
kWh/anno), gas base 1.200 x 150 =
180.000 kWh/anno, costo base 287.400
EUR/anno; recupero calore 0,50: gas
alternativo 90.000 kWh/anno;
elettricita' alternativa 1.200 x 350 =
420.000 kWh/anno; kWp = sup x kwp/m2
(demo 400 kWp); E_pv 440.000
kWh/anno; E_pv_auto = min(E_pv x
f_autoconsumo, E_alt) (demo 264.000
kWh/anno); immessa 176.000 kWh/anno;
deficit 156.000 kWh/anno; ricavo
immissione 14.080 EUR/anno; O&M
alternativa 90.000 EUR/anno; C_alt
118.340 EUR/anno; risparmio 169.060
EUR/anno; CAPEX 500.000 + 80.000 +
400 x 450 = 760.000 EUR; CO2 base =
(gas base x 0,20 + E_base x 0,30) /
1000 = 324,00 t/anno; CO2 alt =
(gas alt x 0,20 + deficit x 0,30) /
1000 = 64,80 t/anno (immessa senza
credito CO2); CO2 evitata 259,20
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt - E_base x
p_el - om_base) / (gas_base - gas_alt)
in forma chiusa (demo None: rapporto
negativo -1,78844, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (tonnellate <= 0, kWh per
tonnellata < 0, prezzi < 0, O&M < 0,
f_recupero < 0 o > 1, superficie < 0,
kwp per m2 < 0, resa < 0,
f_autoconsumo < 0 o > 1, voci CAPEX <
0, fattori CO2 < 0, WACC < 0, vita <= 0
o non intera, tolleranza < 0) o se
risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON estrusione
(niente profilo continuo estruso),
NON soffiaggio (niente corpi cavi
soffiati), NON termoformatura (niente
lastre formate); qui solo stampaggio a
iniezione: presse + essiccazione a gas
+ free-cooling stampi + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w872_helpers import (
        demo_calcoli,
        mh868_c_alt,
        mh868_c_base,
        mh868_calcola,
        mh868_capex_totale,
        mh868_co2_alt,
        mh868_co2_base,
        mh868_co2_evitata,
        mh868_csv,
        mh868_demo,
        mh868_demo_calcoli,
        mh868_e_alt,
        mh868_e_base,
        mh868_e_deficit,
        mh868_e_immessa,
        mh868_e_pv,
        mh868_e_pv_auto,
        mh868_flussi,
        mh868_frazione,
        mh868_gas_alt,
        mh868_gas_base,
        mh868_int_pos,
        mh868_kwp,
        mh868_nneg,
        mh868_num,
        mh868_p_gas_pareggio,
        mh868_payback,
        mh868_pos,
        mh868_ricavo_immissione,
        mh868_risparmio,
        mh868_sensibilita,
        mh868_tir,
        mh868_valida,
        mh868_van,
        mh868_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w872_helpers", os.path.join(_hf, "w872_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh868_c_alt = _mod.mh868_c_alt
    mh868_c_base = _mod.mh868_c_base
    mh868_calcola = _mod.mh868_calcola
    mh868_capex_totale = _mod.mh868_capex_totale
    mh868_co2_alt = _mod.mh868_co2_alt
    mh868_co2_base = _mod.mh868_co2_base
    mh868_co2_evitata = _mod.mh868_co2_evitata
    mh868_csv = _mod.mh868_csv
    mh868_demo = _mod.mh868_demo
    mh868_demo_calcoli = _mod.mh868_demo_calcoli
    mh868_e_alt = _mod.mh868_e_alt
    mh868_e_base = _mod.mh868_e_base
    mh868_e_deficit = _mod.mh868_e_deficit
    mh868_e_immessa = _mod.mh868_e_immessa
    mh868_e_pv = _mod.mh868_e_pv
    mh868_e_pv_auto = _mod.mh868_e_pv_auto
    mh868_flussi = _mod.mh868_flussi
    mh868_frazione = _mod.mh868_frazione
    mh868_gas_alt = _mod.mh868_gas_alt
    mh868_gas_base = _mod.mh868_gas_base
    mh868_int_pos = _mod.mh868_int_pos
    mh868_kwp = _mod.mh868_kwp
    mh868_nneg = _mod.mh868_nneg
    mh868_num = _mod.mh868_num
    mh868_p_gas_pareggio = _mod.mh868_p_gas_pareggio
    mh868_payback = _mod.mh868_payback
    mh868_pos = _mod.mh868_pos
    mh868_ricavo_immissione = _mod.mh868_ricavo_immissione
    mh868_risparmio = _mod.mh868_risparmio
    mh868_sensibilita = _mod.mh868_sensibilita
    mh868_tir = _mod.mh868_tir
    mh868_valida = _mod.mh868_valida
    mh868_van = _mod.mh868_van
    mh868_verdetto = _mod.mh868_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w872_helpers.py")
_UI_PATH = _risolvi("w872_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "7"
_VECCHIO_TAB = "tab86" + "7"
_VECCHIO_ST = "st86" + "7_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "gas_base_kwh_anno": 180000.0,
    "e_base_kwh_anno": 960000.0,
    "c_base_eur_anno": 287400.0,
    "gas_alt_kwh_anno": 90000.0,
    "e_alt_kwh_anno": 420000.0,
    "kwp": 400.0,
    "e_pv_kwh_anno": 440000.0,
    "e_pv_auto_kwh_anno": 264000.0,
    "e_immessa_kwh_anno": 176000.0,
    "e_deficit_kwh_anno": 156000.0,
    "ricavo_immissione_eur_anno": 14080.0,
    "c_alt_eur_anno": 118340.0,
    "risparmio_eur_anno": 169060.0,
    "capex_eur": 760000.0,
    "co2_base_t_anno": 324.0,
    "co2_alt_t_anno": 64.8,
    "co2_evitata_t_anno": 259.2,
    "van": 1346861.2805098093,
    "tir": 21.814990105996852,
    "payback": 5,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh868_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh868_num(3, "x"), 3.0)
        self.assertEqual(mh868_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh868_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh868_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh868_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh868_pos(0, "x")
        with self.assertRaises(ValueError):
            mh868_pos(-1, "x")
        self.assertEqual(mh868_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh868_int_pos(20, "x"), 20)
        self.assertEqual(mh868_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh868_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh868_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh868_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh868_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh868_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh868_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_gas_e_costo_base(self):
        self.assertEqual(mh868_gas_base(1200, 150), 180000.0)
        self.assertEqual(mh868_e_base(1200, 800), 960000.0)
        self.assertEqual(mh868_c_base(180000.0, 0.09, 960000.0, 0.22,
                                       60000), 287400.0)

    def test_recupero_riduce_gas_non_azzera(self):
        self.assertEqual(mh868_gas_alt(180000.0, 0.50), 90000.0)
        self.assertEqual(mh868_gas_alt(180000.0, 0.0), 180000.0)
        self.assertEqual(mh868_gas_alt(180000.0, 1.0), 0.0)
        self.assertEqual(mh868_e_alt(1200, 350), 420000.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh868_kwp(2000, 0.20), 400.0)
        self.assertEqual(mh868_e_pv(400.0, 1100), 440000.0)
        self.assertEqual(mh868_e_pv_auto(440000.0, 0.60, 420000.0),
                         264000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh868_e_pv_auto(440000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh868_e_immessa(440000.0, 264000.0), 176000.0)
        self.assertEqual(mh868_e_deficit(420000.0, 264000.0), 156000.0)
        self.assertEqual(mh868_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh868_ricavo_immissione(176000.0, 0.08), 14080.0)
        self.assertAlmostEqual(
            mh868_c_alt(90000.0, 0.09, 156000.0, 0.22, 14080.0,
                        90000.0),
            118340.0)
        self.assertAlmostEqual(mh868_risparmio(287400.0, 118340.0),
                               169060.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh868_capex_totale(500000, 80000, 400.0,
                                            450),
                         760000.0)
        self.assertEqual(mh868_capex_totale(500000, 80000, 0.0,
                                            450),
                         580000.0)

    def test_co2_base_e_alt(self):
        cb = mh868_co2_base(180000.0, 0.20, 960000.0, 0.30)
        self.assertAlmostEqual(cb, 324.0, places=4)
        ca = mh868_co2_alt(90000.0, 0.20, 156000.0, 0.30)
        self.assertAlmostEqual(ca, 64.8, places=4)
        self.assertAlmostEqual(mh868_co2_evitata(cb, ca), 259.2, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # gas alternativo e deficit.
        self.assertEqual(mh868_co2_alt(0.0, 0.20, 0.0, 0.30), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh868_flussi(760000, 169060.0, 3),
                         [-760000, 169060.0, 169060.0, 169060.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh868_van([-100, 60, 60], 0), 20.0)
        bc = mh868_demo_calcoli()
        self.assertAlmostEqual(mh868_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh868_demo_calcoli()
        tir = mh868_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh868_tir([-100, -10, -10]))
        self.assertIsNone(mh868_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh868_demo_calcoli()
        self.assertEqual(mh868_payback(bc["flussi"]), 5)
        self.assertIsNone(mh868_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh868_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh868_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:5]), -83760.0, places=2)
        self.assertAlmostEqual(sum(flussi[:6]), 85300.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh868_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh868_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh868_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh868_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh868_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh868_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh868_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh868_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / (bc["gas_base_kwh_anno"]
                           - bc["gas_alt_kwh_anno"]), 0.0)
        self.assertAlmostEqual(
            (bc["e_deficit_kwh_anno"] * bc["p_el"]
             - bc["ricavo_immissione_eur_anno"]
             + bc["om_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / (bc["gas_base_kwh_anno"]
               - bc["gas_alt_kwh_anno"]), -1.7884444444444445, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertEqual(mh868_p_gas_pareggio(180000.0, 90000.0,
                                             960000.0, 156000.0,
                                             0.22, 14080.0,
                                             60000.0, 400000.0),
                         1.656)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh868_p_gas_pareggio(180000.0, 90000.0,
                                             960000.0, 156000.0,
                                             0.22, 14080.0,
                                             60000.0, 250960.0),
                         0.0)
        self.assertIsNone(mh868_p_gas_pareggio(90000.0, 90000.0,
                                              960000.0, 156000.0,
                                              0.22, 14080.0,
                                              60000.0, 90000.0))
        self.assertIsNone(mh868_p_gas_pareggio(180000.0, 90000.0,
                                              960000.0, 156000.0,
                                              0.22, 14080.0,
                                              60000.0, 90000.0))

    def test_valida_demo_ok(self):
        demo = mh868_demo()
        val = mh868_valida(*[demo[k] for k in (
            "t_anno", "e_base_per_t", "q_gas_base_per_t",
            "p_gas", "p_el", "om_base_eur_anno",
            "f_recupero", "e_alt_per_t", "sup_m2", "kwp_per_m2",
            "resa_fv", "f_autoconsumo", "p_immissione",
            "om_alt_eur_anno", "capex_presse_eur", "capex_free_cooling_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_kwh",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonnellate_zero_no(self):
        kw = _demo_kwargs(t_anno=0)
        self.assertRaises(ValueError, mh868_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh868_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh868_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh868_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh868_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh868_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("t_anno", -1),
                              ("e_base_per_t", -1),
                              ("p_gas", -0.01),
                              ("capex_presse_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh868_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh868_calcola(mh868_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh868_calcola(dict(mh868_demo(), capex_presse_eur=999999),
                           capex_presse_eur=500000)
        self.assertEqual(bc["capex_eur"], 760000.0)


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
            bc["gas_base_kwh_anno"] * bc["p_gas"]
            + bc["e_base_kwh_anno"] * bc["p_el"]
            + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["gas_alt_kwh_anno"] * bc["p_gas"]
            + bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["ricavo_immissione_eur_anno"]
            + bc["om_alt_eur_anno"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / (bc["gas_base_kwh_anno"]
                           - bc["gas_alt_kwh_anno"]), 0.0)

    def test_sensibilita_valori(self):
        s = mh868_sensibilita(**mh868_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               170680.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               1367050.06, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               96900.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               627588.18, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 6)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 580000.0)
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               160960.0, places=2)
        self.assertAlmostEqual(s["senza_recupero"]["van"],
                               1245917.38, places=2)
        self.assertEqual(s["senza_recupero"]["payback"], 5)
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["e_alt_uguale_base"]["risparmio_eur_anno"],
                               50260.0, places=2)
        self.assertAlmostEqual(s["e_alt_uguale_base"]["van"],
                               -133649.31, places=2)
        self.assertEqual(s["e_alt_uguale_base"]["payback"], 16)
        self.assertEqual(s["e_alt_uguale_base"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               586861.28, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 9)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               545436.51, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               2621200.0, places=2)

    def test_marginale_con_capex_presse_alto(self):
        # CAPEX totale 2.160.000 (presse a 1.900.000):
        # VAN circa -53.139, entro la tolleranza del 10%
        # (216.000).
        bc = mh868_calcola(**_demo_kwargs(capex_presse_eur=1900000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -53138.72, places=2)

    def test_non_convente_con_capex_presse_altissimo(self):
        bc = mh868_calcola(**_demo_kwargs(capex_presse_eur=2100000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -253138.72, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh868_calcola(**_demo_kwargs(om_alt_eur_anno=400000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -140940.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh868_csv(bc, mh868_demo())
        for voce in ("t_anno", "gas_base_kwh_anno",
                     "gas_alt_kwh_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -760000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (t/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh868_c_alt(90000.0, 0.09, 420000.0, 0.22, 0.0,
                            90000.0)
        con = mh868_c_alt(90000.0, 0.09, 156000.0, 0.22, 14080.0,
                          90000.0)
        self.assertAlmostEqual(senza - con, 420000.0 * 0.22 - 156000.0 * 0.22 + 14080.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh868_sensibilita(**mh868_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "senza_fv",
                          "senza_recupero", "e_alt_uguale_base",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh868_csv(bc, mh868_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("gas_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh868_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh868_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh868_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 580000.0)
        bc = mh868_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def868\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh868_demo().keys()), lette - set(mh868_demo().keys()))
        self.assertEqual(lette, set(mh868_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc868\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc868\["([^"]+)"\]', src))
        attese = set(mh868_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab868:"), 1)
        self.assertTrue(src.startswith("    # W872"))

    def test_ui_tab868_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab868:"), 1)
        self.assertIn("def mh868_demo(", src_h)
        self.assertIn("def mh868_calcola(", src_h)
        self.assertIn("tab868", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Stampaggio plastica a iniezione: presse servo-elettriche + free-cooling stampi + FV battono presse idrauliche tradizionali + essiccazione a gas?", src)
        self.assertIn("🏭 Stampaggio plastica a iniezione: presse servo-elettriche + free-cooling stampi + FV battono presse idrauliche tradizionali + essiccazione a gas?", src)
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
        chiavi = re.findall(r'key="(st868_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st868_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st868_calcola"', src)
        self.assertIn('key="st868_csv"', src)
        self.assertIn('key="st868_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg868"), src.index(".paiac("))
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
