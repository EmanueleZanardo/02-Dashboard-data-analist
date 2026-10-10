"""Test tab363 'Kelly con limite di posizione: sizing con cap f_max': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh363_num", "mh363_parse_seq", "mh363_g", "mh363_fstar",
           "mh363_feff", "mh363_verdetto", "mh363_walk", "mh363_curva",
           "mh363_analisi")

TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
P = 0.6
B = 1.2
FMAX = 0.15
SEQ = "WLWWLWWWLLWWWLWWLWLW"
FK = 0.26666666666666666
FEFF = 0.15
GK = 0.04251707063743193
GEFF = 0.03430109128743403
GR = 0.8067604558164321
FINK = 4.212802392411251
FINE = 2.756757564718123
VERDETTO = "VINCOLO SIGNIFICATIVO: cap 15.00% su f* 26.67%, il tasso di crescita scende al 80.7% dell'ottimo (15.00% invece di 26.67%)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry363:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 368
        assert "tab363" in dvars
        assert "tab363" in withs

    def test_titoli_allineati_359_360_361_362_363(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab359")] == TITLE359
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab368"
        assert titoli[-1] == TITLE368
        assert withs[-1] == "tab368"


class TestNum:
    def test_num_ok(self):
        assert _F["mh363_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_num"](float("nan"), "x")


class TestParseSeq:
    def test_ok(self):
        assert _F["mh363_parse_seq"]("wL") == ("W", "L")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_parse_seq"]("   ")

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_parse_seq"]("WX")


class TestG:
    def test_g_zero(self):
        assert _F["mh363_g"](0.0, P, B) == 0.0

    def test_g_demo(self):
        assert abs(_F["mh363_g"](FK, P, B) - GK) < 1e-12

    def test_g_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_g"](1.0, P, B)


class TestFstar:
    def test_demo(self):
        assert abs(_F["mh363_fstar"](P, B) - FK) < 1e-12

    def test_no_edge(self):
        assert _F["mh363_fstar"](0.30, 1.0) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_fstar"](P, 0.0)


class TestFeff:
    def test_cap_vincolante(self):
        assert _F["mh363_feff"](FK, FMAX) == FEFF

    def test_cap_non_vincolante(self):
        assert _F["mh363_feff"](0.10, 0.30) == 0.10

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_feff"](0.10, 1.0)


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh363_verdetto"](0.0, 0.20, 0.0, 1.0).startswith(
            "NESSUN EDGE")

    def test_cap_non_vincolante(self):
        assert _F["mh363_verdetto"](0.10, 0.30, 0.10, 1.0).startswith(
            "CAP NON VINCOLANTE")

    def test_vincolo_leggero(self):
        assert _F["mh363_verdetto"](0.20, 0.15, 0.15, 0.99).startswith(
            "VINCOLO LEGGERO")

    def test_vincolo_significativo(self):
        assert _F["mh363_verdetto"](0.20, 0.15, 0.15, 0.80).startswith(
            "VINCOLO SIGNIFICATIVO")

    def test_vincolo_forte(self):
        assert _F["mh363_verdetto"](0.20, 0.10, 0.10, 0.50).startswith(
            "VINCOLO FORTE")


class TestWalk:
    def test_demo(self):
        sq = _F["mh363_parse_seq"](SEQ)
        wk = _F["mh363_walk"](sq, FK, B)
        we = _F["mh363_walk"](sq, FEFF, B)
        assert wk["n"] == we["n"] == 20
        assert abs(wk["finale"] - FINK) < 1e-9
        assert abs(we["finale"] - FINE) < 1e-9
        assert len(wk["equity"]) == 21
        assert 0.0 <= wk["max_dd"] < 1.0

    def test_f_zero_fermo(self):
        sq = _F["mh363_parse_seq"]("WL")
        w = _F["mh363_walk"](sq, 0.0, B)
        assert all(e == 1.0 for e in w["equity"])

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_walk"](("W",), 1.0, B)


class TestCurva:
    def test_demo(self):
        c = _F["mh363_curva"](P, B, 0.60, 25)
        assert len(c) == 25
        assert c[0]["f"] == 0.0
        assert abs(c[0]["g"]) < 1e-15
        imax = max(range(25), key=lambda i: c[i]["g"])
        assert abs(c[imax]["f"] - FK) < 0.03

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_curva"](P, B, 0.60, 1)


class TestAnalisi:
    def _demo(self):
        return _F["mh363_analisi"](P, B, FMAX, SEQ)

    def test_demo(self):
        a = self._demo()
        assert abs(a["f_kelly"] - FK) < 1e-12
        assert a["f_eff"] == FEFF
        assert abs(a["g_kelly"] - GK) < 1e-12
        assert abs(a["g_ratio"] - GR) < 1e-12
        assert abs(a["finalek"] - FINK) < 1e-9
        assert abs(a["finalee"] - FINE) < 1e-9
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("VINCOLO SIGNIFICATIVO")
        assert a["n"] == 20
        assert a["finalee"] < a["finalek"]

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["finalek"] == a2["finalek"]
        assert a1["verdetto"] == a2["verdetto"]

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_analisi"](0.0, B, FMAX, SEQ)

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_analisi"](P, B, 2.0, SEQ)

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_analisi"](P, B, FMAX, "WX")
