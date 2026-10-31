"""Test nuova scheda tab830 "Impianto di asfalto:
conglomerato bituminoso con mescolatore
efficiente + aspirazione con inverter +
recupero calore fumi su tamburo battono
mescolatore tradizionale + aspirazione
tradizionale + bruciatore tradizionale
a gas?".

Business case deterministico di un
impianto di asfalto guidato dalle
TONNELLATE DI CONGLOMERATO BITUMINOSO
prodotte in un anno: E_misc_base = t x
e_misc_base; E_misc_alt = t x e_misc_alt
(il mescolatore efficiente riduce solo la
miscelazione); E_asp_base = t x e_asp_base;
E_asp_alt = t x e_asp_alt (l'aspirazione
con inverter riduce solo l'aspirazione);
E_base = E_misc_base + E_asp_base; E_alt =
E_misc_alt + E_asp_alt; gas_base = t x
g_base; gas_alt = t x g_alt (il recupero
calore fumi RIDUCE il gas, non lo azzera:
gas_alt resta positivo nel demo);
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
0,00895 EUR/kWh (numeratore 28.640 EUR,
denominatore 3.200.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(t <= 0, specifici negativi, prezzi <= 0,
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
previsto (t, prezzi, CAPEX, vita). Gli zeri
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
calcestruzzo (legante cementizio, niente
bitume: qui solo bitume e inerti
riscaldati), dalla raffineria e produzione
di bitume (raffinazione del petrolio: qui
niente raffinazione, solo miscelazione a
caldo) e dal cantiere stradale (stesura
dell'asfalto: qui solo produzione in
impianto): qui driver T DI CONGLOMERATO
BITUMINOSO + MESCOLATORE EFFICIENTE +
ASPIRAZIONE CON INVERTER + RECUPERO
CALORE FUMI SU TAMBURO.

Demo (impianto di asfalto): 80.000 t di
conglomerato bituminoso prodotte in un
anno, miscelazione specifica base 3,00
(240.000 kWh_e/anno) e alternativa 2,10
(168.000 kWh_e/anno), aspirazione
specifica base 1,20 (96.000 kWh_e/anno) e
alternativa 0,70 (56.000 kWh_e/anno),
elettricita' base 336.000 e alternativa
224.000 kWh_e/anno, gas specifico base
95,00 (7.600.000 kWh/anno) e alternativo
55,00 (4.400.000 kWh/anno, il recupero
riduce il gas del 42,11 %, non lo azzera),
prezzi elettricita' 0,28 e gas 0,11
EUR/kWh, O&M base 120.000 e alternativo
180.000 EUR/anno, CAPEX 900.000 EUR, WACC
5 %, vita 12 anni, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh830_demo_calcoli(): E_base 336.000,
E_alt 224.000, gas_base 7.600.000,
gas_alt 4.400.000, C_base 1.050.080,
C_alt 726.720, risparmio 323.360,
CO2_base 1.619,2, CO2_alt 944,8,
CO2_evitata 674,4, VAN 1966021,0491620866,
TIR 34,94346895399445 %, payback 3,
breakeven gas 0,00895 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w830_asfalto.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w832_helpers import (
    demo_calcoli,
    mh830_breakeven_gas,
    mh830_c_alt,
    mh830_c_base,
    mh830_calcola,
    mh830_co2_alt,
    mh830_co2_base,
    mh830_co2_evitata,
    mh830_csv,
    mh830_demo,
    mh830_demo_calcoli,
    mh830_e_alt,
    mh830_e_base,
    mh830_e_asp_alt,
    mh830_e_asp_base,
    mh830_e_misc_alt,
    mh830_e_misc_base,
    mh830_flussi,
    mh830_gas_alt,
    mh830_gas_base,
    mh830_int_pos,
    mh830_nneg,
    mh830_num,
    mh830_payback,
    mh830_pos,
    mh830_risparmio,
    mh830_tir,
    mh830_valida,
    mh830_van,
    mh830_verdetto,
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


_HELPERS_PATH = _risolvi("w832_helpers.py")
_UI_PATH = _risolvi("w832_ui.py")

_DEMO = {
    "e_misc_base_kwh_e_anno": 240000.0,
    "e_misc_alt_kwh_e_anno": 168000.0,
    "e_asp_base_kwh_e_anno": 96000.0,
    "e_asp_alt_kwh_e_anno": 56000.0,
    "e_base_kwh_e_anno": 336000.0,
    "e_alt_kwh_e_anno": 224000.0,
    "gas_base_kwh_anno": 7600000.0,
    "gas_alt_kwh_anno": 4400000.0,
    "c_base_eur_anno": 1050080.0,
    "c_alt_eur_anno": 726720.0,
    "risparmio_eur_anno": 323360.0,
    "co2_base_t_anno": 1619.2,
    "co2_alt_t_anno": 944.8,
    "co2_evitata_t_anno": 674.4,
    "van": 1966021.0491620866,
    "tir": 34.94346895399445,
    "payback": 3,
    "breakeven_gas_eur_kwh": 0.00895,
}


def _demo_kwargs(**over):
    kw = dict(mh830_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh830_num(3, "x"), 3.0)
        self.assertEqual(mh830_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh830_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh830_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh830_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh830_pos(0, "x")
        with self.assertRaises(ValueError):
            mh830_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh830_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh830_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_misc_asp_e_base(self):
        self.assertEqual(mh830_e_misc_base(80000, 3.00), 240000.0)
        self.assertEqual(mh830_e_misc_alt(80000, 2.10), 168000.0)
        self.assertEqual(mh830_e_asp_base(80000, 1.20), 96000.0)
        self.assertAlmostEqual(mh830_e_asp_alt(80000, 0.70), 56000.0, places=6)
        self.assertEqual(mh830_e_base(240000.0, 96000.0), 336000.0)
        self.assertAlmostEqual(mh830_e_alt(168000.0, 56000.0), 224000.0, places=6)

    def test_gas_base_alt(self):
        self.assertEqual(mh830_gas_base(80000, 95.00), 7600000.0)
        self.assertEqual(mh830_gas_alt(80000, 55.00), 4400000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh830_c_base(336000.0, 0.28, 7600000.0, 0.11, 120000), 1050080.0)
        self.assertEqual(mh830_c_alt(224000.0, 0.28, 4400000.0, 0.11, 180000), 726720.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh830_risparmio(1050080.0, 726720.0), 323360.0)
        self.assertEqual(mh830_risparmio(726720.0, 1050080.0), -323360.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh830_co2_base(336000.0, 7600000.0), 1619.2, places=9)
        self.assertAlmostEqual(mh830_co2_alt(224000.0, 4400000.0), 944.8, places=9)
        self.assertAlmostEqual(
            mh830_co2_evitata(336000.0, 7600000.0, 224000.0, 4400000.0), 674.4, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh830_breakeven_gas(224000.0, 0.28, 180000, 336000.0, 120000, 7600000.0, 4400000.0)
        self.assertAlmostEqual(be, 0.00895, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh830_breakeven_gas(1000.0, 0.28, 1000, 336000.0, 120000, 7600000.0, 4400000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh830_breakeven_gas(224000.0, 0.28, 180000, 336000.0, 120000, 4400000.0, 4400000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh830_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh830_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh830_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh830_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh830_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh830_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh830_flussi(900000, 323360.0, 12)
        self.assertEqual(len(flussi), 13)
        self.assertEqual(flussi[0], -900000)
        self.assertTrue(all(f == 323360.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh830_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 1966021.0491620866, places=6)
        self.assertEqual(mh830_van([-900000] + [323360.0] * 12, 0.0), 2980320.0)

    def test_tir_demo(self):
        bc = mh830_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 34.94346895399445, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh830_payback([-900000] + [323360.0] * 12), 3)
        self.assertEqual(mh830_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh830_payback([-900000] + [100.0] * 12))

    def test_verdetto(self):
        self.assertEqual(mh830_verdetto(323360.0, 100.0, 900000, 10.0), "CONVIENTE")
        self.assertEqual(mh830_verdetto(100000.0, -13674.84, 900000, 10.0), "MARGINALE")
        self.assertEqual(mh830_verdetto(323360.0, -633978.95, 900000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh830_verdetto(0.0, 100.0, 900000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh830_verdetto(-100.0, 100.0, 900000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh830_verdetto(None, 100.0, 900000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh830_verdetto(323360.0, 0.0, 900000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh830_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("t", "80000"), ("t", float("nan")),
                            ("t", float("inf")), ("t", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh830_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"t": 0}, {"t": -1}, {"e_misc_base_kwh_e_t": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh830_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh830_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh830_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh830_valida(**_demo_kwargs(
            e_misc_base_kwh_e_t=0, e_asp_base_kwh_e_t=0,
            g_base_kwh_t=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh830_demo()
        self.assertEqual(d["t"], 80000)
        self.assertEqual(d["e_misc_base_kwh_e_t"], 3.00)
        self.assertEqual(d["e_misc_alt_kwh_e_t"], 2.10)
        self.assertEqual(d["e_asp_base_kwh_e_t"], 1.20)
        self.assertEqual(d["e_asp_alt_kwh_e_t"], 0.70)
        self.assertEqual(d["g_base_kwh_t"], 95.00)
        self.assertEqual(d["g_alt_kwh_t"], 55.00)
        self.assertEqual(d["capex"], 900000)
        self.assertEqual(d["vita_anni"], 12)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh830_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh830_demo_calcoli()
        self.assertEqual(bc["e_misc_base_kwh_e_anno"], 240000.0)
        self.assertEqual(bc["e_misc_alt_kwh_e_anno"], 168000.0)
        self.assertEqual(bc["e_asp_base_kwh_e_anno"], 96000.0)
        self.assertAlmostEqual(bc["e_asp_alt_kwh_e_anno"], 56000.0, places=6)
        self.assertEqual(bc["c_base_eur_anno"], 1050080.0)
        self.assertEqual(bc["c_alt_eur_anno"], 726720.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh830_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 13)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[2], -253280.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[3], 70080.0)

    def test_demo_tabella_righe(self):
        bc = mh830_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Conglomerato bituminoso (t/anno)", voci)
        self.assertIn("Miscelazione baseline (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh830_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_misc_base_kwh_e_anno"] + bc["e_asp_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        t = 80000
        e_base = t * (3.00 + 1.20)
        e_alt = t * (2.10 + 0.70)
        gas_base = t * 95.00
        gas_alt = t * 55.00
        c_base = e_base * 0.28 + gas_base * 0.11 + 120000
        c_alt = e_alt * 0.28 + gas_alt * 0.11 + 180000
        bc = mh830_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh830_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_mescolatore_resta_convinte(self):
        r = mh830_calcola(**_demo_kwargs(e_misc_alt_kwh_e_t=3.00))
        self.assertEqual(r["risparmio_eur_anno"], 303200.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 1787337.8961712783, places=6)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.01525, places=12)

    def test_variante_senza_aspirazione_resta_convinte(self):
        r = mh830_calcola(**_demo_kwargs(e_asp_alt_kwh_e_t=1.20))
        self.assertEqual(r["risparmio_eur_anno"], 312160.0)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 1866752.6308338596, places=6)
        self.assertIsNotNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.01245, places=12)

    def test_variante_senza_recupero_non_calcolabile(self):
        r = mh830_calcola(**_demo_kwargs(g_alt_kwh_t=95.00))
        self.assertEqual(r["risparmio_eur_anno"], -28640.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_3500000_non_convinte(self):
        r = mh830_calcola(**_demo_kwargs(capex=3500000))
        self.assertAlmostEqual(r["van"], -633978.9508379139, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["payback"], 11)

    def test_variante_om_alt_403360_marginale(self):
        r = mh830_calcola(**_demo_kwargs(om_alt=403360))
        self.assertEqual(r["risparmio_eur_anno"], 100000.0)
        self.assertAlmostEqual(r["van"], -13674.836355119354, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 9)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.07875, places=12)

    def test_variante_om_alt_500000_non_convinte(self):
        r = mh830_calcola(**_demo_kwargs(om_alt=500000))
        self.assertEqual(r["risparmio_eur_anno"], 3360.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -870219.4745015318, places=6)
        self.assertIsNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.10895, places=12)

    def test_variante_om_alt_520000_non_calcolabile(self):
        r = mh830_calcola(**_demo_kwargs(om_alt=520000))
        self.assertEqual(r["risparmio_eur_anno"], -16640.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.1152, places=12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh830_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], 35360.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(basso["van"], -586595.4221351701, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh830_calcola(**_demo_kwargs(p_gas=0.20))
        self.assertEqual(alto["risparmio_eur_anno"], 611360.0)
        self.assertAlmostEqual(alto["van"], 4518637.520459343, places=6)
        self.assertAlmostEqual(alto["tir"], 67.79249842003051, places=6)
        self.assertEqual(alto["payback"], 2)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh830_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 2980320.0)
        self.assertEqual(zero["payback"], 3)
        tre = mh830_calcola(**_demo_kwargs(vita_anni=3))
        self.assertAlmostEqual(tre["van"], -19410.517222762166, places=6)
        self.assertEqual(tre["verdetto"], "MARGINALE")
        self.assertEqual(tre["payback"], 3)
        due = mh830_calcola(**_demo_kwargs(vita_anni=2))
        self.assertAlmostEqual(due["van"], -298741.04308390024, places=6)
        self.assertEqual(due["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(due["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh830_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh830_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh830_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_misc_e_recupero(self):
        base = mh830_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh830_calcola(**_demo_kwargs(e_misc_alt_kwh_e_t=2.50))["risparmio_eur_anno"], base)
        self.assertLess(mh830_calcola(**_demo_kwargs(g_alt_kwh_t=70.00))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh830_demo_calcoli()
        b = mh830_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh830_demo()
        attese = {"t", "e_misc_base_kwh_e_t", "e_misc_alt_kwh_e_t",
                  "e_asp_base_kwh_e_t", "e_asp_alt_kwh_e_t",
                  "g_base_kwh_t", "g_alt_kwh_t", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["t", "e_misc_base_kwh_e_t", "e_misc_alt_kwh_e_t",
                 "e_asp_base_kwh_e_t", "e_asp_alt_kwh_e_t",
                 "g_base_kwh_t", "g_alt_kwh_t", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh830_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("t", "80000"), ("t", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh830_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh830_calcola(**_demo_kwargs(e_misc_base_kwh_e_t=0,
                                         e_asp_base_kwh_e_t=0,
                                         g_base_kwh_t=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh830_calcola(**_demo_kwargs(g_alt_kwh_t=95.00))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh830_calcola(**_demo_kwargs(om_alt=600000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh830_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh830_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh830_demo_calcoli()
        csv = mh830_csv(bc, dict(mh830_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh830_demo_calcoli()
        csv = mh830_csv(bc, dict(mh830_demo()))
        self.assertIn("risparmio_eur_anno;323360.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh830_demo_calcoli()
        csv = mh830_csv(bc, dict(mh830_demo()))
        for chiave in mh830_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh829_", src)
        self.assertNotIn("mh828_", src)
        self.assertNotIn("mh827_", src)
        self.assertNotIn("mh826_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab830:"), 1)
        self.assertTrue(src.startswith("    # W832"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Impianto di asfalto: mescolatore efficiente", src)
        self.assertIn("recupero calore fumi su tamburo", src)
        self.assertNotIn("tab829", src)
        self.assertNotIn("tab828", src)
        self.assertNotIn("tab827", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        # "calcestruzzo"/"raffineria"/"cantiere" compaiono
        # legittimamente solo nella distinzione esplicita
        # dell'header: qui si vietano solo i residui di
        # funzione delle tab vecchie.
        for vecchio in ("mh829_", "mh828_", "mh827_", "mh826_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh829_", src)
        self.assertNotIn("st829_", src)
        self.assertNotIn("mh828_", src)
        self.assertNotIn("st828_", src)
        chiavi = re.findall(r'key="(st830_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st830_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st830_calcola"', src)
        self.assertIn('key="st830_csv"', src)
        self.assertIn('key="st830_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def830\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh830_demo().keys()), lette - set(mh830_demo().keys()))
        self.assertEqual(lette, set(mh830_demo().keys()))

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg830"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
