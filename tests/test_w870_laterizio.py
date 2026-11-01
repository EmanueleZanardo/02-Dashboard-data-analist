"""Test nuova scheda laterizio: recupero
calore forno + essiccatoio efficiente +
FV battono forno ed essiccatoio
tradizionali a gas?

Business case annuo di un laterizio,
guidato dalle TONNELLATE all'anno di
laterizi prodotti (demo 30.000 t/anno):
gas forno base = t x kWh/t (demo
30.000 x 400 = 12.000.000 kWh/anno),
gas essiccatoio base 30.000 x 150 =
4.500.000 kWh/anno, gas base totale
16.500.000 kWh/anno, elettricita' base
30.000 x 60 = 1.800.000 kWh/anno, costo
base 2.001.000 EUR/anno; recupero calore
0,50: gas essiccatoio alternativo
2.250.000 kWh/anno, gas alternativo
totale 14.250.000 kWh/anno;
elettricita' alternativa 30.000 x 45 =
1.350.000 kWh/anno; kWp = sup x kwp/m2
(demo 1.000 kWp); E_pv 1.100.000
kWh/anno; E_pv_auto = min(E_pv x
f_autoconsumo, E_alt) (demo 660.000
kWh/anno); immessa 440.000 kWh/anno;
deficit 690.000 kWh/anno; ricavo
immissione 35.200 EUR/anno; O&M
alternativa 150.000 EUR/anno; C_alt
1.549.100 EUR/anno; risparmio 451.900
EUR/anno; CAPEX 400.000 + 250.000 +
1.000 x 450 = 1.100.000 EUR; CO2 base =
(gas base x 0,20 + E_base x 0,30) /
1000 = 3.840,00 t/anno; CO2 alt =
(gas alt x 0,20 + deficit x 0,30) /
1000 = 3.057,00 t/anno (immessa senza
credito CO2); CO2 evitata 783,00
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt - E_base x
p_el - om_base) / (gas_base - gas_alt)
in forma chiusa (demo None: rapporto
negativo -0,11084444, vince anche a gas
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
Distinzione esplicita: NON vetreria
(niente vetro fuso), NON ceramica
(niente smalto), NON cementificio
(niente clinker), NON pastificio
(niente essiccazione di pasta); qui
solo laterizi: forno a tunnel +
essiccatoio + elettricita' + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w870_helpers import (
        demo_calcoli,
        mh866_c_alt,
        mh866_c_base,
        mh866_calcola,
        mh866_capex_totale,
        mh866_co2_alt,
        mh866_co2_base,
        mh866_co2_evitata,
        mh866_csv,
        mh866_demo,
        mh866_demo_calcoli,
        mh866_e_alt,
        mh866_e_base,
        mh866_e_deficit,
        mh866_e_immessa,
        mh866_e_pv,
        mh866_e_pv_auto,
        mh866_flussi,
        mh866_frazione,
        mh866_gas_alt,
        mh866_gas_base,
        mh866_gas_ess_alt,
        mh866_gas_ess_base,
        mh866_gas_forno_base,
        mh866_int_pos,
        mh866_kwp,
        mh866_nneg,
        mh866_num,
        mh866_p_gas_pareggio,
        mh866_payback,
        mh866_pos,
        mh866_ricavo_immissione,
        mh866_risparmio,
        mh866_sensibilita,
        mh866_tir,
        mh866_valida,
        mh866_van,
        mh866_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w870_helpers", os.path.join(_hf, "w870_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh866_c_alt = _mod.mh866_c_alt
    mh866_c_base = _mod.mh866_c_base
    mh866_calcola = _mod.mh866_calcola
    mh866_capex_totale = _mod.mh866_capex_totale
    mh866_co2_alt = _mod.mh866_co2_alt
    mh866_co2_base = _mod.mh866_co2_base
    mh866_co2_evitata = _mod.mh866_co2_evitata
    mh866_csv = _mod.mh866_csv
    mh866_demo = _mod.mh866_demo
    mh866_demo_calcoli = _mod.mh866_demo_calcoli
    mh866_e_alt = _mod.mh866_e_alt
    mh866_e_base = _mod.mh866_e_base
    mh866_e_deficit = _mod.mh866_e_deficit
    mh866_e_immessa = _mod.mh866_e_immessa
    mh866_e_pv = _mod.mh866_e_pv
    mh866_e_pv_auto = _mod.mh866_e_pv_auto
    mh866_flussi = _mod.mh866_flussi
    mh866_frazione = _mod.mh866_frazione
    mh866_gas_alt = _mod.mh866_gas_alt
    mh866_gas_base = _mod.mh866_gas_base
    mh866_gas_ess_alt = _mod.mh866_gas_ess_alt
    mh866_gas_ess_base = _mod.mh866_gas_ess_base
    mh866_gas_forno_base = _mod.mh866_gas_forno_base
    mh866_int_pos = _mod.mh866_int_pos
    mh866_kwp = _mod.mh866_kwp
    mh866_nneg = _mod.mh866_nneg
    mh866_num = _mod.mh866_num
    mh866_p_gas_pareggio = _mod.mh866_p_gas_pareggio
    mh866_payback = _mod.mh866_payback
    mh866_pos = _mod.mh866_pos
    mh866_ricavo_immissione = _mod.mh866_ricavo_immissione
    mh866_risparmio = _mod.mh866_risparmio
    mh866_sensibilita = _mod.mh866_sensibilita
    mh866_tir = _mod.mh866_tir
    mh866_valida = _mod.mh866_valida
    mh866_van = _mod.mh866_van
    mh866_verdetto = _mod.mh866_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w870_helpers.py")
_UI_PATH = _risolvi("w870_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "5"
_VECCHIO_TAB = "tab86" + "5"
_VECCHIO_ST = "st86" + "5_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "gas_forno_base_kwh_anno": 12000000.0,
    "gas_ess_base_kwh_anno": 4500000.0,
    "gas_base_kwh_anno": 16500000.0,
    "e_base_kwh_anno": 1800000.0,
    "c_base_eur_anno": 2001000.0,
    "gas_ess_alt_kwh_anno": 2250000.0,
    "gas_alt_kwh_anno": 14250000.0,
    "e_alt_kwh_anno": 1350000.0,
    "kwp": 1000.0,
    "e_pv_kwh_anno": 1100000.0,
    "e_pv_auto_kwh_anno": 660000.0,
    "e_immessa_kwh_anno": 440000.0,
    "e_deficit_kwh_anno": 690000.0,
    "ricavo_immissione_eur_anno": 35200.0,
    "c_alt_eur_anno": 1549100.0,
    "risparmio_eur_anno": 451900.0,
    "capex_eur": 1100000.0,
    "co2_base_t_anno": 3840.0,
    "co2_alt_t_anno": 3057.0,
    "co2_evitata_t_anno": 783.0,
    "van": 4531672.853793818,
    "tir": 41.039469848839346,
    "payback": 3,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh866_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh866_num(3, "x"), 3.0)
        self.assertEqual(mh866_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh866_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh866_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh866_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh866_pos(0, "x")
        with self.assertRaises(ValueError):
            mh866_pos(-1, "x")
        self.assertEqual(mh866_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh866_int_pos(20, "x"), 20)
        self.assertEqual(mh866_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh866_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh866_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh866_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh866_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh866_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh866_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_gas_e_costo_base(self):
        self.assertEqual(mh866_gas_forno_base(30000, 400), 12000000.0)
        self.assertEqual(mh866_gas_ess_base(30000, 150), 4500000.0)
        self.assertEqual(mh866_gas_base(12000000.0, 4500000.0),
                         16500000.0)
        self.assertEqual(mh866_e_base(30000, 60), 1800000.0)
        self.assertEqual(mh866_c_base(16500000.0, 0.09, 1800000.0, 0.22,
                                       120000), 2001000.0)

    def test_recupero_riduce_solo_essiccatoio(self):
        self.assertEqual(mh866_gas_ess_alt(4500000.0, 0.50), 2250000.0)
        self.assertEqual(mh866_gas_ess_alt(4500000.0, 0.0), 4500000.0)
        self.assertEqual(mh866_gas_ess_alt(4500000.0, 1.0), 0.0)
        self.assertEqual(mh866_gas_alt(12000000.0, 2250000.0),
                         14250000.0)
        self.assertEqual(mh866_e_alt(30000, 45), 1350000.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh866_kwp(5000, 0.20), 1000.0)
        self.assertEqual(mh866_e_pv(1000.0, 1100), 1100000.0)
        self.assertEqual(mh866_e_pv_auto(1100000.0, 0.60, 1350000.0),
                         660000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh866_e_pv_auto(1100000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh866_e_immessa(1100000.0, 660000.0), 440000.0)
        self.assertEqual(mh866_e_deficit(1350000.0, 660000.0), 690000.0)
        self.assertEqual(mh866_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh866_ricavo_immissione(440000.0, 0.08), 35200.0)
        self.assertAlmostEqual(
            mh866_c_alt(14250000.0, 0.09, 690000.0, 0.22, 35200.0,
                        150000.0),
            1549100.0)
        self.assertAlmostEqual(mh866_risparmio(2001000.0, 1549100.0),
                               451900.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh866_capex_totale(400000, 250000, 1000.0,
                                            450),
                         1100000.0)
        self.assertEqual(mh866_capex_totale(400000, 250000, 0.0,
                                            450),
                         650000.0)

    def test_co2_base_e_alt(self):
        cb = mh866_co2_base(16500000.0, 0.20, 1800000.0, 0.30)
        self.assertAlmostEqual(cb, 3840.0, places=4)
        ca = mh866_co2_alt(14250000.0, 0.20, 690000.0, 0.30)
        self.assertAlmostEqual(ca, 3057.0, places=4)
        self.assertAlmostEqual(mh866_co2_evitata(cb, ca), 783.0, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # gas alternativo e deficit.
        self.assertEqual(mh866_co2_alt(0.0, 0.20, 0.0, 0.30), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh866_flussi(1100000, 451900.0, 3),
                         [-1100000, 451900.0, 451900.0, 451900.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh866_van([-100, 60, 60], 0), 20.0)
        bc = mh866_demo_calcoli()
        self.assertAlmostEqual(mh866_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh866_demo_calcoli()
        tir = mh866_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh866_tir([-100, -10, -10]))
        self.assertIsNone(mh866_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh866_demo_calcoli()
        self.assertEqual(mh866_payback(bc["flussi"]), 3)
        self.assertIsNone(mh866_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh866_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh866_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:3]), -196200.0, places=2)
        self.assertAlmostEqual(sum(flussi[:4]), 255700.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh866_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh866_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh866_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh866_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh866_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh866_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh866_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh866_demo_calcoli()
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
               - bc["gas_alt_kwh_anno"]), -0.11084444, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertEqual(mh866_p_gas_pareggio(16500000.0, 14250000.0,
                                             1800000.0, 690000.0,
                                             0.22, 35200.0,
                                             120000.0, 600000.0),
                         0.08915555555555556)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh866_p_gas_pareggio(16500000.0, 14250000.0,
                                             1800000.0, 690000.0,
                                             0.22, 35200.0,
                                             120000.0, 399400.0),
                         0.0)
        self.assertIsNone(mh866_p_gas_pareggio(14250000.0, 14250000.0,
                                              1800000.0, 690000.0,
                                              0.22, 35200.0,
                                              120000.0, 150000.0))
        self.assertIsNone(mh866_p_gas_pareggio(16500000.0, 14250000.0,
                                              1800000.0, 690000.0,
                                              0.22, 35200.0,
                                              120000.0, 150000.0))

    def test_valida_demo_ok(self):
        demo = mh866_demo()
        val = mh866_valida(*[demo[k] for k in (
            "t_anno", "q_forno_base_per_t", "q_ess_base_per_t",
            "e_base_per_t", "p_gas", "p_el", "om_base_eur_anno",
            "f_recupero", "e_alt_per_t", "sup_m2", "kwp_per_m2",
            "resa_fv", "f_autoconsumo", "p_immissione",
            "om_alt_eur_anno", "capex_recupero_eur", "capex_ess_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_kwh",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonnellate_zero_no(self):
        kw = _demo_kwargs(t_anno=0)
        self.assertRaises(ValueError, mh866_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh866_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh866_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh866_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh866_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh866_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("t_anno", -1),
                              ("q_forno_base_per_t", -1),
                              ("p_gas", -0.01),
                              ("capex_ess_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh866_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh866_calcola(mh866_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh866_calcola(dict(mh866_demo(), capex_ess_eur=999999),
                           capex_ess_eur=250000)
        self.assertEqual(bc["capex_eur"], 1100000.0)


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
        self.assertEqual(bc["payback"], 3)

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
        s = mh866_sensibilita(**mh866_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               492400.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               5036392.37, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 3)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               271500.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               2733490.11, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 3)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 650000.0)
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               249400.0, places=2)
        self.assertAlmostEqual(s["senza_recupero"]["van"],
                               2008075.26, places=2)
        self.assertEqual(s["senza_recupero"]["payback"], 5)
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["e_alt_uguale_base"]["risparmio_eur_anno"],
                               352900.0, places=2)
        self.assertAlmostEqual(s["e_alt_uguale_base"]["van"],
                               3297914.03, places=2)
        self.assertEqual(s["e_alt_uguale_base"]["payback"], 4)
        self.assertEqual(s["e_alt_uguale_base"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               3431672.85, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 5)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               2389452.01, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               7938000.0, places=2)

    def test_marginale_con_capex_recupero_alto(self):
        # CAPEX totale 6.100.000 (recupero a 5.500.000):
        # VAN circa -568.327, entro la tolleranza del 10%
        # (610.000).
        bc = mh866_calcola(**_demo_kwargs(capex_recupero_eur=5500000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -568327.15, places=2)

    def test_non_convente_con_capex_recupero_altissimo(self):
        bc = mh866_calcola(**_demo_kwargs(capex_recupero_eur=6500000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -1568327.15, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh866_calcola(**_demo_kwargs(om_alt_eur_anno=650000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -48100.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh866_csv(bc, mh866_demo())
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
                         -1100000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (t/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh866_c_alt(14250000.0, 0.09, 1350000.0, 0.22, 0.0,
                            150000.0)
        con = mh866_c_alt(14250000.0, 0.09, 690000.0, 0.22, 35200.0,
                          150000.0)
        self.assertAlmostEqual(senza - con, 1350000.0 * 0.22 - 690000.0 * 0.22 + 35200.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh866_sensibilita(**mh866_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "senza_fv",
                          "senza_recupero", "e_alt_uguale_base",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh866_csv(bc, mh866_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("gas_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh866_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh866_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh866_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 650000.0)
        bc = mh866_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def866\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh866_demo().keys()), lette - set(mh866_demo().keys()))
        self.assertEqual(lette, set(mh866_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc866\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc866\["([^"]+)"\]', src))
        attese = set(mh866_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab866:"), 1)
        self.assertTrue(src.startswith("    # W870"))

    def test_ui_tab866_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab866:"), 1)
        self.assertIn("def mh866_demo(", src_h)
        self.assertIn("def mh866_calcola(", src_h)
        self.assertIn("tab866", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Laterizio: recupero calore forno + essiccatoio efficiente + FV battono forno ed essiccatoio tradizionali a gas?", src)
        self.assertIn("🧱 Laterizio: recupero calore forno + essiccatoio efficiente + FV battono forno ed essiccatoio tradizionali a gas?", src)
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
        chiavi = re.findall(r'key="(st866_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st866_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st866_calcola"', src)
        self.assertIn('key="st866_csv"', src)
        self.assertIn('key="st866_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg866"), src.index(".paiac("))
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
