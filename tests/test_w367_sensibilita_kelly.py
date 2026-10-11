"""Test tab367 'Kelly: mappa di sensibilità f* e crescita su (p, b)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh367_num", "mh367_fstar", "mh367_log_g", "mh367_p_edge",
           "mh367_margine", "mh367_griglia", "mh367_verdetto",
           "mh367_analisi")

TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
P = 0.6
B = 1.2
FSTAR = 0.26666666666666666
G = 0.04251707063743193
PEDGE = 0.45454545454545453
DELTA = 0.14545454545454545
VERDETTO = 'MARGINE ADEGUATO: cuscinetto di 14.5% su p: il sizing regge errori di stima moderati, mezza Kelly consigliata per prudenza.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry367:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 370
        assert "tab367" in dvars
        assert "tab367" in withs

    def test_titoli_allineati_362_363_364_365_366_367(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364
        assert titoli[dvars.index("tab365")] == TITLE365
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab370"
        assert titoli[-1] == TITLE370
        assert withs[-1] == "tab370"


class TestNum:
    def test_num_ok(self):
        assert _F["mh367_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_num"](float("inf"), "x")


class TestFstar:
    def test_demo(self):
        assert _F["mh367_fstar"](P, B) == pytest.approx(FSTAR)

    def test_forma_chiusa(self):
        assert _F["mh367_fstar"](0.7, 2.0) == pytest.approx((0.7 * 2 - 0.3) / 2)

    def test_no_edge(self):
        assert _F["mh367_fstar"](0.40, 1.0) == 0.0

    def test_sul_confine(self):
        # p = 1/(1+b) -> f* = 0
        assert _F["mh367_fstar"](1.0 / 2.2, 1.2) == pytest.approx(0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_fstar"](1.5, B)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_fstar"](P, 0.0)


class TestLogG:
    def test_demo(self):
        assert _F["mh367_log_g"](FSTAR, P, B) == pytest.approx(G)

    def test_f_zero(self):
        assert _F["mh367_log_g"](0.0, P, B) == pytest.approx(0.0)

    def test_f_uno_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_log_g"](1.0, P, B)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_log_g"](FSTAR, 0.0, B)


class TestPEdge:
    def test_identita(self):
        for b in (0.2, 0.5, 1.2, 3.0):
            assert _F["mh367_p_edge"](b) * (1.0 + b) == pytest.approx(1.0)

    def test_demo(self):
        assert _F["mh367_p_edge"](B) == pytest.approx(PEDGE)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_p_edge"](0.0)


class TestMargine:
    def test_demo(self):
        m = _F["mh367_margine"](P, B)
        assert m["p_edge"] == pytest.approx(PEDGE)
        assert m["delta_p"] == pytest.approx(DELTA)

    def test_sotto_edge(self):
        m = _F["mh367_margine"](0.40, 1.2)
        assert m["delta_p"] < 0.0

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_margine"](1.5, B)


class TestGriglia:
    def _gr(self):
        return _F["mh367_griglia"](0.30, 0.90, 0.20, 3.00, 41)

    def test_dimensioni(self):
        gr = self._gr()
        assert len(gr["ps"]) == 41
        assert len(gr["bs"]) == 41
        assert len(gr["fstar"]) == 41
        assert all(len(r) == 41 for r in gr["fstar"])
        assert len(gr["g"]) == 41
        assert all(len(r) == 41 for r in gr["g"])

    def test_estremi(self):
        gr = self._gr()
        assert gr["ps"][0] == pytest.approx(0.30)
        assert gr["ps"][-1] == pytest.approx(0.90)
        assert gr["bs"][0] == pytest.approx(0.20)
        assert gr["bs"][-1] == pytest.approx(3.00)

    def test_angoli_coerenti(self):
        gr = self._gr()
        assert gr["fstar"][0][0] == pytest.approx(
            _F["mh367_fstar"](gr["ps"][0], gr["bs"][0]))
        assert gr["g"][-1][-1] == pytest.approx(
            _F["mh367_log_g"](gr["fstar"][-1][-1],
                              gr["ps"][-1], gr["bs"][-1]))

    def test_zero_sotto_confine(self):
        gr = self._gr()
        b0 = gr["bs"][0]
        pe = 1.0 / (1.0 + b0)
        attesi = sum(1 for p in gr["ps"] if p <= pe)
        reali = sum(1 for f in gr["fstar"][0] if f == 0.0)
        assert attesi > 0
        assert reali == attesi

    def test_monotonia_in_p(self):
        gr = self._gr()
        for row in gr["fstar"]:
            assert all(a <= b for a, b in zip(row, row[1:]))

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_griglia"](0.30, 0.90, 0.20, 3.00, 1)

    def test_bounds_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_griglia"](0.90, 0.30, 0.20, 3.00, 41)


class TestVerdetto:
    def test_nessun_edge_margine(self):
        assert _F["mh367_verdetto"](-0.01, 0.02).startswith("NESSUN EDGE")

    def test_nessun_edge_g(self):
        assert _F["mh367_verdetto"](0.10, 0.0).startswith("NESSUN EDGE")

    def test_sottile(self):
        assert _F["mh367_verdetto"](0.03, 0.02).startswith("MARGINE SOTTILE")

    def test_adeguato(self):
        assert _F["mh367_verdetto"](0.10, 0.02).startswith("MARGINE ADEGUATO")

    def test_adeguato_al_limite(self):
        # 0.05 non e' < 0.05 -> ADEGUATO
        assert _F["mh367_verdetto"](0.05, 0.02).startswith("MARGINE ADEGUATO")

    def test_ampio(self):
        assert _F["mh367_verdetto"](0.30, 0.02).startswith("MARGINE AMPIO")

    def test_ampio_al_limite(self):
        # 0.15 non e' < 0.15 -> AMPIO
        assert _F["mh367_verdetto"](0.15, 0.02).startswith("MARGINE AMPIO")


class TestAnalisi:
    def _demo(self):
        return _F["mh367_analisi"](P, B)

    def test_demo(self):
        a = self._demo()
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["g"] == pytest.approx(G)
        assert a["p_edge"] == pytest.approx(PEDGE)
        assert a["delta_p"] == pytest.approx(DELTA)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("MARGINE ADEGUATO")
        assert len(a["griglia"]["ps"]) == 41

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["f_star"] == a2["f_star"]

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_analisi"](P, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_analisi"](1.5, B)
