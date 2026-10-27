"""Test tab507 '🔭 Test prospettico di efficacia (scenari forward)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh507_num", "mh507_pos", "mh507_nonneg", "mh507_str",
           "mh507_scenario", "mh507_test", "mh507_riepilogo")

TITLE507 = "🔭 Test prospettico di efficacia (scenari forward)"
TITLE506 = "📉 Regressione di efficacia (OLS)"


def _demo():
    labs = ["Shock -20", "Shock -10", "Shock -5", "Shock +5", "Shock +10",
            "Shock +20"]
    moves = [-20.0, -10.0, -5.0, 5.0, 10.0, 20.0]
    dh = [48000.0] * 6
    di = [11500.0, 11750.0, 11875.0, 12125.0, 12250.0, 12500.0]
    return labs, moves, dh, di


class TestW507Validatori:
    def test_num_ok(self):
        assert _F["mh507_num"](3, "x") == 3.0
        assert _F["mh507_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh507_num"](bad, "x")

    def test_pos_ok(self):
        assert _F["mh507_pos"](0.001, "x") == 0.001

    def test_pos_ko(self):
        for bad in (0.0, -1.0, True, "2", float("nan")):
            with pytest.raises(ValueError):
                _F["mh507_pos"](bad, "x")

    def test_nonneg_ok(self):
        assert _F["mh507_nonneg"](0.0, "x") == 0.0
        assert _F["mh507_nonneg"](5, "x") == 5.0

    def test_nonneg_ko(self):
        for bad in (-0.001, float("inf"), None):
            with pytest.raises(ValueError):
                _F["mh507_nonneg"](bad, "x")

    def test_str_ok(self):
        assert _F["mh507_str"]("  Shock +5  ", "x") == "Shock +5"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh507_str"](bad, "x")


class TestW507Scenario:
    def test_demo_scenario(self):
        s = _F["mh507_scenario"](-20.0, 48000.0, 11500.0, 3.9, 1500.0)
        assert s["delta_coperto_eur"] == pytest.approx(-960000.0)
        assert s["delta_strumento_eur"] == pytest.approx(897000.0)
        assert s["ratio_offset"] == pytest.approx(0.934375)
        assert s["rapporto_credito"] == pytest.approx(1500.0 / 897000.0)
        assert s["verdetto"] == "IN_BANDA"

    def test_segno_move_positivo(self):
        # move positivo: coperto guadagna, strumento perde, ratio resta > 0
        s = _F["mh507_scenario"](10.0, 48000.0, 12250.0, 3.9, 1500.0)
        assert s["delta_coperto_eur"] == pytest.approx(480000.0)
        assert s["delta_strumento_eur"] == pytest.approx(-477750.0)
        assert s["ratio_offset"] == pytest.approx(0.9953125)
        assert s["verdetto"] == "IN_BANDA"

    def test_bordi_banda(self):
        # ratio esattamente 0.8 e 1.25 -> IN_BANDA (bordi inclusi)
        s1 = _F["mh507_scenario"](10.0, 10000.0, 8000.0, 1.0, 0.0)
        assert s1["ratio_offset"] == pytest.approx(0.8)
        assert s1["verdetto"] == "IN_BANDA"
        s2 = _F["mh507_scenario"](10.0, 10000.0, 12500.0, 1.0, 0.0)
        assert s2["ratio_offset"] == pytest.approx(1.25)
        assert s2["verdetto"] == "IN_BANDA"

    def test_fuori_banda_sotto(self):
        s = _F["mh507_scenario"](10.0, 48000.0, 12000.0, 2.0, 1500.0)
        assert s["ratio_offset"] == pytest.approx(0.5)
        assert s["verdetto"] == "FUORI_BANDA"

    def test_fuori_banda_sopra(self):
        s = _F["mh507_scenario"](10.0, 48000.0, 12000.0, 6.0, 1500.0)
        assert s["ratio_offset"] == pytest.approx(1.5)
        assert s["verdetto"] == "FUORI_BANDA"

    def test_rischio_credito(self):
        # ecl enorme rispetto all'offset atteso
        s = _F["mh507_scenario"](5.0, 48000.0, 12000.0, 3.9, 500000.0)
        assert s["verdetto"] == "RISCHIO_CREDITO"

    def test_soglia_credito_bordo(self):
        # rapporto credito esattamente 5% -> non domina (bordo incluso)
        # |ΔI| = 12000*4*10 = 480000 ; ecl = 24000 -> 0.05 ; ratio = 1.0
        s = _F["mh507_scenario"](10.0, 48000.0, 12000.0, 4.0, 24000.0,
                                 soglia_credito=0.05)
        assert s["rapporto_credito"] == pytest.approx(0.05)
        assert s["ratio_offset"] == pytest.approx(1.0)
        assert s["verdetto"] == "IN_BANDA"

    def test_move_nullo(self):
        s = _F["mh507_scenario"](0.0, 48000.0, 12000.0, 3.9, 1500.0)
        assert s["verdetto"] == "NON_VALUTABILE"
        assert s["ratio_offset"] is None
        assert s["rapporto_credito"] is None

    def test_parametri_ko(self):
        with pytest.raises(ValueError):
            _F["mh507_scenario"](10.0, 0.0, 12000.0, 3.9, 1500.0)  # dv01_h
        with pytest.raises(ValueError):
            _F["mh507_scenario"](10.0, 48000.0, -1.0, 3.9, 1500.0)  # dv01_i
        with pytest.raises(ValueError):
            _F["mh507_scenario"](10.0, 48000.0, 12000.0, 0.0, 1500.0)  # n
        with pytest.raises(ValueError):
            _F["mh507_scenario"](10.0, 48000.0, 12000.0, 3.9, -5.0)  # ecl
        with pytest.raises(ValueError):
            _F["mh507_scenario"](10.0, 48000.0, 12000.0, 3.9, 1500.0,
                                 banda_inf=1.3, banda_sup=1.0)
        with pytest.raises(ValueError):
            _F["mh507_scenario"](10.0, 48000.0, 12000.0, 3.9, 1500.0,
                                 soglia_credito=1.5)


class TestW507Verdetti:
    def test_demo_prospetticamente_efficace(self):
        labs, moves, dh, di = _demo()
        r = _F["mh507_test"](labs, moves, dh, di, 3.9, 1500.0, 48000.0,
                             12000.0)
        assert r["verdetto"] == "PROSPETTICAMENTE_EFFICACE"
        assert r["n_scenari"] == 6
        assert r["hedge_ratio_ottimale"] == pytest.approx(4.0)
        assert r["ratio_min"] == pytest.approx(0.934375)
        assert r["ratio_max"] == pytest.approx(1.015625)
        assert r["banda"] == (0.8, 1.25)
        assert r["soglia_credito"] == 0.05
        assert all(x["verdetto"] == "IN_BANDA" for x in r["righe"])
        assert r["righe"][0]["scenario"] == "Shock -20"

    def test_non_efficace_un_fuori_banda_basta(self):
        labs, moves, dh, di = _demo()
        di2 = list(di)
        di2[-1] = 20000.0  # ratio ultimo scenario = 1.625 -> FUORI_BANDA
        r = _F["mh507_test"](labs, moves, dh, di2, 3.9, 1500.0, 48000.0,
                             12000.0)
        assert r["righe"][-1]["verdetto"] == "FUORI_BANDA"
        assert r["verdetto"] == "NON_EFFICACE"

    def test_a_rischio(self):
        labs, moves, dh, di = _demo()
        r = _F["mh507_test"](labs, moves, dh, di, 3.9, 500000.0, 48000.0,
                             12000.0)
        assert r["verdetto"] == "A_RISCHIO"

    def test_non_valutabile(self):
        labs = ["a", "b", "c"]
        r = _F["mh507_test"](labs, [0.0, 0.0, 0.0], [48000.0] * 3,
                             [12000.0] * 3, 3.9, 1500.0, 48000.0, 12000.0)
        assert r["verdetto"] == "NON_VALUTABILE"
        assert r["ratio_min"] is None and r["ratio_max"] is None

    def test_lunghezze_diverse(self):
        labs, moves, dh, di = _demo()
        with pytest.raises(ValueError):
            _F["mh507_test"](labs, moves[:5], dh, di, 3.9, 1500.0, 48000.0,
                             12000.0)

    def test_pochi_scenari(self):
        with pytest.raises(ValueError):
            _F["mh507_test"](["a", "b"], [10.0, -10.0], [48000.0] * 2,
                             [12000.0] * 2, 3.9, 1500.0, 48000.0, 12000.0)

    def test_basi_ko(self):
        labs, moves, dh, di = _demo()
        with pytest.raises(ValueError):
            _F["mh507_test"](labs, moves, dh, di, 3.9, 1500.0, 0.0, 12000.0)

    def test_etichette_ko(self):
        labs, moves, dh, di = _demo()
        with pytest.raises(ValueError):
            _F["mh507_test"](["solo", "due"], moves, dh, di, 3.9, 1500.0,
                             48000.0, 12000.0)


class TestW507Riepilogo:
    def test_demo(self):
        labs, moves, dh, di = _demo()
        s = _F["mh507_riepilogo"](labs, moves, dh, di, 3.9, 1500.0, 48000.0,
                                  12000.0)
        assert s["verdetto"] == "PROSPETTICAMENTE_EFFICACE"
        assert len(s["righe"]) == 6
        assert s["righe"][3]["scenario"] == "Shock +5"
        assert s["righe"][3]["delta_coperto_eur"] == pytest.approx(240000.0)
        assert s["righe"][3]["delta_strumento_eur"] == pytest.approx(
            -236437.5)


def test_registry_tab507():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 749
    assert TITLE507 in titoli
    assert src.count(TITLE507) == 3
    assert "tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749 = st.tabs([" in src
    assert "    with tab507:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab507" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab507" in withs
    assert len(withs) == len(dvars) == 749
    # ordine: tab507 dopo tab506
    _decl507 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl507.index(f'"{TITLE506}"') < _decl507.index(f'"{TITLE507}"')
    assert titoli[dvars.index("tab507")] == TITLE507


def test_chiavi_st507_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st507_[^"]+)"', src) + re.findall(
        r'key=f"(st507_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
