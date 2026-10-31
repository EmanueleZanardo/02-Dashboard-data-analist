"""Test nuova scheda tab842 "Autosalone:
fotovoltaico + ricarica EV + pompa di
calore battono caldaia a gas +
prelievo da rete per showroom,
officina e piazzale?".

Business case annuo di un autosalone
(showroom + officina + piazzale) con
ricarica EV dei veicoli in vendita/demo,
connesso alla rete, 300 giorni di
apertura, guidato da SUPERFICIE (mq)
per termico ed elettrico base e da
veicoli x giorni x kWh/veicolo/giorno
per la ricarica EV:
Q_term = superficie x q_spec_termico;
E_el_base = superficie x
e_spec_elettrico (SENZA ricarica EV);
E_ev = veicoli x giorni x
kwh_ev_giorno (carico aggiuntivo,
identico in baseline e alternativa:
cambia solo la fonte che lo alimenta);
E_el_base_tot = E_el_base + E_ev
(elettricita' piena della baseline, a
prezzo pieno); E_pdc = Q_term / COP;
E_tot_alt = E_pdc + E_el_base + E_ev;
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
la rete esiste: differenza onesta dal
campeggio off-grid); autonomia_batt =
cap_batt x DoD / (E_tot_alt / giorni)
(0 se domanda nulla); gas_base = Q_term /
eta_caldaia; costo_gas = gas_base x
p_gas; prelievo rete base = E_el_base_tot
x p_rete (base PIU' ricarica EV a prezzo
pieno); C_base = costo_gas + prelievo
rete base + O&M_base; C_alt = deficit x
p_rete - immessa x p_immissione +
O&M_alt (l'immissione e' un ricavo, segno
meno); risparmio = C_base - C_alt;
CO2 gas base = gas_base x f_co2_gas /
1000; CO2 rete base = E_el_base_tot x
f_co2_rete / 1000; CO2 base = somma dei
due; CO2 alt = (deficit - immessa) x
f_co2_rete / 1000 (credito CO2
sull'immissione allo stesso fattore rete,
scelta simmetrica documentata; puo'
essere negativa se l'immissione supera
il deficit); CO2 evitata = base - alt
(segno libero, non clampata: puo' essere
negativa se il deficit supera la base
elettrica totale piu' l'immissione);
flussi [-CAPEX, risparmio x vita]; VAN al
WACC (FRAZIONE, non percentuale); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo gas di pareggio
p* = (deficit x p_rete - immessa x
p_immissione + O&M_alt - E_el_base_tot x
p_rete - O&M_base) / gas_base in forma
chiusa a prezzi elettrici FERMI, None se
gas_base <= 0 o se p* < 0, SOGLIA MINIMA
sui soli costi annui quando esiste (sopra
di essa l'alternativa vince, sotto perde;
il CAPEX non entra nel pareggio annuo).
Nel demo p* e' None: a prezzo gas nullo
il risparmio resterebbe 23.280,00
EUR/anno (solo elettrico netto + O&M),
quindi l'alternativa vince sui costi
annui anche a gas gratis.
Verdetto: NON_CALCOLABILE se input
degenere (veicoli <= 0 o non interi,
giorni <= 0 o non interi, kwh_ev_giorno
< 0, superficie < 0, fabbisogni specifici
< 0, eta_caldaia <= 0 o > 1, prezzi < 0,
COP <= 0, quota_diretta < 0 o > 1,
RTE <= 0 o > 1, cap_batt < 0,
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
previsto (veicoli, giorni, vita, COP,
eta_caldaia, RTE). Gli zeri ammessi in
entrambi (kwh_ev_giorno, superficie,
fabbisogni specifici, prezzi, quota FV
diretta, cap_batt, DoD, cicli, kWp,
producibilita', O&M, CAPEX, fattori CO2,
WACC, tolleranza) non creano divergenza.
Quote e DoD > 1 e eta_caldaia > 1 sono
degeneri in entrambi ma non raggiungibili
via slider (tetto 1,0). WACC sopra 0,20 e
tolleranza sopra 1,0 sono ammessi negli
helper e limitati solo dagli slider UI
(0,20 e 1,0): nessuna divergenza nel range
raggiungibile, perche' la guard controlla
solo gli stessi limiti degli helper.
Distinzione esplicita: distinto dal
maneggio (driver box x giorni, LED arena
che tagliano solo la quota illuminazione:
qui driver superficie in mq piu'
ricarica EV veicoli x giorni x kWh,
senza LED) e dal campeggio stagionale
off-grid (150 giorni, senza rete,
eccesso FV sprecato senza credito: qui
300 giorni, con rete, eccesso immesso
e pagato, deficit prelevato a prezzo
pieno).

Demo (autosalone): 20 veicoli, 300
giorni, kwh_ev_giorno 15 (E_ev 90.000
kWh_e/anno), superficie 2.000 mq,
q_spec_termico 60 (Q_term 120.000
kWh_th/anno), e_spec 40 (E_el_base
80.000, E_el_base_tot 170.000
kWh_e/anno), eta_caldaia 0,90, prezzo
gas 0,10 EUR/kWh, prezzo prelievo rete
0,28 EUR/kWh, prezzo immissione 0,12
EUR/kWh, COP 3,0 (E_pdc 40.000,
E_tot_alt 210.000 kWh_e/anno),
quota_diretta 0,50, RTE 0,90, batteria
200 kWh con DoD 0,85 e 300 cicli/anno
(cap throughput 51.000 kWh_e/anno),
fotovoltaico 150 kWp a 1.100
kWh/kWp/anno (E_pv 165.000, diretta
82.500, batt lordo 82.500, batt netta
51.000, servita potenziale 133.500,
autoconsumo 133.500, deficit 76.500,
ciclata 56.666,666666666664, perdite
batt 5.666,666666666664, immessa
25.833,333333333336 con ricavo 3.100
EUR/anno, autonomia
0,24285714285714285 giorni), gas base
133.333,33333333334 kWh/anno (costo gas
13.333,333333333336, prelievo rete base
47.600,00000000001), O&M base 3.000,
O&M alt 9.000, CAPEX 320.000 EUR,
fattore CO2 gas 0,202 kg/kWh, fattore
CO2 rete 0,30 kg/kWh_e, WACC 0,05
(frazione), vita 20 anni, tolleranza
0,10 (frazione del CAPEX).
Valori calcolati eseguendo
mh842_demo_calcoli(): Q_term 120000,0,
E_el_base 80000,0, E_ev 90000,0,
E_el_base_tot 170000,0, E_pdc 40000,0,
E_tot_alt 210000,0, E_pv 165000,0,
diretta 82500,0, batt lordo 82500,0,
batt netta 51000,0, servita pot
133500,0, autoconsumo 133500,0, deficit
76500,0, ciclata 56666,666666666664,
perdite batt 5666,666666666664, immessa
25833,333333333336, autonomia
0,24285714285714285, gas base
133333,33333333334, costo gas
13333,333333333336, prelievo rete base
47600,00000000001, C_base
63933,33333333334, C_alt 27320,0,
risparmio 36613,33333333334, CO2 gas
base 26,933333333333337, CO2 rete base
51,0, CO2 base 77,93333333333334, CO2
alt 15,199999999999998, CO2 evitata
62,73333333333334, VAN
136283,06134153064, TIR
9,618589195964601 %, payback 9,
p_gas_pareggio None (a gas nullo il
risparmio resterebbe 23.280,00 EUR/anno),
verdetto CONVIENTE (VAN il 42,59 % del
CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab842 in app.py NON e'
incluso in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza in app.py spetta
alla fase di apply del worker, non a
questa fase. Tutti i test qui inclusi
passano da hidden_files senza app.py.

Destinazione nel repo: tests/test_w842_autosalone.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w845_helpers import (
        demo_calcoli,
        mh842_autonomia_batt,
        mh842_c_alt,
        mh842_c_base,
        mh842_calcola,
        mh842_co2_evitata,
        mh842_co2_gas,
        mh842_co2_rete,
        mh842_costo_gas,
        mh842_costo_rete_base,
        mh842_csv,
        mh842_demo,
        mh842_demo_calcoli,
        mh842_e_deficit,
        mh842_e_el_base,
        mh842_e_el_base_tot,
        mh842_e_ev,
        mh842_e_pdc,
        mh842_e_pv,
        mh842_e_tot_alt,
        mh842_eta,
        mh842_frazione,
        mh842_flussi,
        mh842_gas_kwh,
        mh842_int_pos,
        mh842_nneg,
        mh842_num,
        mh842_p_gas_pareggio,
        mh842_payback,
        mh842_pos,
        mh842_pv_autoconsumo,
        mh842_pv_batt_ciclata,
        mh842_pv_batt_lordo,
        mh842_pv_batt_netta,
        mh842_pv_diretta,
        mh842_pv_immessa,
        mh842_pv_perdite_batt,
        mh842_pv_servita_pot,
        mh842_q_termico,
        mh842_risparmio,
        mh842_sensibilita,
        mh842_tir,
        mh842_valida,
        mh842_van,
        mh842_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w845_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w845_helpers", os.path.join(_hf, "w845_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh842_autonomia_batt = _mod.mh842_autonomia_batt
    mh842_c_alt = _mod.mh842_c_alt
    mh842_c_base = _mod.mh842_c_base
    mh842_calcola = _mod.mh842_calcola
    mh842_co2_evitata = _mod.mh842_co2_evitata
    mh842_co2_gas = _mod.mh842_co2_gas
    mh842_co2_rete = _mod.mh842_co2_rete
    mh842_costo_gas = _mod.mh842_costo_gas
    mh842_costo_rete_base = _mod.mh842_costo_rete_base
    mh842_csv = _mod.mh842_csv
    mh842_demo = _mod.mh842_demo
    mh842_demo_calcoli = _mod.mh842_demo_calcoli
    mh842_e_deficit = _mod.mh842_e_deficit
    mh842_e_el_base = _mod.mh842_e_el_base
    mh842_e_el_base_tot = _mod.mh842_e_el_base_tot
    mh842_e_ev = _mod.mh842_e_ev
    mh842_e_pdc = _mod.mh842_e_pdc
    mh842_e_pv = _mod.mh842_e_pv
    mh842_e_tot_alt = _mod.mh842_e_tot_alt
    mh842_eta = _mod.mh842_eta
    mh842_frazione = _mod.mh842_frazione
    mh842_flussi = _mod.mh842_flussi
    mh842_gas_kwh = _mod.mh842_gas_kwh
    mh842_int_pos = _mod.mh842_int_pos
    mh842_nneg = _mod.mh842_nneg
    mh842_num = _mod.mh842_num
    mh842_p_gas_pareggio = _mod.mh842_p_gas_pareggio
    mh842_payback = _mod.mh842_payback
    mh842_pos = _mod.mh842_pos
    mh842_pv_autoconsumo = _mod.mh842_pv_autoconsumo
    mh842_pv_batt_ciclata = _mod.mh842_pv_batt_ciclata
    mh842_pv_batt_lordo = _mod.mh842_pv_batt_lordo
    mh842_pv_batt_netta = _mod.mh842_pv_batt_netta
    mh842_pv_diretta = _mod.mh842_pv_diretta
    mh842_pv_immessa = _mod.mh842_pv_immessa
    mh842_pv_perdite_batt = _mod.mh842_pv_perdite_batt
    mh842_pv_servita_pot = _mod.mh842_pv_servita_pot
    mh842_q_termico = _mod.mh842_q_termico
    mh842_risparmio = _mod.mh842_risparmio
    mh842_sensibilita = _mod.mh842_sensibilita
    mh842_tir = _mod.mh842_tir
    mh842_valida = _mod.mh842_valida
    mh842_van = _mod.mh842_van
    mh842_verdetto = _mod.mh842_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w845_helpers.py")
_UI_PATH = _risolvi("w845_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# tab precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "1_"
_VECCHIO_TAB = "tab84" + "1"
_VECCHIO_ST = "st84" + "1_"

_DEMO = {
    "q_termico_kwh_th_anno": 120000.0,
    "e_el_base_kwh_e_anno": 80000.0,
    "e_ev_kwh_e_anno": 90000.0,
    "e_el_base_tot_kwh_e_anno": 170000.0,
    "e_pdc_kwh_e_anno": 40000.0,
    "e_tot_alt_kwh_e_anno": 210000.0,
    "e_pv_kwh_e_anno": 165000.0,
    "e_pv_diretta_kwh_e_anno": 82500.0,
    "e_pv_batt_lordo_kwh_e_anno": 82500.0,
    "e_pv_batt_netta_kwh_e_anno": 51000.0,
    "e_pv_servita_pot_kwh_e_anno": 133500.0,
    "e_pv_autoconsumo_kwh_e_anno": 133500.0,
    "e_deficit_kwh_e_anno": 76500.0,
    "e_pv_batt_ciclata_kwh_e_anno": 56666.666666666664,
    "e_pv_perdite_batt_kwh_e_anno": 5666.666666666664,
    "e_pv_immessa_kwh_e_anno": 25833.333333333336,
    "autonomia_batt_giorni": 0.24285714285714285,
    "gas_base_kwh_anno": 133333.33333333334,
    "costo_gas_eur_anno": 13333.333333333336,
    "costo_rete_base_eur_anno": 47600.00000000001,
    "c_base_eur_anno": 63933.33333333334,
    "c_alt_eur_anno": 27320.000000000004,
    "risparmio_eur_anno": 36613.33333333334,
    "co2_gas_base_t_anno": 26.933333333333337,
    "co2_rete_base_t_anno": 51.0,
    "co2_base_t_anno": 77.93333333333334,
    "co2_alt_t_anno": 15.199999999999998,
    "co2_evitata_t_anno": 62.73333333333334,
    "van": 136283.06134153064,
    "tir": 9.618589195964601,
    "payback": 9,
    "p_gas_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh842_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh842_num(3, "x"), 3.0)
        self.assertEqual(mh842_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh842_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh842_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh842_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh842_pos(0, "x")
        with self.assertRaises(ValueError):
            mh842_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh842_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh842_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh842_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh842_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh842_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh842_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh842_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh842_frazione(0, "quota"), 0.0)
        self.assertEqual(mh842_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh842_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh842_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_termico_e_el_base_driver_superficie(self):
        self.assertEqual(mh842_q_termico(2000, 60), 120000.0)
        self.assertEqual(mh842_e_el_base(2000, 40), 80000.0)

    def test_ev_carico_additivo_veicoli_giorni_kwh(self):
        self.assertEqual(mh842_e_ev(20, 300, 15), 90000.0)
        self.assertEqual(mh842_e_ev(20, 300, 0), 0.0)
        self.assertEqual(mh842_e_el_base_tot(80000.0, 90000.0), 170000.0)

    def test_e_pdc_e_tot(self):
        self.assertAlmostEqual(mh842_e_pdc(120000.0, 3.0), 40000.0, places=6)
        self.assertAlmostEqual(mh842_e_tot_alt(40000.0, 80000.0, 90000.0), 210000.0, places=6)

    def test_pv_diretta_lordo(self):
        self.assertEqual(mh842_e_pv(150, 1100), 165000.0)
        self.assertEqual(mh842_pv_diretta(165000.0, 0.50), 82500.0)
        self.assertEqual(mh842_pv_batt_lordo(165000.0, 0.50), 82500.0)

    def test_batt_netta_cap_throughput_lega(self):
        self.assertEqual(mh842_pv_batt_netta(82500.0, 0.90, 200, 0.85, 300), 51000.0)
        self.assertEqual(mh842_pv_batt_netta(82500.0, 0.90, 10000, 0.85, 300), 74250.0)
        self.assertEqual(mh842_pv_batt_netta(82500.0, 0.90, 0, 0.85, 300), 0.0)

    def test_autoconsumo_cappato_a_domanda_e_immessa(self):
        self.assertEqual(mh842_pv_servita_pot(82500.0, 51000.0), 133500.0)
        self.assertEqual(mh842_pv_autoconsumo(133500.0, 210000.0), 133500.0)
        self.assertEqual(mh842_pv_autoconsumo(326000.0, 210000.0), 210000.0)
        self.assertEqual(mh842_pv_batt_ciclata(51000.0, 0.90), 56666.666666666664)
        self.assertEqual(mh842_pv_perdite_batt(56666.666666666664, 51000.0), 5666.666666666664)
        self.assertEqual(mh842_pv_immessa(165000.0, 133500.0, 5666.666666666664), 25833.333333333336)

    def test_immessa_mai_negativa_e_bilancio_pv(self):
        bc = mh842_demo_calcoli()
        self.assertGreaterEqual(bc["e_pv_immessa_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_autoconsumo_kwh_e_anno"]
                               + bc["e_pv_perdite_batt_kwh_e_anno"]
                               + bc["e_pv_immessa_kwh_e_anno"], places=6)
        grosso = mh842_calcola(**_demo_kwargs(p_pv_kwp=500))
        self.assertEqual(grosso["e_pv_autoconsumo_kwh_e_anno"], 210000.0)
        self.assertEqual(grosso["e_deficit_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(grosso["e_pv_immessa_kwh_e_anno"], 334333.3333333333, places=6)
        self.assertGreater(grosso["e_pv_immessa_kwh_e_anno"], 0.0)

    def test_deficit_e_autonomia(self):
        self.assertAlmostEqual(mh842_e_deficit(210000.0, 133500.0), 76500.0, places=6)
        self.assertAlmostEqual(mh842_autonomia_batt(200, 0.85, 210000.0, 300), 0.24285714285714285, places=12)
        self.assertEqual(mh842_autonomia_batt(200, 0.85, 0, 300), 0.0)

    def test_gas_e_prelievo_rete_base(self):
        self.assertEqual(mh842_gas_kwh(120000.0, 0.90), 133333.33333333334)
        self.assertAlmostEqual(mh842_costo_gas(133333.33333333334, 0.10), 13333.333333333336, places=6)
        self.assertAlmostEqual(mh842_costo_rete_base(170000.0, 0.28), 47600.0, places=6)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh842_c_base(13333.333333333336, 47600.0, 3000), 63933.33333333334, places=6)
        self.assertAlmostEqual(mh842_c_alt(76500.0, 0.28, 25833.333333333336, 0.12, 9000), 27320.0, places=6)

    def test_immissione_e_ricavo_non_spreco(self):
        # Con immissione a zero il costo alternativo sale del ricavo perso.
        base = mh842_demo_calcoli()
        senza_ricavo = mh842_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 3100.0, places=6)
        self.assertAlmostEqual(senza_ricavo["risparmio_eur_anno"],
                               base["risparmio_eur_anno"] - 3100.0, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh842_risparmio(63933.33333333334, 27320.0), 36613.33333333334, places=6)
        self.assertLess(mh842_risparmio(27320.0, 63933.33333333334), 0.0)

    def test_co2_due_fattori_e_evitata(self):
        self.assertAlmostEqual(mh842_co2_gas(133333.33333333334, 0.202), 26.933333333333337, places=6)
        self.assertAlmostEqual(mh842_co2_rete(170000.0, 0.30), 51.0, places=6)
        self.assertAlmostEqual(mh842_co2_rete(76500.0 - 25833.333333333336, 0.30), 15.2, places=6)
        self.assertAlmostEqual(mh842_co2_evitata(77.93333333333334, 15.2), 62.73333333333334, places=6)

    def test_co2_evitata_negativa_non_clampata_e_alt_negativa(self):
        self.assertAlmostEqual(mh842_co2_evitata(100.0, 200.0), -100.0, places=6)
        grosso = mh842_calcola(**_demo_kwargs(p_pv_kwp=500))
        self.assertLess(grosso["co2_alt_t_anno"], 0.0)
        self.assertAlmostEqual(grosso["co2_alt_t_anno"], -100.3, places=6)
        self.assertGreater(grosso["co2_evitata_t_anno"], grosso["co2_base_t_anno"])

    def test_immessa_con_ricavo_in_c_alt(self):
        bc = mh842_demo_calcoli()
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_deficit_kwh_e_anno"] * 0.28
                               - bc["e_pv_immessa_kwh_e_anno"] * 0.12 + 9000, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"],
                               bc["costo_gas_eur_anno"]
                               + bc["costo_rete_base_eur_anno"] + 3000, places=6)

    def test_ev_identica_in_baseline_e_alternativa(self):
        # La ricarica EV non cambia tra baseline e alternativa:
        # a kwh_ev_giorno 0 la domanda totale cala esattamente di E_ev.
        base = mh842_demo_calcoli()
        senza = mh842_calcola(**_demo_kwargs(kwh_ev_giorno=0))
        self.assertAlmostEqual(base["e_tot_alt_kwh_e_anno"]
                               - senza["e_tot_alt_kwh_e_anno"], 90000.0, places=6)
        self.assertAlmostEqual(base["e_el_base_tot_kwh_e_anno"]
                               - senza["e_el_base_tot_kwh_e_anno"], 90000.0, places=6)


class TestFinanza(unittest.TestCase):
    def test_p_gas_pareggio_demo_none_elettrico_supera_om(self):
        self.assertIsNone(mh842_demo_calcoli()["p_gas_pareggio"])
        self.assertIsNone(mh842_p_gas_pareggio(76500.0, 0.28, 25833.333333333336, 0.12,
                                              9000, 170000.0, 3000, 133333.33333333334))

    def test_p_gas_pareggio_none_casi(self):
        self.assertIsNone(mh842_p_gas_pareggio(76500.0, 0.28, 25833.333333333336, 0.12,
                                              9000, 170000.0, 3000, 0.0))
        self.assertIsNone(mh842_p_gas_pareggio(76500.0, 0.28, 25833.333333333336, 0.12,
                                              9000, 170000.0, 3000, 133333.33333333334))
        self.assertAlmostEqual(mh842_p_gas_pareggio(76500.0, 0.28, 25833.333333333336, 0.12,
                                             60000, 170000.0, 3000, 133333.33333333334),
                         0.2079, places=12)

    def test_p_gas_pareggio_positivo_a_om_alt_alto(self):
        bc = mh842_calcola(**_demo_kwargs(om_alt=60000))
        self.assertAlmostEqual(bc["p_gas_pareggio"], 0.2079, places=12)

    def test_p_gas_pareggio_verifica_a_om_alt_alto(self):
        bc = mh842_calcola(**_demo_kwargs(om_alt=60000))
        pstar = bc["p_gas_pareggio"]
        r = mh842_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_gas_pareggio_soglia_minima_a_om_alt_alto(self):
        bc = mh842_calcola(**_demo_kwargs(om_alt=60000))
        pstar = bc["p_gas_pareggio"]
        self.assertAlmostEqual(mh842_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar + 0.01))["risparmio_eur_anno"], 1333.3333333333285, places=6)
        self.assertAlmostEqual(mh842_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar - 0.01))["risparmio_eur_anno"], -1333.333333333343, places=6)

    def test_risparmio_a_gas_nullo_resta_positivo_ma_marginale(self):
        r = mh842_calcola(**_demo_kwargs(p_gas=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 23280.0, places=6)
        self.assertAlmostEqual(r["van"], -29879.743225669215, places=6)
        self.assertAlmostEqual(r["tir"], 3.8719733551428672, places=6)
        self.assertEqual(r["payback"], 14)
        self.assertEqual(r["verdetto"], "MARGINALE")

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh842_flussi(320000, 36613.33333333334, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -320000)
        self.assertTrue(all(f == 36613.33333333334 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh842_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 136283.06134153064, places=6)
        self.assertAlmostEqual(mh842_van([-320000] + [36613.33333333334] * 20, 0.0), 412266.66666666667, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh842_van([-320000] + [36613.33333333334] * 20, 0.05), 136283.06134153064, places=6)
        self.assertLess(mh842_van([-320000] + [36613.33333333334] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh842_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 9.618589195964601, places=6)
        self.assertGreater(bc["tir"], 9.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh842_payback([-320000] + [36613.33333333334] * 20), 9)
        self.assertEqual(mh842_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh842_payback([-320000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh842_verdetto(36613.33333333334, 100.0, 320000, 0.10), "CONVIENTE")
        self.assertEqual(mh842_verdetto(36613.33333333334, -20000.0, 320000, 0.10), "MARGINALE")
        self.assertEqual(mh842_verdetto(36613.33333333334, -100000.0, 320000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh842_verdetto(0.0, 100.0, 320000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh842_verdetto(-100.0, 100.0, 320000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh842_verdetto(None, 100.0, 320000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh842_verdetto(36613.33333333334, 0.0, 320000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh842_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("veicoli", "20"), ("veicoli", float("nan")),
                            ("veicoli", float("inf")), ("veicoli", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh842_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"veicoli": 0}, {"veicoli": -1},
                     {"veicoli": 20.5},
                     {"giorni_apertura": 0}, {"giorni_apertura": 300.5},
                     {"kwh_ev_giorno": -0.1},
                     {"superficie": -1},
                     {"q_spec_termico": -0.1}, {"e_spec_elettrico": -0.1},
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
            self.assertFalse(mh842_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh842_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh842_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh842_valida(**_demo_kwargs(
            kwh_ev_giorno=0, superficie=0,
            q_spec_termico=0, e_spec_elettrico=0,
            p_gas=0, p_rete=0, p_immissione=0, quota_diretta=0, cap_batt=0, dod=0,
            cicli_anno=0, p_pv_kwp=0, prod_specifica=0,
            om_base=0, om_alt=0, capex=0, f_co2_gas=0,
            f_co2_rete=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh842_demo()
        self.assertEqual(d["veicoli"], 20)
        self.assertEqual(d["giorni_apertura"], 300)
        self.assertEqual(d["kwh_ev_giorno"], 15)
        self.assertEqual(d["superficie"], 2000)
        self.assertEqual(d["q_spec_termico"], 60)
        self.assertEqual(d["e_spec_elettrico"], 40)
        self.assertEqual(d["eta_caldaia"], 0.90)
        self.assertEqual(d["p_gas"], 0.10)
        self.assertEqual(d["p_rete"], 0.28)
        self.assertEqual(d["p_immissione"], 0.12)
        self.assertEqual(d["cop"], 3.0)
        self.assertEqual(d["quota_diretta"], 0.50)
        self.assertEqual(d["rte"], 0.90)
        self.assertEqual(d["cap_batt"], 200)
        self.assertEqual(d["dod"], 0.85)
        self.assertEqual(d["cicli_anno"], 300)
        self.assertEqual(d["p_pv_kwp"], 150)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["om_base"], 3000)
        self.assertEqual(d["om_alt"], 9000)
        self.assertEqual(d["capex"], 320000)
        self.assertEqual(d["f_co2_gas"], 0.202)
        self.assertEqual(d["f_co2_rete"], 0.30)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh842_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh842_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], 120000.0, places=6)
        self.assertEqual(bc["e_el_base_kwh_e_anno"], 80000.0)
        self.assertEqual(bc["e_ev_kwh_e_anno"], 90000.0)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], 40000.0, places=6)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 165000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 63933.33333333334, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 27320.0, places=6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh842_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8], -27093.333333333227, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[9], 9520.000000000116, places=6)

    def test_demo_tabella_righe(self):
        bc = mh842_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Veicoli elettrici in vendita/demo", voci)
        self.assertIn("Ricarica EV (kWh_e/anno)", voci)
        self.assertIn("Elettricita' piena baseline (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico netto da batteria (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico immesso, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Perdite round-trip batteria (kWh_e/anno)", voci)
        self.assertIn("Autonomia batteria (giorni)", voci)
        self.assertIn("Gas baseline (kWh/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("Prezzo gas di pareggio (EUR/kWh, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh842_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"],
                               bc["superficie"] * bc["q_spec_termico"])
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] + bc["e_el_base_kwh_e_anno"] + bc["e_ev_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_tot_alt_kwh_e_anno"] - bc["e_pv_autoconsumo_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        qterm = 2000 * 60
        eelbase = 2000 * 40
        eev = 20 * 300 * 15
        eeltot = eelbase + eev
        epdc = qterm / 3.0
        etot = epdc + eelbase + eev
        e_pv = 150 * 1100
        diretta = e_pv * 0.50
        batt_netta = min(e_pv * 0.50 * 0.90, 200 * 0.85 * 300)
        autoconsumo = min(diretta + batt_netta, etot)
        ciclata = batt_netta / 0.90
        perdite = ciclata - batt_netta
        immessa = e_pv - autoconsumo - perdite
        gasb = qterm / 0.90
        deficit = etot - autoconsumo
        c_base = gasb * 0.10 + eeltot * 0.28 + 3000
        c_alt = deficit * 0.28 - immessa * 0.12 + 9000
        bc = mh842_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], qterm, places=6)
        self.assertAlmostEqual(bc["e_el_base_kwh_e_anno"], eelbase, places=6)
        self.assertAlmostEqual(bc["e_ev_kwh_e_anno"], eev, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"], etot, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_pv_autoconsumo_kwh_e_anno"], autoconsumo, places=6)
        self.assertAlmostEqual(bc["e_pv_immessa_kwh_e_anno"], immessa, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh842_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_gas_piu_meno_20(self):
        meno = mh842_calcola(**_demo_kwargs(p_gas=0.08))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 33946.66666666667, places=6)
        self.assertAlmostEqual(meno["van"], 103050.50042809064, places=6)
        self.assertAlmostEqual(meno["tir"], 8.553546115452091, places=6)
        self.assertEqual(meno["payback"], 10)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh842_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 39280.0, places=6)
        self.assertAlmostEqual(piu["van"], 169515.62225497043, places=6)
        self.assertAlmostEqual(piu["tir"], 10.654548214918403, places=6)
        self.assertEqual(piu["payback"], 9)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_gas_alto_migliora_il_caso(self):
        demo = mh842_demo_calcoli()
        meno = mh842_calcola(**_demo_kwargs(p_gas=0.08))
        piu = mh842_calcola(**_demo_kwargs(p_gas=0.12))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_non_calcolabile(self):
        r = mh842_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], -3866.666666666657, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["van"], -368187.21332448773, places=6)
        self.assertIsNone(r["tir"])
        self.assertIsNone(r["payback"])

    def test_variante_senza_batteria_convinte(self):
        r = mh842_calcola(**_demo_kwargs(cap_batt=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 29133.333333333343, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 43065.72797933158, places=6)
        self.assertAlmostEqual(r["tir"], 6.539543422747383, places=6)
        self.assertEqual(r["payback"], 11)

    def test_variante_senza_ev_convinte(self):
        r = mh842_calcola(**_demo_kwargs(kwh_ev_giorno=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 34453.33333333334, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 109364.68700164421, places=6)
        self.assertAlmostEqual(r["tir"], 8.75837293736907, places=6)
        self.assertEqual(r["payback"], 10)

    def test_variante_cop_basso_convinte(self):
        r = mh842_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 31013.333333333343, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 66494.68342330669, places=6)
        self.assertAlmostEqual(r["tir"], 7.342013891184871, places=6)
        self.assertEqual(r["payback"], 11)

    def test_variante_capex_doppio_non_convinte(self):
        r = mh842_calcola(**_demo_kwargs(capex=640000))
        self.assertAlmostEqual(r["van"], -183716.93865846936, places=6)
        self.assertAlmostEqual(r["tir"], 1.3183961451171025, places=6)
        self.assertEqual(r["payback"], 18)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh842_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -37281.545126113386, places=6)
        self.assertAlmostEqual(r["tir"], 2.526735123122475, places=6)
        self.assertEqual(r["payback"], 9)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh842_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 412266.66666666667, places=6)
        self.assertEqual(zero["payback"], 9)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh842_sensibilita(**mh842_demo())
        self.assertEqual(set(s.keys()), {"gas_meno20", "gas_piu20",
                                         "senza_pv", "senza_batt", "senza_ev",
                                         "cop_2", "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["gas_meno20"]["risparmio_eur_anno"], 33946.66666666667, places=6)
        self.assertAlmostEqual(s["gas_piu20"]["van"], 169515.62225497043, places=6)
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(s["senza_batt"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_ev"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh842_demo_calcoli()
        b = mh842_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh842_demo()
        attese = {"veicoli", "giorni_apertura", "kwh_ev_giorno",
                  "superficie", "q_spec_termico",
                  "e_spec_elettrico", "eta_caldaia",
                  "p_gas", "p_rete", "p_immissione", "cop", "quota_diretta", "rte",
                  "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                  "prod_specifica", "om_base", "om_alt", "capex",
                  "f_co2_gas", "f_co2_rete", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["veicoli", "giorni_apertura", "kwh_ev_giorno",
                 "superficie", "q_spec_termico",
                 "e_spec_elettrico", "eta_caldaia",
                 "p_gas", "p_rete", "p_immissione", "cop", "quota_diretta", "rte",
                 "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                 "prod_specifica", "om_base", "om_alt", "capex",
                 "f_co2_gas", "f_co2_rete", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh842_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh842_calcola(**_demo_kwargs(quota_diretta=1.1))
        with self.assertRaises(ValueError):
            mh842_calcola(**_demo_kwargs(dod=1.1))
        with self.assertRaises(ValueError):
            mh842_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh842_calcola(**_demo_kwargs(rte=1.1))
        with self.assertRaises(ValueError):
            mh842_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh842_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("veicoli", "20"), ("veicoli", float("nan")),
                           ("capex", float("inf")), ("p_gas", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh842_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh842_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_diretta=0,
                                         cap_batt=0, dod=0, cicli_anno=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_gas=0,
                                         f_co2_rete=0, kwh_ev_giorno=0,
                                         p_gas=0, p_rete=0,
                                         p_immissione=0))
        self.assertTrue(r["valid"])
        r2 = mh842_calcola(**_demo_kwargs(om_alt=60000, p_gas=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh842_calcola(**_demo_kwargs(om_alt=90000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        bc = mh842_calcola(**_demo_kwargs(om_alt=60000))
        pstar = bc["p_gas_pareggio"]
        r = mh842_calcola(**_demo_kwargs(om_alt=60000, p_gas=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh842_demo_calcoli()
        csv = mh842_csv(bc, dict(mh842_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh842_demo_calcoli()
        csv = mh842_csv(bc, dict(mh842_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]), 36613.33333333334, places=6)
        self.assertEqual(righe["p_gas_pareggio"], "")

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh842_demo_calcoli()
        csv = mh842_csv(bc, dict(mh842_demo()))
        for chiave in mh842_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn("mh840_", src)
        self.assertNotIn("mh839_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab842:"), 1)
        self.assertTrue(src.startswith("    # W845"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Autosalone: fotovoltaico + ricarica EV + pompa di calore battono caldaia a gas + prelievo da rete per showroom, officina e piazzale?", src)
        self.assertIn("🚗 Autosalone: fotovoltaico + ricarica EV + pompa di calore battono caldaia a gas + prelievo da rete per showroom, officina e piazzale?", src)
        self.assertNotIn(_VECCHIO_TAB, src)
        self.assertNotIn("tab840", src)
        self.assertNotIn("tab839", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in (_VECCHIO_MH, "mh840_", "mh839_", "mh838_"):
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
        self.assertNotIn("mh840_", src)
        self.assertNotIn("st840_", src)
        chiavi = re.findall(r'key="(st842_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st842_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st842_calcola"', src)
        self.assertIn('key="st842_csv"', src)
        self.assertIn('key="st842_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def842\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh842_demo().keys()), lette - set(mh842_demo().keys()))
        self.assertEqual(lette, set(mh842_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc842\['([^']+)'\]", src))
        attese = set(mh842_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg842"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
