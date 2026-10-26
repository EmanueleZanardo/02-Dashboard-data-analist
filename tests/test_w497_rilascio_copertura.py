"""Test tab497 '🔓🛡️ Rilascio della copertura: quando alleggerire l'hedge?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh497_num", "mh497_segno", "mh497_mese", "mh497_z",
           "mh497_phi", "mh497_Phi", "mh497_lambda",
           "mh497_mult", "mh497_limite", "mh497_fill",
           "mh497_decadimento", "mh497_buffer", "mh497_n_giorni",
           "mh497_spread_bps", "mh497_adv", "mh497_k_imp",
           "mh497_lato_chiusura", "mh497_riga", "mh497_portafoglio_oggi",
           "mh497_h_needed", "mh497_h_real", "mh497_rilascio_linea",
           "mh497_costo_spread", "mh497_costo_impatto",
           "mh497_verdetto", "mh497_rilascio")

TITLE497 = "🔓🛡️ Rilascio della copertura: quando alleggerire l'hedge?"
TITLE496 = "📊✅ Verifica della copertura: il piano ha funzionato?"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo (stessi numeri tab491-tab496): 3 linee, z 99%, stress x2,
# limite 3M EUR, buffer 10%, decadimento 0.70, fill = piano tab495,
# 5 giorni di smontaggio, k=0.10.
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
ES_STRESS_B = 3998354.3733627778
PLAN_B = [24969.13180116952, 12484.56590058476, 49938.26360233904]
SPR_B = {"TTF gas": 4.0, "Power baseload DE": 6.0,
         "Power baseload IT": 10.0, "CO2 EUA": 8.0}
ADV_B = {"TTF gas": 8000000.0, "Power baseload DE": 5000000.0,
         "Power baseload IT": 2000000.0, "CO2 EUA": 1500000.0}
DEC_B = 0.70
BUF_B = 0.10
ES_OGGI_B = 2798848.0613539447
H_NEEDED_B = 0.03531740887217971
ES_RES_OGGI_B = 2100000.0
MARGINE_B = 600000.0
RELEASE_TOT_B = 75030.86819883042
RELEASE_L1_B = 21437.39091395155
NOZ_B = 7824647.683592315
CS_B = 2062.277005922139
CI_B = 26542.811403010914
CTOT_B = 28605.088408933054


def _righe():
    return [_F["mh497_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


def _rilascio_full(d=DEC_B):
    return _F["mh497_rilascio"](_righe(), Z99, 2.0, d, LIMITE_B, BUF_B,
                                list(PLAN_B), SPR_B, ADV_B, 5, 0.10)


def test_registry_tab497():
    import re
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 727
    assert TITLE497 in titoli
    assert src.count(TITLE497) == 3
    assert "tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727 = st.tabs([" in src
    assert "    with tab497:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab497" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab497" in withs
    assert len(withs) == len(dvars) == 727
    # ordine: tab497 dopo tab496 nella dichiarazione delle tab
    _decl497 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl497.index(f'"{TITLE496}"') < _decl497.index(f'"{TITLE497}"')


def test_chiavi_st497_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    import re
    keys = re.findall(r'key="(st497_[^"]+)"', src) + re.findall(
        r'key=f"(st497_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10


def test_lambda99():
    assert _F["mh497_lambda"](Z99) == pytest.approx(LAMBDA99, rel=1e-12)


def test_portafoglio_oggi_demo():
    pf = _F["mh497_portafoglio_oggi"](_righe(), Z99, 2.0, DEC_B)
    assert pf["es_stress_oggi"] == pytest.approx(ES_OGGI_B, rel=1e-9)
    assert pf["n"] == 3
    # l'ES e' lineare nella vol: dimezzare il decadimento dimezza l'ES
    pf1 = _F["mh497_portafoglio_oggi"](_righe(), Z99, 2.0, 1.0)
    assert pf1["es_stress_oggi"] == pytest.approx(ES_STRESS_B, rel=1e-9)
    assert pf["es_stress_oggi"] == pytest.approx(pf1["es_stress_oggi"] * DEC_B,
                                                rel=1e-12)


def test_h_needed_demo():
    hn = _F["mh497_h_needed"](ES_OGGI_B, LIMITE_B, BUF_B)
    assert hn == pytest.approx(H_NEEDED_B, rel=1e-9)
    # stress dentro il limite con buffer -> nessun hedge necessario
    assert _F["mh497_h_needed"](LIMITE_B * 0.9, LIMITE_B, BUF_B) == 0.0
    assert _F["mh497_h_needed"](LIMITE_B * (1.0 - BUF_B), LIMITE_B,
                               BUF_B) == 0.0
    # senza buffer serve la frazione classica
    assert _F["mh497_h_needed"](ES_STRESS_B, LIMITE_B, 0.0) == pytest.approx(
        1.0 - LIMITE_B / ES_STRESS_B, rel=1e-12)


def test_rilascio_demo_alleggerisci():
    r = _rilascio_full()
    assert r["verdetto"]["codice"] == "ALLEGGERISCI"
    assert r["h_needed"] == pytest.approx(H_NEEDED_B, rel=1e-9)
    assert r["es_stress_oggi"] == pytest.approx(ES_OGGI_B, rel=1e-9)
    assert r["es_residuo_oggi"] == pytest.approx(ES_RES_OGGI_B, rel=1e-9)
    assert r["margine_rischio"] == pytest.approx(MARGINE_B, rel=1e-9)
    assert r["release_tot_mwh"] == pytest.approx(RELEASE_TOT_B, rel=1e-9)
    assert r["nozionale_rilascio_tot"] == pytest.approx(NOZ_B, rel=1e-9)
    assert r["costo_spread_tot"] == pytest.approx(CS_B, rel=1e-9)
    assert r["costo_impatto_tot"] == pytest.approx(CI_B, rel=1e-9)
    assert r["costo_totale"] == pytest.approx(CTOT_B, rel=1e-9)
    rl = r["righe_rilascio"]
    assert rl[0]["rilascio_mwh"] == pytest.approx(RELEASE_L1_B, rel=1e-9)
    assert rl[0]["lato_chiusura"] == "compra"   # long -> hedge short -> chiudi comprando
    assert rl[1]["lato_chiusura"] == "vendi"    # short -> hedge long -> chiudi vendendo
    assert sum(x["rilascio_mwh"] for x in rl) == pytest.approx(
        r["release_tot_mwh"], rel=1e-12)


def test_rilascio_linea_clip():
    # non si rilascia piu' della fill in essere
    assert _F["mh497_rilascio_linea"](100000.0, 20000.0, 1.0, 0.0) == 20000.0
    # hedge in essere sotto il necessario -> nessun rilascio
    assert _F["mh497_rilascio_linea"](100000.0, 10000.0, 0.1, 0.2) == 0.0
    # h_real oltre il cap 1.0 non esiste (clip a 1.0 in h_real)
    assert _F["mh497_h_real"](150000.0, 100000.0) == 1.0
    assert _F["mh497_h_real"](50000.0, 100000.0) == 0.5


def test_mantieni_stress_invariato():
    # d=1.0: lo stress non e' decaduto, l'hedge serve ancora tutto
    r = _rilascio_full(d=1.0)
    assert r["verdetto"]["codice"] == "MANTIENI"
    assert r["release_tot_mwh"] == 0.0
    assert r["h_needed"] == pytest.approx(0.32472218621052573, rel=1e-9)


def test_rilascio_totale_stress_rientrato():
    # d=0.5: ES oggi (1'999'177) sotto il limite con buffer (2.7M)
    r = _rilascio_full(d=0.5)
    assert r["verdetto"]["codice"] == "RILASCIO_TOTALE"
    assert r["h_needed"] == 0.0
    assert r["release_tot_mwh"] == pytest.approx(sum(PLAN_B), rel=1e-9)


def test_lato_chiusura():
    assert _F["mh497_lato_chiusura"](1.0) == "compra"
    assert _F["mh497_lato_chiusura"](-1.0) == "vendi"


def test_costo_impatto_scala_sqrt():
    # dimezzare i giorni raddoppia la q_giorno: impatto scala di sqrt(2)
    r5 = _rilascio_full()
    r10 = _F["mh497_rilascio"](_righe(), Z99, 2.0, DEC_B, LIMITE_B, BUF_B,
                               list(PLAN_B), SPR_B, ADV_B, 10, 0.10)
    assert r5["costo_impatto_tot"] == pytest.approx(
        r10["costo_impatto_tot"] * math.sqrt(2.0), rel=1e-9)
    assert _F["mh497_costo_impatto"](1e6, 1000.0, 1e6, 0.0) == 0.0
    assert _F["mh497_costo_spread"](1e6, 0.0) == 0.0


def test_verdetto_rami():
    f = _F["mh497_verdetto"]
    assert f(0.0, 1000.0, LIMITE_B, LIMITE_B, 0.10)["codice"] == "RILASCIO_TOTALE"
    assert f(0.05, 1000.0, LIMITE_B, LIMITE_B, 0.10)["codice"] == "ALLEGGERISCI"
    assert f(0.05, 0.0, LIMITE_B * 2, LIMITE_B, 0.10)["codice"] == "MANTIENI"
    with pytest.raises(ValueError):
        f(0.05, -1.0, LIMITE_B, LIMITE_B, 0.10)


def test_validatori():
    f = _F
    with pytest.raises(ValueError):
        f["mh497_segno"](0.5, "segno")
    with pytest.raises(ValueError):
        f["mh497_mese"]("2027-13", "mese")
    with pytest.raises(ValueError):
        f["mh497_z"](0.9, "z")
    with pytest.raises(ValueError):
        f["mh497_mult"](11.0, "mult")
    with pytest.raises(ValueError):
        f["mh497_limite"](0.0, "limite")
    with pytest.raises(ValueError):
        f["mh497_fill"](-1.0, "fill")
    with pytest.raises(ValueError):
        f["mh497_decadimento"](0.0, "d")
    with pytest.raises(ValueError):
        f["mh497_decadimento"](1.5, "d")
    with pytest.raises(ValueError):
        f["mh497_buffer"](0.6, "b")
    with pytest.raises(ValueError):
        f["mh497_n_giorni"](0, "n")
    with pytest.raises(ValueError):
        f["mh497_n_giorni"](2.5, "n")
    with pytest.raises(ValueError):
        f["mh497_spread_bps"](-1.0, "spread")
    with pytest.raises(ValueError):
        f["mh497_adv"](0.0, "adv")
    with pytest.raises(ValueError):
        f["mh497_k_imp"](-0.1, "k")
    with pytest.raises(ValueError):
        f["mh497_h_needed"](-5.0, 100.0, 0.1)
    with pytest.raises(ValueError):
        f["mh497_h_real"](-5.0, 100.0)
    with pytest.raises(ValueError):
        f["mh497_rilascio_linea"](100000.0, 1000.0, 1.5, 0.1)
    with pytest.raises(ValueError):
        f["mh497_rilascio"](_righe(), Z99, 2.0, DEC_B, LIMITE_B, BUF_B,
                            [1.0, 2.0], SPR_B, ADV_B, 5, 0.10)
    with pytest.raises(ValueError):
        f["mh497_rilascio"](_righe(), Z99, 2.0, DEC_B, LIMITE_B, BUF_B,
                            list(PLAN_B), SPR_B, ADV_B, 5, -0.1)


def test_rilascio_commodity_sconosciuta():
    with pytest.raises(ValueError):
        _F["mh497_rilascio"](_righe(), Z99, 2.0, DEC_B, LIMITE_B, BUF_B,
                             list(PLAN_B), {"Altro": 4.0}, ADV_B, 5, 0.10)
