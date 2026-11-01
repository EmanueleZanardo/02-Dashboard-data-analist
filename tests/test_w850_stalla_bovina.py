"""Test nuova scheda stalla bovina da latte:
raffreddamento latte + recupero calore + pompa di
calore battono caldaia a gas + tank frigo
tradizionale?

Business case annuo di una stalla bovina da latte,
connessa alla rete, guidata dalle VACCHE IN
LATTAZIONE + LITRI DI LATTE AL GIORNO +
SUPERFICIE STALLA (non pizzeria, non caseificio
generico, non allevamento da carne):
litri_anno = litri_latte_giorno x giorni_anno;
Q_raffr = litri_anno x 1,03 x 3,93 x 31 / 3600
(31 K = 35 C - 4 C, calore specifico latte 3,93
kJ/kgK, densita' 1,03 kg/L); Q_acs = vacche x
litri_acs_per_vacca_giorno x giorni_anno x 4,186
x dT / 3600; Q_risc = superficie_stalla_m2 x
q_risc; Q_termico = Q_risc + Q_acs;
E_tank_base = Q_raffr / COP_tank_base;
E_tank_alt = Q_raffr / COP_tank_alt;
Q_cond_alt = Q_raffr + E_tank_alt (primo
principio); Q_rec = min(Q_termico, Q_cond_alt x
f_rec x f_uso) (satura sulla domanda, solo la
frazione utilizzabile coincide con la domanda);
Q_net = max(0, Q_termico - Q_rec);
Gas_base = Q_termico / eta_caldaia;
Gas_alt = 0 (la caldaia a gas SCOMPARE:
il termico netto va in pompa di calore);
E_pdc_risc = Q_net / COP_pdc;
E_vent_base = superficie_stalla_m2 x
e_vent_per_m2; E_vent_alt = E_vent_base x
(1 - risparmio_vent); E_illum_base =
superficie_stalla_m2 x e_illum_per_m2;
E_illum_alt = E_illum_base x (1 - risparmio_led);
E_base_el = E_tank_base + E_vent_base +
E_illum_base; E_alt_el = E_tank_alt + E_pdc_risc
+ E_vent_alt + E_illum_alt; kWp copertura =
superficie_copertura_m2 x quota_copertura x
0,18 kWp/m2; E_pv = kWp x producibilita';
E_pv_auto = min(E_pv x f_autoconsumo, E_alt_el)
(cappato alla domanda elettrica alternativa);
E_immessa = E_pv - E_pv_auto; E_deficit =
max(0, E_alt_el - E_pv_auto); C_base =
E_base_el x p_el + Gas_base x p_gas + OM_base;
C_alt = E_deficit x p_el - E_immessa x
p_immissione + OM_alt (gas alternativo zero;
l'immessa e' un RICAVO a prezzo di immissione,
INFERIORE a p_el; nessun credito CO2 per
l'immessa); risparmio = C_base - C_alt;
CAPEX forfettario; CO2 base = E_base_el x f_el
+ Gas_base x f_gas; CO2 alt = E_deficit x f_el
(gas alternativo zero, nessun credito CO2 per
l'immessa); CO2 evitata = base - alt (segno
libero); flussi [-CAPEX, risparmio x vita];
VAN al WACC (PERCENTUALE in ingresso,
/ 100 dentro); TIR per bisezione; payback
(primo anno con cumulato >= 0); prezzo
elettrico di pareggio p_star = (OM_alt -
OM_base - Gas_base x p_gas - E_immessa x
p_immissione) / (E_base_el - E_deficit) in
forma chiusa a prezzo gas, prezzo immissione
e O&M FERMI, None se E_base_el - E_deficit
<= 0 o se p_star < 0, SOGLIA MINIMA sui soli
costi annui quando esiste (sopra di essa
l'alternativa vince, sotto perde; il CAPEX
non entra nel pareggio annuo).
Nel demo p_star e' None, documentato: il
numeratore e' negativo (-9.405,73 EUR/anno),
quindi l'alternativa vince sui costi annui
anche a prezzo elettrico nullo. Un caso
costruito con pareggio positivo (niente
termico: q_risc 0 e litri ACS per vacca 0,
niente fotovoltaico: quota copertura 0, COP
tank base 2,0, COP tank alt 4,0, risparmio
ventilazione 0,80, risparmio LED 0,80, O&M alt
20.000) ha p_star 0,21957714259310135
EUR/kWh: a p_star il risparmio e' zero e il
verdetto e' NON_CALCOLABILE, a p_star + 0,01
il risparmio e' 546,50 EUR/anno, a p_star
- 0,01 e' -546,50 EUR/anno.
Verdetto: NON_CALCOLABILE se input degenere
(vacche <= 0, litri al giorno <= 0, giorni < 0,
litri ACS per vacca < 0, dT < 0, stalla <= 0,
q_risc < 0, copertura < 0, quota copertura < 0
o > 1, COP tank base <= 0, COP tank alt <= 0,
COP pdc <= 0, f_rec o f_uso < 0 o > 1,
ventilazione per m2 < 0, risparmio ventilazione
< 0 o > 1, illuminazione per m2 < 0, risparmio
LED < 0 o > 1, producibilita' < 0,
f_autoconsumo < 0 o > 1, eta caldaia <= 0 o
> 1, prezzi < 0, O&M < 0, CAPEX < 0, f_el < 0,
f_gas < 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e
CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza
PERCENTUALE del CAPEX, NON_CONVIENTE
altrimenti.
"""

