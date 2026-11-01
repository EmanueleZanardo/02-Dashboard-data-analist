"""Test nuova scheda tab845 "Impianto di depurazione:
soffianti ad alta efficienza + fotovoltaico
+ biogas da digestione anaerobica battono
soffianti tradizionali + rete?".

Business case annuo di un impianto di
depurazione, connesso alla rete, guidato
da PORTATA TRATTATA x COD INFLUENTE +
ENERGIA SPECIFICA (non da superfici,
camere, coperti o pallet):
COD_kg_giorno = portata x COD / 1000;
E_base = portata x 365 x e_specifica;
aerazione = E_base x share_aerazione;
resto = E_base x (1 - share_aerazione);
aerazione_alt = aerazione x
(1 - risparmio_soffianti);
E_alt_domanda = aerazione_alt + resto;
COD_rimosso = COD_kg_giorno x rimozione;
biogas = COD_rimosso x 365 x resa;
elettricita_biogas = biogas x share_CH4
x PCI_CH4 x eta_el_cogen;
E_fv = kWp x producibilita';
produzione = E_fv + elettricita_biogas;
autoconsumo = min(E_alt_domanda,
produzione); deficit = E_alt_domanda -
autoconsumo (prelevato da rete a prezzo
di prelievo); immessa = produzione -
autoconsumo (tutta la produzione
eccedente va immessa come ricavo allo
stesso prezzo di immissione; niente
batteria in questa scheda, quindi niente
perdite round-trip); C_base = E_base x
p_prelievo; C_alt = deficit x p_prelievo
- immessa x p_immissione + opex_alt
(l'immissione e' un ricavo, segno
meno); risparmio = C_base - C_alt;
CAPEX = capex_fv x kWp + capex_soffianti
+ capex_digestore_cogen (forfettario);
CO2 base = E_base x f_el / 1000; CO2 alt
= deficit x f_el / 1000 (l'elettricita'
da biogas e' conteggiata a CO2 netta
zero); CO2 evitata = base - alt (segno
libero, non clampata);
flussi [-CAPEX, risparmio x vita];
VAN al tasso (FRAZIONE, non percentuale);
TIR per bisezione; payback (primo anno
con cumulato >= 0); prezzo di prelievo
di pareggio p_star = (opex_alt - immessa
x p_immissione) / (E_base - deficit) in
forma chiusa a prezzo di immissione e
OPEX FERMI, None se E_base - deficit
<= 0 o se p_star < 0, SOGLIA sui soli
costi annui quando esiste (sopra di
essa l'alternativa vince, sotto perde;
il CAPEX non entra nel pareggio annuo).
Nel demo p_star e' 0,010256368599774713
EUR/kWh: una soglia bassissima, perche'
il risparmio e' enorme rispetto
all'OPEX alternativo; a p_star il
risparmio e' zero e il verdetto e'
NON_CALCOLABILE, a p_star + 0,01 il
risparmio e' 14.625,06 EUR/anno, a
p_star - 0,01 e' -14.625,06 EUR/anno.
Verdetto: NON_CALCOLABILE se input
degenere (portata <= 0, COD < 0,
e_specifica < 0, share_aerazione < 0
o > 1, risparmio_soffianti < 0 o > 1,
rimozione_COD < 0 o > 1, resa_biogas
< 0, share_CH4 < 0 o > 1, PCI_CH4 < 0,
eta_el_cogen <= 0 o > 1, kWp < 0,
producibilita' < 0, prezzi < 0,
opex_alt < 0, capex voci < 0, f_el < 0,
tasso < 0, vita <= 0 o non intera,
tolleranza < 0) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa
entro tolleranza FRAZIONE del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Guard UI IDENTICA agli
helper: nessuna divergenza di verdetto.
Tutti gli slider UI hanno minimo 0,
quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0
raggiungibili via slider sono bloccati in
UI esattamente come negli helper dove
previsto (portata, vita, eta_el_cogen).
Gli zeri ammessi in entrambi (COD,
e_specifica, quote, frazioni, resa, PCI,
kWp, producibilita', prezzi, opex, capex
voci, f_el, tasso, tolleranza) non
creano divergenza. Quote e frazioni > 1
e eta_el_cogen > 1 sono degeneri in
entrambi ma non raggiungibili via slider
(tetto 1,0). Tasso sopra 0,20 e
tolleranza sopra 1,0 sono ammessi negli
helper e limitati solo dagli slider UI
(0,20 e 1,0): nessuna divergenza nel
range raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper.

Demo (impianto di depurazione): portata
10.000 m3/giorno, COD 400 mg/L (carico
4.000 kg COD/giorno), e_specifica 0,45
kWh/m3 (E_base 1.642.500), share
aerazione 0,55 (aerazione 903.375, resto
739.125), risparmio soffianti 0,25
(aerazione alt 677.531,25, domanda alt
1.416.656,25), rimozione COD 0,85
(3.400 kg/giorno), resa biogas 0,35
(434.350 m3/anno), share CH4 0,60,
PCI CH4 9,94 kWh/m3, eta_el_cogen 0,35
(elettricita' biogas 906.662,19),
fotovoltaico 300 kWp a 1.100
kWh/kWp/anno (330.000), produzione
1.236.662,19, autoconsumo 1.236.662,19,
deficit 179.994,06, immessa 0, C_base
361.350, C_alt 54.598,69, risparmio
306.751,31, CAPEX voci: FV 900 EUR/kWp
(270.000), soffianti 80.000, digestore e
cogen 250.000 (totale 600.000), f_el
0,35 kg/kWh_e, tasso 0,06 (frazione),
vita 15 anni, tolleranza 0,05 (frazione
del CAPEX).
Valori calcolati eseguendo
mh845_demo_calcoli(): COD_kg_giorno
4000,0, E_base 1642500,0, aerazione
903375,0, resto 739125,0, aerazione_alt
677531,25, E_alt_domanda 1416656,25,
COD_rimosso 3400,0, biogas 434350,0,
e_biogas 906662,19, E_fv 330000,0,
produzione 1236662,19, autoconsumo
1236662,19, deficit 179994,06, immessa
0,0, C_base 361350,0, C_alt
54598,6932, risparmio 306751,3068,
CAPEX tot 600000,0, CO2 base 574,875,
CO2 alt 62,997921, CO2 evitata
511,877079, VAN 2379245,068956523, TIR
51,01974777172603 %, payback 2,
p_prelievo_pareggio
0,010256368599774713, verdetto
CONVIENTE (VAN quasi quattro volte il
CAPEX).

NOTA SUL TEST DI PRESENZA IN APP.PY: il
test di presenza tab845 in app.py e il
count-assert sui 845 tab NON sono
inclusi in questo file perche' questo
authoring e' SOLO authoring (niente
apply, niente push, repo non toccato):
la verifica di presenza e del conteggio
in app.py spetta alla fase di apply del
worker, non a questa fase. Tutti i test
qui inclusi passano da hidden_files
senza app.py. La forma del count in
questa fase e' strutturale: il blocco UI
apre tab845 esattamente una volta e gli
helper definiscono le funzioni mh845.

Destinazione nel repo: tests/test_w845_depurazione.py
"""


