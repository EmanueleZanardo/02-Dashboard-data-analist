"""Test tab350 'Kelly robusto: sizing con edge incerta': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh350_num", "mh350_kelly_f", "mh350_logstats",
           "mh350_lambda_max", "mh350_verdetto", "mh350_robusto")

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
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
P = 0.55
E = 0.05
WIN = 120.0
LOSS = 100.0
LAM = 0.5
B = 1.2
FSTAR = 0.17500000000000007
F_LO = 0.08333333333333331
F_SCELTA = 0.08750000000000004
G_LO = 0.004139070722112809
SIGMA_LO = 0.09570626424760331
G_MID = 0.013709697146873145
SIGMA_MID = 0.09522653057877176
RATIO_MID = 0.1439693020794497
LAM_MAX = 0.952
VERDETTO = 'ROBUSTO — con λ = 0.50 la size f = 8.75% cresce anche nel worst case p-e = 50% (+0.414%/trade); λ_max ≈ 0.95: oltre quella frazione la crescita nel worst case diventa negativa.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry350:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 375
        assert "tab350" in dvars
        assert "tab350" in withs

    def test_titoli_allineati_347_348_349_350(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab347")] == TITLE347
        assert titoli[dvars.index("tab348")] == TITLE348
        assert titoli[dvars.index("tab349")] == TITLE349
        assert titoli[dvars.index("tab350")] == TITLE350

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab375"
        assert titoli[-1] == TITLE375
        assert withs[-1] == "tab375"


class TestNum:
    def test_num_ok(self):
        assert _F["mh350_num"](1.5, "x") == 1.5
        assert _F["mh350_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh350_num"](bad, "x")


class TestKellyF:
    def test_demo_formula(self):
        att = (P * B - (1.0 - P)) / B
        assert _F["mh350_kelly_f"](P, B) == pytest.approx(att, rel=1e-12)
        assert FSTAR == pytest.approx(att, rel=1e-12)
        assert FSTAR == pytest.approx(0.175, rel=1e-12)

    def test_demo_worst(self):
        att = ((P - E) * B - (1.0 - (P - E))) / B
        assert _F["mh350_kelly_f"](P - E, B) == pytest.approx(att, rel=1e-12)
        assert F_LO == pytest.approx(att, rel=1e-12)
        assert F_LO == pytest.approx(0.08333333333333333, rel=1e-9)

    def test_senza_edge(self):
        assert _F["mh350_kelly_f"](0.40, 1.2) == 0.0
        assert _F["mh350_kelly_f"](0.50, 1.0) == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh350_kelly_f"](0.0, B)
        with pytest.raises(ValueError):
            _F["mh350_kelly_f"](1.0, B)
        with pytest.raises(ValueError):
            _F["mh350_kelly_f"](P, 0.0)


class TestLogstats:
    def test_demo_g_worst_formula(self):
        att = ((P - E) * math.log(1.0 + F_SCELTA * B)
               + (1.0 - (P - E)) * math.log(1.0 - F_SCELTA))
        assert _F["mh350_logstats"](P - E, B, F_SCELTA)["g"] == pytest.approx(
            att, rel=1e-12)
        assert G_LO == pytest.approx(att, rel=1e-12)
        assert G_LO > 0.0

    def test_demo_sigma_mid(self):
        x1 = math.log(1.0 + F_SCELTA * B)
        x2 = math.log(1.0 - F_SCELTA)
        var = P * x1 * x1 + (1.0 - P) * x2 * x2 - G_MID * G_MID
        assert _F["mh350_logstats"](P, B, F_SCELTA)["sigma"] == pytest.approx(
            math.sqrt(var), rel=1e-12)
        assert SIGMA_MID == pytest.approx(math.sqrt(var), rel=1e-12)

    def test_demo_ratio_mid(self):
        s = _F["mh350_logstats"](P, B, F_SCELTA)
        assert s["ratio"] == pytest.approx(s["g"] / s["sigma"], rel=1e-12)
        assert RATIO_MID == pytest.approx(s["ratio"], rel=1e-12)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh350_logstats"](P, B, 1.0)
        with pytest.raises(ValueError):
            _F["mh350_logstats"](P, B, -0.1)
        with pytest.raises(ValueError):
            _F["mh350_logstats"](0.0, B, F_SCELTA)


class TestLambdaMax:
    def test_demo_valore(self):
        assert LAM_MAX == pytest.approx(0.952381, rel=1e-2)

    def test_demo_proprieta_soglia(self):
        s = _F["mh350_logstats"]
        assert s(P - E, B, LAM_MAX * FSTAR)["g"] >= 0.0
        assert s(P - E, B, (LAM_MAX + 0.002) * FSTAR)["g"] < 0.0

    def test_demo_monotona(self):
        s = _F["mh350_logstats"]
        assert s(P - E, B, 0.10 * FSTAR)["g"] > 0.0
        assert s(P - E, B, 1.90 * FSTAR)["g"] < 0.0

    def test_zero_senza_fhat(self):
        assert _F["mh350_lambda_max"](0.0, P - E, B) == 0.0

    def test_zero_senza_edge_worst(self):
        assert _F["mh350_lambda_max"](0.10, 0.45, 1.2) == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh350_lambda_max"](FSTAR, 0.0, B)
        with pytest.raises(ValueError):
            _F["mh350_lambda_max"](FSTAR, 1.0, B)
        with pytest.raises(ValueError):
            _F["mh350_lambda_max"](FSTAR, P - E, 0.0)


class TestVerdetto:
    def test_demo_robusto(self):
        assert VERDETTO == _F["mh350_verdetto"](
            FSTAR, F_LO, LAM_MAX, LAM, G_LO, P - E)
        assert VERDETTO.startswith("ROBUSTO")

    def test_overbet(self):
        v = _F["mh350_verdetto"](FSTAR, F_LO, LAM_MAX, 1.5, -0.01, P - E)
        assert v.startswith("OVERBET")

    def test_edge_fragile(self):
        v = _F["mh350_verdetto"](0.05, 0.0, 0.0, LAM, 0.0, 0.45)
        assert v.startswith("EDGE FRAGILE")

    def test_nessun_edge(self):
        v = _F["mh350_verdetto"](0.0, 0.0, 0.0, LAM, 0.0, P - E)
        assert v.startswith("NESSUN EDGE")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh350_verdetto"](FSTAR, F_LO, LAM_MAX, 0.0, G_LO, P - E)
        with pytest.raises(ValueError):
            _F["mh350_verdetto"](FSTAR, F_LO, LAM_MAX, LAM, G_LO, 1.0)


class TestRobusto:
    def test_demo(self):
        m = _F["mh350_robusto"](P, E, WIN, LOSS, LAM)
        assert m["b"] == pytest.approx(B, rel=1e-12)
        assert m["f_hat"] == pytest.approx(FSTAR, rel=1e-12)
        assert m["f_lo"] == pytest.approx(F_LO, rel=1e-12)
        assert m["f_scelta"] == pytest.approx(F_SCELTA, rel=1e-12)
        assert m["f_scelta"] == pytest.approx(LAM * FSTAR, rel=1e-12)
        assert m["g_lo"] == pytest.approx(G_LO, rel=1e-12)
        assert m["sigma_lo"] == pytest.approx(SIGMA_LO, rel=1e-12)
        assert m["g"] == pytest.approx(G_MID, rel=1e-12)
        assert m["sigma"] == pytest.approx(SIGMA_MID, rel=1e-12)
        assert m["ratio"] == pytest.approx(RATIO_MID, rel=1e-12)
        assert m["lam_max"] == pytest.approx(LAM_MAX, rel=1e-12)
        assert m["verdetto"] == VERDETTO

    def test_righe_scenari(self):
        m = _F["mh350_robusto"](P, E, WIN, LOSS, LAM)
        righe = m["righe"]
        assert len(righe) == 3
        assert [r["p"] for r in righe] == [P - E, P, P + E]
        assert righe[0]["scenario"].startswith("pessimistico")
        assert righe[1]["scenario"].startswith("centrale")
        assert righe[2]["scenario"].startswith("ottimistico")
        assert righe[1]["f_star"] == pytest.approx(FSTAR, rel=1e-12)
        assert righe[0]["g"] == pytest.approx(G_LO, rel=1e-12)
        assert righe[1]["g"] == pytest.approx(G_MID, rel=1e-12)
        assert righe[2]["g"] > righe[1]["g"] > righe[0]["g"]

    def test_overbet_demo(self):
        m = _F["mh350_robusto"](P, E, WIN, LOSS, 1.5)
        assert m["g_lo"] < 0.0
        assert m["verdetto"].startswith("OVERBET")

    def test_edge_fragile_demo(self):
        m = _F["mh350_robusto"](0.50, 0.05, WIN, LOSS, LAM)
        assert m["f_lo"] == 0.0
        assert m["verdetto"].startswith("EDGE FRAGILE")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh350_robusto"](0.0, E, WIN, LOSS, LAM)
        with pytest.raises(ValueError):
            _F["mh350_robusto"](P, 0.0, WIN, LOSS, LAM)
        with pytest.raises(ValueError):
            _F["mh350_robusto"](0.04, 0.05, WIN, LOSS, LAM)
        with pytest.raises(ValueError):
            _F["mh350_robusto"](0.97, 0.05, WIN, LOSS, LAM)
        with pytest.raises(ValueError):
            _F["mh350_robusto"](P, E, 0.0, LOSS, LAM)
        with pytest.raises(ValueError):
            _F["mh350_robusto"](P, E, WIN, LOSS, 0.0)
        with pytest.raises(ValueError):
            _F["mh350_robusto"](P, E, WIN, LOSS, 2.5)

