"""Test tab361 'Rischio di rovina (risk of ruin): probabilita' di rovina prima del target': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh361_num", "mh361_kelly", "mh361_griglia", "mh361_rischio",
           "mh361_verdetto", "mh361_curva", "mh361_analisi")

TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
P = 0.55
B = 1.0
F = 0.1
DD = 0.5
GOAL = 2.0
FSTAR = 0.10000000000000009
EDGE = 0.10000000000000009
ROR = 0.19707216357088447
TRADES = 42.40989709989181
K = 7
NLEV = 14
UP = 1
GSTEPS = 7
VERDETTO = "ELEVATO: P(rovina) = 19.7%: quasi 1 volta su 5 o piu' finisci sul drawdown massimo prima del target. Considera di dimezzare f: la curva qui sotto mostra quanto scende il rischio."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry361:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 366
        assert "tab361" in dvars
        assert "tab361" in withs

    def test_titoli_allineati_357_358_359_360_361(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab357")] == TITLE357
        assert titoli[dvars.index("tab358")] == TITLE358
        assert titoli[dvars.index("tab359")] == TITLE359
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab366"
        assert titoli[-1] == TITLE366
        assert withs[-1] == "tab366"


class TestNum:
    def test_num_ok(self):
        assert _F["mh361_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_num"](float("nan"), "x")


class TestKelly:
    def test_fstar_demo(self):
        assert abs(_F["mh361_kelly"](0.55, 1.0) - 0.10) < 1e-12

    def test_no_edge_zero(self):
        assert _F["mh361_kelly"](0.4, 1.0) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_kelly"](0.5, 0.0)


class TestGriglia:
    def test_demo(self):
        g = _F["mh361_griglia"](F, B, DD, GOAL)
        assert g["k"] == K == 7
        assert g["n_livelli"] == NLEV == 14
        assert g["up"] == UP == 1
        assert g["goal_steps"] == GSTEPS == 7

    def test_dd_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_griglia"](0.1, 1.0, 1.0, 2.0)

    def test_goal_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_griglia"](0.1, 1.0, 0.5, 1.0)

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_griglia"](1.0, 1.0, 0.5, 2.0)


class TestRischio:
    def _demo(self):
        return _F["mh361_analisi"](P, B, F, DD, GOAL)

    def test_demo_range(self):
        m = self._demo()
        assert 0.19 < m["ror"] < 0.21
        assert abs(m["ror"] - ROR) < 1e-12
        assert 40.0 < m["trades_attesi"] < 44.0
        assert abs(m["trades_attesi"] - TRADES) < 1e-9

    def test_demo_parametri(self):
        m = self._demo()
        assert abs(m["f_star"] - FSTAR) < 1e-12
        assert abs(m["edge"] - EDGE) < 1e-12
        assert m["verdetto"] == VERDETTO
        assert m["verdetto"].startswith("ELEVATO")
        assert m["p"] == P and m["b"] == B and m["f"] == F

    def test_determinismo(self):
        m1 = _F["mh361_rischio"](P, B, F, DD, GOAL)
        m2 = _F["mh361_rischio"](P, B, F, DD, GOAL)
        assert m1["ror"] == m2["ror"]
        assert m1["trades_attesi"] == m2["trades_attesi"]

    def test_f_zero_nessun_rischio(self):
        m = _F["mh361_rischio"](P, B, 0.0, DD, GOAL)
        assert m["ror"] == 0.0

    def test_p_zero_rovina_certa(self):
        m = _F["mh361_rischio"](0.0, B, F, DD, GOAL)
        assert m["ror"] == 1.0
        assert m["trades_attesi"] == m["k"] == 7

    def test_p_uno_rovina_impossibile(self):
        m = _F["mh361_rischio"](1.0, B, F, DD, GOAL)
        assert m["ror"] == 0.0
        assert m["trades_attesi"] == m["goal_steps"] == 7

    def test_monotonia_f(self):
        r_piccola = _F["mh361_rischio"](P, B, 0.05, DD, GOAL)["ror"]
        r_grande = _F["mh361_rischio"](P, B, 0.20, DD, GOAL)["ror"]
        assert r_grande > r_piccola

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_rischio"](P, B, 1.0, DD, GOAL)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_rischio"](1.5, B, F, DD, GOAL)


class TestVerdetto:
    def test_trascurabile(self):
        m = _F["mh361_analisi"](0.60, 1.0, 0.02, 0.5, 1.5)
        assert m["ror"] < 0.01
        assert m["verdetto"].startswith("TRASCURABILE")

    def test_contenuto(self):
        m = _F["mh361_analisi"](0.60, 1.0, 0.06, 0.5, 2.0)
        assert 0.01 <= m["ror"] < 0.05
        assert m["verdetto"].startswith("CONTENUTO")

    def test_moderato(self):
        m = _F["mh361_analisi"](0.58, 1.0, 0.08, 0.5, 2.0)
        assert 0.05 <= m["ror"] < 0.10
        assert m["verdetto"].startswith("MODERATO")

    def test_elevato(self):
        m = _F["mh361_analisi"](P, B, F, DD, GOAL)
        assert 0.10 <= m["ror"] < 0.25
        assert m["verdetto"].startswith("ELEVATO")

    def test_critico(self):
        m = _F["mh361_analisi"](0.52, 1.0, 0.40, 0.3, 3.0)
        assert m["ror"] >= 0.25
        assert m["verdetto"].startswith("CRITICO")

    def test_nota_edge_negativo(self):
        v = _F["mh361_verdetto"](0.30, -0.02)
        assert v.startswith("CRITICO")
        assert "edge" in v

    def test_ror_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_verdetto"](1.5, 0.1)


class TestCurva:
    def test_struttura(self):
        c = _F["mh361_curva"](P, B, DD, GOAL, 0.20, 25)
        assert len(c) == 25
        fs = [r["f"] for r in c]
        assert fs == sorted(fs) and len(set(fs)) == 25
        assert all(0.0 <= r["ror"] <= 1.0 for r in c)
        assert c[-1]["ror"] >= c[0]["ror"]

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_curva"](P, B, DD, GOAL, 0.20, 2)

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh361_curva"](P, B, DD, GOAL, 0.0, 25)

