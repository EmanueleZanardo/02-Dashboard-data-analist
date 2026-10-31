"""Test nuova scheda tab831 "Impianto di betonaggio:
miscelatore ad alta efficienza + nastri
con inverter + pompa di calore per acqua
di impasto battono miscelatore
tradizionale + nastri tradizionali +
caldaia a gas per acqua?".

Business case deterministico di un
impianto di betonaggio guidato dai
METRI CUBI DI CALCESTRUZZO prodotti in
un anno: E_misc_base = m3 x e_misc_base;
E_misc_alt = m3 x e_misc_alt (il
miscelatore ad alta efficienza riduce
solo la miscelazione); E_nas_base = m3 x
e_nas_base; E_nas_alt = m3 x e_nas_alt
(i nastri con inverter riducono solo i
nastri); E_pdc_alt = m3 x e_pdc_alt (la
pompa di calore per acqua di impasto,
GIA' dentro E_alt); E_base = E_misc_base
+ E_nas_base; E_alt = E_misc_alt +
E_nas_alt + E_pdc_alt; gas_base = m3 x
g_base; gas_alt = m3 x g_alt (0 nel demo:
la pompa di calore azzera il gas, quindi
il risparmio gas e' totale, ma E_alt
resta inferiore a E_base: 2,85 contro
3,60 kWh_e/m3); C_base = E_base x p_el +
gas_base x p_gas + OM_base; C_alt =
E_alt x p_el + gas_alt x p_gas + OM_alt
(prezzi in EUR/kWh, nessuna conversione
/ 1000); risparmio = C_base - C_alt;
CO2 evitata = (E_base x 0,25 + gas_base x
0,20 - E_alt x 0,25 - gas_alt x 0,20) /
1000 (fattori letterali); flussi
[-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas = (E_alt x p_el + OM_alt -
E_base x p_el - OM_base) / (gas_base -
gas_alt) EUR/kWh, None se gas_base <=
gas_alt o numeratore < 0, SOGLIA MINIMA
quando esiste. Nel demo il breakeven e'
0,01861111111111111 EUR/kWh (numeratore
20.100 EUR, denominatore 1.080.000
kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(m3 <= 0, specifici negativi, prezzi <= 0,
O&M negativi, CAPEX <= 0, WACC negativo,
vita <= 0, tolleranza negativa) o se
risparmio <= 0 (guard degenere: UI salta
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
previsto (m3, prezzi, CAPEX, vita). Gli zeri
ammessi in entrambi (specifici elettrici e
gas, O&M, WACC, tolleranza) non creano
divergenza: con gas specifico base uguale a
gas specifico alternativo il breakeven e'
None, e il caso resta calcolabile in
entrambi. WACC sopra 20 % e tolleranza
sopra 100 % sono ammessi negli helper e
limitati solo dagli slider UI (20, 100):
nessuna divergenza nel range raggiungibile,
perche' la guard controlla solo gli stessi
limiti degli helper.
Distinzione esplicita: distinto
dall'asfalto (legante bitume, tamburo a
gas: qui solo cemento, inerti e acqua di
impasto), dal cantiere (getto del
calcestruzzo: qui solo produzione in
impianto) e dal cementificio (produzione
del cemento: qui solo miscelazione con
cemento gia' pronto): qui driver M3 DI
CALCESTRUZZO + MISCELATORE AD ALTA
EFFICIENZA + NASTRI CON INVERTER + POMPA
DI CALORE PER ACQUA DI IMPASTO.

Demo (impianto di betonaggio): 60.000 m3 di
calcestruzzo prodotti in un anno,
miscelazione specifica base 2,50
(150.000 kWh_e/anno) e alternativa 1,80
(108.000 kWh_e/anno), nastri specifici
base 1,10 (66.000 kWh_e/anno) e
alternativa 0,65 (39.000 kWh_e/anno),
pompa di calore alternativa 0,40
(24.000 kWh_e/anno, gia' dentro E_alt),
elettricita' base 216.000 e alternativa
171.000 kWh_e/anno, gas specifico base
18,00 (1.080.000 kWh/anno) e alternativo
0,00 (0 kWh/anno: la pompa di calore
azzera il gas), prezzi elettricita' 0,22
e gas 0,09 EUR/kWh, O&M base 90.000 e
alternativo 120.000 EUR/anno, CAPEX
420.000 EUR, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh831_demo_calcoli(): E_base
216.000, E_alt 171.000, gas_base
1.080.000, gas_alt 0, C_base 234.720,
C_alt 157.620, risparmio 77.100,
CO2_base 270,0, CO2_alt 42,75,
CO2_evitata 227,25, VAN 380271,63474372355,
TIR 16,49960150783494 %, payback 6,
breakeven gas 0,01861111111111111 EUR/kWh,
verdetto CONVIENTE.

Destinazione nel repo: tests/test_w831_betonaggio.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w833_helpers import (
    demo_calcoli,
    mh831_breakeven_gas,
    mh831_c_alt,
    mh831_c_base,
    mh831_calcola,
    mh831_co2_alt,
    mh831_co2_base,
    mh831_co2_evitata,
    mh831_csv,
    mh831_demo,
    mh831_demo_calcoli,
    mh831_e_alt,
    mh831_e_base,
    mh831_e_nas_alt,
    mh831_e_nas_base,
    mh831_e_misc_alt,
    mh831_e_misc_base,
    mh831_e_pdc_alt,
    mh831_flussi,
    mh831_gas_alt,
    mh831_gas_base,
    mh831_int_pos,
    mh831_nneg,
    mh831_num,
    mh831_payback,
    mh831_pos,
    mh831_risparmio,
    mh831_tir,
    mh831_valida,
    mh831_van,
    mh831_verdetto,
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


_HELPERS_PATH = _risolvi("w833_helpers.py")
_UI_PATH = _risolvi("w833_ui.py")

_DEMO = {
    "e_misc_base_kwh_e_anno": 150000.0,
    "e_misc_alt_kwh_e_anno": 108000.0,
    "e_nas_base_kwh_e_anno": 66000.0,
    "e_nas_alt_kwh_e_anno": 39000.0,
    "e_pdc_alt_kwh_e_anno": 24000.0,
    "e_base_kwh_e_anno": 216000.0,
    "e_alt_kwh_e_anno": 171000.0,
    "gas_base_kwh_anno": 1080000.0,
    "gas_alt_kwh_anno": 0.0,
    "c_base_eur_anno": 234720.0,
    "c_alt_eur_anno": 157620.0,
    "risparmio_eur_anno": 77100.0,
    "co2_base_t_anno": 270.0,
    "co2_alt_t_anno": 42.75,
    "co2_evitata_t_anno": 227.25,
    "van": 380271.63474372355,
    "tir": 16.49960150783494,
    "payback": 6,
    "breakeven_gas_eur_kwh": 0.01861111111111111,
}


def _demo_kwargs(**over):
    kw = dict(mh831_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh831_num(3, "x"), 3.0)
        self.assertEqual(mh831_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh831_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh831_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh831_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh831_pos(0, "x")
        with self.assertRaises(ValueError):
            mh831_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh831_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh831_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_misc_nas_pdc_e_base(self):
        self.assertEqual(mh831_e_misc_base(60000, 2.50), 150000.0)
        self.assertEqual(mh831_e_misc_alt(60000, 1.80), 108000.0)
        self.assertEqual(mh831_e_nas_base(60000, 1.10), 66000.0)
        self.assertAlmostEqual(mh831_e_nas_alt(60000, 0.65), 39000.0, places=6)
        self.assertEqual(mh831_e_pdc_alt(60000, 0.40), 24000.0)
        self.assertEqual(mh831_e_base(150000.0, 66000.0), 216000.0)
        self.assertAlmostEqual(mh831_e_alt(108000.0, 39000.0, 24000.0), 171000.0, places=6)

    def test_gas_base_alt_azzerato(self):
        self.assertEqual(mh831_gas_base(60000, 18.00), 1080000.0)
        self.assertEqual(mh831_gas_alt(60000, 0.00), 0.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh831_c_base(216000.0, 0.22, 1080000.0, 0.09, 90000), 234720.0)
        self.assertEqual(mh831_c_alt(171000.0, 0.22, 0.0, 0.09, 120000), 157620.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh831_risparmio(234720.0, 157620.0), 77100.0)
        self.assertEqual(mh831_risparmio(157620.0, 234720.0), -77100.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh831_co2_base(216000.0, 1080000.0), 270.0, places=9)
        self.assertAlmostEqual(mh831_co2_alt(171000.0, 0.0), 42.75, places=9)
        self.assertAlmostEqual(
            mh831_co2_evitata(216000.0, 1080000.0, 171000.0, 0.0), 227.25, places=9)

    def test_e_alt_inferiore_a_e_base(self):
        bc = mh831_demo_calcoli()
        self.assertLess(bc["e_alt_kwh_e_anno"], bc["e_base_kwh_e_anno"])


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh831_breakeven_gas(171000.0, 0.22, 120000, 216000.0, 90000, 1080000.0, 0.0)
        self.assertAlmostEqual(be, 0.01861111111111111, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh831_breakeven_gas(1000.0, 0.22, 1000, 216000.0, 90000, 1080000.0, 0.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh831_breakeven_gas(171000.0, 0.22, 120000, 216000.0, 90000, 1080000.0, 1080000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh831_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh831_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh831_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh831_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh831_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh831_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh831_flussi(420000, 77100.0, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -420000)
        self.assertTrue(all(f == 77100.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh831_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 380271.63474372355, places=6)
        self.assertEqual(mh831_van([-420000] + [77100.0] * 15, 0.0), 736500.0)

    def test_tir_demo(self):
        bc = mh831_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 16.49960150783494, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh831_payback([-420000] + [77100.0] * 15), 6)
        self.assertEqual(mh831_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh831_payback([-420000] + [100.0] * 15))

    def test_verdetto(self):
        self.assertEqual(mh831_verdetto(77100.0, 100.0, 420000, 10.0), "CONVIENTE")
        self.assertEqual(mh831_verdetto(77100.0, -28664.14, 420000, 10.0), "MARGINALE")
        self.assertEqual(mh831_verdetto(77100.0, -99728.37, 420000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh831_verdetto(0.0, 100.0, 420000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh831_verdetto(-100.0, 100.0, 420000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh831_verdetto(None, 100.0, 420000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh831_verdetto(77100.0, 0.0, 420000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh831_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("m3", "60000"), ("m3", float("nan")),
                            ("m3", float("inf")), ("m3", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh831_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"m3": 0}, {"m3": -1}, {"e_misc_base_kwh_e_m3": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh831_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh831_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh831_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh831_valida(**_demo_kwargs(
            e_misc_base_kwh_e_m3=0, e_nas_base_kwh_e_m3=0,
            g_base_kwh_m3=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh831_demo()
        self.assertEqual(d["m3"], 60000)
        self.assertEqual(d["e_misc_base_kwh_e_m3"], 2.50)
        self.assertEqual(d["e_misc_alt_kwh_e_m3"], 1.80)
        self.assertEqual(d["e_nas_base_kwh_e_m3"], 1.10)
        self.assertEqual(d["e_nas_alt_kwh_e_m3"], 0.65)
        self.assertEqual(d["e_pdc_alt_kwh_e_m3"], 0.40)
        self.assertEqual(d["g_base_kwh_m3"], 18.00)
        self.assertEqual(d["g_alt_kwh_m3"], 0.00)
        self.assertEqual(d["capex"], 420000)
        self.assertEqual(d["vita_anni"], 15)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh831_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh831_demo_calcoli()
        self.assertEqual(bc["e_misc_base_kwh_e_anno"], 150000.0)
        self.assertEqual(bc["e_misc_alt_kwh_e_anno"], 108000.0)
        self.assertEqual(bc["e_nas_base_kwh_e_anno"], 66000.0)
        self.assertAlmostEqual(bc["e_nas_alt_kwh_e_anno"], 39000.0, places=6)
        self.assertEqual(bc["e_pdc_alt_kwh_e_anno"], 24000.0)
        self.assertEqual(bc["c_base_eur_anno"], 234720.0)
        self.assertEqual(bc["c_alt_eur_anno"], 157620.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh831_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[5], -34500.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[6], 42600.0)

    def test_demo_tabella_righe(self):
        bc = mh831_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Calcestruzzo (m3/anno)", voci)
        self.assertIn("Miscelazione baseline (kWh_e/anno)", voci)
        self.assertIn("Pompa di calore alternativa (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh831_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_misc_base_kwh_e_anno"] + bc["e_nas_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"],
                               bc["e_misc_alt_kwh_e_anno"] + bc["e_nas_alt_kwh_e_anno"] + bc["e_pdc_alt_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        m3 = 60000
        e_base = m3 * (2.50 + 1.10)
        e_alt = m3 * (1.80 + 0.65 + 0.40)
        gas_base = m3 * 18.00
        gas_alt = m3 * 0.00
        c_base = e_base * 0.22 + gas_base * 0.09 + 90000
        c_alt = e_alt * 0.22 + gas_alt * 0.09 + 120000
        bc = mh831_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh831_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_mescolatore_resta_convinte(self):
        r = mh831_calcola(**_demo_kwargs(e_misc_alt_kwh_e_m3=2.50))
        self.assertEqual(r["risparmio_eur_anno"], 67860.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 284363.5944709348, places=6)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.027166666666666665, places=12)

    def test_variante_senza_nastri_resta_convinte(self):
        r = mh831_calcola(**_demo_kwargs(e_nas_alt_kwh_e_m3=1.10))
        self.assertEqual(r["risparmio_eur_anno"], 71160.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 318616.4659969309, places=6)
        self.assertIsNotNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.02411111111111111, places=12)

    def test_variante_senza_pompa_calore_non_calcolabile(self):
        r = mh831_calcola(**_demo_kwargs(g_alt_kwh_m3=18.00))
        self.assertEqual(r["risparmio_eur_anno"], -20100.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_900000_non_convinte(self):
        r = mh831_calcola(**_demo_kwargs(capex=900000))
        self.assertAlmostEqual(r["van"], -99728.36525627662, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["payback"], 12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh831_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], 1500.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(basso["van"], -404430.51294272905, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh831_calcola(**_demo_kwargs(p_gas=0.15))
        self.assertEqual(alto["risparmio_eur_anno"], 141900.0)
        self.assertAlmostEqual(alto["van"], 1052873.4756178258, places=6)
        self.assertAlmostEqual(alto["tir"], 33.33426766507289, places=6)
        self.assertEqual(alto["payback"], 3)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_elettricita_piu_meno_20(self):
        meno = mh831_calcola(**_demo_kwargs(p_el=0.176))
        self.assertEqual(meno["risparmio_eur_anno"], 75120.0)
        self.assertAlmostEqual(meno["van"], 359719.91182812594, places=6)
        self.assertAlmostEqual(meno["tir"], 15.94043233975475, places=6)
        self.assertEqual(meno["payback"], 6)
        piu = mh831_calcola(**_demo_kwargs(p_el=0.264))
        self.assertEqual(piu["risparmio_eur_anno"], 79080.0)
        self.assertAlmostEqual(piu["van"], 400823.357659321, places=6)
        self.assertAlmostEqual(piu["tir"], 17.05437017256195, places=6)
        self.assertEqual(piu["payback"], 6)

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh831_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 736500.0)
        self.assertEqual(zero["payback"], 6)
        sei = mh831_calcola(**_demo_kwargs(vita_anni=6))
        self.assertAlmostEqual(sei["van"], -28664.141613679865, places=6)
        self.assertEqual(sei["verdetto"], "MARGINALE")
        self.assertEqual(sei["payback"], 6)
        cinque = mh831_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(cinque["van"], -86197.34869436384, places=6)
        self.assertEqual(cinque["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(cinque["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh831_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh831_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh831_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_misc_e_pompa_calore(self):
        base = mh831_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh831_calcola(**_demo_kwargs(e_misc_alt_kwh_e_m3=2.20))["risparmio_eur_anno"], base)
        self.assertLess(mh831_calcola(**_demo_kwargs(g_alt_kwh_m3=5.00))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh831_demo_calcoli()
        b = mh831_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh831_demo()
        attese = {"m3", "e_misc_base_kwh_e_m3", "e_misc_alt_kwh_e_m3",
                  "e_nas_base_kwh_e_m3", "e_nas_alt_kwh_e_m3",
                  "e_pdc_alt_kwh_e_m3",
                  "g_base_kwh_m3", "g_alt_kwh_m3", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["m3", "e_misc_base_kwh_e_m3", "e_misc_alt_kwh_e_m3",
                 "e_nas_base_kwh_e_m3", "e_nas_alt_kwh_e_m3",
                 "e_pdc_alt_kwh_e_m3",
                 "g_base_kwh_m3", "g_alt_kwh_m3", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh831_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("m3", "60000"), ("m3", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh831_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh831_calcola(**_demo_kwargs(e_misc_base_kwh_e_m3=0,
                                         e_nas_base_kwh_e_m3=0,
                                         g_base_kwh_m3=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh831_calcola(**_demo_kwargs(g_alt_kwh_m3=18.00))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh831_calcola(**_demo_kwargs(om_alt=250000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh831_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh831_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh831_demo_calcoli()
        csv = mh831_csv(bc, dict(mh831_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh831_demo_calcoli()
        csv = mh831_csv(bc, dict(mh831_demo()))
        self.assertIn("risparmio_eur_anno;77100.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh831_demo_calcoli()
        csv = mh831_csv(bc, dict(mh831_demo()))
        for chiave in mh831_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh830_", src)
        self.assertNotIn("mh829_", src)
        self.assertNotIn("mh828_", src)
        self.assertNotIn("mh827_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab831:"), 1)
        self.assertTrue(src.startswith("    # W833"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Impianto di betonaggio: miscelatore ad alta efficienza", src)
        self.assertIn("pompa di calore per acqua di impasto", src)
        self.assertNotIn("tab830", src)
        self.assertNotIn("tab829", src)
        self.assertNotIn("tab828", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh830_", "mh829_", "mh828_", "mh827_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh830_", src)
        self.assertNotIn("st830_", src)
        self.assertNotIn("mh829_", src)
        self.assertNotIn("st829_", src)
        chiavi = re.findall(r'key="(st831_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st831_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st831_calcola"', src)
        self.assertIn('key="st831_csv"', src)
        self.assertIn('key="st831_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def831\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh831_demo().keys()), lette - set(mh831_demo().keys()))
        self.assertEqual(lette, set(mh831_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc831\['([^']+)'\]", src))
        attese = set(mh831_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg831"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
