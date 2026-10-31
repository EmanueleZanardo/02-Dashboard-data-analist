"""Test nuova scheda tab839 "Rifugio alpino:
fotovoltaico + batteria + pompa di calore
battono generatore diesel + caldaia a
gasolio in autonomia off-grid?".

Business case deterministico di un rifugio
alpino off-grid guidato dal PRODOTTO posti
letto x giorni di apertura:
Q_term = posti x giorni x q_spec_termico;
E_el = posti x giorni x e_spec_elettrico;
E_pdc = Q_term / COP; E_tot_alt = E_pdc +
E_el; E_pv = kWp x producibilita';
E_pv_diretta = E_pv x quota_diretta;
E_pv_batt_lordo = E_pv x (1 - quota_diretta);
E_pv_batt_netta = min(lordo x RTE,
cap_batt x DoD x cicli_anno) (cap annuo di
throughput batteria); E_pv_servita =
min(diretta + netta, E_tot_alt);
E_pv_sprecata = E_pv - servito (eccesso +
perdite round-trip, NESSUN credito di
costo ne' di CO2: scelta conservativa
off-grid, niente rete in cui immettere);
E_diesel_residuo = E_tot_alt - servito;
autonomia_batt = cap_batt x DoD /
(E_tot_alt / giorni) (0 se domanda nulla);
litri_base_el = E_el / eta_gen / 9,9;
litri_base_calore = Q_term / eta_caldaia /
9,9; litri_residuo = E_diesel_residuo /
eta_gen / 9,9; C_base = litri_base_tot x
p_diesel + O&M_base; C_alt = litri_residuo
x p_diesel + O&M_alt; risparmio = C_base -
C_alt; CO2 base = litri_base_tot x
f_co2_diesel / 1000; CO2 alt =
litri_residuo x f_co2_diesel / 1000; CO2
evitata = base - alt (segno libero, non
clampata: puo' essere negativa se il
diesel residuo supera la base);
flussi [-CAPEX, risparmio x vita]; VAN al
WACC (FRAZIONE, non percentuale); TIR per
bisezione; payback (primo anno con
cumulato >= 0); prezzo diesel di pareggio
p* = (O&M_alt - O&M_base) / (litri_base_tot
- litri_residuo) in forma chiusa, None se
litri_base_tot <= litri_residuo o se p* < 0,
SOGLIA MINIMA sui soli costi annui quando
esiste (sopra di essa l'alternativa vince,
sotto perde; il CAPEX non entra nel
pareggio annuo). Per COP NON viene
dichiarato alcun pareggio: il pareggio
dichiarato qui e' SOLO p_diesel_pareggio.
Verdetto: NON_CALCOLABILE se input
degenere (posti <= 0 o non interi, giorni
<= 0 o non interi, fabbisogni specifici
< 0, rendimenti <= 0 o > 1, prezzo diesel
< 0, COP <= 0, quota_diretta < 0 o > 1,
RTE <= 0 o > 1, cap_batt < 0, DoD < 0 o > 1,
cicli < 0, kWp < 0, producibilita' < 0,
O&M < 0, CAPEX < 0, fattore CO2 < 0,
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
previsto (posti, giorni, vita, COP,
rendimenti, RTE). Gli zeri ammessi in
entrambi (fabbisogni specifici, prezzo
diesel, quota_diretta, cap_batt, DoD,
cicli, kWp, producibilita', O&M, CAPEX,
fattore CO2, WACC, tolleranza) non creano
divergenza. Quote e DoD > 1 e rendimenti
> 1 sono degeneri in entrambi ma non
raggiungibili via slider (tetto 1,0).
WACC sopra 0,20 e tolleranza sopra 1,0
sono ammessi negli helper e limitati solo
dagli slider UI (0,20 e 1,0): nessuna
divergenza nel range raggiungibile,
perche' la guard controlla solo gli
stessi limiti degli helper. Distinzione
esplicita: distinto dall'albergo di
fondovalle connesso alla rete (eccesso FV
immesso e valorizzato: qui off-grid,
eccesso sprecato senza credito) e dalla
baita privata stagionale (pochi posti e
carichi discontinui: qui 40 posti e 180
giorni con domanda continuativa): qui
driver posti x giorni + FV + batteria +
pompa di calore + diesel solo residuo.

Demo (rifugio): 40 posti, 180 giorni,
q_spec_termico 12 (Q_term 86.400,00
kWh_th/anno), e_spec 4 (E_el 28.800,00
kWh_e/anno), eta_gen 0,32, eta_caldaia
0,85, prezzo diesel consegnato in quota
2,20 EUR/l, COP 2,8 (E_pdc 30.857,14,
E_tot_alt 59.657,14 kWh_e/anno),
quota_diretta 0,40, RTE 0,90, batteria 100
kWh con DoD 0,80 e 200 cicli/anno (cap
throughput 16.000,00 kWh_e/anno),
fotovoltaico 50 kWp a 1.300
kWh/kWp/anno (E_pv 65.000,00, diretta
26.000,00, batt lordo 39.000,00, batt
netta 16.000,00, servito 42.000,00,
sprecato 23.000,00 senza credito, diesel
residuo 17.657,14 kWh_e/anno, autonomia
0,24 giorni), litri base el 9.090,91,
litri base calore 10.267,38, litri base
tot 19.358,29, litri residuo 5.573,59,
O&M base 2.000, O&M alt 6.000, CAPEX
320.000 EUR, fattore CO2 diesel 2,68
kg/l, WACC 0,05 (frazione), vita 20 anni,
tolleranza 0,10 (frazione del CAPEX).
Valori calcolati eseguendo
mh839_demo_calcoli(): Q_term 86400,0,
E_el 28800,0, E_pdc 30857,14285714286,
E_tot_alt 59657,142857142855, E_pv
65000,0, diretta 26000,0, batt lordo
39000,0, batt netta 16000,0, servito
42000,0, sprecato 23000,0, diesel residuo
17657,142857142855, autonomia
0,24137931034482757, litri base el
9090,90909090909, litri base calore
10267,379679144386, litri base tot
19358,288770053477, litri residuo
5573,593073593072, C_base
44588,23529411765, C_alt
18261,90476190476, risparmio
26326,33053221289, CO2_base
51,880213903743325, CO2_alt
14,937229437229435, CO2_evitata
36,94298446651389, VAN 8084,268639669561,
TIR 5,296147967026567 %, payback 13,
p_diesel_pareggio 0,2901768808017364,
verdetto CONVIENTE (fragile: VAN solo il
2,53 % del CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab839 in app.py NON e'
incluso in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza in app.py spetta
alla fase di apply del worker, non a
questa fase. Tutti i test qui inclusi
passano da hidden_files senza app.py.

Destinazione nel repo: tests/test_w839_rifugio.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w842_helpers import (
        demo_calcoli,
        mh839_autonomia_batt,
        mh839_c_alt,
        mh839_c_base,
        mh839_calcola,
        mh839_co2,
        mh839_co2_evitata,
        mh839_csv,
        mh839_demo,
        mh839_demo_calcoli,
        mh839_e_el,
        mh839_e_pdc,
        mh839_e_pv,
        mh839_e_tot_alt,
        mh839_eta,
        mh839_frazione,
        mh839_int_pos,
        mh839_litri,
        mh839_nneg,
        mh839_num,
        mh839_p_diesel_pareggio,
        mh839_payback,
        mh839_pos,
        mh839_pv_batt_lordo,
        mh839_pv_batt_netta,
        mh839_pv_diretta,
        mh839_pv_servita,
        mh839_pv_servita_pot,
        mh839_pv_sprecata,
        mh839_q_termico,
        mh839_risparmio,
        mh839_sensibilita,
        mh839_tir,
        mh839_valida,
        mh839_van,
        mh839_verdetto,
        mh839_e_diesel_residuo,
        mh839_flussi,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w842_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w842_helpers", os.path.join(_hf, "w842_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh839_autonomia_batt = _mod.mh839_autonomia_batt
    mh839_c_alt = _mod.mh839_c_alt
    mh839_c_base = _mod.mh839_c_base
    mh839_calcola = _mod.mh839_calcola
    mh839_co2 = _mod.mh839_co2
    mh839_co2_evitata = _mod.mh839_co2_evitata
    mh839_csv = _mod.mh839_csv
    mh839_demo = _mod.mh839_demo
    mh839_demo_calcoli = _mod.mh839_demo_calcoli
    mh839_e_el = _mod.mh839_e_el
    mh839_e_pdc = _mod.mh839_e_pdc
    mh839_e_pv = _mod.mh839_e_pv
    mh839_e_tot_alt = _mod.mh839_e_tot_alt
    mh839_eta = _mod.mh839_eta
    mh839_frazione = _mod.mh839_frazione
    mh839_int_pos = _mod.mh839_int_pos
    mh839_litri = _mod.mh839_litri
    mh839_nneg = _mod.mh839_nneg
    mh839_num = _mod.mh839_num
    mh839_p_diesel_pareggio = _mod.mh839_p_diesel_pareggio
    mh839_payback = _mod.mh839_payback
    mh839_pos = _mod.mh839_pos
    mh839_pv_batt_lordo = _mod.mh839_pv_batt_lordo
    mh839_pv_batt_netta = _mod.mh839_pv_batt_netta
    mh839_pv_diretta = _mod.mh839_pv_diretta
    mh839_pv_servita = _mod.mh839_pv_servita
    mh839_pv_servita_pot = _mod.mh839_pv_servita_pot
    mh839_pv_sprecata = _mod.mh839_pv_sprecata
    mh839_q_termico = _mod.mh839_q_termico
    mh839_risparmio = _mod.mh839_risparmio
    mh839_sensibilita = _mod.mh839_sensibilita
    mh839_tir = _mod.mh839_tir
    mh839_valida = _mod.mh839_valida
    mh839_van = _mod.mh839_van
    mh839_verdetto = _mod.mh839_verdetto
    mh839_e_diesel_residuo = _mod.mh839_e_diesel_residuo
    mh839_flussi = _mod.mh839_flussi

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w842_helpers.py")
_UI_PATH = _risolvi("w842_ui.py")

_DEMO = {
    "q_termico_kwh_th_anno": 86400.0,
    "e_el_kwh_e_anno": 28800.0,
    "e_pdc_kwh_e_anno": 30857.14285714286,
    "e_tot_alt_kwh_e_anno": 59657.142857142855,
    "e_pv_kwh_e_anno": 65000.0,
    "e_pv_diretta_kwh_e_anno": 26000.0,
    "e_pv_batt_lordo_kwh_e_anno": 39000.0,
    "e_pv_batt_netta_kwh_e_anno": 16000.0,
    "e_pv_servita_kwh_e_anno": 42000.0,
    "e_pv_sprecata_kwh_e_anno": 23000.0,
    "e_diesel_residuo_kwh_e_anno": 17657.142857142855,
    "autonomia_batt_giorni": 0.24137931034482757,
    "litri_base_el_l_anno": 9090.90909090909,
    "litri_base_calore_l_anno": 10267.379679144386,
    "litri_base_tot_l_anno": 19358.288770053477,
    "litri_diesel_residuo_l_anno": 5573.593073593072,
    "c_base_eur_anno": 44588.23529411765,
    "c_alt_eur_anno": 18261.90476190476,
    "risparmio_eur_anno": 26326.33053221289,
    "co2_base_t_anno": 51.880213903743325,
    "co2_alt_t_anno": 14.937229437229435,
    "co2_evitata_t_anno": 36.94298446651389,
    "van": 8084.268639669561,
    "tir": 5.296147967026567,
    "payback": 13,
    "p_diesel_pareggio": 0.2901768808017364,
}


def _demo_kwargs(**over):
    kw = dict(mh839_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh839_num(3, "x"), 3.0)
        self.assertEqual(mh839_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh839_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh839_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh839_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh839_pos(0, "x")
        with self.assertRaises(ValueError):
            mh839_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh839_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh839_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh839_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh839_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh839_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh839_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh839_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh839_frazione(0, "quota"), 0.0)
        self.assertEqual(mh839_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh839_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh839_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_termico_e_el_driver_posti_giorni(self):
        self.assertEqual(mh839_q_termico(40, 180, 12), 86400.0)
        self.assertEqual(mh839_e_el(40, 180, 4), 28800.0)

    def test_e_pdc_e_tot(self):
        self.assertAlmostEqual(mh839_e_pdc(86400.0, 2.8), 30857.14285714286, places=6)
        self.assertAlmostEqual(mh839_e_tot_alt(30857.14285714286, 28800.0), 59657.142857142855, places=6)

    def test_pv_diretta_lordo(self):
        self.assertEqual(mh839_e_pv(50, 1300), 65000.0)
        self.assertEqual(mh839_pv_diretta(65000.0, 0.40), 26000.0)
        self.assertEqual(mh839_pv_batt_lordo(65000.0, 0.40), 39000.0)

    def test_batt_netta_cap_throughput_lega(self):
        self.assertEqual(mh839_pv_batt_netta(39000.0, 0.90, 100, 0.80, 200), 16000.0)
        self.assertEqual(mh839_pv_batt_netta(39000.0, 0.90, 10000, 0.80, 200), 35100.0)
        self.assertEqual(mh839_pv_batt_netta(39000.0, 0.90, 0, 0.80, 200), 0.0)

    def test_servita_cappata_a_domanda_e_sprecata(self):
        self.assertEqual(mh839_pv_servita_pot(26000.0, 16000.0), 42000.0)
        self.assertEqual(mh839_pv_servita(42000.0, 59657.142857142855), 42000.0)
        self.assertEqual(mh839_pv_servita(80000.0, 59657.142857142855), 59657.142857142855)
        self.assertEqual(mh839_pv_sprecata(65000.0, 42000.0), 23000.0)

    def test_diesel_residuo_e_autonomia(self):
        self.assertAlmostEqual(mh839_e_diesel_residuo(59657.142857142855, 42000.0), 17657.142857142855, places=6)
        self.assertAlmostEqual(mh839_autonomia_batt(100, 0.80, 59657.142857142855, 180), 0.24137931034482757, places=12)
        self.assertEqual(mh839_autonomia_batt(100, 0.80, 0, 180), 0.0)

    def test_litri_contenuto_9_9(self):
        self.assertAlmostEqual(mh839_litri(28800.0, 0.32), 9090.90909090909, places=6)
        self.assertAlmostEqual(mh839_litri(86400.0, 0.85), 10267.379679144386, places=6)
        self.assertAlmostEqual(mh839_litri(17657.142857142855, 0.32), 5573.593073593072, places=6)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh839_c_base(19358.288770053477, 2.20, 2000), 44588.23529411765, places=6)
        self.assertAlmostEqual(mh839_c_alt(5573.593073593072, 2.20, 6000), 18261.90476190476, places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh839_risparmio(44588.23529411765, 18261.90476190476), 26326.33053221289, places=6)
        self.assertLess(mh839_risparmio(18261.90476190476, 44588.23529411765), 0.0)

    def test_co2_unico_fattore_e_evitata(self):
        self.assertAlmostEqual(mh839_co2(19358.288770053477, 2.68), 51.880213903743325, places=6)
        self.assertAlmostEqual(mh839_co2(5573.593073593072, 2.68), 14.937229437229435, places=6)
        self.assertAlmostEqual(mh839_co2_evitata(19358.288770053477, 5573.593073593072, 2.68), 36.94298446651389, places=6)

    def test_co2_evitata_negativa_non_clampata(self):
        self.assertAlmostEqual(mh839_co2_evitata(100.0, 2000.0, 2.68), -5.092, places=6)

    def test_sprecato_senza_credito(self):
        bc = mh839_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_sprecata_kwh_e_anno"], 23000.0, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"],
                               bc["e_pv_servita_kwh_e_anno"] + bc["e_pv_sprecata_kwh_e_anno"], places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["litri_diesel_residuo_l_anno"] * 2.20 + 6000, places=6)


class TestFinanza(unittest.TestCase):
    def test_p_diesel_pareggio_demo_valore(self):
        p = mh839_p_diesel_pareggio(6000, 2000, 19358.288770053477, 5573.593073593072)
        self.assertAlmostEqual(p, 0.2901768808017364, places=12)

    def test_p_diesel_pareggio_none_casi(self):
        self.assertIsNone(mh839_p_diesel_pareggio(6000, 2000, 5000.0, 6000.0))
        self.assertIsNone(mh839_p_diesel_pareggio(6000, 2000, 5000.0, 5000.0))
        self.assertIsNone(mh839_p_diesel_pareggio(1000, 2000, 19358.288770053477, 5573.593073593072))
        self.assertEqual(mh839_p_diesel_pareggio(2000, 2000, 19358.288770053477, 5573.593073593072), 0.0)

    def test_p_diesel_pareggio_verifica_su_demo(self):
        bc = mh839_demo_calcoli()
        pstar = bc["p_diesel_pareggio"]
        r = mh839_calcola(**_demo_kwargs(p_diesel=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_diesel_pareggio_soglia_minima_su_demo(self):
        bc = mh839_demo_calcoli()
        pstar = bc["p_diesel_pareggio"]
        self.assertGreater(mh839_calcola(**_demo_kwargs(p_diesel=pstar + 0.10))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh839_calcola(**_demo_kwargs(p_diesel=pstar - 0.10))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh839_flussi(320000, 26326.33053221289, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -320000)
        self.assertTrue(all(f == 26326.33053221289 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh839_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 8084.268639669561, places=6)
        self.assertAlmostEqual(mh839_van([-320000] + [26326.33053221289] * 20, 0.0), 206526.61064425783, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh839_van([-320000] + [26326.33053221289] * 20, 0.05), 8084.268639669561, places=6)
        self.assertLess(mh839_van([-320000] + [26326.33053221289] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh839_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 5.296147967026567, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh839_payback([-320000] + [26326.33053221289] * 20), 13)
        self.assertEqual(mh839_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh839_payback([-320000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh839_verdetto(26326.33053221289, 100.0, 320000, 0.10), "CONVIENTE")
        self.assertEqual(mh839_verdetto(26326.33053221289, -20000.0, 320000, 0.10), "MARGINALE")
        self.assertEqual(mh839_verdetto(26326.33053221289, -100000.0, 320000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh839_verdetto(0.0, 100.0, 320000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh839_verdetto(-100.0, 100.0, 320000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh839_verdetto(None, 100.0, 320000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh839_verdetto(26326.33053221289, 0.0, 320000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh839_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("posti_letto", "40"), ("posti_letto", float("nan")),
                            ("posti_letto", float("inf")), ("posti_letto", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh839_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"posti_letto": 0}, {"posti_letto": -1},
                     {"posti_letto": 40.5},
                     {"giorni_apertura": 0}, {"giorni_apertura": 180.5},
                     {"q_spec_termico": -0.1}, {"e_spec_elettrico": -0.1},
                     {"eta_gen": 0}, {"eta_gen": 1.1},
                     {"eta_caldaia": 0}, {"eta_caldaia": 1.1},
                     {"p_diesel": -0.1},
                     {"cop": 0}, {"cop": -1},
                     {"quota_diretta": -0.1}, {"quota_diretta": 1.1},
                     {"rte": 0}, {"rte": 1.1},
                     {"cap_batt": -1},
                     {"dod": -0.1}, {"dod": 1.1},
                     {"cicli_anno": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"om_base": -1}, {"om_alt": -1},
                     {"capex": -1}, {"f_co2_diesel": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh839_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh839_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh839_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh839_valida(**_demo_kwargs(
            q_spec_termico=0, e_spec_elettrico=0,
            p_diesel=0, quota_diretta=0, cap_batt=0, dod=0,
            cicli_anno=0, p_pv_kwp=0, prod_specifica=0,
            om_base=0, om_alt=0, capex=0, f_co2_diesel=0,
            wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh839_demo()
        self.assertEqual(d["posti_letto"], 40)
        self.assertEqual(d["giorni_apertura"], 180)
        self.assertEqual(d["q_spec_termico"], 12)
        self.assertEqual(d["e_spec_elettrico"], 4)
        self.assertEqual(d["eta_gen"], 0.32)
        self.assertEqual(d["eta_caldaia"], 0.85)
        self.assertEqual(d["p_diesel"], 2.20)
        self.assertEqual(d["cop"], 2.8)
        self.assertEqual(d["quota_diretta"], 0.40)
        self.assertEqual(d["rte"], 0.90)
        self.assertEqual(d["cap_batt"], 100)
        self.assertEqual(d["dod"], 0.80)
        self.assertEqual(d["cicli_anno"], 200)
        self.assertEqual(d["p_pv_kwp"], 50)
        self.assertEqual(d["prod_specifica"], 1300)
        self.assertEqual(d["om_base"], 2000)
        self.assertEqual(d["om_alt"], 6000)
        self.assertEqual(d["capex"], 320000)
        self.assertEqual(d["f_co2_diesel"], 2.68)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh839_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh839_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], 86400.0, places=6)
        self.assertEqual(bc["e_el_kwh_e_anno"], 28800.0)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], 30857.14285714286, places=6)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 65000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 44588.23529411765, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 18261.90476190476, places=6)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh839_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[12], -4084.033613445288, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[13], 22242.2969187676, places=6)

    def test_demo_tabella_righe(self):
        bc = mh839_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Posti letto", voci)
        self.assertIn("Fotovoltaico netto da batteria (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico sprecato, senza credito (kWh_e/anno)", voci)
        self.assertIn("Autonomia batteria (giorni)", voci)
        self.assertIn("Litri diesel residuo (l/anno)", voci)
        self.assertIn("Prezzo diesel di pareggio (EUR/l, soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh839_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"],
                               bc["posti_letto"] * bc["giorni_apertura"] * bc["q_spec_termico"])
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] + bc["e_el_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_diesel_residuo_kwh_e_anno"],
                               bc["e_tot_alt_kwh_e_anno"] - bc["e_pv_servita_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        qterm = 40 * 180 * 12
        eel = 40 * 180 * 4
        epdc = qterm / 2.8
        etot = epdc + eel
        e_pv = 50 * 1300
        diretta = e_pv * 0.40
        batt_netta = min(e_pv * 0.60 * 0.90, 100 * 0.80 * 200)
        servita = min(diretta + batt_netta, etot)
        lit_tot = eel / 0.32 / 9.9 + qterm / 0.85 / 9.9
        lit_res = (etot - servita) / 0.32 / 9.9
        c_base = lit_tot * 2.20 + 2000
        c_alt = lit_res * 2.20 + 6000
        bc = mh839_demo_calcoli()
        self.assertAlmostEqual(bc["q_termico_kwh_th_anno"], qterm, places=6)
        self.assertAlmostEqual(bc["e_el_kwh_e_anno"], eel, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_tot_alt_kwh_e_anno"], etot, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_pv_servita_kwh_e_anno"], servita, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh839_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_diesel_piu_meno_20(self):
        meno = mh839_calcola(**_demo_kwargs(p_diesel=1.76))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 20261.064425770317, places=6)
        self.assertAlmostEqual(meno["van"], -67502.35336229621, places=6)
        self.assertAlmostEqual(meno["tir"], 2.362318581441568, places=6)
        self.assertEqual(meno["payback"], 16)
        self.assertEqual(meno["verdetto"], "NON_CONVIENTE")
        piu = mh839_calcola(**_demo_kwargs(p_diesel=2.64))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 32391.596638655472, places=6)
        self.assertAlmostEqual(piu["van"], 83670.89064163555, places=6)
        self.assertAlmostEqual(piu["tir"], 7.91697543130095, places=6)
        self.assertEqual(piu["payback"], 10)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_diesel_alto_migliora_il_caso(self):
        demo = mh839_demo_calcoli()
        meno = mh839_calcola(**_demo_kwargs(p_diesel=1.76))
        piu = mh839_calcola(**_demo_kwargs(p_diesel=2.64))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(demo["litri_base_tot_l_anno"], demo["litri_diesel_residuo_l_anno"])

    def test_variante_senza_fotovoltaico_non_calcolabile(self):
        r = mh839_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], -2840.336134453777, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertAlmostEqual(r["van"], -355396.86635107984, places=6)
        self.assertIsNone(r["tir"])
        self.assertIsNone(r["payback"])

    def test_variante_senza_batteria_non_convinte(self):
        r = mh839_calcola(**_demo_kwargs(cap_batt=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 15215.219421101778, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -130384.7351663301, places=6)
        self.assertAlmostEqual(r["tir"], -0.47427001118780093, places=6)
        self.assertIsNone(r["payback"])

    def test_variante_cop_basso_non_convinte(self):
        r = mh839_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 17754.901960784315, places=6)
        self.assertAlmostEqual(r["van"], -98734.6771535303, places=6)
        self.assertAlmostEqual(r["tir"], 1.012317921851317, places=6)
        self.assertEqual(r["payback"], 19)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_capex_doppio_non_convinte(self):
        r = mh839_calcola(**_demo_kwargs(capex=640000))
        self.assertAlmostEqual(r["van"], -311915.7313603305, places=6)
        self.assertAlmostEqual(r["tir"], -1.7908489651984523, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh839_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -116715.05397214719, places=6)
        self.assertAlmostEqual(r["tir"], -3.3997073604142, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh839_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 206526.61064425783, places=6)
        self.assertEqual(zero["payback"], 13)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh839_sensibilita(**mh839_demo())
        self.assertEqual(set(s.keys()), {"diesel_meno20", "diesel_piu20",
                                         "senza_pv", "senza_batt", "cop_2",
                                         "capex_doppio", "vita_10", "wacc_0"})
        self.assertAlmostEqual(s["diesel_meno20"]["risparmio_eur_anno"], 20261.064425770317, places=6)
        self.assertAlmostEqual(s["diesel_piu20"]["van"], 83670.89064163555, places=6)
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(s["senza_batt"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh839_demo_calcoli()
        b = mh839_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh839_demo()
        attese = {"posti_letto", "giorni_apertura", "q_spec_termico",
                  "e_spec_elettrico", "eta_gen", "eta_caldaia",
                  "p_diesel", "cop", "quota_diretta", "rte",
                  "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                  "prod_specifica", "om_base", "om_alt", "capex",
                  "f_co2_diesel", "wacc", "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["posti_letto", "giorni_apertura", "q_spec_termico",
                 "e_spec_elettrico", "eta_gen", "eta_caldaia",
                 "p_diesel", "cop", "quota_diretta", "rte",
                 "cap_batt", "dod", "cicli_anno", "p_pv_kwp",
                 "prod_specifica", "om_base", "om_alt", "capex",
                 "f_co2_diesel", "wacc", "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh839_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(quota_diretta=1.1))
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(dod=1.1))
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(eta_gen=1.1))
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(rte=1.1))
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh839_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("posti_letto", "40"), ("posti_letto", float("nan")),
                           ("capex", float("inf")), ("p_diesel", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh839_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh839_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_diretta=0,
                                         cap_batt=0, dod=0, cicli_anno=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_diesel=0))
        self.assertTrue(r["valid"])
        r2 = mh839_calcola(**_demo_kwargs(om_alt=30000, p_diesel=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh839_calcola(**_demo_kwargs(om_alt=60000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        pstar = mh839_demo_calcoli()["p_diesel_pareggio"]
        r = mh839_calcola(**_demo_kwargs(p_diesel=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh839_demo_calcoli()
        csv = mh839_csv(bc, dict(mh839_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh839_demo_calcoli()
        csv = mh839_csv(bc, dict(mh839_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]), 26326.33053221289, places=6)
        self.assertAlmostEqual(float(righe["p_diesel_pareggio"]), 0.2901768808017364, places=12)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh839_demo_calcoli()
        csv = mh839_csv(bc, dict(mh839_demo()))
        for chiave in mh839_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh838_", src)
        self.assertNotIn("mh837_", src)
        self.assertNotIn("mh836_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab839:"), 1)
        self.assertTrue(src.startswith("    # W842"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Rifugio alpino: fotovoltaico + batteria + pompa di calore battono generatore diesel + caldaia a gasolio in autonomia off-grid?", src)
        self.assertIn("🏔️ Rifugio alpino: fotovoltaico + batteria + pompa di calore battono generatore diesel + caldaia a gasolio in autonomia off-grid?", src)
        self.assertNotIn("tab838", src)
        self.assertNotIn("tab837", src)
        self.assertNotIn("tab836", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh838_", "mh837_", "mh836_", "mh835_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh838_", src)
        self.assertNotIn("st838_", src)
        self.assertNotIn("mh837_", src)
        self.assertNotIn("st837_", src)
        chiavi = re.findall(r'key="(st839_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st839_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st839_calcola"', src)
        self.assertIn('key="st839_csv"', src)
        self.assertIn('key="st839_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def839\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh839_demo().keys()), lette - set(mh839_demo().keys()))
        self.assertEqual(lette, set(mh839_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc839\['([^']+)'\]", src))
        attese = set(mh839_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg839"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
