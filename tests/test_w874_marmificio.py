"""Test nuova scheda marmificio /
lavorazione marmo e pietra: seghe
diamantate con inverter + lucidatura
efficiente + FV battono seghe
tradizionali + essiccazione a gas?

Business case annuo di un marmificio,
guidato dai METRI QUADRI all'anno di
lastre lavorate (demo 60.000 m2/anno):
seghe base 60.000 x 6,0 = 360.000
kWh/anno, costo energia seghe base
79.200 EUR/anno; gas base 60.000 x 0,8
= 48.000 Smc/anno, costo gas base
43.200 EUR/anno; O&M base 50.000
EUR/anno; costo base 172.400 EUR/anno;
seghe diamantate con inverter 60.000 x
4,0 = 240.000 kWh/anno; lucidatura
efficiente 60.000 x 2,5 = 150.000
kWh/anno; elettricita' alternativa
390.000 kWh/anno; kWp = sup x kwp/m2
(demo 400 kWp); E_pv 440.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 264.000 kWh/anno); immessa
176.000 kWh/anno; deficit 126.000
kWh/anno; ricavo immissione 14.080
EUR/anno; O&M alternativa 40.000
EUR/anno; C_alt 53.640 EUR/anno;
risparmio 118.760 EUR/anno; CAPEX
350.000 + 150.000 + 400 x 900 = 860.000
EUR; CO2 base = (gas x 1,96 +
E_seghe_base x 0,35) / 1000 = 220,08
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 44,10 t/anno (immessa senza
credito CO2); CO2 evitata 175,98
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt -
E_seghe_base x p_el - om_base) / gas in
forma chiusa (demo None: rapporto
negativo -1,57417, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (metri quadri <= 0, kWh per m2
< 0, prezzi < 0, O&M < 0, superficie < 0,
kwp per m2 < 0, resa < 0, f_autoconsumo
< 0 o > 1, voci CAPEX < 0, fattori CO2 <
0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON cava /
frantumazione inerti (niente inerti
sfusi e niente frantoi), NON segheria
(niente legno), NON laterizio e NON
forno ceramico (niente cottura), NON
vetreria (niente fusione); qui solo
taglio e lucidatura di lastre di marmo
e pietra + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w874_helpers import (
        demo_calcoli,
        mh870_c_alt,
        mh870_c_base,
        mh870_calcola,
        mh870_capex_totale,
        mh870_co2_alt,
        mh870_co2_base,
        mh870_co2_evitata,
        mh870_csv,
        mh870_demo,
        mh870_demo_calcoli,
        mh870_e_alt,
        mh870_e_deficit,
        mh870_e_immessa,
        mh870_e_lucid_alt,
        mh870_e_pv,
        mh870_e_pv_auto,
        mh870_e_seghe_alt,
        mh870_e_seghe_base,
        mh870_flussi,
        mh870_frazione,
        mh870_gas_base,
        mh870_int_pos,
        mh870_kwp,
        mh870_nneg,
        mh870_num,
        mh870_p_gas_pareggio,
        mh870_payback,
        mh870_pos,
        mh870_ricavo_immissione,
        mh870_risparmio,
        mh870_sensibilita,
        mh870_tir,
        mh870_valida,
        mh870_van,
        mh870_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w874_helpers", os.path.join(_hf, "w874_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh870_c_alt = _mod.mh870_c_alt
    mh870_c_base = _mod.mh870_c_base
    mh870_calcola = _mod.mh870_calcola
    mh870_capex_totale = _mod.mh870_capex_totale
    mh870_co2_alt = _mod.mh870_co2_alt
    mh870_co2_base = _mod.mh870_co2_base
    mh870_co2_evitata = _mod.mh870_co2_evitata
    mh870_csv = _mod.mh870_csv
    mh870_demo = _mod.mh870_demo
    mh870_demo_calcoli = _mod.mh870_demo_calcoli
    mh870_e_alt = _mod.mh870_e_alt
    mh870_e_deficit = _mod.mh870_e_deficit
    mh870_e_immessa = _mod.mh870_e_immessa
    mh870_e_lucid_alt = _mod.mh870_e_lucid_alt
    mh870_e_pv = _mod.mh870_e_pv
    mh870_e_pv_auto = _mod.mh870_e_pv_auto
    mh870_e_seghe_alt = _mod.mh870_e_seghe_alt
    mh870_e_seghe_base = _mod.mh870_e_seghe_base
    mh870_flussi = _mod.mh870_flussi
    mh870_frazione = _mod.mh870_frazione
    mh870_gas_base = _mod.mh870_gas_base
    mh870_int_pos = _mod.mh870_int_pos
    mh870_kwp = _mod.mh870_kwp
    mh870_nneg = _mod.mh870_nneg
    mh870_num = _mod.mh870_num
    mh870_p_gas_pareggio = _mod.mh870_p_gas_pareggio
    mh870_payback = _mod.mh870_payback
    mh870_pos = _mod.mh870_pos
    mh870_ricavo_immissione = _mod.mh870_ricavo_immissione
    mh870_risparmio = _mod.mh870_risparmio
    mh870_sensibilita = _mod.mh870_sensibilita
    mh870_tir = _mod.mh870_tir
    mh870_valida = _mod.mh870_valida
    mh870_van = _mod.mh870_van
    mh870_verdetto = _mod.mh870_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w874_helpers.py")
_UI_PATH = _risolvi("w874_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "9"
_VECCHIO_TAB = "tab86" + "9"
_VECCHIO_ST = "st86" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")
_TITLES_SNAPSHOT = os.path.join(_HF_FALLBACK, "w873_titles.txt")

_DEMO = {
    "e_seghe_base_kwh_anno": 360000.0,
    "gas_base_smc_anno": 48000.0,
    "c_base_eur_anno": 172400.0,
    "e_seghe_alt_kwh_anno": 240000.0,
    "e_lucid_alt_kwh_anno": 150000.0,
    "e_alt_kwh_anno": 390000.0,
    "kwp": 400.0,
    "e_pv_kwh_anno": 440000.0,
    "e_pv_auto_kwh_anno": 264000.0,
    "e_immessa_kwh_anno": 176000.0,
    "e_deficit_kwh_anno": 126000.0,
    "ricavo_immissione_eur_anno": 14080.0,
    "c_alt_eur_anno": 53640.0,
    "risparmio_eur_anno": 118760.0,
    "capex_eur": 860000.0,
    "co2_base_t_anno": 220.08,
    "co2_alt_t_anno": 44.1,
    "co2_evitata_t_anno": 175.98,
    "van": 620012.1002800481,
    "tir": 12.499680293787431,
    "payback": 8,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh870_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh870_num(3, "x"), 3.0)
        self.assertEqual(mh870_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh870_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh870_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh870_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh870_pos(0, "x")
        with self.assertRaises(ValueError):
            mh870_pos(-1, "x")
        self.assertEqual(mh870_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh870_int_pos(20, "x"), 20)
        self.assertEqual(mh870_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh870_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh870_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh870_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh870_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh870_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh870_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_seghe_e_gas_e_costo_base(self):
        self.assertEqual(mh870_e_seghe_base(60000, 6.0), 360000.0)
        self.assertEqual(mh870_gas_base(60000, 0.8), 48000.0)
        self.assertEqual(mh870_c_base(360000.0, 0.22, 48000.0, 0.90,
                                       50000), 172400.0)

    def test_seghe_alt_lucid_alt_somma(self):
        self.assertEqual(mh870_e_seghe_alt(60000, 4.0), 240000.0)
        self.assertEqual(mh870_e_lucid_alt(60000, 2.5), 150000.0)
        self.assertEqual(mh870_e_alt(240000.0, 150000.0), 390000.0)
        # L'inverter RIDUCE le seghe, non le azzera:
        # 4,0 resta sopra zero anche a parita' di base 6,0.
        self.assertGreater(mh870_e_seghe_alt(60000, 4.0), 0.0)
        self.assertLess(mh870_e_seghe_alt(60000, 4.0),
                        mh870_e_seghe_base(60000, 6.0))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh870_kwp(2000, 0.20), 400.0)
        self.assertEqual(mh870_e_pv(400.0, 1100), 440000.0)
        self.assertEqual(mh870_e_pv_auto(440000.0, 0.60, 390000.0),
                         264000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh870_e_pv_auto(440000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh870_e_immessa(440000.0, 264000.0), 176000.0)
        self.assertEqual(mh870_e_deficit(390000.0, 264000.0), 126000.0)
        self.assertEqual(mh870_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh870_ricavo_immissione(176000.0, 0.08), 14080.0)
        self.assertAlmostEqual(
            mh870_c_alt(126000.0, 0.22, 14080.0, 40000.0),
            53640.0)
        self.assertAlmostEqual(mh870_risparmio(172400.0, 53640.0),
                               118760.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh870_capex_totale(350000, 150000, 400.0,
                                            900),
                         860000.0)
        self.assertEqual(mh870_capex_totale(350000, 150000, 0.0,
                                            900),
                         500000.0)

    def test_co2_base_e_alt(self):
        cb = mh870_co2_base(48000.0, 1.96, 360000.0, 0.35)
        self.assertAlmostEqual(cb, 220.08, places=4)
        ca = mh870_co2_alt(126000.0, 0.35)
        self.assertAlmostEqual(ca, 44.1, places=4)
        self.assertAlmostEqual(mh870_co2_evitata(cb, ca), 175.98, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh870_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh870_flussi(860000, 118760.0, 3),
                         [-860000, 118760.0, 118760.0, 118760.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh870_van([-100, 60, 60], 0), 20.0)
        bc = mh870_demo_calcoli()
        self.assertAlmostEqual(mh870_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh870_demo_calcoli()
        tir = mh870_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh870_tir([-100, -10, -10]))
        self.assertIsNone(mh870_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh870_demo_calcoli()
        self.assertEqual(mh870_payback(bc["flussi"]), 8)
        self.assertIsNone(mh870_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh870_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh870_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:8]), -28680.0, places=2)
        self.assertAlmostEqual(sum(flussi[:9]), 90080.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh870_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh870_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh870_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh870_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh870_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh870_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh870_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh870_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_seghe_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["e_deficit_kwh_anno"] * bc["p_el"]
             - bc["ricavo_immissione_eur_anno"]
             + bc["om_alt_eur_anno"]
             - bc["e_seghe_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], -1.5741666666666667, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh870_p_gas_pareggio(48000.0, 360000.0, 126000.0,
                                 0.22, 14080.0, 50000.0, 200000.0),
            1.7591666666666668, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh870_p_gas_pareggio(48000.0, 360000.0,
                                              126000.0, 0.22, 14080.0,
                                              50000.0, 115560.0),
                         0.0)
        self.assertIsNone(mh870_p_gas_pareggio(0.0, 360000.0,
                                               126000.0, 0.22, 14080.0,
                                               50000.0, 40000.0))
        self.assertIsNone(mh870_p_gas_pareggio(48000.0, 360000.0,
                                               126000.0, 0.22, 14080.0,
                                               50000.0, 40000.0))

    def test_valida_demo_ok(self):
        demo = mh870_demo()
        val = mh870_valida(*[demo[k] for k in (
            "m2_anno", "e_seghe_base_per_m2", "p_el",
            "gas_per_m2", "p_gas", "om_base_eur_anno",
            "e_seghe_alt_per_m2", "e_lucid_alt_per_m2", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_seghe_eur", "capex_lucid_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_m2_zero_no(self):
        kw = _demo_kwargs(m2_anno=0)
        self.assertRaises(ValueError, mh870_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh870_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh870_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh870_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh870_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("m2_anno", -1),
                              ("e_seghe_base_per_m2", -1),
                              ("p_gas", -0.01),
                              ("capex_seghe_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh870_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh870_calcola(mh870_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh870_calcola(dict(mh870_demo(), capex_seghe_eur=999999),
                           capex_seghe_eur=350000)
        self.assertEqual(bc["capex_eur"], 860000.0)

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
        self.assertEqual(bc["payback"], 8)

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
            bc["e_seghe_base_kwh_anno"] * bc["p_el"]
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
                         - bc["e_seghe_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh870_sensibilita(**mh870_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               127400.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               727685.60, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 7)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               129056.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               748323.02, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 7)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               46600.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               80739.00, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 11)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 500000.0)
        self.assertAlmostEqual(s["senza_inverter"]["risparmio_eur_anno"],
                               92360.0, places=2)
        self.assertAlmostEqual(s["senza_inverter"]["van"],
                               291009.75, places=2)
        self.assertEqual(s["senza_inverter"]["payback"], 10)
        self.assertEqual(s["senza_inverter"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -239987.90, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 15)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               57033.24, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               1515200.0, places=2)

    def test_marginale_con_capex_seghe_alto(self):
        # CAPEX totale 1.510.000 (seghe a 1.000.000):
        # VAN circa -29.987,90, entro la tolleranza del 10%
        # (151.000).
        bc = mh870_calcola(**_demo_kwargs(capex_seghe_eur=1000000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -29987.90, places=2)

    def test_non_convente_con_capex_seghe_altissimo(self):
        bc = mh870_calcola(**_demo_kwargs(capex_seghe_eur=1200000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -229987.90, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh870_calcola(**_demo_kwargs(om_alt_eur_anno=300000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -141240.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh870_csv(bc, mh870_demo())
        for voce in ("m2_anno", "e_seghe_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -860000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Metri quadri (m2/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh870_c_alt(390000.0, 0.22, 0.0, 40000.0)
        con = mh870_c_alt(126000.0, 0.22, 14080.0, 40000.0)
        self.assertAlmostEqual(senza - con, 390000.0 * 0.22 - 126000.0 * 0.22 + 14080.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh870_sensibilita(**mh870_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_inverter",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh870_csv(bc, mh870_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_seghe_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh870_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh870_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh870_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 500000.0)
        bc = mh870_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def870\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh870_demo().keys()), lette - set(mh870_demo().keys()))
        self.assertEqual(lette, set(mh870_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc870\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc870\["([^"]+)"\]', src))
        attese = set(mh870_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 874)
        elif os.path.exists(_TITLES_SNAPSHOT):
            with open(_TITLES_SNAPSHOT, encoding="utf-8") as f:
                self.assertEqual(sum(1 for _ in f), 868)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab870:"), 1)
        self.assertTrue(src.startswith("    # W874"))

    def test_ui_tab870_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab870:"), 1)
        self.assertIn("def mh870_demo(", src_h)
        self.assertIn("def mh870_calcola(", src_h)
        self.assertIn("tab870", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Marmificio / lavorazione marmo e pietra: seghe diamantate con inverter + lucidatura efficiente + FV battono seghe tradizionali + essiccazione a gas?", src)
        self.assertIn("🪨 Marmificio / lavorazione marmo e pietra: seghe diamantate con inverter + lucidatura efficiente + FV battono seghe tradizionali + essiccazione a gas?", src)
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
        chiavi = re.findall(r'key="(st870_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st870_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st870_calcola"', src)
        self.assertIn('key="st870_csv"', src)
        self.assertIn('key="st870_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg870"), src.index(".paiac("))
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
