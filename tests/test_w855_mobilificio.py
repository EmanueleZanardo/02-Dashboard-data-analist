"""Test nuova scheda mobilificio: lavorazione
legno efficiente + essiccazione a pompa di
calore + verniciatura ad acqua + FV battono
lavorazione tradizionale + essiccazione a
gas + caldaia a gas?

File: tests/test_w855_mobilificio.py

Business case annuo di un mobilificio,
connesso alla rete, guidato dai PEZZI DI
MOBILI PRODOTTI ALL'ANNO + SUPERFICIE
COPERTURA CAPANNONE (m2) + QUOTA FV (non
falegnameria, non serramenti, non
verniciatura industriale):
E_lav_base = pezzi x kwh_per_pezzo_base;
E_lav_alt = pezzi x kwh_per_pezzo_alt
(efficiente, minore); E_base_el =
E_lav_base + altre; E_alt_el = E_lav_alt
+ altre + E_pdc; Q_ess_base = pezzi x
q_ess_per_pezzo_base; Q_ess_alt = pezzi x
q_ess_per_pezzo_alt; Q_rec = f_recupero x
Q_ess_alt (35% del termico ALTERNATIVO,
non della base); Q_net = max(0, Q_ess_alt
- Q_rec); Gas_base = Q_ess_base /
eta_caldaia; Gas_alt = 0 (la caldaia a
gas SCOMPARE: il termico netto va in
pompa di calore); E_pdc = Q_net /
COP_pdc; kWp copertura = sup_copertura
x quota_fv x kwp_per_m2; E_pv = kWp x
resa_fv; E_pv_auto = min(E_pv x
f_autoconsumo, E_alt_el) (cappato alla
domanda elettrica alternativa);
E_immessa = E_pv - E_pv_auto; E_deficit
= max(0, E_alt_el - E_pv_auto); C_base
= E_base_el x p_el + Gas_base x p_gas
(nessun O&M); C_alt = E_deficit x p_el
- E_immessa x p_immissione (gas
alternativo zero; l'immessa e' un RICAVO
a prezzo di immissione, INFERIORE a p_el;
nessun credito CO2 per l'immessa);
risparmio = C_base - C_alt; CAPEX
forfettario 380.000 (FV 216.000 + PdC
45.000 + recupero 30.000 + lavorazione e
verniciatura delta 89.000); CO2 base =
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
e' -0,13587035591186944 EUR/kWh, quindi
None: il numeratore e' negativo
(-35.974,59 EUR/anno circa: gas evitato
26.470,59 piu' ricavo da immissione
9.504,00; denominatore 264.771,43
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
degenere (pezzi <= 0, copertura <= 0,
quota fv < 0 o > 1, kwh per pezzo base
<= 0, kwh per pezzo alt <= 0, altre < 0,
q ess per pezzo base <= 0, q ess per
pezzo alt <= 0, f_recupero < 0 o > 1,
cop_pdc <= 0, eta caldaia <= 0 o > 1,
kwp per m2 < 0, resa fv < 0,
f_autoconsumo < 0 o > 1, prezzi < 0,
CAPEX < 0, f_el < 0, f_gas < 0, WACC < 0,
vita <= 0 o non intera, tolleranza < 0)
o se risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w859_helpers import (
        demo_calcoli,
        mh855_c_alt,
        mh855_c_base,
        mh855_calcola,
        mh855_co2_alt,
        mh855_co2_base,
        mh855_co2_evitata,
        mh855_csv,
        mh855_demo,
        mh855_demo_calcoli,
        mh855_e_alt_el,
        mh855_e_base_el,
        mh855_e_deficit,
        mh855_e_immessa,
        mh855_e_lav_alt,
        mh855_e_lav_base,
        mh855_e_pdc,
        mh855_e_pv,
        mh855_e_pv_auto,
        mh855_eta,
        mh855_flussi,
        mh855_frazione,
        mh855_gas_alt,
        mh855_gas_base,
        mh855_int_pos,
        mh855_nneg,
        mh855_num,
        mh855_p_el_pareggio,
        mh855_p_pv_kwp,
        mh855_payback,
        mh855_pos,
        mh855_q_ess_alt,
        mh855_q_ess_base,
        mh855_q_net,
        mh855_q_rec,
        mh855_risparmio,
        mh855_sensibilita,
        mh855_tir,
        mh855_valida,
        mh855_van,
        mh855_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w859_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w859_helpers", os.path.join(_hf, "w859_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh855_c_alt = _mod.mh855_c_alt
    mh855_c_base = _mod.mh855_c_base
    mh855_calcola = _mod.mh855_calcola
    mh855_co2_alt = _mod.mh855_co2_alt
    mh855_co2_base = _mod.mh855_co2_base
    mh855_co2_evitata = _mod.mh855_co2_evitata
    mh855_csv = _mod.mh855_csv
    mh855_demo = _mod.mh855_demo
    mh855_demo_calcoli = _mod.mh855_demo_calcoli
    mh855_e_alt_el = _mod.mh855_e_alt_el
    mh855_e_base_el = _mod.mh855_e_base_el
    mh855_e_deficit = _mod.mh855_e_deficit
    mh855_e_immessa = _mod.mh855_e_immessa
    mh855_e_lav_alt = _mod.mh855_e_lav_alt
    mh855_e_lav_base = _mod.mh855_e_lav_base
    mh855_e_pdc = _mod.mh855_e_pdc
    mh855_e_pv = _mod.mh855_e_pv
    mh855_e_pv_auto = _mod.mh855_e_pv_auto
    mh855_eta = _mod.mh855_eta
    mh855_flussi = _mod.mh855_flussi
    mh855_frazione = _mod.mh855_frazione
    mh855_gas_alt = _mod.mh855_gas_alt
    mh855_gas_base = _mod.mh855_gas_base
    mh855_int_pos = _mod.mh855_int_pos
    mh855_nneg = _mod.mh855_nneg
    mh855_num = _mod.mh855_num
    mh855_p_el_pareggio = _mod.mh855_p_el_pareggio
    mh855_p_pv_kwp = _mod.mh855_p_pv_kwp
    mh855_payback = _mod.mh855_payback
    mh855_pos = _mod.mh855_pos
    mh855_q_ess_alt = _mod.mh855_q_ess_alt
    mh855_q_ess_base = _mod.mh855_q_ess_base
    mh855_q_net = _mod.mh855_q_net
    mh855_q_rec = _mod.mh855_q_rec
    mh855_risparmio = _mod.mh855_risparmio
    mh855_sensibilita = _mod.mh855_sensibilita
    mh855_tir = _mod.mh855_tir
    mh855_valida = _mod.mh855_valida
    mh855_van = _mod.mh855_van
    mh855_verdetto = _mod.mh855_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w859_helpers.py")
_UI_PATH = _risolvi("w859_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "4"
_VECCHIO_TAB = "tab85" + "4"
_VECCHIO_ST = "st85" + "4_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "e_lav_base_kwh_e_anno": 400000.0,
    "e_lav_alt_kwh_e_anno": 280000.0,
    "e_altre_kwh_e_anno": 60000.0,
    "e_base_el_kwh_e_anno": 460000.0,
    "e_alt_el_kwh_e_anno": 373428.5714285714,
    "q_ess_base_kwh_th_anno": 250000.0,
    "q_ess_alt_kwh_th_anno": 180000.0,
    "q_rec_kwh_th_anno": 63000.0,
    "q_net_kwh_th_anno": 117000.0,
    "gas_base_kwh_anno": 294117.64705882355,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 33428.57142857143,
    "p_pv_kwp": 270.0,
    "e_pv_kwh_e_anno": 297000.0,
    "e_pv_auto_kwh_e_anno": 178200.0,
    "e_immessa_kwh_e_anno": 118800.0,
    "e_deficit_kwh_e_anno": 195228.57142857142,
    "c_base_eur_anno": 155270.58823529413,
    "c_alt_eur_anno": 45160.0,
    "risparmio_eur_anno": 110110.58823529413,
    "capex_eur": 380000.0,
    "co2_base_t_anno": 219.8235294117647,
    "co2_alt_t_anno": 68.33,
    "co2_evitata_t_anno": 151.4935294117647,
    "van": 762910.2522652638,
    "tir": 28.285634376229897,
    "payback": 4,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh855_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh855_num(3, "x"), 3.0)
        self.assertEqual(mh855_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh855_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh855_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh855_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh855_pos(0, "x")
        with self.assertRaises(ValueError):
            mh855_pos(-1, "x")
        self.assertEqual(mh855_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh855_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh855_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh855_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh855_int_pos(15, "x"), 15)
        self.assertEqual(mh855_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh855_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh855_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh855_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh855_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh855_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh855_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_e_lav_base_e_alt(self):
        self.assertEqual(mh855_e_lav_base(10000, 40), 400000.0)
        self.assertEqual(mh855_e_lav_alt(10000, 28), 280000.0)
        with self.assertRaises(ValueError):
            mh855_e_lav_base(0, 40)
        with self.assertRaises(ValueError):
            mh855_e_lav_alt(10000, 0.0)

    def test_q_ess_base_e_alt(self):
        self.assertEqual(mh855_q_ess_base(10000, 25), 250000.0)
        self.assertEqual(mh855_q_ess_alt(10000, 18), 180000.0)

    def test_q_rec_sul_termico_alt_non_sulla_base(self):
        # 35% di 180.000 (alt), non di 250.000 (base):
        # 63.000, non 87.500.
        self.assertAlmostEqual(mh855_q_rec(180000.0, 0.35), 63000.0,
                               places=2)
        self.assertNotEqual(mh855_q_rec(180000.0, 0.35),
                            0.35 * 250000.0)
        self.assertEqual(mh855_q_rec(180000.0, 0.0), 0.0)

    def test_q_net(self):
        self.assertEqual(mh855_q_net(180000.0, 63000.0), 117000.0)
        self.assertEqual(mh855_q_net(180000.0, 180000.0), 0.0)

    def test_gas_base_e_alt_zero(self):
        self.assertAlmostEqual(mh855_gas_base(250000.0, 0.85),
                               294117.6471, places=2)
        self.assertEqual(mh855_gas_alt(), 0.0)

    def test_e_pdc(self):
        self.assertAlmostEqual(mh855_e_pdc(117000.0, 3.5),
                               33428.5714, places=2)
        with self.assertRaises(ValueError):
            mh855_e_pdc(100.0, 0.0)

    def test_e_base_e_alt(self):
        self.assertEqual(mh855_e_base_el(400000.0, 60000.0),
                         460000.0)
        self.assertEqual(mh855_e_alt_el(280000.0, 60000.0,
                                        33428.57142857143),
                         373428.5714285714)

    def test_p_pv_ed_e_pv(self):
        self.assertEqual(mh855_p_pv_kwp(3000, 0.50, 0.18), 270.0)
        self.assertEqual(mh855_e_pv(270.0, 1100), 297000.0)
        self.assertEqual(mh855_p_pv_kwp(3000, 0.0, 0.18), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh855_e_pv_auto(297000.0, 0.60, 373428.5714285714),
                         178200.0)
        self.assertEqual(mh855_e_pv_auto(200000.0, 0.60, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh855_e_immessa(297000.0, 178200.0), 118800.0)
        self.assertEqual(mh855_e_deficit(373428.5714285714, 178200.0),
                         195228.57142857142)
        self.assertEqual(mh855_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh855_c_base(460000.0, 0.28, 294117.6471, 0.09)
        self.assertAlmostEqual(cb, 155270.5882, places=2)
        ca = mh855_c_alt(195228.5714, 0.28, 118800.0, 0.08)
        self.assertAlmostEqual(ca, 45160.0, places=2)
        self.assertAlmostEqual(mh855_risparmio(cb, ca), 110110.5882,
                               places=2)

    def test_co2_con_divisione_per_mille(self):
        # Fattori in kg/kWh: divisione per 1000 in
        # questa scheda, a differenza delle schede
        # con fattori diretti in t/kWh.
        cb = mh855_co2_base(460000.0, 0.35, 294117.6471, 0.20)
        self.assertAlmostEqual(cb, 219.8235, places=2)
        ca = mh855_co2_alt(195228.5714, 0.35)
        self.assertAlmostEqual(ca, 68.33, places=2)
        self.assertAlmostEqual(mh855_co2_evitata(cb, ca), 151.4935,
                               places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh855_flussi(380000, 110110.5882, 3),
                         [-380000, 110110.5882, 110110.5882, 110110.5882])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh855_van([-100, 60, 60], 0), 20.0)
        bc = mh855_demo_calcoli()
        self.assertAlmostEqual(mh855_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh855_demo_calcoli()
        tir = mh855_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh855_tir([-100, -10, -10]))
        self.assertIsNone(mh855_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh855_demo_calcoli()
        self.assertEqual(mh855_payback(bc["flussi"]), 4)
        self.assertIsNone(mh855_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh855_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh855_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh855_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh855_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh855_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh855_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh855_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh855_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none_e_segno(self):
        bc = mh855_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh855_p_el_pareggio(
            bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.08,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]))
        grezzo = (-bc["gas_base_kwh_anno"] * 0.09
                  - bc["e_immessa_kwh_e_anno"] * 0.08) / (
                      bc["e_base_el_kwh_e_anno"]
                      - bc["e_deficit_kwh_e_anno"])
        self.assertAlmostEqual(grezzo, -0.13587035591186944, places=12)
        self.assertLess(grezzo, 0.0)

    def test_p_el_pareggio_denominatore_non_positivo(self):
        self.assertIsNone(mh855_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 100.0))
        self.assertIsNone(mh855_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 150.0))

    def test_p_el_pareggio_caso_limite_zero(self):
        # Solo nel caso limite gas zero e immessa
        # zero il pareggio vale 0 (non negativo):
        # e' l'unico caso in cui non e' None.
        self.assertEqual(mh855_p_el_pareggio(
            0.0, 0.09, 0.0, 0.08, 460000.0, 10000.0), 0.0)

    def test_valida_demo_ok(self):
        demo = mh855_demo()
        val = mh855_valida(*[demo[k] for k in (
            "pezzi_anno", "sup_copertura_m2",
            "quota_fv", "kwh_per_pezzo_base", "kwh_per_pezzo_alt",
            "e_altre", "q_ess_per_pezzo_base",
            "q_ess_per_pezzo_alt", "f_recupero", "cop_pdc",
            "eta_caldaia", "kwp_per_m2", "resa_fv",
            "f_autoconsumo", "p_el", "p_gas", "p_immissione",
            "capex", "f_el", "f_gas", "wacc", "vita",
            "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_pezzi_zero_no(self):
        kw = _demo_kwargs(pezzi_anno=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_copertura_zero_no(self):
        kw = _demo_kwargs(sup_copertura_m2=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)
        kw = _demo_kwargs(kwh_per_pezzo_base=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)
        kw = _demo_kwargs(kwh_per_pezzo_alt=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)
        kw = _demo_kwargs(q_ess_per_pezzo_alt=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh855_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh855_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh855_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_altre", -1),
                              ("p_gas", -0.01),
                              ("capex", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh855_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh855_calcola(mh855_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh855_calcola(dict(mh855_demo(), capex=999999), capex=380000)
        self.assertEqual(bc["capex_eur"], 380000.0)


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
            bc["q_ess_alt_kwh_th_anno"],
            bc["q_rec_kwh_th_anno"] + bc["q_net_kwh_th_anno"])
        self.assertAlmostEqual(
            bc["e_base_el_kwh_e_anno"],
            bc["e_lav_base_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_lav_alt_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"]
            + bc["e_pdc_kwh_e_anno"])
        self.assertLessEqual(bc["q_rec_kwh_th_anno"],
                             bc["q_ess_alt_kwh_th_anno"])

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
        s = mh855_sensibilita(**mh855_demo())
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               95283.39, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               124937.79, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], 146358.56, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               105070.59, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], 382910.25, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"], 470244.78, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 1271658.82, places=2)

    def test_marginale_con_capex_alto(self):
        # CAPEX 1.150.000: VAN negativa entro la
        # tolleranza del 10% di 1.150.000.
        bc = mh855_calcola(**_demo_kwargs(capex=1150000))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_alto(self):
        bc = mh855_calcola(**_demo_kwargs(capex=1300000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh855_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh855_csv(bc, mh855_demo())
        for voce in ("pezzi_anno", "e_lav_base_kwh_e_anno",
                     "q_rec_kwh_th_anno",
                     "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -380000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, caldaia a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Calore recuperato (kWh_th/anno)",
                      voci)

    def test_recupero_zero_con_f_recupero_zero(self):
        self.assertEqual(mh855_q_rec(180000.0, 0.0), 0.0)

    def test_e_lav_scala_lineare_con_pezzi(self):
        self.assertAlmostEqual(mh855_e_lav_base(10000.0, 40),
                               2.0 * mh855_e_lav_base(5000.0, 40))

    def test_co2_alt_senza_credito_immessa(self):
        # L'energia immessa non sottrae CO2: a parita' di
        # deficit, la CO2 alternativa non cambia.
        self.assertEqual(mh855_co2_alt(20000.0, 0.35),
                         20000.0 * 0.35 / 1000.0)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh855_c_alt(20000.0, 0.28, 0.0, 0.08, )
        con = mh855_c_alt(20000.0, 0.28, 10000.0, 0.08)
        self.assertAlmostEqual(senza - con, 800.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh855_sensibilita(**mh855_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh855_csv(bc, mh855_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_lav_base_kwh_e_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh855_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh855_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh855_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        bc = mh855_calcola(**_demo_kwargs(e_altre=0))
        self.assertEqual(bc["e_altre_kwh_e_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def855\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh855_demo().keys()), lette - set(mh855_demo().keys()))
        self.assertEqual(lette, set(mh855_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc855\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc855\["([^"]+)"\]', src))
        attese = set(mh855_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab855:"), 1)
        self.assertTrue(src.startswith("    # W859"))

    def test_ui_tab855_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab855:"), 1)
        self.assertIn("def mh855_demo(", src_h)
        self.assertIn("def mh855_calcola(", src_h)
        self.assertIn("tab855", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Mobilificio: lavorazione legno efficiente + essiccazione a pompa di calore + verniciatura ad acqua + FV battono lavorazione tradizionale + essiccazione a gas + caldaia a gas?", src)
        self.assertIn("🪑 Mobilificio: lavorazione legno efficiente + essiccazione a pompa di calore + verniciatura ad acqua + FV battono lavorazione tradizionale + essiccazione a gas + caldaia a gas?", src)
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
        chiavi = re.findall(r'key="(st855_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st855_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st855_calcola"', src)
        self.assertIn('key="st855_csv"', src)
        self.assertIn('key="st855_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg855"), src.index(".paiac("))
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
