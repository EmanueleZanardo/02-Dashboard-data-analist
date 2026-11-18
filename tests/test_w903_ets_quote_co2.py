"""Test nuova scheda EU ETS: le quote CO2 dell'impianto, comprare,
coprirsi o abbattere?
Repo path: tests/test_w903_ets_quote_co2.py

Effetto ECONOMICO (non solo climatico): un impianto che emette
CO2 deve consegnare ogni anno tante quote EUA quante sono le sue
emissioni eccedenti l'allocazione gratuita; ogni tonnellata in
deficit si compra al prezzo EUA dell'anno. Abbattere le emissioni
di una frazione r riduce il deficit e quindi il costo compliance:
il risparmio annuo e la differenza tra costo base e costo
abbattuto meno O&M, e ripaga il CAPEX di abbattimento solo se la
VAN dei risparmi attualizzati supera quel CAPEX.
Demo: impianto 50,0 MW, 5.000 ore/anno, fattore di emissione
0,40 tCO2/MWh, allocazione gratuita A0 40.000 t/anno, decadimento
allocazione 0,05/anno, prezzo EUA p0 85,00 EUR/t, crescita
prezzo 0,03/anno, abbattimento r 0,30, CAPEX abbattimento
12.000.000 EUR, O&M 300.000 EUR/anno, vita 10 anni, tasso 0,05
(frazione), copertura forward 0,70, tolleranza 0,10 (frazione
del CAPEX).
Energia E = 50,0 per 5.000 = 250.000,00 MWh/anno; emissioni base
E0 = 250.000,00 per 0,40 = 100.000,00 t/anno; emissioni abbattute
E_ab = 100.000,00 per (1 meno 0,30) = 70.000,00 t/anno.
Anno 1: A = 40.000,00, p = 85,00, D_base = 60.000,00,
D_ab = 30.000,00, C_base = 5.100.000,00, C_ab = 2.550.000,00,
S = 2.250.000,00. Anno 10: A = 25.209,98, p = 110,91,
D_base = 74.790,02, D_ab = 44.790,02, C_base = 8.294.641,46,
C_ab = 4.967.469,85, S = 3.027.171,62.
Flussi [-12.000.000, 2.250.000, 2.326.500, 2.405.295,
2.486.453,85, 2.570.047,47, 2.656.148,89, 2.744.833,36,
2.836.178,36, 2.930.263,71, 3.027.171,62]; cumulato anno 5
38.296,32 (payback 5), cumulato finale 14.232.892,24.
VAN = 7.989.849,71 EUR; TIR per bisezione su flussi con
intervallo da meno 0,9 a 5,0 (16,40 %); payback (primo anno con
cumulato netto maggiore o uguale a 0) = 5; breakeven p0 per
bisezione su VAN(p0) = 0 tra 0 e 1000 EUR/t = 54,55 EUR/t;
costo abbattimento livellato = (CAPEX per CRF piu O&M) diviso
(E0 per r) = 61,80 EUR/t; CRF = 0,129505.
PV compliance spot = 50.292.399,26 EUR; PV compliance con
copertura (forward 70% a p0 fisso) = 45.980.269,12 EUR;
risparmio PV copertura = 4.312.130,15 EUR.
CO2 evitata vita = E0 per r per vita = 300.000,00 t
(INFORMATIVA, mai nel conto economico).
Scenari: base VAN 7.989.849,71, TIR 16,40 %, payback 5,
CONVIENTE; EUA alto (p0 130) VAN 19.799.104,52, TIR 30,31 %,
payback 4, CONVIENTE; EUA basso (p0 50) VAN meno 1.195.126,25,
TIR 3,01 %, payback 9, MARGINALE (edge intenzionale: valore
assoluto VAN 1.195.126,25 minore di 10 % del CAPEX,
1.200.000,00, quindi MARGINALE per la regola, non errore);
abbattimento 50 % (r 0,50) VAN 22.860.763,17, TIR 33,65 %,
payback 3, livellato 37,08, breakeven 32,73, CONVIENTE;
crescita prezzo 0 % (g 0) VAN 5.373.903,59, TIR 13,43 %,
payback 6, breakeven 61,80 uguale al livellato, CONVIENTE.
Confronto compliance: PV spot 50.292.399,26 contro PV con
copertura 45.980.269,12, risparmio PV 4.312.130,15, CAPEX
12.000.000,00, VAN 7.989.849,71, CO2 evitata vita 300.000,00 t.
Tolleranza in FRAZIONE (0,10 = 10 % del CAPEX), usata diretta,
NON divisa per 100 e NON in percentuale (a differenza della
scheda precedente). Il tasso e in FRAZIONE (0,05 = 5 %), usato
diretto, NON diviso per 100. Prezzi, costi, ore, fattore di
emissione e abbattimento restano costanti per tutta la vita,
SEMPLIFICAZIONE DICHIARATA (prezzo EUA volatile, allocazione
rivista, fattore reale e O&M reale variano nel mondo reale, qui
valore medio costante); la copertura forward e solo informativa
e non entra in VAN, TIR e payback; l'allocazione gratuita sposta
il livello del costo compliance ma NON il delta finche D_ab(t)
resta maggiore di 0 (nel demo A(t) resta sotto E_ab in tutti
gli anni: con A0 0 la VAN resta 7.989.849,71 e il PV spot sale
a 74.354.567,30; con decadimento 0 la VAN resta 7.989.849,71 e
il PV spot scende a 44.612.740,38).
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il risparmio S(t) e minore o
uguale a 0 in tutti gli anni (guard degenere: UI salta KPI,
grafico, tabella e CSV) oppure se un input e degenere (P nulla
o negativa, ore nulle o negative, f nullo o negativo o sopra 1,
A0 negativo, d negativo o maggiore o uguale a 1, p0 negativo, g
minore di meno 0,9 o sopra 1, r negativo o sopra 1, CAPEX
negativo, O&M negativo, vita nulla o negativa o non intera,
tasso nullo o negativo o maggiore o uguale a 1, copertura
negativa o sopra 1, tolleranza negativa o sopra 1); altrimenti
CONVIENTE se VAN maggiore o uguale a 0, MARGINALE se VAN
negativa entro tolleranza in FRAZIONE del CAPEX,
NON_CONVIENTE altrimenti.
Casi limite: r zero (risparmio uguale a meno O&M in tutti gli
anni, VAN None, NON_CALCOLABILE); p0 zero (stesso, S uguale a
meno O&M, NON_CALCOLABILE); O&M 10.000.000 (risparmio anno 1
meno 7.450.000, NON_CALCOLABILE); A0 100.000 (risparmio anno 1
meno 300.000 ma positivo dall'anno 2 (137.750,00), VAN meno 857.938,77, TIR
3,95 %, payback 9, MARGINALE); r 0,10 (VAN meno 6.881.063,75,
TIR meno 8,84 %, payback nessuno, livellato 185,41, breakeven
163,66); CAPEX zero (VAN 19.989.849,71, TIR non definita,
payback 1, livellato 10,00, breakeven 8,83); vita 5 (VAN meno
1.609.843,34, TIR 0,10 %, payback 5); tasso 0,10 (VAN
3.710.176,28, TIR 16,40 %, payback 5); tolleranza zero con p0
50 (NON_CONVIENTE, non piu MARGINALE).
Distinzione esplicita: qui SOLO il costo compliance EU ETS e
il confronto comprare quote contro abbattere (VAN sul RISPARMIO
con CAPEX di abbattimento), NIENTE carbon tax nazionale (li
l'aliquota fiscale per tonnellata: qui il prezzo e di mercato
EUA), NIENTE certificati verdi o garanzie di origine (li il
valore dell'energia rinnovabile: qui solo le quote CO2), NIENTE
LCOE di un impianto di generazione (li il costo livellato
dell'energia prodotta: qui il costo livellato
dell'abbattimento per tonnellata evitata).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w903_helpers import (
        demo_calcoli,
        mh898_allocazione,
        mh898_breakeven_p0,
        mh898_calcola,
        mh898_confronto,
        mh898_co2_evitata,
        mh898_costo,
        mh898_costo_livellato,
        mh898_crescita,
        mh898_crf,
        mh898_csv,
        mh898_deficit,
        mh898_demo,
        mh898_demo_calcoli,
        mh898_emissioni_abbattute,
        mh898_emissioni_base,
        mh898_energia,
        mh898_flussi,
        mh898_fraz,
        mh898_fraz_dec,
        mh898_fraz_pos,
        mh898_int_pos,
        mh898_nneg,
        mh898_num,
        mh898_payback,
        mh898_pos,
        mh898_prezzo,
        mh898_pv_copertura,
        mh898_pv_spot,
        mh898_riga_anno,
        mh898_risparmio,
        mh898_scenario,
        mh898_sensibilita,
        mh898_serie_annua,
        mh898_tasso,
        mh898_tir,
        mh898_valida,
        mh898_van,
        mh898_van_a_prezzo,
        mh898_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w903_helpers", os.path.join(_hf, "w903_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh898_allocazione = _mod.mh898_allocazione
    mh898_breakeven_p0 = _mod.mh898_breakeven_p0
    mh898_calcola = _mod.mh898_calcola
    mh898_confronto = _mod.mh898_confronto
    mh898_co2_evitata = _mod.mh898_co2_evitata
    mh898_costo = _mod.mh898_costo
    mh898_costo_livellato = _mod.mh898_costo_livellato
    mh898_crescita = _mod.mh898_crescita
    mh898_crf = _mod.mh898_crf
    mh898_csv = _mod.mh898_csv
    mh898_deficit = _mod.mh898_deficit
    mh898_demo = _mod.mh898_demo
    mh898_demo_calcoli = _mod.mh898_demo_calcoli
    mh898_emissioni_abbattute = _mod.mh898_emissioni_abbattute
    mh898_emissioni_base = _mod.mh898_emissioni_base
    mh898_energia = _mod.mh898_energia
    mh898_flussi = _mod.mh898_flussi
    mh898_fraz = _mod.mh898_fraz
    mh898_fraz_dec = _mod.mh898_fraz_dec
    mh898_fraz_pos = _mod.mh898_fraz_pos
    mh898_int_pos = _mod.mh898_int_pos
    mh898_nneg = _mod.mh898_nneg
    mh898_num = _mod.mh898_num
    mh898_payback = _mod.mh898_payback
    mh898_pos = _mod.mh898_pos
    mh898_prezzo = _mod.mh898_prezzo
    mh898_pv_copertura = _mod.mh898_pv_copertura
    mh898_pv_spot = _mod.mh898_pv_spot
    mh898_riga_anno = _mod.mh898_riga_anno
    mh898_risparmio = _mod.mh898_risparmio
    mh898_scenario = _mod.mh898_scenario
    mh898_sensibilita = _mod.mh898_sensibilita
    mh898_serie_annua = _mod.mh898_serie_annua
    mh898_tasso = _mod.mh898_tasso
    mh898_tir = _mod.mh898_tir
    mh898_valida = _mod.mh898_valida
    mh898_van = _mod.mh898_van
    mh898_van_a_prezzo = _mod.mh898_van_a_prezzo
    mh898_verdetto = _mod.mh898_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w903_helpers.py")
_UI_PATH = _risolvi("w903_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh89" + "7"
_VECCHIO_TAB = "tab89" + "7"
_VECCHIO_ST = "st89" + "7_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "energia_mwh_anno": 250000.0,
    "emissioni_base_t_anno": 100000.0,
    "emissioni_abbattute_t_anno": 70000.0,
    "allocazione_anno1": 40000.0,
    "allocazione_anno10": 25209.976388984363,
    "prezzo_anno1": 85.0,
    "prezzo_anno10": 110.90572062548581,
    "deficit_base_anno1": 60000.0,
    "deficit_abbattuto_anno1": 30000.0,
    "deficit_base_anno10": 74790.02361101564,
    "deficit_abbattuto_anno10": 44790.02361101564,
    "costo_base_anno1": 5100000.0,
    "costo_abbattuto_anno1": 2550000.0,
    "risparmio_anno1": 2250000.0,
    "costo_base_anno10": 8294641.464176788,
    "costo_abbattuto_anno10": 4967469.845412214,
    "risparmio_anno10": 3027171.6187645737,
    "crf": 0.12950457496545661,
    "costo_livellato": 61.801829986182646,
    "breakeven_p0": 54.55411302916025,
    "pv_spot": 50292399.26338959,
    "pv_copertura": 45980269.1163788,
    "risparmio_pv": 4312130.147010788,
    "co2_evitata_t": 300000.0,
    "van": 7989849.712686474,
    "tir": 16.400124376523873,
    "payback": 5,
}

_DEMO_SCENARI = [
    {"nome": "Base", "prezzo_eua_p0": 85.0,
     "crescita_prezzo": 0.03, "abbattimento_r": 0.3,
     "e0": 100000.0, "e_ab": 70000.0,
     "van": 7989849.712686474, "tir": 16.400124376523873,
     "payback": 5, "verdetto": "CONVIENTE",
     "breakeven_p0": 54.55411302916025,
     "costo_livellato": 61.801829986182646,
     "pv_spot": 50292399.26338959,
     "pv_copertura": 45980269.1163788,
     "risparmio_pv": 4312130.147010788},
    {"nome": "EUA alto", "prezzo_eua_p0": 130.0,
     "crescita_prezzo": 0.03, "abbattimento_r": 0.3,
     "e0": 100000.0, "e_ab": 70000.0,
     "van": 19799104.51992043, "tir": 30.314209696309145,
     "payback": 4, "verdetto": "CONVIENTE",
     "breakeven_p0": 54.55411302916025,
     "costo_livellato": 61.801829986182646,
     "pv_spot": 76917787.10871351,
     "pv_copertura": 70322764.53093228,
     "risparmio_pv": 6595022.57778123},
    {"nome": "EUA basso", "prezzo_eua_p0": 50.0,
     "crescita_prezzo": 0.03, "abbattimento_r": 0.3,
     "e0": 100000.0, "e_ab": 70000.0,
     "van": -1195126.2484954926, "tir": 3.006254506661316,
     "payback": 9, "verdetto": "MARGINALE",
     "breakeven_p0": 54.55411302916025,
     "costo_livellato": 61.801829986182646,
     "pv_spot": 29583764.272582114,
     "pv_copertura": 27047217.127281643,
     "risparmio_pv": 2536547.1453004703},
    {"nome": "Abbattimento 50%", "prezzo_eua_p0": 85.0,
     "crescita_prezzo": 0.03, "abbattimento_r": 0.5,
     "e0": 100000.0, "e_ab": 50000.0,
     "van": 22860763.173647754, "tir": 33.646650089416994,
     "payback": 3, "verdetto": "CONVIENTE",
     "breakeven_p0": 32.7324678174965,
     "costo_livellato": 37.08109799170959,
     "pv_spot": 50292399.26338959,
     "pv_copertura": 45980269.1163788,
     "risparmio_pv": 4312130.147010788},
    {"nome": "Crescita prezzo 0%", "prezzo_eua_p0": 85.0,
     "crescita_prezzo": 0.0, "abbattimento_r": 0.3,
     "e0": 100000.0, "e_ab": 70000.0,
     "van": 5373903.590665823, "tir": 13.434372429251763,
     "payback": 6, "verdetto": "CONVIENTE",
     "breakeven_p0": 61.80182998618244,
     "costo_livellato": 61.801829986182646,
     "pv_spot": 44132213.33908845,
     "pv_copertura": 44132213.33908845,
     "risparmio_pv": 0.0},
]

_DEMO_CONFRONTO = {
    "pv_spot": 50292399.26338959,
    "pv_copertura": 45980269.1163788,
    "risparmio_pv": 4312130.147010788,
    "van": 7989849.712686474,
    "capex": 12000000.0,
    "co2_evitata_t": 300000.0,
    "costo_livellato": 61.801829986182646,
    "breakeven_p0": 54.55411302916025,
}

_ORDINE_VALIDA = (
    "p_mw", "ore_annue", "fattore_emissione",
    "allocazione_a0", "decadimento_allocazione",
    "prezzo_eua_p0", "crescita_prezzo", "abbattimento_r",
    "capex_eur", "om_eur_anno", "vita_anni", "tasso",
    "copertura_frazione", "tolleranza_frazione")


def _demo_kwargs(**over):
    kw = dict(mh898_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh898_num(3, "x"), 3.0)
        self.assertEqual(mh898_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh898_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh898_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh898_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh898_pos(0, "x")
        with self.assertRaises(ValueError):
            mh898_pos(-1, "x")
        self.assertEqual(mh898_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh898_fraz(0, "x"), 0.0)
        self.assertEqual(mh898_fraz(1, "x"), 1.0)
        self.assertEqual(mh898_fraz(0.30, "x"), 0.30)
        with self.assertRaises(ValueError):
            mh898_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh898_fraz(1.01, "x")

    def test_fraz_pos_zero_no_uno_ok(self):
        self.assertEqual(mh898_fraz_pos(1, "x"), 1.0)
        self.assertEqual(mh898_fraz_pos(0.40, "x"), 0.40)
        with self.assertRaises(ValueError):
            mh898_fraz_pos(0, "x")
        with self.assertRaises(ValueError):
            mh898_fraz_pos(1.01, "x")

    def test_fraz_dec_bordi(self):
        self.assertEqual(mh898_fraz_dec(0, "x"), 0.0)
        self.assertEqual(mh898_fraz_dec(0.05, "x"), 0.05)
        self.assertEqual(mh898_fraz_dec(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh898_fraz_dec(-0.01, "x")
        with self.assertRaises(ValueError):
            mh898_fraz_dec(1.0, "x")

    def test_crescita_bordi(self):
        self.assertEqual(mh898_crescita(0.03, "x"), 0.03)
        self.assertEqual(mh898_crescita(-0.9, "x"), -0.9)
        self.assertEqual(mh898_crescita(1.0, "x"), 1.0)
        self.assertEqual(mh898_crescita(0.0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh898_crescita(-0.91, "x")
        with self.assertRaises(ValueError):
            mh898_crescita(1.01, "x")

    def test_int_pos(self):
        self.assertEqual(mh898_int_pos(10, "x"), 10)
        self.assertEqual(mh898_int_pos(10.0, "x"), 10)
        with self.assertRaises(ValueError):
            mh898_int_pos(0, "x")
        with self.assertRaises(ValueError):
            mh898_int_pos(10.5, "x")

    def test_tasso_intervallo_aperto(self):
        self.assertEqual(mh898_tasso(0.05, "x"), 0.05)
        self.assertEqual(mh898_tasso(0.99, "x"), 0.99)
        with self.assertRaises(ValueError):
            mh898_tasso(0.0, "x")
        with self.assertRaises(ValueError):
            mh898_tasso(1.0, "x")
        with self.assertRaises(ValueError):
            mh898_tasso(1.5, "x")
        with self.assertRaises(ValueError):
            mh898_tasso(-0.01, "x")


class TestFisica(unittest.TestCase):
    def test_energia(self):
        self.assertEqual(mh898_energia(50.0, 5000), 250000.0)
        self.assertEqual(mh898_energia(50.0, 4000), 200000.0)
        self.assertEqual(mh898_energia(100.0, 8760), 876000.0)
        with self.assertRaises(ValueError):
            mh898_energia(0, 5000)
        with self.assertRaises(ValueError):
            mh898_energia(50.0, 0)
        with self.assertRaises(ValueError):
            mh898_energia(-50.0, 5000)

    def test_emissioni_base_e_abbattute(self):
        self.assertEqual(mh898_emissioni_base(250000.0, 0.40),
                         100000.0)
        self.assertEqual(mh898_emissioni_base(200000.0, 0.50),
                         100000.0)
        self.assertEqual(mh898_emissioni_base(250000.0, 1.0),
                         250000.0)
        self.assertEqual(
            mh898_emissioni_abbattute(100000.0, 0.30), 70000.0)
        self.assertEqual(
            mh898_emissioni_abbattute(100000.0, 0.50), 50000.0)
        self.assertEqual(
            mh898_emissioni_abbattute(100000.0, 0.0), 100000.0)
        self.assertEqual(
            mh898_emissioni_abbattute(100000.0, 1.0), 0.0)
        with self.assertRaises(ValueError):
            mh898_emissioni_base(250000.0, 0)
        with self.assertRaises(ValueError):
            mh898_emissioni_base(250000.0, 1.1)
        with self.assertRaises(ValueError):
            mh898_emissioni_abbattute(100000.0, 1.1)
        with self.assertRaises(ValueError):
            mh898_emissioni_abbattute(100000.0, -0.1)

    def test_allocazione(self):
        self.assertEqual(mh898_allocazione(1, 40000.0, 0.05),
                         40000.0)
        self.assertAlmostEqual(
            mh898_allocazione(10, 40000.0, 0.05), 25209.98,
            places=2)
        self.assertAlmostEqual(
            mh898_allocazione(2, 40000.0, 0.05), 38000.0)
        self.assertEqual(mh898_allocazione(5, 40000.0, 0.0),
                         40000.0)
        self.assertEqual(mh898_allocazione(3, 0.0, 0.05), 0.0)
        with self.assertRaises(ValueError):
            mh898_allocazione(0, 40000.0, 0.05)
        with self.assertRaises(ValueError):
            mh898_allocazione(10, 40000.0, 1.0)
        with self.assertRaises(ValueError):
            mh898_allocazione(10, -1.0, 0.05)

    def test_prezzo(self):
        self.assertEqual(mh898_prezzo(1, 85.0, 0.03), 85.0)
        self.assertAlmostEqual(
            mh898_prezzo(10, 85.0, 0.03), 110.91, places=2)
        self.assertAlmostEqual(
            mh898_prezzo(2, 85.0, 0.03), 87.55, places=2)
        self.assertEqual(mh898_prezzo(10, 85.0, 0.0), 85.0)
        self.assertAlmostEqual(
            mh898_prezzo(2, 85.0, -0.5), 42.5, places=2)
        self.assertEqual(mh898_prezzo(5, 0.0, 0.03), 0.0)
        with self.assertRaises(ValueError):
            mh898_prezzo(0, 85.0, 0.03)
        with self.assertRaises(ValueError):
            mh898_prezzo(10, 85.0, -1.0)
        with self.assertRaises(ValueError):
            mh898_prezzo(10, -1.0, 0.03)

    def test_deficit_costo_risparmio(self):
        self.assertEqual(mh898_deficit(100000.0, 40000.0),
                         60000.0)
        self.assertEqual(mh898_deficit(70000.0, 40000.0), 30000.0)
        self.assertEqual(mh898_deficit(70000.0, 100000.0), 0.0)
        self.assertEqual(mh898_deficit(100000.0, 100000.0), 0.0)
        self.assertEqual(mh898_deficit(0.0, 0.0), 0.0)
        self.assertEqual(mh898_costo(60000.0, 85.0), 5100000.0)
        self.assertEqual(mh898_costo(30000.0, 85.0), 2550000.0)
        self.assertEqual(mh898_costo(0.0, 85.0), 0.0)
        self.assertEqual(mh898_costo(60000.0, 0.0), 0.0)
        self.assertEqual(
            mh898_risparmio(5100000.0, 2550000.0, 300000.0),
            2250000.0)
        self.assertEqual(
            mh898_risparmio(5100000.0, 2550000.0, 0.0),
            2550000.0)
        self.assertEqual(
            mh898_risparmio(0.0, 0.0, 300000.0), -300000.0)
        with self.assertRaises(ValueError):
            mh898_deficit(-1.0, 40000.0)
        with self.assertRaises(ValueError):
            mh898_deficit(100000.0, -1.0)
        with self.assertRaises(ValueError):
            mh898_costo(60000.0, -1.0)
        with self.assertRaises(ValueError):
            mh898_risparmio(5100000.0, 2550000.0, -1.0)

    def test_riga_anno(self):
        riga = mh898_riga_anno(1, 100000.0, 70000.0, 40000.0,
                               0.05, 85.0, 0.03, 300000.0)
        self.assertEqual(riga["anno"], 1)
        self.assertEqual(riga["allocazione"], 40000.0)
        self.assertEqual(riga["prezzo"], 85.0)
        self.assertEqual(riga["d_base"], 60000.0)
        self.assertEqual(riga["d_ab"], 30000.0)
        self.assertEqual(riga["c_base"], 5100000.0)
        self.assertEqual(riga["c_ab"], 2550000.0)
        self.assertEqual(riga["risparmio"], 2250000.0)
        riga = mh898_riga_anno(10, 100000.0, 70000.0, 40000.0,
                               0.05, 85.0, 0.03, 300000.0)
        self.assertAlmostEqual(riga["allocazione"], 25209.98,
                               places=2)
        self.assertAlmostEqual(riga["prezzo"], 110.91, places=2)
        self.assertAlmostEqual(riga["d_base"], 74790.02, places=2)
        self.assertAlmostEqual(riga["d_ab"], 44790.02, places=2)
        self.assertAlmostEqual(riga["c_base"], 8294641.46,
                               places=2)
        self.assertAlmostEqual(riga["c_ab"], 4967469.85, places=2)
        self.assertAlmostEqual(riga["risparmio"], 3027171.62,
                               places=2)
        # Allocazione sopra le emissioni abbattute:
        # deficit abbattuto zero, risparmio solo da base.
        riga = mh898_riga_anno(1, 100000.0, 70000.0, 100000.0,
                               0.05, 85.0, 0.03, 300000.0)
        self.assertEqual(riga["d_base"], 0.0)
        self.assertEqual(riga["d_ab"], 0.0)
        self.assertEqual(riga["c_base"], 0.0)
        self.assertEqual(riga["risparmio"], -300000.0)
        with self.assertRaises(ValueError):
            mh898_riga_anno(0, 100000.0, 70000.0, 40000.0,
                            0.05, 85.0, 0.03, 300000.0)

    def test_serie_annua(self):
        serie = mh898_serie_annua(100000.0, 70000.0, 40000.0,
                                  0.05, 85.0, 0.03, 300000.0, 10)
        self.assertEqual(len(serie), 10)
        self.assertEqual(serie[0]["risparmio"], 2250000.0)
        self.assertAlmostEqual(serie[4]["risparmio"], 2570047.47,
                               places=2)
        self.assertAlmostEqual(serie[9]["risparmio"], 3027171.62,
                               places=2)
        # Il risparmio cresce ogni anno (allocazione che
        # decade piu prezzo che cresce).
        for t in range(1, 10):
            self.assertGreater(serie[t]["risparmio"],
                               serie[t - 1]["risparmio"])
        # Con decadimento zero il deficit base e costante.
        serie = mh898_serie_annua(100000.0, 70000.0, 40000.0,
                                  0.0, 85.0, 0.03, 300000.0, 10)
        self.assertTrue(all(r["d_base"] == 60000.0
                            for r in serie))
        with self.assertRaises(ValueError):
            mh898_serie_annua(100000.0, 70000.0, 40000.0,
                              0.05, 85.0, 0.03, 300000.0, 0)

    def test_flussi_e_cumulati(self):
        bc = demo_calcoli()
        flussi = bc["flussi"]
        self.assertEqual(len(flussi), 11)
        self.assertEqual(flussi[0], -12000000.0)
        self.assertEqual(flussi[1], 2250000.0)
        self.assertAlmostEqual(flussi[5], 2570047.47, places=2)
        self.assertAlmostEqual(flussi[10], 3027171.62, places=2)
        self.assertAlmostEqual(sum(flussi), 14232892.24, places=2)
        # Cumulato anno 5 positivo: payback 5.
        self.assertAlmostEqual(sum(flussi[:6]), 38296.32, places=2)
        self.assertLess(sum(flussi[:5]), 0.0)
        flussi2 = mh898_flussi(bc["serie"], bc["capex_eur"], 10)
        self.assertEqual(flussi2, flussi)
        self.assertAlmostEqual(mh898_van(flussi, 0.05), bc["van"])
        with self.assertRaises(ValueError):
            mh898_flussi(bc["serie"][:9], bc["capex_eur"], 10)

    def test_crf_e_livellato(self):
        self.assertAlmostEqual(mh898_crf(0.05, 10), 0.129505,
                               places=6)
        self.assertAlmostEqual(mh898_crf(0.10, 10), 0.162745,
                               places=6)
        self.assertAlmostEqual(mh898_crf(0.05, 5), 0.230975,
                               places=6)
        self.assertAlmostEqual(
            mh898_costo_livellato(12000000.0, 0.12950457496545661,
                                  300000.0, 100000.0, 0.30),
            61.80, places=2)
        self.assertAlmostEqual(
            mh898_costo_livellato(12000000.0, 0.12950457496545661,
                                  300000.0, 100000.0, 0.50),
            37.08, places=2)
        self.assertAlmostEqual(
            mh898_costo_livellato(0.0, 0.12950457496545661,
                                  300000.0, 100000.0, 0.30),
            10.00, places=2)
        with self.assertRaises(ValueError):
            mh898_costo_livellato(12000000.0, 0.129505,
                                  300000.0, 100000.0, 0.0)
        with self.assertRaises(ValueError):
            mh898_costo_livellato(12000000.0, 0.129505,
                                  300000.0, 0.0, 0.30)
        with self.assertRaises(ValueError):
            mh898_crf(0.0, 10)
        with self.assertRaises(ValueError):
            mh898_crf(0.05, 0)

    def test_breakeven_p0(self):
        self.assertAlmostEqual(
            mh898_breakeven_p0(mh898_demo()), 54.55, places=2)
        # Con crescita prezzo 0 il breakeven coincide
        # col costo livellato (61,80).
        self.assertAlmostEqual(
            mh898_breakeven_p0(
                dict(mh898_demo(), crescita_prezzo=0.0)),
            61.80, places=2)
        # Con abbattimento 50 % il breakeven scende.
        self.assertAlmostEqual(
            mh898_breakeven_p0(
                dict(mh898_demo(), abbattimento_r=0.50)),
            32.73, places=2)
        # VAN al breakeven esatto circa zero; VAN(85)
        # positiva; VAN(0) negativa.
        be = mh898_breakeven_p0(mh898_demo())
        self.assertAlmostEqual(
            mh898_van_a_prezzo(be, mh898_demo()), 0.0,
            places=0)
        self.assertGreater(
            mh898_van_a_prezzo(85.0, mh898_demo()), 0.0)
        self.assertLess(
            mh898_van_a_prezzo(0.0, mh898_demo()), 0.0)
        with self.assertRaises(ValueError):
            mh898_breakeven_p0("non un dict")
        with self.assertRaises(ValueError):
            mh898_van_a_prezzo(-1.0, mh898_demo())

    def test_pv_spot_e_copertura(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            mh898_pv_spot(bc["serie"], 0.05), 50292399.26,
            places=2)
        self.assertAlmostEqual(
            mh898_pv_copertura(bc["serie"], 85.0, 0.70, 0.05),
            45980269.12, places=2)
        # Con copertura zero il PV e lo spot.
        self.assertAlmostEqual(
            mh898_pv_copertura(bc["serie"], 85.0, 0.0, 0.05),
            bc["pv_spot"])
        # Con copertura uno tutto il deficit e a p0 fisso:
        # il PV coincide col PV spot del caso a crescita
        # zero (prezzo costante 85 in entrambi).
        pv1 = mh898_pv_copertura(bc["serie"], 85.0, 1.0, 0.05)
        self.assertLess(pv1, bc["pv_spot"])
        self.assertAlmostEqual(pv1, 44132213.34, places=2)
        # Con crescita zero la copertura non cambia nulla.
        bc0 = mh898_calcola(
            _scenari=False,
            **dict(mh898_demo(), crescita_prezzo=0.0))
        self.assertAlmostEqual(bc0["pv_spot"],
                               bc0["pv_copertura"])
        with self.assertRaises(ValueError):
            mh898_pv_spot(bc["serie"], 0.0)
        with self.assertRaises(ValueError):
            mh898_pv_copertura(bc["serie"], 85.0, 1.5, 0.05)

    def test_scenario_singolo(self):
        s = mh898_scenario("EUA alto", mh898_demo(),
                           {"prezzo_eua_p0": 130.0})
        self.assertEqual(s["nome"], "EUA alto")
        self.assertEqual(s["prezzo_eua_p0"], 130.0)
        self.assertAlmostEqual(s["van"], 19799104.52, places=2)
        self.assertEqual(s["payback"], 4)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh898_scenario("EUA basso", mh898_demo(),
                           {"prezzo_eua_p0": 50.0})
        self.assertAlmostEqual(s["van"], -1195126.25, places=2)
        self.assertEqual(s["verdetto"], "MARGINALE")
        s = mh898_scenario("Abbattimento 50%", mh898_demo(),
                           {"abbattimento_r": 0.50})
        self.assertAlmostEqual(s["van"], 22860763.17, places=2)
        self.assertEqual(s["e_ab"], 50000.0)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        with self.assertRaises(ValueError):
            mh898_scenario("", mh898_demo(),
                           {"prezzo_eua_p0": 130.0})
        with self.assertRaises(ValueError):
            mh898_scenario("X", mh898_demo(),
                           {"fattore_emissione": 1.5})

    def test_scenario_risparmio_negativo_non_calcolabile(self):
        s = mh898_scenario("Senza abbattimento", mh898_demo(),
                           {"abbattimento_r": 0.0})
        self.assertIsNone(s["van"])
        self.assertIsNone(s["tir"])
        self.assertIsNone(s["payback"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh898_confronto(50292399.26, 45980269.12, 4312130.15,
                            7989849.71, 12000000.0, 300000.0,
                            61.80, 54.55)
        self.assertEqual(c["pv_spot"], 50292399.26)
        self.assertEqual(c["pv_copertura"], 45980269.12)
        self.assertAlmostEqual(c["risparmio_pv"], 4312130.15,
                               places=2)
        self.assertEqual(c["van"], 7989849.71)
        self.assertEqual(c["capex"], 12000000.0)
        self.assertEqual(c["co2_evitata_t"], 300000.0)
        self.assertEqual(c["costo_livellato"], 61.80)
        self.assertEqual(c["breakeven_p0"], 54.55)
        c = mh898_confronto(50292399.26, 45980269.12, 4312130.15,
                            0.0, 12000000.0, 300000.0,
                            None, None)
        self.assertIsNone(c["costo_livellato"])
        self.assertIsNone(c["breakeven_p0"])
        with self.assertRaises(ValueError):
            mh898_confronto(-1.0, 45980269.12, 4312130.15,
                            7989849.71, 12000000.0, 300000.0,
                            61.80, 54.55)

    def test_co2_evitata_informativa(self):
        self.assertEqual(mh898_co2_evitata(100000.0, 0.30, 10),
                         300000.0)
        self.assertEqual(mh898_co2_evitata(100000.0, 0.50, 10),
                         500000.0)
        self.assertEqual(mh898_co2_evitata(100000.0, 0.0, 10), 0.0)
        self.assertEqual(mh898_co2_evitata(100000.0, 0.30, 5),
                         150000.0)
        with self.assertRaises(ValueError):
            mh898_co2_evitata(100000.0, -0.1, 10)
        with self.assertRaises(ValueError):
            mh898_co2_evitata(-1.0, 0.30, 10)
        with self.assertRaises(ValueError):
            mh898_co2_evitata(100000.0, 0.30, 0)


class TestFinanza(unittest.TestCase):
    def test_van_tasso_cinque(self):
        bc = mh898_demo_calcoli()
        self.assertAlmostEqual(
            mh898_van(bc["flussi"], 0.05),
            bc["van"])
        bc_basso = mh898_calcola(
            _scenari=False,
            **dict(mh898_demo(), prezzo_eua_p0=50.0))
        self.assertAlmostEqual(
            mh898_van(bc_basso["flussi"], 0.05),
            bc["scenari"][2]["van"])

    def test_van_tasso_zero_sollevata(self):
        # Il tasso zero e degenere in questa scheda (tasso
        # maggiore di 0): la VAN con tasso zero solleva.
        with self.assertRaises(ValueError):
            mh898_van([-12000000, 2250000, 2326500], 0)

    def test_van_tasso_frazione_non_percentuale(self):
        # Il tasso e' in FRAZIONE (0,05 = 5 %): usato
        # diretto, NON diviso per 100. Con 0,05 la VAN
        # demo e' 7989849,71; con 0,50 (cioe' 50 %)
        # sarebbe tutt'altra; con 5,0 (cioe' 500 % se
        # letto come frazione) il tasso e' degenere
        # (maggiore o uguale a 1) e solleva ValueError.
        bc = mh898_demo_calcoli()
        self.assertAlmostEqual(
            mh898_van(bc["flussi"], 0.05),
            7989849.71, places=2)
        self.assertNotAlmostEqual(
            mh898_van(bc["flussi"], 0.50),
            7989849.71, places=2)
        with self.assertRaises(ValueError):
            mh898_van(bc["flussi"], 5.0)

    def test_tir_demo(self):
        bc = mh898_demo_calcoli()
        tir = mh898_tir(bc["flussi"])
        self.assertIsNotNone(tir)
        self.assertAlmostEqual(tir * 100.0, bc["tir"], places=6)

    def test_tir_none_senza_cambio_segno(self):
        self.assertIsNone(mh898_tir([-100, -10, -10]))
        self.assertIsNone(mh898_tir([100, 10, 10]))
        self.assertIsNone(mh898_tir([0, 10, 10]))

    def test_tir_none_doppio_cambio_segno(self):
        # Flussi con due cambi di segno (crescita prezzo
        # meno 0,5: il risparmio cala e diventa negativo):
        # la TIR non e definita.
        bc = mh898_calcola(
            **_demo_kwargs(crescita_prezzo=-0.5))
        self.assertIsNone(mh898_tir(bc["flussi"]))
        self.assertIsNone(bc["tir"])

    def test_payback_demo_e_regola_cumulato(self):
        bc = mh898_demo_calcoli()
        self.assertEqual(mh898_payback(bc["flussi"]), 5)
        # Il cumulato nullo basta (regola maggiore o
        # uguale a zero).
        self.assertEqual(mh898_payback([-100, 100, 10]), 1)
        self.assertEqual(mh898_payback([-100, 50, 50, 10]), 2)
        self.assertIsNone(mh898_payback([-100, 10, 10]))
        # Con CAPEX zero il payback e l'anno 1.
        self.assertEqual(mh898_payback([0, 50, 10]), 1)

    def test_payback_demo_cumulati(self):
        bc = mh898_demo_calcoli()
        f0 = bc["flussi"]
        self.assertAlmostEqual(sum(f0[:5]), -2531751.15, places=2)
        self.assertAlmostEqual(sum(f0[:6]), 38296.32, places=2)
        self.assertAlmostEqual(sum(f0), 14232892.24, places=2)

    def test_verdetto_bordi(self):
        self.assertEqual(mh898_verdetto(100.0, 12000000, 0.10),
                         "CONVIENTE")
        self.assertEqual(mh898_verdetto(-500000.0, 12000000, 0.10),
                         "MARGINALE")
        self.assertEqual(mh898_verdetto(-2000000.0, 12000000, 0.10),
                         "NON_CONVIENTE")
        # VAN zero: CONVIENTE in questa scheda (VAN
        # maggiore o uguale a 0, come da brief).
        self.assertEqual(mh898_verdetto(0.0, 12000000, 0.10),
                         "CONVIENTE")
        # VAN esattamente alla tolleranza: MARGINALE (inclusa).
        self.assertEqual(mh898_verdetto(-1200000.0, 12000000, 0.10),
                         "MARGINALE")
        self.assertEqual(mh898_verdetto(-1200000.01, 12000000, 0.10),
                         "NON_CONVIENTE")
        # Con tolleranza zero solo VAN zero e' CONVIENTE.
        self.assertEqual(mh898_verdetto(-1.0, 12000000, 0.0),
                         "NON_CONVIENTE")
        self.assertEqual(mh898_verdetto(0.0, 12000000, 0.0),
                         "CONVIENTE")
        # La tolleranza e in FRAZIONE (0,10 = 10 %):
        # con 10 (cioe 1000 % se letta come frazione)
        # il validatore solleva.
        with self.assertRaises(ValueError):
            mh898_verdetto(-500000.0, 12000000, 10)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(mh898_verdetto(None, 12000000, 0.10),
                         "NON_CALCOLABILE")

    def test_valida_demo_ok(self):
        demo = mh898_demo()
        val = mh898_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_e_non_intera_no(self):
        kw = _demo_kwargs(vita_anni=0)
        self.assertRaises(ValueError, mh898_calcola, **kw)
        kw = _demo_kwargs(vita_anni=10.5)
        self.assertRaises(ValueError, mh898_calcola, **kw)
        kw = _demo_kwargs(vita_anni=5)
        bc = mh898_calcola(**kw)
        self.assertEqual(bc["vita_anni"], 5)

    def test_valida_tasso_zero_e_uno_no(self):
        for tasso in (0, 1, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh898_calcola(**_demo_kwargs(tasso=tasso))
        bc = mh898_calcola(**_demo_kwargs(tasso=0.10))
        self.assertEqual(bc["tasso"], 0.10)

    def test_valida_decadimento_uno_no(self):
        for dec in (1.0, 1.5, -0.01):
            with self.assertRaises(ValueError):
                mh898_calcola(
                    **_demo_kwargs(decadimento_allocazione=dec))
        bc = mh898_calcola(
            **_demo_kwargs(decadimento_allocazione=0.0))
        self.assertEqual(bc["decadimento_allocazione"], 0.0)

    def test_valida_crescita_fuori_range_no(self):
        for g in (-0.91, 1.01, -1.0):
            with self.assertRaises(ValueError):
                mh898_calcola(**_demo_kwargs(crescita_prezzo=g))
        bc = mh898_calcola(**_demo_kwargs(crescita_prezzo=-0.5))
        self.assertEqual(bc["crescita_prezzo"], -0.5)

    def test_valida_zeri_bloccati_no(self):
        for campo, valore in (("p_mw", 0),
                              ("ore_annue", 0),
                              ("fattore_emissione", 0)):
            with self.assertRaises(ValueError):
                mh898_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_fattore_sopra_uno_no(self):
        kw = _demo_kwargs(fattore_emissione=1.5)
        self.assertRaises(ValueError, mh898_calcola, **kw)
        self.assertFalse(mh898_valida(*[kw[k] for k in _ORDINE_VALIDA])["valido"])

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_eua_p0=float("nan"))
        self.assertRaises(ValueError, mh898_calcola, **kw)
        kw = _demo_kwargs(decadimento_allocazione=float("inf"))
        self.assertRaises(ValueError, mh898_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (("p_mw", -1),
                              ("ore_annue", -1),
                              ("fattore_emissione", -0.1),
                              ("allocazione_a0", -1),
                              ("decadimento_allocazione", -0.01),
                              ("prezzo_eua_p0", -1),
                              ("abbattimento_r", -0.1),
                              ("capex_eur", -1),
                              ("om_eur_anno", -1),
                              ("tasso", -0.01),
                              ("copertura_frazione", -0.1),
                              ("tolleranza_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh898_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_frazioni_sopra_uno_no(self):
        for campo in ("fattore_emissione", "abbattimento_r",
                      "copertura_frazione", "tolleranza_frazione"):
            with self.assertRaises(ValueError):
                mh898_calcola(**_demo_kwargs(**{campo: 1.5}))

    def test_calcola_accetta_dict(self):
        bc = mh898_calcola(mh898_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 5)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh898_calcola(dict(mh898_demo(), prezzo_eua_p0=999.0),
                           prezzo_eua_p0=85.0)
        self.assertEqual(bc["prezzo_eua_p0"], 85.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh898_calcola(_scenari=False, **mh898_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van"], 7989849.71, places=2)


class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo_scalari(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO_SCALARI.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, int):
                    self.assertEqual(ottenuto, atteso)
                else:
                    self.assertLess(_rel(ottenuto, atteso), 1e-9)

    def test_demo_scenari(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["scenari"]), len(_DEMO_SCENARI))
        for i, atteso in enumerate(_DEMO_SCENARI):
            for chiave, valore in atteso.items():
                with self.subTest(scenario=i, chiave=chiave):
                    ottenuto = bc["scenari"][i][chiave]
                    if valore is None or isinstance(valore, (int, str)):
                        self.assertEqual(ottenuto, valore)
                    else:
                        self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_confronto(self):
        bc = demo_calcoli()
        for chiave, valore in _DEMO_CONFRONTO.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc["confronto"][chiave]
                if isinstance(valore, bool):
                    self.assertEqual(ottenuto, valore)
                else:
                    self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_verdetto_principale(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertGreater(bc["van"], 0.0)
        self.assertEqual(bc["payback"], 5)
        self.assertAlmostEqual(bc["tir"], 16.40, places=2)
        self.assertAlmostEqual(bc["breakeven_p0"], 54.55, places=2)
        self.assertAlmostEqual(bc["costo_livellato"], 61.80,
                               places=2)
        self.assertAlmostEqual(bc["crf"], 0.129505, places=6)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["energia_mwh_anno"],
            bc["p_mw"] * bc["ore_annue"])
        self.assertAlmostEqual(
            bc["emissioni_base_t_anno"],
            bc["energia_mwh_anno"] * bc["fattore_emissione"])
        self.assertAlmostEqual(
            bc["emissioni_abbattute_t_anno"],
            bc["emissioni_base_t_anno"]
            * (1.0 - bc["abbattimento_r"]))
        self.assertAlmostEqual(
            bc["allocazione_anno10"],
            bc["allocazione_a0"]
            * (1.0 - bc["decadimento_allocazione"]) ** 9)
        self.assertAlmostEqual(
            bc["prezzo_anno10"],
            bc["prezzo_eua_p0"]
            * (1.0 + bc["crescita_prezzo"]) ** 9)
        self.assertAlmostEqual(
            bc["deficit_base_anno1"],
            bc["emissioni_base_t_anno"]
            - bc["allocazione_anno1"])
        self.assertAlmostEqual(
            bc["costo_base_anno1"],
            bc["deficit_base_anno1"] * bc["prezzo_anno1"])
        self.assertAlmostEqual(
            bc["risparmio_anno1"],
            bc["costo_base_anno1"]
            - bc["costo_abbattuto_anno1"] - bc["om_eur_anno"])
        self.assertAlmostEqual(
            bc["costo_livellato"],
            (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"])
            / (bc["emissioni_base_t_anno"]
               * bc["abbattimento_r"]))
        self.assertAlmostEqual(
            bc["co2_evitata_t"],
            bc["emissioni_base_t_anno"]
            * bc["abbattimento_r"] * bc["vita_anni"])
        self.assertAlmostEqual(
            bc["van"],
            mh898_van(bc["flussi"], bc["tasso"]))
        self.assertAlmostEqual(
            bc["pv_spot"],
            mh898_pv_spot(bc["serie"], bc["tasso"]))
        self.assertAlmostEqual(
            bc["pv_copertura"],
            mh898_pv_copertura(bc["serie"], bc["prezzo_eua_p0"],
                               bc["copertura_frazione"],
                               bc["tasso"]))
        self.assertAlmostEqual(
            bc["risparmio_pv"],
            bc["pv_spot"] - bc["pv_copertura"])
        self.assertAlmostEqual(
            bc["breakeven_p0"],
            mh898_breakeven_p0(mh898_demo()))
        for t in range(1, bc["vita_anni"] + 1):
            riga = bc["serie"][t - 1]
            with self.subTest(anno=t):
                self.assertAlmostEqual(
                    riga["risparmio"],
                    (riga["d_base"] - riga["d_ab"])
                    * riga["prezzo"] - bc["om_eur_anno"])
                self.assertEqual(riga["d_base"],
                                 max(bc["emissioni_base_t_anno"]
                                     - riga["allocazione"], 0.0))
                self.assertEqual(riga["d_ab"],
                                 max(bc["emissioni_abbattute_t_anno"]
                                     - riga["allocazione"], 0.0))
        conf = bc["confronto"]
        self.assertAlmostEqual(
            conf["risparmio_pv"],
            conf["pv_spot"] - conf["pv_copertura"])
        self.assertEqual(conf["van"], bc["van"])
        self.assertEqual(conf["capex"], bc["capex_eur"])

    def test_scenari_ordinamento(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # L'EUA alto migliora sul base, l'EUA basso peggiora
        # e diventa MARGINALE, l'abbattimento 50 % migliora
        # piu di tutti, la crescita zero peggiora sul base
        # ma resta conveniente.
        self.assertGreater(bc["scenari"][1]["van"], base["van"])
        self.assertGreater(bc["scenari"][1]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][1]["payback"], 4)
        self.assertLess(bc["scenari"][2]["van"], base["van"])
        self.assertLess(bc["scenari"][2]["tir"], base["tir"])
        self.assertEqual(bc["scenari"][2]["payback"], 9)
        self.assertEqual(bc["scenari"][2]["verdetto"], "MARGINALE")
        self.assertGreater(bc["scenari"][3]["van"],
                           bc["scenari"][1]["van"])
        self.assertEqual(bc["scenari"][3]["payback"], 3)
        self.assertLess(bc["scenari"][4]["van"], base["van"])
        self.assertEqual(bc["scenari"][4]["payback"], 6)
        # Con crescita zero il breakeven coincide col
        # costo livellato.
        self.assertAlmostEqual(
            bc["scenari"][4]["breakeven_p0"],
            bc["scenari"][4]["costo_livellato"], places=6)

    def test_sensibilita_valori(self):
        s = mh898_sensibilita(**mh898_demo())
        self.assertEqual(set(s.keys()),
                         {"p0_130", "p0_050", "r_050", "g_000",
                          "vita_005", "tasso_010", "om_000",
                          "capex_000", "a0_000", "d_000",
                          "f_050"})
        attesi = {
            "p0_130": (19799104.52, 30.31, 4, "CONVIENTE"),
            "p0_050": (-1195126.25, 3.01, 9, "MARGINALE"),
            "r_050": (22860763.17, 33.65, 3, "CONVIENTE"),
            "g_000": (5373903.59, 13.43, 6, "CONVIENTE"),
            "vita_005": (-1609843.34, 0.10, 5, "NON_CONVIENTE"),
            "tasso_010": (3710176.28, 16.40, 5, "CONVIENTE"),
            "om_000": (10306370.19, 19.40, 5, "CONVIENTE"),
            "capex_000": (19989849.71, None, 1, "CONVIENTE"),
            "a0_000": (7989849.71, 16.40, 5, "CONVIENTE"),
            "d_000": (7989849.71, 16.40, 5, "CONVIENTE"),
            "f_050": (13566442.26, 23.24, 4, "CONVIENTE"),
        }
        for nome, (van, tir, pb, verd) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(s[nome]["van"], van, places=2)
                if tir is None:
                    self.assertIsNone(s[nome]["tir"])
                else:
                    self.assertAlmostEqual(s[nome]["tir"], tir,
                                           places=2)
                self.assertEqual(s[nome]["payback"], pb)
                self.assertEqual(s[nome]["verdetto"], verd)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh898_csv(bc, mh898_demo())
        for voce in ("p_mw", "ore_annue", "fattore_emissione",
                     "allocazione_a0", "decadimento_allocazione",
                     "prezzo_eua_p0", "crescita_prezzo",
                     "abbattimento_r", "capex_eur", "om_eur_anno",
                     "vita_anni", "tasso", "copertura_frazione",
                     "tolleranza_frazione", "energia_mwh_anno",
                     "emissioni_base_t_anno",
                     "emissioni_abbattute_t_anno",
                     "allocazione_anno1", "allocazione_anno10",
                     "prezzo_anno1", "prezzo_anno10",
                     "deficit_base_anno1",
                     "deficit_abbattuto_anno1",
                     "deficit_base_anno10",
                     "deficit_abbattuto_anno10",
                     "costo_base_anno1", "costo_abbattuto_anno1",
                     "risparmio_anno1", "costo_base_anno10",
                     "costo_abbattuto_anno10",
                     "risparmio_anno10", "crf",
                     "costo_livellato", "breakeven_p0",
                     "pv_spot", "pv_copertura", "risparmio_pv",
                     "co2_evitata_t", "van", "tir", "payback",
                     "scenario_base_van", "scenario_base_tir",
                     "scenario_base_verdetto",
                     "scenario_eua_alto_van",
                     "scenario_eua_alto_verdetto",
                     "scenario_eua_basso_van",
                     "scenario_eua_basso_verdetto",
                     "scenario_abbattimento_50_van",
                     "scenario_abbattimento_50_verdetto",
                     "scenario_crescita_0_van",
                     "scenario_crescita_0_verdetto",
                     "anno_1_allocazione", "anno_1_prezzo",
                     "anno_1_deficit_base", "anno_1_risparmio",
                     "anno_10_allocazione", "anno_10_prezzo",
                     "anno_10_deficit_base",
                     "anno_10_risparmio",
                     "confronto_pv_spot",
                     "confronto_pv_copertura",
                     "confronto_risparmio_pv",
                     "confronto_van", "confronto_capex",
                     "confronto_co2_evitata_t",
                     "confronto_costo_livellato",
                     "confronto_breakeven_p0",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_df_annua_scenari_confronto_tabella(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_annua"]), 10)
        self.assertEqual(len(bc["df_scenari"]), 5)
        self.assertEqual(len(bc["df_confronto"]), 8)
        self.assertEqual(len(bc["df_tabella"]), 42)
        self.assertEqual(bc["df_annua"]["Anno"].iloc[0], 1)
        self.assertAlmostEqual(
            bc["df_annua"]["Flusso (EUR)"].iloc[0],
            2250000.0, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[4],
            38296.32, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Cumulato (EUR)"].iloc[-1],
            14232892.24, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Risparmio (EUR/anno)"].iloc[9],
            3027171.62, places=2)
        self.assertAlmostEqual(
            bc["df_annua"]["Costo base (EUR/anno)"].iloc[9],
            8294641.46, places=2)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["PV compliance spot (EUR)",
             "PV compliance con copertura (EUR)",
             "Risparmio PV copertura (EUR)",
             "CAPEX abbattimento (EUR)",
             "VAN investimento (EUR)",
             "CO2 evitata vita (t)",
             "Costo abbattimento livellato (EUR/t)",
             "Breakeven p0 (EUR/t)"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            50292399.26, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[2],
            4312130.15, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Energia (MWh/anno)", voci)
        self.assertIn("Emissioni base E0 (t/anno)", voci)
        self.assertIn("Costo abbattimento livellato (EUR/t)", voci)
        self.assertIn("CO2 evitata vita (t)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto", set(bc["df_scenari"].columns))

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh898_csv(bc, mh898_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("p_mw;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh898_demo_calcoli()["van"],
                         demo_calcoli()["van"])
        self.assertEqual(mh898_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_zero_ammessi(self):
        bc = mh898_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertAlmostEqual(bc["van"], 19989849.71, places=2)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh898_calcola(**_demo_kwargs(om_eur_anno=0.0))
        self.assertEqual(bc["om_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van"], 10306370.19, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh898_calcola(**_demo_kwargs(copertura_frazione=0.0))
        self.assertAlmostEqual(bc["pv_copertura"], bc["pv_spot"])
        self.assertEqual(bc["risparmio_pv"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh898_calcola(**_demo_kwargs(copertura_frazione=1.0))
        self.assertLess(bc["pv_copertura"], bc["pv_spot"])
        self.assertAlmostEqual(bc["van"], 7989849.71, places=2)
        bc = mh898_calcola(**_demo_kwargs(allocazione_a0=0.0))
        self.assertAlmostEqual(bc["van"], 7989849.71, places=2)
        self.assertAlmostEqual(bc["pv_spot"], 74354567.30,
                               places=2)
        bc = mh898_calcola(
            **_demo_kwargs(decadimento_allocazione=0.0))
        self.assertAlmostEqual(bc["van"], 7989849.71, places=2)
        self.assertAlmostEqual(bc["pv_spot"], 44612740.38,
                               places=2)


class TestCasiLimite(unittest.TestCase):
    def test_abbattimento_zero_non_calcolabile(self):
        # Senza abbattimento non c'e risparmio: S(t)
        # uguale a meno O&M in tutti gli anni, VAN None,
        # NON_CALCOLABILE negli helper e guard
        # NON_CALCOLABILE in UI.
        kw = _demo_kwargs(abbattimento_r=0.0)
        bc = mh898_calcola(**kw)
        self.assertTrue(all(r["risparmio"] == -300000.0
                            for r in bc["serie"]))
        self.assertIsNone(bc["van"])
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertIsNone(bc["breakeven_p0"])
        self.assertIsNone(bc["costo_livellato"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        # I PV compliance restano calcolati anche nel
        # regime degenere (sono costi, non KPI di
        # investimento).
        self.assertAlmostEqual(bc["pv_spot"], 50292399.26,
                               places=2)

    def test_prezzo_zero_non_calcolabile(self):
        kw = _demo_kwargs(prezzo_eua_p0=0.0)
        bc = mh898_calcola(**kw)
        self.assertTrue(all(r["risparmio"] == -300000.0
                            for r in bc["serie"]))
        self.assertEqual(bc["pv_spot"], 0.0)
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_om_enorme_non_calcolabile(self):
        # O&M 10.000.000: il risparmio anno 1 e meno
        # 7.450.000 e resta negativo in tutti gli anni.
        kw = _demo_kwargs(om_eur_anno=10000000.0)
        bc = mh898_calcola(**kw)
        self.assertEqual(bc["risparmio_anno1"], -7450000.0)
        self.assertTrue(all(r["risparmio"] <= 0.0
                            for r in bc["serie"]))
        self.assertIsNone(bc["van"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_allocazione_centomila_marginale(self):
        # Allocazione 100.000: il risparmio anno 1 e
        # meno 300.000 ma diventa positivo dall'anno 2
        # (137.750,00), VAN meno 857.938,77,
        # TIR 3,95 %, payback 9, MARGINALE.
        bc = mh898_calcola(
            **_demo_kwargs(allocazione_a0=100000.0))
        self.assertEqual(bc["risparmio_anno1"], -300000.0)
        self.assertAlmostEqual(bc["serie"][1]["risparmio"],
                               137750.00, places=2)
        self.assertGreater(bc["serie"][1]["risparmio"], 0.0)
        self.assertAlmostEqual(bc["serie"][7]["d_ab"], 166.27,
                               places=2)
        self.assertAlmostEqual(bc["van"], -857938.77, places=2)
        self.assertAlmostEqual(bc["tir"], 3.95, places=2)
        self.assertEqual(bc["payback"], 9)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_abbattimento_dieci_non_conveniente(self):
        # Abbattimento 10 %: poco delta, VAN meno
        # 6.881.063,75, TIR meno 8,84 %, payback nessuno.
        bc = mh898_calcola(
            **_demo_kwargs(abbattimento_r=0.10))
        self.assertAlmostEqual(bc["van"], -6881063.75, places=2)
        self.assertAlmostEqual(bc["tir"], -8.84, places=2)
        self.assertIsNone(bc["payback"])
        self.assertAlmostEqual(bc["costo_livellato"], 185.41,
                               places=2)
        self.assertAlmostEqual(bc["breakeven_p0"], 163.66,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_ore_quattromila(self):
        bc = mh898_calcola(**_demo_kwargs(ore_annue=4000))
        self.assertEqual(bc["energia_mwh_anno"], 200000.0)
        self.assertEqual(bc["emissioni_base_t_anno"], 80000.0)
        self.assertAlmostEqual(bc["van"], 3528575.67, places=2)
        self.assertAlmostEqual(bc["tir"], 10.36, places=2)
        self.assertEqual(bc["payback"], 7)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_tir_non_definita_payback_uno(self):
        bc = mh898_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertIsNone(bc["tir"])
        self.assertEqual(bc["payback"], 1)
        self.assertAlmostEqual(bc["costo_livellato"], 10.00,
                               places=2)
        self.assertAlmostEqual(bc["breakeven_p0"], 8.83,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_vita_cinque_e_tasso_dieci(self):
        bc = mh898_calcola(**_demo_kwargs(vita_anni=5))
        self.assertAlmostEqual(bc["van"], -1609843.34, places=2)
        self.assertAlmostEqual(bc["tir"], 0.10, places=2)
        self.assertEqual(bc["payback"], 5)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh898_calcola(**_demo_kwargs(tasso=0.10))
        self.assertAlmostEqual(bc["van"], 3710176.28, places=2)
        self.assertAlmostEqual(bc["tir"], 16.40, places=2)
        self.assertEqual(bc["payback"], 5)

    def test_tolleranza_zero_bordo(self):
        # Con tolleranza zero ogni VAN negativa e'
        # NON_CONVIENTE, anche lo scenario EUA basso.
        bc = mh898_calcola(
            **_demo_kwargs(prezzo_eua_p0=50.0,
                           tolleranza_frazione=0.0))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "NON_CONVIENTE")
        bc = mh898_calcola(
            **_demo_kwargs(prezzo_eua_p0=130.0,
                           tolleranza_frazione=0.0))
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_crescita_negativa_tir_non_definita(self):
        # Crescita prezzo meno 0,5: il risparmio cala e
        # diventa negativo, i flussi cambiano segno due
        # volte, TIR non definita, payback nessuno.
        bc = mh898_calcola(
            **_demo_kwargs(crescita_prezzo=-0.5))
        self.assertAlmostEqual(bc["van"], -9682936.46, places=2)
        self.assertIsNone(bc["tir"])
        self.assertIsNone(bc["payback"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_fattore_uno(self):
        bc = mh898_calcola(
            **_demo_kwargs(fattore_emissione=1.0))
        self.assertEqual(bc["emissioni_base_t_anno"], 250000.0)
        self.assertAlmostEqual(bc["van"], 41449405.00, places=2)
        self.assertAlmostEqual(bc["tir"], 52.77, places=2)
        self.assertEqual(bc["payback"], 2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(p_mw="50.0")
        self.assertRaises(ValueError, mh898_calcola, **kw)
        kw = _demo_kwargs(p_mw=True)
        self.assertRaises(ValueError, mh898_calcola, **kw)
        val = mh898_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def898\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh898_demo().keys()), lette - set(mh898_demo().keys()))
        self.assertEqual(lette, set(mh898_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc898\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc898\["([^"]+)"\]', src))
        attese = set(mh898_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 897 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 898.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 901)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab898:"), 1)
        self.assertTrue(src.startswith("    # W903"))

    def test_ui_tab898_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab898:"), 1)
        self.assertIn("def mh898_demo(", src_h)
        self.assertIn("def mh898_calcola(", src_h)
        self.assertIn("tab898", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("EU ETS: le quote CO2 dell'impianto, comprare, coprirsi o abbattere?", src)
        self.assertIn("🌍📜 EU ETS: le quote CO2 dell'impianto — comprare, coprirsi o abbattere?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st898_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st898_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 20)
        self.assertIn('key="st898_calcola"', src)
        self.assertIn('key="st898_csv"', src)
        self.assertIn('key="st898_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg898"), src.index(".paiac("))
        self.assertIn("st.stop()", src)
        self.assertIn("not _any_pos898", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"st\.slider\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)

    def test_ui_nessun_trattino_lungo(self):
        # Il titolo prescritto della scheda
        # contiene un trattino lungo nella riga
        # h1: quella riga e' esclusa dal controllo,
        # tutto il resto deve esserne privo.
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            righe = [r for r in src.split("\n") if "<h1>" not in r]
            testo = "\n".join(righe)
            self.assertNotIn(chr(8212), testo)
            self.assertNotIn(chr(8211), testo)

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato) e salvo la
        # riga h1 col titolo prescritto (contiene
        # un trattino lungo).
        import textwrap as _tw
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            if percorso == _UI_PATH:
                src = _tw.dedent(src)
            tree = ast.parse(src)
            for nodo in ast.walk(tree):
                if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                    if nodo.value == "utf-8":
                        continue
                    if "<h1>" in nodo.value:
                        continue
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)


if __name__ == "__main__":
    unittest.main()
