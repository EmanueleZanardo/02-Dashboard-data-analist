"""Test nuova scheda tab836 "Funivia:
azionamento con recupero in frenata
+ motori efficienti + fotovoltaico in
stazione battono azionamento
tradizionale senza recupero +
riscaldamento stazione a gas?".

Business case deterministico di una
funivia turistico-montana con stazione
guidata dai PASSEGGERI/anno:
E_base = passeggeri x e_spec_base;
E_alt_lorda = passeggeri x e_spec_alt;
recupero = quota_recupero x E_alt_lorda;
E_alt_netta_trazione = E_alt_lorda -
recupero; E_pv = kWp x producibilita';
autoconsumo = min(E_pv x quota_autoconsumo,
E_alt_netta_trazione) (cappato: E_alt_rete
non scende sotto zero); E_alt_rete =
E_alt_netta_trazione - autoconsumo;
E_esportata = E_pv - autoconsumo (NESSUN
credito di costo ne' di CO2: scelta
conservativa); C_base = E_base x p_el +
Q_gas x p_gas; C_alt = E_alt_rete x p_el
+ (Q_gas / COP) x p_el + O&M_alt;
risparmio = C_base - C_alt; CO2 base =
E_base x f_co2_el / 1000 + Q_gas x
f_co2_gas / 1000; CO2 alt = E_alt_rete x
f_co2_el / 1000 + (Q_gas / COP) x
f_co2_el / 1000; CO2 evitata = base - alt
(segno libero, non clampata: puo' essere
negativa se E_alt_rete supera E_base);
flussi [-CAPEX, risparmio x vita]; VAN al
WACC (FRAZIONE, non percentuale); TIR per
bisezione; payback (primo anno con
cumulato >= 0); e_spec_alt_max = ((C_base
- Q_gas / COP x p_el - O&M_alt) / p_el +
autoconsumo_saturo) / (passeggeri x
(1 - quota_recupero)) nel ramo autoconsumo
saturo, None se p_el <= 0, passeggeri
<= 0, quota_recupero >= 1, e_max < 0, o
ramo incoerente (passeggeri x e_max x
(1 - quota_recupero) < autoconsumo_saturo),
SOGLIA MASSIMA quando esiste (sotto di
essa l'alternativa vince sui costi, sopra
perde; e' dominata ANCHE dal valore del
riscaldamento e dall'O&M, non solo
dall'elettricita' di trazione). Per p_el
NON viene dichiarato alcun pareggio: il
pareggio dichiarato qui e' SOLO
e_spec_alt_max. Verdetto: NON_CALCOLABILE
se input degenere (passeggeri <= 0,
e_spec < 0, quote < 0 o > 1, prezzi < 0,
Q_gas < 0, COP <= 0, O&M_alt < 0, kWp < 0,
producibilita' < 0, CAPEX < 0, fattori CO2
< 0, WACC < 0, vita <= 0, tolleranza < 0)
o se risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE
se VAN negativa entro tolleranza FRAZIONE
del CAPEX, NON_CONVIENTE se VAN negativa
oltre la tolleranza. Guard UI IDENTICA
agli helper: nessuna divergenza di
verdetto. Tutti gli slider UI hanno minimo
0, quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0 raggiungibili
via slider sono bloccati in UI esattamente
come negli helper dove previsto (passeggeri,
vita, COP). Gli zeri ammessi in entrambi
(e_spec, prezzi, Q_gas, O&M_alt, kWp,
producibilita', quote, CAPEX, fattori CO2,
WACC, tolleranza) non creano divergenza.
Quote > 1 sono degeneri in entrambi ma non
raggiungibili via slider (tetto 1,0). WACC
sopra 0,20 e tolleranza sopra 1,0 sono
ammessi negli helper e limitati solo dagli
slider UI (0,20 e 1,0): nessuna divergenza
nel range raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper. Distinzione esplicita: distinto
dalla seggiovia o cabinovia a sola salita
senza recupero (frenata rigenerativa
assente: qui la funivia recupera energia
in discesa), dal trasporto urbano (corse
urbane con fermate frequenti e domanda
pendolare: qui impianto a fune
turistico-montano con stazione) e
dall'impianto di risalita a motore termico
(trazione diesel: qui trazione elettrica in
entrambi i casi, cambia solo recupero,
efficienza dei motori, fotovoltaico e
riscaldamento): qui driver PASSEGGERI +
RECUPERO IN FRENATA + MOTORI EFFICIENTI +
FOTOVOLTAICO IN STAZIONE + POMPA DI CALORE.

Demo (funivia): 400.000 passeggeri/anno,
consumo specifico base 1,20 (energia base
480.000,00 kWh_e/anno) e alternativo 0,85
(energia alternativa lorda 340.000,00
kWh_e/anno), quota recupero 0,25
(recupero 85.000,00, netta di trazione
255.000,00 kWh_e/anno), fotovoltaico
120 kWp a 1.100 kWh/kWp/anno (132.000,00
kWh_e/anno, autoconsumo 92.400,00,
esportato 39.600,00 senza credito),
energia di rete alternativa 162.600,00
kWh_e/anno, prezzo elettricita' 0,22
EUR/kWh, prezzo gas 0,09 EUR/kWh_th,
fabbisogno termico 180.000 kWh_th/anno,
COP 3,0 (pompa di calore 60.000,00
kWh_e/anno), O&M alternativo 30.000
EUR/anno, CAPEX 450.000 EUR, fattore CO2
elettricita' 0,25 kg/kWh, fattore CO2 gas
0,20 kg/kWh_th, WACC 0,05 (frazione), vita
20 anni, tolleranza 0,10 (frazione del
CAPEX). Valori calcolati eseguendo
mh836_demo_calcoli(): E_base 480.000,00,
E_alt_lorda 340.000,00, recupero 85.000,00,
E_alt_netta_trazione 255.000,00, E_pv
132.000,00, autoconsumo 92.400,00,
E_alt_rete 162.600,00, esportata 39.600,00,
C_base 121.800,00, C_alt 78.972,00,
risparmio 42.828,00, CO2_base 156,00,
CO2_alt 55,65, CO2_evitata 100,35, VAN
83731,5445503024, TIR 7,106181555611609 %,
payback 11, e_spec_alt_max
1,498909090909091, verdetto CONVIENTE.

Destinazione nel repo: tests/test_w836_funivia.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from w838_helpers import (
    demo_calcoli,
    mh836_autoconsumo,
    mh836_c_alt,
    mh836_c_base,
    mh836_calcola,
    mh836_co2_alt,
    mh836_co2_base,
    mh836_co2_evitata,
    mh836_csv,
    mh836_demo,
    mh836_demo_calcoli,
    mh836_e_alt_lorda,
    mh836_e_alt_netta_trazione,
    mh836_e_alt_rete,
    mh836_e_base,
    mh836_e_esportata,
    mh836_e_pv,
    mh836_e_spec_alt_max,
    mh836_flussi,
    mh836_frazione,
    mh836_int_pos,
    mh836_nneg,
    mh836_num,
    mh836_payback,
    mh836_pos,
    mh836_recupero,
    mh836_risparmio,
    mh836_sensibilita,
    mh836_tir,
    mh836_valida,
    mh836_van,
    mh836_verdetto,
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


_HELPERS_PATH = _risolvi("w838_helpers.py")
_UI_PATH = _risolvi("w838_ui.py")


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
    "e_base_kwh_e_anno": 480000.0,
    "e_alt_lorda_kwh_e_anno": 340000.0,
    "recupero_kwh_e_anno": 85000.0,
    "e_alt_netta_trazione_kwh_e_anno": 255000.0,
    "e_pv_kwh_e_anno": 132000.0,
    "e_pv_auto_kwh_e_anno": 92400.0,
    "e_pv_exp_kwh_e_anno": 39600.0,
    "e_alt_rete_kwh_e_anno": 162600.0,
    "c_base_eur_anno": 121800.0,
    "c_alt_eur_anno": 78972.0,
    "risparmio_eur_anno": 42828.0,
    "co2_base_t_anno": 156.0,
    "co2_alt_t_anno": 55.65,
    "co2_evitata_t_anno": 100.35,
    "van": 83731.5445503024,
    "tir": 7.106181555611609,
    "payback": 11,
    "e_spec_alt_max": 1.498909090909091,
}


def _demo_kwargs(**over):
    kw = dict(mh836_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh836_num(3, "x"), 3.0)
        self.assertEqual(mh836_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh836_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh836_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh836_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh836_pos(0, "x")
        with self.assertRaises(ValueError):
            mh836_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh836_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh836_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh836_frazione(0, "quota"), 0.0)
        self.assertEqual(mh836_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh836_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh836_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_energie_base_lorda_recupero_netta(self):
        self.assertEqual(mh836_e_base(400000, 1.20), 480000.0)
        self.assertEqual(mh836_e_alt_lorda(400000, 0.85), 340000.0)
        self.assertEqual(mh836_recupero(340000.0, 0.25), 85000.0)
        self.assertEqual(mh836_e_alt_netta_trazione(340000.0, 85000.0), 255000.0)

    def test_recupero_zero_e_totale(self):
        self.assertEqual(mh836_recupero(340000.0, 0.0), 0.0)
        self.assertEqual(mh836_recupero(340000.0, 1.0), 340000.0)
        self.assertEqual(mh836_e_alt_netta_trazione(340000.0, 340000.0), 0.0)

    def test_pv_autoconsumo_cappato_alla_netta(self):
        self.assertEqual(mh836_e_pv(120, 1100), 132000.0)
        self.assertAlmostEqual(mh836_autoconsumo(132000.0, 0.70, 255000.0), 92400.0, places=6)
        self.assertEqual(mh836_autoconsumo(132000.0, 0.70, 50000.0), 50000.0)

    def test_e_alt_rete_e_esportata(self):
        self.assertEqual(mh836_e_alt_rete(255000.0, 92400.0), 162600.0)
        self.assertEqual(mh836_e_esportata(132000.0, 92400.0), 39600.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh836_c_base(480000.0, 0.22, 180000, 0.09), 121800.0, places=9)
        self.assertAlmostEqual(mh836_c_alt(162600.0, 0.22, 180000, 3.0, 30000), 78972.0, places=9)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh836_risparmio(121800.0, 78972.0), 42828.0, places=9)
        self.assertLess(mh836_risparmio(78972.0, 121800.0), 0.0)

    def test_co2_base_alt_evitata_fattori_separati(self):
        self.assertAlmostEqual(mh836_co2_base(480000.0, 0.25, 180000, 0.20), 156.0, places=9)
        self.assertAlmostEqual(mh836_co2_alt(162600.0, 0.25, 180000, 3.0), 55.65, places=9)
        self.assertAlmostEqual(mh836_co2_evitata(480000.0, 0.25, 180000, 0.20, 162600.0, 3.0), 100.35, places=9)

    def test_co2_evitata_negativa_non_clampata(self):
        self.assertEqual(mh836_co2_evitata(100.0, 0.25, 0, 0.20, 200.0, 3.0), -0.025)

    def test_rete_alt_minore_di_base_nel_demo(self):
        bc = mh836_demo_calcoli()
        self.assertLess(bc["e_alt_rete_kwh_e_anno"], bc["e_base_kwh_e_anno"])
        self.assertLess(bc["e_alt_netta_trazione_kwh_e_anno"], bc["e_base_kwh_e_anno"])

    def test_pv_esportato_senza_credito(self):
        bc = mh836_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_exp_kwh_e_anno"], 39600.0, places=6)
        self.assertAlmostEqual(bc["e_alt_rete_kwh_e_anno"],
                               bc["e_alt_netta_trazione_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"], places=9)
        # Se l'esportato avesse credito, il costo alternativo sarebbe piu' basso:
        # qui non lo e': il costo usa solo la rete.
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_alt_rete_kwh_e_anno"] * 0.22 + 180000 / 3.0 * 0.22 + 30000, places=6)


class TestFinanza(unittest.TestCase):
    def test_e_spec_alt_max_demo_valore(self):
        emax = mh836_e_spec_alt_max(121800.0, 400000, 0.25, 180000, 3.0, 30000, 0.22, 92400.0)
        self.assertAlmostEqual(emax, 1.498909090909091, places=12)

    def test_e_spec_alt_max_none_casi(self):
        self.assertIsNone(mh836_e_spec_alt_max(121800.0, 400000, 0.25, 180000, 3.0, 30000, 0.0, 92400.0))
        self.assertIsNone(mh836_e_spec_alt_max(121800.0, 400000, 1.0, 180000, 3.0, 30000, 0.22, 92400.0))
        self.assertIsNone(mh836_e_spec_alt_max(1000.0, 400000, 0.25, 180000, 3.0, 30000, 0.22, 92400.0))
        self.assertIsNone(mh836_e_spec_alt_max(40000.0, 400000, 0.25, 180000, 3.0, 30000, 0.22, 92400.0))

    def test_e_spec_alt_max_verifica_pareggio_su_demo(self):
        bc = mh836_demo_calcoli()
        emax = bc["e_spec_alt_max"]
        r = mh836_calcola(**_demo_kwargs(e_spec_alt=emax))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_e_spec_alt_max_soglia_massima_su_demo(self):
        bc = mh836_demo_calcoli()
        emax = bc["e_spec_alt_max"]
        self.assertGreater(mh836_calcola(**_demo_kwargs(e_spec_alt=emax - 0.1))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh836_calcola(**_demo_kwargs(e_spec_alt=emax + 0.1))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh836_flussi(450000, 42828.0, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -450000)
        self.assertTrue(all(f == 42828.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh836_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 83731.5445503024, places=6)
        self.assertAlmostEqual(mh836_van([-450000] + [42828.0] * 20, 0.0), 406560.0, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        # WACC 0,05 come frazione: VAN demo; se fosse percentuale
        # (5,0) il risultato sarebbe diverso e molto piu' basso.
        self.assertAlmostEqual(mh836_van([-450000] + [42828.0] * 20, 0.05), 83731.5445503024, places=6)
        self.assertLess(mh836_van([-450000] + [42828.0] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh836_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 7.106181555611609, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh836_payback([-450000] + [42828.0] * 20), 11)
        self.assertEqual(mh836_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh836_payback([-450000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh836_verdetto(42828.0, 100.0, 450000, 0.10), "CONVIENTE")
        self.assertEqual(mh836_verdetto(42828.0, -30000.0, 450000, 0.10), "MARGINALE")
        self.assertEqual(mh836_verdetto(42828.0, -100000.0, 450000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh836_verdetto(0.0, 100.0, 450000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh836_verdetto(-100.0, 100.0, 450000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh836_verdetto(None, 100.0, 450000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh836_verdetto(42828.0, 0.0, 450000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh836_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("passeggeri", "400000"), ("passeggeri", float("nan")),
                            ("passeggeri", float("inf")), ("passeggeri", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh836_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"passeggeri": 0}, {"passeggeri": -1},
                     {"e_spec_base": -0.1}, {"e_spec_alt": -0.1},
                     {"quota_recupero": -0.1}, {"quota_recupero": 1.1},
                     {"p_el": -0.1}, {"p_gas": -0.1}, {"q_gas": -1},
                     {"cop": 0}, {"cop": -1}, {"om_alt": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"quota_autoconsumo": -0.1}, {"quota_autoconsumo": 1.1},
                     {"capex": -1}, {"f_co2_el": -0.1}, {"f_co2_gas": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh836_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh836_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh836_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh836_valida(**_demo_kwargs(
            e_spec_base=0, e_spec_alt=0, quota_recupero=0,
            p_el=0, p_gas=0, q_gas=0, om_alt=0, p_pv_kwp=0,
            prod_specifica=0, quota_autoconsumo=0, capex=0,
            f_co2_el=0, f_co2_gas=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh836_demo()
        self.assertEqual(d["passeggeri"], 400000)
        self.assertEqual(d["e_spec_base"], 1.20)
        self.assertEqual(d["e_spec_alt"], 0.85)
        self.assertEqual(d["quota_recupero"], 0.25)
        self.assertEqual(d["p_el"], 0.22)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["q_gas"], 180000)
        self.assertEqual(d["cop"], 3.0)
        self.assertEqual(d["om_alt"], 30000)
        self.assertEqual(d["p_pv_kwp"], 120)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["quota_autoconsumo"], 0.70)
        self.assertEqual(d["capex"], 450000)
        self.assertEqual(d["f_co2_el"], 0.25)
        self.assertEqual(d["f_co2_gas"], 0.20)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh836_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh836_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], 480000.0, places=6)
        self.assertEqual(bc["e_alt_lorda_kwh_e_anno"], 340000.0)
        self.assertEqual(bc["recupero_kwh_e_anno"], 85000.0)
        self.assertEqual(bc["e_alt_netta_trazione_kwh_e_anno"], 255000.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 132000.0)
        self.assertEqual(bc["c_base_eur_anno"], 121800.0)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 78972.0, places=9)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh836_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[10], -21720.0, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[11], 21108.0, places=6)

    def test_demo_tabella_righe(self):
        bc = mh836_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Passeggeri (persone/anno)", voci)
        self.assertIn("Energia recuperata in frenata (kWh_e/anno)", voci)
        self.assertIn("Energia di rete alternativa (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico esportato, senza credito (kWh_e/anno)", voci)
        self.assertIn("Consumo specifico alternativo massimo (soglia massima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh836_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["passeggeri"] * bc["e_spec_base"])
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"],
                               bc["passeggeri"] * bc["e_spec_alt"])
        self.assertAlmostEqual(bc["e_alt_netta_trazione_kwh_e_anno"],
                               bc["e_alt_lorda_kwh_e_anno"] - bc["recupero_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_rete_kwh_e_anno"],
                               bc["e_alt_netta_trazione_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        eb = 400000 * 1.20
        ea = 400000 * 0.85
        rec = 0.25 * ea
        en = ea - rec
        e_pv = 120 * 1100
        auto = min(e_pv * 0.70, en)
        er = en - auto
        c_base = eb * 0.22 + 180000 * 0.09
        c_alt = er * 0.22 + 180000 / 3.0 * 0.22 + 30000
        bc = mh836_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], eb, places=6)
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"], ea, places=6)
        self.assertAlmostEqual(bc["recupero_kwh_e_anno"], rec, places=6)
        self.assertAlmostEqual(bc["e_alt_netta_trazione_kwh_e_anno"], en, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_alt_rete_kwh_e_anno"], er, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh836_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_elettricita_piu_meno_20(self):
        meno = mh836_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 31502.40000000001, places=6)
        self.assertAlmostEqual(meno["van"], -57410.46490516835, places=6)
        self.assertAlmostEqual(meno["tir"], 3.4440489653923656, places=6)
        self.assertEqual(meno["payback"], 15)
        self.assertEqual(meno["verdetto"], "NON_CONVIENTE")
        piu = mh836_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 54153.600000000006, places=6)
        self.assertAlmostEqual(piu["van"], 224873.55400577327, places=6)
        self.assertAlmostEqual(piu["tir"], 10.35783462443106, places=6)
        self.assertEqual(piu["payback"], 9)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_elettricita_alta_migliora_il_caso(self):
        demo = mh836_demo_calcoli()
        meno = mh836_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh836_calcola(**_demo_kwargs(p_el=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(demo["e_alt_rete_kwh_e_anno"], demo["e_base_kwh_e_anno"])

    def test_variante_senza_recupero(self):
        r = mh836_calcola(**_demo_kwargs(quota_recupero=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 24128.0, places=6)
        self.assertAlmostEqual(r["van"], -149311.78885519534, places=6)
        self.assertAlmostEqual(r["tir"], 0.6747364304547402, places=6)
        self.assertEqual(r["payback"], 19)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_senza_fotovoltaico(self):
        r = mh836_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 22500.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -169600.26729285036, places=6)
        self.assertAlmostEqual(r["tir"], 0.0, places=6)
        self.assertEqual(r["payback"], 20)

    def test_variante_cop_basso_ancora_convinte(self):
        r = mh836_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 36228.0, places=6)
        self.assertAlmostEqual(r["van"], 1480.956289538426, places=6)
        self.assertAlmostEqual(r["tir"], 5.038782574270212, places=6)
        self.assertEqual(r["payback"], 13)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_variante_capex_doppio_non_convinte(self):
        r = mh836_calcola(**_demo_kwargs(capex=900000))
        self.assertAlmostEqual(r["van"], -366268.4554496979, places=6)
        self.assertAlmostEqual(r["tir"], -0.4665917457185204, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh836_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -119293.53645287285, places=6)
        self.assertAlmostEqual(r["tir"], -0.8894952816296524, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh836_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 406560.0, places=6)
        self.assertEqual(zero["payback"], 11)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh836_sensibilita(**mh836_demo())
        self.assertEqual(set(s.keys()), {"el_meno20", "el_piu20", "rec_0",
                                         "senza_pv", "cop_2", "capex_doppio",
                                         "vita_10", "wacc_0"})
        self.assertAlmostEqual(s["el_meno20"]["risparmio_eur_anno"], 31502.40000000001, places=6)
        self.assertAlmostEqual(s["el_piu20"]["van"], 224873.55400577327, places=6)
        self.assertEqual(s["rec_0"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh836_demo_calcoli()
        b = mh836_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh836_demo()
        attese = {"passeggeri", "e_spec_base", "e_spec_alt",
                  "quota_recupero", "p_el", "p_gas", "q_gas",
                  "cop", "om_alt", "p_pv_kwp", "prod_specifica",
                  "quota_autoconsumo", "capex", "f_co2_el",
                  "f_co2_gas", "wacc", "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["passeggeri", "e_spec_base", "e_spec_alt",
                 "quota_recupero", "p_el", "p_gas", "q_gas",
                 "cop", "om_alt", "p_pv_kwp", "prod_specifica",
                 "quota_autoconsumo", "capex", "f_co2_el",
                 "f_co2_gas", "wacc", "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh836_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh836_calcola(**_demo_kwargs(quota_recupero=1.1))
        with self.assertRaises(ValueError):
            mh836_calcola(**_demo_kwargs(quota_autoconsumo=1.1))
        with self.assertRaises(ValueError):
            mh836_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("passeggeri", "400000"), ("passeggeri", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh836_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh836_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_autoconsumo=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_el=0, f_co2_gas=0))
        self.assertTrue(r["valid"])
        r2 = mh836_calcola(**_demo_kwargs(om_alt=30000, p_el=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh836_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        emax = mh836_demo_calcoli()["e_spec_alt_max"]
        r = mh836_calcola(**_demo_kwargs(e_spec_alt=emax))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh836_demo_calcoli()
        csv = mh836_csv(bc, dict(mh836_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh836_demo_calcoli()
        csv = mh836_csv(bc, dict(mh836_demo()))
        self.assertIn("risparmio_eur_anno;42828.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh836_demo_calcoli()
        csv = mh836_csv(bc, dict(mh836_demo()))
        for chiave in mh836_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh835_", src)
        self.assertNotIn("mh834_", src)
        self.assertNotIn("mh833_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab836:"), 1)
        self.assertTrue(src.startswith("    # W838"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Funivia: azionamento con recupero in frenata + motori efficienti + fotovoltaico in stazione", src)
        self.assertIn("🚡 Funivia: azionamento con recupero in frenata + motori efficienti + fotovoltaico in stazione battono azionamento tradizionale senza recupero + riscaldamento stazione a gas?", src)
        self.assertNotIn("tab835", src)
        self.assertNotIn("tab834", src)
        self.assertNotIn("tab833", src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn("streamlit", src)
        for vecchio in ("mh835_", "mh834_", "mh833_", "mh832_"):
            self.assertNotIn(vecchio, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn("mh835_", src)
        self.assertNotIn("st835_", src)
        self.assertNotIn("mh834_", src)
        self.assertNotIn("st834_", src)
        chiavi = re.findall(r'key="(st836_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st836_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st836_calcola"', src)
        self.assertIn('key="st836_csv"', src)
        self.assertIn('key="st836_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def836\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh836_demo().keys()), lette - set(mh836_demo().keys()))
        self.assertEqual(lette, set(mh836_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc836\['([^']+)'\]", src))
        attese = set(mh836_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg836"), src.index(".paiac("))
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
    def test_app_contiene_tab836_e_titolo(self):
        self.assertTrue(os.path.exists(_APP_PATH), f"app.py non trovato: {_APP_PATH} (apply tab836 non ancora fatto)")
        src = open(_APP_PATH, encoding="utf-8").read()
        self.assertIn("tab836", src)
        self.assertIn("🚡 Funivia: azionamento con recupero in frenata + motori efficienti + fotovoltaico in stazione battono azionamento tradizionale senza recupero + riscaldamento stazione a gas?", src)


if __name__ == "__main__":
    unittest.main()
