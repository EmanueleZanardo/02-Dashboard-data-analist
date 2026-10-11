
"""Test tab341 '📐 K-ratio: la regolarità della crescita dell'equity': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del K-ratio di Zephyr: validatori,
parse della serie di rendimenti %, equity curve, misure OLS (slope, SE, k =
slope*sqrt(n_punti)/SE, None se SE ~ 0) e verdetto a 4 stati (ECCELLENTE /
BUONO / MODERATO / DEBOLE + NON MISURABILE; SE ~ 0 -> ECCELLENTE per
regolarita' perfetta).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh341_num", "mh341_parse_serie", "mh341_equity",
           "mh341_misure", "mh341_verdetto")

TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
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
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
SERIE_DEMO = '1.2\n0.8\n1.5\n-0.6\n0.9\n1.1\n-4.8\n-2.5\n1.6\n0.7\n-0.9\n1.3\n0.8\n1.0\n1.4\n-1.2\n0.6\n0.9\n1.7\n-0.5\n1.1\n0.4\n-0.7\n1.2\n0.9\n0.5\n1.6\n-1.4\n0.8\n1.0\n0.6\n1.3\n-0.8\n0.9\n0.7\n1.2'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
N_PUNTI = 37
SLOPE = 0.38674799099978485
SE = 2.251689797436529
K = 1.0447692177669587
STATO = "K-ratio BUONO"
VERDETTO = "K-ratio BUONO (1.04): crescita costante con scarti contenuti dal trend: sizing sereno. L'equity cresce di +0.39 punti per periodo con un rumore di 2.25 punti attorno al trend (36 periodi)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return _F["mh341_parse_serie"](SERIE_DEMO, "strategia")


class TestRegistry341:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 374
        assert "tab341" in dvars
        assert "tab341" in withs

    def test_titoli_allineati_338_339_340_341(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab338")] == TITLE338
        assert titoli[dvars.index("tab339")] == TITLE339
        assert titoli[dvars.index("tab340")] == TITLE340
        assert titoli[dvars.index("tab341")] == TITLE341

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab374"
        assert titoli[-1] == TITLE374
        assert withs[-1] == "tab374"


class TestNum:
    def test_num_ok(self):
        assert _F["mh341_num"](1.5, "x") == 1.5
        assert _F["mh341_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh341_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh341_parse_serie"](SERIE_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.2)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh341_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh341_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh341_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh341_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestEquity:
    def test_equity_base(self):
        eq = _F["mh341_equity"](_demo())
        assert eq[0] == pytest.approx(100.0)
        assert len(eq) == N_PER + 1 == N_PUNTI

    def test_equity_compound(self):
        eq = _F["mh341_equity"](np.array([10.0, -10.0]))
        assert eq[1] == pytest.approx(110.0)
        assert eq[2] == pytest.approx(99.0)


class TestMisure:
    def test_demo(self):
        r = _demo()
        m = _F["mh341_misure"](r)
        assert m["n"] == N_PER == 36
        assert m["n_punti"] == N_PUNTI == 37
        assert m["slope"] == pytest.approx(SLOPE, rel=1e-9)
        assert m["slope"] > 0
        assert m["se"] == pytest.approx(SE, rel=1e-9)
        assert m["se"] > 0
        assert m["k"] == pytest.approx(K, rel=1e-9)
        assert len(m["eq"]) == len(m["trend"]) == N_PUNTI

    def test_relazioni(self):
        r = _demo()
        m = _F["mh341_misure"](r)
        import math
        assert m["k"] == pytest.approx(
            m["slope"] * math.sqrt(m["n_punti"]) / m["se"], rel=1e-9)

    def test_trend_lineare(self):
        r = _demo()
        m = _F["mh341_misure"](r)
        # il trend OLS passa per il baricentro: media(trend) == media(eq)
        assert np.mean(m["trend"]) == pytest.approx(np.mean(m["eq"]),
                                                    rel=1e-9)

    def test_equity_retta_se_piccolo(self):
        # equity esattamente su una retta: residui ~ 0
        n = 36
        eq = 100.0 + 0.5 * np.arange(n + 1)
        r = 100.0 * (eq[1:] / eq[:-1] - 1.0)
        m = _F["mh341_misure"](r)
        assert m["se"] < 1e-6

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh341_misure"](np.ones(11))


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh341_verdetto"](1.8, 0.5, 0.3, 36)
        assert v.startswith("K-ratio ECCELLENTE")

    def test_verdetto_soglia_15(self):
        v = _F["mh341_verdetto"](1.5, 0.5, 0.3, 36)
        assert v.startswith("K-ratio ECCELLENTE")

    def test_verdetto_buono(self):
        v = _F["mh341_verdetto"](1.0, 0.4, 0.4, 36)
        assert v.startswith("K-ratio BUONO")

    def test_verdetto_soglia_075(self):
        v = _F["mh341_verdetto"](0.75, 0.4, 0.4, 36)
        assert v.startswith("K-ratio BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh341_verdetto"](0.3, 0.2, 0.6, 36)
        assert v.startswith("K-ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh341_verdetto"](-0.4, -0.1, 0.5, 36)
        assert v.startswith("K-ratio DEBOLE")

    def test_verdetto_retta(self):
        v = _F["mh341_verdetto"](None, 0.5, 0.0, 36)
        assert v.startswith("K-ratio ECCELLENTE")
        assert "regolarit" in v

    def test_verdetto_non_misurabile(self):
        v = _F["mh341_verdetto"](None, None, 0.3, 36)
        assert v.startswith("K-ratio NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh341_verdetto"](K, SLOPE, SE, N_PER)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh341_verdetto"]("x", 0.4, 0.4, 36)
