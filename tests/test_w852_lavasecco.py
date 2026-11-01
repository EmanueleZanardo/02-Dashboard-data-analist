"""Test nuova scheda lavasecco: macchine
efficienti + recupero calore vapore + pompa
di calore + FV battono caldaia a gas +
macchine tradizionali?

Business case annuo di un lavasecco,
connesso alla rete, guidato dai KG DI CAPI
LAVATI ALL'ANNO + SUPERFICIE LOCALE +
SUPERFICIE COPERTURA (non lavanderia
industriale generica, non autolavaggio,
non gommista): E_lav_base = kg x
kwh_per_kg_base; E_lav_alt = kg x
kwh_per_kg_alt (efficienti, minore);
E_illum_base = sup_locale x
e_illum_per_m2_base; E_illum_alt =
sup_locale x e_illum_per_m2_alt (LED);
E_base_el = E_lav_base + stireria base +
illum base + altre; E_alt_el = E_lav_alt
+ stireria alt + illum alt + altre +
E_pdc; Q_vapore_base = kg x
q_vapore_per_kg_base; Q_vapore_alt = kg x
q_vapore_per_kg_alt; Q_risc = sup_locale
x q_risc_per_m2; Q_termico_base =
Q_vapore_base + Q_risc; Q_rec =
f_recupero x Q_vapore_alt (25% del vapore
ALTERNATIVO, non del base); Q_net =
Q_vapore_alt + Q_risc - Q_rec;
Gas_base = Q_termico_base / eta_caldaia;
Gas_alt = 0 (la caldaia a gas SCOMPARE:
il termico netto va in pompa di calore);
E_pdc = Q_net / COP_pdc; kWp copertura =
sup_copertura x quota_fv x kwp_per_m2;
E_pv = kWp x resa_fv; E_pv_auto =
min(E_pv x f_autoconsumo, E_alt_el)
(cappato alla domanda elettrica
alternativa); E_immessa = E_pv - E_pv_auto;
E_deficit = max(0, E_alt_el - E_pv_auto);
C_base = E_base_el x p_el + Gas_base x
p_gas (nessun O&M); C_alt = E_deficit x
p_el - E_immessa x p_immissione (gas
alternativo zero; l'immessa e' un RICAVO
a prezzo di immissione, INFERIORE a p_el;
nessun credito CO2 per l'immessa);
risparmio = C_base - C_alt; CAPEX
forfettario 77.400 (FV 32.400 + PdC
15.000 + recupero 8.000 + macchine delta
20.000 + LED 2.000); CO2 base =
(E_base_el x f_el + Gas_base x f_gas) /
1000 (fattori in kg/kWh, divisione per
1000 in questa scheda); CO2 alt =
E_deficit x f_el / 1000 (gas alternativo
zero, nessun credito CO2 per l'immessa);
CO2 evitata = base - alt (segno libero);
flussi [-CAPEX, risparmio x vita];
VAN al WACC (PERCENTUALE in ingresso,
/ 100 dentro); TIR per bisezione; payback
(primo anno con cumulato >= 0); prezzo
elettrico di pareggio p_star =
(- Gas_base x p_gas - E_immessa x
p_immissione) / (E_base_el - E_deficit)
in forma chiusa a prezzo gas e prezzo
immissione FERMI (nessun O&M), None se
E_base_el - E_deficit <= 0 o se p_star
< 0, SOGLIA MINIMA sui soli costi annui
quando esiste (il CAPEX non entra nel
pareggio annuo). Nel demo p_star grezzo
e' -0,9261617912348339 EUR/kWh, quindi
None: il numeratore e' negativo
(-10.267,06 EUR/anno circa: gas evitato
9.317,65 piu' ricavo da immissione
950,40; denominatore 11.086,67
kWh_e/anno), quindi l'alternativa vince
sui costi annui anche a prezzo elettrico
nullo. In regime valido con gas base
positivo o immessa positiva il pareggio
non puo' mai essere positivo, perche'
il numeratore e' sempre nullo o
negativo (nessun O&M a spostarlo): solo
nel caso limite gas base zero e immessa
zero il pareggio vale 0.
Verdetto: NON_CALCOLABILE se input
degenere (kg <= 0, superfici <= 0, quota
fv < 0 o > 1, kwh per kg base <= 0, kwh
per kg alt <= 0, stireria < 0,
illuminazione per m2 < 0, altre < 0,
q vapore per kg base <= 0, q vapore per
kg alt <= 0, q risc per m2 < 0,
f_recupero < 0 o > 1, cop_pdc <= 0, eta
caldaia <= 0 o > 1, kwp per m2 < 0,
resa fv < 0, f_autoconsumo < 0 o > 1,
prezzi < 0, CAPEX < 0, f_el < 0, f_gas
< 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
"""

