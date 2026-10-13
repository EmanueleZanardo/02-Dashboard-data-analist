"""Test tab410 '⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh410_num", "mh410_parse_serie", "mh410_gain_pain",
           "mh410_verdetto", "mh410_mappa")

TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
DEMO = '3.2\n1.8\n-1.2\n2.5\n4.1\n-2.8\n0.9\n2.2\n-0.9\n3.0\n1.5\n-1.5\n5.2\n2.8\n1.1\n-3.1\n0.7\n3.6\n-0.6\n2.0\n1.4\n-1.9\n2.6\n0.8\n-1.1\n3.3\n1.7\n-2.2\n2.9\n0.5\n1.9\n-1.4\n2.4\n3.1\n-0.8\n1.6'
SOMMA = 39.3
PERDITE = 17.5
GUADAGNI = 56.8
GTP = 2.2457142857142856
N_DOWN = 11
N_UP = 25
MEDIA = 1.0916666666666666
MAXDOWN = -3.1


class TestRegistry410:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 420
        assert "tab410" in dvars
        assert "tab410" in withs

    def test_titoli_allineati_405_406_407_408_409_410(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab420"
        assert titoli[-1] == TITLE420
        assert withs[-1] == "tab420"


class TestGainPain410:
    def _xs(self):
        return _F["mh410_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh410_mappa"](xs)
        assert abs(m["somma"] - SOMMA) < 1e-12
        assert abs(m["perdite"] - PERDITE) < 1e-12
        assert abs(m["guadagni"] - GUADAGNI) < 1e-12
        assert abs(m["gain_pain"] - GTP) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert abs(m["max_down"] - MAXDOWN) < 1e-9
        assert m["n_per"] == 36
        assert m["n_down"] == N_DOWN
        assert m["n_up"] == N_UP
        assert m["verdetto"].startswith("ECCELLENTE")

    def test_gain_pain_definizione(self):
        # gtp = somma / |somma negativi|, calcolato a mano
        xs = list(self._xs())
        somma = sum(xs)
        perdite = -sum(v for v in xs if v < 0.0)
        assert abs(somma - SOMMA) < 1e-9
        assert abs(perdite - PERDITE) < 1e-9
        assert abs(_F["mh410_gain_pain"](tuple(xs))
                   - somma / perdite) < 1e-12
        assert abs(min(xs) - MAXDOWN) < 1e-9

    def test_casi_degeneri(self):
        F = _F
        assert F["mh410_gain_pain"](tuple([1.0] * 25)) == math.inf
        assert F["mh410_gain_pain"](tuple([0.0] * 25)) == 0.0
        assert F["mh410_gain_pain"](tuple([-1.0] * 25)) < 0.0
        assert F["mh410_gain_pain"](
            tuple([2.0] * 20 + [-1.0] * 5)) == (2.0 * 20 - 5.0) / 5.0
        assert F["mh410_verdetto"](math.inf).startswith("NESSUNA PERDITA")
        assert F["mh410_verdetto"](2.5).startswith("ECCELLENTE")
        assert F["mh410_verdetto"](2.0).startswith("ECCELLENTE")
        assert F["mh410_verdetto"](1.7).startswith("BUONO")
        assert F["mh410_verdetto"](1.2).startswith("ACCETTABILE")
        assert F["mh410_verdetto"](0.8).startswith("DEBOLE")
        assert F["mh410_verdetto"](0.3).startswith("SCARSO")
        assert F["mh410_verdetto"](-1.0).startswith("SCARSO")

    def test_validatori(self):
        F = _F
        for _bad in (lambda: F["mh410_gain_pain"](None),
                     lambda: F["mh410_gain_pain"]((1.0,) * 19),
                     lambda: F["mh410_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: F["mh410_parse_serie"](
                         "\n".join(["1.0"] * 19 + ["xx"])),
                     lambda: F["mh410_num"](True, "x"),
                     lambda: F["mh410_num"](float("nan"), "x"),
                     lambda: F["mh410_mappa"]((1.0,) * 19),
                     lambda: F["mh410_mappa"](None)):
            try:
                _bad()
                raise AssertionError("caso degenere non rilevato")
            except ValueError:
                pass

    def test_coerenza_mappa_gain_pain(self):
        # mappa e gain_pain devono concordare su serie arbitrarie
        xs = tuple([round(3.0 * ((-1) ** i) * (1 + i % 4), 2)
                    for i in range(25)])
        m = _F["mh410_mappa"](xs)
        assert abs(m["gain_pain"] - _F["mh410_gain_pain"](xs)) < 1e-12
        assert m["n_down"] + m["n_up"] <= m["n_per"]
        assert abs(m["guadagni"] - m["perdite"] - m["somma"]) < 1e-9
