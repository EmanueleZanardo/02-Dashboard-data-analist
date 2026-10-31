"""Test nuova scheda tab833 "Malteria:
ventilazione germinazione con
inverter + ventilazione essiccatoio
con inverter + recupero calore fumi
+ essiccatoio a pompa di calore
battono ventilazione tradizionale +
essiccatoio a gas?".

Business case deterministico di una
malteria guidato dalle TONNELLATE DI
MALTO prodotte in un anno: E_ger_base =
t_malto x e_ger_base; E_ger_alt =
t_malto x e_ger_alt (la ventilazione
germinazione con inverter riduce solo
la ventilazione germinazione);
E_ess_base = t_malto x e_ess_base;
E_ess_alt = t_malto x e_ess_alt (la
ventilazione essiccatoio con inverter
riduce solo la ventilazione
essiccatoio); E_pdc_alt = t_malto x
e_pdc_alt (l'essiccatoio a pompa di
calore, COP 4: 60 kWh_e/t erogano 240
kWh_th/t, GIA' dentro E_alt); E_base =
E_ger_base + E_ess_base; E_alt =
E_ger_alt + E_ess_alt + E_pdc_alt;
gas_base = t_malto x g_base; gas_alt =
t_malto x g_alt (300 nel demo: 900 -
360 recupero calore fumi senza
elettricita' - 240 pompa di calore, per
un risparmio gas totale di 600 kWh/t,
ma E_alt e' SUPERIORE a E_base: 95
contro 50 kWh_e/t, e un prezzo
elettricita' piu' alto PEGGIORA il
caso); C_base = E_base x p_el +
gas_base x p_gas + OM_base; C_alt =
E_alt x p_el + gas_alt x p_gas + OM_alt
(prezzi in EUR/kWh, nessuna conversione
/ 1000); risparmio = C_base - C_alt;
CO2 evitata = (E_base x 0,25 + gas_base
x 0,20 - E_alt x 0,25 - gas_alt x 0,20)
/ 1000 (fattori letterali); flussi
[-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato
>= 0); breakeven gas = (E_alt x p_el +
OM_alt - E_base x p_el - OM_base) /
(gas_base - gas_alt) EUR/kWh, None se
gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo
il breakeven e' 0,0215 EUR/kWh
(numeratore 129.000 EUR, denominatore
6.000.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(t_malto <= 0, specifici negativi, prezzi <= 0,
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
previsto (t_malto, prezzi, CAPEX, vita). Gli zeri
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
Distinzione esplicita: distinto dalla
segheria (segatura del legname: qui solo
malto), dal betonaggio (miscelazione del
calcestruzzo: qui niente cemento), dal
birrificio (produzione di birra: qui solo
malto, nessuna fermentazione) e
dall'essiccatoio cerealicolo generico
(essiccazione di granella: qui germinazione
piu' essiccatoio del malto con recupero
calore fumi): qui driver TONNELLATE DI
MALTO + VENTILAZIONE GERMINAZIONE CON
INVERTER + VENTILAZIONE ESSICCATOIO CON
INVERTER + RECUPERO CALORE FUMI +
ESSICCATOIO A POMPA DI CALORE.

Demo (malteria): 10.000 t di malto
prodotte in un anno, ventilazione
germinazione specifica base 30,0
(300.000 kWh_e/anno) e alternativa
21,0 (210.000 kWh_e/anno), ventilazione
essiccatoio specifica base 20,0
(200.000 kWh_e/anno) e alternativa
14,0 (140.000 kWh_e/anno), essiccatoio
a pompa di calore alternativa 60,0
(600.000 kWh_e/anno, gia' dentro E_alt,
COP 4: 240 kWh_th/t), elettricita' base
500.000 e alternativa 950.000
kWh_e/anno, gas specifico base 900,0
(9.000.000 kWh/anno) e alternativo
300,0 (3.000.000 kWh/anno: risparmio gas
600 kWh/t = 360 recupero calore + 240
pompa di calore), prezzi elettricita'
0,22 e gas 0,06 EUR/kWh, O&M base
50.000 e alternativo 80.000 EUR/anno,
CAPEX 1.700.000 EUR (recupero calore
600.000 + pompa di calore 900.000 +
inverter 200.000), WACC 5 %, vita 15
anni, tolleranza 5 % del CAPEX.
Valori calcolati eseguendo
mh833_demo_calcoli(): E_base 500.000,
E_alt 950.000, gas_base 9.000.000,
gas_alt 3.000.000, C_base 700.000,
C_alt 469.000, risparmio 231.000,
CO2_base 1.925,0, CO2_alt 837,50,
CO2_evitata 1.087,50, VAN
697701,0068197162, TIR
10,583478164582454 %, payback 8,
breakeven gas 0,0215 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w833_malteria.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w835_helpers import (
    demo_calcoli,
    mh833_breakeven_gas,
    mh833_c_alt,
    mh833_c_base,
    mh833_calcola,
    mh833_co2_alt,
    mh833_co2_base,
    mh833_co2_evitata,
    mh833_csv,
    mh833_demo,
    mh833_demo_calcoli,
    mh833_e_alt,
    mh833_e_base,
    mh833_e_ess_alt,
    mh833_e_ess_base,
    mh833_e_ger_alt,
    mh833_e_ger_base,
    mh833_e_pdc_alt,
    mh833_flussi,
    mh833_gas_alt,
    mh833_gas_base,
    mh833_int_pos,
    mh833_nneg,
    mh833_num,
    mh833_payback,
    mh833_pos,
    mh833_risparmio,
    mh833_tir,
    mh833_valida,
    mh833_van,
    mh833_verdetto,
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


_HELPERS_PATH = _risolvi("w835_helpers.py")
_UI_PATH = _risolvi("w835_ui.py")


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
    "e_ger_base_kwh_e_anno": 300000.0,
    "e_ger_alt_kwh_e_anno": 210000.0,
    "e_ess_base_kwh_e_anno": 200000.0,
    "e_ess_alt_kwh_e_anno": 140000.0,
    "e_pdc_alt_kwh_e_anno": 600000.0,
    "e_base_kwh_e_anno": 500000.0,
    "e_alt_kwh_e_anno": 950000.0,
    "gas_base_kwh_anno": 9000000.0,
    "gas_alt_kwh_anno": 3000000.0,
    "c_base_eur_anno": 700000.0,
    "c_alt_eur_anno": 469000.0,
    "risparmio_eur_anno": 231000.0,
    "co2_base_t_anno": 1925.0,
    "co2_alt_t_anno": 837.5,
    "co2_evitata_t_anno": 1087.5,
    "van": 697701.0068197162,
    "tir": 10.583478164582454,
    "payback": 8,
    "breakeven_gas_eur_kwh": 0.0215,
}


def _demo_kwargs(**over):
    kw = dict(mh833_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh833_num(3, "x"), 3.0)
        self.assertEqual(mh833_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh833_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh833_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh833_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh833_pos(0, "x")
        with self.assertRaises(ValueError):
            mh833_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh833_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh833_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_ger_ess_pdc_e_base(self):
        self.assertEqual(mh833_e_ger_base(10000, 30.0), 300000.0)
        self.assertEqual(mh833_e_ger_alt(10000, 21.0), 210000.0)
        self.assertEqual(mh833_e_ess_base(10000, 20.0), 200000.0)
        self.assertEqual(mh833_e_ess_alt(10000, 14.0), 140000.0)
        self.assertEqual(mh833_e_pdc_alt(10000, 60.0), 600000.0)
        self.assertEqual(mh833_e_base(300000.0, 200000.0), 500000.0)
        self.assertEqual(mh833_e_alt(210000.0, 140000.0, 600000.0), 950000.0)

    def test_gas_base_alt(self):
        self.assertEqual(mh833_gas_base(10000, 900.0), 9000000.0)
        self.assertEqual(mh833_gas_alt(10000, 300.0), 3000000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh833_c_base(500000.0, 0.22, 9000000.0, 0.06, 50000), 700000.0)
        self.assertEqual(mh833_c_alt(950000.0, 0.22, 3000000.0, 0.06, 80000), 469000.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh833_risparmio(700000.0, 469000.0), 231000.0)
        self.assertEqual(mh833_risparmio(469000.0, 700000.0), -231000.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh833_co2_base(500000.0, 9000000.0), 1925.0, places=9)
        self.assertAlmostEqual(mh833_co2_alt(950000.0, 3000000.0), 837.5, places=9)
        self.assertAlmostEqual(
            mh833_co2_evitata(500000.0, 9000000.0, 950000.0, 3000000.0), 1087.5, places=9)

    def test_e_alt_superiore_a_e_base(self):
        bc = mh833_demo_calcoli()
        self.assertGreater(bc["e_alt_kwh_e_anno"], bc["e_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"] / bc["t_malto"], 95.0, places=9)
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"] / bc["t_malto"], 50.0, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh833_breakeven_gas(950000.0, 0.22, 80000, 500000.0, 50000, 9000000.0, 3000000.0)
        self.assertAlmostEqual(be, 0.0215, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh833_breakeven_gas(1000.0, 0.22, 1000, 500000.0, 50000, 9000000.0, 3000000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh833_breakeven_gas(950000.0, 0.22, 80000, 500000.0, 50000, 9000000.0, 9000000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh833_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh833_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh833_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh833_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh833_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh833_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh833_flussi(1700000, 231000.0, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -1700000)
        self.assertTrue(all(f == 231000.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh833_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 697701.0068197162, places=6)
        self.assertEqual(mh833_van([-1700000] + [231000.0] * 15, 0.0), 1765000.0)

    def test_tir_demo(self):
        bc = mh833_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 10.583478164582454, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh833_payback([-1700000] + [231000.0] * 15), 8)
        self.assertEqual(mh833_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh833_payback([-1700000] + [100.0] * 15))

    def test_verdetto(self):
        self.assertEqual(mh833_verdetto(231000.0, 100.0, 1700000, 5.0), "CONVIENTE")
        self.assertEqual(mh833_verdetto(231000.0, -50000.0, 1700000, 5.0), "MARGINALE")
        self.assertEqual(mh833_verdetto(231000.0, -200000.0, 1700000, 5.0), "NON_CONVIENTE")
        self.assertEqual(mh833_verdetto(0.0, 100.0, 1700000, 5.0), "NON_CALCOLABILE")
        self.assertEqual(mh833_verdetto(-100.0, 100.0, 1700000, 5.0), "NON_CALCOLABILE")
        self.assertEqual(mh833_verdetto(None, 100.0, 1700000, 5.0), "NON_CALCOLABILE")
        self.assertEqual(mh833_verdetto(231000.0, 0.0, 1700000, 5.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh833_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("t_malto", "10000"), ("t_malto", float("nan")),
                            ("t_malto", float("inf")), ("t_malto", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh833_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"t_malto": 0}, {"t_malto": -1}, {"e_ger_base_kwh_e_t": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh833_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh833_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh833_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh833_valida(**_demo_kwargs(
            e_ger_base_kwh_e_t=0, e_ess_base_kwh_e_t=0,
            g_base_kwh_t=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh833_demo()
        self.assertEqual(d["t_malto"], 10000)
        self.assertEqual(d["e_ger_base_kwh_e_t"], 30.0)
        self.assertEqual(d["e_ger_alt_kwh_e_t"], 21.0)
        self.assertEqual(d["e_ess_base_kwh_e_t"], 20.0)
        self.assertEqual(d["e_ess_alt_kwh_e_t"], 14.0)
        self.assertEqual(d["e_pdc_alt_kwh_e_t"], 60.0)
        self.assertEqual(d["g_base_kwh_t"], 900.0)
        self.assertEqual(d["g_alt_kwh_t"], 300.0)
        self.assertEqual(d["capex"], 1700000)
        self.assertEqual(d["vita_anni"], 15)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh833_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh833_demo_calcoli()
        self.assertEqual(bc["e_ger_base_kwh_e_anno"], 300000.0)
        self.assertEqual(bc["e_ger_alt_kwh_e_anno"], 210000.0)
        self.assertEqual(bc["e_ess_base_kwh_e_anno"], 200000.0)
        self.assertEqual(bc["e_ess_alt_kwh_e_anno"], 140000.0)
        self.assertEqual(bc["e_pdc_alt_kwh_e_anno"], 600000.0)
        self.assertEqual(bc["c_base_eur_anno"], 700000.0)
        self.assertEqual(bc["c_alt_eur_anno"], 469000.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh833_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7], -83000.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], 148000.0)

    def test_demo_tabella_righe(self):
        bc = mh833_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Malto (t/anno)", voci)
        self.assertIn("Ventilazione germinazione baseline (kWh_e/anno)", voci)
        self.assertIn("Pompa di calore alternativa (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh833_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_ger_base_kwh_e_anno"] + bc["e_ess_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"],
                               bc["e_ger_alt_kwh_e_anno"] + bc["e_ess_alt_kwh_e_anno"] + bc["e_pdc_alt_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        t = 10000
        e_base = t * (30.0 + 20.0)
        e_alt = t * (21.0 + 14.0 + 60.0)
        gas_base = t * 900.0
        gas_alt = t * 300.0
        c_base = e_base * 0.22 + gas_base * 0.06 + 50000
        c_alt = e_alt * 0.22 + gas_alt * 0.06 + 80000
        bc = mh833_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh833_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_inverter_germinazione(self):
        r = mh833_calcola(**_demo_kwargs(e_ger_alt_kwh_e_t=30.0))
        self.assertEqual(r["risparmio_eur_anno"], 211200.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 492183.77766374266, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.0248, places=12)

    def test_variante_senza_inverter_essiccatoio(self):
        r = mh833_calcola(**_demo_kwargs(e_ess_alt_kwh_e_t=20.0))
        self.assertEqual(r["risparmio_eur_anno"], 217800.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 560689.5207157345, places=6)
        self.assertEqual(r["payback"], 8)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.0237, places=12)

    def test_variante_senza_recupero_calore_non_convinte(self):
        r = mh833_calcola(**_demo_kwargs(g_alt_kwh_t=660.0))
        self.assertEqual(r["risparmio_eur_anno"], 15000.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -1544305.129427291, places=6)
        self.assertIsNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.05375, places=12)

    def test_variante_senza_pompa_calore(self):
        r = mh833_calcola(**_demo_kwargs(e_pdc_alt_kwh_e_t=0.0, g_alt_kwh_t=540.0))
        self.assertEqual(r["risparmio_eur_anno"], 219000.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 573145.1103615493, places=6)
        self.assertEqual(r["payback"], 8)
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_2500000_marginale(self):
        r = mh833_calcola(**_demo_kwargs(capex=2500000))
        self.assertAlmostEqual(r["van"], -102298.9931802839, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 11)

    def test_variante_gas_basso_e_alto(self):
        basso = mh833_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], -9000.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(basso["van"], -1793416.9223436255, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh833_calcola(**_demo_kwargs(p_gas=0.10))
        self.assertEqual(alto["risparmio_eur_anno"], 471000.0)
        self.assertAlmostEqual(alto["van"], 3188818.935983062, places=6)
        self.assertAlmostEqual(alto["tir"], 26.931352088622816, places=6)
        self.assertEqual(alto["payback"], 4)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_elettricita_piu_meno_20(self):
        meno = mh833_calcola(**_demo_kwargs(p_el=0.176))
        self.assertEqual(meno["risparmio_eur_anno"], 250800.0)
        self.assertAlmostEqual(meno["van"], 903218.2359756944, places=6)
        self.assertAlmostEqual(meno["tir"], 12.089866622164458, places=6)
        self.assertEqual(meno["payback"], 7)
        piu = mh833_calcola(**_demo_kwargs(p_el=0.264))
        self.assertEqual(piu["risparmio_eur_anno"], 211200.0)
        self.assertAlmostEqual(piu["van"], 492183.77766374266, places=6)
        self.assertAlmostEqual(piu["tir"], 9.024080716053373, places=6)
        self.assertEqual(piu["payback"], 9)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_elettricita_alta_peggiora_il_caso(self):
        demo = mh833_demo_calcoli()
        meno = mh833_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh833_calcola(**_demo_kwargs(p_el=0.264))
        self.assertGreater(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(demo["e_alt_kwh_e_anno"], demo["e_base_kwh_e_anno"])

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh833_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 1765000.0)
        self.assertEqual(zero["payback"], 8)
        dieci = mh833_calcola(**_demo_kwargs(vita_anni=10))
        self.assertAlmostEqual(dieci["van"], 83720.76864169119, places=6)
        self.assertEqual(dieci["verdetto"], "CONVIENTE")
        self.assertEqual(dieci["payback"], 8)
        nove = mh833_calcola(**_demo_kwargs(vita_anni=9))
        self.assertAlmostEqual(nove["van"], -58093.192926224176, places=6)
        self.assertEqual(nove["verdetto"], "MARGINALE")
        self.assertEqual(nove["payback"], 8)

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh833_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh833_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh833_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_ger_e_pompa_calore(self):
        base = mh833_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh833_calcola(**_demo_kwargs(e_ger_alt_kwh_e_t=25.0))["risparmio_eur_anno"], base)
        self.assertLess(mh833_calcola(**_demo_kwargs(g_alt_kwh_t=350.0))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh833_demo_calcoli()
        b = mh833_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh833_demo()
        attese = {"t_malto", "e_ger_base_kwh_e_t", "e_ger_alt_kwh_e_t",
                  "e_ess_base_kwh_e_t", "e_ess_alt_kwh_e_t",
                  "e_pdc_alt_kwh_e_t",
                  "g_base_kwh_t", "g_alt_kwh_t", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["t_malto", "e_ger_base_kwh_e_t", "e_ger_alt_kwh_e_t",
                 "e_ess_base_kwh_e_t", "e_ess_alt_kwh_e_t",
                 "e_pdc_alt_kwh_e_t",
                 "g_base_kwh_t", "g_alt_kwh_t", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh833_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("t_malto", "10000"), ("t_malto", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh833_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh833_calcola(**_demo_kwargs(e_ger_base_kwh_e_t=0,
                                         e_ess_base_kwh_e_t=0,
                                         g_base_kwh_t=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh833_calcola(**_demo_kwargs(g_alt_kwh_t=900.0))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh833_calcola(**_demo_kwargs(om_alt=400000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh833_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh833_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh833_demo_calcoli()
        csv = mh833_csv(bc, dict(mh833_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh833_demo_calcoli()
        csv = mh833_csv(bc, dict(mh833_demo()))
        self.assertIn("risparmio_eur_anno;231000.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh833_demo_calcoli()
        csv = mh833_csv(bc, dict(mh833_demo()))
        for chiave in mh833_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh832_", src)
        self.assertNotIn("mh831_", src)
        self.assertNotIn("mh830_", src)
        self.assertNotIn("mh829_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab833:"), 1)
        self.assertTrue(src.startswith("    # W835"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Malteria: ventilazione germinazione", src)
        self.assertIn("essiccatoio a pompa di calore", src)
        self.assertIn("🌾 Malteria: ventilazione germinazione con inverter + ventilazione essiccatoio con inverter + recupero calore fumi + essiccatoio a pompa di calore battono ventilazione tradizionale + essiccatoio a gas?", src)
        self.assertNotIn("tab832", src)
        self.assertNotIn("tab831", src)
        self.assertNotIn("tab830", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh832_", "mh831_", "mh830_", "mh829_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh832_", src)
        self.assertNotIn("st832_", src)
        self.assertNotIn("mh831_", src)
        self.assertNotIn("st831_", src)
        chiavi = re.findall(r'key="(st833_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st833_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st833_calcola"', src)
        self.assertIn('key="st833_csv"', src)
        self.assertIn('key="st833_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def833\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh833_demo().keys()), lette - set(mh833_demo().keys()))
        self.assertEqual(lette, set(mh833_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc833\['([^']+)'\]", src))
        attese = set(mh833_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg833"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)


class TestAppPresenza(unittest.TestCase):
    def test_app_contiene_tab833_e_titolo(self):
        self.assertTrue(os.path.exists(_APP_PATH), f"app.py non trovato: {_APP_PATH} (apply tab833 non ancora fatto)")
        src = open(_APP_PATH, encoding="utf-8").read()
        self.assertIn("tab833", src)
        self.assertIn("Malteria: ventilazione germinazione con inverter + ventilazione essiccatoio con inverter + recupero calore fumi + essiccatoio a pompa di calore battono ventilazione tradizionale + essiccatoio a gas?", src)


if __name__ == "__main__":
    unittest.main()
