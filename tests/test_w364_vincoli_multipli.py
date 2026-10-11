"""Test tab364 'Kelly con vincoli multipli: cap, lotti, stop e drawdown': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh364_num", "mh364_parse_seq", "mh364_fstar_sl", "mh364_g_sl",
           "mh364_cap", "mh364_lotti", "mh364_dd_mult", "mh364_bindings",
           "mh364_verdetto", "mh364_walk", "mh364_curva", "mh364_analisi")

TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
P = 0.6
B = 1.2
L = 0.5
FCAP = 0.2
LOT = 0.01
DD = 0.05
DDMAX = 0.25
SEQ = "WLWWLWWWLLWWWLWWLWLW"
FSTAR = 0.8666666666666667
FDCAP = 0.2
FDLOT = 0.2
FFIN = 0.16000000000000003
GSTAR = 0.20057626967129927
GFIN = 0.07202689761027432
GR = 0.3590997964430722
FINK = 198.83179954253245
FINV = 5.471496322668106
BIND = ['cap', 'drawdown']
VERDETTO = "VINCOLI FORTI (cap, drawdown): il tasso di crescita crolla al 35.9% dell'ottimo (f* 86.67% -> 16.00%). Valuta se tutti i vincoli sono davvero necessari."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry364:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 371
        assert "tab364" in dvars
        assert "tab364" in withs

    def test_titoli_allineati_360_361_362_363_364(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab371"
        assert titoli[-1] == TITLE371
        assert withs[-1] == "tab371"


class TestNum:
    def test_num_ok(self):
        assert _F["mh364_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_num"](float("nan"), "x")


class TestParseSeq:
    def test_ok(self):
        assert _F["mh364_parse_seq"]("wL") == ("W", "L")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_parse_seq"]("   ")

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_parse_seq"]("WX")


class TestFstarSl:
    def test_demo(self):
        assert abs(_F["mh364_fstar_sl"](P, B, L) - FSTAR) < 1e-12

    def test_stop_1_classico(self):
        assert abs(_F["mh364_fstar_sl"](P, B, 1.0)
                   - (P * B - (1.0 - P)) / B) < 1e-12

    def test_no_edge(self):
        assert _F["mh364_fstar_sl"](0.30, 1.0, 0.5) == 0.0

    def test_L_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_fstar_sl"](P, B, 0.0)


class TestGSl:
    def test_g_zero(self):
        assert _F["mh364_g_sl"](0.0, P, B, L) == 0.0

    def test_g_demo(self):
        assert abs(_F["mh364_g_sl"](FSTAR, P, B, L) - GSTAR) < 1e-12

    def test_g_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_g_sl"](1.0 / L, P, B, L)


class TestCap:
    def test_cap_vincolante(self):
        assert _F["mh364_cap"](FSTAR, FCAP) == FDCAP

    def test_cap_non_vincolante(self):
        assert _F["mh364_cap"](0.10, 0.30) == 0.10

    def test_fcap_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_cap"](0.10, 1.0)


class TestLotti:
    def test_demo(self):
        assert _F["mh364_lotti"](FDCAP, LOT) == FDLOT

    def test_floor_prudente(self):
        assert _F["mh364_lotti"](0.157, 0.05) == pytest.approx(0.15)

    def test_lot_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_lotti"](0.10, 0.0)


class TestDdMult:
    def test_demo(self):
        assert abs(_F["mh364_dd_mult"](DD, DDMAX) - 0.8) < 1e-12

    def test_azzerato_al_limite(self):
        assert _F["mh364_dd_mult"](DDMAX, DDMAX) == 0.0

    def test_ddmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_dd_mult"](0.05, 0.0)


class TestBindings:
    def test_demo(self):
        assert _F["mh364_bindings"](FSTAR, FDCAP, FDLOT, 0.8) == BIND

    def test_nessuno(self):
        assert _F["mh364_bindings"](0.10, 0.10, 0.10, 1.0) == []


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh364_verdetto"](0.0, 0.0, 1.0, []).startswith(
            "NESSUN EDGE")

    def test_non_vincolanti(self):
        assert _F["mh364_verdetto"](0.20, 0.20, 1.0, []).startswith(
            "NON VINCOLANTI")

    def test_leggeri(self):
        assert _F["mh364_verdetto"](0.20, 0.19, 0.99, ["cap"]).startswith(
            "VINCOLI LEGGERI")

    def test_significativi(self):
        assert _F["mh364_verdetto"](0.20, 0.15, 0.80,
                                   ["cap"]).startswith(
            "VINCOLI SIGNIFICATIVI")

    def test_forti(self):
        assert _F["mh364_verdetto"](0.20, 0.10, 0.50,
                                   ["cap", "drawdown"]).startswith(
            "VINCOLI FORTI")


class TestWalk:
    def test_demo(self):
        sq = _F["mh364_parse_seq"](SEQ)
        wk = _F["mh364_walk"](sq, FSTAR, B, L)
        wv = _F["mh364_walk"](sq, FFIN, B, L)
        assert wk["n"] == wv["n"] == 20
        assert abs(wk["finale"] - FINK) < 1e-9
        assert abs(wv["finale"] - FINV) < 1e-9
        assert len(wk["equity"]) == 21
        assert 0.0 <= wk["max_dd"] < 1.0

    def test_stop_tronca_perdita(self):
        sq = _F["mh364_parse_seq"]("L")
        w = _F["mh364_walk"](sq, 0.10, 2.0, 0.5)
        assert w["finale"] == pytest.approx(1.0 - 0.10 * 0.5)

    def test_f_zero_fermo(self):
        sq = _F["mh364_parse_seq"]("WL")
        w = _F["mh364_walk"](sq, 0.0, B, L)
        assert all(e == 1.0 for e in w["equity"])

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_walk"](("W",), 1.0 / L, B, L)


class TestCurva:
    def test_demo(self):
        c = _F["mh364_curva"](P, B, L, 1.90, 25)
        assert len(c) == 25
        assert c[0]["f"] == 0.0
        assert abs(c[0]["g"]) < 1e-15
        imax = max(range(25), key=lambda i: c[i]["g"])
        assert abs(c[imax]["f"] - FSTAR) < 0.10

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_curva"](P, B, L, 1.90, 1)


class TestAnalisi:
    def _demo(self):
        return _F["mh364_analisi"](P, B, L, FCAP, LOT, DD, DDMAX, SEQ)

    def test_demo(self):
        a = self._demo()
        assert abs(a["f_star"] - FSTAR) < 1e-12
        assert a["f_dopo_cap"] == FDCAP
        assert a["f_dopo_lotti"] == FDLOT
        assert abs(a["f_fin"] - FFIN) < 1e-9
        assert abs(a["g_star"] - GSTAR) < 1e-12
        assert abs(a["g_ratio"] - GR) < 1e-12
        assert abs(a["finalek"] - FINK) < 1e-9
        assert abs(a["finalev"] - FINV) < 1e-9
        assert a["bindings"] == BIND
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("VINCOLI FORTI")
        assert a["n"] == 20
        assert a["finalev"] < a["finalek"]

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["finalek"] == a2["finalek"]
        assert a1["verdetto"] == a2["verdetto"]

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_analisi"](0.0, B, L, FCAP, LOT, DD, DDMAX, SEQ)

    def test_ddmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_analisi"](P, B, L, FCAP, LOT, DD, 0.0, SEQ)

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh364_analisi"](P, B, L, FCAP, LOT, DD, DDMAX, "WX")
