"""Test nuova scheda tab832 "Segheria:
seghe efficienti + aspirazione con
inverter + essiccatoio a pompa di calore
battono seghe tradizionali +
aspirazione tradizionale + essiccatoio
a gas?".

Business case deterministico di una
segheria guidato dai M3 DI LEGNAME
segati in un anno: E_seg_base = m3 x
e_seg_base; E_seg_alt = m3 x e_seg_alt
(le seghe efficienti riducono solo la
segatura); E_asp_base = m3 x e_asp_base;
E_asp_alt = m3 x e_asp_alt
(l'aspirazione con inverter riduce solo
l'aspirazione); E_pdc_alt = m3 x
e_pdc_alt (l'essiccatoio a pompa di
calore, GIA' dentro E_alt); E_base =
E_seg_base + E_asp_base; E_alt =
E_seg_alt + E_asp_alt + E_pdc_alt;
gas_base = m3 x g_base; gas_alt = m3 x
g_alt (0 nel demo: l'essiccatoio a pompa
di calore azzera il gas, quindi il
risparmio gas e' totale, ma E_alt e'
SUPERIORE a E_base: 19,20 contro 10,00
kWh_e/m3, e un prezzo elettricita' piu'
alto PEGGIORA il caso); C_base = E_base
x p_el + gas_base x p_gas + OM_base;
C_alt = E_alt x p_el + gas_alt x p_gas
+ OM_alt (prezzi in EUR/kWh, nessuna
conversione / 1000); risparmio = C_base
- C_alt; CO2 evitata = (E_base x 0,25 +
gas_base x 0,20 - E_alt x 0,25 - gas_alt
x 0,20) / 1000 (fattori letterali);
flussi [-CAPEX, risparmio x vita]; VAN,
TIR, payback (primo anno con cumulato
>= 0); breakeven gas = (E_alt x p_el +
OM_alt - E_base x p_el - OM_base) /
(gas_base - gas_alt) EUR/kWh, None se
gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo
il breakeven e' 0,046233333333333335
EUR/kWh (numeratore 55.480 EUR,
denominatore 1.200.000 kWh/anno).
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
Distinzione esplicita: distinto dal
segheria (segatura del legname:
qui solo taglio, aspirazione ed
essiccazione del legname), dall'asfalto
(legante bitume: qui niente bitume), dal
cantiere (getto o posa: qui solo
lavorazione in segheria), dal cementificio
(produzione del cemento: qui niente
cemento) e dalla falegnameria (produzione
di mobili: qui nessuna produzione di
mobili): qui driver M3 DI LEGNAME +
SEGHE EFFICIENTI + ASPIRAZIONE CON
INVERTER + ESSICCATOIO A POMPA DI CALORE.

Demo (segheria): 20.000 m3 di legname
segati in un anno, segatura specifica
base 8,0 (160.000 kWh_e/anno) e
alternativa 6,0 (120.000 kWh_e/anno),
aspirazione specifica base 2,0 (40.000
kWh_e/anno) e alternativa 1,2 (24.000
kWh_e/anno), essiccatoio a pompa di
calore alternativa 12,0 (240.000
kWh_e/anno, gia' dentro E_alt),
elettricita' base 200.000 e alternativa
384.000 kWh_e/anno, gas specifico base
60,0 (1.200.000 kWh/anno) e alternativo
0,0 (0 kWh/anno: l'essiccatoio a pompa
di calore azzera il gas), prezzi
elettricita' 0,22 e gas 0,06 EUR/kWh,
O&M base 30.000 e alternativo 45.000
EUR/anno, CAPEX 150.000 EUR, WACC 5 %,
vita 15 anni, tolleranza 5 % del CAPEX.
Valori calcolati eseguendo
mh832_demo_calcoli(): E_base 200.000,
E_alt 384.000, gas_base 1.200.000,
gas_alt 0, C_base 146.000, C_alt
129.480, risparmio 16.520, CO2_base
290,0, CO2_alt 96,0, CO2_evitata 194,0,
VAN 21471,950790743358, TIR
7,04880696351682 %, payback 10,
breakeven gas 0,046233333333333335
EUR/kWh, verdetto CONVIENTE.

Destinazione nel repo: tests/test_w832_segheria.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w834_helpers import (
    demo_calcoli,
    mh832_breakeven_gas,
    mh832_c_alt,
    mh832_c_base,
    mh832_calcola,
    mh832_co2_alt,
    mh832_co2_base,
    mh832_co2_evitata,
    mh832_csv,
    mh832_demo,
    mh832_demo_calcoli,
    mh832_e_alt,
    mh832_e_base,
    mh832_e_asp_alt,
    mh832_e_asp_base,
    mh832_e_seg_alt,
    mh832_e_seg_base,
    mh832_e_pdc_alt,
    mh832_flussi,
    mh832_gas_alt,
    mh832_gas_base,
    mh832_int_pos,
    mh832_nneg,
    mh832_num,
    mh832_payback,
    mh832_pos,
    mh832_risparmio,
    mh832_tir,
    mh832_valida,
    mh832_van,
    mh832_verdetto,
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


_HELPERS_PATH = _risolvi("w834_helpers.py")
_UI_PATH = _risolvi("w834_ui.py")

_DEMO = {
    "e_seg_base_kwh_e_anno": 160000.0,
    "e_seg_alt_kwh_e_anno": 120000.0,
    "e_asp_base_kwh_e_anno": 40000.0,
    "e_asp_alt_kwh_e_anno": 24000.0,
    "e_pdc_alt_kwh_e_anno": 240000.0,
    "e_base_kwh_e_anno": 200000.0,
    "e_alt_kwh_e_anno": 384000.0,
    "gas_base_kwh_anno": 1200000.0,
    "gas_alt_kwh_anno": 0.0,
    "c_base_eur_anno": 146000.0,
    "c_alt_eur_anno": 129480.0,
    "risparmio_eur_anno": 16520.0,
    "co2_base_t_anno": 290.0,
    "co2_alt_t_anno": 96.0,
    "co2_evitata_t_anno": 194.0,
    "van": 21471.950790743358,
    "tir": 7.04880696351682,
    "payback": 10,
    "breakeven_gas_eur_kwh": 0.046233333333333335,
}


def _demo_kwargs(**over):
    kw = dict(mh832_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh832_num(3, "x"), 3.0)
        self.assertEqual(mh832_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh832_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh832_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh832_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh832_pos(0, "x")
        with self.assertRaises(ValueError):
            mh832_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh832_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh832_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_seg_asp_pdc_e_base(self):
        self.assertEqual(mh832_e_seg_base(20000, 8.0), 160000.0)
        self.assertEqual(mh832_e_seg_alt(20000, 6.0), 120000.0)
        self.assertEqual(mh832_e_asp_base(20000, 2.0), 40000.0)
        self.assertAlmostEqual(mh832_e_asp_alt(20000, 1.2), 24000.0, places=6)
        self.assertEqual(mh832_e_pdc_alt(20000, 12.0), 240000.0)
        self.assertEqual(mh832_e_base(160000.0, 40000.0), 200000.0)
        self.assertAlmostEqual(mh832_e_alt(120000.0, 24000.0, 240000.0), 384000.0, places=6)

    def test_gas_base_alt_azzerato(self):
        self.assertEqual(mh832_gas_base(20000, 60.0), 1200000.0)
        self.assertEqual(mh832_gas_alt(20000, 0.00), 0.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh832_c_base(200000.0, 0.22, 1200000.0, 0.06, 30000), 146000.0)
        self.assertEqual(mh832_c_alt(384000.0, 0.22, 0.0, 0.06, 45000), 129480.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh832_risparmio(146000.0, 129480.0), 16520.0)
        self.assertEqual(mh832_risparmio(129480.0, 146000.0), -16520.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh832_co2_base(200000.0, 1200000.0), 290.0, places=9)
        self.assertAlmostEqual(mh832_co2_alt(384000.0, 0.0), 96.0, places=9)
        self.assertAlmostEqual(
            mh832_co2_evitata(200000.0, 1200000.0, 384000.0, 0.0), 194.0, places=9)

    def test_e_alt_superiore_a_e_base(self):
        bc = mh832_demo_calcoli()
        self.assertGreater(bc["e_alt_kwh_e_anno"], bc["e_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"] / bc["m3"], 19.20, places=9)
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"] / bc["m3"], 10.00, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh832_breakeven_gas(384000.0, 0.22, 45000, 200000.0, 30000, 1200000.0, 0.0)
        self.assertAlmostEqual(be, 0.046233333333333335, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh832_breakeven_gas(1000.0, 0.22, 1000, 200000.0, 30000, 1200000.0, 0.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh832_breakeven_gas(384000.0, 0.22, 45000, 200000.0, 30000, 1200000.0, 1200000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh832_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh832_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh832_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh832_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh832_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh832_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh832_flussi(150000, 16520.0, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -150000)
        self.assertTrue(all(f == 16520.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh832_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 21471.950790743358, places=6)
        self.assertEqual(mh832_van([-150000] + [16520.0] * 15, 0.0), 97800.0)

    def test_tir_demo(self):
        bc = mh832_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 7.04880696351682, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh832_payback([-150000] + [16520.0] * 15), 10)
        self.assertEqual(mh832_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh832_payback([-150000] + [100.0] * 15))

    def test_verdetto(self):
        self.assertEqual(mh832_verdetto(16520.0, 100.0, 150000, 5.0), "CONVIENTE")
        self.assertEqual(mh832_verdetto(16520.0, -5000.0, 150000, 5.0), "MARGINALE")
        self.assertEqual(mh832_verdetto(16520.0, -20000.0, 150000, 5.0), "NON_CONVIENTE")
        self.assertEqual(mh832_verdetto(0.0, 100.0, 150000, 5.0), "NON_CALCOLABILE")
        self.assertEqual(mh832_verdetto(-100.0, 100.0, 150000, 5.0), "NON_CALCOLABILE")
        self.assertEqual(mh832_verdetto(None, 100.0, 150000, 5.0), "NON_CALCOLABILE")
        self.assertEqual(mh832_verdetto(16520.0, 0.0, 150000, 5.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh832_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("m3", "20000"), ("m3", float("nan")),
                            ("m3", float("inf")), ("m3", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh832_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"m3": 0}, {"m3": -1}, {"e_seg_base_kwh_e_m3": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh832_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh832_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh832_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh832_valida(**_demo_kwargs(
            e_seg_base_kwh_e_m3=0, e_asp_base_kwh_e_m3=0,
            g_base_kwh_m3=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh832_demo()
        self.assertEqual(d["m3"], 20000)
        self.assertEqual(d["e_seg_base_kwh_e_m3"], 8.0)
        self.assertEqual(d["e_seg_alt_kwh_e_m3"], 6.0)
        self.assertEqual(d["e_asp_base_kwh_e_m3"], 2.0)
        self.assertEqual(d["e_asp_alt_kwh_e_m3"], 1.2)
        self.assertEqual(d["e_pdc_alt_kwh_e_m3"], 12.0)
        self.assertEqual(d["g_base_kwh_m3"], 60.0)
        self.assertEqual(d["g_alt_kwh_m3"], 0.00)
        self.assertEqual(d["capex"], 150000)
        self.assertEqual(d["vita_anni"], 15)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh832_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh832_demo_calcoli()
        self.assertEqual(bc["e_seg_base_kwh_e_anno"], 160000.0)
        self.assertEqual(bc["e_seg_alt_kwh_e_anno"], 120000.0)
        self.assertEqual(bc["e_asp_base_kwh_e_anno"], 40000.0)
        self.assertAlmostEqual(bc["e_asp_alt_kwh_e_anno"], 24000.0, places=6)
        self.assertEqual(bc["e_pdc_alt_kwh_e_anno"], 240000.0)
        self.assertEqual(bc["c_base_eur_anno"], 146000.0)
        self.assertEqual(bc["c_alt_eur_anno"], 129480.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh832_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[9], -1320.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[10], 15200.0)

    def test_demo_tabella_righe(self):
        bc = mh832_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Legname (m3/anno)", voci)
        self.assertIn("Segatura baseline (kWh_e/anno)", voci)
        self.assertIn("Pompa di calore alternativa (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh832_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_seg_base_kwh_e_anno"] + bc["e_asp_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"],
                               bc["e_seg_alt_kwh_e_anno"] + bc["e_asp_alt_kwh_e_anno"] + bc["e_pdc_alt_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        m3 = 20000
        e_base = m3 * (8.0 + 2.0)
        e_alt = m3 * (6.0 + 1.2 + 12.0)
        gas_base = m3 * 60.0
        gas_alt = m3 * 0.00
        c_base = e_base * 0.22 + gas_base * 0.06 + 30000
        c_alt = e_alt * 0.22 + gas_alt * 0.06 + 45000
        bc = mh832_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh832_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_seghe_non_convinte(self):
        r = mh832_calcola(**_demo_kwargs(e_seg_alt_kwh_e_m3=8.0))
        self.assertEqual(r["risparmio_eur_anno"], 7720.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -69869.03994524582, places=6)
        self.assertIsNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.053566666666666665, places=12)

    def test_variante_senza_aspirazione_non_convinte(self):
        r = mh832_calcola(**_demo_kwargs(e_asp_alt_kwh_e_m3=2.0))
        self.assertEqual(r["risparmio_eur_anno"], 13000.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -15064.44550365235, places=6)
        self.assertEqual(r["payback"], 12)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.049166666666666664, places=12)

    def test_variante_senza_pompa_calore_non_calcolabile(self):
        r = mh832_calcola(**_demo_kwargs(g_alt_kwh_m3=60.0))
        self.assertEqual(r["risparmio_eur_anno"], -55480.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_300000_non_convinte(self):
        r = mh832_calcola(**_demo_kwargs(capex=300000))
        self.assertAlmostEqual(r["van"], -128528.04920925666, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(r["payback"])

    def test_variante_gas_basso_e_alto(self):
        basso = mh832_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], -31480.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(basso["van"], -476751.635041925, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh832_calcola(**_demo_kwargs(p_gas=0.10))
        self.assertEqual(alto["risparmio_eur_anno"], 64520.0)
        self.assertAlmostEqual(alto["van"], 519695.53662341164, places=6)
        self.assertAlmostEqual(alto["tir"], 42.80806977079084, places=6)
        self.assertEqual(alto["payback"], 3)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_elettricita_piu_meno_20(self):
        meno = mh832_calcola(**_demo_kwargs(p_el=0.176))
        self.assertEqual(meno["risparmio_eur_anno"], 24616.0)
        self.assertAlmostEqual(meno["van"], 105505.66226785342, places=6)
        self.assertAlmostEqual(meno["tir"], 14.159222437209845, places=6)
        self.assertEqual(meno["payback"], 7)
        piu = mh832_calcola(**_demo_kwargs(p_el=0.264))
        self.assertEqual(piu["risparmio_eur_anno"], 8424.0)
        self.assertAlmostEqual(piu["van"], -62561.76068636671, places=6)
        self.assertAlmostEqual(piu["tir"], -2.070957906631579, places=6)
        self.assertIsNone(piu["payback"])
        self.assertEqual(piu["verdetto"], "NON_CONVIENTE")

    def test_elettricita_alta_peggiora_il_caso(self):
        demo = mh832_demo_calcoli()
        meno = mh832_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh832_calcola(**_demo_kwargs(p_el=0.264))
        self.assertGreater(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(demo["e_alt_kwh_e_anno"], demo["e_base_kwh_e_anno"])

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh832_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 97800.0)
        self.assertEqual(zero["payback"], 10)
        dieci = mh832_calcola(**_demo_kwargs(vita_anni=10))
        self.assertAlmostEqual(dieci["van"], -22436.93896986692, places=6)
        self.assertEqual(dieci["verdetto"], "NON_CONVIENTE")
        self.assertEqual(dieci["payback"], 10)
        dieci_marg = mh832_calcola(**_demo_kwargs(vita_anni=10, tolleranza_pct=20.0))
        self.assertEqual(dieci_marg["verdetto"], "MARGINALE")
        nove = mh832_calcola(**_demo_kwargs(vita_anni=9))
        self.assertAlmostEqual(nove["van"], -32578.78591836026, places=6)
        self.assertEqual(nove["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(nove["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh832_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh832_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh832_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_seg_e_pompa_calore(self):
        base = mh832_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh832_calcola(**_demo_kwargs(e_seg_alt_kwh_e_m3=7.0))["risparmio_eur_anno"], base)
        self.assertLess(mh832_calcola(**_demo_kwargs(g_alt_kwh_m3=5.00))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh832_demo_calcoli()
        b = mh832_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh832_demo()
        attese = {"m3", "e_seg_base_kwh_e_m3", "e_seg_alt_kwh_e_m3",
                  "e_asp_base_kwh_e_m3", "e_asp_alt_kwh_e_m3",
                  "e_pdc_alt_kwh_e_m3",
                  "g_base_kwh_m3", "g_alt_kwh_m3", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["m3", "e_seg_base_kwh_e_m3", "e_seg_alt_kwh_e_m3",
                 "e_asp_base_kwh_e_m3", "e_asp_alt_kwh_e_m3",
                 "e_pdc_alt_kwh_e_m3",
                 "g_base_kwh_m3", "g_alt_kwh_m3", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh832_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("m3", "20000"), ("m3", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh832_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh832_calcola(**_demo_kwargs(e_seg_base_kwh_e_m3=0,
                                         e_asp_base_kwh_e_m3=0,
                                         g_base_kwh_m3=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh832_calcola(**_demo_kwargs(g_alt_kwh_m3=60.0))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh832_calcola(**_demo_kwargs(om_alt=250000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh832_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh832_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh832_demo_calcoli()
        csv = mh832_csv(bc, dict(mh832_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh832_demo_calcoli()
        csv = mh832_csv(bc, dict(mh832_demo()))
        self.assertIn("risparmio_eur_anno;16520.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh832_demo_calcoli()
        csv = mh832_csv(bc, dict(mh832_demo()))
        for chiave in mh832_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh831_", src)
        self.assertNotIn("mh830_", src)
        self.assertNotIn("mh829_", src)
        self.assertNotIn("mh828_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab832:"), 1)
        self.assertTrue(src.startswith("    # W834"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Segheria: seghe efficienti", src)
        self.assertIn("essiccatoio a pompa di calore", src)
        self.assertNotIn("tab831", src)
        self.assertNotIn("tab830", src)
        self.assertNotIn("tab829", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh831_", "mh830_", "mh829_", "mh828_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh831_", src)
        self.assertNotIn("st831_", src)
        self.assertNotIn("mh830_", src)
        self.assertNotIn("st830_", src)
        chiavi = re.findall(r'key="(st832_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st832_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st832_calcola"', src)
        self.assertIn('key="st832_csv"', src)
        self.assertIn('key="st832_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def832\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh832_demo().keys()), lette - set(mh832_demo().keys()))
        self.assertEqual(lette, set(mh832_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc832\['([^']+)'\]", src))
        attese = set(mh832_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg832"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
