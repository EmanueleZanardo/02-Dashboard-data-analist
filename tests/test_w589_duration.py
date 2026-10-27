"""Test tab589 "📉⏳ Curva di durata prezzi": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh589_num", "mh589_str", "mh589_parse_serie",
           "mh589_percentile", "mh589_duration_curve", "mh589_demo")

TITLE589 = "📉⏳ Curva di durata prezzi"

SERIE_1_24 = list(range(1, 25))


class TestW589Validatori:
    def test_num_ok(self):
        assert _F["mh589_num"](2, "x") == 2.0
        assert _F["mh589_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh589_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh589_str"]("  a ", "x") == "a"

    def test_str_ko(self):
        for bad in ("", "   ", 5, None):
            with pytest.raises(ValueError):
                _F["mh589_str"](bad, "x")

    def test_parse_ok(self):
        t = ", ".join(str(v) for v in SERIE_1_24)
        assert _F["mh589_parse_serie"](t) == [float(v) for v in SERIE_1_24]
        mix = "1;2 3\n4," + ",".join(str(v) for v in range(5, 25))
        assert _F["mh589_parse_serie"](mix) == [float(v) for v in SERIE_1_24]

    def test_parse_negativi_ok(self):
        t = ",".join(["-5.5"] + [str(v) for v in range(2, 25)])
        r = _F["mh589_parse_serie"](t)
        assert r[0] == -5.5 and len(r) == 24

    def test_parse_ko(self):
        with pytest.raises(ValueError):
            _F["mh589_parse_serie"](", ".join(["1"] * 23))
        with pytest.raises(ValueError):
            _F["mh589_parse_serie"](", ".join(["1"] * 9001))
        with pytest.raises(ValueError):
            _F["mh589_parse_serie"]("1, 2, x," + ",".join(["1"] * 21))
        with pytest.raises(ValueError):
            _F["mh589_parse_serie"]("")


class TestW589Duration:
    def test_base_1_24(self):
        r = _F["mh589_duration_curve"](SERIE_1_24, 20.0, 3)
        assert r["n"] == 24
        assert r["min"] == 1.0
        assert r["max"] == 24.0
        assert r["mean"] == pytest.approx(12.5)
        assert r["median"] == pytest.approx(12.5)
        assert r["p5"] == pytest.approx(2.15)
        assert r["p95"] == pytest.approx(22.85)
        assert r["std"] == pytest.approx(math.sqrt(575.0 / 12.0))
        assert r["ordinata"] == [float(v) for v in range(24, 0, -1)]
        assert r["ore_sopra_strike"] == 4
        assert r["pct_sopra"] == pytest.approx(100.0 * 4 / 24)
        assert r["media_sopra_strike"] == pytest.approx(22.5)
        assert r["media_top_n"] == pytest.approx(23.0)
        assert r["somma_top_n"] == pytest.approx(69.0)
        assert r["n_negativi"] == 0
        assert r["verdetto"] == "CURVA_VOLATILE"

    def test_strike_sopra_max(self):
        r = _F["mh589_duration_curve"](SERIE_1_24, 100.0, 1)
        assert r["ore_sopra_strike"] == 0
        assert r["media_sopra_strike"] is None
        assert any("sopra il massimo" in n for n in r["note"])

    def test_strike_sotto_min(self):
        r = _F["mh589_duration_curve"](SERIE_1_24, 0.0, 24)
        assert r["ore_sopra_strike"] == 24
        assert any("sotto il minimo" in n for n in r["note"])

    def test_piatta(self):
        r = _F["mh589_duration_curve"]([50.0] * 24, 40.0, 5)
        assert r["verdetto"] == "CURVA_PIATTA"
        assert r["std"] == 0.0
        assert any("tutti uguali" in n for n in r["note"])

    def test_moderata(self):
        serie = [80.0 + i * (40.0 / 23.0) for i in range(24)]
        r = _F["mh589_duration_curve"](serie, 100.0, 2)
        assert r["verdetto"] == "CURVA_MODERATA"

    def test_negativi(self):
        serie = [-5.0, -1.0] + [float(v) for v in range(3, 25)]
        r = _F["mh589_duration_curve"](serie, 10.0, 2)
        assert r["n_negativi"] == 2
        assert r["quota_negativi_pct"] == pytest.approx(100.0 * 2 / 24)
        assert any("negativi" in n for n in r["note"])

    def test_demo(self):
        d = _F["mh589_demo"]()
        r = _F["mh589_duration_curve"](d["serie"], d["strike"],
                                       d["top_n"])
        assert r["max"] == pytest.approx(128.4)
        assert r["min"] == pytest.approx(33.2)
        assert r["mean"] == pytest.approx(66.5875)
        assert r["ore_sopra_strike"] == 3
        assert r["media_top_n"] == pytest.approx(114.475)
        assert r["verdetto"] == "CURVA_VOLATILE"

    def test_errori(self):
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"]([1.0] * 23, 0.0, 1)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"]([1.0] * 9001, 0.0, 1)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"](SERIE_1_24, 0.0, 0)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"](SERIE_1_24, 0.0, 25)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"](SERIE_1_24, 0.0, True)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"](SERIE_1_24, 0.0, 2.0)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"](SERIE_1_24, math.nan, 1)
        with pytest.raises(ValueError):
            _F["mh589_duration_curve"]([1.0] * 23 + [math.inf],
                                       0.0, 1)


class TestW589Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_presente(self):
        assert f'"{TITLE589}"' in self._src()

    def test_conteggio_tab(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 745
        assert TITLE589 in titles

    def test_chain_tab_var(self):
        assert ", tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745 = st.tabs([" in self._src()
        assert "with tab589:" in self._src()

    def test_chiavi_univoche(self):
        keys = set(re.findall(r"st589_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
