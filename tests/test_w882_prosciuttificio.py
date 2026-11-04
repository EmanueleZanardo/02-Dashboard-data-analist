"""Test nuova scheda prosciuttificio:
stagionare e asciugare i prosciutti con pompa di
calore + recupero calore + FV battono caldaia a
gas + freddo tradizionale?

Business case annuo di un prosciuttificio,
guidato dalle TONNELLATE di prosciutto stagionato
all'anno (demo 200 tonnellate/anno):
celle di stagionatura con freddo tradizionale base
200 x 900 = 180.000 kWh/anno; elettricita' base
180.000 kWh/anno, costo energia base 39.600
EUR/anno; gas base 200 x 40 = 8.000 Smc/anno,
costo gas base 7.200 EUR/anno; O&M base 35.000
EUR/anno; costo base 81.800 EUR/anno; celle
efficienti con pompa di calore 200 x 550 =
110.000 kWh/anno; asciugatura con pompa di calore
200 x 150 = 30.000 kWh/anno; elettricita'
alternativa 140.000 kWh/anno; kWp = sup x kwp/m2
(demo 120 kWp); E_pv 132.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 79.200 kWh/anno); immessa 52.800 kWh/anno;
deficit 60.800 kWh/anno; ricavo immissione 4.224
EUR/anno; O&M alternativa 25.000 EUR/anno; C_alt
34.152 EUR/anno; risparmio 47.648 EUR/anno; CAPEX
120.000 + 80.000 + 120 x 900 = 308.000 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 60,6
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 15,2
t/anno (immessa senza credito CO2); CO2 evitata
45,4 t/anno; LCO base 409,00 EUR/t e LCO alt
170,76 EUR/t (costi operativi annui per
tonnellata, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato >= 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / gas in forma chiusa
(demo None: rapporto negativo meno 5,056, vince
anche a gas gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e' negativo.
E' una SOGLIA MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa vince, sotto
perde. Verdetto: NON_VALUTABILE se input degenere
(tonnellate <= 0, kWh per tonnellata < 0, prezzi <
0, O&M < 0, superficie < 0, kwp per m2 < 0, resa <
0, f_autoconsumo < 0 o > 1, voci CAPEX < 0,
fattori CO2 < 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: produzione zero (tonnellate zero) non
calcolabile (ValueError negli helper, guard
NON_VALUTABILE in UI); quota FV zero
(f_autoconsumo zero, autoconsumo zero); prezzo gas
zero (ancora calcolabile, risparmio positivo);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: NON salumificio (li'
salumi vari da stagionare o cuocere, qui SOLO
prosciutti crudi stagionati, niente altri salumi,
niente cottura), NON caseificio (li' latte e
formaggi, qui NIENTE latte e NIENTE formaggi),
NON surgelati (li' prodotto surgelato, qui NIENTE
surgelati), NON macelleria (li' carne fresca al
banco, qui NIENTE vendita al banco); qui solo
stagionatura + asciugatura di prosciutti con pompa
di calore + recupero calore + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w882_helpers import (
        demo_calcoli,
        mh878_c_alt,
        mh878_c_base,
        mh878_calcola,
        mh878_capex_totale,
        mh878_co2_alt,
        mh878_co2_base,
        mh878_co2_evitata,
        mh878_csv,
        mh878_demo,
        mh878_demo_calcoli,
        mh878_e_alt,
        mh878_e_asciug_alt,
        mh878_e_base,
        mh878_e_deficit,
        mh878_e_freddo_alt,
        mh878_e_freddo_base,
        mh878_e_immessa,
        mh878_e_pv,
        mh878_e_pv_auto,
        mh878_flussi,
        mh878_frazione,
        mh878_gas_base,
        mh878_int_pos,
        mh878_kwp,
        mh878_lco,
        mh878_nneg,
        mh878_num,
        mh878_p_gas_pareggio,
        mh878_payback,
        mh878_pos,
        mh878_ricavo_immissione,
        mh878_risparmio,
        mh878_sensibilita,
        mh878_tir,
        mh878_valida,
        mh878_van,
        mh878_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w882_helpers", os.path.join(_hf, "w882_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh878_c_alt = _mod.mh878_c_alt
    mh878_c_base = _mod.mh878_c_base
    mh878_calcola = _mod.mh878_calcola
    mh878_capex_totale = _mod.mh878_capex_totale
    mh878_co2_alt = _mod.mh878_co2_alt
    mh878_co2_base = _mod.mh878_co2_base
    mh878_co2_evitata = _mod.mh878_co2_evitata
    mh878_csv = _mod.mh878_csv
    mh878_demo = _mod.mh878_demo
    mh878_demo_calcoli = _mod.mh878_demo_calcoli
    mh878_e_alt = _mod.mh878_e_alt
    mh878_e_asciug_alt = _mod.mh878_e_asciug_alt
    mh878_e_base = _mod.mh878_e_base
    mh878_e_deficit = _mod.mh878_e_deficit
    mh878_e_freddo_alt = _mod.mh878_e_freddo_alt
    mh878_e_freddo_base = _mod.mh878_e_freddo_base
    mh878_e_immessa = _mod.mh878_e_immessa
    mh878_e_pv = _mod.mh878_e_pv
    mh878_e_pv_auto = _mod.mh878_e_pv_auto
    mh878_flussi = _mod.mh878_flussi
    mh878_frazione = _mod.mh878_frazione
    mh878_gas_base = _mod.mh878_gas_base
    mh878_int_pos = _mod.mh878_int_pos
    mh878_kwp = _mod.mh878_kwp
    mh878_lco = _mod.mh878_lco
    mh878_nneg = _mod.mh878_nneg
    mh878_num = _mod.mh878_num
    mh878_p_gas_pareggio = _mod.mh878_p_gas_pareggio
    mh878_payback = _mod.mh878_payback
    mh878_pos = _mod.mh878_pos
    mh878_ricavo_immissione = _mod.mh878_ricavo_immissione
    mh878_risparmio = _mod.mh878_risparmio
    mh878_sensibilita = _mod.mh878_sensibilita
    mh878_tir = _mod.mh878_tir
    mh878_valida = _mod.mh878_valida
    mh878_van = _mod.mh878_van
    mh878_verdetto = _mod.mh878_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w882_helpers.py")
_UI_PATH = _risolvi("w882_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "7"
_VECCHIO_TAB = "tab87" + "7"
_VECCHIO_ST = "st87" + "7_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_freddo_base_kwh_anno": 180000.0,
    "e_base_kwh_anno": 180000.0,
    "gas_base_smc_anno": 8000.0,
    "c_base_eur_anno": 81800.0,
    "e_freddo_alt_kwh_anno": 110000.0,
    "e_asciug_alt_kwh_anno": 30000.0,
    "e_alt_kwh_anno": 140000.0,
    "kwp": 120.0,
    "e_pv_kwh_anno": 132000.0,
    "e_pv_auto_kwh_anno": 79200.0,
    "e_immessa_kwh_anno": 52800.0,
    "e_deficit_kwh_anno": 60800.0,
    "ricavo_immissione_eur_anno": 4224.0,
    "c_alt_eur_anno": 34152.0,
    "risparmio_eur_anno": 47648.0,
    "capex_eur": 308000.0,
    "co2_base_t_anno": 60.6,
    "co2_alt_t_anno": 15.2,
    "co2_evitata_t_anno": 45.4,
    "lco_base_eur_t": 409.0,
    "lco_alt_eur_t": 170.76,
    "van": 186569.94620322878,
    "tir": 12.99493573533112,
    "payback": 7,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh878_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh878_num(3, "x"), 3.0)
        self.assertEqual(mh878_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh878_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh878_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh878_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh878_pos(0, "x")
        with self.assertRaises(ValueError):
            mh878_pos(-1, "x")
        self.assertEqual(mh878_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh878_int_pos(15, "x"), 15)
        self.assertEqual(mh878_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh878_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh878_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh878_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh878_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh878_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh878_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_freddo_base_e_costo_base(self):
        self.assertEqual(mh878_e_freddo_base(200, 900), 180000.0)
        self.assertEqual(mh878_e_base(180000.0), 180000.0)
        self.assertEqual(mh878_gas_base(200, 40), 8000.0)
        self.assertEqual(mh878_c_base(180000.0, 0.22, 8000.0, 0.90,
                                       35000), 81800.0)

    def test_freddo_alt_asciug_alt_somma(self):
        self.assertEqual(mh878_e_freddo_alt(200, 550), 110000.0)
        self.assertEqual(mh878_e_asciug_alt(200, 150), 30000.0)
        self.assertEqual(mh878_e_alt(110000.0, 30000.0), 140000.0)
        # La pompa di calore RIDUCE il consumo di
        # freddo, non lo azzera: 550 resta sopra zero
        # anche a parita' di base 900.
        self.assertGreater(mh878_e_freddo_alt(200, 550), 0.0)
        self.assertLess(mh878_e_freddo_alt(200, 550),
                        mh878_e_freddo_base(200, 900))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh878_kwp(600, 0.20), 120.0)
        self.assertEqual(mh878_e_pv(120.0, 1100), 132000.0)
        self.assertEqual(mh878_e_pv_auto(132000.0, 0.60, 140000.0),
                         79200.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh878_e_pv_auto(132000.0, 1.0, 50000.0), 50000.0)
        self.assertEqual(mh878_e_immessa(132000.0, 79200.0), 52800.0)
        self.assertEqual(mh878_e_deficit(140000.0, 79200.0), 60800.0)
        self.assertEqual(mh878_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh878_ricavo_immissione(52800.0, 0.08), 4224.0)
        self.assertAlmostEqual(
            mh878_c_alt(60800.0, 0.22, 4224.0, 25000.0),
            34152.0)
        self.assertAlmostEqual(mh878_risparmio(81800.0, 34152.0),
                               47648.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh878_capex_totale(120000, 80000, 120.0,
                                            900),
                         308000.0)
        self.assertEqual(mh878_capex_totale(120000, 80000, 0.0,
                                            900),
                         200000.0)

    def test_co2_base_e_alt(self):
        cb = mh878_co2_base(8000.0, 1.95, 180000.0, 0.25)
        self.assertAlmostEqual(cb, 60.6, places=4)
        ca = mh878_co2_alt(60800.0, 0.25)
        self.assertAlmostEqual(ca, 15.2, places=4)
        self.assertAlmostEqual(mh878_co2_evitata(cb, ca), 45.4, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh878_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh878_lco(81800.0, 200), 409.0)
        self.assertEqual(mh878_lco(34152.0, 200), 170.76)
        with self.assertRaises(ValueError):
            mh878_lco(81800.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh878_flussi(308000, 47648.0, 3),
                         [-308000, 47648.0, 47648.0, 47648.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh878_van([-100, 60, 60], 0), 20.0)
        bc = mh878_demo_calcoli()
        self.assertAlmostEqual(mh878_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh878_demo_calcoli()
        tir = mh878_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh878_tir([-100, -10, -10]))
        self.assertIsNone(mh878_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh878_demo_calcoli()
        self.assertEqual(mh878_payback(bc["flussi"]), 7)
        self.assertIsNone(mh878_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh878_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh878_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:7]), -22112.0, places=2)
        self.assertAlmostEqual(sum(flussi[:8]), 25536.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh878_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh878_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh878_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh878_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh878_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh878_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh878_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh878_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["c_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], -5.056, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh878_p_gas_pareggio(8000.0, 180000.0,
                                 0.22, 35000.0, 200000.0),
            15.675, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh878_p_gas_pareggio(8000.0, 180000.0,
                                              0.22, 35000.0, 74600.0),
                         0.0)
        self.assertIsNone(mh878_p_gas_pareggio(0.0, 180000.0,
                                               0.22, 35000.0, 200000.0))
        self.assertIsNone(mh878_p_gas_pareggio(8000.0, 180000.0,
                                               0.22, 35000.0, 34152.0))

    def test_valida_demo_ok(self):
        demo = mh878_demo()
        val = mh878_valida(*[demo[k] for k in (
            "tonn_anno", "e_freddo_base_per_t",
            "p_el", "gas_per_t",
            "p_gas", "om_base_eur_anno",
            "e_freddo_alt_per_t", "e_asciug_alt_per_t", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_celle_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_tonn_zero_no(self):
        kw = _demo_kwargs(tonn_anno=0)
        self.assertRaises(ValueError, mh878_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh878_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh878_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh878_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh878_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("tonn_anno", -1),
                              ("e_freddo_base_per_t", -1),
                              ("p_gas", -0.01),
                              ("capex_celle_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh878_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh878_calcola(mh878_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh878_calcola(dict(mh878_demo(), capex_celle_eur=999999),
                           capex_celle_eur=120000)
        self.assertEqual(bc["capex_eur"], 308000.0)


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
        self.assertAlmostEqual(
            bc["lco_base_eur_t"],
            bc["c_base_eur_anno"] / bc["tonn_anno"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_t"],
            bc["c_alt_eur_anno"] / bc["tonn_anno"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh878_sensibilita(**mh878_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               49088.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               201516.65, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 7)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               52892.8, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               241009.18, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               26000.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               69871.11, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 8)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 200000.0)
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               32248.0, places=2)
        self.assertAlmostEqual(s["senza_recupero"]["van"],
                               26723.21, places=2)
        self.assertEqual(s["senza_recupero"]["payback"], 10)
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -121430.05, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 13)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               59925.23, places=2)
        self.assertEqual(s["vita_10"]["payback"], 7)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               406720.0, places=2)

    def test_marginale_con_capex_celle_alto(self):
        # CAPEX totale 508.000 (celle a 320.000):
        # VAN circa meno 13.430,05, entro la tolleranza del 10%
        # (50.800).
        bc = mh878_calcola(**_demo_kwargs(capex_celle_eur=320000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -13430.05, places=2)

    def test_non_convente_con_capex_celle_altissimo(self):
        bc = mh878_calcola(**_demo_kwargs(capex_celle_eur=400000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -93430.05, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh878_calcola(**_demo_kwargs(om_alt_eur_anno=200000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -127352.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh878_csv(bc, mh878_demo())
        for voce in ("tonn_anno", "e_freddo_base_kwh_anno",
                     "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_t", "lco_alt_eur_t"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -308000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Tonnellate (tonnellate/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh878_c_alt(140000.0, 0.22, 0.0, 25000.0)
        con = mh878_c_alt(60800.0, 0.22, 4224.0, 25000.0)
        self.assertAlmostEqual(senza - con, 140000.0 * 0.22 - 60800.0 * 0.22 + 4224.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh878_sensibilita(**mh878_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_recupero",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh878_csv(bc, mh878_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_freddo_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh878_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh878_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh878_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 200000.0)
        bc = mh878_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero (tonnellate zero): non
        # calcolabile negli helper (ValueError) e
        # guard NON_VALUTABILE in UI.
        kw = _demo_kwargs(tonn_anno=0)
        self.assertRaises(ValueError, mh878_calcola, **kw)
        self.assertFalse(mh878_valida(*[kw[k] for k in (
            "tonn_anno", "e_freddo_base_per_t",
            "p_el", "gas_per_t",
            "p_gas", "om_base_eur_anno",
            "e_freddo_alt_per_t", "e_asciug_alt_per_t", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_celle_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh878_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 132000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 140000.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               10560.0)

    def test_prezzo_gas_zero(self):
        bc = mh878_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 74600.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 40448.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh878_calcola(**_demo_kwargs(capex_celle_eur=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh878_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 406720.0)
        self.assertEqual(bc["payback"], 7)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def878\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh878_demo().keys()), lette - set(mh878_demo().keys()))
        self.assertEqual(lette, set(mh878_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc878\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc878\["([^"]+)"\]', src))
        attese = set(mh878_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 887)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab878:"), 1)
        self.assertTrue(src.startswith("    # W882"))

    def test_ui_tab878_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab878:"), 1)
        self.assertIn("def mh878_demo(", src_h)
        self.assertIn("def mh878_calcola(", src_h)
        self.assertIn("tab878", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Prosciuttificio: stagionare e asciugare i prosciutti con pompa di calore + recupero calore + FV battono caldaia a gas + freddo tradizionale?", src)
        self.assertIn("🏭 Prosciuttificio: stagionare e asciugare i prosciutti con pompa di calore + recupero calore + FV battono caldaia a gas + freddo tradizionale?", src)
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
        chiavi = re.findall(r'key="(st878_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st878_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st878_calcola"', src)
        self.assertIn('key="st878_csv"', src)
        self.assertIn('key="st878_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg878"), src.index(".paiac("))
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
