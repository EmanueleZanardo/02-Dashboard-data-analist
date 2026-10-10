"""Test tab349 'Frazione di Kelly: half-Kelly e trade-off crescita/volatilità': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh349_num", "mh349_kelly_f", "mh349_logstats",
           "mh349_dd_prob", "mh349_verdetto", "mh349_confronto")

TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
P = 0.55
WIN = 120.0
LOSS = 100.0
LAM = 0.5
D = 0.2
B = 1.2
FSTAR = 0.17500000000000007
G_FULL = 0.018273846093402088
SIGMA_FULL = 0.19053623975199743
RATIO_FULL = 0.09590745633055099
G_HALF = 0.013709697146873145
QUOTA_HALF = 0.7502359972169809
SIGMA_HALF = 0.09522653057877176
PDD_HALF = 0.5092968758565635
PDD_FULL = 0.7988028982533437
G_SCELTA = 0.013709697146873145
SIGMA_SCELTA = 0.09522653057877176
RATIO_SCELTA = 0.1439693020794497
PDD_SCELTA = 0.5092968758565635
F_SCELTA = 0.08750000000000004
VERDETTO = "HALF-KELLY: con λ=0.50 ottieni il 75% della crescita massima (+1.371%/trade) con solo il 50% della volatilita' del full Kelly (9.52% vs 19.05%/trade); P(drawdown ≥ 20%) scende da 80% a 51%. Il full Kelly massimizza la crescita ma alza molto il rischio di drawdown."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry349:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 357
        assert "tab349" in dvars
        assert "tab349" in withs

    def test_titoli_allineati_346_347_348_349(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab346")] == TITLE346
        assert titoli[dvars.index("tab347")] == TITLE347
        assert titoli[dvars.index("tab348")] == TITLE348
        assert titoli[dvars.index("tab349")] == TITLE349

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab357"
        assert titoli[-1] == TITLE357
        assert withs[-1] == "tab357"


class TestNum:
    def test_num_ok(self):
        assert _F["mh349_num"](1.5, "x") == 1.5
        assert _F["mh349_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh349_num"](bad, "x")


class TestKellyF:
    def test_demo_formula(self):
        att = (P * B - (1.0 - P)) / B
        assert _F["mh349_kelly_f"](P, B) == pytest.approx(att, rel=1e-12)
        assert FSTAR == pytest.approx(att, rel=1e-12)
        assert FSTAR == pytest.approx(0.175, rel=1e-12)

    def test_senza_edge(self):
        assert _F["mh349_kelly_f"](0.40, 1.2) == 0.0
        assert _F["mh349_kelly_f"](0.50, 1.0) == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh349_kelly_f"](0.0, B)
        with pytest.raises(ValueError):
            _F["mh349_kelly_f"](1.0, B)
        with pytest.raises(ValueError):
            _F["mh349_kelly_f"](P, 0.0)


class TestLogstats:
    def test_demo_g_formula(self):
        att = (P * math.log(1.0 + FSTAR * B)
               + (1.0 - P) * math.log(1.0 - FSTAR))
        assert _F["mh349_logstats"](P, B, FSTAR)["g"] == pytest.approx(
            att, rel=1e-12)
        assert G_FULL == pytest.approx(att, rel=1e-12)

    def test_demo_sigma_formula(self):
        x1 = math.log(1.0 + FSTAR * B)
        x2 = math.log(1.0 - FSTAR)
        var = P * x1 * x1 + (1.0 - P) * x2 * x2 - G_FULL * G_FULL
        assert _F["mh349_logstats"](P, B, FSTAR)["sigma"] == pytest.approx(
            math.sqrt(var), rel=1e-12)
        assert SIGMA_FULL == pytest.approx(math.sqrt(var), rel=1e-12)

    def test_demo_ratio(self):
        s = _F["mh349_logstats"](P, B, FSTAR)
        assert s["ratio"] == pytest.approx(s["g"] / s["sigma"], rel=1e-12)
        assert RATIO_FULL == pytest.approx(s["ratio"], rel=1e-12)

    def test_kelly_massimizza_g(self):
        s = _F["mh349_logstats"]
        assert s(P, B, FSTAR)["g"] >= s(P, B, FSTAR / 2.0)["g"]
        assert s(P, B, FSTAR)["g"] > 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh349_logstats"](P, B, 1.0)
        with pytest.raises(ValueError):
            _F["mh349_logstats"](P, B, -0.1)
        with pytest.raises(ValueError):
            _F["mh349_logstats"](0.0, B, FSTAR)


class TestDdProb:
    def test_demo_formula(self):
        att = math.exp(-2.0 * G_FULL * abs(math.log(1.0 - D))
                       / (SIGMA_FULL ** 2))
        assert _F["mh349_dd_prob"](G_FULL, SIGMA_FULL, D) == pytest.approx(
            att, rel=1e-12)
        assert PDD_FULL == pytest.approx(att, rel=1e-12)
        assert 0.0 < PDD_FULL < 1.0

    def test_senza_crescita_uno(self):
        assert _F["mh349_dd_prob"](-0.01, 0.1, D) == 1.0
        assert _F["mh349_dd_prob"](0.0, 0.0, D) == 1.0

    def test_monotono_in_d(self):
        f = _F["mh349_dd_prob"]
        assert f(G_FULL, SIGMA_FULL, 0.30) < f(G_FULL, SIGMA_FULL, 0.10)

    def test_clip_uno(self):
        assert _F["mh349_dd_prob"](1e-9, 1.0, 0.20) <= 1.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh349_dd_prob"](G_FULL, SIGMA_FULL, 0.0)
        with pytest.raises(ValueError):
            _F["mh349_dd_prob"](G_FULL, SIGMA_FULL, 1.0)
        with pytest.raises(ValueError):
            _F["mh349_dd_prob"](G_FULL, -0.1, D)


class TestVerdetto:
    def test_demo(self):
        assert VERDETTO == _F["mh349_verdetto"](
            FSTAR, G_HALF, QUOTA_HALF, SIGMA_HALF, SIGMA_FULL,
            PDD_HALF, PDD_FULL, D)
        assert VERDETTO.startswith("HALF-KELLY")

    def test_senza_edge(self):
        v = _F["mh349_verdetto"](0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, D)
        assert v.startswith("NESSUN EDGE")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh349_verdetto"](FSTAR, G_HALF, QUOTA_HALF, SIGMA_HALF,
                                 SIGMA_FULL, PDD_HALF, PDD_FULL, 0.0)


class TestConfronto:
    def test_demo(self):
        m = _F["mh349_confronto"](P, WIN, LOSS, LAM, D)
        assert m["b"] == pytest.approx(B, rel=1e-12)
        assert m["f_star"] == pytest.approx(FSTAR, rel=1e-12)
        assert m["f_scelta"] == pytest.approx(F_SCELTA, rel=1e-12)
        assert m["f_scelta"] == pytest.approx(LAM * FSTAR, rel=1e-12)
        assert m["g"] == pytest.approx(G_SCELTA, rel=1e-12)
        assert m["sigma"] == pytest.approx(SIGMA_SCELTA, rel=1e-12)
        assert m["ratio"] == pytest.approx(RATIO_SCELTA, rel=1e-12)
        assert m["p_dd"] == pytest.approx(PDD_SCELTA, rel=1e-12)
        assert m["g_full"] == pytest.approx(G_FULL, rel=1e-12)
        assert m["sigma_full"] == pytest.approx(SIGMA_FULL, rel=1e-12)
        assert m["verdetto"] == VERDETTO

    def test_righe_lambda(self):
        m = _F["mh349_confronto"](P, WIN, LOSS, LAM, D)
        righe = m["righe"]
        assert [r["lambda"] for r in righe] == [0.25, 0.5, 0.75, 1.0, 1.5]
        assert righe[3]["g"] == pytest.approx(G_FULL, rel=1e-12)
        assert righe[3]["quota_crescita"] == pytest.approx(1.0, rel=1e-12)
        assert righe[1]["g"] == pytest.approx(G_HALF, rel=1e-12)
        assert righe[1]["quota_crescita"] == pytest.approx(
            QUOTA_HALF, rel=1e-12)
        assert righe[1]["sigma"] == pytest.approx(SIGMA_HALF, rel=1e-12)
        assert righe[1]["p_dd"] == pytest.approx(PDD_HALF, rel=1e-12)

    def test_pdd_monotono_in_lambda(self):
        m = _F["mh349_confronto"](P, WIN, LOSS, LAM, D)
        pdds = [r["p_dd"] for r in m["righe"]]
        assert all(a <= b for a, b in zip(pdds, pdds[1:]))

    def test_senza_edge(self):
        m = _F["mh349_confronto"](0.40, WIN, LOSS, LAM, D)
        assert m["f_star"] == 0.0
        assert m["g"] == 0.0
        assert m["verdetto"].startswith("NESSUN EDGE")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh349_confronto"](0.0, WIN, LOSS, LAM, D)
        with pytest.raises(ValueError):
            _F["mh349_confronto"](P, 0.0, LOSS, LAM, D)
        with pytest.raises(ValueError):
            _F["mh349_confronto"](P, WIN, LOSS, 0.0, D)
        with pytest.raises(ValueError):
            _F["mh349_confronto"](P, WIN, LOSS, 2.5, D)
        with pytest.raises(ValueError):
            _F["mh349_confronto"](P, WIN, LOSS, LAM, 1.0)

