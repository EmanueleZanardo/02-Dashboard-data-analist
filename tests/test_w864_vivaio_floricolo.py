"""Test nuova scheda vivaio floricolo: pompa
di calore + irrigazione efficiente + FV in
copertura battono caldaia a gas +
pompaggio tradizionale?

Business case annuo di un vivaio
floricolo, guidato dalla SUPERFICIE
DELLA SERRA (m2) e dalle PIANTE
PRODOTTE ALL'ANNO (non fioraio con
cella frigo, non mobilificio con pezzi
ed essiccazione, non orto da
autoconsumo): Q_term = sup x q_spec;
Gas_base = Q_term / eta_caldaia;
C_gas = Gas_base x p_gas; acqua_m3 =
piante x litri / 1000; E_pomp_base =
acqua x kwh_pomp_base; C_pomp_base =
E_pomp_base x p_el; C_base = somma;
E_pdc = Q_term / COP; E_pomp_alt =
acqua x kwh_pomp_alt; E_domanda_alt =
somma; kWp = sup x quota_fv x
kwp_per_m2; E_pv = kWp x resa;
E_pv_auto = min(E_pv x f_autoconsumo,
E_domanda_alt); E_immessa = E_pv -
E_pv_auto; E_deficit = max(0,
E_domanda_alt - E_pv_auto); C_alt =
deficit x p_el - immessa x
p_immissione; risparmio = C_base -
C_alt; CAPEX = capex_pdc +
capex_irrigazione + kWp x capex_fv
(demo 183.000); CO2 base = (gas x
0,20 + E_pomp_base x 0,25) / 1000; CO2
alt = deficit x 0,25 / 1000 (immessa
senza credito CO2); CO2 evitata =
base - alt (segno libero); flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo gas di
pareggio p_gas_star = (C_alt -
C_pomp_base) / Gas_base in forma
chiusa (demo 0,011844 EUR/kWh), None
se Gas_base nullo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui
soli costi annui (CAPEX escluso):
sopra di essa l'alternativa vince,
sotto perde.
Verdetto: NON_CALCOLABILE se input
degenere (sup <= 0 o non intera,
q_term_spec < 0, eta <= 0 o > 1,
piante <= 0 o non intere, litri < 0,
pompaggi < 0, prezzi < 0, COP <= 0,
quote < 0 o > 1, kwp_per_m2 < 0, resa
< 0, p_immissione < 0, voci CAPEX < 0,
fattori CO2 < 0, WACC < 0, vita <= 0 o
non intera, tolleranza < 0) o se
risparmio <= 0 (guard degenere: UI
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
    from w864_helpers import (
        demo_calcoli,
        mh860_acqua_m3,
        mh860_c_alt,
        mh860_c_base,
        mh860_c_gas,
        mh860_c_pomp_base,
        mh860_calcola,
        mh860_capex_totale,
        mh860_co2_alt,
        mh860_co2_base,
        mh860_co2_evitata,
        mh860_csv,
        mh860_demo,
        mh860_demo_calcoli,
        mh860_e_deficit,
        mh860_e_domanda_alt,
        mh860_e_immessa,
        mh860_e_pdc,
        mh860_e_pomp_alt,
        mh860_e_pomp_base,
        mh860_e_pv,
        mh860_e_pv_auto,
        mh860_flussi,
        mh860_frazione,
        mh860_gas_base,
        mh860_int_nneg,
        mh860_int_pos,
        mh860_kwp,
        mh860_nneg,
        mh860_num,
        mh860_p_gas_pareggio,
        mh860_payback,
        mh860_pos,
        mh860_q_term,
        mh860_rendimento,
        mh860_risparmio,
        mh860_sensibilita,
        mh860_tir,
        mh860_valida,
        mh860_van,
        mh860_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w864_helpers", os.path.join(_hf, "w864_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh860_acqua_m3 = _mod.mh860_acqua_m3
    mh860_c_alt = _mod.mh860_c_alt
    mh860_c_base = _mod.mh860_c_base
    mh860_c_gas = _mod.mh860_c_gas
    mh860_c_pomp_base = _mod.mh860_c_pomp_base
    mh860_calcola = _mod.mh860_calcola
    mh860_capex_totale = _mod.mh860_capex_totale
    mh860_co2_alt = _mod.mh860_co2_alt
    mh860_co2_base = _mod.mh860_co2_base
    mh860_co2_evitata = _mod.mh860_co2_evitata
    mh860_csv = _mod.mh860_csv
    mh860_demo = _mod.mh860_demo
    mh860_demo_calcoli = _mod.mh860_demo_calcoli
    mh860_e_deficit = _mod.mh860_e_deficit
    mh860_e_domanda_alt = _mod.mh860_e_domanda_alt
    mh860_e_immessa = _mod.mh860_e_immessa
    mh860_e_pdc = _mod.mh860_e_pdc
    mh860_e_pomp_alt = _mod.mh860_e_pomp_alt
    mh860_e_pomp_base = _mod.mh860_e_pomp_base
    mh860_e_pv = _mod.mh860_e_pv
    mh860_e_pv_auto = _mod.mh860_e_pv_auto
    mh860_flussi = _mod.mh860_flussi
    mh860_frazione = _mod.mh860_frazione
    mh860_gas_base = _mod.mh860_gas_base
    mh860_int_nneg = _mod.mh860_int_nneg
    mh860_int_pos = _mod.mh860_int_pos
    mh860_kwp = _mod.mh860_kwp
    mh860_nneg = _mod.mh860_nneg
    mh860_num = _mod.mh860_num
    mh860_p_gas_pareggio = _mod.mh860_p_gas_pareggio
    mh860_payback = _mod.mh860_payback
    mh860_pos = _mod.mh860_pos
    mh860_q_term = _mod.mh860_q_term
    mh860_rendimento = _mod.mh860_rendimento
    mh860_risparmio = _mod.mh860_risparmio
    mh860_sensibilita = _mod.mh860_sensibilita
    mh860_tir = _mod.mh860_tir
    mh860_valida = _mod.mh860_valida
    mh860_van = _mod.mh860_van
    mh860_verdetto = _mod.mh860_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w864_helpers.py")
_UI_PATH = _risolvi("w864_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "9"
_VECCHIO_TAB = "tab85" + "9"
_VECCHIO_ST = "st85" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "q_term_kwh_th_anno": 300000.0,
    "gas_base_kwh_anno": 333333.3333333333,
    "c_gas_eur_anno": 30000.0,
    "acqua_m3_anno": 3000.0,
    "e_pomp_base_kwh_anno": 2400.0,
    "c_pomp_base_eur_anno": 672.0,
    "c_base_eur_anno": 30672.0,
    "e_pdc_kwh_anno": 85714.28571428571,
    "e_pomp_alt_kwh_anno": 1500.0,
    "e_domanda_alt_kwh_anno": 87214.28571428571,
    "kwp": 90.0,
    "e_pv_kwh_anno": 99000.0,
    "e_pv_auto_kwh_anno": 59400.0,
    "e_immessa_kwh_anno": 39600.0,
    "e_deficit_kwh_anno": 27814.28571428571,
    "c_alt_eur_anno": 4620.0,
    "risparmio_eur_anno": 26052.0,
    "capex_eur": 183000.0,
    "co2_base_t_anno": 67.26666666666667,
    "co2_alt_t_anno": 6.953571428571427,
    "co2_evitata_t_anno": 60.31309523809524,
    "van": 87410.85121068072,
    "tir": 11.427296071464578,
    "payback": 8,
    "p_gas_pareggio": 0.011844,
}


def _demo_kwargs(**over):
    kw = dict(mh860_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh860_num(3, "x"), 3.0)
        self.assertEqual(mh860_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh860_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh860_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh860_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh860_pos(0, "x")
        with self.assertRaises(ValueError):
            mh860_pos(-1, "x")
        self.assertEqual(mh860_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh860_int_pos(15, "x"), 15)
        self.assertEqual(mh860_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh860_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh860_int_pos(15.5, "x")

    def test_int_nneg(self):
        self.assertEqual(mh860_int_nneg(0, "x"), 0)
        self.assertEqual(mh860_int_nneg(10, "x"), 10)
        with self.assertRaises(ValueError):
            mh860_int_nneg(-1, "x")
        with self.assertRaises(ValueError):
            mh860_int_nneg(2.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh860_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh860_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh860_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh860_frazione(1.1, "x")

    def test_rendimento_intervallo(self):
        self.assertEqual(mh860_rendimento(1.0, "x"), 1.0)
        self.assertEqual(mh860_rendimento(0.9, "x"), 0.9)
        with self.assertRaises(ValueError):
            mh860_rendimento(0.0, "x")
        with self.assertRaises(ValueError):
            mh860_rendimento(1.1, "x")
        with self.assertRaises(ValueError):
            mh860_rendimento(-0.5, "x")


class TestFisica(unittest.TestCase):
    def test_q_term_e_gas(self):
        self.assertEqual(mh860_q_term(2000, 150), 300000.0)
        self.assertAlmostEqual(mh860_gas_base(300000.0, 0.90),
                               333333.3333333333)
        with self.assertRaises(ValueError):
            mh860_q_term(0, 150)
        with self.assertRaises(ValueError):
            mh860_gas_base(300000.0, 0.0)

    def test_gas_e_costi_base(self):
        self.assertAlmostEqual(mh860_c_gas(333333.3333333333, 0.09),
                               30000.0)
        self.assertEqual(mh860_acqua_m3(120000, 25), 3000.0)
        self.assertEqual(mh860_e_pomp_base(3000.0, 0.8), 2400.0)
        self.assertAlmostEqual(mh860_c_pomp_base(2400.0, 0.28), 672.0)
        self.assertAlmostEqual(mh860_c_base(30000.0, 672.0), 30672.0)

    def test_pdc_pomp_alt_domanda(self):
        self.assertAlmostEqual(mh860_e_pdc(300000.0, 3.5),
                               85714.28571428571)
        self.assertEqual(mh860_e_pomp_alt(3000.0, 0.5), 1500.0)
        self.assertAlmostEqual(mh860_e_domanda_alt(85714.28571428571,
                                                   1500.0),
                               87214.28571428571)
        with self.assertRaises(ValueError):
            mh860_e_pdc(300000.0, 0.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh860_kwp(2000, 0.30, 0.15), 90.0)
        self.assertEqual(mh860_e_pv(90.0, 1100), 99000.0)
        self.assertEqual(mh860_e_pv_auto(99000.0, 0.60, 87214.28571428571),
                         59400.0)
        # Cap alla domanda: autoconsumo non supera la domanda.
        self.assertEqual(mh860_e_pv_auto(99000.0, 1.0, 50000.0), 50000.0)
        self.assertEqual(mh860_e_immessa(99000.0, 59400.0), 39600.0)
        self.assertAlmostEqual(mh860_e_deficit(87214.28571428571, 59400.0),
                               27814.28571428571)
        self.assertEqual(mh860_e_deficit(50000.0, 60000.0), 0.0)

    def test_c_alt_con_ricavo_immissione(self):
        self.assertAlmostEqual(mh860_c_alt(27814.28571428571, 0.28,
                                           39600.0, 0.08), 4620.0)
        self.assertAlmostEqual(
            mh860_risparmio(30672.0, 4620.0), 26052.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh860_capex_totale(60000, 15000, 90.0, 1200),
                         183000.0)
        self.assertEqual(mh860_capex_totale(60000, 15000, 0.0, 1200),
                         75000.0)

    def test_co2_con_divisione_per_mille_senza_credito_immessa(self):
        cb = mh860_co2_base(333333.3333333333, 0.20, 2400.0, 0.25)
        self.assertAlmostEqual(cb, 67.26666666666667, places=4)
        ca = mh860_co2_alt(27814.28571428571, 0.25)
        self.assertAlmostEqual(ca, 6.953571428571427, places=4)
        self.assertAlmostEqual(mh860_co2_evitata(cb, ca),
                               60.31309523809524, places=4)
        # L'immessa non sottrae CO2: alt conta solo il deficit.
        self.assertEqual(mh860_co2_alt(0.0, 0.25), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh860_flussi(183000, 26052.0, 3),
                         [-183000, 26052.0, 26052.0, 26052.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh860_van([-100, 60, 60], 0), 20.0)
        bc = mh860_demo_calcoli()
        self.assertAlmostEqual(mh860_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh860_demo_calcoli()
        tir = mh860_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh860_tir([-100, -10, -10]))
        self.assertIsNone(mh860_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh860_demo_calcoli()
        self.assertEqual(mh860_payback(bc["flussi"]), 8)
        self.assertIsNone(mh860_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh860_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh860_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:8]), -636.0, places=2)
        self.assertAlmostEqual(sum(flussi[:9]), 25416.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh860_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh860_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh860_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh860_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh860_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh860_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh860_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_soglia_minima(self):
        bc = mh860_demo_calcoli()
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.011844, places=12)
        self.assertAlmostEqual(mh860_p_gas_pareggio(
            bc["c_alt_eur_anno"], bc["c_pomp_base_eur_anno"],
            bc["gas_base_kwh_anno"]),
            0.011844, places=12)
        # Soglia MINIMA: sopra vince, sotto perde.
        self.assertGreater(bc["p_gas"], bc["p_gas_pareggio"])
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_gas_nullo_none(self):
        self.assertIsNone(mh860_p_gas_pareggio(4620.0, 672.0, 0.0))

    def test_p_gas_pareggio_negativo_none(self):
        # Costo alternativo sotto il pompaggio base: il rapporto
        # e' negativo, l'alternativa vince anche a gas gratuito.
        self.assertIsNone(mh860_p_gas_pareggio(100.0, 672.0,
                                              333333.3333333333))

    def test_p_gas_pareggio_caso_limite_zero(self):
        self.assertEqual(mh860_p_gas_pareggio(672.0, 672.0,
                                             333333.3333333333), 0.0)

    def test_valida_demo_ok(self):
        demo = mh860_demo()
        val = mh860_valida(*[demo[k] for k in (
            "sup_serra_m2", "q_term_spec_kwh_m2", "eta_caldaia",
            "piante_anno", "litri_pianta", "kwh_pomp_m3_base",
            "p_gas", "p_el", "cop_pdc", "kwh_pomp_m3_alt",
            "quota_fv", "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "capex_pdc", "capex_irrigazione",
            "capex_fv_eur_kwp", "f_co2_gas_kg_kwh",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_sup_zero_no(self):
        kw = _demo_kwargs(sup_serra_m2=0)
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_piante_zero_no(self):
        kw = _demo_kwargs(piante_anno=0)
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_eta_zero_e_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=0.0)
        self.assertRaises(ValueError, mh860_calcola, **kw)
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0.0)
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_quote_sopra_uno_no(self):
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh860_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh860_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh860_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("q_term_spec_kwh_m2", -1),
                              ("p_gas", -0.01),
                              ("capex_pdc", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh860_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh860_calcola(mh860_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh860_calcola(dict(mh860_demo(), capex_pdc=999999),
                           capex_pdc=60000)
        self.assertEqual(bc["capex_eur"], 183000.0)


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
        self.assertEqual(bc["payback"], 8)

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
            bc["c_gas_eur_anno"] + bc["c_pomp_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["e_immessa_kwh_anno"] * bc["p_immissione"])

    def test_coerenza_p_gas_pareggio(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["p_gas_pareggio"],
            (bc["c_alt_eur_anno"] - bc["c_pomp_base_eur_anno"])
            / bc["gas_base_kwh_anno"])

    def test_sensibilita_valori(self):
        s = mh860_sensibilita(**mh860_demo())
        self.assertAlmostEqual(s["p_gas_meno20"]["risparmio_eur_anno"],
                               20052.0, places=2)
        self.assertAlmostEqual(s["p_gas_meno20"]["van"],
                               25132.90, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               24628.8, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               72638.52, places=2)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               6252.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               -10106.38, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["cop_2_5"]["risparmio_eur_anno"],
                               16452.0, places=2)
        self.assertAlmostEqual(s["cop_2_5"]["van"],
                               -12233.87, places=2)
        self.assertEqual(s["cop_2_5"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -95589.15, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["payback"], 15)
        self.assertAlmostEqual(s["vita_10"]["van"],
                               18166.64, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               207780.0, places=2)

    def test_marginale_con_capex_pdc_alto(self):
        # CAPEX totale 280.000 (pompa di calore 157.000):
        # VAN circa -9.585, entro la tolleranza del 10%
        # (28.000).
        bc = mh860_calcola(**_demo_kwargs(capex_pdc=157000))
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_non_convente_con_capex_pdc_altissimo(self):
        bc = mh860_calcola(**_demo_kwargs(capex_pdc=400000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh860_calcola(**_demo_kwargs(p_gas=0.0,
                                          kwh_pomp_m3_base=0.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_q_term_zero_pareggio_none(self):
        # Senza termico il gas e' nullo e il pareggio
        # e' None; il caso resta calcolabile perche'
        # il FV rende il risparmio positivo (costo
        # alternativo negativo da ricavo immissione).
        bc = mh860_calcola(**_demo_kwargs(q_term_spec_kwh_m2=0))
        self.assertEqual(bc["gas_base_kwh_anno"], 0.0)
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertAlmostEqual(bc["c_base_eur_anno"], 672.0)
        self.assertLess(bc["c_alt_eur_anno"], 0.0)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh860_csv(bc, mh860_demo())
        for voce in ("sup_serra_m2", "q_term_kwh_th_anno",
                     "gas_base_kwh_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -183000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie serra (m2)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_q_term_scala_lineare_con_superficie(self):
        self.assertAlmostEqual(mh860_q_term(4000, 150.0),
                               2.0 * mh860_q_term(2000, 150.0))

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh860_c_alt(87214.28571428571, 0.28, 0.0, 0.08)
        con = mh860_c_alt(27814.28571428571, 0.28, 39600.0, 0.08)
        self.assertAlmostEqual(senza - con, 59400.0 * 0.28 + 39600.0 * 0.08)

    def test_sensibilita_chiavi_complete(self):
        s = mh860_sensibilita(**mh860_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_meno20", "p_el_piu20", "senza_fv",
                          "cop_2_5", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh860_csv(bc, mh860_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("q_term_kwh_th_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh860_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh860_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh860_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["capex_eur"], 75000.0)
        bc = mh860_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def860\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh860_demo().keys()), lette - set(mh860_demo().keys()))
        self.assertEqual(lette, set(mh860_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc860\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc860\["([^"]+)"\]', src))
        attese = set(mh860_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab860:"), 1)
        self.assertTrue(src.startswith("    # W864"))

    def test_ui_tab860_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab860:"), 1)
        self.assertIn("def mh860_demo(", src_h)
        self.assertIn("def mh860_calcola(", src_h)
        self.assertIn("tab860", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Vivaio floricolo: pompa di calore + irrigazione efficiente + FV in copertura battono caldaia a gas + pompaggio tradizionale?", src)
        self.assertIn("🌱 Vivaio floricolo: pompa di calore + irrigazione efficiente + FV in copertura battono caldaia a gas + pompaggio tradizionale?", src)
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
        chiavi = re.findall(r'key="(st860_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st860_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st860_calcola"', src)
        self.assertIn('key="st860_csv"', src)
        self.assertIn('key="st860_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg860"), src.index(".paiac("))
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
