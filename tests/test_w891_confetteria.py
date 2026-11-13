"""Test nuova scheda confetteria:
cottura con pompa di calore + recupero calore +
essiccazione efficiente + lucidatura efficiente +
LED + FV battono
cottura a gas + essiccazione a gas +
lucidatura tradizionale + illuminazione tradizionale?
Repo path: tests/test_w891_confetteria.py

Business case annuo di una confetteria,
guidato dai KG ANNUI DI CONFETTI E CARAMELLE
(demo 400000 kg/anno):
cottura sciroppo a gas 400000 x 0,12 =
48000 Smc/anno; essiccazione a gas 400000 x 0,08
= 32000 Smc/anno; gas base totale 80000 Smc/anno,
costo gas base 72000 EUR/anno; lucidatura
tradizionale 400000 x 0,35 = 140000 kWh/anno;
illuminazione tradizionale 400000 x 0,10 = 40000
kWh/anno; elettricita' base totale 180000
kWh/anno, costo energia base 39600 EUR/anno;
O&M base 45000 EUR/anno; costo base 156600
EUR/anno; cottura con pompa di calore 1,20 kWh
termici per kg diviso COP 3,0 = 0,40 kWh/kg
(160000 kWh/anno); essiccazione efficiente con
recupero calore 0,90 kWh termici per kg per
(1 meno 0,30) diviso COP 2,5 = 0,252 kWh/kg
(100800 kWh/anno); lucidatura efficiente 400000 x
0,20 = 80000 kWh/anno; illuminazione LED 400000 x
0,03 = 12000 kWh/anno; elettricita' alternativa
352800 kWh/anno, gas ELIMINATO (l'alternativa
elettrifica cottura ed essiccazione, quindi
l'elettricita' alternativa e' MAGGIORE della base);
kWp = sup FV x kwp per m2 (demo 160 kWp); E_pv
176000 kWh/anno; E_pv_auto = min(E_pv x
f_autoconsumo, E_alt) (demo 105600 kWh/anno);
immessa 70400 kWh/anno; deficit 247200 kWh/anno;
ricavo immissione 5632 EUR/anno; O&M alternativa
38000 EUR/anno; C_alt 86752 EUR/anno; risparmio
69848 EUR/anno; CAPEX 120000 + 90000 + 35000 +
15000 + 160 x 900 = 404000 EUR; CO2 base = (gas
x 1,95 + E_base x 0,25) / 1000 = 201,00 t/anno;
CO2 alt = (deficit x 0,25) / 1000 = 61,80 t/anno
(immessa senza credito CO2); CO2 evitata 139,20
t/anno; LCO base 0,3915 EUR/kg e LCO alt 0,21688
EUR/kg (costi operativi annui per kg, CAPEX
escluso); flussi [CAPEX negativo, risparmio x
vita]; VAN al WACC (PERCENTUALE in ingresso, /
100 dentro); TIR per bisezione; payback (primo
anno con cumulato maggiore o uguale a 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno
gas_alt) in forma chiusa (demo 0,0269 EUR/Smc,
soglia MINIMA positiva: sopra di essa
l'alternativa vince sui costi annui, sotto perde),
None se il denominatore e' nullo o negativo o se
il rapporto e' negativo. L'alternativa non usa
gas, quindi gas_alt = 0 e il denominatore e'
gas_base. Verdetto: NON_CALCOLABILE se input
degenere (produzione minore o uguale a 0, Smc per
kg minori di 0, kWh per kg minori di 0, prezzi
minori di 0, O&M minori di 0, calore cottura
minore di 0, COP cottura minore o uguale a 0,
calore essiccazione minore di 0, recupero minore
di 0 o maggiore di 1, COP essiccazione minore o
uguale a 0, superficie FV minore di 0, kwp per m2
minore di 0, resa minore di 0, f_autoconsumo
minore di 0 o maggiore di 1, voci CAPEX minori di
0, fattori CO2 minori di 0, WACC minore di 0, vita
minore o uguale a 0 o non intera, tolleranza
minore di 0) o se risparmio minore o uguale a 0
(guard degenere: UI salta KPI, grafico, tabella e
CSV); altrimenti CONVIENTE se VAN maggiore di 0,
MARGINALE se VAN negativa entro tolleranza
PERCENTUALE del CAPEX, NON_CONVIENTE altrimenti.
Casi limite: produzione zero non calcolabile
(ValueError negli helper, guard NON_CALCOLABILE in
UI); frazione autoconsumo zero (autoconsumo zero);
prezzo gas zero (risparmio negativo meno 2152,
quindi NON_CALCOLABILE: sotto la soglia di
pareggio 0,0269 l'alternativa perde sui costi
annui); FV che non supera il fabbisogno
elettrico (autoconsumo cappato alla domanda:
con FV grande l'autoconsumata e' uguale a E_alt
e il deficit e' zero); CAPEX zero (TIR non
definita, payback 0); WACC zero (VAN uguale alla
somma dei flussi).
Distinzione esplicita: qui SOLO confetti e
caramelle come prodotto finito a valle, NIENTE
estrazione industriale dello zucchero (quella e'
lo Zuccherificio, settore diverso a monte),
NIENTE altri dolci, NIENTE cioccolato, NIENTE
forni da pane o pasticceria; qui solo
confetteria: cottura + essiccazione + lucidatura
+ illuminazione + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w891_helpers import (
        demo_calcoli,
        mh887_c_alt,
        mh887_c_base,
        mh887_calcola,
        mh887_capex_totale,
        mh887_co2_alt,
        mh887_co2_base,
        mh887_co2_evitata,
        mh887_csv,
        mh887_demo,
        mh887_demo_calcoli,
        mh887_e_alt,
        mh887_e_base_totale,
        mh887_e_cottura_alt,
        mh887_e_cottura_alt_per_kg,
        mh887_e_deficit,
        mh887_e_essiccazione_alt,
        mh887_e_essiccazione_alt_per_kg,
        mh887_e_illuminazione_alt,
        mh887_e_illuminazione_base,
        mh887_e_immessa,
        mh887_e_lucidatura_alt,
        mh887_e_lucidatura_base,
        mh887_e_pv,
        mh887_e_pv_auto,
        mh887_flussi,
        mh887_frazione,
        mh887_gas_base_totale,
        mh887_gas_cottura_base,
        mh887_gas_essiccazione_base,
        mh887_int_pos,
        mh887_kwp,
        mh887_lco,
        mh887_nneg,
        mh887_num,
        mh887_p_gas_pareggio,
        mh887_payback,
        mh887_pos,
        mh887_ricavo_immissione,
        mh887_risparmio,
        mh887_sensibilita,
        mh887_tir,
        mh887_valida,
        mh887_van,
        mh887_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w891_helpers", os.path.join(_hf, "w891_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh887_c_alt = _mod.mh887_c_alt
    mh887_c_base = _mod.mh887_c_base
    mh887_calcola = _mod.mh887_calcola
    mh887_capex_totale = _mod.mh887_capex_totale
    mh887_co2_alt = _mod.mh887_co2_alt
    mh887_co2_base = _mod.mh887_co2_base
    mh887_co2_evitata = _mod.mh887_co2_evitata
    mh887_csv = _mod.mh887_csv
    mh887_demo = _mod.mh887_demo
    mh887_demo_calcoli = _mod.mh887_demo_calcoli
    mh887_e_alt = _mod.mh887_e_alt
    mh887_e_base_totale = _mod.mh887_e_base_totale
    mh887_e_cottura_alt = _mod.mh887_e_cottura_alt
    mh887_e_cottura_alt_per_kg = _mod.mh887_e_cottura_alt_per_kg
    mh887_e_deficit = _mod.mh887_e_deficit
    mh887_e_essiccazione_alt = _mod.mh887_e_essiccazione_alt
    mh887_e_essiccazione_alt_per_kg = _mod.mh887_e_essiccazione_alt_per_kg
    mh887_e_illuminazione_alt = _mod.mh887_e_illuminazione_alt
    mh887_e_illuminazione_base = _mod.mh887_e_illuminazione_base
    mh887_e_immessa = _mod.mh887_e_immessa
    mh887_e_lucidatura_alt = _mod.mh887_e_lucidatura_alt
    mh887_e_lucidatura_base = _mod.mh887_e_lucidatura_base
    mh887_e_pv = _mod.mh887_e_pv
    mh887_e_pv_auto = _mod.mh887_e_pv_auto
    mh887_flussi = _mod.mh887_flussi
    mh887_frazione = _mod.mh887_frazione
    mh887_gas_base_totale = _mod.mh887_gas_base_totale
    mh887_gas_cottura_base = _mod.mh887_gas_cottura_base
    mh887_gas_essiccazione_base = _mod.mh887_gas_essiccazione_base
    mh887_int_pos = _mod.mh887_int_pos
    mh887_kwp = _mod.mh887_kwp
    mh887_lco = _mod.mh887_lco
    mh887_nneg = _mod.mh887_nneg
    mh887_num = _mod.mh887_num
    mh887_p_gas_pareggio = _mod.mh887_p_gas_pareggio
    mh887_payback = _mod.mh887_payback
    mh887_pos = _mod.mh887_pos
    mh887_ricavo_immissione = _mod.mh887_ricavo_immissione
    mh887_risparmio = _mod.mh887_risparmio
    mh887_sensibilita = _mod.mh887_sensibilita
    mh887_tir = _mod.mh887_tir
    mh887_valida = _mod.mh887_valida
    mh887_van = _mod.mh887_van
    mh887_verdetto = _mod.mh887_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w891_helpers.py")
_UI_PATH = _risolvi("w891_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "6"
_VECCHIO_TAB = "tab88" + "6"
_VECCHIO_ST = "st88" + "6_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "gas_cottura_base_smc_anno": 48000.0,
    "gas_essiccazione_base_smc_anno": 32000.0,
    "gas_base_smc_anno": 80000.0,
    "e_lucidatura_base_kwh_anno": 140000.0,
    "e_illuminazione_base_kwh_anno": 40000.0,
    "e_base_kwh_anno": 180000.0,
    "c_base_eur_anno": 156600.0,
    "e_cottura_alt_per_kg": 0.4,
    "e_essiccazione_alt_per_kg": 0.252,
    "e_cottura_alt_kwh_anno": 160000.0,
    "e_essiccazione_alt_kwh_anno": 100800.0,
    "e_lucidatura_alt_kwh_anno": 80000.0,
    "e_illuminazione_alt_kwh_anno": 12000.0,
    "e_alt_kwh_anno": 352800.0,
    "kwp": 160.0,
    "e_pv_kwh_anno": 176000.0,
    "e_pv_auto_kwh_anno": 105600.0,
    "e_immessa_kwh_anno": 70400.0,
    "e_deficit_kwh_anno": 247200.0,
    "ricavo_immissione_eur_anno": 5632.0,
    "c_alt_eur_anno": 86752.0,
    "risparmio_eur_anno": 69848.0,
    "capex_eur": 404000.0,
    "co2_base_t_anno": 201.0,
    "co2_alt_t_anno": 61.8,
    "co2_evitata_t_anno": 139.2,
    "lco_base_eur_kg": 0.3915,
    "lco_alt_eur_kg": 0.21688,
    "van": 320998.3546508379,
    "tir": 15.226044378070409,
    "payback": 6,
    "p_gas_pareggio": 0.0269,
}


def _demo_kwargs(**over):
    kw = dict(mh887_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh887_num(3, "x"), 3.0)
        self.assertEqual(mh887_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh887_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh887_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh887_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh887_pos(0, "x")
        with self.assertRaises(ValueError):
            mh887_pos(-1, "x")
        self.assertEqual(mh887_pos(3, "x"), 3.0)

    def test_int_pos(self):
        self.assertEqual(mh887_int_pos(15, "x"), 15)
        self.assertEqual(mh887_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh887_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh887_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh887_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh887_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh887_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh887_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_gas_base_e_costo_base(self):
        self.assertEqual(mh887_gas_cottura_base(400000, 0.12), 48000.0)
        self.assertEqual(mh887_gas_essiccazione_base(400000, 0.08), 32000.0)
        self.assertEqual(mh887_gas_base_totale(48000.0, 32000.0), 80000.0)
        self.assertEqual(mh887_e_lucidatura_base(400000, 0.35), 140000.0)
        self.assertEqual(mh887_e_illuminazione_base(400000, 0.10), 40000.0)
        self.assertEqual(mh887_e_base_totale(140000.0, 40000.0), 180000.0)
        self.assertEqual(mh887_c_base(180000.0, 0.22, 80000.0, 0.90,
                                       45000), 156600.0)

    def test_cottura_pdc_e_essiccazione_recupero(self):
        self.assertAlmostEqual(mh887_e_cottura_alt_per_kg(1.20, 3.0), 0.40)
        self.assertAlmostEqual(
            mh887_e_essiccazione_alt_per_kg(0.90, 0.30, 2.5), 0.252)
        # La pompa di calore converte il consumo di
        # cottura in elettricita', non lo azzera.
        self.assertGreater(mh887_e_cottura_alt_per_kg(1.20, 3.0), 0.0)
        # Il recupero calore RIDUCE il fabbisogno di
        # essiccazione, non lo azzera: 0,252 resta
        # sopra zero e sotto il caso senza recupero.
        self.assertGreater(
            mh887_e_essiccazione_alt_per_kg(0.90, 0.30, 2.5), 0.0)
        self.assertLess(
            mh887_e_essiccazione_alt_per_kg(0.90, 0.30, 2.5),
            mh887_e_essiccazione_alt_per_kg(0.90, 0.0, 2.5))
        self.assertAlmostEqual(
            mh887_e_essiccazione_alt_per_kg(0.90, 0.0, 2.5), 0.36)
        self.assertEqual(mh887_e_cottura_alt(400000, 0.40), 160000.0)
        self.assertEqual(mh887_e_essiccazione_alt(400000, 0.252), 100800.0)
        self.assertEqual(mh887_e_lucidatura_alt(400000, 0.20), 80000.0)
        self.assertEqual(mh887_e_illuminazione_alt(400000, 0.03), 12000.0)
        self.assertEqual(
            mh887_e_alt(160000.0, 100800.0, 80000.0, 12000.0), 352800.0)
        # La lucidatura efficiente RIDUCE il consumo,
        # non lo azzera: 0,20 resta sopra zero e sotto
        # la base 0,35.
        self.assertGreater(mh887_e_lucidatura_alt(400000, 0.20), 0.0)
        self.assertLess(mh887_e_lucidatura_alt(400000, 0.20),
                        mh887_e_lucidatura_base(400000, 0.35))
        # Il LED RIDUCE il consumo, non lo azzera:
        # 0,03 resta sopra zero e sotto la base 0,10.
        self.assertGreater(mh887_e_illuminazione_alt(400000, 0.03), 0.0)
        self.assertLess(mh887_e_illuminazione_alt(400000, 0.03),
                        mh887_e_illuminazione_base(400000, 0.10))

    def test_alternativa_elettrifica_piu_della_base(self):
        # Onesta' fisica: l'alternativa elettrifica
        # cottura ed essiccazione, quindi E_alt e'
        # MAGGIORE di E_base; il vantaggio sta nel
        # gas eliminato e nel FV, non in un calo
        # dell'elettricita' totale.
        bc = demo_calcoli()
        self.assertGreater(bc["e_alt_kwh_anno"], bc["e_base_kwh_anno"])
        self.assertEqual(bc["gas_base_smc_anno"], 80000.0)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh887_kwp(800, 0.20), 160.0)
        self.assertEqual(mh887_e_pv(160.0, 1100), 176000.0)
        self.assertEqual(mh887_e_pv_auto(176000.0, 0.60, 352800.0),
                         105600.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh887_e_pv_auto(176000.0, 1.0, 50000.0), 50000.0)
        self.assertEqual(mh887_e_immessa(176000.0, 105600.0), 70400.0)
        self.assertEqual(mh887_e_deficit(352800.0, 105600.0), 247200.0)
        self.assertEqual(mh887_e_deficit(352800.0, 400000.0), 0.0)

    def test_fv_non_supera_fabbisogno_elettrico(self):
        # Con FV molto grande (5000 m2, 1000 kWp,
        # produzione 1100000 kWh/anno) l'autoconsumo
        # resta cappato alla domanda alternativa:
        # autoconsumata uguale a E_alt, deficit zero.
        bc = mh887_calcola(**_demo_kwargs(sup_fv_m2=5000))
        self.assertEqual(bc["e_pv_auto_kwh_anno"],
                         bc["e_alt_kwh_anno"])
        self.assertEqual(bc["e_deficit_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 747200.0)
        self.assertLessEqual(bc["e_pv_auto_kwh_anno"],
                             bc["e_alt_kwh_anno"])
        # Proprieta' generale: l'autoconsumo non
        # supera mai la domanda, in demo e con FV
        # grande.
        for caso in (demo_calcoli(), bc):
            self.assertLessEqual(caso["e_pv_auto_kwh_anno"],
                                 caso["e_alt_kwh_anno"])

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh887_ricavo_immissione(70400.0, 0.08), 5632.0)
        self.assertAlmostEqual(
            mh887_c_alt(247200.0, 0.22, 5632.0, 38000.0),
            86752.0)
        self.assertAlmostEqual(mh887_risparmio(156600.0, 86752.0),
                               69848.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh887_capex_totale(120000, 90000, 35000, 15000,
                                            160.0, 900),
                         404000.0)
        self.assertEqual(mh887_capex_totale(120000, 90000, 35000, 15000,
                                            0.0, 900),
                         260000.0)

    def test_co2_base_e_alt(self):
        cb = mh887_co2_base(80000.0, 1.95, 180000.0, 0.25)
        self.assertAlmostEqual(cb, 201.0, places=4)
        ca = mh887_co2_alt(247200.0, 0.25)
        self.assertAlmostEqual(ca, 61.8, places=4)
        self.assertAlmostEqual(mh887_co2_evitata(cb, ca), 139.2, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh887_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh887_lco(156600.0, 400000), 0.3915)
        self.assertAlmostEqual(mh887_lco(86752.0, 400000), 0.21688)
        with self.assertRaises(ValueError):
            mh887_lco(156600.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh887_flussi(404000, 69848, 3),
                         [-404000, 69848, 69848, 69848])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh887_van([-100, 60, 60], 0), 20.0)
        bc = mh887_demo_calcoli()
        self.assertAlmostEqual(mh887_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh887_demo_calcoli()
        tir = mh887_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh887_tir([-100, -10, -10]))
        self.assertIsNone(mh887_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh887_demo_calcoli()
        self.assertEqual(mh887_payback(bc["flussi"]), 6)
        self.assertIsNone(mh887_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh887_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh887_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:6]), -54760.0, places=2)
        self.assertAlmostEqual(sum(flussi[:7]), 15088.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh887_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh887_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh887_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh887_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh887_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh887_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh887_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_positivo(self):
        bc = mh887_demo_calcoli()
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.0269, places=6)
        # Soglia MINIMA: in demo il rapporto e'
        # positivo, quindi sopra 0,0269 EUR/Smc
        # l'alternativa vince sui costi annui,
        # sotto perde.
        self.assertAlmostEqual(
            (bc["c_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], 0.0269, places=6)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore_negativo(self):
        self.assertAlmostEqual(
            mh887_p_gas_pareggio(80000.0, 0.0, 180000.0,
                                 0.22, 45000.0, 200000.0),
            1.4425, places=6)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh887_p_gas_pareggio(80000.0, 0.0, 180000.0,
                                              0.22, 45000.0, 84600.0),
                         0.0)
        self.assertIsNone(mh887_p_gas_pareggio(0.0, 0.0, 180000.0,
                                               0.22, 45000.0, 200000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh887_p_gas_pareggio(80000.0, 80000.0, 180000.0,
                                               0.22, 45000.0, 200000.0))
        # Rapporto negativo: l'alternativa vince
        # anche a gas gratuito.
        self.assertIsNone(mh887_p_gas_pareggio(80000.0, 0.0, 180000.0,
                                               0.22, 45000.0, 80000.0))

    def test_valida_demo_ok(self):
        demo = mh887_demo()
        val = mh887_valida(*[demo[k] for k in (
            "produzione_kg_anno", "gas_cottura_base_per_kg",
            "gas_essiccazione_base_per_kg",
            "e_lucidatura_base_per_kg",
            "e_illuminazione_base_per_kg",
            "p_el", "p_gas", "om_base_eur_anno",
            "calore_cottura_kwh_t_per_kg", "cop_cottura",
            "calore_essiccazione_kwh_t_per_kg",
            "f_recupero_essiccazione", "cop_essiccazione",
            "e_lucidatura_alt_per_kg",
            "e_illuminazione_alt_per_kg", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_cottura_eur",
            "capex_essiccazione_eur", "capex_lucidatura_eur",
            "capex_led_eur", "capex_fv_eur_kwp",
            "f_co2_gas_kg_smc", "f_co2_el_kg_kwh",
            "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_produzione_zero_no(self):
        kw = _demo_kwargs(produzione_kg_anno=0)
        self.assertRaises(ValueError, mh887_calcola, **kw)

    def test_valida_cop_zero_no(self):
        kw = _demo_kwargs(cop_cottura=0)
        self.assertRaises(ValueError, mh887_calcola, **kw)
        kw = _demo_kwargs(cop_essiccazione=0)
        self.assertRaises(ValueError, mh887_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh887_calcola, **kw)
        kw = _demo_kwargs(f_recupero_essiccazione=1.1)
        self.assertRaises(ValueError, mh887_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh887_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh887_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh887_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("produzione_kg_anno", -1),
                              ("gas_cottura_base_per_kg", -0.01),
                              ("p_gas", -0.01),
                              ("capex_cottura_eur", -1),
                              ("capex_led_eur", -1),
                              ("e_lucidatura_base_per_kg", -0.01),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh887_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh887_calcola(mh887_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh887_calcola(dict(mh887_demo(), capex_cottura_eur=99999),
                           capex_cottura_eur=120000)
        self.assertEqual(bc["capex_eur"], 404000.0)


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
        self.assertEqual(bc["payback"], 6)

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
        self.assertAlmostEqual(
            bc["lco_base_eur_kg"],
            bc["c_base_eur_anno"] / bc["produzione_kg_anno"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_kg"],
            bc["c_alt_eur_anno"] / bc["produzione_kg_anno"])

    def test_coerenza_p_gas_pareggio_positivo(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.0269, places=6)
        self.assertGreater((bc["c_alt_eur_anno"]
                            - bc["e_base_kwh_anno"] * bc["p_el"]
                            - bc["om_base_eur_anno"])
                           / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh887_sensibilita(**mh887_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               84248.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               470465.43, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 5)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               66891.2, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               290307.78, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 7)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               40984.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               165399.91, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 7)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 260000.0)
        self.assertAlmostEqual(s["senza_recupero"]["risparmio_eur_anno"],
                               60344.0, places=2)
        self.assertAlmostEqual(s["senza_recupero"]["van"],
                               222350.08, places=2)
        self.assertEqual(s["senza_recupero"]["payback"], 7)
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -83001.65, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 12)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               135347.74, places=2)
        self.assertEqual(s["vita_10"]["payback"], 6)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               643720.0, places=2)

    def test_marginale_con_capex_cottura_alto(self):
        # CAPEX totale 729000 (cottura a 445000):
        # VAN circa meno 4001,65, entro la tolleranza del 10%
        # (72900).
        bc = mh887_calcola(**_demo_kwargs(capex_cottura_eur=445000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -4001.65, places=2)

    def test_non_convente_con_capex_cottura_altissimo(self):
        bc = mh887_calcola(**_demo_kwargs(capex_cottura_eur=900000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -459001.65, places=2)
        self.assertIsNone(bc["payback"])

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh887_calcola(**_demo_kwargs(om_alt_eur_anno=200000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -92152.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh887_csv(bc, mh887_demo())
        for voce in ("produzione_kg_anno", "gas_base_smc_anno",
                     "e_cottura_alt_kwh_anno", "e_essiccazione_alt_per_kg",
                     "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_kg", "lco_alt_eur_kg"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -404000.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Produzione (kg/anno)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh887_c_alt(352800.0, 0.22, 0.0, 38000.0)
        con = mh887_c_alt(247200.0, 0.22, 5632.0, 38000.0)
        self.assertAlmostEqual(senza - con, 105600.0 * 0.22 + 5632.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh887_sensibilita(**mh887_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_recupero",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh887_csv(bc, mh887_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("gas_base_smc_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh887_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh887_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh887_calcola(**_demo_kwargs(sup_fv_m2=0))
        self.assertEqual(bc["capex_eur"], 260000.0)
        bc = mh887_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_produzione_zero_non_calcolabile(self):
        # Produzione zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(produzione_kg_anno=0)
        self.assertRaises(ValueError, mh887_calcola, **kw)
        self.assertFalse(mh887_valida(*[kw[k] for k in (
            "produzione_kg_anno", "gas_cottura_base_per_kg",
            "gas_essiccazione_base_per_kg",
            "e_lucidatura_base_per_kg",
            "e_illuminazione_base_per_kg",
            "p_el", "p_gas", "om_base_eur_anno",
            "calore_cottura_kwh_t_per_kg", "cop_cottura",
            "calore_essiccazione_kwh_t_per_kg",
            "f_recupero_essiccazione", "cop_essiccazione",
            "e_lucidatura_alt_per_kg",
            "e_illuminazione_alt_per_kg", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_cottura_eur",
            "capex_essiccazione_eur", "capex_lucidatura_eur",
            "capex_led_eur", "capex_fv_eur_kwp",
            "f_co2_gas_kg_smc", "f_co2_el_kg_kwh",
            "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh887_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 176000.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 352800.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               14080.0)

    def test_prezzo_gas_zero(self):
        # A gas gratuito l'alternativa perde sui costi
        # annui: il risparmio diventa negativo e il
        # verdetto e' NON_CALCOLABILE, coerente con la
        # soglia di pareggio positiva 0,0269 EUR/Smc.
        bc = mh887_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 84600.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -2152.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh887_calcola(**_demo_kwargs(capex_cottura_eur=0,
                                          capex_essiccazione_eur=0,
                                          capex_lucidatura_eur=0,
                                          capex_led_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh887_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 643720.0)
        self.assertEqual(bc["payback"], 6)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def887\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh887_demo().keys()), lette - set(mh887_demo().keys()))
        self.assertEqual(lette, set(mh887_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc887\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc887\["([^"]+)"\]', src))
        attese = set(mh887_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 886 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 887.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 896)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab887:"), 1)
        self.assertTrue(src.startswith("    # W891"))

    def test_ui_tab887_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab887:"), 1)
        self.assertIn("def mh887_demo(", src_h)
        self.assertIn("def mh887_calcola(", src_h)
        self.assertIn("tab887", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Confetteria: cottura con pompa di calore + recupero calore + essiccazione efficiente + lucidatura efficiente + LED + FV battono cottura a gas + essiccazione a gas + lucidatura tradizionale + illuminazione tradizionale?", src)
        self.assertIn("🍬 Confetteria: cottura con pompa di calore + recupero calore + essiccazione efficiente + lucidatura efficiente + LED + FV battono cottura a gas + essiccazione a gas + lucidatura tradizionale + illuminazione tradizionale?", src)
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
        chiavi = re.findall(r'key="(st887_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st887_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st887_calcola"', src)
        self.assertIn('key="st887_csv"', src)
        self.assertIn('key="st887_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg887"), src.index(".paiac("))
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