import ast
import os
import re
import sys
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w848_helpers import (
        demo_calcoli,
        mh845_aerazione,
        mh845_aerazione_alt,
        mh845_autoconsumo,
        mh845_biogas_m3_anno,
        mh845_c_alt,
        mh845_c_base,
        mh845_calcola,
        mh845_capex_totale,
        mh845_cod_kg_giorno,
        mh845_cod_rimosso,
        mh845_co2,
        mh845_co2_evitata,
        mh845_csv,
        mh845_deficit,
        mh845_demo,
        mh845_demo_calcoli,
        mh845_e_alt_domanda,
        mh845_e_base,
        mh845_e_biogas,
        mh845_e_fv,
        mh845_eta,
        mh845_frazione,
        mh845_flussi,
        mh845_immessa,
        mh845_int_pos,
        mh845_nneg,
        mh845_num,
        mh845_p_prelievo_pareggio,
        mh845_payback,
        mh845_pos,
        mh845_produzione,
        mh845_resto,
        mh845_risparmio,
        mh845_sensibilita,
        mh845_tir,
        mh845_valida,
        mh845_van,
        mh845_verdetto,
    )
except ModuleNotFoundError:
    # Fallback hidden_files (schema w826 _leggi): da repo
    # w848_helpers.py non e' importabile, si carica dal percorso
    # assoluto degli artefatti del ciclo.
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w848_helpers", os.path.join(_hf, "w848_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh845_aerazione = _mod.mh845_aerazione
    mh845_aerazione_alt = _mod.mh845_aerazione_alt
    mh845_autoconsumo = _mod.mh845_autoconsumo
    mh845_biogas_m3_anno = _mod.mh845_biogas_m3_anno
    mh845_c_alt = _mod.mh845_c_alt
    mh845_c_base = _mod.mh845_c_base
    mh845_calcola = _mod.mh845_calcola
    mh845_capex_totale = _mod.mh845_capex_totale
    mh845_cod_kg_giorno = _mod.mh845_cod_kg_giorno
    mh845_cod_rimosso = _mod.mh845_cod_rimosso
    mh845_co2 = _mod.mh845_co2
    mh845_co2_evitata = _mod.mh845_co2_evitata
    mh845_csv = _mod.mh845_csv
    mh845_deficit = _mod.mh845_deficit
    mh845_demo = _mod.mh845_demo
    mh845_demo_calcoli = _mod.mh845_demo_calcoli
    mh845_e_alt_domanda = _mod.mh845_e_alt_domanda
    mh845_e_base = _mod.mh845_e_base
    mh845_e_biogas = _mod.mh845_e_biogas
    mh845_e_fv = _mod.mh845_e_fv
    mh845_eta = _mod.mh845_eta
    mh845_frazione = _mod.mh845_frazione
    mh845_flussi = _mod.mh845_flussi
    mh845_immessa = _mod.mh845_immessa
    mh845_int_pos = _mod.mh845_int_pos
    mh845_nneg = _mod.mh845_nneg
    mh845_num = _mod.mh845_num
    mh845_p_prelievo_pareggio = _mod.mh845_p_prelievo_pareggio
    mh845_payback = _mod.mh845_payback
    mh845_pos = _mod.mh845_pos
    mh845_produzione = _mod.mh845_produzione
    mh845_resto = _mod.mh845_resto
    mh845_risparmio = _mod.mh845_risparmio
    mh845_sensibilita = _mod.mh845_sensibilita
    mh845_tir = _mod.mh845_tir
    mh845_valida = _mod.mh845_valida
    mh845_van = _mod.mh845_van
    mh845_verdetto = _mod.mh845_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w848_helpers.py")
