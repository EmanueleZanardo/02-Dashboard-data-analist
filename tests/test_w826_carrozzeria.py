"""Test nuova scheda tab826 "Carrozzeria:
ventilazione cabina con inverter +
aria compressa efficiente + recupero calore
su cabina battono ventilazione
tradizionale + aria compressa tradizionale
+ riscaldamento a gas?".

Business case deterministico di una
carrozzeria guidata dagli INTERVENTI DI VERNICIATURA
in cabina/anno: E_vent_base = interventi x e_vent_base;
E_vent_alt = interventi x e_vent_alt (l'inverter
riduce solo la ventilazione cabina);
E_comp_base = interventi x e_comp_base; E_comp_alt =
interventi x e_comp_alt (il compressore efficiente riduce
solo l'aria compressa); E_base = E_vent_base
+ E_comp_base; E_alt = E_vent_alt + E_comp_alt;
gas_base = interventi x g_base; gas_alt = interventi x g_alt
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
0,025244444444444403 EUR/kWh (numeratore
2.272 EUR, denominatore 90.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(interventi <= 0, specifici negativi, prezzi <= 0,
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
previsto (interventi, prezzi, CAPEX, vita). Gli zeri
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
verniciatura industriale (pezzi in linea,
forno: qui niente linea, niente forno,
solo interventi in cabina), dall'officina
meccanica (riparazioni meccaniche, utensili:
qui niente riparazioni meccaniche, il
compressore alimenta solo le pistole), e
dall'autolavaggio (lavaggi, acqua di
lavaggio: qui niente lavaggi, niente acqua
di lavaggio): qui driver INTERVENTI DI
VERNICIATURA + VENTILAZIONE CON INVERTER +
ARIA COMPRESSA EFFICIENTE + RECUPERO CALORE
SU CABINA.

Demo (carrozzeria): 1.200 interventi di
verniciatura in cabina, ventilazione cabina
specifica base 45 (54.000 kWh_e/anno) e
alternativa 28 (33.600 kWh_e/anno), aria
compressa specifica base 18 (21.600
kWh_e/anno) e alternativa 12 (14.400
kWh_e/anno), elettricita' base 75.600 e
alternativa 48.000 kWh_e/anno, gas specifico
base 120 (144.000 kWh/anno) e alternativo 45
(54.000 kWh/anno, il recupero riduce il gas
del 62,5 %, non lo azzera), prezzi
elettricita' 0,28 e gas 0,11 EUR/kWh, O&M
base 12.000 e alternativo 22.000 EUR/anno,
CAPEX 45.000 EUR, WACC 5 %, vita 12 anni,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh826_demo_calcoli(): E_base
75.600, E_alt 48.000, gas_base 144.000,
gas_alt 54.000, C_base 49.008, C_alt 41.380,
risparmio 7.628, CO2_base 47,988, CO2_alt
22,908, CO2_evitata 25,08, VAN
22608,883482831505, TIR 13,068884539688892 %,
payback 6, breakeven gas
0,025244444444444403 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w826_carrozzeria.py
"""

