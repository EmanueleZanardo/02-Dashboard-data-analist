"""Test tab594 "💱⛽ Prezzo CO₂ di switch: gas vs carbone": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh594_num", "mh594_nneg", "mh594_eff", "mh594_serie",
           "mh594_costo_fuel", "mh594_intensita_co2", "mh594_pstar",
           "mh594_verdetto", "mh594_serie_pstar", "mh594_kpi_serie",
           "mh594_griglia", "mh594_demo", "_mh594_eta")

TITLE594 = "💱⛽ Prezzo CO₂ di switch: gas vs carbone"

DEMO = _F["mh594_demo"]()
# Caso base: p_gas=40, p_coal=15, eff 55/40, ef 0.202/0.341
#   costo_gas = 40/0.55 = 800/11 = 72.7272727
#   costo_carbone = 15/0.4 = 37.5
#   co2_gas = 0.202/0.55 = 101/275 = 0.3672727
#   co2_carbone = 0.341/0.4 = 341/400 = 0.8525
#   D = 427/880 = 0.48522727 ; P* = 31000/427 = 72.5995316
RES_DEMO = _F["mh594_pstar"](40, 15, 55, 40, 0.202, 0.341)
PSTAR_DEMO = 31000.0 / 427.0
D_DEMO = 427.0 / 880.0


class TestW594Validatori:
    def test_num_ok(self):
        assert _F["mh594_num"](2, "x") == 2.0
        assert _F["mh594_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, False, "2", None, [1], math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh594_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh594_nneg"](0, "x") == 0.0
        assert _F["mh594_nneg"](1.5, "x") == 1.5
        with pytest.raises(ValueError):
            _F["mh594_nneg"](-0.1, "x")

    def test_eff(self):
        assert _F["mh594_eff"](55, "e") == 55.0
        assert _F["mh594_eff"](100, "e") == 100.0
        for bad in (0, -1, 100.01, "x", True):
            with pytest.raises(ValueError):
                _F["mh594_eff"](bad, "e")


class TestW594Serie:
    def test_serie_ok(self):
        assert _F["mh594_serie"]([1, 2.5, -3], "s") == [1.0, 2.5, -3.0]
        assert _F["mh594_serie"]((4,), "s") == [4.0]

    def test_serie_ko(self):
        for bad in ([], "", "1,2", None, 5, [1, "x"], [True], [math.nan]):
            with pytest.raises(ValueError):
                _F["mh594_serie"](bad, "s")


class TestW594Formule:
    def test_costo_fuel(self):
        assert _F["mh594_costo_fuel"](40, 55) == pytest.approx(800.0 / 11.0)
        assert _F["mh594_costo_fuel"](15, 40) == pytest.approx(37.5)

    def test_intensita_co2(self):
        assert _F["mh594_intensita_co2"](0.202, 55) == pytest.approx(
            101.0 / 275.0)
        assert _F["mh594_intensita_co2"](0.341, 40) == pytest.approx(0.8525)

    def test_pstar_demo(self):
        r = RES_DEMO
        assert r["regime"] == "NORMALE"
        assert r["pstar"] == pytest.approx(PSTAR_DEMO, abs=1e-9)
        assert r["costo_gas_mwhe"] == pytest.approx(800.0 / 11.0)
        assert r["costo_carbone_mwhe"] == pytest.approx(37.5)
        assert r["co2_gas_mwhe"] == pytest.approx(101.0 / 275.0)
        assert r["co2_carbone_mwhe"] == pytest.approx(0.8525)
        assert r["d_co2"] == pytest.approx(D_DEMO, abs=1e-12)

    def test_pstar_gas_domina(self):
        # p_gas=10 -> costo_gas=200/11=18.18 < 37.5, D>0 -> P*<0
        r = _F["mh594_pstar"](10, 15, 55, 40, 0.202, 0.341)
        assert r["regime"] == "GAS_DOMINA"
        assert r["pstar"] == pytest.approx(-17000.0 / 427.0, abs=1e-9)

    def test_pstar_inversione(self):
        # eta gas 30 / carbone 90 -> carbone meno carbon-intensive per MWh_e
        r = _F["mh594_pstar"](40, 15, 30, 90, 0.202, 0.341)
        assert r["regime"] == "INVERSIONE"
        assert r["pstar"] is None
        assert r["d_co2"] < 0

    def test_pstar_ko(self):
        with pytest.raises(ValueError):
            _F["mh594_pstar"](40, 15, 0, 40, 0.202, 0.341)
        with pytest.raises(ValueError):
            _F["mh594_pstar"](-1, 15, 55, 40, 0.202, 0.341)
        with pytest.raises(ValueError):
            _F["mh594_pstar"](40, 15, 55, 40, -0.1, 0.341)

    def test_serie_pstar(self):
        r = _F["mh594_serie_pstar"]([40, 40], [15, 15], 55, 40, 0.202, 0.341)
        assert r == pytest.approx([PSTAR_DEMO, PSTAR_DEMO])

    def test_serie_pstar_lunghezze(self):
        with pytest.raises(ValueError):
            _F["mh594_serie_pstar"]([40, 40], [15], 55, 40, 0.202, 0.341)


class TestW594Verdetto:
    def test_gas_conviene(self):
        # EUA 82.5 > P* 72.5995 -> gas; diff = D*(82.5-P*) = 4.8040
        v = _F["mh594_verdetto"](RES_DEMO, 82.5)
        assert v["verdetto"] == "GAS_CONVIENE"
        assert v["delta_co2"] == pytest.approx(82.5 - PSTAR_DEMO, abs=1e-9)
        assert v["differenziale_mwhe"] == pytest.approx(4.8040, abs=1e-3)

    def test_carbone_conviene(self):
        # EUA 50 < P* -> carbone; diff = D*(50-P*) = -10.9659
        v = _F["mh594_verdetto"](RES_DEMO, 50)
        assert v["verdetto"] == "CARBONE_CONVIENE"
        assert v["delta_co2"] == pytest.approx(50 - PSTAR_DEMO, abs=1e-9)
        assert v["differenziale_mwhe"] == pytest.approx(-10.9659, abs=1e-3)

    def test_pareggio(self):
        v = _F["mh594_verdetto"](RES_DEMO, PSTAR_DEMO)
        assert v["verdetto"] == "PAREGGIO"
        assert v["delta_co2"] == pytest.approx(0.0, abs=1e-9)
        assert v["differenziale_mwhe"] == pytest.approx(0.0, abs=1e-9)

    def test_gas_domina_verdetto(self):
        r = _F["mh594_pstar"](10, 15, 55, 40, 0.202, 0.341)
        v = _F["mh594_verdetto"](r, 82.5)
        assert v["verdetto"] == "GAS_DOMINA"
        assert v["delta_co2"] == pytest.approx(82.5 + 17000.0 / 427.0,
                                               abs=1e-9)
        assert v["differenziale_mwhe"] == pytest.approx(59.3494, abs=1e-3)

    def test_inversione_verdetto(self):
        r = _F["mh594_pstar"](40, 15, 30, 90, 0.202, 0.341)
        v = _F["mh594_verdetto"](r, 82.5)
        assert v["verdetto"] == "INVERSIONE_PARAMETRI"
        assert v["delta_co2"] is None
        assert v["differenziale_mwhe"] is None

    def test_verdetto_ko(self):
        with pytest.raises(ValueError):
            _F["mh594_verdetto"]({"x": 1}, 82.5)
        with pytest.raises(ValueError):
            _F["mh594_verdetto"]({**RES_DEMO, "regime": "BOH"}, 82.5)
        with pytest.raises(ValueError):
            _F["mh594_verdetto"](RES_DEMO, -1)


class TestW594KpiGriglia:
    def test_kpi_serie(self):
        k = _F["mh594_kpi_serie"]([70.0, 80.0, PSTAR_DEMO], PSTAR_DEMO)
        assert k["n"] == 3
        assert k["ore_gas"] == 1
        assert k["ore_carbone"] == 1
        assert k["ore_pari"] == 1
        assert k["pct_gas"] == pytest.approx(100.0 / 3.0)
        assert k["pct_carbone"] == pytest.approx(100.0 / 3.0)

    def test_kpi_media(self):
        k = _F["mh594_kpi_serie"]([PSTAR_DEMO, PSTAR_DEMO], 82.5)
        assert k["media"] == pytest.approx(PSTAR_DEMO, abs=1e-9)
        assert k["minimo"] == pytest.approx(PSTAR_DEMO, abs=1e-9)
        assert k["massimo"] == pytest.approx(PSTAR_DEMO, abs=1e-9)
        assert k["ore_gas"] == 2

    def test_griglia(self):
        g = _F["mh594_griglia"](40, 15, 55, 40, 0.202, 0.341)
        assert len(g) == 25
        centro = [r for r in g
                  if r["delta_gas_pct"] == 0.0 and r["delta_coal_pct"] == 0.0]
        assert len(centro) == 1
        assert centro[0]["pstar"] == pytest.approx(72.60, abs=0.01)
        assert centro[0]["regime"] == "NORMALE"
        assert set(g[0]) == {"delta_gas_pct", "delta_coal_pct", "p_gas",
                             "p_coal", "pstar", "regime"}

    def test_griglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh594_griglia"](-1, 15, 55, 40, 0.202, 0.341)


class TestW594Demo:
    def test_demo(self):
        assert DEMO["p_gas"] == 40.0
        assert DEMO["p_coal"] == 15.0
        assert DEMO["eff_gas"] == 55.0
        assert DEMO["eua"] == 82.5
        assert len(DEMO["gas"]) == 48
        assert len(DEMO["coal"]) == 48


class TestW594Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 817
        assert TITLE594 in titles
        assert TITLE594 in titles

    def test_chain(self):
        assert ", tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817 = st.tabs([" in self._src()
        assert "with tab594:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st594_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
