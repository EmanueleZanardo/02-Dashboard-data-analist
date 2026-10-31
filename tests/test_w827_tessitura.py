"""Test nuova scheda tab827 "Tessitura:
telai con azionamento efficiente +
aria compressa efficiente + recupero calore
su climatizzazione sala telai battono telai
tradizionali + aria compressa tradizionale
+ riscaldamento a gas?".

Business case deterministico di una
tessitura guidata dai METRI DI TESSUTO
prodotti in un anno: E_telai_base = metri x e_telai_base;
E_telai_alt = metri x e_telai_alt (l'azionamento
efficiente riduce solo i telai);
E_comp_base = metri x e_comp_base; E_comp_alt =
metri x e_comp_alt (il compressore efficiente riduce
solo l'aria compressa); E_base = E_telai_base
+ E_comp_base; E_alt = E_telai_alt + E_comp_alt;
gas_base = metri x g_base; gas_alt = metri x g_alt
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
0,008380952380952312 EUR/kWh (numeratore
1.760 EUR, denominatore 210.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(metri <= 0, specifici negativi, prezzi <= 0,
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
previsto (metri, prezzi, CAPEX, vita). Gli zeri
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
tintoria (chilogrammi tinti, vasche, vapore:
qui niente vasche, niente vapore, solo
metri al telaio), dalla filatura
(chilogrammi di filato, fusi, rotori: qui
niente fusi, niente rotori), e dalla
confezione (capi cuciti, taglio, cucito:
qui niente taglio, niente cucito, niente
capi finiti): qui driver METRI DI TESSUTO
+ TELAI CON AZIONAMENTO EFFICIENTE +
ARIA COMPRESSA EFFICIENTE + RECUPERO CALORE
SU CLIMATIZZAZIONE SALA TELAI.

Demo (tessitura): 600.000 metri di tessuto
prodotti in un anno, telai specifica base
0,35 (210.000 kWh_e/anno) e alternativa
0,22 (132.000 kWh_e/anno), aria compressa
specifica base 0,12 (72.000 kWh_e/anno) e
alternativa 0,07 (42.000 kWh_e/anno),
elettricita' base 282.000 e alternativa
174.000 kWh_e/anno, gas specifico base
0,60 (360.000 kWh/anno) e alternativo 0,25
(150.000 kWh/anno, il recupero riduce il gas
del 58,3 %, non lo azzera), prezzi
elettricita' 0,28 e gas 0,11 EUR/kWh, O&M
base 40.000 e alternativo 72.000 EUR/anno,
CAPEX 150.000 EUR, WACC 5 %, vita 12 anni,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh827_demo_calcoli(): E_base
282.000, E_alt 174.000, gas_base 360.000,
gas_alt 150.000, C_base 158.560, C_alt 137.220,
risparmio 21.340, CO2_base 143,22, CO2_alt
73,80, CO2_evitata 69,42, VAN
39141,789921817566, TIR 9,370327622050521 %,
payback 8, breakeven gas
0,008380952380952312 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w827_tessitura.py
"""

