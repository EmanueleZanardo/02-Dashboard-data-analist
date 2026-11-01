"""Test nuova scheda autogrill:
pompa di calore + recupero calore
cucina + FV pensiline battono caldaia
a gas + chiller?

Business case annuo di un'area di
servizio autostradale, connessa alla
rete, guidata dai PASTI AL GIORNO +
superficie sala + piazzale (non sala
generica, non ristorante generico, non
hotel, non mensa):
pasti_anno = pasti_giorno x giorni_anno;
Q_risc = superficie_sala_m2 x q_risc;
Q_acs = pasti_anno x litri_pasto x
4,186 x dT / 3600; Q_termico = Q_risc
+ Q_acs; Q_freddo_sale =
superficie_sala_m2 x q_freddo_sala;
Q_freddo_celle = pasti_anno x
freddo_celle_per_pasto; Q_freddo =
sale + celle; Gas_cucina = pasti_anno
x gas_cucina_per_pasto (invariato in
baseline e alternativa: la pompa di
calore non sostituisce i fornelli);
E_chiller_base = Q_freddo / EER_base;
E_pdc_freddo = Q_freddo / EER_alt;
Q_cond_alt = Q_freddo + E_pdc_freddo
(primo principio); Q_sorgente =
Gas_cucina + Q_cond_alt; Q_rec =
min(Q_termico, Q_sorgente x f_rec x
f_uso) (satura sulla domanda, solo la
frazione utilizzabile coincide con la
domanda); Q_net = max(0, Q_termico -
Q_rec); Gas_base = Q_termico /
eta_caldaia + Gas_cucina; Gas_alt =
Q_net / eta_caldaia + Gas_cucina;
E_pdc_risc = Q_net / COP_pdc;
E_pdc_alt = E_pdc_risc + E_pdc_freddo;
E_illum_base = superficie_sala_m2 x
e_illum_per_m2; E_illum_alt =
E_illum_base x (1 - risparmio_led);
E_base_el = E_chiller_base +
E_illum_base; E_alt_el = E_pdc_alt +
E_illum_alt; kWp pensiline =
superficie_piazzale_m2 x
quota_pensiline x 0,15 kWp/m2;
E_pv = kWp x producibilita';
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt_el) (cappato alla domanda
elettrica alternativa); E_immessa =
E_pv - E_pv_auto; E_deficit = max(0,
E_alt_el - E_pv_auto); C_base =
E_base_el x p_el + Gas_base x p_gas +
OM_base; C_alt = E_deficit x p_el -
E_immessa x p_immissione + Gas_alt x
p_gas + OM_alt (l'immessa e' un RICAVO
a prezzo di immissione, INFERIORE a
p_el; nessun credito CO2 per
l'immessa); risparmio = C_base -
C_alt; CAPEX forfettario; CO2 base =
E_base_el x f_el + Gas_base x f_gas;
CO2 alt = E_deficit x f_el + Gas_alt
x f_gas (fattori in t/kWh, nessuna
divisione per 1000; nessun credito
CO2 per l'immessa); CO2 evitata =
base - alt (segno libero);
flussi [-CAPEX, risparmio x vita];
VAN al WACC (PERCENTUALE in ingresso,
/ 100 dentro); TIR per bisezione;
payback (primo anno con cumulato >= 0);
prezzo elettrico di pareggio p_star =
(OM_alt - OM_base - (Gas_base -
Gas_alt) x p_gas - E_immessa x
p_immissione) / (E_base_el -
E_deficit) in forma chiusa a prezzo
gas, prezzo immissione e O&M FERMI,
None se E_base_el - E_deficit <= 0
o se p_star < 0, SOGLIA MINIMA sui
soli costi annui quando esiste (sopra
di essa l'alternativa vince, sotto
perde; il CAPEX non entra nel
pareggio annuo).
Nel demo p_star e' None, documentato:
il numeratore e' negativo (-5.911,87
EUR/anno), quindi l'alternativa vince
sui costi annui anche a prezzo
elettrico nullo. Un caso costruito
con pareggio positivo (niente termico:
q_risc 0 e litri 0, niente
fotovoltaico: quota pensiline 0) ha
p_star 0,15117644830068577 EUR/kWh: a
p_star il risparmio e' zero e il
verdetto e' NON_CALCOLABILE, a p_star
+ 0,01 il risparmio e' 396,89
EUR/anno, a p_star - 0,01 e'
-396,89 EUR/anno.
Verdetto: NON_CALCOLABILE se input
degenere (pasti <= 0, giorni < 0,
litri < 0, dT < 0, sala <= 0, q_risc
< 0, piazzale < 0, quota pensiline < 0
o > 1, freddo sale < 0, freddo celle
< 0, gas cucina < 0, EER base <= 0,
COP <= 0, EER alt <= 0, f_rec o f_uso
< 0 o > 1, illuminazione per m2 < 0,
risparmio LED < 0 o > 1,
producibilita' < 0, f_autoconsumo < 0
o > 1, eta caldaia <= 0 o > 1, prezzi
< 0, O&M < 0, CAPEX < 0, f_el < 0,
f_gas < 0, WACC < 0, vita <= 0 o non
intera, tolleranza < 0) o se risparmio
<= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se
VAN negativa entro tolleranza
PERCENTUALE del CAPEX, NON_CONVIENTE
se VAN negativa oltre la tolleranza.
Guard UI IDENTICA agli helper:
nessuna divergenza di verdetto. Tutti
gli slider UI hanno minimo 0, quindi i
casi negativi sono NON RAGGIUNGIBILI
via slider, ma la guard li controlla
comunque; i casi = 0 raggiungibili via
slider sono bloccati in UI esattamente
come negli helper dove previsto
(pasti, sala, EER base, COP, EER alt,
vita, rendimento caldaia). Gli zeri
ammessi in entrambi non creano
divergenza. Quote e frazioni > 1 sono
degeneri in entrambi ma non
raggiungibili via slider (tetto 1,0).
WACC sopra 20 e tolleranza sopra 100
sono ammessi negli helper e limitati
solo dagli slider UI (20 e 100):
nessuna divergenza nel range
raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper.

Demo (autogrill): 800 pasti/giorno x
365 giorni (292.000 pasti/anno), sala
600 m2 x 150 kWh_th/m2 (Q_risc
90.000), ACS 5 l/pasto x 35 K (Q_acs
59.417,94), Q_termico 149.417,94,
freddo sale 72.000, freddo celle
146.000, freddo totale 218.000, gas
cucina 233.600, EER base 2,8
(E_chiller 77.857,14), COP 3,5, EER
alt 3,8 (E_pdc_freddo 57.368,42),
Q_cond_alt 275.368,42, sorgente
508.968,42, f_rec 0,50 e f_uso 0,40
(Q_rec 101.793,68, Q_net 47.624,26),
eta caldaia 0,9 (Gas_base 399.619,94,
Gas_alt 286.515,84), piazzale 2.000 m2
x quota 0,35 x 0,15 (kWp 105,00),
fotovoltaico 115.500,00,
f_autoconsumo 0,70 (autoconsumo
80.850,00, deficit 18.925,35,
immessa 34.650,00), illuminazione
base 48.000, LED 28.800, domanda base
125.857,14, domanda alt 99.775,35,
prezzo elettrico 0,22, prezzo gas
0,09, prezzo immissione 0,05 EUR/kWh
(inferiore al prelievo), O&M base
10.000, O&M alt 16.000 EUR/anno,
CAPEX 220.000 EUR, f_el 0,00035
t/kWh, f_gas 0,00020 t/kWh, WACC 5
(percentuale), vita 15 anni,
tolleranza 10 (percentuale del CAPEX).
Valori calcolati eseguendo
mh848_demo_calcoli(): pasti_anno
292000,0, Q_risc 90000,0, Q_acs
59417,944444444445, Q_termico
149417,94444444444, Q_freddo_sale
72000,0, Q_freddo_celle 146000,0,
Q_freddo 218000,0, Gas_cucina
233600,0, E_chiller_base
77857,14285714286, E_pdc_freddo
57368,42105263158, Q_cond_alt
275368,4210526316, Q_sorgente
508968,4210526316, Q_rec
101793,68421052632, Q_net
47624,26023391812, Gas_base
399619,93827160494, Gas_alt
286515,8447043535, E_pdc_risc
13606,931495405177, E_pdc_alt
70975,35254803675, E_illum_base
48000,0, E_illum_alt 28800,0,
E_base_el 125857,14285714286,
E_alt_el 99775,35254803675, kWp
105,0, E_pv 115500,0, E_pv_auto
80850,0, E_immessa 34650,0,
E_deficit 18925,352548036753, C_base
73654,36587301586, C_alt
44217,5035839599, risparmio
29436,862289055964, CAPEX 220000,0,
CO2 base 123,973987654321, CO2 alt
63,92704233268356, CO2 evitata
60,04694532163743, VAN
85544,56427741483, TIR
10,309371807789542 %, payback 8,
p_el_pareggio None, verdetto
CONVIENTE.

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza della nuova scheda in
app.py e il count-assert sulle schede
NON sono inclusi in questo file perche'
questo authoring e' SOLO authoring
(niente apply, niente push, repo non
toccato): la verifica di presenza e del
conteggio in app.py spetta alla fase di
apply del worker, non a questa fase.
Tutti i test qui inclusi passano da
hidden_files senza app.py. La forma del
count in questa fase e' strutturale: il
blocco UI apre la scheda attesa
esattamente una volta e gli helper
definiscono le funzioni attese.
Questo schema e' lo STESSO usato da
w850_test.py (import diretto da
w850_helpers, NON via tests/appfuncs.py
load): replicato qui con w851_helpers.

Destinazione nel repo: tests dedicati
alla nuova scheda autogrill.
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w851_helpers import (
        demo_calcoli,
        mh848_c_alt,
        mh848_c_base,
        mh848_calcola,
        mh848_co2_alt,
        mh848_co2_base,
        mh848_co2_evitata,
        mh848_csv,
        mh848_demo,
        mh848_demo_calcoli,
        mh848_e_alt_el,
        mh848_e_base_el,
        mh848_e_chiller_base,
        mh848_e_deficit,
        mh848_e_illum_alt,
        mh848_e_illum_base,
        mh848_e_immessa,
        mh848_e_pdc_alt,
        mh848_e_pdc_freddo,
        mh848_e_pdc_risc,
        mh848_e_pv,
        mh848_e_pv_auto,
        mh848_eta,
        mh848_flussi,
        mh848_frazione,
        mh848_gas_alt,
        mh848_gas_base,
        mh848_gas_cucina,
        mh848_int_pos,
        mh848_nneg,
        mh848_num,
        mh848_p_el_pareggio,
        mh848_p_pv_kwp,
        mh848_pasti_anno,
        mh848_payback,
        mh848_pos,
        mh848_q_acs,
        mh848_q_cond_alt,
        mh848_q_freddo,
        mh848_q_freddo_celle,
        mh848_q_freddo_sale,
        mh848_q_net,
        mh848_q_rec,
        mh848_q_risc,
        mh848_q_sorgente,
        mh848_q_termico,
        mh848_risparmio,
        mh848_sensibilita,
        mh848_tir,
        mh848_valida,
        mh848_van,
        mh848_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w851_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w851_helpers", os.path.join(_hf, "w851_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh848_c_alt = _mod.mh848_c_alt
    mh848_c_base = _mod.mh848_c_base
    mh848_calcola = _mod.mh848_calcola
    mh848_co2_alt = _mod.mh848_co2_alt
    mh848_co2_base = _mod.mh848_co2_base
    mh848_co2_evitata = _mod.mh848_co2_evitata
    mh848_csv = _mod.mh848_csv
    mh848_demo = _mod.mh848_demo
    mh848_demo_calcoli = _mod.mh848_demo_calcoli
    mh848_e_alt_el = _mod.mh848_e_alt_el
    mh848_e_base_el = _mod.mh848_e_base_el
    mh848_e_chiller_base = _mod.mh848_e_chiller_base
    mh848_e_deficit = _mod.mh848_e_deficit
    mh848_e_illum_alt = _mod.mh848_e_illum_alt
    mh848_e_illum_base = _mod.mh848_e_illum_base
    mh848_e_immessa = _mod.mh848_e_immessa
    mh848_e_pdc_alt = _mod.mh848_e_pdc_alt
    mh848_e_pdc_freddo = _mod.mh848_e_pdc_freddo
    mh848_e_pdc_risc = _mod.mh848_e_pdc_risc
    mh848_e_pv = _mod.mh848_e_pv
    mh848_e_pv_auto = _mod.mh848_e_pv_auto
    mh848_eta = _mod.mh848_eta
    mh848_flussi = _mod.mh848_flussi
    mh848_frazione = _mod.mh848_frazione
    mh848_gas_alt = _mod.mh848_gas_alt
    mh848_gas_base = _mod.mh848_gas_base
    mh848_gas_cucina = _mod.mh848_gas_cucina
    mh848_int_pos = _mod.mh848_int_pos
    mh848_nneg = _mod.mh848_nneg
    mh848_num = _mod.mh848_num
    mh848_p_el_pareggio = _mod.mh848_p_el_pareggio
    mh848_p_pv_kwp = _mod.mh848_p_pv_kwp
    mh848_pasti_anno = _mod.mh848_pasti_anno
    mh848_payback = _mod.mh848_payback
    mh848_pos = _mod.mh848_pos
    mh848_q_acs = _mod.mh848_q_acs
    mh848_q_cond_alt = _mod.mh848_q_cond_alt
    mh848_q_freddo = _mod.mh848_q_freddo
    mh848_q_freddo_celle = _mod.mh848_q_freddo_celle
    mh848_q_freddo_sale = _mod.mh848_q_freddo_sale
    mh848_q_net = _mod.mh848_q_net
    mh848_q_rec = _mod.mh848_q_rec
    mh848_q_risc = _mod.mh848_q_risc
    mh848_q_sorgente = _mod.mh848_q_sorgente
    mh848_q_termico = _mod.mh848_q_termico
    mh848_risparmio = _mod.mh848_risparmio
    mh848_sensibilita = _mod.mh848_sensibilita
    mh848_tir = _mod.mh848_tir
    mh848_valida = _mod.mh848_valida
    mh848_van = _mod.mh848_van
    mh848_verdetto = _mod.mh848_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w851_helpers.py")
_UI_PATH = _risolvi("w851_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "7"
_VECCHIO_TAB = "tab84" + "7"
_VECCHIO_ST = "st84" + "7_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "pasti_anno": 292000.0,
    "q_risc_kwh_th_anno": 90000.0,
    "q_acs_kwh_th_anno": 59417.944444444445,
    "q_termico_kwh_th_anno": 149417.94444444444,
    "q_freddo_sale_kwh_c_anno": 72000.0,
    "q_freddo_celle_kwh_c_anno": 146000.0,
    "q_freddo_kwh_c_anno": 218000.0,
    "gas_cucina_kwh_anno": 233600.0,
    "e_chiller_base_kwh_e_anno": 77857.14285714286,
    "e_pdc_freddo_kwh_e_anno": 57368.42105263158,
    "q_cond_alt_kwh_c_anno": 275368.4210526316,
    "q_sorgente_kwh_th_anno": 508968.4210526316,
    "q_rec_kwh_th_anno": 101793.68421052632,
    "q_net_kwh_th_anno": 47624.26023391812,
    "gas_base_kwh_anno": 399619.93827160494,
    "gas_alt_kwh_anno": 286515.8447043535,
    "e_pdc_risc_kwh_e_anno": 13606.931495405177,
    "e_pdc_alt_kwh_e_anno": 70975.35254803675,
    "e_illum_base_kwh_e_anno": 48000.0,
    "e_illum_alt_kwh_e_anno": 28800.0,
    "e_base_el_kwh_e_anno": 125857.14285714286,
    "e_alt_el_kwh_e_anno": 99775.35254803675,
    "p_pv_kwp": 105.0,
    "e_pv_kwh_e_anno": 115500.0,
    "e_pv_auto_kwh_e_anno": 80850.0,
    "e_immessa_kwh_e_anno": 34650.0,
    "e_deficit_kwh_e_anno": 18925.352548036753,
    "c_base_eur_anno": 73654.36587301586,
    "c_alt_eur_anno": 44217.5035839599,
    "risparmio_eur_anno": 29436.862289055964,
    "capex_eur": 220000.0,
    "co2_base_t_anno": 123.973987654321,
    "co2_alt_t_anno": 63.92704233268356,
    "co2_evitata_t_anno": 60.04694532163743,
    "van": 85544.56427741483,
    "tir": 10.309371807789542,
    "payback": 8,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh848_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh848_num(3, "x"), 3.0)
        self.assertEqual(mh848_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh848_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh848_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh848_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh848_pos(0, "x")
        with self.assertRaises(ValueError):
            mh848_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh848_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh848_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh848_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh848_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh848_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh848_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh848_int_pos(15.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh848_frazione(0, "quota"), 0.0)
        self.assertEqual(mh848_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh848_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh848_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_pasti_e_termico(self):
        self.assertEqual(mh848_pasti_anno(800, 365), 292000.0)
        self.assertEqual(mh848_q_risc(600, 150), 90000.0)
        self.assertAlmostEqual(mh848_q_acs(292000.0, 5, 35),
                               59417.944444444445, places=6)
        self.assertAlmostEqual(mh848_q_termico(90000.0, 59417.944444444445),
                               149417.94444444444, places=6)
        self.assertEqual(mh848_q_acs(0, 5, 35), 0.0)
        self.assertEqual(mh848_q_acs(292000.0, 0, 35), 0.0)

    def test_freddo_sale_celle_e_totale(self):
        self.assertEqual(mh848_q_freddo_sale(600, 120), 72000.0)
        self.assertEqual(mh848_q_freddo_celle(292000.0, 0.50), 146000.0)
        self.assertEqual(mh848_q_freddo(72000.0, 146000.0), 218000.0)

    def test_gas_cucina_invariato_concetto(self):
        self.assertEqual(mh848_gas_cucina(292000.0, 0.80), 233600.0)
        bc = mh848_demo_calcoli()
        self.assertEqual(bc["gas_cucina_kwh_anno"], 233600.0)

    def test_chiller_e_pdc_freddo_e_cond(self):
        self.assertEqual(mh848_e_chiller_base(218000.0, 2.8),
                         77857.14285714286)
        self.assertEqual(mh848_e_pdc_freddo(218000.0, 3.8),
                         57368.42105263158)
        self.assertLess(mh848_e_pdc_freddo(218000.0, 3.8),
                        mh848_e_chiller_base(218000.0, 2.8))
        self.assertEqual(mh848_q_cond_alt(218000.0, 57368.42105263158),
                         275368.4210526316)
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["q_cond_alt_kwh_c_anno"],
                               bc["q_freddo_kwh_c_anno"]
                               + bc["e_pdc_freddo_kwh_e_anno"], places=6)

    def test_sorgente_rec_net(self):
        self.assertEqual(mh848_q_sorgente(233600.0, 275368.4210526316),
                         508968.4210526316)
        self.assertEqual(mh848_q_rec(149417.94444444444, 508968.4210526316,
                                     0.50, 0.40), 101793.68421052632)
        self.assertEqual(mh848_q_rec(10000.0, 508968.4210526316,
                                     0.50, 0.40), 10000.0)
        self.assertEqual(mh848_q_rec(149417.94444444444, 508968.4210526316,
                                     0.0, 0.40), 0.0)
        self.assertEqual(mh848_q_net(149417.94444444444, 101793.68421052632),
                         47624.26023391812)
        self.assertEqual(mh848_q_net(10000.0, 10000.0), 0.0)

    def test_gas_base_alt_cucina_invariata(self):
        self.assertAlmostEqual(mh848_gas_base(149417.94444444444, 0.9,
                                              233600.0),
                               399619.93827160494, places=6)
        self.assertAlmostEqual(mh848_gas_alt(47624.26023391812, 0.9,
                                             233600.0),
                               286515.8447043535, places=6)
        self.assertAlmostEqual(
            mh848_gas_base(149417.94444444444, 0.9, 233600.0)
            - mh848_gas_alt(47624.26023391812, 0.9, 233600.0),
            (149417.94444444444 - 47624.26023391812) / 0.9, places=6)

    def test_pdc_risc_e_illum_e_domande(self):
        self.assertAlmostEqual(mh848_e_pdc_risc(47624.26023391812, 3.5),
                               13606.931495405177, places=6)
        self.assertAlmostEqual(mh848_e_pdc_alt(13606.931495405177,
                                               57368.42105263158),
                               70975.35254803675, places=6)
        self.assertEqual(mh848_e_illum_base(600, 80), 48000.0)
        self.assertEqual(mh848_e_illum_alt(48000.0, 0.40), 28800.0)
        self.assertEqual(mh848_e_base_el(77857.14285714286, 48000.0),
                         125857.14285714286)
        self.assertAlmostEqual(mh848_e_alt_el(70975.35254803675, 28800.0),
                               99775.35254803675, places=6)

    def test_fv_pensiline_da_piazzale(self):
        self.assertEqual(mh848_p_pv_kwp(2000, 0.35), 105.0)
        self.assertEqual(mh848_p_pv_kwp(0, 0.35), 0.0)
        self.assertEqual(mh848_p_pv_kwp(2000, 0), 0.0)
        self.assertEqual(mh848_e_pv(105.0, 1100), 115500.0)
        self.assertEqual(mh848_e_pv_auto(115500.0, 0.70, 99775.35254803675),
                         80850.0)
        self.assertEqual(mh848_e_pv_auto(1155000.0, 0.70, 99775.35254803675),
                         99775.35254803675)
        self.assertEqual(mh848_e_immessa(115500.0, 80850.0), 34650.0)
        self.assertAlmostEqual(mh848_e_deficit(99775.35254803675, 80850.0),
                               18925.352548036753, places=6)

    def test_bilancio_fv_e_deficit(self):
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_auto_kwh_e_anno"]
                               + bc["e_immessa_kwh_e_anno"], places=6)
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_alt_el_kwh_e_anno"]
                               - bc["e_pv_auto_kwh_e_anno"], places=6)
        self.assertGreaterEqual(bc["e_immessa_kwh_e_anno"], 0.0)
        self.assertGreaterEqual(bc["e_deficit_kwh_e_anno"], 0.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh848_c_base(125857.14285714286, 0.22,
                                            399619.93827160494, 0.09,
                                            10000), 73654.36587301586,
                               places=6)
        self.assertAlmostEqual(mh848_c_alt(18925.352548036753, 0.22,
                                           34650.0, 0.05,
                                           286515.8447043535, 0.09,
                                           16000), 44217.5035839599,
                               places=6)

    def test_immessa_ricavo_a_prezzo_inferiore_non_pieno(self):
        base = mh848_demo_calcoli()
        senza_ricavo = mh848_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 1732.5, places=6)
        self.assertEqual(senza_ricavo["co2_alt_t_anno"],
                         base["co2_alt_t_anno"])

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh848_risparmio(73654.36587301586,
                                              44217.5035839599),
                               29436.862289055964, places=6)

    def test_co2_base_alt_evitata_senza_credito_immessa(self):
        self.assertAlmostEqual(mh848_co2_base(125857.14285714286, 0.00035,
                                              399619.93827160494, 0.00020),
                               123.973987654321, places=6)
        self.assertAlmostEqual(mh848_co2_alt(18925.352548036753, 0.00035,
                                             286515.8447043535, 0.00020),
                               63.92704233268356, places=6)
        self.assertAlmostEqual(mh848_co2_evitata(123.973987654321,
                                                63.92704233268356),
                               60.04694532163743, places=6)

    def test_fv_nullo_ammesso(self):
        r = mh848_calcola(**_demo_kwargs(quota_pensiline=0))
        self.assertEqual(r["p_pv_kwp"], 0.0)
        self.assertEqual(r["e_pv_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_pv_auto_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_immessa_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_deficit_kwh_e_anno"],
                         r["e_alt_el_kwh_e_anno"])
        self.assertTrue(r["valid"])

    def test_calcola_accetta_dict_singolo(self):
        a = mh848_calcola(mh848_demo())
        b = mh848_calcola(**mh848_demo())
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])
        self.assertEqual(a["verdetto"], b["verdetto"])
        with self.assertRaises(ValueError):
            mh848_calcola("non-un-dict")


class TestFinanza(unittest.TestCase):
    def test_p_el_pareggio_demo_none(self):
        bc = mh848_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh848_p_el_pareggio(10000, 16000,
                                              399619.93827160494,
                                              286515.8447043535, 0.09,
                                              34650.0, 0.05,
                                              125857.14285714286,
                                              18925.352548036753))

    def test_p_el_pareggio_none_casi(self):
        self.assertIsNone(mh848_p_el_pareggio(10000, 16000, 0.0, 0.0,
                                              0.09, 0.0, 0.05,
                                              99775.35254803675,
                                              99775.35254803675))

    def test_p_el_pareggio_costruito_positivo(self):
        base = _demo_kwargs(q_risc=0, litri_pasto=0,
                            quota_pensiline=0)
        bc = mh848_calcola(**base)
        self.assertAlmostEqual(bc["p_el_pareggio"],
                               0.15117644830068577, places=12)

    def test_p_el_pareggio_verifica(self):
        base = _demo_kwargs(q_risc=0, litri_pasto=0,
                            quota_pensiline=0)
        bc = mh848_calcola(**base)
        pstar = bc["p_el_pareggio"]
        r = mh848_calcola(**_demo_kwargs(q_risc=0, litri_pasto=0,
                                         quota_pensiline=0,
                                         p_el=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_el_pareggio_soglia_minima(self):
        base = _demo_kwargs(q_risc=0, litri_pasto=0,
                            quota_pensiline=0)
        pstar = mh848_calcola(**base)["p_el_pareggio"]
        self.assertAlmostEqual(
            mh848_calcola(**_demo_kwargs(q_risc=0, litri_pasto=0,
                                         quota_pensiline=0,
                                         p_el=pstar + 0.01))
            ["risparmio_eur_anno"], 396.88721804510715, places=6)
        self.assertAlmostEqual(
            mh848_calcola(**_demo_kwargs(q_risc=0, litri_pasto=0,
                                         quota_pensiline=0,
                                         p_el=pstar - 0.01))
            ["risparmio_eur_anno"], -396.8872180451144, places=6)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh848_flussi(220000, 29436.862289055964, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -220000)
        self.assertTrue(all(f == 29436.862289055964 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 85544.56427741483, places=6)
        self.assertAlmostEqual(mh848_van([-220000] + [29436.862289055964] * 15,
                                         0.0), 221552.93433583935, places=6)

    def test_van_usa_percentuale_non_frazione(self):
        self.assertAlmostEqual(mh848_van([-220000] + [29436.862289055964] * 15,
                                         5.0), 85544.56427741483, places=6)
        self.assertGreater(mh848_van([-220000] + [29436.862289055964] * 15, 0.05),
                           85544.56427741483)

    def test_tir_demo_e_none(self):
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 10.309371807789542, places=6)
        self.assertGreater(bc["tir"], 10.0)
        self.assertIsNone(mh848_tir([-100.0, -10.0, -10.0]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh848_payback([-220000] + [29436.862289055964] * 15), 8)
        self.assertEqual(mh848_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh848_payback([-220000] + [100.0] * 15))

    def test_verdetto_percentuale(self):
        self.assertEqual(mh848_verdetto(29436.862289055964, 100.0, 220000, 10),
                         "CONVIENTE")
        self.assertEqual(mh848_verdetto(29436.862289055964, -20000.0, 220000, 10),
                         "MARGINALE")
        self.assertEqual(mh848_verdetto(29436.862289055964, -100000.0, 220000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh848_verdetto(0.0, 100.0, 220000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh848_verdetto(-100.0, 100.0, 220000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh848_verdetto(None, 100.0, 220000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh848_verdetto(29436.862289055964, 0.0, 220000, 10),
                         "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh848_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("pasti_giorno", "800"),
                            ("pasti_giorno", float("nan")),
                            ("pasti_giorno", float("inf")),
                            ("pasti_giorno", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh848_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"pasti_giorno": 0},
                     {"pasti_giorno": -1},
                     {"giorni_anno": -1},
                     {"litri_pasto": -1},
                     {"acs_dt": -1},
                     {"superficie_sala_m2": 0},
                     {"superficie_sala_m2": -1},
                     {"q_risc": -1},
                     {"superficie_piazzale_m2": -1},
                     {"quota_pensiline": -0.1},
                     {"quota_pensiline": 1.1},
                     {"q_freddo_sala": -1},
                     {"freddo_celle_per_pasto": -1},
                     {"gas_cucina_per_pasto": -1},
                     {"eer_base": 0},
                     {"eer_base": -1},
                     {"cop_pdc": 0},
                     {"cop_pdc": -1},
                     {"eer_alt": 0},
                     {"eer_alt": -1},
                     {"f_rec": -0.1},
                     {"f_rec": 1.1},
                     {"f_uso": -0.1},
                     {"f_uso": 1.1},
                     {"e_illum_per_m2": -1},
                     {"risparmio_led": -0.1},
                     {"risparmio_led": 1.1},
                     {"prod_specifica": -1},
                     {"f_autoconsumo": -0.1},
                     {"f_autoconsumo": 1.1},
                     {"eta_caldaia": 0},
                     {"eta_caldaia": 1.1},
                     {"p_el": -0.1},
                     {"p_gas": -0.1},
                     {"p_immissione": -0.1},
                     {"om_base": -1},
                     {"om_alt": -1},
                     {"capex": -1},
                     {"f_el": -0.1},
                     {"f_gas": -0.1},
                     {"wacc": -0.1},
                     {"vita": 0},
                     {"vita": 15.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh848_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh848_valida(**_demo_kwargs(wacc=25))["valido"])
        self.assertTrue(mh848_valida(**_demo_kwargs(tolleranza=150))["valido"])
        self.assertTrue(mh848_valida(**_demo_kwargs(
            giorni_anno=0, litri_pasto=0, acs_dt=0, q_risc=0,
            superficie_piazzale_m2=0, quota_pensiline=0,
            q_freddo_sala=0, freddo_celle_per_pasto=0,
            gas_cucina_per_pasto=0, f_rec=0, f_uso=0,
            e_illum_per_m2=0, risparmio_led=0, prod_specifica=0,
            f_autoconsumo=0, p_el=0, p_gas=0, p_immissione=0,
            om_base=0, om_alt=0, capex=0, f_el=0, f_gas=0,
            wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh848_demo()
        self.assertEqual(d["pasti_giorno"], 800)
        self.assertEqual(d["giorni_anno"], 365)
        self.assertEqual(d["litri_pasto"], 5)
        self.assertEqual(d["acs_dt"], 35)
        self.assertEqual(d["superficie_sala_m2"], 600)
        self.assertEqual(d["q_risc"], 150)
        self.assertEqual(d["superficie_piazzale_m2"], 2000)
        self.assertEqual(d["quota_pensiline"], 0.35)
        self.assertEqual(d["q_freddo_sala"], 120)
        self.assertEqual(d["freddo_celle_per_pasto"], 0.50)
        self.assertEqual(d["gas_cucina_per_pasto"], 0.80)
        self.assertEqual(d["eer_base"], 2.8)
        self.assertEqual(d["cop_pdc"], 3.5)
        self.assertEqual(d["eer_alt"], 3.8)
        self.assertEqual(d["f_rec"], 0.50)
        self.assertEqual(d["f_uso"], 0.40)
        self.assertEqual(d["e_illum_per_m2"], 80)
        self.assertEqual(d["risparmio_led"], 0.40)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["f_autoconsumo"], 0.70)
        self.assertEqual(d["eta_caldaia"], 0.9)
        self.assertEqual(d["p_el"], 0.22)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["p_immissione"], 0.05)
        self.assertEqual(d["om_base"], 10000)
        self.assertEqual(d["om_alt"], 16000)
        self.assertEqual(d["capex"], 220000)
        self.assertEqual(d["f_el"], 0.00035)
        self.assertEqual(d["f_gas"], 0.00020)
        self.assertEqual(d["wacc"], 5)
        self.assertEqual(d["vita"], 15)
        self.assertEqual(d["tolleranza"], 10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh848_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["q_freddo_kwh_c_anno"], 218000.0, places=6)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 115500.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 73654.36587301586, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 44217.5035839599, places=6)
        self.assertEqual(bc["capex_eur"], 220000.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh848_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7],
                               -13941.963976608298, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[8],
                               15494.898312447665, places=6)

    def test_demo_tabella_righe(self):
        bc = mh848_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Pasti all'anno", voci)
        self.assertIn("Freddo totale sale + celle (kWh_c/anno)", voci)
        self.assertIn("Gas cucina (kWh/anno)", voci)
        self.assertIn("Sorgente calore cucina + celle (kWh_th/anno)", voci)
        self.assertIn("Calore recuperato (kWh_th/anno)", voci)
        self.assertIn("Domanda elettrica alternativa (kWh_e/anno)", voci)
        self.assertIn("Potenza FV pensiline (kWp)", voci)
        self.assertIn("Energia immessa, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("CAPEX totale (EUR)", voci)
        self.assertIn("Prezzo elettrico di pareggio (EUR/kWh, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["pasti_anno"],
                               bc["pasti_giorno"] * bc["giorni_anno"])
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"],
                               bc["q_risc_kwh_th_anno"]
                               + bc["q_acs_kwh_th_anno"])
        self.assertAlmostEqual(bc["q_net_kwh_th_anno"],
                               bc["q_termico_kwh_th_anno"]
                               - bc["q_rec_kwh_th_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(bc["gas_base_kwh_anno"],
                               bc["q_termico_kwh_th_anno"]
                               / bc["eta_caldaia"]
                               + bc["gas_cucina_kwh_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        pastia = 800 * 365
        qr = 600 * 150
        qacs = pastia * 5 * 4.186 * 35 / 3600
        qterm = qr + qacs
        qfsale = 600 * 120
        qfcelle = pastia * 0.50
        qfreddo = qfsale + qfcelle
        gcuc = pastia * 0.80
        echill = qfreddo / 2.8
        epdcfred = qfreddo / 3.8
        qcond = qfreddo + epdcfred
        qsorg = gcuc + qcond
        qrec = min(qterm, qsorg * 0.50 * 0.40)
        qnet = max(0, qterm - qrec)
        gbase = qterm / 0.9 + gcuc
        galt = qnet / 0.9 + gcuc
        epdcrisc = qnet / 3.5
        epdcalt = epdcrisc + epdcfred
        eillb = 600 * 80
        eilla = eillb * (1 - 0.40)
        ebase = echill + eillb
        ealt = epdcalt + eilla
        ppv = 2000 * 0.35 * 0.15
        epv = ppv * 1100
        eauto = min(epv * 0.70, ealt)
        edef = max(0, ealt - eauto)
        eimm = epv - eauto
        c_base = ebase * 0.22 + gbase * 0.09 + 10000
        c_alt = edef * 0.22 - eimm * 0.05 + galt * 0.09 + 16000
        bc = mh848_demo_calcoli()
        self.assertAlmostEqual(bc["q_risc_kwh_th_anno"], qr, places=6)
        self.assertAlmostEqual(bc["q_acs_kwh_th_anno"], qacs, places=6)
        self.assertAlmostEqual(bc["q_freddo_kwh_c_anno"], qfreddo, places=6)
        self.assertAlmostEqual(bc["gas_cucina_kwh_anno"], gcuc, places=6)
        self.assertAlmostEqual(bc["q_sorgente_kwh_th_anno"], qsorg, places=6)
        self.assertAlmostEqual(bc["q_rec_kwh_th_anno"], qrec, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], epv, places=6)
        self.assertAlmostEqual(bc["e_pv_auto_kwh_e_anno"], eauto, places=6)
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"], edef, places=6)
        self.assertAlmostEqual(bc["e_immessa_kwh_e_anno"], eimm, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt,
                               places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh848_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_p_el_piu_meno_20(self):
        meno = mh848_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 24731.863515455305,
                               places=6)
        self.assertAlmostEqual(meno["van"], 36708.28593738092, places=6)
        self.assertAlmostEqual(meno["tir"], 7.376166736563332, places=6)
        self.assertEqual(meno["payback"], 9)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh848_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 34141.86106265664,
                               places=6)
        self.assertAlmostEqual(piu["van"], 134380.84261744886, places=6)
        self.assertAlmostEqual(piu["tir"], 13.056076089599456, places=6)
        self.assertEqual(piu["payback"], 7)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_p_el_alto_migliora_il_caso(self):
        demo = mh848_demo_calcoli()
        meno = mh848_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh848_calcola(**_demo_kwargs(p_el=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_non_convinte(self):
        r = mh848_calcola(**_demo_kwargs(quota_pensiline=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 9917.362289055964,
                               places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -117061.17079885119, places=6)
        self.assertAlmostEqual(r["tir"], -4.534826699551392, places=6)
        self.assertIsNone(r["payback"])

    def test_variante_senza_recupero_non_convinte(self):
        r = mh848_calcola(**_demo_kwargs(f_rec=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 12859.033717627397,
                               places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -86527.62730959353, places=6)
        self.assertAlmostEqual(r["tir"], -1.6008152016417538, places=6)
        self.assertIsNone(r["payback"])

    def test_variante_senza_led_convinte(self):
        r = mh848_calcola(**_demo_kwargs(risparmio_led=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 25212.862289055964,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 41700.88872414, places=6)

    def test_variante_capex_doppio_non_convinte(self):
        r = mh848_calcola(**_demo_kwargs(capex=440000))
        self.assertAlmostEqual(r["van"], -134455.43572258516, places=6)
        self.assertAlmostEqual(r["tir"], 0.04407214118242264, places=6)
        self.assertEqual(r["payback"], 15)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["capex_eur"], 440000.0)

    def test_variante_capex_marginale(self):
        r = mh848_calcola(**_demo_kwargs(capex=320000))
        self.assertAlmostEqual(r["van"], -14455.435722585196, places=6)
        self.assertAlmostEqual(r["tir"], 4.32393518451266, places=6)
        self.assertEqual(r["payback"], 11)
        self.assertEqual(r["verdetto"], "MARGINALE")

    def test_variante_vita_10_convinte(self):
        r = mh848_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 7303.6477430065825, places=6)
        self.assertAlmostEqual(r["tir"], 5.678172290609209, places=6)
        self.assertEqual(r["payback"], 8)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh848_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 221552.93433583935, places=6)
        self.assertEqual(zero["payback"], 8)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh848_sensibilita(**mh848_demo())
        self.assertEqual(set(s.keys()), {"p_el_meno20", "p_el_piu20",
                                         "senza_fv", "senza_recupero",
                                         "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               24731.863515455305, places=6)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               134380.84261744886, places=6)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_recupero"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh848_demo_calcoli()
        b = mh848_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh848_demo()
        attese = {"pasti_giorno", "giorni_anno", "litri_pasto", "acs_dt",
                  "superficie_sala_m2", "q_risc",
                  "superficie_piazzale_m2", "quota_pensiline",
                  "q_freddo_sala", "freddo_celle_per_pasto",
                  "gas_cucina_per_pasto", "eer_base", "cop_pdc",
                  "eer_alt", "f_rec", "f_uso", "e_illum_per_m2",
                  "risparmio_led", "prod_specifica", "f_autoconsumo",
                  "eta_caldaia", "p_el", "p_gas", "p_immissione",
                  "om_base", "om_alt", "capex", "f_el", "f_gas",
                  "wacc", "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["pasti_giorno", "giorni_anno", "litri_pasto", "acs_dt",
                 "superficie_sala_m2", "q_risc",
                 "superficie_piazzale_m2", "quota_pensiline",
                 "q_freddo_sala", "freddo_celle_per_pasto",
                 "gas_cucina_per_pasto", "eer_base", "cop_pdc",
                 "eer_alt", "f_rec", "f_uso", "e_illum_per_m2",
                 "risparmio_led", "prod_specifica", "f_autoconsumo",
                 "eta_caldaia", "p_el", "p_gas", "p_immissione",
                 "om_base", "om_alt", "capex", "f_el", "f_gas",
                 "wacc", "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh848_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_cop_zero_pasti_zero_e_vita(self):
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(quota_pensiline=1.1))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(f_rec=1.1))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(f_uso=1.1))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(f_autoconsumo=1.1))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(cop_pdc=0))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(eer_base=0))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(eer_alt=0))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(pasti_giorno=0))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(superficie_sala_m2=0))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh848_calcola(**_demo_kwargs(vita=15.5))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("pasti_giorno", "800"),
                           ("pasti_giorno", float("nan")),
                           ("capex", float("inf")),
                           ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh848_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh848_calcola(**_demo_kwargs(
            giorni_anno=0, litri_pasto=0, acs_dt=0, q_risc=0,
            superficie_piazzale_m2=0, quota_pensiline=0,
            q_freddo_sala=0, freddo_celle_per_pasto=0,
            gas_cucina_per_pasto=0, f_rec=0, f_uso=0,
            e_illum_per_m2=0, risparmio_led=0, prod_specifica=0,
            f_autoconsumo=0, p_el=0, p_gas=0, p_immissione=0,
            om_base=0, om_alt=0, capex=0, f_el=0, f_gas=0,
            wacc=0, tolleranza=0))
        self.assertTrue(r["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh848_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(r["risparmio_eur_anno"], -154563.13771094402,
                               places=6)

    def test_pareggio_esatto_soglia(self):
        base = _demo_kwargs(q_risc=0, litri_pasto=0,
                            quota_pensiline=0)
        pstar = mh848_calcola(**base)["p_el_pareggio"]
        r = mh848_calcola(**_demo_kwargs(q_risc=0, litri_pasto=0,
                                         quota_pensiline=0,
                                         p_el=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh848_demo_calcoli()
        csv = mh848_csv(bc, dict(mh848_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh848_demo_calcoli()
        csv = mh848_csv(bc, dict(mh848_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1]
                 for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]),
                               29436.862289055964, places=6)
        self.assertIn("p_el_pareggio", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh848_demo_calcoli()
        csv = mh848_csv(bc, dict(mh848_demo()))
        for chiave in mh848_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn(_IMP_STREAMLIT, src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab848:"), 1)
        self.assertTrue(src.startswith("    # W851"))

    def test_ui_tab848_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab848:"), 1)
        self.assertIn("def mh848_demo(", src_h)
        self.assertIn("def mh848_calcola(", src_h)
        self.assertIn("tab848", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Autogrill: pompa di calore + recupero calore cucina + FV pensiline battono caldaia a gas + chiller?", src)
        self.assertIn("🛣️ Autogrill: pompa di calore + recupero calore cucina + FV pensiline battono caldaia a gas + chiller?", src)
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
        chiavi = re.findall(r'key="(st848_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st848_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st848_calcola"', src)
        self.assertIn('key="st848_csv"', src)
        self.assertIn('key="st848_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def848\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh848_demo().keys()), lette - set(mh848_demo().keys()))
        self.assertEqual(lette, set(mh848_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc848\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc848\["([^"]+)"\]', src))
        attese = set(mh848_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg848"), src.index(".paiac("))
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
            self.assertNotIn("\u2014", src)
            self.assertNotIn("\u2013", src)


if __name__ == "__main__":
    unittest.main()
