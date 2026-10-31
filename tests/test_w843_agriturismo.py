"""Test nuova scheda tab843 "Agriturismo:
fotovoltaico + batteria + pompa di
calore + solare termico battono caldaia
a gas + prelievo da rete per camere e
ristorante?".

Business case annuo di un agriturismo
(camere + ristorante) connesso alla
rete, 280 giorni di apertura, guidato
da CAMERE x GIORNI x OCCUPAZIONE
(pernottamenti) + COPERTI x GIORNI
(coperti totali), NON dalla superficie:
pernottamenti = camere x giorni x
occupazione; coperti_totali =
coperti_giorno x giorni; Q_term =
pernottamenti x q_term_pernot +
coperti_totali x q_term_coperto;
E_el_base = pernottamenti x e_pernot
+ coperti_totali x e_coperto;
Q_solare = min(coll_mq x resa_solare,
Q_term) (il solare termico copre per
primo, cappato al fabbisogno);
Q_residuo = Q_term - Q_solare;
E_pdc = Q_residuo / COP (solo il
residuo, non tutto Q_term);
E_tot_alt = E_pdc + E_el_base;
E_pv = kWp x producibilita';
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
la rete esiste); autonomia_batt =
cap_batt x DoD / (E_tot_alt / giorni)
(0 se domanda nulla); gas_base = Q_term /
eta_caldaia (baseline: caldaia su TUTTO
Q_term, solare termico assente);
costo_gas = gas_base x p_gas;
prelievo rete base = E_el_base x p_rete;
C_base = costo_gas + prelievo rete base
+ O&M_base; C_alt = deficit x p_rete -
immessa x p_immissione + O&M_alt
(l'immissione e' un ricavo, segno
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
elettrica piu' l'immissione);
flussi [-CAPEX, risparmio x vita]; VAN al
WACC (FRAZIONE, non percentuale); TIR per
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
il risparmio resterebbe 12.913,73
EUR/anno (solo elettrico netto + O&M),
quindi l'alternativa vince sui costi
annui anche a gas gratis.
Verdetto: NON_CALCOLABILE se input
degenere (camere <= 0 o non intere,
giorni <= 0 o non interi, occupazione
< 0 o > 1, coperti_giorno < 0,
fabbisogni specifici < 0, eta_caldaia
<= 0 o > 1, prezzi < 0, COP <= 0,
quota_diretta < 0 o > 1, RTE <= 0 o > 1,
cap_batt < 0, DoD < 0 o > 1, cicli < 0,
kWp < 0, producibilita' < 0, coll_mq < 0,
resa_solare < 0, O&M < 0, CAPEX < 0,
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
previsto (camere, giorni, vita, COP,
eta_caldaia, RTE). Gli zeri ammessi in
entrambi (occupazione, coperti_giorno,
fabbisogni specifici, prezzi, quota FV
diretta, cap_batt, DoD, cicli, kWp,
producibilita', coll_mq, resa_solare,
O&M, CAPEX, fattori CO2, WACC,
tolleranza) non creano divergenza.
Quote, DoD e occupazione > 1 e
eta_caldaia > 1 sono degeneri in entrambi
ma non raggiungibili via slider (tetto
1,0). WACC sopra 0,20 e tolleranza sopra
1,0 sono ammessi negli helper e limitati
solo dagli slider UI (0,20 e 1,0):
nessuna divergenza nel range
raggiungibile, perche' la guard controlla
solo gli stessi limiti degli helper.
Distinzione esplicita: distinto
dall'autosalone (driver superficie in mq
piu' ricarica EV veicoli x giorni x kWh,
senza solare termico e senza
pernottamenti: qui driver camere x
giorni x occupazione piu' coperti x
giorni, e il solare termico copre per
primo parte del calore) e dal campeggio
stagionale off-grid (senza rete, eccesso
FV sprecato senza credito: qui con rete,
eccesso immesso e pagato, deficit
prelevato a prezzo pieno).

Demo (agriturismo): 14 camere, 280
giorni, occupazione 0,65 (pernottamenti
2.548 notti/anno), 60 coperti/giorno
(coperti totali 16.800 coperti/anno),
q_term_pernot 20 (50.960 kWh_th/anno
camere), q_term_coperto 2,5 (42.000
kWh_th/anno ristorante, Q_term 92.960),
e_pernot 15 (38.220 kWh_e/anno),
e_coperto 2,0 (33.600 kWh_e/anno,
E_el_base 71.820), eta_caldaia 0,90,
prezzo gas 0,10 EUR/kWh, prezzo prelievo
rete 0,28 EUR/kWh, prezzo immissione
0,12 EUR/kWh, COP 3,0, solare termico
40 mq a 450 kWh_th/mq/anno (Q_solare
18.000, residuo 74.960, E_pdc
24.986,666666666668, E_tot_alt
96.806,66666666667), quota_diretta 0,50,
RTE 0,90, batteria 150 kWh con DoD 0,85
e 300 cicli/anno (cap throughput 38.250
kWh_e/anno), fotovoltaico 90 kWp a 1.100
kWh/kWp/anno (E_pv 99.000, diretta
49.500, batt lordo 49.500, batt netta
38.250, servita potenziale 87.750,
autoconsumo 87.750, deficit 9.056,666666666672,
ciclata 42.500, perdite batt 4.250,
immessa 7.000 con ricavo 840 EUR/anno,
autonomia 0,3687762550788513 giorni),
gas base 103.288,88888888889 kWh/anno
(costo gas 10.328,88888888889, prelievo
rete base 20.109,600000000002), O&M base
2.500, O&M alt 8.000, CAPEX 250.000 EUR,
fattore CO2 gas 0,202 kg/kWh, fattore
CO2 rete 0,30 kg/kWh_e, WACC 0,05
(frazione), vita 20 anni, tolleranza
0,10 (frazione del CAPEX).
Valori calcolati eseguendo
mh843_demo_calcoli(): Q_term 92960,0,
Q_solare 18000,0, Q_residuo 74960,0,
E_el_base 71820,0, E_pdc
24986,666666666668, E_tot_alt
96806,66666666667, E_pv 99000,0,
diretta 49500,0, batt lordo 49500,0,
batt netta 38250,0, servita pot
87750,0, autoconsumo 87750,0, deficit
9056,666666666672, ciclata 42500,0,
perdite batt 4250,0, immessa 7000,0,
autonomia 0,3687762550788513, gas base
103288,88888888889, costo gas
10328,88888888889, prelievo rete base
20109,600000000002, C_base
32938,488888888896, C_alt
9695,866666666669, risparmio
23242,622222222228, CO2 gas base
20,86435555555556, CO2 rete base
21,546, CO2 base 42,410355555555554,
CO2 alt 0,6170000000000014, CO2 evitata
41,79335555555555, VAN
39654,44704552741, TIR
6,805463949066333 %, payback 11,
p_gas_pareggio None (a gas nullo il
risparmio resterebbe 12.913,73 EUR/anno),
verdetto CONVIENTE (VAN il 15,86 % del
CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab843 in app.py NON e'
incluso in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza in app.py spetta
alla fase di apply del worker, non a
questa fase. Tutti i test qui inclusi
passano da hidden_files senza app.py.

Destinazione nel repo: tests/test_w843_agriturismo.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w846_helpers import (
        demo_calcoli,
        mh843_autonomia_batt,
        mh843_c_alt,
        mh843_c_base,
        mh843_calcola,
        mh843_co2_evitata,
        mh843_co2_gas,
        mh843_co2_rete,
        mh843_coperti_totali,
        mh843_costo_gas,
        mh843_costo_rete_base,
        mh843_csv,
        mh843_demo,
        mh843_demo_calcoli,
        mh843_e_deficit,
        mh843_e_el_base,
        mh843_e_pdc,
        mh843_e_pv,
        mh843_e_tot_alt,
        mh843_eta,
        mh843_frazione,
        mh843_flussi,
        mh843_gas_kwh,
        mh843_int_pos,
        mh843_nneg,
        mh843_num,
        mh843_p_gas_pareggio,
        mh843_payback,
        mh843_pernottamenti,
        mh843_pos,
        mh843_pv_autoconsumo,
        mh843_pv_batt_ciclata,
        mh843_pv_batt_lordo,
        mh843_pv_batt_netta,
        mh843_pv_diretta,
        mh843_pv_immessa,
        mh843_pv_perdite_batt,
        mh843_pv_servita_pot,
        mh843_q_residuo,
        mh843_q_solare,
        mh843_q_termico,
        mh843_risparmio,
        mh843_sensibilita,
        mh843_tir,
        mh843_valida,
        mh843_van,
        mh843_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w846_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w846_helpers", os.path.join(_hf, "w846_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh843_autonomia_batt = _mod.mh843_autonomia_batt
    mh843_c_alt = _mod.mh843_c_alt
    mh843_c_base = _mod.mh843_c_base
    mh843_calcola = _mod.mh843_calcola
    mh843_co2_evitata = _mod.mh843_co2_evitata
    mh843_co2_gas = _mod.mh843_co2_gas
    mh843_co2_rete = _mod.mh843_co2_rete
    mh843_coperti_totali = _mod.mh843_coperti_totali
    mh843_costo_gas = _mod.mh843_costo_gas
    mh843_costo_rete_base = _mod.mh843_costo_rete_base
    mh843_csv = _mod.mh843_csv
    mh843_demo = _mod.mh843_demo
    mh843_demo_calcoli = _mod.mh843_demo_calcoli
    mh843_e_deficit = _mod.mh843_e_deficit
    mh843_e_el_base = _mod.mh843_e_el_base
    mh843_e_pdc = _mod.mh843_e_pdc
    mh843_e_pv = _mod.mh843_e_pv
    mh843_e_tot_alt = _mod.mh843_e_tot_alt
    mh843_eta = _mod.mh843_eta
    mh843_frazione = _mod.mh843_frazione
    mh843_flussi = _mod.mh843_flussi
    mh843_gas_kwh = _mod.mh843_gas_kwh
    mh843_int_pos = _mod.mh843_int_pos
    mh843_nneg = _mod.mh843_nneg
    mh843_num = _mod.mh843_num
    mh843_p_gas_pareggio = _mod.mh843_p_gas_pareggio
    mh843_payback = _mod.mh843_payback
    mh843_pernottamenti = _mod.mh843_pernottamenti
    mh843_pos = _mod.mh843_pos
    mh843_pv_autoconsumo = _mod.mh843_pv_autoconsumo
    mh843_pv_batt_ciclata = _mod.mh843_pv_batt_ciclata
    mh843_pv_batt_lordo = _mod.mh843_pv_batt_lordo
    mh843_pv_batt_netta = _mod.mh843_pv_batt_netta
    mh843_pv_diretta = _mod.mh843_pv_diretta
    mh843_pv_immessa = _mod.mh843_pv_immessa
    mh843_pv_perdite_batt = _mod.mh843_pv_perdite_batt
    mh843_pv_servita_pot = _mod.mh843_pv_servita_pot
    mh843_q_residuo = _mod.mh843_q_residuo
    mh843_q_solare = _mod.mh843_q_solare
    mh843_q_termico = _mod.mh843_q_termico
    mh843_risparmio = _mod.mh843_risparmio
    mh843_sensibilita = _mod.mh843_sensibilita
    mh843_tir = _mod.mh843_tir
    mh843_valida = _mod.mh843_valida
    mh843_van = _mod.mh843_van
    mh843_verdetto = _mod.mh843_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w846_helpers.py")
_UI_PATH = _risolvi("w846_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# tab precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "2_"
_VECCHIO_TAB = "tab84" + "2"
_VECCHIO_ST = "st84" + "2_"

_DEMO = {
    "pernottamenti": 2548.0,
    "coperti_totali": 16800.0,
    "q_termico_kwh_th_anno": 92960.0,
    "q_solare_kwh_th_anno": 18000.0,
    "q_residuo_kwh_th_anno": 74960.0,
    "e_el_base_kwh_e_anno": 71820.0,
    "e_pdc_kwh_e_anno": 24986.666666666668,
    "e_tot_alt_kwh_e_anno": 96806.66666666667,
    "e_pv_kwh_e_anno": 99000.0,
    "e_pv_diretta_kwh_e_anno": 49500.0,
    "e_pv_batt_lordo_kwh_e_anno": 49500.0,
    "e_pv_batt_netta_kwh_e_anno": 38250.0,
    "e_pv_servita_pot_kwh_e_anno": 87750.0,
    "e_pv_autoconsumo_kwh_e_anno": 87750.0,
    "e_deficit_kwh_e_anno": 9056.666666666672,
    "e_pv_batt_ciclata_kwh_e_anno": 42500.0,
    "e_pv_perdite_batt_kwh_e_anno": 4250.0,
    "e_pv_immessa_kwh_e_anno": 7000.0,
    "autonomia_batt_giorni": 0.3687762550788513,
    "gas_base_kwh_anno": 103288.88888888889,
    "costo_gas_eur_anno": 10328.88888888889,
    "costo_rete_base_eur_anno": 20109.600000000002,
    "c_base_eur_anno": 32938.488888888896,
    "c_alt_eur_anno": 9695.866666666669,
    "risparmio_eur_anno": 23242.622222222228,
    "co2_gas_base_t_anno": 20.86435555555556,
    "co2_rete_base_t_anno": 21.546,
    "co2_base_t_anno": 42.410355555555554,
    "co2_alt_t_anno": 0.6170000000000014,
    "co2_evitata_t_anno": 41.79335555555555,
    "van": 39654.44704552741,
    "tir": 6.805463949066333,
    "payback": 11,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh843_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh843_num(3, "x"), 3.0)
        self.assertEqual(mh843_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh843_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh843_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh843_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh843_pos(0, "x")
        with self.assertRaises(ValueError):
            mh843_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh843_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh843_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh843_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh843_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh843_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh843_int_pos(14.0, "camere"), 14)
        with self.assertRaises(ValueError):
            mh843_int_pos(14.5, "camere")

    def test_frazione_limiti(self):
        self.assertEqual(mh843_frazione(0, "occupazione"), 0.0)
        self.assertEqual(mh843_frazione(1, "occupazione"), 1.0)
        with self.assertRaises(ValueError):
            mh843_frazione(-0.1, "occupazione")
        with self.assertRaises(ValueError):
            mh843_frazione(1.1, "occupazione")


class TestFisica(unittest.TestCase):
    def test_pernottamenti_e_coperti_driver(self):
        self.assertEqual(mh843_pernottamenti(14, 280, 0.65), 2548.0)
        self.assertEqual(mh843_pernottamenti(14, 280, 0), 0.0)
        self.assertEqual(mh843_coperti_totali(60, 280), 16800.0)
        self.assertEqual(mh843_coperti_totali(0, 280), 0.0)

    def test_q_termico_e_el_base_pernot_coperti(self):
        self.assertEqual(mh843_q_termico(2548.0, 20, 16800.0, 2.5), 92960.0)
        self.assertEqual(mh843_e_el_base(2548.0, 15, 16800.0, 2.0), 71820.0)

    def test_solare_copre_per_primo_e_residuo_a_pdc(self):
        self.assertEqual(mh843_q_solare(40, 450, 92960.0), 18000.0)
        self.assertEqual(mh843_q_solare(500, 450, 92960.0), 92960.0)
        self.assertEqual(mh843_q_solare(0, 450, 92960.0), 0.0)
        self.assertEqual(mh843_q_residuo(92960.0, 18000.0), 74960.0)
        self.assertAlmostEqual(mh843_e_pdc(74960.0, 3.0), 24986.666666666668, places=6)
        self.assertAlmostEqual(mh843_e_pdc(92960.0, 3.0), 30986.666666666668, places=6)
        self.assertAlmostEqual(mh843_e_tot_alt(24986.666666666668, 71820.0), 96806.66666666667, places=6)

    def test_pv_diretta_lordo(self):
        self.assertEqual(mh843_e_pv(90, 1100), 99000.0)
        self.assertEqual(mh843_pv_diretta(99000.0, 0.50), 49500.0)
        self.assertEqual(mh843_pv_batt_lordo(99000.0, 0.50), 49500.0)

    def test_batt_netta_cap_throughput_lega(self):
        self.assertEqual(mh843_pv_batt_netta(49500.0, 0.90, 150, 0.85, 300), 38250.0)
        self.assertEqual(mh843_pv_batt_netta(49500.0, 0.90, 10000, 0.85, 300), 44550.0)
        self.assertEqual(mh843_pv_batt_netta(49500.0, 0.90, 0, 0.85, 300), 0.0)

    def test_autoconsumo_cappato_a_domanda_e_immessa(self):
        self.assertEqual(mh843_pv_servita_pot(49500.0, 38250.0), 87750.0)
        self.assertEqual(mh843_pv_autoconsumo(87750.0, 96806.66666666667), 87750.0)
        self.assertEqual(mh843_pv_autoconsumo(200000.0, 96806.66666666667), 96806.66666666667)
        self.assertEqual(mh843_pv_batt_ciclata(38250.0, 0.90), 42500.0)
        self.assertEqual(mh843_pv_perdite_batt(42500.0, 38250.0), 4250.0)
        self.assertEqual(mh843_pv_immessa(99000.0, 87750.0, 4250.0), 7000.0)

    def test_immessa_mai_negativa_e_bilancio_pv(self):
        bc = mh843_demo_calcoli()
        self.assertGreaterEqual(bc["e_pv_immessa_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_autoconsumo_kwh_e_anno"]
                               + bc["e_pv_perdite_batt_kwh_e_anno"]
                               + bc["e_pv_immessa_kwh_e_anno"], places=6)
        grosso = mh843_calcola(**_demo_kwargs(p_pv_kwp=500))
        self.assertEqual(grosso["e_pv_autoconsumo_kwh_e_anno"], 96806.66666666667)
        self.assertEqual(grosso["e_deficit_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(grosso["e_pv_immessa_kwh_e_anno"], 448943.3333333333, places=6)
        self.assertGreater(grosso["e_pv_immessa_kwh_e_anno"], 0.0)

    def test_deficit_e_autonomia(self):
        self.assertAlmostEqual(mh843_e_deficit(96806.66666666667, 87750.0), 9056.666666666672, places=6)
        self.assertAlmostEqual(mh843_autonomia_batt(150, 0.85, 96806.66666666667, 280), 0.3687762550788513, places=12)
        self.assertEqual(mh843_autonomia_batt(150, 0.85, 0, 280), 0.0)

    def test_gas_e_prelievo_rete_base(self):
        self.assertEqual(mh843_gas_kwh(92960.0, 0.90), 103288.88888888889)
        self.assertAlmostEqual(mh843_costo_gas(103288.88888888889, 0.10), 10328.88888888889, places=6)
        self.assertAlmostEqual(mh843_costo_rete_base(71820.0, 0.28), 20109.6, places=6)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh843_c_base(10328.88888888889, 20109.6, 2500), 32938.488888888896, places=6)
        self.assertAlmostEqual(mh843_c_alt(9056.666666666672, 0.28, 7000.0, 0.12, 8000), 9695.866666666669, places=6)

    def test_immissione_e_ricavo_non_spreco(self):
        base = mh843_demo_calcoli()
        senza_ricavo = mh843_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 840.0, places=6)
        self.assertAlmostEqual(senza_ricavo["risparmio_eur_anno"],
                               base["risparmio_eur_anno"] - 840.0, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh843_risparmio(32938.488888888896, 9695.866666666669), 23242.622222222228, places=6)
        self.assertLess(mh843_risparmio(9695.866666666669, 32938.488888888896), 0.0)

    def test_co2_due_fattori_e_evitata(self):
        self.assertAlmostEqual(mh843_co2_gas(103288.88888888889, 0.202), 20.86435555555556, places=6)
        self.assertAlmostEqual(mh843_co2_rete(71820.0, 0.30), 21.546, places=6)
        self.assertAlmostEqual(mh843_co2_rete(9056.666666666672 - 7000.0, 0.30), 0.617, places=6)
        self.assertAlmostEqual(mh843_co2_evitata(42.410355555555554, 0.617), 41.79335555555555, places=6)

    def test_co2_evitata_negativa_non_clampata_e_alt_negativa(self):
        self.assertAlmostEqual(mh843_co2_evitata(100.0, 200.0), -100.0, places=6)
        grosso = mh843_calcola(**_demo_kwargs(p_pv_kwp=400))
        self.assertLess(grosso["co2_alt_t_anno"], 0.0)
        self.assertAlmostEqual(grosso["co2_alt_t_anno"], -101.683, places=6)
        self.assertGreater(grosso["co2_evitata_t_anno"], grosso["co2_base_t_anno"])

    def test_immessa_con_ricavo_in_c_alt(self):
        bc = mh843_demo_calcoli()
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_deficit_kwh_e_anno"] * 0.28
                               - bc["e_pv_immessa_kwh_e_anno"] * 0.12 + 8000, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"],
                               bc["costo_gas_eur_anno"]
                               + bc["costo_rete_base_eur_anno"] + 2500, places=6)

    def test_solare_vale_in_risparmio(self):
        base = mh843_demo_calcoli()
        senza = mh843_calcola(**_demo_kwargs(coll_mq=0))
        self.assertAlmostEqual(base["risparmio_eur_anno"]
                               - senza["risparmio_eur_anno"], 1680.0, places=6)
        self.assertAlmostEqual(senza["e_pdc_kwh_e_anno"], 30986.666666666668, places=6)


class TestFinanza(unittest.TestCase):
    def test_p_gas_pareggio_demo_none_elettrico_supera_om(self):
        self.assertIsNone(mh843_demo_calcoli()["p_gas_pareggio"])
        self.assertIsNone(mh843_p_gas_pareggio(9056.666666666672, 0.28, 7000.0, 0.12,
                                              8000, 71820.0, 2500, 103288.88888888889))

    def test_p_gas_pareggio_none_casi(self):
        self.assertIsNone(mh843_p_gas_pareggio(9056.666666666672, 0.28, 7000.0, 0.12,
                                              8000, 71820.0, 2500, 0.0))
        self.assertIsNone(mh843_p_gas_pareggio(9056.666666666672, 0.28, 7000.0, 0.12,
                                              8000, 71820.0, 2500, 103288.88888888889))
        self.assertAlmostEqual(mh843_p_gas_pareggio(9056.666666666672, 0.28, 7000.0, 0.12,
                                             60000, 71820.0, 2500, 103288.88888888889),
                         0.37841695352839927, places=12)

    def test_p_gas_pareggio_positivo_a_om_alt_alto(self):
        bc = mh843_calcola(**_demo_kwargs(om_alt=60000))
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.37841695352839927, places=12)

    def test_p_gas_pareggio_verifica_a_om_alt_alto(self):
        bc = mh843_calcola(**_demo_kwargs(om_alt=60000))
        pstar = bc["p_gas_pareggio"]
        r = mh843_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_gas_pareggio_soglia_minima_a_om_alt_alto(self):
        bc = mh843_calcola(**_demo_kwargs(om_alt=60000))
        pstar = bc["p_gas_pareggio"]
        self.assertAlmostEqual(mh843_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar + 0.01))["risparmio_eur_anno"], 1032.8888888888905, places=6)
        self.assertAlmostEqual(mh843_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar - 0.01))["risparmio_eur_anno"], -1032.8888888888905, places=6)

    def test_risparmio_a_gas_nullo_resta_positivo(self):
        r = mh843_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 12913.733333333334, places=6)
        self.assertAlmostEqual(r["van"], -89066.33889253007, places=6)
        self.assertAlmostEqual(r["tir"], 0.3121449769058101, places=6)
        self.assertEqual(r["payback"], 20)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh843_flussi(250000, 23242.622222222228, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -250000)
        self.assertTrue(all(f == 23242.622222222228 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh843_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 39654.44704552741, places=6)
        self.assertAlmostEqual(mh843_van([-250000] + [23242.622222222228] * 20, 0.0), 214852.44444444444, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh843_van([-250000] + [23242.622222222228] * 20, 0.05), 39654.44704552741, places=6)
        self.assertLess(mh843_van([-250000] + [23242.622222222228] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh843_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 6.805463949066333, places=6)
        self.assertGreater(bc["tir"], 6.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh843_payback([-250000] + [23242.622222222228] * 20), 11)
        self.assertEqual(mh843_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh843_payback([-250000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh843_verdetto(23242.622222222228, 100.0, 250000, 0.10), "CONVIENTE")
        self.assertEqual(mh843_verdetto(23242.622222222228, -20000.0, 250000, 0.10), "MARGINALE")
        self.assertEqual(mh843_verdetto(23242.622222222228, -100000.0, 250000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh843_verdetto(0.0, 100.0, 250000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh843_verdetto(-100.0, 100.0, 250000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh843_verdetto(None, 100.0, 250000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh843_verdetto(23242.622222222228, 0.0, 250000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh843_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("camere", "14"), ("camere", float("nan")),
                            ("camere", float("inf")), ("camere", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh843_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"camere": 0}, {"camere": -1},
                     {"camere": 14.5},
                     {"giorni_apertura": 0}, {"giorni_apertura": 280.5},
                     {"occupazione": -0.1}, {"occupazione": 1.1},
                     {"coperti_giorno": -1},
                     {"q_term_pernot": -0.1}, {"q_term_coperto": -0.1},
                     {"e_pernot": -0.1}, {"e_coperto": -0.1},
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
                     {"coll_mq": -1}, {"resa_solare": -1},
                     {"om_base": -1}, {"om_alt": -1},
                     {"capex": -1}, {"f_co2_gas": -0.1},
                     {"f_co2_rete": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh843_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh843_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh843_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh843_valida(**_demo_kwargs(
            occupazione=0, coperti_giorno=0,
            q_term_pernot=0, q_term_coperto=0,
            e_pernot=0, e_coperto=0,
            p_gas=0, p_rete=0, p_immissione=0, quota_diretta=0, cap_batt=0, dod=0,
            cicli_anno=0, p_pv_kwp=0, prod_specifica=0,
            coll_mq=0, resa_solare=0,
            om_base=0, om_alt=0, capex=0, f_co2_gas=0,
            f_co2_rete=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh843_demo()
        self.assertEqual(d["camere"], 14)
        self.assertEqual(d["giorni_apertura"], 280)
        self.assertEqual(d["occupazione"], 0.65)
        self.assertEqual(d["coperti_giorno"], 60)
        self.assertEqual(d["q_term_pernot"], 20)
        self.assertEqual(d["q_term_coperto"], 2.5)
        self.assertEqual(d["e_pernot"], 15)
        self.assertEqual(d["e_coperto"], 2.0)
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
        self.assertEqual(d["p_pv_kwp"], 90)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["coll_mq"], 40)
        self.assertEqual(d["resa_solare"], 450)
        self.assertEqual(d["om_base"], 2500)
        self.assertEqual(d["om_alt"], 8000)
        self.assertEqual(d["capex"], 250000)
        self.assertEqual(d["f_co2_gas"], 0.202)
        self.assertEqual(d["f_co2_rete"], 0.30)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh843_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh843_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], 92960.0, places=6)
        self.assertEqual(bc["e_el_base_kwh_e_anno"], 71820.0)
        self.assertEqual(bc["pernottamenti"], 2548.0)
        self.assertEqual(bc["coperti_totali"], 16800.0)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], 24986.666666666668, places=6)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 99000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 32938.488888888896, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 9695.866666666669, places=6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh843_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[10], -17573.777777777796, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[11], 5668.844444444432, places=6)

    def test_demo_tabella_righe(self):
        bc = mh843_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Camere", voci)
        self.assertIn("Pernottamenti (notti/anno)", voci)
        self.assertIn("Coperti totali ristorante (coperti/anno)", voci)
        self.assertIn("Solare termico utile (kWh_th/anno)", voci)
        self.assertIn("Residuo termico alla pompa di calore (kWh_th/anno)", voci)
        self.assertIn("Fotovoltaico netto da batteria (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico immesso, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Perdite round-trip batteria (kWh_e/anno)", voci)
        self.assertIn("Autonomia batteria (giorni)", voci)
        self.assertIn("Gas baseline (kWh/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("Prezzo gas di pareggio (EUR/kWh, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh843_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"],
                               bc["pernottamenti"] * bc["q_term_pernot"]
                               + bc["coperti_totali"] * bc["q_term_coperto"])
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] + bc["e_el_base_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_tot_alt_kwh_e_anno"] - bc["e_pv_autoconsumo_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        pern = 14 * 280 * 0.65
        copt = 60 * 280
        qterm = pern * 20 + copt * 2.5
        eelbase = pern * 15 + copt * 2.0
        qsol = min(40 * 450, qterm)
        qres = qterm - qsol
        epdc = qres / 3.0
        etot = epdc + eelbase
        e_pv = 90 * 1100
        diretta = e_pv * 0.50
        batt_netta = min(e_pv * 0.50 * 0.90, 150 * 0.85 * 300)
        autoconsumo = min(diretta + batt_netta, etot)
        ciclata = batt_netta / 0.90
        perdite = ciclata - batt_netta
        immessa = e_pv - autoconsumo - perdite
        gasb = qterm / 0.90
        deficit = etot - autoconsumo
        c_base = gasb * 0.10 + eelbase * 0.28 + 2500
        c_alt = deficit * 0.28 - immessa * 0.12 + 8000
        bc = mh843_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], qterm, places=6)
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"], eelbase, places=6)
        self.assertAlmostEqual(bc["pernottamenti"], pern, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"], etot, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_pv_autoconsumo_kwh_e_anno"], autoconsumo, places=6)
        self.assertAlmostEqual(bc["e_pv_immessa_kwh_e_anno"], immessa, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh843_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_gas_piu_meno_20(self):
        meno = mh843_calcola(**_demo_kwargs(p_gas=0.08))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 21176.844444444447, places=6)
        self.assertAlmostEqual(meno["van"], 13910.28985791589, places=6)
        self.assertAlmostEqual(meno["tir"], 5.647649540991265, places=6)
        self.assertEqual(meno["payback"], 12)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh843_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 25308.4, places=6)
        self.assertAlmostEqual(piu["van"], 65398.60423313889, places=6)
        self.assertAlmostEqual(piu["tir"], 7.918279723731696, places=6)
        self.assertEqual(piu["payback"], 10)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_gas_alto_migliora_il_caso(self):
        demo = mh843_demo_calcoli()
        meno = mh843_calcola(**_demo_kwargs(p_gas=0.08))
        piu = mh843_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_non_calcolabile(self):
        r = mh843_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], -2167.3777777777723, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["van"], -277010.31775841344, places=6)
        self.assertIsNone(r["tir"])
        self.assertIsNone(r["payback"])

    def test_variante_senza_batteria_non_convinte(self):
        r = mh843_calcola(**_demo_kwargs(cap_batt=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 17632.622222222228, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -30258.55297612183, places=6)
        self.assertAlmostEqual(r["tir"], 3.5265929726248784, places=6)
        self.assertEqual(r["payback"], 15)

    def test_variante_senza_solare_convinte(self):
        r = mh843_calcola(**_demo_kwargs(coll_mq=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 21562.622222222228, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 18717.933670060287, places=6)
        self.assertAlmostEqual(r["tir"], 5.8676962413006155, places=6)
        self.assertEqual(r["payback"], 12)

    def test_variante_cop_basso_marginale(self):
        r = mh843_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 19744.488888888896, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertAlmostEqual(r["van"], -3940.026360723048, places=6)
        self.assertAlmostEqual(r["tir"], 4.813406278315992, places=6)
        self.assertEqual(r["payback"], 13)

    def test_variante_capex_doppio_non_convinte(self):
        r = mh843_calcola(**_demo_kwargs(capex=500000))
        self.assertAlmostEqual(r["van"], -210345.5529544726, places=6)
        self.assertAlmostEqual(r["tir"], -0.6843543346593066, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh843_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -70526.63214081958, places=6)
        self.assertAlmostEqual(r["tir"], -1.3037496013860763, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh843_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 214852.44444444444, places=6)
        self.assertEqual(zero["payback"], 11)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh843_sensibilita(**mh843_demo())
        self.assertEqual(set(s.keys()), {"gas_meno20", "gas_piu20",
                                         "senza_pv", "senza_batt", "senza_solare",
                                         "cop_2", "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["gas_meno20"]["risparmio_eur_anno"], 21176.844444444447, places=6)
        self.assertAlmostEqual(s["gas_piu20"]["van"], 65398.60423313889, places=6)
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(s["senza_batt"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_solare"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "MARGINALE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh843_demo_calcoli()
        b = mh843_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh843_demo()
        attese = {"camere", "giorni_apertura", "occupazione",
                  "coperti_giorno", "q_term_pernot",
                  "q_term_coperto", "e_pernot", "e_coperto",
                  "eta_caldaia", "p_gas", "p_rete",
                  "p_immissione", "cop", "quota_diretta", "rte",
                  "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                  "prod_specifica", "coll_mq", "resa_solare",
                  "om_base", "om_alt", "capex",
                  "f_co2_gas", "f_co2_rete", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["camere", "giorni_apertura", "occupazione",
                 "coperti_giorno", "q_term_pernot",
                 "q_term_coperto", "e_pernot", "e_coperto",
                 "eta_caldaia", "p_gas", "p_rete",
                 "p_immissione", "cop", "quota_diretta", "rte",
                 "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                 "prod_specifica", "coll_mq", "resa_solare",
                 "om_base", "om_alt", "capex",
                 "f_co2_gas", "f_co2_rete", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh843_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(quota_diretta=1.1))
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(dod=1.1))
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(occupazione=1.1))
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(rte=1.1))
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh843_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("camere", "14"), ("camere", float("nan")),
                           ("capex", float("inf")), ("p_gas", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh843_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh843_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_diretta=0,
                                         cap_batt=0, dod=0, cicli_anno=0,
                                         coll_mq=0, resa_solare=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_gas=0,
                                         f_co2_rete=0, occupazione=0,
                                         coperti_giorno=0,
                                         p_gas=0, p_rete=0,
                                         p_immissione=0))
        self.assertTrue(r["valid"])
        r2 = mh843_calcola(**_demo_kwargs(om_alt=60000, p_gas=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh843_calcola(**_demo_kwargs(om_alt=90000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        bc = mh843_calcola(**_demo_kwargs(om_alt=60000))
        pstar = bc["p_gas_pareggio"]
        r = mh843_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh843_demo_calcoli()
        csv = mh843_csv(bc, dict(mh843_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh843_demo_calcoli()
        csv = mh843_csv(bc, dict(mh843_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]), 23242.622222222228, places=6)
        self.assertEqual(righe["p_gas_pareggio"], "")

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh843_demo_calcoli()
        csv = mh843_csv(bc, dict(mh843_demo()))
        for chiave in mh843_demo().keys():
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
        self.assertEqual(src.count("with tab843:"), 1)
        self.assertTrue(src.startswith("    # W846"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Agriturismo: fotovoltaico + batteria + pompa di calore + solare termico battono caldaia a gas + prelievo da rete per camere e ristorante?", src)
        self.assertIn("🏡 Agriturismo: fotovoltaico + batteria + pompa di calore + solare termico battono caldaia a gas + prelievo da rete per camere e ristorante?", src)
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
        chiavi = re.findall(r'key="(st843_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st843_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st843_calcola"', src)
        self.assertIn('key="st843_csv"', src)
        self.assertIn('key="st843_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def843\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh843_demo().keys()), lette - set(mh843_demo().keys()))
        self.assertEqual(lette, set(mh843_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc843\['([^']+)'\]", src))
        attese = set(mh843_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg843"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
