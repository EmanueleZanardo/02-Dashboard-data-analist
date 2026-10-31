"""Test nuova scheda tab841 "Maneggio:
fotovoltaico + batteria + pompa di calore
+ LED arena battono caldaia a gas +
prelievo da rete per box, scuderie e
maneggio coperto?".

Business case annuo di un maneggio coperto
con scuderie (300 giorni di apertura),
connesso alla rete, guidato dal PRODOTTO
box x giorni di apertura:
Q_term = box x giorni x q_spec_termico;
E_el_base = box x giorni x
e_spec_elettrico; E_led_risp = E_el_base x
quota_illum x rid_led (i LED arena
tagliano solo la quota illuminazione);
E_el_led = E_el_base - E_led_risp;
E_pdc = Q_term / COP; E_tot_alt = E_pdc +
E_el_led; E_pv = kWp x producibilita';
E_pv_diretta = E_pv x quota_diretta;
E_pv_batt_lordo = E_pv x (1 - quota_diretta);
E_pv_batt_netta = min(lordo x RTE, cap_batt
x DoD x cicli_anno) (cap annuo di
throughput batteria); E_pv_servita_pot =
diretta + netta; E_autoconsumo =
min(servita_pot, E_tot_alt); E_deficit =
E_tot_alt - autoconsumo (prelevato da rete
a prezzo di prelievo); E_batt_ciclata =
netta / RTE; E_perdite_batt = ciclata -
netta (perdite reali, ne' consumo ne'
immissione); E_immessa = E_pv -
autoconsumo - perdite_batt (>= 0 per
costruzione: lordo non ciclato piu'
eventuale servito potenziale sopra la
domanda; immessa a prezzo inferiore al
prelievo, RICAVO e non spreco, perche'
la rete esiste: differenza onesta dal
campeggio off-grid); autonomia_batt =
cap_batt x DoD / (E_tot_alt / giorni)
(0 se domanda nulla); gas_base = Q_term /
eta_caldaia; costo_gas = gas_base x
p_gas; prelievo rete base = E_el_base x
p_rete; C_base = costo_gas + prelievo
rete base + O&M_base; C_alt = deficit x
p_rete - immessa x p_immissione +
O&M_alt (l'immissione e' un ricavo, segno
meno); risparmio = C_base - C_alt;
CO2 gas base = gas_base x f_co2_gas /
1000; CO2 rete base = E_el_base x
f_co2_rete / 1000; CO2 base = somma dei
due; CO2 alt = (deficit - immessa) x
f_co2_rete / 1000 (credito CO2
sull'immissione allo stesso fattore rete,
scelta simmetrica documentata; puo'
essere negativa se l'immissione supera
il deficit); CO2 evitata = base - alt
(segno libero, non clampata: puo' essere
negativa se il deficit supera la base
elettrica piu' l'immissione); flussi
[-CAPEX, risparmio x vita]; VAN al WACC
(FRAZIONE, non percentuale); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p* = (deficit x p_rete - immessa x
p_immissione + O&M_alt - E_el_base x
p_rete - O&M_base) / gas_base in forma
chiusa a prezzi elettrici FERMI, None se
gas_base <= 0 o se p* < 0, SOGLIA MINIMA
sui soli costi annui quando esiste (sopra
di essa l'alternativa vince, sotto perde;
il CAPEX non entra nel pareggio annuo).
Nel demo p* e' None: a prezzo gas nullo
il risparmio resterebbe 12.565,20
EUR/anno (solo elettrico netto + O&M),
quindi l'alternativa vince sui costi
annui anche a gas gratis.
Verdetto: NON_CALCOLABILE se input
degenere (box <= 0 o non interi,
giorni <= 0 o non interi, fabbisogni
specifici < 0, quota_illum < 0 o > 1,
rid_led < 0 o > 1, eta_caldaia <= 0 o
> 1, prezzi < 0, COP <= 0, quota_diretta
< 0 o > 1, RTE <= 0 o > 1, cap_batt < 0,
DoD < 0 o > 1, cicli < 0, kWp < 0,
producibilita' < 0, O&M < 0, CAPEX < 0,
fattori CO2 < 0, WACC < 0, vita <= 0 o
non intera, tolleranza < 0) o se risparmio
<= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza FRAZIONE del
CAPEX, NON_CONVIENTE se VAN negativa
oltre la tolleranza. Guard UI IDENTICA
agli helper: nessuna divergenza di
verdetto. Tutti gli slider UI hanno
minimo 0, quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0
raggiungibili via slider sono bloccati in
UI esattamente come negli helper dove
previsto (box, giorni, vita, COP,
eta_caldaia, RTE). Gli zeri ammessi in
entrambi (fabbisogni specifici, quote,
rid_led, prezzi, quota FV diretta,
cap_batt, DoD, cicli, kWp, producibilita',
O&M, CAPEX, fattori CO2, WACC, tolleranza)
non creano divergenza. Quote, rid_led e
DoD > 1 e eta_caldaia > 1 sono degeneri in
entrambi ma non raggiungibili via slider
(tetto 1,0). WACC sopra 0,20 e tolleranza
sopra 1,0 sono ammessi negli helper e
limitati solo dagli slider UI (0,20 e 1,0):
nessuna divergenza nel range raggiungibile,
perche' la guard controlla solo gli
stessi limiti degli helper. Distinzione
esplicita: distinto dal campeggio
stagionale off-grid (150 giorni, senza
rete, eccesso FV sprecato senza credito:
qui 300 giorni, con rete, eccesso immesso
e pagato, deficit prelevato a prezzo
pieno) e dall'albergo annuale connesso
alla rete con domanda piatta (driver non
box x giorni, nessun LED arena dedicato:
qui driver box x giorni di apertura e LED
che tagliano solo la quota illuminazione
arena).

Demo (maneggio): 30 box, 300 giorni,
q_spec_termico 12 (Q_term 108.000
kWh_th/anno), e_spec 8 (E_el_base
72.000 kWh_e/anno), quota_illum 0,40
con rid_led 0,55 (risparmio LED 15.840,
E_el_led 56.160 kWh_e/anno),
eta_caldaia 0,90, prezzo gas 0,10
EUR/kWh, prezzo prelievo rete 0,28
EUR/kWh, prezzo immissione 0,12 EUR/kWh,
COP 3,0 (E_pdc 36.000, E_tot_alt 92.160
kWh_e/anno), quota_diretta 0,50, RTE
0,90, batteria 150 kWh con DoD 0,85 e
300 cicli/anno (cap throughput 38.250
kWh_e/anno), fotovoltaico 80 kWp a 1.100
kWh/kWp/anno (E_pv 88.000, diretta
44.000, batt lordo 44.000, batt netta
38.250, servita potenziale 82.250,
autoconsumo 82.250, deficit 9.910,
ciclata 42.500, perdite batt 4.250,
immessa 1.500 con ricavo, autonomia
0,4150390625 giorni), gas base 120.000
kWh/anno (costo gas 12.000, prelievo rete
base 20.160), O&M base 2.500, O&M alt
7.500, CAPEX 220.000 EUR, fattore CO2
gas 0,202 kg/kWh, fattore CO2 rete 0,30
kg/kWh_e, WACC 0,05 (frazione), vita 20
anni, tolleranza 0,10 (frazione del
CAPEX).
Valori calcolati eseguendo
mh841_demo_calcoli(): Q_term 108000,0,
E_el_base 72000,0, E_led_risp 15840,0,
E_el_led 56160,0, E_pdc 36000,0,
E_tot_alt 92160,0, E_pv 88000,0,
diretta 44000,0, batt lordo 44000,0,
batt netta 38250,0, servita pot 82250,0,
autoconsumo 82250,0, deficit 9910,0,
ciclata 42500,0, perdite batt 4250,0,
immessa 1500,0, autonomia
0,4150390625, gas base 120000,0,
costo gas 12000,0, prelievo rete base
20160,0, C_base 34660,0, C_alt
10094,8, risparmio 24565,2, CO2 gas
base 24,24, CO2 rete base 21,6, CO2 base
45,84, CO2 alt 2,523, CO2 evitata
43,317, VAN 86136,68950656317, TIR
9,269729665519828 %, payback 9,
p_gas_pareggio None (a gas nullo il
risparmio resterebbe 12.565,20 EUR/anno),
verdetto CONVIENTE (VAN il 39,15 % del
CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab841 in app.py NON e'
incluso in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza in app.py spetta
alla fase di apply del worker, non a
questa fase. Tutti i test qui inclusi
passano da hidden_files senza app.py.

Destinazione nel repo: tests/test_w841_maneggio.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w844_helpers import (
        demo_calcoli,
        mh841_autonomia_batt,
        mh841_c_alt,
        mh841_c_base,
        mh841_calcola,
        mh841_co2_evitata,
        mh841_co2_gas,
        mh841_co2_rete,
        mh841_costo_gas,
        mh841_costo_rete_base,
        mh841_csv,
        mh841_demo,
        mh841_demo_calcoli,
        mh841_e_deficit,
        mh841_e_el_base,
        mh841_e_el_led,
        mh841_e_led_risparmio,
        mh841_e_pdc,
        mh841_e_pv,
        mh841_e_tot_alt,
        mh841_eta,
        mh841_frazione,
        mh841_flussi,
        mh841_gas_kwh,
        mh841_int_pos,
        mh841_nneg,
        mh841_num,
        mh841_p_gas_pareggio,
        mh841_payback,
        mh841_pos,
        mh841_pv_autoconsumo,
        mh841_pv_batt_ciclata,
        mh841_pv_batt_lordo,
        mh841_pv_batt_netta,
        mh841_pv_diretta,
        mh841_pv_immessa,
        mh841_pv_perdite_batt,
        mh841_pv_servita_pot,
        mh841_q_termico,
        mh841_risparmio,
        mh841_sensibilita,
        mh841_tir,
        mh841_valida,
        mh841_van,
        mh841_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w844_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w844_helpers", os.path.join(_hf, "w844_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh841_autonomia_batt = _mod.mh841_autonomia_batt
    mh841_c_alt = _mod.mh841_c_alt
    mh841_c_base = _mod.mh841_c_base
    mh841_calcola = _mod.mh841_calcola
    mh841_co2_evitata = _mod.mh841_co2_evitata
    mh841_co2_gas = _mod.mh841_co2_gas
    mh841_co2_rete = _mod.mh841_co2_rete
    mh841_costo_gas = _mod.mh841_costo_gas
    mh841_costo_rete_base = _mod.mh841_costo_rete_base
    mh841_csv = _mod.mh841_csv
    mh841_demo = _mod.mh841_demo
    mh841_demo_calcoli = _mod.mh841_demo_calcoli
    mh841_e_deficit = _mod.mh841_e_deficit
    mh841_e_el_base = _mod.mh841_e_el_base
    mh841_e_el_led = _mod.mh841_e_el_led
    mh841_e_led_risparmio = _mod.mh841_e_led_risparmio
    mh841_e_pdc = _mod.mh841_e_pdc
    mh841_e_pv = _mod.mh841_e_pv
    mh841_e_tot_alt = _mod.mh841_e_tot_alt
    mh841_eta = _mod.mh841_eta
    mh841_frazione = _mod.mh841_frazione
    mh841_flussi = _mod.mh841_flussi
    mh841_gas_kwh = _mod.mh841_gas_kwh
    mh841_int_pos = _mod.mh841_int_pos
    mh841_nneg = _mod.mh841_nneg
    mh841_num = _mod.mh841_num
    mh841_p_gas_pareggio = _mod.mh841_p_gas_pareggio
    mh841_payback = _mod.mh841_payback
    mh841_pos = _mod.mh841_pos
    mh841_pv_autoconsumo = _mod.mh841_pv_autoconsumo
    mh841_pv_batt_ciclata = _mod.mh841_pv_batt_ciclata
    mh841_pv_batt_lordo = _mod.mh841_pv_batt_lordo
    mh841_pv_batt_netta = _mod.mh841_pv_batt_netta
    mh841_pv_diretta = _mod.mh841_pv_diretta
    mh841_pv_immessa = _mod.mh841_pv_immessa
    mh841_pv_perdite_batt = _mod.mh841_pv_perdite_batt
    mh841_pv_servita_pot = _mod.mh841_pv_servita_pot
    mh841_q_termico = _mod.mh841_q_termico
    mh841_risparmio = _mod.mh841_risparmio
    mh841_sensibilita = _mod.mh841_sensibilita
    mh841_tir = _mod.mh841_tir
    mh841_valida = _mod.mh841_valida
    mh841_van = _mod.mh841_van
    mh841_verdetto = _mod.mh841_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w844_helpers.py")
_UI_PATH = _risolvi("w844_ui.py")

_DEMO = {
    "q_termico_kwh_th_anno": 108000.0,
    "e_el_base_kwh_e_anno": 72000.0,
    "e_led_risparmio_kwh_e_anno": 15840.0,
    "e_el_led_kwh_e_anno": 56160.0,
    "e_pdc_kwh_e_anno": 36000.0,
    "e_tot_alt_kwh_e_anno": 92160.0,
    "e_pv_kwh_e_anno": 88000.0,
    "e_pv_diretta_kwh_e_anno": 44000.0,
    "e_pv_batt_lordo_kwh_e_anno": 44000.0,
    "e_pv_batt_netta_kwh_e_anno": 38250.0,
    "e_pv_servita_pot_kwh_e_anno": 82250.0,
    "e_pv_autoconsumo_kwh_e_anno": 82250.0,
    "e_deficit_kwh_e_anno": 9910.0,
    "e_pv_batt_ciclata_kwh_e_anno": 42500.0,
    "e_pv_perdite_batt_kwh_e_anno": 4250.0,
    "e_pv_immessa_kwh_e_anno": 1500.0,
    "autonomia_batt_giorni": 0.4150390625,
    "gas_base_kwh_anno": 120000.0,
    "costo_gas_eur_anno": 12000.0,
    "costo_rete_base_eur_anno": 20160.0,
    "c_base_eur_anno": 34660.0,
    "c_alt_eur_anno": 10094.8,
    "risparmio_eur_anno": 24565.2,
    "co2_gas_base_t_anno": 24.24,
    "co2_rete_base_t_anno": 21.6,
    "co2_base_t_anno": 45.84,
    "co2_alt_t_anno": 2.523,
    "co2_evitata_t_anno": 43.317,
    "van": 86136.68950656317,
    "tir": 9.269729665519828,
    "payback": 9,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh841_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh841_num(3, "x"), 3.0)
        self.assertEqual(mh841_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh841_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh841_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh841_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh841_pos(0, "x")
        with self.assertRaises(ValueError):
            mh841_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh841_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh841_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh841_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh841_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh841_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh841_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh841_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh841_frazione(0, "quota"), 0.0)
        self.assertEqual(mh841_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh841_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh841_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_termico_e_el_base_driver_box_giorni(self):
        self.assertEqual(mh841_q_termico(30, 300, 12), 108000.0)
        self.assertEqual(mh841_e_el_base(30, 300, 8), 72000.0)

    def test_led_taglia_solo_quota_illuminazione(self):
        self.assertAlmostEqual(mh841_e_led_risparmio(72000.0, 0.40, 0.55), 15840.0, places=6)
        self.assertEqual(mh841_e_el_led(72000.0, 15840.0), 56160.0)
        self.assertEqual(mh841_e_led_risparmio(72000.0, 0.0, 0.55), 0.0)
        self.assertEqual(mh841_e_led_risparmio(72000.0, 0.40, 0.0), 0.0)
        self.assertEqual(mh841_e_led_risparmio(72000.0, 1.0, 1.0), 72000.0)

    def test_e_pdc_e_tot(self):
        self.assertAlmostEqual(mh841_e_pdc(108000.0, 3.0), 36000.0, places=6)
        self.assertAlmostEqual(mh841_e_tot_alt(36000.0, 56160.0), 92160.0, places=6)

    def test_pv_diretta_lordo(self):
        self.assertEqual(mh841_e_pv(80, 1100), 88000.0)
        self.assertEqual(mh841_pv_diretta(88000.0, 0.50), 44000.0)
        self.assertEqual(mh841_pv_batt_lordo(88000.0, 0.50), 44000.0)

    def test_batt_netta_cap_throughput_lega(self):
        self.assertEqual(mh841_pv_batt_netta(44000.0, 0.90, 150, 0.85, 300), 38250.0)
        self.assertEqual(mh841_pv_batt_netta(44000.0, 0.90, 10000, 0.85, 300), 39600.0)
        self.assertEqual(mh841_pv_batt_netta(44000.0, 0.90, 0, 0.85, 300), 0.0)

    def test_autoconsumo_cappato_a_domanda_e_immessa(self):
        self.assertEqual(mh841_pv_servita_pot(44000.0, 38250.0), 82250.0)
        self.assertEqual(mh841_pv_autoconsumo(82250.0, 92160.0), 82250.0)
        self.assertEqual(mh841_pv_autoconsumo(313250.0, 92160.0), 92160.0)
        self.assertEqual(mh841_pv_batt_ciclata(38250.0, 0.90), 42500.0)
        self.assertEqual(mh841_pv_perdite_batt(42500.0, 38250.0), 4250.0)
        self.assertEqual(mh841_pv_immessa(88000.0, 82250.0, 4250.0), 1500.0)

    def test_immessa_mai_negativa_e_bilancio_pv(self):
        bc = mh841_demo_calcoli()
        self.assertGreaterEqual(bc["e_pv_immessa_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_autoconsumo_kwh_e_anno"]
                               + bc["e_pv_perdite_batt_kwh_e_anno"]
                               + bc["e_pv_immessa_kwh_e_anno"], places=6)
        grosso = mh841_calcola(**_demo_kwargs(p_pv_kwp=500))
        self.assertEqual(grosso["e_pv_autoconsumo_kwh_e_anno"], 92160.0)
        self.assertEqual(grosso["e_deficit_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(grosso["e_pv_immessa_kwh_e_anno"], 453590.0, places=6)
        self.assertGreater(grosso["e_pv_immessa_kwh_e_anno"], 0.0)

    def test_deficit_e_autonomia(self):
        self.assertAlmostEqual(mh841_e_deficit(92160.0, 82250.0), 9910.0, places=6)
        self.assertAlmostEqual(mh841_autonomia_batt(150, 0.85, 92160.0, 300), 0.4150390625, places=12)
        self.assertEqual(mh841_autonomia_batt(150, 0.85, 0, 300), 0.0)

    def test_gas_e_prelievo_rete_base(self):
        self.assertEqual(mh841_gas_kwh(108000.0, 0.90), 120000.0)
        self.assertEqual(mh841_costo_gas(120000.0, 0.10), 12000.0)
        self.assertAlmostEqual(mh841_costo_rete_base(72000.0, 0.28), 20160.0, places=6)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh841_c_base(12000.0, 20160.0, 2500), 34660.0, places=6)
        self.assertAlmostEqual(mh841_c_alt(9910.0, 0.28, 1500.0, 0.12, 7500), 10094.8, places=6)

    def test_immissione_e_ricavo_non_spreco(self):
        # Con immissione a zero il costo alternativo sale del ricavo perso.
        base = mh841_demo_calcoli()
        senza_ricavo = mh841_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 180.0, places=6)
        self.assertAlmostEqual(senza_ricavo["risparmio_eur_anno"],
                               base["risparmio_eur_anno"] - 180.0, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh841_risparmio(34660.0, 10094.8), 24565.2, places=6)
        self.assertLess(mh841_risparmio(10094.8, 34660.0), 0.0)

    def test_co2_due_fattori_e_evitata(self):
        self.assertAlmostEqual(mh841_co2_gas(120000.0, 0.202), 24.24, places=6)
        self.assertAlmostEqual(mh841_co2_rete(72000.0, 0.30), 21.6, places=6)
        self.assertAlmostEqual(mh841_co2_rete(9910.0 - 1500.0, 0.30), 2.523, places=6)
        self.assertAlmostEqual(mh841_co2_evitata(45.84, 2.523), 43.317, places=6)

    def test_co2_evitata_negativa_non_clampata_e_alt_negativa(self):
        self.assertAlmostEqual(mh841_co2_evitata(100.0, 200.0), -100.0, places=6)
        grosso = mh841_calcola(**_demo_kwargs(p_pv_kwp=500))
        self.assertLess(grosso["co2_alt_t_anno"], 0.0)
        self.assertAlmostEqual(grosso["co2_alt_t_anno"], -136.077, places=6)
        self.assertGreater(grosso["co2_evitata_t_anno"], grosso["co2_base_t_anno"])

    def test_immessa_con_ricavo_in_c_alt(self):
        bc = mh841_demo_calcoli()
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_deficit_kwh_e_anno"] * 0.28
                               - bc["e_pv_immessa_kwh_e_anno"] * 0.12 + 7500, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"],
                               bc["costo_gas_eur_anno"]
                               + bc["costo_rete_base_eur_anno"] + 2500, places=6)


class TestFinanza(unittest.TestCase):
    def test_p_gas_pareggio_demo_none_elettrico_supera_om(self):
        self.assertIsNone(mh841_demo_calcoli()["p_gas_pareggio"])
        self.assertIsNone(mh841_p_gas_pareggio(9910.0, 0.28, 1500.0, 0.12,
                                              7500, 72000.0, 2500, 120000.0))

    def test_p_gas_pareggio_none_casi(self):
        self.assertIsNone(mh841_p_gas_pareggio(9910.0, 0.28, 1500.0, 0.12,
                                              7500, 72000.0, 2500, 0.0))
        self.assertIsNone(mh841_p_gas_pareggio(9910.0, 0.28, 1500.0, 0.12,
                                              7500, 72000.0, 2500, 120000.0))
        self.assertAlmostEqual(mh841_p_gas_pareggio(9910.0, 0.28, 1500.0, 0.12,
                                             30000, 72000.0, 2500, 120000.0),
                         0.08279, places=12)

    def test_p_gas_pareggio_positivo_a_om_alt_alto(self):
        bc = mh841_calcola(**_demo_kwargs(om_alt=30000))
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.08279, places=12)

    def test_p_gas_pareggio_verifica_a_om_alt_alto(self):
        bc = mh841_calcola(**_demo_kwargs(om_alt=30000))
        pstar = bc["p_gas_pareggio"]
        r = mh841_calcola(**_demo_kwargs(om_alt=30000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_gas_pareggio_soglia_minima_a_om_alt_alto(self):
        bc = mh841_calcola(**_demo_kwargs(om_alt=30000))
        pstar = bc["p_gas_pareggio"]
        self.assertAlmostEqual(mh841_calcola(**_demo_kwargs(om_alt=30000, p_gas=pstar + 0.01))["risparmio_eur_anno"], 1200.0, places=6)
        self.assertAlmostEqual(mh841_calcola(**_demo_kwargs(om_alt=30000, p_gas=pstar - 0.01))["risparmio_eur_anno"], -1200.0, places=6)

    def test_risparmio_a_gas_nullo_resta_positivo_ma_non_convinte(self):
        r = mh841_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 12565.2, places=6)
        self.assertAlmostEqual(r["van"], -63409.834603916555, places=6)
        self.assertAlmostEqual(r["tir"], 1.301885408272764, places=6)
        self.assertEqual(r["payback"], 18)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh841_flussi(220000, 24565.2, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -220000)
        self.assertTrue(all(f == 24565.2 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh841_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 86136.68950656317, places=6)
        self.assertAlmostEqual(mh841_van([-220000] + [24565.2] * 20, 0.0), 271304.0, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh841_van([-220000] + [24565.2] * 20, 0.05), 86136.68950656317, places=6)
        self.assertLess(mh841_van([-220000] + [24565.2] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh841_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 9.269729665519828, places=6)
        self.assertGreater(bc["tir"], 9.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh841_payback([-220000] + [24565.2] * 20), 9)
        self.assertEqual(mh841_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh841_payback([-220000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh841_verdetto(24565.2, 100.0, 220000, 0.10), "CONVIENTE")
        self.assertEqual(mh841_verdetto(24565.2, -20000.0, 220000, 0.10), "MARGINALE")
        self.assertEqual(mh841_verdetto(24565.2, -100000.0, 220000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh841_verdetto(0.0, 100.0, 220000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh841_verdetto(-100.0, 100.0, 220000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh841_verdetto(None, 100.0, 220000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh841_verdetto(24565.2, 0.0, 220000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh841_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("box", "30"), ("box", float("nan")),
                            ("box", float("inf")), ("box", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh841_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"box": 0}, {"box": -1},
                     {"box": 30.5},
                     {"giorni_apertura": 0}, {"giorni_apertura": 300.5},
                     {"q_spec_termico": -0.1}, {"e_spec_elettrico": -0.1},
                     {"quota_illum": -0.1}, {"quota_illum": 1.1},
                     {"rid_led": -0.1}, {"rid_led": 1.1},
                     {"eta_caldaia": 0}, {"eta_caldaia": 1.1},
                     {"p_gas": -0.1}, {"p_rete": -0.1},
                     {"p_immissione": -0.1},
                     {"cop": 0}, {"cop": -1},
                     {"quota_diretta": -0.1}, {"quota_diretta": 1.1},
                     {"rte": 0}, {"rte": 1.1},
                     {"cap_batt": -1},
                     {"dod": -0.1}, {"dod": 1.1},
                     {"cicli_anno": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"om_base": -1}, {"om_alt": -1},
                     {"capex": -1}, {"f_co2_gas": -0.1},
                     {"f_co2_rete": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh841_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh841_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh841_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh841_valida(**_demo_kwargs(
            q_spec_termico=0, e_spec_elettrico=0,
            quota_illum=0, rid_led=0,
            p_gas=0, p_rete=0, p_immissione=0, quota_diretta=0, cap_batt=0, dod=0,
            cicli_anno=0, p_pv_kwp=0, prod_specifica=0,
            om_base=0, om_alt=0, capex=0, f_co2_gas=0,
            f_co2_rete=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh841_demo()
        self.assertEqual(d["box"], 30)
        self.assertEqual(d["giorni_apertura"], 300)
        self.assertEqual(d["q_spec_termico"], 12)
        self.assertEqual(d["e_spec_elettrico"], 8)
        self.assertEqual(d["quota_illum"], 0.40)
        self.assertEqual(d["rid_led"], 0.55)
        self.assertEqual(d["eta_caldaia"], 0.90)
        self.assertEqual(d["p_gas"], 0.10)
        self.assertEqual(d["p_rete"], 0.28)
        self.assertEqual(d["p_immissione"], 0.12)
        self.assertEqual(d["cop"], 3.0)
        self.assertEqual(d["quota_diretta"], 0.50)
        self.assertEqual(d["rte"], 0.90)
        self.assertEqual(d["cap_batt"], 150)
        self.assertEqual(d["dod"], 0.85)
        self.assertEqual(d["cicli_anno"], 300)
        self.assertEqual(d["p_pv_kwp"], 80)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["om_base"], 2500)
        self.assertEqual(d["om_alt"], 7500)
        self.assertEqual(d["capex"], 220000)
        self.assertEqual(d["f_co2_gas"], 0.202)
        self.assertEqual(d["f_co2_rete"], 0.30)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh841_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh841_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], 108000.0, places=6)
        self.assertEqual(bc["e_el_base_kwh_e_anno"], 72000.0)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], 36000.0, places=6)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 88000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 34660.0, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 10094.8, places=6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh841_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], -23478.4, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[9], 1086.8, places=6)

    def test_demo_tabella_righe(self):
        bc = mh841_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Box", voci)
        self.assertIn("Risparmio LED arena (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico netto da batteria (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico immesso, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Perdite round-trip batteria (kWh_e/anno)", voci)
        self.assertIn("Autonomia batteria (giorni)", voci)
        self.assertIn("Gas baseline (kWh/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("Prezzo gas di pareggio (EUR/kWh, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh841_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"],
                               bc["box"] * bc["giorni_apertura"] * bc["q_spec_termico"])
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] + bc["e_el_led_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_tot_alt_kwh_e_anno"] - bc["e_pv_autoconsumo_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        qterm = 30 * 300 * 12
        eelbase = 30 * 300 * 8
        eledr = eelbase * 0.40 * 0.55
        eel = eelbase - eledr
        epdc = qterm / 3.0
        etot = epdc + eel
        e_pv = 80 * 1100
        diretta = e_pv * 0.50
        batt_netta = min(e_pv * 0.50 * 0.90, 150 * 0.85 * 300)
        autoconsumo = min(diretta + batt_netta, etot)
        ciclata = batt_netta / 0.90
        perdite = ciclata - batt_netta
        immessa = e_pv - autoconsumo - perdite
        gasb = qterm / 0.90
        deficit = etot - autoconsumo
        c_base = gasb * 0.10 + eelbase * 0.28 + 2500
        c_alt = deficit * 0.28 - immessa * 0.12 + 7500
        bc = mh841_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], qterm, places=6)
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"], eelbase, places=6)
        self.assertAlmostEqual(bc["e_led_risparmio_kwh_e_anno"], eledr, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"], etot, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_pv_autoconsumo_kwh_e_anno"], autoconsumo, places=6)
        self.assertAlmostEqual(bc["e_pv_immessa_kwh_e_anno"], immessa, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh841_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_gas_piu_meno_20(self):
        meno = mh841_calcola(**_demo_kwargs(p_gas=0.08))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 22165.2, places=6)
        self.assertAlmostEqual(meno["van"], 56227.384684467295, places=6)
        self.assertAlmostEqual(meno["tir"], 7.85436943854864, places=6)
        self.assertEqual(meno["payback"], 10)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh841_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 26965.2, places=6)
        self.assertAlmostEqual(piu["van"], 116045.99432865909, places=6)
        self.assertAlmostEqual(piu["tir"], 10.632335696121737, places=6)
        self.assertEqual(piu["payback"], 9)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_gas_alto_migliora_il_caso(self):
        demo = mh841_demo_calcoli()
        meno = mh841_calcola(**_demo_kwargs(p_gas=0.08))
        piu = mh841_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_non_convinte(self):
        r = mh841_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 1355.2, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -203111.21254378988, places=6)
        self.assertAlmostEqual(r["tir"], -14.897168455972459, places=6)
        self.assertIsNone(r["payback"])

    def test_variante_senza_batteria_convinte(self):
        r = mh841_calcola(**_demo_kwargs(cap_batt=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 18955.2, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 16223.689484913808, places=6)
        self.assertAlmostEqual(r["tir"], 5.854843775527738, places=6)
        self.assertEqual(r["payback"], 12)

    def test_variante_senza_led_convinte(self):
        r = mh841_calcola(**_demo_kwargs(rid_led=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 20130.0, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 30864.294195329814, places=6)
        self.assertAlmostEqual(r["tir"], 6.602959393106913, places=6)
        self.assertEqual(r["payback"], 11)

    def test_variante_cop_basso_convinte(self):
        r = mh841_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 19525.2, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 23327.149380161576, places=6)
        self.assertAlmostEqual(r["tir"], 6.220397591745663, places=6)
        self.assertEqual(r["payback"], 12)

    def test_variante_capex_doppio_non_convinte(self):
        r = mh841_calcola(**_demo_kwargs(capex=440000))
        self.assertAlmostEqual(r["van"], -133863.31049343685, places=6)
        self.assertAlmostEqual(r["tir"], 1.0741610359037252, places=6)
        self.assertEqual(r["payback"], 18)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh841_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -30314.037117589272, places=6)
        self.assertAlmostEqual(r["tir"], 2.0572064932136382, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh841_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 271304.0, places=6)
        self.assertEqual(zero["payback"], 9)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh841_sensibilita(**mh841_demo())
        self.assertEqual(set(s.keys()), {"gas_meno20", "gas_piu20",
                                         "senza_pv", "senza_batt", "senza_led",
                                         "cop_2", "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["gas_meno20"]["risparmio_eur_anno"], 22165.2, places=6)
        self.assertAlmostEqual(s["gas_piu20"]["van"], 116045.99432865909, places=6)
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_batt"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_led"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh841_demo_calcoli()
        b = mh841_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh841_demo()
        attese = {"box", "giorni_apertura", "q_spec_termico",
                  "e_spec_elettrico", "quota_illum", "rid_led",
                  "eta_caldaia",
                  "p_gas", "p_rete", "p_immissione", "cop", "quota_diretta", "rte",
                  "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                  "prod_specifica", "om_base", "om_alt", "capex",
                  "f_co2_gas", "f_co2_rete", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["box", "giorni_apertura", "q_spec_termico",
                 "e_spec_elettrico", "quota_illum", "rid_led",
                 "eta_caldaia",
                 "p_gas", "p_rete", "p_immissione", "cop", "quota_diretta", "rte",
                 "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                 "prod_specifica", "om_base", "om_alt", "capex",
                 "f_co2_gas", "f_co2_rete", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh841_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(quota_illum=1.1))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(rid_led=1.1))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(quota_diretta=1.1))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(dod=1.1))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(rte=1.1))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh841_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("box", "30"), ("box", float("nan")),
                           ("capex", float("inf")), ("p_gas", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh841_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh841_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_diretta=0,
                                         cap_batt=0, dod=0, cicli_anno=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_gas=0,
                                         f_co2_rete=0, quota_illum=0,
                                         rid_led=0, p_gas=0, p_rete=0,
                                         p_immissione=0))
        self.assertTrue(r["valid"])
        r2 = mh841_calcola(**_demo_kwargs(om_alt=30000, p_gas=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh841_calcola(**_demo_kwargs(om_alt=60000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        bc = mh841_calcola(**_demo_kwargs(om_alt=30000))
        pstar = bc["p_gas_pareggio"]
        r = mh841_calcola(**_demo_kwargs(om_alt=30000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh841_demo_calcoli()
        csv = mh841_csv(bc, dict(mh841_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh841_demo_calcoli()
        csv = mh841_csv(bc, dict(mh841_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]), 24565.2, places=6)
        self.assertEqual(righe["p_gas_pareggio"], "")

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh841_demo_calcoli()
        csv = mh841_csv(bc, dict(mh841_demo()))
        for chiave in mh841_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh840_", src)
        self.assertNotIn("mh839_", src)
        self.assertNotIn("mh838_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab841:"), 1)
        self.assertTrue(src.startswith("    # W844"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Maneggio: fotovoltaico + batteria + pompa di calore + LED arena battono caldaia a gas + prelievo da rete per box, scuderie e maneggio coperto?", src)
        self.assertIn("🐴 Maneggio: fotovoltaico + batteria + pompa di calore + LED arena battono caldaia a gas + prelievo da rete per box, scuderie e maneggio coperto?", src)
        self.assertNotIn("tab840", src)
        self.assertNotIn("tab839", src)
        self.assertNotIn("tab838", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh840_", "mh839_", "mh838_", "mh837_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh840_", src)
        self.assertNotIn("st840_", src)
        self.assertNotIn("mh839_", src)
        self.assertNotIn("st839_", src)
        chiavi = re.findall(r'key="(st841_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st841_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st841_calcola"', src)
        self.assertIn('key="st841_csv"', src)
        self.assertIn('key="st841_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def841\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh841_demo().keys()), lette - set(mh841_demo().keys()))
        self.assertEqual(lette, set(mh841_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc841\['([^']+)'\]", src))
        attese = set(mh841_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg841"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
