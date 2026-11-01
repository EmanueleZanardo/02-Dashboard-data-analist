"""Test nuova scheda tab846 "Campus universitario:
fotovoltaico + batteria + pompa di calore
+ LED + recupero calore laboratori battono
caldaia a gas + rete + illuminazione
tradizionale?".

Business case annuo di un campus
universitario, connesso alla rete, guidato
da STUDENTI equivalenti a tempo pieno +
SUPERFICIE (aule + laboratori):
E_el_base = studenti x kwh_e_per_studente;
illuminazione = E_el_base x
share_illuminazione; resto = E_el_base x
(1 - share_illuminazione); illum_alt =
illuminazione x (1 - risparmio_led);
E_alt_el = illum_alt + resto;
Q_base = superficie_m2 x kwh_th_per_m2;
Q_alt = Q_base x (1 - recupero_lab);
E_pdc = Q_alt / COP (la PdC sostituisce
integralmente la caldaia a gas:
gas_alt = 0); E_alt = E_alt_el + E_pdc;
E_fv = kWp x producibilita';
autoconsumo = min(E_alt, E_fv x
f_autoconsumo) (le perdite round-trip
della batteria sono incorporate nel
fattore efficace f_autoconsumo,
nessun'altra perdita nascosta);
deficit = E_alt - autoconsumo (prelevato
da rete a prezzo di prelievo); immessa =
E_fv - autoconsumo (tutta la produzione
eccedente va immessa come ricavo allo
stesso prezzo di immissione; la rete
ESISTE); C_base = E_el_base x
p_prelievo + Q_base x p_gas; C_alt =
deficit x p_prelievo - immessa x
p_immissione + opex_alt (l'immissione
e' un ricavo, segno meno; gas_alt = 0);
risparmio = C_base - C_alt;
CAPEX = capex_fv x kWp + capex_batteria
x kwh_batteria + capex_pdc + capex_led
+ capex_recupero (tutti forfettari
tranne FV e batteria, dichiarato);
CO2 base = E_el_base x f_el / 1000 +
Q_base x f_gas / 1000; CO2 alt =
deficit x f_el / 1000 (gas zero,
dichiarato); CO2 evitata = base - alt
(segno libero, non clampata);
flussi [-CAPEX, risparmio x vita];
VAN al tasso (FRAZIONE, non percentuale);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo di prelievo
di pareggio p_star = (opex_alt - immessa
x p_immissione - Q_base x p_gas) /
(E_el_base - deficit) in forma chiusa a
prezzo di gas, prezzo di immissione e
OPEX FERMI, None se E_el_base - deficit
<= 0 o se p_star < 0, SOGLIA sui soli
costi annui quando esiste (sopra di
essa l'alternativa vince, sotto perde;
il CAPEX non entra nel pareggio annuo).
Nel demo p_star e' None, documentato:
il risparmio gas da solo (432.000
EUR/anno) supera gia' opex_alt - ricavo
immissione (40.000 - 39.600 = 400
EUR/anno), quindi l'alternativa vince
sui costi annui anche a prezzo di
prelievo nullo. Un caso costruito con
pareggio positivo (superficie 0 e FV 0:
niente gas, niente immessa) ha p_star
0,027777777777777776 EUR/kWh: a p_star
il risparmio e' zero e il verdetto e'
NON_CALCOLABILE, a p_star + 0,01 il
risparmio e' 14.400,00 EUR/anno, a
p_star - 0,01 e' -14.400,00 EUR/anno.
Verdetto: NON_CALCOLABILE se input
degenere (studenti <= 0,
kwh_e_per_studente < 0,
share_illuminazione < 0 o > 1,
risparmio_led < 0 o > 1,
superficie_m2 < 0, kwh_th_per_m2 < 0,
recupero_lab < 0 o > 1, COP <= 0,
kWp < 0, producibilita' < 0,
f_autoconsumo < 0 o > 1,
kwh_batteria < 0, prezzi < 0,
opex_alt < 0, capex voci < 0,
f_el < 0, f_gas < 0, tasso < 0,
vita <= 0 o non intera, tolleranza < 0)
o se risparmio <= 0 (guard degenere:
UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro
tolleranza FRAZIONE del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Guard UI IDENTICA agli
helper: nessuna divergenza di verdetto.
Tutti gli slider UI hanno minimo 0,
quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0
raggiungibili via slider sono bloccati in
UI esattamente come negli helper dove
previsto (studenti, vita, COP).
Gli zeri ammessi in entrambi (kWh per
studente, quote, frazioni, superficie,
kWh termici per m2, potenza
fotovoltaico, producibilita', kWh
batteria, prezzi, OPEX, voci CAPEX,
fattori CO2, tasso, tolleranza) non
creano divergenza. Quote e frazioni > 1
sono degeneri in entrambi ma non
raggiungibili via slider (tetto 1,0).
Tasso sopra 0,20 e tolleranza sopra 1,0
sono ammessi negli helper e limitati
solo dagli slider UI (0,20 e 1,0):
nessuna divergenza nel range
raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper.

Demo (campus universitario): 8.000
studenti, 1.200 kWh_e/studente
(E_el_base 9.600.000), share
illuminazione 0,30 (illuminazione
2.880.000, resto 6.720.000), risparmio
LED 0,50 (illum_alt 1.440.000, E_alt_el
8.160.000), superficie 60.000 m2,
80 kWh_th/m2 (Q_base 4.800.000),
recupero laboratori 0,15 (Q_alt
4.080.000), COP 3,5 (E_pdc
1.165.714,29, E_alt 9.325.714,29),
fotovoltaico 1.500 kWp a 1.100
kWh/kWp/anno (1.650.000),
f_autoconsumo 0,70 (autoconsumo
1.155.000, deficit 8.170.714,29,
immessa 495.000), batteria 500 kWh,
prezzo prelievo 0,22, prezzo gas 0,09,
prezzo immissione 0,08 EUR/kWh, OPEX
40.000 EUR/anno, CAPEX voci: FV 900
EUR/kWp (1.350.000), batteria 500
EUR/kWh (250.000), PdC 400.000, LED
150.000, recupero 200.000 (totale
2.350.000), f_el 0,35 kg/kWh_e, f_gas
0,20 kg/kWh_th, tasso 0,06 (frazione),
vita 20 anni, tolleranza 0,05
(frazione del CAPEX).
Valori calcolati eseguendo
mh846_demo_calcoli(): E_el_base
9600000,0, illuminazione 2880000,0,
resto 6720000,0, illum_alt 1440000,0,
E_alt_el 8160000,0, Q_base 4800000,0,
Q_alt 4080000,0, E_pdc
1165714,2857142857, E_alt
9325714,285714285, E_fv 1650000,0,
autoconsumo 1155000,0, deficit
8170714,285714285, immessa 495000,0,
C_base 2544000,0, C_alt
1797957,1428571427, risparmio
746042,8571428573, CAPEX tot
2350000,0, CO2 base 4320,0, CO2 alt
2859,7499999999995, CO2 evitata
1460,2500000000005, VAN
6207052,797101904, TIR
31,616031735012427 %, payback 4,
p_prelievo_pareggio None, verdetto
CONVIENTE (VAN piu' di due volte e
mezzo il CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab846 in app.py e il
count-assert sui 846 tab NON sono
inclusi in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza e del conteggio
in app.py spetta alla fase di apply del
worker, non a questa fase. Tutti i test
qui inclusi passano da hidden_files
senza app.py. La forma del count in
questa fase e' strutturale: il blocco UI
apre tab846 esattamente una volta e gli
helper definiscono le funzioni mh846.

Destinazione nel repo: tests/test_w846_campus.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w849_helpers import (
        demo_calcoli,
        mh846_autoconsumo,
        mh846_c_alt,
        mh846_c_base,
        mh846_calcola,
        mh846_capex_totale,
        mh846_co2_alt,
        mh846_co2_base,
        mh846_co2_evitata,
        mh846_csv,
        mh846_deficit,
        mh846_demo,
        mh846_demo_calcoli,
        mh846_e_alt,
        mh846_e_alt_el,
        mh846_e_el_base,
        mh846_e_fv,
        mh846_e_pdc,
        mh846_eta,
        mh846_frazione,
        mh846_flussi,
        mh846_illum_alt,
        mh846_illuminazione,
        mh846_immessa,
        mh846_int_pos,
        mh846_nneg,
        mh846_num,
        mh846_p_prelievo_pareggio,
        mh846_payback,
        mh846_pos,
        mh846_q_alt,
        mh846_q_base,
        mh846_resto,
        mh846_risparmio,
        mh846_sensibilita,
        mh846_tir,
        mh846_valida,
        mh846_van,
        mh846_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w849_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w849_helpers", os.path.join(_hf, "w849_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh846_autoconsumo = _mod.mh846_autoconsumo
    mh846_c_alt = _mod.mh846_c_alt
    mh846_c_base = _mod.mh846_c_base
    mh846_calcola = _mod.mh846_calcola
    mh846_capex_totale = _mod.mh846_capex_totale
    mh846_co2_alt = _mod.mh846_co2_alt
    mh846_co2_base = _mod.mh846_co2_base
    mh846_co2_evitata = _mod.mh846_co2_evitata
    mh846_csv = _mod.mh846_csv
    mh846_deficit = _mod.mh846_deficit
    mh846_demo = _mod.mh846_demo
    mh846_demo_calcoli = _mod.mh846_demo_calcoli
    mh846_e_alt = _mod.mh846_e_alt
    mh846_e_alt_el = _mod.mh846_e_alt_el
    mh846_e_el_base = _mod.mh846_e_el_base
    mh846_e_fv = _mod.mh846_e_fv
    mh846_e_pdc = _mod.mh846_e_pdc
    mh846_eta = _mod.mh846_eta
    mh846_frazione = _mod.mh846_frazione
    mh846_flussi = _mod.mh846_flussi
    mh846_illum_alt = _mod.mh846_illum_alt
    mh846_illuminazione = _mod.mh846_illuminazione
    mh846_immessa = _mod.mh846_immessa
    mh846_int_pos = _mod.mh846_int_pos
    mh846_nneg = _mod.mh846_nneg
    mh846_num = _mod.mh846_num
    mh846_p_prelievo_pareggio = _mod.mh846_p_prelievo_pareggio
    mh846_payback = _mod.mh846_payback
    mh846_pos = _mod.mh846_pos
    mh846_q_alt = _mod.mh846_q_alt
    mh846_q_base = _mod.mh846_q_base
    mh846_resto = _mod.mh846_resto
    mh846_risparmio = _mod.mh846_risparmio
    mh846_sensibilita = _mod.mh846_sensibilita
    mh846_tir = _mod.mh846_tir
    mh846_valida = _mod.mh846_valida
    mh846_van = _mod.mh846_van
    mh846_verdetto = _mod.mh846_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w849_helpers.py")
_UI_PATH = _risolvi("w849_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# tab precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "5_"
_VECCHIO_TAB = "tab84" + "5"
_VECCHIO_ST = "st84" + "5_"

_DEMO = {
    "e_el_base_kwh_e_anno": 9600000.0,
    "illuminazione_kwh_e_anno": 2880000.0,
    "resto_kwh_e_anno": 6720000.0,
    "illum_alt_kwh_e_anno": 1440000.0,
    "e_alt_el_kwh_e_anno": 8160000.0,
    "q_base_kwh_th_anno": 4800000.0,
    "q_alt_kwh_th_anno": 4080000.0,
    "e_pdc_kwh_e_anno": 1165714.2857142857,
    "e_alt_kwh_e_anno": 9325714.285714285,
    "e_fv_kwh_e_anno": 1650000.0,
    "autoconsumo_kwh_e_anno": 1155000.0,
    "deficit_kwh_e_anno": 8170714.285714285,
    "immessa_kwh_e_anno": 495000.0,
    "c_base_eur_anno": 2544000.0,
    "c_alt_eur_anno": 1797957.1428571427,
    "risparmio_eur_anno": 746042.8571428573,
    "capex_totale_eur": 2350000.0,
    "co2_base_t_anno": 4320.0,
    "co2_alt_t_anno": 2859.7499999999995,
    "co2_evitata_t_anno": 1460.2500000000005,
    "van": 6207052.797101904,
    "tir": 31.616031735012427,
    "payback": 4,
    "p_prelievo_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh846_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh846_num(3, "x"), 3.0)
        self.assertEqual(mh846_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh846_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh846_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh846_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh846_pos(0, "x")
        with self.assertRaises(ValueError):
            mh846_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh846_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh846_eta(0.35, "eta"), 0.35)
        with self.assertRaises(ValueError):
            mh846_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh846_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh846_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh846_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh846_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh846_frazione(0, "quota"), 0.0)
        self.assertEqual(mh846_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh846_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh846_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_e_el_base_e_split(self):
        self.assertEqual(mh846_e_el_base(8000, 1200), 9600000.0)
        self.assertEqual(mh846_e_el_base(8000, 0), 0.0)
        self.assertEqual(mh846_illuminazione(9600000.0, 0.30), 2880000.0)
        self.assertEqual(mh846_resto(9600000.0, 0.30), 6720000.0)
        self.assertAlmostEqual(mh846_illuminazione(9600000.0, 0.30)
                               + mh846_resto(9600000.0, 0.30),
                               9600000.0, places=6)
        self.assertEqual(mh846_illum_alt(2880000.0, 0.50), 1440000.0)
        self.assertEqual(mh846_e_alt_el(1440000.0, 6720000.0), 8160000.0)

    def test_termico_e_pdc(self):
        self.assertEqual(mh846_q_base(60000, 80), 4800000.0)
        self.assertEqual(mh846_q_alt(4800000.0, 0.15), 4080000.0)
        self.assertAlmostEqual(mh846_e_pdc(4080000.0, 3.5),
                               1165714.2857142857, places=6)
        self.assertAlmostEqual(mh846_e_alt(8160000.0, 1165714.2857142857),
                               9325714.285714285, places=6)

    def test_fv_autoconsumo_deficit_immessa(self):
        self.assertEqual(mh846_e_fv(1500, 1100), 1650000.0)
        self.assertEqual(mh846_autoconsumo(9325714.285714285, 1650000.0,
                                           0.70), 1155000.0)
        self.assertEqual(mh846_autoconsumo(1000000.0, 1650000.0, 0.70),
                         1000000.0)
        self.assertEqual(mh846_autoconsumo(9325714.285714285, 1650000.0,
                                           0.0), 0.0)
        self.assertAlmostEqual(mh846_deficit(9325714.285714285, 1155000.0),
                               8170714.285714285, places=6)
        self.assertEqual(mh846_immessa(1650000.0, 1155000.0), 495000.0)

    def test_bilancio_fv_autoconsumo_immessa(self):
        bc = mh846_demo_calcoli()
        self.assertAlmostEqual(bc["e_fv_kwh_e_anno"],
                               bc["autoconsumo_kwh_e_anno"]
                               + bc["immessa_kwh_e_anno"], places=6)
        self.assertGreaterEqual(bc["immessa_kwh_e_anno"], 0.0)
        self.assertGreaterEqual(bc["deficit_kwh_e_anno"], 0.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh846_c_base(9600000.0, 0.22, 4800000.0,
                                            0.09), 2544000.0, places=6)
        self.assertAlmostEqual(mh846_c_alt(8170714.285714285, 0.22,
                                           495000.0, 0.08, 40000),
                               1797957.1428571427, places=6)

    def test_capex_totale_voci(self):
        self.assertEqual(mh846_capex_totale(900, 1500, 500, 500,
                                            400000, 150000, 200000),
                         2350000.0)
        self.assertEqual(mh846_capex_totale(900, 0, 500, 0, 0, 0, 0), 0.0)

    def test_immissione_e_ricavo_non_spreco(self):
        base = mh846_demo_calcoli()
        senza_ricavo = mh846_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 39600.0, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh846_risparmio(2544000.0, 1797957.1428571427),
                               746042.8571428573, places=6)
        self.assertLess(mh846_risparmio(1797957.1428571427, 2544000.0), 0.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh846_co2_base(9600000.0, 0.35, 4800000.0,
                                              0.20), 4320.0, places=6)
        self.assertAlmostEqual(mh846_co2_alt(8170714.285714285, 0.35),
                               2859.7499999999995, places=6)
        self.assertAlmostEqual(mh846_co2_evitata(4320.0, 2859.7499999999995),
                               1460.2500000000005, places=6)

    def test_fv_nullo_e_batteria_nulla_ammessi(self):
        r = mh846_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertEqual(r["e_fv_kwh_e_anno"], 0.0)
        self.assertEqual(r["autoconsumo_kwh_e_anno"], 0.0)
        self.assertTrue(r["valid"])
        s = mh846_calcola(**_demo_kwargs(kwh_batteria=0))
        self.assertEqual(s["kwh_batteria"], 0.0)
        self.assertTrue(s["valid"])


class TestFinanza(unittest.TestCase):
    def test_p_prelievo_pareggio_demo_none(self):
        bc = mh846_demo_calcoli()
        self.assertIsNone(bc["p_prelievo_pareggio"])
        self.assertIsNone(mh846_p_prelievo_pareggio(40000, 495000.0, 0.08,
                                                    4800000.0, 0.09,
                                                    9600000.0,
                                                    8170714.285714285))

    def test_p_prelievo_pareggio_none_casi(self):
        self.assertIsNone(mh846_p_prelievo_pareggio(40000, 495000.0, 0.08,
                                                    4800000.0, 0.09,
                                                    9600000.0, 9600000.0))
        self.assertIsNone(mh846_calcola(**_demo_kwargs(
            risparmio_led=0, recupero_lab=0, cop=1.0))
            ["p_prelievo_pareggio"])

    def test_p_prelievo_pareggio_costruito_positivo(self):
        base = _demo_kwargs(superficie_m2=0, p_pv_kwp=0)
        bc = mh846_calcola(**base)
        self.assertAlmostEqual(bc["p_prelievo_pareggio"],
                               0.027777777777777776, places=12)
        self.assertAlmostEqual(mh846_p_prelievo_pareggio(40000, 0.0, 0.08,
                                                         0.0, 0.09,
                                                         9600000.0,
                                                         8160000.0),
                               0.027777777777777776, places=12)

    def test_p_prelievo_pareggio_verifica(self):
        base = _demo_kwargs(superficie_m2=0, p_pv_kwp=0)
        bc = mh846_calcola(**base)
        pstar = bc["p_prelievo_pareggio"]
        r = mh846_calcola(**_demo_kwargs(superficie_m2=0, p_pv_kwp=0,
                                         p_prelievo=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_prelievo_pareggio_soglia(self):
        base = _demo_kwargs(superficie_m2=0, p_pv_kwp=0)
        pstar = mh846_calcola(**base)["p_prelievo_pareggio"]
        self.assertAlmostEqual(
            mh846_calcola(**_demo_kwargs(superficie_m2=0, p_pv_kwp=0,
                                         p_prelievo=pstar + 0.01))
            ["risparmio_eur_anno"], 14400.0, places=6)
        self.assertAlmostEqual(
            mh846_calcola(**_demo_kwargs(superficie_m2=0, p_pv_kwp=0,
                                         p_prelievo=pstar - 0.01))
            ["risparmio_eur_anno"], -14400.0, places=6)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh846_flussi(2350000, 746042.8571428573, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -2350000)
        self.assertTrue(all(f == 746042.8571428573 for f in flussi[1:]))

    def test_van_demo_e_zero_tasso(self):
        bc = mh846_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 6207052.797101904, places=6)
        self.assertAlmostEqual(mh846_van([-2350000] + [746042.8571428573] * 20,
                                         0.0), 12570857.14285715, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh846_van([-2350000] + [746042.8571428573] * 20,
                                         0.06), 6207052.797101904, places=6)
        self.assertLess(mh846_van([-2350000] + [746042.8571428573] * 20, 6.0),
                        0.0)

    def test_tir_demo(self):
        bc = mh846_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 31.616031735012427, places=6)
        self.assertGreater(bc["tir"], 30.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh846_payback([-2350000] + [746042.8571428573] * 20), 4)
        self.assertEqual(mh846_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh846_payback([-2350000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh846_verdetto(746042.8571428573, 100.0, 2350000, 0.05),
                         "CONVIENTE")
        self.assertEqual(mh846_verdetto(746042.8571428573, -20000.0, 2350000, 0.05),
                         "MARGINALE")
        self.assertEqual(mh846_verdetto(746042.8571428573, -200000.0, 2350000, 0.05),
                         "NON_CONVIENTE")
        self.assertEqual(mh846_verdetto(0.0, 100.0, 2350000, 0.05),
                         "NON_CALCOLABILE")
        self.assertEqual(mh846_verdetto(-100.0, 100.0, 2350000, 0.05),
                         "NON_CALCOLABILE")
        self.assertEqual(mh846_verdetto(None, 100.0, 2350000, 0.05),
                         "NON_CALCOLABILE")
        self.assertEqual(mh846_verdetto(746042.8571428573, 0.0, 2350000, 0.05),
                         "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh846_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("studenti", "8000"),
                            ("studenti", float("nan")),
                            ("studenti", float("inf")),
                            ("studenti", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh846_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"studenti": 0},
                     {"studenti": -1},
                     {"kwh_e_per_studente": -1},
                     {"share_illuminazione": -0.1},
                     {"share_illuminazione": 1.1},
                     {"risparmio_led": -0.1},
                     {"risparmio_led": 1.1},
                     {"superficie_m2": -1},
                     {"kwh_th_per_m2": -1},
                     {"recupero_lab": -0.1},
                     {"recupero_lab": 1.1},
                     {"cop": 0},
                     {"cop": -1},
                     {"p_pv_kwp": -1},
                     {"prod_specifica": -1},
                     {"f_autoconsumo": -0.1},
                     {"f_autoconsumo": 1.1},
                     {"kwh_batteria": -1},
                     {"p_prelievo": -0.1},
                     {"p_gas": -0.1},
                     {"p_immissione": -0.1},
                     {"opex_alt": -1},
                     {"capex_fv": -1},
                     {"capex_batteria": -1},
                     {"capex_pdc": -1},
                     {"capex_led": -1},
                     {"capex_recupero": -1},
                     {"f_el": -0.1},
                     {"f_gas": -0.1},
                     {"tasso": -0.1},
                     {"vita": 0},
                     {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh846_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_tasso_tolleranza(self):
        self.assertTrue(mh846_valida(**_demo_kwargs(tasso=0.25))["valido"])
        self.assertTrue(mh846_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh846_valida(**_demo_kwargs(
            kwh_e_per_studente=0, share_illuminazione=0,
            risparmio_led=0, superficie_m2=0, kwh_th_per_m2=0,
            recupero_lab=0, p_pv_kwp=0, prod_specifica=0,
            f_autoconsumo=0, kwh_batteria=0, p_prelievo=0,
            p_gas=0, p_immissione=0, opex_alt=0, capex_fv=0,
            capex_batteria=0, capex_pdc=0, capex_led=0,
            capex_recupero=0, f_el=0, f_gas=0, tasso=0,
            tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh846_demo()
        self.assertEqual(d["studenti"], 8000)
        self.assertEqual(d["kwh_e_per_studente"], 1200)
        self.assertEqual(d["share_illuminazione"], 0.30)
        self.assertEqual(d["risparmio_led"], 0.50)
        self.assertEqual(d["superficie_m2"], 60000)
        self.assertEqual(d["kwh_th_per_m2"], 80)
        self.assertEqual(d["recupero_lab"], 0.15)
        self.assertEqual(d["cop"], 3.5)
        self.assertEqual(d["p_pv_kwp"], 1500)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["f_autoconsumo"], 0.70)
        self.assertEqual(d["kwh_batteria"], 500)
        self.assertEqual(d["p_prelievo"], 0.22)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["p_immissione"], 0.08)
        self.assertEqual(d["opex_alt"], 40000)
        self.assertEqual(d["capex_fv"], 900)
        self.assertEqual(d["capex_batteria"], 500)
        self.assertEqual(d["capex_pdc"], 400000)
        self.assertEqual(d["capex_led"], 150000)
        self.assertEqual(d["capex_recupero"], 200000)
        self.assertEqual(d["f_el"], 0.35)
        self.assertEqual(d["f_gas"], 0.20)
        self.assertEqual(d["tasso"], 0.06)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.05)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh846_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh846_demo_calcoli()
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"], 9600000.0, places=6)
        self.assertEqual(bc["e_alt_kwh_e_anno"], 9325714.285714285)
        self.assertEqual(bc["e_fv_kwh_e_anno"], 1650000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 2544000.0, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 1797957.1428571427, places=6)
        self.assertEqual(bc["capex_totale_eur"], 2350000.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh846_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[1],
                               -1603957.1428571427, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[4],
                               634171.4285714291, places=6)

    def test_demo_tabella_righe(self):
        bc = mh846_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Studenti equivalenti a tempo pieno", voci)
        self.assertIn("Superficie aule e laboratori (m2)", voci)
        self.assertIn("Domanda elettrica base (kWh_e/anno)", voci)
        self.assertIn("Illuminazione base (kWh_e/anno)", voci)
        self.assertIn("Domanda elettrica alternativa totale (kWh_e/anno)", voci)
        self.assertIn("Fabbisogno termico base (kWh_th/anno)", voci)
        self.assertIn("Elettricita' pompa di calore (kWh_e/anno)", voci)
        self.assertIn("Energia immessa, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("CAPEX totale (EUR)", voci)
        self.assertIn("Prezzo di prelievo di pareggio (EUR/kWh, soglia)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh846_demo_calcoli()
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"],
                               bc["studenti"] * bc["kwh_e_per_studente"])
        self.assertAlmostEqual(bc["e_alt_kwh_e_anno"],
                               bc["e_alt_el_kwh_e_anno"]
                               + bc["e_pdc_kwh_e_anno"])
        self.assertAlmostEqual(bc["deficit_kwh_e_anno"],
                               bc["e_alt_kwh_e_anno"]
                               - bc["autoconsumo_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(bc["capex_totale_eur"],
                               bc["capex_fv"] * bc["p_pv_kwp"]
                               + bc["capex_batteria"] * bc["kwh_batteria"]
                               + bc["capex_pdc"] + bc["capex_led"]
                               + bc["capex_recupero"])

    def test_demo_contro_riconteggio_indipendente(self):
        ebase = 8000 * 1200
        ill = ebase * 0.30
        resto = ebase * 0.70
        ialt = ill * 0.50
        ealtel = ialt + resto
        qb = 60000 * 80
        qa = qb * 0.85
        epdc = qa / 3.5
        ealt = ealtel + epdc
        efv = 1500 * 1100
        aut = min(ealt, efv * 0.70)
        dft = ealt - aut
        imm = efv - aut
        c_base = ebase * 0.22 + qb * 0.09
        c_alt = dft * 0.22 - imm * 0.08 + 40000
        bc = mh846_demo_calcoli()
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"], ebase, places=6)
        self.assertAlmostEqual(bc["illuminazione_kwh_e_anno"], ill, places=6)
        self.assertAlmostEqual(bc["e_alt_el_kwh_e_anno"], ealtel, places=6)
        self.assertAlmostEqual(bc["q_base_kwh_th_anno"], qb, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_fv_kwh_e_anno"], efv, places=6)
        self.assertAlmostEqual(bc["autoconsumo_kwh_e_anno"], aut, places=6)
        self.assertAlmostEqual(bc["deficit_kwh_e_anno"], dft, places=6)
        self.assertAlmostEqual(bc["immessa_kwh_e_anno"], imm, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt,
                               places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh846_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_prelievo_piu_meno_20(self):
        meno = mh846_calcola(**_demo_kwargs(p_prelievo=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 683154.2857142857,
                               places=6)
        self.assertAlmostEqual(meno["van"], 5485725.837268074, places=6)
        self.assertAlmostEqual(meno["tir"], 28.888781447909572, places=6)
        self.assertEqual(meno["payback"], 4)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh846_calcola(**_demo_kwargs(p_prelievo=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 808931.4285714286,
                               places=6)
        self.assertAlmostEqual(piu["van"], 6928379.7569357315, places=6)
        self.assertAlmostEqual(piu["tir"], 34.32853814783577, places=6)
        self.assertEqual(piu["payback"], 3)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_prelievo_alto_migliora_il_caso(self):
        demo = mh846_demo_calcoli()
        meno = mh846_calcola(**_demo_kwargs(p_prelievo=0.176))
        piu = mh846_calcola(**_demo_kwargs(p_prelievo=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_convinte(self):
        r = mh846_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 452342.8571428573,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 4188336.9352092897, places=6)
        self.assertAlmostEqual(r["tir"], 45.208245643086734, places=6)
        self.assertEqual(r["payback"], 3)
        self.assertEqual(r["capex_totale_eur"], 1000000.0)

    def test_variante_senza_led_convinte(self):
        r = mh846_calcola(**_demo_kwargs(risparmio_led=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 429242.8571428573,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 2573381.755060432, places=6)
        self.assertAlmostEqual(r["tir"], 17.545329919389868, places=6)
        self.assertEqual(r["payback"], 6)

    def test_variante_senza_recupero_convinte(self):
        r = mh846_calcola(**_demo_kwargs(recupero_lab=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 700785.7142857143,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 5687956.933953121, places=6)
        self.assertAlmostEqual(r["tir"], 29.655198923800917, places=6)
        self.assertEqual(r["payback"], 4)

    def test_variante_capex_doppio_convinte(self):
        r = mh846_calcola(**_demo_kwargs(capex_fv=1800,
                                         capex_batteria=1000,
                                         capex_pdc=800000,
                                         capex_led=300000,
                                         capex_recupero=400000))
        self.assertAlmostEqual(r["van"], 3857052.7971019032, places=6)
        self.assertAlmostEqual(r["tir"], 14.883537872978597, places=6)
        self.assertEqual(r["payback"], 7)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertEqual(r["capex_totale_eur"], 4700000.0)

    def test_variante_vita_10_convinte(self):
        r = mh846_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 3140940.372657567, places=6)
        self.assertAlmostEqual(r["tir"], 29.319602128249755, places=6)
        self.assertEqual(r["payback"], 4)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_variante_tasso_zero(self):
        zero = mh846_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(zero["van"], 12570857.14285715, places=6)
        self.assertEqual(zero["payback"], 4)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh846_sensibilita(**mh846_demo())
        self.assertEqual(set(s.keys()), {"prelievo_meno20", "prelievo_piu20",
                                         "senza_fv", "senza_led",
                                         "senza_recupero",
                                         "capex_doppio", "vita_10",
                                         "tasso_0"})
        self.assertAlmostEqual(s["prelievo_meno20"]["risparmio_eur_anno"],
                               683154.2857142857, places=6)
        self.assertAlmostEqual(s["prelievo_piu20"]["van"],
                               6928379.7569357315, places=6)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_led"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["tasso_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh846_demo_calcoli()
        b = mh846_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh846_demo()
        attese = {"studenti", "kwh_e_per_studente",
                  "share_illuminazione", "risparmio_led",
                  "superficie_m2", "kwh_th_per_m2",
                  "recupero_lab", "cop", "p_pv_kwp",
                  "prod_specifica", "f_autoconsumo",
                  "kwh_batteria", "p_prelievo", "p_gas",
                  "p_immissione", "opex_alt", "capex_fv",
                  "capex_batteria", "capex_pdc", "capex_led",
                  "capex_recupero", "f_el", "f_gas", "tasso",
                  "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["studenti", "kwh_e_per_studente",
                 "share_illuminazione", "risparmio_led",
                 "superficie_m2", "kwh_th_per_m2",
                 "recupero_lab", "cop", "p_pv_kwp",
                 "prod_specifica", "f_autoconsumo",
                 "kwh_batteria", "p_prelievo", "p_gas",
                 "p_immissione", "opex_alt", "capex_fv",
                 "capex_batteria", "capex_pdc", "capex_led",
                 "capex_recupero", "f_el", "f_gas", "tasso",
                 "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh846_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_cop_zero_e_vita(self):
        with self.assertRaises(ValueError):
            mh846_calcola(**_demo_kwargs(share_illuminazione=1.1))
        with self.assertRaises(ValueError):
            mh846_calcola(**_demo_kwargs(risparmio_led=1.1))
        with self.assertRaises(ValueError):
            mh846_calcola(**_demo_kwargs(recupero_lab=1.1))
        with self.assertRaises(ValueError):
            mh846_calcola(**_demo_kwargs(f_autoconsumo=1.1))
        with self.assertRaises(ValueError):
            mh846_calcola(**_demo_kwargs(cop=0))
        with self.assertRaises(ValueError):
            mh846_calcola(**_demo_kwargs(studenti=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("studenti", "8000"),
                           ("studenti", float("nan")),
                           ("capex_pdc", float("inf")),
                           ("p_prelievo", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh846_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh846_calcola(**_demo_kwargs(
            kwh_e_per_studente=0, share_illuminazione=0,
            risparmio_led=0, superficie_m2=0, kwh_th_per_m2=0,
            recupero_lab=0, p_pv_kwp=0, prod_specifica=0,
            f_autoconsumo=0, kwh_batteria=0, p_prelievo=0,
            p_gas=0, p_immissione=0, opex_alt=0, capex_fv=0,
            capex_batteria=0, capex_pdc=0, capex_led=0,
            capex_recupero=0, f_el=0, f_gas=0, tasso=0,
            tolleranza=0))
        self.assertTrue(r["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh846_calcola(**_demo_kwargs(opex_alt=900000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(r["risparmio_eur_anno"], -113957.14285714272,
                               places=6)

    def test_pareggio_esatto_soglia(self):
        base = _demo_kwargs(superficie_m2=0, p_pv_kwp=0)
        pstar = mh846_calcola(**base)["p_prelievo_pareggio"]
        r = mh846_calcola(**_demo_kwargs(superficie_m2=0, p_pv_kwp=0,
                                         p_prelievo=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh846_demo_calcoli()
        csv = mh846_csv(bc, dict(mh846_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh846_demo_calcoli()
        csv = mh846_csv(bc, dict(mh846_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1]
                 for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]),
                               746042.8571428573, places=6)
        self.assertIn("p_prelievo_pareggio", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh846_demo_calcoli()
        csv = mh846_csv(bc, dict(mh846_demo()))
        for chiave in mh846_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab846:"), 1)
        self.assertTrue(src.startswith("    # W849"))

    def test_ui_tab846_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre tab846 esattamente una
        # volta e gli helper definiscono le funzioni mh846.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab846:"), 1)
        self.assertIn("def mh846_demo(", src_h)
        self.assertIn("def mh846_calcola(", src_h)
        self.assertIn("tab846", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Campus universitario: fotovoltaico + batteria + pompa di calore + LED + recupero calore laboratori battono caldaia a gas + rete + illuminazione tradizionale?", src)
        self.assertIn("🎓 Campus universitario: fotovoltaico + batteria + pompa di calore + LED + recupero calore laboratori battono caldaia a gas + rete + illuminazione tradizionale?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
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
        chiavi = re.findall(r'key="(st846_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st846_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st846_calcola"', src)
        self.assertIn('key="st846_csv"', src)
        self.assertIn('key="st846_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def846\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh846_demo().keys()), lette - set(mh846_demo().keys()))
        self.assertEqual(lette, set(mh846_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc846\['([^']+)'\]", src))
        attese = set(mh846_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg846"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
