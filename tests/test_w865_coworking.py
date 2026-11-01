"""Test nuova scheda coworking: pompa
di calore reversibile + recupero calore
ventilazione + LED + FV battono caldaia
a gas + chiller + illuminazione
tradizionale?

Business case annuo di uno spazio di
coworking, guidato dalla SUPERFICIE
(m2) e dalle ORE DI ILLUMINAZIONE
(ore/anno) di uno spazio di lavoro
condiviso aperto tutto il giorno (non
ufficio aziendale classico con
postazioni assegnate, non hotel/B&B
con camere e docce, non sala
conferenze/eventi con posti a sedere
per evento): Q_heat = sup x q_heat;
Gas_base = Q_heat / eta_caldaia;
C_gas = Gas_base x p_gas; Q_cool =
sup x q_cool; E_chiller = Q_cool /
eer; E_light_base = sup x w_base /
1000 x ore; E_vent = sup x
kwh_vent_m2; C_el_base = (chiller +
luce base + vent) x p_el; C_base =
somma; E_hp_heat = Q_heat x
(1 - f_recupero) / cop; E_hp_cool =
Q_cool / eer_hp (EER SEPARATO dal
chiller); E_led = sup x w_led / 1000
x ore; E_domanda_alt = somma; kWp =
sup x quota_fv x kwp_per_m2; E_pv =
kWp x resa; E_pv_auto = min(E_pv x
f_autoconsumo, E_domanda_alt);
E_immessa = E_pv - E_pv_auto;
E_deficit = max(0, E_domanda_alt -
E_pv_auto); C_alt = deficit x p_el -
immessa x p_immissione; risparmio =
C_base - C_alt; CAPEX = capex_pdc +
capex_recupero + sup x capex_led_m2
+ kWp x capex_fv (demo 108.000);
CO2 base = (gas x 0,20 + (chiller +
luce base + vent) x 0,25) / 1000; CO2
alt = deficit x 0,25 / 1000 (immessa
senza credito CO2); CO2 evitata =
base - alt (segno libero); flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(PERCENTUALE in ingresso, / 100 dentro);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo gas di
pareggio p_gas_star = (C_alt -
C_el_base) / Gas_base in forma
chiusa (demo None: rapporto negativo
-0,154175, vince anche a gas gratuito),
None se Gas_base nullo o se il
rapporto e' negativo. E' una SOGLIA
MINIMA sui soli costi annui (CAPEX
escluso): sopra di essa l'alternativa
vince, sotto perde.
Verdetto: NON_CALCOLABILE se input
degenere (sup <= 0 o non intera,
q_heat/q_cool < 0, eta <= 0 o > 1,
cop/eer <= 0, f_recupero/quota_fv/
f_autoconsumo < 0 o > 1, potenze/ore/
ventilazione/prezzi < 0, kwp_per_m2
< 0, resa < 0, p_immissione < 0, voci
CAPEX < 0, fattori CO2 < 0, WACC < 0,
vita <= 0 o non intera, tolleranza
< 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa
entro tolleranza PERCENTUALE del
CAPEX, NON_CONVIENTE altrimenti.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w865_helpers import (
        demo_calcoli,
        mh861_c_alt,
        mh861_c_base,
        mh861_c_el_base,
        mh861_c_gas,
        mh861_calcola,
        mh861_capex_totale,
        mh861_co2_alt,
        mh861_co2_base,
        mh861_co2_evitata,
        mh861_csv,
        mh861_demo,
        mh861_demo_calcoli,
        mh861_e_chiller,
        mh861_e_deficit,
        mh861_e_domanda_alt,
        mh861_e_hp_cool,
        mh861_e_hp_heat,
        mh861_e_immessa,
        mh861_e_led,
        mh861_e_light_base,
        mh861_e_pv,
        mh861_e_pv_auto,
        mh861_e_vent,
        mh861_flussi,
        mh861_frazione,
        mh861_gas_base,
        mh861_int_nneg,
        mh861_int_pos,
        mh861_kwp,
        mh861_nneg,
        mh861_num,
        mh861_p_gas_pareggio,
        mh861_payback,
        mh861_pos,
        mh861_q_cool,
        mh861_q_heat,
        mh861_rendimento,
        mh861_risparmio,
        mh861_sensibilita,
        mh861_tir,
        mh861_valida,
        mh861_van,
        mh861_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w865_helpers", os.path.join(_hf, "w865_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh861_c_alt = _mod.mh861_c_alt
    mh861_c_base = _mod.mh861_c_base
    mh861_c_el_base = _mod.mh861_c_el_base
    mh861_c_gas = _mod.mh861_c_gas
    mh861_calcola = _mod.mh861_calcola
    mh861_capex_totale = _mod.mh861_capex_totale
    mh861_co2_alt = _mod.mh861_co2_alt
    mh861_co2_base = _mod.mh861_co2_base
    mh861_co2_evitata = _mod.mh861_co2_evitata
    mh861_csv = _mod.mh861_csv
    mh861_demo = _mod.mh861_demo
    mh861_demo_calcoli = _mod.mh861_demo_calcoli
    mh861_e_chiller = _mod.mh861_e_chiller
    mh861_e_deficit = _mod.mh861_e_deficit
    mh861_e_domanda_alt = _mod.mh861_e_domanda_alt
    mh861_e_hp_cool = _mod.mh861_e_hp_cool
    mh861_e_hp_heat = _mod.mh861_e_hp_heat
    mh861_e_immessa = _mod.mh861_e_immessa
    mh861_e_led = _mod.mh861_e_led
    mh861_e_light_base = _mod.mh861_e_light_base
    mh861_e_pv = _mod.mh861_e_pv
    mh861_e_pv_auto = _mod.mh861_e_pv_auto
    mh861_e_vent = _mod.mh861_e_vent
    mh861_flussi = _mod.mh861_flussi
    mh861_frazione = _mod.mh861_frazione
    mh861_gas_base = _mod.mh861_gas_base
    mh861_int_nneg = _mod.mh861_int_nneg
    mh861_int_pos = _mod.mh861_int_pos
    mh861_kwp = _mod.mh861_kwp
    mh861_nneg = _mod.mh861_nneg
    mh861_num = _mod.mh861_num
    mh861_p_gas_pareggio = _mod.mh861_p_gas_pareggio
    mh861_payback = _mod.mh861_payback
    mh861_pos = _mod.mh861_pos
    mh861_q_cool = _mod.mh861_q_cool
    mh861_q_heat = _mod.mh861_q_heat
    mh861_rendimento = _mod.mh861_rendimento
    mh861_risparmio = _mod.mh861_risparmio
    mh861_sensibilita = _mod.mh861_sensibilita
    mh861_tir = _mod.mh861_tir
    mh861_valida = _mod.mh861_valida
    mh861_van = _mod.mh861_van
    mh861_verdetto = _mod.mh861_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w865_helpers.py")
_UI_PATH = _risolvi("w865_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh86" + "0"
_VECCHIO_TAB = "tab86" + "0"
_VECCHIO_ST = "st86" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "q_heat_kwh_th_anno": 60000.0,
    "gas_base_kwh_anno": 66666.66666666667,
    "c_gas_eur_anno": 6000.0,
    "q_cool_kwh_th_anno": 40000.0,
    "e_chiller_kwh_anno": 13333.333333333334,
    "e_light_base_kwh_anno": 18750.0,
    "e_vent_kwh_anno": 5000.0,
    "c_el_base_eur_anno": 10383.333333333336,
    "c_base_eur_anno": 16383.333333333336,
    "e_hp_heat_kwh_anno": 10285.714285714286,
    "e_hp_cool_kwh_anno": 10000.0,
    "e_led_kwh_anno": 7500.0,
    "e_domanda_alt_kwh_anno": 32785.71428571429,
    "kwp": 37.5,
    "e_pv_kwh_anno": 41250.0,
    "e_pv_auto_kwh_anno": 28875.0,
    "e_immessa_kwh_anno": 12375.0,
    "e_deficit_kwh_anno": 3910.7142857142935,
    "c_alt_eur_anno": 105.0,
    "risparmio_eur_anno": 16278.333333333334,
    "capex_eur": 108000.0,
    "co2_base_t_anno": 22.60416666666667,
    "co2_alt_t_anno": 0.9776785714285734,
    "co2_evitata_t_anno": 21.6264880952381,
    "van": 60963.53343151638,
    "tir": 12.495144618211436,
    "payback": 7,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh861_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh861_num(3, "x"), 3.0)
        self.assertEqual(mh861_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh861_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh861_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh861_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh861_pos(0, "x")
        with self.assertRaises(ValueError):
            mh861_pos(-1, "x")
        self.assertEqual(mh861_pos(2, "x"), 2.0)

    def test_int_pos(self):
        self.assertEqual(mh861_int_pos(15, "x"), 15)
        self.assertEqual(mh861_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh861_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh861_int_pos(15.5, "x")

    def test_int_nneg(self):
        self.assertEqual(mh861_int_nneg(0, "x"), 0)
        self.assertEqual(mh861_int_nneg(10, "x"), 10)
        with self.assertRaises(ValueError):
            mh861_int_nneg(-1, "x")
        with self.assertRaises(ValueError):
            mh861_int_nneg(2.5, "x")

    def test_frazione_intervallo(self):
        self.assertEqual(mh861_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh861_frazione(1.0, "x"), 1.0)
        with self.assertRaises(ValueError):
            mh861_frazione(-0.1, "x")
        with self.assertRaises(ValueError):
            mh861_frazione(1.1, "x")

    def test_rendimento_intervallo(self):
        self.assertEqual(mh861_rendimento(1.0, "x"), 1.0)
        self.assertEqual(mh861_rendimento(0.9, "x"), 0.9)
        with self.assertRaises(ValueError):
            mh861_rendimento(0.0, "x")
        with self.assertRaises(ValueError):
            mh861_rendimento(1.1, "x")
        with self.assertRaises(ValueError):
            mh861_rendimento(-0.5, "x")


class TestFisica(unittest.TestCase):
    def test_q_heat_e_gas(self):
        self.assertEqual(mh861_q_heat(500, 120), 60000.0)
        self.assertAlmostEqual(mh861_gas_base(60000.0, 0.90),
                               66666.66666666667)
        with self.assertRaises(ValueError):
            mh861_q_heat(0, 120)
        with self.assertRaises(ValueError):
            mh861_gas_base(60000.0, 0.0)

    def test_q_cool_chiller_luce_vent(self):
        self.assertEqual(mh861_q_cool(500, 80), 40000.0)
        self.assertAlmostEqual(mh861_e_chiller(40000.0, 3.0),
                               13333.333333333334)
        self.assertEqual(mh861_e_light_base(500, 15, 2500), 18750.0)
        self.assertEqual(mh861_e_vent(500, 10), 5000.0)
        self.assertAlmostEqual(mh861_c_el_base(13333.333333333334,
                                               18750.0, 5000.0, 0.28),
                               10383.333333333336)
        self.assertAlmostEqual(mh861_c_base(6000.0, 10383.333333333336),
                               16383.333333333336)

    def test_hp_heat_recupero_e_hp_cool_eer_separato(self):
        self.assertAlmostEqual(mh861_e_hp_heat(60000.0, 0.40, 3.5),
                               10285.714285714286)
        # EER separato: la PdC raffresca meglio del chiller.
        self.assertEqual(mh861_e_hp_cool(40000.0, 4.0), 10000.0)
        self.assertNotEqual(mh861_e_hp_cool(40000.0, 4.0),
                            mh861_e_chiller(40000.0, 3.0))
        with self.assertRaises(ValueError):
            mh861_e_hp_heat(60000.0, 0.40, 0.0)
        with self.assertRaises(ValueError):
            mh861_e_hp_cool(40000.0, 0.0)

    def test_led_e_domanda(self):
        self.assertEqual(mh861_e_led(500, 6, 2500), 7500.0)
        self.assertAlmostEqual(mh861_e_domanda_alt(10285.714285714286,
                                                   10000.0, 7500.0,
                                                   5000.0),
                               32785.71428571429)

    def test_fv_autoconsumo_cappato(self):
        self.assertEqual(mh861_kwp(500, 0.50, 0.15), 37.5)
        self.assertEqual(mh861_e_pv(37.5, 1100), 41250.0)
        self.assertAlmostEqual(mh861_e_pv_auto(41250.0, 0.70,
                                               32785.71428571429),
                               28875.0)
        # Cap alla domanda: autoconsumo non supera la domanda.
        self.assertEqual(mh861_e_pv_auto(41250.0, 1.0, 20000.0), 20000.0)
        self.assertAlmostEqual(mh861_e_immessa(41250.0, 28875.0), 12375.0)
        self.assertAlmostEqual(mh861_e_deficit(32785.71428571429, 28875.0),
                               3910.7142857142935)
        self.assertEqual(mh861_e_deficit(20000.0, 25000.0), 0.0)

    def test_c_alt_con_ricavo_immissione(self):
        self.assertAlmostEqual(mh861_c_alt(3910.7142857142935, 0.28,
                                           12375.0, 0.08), 105.0)
        self.assertAlmostEqual(
            mh861_risparmio(16383.333333333336, 105.0),
            16278.333333333334)

    def test_capex_totale_voci(self):
        self.assertEqual(mh861_capex_totale(45000, 12000, 500, 12, 37.5,
                                            1200),
                         108000.0)
        self.assertEqual(mh861_capex_totale(45000, 12000, 500, 12, 0.0,
                                            1200),
                         63000.0)

    def test_co2_con_divisione_per_mille_senza_credito_immessa(self):
        cb = mh861_co2_base(66666.66666666667, 0.20, 13333.333333333334,
                            18750.0, 5000.0, 0.25)
        self.assertAlmostEqual(cb, 22.60416666666667, places=4)
        ca = mh861_co2_alt(3910.7142857142935, 0.25)
        self.assertAlmostEqual(ca, 0.9776785714285734, places=4)
        self.assertAlmostEqual(mh861_co2_evitata(cb, ca),
                               21.6264880952381, places=4)
        # L'immessa non sottrae CO2: alt conta solo il deficit.
        self.assertEqual(mh861_co2_alt(0.0, 0.25), 0.0)


class TestFinanza(unittest.TestCase):
    def test_flussi(self):
        self.assertEqual(mh861_flussi(108000, 16278.333333333334, 3),
                         [-108000, 16278.333333333334,
                          16278.333333333334, 16278.333333333334])

    def test_van_wacc_zero_e_cinque(self):
        self.assertAlmostEqual(mh861_van([-100, 60, 60], 0), 20.0)
        bc = mh861_demo_calcoli()
        self.assertAlmostEqual(mh861_van(bc["flussi"], 5), bc["van"])

    def test_tir_demo(self):
        bc = mh861_demo_calcoli()
        tir = mh861_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh861_tir([-100, -10, -10]))
        self.assertIsNone(mh861_tir([100, 10, 10]))

    def test_payback_demo_e_none(self):
        bc = mh861_demo_calcoli()
        self.assertEqual(mh861_payback(bc["flussi"]), 7)
        self.assertIsNone(mh861_payback([-100, 10, 10]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh861_payback([-100, 100, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh861_demo_calcoli()
        flussi = bc["flussi"]
        self.assertAlmostEqual(sum(flussi[:7]), -10330.0, places=2)
        self.assertAlmostEqual(sum(flussi[:8]), 5948.33, places=2)

    def test_verdetto_convente_marginale_non(self):
        self.assertEqual(mh861_verdetto(100.0, 10.0, 1000, 10), "CONVIENTE")
        self.assertEqual(mh861_verdetto(100.0, -50.0, 1000, 10), "MARGINALE")
        self.assertEqual(mh861_verdetto(100.0, -150.0, 1000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh861_verdetto(100.0, 0.0, 1000, 10), "MARGINALE")

    def test_verdetto_risparmio_non_positivo(self):
        self.assertEqual(mh861_verdetto(0.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh861_verdetto(-5.0, 10.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh861_verdetto(None, 10.0, 1000, 10),
                         "NON_CALCOLABILE")

    def test_p_gas_pareggio_demo_none_rapporto_negativo(self):
        bc = mh861_demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        # Soglia MINIMA: in demo l'alternativa vince
        # anche a gas gratuito, quindi il rapporto e'
        # negativo e la regola restituisce None.
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["c_el_base_eur_anno"])
                        / bc["gas_base_kwh_anno"], 0.0)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_p_gas_pareggio_positivo(self):
        self.assertAlmostEqual(mh861_p_gas_pareggio(
            12000.0, 10383.333333333336, 66666.66666666667),
            0.02425, places=5)

    def test_p_gas_pareggio_gas_nullo_none(self):
        self.assertIsNone(mh861_p_gas_pareggio(105.0, 10383.33, 0.0))

    def test_p_gas_pareggio_negativo_none(self):
        self.assertIsNone(mh861_p_gas_pareggio(100.0, 10383.33,
                                              66666.66666666667))

    def test_p_gas_pareggio_caso_limite_zero(self):
        self.assertEqual(mh861_p_gas_pareggio(10383.333333333336,
                                             10383.333333333336,
                                             66666.66666666667), 0.0)

    def test_valida_demo_ok(self):
        demo = mh861_demo()
        val = mh861_valida(*[demo[k] for k in (
            "sup_m2", "q_heat_spec_kwh_m2", "q_cool_spec_kwh_m2",
            "eta_caldaia", "cop_pdc", "eer_chiller", "eer_hp",
            "f_recupero", "w_light_base", "w_led", "ore_luce",
            "kwh_vent_m2", "p_gas", "p_el", "quota_fv", "kwp_per_m2",
            "resa_fv", "f_autoconsumo", "p_immissione", "capex_pdc",
            "capex_recupero", "capex_led_m2", "capex_fv_eur_kwp",
            "f_co2_gas_kg_kwh", "f_co2_el_kg_kwh", "wacc_pct",
            "vita_anni", "tolleranza_pct")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_sup_zero_no(self):
        kw = _demo_kwargs(sup_m2=0)
        self.assertRaises(ValueError, mh861_calcola, **kw)

    def test_valida_eta_zero_e_sopra_uno_no(self):
        kw = _demo_kwargs(eta_caldaia=0.0)
        self.assertRaises(ValueError, mh861_calcola, **kw)
        kw = _demo_kwargs(eta_caldaia=1.1)
        self.assertRaises(ValueError, mh861_calcola, **kw)

    def test_valida_cop_eer_zero_no(self):
        kw = _demo_kwargs(cop_pdc=0.0)
        self.assertRaises(ValueError, mh861_calcola, **kw)
        kw = _demo_kwargs(eer_chiller=0.0)
        self.assertRaises(ValueError, mh861_calcola, **kw)
        kw = _demo_kwargs(eer_hp=0.0)
        self.assertRaises(ValueError, mh861_calcola, **kw)

    def test_valida_quote_sopra_uno_no(self):
        kw = _demo_kwargs(f_recupero=1.1)
        self.assertRaises(ValueError, mh861_calcola, **kw)
        kw = _demo_kwargs(quota_fv=1.1)
        self.assertRaises(ValueError, mh861_calcola, **kw)
        kw = _demo_kwargs(f_autoconsumo=1.1)
        self.assertRaises(ValueError, mh861_calcola, **kw)

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh861_calcola, **kw)
        kw = _demo_kwargs(vita_anni=4.5)
        self.assertRaises(ValueError, mh861_calcola, **kw)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(p_el=float("nan"))
        self.assertRaises(ValueError, mh861_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("q_heat_spec_kwh_m2", -1),
                              ("q_cool_spec_kwh_m2", -1),
                              ("w_light_base", -1),
                              ("ore_luce", -1),
                              ("p_gas", -0.01),
                              ("capex_pdc", -1),
                              ("wacc_pct", -1),
                              ("tolleranza_pct", -1)):
            with self.assertRaises(ValueError):
                mh861_calcola(**_demo_kwargs(**{campo: valore}))

    def test_calcola_accetta_dict(self):
        bc = mh861_calcola(mh861_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh861_calcola(dict(mh861_demo(), capex_pdc=999999),
                           capex_pdc=45000)
        self.assertEqual(bc["capex_eur"], 108000.0)


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
        self.assertEqual(bc["payback"], 7)

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
            bc["c_gas_eur_anno"] + bc["c_el_base_eur_anno"])
        self.assertAlmostEqual(
            bc["c_alt_eur_anno"],
            bc["e_deficit_kwh_anno"] * bc["p_el"]
            - bc["e_immessa_kwh_anno"] * bc["p_immissione"])

    def test_coerenza_p_gas_pareggio_negativo(self):
        bc = demo_calcoli()
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertLess((bc["c_alt_eur_anno"]
                         - bc["c_el_base_eur_anno"])
                        / bc["gas_base_kwh_anno"], 0.0)

    def test_sensibilita_valori(self):
        s = mh861_sensibilita(**mh861_demo())
        self.assertAlmostEqual(s["p_gas_meno20"]["risparmio_eur_anno"],
                               15078.33, places=2)
        self.assertAlmostEqual(s["p_gas_meno20"]["van"],
                               48507.94, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["risparmio_eur_anno"],
                               18136.0, places=2)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               80245.48, places=2)
        self.assertAlmostEqual(s["senza_fv"]["risparmio_eur_anno"],
                               7203.33, places=2)
        self.assertAlmostEqual(s["senza_fv"]["van"],
                               11768.14, places=2)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["cop_2_5"]["risparmio_eur_anno"],
                               15126.33, places=2)
        self.assertAlmostEqual(s["cop_2_5"]["van"],
                               49006.17, places=2)
        self.assertEqual(s["cop_2_5"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["capex_doppio"]["van"],
                               -47036.47, places=2)
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["payback"], 14)
        self.assertAlmostEqual(s["vita_10"]["van"],
                               17696.98, places=2)
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["wacc_0"]["van"],
                               136175.0, places=2)

    def test_marginale_con_capex_pdc_alto(self):
        # CAPEX totale 183.000 (pompa di calore 120.000):
        # VAN circa -14.036, entro la tolleranza del 10%
        # (18.300).
        bc = mh861_calcola(**_demo_kwargs(capex_pdc=120000))
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van"], -14036.47, places=2)

    def test_non_convente_con_capex_pdc_altissimo(self):
        bc = mh861_calcola(**_demo_kwargs(capex_pdc=200000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(bc["van"], -94036.47, places=2)

    def test_risparmio_non_positivo_restituisce_non_calcolabile(self):
        bc = mh861_calcola(**_demo_kwargs(p_gas=0.0, quota_fv=0,
                                          w_led=15, cop_pdc=1.0))
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertLessEqual(bc["risparmio_eur_anno"], 0.0)

    def test_q_heat_zero_pareggio_none(self):
        # Senza riscaldamento il gas e' nullo e il pareggio
        # e' None; il caso resta calcolabile perche'
        # il FV rende il costo alternativo negativo
        # (ricavo immissione sopra il deficit nullo).
        bc = mh861_calcola(**_demo_kwargs(q_heat_spec_kwh_m2=0))
        self.assertEqual(bc["gas_base_kwh_anno"], 0.0)
        self.assertIsNone(bc["p_gas_pareggio"])
        self.assertAlmostEqual(bc["c_base_eur_anno"], 10383.33, places=2)
        self.assertLess(bc["c_alt_eur_anno"], 0.0)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh861_csv(bc, mh861_demo())
        for voce in ("sup_m2", "q_heat_kwh_th_anno",
                     "gas_base_kwh_anno", "p_gas_pareggio",
                     "risparmio_eur_anno", "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_flussi_e_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 16)
        self.assertEqual(bc["df_flussi"]["Anno"].iloc[0], 0)
        self.assertEqual(bc["df_flussi"]["Flusso (EUR/anno)"].iloc[0],
                         -108000.0)
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie (m2)", voci)
        self.assertIn("Potenza FV (kWp)", voci)

    def test_q_heat_scala_lineare_con_superficie(self):
        self.assertAlmostEqual(mh861_q_heat(1000, 120.0),
                               2.0 * mh861_q_heat(500, 120.0))

    def test_c_alt_senza_fv_piu_cara(self):
        senza = mh861_c_alt(32785.71428571429, 0.28, 0.0, 0.08)
        con = mh861_c_alt(3910.7142857142935, 0.28, 12375.0, 0.08)
        self.assertAlmostEqual(senza - con, 28875.0 * 0.28 + 12375.0 * 0.08)

    def test_sensibilita_chiavi_complete(self):
        s = mh861_sensibilita(**mh861_demo())
        self.assertEqual(set(s.keys()),
                         {"p_gas_meno20", "p_el_piu20", "senza_fv",
                          "cop_2_5", "capex_doppio", "vita_10",
                          "wacc_0"})
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh861_csv(bc, mh861_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("q_heat_kwh_th_anno;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh861_demo_calcoli()["risparmio_eur_anno"],
                         demo_calcoli()["risparmio_eur_anno"])
        self.assertEqual(mh861_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh861_calcola(**_demo_kwargs(quota_fv=0))
        self.assertEqual(bc["capex_eur"], 63000.0)
        bc = mh861_calcola(**_demo_kwargs(f_autoconsumo=0))
        self.assertEqual(bc["e_pv_auto_kwh_anno"], 0.0)


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def861\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh861_demo().keys()), lette - set(mh861_demo().keys()))
        self.assertEqual(lette, set(mh861_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc861\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc861\["([^"]+)"\]', src))
        attese = set(mh861_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab861:"), 1)
        self.assertTrue(src.startswith("    # W865"))

    def test_ui_tab861_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab861:"), 1)
        self.assertIn("def mh861_demo(", src_h)
        self.assertIn("def mh861_calcola(", src_h)
        self.assertIn("tab861", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Coworking: pompa di calore reversibile + recupero calore ventilazione + LED + FV battono caldaia a gas + chiller + illuminazione tradizionale?", src)
        self.assertIn("🏢 Coworking: pompa di calore reversibile + recupero calore ventilazione + LED + FV battono caldaia a gas + chiller + illuminazione tradizionale?", src)
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
        chiavi = re.findall(r'key="(st861_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st861_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st861_calcola"', src)
        self.assertIn('key="st861_csv"', src)
        self.assertIn('key="st861_csv_flussi"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg861"), src.index(".paiac("))
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