import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w856_helpers import (
        demo_calcoli,
        mh852_c_alt,
        mh852_c_base,
        mh852_calcola,
        mh852_co2_alt,
        mh852_co2_base,
        mh852_co2_evitata,
        mh852_csv,
        mh852_demo,
        mh852_demo_calcoli,
        mh852_e_alt_el,
        mh852_e_base_el,
        mh852_e_deficit,
        mh852_e_illum_alt,
        mh852_e_illum_base,
        mh852_e_immessa,
        mh852_e_lav_alt,
        mh852_e_lav_base,
        mh852_e_pdc,
        mh852_e_pv,
        mh852_e_pv_auto,
        mh852_eta,
        mh852_flussi,
        mh852_frazione,
        mh852_gas_alt,
        mh852_gas_base,
        mh852_int_pos,
        mh852_nneg,
        mh852_num,
        mh852_p_el_pareggio,
        mh852_p_pv_kwp,
        mh852_payback,
        mh852_pos,
        mh852_q_net,
        mh852_q_rec,
        mh852_q_risc,
        mh852_q_termico,
        mh852_q_vapore_alt,
        mh852_q_vapore_base,
        mh852_risparmio,
        mh852_sensibilita,
        mh852_tir,
        mh852_valida,
        mh852_van,
        mh852_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w856_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w856_helpers", os.path.join(_hf, "w856_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh852_c_alt = _mod.mh852_c_alt
    mh852_c_base = _mod.mh852_c_base
    mh852_calcola = _mod.mh852_calcola
    mh852_co2_alt = _mod.mh852_co2_alt
    mh852_co2_base = _mod.mh852_co2_base
    mh852_co2_evitata = _mod.mh852_co2_evitata
    mh852_csv = _mod.mh852_csv
    mh852_demo = _mod.mh852_demo
    mh852_demo_calcoli = _mod.mh852_demo_calcoli
    mh852_e_alt_el = _mod.mh852_e_alt_el
    mh852_e_base_el = _mod.mh852_e_base_el
    mh852_e_deficit = _mod.mh852_e_deficit
    mh852_e_illum_alt = _mod.mh852_e_illum_alt
    mh852_e_illum_base = _mod.mh852_e_illum_base
    mh852_e_immessa = _mod.mh852_e_immessa
    mh852_e_lav_alt = _mod.mh852_e_lav_alt
    mh852_e_lav_base = _mod.mh852_e_lav_base
    mh852_e_pdc = _mod.mh852_e_pdc
    mh852_e_pv = _mod.mh852_e_pv
    mh852_e_pv_auto = _mod.mh852_e_pv_auto
    mh852_eta = _mod.mh852_eta
    mh852_flussi = _mod.mh852_flussi
    mh852_frazione = _mod.mh852_frazione
    mh852_gas_alt = _mod.mh852_gas_alt
    mh852_gas_base = _mod.mh852_gas_base
    mh852_int_pos = _mod.mh852_int_pos
    mh852_nneg = _mod.mh852_nneg
    mh852_num = _mod.mh852_num
    mh852_p_el_pareggio = _mod.mh852_p_el_pareggio
    mh852_p_pv_kwp = _mod.mh852_p_pv_kwp
    mh852_payback = _mod.mh852_payback
    mh852_pos = _mod.mh852_pos
    mh852_q_net = _mod.mh852_q_net
    mh852_q_rec = _mod.mh852_q_rec
    mh852_q_risc = _mod.mh852_q_risc
    mh852_q_termico = _mod.mh852_q_termico
    mh852_q_vapore_alt = _mod.mh852_q_vapore_alt
    mh852_q_vapore_base = _mod.mh852_q_vapore_base
    mh852_risparmio = _mod.mh852_risparmio
    mh852_sensibilita = _mod.mh852_sensibilita
    mh852_tir = _mod.mh852_tir
    mh852_valida = _mod.mh852_valida
    mh852_van = _mod.mh852_van
    mh852_verdetto = _mod.mh852_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w856_helpers.py")
_UI_PATH = _risolvi("w856_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "1"
_VECCHIO_TAB = "tab85" + "1"
_VECCHIO_ST = "st85" + "1_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "e_lav_base_kwh_e_anno": 18000.0,
    "e_lav_alt_kwh_e_anno": 10800.0,
    "e_illum_base_kwh_e_anno": 8000.0,
    "e_illum_alt_kwh_e_anno": 4000.0,
    "e_altre_kwh_e_anno": 6000.0,
    "e_base_el_kwh_e_anno": 40000.0,
    "e_alt_el_kwh_e_anno": 46733.33333333333,
    "q_vapore_base_kwh_th_anno": 72000.0,
    "q_vapore_alt_kwh_th_anno": 60000.0,
    "q_risc_kwh_th_anno": 16000.0,
    "q_termico_base_kwh_th_anno": 88000.0,
    "q_termico_alt_kwh_th_anno": 76000.0,
    "q_rec_kwh_th_anno": 15000.0,
    "q_net_kwh_th_anno": 61000.0,
    "gas_base_kwh_anno": 103529.41176470589,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 20333.333333333332,
    "p_pv_kwp": 27.0,
    "e_pv_kwh_e_anno": 29700.0,
    "e_pv_auto_kwh_e_anno": 17820.0,
    "e_immessa_kwh_e_anno": 11880.0,
    "e_deficit_kwh_e_anno": 28913.33333333333,
    "c_base_eur_anno": 20517.64705882353,
    "c_alt_eur_anno": 7145.333333333333,
    "risparmio_eur_anno": 13372.3137254902,
    "capex_eur": 77400.0,
    "co2_base_t_anno": 34.705882352941174,
    "co2_alt_t_anno": 10.119666666666664,
    "co2_evitata_t_anno": 24.58621568627451,
    "van": 61400.04364985698,
    "tir": 15.211331990133747,
    "payback": 6,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh852_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh852_num(3, "x"), 3.0)
        self.assertEqual(mh852_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh852_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh852_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh852_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh852_pos(0, "x")
        with self.assertRaises(ValueError):
            mh852_pos(-1, "x")
        self.assertEqual(mh852_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh852_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh852_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh852_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh852_int_pos(15, "x"), 15)
        self.assertEqual(mh852_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh852_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh852_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh852_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh852_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh852_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh852_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_e_lav_base_e_alt(self):
        self.assertEqual(mh852_e_lav_base(60000, 0.30), 18000.0)
        self.assertEqual(mh852_e_lav_alt(60000, 0.18), 10800.0)
        with self.assertRaises(ValueError):
            mh852_e_lav_base(0, 0.30)
        with self.assertRaises(ValueError):
            mh852_e_lav_alt(60000, 0.0)

    def test_q_vapore_base_e_alt(self):
        self.assertEqual(mh852_q_vapore_base(60000, 1.20), 72000.0)
        self.assertEqual(mh852_q_vapore_alt(60000, 1.00), 60000.0)

    def test_q_risc_e_termico(self):
        self.assertEqual(mh852_q_risc(200, 80), 16000.0)
        self.assertEqual(mh852_q_termico(72000.0, 16000.0), 88000.0)

    def test_q_rec_sul_vapore_alt_non_sul_base(self):
        # 25% di 60.000 (alt), non di 72.000 (base):
        # 15.000, non 18.000.
        self.assertEqual(mh852_q_rec(60000.0, 0.25), 15000.0)
        self.assertNotEqual(mh852_q_rec(60000.0, 0.25),
                            0.25 * 72000.0)
        self.assertEqual(mh852_q_rec(60000.0, 0.0), 0.0)

    def test_q_net(self):
        self.assertEqual(mh852_q_net(60000.0, 16000.0, 15000.0),
                         61000.0)
        self.assertEqual(mh852_q_net(60000.0, 0.0, 60000.0), 0.0)

    def test_gas_base_e_alt_zero(self):
        self.assertAlmostEqual(mh852_gas_base(88000.0, 0.85),
                               103529.4118, places=2)
        self.assertEqual(mh852_gas_alt(), 0.0)

    def test_e_pdc(self):
        self.assertAlmostEqual(mh852_e_pdc(61000.0, 3.0),
                               20333.3333, places=2)
        with self.assertRaises(ValueError):
            mh852_e_pdc(100.0, 0.0)

    def test_illum_base_e_alt(self):
        self.assertEqual(mh852_e_illum_base(200, 40), 8000.0)
        self.assertEqual(mh852_e_illum_alt(200, 20), 4000.0)

    def test_e_base_e_alt(self):
        self.assertEqual(mh852_e_base_el(18000.0, 8000.0, 8000.0,
                                         6000.0), 40000.0)
        self.assertAlmostEqual(
            mh852_e_alt_el(10800.0, 5600.0, 4000.0, 6000.0,
                           20333.3333),
            46733.3333, places=2)

    def test_p_pv_ed_e_pv(self):
        self.assertEqual(mh852_p_pv_kwp(250, 0.60, 0.18), 27.0)
        self.assertEqual(mh852_e_pv(27.0, 1100), 29700.0)
        self.assertEqual(mh852_p_pv_kwp(250, 0.0, 0.18), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh852_e_pv_auto(29700.0, 0.60, 46733.3333),
                         17820.0)
        self.assertEqual(mh852_e_pv_auto(200000.0, 0.60, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh852_e_immessa(29700.0, 17820.0), 11880.0)
        self.assertAlmostEqual(mh852_e_deficit(46733.3333, 17820.0),
                               28913.3333, places=2)
        self.assertEqual(mh852_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh852_c_base(40000.0, 0.28, 103529.4118, 0.09)
        self.assertAlmostEqual(cb, 20517.6471, places=2)
        ca = mh852_c_alt(28913.3333, 0.28, 11880.0, 0.08)
        self.assertAlmostEqual(ca, 7145.3333, places=2)
        self.assertAlmostEqual(mh852_risparmio(cb, ca), 13372.3137,
                               places=2)

    def test_co2_con_divisione_per_mille(self):
        # Fattori in kg/kWh: divisione per 1000 in
        # questa scheda, a differenza delle schede
        # con fattori diretti in t/kWh.
        cb = mh852_co2_base(40000.0, 0.35, 103529.4118, 0.20)
        self.assertAlmostEqual(cb, 34.7059, places=2)
        ca = mh852_co2_alt(28913.3333, 0.35)
        self.assertAlmostEqual(ca, 10.1197, places=2)
        self.assertAlmostEqual(mh852_co2_evitata(cb, ca), 24.5862,
                               places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh852_flussi(77400, 13372.3137, 3),
                         [-77400, 13372.3137, 13372.3137, 13372.3137])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh852_van([-100, 60, 60], 0), 20.0)
        bc = mh852_demo_calcoli()
        self.assertAlmostEqual(mh852_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh852_demo_calcoli()
        tir = mh852_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh852_tir([-100, -10, -10]))
        self.assertIsNone(mh852_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh852_demo_calcoli()
        self.assertEqual(mh852_payback(bc["flussi"]), 6)
        self.assertIsNone(mh852_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh852_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh852_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh852_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh852_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh852_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh852_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh852_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh852_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none_e_segno(self):
        bc = mh852_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh852_p_el_pareggio(
            bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.08,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]))
        grezzo = (-bc["gas_base_kwh_anno"] * 0.09
                  - bc["e_immessa_kwh_e_anno"] * 0.08) / (
                      bc["e_base_el_kwh_e_anno"]
                      - bc["e_deficit_kwh_e_anno"])
        self.assertAlmostEqual(grezzo, -0.9261617912348339, places=12)
        self.assertLess(grezzo, 0.0)

    def test_p_el_pareggio_denominatore_non_positivo(self):
        self.assertIsNone(mh852_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 100.0))
        self.assertIsNone(mh852_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 150.0))

    def test_p_el_pareggio_caso_limite_zero(self):
        # Solo nel caso limite gas zero e immessa
        # zero il pareggio vale 0 (non negativo):
        # e' l'unico caso in cui non e' None.
        self.assertEqual(mh852_p_el_pareggio(
            0.0, 0.09, 0.0, 0.08, 40000.0, 10000.0), 0.0)

    def test_valida_demo_ok(self):
        demo = mh852_demo()
        val = mh852_valida(*[demo[k] for k in (
            "kg_capi_anno", "sup_locale_m2", "sup_copertura_m2",
            "quota_fv", "kwh_per_kg_base", "kwh_per_kg_alt",
            "e_stireria_base", "e_stireria_alt",
            "e_illum_per_m2_base", "e_illum_per_m2_alt",
            "e_altre", "q_vapore_per_kg_base",
            "q_vapore_per_kg_alt", "q_risc_per_m2",
            "f_recupero", "cop_pdc", "eta_caldaia",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_el", "p_gas", "p_immissione", "capex",
            "f_el", "f_gas", "wacc", "vita", "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_kg_zero_no(self):
        kw = _demo_kwargs(kg_capi_anno=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_superfici_zero_no(self):
        kw = _demo_kwargs(sup_locale_m2=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)
        kw = _demo_kwargs(sup_copertura_m2=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)
        kw = _demo_kwargs(kwh_per_kg_base=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)
        kw = _demo_kwargs(q_vapore_per_kg_alt=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh852_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh852_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh852_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("q_risc_per_m2", -1),
                              ("e_altre", -1),
                              ("p_gas", -0.01),
                              ("capex", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh852_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh852_calcola(mh852_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh852_calcola(dict(mh852_demo(), capex=999999), capex=77400)
        self.assertEqual(bc["capex_eur"], 77400.0)


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
        self.assertEqual(bc["payback"], 6)

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
            bc["q_termico_alt_kwh_th_anno"],
            bc["q_rec_kwh_th_anno"] + bc["q_net_kwh_th_anno"])
        self.assertAlmostEqual(
            bc["e_base_el_kwh_e_anno"],
            bc["e_lav_base_kwh_e_anno"]
            + bc["e_stireria_base"]
            + bc["e_illum_base_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_lav_alt_kwh_e_anno"]
            + bc["e_stireria_alt"]
            + bc["e_illum_alt_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"]
            + bc["e_pdc_kwh_e_anno"])
        self.assertLessEqual(bc["q_rec_kwh_th_anno"],
                             bc["q_vapore_alt_kwh_th_anno"])

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
        s = mh852_sensibilita(**mh852_demo())
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               12751.46, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               13993.17, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], -255.13, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               11972.31, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], -15999.96, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"], 25857.46, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 123184.71, places=2)

    def test_marginale_con_capex_alto(self):
        # CAPEX 140.000: VAN negativa entro la
        # tolleranza del 10% di 140.000.
        bc = mh852_calcola(**_demo_kwargs(capex=140000))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_160k(self):
        bc = mh852_calcola(**_demo_kwargs(capex=160000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh852_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh852_csv(bc, mh852_demo())
        for voce in ("kg_capi_anno", "e_lav_base_kwh_e_anno",
                     "q_rec_kwh_th_anno", "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -77400.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, caldaia a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Calore recuperato dal vapore (kWh_th/anno)",
                      voci)

    def test_recupero_zero_con_f_recupero_zero(self):
        self.assertEqual(mh852_q_rec(60000.0, 0.0), 0.0)

    def test_e_lav_scala_lineare_con_kg(self):
        self.assertAlmostEqual(mh852_e_lav_base(2000.0, 0.30),
                               2.0 * mh852_e_lav_base(1000.0, 0.30))

    def test_co2_alt_senza_credito_immessa(self):
        # L'energia immessa non sottrae CO2: a parita' di
        # deficit, la CO2 alternativa non cambia.
        self.assertEqual(mh852_co2_alt(20000.0, 0.35),
                         20000.0 * 0.35 / 1000.0)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh852_c_alt(20000.0, 0.28, 0.0, 0.08, )
        con = mh852_c_alt(20000.0, 0.28, 10000.0, 0.08)
        self.assertAlmostEqual(senza - con, 800.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh852_sensibilita(**mh852_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh852_csv(bc, mh852_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_lav_base_kwh_e_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh852_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh852_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh852_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        bc = mh852_calcola(**_demo_kwargs(e_altre=0))
        self.assertEqual(bc["e_altre_kwh_e_anno"], 0.0)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab852:"), 1)
        self.assertTrue(src.startswith("    # W856"))

    def test_ui_tab852_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab852:"), 1)
        self.assertIn("def mh852_demo(", src_h)
        self.assertIn("def mh852_calcola(", src_h)
        self.assertIn("tab852", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Lavasecco: macchine efficienti + recupero calore vapore + pompa di calore + FV battono caldaia a gas + macchine tradizionali?", src)
        self.assertIn("🧺 Lavasecco: macchine efficienti + recupero calore vapore + pompa di calore + FV battono caldaia a gas + macchine tradizionali?", src)
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
        chiavi = re.findall(r'key="(st852_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st852_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st852_calcola"', src)
        self.assertIn('key="st852_csv"', src)
        self.assertIn('key="st852_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def852\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh852_demo().keys()), lette - set(mh852_demo().keys()))
        self.assertEqual(lette, set(mh852_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc852\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc852\["([^"]+)"\]', src))
        attese = set(mh852_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg852"), src.index(".paiac("))
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
