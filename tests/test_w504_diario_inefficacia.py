"""Test tab504 '📊📓 Diario dell'inefficacia: OCI vs P&L per periodo': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh504_num", "mh504_str", "mh504_pct", "mh504_periodo",
           "mh504_lower_of", "mh504_inefficacia", "mh504_riepilogo")

TITLE504 = "📊📓 Diario dell'inefficacia: OCI vs P&L per periodo"
TITLE503 = "📦 Cost-of-carry: scomponi il premio del forward"

TOL = 5.0


def _demo():
    return [_F["mh504_periodo"](n, dh, di) for n, dh, di in
            [("Gennaio", 1000000.0, -1000000.0),
             ("Febbraio", 500000.0, -480000.0),
             ("Marzo", -200000.0, 260000.0),
             ("Aprile", -1000000.0, 1100000.0)]]


class TestW504Validatori:
    def test_num_ok(self):
        assert _F["mh504_num"](3, "x") == 3.0
        assert _F["mh504_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh504_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh504_str"]("  Gennaio  ", "x") == "Gennaio"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh504_str"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh504_pct"](0, "x") == 0.0
        assert _F["mh504_pct"](100, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "5", None):
            with pytest.raises(ValueError):
                _F["mh504_pct"](bad, "x")

    def test_periodo_ok(self):
        p = _F["mh504_periodo"](" Q1 ", 100.0, -90.0)
        assert p == {"nome": "Q1", "d_hedge": 100.0, "d_item": -90.0}

    def test_periodo_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_periodo"]("", 100.0, -90.0)
        with pytest.raises(ValueError):
            _F["mh504_periodo"]("Q1", "100", -90.0)
        with pytest.raises(ValueError):
            _F["mh504_periodo"]("Q1", 100.0, float("nan"))


class TestW504LowerOf:
    def test_hedge_zero(self):
        assert _F["mh504_lower_of"](0.0, 5000.0) == 0.0
        assert _F["mh504_lower_of"](1e-12, -3000.0) == 0.0

    def test_min_item(self):
        # |I| < |H| -> efficace = I col segno di H
        assert _F["mh504_lower_of"](1000000.0, -800000.0) == 800000.0
        assert _F["mh504_lower_of"](-1000000.0, 800000.0) == -800000.0

    def test_min_hedge(self):
        # |H| < |I| -> efficace = H
        assert _F["mh504_lower_of"](-150.0, -200.0) == -150.0
        assert _F["mh504_lower_of"](150.0, -200.0) == 150.0

    def test_uguali(self):
        assert _F["mh504_lower_of"](1000000.0, -1000000.0) == 1000000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_lower_of"]("x", 1.0)


class TestW504Diario:
    def test_gennaio_efficace(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[0]
        assert r["cum_hedge"] == 1000000.0
        assert r["cum_item"] == -1000000.0
        assert r["eff_cum"] == 1000000.0
        assert r["ineff_cum"] == 0.0
        assert r["eff_periodo"] == 1000000.0
        assert r["ineff_periodo"] == 0.0
        assert r["verdetto"] == "EFFICACE"

    def test_febbraio_entro_soglia(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[1]
        assert r["cum_hedge"] == 1500000.0
        assert r["cum_item"] == -1480000.0
        assert r["eff_cum"] == 1480000.0
        assert r["ineff_cum"] == 20000.0
        assert r["ineff_periodo"] == 20000.0
        assert r["eff_periodo"] == 480000.0
        assert r["soglia"] == pytest.approx(25000.0)
        assert r["verdetto"] == "INEFFICACE_ENTRO_SOGLIA"

    def test_marzo_oltre_soglia(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[2]
        assert r["cum_hedge"] == 1300000.0
        assert r["cum_item"] == -1220000.0
        assert r["eff_cum"] == 1220000.0
        assert r["ineff_cum"] == 80000.0
        assert r["ineff_periodo"] == 60000.0
        assert r["eff_periodo"] == -260000.0
        assert r["soglia"] == pytest.approx(10000.0)
        assert r["verdetto"] == "INEFFICACE_OLTRE_SOGLIA"

    def test_aprile_oltre_soglia(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[3]
        assert r["cum_hedge"] == 300000.0
        assert r["cum_item"] == -120000.0
        assert r["eff_cum"] == 120000.0
        assert r["ineff_cum"] == 180000.0
        assert r["ineff_periodo"] == 100000.0
        assert r["eff_periodo"] == -1100000.0
        assert r["soglia"] == pytest.approx(50000.0)
        assert r["verdetto"] == "INEFFICACE_OLTRE_SOGLIA"

    def test_identita_contabile(self):
        # d_hedge = eff_periodo + ineff_periodo per ogni riga
        for r in _F["mh504_inefficacia"](_demo(), TOL):
            assert r["d_hedge"] == pytest.approx(r["eff_periodo"] + r["ineff_periodo"])
            assert r["cum_hedge"] == pytest.approx(r["eff_cum"] + r["ineff_cum"])

    def test_tolleranza_zero(self):
        # con tolleranza 0, qualsiasi inefficacia != 0 e' OLTRE_SOGLIA
        demo = [_F["mh504_periodo"]("A", 1000.0, -990.0)]
        assert _F["mh504_inefficacia"](demo, 0.0)[0]["verdetto"] == \
            "INEFFICACE_OLTRE_SOGLIA"

    def test_soglia_rispettata_con_tolleranza_alta(self):
        demo = [_F["mh504_periodo"]("A", 1000.0, -990.0)]
        assert _F["mh504_inefficacia"](demo, 100.0)[0]["verdetto"] == \
            "INEFFICACE_ENTRO_SOGLIA"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_inefficacia"]([], TOL)
        with pytest.raises(ValueError):
            _F["mh504_inefficacia"](_demo(), -1.0)
        with pytest.raises(ValueError):
            _F["mh504_inefficacia"](_demo(), 101.0)


class TestW504Riepilogo:
    def test_demo(self):
        s = _F["mh504_riepilogo"](_demo(), TOL)
        assert s["n_periodi"] == 4
        assert s["conteggi"] == {"EFFICACE": 1, "INEFFICACE_ENTRO_SOGLIA": 1,
                                 "INEFFICACE_OLTRE_SOGLIA": 2}
        assert s["verdetto_complessivo"] == "INEFFICACE_OLTRE_SOGLIA"
        assert s["oci_cum_eur"] == 120000.0
        assert s["pnl_cum_eur"] == 180000.0
        assert s["ratio_inefficacia"] == pytest.approx(0.6)
        assert s["periodi_con_inefficacia"] == 3
        assert len(s["righe"]) == 4

    def test_tutto_efficace(self):
        demo = [_F["mh504_periodo"]("A", 1000.0, -1000.0),
                _F["mh504_periodo"]("B", -500.0, 500.0)]
        s = _F["mh504_riepilogo"](demo, TOL)
        assert s["verdetto_complessivo"] == "EFFICACE"
        assert s["oci_cum_eur"] == 500.0
        assert s["pnl_cum_eur"] == 0.0
        assert s["ratio_inefficacia"] == 0.0
        assert s["periodi_con_inefficacia"] == 0

    def test_severita_complessivo(self):
        # il piu' severo vince: ENTRO < OLTRE
        demo = [_F["mh504_periodo"]("A", 1000.0, -990.0),   # entro soglia 5%
                _F["mh504_periodo"]("B", 1000.0, -1000.0)]  # efficace
        s = _F["mh504_riepilogo"](demo, TOL)
        assert s["verdetto_complessivo"] == "INEFFICACE_ENTRO_SOGLIA"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_riepilogo"]([], TOL)


def test_registry_tab504():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 819
    assert TITLE504 in titoli
    assert src.count(TITLE504) == 3
    assert "tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819 = st.tabs([" in src
    assert "    with tab504:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab504" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab504" in withs
    assert len(withs) == len(dvars) == 819
    # ordine: tab504 dopo tab503
    _decl504 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl504.index(f'"{TITLE503}"') < _decl504.index(f'"{TITLE504}"')
    assert titoli[dvars.index("tab504")] == TITLE504


def test_chiavi_st504_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st504_[^"]+)"', src) + re.findall(
        r'key=f"(st504_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
