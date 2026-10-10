"""Test tab366 'Kelly su N trade: raddoppio, dimezzamento e crescita attesa': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh366_num", "mh366_int", "mh366_fstar", "mh366_log_g",
           "mh366_pmf", "mh366_p_raddoppio", "mh366_p_dimezzamento",
           "mh366_quantili", "mh366_verdetto", "mh366_analisi")

TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
P = 0.6
B = 1.2
N = 100
FSTAR = 0.26666666666666666
G = 0.04251707063743193
LOGATT = 4.2517070637431935
MULT = 70.22518895837565
PRADD = 0.9070199083322035
PDIM = 0.0423014201891379
Q50 = 70.22518895837578
VERDETTO = "CRESCITA SOLIDA: P(raddoppio) = 91% con P(dimezzamento) = 4.2%: l'orizzonte premia il sizing pieno."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry366:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 366
        assert "tab366" in dvars
        assert "tab366" in withs

    def test_titoli_allineati_361_362_363_364_365_366(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364
        assert titoli[dvars.index("tab365")] == TITLE365
        assert titoli[dvars.index("tab366")] == TITLE366

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab366"
        assert titoli[-1] == TITLE366
        assert withs[-1] == "tab366"


class TestNum:
    def test_num_ok(self):
        assert _F["mh366_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_num"](float("nan"), "x")

    def test_int_ok(self):
        assert _F["mh366_int"](100.0, "n", 1) == 100

    def test_int_non_intero_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_int"](100.5, "n", 1)

    def test_int_sotto_minimo_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_int"](0, "n", 1)


class TestFstar:
    def test_demo(self):
        assert _F["mh366_fstar"](P, B) == pytest.approx(FSTAR)

    def test_no_edge(self):
        assert _F["mh366_fstar"](0.40, 1.0) == 0.0

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_fstar"](1.5, B)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_fstar"](P, 0.0)


class TestLogG:
    def test_demo(self):
        assert _F["mh366_log_g"](FSTAR, P, B) == pytest.approx(G)

    def test_f_zero(self):
        assert _F["mh366_log_g"](0.0, P, B) == pytest.approx(0.0)

    def test_f_uno_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_log_g"](1.0, P, B)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_log_g"](FSTAR, 0.0, B)


class TestPmf:
    def test_somma_uno(self):
        s = sum(_F["mh366_pmf"](k, N, P) for k in range(N + 1))
        assert s == pytest.approx(1.0)

    def test_moneta(self):
        assert _F["mh366_pmf"](0, 1, 0.5) == pytest.approx(0.5)
        assert _F["mh366_pmf"](1, 1, 0.5) == pytest.approx(0.5)

    def test_k_maggiore_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_pmf"](N + 1, N, P)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_pmf"](0, 0, P)


class TestProb:
    def test_demo_raddoppio(self):
        assert _F["mh366_p_raddoppio"](FSTAR, P, B, N) == pytest.approx(PRADD)

    def test_demo_dimezzamento(self):
        assert _F["mh366_p_dimezzamento"](FSTAR, P, B, N) == pytest.approx(PDIM)

    def test_fstar_massimizza_crescita(self):
        # f* e' il massimizzatore di g: la proprieta' che definisce Kelly
        g_full = _F["mh366_log_g"](FSTAR, P, B)
        g_half = _F["mh366_log_g"](FSTAR / 2.0, P, B)
        assert g_half < g_full

    def test_frazionario_riduce_coda_sinistra(self):
        # la mezza Kelly taglia la coda sinistra (P dimezzamento)
        pd_full = _F["mh366_p_dimezzamento"](FSTAR, P, B, N)
        pd_half = _F["mh366_p_dimezzamento"](FSTAR / 2.0, P, B, N)
        assert pd_half < pd_full

    def test_raddoppio_non_monotono_in_f(self):
        # Con f dimezzata le perdite pesano meno: la soglia k per il
        # raddoppio scende e P(raddoppio) puo' SALIRE (demo: 95.8% > 90.7%)
        pr_full = _F["mh366_p_raddoppio"](FSTAR, P, B, N)
        pr_half = _F["mh366_p_raddoppio"](FSTAR / 2.0, P, B, N)
        assert pr_half > pr_full

    def test_somma_code_minore_uno(self):
        assert (_F["mh366_p_raddoppio"](FSTAR, P, B, N)
                + _F["mh366_p_dimezzamento"](FSTAR, P, B, N)) < 1.0

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_p_raddoppio"](FSTAR, P, B, 0)


class TestQuantili:
    def test_demo_chiavi(self):
        q = _F["mh366_quantili"](FSTAR, P, B, N)
        assert sorted(q.keys()) == [0.05, 0.25, 0.5, 0.75, 0.95]

    def test_monotonia(self):
        q = _F["mh366_quantili"](FSTAR, P, B, N)
        vs = [q[k] for k in sorted(q)]
        assert all(a < b for a, b in zip(vs, vs[1:]))

    def test_mediana(self):
        q = _F["mh366_quantili"](FSTAR, P, B, N)
        assert q[0.5] == pytest.approx(Q50)
        assert q[0.5] == pytest.approx(MULT, rel=0.02)

    def test_q_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_quantili"](FSTAR, P, B, N, qs=(0.5, 1.5))


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh366_verdetto"](0.0, 0.0, 0.0).startswith("NESSUN EDGE")

    def test_solida(self):
        assert _F["mh366_verdetto"](0.90, 0.04, 0.04).startswith(
            "CRESCITA SOLIDA")

    def test_probabile(self):
        assert _F["mh366_verdetto"](0.60, 0.10, 0.03).startswith(
            "CRESCITA PROBABILE")

    def test_incerta(self):
        assert _F["mh366_verdetto"](0.30, 0.20, 0.02).startswith(
            "CRESCITA INCERTA")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_verdetto"](1.5, 0.0, 0.01)


class TestAnalisi:
    def _demo(self):
        return _F["mh366_analisi"](P, B, N)

    def test_demo(self):
        a = self._demo()
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["g"] == pytest.approx(G)
        assert a["log_atteso"] == pytest.approx(LOGATT)
        assert a["moltiplicatore_geometrico"] == pytest.approx(MULT)
        assert a["p_raddoppio"] == pytest.approx(PRADD)
        assert a["p_dimezzamento"] == pytest.approx(PDIM)
        assert a["quantili"][0.5] == pytest.approx(Q50)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("CRESCITA SOLIDA")

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["p_raddoppio"] == a2["p_raddoppio"]

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_analisi"](P, 0.0, N)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_analisi"](1.5, B, N)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh366_analisi"](P, B, 0)
