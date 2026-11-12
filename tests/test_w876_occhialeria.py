"""Test nuova scheda occhialeria /
produzione occhiali e montature:
stampaggio/fresatura efficienti +
lucidatura efficiente + FV battono
lavorazioni tradizionali +
essiccazione a gas?

Business case annuo di una occhialeria,
guidato dalle MONTATURE all'anno
prodotte (demo 200.000 montature/
anno): lavorazioni meccaniche base
200.000 x 1,4 = 280.000 kWh/anno;
lucidatura base 200.000 x 0,7 =
140.000 kWh/anno; elettricita' base
totale 420.000 kWh/anno, costo energia
base 92.400 EUR/anno; gas base
200.000 x 0,30 = 60.000 Smc/anno,
costo gas base 54.000 EUR/anno; O&M
base 38.000 EUR/anno; costo base
184.400 EUR/anno; fresatura/CNC con
inverter 200.000 x 1,05 = 210.000
kWh/anno; lucidatura efficiente
200.000 x 0,45 = 90.000 kWh/anno;
elettricita' alternativa 300.000
kWh/anno; kWp = sup x kwp/m2
(demo 240 kWp); E_pv 264.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 158.400 kWh/anno); immessa
105.600 kWh/anno; deficit 141.600
kWh/anno; ricavo immissione 8.448
EUR/anno; O&M alternativa 30.000
EUR/anno; C_alt 52.704 EUR/anno;
risparmio 131.696 EUR/anno; CAPEX
220.000 + 70.000 + 240 x 900 = 506.000
EUR; CO2 base = (gas x 1,96 +
E_base x 0,35) / 1000 = 264,60
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 49,56 t/anno (immessa senza
credito CO2); CO2 evitata 215,04
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt -
E_base x p_el - om_base) / gas in
forma chiusa (demo None: rapporto
negativo -1,29493, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (montature <= 0, kWh per
montatura < 0, prezzi < 0, O&M < 0,
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
Distinzione esplicita: NON rubinetteria
(niente pezzi di rubinetti e valvolame),
NON falegnameria e NON serramenti
(niente legno), NON galvanica (niente
bagni galvanici), NON stampaggio
plastica generico (niente pezzi
stampati in generale); qui solo
lavorazioni meccaniche + lucidatura +
FV su montature di occhiali.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w876_helpers import (
        demo_calcoli,
        mh872_c_alt,
        mh872_c_base,
        mh872_calcola,
        mh872_capex_totale,
        mh872_co2_alt,
        mh872_co2_base,
        mh872_co2_evitata,
        mh872_csv,
        mh872_demo,
        mh872_demo_calcoli,
        mh872_e_alt,
        mh872_e_deficit,
        mh872_e_immessa,
        mh872_e_lucid_alt,
        mh872_e_lucid_base,
        mh872_e_base,
        mh872_e_pv,
        mh872_e_pv_auto,
        mh872_e_cnc_alt,
        mh872_e_mecc_base,
        mh872_flussi,
        mh872_frazione,
        mh872_gas_base,
        mh872_int_pos,
        mh872_kwp,
        mh872_nneg,
        mh872_num,
        mh872_p_gas_pareggio,
        mh872_payback,
        mh872_pos,
        mh872_ricavo_immissione,
        mh872_risparmio,
        mh872_sensibilita,
        mh872_tir,
        mh872_valida,
        mh872_van,
        mh872_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w876_helpers", os.path.join(_hf, "w876_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh872_c_alt = _mod.mh872_c_alt
    mh872_c_base = _mod.mh872_c_base
    mh872_calcola = _mod.mh872_calcola
    mh872_capex_totale = _mod.mh872_capex_totale
    mh872_co2_alt = _mod.mh872_co2_alt
    mh872_co2_base = _mod.mh872_co2_base
    mh872_co2_evitata = _mod.mh872_co2_evitata
    mh872_csv = _mod.mh872_csv
    mh872_demo = _mod.mh872_demo
    mh872_demo_calcoli = _mod.mh872_demo_calcoli
    mh872_e_alt = _mod.mh872_e_alt
    mh872_e_deficit = _mod.mh872_e_deficit
    mh872_e_immessa = _mod.mh872_e_immessa
    mh872_e_lucid_alt = _mod.mh872_e_lucid_alt
    mh872_e_lucid_base = _mod.mh872_e_lucid_base
    mh872_e_base = _mod.mh872_e_base
    mh872_e_pv = _mod.mh872_e_pv
    mh872_e_pv_auto = _mod.mh872_e_pv_auto
    mh872_e_cnc_alt = _mod.mh872_e_cnc_alt
    mh872_e_mecc_base = _mod.mh872_e_mecc_base
    mh872_flussi = _mod.mh872_flussi
    mh872_frazione = _mod.mh872_frazione
    mh872_gas_base = _mod.mh872_gas_base
    mh872_int_pos = _mod.mh872_int_pos
    mh872_kwp = _mod.mh872_kwp
    mh872_nneg = _mod.mh872_nneg
    mh872_num = _mod.mh872_num
    mh872_p_gas_pareggio = _mod.mh872_p_gas_pareggio
    mh872_payback = _mod.mh872_payback
    mh872_pos = _mod.mh872_pos
    mh872_ricavo_immissione = _mod.mh872_ricavo_immissione
    mh872_risparmio = _mod.mh872_risparmio
    mh872_sensibilita = _mod.mh872_sensibilita
    mh872_tir = _mod.mh872_tir
    mh872_valida = _mod.mh872_valida
    mh872_van = _mod.mh872_van
    mh872_verdetto = _mod.mh872_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w876_helpers.py")
_UI_PATH = _risolvi("w876_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "1"
_VECCHIO_TAB = "tab87" + "1"
_VECCHIO_ST = "st87" + "1_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")
_TITLES_SNAPSHOT = os.path.join(_HF_FALLBACK, "w875_titles.txt")

_DEMO = {
    "e_mecc_base_kwh_anno": 280000.0,
    "e_lucid_base_kwh_anno": 140000.0,
    "e_base_kwh_anno": 420000.0,
    "gas_base_smc_anno": 60000.0,
    "c_base_eur_anno": 184400.0,
    "e_cnc_alt_kwh_anno": 210000.0,
    "e_lucid_alt_kwh_anno": 90000.0,
    "e_alt_kwh_anno": 300000.0,
    "kwp": 240.0,
    "e_pv_kwh_anno": 264000.0,
    "e_pv_auto_kwh_anno": 158400.0,
    "e_immessa_kwh_anno": 105600.0,
    "e_deficit_kwh_anno": 141600.0,
    "ricavo_immissione_eur_anno": 8448.0,
    "c_alt_eur_anno": 52704.0,
    "risparmio_eur_anno": 131696.0,
    "capex_eur": 506000.0,
    "co2_base_t_anno": 264.6,
    "co2_alt_t_anno": 49.56,
    "co2_evitata_t_anno": 215.04,
    "van": 1135223.2532711455,
    "tir": 25.761114468422242,
    "payback": 4,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh872_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh872_num(3, "x"), 3.0)
        self.assertEqual(mh872_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh872_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh872_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh872_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh872_pos(0, "x")
        with self.assertRaises(ValueError):
            mh872_pos(-1, "x")
        self.assertEqual(mh872_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh872_int_pos(20, "x"), 20)
        self.assertEqual(mh872_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh872_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh872_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh872_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh872_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh872_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh872_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_mecc_e_lucid_base_e_costo_base(self):
        self.assertEqual(mh872_e_mecc_base(200000, 1.4), 280000.0)
        self.assertEqual(mh872_e_lucid_base(200000, 0.7), 140000.0)
        self.assertEqual(mh872_e_base(280000.0, 140000.0), 420000.0)
        self.assertEqual(mh872_gas_base(200000, 0.30), 60000.0)
        self.assertEqual(mh872_c_base(420000.0, 0.22, 60000.0, 0.90,
                                       38000), 184400.0)

    def test_cnc_alt_lucid_alt_somma(self):
        self.assertEqual(mh872_e_cnc_alt(200000, 1.05), 210000.0)
        self.assertEqual(mh872_e_lucid_alt(200000, 0.45), 90000.0)
        self.assertEqual(mh872_e_alt(210000.0, 90000.0), 300000.0)
        # L'inverter RIDUCE la fresatura/CNC, non lo azzera:
        # 1,05 resta sopra zero anche a parita' di base 1,4.
        self.assertGreater(mh872_e_cnc_alt(200000, 1.05), 0.0)
        self.assertLess(mh872_e_cnc_alt(200000, 1.05),
                        mh872_e_mecc_base(200000, 1.4))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh872_kwp(1200, 0.20), 240.0)
        self.assertEqual(mh872_e_pv(240.0, 1100), 264000.0)
        self.assertEqual(mh872_e_pv_auto(264000.0, 0.60, 300000.0),
                         158400.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh872_e_pv_auto(264000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh872_e_immessa(264000.0, 158400.0), 105600.0)
        self.assertEqual(mh872_e_deficit(300000.0, 158400.0), 141600.0)
        self.assertEqual(mh872_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh872_ricavo_immissione(105600.0, 0.08), 8448.0)
        self.assertAlmostEqual(
            mh872_c_alt(141600.0, 0.22, 8448.0, 30000.0),
            52704.0)
        self.assertAlmostEqual(mh872_risparmio(184400.0, 52704.0),
                               131696.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh872_capex_totale(220000, 70000, 240.0,
                                            900),
                         506000.0)
        self.assertEqual(mh872_capex_totale(220000, 70000, 0.0,
                                            900),
                         290000.0)

    def test_co2_base_e_alt(self):
        cb = mh872_co2_base(60000.0, 1.96, 420000.0, 0.35)
        self.assertAlmostEqual(cb, 264.6, places=4)
        ca = mh872_co2_alt(141600.0, 0.35)
        self.assertAlmostEqual(ca, 49.56, places=4)
        self.assertAlmostEqual(mh872_co2_evitata(cb, ca), 215.04, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh872_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh872_flussi(506000, 131696.0, 3),
                         [-506000, 131696.0, 131696.0, 131696.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh872_van([-100, 60, 60], 0), 20.0)
        bc = mh872_demo_calcoli()
        self.assertAlmostEqual(mh872_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh872_demo_calcoli()
        tir = mh872_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh872_tir([-100, -10, -10]))
        self.assertIsNone(mh872_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh872_demo_calcoli()
        self.assertEqual(mh872_payback(bc["flussi"]), 4)
        self.assertIsNone(mh872_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh872_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh872_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:4]), -110912.0, places=2)
        self.assertAlmostEqual(sum(flussi[:5]), 20784.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh872_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh872_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh872_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh872_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh872_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh872_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh872_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh872_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -1.2949333333333333, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh872_p_gas_pareggio(60000.0, 420000.0, 141600.0,
                                 0.22, 8448.0, 38000.0, 200000.0),
            1.5384, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh872_p_gas_pareggio(60000.0, 420000.0,
                                              141600.0, 0.22, 8448.0,
                                              38000.0, 107696.0),
                         0.0)
        self.assertIsNone(mh872_p_gas_pareggio(0.0, 420000.0,
                                               141600.0, 0.22, 8448.0,
                                               38000.0, 30000.0))
        self.assertIsNone(mh872_p_gas_pareggio(60000.0, 420000.0,
                                               141600.0, 0.22, 8448.0,
                                               38000.0, 30000.0))

    def test_valida_demo_ok(self):
        demo = mh872_demo()
        val = mh872_valida(*[demo[k] for k in (
            "montature_anno", "e_mecc_base_per_pezzo",
            "e_lucid_base_per_pezzo", "p_el",
            "gas_per_pezzo", "p_gas", "om_base_eur_anno",
            "e_cnc_alt_per_pezzo", "e_lucid_alt_per_pezzo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_cnc_eur", "capex_lucid_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_montature_zero_no(self):
        kw = _demo_kwargs(montature_anno=0)
        self.assertRaises(ValueError, mh872_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh872_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh872_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh872_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh872_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("montature_anno", -1),
                              ("e_mecc_base_per_pezzo", -1),
                              ("p_gas", -0.01),
                              ("capex_cnc_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh872_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh872_calcola(mh872_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh872_calcola(dict(mh872_demo(), capex_cnc_eur=999999),
                           capex_cnc_eur=220000)
        self.assertEqual(bc["capex_eur"], 506000.0)


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
        s = mh872_sensibilita(**mh872_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               142496.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               1269815.12, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               143945.6, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               1287880.35, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 4)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               88400.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               811659.39, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 4)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 290000.0)
        self.assertAlmostEqual(s["senza_inverter"]["risparmio_eur_anno"],
                               116296.0, places=2)
        self.assertAlmostEqual(s["senza_inverter"]["van"],
                               943305.21, places=2)
        self.assertEqual(s["senza_inverter"]["payback"], 5)
        self.assertEqual(s["senza_inverter"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               629223.25, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 8)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               510921.60, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               2127920.0, places=2)

    def test_marginale_con_capex_cnc_alto(self):
        # CAPEX totale 1.736.000 (fresatura/CNC a 1.450.000):
        # VAN circa -94.776,75, entro la tolleranza del 10%
        # (173.600).
        bc = mh872_calcola(**_demo_kwargs(capex_cnc_eur=1450000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -94776.75, places=2)

    def test_non_convente_con_capex_cnc_altissimo(self):
        bc = mh872_calcola(**_demo_kwargs(capex_cnc_eur=1800000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -444776.75, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh872_calcola(**_demo_kwargs(om_alt_eur_anno=300000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -138304.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh872_csv(bc, mh872_demo())
        for voce in ("montature_anno", "e_mecc_base_kwh_anno",
                     "e_lucid_base_kwh_anno", "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -506000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Montature (montature/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh872_c_alt(300000.0, 0.22, 0.0, 30000.0)
        con = mh872_c_alt(141600.0, 0.22, 8448.0, 30000.0)
        self.assertAlmostEqual(senza - con, 300000.0 * 0.22 - 141600.0 * 0.22 + 8448.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh872_sensibilita(**mh872_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_inverter",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh872_csv(bc, mh872_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_mecc_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh872_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh872_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh872_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 290000.0)
        bc = mh872_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def872\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh872_demo().keys()), lette - set(mh872_demo().keys()))
        self.assertEqual(lette, set(mh872_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc872\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc872\["([^"]+)"\]', src))
        attese = set(mh872_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 895)
        elif os.path.exists(_TITLES_SNAPSHOT):
            with open(_TITLES_SNAPSHOT, encoding="utf-8") as f:
                self.assertEqual(sum(1 for _ in f), 871)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab872:"), 1)
        self.assertTrue(src.startswith("    # W876"))

    def test_ui_tab872_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab872:"), 1)
        self.assertIn("def mh872_demo(", src_h)
        self.assertIn("def mh872_calcola(", src_h)
        self.assertIn("tab872", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Occhialeria / produzione occhiali e montature: stampaggio/fresatura efficienti + lucidatura efficiente + FV battono lavorazioni tradizionali + essiccazione a gas?", src)
        self.assertIn("👓 Occhialeria / produzione occhiali e montature: stampaggio/fresatura efficienti + lucidatura efficiente + FV battono lavorazioni tradizionali + essiccazione a gas?", src)
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
        chiavi = re.findall(r'key="(st872_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st872_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st872_calcola"', src)
        self.assertIn('key="st872_csv"', src)
        self.assertIn('key="st872_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg872"), src.index(".paiac("))
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
