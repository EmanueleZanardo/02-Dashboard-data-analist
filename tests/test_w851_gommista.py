"""Test nuova scheda gommista: compressore a
velocita' variabile + recupero calore
compressore + pompa di calore battono caldaia
a gas + compressore on/off tradizionale?

Business case annuo di un gommista, connesso
alla rete, guidato dagli PNEUMATICI MONTATI
ALL'ANNO + SUPERFICIE OFFICINA + SUPERFICIE
COPERTURA (non officina meccanica generica,
non autolavaggio, non centro revisioni):
E_comp_base = pneumatici_anno x
kwh_per_pneumatico_base; E_comp_alt =
pneumatici_anno x kwh_per_pneumatico_alt
(VSD, minore); Q_risc = superficie_officina_m2
x q_risc; Q_acs = addetti x litri_acs_giorno
x giorni_anno x 4,186 x dT / 3600;
Q_termico = Q_risc + Q_acs;
Q_disp_alt = E_comp_alt x f_calore_disp
(frazione elettrica che diventa calore, < 1);
Q_rec = min(Q_termico, Q_disp_alt x f_rec x
f_uso) (satura sulla domanda, solo la
frazione utilizzabile coincide con la
domanda); Q_net = max(0, Q_termico - Q_rec);
Gas_base = Q_termico / eta_caldaia;
Gas_alt = 0 (la caldaia a gas SCOMPARE:
il termico netto va in pompa di calore);
E_pdc = Q_net / COP_pdc;
E_illum_base = superficie_officina_m2 x
e_illum_per_m2; E_illum_alt = E_illum_base x
(1 - risparmio_led); E_altre =
superficie_officina_m2 x e_altre_per_m2
(uguale nei due casi); E_base_el =
E_comp_base + E_illum_base + E_altre;
E_alt_el = E_comp_alt + E_pdc + E_illum_alt
+ E_altre; kWp copertura =
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
numeratore e' negativo (-1.441,16 EUR/anno),
quindi l'alternativa vince sui costi annui
anche a prezzo elettrico nullo. Un caso
costruito con pareggio positivo (niente
termico: q_risc 0 e litri ACS al giorno 0,
niente fotovoltaico: quota copertura 0,
risparmio LED 0,80, O&M alt 20.000) ha
p_star 0,9210526315789473 EUR/kWh: a p_star
il risparmio e' zero e il verdetto e'
NON_CALCOLABILE, a p_star + 0,01 il
risparmio e' 152,00 EUR/anno, a p_star
- 0,01 e' -152,00 EUR/anno.
Verdetto: NON_CALCOLABILE se input degenere
(pneumatici <= 0, superficie officina <= 0,
addetti < 0, litri ACS al giorno < 0,
giorni < 0, dT < 0, q_risc < 0, superficie
copertura <= 0, quota copertura < 0 o > 1,
kwh per pneumatico base <= 0, kwh per
pneumatico alt <= 0, f_calore_disp < 0 o
> 1, f_rec o f_uso < 0 o > 1, cop_pdc <= 0,
eta caldaia <= 0 o > 1, illuminazione per
m2 < 0, risparmio LED < 0 o > 1, altre
utenze per m2 < 0, producibilita' < 0,
f_autoconsumo < 0 o > 1, prezzi < 0,
O&M < 0, CAPEX < 0, f_el < 0, f_gas < 0,
WACC < 0, vita <= 0 o non intera,
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
    from w855_helpers import (
        demo_calcoli,
        mh851_c_alt,
        mh851_c_base,
        mh851_calcola,
        mh851_co2_alt,
        mh851_co2_base,
        mh851_co2_evitata,
        mh851_csv,
        mh851_demo,
        mh851_demo_calcoli,
        mh851_e_alt_el,
        mh851_e_altre,
        mh851_e_base_el,
        mh851_e_comp_alt,
        mh851_e_comp_base,
        mh851_e_deficit,
        mh851_e_illum_alt,
        mh851_e_illum_base,
        mh851_e_immessa,
        mh851_e_pdc,
        mh851_e_pv,
        mh851_e_pv_auto,
        mh851_eta,
        mh851_flussi,
        mh851_frazione,
        mh851_gas_alt,
        mh851_gas_base,
        mh851_int_pos,
        mh851_nneg,
        mh851_num,
        mh851_p_el_pareggio,
        mh851_p_pv_kwp,
        mh851_payback,
        mh851_pos,
        mh851_q_acs,
        mh851_q_disp_alt,
        mh851_q_net,
        mh851_q_rec,
        mh851_q_risc,
        mh851_q_termico,
        mh851_risparmio,
        mh851_sensibilita,
        mh851_tir,
        mh851_valida,
        mh851_van,
        mh851_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w855_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w855_helpers", os.path.join(_hf, "w855_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh851_c_alt = _mod.mh851_c_alt
    mh851_c_base = _mod.mh851_c_base
    mh851_calcola = _mod.mh851_calcola
    mh851_co2_alt = _mod.mh851_co2_alt
    mh851_co2_base = _mod.mh851_co2_base
    mh851_co2_evitata = _mod.mh851_co2_evitata
    mh851_csv = _mod.mh851_csv
    mh851_demo = _mod.mh851_demo
    mh851_demo_calcoli = _mod.mh851_demo_calcoli
    mh851_e_alt_el = _mod.mh851_e_alt_el
    mh851_e_altre = _mod.mh851_e_altre
    mh851_e_base_el = _mod.mh851_e_base_el
    mh851_e_comp_alt = _mod.mh851_e_comp_alt
    mh851_e_comp_base = _mod.mh851_e_comp_base
    mh851_e_deficit = _mod.mh851_e_deficit
    mh851_e_illum_alt = _mod.mh851_e_illum_alt
    mh851_e_illum_base = _mod.mh851_e_illum_base
    mh851_e_immessa = _mod.mh851_e_immessa
    mh851_e_pdc = _mod.mh851_e_pdc
    mh851_e_pv = _mod.mh851_e_pv
    mh851_e_pv_auto = _mod.mh851_e_pv_auto
    mh851_eta = _mod.mh851_eta
    mh851_flussi = _mod.mh851_flussi
    mh851_frazione = _mod.mh851_frazione
    mh851_gas_alt = _mod.mh851_gas_alt
    mh851_gas_base = _mod.mh851_gas_base
    mh851_int_pos = _mod.mh851_int_pos
    mh851_nneg = _mod.mh851_nneg
    mh851_num = _mod.mh851_num
    mh851_p_el_pareggio = _mod.mh851_p_el_pareggio
    mh851_p_pv_kwp = _mod.mh851_p_pv_kwp
    mh851_payback = _mod.mh851_payback
    mh851_pos = _mod.mh851_pos
    mh851_q_acs = _mod.mh851_q_acs
    mh851_q_disp_alt = _mod.mh851_q_disp_alt
    mh851_q_net = _mod.mh851_q_net
    mh851_q_rec = _mod.mh851_q_rec
    mh851_q_risc = _mod.mh851_q_risc
    mh851_q_termico = _mod.mh851_q_termico
    mh851_risparmio = _mod.mh851_risparmio
    mh851_sensibilita = _mod.mh851_sensibilita
    mh851_tir = _mod.mh851_tir
    mh851_valida = _mod.mh851_valida
    mh851_van = _mod.mh851_van
    mh851_verdetto = _mod.mh851_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w855_helpers.py")
_UI_PATH = _risolvi("w855_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "0"
_VECCHIO_TAB = "tab85" + "0"
_VECCHIO_ST = "st85" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "e_comp_base_kwh_e_anno": 20000.0,
    "e_comp_alt_kwh_e_anno": 12800.0,
    "q_risc_kwh_th_anno": 32000.0,
    "q_acs_kwh_th_anno": 2511.6,
    "q_termico_kwh_th_anno": 34511.6,
    "q_disp_alt_kwh_th_anno": 10240.0,
    "q_rec_kwh_th_anno": 5734.400000000001,
    "q_net_kwh_th_anno": 28777.199999999997,
    "gas_base_kwh_anno": 38346.22222222222,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 8222.057142857142,
    "e_illum_base_kwh_e_anno": 10000.0,
    "e_illum_alt_kwh_e_anno": 5000.0,
    "e_altre_kwh_e_anno": 12000.0,
    "e_base_el_kwh_e_anno": 42000.0,
    "e_alt_el_kwh_e_anno": 38022.05714285714,
    "p_pv_kwp": 45.0,
    "e_pv_kwh_e_anno": 49500.0,
    "e_pv_auto_kwh_e_anno": 29700.0,
    "e_immessa_kwh_e_anno": 19800.0,
    "e_deficit_kwh_e_anno": 8322.057142857142,
    "c_base_eur_anno": 18691.16,
    "c_alt_eur_anno": 9840.852571428572,
    "risparmio_eur_anno": 8850.307428571428,
    "capex_eur": 80000.0,
    "co2_base_t_anno": 22.369244444444444,
    "co2_alt_t_anno": 2.9127199999999998,
    "co2_evitata_t_anno": 19.456524444444444,
    "van": 11863.164641340813,
    "tir": 7.120083553487739,
    "payback": 10,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh851_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh851_num(3, "x"), 3.0)
        self.assertEqual(mh851_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh851_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh851_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh851_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh851_pos(0, "x")
        with self.assertRaises(ValueError):
            mh851_pos(-1, "x")
        self.assertEqual(mh851_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh851_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh851_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh851_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh851_int_pos(15, "x"), 15)
        self.assertEqual(mh851_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh851_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh851_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh851_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh851_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh851_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh851_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_e_comp_base_e_alt(self):
        self.assertEqual(mh851_e_comp_base(8000, 2.5), 20000.0)
        self.assertEqual(mh851_e_comp_alt(8000, 1.6), 12800.0)
        with self.assertRaises(ValueError):
            mh851_e_comp_base(0, 2.5)
        with self.assertRaises(ValueError):
            mh851_e_comp_alt(8000, 0.0)

    def test_q_risc_e_termico(self):
        self.assertEqual(mh851_q_risc(400, 80), 32000.0)
        self.assertEqual(mh851_q_termico(32000.0, 2511.6), 34511.6)

    def test_q_acs(self):
        self.assertAlmostEqual(
            mh851_q_acs(6, 30, 300, 40), 2511.6, places=2)
        self.assertEqual(mh851_q_acs(6, 0, 300, 40), 0.0)

    def test_q_disp_alt(self):
        self.assertEqual(mh851_q_disp_alt(12800.0, 0.80), 10240.0)
        self.assertEqual(mh851_q_disp_alt(12800.0, 0.0), 0.0)

    def test_q_rec_satura_sulla_domanda(self):
        self.assertEqual(mh851_q_rec(100.0, 1000.0, 0.7, 0.8), 100.0)

    def test_q_rec_sotto_domanda(self):
        self.assertAlmostEqual(mh851_q_rec(34511.6, 10240.0, 0.7, 0.8),
                               5734.4, places=2)

    def test_q_net(self):
        self.assertAlmostEqual(mh851_q_net(34511.6, 5734.4),
                               28777.2, places=2)
        self.assertEqual(mh851_q_net(100.0, 100.0), 0.0)

    def test_gas_base_e_alt_zero(self):
        self.assertAlmostEqual(mh851_gas_base(34511.6, 0.9),
                               38346.2222, places=2)
        self.assertEqual(mh851_gas_alt(), 0.0)

    def test_e_pdc(self):
        self.assertAlmostEqual(mh851_e_pdc(28777.2, 3.5),
                               8222.0571, places=2)
        with self.assertRaises(ValueError):
            mh851_e_pdc(100.0, 0.0)

    def test_illum_base_e_alt(self):
        self.assertEqual(mh851_e_illum_base(400, 25), 10000.0)
        self.assertEqual(mh851_e_illum_alt(10000.0, 0.50), 5000.0)

    def test_altre_utenze(self):
        self.assertEqual(mh851_e_altre(400, 30), 12000.0)

    def test_e_base_e_alt(self):
        self.assertEqual(mh851_e_base_el(20000.0, 10000.0, 12000.0),
                         42000.0)
        self.assertAlmostEqual(
            mh851_e_alt_el(12800.0, 8222.0571, 5000.0, 12000.0),
            38022.0571, places=2)

    def test_p_pv_ed_e_pv(self):
        self.assertEqual(mh851_p_pv_kwp(500, 0.50), 45.0)
        self.assertEqual(mh851_e_pv(45.0, 1100), 49500.0)
        self.assertEqual(mh851_p_pv_kwp(500, 0.0), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh851_e_pv_auto(49500.0, 0.60, 38022.0571),
                         29700.0)
        self.assertEqual(mh851_e_pv_auto(200000.0, 0.60, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh851_e_immessa(49500.0, 29700.0), 19800.0)
        self.assertAlmostEqual(mh851_e_deficit(38022.0571, 29700.0),
                               8322.0571, places=2)
        self.assertEqual(mh851_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh851_c_base(42000.0, 0.22, 38346.2222, 0.09, 6000)
        self.assertAlmostEqual(cb, 18691.16, places=2)
        ca = mh851_c_alt(8322.0571, 0.22, 19800.0, 0.05, 9000)
        self.assertAlmostEqual(ca, 9840.8526, places=2)
        self.assertAlmostEqual(mh851_risparmio(cb, ca), 8850.3074, places=2)

    def test_co2(self):
        cb = mh851_co2_base(42000.0, 0.00035, 38346.2222, 0.00020)
        self.assertAlmostEqual(cb, 22.3692, places=2)
        ca = mh851_co2_alt(8322.0571, 0.00035)
        self.assertAlmostEqual(ca, 2.9127, places=2)
        self.assertAlmostEqual(mh851_co2_evitata(cb, ca), 19.4565, places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh851_flussi(80000, 8850.3074, 3),
                         [-80000, 8850.3074, 8850.3074, 8850.3074])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh851_van([-100, 60, 60], 0), 20.0)
        bc = mh851_demo_calcoli()
        self.assertAlmostEqual(mh851_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh851_demo_calcoli()
        tir = mh851_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh851_tir([-100, -10, -10]))
        self.assertIsNone(mh851_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh851_demo_calcoli()
        self.assertEqual(mh851_payback(bc["flussi"]), 10)
        self.assertIsNone(mh851_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh851_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh851_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh851_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh851_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh851_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh851_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh851_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh851_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none(self):
        bc = mh851_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh851_p_el_pareggio(
            6000, 9000, bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.05,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]))

    def test_p_el_pareggio_denominatore_non_positivo(self):
        self.assertIsNone(mh851_p_el_pareggio(
            6000, 9000, 1000.0, 0.09, 0.0, 0.05, 100.0, 100.0))
        self.assertIsNone(mh851_p_el_pareggio(
            6000, 9000, 1000.0, 0.09, 0.0, 0.05, 100.0, 150.0))

    def test_p_el_pareggio_positivo_e_soglia(self):
        kw = _demo_kwargs(q_risc=0, litri_acs_giorno=0,
                          quota_copertura=0, risparmio_led=0.80,
                          om_alt=20000)
        caso = mh851_calcola(**kw)
        p_star = caso["p_el_pareggio"]
        self.assertIsNotNone(p_star)
        self.assertAlmostEqual(p_star, 0.9210526315789473, places=12)
        esatto = mh851_calcola(**dict(kw, p_el=p_star))
        self.assertAlmostEqual(esatto["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(esatto["verdetto"], "NON_CALCOLABILE")
        sopra = mh851_calcola(**dict(kw, p_el=p_star + 0.01))
        self.assertAlmostEqual(sopra["risparmio_eur_anno"], 152.0,
                               places=4)
        sotto = mh851_calcola(**dict(kw, p_el=p_star - 0.01))
        self.assertAlmostEqual(sotto["risparmio_eur_anno"], -152.0,
                               places=4)
        self.assertEqual(sotto["verdetto"], "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh851_demo()
        val = mh851_valida(*[demo[k] for k in (
            "pneumatici_anno", "superficie_officina_m2",
            "addetti", "litri_acs_giorno", "giorni_anno",
            "acs_dt", "q_risc", "superficie_copertura_m2",
            "quota_copertura", "kwh_per_pneumatico_base",
            "kwh_per_pneumatico_alt", "f_calore_disp",
            "f_rec", "f_uso", "cop_pdc", "eta_caldaia",
            "e_illum_per_m2", "risparmio_led",
            "e_altre_per_m2", "prod_specifica",
            "f_autoconsumo", "p_el", "p_gas",
            "p_immissione", "om_base", "om_alt", "capex",
            "f_el", "f_gas", "wacc", "vita", "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_pneumatici_zero_no(self):
        self.assertFalse(mh851_valida(
            *([0] + [mh851_demo()[k] for k in (
                "superficie_officina_m2",
                "addetti", "litri_acs_giorno", "giorni_anno",
                "acs_dt", "q_risc", "superficie_copertura_m2",
                "quota_copertura", "kwh_per_pneumatico_base",
                "kwh_per_pneumatico_alt", "f_calore_disp",
                "f_rec", "f_uso", "cop_pdc", "eta_caldaia",
                "e_illum_per_m2", "risparmio_led",
                "e_altre_per_m2", "prod_specifica",
                "f_autoconsumo", "p_el", "p_gas",
                "p_immissione", "om_base", "om_alt", "capex",
                "f_el", "f_gas", "wacc", "vita", "tolleranza")]))["valido"])

    def test_valida_officina_zero_no(self):
        kw = _demo_kwargs(superficie_officina_m2=0)
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_copertura_zero_no(self):
        kw = _demo_kwargs(superficie_copertura_m2=0)
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0)
        self.assertRaises(ValueError, mh851_calcola, **kw)
        kw = _demo_kwargs(kwh_per_pneumatico_base=0)
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_rec=1.1)
        self.assertRaises(ValueError, mh851_calcola, **kw)
        kw = _demo_kwargs(quota_copertura=1.1)
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh851_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh851_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("giorni_anno", -1),
                              ("acs_dt", -1),
                              ("q_risc", -1),
                              ("p_gas", -0.01),
                              ("capex", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh851_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh851_calcola(mh851_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh851_calcola(dict(mh851_demo(), capex=999999), capex=80000)
        self.assertEqual(bc["capex_eur"], 80000.0)


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
        self.assertEqual(bc["payback"], 10)

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
            bc["e_comp_base_kwh_e_anno"]
            + bc["e_illum_base_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_comp_alt_kwh_e_anno"]
            + bc["e_pdc_kwh_e_anno"]
            + bc["e_illum_alt_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"])
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
        s = mh851_sensibilita(**mh851_demo())
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               7368.48, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               10332.14, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], -66233.38, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               8489.86, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], -68136.84, places=2)
        self.assertAlmostEqual(s["vita_10"]["van"], -11660.27, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 52754.61, places=2)

    def test_marginale_con_capex_95k(self):
        bc = mh851_calcola(**_demo_kwargs(capex=95000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -3136.84, places=2)
        self.assertEqual(bc["payback"], 11)

    def test_non_convente_con_capex_160k(self):
        bc = mh851_calcola(**_demo_kwargs(capex=160000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh851_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0, om_alt=999999))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh851_csv(bc, mh851_demo())
        for voce in ("pneumatici_anno", "e_comp_base_kwh_e_anno",
                     "q_disp_alt_kwh_th_anno", "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -80000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, caldaia a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Calore disponibile compressore VSD (kWh_th/anno)",
                      voci)

    def test_recupero_zero_con_f_rec_zero_o_f_uso_zero(self):
        self.assertEqual(mh851_q_rec(1000.0, 5000.0, 0.0, 0.8), 0.0)
        self.assertEqual(mh851_q_rec(1000.0, 5000.0, 0.7, 0.0), 0.0)

    def test_e_comp_scala_lineare_con_pneumatici(self):
        self.assertAlmostEqual(mh851_e_comp_base(2000.0, 2.5),
                               2.0 * mh851_e_comp_base(1000.0, 2.5))

    def test_co2_alt_senza_credito_immessa(self):
        # L'energia immessa non sottrae CO2: a parita' di
        # deficit, la CO2 alternativa non cambia.
        self.assertEqual(mh851_co2_alt(20000.0, 0.00035),
                         20000.0 * 0.00035)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh851_c_alt(20000.0, 0.22, 0.0, 0.05, 9000)
        con = mh851_c_alt(20000.0, 0.22, 10000.0, 0.05, 9000)
        self.assertAlmostEqual(senza - con, 500.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh851_sensibilita(**mh851_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh851_csv(bc, mh851_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_comp_base_kwh_e_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh851_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh851_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh851_calcola(**_demo_kwargs(giorni_anno=0))
        self.assertEqual(bc["q_acs_kwh_th_anno"], 0.0)
        bc = mh851_calcola(**_demo_kwargs(quota_copertura=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab851:"), 1)
        self.assertTrue(src.startswith("    # W855"))

    def test_ui_tab851_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab851:"), 1)
        self.assertIn("def mh851_demo(", src_h)
        self.assertIn("def mh851_calcola(", src_h)
        self.assertIn("tab851", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Gommista: compressore a velocita' variabile + recupero calore compressore + pompa di calore battono caldaia a gas + compressore on/off tradizionale?", src)
        self.assertIn("🛞 Gommista: compressore a velocita' variabile + recupero calore compressore + pompa di calore battono caldaia a gas + compressore on/off tradizionale?", src)
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
        chiavi = re.findall(r'key="(st851_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st851_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st851_calcola"', src)
        self.assertIn('key="st851_csv"', src)
        self.assertIn('key="st851_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def851\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh851_demo().keys()), lette - set(mh851_demo().keys()))
        self.assertEqual(lette, set(mh851_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc851\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc851\["([^"]+)"\]', src))
        attese = set(mh851_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg851"), src.index(".paiac("))
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
