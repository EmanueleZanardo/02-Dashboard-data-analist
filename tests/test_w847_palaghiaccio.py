"""Test nuova scheda palaghiaccio:
frigorifero efficiente + recupero calore
+ fotovoltaico battono frigorifero
tradizionale + caldaia a gas?

Business case annuo di un palaghiaccio,
connesso alla rete, guidato dal CARICO
FRIGORIFERO DELLA PISTA (non da sala
sportiva, non da acqua di vasca, non da
ghiaccio venduto al kg):
Q_freddo = superficie_pista_m2 x q_pista;
E_frigo_base = Q_freddo / COP_base;
E_frigo_alt = Q_freddo / COP_alt;
Q_cond_alt = Q_freddo + E_frigo_alt
(primo principio); Q_risc =
superficie_spogliatoi_m2 x q_risc;
Q_acs = litri_giorno x giorni_anno x
4,186 x dT / 3600; Q_termico = Q_risc
+ Q_acs; Q_rec = min(Q_termico,
Q_cond_alt x f_rec x f_uso) (satura
sulla domanda, solo la frazione
utilizzabile coincide con la domanda);
Q_net = max(0, Q_termico - Q_rec);
Gas_base = Q_termico / eta_caldaia;
Gas_alt = Q_net / eta_caldaia;
E_pv = kWp x producibilita';
E_pv_auto = min(E_pv x f_autoconsumo,
E_frigo_alt) (cappato al frigo alt);
E_immessa = E_pv - E_pv_auto;
E_deficit = max(0, E_frigo_alt -
E_pv_auto); C_base = E_frigo_base x
p_el + Gas_base x p_gas + OM_base;
C_alt = E_deficit x p_el - E_immessa
x p_immissione + Gas_alt x p_gas +
OM_alt (l'immessa e' un RICAVO a
prezzo di immissione, INFERIORE a
p_el; nessun credito CO2 per
l'immessa); risparmio = C_base -
C_alt; CAPEX forfettario; CO2 base =
E_frigo_base x f_el + Gas_base x
f_gas; CO2 alt = E_deficit x f_el +
Gas_alt x f_gas (fattori in t/kWh,
nessuna divisione per 1000; nessun
credito CO2 per l'immessa); CO2
evitata = base - alt (segno libero);
flussi [-CAPEX, risparmio x vita];
VAN al WACC (PERCENTUALE in ingresso,
/ 100 dentro); TIR per bisezione;
payback (primo anno con cumulato >= 0);
prezzo elettrico di pareggio p_star =
(OM_alt - OM_base - (Gas_base -
Gas_alt) x p_gas - E_immessa x
p_immissione) / (E_frigo_base -
E_deficit) in forma chiusa a prezzo
gas, prezzo immissione e O&M FERMI,
None se E_frigo_base - E_deficit <= 0
o se p_star < 0, SOGLIA MINIMA sui
soli costi annui quando esiste (sopra
di essa l'alternativa vince, sotto
perde; il CAPEX non entra nel
pareggio annuo).
Nel demo p_star e' None, documentato:
il numeratore e' negativo (-16.664,38
EUR/anno), quindi l'alternativa vince
sui costi annui anche a prezzo
elettrico nullo. Un caso costruito
con pareggio positivo (niente termico:
spogliatoi 0 e ACS 0, niente
fotovoltaico) ha p_star
0,0446984126984127 EUR/kWh: a p_star
il risparmio e' zero e il verdetto e'
NON_CALCOLABILE, a p_star + 0,01 il
risparmio e' 894,89 EUR/anno, a
p_star - 0,01 e' -894,89 EUR/anno.
Verdetto: NON_CALCOLABILE se input
degenere (superficie pista <= 0,
q_pista < 0, COP base o alt <= 0,
superficie spogliatoi < 0, q_risc < 0,
ACS litri, giorni o dT < 0, eta
caldaia <= 0 o > 1, f_rec o f_uso < 0
o > 1, kWp < 0, producibilita' < 0,
f_autoconsumo < 0 o > 1, prezzi < 0,
O&M < 0, CAPEX < 0, f_el < 0, f_gas
< 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI,
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
(superficie pista, COP base, COP alt,
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

Demo (palaghiaccio): pista 1.800 m2,
350 kWh_c/m2/anno (Q_freddo 630.000),
COP base 2,2 (E_frigo_base
286.363,64), COP alt 3,2 (E_frigo_alt
196.875,00), Q_cond_alt 826.875,00,
spogliatoi 1.000 m2 x 180 kWh_th/m2
(Q_risc 180.000,00), ACS 2.000
l/giorno x 200 giorni x 4,186 x 35 /
3600 (Q_acs 16.278,89), Q_termico
196.278,89, f_rec 0,60 e f_uso 0,35
(Q_rec 173.643,75, Q_net 22.635,14),
eta caldaia 0,9 (Gas_base
218.087,65, Gas_alt 25.150,15),
fotovoltaico 200 kWp a 1.100
kWh/kWp/anno (220.000,00),
f_autoconsumo 0,70 (autoconsumo
154.000,00, deficit 42.875,00,
immessa 66.000,00), prezzo elettrico
0,22, prezzo gas 0,09, prezzo
immissione 0,05 EUR/kWh (inferiore
al prelievo), O&M base 8.000, O&M alt
12.000 EUR/anno, CAPEX 450.000 EUR,
f_el 0,00035 t/kWh, f_gas 0,00020
t/kWh, WACC 5 (percentuale), vita 15
anni, tolleranza 10 (percentuale del
CAPEX).
Valori calcolati eseguendo
mh847_demo_calcoli(): Q_freddo
630000,0, E_frigo_base
286363,63636363635, E_frigo_alt
196875,0, Q_cond_alt 826875,0,
Q_risc 180000,0, Q_acs
16278,888888888889, Q_termico
196278,88888888888, Q_rec 173643,75,
Q_net 22635,138888888876, Gas_base
218087,65432098764, Gas_alt
25150,15432098764, E_pv 220000,0,
E_pv_auto 154000,0, E_immessa
66000,0, E_deficit 42875,0, C_base
90627,88888888889, C_alt
20396,013888888887, risparmio
70231,875, CAPEX 450000,0, CO2 base
143,84480359147025, CO2 alt
20,03628086419753, CO2 evitata
123,80852272727273, VAN
278982,84588024445, TIR
13,166002809225741 %, payback 7,
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

Destinazione nel repo: tests dedicati
alla nuova scheda palaghiaccio.
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w850_helpers import (
        demo_calcoli,
        mh847_c_alt,
        mh847_c_base,
        mh847_calcola,
        mh847_co2_alt,
        mh847_co2_base,
        mh847_co2_evitata,
        mh847_csv,
        mh847_demo,
        mh847_demo_calcoli,
        mh847_e_deficit,
        mh847_e_frigo_alt,
        mh847_e_frigo_base,
        mh847_e_immessa,
        mh847_e_pv,
        mh847_e_pv_auto,
        mh847_eta,
        mh847_flussi,
        mh847_frazione,
        mh847_gas_alt,
        mh847_gas_base,
        mh847_int_pos,
        mh847_nneg,
        mh847_num,
        mh847_p_el_pareggio,
        mh847_payback,
        mh847_pos,
        mh847_q_acs,
        mh847_q_cond_alt,
        mh847_q_freddo,
        mh847_q_net,
        mh847_q_rec,
        mh847_q_risc,
        mh847_q_termico,
        mh847_risparmio,
        mh847_sensibilita,
        mh847_tir,
        mh847_valida,
        mh847_van,
        mh847_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w850_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w850_helpers", os.path.join(_hf, "w850_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh847_c_alt = _mod.mh847_c_alt
    mh847_c_base = _mod.mh847_c_base
    mh847_calcola = _mod.mh847_calcola
    mh847_co2_alt = _mod.mh847_co2_alt
    mh847_co2_base = _mod.mh847_co2_base
    mh847_co2_evitata = _mod.mh847_co2_evitata
    mh847_csv = _mod.mh847_csv
    mh847_demo = _mod.mh847_demo
    mh847_demo_calcoli = _mod.mh847_demo_calcoli
    mh847_e_deficit = _mod.mh847_e_deficit
    mh847_e_frigo_alt = _mod.mh847_e_frigo_alt
    mh847_e_frigo_base = _mod.mh847_e_frigo_base
    mh847_e_immessa = _mod.mh847_e_immessa
    mh847_e_pv = _mod.mh847_e_pv
    mh847_e_pv_auto = _mod.mh847_e_pv_auto
    mh847_eta = _mod.mh847_eta
    mh847_flussi = _mod.mh847_flussi
    mh847_frazione = _mod.mh847_frazione
    mh847_gas_alt = _mod.mh847_gas_alt
    mh847_gas_base = _mod.mh847_gas_base
    mh847_int_pos = _mod.mh847_int_pos
    mh847_nneg = _mod.mh847_nneg
    mh847_num = _mod.mh847_num
    mh847_p_el_pareggio = _mod.mh847_p_el_pareggio
    mh847_payback = _mod.mh847_payback
    mh847_pos = _mod.mh847_pos
    mh847_q_acs = _mod.mh847_q_acs
    mh847_q_cond_alt = _mod.mh847_q_cond_alt
    mh847_q_freddo = _mod.mh847_q_freddo
    mh847_q_net = _mod.mh847_q_net
    mh847_q_rec = _mod.mh847_q_rec
    mh847_q_risc = _mod.mh847_q_risc
    mh847_q_termico = _mod.mh847_q_termico
    mh847_risparmio = _mod.mh847_risparmio
    mh847_sensibilita = _mod.mh847_sensibilita
    mh847_tir = _mod.mh847_tir
    mh847_valida = _mod.mh847_valida
    mh847_van = _mod.mh847_van
    mh847_verdetto = _mod.mh847_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w850_helpers.py")
_UI_PATH = _risolvi("w850_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "9"
_VECCHIO_TAB = "tab84" + "6"
_VECCHIO_ST = "st84" + "6_"
_IMP_STREAMLIT = "import " + "streamlit"

_DEMO = {
    "q_freddo_kwh_c_anno": 630000.0,
    "e_frigo_base_kwh_e_anno": 286363.63636363635,
    "e_frigo_alt_kwh_e_anno": 196875.0,
    "q_cond_alt_kwh_c_anno": 826875.0,
    "q_risc_kwh_th_anno": 180000.0,
    "q_acs_kwh_th_anno": 16278.888888888889,
    "q_termico_kwh_th_anno": 196278.88888888888,
    "q_rec_kwh_th_anno": 173643.75,
    "q_net_kwh_th_anno": 22635.138888888876,
    "gas_base_kwh_anno": 218087.65432098764,
    "gas_alt_kwh_anno": 25150.15432098764,
    "e_pv_kwh_e_anno": 220000.0,
    "e_pv_auto_kwh_e_anno": 154000.0,
    "e_immessa_kwh_e_anno": 66000.0,
    "e_deficit_kwh_e_anno": 42875.0,
    "c_base_eur_anno": 90627.88888888889,
    "c_alt_eur_anno": 20396.013888888887,
    "risparmio_eur_anno": 70231.875,
    "capex_eur": 450000.0,
    "co2_base_t_anno": 143.84480359147025,
    "co2_alt_t_anno": 20.03628086419753,
    "co2_evitata_t_anno": 123.80852272727273,
    "van": 278982.84588024445,
    "tir": 13.166002809225741,
    "payback": 7,
    "p_el_pareggio": None,
}


def _demo_kwargs(**over):
    kw = dict(mh847_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh847_num(3, "x"), 3.0)
        self.assertEqual(mh847_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh847_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh847_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh847_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh847_pos(0, "x")
        with self.assertRaises(ValueError):
            mh847_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh847_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh847_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh847_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh847_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh847_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh847_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh847_int_pos(15.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh847_frazione(0, "quota"), 0.0)
        self.assertEqual(mh847_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh847_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh847_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_freddo_e_frigo(self):
        self.assertEqual(mh847_q_freddo(1800, 350), 630000.0)
        self.assertEqual(mh847_e_frigo_base(630000.0, 2.2),
                         286363.63636363635)
        self.assertEqual(mh847_e_frigo_alt(630000.0, 3.2), 196875.0)
        self.assertLess(mh847_e_frigo_alt(630000.0, 3.2),
                        mh847_e_frigo_base(630000.0, 2.2))

    def test_q_cond_primo_principio(self):
        self.assertEqual(mh847_q_cond_alt(630000.0, 196875.0), 826875.0)
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["q_cond_alt_kwh_c_anno"],
                               bc["q_freddo_kwh_c_anno"]
                               + bc["e_frigo_alt_kwh_e_anno"], places=6)

    def test_termico_risc_acs(self):
        self.assertEqual(mh847_q_risc(1000, 180), 180000.0)
        self.assertAlmostEqual(mh847_q_acs(2000, 200, 35),
                               16278.888888888889, places=6)
        self.assertAlmostEqual(mh847_q_termico(180000.0, 16278.888888888889),
                               196278.88888888888, places=6)
        self.assertEqual(mh847_q_acs(0, 200, 35), 0.0)
        self.assertEqual(mh847_q_acs(2000, 0, 35), 0.0)

    def test_q_rec_satura_sulla_domanda(self):
        self.assertEqual(mh847_q_rec(196278.88888888888, 826875.0,
                                     0.60, 0.35), 173643.75)
        self.assertEqual(mh847_q_rec(18000.0, 826875.0, 0.60, 0.35),
                         18000.0)
        self.assertEqual(mh847_q_rec(196278.88888888888, 826875.0,
                                     0.0, 0.35), 0.0)
        self.assertEqual(mh847_q_rec(196278.88888888888, 826875.0,
                                     0.60, 0.0), 0.0)
        self.assertEqual(mh847_q_net(196278.88888888888, 173643.75),
                         22635.138888888876)
        self.assertEqual(mh847_q_net(18000.0, 18000.0), 0.0)

    def test_gas_base_alt(self):
        self.assertAlmostEqual(mh847_gas_base(196278.88888888888, 0.9),
                               218087.65432098764, places=6)
        self.assertAlmostEqual(mh847_gas_alt(22635.138888888876, 0.9),
                               25150.15432098764, places=6)

    def test_fv_autoconsumo_cappato_deficit_immessa(self):
        self.assertEqual(mh847_e_pv(200, 1100), 220000.0)
        self.assertEqual(mh847_e_pv_auto(220000.0, 0.70, 196875.0),
                         154000.0)
        self.assertEqual(mh847_e_pv_auto(1100000.0, 0.70, 196875.0),
                         196875.0)
        self.assertEqual(mh847_e_pv_auto(220000.0, 0.0, 196875.0), 0.0)
        self.assertEqual(mh847_e_immessa(220000.0, 154000.0), 66000.0)
        self.assertEqual(mh847_e_deficit(196875.0, 154000.0), 42875.0)
        self.assertEqual(mh847_e_deficit(196875.0, 196875.0), 0.0)

    def test_bilancio_fv_e_deficit(self):
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_auto_kwh_e_anno"]
                               + bc["e_immessa_kwh_e_anno"], places=6)
        self.assertAlmostEqual(bc["e_deficit_kwh_e_anno"],
                               bc["e_frigo_alt_kwh_e_anno"]
                               - bc["e_pv_auto_kwh_e_anno"], places=6)
        self.assertGreaterEqual(bc["e_immessa_kwh_e_anno"], 0.0)
        self.assertGreaterEqual(bc["e_deficit_kwh_e_anno"], 0.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh847_c_base(286363.63636363635, 0.22,
                                            218087.65432098764, 0.09,
                                            8000), 90627.88888888889,
                               places=6)
        self.assertAlmostEqual(mh847_c_alt(42875.0, 0.22, 66000.0, 0.05,
                                           25150.15432098764, 0.09,
                                           12000), 20396.013888888887,
                               places=6)

    def test_immessa_ricavo_a_prezzo_inferiore_non_pieno(self):
        base = mh847_demo_calcoli()
        senza_ricavo = mh847_calcola(**_demo_kwargs(p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo["c_alt_eur_anno"],
                               base["c_alt_eur_anno"] + 3300.0, places=6)
        self.assertEqual(senza_ricavo["co2_alt_t_anno"],
                         base["co2_alt_t_anno"])

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh847_risparmio(90627.88888888889,
                                              20396.013888888887),
                               70231.875, places=6)
        self.assertLess(mh847_risparmio(20396.013888888887,
                                        90627.88888888889), 0.0)

    def test_co2_base_alt_evitata_senza_credito_immessa(self):
        self.assertAlmostEqual(mh847_co2_base(286363.63636363635, 0.00035,
                                              218087.65432098764, 0.00020),
                               143.84480359147025, places=6)
        self.assertAlmostEqual(mh847_co2_alt(42875.0, 0.00035,
                                             25150.15432098764, 0.00020),
                               20.03628086419753, places=6)
        self.assertAlmostEqual(mh847_co2_evitata(143.84480359147025,
                                                20.03628086419753),
                               123.80852272727273, places=6)
        # L'immessa non entra nella CO2 alternativa:
        # stesso deficit e stesso gas, immessa diversa,
        # CO2 alternativa identica per costruzione.
        self.assertAlmostEqual(
            mh847_co2_alt(42875.0, 0.00035, 25150.15432098764, 0.00020),
            42875.0 * 0.00035 + 25150.15432098764 * 0.00020, places=6)

    def test_fv_nullo_ammesso(self):
        r = mh847_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertEqual(r["e_pv_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_pv_auto_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_immessa_kwh_e_anno"], 0.0)
        self.assertEqual(r["e_deficit_kwh_e_anno"],
                         r["e_frigo_alt_kwh_e_anno"])
        self.assertTrue(r["valid"])

    def test_calcola_accetta_dict_singolo(self):
        a = mh847_calcola(mh847_demo())
        b = mh847_calcola(**mh847_demo())
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])
        self.assertEqual(a["verdetto"], b["verdetto"])
        with self.assertRaises(ValueError):
            mh847_calcola("non-un-dict")


class TestFinanza(unittest.TestCase):
    def test_p_el_pareggio_demo_none(self):
        bc = mh847_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])
        self.assertIsNone(mh847_p_el_pareggio(8000, 12000,
                                              218087.65432098764,
                                              25150.15432098764, 0.09,
                                              66000.0, 0.05,
                                              286363.63636363635, 42875.0))

    def test_p_el_pareggio_none_casi(self):
        self.assertIsNone(mh847_p_el_pareggio(8000, 12000, 0.0, 0.0,
                                              0.09, 0.0, 0.05,
                                              196875.0, 196875.0))
        self.assertIsNone(mh847_calcola(**_demo_kwargs(
            cop_alt=2.2, p_pv_kwp=0, superficie_spogliatoi_m2=0,
            acs_litri_giorno=0, om_alt=8000))["p_el_pareggio"])

    def test_p_el_pareggio_costruito_positivo(self):
        base = _demo_kwargs(superficie_spogliatoi_m2=0,
                            acs_litri_giorno=0, p_pv_kwp=0)
        bc = mh847_calcola(**base)
        self.assertAlmostEqual(bc["p_el_pareggio"],
                               0.0446984126984127, places=12)
        self.assertAlmostEqual(mh847_p_el_pareggio(8000, 12000, 0.0, 0.0,
                                                   0.09, 0.0, 0.05,
                                                   286363.63636363635,
                                                   196875.0),
                               0.0446984126984127, places=12)

    def test_p_el_pareggio_verifica(self):
        base = _demo_kwargs(superficie_spogliatoi_m2=0,
                            acs_litri_giorno=0, p_pv_kwp=0)
        bc = mh847_calcola(**base)
        pstar = bc["p_el_pareggio"]
        r = mh847_calcola(**_demo_kwargs(superficie_spogliatoi_m2=0,
                                         acs_litri_giorno=0, p_pv_kwp=0,
                                         p_el=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_el_pareggio_soglia_minima(self):
        base = _demo_kwargs(superficie_spogliatoi_m2=0,
                            acs_litri_giorno=0, p_pv_kwp=0)
        pstar = mh847_calcola(**base)["p_el_pareggio"]
        self.assertAlmostEqual(
            mh847_calcola(**_demo_kwargs(superficie_spogliatoi_m2=0,
                                         acs_litri_giorno=0, p_pv_kwp=0,
                                         p_el=pstar + 0.01))
            ["risparmio_eur_anno"], 894.886363636364, places=6)
        self.assertAlmostEqual(
            mh847_calcola(**_demo_kwargs(superficie_spogliatoi_m2=0,
                                         acs_litri_giorno=0, p_pv_kwp=0,
                                         p_el=pstar - 0.01))
            ["risparmio_eur_anno"], -894.886363636364, places=6)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh847_flussi(450000, 70231.875, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -450000)
        self.assertTrue(all(f == 70231.875 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 278982.84588024445, places=6)
        self.assertAlmostEqual(mh847_van([-450000] + [70231.875] * 15,
                                         0.0), 603478.125, places=6)

    def test_van_usa_percentuale_non_frazione(self):
        self.assertAlmostEqual(mh847_van([-450000] + [70231.875] * 15,
                                         5.0), 278982.84588024445, places=6)
        self.assertGreater(mh847_van([-450000] + [70231.875] * 15, 0.05),
                           278982.84588024445)

    def test_tir_demo_e_none(self):
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 13.166002809225741, places=6)
        self.assertGreater(bc["tir"], 13.0)
        self.assertIsNone(mh847_tir([-100.0, -10.0, -10.0]))

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh847_payback([-450000] + [70231.875] * 15), 7)
        self.assertEqual(mh847_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh847_payback([-450000] + [100.0] * 15))

    def test_verdetto_percentuale(self):
        self.assertEqual(mh847_verdetto(70231.875, 100.0, 450000, 10),
                         "CONVIENTE")
        self.assertEqual(mh847_verdetto(70231.875, -20000.0, 450000, 10),
                         "MARGINALE")
        self.assertEqual(mh847_verdetto(70231.875, -100000.0, 450000, 10),
                         "NON_CONVIENTE")
        self.assertEqual(mh847_verdetto(0.0, 100.0, 450000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh847_verdetto(-100.0, 100.0, 450000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh847_verdetto(None, 100.0, 450000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh847_verdetto(70231.875, 0.0, 450000, 10),
                         "MARGINALE")
        self.assertEqual(mh847_verdetto(70231.875, -71017.1541197555,
                                        800000, 10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh847_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("superficie_pista_m2", "1800"),
                            ("superficie_pista_m2", float("nan")),
                            ("superficie_pista_m2", float("inf")),
                            ("superficie_pista_m2", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh847_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"superficie_pista_m2": 0},
                     {"superficie_pista_m2": -1},
                     {"q_pista": -1},
                     {"cop_base": 0},
                     {"cop_base": -1},
                     {"cop_alt": 0},
                     {"cop_alt": -1},
                     {"superficie_spogliatoi_m2": -1},
                     {"q_risc": -1},
                     {"acs_litri_giorno": -1},
                     {"acs_giorni_anno": -1},
                     {"acs_dt": -1},
                     {"eta_caldaia": 0},
                     {"eta_caldaia": 1.1},
                     {"f_rec": -0.1},
                     {"f_rec": 1.1},
                     {"f_uso": -0.1},
                     {"f_uso": 1.1},
                     {"p_pv_kwp": -1},
                     {"prod_specifica": -1},
                     {"f_autoconsumo": -0.1},
                     {"f_autoconsumo": 1.1},
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
            self.assertFalse(mh847_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh847_valida(**_demo_kwargs(wacc=25))["valido"])
        self.assertTrue(mh847_valida(**_demo_kwargs(tolleranza=150))["valido"])
        self.assertTrue(mh847_valida(**_demo_kwargs(
            q_pista=0, superficie_spogliatoi_m2=0, q_risc=0,
            acs_litri_giorno=0, acs_giorni_anno=0, acs_dt=0,
            f_rec=0, f_uso=0, p_pv_kwp=0, prod_specifica=0,
            f_autoconsumo=0, p_el=0, p_gas=0, p_immissione=0,
            om_base=0, om_alt=0, capex=0, f_el=0, f_gas=0,
            wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh847_demo()
        self.assertEqual(d["superficie_pista_m2"], 1800)
        self.assertEqual(d["q_pista"], 350)
        self.assertEqual(d["cop_base"], 2.2)
        self.assertEqual(d["cop_alt"], 3.2)
        self.assertEqual(d["superficie_spogliatoi_m2"], 1000)
        self.assertEqual(d["q_risc"], 180)
        self.assertEqual(d["acs_litri_giorno"], 2000)
        self.assertEqual(d["acs_giorni_anno"], 200)
        self.assertEqual(d["acs_dt"], 35)
        self.assertEqual(d["eta_caldaia"], 0.9)
        self.assertEqual(d["f_rec"], 0.60)
        self.assertEqual(d["f_uso"], 0.35)
        self.assertEqual(d["p_pv_kwp"], 200)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["f_autoconsumo"], 0.70)
        self.assertEqual(d["p_el"], 0.22)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["p_immissione"], 0.05)
        self.assertEqual(d["om_base"], 8000)
        self.assertEqual(d["om_alt"], 12000)
        self.assertEqual(d["capex"], 450000)
        self.assertEqual(d["f_el"], 0.00035)
        self.assertEqual(d["f_gas"], 0.00020)
        self.assertEqual(d["wacc"], 5)
        self.assertEqual(d["vita"], 15)
        self.assertEqual(d["tolleranza"], 10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh847_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["q_freddo_kwh_c_anno"], 630000.0, places=6)
        self.assertEqual(bc["e_frigo_alt_kwh_e_anno"], 196875.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 220000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 90627.88888888889, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 20396.013888888887, places=6)
        self.assertEqual(bc["capex_eur"], 450000.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh847_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[1],
                               -379768.125, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[7],
                               41623.125, places=6)

    def test_demo_tabella_righe(self):
        bc = mh847_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie pista (m2)", voci)
        self.assertIn("Carico frigorifero pista (kWh_c/anno)", voci)
        self.assertIn("Elettricita' frigorifero base (kWh_e/anno)", voci)
        self.assertIn("Calore di condensazione alternativo (kWh_c/anno)", voci)
        self.assertIn("Fabbisogno termico totale (kWh_th/anno)", voci)
        self.assertIn("Calore recuperato (kWh_th/anno)", voci)
        self.assertIn("Energia immessa, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("CAPEX totale (EUR)", voci)
        self.assertIn("Prezzo elettrico di pareggio (EUR/kWh, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["q_freddo_kwh_c_anno"],
                               bc["superficie_pista_m2"] * bc["q_pista"])
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
                               / bc["eta_caldaia"])

    def test_demo_contro_riconteggio_indipendente(self):
        qfreddo = 1800 * 350
        ebase = qfreddo / 2.2
        ealt = qfreddo / 3.2
        qcond = qfreddo + ealt
        qr = 1000 * 180
        qacs = 2000 * 200 * 4.186 * 35 / 3600
        qterm = qr + qacs
        qrec = min(qterm, qcond * 0.60 * 0.35)
        qnet = max(0, qterm - qrec)
        gbase = qterm / 0.9
        galt = qnet / 0.9
        epv = 200 * 1100
        eauto = min(epv * 0.70, ealt)
        edef = max(0, ealt - eauto)
        eimm = epv - eauto
        c_base = ebase * 0.22 + gbase * 0.09 + 8000
        c_alt = edef * 0.22 - eimm * 0.05 + galt * 0.09 + 12000
        bc = mh847_demo_calcoli()
        self.assertAlmostEqual(bc["q_freddo_kwh_c_anno"], qfreddo, places=6)
        self.assertAlmostEqual(bc["e_frigo_base_kwh_e_anno"], ebase, places=6)
        self.assertAlmostEqual(bc["e_frigo_alt_kwh_e_anno"], ealt, places=6)
        self.assertAlmostEqual(bc["q_cond_alt_kwh_c_anno"], qcond, places=6)
        self.assertAlmostEqual(bc["q_acs_kwh_th_anno"], qacs, places=6)
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
        bc = mh847_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_p_el_piu_meno_20(self):
        meno = mh847_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 59518.374999999985,
                               places=6)
        self.assertAlmostEqual(meno["van"], 167780.37948819646, places=6)
        self.assertAlmostEqual(meno["tir"], 10.105041920305945, places=6)
        self.assertEqual(meno["payback"], 8)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh847_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 80945.375,
                               places=6)
        self.assertAlmostEqual(piu["van"], 390185.31227229215, places=6)
        self.assertAlmostEqual(piu["tir"], 16.0619775049766, places=6)
        self.assertEqual(piu["payback"], 6)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_p_el_alto_migliora_il_caso(self):
        demo = mh847_demo_calcoli()
        meno = mh847_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh847_calcola(**_demo_kwargs(p_el=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_non_convinte(self):
        r = mh847_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 33051.875,
                               places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -106932.83997930987, places=6)
        self.assertAlmostEqual(r["tir"], 1.2361957820349374, places=6)
        self.assertEqual(r["payback"], 14)

    def test_variante_senza_recupero_convinte(self):
        r = mh847_calcola(**_demo_kwargs(f_rec=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 52867.5,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 98746.5713335123, places=6)
        self.assertAlmostEqual(r["tir"], 8.091535242978408, places=6)
        self.assertEqual(r["payback"], 9)

    def test_variante_capex_doppio_non_convinte(self):
        r = mh847_calcola(**_demo_kwargs(capex=900000))
        self.assertAlmostEqual(r["van"], -171017.1541197555, places=6)
        self.assertAlmostEqual(r["tir"], 2.036031769758264, places=6)
        self.assertEqual(r["payback"], 13)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertEqual(r["capex_eur"], 900000.0)

    def test_variante_capex_marginale(self):
        r = mh847_calcola(**_demo_kwargs(capex=800000))
        self.assertAlmostEqual(r["van"], -71017.1541197555, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")

    def test_variante_vita_10_convinte(self):
        r = mh847_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 92311.92232964147, places=6)
        self.assertAlmostEqual(r["tir"], 9.036545810060655, places=6)
        self.assertEqual(r["payback"], 7)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh847_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 603478.125, places=6)
        self.assertEqual(zero["payback"], 7)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh847_sensibilita(**mh847_demo())
        self.assertEqual(set(s.keys()), {"p_el_meno20", "p_el_piu20",
                                         "senza_fv", "senza_recupero",
                                         "capex_doppio", "vita_10",
                                         "wacc_0"})
        self.assertAlmostEqual(s["p_el_meno20"]["risparmio_eur_anno"],
                               59518.374999999985, places=6)
        self.assertAlmostEqual(s["p_el_piu20"]["van"],
                               390185.31227229215, places=6)
        self.assertEqual(s["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh847_demo_calcoli()
        b = mh847_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh847_demo()
        attese = {"superficie_pista_m2", "q_pista",
                  "cop_base", "cop_alt",
                  "superficie_spogliatoi_m2", "q_risc",
                  "acs_litri_giorno", "acs_giorni_anno", "acs_dt",
                  "eta_caldaia", "f_rec", "f_uso", "p_pv_kwp",
                  "prod_specifica", "f_autoconsumo", "p_el", "p_gas",
                  "p_immissione", "om_base", "om_alt", "capex",
                  "f_el", "f_gas", "wacc", "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["superficie_pista_m2", "q_pista", "cop_base", "cop_alt",
                 "superficie_spogliatoi_m2", "q_risc",
                 "acs_litri_giorno", "acs_giorni_anno", "acs_dt",
                 "eta_caldaia", "f_rec", "f_uso", "p_pv_kwp",
                 "prod_specifica", "f_autoconsumo", "p_el", "p_gas",
                 "p_immissione", "om_base", "om_alt", "capex",
                 "f_el", "f_gas", "wacc", "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh847_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_cop_zero_pista_zero_e_vita(self):
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(f_rec=1.1))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(f_uso=1.1))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(f_autoconsumo=1.1))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(cop_base=0))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(cop_alt=0))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(superficie_pista_m2=0))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh847_calcola(**_demo_kwargs(vita=15.5))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("superficie_pista_m2", "1800"),
                           ("superficie_pista_m2", float("nan")),
                           ("capex", float("inf")),
                           ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh847_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh847_calcola(**_demo_kwargs(
            q_pista=0, superficie_spogliatoi_m2=0, q_risc=0,
            acs_litri_giorno=0, acs_giorni_anno=0, acs_dt=0,
            f_rec=0, f_uso=0, p_pv_kwp=0, prod_specifica=0,
            f_autoconsumo=0, p_el=0, p_gas=0, p_immissione=0,
            om_base=0, om_alt=0, capex=0, f_el=0, f_gas=0,
            wacc=0, tolleranza=0))
        self.assertTrue(r["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh847_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(r["risparmio_eur_anno"], -117768.125,
                               places=6)

    def test_pareggio_esatto_soglia(self):
        base = _demo_kwargs(superficie_spogliatoi_m2=0,
                            acs_litri_giorno=0, p_pv_kwp=0)
        pstar = mh847_calcola(**base)["p_el_pareggio"]
        r = mh847_calcola(**_demo_kwargs(superficie_spogliatoi_m2=0,
                                         acs_litri_giorno=0, p_pv_kwp=0,
                                         p_el=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh847_demo_calcoli()
        csv = mh847_csv(bc, dict(mh847_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh847_demo_calcoli()
        csv = mh847_csv(bc, dict(mh847_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1]
                 for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]),
                               70231.875, places=6)
        self.assertIn("p_el_pareggio", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh847_demo_calcoli()
        csv = mh847_csv(bc, dict(mh847_demo()))
        for chiave in mh847_demo().keys():
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
        self.assertEqual(src.count("with tab847:"), 1)
        self.assertTrue(src.startswith("    # W850"))

    def test_ui_tab847_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre la scheda attesa
        # esattamente una volta e gli helper definiscono
        # le funzioni attese.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab847:"), 1)
        self.assertIn("def mh847_demo(", src_h)
        self.assertIn("def mh847_calcola(", src_h)
        self.assertIn("tab847", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Palaghiaccio: frigorifero efficiente + recupero calore + fotovoltaico battono frigorifero tradizionale + caldaia a gas?", src)
        self.assertIn("⛸️ Palaghiaccio: frigorifero efficiente + recupero calore + fotovoltaico battono frigorifero tradizionale + caldaia a gas?", src)
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
        chiavi = re.findall(r'key="(st847_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st847_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st847_calcola"', src)
        self.assertIn('key="st847_csv"', src)
        self.assertIn('key="st847_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def847\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh847_demo().keys()), lette - set(mh847_demo().keys()))
        self.assertEqual(lette, set(mh847_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc847\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc847\["([^"]+)"\]', src))
        attese = set(mh847_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg847"), src.index(".paiac("))
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
