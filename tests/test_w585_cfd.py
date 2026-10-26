"""Test tab585 "CfD a due vie: payoff, MtM e sensibilita'": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh585_num", "mh585_num_nneg", "mh585_pos", "mh585_str",
           "mh585_contratto", "mh585_demo", "mh585_riepilogo",
           "mh585_sensibilita")

TITLE585 = "📜⚖️ CfD a due vie: payoff, MtM e sensibilità"


def _k(sid="K-1", descrizione="cfd", strike=60.0, riferimento=50.0,
       volume=1000.0, **kw):
    return _F["mh585_contratto"](sid, descrizione, strike, riferimento,
                                 volume, **kw)


class TestW585Validatori:
    def test_num_ok(self):
        assert _F["mh585_num"](2, "x") == 2.0
        assert _F["mh585_num"](-3.5, "x") == -3.5
        assert _F["mh585_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh585_num"](bad, "x")

    def test_num_nneg_ok(self):
        assert _F["mh585_num_nneg"](0.0, "x") == 0.0
        assert _F["mh585_num_nneg"](2.5, "x") == 2.5

    def test_num_nneg_ko(self):
        for bad in (-0.1, -1, True, "x", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh585_num_nneg"](bad, "x")

    def test_pos_ok(self):
        assert _F["mh585_pos"](0.001, "x") == pytest.approx(0.001)
        assert _F["mh585_pos"](5, "x") == 5.0

    def test_pos_ko(self):
        for bad in (0.0, -1.0, True, "x", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh585_pos"](bad, "x")

    def test_str_ok(self):
        assert _F["mh585_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh585_str"](bad, "x")


class TestW585Contratto:
    def test_payoff_itm(self):
        c = _k(strike=60.0, riferimento=50.0, volume=1000.0)
        assert c["completa"]
        assert c["payoff_unitario"] == pytest.approx(10.0)
        assert c["payoff_totale"] == pytest.approx(10000.0)
        assert c["moneyness"] == "IN_THE_MONEY"
        assert c["ricavo_merchant"] == pytest.approx(50000.0)
        assert c["ricavo_totale"] == pytest.approx(60000.0)
        assert c["strike_effettivo"] == pytest.approx(60.0)

    def test_payoff_otm(self):
        c = _k(strike=60.0, riferimento=75.0, volume=2000.0)
        assert c["completa"]
        assert c["payoff_unitario"] == pytest.approx(-15.0)
        assert c["payoff_totale"] == pytest.approx(-30000.0)
        assert c["moneyness"] == "OUT_OF_THE_MONEY"
        assert c["ricavo_totale"] == pytest.approx(120000.0)
        assert c["strike_effettivo"] == pytest.approx(60.0)

    def test_at_the_money(self):
        c = _k(strike=50.0, riferimento=50.0, volume=1000.0)
        assert c["completa"]
        assert c["payoff_unitario"] == pytest.approx(0.0)
        assert c["payoff_totale"] == pytest.approx(0.0)
        assert c["moneyness"] == "AT_THE_MONEY"

    def test_collar_cap(self):
        c = _k("C1", "collar", 92.0, 120.0, 80000.0,
               cap_u=5.0, floor_u=-25.0)
        assert c["completa"]
        assert c["payoff_unitario"] == pytest.approx(-25.0)
        assert c["payoff_totale"] == pytest.approx(-2000000.0)
        assert c["strike_effettivo"] == pytest.approx(95.0)

    def test_collar_floor(self):
        c = _k("C2", "collar", 40.0, 10.0, 1000.0,
               cap_u=5.0, floor_u=-25.0)
        assert c["payoff_unitario"] == pytest.approx(5.0)
        assert c["payoff_totale"] == pytest.approx(5000.0)

    def test_collar_non_vincolante(self):
        c = _k("C3", "collar", 60.0, 55.0, 1000.0,
               cap_u=50.0, floor_u=-50.0)
        assert c["payoff_unitario"] == pytest.approx(5.0)

    def test_collar_ko(self):
        with pytest.raises(ValueError):
            _k(floor_u=10.0, cap_u=5.0)

    def test_strike_negativo_ko(self):
        with pytest.raises(ValueError):
            _k(strike=-1.0)

    def test_volume_zero_ko(self):
        with pytest.raises(ValueError):
            _k(volume=0.0)

    def test_volume_negativo_ko(self):
        with pytest.raises(ValueError):
            _k(volume=-100.0)

    def test_riferimento_negativo_anomalia(self):
        c = _k(strike=60.0, riferimento=-5.0, volume=1000.0)
        assert not c["completa"]
        assert c["anomalie"] == ["Prezzo di riferimento negativo "
                                 "da verificare"]
        assert c["payoff_totale"] is None
        assert c["moneyness"] is None

    def test_tipi_ko(self):
        with pytest.raises(ValueError):
            _k(strike=True)
        with pytest.raises(ValueError):
            _k(strike="60")
        with pytest.raises(ValueError):
            _k(riferimento=math.nan)
        with pytest.raises(ValueError):
            _k(volume=math.inf)
        with pytest.raises(ValueError):
            _k(sid="   ")
        with pytest.raises(ValueError):
            _k(descrizione="")
        with pytest.raises(ValueError):
            _k(cap_u="x")

    def test_demo(self):
        d = _F["mh585_demo"]()
        assert len(d) == 3
        assert all(c["completa"] for c in d)
        assert d[0]["payoff_totale"] == pytest.approx(-875000.0)
        assert d[1]["payoff_totale"] == pytest.approx(504000.0)
        assert d[2]["payoff_totale"] == pytest.approx(-2000000.0)
        assert (d[0]["moneyness"], d[1]["moneyness"],
                d[2]["moneyness"]) == ("OUT_OF_THE_MONEY",
                                       "IN_THE_MONEY",
                                       "OUT_OF_THE_MONEY")


class TestW585Riepilogo:
    def test_vuoto(self):
        r = _F["mh585_riepilogo"]([])
        assert r["verdetto"] == "NESSUN_CONTRATTO"
        assert r["n_contratti"] == 0
        assert r["payoff_totale"] == 0.0

    def test_tutti_itm(self):
        r = _F["mh585_riepilogo"](
            [_k("A", "a", 60.0, 50.0, 1000.0),
             _k("B", "b", 70.0, 60.0, 1000.0)])
        assert r["verdetto"] == "TUTTI_IN_THE_MONEY"
        assert (r["n_itm"], r["n_otm"], r["n_atm"]) == (2, 0, 0)
        assert r["payoff_totale"] == pytest.approx(20000.0)

    def test_tutti_otm(self):
        r = _F["mh585_riepilogo"](
            [_k("A", "a", 60.0, 75.0, 1000.0),
             _k("B", "b", 70.0, 80.0, 1000.0)])
        assert r["verdetto"] == "TUTTI_OUT_OF_THE_MONEY"
        assert (r["n_itm"], r["n_otm"]) == (0, 2)

    def test_misti(self):
        r = _F["mh585_riepilogo"](_F["mh585_demo"]())
        assert r["verdetto"] == "MISTI"
        assert (r["n_contratti"], r["n_completi"],
                r["n_anomalie"]) == (3, 3, 0)
        assert (r["n_itm"], r["n_otm"], r["n_atm"]) == (1, 2, 0)
        assert r["payoff_totale"] == pytest.approx(-2371000.0)

    def test_duplicati(self):
        r = _F["mh585_riepilogo"]([_k("DUP"), _k("DUP")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert r["n_completi"] == 0

    def test_anomalia_precede(self):
        r = _F["mh585_riepilogo"](
            [_k("A", "a", 60.0, 50.0, 1000.0),
             _k("B", "b", 60.0, -3.0, 1000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert (r["n_completi"], r["n_anomalie"]) == (1, 1)


class TestW585Sensibilita:
    def test_griglia(self):
        rows = _F["mh585_sensibilita"]("S", "d", 60.0, 50.0, 1000.0,
                                      None, None, [-0.2, 0.0, 0.2])
        assert len(rows) == 3
        assert rows[1]["riferimento"] == pytest.approx(50.0)
        assert rows[1]["payoff_unitario"] == pytest.approx(10.0)
        assert rows[1]["payoff_totale"] == pytest.approx(10000.0)
        assert rows[1]["moneyness"] == "IN_THE_MONEY"

    def test_estremi(self):
        rows = _F["mh585_sensibilita"]("S", "d", 60.0, 50.0, 1000.0,
                                      None, None, [-0.2, 0.2])
        assert rows[0]["riferimento"] == pytest.approx(40.0)
        assert rows[0]["payoff_unitario"] == pytest.approx(20.0)
        assert rows[1]["riferimento"] == pytest.approx(60.0)
        assert rows[1]["payoff_unitario"] == pytest.approx(0.0)
        assert rows[1]["moneyness"] == "AT_THE_MONEY"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh585_sensibilita"]("S", "d", 60.0, 50.0, 1000.0,
                                    None, None, [])
        with pytest.raises(ValueError):
            _F["mh585_sensibilita"]("S", "d", 60.0, 50.0, 1000.0,
                                    None, None, "x")
        with pytest.raises(ValueError):
            _F["mh585_sensibilita"]("S", "d", 60.0, 50.0, 1000.0,
                                    None, None, [0.1, "a"])


class TestW585Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE585}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 731
        assert TITLE585 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731 = st.tabs([" in src
        assert "with tab585:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st585_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
