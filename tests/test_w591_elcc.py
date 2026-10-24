"""Test tab591 "🔌📏 ELCC: capacity credit delle rinnovabili": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh591_num", "mh591_pos", "mh591_nneg", "mh591_pct",
           "mh591_str", "mh591_unita", "mh591_copt", "mh591_lolp",
           "mh591_parse_profilo", "mh591_elcc", "mh591_riepilogo",
           "mh591_demo")

TITLE591 = "🔌📏 ELCC: capacity credit delle rinnovabili"

U1 = [{"id": "A", "descr": "una", "cap_mw": 100.0, "for_pct": 10.0}]
U2 = U1 + [{"id": "B", "descr": "due", "cap_mw": 100.0, "for_pct": 10.0}]
# COPT 2x100 MW FOR 10% (hand-computed):
# 0 MW: 0.81, 100 MW: 0.18, 200 MW: 0.01
COPT2 = [(0.0, 0.81), (100.0, 0.18), (200.0, 0.01)]


class TestW591Validatori:
    def test_num_ok(self):
        assert _F["mh591_num"](2, "x") == 2.0
        assert _F["mh591_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh591_num"](bad, "x")

    def test_pos_ko(self):
        for bad in (0, -1.5):
            with pytest.raises(ValueError):
                _F["mh591_pos"](bad, "x")
        assert _F["mh591_pos"](0.5, "x") == 0.5

    def test_nneg_ko(self):
        with pytest.raises(ValueError):
            _F["mh591_nneg"](-0.1, "x")
        assert _F["mh591_nneg"](0, "x") == 0.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh591_pct"](bad, "x")
        assert _F["mh591_pct"](0, "x") == 0.0
        assert _F["mh591_pct"](100, "x") == 100.0

    def test_str_ok_ko(self):
        assert _F["mh591_str"]("  a ", "x") == "a"
        for bad in ("", "   ", 5, None):
            with pytest.raises(ValueError):
                _F["mh591_str"](bad, "x")

    def test_unita_ok_ko(self):
        u = _F["mh591_unita"](" U1 ", "CCGT", 200, 3)
        assert u == {"id": "U1", "descr": "CCGT", "cap_mw": 200.0,
                     "for_pct": 3.0}
        with pytest.raises(ValueError):
            _F["mh591_unita"]("U1", "d", 0, 3)
        with pytest.raises(ValueError):
            _F["mh591_unita"]("U1", "d", 100, 101)
        with pytest.raises(ValueError):
            _F["mh591_unita"]("", "d", 100, 3)


class TestW591CoptLolp:
    def test_copt_1u(self):
        assert _F["mh591_copt"](U1) == [(0.0, 0.9), (100.0, 0.1)]

    def test_copt_2u(self):
        got = _F["mh591_copt"](U2)
        assert len(got) == 3
        for (_o, _p), (_eo, _ep) in zip(got, COPT2):
            assert _o == pytest.approx(_eo)
            assert _p == pytest.approx(_ep)
        assert sum(_p for _, _p in got) == pytest.approx(1.0)

    def test_copt_for_0_e_100(self):
        u = [_F["mh591_unita"]("A", "a", 80.0, 0.0)]
        assert _F["mh591_copt"](u) == [(0.0, 1.0)]
        u = [_F["mh591_unita"]("A", "a", 80.0, 100.0)]
        assert _F["mh591_copt"](u) == [(80.0, 1.0)]

    def test_copt_ko(self):
        with pytest.raises(ValueError):
            _F["mh591_copt"]([])

    def test_lolp_hand(self):
        # installato 200 MW; LOLP(carico) = P(out > 200 - carico)
        assert _F["mh591_lolp"](COPT2, 150.0, 200.0) == \
            pytest.approx(0.19)   # riserva 50: 100 e 200 oltre
        assert _F["mh591_lolp"](COPT2, 50.0, 200.0) == \
            pytest.approx(0.01)   # riserva 150: solo 200 oltre
        assert _F["mh591_lolp"](COPT2, 0.0, 200.0) == pytest.approx(0.0)

    def test_lolp_bordo_stretto(self):
        # carico == installato: riserva = 0, fuori_servizio 100 e 200
        # contano entrambi (disuguaglianza stretta su riserva 0)
        assert _F["mh591_lolp"](COPT2, 200.0, 200.0) == \
            pytest.approx(0.19)
        # riserva 100: fuori_servizio == 100 NON conta (stretta)
        assert _F["mh591_lolp"](COPT2, 100.0, 200.0) == \
            pytest.approx(0.01)   # solo fuori_servizio = 200 > 100

    def test_parse_profilo_ok_ko(self):
        t = ", ".join(str(v) for v in range(1, 25))
        assert _F["mh591_parse_profilo"](t, 24, "x") == \
            [float(v) for v in range(1, 25)]
        with pytest.raises(ValueError):
            _F["mh591_parse_profilo"]("1, 2, 3", 24, "x")
        with pytest.raises(ValueError):
            _F["mh591_parse_profilo"]("1, -2", 2, "x")
        with pytest.raises(ValueError):
            _F["mh591_parse_profilo"]("a, b", 2, "x")


class TestW591Elcc:
    def test_firm_100pct(self):
        # risorsa "ferma" 50 MW: ELCC = 50, credit 100%, Garver = 50
        # (hand: m=100, S_base=24*e^-0.5, S_new=24*e^-1 ->
        #  100*ln(e^0.5) = 50)
        r = _F["mh591_elcc"](U2, [150.0] * 24, [50.0] * 24, 50.0)
        assert r["elcc_mw"] == pytest.approx(50.0, abs=1e-6)
        assert r["capacity_credit_pct"] == pytest.approx(100.0, abs=1e-6)
        assert r["elcc_garver_mw"] == pytest.approx(50.0, abs=1e-6)
        assert r["lolp_new"] < r["lolp_base"]

    def test_peak_shaving(self):
        # 60 MW solo nelle 12 ore di picco: ELCC ~ 50 MW (hand),
        # credit ~ 83.3%
        r = _F["mh591_elcc"](U2, [150.0] * 12 + [50.0] * 12,
                             [60.0] * 12 + [0.0] * 12, 60.0)
        assert r["elcc_mw"] == pytest.approx(50.0, abs=0.5)
        assert r["capacity_credit_pct"] == pytest.approx(83.333, abs=1.0)
        rp = _F["mh591_riepilogo"](r["elcc_mw"], 60.0, r["lolp_base"],
                                   r["lolp_new"])
        assert rp["verdetto"] == "CREDITO_ELEVATO"

    def test_zero_gen(self):
        r = _F["mh591_elcc"](U2, [150.0] * 24, [0.0] * 24, 50.0)
        assert r["elcc_mw"] == 0.0
        assert r["capacity_credit_pct"] == 0.0
        assert any("ELCC = 0" in n for n in r["note"])
        rp = _F["mh591_riepilogo"](0.0, 50.0, r["lolp_base"],
                                   r["lolp_new"])
        assert rp["verdetto"] == "RISORSA_INUTILE"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh591_elcc"](U2, [150.0] * 24, [10.0] * 23, 50.0)
        with pytest.raises(ValueError):
            _F["mh591_elcc"](U2, [], [], 50.0)
        with pytest.raises(ValueError):
            _F["mh591_elcc"](U2, [150.0] * 24, [60.0] * 24, 50.0)
        with pytest.raises(ValueError):
            _F["mh591_elcc"](U2, [150.0] * 24, [10.0] * 24, 0.0)
        with pytest.raises(ValueError):
            _F["mh591_elcc"](U2, [-5.0] * 24, [10.0] * 24, 50.0)
        with pytest.raises(ValueError):
            _F["mh591_elcc"](U2, [150.0] * 24, [10.0] * 24, 50.0,
                             m_garver=0.0)

    def test_demo(self):
        d = _F["mh591_demo"]()
        uu = [_F["mh591_unita"](*_t) for _t in d["unita"]]
        r = _F["mh591_elcc"](uu, d["carichi"], d["generazione"],
                             d["targa"])
        # eolico notturno 200 MW su parco 900 MW: ELCC ~ 40 MW
        assert r["elcc_mw"] == pytest.approx(40.0, abs=1.5)
        assert r["capacity_credit_pct"] == pytest.approx(20.0, abs=1.0)
        rp = _F["mh591_riepilogo"](r["elcc_mw"], d["targa"],
                                   r["lolp_base"], r["lolp_new"])
        assert rp["verdetto"] == "CREDITO_BASSO"
        assert rp["delta_lole_h_anno"] == pytest.approx(24.64, abs=0.5)
        assert len(r["lolp_h_base"]) == 24
        assert len(r["carico_netto"]) == 24


class TestW591Riepilogo:
    def _r(self, cc):
        return _F["mh591_riepilogo"](cc, 100.0, 0.01, 0.005)

    def test_verdetti(self):
        assert self._r(0.0)["verdetto"] == "RISORSA_INUTILE"
        assert self._r(0.9)["verdetto"] == "RISORSA_INUTILE"
        assert self._r(1.0)["verdetto"] == "CREDITO_BASSO"
        assert self._r(29.9)["verdetto"] == "CREDITO_BASSO"
        assert self._r(30.0)["verdetto"] == "CREDITO_MODERATO"
        assert self._r(59.9)["verdetto"] == "CREDITO_MODERATO"
        assert self._r(60.0)["verdetto"] == "CREDITO_ELEVATO"
        assert self._r(100.0)["verdetto"] == "CREDITO_ELEVATO"

    def test_lole(self):
        r = _F["mh591_riepilogo"](50.0, 100.0, 0.01, 0.005,
                                  giorni_eq=365.0)
        assert r["lole_base_h_anno"] == pytest.approx(87.6)
        assert r["lole_new_h_anno"] == pytest.approx(43.8)
        assert r["delta_lole_h_anno"] == pytest.approx(43.8)


class TestW591Registry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_title_present(self):
        assert f'"{TITLE591}"' in self._src()

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 672
        assert TITLE591 in titles
        assert TITLE591 in titles

    def test_chain(self):
        assert ", tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672 = st.tabs([" in self._src()
        assert "with tab591:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st591_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
