"""Test tab493 '💸⏳ Costo dell'attesa: il budget di rischio consumato': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh493_num", "mh493_segno", "mh493_mese", "mh493_z",
           "mh493_phi", "mh493_Phi", "mh493_lambda",
           "mh493_mult", "mh493_limite", "mh493_halflife", "mh493_orizzonte",
           "mh493_budget",
           "mh493_dv01_linea", "mh493_sigma_mtm_linea",
           "mh493_es_linea", "mh493_riga", "mh493_portafoglio",
           "mh493_es_t", "mh493_t_rientro",
           "mh493_eccesso_t", "mh493_integrale_chiusa",
           "mh493_integrale_eccesso",
           "mh493_giorni_equivalenti", "mh493_frazione_budget",
           "mh493_cumulata", "mh493_curva",
           "mh493_verdetto")

TITLE493 = "💸⏳ Costo dell'attesa: il budget di rischio consumato"
TITLE492 = "⏳🌪️ Decadimento dello stress: aspettare o coprire?"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo A: linea singola long TTF 100k MWh, scadenza 2027-01, f_now 88.00,
# vol giornaliera 2.5% -> sigma_mtm = 220000 (stessi numeri tab491/tab492).
SIGMA_MTM_A = 220000.0
ES_BASE_A = 586347.1284759773
ES_STRESS_A = 1172694.2569519547

# Demo A: limite 800k, emivita 10 gg, orizzonte 90 gg, budget = limite x 30.
LIMITE_A = 800000.0
HL_A = 10.0
ORIZ_A = 90
BUDGET_A = 24000000.0
T_STAR_A = 14.564863128705067
INTEGRALE_A = 2265016.7319216225
NEQ_A = 2.8312709149020283
FRAC_A = 0.09437569716340094

# Demo B: portafoglio 3 linee (come tab491/tab492), z 99%, stress x2,
# limite 3M EUR, emivita 10 gg, orizzonte 90 gg, budget 90M EUR*giorni.
POS_B = [
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00,
     "f_now": 88.00, "sigma_pct": 2.5},
    {"commodity": "TTF gas", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 91.00,
     "f_now": 90.00, "sigma_pct": 2.5},
    {"commodity": "Power baseload DE", "scadenza": "2027-03",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 110.00,
     "f_now": 116.00, "sigma_pct": 1.8},
]
LIMITE_B = 3000000.0
HL_B = 10.0
ORIZ_B = 90
BUDGET_B = 90000000.0
ES_BASE_B = 1999177.1866813889
ES_STRESS_B = 3998354.3733627778
T_STAR_B = 9.982197629332461
INTEGRALE_B = 4412797.920512
FRAC_B = 0.04903108800568889


def _righe_b():
    return [_F["mh493_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


def _pf_b():
    return _F["mh493_portafoglio"](_righe_b(), Z99, 2.0)


def test_registry_tab493():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    assert f'"{TITLE493}"' in src
    assert "tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661 = st.tabs([" in src
    assert "    with tab493:" in src
    # ordine: tab493 dopo tab492 nella dichiarazione
    i92 = src.index(f'"{TITLE492}"')
    i93 = src.index(f'"{TITLE493}"')
    assert i92 < i93


def test_lambda99():
    assert abs(_F["mh493_lambda"](Z99) - LAMBDA99) < 1e-12


def test_riga_demo_a():
    r = _F["mh493_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00, 88.00, 2.5)
    assert abs(r["sigma_mtm"] - SIGMA_MTM_A) < 1e-9
    assert r["scadenza"] == "2027-01"


def test_portafoglio_b():
    pf = _pf_b()
    assert abs(pf["es_base_cons"] - ES_BASE_B) < 1e-6
    assert abs(pf["es_stress_cons"] - ES_STRESS_B) < 1e-6
    for b, s in zip(pf["es_base_linee"], pf["es_stress_linee"]):
        assert abs(s - 2.0 * b) < 1e-6


def test_t_rientro_demo_a():
    t = _F["mh493_t_rientro"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A)
    assert abs(t - T_STAR_A) < 1e-9
    # a t* l'eccesso e' zero
    assert abs(_F["mh493_eccesso_t"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, t)) < 1e-6


def test_eccesso_t():
    x0 = _F["mh493_eccesso_t"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, 0.0)
    assert abs(x0 - (ES_STRESS_A - LIMITE_A)) < 1e-9
    # monotono decrescente, mai negativo
    ts = [0.0, 1.0, 5.0, 10.0, 14.0, 20.0, 90.0]
    xs = [_F["mh493_eccesso_t"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, t)
          for t in ts]
    assert all(xs[i] >= xs[i + 1] for i in range(len(xs) - 1))
    assert all(x >= 0.0 for x in xs)
    assert xs[-1] == 0.0


def test_integrale_demo_a():
    i = _F["mh493_integrale_eccesso"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                                      T_STAR_A)
    assert abs(i - INTEGRALE_A) < 1e-6
    # t_rientro 0 -> integrale 0
    assert _F["mh493_integrale_eccesso"](ES_BASE_A, ES_STRESS_A, 3000000.0,
                                         HL_A, 0.0) == 0.0
    # verifica indipendente: integrale numerico (trapezi fini)
    n = 20000
    h = T_STAR_A / n
    s = sum(_F["mh493_eccesso_t"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                                  (k + 0.5) * h) for k in range(n)) * h
    assert abs(s - i) / i < 1e-6


def test_giorni_equivalenti():
    neq = _F["mh493_giorni_equivalenti"](INTEGRALE_A, LIMITE_A)
    assert abs(neq - NEQ_A) < 1e-9
    # N_eq < t*: l'eccesso decade, non resta a limite pieno
    assert neq < T_STAR_A
    assert _F["mh493_giorni_equivalenti"](0.0, LIMITE_A) == 0.0


def test_frazione_budget():
    fr = _F["mh493_frazione_budget"](INTEGRALE_A, BUDGET_A)
    assert abs(fr - FRAC_A) < 1e-12
    assert _F["mh493_frazione_budget"](BUDGET_A, BUDGET_A) == 1.0
    assert _F["mh493_frazione_budget"](0.0, BUDGET_A) == 0.0


def test_cumulata():
    c0 = _F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                               T_STAR_A, 0.0)
    assert c0 == 0.0
    # a t* la cumulata coincide con l'integrale
    c_star = _F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                                   T_STAR_A, T_STAR_A)
    assert abs(c_star - INTEGRALE_A) < 1e-9
    # oltre t* resta piatta
    c_oltre = _F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                                   T_STAR_A, 3 * T_STAR_A)
    assert c_oltre == c_star
    # monotona non decrescente
    ts = [0.0, 2.0, 7.0, 14.0, 30.0, 90.0]
    cs = [_F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                               T_STAR_A, t) for t in ts]
    assert all(cs[i] <= cs[i + 1] for i in range(len(cs) - 1))


def test_curva():
    cv = _F["mh493_curva"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, 7,
                            T_STAR_A)
    assert len(cv) == 8
    assert cv[0][0] == 0.0 and cv[-1][0] == 7.0
    t, e, x, c = cv[0]
    assert abs(e - ES_STRESS_A) < 1e-9
    assert abs(x - (ES_STRESS_A - LIMITE_A)) < 1e-9
    assert c == 0.0
    # coerenza riga per riga con le funzioni atomiche
    for t, e, x, c in cv:
        assert abs(e - _F["mh493_es_t"](ES_BASE_A, ES_STRESS_A, t, HL_A)) < 1e-9
        assert abs(x - _F["mh493_eccesso_t"](ES_BASE_A, ES_STRESS_A, LIMITE_A,
                                             HL_A, t)) < 1e-9
        assert abs(c - _F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A,
                                            HL_A, T_STAR_A, t)) < 1e-9


def test_verdetto_sostenibile_a():
    v = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A,
                              BUDGET_A)
    assert v["codice"] == "SOSTENIBILE"
    assert abs(v["t_rientro_giorni"] - T_STAR_A) < 1e-9
    assert abs(v["integrale_eur_giorni"] - INTEGRALE_A) < 1e-6
    assert abs(v["giorni_equivalenti"] - NEQ_A) < 1e-9
    assert abs(v["frazione_budget"] - FRAC_A) < 1e-12


def test_verdetto_sostenibile_b():
    pf = _pf_b()
    v = _F["mh493_verdetto"](pf["es_base_cons"], pf["es_stress_cons"],
                              LIMITE_B, HL_B, ORIZ_B, BUDGET_B)
    assert v["codice"] == "SOSTENIBILE"
    assert abs(v["t_rientro_giorni"] - T_STAR_B) < 1e-9
    assert abs(v["integrale_eur_giorni"] - INTEGRALE_B) < 1e-3
    assert abs(v["frazione_budget"] - FRAC_B) < 1e-12


def test_verdetto_ok_stress():
    v = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, 3000000.0, HL_A, ORIZ_A,
                              BUDGET_A)
    assert v["codice"] == "OK_STRESS"
    assert v["t_rientro_giorni"] == 0.0
    assert v["integrale_eur_giorni"] == 0.0
    assert v["frazione_budget"] == 0.0


def test_verdetto_mai():
    v = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, 400000.0, HL_A, ORIZ_A,
                              BUDGET_A)
    assert v["codice"] == "MAI"
    assert v["t_rientro_giorni"] is None
    assert v["integrale_eur_giorni"] is None


def test_verdetto_oltre_orizzonte():
    v = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, 7,
                              BUDGET_A)
    assert v["codice"] == "OLTRE_ORIZZONTE"
    assert v["t_rientro_giorni"] > 7
    assert v["integrale_eur_giorni"] > 0.0


def test_verdetto_elevato():
    # budget tale che la frazione sia 60% -> ELEVATO
    b = INTEGRALE_A / 0.6
    v = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A, b)
    assert v["codice"] == "ELEVATO"
    assert abs(v["frazione_budget"] - 0.6) < 1e-12


def test_verdetto_budget_sfondato():
    # budget = meta' dell'integrale -> frazione 200%
    b = INTEGRALE_A / 2.0
    v = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A, b)
    assert v["codice"] == "BUDGET_SFONDATO"
    assert abs(v["frazione_budget"] - 2.0) < 1e-12


def test_verdetto_soglie():
    # frazione esattamente 0.5 -> ELEVATO; esattamente 1.0 -> BUDGET_SFONDATO
    v50 = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A,
                                INTEGRALE_A / 0.5)
    assert v50["codice"] == "ELEVATO"
    v100 = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A,
                                 INTEGRALE_A)
    assert v100["codice"] == "BUDGET_SFONDATO"


def test_validazioni():
    with pytest.raises(ValueError):
        _F["mh493_budget"](0.0, "b")
    with pytest.raises(ValueError):
        _F["mh493_budget"](-5.0, "b")
    assert _F["mh493_budget"](1.0, "b") == 1.0
    with pytest.raises(ValueError):
        _F["mh493_integrale_eccesso"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                                      None, "i")
    with pytest.raises(ValueError):
        _F["mh493_integrale_eccesso"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A,
                                      -1.0, "i")
    with pytest.raises(ValueError):
        _F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, None,
                              5.0, "c")
    with pytest.raises(ValueError):
        _F["mh493_cumulata"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, T_STAR_A,
                              -1.0, "c")
    with pytest.raises(ValueError):
        _F["mh493_eccesso_t"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, -1.0, "e")
    with pytest.raises(ValueError):
        _F["mh493_giorni_equivalenti"](-1.0, LIMITE_A, "g")
    with pytest.raises(ValueError):
        _F["mh493_frazione_budget"](INTEGRALE_A, 0.0, "f")
    with pytest.raises(ValueError):
        _F["mh493_z"](0.9, "z")
    with pytest.raises(ValueError):
        _F["mh493_mult"](0.5, "m")
    with pytest.raises(ValueError):
        _F["mh493_limite"](0.0, "l")
    with pytest.raises(ValueError):
        _F["mh493_halflife"](0.1, "h")
    with pytest.raises(ValueError):
        _F["mh493_orizzonte"](6, "o")
    with pytest.raises(ValueError):
        _F["mh493_segno"](0.0, "s")
    with pytest.raises(ValueError):
        _F["mh493_mese"]("2027-13", "me")
    with pytest.raises(ValueError):
        _F["mh493_es_t"](2.0, 1.0, 0.0, HL_A, "e")


def test_determinismo():
    a = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A,
                              BUDGET_A)
    b = _F["mh493_verdetto"](ES_BASE_A, ES_STRESS_A, LIMITE_A, HL_A, ORIZ_A,
                              BUDGET_A)
    assert a == b
