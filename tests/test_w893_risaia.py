"""Test nuova scheda risaia:
essiccare il risone con pompa di calore +
recupero calore e irrigare efficiente + FV
battono essiccatore a gas + irrigazione
tradizionale?
Repo path: tests/test_w893_risaia.py

Business case annuo di una risaia,
guidato dalle TONNELLATE ANNUE DI RISONE
(demo 1000 t/anno):
acqua da evaporare 1000 x 1000 x (0,22 meno
0,14) diviso 0,86 = 93023,26 kg/anno; energia
gas base 93023,26 x 1,05 diviso 0,85 =
114911,08 kWh/anno; calore alternativo dopo
recupero 93023,26 x 1,05 per (1 meno 0,30) =
68372,09 kWh termici/anno; elettricita' pompa
di calore 68372,09 diviso 3,2 = 21366,28
kWh/anno; volume irriguo base 200 x 12000 =
2400000 m3/anno; volume alternativo 2400000
per (1 meno 0,15) = 2040000 m3/anno; energia
irrigazione base 87200,00 kWh/anno (eta 0,60),
alternativa 59296,00 kWh/anno (eta 0,75);
produzione FV 100 x 1150 = 115000 kWh/anno;
autoconsumo = min(0,70 per E_fv, E_hp piu
E_irr_alt) = 80500,00 kWh/anno; immessa 34500
kWh/anno; deficit 162,28 kWh/anno; risparmio
FV 80500 x 0,28 piu 34500 x 0,08 = 25300,00
EUR/anno; costo base 114911,08 x 0,09 piu
87200,00 x 0,28 = 34758,00 EUR/anno (senza
O&M base); costo alternativo 80662,28 x 0,28
meno 25300,00 piu 3500,00 = 785,44 EUR/anno;
risparmio 33972,56 EUR/anno; CAPEX 200000 +
30000 + 50000 + 100 x 850 = 365000 EUR; CO2
base = (E_gas_base x 0,20 + E_irr_base x 0,35)
/ 1000 = 53,50 t/anno; CO2 alt = (deficit x
0,35) / 1000 = 0,06 t/anno (immessa senza
credito CO2); CO2 evitata 53,45 t/anno; LCO
base 34,76 EUR/t e LCO alt 0,79 EUR/t (costi
operativi annui per tonnellata, CAPEX
escluso); flussi [CAPEX negativo, risparmio x
vita]; VAN al tasso (FRAZIONE in ingresso,
0,05 = 5 %, usato diretto, NON diviso per
100); TIR per bisezione su intervallo da meno
0,9 a 5,0; payback (primo anno con cumulato
maggiore o uguale a 0). Tolleranza in
PERCENTUALE (10 = 10 % del CAPEX).
Verdetto: NON_CALCOLABILE se input degenere
(produzione minore o uguale a 0, umidita
raccolta o target fuori [0, 1], umidita
target uguale a 1, umidita raccolta sotto
umidita target, energia gas per kg negativa,
eta essiccatore gas minore o uguale a 0,
recupero minore di 0 o maggiore di 1, COP
minore o uguale a 0, superficie negativa,
volume per ha negativo, prevalenza negativa,
eta pompe minori o uguali a 0, riduzione
volume minore di 0 o maggiore di 1, prezzi
minori di 0, potenza FV negativa, resa
negativa, quota autoconsumo minore di 0 o
maggiore di 1, O&M negativa, voci CAPEX
minori di 0, fattori CO2 minori di 0, tasso
minore di 0, vita minore o uguale a 0 o non
intera, tolleranza minore di 0) o se
risparmio minore o uguale a 0 (guard
degenere: UI salta KPI, grafico, tabella e
CSV); altrimenti CONVIENTE se VAN maggiore di
0, MARGINALE se VAN negativa entro tolleranza
PERCENTUALE del CAPEX, NON_CONVIENTE
altrimenti.
Casi limite: produzione zero non calcolabile
(ValueError negli helper, guard NON_CALCOLABILE in
UI); umidita target uguale a umidita raccolta
(acqua zero, E_hp zero); quota FV zero
(autoconsumo zero); prezzo gas zero (costo
base 24416,00, risparmio 23630,56 ancora
positivo, ma VAN meno 70510,97 e verdetto
NON_CONVIENTE: il risparmio da solo non
basta, serve anche che la VAN copra il
CAPEX); FV che non supera il fabbisogno
elettrico (autoconsumo cappato alla domanda:
con FV grande l'autoconsumata e' uguale a
E_hp piu E_irr_alt e il deficit e' zero);
CAPEX zero (TIR non definita, payback 0);
tasso zero (VAN uguale alla somma dei
flussi).
Distinzione esplicita: qui SOLO risone come
prodotto agricolo (essiccazione del risone,
irrigazione della risaia, FV), NIENTE altri
cereali, NIENTE altri raccolti, NIENTE
allevamenti, NIENTE latte, NIENTE
trasformazione del latte, NIENTE serre,
NIENTE altri settori agricoli; qui solo
risaia: essiccazione + irrigazione + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w893_helpers import (
        demo_calcoli,
        mh888_autoconsumo,
        mh888_c_alt,
        mh888_c_base,
        mh888_calcola,
        mh888_capex_totale,
        mh888_co2_alt,
        mh888_co2_base,
        mh888_co2_evitata,
        mh888_csv,
        mh888_demo,
        mh888_demo_calcoli,
        mh888_e_deficit,
        mh888_e_fv,
        mh888_e_gas_base,
        mh888_e_hp,
        mh888_e_immessa,
        mh888_e_irr,
        mh888_flussi,
        mh888_frazione,
        mh888_fv_risparmio,
        mh888_int_pos,
        mh888_lco,
        mh888_m_acqua,
        mh888_nneg,
        mh888_num,
        mh888_payback,
        mh888_pos,
        mh888_q_th_alt,
        mh888_risparmio,
        mh888_sensibilita,
        mh888_tir,
        mh888_v_alt,
        mh888_v_base,
        mh888_valida,
        mh888_van,
        mh888_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w893_helpers", os.path.join(_hf, "w893_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh888_autoconsumo = _mod.mh888_autoconsumo
    mh888_c_alt = _mod.mh888_c_alt
    mh888_c_base = _mod.mh888_c_base
    mh888_calcola = _mod.mh888_calcola
    mh888_capex_totale = _mod.mh888_capex_totale
    mh888_co2_alt = _mod.mh888_co2_alt
    mh888_co2_base = _mod.mh888_co2_base
    mh888_co2_evitata = _mod.mh888_co2_evitata
    mh888_csv = _mod.mh888_csv
    mh888_demo = _mod.mh888_demo
    mh888_demo_calcoli = _mod.mh888_demo_calcoli
    mh888_e_deficit = _mod.mh888_e_deficit
    mh888_e_fv = _mod.mh888_e_fv
    mh888_e_gas_base = _mod.mh888_e_gas_base
    mh888_e_hp = _mod.mh888_e_hp
    mh888_e_immessa = _mod.mh888_e_immessa
    mh888_e_irr = _mod.mh888_e_irr
    mh888_flussi = _mod.mh888_flussi
    mh888_frazione = _mod.mh888_frazione
    mh888_fv_risparmio = _mod.mh888_fv_risparmio
    mh888_int_pos = _mod.mh888_int_pos
    mh888_lco = _mod.mh888_lco
    mh888_m_acqua = _mod.mh888_m_acqua
    mh888_nneg = _mod.mh888_nneg
    mh888_num = _mod.mh888_num
    mh888_payback = _mod.mh888_payback
    mh888_pos = _mod.mh888_pos
    mh888_q_th_alt = _mod.mh888_q_th_alt
    mh888_risparmio = _mod.mh888_risparmio
    mh888_sensibilita = _mod.mh888_sensibilita
    mh888_tir = _mod.mh888_tir
    mh888_v_alt = _mod.mh888_v_alt
    mh888_v_base = _mod.mh888_v_base
    mh888_valida = _mod.mh888_valida
    mh888_van = _mod.mh888_van
    mh888_verdetto = _mod.mh888_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w893_helpers.py")
_UI_PATH = _risolvi("w893_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "7"
_VECCHIO_TAB = "tab88" + "7"
_VECCHIO_ST = "st88" + "7_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "m_acqua_kg": 93023.25581395347,
    "e_gas_base_kwh_anno": 114911.0807113543,
    "q_th_alt_kwh_anno": 68372.0930232558,
    "e_hp_kwh_anno": 21366.279069767435,
    "v_base_m3_anno": 2400000.0,
    "v_alt_m3_anno": 2040000.0,
    "e_irr_base_kwh_anno": 87200.0,
    "e_irr_alt_kwh_anno": 59296.0,
    "e_fv_kwh_anno": 115000.0,
    "autoconsumo_kwh_anno": 80500.0,
    "e_immessa_kwh_anno": 34500.0,
    "e_deficit_kwh_anno": 162.27906976743543,
    "fv_risparmio_eur_anno": 25300.000000000004,
    "c_base_eur_anno": 34757.99726402189,
    "c_alt_eur_anno": 785.4381395348792,
    "risparmio_eur_anno": 33972.559124487016,
    "capex_eur": 365000.0,
    "co2_base_t_anno": 53.50221614227086,
    "co2_alt_t_anno": 0.056797674418602395,
    "co2_evitata_t_anno": 53.44541846785226,
    "lco_base_eur_t": 34.75799726402189,
    "lco_alt_eur_t": 0.7854381395348792,
    "van": 58373.1776837331,
    "tir": 6.819871024515003,
    "payback": 11,
}


def _demo_kwargs(**over):
    kw = dict(mh888_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh888_num(3, "x"), 3.0)
        self.assertEqual(mh888_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh888_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh888_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh888_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh888_pos(0, "x")
        with self.assertRaises(ValueError):
            mh888_pos(-1, "x")
        self.assertEqual(mh888_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh888_int_pos(20, "x"), 20)
        self.assertEqual(mh888_int_pos(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh888_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh888_int_pos(20.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh888_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh888_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh888_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh888_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_m_acqua_e_gas_base(self):
        self.assertAlmostEqual(mh888_m_acqua(1000, 0.22, 0.14),
                               93023.26, places=2)
        self.assertAlmostEqual(
            mh888_e_gas_base(93023.25581395347, 1.05, 0.85),
            114911.08, places=2)
        self.assertAlmostEqual(
            mh888_q_th_alt(93023.25581395347, 1.05, 0.30),
            68372.09, places=2)
        self.assertAlmostEqual(
            mh888_e_hp(68372.0930232558, 3.2), 21366.28, places=2)

    def test_pompa_converte_non_azzera_e_recupero_riduce(self):
        # La pompa di calore converte il consumo di
        # essiccazione in elettricita', non lo azzera.
        self.assertGreater(mh888_e_hp(68372.0930232558, 3.2), 0.0)
        self.assertLess(mh888_e_hp(68372.0930232558, 3.2),
                        68372.0930232558)
        # Il recupero calore RIDUCE il fabbisogno
        # termico, non lo azzera: 68372,09 resta
        # sopra zero e sotto il caso senza recupero.
        self.assertGreater(
            mh888_q_th_alt(93023.25581395347, 1.05, 0.30), 0.0)
        self.assertLess(
            mh888_q_th_alt(93023.25581395347, 1.05, 0.30),
            mh888_q_th_alt(93023.25581395347, 1.05, 0.0))
        self.assertAlmostEqual(
            mh888_q_th_alt(93023.25581395347, 1.05, 0.0),
            97674.42, places=2)

    def test_irrigazione_volumi_ed_energie(self):
        self.assertEqual(mh888_v_base(200, 12000), 2400000.0)
        self.assertEqual(mh888_v_alt(2400000.0, 0.15), 2040000.0)
        self.assertEqual(mh888_e_irr(2400000, 8, 0.60), 87200.0)
        self.assertEqual(mh888_e_irr(2040000, 8, 0.75), 59296.0)
        # L'irrigazione efficiente RIDUCE volume ed
        # energia, non li azzera.
        self.assertGreater(mh888_v_alt(2400000.0, 0.15), 0.0)
        self.assertLess(mh888_v_alt(2400000.0, 0.15),
                        mh888_v_base(200, 12000))
        self.assertGreater(mh888_e_irr(2040000, 8, 0.75), 0.0)
        self.assertLess(mh888_e_irr(2040000, 8, 0.75),
                        mh888_e_irr(2400000, 8, 0.60))
        with self.assertRaises(ValueError):
            mh888_e_irr(2400000, 8, 0)

    def test_m_acqua_umidita_target_uno_no(self):
        with self.assertRaises(ValueError):
            mh888_m_acqua(1000, 0.22, 1.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh888_e_fv(100, 1150), 115000.0)
        self.assertEqual(
            mh888_autoconsumo(115000.0, 0.70, 21366.279069767435,
                              59296.0),
            80500.0)
        # Cap min(): anche con quota 1,0 la domanda
        # piccola limita l'autoconsumo.
        self.assertAlmostEqual(
            mh888_autoconsumo(115000.0, 1.0, 21366.279069767435,
                              59296.0),
            80662.28, places=2)
        self.assertEqual(mh888_e_immessa(115000.0, 80500.0), 34500.0)
        self.assertAlmostEqual(
            mh888_e_deficit(21366.279069767435, 59296.0, 80500.0),
            162.28, places=2)
        self.assertEqual(mh888_e_deficit(21366.279069767435, 59296.0,
                                         90000.0), 0.0)

    def test_fv_non_supera_fabbisogno_elettrico(self):
        # Con FV molto grande (1000 kWp, produzione
        # 1150000 kWh/anno) l'autoconsumo resta
        # cappato alla domanda alternativa:
        # autoconsumata uguale a E_hp piu E_irr_alt,
        # deficit zero.
        bc = mh888_calcola(**_demo_kwargs(fv_kwp=1000))
        self.assertAlmostEqual(bc["autoconsumo_kwh_anno"],
                               bc["e_hp_kwh_anno"]
                               + bc["e_irr_alt_kwh_anno"])
        self.assertEqual(bc["e_deficit_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["e_immessa_kwh_anno"],
                               1069337.72, places=2)
        self.assertLessEqual(bc["autoconsumo_kwh_anno"],
                             bc["e_hp_kwh_anno"]
                             + bc["e_irr_alt_kwh_anno"])
        # Proprieta' generale: l'autoconsumo non
        # supera mai la domanda, in demo e con FV
        # grande.
        for caso in (demo_calcoli(), bc):
            self.assertLessEqual(
                caso["autoconsumo_kwh_anno"],
                caso["e_hp_kwh_anno"] + caso["e_irr_alt_kwh_anno"])

    def test_fv_risparmio_e_costi(self):
        self.assertAlmostEqual(
            mh888_fv_risparmio(80500.0, 0.28, 34500.0, 0.08), 25300.0,
            places=2)
        self.assertAlmostEqual(
            mh888_c_base(114911.0807113543, 0.09, 87200.0, 0.28),
            34758.00, places=2)
        self.assertAlmostEqual(
            mh888_c_alt(21366.279069767435, 59296.0, 0.28,
                        25300.0, 3500),
            785.44, places=2)
        self.assertAlmostEqual(
            mh888_risparmio(34757.99726402189, 785.4381395348792),
            33972.56, places=2)

    def test_capex_totale_voci(self):
        self.assertEqual(mh888_capex_totale(200000, 30000, 50000,
                                            100, 850),
                         365000.0)
        self.assertEqual(mh888_capex_totale(200000, 30000, 50000,
                                            0, 850),
                         280000.0)

    def test_co2_base_e_alt(self):
        cb = mh888_co2_base(114911.0807113543, 0.20, 87200.0, 0.35)
        self.assertAlmostEqual(cb, 53.50, places=2)
        ca = mh888_co2_alt(162.27906976743543, 0.35)
        self.assertAlmostEqual(ca, 0.06, places=2)
        self.assertAlmostEqual(mh888_co2_evitata(cb, ca), 53.45,
                               places=2)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh888_co2_alt(0.0, 0.35), 0.0)

    def test_lco_base_e_alt(self):
        self.assertAlmostEqual(mh888_lco(34757.99726402189, 1000),
                               34.76, places=2)
        self.assertAlmostEqual(mh888_lco(785.4381395348792, 1000),
                               0.79, places=2)
        with self.assertRaises(ValueError):
            mh888_lco(34757.99726402189, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh888_flussi(365000, 33972.56, 3),
                         [-365000, 33972.56, 33972.56, 33972.56])

    def test_van_tasso_zero_e_cinque(self):
        self.assertAlmostEqual(mh888_van([-100, 60, 60], 0), 20.0)
        bc = mh888_demo_calcoli()
        self.assertAlmostEqual(mh888_van(bc["flussi"], 0.05), bc["van"])

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 58373,18; con 5,0 (cioe' 500 % se
        # letto come frazione) sarebbe tutt'altra.
        bc = mh888_demo_calcoli()
        self.assertAlmostEqual(mh888_van(bc["flussi"], 0.05),
                               58373.18, places=2)
        self.assertNotAlmostEqual(mh888_van(bc["flussi"], 5.0),
                                  58373.18, places=2)

    def test_tir_demo(self):
        bc = mh888_demo_calcoli()
        tir = mh888_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh888_tir([-100, -10, -10]))
        self.assertIsNone(mh888_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh888_demo_calcoli()
        self.assertEqual(mh888_payback(bc["flussi"]), 11)
        self.assertIsNone(mh888_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh888_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh888_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:11]), -25274.41, places=2)
        self.assertAlmostEqual(sum(flussi[:12]), 8698.15, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh888_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh888_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh888_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh888_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh888_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh888_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh888_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh888_demo()
        val = mh888_valida(*[demo[k] for k in (
            "produzione_t_anno", "umidita_raccolta",
            "umidita_target", "e_gas_per_kg",
            "eta_essiccatore_gas", "recupero_calore",
            "cop_hp", "superficie_ha",
            "volume_irriguo_per_ha", "prevalenza_m",
            "eta_pompa_base", "eta_pompa_alt",
            "riduzione_volume", "prezzo_gas", "prezzo_el",
            "prezzo_cessione", "fv_kwp", "fv_resa",
            "fv_autoconsumo", "om_alt", "capex_hp",
            "capex_recupero", "capex_irrigazione",
            "capex_fv_per_kwp", "f_co2_gas", "f_co2_el",
            "tasso", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_produzione_zero_no(self):
        kw = _demo_kwargs(produzione_t_anno=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_eta_e_cop_zero_no(self):
        kw = _demo_kwargs(eta_essiccatore_gas=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        kw = _demo_kwargs(cop_hp=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        kw = _demo_kwargs(eta_pompa_base=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        kw = _demo_kwargs(eta_pompa_alt=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_umidita_target_uno_no(self):
        kw = _demo_kwargs(umidita_target=1.0)
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_umidita_raccolta_sotto_target_no(self):
        kw = _demo_kwargs(umidita_raccolta=0.10)
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(fv_autoconsumo=1.1)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        kw = _demo_kwargs(recupero_calore=1.1)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        kw = _demo_kwargs(riduzione_volume=1.1)
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_gas=float("nan"))
        self.assertRaises(ValueError, mh888_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("produzione_t_anno", -1),
                              ("e_gas_per_kg", -0.01),
                              ("prezzo_gas", -0.01),
                              ("capex_hp", -1),
                              ("capex_irrigazione", -1),
                              ("superficie_ha", -1),
                              ("tasso", -0.01),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh888_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh888_calcola(mh888_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh888_calcola(dict(mh888_demo(), capex_hp=99999),
                           capex_hp=200000)
        self.assertEqual(bc["capex_eur"], 365000.0)


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
        self.assertEqual(bc["payback"], 11)

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
            bc["e_gas_base_kwh_anno"] * bc["prezzo_gas"]
            + bc["e_irr_base_kwh_anno"] * bc["prezzo_el"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            (bc["e_hp_kwh_anno"] + bc["e_irr_alt_kwh_anno"])
            * bc["prezzo_el"]
            - bc["fv_risparmio_eur_anno"]
            + bc["om_alt"])
        self.assertAlmostEqual(
            bc["lco_base_eur_t"],
            bc["c_base_eur_anno"] / bc["produzione_t_anno"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_t"],
            bc["c_alt_eur_anno"] / bc["produzione_t_anno"])
        self.assertAlmostEqual(
            bc["fv_risparmio_eur_anno"],
            bc["autoconsumo_kwh_anno"] * bc["prezzo_el"]
            + bc["e_immessa_kwh_anno"] * bc["prezzo_cessione"])

    def test_sensibilita_valori(self):
        s = mh888_sensibilita(**mh888_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               36040.96, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               84150.01, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 11)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               38846.67, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               119115.39, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 10)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               8672.56, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               -171920.74, places=2)
        self.assertIsNone(s["senza_fv"]["payback"])
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 280000.0)
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               31408.61, places=2)
        self.assertAlmostEqual(s["senza_recupero"]["van"],
                               26420.65, places=2)
        self.assertEqual(s["senza_recupero"]["payback"], 12)
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -306626.82, places=2)
        self.assertIsNone(s["capex_doppio"]["payback"])
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               -102672.90, places=2)
        self.assertIsNone(s["vita_10"]["payback"])
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["tasso_0"]["van"],
                               314451.18, places=2)

    def test_marginale_con_capex_hp_alto(self):
        # CAPEX totale 427000 (pompa di calore a 262000):
        # VAN circa meno 3626,82, entro la tolleranza del 10%
        # (42700).
        bc = mh888_calcola(**_demo_kwargs(capex_hp=262000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -3626.82, places=2)

    def test_non_convente_con_capex_hp_altissimo(self):
        bc = mh888_calcola(**_demo_kwargs(capex_hp=900000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -641626.82, places=2)
        self.assertIsNone(bc["payback"])

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh888_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -162527.44,
                               places=2)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh888_csv(bc, mh888_demo())
        for voce in ("produzione_t_anno", "m_acqua_kg",
                     "e_gas_base_kwh_anno", "q_th_alt_kwh_anno",
                     "e_hp_kwh_anno", "v_base_m3_anno",
                     "e_irr_alt_kwh_anno", "fv_risparmio_eur_anno",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_t", "lco_alt_eur_t"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -365000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Produzione (t/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh888_c_alt(21366.279069767435, 59296.0, 0.28, 0.0,
                            3500)
        con = mh888_c_alt(21366.279069767435, 59296.0, 0.28, 25300.0,
                          3500)
        self.assertAlmostEqual(senza - con, 25300.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh888_sensibilita(**mh888_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_recupero",
                          "capex_doppio", "vita_10", "tasso_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh888_csv(bc, mh888_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("m_acqua_kg;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh888_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh888_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh888_calcola(**_demo_kwargs(fv_kwp=0))
        self.assertEqual(bc["capex_eur"], 280000.0)
        bc = mh888_calcola(**_demo_kwargs(fv_autoconsumo=0))
        self.assertEqual(bc["autoconsumo_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(produzione_t_anno=0)
        self.assertRaises(ValueError, mh888_calcola, **kw)
        self.assertFalse(mh888_valida(*[kw[k] for k in (
            "produzione_t_anno", "umidita_raccolta",
            "umidita_target", "e_gas_per_kg",
            "eta_essiccatore_gas", "recupero_calore",
            "cop_hp", "superficie_ha",
            "volume_irriguo_per_ha", "prevalenza_m",
            "eta_pompa_base", "eta_pompa_alt",
            "riduzione_volume", "prezzo_gas", "prezzo_el",
            "prezzo_cessione", "fv_kwp", "fv_resa",
            "fv_autoconsumo", "om_alt", "capex_hp",
            "capex_recupero", "capex_irrigazione",
            "capex_fv_per_kwp", "f_co2_gas", "f_co2_el",
            "tasso", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh888_calcola(**_demo_kwargs(fv_autoconsumo=0))
        self.assertEqual(bc["autoconsumo_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 115000.0)
        self.assertAlmostEqual(bc["e_deficit_kwh_anno"], 80662.28,
                               places=2)
        self.assertAlmostEqual(bc["fv_risparmio_eur_anno"],
                               9200.0)

    def test_prezzo_gas_zero(self):
        # A gas gratuito il risparmio resta positivo
        # (23630,56) perche' il costo base tiene
        # anche l'irrigazione, ma la VAN diventa
        # negativa (meno 70510,97) e il verdetto e'
        # NON_CONVIENTE: il risparmio da solo non
        # basta, serve anche che la VAN copra il
        # CAPEX.
        bc = mh888_calcola(**_demo_kwargs(prezzo_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 24416.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 23630.56,
                               places=2)
        self.assertAlmostEqual(bc["van"], -70510.97, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["payback"], 16)

    def test_umidita_target_uguale_raccolta(self):
        # Umidita target uguale alla raccolta: acqua
        # zero, E_hp zero, costo alternativo negativo
        # (il risparmio FV supera i costi elettrici).
        bc = mh888_calcola(**_demo_kwargs(umidita_target=0.22))
        self.assertEqual(bc["m_acqua_kg"], 0.0)
        self.assertEqual(bc["e_hp_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], -956.32,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh888_calcola(**_demo_kwargs(capex_hp=0,
                                          capex_recupero=0,
                                          capex_irrigazione=0,
                                          capex_fv_per_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero(self):
        bc = mh888_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(bc["van"], 314451.18, places=2)
        self.assertEqual(bc["payback"], 11)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def888\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh888_demo().keys()), lette - set(mh888_demo().keys()))
        self.assertEqual(lette, set(mh888_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc888\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc888\["([^"]+)"\]', src))
        attese = set(mh888_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 887 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 888.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 888)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab888:"), 1)
        self.assertTrue(src.startswith("    # W893"))

    def test_ui_tab888_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab888:"), 1)
        self.assertIn("def mh888_demo(", src_h)
        self.assertIn("def mh888_calcola(", src_h)
        self.assertIn("tab888", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Risaia: essiccare il risone con pompa di calore + recupero calore e irrigare efficiente + FV battono essiccatore a gas + irrigazione tradizionale?", src)
        self.assertIn("🌾 Risaia: essiccare il risone con pompa di calore + recupero calore e irrigare efficiente + FV battono essiccatore a gas + irrigazione tradizionale?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st888_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st888_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st888_calcola"', src)
        self.assertIn('key="st888_csv"', src)
        self.assertIn('key="st888_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg888"), src.index(".paiac("))
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
            self.assertNotIn(chr(8212), src)
            self.assertNotIn(chr(8211), src)

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato).
        import textwrap as _tw
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            if percorso == _UI_PATH:
                src = _tw.dedent(src)
            tree = ast.parse(src)
            for nodo in ast.walk(tree):
                if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                    if nodo.value == "utf-8":
                        continue
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)


if __name__ == "__main__":
    unittest.main()
