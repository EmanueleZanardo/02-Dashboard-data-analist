"""Test nuova scheda tab829 "Serramenti in legno:
taglio/fresatura con motori efficienti +
aria compressa efficiente + recupero calore
su essiccazione vernici battono taglio
tradizionale + aria compressa tradizionale
+ essiccazione a gas?".

Business case deterministico di un
produttore di serramenti in legno guidato
dai M² DI SERRAMENTI IN LEGNO prodotti in
un anno: E_taglio_base = mq x e_taglio_base;
E_taglio_alt = mq x e_taglio_alt (i motori
efficienti riducono solo il taglio);
E_comp_base = mq x e_comp_base; E_comp_alt =
mq x e_comp_alt (il compressore efficiente riduce
solo l'aria compressa); E_base = E_taglio_base
+ E_comp_base; E_alt = E_taglio_alt + E_comp_alt;
gas_base = mq x g_base; gas_alt = mq x g_alt
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
0,014666666666666666 EUR/kWh (numeratore
1.056 EUR, denominatore 72.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(mq <= 0, specifici negativi, prezzi <= 0,
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
previsto (mq, prezzi, CAPEX, vita). Gli zeri
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
falegnameria generica (mobili e arredi vari:
qui niente mobili, solo m² di serramenti in
legno, processi taglio e fresatura profili in
legno, avvitatori e presse pneumatiche,
cabine di essiccazione vernici), dalla
vetreria (vetro, forni fusori: qui niente
forni fusori, niente vetro fuso) e dai
serramenti in PVC/alluminio (profili plastici
o metallici: qui solo profili in legno):
qui driver M² DI SERRAMENTI IN LEGNO +
TAGLIO/FRESATURA CON MOTORI EFFICIENTI +
ARIA COMPRESSA EFFICIENTE + RECUPERO
CALORE SU ESSICCAZIONE VERNICI.

Demo (serramenti in legno): 60.000 m² di
serramenti in legno prodotti in un anno,
taglio specifica base 1,50 (90.000 kWh_e/anno)
e alternativa 0,95 (57.000 kWh_e/anno),
aria compressa specifica base 0,60
(36.000 kWh_e/anno) e alternativa 0,32
(19.200 kWh_e/anno), elettricita' base
126.000 e alternativa 76.200 kWh_e/anno,
gas specifico base 2,20 (132.000 kWh/anno)
e alternativo 1,00 (60.000 kWh/anno, il
recupero riduce il gas del 54,55 %, non lo
azzera), prezzi elettricita' 0,28 e gas
0,11 EUR/kWh, O&M base 40.000 e alternativo
55.000 EUR/anno, CAPEX 50.000 EUR, WACC 5 %,
vita 12 anni, tolleranza 10 % del CAPEX.
Valori calcolati eseguendo
mh829_demo_calcoli(): E_base 126.000,
E_alt 76.200, gas_base 132.000,
gas_alt 60.000, C_base 89.800, C_alt 82.936,
risparmio 6.864, CO2_base 58,164, CO2_alt
31,17, CO2_evitata 26,994, VAN
10837,359232584611, TIR 8,661741715601408 %,
payback 8, breakeven gas
0,014666666666666666 EUR/kWh, verdetto
CONVIENTE.

Destinazione nel repo: tests/test_w829_serramenti.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w831_helpers import (
    demo_calcoli,
    mh829_breakeven_gas,
    mh829_c_alt,
    mh829_c_base,
    mh829_calcola,
    mh829_co2_alt,
    mh829_co2_base,
    mh829_co2_evitata,
    mh829_csv,
    mh829_demo,
    mh829_demo_calcoli,
    mh829_e_alt,
    mh829_e_base,
    mh829_e_comp_alt,
    mh829_e_comp_base,
    mh829_e_taglio_alt,
    mh829_e_taglio_base,
    mh829_flussi,
    mh829_gas_alt,
    mh829_gas_base,
    mh829_int_pos,
    mh829_nneg,
    mh829_num,
    mh829_payback,
    mh829_pos,
    mh829_risparmio,
    mh829_tir,
    mh829_valida,
    mh829_van,
    mh829_verdetto,
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


_HELPERS_PATH = _risolvi("w831_helpers.py")
_UI_PATH = _risolvi("w831_ui.py")

_DEMO = {
    "e_taglio_base_kwh_e_anno": 90000.0,
    "e_taglio_alt_kwh_e_anno": 57000.0,
    "e_comp_base_kwh_e_anno": 36000.0,
    "e_comp_alt_kwh_e_anno": 19200.0,
    "e_base_kwh_e_anno": 126000.0,
    "e_alt_kwh_e_anno": 76200.0,
    "gas_base_kwh_anno": 132000.0,
    "gas_alt_kwh_anno": 60000.0,
    "c_base_eur_anno": 89800.0,
    "c_alt_eur_anno": 82936.0,
    "risparmio_eur_anno": 6864.0,
    "co2_base_t_anno": 58.164,
    "co2_alt_t_anno": 31.17,
    "co2_evitata_t_anno": 26.994,
    "van": 10837.359232584611,
    "tir": 8.661741715601408,
    "payback": 8,
    "breakeven_gas_eur_kwh": 0.014666666666666666,
}


def _demo_kwargs(**over):
    kw = dict(mh829_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh829_num(3, "x"), 3.0)
        self.assertEqual(mh829_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh829_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh829_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh829_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh829_pos(0, "x")
        with self.assertRaises(ValueError):
            mh829_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh829_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh829_int_pos(15.5, "vita")


class TestFisica(unittest.TestCase):
    def test_cuc_comp_e_base(self):
        self.assertEqual(mh829_e_taglio_base(60000, 1.50), 90000.0)
        self.assertEqual(mh829_e_taglio_alt(60000, 0.95), 57000.0)
        self.assertEqual(mh829_e_comp_base(60000, 0.60), 36000.0)
        self.assertAlmostEqual(mh829_e_comp_alt(60000, 0.32), 19200.0, places=6)
        self.assertEqual(mh829_e_base(90000.0, 36000.0), 126000.0)
        self.assertAlmostEqual(mh829_e_alt(57000.0, 19200.0), 76200.0, places=6)

    def test_gas_base_alt(self):
        self.assertEqual(mh829_gas_base(60000, 2.20), 132000.0)
        self.assertEqual(mh829_gas_alt(60000, 1.00), 60000.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertEqual(mh829_c_base(126000.0, 0.28, 132000.0, 0.11, 40000), 89800.0)
        self.assertEqual(mh829_c_alt(76200.0, 0.28, 60000.0, 0.11, 55000), 82936.0)

    def test_risparmio_segno(self):
        self.assertEqual(mh829_risparmio(89800.0, 82936.0), 6864.0)
        self.assertEqual(mh829_risparmio(82936.0, 89800.0), -6864.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh829_co2_base(126000.0, 132000.0), 58.164, places=9)
        self.assertAlmostEqual(mh829_co2_alt(76200.0, 60000.0), 31.17, places=9)
        self.assertAlmostEqual(
            mh829_co2_evitata(126000.0, 132000.0, 76200.0, 60000.0), 26.994, places=9)


class TestFinanza(unittest.TestCase):
    def test_breakeven_demo_valore(self):
        be = mh829_breakeven_gas(76200.0, 0.28, 55000, 126000.0, 40000, 132000.0, 60000.0)
        self.assertAlmostEqual(be, 0.014666666666666666, places=12)

    def test_breakeven_numeratore_negativo_none(self):
        self.assertIsNone(mh829_breakeven_gas(1000.0, 0.28, 1000, 126000.0, 40000, 132000.0, 60000.0))

    def test_breakeven_gas_uguale_none(self):
        self.assertIsNone(mh829_breakeven_gas(76200.0, 0.28, 55000, 126000.0, 40000, 60000.0, 60000.0))

    def test_breakeven_verifica_pareggio_su_demo(self):
        bc = mh829_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        alt = mh829_c_alt(bc["e_alt_kwh_e_anno"], bc["p_el"],
                          bc["gas_alt_kwh_anno"], be, bc["om_alt"])
        base = mh829_c_base(bc["e_base_kwh_e_anno"], bc["p_el"],
                            bc["gas_base_kwh_anno"], be, bc["om_base"])
        self.assertAlmostEqual(alt, base, places=6)

    def test_breakeven_soglia_minima_su_demo(self):
        bc = mh829_demo_calcoli()
        be = bc["breakeven_gas_eur_kwh"]
        self.assertGreater(mh829_calcola(**_demo_kwargs(p_gas=be + 0.005))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh829_calcola(**_demo_kwargs(p_gas=be - 0.005))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh829_flussi(50000, 6864.0, 12)
        self.assertEqual(len(flussi), 13)
        self.assertEqual(flussi[0], -50000)
        self.assertTrue(all(f == 6864.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh829_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 10837.359232584611, places=6)
        self.assertEqual(mh829_van([-50000] + [6864.0] * 12, 0.0), 32368.0)

    def test_tir_demo(self):
        bc = mh829_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 8.661741715601408, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh829_payback([-50000] + [6864.0] * 12), 8)
        self.assertEqual(mh829_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh829_payback([-50000] + [100.0] * 12))

    def test_verdetto(self):
        self.assertEqual(mh829_verdetto(6864.0, 100.0, 50000, 10.0), "CONVIENTE")
        self.assertEqual(mh829_verdetto(5364.0, -2457.52, 50000, 10.0), "MARGINALE")
        self.assertEqual(mh829_verdetto(6864.0, -39162.64, 50000, 10.0), "NON_CONVIENTE")
        self.assertEqual(mh829_verdetto(0.0, 100.0, 50000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh829_verdetto(-100.0, 100.0, 50000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh829_verdetto(None, 100.0, 50000, 10.0), "NON_CALCOLABILE")
        self.assertEqual(mh829_verdetto(6864.0, 0.0, 50000, 10.0), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh829_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("mq", "60000"), ("mq", float("nan")),
                            ("mq", float("inf")), ("mq", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh829_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"mq": 0}, {"mq": -1}, {"e_taglio_base_kwh_e_mq": -0.1},
                     {"p_el": 0}, {"p_gas": -0.1}, {"om_alt": -1},
                     {"capex": 0}, {"wacc_pct": -1}, {"vita_anni": 0},
                     {"vita_anni": 15.5}, {"tolleranza_pct": -1}):
            self.assertFalse(mh829_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh829_valida(**_demo_kwargs(wacc_pct=25.0))["valido"])
        self.assertTrue(mh829_valida(**_demo_kwargs(tolleranza_pct=150.0))["valido"])
        self.assertTrue(mh829_valida(**_demo_kwargs(
            e_taglio_base_kwh_e_mq=0, e_comp_base_kwh_e_mq=0,
            g_base_kwh_mq=0, om_base=0, wacc_pct=0, tolleranza_pct=0))["valido"])

    def test_demo_dict(self):
        d = mh829_demo()
        self.assertEqual(d["mq"], 60000)
        self.assertEqual(d["e_taglio_base_kwh_e_mq"], 1.50)
        self.assertEqual(d["e_taglio_alt_kwh_e_mq"], 0.95)
        self.assertEqual(d["e_comp_base_kwh_e_mq"], 0.60)
        self.assertEqual(d["e_comp_alt_kwh_e_mq"], 0.32)
        self.assertEqual(d["g_base_kwh_mq"], 2.20)
        self.assertEqual(d["g_alt_kwh_mq"], 1.00)
        self.assertEqual(d["capex"], 50000)
        self.assertEqual(d["vita_anni"], 12)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh829_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_calcoli_fisica_economia(self):
        bc = mh829_demo_calcoli()
        self.assertEqual(bc["e_taglio_base_kwh_e_anno"], 90000.0)
        self.assertEqual(bc["e_taglio_alt_kwh_e_anno"], 57000.0)
        self.assertEqual(bc["e_comp_base_kwh_e_anno"], 36000.0)
        self.assertAlmostEqual(bc["e_comp_alt_kwh_e_anno"], 19200.0, places=6)
        self.assertEqual(bc["c_base_eur_anno"], 89800.0)
        self.assertEqual(bc["c_alt_eur_anno"], 82936.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh829_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 13)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7], -1952.0)
        self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], 4912.0)

    def test_demo_tabella_righe(self):
        bc = mh829_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Serramenti in legno (m²/anno)", voci)
        self.assertIn("Taglio/fresatura baseline (kWh_e/anno)", voci)
        self.assertIn("Gas alternativo (kWh/anno)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh829_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["e_taglio_base_kwh_e_anno"] + bc["e_comp_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        mq = 60000
        e_base = mq * (1.50 + 0.60)
        e_alt = mq * (0.95 + 0.32)
        gas_base = mq * 2.20
        gas_alt = mq * 1.00
        c_base = e_base * 0.28 + gas_base * 0.11 + 40000
        c_alt = e_alt * 0.28 + gas_alt * 0.11 + 55000
        bc = mh829_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], e_base, places=6)
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"], e_alt, places=6)
        self.assertAlmostEqual(bc["gas_base_kwh_anno"], gas_base, places=6)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], gas_alt, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh829_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_senza_motori_non_calcolabile(self):
        r = mh829_calcola(**_demo_kwargs(e_taglio_alt_kwh_e_mq=1.50))
        self.assertEqual(r["risparmio_eur_anno"], -2376.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["van"], -71059.08588820237, places=6)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.143, places=12)

    def test_variante_senza_compressore_non_convinte(self):
        r = mh829_calcola(**_demo_kwargs(e_comp_alt_kwh_e_mq=0.60))
        self.assertEqual(r["risparmio_eur_anno"], 2160.0)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -30855.376465270583, places=6)
        self.assertIsNone(r["payback"])
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.08, places=12)

    def test_variante_senza_recupero_non_calcolabile(self):
        r = mh829_calcola(**_demo_kwargs(g_alt_kwh_mq=2.20))
        self.assertEqual(r["risparmio_eur_anno"], -1056.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(r["breakeven_gas_eur_kwh"])

    def test_variante_capex_100000_non_convinte(self):
        r = mh829_calcola(**_demo_kwargs(capex=100000))
        self.assertAlmostEqual(r["van"], -39162.64076741539, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(r["payback"])

    def test_variante_om_alt_56500_marginale(self):
        r = mh829_calcola(**_demo_kwargs(om_alt=56500))
        self.assertEqual(r["risparmio_eur_anno"], 5364.0)
        self.assertAlmostEqual(r["van"], -2457.518222088594, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertEqual(r["payback"], 10)
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.0355, places=12)

    def test_variante_om_alt_65000_non_calcolabile(self):
        r = mh829_calcola(**_demo_kwargs(om_alt=65000))
        self.assertEqual(r["risparmio_eur_anno"], -3136.0)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["breakeven_gas_eur_kwh"], 0.15355555555555556, places=12)

    def test_variante_gas_basso_e_alto(self):
        basso = mh829_calcola(**_demo_kwargs(p_gas=0.02))
        self.assertAlmostEqual(basso["risparmio_eur_anno"], 384.0, places=6)
        self.assertEqual(basso["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(basso["van"], -46596.51137160366, places=6)
        self.assertIsNone(basso["payback"])
        alto = mh829_calcola(**_demo_kwargs(p_gas=0.20))
        self.assertEqual(alto["risparmio_eur_anno"], 13344.0)
        self.assertAlmostEqual(alto["van"], 68271.22983677288, places=6)
        self.assertAlmostEqual(alto["tir"], 24.822467250889467, places=6)
        self.assertEqual(alto["payback"], 4)
        self.assertEqual(alto["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero_e_vita_diversa(self):
        zero = mh829_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertEqual(zero["van"], 32368.0)
        self.assertEqual(zero["payback"], 8)
        otto = mh829_calcola(**_demo_kwargs(vita_anni=8))
        self.assertAlmostEqual(otto["van"], -5636.5076192981915, places=6)
        self.assertEqual(otto["verdetto"], "NON_CONVIENTE")
        self.assertEqual(otto["payback"], 8)
        cinque = mh829_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(cinque["van"], -20282.472132790062, places=6)
        self.assertEqual(cinque["verdetto"], "NON_CONVIENTE")
        self.assertIsNone(cinque["payback"])

    def test_monotonia_prezzo_gas_crescente(self):
        base = mh829_demo_calcoli()["risparmio_eur_anno"]
        self.assertGreater(mh829_calcola(**_demo_kwargs(p_gas=0.15))["risparmio_eur_anno"], base)
        self.assertLess(mh829_calcola(**_demo_kwargs(p_gas=0.05))["risparmio_eur_anno"], base)

    def test_monotonia_taglio_e_recupero(self):
        base = mh829_demo_calcoli()["risparmio_eur_anno"]
        self.assertLess(mh829_calcola(**_demo_kwargs(e_taglio_alt_kwh_e_mq=1.20))["risparmio_eur_anno"], base)
        self.assertLess(mh829_calcola(**_demo_kwargs(g_alt_kwh_mq=1.50))["risparmio_eur_anno"], base)

    def test_demo_deterministica_due_chiamate(self):
        a = mh829_demo_calcoli()
        b = mh829_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh829_demo()
        attese = {"mq", "e_taglio_base_kwh_e_mq", "e_taglio_alt_kwh_e_mq",
                  "e_comp_base_kwh_e_mq", "e_comp_alt_kwh_e_mq",
                  "g_base_kwh_mq", "g_alt_kwh_mq", "p_el", "p_gas",
                  "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                  "tolleranza_pct"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["mq", "e_taglio_base_kwh_e_mq", "e_taglio_alt_kwh_e_mq",
                 "e_comp_base_kwh_e_mq", "e_comp_alt_kwh_e_mq",
                 "g_base_kwh_mq", "g_alt_kwh_mq", "p_el", "p_gas",
                 "om_base", "om_alt", "capex", "wacc_pct", "vita_anni",
                 "tolleranza_pct"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh829_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("mq", "60000"), ("mq", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh829_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh829_calcola(**_demo_kwargs(e_taglio_base_kwh_e_mq=0,
                                         e_comp_base_kwh_e_mq=0,
                                         g_base_kwh_mq=0, om_base=0,
                                         wacc_pct=0, tolleranza_pct=0))
        self.assertTrue(r["valid"])
        r2 = mh829_calcola(**_demo_kwargs(g_alt_kwh_mq=2.20))
        self.assertIsNone(r2["breakeven_gas_eur_kwh"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh829_calcola(**_demo_kwargs(om_alt=108000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto(self):
        be = mh829_demo_calcoli()["breakeven_gas_eur_kwh"]
        r = mh829_calcola(**_demo_kwargs(p_gas=be))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh829_demo_calcoli()
        csv = mh829_csv(bc, dict(mh829_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh829_demo_calcoli()
        csv = mh829_csv(bc, dict(mh829_demo()))
        self.assertIn("risparmio_eur_anno;6864.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh829_demo_calcoli()
        csv = mh829_csv(bc, dict(mh829_demo()))
        for chiave in mh829_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh828_", src)
        self.assertNotIn("mh827_", src)
        self.assertNotIn("mh826_", src)
        self.assertNotIn("mh825_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab829:"), 1)
        self.assertTrue(src.startswith("    # W831"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Serramenti in legno: taglio/fresatura con motori efficienti", src)
        self.assertIn("recupero calore su essiccazione vernici", src)
        self.assertNotIn("tab828", src)
        self.assertNotIn("tab827", src)
        self.assertNotIn("tab826", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        # "falegnameria"/"vetreria"/"PVC" compaiono legittimamente
        # solo nella distinzione esplicita dell'header: qui si
        # vietano solo i residui di funzione delle tab vecchie.
        for vecchio in ("mh828_", "mh827_", "mh826_", "mh825_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh828_", src)
        self.assertNotIn("st828_", src)
        self.assertNotIn("mh827_", src)
        self.assertNotIn("st827_", src)
        chiavi = re.findall(r'key="(st829_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st829_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st829_calcola"', src)
        self.assertIn('key="st829_csv"', src)
        self.assertIn('key="st829_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def829\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh829_demo().keys()), lette - set(mh829_demo().keys()))
        self.assertEqual(lette, set(mh829_demo().keys()))

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg829"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)


if __name__ == "__main__":
    unittest.main()
