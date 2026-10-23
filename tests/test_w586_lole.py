"""Test tab586 "LoLE & EENS: adeguatezza del parco di generazione": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh586_num", "mh586_num_nneg", "mh586_pos", "mh586_str",
           "mh586_for", "mh586_unita", "mh586_copt", "mh586_lolp",
           "mh586_eens_ora", "mh586_carichi", "mh586_parse_carichi",
           "mh586_demo", "mh586_riepilogo")

TITLE586 = "🔌📉 LoLE & EENS: adeguatezza del parco di generazione"


def _copt2():
    # 100 MW FOR 10% + 50 MW FOR 20% -> stati hand-computed
    return _F["mh586_copt"]([{"capacita_mw": 100.0, "for_pct": 10.0},
                             {"capacita_mw": 50.0, "for_pct": 20.0}])


class TestW586Validatori:
    def test_num_ok(self):
        assert _F["mh586_num"](2, "x") == 2.0
        assert _F["mh586_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh586_num"](bad, "x")

    def test_pos_ko(self):
        for bad in (0.0, -1.0, True, "x", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh586_pos"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh586_str"](bad, "x")

    def test_for_ok(self):
        assert _F["mh586_for"](0.0, "x") == 0.0
        assert _F["mh586_for"](100.0, "x") == 100.0
        assert _F["mh586_for"](4.5, "x") == 4.5

    def test_for_ko(self):
        for bad in (-0.1, 100.1, True, "x", None, math.nan):
            with pytest.raises(ValueError):
                _F["mh586_for"](bad, "x")


class TestW586Unita:
    def test_ok(self):
        u = _F["mh586_unita"]("G-1", "ccgt", 400.0, 4.0)
        assert u["capacita_mw"] == 400.0
        assert u["for_pct"] == 4.0
        assert u["prob_up"] == pytest.approx(0.96)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh586_unita"]("G-1", "x", 0.0, 4.0)
        with pytest.raises(ValueError):
            _F["mh586_unita"]("G-1", "x", 100.0, 101.0)
        with pytest.raises(ValueError):
            _F["mh586_unita"]("  ", "x", 100.0, 4.0)


class TestW586Copt:
    def test_stati_hand(self):
        c = _copt2()
        assert c["capacita_totale"] == 150.0
        assert c["n_unita"] == 2
        assert [o for o, _ in c["stati"]] == [0.0, 50.0, 100.0, 150.0]
        assert [p for _, p in c["stati"]] == pytest.approx(
            [0.72, 0.18, 0.08, 0.02])

    def test_prob_somma_uno(self):
        c = _copt2()
        assert sum(p for _, p in c["stati"]) == pytest.approx(1.0)

    def test_for_zero(self):
        c = _F["mh586_copt"]([{"capacita_mw": 80.0, "for_pct": 0.0}])
        assert c["stati"] == [(0.0, 1.0)]

    def test_for_cento(self):
        c = _F["mh586_copt"]([{"capacita_mw": 80.0, "for_pct": 100.0}])
        assert c["stati"] == [(80.0, 1.0)]

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh586_copt"]([])


class TestW586Lolp:
    def test_hand(self):
        c = _copt2()
        assert _F["mh586_lolp"](c, 0.0) == pytest.approx(0.0)
        assert _F["mh586_lolp"](c, 50.0) == pytest.approx(0.02)
        assert _F["mh586_lolp"](c, 100.0) == pytest.approx(0.10)
        assert _F["mh586_lolp"](c, 120.0) == pytest.approx(0.28)
        assert _F["mh586_lolp"](c, 150.0) == pytest.approx(0.28)
        assert _F["mh586_lolp"](c, 200.0) == pytest.approx(1.0)

    def test_bordo_nessuna_perdita(self):
        # outage == riserva esatta -> disponibile == carico -> non e'
        # perdita di carico (disuguaglianza stretta): 2x100 MW,
        # carico 100 -> conta solo l'outage totale (0.1^2)
        c = _F["mh586_copt"]([{"capacita_mw": 100.0, "for_pct": 10.0},
                               {"capacita_mw": 100.0, "for_pct": 10.0}])
        assert _F["mh586_lolp"](c, 100.0) == pytest.approx(0.01)

    def test_carico_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh586_lolp"](_copt2(), -1.0)


class TestW586Eens:
    def test_hand(self):
        c = _copt2()
        assert _F["mh586_eens_ora"](c, 50.0) == pytest.approx(1.0)
        assert _F["mh586_eens_ora"](c, 100.0) == pytest.approx(6.0)
        assert _F["mh586_eens_ora"](c, 120.0) == pytest.approx(11.6)
        assert _F["mh586_eens_ora"](c, 150.0) == pytest.approx(20.0)
        assert _F["mh586_eens_ora"](c, 200.0) == pytest.approx(70.0)
        assert _F["mh586_eens_ora"](c, 0.0) == pytest.approx(0.0)


class TestW586Carichi:
    def test_ok(self):
        assert _F["mh586_carichi"]([10, 20.5]) == [10.0, 20.5]

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh586_carichi"]([])
        with pytest.raises(ValueError):
            _F["mh586_carichi"]([10.0, -1.0])
        with pytest.raises(ValueError):
            _F["mh586_carichi"]("non lista")

    def test_parse_ok(self):
        vals = [str(v) for v in range(1, 25)]
        p = _F["mh586_parse_carichi"](", ".join(vals))
        assert p == [float(v) for v in range(1, 25)]

    def test_parse_misto_separatori(self):
        p = _F["mh586_parse_carichi"]("1 2;3\n" + " ".join(["4"] * 21))
        assert len(p) == 24 and p[2] == 3.0

    def test_parse_ko(self):
        with pytest.raises(ValueError):
            _F["mh586_parse_carichi"]("1, 2, 3")
        with pytest.raises(ValueError):
            _F["mh586_parse_carichi"](", ".join(["1"] * 23 + ["x"]))


class TestW586Riepilogo:
    def test_nessuna_unita(self):
        r = _F["mh586_riepilogo"]([], [100.0] * 24)
        assert r["verdetto"] == "NESSUNA_UNITA"

    def test_adeguato(self):
        uu = [_F["mh586_unita"]("U1", "a", 100.0, 1.0),
              _F["mh586_unita"]("U2", "b", 100.0, 1.0)]
        r = _F["mh586_riepilogo"](uu, [50.0] * 24, giorni=365,
                                  target_lole=3.0)
        assert r["verdetto"] == "ADEGUATO"
        assert r["lole_annuo"] == pytest.approx(0.876)
        assert r["eens_annuo"] == pytest.approx(43.8)
        assert r["margine_lole"] == pytest.approx(3.0 - 0.876)

    def test_non_adeguato(self):
        uu = [_F["mh586_unita"]("U1", "a", 100.0, 50.0)]
        r = _F["mh586_riepilogo"](uu, [90.0] * 24, giorni=365,
                                  target_lole=3.0)
        assert r["verdetto"] == "NON_ADEGUATO"
        assert r["lole_annuo"] == pytest.approx(4380.0)
        assert r["margine_lole"] < 0

    def test_id_duplicati_anomalia(self):
        uu = [_F["mh586_unita"]("D", "a", 100.0, 5.0),
              _F["mh586_unita"]("D", "b", 50.0, 5.0)]
        r = _F["mh586_riepilogo"](uu, [100.0] * 24)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("duplicato" in a for a in r["anomalie"])

    def test_carico_oltre_installato_anomalia(self):
        uu = [_F["mh586_unita"]("U1", "a", 100.0, 5.0)]
        r = _F["mh586_riepilogo"](uu, [120.0] * 24)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 24
        assert all(o["lolp"] == pytest.approx(1.0) for o in r["ore"])

    def test_giorni_target_ko(self):
        uu = [_F["mh586_unita"]("U1", "a", 100.0, 5.0)]
        with pytest.raises(ValueError):
            _F["mh586_riepilogo"](uu, [50.0] * 24, giorni=0)
        with pytest.raises(ValueError):
            _F["mh586_riepilogo"](uu, [50.0] * 24, target_lole=-1.0)


class TestW586Demo:
    def test_demo(self):
        d = _F["mh586_demo"]()
        assert len(d["unita"]) == 6
        assert len(d["carichi_mw"]) == 24
        r = _F["mh586_riepilogo"](d["unita"], d["carichi_mw"])
        assert r["verdetto"] == "NON_ADEGUATO"
        assert r["lole_annuo"] == pytest.approx(60.48, abs=0.05)
        assert r["eens_annuo"] == pytest.approx(3764.0, abs=1.0)
        assert r["capacita_totale"] == pytest.approx(900.0)
        assert r["n_anomalie"] == 0


class TestW586Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_presente(self):
        assert f'"{TITLE586}"' in self._src()

    def test_conteggio_tab(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 671
        assert TITLE586 in titles

    def test_chain_tab_var(self):
        assert ", tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671 = st.tabs([" in self._src()
        assert "with tab586:" in self._src()

    def test_chiavi_univoche(self):
        keys = set(re.findall(r"st586_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