import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w828_helpers import (
    demo_calcoli,
    mh826_breakeven_gas,
    mh826_c_alt,
    mh826_c_base,
    mh826_calcola,
    mh826_co2_alt,
    mh826_co2_base,
    mh826_co2_evitata,
    mh826_csv,
    mh826_demo,
    mh826_demo_calcoli,
    mh826_e_alt,
    mh826_e_base,
    mh826_e_comp_alt,
    mh826_e_comp_base,
    mh826_e_vent_alt,
    mh826_e_vent_base,
    mh826_flussi,
    mh826_gas_alt,
    mh826_gas_base,
    mh826_int_pos,
    mh826_nneg,
    mh826_num,
    mh826_payback,
    mh826_pos,
    mh826_risparmio,
    mh826_tir,
    mh826_valida,
    mh826_van,
    mh826_verdetto,
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


_HELPERS_PATH = _risolvi("w828_helpers.py")
_UI_PATH = _risolvi("w828_ui.py")

_DEMO = {
    "e_vent_base_kwh_e_anno": 54000.0,
    "e_vent_alt_kwh_e_anno": 33600.0,
    "e_comp_base_kwh_e_anno": 21600.0,
    "e_comp_alt_kwh_e_anno": 14400.0,
    "e_base_kwh_e_anno": 75600.0,
    "e_alt_kwh_e_anno": 48000.0,
    "gas_base_kwh_anno": 144000.0,
    "gas_alt_kwh_anno": 54000.0,
    "c_base_eur_anno": 49008.0,
    "c_alt_eur_anno": 41380.0,
    "risparmio_eur_anno": 7628.0,
    "co2_base_t_anno": 47.988,
    "co2_alt_t_anno": 22.908,
    "co2_evitata_t_anno": 25.08,
    "van": 22608.883482831505,
    "tir": 13.068884539688892,
    "payback": 6,
    "breakeven_gas_eur_kwh": 0.025244444444444403,
}


def _demo_kwargs(**over):
    kw = dict(mh826_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh826_num(3, "x"), 3.0)
        self.assertEqual(mh826_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh826_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh826_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh826_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh826_pos(0, "x")
        with self.assertRaises(ValueError):
            mh826_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh826_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh826_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_vent_comp_e_base(self):
        self.assertEqual(mh826_e_vent_base(1200, 45), 54000.0)
        self.assertEqual(mh826_e_vent_alt(1200, 28), 33600.0)
        self.assertEqual(mh826_e_comp_base(1200, 18), 21600.0)
        self.assertEqual(mh826_e_comp_alt(1200, 12), 14400.0)
        self.assertEqual(mh826_e_base(54000.0, 21600.0), 75600.0)
        self.assertEqual(mh826_e_alt(33600.0, 14400.0), 48000.0)

    def test_gas_base_alt(self):
        self.assertEqual(mh826_gas_base(1200, 120), 144000.0)
        self.assertEqual(mh826_gas_alt(1200, 45), 54000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh826_c_base(75600.0, 0.28, 144000.0, 0.11, 12000), 49008.0)
        self.assertEqual(mh826_c_alt(48000.0, 0.28, 54000.0, 0.11, 22000), 41380.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh826_risparmio(49008.0, 41380.0), 7628.0)
        self.assertEqual(mh826_risparmio(41380.0, 49008.0), -7628.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh826_co2_base(75600.0, 144000.0), 47.988, places=9)
        self.assertAlmostEqual(mh826_co2_alt(48000.0, 54000.0), 22.908, places=9)
        self.assertAlmostEqual(
            mh826_co2_evitata(75600.0, 144000.0, 48000.0, 54000.0), 25.08, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh826_breakeven_gas(48000.0, 0.28, 22000, 75600.0, 12000, 144000.0, 54000.0)
        self.assertAlmostEqual(be, 0.025244444444444403, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh826_breakeven_gas(1000.0, 0.28, 1000, 75600.0, 12000, 144000.0, 54000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh826_breakeven_gas(48000.0, 0.28, 22000, 75600.0, 12000, 54000.0, 54000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh826_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh826_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh826_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh826_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh826_calcola(**_demo_kwargs(p_gas=be + 0.01))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh826_calcola(**_demo_kwargs(p_gas=be - 0.01))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh826_flussi(45000, 7628.0, 12)
        self.assertEqual(len(flussi), 13)
        self.assertEqual(flussi[0], -45000)
        self.assertTrue(all(f == 7628.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh826_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 22608.883482831505, places=6)
        self.assertEqual(mh826_van([-45000] + [7628.0] * 12, 0.0), 46536.0)

    def test_tir_demo(self):
        bc = mh826_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 13.068884539688892, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh826_payback([-45000] + [7628.0] * 12), 6)
        self.assertEqual(mh826_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh826_payback([-45000] + [100.0] * 12))

    def test_verdetto(self):
        self.assertEqual(mh826_verdetto(7628.0, 100.0, 45000, 10.0), "CONVIENTE")
        self.assertEqual(mh826_verdetto(4628.0, -3980.87, 45000, 10.0), "MARGINALE")
        self.assertEqual(mh826_verdetto(7628.0, -22391.12, 45000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh826_verdetto(0.0, 100.0, 45000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh826_verdetto(-100.0, 100.0, 45000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh826_verdetto(None, 100.0, 45000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh826_verdetto(7628.0, 0.0, 45000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh826_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("interventi", "1200"), ("interventi", float("nan")),
                            ("interventi", float("inf")), ("interventi", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh826_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"interventi": 0}, {"interventi": -1}, {"e_vent_base_kwh_e_int": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh826_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh826_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh826_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh826_valida(**_demo_kwargs(
            e_vent_base_kwh_e_int=0, e_comp_base_kwh_e_int=0,
            g_base_kwh_int=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh826_demo()
        self.assertEqual(d["interventi"], 1200)
        self.assertEqual(d["e_vent_base_kwh_e_int"], 45)
        self.assertEqual(d["e_vent_alt_kwh_e_int"], 28)
        self.assertEqual(d["e_comp_base_kwh_e_int"], 18)
        self.assertEqual(d["e_comp_alt_kwh_e_int"], 12)
        self.assertEqual(d["g_base_kwh_int"], 120)
        self.assertEqual(d["g_alt_kwh_int"], 45)
        self.assertEqual(d["capex"], 45000)
        self.assertEqual(d["vita_anni"], 12)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh826_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh826_demo_calcoli()
        self.assertEqual(bc["e_vent_base_kwh_e_anno"], 54000.0)
        self.assertEqual(bc["e_vent_alt_kwh_e_anno"], 33600.0)
        self.assertEqual(bc["e_comp_base_kwh_e_anno"], 21600.0)
        self.assertEqual(bc["e_comp_alt_kwh_e_anno"], 14400.0)
        self.assertEqual(bc["c_base_eur_anno"], 49008.0)
        self.assertEqual(bc["c_alt_eur_anno"], 41380.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh826_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 13)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[5], -6860.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[6], 768.0)

    def test_demo_tabella_righe(self):
        bc = mh826_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Interventi di verniciatura (interventi/anno)", voci)
        self.assertIn("Ventilazione cabina baseline (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh826_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_vent_base_kwh_e_anno"] + bc["e_comp_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        interventi = 1200
        e_base = interventi * (45 + 18)
        e_alt = interventi * (28 + 12)
        gas_base = interventi * 120
        gas_alt = interventi * 45
        c_base = e_base * 0.28 + gas_base * 0.11 + 12000
        c_alt = e_alt * 0.28 + gas_alt * 0.11 + 22000
        bc = mh826_demo_calcoli()
        self.assertEqual(bc["e_base_kwh_e_anno"], e_base)
        self.assertEqual(bc["e_alt_kwh_e_anno"], e_alt)
        self.assertEqual(bc["gas_base_kwh_anno"], gas_base)
        self.assertEqual(bc["gas_alt_kwh_anno"], gas_alt)
        self.assertEqual(bc["c_base_eur_anno"], c_base)
        self.assertEqual(bc["c_alt_eur_anno"], c_alt)
        self.assertEqual(bc["risparmio_eur_anno"], c_base - c_alt)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh826_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_inverter_non_convinte(self):
        r = mh826_calcola(**_demo_kwargs(e_vent_alt_kwh_e_int=45))
        self.assertEqual(r["risparmio_eur_anno"], 1916.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -28018.009864564086, places=6)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.08871111111111107, places=12)

    def test_variante_senza_compressore_convinte(self):
        r = mh826_calcola(**_demo_kwargs(e_comp_alt_kwh_e_int=18))
        self.assertEqual(r["risparmio_eur_anno"], 5612.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 4740.5681837507145, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.047644444444444406, places=12)

    def test_variante_senza_recupero_non_calcolabile(self):
        r = mh826_calcola(**_demo_kwargs(g_alt_kwh_int=120))
        self.assertEqual(r["risparmio_eur_anno"], -2272.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_90000_non_convinte(self):
        r = mh826_calcola(**_demo_kwargs(capex=90000))
        self.assertAlmostEqual(r["van"], -22391.11651716849, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["payback"], 12)

    def test_variante_om_alt_25000_marginale(self):
        r = mh826_calcola(**_demo_kwargs(om_alt=25000))
        self.assertEqual(r["risparmio_eur_anno"], 4628.0)
        self.assertAlmostEqual(r["van"], -3980.871426514918, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 10)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.058577777777777736, places=12)

    def test_variante_om_alt_30000_non_calcolabile(self):
        r = mh826_calcola(**_demo_kwargs(om_alt=30000))
        self.assertEqual(r["risparmio_eur_anno"], -372.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.1141333333333333, places=12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh826_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertEqual(basso["risparmio_eur_anno"], -472.0)
        self.assertEqual(basso["verdetto"], "NON_CALCOLABILE")
        alto = mh826_calcola(**_demo_kwargs(p_gas=0.20))
        self.assertEqual(alto["risparmio_eur_anno"], 15728.0)
        self.assertAlmostEqual(alto["van"], 94401.22173806684, places=6)
        self.assertAlmostEqual(alto["tir"], 33.89880906392221, places=6)
        self.assertEqual(alto["payback"], 3)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh826_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 46536.0)
        self.assertEqual(zero["payback"], 6)
        dieci = mh826_calcola(**_demo_kwargs(vita_anni=8))
        self.assertAlmostEqual(dieci["van"], 4301.386928903473, places=6)
        self.assertEqual(dieci["verdetto"], "CONVIENTE")
        cinque = mh826_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(cinque["van"], -11974.75195642811, places=6)
        self.assertEqual(cinque["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(cinque["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh826_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh826_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh826_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_ventilazione_e_recupero(self):
        base = mh826_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh826_calcola(**_demo_kwargs(e_vent_alt_kwh_e_int=35))["risparmio_eur_anno"], base)
        self.assertLess(mh826_calcola(**_demo_kwargs(g_alt_kwh_int=60))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh826_demo_calcoli()
        b = mh826_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh826_demo()
        attese = {"interventi", "e_vent_base_kwh_e_int", "e_vent_alt_kwh_e_int",
                  "e_comp_base_kwh_e_int", "e_comp_alt_kwh_e_int",
                  "g_base_kwh_int", "g_alt_kwh_int", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["interventi", "e_vent_base_kwh_e_int", "e_vent_alt_kwh_e_int",
                 "e_comp_base_kwh_e_int", "e_comp_alt_kwh_e_int",
                 "g_base_kwh_int", "g_alt_kwh_int", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh826_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("interventi", "1200"), ("interventi", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh826_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh826_calcola(**_demo_kwargs(e_vent_base_kwh_e_int=0,
                                         e_comp_base_kwh_e_int=0,
                                         g_base_kwh_int=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh826_calcola(**_demo_kwargs(g_alt_kwh_int=120))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh826_calcola(**_demo_kwargs(om_alt=30000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh826_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh826_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh826_demo_calcoli()
        csv = mh826_csv(bc, dict(mh826_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh826_demo_calcoli()
        csv = mh826_csv(bc, dict(mh826_demo()))
        self.assertIn("risparmio_eur_anno;7628.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh826_demo_calcoli()
        csv = mh826_csv(bc, dict(mh826_demo()))
        for chiave in mh826_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh825_", src)
        self.assertNotIn("mh824_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab826:"), 1)
        self.assertTrue(src.startswith("    # W828"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Carrozzeria: ventilazione cabina con inverter", src)
        self.assertIn("recupero calore su cabina", src)
        self.assertNotIn("tab825", src)
        self.assertNotIn("tab824", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        # "pollaio"/"porcilaia" compaiono legittimamente solo
        # nella distinzione esplicita dell'header: qui si
        # vietano solo i residui di funzione delle tab vecchie.
        for vecchio in ("mh825_", "mh824_", "mh823_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh825_", src)
        self.assertNotIn("st825_", src)
        chiavi = re.findall(r'key="(st826_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st826_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st826_calcola"', src)
        self.assertIn('key="st826_csv"', src)
        self.assertIn('key="st826_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def826\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh826_demo().keys()), lette - set(mh826_demo().keys()))
        self.assertEqual(lette, set(mh826_demo().keys()))

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg826"), src.index(".metric("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".metric("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
