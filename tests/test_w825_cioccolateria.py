"""Test nuova scheda tab825 "Cioccolateria:
raffinazione con motori efficienti +
refrigerazione efficiente + recupero calore
su concheggio battono raffinazione
tradizionale + refrigerazione tradizionale
+ riscaldamento a gas?".

Business case deterministico di una
cioccolateria guidata dai KG DI CIOCCOLATO
prodotti/anno: E_raff_base = kg x e_raff_base;
E_raff_alt = kg x e_raff_alt (i motori
efficienti riducono solo la raffinazione);
E_fred_base = kg x e_fred_base; E_fred_alt =
kg x e_fred_alt (il freddo efficiente riduce
solo la refrigerazione); E_base = E_raff_base
+ E_fred_base; E_alt = E_raff_alt + E_fred_alt;
gas_base = kg x g_base; gas_alt = kg x g_alt
(il recupero calore RIDUCE il gas, non lo
azzera: gas_alt resta positivo nel demo);
C_base = E_base x p_el + gas_base x p_gas
+ OM_base; C_alt = E_alt x p_el + gas_alt x
p_gas + OM_alt (prezzi in EUR/kWh, nessuna
conversione / 1000); risparmio = C_base -
C_alt; CO2 evitata = (E_base x 0,25 +
gas_base x 0,202 - E_alt x 0,25 - gas_alt x
0,202) / 1000 (fattori letterali); flussi
[-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas = (E_alt x p_el + OM_alt -
E_base x p_el - OM_base) / (gas_base -
gas_alt) EUR/kWh, None se gas_base <=
gas_alt o numeratore < 0, SOGLIA MINIMA
quando esiste. Nel demo il breakeven e'
0,041666666666666664 EUR/kWh (numeratore
5.500 EUR, denominatore 132.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(kg <= 0, specifici negativi, prezzi <= 0,
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
previsto (kg, prezzi, CAPEX, vita). Gli zeri
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
caseificio (litri di latte, pastorizzazione:
qui niente litri di latte, niente
pastorizzazione), dalla gelateria (litri di
miscela, mantecazione: qui niente miscela
gelato, niente mantecazione), dal birrificio
(ettolitri di mosto, bollitura: qui niente
mosto, niente bollitura), dal pastificio
(kg di pasta, essiccazione: qui niente
pasta, niente essiccazione pasta), dalla
porcilaia (capi suini: qui niente capi
suini, niente ventilazione animale), dal
pollaio (capi avicoli: qui niente capi
avicoli, niente raffrescamento evaporativo
animale): qui driver KG DI CIOCCOLATO +
MOTORI EFFICIENTI + FREDDO EFFICIENTE +
RECUPERO CALORE SU CONCHEGGIO.

Demo (cioccolateria): 120.000 kg di
cioccolato, raffinazione specifica base 1,20
(144.000 kWh_e/anno) e alternativa 0,85
(102.000 kWh_e/anno), refrigerazione
specifica base 0,90 (108.000 kWh_e/anno) e
alternativa 0,60 (72.000 kWh_e/anno),
elettricita' base 252.000 e alternativa
174.000 kWh_e/anno, gas specifico base 1,80
(216.000 kWh/anno) e alternativo 0,70
(84.000 kWh/anno, il recupero riduce il gas
del 61,1 %, non lo azzera), prezzi
elettricita' 0,25 e gas 0,10 EUR/kWh, O&M
base 20.000 e alternativo 45.000 EUR/anno,
CAPEX 50.000 EUR, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh825_demo_calcoli(): E_base
252.000, E_alt 174.000, gas_base 216.000,
gas_alt 84.000, C_base 104.600, C_alt 96.900,
risparmio 7.700, CO2_base 106,632, CO2_alt
60,468, CO2_evitata 46,164, VAN
29923,36689399055, TIR 12,907125131592062 %,
payback 7, breakeven gas
0,041666666666666664 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w825_cioccolateria.py
"""

