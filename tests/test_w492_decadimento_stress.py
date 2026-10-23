"""Test tab492 '⏳🌪️ Decadimento dello stress: aspettare o coprire?': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh492_num", "mh492_segno", "mh492_mese", "mh492_z",
           "mh492_phi", "mh492_Phi", "mh492_lambda",
           "mh492_mult", "mh492_limite", "mh492_halflife", "mh492_orizzonte",
           "mh492_dv01_linea", "mh492_sigma_mtm_linea",
           "mh492_es_linea", "mh492_riga", "mh492_portafoglio",
           "mh492_decay", "mh492_es_t", "mh492_curva_es",
           "mh492_t_rientro", "mh492_es_per_mwh_hedge",
           "mh492_spread_bps", "mh492_hedge_t", "mh492_costo",
           "mh492_verdetto")

TITLE492 = "⏳🌪️ Decadimento dello stress: aspettare o coprire?"
TITLE491 = "🛡️🌪️ Copertura dello Stressed ES: quanto hedgiare per rientrare nel limite?"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo A: linea singola long TTF 100k MWh, scadenza 2027-01, f_now 88.00,
# vol giornaliera 2.5% -> sigma_mtm = 220000 (stessi numeri tab491).
SIGMA_MTM_A = 220000.0
ES_BASE_A = 586347.1284759773
ES_STRESS_A = 1172694.2569519547

# Demo B: portafoglio 3 linee (come tab491), z 99%, stress x2, limite 3M EUR,
# emivita 10 gg, orizzonte 90 gg; hedge sulla peggiore (Power DE 2027-03)
# con F_hedge = 116.00, sigma_hedge = 1.8%, spread 10 bps.
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


def _righe_b():
    return [_F["mh492_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


def _pf_b():
    return _F["mh492_portafoglio"](_righe_b(), Z99, 2.0)


def test_registry_tab492():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    assert f'"{TITLE492}"' in src
    assert "tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663 = st.tabs([" in src
    assert "    with tab492:" in src
    # ordine: tab492 dopo tab491 nella dichiarazione
    i91 = src.index(f'"{TITLE491}"')
    i92 = src.index(f'"{TITLE492}"')
    assert i91 < i92


def test_lambda99():
    assert abs(_F["mh492_lambda"](Z99) - LAMBDA99) < 1e-12


def test_riga_demo_a():
    r = _F["mh492_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00, 88.00, 2.5)
    assert abs(r["sigma_mtm"] - SIGMA_MTM_A) < 1e-9
    assert r["scadenza"] == "2027-01"


def test_es_linea_demo_a():
    eb = _F["mh492_es_linea"](SIGMA_MTM_A, Z99, 1.0)
    es_ = _F["mh492_es_linea"](SIGMA_MTM_A, Z99, 2.0)
    assert abs(eb - ES_BASE_A) < 1e-6
    assert abs(es_ - ES_STRESS_A) < 1e-6


def test_portafoglio_b():
    pf = _pf_b()
    assert abs(pf["es_base_cons"] - sum(pf["es_base_linee"])) < 1e-9
    assert abs(pf["es_stress_cons"] - sum(pf["es_stress_linee"])) < 1e-9
    # stress = 2x base linea per linea
    for b, s in zip(pf["es_base_linee"], pf["es_stress_linee"]):
        assert abs(s - 2.0 * b) < 1e-6


def test_decay():
    assert abs(_F["mh492_decay"](0.0, HL_B) - 1.0) < 1e-12
    assert abs(_F["mh492_decay"](HL_B, HL_B) - 0.5) < 1e-12
    assert abs(_F["mh492_decay"](2 * HL_B, HL_B) - 0.25) < 1e-12


def test_es_t_demo_a():
    # a t = emivita il gap si dimezza
    assert abs(_F["mh492_es_t"](ES_BASE_A, ES_STRESS_A, HL_B, HL_B)
               - (ES_BASE_A + ES_STRESS_A) / 2) < 1e-6
    assert abs(_F["mh492_es_t"](ES_BASE_A, ES_STRESS_A, 0.0, HL_B)
               - ES_STRESS_A) < 1e-9
    # a t grande -> base
    assert abs(_F["mh492_es_t"](ES_BASE_A, ES_STRESS_A, 1e6, HL_B)
               - ES_BASE_A) < 1e-3
    # monotona decrescente
    ts = [0.0, 1.0, 5.0, 10.0, 30.0, 90.0]
    es = [_F["mh492_es_t"](ES_BASE_A, ES_STRESS_A, t, HL_B) for t in ts]
    assert all(es[i] >= es[i + 1] for i in range(len(es) - 1))


def test_t_rientro_demo_a():
    # limite 800k tra base (586k) e stress (1.17M), hl 10 -> 14.5649 gg
    t = _F["mh492_t_rientro"](ES_BASE_A, ES_STRESS_A, 800000.0, HL_B)
    assert abs(t - 14.56486312871427) < 1e-9
    # a t* l'ES e' esattamente il limite
    assert abs(_F["mh492_es_t"](ES_BASE_A, ES_STRESS_A, t, HL_B)
               - 800000.0) < 1e-6
    # formula chiusa indipendente
    att = HL_B / math.log(2.0) * math.log(
        (ES_STRESS_A - ES_BASE_A) / (800000.0 - ES_BASE_A))
    assert abs(t - att) < 1e-12


def test_t_rientro_casi_limite():
    assert _F["mh492_t_rientro"](ES_BASE_A, ES_STRESS_A, 3000000.0, HL_B) == 0.0
    assert _F["mh492_t_rientro"](ES_BASE_A, ES_STRESS_A, 400000.0, HL_B) is None
    # limite == es_base -> mai (serve <, non <=)
    assert _F["mh492_t_rientro"](ES_BASE_A, ES_STRESS_A, ES_BASE_A, HL_B) is None


def test_es_per_mwh_hedge():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    assert abs(u - LAMBDA99 * 2 * 0.018 * 116.0) < 1e-9


def test_hedge_t():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    h = _F["mh492_hedge_t"](ES_STRESS_A, 800000.0, u, 100000.0)
    assert abs(h - (ES_STRESS_A - 800000.0) / u) < 1e-6
    assert _F["mh492_hedge_t"](700000.0, 800000.0, u, 100000.0) == 0.0
    # clip al volume della linea
    assert _F["mh492_hedge_t"](1e12, 800000.0, u, 100000.0) == 100000.0


def test_costo():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    h = _F["mh492_hedge_t"](ES_STRESS_A, 800000.0, u, 100000.0)
    c = _F["mh492_costo"](h, 116.00, 10.0)
    assert abs(c - h * 116.0 * 10 / 10000) < 1e-9
    assert _F["mh492_costo"](0.0, 116.00, 10.0) == 0.0


def test_verdetto_ok_stress():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    v = _F["mh492_verdetto"](ES_BASE_A, ES_STRESS_A, 3000000.0, HL_B, ORIZ_B,
                              u, 100000.0, 116.00, 10.0)
    assert v["codice"] == "OK_STRESS"
    assert v["t_rientro_giorni"] == 0.0
    assert v["hedge_oggi_mwh"] == 0.0
    assert v["costo_oggi_eur"] == 0.0


def test_verdetto_mai():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    v = _F["mh492_verdetto"](ES_BASE_A, ES_STRESS_A, 400000.0, HL_B, ORIZ_B,
                              u, 100000.0, 116.00, 10.0)
    assert v["codice"] == "MAI"
    assert v["t_rientro_giorni"] is None
    assert v["risparmio_eur"] == 0.0


def test_verdetto_aspettare():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    v = _F["mh492_verdetto"](ES_BASE_A, ES_STRESS_A, 800000.0, HL_B, ORIZ_B,
                              u, 100000.0, 116.00, 10.0)
    assert v["codice"] == "ASPETTARE"
    assert abs(v["t_rientro_giorni"] - 14.56486312871427) < 1e-9
    assert v["risparmio_eur"] == v["costo_oggi_eur"] > 0
    # coerenza con hedge_t e costo
    h = _F["mh492_hedge_t"](ES_STRESS_A, 800000.0, u, 100000.0)
    assert abs(v["hedge_oggi_mwh"] - h) < 1e-9
    assert abs(v["costo_oggi_eur"] - _F["mh492_costo"](h, 116.00, 10.0)) < 1e-9


def test_verdetto_oltre_orizzonte():
    u = _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8)
    v = _F["mh492_verdetto"](ES_BASE_A, ES_STRESS_A, 800000.0, HL_B, 7,
                              u, 100000.0, 116.00, 10.0)
    assert v["codice"] == "OLTRE_ORIZZONTE"
    assert v["t_rientro_giorni"] > 7
    assert v["risparmio_eur"] == 0.0


def test_curva_es():
    cv = _F["mh492_curva_es"](ES_BASE_A, ES_STRESS_A, HL_B, 7)
    assert len(cv) == 8
    assert cv[0][0] == 0.0 and cv[-1][0] == 7.0
    assert abs(cv[0][1] - ES_STRESS_A) < 1e-9
    assert all(cv[i][1] >= cv[i + 1][1] for i in range(7))


def test_validazioni():
    with pytest.raises(ValueError):
        _F["mh492_halflife"](0.1, "hl")
    assert _F["mh492_halflife"](0.5, "hl") == 0.5
    with pytest.raises(ValueError):
        _F["mh492_orizzonte"](6, "o")
    assert _F["mh492_orizzonte"](7.0, "o") == 7
    with pytest.raises(ValueError):
        _F["mh492_decay"](-1.0, HL_B, "d")
    with pytest.raises(ValueError):
        _F["mh492_es_t"](2.0, 1.0, 0.0, HL_B, "e")
    with pytest.raises(ValueError):
        _F["mh492_mult"](0.5, "m")
    with pytest.raises(ValueError):
        _F["mh492_spread_bps"](1001.0, "s")
    with pytest.raises(ValueError):
        _F["mh492_z"](0.9, "z")
    with pytest.raises(ValueError):
        _F["mh492_segno"](0.0, "sg")
    with pytest.raises(ValueError):
        _F["mh492_mese"]("2027-13", "me")
    with pytest.raises(ValueError):
        _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 0.0, 1.8, "h")
    with pytest.raises(ValueError):
        _F["mh492_costo"](-1.0, 116.0, 10.0, "c")


def test_determinismo():
    a = _F["mh492_verdetto"](ES_BASE_A, ES_STRESS_A, 800000.0, HL_B, ORIZ_B,
                              _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8),
                              100000.0, 116.00, 10.0)
    b = _F["mh492_verdetto"](ES_BASE_A, ES_STRESS_A, 800000.0, HL_B, ORIZ_B,
                              _F["mh492_es_per_mwh_hedge"](Z99, 2.0, 116.00, 1.8),
                              100000.0, 116.00, 10.0)
    assert a == b
