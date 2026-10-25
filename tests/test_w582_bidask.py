"""Test tab582 "Bid-ask spread e costi di transazione": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh582_num", "mh582_str", "mh582_prodotto",
           "mh582_liquidita", "mh582_strumento", "mh582_demo",
           "mh582_riepilogo")

TITLE582 = "📊↔️ Bid-ask spread e costi di transazione"


def _s(sid="D-1", descrizione="strumento", prodotto="MONTH", bid=95.0,
       ask=95.4, lotto=1.0, ore=720.0):
    return _F["mh582_strumento"](sid, descrizione, prodotto, bid, ask,
                                 lotto, ore)


class TestW582Validatori:
    def test_num_ok(self):
        assert _F["mh582_num"](2, "x") == 2.0
        assert _F["mh582_num"](-3.5, "x") == -3.5
        assert _F["mh582_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh582_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh582_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh582_str"](bad, "x")

    def test_prodotto_ok(self):
        for p in ("DAY_AHEAD", "INTRADAY", "WEEK", "MONTH", "QUARTER",
                  "YEAR", "OTC", "month"):
            assert _F["mh582_prodotto"](p) == p.upper()

    def test_prodotto_ko(self):
        for bad in ("SETTIMANA", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh582_prodotto"](bad)


class TestW582Liquidita:
    def test_boundary(self):
        f = _F["mh582_liquidita"]
        assert f(0.49) == "MOLTO_LIQUIDO"
        assert f(0.5) == "LIQUIDO"
        assert f(1.99) == "LIQUIDO"
        assert f(2.0) == "POCO_LIQUIDO"
        assert f(4.99) == "POCO_LIQUIDO"
        assert f(5.0) == "ILLIQUIDO"
        assert f(25.0) == "ILLIQUIDO"


class TestW582Strumento:
    def test_hand_d001(self):
        o = _F["mh582_strumento"]("D-001", "DE Baseload M+1", "MONTH",
                                  95.00, 95.40, 1.0, 720.0)
        assert o["completa"] is True
        assert o["anomalie"] == []
        assert o["mid_eur_mwh"] == pytest.approx(95.20)
        assert o["spread_eur_mwh"] == pytest.approx(0.40)
        assert o["spread_pct"] == pytest.approx(0.420168, rel=1e-4)
        assert o["liquidita"] == "MOLTO_LIQUIDO"
        assert o["roundtrip_eur"] == pytest.approx(288.0)

    def test_hand_d003(self):
        o = _F["mh582_strumento"]("D-003", "FR Peak Q+1", "QUARTER",
                                  210.00, 218.00, 5.0, 2190.0)
        assert o["mid_eur_mwh"] == pytest.approx(214.00)
        assert o["spread_pct"] == pytest.approx(3.738317, rel=1e-4)
        assert o["liquidita"] == "POCO_LIQUIDO"
        assert o["roundtrip_eur"] == pytest.approx(87600.0)

    def test_crossed_market_anomalia(self):
        o = _s(bid=100.0, ask=99.0)
        assert o["completa"] is False
        assert any("crossed" in a for a in o["anomalie"])
        assert o["spread_eur_mwh"] is None

    def test_bid_uguale_ask_anomalia(self):
        o = _s(bid=100.0, ask=100.0)
        assert o["completa"] is False
        assert any("crossed" in a for a in o["anomalie"])

    def test_bid_zero_anomalia(self):
        o = _s(bid=0.0, ask=95.4)
        assert o["completa"] is False
        assert any("Bid" in a for a in o["anomalie"])

    def test_ask_negativo_anomalia(self):
        o = _s(bid=95.0, ask=-1.0)
        assert o["completa"] is False
        assert any("Ask" in a for a in o["anomalie"])

    def test_spread_eccessivo_anomalia(self):
        o = _s(bid=90.0, ask=110.0)  # spread% = 20/100*100 = 20%
        assert o["completa"] is False
        assert any("illiquida" in a for a in o["anomalie"])
        assert o["spread_pct"] == pytest.approx(20.0)

    def test_lotto_nullo_anomalia(self):
        o = _s(lotto=0.0)
        assert o["completa"] is False
        assert any("Lotto" in a for a in o["anomalie"])

    def test_lotto_negativo_ko(self):
        with pytest.raises(ValueError):
            _s(lotto=-1.0)

    def test_ore_nulle_ko(self):
        with pytest.raises(ValueError):
            _s(ore=0.0)

    def test_ore_negative_ko(self):
        with pytest.raises(ValueError):
            _s(ore=-5.0)

    def test_prodotto_non_valido_ko(self):
        with pytest.raises(ValueError):
            _s(prodotto="ANNO")

    def test_id_vuoto_ko(self):
        with pytest.raises(ValueError):
            _s(sid="   ")


class TestW582Demo:
    def test_demo_tre_strumenti(self):
        d = _F["mh582_demo"]()
        assert len(d) == 3
        assert [x["id"] for x in d] == ["D-001", "D-002", "D-003"]
        assert all(x["completa"] for x in d)

    def test_demo_d002_hand(self):
        d = _F["mh582_demo"]()[1]
        assert d["mid_eur_mwh"] == pytest.approx(119.75)
        assert d["spread_pct"] == pytest.approx(2.922761, rel=1e-4)
        assert d["liquidita"] == "POCO_LIQUIDO"
        assert d["roundtrip_eur"] == pytest.approx(588.0)


class TestW582Riepilogo:
    def test_vuoto(self):
        r = _F["mh582_riepilogo"]([])
        assert r["verdetto"] == "NESSUNO_STRUMENTO"
        assert r["n_strumenti"] == 0

    def test_demo_costi_elevati(self):
        r = _F["mh582_riepilogo"](_F["mh582_demo"]())
        assert r["verdetto"] == "COSTI_ELEVATI"
        assert r["n_strumenti"] == 3
        assert r["n_anomalie"] == 0
        assert r["spread_medio_pct"] == pytest.approx(2.360415,
                                                     rel=1e-4)
        assert r["roundtrip_tot_eur"] == pytest.approx(88476.0)
        assert r["miglior_id"] == "D-001"
        assert r["miglior_spread_pct"] == pytest.approx(0.420168,
                                                        rel=1e-4)

    def test_soglia_custom_liquido(self):
        r = _F["mh582_riepilogo"](_F["mh582_demo"](), soglia_pct=5.0)
        assert r["verdetto"] == "LIQUIDITA_ADEGUATA"

    def test_duplicati_anomalia(self):
        r = _F["mh582_riepilogo"]([_s("X"), _s("X")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2
        assert all(any("duplicato" in a for a in o["anomalie"])
                   for o in r["analizzati"])

    def test_anomalia_precede_verdetto(self):
        r = _F["mh582_riepilogo"]([_s("A"), _s("B", bid=100.0,
                                                ask=99.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_completi"] == 1

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["mh582_riepilogo"](_F["mh582_demo"](), soglia_pct=0.0)
        with pytest.raises(ValueError):
            _F["mh582_riepilogo"](_F["mh582_demo"](),
                                  soglia_pct="alta")


class TestW582Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE582}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 699
        assert TITLE582 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699 = st.tabs([" in src
        assert "with tab582:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st582_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
