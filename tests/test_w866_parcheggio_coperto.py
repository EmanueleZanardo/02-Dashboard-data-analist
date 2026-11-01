"""Test nuova scheda parcheggio coperto: LED +
ventilazione a controllo CO + FV su
pensiline/copertura + ricarica EV battono
illuminazione tradizionale + ventilazione
sempre accesa?

Business case annuo di un parcheggio
coperto, guidato dai POSTI AUTO per i M2
PER POSTO e dalle ORE DI APERTURA:
sup = n_posti x m2_per_posto (demo 300 x
25 = 7.500 m2); E_light_base = sup x
w_light_base / 1000 x ore (demo 360.000
kWh/anno); E_vent_base = sup x
w_vent_base / 1000 x ore (demo 270.000
kWh/anno); domanda base 630.000
kWh/anno, costo base 176.400 EUR/anno;
E_led = sup x w_led / 1000 x ore (demo
135.000 kWh/anno); E_vent_alt =
E_vent_base x f_vent_co (demo 121.500
kWh/anno); E_ev = n_colonnine x
kwh_ev_colonnina (demo 20 x 2.000 =
40.000 kWh/anno, driver ESPLICITO, non
il 10% dei posti); domanda alt 296.500
kWh/anno; kWp = sup x quota_fv x
kwp_per_m2 (demo 600 kWp); E_pv = kWp x
resa (demo 660.000 kWh/anno); E_pv_auto
= min(E_pv x f_autoconsumo, domanda alt)
(demo 296.500 kWh/anno, cappata alla
domanda); E_immessa = E_pv - E_pv_auto
(demo 363.500 kWh/anno); E_deficit =
max(0, domanda alt - E_pv_auto) (demo 0);
ricavo EV = E_ev x p_ev (demo 18.000
EUR/anno, venduta, NON costo netto);
ricavo immissione = E_immessa x
p_immissione (demo 29.080 EUR/anno);
C_alt = deficit x p_el - ricavo
immissione - ricavo EV (demo -47.080
EUR/anno, ricavo netto); risparmio =
C_base - C_alt (demo 223.480 EUR/anno);
CAPEX = sup x capex_led_m2 +
capex_vent_co + kWp x capex_fv +
n_colonnine x capex_colonnina (demo
815.000 EUR); CO2 base = domanda base x
0,25 / 1000 (demo 157,50 t/anno); CO2 alt
= deficit x 0,25 / 1000 (demo 0, immessa
senza credito CO2); CO2 evitata =
base - alt (segno libero); flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo elettrico di
pareggio p_el_star = (-E_immessa x
p_immissione - E_ev x p_ev) /
(E_domanda_base - E_deficit) in forma
chiusa (demo None: rapporto negativo
-0,074730, vince anche a elettricita'
gratuita), None se il denominatore e'
nullo o se il rapporto e' negativo.
Con ricavi non negativi il numeratore
non puo' essere positivo: gli unici casi
non-None sono 0,0 (ricavi nulli).
E' una SOGLIA MINIMA sui soli costi
annui (CAPEX escluso): sopra di essa
l'alternativa vince, sotto perde.
Verdetto: NON_CALCOLABILE se input
degenere (n_posti <= 0 o non intero,
m2_per_posto <= 0, ore/potenze < 0,
f_vent_co/quota_fv/f_autoconsumo < 0 o
> 1, n_colonnine < 0 o non intero,
kwh_ev < 0, prezzi < 0, kwp_per_m2 < 0,
resa < 0, voci CAPEX < 0, fattore CO2
< 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del
CAPEX, NON_CONVIENTE altrimenti.
Distinzione esplicita: NON autorimessa
condominiale piccola (pochi posti,
niente ventilazione meccanica
dimensionata), NON autosilo
automatizzato (niente circolazione
pedonale/illuminazione per piano), NON
parcheggio scoperto senza copertura
(niente FV su copertura/pensiline e
niente ventilazione di ambiente
chiuso).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w866_helpers import (
        demo_calcoli,
        mh862_c_alt,
        mh862_c_base,
        mh862_calcola,
        mh862_capex_totale,
        mh862_co2_alt,
        mh862_co2_base,
        mh862_co2_evitata,
        mh862_csv,
        mh862_demo,
        mh862_demo_calcoli,
        mh862_e_deficit,
        mh862_e_domanda_alt,
        mh862_e_domanda_base,
        mh862_e_ev,
        mh862_e_immessa,
        mh862_e_led,
        mh862_e_light_base,
        mh862_e_pv,
        mh862_e_pv_auto,
        mh862_e_vent_alt,
        mh862_e_vent_base,
        mh862_flussi,
        mh862_frazione,
        mh862_int_nneg,
        mh862_int_pos,
        mh862_kwp,
        mh862_nneg,
        mh862_num,
        mh862_p_el_pareggio,
        mh862_payback,
        mh862_pos,
        mh862_ricavo_ev,
        mh862_ricavo_immissione,
        mh862_risparmio,
        mh862_sensibilita,
        mh862_sup,
        mh862_tir,
        mh862_valida,
        mh862_van,
        mh862_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w866_helpers", os.path.join(_hf, "w866_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh862_c_alt = _mod.mh862_c_alt
    mh862_c_base = _mod.mh862_c_base
    mh862_calcola = _mod.mh862_calcola
    mh862_capex_totale = _mod.mh862_capex_totale
    mh862_co2_alt = _mod.mh862_co2_alt
    mh862_co2_base = _mod.mh862_co2_base
    mh862_co2_evitata = _mod.mh862_co2_evitata
    mh862_csv = _mod.mh862_csv
    mh862_demo = _mod.mh862_demo
    mh862_demo_calcoli = _mod.mh862_demo_calcoli
    mh862_e_deficit = _mod.mh862_e_deficit
    mh862_e_domanda_alt = _mod.mh862_e_domanda_alt
    mh862_e_domanda_base = _mod.mh862_e_domanda_base
    mh862_e_ev = _mod.mh862_e_ev
    mh862_e_immessa = _mod.mh862_e_immessa
    mh862_e_led = _mod.mh862_e_led
    mh862_e_light_base = _mod.mh862_e_light_base
    mh862_e_pv = _mod.mh862_e_pv
    mh862_e_pv_auto = _mod.mh862_e_pv_auto
    mh862_e_vent_alt = _mod.mh862_e_vent_alt
    mh862_e_vent_base = _mod.mh862_e_vent_base
    mh862_flussi = _mod.mh862_flussi
    mh862_frazione = _mod.mh862_frazione
    mh862_int_nneg = _mod.mh862_int_nneg
    mh862_int_pos = _mod.mh862_int_pos
    mh862_kwp = _mod.mh862_kwp
    mh862_nneg = _mod.mh862_nneg
    mh862_num = _mod.mh862_num
    mh862_p_el_pareggio = _mod.mh862_p_el_pareggio
    mh862_payback = _mod.mh862_payback
    mh862_pos = _mod.mh862_pos
    mh862_ricavo_ev = _mod.mh862_ricavo_ev
    mh862_ricavo_immissione = _mod.mh862_ricavo_immissione
    mh862_risparmio = _mod.mh862_risparmio
    mh862_sensibilita = _mod.mh862_sensibilita
    mh862_sup = _mod.mh862_sup
    mh862_tir = _mod.mh862_tir
    mh862_valida = _mod.mh862_valida
    mh862_van = _mod.mh862_van
    mh862_verdetto = _mod.mh862_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w866_helpers.py")
_UI_PATH = _risolvi("w866_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "1"
_VECCHIO_TAB = "tab86" + "1"
_VECCHIO_ST = "st86" + "1_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "sup_m2": 7500.0,
    "e_light_base_kwh_anno": 360000.0,
    "e_vent_base_kwh_anno": 270000.0,
    "e_domanda_base_kwh_anno": 630000.0,
    "c_base_eur_anno": 176400.0,
    "e_led_kwh_anno": 135000.0,
    "e_vent_alt_kwh_anno": 121500.0,
    "e_ev_kwh_anno": 40000.0,
    "e_domanda_alt_kwh_anno": 296500.0,
    "kwp": 600.0,
    "e_pv_kwh_anno": 660000.0,
    "e_pv_auto_kwh_anno": 296500.0,
    "e_immessa_kwh_anno": 363500.0,
    "e_deficit_kwh_anno": 0.0,
    "ricavo_ev_eur_anno": 18000.0,
    "ricavo_immissione_eur_anno": 29080.0,
    "c_alt_eur_anno": -47080.0,
    "risparmio_eur_anno": 223480.0,
    "capex_eur": 815000.0,
    "co2_base_t_anno": 157.5,
    "co2_alt_t_anno": 0.0,
    "co2_evitata_t_anno": 157.5,
    "van": 1970054.767350835,
    "tir": 27.19776299863024,
    "payback": 4,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh862_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh862_num(3, "x"), 3.0)
        self.assertEqual(mh862_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh862_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh862_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh862_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh862_pos(0, "x")
        with self.assertRaises(ValueError):
            mh862_pos(-1, "x")
        self.assertEqual(mh862_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh862_int_pos(300, "x"), 300)
        self.assertEqual(mh862_int_pos(300.0, "x"), 300)
        with self.assertRaises(ValueError):
            mh862_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh862_int_pos(300.5, "x")

    def test_int_nneg(self):
        self.assertEqual(mh862_int_nneg(0, "x"), 0)
        self.assertEqual(mh862_int_nneg(20, "x"), 20)
        with self.assertRaises(ValueError):
            mh862_int_nneg(-1, "x")
        with self.assertRaises(ValueError):
            mh862_int_nneg(2.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh862_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh862_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh862_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh862_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_sup_posti_per_m2(self):
        self.assertEqual(mh862_sup(300, 25), 7500.0)
        with self.assertRaises(ValueError):
            mh862_sup(0, 25)
        with self.assertRaises(ValueError):
            mh862_sup(300, 0)

    def test_luce_vent_base_e_domanda_base(self):
        self.assertEqual(mh862_e_light_base(7500, 8, 6000), 360000.0)
        self.assertEqual(mh862_e_vent_base(7500, 6, 6000), 270000.0)
        self.assertEqual(mh862_e_domanda_base(360000.0, 270000.0),
                         630000.0)
        self.assertAlmostEqual(mh862_c_base(630000.0, 0.28), 176400.0)

    def test_led_vent_co_ev_driver_esplicito(self):
        self.assertEqual(mh862_e_led(7500, 3, 6000), 135000.0)
        self.assertEqual(mh862_e_vent_alt(270000.0, 0.45), 121500.0)
        # Le colonnine sono un driver esplicito, non il 10% dei posti.
        self.assertEqual(mh862_e_ev(20, 2000), 40000.0)
        self.assertNotEqual(mh862_e_ev(20, 2000), 300 * 0.10 * 2000)
        self.assertEqual(mh862_e_domanda_alt(135000.0, 121500.0, 40000.0),
                         296500.0)
        with self.assertRaises(ValueError):
            mh862_e_vent_alt(270000.0, 1.1)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh862_kwp(7500, 0.40, 0.20), 600.0)
        self.assertEqual(mh862_e_pv(600.0, 1100), 660000.0)
        self.assertEqual(mh862_e_pv_auto(660000.0, 0.60, 296500.0),
                         296500.0)
        # Cap alla domanda: autoconsumo non supera la domanda.
        self.assertEqual(mh862_e_pv_auto(660000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh862_e_immessa(660000.0, 296500.0), 363500.0)
        self.assertEqual(mh862_e_deficit(296500.0, 296500.0), 0.0)
        self.assertEqual(mh862_e_deficit(20000.0, 25000.0), 0.0)

    def test_c_alt_con_ricavi_ev_e_immissione(self):
        self.assertEqual(mh862_ricavo_ev(40000.0, 0.45), 18000.0)
        self.assertEqual(mh862_ricavo_immissione(363500.0, 0.08),
                         29080.0)
        self.assertAlmostEqual(mh862_c_alt(0.0, 0.28, 29080.0, 18000.0),
                               -47080.0)
        self.assertAlmostEqual(mh862_risparmio(176400.0, -47080.0),
                               223480.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh862_capex_totale(7500, 8, 45000, 600.0, 1100,
                                            20, 2500),
                         815000.0)
        self.assertEqual(mh862_capex_totale(7500, 8, 45000, 0.0, 1100,
                                            20, 2500),
                         155000.0)

    def test_co2_con_divisione_per_mille_senza_credito_immessa(self):
        cb = mh862_co2_base(630000.0, 0.25)
        self.assertAlmostEqual(cb, 157.5, places=4)
        ca = mh862_co2_alt(0.0, 0.25)
        self.assertEqual(ca, 0.0)
        self.assertAlmostEqual(mh862_co2_evitata(cb, ca), 157.5, places=4)
        # L'immessa non sottrae CO2: alt conta solo il deficit.
        self.assertEqual(mh862_co2_alt(0.0, 0.25), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh862_flussi(815000, 223480.0, 3),
                         [-815000, 223480.0, 223480.0, 223480.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh862_van([-100, 60, 60], 0), 20.0)
        bc = mh862_demo_calcoli()
        self.assertAlmostEqual(mh862_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh862_demo_calcoli()
        tir = mh862_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh862_tir([-100, -10, -10]))
        self.assertIsNone(mh862_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh862_demo_calcoli()
        self.assertEqual(mh862_payback(bc["flussi"]), 4)
        self.assertIsNone(mh862_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh862_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh862_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:4]), -144560.0, places=2)
        self.assertAlmostEqual(sum(flussi[:5]), 78920.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh862_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh862_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh862_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh862_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh862_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh862_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh862_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none_rapporto_negativo(self):
        bc = mh862_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a elettricita' gratuita, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((-bc["e_immessa_kwh_anno"] * bc["p_immissione"]
                         - bc["e_ev_kwh_anno"] * bc["p_ev_eur_kwh"])
                        / (bc["e_domanda_base_kwh_anno"]
                           - bc["e_deficit_kwh_anno"]), 0.0)
        self.assertAlmostEqual(
            (-bc["e_immessa_kwh_anno"] * bc["p_immissione"]
             - bc["e_ev_kwh_anno"] * bc["p_ev_eur_kwh"])
            / (bc["e_domanda_base_kwh_anno"]
               - bc["e_deficit_kwh_anno"]), -0.07473015873015873,
            places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_el_pareggio_ricavi_nulli_zero(self):
        # Senza ricavi (immessa ed EV nulli) il numeratore e' nullo:
        # pareggio a prezzo zero, non None.
        self.assertEqual(mh862_p_el_pareggio(0.0, 0.08, 0.0, 0.45,
                                            630000.0, 296500.0), 0.0)

    def test_p_el_pareggio_denominatore_nullo_none(self):
        self.assertIsNone(mh862_p_el_pareggio(100.0, 0.08, 0.0, 0.45,
                                             500000.0, 500000.0))

    def test_p_el_pareggio_negativo_none(self):
        self.assertIsNone(mh862_p_el_pareggio(363500.0, 0.08, 40000.0,
                                             0.45, 630000.0, 0.0))

    def test_valida_demo_ok(self):
        demo = mh862_demo()
        val = mh862_valida(*[demo[k] for k in (
            "n_posti", "m2_per_posto", "ore_apertura", "w_light_base",
            "w_vent_base", "w_led", "f_vent_co", "n_colonnine",
            "kwh_ev_colonnina", "p_ev_eur_kwh", "p_el", "quota_fv",
            "kwp_per_m2", "resa_fv", "f_autoconsumo", "p_immissione",
            "capex_led_m2", "capex_vent_co", "capex_fv_eur_kwp",
            "capex_colonnina", "f_co2_el_kg_kwh", "wacc_pct",
            "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_posti_e_m2_zero_no(self):
        kw = _demo_kwargs(n_posti=0)
        self.assertRaises(ValueError, mh862_calcola, **kw)
        kw = _demo_kwargs(m2_per_posto=0)
        self.assertRaises(ValueError, mh862_calcola, **kw)

    def test_valida_quote_sopra_uno_no(self):
        kw = _demo_kwargs(f_vent_co=1.1)
        self.assertRaises(ValueError, mh862_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh862_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh862_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh862_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh862_calcola, **kw)

    def test_valida_colonnine_non_intere_no(self):
        kw = _demo_kwargs(n_colonnine=2.5)
        self.assertRaises(ValueError, mh862_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh862_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("ore_apertura", -1),
                              ("w_light_base", -1),
                              ("p_el", -0.01),
                              ("capex_vent_co", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh862_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh862_calcola(mh862_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh862_calcola(dict(mh862_demo(), capex_vent_co=999999),
                           capex_vent_co=45000)
        self.assertEqual(bc["capex_eur"], 815000.0)


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
        self.assertEqual(bc["payback"], 4)

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
            bc["e_domanda_base_kwh_anno"] * bc["p_el"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["e_immessa_kwh_anno"] * bc["p_immissione"]
            - bc["e_ev_kwh_anno"] * bc["p_ev_eur_kwh"])

    def test_coerenza_p_el_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertLess((-bc["e_immessa_kwh_anno"] * bc["p_immissione"]
                         - bc["e_ev_kwh_anno"] * bc["p_ev_eur_kwh"])
                        / (bc["e_domanda_base_kwh_anno"]
                           - bc["e_deficit_kwh_anno"]), 0.0)

    def test_sensibilita_valori(self):
        s = mh862_sensibilita(**mh862_demo())
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               258760.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               2409721.55, places=2)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               111380.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               1233040.99, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 155000.0)
        self.assertAlmostEqual(s["vent_sempre_accesa"]["risparmio_eur_anno"],
                               201800.0, places=2)
        self.assertAlmostEqual(s["vent_sempre_accesa"]["van"],
                               1699874.05, places=2)
        self.assertEqual(s["vent_sempre_accesa"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               1155054.77, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 8)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               910653.32, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               3654600.0, places=2)

    def test_marginale_con_capex_fv_alto(self):
        # CAPEX totale 2.855.000 (FV a 4.500 EUR/kWp):
        # VAN circa -69.945, entro la tolleranza del 10%
        # (285.500).
        bc = mh862_calcola(**_demo_kwargs(capex_fv_eur_kwp=4500))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -69945.23, places=2)

    def test_non_convente_con_capex_fv_altissimo(self):
        bc = mh862_calcola(**_demo_kwargs(capex_fv_eur_kwp=5000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -369945.23, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh862_calcola(**_demo_kwargs(quota_fv=0, w_led=8,
                                          f_vent_co=1.0,
                                          p_ev_eur_kwh=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -11200.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh862_csv(bc, mh862_demo())
        for voce in ("n_posti", "e_light_base_kwh_anno",
                     "e_domanda_base_kwh_anno", "p_el_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -815000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie (m2)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_sup_scala_lineare_con_posti(self):
        self.assertAlmostEqual(mh862_sup(600, 25.0),
                               2.0 * mh862_sup(300, 25.0))

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh862_c_alt(296500.0, 0.28, 0.0, 18000.0)
        con = mh862_c_alt(0.0, 0.28, 29080.0, 18000.0)
        self.assertAlmostEqual(senza - con, 296500.0 * 0.28 + 29080.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh862_sensibilita(**mh862_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_piu20", "senza_fv",
                          "vent_sempre_accesa", "capex_doppio",
                          "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh862_csv(bc, mh862_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_light_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh862_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh862_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh862_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["capex_eur"], 155000.0)
        bc = mh862_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def862\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh862_demo().keys()), lette - set(mh862_demo().keys()))
        self.assertEqual(lette, set(mh862_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc862\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc862\["([^"]+)"\]', src))
        attese = set(mh862_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab862:"), 1)
        self.assertTrue(src.startswith("    # W866"))

    def test_ui_tab862_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab862:"), 1)
        self.assertIn("def mh862_demo(", src_h)
        self.assertIn("def mh862_calcola(", src_h)
        self.assertIn("tab862", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Parcheggio coperto: LED + ventilazione a controllo CO + FV su pensiline/copertura + ricarica EV battono illuminazione tradizionale + ventilazione sempre accesa?", src)
        self.assertIn("🅿️ Parcheggio coperto: LED + ventilazione a controllo CO + FV su pensiline/copertura + ricarica EV battono illuminazione tradizionale + ventilazione sempre accesa?", src)
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
        chiavi = re.findall(r'key="(st862_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st862_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st862_calcola"', src)
        self.assertIn('key="st862_csv"', src)
        self.assertIn('key="st862_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg862"), src.index(".paiac("))
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
