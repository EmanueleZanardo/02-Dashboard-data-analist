"""Test tab494 '🚨⏳ Monitoraggio dell'attesa: il trigger di escalation': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh494_num", "mh494_segno", "mh494_mese", "mh494_z",
           "mh494_phi", "mh494_Phi", "mh494_lambda",
           "mh494_mult", "mh494_limite", "mh494_halflife", "mh494_orizzonte",
           "mh494_tol",
           "mh494_dv01_linea", "mh494_sigma_mtm_linea",
           "mh494_es_linea", "mh494_riga", "mh494_portafoglio",
           "mh494_es_t", "mh494_t_rientro", "mh494_t_rivisto",
           "mh494_deviazione", "mh494_parse_osservazioni",
           "mh494_stato", "mh494_monitora_giorno",
           "mh494_verdetto")

TITLE494 = "🚨⏳ Monitoraggio dell'attesa: il trigger di escalation"
TITLE493 = "💸⏳ Costo dell'attesa: il budget di rischio consumato"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo B (stessi numeri tab491/tab492/tab493): 3 linee, z 99%, stress x2,
# limite 3M EUR, emivita 10 gg, orizzonte 90 gg.
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
ES_BASE_B = 1999177.1866813889
ES_STRESS_B = 3998354.3733627778
T_STAR_B = 9.982197629332461
ES_T5_B = 3412808.9321772438
ES_T7_B = 3229815.099016088
ES_T10_B = 2998765.7800220833
TOLM = 0.10
TOLE = 0.25


def _righe_b():
    return [_F["mh494_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


def _pf_b():
    return _F["mh494_portafoglio"](_righe_b(), Z99, 2.0)


def test_registry_tab494():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    assert f'"{TITLE494}"' in src
    assert "tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605 = st.tabs([" in src
    assert "    with tab494:" in src
    # ordine: tab494 dopo tab493 nella dichiarazione
    i93 = src.index(f'"{TITLE493}"')
    i94 = src.index(f'"{TITLE494}"')
    assert i93 < i94


def test_lambda99():
    assert _F["mh494_lambda"](Z99) == pytest.approx(LAMBDA99)


def test_portafoglio_b():
    pf = _pf_b()
    assert pf["es_base_cons"] == pytest.approx(ES_BASE_B)
    assert pf["es_stress_cons"] == pytest.approx(ES_STRESS_B)


def test_es_t_sentiero():
    es_t = _F["mh494_es_t"]
    assert es_t(ES_BASE_B, ES_STRESS_B, 0, HL_B) == pytest.approx(ES_STRESS_B)
    assert es_t(ES_BASE_B, ES_STRESS_B, 5, HL_B) == pytest.approx(ES_T5_B)
    assert es_t(ES_BASE_B, ES_STRESS_B, 7, HL_B) == pytest.approx(ES_T7_B)
    assert es_t(ES_BASE_B, ES_STRESS_B, 10, HL_B) == pytest.approx(ES_T10_B)
    # monotona decrescente verso la base
    assert es_t(ES_BASE_B, ES_STRESS_B, 365, HL_B) == pytest.approx(
        ES_BASE_B, rel=1e-6)


def test_t_rientro_demo_b():
    assert _F["mh494_t_rientro"](ES_BASE_B, ES_STRESS_B, LIMITE_B,
                                HL_B) == pytest.approx(T_STAR_B)


def test_t_rivisto():
    t_riv = _F["mh494_t_rivisto"]
    # osservato sopra il limite: rientro rivisto piu' lungo/corto del piano
    assert t_riv(ES_BASE_B, 3560000.0, LIMITE_B, HL_B) == pytest.approx(
        6.411201893575199)
    assert t_riv(ES_BASE_B, 3750000.0, LIMITE_B, HL_B) == pytest.approx(
        8.06846507014577)
    # gia' dentro il limite
    assert t_riv(ES_BASE_B, LIMITE_B, LIMITE_B, HL_B) == 0.0
    assert t_riv(ES_BASE_B, 2900000.0, LIMITE_B, HL_B) == 0.0
    # decadimento completo (osservato <= base < limite)
    assert t_riv(ES_BASE_B, ES_BASE_B, LIMITE_B, HL_B) == 0.0
    # mai: base sopra il limite
    assert t_riv(LIMITE_B, LIMITE_B + 1.0, LIMITE_B, HL_B) is None


def test_deviazione():
    dev = _F["mh494_deviazione"]
    assert dev(3560000.0, ES_T5_B) == pytest.approx(0.043129009196789074)
    assert dev(ES_T5_B, ES_T5_B) == pytest.approx(0.0)
    assert dev(2900000.0, ES_T10_B) == pytest.approx(-0.032935476548407186)


def test_parse_osservazioni():
    parse = _F["mh494_parse_osservazioni"]
    txt = "giorno,es_EUR\n10,3750000\n0,3998354\n# commento\n5,3560000\n"
    assert parse(txt, ORIZ_B) == [(0, 3998354.0), (5, 3560000.0),
                                  (10, 3750000.0)]
    # separatore ; ammesso
    assert parse("0;3998354", ORIZ_B) == [(0, 3998354.0)]
    # vuota -> lista vuota
    assert parse("", ORIZ_B) == []
    assert parse("# solo commenti\n\n", ORIZ_B) == []


def test_parse_osservazioni_errori():
    parse = _F["mh494_parse_osservazioni"]
    with pytest.raises(ValueError):
        parse("0,3998354\n0,3998354", ORIZ_B)  # duplicato
    with pytest.raises(ValueError):
        parse("91,1000", ORIZ_B)  # fuori orizzonte
    with pytest.raises(ValueError):
        parse("-1,1000", ORIZ_B)  # giorno negativo
    with pytest.raises(ValueError):
        parse("5,-100", ORIZ_B)  # es negativo
    with pytest.raises(ValueError):
        parse("5", ORIZ_B)  # formato errato
    with pytest.raises(ValueError):
        parse("0,1000\ncinque,1000", ORIZ_B)  # giorno non intero (non header)
    with pytest.raises(ValueError):
        parse("5,mille", ORIZ_B)  # es non numerico


def test_stato():
    stato = _F["mh494_stato"]
    assert stato(0.05, TOLM, TOLE) == "IN_LINEA"
    assert stato(-0.05, TOLM, TOLE) == "IN_LINEA"
    assert stato(0.10, TOLM, TOLE) == "IN_LINEA"  # bordo incluso
    assert stato(-0.10, TOLM, TOLE) == "IN_LINEA"
    assert stato(-0.15, TOLM, TOLE) == "SOTTO_SENTIERO"
    assert stato(0.20, TOLM, TOLE) == "SOPRA_SENTIERO"
    assert stato(0.25, TOLM, TOLE) == "SOPRA_SENTIERO"  # bordo incluso
    assert stato(0.2500001, TOLM, TOLE) == "ESCALATION"
    with pytest.raises(ValueError):
        stato(0.05, 0.30, 0.25)  # tol_mon > tol_esc


def test_monitora_giorno():
    m = _F["mh494_monitora_giorno"](5, 3560000.0, ES_BASE_B, ES_STRESS_B,
                                    LIMITE_B, HL_B, TOLM, TOLE)
    assert m["giorno"] == pytest.approx(5.0)
    assert m["es_obs"] == pytest.approx(3560000.0)
    assert m["es_atteso"] == pytest.approx(ES_T5_B)
    assert m["deviazione"] == pytest.approx(0.043129009196789074)
    assert m["stato"] == "IN_LINEA"
    assert m["t_rivisto_giorni"] == pytest.approx(6.411201893575199)


def test_verdetto_in_linea():
    v = _F["mh494_verdetto"](ES_BASE_B, ES_STRESS_B, 3412810.0, 5, LIMITE_B,
                             HL_B, TOLM, TOLE)
    assert v["codice"] == "IN_LINEA"
    assert v["deviazione"] == pytest.approx(3.128867678989874e-07)
    assert "IN LINEA" in v["testo"]


def test_verdetto_sopra_sentiero():
    v = _F["mh494_verdetto"](ES_BASE_B, ES_STRESS_B, 3600000.0, 7, LIMITE_B,
                             HL_B, TOLM, TOLE)
    assert v["codice"] == "SOPRA_SENTIERO"
    assert v["deviazione"] == pytest.approx(0.1146148895943557)
    assert v["t_rivisto_giorni"] == pytest.approx(6.776270517491428)
    assert "SOPRA IL SENTIERO" in v["testo"]


def test_verdetto_sotto_sentiero():
    v = _F["mh494_verdetto"](ES_BASE_B, ES_STRESS_B, 2600000.0, 10, LIMITE_B,
                             HL_B, TOLM, TOLE)
    assert v["codice"] == "SOTTO_SENTIERO"
    assert v["deviazione"] == pytest.approx(-0.13297663414684782)
    assert v["t_rivisto_giorni"] == 0.0  # gia' dentro il limite
    assert "SOTTO IL SENTIERO" in v["testo"]


def test_verdetto_escalation():
    v = _F["mh494_verdetto"](ES_BASE_B, ES_STRESS_B, 3750000.0, 10, LIMITE_B,
                             HL_B, TOLM, TOLE)
    assert v["codice"] == "ESCALATION"
    assert v["deviazione"] == pytest.approx(0.25051446998050797)
    assert "ESCALATION" in v["testo"]
    assert "tab491" in v["testo"]


def test_validazioni():
    with pytest.raises(ValueError):
        _F["mh494_num"](float("nan"), "x")
    with pytest.raises(ValueError):
        _F["mh494_num"](True, "x")
    with pytest.raises(ValueError):
        _F["mh494_segno"](0.0, "s")
    with pytest.raises(ValueError):
        _F["mh494_mese"]("2027-13", "m")
    with pytest.raises(ValueError):
        _F["mh494_z"](0.95, "z")
    with pytest.raises(ValueError):
        _F["mh494_mult"](0.5, "m")
    with pytest.raises(ValueError):
        _F["mh494_limite"](0.0, "l")
    with pytest.raises(ValueError):
        _F["mh494_halflife"](0.1, "h")
    with pytest.raises(ValueError):
        _F["mh494_orizzonte"](6, "n")
    with pytest.raises(ValueError):
        _F["mh494_tol"](1.5, "t")
    with pytest.raises(ValueError):
        _F["mh494_deviazione"](100.0, 0.0)
    with pytest.raises(ValueError):
        _F["mh494_deviazione"](-5.0, 100.0)
    with pytest.raises(ValueError):
        _F["mh494_es_t"](ES_BASE_B, ES_STRESS_B, -1.0, HL_B)
    with pytest.raises(ValueError):
        _F["mh494_es_t"](ES_STRESS_B, ES_BASE_B, 1.0, HL_B)  # stress < base


def test_determinismo():
    v1 = _F["mh494_verdetto"](ES_BASE_B, ES_STRESS_B, 3600000.0, 7,
                              LIMITE_B, HL_B, TOLM, TOLE)
    v2 = _F["mh494_verdetto"](ES_BASE_B, ES_STRESS_B, 3600000.0, 7,
                              LIMITE_B, HL_B, TOLM, TOLE)
    assert v1 == v2
    m1 = _F["mh494_monitora_giorno"](7, 3600000.0, ES_BASE_B, ES_STRESS_B,
                                    LIMITE_B, HL_B, TOLM, TOLE)
    assert m1["deviazione"] == v1["deviazione"]
    assert m1["t_rivisto_giorni"] == v1["t_rivisto_giorni"]
