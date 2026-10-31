"""Test nuova scheda tab828 "Calzaturificio:
cucitura/montaggio con motori efficienti +
aria compressa efficiente + recupero calore
su forni di asciugatura collanti battono
cucitura tradizionale + aria compressa
tradizionale + riscaldamento a gas?".

Business case deterministico di un
calzaturificio guidato dalle PAIA DI SCARPE
prodotte in un anno: E_cuc_base = paia x e_cuc_base;
E_cuc_alt = paia x e_cuc_alt (i motori
efficienti riducono solo la cucitura);
E_comp_base = paia x e_comp_base; E_comp_alt =
paia x e_comp_alt (il compressore efficiente riduce
solo l'aria compressa); E_base = E_cuc_base
+ E_comp_base; E_alt = E_cuc_alt + E_comp_alt;
gas_base = paia x g_base; gas_alt = paia x g_alt
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
0,01244444444444438 EUR/kWh (numeratore
2.800 EUR, denominatore 225.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(paia <= 0, specifici negativi, prezzi <= 0,
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
previsto (paia, prezzi, CAPEX, vita). Gli zeri
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
confezione (capi cuciti, taglio, cucito di
abbigliamento: qui niente capi di
abbigliamento, solo paia di scarpe, processi
taglio tomaia, cucitura/montaggio, presse
pneumatiche, forni di asciugatura collanti)
e dalla tessitura (metri di tessuto, telai:
qui niente telai, niente tessuto da tessere):
qui driver PAIA DI SCARPE + CUCITURA CON
MOTORI EFFICIENTI + ARIA COMPRESSA
EFFICIENTE + RECUPERO CALORE SU FORNI DI
ASCIUGATURA COLLANTI.

Demo (calzaturificio): 500.000 paia di scarpe
prodotte in un anno, cucitura specifica base
0,45 (225.000 kWh_e/anno) e alternativa
0,30 (150.000 kWh_e/anno), aria compressa
specifica base 0,18 (90.000 kWh_e/anno) e
alternativa 0,10 (50.000 kWh_e/anno),
elettricita' base 315.000 e alternativa
200.000 kWh_e/anno, gas specifico base
0,80 (400.000 kWh/anno) e alternativo 0,35
(175.000 kWh/anno, il recupero riduce il gas
del 56,25 %, non lo azzera), prezzi
elettricita' 0,28 e gas 0,11 EUR/kWh, O&M
base 50.000 e alternativo 85.000 EUR/anno,
CAPEX 150.000 EUR, WACC 5 %, vita 12 anni,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh828_demo_calcoli(): E_base
315.000, E_alt 200.000, gas_base 400.000,
gas_alt 175.000, C_base 182.200, C_alt 160.250,
risparmio 21.950, CO2_base 159,55, CO2_alt
85,35, CO2_evitata 74,20, VAN
44548,37342005131, TIR 9,940153462119552 %,
payback 7, breakeven gas
0,01244444444444438 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w828_calzaturificio.py
"""

