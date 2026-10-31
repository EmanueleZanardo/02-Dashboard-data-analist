"""Test nuova scheda tab835 "Acquedotto:
pompe a velocita' variabile + riduzione
perdite + fotovoltaico battono pompe a
velocita' fissa + perdite alte?".

Business case deterministico di un
acquedotto civile in pressione guidato
dal VOLUME EROGATO: V_pompato_base =
V_erogato / (1 - perdita_base);
V_pompato_alt = V_erogato /
(1 - perdita_alt); E_base = V_pompato_base
x e_spec_base; E_alt_lorda = V_pompato_alt
x e_spec_alt; E_pv = kWp x producibilita';
autoconsumo = min(E_pv x quota_autoconsumo,
E_alt_lorda) (cappato: E_alt_netta non
scende sotto zero); E_alt_netta =
E_alt_lorda - autoconsumo; E_esportata =
E_pv - autoconsumo (NESSUN credito di
costo ne' di CO2: scelta conservativa);
C_base = E_base x p_el + V_pompato_base x
c_acqua; C_alt = E_alt_netta x p_el +
V_pompato_alt x c_acqua + O&M_alt;
risparmio = C_base - C_alt; CO2 base =
E_base x f_co2 / 1000; CO2 alt =
E_alt_netta x f_co2 / 1000; CO2 evitata =
base - alt (segno libero, non clampata:
puo' essere negativa se E_alt_netta >
E_base); flussi [-CAPEX, risparmio x
vita]; VAN al WACC (FRAZIONE, non
percentuale); TIR per bisezione; payback
(primo anno con cumulato >= 0);
e_spec_alt_max = ((C_base - V_pompato_alt
x c_acqua - O&M_alt) / p_el +
autoconsumo_saturo) / V_pompato_alt nel
ramo autoconsumo saturo, None se p_el
<= 0, V_pompato_alt <= 0, e_max < 0, o
ramo incoerente (V_pompato_alt x e_max <
autoconsumo_saturo), SOGLIA MASSIMA
quando esiste (sotto di essa
l'alternativa vince sui costi, sopra
perde; e' dominata ANCHE dal valore
dell'acqua risparmiata, non solo
dall'elettricita'). Per p_el NON viene
dichiarato alcun pareggio: il pareggio
dichiarato qui e' SOLO e_spec_alt_max.
Verdetto: NON_CALCOLABILE se input degenere
(V_erogato <= 0, perdite < 0 o >= 1,
e_spec < 0, prezzi < 0, O&M_alt < 0, kWp
< 0, producibilita' < 0, quota < 0 o > 1,
CAPEX < 0, f_co2 < 0, WACC < 0, vita <= 0,
tolleranza < 0) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza
FRAZIONE del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Guard UI
IDENTICA agli helper: nessuna divergenza
di verdetto. Tutti gli slider UI hanno
minimo 0, quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0 raggiungibili
via slider sono bloccati in UI esattamente
come negli helper dove previsto (V_erogato,
vita). Gli zeri ammessi in entrambi
(e_spec, prezzi, O&M_alt, kWp, producibilita',
quota, CAPEX, f_co2, WACC, tolleranza,
perdite a 0) non creano divergenza. Perdite
>= 1 e quota > 1 sono degeneri in entrambi
ma non raggiungibili via slider (tetti 0,90
e 1,0). WACC sopra 0,20 e tolleranza sopra
1,0 sono ammessi negli helper e limitati
solo dagli slider UI (0,20 e 1,0): nessuna
divergenza nel range raggiungibile, perche'
la guard controlla solo gli stessi limiti
degli helper.
Distinzione esplicita: distinto dal
depuratore (trattamento reflui: qui acqua
potabile in pressione, niente trattamento
reflui), dall'irrigazione agricola (acqua
per campi e turni irrigui: qui acquedotto
civile con domanda continua di acqua
potabile) e dalla piscina (acqua di vasca:
qui niente vasca, solo rete idrica in
pressione): qui driver VOLUME EROGATO +
POMPE VSD + RIDUZIONE PERDITE +
FOTOVOLTAICO IN AUTOCONSUMO.

Demo (acquedotto): 1.000.000 m3/anno
erogati, perdite base 0,35 (volume
pompato 1.538.461,54 m3/anno) e
alternative 0,20 (1.250.000,00 m3/anno),
consumo specifico base 0,45 (energia
base 692.307,69 kWh_e/anno) e alternativo
0,32 (energia alternativa lorda
400.000,00 kWh_e/anno), fotovoltaico
150 kWp a 1.100 kWh/kWp/anno (165.000,00
kWh_e/anno, autoconsumo 115.500,00,
esportato 49.500,00 senza credito),
energia di rete alternativa netta
284.500,00 kWh_e/anno, prezzo elettricita'
0,22 EUR/kWh, costo acqua 0,35 EUR/m3,
O&M alternativo 25.000 EUR/anno, CAPEX
600.000 EUR, fattore CO2 0,25 kg/kWh,
WACC 0,05 (frazione), vita 20 anni,
tolleranza 0,10 (frazione del CAPEX).
Valori calcolati eseguendo
mh835_demo_calcoli(): V_pompato_base
1.538.461,54, V_pompato_alt 1.250.000,00,
E_base 692.307,69, E_alt_lorda 400.000,00,
E_pv 165.000,00, autoconsumo 115.500,00,
E_alt_netta 284.500,00, esportata
49.500,00, C_base 690.769,23, C_alt
525.090,00, risparmio 165.679,23,
CO2_base 173,08, CO2_alt 71,13,
CO2_evitata 101,95, VAN
1464729,4232363757, TIR
27,39541361323613 %, payback 4,
e_spec_alt_max 0,9224699300699299,
verdetto CONVIENTE.

Destinazione nel repo: tests/test_w835_acquedotto.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w837_helpers import (
    demo_calcoli,
    mh835_autoconsumo,
    mh835_c_alt,
    mh835_c_base,
    mh835_calcola,
    mh835_co2_alt,
    mh835_co2_base,
    mh835_co2_evitata,
    mh835_csv,
    mh835_demo,
    mh835_demo_calcoli,
    mh835_e_alt_lorda,
    mh835_e_alt_netta,
    mh835_e_base,
    mh835_e_esportata,
    mh835_e_pv,
    mh835_e_spec_alt_max,
    mh835_flussi,
    mh835_frazione,
    mh835_int_pos,
    mh835_nneg,
    mh835_num,
    mh835_payback,
    mh835_perdita,
    mh835_pos,
    mh835_risparmio,
    mh835_sensibilita,
    mh835_tir,
    mh835_v_pompato,
    mh835_valida,
    mh835_van,
    mh835_verdetto,
)

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w837_helpers.py")
_UI_PATH = _risolvi("w837_ui.py")


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
    "v_pompato_base_m3_anno": 1538461.5384615385,
    "v_pompato_alt_m3_anno": 1250000.0,
    "e_base_kwh_e_anno": 692307.6923076924,
    "e_alt_lorda_kwh_e_anno": 400000.0,
    "e_pv_kwh_e_anno": 165000.0,
    "e_pv_auto_kwh_e_anno": 115500.0,
    "e_pv_exp_kwh_e_anno": 49500.0,
    "e_alt_netta_kwh_e_anno": 284500.0,
    "c_base_eur_anno": 690769.2307692308,
    "c_alt_eur_anno": 525090.0,
    "risparmio_eur_anno": 165679.23076923075,
    "co2_base_t_anno": 173.0769230769231,
    "co2_alt_t_anno": 71.125,
    "co2_evitata_t_anno": 101.9519230769231,
    "van": 1464729.4232363757,
    "tir": 27.39541361323613,
    "payback": 4,
    "e_spec_alt_max": 0.9224699300699299,
}


def _demo_kwargs(**over):
    kw = dict(mh835_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh835_num(3, "x"), 3.0)
        self.assertEqual(mh835_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh835_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh835_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh835_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh835_pos(0, "x")
        with self.assertRaises(ValueError):
            mh835_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh835_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh835_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh835_frazione(0, "quota"), 0.0)
        self.assertEqual(mh835_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh835_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh835_frazione(1.1, "quota")

    def test_perdita_limiti_uno_escluso(self):
        self.assertEqual(mh835_perdita(0, "perdita"), 0.0)
        self.assertEqual(mh835_perdita(0.99, "perdita"), 0.99)
        with self.assertRaises(ValueError):
            mh835_perdita(1.0, "perdita")
        with self.assertRaises(ValueError):
            mh835_perdita(1.1, "perdita")
        with self.assertRaises(ValueError):
            mh835_perdita(-0.1, "perdita")


class TestFisica(unittest.TestCase):
    def test_volumi_pompati(self):
        self.assertAlmostEqual(mh835_v_pompato(1000000, 0.35), 1538461.5384615385, places=9)
        self.assertEqual(mh835_v_pompato(1000000, 0.20), 1250000.0)

    def test_energie_base_lorda_pv(self):
        self.assertAlmostEqual(mh835_e_base(1538461.5384615385, 0.45), 692307.6923076924, places=9)
        self.assertEqual(mh835_e_alt_lorda(1250000.0, 0.32), 400000.0)
        self.assertEqual(mh835_e_pv(150, 1100), 165000.0)

    def test_autoconsumo_cappato(self):
        self.assertAlmostEqual(mh835_autoconsumo(165000.0, 0.70, 400000.0), 115500.0, places=6)
        self.assertEqual(mh835_autoconsumo(165000.0, 0.70, 50000.0), 50000.0)

    def test_e_alt_netta_e_esportata(self):
        self.assertEqual(mh835_e_alt_netta(400000.0, 115500.0), 284500.0)
        self.assertEqual(mh835_e_esportata(165000.0, 115500.0), 49500.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh835_c_base(692307.6923076924, 0.22, 1538461.5384615385, 0.35), 690769.2307692308, places=9)
        self.assertAlmostEqual(mh835_c_alt(284500.0, 0.22, 1250000.0, 0.35, 25000), 525090.0, places=9)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh835_risparmio(690769.2307692308, 525090.0), 165679.23076923075, places=9)
        self.assertLess(mh835_risparmio(525090.0, 690769.2307692308), 0.0)

    def test_co2_base_alt_evitata(self):
        self.assertAlmostEqual(mh835_co2_base(692307.6923076924, 0.25), 173.0769230769231, places=9)
        self.assertEqual(mh835_co2_alt(284500.0, 0.25), 71.125)
        self.assertAlmostEqual(mh835_co2_evitata(692307.6923076924, 284500.0, 0.25), 101.9519230769231, places=9)

    def test_co2_evitata_negativa_non_clampata(self):
        self.assertEqual(mh835_co2_evitata(100.0, 200.0, 0.25), -0.025)

    def test_alt_netta_e_volume_minori_di_base_nel_demo(self):
        bc = mh835_demo_calcoli()
        self.assertLess(bc["e_alt_netta_kwh_e_anno"], bc["e_base_kwh_e_anno"])
        self.assertLess(bc["v_pompato_alt_m3_anno"], bc["v_pompato_base_m3_anno"])

    def test_pv_esportato_senza_credito(self):
        bc = mh835_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_exp_kwh_e_anno"], 49500.0, places=6)
        self.assertAlmostEqual(bc["e_alt_netta_kwh_e_anno"],
                               bc["e_alt_lorda_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"], places=9)
        # Se l'esportato avesse credito, il costo alternativo sarebbe piu' basso:
        # qui non lo e': il costo usa solo la netta.
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_alt_netta_kwh_e_anno"] * 0.22 + bc["v_pompato_alt_m3_anno"] * 0.35 + 25000, places=6)


class TestFinanza(unittest.TestCase):
    def test_e_spec_alt_max_demo_valore(self):
        emax = mh835_e_spec_alt_max(690769.2307692308, 1250000.0, 0.35, 25000, 0.22, 115500.0)
        self.assertAlmostEqual(emax, 0.9224699300699299, places=12)

    def test_e_spec_alt_max_none_casi(self):
        self.assertIsNone(mh835_e_spec_alt_max(690769.2307692308, 1250000.0, 0.35, 25000, 0.0, 115500.0))
        self.assertIsNone(mh835_e_spec_alt_max(1000.0, 1250000.0, 0.35, 25000, 0.22, 115500.0))
        self.assertIsNone(mh835_e_spec_alt_max(400000.0, 1250000.0, 0.35, 0, 0.22, 200000.0))

    def test_e_spec_alt_max_verifica_pareggio_su_demo(self):
        bc = mh835_demo_calcoli()
        emax = bc["e_spec_alt_max"]
        r = mh835_calcola(**_demo_kwargs(e_spec_alt=emax))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_e_spec_alt_max_soglia_massima_su_demo(self):
        bc = mh835_demo_calcoli()
        emax = bc["e_spec_alt_max"]
        self.assertGreater(mh835_calcola(**_demo_kwargs(e_spec_alt=emax - 0.1))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh835_calcola(**_demo_kwargs(e_spec_alt=emax + 0.1))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh835_flussi(600000, 165679.23076923075, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -600000)
        self.assertTrue(all(f == 165679.23076923075 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh835_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 1464729.4232363757, places=6)
        self.assertAlmostEqual(mh835_van([-600000] + [165679.23076923075] * 20, 0.0), 2713584.615384616, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        # WACC 0,05 come frazione: VAN demo; se fosse percentuale
        # (5,0) il risultato sarebbe diverso e molto piu' basso.
        self.assertAlmostEqual(mh835_van([-600000] + [165679.23076923075] * 20, 0.05), 1464729.4232363757, places=6)
        self.assertLess(mh835_van([-600000] + [165679.23076923075] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh835_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 27.39541361323613, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh835_payback([-600000] + [165679.23076923075] * 20), 4)
        self.assertEqual(mh835_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh835_payback([-600000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh835_verdetto(165679.23076923075, 100.0, 600000, 0.10), "CONVIENTE")
        self.assertEqual(mh835_verdetto(165679.23076923075, -30000.0, 600000, 0.10), "MARGINALE")
        self.assertEqual(mh835_verdetto(165679.23076923075, -100000.0, 600000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh835_verdetto(0.0, 100.0, 600000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh835_verdetto(-100.0, 100.0, 600000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh835_verdetto(None, 100.0, 600000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh835_verdetto(165679.23076923075, 0.0, 600000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh835_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("v_erogato", "1000000"), ("v_erogato", float("nan")),
                            ("v_erogato", float("inf")), ("v_erogato", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh835_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"v_erogato": 0}, {"v_erogato": -1}, {"perdita_base": -0.1},
                     {"perdita_base": 1.0}, {"perdita_alt": 1.0},
                     {"e_spec_base": -0.1}, {"e_spec_alt": -0.1},
                     {"p_el": -0.1}, {"c_acqua": -0.1}, {"om_alt": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"quota_autoconsumo": -0.1}, {"quota_autoconsumo": 1.1},
                     {"capex": -1}, {"f_co2": -0.1}, {"wacc": -0.1},
                     {"vita": 0}, {"vita": 20.5}, {"tolleranza": -0.1}):
            self.assertFalse(mh835_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh835_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh835_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh835_valida(**_demo_kwargs(
            perdita_base=0, perdita_alt=0, e_spec_base=0,
            p_el=0, c_acqua=0, om_alt=0, p_pv_kwp=0,
            prod_specifica=0, quota_autoconsumo=0, capex=0,
            f_co2=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh835_demo()
        self.assertEqual(d["v_erogato"], 1000000)
        self.assertEqual(d["perdita_base"], 0.35)
        self.assertEqual(d["perdita_alt"], 0.20)
        self.assertEqual(d["e_spec_base"], 0.45)
        self.assertEqual(d["e_spec_alt"], 0.32)
        self.assertEqual(d["p_el"], 0.22)
        self.assertEqual(d["c_acqua"], 0.35)
        self.assertEqual(d["om_alt"], 25000)
        self.assertEqual(d["p_pv_kwp"], 150)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["quota_autoconsumo"], 0.70)
        self.assertEqual(d["capex"], 600000)
        self.assertEqual(d["f_co2"], 0.25)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh835_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh835_demo_calcoli()
        self.assertAlmostEqual(bc["v_pompato_base_m3_anno"], 1538461.5384615385, places=6)
        self.assertEqual(bc["v_pompato_alt_m3_anno"], 1250000.0)
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], 692307.6923076924, places=6)
        self.assertEqual(bc["e_alt_lorda_kwh_e_anno"], 400000.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 165000.0)
        self.assertEqual(bc["c_base_eur_anno"], 690769.2307692308)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 525090.0, places=9)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh835_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[3], -102962.30769230775, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[4], 62716.923076923005, places=6)

    def test_demo_tabella_righe(self):
        bc = mh835_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Volume erogato (m3/anno)", voci)
        self.assertIn("Volume pompato alternativo (m3/anno)", voci)
        self.assertIn("Energia di rete alternativa netta (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico esportato, senza credito (kWh_e/anno)", voci)
        self.assertIn("Consumo specifico alternativo massimo (soglia massima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh835_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["v_pompato_base_m3_anno"] * bc["e_spec_base"])
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"],
                               bc["v_pompato_alt_m3_anno"] * bc["e_spec_alt"])
        self.assertAlmostEqual(bc["e_alt_netta_kwh_e_anno"],
                               bc["e_alt_lorda_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        vpb = 1000000 / (1 - 0.35)
        vpa = 1000000 / (1 - 0.20)
        eb = vpb * 0.45
        ea = vpa * 0.32
        e_pv = 150 * 1100
        auto = min(e_pv * 0.70, ea)
        en = ea - auto
        c_base = eb * 0.22 + vpb * 0.35
        c_alt = en * 0.22 + vpa * 0.35 + 25000
        bc = mh835_demo_calcoli()
        self.assertAlmostEqual(bc["v_pompato_base_m3_anno"], vpb, places=6)
        self.assertAlmostEqual(bc["v_pompato_alt_m3_anno"], vpa, places=6)
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], eb, places=6)
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"], ea, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_alt_netta_kwh_e_anno"], en, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh835_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_elettricita_piu_meno_20(self):
        meno = mh835_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 147735.69230769237, places=6)
        self.assertAlmostEqual(meno["van"], 1241113.2726392283, places=6)
        self.assertAlmostEqual(meno["tir"], 24.305261398287087, places=6)
        self.assertEqual(meno["payback"], 5)
        piu = mh835_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 183622.76923076925, places=6)
        self.assertAlmostEqual(piu["van"], 1688345.5738335252, places=6)
        self.assertAlmostEqual(piu["tir"], 30.453600421323756, places=6)
        self.assertEqual(piu["payback"], 4)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_elettricita_alta_migliora_il_caso(self):
        demo = mh835_demo_calcoli()
        meno = mh835_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh835_calcola(**_demo_kwargs(p_el=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(demo["e_alt_netta_kwh_e_anno"], demo["e_base_kwh_e_anno"])

    def test_variante_perdita_alt_025_e_015(self):
        r25 = mh835_calcola(**_demo_kwargs(perdita_alt=0.25))
        self.assertAlmostEqual(r25["risparmio_eur_anno"], 130645.8974358975, places=6)
        self.assertAlmostEqual(r25["van"], 1028136.6542360594, places=6)
        self.assertEqual(r25["payback"], 5)
        self.assertEqual(r25["verdetto"], "CONVIENTE")
        r15 = mh835_calcola(**_demo_kwargs(perdita_alt=0.15))
        self.assertAlmostEqual(r15["risparmio_eur_anno"], 196590.9954751131, places=6)
        self.assertAlmostEqual(r15["van"], 1849958.337060185, places=6)
        self.assertEqual(r15["payback"], 4)
        self.assertEqual(r15["verdetto"], "CONVIENTE")

    def test_variante_senza_fotovoltaico(self):
        r = mh835_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 140269.23076923075, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 1148064.658432435, places=6)
        self.assertEqual(r["payback"], 5)

    def test_variante_senza_riduzione_perdite_marginale(self):
        r = mh835_calcola(**_demo_kwargs(perdita_alt=0.35))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 44410.0, places=6)
        self.assertEqual(r["verdetto"], "MARGINALE")
        self.assertAlmostEqual(r["van"], -46553.238687799356, places=6)
        self.assertAlmostEqual(r["tir"], 4.06664946322547, places=6)
        self.assertEqual(r["payback"], 14)

    def test_variante_capex_doppio_convinte(self):
        r = mh835_calcola(**_demo_kwargs(capex=1200000))
        self.assertAlmostEqual(r["van"], 864729.4232363757, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertEqual(r["payback"], 8)

    def test_variante_vita_10_convinte(self):
        r = mh835_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 679331.1032712399, places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertEqual(r["payback"], 4)

    def test_variante_wacc_zero(self):
        zero = mh835_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 2713584.615384616, places=6)
        self.assertEqual(zero["payback"], 4)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh835_sensibilita(**mh835_demo())
        self.assertEqual(set(s.keys()), {"el_meno20", "el_piu20", "pa_025",
                                         "pa_015", "senza_pv", "senza_perdite",
                                         "capex_doppio", "vita_10", "wacc_0"})
        self.assertAlmostEqual(s["el_meno20"]["risparmio_eur_anno"], 147735.69230769237, places=6)
        self.assertAlmostEqual(s["el_piu20"]["van"], 1688345.5738335252, places=6)
        self.assertEqual(s["pa_025"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["pa_015"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_pv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_perdite"]["verdetto"], "MARGINALE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh835_demo_calcoli()
        b = mh835_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh835_demo()
        attese = {"v_erogato", "perdita_base", "perdita_alt",
                  "e_spec_base", "e_spec_alt",
                  "p_el", "c_acqua", "om_alt",
                  "p_pv_kwp", "prod_specifica", "quota_autoconsumo",
                  "capex", "f_co2", "wacc", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["v_erogato", "perdita_base", "perdita_alt",
                 "e_spec_base", "e_spec_alt",
                 "p_el", "c_acqua", "om_alt",
                 "p_pv_kwp", "prod_specifica", "quota_autoconsumo",
                 "capex", "f_co2", "wacc", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh835_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_perdita_uno_e_quota_sopra_uno(self):
        with self.assertRaises(ValueError):
            mh835_calcola(**_demo_kwargs(perdita_base=1.0))
        with self.assertRaises(ValueError):
            mh835_calcola(**_demo_kwargs(perdita_alt=1.0))
        with self.assertRaises(ValueError):
            mh835_calcola(**_demo_kwargs(quota_autoconsumo=1.1))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("v_erogato", "1000000"), ("v_erogato", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh835_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh835_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_autoconsumo=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2=0))
        self.assertTrue(r["valid"])
        r2 = mh835_calcola(**_demo_kwargs(om_alt=25000, p_el=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh835_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        emax = mh835_demo_calcoli()["e_spec_alt_max"]
        r = mh835_calcola(**_demo_kwargs(e_spec_alt=emax))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh835_demo_calcoli()
        csv = mh835_csv(bc, dict(mh835_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh835_demo_calcoli()
        csv = mh835_csv(bc, dict(mh835_demo()))
        self.assertIn("risparmio_eur_anno;165679.23076923075", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh835_demo_calcoli()
        csv = mh835_csv(bc, dict(mh835_demo()))
        for chiave in mh835_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh834_", src)
        self.assertNotIn("mh833_", src)
        self.assertNotIn("mh832_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab835:"), 1)
        self.assertTrue(src.startswith("    # W837"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Acquedotto: pompe a velocita' variabile + riduzione perdite + fotovoltaico", src)
        self.assertIn("🚰 Acquedotto: pompe a velocita' variabile + riduzione perdite + fotovoltaico battono pompe a velocita' fissa + perdite alte?", src)
        self.assertNotIn("tab834", src)
        self.assertNotIn("tab833", src)
        self.assertNotIn("tab832", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh834_", "mh833_", "mh832_", "mh831_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh834_", src)
        self.assertNotIn("st834_", src)
        self.assertNotIn("mh833_", src)
        self.assertNotIn("st833_", src)
        chiavi = re.findall(r'key="(st835_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st835_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st835_calcola"', src)
        self.assertIn('key="st835_csv"', src)
        self.assertIn('key="st835_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def835\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh835_demo().keys()), lette - set(mh835_demo().keys()))
        self.assertEqual(lette, set(mh835_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc835\['([^']+)'\]", src))
        attese = set(mh835_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg835"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        # Ogni slider/number_input deve avere min_value=0 (negativi non
        # raggiungibili via UI, ma guardati comunque negli helper).
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


class TestAppPresenza(unittest.TestCase):
    def test_app_contiene_tab835_e_titolo(self):
        self.assertTrue(os.path.exists(_APP_PATH), f"app.py non trovato: {_APP_PATH} (apply tab835 non ancora fatto)")
        src = open(_APP_PATH, encoding="utf-8").read()
        self.assertIn("tab835", src)
        self.assertIn("🚰 Acquedotto: pompe a velocita' variabile + riduzione perdite + fotovoltaico battono pompe a velocita' fissa + perdite alte?", src)


if __name__ == "__main__":
    unittest.main()
