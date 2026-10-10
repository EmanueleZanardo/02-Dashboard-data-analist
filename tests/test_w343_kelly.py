
"""Test tab343 '📐 Kelly criterion: il sizing ottimale dall'edge stimato': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del criterio di Kelly: validatori,
frazione f* = (p*(b+1)-1)/b, curva di crescita geometrica
g(f) = p*ln(1+f*b) + q*ln(1-f) (None se f >= 1), misure (b, f*, half/quarter
Kelly, EV per operazione) e verdetto a 3 stati (NESSUN EDGE / EDGE POSITIVO /
EDGE ECCESSIVO).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh343_num", "mh343_kelly", "mh343_growth", "mh343_misure",
           "mh343_verdetto")

TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
B = 1.2
F_STAR = 0.17500000000000016
F_HALF = 0.08750000000000008
F_QUARTER = 0.04375000000000004
EV = 21.000000000000007
VERDETTO = 'KELLY EDGE POSITIVO (f* = 17.50%): aspettativa +21.00 per operazione: taglia prudente half-Kelly = 8.75% del capitale: massimizza la crescita geometrica g(f) lasciando margine di errore sulla stima di p e b.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry343:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 360
        assert "tab343" in dvars
        assert "tab343" in withs

    def test_titoli_allineati_340_341_342_343(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab340")] == TITLE340
        assert titoli[dvars.index("tab341")] == TITLE341
        assert titoli[dvars.index("tab342")] == TITLE342
        assert titoli[dvars.index("tab343")] == TITLE343

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab360"
        assert titoli[-1] == TITLE360
        assert withs[-1] == "tab360"


class TestNum:
    def test_num_ok(self):
        assert _F["mh343_num"](1.5, "x") == 1.5
        assert _F["mh343_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh343_num"](bad, "x")


class TestKelly:
    def test_demo(self):
        f = _F["mh343_kelly"](P, B)
        assert f == pytest.approx(F_STAR, rel=1e-9)
        assert f == pytest.approx(0.175, rel=1e-9)

    def test_formula(self):
        assert _F["mh343_kelly"](0.6, 2.0) == pytest.approx(
            (0.6 * 3.0 - 1.0) / 2.0, rel=1e-9)

    def test_zero_edge(self):
        # p=0.5, b=1: f* = 0, nessun edge
        assert _F["mh343_kelly"](0.5, 1.0) == pytest.approx(0.0, abs=1e-12)

    def test_negativo(self):
        assert _F["mh343_kelly"](0.4, 1.0) < 0.0

    def test_ko_p_bordi(self):
        for p in (0.0, 1.0, -0.1, 1.5):
            with pytest.raises(ValueError):
                _F["mh343_kelly"](p, 1.2)

    def test_ko_b(self):
        for b in (0.0, -1.0):
            with pytest.raises(ValueError):
                _F["mh343_kelly"](0.55, b)


class TestGrowth:
    def test_demo(self):
        g = _F["mh343_growth"](F_STAR, P, B)
        assert g is not None and g > 0.0

    def test_zero(self):
        assert _F["mh343_growth"](0.0, P, B) == pytest.approx(0.0, abs=1e-12)

    def test_none_oltre_uno(self):
        assert _F["mh343_growth"](1.0, P, B) is None
        assert _F["mh343_growth"](1.5, P, B) is None

    def test_picco_a_fstar(self):
        g0 = _F["mh343_growth"](F_STAR * 0.5, P, B)
        g1 = _F["mh343_growth"](F_STAR, P, B)
        g2 = _F["mh343_growth"](F_STAR * 1.5, P, B)
        assert g1 > g0 and g1 > g2

    def test_formula(self):
        p, b, f = 0.6, 2.0, 0.1
        q = 1.0 - p
        assert _F["mh343_growth"](f, p, b) == pytest.approx(
            p * math.log(1.0 + f * b) + q * math.log(1.0 - f), rel=1e-9)

    def test_ko_f_negativa(self):
        with pytest.raises(ValueError):
            _F["mh343_growth"](-0.1, P, B)

    def test_ko_p_bordi(self):
        with pytest.raises(ValueError):
            _F["mh343_growth"](0.1, 1.0, B)


class TestMisure:
    def _m(self):
        return _F["mh343_misure"](P, WIN, LOSS)

    def test_demo(self):
        m = self._m()
        assert m["p"] == pytest.approx(P)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f_star"] == pytest.approx(F_STAR, rel=1e-9)
        assert m["f_half"] == pytest.approx(F_HALF, rel=1e-9)
        assert m["f_quarter"] == pytest.approx(F_QUARTER, rel=1e-9)
        assert m["ev"] == pytest.approx(EV, rel=1e-9) == pytest.approx(21.0)
        assert m["f_half"] == pytest.approx(m["f_star"] / 2.0, rel=1e-9)

    def test_relazioni(self):
        m = self._m()
        assert m["b"] == pytest.approx(m["win"] / m["loss"], rel=1e-9)
        assert m["ev"] == pytest.approx(
            m["p"] * m["win"] - (1.0 - m["p"]) * m["loss"], rel=1e-9)

    def test_ko_win_loss(self):
        with pytest.raises(ValueError):
            _F["mh343_misure"](P, 0.0, LOSS)
        with pytest.raises(ValueError):
            _F["mh343_misure"](P, WIN, -1.0)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh343_misure"](1.0, WIN, LOSS)


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh343_verdetto"](-0.05, 0.4, 1.0, -5.0)
        assert v.startswith("KELLY NESSUN EDGE")

    def test_nessun_edge_zero(self):
        v = _F["mh343_verdetto"](0.0, 0.5, 1.0, 0.0)
        assert v.startswith("KELLY NESSUN EDGE")

    def test_positivo(self):
        v = _F["mh343_verdetto"](0.175, 0.55, 1.2, 21.0)
        assert v.startswith("KELLY EDGE POSITIVO")
        assert "8.75%" in v

    def test_eccessivo(self):
        v = _F["mh343_verdetto"](1.5, 0.9, 5.0, 100.0)
        assert v.startswith("KELLY EDGE ECCESSIVO")

    def test_verdetto_demo(self):
        v = _F["mh343_verdetto"](F_STAR, P, B, EV)
        assert v == VERDETTO
        assert v.startswith("KELLY EDGE POSITIVO")

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh343_verdetto"]("x", P, B, EV)
