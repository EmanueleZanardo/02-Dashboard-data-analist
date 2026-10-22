"""Test tab593 "🔥📈 Spark/Dark spread: margini di generazione (clean)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh593_num", "mh593_nneg", "mh593_eff", "mh593_serie",
           "mh593_spread", "mh593_clean", "mh593_serie_spread",
           "mh593_serie_clean", "mh593_kpi", "mh593_confronto",
           "mh593_fuel_switch", "mh593_demo", "_mh593_eta")

TITLE593 = "🔥📈 Spark/Dark spread: margini di generazione (clean)"

DEMO = _F["mh593_demo"]()


class TestW593Validatori:
    def test_num_ok(self):
        assert _F["mh593_num"](2, "x") == 2.0
        assert _F["mh593_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, False, "2", None, [1], math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh593_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh593_nneg"](0, "x") == 0.0
        assert _F["mh593_nneg"](1.5, "x") == 1.5
        with pytest.raises(ValueError):
            _F["mh593_nneg"](-0.1, "x")

    def test_eff(self):
        assert _F["mh593_eff"](55, "e") == 55.0
        assert _F["mh593_eff"](100, "e") == 100.0
        for bad in (0, -1, 100.01, "x", True):
            with pytest.raises(ValueError):
                _F["mh593_eff"](bad, "e")


class TestW593Serie:
    def test_ok(self):
        assert _F["mh593_serie"]([1, 2.5, -3], "s") == [1.0, 2.5, -3.0]
        assert _F["mh593_serie"]((4,), "s") == [4.0]

    def test_ko(self):
        for bad in ([], "", "1,2", None, 5, [1, "x"], [True], [math.nan]):
            with pytest.raises(ValueError):
                _F["mh593_serie"](bad, "s")


class TestW593Formule:
    def test_spread(self):
        # P=80, F=40, eta=50% -> 80 - 80 = 0
        assert _F["mh593_spread"](80, 40, 50) == pytest.approx(0.0)
        # eta=100% -> 80 - 40 = 40
        assert _F["mh593_spread"](80, 40, 100) == pytest.approx(40.0)

    def test_spread_negativi(self):
        with pytest.raises(ValueError):
            _F["mh593_spread"](80, -1, 50)
        with pytest.raises(ValueError):
            _F["mh593_spread"](80, 40, 0)

    def test_clean(self):
        # spread=10, co2=100, ef=0.2, eta=50% -> 10 - 40 = -30
        assert _F["mh593_clean"](10, 100, 0.2, 50) == pytest.approx(-30.0)

    def test_clean_senza_co2(self):
        assert _F["mh593_clean"](7.5, 0, 0.341, 40) == pytest.approx(7.5)

    def test_serie_spread(self):
        r = _F["mh593_serie_spread"]([100, 80], [40, 40], 50)
        assert r == pytest.approx([20.0, 0.0])

    def test_serie_spread_lunghezze(self):
        with pytest.raises(ValueError):
            _F["mh593_serie_spread"]([100, 80], [40], 50)

    def test_serie_clean_scalare_e_serie(self):
        r1 = _F["mh593_serie_clean"]([10, 10], 100, 0.2, 50)
        r2 = _F["mh593_serie_clean"]([10, 10], [100, 50], 0.2, 50)
        assert r1 == pytest.approx([-30.0, -30.0])
        assert r2 == pytest.approx([-30.0, -10.0])

    def test_serie_clean_lunghezze(self):
        with pytest.raises(ValueError):
            _F["mh593_serie_clean"]([10, 10], [100], 0.2, 50)


class TestW593Kpi:
    def test_kpi(self):
        k = _F["mh593_kpi"]([10, -5, 0, 20])
        assert k["n"] == 4
        assert k["media"] == pytest.approx(6.25)
        assert k["minimo"] == pytest.approx(-5.0)
        assert k["massimo"] == pytest.approx(20.0)
        assert k["somma"] == pytest.approx(25.0)
        assert k["ore_positive"] == 2
        assert k["ore_negative"] == 1
        assert k["pct_positive"] == pytest.approx(50.0)
        assert k["pct_negative"] == pytest.approx(25.0)

    def test_kpi_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh593_kpi"]([])


class TestW593Confronto:
    def test_migliore(self):
        r = _F["mh593_confronto"]({"gas": 3.5, "carbone": 9.2})
        assert r["migliore"] == "carbone"
        assert [n for n, _ in r["classifica"]] == ["carbone", "gas"]

    def test_pareggio_deterministico(self):
        r = _F["mh593_confronto"]({"b": 1.0, "a": 1.0})
        assert r["migliore"] == "a"

    def test_ko(self):
        for bad in ({}, {"x": "no"}, {"": 1.0}, {"x": True}, [("a", 1)]):
            with pytest.raises(ValueError):
                _F["mh593_confronto"](bad)


class TestW593FuelSwitch:
    def test_switch(self):
        r = _F["mh593_fuel_switch"]([5, 1, 3], [4, 6, 3])
        assert r["ore_gas_vince"] == 1
        assert r["ore_carbone_vince"] == 1
        assert r["ore_pari"] == 1
        assert r["n"] == 3
        assert r["pct_gas_vince"] == pytest.approx(100.0 / 3)

    def test_lunghezze(self):
        with pytest.raises(ValueError):
            _F["mh593_fuel_switch"]([1, 2], [1])


class TestW593Demo:
    def test_demo_shape(self):
        assert len(DEMO["power"]) == 48
        assert len(DEMO["gas"]) == 48
        assert len(DEMO["coal"]) == 48
        assert DEMO["co2"] == pytest.approx(82.5)
        assert DEMO["eff_gas"] == pytest.approx(55.0)
        assert DEMO["eff_coal"] == pytest.approx(40.0)

    def test_demo_coerente(self):
        sp = _F["mh593_serie_spread"](DEMO["power"], DEMO["gas"],
                                      DEMO["eff_gas"])
        cs = _F["mh593_serie_clean"](sp, DEMO["co2"], DEMO["ef_gas"],
                                     DEMO["eff_gas"])
        k = _F["mh593_kpi"](cs)
        assert k["n"] == 48
        # con CO2 a 82.5 il clean spark medio della demo e' negativo
        assert k["media"] < 0


class TestW593Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 648
        assert TITLE593 in titles
        assert TITLE593 in titles

    def test_chain(self):
        assert ", tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648 = st.tabs([" in self._src()
        assert "with tab593:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st593_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
