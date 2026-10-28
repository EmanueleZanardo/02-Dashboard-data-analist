"""Test tab513 '🧪 Test retrospettivo di efficacia (look-back)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh513_num", "mh513_str", "mh513_periodo",
           "mh513_backtest", "mh513_riepilogo")

TITLE513 = "🧪 Test retrospettivo di efficacia (look-back)"
TITLE512 = "📒 Rollforward riserva cash-flow hedge (OCI)"


def _p(periodo="2026-Q1", s=-9500.0, h=10000.0):
    return {"periodo": periodo, "d_fv_strumento": s, "d_fv_coperto": h}


def _demo():
    return [_p(),
            _p("2026-Q2", 12100.0, -11000.0),
            _p("2026-Q3", -6000.0, 10000.0),
            _p("2026-Q4", 8400.0, -7000.0)]


class TestW513Validatori:
    def test_num_ok(self):
        assert _F["mh513_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh513_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh513_str"]("  2026-Q1 ", "x") == "2026-Q1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh513_str"](bad, "x")


class TestW513Periodo:
    def test_ok(self):
        r = _F["mh513_periodo"](_p())
        assert r["periodo"] == "2026-Q1"
        assert r["d_fv_strumento"] == -9500.0
        assert r["d_fv_coperto"] == 10000.0

    def test_chiave_mancante_ko(self):
        d = _p()
        del d["d_fv_coperto"]
        with pytest.raises(ValueError):
            _F["mh513_periodo"](d)

    def test_non_numerica_ko(self):
        with pytest.raises(ValueError):
            _F["mh513_periodo"](_p(s="x"))

    def test_periodo_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh513_periodo"](_p(periodo="   "))

    def test_non_dict_ko(self):
        with pytest.raises(ValueError):
            _F["mh513_periodo"](["2026-Q1"])


class TestW513Backtest:
    def test_ratio_efficace(self):
        # ratio = -(-9500)/10000 = 0.95 -> EFFICACE; inefficacia = 500
        a = _F["mh513_backtest"]([_p()])
        o = a["righe"][0]
        assert o["ratio"] == pytest.approx(0.95)
        assert o["verdetto"] == "EFFICACE"
        assert o["inefficacia"] == pytest.approx(500.0)

    def test_ratio_segno_invertito(self):
        # ratio = -(9500)/10000 = -0.95 -> |ratio| 0.95 -> EFFICACE
        a = _F["mh513_backtest"]([_p(s=9500.0)])
        o = a["righe"][0]
        assert o["ratio"] == pytest.approx(-0.95)
        assert o["verdetto"] == "EFFICACE"

    def test_banda_estremi_inclusi(self):
        # |ratio| = 0.80 e 1.25 -> EFFICACE (estremi inclusi)
        a = _F["mh513_backtest"]([_p("A", -80.0, 100.0)])
        assert a["righe"][0]["verdetto"] == "EFFICACE"
        b = _F["mh513_backtest"]([_p("B", -125.0, 100.0)])
        assert b["righe"][0]["verdetto"] == "EFFICACE"

    def test_banda_fuori(self):
        # 0.799 e 1.251 -> INEFFICACE
        a = _F["mh513_backtest"]([_p("A", -79.9, 100.0)])
        assert a["righe"][0]["verdetto"] == "INEFFICACE"
        b = _F["mh513_backtest"]([_p("B", -125.1, 100.0)])
        assert b["righe"][0]["verdetto"] == "INEFFICACE"

    def test_coperto_zero(self):
        a = _F["mh513_backtest"]([_p("A", 500.0, 0.0)])
        o = a["righe"][0]
        assert o["ratio"] is None
        assert o["verdetto"] == "NON_VALUTABILE"
        assert o["inefficacia"] == pytest.approx(500.0)

    def test_demo_totali(self):
        # Q1: 0.95 EFFICACE (ineff 500); Q2: 1.10 EFFICACE (ineff 1100)
        # Q3: 0.60 INEFFICACE (ineff 4000); Q4: 1.20 EFFICACE (ineff 1400)
        a = _F["mh513_backtest"](_demo())
        tt = a["totali"]
        assert [o["verdetto"] for o in a["righe"]] == \
            ["EFFICACE", "EFFICACE", "INEFFICACE", "EFFICACE"]
        assert a["righe"][2]["ratio"] == pytest.approx(0.60)
        assert tt["n_periodi"] == 4
        assert tt["n_efficaci"] == 3
        assert tt["n_inefficaci"] == 1
        assert tt["n_non_valutabili"] == 0
        # Σs = -9500+12100-6000+8400 = 5000
        # Σh = 10000-11000+10000-7000 = 2000 -> ratio_cumulato = -2.5
        assert tt["somma_strumento"] == pytest.approx(5000.0)
        assert tt["somma_coperto"] == pytest.approx(2000.0)
        assert tt["inefficacia_cumulata"] == pytest.approx(7000.0)
        assert tt["ratio_cumulato"] == pytest.approx(-2.5)
        assert tt["verdetto"] == "INEFFICACE"

    def test_tutti_efficaci(self):
        a = _F["mh513_backtest"]([_p("A", -9500.0, 10000.0),
                                  _p("B", 12100.0, -11000.0)])
        assert a["totali"]["verdetto"] == "EFFICACE"
        assert a["totali"]["n_inefficaci"] == 0

    def test_tutti_non_valutabili(self):
        a = _F["mh513_backtest"]([_p("A", 100.0, 0.0),
                                  _p("B", -50.0, 0.0)])
        tt = a["totali"]
        assert tt["n_non_valutabili"] == 2
        assert tt["ratio_cumulato"] is None
        assert tt["verdetto"] == "NON_VALUTABILE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh513_backtest"]([])
        with pytest.raises(ValueError):
            _F["mh513_backtest"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh513_backtest"]([_p("A"), _p("A")])
        with pytest.raises(ValueError):
            _F["mh513_backtest"]([_p(s=float("nan"))])

    def test_riepilogo_wrapper(self):
        a = _F["mh513_riepilogo"]([_p()])
        assert a["totali"]["verdetto"] == "EFFICACE"
        assert a["totali"]["n_periodi"] == 1


def test_registry_tab513():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 776
    assert TITLE513 in titoli
    assert src.count(TITLE513) == 3
    assert ", tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776 = st.tabs([" in src
    assert "    with tab513:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab513" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab513" in withs
    assert len(withs) == len(dvars) == 776
    # ordine: tab513 dopo tab512
    _decl513 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl513.index(f'"{TITLE512}"') < _decl513.index(f'"{TITLE513}"')
    assert titoli[dvars.index("tab513")] == TITLE513


def test_chiavi_st513_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st513_[^"]+)"', src) + re.findall(
        r'key=f"(st513_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