_UI_PATH = _risolvi("w848_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# tab precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh84" + "4_"
_VECCHIO_TAB = "tab84" + "4"
_VECCHIO_ST = "st84" + "4_"

_DEMO = {
    "cod_kg_giorno": 4000.0,
    "e_base_kwh_e_anno": 1642500.0,
    "aerazione_kwh_e_anno": 903375.0,
    "resto_kwh_e_anno": 739125.0,
    "aerazione_alt_kwh_e_anno": 677531.25,
    "e_alt_domanda_kwh_e_anno": 1416656.25,
    "cod_rimosso_kg_giorno": 3400.0,
    "biogas_m3_anno": 434350.0,
    "e_biogas_kwh_e_anno": 906662.19,
    "e_fv_kwh_e_anno": 330000.0,
    "produzione_kwh_e_anno": 1236662.19,
    "autoconsumo_kwh_e_anno": 1236662.19,
    "deficit_kwh_e_anno": 179994.06,
    "immessa_kwh_e_anno": 0.0,
    "c_base_eur_anno": 361350.0,
    "c_alt_eur_anno": 54598.6932,
    "risparmio_eur_anno": 306751.3068,
    "capex_totale_eur": 600000.0,
    "co2_base_t_anno": 574.875,
    "co2_alt_t_anno": 62.997921,
    "co2_evitata_t_anno": 511.877079,
    "van": 2379245.068956523,
    "tir": 51.01974777172603,
    "payback": 2,
    "p_prelievo_pareggio": 0.010256368599774713,
}


def _demo_kwargs(**over):
    kw = dict(mh845_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh845_num(3, "x"), 3.0)
        self.assertEqual(mh845_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for bad in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh845_num(bad, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh845_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh845_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh845_pos(0, "x")
        with self.assertRaises(ValueError):
            mh845_pos(-1, "x")

    def test_eta_limiti(self):
        self.assertEqual(mh845_eta(1.0, "eta"), 1.0)
        self.assertEqual(mh845_eta(0.35, "eta"), 0.35)
        with self.assertRaises(ValueError):
            mh845_eta(0, "eta")
        with self.assertRaises(ValueError):
            mh845_eta(-0.1, "eta")
        with self.assertRaises(ValueError):
            mh845_eta(1.1, "eta")

    def test_int_pos_float_intero_ok_frazionario_no(self):
        self.assertEqual(mh845_int_pos(15.0, "vita"), 15)
        with self.assertRaises(ValueError):
            mh845_int_pos(15.5, "vita")

    def test_frazione_limiti(self):
        self.assertEqual(mh845_frazione(0, "quota"), 0.0)
        self.assertEqual(mh845_frazione(1, "quota"), 1.0)
        with self.assertRaises(ValueError):
            mh845_frazione(-0.1, "quota")
        with self.assertRaises(ValueError):
            mh845_frazione(1.1, "quota")


class TestFisica(unittest.TestCase):
    def test_cod_e_base(self):
        self.assertEqual(mh845_cod_kg_giorno(10000, 400), 4000.0)
        self.assertEqual(mh845_cod_kg_giorno(10000, 0), 0.0)
        self.assertEqual(mh845_e_base(10000, 0.45), 1642500.0)
        self.assertEqual(mh845_e_base(10000, 0), 0.0)

    def test_split_aerazione_resto_e_domanda_alt(self):
        self.assertAlmostEqual(mh845_aerazione(1642500.0, 0.55), 903375.0,
                               places=6)
        self.assertAlmostEqual(mh845_resto(1642500.0, 0.55), 739125.0,
                               places=6)
        self.assertAlmostEqual(mh845_aerazione(1642500.0, 0.55)
                               + mh845_resto(1642500.0, 0.55),
                               1642500.0, places=6)
        self.assertEqual(mh845_aerazione_alt(903375.0, 0.25), 677531.25)
        self.assertEqual(mh845_e_alt_domanda(677531.25, 739125.0), 1416656.25)

    def test_cod_rimosso_biogas_elettricita(self):
        self.assertEqual(mh845_cod_rimosso(4000.0, 0.85), 3400.0)
        self.assertEqual(mh845_biogas_m3_anno(3400.0, 0.35), 434350.0)
        self.assertAlmostEqual(mh845_e_biogas(434350.0, 0.60, 9.94, 0.35),
                               906662.19, places=6)
        self.assertEqual(mh845_e_biogas(434350.0, 0.60, 9.94, 0.35) * 0,
                         0.0)

    def test_fv_produzione_autoconsumo_deficit_immessa(self):
        self.assertEqual(mh845_e_fv(300, 1100), 330000.0)
        self.assertEqual(mh845_produzione(330000.0, 906662.19), 1236662.19)
        self.assertEqual(mh845_autoconsumo(1416656.25, 1236662.19), 1236662.19)
        self.assertEqual(mh845_autoconsumo(1416656.25, 2000000.0), 1416656.25)
        self.assertAlmostEqual(mh845_deficit(1416656.25, 1236662.19),
                               179994.06, places=6)
        self.assertEqual(mh845_immessa(1236662.19, 1236662.19), 0.0)
        self.assertEqual(mh845_immessa(2000000.0, 1416656.25), 583343.75)

    def test_bilancio_produzione_senza_batteria(self):
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["produzione_kwh_e_anno"],
                               bc["autoconsumo_kwh_e_anno"]
                               + bc["immessa_kwh_e_anno"], places=6)
        self.assertGreaterEqual(bc["immessa_kwh_e_anno"], 0.0)
        grosso = mh845_calcola(**_demo_kwargs(p_pv_kwp=2000))
        self.assertEqual(grosso["deficit_kwh_e_anno"], 0.0)
        self.assertAlmostEqual(grosso["immessa_kwh_e_anno"], 1690005.94,
                               places=6)

    def test_c_base_c_alt_scomposizione(self):
        self.assertAlmostEqual(mh845_c_base(1642500.0, 0.22), 361350.0,
                               places=6)
        self.assertAlmostEqual(mh845_c_alt(179994.06, 0.22, 0.0, 0.08,
                                           15000), 54598.6932, places=6)
        self.assertAlmostEqual(mh845_c_alt(0.0, 0.22, 1690005.94, 0.08,
                                           15000), -120200.4752, places=6)

    def test_capex_totale_voci(self):
        self.assertEqual(mh845_capex_totale(900, 300, 80000, 250000),
                         600000.0)
        self.assertEqual(mh845_capex_totale(900, 0, 80000, 250000),
                         330000.0)
        self.assertEqual(mh845_capex_totale(0, 300, 0, 0), 0.0)

    def test_immissione_e_ricavo_non_spreco(self):
        base = mh845_demo_calcoli()
        senza_ricavo = mh845_calcola(**_demo_kwargs(p_immissione=0.0))
        grosso = mh845_calcola(**_demo_kwargs(p_pv_kwp=2000))
        senza_ricavo_grosso = mh845_calcola(**_demo_kwargs(p_pv_kwp=2000,
                                                           p_immissione=0.0))
        self.assertAlmostEqual(senza_ricavo_grosso["c_alt_eur_anno"],
                               grosso["c_alt_eur_anno"] + 135200.4752,
                               places=6)
        self.assertAlmostEqual(base["c_alt_eur_anno"],
                               base["deficit_kwh_e_anno"] * 0.22 + 15000,
                               places=6)

    def test_risparmio_segno(self):
        self.assertAlmostEqual(mh845_risparmio(361350.0, 54598.6932),
                               306751.3068, places=6)
        self.assertLess(mh845_risparmio(54598.6932, 361350.0), 0.0)

    def test_co2_solo_deficit_biogas_zero(self):
        self.assertAlmostEqual(mh845_co2(1642500.0, 0.35), 574.875,
                               places=6)
        self.assertAlmostEqual(mh845_co2(179994.06, 0.35), 62.997921,
                               places=6)
        self.assertAlmostEqual(mh845_co2_evitata(574.875, 62.997921),
                               511.877079, places=6)
        grosso = mh845_calcola(**_demo_kwargs(p_pv_kwp=2000))
        self.assertEqual(grosso["co2_alt_t_anno"], 0.0)
        self.assertAlmostEqual(grosso["co2_evitata_t_anno"], 574.875,
                               places=6)

    def test_fv_nullo_e_biogas_nullo_ammessi_non_degeneri(self):
        r = mh845_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertEqual(r["e_fv_kwh_e_anno"], 0.0)
        self.assertEqual(r["produzione_kwh_e_anno"], 906662.19)
        self.assertTrue(r["valid"])
        s = mh845_calcola(**_demo_kwargs(resa_biogas=0))
        self.assertEqual(s["e_biogas_kwh_e_anno"], 0.0)
        self.assertEqual(s["produzione_kwh_e_anno"], 330000.0)
        self.assertTrue(s["valid"])


class TestFinanza(unittest.TestCase):
    def test_p_prelievo_pareggio_demo(self):
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["p_prelievo_pareggio"],
                               0.010256368599774713, places=12)
        self.assertAlmostEqual(mh845_p_prelievo_pareggio(15000, 0.0, 0.08,
                                                         1642500.0,
                                                         179994.06),
                               0.010256368599774713, places=12)

    def test_p_prelievo_pareggio_none_casi(self):
        self.assertIsNone(mh845_p_prelievo_pareggio(15000, 0.0, 0.08,
                                                    1642500.0, 1642500.0))
        self.assertIsNone(mh845_p_prelievo_pareggio(15000, 1690005.94,
                                                    0.08, 1642500.0, 0.0))
        self.assertIsNone(mh845_calcola(**_demo_kwargs(p_pv_kwp=2000))
                          ["p_prelievo_pareggio"])
        self.assertIsNone(mh845_calcola(**_demo_kwargs(
            risparmio_soffianti=0, p_pv_kwp=0,
            resa_biogas=0))["p_prelievo_pareggio"])

    def test_p_prelievo_pareggio_verifica(self):
        bc = mh845_demo_calcoli()
        pstar = bc["p_prelievo_pareggio"]
        r = mh845_calcola(**_demo_kwargs(p_prelievo=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")

    def test_p_prelievo_pareggio_soglia(self):
        bc = mh845_demo_calcoli()
        pstar = bc["p_prelievo_pareggio"]
        self.assertAlmostEqual(
            mh845_calcola(**_demo_kwargs(p_prelievo=pstar + 0.01))
            ["risparmio_eur_anno"], 14625.0594, places=6)
        self.assertAlmostEqual(
            mh845_calcola(**_demo_kwargs(p_prelievo=pstar - 0.01))
            ["risparmio_eur_anno"], -14625.0594, places=6)

    def test_flussi_lunghezza_e_primo(self):
        flussi = mh845_flussi(600000, 306751.3068, 15)
        self.assertEqual(len(flussi), 16)
        self.assertEqual(flussi[0], -600000)
        self.assertTrue(all(f == 306751.3068 for f in flussi[1:]))

    def test_van_demo_e_zero_tasso(self):
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["van"], 2379245.068956523, places=6)
        self.assertAlmostEqual(mh845_van([-600000] + [306751.3068] * 15,
                                         0.0), 4001269.602, places=6)

    def test_van_usa_frazione_non_percentuale(self):
        self.assertAlmostEqual(mh845_van([-600000] + [306751.3068] * 15,
                                         0.06), 2379245.068956523, places=6)
        self.assertLess(mh845_van([-600000] + [306751.3068] * 15, 6.0),
                        0.0)

    def test_tir_demo(self):
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["tir"], 51.01974777172603, places=6)
        self.assertGreater(bc["tir"], 50.0)

    def test_payback_regola_maggiore_uguale(self):
        self.assertEqual(mh845_payback([-600000] + [306751.3068] * 15), 2)
        self.assertEqual(mh845_payback([-10000, 10000.0]), 1)
        self.assertIsNone(mh845_payback([-600000] + [100.0] * 15))

    def test_verdetto_frazione(self):
        self.assertEqual(mh845_verdetto(306751.3068, 100.0, 600000, 0.05),
                         "CONVIENTE")
        self.assertEqual(mh845_verdetto(306751.3068, -20000.0, 600000, 0.05),
                         "MARGINALE")
        self.assertEqual(mh845_verdetto(306751.3068, -100000.0, 600000, 0.05),
                         "NON_CONVIENTE")
        self.assertEqual(mh845_verdetto(0.0, 100.0, 600000, 0.05),
                         "NON_CALCOLABILE")
        self.assertEqual(mh845_verdetto(-100.0, 100.0, 600000, 0.05),
                         "NON_CALCOLABILE")
        self.assertEqual(mh845_verdetto(None, 100.0, 600000, 0.05),
                         "NON_CALCOLABILE")
        self.assertEqual(mh845_verdetto(306751.3068, 0.0, 600000, 0.05),
                         "MARGINALE")


class TestValidaEDemo(unittest.TestCase):
    def test_valida_demo_ok(self):
        self.assertTrue(mh845_valida(**_demo_kwargs())["valido"])

    def test_valida_rifiuta_stringa_nan_inf_bool(self):
        for chiave, bad in (("portata_m3_giorno", "10000"),
                            ("portata_m3_giorno", float("nan")),
                            ("portata_m3_giorno", float("inf")),
                            ("portata_m3_giorno", True)):
            kw = _demo_kwargs(**{chiave: bad})
            self.assertFalse(mh845_valida(**kw)["valido"])

    def test_valida_rifiuta_range(self):
        for over in ({"portata_m3_giorno": 0},
                     {"portata_m3_giorno": -1},
                     {"cod_mg_l": -1},
                     {"e_specifica": -0.1},
                     {"share_aerazione": -0.1},
                     {"share_aerazione": 1.1},
                     {"risparmio_soffianti": -0.1},
                     {"risparmio_soffianti": 1.1},
                     {"rimozione_cod": -0.1},
                     {"rimozione_cod": 1.1},
                     {"resa_biogas": -0.1},
                     {"share_ch4": -0.1},
                     {"share_ch4": 1.1},
                     {"pci_ch4": -0.1},
                     {"eta_el_cogen": 0},
                     {"eta_el_cogen": 1.1},
                     {"p_pv_kwp": -1},
                     {"prod_specifica": -1},
                     {"p_prelievo": -0.1},
                     {"p_immissione": -0.1},
                     {"opex_alt": -1},
                     {"capex_fv": -1},
                     {"capex_soffianti": -1},
                     {"capex_digestore_cogen": -1},
                     {"f_el": -0.1},
                     {"tasso": -0.1},
                     {"vita": 0},
                     {"vita": 15.5},
                     {"tolleranza": -0.1}):
            self.assertFalse(mh845_valida(**_demo_kwargs(**over))["valido"])

    def test_valida_accetta_limiti_e_nessun_tetto_tasso_tolleranza(self):
        self.assertTrue(mh845_valida(**_demo_kwargs(tasso=0.25))["valido"])
        self.assertTrue(mh845_valida(**_demo_kwargs(tolleranza=1.5))["valido"])
        self.assertTrue(mh845_valida(**_demo_kwargs(
            cod_mg_l=0, e_specifica=0, share_aerazione=0,
            risparmio_soffianti=0, rimozione_cod=0, resa_biogas=0,
            share_ch4=0, pci_ch4=0, p_pv_kwp=0, prod_specifica=0,
            p_prelievo=0, p_immissione=0, opex_alt=0, capex_fv=0,
            capex_soffianti=0, capex_digestore_cogen=0, f_el=0,
            tasso=0, tolleranza=0))["valido"])

    def test_demo_dict(self):
        d = mh845_demo()
        self.assertEqual(d["portata_m3_giorno"], 10000)
        self.assertEqual(d["cod_mg_l"], 400)
        self.assertEqual(d["e_specifica"], 0.45)
        self.assertEqual(d["share_aerazione"], 0.55)
        self.assertEqual(d["risparmio_soffianti"], 0.25)
        self.assertEqual(d["rimozione_cod"], 0.85)
        self.assertEqual(d["resa_biogas"], 0.35)
        self.assertEqual(d["share_ch4"], 0.60)
        self.assertEqual(d["pci_ch4"], 9.94)
        self.assertEqual(d["eta_el_cogen"], 0.35)
        self.assertEqual(d["p_pv_kwp"], 300)
        self.assertEqual(d["prod_specifica"], 1100)
        self.assertEqual(d["p_prelievo"], 0.22)
        self.assertEqual(d["p_immissione"], 0.08)
        self.assertEqual(d["opex_alt"], 15000)
        self.assertEqual(d["capex_fv"], 900)
        self.assertEqual(d["capex_soffianti"], 80000)
        self.assertEqual(d["capex_digestore_cogen"], 250000)
        self.assertEqual(d["f_el"], 0.35)
        self.assertEqual(d["tasso"], 0.06)
        self.assertEqual(d["vita"], 15)
        self.assertEqual(d["tolleranza"], 0.05)

    def test_demo_costanti_vs_demo_calcoli(self):
        bc = mh845_demo_calcoli()
        for chiave, atteso in _DEMO.items():
            got = bc[chiave]
            if atteso is None:
                self.assertIsNone(got, chiave)
            elif isinstance(atteso, float):
                self.assertLess(_rel(got, atteso), 1e-9, chiave)
            else:
                self.assertEqual(got, atteso, chiave)

    def test_demo_fisica_economia(self):
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], 1642500.0, places=6)
        self.assertEqual(bc["e_alt_domanda_kwh_e_anno"], 1416656.25)
        self.assertEqual(bc["produzione_kwh_e_anno"], 1236662.19)
        self.assertAlmostEqual(bc["c_base_eur_anno"], 361350.0, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], 54598.6932, places=6)
        self.assertEqual(bc["capex_totale_eur"], 600000.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(demo_calcoli()["verdetto"], "CONVIENTE")

    def test_demo_flussi_e_cumulato(self):
        bc = mh845_demo_calcoli()
        self.assertEqual(len(bc["flussi"]), 16)
        cum = 0.0
        for i, f in enumerate(bc["flussi"]):
            cum += f
            self.assertEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[i], cum)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[1],
                               -293248.6932, places=6)
        self.assertAlmostEqual(bc["df_flussi"]["Cumulato (EUR)"].iloc[2],
                               13502.6136, places=6)

    def test_demo_tabella_righe(self):
        bc = mh845_demo_calcoli()
        voci = list(bc["df_tabella"]["Voce"])
        self.assertIn("Portata trattata (m3/giorno)", voci)
        self.assertIn("COD influente (mg/L)", voci)
        self.assertIn("Consumo elettrico base (kWh_e/anno)", voci)
        self.assertIn("Aerazione base (kWh_e/anno)", voci)
        self.assertIn("Domanda elettrica alternativa (kWh_e/anno)", voci)
        self.assertIn("Biogas (m3/anno)", voci)
        self.assertIn("Elettricita' da biogas (kWh_e/anno)", voci)
        self.assertIn("Produzione rinnovabile totale (kWh_e/anno)", voci)
        self.assertIn("Energia immessa, con ricavo (kWh_e/anno)", voci)
        self.assertIn("Deficit da rete (kWh_e/anno)", voci)
        self.assertIn("CAPEX totale (EUR)", voci)
        self.assertIn("Prezzo di prelievo di pareggio (EUR/kWh, soglia)", voci)
        self.assertIn("Verdetto", voci)

    def test_demo_coerenza_interna(self):
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"],
                               bc["portata_m3_giorno"] * 365
                               * bc["e_specifica"])
        self.assertAlmostEqual(bc["e_alt_domanda_kwh_e_anno"],
                               bc["aerazione_alt_kwh_e_anno"]
                               + bc["resto_kwh_e_anno"])
        self.assertAlmostEqual(bc["deficit_kwh_e_anno"],
                               bc["e_alt_domanda_kwh_e_anno"]
                               - bc["autoconsumo_kwh_e_anno"])
        self.assertAlmostEqual(bc["risparmio_eur_anno"],
                               bc["c_base_eur_anno"] - bc["c_alt_eur_anno"])
        self.assertAlmostEqual(bc["co2_evitata_t_anno"],
                               bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
        self.assertAlmostEqual(bc["capex_totale_eur"],
                               bc["capex_fv"] * bc["p_pv_kwp"]
                               + bc["capex_soffianti"]
                               + bc["capex_digestore_cogen"])

    def test_demo_contro_riconteggio_indipendente(self):
        codkg = 10000 * 400 / 1000
        ebase = 10000 * 365 * 0.45
        aer = ebase * 0.55
        resto = ebase * 0.45
        aalt = aer * 0.75
        edom = aalt + resto
        codr = codkg * 0.85
        bio = codr * 365 * 0.35
        ebg = bio * 0.60 * 9.94 * 0.35
        efv = 300 * 1100
        prd = efv + ebg
        aut = min(edom, prd)
        dft = edom - aut
        imm = prd - aut
        c_base = ebase * 0.22
        c_alt = dft * 0.22 - imm * 0.08 + 15000
        bc = mh845_demo_calcoli()
        self.assertAlmostEqual(bc["cod_kg_giorno"], codkg, places=6)
        self.assertAlmostEqual(bc["e_base_kwh_e_anno"], ebase, places=6)
        self.assertAlmostEqual(bc["aerazione_kwh_e_anno"], aer, places=6)
        self.assertAlmostEqual(bc["e_alt_domanda_kwh_e_anno"], edom, places=6)
        self.assertAlmostEqual(bc["biogas_m3_anno"], bio, places=6)
        self.assertAlmostEqual(bc["e_biogas_kwh_e_anno"], ebg, places=6)
        self.assertAlmostEqual(bc["produzione_kwh_e_anno"], prd, places=6)
        self.assertAlmostEqual(bc["autoconsumo_kwh_e_anno"], aut, places=6)
        self.assertAlmostEqual(bc["deficit_kwh_e_anno"], dft, places=6)
        self.assertAlmostEqual(bc["immessa_kwh_e_anno"], imm, places=6)
        self.assertAlmostEqual(bc["c_base_eur_anno"], c_base, places=6)
        self.assertAlmostEqual(bc["c_alt_eur_anno"], c_alt, places=6)
        self.assertAlmostEqual(bc["risparmio_eur_anno"], c_base - c_alt,
                               places=6)

    def test_demo_verdetto_coerente_con_risparmio_e_van(self):
        bc = mh845_demo_calcoli()
        self.assertGreater(bc["risparmio_eur_anno"], 0.0)
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")


class TestVarianti(unittest.TestCase):
    def test_variante_prelievo_piu_meno_20(self):
        meno = mh845_calcola(**_demo_kwargs(p_prelievo=0.176))
        self.assertAlmostEqual(meno["risparmio_eur_anno"], 242401.04544,
                               places=6)
        self.assertAlmostEqual(meno["van"], 1754259.3082019961, places=6)
        self.assertAlmostEqual(meno["tir"], 40.14446647295193, places=6)
        self.assertEqual(meno["payback"], 3)
        self.assertEqual(meno["verdetto"], "CONVIENTE")
        piu = mh845_calcola(**_demo_kwargs(p_prelievo=0.264))
        self.assertAlmostEqual(piu["risparmio_eur_anno"], 371101.56816,
                               places=6)
        self.assertAlmostEqual(piu["van"], 3004230.8297110517, places=6)
        self.assertAlmostEqual(piu["tir"], 61.80492302456522, places=6)
        self.assertEqual(piu["payback"], 2)
        self.assertEqual(piu["verdetto"], "CONVIENTE")

    def test_prelievo_alto_migliora_il_caso(self):
        demo = mh845_demo_calcoli()
        meno = mh845_calcola(**_demo_kwargs(p_prelievo=0.176))
        piu = mh845_calcola(**_demo_kwargs(p_prelievo=0.264))
        self.assertLess(meno["risparmio_eur_anno"], demo["risparmio_eur_anno"])
        self.assertGreater(piu["risparmio_eur_anno"], demo["risparmio_eur_anno"])

    def test_variante_senza_fotovoltaico_convinte(self):
        r = mh845_calcola(**_demo_kwargs(p_pv_kwp=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 234151.3068,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 1944135.792446528, places=6)
        self.assertAlmostEqual(r["tir"], 70.93210503408358, places=6)
        self.assertEqual(r["payback"], 2)
        self.assertEqual(r["capex_totale_eur"], 330000.0)

    def test_variante_senza_biogas_convinte(self):
        r = mh845_calcola(**_demo_kwargs(resa_biogas=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 107285.625,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 441984.7028054087, places=6)
        self.assertAlmostEqual(r["tir"], 15.93474306053536, places=6)
        self.assertEqual(r["payback"], 6)

    def test_variante_senza_soffianti_convinte(self):
        r = mh845_calcola(**_demo_kwargs(risparmio_soffianti=0))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 257065.6818,
                               places=6)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(r["van"], 1896685.9078449956, places=6)
        self.assertAlmostEqual(r["tir"], 42.63609441977058, places=6)
        self.assertEqual(r["payback"], 3)

    def test_variante_capex_doppio_convinte(self):
        r = mh845_calcola(**_demo_kwargs(capex_fv=1800,
                                         capex_soffianti=160000,
                                         capex_digestore_cogen=500000))
        self.assertAlmostEqual(r["van"], 1779245.0689565234, places=6)
        self.assertAlmostEqual(r["tir"], 24.621327253028703, places=6)
        self.assertEqual(r["payback"], 4)
        self.assertEqual(r["verdetto"], "CONVIENTE")
        self.assertEqual(r["capex_totale_eur"], 1200000.0)

    def test_variante_vita_10_convinte(self):
        r = mh845_calcola(**_demo_kwargs(vita=10))
        self.assertAlmostEqual(r["van"], 1657716.3211832163, places=6)
        self.assertAlmostEqual(r["tir"], 50.25347169211655, places=6)
        self.assertEqual(r["payback"], 2)
        self.assertEqual(r["verdetto"], "CONVIENTE")

    def test_variante_tasso_zero(self):
        zero = mh845_calcola(**_demo_kwargs(tasso=0.0))
        self.assertAlmostEqual(zero["van"], 4001269.602, places=6)
        self.assertEqual(zero["payback"], 2)

    def test_sensibilita_helper_coerente_con_calcola(self):
        s = mh845_sensibilita(**mh845_demo())
        self.assertEqual(set(s.keys()), {"prelievo_meno20", "prelievo_piu20",
                                         "senza_fv", "senza_biogas",
                                         "senza_soffianti",
                                         "capex_doppio", "vita_10",
                                         "tasso_0"})
        self.assertAlmostEqual(s["prelievo_meno20"]["risparmio_eur_anno"],
                               242401.04544, places=6)
        self.assertAlmostEqual(s["prelievo_piu20"]["van"],
                               3004230.8297110517, places=6)
        self.assertEqual(s["senza_fv"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_biogas"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["senza_soffianti"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["capex_doppio"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["vita_10"]["verdetto"], "CONVIENTE")
        self.assertEqual(s["tasso_0"]["verdetto"], "CONVIENTE")

    def test_demo_deterministica_due_chiamate(self):
        a = mh845_demo_calcoli()
        b = mh845_demo_calcoli()
        self.assertEqual(a["van"], b["van"])
        self.assertEqual(a["flussi"], b["flussi"])

    def test_demo_chiavi_attese(self):
        d = mh845_demo()
        attese = {"portata_m3_giorno", "cod_mg_l", "e_specifica",
                  "share_aerazione", "risparmio_soffianti",
                  "rimozione_cod", "resa_biogas", "share_ch4",
                  "pci_ch4", "eta_el_cogen", "p_pv_kwp",
                  "prod_specifica", "p_prelievo", "p_immissione",
                  "opex_alt", "capex_fv", "capex_soffianti",
                  "capex_digestore_cogen", "f_el", "tasso", "vita",
                  "tolleranza"}
        self.assertEqual(set(d.keys()), attese)


class TestDegeneri(unittest.TestCase):
    def test_degenere_tutti_i_campi_sollevano(self):
        campi = ["portata_m3_giorno", "cod_mg_l", "e_specifica",
                 "share_aerazione", "risparmio_soffianti",
                 "rimozione_cod", "resa_biogas", "share_ch4",
                 "pci_ch4", "eta_el_cogen", "p_pv_kwp",
                 "prod_specifica", "p_prelievo", "p_immissione",
                 "opex_alt", "capex_fv", "capex_soffianti",
                 "capex_digestore_cogen", "f_el", "tasso", "vita",
                 "tolleranza"]
        for campo in campi:
            with self.assertRaises(ValueError, msg=campo):
                mh845_calcola(**_demo_kwargs(**{campo: -1}))

    def test_degenere_quota_sopra_uno_eta_sopra_uno_e_vita(self):
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(share_aerazione=1.1))
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(risparmio_soffianti=1.1))
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(rimozione_cod=1.1))
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(share_ch4=1.1))
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(eta_el_cogen=1.1))
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(eta_el_cogen=0))
        with self.assertRaises(ValueError):
            mh845_calcola(**_demo_kwargs(portata_m3_giorno=0))

    def test_degenere_stringa_nan_inf(self):
        for campo, bad in (("portata_m3_giorno", "10000"),
                           ("portata_m3_giorno", float("nan")),
                           ("capex_soffianti", float("inf")),
                           ("p_prelievo", True)):
            with self.assertRaises(ValueError, msg=campo):
                mh845_calcola(**_demo_kwargs(**{campo: bad}))

    def test_zeri_ammessi_non_sollevano(self):
        r = mh845_calcola(**_demo_kwargs(
            cod_mg_l=0, e_specifica=0, share_aerazione=0,
            risparmio_soffianti=0, rimozione_cod=0, resa_biogas=0,
            share_ch4=0, pci_ch4=0, p_pv_kwp=0, prod_specifica=0,
            p_prelievo=0, p_immissione=0, opex_alt=0, capex_fv=0,
            capex_soffianti=0, capex_digestore_cogen=0, f_el=0,
            tasso=0, tolleranza=0))
        self.assertTrue(r["valid"])

    def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile(self):
        r = mh845_calcola(**_demo_kwargs(opex_alt=400000))
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")
        self.assertLess(r["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(r["risparmio_eur_anno"], -78248.6932,
                               places=6)

    def test_pareggio_esatto_soglia(self):
        bc = mh845_demo_calcoli()
        pstar = bc["p_prelievo_pareggio"]
        r = mh845_calcola(**_demo_kwargs(p_prelievo=pstar))
        self.assertAlmostEqual(r["risparmio_eur_anno"], 0.0, places=6)
        self.assertEqual(r["verdetto"], "NON_CALCOLABILE")


class TestCsv(unittest.TestCase):
    def test_csv_sep_e_righe(self):
        bc = mh845_demo_calcoli()
        csv = mh845_csv(bc, dict(mh845_demo()))
        self.assertIn(";", csv)
        righe = csv.strip().splitlines()
        self.assertEqual(righe[0], "voce;valore")
        self.assertGreater(len(righe), 30)

    def test_csv_valori_coerenti_con_calcola(self):
        bc = mh845_demo_calcoli()
        csv = mh845_csv(bc, dict(mh845_demo()))
        self.assertIn("verdetto;CONVIENTE", csv)
        righe = {r.split(";")[0]: r.split(";")[1]
                 for r in csv.strip().splitlines()[1:]}
        self.assertAlmostEqual(float(righe["risparmio_eur_anno"]),
                               306751.3068, places=6)
        self.assertAlmostEqual(float(righe["p_prelievo_pareggio"]),
                               0.010256368599774713, places=12)

    def test_csv_contiene_tutte_le_chiavi_input(self):
        bc = mh845_demo_calcoli()
        csv = mh845_csv(bc, dict(mh845_demo()))
        for chiave in mh845_demo().keys():
            self.assertIn(chiave, csv)


class TestStruttura(unittest.TestCase):
    def test_ast_helpers_parsabile(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        ast.parse(src)
        self.assertNotIn("import streamlit", src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_ast_ui_dedentata_parsabile(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        ast.parse(textwrap.dedent(src))

    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab845:"), 1)
        self.assertTrue(src.startswith("    # W848"))

    def test_ui_tab845_count_form(self):
        # Forma del count in questa fase (standalone, senza
        # app.py): il blocco UI apre tab845 esattamente una
        # volta e gli helper definiscono le funzioni mh845.
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab845:"), 1)
        self.assertIn("def mh845_demo(", src_h)
        self.assertIn("def mh845_calcola(", src_h)
        self.assertIn("tab845", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Impianto di depurazione: soffianti ad alta efficienza + fotovoltaico + biogas da digestione anaerobica battono soffianti tradizionali + rete?", src)
        self.assertIn("🏭 Impianto di depurazione: soffianti ad alta efficienza + fotovoltaico + biogas da digestione anaerobica battono soffianti tradizionali + rete?", src)
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
        chiavi = re.findall(r'key="(st845_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st845_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertIn('key="st845_calcola"', src)
        self.assertIn('key="st845_csv"', src)
        self.assertIn('key="st845_csv_flussi"', src)

    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def845\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh845_demo().keys()), lette - set(mh845_demo().keys()))
        self.assertEqual(lette, set(mh845_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc845\['([^']+)'\]", src))
        attese = set(mh845_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg845"), src.index(".paiac("))
        self.assertLess(src.index('risparmio_eur_anno"] <= 0.0'), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"(st\.slider|st\.number_input)\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)


if __name__ == "__main__":
    unittest.main()
