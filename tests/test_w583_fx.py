"""Test tab583 "Rischio cambio: costo EUR del procurement in USD": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh583_num", "mh583_str", "mh583_commodity", "mh583_unita",
           "mh583_hedge_ratio", "mh583_cambio", "mh583_posizione",
           "mh583_eur", "mh583_demo", "mh583_riepilogo")

TITLE583 = "💱📉 Rischio cambio: costo EUR del procurement in USD"


def _p(sid="F-1", descrizione="posizione", commodity="GNL",
       prezzo=11.50, quantita=480000.0, unita="MMBTU", hedge=0.6):
    return _F["mh583_posizione"](sid, descrizione, commodity, prezzo,
                                 quantita, unita, hedge)


class TestW583Validatori:
    def test_num_ok(self):
        assert _F["mh583_num"](2, "x") == 2.0
        assert _F["mh583_num"](-3.5, "x") == -3.5
        assert _F["mh583_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh583_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh583_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh583_str"](bad, "x")

    def test_commodity_ok(self):
        for c in ("GAS_NATURALE", "GNL", "PETROLIO", "CARBONE",
                  "ELETTRICITA", "ALTRO", "gnl"):
            assert _F["mh583_commodity"](c) == c.upper()

    def test_commodity_ko(self):
        for bad in ("SETTIMANA", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh583_commodity"](bad)

    def test_unita_ok(self):
        for u in ("MMBTU", "BBL", "TONN", "MWH", "SM3", "bbl"):
            assert _F["mh583_unita"](u) == u.upper()

    def test_unita_ko(self):
        for bad in ("KG", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh583_unita"](bad)

    def test_hedge_ok(self):
        assert _F["mh583_hedge_ratio"](0) == 0.0
        assert _F["mh583_hedge_ratio"](1) == 1.0
        assert _F["mh583_hedge_ratio"](0.35) == pytest.approx(0.35)

    def test_hedge_ko(self):
        for bad in (-0.01, 1.01, 2, "0.5", None, math.nan, True):
            with pytest.raises(ValueError):
                _F["mh583_hedge_ratio"](bad)

    def test_cambio_ok(self):
        assert _F["mh583_cambio"](1.10) == pytest.approx(1.10)

    def test_cambio_ko(self):
        for bad in (0.0, -1.10, "1.10", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh583_cambio"](bad)


class TestW583Posizione:
    def test_hand_f001(self):
        o = _F["mh583_posizione"]("F-001", "GNL cargo nov-26", "GNL",
                                  11.50, 480000.0, "MMBTU", 0.6)
        assert o["completa"] is True
        assert o["anomalie"] == []
        assert o["costo_usd"] == pytest.approx(5520000.0)
        assert o["coperto_usd"] == pytest.approx(3312000.0)
        assert o["scoperto_usd"] == pytest.approx(2208000.0)
        assert _F["mh583_eur"](o["costo_usd"], 1.10) == pytest.approx(
            5018181.818182, rel=1e-6)

    def test_hand_f003_scoperto_totale(self):
        o = _F["mh583_posizione"]("F-003", "Carbone API2 Q1-27",
                                  "CARBONE", 105.00, 15000.0, "TONN",
                                  0.0)
        assert o["costo_usd"] == pytest.approx(1575000.0)
        assert o["scoperto_usd"] == pytest.approx(1575000.0)
        assert o["coperto_usd"] == pytest.approx(0.0)

    def test_prezzo_zero_anomalia(self):
        o = _p(prezzo=0.0)
        assert o["completa"] is False
        assert any("Prezzo" in a for a in o["anomalie"])
        assert o["costo_usd"] is None

    def test_quantita_nulla_anomalia(self):
        o = _p(quantita=0.0)
        assert o["completa"] is False
        assert any("Quantita" in a for a in o["anomalie"])

    def test_prezzo_negativo_ko(self):
        with pytest.raises(ValueError):
            _p(prezzo=-1.0)

    def test_quantita_negativa_ko(self):
        with pytest.raises(ValueError):
            _p(quantita=-5.0)


class TestW583Demo:
    def test_demo_shape(self):
        d = _F["mh583_demo"]()
        assert len(d) == 3
        assert [x["id"] for x in d] == ["F-001", "F-002", "F-003"]
        assert all(x["completa"] for x in d)

    def test_demo_f002_hand(self):
        d = _F["mh583_demo"]()[1]
        assert d["costo_usd"] == pytest.approx(1564000.0)
        assert d["scoperto_usd"] == pytest.approx(938400.0)
        assert d["coperto_usd"] == pytest.approx(625600.0)


class TestW583Riepilogo:
    def test_vuoto(self):
        r = _F["mh583_riepilogo"]([], 1.10)
        assert r["verdetto"] == "NESSUNA_POSIZIONE"
        assert r["n_posizioni"] == 0

    def test_demo_esposizione_elevata(self):
        r = _F["mh583_riepilogo"](_F["mh583_demo"](), 1.10, 10.0, 50.0)
        assert r["verdetto"] == "ESPOSIZIONE_ELEVATA"
        assert r["n_posizioni"] == 3
        assert r["n_anomalie"] == 0
        assert r["costo_tot_usd"] == pytest.approx(8659000.0)
        assert r["costo_tot_eur"] == pytest.approx(7871818.181818,
                                                  rel=1e-6)
        assert r["scoperto_usd"] == pytest.approx(4721400.0)
        assert r["scoperto_eur"] == pytest.approx(4292181.818182,
                                                  rel=1e-6)
        assert r["esposto_pct"] == pytest.approx(54.525927, rel=1e-5)
        assert r["costo_shock_up_eur"] == pytest.approx(
            4769090.909091, rel=1e-6)
        assert r["costo_shock_down_eur"] == pytest.approx(
            3901983.471074, rel=1e-6)
        assert r["delta_shock_eur"] == pytest.approx(
            867107.438017, rel=1e-5)

    def test_soglia_custom_coperta(self):
        r = _F["mh583_riepilogo"](_F["mh583_demo"](), 1.10, 10.0, 60.0)
        assert r["verdetto"] == "ESPOSIZIONE_COPERTA"

    def test_duplicati_anomalia(self):
        r = _F["mh583_riepilogo"]([_p("X"), _p("X")], 1.10)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all(any("duplicato" in a for a in o["anomalie"])
                   for o in r["analizzati"])

    def test_anomalia_precede_verdetto(self):
        r = _F["mh583_riepilogo"]([_p("A"), _p("B", prezzo=0.0)], 1.10)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_completi"] == 1

    def test_cambio_ko(self):
        with pytest.raises(ValueError):
            _F["mh583_riepilogo"](_F["mh583_demo"](), 0.0)

    def test_shock_ko(self):
        with pytest.raises(ValueError):
            _F["mh583_riepilogo"](_F["mh583_demo"](), 1.10, 0.0)

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh583_riepilogo"](_F["mh583_demo"](), 1.10, 10.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh583_riepilogo"](_F["mh583_demo"](), 1.10, 10.0, 101.0)


class TestW583Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE583}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 806
        assert TITLE583 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806 = st.tabs([" in src
        assert "with tab583:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st583_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
