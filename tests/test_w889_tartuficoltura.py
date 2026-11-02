"""Test nuova scheda tartuficoltura:
irrigazione a goccia + celle frigo efficienti +
riscaldamento da pompa di calore + FV battono
irrigazione tradizionale + celle tradizionali +
riscaldamento a gas?
Repo path: tests/test_w889_tartuficoltura.py

Business case annuo di una tartuficoltura,
guidato dagli ETTARI DI TARTUFAIA
(demo 2 ha):
irrigazione tradizionale base 2 x 2500 =
5000 kWh/anno; celle frigo tradizionali
2 x 3500 = 7000 kWh/anno; elettricita' base
totale 12000 kWh/anno, costo energia base 2640
EUR/anno; gas base 2 x 800 = 1600 Smc/anno,
costo gas base 1440 EUR/anno; O&M base 6000
EUR/anno; costo base 10080 EUR/anno;
irrigazione a goccia 2 x 1200 = 2400
kWh/anno; celle frigo efficienti 2 x 1800 = 3600
kWh/anno; pompa di calore riscaldamento 2 x 1500
= 3000 kWh/anno; elettricita'
alternativa 9000 kWh/anno, gas per riscaldamento
ELIMINATO; kWp = sup FV x kwp per m2
(demo 16 kWp); E_pv 17600 kWh/anno;
E_pv_auto = min(E_pv x f_autoconsumo, E_alt)
(demo 8800 kWh/anno); immessa 8800 kWh/anno;
deficit 200 kWh/anno; ricavo immissione 704
EUR/anno; O&M alternativa 4500 EUR/anno; C_alt
3840 EUR/anno; risparmio 6240 EUR/anno; CAPEX
4000 + 8000 + 9000 + 16 x 900 = 35400 EUR; CO2
base = (gas x 1,95 + E_base x 0,25) / 1000 = 6,12
t/anno; CO2 alt = (deficit x 0,25) / 1000 = 0,05
t/anno (immessa senza credito CO2); CO2 evitata
6,07 t/anno; LCO base 5040 EUR/ha e LCO alt
1920 EUR/ha (costi operativi annui per
ha, CAPEX escluso); flussi [CAPEX
negativo, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro); TIR per
bisezione; payback (primo anno con cumulato
maggiore o uguale a 0);
prezzo gas di pareggio p_gas_star = (C_alt meno
E_base x p_el meno om_base) / (gas_base meno gas_alt)
in forma chiusa (demo None: rapporto negativo meno
3,0, vince anche a gas gratuito), None se il
denominatore e' nullo o negativo o se il rapporto e'
negativo. L'alternativa non usa gas, quindi gas_alt
= 0 e il denominatore e' gas_base.
E' una SOGLIA MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa vince, sotto
perde. Verdetto: NON_CALCOLABILE se input degenere
(ettari minori o uguali a 0, kWh per ha minori
di 0, prezzi minori di 0, O&M minori di 0,
superficie FV minore di 0, kwp per m2 minore di 0,
resa minore di 0, f_autoconsumo minore di 0 o
maggiore di 1, voci CAPEX minori di 0,
fattori CO2 minori di 0, WACC minore di 0, vita
minore o uguale a 0 o non intera,
tolleranza minore di 0) o se risparmio minore o
uguale a 0 (guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN
maggiore di 0, MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: ettari zero non calcolabile
(ValueError negli helper, guard NON_CALCOLABILE in
UI); frazione autoconsumo zero (autoconsumo zero);
prezzo gas zero (ancora calcolabile, risparmio
positivo, VAN positiva: CONVIENTE);
CAPEX zero (TIR non definita, payback 0); WACC
zero (VAN uguale alla somma dei flussi).
Distinzione esplicita: NON fungaia (li'
si coltivano funghi con substrato e
pastorizzazione, qui SOLO tartufi:
irrigazione + celle frigo + riscaldamento + FV,
NIENTE funghi, NIENTE substrato, NIENTE
pastorizzazione, NIENTE fungaia), NON vigneto
(li' viti da uva, qui SOLO tartufi, NIENTE
uva, NIENTE vigneto, NIENTE antibrina per viti),
NON frutteto (li' frutta da albero, qui SOLO
tartufi, NIENTE frutta, NIENTE frutteto, NIENTE
antibrina per frutta), NON sericoltura (li'
si allevano bachi da seta, qui SOLO tartufi,
NIENTE bachi, NIENTE sericoltura), NON acquacoltura
(li' si allevano pesci, qui SOLO tartufi, NIENTE
pesci, NIENTE acquacoltura), NON elicicoltura
(li' si allevano lumache, qui SOLO tartufi,
NIENTE lumache, NIENTE elicicoltura), NON porcilaia
(li' si allevano suini, qui SOLO tartufi,
NIENTE suini, NIENTE porcilaia), NON pollaio
avicolo (li' si allevano avicoli, qui SOLO tartufi,
NIENTE avicoli, NIENTE pollaio), NON stalla
bovina (li' si allevano bovini, qui SOLO tartufi,
NIENTE bovini, NIENTE stalla bovina), NON sala
mungitura (li' si munge, qui SOLO tartufi,
NIENTE latte, NIENTE mungitura, NIENTE
refrigerazione latte), NON caseificio (li' si
trasforma il latte in formaggio, qui SOLO tartufi,
NIENTE latte, NIENTE caseificio), NON vigneto
(vedi sopra), NON frutteto (vedi sopra), NON
allevamento ovino (li' ovini e tosatura, qui SOLO
tartufi, NIENTE ovini, NIENTE tosatura), NON
coniglicoltura (li' conigli, qui SOLO tartufi,
NIENTE conigli, NIENTE coniglicoltura), NON
vivaio floricolo (li' fiori in vivaio, qui SOLO
tartufi, NIENTE vivaio floricolo), NON fioraio
(li' vendita di fiori, qui SOLO tartufi,
NIENTE fioraio), NON maneggio (li' cavalli, qui
SOLO tartufi, NIENTE cavalli, NIENTE maneggio); qui
solo tartuficoltura: irrigazione + celle frigo +
riscaldamento + FV.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w889_helpers import (
        demo_calcoli,
        mh885_c_alt,
        mh885_c_base,
        mh885_calcola,
        mh885_capex_totale,
        mh885_co2_alt,
        mh885_co2_base,
        mh885_co2_evitata,
        mh885_csv,
        mh885_demo,
        mh885_demo_calcoli,
        mh885_e_alt,
        mh885_e_base_totale,
        mh885_e_deficit,
        mh885_e_irrigazione_alt,
        mh885_e_irrigazione_base,
        mh885_e_immessa,
        mh885_e_pdc,
        mh885_e_pv,
        mh885_e_pv_auto,
        mh885_e_celle_alt,
        mh885_e_celle_base,
        mh885_flussi,
        mh885_frazione,
        mh885_gas_base,
        mh885_int_pos,
        mh885_kwp,
        mh885_lco,
        mh885_nneg,
        mh885_num,
        mh885_p_gas_pareggio,
        mh885_payback,
        mh885_pos,
        mh885_ricavo_immissione,
        mh885_risparmio,
        mh885_sensibilita,
        mh885_tir,
        mh885_valida,
        mh885_van,
        mh885_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w889_helpers", os.path.join(_hf, "w889_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh885_c_alt = _mod.mh885_c_alt
    mh885_c_base = _mod.mh885_c_base
    mh885_calcola = _mod.mh885_calcola
    mh885_capex_totale = _mod.mh885_capex_totale
    mh885_co2_alt = _mod.mh885_co2_alt
    mh885_co2_base = _mod.mh885_co2_base
    mh885_co2_evitata = _mod.mh885_co2_evitata
    mh885_csv = _mod.mh885_csv
    mh885_demo = _mod.mh885_demo
    mh885_demo_calcoli = _mod.mh885_demo_calcoli
    mh885_e_alt = _mod.mh885_e_alt
    mh885_e_base_totale = _mod.mh885_e_base_totale
    mh885_e_deficit = _mod.mh885_e_deficit
    mh885_e_irrigazione_alt = _mod.mh885_e_irrigazione_alt
    mh885_e_irrigazione_base = _mod.mh885_e_irrigazione_base
    mh885_e_immessa = _mod.mh885_e_immessa
    mh885_e_pdc = _mod.mh885_e_pdc
    mh885_e_pv = _mod.mh885_e_pv
    mh885_e_pv_auto = _mod.mh885_e_pv_auto
    mh885_e_celle_alt = _mod.mh885_e_celle_alt
    mh885_e_celle_base = _mod.mh885_e_celle_base
    mh885_flussi = _mod.mh885_flussi
    mh885_frazione = _mod.mh885_frazione
    mh885_gas_base = _mod.mh885_gas_base
    mh885_int_pos = _mod.mh885_int_pos
    mh885_kwp = _mod.mh885_kwp
    mh885_lco = _mod.mh885_lco
    mh885_nneg = _mod.mh885_nneg
    mh885_num = _mod.mh885_num
    mh885_p_gas_pareggio = _mod.mh885_p_gas_pareggio
    mh885_payback = _mod.mh885_payback
    mh885_pos = _mod.mh885_pos
    mh885_ricavo_immissione = _mod.mh885_ricavo_immissione
    mh885_risparmio = _mod.mh885_risparmio
    mh885_sensibilita = _mod.mh885_sensibilita
    mh885_tir = _mod.mh885_tir
    mh885_valida = _mod.mh885_valida
    mh885_van = _mod.mh885_van
    mh885_verdetto = _mod.mh885_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w889_helpers.py")
_UI_PATH = _risolvi("w889_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh88" + "4"
_VECCHIO_TAB = "tab88" + "4"
_VECCHIO_ST = "st88" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO = {
    "e_irrigazione_base_kwh_anno": 5000.0,
    "e_celle_base_kwh_anno": 7000.0,
    "e_base_kwh_anno": 12000.0,
    "gas_base_smc_anno": 1600.0,
    "c_base_eur_anno": 10080.0,
    "e_irrigazione_alt_kwh_anno": 2400.0,
    "e_celle_alt_kwh_anno": 3600.0,
    "e_pdc_kwh_anno": 3000.0,
    "e_alt_kwh_anno": 9000.0,
    "kwp": 16.0,
    "e_pv_kwh_anno": 17600.0,
    "e_pv_auto_kwh_anno": 8800.0,
    "e_immessa_kwh_anno": 8800.0,
    "e_deficit_kwh_anno": 200.0,
    "ricavo_immissione_eur_anno": 704.0,
    "c_alt_eur_anno": 3840.0,
    "risparmio_eur_anno": 6240.0,
    "capex_eur": 35400.0,
    "co2_base_t_anno": 6.12,
    "co2_alt_t_anno": 0.05,
    "co2_evitata_t_anno": 6.07,
    "lco_base_eur_ha": 5040.0,
    "lco_alt_eur_ha": 1920.0,
    "van": 29369.066158246882,
    "tir": 15.631739410941863,
    "payback": 6,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh885_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh885_num(3, "x"), 3.0)
        self.assertEqual(mh885_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh885_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh885_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh885_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh885_pos(0, "x")
        with self.assertRaises(ValueError):
            mh885_pos(-1, "x")
        self.assertEqual(mh885_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh885_int_pos(15, "x"), 15)
        self.assertEqual(mh885_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh885_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh885_int_pos(15.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh885_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh885_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh885_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh885_frazione(1.1, "x")


class TestFisica(unittest.TestCase):
    def test_irrigazione_celle_base_e_costo_base(self):
        self.assertEqual(mh885_e_irrigazione_base(2, 2500), 5000.0)
        self.assertEqual(mh885_e_celle_base(2, 3500), 7000.0)
        self.assertEqual(mh885_e_base_totale(5000.0, 7000.0), 12000.0)
        self.assertEqual(mh885_gas_base(2, 800), 1600.0)
        self.assertEqual(mh885_c_base(12000.0, 0.22, 1600.0, 0.90,
                                       6000), 10080.0)

    def test_irrigazione_celle_pdc_somma(self):
        self.assertEqual(mh885_e_irrigazione_alt(2, 1200), 2400.0)
        self.assertEqual(mh885_e_celle_alt(2, 1800), 3600.0)
        self.assertEqual(mh885_e_pdc(2, 1500), 3000.0)
        self.assertEqual(mh885_e_alt(2400.0, 3600.0, 3000.0), 9000.0)
        # L'irrigazione a goccia RIDUCE il consumo di
        # irrigazione, non lo azzera: 1200 resta sopra zero
        # anche a parita' di base 2500.
        self.assertGreater(mh885_e_irrigazione_alt(2, 1200), 0.0)
        self.assertLess(mh885_e_irrigazione_alt(2, 1200),
                        mh885_e_irrigazione_base(2, 2500))
        # Le celle frigo efficienti RIDUCONO il consumo di
        # celle frigo, non lo azzerano: 1800 resta sopra zero
        # anche a parita' di base 3500.
        self.assertGreater(mh885_e_celle_alt(2, 1800), 0.0)
        self.assertLess(mh885_e_celle_alt(2, 1800),
                        mh885_e_celle_base(2, 3500))

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh885_kwp(80, 0.20), 16.0)
        self.assertEqual(mh885_e_pv(16.0, 1100), 17600.0)
        self.assertEqual(mh885_e_pv_auto(17600.0, 0.50, 9000.0),
                         8800.0)
        # Cap min(): anche con autoconsumo 1,0 la
        # domanda piccola limita l'autoconsumo.
        self.assertEqual(mh885_e_pv_auto(17600.0, 1.0, 5000.0), 5000.0)
        self.assertEqual(mh885_e_immessa(17600.0, 8800.0), 8800.0)
        self.assertEqual(mh885_e_deficit(9000.0, 8800.0), 200.0)
        self.assertEqual(mh885_e_deficit(9000.0, 15000.0), 0.0)

    def test_ricavo_immissione_e_c_alt(self):
        self.assertEqual(mh885_ricavo_immissione(8800.0, 0.08), 704.0)
        self.assertAlmostEqual(
            mh885_c_alt(200.0, 0.22, 704.0, 4500.0),
            3840.0)
        self.assertAlmostEqual(mh885_risparmio(10080.0, 3840.0),
                               6240.0)

    def test_capex_totale_voci(self):
        self.assertEqual(mh885_capex_totale(4000, 8000, 9000, 16.0,
                                            900),
                         35400.0)
        self.assertEqual(mh885_capex_totale(4000, 8000, 9000, 0.0,
                                            900),
                         21000.0)

    def test_co2_base_e_alt(self):
        cb = mh885_co2_base(1600.0, 1.95, 12000.0, 0.25)
        self.assertAlmostEqual(cb, 6.12, places=4)
        ca = mh885_co2_alt(200.0, 0.25)
        self.assertAlmostEqual(ca, 0.05, places=4)
        self.assertAlmostEqual(mh885_co2_evitata(cb, ca), 6.07, places=4)
        # L'immessa non sottrae CO2: alt conta solo
        # il deficit.
        self.assertEqual(mh885_co2_alt(0.0, 0.25), 0.0)

    def test_lco_base_e_alt(self):
        self.assertEqual(mh885_lco(10080.0, 2), 5040.0)
        self.assertAlmostEqual(mh885_lco(3840.0, 2), 1920.0)
        with self.assertRaises(ValueError):
            mh885_lco(10080.0, 0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh885_flussi(35400, 6240.0, 3),
                         [-35400, 6240.0, 6240.0, 6240.0])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh885_van([-100, 60, 60], 0), 20.0)
        bc = mh885_demo_calcoli()
        self.assertAlmostEqual(mh885_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh885_demo_calcoli()
        tir = mh885_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh885_tir([-100, -10, -10]))
        self.assertIsNone(mh885_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh885_demo_calcoli()
        self.assertEqual(mh885_payback(bc["flussi"]), 6)
        self.assertIsNone(mh885_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh885_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh885_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:6]), -4200.0, places=2)
        self.assertAlmostEqual(sum(flussi[:7]), 2040.0, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh885_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh885_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh885_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh885_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh885_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh885_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh885_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh885_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)
        self.assertAlmostEqual(
            (bc["c_alt_eur_anno"]
             - bc["e_base_kwh_anno"] * bc["p_el"]
             - bc["om_base_eur_anno"])
            / bc["gas_base_smc_anno"], -3.0, places=8)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo_zero_denominatore(self):
        self.assertAlmostEqual(
            mh885_p_gas_pareggio(1600.0, 0.0, 12000.0,
                                 0.22, 6000.0, 20000.0),
            7.1, places=10)
        # Rapporto zero: numeratore nullo.
        self.assertEqual(mh885_p_gas_pareggio(1600.0, 0.0, 12000.0,
                                              0.22, 6000.0, 8640.0),
                         0.0)
        self.assertIsNone(mh885_p_gas_pareggio(0.0, 0.0, 12000.0,
                                               0.22, 6000.0, 20000.0))
        # Denominatore nullo: gas base uguale al gas
        # alternativo.
        self.assertIsNone(mh885_p_gas_pareggio(1600.0, 1600.0, 12000.0,
                                               0.22, 6000.0, 20000.0))
        self.assertIsNone(mh885_p_gas_pareggio(1600.0, 0.0, 12000.0,
                                               0.22, 6000.0, 3840.0))

    def test_valida_demo_ok(self):
        demo = mh885_demo()
        val = mh885_valida(*[demo[k] for k in (
            "ettari_ha", "e_irrigazione_base_per_ha",
            "e_celle_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_irrigazione_alt_per_ha", "e_celle_alt_per_ha",
            "e_pdc_per_ha", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_irrigazione_eur",
            "capex_celle_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_ettari_zero_no(self):
        kw = _demo_kwargs(ettari_ha=0)
        self.assertRaises(ValueError, mh885_calcola, **kw)

    def test_valida_frazione_sopra_uno_no(self):
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh885_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh885_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh885_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_gas=float("nan"))
        self.assertRaises(ValueError, mh885_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("ettari_ha", -1),
                              ("e_irrigazione_base_per_ha", -1),
                              ("p_gas", -0.01),
                              ("capex_irrigazione_eur", -1),
                              ("capex_pdc_eur", -1),
                              ("e_celle_base_per_ha", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh885_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh885_calcola(mh885_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh885_calcola(dict(mh885_demo(), capex_irrigazione_eur=99999),
                           capex_irrigazione_eur=4000)
        self.assertEqual(bc["capex_eur"], 35400.0)


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
            bc["lco_base_eur_ha"],
            bc["c_base_eur_anno"] / bc["ettari_ha"])
        self.assertAlmostEqual(
            bc["lco_alt_eur_ha"],
            bc["c_alt_eur_anno"] / bc["ettari_ha"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["e_base_kwh_anno"] * bc["p_el"]
                         - bc["om_base_eur_anno"])
                        / bc["gas_base_smc_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh885_sensibilita(**mh885_demo())
        self.assertAlmostEqual(s["p_gas_piu20"]["risparmio_eur_anno"],
                               6528.0, places=2)
        self.assertAlmostEqual(s["p_gas_piu20"]["van"],
                               32358.41, places=2)
        self.assertEqual(s["p_gas_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               6759.2, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               34758.18, places=2)
        self.assertEqual(s["p_el_piu20"]["payback"], 6)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               3600.0, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               16366.77, places=2)
        self.assertEqual(s["senza_fv"]["payback"], 6)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_fv"]["capex_eur"], 21000.0)
        self.assertAlmostEqual(s["senza_irrigazione_goccia"]["risparmio_eur_anno"],
                               5668.0, places=2)
        self.assertAlmostEqual(s["senza_irrigazione_goccia"]["van"],
                               23431.90, places=2)
        self.assertEqual(s["senza_irrigazione_goccia"]["payback"], 7)
        self.assertEqual(s["senza_irrigazione_goccia"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -6030.93, places=2)
        self.assertEqual(s["capex_doppio"]["payback"], 12)
        self.assertEqual(s["capex_doppio"]["verdetto"], "MARGINALE")
        self.assertAlmostEqual(s["vita_10"]["van"],
                               12783.63, places=2)
        self.assertEqual(s["vita_10"]["payback"], 6)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               58200.0, places=2)

    def test_marginale_con_capex_irrigazione_alto(self):
        # CAPEX totale 67400 (irrigazione a 36000):
        # VAN circa meno 2630,93, entro la tolleranza del 10%
        # (6740).
        bc = mh885_calcola(**_demo_kwargs(capex_irrigazione_eur=36000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -2630.93, places=2)

    def test_non_convente_con_capex_irrigazione_altissimo(self):
        bc = mh885_calcola(**_demo_kwargs(capex_irrigazione_eur=64000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -30630.93, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh885_calcola(**_demo_kwargs(om_alt_eur_anno=100000))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], -89260.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh885_csv(bc, mh885_demo())
        for voce in ("ettari_ha", "e_base_kwh_anno",
                     "e_irrigazione_base_kwh_anno", "e_pdc_kwh_anno",
                     "gas_base_smc_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto",
                     "lco_base_eur_ha", "lco_alt_eur_ha"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -35400.0)
        self.assertGreater(len(bc["df_tabella"]), 40)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Ettari di tartufaia (ha)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh885_c_alt(9000.0, 0.22, 0.0, 4500.0)
        con = mh885_c_alt(200.0, 0.22, 704.0, 4500.0)
        self.assertAlmostEqual(senza - con, 8800.0 * 0.22 + 704.0)

    def test_sensibilita_chiavi_complete(self):
        s = mh885_sensibilita(**mh885_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_piu20", "p_el_piu20",
                          "senza_fv", "senza_irrigazione_goccia",
                          "capex_doppio", "vita_10", "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh885_csv(bc, mh885_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("e_base_kwh_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh885_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh885_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh885_calcola(**_demo_kwargs(sup_fv_m2=0))
        self.assertEqual(bc["capex_eur"], 21000.0)
        bc = mh885_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestCasiLimite(unittest.TestCase):
    def test_ettari_zero_non_calcolabile(self):
        # Ettari zero: non calcolabile negli helper
        # (ValueError) e guard NON_CALCOLABILE in UI.
        kw = _demo_kwargs(ettari_ha=0)
        self.assertRaises(ValueError, mh885_calcola, **kw)
        self.assertFalse(mh885_valida(*[kw[k] for k in (
            "ettari_ha", "e_irrigazione_base_per_ha",
            "e_celle_base_per_ha",
            "p_el", "gas_per_ha",
            "p_gas", "om_base_eur_anno",
            "e_irrigazione_alt_per_ha", "e_celle_alt_per_ha",
            "e_pdc_per_ha", "sup_fv_m2",
            "kwp_per_m2", "resa_fv", "f_autoconsumo",
            "p_immissione", "om_alt_eur_anno",
            "capex_irrigazione_eur",
            "capex_celle_eur", "capex_pdc_eur",
            "capex_fv_eur_kwp", "f_co2_gas_kg_smc",
            "f_co2_el_kg_kwh", "wacc_pct", "vita_anni",
            "tolleranza_pct")])["valido"])

    def test_quota_fv_zero(self):
        bc = mh885_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_anno"], 17600.0)
        self.assertEqual(bc["e_deficit_kwh_anno"], 9000.0)
        self.assertAlmostEqual(bc["ricavo_immissione_eur_anno"],
                               1408.0)

    def test_prezzo_gas_zero(self):
        bc = mh885_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(bc["c_base_eur_anno"], 8640.0)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], 4800.0)
        self.assertAlmostEqual(bc["van"], 14422.36, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_zero(self):
        bc = mh885_calcola(**_demo_kwargs(capex_irrigazione_eur=0,
                                          capex_celle_eur=0,
                                          capex_pdc_eur=0,
                                          capex_fv_eur_kwp=0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_wacc_zero(self):
        bc = mh885_calcola(**_demo_kwargs(wacc_pct=0.0))
        self.assertAlmostEqual(bc["van"], 58200.0)
        self.assertEqual(bc["payback"], 6)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def889\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh885_demo().keys()), lette - set(mh885_demo().keys()))
        self.assertEqual(lette, set(mh885_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc889\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc889\["([^"]+)"\]', src))
        attese = set(mh885_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_post_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 884 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 885)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab885:"), 1)
        self.assertTrue(src.startswith("    # W889"))

    def test_ui_tab885_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab885:"), 1)
        self.assertIn("def mh885_demo(", src_h)
        self.assertIn("def mh885_calcola(", src_h)
        self.assertIn("tab885", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Tartuficoltura: irrigazione a goccia + celle frigo efficienti + riscaldamento da pompa di calore + FV battono irrigazione tradizionale + celle tradizionali + riscaldamento a gas?", src)
        self.assertIn("🌳 Tartuficoltura: irrigazione a goccia + celle frigo efficienti + riscaldamento da pompa di calore + FV battono irrigazione tradizionale + celle tradizionali + riscaldamento a gas?", src)
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
        chiavi = re.findall(r'key="(st889_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st889_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st889_calcola"', src)
        self.assertIn('key="st889_csv"', src)
        self.assertIn('key="st889_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg889"), src.index(".paiac("))
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
