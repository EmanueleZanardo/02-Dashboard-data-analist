"""Test nuova scheda surgelati: surgelazione
rapida + celle frigorifere efficienti +
recupero calore + pompa di calore + FV
battono caldaia a gas + freddo
tradizionale?

Business case annuo di un impianto di
produzione e stoccaggio di surgelati,
connesso alla rete, guidato dalle
TONNELLATE DI PRODOTTO SURGELATO
ALL'ANNO + VOLUME CELLE FRIGORIFERE
(m3) + SUPERFICIE COPERTURA (m2) (non
acquacoltura, non salumificio, non
macelleria, non frigorifero industriale
generico):
E_surg_base = t x kwh_per_t_base;
E_surg_alt = t x kwh_per_t_alt
(efficiente, minore); E_celle_base =
volume x kwh_per_m3_base; E_celle_alt =
volume x kwh_per_m3_alt (efficienti,
minore); E_base_el = E_surg_base +
E_celle_base + altre; E_alt_el =
E_surg_alt + E_celle_alt + altre + E_pdc;
Q_term_base = t x q_term_per_t_base;
Q_term_alt = t x q_term_per_t_alt;
Q_rec = f_recupero x Q_term_alt (30%
del termico ALTERNATIVO, non della
base); Q_net = max(0, Q_term_alt -
Q_rec); Gas_base = Q_term_base /
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
forfettario 420.000 (FV 216.000 + PdC
45.000 + recupero 30.000 + surgelatore e
celle delta 129.000); CO2 base =
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
e' -0,11226225143522756 EUR/kWh, quindi
None: il numeratore e' negativo
(-31.747,76 EUR/anno circa: gas evitato
25.411,76 piu' ricavo da immissione
6.336,00; denominatore 282.800,00
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
degenere (t <= 0, volume <= 0,
copertura <= 0, quota fv < 0 o > 1, kwh
per t base <= 0, kwh per t alt <= 0,
kwh per m3 base <= 0, kwh per m3 alt
<= 0, altre < 0, q term per t base <= 0,
q term per t alt <= 0, f_recupero < 0
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
    from w858_helpers import (
        demo_calcoli,
        mh854_c_alt,
        mh854_c_base,
        mh854_calcola,
        mh854_co2_alt,
        mh854_co2_base,
        mh854_co2_evitata,
        mh854_csv,
        mh854_demo,
        mh854_demo_calcoli,
        mh854_e_alt_el,
        mh854_e_base_el,
        mh854_e_celle_alt,
        mh854_e_celle_base,
        mh854_e_deficit,
        mh854_e_immessa,
        mh854_e_pdc,
        mh854_e_pv,
        mh854_e_pv_auto,
        mh854_e_surg_alt,
        mh854_e_surg_base,
        mh854_eta,
        mh854_flussi,
        mh854_frazione,
        mh854_gas_alt,
        mh854_gas_base,
        mh854_int_pos,
        mh854_nneg,
        mh854_num,
        mh854_p_el_pareggio,
        mh854_p_pv_kwp,
        mh854_payback,
        mh854_pos,
        mh854_q_net,
        mh854_q_rec,
        mh854_q_term_alt,
        mh854_q_term_base,
        mh854_risparmio,
        mh854_sensibilita,
        mh854_tir,
        mh854_valida,
        mh854_van,
        mh854_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w858_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w858_helpers", os.path.join(_hf, "w858_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh854_c_alt = _mod.mh854_c_alt
    mh854_c_base = _mod.mh854_c_base
    mh854_calcola = _mod.mh854_calcola
    mh854_co2_alt = _mod.mh854_co2_alt
    mh854_co2_base = _mod.mh854_co2_base
    mh854_co2_evitata = _mod.mh854_co2_evitata
    mh854_csv = _mod.mh854_csv
    mh854_demo = _mod.mh854_demo
    mh854_demo_calcoli = _mod.mh854_demo_calcoli
    mh854_e_alt_el = _mod.mh854_e_alt_el
    mh854_e_base_el = _mod.mh854_e_base_el
    mh854_e_celle_alt = _mod.mh854_e_celle_alt
    mh854_e_celle_base = _mod.mh854_e_celle_base
    mh854_e_deficit = _mod.mh854_e_deficit
    mh854_e_immessa = _mod.mh854_e_immessa
    mh854_e_pdc = _mod.mh854_e_pdc
    mh854_e_pv = _mod.mh854_e_pv
    mh854_e_pv_auto = _mod.mh854_e_pv_auto
    mh854_e_surg_alt = _mod.mh854_e_surg_alt
    mh854_e_surg_base = _mod.mh854_e_surg_base
    mh854_eta = _mod.mh854_eta
    mh854_flussi = _mod.mh854_flussi
    mh854_frazione = _mod.mh854_frazione
    mh854_gas_alt = _mod.mh854_gas_alt
    mh854_gas_base = _mod.mh854_gas_base
    mh854_int_pos = _mod.mh854_int_pos
    mh854_nneg = _mod.mh854_nneg
    mh854_num = _mod.mh854_num
    mh854_p_el_pareggio = _mod.mh854_p_el_pareggio
    mh854_p_pv_kwp = _mod.mh854_p_pv_kwp
    mh854_payback = _mod.mh854_payback
    mh854_pos = _mod.mh854_pos
    mh854_q_net = _mod.mh854_q_net
    mh854_q_rec = _mod.mh854_q_rec
    mh854_q_term_alt = _mod.mh854_q_term_alt
    mh854_q_term_base = _mod.mh854_q_term_base
    mh854_risparmio = _mod.mh854_risparmio
    mh854_sensibilita = _mod.mh854_sensibilita
    mh854_tir = _mod.mh854_tir
    mh854_valida = _mod.mh854_valida
    mh854_van = _mod.mh854_van
    mh854_verdetto = _mod.mh854_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w858_helpers.py")
_UI_PATH = _risolvi("w858_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "3"
_VECCHIO_TAB = "tab85" + "3"
_VECCHIO_ST = "st85" + "3_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "e_surg_base_kwh_e_anno": 500000.0,
    "e_surg_alt_kwh_e_anno": 360000.0,
    "e_celle_base_kwh_e_anno": 240000.0,
    "e_celle_alt_kwh_e_anno": 180000.0,
    "e_altre_kwh_e_anno": 50000.0,
    "e_base_el_kwh_e_anno": 790000.0,
    "e_alt_el_kwh_e_anno": 626000.0,
    "q_term_base_kwh_th_anno": 240000.0,
    "q_term_alt_kwh_th_anno": 180000.0,
    "q_rec_kwh_th_anno": 54000.0,
    "q_net_kwh_th_anno": 126000.0,
    "gas_base_kwh_anno": 282352.9411764706,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 36000.0,
    "p_pv_kwp": 180.0,
    "e_pv_kwh_e_anno": 198000.0,
    "e_pv_auto_kwh_e_anno": 118800.0,
    "e_immessa_kwh_e_anno": 79200.0,
    "e_deficit_kwh_e_anno": 507200.0,
    "c_base_eur_anno": 246611.76470588238,
    "c_alt_eur_anno": 135680.0,
    "risparmio_eur_anno": 110931.76470588238,
    "capex_eur": 420000.0,
    "co2_base_t_anno": 332.9705882352941,
    "co2_alt_t_anno": 177.52,
    "co2_evitata_t_anno": 155.45058823529408,
    "van": 731433.7832189698,
    "tir": 25.54135210528481,
    "payback": 4,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh854_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh854_num(3, "x"), 3.0)
        self.assertEqual(mh854_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh854_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh854_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh854_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh854_pos(0, "x")
        with self.assertRaises(ValueError):
            mh854_pos(-1, "x")
        self.assertEqual(mh854_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh854_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh854_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh854_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh854_int_pos(15, "x"), 15)
        self.assertEqual(mh854_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh854_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh854_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh854_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh854_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh854_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh854_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_e_surg_base_e_alt(self):
        self.assertEqual(mh854_e_surg_base(2000, 250), 500000.0)
        self.assertEqual(mh854_e_surg_alt(2000, 180), 360000.0)
        with self.assertRaises(ValueError):
            mh854_e_surg_base(0, 250)
        with self.assertRaises(ValueError):
            mh854_e_surg_alt(2000, 0.0)

    def test_e_celle_base_e_alt(self):
        self.assertEqual(mh854_e_celle_base(4000, 60), 240000.0)
        self.assertEqual(mh854_e_celle_alt(4000, 45), 180000.0)
        with self.assertRaises(ValueError):
            mh854_e_celle_base(0, 60)
        with self.assertRaises(ValueError):
            mh854_e_celle_alt(4000, 0.0)

    def test_q_term_base_e_alt(self):
        self.assertEqual(mh854_q_term_base(2000, 120), 240000.0)
        self.assertEqual(mh854_q_term_alt(2000, 90), 180000.0)

    def test_q_rec_sul_termico_alt_non_sulla_base(self):
        # 30% di 180.000 (alt), non di 240.000 (base):
        # 54.000, non 72.000.
        self.assertEqual(mh854_q_rec(180000.0, 0.30), 54000.0)
        self.assertNotEqual(mh854_q_rec(180000.0, 0.30),
                            0.30 * 240000.0)
        self.assertEqual(mh854_q_rec(180000.0, 0.0), 0.0)

    def test_q_net(self):
        self.assertEqual(mh854_q_net(180000.0, 54000.0), 126000.0)
        self.assertEqual(mh854_q_net(180000.0, 180000.0), 0.0)

    def test_gas_base_e_alt_zero(self):
        self.assertAlmostEqual(mh854_gas_base(240000.0, 0.85),
                               282352.9412, places=2)
        self.assertEqual(mh854_gas_alt(), 0.0)

    def test_e_pdc(self):
        self.assertAlmostEqual(mh854_e_pdc(126000.0, 3.5),
                               36000.0, places=2)
        with self.assertRaises(ValueError):
            mh854_e_pdc(100.0, 0.0)

    def test_e_base_e_alt(self):
        self.assertEqual(mh854_e_base_el(500000.0, 240000.0, 50000.0),
                         790000.0)
        self.assertEqual(mh854_e_alt_el(360000.0, 180000.0, 50000.0,
                                        36000.0), 626000.0)

    def test_p_pv_ed_e_pv(self):
        self.assertEqual(mh854_p_pv_kwp(2000, 0.50, 0.18), 180.0)
        self.assertEqual(mh854_e_pv(180.0, 1100), 198000.0)
        self.assertEqual(mh854_p_pv_kwp(2000, 0.0, 0.18), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh854_e_pv_auto(198000.0, 0.60, 626000.0),
                         118800.0)
        self.assertEqual(mh854_e_pv_auto(200000.0, 0.60, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh854_e_immessa(198000.0, 118800.0), 79200.0)
        self.assertEqual(mh854_e_deficit(626000.0, 118800.0), 507200.0)
        self.assertEqual(mh854_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh854_c_base(790000.0, 0.28, 282352.9412, 0.09)
        self.assertAlmostEqual(cb, 246611.7647, places=2)
        ca = mh854_c_alt(507200.0, 0.28, 79200.0, 0.08)
        self.assertAlmostEqual(ca, 135680.0, places=2)
        self.assertAlmostEqual(mh854_risparmio(cb, ca), 110931.7647,
                               places=2)

    def test_co2_con_divisione_per_mille(self):
        # Fattori in kg/kWh: divisione per 1000 in
        # questa scheda, a differenza delle schede
        # con fattori diretti in t/kWh.
        cb = mh854_co2_base(790000.0, 0.35, 282352.9412, 0.20)
        self.assertAlmostEqual(cb, 332.9706, places=2)
        ca = mh854_co2_alt(507200.0, 0.35)
        self.assertAlmostEqual(ca, 177.52, places=2)
        self.assertAlmostEqual(mh854_co2_evitata(cb, ca), 155.4506,
                               places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh854_flussi(420000, 110931.7647, 3),
                         [-420000, 110931.7647, 110931.7647, 110931.7647])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh854_van([-100, 60, 60], 0), 20.0)
        bc = mh854_demo_calcoli()
        self.assertAlmostEqual(mh854_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh854_demo_calcoli()
        tir = mh854_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh854_tir([-100, -10, -10]))
        self.assertIsNone(mh854_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh854_demo_calcoli()
        self.assertEqual(mh854_payback(bc["flussi"]), 4)
        self.assertIsNone(mh854_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh854_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh854_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh854_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh854_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh854_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh854_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh854_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh854_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_none_e_segno(self):
        bc = mh854_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh854_p_el_pareggio(
            bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.08,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]))
        grezzo = (-bc["gas_base_kwh_anno"] * 0.09
                  - bc["e_immessa_kwh_e_anno"] * 0.08) / (
                      bc["e_base_el_kwh_e_anno"]
                      - bc["e_deficit_kwh_e_anno"])
        self.assertAlmostEqual(grezzo, -0.11226225143522756, places=12)
        self.assertLess(grezzo, 0.0)

    def test_p_el_pareggio_denominatore_non_positivo(self):
        self.assertIsNone(mh854_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 100.0))
        self.assertIsNone(mh854_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 150.0))

    def test_p_el_pareggio_caso_limite_zero(self):
        # Solo nel caso limite gas zero e immessa
        # zero il pareggio vale 0 (non negativo):
        # e' l'unico caso in cui non e' None.
        self.assertEqual(mh854_p_el_pareggio(
            0.0, 0.09, 0.0, 0.08, 790000.0, 10000.0), 0.0)

    def test_valida_demo_ok(self):
        demo = mh854_demo()
        val = mh854_valida(*[demo[k] for k in (
            "t_surgelato_anno", "volume_celle_m3", "sup_copertura_m2",
            "quota_fv", "kwh_per_t_base", "kwh_per_t_alt",
            "kwh_per_m3_base", "kwh_per_m3_alt",
            "e_altre", "q_term_per_t_base",
            "q_term_per_t_alt", "f_recupero", "cop_pdc",
            "eta_caldaia", "kwp_per_m2", "resa_fv",
            "f_autoconsumo", "p_el", "p_gas", "p_immissione",
            "capex", "f_el", "f_gas", "wacc", "vita",
            "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_t_zero_no(self):
        kw = _demo_kwargs(t_surgelato_anno=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_superfici_zero_no(self):
        kw = _demo_kwargs(volume_celle_m3=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)
        kw = _demo_kwargs(sup_copertura_m2=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)
        kw = _demo_kwargs(kwh_per_t_base=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)
        kw = _demo_kwargs(kwh_per_m3_alt=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)
        kw = _demo_kwargs(q_term_per_t_alt=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh854_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh854_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh854_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_altre", -1),
                              ("p_gas", -0.01),
                              ("capex", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh854_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh854_calcola(mh854_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh854_calcola(dict(mh854_demo(), capex=999999), capex=420000)
        self.assertEqual(bc["capex_eur"], 420000.0)


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
            bc["q_term_alt_kwh_th_anno"],
            bc["q_rec_kwh_th_anno"] + bc["q_net_kwh_th_anno"])
        self.assertAlmostEqual(
            bc["e_base_el_kwh_e_anno"],
            bc["e_surg_base_kwh_e_anno"]
            + bc["e_celle_base_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"])
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            bc["e_surg_alt_kwh_e_anno"]
            + bc["e_celle_alt_kwh_e_anno"]
            + bc["e_altre_kwh_e_anno"]
            + bc["e_pdc_kwh_e_anno"])
        self.assertLessEqual(bc["q_rec_kwh_th_anno"],
                             bc["q_term_alt_kwh_th_anno"])

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
        s = mh854_sensibilita(**mh854_demo())
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               95094.96, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               126768.56, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], 320399.32, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               106611.76, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], 311433.78, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"], 436585.68, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 1243976.47, places=2)

    def test_marginale_con_capex_alto(self):
        # CAPEX 1.200.000: VAN negativa entro la
        # tolleranza del 10% di 1.200.000.
        bc = mh854_calcola(**_demo_kwargs(capex=1200000))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_alto(self):
        bc = mh854_calcola(**_demo_kwargs(capex=1300000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh854_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh854_csv(bc, mh854_demo())
        for voce in ("t_surgelato_anno", "e_surg_base_kwh_e_anno",
                     "e_celle_base_kwh_e_anno", "q_rec_kwh_th_anno",
                     "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -420000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, caldaia a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Calore recuperato dai condensatori (kWh_th/anno)",
                      voci)

    def test_recupero_zero_con_f_recupero_zero(self):
        self.assertEqual(mh854_q_rec(180000.0, 0.0), 0.0)

    def test_e_surg_scala_lineare_con_t(self):
        self.assertAlmostEqual(mh854_e_surg_base(2000.0, 250),
                               2.0 * mh854_e_surg_base(1000.0, 250))

    def test_co2_alt_senza_credito_immessa(self):
        # L'energia immessa non sottrae CO2: a parita' di
        # deficit, la CO2 alternativa non cambia.
        self.assertEqual(mh854_co2_alt(20000.0, 0.35),
                         20000.0 * 0.35 / 1000.0)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh854_c_alt(20000.0, 0.28, 0.0, 0.08, )
        con = mh854_c_alt(20000.0, 0.28, 10000.0, 0.08)
        self.assertAlmostEqual(senza - con, 800.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh854_sensibilita(**mh854_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh854_csv(bc, mh854_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_surg_base_kwh_e_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh854_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh854_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh854_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        bc = mh854_calcola(**_demo_kwargs(e_altre=0))
        self.assertEqual(bc["e_altre_kwh_e_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def854\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh854_demo().keys()), lette - set(mh854_demo().keys()))
        self.assertEqual(lette, set(mh854_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc854\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc854\["([^"]+)"\]', src))
        attese = set(mh854_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab854:"), 1)
        self.assertTrue(src.startswith("    # W858"))

    def test_ui_tab854_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab854:"), 1)
        self.assertIn("def mh854_demo(", src_h)
        self.assertIn("def mh854_calcola(", src_h)
        self.assertIn("tab854", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Surgelati: surgelazione rapida + celle frigorifere efficienti + recupero calore + pompa di calore + FV battono caldaia a gas + freddo tradizionale?", src)
        self.assertIn("❄️ Surgelati: surgelazione rapida + celle frigorifere efficienti + recupero calore + pompa di calore + FV battono caldaia a gas + freddo tradizionale?", src)
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
        chiavi = re.findall(r'key="(st854_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st854_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st854_calcola"', src)
        self.assertIn('key="st854_csv"', src)
        self.assertIn('key="st854_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg854"), src.index(".paiac("))
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
