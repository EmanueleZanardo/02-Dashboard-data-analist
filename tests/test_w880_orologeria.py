"""Test nuova scheda orologeria:
micromeccanica CNC efficiente +
lucidatura efficiente + FV battono
micromeccanica tradizionale +
trattamenti termici a gas?

Business case annuo di una orologeria,
guidato dagli OROLOGI all'anno
prodotti (demo 8.000 orologi/anno):
micromeccanica tradizionale base
8.000 x 2,0 = 16.000 kWh/anno;
lucidatura base 8.000 x 0,6 = 4.800
kWh/anno; elettricita' base totale
20.800 kWh/anno, costo energia base
4.576 EUR/anno; gas base 8.000 x 0,30
= 2.400 Smc/anno, costo gas base 2.160
EUR/anno; O&M base 12.000 EUR/anno;
costo base 18.736 EUR/anno; micromeccanica
CNC efficiente 8.000 x 1,2 =
9.600 kWh/anno; lucidatura efficiente
8.000 x 0,35 = 2.800 kWh/anno;
elettricita' alternativa 12.400
kWh/anno; kWp = sup x kwp/m2
(demo 40 kWp); E_pv 44.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 12.400 kWh/anno); immessa
31.600 kWh/anno; deficit 0 kWh/anno;
ricavo immissione 2.528 EUR/anno; O&M
alternativa 9.000 EUR/anno; C_alt
6.472 EUR/anno; risparmio 12.264
EUR/anno; CAPEX 60.000 + 20.000 + 40 x
900 = 116.000 EUR; CO2 base = (gas x
1,96 + E_base x 0,35) / 1000 = 11,984
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 0,0 t/anno (immessa senza
credito CO2); CO2 evitata 11,984
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt -
E_base x p_el - om_base) / gas in
forma chiusa (demo None: rapporto
negativo -4,21, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (orologi <= 0, kWh per
orologio < 0, prezzi < 0, O&M < 0,
superficie < 0, kwp per m2 < 0,
resa < 0, f_autoconsumo < 0 o > 1,
voci CAPEX < 0, fattori CO2 < 0,
WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON
gioielleria (niente fusione di metalli
preziosi e niente gioielli, solo orologi
da lavorare in micromeccanica e
lucidare), NON occhialeria (niente
montature e niente lenti, solo orologi
con micromeccanica di precisione e
lucidatura di casse e quadranti), NON
calzaturificio (niente cucitura e
niente montaggio di scarpe, solo orologi
da lavorare in micromeccanica e
lucidare); qui solo micromeccanica di
precisione + lucidatura casse e
quadranti + trattamenti termici a gas
+ FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w880_helpers import (
        demo_calcoli,
        mh876_c_alt,
        mh876_c_base,
        mh876_calcola,
        mh876_capex_totale,
        mh876_co2_alt,
        mh876_co2_base,
        mh876_co2_evitata,
        mh876_csv,
        mh876_demo,
        mh876_demo_calcoli,
        mh876_e_alt,
        mh876_e_deficit,
        mh876_e_immessa,
        mh876_e_mec_alt,
        mh876_e_mec_base,
        mh876_e_luc_alt,
        mh876_e_luc_base,
        mh876_e_base,
        mh876_e_pv,
        mh876_e_pv_auto,
        mh876_flussi,
        mh876_frazione,
        mh876_gas_base,
        mh876_int_pos,
        mh876_kwp,
        mh876_nneg,
        mh876_num,
        mh876_p_gas_pareggio,
        mh876_payback,
        mh876_pos,
        mh876_ricavo_immissione,
        mh876_risparmio,
        mh876_sensibilita,
        mh876_tir,
        mh876_valida,
        mh876_van,
        mh876_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w880_helpers", os.path.join(_hf, "w880_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh876_c_alt = _mod.mh876_c_alt
    mh876_c_base = _mod.mh876_c_base
    mh876_calcola = _mod.mh876_calcola
    mh876_capex_totale = _mod.mh876_capex_totale
    mh876_co2_alt = _mod.mh876_co2_alt
    mh876_co2_base = _mod.mh876_co2_base
    mh876_co2_evitata = _mod.mh876_co2_evitata
    mh876_csv = _mod.mh876_csv
    mh876_demo = _mod.mh876_demo
    mh876_demo_calcoli = _mod.mh876_demo_calcoli
    mh876_e_alt = _mod.mh876_e_alt
    mh876_e_deficit = _mod.mh876_e_deficit
    mh876_e_immessa = _mod.mh876_e_immessa
    mh876_e_mec_alt = _mod.mh876_e_mec_alt
    mh876_e_mec_base = _mod.mh876_e_mec_base
    mh876_e_luc_alt = _mod.mh876_e_luc_alt
    mh876_e_luc_base = _mod.mh876_e_luc_base
    mh876_e_base = _mod.mh876_e_base
    mh876_e_pv = _mod.mh876_e_pv
    mh876_e_pv_auto = _mod.mh876_e_pv_auto
    mh876_flussi = _mod.mh876_flussi
    mh876_frazione = _mod.mh876_frazione
    mh876_gas_base = _mod.mh876_gas_base
    mh876_int_pos = _mod.mh876_int_pos
    mh876_kwp = _mod.mh876_kwp
    mh876_nneg = _mod.mh876_nneg
    mh876_num = _mod.mh876_num
    mh876_p_gas_pareggio = _mod.mh876_p_gas_pareggio
    mh876_payback = _mod.mh876_payback
    mh876_pos = _mod.mh876_pos
    mh876_ricavo_immissione = _mod.mh876_ricavo_immissione
    mh876_risparmio = _mod.mh876_risparmio
    mh876_sensibilita = _mod.mh876_sensibilita
    mh876_tir = _mod.mh876_tir
    mh876_valida = _mod.mh876_valida
    mh876_van = _mod.mh876_van
    mh876_verdetto = _mod.mh876_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w880_helpers.py")
_UI_PATH = _risolvi("w880_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "5"
_VECCHIO_TAB = "tab87" + "5"
_VECCHIO_ST = "st87" + "5_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_mec_base_kwh_anno": 16000.0,
    "e_luc_base_kwh_anno": 4800.0,
    "e_base_kwh_anno": 20800.0,
    "gas_base_smc_anno": 2400.0,
    "c_base_eur_anno": 18736.0,
    "e_mec_alt_kwh_anno": 9600.0,
    "e_luc_alt_kwh_anno": 2800.0,
    "e_alt_kwh_anno": 12400.0,
    "kwp": 40.0,
    "e_pv_kwh_anno": 44000.0,
    "e_pv_auto_kwh_anno": 12400.0,
    "e_immessa_kwh_anno": 31600.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_immissione_eur_anno": 2528.0,
    "c_alt_eur_anno": 6472.0,
    "risparmio_eur_anno": 12264.0,
    "capex_eur": 116000.0,
    "co2_base_t_anno": 11.984,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 11.984,
    "van": 36836.54764091034,
    "tir": 8.506908198318396,
    "payback": 10,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh876_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh876_num(3, "x"), 3.0)
        self.assertEqual(mh876_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh876_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh876_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh876_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh876_pos(0, "x")
        with self.assertRaises(ValueError):
            mh876_pos(-1, "x")
        self.assertEqual(mh876_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh876_int_pos(20, "x"), 20)
        self.assertEqual(mh876_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh876_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh876_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh876_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh876_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh876_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh876_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_fus_e_luc_base_e_costo_base(self):
        self.assertEqual(mh876_e_mec_base(8000, 2.0), 16000.0)
        self.assertEqual(mh876_e_luc_base(8000, 0.6), 4800.0)
        self.assertEqual(mh876_e_base(16000.0, 4800.0), 20800.0)
        self.assertEqual(mh876_gas_base(8000, 0.30), 2400.0)
        self.assertEqual(mh876_c_base(20800.0, 0.22, 2400.0, 0.90,
                                       12000), 18736.0)

    def test_fus_alt_luc_alt_somma(self):
        self.assertEqual(mh876_e_mec_alt(8000, 1.2), 9600.0)
        self.assertEqual(mh876_e_luc_alt(8000, 0.35), 2800.0)
        self.assertEqual(mh876_e_alt(9600.0, 2800.0), 12400.0)
        # La micromeccanica CNC RIDUCE il consumo,
        # non lo azzerano: 0,90 resta sopra zero anche
        # a parita' di base 1,5.
        self.assertGreater(mh876_e_mec_alt(8000, 1.2), 0.0)
        self.assertLess(mh876_e_mec_alt(8000, 1.2),
                        mh876_e_mec_base(8000, 2.0))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh876_kwp(200, 0.20), 40.0)
        self.assertEqual(mh876_e_pv(40.0, 1100), 44000.0)
        self.assertEqual(mh876_e_pv_auto(44000.0, 0.50, 12400.0),
                         12400.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh876_e_pv_auto(44000.0, 1.0, 10000.0), 10000.0)
        self.assertEqual(mh876_e_immessa(44000.0, 12400.0), 31600.0)
        self.assertEqual(mh876_e_deficit(12400.0, 12400.0), 0.0)
        self.assertEqual(mh876_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh876_ricavo_immissione(31600.0, 0.08), 2528.0)
        self.assertAlmostEqual(
            mh876_c_alt(0.0, 0.22, 2528.0, 9000.0),
            6472.0)
        self.assertAlmostEqual(mh876_risparmio(18736.0, 6472.0),
                               12264.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh876_capex_totale(60000, 20000, 40.0,
                                            900),
                         116000.0)
        self.assertEqual(mh876_capex_totale(60000, 20000, 0.0,
                                            900),
                         80000.0)

    def test_co2_base_e_alt(self):
        cb = mh876_co2_base(2400.0, 1.96, 20800.0, 0.35)
        self.assertAlmostEqual(cb, 11.984, places=4)
        ca = mh876_co2_alt(0.0, 0.35)
        self.assertAlmostEqual(ca, 0.0, places=4)
        self.assertAlmostEqual(mh876_co2_evitata(cb, ca), 11.984, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh876_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh876_flussi(116000, 12264.0, 3),
                         [-116000, 12264.0, 12264.0, 12264.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh876_van([-100, 60, 60], 0), 20.0)
        bc = mh876_demo_calcoli()
        self.assertAlmostEqual(mh876_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh876_demo_calcoli()
        tir = mh876_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh876_tir([-100, -10, -10]))
        self.assertIsNone(mh876_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh876_demo_calcoli()
        self.assertEqual(mh876_payback(bc["flussi"]), 10)
        self.assertIsNone(mh876_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh876_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh876_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:10]), -5624.0, places=2)
        self.assertAlmostEqual(sum(flussi[:11]), 6640.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh876_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh876_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh876_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh876_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh876_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh876_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh876_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh876_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["e_deficit_kwh_anno"] * bc["p_el"]
             - bc["ricavo_immissione_eur_anno"]
             + bc["om_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], -4.21, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh876_p_gas_pareggio(2400.0, 20800.0, 0.0,
                                 0.22, 2528.0, 12000.0, 100000.0),
            33.7066666667, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh876_p_gas_pareggio(2400.0, 20800.0,
                                              0.0, 0.22, 2528.0,
                                              12000.0, 19104.0),
                         0.0)
        self.assertIsNone(mh876_p_gas_pareggio(0.0, 20800.0,
                                               0.0, 0.22, 2528.0,
                                               12000.0, 9000.0))
        self.assertIsNone(mh876_p_gas_pareggio(2400.0, 20800.0,
                                               0.0, 0.22, 2528.0,
                                               12000.0, 9000.0))

    def test_valida_demo_ok(self):
        demo = mh876_demo()
        val = mh876_valida(*[demo[k] for k in (
            "orologi_anno", "e_mec_base_per_orologio",
            "e_luc_base_per_orologio", "p_el",
            "gas_per_orologio", "p_gas", "om_base_eur_anno",
            "e_mec_alt_per_orologio", "e_luc_alt_per_orologio", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_mec_eur", "capex_luc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_orologi_zero_no(self):
        kw = _demo_kwargs(orologi_anno=0)
        self.assertRaises(ValueError, mh876_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh876_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh876_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh876_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh876_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("orologi_anno", -1),
                              ("e_mec_base_per_orologio", -1),
                              ("p_gas", -0.01),
                              ("capex_mec_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh876_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh876_calcola(mh876_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh876_calcola(dict(mh876_demo(), capex_mec_eur=999999),
                           capex_mec_eur=60000)
        self.assertEqual(bc["capex_eur"], 116000.0)


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
        self.assertEqual(bc["payback"], 10)

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
            bc["e_base_kwh_anno"] * bc["p_el"]
            + bc["gas_base_smc_anno"] * bc["p_gas"]
            + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
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
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh876_sensibilita(**mh876_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               12696.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               42220.22, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 10)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               13179.2, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               48241.96, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 9)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               7008.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               7335.17, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 12)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 80000.0)
        self.assertAlmostEqual(s["senza_cnc"]["risparmio_eur_anno"],
                               11752.0, places=2)
        self.assertAlmostEqual(s["senza_cnc"]["van"],
                               30455.90, places=2)
        self.assertEqual(s["senza_cnc"]["payback"], 10)
        self.assertEqual(s["senza_cnc"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -79163.45, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 19)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -21300.64, places=2)
        self.assertEqual(s["vita_10"]["payback"], 10)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               129280.0, places=2)

    def test_marginale_con_capex_micromeccanica_alto(self):
        # CAPEX totale 166.000 (micromeccanica a 110.000):
        # VAN circa -13.163,45, entro la tolleranza del 10%
        # (16.600).
        bc = mh876_calcola(**_demo_kwargs(capex_mec_eur=110000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -13163.45, places=2)

    def test_non_convente_con_capex_micromeccanica_altissimo(self):
        bc = mh876_calcola(**_demo_kwargs(capex_mec_eur=130000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -33163.45, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh876_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -78736.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh876_csv(bc, mh876_demo())
        for voce in ("orologi_anno", "e_mec_base_kwh_anno",
                     "e_luc_base_kwh_anno", "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -116000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Orologi (orologi/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh876_c_alt(12400.0, 0.22, 0.0, 9000.0)
        con = mh876_c_alt(0.0, 0.22, 2528.0, 9000.0)
        self.assertAlmostEqual(senza - con, 12400.0 * 0.22 - 0.0 * 0.22 + 2528.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh876_sensibilita(**mh876_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_cnc",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh876_csv(bc, mh876_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_mec_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh876_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh876_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh876_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 80000.0)
        bc = mh876_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def876\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh876_demo().keys()), lette - set(mh876_demo().keys()))
        self.assertEqual(lette, set(mh876_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc876\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc876\["([^"]+)"\]', src))
        attese = set(mh876_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 889)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab876:"), 1)
        self.assertTrue(src.startswith("    # W880"))

    def test_ui_tab876_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab876:"), 1)
        self.assertIn("def mh876_demo(", src_h)
        self.assertIn("def mh876_calcola(", src_h)
        self.assertIn("tab876", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Orologeria: micromeccanica CNC efficiente + lucidatura efficiente + FV battono micromeccanica tradizionale + trattamenti termici a gas?", src)
        self.assertIn("⌚ Orologeria: micromeccanica CNC efficiente + lucidatura efficiente + FV battono micromeccanica tradizionale + trattamenti termici a gas?", src)
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
        chiavi = re.findall(r'key="(st876_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st876_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st876_calcola"', src)
        self.assertIn('key="st876_csv"', src)
        self.assertIn('key="st876_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg876"), src.index(".paiac("))
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


if __name__ == "__main__":
    unittest.main()
