"""Test nuova scheda maglieria /
capi in maglia: macchine elettroniche
efficienti + stiratura efficiente + FV
battono maglieria tradizionale +
vaporizzazione a gas?

Business case annuo di una maglieria,
guidato dai CAPI all'anno prodotti
(demo 80.000 capi/anno): macchine
tradizionali base 80.000 x 1,2 = 96.000
kWh/anno; stiratura base 80.000 x
0,5 = 40.000 kWh/anno; elettricita'
base totale 136.000 kWh/anno, costo
energia base 29.920 EUR/anno; gas base
80.000 x 0,25 = 20.000 Smc/anno,
costo gas base 18.000 EUR/anno; O&M
base 25.000 EUR/anno; costo base
72.920 EUR/anno; macchine elettroniche
efficienti 80.000 x 0,80 = 64.000
kWh/anno; stiratura efficiente
80.000 x 0,30 = 24.000 kWh/anno;
elettricita' alternativa 88.000
kWh/anno; kWp = sup x kwp/m2
(demo 140 kWp); E_pv 154.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 77.000 kWh/anno); immessa
77.000 kWh/anno; deficit 11.000
kWh/anno; ricavo immissione 6.160
EUR/anno; O&M alternativa 20.000
EUR/anno; C_alt 16.260 EUR/anno;
risparmio 56.660 EUR/anno; CAPEX
120.000 + 40.000 + 140 x 900 = 286.000
EUR; CO2 base = (gas x 1,96 +
E_base x 0,35) / 1000 = 86,80
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 3,85 t/anno (immessa senza
credito CO2); CO2 evitata 82,95
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt -
E_base x p_el - om_base) / gas in
forma chiusa (demo None: rapporto
negativo -1,933, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (capi <= 0, kWh per
capo < 0, prezzi < 0, O&M < 0,
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
Distinzione esplicita: NON tessitura
(niente telai, niente tessuto a navetta,
solo capi in maglia), NON tintoria
(niente tintura in vasca, niente bagni
di tintura, solo maglia finita da
stirare e vaporizzare), NON confezione
(niente taglio e niente cucito di capi,
solo capi in maglia con macchine per
maglieria e stiratura); qui solo
macchine per maglieria + stiratura + FV
su capi in maglia.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w878_helpers import (
        demo_calcoli,
        mh874_c_alt,
        mh874_c_base,
        mh874_calcola,
        mh874_capex_totale,
        mh874_co2_alt,
        mh874_co2_base,
        mh874_co2_evitata,
        mh874_csv,
        mh874_demo,
        mh874_demo_calcoli,
        mh874_e_alt,
        mh874_e_deficit,
        mh874_e_immessa,
        mh874_e_macch_alt,
        mh874_e_macch_base,
        mh874_e_stir_alt,
        mh874_e_stir_base,
        mh874_e_base,
        mh874_e_pv,
        mh874_e_pv_auto,
        mh874_flussi,
        mh874_frazione,
        mh874_gas_base,
        mh874_int_pos,
        mh874_kwp,
        mh874_nneg,
        mh874_num,
        mh874_p_gas_pareggio,
        mh874_payback,
        mh874_pos,
        mh874_ricavo_immissione,
        mh874_risparmio,
        mh874_sensibilita,
        mh874_tir,
        mh874_valida,
        mh874_van,
        mh874_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w878_helpers", os.path.join(_hf, "w878_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh874_c_alt = _mod.mh874_c_alt
    mh874_c_base = _mod.mh874_c_base
    mh874_calcola = _mod.mh874_calcola
    mh874_capex_totale = _mod.mh874_capex_totale
    mh874_co2_alt = _mod.mh874_co2_alt
    mh874_co2_base = _mod.mh874_co2_base
    mh874_co2_evitata = _mod.mh874_co2_evitata
    mh874_csv = _mod.mh874_csv
    mh874_demo = _mod.mh874_demo
    mh874_demo_calcoli = _mod.mh874_demo_calcoli
    mh874_e_alt = _mod.mh874_e_alt
    mh874_e_deficit = _mod.mh874_e_deficit
    mh874_e_immessa = _mod.mh874_e_immessa
    mh874_e_macch_alt = _mod.mh874_e_macch_alt
    mh874_e_macch_base = _mod.mh874_e_macch_base
    mh874_e_stir_alt = _mod.mh874_e_stir_alt
    mh874_e_stir_base = _mod.mh874_e_stir_base
    mh874_e_base = _mod.mh874_e_base
    mh874_e_pv = _mod.mh874_e_pv
    mh874_e_pv_auto = _mod.mh874_e_pv_auto
    mh874_flussi = _mod.mh874_flussi
    mh874_frazione = _mod.mh874_frazione
    mh874_gas_base = _mod.mh874_gas_base
    mh874_int_pos = _mod.mh874_int_pos
    mh874_kwp = _mod.mh874_kwp
    mh874_nneg = _mod.mh874_nneg
    mh874_num = _mod.mh874_num
    mh874_p_gas_pareggio = _mod.mh874_p_gas_pareggio
    mh874_payback = _mod.mh874_payback
    mh874_pos = _mod.mh874_pos
    mh874_ricavo_immissione = _mod.mh874_ricavo_immissione
    mh874_risparmio = _mod.mh874_risparmio
    mh874_sensibilita = _mod.mh874_sensibilita
    mh874_tir = _mod.mh874_tir
    mh874_valida = _mod.mh874_valida
    mh874_van = _mod.mh874_van
    mh874_verdetto = _mod.mh874_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w878_helpers.py")
_UI_PATH = _risolvi("w878_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "3"
_VECCHIO_TAB = "tab87" + "3"
_VECCHIO_ST = "st87" + "3_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_macch_base_kwh_anno": 96000.0,
    "e_stir_base_kwh_anno": 40000.0,
    "e_base_kwh_anno": 136000.0,
    "gas_base_smc_anno": 20000.0,
    "c_base_eur_anno": 72920.0,
    "e_macch_alt_kwh_anno": 64000.0,
    "e_stir_alt_kwh_anno": 24000.0,
    "e_alt_kwh_anno": 88000.0,
    "kwp": 140.0,
    "e_pv_kwh_anno": 154000.0,
    "e_pv_auto_kwh_anno": 77000.0,
    "e_immessa_kwh_anno": 77000.0,
    "e_deficit_kwh_anno": 11000.0,
    "ricavo_immissione_eur_anno": 6160.0,
    "c_alt_eur_anno": 16260.0,
    "risparmio_eur_anno": 56660.0,
    "capex_eur": 286000.0,
    "co2_base_t_anno": 86.8,
    "co2_alt_t_anno": 3.85,
    "co2_evitata_t_anno": 82.95,
    "van": 420108.83800831524,
    "tir": 19.222710120996734,
    "payback": 6,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh874_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh874_num(3, "x"), 3.0)
        self.assertEqual(mh874_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh874_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh874_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh874_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh874_pos(0, "x")
        with self.assertRaises(ValueError):
            mh874_pos(-1, "x")
        self.assertEqual(mh874_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh874_int_pos(20, "x"), 20)
        self.assertEqual(mh874_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh874_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh874_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh874_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh874_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh874_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh874_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_macch_e_stir_base_e_costo_base(self):
        self.assertEqual(mh874_e_macch_base(80000, 1.2), 96000.0)
        self.assertEqual(mh874_e_stir_base(80000, 0.5), 40000.0)
        self.assertEqual(mh874_e_base(96000.0, 40000.0), 136000.0)
        self.assertEqual(mh874_gas_base(80000, 0.25), 20000.0)
        self.assertEqual(mh874_c_base(136000.0, 0.22, 20000.0, 0.90,
                                       25000), 72920.0)

    def test_macch_alt_stir_alt_somma(self):
        self.assertEqual(mh874_e_macch_alt(80000, 0.80), 64000.0)
        self.assertEqual(mh874_e_stir_alt(80000, 0.30), 24000.0)
        self.assertEqual(mh874_e_alt(64000.0, 24000.0), 88000.0)
        # Le macchine elettroniche RIDUCONO il consumo,
        # non lo azzerano: 0,80 resta sopra zero anche
        # a parita' di base 1,2.
        self.assertGreater(mh874_e_macch_alt(80000, 0.80), 0.0)
        self.assertLess(mh874_e_macch_alt(80000, 0.80),
                        mh874_e_macch_base(80000, 1.2))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh874_kwp(700, 0.20), 140.0)
        self.assertEqual(mh874_e_pv(140.0, 1100), 154000.0)
        self.assertEqual(mh874_e_pv_auto(154000.0, 0.50, 88000.0),
                         77000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh874_e_pv_auto(154000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh874_e_immessa(154000.0, 77000.0), 77000.0)
        self.assertEqual(mh874_e_deficit(88000.0, 77000.0), 11000.0)
        self.assertEqual(mh874_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh874_ricavo_immissione(77000.0, 0.08), 6160.0)
        self.assertAlmostEqual(
            mh874_c_alt(11000.0, 0.22, 6160.0, 20000.0),
            16260.0)
        self.assertAlmostEqual(mh874_risparmio(72920.0, 16260.0),
                               56660.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh874_capex_totale(120000, 40000, 140.0,
                                            900),
                         286000.0)
        self.assertEqual(mh874_capex_totale(120000, 40000, 0.0,
                                            900),
                         160000.0)

    def test_co2_base_e_alt(self):
        cb = mh874_co2_base(20000.0, 1.96, 136000.0, 0.35)
        self.assertAlmostEqual(cb, 86.8, places=4)
        ca = mh874_co2_alt(11000.0, 0.35)
        self.assertAlmostEqual(ca, 3.85, places=4)
        self.assertAlmostEqual(mh874_co2_evitata(cb, ca), 82.95, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh874_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh874_flussi(286000, 56660.0, 3),
                         [-286000, 56660.0, 56660.0, 56660.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh874_van([-100, 60, 60], 0), 20.0)
        bc = mh874_demo_calcoli()
        self.assertAlmostEqual(mh874_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh874_demo_calcoli()
        tir = mh874_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh874_tir([-100, -10, -10]))
        self.assertIsNone(mh874_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh874_demo_calcoli()
        self.assertEqual(mh874_payback(bc["flussi"]), 6)
        self.assertIsNone(mh874_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh874_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh874_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:6]), -2700.0, places=2)
        self.assertAlmostEqual(sum(flussi[:7]), 53960.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh874_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh874_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh874_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh874_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh874_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh874_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh874_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh874_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -1.933, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh874_p_gas_pareggio(20000.0, 136000.0, 11000.0,
                                 0.22, 6160.0, 25000.0, 100000.0),
            2.067, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh874_p_gas_pareggio(20000.0, 136000.0,
                                              11000.0, 0.22, 6160.0,
                                              25000.0, 58660.0),
                         0.0)
        self.assertIsNone(mh874_p_gas_pareggio(0.0, 136000.0,
                                               11000.0, 0.22, 6160.0,
                                               25000.0, 20000.0))
        self.assertIsNone(mh874_p_gas_pareggio(20000.0, 136000.0,
                                               11000.0, 0.22, 6160.0,
                                               25000.0, 20000.0))

    def test_valida_demo_ok(self):
        demo = mh874_demo()
        val = mh874_valida(*[demo[k] for k in (
            "capi_anno", "e_macch_base_per_capo",
            "e_stir_base_per_capo", "p_el",
            "gas_per_capo", "p_gas", "om_base_eur_anno",
            "e_macch_alt_per_capo", "e_stir_alt_per_capo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_macchine_eur", "capex_stir_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_capi_zero_no(self):
        kw = _demo_kwargs(capi_anno=0)
        self.assertRaises(ValueError, mh874_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh874_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh874_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh874_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh874_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("capi_anno", -1),
                              ("e_macch_base_per_capo", -1),
                              ("p_gas", -0.01),
                              ("capex_macchine_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh874_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh874_calcola(mh874_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh874_calcola(dict(mh874_demo(), capex_macchine_eur=999999),
                           capex_macchine_eur=120000)
        self.assertEqual(bc["capex_eur"], 286000.0)


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
        self.assertEqual(bc["payback"], 6)

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
        s = mh874_sensibilita(**mh874_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               60260.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               464972.80, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               62160.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               488650.99, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               33560.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               258231.78, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 5)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 160000.0)
        self.assertAlmostEqual(s["senza_elettroniche"]["risparmio_eur_anno"],
                               49620.0, places=2)
        self.assertAlmostEqual(s["senza_elettroniche"]["van"],
                               332374.88, places=2)
        self.assertEqual(s["senza_elettroniche"]["payback"], 6)
        self.assertEqual(s["senza_elettroniche"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               134108.84, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 11)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               151513.50, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               847200.0, places=2)

    def test_marginale_con_capex_macchine_alto(self):
        # CAPEX totale 716.000 (macchine a 550.000):
        # VAN circa -9.891,16, entro la tolleranza del 10%
        # (71.600).
        bc = mh874_calcola(**_demo_kwargs(capex_macchine_eur=550000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -9891.16, places=2)

    def test_non_convente_con_capex_macchine_altissimo(self):
        bc = mh874_calcola(**_demo_kwargs(capex_macchine_eur=620000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -79891.16, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh874_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -23340.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh874_csv(bc, mh874_demo())
        for voce in ("capi_anno", "e_macch_base_kwh_anno",
                     "e_stir_base_kwh_anno", "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -286000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Capi (capi/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh874_c_alt(88000.0, 0.22, 0.0, 20000.0)
        con = mh874_c_alt(11000.0, 0.22, 6160.0, 20000.0)
        self.assertAlmostEqual(senza - con, 88000.0 * 0.22 - 11000.0 * 0.22 + 6160.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh874_sensibilita(**mh874_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_elettroniche",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh874_csv(bc, mh874_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_macch_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh874_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh874_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh874_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 160000.0)
        bc = mh874_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def874\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh874_demo().keys()), lette - set(mh874_demo().keys()))
        self.assertEqual(lette, set(mh874_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc874\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc874\["([^"]+)"\]', src))
        attese = set(mh874_demo_calcoli().keys())
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
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab874:"), 1)
        self.assertTrue(src.startswith("    # W878"))

    def test_ui_tab874_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab874:"), 1)
        self.assertIn("def mh874_demo(", src_h)
        self.assertIn("def mh874_calcola(", src_h)
        self.assertIn("tab874", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Maglieria / capi in maglia: macchine elettroniche efficienti + stiratura efficiente + FV battono maglieria tradizionale + vaporizzazione a gas?", src)
        self.assertIn("🧶 Maglieria / capi in maglia: macchine elettroniche efficienti + stiratura efficiente + FV battono maglieria tradizionale + vaporizzazione a gas?", src)
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
        chiavi = re.findall(r'key="(st874_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st874_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st874_calcola"', src)
        self.assertIn('key="st874_csv"', src)
        self.assertIn('key="st874_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg874"), src.index(".paiac("))
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