import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w829_helpers import (
    demo_calcoli,
    mh827_breakeven_gas,
    mh827_c_alt,
    mh827_c_base,
    mh827_calcola,
    mh827_co2_alt,
    mh827_co2_base,
    mh827_co2_evitata,
    mh827_csv,
    mh827_demo,
    mh827_demo_calcoli,
    mh827_e_alt,
    mh827_e_base,
    mh827_e_comp_alt,
    mh827_e_comp_base,
    mh827_e_telai_alt,
    mh827_e_telai_base,
    mh827_flussi,
    mh827_gas_alt,
    mh827_gas_base,
    mh827_int_pos,
    mh827_nneg,
    mh827_num,
    mh827_payback,
    mh827_pos,
    mh827_risparmio,
    mh827_tir,
    mh827_valida,
    mh827_van,
    mh827_verdetto,
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


_HELPERS_PATH = _risolvi("w829_helpers.py")
_UI_PATH = _risolvi("w829_ui.py")

_DEMO = {
    "e_telai_base_kwh_e_anno": 210000.0,
    "e_telai_alt_kwh_e_anno": 132000.0,
    "e_comp_base_kwh_e_anno": 72000.0,
    "e_comp_alt_kwh_e_anno": 42000.0,
    "e_base_kwh_e_anno": 282000.0,
    "e_alt_kwh_e_anno": 174000.0,
    "gas_base_kwh_anno": 360000.0,
    "gas_alt_kwh_anno": 150000.0,
    "c_base_eur_anno": 158560.0,
    "c_alt_eur_anno": 137220.0,
    "risparmio_eur_anno": 21340.0,
    "co2_base_t_anno": 143.22,
    "co2_alt_t_anno": 73.8,
    "co2_evitata_t_anno": 69.42,
    "van": 39141.789921817566,
    "tir": 9.370327622050521,
    "payback": 8,
    "breakeven_gas_eur_kwh": 0.008380952380952312,
}


def _demo_kwargs(**over):
    kw = dict(mh827_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh827_num(3, "x"), 3.0)
        self.assertEqual(mh827_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh827_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh827_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh827_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh827_pos(0, "x")
        with self.assertRaises(ValueError):
            mh827_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh827_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh827_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_vent_comp_e_base(self):
        self.assertEqual(mh827_e_telai_base(600000, 0.35), 210000.0)
        self.assertEqual(mh827_e_telai_alt(600000, 0.22), 132000.0)
        self.assertEqual(mh827_e_comp_base(600000, 0.12), 72000.0)
        self.assertAlmostEqual(mh827_e_comp_alt(600000, 0.07), 42000.0, places=6)
        self.assertEqual(mh827_e_base(210000.0, 72000.0), 282000.0)
        self.assertAlmostEqual(mh827_e_alt(132000.0, 42000.0), 174000.0, places=6)

    def test_gas_base_alt(self):
        self.assertEqual(mh827_gas_base(600000, 0.60), 360000.0)
        self.assertEqual(mh827_gas_alt(600000, 0.25), 150000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh827_c_base(282000.0, 0.28, 360000.0, 0.11, 40000), 158560.0)
        self.assertEqual(mh827_c_alt(174000.0, 0.28, 150000.0, 0.11, 72000), 137220.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh827_risparmio(158560.0, 137220.0), 21340.0)
        self.assertEqual(mh827_risparmio(137220.0, 158560.0), -21340.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh827_co2_base(282000.0, 360000.0), 143.22, places=9)
        self.assertAlmostEqual(mh827_co2_alt(174000.0, 150000.0), 73.8, places=9)
        self.assertAlmostEqual(
            mh827_co2_evitata(282000.0, 360000.0, 174000.0, 150000.0), 69.42, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh827_breakeven_gas(174000.0, 0.28, 72000, 282000.0, 40000, 360000.0, 150000.0)
        self.assertAlmostEqual(be, 0.008380952380952312, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh827_breakeven_gas(1000.0, 0.28, 1000, 282000.0, 40000, 360000.0, 150000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh827_breakeven_gas(174000.0, 0.28, 72000, 282000.0, 40000, 150000.0, 150000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh827_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh827_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh827_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh827_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh827_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh827_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh827_flussi(150000, 21340.0, 12)
        self.assertEqual(len(flussi), 13)
        self.assertEqual(flussi[0], -150000)
        self.assertTrue(all(f == 21340.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh827_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 39141.789921817566, places=6)
        self.assertEqual(mh827_van([-150000] + [21340.0] * 12, 0.0), 106080.0)

    def test_tir_demo(self):
        bc = mh827_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 9.370327622050521, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh827_payback([-150000] + [21340.0] * 12), 8)
        self.assertEqual(mh827_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh827_payback([-150000] + [100.0] * 12))

    def test_verdetto(self):
        self.assertEqual(mh827_verdetto(21340.0, 100.0, 150000, 10.0), "CONVIENTE")
        self.assertEqual(mh827_verdetto(15340.0, -14037.72, 150000, 10.0), "MARGINALE")
        self.assertEqual(mh827_verdetto(21340.0, -110858.21, 150000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh827_verdetto(0.0, 100.0, 150000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh827_verdetto(-100.0, 100.0, 150000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh827_verdetto(None, 100.0, 150000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh827_verdetto(21340.0, 0.0, 150000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh827_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("metri", "600000"), ("metri", float("nan")),
                            ("metri", float("inf")), ("metri", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh827_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"metri": 0}, {"metri": -1}, {"e_telai_base_kwh_e_m": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh827_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh827_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh827_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh827_valida(**_demo_kwargs(
            e_telai_base_kwh_e_m=0, e_comp_base_kwh_e_m=0,
            g_base_kwh_m=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh827_demo()
        self.assertEqual(d["metri"], 600000)
        self.assertEqual(d["e_telai_base_kwh_e_m"], 0.35)
        self.assertEqual(d["e_telai_alt_kwh_e_m"], 0.22)
        self.assertEqual(d["e_comp_base_kwh_e_m"], 0.12)
        self.assertEqual(d["e_comp_alt_kwh_e_m"], 0.07)
        self.assertEqual(d["g_base_kwh_m"], 0.60)
        self.assertEqual(d["g_alt_kwh_m"], 0.25)
        self.assertEqual(d["capex"], 150000)
        self.assertEqual(d["vita_anni"], 12)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh827_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh827_demo_calcoli()
        self.assertEqual(bc["e_telai_base_kwh_e_anno"], 210000.0)
        self.assertEqual(bc["e_telai_alt_kwh_e_anno"], 132000.0)
        self.assertEqual(bc["e_comp_base_kwh_e_anno"], 72000.0)
        self.assertAlmostEqual(bc["e_comp_alt_kwh_e_anno"], 42000.0, places=6)
        self.assertEqual(bc["c_base_eur_anno"], 158560.0)
        self.assertEqual(bc["c_alt_eur_anno"], 137220.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh827_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 13)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7], -620.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], 20720.0)

    def test_demo_tabella_righe(self):
        bc = mh827_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Metri di tessuto (metri/anno)", voci)
        self.assertIn("Telai baseline (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh827_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_telai_base_kwh_e_anno"] + bc["e_comp_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        metri = 600000
        e_base = metri * (0.35 + 0.12)
        e_alt = metri * (0.22 + 0.07)
        gas_base = metri * 0.60
        gas_alt = metri * 0.25
        c_base = e_base * 0.28 + gas_base * 0.11 + 40000
        c_alt = e_alt * 0.28 + gas_alt * 0.11 + 72000
        bc = mh827_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh827_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_azionamento_non_calcolabile(self):
        r = mh827_calcola(**_demo_kwargs(e_telai_alt_kwh_e_m=0.35))
        self.assertEqual(r["risparmio_eur_anno"], -500.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["van"], -154431.62581822442, places=6)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.11238095238095232, places=12)

    def test_variante_senza_compressore_non_convinte(self):
        r = mh827_calcola(**_demo_kwargs(e_comp_alt_kwh_e_m=0.12))
        self.assertEqual(r["risparmio_eur_anno"], 12940.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -35309.52382435244, places=6)
        self.assertEqual(r["payback"], 12)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.04838095238095231, places=12)

    def test_variante_senza_recupero_non_calcolabile(self):
        r = mh827_calcola(**_demo_kwargs(g_alt_kwh_m=0.60))
        self.assertEqual(r["risparmio_eur_anno"], -1760.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_300000_non_convinte(self):
        r = mh827_calcola(**_demo_kwargs(capex=300000))
        self.assertAlmostEqual(r["van"], -110858.21007818243, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(r["payback"])

    def test_variante_om_alt_78000_marginale(self):
        r = mh827_calcola(**_demo_kwargs(om_alt=78000))
        self.assertEqual(r["risparmio_eur_anno"], 15340.0)
        self.assertAlmostEqual(r["van"], -14037.719896875295, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 10)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.03695238095238088, places=12)

    def test_variante_om_alt_95000_non_calcolabile(self):
        r = mh827_calcola(**_demo_kwargs(om_alt=95000))
        self.assertEqual(r["risparmio_eur_anno"], -1660.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.11790476190476183, places=12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh827_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], 2440.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(basso["van"], -128373.66600706476, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh827_calcola(**_demo_kwargs(p_gas=0.20))
        self.assertEqual(alto["risparmio_eur_anno"], 40240.0)
        self.assertAlmostEqual(alto["van"], 206657.24585069998, places=6)
        self.assertAlmostEqual(alto["tir"], 24.979524632464, places=6)
        self.assertEqual(alto["payback"], 4)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh827_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 106080.0)
        self.assertEqual(zero["payback"], 8)
        dieci = mh827_calcola(**_demo_kwargs(vita_anni=8))
        self.assertAlmostEqual(dieci["van"], -12075.03971384371, places=6)
        self.assertEqual(dieci["verdetto"], "MARGINALE")
        self.assertEqual(dieci["payback"], 8)
        cinque = mh827_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(cinque["van"], -57608.967848738306, places=6)
        self.assertEqual(cinque["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(cinque["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh827_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh827_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh827_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_telai_e_recupero(self):
        base = mh827_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh827_calcola(**_demo_kwargs(e_telai_alt_kwh_e_m=0.30))["risparmio_eur_anno"], base)
        self.assertLess(mh827_calcola(**_demo_kwargs(g_alt_kwh_m=0.40))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh827_demo_calcoli()
        b = mh827_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh827_demo()
        attese = {"metri", "e_telai_base_kwh_e_m", "e_telai_alt_kwh_e_m",
                  "e_comp_base_kwh_e_m", "e_comp_alt_kwh_e_m",
                  "g_base_kwh_m", "g_alt_kwh_m", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["metri", "e_telai_base_kwh_e_m", "e_telai_alt_kwh_e_m",
                 "e_comp_base_kwh_e_m", "e_comp_alt_kwh_e_m",
                 "g_base_kwh_m", "g_alt_kwh_m", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh827_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("metri", "600000"), ("metri", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh827_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh827_calcola(**_demo_kwargs(e_telai_base_kwh_e_m=0,
                                         e_comp_base_kwh_e_m=0,
                                         g_base_kwh_m=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh827_calcola(**_demo_kwargs(g_alt_kwh_m=0.60))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh827_calcola(**_demo_kwargs(om_alt=95000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh827_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh827_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh827_demo_calcoli()
        csv = mh827_csv(bc, dict(mh827_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh827_demo_calcoli()
        csv = mh827_csv(bc, dict(mh827_demo()))
        self.assertIn("risparmio_eur_anno;21340.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh827_demo_calcoli()
        csv = mh827_csv(bc, dict(mh827_demo()))
        for chiave in mh827_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh826_", src)
        self.assertNotIn("mh825_", src)
        self.assertNotIn("mh824_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab827:"), 1)
        self.assertTrue(src.startswith("    # W829"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Tessitura: telai con azionamento efficiente", src)
        self.assertIn("recupero calore su climatizzazione sala telai", src)
        self.assertNotIn("tab826", src)
        self.assertNotIn("tab825", src)
        self.assertNotIn("tab824", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        # "pollaio"/"porcilaia" compaiono legittimamente solo
        # nella distinzione esplicita dell'header: qui si
        # vietano solo i residui di funzione delle tab vecchie.
        for vecchio in ("mh826_", "mh825_", "mh824_", "mh823_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh826_", src)
        self.assertNotIn("st826_", src)
        self.assertNotIn("mh825_", src)
        self.assertNotIn("st825_", src)
        chiavi = re.findall(r'key="(st827_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st827_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st827_calcola"', src)
        self.assertIn('key="st827_csv"', src)
        self.assertIn('key="st827_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def827\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh827_demo().keys()), lette - set(mh827_demo().keys()))
        self.assertEqual(lette, set(mh827_demo().keys()))

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg827"), src.index(".metric("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".metric("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
