"""Test nuova scheda pelletteria /
produzione borse, cinture e portafogli
in pelle finita: taglio laser +
rifinitura efficiente + FV battono
taglio/cucitura tradizionali +
essiccazione a gas?

Business case annuo di una pelletteria,
guidato dai PEZZI all'anno prodotti
(demo 120.000 pezzi/anno): taglio/
cucitura base 120.000 x 0,9 = 108.000
kWh/anno; rifinitura base 120.000 x
0,4 = 48.000 kWh/anno; elettricita'
base totale 156.000 kWh/anno, costo
energia base 34.320 EUR/anno; gas base
120.000 x 0,20 = 24.000 Smc/anno,
costo gas base 21.600 EUR/anno; O&M
base 28.000 EUR/anno; costo base
83.920 EUR/anno; taglio laser/CNC con
inverter 120.000 x 0,65 = 78.000
kWh/anno; rifinitura efficiente
120.000 x 0,25 = 30.000 kWh/anno;
elettricita' alternativa 108.000
kWh/anno; kWp = sup x kwp/m2
(demo 160 kWp); E_pv 176.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 105.600 kWh/anno); immessa
70.400 kWh/anno; deficit 2.400
kWh/anno; ricavo immissione 5.632
EUR/anno; O&M alternativa 22.000
EUR/anno; C_alt 16.896 EUR/anno;
risparmio 67.024 EUR/anno; CAPEX
150.000 + 50.000 + 160 x 900 = 344.000
EUR; CO2 base = (gas x 1,96 +
E_base x 0,35) / 1000 = 101,64
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 0,84 t/anno (immessa senza
credito CO2); CO2 evitata 100,80
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt -
E_base x p_el - om_base) / gas in
forma chiusa (demo None: rapporto
negativo -1,89267, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (pezzi <= 0, kWh per
pezzo < 0, prezzi < 0, O&M < 0,
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
Distinzione esplicita: NON conceria
(niente concia, niente pelli grezze,
solo pelle finita), NON calzaturificio
(niente scarpe, solo borse, cinture e
portafogli), NON occhialeria (niente
montature di occhiali in acetato e
metallo, solo pelletteria in pelle
finita); qui solo taglio/cucitura +
rifinitura + FV su pezzi di pelletteria.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w877_helpers import (
        demo_calcoli,
        mh873_c_alt,
        mh873_c_base,
        mh873_calcola,
        mh873_capex_totale,
        mh873_co2_alt,
        mh873_co2_base,
        mh873_co2_evitata,
        mh873_csv,
        mh873_demo,
        mh873_demo_calcoli,
        mh873_e_alt,
        mh873_e_deficit,
        mh873_e_immessa,
        mh873_e_laser_alt,
        mh873_e_rif_alt,
        mh873_e_rif_base,
        mh873_e_base,
        mh873_e_pv,
        mh873_e_pv_auto,
        mh873_e_taglio_cuc_base,
        mh873_flussi,
        mh873_frazione,
        mh873_gas_base,
        mh873_int_pos,
        mh873_kwp,
        mh873_nneg,
        mh873_num,
        mh873_p_gas_pareggio,
        mh873_payback,
        mh873_pos,
        mh873_ricavo_immissione,
        mh873_risparmio,
        mh873_sensibilita,
        mh873_tir,
        mh873_valida,
        mh873_van,
        mh873_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w877_helpers", os.path.join(_hf, "w877_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh873_c_alt = _mod.mh873_c_alt
    mh873_c_base = _mod.mh873_c_base
    mh873_calcola = _mod.mh873_calcola
    mh873_capex_totale = _mod.mh873_capex_totale
    mh873_co2_alt = _mod.mh873_co2_alt
    mh873_co2_base = _mod.mh873_co2_base
    mh873_co2_evitata = _mod.mh873_co2_evitata
    mh873_csv = _mod.mh873_csv
    mh873_demo = _mod.mh873_demo
    mh873_demo_calcoli = _mod.mh873_demo_calcoli
    mh873_e_alt = _mod.mh873_e_alt
    mh873_e_deficit = _mod.mh873_e_deficit
    mh873_e_immessa = _mod.mh873_e_immessa
    mh873_e_laser_alt = _mod.mh873_e_laser_alt
    mh873_e_rif_alt = _mod.mh873_e_rif_alt
    mh873_e_rif_base = _mod.mh873_e_rif_base
    mh873_e_base = _mod.mh873_e_base
    mh873_e_pv = _mod.mh873_e_pv
    mh873_e_pv_auto = _mod.mh873_e_pv_auto
    mh873_e_taglio_cuc_base = _mod.mh873_e_taglio_cuc_base
    mh873_flussi = _mod.mh873_flussi
    mh873_frazione = _mod.mh873_frazione
    mh873_gas_base = _mod.mh873_gas_base
    mh873_int_pos = _mod.mh873_int_pos
    mh873_kwp = _mod.mh873_kwp
    mh873_nneg = _mod.mh873_nneg
    mh873_num = _mod.mh873_num
    mh873_p_gas_pareggio = _mod.mh873_p_gas_pareggio
    mh873_payback = _mod.mh873_payback
    mh873_pos = _mod.mh873_pos
    mh873_ricavo_immissione = _mod.mh873_ricavo_immissione
    mh873_risparmio = _mod.mh873_risparmio
    mh873_sensibilita = _mod.mh873_sensibilita
    mh873_tir = _mod.mh873_tir
    mh873_valida = _mod.mh873_valida
    mh873_van = _mod.mh873_van
    mh873_verdetto = _mod.mh873_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w877_helpers.py")
_UI_PATH = _risolvi("w877_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "2"
_VECCHIO_TAB = "tab87" + "2"
_VECCHIO_ST = "st87" + "2_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_taglio_cuc_base_kwh_anno": 108000.0,
    "e_rif_base_kwh_anno": 48000.0,
    "e_base_kwh_anno": 156000.0,
    "gas_base_smc_anno": 24000.0,
    "c_base_eur_anno": 83920.0,
    "e_laser_alt_kwh_anno": 78000.0,
    "e_rif_alt_kwh_anno": 30000.0,
    "e_alt_kwh_anno": 108000.0,
    "kwp": 160.0,
    "e_pv_kwh_anno": 176000.0,
    "e_pv_auto_kwh_anno": 105600.0,
    "e_immessa_kwh_anno": 70400.0,
    "e_deficit_kwh_anno": 2400.0,
    "ricavo_immissione_eur_anno": 5632.0,
    "c_alt_eur_anno": 16896.0,
    "risparmio_eur_anno": 67024.0,
    "capex_eur": 344000.0,
    "co2_base_t_anno": 101.64,
    "co2_alt_t_anno": 0.84,
    "co2_evitata_t_anno": 100.80,
    "van": 491267.1859983996,
    "tir": 18.869596884634554,
    "payback": 6,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh873_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh873_num(3, "x"), 3.0)
        self.assertEqual(mh873_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh873_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh873_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh873_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh873_pos(0, "x")
        with self.assertRaises(ValueError):
            mh873_pos(-1, "x")
        self.assertEqual(mh873_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh873_int_pos(20, "x"), 20)
        self.assertEqual(mh873_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh873_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh873_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh873_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh873_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh873_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh873_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_taglio_cuc_e_rif_base_e_costo_base(self):
        self.assertEqual(mh873_e_taglio_cuc_base(120000, 0.9), 108000.0)
        self.assertEqual(mh873_e_rif_base(120000, 0.4), 48000.0)
        self.assertEqual(mh873_e_base(108000.0, 48000.0), 156000.0)
        self.assertEqual(mh873_gas_base(120000, 0.20), 24000.0)
        self.assertEqual(mh873_c_base(156000.0, 0.22, 24000.0, 0.90,
                                       28000), 83920.0)

    def test_laser_alt_rif_alt_somma(self):
        self.assertEqual(mh873_e_laser_alt(120000, 0.65), 78000.0)
        self.assertEqual(mh873_e_rif_alt(120000, 0.25), 30000.0)
        self.assertEqual(mh873_e_alt(78000.0, 30000.0), 108000.0)
        # Il laser RIDUCE il taglio, non lo azzera:
        # 0,65 resta sopra zero anche a parita' di base 0,9.
        self.assertGreater(mh873_e_laser_alt(120000, 0.65), 0.0)
        self.assertLess(mh873_e_laser_alt(120000, 0.65),
                        mh873_e_taglio_cuc_base(120000, 0.9))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh873_kwp(800, 0.20), 160.0)
        self.assertEqual(mh873_e_pv(160.0, 1100), 176000.0)
        self.assertEqual(mh873_e_pv_auto(176000.0, 0.60, 108000.0),
                         105600.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh873_e_pv_auto(176000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh873_e_immessa(176000.0, 105600.0), 70400.0)
        self.assertEqual(mh873_e_deficit(108000.0, 105600.0), 2400.0)
        self.assertEqual(mh873_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh873_ricavo_immissione(70400.0, 0.08), 5632.0)
        self.assertAlmostEqual(
            mh873_c_alt(2400.0, 0.22, 5632.0, 22000.0),
            16896.0)
        self.assertAlmostEqual(mh873_risparmio(83920.0, 16896.0),
                               67024.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh873_capex_totale(150000, 50000, 160.0,
                                            900),
                         344000.0)
        self.assertEqual(mh873_capex_totale(150000, 50000, 0.0,
                                            900),
                         200000.0)

    def test_co2_base_e_alt(self):
        cb = mh873_co2_base(24000.0, 1.96, 156000.0, 0.35)
        self.assertAlmostEqual(cb, 101.64, places=4)
        ca = mh873_co2_alt(2400.0, 0.35)
        self.assertAlmostEqual(ca, 0.84, places=4)
        self.assertAlmostEqual(mh873_co2_evitata(cb, ca), 100.80, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh873_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh873_flussi(344000, 67024.0, 3),
                         [-344000, 67024.0, 67024.0, 67024.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh873_van([-100, 60, 60], 0), 20.0)
        bc = mh873_demo_calcoli()
        self.assertAlmostEqual(mh873_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh873_demo_calcoli()
        tir = mh873_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh873_tir([-100, -10, -10]))
        self.assertIsNone(mh873_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh873_demo_calcoli()
        self.assertEqual(mh873_payback(bc["flussi"]), 6)
        self.assertIsNone(mh873_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh873_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh873_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:6]), -8880.0, places=2)
        self.assertAlmostEqual(sum(flussi[:7]), 58144.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh873_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh873_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh873_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh873_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh873_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh873_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh873_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh873_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -1.8926666666666667, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh873_p_gas_pareggio(24000.0, 156000.0, 2400.0,
                                 0.22, 5632.0, 28000.0, 100000.0),
            1.3573333333333333, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh873_p_gas_pareggio(24000.0, 156000.0,
                                              2400.0, 0.22, 5632.0,
                                              28000.0, 67424.0),
                         0.0)
        self.assertIsNone(mh873_p_gas_pareggio(0.0, 156000.0,
                                               2400.0, 0.22, 5632.0,
                                               28000.0, 22000.0))
        self.assertIsNone(mh873_p_gas_pareggio(24000.0, 156000.0,
                                               2400.0, 0.22, 5632.0,
                                               28000.0, 22000.0))

    def test_valida_demo_ok(self):
        demo = mh873_demo()
        val = mh873_valida(*[demo[k] for k in (
            "pezzi_anno", "e_taglio_cuc_base_per_pezzo",
            "e_rif_base_per_pezzo", "p_el",
            "gas_per_pezzo", "p_gas", "om_base_eur_anno",
            "e_laser_alt_per_pezzo", "e_rif_alt_per_pezzo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_taglio_eur", "capex_rif_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_pezzi_zero_no(self):
        kw = _demo_kwargs(pezzi_anno=0)
        self.assertRaises(ValueError, mh873_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh873_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh873_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh873_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh873_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("pezzi_anno", -1),
                              ("e_taglio_cuc_base_per_pezzo", -1),
                              ("p_gas", -0.01),
                              ("capex_taglio_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh873_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh873_calcola(mh873_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh873_calcola(dict(mh873_demo(), capex_taglio_eur=999999),
                           capex_taglio_eur=150000)
        self.assertEqual(bc["capex_eur"], 344000.0)


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
        s = mh873_sensibilita(**mh873_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               71344.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               545103.93, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               73782.4, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               575491.79, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               38160.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               275557.95, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 6)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 200000.0)
        self.assertAlmostEqual(s["senza_laser"]["risparmio_eur_anno"],
                               60424.0, places=2)
        self.assertAlmostEqual(s["senza_laser"]["van"],
                               409016.60, places=2)
        self.assertEqual(s["senza_laser"]["payback"], 6)
        self.assertEqual(s["senza_laser"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               147267.19, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 11)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               173541.56, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               996480.0, places=2)

    def test_marginale_con_capex_taglio_alto(self):
        # CAPEX totale 844.000 (taglio a 650.000):
        # VAN circa -8.732,81, entro la tolleranza del 10%
        # (84.400).
        bc = mh873_calcola(**_demo_kwargs(capex_taglio_eur=650000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -8732.81, places=2)

    def test_non_convente_con_capex_taglio_altissimo(self):
        bc = mh873_calcola(**_demo_kwargs(capex_taglio_eur=900000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -258732.81, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh873_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -10976.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh873_csv(bc, mh873_demo())
        for voce in ("pezzi_anno", "e_taglio_cuc_base_kwh_anno",
                     "e_rif_base_kwh_anno", "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -344000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Pezzi (pezzi/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh873_c_alt(108000.0, 0.22, 0.0, 22000.0)
        con = mh873_c_alt(2400.0, 0.22, 5632.0, 22000.0)
        self.assertAlmostEqual(senza - con, 108000.0 * 0.22 - 2400.0 * 0.22 + 5632.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh873_sensibilita(**mh873_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_laser",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh873_csv(bc, mh873_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_taglio_cuc_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh873_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh873_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh873_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 200000.0)
        bc = mh873_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def873\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh873_demo().keys()), lette - set(mh873_demo().keys()))
        self.assertEqual(lette, set(mh873_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc873\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc873\["([^"]+)"\]', src))
        attese = set(mh873_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 891)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab873:"), 1)
        self.assertTrue(src.startswith("    # W877"))

    def test_ui_tab873_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab873:"), 1)
        self.assertIn("def mh873_demo(", src_h)
        self.assertIn("def mh873_calcola(", src_h)
        self.assertIn("tab873", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Pelletteria / borse, cinture e portafogli: taglio laser + rifinitura efficiente + FV battono taglio/cucitura tradizionali + essiccazione a gas?", src)
        self.assertIn("👜 Pelletteria / borse, cinture e portafogli: taglio laser + rifinitura efficiente + FV battono taglio/cucitura tradizionali + essiccazione a gas?", src)
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
        chiavi = re.findall(r'key="(st873_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st873_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st873_calcola"', src)
        self.assertIn('key="st873_csv"', src)
        self.assertIn('key="st873_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg873"), src.index(".paiac("))
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
