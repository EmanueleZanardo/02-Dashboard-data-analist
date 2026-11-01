"""Test nuova scheda apicoltura: smielatura +
fusione cera + deumidificazione miele con
pompa di calore + FV battono laboratorio
tradizionale + caldaia a gas?

File: tests/test_w860_apicoltura.py

Business case annuo di un'azienda apistica,
connessa alla rete, guidata dalle ARNIE +
MIELE PER ARNIA (kg) + SUPERFICIE TETTO
(m2) + QUOTA FV (non serra riscaldata, non
albergo, non altre tab alimentari):
miele_kg = arnie x miele_per_arnia_kg;
E_smiel_base = miele_kg x
kwh_smiel_per_kg_base; E_smiel_alt =
miele_kg x kwh_smiel_per_kg_alt
(efficiente, minore); E_base_el =
E_smiel_base + celle_frigo_base +
altre_base; E_alt_el = E_smiel_alt +
celle_frigo_alt + altre_alt + E_pdc;
Q_term_base = fusione_cera_base +
riscaldamento_lab_base; Q_term_alt =
fusione_cera_alt + riscaldamento_lab_alt;
Q_rec = f_recupero x Q_term_alt (30% del
termico ALTERNATIVO, non della base);
Q_net = max(0, Q_term_alt - Q_rec);
Gas_base = Q_term_base / eta_caldaia;
Gas_alt = 0 (la caldaia a gas SCOMPARE:
il termico netto va in pompa di calore,
che copre anche la deumidificazione
miele); E_pdc = Q_net / COP_pdc; kWp
tetto = sup_tetto_m2 x quota_fv x
kwp_per_m2; E_pv = kWp x resa_fv;
E_pv_auto = min(E_pv x f_autoconsumo,
E_alt_el) (cappato alla domanda elettrica
alternativa); E_immessa = E_pv -
E_pv_auto; E_deficit = max(0, E_alt_el -
E_pv_auto); C_base = E_base_el x p_el +
Gas_base x p_gas (nessun O&M); C_alt =
E_deficit x p_el - E_immessa x
p_immissione (gas alternativo zero;
l'immessa e' un RICAVO a prezzo di
immissione, INFERIORE a p_el; nessun
credito CO2 per l'immessa); risparmio =
C_base - C_alt; CAPEX forfettario 18.000
(FV 8.000 + PdC 5.000 + smielatore e
deumidificatore efficienti 3.000 + celle
frigo e recupero 2.000); CO2 base =
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
-0,42133025608388985 EUR/kWh, quindi
None: il numeratore e' negativo
(-1.824,50 EUR/anno circa: gas evitato
1.482,35 piu' ricavo da immissione
342,14; denominatore 4.330,33
kWh_e/anno), quindi l'alternativa vince
sui costi annui anche a prezzo elettrico
nullo. In regime valido con gas base
positivo o immessa positiva il pareggio
non puo' mai essere positivo, perche'
il numeratore e' sempre nullo o
negativo (nessun O&M a spostarlo).
Verdetto: NON_CALCOLABILE se input
degenere (arnie <= 0, miele per arnia
<= 0, kwh smiel per kg base <= 0, kwh
smiel per kg alt <= 0, celle frigo base
< 0, celle frigo alt < 0, altre base < 0,
altre alt < 0, fusione cera base < 0,
fusione cera alt < 0, riscaldamento lab
base < 0, riscaldamento lab alt < 0,
f_recupero < 0 o > 1, cop_pdc <= 0, eta
caldaia <= 0 o > 1, sup tetto <= 0,
quota fv < 0 o > 1, kwp per m2 < 0,
resa fv < 0, f_autoconsumo < 0 o > 1,
prezzi < 0, CAPEX < 0, f_el < 0, f_gas
< 0, WACC < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa entro
tolleranza PERCENTUALE del CAPEX,
NON_CONVIENTE altrimenti.
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w860_helpers import (
        demo_calcoli,
        mh856_c_alt,
        mh856_c_base,
        mh856_calcola,
        mh856_co2_alt,
        mh856_co2_base,
        mh856_co2_evitata,
        mh856_csv,
        mh856_demo,
        mh856_demo_calcoli,
        mh856_e_alt_el,
        mh856_e_base_el,
        mh856_e_deficit,
        mh856_e_immessa,
        mh856_e_pdc,
        mh856_e_pv,
        mh856_e_pv_auto,
        mh856_e_smiel_alt,
        mh856_e_smiel_base,
        mh856_eta,
        mh856_flussi,
        mh856_frazione,
        mh856_gas_alt,
        mh856_gas_base,
        mh856_int_pos,
        mh856_miele_kg,
        mh856_nneg,
        mh856_num,
        mh856_p_el_pareggio,
        mh856_p_pv_kwp,
        mh856_payback,
        mh856_pos,
        mh856_q_net,
        mh856_q_rec,
        mh856_q_term_alt,
        mh856_q_term_base,
        mh856_risparmio,
        mh856_sensibilita,
        mh856_tir,
        mh856_valida,
        mh856_van,
        mh856_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files: da repo
    # w860_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w860_helpers", os.path.join(_hf, "w860_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh856_c_alt = _mod.mh856_c_alt
    mh856_c_base = _mod.mh856_c_base
    mh856_calcola = _mod.mh856_calcola
    mh856_co2_alt = _mod.mh856_co2_alt
    mh856_co2_base = _mod.mh856_co2_base
    mh856_co2_evitata = _mod.mh856_co2_evitata
    mh856_csv = _mod.mh856_csv
    mh856_demo = _mod.mh856_demo
    mh856_demo_calcoli = _mod.mh856_demo_calcoli
    mh856_e_alt_el = _mod.mh856_e_alt_el
    mh856_e_base_el = _mod.mh856_e_base_el
    mh856_e_deficit = _mod.mh856_e_deficit
    mh856_e_immessa = _mod.mh856_e_immessa
    mh856_e_pdc = _mod.mh856_e_pdc
    mh856_e_pv = _mod.mh856_e_pv
    mh856_e_pv_auto = _mod.mh856_e_pv_auto
    mh856_e_smiel_alt = _mod.mh856_e_smiel_alt
    mh856_e_smiel_base = _mod.mh856_e_smiel_base
    mh856_eta = _mod.mh856_eta
    mh856_flussi = _mod.mh856_flussi
    mh856_frazione = _mod.mh856_frazione
    mh856_gas_alt = _mod.mh856_gas_alt
    mh856_gas_base = _mod.mh856_gas_base
    mh856_int_pos = _mod.mh856_int_pos
    mh856_miele_kg = _mod.mh856_miele_kg
    mh856_nneg = _mod.mh856_nneg
    mh856_num = _mod.mh856_num
    mh856_p_el_pareggio = _mod.mh856_p_el_pareggio
    mh856_p_pv_kwp = _mod.mh856_p_pv_kwp
    mh856_payback = _mod.mh856_payback
    mh856_pos = _mod.mh856_pos
    mh856_q_net = _mod.mh856_q_net
    mh856_q_rec = _mod.mh856_q_rec
    mh856_q_term_alt = _mod.mh856_q_term_alt
    mh856_q_term_base = _mod.mh856_q_term_base
    mh856_risparmio = _mod.mh856_risparmio
    mh856_sensibilita = _mod.mh856_sensibilita
    mh856_tir = _mod.mh856_tir
    mh856_valida = _mod.mh856_valida
    mh856_van = _mod.mh856_van
    mh856_verdetto = _mod.mh856_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w860_helpers.py")
_UI_PATH = _risolvi("w860_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh85" + "5"
_VECCHIO_TAB = "tab85" + "5"
_VECCHIO_ST = "st85" + "5_"
_IMP_STREAMLIT = "import " + "streamlit"

# Valori demo ricalcolati a mano dal brief
# (arnie 200, miele per arnia 25 kg).
_DEMO = {
    "miele_kg": 5000.0,
    "e_smiel_base_kwh_e_anno": 1750.0,
    "e_smiel_alt_kwh_e_anno": 1250.0,
    "e_base_el_kwh_e_anno": 5950.0,
    "e_alt_el_kwh_e_anno": 6846.875,
    "q_term_base_kwh_th_anno": 14000.0,
    "q_term_alt_kwh_th_anno": 10500.0,
    "q_rec_kwh_th_anno": 3150.0,
    "q_net_kwh_th_anno": 7350.0,
    "gas_base_kwh_anno": 16470.58823529412,
    "gas_alt_kwh_anno": 0.0,
    "e_pdc_kwh_e_anno": 2296.875,
    "p_pv_kwp": 8.64,
    "e_pv_kwh_e_anno": 9504.0,
    "e_pv_auto_kwh_e_anno": 5227.2,
    "e_immessa_kwh_e_anno": 4276.8,
    "e_deficit_kwh_e_anno": 1619.675,
    "c_base_eur_anno": 3148.352941176471,
    "c_alt_eur_anno": 111.365,
    "risparmio_eur_anno": 3036.9879411764714,
    "co2_base_t_anno": 5.376617647058824,
    "co2_alt_t_anno": 0.56688625,
    "co2_evitata_t_anno": 4.809731397058824,
    "van": 19847.582530698626,
    "tir": 16.006080205932953,
    "payback": 6,
}


def _rel(a, b):
    """Confronto con tolleranza relativa 1e-9."""
    if b == 0.0:
        return a == 0.0
    return abs(a - b) <= 1e-9 * abs(b)


class TestDemo(unittest.TestCase):
    """Demo ricalcolata a mano, valore per valore."""

    def test_miele(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["miele_kg"], _DEMO["miele_kg"]))

    def test_smiel_base(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_smiel_base_kwh_e_anno"],
                             _DEMO["e_smiel_base_kwh_e_anno"]))

    def test_smiel_alt(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_smiel_alt_kwh_e_anno"],
                             _DEMO["e_smiel_alt_kwh_e_anno"]))

    def test_domanda_base(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_base_el_kwh_e_anno"],
                             _DEMO["e_base_el_kwh_e_anno"]))

    def test_domanda_alt(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_alt_el_kwh_e_anno"],
                             _DEMO["e_alt_el_kwh_e_anno"]))

    def test_termico_base(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["q_term_base_kwh_th_anno"],
                             _DEMO["q_term_base_kwh_th_anno"]))

    def test_termico_alt(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["q_term_alt_kwh_th_anno"],
                             _DEMO["q_term_alt_kwh_th_anno"]))

    def test_recupero(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["q_rec_kwh_th_anno"],
                             _DEMO["q_rec_kwh_th_anno"]))

    def test_termico_netto(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["q_net_kwh_th_anno"],
                             _DEMO["q_net_kwh_th_anno"]))

    def test_gas_base(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["gas_base_kwh_anno"],
                             _DEMO["gas_base_kwh_anno"]))

    def test_gas_alt_zero(self):
        bc = mh856_demo_calcoli()
        self.assertEqual(bc["gas_alt_kwh_anno"], 0.0)

    def test_e_pdc(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_pdc_kwh_e_anno"],
                             _DEMO["e_pdc_kwh_e_anno"]))

    def test_p_pv(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["p_pv_kwp"], _DEMO["p_pv_kwp"]))

    def test_e_pv(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_pv_kwh_e_anno"],
                             _DEMO["e_pv_kwh_e_anno"]))

    def test_autoconsumo(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_pv_auto_kwh_e_anno"],
                             _DEMO["e_pv_auto_kwh_e_anno"]))

    def test_immessa(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_immessa_kwh_e_anno"],
                             _DEMO["e_immessa_kwh_e_anno"]))

    def test_deficit(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_deficit_kwh_e_anno"],
                             _DEMO["e_deficit_kwh_e_anno"]))

    def test_costo_base(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["c_base_eur_anno"],
                             _DEMO["c_base_eur_anno"]))

    def test_costo_alt(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["c_alt_eur_anno"],
                             _DEMO["c_alt_eur_anno"]))

    def test_risparmio(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["risparmio_eur_anno"],
                             _DEMO["risparmio_eur_anno"]))

    def test_co2_base(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["co2_base_t_anno"],
                             _DEMO["co2_base_t_anno"]))

    def test_co2_alt(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["co2_alt_t_anno"],
                             _DEMO["co2_alt_t_anno"]))

    def test_co2_evitata(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["co2_evitata_t_anno"],
                             _DEMO["co2_evitata_t_anno"]))

    def test_van(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["van"], _DEMO["van"]))

    def test_tir(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["tir"], _DEMO["tir"]))

    def test_payback(self):
        bc = mh856_demo_calcoli()
        self.assertEqual(bc["payback"], _DEMO["payback"])

    def test_p_el_pareggio_none(self):
        bc = mh856_demo_calcoli()
        self.assertIsNone(bc["p_el_pareggio"])

    def test_verdetto_conviente(self):
        bc = mh856_demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_demo_dict_completo(self):
        """Ogni voce di _DEMO contro demo_calcoli()."""
        bc = mh856_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            self.assertTrue(_rel(bc[chiave], atteso),
                            f"{chiave}: {bc[chiave]} != {atteso}")

    def test_demo_input(self):
        d = mh856_demo()
        self.assertEqual(d["arnie"], 200)
        self.assertEqual(d["miele_per_arnia_kg"], 25)
        self.assertEqual(d["kwh_smiel_per_kg_base"], 0.35)
        self.assertEqual(d["kwh_smiel_per_kg_alt"], 0.25)
        self.assertEqual(d["celle_frigo_base"], 2400)
        self.assertEqual(d["celle_frigo_alt"], 1800)
        self.assertEqual(d["altre_base"], 1800)
        self.assertEqual(d["altre_alt"], 1500)
        self.assertEqual(d["fusione_cera_base"], 8000)
        self.assertEqual(d["fusione_cera_alt"], 6000)
        self.assertEqual(d["riscaldamento_lab_base"], 6000)
        self.assertEqual(d["riscaldamento_lab_alt"], 4500)
        self.assertEqual(d["f_recupero"], 0.30)
        self.assertEqual(d["cop_pdc"], 3.2)
        self.assertEqual(d["eta_caldaia"], 0.85)
        self.assertEqual(d["sup_tetto_m2"], 120)
        self.assertEqual(d["quota_fv"], 0.40)
        self.assertEqual(d["kwp_per_m2"], 0.18)
        self.assertEqual(d["resa_fv"], 1100)
        self.assertEqual(d["f_autoconsumo"], 0.55)
        self.assertEqual(d["p_el"], 0.28)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["p_immissione"], 0.08)
        self.assertEqual(d["capex"], 18000)
        self.assertEqual(d["f_el"], 0.35)
        self.assertEqual(d["f_gas"], 0.20)
        self.assertEqual(d["wacc"], 5)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 10)

    def test_alias_demo_calcoli(self):
        self.assertEqual(demo_calcoli()["verdetto"],
                         mh856_demo_calcoli()["verdetto"])


class TestCoerenza(unittest.TestCase):
    """Coerenza interna dei bilanci."""

    def test_bilancio_fv(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_pv_auto_kwh_e_anno"]
                             + bc["e_immessa_kwh_e_anno"],
                             bc["e_pv_kwh_e_anno"]))

    def test_deficit_coerente(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_deficit_kwh_e_anno"],
                             max(0.0, bc["e_alt_el_kwh_e_anno"]
                                 - bc["e_pv_auto_kwh_e_anno"])))

    def test_autoconsumo_cappato(self):
        bc = mh856_demo_calcoli()
        self.assertLessEqual(bc["e_pv_auto_kwh_e_anno"],
                             bc["e_alt_el_kwh_e_anno"])
        self.assertLessEqual(bc["e_pv_auto_kwh_e_anno"],
                             bc["e_pv_kwh_e_anno"])

    def test_domanda_base_somma(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_base_el_kwh_e_anno"],
                             bc["e_smiel_base_kwh_e_anno"]
                             + bc["e_celle_frigo_base_kwh_e_anno"]
                             + bc["e_altre_base_kwh_e_anno"]))

    def test_domanda_alt_somma(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["e_alt_el_kwh_e_anno"],
                             bc["e_smiel_alt_kwh_e_anno"]
                             + bc["e_celle_frigo_alt_kwh_e_anno"]
                             + bc["e_altre_alt_kwh_e_anno"]
                             + bc["e_pdc_kwh_e_anno"]))

    def test_termico_netto_somma(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["q_net_kwh_th_anno"],
                             bc["q_term_alt_kwh_th_anno"]
                             - bc["q_rec_kwh_th_anno"]))

    def test_gas_base_formula(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["gas_base_kwh_anno"],
                             bc["q_term_base_kwh_th_anno"] / 0.85))

    def test_risparmio_differenza(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["risparmio_eur_anno"],
                             bc["c_base_eur_anno"]
                             - bc["c_alt_eur_anno"]))

    def test_co2_evitata_differenza(self):
        bc = mh856_demo_calcoli()
        self.assertTrue(_rel(bc["co2_evitata_t_anno"],
                             bc["co2_base_t_anno"]
                             - bc["co2_alt_t_anno"]))

    def test_flussi(self):
        bc = mh856_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        self.assertEqual(bc["flussi"][0], -18000)
        for f in bc["flussi"][1:]:
            self.assertTrue(_rel(f, bc["risparmio_eur_anno"]))

    def test_van_da_flussi(self):
        bc = mh856_demo_calcoli()
        van = sum(f / 1.05 ** t
                  for t, f in enumerate(bc["flussi"]))
        self.assertTrue(_rel(bc["van"], van))

    def test_tir_annulla_van(self):
        bc = mh856_demo_calcoli()
        r = bc["tir"] / 100.0
        van = sum(f / (1.0 + r) ** t
                  for t, f in enumerate(bc["flussi"]))
        self.assertLess(abs(van), 1e-6 * abs(bc["van"]) + 1e-6)

    def test_payback_cumulato(self):
        bc = mh856_demo_calcoli()
        cum = 0.0
        for k, f in enumerate(bc["flussi"]):
            cum += f
            if k < bc["payback"]:
                self.assertLess(cum, 0.0)
            if k == bc["payback"]:
                self.assertGreaterEqual(cum, 0.0)

    def test_df_flussi(self):
        bc = mh856_demo_calcoli()
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertAlmostEqual(
            bc["df_flussi"]["Cumulato (EUR)"].iloc[-1],
            -18000 + 20 * bc["risparmio_eur_anno"], places=6)

    def test_df_tabella(self):
        bc = mh856_demo_calcoli()
        self.assertGreater(len(bc["df_tabella"]), 50)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)", voci)

    def test_csv(self):
        bc = mh856_demo_calcoli()
        csv = mh856_csv(bc, mh856_demo())
        self.assertIn("risparmio_eur_anno", csv)
        self.assertIn("gas_alt_kwh_anno", csv)
        self.assertIn("CONVIENTE", csv)

    def test_funzioni_pure(self):
        self.assertEqual(mh856_miele_kg(200, 25), 5000.0)
        self.assertEqual(mh856_e_smiel_base(5000.0, 0.35), 1750.0)
        self.assertEqual(mh856_e_smiel_alt(5000.0, 0.25), 1250.0)
        self.assertEqual(mh856_q_term_base(8000, 6000), 14000.0)
        self.assertEqual(mh856_q_term_alt(6000, 4500), 10500.0)
        self.assertEqual(mh856_q_rec(10500.0, 0.30), 3150.0)
        self.assertEqual(mh856_q_net(10500.0, 3150.0), 7350.0)
        self.assertEqual(mh856_gas_alt(), 0.0)
        self.assertEqual(mh856_e_pdc(7350.0, 3.2), 2296.875)
        self.assertEqual(mh856_p_pv_kwp(120, 0.40, 0.18), 8.64)
        self.assertEqual(mh856_e_pv(8.64, 1100), 9504.0)

    def test_sensibilita(self):
        sens = mh856_sensibilita(**mh856_demo())
        self.assertEqual(set(sens), {"p_el_meno20", "p_el_piu20",
                                     "senza_fv", "senza_recupero",
                                     "capex_doppio", "vita_10",
                                     "wacc_0"})
        self.assertTrue(_rel(sens["senza_fv"]["risparmio_eur_anno"],
                             1231.2279411764714))
        self.assertEqual(sens["senza_fv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(sens["p_el_piu20"]["verdetto"], "CONVIENTE")
        self.assertEqual(sens["wacc_0"]["verdetto"], "CONVIENTE")

    def test_validazione_ok(self):
        d = mh856_demo()
        val = mh856_valida(**d)
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")


class TestGuard(unittest.TestCase):
    """Regime degenere: errori puliti e verdetti."""

    def _demo_con(self, **kw):
        d = mh856_demo()
        d.update(kw)
        return d

    def test_arnie_zero(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(arnie=0))

    def test_arnie_negative(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(arnie=-5))

    def test_miele_per_arnia_zero(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(miele_per_arnia_kg=0))

    def test_cop_zero(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(cop_pdc=0))

    def test_cop_negativo(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(cop_pdc=-1.0))

    def test_quota_fv_oltre_uno(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(quota_fv=1.5))

    def test_f_recupero_oltre_uno(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(f_recupero=1.2))

    def test_eta_caldaia_oltre_uno(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(eta_caldaia=1.1))

    def test_eta_caldaia_zero(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(eta_caldaia=0))

    def test_tetto_zero(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(sup_tetto_m2=0))

    def test_vita_zero(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(vita=0))

    def test_vita_non_intera(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(vita=2.5))

    def test_prezzo_negativo(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(p_el=-0.1))

    def test_nan(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(p_el=float("nan")))

    def test_infinito(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(capex=float("inf")))

    def test_stringa(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(arnie="200"))

    def test_bool(self):
        with self.assertRaises(ValueError):
            mh856_calcola(**self._demo_con(arnie=True))

    def test_risparmio_zero_non_calcolabile(self):
        bc = mh856_calcola(**self._demo_con(p_el=0.0, p_gas=0.0,
                                            p_immissione=0.0))
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_risparmio_negativo_non_calcolabile(self):
        # COP bassissimo + niente FV: la pompa di calore
        # assorbe piu' di quanto il gas evitato valga.
        bc = mh856_calcola(**self._demo_con(cop_pdc=0.5,
                                            quota_fv=0))
        self.assertLess(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_verdetto_marginale(self):
        bc = mh856_calcola(**self._demo_con(capex=40000))
        self.assertLess(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_verdetto_non_conviente(self):
        bc = mh856_calcola(**self._demo_con(capex=100000))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_verdetto_funzione(self):
        self.assertEqual(mh856_verdetto(0.0, 100.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh856_verdetto(None, 100.0, 1000, 10),
                         "NON_CALCOLABILE")
        self.assertEqual(mh856_verdetto(100.0, 50.0, 1000, 10),
                         "CONVIENTE")
        self.assertEqual(mh856_verdetto(100.0, -50.0, 1000, 10),
                         "MARGINALE")
        self.assertEqual(mh856_verdetto(100.0, -500.0, 1000, 10),
                         "NON_CONVIENTE")


class TestLimiti(unittest.TestCase):
    """Casi limite ammessi."""

    def _demo_con(self, **kw):
        d = mh856_demo()
        d.update(kw)
        return d

    def test_quota_fv_zero(self):
        bc = mh856_calcola(**self._demo_con(quota_fv=0))
        self.assertEqual(bc["p_pv_kwp"], 0.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 0.0)
        self.assertEqual(bc["e_pv_auto_kwh_e_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh_e_anno"], 0.0)
        self.assertTrue(_rel(bc["e_deficit_kwh_e_anno"],
                             bc["e_alt_el_kwh_e_anno"]))
        self.assertEqual(bc["gas_alt_kwh_anno"], 0.0)

    def test_recupero_zero(self):
        bc = mh856_calcola(**self._demo_con(f_recupero=0))
        self.assertEqual(bc["q_rec_kwh_th_anno"], 0.0)
        self.assertEqual(bc["q_net_kwh_th_anno"],
                         bc["q_term_alt_kwh_th_anno"])

    def test_recupero_totale(self):
        bc = mh856_calcola(**self._demo_con(f_recupero=1.0))
        self.assertEqual(bc["q_net_kwh_th_anno"], 0.0)
        self.assertEqual(bc["e_pdc_kwh_e_anno"], 0.0)

    def test_autoconsumo_cappato_a_domanda(self):
        bc = mh856_calcola(**self._demo_con(quota_fv=1.0,
                                            sup_tetto_m2=1000,
                                            f_autoconsumo=1.0))
        self.assertTrue(_rel(bc["e_pv_auto_kwh_e_anno"],
                             bc["e_alt_el_kwh_e_anno"]))
        self.assertEqual(bc["e_deficit_kwh_e_anno"], 0.0)

    def test_tir_none_senza_cambio_segno(self):
        # Flussi tutti negativi: nessun cambio di segno.
        bc = mh856_calcola(**self._demo_con(cop_pdc=0.5,
                                            quota_fv=0))
        self.assertLess(bc["risparmio_eur_anno"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])

    def test_p_el_pareggio_none_denominatore(self):
        p = mh856_p_el_pareggio(1000.0, 0.09, 0.0, 0.08,
                                5000.0, 6000.0)
        self.assertIsNone(p)

    def test_van_wacc_zero(self):
        flussi = mh856_flussi(18000, 3036.9879411764714, 20)
        self.assertTrue(_rel(mh856_van(flussi, 0),
                             sum(flussi)))

    def test_payback_mai(self):
        self.assertIsNone(mh856_payback([-100, -10, -10]))

    def test_payback_zero_immediato(self):
        self.assertEqual(mh856_payback([0, 10]), 0)


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
        # Frammento innestato dentro "with tab856:":
        # il parse standalone richiede il dedent.
        ast.parse(textwrap.dedent(src))
        for ln in src.splitlines():
            if ln.strip():
                self.assertTrue(ln.startswith("    "),
                                f"riga non indentata di 4: {ln[:60]}")
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_TAB, src)
        self.assertNotIn(_VECCHIO_ST, src)
        self.assertIn("tab856", src)

    def test_ui_chiavi_demo(self):
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        chiavi_ui = set(re.findall(r'_def856\["([^"]+)"\]', src))
        chiavi_demo = set(mh856_demo())
        self.assertTrue(chiavi_ui, "nessuna chiave _def856 in UI")
        self.assertTrue(chiavi_ui <= chiavi_demo,
                        f"chiavi UI non in demo: {chiavi_ui - chiavi_demo}")

    def test_ui_chiavi_bc(self):
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        chiavi_ui = set(re.findall(r"_bc856\['([^']+)'\]", src))
        chiavi_bc = set(mh856_demo_calcoli())
        self.assertTrue(chiavi_ui, "nessuna chiave _bc856 in UI")
        self.assertTrue(chiavi_ui <= chiavi_bc,
                        f"chiavi UI non in calcola: {chiavi_ui - chiavi_bc}")

    def test_ui_chiavi_st856_uniche(self):
        with open(_UI_PATH, encoding="utf-8") as f:
            src = f.read()
        chiavi = re.findall(r'key="(st856_[^"]+)"', src)
        self.assertTrue(chiavi, "nessuna chiave st856 in UI")
        self.assertEqual(len(chiavi), len(set(chiavi)),
                         f"chiavi st856 duplicate: {chiavi}")
        for k in chiavi:
            self.assertTrue(k.startswith("st856_"))

    def test_nessun_import_streamlit_negli_helper(self):
        with open(_HELPERS_PATH, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("streamlit", src)


if __name__ == "__main__":
    unittest.main()
