"""Test nuova scheda tab838 "Terme:
pompa di calore + recupero calore
acque termali reflue + fotovoltaico
battono caldaia a gas per vasche,
ACS e ambienti?".

Business case deterministico di uno
stabilimento termale guidato dalla
SUPERFICIE VASCHE in m2:
Q_vasche = sup_vasche x q_spec_vasche;
Q_base = Q_vasche + Q_acs + Q_amb;
Q_recupero = quota_recupero x Q_vasche
(acque termali reflue di scarico vasche);
Q_netto = Q_base - Q_recupero;
E_pdc = Q_netto / COP; E_pv = kWp x
producibilita'; autoconsumo = min(E_pv x
quota_autoconsumo, E_pdc) (cappato:
E_rete non scende sotto zero); E_rete =
E_pdc - autoconsumo; E_esportata = E_pv -
autoconsumo (NESSUN credito di costo ne'
di CO2: scelta conservativa); Q_gas =
Q_base / eta_caldaia; C_base = Q_gas x
p_gas + E_aux_base x p_el; C_alt =
E_rete x p_el + O&M_alt; risparmio =
C_base - C_alt; CO2 base = Q_gas x
f_co2_gas / 1000 + E_aux_base x f_co2_el
/ 1000; CO2 alt = E_rete x f_co2_el /
1000; CO2 evitata = base - alt (segno
libero, non clampata: puo' essere
negativa se E_rete supera gli ausiliari
base in modo da superare la base);
flussi [-CAPEX, risparmio x vita]; VAN al
WACC (FRAZIONE, non percentuale); TIR per
bisezione; payback (primo anno con
cumulato >= 0); COP_min = Q_netto /
((C_base - O&M_alt) / p_el +
autoconsumo_saturo) nel ramo autoconsumo
saturo, None se p_el <= 0, Q_netto <= 0,
COP_min < 0, o ramo incoerente
(Q_netto / COP_min < autoconsumo_saturo),
SOGLIA MINIMA quando esiste (sopra di
essa l'alternativa vince sui costi, sotto
perde; e' dominata ANCHE dal costo base
e dall'O&M, non solo dall'elettricita'
della pompa di calore). Per p_el NON
viene dichiarato alcun pareggio: il
pareggio dichiarato qui e' SOLO COP_min.
Verdetto: NON_CALCOLABILE se input
degenere (sup_vasche <= 0, fabbisogni
< 0, quote < 0 o > 1, eta_caldaia <= 0 o
> 1, ausiliari < 0, prezzi < 0, COP <= 0,
O&M_alt < 0, kWp < 0, producibilita' < 0,
CAPEX < 0, fattori CO2 < 0, WACC < 0,
vita <= 0, tolleranza < 0) o se risparmio
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
previsto (sup_vasche, vita, COP,
eta_caldaia). Gli zeri ammessi in
entrambi (fabbisogni, quote, ausiliari,
prezzi, O&M_alt, kWp, producibilita',
CAPEX, fattori CO2, WACC, tolleranza) non
creano divergenza. Quote > 1 e eta > 1
sono degeneri in entrambi ma non
raggiungibili via slider (tetto 1,0).
WACC sopra 0,20 e tolleranza sopra 1,0
sono ammessi negli helper e limitati solo
dagli slider UI (0,20 e 1,0): nessuna
divergenza nel range raggiungibile,
perche' la guard controlla solo gli
stessi limiti degli helper. Distinzione
esplicita: distinto dalla piscina
coperta riscaldata esistente (solo
riscaldamento vasca: qui stabilimento
termale completo, vasche + ACS + ambienti
+ recupero da acque reflue termali),
dall'albergo (pernottamento e
ristorazione: qui vasche termali e acque
reflue) e dall'ospedale (degenze e
sterilizzazione: qui vasche termali e
acque reflue): qui driver SUPERFICIE
VASCHE + RECUPERO CALORE ACQUE TERMALI
REFLUE + POMPA DI CALORE + FOTOVOLTAICO
IN COPERTURA.

Demo (terme): 500 m2 di vasche a 1.200
kWh_th/m2/anno (Q_vasche 600.000,00
kWh_th/anno), ACS 150.000,00, ambienti
200.000,00 (Q_base 950.000,00
kWh_th/anno), quota recupero 0,30
(Q_recupero 180.000,00, Q_netto
770.000,00 kWh_th/anno), rendimento
caldaia 0,90 (Q_gas 1.055.555,56
kWh/anno), ausiliari base 40.000,00
kWh_e/anno, prezzo elettricita' 0,22
EUR/kWh, prezzo gas 0,09 EUR/kWh, COP
3,2 (E_pdc 240.625,00 kWh_e/anno),
O&M alternativo 20.000 EUR/anno,
fotovoltaico 80 kWp a 1.100
kWh/kWp/anno (88.000,00 kWh_e/anno,
autoconsumo 61.600,00, esportato
26.400,00 senza credito), energia di
rete alternativa 179.025,00 kWh_e/anno,
CAPEX 500.000 EUR, fattore CO2
elettricita' 0,25 kg/kWh, fattore CO2
gas 0,20 kg/kWh, WACC 0,05 (frazione),
vita 20 anni, tolleranza 0,10 (frazione
del CAPEX). Valori calcolati eseguendo
mh838_demo_calcoli(): Q_vasche 600.000,00,
Q_base 950.000,00, Q_recupero 180.000,00,
Q_netto 770.000,00, E_pdc 240.625,00,
E_pv 88.000,00, autoconsumo 61.600,00,
E_rete 179.025,00, esportata 26.400,00,
Q_gas 1055555,5555555555, C_base
103.800,00, C_alt 59.385,50, risparmio
44.414,50, CO2_base 221,11, CO2_alt
44,76, CO2_evitata 176,35, VAN
53502,841258741784, TIR 6,2313385335571025 %,
payback 12, COP_min
1,7400772454597753, verdetto CONVIENTE.

Destinazione nel repo: tests/test_w838_terme.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w841_helpers import (
        demo_calcoli,
        mh838_autoconsumo,
        mh838_c_alt,
        mh838_c_base,
        mh838_calcola,
        mh838_co2_alt,
        mh838_co2_base,
        mh838_co2_evitata,
        mh838_cop_min,
        mh838_csv,
        mh838_demo,
        mh838_demo_calcoli,
        mh838_e_esportata,
        mh838_e_pdc,
        mh838_e_pv,
        mh838_e_rete,
        mh838_eta,
        mh838_flussi,
        mh838_frazione,
        mh838_int_pos,
        mh838_nneg,
        mh838_num,
        mh838_payback,
        mh838_pos,
        mh838_q_base,
        mh838_q_gas,
        mh838_q_netto,
        mh838_q_recupero,
        mh838_q_vasche,
        mh838_risparmio,
        mh838_sensibilita,
        mh838_tir,
        mh838_valida,
        mh838_van,
        mh838_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w841_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w841_helpers", os.path.join(_hf, "w841_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh838_autoconsumo = _mod.mh838_autoconsumo
    mh838_c_alt = _mod.mh838_c_alt
    mh838_c_base = _mod.mh838_c_base
    mh838_calcola = _mod.mh838_calcola
    mh838_co2_alt = _mod.mh838_co2_alt
    mh838_co2_base = _mod.mh838_co2_base
    mh838_co2_evitata = _mod.mh838_co2_evitata
    mh838_cop_min = _mod.mh838_cop_min
    mh838_csv = _mod.mh838_csv
    mh838_demo = _mod.mh838_demo
    mh838_demo_calcoli = _mod.mh838_demo_calcoli
    mh838_e_esportata = _mod.mh838_e_esportata
    mh838_e_pdc = _mod.mh838_e_pdc
    mh838_e_pv = _mod.mh838_e_pv
    mh838_e_rete = _mod.mh838_e_rete
    mh838_eta = _mod.mh838_eta
    mh838_flussi = _mod.mh838_flussi
    mh838_frazione = _mod.mh838_frazione
    mh838_int_pos = _mod.mh838_int_pos
    mh838_nneg = _mod.mh838_nneg
    mh838_num = _mod.mh838_num
    mh838_payback = _mod.mh838_payback
    mh838_pos = _mod.mh838_pos
    mh838_q_base = _mod.mh838_q_base
    mh838_q_gas = _mod.mh838_q_gas
    mh838_q_netto = _mod.mh838_q_netto
    mh838_q_recupero = _mod.mh838_q_recupero
    mh838_q_vasche = _mod.mh838_q_vasche
    mh838_risparmio = _mod.mh838_risparmio
    mh838_sensibilita = _mod.mh838_sensibilita
    mh838_tir = _mod.mh838_tir
    mh838_valida = _mod.mh838_valida
    mh838_van = _mod.mh838_van
    mh838_verdetto = _mod.mh838_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w841_helpers.py")
_UI_PATH = _risolvi("w841_ui.py")


def _trova_app():
    candidati = [
        os.path.expanduser("~/workspace/repo-dashboard/Dashboard-data-analist/app.py"),
        os.path.join(os.path.dirname(_HERE), "app.py"),
        os.path.join(_HERE, "app.py"),
        os.path.join(os.path.dirname(_HERE), "..", "app.py"),
        os.path.expanduser("~/workspace/qa-dashboard/repo/app.py"),
    ]
    for p in candidati:
        p = os.path.normpath(p)
        if os.path.exists(p):
            return p
    return candidati[0]


_APP_PATH = _trova_app()

_DEMO = {
    "q_vasche_kwh_th_anno": 600000.0,
    "q_base_kwh_th_anno": 950000.0,
    "q_recupero_kwh_th_anno": 180000.0,
    "q_netto_kwh_th_anno": 770000.0,
    "e_pdc_kwh_e_anno": 240625.0,
    "e_pv_kwh_e_anno": 88000.0,
    "e_pv_auto_kwh_e_anno": 61600.0,
    "e_pv_exp_kwh_e_anno": 26400.0,
    "e_rete_kwh_e_anno": 179025.0,
    "q_gas_kwh_anno": 1055555.5555555555,
    "c_base_eur_anno": 103800.0,
    "c_alt_eur_anno": 59385.5,
    "risparmio_eur_anno": 44414.5,
    "co2_base_t_anno": 221.11111111111111,
    "co2_alt_t_anno": 44.75625,
    "co2_evitata_t_anno": 176.35486111111112,
    "van": 53502.841258741784,
    "tir": 6.2313385335571025,
    "payback": 12,
    "cop_min": 1.7400772454597753,
}


def _demo_kwargs(**over):
    kw = dict(mh838_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh838_num(3, "x"), 3.0)
        self.assertEqual(mh838_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh838_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh838_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh838_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh838_pos(0, "x")
        with self.assertRaises(ValueError):
            mh838_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh838_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh838_eta(0.9, "eta"), 0.9)
        with self.assertRaises(ValueError):
            mh838_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh838_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh838_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh838_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh838_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh838_frazione(0, "quota"), 0.0)
        self.assertEqual(mh838_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh838_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh838_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_q_vasche_base_recupero_netto(self):
        self.assertEqual(mh838_q_vasche(500, 1200), 600000.0)
        self.assertEqual(mh838_q_base(600000.0, 150000, 200000), 950000.0)
        self.assertEqual(mh838_q_recupero(600000.0, 0.30), 180000.0)
        self.assertEqual(mh838_q_netto(950000.0, 180000.0), 770000.0)

    def test_recupero_zero_e_totale(self):
        self.assertEqual(mh838_q_recupero(600000.0, 0.0), 0.0)
        self.assertEqual(mh838_q_recupero(600000.0, 1.0), 600000.0)
        self.assertEqual(mh838_q_netto(950000.0, 600000.0), 350000.0)

    def test_e_pdc_e_q_gas(self):
        self.assertEqual(mh838_e_pdc(770000.0, 3.2), 240625.0)
        self.assertAlmostEqual(mh838_q_gas(950000.0, 0.90), 1055555.5555555555, places=6)

    def test_pv_autoconsumo_cappato_a_e_pdc(self):
        self.assertEqual(mh838_e_pv(80, 1100), 88000.0)
        self.assertAlmostEqual(mh838_autoconsumo(88000.0, 0.70, 240625.0), 61600.0, places=6)
        self.assertEqual(mh838_autoconsumo(88000.0, 0.70, 50000.0), 50000.0)

    def test_e_rete_e_esportata(self):
        self.assertEqual(mh838_e_rete(240625.0, 61600.0), 179025.0)
        self.assertEqual(mh838_e_esportata(88000.0, 61600.0), 26400.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh838_c_base(1055555.5555555555, 0.09, 40000, 0.22), 103800.0, places=6)
        self.assertAlmostEqual(mh838_c_alt(179025.0, 0.22, 20000), 59385.5, places=9)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh838_risparmio(103800.0, 59385.5), 44414.5, places=9)
        self.assertLess(mh838_risparmio(59385.5, 103800.0), 0.0)

    def test_co2_base_alt_evitata_fattori_separati(self):
        self.assertAlmostEqual(mh838_co2_base(1055555.5555555555, 0.20, 40000, 0.25), 221.11111111111111, places=9)
        self.assertAlmostEqual(mh838_co2_alt(179025.0, 0.25), 44.75625, places=9)
        self.assertAlmostEqual(mh838_co2_evitata(1055555.5555555555, 0.20, 40000, 0.25, 179025.0), 176.35486111111112, places=9)

    def test_co2_evitata_negativa_non_clampata(self):
        self.assertEqual(mh838_co2_evitata(100.0, 0.20, 0, 0.25, 2000.0), -0.48)

    def test_rete_alt_maggiore_di_aux_ma_costo_minore(self):
        bc = mh838_demo_calcoli()
        self.assertGreater(bc["e_rete_kwh_e_anno"], bc["e_aux_base"])
        self.assertLess(bc["c_alt_eur_anno"], bc["c_base_eur_anno"])

    def test_pv_esportato_senza_credito(self):
        bc = mh838_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_exp_kwh_e_anno"], 26400.0, places=6)
        self.assertAlmostEqual(bc["e_rete_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"], places=9)
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_rete_kwh_e_anno"] * 0.22 + 20000, places=6)


class TestFinanza(unittest.TestCase):
    def test_cop_min_demo_valore(self):
        cmin = mh838_cop_min(770000.0, 103800.0, 20000, 0.22, 61600.0)
        self.assertAlmostEqual(cmin, 1.7400772454597753, places=12)

    def test_cop_min_none_casi(self):
        self.assertIsNone(mh838_cop_min(770000.0, 103800.0, 20000, 0.0, 61600.0))
        self.assertIsNone(mh838_cop_min(0, 103800.0, 20000, 0.22, 61600.0))
        self.assertIsNone(mh838_cop_min(770000.0, 1000.0, 20000, 0.22, 61600.0))
        self.assertIsNone(mh838_cop_min(770000.0, 15000.0, 20000, 0.22, 61600.0))

    def test_cop_min_verifica_pareggio_su_demo(self):
        bc = mh838_demo_calcoli()
        cmin = bc["cop_min"]
        r = mh838_calcola(**_demo_kwargs(cop=cmin))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_cop_min_soglia_minima_su_demo(self):
        bc = mh838_demo_calcoli()
        cmin = bc["cop_min"]
        self.assertGreater(mh838_calcola(**_demo_kwargs(cop=cmin + 0.1))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh838_calcola(**_demo_kwargs(cop=cmin - 0.1))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh838_flussi(500000, 44414.5, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -500000)
        self.assertTrue(all(f == 44414.5 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh838_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 53502.841258741784, places=6)
        self.assertAlmostEqual(mh838_van([-500000] + [44414.5] * 20, 0.0), 388290.0, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh838_van([-500000] + [44414.5] * 20, 0.05), 53502.841258741784, places=6)
        self.assertLess(mh838_van([-500000] + [44414.5] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh838_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 6.2313385335571025, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh838_payback([-500000] + [44414.5] * 20), 12)
        self.assertEqual(mh838_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh838_payback([-500000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh838_verdetto(44414.5, 100.0, 500000, 0.10), "CONVIENTE")
        self.assertEqual(mh838_verdetto(44414.5, -20000.0, 500000, 0.10), "MARGINALE")
        self.assertEqual(mh838_verdetto(44414.5, -100000.0, 500000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh838_verdetto(0.0, 100.0, 500000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh838_verdetto(-100.0, 100.0, 500000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh838_verdetto(None, 100.0, 500000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh838_verdetto(44414.5, 0.0, 500000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh838_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("sup_vasche", "500"), ("sup_vasche", float("nan")),
                            ("sup_vasche", float("inf")), ("sup_vasche", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh838_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"sup_vasche": 0}, {"sup_vasche": -1},
                     {"q_spec_vasche": -0.1}, {"q_acs": -1}, {"q_amb": -1},
                     {"quota_recupero": -0.1}, {"quota_recupero": 1.1},
                     {"eta_caldaia": 0}, {"eta_caldaia": 1.1},
                     {"e_aux_base": -1},
                     {"p_el": -0.1}, {"p_gas": -0.1},
                     {"cop": 0}, {"cop": -1}, {"om_alt": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"quota_autoconsumo": -0.1}, {"quota_autoconsumo": 1.1},
                     {"capex": -1}, {"f_co2_el": -0.1}, {"f_co2_gas": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh838_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh838_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh838_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh838_valida(**_demo_kwargs(
            q_spec_vasche=0, q_acs=0, q_amb=0, quota_recupero=0,
            e_aux_base=0, p_el=0, p_gas=0, om_alt=0, p_pv_kwp=0,
            prod_specifica=0, quota_autoconsumo=0, capex=0,
            f_co2_el=0, f_co2_gas=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh838_demo()
        self.assertEqual(d["sup_vasche"], 500)
        self.assertEqual(d["q_spec_vasche"], 1200)
        self.assertEqual(d["q_acs"], 150000)
        self.assertEqual(d["q_amb"], 200000)
        self.assertEqual(d["quota_recupero"], 0.30)
        self.assertEqual(d["eta_caldaia"], 0.90)
        self.assertEqual(d["e_aux_base"], 40000)
        self.assertEqual(d["p_el"], 0.22)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["cop"], 3.2)
        self.assertEqual(d["om_alt"], 20000)
        self.assertEqual(d["p_pv_kwp"], 80)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["quota_autoconsumo"], 0.70)
        self.assertEqual(d["capex"], 500000)
        self.assertEqual(d["f_co2_el"], 0.25)
        self.assertEqual(d["f_co2_gas"], 0.20)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh838_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh838_demo_calcoli()
        self.assertAlmostEqual(bc["q_vasche_kwh_th_anno"], 600000.0, places=6)
        self.assertEqual(bc["q_base_kwh_th_anno"], 950000.0)
        self.assertEqual(bc["q_recupero_kwh_th_anno"], 180000.0)
        self.assertEqual(bc["q_netto_kwh_th_anno"], 770000.0)
        self.assertEqual(bc["e_pdc_kwh_e_anno"], 240625.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 88000.0)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 103800.0, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 59385.5, places=9)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh838_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[11], -11440.5, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[12], 32974.0, places=6)

    def test_demo_tabella_righe(self):
        bc = mh838_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Superficie vasche (m2)", voci)
        self.assertIn("Calore recuperato da acque termali reflue (kWh_th/anno)", voci)
        self.assertIn("Energia di rete alternativa (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico esportato, senza credito (kWh_e/anno)", voci)
        self.assertIn("COP minimo (soglia minima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh838_demo_calcoli()
        self.assertAlmostEqual(bc["q_vasche_kwh_th_anno"],
                               bc["sup_vasche"] * bc["q_spec_vasche"])
        self.assertAlmostEqual(bc["q_base_kwh_th_anno"],
                               bc["q_vasche_kwh_th_anno"] + bc["q_acs"] + bc["q_amb"])
        self.assertAlmostEqual(bc["q_netto_kwh_th_anno"],
                               bc["q_base_kwh_th_anno"] - bc["q_recupero_kwh_th_anno"])
        self.assertAlmostEqual(bc["e_rete_kwh_e_anno"],
                               bc["e_pdc_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        qv = 500 * 1200
        qb = qv + 150000 + 200000
        qrec = 0.30 * qv
        qn = qb - qrec
        epdc = qn / 3.2
        e_pv = 80 * 1100
        auto = min(e_pv * 0.70, epdc)
        er = epdc - auto
        qgas = qb / 0.90
        c_base = qgas * 0.09 + 40000 * 0.22
        c_alt = er * 0.22 + 20000
        bc = mh838_demo_calcoli()
        self.assertAlmostEqual(bc["q_vasche_kwh_th_anno"], qv, places=6)
        self.assertAlmostEqual(bc["q_base_kwh_th_anno"], qb, places=6)
        self.assertAlmostEqual(bc["q_recupero_kwh_th_anno"], qrec, places=6)
        self.assertAlmostEqual(bc["q_netto_kwh_th_anno"], qn, places=6)
        self.assertAlmostEqual(bc["e_pdc_kwh_e_anno"], epdc, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_rete_kwh_e_anno"], er, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh838_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_elettricita_piu_meno_20(self):
        meno = mh838_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 50531.6, places=6)
        self.assertAlmostEqual(meno["van"], 129735.42814509307, places=6)
        self.assertAlmostEqual(meno["tir"], 7.895732673237997, places=6)
        self.assertEqual(meno["payback"], 10)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh838_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 38297.4, places=6)
        self.assertAlmostEqual(piu["van"], -22729.74562760963, places=6)
        self.assertAlmostEqual(piu["tir"], 4.45772634756423, places=6)
        self.assertEqual(piu["payback"], 14)
        self.assertEqual(piu["verdetto"], "MARGINALE")

    def test_elettricita_alta_peggiora_il_caso(self):
        demo = mh838_demo_calcoli()
        meno = mh838_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh838_calcola(**_demo_kwargs(p_el=0.264))
        self.assertGreater(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(demo["e_rete_kwh_e_anno"], demo["e_aux_base"])

    def test_variante_senza_recupero(self):
        r = mh838_calcola(**_demo_kwargs(quota_recupero=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 32039.5, places=6)
        self.assertAlmostEqual(r["van"], -100717.01173019038, places=6)
        self.assertAlmostEqual(r["tir"], 2.4887533123412, places=6)
        self.assertEqual(r["payback"], 16)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_senza_fotovoltaico(self):
        r = mh838_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 30862.5, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -115385.03330336002, places=6)
        self.assertAlmostEqual(r["tir"], 2.096041639454878, places=6)
        self.assertEqual(r["payback"], 17)

    def test_variante_cop_basso_non_convinte(self):
        r = mh838_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 12652.0, places=6)
        self.assertAlmostEqual(r["van"], -342328.11474618426, places=6)
        self.assertAlmostEqual(r["tir"], -5.762308441801739, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_capex_doppio_non_convinte(self):
        r = mh838_calcola(**_demo_kwargs(capex=1000000))
        self.assertAlmostEqual(r["van"], -446497.1587412582, places=6)
        self.assertAlmostEqual(r["tir"], -1.1025836740320212, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh838_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -157043.00398772137, places=6)
        self.assertAlmostEqual(r["tir"], -2.097751065775301, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh838_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 388290.0, places=6)
        self.assertEqual(zero["payback"], 12)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh838_sensibilita(**mh838_demo())
        self.assertEqual(set(s.keys()), {"el_meno20", "el_piu20", "rec_0",
                                         "senza_pv", "cop_2", "capex_doppio",
                                         "vita_10", "wacc_0"})
        self.assertAlmostEqual(s["el_meno20"]["risparmio_eur_anno"], 50531.6, places=6)
        self.assertAlmostEqual(s["el_piu20"]["van"], -22729.74562760963, places=6)
        self.assertEqual(s["rec_0"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh838_demo_calcoli()
        b = mh838_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh838_demo()
        attese = {"sup_vasche", "q_spec_vasche", "q_acs", "q_amb",
                  "quota_recupero", "eta_caldaia", "e_aux_base",
                  "p_el", "p_gas", "cop", "om_alt", "p_pv_kwp",
                  "prod_specifica", "quota_autoconsumo", "capex",
                  "f_co2_el", "f_co2_gas", "wacc", "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["sup_vasche", "q_spec_vasche", "q_acs", "q_amb",
                 "quota_recupero", "eta_caldaia", "e_aux_base",
                 "p_el", "p_gas", "cop", "om_alt", "p_pv_kwp",
                 "prod_specifica", "quota_autoconsumo", "capex",
                 "f_co2_el", "f_co2_gas", "wacc", "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh838_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh838_calcola(**_demo_kwargs(quota_recupero=1.1))
        with self.assertRaises(ValueError):
            mh838_calcola(**_demo_kwargs(quota_autoconsumo=1.1))
        with self.assertRaises(ValueError):
            mh838_calcola(**_demo_kwargs(eta_caldaia=1.1))
        with self.assertRaises(ValueError):
            mh838_calcola(**_demo_kwargs(eta_caldaia=0))
        with self.assertRaises(ValueError):
            mh838_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("sup_vasche", "500"), ("sup_vasche", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh838_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh838_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_autoconsumo=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_el=0, f_co2_gas=0))
        self.assertTrue(r["valid"])
        r2 = mh838_calcola(**_demo_kwargs(om_alt=30000, p_el=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh838_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        cmin = mh838_demo_calcoli()["cop_min"]
        r = mh838_calcola(**_demo_kwargs(cop=cmin))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh838_demo_calcoli()
        csv = mh838_csv(bc, dict(mh838_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh838_demo_calcoli()
        csv = mh838_csv(bc, dict(mh838_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1] for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]), 44414.5, places=6)
        self.assertAlmostEqual(float(righe["cop_min"]), 1.7400772454597753, places=12)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh838_demo_calcoli()
        csv = mh838_csv(bc, dict(mh838_demo()))
        for chiave in mh838_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh837_", src)
        self.assertNotIn("mh836_", src)
        self.assertNotIn("mh835_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab838:"), 1)
        self.assertTrue(src.startswith("    # W841"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Terme: pompa di calore + recupero calore acque termali reflue + fotovoltaico battono caldaia a gas per vasche, ACS e ambienti?", src)
        self.assertIn("♨️ Terme: pompa di calore + recupero calore acque termali reflue + fotovoltaico battono caldaia a gas per vasche, ACS e ambienti?", src)
        self.assertNotIn("tab837", src)
        self.assertNotIn("tab836", src)
        self.assertNotIn("tab835", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh837_", "mh836_", "mh835_", "mh834_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh837_", src)
        self.assertNotIn("st837_", src)
        self.assertNotIn("mh836_", src)
        self.assertNotIn("st836_", src)
        chiavi = re.findall(r'key="(st838_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st838_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st838_calcola"', src)
        self.assertIn('key="st838_csv"', src)
        self.assertIn('key="st838_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def838\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh838_demo().keys()), lette - set(mh838_demo().keys()))
        self.assertEqual(lette, set(mh838_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc838\['([^']+)'\]", src))
        attese = set(mh838_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg838"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


class TestAppPresenza(unittest.TestCase):
    def test_app_contiene_tab838_e_titolo(self):
        self.assertTrue(os.path.exists(_APP_PATH), f"app.py non trovato: {_APP_PATH} (apply tab838 non ancora fatto)")
        src = open(_APP_PATH, encoding="utf-8").read()
        self.assertIn("tab838", src)
        self.assertIn("♨️ Terme: pompa di calore + recupero calore acque termali reflue + fotovoltaico battono caldaia a gas per vasche, ACS e ambienti?", src)


if __name__ == "__main__":
    unittest.main()
