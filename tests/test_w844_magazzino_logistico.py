"""Test nuova scheda tab844 "Magazzino logistico:
fotovoltaico + batteria + pompa di
calore + illuminazione LED battono
caldaia a gas + rete + illuminazione
tradizionale?".

Business case annuo di un magazzino
logistico con uffici, connesso alla
rete, guidato da SUPERFICIE x
FABBISOGNO SPECIFICO + ORE OPERATIVE
(per l'illuminazione) + PALLET ANNUI
(per la movimentazione), NON da camere,
coperti, veicoli o box:
Q_term = sup_mag x q_mag + sup_uff
x q_uff; E_ill_trad = (sup_mag +
sup_uff) x p_ill_trad x ore / 1000;
E_ill_led = (sup_mag + sup_uff)
x p_ill_led x ore / 1000;
E_mov = e_mov_pallet x pallet_anno;
E_uff = sup_uff x e_uffici;
E_el_base = E_ill_trad + E_mov + E_uff;
E_pdc = Q_term / COP (tutto Q_term:
qui NON c'e' solare termico a monte);
E_tot_alt = E_ill_led + E_mov + E_uff
+ E_pdc; E_pv = kWp x producibilita';
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
la rete esiste); autonomia_batt_ore =
cap_batt x DoD / (E_tot_alt / ore_anno)
(0 se domanda nulla); gas_base = Q_term /
eta_caldaia (baseline: caldaia su TUTTO
Q_term); costo_gas = gas_base x p_gas;
prelievo rete base = E_el_base x p_rete;
C_base = costo_gas + prelievo rete base
+ O&M_base; C_alt = deficit x p_rete -
immessa x p_immissione + O&M_alt
(l'immissione e' un ricavo, segno
meno); risparmio = C_base - C_alt;
CAPEX_tot = capex_fv x kWp + capex_batt
x cap_batt + capex_pdc + capex_led
(voci separate, sommate senza costi
nascosti); CO2 gas base = gas_base x
f_co2_gas / 1000; CO2 rete base =
E_el_base x f_co2_rete / 1000; CO2 base
= somma dei due; CO2 alt = (deficit -
immessa) x f_co2_rete / 1000 (credito
CO2 sull'immissione allo stesso fattore
rete, scelta simmetrica documentata;
puo' essere negativa se l'immissione
supera il deficit); CO2 evitata = base
- alt (segno libero, non clampata: puo'
essere negativa se il deficit supera la
base elettrica piu' l'immissione);
flussi [-CAPEX_tot, risparmio x vita];
VAN al WACC (FRAZIONE, non percentuale);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo gas di
pareggio p* = (deficit x p_rete -
immessa x p_immissione + O&M_alt -
E_el_base x p_rete - O&M_base) /
gas_base in forma chiusa a prezzi
elettrici FERMI, None se gas_base <= 0
o se p* < 0, SOGLIA MINIMA sui soli
costi annui quando esiste (sopra di
essa l'alternativa vince, sotto perde;
il CAPEX non entra nel pareggio annuo).
Nel demo p* e' None: a prezzo gas nullo
il risparmio resterebbe 63.864,00
EUR/anno (solo elettrico netto + O&M),
quindi l'alternativa vince sui costi
annui anche a gas gratis.
Verdetto: NON_CALCOLABILE se input
degenere (sup_mag <= 0, sup_uff < 0,
ore <= 0 o non intere, fabbisogni
specifici < 0, potenze illuminazione
< 0, energia per pallet < 0, pallet
annui < 0, energia uffici < 0, COP <= 0,
eta_caldaia <= 0 o > 1, prezzi < 0,
quota_diretta < 0 o > 1, RTE <= 0 o > 1,
cap_batt < 0, DoD < 0 o > 1, cicli < 0,
kWp < 0, producibilita' < 0, voci CAPEX
< 0, O&M < 0, fattori CO2 < 0, WACC < 0,
vita <= 0 o non intera, tolleranza < 0)
o se risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
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
previsto (sup_mag, ore, vita, COP,
eta_caldaia, RTE). Gli zeri ammessi in
entrambi (sup_uff, fabbisogni specifici,
potenze illuminazione, energia per
pallet, pallet annui, energia uffici,
prezzi, quota FV diretta, cap_batt, DoD,
cicli, kWp, producibilita', voci CAPEX,
O&M, fattori CO2, WACC, tolleranza) non
creano divergenza. Quote e DoD > 1 e
eta_caldaia > 1 sono degeneri in entrambi
ma non raggiungibili via slider (tetto
1,0). WACC sopra 0,20 e tolleranza sopra
1,0 sono ammessi negli helper e limitati
solo dagli slider UI (0,20 e 1,0):
nessuna divergenza nel range
raggiungibile, perche' la guard controlla
solo gli stessi limiti degli helper.
Distinzione esplicita: distinto
dall'agriturismo (driver camere x giorni
x occupazione piu' coperti x giorni, con
solare termico che copre per primo parte
del calore: qui driver superficie x
fabbisogno specifico piu' ore operative
x W/mq, senza solare termico e senza
pernottamenti) e dall'autosalone (driver
superficie piu' ricarica EV veicoli x
giorni x kWh: qui driver superficie
magazzino e uffici piu' ore operative e
pallet annui, e il calore alternativo e'
tutto da pompa di calore).

Demo (magazzino logistico): 8.000 mq
magazzino, 800 mq uffici (totale 8.800),
3.000 ore operative/anno, q_mag 60
(480.000 kWh_th/anno magazzino), q_uff
90 (72.000 kWh_th/anno uffici, Q_term
552.000), illuminazione tradizionale 12
W/mq (316.800 kWh_e/anno), LED 5 W/mq
(132.000 kWh_e/anno), movimentazione
0,8 kWh/pallet x 60.000 pallet/anno
(48.000 kWh_e/anno), uffici elettrici 40
kWh_e/mq/anno (32.000 kWh_e/anno,
E_el_base 396.800), COP 3,2 (E_pdc
172.500, E_tot_alt 384.500),
eta_caldaia 0,92 (gas base 600.000),
prezzo gas 0,10 EUR/kWh, prezzo prelievo
rete 0,28 EUR/kWh, prezzo immissione
0,12 EUR/kWh, quota_diretta 0,55, RTE
0,90, batteria 300 kWh con DoD 0,85 e
300 cicli/anno (cap throughput 76.500
kWh_e/anno), fotovoltaico 250 kWp a
1.100 kWh/kWp/anno (E_pv 275.000,
diretta 151.250, batt lordo 123.750,
batt netta 76.500, servita potenziale
227.750, autoconsumo 227.750, deficit
156.750, ciclata 85.000, perdite batt
8.500, immessa 38.750 con ricavo 4.650
EUR/anno, autonomia 1,9895968790637193
ore operative), costo gas 60.000,
prelievo rete base 111.104, O&M base
4.000, O&M alt 12.000, CAPEX voci: FV
900 EUR/kWp (225.000), batteria 600
EUR/kWh (180.000), pompa di calore
80.000, LED 30.000 (totale 515.000),
fattore CO2 gas 0,202 kg/kWh, fattore
CO2 rete 0,30 kg/kWh_e, WACC 0,05
(frazione), vita 20 anni, tolleranza
0,10 (frazione del CAPEX).
Valori calcolati eseguendo
mh844_demo_calcoli(): Q_term 552000,0,
E_ill_trad 316800,0, E_ill_led 132000,0,
E_mov 48000,0, E_uff 32000,0, E_el_base
396800,0, E_pdc 172500,0, E_tot_alt
384500,0, E_pv 275000,0, diretta
151250,0, batt lordo 123750,0, batt
netta 76500,0, servita pot 227750,0,
autoconsumo 227750,0, deficit 156750,0,
ciclata 85000,0, perdite batt 8500,0,
immessa 38750,0, autonomia
1,9895968790637193, gas base 600000,0,
costo gas 60000,0, prelievo rete base
111104,0, C_base 175104,0, C_alt
51240,0, risparmio 123864,0, CAPEX tot
515000,0, CO2 gas base 121,2, CO2 rete
base 119,04, CO2 base 240,24, CO2 alt
35,4, CO2 evitata 204,84, VAN
1028619,2218683723, TIR
23,710038562941637 %, payback 5,
p_gas_pareggio None (a gas nullo il
risparmio resterebbe 63.864,00 EUR/anno),
verdetto CONVIENTE (VAN quasi il doppio
del CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab844 in app.py e il
count-assert sui 844 tab NON sono
inclusi in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza e del conteggio
in app.py spetta alla fase di apply del
worker, non a questa fase. Tutti i test
qui inclusi passano da hidden_files
senza app.py. La forma del count in
questa fase e' strutturale: il blocco UI
apre tab844 esattamente una volta e gli
helper definiscono le funzioni mh844.

Destinazione nel repo: tests/test_w844_magazzino_logistico.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w847_helpers import (
        demo_calcoli,
        mh844_autonomia_batt_ore,
        mh844_c_alt,
        mh844_c_base,
        mh844_calcola,
        mh844_capex_totale,
        mh844_co2_evitata,
        mh844_co2_gas,
        mh844_co2_rete,
        mh844_costo_gas,
        mh844_costo_rete_base,
        mh844_csv,
        mh844_demo,
        mh844_demo_calcoli,
        mh844_e_deficit,
        mh844_e_el_base,
        mh844_e_illuminazione,
        mh844_e_movimentazione,
        mh844_e_pdc,
        mh844_e_pv,
        mh844_e_tot_alt,
        mh844_e_uffici,
        mh844_eta,
        mh844_frazione,
        mh844_flussi,
        mh844_gas_kwh,
        mh844_int_pos,
        mh844_nneg,
        mh844_num,
        mh844_p_gas_pareggio,
        mh844_payback,
        mh844_pos,
        mh844_pv_autoconsumo,
        mh844_pv_batt_ciclata,
        mh844_pv_batt_lordo,
        mh844_pv_batt_netta,
        mh844_pv_diretta,
        mh844_pv_immessa,
        mh844_pv_perdite_batt,
        mh844_pv_servita_pot,
        mh844_q_termico,
        mh844_risparmio,
        mh844_sensibilita,
        mh844_tir,
        mh844_valida,
        mh844_van,
        mh844_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w847_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w847_helpers", os.path.join(_hf, "w847_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh844_autonomia_batt_ore = _mod.mh844_autonomia_batt_ore
    mh844_c_alt = _mod.mh844_c_alt
    mh844_c_base = _mod.mh844_c_base
    mh844_calcola = _mod.mh844_calcola
    mh844_capex_totale = _mod.mh844_capex_totale
    mh844_co2_evitata = _mod.mh844_co2_evitata
    mh844_co2_gas = _mod.mh844_co2_gas
    mh844_co2_rete = _mod.mh844_co2_rete
    mh844_costo_gas = _mod.mh844_costo_gas
    mh844_costo_rete_base = _mod.mh844_costo_rete_base
    mh844_csv = _mod.mh844_csv
    mh844_demo = _mod.mh844_demo
    mh844_demo_calcoli = _mod.mh844_demo_calcoli
    mh844_e_deficit = _mod.mh844_e_deficit
    mh844_e_el_base = _mod.mh844_e_el_base
    mh844_e_illuminazione = _mod.mh844_e_illuminazione
    mh844_e_movimentazione = _mod.mh844_e_movimentazione
    mh844_e_pdc = _mod.mh844_e_pdc
    mh844_e_pv = _mod.mh844_e_pv
    mh844_e_tot_alt = _mod.mh844_e_tot_alt
    mh844_e_uffici = _mod.mh844_e_uffici
    mh844_eta = _mod.mh844_eta
    mh844_frazione = _mod.mh844_frazione
    mh844_flussi = _mod.mh844_flussi
    mh844_gas_kwh = _mod.mh844_gas_kwh
    mh844_int_pos = _mod.mh844_int_pos
    mh844_nneg = _mod.mh844_nneg
    mh844_num = _mod.mh844_num
    mh844_p_gas_pareggio = _mod.mh844_p_gas_pareggio
    mh844_payback = _mod.mh844_payback
    mh844_pos = _mod.mh844_pos
    mh844_pv_autoconsumo = _mod.mh844_pv_autoconsumo
    mh844_pv_batt_ciclata = _mod.mh844_pv_batt_ciclata
    mh844_pv_batt_lordo = _mod.mh844_pv_batt_lordo
    mh844_pv_batt_netta = _mod.mh844_pv_batt_netta
    mh844_pv_diretta = _mod.mh844_pv_diretta
    mh844_pv_immessa = _mod.mh844_pv_immessa
    mh844_pv_perdite_batt = _mod.mh844_pv_perdite_batt
    mh844_pv_servita_pot = _mod.mh844_pv_servita_pot
    mh844_q_termico = _mod.mh844_q_termico
    mh844_risparmio = _mod.mh844_risparmio
    mh844_sensibilita = _mod.mh844_sensibilita
    mh844_tir = _mod.mh844_tir
    mh844_valida = _mod.mh844_valida
    mh844_van = _mod.mh844_van
    mh844_verdetto = _mod.mh844_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w847_helpers.py")
_UI_PATH = _risolvi("w847_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# tab precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "3_"
_VECCHIO_TAB = "tab84" + "3"
_VECCHIO_ST = "st84" + "3_"

_DEMO = {
    "q_termico_kwh_th_anno": 552000.0,
    "e_ill_trad_kwh_e_anno": 316800.0,
    "e_ill_led_kwh_e_anno": 132000.0,
    "e_mov_kwh_e_anno": 48000.0,
    "e_uff_kwh_e_anno": 32000.0,
    "e_el_base_kwh_e_anno": 396800.0,
    "e_pdc_kwh_e_anno": 172500.0,
    "e_tot_alt_kwh_e_anno": 384500.0,
    "e_pv_kwh_e_anno": 275000.0,
    "e_pv_diretta_kwh_e_anno": 151250.0,
    "e_pv_batt_lordo_kwh_e_anno": 123750.0,
    "e_pv_batt_netta_kwh_e_anno": 76500.0,
    "e_pv_servita_pot_kwh_e_anno": 227750.0,
    "e_pv_autoconsumo_kwh_e_anno": 227750.0,
    "e_deficit_kwh_e_anno": 156750.0,
    "e_pv_batt_ciclata_kwh_e_anno": 85000.0,
    "e_pv_perdite_batt_kwh_e_anno": 8500.0,
    "e_pv_immessa_kwh_e_anno": 38750.0,
    "autonomia_batt_ore": 1.9895968790637193,
    "gas_base_kwh_anno": 600000.0,
    "costo_gas_eur_anno": 60000.0,
    "costo_rete_base_eur_anno": 111104.0,
    "c_base_eur_anno": 175104.0,
    "c_alt_eur_anno": 51240.0,
    "risparmio_eur_anno": 123864.0,
    "capex_totale_eur": 515000.0,
    "co2_gas_base_t_anno": 121.2,
    "co2_rete_base_t_anno": 119.04,
    "co2_base_t_anno": 240.24,
    "co2_alt_t_anno": 35.4,
    "co2_evitata_t_anno": 204.84,
    "van": 1028619.2218683723,
    "tir": 23.710038562941637,
    "payback": 5,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh844_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh844_num(3, "x"), 3.0)
        self.assertEqual(mh844_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh844_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh844_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh844_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh844_pos(0, "x")
        with self.assertRaises(ValueError):
            mh844_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh844_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh844_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh844_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh844_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh844_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh844_int_pos(3000.0, "ore"), 3000)
        with self.assertRaises(ValueError):
            mh844_int_pos(3000.5, "ore")

    def test_frazione_limiti(self):
        self.assertEqual(mh844_frazione(0, "quota"), 0.0)
        self.assertEqual(mh844_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh844_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh844_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_termico_superfici(self):
        self.assertEqual(mh844_q_termico(8000, 60, 800, 90), 552000.0)
        self.assertEqual(mh844_q_termico(8000, 60, 0, 90), 480000.0)

    def test_illuminazione_ore_e_watt(self):
        self.assertEqual(mh844_e_illuminazione(8800, 12, 3000), 316800.0)
        self.assertEqual(mh844_e_illuminazione(8800, 5, 3000), 132000.0)
        self.assertEqual(mh844_e_illuminazione(8800, 0, 3000), 0.0)

    def test_movimentazione_e_uffici(self):
        self.assertEqual(mh844_e_movimentazione(0.8, 60000), 48000.0)
        self.assertEqual(mh844_e_movimentazione(0.8, 0), 0.0)
        self.assertEqual(mh844_e_uffici(800, 40), 32000.0)
        self.assertEqual(mh844_e_uffici(0, 40), 0.0)

    def test_el_base_e_pdc_e_tot_alt(self):
        self.assertEqual(mh844_e_el_base(316800.0, 48000.0, 32000.0), 396800.0)
        self.assertEqual(mh844_e_pdc(552000.0, 3.2), 172500.0)
        self.assertEqual(mh844_e_tot_alt(172500.0, 132000.0, 48000.0, 32000.0), 384500.0)

    def test_pv_diretta_lordo(self):
        self.assertEqual(mh844_e_pv(250, 1100), 275000.0)
        self.assertEqual(mh844_pv_diretta(275000.0, 0.55), 151250.0)
        self.assertAlmostEqual(mh844_pv_batt_lordo(275000.0, 0.55), 123750.0, places=6)

    def test_batt_netta_cap_throughput_lega(self):
        self.assertEqual(mh844_pv_batt_netta(123750.0, 0.90, 300, 0.85, 300), 76500.0)
        self.assertEqual(mh844_pv_batt_netta(123750.0, 0.90, 10000, 0.85, 300), 111375.0)
        self.assertEqual(mh844_pv_batt_netta(123750.0, 0.90, 0, 0.85, 300), 0.0)

    def test_autoconsumo_cappato_a_domanda_e_immessa(self):
        self.assertEqual(mh844_pv_servita_pot(151250.0, 76500.0), 227750.0)
        self.assertEqual(mh844_pv_autoconsumo(227750.0, 384500.0), 227750.0)
        self.assertEqual(mh844_pv_autoconsumo(500000.0, 384500.0), 384500.0)
        self.assertEqual(mh844_pv_batt_ciclata(76500.0, 0.90), 85000.0)
        self.assertEqual(mh844_pv_perdite_batt(85000.0, 76500.0), 8500.0)
        self.assertEqual(mh844_pv_immessa(275000.0, 227750.0, 8500.0), 38750.0)

    def test_immessa_mai_negativa_e_bilancio_pv(self):
        bc = mh844_demo_calcoli()
        self.assertGreaterEqual(bc["e_pv_immessa_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_autoconsumo_kwh_e_anno"]
                               + bc["e_pv_perdite_batt_kwh_e_anno"]
                               + bc["e_pv_immessa_kwh_e_anno"], places=6)
        grosso = mh844_calcola(**_demo_kwargs(p_pv_kwp=1000))
        self.assertEqual(grosso["e_pv_autoconsumo_kwh_e_anno"], 384500.0)
        self.assertEqual(grosso["e_deficit_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(grosso["e_pv_immessa_kwh_e_anno"], 707000.0, places=6)
        self.assertGreater(grosso["e_pv_immessa_kwh_e_anno"], 0.0)

    def test_deficit_e_autonomia_ore(self):
        self.assertEqual(mh844_e_deficit(384500.0, 227750.0), 156750.0)
        self.assertAlmostEqual(mh844_autonomia_batt_ore(300, 0.85, 384500.0, 3000), 1.9895968790637193, places=12)
        self.assertEqual(mh844_autonomia_batt_ore(300, 0.85, 0, 3000), 0.0)

    def test_gas_e_prelievo_rete_base(self):
        self.assertEqual(mh844_gas_kwh(552000.0, 0.92), 600000.0)
        self.assertEqual(mh844_costo_gas(600000.0, 0.10), 60000.0)
        self.assertAlmostEqual(mh844_costo_rete_base(396800.0, 0.28), 111104.0, places=6)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh844_c_base(60000.0, 111104.0, 4000), 175104.0, places=6)
        self.assertAlmostEqual(mh844_c_alt(156750.0, 0.28, 38750.0, 0.12, 12000), 51240.0, places=6)

    def test_capex_totale_voci(self):
        self.assertEqual(mh844_capex_totale(900, 250, 600, 300, 80000, 30000), 515000.0)
        self.assertEqual(mh844_capex_totale(900, 0, 600, 300, 80000, 30000), 290000.0)
        self.assertEqual(mh844_capex_totale(0, 250, 0, 300, 0, 0), 0.0)

    def test_immissione_e_ricavo_non_spreco(self):
        base = mh844_demo_calcoli()
        senza_ricavo = mh844_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 4650.0, places=6)
        self.assertAlmostEqual(senza_ricavo["risparmio_eur_anno"],
                               base["risparmio_eur_anno"] - 4650.0, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh844_risparmio(175104.0, 51240.0), 123864.0, places=6)
        self.assertLess(mh844_risparmio(51240.0, 175104.0), 0.0)

    def test_co2_due_fattori_e_evitata(self):
        self.assertAlmostEqual(mh844_co2_gas(600000.0, 0.202), 121.2, places=6)
        self.assertAlmostEqual(mh844_co2_rete(396800.0, 0.30), 119.04, places=6)
        self.assertAlmostEqual(mh844_co2_rete(156750.0 - 38750.0, 0.30), 35.4, places=6)
        self.assertAlmostEqual(mh844_co2_evitata(240.24, 35.4), 204.84, places=6)

    def test_co2_evitata_negativa_non_clampata_e_alt_negativa(self):
        self.assertAlmostEqual(mh844_co2_evitata(100.0, 200.0), -100.0, places=6)
        grosso = mh844_calcola(**_demo_kwargs(p_pv_kwp=1000))
        self.assertLess(grosso["co2_alt_t_anno"], 0.0)
        self.assertAlmostEqual(grosso["co2_alt_t_anno"], -212.1, places=6)
        self.assertGreater(grosso["co2_evitata_t_anno"], grosso["co2_base_t_anno"])

    def test_immessa_con_ricavo_in_c_alt(self):
        bc = mh844_demo_calcoli()
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_deficit_kwh_e_anno"] * 0.28
                               - bc["e_pv_immessa_kwh_e_anno"] * 0.12 + 12000, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"],
                               bc["costo_gas_eur_anno"]
                               + bc["costo_rete_base_eur_anno"] + 4000, places=6)

    def test_led_vale_in_risparmio(self):
        base = mh844_demo_calcoli()
        senza = mh844_calcola(**_demo_kwargs(p_ill_led=12))
        self.assertAlmostEqual(base["risparmio_eur_anno"]
                               - senza["risparmio_eur_anno"], 51744.0, places=6)
        self.assertAlmostEqual(senza["e_ill_led_kwh_e_anno"], 316800.0, places=6)

    def test_fv_nullo_ammesso_non_degenere(self):
        r = mh844_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertEqual(r["e_pv_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_pv_autoconsumo_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_pv_immessa_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_deficit_kwh_e_anno"], 384500.0)
        self.assertTrue(r["valid"])


class TestFinanza(unittest.TestCase):
    def test_p_gas_pareggio_demo_none_elettrico_supera_om(self):
        self.assertIsNone(mh844_demo_calcoli()["p_gas_pareggio"])
        self.assertIsNone(mh844_p_gas_pareggio(156750.0, 0.28, 38750.0, 0.12,
                                              12000, 396800.0, 4000, 600000.0))

    def test_p_gas_pareggio_none_casi(self):
        self.assertIsNone(mh844_p_gas_pareggio(156750.0, 0.28, 38750.0, 0.12,
                                              12000, 396800.0, 4000, 0.0))
        self.assertIsNone(mh844_p_gas_pareggio(156750.0, 0.28, 38750.0, 0.12,
                                              12000, 396800.0, 4000, 600000.0))
        self.assertAlmostEqual(mh844_p_gas_pareggio(156750.0, 0.28, 38750.0, 0.12,
                                             120000, 396800.0, 4000, 600000.0),
                         0.07356, places=12)

    def test_p_gas_pareggio_positivo_a_om_alt_alto(self):
        bc = mh844_calcola(**_demo_kwargs(om_alt=120000))
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.07356, places=12)

    def test_p_gas_pareggio_verifica_a_om_alt_alto(self):
        bc = mh844_calcola(**_demo_kwargs(om_alt=120000))
        pstar = bc["p_gas_pareggio"]
        r = mh844_calcola(**_demo_kwargs(om_alt=120000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_gas_pareggio_soglia_minima_a_om_alt_alto(self):
        bc = mh844_calcola(**_demo_kwargs(om_alt=120000))
        pstar = bc["p_gas_pareggio"]
        self.assertAlmostEqual(mh844_calcola(**_demo_kwargs(om_alt=120000, p_gas=pstar + 0.01))["risparmio_eur_anno"], 6000.0, places=6)
        self.assertAlmostEqual(mh844_calcola(**_demo_kwargs(om_alt=120000, p_gas=pstar - 0.01))["risparmio_eur_anno"], -6000.0, places=6)

    def test_risparmio_a_gas_nullo_resta_positivo(self):
        r = mh844_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 63864.0, places=6)
        self.assertAlmostEqual(r["van"], 280886.6013159735, places=6)
        self.assertAlmostEqual(r["tir"], 10.80866036370804, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh844_flussi(515000, 123864.0, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -515000)
        self.assertTrue(all(f == 123864.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh844_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 1028619.2218683723, places=6)
        self.assertAlmostEqual(mh844_van([-515000] + [123864.0] * 20, 0.0), 1962280.0, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh844_van([-515000] + [123864.0] * 20, 0.05), 1028619.2218683723, places=6)
        self.assertLess(mh844_van([-515000] + [123864.0] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh844_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 23.710038562941637, places=6)
        self.assertGreater(bc["tir"], 20.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh844_payback([-515000] + [123864.0] * 20), 5)
        self.assertEqual(mh844_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh844_payback([-515000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh844_verdetto(123864.0, 100.0, 515000, 0.10), "CONVIENTE")
        self.assertEqual(mh844_verdetto(123864.0, -40000.0, 515000, 0.10), "MARGINALE")
        self.assertEqual(mh844_verdetto(123864.0, -100000.0, 515000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh844_verdetto(0.0, 100.0, 515000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh844_verdetto(-100.0, 100.0, 515000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh844_verdetto(None, 100.0, 515000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh844_verdetto(123864.0, 0.0, 515000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh844_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("sup_mag_m2", "8000"), ("sup_mag_m2", float("nan")),
                            ("sup_mag_m2", float("inf")), ("sup_mag_m2", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh844_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"sup_mag_m2": 0}, {"sup_mag_m2": -1},
                     {"sup_uff_m2": -1},
                     {"ore_anno": 0}, {"ore_anno": 3000.5},
                     {"q_mag": -0.1}, {"q_uff": -0.1},
                     {"p_ill_trad": -0.1}, {"p_ill_led": -0.1},
                     {"e_mov_pallet": -0.1}, {"pallet_anno": -1},
                     {"e_uffici": -0.1},
                     {"cop": 0}, {"cop": -1},
                     {"eta_caldaia": 0}, {"eta_caldaia": 1.1},
                     {"p_gas": -0.1}, {"p_rete": -0.1},
                     {"p_immissione": -0.1},
                     {"quota_diretta": -0.1}, {"quota_diretta": 1.1},
                     {"rte": 0}, {"rte": 1.1},
                     {"cap_batt": -1},
                     {"dod": -0.1}, {"dod": 1.1},
                     {"cicli_anno": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"capex_fv": -1}, {"capex_batt": -1},
                     {"capex_pdc": -1}, {"capex_led": -1},
                     {"om_base": -1}, {"om_alt": -1},
                     {"f_co2_gas": -0.1},
                     {"f_co2_rete": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh844_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh844_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh844_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh844_valida(**_demo_kwargs(
            sup_uff_m2=0, q_mag=0, q_uff=0,
            p_ill_trad=0, p_ill_led=0,
            e_mov_pallet=0, pallet_anno=0, e_uffici=0,
            p_gas=0, p_rete=0, p_immissione=0, quota_diretta=0, cap_batt=0, dod=0,
            cicli_anno=0, p_pv_kwp=0, prod_specifica=0,
            capex_fv=0, capex_batt=0, capex_pdc=0, capex_led=0,
            om_base=0, om_alt=0, f_co2_gas=0,
            f_co2_rete=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh844_demo()
        self.assertEqual(d["sup_mag_m2"], 8000)
        self.assertEqual(d["sup_uff_m2"], 800)
        self.assertEqual(d["ore_anno"], 3000)
        self.assertEqual(d["q_mag"], 60)
        self.assertEqual(d["q_uff"], 90)
        self.assertEqual(d["p_ill_trad"], 12)
        self.assertEqual(d["p_ill_led"], 5)
        self.assertEqual(d["e_mov_pallet"], 0.8)
        self.assertEqual(d["pallet_anno"], 60000)
        self.assertEqual(d["e_uffici"], 40)
        self.assertEqual(d["cop"], 3.2)
        self.assertEqual(d["eta_caldaia"], 0.92)
        self.assertEqual(d["p_gas"], 0.10)
        self.assertEqual(d["p_rete"], 0.28)
        self.assertEqual(d["p_immissione"], 0.12)
        self.assertEqual(d["quota_diretta"], 0.55)
        self.assertEqual(d["rte"], 0.90)
        self.assertEqual(d["cap_batt"], 300)
        self.assertEqual(d["dod"], 0.85)
        self.assertEqual(d["cicli_anno"], 300)
        self.assertEqual(d["p_pv_kwp"], 250)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["capex_fv"], 900)
        self.assertEqual(d["capex_batt"], 600)
        self.assertEqual(d["capex_pdc"], 80000)
        self.assertEqual(d["capex_led"], 30000)
        self.assertEqual(d["om_base"], 4000)
        self.assertEqual(d["om_alt"], 12000)
        self.assertEqual(d["f_co2_gas"], 0.202)
        self.assertEqual(d["f_co2_rete"], 0.30)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh844_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh844_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], 552000.0, places=6)
        self.assertEqual(bc["e_el_base_kwh_e_anno"], 396800.0)
        self.assertEqual(bc["sup_tot_m2"], 8800.0)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], 172500.0, places=6)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 275000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 175104.0, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 51240.0, places=6)
        self.assertEqual(bc["capex_totale_eur"], 515000.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh844_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[4], -19544.0, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[5], 104320.0, places=6)

    def test_demo_tabella_righe(self):
        bc = mh844_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie magazzino (mq)", voci)
        self.assertIn("Superficie totale (mq)", voci)
        self.assertIn("Ore operative (ore/anno)", voci)
        self.assertIn("Illuminazione tradizionale (kWh_e/anno)", voci)
        self.assertIn("Illuminazione LED (kWh_e/anno)", voci)
        self.assertIn("Movimentazione (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico netto da batteria (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico immesso, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Perdite round-trip batteria (kWh_e/anno)", voci)
        self.assertIn("Autonomia batteria (ore operative)", voci)
        self.assertIn("Gas baseline (kWh/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("CAPEX totale (EUR)", voci)
        self.assertIn("Prezzo gas di pareggio (EUR/kWh, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh844_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"],
                               bc["sup_mag_m2"] * bc["q_mag"]
                               + bc["sup_uff_m2"] * bc["q_uff"])
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] + bc["e_ill_led_kwh_e_anno"]
                               + bc["e_mov_kwh_e_anno"] + bc["e_uff_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_tot_alt_kwh_e_anno"] - bc["e_pv_autoconsumo_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(bc["capex_totale_eur"],
                               bc["capex_fv"] * bc["p_pv_kwp"]
                               + bc["capex_batt"] * bc["cap_batt"]
                               + bc["capex_pdc"] + bc["capex_led"])

    def test_demo_contro_riconteggio_indipendente(self):
        stot = 8000 + 800
        qterm = 8000 * 60 + 800 * 90
        illt = stot * 12 * 3000 / 1000
        illl = stot * 5 * 3000 / 1000
        emov = 0.8 * 60000
        euff = 800 * 40
        eelbase = illt + emov + euff
        epdc = qterm / 3.2
        etot = illl + emov + euff + epdc
        e_pv = 250 * 1100
        diretta = e_pv * 0.55
        batt_netta = min(e_pv * 0.45 * 0.90, 300 * 0.85 * 300)
        autoconsumo = min(diretta + batt_netta, etot)
        ciclata = batt_netta / 0.90
        perdite = ciclata - batt_netta
        immessa = e_pv - autoconsumo - perdite
        gasb = qterm / 0.92
        deficit = etot - autoconsumo
        c_base = gasb * 0.10 + eelbase * 0.28 + 4000
        c_alt = deficit * 0.28 - immessa * 0.12 + 12000
        bc = mh844_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], qterm, places=6)
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"], eelbase, places=6)
        self.assertAlmostEqual(bc["sup_tot_m2"], stot, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"], etot, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_pv_autoconsumo_kwh_e_anno"], autoconsumo, places=6)
        self.assertAlmostEqual(bc["e_pv_immessa_kwh_e_anno"], immessa, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh844_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_gas_piu_meno_20(self):
        meno = mh844_calcola(**_demo_kwargs(p_gas=0.08))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 111864.0, places=6)
        self.assertAlmostEqual(meno["van"], 879072.6977578924, places=6)
        self.assertAlmostEqual(meno["tir"], 21.261519571543026, places=6)
        self.assertEqual(meno["payback"], 5)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh844_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 135864.0, places=6)
        self.assertAlmostEqual(piu["van"], 1178165.745978852, places=6)
        self.assertAlmostEqual(piu["tir"], 26.127190120280773, places=6)
        self.assertEqual(piu["payback"], 4)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_gas_alto_migliora_il_caso(self):
        demo = mh844_demo_calcoli()
        meno = mh844_calcola(**_demo_kwargs(p_gas=0.08))
        piu = mh844_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_convinte(self):
        r = mh844_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 55444.0, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 400954.79023178655, places=6)
        self.assertAlmostEqual(r["tir"], 18.47451394918863, places=6)
        self.assertEqual(r["payback"], 6)
        self.assertEqual(r["capex_totale_eur"], 290000.0)

    def test_variante_senza_batteria_risparmio_giu_van_su(self):
        r = mh844_calcola(**_demo_kwargs(cap_batt=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 112644.0, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 1068793.2218250735, places=6)
        self.assertAlmostEqual(r["tir"], 33.521406491427854, places=6)
        self.assertEqual(r["payback"], 3)
        self.assertGreater(r["van"], mh844_demo_calcoli()["van"])

    def test_variante_senza_led_convinte(self):
        r = mh844_calcola(**_demo_kwargs(p_ill_led=12))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 72120.0, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 383774.6099039833, places=6)
        self.assertAlmostEqual(r["tir"], 12.728753762033135, places=6)
        self.assertEqual(r["payback"], 8)

    def test_variante_cop_basso_convinte(self):
        r = mh844_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 94884.0, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 667464.3661415636, places=6)
        self.assertAlmostEqual(r["tir"], 17.718598682075985, places=6)
        self.assertEqual(r["payback"], 6)

    def test_variante_capex_doppio_convinte(self):
        r = mh844_calcola(**_demo_kwargs(capex_fv=1800, capex_batt=1200,
                                         capex_pdc=160000, capex_led=60000))
        self.assertAlmostEqual(r["van"], 513619.2218683723, places=6)
        self.assertAlmostEqual(r["tir"], 10.347322117605637, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertEqual(r["capex_totale_eur"], 1030000.0)

    def test_variante_vita_10_convinte(self):
        r = mh844_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 441444.9752685473, places=6)
        self.assertAlmostEqual(r["tir"], 20.245398645991543, places=6)
        self.assertEqual(r["payback"], 5)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh844_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 1962280.0, places=6)
        self.assertEqual(zero["payback"], 5)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh844_sensibilita(**mh844_demo())
        self.assertEqual(set(s.keys()), {"gas_meno20", "gas_piu20",
                                         "senza_pv", "senza_batt", "senza_led",
                                         "cop_2", "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["gas_meno20"]["risparmio_eur_anno"], 111864.0, places=6)
        self.assertAlmostEqual(s["gas_piu20"]["van"], 1178165.745978852, places=6)
        self.assertEqual(s["senza_pv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_batt"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_led"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh844_demo_calcoli()
        b = mh844_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh844_demo()
        attese = {"sup_mag_m2", "sup_uff_m2", "ore_anno",
                  "q_mag", "q_uff", "p_ill_trad", "p_ill_led",
                  "e_mov_pallet", "pallet_anno", "e_uffici",
                  "cop", "eta_caldaia", "p_gas", "p_rete",
                  "p_immissione", "quota_diretta", "rte",
                  "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                  "prod_specifica", "capex_fv", "capex_batt",
                  "capex_pdc", "capex_led",
                  "om_base", "om_alt",
                  "f_co2_gas", "f_co2_rete", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["sup_mag_m2", "sup_uff_m2", "ore_anno",
                 "q_mag", "q_uff", "p_ill_trad", "p_ill_led",
                 "e_mov_pallet", "pallet_anno", "e_uffici",
                 "cop", "eta_caldaia", "p_gas", "p_rete",
                 "p_immissione", "quota_diretta", "rte",
                 "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                 "prod_specifica", "capex_fv", "capex_batt",
                 "capex_pdc", "capex_led",
                 "om_base", "om_alt",
                 "f_co2_gas", "f_co2_rete", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh844_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh844_calcola(**_demo_kwargs(quota_diretta=1.1))
        with self.assertRaises(ValueError):
            mh844_calcola(**_demo_kwargs(dod=1.1))
        with self.assertRaises(ValueError):
            mh844_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh844_calcola(**_demo_kwargs(rte=1.1))
        with self.assertRaises(ValueError):
            mh844_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh844_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("sup_mag_m2", "8000"), ("sup_mag_m2", float("nan")),
                           ("capex_pdc", float("inf")), ("p_gas", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh844_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh844_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_diretta=0,
                                         cap_batt=0, dod=0, cicli_anno=0,
                                         capex_fv=0, capex_batt=0,
                                         capex_pdc=0, capex_led=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         f_co2_gas=0,
                                         f_co2_rete=0,
                                         p_gas=0, p_rete=0,
                                         p_immissione=0,
                                         sup_uff_m2=0, q_mag=0, q_uff=0,
                                         p_ill_trad=0, p_ill_led=0,
                                         e_mov_pallet=0, pallet_anno=0,
                                         e_uffici=0))
        self.assertTrue(r["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh844_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(r["risparmio_eur_anno"], -64136.0, places=6)

    def test_pareggio_esatto_soglia(self):
        bc = mh844_calcola(**_demo_kwargs(om_alt=120000))
        pstar = bc["p_gas_pareggio"]
        r = mh844_calcola(**_demo_kwargs(om_alt=120000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh844_demo_calcoli()
        csv = mh844_csv(bc, dict(mh844_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh844_demo_calcoli()
        csv = mh844_csv(bc, dict(mh844_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]), 123864.0, places=6)
        self.assertEqual(righe["p_gas_pareggio"], "")

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh844_demo_calcoli()
        csv = mh844_csv(bc, dict(mh844_demo()))
        for chiave in mh844_demo().keys():
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
        self.assertEqual(src.count("with tab844:"), 1)
        self.assertTrue(src.startswith("    # W847"))

    def test_ui_tab844_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre tab844 esattamente una
        # volta e gli helper definiscono le funzioni mh844.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab844:"), 1)
        self.assertIn("def mh844_demo(", src_h)
        self.assertIn("def mh844_calcola(", src_h)
        self.assertIn("tab844", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Magazzino logistico: fotovoltaico + batteria + pompa di calore + illuminazione LED battono caldaia a gas + rete + illuminazione tradizionale?", src)
        self.assertIn("📦 Magazzino logistico: fotovoltaico + batteria + pompa di calore + illuminazione LED battono caldaia a gas + rete + illuminazione tradizionale?", src)
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
        chiavi = re.findall(r'key="(st844_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st844_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st844_calcola"', src)
        self.assertIn('key="st844_csv"', src)
        self.assertIn('key="st844_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def844\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh844_demo().keys()), lette - set(mh844_demo().keys()))
        self.assertEqual(lette, set(mh844_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc844\['([^']+)'\]", src))
        attese = set(mh844_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg844"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
