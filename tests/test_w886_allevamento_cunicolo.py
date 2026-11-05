"""Test nuova scheda coniglicoltura:
ventilazione efficiente + illuminazione LED +
riscaldamento da pompa di calore + FV battono
ventilazione tradizionale + illuminazione
tradizionale + riscaldamento a gas?
Repo path: tests/test_w886_allevamento_cunicolo.py

Business case annuo di una coniglicoltura,
guidato dal NUMERO DI CAPI CONIGLI (demo 2000 capi):
ventilazione tradizionale base 2000 x 6,0 =
12.000 kWh/anno; illuminazione tradizionale
2000 x 2,0 = 4.000 kWh/anno; elettricita' base
totale 16.000 kWh/anno, costo energia base 3.520
EUR/anno; gas base 2000 x 1,5 = 3.000 Smc/anno,
costo gas base 2.700 EUR/anno; O&M base 12.000
EUR/anno; costo base 18.220 EUR/anno;
ventilazione efficiente 2000 x 3,0 = 6.000
kWh/anno; illuminazione LED 2000 x 0,8 = 1.600
kWh/anno; pompa di calore riscaldamento 2000 x 2,5
= 5.000 kWh/anno; elettricita'
alternativa 12.600 kWh/anno, gas per riscaldamento
ELIMINATO; kWp = sup x kwp/m2
(demo 20 kWp); E_pv 22.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 12.600 kWh/anno, cappata alla domanda);
immessa 9.400 kWh/anno; deficit 0 kWh/anno;
ricavo immissione 752 EUR/anno; O&M alternativa
9.000 EUR/anno; C_alt 8.248 EUR/anno;
risparmio 9.972 EUR/anno; CAPEX
15.000 + 2000 x 5 + 14.000 + 20 x 900 = 57.000 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 9,85
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0
t/anno (immessa senza credito CO2); CO2 evitata
9,85 t/anno; LCO base 9,11 EUR/capo e LCO alt
4,12 EUR/capo arrotondato a 2 decimali da 4,124
(costi operativi annui per
capo, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato >= 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno gas_alt)
in forma chiusa (demo None: rapporto negativo meno
2,424, vince anche a gas gratuito), None se il
denominatore e' nullo o negativo o se il rapporto e'
negativo. L'alternativa non usa gas, quindi gas_alt
= 0 e il denominatore e' gas_base.
E' una SOGLIA MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa vince, sotto
perde. Verdetto: NON_CALCOLABILE se input degenere
(capi <= 0, kWh per capo < 0, prezzi <
0, O&M < 0, superficie < 0, kwp per m2 < 0, resa <
0, f_autoconsumo < 0 o > 1, voci CAPEX < 0,
fattori CO2 < 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: produzione zero (capi zero) non
calcolabile (ValueError negli helper, guard
NON_CALCOLABILE in UI); quota FV zero
(f_autoconsumo zero, autoconsumo zero); prezzo gas
zero (ancora calcolabile, risparmio positivo, VAN
positiva: CONVIENTE);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: NON porcilaia (li'
si allevano suini, qui SOLO conigli:
ventilazione + illuminazione + riscaldamento + FV,
NIENTE suini, NIENTE porcilaia), NON pollaio
avicolo (li' si allevano avicoli, qui SOLO conigli,
NIENTE avicoli, NIENTE pollaio), NON stalla bovina
(li' si allevano bovini, qui SOLO conigli, NIENTE
bovini, NIENTE stalla bovina), NON sala mungitura
(li' si munge, qui SOLO conigli, NIENTE latte,
NIENTE mungitura, NIENTE refrigerazione latte),
NON caseificio (li' si trasforma il latte in
formaggio, qui SOLO conigli, NIENTE latte, NIENTE
caseificio), NON vigneto (li' viti da uva, qui
SOLO conigli, NIENTE uva, NIENTE vigneto), NON
frutteto (li' frutta da albero, qui SOLO conigli,
NIENTE frutta, NIENTE frutteto); qui solo
coniglicoltura: ventilazione + illuminazione +
riscaldamento + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w886_helpers import (
        demo_calcoli,
        mh882_c_alt,
        mh882_c_base,
        mh882_calcola,
        mh882_capex_totale,
        mh882_co2_alt,
        mh882_co2_base,
        mh882_co2_evitata,
        mh882_csv,
        mh882_demo,
        mh882_demo_calcoli,
        mh882_e_alt,
        mh882_e_base_totale,
        mh882_e_deficit,
        mh882_e_illuminazione_base,
        mh882_e_immessa,
        mh882_e_led,
        mh882_e_pdc,
        mh882_e_pv,
        mh882_e_pv_auto,
        mh882_e_ventilazione_alt,
        mh882_e_ventilazione_base,
        mh882_flussi,
        mh882_frazione,
        mh882_gas_base,
        mh882_int_pos,
        mh882_kwp,
        mh882_lco,
        mh882_nneg,
        mh882_num,
        mh882_p_gas_pareggio,
        mh882_payback,
        mh882_pos,
        mh882_ricavo_immissione,
        mh882_risparmio,
        mh882_sensibilita,
        mh882_tir,
        mh882_valida,
        mh882_van,
        mh882_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w886_helpers", os.path.join(_hf, "w886_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh882_c_alt = _mod.mh882_c_alt
    mh882_c_base = _mod.mh882_c_base
    mh882_calcola = _mod.mh882_calcola
    mh882_capex_totale = _mod.mh882_capex_totale
    mh882_co2_alt = _mod.mh882_co2_alt
    mh882_co2_base = _mod.mh882_co2_base
    mh882_co2_evitata = _mod.mh882_co2_evitata
    mh882_csv = _mod.mh882_csv
    mh882_demo = _mod.mh882_demo
    mh882_demo_calcoli = _mod.mh882_demo_calcoli
    mh882_e_alt = _mod.mh882_e_alt
    mh882_e_base_totale = _mod.mh882_e_base_totale
    mh882_e_deficit = _mod.mh882_e_deficit
    mh882_e_illuminazione_base = _mod.mh882_e_illuminazione_base
    mh882_e_immessa = _mod.mh882_e_immessa
    mh882_e_led = _mod.mh882_e_led
    mh882_e_pdc = _mod.mh882_e_pdc
    mh882_e_pv = _mod.mh882_e_pv
    mh882_e_pv_auto = _mod.mh882_e_pv_auto
    mh882_e_ventilazione_alt = _mod.mh882_e_ventilazione_alt
    mh882_e_ventilazione_base = _mod.mh882_e_ventilazione_base
    mh882_flussi = _mod.mh882_flussi
    mh882_frazione = _mod.mh882_frazione
    mh882_gas_base = _mod.mh882_gas_base
    mh882_int_pos = _mod.mh882_int_pos
    mh882_kwp = _mod.mh882_kwp
    mh882_lco = _mod.mh882_lco
    mh882_nneg = _mod.mh882_nneg
    mh882_num = _mod.mh882_num
    mh882_p_gas_pareggio = _mod.mh882_p_gas_pareggio
    mh882_payback = _mod.mh882_payback
    mh882_pos = _mod.mh882_pos
    mh882_ricavo_immissione = _mod.mh882_ricavo_immissione
    mh882_risparmio = _mod.mh882_risparmio
    mh882_sensibilita = _mod.mh882_sensibilita
    mh882_tir = _mod.mh882_tir
    mh882_valida = _mod.mh882_valida
    mh882_van = _mod.mh882_van
    mh882_verdetto = _mod.mh882_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w886_helpers.py")
_UI_PATH = _risolvi("w886_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "1"
_VECCHIO_TAB = "tab88" + "1"
_VECCHIO_ST = "st88" + "1_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_ventilazione_base_kwh_anno": 12000.0,
    "e_illuminazione_base_kwh_anno": 4000.0,
    "e_base_kwh_anno": 16000.0,
    "gas_base_smc_anno": 3000.0,
    "c_base_eur_anno": 18220.0,
    "e_ventilazione_alt_kwh_anno": 6000.0,
    "e_led_kwh_anno": 1600.0,
    "e_pdc_kwh_anno": 5000.0,
    "e_alt_kwh_anno": 12600.0,
    "kwp": 20.0,
    "e_pv_kwh_anno": 22000.0,
    "e_pv_auto_kwh_anno": 12600.0,
    "e_immessa_kwh_anno": 9400.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_immissione_eur_anno": 752.0,
    "c_alt_eur_anno": 8248.0,
    "risparmio_eur_anno": 9972.0,
    "capex_eur": 57000.0,
    "co2_base_t_anno": 9.85,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 9.85,
    "lco_base_eur_capo": 9.11,
    "lco_alt_eur_capo": 4.124,
    "van": 46505.94995673683,
    "tir": 15.473151167446481,
    "payback": 6,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh882_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh882_num(3, "x"), 3.0)
        self.assertEqual(mh882_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh882_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh882_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh882_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh882_pos(0, "x")
        with self.assertRaises(ValueError):
            mh882_pos(-1, "x")
        self.assertEqual(mh882_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh882_int_pos(15, "x"), 15)
        self.assertEqual(mh882_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh882_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh882_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh882_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh882_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh882_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh882_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_ventilazione_illuminazione_base_e_costo_base(self):
        self.assertEqual(mh882_e_ventilazione_base(2000, 6.0), 12000.0)
        self.assertEqual(mh882_e_illuminazione_base(2000, 2.0), 4000.0)
        self.assertEqual(mh882_e_base_totale(12000.0, 4000.0), 16000.0)
        self.assertEqual(mh882_gas_base(2000, 1.5), 3000.0)
        self.assertEqual(mh882_c_base(16000.0, 0.22, 3000.0, 0.90,
                                       12000), 18220.0)

    def test_ventilazione_led_pdc_somma(self):
        self.assertEqual(mh882_e_ventilazione_alt(2000, 3.0), 6000.0)
        self.assertEqual(mh882_e_led(2000, 0.8), 1600.0)
        self.assertEqual(mh882_e_pdc(2000, 2.5), 5000.0)
        self.assertEqual(mh882_e_alt(6000.0, 1600.0, 5000.0), 12600.0)
        # La ventilazione efficiente RIDUCE il consumo di
        # ventilazione, non lo azzera: 3,0 resta sopra zero
        # anche a parita' di base 6,0.
        self.assertGreater(mh882_e_ventilazione_alt(2000, 3.0), 0.0)
        self.assertLess(mh882_e_ventilazione_alt(2000, 3.0),
                        mh882_e_ventilazione_base(2000, 6.0))
        # Il LED RIDUCE il consumo di illuminazione,
        # non lo azzera: 0,8 resta sopra zero anche
        # a parita' di base 2,0.
        self.assertGreater(mh882_e_led(2000, 0.8), 0.0)
        self.assertLess(mh882_e_led(2000, 0.8),
                        mh882_e_illuminazione_base(2000, 2.0))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh882_kwp(100, 0.20), 20.0)
        self.assertEqual(mh882_e_pv(20.0, 1100), 22000.0)
        self.assertEqual(mh882_e_pv_auto(22000.0, 0.60, 12600.0),
                         12600.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh882_e_pv_auto(22000.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh882_e_immessa(22000.0, 12600.0), 9400.0)
        self.assertEqual(mh882_e_deficit(12600.0, 12600.0), 0.0)
        self.assertEqual(mh882_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh882_ricavo_immissione(9400.0, 0.08), 752.0)
        self.assertAlmostEqual(
            mh882_c_alt(0.0, 0.22, 752.0, 9000.0),
            8248.0)
        self.assertAlmostEqual(mh882_risparmio(18220.0, 8248.0),
                               9972.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh882_capex_totale(2000, 15000, 5, 14000, 20.0,
                                            900),
                         57000.0)
        self.assertEqual(mh882_capex_totale(2000, 15000, 5, 14000, 0.0,
                                            900),
                         39000.0)

    def test_co2_base_e_alt(self):
        cb = mh882_co2_base(3000.0, 1.95, 16000.0, 0.25)
        self.assertAlmostEqual(cb, 9.85, places=4)
        ca = mh882_co2_alt(0.0, 0.25)
        self.assertAlmostEqual(ca, 0.0, places=4)
        self.assertAlmostEqual(mh882_co2_evitata(cb, ca), 9.85, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh882_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh882_lco(18220.0, 2000), 9.11)
        self.assertAlmostEqual(mh882_lco(8248.0, 2000), 4.124)
        with self.assertRaises(ValueError):
            mh882_lco(18220.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh882_flussi(57000, 9972.0, 3),
                         [-57000, 9972.0, 9972.0, 9972.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh882_van([-100, 60, 60], 0), 20.0)
        bc = mh882_demo_calcoli()
        self.assertAlmostEqual(mh882_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh882_demo_calcoli()
        tir = mh882_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh882_tir([-100, -10, -10]))
        self.assertIsNone(mh882_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh882_demo_calcoli()
        self.assertEqual(mh882_payback(bc["flussi"]), 6)
        self.assertIsNone(mh882_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh882_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh882_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:6]), -7140.0, places=2)
        self.assertAlmostEqual(sum(flussi[:7]), 2832.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh882_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh882_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh882_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh882_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh882_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh882_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh882_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh882_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -2.424, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh882_p_gas_pareggio(3000.0, 0.0, 16000.0,
                                 0.22, 12000.0, 50000.0),
            11.4933333333, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh882_p_gas_pareggio(3000.0, 0.0, 16000.0,
                                              0.22, 12000.0, 15520.0),
                         0.0)
        self.assertIsNone(mh882_p_gas_pareggio(0.0, 0.0, 16000.0,
                                               0.22, 12000.0, 50000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh882_p_gas_pareggio(3000.0, 3000.0, 16000.0,
                                               0.22, 12000.0, 50000.0))
        self.assertIsNone(mh882_p_gas_pareggio(3000.0, 0.0, 16000.0,
                                               0.22, 12000.0, 8248.0))

    def test_valida_demo_ok(self):
        demo = mh882_demo()
        val = mh882_valida(*[demo[k] for k in (
            "capi", "e_ventilazione_base_per_capo",
            "e_illuminazione_base_per_capo",
            "p_el", "gas_per_capo",
            "p_gas", "om_base_eur_anno",
            "e_ventilazione_alt_per_capo", "e_led_per_capo",
            "e_pdc_per_capo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_ventilazione_eur",
            "capex_led_per_capo", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_capi_zero_no(self):
        kw = _demo_kwargs(capi=0)
        self.assertRaises(ValueError, mh882_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh882_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh882_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh882_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh882_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("capi", -1),
                              ("e_ventilazione_base_per_capo", -1),
                              ("p_gas", -0.01),
                              ("capex_ventilazione_eur", -1),
                              ("capex_pdc_eur", -1),
                              ("e_illuminazione_base_per_capo", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh882_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh882_calcola(mh882_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh882_calcola(dict(mh882_demo(), capex_ventilazione_eur=99999),
                           capex_ventilazione_eur=15000)
        self.assertEqual(bc["capex_eur"], 57000.0)


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
        self.assertAlmostEqual(
            bc["lco_base_eur_capo"],
            bc["c_base_eur_anno"] / bc["capi"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_capo"],
            bc["c_alt_eur_anno"] / bc["capi"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh882_sensibilita(**mh882_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               10512.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               52110.97, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               10676.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               53813.23, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               6448.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               27928.04, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 7)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 39000.0)
        self.assertAlmostEqual(s["senza_ventilazione_efficiente"]["risparmio_eur_anno"],
                               8736.0, places=2)
        self.assertAlmostEqual(s["senza_ventilazione_efficiente"]["van"],
                               33676.69, places=2)
        self.assertEqual(s["senza_ventilazione_efficiente"]["payback"], 7)
        self.assertEqual(s["senza_ventilazione_efficiente"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -10494.05, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 12)
        self.assertEqual(s["capex_doppio"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               20001.14, places=2)
        self.assertEqual(s["vita_10"]["payback"], 6)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               92580.0, places=2)

    def test_marginale_con_capex_led_alto(self):
        # CAPEX totale 107.000 (LED a 30 per capo):
        # VAN circa meno 3.494,05, entro la tolleranza del 10%
        # (10.700).
        bc = mh882_calcola(**_demo_kwargs(capex_led_per_capo=30))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -3494.05, places=2)

    def test_non_convente_con_capex_led_altissimo(self):
        bc = mh882_calcola(**_demo_kwargs(capex_led_per_capo=35))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -13494.05, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh882_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -81028.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh882_csv(bc, mh882_demo())
        for voce in ("capi", "e_base_kwh_anno",
                     "e_ventilazione_base_kwh_anno", "e_led_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_capo", "lco_alt_eur_capo"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -57000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Capi (capi)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh882_c_alt(12600.0, 0.22, 0.0, 9000.0)
        con = mh882_c_alt(0.0, 0.22, 752.0, 9000.0)
        self.assertAlmostEqual(senza - con, 12600.0 * 0.22 + 752.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh882_sensibilita(**mh882_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_ventilazione_efficiente",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh882_csv(bc, mh882_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh882_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh882_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh882_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 39000.0)
        bc = mh882_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero (capi zero): non
        # calcolabile negli helper (ValueError) e
        # guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(capi=0)
        self.assertRaises(ValueError, mh882_calcola, **kw)
        self.assertFalse(mh882_valida(*[kw[k] for k in (
            "capi", "e_ventilazione_base_per_capo",
            "e_illuminazione_base_per_capo",
            "p_el", "gas_per_capo",
            "p_gas", "om_base_eur_anno",
            "e_ventilazione_alt_per_capo", "e_led_per_capo",
            "e_pdc_per_capo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_ventilazione_eur",
            "capex_led_per_capo", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh882_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 22000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 12600.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               1760.0)

    def test_prezzo_gas_zero(self):
        bc = mh882_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 15520.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 7272.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh882_calcola(**_demo_kwargs(capex_ventilazione_eur=0,
                                          capex_led_per_capo=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh882_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 92580.0)
        self.assertEqual(bc["payback"], 6)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def882\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh882_demo().keys()), lette - set(mh882_demo().keys()))
        self.assertEqual(lette, set(mh882_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc882\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc882\["([^"]+)"\]', src))
        attese = set(mh882_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_post_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 881 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 888)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab882:"), 1)
        self.assertTrue(src.startswith("    # W886"))

    def test_ui_tab882_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab882:"), 1)
        self.assertIn("def mh882_demo(", src_h)
        self.assertIn("def mh882_calcola(", src_h)
        self.assertIn("tab882", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Coniglicoltura: ventilazione efficiente + illuminazione LED + riscaldamento da pompa di calore + FV battono ventilazione tradizionale + illuminazione tradizionale + riscaldamento a gas?", src)
        self.assertIn("🐰 Coniglicoltura: ventilazione efficiente + illuminazione LED + riscaldamento da pompa di calore + FV battono ventilazione tradizionale + illuminazione tradizionale + riscaldamento a gas?", src)
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
        chiavi = re.findall(r'key="(st882_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st882_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st882_calcola"', src)
        self.assertIn('key="st882_csv"', src)
        self.assertIn('key="st882_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg882"), src.index(".paiac("))
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

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato).
        import textwrap as _tw
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            if percorso == _UI_PATH:
                src = _tw.dedent(src)
            tree = ast.parse(src)
            for nodo in ast.walk(tree):
                if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                    if nodo.value == "utf-8":
                        continue
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)


if __name__ == "__main__":
    unittest.main()
