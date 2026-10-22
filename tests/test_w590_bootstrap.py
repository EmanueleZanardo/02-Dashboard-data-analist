"""Test tab590 "🧱📐 Bootstrap curva forward (mensile→oraria)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh590_num", "mh590_str", "mh590_parse_lista",
           "mh590_bootstrap", "mh590_demo")

TITLE590 = "🧱📐 Bootstrap curva forward (mensile→oraria)"

M12 = [100.0] * 12
S24_PIATTA = [1.0] * 24
S24_ALT = [1.0, 2.0] * 12


class TestW590Validatori:
    def test_num_ok(self):
        assert _F["mh590_num"](2, "x") == 2.0
        assert _F["mh590_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh590_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh590_str"]("  a ", "x") == "a"

    def test_str_ko(self):
        for bad in ("", "   ", 5, None):
            with pytest.raises(ValueError):
                _F["mh590_str"](bad, "x")

    def test_parse_ok(self):
        t = ", ".join(str(v) for v in range(1, 13))
        assert _F["mh590_parse_lista"](t, 12, "x") == \
            [float(v) for v in range(1, 13)]
        t2 = "\n".join(["1"] * 24)
        assert _F["mh590_parse_lista"](t2, 24, "y") == [1.0] * 24

    def test_parse_ko(self):
        with pytest.raises(ValueError):
            _F["mh590_parse_lista"]("1, 2, 3", 12, "x")
        with pytest.raises(ValueError):
            _F["mh590_parse_lista"]("a, b", 2, "x")
        with pytest.raises(ValueError):
            _F["mh590_parse_lista"]("1, nan", 2, "x")


class TestW590Bootstrap:
    def test_piatta(self):
        r = _F["mh590_bootstrap"](M12, S24_PIATTA)
        assert r["verdetto"] == "CURVA_PIATTA"
        assert r["oraria"] == [100.0] * 288
        assert r["medie_mensili"] == [100.0] * 12
        assert r["deviazione_max_ass"] == 0.0
        assert r["min"] == 100.0 and r["max"] == 100.0
        assert r["media_annua"] == 100.0
        assert r["ratio_max_min"] == 1.0
        assert r["spread_shape_pct"] == 0.0

    def test_alternata_1_2(self):
        r = _F["mh590_bootstrap"](M12, S24_ALT)
        assert r["verdetto"] == "CURVA_MODERATA"
        # fattori normalizzati: media 1.5 -> [2/3, 4/3]
        assert r["shape_norm"][0] == pytest.approx(2.0 / 3.0)
        assert r["shape_norm"][1] == pytest.approx(4.0 / 3.0)
        assert r["oraria"][0] == pytest.approx(200.0 / 3.0)
        assert r["oraria"][1] == pytest.approx(400.0 / 3.0)
        assert len(r["oraria"]) == 288
        assert r["medie_mensili"] == pytest.approx([100.0] * 12)
        assert r["deviazione_max_ass"] < 1e-9
        assert r["ratio_max_min"] == pytest.approx(2.0)

    def test_non_arbitraggio_demo(self):
        d = _F["mh590_demo"]()
        r = _F["mh590_bootstrap"](d["monthly"], d["shape"])
        assert r["medie_mensili"] == pytest.approx(d["monthly"],
                                                   abs=1e-9)
        assert r["deviazione_max_ass"] < 1e-9
        assert r["verdetto"] == "CURVA_MODERATA"
        assert r["media_annua"] == pytest.approx(
            sum(d["monthly"]) / 12.0, rel=1e-9)
        # picco serale: media 8-19 sopra la media annua
        assert r["media_picco"] > r["media_annua"] > r["media_offpeak"]
        assert r["min"] < r["media_annua"] < r["max"]

    def test_shape_normalizzata_media_1(self):
        r = _F["mh590_bootstrap"](
            M12, [float(v) for v in range(1, 25)])
        assert sum(r["shape_norm"]) / 24.0 == pytest.approx(1.0)
        assert r["medie_mensili"] == pytest.approx([100.0] * 12,
                                                   abs=1e-9)

    def test_estrema(self):
        s = [1.0] * 23 + [10.0]
        r = _F["mh590_bootstrap"](M12, s)
        assert r["verdetto"] == "CURVA_ESTREMA"
        assert r["ratio_max_min"] == pytest.approx(10.0)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"]([100.0] * 11, S24_PIATTA)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"](M12, [1.0] * 23)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"]([0.0] + [100.0] * 11, S24_PIATTA)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"]([-5.0] + [100.0] * 11, S24_PIATTA)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"](M12, [0.0] + [1.0] * 23)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"](M12, [-1.0] + [1.0] * 23)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"]("no", S24_PIATTA)
        with pytest.raises(ValueError):
            _F["mh590_bootstrap"]([True] * 12, S24_PIATTA)

    def test_demo(self):
        d = _F["mh590_demo"]()
        assert len(d["monthly"]) == 12
        assert len(d["shape"]) == 24
        assert all(v > 0 for v in d["monthly"] + d["shape"])


class TestW590Registry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_title_present(self):
        assert f'"{TITLE590}"' in self._src()

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 638
        assert TITLE590 in titles

    def test_chain(self):
        assert ", tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab637, tab638 = st.tabs([" in self._src()
        assert "with tab590:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st590_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
