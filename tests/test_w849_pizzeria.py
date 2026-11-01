"""Test nuova scheda pizzeria:
forno elettrico con recupero fumi +
pompa di calore batte il forno a gas?

Business case annuo di una pizzeria,
connessa alla rete, guidata dalle PIZZE
AL GIORNO + superficie sala + tetto (non
panificio, non ristorante generico, non
autogrill):
pizze_anno = pizze_giorno x giorni_anno;
Q_risc = superficie_sala_m2 x q_risc;
Q_acs = pizze_anno x litri_pizza x
4,186 x dT / 3600; Q_termico = Q_risc
+ Q_acs; Q_freddo_sale =
superficie_sala_m2 x q_freddo_sala;
Q_freddo_celle = pizze_anno x
freddo_celle_per_pizza; Q_freddo =
sale + celle; Gas_forno_base = pizze_anno
x gas_forno_per_pizza (SCOMPARE
nell'alternativa: il forno elettrico non
brucia gas); E_forno_alt = pizze_anno
x e_forno_per_pizza (rientra nella
domanda elettrica alternativa totale);
Q_disp = E_forno_alt x f_disp (solo la
quota f_disp diventa calore
recuperabile); E_chiller_base = Q_freddo
/ EER_base; E_pdc_freddo = Q_freddo /
EER_alt; Q_cond_alt = Q_freddo +
E_pdc_freddo (primo principio);
Q_sorgente = Q_disp + Q_cond_alt;
Q_rec = min(Q_termico, Q_sorgente x
f_rec x f_uso) (satura sulla domanda,
solo la frazione utilizzabile coincide
con la domanda); Q_net = max(0,
Q_termico - Q_rec); Gas_base = Q_termico
/ eta_caldaia + Gas_forno_base; Gas_alt
= Q_net / eta_caldaia (senza gas forno);
E_pdc_risc = Q_net / COP_pdc;
E_pdc_alt = E_pdc_risc + E_pdc_freddo;
E_illum_base = superficie_sala_m2 x
e_illum_per_m2; E_illum_alt =
E_illum_base x (1 - risparmio_led);
E_base_el = E_chiller_base +
E_illum_base (il forno a gas non consuma
elettricita'); E_alt_el = E_pdc_alt +
E_illum_alt + E_forno_alt; kWp tetto =
superficie_tetto_m2 x quota_tetto x
0,18 kWp/m2; E_pv = kWp x
producibilita'; E_pv_auto = min(E_pv x
f_autoconsumo, E_alt_el) (cappato alla
domanda elettrica alternativa);
E_immessa = E_pv - E_pv_auto; E_deficit
= max(0, E_alt_el - E_pv_auto); C_base =
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
il numeratore e' negativo (-15.649,61
EUR/anno), quindi l'alternativa vince
sui costi annui anche a prezzo
elettrico nullo. Un caso costruito
con pareggio positivo (niente termico:
q_risc 0 e litri 0, niente
fotovoltaico: quota tetto 0, EER base
2,0, EER alt 5,0, risparmio LED 0,80,
gas forno 0,30, elettricita' forno
0,05, O&M alt 12.000) ha p_star
0,12011834319526628 EUR/kWh: a
p_star il risparmio e' zero e il
verdetto e' NON_CALCOLABILE, a p_star
+ 0,01 il risparmio e' 202,80
EUR/anno, a p_star - 0,01 e'
-202,80 EUR/anno.
Verdetto: NON_CALCOLABILE se input
degenere (pizze <= 0, giorni < 0,
litri < 0, dT < 0, sala <= 0, q_risc
< 0, tetto < 0, quota tetto < 0 o > 1,
freddo sale < 0, freddo celle < 0,
gas forno < 0, elettricita' forno < 0,
f_disp < 0 o > 1, EER base <= 0,
COP <= 0, EER alt <= 0, f_rec o f_uso
< 0 o > 1, illuminazione per m2 < 0,
risparmio LED < 0 o > 1,
producibilita' < 0, f_autoconsumo < 0 o
> 1, eta caldaia <= 0 o > 1, prezzi
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
(pizze, sala, EER base, COP, EER alt,
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

Demo (pizzeria): 400 pizze/giorno x
330 giorni (132.000 pizze/anno), sala
150 m2 x 150 kWh_th/m2 (Q_risc
22.500), ACS 2 l/pizza x 35 K (Q_acs
10.744,07), Q_termico 33.244,07,
freddo sale 18.000, freddo celle
39.600, freddo totale 57.600, gas
forno 158.400 (SCOMPARE in alt),
elettricita' forno 79.200, calore
dissipato forno 39.600, EER base 2,8
(E_chiller 20.571,43), COP 3,5, EER
alt 3,8 (E_pdc_freddo 15.157,89),
Q_cond_alt 72.757,89, sorgente
112.357,89, f_rec 0,60 e f_uso 0,50
(Q_rec 33.244,07: SATURA sulla domanda,
Q_net 0,00), eta caldaia 0,9
(Gas_base 195.337,85, Gas_alt 0,00),
tetto 600 m2 x quota 0,60 x 0,18
(kWp 64,80), fotovoltaico 71.280,00,
f_autoconsumo 0,70 (autoconsumo
49.896,00, deficit 51.661,89,
immessa 21.384,00), illuminazione
base 12.000, LED 7.200, domanda base
32.571,43, domanda alt 101.557,89
(l'alternativa preleva PIU'
elettricita' della baseline: forno
elettrico), prezzo elettrico 0,22,
prezzo gas 0,09, prezzo immissione
0,05 EUR/kWh (inferiore al prelievo),
O&M base 6.000, O&M alt 9.000
EUR/anno, CAPEX 100.000 EUR, f_el
0,00035 t/kWh, f_gas 0,00020 t/kWh,
WACC 5 (percentuale), vita 15 anni,
tolleranza 10 (percentuale del CAPEX).
Valori calcolati eseguendo
mh849_demo_calcoli(): pizze_anno
132000,0, Q_risc 22500,0, Q_acs
10744,066666666668, Q_termico
33244,066666666666, Q_freddo_sale
18000,0, Q_freddo_celle 39600,0,
Q_freddo 57600,0, Gas_forno_base
158400,0, E_forno_alt 79200,0,
Q_disp 39600,0, E_chiller_base
20571,428571428572, E_pdc_freddo
15157,894736842107, Q_cond_alt
72757,8947368421, Q_sorgente
112357,8947368421, Q_rec
33244,066666666666, Q_net 0,0,
Gas_base 195337,85185185185, Gas_alt
0,0, E_pdc_risc 0,0, E_pdc_alt
15157,894736842107, E_illum_base
12000,0, E_illum_alt 7200,0,
E_base_el 32571,428571428572,
E_alt_el 101557,8947368421, kWp 64,8,
E_pv 71280,0, E_pv_auto 49896,0,
E_immessa 21384,0, E_deficit
51661,89473684211, C_base
30746,120952380952, C_alt
19296,416842105264, risparmio
11449,704110275688, CAPEX 100000,0,
CO2 base 50,467570370370375, CO2 alt
18,081663157894738, CO2 evitata
32,38590721247564, VAN
18844,01330301239, TIR
7,671547811231501 %, payback 9,
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
w851_test.py (import diretto da
w851_helpers, NON via tests/appfuncs.py
load): replicato qui con w853_helpers.

Destinazione nel repo: tests dedicati
alla nuova scheda pizzeria.
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w853_helpers import (
        demo_calcoli,
        mh849_c_alt,
        mh849_c_base,
        mh849_calcola,
        mh849_co2_alt,
        mh849_co2_base,
        mh849_co2_evitata,
        mh849_csv,
        mh849_demo,
        mh849_demo_calcoli,
        mh849_e_alt_el,
        mh849_e_base_el,
        mh849_e_chiller_base,
        mh849_e_deficit,
        mh849_e_forno_alt,
        mh849_e_illum_alt,
        mh849_e_illum_base,
        mh849_e_immessa,
        mh849_e_pdc_alt,
        mh849_e_pdc_freddo,
        mh849_e_pdc_risc,
        mh849_e_pv,
        mh849_e_pv_auto,
        mh849_eta,
        mh849_flussi,
        mh849_frazione,
        mh849_gas_alt,
        mh849_gas_base,
        mh849_gas_forno_base,
        mh849_int_pos,
        mh849_nneg,
        mh849_num,
        mh849_p_el_pareggio,
        mh849_p_pv_kwp,
        mh849_payback,
        mh849_pizze_anno,
        mh849_pos,
        mh849_q_acs,
        mh849_q_cond_alt,
        mh849_q_disp,
        mh849_q_freddo,
        mh849_q_freddo_celle,
        mh849_q_freddo_sale,
        mh849_q_net,
        mh849_q_rec,
        mh849_q_risc,
        mh849_q_sorgente,
        mh849_q_termico,
        mh849_risparmio,
        mh849_sensibilita,
        mh849_tir,
        mh849_valida,
        mh849_van,
        mh849_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w853_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w853_helpers", os.path.join(_hf, "w853_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh849_c_alt = _mod.mh849_c_alt
    mh849_c_base = _mod.mh849_c_base
    mh849_calcola = _mod.mh849_calcola
    mh849_co2_alt = _mod.mh849_co2_alt
    mh849_co2_base = _mod.mh849_co2_base
    mh849_co2_evitata = _mod.mh849_co2_evitata
    mh849_csv = _mod.mh849_csv
    mh849_demo = _mod.mh849_demo
    mh849_demo_calcoli = _mod.mh849_demo_calcoli
    mh849_e_alt_el = _mod.mh849_e_alt_el
    mh849_e_base_el = _mod.mh849_e_base_el
    mh849_e_chiller_base = _mod.mh849_e_chiller_base
    mh849_e_deficit = _mod.mh849_e_deficit
    mh849_e_forno_alt = _mod.mh849_e_forno_alt
    mh849_e_illum_alt = _mod.mh849_e_illum_alt
    mh849_e_illum_base = _mod.mh849_e_illum_base
    mh849_e_immessa = _mod.mh849_e_immessa
    mh849_e_pdc_alt = _mod.mh849_e_pdc_alt
    mh849_e_pdc_freddo = _mod.mh849_e_pdc_freddo
    mh849_e_pdc_risc = _mod.mh849_e_pdc_risc
    mh849_e_pv = _mod.mh849_e_pv
    mh849_e_pv_auto = _mod.mh849_e_pv_auto
    mh849_eta = _mod.mh849_eta
    mh849_flussi = _mod.mh849_flussi
    mh849_frazione = _mod.mh849_frazione
    mh849_gas_alt = _mod.mh849_gas_alt
    mh849_gas_base = _mod.mh849_gas_base
    mh849_gas_forno_base = _mod.mh849_gas_forno_base
    mh849_int_pos = _mod.mh849_int_pos
    mh849_nneg = _mod.mh849_nneg
    mh849_num = _mod.mh849_num
    mh849_p_el_pareggio = _mod.mh849_p_el_pareggio
    mh849_p_pv_kwp = _mod.mh849_p_pv_kwp
    mh849_payback = _mod.mh849_payback
    mh849_pizze_anno = _mod.mh849_pizze_anno
    mh849_pos = _mod.mh849_pos
    mh849_q_acs = _mod.mh849_q_acs
    mh849_q_cond_alt = _mod.mh849_q_cond_alt
    mh849_q_disp = _mod.mh849_q_disp
    mh849_q_freddo = _mod.mh849_q_freddo
    mh849_q_freddo_celle = _mod.mh849_q_freddo_celle
    mh849_q_freddo_sale = _mod.mh849_q_freddo_sale
    mh849_q_net = _mod.mh849_q_net
    mh849_q_rec = _mod.mh849_q_rec
    mh849_q_risc = _mod.mh849_q_risc
    mh849_q_sorgente = _mod.mh849_q_sorgente
    mh849_q_termico = _mod.mh849_q_termico
    mh849_risparmio = _mod.mh849_risparmio
    mh849_sensibilita = _mod.mh849_sensibilita
    mh849_tir = _mod.mh849_tir
    mh849_valida = _mod.mh849_valida
    mh849_van = _mod.mh849_van
    mh849_verdetto = _mod.mh849_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w853_helpers.py")
_UI_PATH = _risolvi("w853_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "8"
_VECCHIO_TAB = "tab84" + "8"
_VECCHIO_ST = "st84" + "8_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "pizze_anno": 132000.0,
    "q_risc_kwh_th_anno": 22500.0,
    "q_acs_kwh_th_anno": 10744.066666666668,
    "q_termico_kwh_th_anno": 33244.066666666666,
    "q_freddo_sale_kwh_c_anno": 18000.0,
    "q_freddo_celle_kwh_c_anno": 39600.0,
    "q_freddo_kwh_c_anno": 57600.0,
    "gas_forno_base_kwh_anno": 158400.0,
    "e_forno_alt_kwh_e_anno": 79200.0,
    "q_disp_kwh_th_anno": 39600.0,
    "e_chiller_base_kwh_e_anno": 20571.428571428572,
    "e_pdc_freddo_kwh_e_anno": 15157.894736842107,
    "q_cond_alt_kwh_c_anno": 72757.8947368421,
    "q_sorgente_kwh_th_anno": 112357.8947368421,
    "q_rec_kwh_th_anno": 33244.066666666666,
    "q_net_kwh_th_anno": 0.0,
    "gas_base_kwh_anno": 195337.85185185185,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_risc_kwh_e_anno": 0.0,
    "e_pdc_alt_kwh_e_anno": 15157.894736842107,
    "e_illum_base_kwh_e_anno": 12000.0,
    "e_illum_alt_kwh_e_anno": 7200.0,
    "e_base_el_kwh_e_anno": 32571.428571428572,
    "e_alt_el_kwh_e_anno": 101557.8947368421,
    "p_pv_kwp": 64.8,
    "e_pv_kwh_e_anno": 71280.0,
    "e_pv_auto_kwh_e_anno": 49896.0,
    "e_immessa_kwh_e_anno": 21384.0,
    "e_deficit_kwh_e_anno": 51661.89473684211,
    "c_base_eur_anno": 30746.120952380952,
    "c_alt_eur_anno": 19296.416842105264,
    "risparmio_eur_anno": 11449.704110275688,
    "capex_eur": 100000.0,
    "co2_base_t_anno": 50.467570370370375,
    "co2_alt_t_anno": 18.081663157894738,
    "co2_evitata_t_anno": 32.38590721247564,
    "van": 18844.01330301239,
    "tir": 7.671547811231501,
    "payback": 9,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh849_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh849_num(3, "x"), 3.0)
        self.assertEqual(mh849_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh849_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh849_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh849_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh849_pos(0, "x")
        with self.assertRaises(ValueError):
            mh849_pos(-1, "x")
        self.assertEqual(mh849_pos(2, "x"), 2.0)

    def test_eta_limiti(self):
        self.assertEqual(mh849_eta(1.0, "x"), 1.0)
        self.assertEqual(mh849_eta(0.9, "x"), 0.9)
        for cattivo in (0.0, -0.1, 1.01):
            with self.assertRaises(ValueError):
                mh849_eta(cattivo, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh849_int_pos(15.0, "x"), 15)
        with self.assertRaises(ValueError):
            mh849_int_pos(15.5, "x")
        with self.assertRaises(ValueError):
            mh849_int_pos(0, "x")

    def test_frazione_limiti(self):
        self.assertEqual(mh849_frazione(0.0, "x"), 0.0)
        self.assertEqual(mh849_frazione(1.0, "x"), 1.0)
        for cattivo in (-0.01, 1.01):
            with self.assertRaises(ValueError):
                mh849_frazione(cattivo, "x")


class TestFisica(unittest.TestCase):
    def test_pizze_e_termico(self):
        self.assertEqual(mh849_pizze_anno(400, 330), 132000.0)
        self.assertEqual(mh849_q_risc(150, 150), 22500.0)
        self.assertAlmostEqual(mh849_q_acs(132000, 2, 35),
                               132000 * 2 * 4.186 * 35 / 3600.0)
        self.assertEqual(mh849_q_termico(22500.0, 10744.066666666668),
                         33244.066666666666)

    def test_freddo_sale_celle_e_totale(self):
        self.assertEqual(mh849_q_freddo_sale(150, 120), 18000.0)
        self.assertEqual(mh849_q_freddo_celle(132000, 0.30), 39600.0)
        self.assertEqual(mh849_q_freddo(18000.0, 39600.0), 57600.0)

    def test_gas_forno_scompare_in_alt_concetto(self):
        # Il gas forno base e' 158.400; il gas alt NON lo
        # somma: con termico netto 0 il gas alt e' 0.
        self.assertEqual(mh849_gas_forno_base(132000, 1.20), 158400.0)
        self.assertEqual(mh849_gas_alt(0.0, 0.9), 0.0)
        self.assertAlmostEqual(mh849_gas_base(33244.066666666666, 0.9,
                                              158400.0), 195337.85185185185)
        self.assertAlmostEqual(mh849_gas_alt(33244.066666666666, 0.9),
                               36937.85185185185)

    def test_forno_alt_e_disp(self):
        self.assertEqual(mh849_e_forno_alt(132000, 0.60), 79200.0)
        self.assertEqual(mh849_q_disp(79200.0, 0.50), 39600.0)
        self.assertEqual(mh849_q_disp(79200.0, 0.0), 0.0)
        self.assertEqual(mh849_q_disp(79200.0, 1.0), 79200.0)

    def test_chiller_e_pdc_freddo_e_cond(self):
        self.assertAlmostEqual(mh849_e_chiller_base(57600.0, 2.8),
                               20571.428571428572)
        self.assertAlmostEqual(mh849_e_pdc_freddo(57600.0, 3.8),
                               15157.894736842107)
        self.assertAlmostEqual(mh849_q_cond_alt(57600.0, 15157.894736842107),
                               72757.8947368421)

    def test_sorgente_rec_net_saturazione(self):
        self.assertAlmostEqual(mh849_q_sorgente(39600.0, 72757.8947368421),
                               112357.8947368421)
        # Demo: sorgente x f_rec x f_uso = 33.707,37 > domanda
        # 33.244,07: il recupero SATURA sulla domanda.
        self.assertAlmostEqual(mh849_q_rec(33244.066666666666,
                                           112357.8947368421, 0.60, 0.50),
                               33244.066666666666)
        self.assertEqual(mh849_q_net(33244.066666666666,
                                     33244.066666666666), 0.0)
        # Senza saturazione: recupero sotto la domanda.
        self.assertAlmostEqual(mh849_q_rec(100000.0, 50000.0, 0.60, 0.50),
                               15000.0)
        self.assertEqual(mh849_q_net(100000.0, 15000.0), 85000.0)

    def test_pdc_risc_e_illum_e_domande(self):
        self.assertEqual(mh849_e_pdc_risc(0.0, 3.5), 0.0)
        self.assertAlmostEqual(mh849_e_pdc_alt(0.0, 15157.894736842107),
                               15157.894736842107)
        self.assertEqual(mh849_e_illum_base(150, 80), 12000.0)
        self.assertEqual(mh849_e_illum_alt(12000.0, 0.40), 7200.0)
        self.assertAlmostEqual(mh849_e_base_el(20571.428571428572, 12000.0),
                               32571.428571428572)
        # Domanda alt: pdc + LED + forno elettrico.
        self.assertAlmostEqual(mh849_e_alt_el(15157.894736842107, 7200.0,
                                              79200.0), 101557.8947368421)

    def test_fv_tetto_da_tetto(self):
        self.assertAlmostEqual(mh849_p_pv_kwp(600, 0.60), 64.8)
        self.assertEqual(mh849_p_pv_kwp(0, 0.60), 0.0)
        self.assertEqual(mh849_p_pv_kwp(600, 0.0), 0.0)
        self.assertAlmostEqual(mh849_e_pv(64.8, 1100), 71280.0)

    def test_bilancio_fv_e_deficit(self):
        self.assertAlmostEqual(mh849_e_pv_auto(71280.0, 0.70,
                                               101557.8947368421), 49896.0)
        # Autoconsumo cappato alla domanda alt.
        self.assertAlmostEqual(mh849_e_pv_auto(71280.0, 1.0, 10000.0),
                               10000.0)
        self.assertAlmostEqual(mh849_e_immessa(71280.0, 49896.0), 21384.0)
        self.assertAlmostEqual(mh849_e_deficit(101557.8947368421, 49896.0),
                               51661.89473684211)
        # Bilancio: autoconsumo + immessa = produzione.
        self.assertAlmostEqual(49896.0 + 21384.0, 71280.0)
        # Deficit + autoconsumo = domanda alt.
        self.assertAlmostEqual(51661.89473684211 + 49896.0,
                               101557.8947368421)


class TestEconomia(unittest.TestCase):
    def test_c_base_c_alt_scomposizione(self):
        cb = mh849_c_base(32571.428571428572, 0.22, 195337.85185185185,
                          0.09, 6000)
        self.assertAlmostEqual(cb, 30746.120952380952)
        ca = mh849_c_alt(51661.89473684211, 0.22, 21384.0, 0.05,
                         0.0, 0.09, 9000)
        self.assertAlmostEqual(ca, 19296.416842105264)

    def test_immessa_ricavo_a_prezzo_inferiore_non_pieno(self):
        # A prezzo di immissione pieno (0,22) il costo alt
        # sarebbe piu' basso di 3.635,28 EUR/anno: il
        # ricavo e' a prezzo di immissione, non pieno.
        ca_imm = mh849_c_alt(51661.89473684211, 0.22, 21384.0, 0.05,
                             0.0, 0.09, 9000)
        ca_pieno = mh849_c_alt(51661.89473684211, 0.22, 21384.0, 0.22,
                               0.0, 0.09, 9000)
        self.assertAlmostEqual(ca_imm - ca_pieno, 21384.0 * (0.22 - 0.05))

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh849_risparmio(30746.120952380952,
                                               19296.416842105264),
                               11449.704110275688)
        self.assertEqual(mh849_risparmio(100.0, 150.0), -50.0)

    def test_co2_base_alt_evitata_senza_credito_immessa(self):
        cb = mh849_co2_base(32571.428571428572, 0.00035,
                            195337.85185185185, 0.00020)
        self.assertAlmostEqual(cb, 50.467570370370375)
        ca = mh849_co2_alt(51661.89473684211, 0.00035, 0.0, 0.00020)
        self.assertAlmostEqual(ca, 18.081663157894738)
        # L'immessa (21.384) NON sottrae CO2: alt conta
        # solo deficit e gas alt.
        self.assertAlmostEqual(mh849_co2_evitata(cb, ca),
                               32.38590721247564)

    def test_fv_nullo_ammesso(self):
        bc = mh849_calcola(**_demo_kwargs(quota_tetto=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        self.assertEqual(bc["e_pv_auto_kwh_e_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_alt_el_kwh_e_anno"])

    def test_calcola_accetta_dict_singolo(self):
        a = mh849_calcola(mh849_demo())
        b = mh849_calcola(**mh849_demo())
        self.assertAlmostEqual(a["risparmio_eur_anno"],
                               b["risparmio_eur_anno"])
        c = mh849_calcola(mh849_demo(), capex=125000)
        self.assertEqual(c["capex"], 125000)

    def test_p_el_pareggio_demo_none(self):
        bc = mh849_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        # Numeratore negativo: alt vince anche a p_el nullo.
        num = (9000 - 6000 - (195337.85185185185 - 0.0) * 0.09
               - 21384.0 * 0.05)
        self.assertLess(num, 0.0)

    def test_p_el_pareggio_none_casi(self):
        # Denominatore <= 0: niente margine.
        self.assertIsNone(mh849_p_el_pareggio(6000, 9000, 1000.0, 0.0,
                                              0.09, 0.0, 0.05,
                                              1000.0, 2000.0))
        self.assertIsNone(mh849_p_el_pareggio(6000, 9000, 1000.0, 0.0,
                                              0.09, 0.0, 0.05,
                                              1000.0, 1000.0))
        # Numeratore negativo: None anche con denominatore > 0.
        self.assertIsNone(mh849_p_el_pareggio(6000, 9000, 195337.85, 0.0,
                                              0.09, 21384.0, 0.05,
                                              32571.43, 20000.0))

    def test_p_el_pareggio_costruito_positivo(self):
        p = _demo_kwargs(q_risc=0, litri_pizza=0, quota_tetto=0,
                         eer_base=2.0, eer_alt=5.0, risparmio_led=0.80,
                         gas_forno_per_pizza=0.30,
                         e_forno_per_pizza=0.05, om_alt=12000)
        bc = mh849_calcola(**p)
        self.assertIsNotNone(bc["p_el_pareggio"])
        self.assertAlmostEqual(bc["p_el_pareggio"],
                               0.12011834319526628, places=12)

    def test_p_el_pareggio_verifica(self):
        p = _demo_kwargs(q_risc=0, litri_pizza=0, quota_tetto=0,
                         eer_base=2.0, eer_alt=5.0, risparmio_led=0.80,
                         gas_forno_per_pizza=0.30,
                         e_forno_per_pizza=0.05, om_alt=12000)
        bc = mh849_calcola(**p)
        ps = bc["p_el_pareggio"]
        # Forma chiusa: risolta da C_base(p) = C_alt(p).
        atteso = ((12000 - 6000
                   - (bc["gas_base_kwh_anno"] - bc["gas_alt_kwh_anno"])
                   * 0.09 - bc["e_immessa_kwh_e_anno"] * 0.05)
                  / (bc["e_base_el_kwh_e_anno"]
                     - bc["e_deficit_kwh_e_anno"]))
        self.assertAlmostEqual(ps, atteso, places=12)

    def test_p_el_pareggio_soglia_minima(self):
        p = _demo_kwargs(q_risc=0, litri_pizza=0, quota_tetto=0,
                         eer_base=2.0, eer_alt=5.0, risparmio_led=0.80,
                         gas_forno_per_pizza=0.30,
                         e_forno_per_pizza=0.05, om_alt=12000)
        bc = mh849_calcola(**p)
        ps = bc["p_el_pareggio"]
        sopra = mh849_calcola(**dict(p, p_el=ps + 0.01))
        sotto = mh849_calcola(**dict(p, p_el=ps - 0.01))
        esatto = mh849_calcola(**dict(p, p_el=ps))
        self.assertAlmostEqual(sopra["risparmio_eur_anno"], 202.80,
                               places=1)
        self.assertAlmostEqual(sotto["risparmio_eur_anno"], -202.80,
                               places=1)
        self.assertAlmostEqual(esatto["risparmio_eur_anno"], 0.0,
                               places=6)
        self.assertEqual(esatto["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(sotto["verdetto"], "NON_CALCOLABILE")

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh849_flussi(100000, 11449.704110275688, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -100000)
        self.assertTrue(all(f == 11449.704110275688 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh849_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 18844.01330301239)
        flussi = mh849_flussi(100000, 11449.704110275688, 15)
        self.assertAlmostEqual(mh849_van(flussi, 0.0),
                               15 * 11449.704110275688 - 100000)
        self.assertAlmostEqual(mh849_van(flussi, 5.0),
                               18844.01330301239)

    def test_van_usa_percentuale_non_frazione(self):
        flussi = mh849_flussi(100000, 11449.704110275688, 15)
        # WACC 5 (percentuale) != WACC 0,05 (frazione mal
        # interpretata): i due VAN devono differire.
        self.assertNotAlmostEqual(mh849_van(flussi, 5.0),
                                  mh849_van(flussi, 0.05))

    def test_tir_demo_e_none(self):
        bc = mh849_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 7.671547811231501)
        # Nessun cambio di segno: risparmio negativo sempre.
        self.assertIsNone(mh849_tir([-100000] + [-1000.0] * 15))
        # Nessun cambio di segno: risparmio sempre nullo.
        self.assertIsNone(mh849_tir([-100000] + [0.0] * 15))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh849_payback([-100000] + [11449.704110275688] * 15),
                         9)
        # Cumulato nullo all'anno 2: la regola >= basta.
        self.assertEqual(mh849_payback([-100.0, 50.0, 50.0]), 2)
        self.assertIsNone(mh849_payback([-100000] + [1000.0] * 15))

    def test_verdetto_percentuale(self):
        self.assertEqual(mh849_verdetto(100.0, 1.0, 100000, 10),
                         "CONVIENTE")
        self.assertEqual(mh849_verdetto(100.0, 0.0, 100000, 10),
                         "MARGINALE")
        self.assertEqual(mh849_verdetto(100.0, -10000.0, 100000, 10),
                         "MARGINALE")
        self.assertEqual(mh849_verdetto(100.0, -10000.01, 100000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh849_verdetto(0.0, 100.0, 100000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh849_verdetto(-5.0, 100.0, 100000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh849_verdetto(None, 100.0, 100000, 10),
                         "NON_CALCOLABILE")


class TestValida(unittest.TestCase):
    def test_valida_demo_ok(self):
        val = mh849_valida(*[mh849_demo()[k] for k in (
            "pizze_giorno", "giorni_anno", "litri_pizza", "acs_dt",
            "superficie_sala_m2", "q_risc",
            "superficie_tetto_m2", "quota_tetto",
            "q_freddo_sala", "freddo_celle_per_pizza",
            "gas_forno_per_pizza", "e_forno_per_pizza",
            "f_disp", "eer_base", "cop_pdc",
            "eer_alt", "f_rec", "f_uso", "e_illum_per_m2",
            "risparmio_led", "prod_specifica", "f_autoconsumo",
            "eta_caldaia", "p_el", "p_gas", "p_immissione",
            "om_base", "om_alt", "capex", "f_el", "f_gas",
            "wacc", "vita", "tolleranza")])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        base = mh849_demo()
        ordine = ("pizze_giorno", "giorni_anno", "litri_pizza", "acs_dt",
                  "superficie_sala_m2", "q_risc",
                  "superficie_tetto_m2", "quota_tetto",
                  "q_freddo_sala", "freddo_celle_per_pizza",
                  "gas_forno_per_pizza", "e_forno_per_pizza",
                  "f_disp", "eer_base", "cop_pdc",
                  "eer_alt", "f_rec", "f_uso", "e_illum_per_m2",
                  "risparmio_led", "prod_specifica", "f_autoconsumo",
                  "eta_caldaia", "p_el", "p_gas", "p_immissione",
                  "om_base", "om_alt", "capex", "f_el", "f_gas",
                  "wacc", "vita", "tolleranza")
        for cattivo in ("x", float("nan"), float("inf"), True):
            vals = [base[k] for k in ordine]
            vals[0] = cattivo
            val = mh849_valida(*vals)
            self.assertFalse(val["valido"])
            self.assertTrue(val["errore"])

    def test_valida_rifiuta_range(self):
        casi = {
            "pizze_giorno": 0, "giorni_anno": -1, "litri_pizza": -1,
            "acs_dt": -1, "superficie_sala_m2": 0, "q_risc": -1,
            "superficie_tetto_m2": -1, "quota_tetto": 1.5,
            "q_freddo_sala": -1, "freddo_celle_per_pizza": -1,
            "gas_forno_per_pizza": -1, "e_forno_per_pizza": -1,
            "f_disp": 1.5, "eer_base": 0, "cop_pdc": 0,
            "eer_alt": 0, "f_rec": -0.1, "f_uso": 1.1,
            "e_illum_per_m2": -1, "risparmio_led": 1.5,
            "prod_specifica": -1, "f_autoconsumo": -0.1,
            "eta_caldaia": 0, "p_el": -1, "p_gas": -1,
            "p_immissione": -1, "om_base": -1, "om_alt": -1,
            "capex": -1, "f_el": -1, "f_gas": -1, "wacc": -1,
            "vita": 0, "tolleranza": -1,
        }
        for chiave, valore in casi.items():
            val = mh849_valida(**_demo_kwargs(**{chiave: valore}))
            self.assertFalse(val["valido"], chiave)
        # eta sopra 1 e vita non intera rifiutati.
        self.assertFalse(mh849_valida(
            **_demo_kwargs(eta_caldaia=1.5))["valido"])
        self.assertFalse(mh849_valida(
            **_demo_kwargs(vita=15.5))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh849_valida(
            **_demo_kwargs(wacc=50, tolleranza=200))["valido"])
        self.assertTrue(mh849_valida(
            **_demo_kwargs(eta_caldaia=1.0))["valido"])
        self.assertTrue(mh849_valida(
            **_demo_kwargs(quota_tetto=1.0, f_disp=1.0))["valido"])
        self.assertTrue(mh849_valida(
            **_demo_kwargs(vita=15.0))["valido"])


class TestDemo(unittest.TestCase):
    def test_demo_dict(self):
        d = mh849_demo()
        attesi = {
            "pizze_giorno": 400, "giorni_anno": 330, "litri_pizza": 2,
            "acs_dt": 35, "superficie_sala_m2": 150, "q_risc": 150,
            "superficie_tetto_m2": 600, "quota_tetto": 0.60,
            "q_freddo_sala": 120, "freddo_celle_per_pizza": 0.30,
            "gas_forno_per_pizza": 1.20, "e_forno_per_pizza": 0.60,
            "f_disp": 0.50, "eer_base": 2.8, "cop_pdc": 3.5,
            "eer_alt": 3.8, "f_rec": 0.60, "f_uso": 0.50,
            "e_illum_per_m2": 80, "risparmio_led": 0.40,
            "prod_specifica": 1100, "f_autoconsumo": 0.70,
            "eta_caldaia": 0.9, "p_el": 0.22, "p_gas": 0.09,
            "p_immissione": 0.05, "om_base": 6000, "om_alt": 9000,
            "capex": 100000, "f_el": 0.00035, "f_gas": 0.00020,
            "wacc": 5, "vita": 15, "tolleranza": 10,
        }
        self.assertEqual(d, attesi)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh849_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            ottenuto = bc[chiave]
            if atteso is None:
                self.assertIsNone(ottenuto, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(ottenuto, atteso), 1e-9, chiave)
            else:
                self.assertEqual(ottenuto, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh849_demo_calcoli()
        self.assertAlmostEqual(bc["pizze_anno"], 132000.0)
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], 33244.066666666666)
        self.assertAlmostEqual(bc["gas_alt_kwh_anno"], 0.0)
        self.assertAlmostEqual(bc["q_net_kwh_th_anno"], 0.0)
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh849_demo_calcoli()
        df = bc["df_flussi"]
        self.assertEqual(len(df), 16)
        self.assertAlmostEqual(df.iloc[0]["Flusso (EUR/anno)"], -100000.0)
        self.assertAlmostEqual(df.iloc[8]["Cumulato (EUR)"], -8402.37,
                               places=1)
        self.assertAlmostEqual(df.iloc[9]["Cumulato (EUR)"], 3047.34,
                               places=1)
        self.assertEqual(bc["payback"], 9)

    def test_demo_tabella_righe(self):
        bc = mh849_demo_calcoli()
        df = bc["df_tabella"]
        voci = set(df["Voce"])
        self.assertIn("Pizze all'anno", voci)
        self.assertIn("Gas forno baseline (kWh/anno)", voci)
        self.assertIn("Gas alternativo, senza gas forno (kWh/anno)", voci)
        self.assertIn("Potenza FV tetto (kWp)", voci)
        self.assertIn("Verdetto", voci)
        self.assertGreater(len(df), 60)

    def test_demo_coerenza_interna(self):
        bc = mh849_demo_calcoli()
        # Bilanci esatti: FV, deficit, costi, CO2.
        self.assertAlmostEqual(bc["e_pv_auto_kwh_e_anno"]
                               + bc["e_immessa_kwh_e_anno"],
                               bc["e_pv_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"]
                               + bc["e_pv_auto_kwh_e_anno"],
                               bc["e_alt_el_kwh_e_anno"])
        self.assertAlmostEqual(bc["c_base_eur_anno"]
                               - bc["c_alt_eur_anno"],
                               bc["risparmio_eur_anno"])
        self.assertAlmostEqual(bc["co2_base_t_anno"]
                               - bc["co2_alt_t_anno"],
                               bc["co2_evitata_t_anno"])
        self.assertLessEqual(bc["q_rec_kwh_th_anno"],
                             bc["q_termico_kwh_th_anno"])
        self.assertAlmostEqual(bc["q_rec_kwh_th_anno"],
                               bc["q_termico_kwh_th_anno"])
        self.assertEqual(bc["q_net_kwh_th_anno"], 0.0)

    def test_demo_contro_riconteggio_indipendente(self):
        d = mh849_demo()
        pizze = d["pizze_giorno"] * d["giorni_anno"]
        q_risc = d["superficie_sala_m2"] * d["q_risc"]
        q_acs = pizze * d["litri_pizza"] * 4.186 * d["acs_dt"] / 3600.0
        q_term = q_risc + q_acs
        q_freddo = (d["superficie_sala_m2"] * d["q_freddo_sala"]
                    + pizze * d["freddo_celle_per_pizza"])
        g_forno = pizze * d["gas_forno_per_pizza"]
        e_forno = pizze * d["e_forno_per_pizza"]
        q_disp = e_forno * d["f_disp"]
        e_chill = q_freddo / d["eer_base"]
        e_pdc_f = q_freddo / d["eer_alt"]
        q_cond = q_freddo + e_pdc_f
        q_sorg = q_disp + q_cond
        q_rec = min(q_term, q_sorg * d["f_rec"] * d["f_uso"])
        q_net = max(0.0, q_term - q_rec)
        g_base = q_term / d["eta_caldaia"] + g_forno
        g_alt = q_net / d["eta_caldaia"]
        e_pdc = q_net / d["cop_pdc"] + e_pdc_f
        e_ill_b = d["superficie_sala_m2"] * d["e_illum_per_m2"]
        e_ill_a = e_ill_b * (1.0 - d["risparmio_led"])
        e_base = e_chill + e_ill_b
        e_alt = e_pdc + e_ill_a + e_forno
        kwp = d["superficie_tetto_m2"] * d["quota_tetto"] * 0.18
        e_pv = kwp * d["prod_specifica"]
        e_auto = min(e_pv * d["f_autoconsumo"], e_alt)
        e_imm = e_pv - e_auto
        e_def = max(0.0, e_alt - e_auto)
        c_base = e_base * d["p_el"] + g_base * d["p_gas"] + d["om_base"]
        c_alt = (e_def * d["p_el"] - e_imm * d["p_immissione"]
                 + g_alt * d["p_gas"] + d["om_alt"])
        bc = mh849_demo_calcoli()
        for chiave, valore in (
                ("pizze_anno", pizze), ("q_risc_kwh_th_anno", q_risc),
                ("q_acs_kwh_th_anno", q_acs),
                ("q_termico_kwh_th_anno", q_term),
                ("q_freddo_kwh_c_anno", q_freddo),
                ("gas_forno_base_kwh_anno", g_forno),
                ("e_forno_alt_kwh_e_anno", e_forno),
                ("q_disp_kwh_th_anno", q_disp),
                ("q_cond_alt_kwh_c_anno", q_cond),
                ("q_sorgente_kwh_th_anno", q_sorg),
                ("q_rec_kwh_th_anno", q_rec),
                ("q_net_kwh_th_anno", q_net),
                ("gas_base_kwh_anno", g_base),
                ("gas_alt_kwh_anno", g_alt),
                ("e_base_el_kwh_e_anno", e_base),
                ("e_alt_el_kwh_e_anno", e_alt),
                ("p_pv_kwp", kwp), ("e_pv_kwh_e_anno", e_pv),
                ("e_pv_auto_kwh_e_anno", e_auto),
                ("e_immessa_kwh_e_anno", e_imm),
                ("e_deficit_kwh_e_anno", e_def),
                ("c_base_eur_anno", c_base),
                ("c_alt_eur_anno", c_alt),
                ("risparmio_eur_anno", c_base - c_alt)):
            self.assertLess(_rel(bc[chiave], valore), 1e-9, chiave)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh849_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_p_el_piu_meno_20(self):
        sens = mh849_sensibilita(**mh849_demo())
        meno = sens["p_el_meno20"]
        piu = sens["p_el_piu20"]
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 12289.68,
                               places=1)
        self.assertAlmostEqual(meno["van"], 27562.72, places=1)
        self.assertAlmostEqual(meno["tir"], 8.84, places=1)
        self.assertEqual(meno["payback"], 9)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 10609.72,
                               places=1)
        self.assertAlmostEqual(piu["van"], 10125.30, places=1)
        self.assertAlmostEqual(piu["tir"], 6.46, places=1)
        self.assertEqual(piu["payback"], 10)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_p_el_basso_migliora_il_caso(self):
        # L'alternativa preleva piu' elettricita' della
        # baseline (forno elettrico): un prezzo piu'
        # basso pesa di piu' sul deficit alternativo.
        base = mh849_demo_calcoli()
        meno = mh849_sensibilita(**mh849_demo())["p_el_meno20"]
        self.assertGreater(meno["risparmio_eur_anno"],
                           base["risparmio_eur_anno"])
        self.assertGreater(base["e_deficit_kwh_e_anno"],
                           base["e_base_el_kwh_e_anno"])

    def test_variante_senza_fotovoltaico_non_calcolabile(self):
        sens = mh849_sensibilita(**mh849_demo())
        caso = sens["senza_fv"]
        self.assertAlmostEqual(caso["risparmio_eur_anno"], -596.62,
                               places=1)
        self.assertEqual(caso["verdetto"], "NON_CALCOLABILE")
        # Il FV da solo vale 12.046,32 EUR/anno di risparmio.
        base = mh849_demo_calcoli()
        self.assertAlmostEqual(base["risparmio_eur_anno"]
                               - caso["risparmio_eur_anno"], 12046.32,
                               places=1)

    def test_variante_senza_recupero_non_convinte(self):
        caso = mh849_sensibilita(**mh849_demo())["senza_recupero"]
        self.assertAlmostEqual(caso["risparmio_eur_anno"], 6035.67,
                               places=1)
        self.assertAlmostEqual(caso["van"], -37351.81, places=1)
        self.assertAlmostEqual(caso["tir"], -1.22, places=1)
        self.assertIsNone(caso["payback"])
        self.assertEqual(caso["verdetto"], "NON_CONVIENTE")

    def test_variante_senza_led_convinte(self):
        caso = mh849_calcola(**_demo_kwargs(risparmio_led=0))
        self.assertAlmostEqual(caso["risparmio_eur_anno"], 10393.70,
                               places=1)
        self.assertAlmostEqual(caso["van"], 7883.09, places=1)
        self.assertEqual(caso["payback"], 10)
        self.assertEqual(caso["verdetto"], "CONVIENTE")

    def test_variante_capex_doppio_non_convinte(self):
        caso = mh849_sensibilita(**mh849_demo())["capex_doppio"]
        self.assertAlmostEqual(caso["van"], -81155.99, places=1)
        self.assertAlmostEqual(caso["tir"], -1.85, places=1)
        self.assertIsNone(caso["payback"])
        self.assertEqual(caso["verdetto"], "NON_CONVIENTE")

    def test_variante_capex_marginale(self):
        caso = mh849_calcola(**_demo_kwargs(capex=125000))
        self.assertAlmostEqual(caso["van"], -6155.99, places=1)
        self.assertAlmostEqual(caso["tir"], 4.26, places=1)
        self.assertEqual(caso["payback"], 11)
        self.assertEqual(caso["verdetto"], "MARGINALE")

    def test_variante_vita_10_non_convinte(self):
        caso = mh849_sensibilita(**mh849_demo())["vita_10"]
        self.assertAlmostEqual(caso["van"], -11588.42, places=1)
        self.assertAlmostEqual(caso["tir"], 2.54, places=1)
        self.assertEqual(caso["payback"], 9)
        self.assertEqual(caso["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        caso = mh849_sensibilita(**mh849_demo())["wacc_0"]
        self.assertAlmostEqual(caso["van"], 71745.56, places=1)
        self.assertAlmostEqual(caso["tir"], 7.67, places=1)
        self.assertEqual(caso["payback"], 9)
        self.assertEqual(caso["verdetto"], "CONVIENTE")

    def test_sensibilita_helper_coerente_con_calcola(self):
        sens = mh849_sensibilita(**mh849_demo())
        diretto = mh849_calcola(**_demo_kwargs(quota_tetto=0))
        self.assertAlmostEqual(sens["senza_fv"]["risparmio_eur_anno"],
                               diretto["risparmio_eur_anno"])
        diretto2 = mh849_calcola(**_demo_kwargs(f_rec=0))
        self.assertAlmostEqual(
            sens["senza_recupero"]["risparmio_eur_anno"],
            diretto2["risparmio_eur_anno"])

    def test_demo_deterministica_due_chiamate(self):
        a = mh849_demo_calcoli()
        b = mh849_demo_calcoli()
        self.assertEqual(a["risparmio_eur_anno"],
                         b["risparmio_eur_anno"])
        self.assertEqual(a["van"], b["van"])

    def test_demo_chiavi_attese(self):
        bc = mh849_demo_calcoli()
        for chiave in (
                "pizze_anno", "q_termico_kwh_th_anno",
                "gas_forno_base_kwh_anno", "e_forno_alt_kwh_e_anno",
                "q_disp_kwh_th_anno", "q_sorgente_kwh_th_anno",
                "q_rec_kwh_th_anno", "q_net_kwh_th_anno",
                "gas_base_kwh_anno", "gas_alt_kwh_anno",
                "e_alt_el_kwh_e_anno", "p_pv_kwp",
                "e_immessa_kwh_e_anno", "e_deficit_kwh_e_anno",
                "risparmio_eur_anno", "van", "tir", "payback",
                "p_el_pareggio", "verdetto", "df_flussi",
                "df_tabella"):
            self.assertIn(chiave, bc, chiave)


class TestDegenere(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        casi = {
            "pizze_giorno": 0, "giorni_anno": -1, "litri_pizza": -1,
            "acs_dt": -1, "superficie_sala_m2": 0, "q_risc": -1,
            "superficie_tetto_m2": -1, "quota_tetto": 1.5,
            "q_freddo_sala": -1, "freddo_celle_per_pizza": -1,
            "gas_forno_per_pizza": -1, "e_forno_per_pizza": -1,
            "f_disp": 1.5, "eer_base": 0, "cop_pdc": 0,
            "eer_alt": 0, "f_rec": -0.1, "f_uso": 1.1,
            "e_illum_per_m2": -1, "risparmio_led": 1.5,
            "prod_specifica": -1, "f_autoconsumo": -0.1,
            "eta_caldaia": 0, "p_el": -1, "p_gas": -1,
            "p_immissione": -1, "om_base": -1, "om_alt": -1,
            "capex": -1, "f_el": -1, "f_gas": -1, "wacc": -1,
            "vita": 0, "tolleranza": -1,
        }
        for chiave, valore in casi.items():
            with self.assertRaises(ValueError, msg=chiave):
                mh849_calcola(**_demo_kwargs(**{chiave: valore}))

    def test_degenere_quota_sopra_uno_cop_zero_pizze_zero_e_vita(self):
        with self.assertRaises(ValueError):
            mh849_calcola(**_demo_kwargs(quota_tetto=1.01))
        with self.assertRaises(ValueError):
            mh849_calcola(**_demo_kwargs(cop_pdc=0))
        with self.assertRaises(ValueError):
            mh849_calcola(**_demo_kwargs(pizze_giorno=0))
        with self.assertRaises(ValueError):
            mh849_calcola(**_demo_kwargs(vita=15.5))
        with self.assertRaises(ValueError):
            mh849_calcola(**_demo_kwargs(eta_caldaia=1.5))

    def test_degenere_stringa_nan_inf(self):
        for cattivo in ("x", float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                mh849_calcola(**_demo_kwargs(pizze_giorno=cattivo))
            with self.assertRaises(ValueError):
                mh849_calcola(**_demo_kwargs(p_el=cattivo))

    def test_zeri_ammessi_non_sollevano(self):
        zeri = {
            "giorni_anno": 0, "litri_pizza": 0, "acs_dt": 0,
            "q_risc": 0, "superficie_tetto_m2": 0, "quota_tetto": 0,
            "q_freddo_sala": 0, "freddo_celle_per_pizza": 0,
            "gas_forno_per_pizza": 0, "e_forno_per_pizza": 0,
            "f_disp": 0, "f_rec": 0, "f_uso": 0,
            "e_illum_per_m2": 0, "risparmio_led": 0,
            "prod_specifica": 0, "f_autoconsumo": 0,
            "p_el": 0, "p_gas": 0, "p_immissione": 0,
            "om_base": 0, "om_alt": 0, "capex": 0, "f_el": 0,
            "f_gas": 0, "wacc": 0, "tolleranza": 0,
        }
        for chiave, valore in zeri.items():
            try:
                mh849_calcola(**_demo_kwargs(**{chiave: valore}))
            except ValueError as exc:
                self.fail(f"zero ammesso {chiave} solleva: {exc}")

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        caso = mh849_calcola(**_demo_kwargs(quota_tetto=0))
        self.assertLessEqual(caso["risparmio_eur_anno"], 0.0)
        self.assertEqual(caso["verdetto"], "NON_CALCOLABILE")
        # Anche con risparmio esattamente zero il verdetto
        # resta NON_CALCOLABILE (pareggio costruito).
        p = _demo_kwargs(q_risc=0, litri_pizza=0, quota_tetto=0,
                         eer_base=2.0, eer_alt=5.0, risparmio_led=0.80,
                         gas_forno_per_pizza=0.30,
                         e_forno_per_pizza=0.05, om_alt=12000)
        bc = mh849_calcola(**p)
        esatto = mh849_calcola(**dict(p, p_el=bc["p_el_pareggio"]))
        self.assertAlmostEqual(esatto["risparmio_eur_anno"], 0.0,
                               places=6)
        self.assertEqual(esatto["verdetto"], "NON_CALCOLABILE")

    def test_pareggio_esatto_soglia(self):
        p = _demo_kwargs(q_risc=0, litri_pizza=0, quota_tetto=0,
                         eer_base=2.0, eer_alt=5.0, risparmio_led=0.80,
                         gas_forno_per_pizza=0.30,
                         e_forno_per_pizza=0.05, om_alt=12000)
        bc = mh849_calcola(**p)
        self.assertIsNotNone(bc["p_el_pareggio"])
        self.assertGreater(bc["p_el_pareggio"], 0.0)


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh849_demo_calcoli()
        csv = mh849_csv(bc, mh849_demo())
        self.assertIn(";", csv)
        righe = [r for r in csv.strip().split("\n") if r]
        self.assertGreater(len(righe), 60)
        self.assertTrue(righe[0].startswith("voce;valore"))

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh849_demo_calcoli()
        csv = mh849_csv(bc, mh849_demo())
        self.assertIn("risparmio_eur_anno;", csv)
        self.assertIn("verdetto;CONVIENTE", csv)
        self.assertIn("pizze_anno;132000", csv)
        self.assertIn("gas_forno_base_kwh_anno;158400", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh849_demo_calcoli()
        csv = mh849_csv(bc, mh849_demo())
        for chiave in mh849_demo().keys():
            self.assertIn(chiave + ";", csv, chiave)


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
        self.assertEqual(src.count("with tab849:"), 1)
        self.assertTrue(src.startswith("    # W853"))

    def test_ui_tab849_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab849:"), 1)
        self.assertIn("def mh849_demo(", src_h)
        self.assertIn("def mh849_calcola(", src_h)
        self.assertIn("tab849", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Pizzeria: forno elettrico con recupero fumi + pompa di calore batte il forno a gas?", src)
        self.assertIn("🍕 Pizzeria: forno elettrico con recupero fumi + pompa di calore batte il forno a gas?", src)
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
        chiavi = re.findall(r'key="(st849_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st849_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st849_calcola"', src)
        self.assertIn('key="st849_csv"', src)
        self.assertIn('key="st849_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def849\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh849_demo().keys()), lette - set(mh849_demo().keys()))
        self.assertEqual(lette, set(mh849_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc849\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc849\["([^"]+)"\]', src))
        attese = set(mh849_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg849"), src.index(".paiac("))
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
