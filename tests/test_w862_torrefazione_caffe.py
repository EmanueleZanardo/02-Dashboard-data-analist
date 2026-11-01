"""Test nuova scheda torrefazione caffe:
tostatore elettrico + recupero fumi + FV
batte il tostatore a gas?

Business case annuo di un impianto di
torrefazione caffe, connesso alla rete,
guidato dai KG DI CAFFE VERDE TOSTATI
ALL'ANNO + SUPERFICIE TETTO (m2) + QUOTA
FV (non torrefazione di biomassa/pellet
della tab719, non bar/caffetteria, non
panificio): Q_term_base = kg x
q_tost_base; Gas_base = Q_term_base /
eta_gas; Gas_alt = 0 (il tostatore a gas
SCOMPARE: la tostatura e' elettrica);
E_base_el = kg x (e_aus_base +
e_raff_conf_base) + e_altri_base;
E_alt_el = kg x (e_tost_alt +
e_raff_conf_alt) + e_altri_alt, dove
e_tost_alt e' la tostatura elettrica
NETTA, gia' al netto del recupero fumi;
kWp tetto = sup_tetto x quota_fv x
kwp_per_m2; E_pv = kWp x resa_fv;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt_el) (cappato alla domanda
elettrica alternativa); E_immessa = E_pv
- E_pv_auto; E_deficit = max(0, E_alt_el
- E_pv_auto); C_base = E_base_el x p_el
+ Gas_base x p_gas (nessun O&M); C_alt =
E_deficit x p_el - E_immessa x
p_immissione (gas alternativo zero;
l'immessa e' un RICAVO a prezzo di
immissione, INFERIORE a p_el; nessun
credito CO2 per l'immessa); risparmio =
C_base - C_alt; CAPEX totale =
capex_tostatore + capex_recupero + kWp x
capex_fv_per_kwp (demo 231.840); CO2 base
= (E_base_el x f_el + Gas_base x f_gas) /
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
denominatore nullo o se p_star < 0.
In questa scheda il denominatore e'
NEGATIVO (deficit 103.088 > domanda base
90.000) e il numeratore e' NEGATIVO
(-25.520,64), quindi p_star e' POSITIVO:
1,949926650366748 EUR/kWh, SOGLIA
MASSIMA sui soli costi annui (il CAPEX
non entra nel pareggio annuo): sotto di
essa l'alternativa vince, sopra perde.
Verdetto: NON_CALCOLABILE se input
degenere (kg <= 0, q_tost_base < 0,
eta_gas <= 0 o > 1, per-kg < 0, altri usi
< 0, sup tetto <= 0, quota fv < 0 o > 1,
kwp per m2 < 0, resa fv < 0,
f_autoconsumo < 0 o > 1, prezzi < 0,
CAPEX voci < 0, f_el < 0, f_gas < 0,
WACC < 0, vita <= 0 o non intera,
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
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w862_helpers import (
        demo_calcoli,
        mh858_c_alt,
        mh858_c_base,
        mh858_calcola,
        mh858_capex_totale,
        mh858_co2_alt,
        mh858_co2_base,
        mh858_co2_evitata,
        mh858_csv,
        mh858_demo,
        mh858_demo_calcoli,
        mh858_e_alt_el,
        mh858_e_base_el,
        mh858_e_deficit,
        mh858_e_immessa,
        mh858_e_pv,
        mh858_e_pv_auto,
        mh858_eta,
        mh858_flussi,
        mh858_frazione,
        mh858_gas_alt,
        mh858_gas_base,
        mh858_int_pos,
        mh858_nneg,
        mh858_num,
        mh858_p_el_pareggio,
        mh858_p_pv_kwp,
        mh858_payback,
        mh858_pos,
        mh858_q_term_base,
        mh858_risparmio,
        mh858_sensibilita,
        mh858_tir,
        mh858_valida,
        mh858_van,
        mh858_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w862_helpers", os.path.join(_hf, "w862_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh858_c_alt = _mod.mh858_c_alt
    mh858_c_base = _mod.mh858_c_base
    mh858_calcola = _mod.mh858_calcola
    mh858_capex_totale = _mod.mh858_capex_totale
    mh858_co2_alt = _mod.mh858_co2_alt
    mh858_co2_base = _mod.mh858_co2_base
    mh858_co2_evitata = _mod.mh858_co2_evitata
    mh858_csv = _mod.mh858_csv
    mh858_demo = _mod.mh858_demo
    mh858_demo_calcoli = _mod.mh858_demo_calcoli
    mh858_e_alt_el = _mod.mh858_e_alt_el
    mh858_e_base_el = _mod.mh858_e_base_el
    mh858_e_deficit = _mod.mh858_e_deficit
    mh858_e_immessa = _mod.mh858_e_immessa
    mh858_e_pv = _mod.mh858_e_pv
    mh858_e_pv_auto = _mod.mh858_e_pv_auto
    mh858_eta = _mod.mh858_eta
    mh858_flussi = _mod.mh858_flussi
    mh858_frazione = _mod.mh858_frazione
    mh858_gas_alt = _mod.mh858_gas_alt
    mh858_gas_base = _mod.mh858_gas_base
    mh858_int_pos = _mod.mh858_int_pos
    mh858_nneg = _mod.mh858_nneg
    mh858_num = _mod.mh858_num
    mh858_p_el_pareggio = _mod.mh858_p_el_pareggio
    mh858_p_pv_kwp = _mod.mh858_p_pv_kwp
    mh858_payback = _mod.mh858_payback
    mh858_pos = _mod.mh858_pos
    mh858_q_term_base = _mod.mh858_q_term_base
    mh858_risparmio = _mod.mh858_risparmio
    mh858_sensibilita = _mod.mh858_sensibilita
    mh858_tir = _mod.mh858_tir
    mh858_valida = _mod.mh858_valida
    mh858_van = _mod.mh858_van
    mh858_verdetto = _mod.mh858_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w862_helpers.py")
_UI_PATH = _risolvi("w862_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "7"
_VECCHIO_TAB = "tab85" + "7"
_VECCHIO_ST = "st85" + "7_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "q_term_base_kwh_th_anno": 240000.0,
    "gas_base_kwh_anno": 266666.6666666667,
    "gas_alt_kwh_anno": 0.0,
    "e_base_el_kwh_e_anno": 90000.0,
    "e_alt_el_kwh_e_anno": 131600.0,
    "p_pv_kwp": 43.2,
    "e_pv_kwh_e_anno": 47520.0,
    "e_pv_auto_kwh_e_anno": 28512.0,
    "e_immessa_kwh_e_anno": 19008.0,
    "e_deficit_kwh_e_anno": 103088.0,
    "c_base_eur_anno": 49200.0,
    "c_alt_eur_anno": 27344.0,
    "risparmio_eur_anno": 21856.0,
    "capex_eur": 231840.0,
    "co2_base_t_anno": 84.83333333333334,
    "co2_alt_t_anno": 36.0808,
    "co2_evitata_t_anno": 48.752533333333346,
    "van": 40534.06924655381,
    "tir": 6.983500440920178,
    "payback": 11,
    "p_el_pareggio": 1.949926650366748,
}


def _demo_kwargs(**over):
    kw = dict(mh858_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh858_num(3, "x"), 3.0)
        self.assertEqual(mh858_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh858_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh858_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh858_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh858_pos(0, "x")
        with self.assertRaises(ValueError):
            mh858_pos(-1, "x")
        self.assertEqual(mh858_pos(2, "x"), 2.0)

    def test_eta_intervallo(self):
        self.assertEqual(mh858_eta(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh858_eta(0.0, "x")
        with self.assertRaises(ValueError):
            mh858_eta(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh858_int_pos(15, "x"), 15)
        self.assertEqual(mh858_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh858_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh858_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh858_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh858_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh858_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh858_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_q_term_base_e_gas(self):
        self.assertEqual(mh858_q_term_base(120000, 2.0), 240000.0)
        self.assertAlmostEqual(mh858_gas_base(240000.0, 0.9),
                               266666.6667, places=2)
        self.assertEqual(mh858_gas_alt(), 0.0)
        with self.assertRaises(ValueError):
            mh858_q_term_base(0, 2.0)

    def test_e_base_e_alt(self):
        self.assertEqual(mh858_e_base_el(120000, 0.25, 0.35, 18000),
                         90000.0)
        self.assertEqual(mh858_e_alt_el(120000, 0.70, 0.28, 14000),
                         131600.0)

    def test_tostatura_netta_non_sottratta_due_volte(self):
        # La tostatura netta 0,70 e' gia' al netto del
        # recupero fumi: la domanda alt usa 0,70, non
        # 0,70 meno un altro recupero.
        self.assertEqual(mh858_e_alt_el(120000, 0.70, 0.28, 14000),
                         120000 * 0.70 + 120000 * 0.28 + 14000)

    def test_p_pv_ed_e_pv(self):
        self.assertAlmostEqual(mh858_p_pv_kwp(400, 0.60, 0.18), 43.2)
        self.assertAlmostEqual(mh858_e_pv(43.2, 1100), 47520.0)
        self.assertEqual(mh858_p_pv_kwp(400, 0.0, 0.18), 0.0)

    def test_pv_auto_cappato_alla_domanda(self):
        self.assertEqual(mh858_e_pv_auto(47520.0, 0.60, 131600.0),
                         28512.0)
        self.assertEqual(mh858_e_pv_auto(200000.0, 0.60, 10000.0),
                         10000.0)

    def test_immessa_e_deficit(self):
        self.assertEqual(mh858_e_immessa(47520.0, 28512.0), 19008.0)
        self.assertEqual(mh858_e_deficit(131600.0, 28512.0), 103088.0)
        self.assertEqual(mh858_e_deficit(100.0, 150.0), 0.0)

    def test_c_base_c_alt_risparmio(self):
        cb = mh858_c_base(90000.0, 0.28, 266666.6667, 0.09)
        self.assertAlmostEqual(cb, 49200.0, places=2)
        ca = mh858_c_alt(103088.0, 0.28, 19008.0, 0.08)
        self.assertAlmostEqual(ca, 27344.0, places=2)
        self.assertAlmostEqual(mh858_risparmio(cb, ca), 21856.0,
                               places=2)

    def test_capex_totale_voci_piu_kwp(self):
        self.assertEqual(mh858_capex_totale(150000, 30000, 43.2, 1200),
                         231840.0)

    def test_co2_con_divisione_per_mille(self):
        cb = mh858_co2_base(90000.0, 0.35, 266666.6667, 0.20)
        self.assertAlmostEqual(cb, 84.8333, places=2)
        ca = mh858_co2_alt(103088.0, 0.35)
        self.assertAlmostEqual(ca, 36.0808, places=2)
        self.assertAlmostEqual(mh858_co2_evitata(cb, ca), 48.7525,
                               places=2)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh858_flussi(231840, 21856, 3),
                         [-231840, 21856, 21856, 21856])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh858_van([-100, 60, 60], 0), 20.0)
        bc = mh858_demo_calcoli()
        self.assertAlmostEqual(mh858_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh858_demo_calcoli()
        tir = mh858_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh858_tir([-100, -10, -10]))
        self.assertIsNone(mh858_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh858_demo_calcoli()
        self.assertEqual(mh858_payback(bc["flussi"]), 11)
        self.assertIsNone(mh858_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh858_payback([-100, 100, 10]), 1)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh858_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh858_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh858_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh858_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh858_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh858_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh858_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_el_pareggio_demo_soglia_massima(self):
        bc = mh858_demo_calcoli()
        self.assertAlmostEqual(bc["p_el_pareggio"],
                               1.949926650366748, places=12)
        self.assertAlmostEqual(mh858_p_el_pareggio(
            bc["gas_base_kwh_anno"], 0.09,
            bc["e_immessa_kwh_e_anno"], 0.08,
            bc["e_base_el_kwh_e_anno"], bc["e_deficit_kwh_e_anno"]),
            1.949926650366748, places=12)
        # Soglia MASSIMA: sotto vince l'alternativa, sopra
        # perde, perche' il deficit supera la domanda base.
        self.assertGreater(bc["e_deficit_kwh_e_anno"],
                           bc["e_base_el_kwh_e_anno"])

    def test_p_el_pareggio_denominatore_nullo(self):
        self.assertIsNone(mh858_p_el_pareggio(
            1000.0, 0.09, 0.0, 0.08, 100.0, 100.0))

    def test_p_el_pareggio_negativo_none(self):
        # Denominatore positivo con numeratore negativo:
        # l'alternativa vince anche a prezzo nullo.
        self.assertIsNone(mh858_p_el_pareggio(
            1000.0, 0.09, 1000.0, 0.08, 120000.0, 10000.0))

    def test_p_el_pareggio_caso_limite_zero(self):
        self.assertEqual(mh858_p_el_pareggio(
            0.0, 0.09, 0.0, 0.08, 10000.0, 120000.0), 0.0)

    def test_valida_demo_ok(self):
        demo = mh858_demo()
        val = mh858_valida(*[demo[k] for k in (
            "kg_verde_anno", "q_tost_base", "eta_gas",
            "e_aus_base", "e_raff_conf_base", "e_altri_base",
            "e_tost_alt", "e_raff_conf_alt", "e_altri_alt",
            "sup_tetto_m2", "quota_fv", "kwp_per_m2", "resa_fv",
            "f_autoconsumo", "p_el", "p_gas", "p_immissione",
            "capex_tostatore", "capex_recupero",
            "capex_fv_per_kwp", "f_el", "f_gas", "wacc", "vita",
            "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_kg_zero_no(self):
        kw = _demo_kwargs(kg_verde_anno=0)
        self.assertRaises(ValueError, mh858_calcola, **kw)

    def test_valida_tetto_zero_no(self):
        kw = _demo_kwargs(sup_tetto_m2=0)
        self.assertRaises(ValueError, mh858_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh858_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh858_calcola, **kw)

    def test_valida_eta_sopra_uno_no(self):
        kw = _demo_kwargs(eta_gas=1.1)
        self.assertRaises(ValueError, mh858_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita=0)
        self.assertRaises(ValueError, mh858_calcola, **kw)
        kw = _demo_kwargs(vita=15.5)
        self.assertRaises(ValueError, mh858_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh858_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("e_altri_base", -1),
                              ("p_gas", -0.01),
                              ("capex_tostatore", -1),
                              ("wacc", -1),
                              ("tolleranza", -1)):
            with self.assertRaises(ValueError):
                mh858_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh858_calcola(mh858_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh858_calcola(dict(mh858_demo(), capex_tostatore=999999),
                           capex_tostatore=150000)
        self.assertEqual(bc["capex_eur"], 231840.0)


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
        self.assertEqual(bc["payback"], 11)

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
            bc["e_base_el_kwh_e_anno"],
            120000 * (0.25 + 0.35) + 18000)
        self.assertAlmostEqual(
            bc["e_alt_el_kwh_e_anno"],
            120000 * (0.70 + 0.28) + 14000)
        self.assertAlmostEqual(
            bc["q_term_base_kwh_th_anno"],
            bc["gas_base_kwh_anno"] * 0.9)

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
        s = mh858_sensibilita(**mh858_demo())
        # Qui il prezzo elettrico SU' peggiora il caso
        # (deficit > domanda base), al contrario delle
        # schede con deficit minore della base.
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               22588.93, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               21123.07, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"], -26066.78, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               11776.0, places=2)
        self.assertAlmostEqual(s["capex_doppio"]["van"], -191305.93, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"], -63073.76, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"], 205280.0, places=2)

    def test_marginale_con_capex_alto(self):
        # CAPEX totale 290.000 (tostatore 208.160):
        # VAN negativa entro la tolleranza del 10%.
        bc = mh858_calcola(**_demo_kwargs(capex_tostatore=208160))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_250k_tostatore(self):
        bc = mh858_calcola(**_demo_kwargs(capex_tostatore=250000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh858_calcola(**_demo_kwargs(p_gas=0.0, p_el=0.0,
                                          p_immissione=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh858_csv(bc, mh858_demo())
        for voce in ("kg_verde_anno", "e_base_el_kwh_e_anno",
                     "q_term_base_kwh_th_anno", "gas_alt_kwh_anno",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -231840.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Gas alternativo, tostatore a gas assente (kWh/anno)",
                      voci)
        self.assertIn("Tostatura elettrica netta alt (kWh_e/kg)",
                      voci)

    def test_e_base_scala_lineare_con_kg(self):
        self.assertAlmostEqual(mh858_e_base_el(2000.0, 0.25, 0.35, 0),
                               2.0 * mh858_e_base_el(1000.0, 0.25, 0.35, 0))

    def test_co2_alt_senza_credito_immessa(self):
        self.assertEqual(mh858_co2_alt(20000.0, 0.35),
                         20000.0 * 0.35 / 1000.0)

    def test_c_alt_immessa_e_ricavo(self):
        senza = mh858_c_alt(20000.0, 0.28, 0.0, 0.08)
        con = mh858_c_alt(20000.0, 0.28, 10000.0, 0.08)
        self.assertAlmostEqual(senza - con, 800.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh858_sensibilita(**mh858_demo())
        self.assertEqual(set(s.keys()),
                         {"p_el_meno20", "p_el_piu20", "senza_fv",
                          "senza_recupero", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh858_csv(bc, mh858_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_el_kwh_e_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh858_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh858_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh858_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        bc = mh858_calcola(**_demo_kwargs(e_altri_base=0))
        self.assertEqual(bc["e_altri_base"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def858\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh858_demo().keys()), lette - set(mh858_demo().keys()))
        self.assertEqual(lette, set(mh858_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc858\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc858\["([^"]+)"\]', src))
        attese = set(mh858_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab858:"), 1)
        self.assertTrue(src.startswith("    # W862"))

    def test_ui_tab858_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab858:"), 1)
        self.assertIn("def mh858_demo(", src_h)
        self.assertIn("def mh858_calcola(", src_h)
        self.assertIn("tab858", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Torrefazione caffè: tostatore elettrico + recupero fumi + FV batte il tostatore a gas?", src)
        self.assertIn("☕ Torrefazione caffè: tostatore elettrico + recupero fumi + FV batte il tostatore a gas?", src)
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
        chiavi = re.findall(r'key="(st858_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st858_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st858_calcola"', src)
        self.assertIn('key="st858_csv"', src)
        self.assertIn('key="st858_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg858"), src.index(".paiac("))
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
