"""Test nuova scheda frutteto:
irrigazione a goccia + ventilatori antibrina
+ celle frigo efficienti + FV battono irrigazione
tradizionale + antibrina a gas + celle tradizionali?

Business case annuo di un frutteto,
guidato dagli ETTARI di frutteto all'anno
(demo 15 ettari/anno):
irrigazione tradizionale base 15 x 700 =
10.500 kWh/anno; celle frigo tradizionali
15 x 800 = 12.000 kWh/anno; elettricita' base
totale 22.500 kWh/anno, costo energia base 4.950
EUR/anno; gas base 15 x 100 = 1.500 Smc/anno,
costo gas base 1.350 EUR/anno; O&M base 15.000
EUR/anno; costo base 21.300 EUR/anno;
irrigazione a goccia 15 x 400 = 6.000
kWh/anno; ventilatori antibrina elettrici
15 x 150 = 2.250 kWh/anno; celle frigo efficienti
15 x 500 = 7.500 kWh/anno; elettricita'
alternativa 15.750 kWh/anno, gas antibrina
ELIMINATO; kWp = sup x kwp/m2
(demo 30 kWp); E_pv 33.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 15.750 kWh/anno, cappata alla domanda);
immessa 17.250 kWh/anno; deficit 0 kWh/anno;
ricavo immissione 1.380 EUR/anno; O&M alternativa
10.000 EUR/anno; C_alt 8.620 EUR/anno;
risparmio 12.680 EUR/anno; CAPEX
45.000 + 22.500 + 30.000 + 30 x 900 = 124.500 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 8,55
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0
t/anno (immessa senza credito CO2); CO2 evitata
8,55 t/anno; LCO base 1.420,00 EUR/ha e LCO alt
574,67 EUR/ha (costi operativi annui per
ettaro, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato >= 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / gas in forma chiusa
(demo None: rapporto negativo meno 7,5533, vince
anche a gas gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e' negativo.
E' una SOGLIA MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa vince, sotto
perde. Verdetto: NON_VALUTABILE se input degenere
(ettari <= 0, kWh per ettaro < 0, prezzi <
0, O&M < 0, superficie < 0, kwp per m2 < 0, resa <
0, f_autoconsumo < 0 o > 1, voci CAPEX < 0,
fattori CO2 < 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: produzione zero (ettari zero) non
calcolabile (ValueError negli helper, guard
NON_VALUTABILE in UI); quota FV zero
(f_autoconsumo zero, autoconsumo zero); prezzo gas
zero (ancora calcolabile, risparmio positivo, VAN
negativa entro tolleranza: MARGINALE);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: NON vigneto (li'
si coltivano viti da uva, qui SOLO frutta da albero:
irrigazione + protezione antibrina + celle frigo,
NIENTE uva, NIENTE vigneto), NON cantina/vinicola (li'
si fa il vino dalle uve, qui SOLO il frutteto:
irrigazione + protezione antibrina + celle frigo,
NIENTE vinificazione, NIENTE cantina), NON vivaio
floricolo (li' piante ornamentali in vivaio, qui
SOLO frutta da albero, NIENTE piante ornamentali,
NIENTE vivaio), NON serra (li' colture sotto
serra, qui NIENTE serra, solo frutteto in campo
aperto), NON orto (li' ortaggi, qui NIENTE
ortaggi, solo frutta da albero); qui solo frutteto:
irrigazione + protezione antibrina + celle frigo + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w884_helpers import (
        demo_calcoli,
        mh880_c_alt,
        mh880_c_base,
        mh880_calcola,
        mh880_capex_totale,
        mh880_co2_alt,
        mh880_co2_base,
        mh880_co2_evitata,
        mh880_csv,
        mh880_demo,
        mh880_demo_calcoli,
        mh880_e_alt,
        mh880_e_base,
        mh880_e_base_totale,
        mh880_e_celle_alt,
        mh880_e_celle_base,
        mh880_e_deficit,
        mh880_e_goccia,
        mh880_e_immessa,
        mh880_e_pv,
        mh880_e_pv_auto,
        mh880_e_ventilatori,
        mh880_flussi,
        mh880_frazione,
        mh880_gas_base,
        mh880_int_pos,
        mh880_kwp,
        mh880_lco,
        mh880_nneg,
        mh880_num,
        mh880_p_gas_pareggio,
        mh880_payback,
        mh880_pos,
        mh880_ricavo_immissione,
        mh880_risparmio,
        mh880_sensibilita,
        mh880_tir,
        mh880_valida,
        mh880_van,
        mh880_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w884_helpers", os.path.join(_hf, "w884_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh880_c_alt = _mod.mh880_c_alt
    mh880_c_base = _mod.mh880_c_base
    mh880_calcola = _mod.mh880_calcola
    mh880_capex_totale = _mod.mh880_capex_totale
    mh880_co2_alt = _mod.mh880_co2_alt
    mh880_co2_base = _mod.mh880_co2_base
    mh880_co2_evitata = _mod.mh880_co2_evitata
    mh880_csv = _mod.mh880_csv
    mh880_demo = _mod.mh880_demo
    mh880_demo_calcoli = _mod.mh880_demo_calcoli
    mh880_e_alt = _mod.mh880_e_alt
    mh880_e_base = _mod.mh880_e_base
    mh880_e_base_totale = _mod.mh880_e_base_totale
    mh880_e_celle_alt = _mod.mh880_e_celle_alt
    mh880_e_celle_base = _mod.mh880_e_celle_base
    mh880_e_deficit = _mod.mh880_e_deficit
    mh880_e_goccia = _mod.mh880_e_goccia
    mh880_e_immessa = _mod.mh880_e_immessa
    mh880_e_pv = _mod.mh880_e_pv
    mh880_e_pv_auto = _mod.mh880_e_pv_auto
    mh880_e_ventilatori = _mod.mh880_e_ventilatori
    mh880_flussi = _mod.mh880_flussi
    mh880_frazione = _mod.mh880_frazione
    mh880_gas_base = _mod.mh880_gas_base
    mh880_int_pos = _mod.mh880_int_pos
    mh880_kwp = _mod.mh880_kwp
    mh880_lco = _mod.mh880_lco
    mh880_nneg = _mod.mh880_nneg
    mh880_num = _mod.mh880_num
    mh880_p_gas_pareggio = _mod.mh880_p_gas_pareggio
    mh880_payback = _mod.mh880_payback
    mh880_pos = _mod.mh880_pos
    mh880_ricavo_immissione = _mod.mh880_ricavo_immissione
    mh880_risparmio = _mod.mh880_risparmio
    mh880_sensibilita = _mod.mh880_sensibilita
    mh880_tir = _mod.mh880_tir
    mh880_valida = _mod.mh880_valida
    mh880_van = _mod.mh880_van
    mh880_verdetto = _mod.mh880_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w884_helpers.py")
_UI_PATH = _risolvi("w884_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "9"
_VECCHIO_TAB = "tab87" + "9"
_VECCHIO_ST = "st87" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_base_kwh_anno": 22500.0,
    "e_irrigazione_base_kwh_anno": 10500.0,
    "e_celle_base_kwh_anno": 12000.0,
    "gas_base_smc_anno": 1500.0,
    "c_base_eur_anno": 21300.0,
    "e_goccia_kwh_anno": 6000.0,
    "e_ventilatori_kwh_anno": 2250.0,
    "e_celle_alt_kwh_anno": 7500.0,
    "e_alt_kwh_anno": 15750.0,
    "kwp": 30.0,
    "e_pv_kwh_anno": 33000.0,
    "e_pv_auto_kwh_anno": 15750.0,
    "e_immessa_kwh_anno": 17250.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_immissione_eur_anno": 1380.0,
    "c_alt_eur_anno": 8620.0,
    "risparmio_eur_anno": 12680.0,
    "capex_eur": 124500.0,
    "co2_base_t_anno": 8.55,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 8.55,
    "lco_base_eur_ha": 1420.0,
    "lco_alt_eur_ha": 574.6666666666666,
    "van": 7114.063924129871,
    "tir": 5.83377220714402,
    "payback": 10,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh880_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh880_num(3, "x"), 3.0)
        self.assertEqual(mh880_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh880_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh880_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh880_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh880_pos(0, "x")
        with self.assertRaises(ValueError):
            mh880_pos(-1, "x")
        self.assertEqual(mh880_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh880_int_pos(15, "x"), 15)
        self.assertEqual(mh880_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh880_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh880_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh880_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh880_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh880_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh880_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_irrigazione_base_e_costo_base(self):
        self.assertEqual(mh880_e_base(15, 700), 10500.0)
        self.assertEqual(mh880_e_celle_base(15, 800), 12000.0)
        self.assertEqual(mh880_e_base_totale(10500.0, 12000.0), 22500.0)
        self.assertEqual(mh880_gas_base(15, 100), 1500.0)
        self.assertEqual(mh880_c_base(22500.0, 0.22, 1500.0, 0.90,
                                       15000), 21300.0)

    def test_goccia_ventilatori_somma(self):
        self.assertEqual(mh880_e_goccia(15, 400), 6000.0)
        self.assertEqual(mh880_e_ventilatori(15, 150), 2250.0)
        self.assertEqual(mh880_e_celle_alt(15, 500), 7500.0)
        self.assertEqual(mh880_e_alt(6000.0, 2250.0, 7500.0), 15750.0)
        # La goccia RIDUCE il consumo di irrigazione,
        # non lo azzera: 400 resta sopra zero anche a
        # parita' di base 700.
        self.assertGreater(mh880_e_goccia(15, 400), 0.0)
        self.assertLess(mh880_e_goccia(15, 400),
                        mh880_e_base(15, 700))
        # Le celle efficienti RIDUCONO il consumo,
        # non lo azzerano: 500 resta sopra zero anche
        # a parita' di base 800.
        self.assertGreater(mh880_e_celle_alt(15, 500), 0.0)
        self.assertLess(mh880_e_celle_alt(15, 500),
                        mh880_e_celle_base(15, 800))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh880_kwp(150, 0.20), 30.0)
        self.assertEqual(mh880_e_pv(30.0, 1100), 33000.0)
        self.assertEqual(mh880_e_pv_auto(33000.0, 0.60, 15750.0),
                         15750.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh880_e_pv_auto(33000.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh880_e_immessa(33000.0, 15750.0), 17250.0)
        self.assertEqual(mh880_e_deficit(15750.0, 15750.0), 0.0)
        self.assertEqual(mh880_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh880_ricavo_immissione(17250.0, 0.08), 1380.0)
        self.assertAlmostEqual(
            mh880_c_alt(0.0, 0.22, 1380.0, 10000.0),
            8620.0)
        self.assertAlmostEqual(mh880_risparmio(21300.0, 8620.0),
                               12680.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh880_capex_totale(45000, 22500, 30000, 30.0,
                                            900),
                         124500.0)
        self.assertEqual(mh880_capex_totale(45000, 22500, 30000, 0.0,
                                            900),
                         97500.0)

    def test_co2_base_e_alt(self):
        cb = mh880_co2_base(1500.0, 1.95, 22500.0, 0.25)
        self.assertAlmostEqual(cb, 8.55, places=4)
        ca = mh880_co2_alt(0.0, 0.25)
        self.assertAlmostEqual(ca, 0.0, places=4)
        self.assertAlmostEqual(mh880_co2_evitata(cb, ca), 8.55, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh880_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh880_lco(21300.0, 15), 1420.0)
        self.assertAlmostEqual(mh880_lco(8620.0, 15), 574.6666666666666)
        with self.assertRaises(ValueError):
            mh880_lco(21300.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh880_flussi(124500, 12680.0, 3),
                         [-124500, 12680.0, 12680.0, 12680.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh880_van([-100, 60, 60], 0), 20.0)
        bc = mh880_demo_calcoli()
        self.assertAlmostEqual(mh880_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh880_demo_calcoli()
        tir = mh880_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh880_tir([-100, -10, -10]))
        self.assertIsNone(mh880_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh880_demo_calcoli()
        self.assertEqual(mh880_payback(bc["flussi"]), 10)
        self.assertIsNone(mh880_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh880_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh880_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:10]), -10380.0, places=2)
        self.assertAlmostEqual(sum(flussi[:11]), 2300.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh880_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh880_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh880_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh880_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh880_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh880_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh880_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh880_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -7.553333333333334, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh880_p_gas_pareggio(1500.0, 22500.0,
                                 0.22, 15000.0, 50000.0),
            20.03333333333333, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh880_p_gas_pareggio(1500.0, 22500.0,
                                              0.22, 15000.0, 19950.0),
                         0.0)
        self.assertIsNone(mh880_p_gas_pareggio(0.0, 22500.0,
                                               0.22, 15000.0, 50000.0))
        self.assertIsNone(mh880_p_gas_pareggio(1500.0, 22500.0,
                                               0.22, 15000.0, 8620.0))

    def test_valida_demo_ok(self):
        demo = mh880_demo()
        val = mh880_valida(*[demo[k] for k in (
            "ha_anno", "e_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_goccia_per_ha", "e_ventilatori_per_ha",
            "e_celle_base_per_ha", "e_celle_alt_per_ha", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_goccia_eur", "capex_ventilatori_eur",
            "capex_celle_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_ettari_zero_no(self):
        kw = _demo_kwargs(ha_anno=0)
        self.assertRaises(ValueError, mh880_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh880_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh880_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh880_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh880_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("ha_anno", -1),
                              ("e_base_per_ha", -1),
                              ("p_gas", -0.01),
                              ("capex_goccia_eur", -1),
                              ("capex_celle_eur", -1),
                              ("e_celle_base_per_ha", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh880_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh880_calcola(mh880_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh880_calcola(dict(mh880_demo(), capex_goccia_eur=999999),
                           capex_goccia_eur=45000)
        self.assertEqual(bc["capex_eur"], 124500.0)


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
        self.assertAlmostEqual(
            bc["lco_base_eur_ha"],
            bc["c_base_eur_anno"] / bc["ha_anno"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_ha"],
            bc["c_alt_eur_anno"] / bc["ha_anno"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh880_sensibilita(**mh880_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               12950.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               9916.57, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 10)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               13670.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               17389.93, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 10)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               7835.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               -16175.38, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 13)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 97500.0)
        self.assertAlmostEqual(s["senza_goccia"]["risparmio_eur_anno"],
                               12257.0, places=2)
        self.assertAlmostEqual(s["senza_goccia"]["van"],
                               2723.47, places=2)
        self.assertEqual(s["senza_goccia"]["payback"], 11)
        self.assertEqual(s["senza_goccia"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -117385.94, places=2)
        self.assertIsNone(s["capex_doppio"]["payback"])
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -26588.40, places=2)
        self.assertEqual(s["vita_10"]["payback"], 10)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               65700.0, places=2)

    def test_marginale_con_capex_goccia_alto(self):
        # CAPEX totale 139.500 (goccia a 60.000):
        # VAN circa meno 7.885,94, entro la tolleranza del 10%
        # (13.950).
        bc = mh880_calcola(**_demo_kwargs(capex_goccia_eur=60000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -7885.94, places=2)

    def test_non_convente_con_capex_goccia_altissimo(self):
        bc = mh880_calcola(**_demo_kwargs(capex_goccia_eur=90000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -37885.94, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh880_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -77320.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh880_csv(bc, mh880_demo())
        for voce in ("ha_anno", "e_base_kwh_anno",
                     "e_celle_base_kwh_anno", "e_celle_alt_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_ha", "lco_alt_eur_ha"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -124500.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Ettari (ettari/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh880_c_alt(15750.0, 0.22, 0.0, 10000.0)
        con = mh880_c_alt(0.0, 0.22, 1380.0, 10000.0)
        self.assertAlmostEqual(senza - con, 15750.0 * 0.22 + 1380.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh880_sensibilita(**mh880_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_goccia",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh880_csv(bc, mh880_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh880_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh880_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh880_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 97500.0)
        bc = mh880_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero (ettari zero): non
        # calcolabile negli helper (ValueError) e
        # guard NON_VALUTABILE in UI.
        kw = _demo_kwargs(ha_anno=0)
        self.assertRaises(ValueError, mh880_calcola, **kw)
        self.assertFalse(mh880_valida(*[kw[k] for k in (
            "ha_anno", "e_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_goccia_per_ha", "e_ventilatori_per_ha",
            "e_celle_base_per_ha", "e_celle_alt_per_ha", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_goccia_eur", "capex_ventilatori_eur",
            "capex_celle_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh880_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 33000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 15750.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               2640.0)

    def test_prezzo_gas_zero(self):
        bc = mh880_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 19950.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 11330.0)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh880_calcola(**_demo_kwargs(capex_goccia_eur=0,
                                          capex_ventilatori_eur=0,
                                          capex_celle_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh880_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 65700.0)
        self.assertEqual(bc["payback"], 10)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def880\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh880_demo().keys()), lette - set(mh880_demo().keys()))
        self.assertEqual(lette, set(mh880_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc880\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc880\["([^"]+)"\]', src))
        attese = set(mh880_demo_calcoli().keys())
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
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 886)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab880:"), 1)
        self.assertTrue(src.startswith("    # W884"))

    def test_ui_tab880_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab880:"), 1)
        self.assertIn("def mh880_demo(", src_h)
        self.assertIn("def mh880_calcola(", src_h)
        self.assertIn("tab880", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Frutteto: irrigazione a goccia + ventilatori antibrina + celle frigo efficienti + FV battono irrigazione tradizionale + antibrina a gas + celle tradizionali?", src)
        self.assertIn("🍎 Frutteto: irrigazione a goccia + ventilatori antibrina + celle frigo efficienti + FV battono irrigazione tradizionale + antibrina a gas + celle tradizionali?", src)
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
        chiavi = re.findall(r'key="(st880_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st880_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st880_calcola"', src)
        self.assertIn('key="st880_csv"', src)
        self.assertIn('key="st880_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg880"), src.index(".paiac("))
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
