"""Test tab506 '📉 Regressione di efficacia (OLS)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh506_num", "mh506_str", "mh506_serie", "mh506_ols",
           "mh506_test", "mh506_riepilogo")

TITLE506 = "📉 Regressione di efficacia (OLS)"
TITLE505 = "♻️ Recycling OCI: rilascio della riserva a P&L"


def _demo_xy():
    x = [120000.0, -80000.0, 45000.0, -60000.0, 90000.0, -30000.0]
    y = [-125800.0, 84200.0, -47100.0, 62900.0, -94100.0, 31400.0]
    return x, y


def _demo_lab():
    return ["Gen-Feb", "Mar", "Apr", "Mag", "Giu", "Lug"]


class TestW506Validatori:
    def test_num_ok(self):
        assert _F["mh506_num"](3, "x") == 3.0
        assert _F["mh506_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh506_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh506_str"]("  Gen-Feb  ", "x") == "Gen-Feb"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh506_str"](bad, "x")

    def test_serie_ok(self):
        assert _F["mh506_serie"]((1, 2, 3), "x") == [1.0, 2.0, 3.0]

    def test_serie_ko(self):
        with pytest.raises(ValueError):
            _F["mh506_serie"]([1.0, 2.0], "x")  # < 3 osservazioni
        with pytest.raises(ValueError):
            _F["mh506_serie"]([1.0, 2.0, float("nan")], "x")
        with pytest.raises(ValueError):
            _F["mh506_serie"]("abc", "x")


class TestW506Ols:
    def test_demo(self):
        x, y = _demo_xy()
        st = _F["mh506_ols"](x, y)
        assert st["n"] == 6
        assert st["slope"] == pytest.approx(-1.048564, abs=1e-5)
        assert st["intercept"] == pytest.approx(104.66, abs=0.5)
        assert st["r2"] == pytest.approx(0.999997, abs=1e-5)
        assert st["se_slope"] == pytest.approx(0.000929, abs=1e-5)
        assert st["t_stat"] == pytest.approx(-52.2554, abs=1e-2)
        assert 0.0 < st["p_value"] < 1e-4

    def test_retta_esatta(self):
        # y = -1.1*x + 500 -> slope -1.1, R2 = 1, se = 0
        x = [100.0, 200.0, 300.0, 400.0]
        y = [-1.1 * v + 500.0 for v in x]
        st = _F["mh506_ols"](x, y)
        assert st["slope"] == pytest.approx(-1.1)
        assert st["intercept"] == pytest.approx(500.0)
        assert st["r2"] == pytest.approx(1.0)
        assert st["se_slope"] == 0.0

    def test_varianza_x_nulla(self):
        with pytest.raises(ValueError):
            _F["mh506_ols"]([5.0, 5.0, 5.0], [1.0, 2.0, 3.0])

    def test_lunghezze_diverse(self):
        with pytest.raises(ValueError):
            _F["mh506_ols"]([1.0, 2.0, 3.0], [1.0, 2.0])

    def test_poche_osservazioni(self):
        with pytest.raises(ValueError):
            _F["mh506_ols"]([1.0, 2.0], [1.0, 2.0])

    def test_nan_vietato(self):
        with pytest.raises(ValueError):
            _F["mh506_ols"]([1.0, 2.0, float("nan")], [1.0, 2.0, 3.0])


class TestW506Verdetti:
    def test_efficace(self):
        x, y = _demo_xy()
        st = _F["mh506_test"](x, y)
        assert st["verdetto"] == "EFFICACE"
        assert st["h0_non_rifiutata"] is False  # se piccolissimo

    def test_con_riserva_fit_debole(self):
        # slope in banda ma R2 basso: punti rumorosi attorno a b=-1
        x = [100.0, -80.0, 60.0, -40.0, 90.0, -30.0, 50.0, -70.0]
        y = [-130.0, 30.0, -20.0, 70.0, -40.0, -10.0, -90.0, 110.0]
        st = _F["mh506_test"](x, y)
        assert 0.8 <= abs(st["slope"]) <= 1.25
        assert st["r2"] < 0.8
        assert st["verdetto"] == "EFFICACE_CON_RISERVA"

    def test_inefficace_segno_errato(self):
        # strumento che amplifica: slope positiva
        x = [100.0, -80.0, 60.0, -40.0, 90.0]
        y = [105.0, -84.0, 63.0, -42.0, 95.0]
        st = _F["mh506_test"](x, y)
        assert st["slope"] > 0
        assert st["verdetto"] == "INEFFICACE"

    def test_inefficace_fuori_banda(self):
        # sottocopertura: slope -0.5
        x = [100.0, -80.0, 60.0, -40.0, 90.0, -30.0]
        y = [-50.0, 40.0, -30.0, 20.0, -45.0, 15.0]
        st = _F["mh506_test"](x, y)
        assert abs(st["slope"]) == pytest.approx(0.5, abs=0.01)
        assert st["verdetto"] == "INEFFICACE"

    def test_bordi_banda(self):
        # slope esattamente -0.8 -> EFFICACE (bordo incluso)
        x = [100.0, -80.0, 60.0, -40.0, 90.0, -30.0]
        y = [-80.0, 64.0, -48.0, 32.0, -72.0, 24.0]
        st = _F["mh506_test"](x, y)
        assert st["slope"] == pytest.approx(-0.8)
        assert st["verdetto"] == "EFFICACE"

    def test_parametri_ko(self):
        x, y = _demo_xy()
        with pytest.raises(ValueError):
            _F["mh506_test"](x, y, banda_inf=1.3, banda_sup=1.0)
        with pytest.raises(ValueError):
            _F["mh506_test"](x, y, r2_min=1.5)
        with pytest.raises(ValueError):
            _F["mh506_test"](x, y, banda_inf=0.0)


class TestW506Riepilogo:
    def test_demo(self):
        x, y = _demo_xy()
        s = _F["mh506_riepilogo"](_demo_lab(), x, y)
        assert s["n_periodi"] == 6
        assert s["verdetto"] == "EFFICACE"
        assert s["slope"] == pytest.approx(-1.048564, abs=1e-5)
        assert s["r2"] == pytest.approx(0.999997, abs=1e-5)
        assert s["banda"] == (0.8, 1.25)
        assert s["r2_min"] == 0.8
        assert len(s["righe"]) == 6
        assert s["righe"][0]["periodo"] == "Gen-Feb"
        assert s["righe"][0]["offset_eur"] == pytest.approx(-5800.0)

    def test_etichette_ko(self):
        x, y = _demo_xy()
        with pytest.raises(ValueError):
            _F["mh506_riepilogo"](["solo", "due"], x, y)


def test_registry_tab506():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 819
    assert TITLE506 in titoli
    assert src.count(TITLE506) == 3
    assert "tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819 = st.tabs([" in src
    assert "    with tab506:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab506" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab506" in withs
    assert len(withs) == len(dvars) == 819
    # ordine: tab506 dopo tab505
    _decl506 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl506.index(f'"{TITLE505}"') < _decl506.index(f'"{TITLE506}"')
    assert titoli[dvars.index("tab506")] == TITLE506


def test_chiavi_st506_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st506_[^"]+)"', src) + re.findall(
        r'key=f"(st506_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
