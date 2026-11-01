"""Test nuova scheda acquacoltura: pompe e
ossigenatori efficienti + recupero calore
+ pompa di calore + FV battono caldaia a
gas + pompaggio tradizionale?

Business case annuo di un impianto di
acquacoltura, connesso alla rete, guidato
dai KG DI PESCE PRODOTTO ALL'ANNO +
VOLUME VASCHE (m3) + SUPERFICIE
COPERTURA (m2) (non pesca, non
allevamento terrestre, non depurazione):
E_oss_base = kg x kwh_per_kg_base;
E_oss_alt = kg x kwh_per_kg_alt
(efficienti, minore); E_base_el =
E_oss_base + altre; E_alt_el = E_oss_alt
+ altre + E_pdc; Q_acqua_base = volume x
q_acqua_per_m3_base; Q_acqua_alt =
volume x q_acqua_per_m3_alt; Q_rec =
f_recupero x Q_acqua_alt (20% dell'acqua
ALTERNATIVA, non della base); Q_net =
max(0, Q_acqua_alt - Q_rec);
Gas_base = Q_acqua_base / eta_caldaia;
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
forfettario 82.200 (FV 43.200 + PdC
18.000 + recupero 6.000 + pompe delta
15.000); CO2 base =
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
e' -0,1425010371748614 EUR/kWh, quindi
None: il numeratore e' negativo
(-7.620,14 EUR/anno circa: gas evitato
6.352,94 piu' ricavo da immissione
1.267,20; denominatore 53.474,29
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
degenere (kg <= 0, volume <= 0,
copertura <= 0, quota fv < 0 o > 1, kwh
per kg base <= 0, kwh per kg alt <= 0,
altre < 0, q acqua per m3 base <= 0,
q acqua per m3 alt <= 0, f_recupero < 0
o > 1, cop_pdc <= 0, eta caldaia <= 0
o > 1, kwp per m2 < 0, resa fv < 0,
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
    from w857_helpers import (
        demo_calcoli,
        mh853_c_alt,
        mh853_c_base,
        mh853_calcola,
        mh853_co2_alt,
        mh853_co2_base,
        mh853_co2_evitata,
        mh853_csv,
        mh853_demo,
        mh853_demo_calcoli,
        mh853_e_alt_el,
        mh853_e_base_el,
        mh853_e_deficit,
        mh853_e_immessa,
        mh853_e_oss_alt,
        mh853_e_oss_base,
        mh853_e_pdc,
        mh853_e_pv,
        mh853_e_pv_auto,
        mh853_eta,
        mh853_flussi,
        mh853_frazione,
        mh853_gas_alt,
        mh853_gas_base,
        mh853_int_pos,
        mh853_nneg,
        mh853_num,
        mh853_p_el_pareggio,
        mh853_p_pv_kwp,
        mh853_payback,
        mh853_pos,
        mh853_q_acqua_alt,
        mh853_q_acqua_base,
        mh853_q_net,
        mh853_q_rec,
        mh853_risparmio,
        mh853_sensibilita,
        mh853_tir,
        mh853_valida,
        mh853_van,
        mh853_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w857_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w857_helpers", os.path.join(_hf, "w857_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh853_c_alt = _mod.mh853_c_alt
    mh853_c_base = _mod.mh853_c_base
    mh853_calcola = _mod.mh853_calcola
    mh853_co2_alt = _mod.mh853_co2_alt
    mh853_co2_base = _mod.mh853_co2_base
    mh853_co2_evitata = _mod.mh853_co2_evitata
    mh853_csv = _mod.mh853_csv
    mh853_demo = _mod.mh853_demo
    mh853_demo_calcoli = _mod.mh853_demo_calcoli
    mh853_e_alt_el = _mod.mh853_e_alt_el
    mh853_e_base_el = _mod.mh853_e_base_el
    mh853_e_deficit = _mod.mh853_e_deficit
    mh853_e_immessa = _mod.mh853_e_immessa
    mh853_e_oss_alt = _mod.mh853_e_oss_alt
    mh853_e_oss_base = _mod.mh853_e_oss_base
    mh853_e_pdc = _mod.mh853_e_pdc
    mh853_e_pv = _mod.mh853_e_pv
    mh853_e_pv_auto = _mod.mh853_e_pv_auto
    mh853_eta = _mod.mh853_eta
    mh853_flussi = _mod.mh853_flussi
    mh853_frazione = _mod.mh853_frazione
    mh853_gas_alt = _mod.mh853_gas_alt
    mh853_gas_base = _mod.mh853_gas_base
    mh853_int_pos = _mod.mh853_int_pos
    mh853_nneg = _mod.mh853_nneg
    mh853_num = _mod.mh853_num
    mh853_p_el_pareggio = _mod.mh853_p_el_pareggio
    mh853_p_pv_kwp = _mod.mh853_p_pv_kwp
    mh853_payback = _mod.mh853_payback
    mh853_pos = _mod.mh853_pos
    mh853_q_acqua_alt = _mod.mh853_q_acqua_alt
    mh853_q_acqua_base = _mod.mh853_q_acqua_base
    mh853_q_net = _mod.mh853_q_net
    mh853_q_rec = _mod.mh853_q_rec
    mh853_risparmio = _mod.mh853_risparmio
    mh853_sensibilita = _mod.mh853_sensibilita
    mh853_tir = _mod.mh853_tir
    mh853_valida = _mod.mh853_valida
    mh853_van = _mod.mh853_van
    mh853_verdetto = _mod.mh853_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w857_helpers.py")
_UI_PATH = _risolvi("w857_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "2"
_VECCHIO_TAB = "tab85" + "2"
_VECCHIO_ST = "st85" + "2_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "e_oss_base_kwh_e_anno": 100000.0,
    "e_oss_alt_kwh_e_anno": 60000.0,
    "e_altre_kwh_e_anno": 20000.0,
    "e_base_el_kwh_e_anno": 120000.0,
    "e_alt_el_kwh_e_anno": 90285.71428571429,
    "q_acqua_base_kwh_th_anno": 60000.0,
    "q_acqua_alt_kwh_th_anno": 45000.0,
    "q_rec_kwh_th_anno": 9000.0,
    "q_net_kwh_th_anno": 36000.0,
    "gas_base_kwh_anno": 70588.23529411765,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 10285.714285714286,
    "p_pv_kwp": 36.0,
    "e_pv_kwh_e_anno": 39600.0,
    "e_pv_auto_kwh_e_anno": 23760.0,
    "e_immessa_kwh_e_anno": 15840.0,
    "e_deficit_kwh_e_anno": 66525.71428571429,
    "c_base_eur_anno": 39952.94117647059,
    "c_alt_eur_anno": 17360.000000000004,
    "risparmio_eur_anno": 22592.941176470584,
    "capex_eur": 82200.0,
    "co2_base_t_anno": 56.11764705882353,
    "co2_alt_t_anno": 23.284,
    "co2_evitata_t_anno": 32.83364705882353,
    "van": 152307.00348849414,
    "tir": 26.695199925893732,
    "payback": 4,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh853_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh853_num(3, "x"), 3.0)
        self.assertEqual(mh853_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh853_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh853_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh853_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh853_pos(0, "x")
        with self.assertRaises(ValueError):
            mh853_pos(-1, "x")
        self.assertEqual(mh853_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh853_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh853_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh853_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh853_int_pos(15, "x"), 15)
        self.assertEqual(mh853_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh853_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh853_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh853_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh853_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh853_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh853_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_e_oss_base_e_alt(self):
        self.assertEqual(mh853_e_oss_base(50000, 2.0), 100000.0)
        self.assertEqual(mh853_e_oss_alt(50000, 1.2), 60000.0)
        with self.assertRaises(ValueError):
            mh853_e_oss_base(0, 2.0)
        with self.assertRaises(ValueError):
            mh853_e_oss_alt(50000, 0.0)

    def test_q_acqua_base_e_alt(self):
        self.assertEqual(mh853_q_acqua_base(500, 120), 60000.0)
        self.assertEqual(mh853_q_acqua_alt(500, 90), 45000.0)

    def test_q_rec_sull_acqua_alt_non_sulla_base(self):
        # 20% di 45.000 (alt), non di 60.000 (base):
        # 9.000, non 12.000.
        self.assertEqual(mh853_q_rec(45000.0, 0.20), 9000.0)
        self.assertNotEqual(mh853_q_rec(45000.0, 0.20),
                            0.20 * 60000.0)
        self.assertEqual(mh853_q_rec(45000.0, 0.0), 0.0)

    def test_q_net(self):
        self.assertEqual(mh853_q_net(45000.0, 9000.0), 36000.0)
        self.assertEqual(mh853_q_net(45000.0, 45000.0), 0.0)

    def test_gas_base_e_alt_zero(self):
        self.assertAlmostEqual(mh853_gas_base(60000.0, 0.85),
                               70588.2353, places=2)
        self.assertEqual(mh853_gas_alt(), 0.0)

    def test_e_pdc(self):
        self.assertAlmostEqual(mh853_e_pdc(36000.0, 3.5),
                               10285.7143, places=2)
        with self.assertRaises(ValueError):
            mh853_e_pdc(100.0, 0.0)

    def test_e_base_e_alt(self):
        self.assertEqual(mh853_e_base_el(100000.0, 20000.0), 120000.0)
        self.assertAlmostEqual(
            mh853_e_alt_el(60000.0, 20000.0, 10285.7143),
            90285.7143, places=2)

    def test_p_pv_ed_e_pv(self):
        self.assertEqual(mh853_p_pv_kwp(400, 0.50, 0.18), 36.0)
        self.assertEqual(mh853_e_pv(36.0, 1100), 39600.0)
        self.assertEqual(mh853_p_pv_kwp(400, 0.0, 0.18), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh853_e_pv_auto(39600.0, 0.60, 90285.7143),
                         23760.0)
        self.assertEqual(mh853_e_pv_auto(200000.0, 0.60, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh853_e_immessa(39600.0, 23760.0), 15840.0)
        self.assertAlmostEqual(mh853_e_deficit(90285.7143, 23760.0),
                               66525.7143, places=2)
        self.assertEqual(mh853_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh853_c_base(120000.0, 0.28, 70588.2353, 0.09)
        self.assertAlmostEqual(cb, 39952.9412, places=2)
        ca = mh853_c_alt(66525.7143, 0.28, 15840.0, 0.08)
        self.assertAlmostEqual(ca, 17360.0, places=2)
        self.assertAlmostEqual(mh853_risparmio(cb, ca), 22592.9412,
                               places=2)

    def test_co2_con_divisione_per_mille(self):
        # Fattori in kg/kWh: divisione per 1000 in
        # questa scheda, a differenza delle schede
        # con fattori diretti in t/kWh.
        cb = mh853_co2_base(120000.0, 0.35, 70588.2353, 0.20)
        self.assertAlmostEqual(cb, 56.1176, places=2)
        ca = mh853_co2_alt(66525.7143, 0.35)
        self.assertAlmostEqual(ca, 23.284, places=2)
        self.assertAlmostEqual(mh853_co2_evitata(cb, ca), 32.8336,
                               places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh853_flussi(82200, 22592.9412, 3),
                         [-82200, 22592.9412, 22592.9412, 22592.9412])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh853_van([-100, 60, 60], 0), 20.0)
        bc = mh853_demo_calcoli()
        self.assertAlmostEqual(mh853_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh853_demo_calcoli()
        tir = mh853_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh853_tir([-100, -10, -10]))
        self.assertIsNone(mh853_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh853_demo_calcoli()
        self.assertEqual(mh853_payback(bc["flussi"]), 4)
        self.assertIsNone(mh853_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh853_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh853_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh853_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh853_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh853_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh853_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh853_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh853_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none_e_segno(self):
        bc = mh853_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh853_p_el_pareggio(
            bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.08,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]))
        grezzo = (-bc["gas_base_kwh_anno"] * 0.09
                  - bc["e_immessa_kwh_e_anno"] * 0.08) / (
                      bc["e_base_el_kwh_e_anno"]
                      - bc["e_deficit_kwh_e_anno"])
        self.assertAlmostEqual(grezzo, -0.1425010371748614, places=12)
        self.assertLess(grezzo, 0.0)

    def test_p_el_pareggio_denominatore_non_positivo(self):
        self.assertIsNone(mh853_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 100.0))
        self.assertIsNone(mh853_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 150.0))

    def test_p_el_pareggio_caso_limite_zero(self):
        # Solo nel caso limite gas zero e immessa
        # zero il pareggio vale 0 (non negativo):
        # e' l'unico caso in cui non e' None.
        self.assertEqual(mh853_p_el_pareggio(
            0.0, 0.09, 0.0, 0.08, 120000.0, 10000.0), 0.0)

    def test_valida_demo_ok(self):
        demo = mh853_demo()
        val = mh853_valida(*[demo[k] for k in (
            "kg_pesce_anno", "volume_vasche_m3", "sup_copertura_m2",
            "quota_fv", "kwh_per_kg_base", "kwh_per_kg_alt",
            "e_altre", "q_acqua_per_m3_base",
            "q_acqua_per_m3_alt", "f_recupero", "cop_pdc",
            "eta_caldaia", "kwp_per_m2", "resa_fv",
            "f_autoconsumo", "p_el", "p_gas", "p_immissione",
            "capex", "f_el", "f_gas", "wacc", "vita",
            "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_kg_zero_no(self):
        kw = _demo_kwargs(kg_pesce_anno=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_superfici_zero_no(self):
        kw = _demo_kwargs(volume_vasche_m3=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)
        kw = _demo_kwargs(sup_copertura_m2=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)
        kw = _demo_kwargs(kwh_per_kg_base=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)
        kw = _demo_kwargs(q_acqua_per_m3_alt=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh853_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh853_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh853_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_altre", -1),
                              ("p_gas", -0.01),
                              ("capex", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh853_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh853_calcola(mh853_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh853_calcola(dict(mh853_demo(), capex=999999), capex=82200)
        self.assertEqual(bc["capex_eur"], 82200.0)


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
            bc["q_acqua_alt_kwh_th_anno"],
            bc["q_rec_kwh_th_anno"] + bc["q_net_kwh_th_anno"])
        self.assertAlmostEqual(
            bc["e_base_el_kwh_e_anno"],
            bc["e_oss_base_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_oss_alt_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"]
            + bc["e_pdc_kwh_e_anno"])
        self.assertLessEqual(bc["q_rec_kwh_th_anno"],
                             bc["q_acqua_alt_kwh_th_anno"])

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
        s = mh853_sensibilita(**mh853_demo())
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               19598.38, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               25587.50, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], 70100.11, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               21872.94, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], 70107.00, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"], 92256.70, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 256694.12, places=2)

    def test_marginale_con_capex_alto(self):
        # CAPEX 250.000: VAN negativa entro la
        # tolleranza del 10% di 250.000.
        bc = mh853_calcola(**_demo_kwargs(capex=250000))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_280k(self):
        bc = mh853_calcola(**_demo_kwargs(capex=280000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh853_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh853_csv(bc, mh853_demo())
        for voce in ("kg_pesce_anno", "e_oss_base_kwh_e_anno",
                     "q_rec_kwh_th_anno", "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -82200.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, caldaia a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Calore recuperato dall'acqua (kWh_th/anno)",
                      voci)

    def test_recupero_zero_con_f_recupero_zero(self):
        self.assertEqual(mh853_q_rec(45000.0, 0.0), 0.0)

    def test_e_oss_scala_lineare_con_kg(self):
        self.assertAlmostEqual(mh853_e_oss_base(2000.0, 2.0),
                               2.0 * mh853_e_oss_base(1000.0, 2.0))

    def test_co2_alt_senza_credito_immessa(self):
        # L'energia immessa non sottrae CO2: a parita' di
        # deficit, la CO2 alternativa non cambia.
        self.assertEqual(mh853_co2_alt(20000.0, 0.35),
                         20000.0 * 0.35 / 1000.0)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh853_c_alt(20000.0, 0.28, 0.0, 0.08, )
        con = mh853_c_alt(20000.0, 0.28, 10000.0, 0.08)
        self.assertAlmostEqual(senza - con, 800.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh853_sensibilita(**mh853_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh853_csv(bc, mh853_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_oss_base_kwh_e_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh853_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh853_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh853_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        bc = mh853_calcola(**_demo_kwargs(e_altre=0))
        self.assertEqual(bc["e_altre_kwh_e_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def853\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh853_demo().keys()), lette - set(mh853_demo().keys()))
        self.assertEqual(lette, set(mh853_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc853\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc853\["([^"]+)"\]', src))
        attese = set(mh853_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab853:"), 1)
        self.assertTrue(src.startswith("    # W857"))

    def test_ui_tab853_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab853:"), 1)
        self.assertIn("def mh853_demo(", src_h)
        self.assertIn("def mh853_calcola(", src_h)
        self.assertIn("tab853", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Acquacoltura: pompe e ossigenatori efficienti + recupero calore + pompa di calore + FV battono caldaia a gas + pompaggio tradizionale?", src)
        self.assertIn("🐟 Acquacoltura: pompe e ossigenatori efficienti + recupero calore + pompa di calore + FV battono caldaia a gas + pompaggio tradizionale?", src)
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
        chiavi = re.findall(r'key="(st853_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st853_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st853_calcola"', src)
        self.assertIn('key="st853_csv"', src)
        self.assertIn('key="st853_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg853"), src.index(".paiac("))
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
