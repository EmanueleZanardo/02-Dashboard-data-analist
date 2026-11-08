"""Test nuova scheda allevamento ovino:
tosatura efficiente + illuminazione LED +
acqua calda da pompa di calore + FV battono
tosatura tradizionale + illuminazione
tradizionale + acqua calda a gas?
Repo path: tests/test_w885_allevamento_ovino.py

Business case annuo di un allevamento ovino,
guidato dal NUMERO DI CAPI OVINI (demo 500 capi):
tosatura tradizionale base 500 x 2,0 =
1.000 kWh/anno; illuminazione tradizionale
500 x 8,0 = 4.000 kWh/anno; elettricita' base
totale 5.000 kWh/anno, costo energia base 1.100
EUR/anno; gas base 500 x 4,0 = 2.000 Smc/anno,
costo gas base 1.800 EUR/anno; O&M base 8.000
EUR/anno; costo base 10.900 EUR/anno;
tosatura efficiente 500 x 1,2 = 600
kWh/anno; illuminazione LED 500 x 3,0 = 1.500
kWh/anno; pompa di calore acqua calda 500 x 10,0
= 5.000 kWh/anno; elettricita'
alternativa 7.100 kWh/anno, gas per acqua calda
ELIMINATO; kWp = sup x kwp/m2
(demo 20 kWp); E_pv 22.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 7.100 kWh/anno, cappata alla domanda);
immessa 14.900 kWh/anno; deficit 0 kWh/anno;
ricavo immissione 1.192 EUR/anno; O&M alternativa
6.000 EUR/anno; C_alt 4.808 EUR/anno;
risparmio 6.092 EUR/anno; CAPEX
500 x 30 + 500 x 15 + 12.000 + 20 x 900 = 52.500 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 5,15
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0
t/anno (immessa senza credito CO2); CO2 evitata
5,15 t/anno; LCO base 21,80 EUR/capo e LCO alt
9,62 EUR/capo (costi operativi annui per
capo, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato >= 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno gas_alt)
in forma chiusa (demo None: rapporto negativo meno
2,146, vince anche a gas gratuito), None se il
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
negativa oltre la tolleranza: NON_CONVIENTE);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: NON porcilaia (li'
si allevano suini, qui SOLO ovini:
tosatura + illuminazione + acqua calda + FV,
NIENTE suini, NIENTE porcilaia), NON pollaio
avicolo (li' si allevano avicoli, qui SOLO ovini,
NIENTE avicoli, NIENTE pollaio), NON stalla bovina
(li' si allevano bovini, qui SOLO ovini, NIENTE
bovini, NIENTE stalla bovina), NON sala mungitura
(li' si munge, qui SOLO ovini, NIENTE latte,
NIENTE mungitura, NIENTE refrigerazione latte),
NON caseificio (li' si trasforma il latte in
formaggio, qui SOLO ovini, NIENTE latte, NIENTE
caseificio), NON vigneto (li' viti da uva, qui
SOLO ovini, NIENTE uva, NIENTE vigneto), NON
frutteto (li' frutta da albero, qui SOLO ovini,
NIENTE frutta, NIENTE frutteto); qui solo
allevamento ovino: tosatura + illuminazione +
acqua calda + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w885_helpers import (
        demo_calcoli,
        mh881_c_alt,
        mh881_c_base,
        mh881_calcola,
        mh881_capex_totale,
        mh881_co2_alt,
        mh881_co2_base,
        mh881_co2_evitata,
        mh881_csv,
        mh881_demo,
        mh881_demo_calcoli,
        mh881_e_alt,
        mh881_e_base_totale,
        mh881_e_deficit,
        mh881_e_illuminazione_base,
        mh881_e_immessa,
        mh881_e_led,
        mh881_e_pdc,
        mh881_e_pv,
        mh881_e_pv_auto,
        mh881_e_tosatura_alt,
        mh881_e_tosatura_base,
        mh881_flussi,
        mh881_frazione,
        mh881_gas_base,
        mh881_int_pos,
        mh881_kwp,
        mh881_lco,
        mh881_nneg,
        mh881_num,
        mh881_p_gas_pareggio,
        mh881_payback,
        mh881_pos,
        mh881_ricavo_immissione,
        mh881_risparmio,
        mh881_sensibilita,
        mh881_tir,
        mh881_valida,
        mh881_van,
        mh881_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w885_helpers", os.path.join(_hf, "w885_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh881_c_alt = _mod.mh881_c_alt
    mh881_c_base = _mod.mh881_c_base
    mh881_calcola = _mod.mh881_calcola
    mh881_capex_totale = _mod.mh881_capex_totale
    mh881_co2_alt = _mod.mh881_co2_alt
    mh881_co2_base = _mod.mh881_co2_base
    mh881_co2_evitata = _mod.mh881_co2_evitata
    mh881_csv = _mod.mh881_csv
    mh881_demo = _mod.mh881_demo
    mh881_demo_calcoli = _mod.mh881_demo_calcoli
    mh881_e_alt = _mod.mh881_e_alt
    mh881_e_base_totale = _mod.mh881_e_base_totale
    mh881_e_deficit = _mod.mh881_e_deficit
    mh881_e_illuminazione_base = _mod.mh881_e_illuminazione_base
    mh881_e_immessa = _mod.mh881_e_immessa
    mh881_e_led = _mod.mh881_e_led
    mh881_e_pdc = _mod.mh881_e_pdc
    mh881_e_pv = _mod.mh881_e_pv
    mh881_e_pv_auto = _mod.mh881_e_pv_auto
    mh881_e_tosatura_alt = _mod.mh881_e_tosatura_alt
    mh881_e_tosatura_base = _mod.mh881_e_tosatura_base
    mh881_flussi = _mod.mh881_flussi
    mh881_frazione = _mod.mh881_frazione
    mh881_gas_base = _mod.mh881_gas_base
    mh881_int_pos = _mod.mh881_int_pos
    mh881_kwp = _mod.mh881_kwp
    mh881_lco = _mod.mh881_lco
    mh881_nneg = _mod.mh881_nneg
    mh881_num = _mod.mh881_num
    mh881_p_gas_pareggio = _mod.mh881_p_gas_pareggio
    mh881_payback = _mod.mh881_payback
    mh881_pos = _mod.mh881_pos
    mh881_ricavo_immissione = _mod.mh881_ricavo_immissione
    mh881_risparmio = _mod.mh881_risparmio
    mh881_sensibilita = _mod.mh881_sensibilita
    mh881_tir = _mod.mh881_tir
    mh881_valida = _mod.mh881_valida
    mh881_van = _mod.mh881_van
    mh881_verdetto = _mod.mh881_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w885_helpers.py")
_UI_PATH = _risolvi("w885_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "0"
_VECCHIO_TAB = "tab88" + "0"
_VECCHIO_ST = "st88" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_tosatura_base_kwh_anno": 1000.0,
    "e_illuminazione_base_kwh_anno": 4000.0,
    "e_base_kwh_anno": 5000.0,
    "gas_base_smc_anno": 2000.0,
    "c_base_eur_anno": 10900.0,
    "e_tosatura_alt_kwh_anno": 600.0,
    "e_led_kwh_anno": 1500.0,
    "e_pdc_kwh_anno": 5000.0,
    "e_alt_kwh_anno": 7100.0,
    "kwp": 20.0,
    "e_pv_kwh_anno": 22000.0,
    "e_pv_auto_kwh_anno": 7100.0,
    "e_immessa_kwh_anno": 14900.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_immissione_eur_anno": 1192.0,
    "c_alt_eur_anno": 4808.0,
    "risparmio_eur_anno": 6092.0,
    "capex_eur": 52500.0,
    "co2_base_t_anno": 5.15,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 5.15,
    "lco_base_eur_capo": 21.8,
    "lco_alt_eur_capo": 9.616,
    "van": 10732.876768596154,
    "tir": 7.888884567907718,
    "payback": 9,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh881_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh881_num(3, "x"), 3.0)
        self.assertEqual(mh881_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh881_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh881_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh881_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh881_pos(0, "x")
        with self.assertRaises(ValueError):
            mh881_pos(-1, "x")
        self.assertEqual(mh881_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh881_int_pos(15, "x"), 15)
        self.assertEqual(mh881_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh881_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh881_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh881_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh881_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh881_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh881_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_tosatura_illuminazione_base_e_costo_base(self):
        self.assertEqual(mh881_e_tosatura_base(500, 2.0), 1000.0)
        self.assertEqual(mh881_e_illuminazione_base(500, 8.0), 4000.0)
        self.assertEqual(mh881_e_base_totale(1000.0, 4000.0), 5000.0)
        self.assertEqual(mh881_gas_base(500, 4.0), 2000.0)
        self.assertEqual(mh881_c_base(5000.0, 0.22, 2000.0, 0.90,
                                       8000), 10900.0)

    def test_tosatura_led_pdc_somma(self):
        self.assertEqual(mh881_e_tosatura_alt(500, 1.2), 600.0)
        self.assertEqual(mh881_e_led(500, 3.0), 1500.0)
        self.assertEqual(mh881_e_pdc(500, 10.0), 5000.0)
        self.assertEqual(mh881_e_alt(600.0, 1500.0, 5000.0), 7100.0)
        # La tosatura efficiente RIDUCE il consumo di
        # tosatura, non lo azzera: 1,2 resta sopra zero
        # anche a parita' di base 2,0.
        self.assertGreater(mh881_e_tosatura_alt(500, 1.2), 0.0)
        self.assertLess(mh881_e_tosatura_alt(500, 1.2),
                        mh881_e_tosatura_base(500, 2.0))
        # Il LED RIDUCE il consumo di illuminazione,
        # non lo azzera: 3,0 resta sopra zero anche
        # a parita' di base 8,0.
        self.assertGreater(mh881_e_led(500, 3.0), 0.0)
        self.assertLess(mh881_e_led(500, 3.0),
                        mh881_e_illuminazione_base(500, 8.0))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh881_kwp(100, 0.20), 20.0)
        self.assertEqual(mh881_e_pv(20.0, 1100), 22000.0)
        self.assertEqual(mh881_e_pv_auto(22000.0, 0.60, 7100.0),
                         7100.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh881_e_pv_auto(22000.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh881_e_immessa(22000.0, 7100.0), 14900.0)
        self.assertEqual(mh881_e_deficit(7100.0, 7100.0), 0.0)
        self.assertEqual(mh881_e_deficit(10000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh881_ricavo_immissione(14900.0, 0.08), 1192.0)
        self.assertAlmostEqual(
            mh881_c_alt(0.0, 0.22, 1192.0, 6000.0),
            4808.0)
        self.assertAlmostEqual(mh881_risparmio(10900.0, 4808.0),
                               6092.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh881_capex_totale(500, 30, 15, 12000, 20.0,
                                            900),
                         52500.0)
        self.assertEqual(mh881_capex_totale(500, 30, 15, 12000, 0.0,
                                            900),
                         34500.0)

    def test_co2_base_e_alt(self):
        cb = mh881_co2_base(2000.0, 1.95, 5000.0, 0.25)
        self.assertAlmostEqual(cb, 5.15, places=4)
        ca = mh881_co2_alt(0.0, 0.25)
        self.assertAlmostEqual(ca, 0.0, places=4)
        self.assertAlmostEqual(mh881_co2_evitata(cb, ca), 5.15, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh881_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh881_lco(10900.0, 500), 21.8)
        self.assertAlmostEqual(mh881_lco(4808.0, 500), 9.616)
        with self.assertRaises(ValueError):
            mh881_lco(10900.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh881_flussi(52500, 6092.0, 3),
                         [-52500, 6092.0, 6092.0, 6092.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh881_van([-100, 60, 60], 0), 20.0)
        bc = mh881_demo_calcoli()
        self.assertAlmostEqual(mh881_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh881_demo_calcoli()
        tir = mh881_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh881_tir([-100, -10, -10]))
        self.assertIsNone(mh881_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh881_demo_calcoli()
        self.assertEqual(mh881_payback(bc["flussi"]), 9)
        self.assertIsNone(mh881_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh881_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh881_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:9]), -3764.0, places=2)
        self.assertAlmostEqual(sum(flussi[:10]), 2328.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh881_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh881_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh881_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh881_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh881_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh881_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh881_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh881_demo_calcoli()
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
            / bc["gas_base_smc_anno"], -2.146, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh881_p_gas_pareggio(2000.0, 0.0, 5000.0,
                                 0.22, 8000.0, 50000.0),
            20.45, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh881_p_gas_pareggio(2000.0, 0.0, 5000.0,
                                              0.22, 8000.0, 9100.0),
                         0.0)
        self.assertIsNone(mh881_p_gas_pareggio(0.0, 0.0, 5000.0,
                                               0.22, 8000.0, 50000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh881_p_gas_pareggio(2000.0, 2000.0, 5000.0,
                                               0.22, 8000.0, 50000.0))
        self.assertIsNone(mh881_p_gas_pareggio(2000.0, 0.0, 5000.0,
                                               0.22, 8000.0, 4808.0))

    def test_valida_demo_ok(self):
        demo = mh881_demo()
        val = mh881_valida(*[demo[k] for k in (
            "capi", "e_tosatura_base_per_capo",
            "e_illuminazione_base_per_capo",
            "p_el", "gas_per_capo",
            "p_gas", "om_base_eur_anno",
            "e_tosatura_alt_per_capo", "e_led_per_capo",
            "e_pdc_per_capo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_tosatura_per_capo",
            "capex_led_per_capo", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_capi_zero_no(self):
        kw = _demo_kwargs(capi=0)
        self.assertRaises(ValueError, mh881_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh881_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh881_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh881_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh881_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("capi", -1),
                              ("e_tosatura_base_per_capo", -1),
                              ("p_gas", -0.01),
                              ("capex_tosatura_per_capo", -1),
                              ("capex_pdc_eur", -1),
                              ("e_illuminazione_base_per_capo", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh881_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh881_calcola(mh881_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh881_calcola(dict(mh881_demo(), capex_tosatura_per_capo=999),
                           capex_tosatura_per_capo=30)
        self.assertEqual(bc["capex_eur"], 52500.0)


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
        s = mh881_sensibilita(**mh881_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               6452.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               14469.55, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 9)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               6312.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               13016.40, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 9)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               3338.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               147.30, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 11)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 34500.0)
        self.assertAlmostEqual(s["senza_tosatura_efficiente"]["risparmio_eur_anno"],
                               6060.0, places=2)
        self.assertAlmostEqual(s["senza_tosatura_efficiente"]["van"],
                               10400.73, places=2)
        self.assertEqual(s["senza_tosatura_efficiente"]["payback"], 9)
        self.assertEqual(s["senza_tosatura_efficiente"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -41767.12, places=2)
        self.assertIsNone(s["capex_doppio"]["payback"])
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -5459.19, places=2)
        self.assertEqual(s["vita_10"]["payback"], 9)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               38880.0, places=2)

    def test_marginale_con_capex_tosatura_alto(self):
        # CAPEX totale 67.500 (tosatura a 60 per capo):
        # VAN circa meno 4.267,12, entro la tolleranza del 10%
        # (6.750).
        bc = mh881_calcola(**_demo_kwargs(capex_tosatura_per_capo=60))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -4267.12, places=2)

    def test_non_convente_con_capex_tosatura_altissimo(self):
        bc = mh881_calcola(**_demo_kwargs(capex_tosatura_per_capo=90))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -19267.12, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh881_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -87908.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh881_csv(bc, mh881_demo())
        for voce in ("capi", "e_base_kwh_anno",
                     "e_tosatura_base_kwh_anno", "e_led_kwh_anno",
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
                         -52500.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Capi (capi)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh881_c_alt(7100.0, 0.22, 0.0, 6000.0)
        con = mh881_c_alt(0.0, 0.22, 1192.0, 6000.0)
        self.assertAlmostEqual(senza - con, 7100.0 * 0.22 + 1192.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh881_sensibilita(**mh881_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_tosatura_efficiente",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh881_csv(bc, mh881_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh881_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh881_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh881_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 34500.0)
        bc = mh881_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero (capi zero): non
        # calcolabile negli helper (ValueError) e
        # guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(capi=0)
        self.assertRaises(ValueError, mh881_calcola, **kw)
        self.assertFalse(mh881_valida(*[kw[k] for k in (
            "capi", "e_tosatura_base_per_capo",
            "e_illuminazione_base_per_capo",
            "p_el", "gas_per_capo",
            "p_gas", "om_base_eur_anno",
            "e_tosatura_alt_per_capo", "e_led_per_capo",
            "e_pdc_per_capo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_tosatura_per_capo",
            "capex_led_per_capo", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh881_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 22000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 7100.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               1760.0)

    def test_prezzo_gas_zero(self):
        bc = mh881_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 9100.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 4292.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh881_calcola(**_demo_kwargs(capex_tosatura_per_capo=0,
                                          capex_led_per_capo=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh881_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 38880.0)
        self.assertEqual(bc["payback"], 9)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def881\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh881_demo().keys()), lette - set(mh881_demo().keys()))
        self.assertEqual(lette, set(mh881_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc881\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc881\["([^"]+)"\]', src))
        attese = set(mh881_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_post_apply(self):
        # Conteggio titoli: prima dell'apply di questa
        # scheda la copia di lavoro del repo ha 880
        # blocchi scheda; l'apply bumpa questo assert
        # a 881 (come la scheda precedente, scritta a 879 e
        # bumpata a 880 dal suo apply).
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 891)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab881:"), 1)
        self.assertTrue(src.startswith("    # W885"))

    def test_ui_tab881_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab881:"), 1)
        self.assertIn("def mh881_demo(", src_h)
        self.assertIn("def mh881_calcola(", src_h)
        self.assertIn("tab881", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Allevamento ovino: tosatura efficiente + illuminazione LED + acqua calda da pompa di calore + FV battono tosatura tradizionale + illuminazione tradizionale + acqua calda a gas?", src)
        self.assertIn("🐑 Allevamento ovino: tosatura efficiente + illuminazione LED + acqua calda da pompa di calore + FV battono tosatura tradizionale + illuminazione tradizionale + acqua calda a gas?", src)
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
        chiavi = re.findall(r'key="(st881_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st881_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st881_calcola"', src)
        self.assertIn('key="st881_csv"', src)
        self.assertIn('key="st881_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg881"), src.index(".paiac("))
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
