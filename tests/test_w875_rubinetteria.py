"""Test nuova scheda rubinetteria /
produzione rubinetti e valvolame: CNC
con inverter + lucidatura efficiente +
FV battono lavorazioni tradizionali +
essiccazione a gas?

Business case annuo di una rubinetteria,
guidato dai PEZZI all'anno prodotti
(demo 120.000 pezzi/anno):
lavorazioni meccaniche base 120.000 x
2,2 = 264.000 kWh/anno; lucidatura base
120.000 x 0,9 = 108.000 kWh/anno;
elettricita' base totale 372.000
kWh/anno, costo energia base 81.840
EUR/anno; gas base 120.000 x 0,45
= 54.000 Smc/anno, costo gas base
48.600 EUR/anno; O&M base 45.000
EUR/anno; costo base 175.440 EUR/anno;
CNC con inverter 120.000 x 1,65 =
198.000 kWh/anno; lucidatura
efficiente 120.000 x 0,6 = 72.000
kWh/anno; elettricita' alternativa
270.000 kWh/anno; kWp = sup x kwp/m2
(demo 300 kWp); E_pv 330.000 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt) (demo 198.000 kWh/anno); immessa
132.000 kWh/anno; deficit 72.000
kWh/anno; ricavo immissione 10.560
EUR/anno; O&M alternativa 35.000
EUR/anno; C_alt 40.280 EUR/anno;
risparmio 135.160 EUR/anno; CAPEX
280.000 + 90.000 + 300 x 900 = 640.000
EUR; CO2 base = (gas x 1,96 +
E_base x 0,35) / 1000 = 236,04
t/anno; CO2 alt = (deficit x 0,35) /
1000 = 25,20 t/anno (immessa senza
credito CO2); CO2 evitata 210,84
t/anno; flussi [-CAPEX, risparmio x
vita]; VAN al WACC (PERCENTUALE in
ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p_gas_star = (deficit x p_el -
ricavo_immissione + om_alt -
E_base x p_el - om_base) / gas in
forma chiusa (demo None: rapporto
negativo -1,60296, vince anche a gas
gratuito), None se il denominatore e'
nullo o negativo o se il rapporto e'
negativo. E' una SOGLIA MINIMA sui soli
costi annui (CAPEX escluso): sopra di
essa l'alternativa vince, sotto perde.
Verdetto: NON_VALUTABILE se input
degenere (pezzi <= 0, kWh per pezzo
< 0, prezzi < 0, O&M < 0, superficie < 0,
kwp per m2 < 0, resa < 0, f_autoconsumo
< 0 o > 1, voci CAPEX < 0, fattori CO2 <
0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Distinzione esplicita: NON marmificio
(niente lastre di marmo e pietra),
NON fonderia e NON pressofusione
(niente fusione), NON galvanica
(niente bagni galvanici), NON
falegnameria e NON serramenti (niente
legno); qui solo lavorazioni
meccaniche + lucidatura + FV su pezzi
di rubinetti e valvolame.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w875_helpers import (
        demo_calcoli,
        mh871_c_alt,
        mh871_c_base,
        mh871_calcola,
        mh871_capex_totale,
        mh871_co2_alt,
        mh871_co2_base,
        mh871_co2_evitata,
        mh871_csv,
        mh871_demo,
        mh871_demo_calcoli,
        mh871_e_alt,
        mh871_e_deficit,
        mh871_e_immessa,
        mh871_e_lucid_alt,
        mh871_e_lucid_base,
        mh871_e_base,
        mh871_e_pv,
        mh871_e_pv_auto,
        mh871_e_cnc_alt,
        mh871_e_mecc_base,
        mh871_flussi,
        mh871_frazione,
        mh871_gas_base,
        mh871_int_pos,
        mh871_kwp,
        mh871_nneg,
        mh871_num,
        mh871_p_gas_pareggio,
        mh871_payback,
        mh871_pos,
        mh871_ricavo_immissione,
        mh871_risparmio,
        mh871_sensibilita,
        mh871_tir,
        mh871_valida,
        mh871_van,
        mh871_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w875_helpers", os.path.join(_hf, "w875_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh871_c_alt = _mod.mh871_c_alt
    mh871_c_base = _mod.mh871_c_base
    mh871_calcola = _mod.mh871_calcola
    mh871_capex_totale = _mod.mh871_capex_totale
    mh871_co2_alt = _mod.mh871_co2_alt
    mh871_co2_base = _mod.mh871_co2_base
    mh871_co2_evitata = _mod.mh871_co2_evitata
    mh871_csv = _mod.mh871_csv
    mh871_demo = _mod.mh871_demo
    mh871_demo_calcoli = _mod.mh871_demo_calcoli
    mh871_e_alt = _mod.mh871_e_alt
    mh871_e_deficit = _mod.mh871_e_deficit
    mh871_e_immessa = _mod.mh871_e_immessa
    mh871_e_lucid_alt = _mod.mh871_e_lucid_alt
    mh871_e_lucid_base = _mod.mh871_e_lucid_base
    mh871_e_base = _mod.mh871_e_base
    mh871_e_pv = _mod.mh871_e_pv
    mh871_e_pv_auto = _mod.mh871_e_pv_auto
    mh871_e_cnc_alt = _mod.mh871_e_cnc_alt
    mh871_e_mecc_base = _mod.mh871_e_mecc_base
    mh871_flussi = _mod.mh871_flussi
    mh871_frazione = _mod.mh871_frazione
    mh871_gas_base = _mod.mh871_gas_base
    mh871_int_pos = _mod.mh871_int_pos
    mh871_kwp = _mod.mh871_kwp
    mh871_nneg = _mod.mh871_nneg
    mh871_num = _mod.mh871_num
    mh871_p_gas_pareggio = _mod.mh871_p_gas_pareggio
    mh871_payback = _mod.mh871_payback
    mh871_pos = _mod.mh871_pos
    mh871_ricavo_immissione = _mod.mh871_ricavo_immissione
    mh871_risparmio = _mod.mh871_risparmio
    mh871_sensibilita = _mod.mh871_sensibilita
    mh871_tir = _mod.mh871_tir
    mh871_valida = _mod.mh871_valida
    mh871_van = _mod.mh871_van
    mh871_verdetto = _mod.mh871_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w875_helpers.py")
_UI_PATH = _risolvi("w875_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh87" + "0"
_VECCHIO_TAB = "tab87" + "0"
_VECCHIO_ST = "st87" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli pre-apply (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")
_TITLES_SNAPSHOT = os.path.join(_HF_FALLBACK, "w874_titles.txt")

_DEMO = {
    "e_mecc_base_kwh_anno": 264000.0,
    "e_lucid_base_kwh_anno": 108000.0,
    "e_base_kwh_anno": 372000.0,
    "gas_base_smc_anno": 54000.0,
    "c_base_eur_anno": 175440.0,
    "e_cnc_alt_kwh_anno": 198000.0,
    "e_lucid_alt_kwh_anno": 72000.0,
    "e_alt_kwh_anno": 270000.0,
    "kwp": 300.0,
    "e_pv_kwh_anno": 330000.0,
    "e_pv_auto_kwh_anno": 198000.0,
    "e_immessa_kwh_anno": 132000.0,
    "e_deficit_kwh_anno": 72000.0,
    "ricavo_immissione_eur_anno": 10560.0,
    "c_alt_eur_anno": 40280.0,
    "risparmio_eur_anno": 135160.0,
    "capex_eur": 640000.0,
    "co2_base_t_anno": 236.04,
    "co2_alt_t_anno": 25.2,
    "co2_evitata_t_anno": 210.84,
    "van": 1044392.3498977037,
    "tir": 20.622000210529613,
    "payback": 5,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh871_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh871_num(3, "x"), 3.0)
        self.assertEqual(mh871_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh871_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh871_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh871_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh871_pos(0, "x")
        with self.assertRaises(ValueError):
            mh871_pos(-1, "x")
        self.assertEqual(mh871_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh871_int_pos(20, "x"), 20)
        self.assertEqual(mh871_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh871_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh871_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh871_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh871_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh871_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh871_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_mecc_e_lucid_base_e_costo_base(self):
        self.assertEqual(mh871_e_mecc_base(120000, 2.2), 264000.0)
        self.assertEqual(mh871_e_lucid_base(120000, 0.9), 108000.0)
        self.assertEqual(mh871_e_base(264000.0, 108000.0), 372000.0)
        self.assertEqual(mh871_gas_base(120000, 0.45), 54000.0)
        self.assertEqual(mh871_c_base(372000.0, 0.22, 54000.0, 0.90,
                                       45000), 175440.0)

    def test_cnc_alt_lucid_alt_somma(self):
        self.assertEqual(mh871_e_cnc_alt(120000, 1.65), 198000.0)
        self.assertEqual(mh871_e_lucid_alt(120000, 0.6), 72000.0)
        self.assertEqual(mh871_e_alt(198000.0, 72000.0), 270000.0)
        # L'inverter RIDUCE il CNC, non lo azzera:
        # 1,65 resta sopra zero anche a parita' di base 2,2.
        self.assertGreater(mh871_e_cnc_alt(120000, 1.65), 0.0)
        self.assertLess(mh871_e_cnc_alt(120000, 1.65),
                        mh871_e_mecc_base(120000, 2.2))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh871_kwp(1500, 0.20), 300.0)
        self.assertEqual(mh871_e_pv(300.0, 1100), 330000.0)
        self.assertEqual(mh871_e_pv_auto(330000.0, 0.60, 270000.0),
                         198000.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh871_e_pv_auto(330000.0, 1.0, 20000.0), 20000.0)
        self.assertEqual(mh871_e_immessa(330000.0, 198000.0), 132000.0)
        self.assertEqual(mh871_e_deficit(270000.0, 198000.0), 72000.0)
        self.assertEqual(mh871_e_deficit(20000.0, 25000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh871_ricavo_immissione(132000.0, 0.08), 10560.0)
        self.assertAlmostEqual(
            mh871_c_alt(72000.0, 0.22, 10560.0, 35000.0),
            40280.0)
        self.assertAlmostEqual(mh871_risparmio(175440.0, 40280.0),
                               135160.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh871_capex_totale(280000, 90000, 300.0,
                                            900),
                         640000.0)
        self.assertEqual(mh871_capex_totale(280000, 90000, 0.0,
                                            900),
                         370000.0)

    def test_co2_base_e_alt(self):
        cb = mh871_co2_base(54000.0, 1.96, 372000.0, 0.35)
        self.assertAlmostEqual(cb, 236.04, places=4)
        ca = mh871_co2_alt(72000.0, 0.35)
        self.assertAlmostEqual(ca, 25.2, places=4)
        self.assertAlmostEqual(mh871_co2_evitata(cb, ca), 210.84, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh871_co2_alt(0.0, 0.35), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh871_flussi(640000, 135160.0, 3),
                         [-640000, 135160.0, 135160.0, 135160.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh871_van([-100, 60, 60], 0), 20.0)
        bc = mh871_demo_calcoli()
        self.assertAlmostEqual(mh871_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh871_demo_calcoli()
        tir = mh871_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh871_tir([-100, -10, -10]))
        self.assertIsNone(mh871_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh871_demo_calcoli()
        self.assertEqual(mh871_payback(bc["flussi"]), 5)
        self.assertIsNone(mh871_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh871_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh871_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:5]), -99360.0, places=2)
        self.assertAlmostEqual(sum(flussi[:6]), 35800.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh871_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh871_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh871_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh871_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh871_verdetto(0.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh871_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_VALUTABILE")
        self.assertEqual(mh871_verdetto(None, 10.0, 1000, 10),
                         "NON_VALUTABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh871_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["e_deficit_kwh_anno"] * bc["p_el"]
             - bc["ricavo_immissione_eur_anno"]
             + bc["om_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], -1.602962962962963, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh871_p_gas_pareggio(54000.0, 372000.0, 72000.0,
                                 0.22, 10560.0, 45000.0, 200000.0),
            1.4525925925925927, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh871_p_gas_pareggio(54000.0, 372000.0,
                                              72000.0, 0.22, 10560.0,
                                              45000.0, 121560.0),
                         0.0)
        self.assertIsNone(mh871_p_gas_pareggio(0.0, 372000.0,
                                               72000.0, 0.22, 10560.0,
                                               45000.0, 35000.0))
        self.assertIsNone(mh871_p_gas_pareggio(54000.0, 372000.0,
                                               72000.0, 0.22, 10560.0,
                                               45000.0, 35000.0))

    def test_valida_demo_ok(self):
        demo = mh871_demo()
        val = mh871_valida(*[demo[k] for k in (
            "pezzi_anno", "e_mecc_base_per_pezzo",
            "e_lucid_base_per_pezzo", "p_el",
            "gas_per_pezzo", "p_gas", "om_base_eur_anno",
            "e_cnc_alt_per_pezzo", "e_lucid_alt_per_pezzo", "sup_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_cnc_eur", "capex_lucid_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_pezzi_zero_no(self):
        kw = _demo_kwargs(pezzi_anno=0)
        self.assertRaises(ValueError, mh871_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh871_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh871_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh871_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh871_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("pezzi_anno", -1),
                              ("e_mecc_base_per_pezzo", -1),
                              ("p_gas", -0.01),
                              ("capex_cnc_eur", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh871_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh871_calcola(mh871_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh871_calcola(dict(mh871_demo(), capex_cnc_eur=999999),
                           capex_cnc_eur=280000)
        self.assertEqual(bc["capex_eur"], 640000.0)

class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, int):
                    self.assertEqual(ottenuto, atteso)
                else:
                    self.assertLess(_rel(ottenuto, atteso), 1e-9)

    def test_demo_verdetto_convente(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 5)

    def test_coerenza_costi_e_co2(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(
            bc["co2_evitata_t_anno"],
            bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(
            bc["c_base_eur_anno"],
            bc["e_base_kwh_anno"] * bc["p_el"]
            + bc["gas_base_smc_anno"] * bc["p_gas"]
            + bc["om_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["ricavo_immissione_eur_anno"]
            + bc["om_alt_eur_anno"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["e_deficit_kwh_anno"] * bc["p_el"]
                         - bc["ricavo_immissione_eur_anno"]
                         + bc["om_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh871_sensibilita(**mh871_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               144880.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               1165525.03, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               148360.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               1208893.53, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               81040.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               639937.53, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 5)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 370000.0)
        self.assertAlmostEqual(s["senza_inverter"]["risparmio_eur_anno"],
                               120640.0, places=2)
        self.assertAlmostEqual(s["senza_inverter"]["van"],
                               863441.06, places=2)
        self.assertEqual(s["senza_inverter"]["payback"], 6)
        self.assertEqual(s["senza_inverter"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               404392.35, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 10)
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               403669.69, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               2063200.0, places=2)

    def test_marginale_con_capex_cnc_alto(self):
        # CAPEX totale 1.760.000 (CNC a 1.400.000):
        # VAN circa -75.607,65, entro la tolleranza del 10%
        # (176.000).
        bc = mh871_calcola(**_demo_kwargs(capex_cnc_eur=1400000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -75607.65, places=2)

    def test_non_convente_con_capex_cnc_altissimo(self):
        bc = mh871_calcola(**_demo_kwargs(capex_cnc_eur=1800000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -475607.65, places=2)

    def test_risparmio_non_positivo_restituisce_non_valutabile(self):
        bc = mh871_calcola(**_demo_kwargs(om_alt_eur_anno=300000))
        self.assertEqual(bc["verdetto"], "NON_VALUTABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -129840.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh871_csv(bc, mh871_demo())
        for voce in ("pezzi_anno", "e_mecc_base_kwh_anno",
                     "e_lucid_base_kwh_anno", "e_base_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -640000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Pezzi (pezzi/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh871_c_alt(270000.0, 0.22, 0.0, 35000.0)
        con = mh871_c_alt(72000.0, 0.22, 10560.0, 35000.0)
        self.assertAlmostEqual(senza - con, 270000.0 * 0.22 - 72000.0 * 0.22 + 10560.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh871_sensibilita(**mh871_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_inverter",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh871_csv(bc, mh871_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_mecc_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh871_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh871_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh871_calcola(**_demo_kwargs(sup_m2=0))
        self.assertEqual(bc["capex_eur"], 370000.0)
        bc = mh871_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def871\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh871_demo().keys()), lette - set(mh871_demo().keys()))
        self.assertEqual(lette, set(mh871_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc871\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc871\["([^"]+)"\]', src))
        attese = set(mh871_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli pre-apply: la copia di
        # lavoro del repo ha questo numero di blocchi
        # scheda prima dell'aggiunta di questa scheda.
        # Dopo l'apply il conteggio sale di uno: il
        # bump dell'apply deve aggiornare anche questo
        # assert, come fa per gli altri test di
        # conteggio, altrimenti il test fallisce
        # contro il repo aggiornato.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 873)
        elif os.path.exists(_TITLES_SNAPSHOT):
            with open(_TITLES_SNAPSHOT, encoding="utf-8") as f:
                self.assertEqual(sum(1 for _ in f), 869)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab871:"), 1)
        self.assertTrue(src.startswith("    # W875"))

    def test_ui_tab871_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab871:"), 1)
        self.assertIn("def mh871_demo(", src_h)
        self.assertIn("def mh871_calcola(", src_h)
        self.assertIn("tab871", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Rubinetteria / produzione rubinetti e valvolame: CNC con inverter + lucidatura efficiente + FV battono lavorazioni tradizionali + essiccazione a gas?", src)
        self.assertIn("🚰 Rubinetteria / produzione rubinetti e valvolame: CNC con inverter + lucidatura efficiente + FV battono lavorazioni tradizionali + essiccazione a gas?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        for vecchio in (_VECCHIO_MH,):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st871_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st871_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st871_calcola"', src)
        self.assertIn('key="st871_csv"', src)
        self.assertIn('key="st871_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg871"), src.index(".paiac("))
        self.assertLess(src.index("risparmio_eur_anno'] <= 0.0"), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)

    def test_ui_nessun_trattino_lungo(self):
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            self.assertNotIn("—", src)
            self.assertNotIn("–", src)


if __name__ == "__main__":
    unittest.main()
