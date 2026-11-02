"""Test nuova scheda carpenteria metallica:
taglio laser efficiente +
saldatura efficiente + FV battono
taglio plasma tradizionale +
saldatura tradizionale + gas per
preriscaldo?

Business case annuo di una carpenteria
metallica, guidato dalle TONNELLATE
all'anno prodotte (demo 500
tonnellate/anno):
taglio plasma tradizionale base
500 x 180 = 90.000 kWh/anno;
saldatura base 500 x 120 = 60.000
kWh/anno; elettricita' base totale
150.000 kWh/anno, costo energia base
33.000 EUR/anno; gas base 500 x 25
= 12.500 Smc/anno, costo gas base 11.250
EUR/anno; O&M base 40.000 EUR/anno;
costo base 84.250 EUR/anno; taglio laser
efficiente 500 x 110 =
55.000 kWh/anno; saldatura efficiente
500 x 70 = 35.000 kWh/anno;
elettricita' alternativa 90.000
kWh/anno; kWp = sup x kwp/m2
(demo 160 kWp); E_pv 176.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 88.000 kWh/anno); immessa
88.000 kWh/anno; deficit 2.000 kWh/anno;
ricavo immissione 7.040 EUR/anno; O&M
alternativa 30.000 EUR/anno; C_alt
23.400 EUR/anno; risparmio 60.850
EUR/anno; CAPEX 150.000 + 80.000 + 160 x
900 = 374.000 EUR; CO2 base = (gas x
1,96 + E_base x 0,35) / 1000 = 77,0
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 0,7 t/anno (immessa senza
credito CO2); CO2 evitata 76,3
t/anno; flussi [CAPEX negativo, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el meno
ricavo_immissione piu' om_alt meno
E_base x p_el meno om_base) / gas in
forma chiusa (demo None: rapporto
negativo meno 3,968, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (tonnellate <= 0, kWh per
tonnellata < 0, prezzi < 0, O&M < 0,
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
fonderia (niente fusione, solo acciaio
gia' laminato da tagliare e saldare),
NON falegnameria (niente legno, solo
acciaio), NON serramentificio (niente
serramenti finiti, solo carpenteria
metallica strutturale da tagliare e
saldare); qui solo taglio + saldatura
+ gas per preriscaldo + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w881_helpers import (
        demo_calcoli,
        mh877_c_alt,
        mh877_c_base,
        mh877_calcola,
        mh877_capex_totale,
        mh877_co2_alt,
        mh877_co2_base,
        mh877_co2_evitata,
        mh877_csv,
        mh877_demo,
        mh877_demo_calcoli,
        mh877_e_alt,
        mh877_e_deficit,
        mh877_e_immessa,
        mh877_e_tag_alt,
        mh877_e_tag_base,
        mh877_e_sal_alt,
        mh877_e_sal_base,
        mh877_e_base,
        mh877_e_pv,
        mh877_e_pv_auto,
        mh877_flussi,
        mh877_frazione,
        mh877_gas_base,
        mh877_int_pos,
        mh877_kwp,
        mh877_nneg,
        mh877_num,
        mh877_p_gas_pareggio,
        mh877_payback,
        mh877_pos,
        mh877_ricavo_immissione,
        mh877_risparmio,
        mh877_sensibilita,
        mh877_tir,
        mh877_valida,
        mh877_van,
        mh877_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w881_helpers", os.path.join(_hf, "w881_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh877_c_alt = _mod.mh877_c_alt
    mh877_c_base = _mod.mh877_c_base
    mh877_calcola = _mod.mh877_calcola
    mh877_capex_totale = _mod.mh877_capex_totale
    mh877_co2_alt = _mod.mh877_co2_alt
    mh877_co2_base = _mod.mh877_co2_base
    mh877_co2_evitata = _mod.mh877_co2_evitata
    mh877_csv = _mod.mh877_csv
    mh877_demo = _mod.mh877_demo
    mh877_demo_calcoli = _mod.mh877_demo_calcoli
    mh877_e_alt = _mod.mh877_e_alt
    mh877_e_deficit = _mod.mh877_e_deficit
    mh877_e_immessa = _mod.mh877_e_immessa
    mh877_e_tag_alt = _mod.mh877_e_tag_alt
    mh877_e_tag_base = _mod.mh877_e_tag_base
    mh877_e_sal_alt = _mod.mh877_e_sal_alt
    mh877_e_sal_base = _mod.mh877_e_sal_base
    mh877_e_base = _mod.mh877_e_base
    mh877_e_pv = _mod.mh877_e_pv
    mh877_e_pv_auto = _mod.mh877_e_pv_auto
    mh877_flussi = _mod.mh877_flussi
    mh877_frazione = _mod.mh877_frazione
    mh877_gas_base = _mod.mh877_gas_base
    mh877_int_pos = _mod.mh877_int_pos
    mh877_kwp = _mod.mh877_kwp
    mh877_nneg = _mod.mh877_nneg
    mh877_num = _mod.mh877_num
    mh877_p_gas_pareggio = _mod.mh877_p_gas_pareggio
    mh877_payback = _mod.mh877_payback
    mh877_pos = _mod.mh877_pos
    mh877_ricavo_immissione = _mod.mh877_ricavo_immissione
    mh877_risparmio = _mod.mh877_risparmio
    mh877_sensibilita = _mod.mh877_sensibilita
    mh877_tir = _mod.mh877_tir
    mh877_valida = _mod.mh877_valida
    mh877_van = _mod.mh877_van
    mh877_verdetto = _mod.mh877_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w881_helpers.py")
_UI_PATH = _risolvi("w881_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "6"
_VECCHIO_TAB = "tab87" + "6"
_VECCHIO_ST = "st87" + "6_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_tag_base_kwh_anno": 90000.0,
    "e_sal_base_kwh_anno": 60000.0,
    "e_base_kwh_anno": 150000.0,
    "gas_base_smc_anno": 12500.0,
    "c_base_eur_anno": 84250.0,
    "e_tag_alt_kwh_anno": 55000.0,
    "e_sal_alt_kwh_anno": 35000.0,
    "e_alt_kwh_anno": 90000.0,
    "kwp": 160.0,
    "e_pv_kwh_anno": 176000.0,
    "e_pv_auto_kwh_anno": 88000.0,
    "e_immessa_kwh_anno": 88000.0,
    "e_deficit_kwh_anno": 2000.0,
    "ricavo_immissione_eur_anno": 7040.0,
    "c_alt_eur_anno": 23400.0,
    "risparmio_eur_anno": 60850.0,
    "capex_eur": 374000.0,
    "co2_base_t_anno": 77.0,
    "co2_alt_t_anno": 0.7,
    "co2_evitata_t_anno": 76.3,
    "van": 384325.4993435579,
    "tir": 15.331574469415783,
    "payback": 7,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh877_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh877_num(3, "x"), 3.0)
        self.assertEqual(mh877_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh877_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh877_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh877_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh877_pos(0, "x")
        with self.assertRaises(ValueError):
            mh877_pos(-1, "x")
        self.assertEqual(mh877_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh877_int_pos(20, "x"), 20)
        self.assertEqual(mh877_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh877_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh877_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh877_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh877_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh877_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh877_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_tag_e_sal_base_e_costo_base(self):
        self.assertEqual(mh877_e_tag_base(500, 180), 90000.0)
        self.assertEqual(mh877_e_sal_base(500, 120), 60000.0)
        self.assertEqual(mh877_e_base(90000.0, 60000.0), 150000.0)
        self.assertEqual(mh877_gas_base(500, 25), 12500.0)
        self.assertEqual(mh877_c_base(150000.0, 0.22, 12500.0, 0.90,
                                       40000), 84250.0)

    def test_tag_alt_sal_alt_somma(self):
        self.assertEqual(mh877_e_tag_alt(500, 110), 55000.0)
        self.assertEqual(mh877_e_sal_alt(500, 70), 35000.0)
        self.assertEqual(mh877_e_alt(55000.0, 35000.0), 90000.0)
        # Il taglio laser RIDUCE il consumo,
        # non lo azzera: 110 resta sopra zero anche
        # a parita' di base 180.
        self.assertGreater(mh877_e_tag_alt(500, 110), 0.0)
        self.assertLess(mh877_e_tag_alt(500, 110),
                        mh877_e_tag_base(500, 180))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh877_kwp(800, 0.20), 160.0)
        self.assertEqual(mh877_e_pv(160.0, 1100), 176000.0)
        self.assertEqual(mh877_e_pv_auto(176000.0, 0.50, 90000.0),
                         88000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh877_e_pv_auto(176000.0, 1.0, 50000.0), 50000.0)
        self.assertEqual(mh877_e_immessa(176000.0, 88000.0), 88000.0)
        self.assertEqual(mh877_e_deficit(90000.0, 88000.0), 2000.0)
        self.assertEqual(mh877_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh877_ricavo_immissione(88000.0, 0.08), 7040.0)
        self.assertAlmostEqual(
            mh877_c_alt(2000.0, 0.22, 7040.0, 30000.0),
            23400.0)
        self.assertAlmostEqual(mh877_risparmio(84250.0, 23400.0),
                               60850.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh877_capex_totale(150000, 80000, 160.0,
                                            900),
                         374000.0)
        self.assertEqual(mh877_capex_totale(150000, 80000, 0.0,
                                            900),
                         230000.0)

    def test_co2_base_e_alt(self):
        cb = mh877_co2_base(12500.0, 1.96, 150000.0, 0.35)
        self.assertAlmostEqual(cb, 77.0, places=4)
        ca = mh877_co2_alt(2000.0, 0.35)
        self.assertAlmostEqual(ca, 0.7, places=4)
        self.assertAlmostEqual(mh877_co2_evitata(cb, ca), 76.3, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh877_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh877_flussi(374000, 60850.0, 3),
                         [-374000, 60850.0, 60850.0, 60850.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh877_van([-100, 60, 60], 0), 20.0)
        bc = mh877_demo_calcoli()
        self.assertAlmostEqual(mh877_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh877_demo_calcoli()
        tir = mh877_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh877_tir([-100, -10, -10]))
        self.assertIsNone(mh877_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh877_demo_calcoli()
        self.assertEqual(mh877_payback(bc["flussi"]), 7)
        self.assertIsNone(mh877_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh877_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh877_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:7]), -8900.0, places=2)
        self.assertAlmostEqual(sum(flussi[:8]), 51950.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh877_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh877_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh877_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh877_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh877_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh877_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh877_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh877_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -3.968, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh877_p_gas_pareggio(12500.0, 150000.0, 2000.0,
                                 0.22, 7040.0, 40000.0, 200000.0),
            9.632, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh877_p_gas_pareggio(12500.0, 150000.0,
                                              2000.0, 0.22, 7040.0,
                                              40000.0, 79600.0),
                         0.0)
        self.assertIsNone(mh877_p_gas_pareggio(0.0, 150000.0,
                                               2000.0, 0.22, 7040.0,
                                               40000.0, 30000.0))
        self.assertIsNone(mh877_p_gas_pareggio(12500.0, 150000.0,
                                               2000.0, 0.22, 7040.0,
                                               40000.0, 30000.0))

    def test_valida_demo_ok(self):
        demo = mh877_demo()
        val = mh877_valida(*[demo[k] for k in (
            "tonn_anno", "e_tag_base_per_t",
            "e_sal_base_per_t", "p_el",
            "gas_per_t", "p_gas", "om_base_eur_anno",
            "e_tag_alt_per_t", "e_sal_alt_per_t", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_tag_eur", "capex_sal_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonn_zero_no(self):
        kw = _demo_kwargs(tonn_anno=0)
        self.assertRaises(ValueError, mh877_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh877_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh877_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh877_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh877_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("tonn_anno", -1),
                              ("e_tag_base_per_t", -1),
                              ("p_gas", -0.01),
                              ("capex_tag_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh877_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh877_calcola(mh877_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh877_calcola(dict(mh877_demo(), capex_tag_eur=999999),
                           capex_tag_eur=150000)
        self.assertEqual(bc["capex_eur"], 374000.0)


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
        s = mh877_sensibilita(**mh877_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               63100.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               412365.47, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               67362.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               465479.41, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               34450.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               199323.15, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 7)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 230000.0)
        self.assertAlmostEqual(s["senza_laser"]["risparmio_eur_anno"],
                               53150.0, places=2)
        self.assertAlmostEqual(s["senza_laser"]["van"],
                               288366.48, places=2)
        self.assertEqual(s["senza_laser"]["payback"], 8)
        self.assertEqual(s["senza_laser"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               10325.50, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 13)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               95867.57, places=2)
        self.assertEqual(s["vita_10"]["payback"], 7)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               843000.0, places=2)

    def test_marginale_con_capex_tag_alto(self):
        # CAPEX totale 804.000 (taglio a 580.000):
        # VAN circa meno 45.674,50, entro la tolleranza del 10%
        # (80.400).
        bc = mh877_calcola(**_demo_kwargs(capex_tag_eur=580000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -45674.50, places=2)

    def test_non_convente_con_capex_tag_altissimo(self):
        bc = mh877_calcola(**_demo_kwargs(capex_tag_eur=700000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -165674.50, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh877_calcola(**_demo_kwargs(om_alt_eur_anno=200000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -109150.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh877_csv(bc, mh877_demo())
        for voce in ("tonn_anno", "e_tag_base_kwh_anno",
                     "e_sal_base_kwh_anno", "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -374000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (tonnellate/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh877_c_alt(90000.0, 0.22, 0.0, 30000.0)
        con = mh877_c_alt(2000.0, 0.22, 7040.0, 30000.0)
        self.assertAlmostEqual(senza - con, 90000.0 * 0.22 - 2000.0 * 0.22 + 7040.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh877_sensibilita(**mh877_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_laser",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh877_csv(bc, mh877_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_tag_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh877_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh877_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh877_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 230000.0)
        bc = mh877_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def877\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh877_demo().keys()), lette - set(mh877_demo().keys()))
        self.assertEqual(lette, set(mh877_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc877\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc877\["([^"]+)"\]', src))
        attese = set(mh877_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 884)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab877:"), 1)
        self.assertTrue(src.startswith("    # W881"))

    def test_ui_tab877_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab877:"), 1)
        self.assertIn("def mh877_demo(", src_h)
        self.assertIn("def mh877_calcola(", src_h)
        self.assertIn("tab877", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Carpenteria metallica: taglio laser efficiente + saldatura efficiente + FV battono taglio plasma tradizionale + saldatura tradizionale + gas per preriscaldo?", src)
        self.assertIn("🏭 Carpenteria metallica: taglio laser efficiente + saldatura efficiente + FV battono taglio plasma tradizionale + saldatura tradizionale + gas per preriscaldo?", src)
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
        chiavi = re.findall(r'key="(st877_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st877_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st877_calcola"', src)
        self.assertIn('key="st877_csv"', src)
        self.assertIn('key="st877_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg877"), src.index(".paiac("))
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
