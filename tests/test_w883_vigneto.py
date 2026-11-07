"""Test nuova scheda vigneto:
irrigazione a goccia + ventilatori antibrina
elettrici + FV battono irrigazione tradizionale
+ riscaldamento antibrina a gas?

Business case annuo di un vigneto,
guidato dagli ETTARI di vigneto all'anno
(demo 20 ettari/anno):
irrigazione tradizionale base 20 x 800 =
16.000 kWh/anno; elettricita' base 16.000
kWh/anno, costo energia base 3.520 EUR/anno;
gas base 20 x 120 = 2.400 Smc/anno,
costo gas base 2.160 EUR/anno; O&M base 18.000
EUR/anno; costo base 23.680 EUR/anno;
irrigazione a goccia 20 x 450 = 9.000
kWh/anno; ventilatori antibrina elettrici
20 x 150 = 3.000 kWh/anno; elettricita'
alternativa 12.000 kWh/anno, gas antibrina
ELIMINATO; kWp = sup x kwp/m2
(demo 20 kWp); E_pv 22.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 12.000 kWh/anno, cappata alla domanda);
immessa 10.000 kWh/anno; deficit 0 kWh/anno;
ricavo immissione 800 EUR/anno; O&M alternativa
12.000 EUR/anno; C_alt 11.200 EUR/anno;
risparmio 12.480 EUR/anno; CAPEX
60.000 + 30.000 + 20 x 900 = 108.000 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 8,68
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0
t/anno (immessa senza credito CO2); CO2 evitata
8,68 t/anno; LCO base 1.184,00 EUR/ha e LCO alt
560,00 EUR/ha (costi operativi annui per
ettaro, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato >= 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / gas in forma chiusa
(demo None: rapporto negativo meno 4,30, vince
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
Distinzione esplicita: NON cantina/vinicola (li'
si fa il vino dalle uve, qui SOLO il vigneto:
irrigazione + protezione antibrina, NIENTE
vinificazione, NIENTE cantina), NON vivaio
floricolo (li' piante ornamentali in vivaio, qui
SOLO viti da uva, NIENTE piante ornamentali,
NIENTE vivaio), NON serra (li' colture sotto
serra, qui NIENTE serra, solo vigneto in campo
aperto), NON orto (li' ortaggi, qui NIENTE
ortaggi, solo viti da uva); qui solo vigneto:
irrigazione + protezione antibrina + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w883_helpers import (
        demo_calcoli,
        mh879_c_alt,
        mh879_c_base,
        mh879_calcola,
        mh879_capex_totale,
        mh879_co2_alt,
        mh879_co2_base,
        mh879_co2_evitata,
        mh879_csv,
        mh879_demo,
        mh879_demo_calcoli,
        mh879_e_alt,
        mh879_e_base,
        mh879_e_deficit,
        mh879_e_goccia,
        mh879_e_immessa,
        mh879_e_pv,
        mh879_e_pv_auto,
        mh879_e_ventilatori,
        mh879_flussi,
        mh879_frazione,
        mh879_gas_base,
        mh879_int_pos,
        mh879_kwp,
        mh879_lco,
        mh879_nneg,
        mh879_num,
        mh879_p_gas_pareggio,
        mh879_payback,
        mh879_pos,
        mh879_ricavo_immissione,
        mh879_risparmio,
        mh879_sensibilita,
        mh879_tir,
        mh879_valida,
        mh879_van,
        mh879_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w883_helpers", os.path.join(_hf, "w883_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh879_c_alt = _mod.mh879_c_alt
    mh879_c_base = _mod.mh879_c_base
    mh879_calcola = _mod.mh879_calcola
    mh879_capex_totale = _mod.mh879_capex_totale
    mh879_co2_alt = _mod.mh879_co2_alt
    mh879_co2_base = _mod.mh879_co2_base
    mh879_co2_evitata = _mod.mh879_co2_evitata
    mh879_csv = _mod.mh879_csv
    mh879_demo = _mod.mh879_demo
    mh879_demo_calcoli = _mod.mh879_demo_calcoli
    mh879_e_alt = _mod.mh879_e_alt
    mh879_e_base = _mod.mh879_e_base
    mh879_e_deficit = _mod.mh879_e_deficit
    mh879_e_goccia = _mod.mh879_e_goccia
    mh879_e_immessa = _mod.mh879_e_immessa
    mh879_e_pv = _mod.mh879_e_pv
    mh879_e_pv_auto = _mod.mh879_e_pv_auto
    mh879_e_ventilatori = _mod.mh879_e_ventilatori
    mh879_flussi = _mod.mh879_flussi
    mh879_frazione = _mod.mh879_frazione
    mh879_gas_base = _mod.mh879_gas_base
    mh879_int_pos = _mod.mh879_int_pos
    mh879_kwp = _mod.mh879_kwp
    mh879_lco = _mod.mh879_lco
    mh879_nneg = _mod.mh879_nneg
    mh879_num = _mod.mh879_num
    mh879_p_gas_pareggio = _mod.mh879_p_gas_pareggio
    mh879_payback = _mod.mh879_payback
    mh879_pos = _mod.mh879_pos
    mh879_ricavo_immissione = _mod.mh879_ricavo_immissione
    mh879_risparmio = _mod.mh879_risparmio
    mh879_sensibilita = _mod.mh879_sensibilita
    mh879_tir = _mod.mh879_tir
    mh879_valida = _mod.mh879_valida
    mh879_van = _mod.mh879_van
    mh879_verdetto = _mod.mh879_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w883_helpers.py")
_UI_PATH = _risolvi("w883_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "8"
_VECCHIO_TAB = "tab87" + "8"
_VECCHIO_ST = "st87" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_base_kwh_anno": 16000.0,
    "gas_base_smc_anno": 2400.0,
    "c_base_eur_anno": 23680.0,
    "e_goccia_kwh_anno": 9000.0,
    "e_ventilatori_kwh_anno": 3000.0,
    "e_alt_kwh_anno": 12000.0,
    "kwp": 20.0,
    "e_pv_kwh_anno": 22000.0,
    "e_pv_auto_kwh_anno": 12000.0,
    "e_immessa_kwh_anno": 10000.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_immissione_eur_anno": 800.0,
    "c_alt_eur_anno": 11200.0,
    "risparmio_eur_anno": 12480.0,
    "capex_eur": 108000.0,
    "co2_base_t_anno": 8.68,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 8.68,
    "lco_base_eur_ha": 1184.0,
    "lco_alt_eur_ha": 560.0,
    "van": 21538.13231649377,
    "tir": 7.8209718291167825,
    "payback": 9,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh879_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh879_num(3, "x"), 3.0)
        self.assertEqual(mh879_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh879_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh879_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh879_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh879_pos(0, "x")
        with self.assertRaises(ValueError):
            mh879_pos(-1, "x")
        self.assertEqual(mh879_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh879_int_pos(15, "x"), 15)
        self.assertEqual(mh879_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh879_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh879_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh879_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh879_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh879_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh879_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_irrigazione_base_e_costo_base(self):
        self.assertEqual(mh879_e_base(20, 800), 16000.0)
        self.assertEqual(mh879_gas_base(20, 120), 2400.0)
        self.assertEqual(mh879_c_base(16000.0, 0.22, 2400.0, 0.90,
                                       18000), 23680.0)

    def test_goccia_ventilatori_somma(self):
        self.assertEqual(mh879_e_goccia(20, 450), 9000.0)
        self.assertEqual(mh879_e_ventilatori(20, 150), 3000.0)
        self.assertEqual(mh879_e_alt(9000.0, 3000.0), 12000.0)
        # La goccia RIDUCE il consumo di irrigazione,
        # non lo azzera: 450 resta sopra zero anche a
        # parita' di base 800.
        self.assertGreater(mh879_e_goccia(20, 450), 0.0)
        self.assertLess(mh879_e_goccia(20, 450),
                        mh879_e_base(20, 800))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh879_kwp(100, 0.20), 20.0)
        self.assertEqual(mh879_e_pv(20.0, 1100), 22000.0)
        self.assertEqual(mh879_e_pv_auto(22000.0, 0.60, 12000.0),
                         12000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh879_e_pv_auto(22000.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh879_e_immessa(22000.0, 12000.0), 10000.0)
        self.assertEqual(mh879_e_deficit(12000.0, 12000.0), 0.0)
        self.assertEqual(mh879_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh879_ricavo_immissione(10000.0, 0.08), 800.0)
        self.assertAlmostEqual(
            mh879_c_alt(0.0, 0.22, 800.0, 12000.0),
            11200.0)
        self.assertAlmostEqual(mh879_risparmio(23680.0, 11200.0),
                               12480.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh879_capex_totale(60000, 30000, 20.0,
                                            900),
                         108000.0)
        self.assertEqual(mh879_capex_totale(60000, 30000, 0.0,
                                            900),
                         90000.0)

    def test_co2_base_e_alt(self):
        cb = mh879_co2_base(2400.0, 1.95, 16000.0, 0.25)
        self.assertAlmostEqual(cb, 8.68, places=4)
        ca = mh879_co2_alt(0.0, 0.25)
        self.assertAlmostEqual(ca, 0.0, places=4)
        self.assertAlmostEqual(mh879_co2_evitata(cb, ca), 8.68, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh879_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh879_lco(23680.0, 20), 1184.0)
        self.assertEqual(mh879_lco(11200.0, 20), 560.0)
        with self.assertRaises(ValueError):
            mh879_lco(23680.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh879_flussi(108000, 12480.0, 3),
                         [-108000, 12480.0, 12480.0, 12480.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh879_van([-100, 60, 60], 0), 20.0)
        bc = mh879_demo_calcoli()
        self.assertAlmostEqual(mh879_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh879_demo_calcoli()
        tir = mh879_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh879_tir([-100, -10, -10]))
        self.assertIsNone(mh879_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh879_demo_calcoli()
        self.assertEqual(mh879_payback(bc["flussi"]), 9)
        self.assertIsNone(mh879_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh879_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh879_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:9]), -8160.0, places=2)
        self.assertAlmostEqual(sum(flussi[:10]), 4320.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh879_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh879_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh879_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh879_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh879_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh879_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh879_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh879_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -4.3, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh879_p_gas_pareggio(2400.0, 16000.0,
                                 0.22, 18000.0, 50000.0),
            11.866666666666667, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh879_p_gas_pareggio(2400.0, 16000.0,
                                              0.22, 18000.0, 21520.0),
                         0.0)
        self.assertIsNone(mh879_p_gas_pareggio(0.0, 16000.0,
                                               0.22, 18000.0, 50000.0))
        self.assertIsNone(mh879_p_gas_pareggio(2400.0, 16000.0,
                                               0.22, 18000.0, 11200.0))

    def test_valida_demo_ok(self):
        demo = mh879_demo()
        val = mh879_valida(*[demo[k] for k in (
            "ha_anno", "e_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_goccia_per_ha", "e_ventilatori_per_ha", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_goccia_eur", "capex_ventilatori_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_ettari_zero_no(self):
        kw = _demo_kwargs(ha_anno=0)
        self.assertRaises(ValueError, mh879_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh879_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh879_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh879_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh879_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("ha_anno", -1),
                              ("e_base_per_ha", -1),
                              ("p_gas", -0.01),
                              ("capex_goccia_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh879_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh879_calcola(mh879_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh879_calcola(dict(mh879_demo(), capex_goccia_eur=999999),
                           capex_goccia_eur=60000)
        self.assertEqual(bc["capex_eur"], 108000.0)


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
        self.assertEqual(bc["payback"], 9)

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
        s = mh879_sensibilita(**mh879_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               12912.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               26022.14, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 9)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               13184.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               28845.41, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 9)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               9040.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               3832.11, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 10)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 90000.0)
        self.assertAlmostEqual(s["senza_goccia"]["risparmio_eur_anno"],
                               11108.0, places=2)
        self.assertAlmostEqual(s["senza_goccia"]["van"],
                               7297.24, places=2)
        self.assertEqual(s["senza_goccia"]["payback"], 10)
        self.assertEqual(s["senza_goccia"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -86461.87, places=2)
        self.assertIsNone(s["capex_doppio"]["payback"])
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -11632.75, places=2)
        self.assertEqual(s["vita_10"]["payback"], 9)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               79200.0, places=2)

    def test_marginale_con_capex_goccia_alto(self):
        # CAPEX totale 138.000 (goccia a 90.000):
        # VAN circa meno 8.461,87, entro la tolleranza del 10%
        # (13.800).
        bc = mh879_calcola(**_demo_kwargs(capex_goccia_eur=90000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -8461.87, places=2)

    def test_non_convente_con_capex_goccia_altissimo(self):
        bc = mh879_calcola(**_demo_kwargs(capex_goccia_eur=120000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -38461.87, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh879_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -75520.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh879_csv(bc, mh879_demo())
        for voce in ("ha_anno", "e_base_kwh_anno",
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
                         -108000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Ettari (ettari/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh879_c_alt(12000.0, 0.22, 0.0, 12000.0)
        con = mh879_c_alt(0.0, 0.22, 800.0, 12000.0)
        self.assertAlmostEqual(senza - con, 12000.0 * 0.22 - 0.0 * 0.22 + 800.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh879_sensibilita(**mh879_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_goccia",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh879_csv(bc, mh879_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh879_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh879_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh879_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 90000.0)
        bc = mh879_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero (ettari zero): non
        # calcolabile negli helper (ValueError) e
        # guard NON_VALUTABILE in UI.
        kw = _demo_kwargs(ha_anno=0)
        self.assertRaises(ValueError, mh879_calcola, **kw)
        self.assertFalse(mh879_valida(*[kw[k] for k in (
            "ha_anno", "e_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_goccia_per_ha", "e_ventilatori_per_ha", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_goccia_eur", "capex_ventilatori_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh879_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 22000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 12000.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               1760.0)

    def test_prezzo_gas_zero(self):
        bc = mh879_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 21520.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 10320.0)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh879_calcola(**_demo_kwargs(capex_goccia_eur=0,
                                          capex_ventilatori_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh879_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 79200.0)
        self.assertEqual(bc["payback"], 9)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def879\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh879_demo().keys()), lette - set(mh879_demo().keys()))
        self.assertEqual(lette, set(mh879_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc879\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc879\["([^"]+)"\]', src))
        attese = set(mh879_demo_calcoli().keys())
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
        self.assertEqual(src.count("with tab879:"), 1)
        self.assertTrue(src.startswith("    # W883"))

    def test_ui_tab879_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab879:"), 1)
        self.assertIn("def mh879_demo(", src_h)
        self.assertIn("def mh879_calcola(", src_h)
        self.assertIn("tab879", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Vigneto: irrigazione a goccia + ventilatori antibrina elettrici + FV battono irrigazione tradizionale + riscaldamento antibrina a gas?", src)
        self.assertIn("🍇 Vigneto: irrigazione a goccia + ventilatori antibrina elettrici + FV battono irrigazione tradizionale + riscaldamento antibrina a gas?", src)
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
        chiavi = re.findall(r'key="(st879_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st879_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st879_calcola"', src)
        self.assertIn('key="st879_csv"', src)
        self.assertIn('key="st879_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg879"), src.index(".paiac("))
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
