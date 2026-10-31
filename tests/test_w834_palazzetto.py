"""Test nuova scheda tab834 "Palazzetto:
LED + pompa di calore + fotovoltaico
battono illuminazione tradizionale +
caldaia a gas?".

Business case deterministico di un
palazzetto dello sport guidato dalle
ORE D'USO della sala: E_ill_base =
ore_uso x p_ill_base_kw; E_ill_alt =
ore_uso x p_ill_led_kw (il LED riduce
solo l'illuminazione); gas_base = Q_th
/ eta_caldaia; gas_alt = 0 (la pompa di
calore sostituisce tutta la caldaia);
E_pdc = Q_th / COP; E_pv = P_pv_kwp x
prod_specifica; E_pv_auto = E_pv x
quota_autoconsumo; E_pv_exp = E_pv -
E_pv_auto (NESSUN credito di costo ne'
di CO2: scelta conservativa); E_base =
E_ill_base (la base non ha pompa di
calore: il calore e' gas); E_alt_lorda
= E_ill_alt + E_pdc; E_alt_netta =
E_alt_lorda - E_pv_auto (elettricita'
di rete alternativa); C_base = E_base x
p_el + gas_base x p_gas + OM_base;
C_alt = E_alt_netta x p_el + gas_alt x
p_gas + OM_alt (gas_alt = 0, termine
per simmetria); risparmio = C_base -
C_alt; CO2 evitata = (E_base x 0,25 +
gas_base x 0,20 - E_alt_netta x 0,25 -
gas_alt x 0,20) / 1000 (fattori
letterali); flussi [-CAPEX, risparmio x
vita]; VAN, TIR, payback (primo anno
con cumulato >= 0); COP_min = Q_th /
E_pdc_max con E_pdc_max =
(C_base - OM_alt) / p_el - E_ill_alt +
E_pv_auto, None se E_pdc_max <= 0,
SOGLIA MINIMA quando esiste. Nel demo
COP_min e' 1,39426800929512: sopra di
essa l'alternativa vince sui costi,
sotto perde. NON esiste un prezzo gas
positivo di pareggio: l'alternativa
vince su entrambi i vettori (meno rete
netta e zero gas), quindi nessun
breakeven gas viene inventato.
Verdetto: NON_CALCOLABILE se input degenere
(ore_uso <= 0, potenze negative, Q_th <= 0,
eta <= 0 o > 1, COP <= 0, P_pv negativo,
prod_specifica negativa, quota < 0 o > 1,
prezzi <= 0, O&M negativi, CAPEX <= 0, WACC
negativo, vita <= 0, tolleranza negativa)
o se risparmio <= 0 (guard degenere: UI salta
KPI, grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Guard UI IDENTICA agli helper:
nessuna divergenza di verdetto. Tutti gli
slider UI hanno minimo 0, quindi i casi
negativi sono NON RAGGIUNGIBILI via slider,
ma la guard li controlla comunque; i casi
= 0 raggiungibili via slider sono bloccati
in UI esattamente come negli helper dove
previsto (ore_uso, Q_th, prezzi, CAPEX, vita).
Gli zeri ammessi in entrambi (potenze, P_pv,
prod_specifica, quota, O&M, WACC, tolleranza)
non creano divergenza. Eta sopra 1 e quota
sopra 1 sono degeneri in entrambi ma non
raggiungibili via slider (tetti 1,0). WACC
sopra 20 % e tolleranza sopra 100 % sono
ammessi negli helper e limitati solo dagli
slider UI (20, 100): nessuna divergenza nel
range raggiungibile, perche' la guard
controlla solo gli stessi limiti degli helper.
Distinzione esplicita: distinto dalla
piscina (riscaldamento di acqua di vasca:
qui niente vasca, solo aria della sala e
luce), dalla palestra fitness (attrezzi e
sale corsi: qui sala sportiva con
illuminazione di gara e riscaldamento
invernale) e dall'edificio scolastico
generico (aule e orari scolastici: qui
palazzetto con ore d'uso sportive,
illuminazione di sala e riscaldamento):
qui driver ORE D'USO + ILLUMINAZIONE LED +
POMPA DI CALORE + FOTOVOLTAICO IN
AUTOCONSUMO.

Demo (palazzetto): 2.500 h/anno d'uso,
illuminazione tradizionale 80 kW
(200.000 kWh_e/anno) e LED 32 kW
(80.000 kWh_e/anno), fabbisogno termico
600.000 kWh_th/anno, caldaia eta 0,90
(gas base 666.666,67 kWh/anno, gas
alternativo 0), pompa di calore COP 3,5
(171.428,57 kWh_e/anno), fotovoltaico
100 kWp a 1.100 kWh/kWp/anno (110.000
kWh_e/anno, autoconsumo 77.000, esportato
33.000 senza credito), elettricita' di
rete base 200.000 e alternativa lorda
251.428,57, netta 174.428,57 kWh_e/anno,
prezzi elettricita' 0,22 e gas 0,08
EUR/kWh, O&M base 0 e alternativo 2.000
EUR/anno, CAPEX 420.000 EUR (LED 40.000 +
pompa di calore 180.000 + fotovoltaico
200.000), WACC 5 %, vita 20 anni,
tolleranza 10 % del CAPEX.
Valori calcolati eseguendo
mh834_demo_calcoli(): E_base 200.000,
E_alt_lorda 251.428,57, E_alt_netta
174.428,57, gas_base 666.666,67,
gas_alt 0, C_base 97.333,33, C_alt
40.374,29, risparmio 56.959,05,
CO2_base 183,33, CO2_alt 43,61,
CO2_evitata 139,73, VAN
289835,6323393226, TIR
12,206677851906129 %, payback 8,
COP_min 1,39426800929512, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w834_palazzetto.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w836_helpers import (
    demo_calcoli,
    mh834_c_alt,
    mh834_c_base,
    mh834_calcola,
    mh834_co2_alt,
    mh834_co2_base,
    mh834_co2_evitata,
    mh834_cop_min,
    mh834_csv,
    mh834_demo,
    mh834_demo_calcoli,
    mh834_e_alt_lorda,
    mh834_e_alt_netta,
    mh834_e_base,
    mh834_e_ill_alt,
    mh834_e_ill_base,
    mh834_e_pdc,
    mh834_e_pv,
    mh834_e_pv_auto,
    mh834_eta,
    mh834_flussi,
    mh834_frazione,
    mh834_gas_base,
    mh834_int_pos,
    mh834_nneg,
    mh834_num,
    mh834_payback,
    mh834_pos,
    mh834_risparmio,
    mh834_sensibilita,
    mh834_tir,
    mh834_valida,
    mh834_van,
    mh834_verdetto,
)

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w836_helpers.py")
_UI_PATH = _risolvi("w836_ui.py")


def _trova_app():
    candidati = [
        os.path.join(os.path.dirname(_HERE), "app.py"),
        os.path.join(_HERE, "app.py"),
        os.path.join(os.path.dirname(_HERE), "..", "app.py"),
        os.path.expanduser("~/workspace/qa-dashboard/repo/app.py"),
    ]
    for p in candidati:
        p = os.path.normpath(p)
        if os.path.exists(p):
            return p
    return candidati[0]


_APP_PATH = _trova_app()

_DEMO = {
    "e_ill_base_kwh_e_anno": 200000.0,
    "e_ill_alt_kwh_e_anno": 80000.0,
    "gas_base_kwh_anno": 666666.6666666666,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 171428.57142857142,
    "e_pv_kwh_e_anno": 110000.0,
    "e_pv_auto_kwh_e_anno": 77000.0,
    "e_pv_exp_kwh_e_anno": 33000.0,
    "e_base_kwh_e_anno": 200000.0,
    "e_alt_lorda_kwh_e_anno": 251428.57142857142,
    "e_alt_netta_kwh_e_anno": 174428.57142857142,
    "c_base_eur_anno": 97333.33333333333,
    "c_alt_eur_anno": 40374.28571428571,
    "risparmio_eur_anno": 56959.04761904762,
    "co2_base_t_anno": 183.33333333333334,
    "co2_alt_t_anno": 43.607142857142854,
    "co2_evitata_t_anno": 139.72619047619048,
    "van": 289835.6323393226,
    "tir": 12.206677851906129,
    "payback": 8,
    "cop_min": 1.39426800929512,
}


def _demo_kwargs(**over):
    kw = dict(mh834_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh834_num(3, "x"), 3.0)
        self.assertEqual(mh834_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh834_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh834_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh834_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh834_pos(0, "x")
        with self.assertRaises(ValueError):
            mh834_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh834_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh834_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh834_frazione(0, "quota"), 0.0)
        self.assertEqual(mh834_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh834_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh834_frazione(1.1, "quota")

    def test_eta_limiti(self):
        self.assertEqual(mh834_eta(1.0, "eta"), 1.0)
        with self.assertRaises(ValueError):
            mh834_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh834_eta(1.1, "eta")


class TestFisica(unittest.TestCase):
    def test_ill_gas_pdc_pv(self):
        self.assertEqual(mh834_e_ill_base(2500, 80), 200000.0)
        self.assertEqual(mh834_e_ill_alt(2500, 32), 80000.0)
        self.assertAlmostEqual(mh834_gas_base(600000, 0.90), 666666.6666666666, places=9)
        self.assertAlmostEqual(mh834_e_pdc(600000, 3.5), 171428.57142857142, places=9)
        self.assertEqual(mh834_e_pv(100, 1100), 110000.0)
        self.assertEqual(mh834_e_pv_auto(110000.0, 0.70), 77000.0)

    def test_e_base_lorda_netta(self):
        self.assertEqual(mh834_e_base(200000.0), 200000.0)
        self.assertAlmostEqual(mh834_e_alt_lorda(80000.0, 171428.57142857142), 251428.57142857142, places=9)
        self.assertAlmostEqual(mh834_e_alt_netta(251428.57142857142, 77000.0), 174428.57142857142, places=9)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh834_c_base(200000.0, 0.22, 666666.6666666666, 0.08, 0), 97333.33333333333, places=9)
        self.assertAlmostEqual(mh834_c_alt(174428.57142857142, 0.22, 0.0, 0.08, 2000), 40374.28571428571, places=9)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh834_risparmio(97333.33333333333, 40374.28571428571), 56959.04761904762, places=9)
        self.assertLess(mh834_risparmio(40374.28571428571, 97333.33333333333), 0.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh834_co2_base(200000.0, 666666.6666666666), 183.33333333333334, places=9)
        self.assertAlmostEqual(mh834_co2_alt(174428.57142857142, 0.0), 43.607142857142854, places=9)
        self.assertAlmostEqual(
            mh834_co2_evitata(200000.0, 666666.6666666666, 174428.57142857142, 0.0), 139.72619047619048, places=9)

    def test_alt_netta_minore_di_base_nel_demo(self):
        bc = mh834_demo_calcoli()
        self.assertLess(bc["e_alt_netta_kwh_e_anno"], bc["e_base_kwh_e_anno"])
        self.assertEqual(bc["gas_alt_kwh_anno"], 0.0)
        self.assertGreater(bc["e_alt_lorda_kwh_e_anno"], bc["e_base_kwh_e_anno"])

    def test_pv_esportato_senza_credito(self):
        bc = mh834_demo_calcoli()
        self.assertEqual(bc["e_pv_exp_kwh_e_anno"], 33000.0)
        self.assertAlmostEqual(bc["e_alt_netta_kwh_e_anno"],
                               bc["e_alt_lorda_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"], places=9)
        # Se l'esportato avesse credito, il costo alternativo sarebbe piu' basso:
        # qui non lo e': il costo usa solo la netta.
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_alt_netta_kwh_e_anno"] * 0.22 + 2000, places=6)


class TestFinanza(unittest.TestCase):
    def test_cop_min_demo_valore(self):
        copmin = mh834_cop_min(97333.33333333333, 2000, 0.22, 80000.0, 77000.0, 600000)
        self.assertAlmostEqual(copmin, 1.39426800929512, places=12)

    def test_cop_min_none_se_epdc_max_nonpositivo(self):
        self.assertIsNone(mh834_cop_min(2000.0, 2000, 0.22, 80000.0, 0.0, 600000))

    def test_cop_min_verifica_pareggio_su_demo(self):
        bc = mh834_demo_calcoli()
        copmin = bc["cop_min"]
        r = mh834_calcola(**_demo_kwargs(cop=copmin))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_cop_min_soglia_minima_su_demo(self):
        bc = mh834_demo_calcoli()
        copmin = bc["cop_min"]
        self.assertGreater(mh834_calcola(**_demo_kwargs(cop=copmin + 0.1))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh834_calcola(**_demo_kwargs(cop=copmin - 0.1))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh834_flussi(420000, 56959.04761904762, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -420000)
        self.assertTrue(all(f == 56959.04761904762 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh834_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 289835.6323393226, places=6)
        self.assertAlmostEqual(mh834_van([-420000] + [56959.04761904762] * 20, 0.0), 719180.9523809524, places=6)

    def test_tir_demo(self):
        bc = mh834_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 12.206677851906129, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh834_payback([-420000] + [56959.04761904762] * 20), 8)
        self.assertEqual(mh834_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh834_payback([-420000] + [100.0] * 20))

    def test_verdetto(self):
        self.assertEqual(mh834_verdetto(56959.04761904762, 100.0, 420000, 10.0), "CONVIENTE")
        self.assertEqual(mh834_verdetto(56959.04761904762, -20000.0, 420000, 10.0), "MARGINALE")
        self.assertEqual(mh834_verdetto(56959.04761904762, -100000.0, 420000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh834_verdetto(0.0, 100.0, 420000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh834_verdetto(-100.0, 100.0, 420000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh834_verdetto(None, 100.0, 420000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh834_verdetto(56959.04761904762, 0.0, 420000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh834_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("ore_uso", "2500"), ("ore_uso", float("nan")),
                            ("ore_uso", float("inf")), ("ore_uso", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh834_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"ore_uso": 0}, {"ore_uso": -1}, {"p_ill_base_kw": -0.1},
                     {"q_th": 0}, {"eta_caldaia": 0}, {"eta_caldaia": 1.1},
                     {"cop": 0}, {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"quota_autoconsumo": -0.1}, {"quota_autoconsumo": 1.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc": -1}, {"vita": 0},
                     {"vita": 20.5}, {"tolleranza": -1}):
            self.assertFalse(mh834_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh834_valida(**_demo_kwargs(wacc=25.0))["valido"])
        self.assertTrue(mh834_valida(**_demo_kwargs(tolleranza=150.0))["valido"])
        self.assertTrue(mh834_valida(**_demo_kwargs(
            p_ill_base_kw=0, p_pv_kwp=0, prod_specifica=0,
            quota_autoconsumo=0, om_base=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh834_demo()
        self.assertEqual(d["ore_uso"], 2500)
        self.assertEqual(d["p_ill_base_kw"], 80)
        self.assertEqual(d["p_ill_led_kw"], 32)
        self.assertEqual(d["q_th"], 600000)
        self.assertEqual(d["eta_caldaia"], 0.90)
        self.assertEqual(d["cop"], 3.5)
        self.assertEqual(d["p_pv_kwp"], 100)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["quota_autoconsumo"], 0.70)
        self.assertEqual(d["capex"], 420000)
        self.assertEqual(d["vita"], 20)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh834_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh834_demo_calcoli()
        self.assertEqual(bc["e_ill_base_kwh_e_anno"], 200000.0)
        self.assertEqual(bc["e_ill_alt_kwh_e_anno"], 80000.0)
        self.assertEqual(bc["e_pdc_kwh_e_anno"], 171428.57142857142)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 110000.0)
        self.assertEqual(bc["c_base_eur_anno"], 97333.33333333333)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 40374.28571428571, places=9)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh834_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7], -21286.6666666666, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], 35672.38095238102, places=6)

    def test_demo_tabella_righe(self):
        bc = mh834_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Ore d'uso (h/anno)", voci)
        self.assertIn("Illuminazione LED (kWh_e/anno)", voci)
        self.assertIn("Pompa di calore (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico esportato, senza credito (kWh_e/anno)", voci)
        self.assertIn("COP di pareggio (soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh834_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], bc["e_ill_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"],
                               bc["e_ill_alt_kwh_e_anno"] + bc["e_pdc_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_netta_kwh_e_anno"],
                               bc["e_alt_lorda_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        e_ill_b = 2500 * 80
        e_ill_a = 2500 * 32
        gas_b = 600000 / 0.90
        e_pdc = 600000 / 3.5
        e_pv = 100 * 1100
        e_pv_a = e_pv * 0.70
        e_netta = e_ill_a + e_pdc - e_pv_a
        c_base = e_ill_b * 0.22 + gas_b * 0.08 + 0
        c_alt = e_netta * 0.22 + 0 * 0.08 + 2000
        bc = mh834_demo_calcoli()
        self.assertAlmostEqual(bc["e_ill_base_kwh_e_anno"], e_ill_b, places=6)
        self.assertAlmostEqual(bc["e_ill_alt_kwh_e_anno"], e_ill_a, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_b, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], e_pdc, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_alt_netta_kwh_e_anno"], e_netta, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh834_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_led_marginale(self):
        r = mh834_calcola(**_demo_kwargs(p_ill_led_kw=80))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 30559.04761904762, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertAlmostEqual(r["van"], -39166.72070373304, places=6)
        self.assertEqual(r["payback"], 14)
        self.assertAlmostEqual(r["cop_min"], 1.933404940923738, places=12)

    def test_variante_senza_fotovoltaico(self):
        r = mh834_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 40019.04761904762, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 78725.78913669521, places=6)
        self.assertEqual(r["payback"], 11)

    def test_variante_gas_basso_e_alto(self):
        basso = mh834_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], 16959.04761904762, places=6)
        self.assertEqual(basso["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(basso["van"], -208652.78136227667, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh834_calcola(**_demo_kwargs(p_gas=0.10))
        self.assertAlmostEqual(alto["risparmio_eur_anno"], 70292.38095238096, places=6)
        self.assertAlmostEqual(alto["van"], 455998.4369065223, places=6)
        self.assertAlmostEqual(alto["tir"], 15.854404211027651, places=6)
        self.assertEqual(alto["payback"], 6)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_elettricita_piu_meno_20(self):
        meno = mh834_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 55833.904761904756, places=6)
        self.assertAlmostEqual(meno["van"], 275813.8653882018, places=6)
        self.assertAlmostEqual(meno["tir"], 11.887744818170914, places=6)
        self.assertEqual(meno["payback"], 8)
        piu = mh834_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 58084.19047619047, places=6)
        self.assertAlmostEqual(piu["van"], 303857.39929044317, places=6)
        self.assertAlmostEqual(piu["tir"], 12.523586824553313, places=6)
        self.assertEqual(piu["payback"], 8)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_elettricita_alta_migliora_leggermente_il_caso(self):
        demo = mh834_demo_calcoli()
        meno = mh834_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh834_calcola(**_demo_kwargs(p_el=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(demo["e_alt_netta_kwh_e_anno"], demo["e_base_kwh_e_anno"])

    def test_variante_capex_doppio_non_convinte(self):
        r = mh834_calcola(**_demo_kwargs(capex=840000))
        self.assertAlmostEqual(r["van"], -130164.36766067763, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["payback"], 15)

    def test_variante_vita_10_convinte(self):
        r = mh834_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 19822.66753310097, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertEqual(r["payback"], 8)

    def test_variante_cop_20_non_convinte_ma_risparmio_positivo(self):
        r = mh834_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 28673.33333333333, places=6)
        self.assertGreater(r["risparmio_eur_anno"], 0.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -62666.888778237, places=6)
        self.assertEqual(r["payback"], 15)

    def test_variante_cop_12_non_calcolabile(self):
        r = mh834_calcola(**_demo_kwargs(cop=1.2))
        self.assertLess(r["risparmio_eur_anno"], 0.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["tir"])
        self.assertIsNone(r["payback"])

    def test_variante_wacc_zero(self):
        zero = mh834_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 719180.9523809524, places=6)
        self.assertEqual(zero["payback"], 8)

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh834_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh834_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh834_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh834_sensibilita(**mh834_demo())
        self.assertEqual(set(s.keys()), {"el_meno20", "el_piu20", "gas_002",
                                         "gas_010", "capex_doppio", "vita_10",
                                         "cop_20", "cop_12"})
        self.assertAlmostEqual(s["el_meno20"]["risparmio_eur_anno"], 55833.904761904756, places=6)
        self.assertAlmostEqual(s["el_piu20"]["van"], 303857.39929044317, places=6)
        self.assertEqual(s["gas_002"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["gas_010"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["cop_20"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["cop_12"]["verdetto"], "NON_CALCOLABILE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh834_demo_calcoli()
        b = mh834_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh834_demo()
        attese = {"ore_uso", "p_ill_base_kw", "p_ill_led_kw",
                  "q_th", "eta_caldaia", "cop",
                  "p_pv_kwp", "prod_specifica", "quota_autoconsumo",
                  "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["ore_uso", "p_ill_base_kw", "p_ill_led_kw",
                 "q_th", "eta_caldaia", "cop",
                 "p_pv_kwp", "prod_specifica", "quota_autoconsumo",
                 "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh834_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_eta_sopra_uno_e_quota_sopra_uno(self):
        with self.assertRaises(ValueError):
            mh834_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh834_calcola(**_demo_kwargs(quota_autoconsumo=1.1))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("ore_uso", "2500"), ("ore_uso", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh834_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh834_calcola(**_demo_kwargs(p_ill_base_kw=0, p_pv_kwp=0,
                                         prod_specifica=0, quota_autoconsumo=0,
                                         om_base=0, wacc=0, tolleranza=0))
        self.assertTrue(r["valid"])
        r2 = mh834_calcola(**_demo_kwargs(om_alt=2000, p_el=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh834_calcola(**_demo_kwargs(om_alt=100000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_cop(self):
        copmin = mh834_demo_calcoli()["cop_min"]
        r = mh834_calcola(**_demo_kwargs(cop=copmin))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh834_demo_calcoli()
        csv = mh834_csv(bc, dict(mh834_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh834_demo_calcoli()
        csv = mh834_csv(bc, dict(mh834_demo()))
        self.assertIn("risparmio_eur_anno;56959.04761904762", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh834_demo_calcoli()
        csv = mh834_csv(bc, dict(mh834_demo()))
        for chiave in mh834_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh833_", src)
        self.assertNotIn("mh832_", src)
        self.assertNotIn("mh831_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab834:"), 1)
        self.assertTrue(src.startswith("    # W836"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Palazzetto: LED + pompa di calore + fotovoltaico", src)
        self.assertIn("🏟️ Palazzetto: LED + pompa di calore + fotovoltaico battono illuminazione tradizionale + caldaia a gas?", src)
        self.assertNotIn("tab833", src)
        self.assertNotIn("tab832", src)
        self.assertNotIn("tab831", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh833_", "mh832_", "mh831_", "mh830_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh833_", src)
        self.assertNotIn("st833_", src)
        self.assertNotIn("mh832_", src)
        self.assertNotIn("st832_", src)
        chiavi = re.findall(r'key="(st834_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st834_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st834_calcola"', src)
        self.assertIn('key="st834_csv"', src)
        self.assertIn('key="st834_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def834\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh834_demo().keys()), lette - set(mh834_demo().keys()))
        self.assertEqual(lette, set(mh834_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc834\['([^']+)'\]", src))
        attese = set(mh834_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg834"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        # Ogni slider/number_input deve avere min_value=0 (negativi non
        # raggiungibili via UI, ma guardati comunque negli helper).
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


class TestAppPresenza(unittest.TestCase):
    def test_app_contiene_tab834_e_titolo(self):
        self.assertTrue(os.path.exists(_APP_PATH), f"app.py non trovato: {_APP_PATH} (apply tab834 non ancora fatto)")
        src = open(_APP_PATH, encoding="utf-8").read()
        self.assertIn("tab834", src)
        self.assertIn("🏟️ Palazzetto: LED + pompa di calore + fotovoltaico battono illuminazione tradizionale + caldaia a gas?", src)


if __name__ == "__main__":
    unittest.main()
