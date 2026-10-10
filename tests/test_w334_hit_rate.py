"""Test tab334 '🎯 Hit rate: quanto spesso la strategia batte il benchmark?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della hit rate: validatori,
parse delle due serie di rendimenti %, statistiche (n_win/n_loss/n_flat,
hit %, avg win/loss in punti %, win/loss, atteso attivo medio, streak
max vinti/persi) e verdetto a 4 stati
(ECCELLENTE / SCOMMESSA / DIFENSIVA / DEBOLE + NON MISURABILE).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh334_num", "mh334_parse_serie", "mh334_statistiche",
           "mh334_verdetto")

TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
SERIE_ST_DEMO = '0.9\n-1.7\n2.9\n0.5\n-0.2\n2.3\n-1.6\n2.8\n-1.1\n0.2\n2.7\n-0.4\n0.0\n0.5\n1.7\n1.7\n-0.7\n-0.5\n1.2\n2.3\n2.4\n-1.0\n2.3\n-1.6\n2.1\n0.4\n-0.5\n2.8\n-1.6\n1.4\n2.5\n-2.0\n2.8\n0.2\n0.3\n-1.3'
SERIE_BM_DEMO = '1.5\n-0.8\n2.1\n0.9\n-1.4\n1.8\n-0.5\n1.2\n-2.0\n0.7\n1.6\n-1.1\n0.8\n-0.9\n2.4\n1.1\n-1.7\n0.5\n-0.6\n1.9\n2.8\n-2.3\n1.4\n-0.7\n0.6\n1.0\n-1.2\n1.7\n-0.4\n0.9\n1.3\n-1.5\n2.0\n-0.8\n1.1\n-1.9'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
N_WIN = 22
N_LOSS = 14
N_FLAT = 0
HIT = 61.111111111111114
AVG_WIN = 0.9818181818181819
AVG_LOSS = -0.742857142857143
WL = 1.3216783216783217
EXP_ACT = 0.31111111111111106
STR_WIN = 2
STR_LOSS = 2
STATO = "hit rate ECCELLENTE"
VERDETTO = "hit rate ECCELLENTE (hit 61.1% / win-loss 1.32): la strategia batte il benchmark piu' spesso della meta' delle volte e quando lo batte guadagna in media piu' di quanto perde quando lo manca. Outperformance frequente e sostenibile: il profilo ideale per una strategia di fixing/hedging."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh334_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh334_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry334:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 349
        assert "tab334" in dvars
        assert "tab334" in withs

    def test_titoli_allineati_331_332_333_334(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab331")] == TITLE331
        assert titoli[dvars.index("tab332")] == TITLE332
        assert titoli[dvars.index("tab333")] == TITLE333
        assert titoli[dvars.index("tab334")] == TITLE334

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab349"
        assert titoli[-1] == TITLE349
        assert withs[-1] == "tab349"


class TestNum:
    def test_num_ok(self):
        assert _F["mh334_num"](1.5, "x") == 1.5
        assert _F["mh334_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh334_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh334_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(0.9)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh334_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh334_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh334_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh334_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestStatistiche:
    def test_demo(self):
        rs, rb = _demo()
        s = _F["mh334_statistiche"](rs, rb)
        assert s["n"] == N_PER
        assert s["n_win"] == N_WIN == 22
        assert s["n_loss"] == N_LOSS == 14
        assert s["n_flat"] == N_FLAT == 0
        assert s["hit"] == pytest.approx(HIT, rel=1e-9)
        assert s["avg_win"] == pytest.approx(AVG_WIN, rel=1e-9)
        assert s["avg_loss"] == pytest.approx(AVG_LOSS, rel=1e-9)
        assert s["win_loss"] == pytest.approx(WL, rel=1e-9)
        assert s["exp_active"] == pytest.approx(EXP_ACT, rel=1e-9)
        assert s["streak_win"] == STR_WIN == 2
        assert s["streak_loss"] == STR_LOSS == 2

    def test_coerenti(self):
        rs, rb = _demo()
        s = _F["mh334_statistiche"](rs, rb)
        assert s["hit"] == pytest.approx(s["n_win"] / s["n"] * 100.0, rel=1e-9)
        assert s["win_loss"] == pytest.approx(
            s["avg_win"] / abs(s["avg_loss"]), rel=1e-9)
        assert s["n_win"] + s["n_loss"] + s["n_flat"] == s["n"]
        assert s["exp_active"] == pytest.approx(
            (rs - rb).mean(), rel=1e-9)

    def test_tutti_vinti(self):
        rs = np.array([2.0] * 36)
        rb = np.array([1.0] * 36)
        s = _F["mh334_statistiche"](rs, rb)
        assert s["n_win"] == 36
        assert s["n_loss"] == 0
        assert s["avg_loss"] is None
        assert s["win_loss"] is None

    def test_tutti_persi(self):
        rs = np.array([0.5] * 36)
        rb = np.array([1.0] * 36)
        s = _F["mh334_statistiche"](rs, rb)
        assert s["n_win"] == 0
        assert s["n_loss"] == 36
        assert s["avg_win"] is None
        assert s["win_loss"] is None

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh334_statistiche"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh334_statistiche"](np.ones(11), np.ones(11))


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh334_verdetto"](61.1, 1.32)
        assert v.startswith("hit rate ECCELLENTE")

    def test_verdetto_scommessa(self):
        v = _F["mh334_verdetto"](40.0, 2.0)
        assert v.startswith("hit rate SCOMMESSA")

    def test_verdetto_soglia_50(self):
        v = _F["mh334_verdetto"](50.0, 1.0)
        assert v.startswith("hit rate ECCELLENTE")

    def test_verdetto_difensiva(self):
        v = _F["mh334_verdetto"](60.0, 0.8)
        assert v.startswith("hit rate DIFENSIVA")

    def test_verdetto_debole(self):
        v = _F["mh334_verdetto"](40.0, 0.8)
        assert v.startswith("hit rate DEBOLE")

    def test_verdetto_none(self):
        v = _F["mh334_verdetto"](None, 1.32)
        assert v.startswith("hit rate NON MISURABILE")
        v2 = _F["mh334_verdetto"](61.1, None)
        assert v2.startswith("hit rate NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh334_verdetto"](HIT, WL)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh334_verdetto"]("x", 1.0)