import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w830_helpers import (
    demo_calcoli,
    mh828_breakeven_gas,
    mh828_c_alt,
    mh828_c_base,
    mh828_calcola,
    mh828_co2_alt,
    mh828_co2_base,
    mh828_co2_evitata,
    mh828_csv,
    mh828_demo,
    mh828_demo_calcoli,
    mh828_e_alt,
    mh828_e_base,
    mh828_e_comp_alt,
    mh828_e_comp_base,
    mh828_e_cuc_alt,
    mh828_e_cuc_base,
    mh828_flussi,
    mh828_gas_alt,
    mh828_gas_base,
    mh828_int_pos,
    mh828_nneg,
    mh828_num,
    mh828_payback,
    mh828_pos,
    mh828_risparmio,
    mh828_tir,
    mh828_valida,
    mh828_van,
    mh828_verdetto,
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


_HELPERS_PATH = _risolvi("w830_helpers.py")
_UI_PATH = _risolvi("w830_ui.py")

_DEMO = {
    "e_cuc_base_kwh_e_anno": 225000.0,
    "e_cuc_alt_kwh_e_anno": 150000.0,
    "e_comp_base_kwh_e_anno": 90000.0,
    "e_comp_alt_kwh_e_anno": 50000.0,
    "e_base_kwh_e_anno": 315000.0,
    "e_alt_kwh_e_anno": 200000.0,
    "gas_base_kwh_anno": 400000.0,
    "gas_alt_kwh_anno": 175000.0,
    "c_base_eur_anno": 182200.0,
    "c_alt_eur_anno": 160250.0,
    "risparmio_eur_anno": 21950.0,
    "co2_base_t_anno": 159.55,
    "co2_alt_t_anno": 85.35,
    "co2_evitata_t_anno": 74.2,
    "van": 44548.37342005131,
    "tir": 9.940153462119552,
    "payback": 7,
    "breakeven_gas_eur_kwh": 0.01244444444444438,
}


def _demo_kwargs(**over):
    kw = dict(mh828_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh828_num(3, "x"), 3.0)
        self.assertEqual(mh828_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh828_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh828_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh828_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh828_pos(0, "x")
        with self.assertRaises(ValueError):
            mh828_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh828_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh828_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_cuc_comp_e_base(self):
        self.assertEqual(mh828_e_cuc_base(500000, 0.45), 225000.0)
        self.assertEqual(mh828_e_cuc_alt(500000, 0.30), 150000.0)
        self.assertEqual(mh828_e_comp_base(500000, 0.18), 90000.0)
        self.assertAlmostEqual(mh828_e_comp_alt(500000, 0.10), 50000.0, places=6)
        self.assertEqual(mh828_e_base(225000.0, 90000.0), 315000.0)
        self.assertAlmostEqual(mh828_e_alt(150000.0, 50000.0), 200000.0, places=6)

    def test_gas_base_alt(self):
        self.assertEqual(mh828_gas_base(500000, 0.80), 400000.0)
        self.assertEqual(mh828_gas_alt(500000, 0.35), 175000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh828_c_base(315000.0, 0.28, 400000.0, 0.11, 50000), 182200.0)
        self.assertEqual(mh828_c_alt(200000.0, 0.28, 175000.0, 0.11, 85000), 160250.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh828_risparmio(182200.0, 160250.0), 21950.0)
        self.assertEqual(mh828_risparmio(160250.0, 182200.0), -21950.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh828_co2_base(315000.0, 400000.0), 159.55, places=9)
        self.assertAlmostEqual(mh828_co2_alt(200000.0, 175000.0), 85.35, places=9)
        self.assertAlmostEqual(
            mh828_co2_evitata(315000.0, 400000.0, 200000.0, 175000.0), 74.2, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh828_breakeven_gas(200000.0, 0.28, 85000, 315000.0, 50000, 400000.0, 175000.0)
        self.assertAlmostEqual(be, 0.01244444444444438, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh828_breakeven_gas(1000.0, 0.28, 1000, 315000.0, 50000, 400000.0, 175000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh828_breakeven_gas(200000.0, 0.28, 85000, 315000.0, 50000, 175000.0, 175000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh828_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh828_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh828_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh828_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh828_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh828_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh828_flussi(150000, 21950.0, 12)
        self.assertEqual(len(flussi), 13)
        self.assertEqual(flussi[0], -150000)
        self.assertTrue(all(f == 21950.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh828_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 44548.37342005131, places=6)
        self.assertEqual(mh828_van([-150000] + [21950.0] * 12, 0.0), 113400.0)

    def test_tir_demo(self):
        bc = mh828_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 9.940153462119552, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh828_payback([-150000] + [21950.0] * 12), 7)
        self.assertEqual(mh828_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh828_payback([-150000] + [100.0] * 12))

    def test_verdetto(self):
        self.assertEqual(mh828_verdetto(21950.0, 100.0, 150000, 10.0), "CONVIENTE")
        self.assertEqual(mh828_verdetto(15950.0, -8631.14, 150000, 10.0), "MARGINALE")
        self.assertEqual(mh828_verdetto(21950.0, -105451.63, 150000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh828_verdetto(0.0, 100.0, 150000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh828_verdetto(-100.0, 100.0, 150000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh828_verdetto(None, 100.0, 150000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh828_verdetto(21950.0, 0.0, 150000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh828_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("paia", "500000"), ("paia", float("nan")),
                            ("paia", float("inf")), ("paia", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh828_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"paia": 0}, {"paia": -1}, {"e_cuc_base_kwh_e_paio": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh828_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh828_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh828_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh828_valida(**_demo_kwargs(
            e_cuc_base_kwh_e_paio=0, e_comp_base_kwh_e_paio=0,
            g_base_kwh_paio=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh828_demo()
        self.assertEqual(d["paia"], 500000)
        self.assertEqual(d["e_cuc_base_kwh_e_paio"], 0.45)
        self.assertEqual(d["e_cuc_alt_kwh_e_paio"], 0.30)
        self.assertEqual(d["e_comp_base_kwh_e_paio"], 0.18)
        self.assertEqual(d["e_comp_alt_kwh_e_paio"], 0.10)
        self.assertEqual(d["g_base_kwh_paio"], 0.80)
        self.assertEqual(d["g_alt_kwh_paio"], 0.35)
        self.assertEqual(d["capex"], 150000)
        self.assertEqual(d["vita_anni"], 12)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh828_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh828_demo_calcoli()
        self.assertEqual(bc["e_cuc_base_kwh_e_anno"], 225000.0)
        self.assertEqual(bc["e_cuc_alt_kwh_e_anno"], 150000.0)
        self.assertEqual(bc["e_comp_base_kwh_e_anno"], 90000.0)
        self.assertAlmostEqual(bc["e_comp_alt_kwh_e_anno"], 50000.0, places=6)
        self.assertEqual(bc["c_base_eur_anno"], 182200.0)
        self.assertEqual(bc["c_alt_eur_anno"], 160250.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh828_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 13)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[6], -18300.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7], 3650.0)

    def test_demo_tabella_righe(self):
        bc = mh828_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Paia di scarpe (paia/anno)", voci)
        self.assertIn("Cucitura baseline (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh828_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_cuc_base_kwh_e_anno"] + bc["e_comp_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        paia = 500000
        e_base = paia * (0.45 + 0.18)
        e_alt = paia * (0.30 + 0.10)
        gas_base = paia * 0.80
        gas_alt = paia * 0.35
        c_base = e_base * 0.28 + gas_base * 0.11 + 50000
        c_alt = e_alt * 0.28 + gas_alt * 0.11 + 85000
        bc = mh828_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh828_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_motori_non_convinte(self):
        r = mh828_calcola(**_demo_kwargs(e_cuc_alt_kwh_e_paio=0.45))
        self.assertEqual(r["risparmio_eur_anno"], 950.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -141579.91094537367, places=6)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.1057777777777777, places=12)

    def test_variante_senza_compressore_non_convinte(self):
        r = mh828_calcola(**_demo_kwargs(e_comp_alt_kwh_e_paio=0.18))
        self.assertEqual(r["risparmio_eur_anno"], 10750.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -54720.04490817532, places=6)
        self.assertIsNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.06222222222222216, places=12)

    def test_variante_senza_recupero_non_calcolabile(self):
        r = mh828_calcola(**_demo_kwargs(g_alt_kwh_paio=0.80))
        self.assertEqual(r["risparmio_eur_anno"], -2800.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_300000_non_convinte(self):
        r = mh828_calcola(**_demo_kwargs(capex=300000))
        self.assertAlmostEqual(r["van"], -105451.62657994864, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(r["payback"])

    def test_variante_om_alt_91000_marginale(self):
        r = mh828_calcola(**_demo_kwargs(om_alt=91000))
        self.assertEqual(r["risparmio_eur_anno"], 15950.0)
        self.assertAlmostEqual(r["van"], -8631.136398641542, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 10)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.03911111111111105, places=12)

    def test_variante_om_alt_108000_non_calcolabile(self):
        r = mh828_calcola(**_demo_kwargs(om_alt=108000))
        self.assertEqual(r["risparmio_eur_anno"], -1050.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.1146666666666666, places=12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh828_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], 1700.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(basso["van"], -134932.472218037, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh828_calcola(**_demo_kwargs(p_gas=0.20))
        self.assertEqual(alto["risparmio_eur_anno"], 42200.0)
        self.assertAlmostEqual(alto["van"], 224029.21905813966, places=6)
        self.assertAlmostEqual(alto["tir"], 26.449884375523357, places=6)
        self.assertEqual(alto["payback"], 4)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh828_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 113400.0)
        self.assertEqual(zero["payback"], 7)
        otto = mh828_calcola(**_demo_kwargs(vita_anni=8))
        self.assertAlmostEqual(otto["van"], -8132.479930593718, places=6)
        self.assertEqual(otto["verdetto"], "MARGINALE")
        self.assertEqual(otto["payback"], 7)
        cinque = mh828_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(cinque["van"], -54967.98707965353, places=6)
        self.assertEqual(cinque["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(cinque["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh828_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh828_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh828_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_cuc_e_recupero(self):
        base = mh828_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh828_calcola(**_demo_kwargs(e_cuc_alt_kwh_e_paio=0.38))["risparmio_eur_anno"], base)
        self.assertLess(mh828_calcola(**_demo_kwargs(g_alt_kwh_paio=0.55))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh828_demo_calcoli()
        b = mh828_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh828_demo()
        attese = {"paia", "e_cuc_base_kwh_e_paio", "e_cuc_alt_kwh_e_paio",
                  "e_comp_base_kwh_e_paio", "e_comp_alt_kwh_e_paio",
                  "g_base_kwh_paio", "g_alt_kwh_paio", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["paia", "e_cuc_base_kwh_e_paio", "e_cuc_alt_kwh_e_paio",
                 "e_comp_base_kwh_e_paio", "e_comp_alt_kwh_e_paio",
                 "g_base_kwh_paio", "g_alt_kwh_paio", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh828_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("paia", "500000"), ("paia", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh828_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh828_calcola(**_demo_kwargs(e_cuc_base_kwh_e_paio=0,
                                         e_comp_base_kwh_e_paio=0,
                                         g_base_kwh_paio=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh828_calcola(**_demo_kwargs(g_alt_kwh_paio=0.80))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh828_calcola(**_demo_kwargs(om_alt=108000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh828_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh828_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh828_demo_calcoli()
        csv = mh828_csv(bc, dict(mh828_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh828_demo_calcoli()
        csv = mh828_csv(bc, dict(mh828_demo()))
        self.assertIn("risparmio_eur_anno;21950.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh828_demo_calcoli()
        csv = mh828_csv(bc, dict(mh828_demo()))
        for chiave in mh828_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh827_", src)
        self.assertNotIn("mh826_", src)
        self.assertNotIn("mh825_", src)
        self.assertNotIn("mh824_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab828:"), 1)
        self.assertTrue(src.startswith("    # W830"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Calzaturificio: cucitura/montaggio con motori efficienti", src)
        self.assertIn("recupero calore su forni di asciugatura collanti", src)
        self.assertNotIn("tab827", src)
        self.assertNotIn("tab826", src)
        self.assertNotIn("tab825", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        # "tessitura"/"confezione" compaiono legittimamente solo
        # nella distinzione esplicita dell'header: qui si
        # vietano solo i residui di funzione delle tab vecchie.
        for vecchio in ("mh827_", "mh826_", "mh825_", "mh824_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh827_", src)
        self.assertNotIn("st827_", src)
        self.assertNotIn("mh826_", src)
        self.assertNotIn("st826_", src)
        chiavi = re.findall(r'key="(st828_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st828_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st828_calcola"', src)
        self.assertIn('key="st828_csv"', src)
        self.assertIn('key="st828_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def828\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh828_demo().keys()), lette - set(mh828_demo().keys()))
        self.assertEqual(lette, set(mh828_demo().keys()))

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg828"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