import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w854_helpers import (
        demo_calcoli,
        mh850_c_alt,
        mh850_c_base,
        mh850_calcola,
        mh850_co2_alt,
        mh850_co2_base,
        mh850_co2_evitata,
        mh850_csv,
        mh850_demo,
        mh850_demo_calcoli,
        mh850_e_alt_el,
        mh850_e_base_el,
        mh850_e_deficit,
        mh850_e_illum_alt,
        mh850_e_illum_base,
        mh850_e_immessa,
        mh850_e_pdc_risc,
        mh850_e_pv,
        mh850_e_pv_auto,
        mh850_e_tank_alt,
        mh850_e_tank_base,
        mh850_e_vent_alt,
        mh850_e_vent_base,
        mh850_eta,
        mh850_flussi,
        mh850_frazione,
        mh850_gas_alt,
        mh850_gas_base,
        mh850_int_pos,
        mh850_litri_anno,
        mh850_nneg,
        mh850_num,
        mh850_p_el_pareggio,
        mh850_p_pv_kwp,
        mh850_payback,
        mh850_pos,
        mh850_q_acs,
        mh850_q_cond_alt,
        mh850_q_net,
        mh850_q_raffr,
        mh850_q_rec,
        mh850_q_risc,
        mh850_q_termico,
        mh850_risparmio,
        mh850_sensibilita,
        mh850_tir,
        mh850_valida,
        mh850_van,
        mh850_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w854_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w854_helpers", os.path.join(_hf, "w854_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh850_c_alt = _mod.mh850_c_alt
    mh850_c_base = _mod.mh850_c_base
    mh850_calcola = _mod.mh850_calcola
    mh850_co2_alt = _mod.mh850_co2_alt
    mh850_co2_base = _mod.mh850_co2_base
    mh850_co2_evitata = _mod.mh850_co2_evitata
    mh850_csv = _mod.mh850_csv
    mh850_demo = _mod.mh850_demo
    mh850_demo_calcoli = _mod.mh850_demo_calcoli
    mh850_e_alt_el = _mod.mh850_e_alt_el
    mh850_e_base_el = _mod.mh850_e_base_el
    mh850_e_deficit = _mod.mh850_e_deficit
    mh850_e_illum_alt = _mod.mh850_e_illum_alt
    mh850_e_illum_base = _mod.mh850_e_illum_base
    mh850_e_immessa = _mod.mh850_e_immessa
    mh850_e_pdc_risc = _mod.mh850_e_pdc_risc
    mh850_e_pv = _mod.mh850_e_pv
    mh850_e_pv_auto = _mod.mh850_e_pv_auto
    mh850_e_tank_alt = _mod.mh850_e_tank_alt
    mh850_e_tank_base = _mod.mh850_e_tank_base
    mh850_e_vent_alt = _mod.mh850_e_vent_alt
    mh850_e_vent_base = _mod.mh850_e_vent_base
    mh850_eta = _mod.mh850_eta
    mh850_flussi = _mod.mh850_flussi
    mh850_frazione = _mod.mh850_frazione
    mh850_gas_alt = _mod.mh850_gas_alt
    mh850_gas_base = _mod.mh850_gas_base
    mh850_int_pos = _mod.mh850_int_pos
    mh850_litri_anno = _mod.mh850_litri_anno
    mh850_nneg = _mod.mh850_nneg
    mh850_num = _mod.mh850_num
    mh850_p_el_pareggio = _mod.mh850_p_el_pareggio
    mh850_p_pv_kwp = _mod.mh850_p_pv_kwp
    mh850_payback = _mod.mh850_payback
    mh850_pos = _mod.mh850_pos
    mh850_q_acs = _mod.mh850_q_acs
    mh850_q_cond_alt = _mod.mh850_q_cond_alt
    mh850_q_net = _mod.mh850_q_net
    mh850_q_raffr = _mod.mh850_q_raffr
    mh850_q_rec = _mod.mh850_q_rec
    mh850_q_risc = _mod.mh850_q_risc
    mh850_q_termico = _mod.mh850_q_termico
    mh850_risparmio = _mod.mh850_risparmio
    mh850_sensibilita = _mod.mh850_sensibilita
    mh850_tir = _mod.mh850_tir
    mh850_valida = _mod.mh850_valida
    mh850_van = _mod.mh850_van
    mh850_verdetto = _mod.mh850_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w854_helpers.py")
_UI_PATH = _risolvi("w854_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "9"
_VECCHIO_TAB = "tab84" + "9"
_VECCHIO_ST = "st84" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "litri_anno": 1314000.0,
    "q_raffr_kwh_c_anno": 45801.98850000001,
    "q_acs_kwh_th_anno": 38197.25,
    "q_risc_kwh_th_anno": 72000.0,
    "q_termico_kwh_th_anno": 110197.25,
    "e_tank_base_kwh_e_anno": 20819.085681818182,
    "e_tank_alt_kwh_e_anno": 13471.173088235297,
    "q_cond_alt_kwh_c_anno": 59273.16158823531,
    "q_rec_kwh_th_anno": 24894.727867058828,
    "q_net_kwh_th_anno": 85302.52213294117,
    "gas_base_kwh_anno": 122441.38888888889,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_risc_kwh_e_anno": 22448.032140247677,
    "e_vent_base_kwh_e_anno": 30000.0,
    "e_vent_alt_kwh_e_anno": 22500.0,
    "e_illum_base_kwh_e_anno": 24000.0,
    "e_illum_alt_kwh_e_anno": 14400.0,
    "e_base_el_kwh_e_anno": 74819.08568181818,
    "e_alt_el_kwh_e_anno": 72819.20522848297,
    "p_pv_kwp": 72.0,
    "e_pv_kwh_e_anno": 79200.0,
    "e_pv_auto_kwh_e_anno": 51480.0,
    "e_immessa_kwh_e_anno": 27720.0,
    "e_deficit_kwh_e_anno": 21339.20522848297,
    "c_base_eur_anno": 35479.92385,
    "c_alt_eur_anno": 14308.625150266253,
    "risparmio_eur_anno": 21171.298699733747,
    "capex_eur": 180000.0,
    "co2_base_t_anno": 50.67495776641414,
    "co2_alt_t_anno": 7.46872182996904,
    "co2_evitata_t_anno": 43.2062359364451,
    "van": 39750.840727413655,
    "tir": 8.110406962930309,
    "payback": 9,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh850_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh850_num(3, "x"), 3.0)
        self.assertEqual(mh850_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh850_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh850_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh850_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh850_pos(0, "x")
        with self.assertRaises(ValueError):
            mh850_pos(-1, "x")
        self.assertEqual(mh850_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh850_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh850_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh850_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh850_int_pos(15, "x"), 15)
        self.assertEqual(mh850_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh850_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh850_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh850_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh850_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh850_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh850_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_litri_anno(self):
        self.assertEqual(mh850_litri_anno(3600, 365), 1314000.0)
        with self.assertRaises(ValueError):
            mh850_litri_anno(0, 365)

    def test_q_raffr(self):
        self.assertAlmostEqual(mh850_q_raffr(1314000.0), 45801.9885, places=2)
        self.assertEqual(mh850_q_raffr(0), 0.0)
        # Formula diretta: 1,03 x 3,93 x 31 / 3600 per litro.
        self.assertAlmostEqual(mh850_q_raffr(3600.0),
                               3600.0 * 1.03 * 3.93 * 31.0 / 3600.0)

    def test_q_acs(self):
        self.assertAlmostEqual(
            mh850_q_acs(120, 15, 365, 50), 38197.25, places=2)
        self.assertEqual(mh850_q_acs(120, 0, 365, 50), 0.0)

    def test_q_risc_e_termico(self):
        self.assertEqual(mh850_q_risc(1200, 60), 72000.0)
        self.assertEqual(mh850_q_termico(72000.0, 38197.25), 110197.25)

    def test_e_tank_base_e_alt(self):
        self.assertAlmostEqual(mh850_e_tank_base(45801.9885, 2.2),
                               20819.0857, places=2)
        self.assertAlmostEqual(mh850_e_tank_alt(45801.9885, 3.4),
                               13471.1731, places=2)
        with self.assertRaises(ValueError):
            mh850_e_tank_base(100.0, 0.0)

    def test_q_cond_primo_principio(self):
        self.assertAlmostEqual(mh850_q_cond_alt(45801.9885, 13471.1731),
                               59273.1616, places=2)

    def test_q_rec_satura_sulla_domanda(self):
        self.assertEqual(mh850_q_rec(100.0, 1000.0, 0.7, 0.6), 100.0)

    def test_q_rec_sotto_domanda(self):
        self.assertAlmostEqual(mh850_q_rec(110197.25, 59273.1616, 0.7, 0.6),
                               24894.7279, places=2)

    def test_q_net(self):
        self.assertAlmostEqual(mh850_q_net(110197.25, 24894.7279),
                               85302.5221, places=2)
        self.assertEqual(mh850_q_net(100.0, 100.0), 0.0)

    def test_gas_base_e_alt_zero(self):
        self.assertAlmostEqual(mh850_gas_base(110197.25, 0.9),
                               122441.3889, places=2)
        self.assertEqual(mh850_gas_alt(), 0.0)

    def test_e_pdc_risc(self):
        self.assertAlmostEqual(mh850_e_pdc_risc(85302.5221, 3.8),
                               22448.0321, places=2)
        with self.assertRaises(ValueError):
            mh850_e_pdc_risc(100.0, 0.0)

    def test_vent_base_e_alt(self):
        self.assertEqual(mh850_e_vent_base(1200, 25), 30000.0)
        self.assertEqual(mh850_e_vent_alt(30000.0, 0.25), 22500.0)
        self.assertEqual(mh850_e_vent_alt(30000.0, 0.0), 30000.0)

    def test_illum_base_e_alt(self):
        self.assertEqual(mh850_e_illum_base(1200, 20), 24000.0)
        self.assertEqual(mh850_e_illum_alt(24000.0, 0.40), 14400.0)

    def test_e_base_e_alt(self):
        self.assertAlmostEqual(
            mh850_e_base_el(20819.0857, 30000.0, 24000.0),
            74819.0857, places=2)
        self.assertAlmostEqual(
            mh850_e_alt_el(13471.1731, 22448.0321, 22500.0, 14400.0),
            72819.2052, places=2)

    def test_p_pv_ed_e_pv(self):
        self.assertEqual(mh850_p_pv_kwp(1000, 0.40), 72.0)
        self.assertEqual(mh850_e_pv(72.0, 1100), 79200.0)
        self.assertEqual(mh850_p_pv_kwp(1000, 0.0), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh850_e_pv_auto(79200.0, 0.65, 72819.2052),
                         51480.0)
        self.assertEqual(mh850_e_pv_auto(200000.0, 0.65, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh850_e_immessa(79200.0, 51480.0), 27720.0)
        self.assertAlmostEqual(mh850_e_deficit(72819.2052, 51480.0),
                               21339.2052, places=2)
        self.assertEqual(mh850_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh850_c_base(74819.0857, 0.22, 122441.3889, 0.09, 8000)
        self.assertAlmostEqual(cb, 35479.9239, places=2)
        ca = mh850_c_alt(21339.2052, 0.22, 27720.0, 0.05, 11000)
        self.assertAlmostEqual(ca, 14308.6252, places=2)
        self.assertAlmostEqual(mh850_risparmio(cb, ca), 21171.2987, places=2)

    def test_co2(self):
        cb = mh850_co2_base(74819.0857, 0.00035, 122441.3889, 0.00020)
        self.assertAlmostEqual(cb, 50.6750, places=2)
        ca = mh850_co2_alt(21339.2052, 0.00035)
        self.assertAlmostEqual(ca, 7.4687, places=2)
        self.assertAlmostEqual(mh850_co2_evitata(cb, ca), 43.2062, places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh850_flussi(180000, 21171.2987, 3),
                         [-180000, 21171.2987, 21171.2987, 21171.2987])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh850_van([-100, 60, 60], 0), 20.0)
        bc = mh850_demo_calcoli()
        self.assertAlmostEqual(mh850_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh850_demo_calcoli()
        tir = mh850_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh850_tir([-100, -10, -10]))
        self.assertIsNone(mh850_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh850_demo_calcoli()
        self.assertEqual(mh850_payback(bc["flussi"]), 9)
        self.assertIsNone(mh850_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh850_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh850_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh850_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh850_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh850_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh850_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh850_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh850_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none(self):
        bc = mh850_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh850_p_el_pareggio(
            8000, 11000, bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.05,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]))

    def test_p_el_pareggio_denominatore_non_positivo(self):
        self.assertIsNone(mh850_p_el_pareggio(
            8000, 11000, 1000.0, 0.09, 0.0, 0.05, 100.0, 100.0))
        self.assertIsNone(mh850_p_el_pareggio(
            8000, 11000, 1000.0, 0.09, 0.0, 0.05, 100.0, 150.0))

    def test_p_el_pareggio_positivo_e_soglia(self):
        kw = _demo_kwargs(q_risc=0, litri_acs_per_vacca_giorno=0,
                          quota_copertura=0, cop_tank_base=2.0,
                          cop_tank_alt=4.0, risparmio_vent=0.80,
                          risparmio_led=0.80, om_alt=20000)
        caso = mh850_calcola(**kw)
        p_star = caso["p_el_pareggio"]
        self.assertIsNotNone(p_star)
        self.assertAlmostEqual(p_star, 0.21957714259310135, places=12)
        esatto = mh850_calcola(**dict(kw, p_el=p_star))
        self.assertAlmostEqual(esatto["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(esatto["verdetto"], "NON_CALCOLABILE")
        sopra = mh850_calcola(**dict(kw, p_el=p_star + 0.01))
        self.assertAlmostEqual(sopra["risparmio_eur_anno"], 546.50497125,
                               places=4)
        sotto = mh850_calcola(**dict(kw, p_el=p_star - 0.01))
        self.assertAlmostEqual(sotto["risparmio_eur_anno"], -546.50497125,
                               places=4)
        self.assertEqual(sotto["verdetto"], "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh850_demo()
        val = mh850_valida(*[demo[k] for k in (
            "vacche_lattazione", "litri_latte_giorno", "giorni_anno",
            "litri_acs_per_vacca_giorno", "acs_dt",
            "superficie_stalla_m2", "q_risc",
            "superficie_copertura_m2", "quota_copertura",
            "cop_tank_base", "cop_tank_alt", "cop_pdc",
            "f_rec", "f_uso", "e_vent_per_m2", "risparmio_vent",
            "e_illum_per_m2", "risparmio_led", "prod_specifica",
            "f_autoconsumo", "eta_caldaia", "p_el", "p_gas",
            "p_immissione", "om_base", "om_alt", "capex",
            "f_el", "f_gas", "wacc", "vita", "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vacche_zero_no(self):
        self.assertFalse(mh850_valida(
            *([0] + [mh850_demo()[k] for k in (
                "litri_latte_giorno", "giorni_anno",
                "litri_acs_per_vacca_giorno", "acs_dt",
                "superficie_stalla_m2", "q_risc",
                "superficie_copertura_m2", "quota_copertura",
                "cop_tank_base", "cop_tank_alt", "cop_pdc",
                "f_rec", "f_uso", "e_vent_per_m2", "risparmio_vent",
                "e_illum_per_m2", "risparmio_led", "prod_specifica",
                "f_autoconsumo", "eta_caldaia", "p_el", "p_gas",
                "p_immissione", "om_base", "om_alt", "capex",
                "f_el", "f_gas", "wacc", "vita", "tolleranza")]))["valido"])

    def test_valida_litri_zero_no(self):
        kw = _demo_kwargs(litri_latte_giorno=0)
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_stalla_zero_no(self):
        kw = _demo_kwargs(superficie_stalla_m2=0)
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_tank_base=0)
        self.assertRaises(ValueError, mh850_calcola, **kw)
        kw = _demo_kwargs(cop_pdc=0)
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_rec=1.1)
        self.assertRaises(ValueError, mh850_calcola, **kw)
        kw = _demo_kwargs(quota_copertura=1.1)
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh850_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh850_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("giorni_anno", -1),
                              ("acs_dt", -1),
                              ("q_risc", -1),
                              ("p_gas", -0.01),
                              ("capex", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh850_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh850_calcola(mh850_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh850_calcola(dict(mh850_demo(), capex=999999), capex=180000)
        self.assertEqual(bc["capex_eur"], 180000.0)


class TestCalcolaDemo(unittest.TestCase):
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

    def test_coerenza_bilancio_fv(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["e_pv_kwh_e_anno"],
            bc["e_pv_auto_kwh_e_anno"] + bc["e_immessa_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_pv_auto_kwh_e_anno"] + bc["e_deficit_kwh_e_anno"])

    def test_coerenza_bilancio_termico_ed_elettrico(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["q_termico_kwh_th_anno"],
            bc["q_rec_kwh_th_anno"] + bc["q_net_kwh_th_anno"])
        self.assertAlmostEqual(
            bc["e_base_el_kwh_e_anno"],
            bc["e_tank_base_kwh_e_anno"]
            + bc["e_vent_base_kwh_e_anno"]
            + bc["e_illum_base_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_tank_alt_kwh_e_anno"]
            + bc["e_pdc_risc_kwh_e_anno"]
            + bc["e_vent_alt_kwh_e_anno"]
            + bc["e_illum_alt_kwh_e_anno"])
        self.assertLessEqual(bc["q_rec_kwh_th_anno"],
                             bc["q_termico_kwh_th_anno"])

    def test_coerenza_risparmio_e_co2(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertEqual(bc["gas_alt_kwh_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh850_sensibilita(**mh850_demo())
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               18818.18, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               23524.41, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], -92191.22, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               19730.02, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], -140249.16, places=2)
        self.assertAlmostEqual(s["vita_10"]["van"], -16520.84, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 137569.48, places=2)

    def test_marginale_con_capex_220k(self):
        bc = mh850_calcola(**_demo_kwargs(capex=220000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -249.16, places=2)
        self.assertEqual(bc["payback"], 11)

    def test_non_convente_con_capex_250k(self):
        bc = mh850_calcola(**_demo_kwargs(capex=250000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh850_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0, om_alt=999999))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh850_csv(bc, mh850_demo())
        for voce in ("vacche_lattazione", "litri_anno",
                     "q_raffr_kwh_c_anno", "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -180000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, caldaia a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Calore da asportare raffreddamento latte (kWh_c/anno)",
                      voci)

    def test_recupero_zero_con_f_rec_zero_o_f_uso_zero(self):
        self.assertEqual(mh850_q_rec(1000.0, 5000.0, 0.0, 0.6), 0.0)
        self.assertEqual(mh850_q_rec(1000.0, 5000.0, 0.7, 0.0), 0.0)

    def test_q_raffr_scala_lineare_con_litri(self):
        self.assertAlmostEqual(mh850_q_raffr(2000.0),
                               2.0 * mh850_q_raffr(1000.0))

    def test_co2_alt_senza_credito_immessa(self):
        # L'energia immessa non sottrae CO2: a parita' di
        # deficit, la CO2 alternativa non cambia.
        self.assertEqual(mh850_co2_alt(20000.0, 0.00035),
                         20000.0 * 0.00035)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh850_c_alt(20000.0, 0.22, 0.0, 0.05, 11000)
        con = mh850_c_alt(20000.0, 0.22, 10000.0, 0.05, 11000)
        self.assertAlmostEqual(senza - con, 500.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh850_sensibilita(**mh850_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh850_csv(bc, mh850_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("q_raffr_kwh_c_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh850_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh850_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh850_calcola(**_demo_kwargs(giorni_anno=0))
        self.assertEqual(bc["litri_anno"], 0.0)
        bc = mh850_calcola(**_demo_kwargs(quota_copertura=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab850:"), 1)
        self.assertTrue(src.startswith("    # W854"))

    def test_ui_tab850_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab850:"), 1)
        self.assertIn("def mh850_demo(", src_h)
        self.assertIn("def mh850_calcola(", src_h)
        self.assertIn("tab850", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Stalla bovina da latte: raffreddamento latte + recupero calore + pompa di calore battono caldaia a gas + tank frigo tradizionale?", src)
        self.assertIn("🐄 Stalla bovina da latte: raffreddamento latte + recupero calore + pompa di calore battono caldaia a gas + tank frigo tradizionale?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
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
        chiavi = re.findall(r'key="(st850_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st850_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st850_calcola"', src)
        self.assertIn('key="st850_csv"', src)
        self.assertIn('key="st850_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def850\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh850_demo().keys()), lette - set(mh850_demo().keys()))
        self.assertEqual(lette, set(mh850_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc850\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc850\["([^"]+)"\]', src))
        attese = set(mh850_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg850"), src.index(".paiac("))
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
            self.assertNotIn("\u2014", src)
            self.assertNotIn("\u2013", src)


if __name__ == "__main__":
    unittest.main()
