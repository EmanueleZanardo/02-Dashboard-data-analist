"""Test nuova scheda tab837 "Fungaia:
climatizzazione efficiente + recupero
calore aria esausta + fotovoltaico in
copertura + pompa di calore per
pastorizzazione battono climatizzazione
tradizionale + pastorizzazione
substrato a gas?".

Business case deterministico di una
fungaia guidata dalla PRODUZIONE in
kg/anno:
E_base = produzione x e_spec_base;
E_alt_lorda = produzione x e_spec_alt;
recupero = quota_recupero x E_alt_lorda
(calore aria esausta + free-cooling);
E_alt_netta_clima = E_alt_lorda -
recupero; E_pv = kWp x producibilita';
autoconsumo = min(E_pv x quota_autoconsumo,
E_alt_netta_clima) (cappato: E_alt_rete
non scende sotto zero); E_alt_rete =
E_alt_netta_clima - autoconsumo;
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
autoconsumo_saturo) / (produzione x
(1 - quota_recupero)) nel ramo autoconsumo
saturo, None se p_el <= 0, produzione
<= 0, quota_recupero >= 1, e_max < 0, o
ramo incoerente (produzione x e_max x
(1 - quota_recupero) < autoconsumo_saturo),
SOGLIA MASSIMA quando esiste (sotto di
essa l'alternativa vince sui costi, sopra
perde; e' dominata ANCHE dal valore della
pastorizzazione e dall'O&M, non solo
dall'elettricita' di climatizzazione). Per
p_el NON viene dichiarato alcun pareggio:
il pareggio dichiarato qui e' SOLO
e_spec_alt_max. Verdetto: NON_CALCOLABILE
se input degenere (produzione <= 0,
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
come negli helper dove previsto (produzione,
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
dalla serra riscaldata (luce solare e
fotosintesi: qui sale buie, umidita'
controllata e pastorizzazione substrato),
dal caseificio e dalla cantina vinicola
(freddo di processo alimentare: qui clima
di sale di coltivazione funghi +
pastorizzazione substrato) e dalla cella
frigorifera (solo freddo di conservazione:
qui clima + pastorizzazione + fotovoltaico):
qui driver PRODUZIONE + RECUPERO CALORE
ARIA ESAUSTA E FREE-COOLING +
CLIMATIZZAZIONE EFFICIENTE + FOTOVOLTAICO
IN COPERTURA + POMPA DI CALORE AD ALTA
TEMPERATURA PER PASTORIZZAZIONE.

Demo (fungaia): 300.000 kg/anno,
consumo specifico base 1,10 (energia base
330.000,00 kWh_e/anno) e alternativo 0,75
(energia alternativa lorda 225.000,00
kWh_e/anno), quota recupero 0,20
(recupero 45.000,00, netta di climatizzazione
180.000,00 kWh_e/anno), fotovoltaico
100 kWp a 1.100 kWh/kWp/anno (110.000,00
kWh_e/anno, autoconsumo 77.000,00,
esportato 33.000,00 senza credito),
energia di rete alternativa 103.000,00
kWh_e/anno, prezzo elettricita' 0,22
EUR/kWh, prezzo gas 0,09 EUR/kWh_th,
fabbisogno termico pastorizzazione
240.000 kWh_th/anno, COP 2,5 (pompa di
calore 96.000,00 kWh_e/anno), O&M
alternativo 25.000 EUR/anno, CAPEX
300.000 EUR, fattore CO2 elettricita'
0,25 kg/kWh, fattore CO2 gas 0,20
kg/kWh_th, WACC 0,05 (frazione), vita
20 anni, tolleranza 0,10 (frazione del
CAPEX). Valori calcolati eseguendo
mh837_demo_calcoli(): E_base 330.000,00,
E_alt_lorda 225.000,00, recupero 45.000,00,
E_alt_netta_clima 180.000,00, E_pv
110.000,00, autoconsumo 77.000,00,
E_alt_rete 103.000,00, esportata 33.000,00,
C_base 94.200,00, C_alt 68.780,00,
risparmio 25.420,00, CO2_base 130,50,
CO2_alt 49,75, CO2_evitata 80,75, VAN
16789,386907366294, TIR 5,651366303222116 %,
payback 12, e_spec_alt_max
1,2314393939393942, verdetto CONVIENTE.

Destinazione nel repo: tests/test_w837_fungaia.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w839_helpers import (
        demo_calcoli,
        mh837_autoconsumo,
        mh837_c_alt,
        mh837_c_base,
        mh837_calcola,
        mh837_co2_alt,
        mh837_co2_base,
        mh837_co2_evitata,
        mh837_csv,
        mh837_demo,
        mh837_demo_calcoli,
        mh837_e_alt_lorda,
        mh837_e_alt_netta_clima,
        mh837_e_alt_rete,
        mh837_e_base,
        mh837_e_esportata,
        mh837_e_pv,
        mh837_e_spec_alt_max,
        mh837_flussi,
        mh837_frazione,
        mh837_int_pos,
        mh837_nneg,
        mh837_num,
        mh837_payback,
        mh837_pos,
        mh837_recupero,
        mh837_risparmio,
        mh837_sensibilita,
        mh837_tir,
        mh837_valida,
        mh837_van,
        mh837_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w839_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w839_helpers", os.path.join(_hf, "w839_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh837_autoconsumo = _mod.mh837_autoconsumo
    mh837_c_alt = _mod.mh837_c_alt
    mh837_c_base = _mod.mh837_c_base
    mh837_calcola = _mod.mh837_calcola
    mh837_co2_alt = _mod.mh837_co2_alt
    mh837_co2_base = _mod.mh837_co2_base
    mh837_co2_evitata = _mod.mh837_co2_evitata
    mh837_csv = _mod.mh837_csv
    mh837_demo = _mod.mh837_demo
    mh837_demo_calcoli = _mod.mh837_demo_calcoli
    mh837_e_alt_lorda = _mod.mh837_e_alt_lorda
    mh837_e_alt_netta_clima = _mod.mh837_e_alt_netta_clima
    mh837_e_alt_rete = _mod.mh837_e_alt_rete
    mh837_e_base = _mod.mh837_e_base
    mh837_e_esportata = _mod.mh837_e_esportata
    mh837_e_pv = _mod.mh837_e_pv
    mh837_e_spec_alt_max = _mod.mh837_e_spec_alt_max
    mh837_flussi = _mod.mh837_flussi
    mh837_frazione = _mod.mh837_frazione
    mh837_int_pos = _mod.mh837_int_pos
    mh837_nneg = _mod.mh837_nneg
    mh837_num = _mod.mh837_num
    mh837_payback = _mod.mh837_payback
    mh837_pos = _mod.mh837_pos
    mh837_recupero = _mod.mh837_recupero
    mh837_risparmio = _mod.mh837_risparmio
    mh837_sensibilita = _mod.mh837_sensibilita
    mh837_tir = _mod.mh837_tir
    mh837_valida = _mod.mh837_valida
    mh837_van = _mod.mh837_van
    mh837_verdetto = _mod.mh837_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w839_helpers.py")
_UI_PATH = _risolvi("w839_ui.py")


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
    "e_base_kwh_e_anno": 330000.0,
    "e_alt_lorda_kwh_e_anno": 225000.0,
    "recupero_kwh_e_anno": 45000.0,
    "e_alt_netta_clima_kwh_e_anno": 180000.0,
    "e_pv_kwh_e_anno": 110000.0,
    "e_pv_auto_kwh_e_anno": 77000.0,
    "e_pv_exp_kwh_e_anno": 33000.0,
    "e_alt_rete_kwh_e_anno": 103000.0,
    "c_base_eur_anno": 94200.0,
    "c_alt_eur_anno": 68780.0,
    "risparmio_eur_anno": 25420.0,
    "co2_base_t_anno": 130.5,
    "co2_alt_t_anno": 49.75,
    "co2_evitata_t_anno": 80.75,
    "van": 16789.386907366294,
    "tir": 5.651366303222116,
    "payback": 12,
    "e_spec_alt_max": 1.2314393939393942,
}


def _demo_kwargs(**over):
    kw = dict(mh837_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh837_num(3, "x"), 3.0)
        self.assertEqual(mh837_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh837_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh837_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh837_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh837_pos(0, "x")
        with self.assertRaises(ValueError):
            mh837_pos(-1, "x")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh837_int_pos(20.0, "vita"), 20)
        with self.assertRaises(ValueError):
            mh837_int_pos(20.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh837_frazione(0, "quota"), 0.0)
        self.assertEqual(mh837_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh837_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh837_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_energie_base_lorda_recupero_netta(self):
        self.assertEqual(mh837_e_base(400000, 1.20), 480000.0)
        self.assertEqual(mh837_e_alt_lorda(400000, 0.85), 340000.0)
        self.assertEqual(mh837_recupero(340000.0, 0.25), 85000.0)
        self.assertEqual(mh837_e_alt_netta_clima(340000.0, 85000.0), 255000.0)

    def test_recupero_zero_e_totale(self):
        self.assertEqual(mh837_recupero(340000.0, 0.0), 0.0)
        self.assertEqual(mh837_recupero(340000.0, 1.0), 340000.0)
        self.assertEqual(mh837_e_alt_netta_clima(340000.0, 340000.0), 0.0)

    def test_pv_autoconsumo_cappato_alla_netta(self):
        self.assertEqual(mh837_e_pv(120, 1100), 132000.0)
        self.assertAlmostEqual(mh837_autoconsumo(132000.0, 0.70, 255000.0), 92400.0, places=6)
        self.assertEqual(mh837_autoconsumo(132000.0, 0.70, 50000.0), 50000.0)

    def test_e_alt_rete_e_esportata(self):
        self.assertEqual(mh837_e_alt_rete(255000.0, 92400.0), 162600.0)
        self.assertEqual(mh837_e_esportata(132000.0, 92400.0), 39600.0)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh837_c_base(480000.0, 0.22, 180000, 0.09), 121800.0, places=9)
        self.assertAlmostEqual(mh837_c_alt(162600.0, 0.22, 180000, 3.0, 30000), 78972.0, places=9)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh837_risparmio(121800.0, 78972.0), 42828.0, places=9)
        self.assertLess(mh837_risparmio(78972.0, 121800.0), 0.0)

    def test_co2_base_alt_evitata_fattori_separati(self):
        self.assertAlmostEqual(mh837_co2_base(480000.0, 0.25, 180000, 0.20), 156.0, places=9)
        self.assertAlmostEqual(mh837_co2_alt(162600.0, 0.25, 180000, 3.0), 55.65, places=9)
        self.assertAlmostEqual(mh837_co2_evitata(480000.0, 0.25, 180000, 0.20, 162600.0, 3.0), 100.35, places=9)

    def test_co2_evitata_negativa_non_clampata(self):
        self.assertEqual(mh837_co2_evitata(100.0, 0.25, 0, 0.20, 200.0, 3.0), -0.025)

    def test_rete_alt_minore_di_base_nel_demo(self):
        bc = mh837_demo_calcoli()
        self.assertLess(bc["e_alt_rete_kwh_e_anno"], bc["e_base_kwh_e_anno"])
        self.assertLess(bc["e_alt_netta_clima_kwh_e_anno"], bc["e_base_kwh_e_anno"])

    def test_pv_esportato_senza_credito(self):
        bc = mh837_demo_calcoli()
        self.assertAlmostEqual(bc["e_pv_exp_kwh_e_anno"], 33000.0, places=6)
        self.assertAlmostEqual(bc["e_alt_rete_kwh_e_anno"],
                               bc["e_alt_netta_clima_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"], places=9)
        # Se l'esportato avesse credito, il costo alternativo sarebbe piu' basso:
        # qui non lo e': il costo usa solo la rete.
        self.assertAlmostEqual(bc["c_alt_eur_anno"],
                               bc["e_alt_rete_kwh_e_anno"] * 0.22 + 240000 / 2.5 * 0.22 + 25000, places=6)


class TestFinanza(unittest.TestCase):
    def test_e_spec_alt_max_demo_valore(self):
        emax = mh837_e_spec_alt_max(94200.0, 300000, 0.20, 240000, 2.5, 25000, 0.22, 77000.0)
        self.assertAlmostEqual(emax, 1.2314393939393942, places=12)

    def test_e_spec_alt_max_none_casi(self):
        self.assertIsNone(mh837_e_spec_alt_max(94200.0, 300000, 0.20, 240000, 2.5, 25000, 0.0, 77000.0))
        self.assertIsNone(mh837_e_spec_alt_max(94200.0, 300000, 1.0, 240000, 2.5, 25000, 0.22, 77000.0))
        self.assertIsNone(mh837_e_spec_alt_max(1000.0, 300000, 0.20, 240000, 2.5, 25000, 0.22, 77000.0))
        self.assertIsNone(mh837_e_spec_alt_max(40000.0, 300000, 0.20, 240000, 2.5, 25000, 0.22, 77000.0))

    def test_e_spec_alt_max_verifica_pareggio_su_demo(self):
        bc = mh837_demo_calcoli()
        emax = bc["e_spec_alt_max"]
        r = mh837_calcola(**_demo_kwargs(e_spec_alt=emax))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_e_spec_alt_max_soglia_massima_su_demo(self):
        bc = mh837_demo_calcoli()
        emax = bc["e_spec_alt_max"]
        self.assertGreater(mh837_calcola(**_demo_kwargs(e_spec_alt=emax - 0.1))["risparmio_eur_anno"], 0.0)
        self.assertLess(mh837_calcola(**_demo_kwargs(e_spec_alt=emax + 0.1))["risparmio_eur_anno"], 0.0)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh837_flussi(300000, 25420.0, 20)
        self.assertEqual(len(flussi), 21)
        self.assertEqual(flussi[0], -300000)
        self.assertTrue(all(f == 25420.0 for f in flussi[1:]))

    def test_van_demo_e_zero_wacc(self):
        bc = mh837_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 16789.386907366294, places=6)
        self.assertAlmostEqual(mh837_van([-300000] + [25420.0] * 20, 0.0), 208400.0, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        # WACC 0,05 come frazione: VAN demo; se fosse percentuale
        # (5,0) il risultato sarebbe diverso e molto piu' basso.
        self.assertAlmostEqual(mh837_van([-300000] + [25420.0] * 20, 0.05), 16789.386907366294, places=6)
        self.assertLess(mh837_van([-300000] + [25420.0] * 20, 5.0), 0.0)

    def test_tir_demo(self):
        bc = mh837_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 5.651366303222116, places=6)
        self.assertGreater(bc["tir"], 5.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh837_payback([-300000] + [25420.0] * 20), 12)
        self.assertEqual(mh837_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh837_payback([-300000] + [100.0] * 20))

    def test_verdetto_frazione(self):
        self.assertEqual(mh837_verdetto(25420.0, 100.0, 300000, 0.10), "CONVIENTE")
        self.assertEqual(mh837_verdetto(25420.0, -20000.0, 300000, 0.10), "MARGINALE")
        self.assertEqual(mh837_verdetto(25420.0, -100000.0, 300000, 0.10), "NON_CONVIENTE")
        self.assertEqual(mh837_verdetto(0.0, 100.0, 300000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh837_verdetto(-100.0, 100.0, 300000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh837_verdetto(None, 100.0, 300000, 0.10), "NON_CALCOLABILE")
        self.assertEqual(mh837_verdetto(25420.0, 0.0, 300000, 0.10), "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh837_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("produzione", "400000"), ("produzione", float("nan")),
                            ("produzione", float("inf")), ("produzione", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh837_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"produzione": 0}, {"produzione": -1},
                     {"e_spec_base": -0.1}, {"e_spec_alt": -0.1},
                     {"quota_recupero": -0.1}, {"quota_recupero": 1.1},
                     {"p_el": -0.1}, {"p_gas": -0.1}, {"q_gas": -1},
                     {"cop": 0}, {"cop": -1}, {"om_alt": -1},
                     {"p_pv_kwp": -1}, {"prod_specifica": -1},
                     {"quota_autoconsumo": -0.1}, {"quota_autoconsumo": 1.1},
                     {"capex": -1}, {"f_co2_el": -0.1}, {"f_co2_gas": -0.1},
                     {"wacc": -0.1}, {"vita": 0}, {"vita": 20.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh837_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza(self):
        self.assertTrue(mh837_valida(**_demo_kwargs(wacc=0.25))["valido"])
        self.assertTrue(mh837_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh837_valida(**_demo_kwargs(
            e_spec_base=0, e_spec_alt=0, quota_recupero=0,
            p_el=0, p_gas=0, q_gas=0, om_alt=0, p_pv_kwp=0,
            prod_specifica=0, quota_autoconsumo=0, capex=0,
            f_co2_el=0, f_co2_gas=0, wacc=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh837_demo()
        self.assertEqual(d["produzione"], 300000)
        self.assertEqual(d["e_spec_base"], 1.10)
        self.assertEqual(d["e_spec_alt"], 0.75)
        self.assertEqual(d["quota_recupero"], 0.20)
        self.assertEqual(d["p_el"], 0.22)
        self.assertEqual(d["p_gas"], 0.09)
        self.assertEqual(d["q_gas"], 240000)
        self.assertEqual(d["cop"], 2.5)
        self.assertEqual(d["om_alt"], 25000)
        self.assertEqual(d["p_pv_kwp"], 100)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["quota_autoconsumo"], 0.70)
        self.assertEqual(d["capex"], 300000)
        self.assertEqual(d["f_co2_el"], 0.25)
        self.assertEqual(d["f_co2_gas"], 0.20)
        self.assertEqual(d["wacc"], 0.05)
        self.assertEqual(d["vita"], 20)
        self.assertEqual(d["tolleranza"], 0.10)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh837_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh837_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], 330000.0, places=6)
        self.assertEqual(bc["e_alt_lorda_kwh_e_anno"], 225000.0)
        self.assertEqual(bc["recupero_kwh_e_anno"], 45000.0)
        self.assertEqual(bc["e_alt_netta_clima_kwh_e_anno"], 180000.0)
        self.assertEqual(bc["e_pv_kwh_e_anno"], 110000.0)
        self.assertEqual(bc["c_base_eur_anno"], 94200.0)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 68780.0, places=9)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh837_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 21)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[10], -45800.0, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[11], -20380.0, places=6)

    def test_demo_tabella_righe(self):
        bc = mh837_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Produzione (kg/anno)", voci)
        self.assertIn("Energia recuperata da calore aria esausta + free-cooling (kWh_e/anno)", voci)
        self.assertIn("Energia di rete alternativa (kWh_e/anno)", voci)
        self.assertIn("Fotovoltaico esportato, senza credito (kWh_e/anno)", voci)
        self.assertIn("Consumo specifico alternativo massimo (soglia massima)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh837_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["produzione"] * bc["e_spec_base"])
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"],
                               bc["produzione"] * bc["e_spec_alt"])
        self.assertAlmostEqual(bc["e_alt_netta_clima_kwh_e_anno"],
                               bc["e_alt_lorda_kwh_e_anno"] - bc["recupero_kwh_e_anno"])
        self.assertAlmostEqual(bc["e_alt_rete_kwh_e_anno"],
                               bc["e_alt_netta_clima_kwh_e_anno"] - bc["e_pv_auto_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])

    def test_demo_contro_riconteggio_indipendente(self):
        eb = 300000 * 1.10
        ea = 300000 * 0.75
        rec = 0.20 * ea
        en = ea - rec
        e_pv = 100 * 1100
        auto = min(e_pv * 0.70, en)
        er = en - auto
        c_base = eb * 0.22 + 240000 * 0.09
        c_alt = er * 0.22 + 240000 / 2.5 * 0.22 + 25000
        bc = mh837_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], eb, places=6)
        self.assertAlmostEqual(bc["e_alt_lorda_kwh_e_anno"], ea, places=6)
        self.assertAlmostEqual(bc["recupero_kwh_e_anno"], rec, places=6)
        self.assertAlmostEqual(bc["e_alt_netta_clima_kwh_e_anno"], en, places=6)
        self.assertAlmostEqual(bc["e_pv_kwh_e_anno"], e_pv, places=6)
        self.assertAlmostEqual(bc["e_alt_rete_kwh_e_anno"], er, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt, places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh837_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_elettricita_piu_meno_20(self):
        meno = mh837_calcola(**_demo_kwargs(p_el=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 19656.0, places=6)
        self.assertAlmostEqual(meno["van"], -55042.79350703411, places=6)
        self.assertAlmostEqual(meno["tir"], 2.725261732119006, places=6)
        self.assertEqual(meno["payback"], 16)
        self.assertEqual(meno["verdetto"], "NON_CONVIENTE")
        piu = mh837_calcola(**_demo_kwargs(p_el=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 31184.0, places=6)
        self.assertAlmostEqual(piu["van"], 88621.56732176681, places=6)
        self.assertAlmostEqual(piu["tir"], 8.27516724403125, places=6)
        self.assertEqual(piu["payback"], 10)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_elettricita_alta_migliora_il_caso(self):
        demo = mh837_demo_calcoli()
        meno = mh837_calcola(**_demo_kwargs(p_el=0.176))
        piu = mh837_calcola(**_demo_kwargs(p_el=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertLess(demo["e_alt_rete_kwh_e_anno"], demo["e_base_kwh_e_anno"])

    def test_variante_senza_recupero(self):
        r = mh837_calcola(**_demo_kwargs(quota_recupero=0.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 15520.0, places=6)
        self.assertAlmostEqual(r["van"], -106586.49548377952, places=6)
        self.assertAlmostEqual(r["tir"], 0.32678289331903143, places=6)
        self.assertEqual(r["payback"], 20)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_senza_fotovoltaico(self):
        r = mh837_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 8480.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")
        self.assertAlmostEqual(r["van"], -194320.45629526096, places=6)
        self.assertAlmostEqual(r["tir"], -4.909325016324888, places=6)
        self.assertIsNone(r["payback"])

    def test_variante_cop_basso_non_convinte(self):
        r = mh837_calcola(**_demo_kwargs(cop=2.0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 20140.0, places=6)
        self.assertAlmostEqual(r["van"], -49011.08370124479, places=6)
        self.assertAlmostEqual(r["tir"], 2.9867403243491104, places=6)
        self.assertEqual(r["payback"], 15)
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_capex_doppio_non_convinte(self):
        r = mh837_calcola(**_demo_kwargs(capex=600000))
        self.assertAlmostEqual(r["van"], -283210.61309263366, places=6)
        self.assertAlmostEqual(r["tir"], -1.5283944687360558, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_vita_10_non_convinte(self):
        r = mh837_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], -103713.49810012215, places=6)
        self.assertAlmostEqual(r["tir"], -2.9039359503170243, places=6)
        self.assertIsNone(r["payback"])
        self.assertEqual(r["verdetto"], "NON_CONVIENTE")

    def test_variante_wacc_zero(self):
        zero = mh837_calcola(**_demo_kwargs(wacc=0.0))
        self.assertAlmostEqual(zero["van"], 208400.0, places=6)
        self.assertEqual(zero["payback"], 12)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh837_sensibilita(**mh837_demo())
        self.assertEqual(set(s.keys()), {"el_meno20", "el_piu20", "rec_0",
                                         "senza_pv", "cop_2", "capex_doppio",
                                         "vita_10", "wacc_0"})
        self.assertAlmostEqual(s["el_meno20"]["risparmio_eur_anno"], 19656.0, places=6)
        self.assertAlmostEqual(s["el_piu20"]["van"], 88621.56732176681, places=6)
        self.assertEqual(s["rec_0"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["senza_pv"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["cop_2"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "NON_CONVIENTE")
        self.assertEqual(s["wacc_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh837_demo_calcoli()
        b = mh837_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh837_demo()
        attese = {"produzione", "e_spec_base", "e_spec_alt",
                  "quota_recupero", "p_el", "p_gas", "q_gas",
                  "cop", "om_alt", "p_pv_kwp", "prod_specifica",
                  "quota_autoconsumo", "capex", "f_co2_el",
                  "f_co2_gas", "wacc", "vita", "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["produzione", "e_spec_base", "e_spec_alt",
                 "quota_recupero", "p_el", "p_gas", "q_gas",
                 "cop", "om_alt", "p_pv_kwp", "prod_specifica",
                 "quota_autoconsumo", "capex", "f_co2_el",
                 "f_co2_gas", "wacc", "vita", "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh837_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_e_cop_zero(self):
        with self.assertRaises(ValueError):
            mh837_calcola(**_demo_kwargs(quota_recupero=1.1))
        with self.assertRaises(ValueError):
            mh837_calcola(**_demo_kwargs(quota_autoconsumo=1.1))
        with self.assertRaises(ValueError):
            mh837_calcola(**_demo_kwargs(cop=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("produzione", "400000"), ("produzione", float("nan")),
                           ("capex", float("inf")), ("p_el", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh837_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh837_calcola(**_demo_kwargs(p_pv_kwp=0,
                                         prod_specifica=0, quota_autoconsumo=0,
                                         om_alt=0, wacc=0, tolleranza=0,
                                         capex=0, f_co2_el=0, f_co2_gas=0))
        self.assertTrue(r["valid"])
        r2 = mh837_calcola(**_demo_kwargs(om_alt=30000, p_el=0.0001))
        self.assertTrue(r2["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh837_calcola(**_demo_kwargs(om_alt=200000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)

    def test_pareggio_esatto_soglia(self):
        emax = mh837_demo_calcoli()["e_spec_alt_max"]
        r = mh837_calcola(**_demo_kwargs(e_spec_alt=emax))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh837_demo_calcoli()
        csv = mh837_csv(bc, dict(mh837_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh837_demo_calcoli()
        csv = mh837_csv(bc, dict(mh837_demo()))
        self.assertIn("risparmio_eur_anno;25420.0", csv)
        self.assertIn("verdetto;CONVIENTE", csv)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh837_demo_calcoli()
        csv = mh837_csv(bc, dict(mh837_demo()))
        for chiave in mh837_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn("mh836_", src)
        self.assertNotIn("mh835_", src)
        self.assertNotIn("mh834_", src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab837:"), 1)
        self.assertTrue(src.startswith("    # W839"))

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Fungaia: climatizzazione efficiente + recupero calore aria esausta + fotovoltaico in copertura + pompa di calore per pastorizzazione", src)
        self.assertIn("🍄 Fungaia: climatizzazione efficiente + recupero calore aria esausta + fotovoltaico in copertura + pompa di calore per pastorizzazione battono climatizzazione tradizionale + pastorizzazione substrato a gas?", src)
        self.assertNotIn("tab836", src)
        self.assertNotIn("tab835", src)
        self.assertNotIn("tab834", src)

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
        self.assertNotIn("mh836_", src)
        self.assertNotIn("st836_", src)
        self.assertNotIn("mh835_", src)
        self.assertNotIn("st835_", src)
        chiavi = re.findall(r'key="(st837_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st837_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st837_calcola"', src)
        self.assertIn('key="st837_csv"', src)
        self.assertIn('key="st837_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def837\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh837_demo().keys()), lette - set(mh837_demo().keys()))
        self.assertEqual(lette, set(mh837_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc837\['([^']+)'\]", src))
        attese = set(mh837_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg837"), src.index(".paiac("))
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
    def test_app_contiene_tab837_e_titolo(self):
        self.assertTrue(os.path.exists(_APP_PATH), f"app.py non trovato: {_APP_PATH} (apply tab837 non ancora fatto)")
        src = open(_APP_PATH, encoding="utf-8").read()
        self.assertIn("tab837", src)
        self.assertIn("🍄 Fungaia: climatizzazione efficiente + recupero calore aria esausta + fotovoltaico in copertura + pompa di calore per pastorizzazione battono climatizzazione tradizionale + pastorizzazione substrato a gas?", src)


if __name__ == "__main__":
    unittest.main()
