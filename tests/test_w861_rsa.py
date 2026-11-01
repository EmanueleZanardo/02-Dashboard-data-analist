"""Test nuova scheda RSA / casa di riposo:
pompa di calore + recupero calore
lavanderia e cucina + FV battono caldaia
a gas + chiller tradizionale?

File: tests/test_w861_rsa.py

Business case annuo di una RSA / casa di
riposo, connessa alla rete, guidata dai
POSTI LETTO occupati stabilmente tutto
l'anno + SUPERFICIE TETTO (m2) + QUOTA FV
(non albergo, non ospedale, non serra
ne' altre tab alimentari):
E_el_posto_base = ill_base + lav_base +
altre_base; E_el_posto_alt = ill_alt +
lav_alt + altre_alt (efficiente, minore);
E_base_el_senza_freddo = posti x
E_el_posto_base; E_alt_el_senza_freddo_e_pdc
= posti x E_el_posto_alt;
Q_freddo = posti x q_freddo_per_posto;
freddo base = Q_freddo / EER_base
(chiller tradizionale); freddo alt =
Q_freddo / EER_alt (PdC reversibile);
E_base_el = E_base_el_senza_freddo +
freddo_base; E_alt_el_parziale =
E_alt_el_senza_freddo_e_pdc + freddo_alt;
Q_term_base = posti x (q_risc_base +
q_acs_base + q_cuc_lav_base); Q_term_alt
= posti x (q_risc_alt + q_acs_alt +
q_cuc_lav_alt); Q_rec = f_recupero x
Q_term_alt (25% del termico ALTERNATIVO,
non della base, da lavanderia e cucina);
Q_net = max(0, Q_term_alt - Q_rec);
Gas_base = Q_term_base / eta_caldaia;
Gas_alt = 0 (la caldaia a gas SCOMPARE:
il termico netto va in pompa di calore);
E_pdc = Q_net / COP_pdc; E_alt_el =
E_alt_el_parziale + E_pdc; kWp tetto =
sup_tetto_m2 x quota_fv x kwp_per_m2;
E_pv = kWp x resa_fv; E_pv_auto =
min(E_pv x f_autoconsumo, E_alt_el)
(cappato alla domanda elettrica
alternativa); E_immessa = E_pv -
E_pv_auto; E_deficit = max(0, E_alt_el -
E_pv_auto); C_base = E_base_el x p_el +
Gas_base x p_gas (nessun O&M); C_alt =
E_deficit x p_el - E_immessa x
p_immissione (gas alternativo zero;
l'immessa e' un RICAVO a prezzo di
immissione, INFERIORE a p_el; nessun
credito CO2 per l'immessa); risparmio =
C_base - C_alt; CAPEX forfettario
420.000 (PdC e reversibile 180.000 + FV
110.000 + efficientamento 80.000 +
recupero 50.000); CO2 base =
(E_base_el x f_el + Gas_base x f_gas) /
1000 (fattori in kg/kWh, divisione per
1000 in questa scheda); CO2 alt =
E_deficit x f_el / 1000 (gas alternativo
zero, nessun credito CO2 per l'immessa);
CO2 evitata = base - alt (segno libero);
flussi [-CAPEX, risparmio x vita];
VAN al WACC (PERCENTUALE in ingresso,
/ 100 dentro); TIR per bisezione; payback
(primo anno con cumulato >= 0); prezzo
elettrico di pareggio p_star =
(- Gas_base x p_gas - E_immessa x
p_immissione) / (E_base_el - E_deficit)
in forma chiusa a prezzo gas e prezzo
immissione FERMI (nessun O&M), None se
E_base_el - E_deficit <= 0 o se il
numeratore e' <= 0, SOGLIA MINIMA sui
soli costi annui quando esisterebbe (il
CAPEX non entra nel pareggio annuo).
Nel demo p_star grezzo e'
-0,8392543366169933 EUR/kWh, quindi
None: il numeratore e' negativo
(-34.851,20 EUR/anno circa: gas evitato
32.000,00 piu' ricavo da immissione
2.851,20; denominatore 41.526,39
kWh_e/anno), quindi l'alternativa vince
sui costi annui anche a prezzo elettrico
nullo. In regime valido con gas base
positivo o immessa positiva il pareggio
non puo' mai essere positivo, perche'
il numeratore e' sempre nullo o
negativo (nessun O&M a spostarlo).
Verdetto: NON_CALCOLABILE se input
degenere (posti <= 0, per-posto < 0,
q_freddo < 0, EER base <= 0, EER alt
<= 0, f_recupero < 0 o > 1, cop_pdc
<= 0, eta caldaia <= 0 o > 1, sup tetto
<= 0, quota fv < 0 o > 1, kwp per m2
< 0, resa fv < 0, f_autoconsumo < 0 o
> 1, prezzi < 0, CAPEX < 0, f_el < 0,
f_gas < 0, WACC < 0, vita <= 0 o non
intera, tolleranza < 0) o se risparmio
<= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza PERCENTUALE
del CAPEX, NON_CONVIENTE altrimenti.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w861_helpers import (
        demo_calcoli,
        mh857_c_alt,
        mh857_c_base,
        mh857_calcola,
        mh857_co2_alt,
        mh857_co2_base,
        mh857_co2_evitata,
        mh857_csv,
        mh857_demo,
        mh857_demo_calcoli,
        mh857_e_alt_el,
        mh857_e_alt_el_parziale,
        mh857_e_base_el,
        mh857_e_base_el_senza_freddo,
        mh857_e_alt_el_senza_freddo_e_pdc,
        mh857_e_deficit,
        mh857_e_el_posto_alt,
        mh857_e_el_posto_base,
        mh857_e_freddo,
        mh857_e_immessa,
        mh857_e_pdc,
        mh857_e_pv,
        mh857_e_pv_auto,
        mh857_eta,
        mh857_flussi,
        mh857_frazione,
        mh857_gas_alt,
        mh857_gas_base,
        mh857_int_pos,
        mh857_nneg,
        mh857_num,
        mh857_p_el_pareggio,
        mh857_p_pv_kwp,
        mh857_payback,
        mh857_pos,
        mh857_q_freddo,
        mh857_q_net,
        mh857_q_rec,
        mh857_q_term_alt,
        mh857_q_term_base,
        mh857_risparmio,
        mh857_sensibilita,
        mh857_tir,
        mh857_valida,
        mh857_van,
        mh857_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w861_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w861_helpers", os.path.join(_hf, "w861_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh857_c_alt = _mod.mh857_c_alt
    mh857_c_base = _mod.mh857_c_base
    mh857_calcola = _mod.mh857_calcola
    mh857_co2_alt = _mod.mh857_co2_alt
    mh857_co2_base = _mod.mh857_co2_base
    mh857_co2_evitata = _mod.mh857_co2_evitata
    mh857_csv = _mod.mh857_csv
    mh857_demo = _mod.mh857_demo
    mh857_demo_calcoli = _mod.mh857_demo_calcoli
    mh857_e_alt_el = _mod.mh857_e_alt_el
    mh857_e_alt_el_parziale = _mod.mh857_e_alt_el_parziale
    mh857_e_base_el = _mod.mh857_e_base_el
    mh857_e_base_el_senza_freddo = _mod.mh857_e_base_el_senza_freddo
    mh857_e_alt_el_senza_freddo_e_pdc = _mod.mh857_e_alt_el_senza_freddo_e_pdc
    mh857_e_deficit = _mod.mh857_e_deficit
    mh857_e_el_posto_alt = _mod.mh857_e_el_posto_alt
    mh857_e_el_posto_base = _mod.mh857_e_el_posto_base
    mh857_e_freddo = _mod.mh857_e_freddo
    mh857_e_immessa = _mod.mh857_e_immessa
    mh857_e_pdc = _mod.mh857_e_pdc
    mh857_e_pv = _mod.mh857_e_pv
    mh857_e_pv_auto = _mod.mh857_e_pv_auto
    mh857_eta = _mod.mh857_eta
    mh857_flussi = _mod.mh857_flussi
    mh857_frazione = _mod.mh857_frazione
    mh857_gas_alt = _mod.mh857_gas_alt
    mh857_gas_base = _mod.mh857_gas_base
    mh857_int_pos = _mod.mh857_int_pos
    mh857_nneg = _mod.mh857_nneg
    mh857_num = _mod.mh857_num
    mh857_p_el_pareggio = _mod.mh857_p_el_pareggio
    mh857_p_pv_kwp = _mod.mh857_p_pv_kwp
    mh857_payback = _mod.mh857_payback
    mh857_pos = _mod.mh857_pos
    mh857_q_freddo = _mod.mh857_q_freddo
    mh857_q_net = _mod.mh857_q_net
    mh857_q_rec = _mod.mh857_q_rec
    mh857_q_term_alt = _mod.mh857_q_term_alt
    mh857_q_term_base = _mod.mh857_q_term_base
    mh857_risparmio = _mod.mh857_risparmio
    mh857_sensibilita = _mod.mh857_sensibilita
    mh857_tir = _mod.mh857_tir
    mh857_valida = _mod.mh857_valida
    mh857_van = _mod.mh857_van
    mh857_verdetto = _mod.mh857_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w861_helpers.py")
_UI_PATH = _risolvi("w861_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "6"
_VECCHIO_TAB = "tab85" + "6"
_VECCHIO_ST = "st85" + "6_"
_IMP_STREAMLIT = "import " + "streamlit"

# Valori demo ricalcolati a mano dal brief
# (posti 80, per-posto base 1.500, alt 950).
_DEMO = {
    "e_el_posto_base_kwh_posto_anno": 1500.0,
    "e_el_posto_alt_kwh_posto_anno": 950.0,
    "e_base_el_senza_freddo_kwh_e_anno": 120000.0,
    "e_alt_el_senza_freddo_e_pdc_kwh_e_anno": 76000.0,
    "q_freddo_kwh_f_anno": 48000.0,
    "e_freddo_base_kwh_e_anno": 17142.857142857145,
    "e_freddo_alt_kwh_e_anno": 12000.0,
    "e_base_el_kwh_e_anno": 137142.85714285716,
    "e_alt_el_parziale_kwh_e_anno": 88000.0,
    "q_term_base_kwh_th_anno": 320000.0,
    "q_term_alt_kwh_th_anno": 232000.0,
    "q_rec_kwh_th_anno": 58000.0,
    "q_net_kwh_th_anno": 174000.0,
    "gas_base_kwh_anno": 355555.55555555556,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 51176.470588235294,
    "e_alt_el_kwh_e_anno": 139176.4705882353,
    "p_pv_kwp": 72.0,
    "e_pv_kwh_e_anno": 79200.0,
    "e_pv_auto_kwh_e_anno": 43560.0,
    "e_immessa_kwh_e_anno": 35640.0,
    "e_deficit_kwh_e_anno": 95616.4705882353,
    "c_base_eur_anno": 70400.0,
    "c_alt_eur_anno": 23921.411764705885,
    "risparmio_eur_anno": 46478.58823529411,
    "co2_base_t_anno": 119.11111111111111,
    "co2_alt_t_anno": 33.46576470588236,
    "co2_evitata_t_anno": 85.64534640522876,
    "van": 159225.9430125394,
    "tir": 9.142781327794458,
    "payback": 10,
}


def _rel(a, b):
    """Confronto con tolleranza relativa 1e-9."""
    if b == 0.0:
        return a == 0.0
    return abs(a - b) <= 1e-9 * abs(b)


class TestDemo(unittest.TestCase):
    """Demo ricalcolata a mano, valore per valore."""

    def test_per_posto_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_el_posto_base_kwh_posto_anno"],
                             _DEMO["e_el_posto_base_kwh_posto_anno"]))

    def test_per_posto_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_el_posto_alt_kwh_posto_anno"],
                             _DEMO["e_el_posto_alt_kwh_posto_anno"]))

    def test_senza_freddo_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_base_el_senza_freddo_kwh_e_anno"],
                             _DEMO["e_base_el_senza_freddo_kwh_e_anno"]))

    def test_senza_freddo_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_alt_el_senza_freddo_e_pdc_kwh_e_anno"],
                             _DEMO["e_alt_el_senza_freddo_e_pdc_kwh_e_anno"]))

    def test_q_freddo(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["q_freddo_kwh_f_anno"],
                             _DEMO["q_freddo_kwh_f_anno"]))

    def test_freddo_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_freddo_base_kwh_e_anno"],
                             _DEMO["e_freddo_base_kwh_e_anno"]))

    def test_freddo_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_freddo_alt_kwh_e_anno"],
                             _DEMO["e_freddo_alt_kwh_e_anno"]))

    def test_domanda_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_base_el_kwh_e_anno"],
                             _DEMO["e_base_el_kwh_e_anno"]))

    def test_domanda_parziale(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_alt_el_parziale_kwh_e_anno"],
                             _DEMO["e_alt_el_parziale_kwh_e_anno"]))

    def test_domanda_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_alt_el_kwh_e_anno"],
                             _DEMO["e_alt_el_kwh_e_anno"]))

    def test_termico_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["q_term_base_kwh_th_anno"],
                             _DEMO["q_term_base_kwh_th_anno"]))

    def test_termico_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["q_term_alt_kwh_th_anno"],
                             _DEMO["q_term_alt_kwh_th_anno"]))

    def test_recupero(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["q_rec_kwh_th_anno"],
                             _DEMO["q_rec_kwh_th_anno"]))

    def test_termico_netto(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["q_net_kwh_th_anno"],
                             _DEMO["q_net_kwh_th_anno"]))

    def test_gas_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["gas_base_kwh_anno"],
                             _DEMO["gas_base_kwh_anno"]))

    def test_gas_alt_zero(self):
        bc = mh857_demo_calcoli()
        self.assertEqual(bc["gas_alt_kwh_anno"], 0.0)

    def test_e_pdc(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_pdc_kwh_e_anno"],
                             _DEMO["e_pdc_kwh_e_anno"]))

    def test_p_pv(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["p_pv_kwp"], _DEMO["p_pv_kwp"]))

    def test_e_pv(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_pv_kwh_e_anno"],
                             _DEMO["e_pv_kwh_e_anno"]))

    def test_autoconsumo(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_pv_auto_kwh_e_anno"],
                             _DEMO["e_pv_auto_kwh_e_anno"]))

    def test_immessa(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_immessa_kwh_e_anno"],
                             _DEMO["e_immessa_kwh_e_anno"]))

    def test_deficit(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_deficit_kwh_e_anno"],
                             _DEMO["e_deficit_kwh_e_anno"]))

    def test_costo_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["c_base_eur_anno"],
                             _DEMO["c_base_eur_anno"]))

    def test_costo_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["c_alt_eur_anno"],
                             _DEMO["c_alt_eur_anno"]))

    def test_risparmio(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["risparmio_eur_anno"],
                             _DEMO["risparmio_eur_anno"]))

    def test_co2_base(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["co2_base_t_anno"],
                             _DEMO["co2_base_t_anno"]))

    def test_co2_alt(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["co2_alt_t_anno"],
                             _DEMO["co2_alt_t_anno"]))

    def test_co2_evitata(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["co2_evitata_t_anno"],
                             _DEMO["co2_evitata_t_anno"]))

    def test_van(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["van"], _DEMO["van"]))

    def test_tir(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["tir"], _DEMO["tir"]))

    def test_payback(self):
        bc = mh857_demo_calcoli()
        self.assertEqual(bc["payback"], _DEMO["payback"])

    def test_p_el_pareggio_none(self):
        bc = mh857_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])

    def test_verdetto_conviente(self):
        bc = mh857_demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_demo_dict_completo(self):
        """Ogni voce di _DEMO contro demo_calcoli()."""
        bc = mh857_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            self.assertTrue(_rel(bc[chiave], atteso),
                            f"{chiave}: {bc[chiave]} != {atteso}")

    def test_demo_input(self):
        d = mh857_demo()
        self.assertEqual(d["posti"], 80)
        self.assertEqual(d["ill_base"], 600)
        self.assertEqual(d["lav_base"], 400)
        self.assertEqual(d["altre_base"], 500)
        self.assertEqual(d["ill_alt"], 350)
        self.assertEqual(d["lav_alt"], 250)
        self.assertEqual(d["altre_alt"], 350)
        self.assertEqual(d["q_risc_base"], 2500)
        self.assertEqual(d["q_acs_base"], 800)
        self.assertEqual(d["q_cuc_lav_base"], 700)
        self.assertEqual(d["q_risc_alt"], 1800)
        self.assertEqual(d["q_acs_alt"], 600)
        self.assertEqual(d["q_cuc_lav_alt"], 500)
        self.assertEqual(d["q_freddo_per_posto"], 600)
        self.assertEqual(d["eer_base"], 2.8)
        self.assertEqual(d["eer_alt"], 4.0)
        self.assertEqual(d["f_recupero"], 0.25)
        self.assertEqual(d["cop_pdc"], 3.4)
        self.assertEqual(d["eta_caldaia"], 0.9)
        self.assertEqual(d["sup_tetto_m2"], 800)
        self.assertEqual(d["quota_fv"], 0.5)
        self.assertEqual(d["kwp_per_m2"], 0.18)
        self.assertEqual(d["resa_fv"], 1100)
        self.assertEqual(d["f_autoconsumo"], 0.55)
        self.assertEqual(d["p_el"], 0.28)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["p_immissione"], 0.08)
        self.assertEqual(d["capex"], 420000)
        self.assertEqual(d["f_el"], 0.35)
        self.assertEqual(d["f_gas"], 0.20)
        self.assertEqual(d["wacc"], 5)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 10)

    def test_alias_demo_calcoli(self):
        self.assertEqual(demo_calcoli()["verdetto"],
                         mh857_demo_calcoli()["verdetto"])


class TestCoerenza(unittest.TestCase):
    """Coerenza interna dei bilanci."""

    def test_bilancio_fv(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_pv_auto_kwh_e_anno"]
                             + bc["e_immessa_kwh_e_anno"],
                             bc["e_pv_kwh_e_anno"]))

    def test_deficit_coerente(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_deficit_kwh_e_anno"],
                             max(0.0, bc["e_alt_el_kwh_e_anno"]
                                 - bc["e_pv_auto_kwh_e_anno"])))

    def test_autoconsumo_cappato(self):
        bc = mh857_demo_calcoli()
        self.assertLessEqual(bc["e_pv_auto_kwh_e_anno"],
                             bc["e_alt_el_kwh_e_anno"])
        self.assertLessEqual(bc["e_pv_auto_kwh_e_anno"],
                             bc["e_pv_kwh_e_anno"])

    def test_domanda_base_somma(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_base_el_kwh_e_anno"],
                             bc["e_base_el_senza_freddo_kwh_e_anno"]
                             + bc["e_freddo_base_kwh_e_anno"]))

    def test_domanda_alt_somma(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["e_alt_el_kwh_e_anno"],
                             bc["e_alt_el_parziale_kwh_e_anno"]
                             + bc["e_pdc_kwh_e_anno"]))

    def test_termico_netto_somma(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["q_net_kwh_th_anno"],
                             bc["q_term_alt_kwh_th_anno"]
                             - bc["q_rec_kwh_th_anno"]))

    def test_gas_base_formula(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["gas_base_kwh_anno"],
                             bc["q_term_base_kwh_th_anno"] / 0.9))

    def test_risparmio_differenza(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["risparmio_eur_anno"],
                             bc["c_base_eur_anno"]
                             - bc["c_alt_eur_anno"]))

    def test_co2_evitata_differenza(self):
        bc = mh857_demo_calcoli()
        self.assertTrue(_rel(bc["co2_evitata_t_anno"],
                             bc["co2_base_t_anno"]
                             - bc["co2_alt_t_anno"]))

    def test_flussi(self):
        bc = mh857_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        self.assertEqual(bc["flussi"][0], -420000)
        for f in bc["flussi"][1:]:
            self.assertTrue(_rel(f, bc["risparmio_eur_anno"]))

    def test_van_da_flussi(self):
        bc = mh857_demo_calcoli()
        van = sum(f / 1.05 ** t
                  for t, f in enumerate(bc["flussi"]))
        self.assertTrue(_rel(bc["van"], van))

    def test_tir_annulla_van(self):
        bc = mh857_demo_calcoli()
        r = bc["tir"] / 100.0
        van = sum(f / (1.0 + r) ** t
                  for t, f in enumerate(bc["flussi"]))
        self.assertLess(abs(van), 1e-6 * abs(bc["van"]) + 1e-6)

    def test_payback_cumulato(self):
        bc = mh857_demo_calcoli()
        cum = 0.0
        for k, f in enumerate(bc["flussi"]):
            cum += f
            if k < bc["payback"]:
                self.assertLess(cum, 0.0)
            if k == bc["payback"]:
                self.assertGreaterEqual(cum, 0.0)

    def test_df_flussi(self):
        bc = mh857_demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertAlmostEqual(
            bc["df_flussi"]["Cumulato (EUR)"].iloc[-1],
            -420000 + 20 * bc["risparmio_eur_anno"], places=6)

    def test_df_tabella(self):
        bc = mh857_demo_calcoli()
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)", voci)

    def test_csv(self):
        bc = mh857_demo_calcoli()
        csv = mh857_csv(bc, mh857_demo())
        self.assertIn("risparmio_eur_anno", csv)
        self.assertIn("gas_alt_kwh_anno", csv)
        self.assertIn("CONVIENTE", csv)

    def test_funzioni_pure(self):
        self.assertEqual(mh857_e_el_posto_base(600, 400, 500), 1500.0)
        self.assertEqual(mh857_e_el_posto_alt(350, 250, 350), 950.0)
        self.assertEqual(mh857_e_base_el_senza_freddo(80, 1500), 120000.0)
        self.assertEqual(mh857_e_alt_el_senza_freddo_e_pdc(80, 950), 76000.0)
        self.assertEqual(mh857_q_freddo(80, 600), 48000.0)
        self.assertEqual(mh857_e_freddo(48000.0, 2.8), 17142.857142857145)
        self.assertEqual(mh857_e_freddo(48000.0, 4.0), 12000.0)
        self.assertEqual(mh857_q_term_base(80, 2500, 800, 700), 320000.0)
        self.assertEqual(mh857_q_term_alt(80, 1800, 600, 500), 232000.0)
        self.assertEqual(mh857_q_rec(232000.0, 0.25), 58000.0)
        self.assertEqual(mh857_q_net(232000.0, 58000.0), 174000.0)
        self.assertEqual(mh857_gas_alt(), 0.0)
        self.assertEqual(mh857_e_pdc(174000.0, 3.4), 51176.470588235294)
        self.assertEqual(mh857_p_pv_kwp(800, 0.5, 0.18), 72.0)
        self.assertEqual(mh857_e_pv(72.0, 1100), 79200.0)

    def test_sensibilita(self):
        sens = mh857_sensibilita(**mh857_demo())
        self.assertEqual(set(sens), {"p_el_meno20", "p_el_piu20",
                                     "senza_fv", "senza_recupero",
                                     "capex_doppio", "vita_10",
                                     "wacc_0"})
        self.assertTrue(_rel(sens["senza_fv"]["risparmio_eur_anno"],
                             31430.58823529411))
        self.assertEqual(sens["senza_fv"]["verdetto"], "MARGINALE")
        self.assertTrue(_rel(sens["senza_recupero"]["risparmio_eur_anno"],
                             41702.117647058825))
        self.assertEqual(sens["senza_recupero"]["verdetto"], "CONVIENTE")
        self.assertEqual(sens["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(sens["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(sens["p_el_piu20"]["verdetto"], "CONVIENTE")
        self.assertEqual(sens["wacc_0"]["verdetto"], "CONVIENTE")

    def test_validazione_ok(self):
        d = mh857_demo()
        val = mh857_valida(**d)
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")


class TestGuard(unittest.TestCase):
    """Regime degenere: errori puliti e verdetti."""

    def _demo_con(self, **kw):
        d = mh857_demo()
        d.update(kw)
        return d

    def test_posti_zero(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(posti=0))

    def test_posti_negativi(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(posti=-5))

    def test_per_posto_negativo(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(ill_base=-10))

    def test_freddo_per_posto_negativo(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(q_freddo_per_posto=-10))

    def test_eer_zero(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(eer_base=0))

    def test_eer_alt_negativo(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(eer_alt=-1.0))

    def test_cop_zero(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(cop_pdc=0))

    def test_cop_negativo(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(cop_pdc=-1.0))

    def test_quota_fv_oltre_uno(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(quota_fv=1.5))

    def test_f_recupero_oltre_uno(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(f_recupero=1.2))

    def test_eta_caldaia_oltre_uno(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(eta_caldaia=1.1))

    def test_eta_caldaia_zero(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(eta_caldaia=0))

    def test_tetto_zero(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(sup_tetto_m2=0))

    def test_vita_zero(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(vita=0))

    def test_vita_non_intera(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(vita=2.5))

    def test_prezzo_negativo(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(p_el=-0.1))

    def test_nan(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(p_el=float("nan")))

    def test_infinito(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(capex=float("inf")))

    def test_stringa(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(posti="80"))

    def test_bool(self):
        with self.assertRaises(ValueError):
            mh857_calcola(**self._demo_con(posti=True))

    def test_risparmio_zero_non_calcolabile(self):
        bc = mh857_calcola(**self._demo_con(p_el=0.0, p_gas=0.0,
                                            p_immissione=0.0))
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_risparmio_negativo_non_calcolabile(self):
        # COP bassissimo + niente FV: la pompa di calore
        # assorbe piu' di quanto il gas evitato valga.
        bc = mh857_calcola(**self._demo_con(cop_pdc=0.5,
                                            quota_fv=0))
        self.assertLess(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_verdetto_marginale(self):
        bc = mh857_calcola(**self._demo_con(capex=600000))
        self.assertLess(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_verdetto_non_conviente(self):
        bc = mh857_calcola(**self._demo_con(capex=1000000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_verdetto_funzione(self):
        self.assertEqual(mh857_verdetto(0.0, 100.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh857_verdetto(None, 100.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh857_verdetto(100.0, 50.0, 1000, 10),
                         "CONVIENTE")
        self.assertEqual(mh857_verdetto(100.0, -50.0, 1000, 10),
                         "MARGINALE")
        self.assertEqual(mh857_verdetto(100.0, -500.0, 1000, 10),
                         "NON_CONVIENTE")


class TestLimiti(unittest.TestCase):
    """Casi limite ammessi."""

    def _demo_con(self, **kw):
        d = mh857_demo()
        d.update(kw)
        return d

    def test_quota_fv_zero(self):
        bc = mh857_calcola(**self._demo_con(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        self.assertEqual(bc["e_pv_auto_kwh_e_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_e_anno"], 0.0)
        self.assertTrue(_rel(bc["e_deficit_kwh_e_anno"],
                             bc["e_alt_el_kwh_e_anno"]))
        self.assertEqual(bc["gas_alt_kwh_anno"], 0.0)

    def test_recupero_zero(self):
        bc = mh857_calcola(**self._demo_con(f_recupero=0))
        self.assertEqual(bc["q_rec_kwh_th_anno"], 0.0)
        self.assertEqual(bc["q_net_kwh_th_anno"],
                         bc["q_term_alt_kwh_th_anno"])

    def test_recupero_totale(self):
        bc = mh857_calcola(**self._demo_con(f_recupero=1.0))
        self.assertEqual(bc["q_net_kwh_th_anno"], 0.0)
        self.assertEqual(bc["e_pdc_kwh_e_anno"], 0.0)

    def test_autoconsumo_cappato_a_domanda(self):
        bc = mh857_calcola(**self._demo_con(quota_fv=1.0,
                                            sup_tetto_m2=5000,
                                            f_autoconsumo=1.0))
        self.assertTrue(_rel(bc["e_pv_auto_kwh_e_anno"],
                             bc["e_alt_el_kwh_e_anno"]))
        self.assertEqual(bc["e_deficit_kwh_e_anno"], 0.0)

    def test_tir_none_senza_cambio_segno(self):
        # Flussi tutti negativi: nessun cambio di segno.
        bc = mh857_calcola(**self._demo_con(cop_pdc=0.5,
                                            quota_fv=0))
        self.assertLess(bc["risparmio_eur_anno"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])

    def test_p_el_pareggio_none_denominatore(self):
        p = mh857_p_el_pareggio(1000.0, 0.09, 0.0, 0.08,
                                5000.0, 6000.0)
        self.assertIsNone(p)

    def test_van_wacc_zero(self):
        flussi = mh857_flussi(420000, 46478.58823529411, 20)
        self.assertTrue(_rel(mh857_van(flussi, 0),
                             sum(flussi)))

    def test_payback_mai(self):
        self.assertIsNone(mh857_payback([-100, -10, -10]))

    def test_payback_zero_immediato(self):
        self.assertEqual(mh857_payback([0, 10]), 0)


class TestStruttura(unittest.TestCase):
    """Struttura dei file consegnati."""

    def test_helpers_parse(self):
        with open(_HELPERS_PATH, encoding="utf-8") as f:
            src = f.read()
        ast.parse(src)
        self.assertNotIn(_IMP_STREAMLIT, src)
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_TAB, src)
        self.assertNotIn(_VECCHIO_ST, src)

    def test_ui_parse_e_indentazione(self):
        import textwrap
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        # Frammento innestato dentro "with tab857:":
        # il parse standalone richiede il dedent.
        ast.parse(textwrap.dedent(src))
        for ln in src.splitlines():
            if ln.strip():
                self.assertTrue(ln.startswith("    "),
                                f"riga non indentata di 4: {ln[:60]}")
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_TAB, src)
        self.assertNotIn(_VECCHIO_ST, src)
        self.assertIn("tab857", src)

    def test_ui_chiavi_demo(self):
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        chiavi_ui = set(re.findall(r'_def857\["([^"]+)"\]', src))
        chiavi_demo = set(mh857_demo())
        self.assertTrue(chiavi_ui, "nessuna chiave _def857 in UI")
        self.assertTrue(chiavi_ui <= chiavi_demo,
                        f"chiavi UI non in demo: {chiavi_ui - chiavi_demo}")

    def test_ui_chiavi_bc(self):
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        chiavi_ui = set(re.findall(r"_bc857\['([^']+)'\]", src))
        chiavi_bc = set(mh857_demo_calcoli())
        self.assertTrue(chiavi_ui, "nessuna chiave _bc857 in UI")
        self.assertTrue(chiavi_ui <= chiavi_bc,
                        f"chiavi UI non in calcola: {chiavi_ui - chiavi_bc}")

    def test_ui_chiavi_st857_uniche(self):
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        chiavi = re.findall(r'key="(st857_[^"]+)"', src)
        self.assertTrue(chiavi, "nessuna chiave st857 in UI")
        self.assertEqual(len(chiavi), len(set(chiavi)),
                         f"chiavi st857 duplicate: {chiavi}")
        for k in chiavi:
            self.assertTrue(k.startswith("st857_"))

    def test_nessun_import_streamlit_negli_helper(self):
        with open(_HELPERS_PATH, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("streamlit", src)


if __name__ == "__main__":
    unittest.main()
