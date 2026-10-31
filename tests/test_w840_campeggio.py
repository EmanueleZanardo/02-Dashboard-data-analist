"""Test nuova scheda tab840 "Campeggio:
fotovoltaico + batteria + pompa di calore
+ LED battono generatore diesel + caldaia
a gas per piazzole, servizi e piscina in
stagione?".

Business case stagionale di un campeggio
(150 giorni) guidato dal PRODOTTO piazzole
x giorni di stagione:
Q_term = piazzole x giorni x q_spec_termico;
E_el_base = piazzole x giorni x
e_spec_elettrico; E_led_risp = E_el_base x
quota_illum x rid_led (i LED tagliano solo
la quota illuminazione); E_el_led =
E_el_base - E_led_risp; E_pdc = Q_term /
COP; E_tot_alt = E_pdc + E_el_led; E_pv =
kWp x producibilita'; E_pv_diretta = E_pv x
quota_diretta; E_pv_batt_lordo = E_pv x
(1 - quota_diretta); E_pv_batt_netta =
min(lordo x RTE, cap_batt x DoD x
cicli_stagione) (cap stagionale di
throughput batteria); E_pv_servita =
min(diretta + netta, E_tot_alt);
E_pv_sprecata = E_pv - servito (eccesso +
perdite round-trip, NESSUN credito di
costo ne' di CO2: scelta conservativa
senza rete, niente rete in cui immettere);
E_diesel_residuo = E_tot_alt - servito;
autonomia_batt = cap_batt x DoD /
(E_tot_alt / giorni) (0 se domanda nulla);
litri_base_el = E_el_base / eta_gen / 9,9;
gas_base = Q_term / eta_caldaia;
costo_gas = gas_base x p_gas;
litri_residuo = E_diesel_residuo /
eta_gen / 9,9; C_base = litri_base_el x
p_diesel + costo_gas + O&M_base; C_alt =
litri_residuo x p_diesel + O&M_alt;
risparmio = C_base - C_alt; CO2 diesel base
= litri_base_el x f_co2_diesel / 1000; CO2
gas base = gas_base x f_co2_gas / 1000;
CO2 base = somma dei due; CO2 alt =
litri_residuo x f_co2_diesel / 1000; CO2
evitata = base - alt (segno libero, non
clampata: puo' essere negativa se il
diesel residuo supera la base);
flussi [-CAPEX, risparmio x vita]; VAN al
WACC (FRAZIONE, non percentuale); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo diesel di pareggio
p* = (O&M_alt - O&M_base - costo_gas) /
(litri_base_el - litri_residuo) in forma
chiusa a prezzo gas FERMO, None se
litri_base_el <= litri_residuo o se p* < 0,
SOGLIA MINIMA sui soli costi annui quando
esiste (sopra di essa l'alternativa vince,
sotto perde; il CAPEX non entra nel
pareggio annuo). Nel demo p* e' None: il
solo risparmio gas (21.600 EUR/stagione)
supera gia' il delta O&M (6.000), quindi
l'alternativa vince sui costi annui anche
a prezzo diesel nullo (risparmio 15.600).
Per COP NON viene dichiarato alcun
pareggio: il pareggio dichiarato qui e'
SOLO p_diesel_pareggio.
Verdetto: NON_CALCOLABILE se input
degenere (piazzole <= 0 o non intere,
giorni <= 0 o non interi, fabbisogni
specifici < 0, quota_illum < 0 o > 1,
rid_led < 0 o > 1, rendimenti <= 0 o > 1,
prezzi < 0, COP <= 0, quota_diretta < 0 o
> 1, RTE <= 0 o > 1, cap_batt < 0, DoD < 0
o > 1, cicli < 0, kWp < 0, producibilita'
< 0, O&M < 0, CAPEX < 0, fattori CO2 < 0,
WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e
CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza
FRAZIONE del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Guard UI
IDENTICA agli helper: nessuna divergenza
di verdetto. Tutti gli slider UI hanno
minimo 0, quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0
raggiungibili via slider sono bloccati in
UI esattamente come negli helper dove
previsto (piazzole, giorni, vita, COP,
rendimenti, RTE). Gli zeri ammessi in
entrambi (fabbisogni specifici, quote,
rid_led, prezzi, quota FV diretta,
cap_batt, DoD, cicli, kWp, producibilita',
O&M, CAPEX, fattori CO2, WACC, tolleranza)
non creano divergenza. Quote, rid_led e
DoD > 1 e rendimenti > 1 sono degeneri in
entrambi ma non raggiungibili via slider
(tetto 1,0). WACC sopra 0,20 e tolleranza
sopra 1,0 sono ammessi negli helper e
limitati solo dagli slider UI (0,20 e 1,0):
nessuna divergenza nel range raggiungibile,
perche' la guard controlla solo gli
stessi limiti degli helper. Distinzione
esplicita: distinto dall'albergo annuale
connesso alla rete (eccesso FV immesso e
valorizzato, domanda non stagionale: qui
150 giorni e senza rete, eccesso sprecato
senza credito) e dal rifugio alpino
off-grid (un unico combustibile trasportato
in quota, nessun LED ne' piscina: qui
diesel per l'elettricita' e gas per il
calore, piu' LED e piscina riscaldata):
qui driver piazzole x giorni + FV +
batteria + pompa di calore + LED + diesel
solo residuo.

Demo (campeggio): 80 piazzole, 150 giorni,
q_spec_termico 18 (Q_term 216.000
kWh_th/stagione), e_spec 6 (E_el_base
72.000 kWh_e/stagione), quota_illum 0,30
con rid_led 0,60 (risparmio LED 12.960,
E_el_led 59.040 kWh_e/stagione),
eta_gen 0,32, eta_caldaia 0,90, prezzo
diesel 1,90 EUR/l, prezzo gas 0,09
EUR/kWh, COP 3,2 (E_pdc 67.500,
E_tot_alt 126.540 kWh_e/stagione),
quota_diretta 0,45, RTE 0,90, batteria 200
kWh con DoD 0,85 e 150 cicli/stagione (cap
throughput 25.500 kWh_e/stagione),
fotovoltaico 120 kWp a 1.150
kWh/kWp/stagione (E_pv 138.000, diretta
62.100, batt lordo 75.900, batt netta
25.500, servito 87.600, sprecato 50.400
senza credito, diesel residuo 38.940
kWh_e/stagione, autonomia 0,20 giorni),
litri base el 22.727,27, gas base 240.000
kWh/stagione (costo gas 21.600), litri
residuo 12.291,67, O&M base 3.000, O&M alt
9.000, CAPEX 300.000 EUR, fattore CO2
diesel 2,68 kg/l, fattore CO2 gas 0,202
kg/kWh, WACC 0,05 (frazione), vita 20
anni, tolleranza 0,10 (frazione del
CAPEX).
Valori calcolati eseguendo
mh840_demo_calcoli(): Q_term 216000,0,
E_el_base 72000,0, E_led_risp 12960,0,
E_el_led 59040,0, E_pdc 67500,0,
E_tot_alt 126540,0, E_pv 138000,0,
diretta 62100,0, batt lordo 75900,0,
batt netta 25500,0, servito 87600,0,
sprecato 50400,0, diesel residuo 38940,0,
autonomia 0,20151730678046467, litri base
el 22727,272727272728, gas base 240000,0,
costo gas 21600,0, litri residuo
12291,666666666666, C_base
67781,81818181818, C_alt
32354,166666666664, risparmio
35427,65151515151, CO2 diesel base
60,909090909090914, CO2 gas base 48,48,
CO2 base 109,38909090909091, CO2 alt
32,94166666666666, CO2 evitata
76,44742424242425, VAN 141506,84512402344,
TIR 10,078819978913826 %, payback 9,
p_diesel_pareggio None (il solo risparmio
gas supera il delta O&M), verdetto
CONVIENTE (solido: VAN il 47,17 % del
CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab840 in app.py NON e'
incluso in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza in app.py spetta
alla fase di apply del worker, non a
questa fase. Tutti i test qui inclusi
passano da hidden_files senza app.py.

Destinazione nel repo: tests/test_w840_campeggio.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w843_helpers import (
        demo_calcoli,
        mh840_autonomia_batt,
        mh840_c_alt,
        mh840_c_base,
        mh840_calcola,
        mh840_co2_diesel,
        mh840_co2_evitata,
        mh840_co2_gas,
        mh840_costo_gas,
        mh840_csv,
        mh840_demo,
        mh840_demo_calcoli,
        mh840_e_el_base,
        mh840_e_el_led,
        mh840_e_led_risparmio,
        mh840_e_pdc,
        mh840_e_pv,
        mh840_e_tot_alt,
        mh840_eta,
        mh840_frazione,
        mh840_gas_kwh,
        mh840_int_pos,
        mh840_litri,
        mh840_nneg,
        mh840_num,
        mh840_p_diesel_pareggio,
        mh840_payback,
        mh840_pos,
        mh840_pv_batt_lordo,
        mh840_pv_batt_netta,
        mh840_pv_diretta,
        mh840_pv_servita,
        mh840_pv_servita_pot,
        mh840_pv_sprecata,
        mh840_q_termico,
        mh840_risparmio,
        mh840_sensibilita,
        mh840_tir,
        mh840_valida,
        mh840_van,
        mh840_verdetto,
        mh840_e_diesel_residuo,
        mh840_flussi,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w843_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w843_helpers", os.path.join(_hf, "w843_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh840_autonomia_batt = _mod.mh840_autonomia_batt
    mh840_c_alt = _mod.mh840_c_alt
    mh840_c_base = _mod.mh840_c_base
    mh840_calcola = _mod.mh840_calcola
    mh840_co2_diesel = _mod.mh840_co2_diesel
    mh840_co2_evitata = _mod.mh840_co2_evitata
    mh840_co2_gas = _mod.mh840_co2_gas
    mh840_costo_gas = _mod.mh840_costo_gas
    mh840_csv = _mod.mh840_csv
    mh840_demo = _mod.mh840_demo
    mh840_demo_calcoli = _mod.mh840_demo_calcoli
    mh840_e_el_base = _mod.mh840_e_el_base
    mh840_e_el_led = _mod.mh840_e_el_led
    mh840_e_led_risparmio = _mod.mh840_e_led_risparmio
    mh840_e_pdc = _mod.mh840_e_pdc
    mh840_e_pv = _mod.mh840_e_pv
    mh840_e_tot_alt = _mod.mh840_e_tot_alt
    mh840_eta = _mod.mh840_eta
    mh840_frazione = _mod.mh840_frazione
    mh840_gas_kwh = _mod.mh840_gas_kwh
    mh840_int_pos = _mod.mh840_int_pos
    mh840_litri = _mod.mh840_litri
    mh840_nneg = _mod.mh840_nneg
    mh840_num = _mod.mh840_num
    mh840_p_diesel_pareggio = _mod.mh840_p_diesel_pareggio
    mh840_payback = _mod.mh840_payback
    mh840_pos = _mod.mh840_pos
    mh840_pv_batt_lordo = _mod.mh840_pv_batt_lordo
    mh840_pv_batt_netta = _mod.mh840_pv_batt_netta
    mh840_pv_diretta = _mod.mh840_pv_diretta
    mh840_pv_servita = _mod.mh840_pv_servita
    mh840_pv_servita_pot = _mod.mh840_pv_servita_pot
    mh840_pv_sprecata = _mod.mh840_pv_sprecata
    mh840_q_termico = _mod.mh840_q_termico
    mh840_risparmio = _mod.mh840_risparmio
    mh840_sensibilita = _mod.mh840_sensibilita
    mh840_tir = _mod.mh840_tir
    mh840_valida = _mod.mh840_valida
    mh840_van = _mod.mh840_van
    mh840_verdetto = _mod.mh840_verdetto
    mh840_e_diesel_residuo = _mod.mh840_e_diesel_residuo
    mh840_flussi = _mod.mh840_flussi

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w843_helpers.py")
_UI_PATH = _risolvi("w843_ui.py")

_DEMO = {
    "q_termico_kwh_th_stagione": 216000.0,
    "e_el_base_kwh_e_stagione": 72000.0,
    "e_led_risparmio_kwh_e_stagione": 12960.0,
    "e_el_led_kwh_e_stagione": 59040.0,
    "e_pdc_kwh_e_stagione": 67500.0,
    "e_tot_alt_kwh_e_stagione": 126540.0,
    "e_pv_kwh_e_stagione": 138000.0,
    "e_pv_diretta_kwh_e_stagione": 62100.0,
    "e_pv_batt_lordo_kwh_e_stagione": 75900.0,
    "e_pv_batt_netta_kwh_e_stagione": 25500.0,
    "e_pv_servita_kwh_e_stagione": 87600.0,
    "e_pv_sprecata_kwh_e_stagione": 50400.0,
    "e_diesel_residuo_kwh_e_stagione": 38940.0,
    "autonomia_batt_giorni": 0.20151730678046467,
    "litri_base_el_l_stagione": 22727.272727272728,
    "gas_base_kwh_stagione": 240000.0,
    "costo_gas_eur_stagione": 21600.0,
    "litri_diesel_residuo_l_stagione": 12291.666666666666,
    "c_base_eur_stagione": 67781.81818181818,
    "c_alt_eur_stagione": 32354.166666666664,
    "risparmio_eur_stagione": 35427.65151515151,
    "co2_diesel_base_t_stagione": 60.909090909090914,
    "co2_gas_base_t_stagione": 48.48,
    "co2_base_t_stagione": 109.38909090909091,
    "co2_alt_t_stagione": 32.94166666666666,
    "co2_evitata_t_stagione": 76.44742424242425,
    "van": 141506.84512402344,
    "tir": 10.078819978913826,
    "payback": 9,
    "p_diesel_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh840_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh840_num(3, "x"), 3.0)
        self.assertEqual(mh840_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh840_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh840_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh840_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh840_pos(0, "x")
        with self.assertRaises(ValueError):
            mh840_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh840_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh840_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh840_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh840_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh840_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh840_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh840_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh840_frazione(0, "quota"), 0.0)
        self.assertEqual(mh840_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh840_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh840_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_termico_e_el_base_driver_piazzole_giorni(self):
        self.assertEqual(mh840_q_termico(80, 150, 18), 216000.0)
        self.assertEqual(mh840_e_el_base(80, 150, 6), 72000.0)

    def test_led_taglia_solo_quota_illuminazione(self):
        self.assertEqual(mh840_e_led_risparmio(72000.0, 0.30, 0.60), 12960.0)
        self.assertEqual(mh840_e_el_led(72000.0, 12960.0), 59040.0)
        self.assertEqual(mh840_e_led_risparmio(72000.0, 0.0, 0.60), 0.0)
        self.assertEqual(mh840_e_led_risparmio(72000.0, 0.30, 0.0), 0.0)
        self.assertEqual(mh840_e_led_risparmio(72000.0, 1.0, 1.0), 72000.0)

    def test_e_pdc_e_tot(self):
        self.assertAlmostEqual(mh840_e_pdc(216000.0, 3.2), 67500.0, places=6)
        self.assertAlmostEqual(mh840_e_tot_alt(67500.0, 59040.0), 126540.0, places=6)

    def test_pv_diretta_lordo(self):
        self.assertEqual(mh840_e_pv(120, 1150), 138000.0)
        self.assertEqual(mh840_pv_diretta(138000.0, 0.45), 62100.0)
        self.assertEqual(mh840_pv_batt_lordo(138000.0, 0.45), 75900.0)

    def test_batt_netta_cap_throughput_lega(self):
        self.assertEqual(mh840_pv_batt_netta(75900.0, 0.90, 200, 0.85, 150), 25500.0)
        self.assertEqual(mh840_pv_batt_netta(75900.0, 0.90, 10000, 0.85, 150), 68310.0)
        self.assertEqual(mh840_pv_batt_netta(75900.0, 0.90, 0, 0.85, 150), 0.0)

    def test_servita_cappata_a_domanda_e_sprecata(self):
        self.assertEqual(mh840_pv_servita_pot(62100.0, 25500.0), 87600.0)
        self.assertEqual(mh840_pv_servita(87600.0, 126540.0), 87600.0)
        self.assertEqual(mh840_pv_servita(200000.0, 126540.0), 126540.0)
        self.assertEqual(mh840_pv_sprecata(138000.0, 87600.0), 50400.0)

    def test_diesel_residuo_e_autonomia(self):
        self.assertAlmostEqual(mh840_e_diesel_residuo(126540.0, 87600.0), 38940.0, places=6)
        self.assertAlmostEqual(mh840_autonomia_batt(200, 0.85, 126540.0, 150), 0.20151730678046467, places=12)
        self.assertEqual(mh840_autonomia_batt(200, 0.85, 0, 150), 0.0)

    def test_litri_contenuto_9_9_e_gas(self):
        self.assertAlmostEqual(mh840_litri(72000.0, 0.32), 22727.272727272728, places=6)
        self.assertAlmostEqual(mh840_litri(38940.0, 0.32), 12291.666666666666, places=6)
        self.assertEqual(mh840_gas_kwh(216000.0, 0.90), 240000.0)
        self.assertEqual(mh840_costo_gas(240000.0, 0.09), 21600.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh840_c_base(22727.272727272728, 1.90, 21600.0, 3000), 67781.81818181818, places=6)
        self.assertAlmostEqual(mh840_c_alt(12291.666666666666, 1.90, 9000), 32354.166666666664, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh840_risparmio(67781.81818181818, 32354.166666666664), 35427.65151515151, places=6)
        self.assertLess(mh840_risparmio(32354.166666666664, 67781.81818181818), 0.0)

    def test_co2_due_fattori_e_evitata(self):
        self.assertAlmostEqual(mh840_co2_diesel(22727.272727272728, 2.68), 60.909090909090914, places=6)
        self.assertAlmostEqual(mh840_co2_gas(240000.0, 0.202), 48.48, places=6)
        self.assertAlmostEqual(mh840_co2_diesel(12291.666666666666, 2.68), 32.94166666666666, places=6)
        self.assertAlmostEqual(mh840_co2_evitata(109.38909090909091, 32.94166666666666), 76.44742424242425, places=6)

    def test_co2_evitata_negativa_non_clampata(self):
        self.assertAlmostEqual(mh840_co2_evitata(100.0, 200.0), -100.0, places=6)

    def test_sprecato_senza_credito(self):
        bc = mh840_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_sprecata_kwh_e_stagione"], 50400.0, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_stagione"],
                               bc["e_pv_servita_kwh_e_stagione"] + bc["e_pv_sprecata_kwh_e_stagione"], places=6)
        self.assertAlmostEqual(bc["c_alt_eur_stagione"],
                               bc["litri_diesel_residuo_l_stagione"] * 1.90 + 9000, places=6)
        self.assertAlmostEqual(bc["c_base_eur_stagione"],
                               bc["litri_base_el_l_stagione"] * 1.90 + bc["costo_gas_eur_stagione"] + 3000, places=6)


class TestFinanza(unittest.TestCase):
    def test_p_diesel_pareggio_demo_none_gas_supera_om(self):
        self.assertIsNone(mh840_demo_calcoli()["p_diesel_pareggio"])
        self.assertIsNone(mh840_p_diesel_pareggio(9000, 3000, 21600.0, 22727.272727272728, 12291.666666666666))

    def test_p_diesel_pareggio_none_casi(self):
        self.assertIsNone(mh840_p_diesel_pareggio(9000, 3000, 21600.0, 5000.0, 6000.0))
        self.assertIsNone(mh840_p_diesel_pareggio(9000, 3000, 21600.0, 5000.0, 5000.0))
        self.assertIsNone(mh840_p_diesel_pareggio(9000, 3000, 21600.0, 22727.272727272728, 12291.666666666666))
        self.assertEqual(mh840_p_diesel_pareggio(24600, 3000, 21600.0, 22727.272727272728, 12291.666666666666), 0.0)

    def test_p_diesel_pareggio_positivo_a_gas_basso(self):
        bc = mh840_calcola(**_demo_kwargs(p_gas=0.01))
        self.assertAlmostEqual(bc["p_diesel_pareggio"], 0.34497277676950994, places=12)

    def test_p_diesel_pareggio_verifica_su_gas_basso(self):
        bc = mh840_calcola(**_demo_kwargs(p_gas=0.01))
        pstar = bc["p_diesel_pareggio"]
        r = mh840_calcola(**_demo_kwargs(p_gas=0.01, p_diesel=pstar))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_diesel_pareggio_soglia_minima_su_gas_basso(self):
        bc = mh840_calcola(**_demo_kwargs(p_gas=0.01))
        pstar = bc["p_diesel_pareggio"]
        self.assertAlmostEqual(mh840_calcola(**_demo_kwargs(p_gas=0.01, p_diesel=pstar + 0.10))["risparmio_eur_stagione"], 1043.560606060606, places=6)
        self.assertAlmostEqual(mh840_calcola(**_demo_kwargs(p_gas=0.01, p_diesel=pstar - 0.10))["risparmio_eur_stagione"], -1043.560606060606, places=6)

    def test_risparmio_a_diesel_nullo_resta_positivo(self):
        r = mh840_calcola(**_demo_kwargs(p_diesel=0.0))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], 15600.0, places=6)
        self.assertAlmostEqual(r["van"], -105589.51865637631, places=6)
        self.assertEqual(r["payback"], 20)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh840_flussi(300000, 35427.65151515151, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -300000)
        self.assertTrue(all(f == 35427.65151515151 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh840_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 141506.84512402344, places=6)
        self.assertAlmostEqual(mh840_van([-300000] + [35427.65151515151] * 20, 0.0), 408553.0303030302, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh840_van([-300000] + [35427.65151515151] * 20, 0.05), 141506.84512402344, places=6)
        self.assertLess(mh840_van([-300000] + [35427.65151515151] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh840_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 10.078819978913826, places=6)
        self.assertGreater(bc["tir"], 10.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh840_payback([-300000] + [35427.65151515151] * 20), 9)
        self.assertEqual(mh840_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh840_payback([-300000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh840_verdetto(35427.65151515151, 100.0, 300000, 0.10), "CONVIENTE")
        self.assertEqual(mh840_verdetto(35427.65151515151, -20000.0, 300000, 0.10), "MARGINALE")
        self.assertEqual(mh840_verdetto(35427.65151515151, -100000.0, 300000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh840_verdetto(0.0, 100.0, 300000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh840_verdetto(-100.0, 100.0, 300000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh840_verdetto(None, 100.0, 300000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh840_verdetto(35427.65151515151, 0.0, 300000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh840_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("piazzole", "80"), ("piazzole", float("nan")),
                            ("piazzole", float("inf")), ("piazzole", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh840_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"piazzole": 0}, {"piazzole": -1},
                     {"piazzole": 80.5},
                     {"giorni_stagione": 0}, {"giorni_stagione": 150.5},
                     {"q_spec_termico": -0.1}, {"e_spec_elettrico": -0.1},
                     {"quota_illum": -0.1}, {"quota_illum": 1.1},
                     {"rid_led": -0.1}, {"rid_led": 1.1},
                     {"eta_gen": 0}, {"eta_gen": 1.1},
                     {"eta_caldaia": 0}, {"eta_caldaia": 1.1},
                     {"p_diesel": -0.1}, {"p_gas": -0.1},
                     {"cop": 0}, {"cop": -1},
                     {"quota_diretta": -0.1}, {"quota_diretta": 1.1},
                     {"rte": 0}, {"rte": 1.1},
                     {"cap_batt": -1},
                     {"dod": -0.1}, {"dod": 1.1},
                     {"cicli_anno": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"om_base": -1}, {"om_alt": -1},
                     {"capex": -1}, {"f_co2_diesel": -0.1},
                     {"f_co2_gas": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh840_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh840_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh840_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh840_valida(**_demo_kwargs(
            q_spec_termico=0, e_spec_elettrico=0,
            quota_illum=0, rid_led=0,
            p_diesel=0, p_gas=0, quota_diretta=0, cap_batt=0, dod=0,
            cicli_anno=0, p_pv_kwp=0, prod_specifica=0,
            om_base=0, om_alt=0, capex=0, f_co2_diesel=0,
            f_co2_gas=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh840_demo()
        self.assertEqual(d["piazzole"], 80)
        self.assertEqual(d["giorni_stagione"], 150)
        self.assertEqual(d["q_spec_termico"], 18)
        self.assertEqual(d["e_spec_elettrico"], 6)
        self.assertEqual(d["quota_illum"], 0.30)
        self.assertEqual(d["rid_led"], 0.60)
        self.assertEqual(d["eta_gen"], 0.32)
        self.assertEqual(d["eta_caldaia"], 0.90)
        self.assertEqual(d["p_diesel"], 1.90)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["cop"], 3.2)
        self.assertEqual(d["quota_diretta"], 0.45)
        self.assertEqual(d["rte"], 0.90)
        self.assertEqual(d["cap_batt"], 200)
        self.assertEqual(d["dod"], 0.85)
        self.assertEqual(d["cicli_anno"], 150)
        self.assertEqual(d["p_pv_kwp"], 120)
        self.assertEqual(d["prod_specifica"], 1150)
        self.assertEqual(d["om_base"], 3000)
        self.assertEqual(d["om_alt"], 9000)
        self.assertEqual(d["capex"], 300000)
        self.assertEqual(d["f_co2_diesel"], 2.68)
        self.assertEqual(d["f_co2_gas"], 0.202)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh840_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh840_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_stagione"], 216000.0, places=6)
        self.assertEqual(bc["e_el_base_kwh_e_stagione"], 72000.0)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_stagione"], 67500.0, places=6)
        self.assertEqual(bc["e_pv_kwh_e_stagione"], 138000.0)
        self.assertAlmostEqual(bc["c_base_eur_stagione"], 67781.81818181818, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_stagione"], 32354.166666666664, places=6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh840_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], -16578.787878787887, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[9], 18848.863636363625, places=6)

    def test_demo_tabella_righe(self):
        bc = mh840_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Piazzole", voci)
        self.assertIn("Risparmio LED (kWh_e/stagione)", voci)
        self.assertIn("Fotovoltaico netto da batteria (kWh_e/stagione)", voci)
        self.assertIn("Fotovoltaico sprecato, senza credito (kWh_e/stagione)", voci)
        self.assertIn("Autonomia batteria (giorni)", voci)
        self.assertIn("Gas baseline (kWh/stagione)", voci)
        self.assertIn("Litri diesel residuo (l/stagione)", voci)
        self.assertIn("Prezzo diesel di pareggio (EUR/l, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh840_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_stagione"],
                               bc["piazzole"] * bc["giorni_stagione"] * bc["q_spec_termico"])
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_stagione"],
                               bc["e_pdc_kwh_e_stagione"] + bc["e_el_led_kwh_e_stagione"])
        self.assertAlmostEqual(bc["e_diesel_residuo_kwh_e_stagione"],
                               bc["e_tot_alt_kwh_e_stagione"] - bc["e_pv_servita_kwh_e_stagione"])
        self.assertAlmostEqual(bc["risparmio_eur_stagione"],
                               bc["c_base_eur_stagione"] - bc["c_alt_eur_stagione"])
        self.assertAlmostEqual(bc["co2_evitata_t_stagione"],
                               bc["co2_base_t_stagione"] - bc["co2_alt_t_stagione"])

    def test_demo_contro_riconteggio_indipendente(self):
        qterm = 80 * 150 * 18
        eelbase = 80 * 150 * 6
        eledr = eelbase * 0.30 * 0.60
        eel = eelbase - eledr
        epdc = qterm / 3.2
        etot = epdc + eel
        e_pv = 120 * 1150
        diretta = e_pv * 0.45
        batt_netta = min(e_pv * 0.55 * 0.90, 200 * 0.85 * 150)
        servita = min(diretta + batt_netta, etot)
        lit_el = eelbase / 0.32 / 9.9
        gasb = qterm / 0.90
        lit_res = (etot - servita) / 0.32 / 9.9
        c_base = lit_el * 1.90 + gasb * 0.09 + 3000
        c_alt = lit_res * 1.90 + 9000
        bc = mh840_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_stagione"], qterm, places=6)
        self.assertAlmostEqual(bc["e_el_base_kwh_e_stagione"], eelbase, places=6)
        self.assertAlmostEqual(bc["e_led_risparmio_kwh_e_stagione"], eledr, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_stagione"], epdc, places=6)
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_stagione"], etot, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_stagione"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_pv_servita_kwh_e_stagione"], servita, places=6)
        self.assertAlmostEqual(bc["c_base_eur_stagione"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_stagione"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_stagione"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh840_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_stagione"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_diesel_piu_meno_20(self):
        meno = mh840_calcola(**_demo_kwargs(p_diesel=1.52))
        self.assertAlmostEqual(meno["risparmio_eur_stagione"], 31462.121212121212, places=6)
        self.assertAlmostEqual(meno["van"], 92087.57236794355, places=6)
        self.assertAlmostEqual(meno["tir"], 8.396235457891233, places=6)
        self.assertEqual(meno["payback"], 10)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh840_calcola(**_demo_kwargs(p_diesel=2.28))
        self.assertAlmostEqual(piu["risparmio_eur_stagione"], 39393.18181818182, places=6)
        self.assertAlmostEqual(piu["van"], 190926.11788010344, places=6)
        self.assertAlmostEqual(piu["tir"], 11.692984403704767, places=6)
        self.assertEqual(piu["payback"], 8)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_diesel_alto_migliora_il_caso(self):
        demo = mh840_demo_calcoli()
        meno = mh840_calcola(**_demo_kwargs(p_diesel=1.52))
        piu = mh840_calcola(**_demo_kwargs(p_diesel=2.28))
        self.assertLess(meno["risparmio_eur_stagione"], demo["risparmio_eur_stagione"])
        self.assertGreater(piu["risparmio_eur_stagione"], demo["risparmio_eur_stagione"])
        self.assertGreater(demo["litri_base_el_l_stagione"], demo["litri_diesel_residuo_l_stagione"])

    def test_variante_senza_fotovoltaico_non_calcolabile(self):
        r = mh840_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], -17110.227272727265, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["van"], -513231.2512813915, places=6)
        self.assertIsNone(r["tir"])
        self.assertIsNone(r["payback"])

    def test_variante_senza_batteria_non_convinte(self):
        r = mh840_calcola(**_demo_kwargs(cap_batt=0))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], 20134.090909090904, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -49084.72403508713, places=6)
        self.assertAlmostEqual(r["tir"], 2.9835684402198095, places=6)
        self.assertEqual(r["payback"], 15)

    def test_variante_senza_led_convinte(self):
        r = mh840_calcola(**_demo_kwargs(rid_led=0))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], 27654.92424242424, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 44641.48291609903, places=6)
        self.assertAlmostEqual(r["tir"], 6.697207684328589, places=6)
        self.assertEqual(r["payback"], 11)

    def test_variante_cop_basso_non_convinte(self):
        r = mh840_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], 11137.878787878784, places=6)
        self.assertAlmostEqual(r["van"], -161197.41177574036, places=6)
        self.assertAlmostEqual(r["tir"], -2.6818798392042167, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_capex_doppio_non_convinte(self):
        r = mh840_calcola(**_demo_kwargs(capex=600000))
        self.assertAlmostEqual(r["van"], -158493.15487597662, places=6)
        self.assertAlmostEqual(r["tir"], 1.6388506654599808, places=6)
        self.assertEqual(r["payback"], 17)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_marginale(self):
        r = mh840_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -26437.06583646736, places=6)
        self.assertAlmostEqual(r["tir"], 3.1437552536436293, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertEqual(r["verdetto"], "MARGINALE")

    def test_variante_wacc_zero(self):
        zero = mh840_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 408553.0303030302, places=6)
        self.assertEqual(zero["payback"], 9)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh840_sensibilita(**mh840_demo())
        self.assertEqual(set(s.keys()), {"diesel_meno20", "diesel_piu20",
                                         "senza_pv", "senza_batt", "senza_led",
                                         "cop_2", "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["diesel_meno20"]["risparmio_eur_stagione"], 31462.121212121212, places=6)
        self.assertAlmostEqual(s["diesel_piu20"]["van"], 190926.11788010344, places=6)
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(s["senza_batt"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_led"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "MARGINALE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh840_demo_calcoli()
        b = mh840_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh840_demo()
        attese = {"piazzole", "giorni_stagione", "q_spec_termico",
                  "e_spec_elettrico", "quota_illum", "rid_led",
                  "eta_gen", "eta_caldaia",
                  "p_diesel", "p_gas", "cop", "quota_diretta", "rte",
                  "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                  "prod_specifica", "om_base", "om_alt", "capex",
                  "f_co2_diesel", "f_co2_gas", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["piazzole", "giorni_stagione", "q_spec_termico",
                 "e_spec_elettrico", "quota_illum", "rid_led",
                 "eta_gen", "eta_caldaia",
                 "p_diesel", "p_gas", "cop", "quota_diretta", "rte",
                 "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                 "prod_specifica", "om_base", "om_alt", "capex",
                 "f_co2_diesel", "f_co2_gas", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh840_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(quota_illum=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(rid_led=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(quota_diretta=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(dod=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(eta_gen=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(rte=1.1))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh840_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("piazzole", "80"), ("piazzole", float("nan")),
                           ("capex", float("inf")), ("p_diesel", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh840_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh840_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_diretta=0,
                                         cap_batt=0, dod=0, cicli_anno=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_diesel=0,
                                         f_co2_gas=0, quota_illum=0,
                                         rid_led=0, p_gas=0))
        self.assertTrue(r["valid"])
        r2 = mh840_calcola(**_demo_kwargs(om_alt=30000, p_diesel=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh840_calcola(**_demo_kwargs(om_alt=60000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_stagione"], 0.0)

    def test_pareggio_esatto_soglia(self):
        bc = mh840_calcola(**_demo_kwargs(p_gas=0.01))
        pstar = bc["p_diesel_pareggio"]
        r = mh840_calcola(**_demo_kwargs(p_gas=0.01, p_diesel=pstar))
        self.assertAlmostEqual(r["risparmio_eur_stagione"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh840_demo_calcoli()
        csv = mh840_csv(bc, dict(mh840_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh840_demo_calcoli()
        csv = mh840_csv(bc, dict(mh840_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_stagione"]), 35427.65151515151, places=6)
        self.assertEqual(righe["p_diesel_pareggio"], "")

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh840_demo_calcoli()
        csv = mh840_csv(bc, dict(mh840_demo()))
        for chiave in mh840_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh839_", src)
        self.assertNotIn("mh838_", src)
        self.assertNotIn("mh837_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab840:"), 1)
        self.assertTrue(src.startswith("    # W843"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Campeggio: fotovoltaico + batteria + pompa di calore + LED battono generatore diesel + caldaia a gas per piazzole, servizi e piscina in stagione?", src)
        self.assertIn("🏕️ Campeggio: fotovoltaico + batteria + pompa di calore + LED battono generatore diesel + caldaia a gas per piazzole, servizi e piscina in stagione?", src)
        self.assertNotIn("tab839", src)
        self.assertNotIn("tab838", src)
        self.assertNotIn("tab837", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh839_", "mh838_", "mh837_", "mh836_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh839_", src)
        self.assertNotIn("st839_", src)
        self.assertNotIn("mh838_", src)
        self.assertNotIn("st838_", src)
        chiavi = re.findall(r'key="(st840_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st840_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st840_calcola"', src)
        self.assertIn('key="st840_csv"', src)
        self.assertIn('key="st840_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def840\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh840_demo().keys()), lette - set(mh840_demo().keys()))
        self.assertEqual(lette, set(mh840_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc840\['([^']+)'\]", src))
        attese = set(mh840_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg840"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_stagione"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