import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w827_helpers import (
    demo_calcoli,
    mh825_breakeven_gas,
    mh825_c_alt,
    mh825_c_base,
    mh825_calcola,
    mh825_co2_alt,
    mh825_co2_base,
    mh825_co2_evitata,
    mh825_csv,
    mh825_demo,
    mh825_demo_calcoli,
    mh825_e_alt,
    mh825_e_base,
    mh825_e_fred_alt,
    mh825_e_fred_base,
    mh825_e_raff_alt,
    mh825_e_raff_base,
    mh825_flussi,
    mh825_gas_alt,
    mh825_gas_base,
    mh825_int_pos,
    mh825_nneg,
    mh825_num,
    mh825_payback,
    mh825_pos,
    mh825_risparmio,
    mh825_tir,
    mh825_valida,
    mh825_van,
    mh825_verdetto,
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


_HELPERS_PATH = _risolvi("w827_helpers.py")
_UI_PATH = _risolvi("w827_ui.py")

_DEMO = {
    "e_raff_base_kwh_e_anno": 144000.0,
    "e_raff_alt_kwh_e_anno": 102000.0,
    "e_fred_base_kwh_e_anno": 108000.0,
    "e_fred_alt_kwh_e_anno": 72000.0,
    "e_base_kwh_e_anno": 252000.0,
    "e_alt_kwh_e_anno": 174000.0,
    "gas_base_kwh_anno": 216000.0,
    "gas_alt_kwh_anno": 84000.0,
    "c_base_eur_anno": 104600.0,
    "c_alt_eur_anno": 96900.0,
    "risparmio_eur_anno": 7700.0,
    "co2_base_t_anno": 106.632,
    "co2_alt_t_anno": 60.468,
    "co2_evitata_t_anno": 46.164,
    "van": 29923.36689399055,
    "tir": 12.907125131592062,
    "payback": 7,
    "breakeven_gas_eur_kwh": 0.041666666666666664,
}


def _demo_kwargs(**over):
    kw = dict(mh825_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh825_num(3, "x"), 3.0)
        self.assertEqual(mh825_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh825_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh825_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh825_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh825_pos(0, "x")
        with self.assertRaises(ValueError):
            mh825_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh825_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh825_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_raff_fred_e_base(self):
        self.assertEqual(mh825_e_raff_base(120000, 1.20), 144000.0)
        self.assertEqual(mh825_e_raff_alt(120000, 0.85), 102000.0)
        self.assertEqual(mh825_e_fred_base(120000, 0.90), 108000.0)
        self.assertEqual(mh825_e_fred_alt(120000, 0.60), 72000.0)
        self.assertEqual(mh825_e_base(144000.0, 108000.0), 252000.0)
        self.assertEqual(mh825_e_alt(102000.0, 72000.0), 174000.0)

    def test_gas_base_alt(self):
        self.assertEqual(mh825_gas_base(120000, 1.80), 216000.0)
        self.assertEqual(mh825_gas_alt(120000, 0.70), 84000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh825_c_base(252000.0, 0.25, 216000.0, 0.10, 20000), 104600.0)
        self.assertEqual(mh825_c_alt(174000.0, 0.25, 84000.0, 0.10, 45000), 96900.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh825_risparmio(104600.0, 96900.0), 7700.0)
        self.assertEqual(mh825_risparmio(96900.0, 104600.0), -7700.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh825_co2_base(252000.0, 216000.0), 106.632, places=9)
        self.assertAlmostEqual(mh825_co2_alt(174000.0, 84000.0), 60.468, places=9)
        self.assertAlmostEqual(
            mh825_co2_evitata(252000.0, 216000.0, 174000.0, 84000.0), 46.164, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh825_breakeven_gas(174000.0, 0.25, 45000, 252000.0, 20000, 216000.0, 84000.0)
        self.assertAlmostEqual(be, 0.041666666666666664, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh825_breakeven_gas(1000.0, 0.25, 1000, 252000.0, 20000, 216000.0, 84000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh825_breakeven_gas(174000.0, 0.25, 45000, 252000.0, 20000, 84000.0, 84000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh825_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh825_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh825_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh825_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh825_calcola(**_demo_kwargs(p_gas=be + 0.01))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh825_calcola(**_demo_kwargs(p_gas=be - 0.01))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh825_flussi(50000, 7700.0, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -50000)
        self.assertTrue(all(f == 7700.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh825_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 29923.36689399055, places=6)
        self.assertEqual(mh825_van([-50000] + [7700.0] * 15, 0.0), 65500.0)

    def test_tir_demo(self):
        bc = mh825_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 12.907125131592062, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh825_payback([-50000] + [7700.0] * 15), 7)
        self.assertEqual(mh825_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh825_payback([-50000] + [100.0] * 15))

    def test_verdetto(self):
        self.assertEqual(mh825_verdetto(7700.0, 100.0, 50000, 10.0), "CONVIENTE")
        self.assertEqual(mh825_verdetto(4700.0, -1215.61, 50000, 10.0), "MARGINALE")
        self.assertEqual(mh825_verdetto(7700.0, -20076.63, 50000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh825_verdetto(0.0, 100.0, 50000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh825_verdetto(-100.0, 100.0, 50000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh825_verdetto(None, 100.0, 50000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh825_verdetto(7700.0, 0.0, 50000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh825_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("kg", "120000"), ("kg", float("nan")),
                            ("kg", float("inf")), ("kg", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh825_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"kg": 0}, {"kg": -1}, {"e_raff_base_kwh_e_kg": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh825_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh825_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh825_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh825_valida(**_demo_kwargs(
            e_raff_base_kwh_e_kg=0, e_fred_base_kwh_e_kg=0,
            g_base_kwh_kg=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh825_demo()
        self.assertEqual(d["kg"], 120000)
        self.assertEqual(d["e_raff_base_kwh_e_kg"], 1.20)
        self.assertEqual(d["e_raff_alt_kwh_e_kg"], 0.85)
        self.assertEqual(d["e_fred_base_kwh_e_kg"], 0.90)
        self.assertEqual(d["e_fred_alt_kwh_e_kg"], 0.60)
        self.assertEqual(d["g_base_kwh_kg"], 1.80)
        self.assertEqual(d["g_alt_kwh_kg"], 0.70)
        self.assertEqual(d["capex"], 50000)
        self.assertEqual(d["vita_anni"], 15)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh825_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh825_demo_calcoli()
        self.assertEqual(bc["e_raff_base_kwh_e_anno"], 144000.0)
        self.assertEqual(bc["e_raff_alt_kwh_e_anno"], 102000.0)
        self.assertEqual(bc["e_fred_base_kwh_e_anno"], 108000.0)
        self.assertEqual(bc["e_fred_alt_kwh_e_anno"], 72000.0)
        self.assertEqual(bc["c_base_eur_anno"], 104600.0)
        self.assertEqual(bc["c_alt_eur_anno"], 96900.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh825_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[6], -3800.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7], 3900.0)

    def test_demo_tabella_righe(self):
        bc = mh825_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Kg cioccolato (kg/anno)", voci)
        self.assertIn("Raffinazione baseline (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh825_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_raff_base_kwh_e_anno"] + bc["e_fred_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        kg = 120000
        e_base = kg * (1.20 + 0.90)
        e_alt = kg * (0.85 + 0.60)
        gas_base = kg * 1.80
        gas_alt = kg * 0.70
        c_base = e_base * 0.25 + gas_base * 0.10 + 20000
        c_alt = e_alt * 0.25 + gas_alt * 0.10 + 45000
        bc = mh825_demo_calcoli()
        self.assertEqual(bc["e_base_kwh_e_anno"], e_base)
        self.assertEqual(bc["e_alt_kwh_e_anno"], e_alt)
        self.assertEqual(bc["gas_base_kwh_anno"], gas_base)
        self.assertEqual(bc["gas_alt_kwh_anno"], gas_alt)
        self.assertEqual(bc["c_base_eur_anno"], c_base)
        self.assertEqual(bc["c_alt_eur_anno"], c_alt)
        self.assertEqual(bc["risparmio_eur_anno"], c_base - c_alt)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh825_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_motori_non_calcolabile(self):
        r = mh825_calcola(**_demo_kwargs(e_raff_alt_kwh_e_kg=1.20))
        self.assertEqual(r["risparmio_eur_anno"], -2800.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.12121212121212122, places=12)

    def test_variante_senza_freddo_non_calcolabile(self):
        r = mh825_calcola(**_demo_kwargs(e_fred_alt_kwh_e_kg=0.90))
        self.assertEqual(r["risparmio_eur_anno"], -1300.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.10984848484848485, places=12)

    def test_variante_senza_recupero_non_calcolabile(self):
        r = mh825_calcola(**_demo_kwargs(g_alt_kwh_kg=1.80))
        self.assertEqual(r["risparmio_eur_anno"], -5500.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_100000_non_convinte(self):
        r = mh825_calcola(**_demo_kwargs(capex=100000))
        self.assertAlmostEqual(r["van"], -20076.633106009464, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["payback"], 13)

    def test_variante_om_alt_48000_marginale(self):
        r = mh825_calcola(**_demo_kwargs(om_alt=48000))
        self.assertEqual(r["risparmio_eur_anno"], 4700.0)
        self.assertAlmostEqual(r["van"], -1215.6072205512396, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 11)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.06439393939393939, places=12)

    def test_variante_om_alt_55000_non_calcolabile(self):
        r = mh825_calcola(**_demo_kwargs(om_alt=55000))
        self.assertEqual(r["risparmio_eur_anno"], -2300.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.11742424242424243, places=12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh825_calcola(**_demo_kwargs(p_gas=0.04))
        self.assertEqual(basso["risparmio_eur_anno"], -220.0)
        self.assertEqual(basso["verdetto"], "NON_CALCOLABILE")
        alto = mh825_calcola(**_demo_kwargs(p_gas=0.20))
        self.assertEqual(alto["risparmio_eur_anno"], 20900.0)
        self.assertAlmostEqual(alto["van"], 166934.85299797435, places=6)
        self.assertAlmostEqual(alto["tir"], 41.57276213455856, places=6)
        self.assertEqual(alto["payback"], 3)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh825_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 65500.0)
        self.assertEqual(zero["payback"], 7)
        dieci = mh825_calcola(**_demo_kwargs(vita_anni=10))
        self.assertAlmostEqual(dieci["van"], 9457.358954723048, places=6)
        self.assertEqual(dieci["verdetto"], "CONVIENTE")
        cinque = mh825_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(cinque["van"], -16663.02963614269, places=6)
        self.assertEqual(cinque["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(cinque["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh825_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh825_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh825_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_raffinazione_e_recupero(self):
        base = mh825_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh825_calcola(**_demo_kwargs(e_raff_alt_kwh_e_kg=1.0))["risparmio_eur_anno"], base)
        self.assertLess(mh825_calcola(**_demo_kwargs(g_alt_kwh_kg=1.0))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh825_demo_calcoli()
        b = mh825_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh825_demo()
        attese = {"kg", "e_raff_base_kwh_e_kg", "e_raff_alt_kwh_e_kg",
                  "e_fred_base_kwh_e_kg", "e_fred_alt_kwh_e_kg",
                  "g_base_kwh_kg", "g_alt_kwh_kg", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["kg", "e_raff_base_kwh_e_kg", "e_raff_alt_kwh_e_kg",
                 "e_fred_base_kwh_e_kg", "e_fred_alt_kwh_e_kg",
                 "g_base_kwh_kg", "g_alt_kwh_kg", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh825_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("kg", "120000"), ("kg", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh825_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh825_calcola(**_demo_kwargs(e_raff_base_kwh_e_kg=0,
                                         e_fred_base_kwh_e_kg=0,
                                         g_base_kwh_kg=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh825_calcola(**_demo_kwargs(g_alt_kwh_kg=1.80))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh825_calcola(**_demo_kwargs(om_alt=55000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh825_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh825_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh825_demo_calcoli()
        csv = mh825_csv(bc, dict(mh825_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh825_demo_calcoli()
        csv = mh825_csv(bc, dict(mh825_demo()))
        self.assertIn("risparmio_eur_anno;7700.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh825_demo_calcoli()
        csv = mh825_csv(bc, dict(mh825_demo()))
        for chiave in mh825_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh824_", src)
        self.assertNotIn("mh823_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab825:"), 1)
        self.assertTrue(src.startswith("    # W827"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Cioccolateria: raffinazione con motori efficienti", src)
        self.assertIn("recupero calore su concheggio", src)
        self.assertNotIn("tab824", src)
        self.assertNotIn("tab823", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        # "pollaio"/"porcilaia" compaiono legittimamente solo
        # nella distinzione esplicita dell'header: qui si
        # vietano solo i residui di funzione delle tab vecchie.
        for vecchio in ("mh824_", "mh823_", "mh822_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh824_", src)
        self.assertNotIn("st824_", src)
        chiavi = re.findall(r'key="(st825_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st825_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st825_calcola"', src)
        self.assertIn('key="st825_csv"', src)
        self.assertIn('key="st825_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def825\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh825_demo().keys()), lette - set(mh825_demo().keys()))
        self.assertEqual(lette, set(mh825_demo().keys()))

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg825"), src.index(".metric("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".metric("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
