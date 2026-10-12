"""Test tab408 '💢 Pain index: il dolore che serve per il rendimento': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh408_num", "mh408_parse_serie", "mh408_equity",
           "mh408_drawdowns", "mh408_pain_index", "mh408_mdd",
           "mh408_picco_valle", "mh408_max_subacqueo",
           "mh408_pain_ratio", "mh408_verdetto", "mh408_mappa")

TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
DEMO = '-1.2\n-1.0\n-0.9\n-0.8\n-0.7\n-0.6\n-0.5\n-0.4\n-0.3\n-0.2\n-0.2\n-0.1\n-0.1\n-0.1\n-0.1\n0.0\n0.1\n0.1\n0.2\n0.2\n0.3\n0.3\n0.4\n0.4\n0.5\n0.5\n0.6\n0.7\n0.8\n0.9\n1.0\n1.2\n1.5\n1.8\n2.2\n2.8'
R_TOT = 9.58663498089436
MDD = 6.971994114740795
PAIN = 4.858164364715195
PR = 1.973303960343953
MEDIA = 0.25833333333333336
MAXSUB = 31


class TestRegistry408:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 411
        assert "tab408" in dvars
        assert "tab408" in withs

    def test_titoli_allineati_403_404_405_406_407_408(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab403")] == TITLE403
        assert titoli[dvars.index("tab404")] == TITLE404
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab411"
        assert titoli[-1] == TITLE411
        assert withs[-1] == "tab411"


class TestPain408:
    def _xs(self):
        return _F["mh408_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh408_mappa"](xs)
        assert abs(m["r_tot"] - R_TOT) < 1e-12
        assert abs(m["mdd"] - MDD) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["pain_ratio"] - PR) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert m["n_per"] == 36
        assert m["max_sub"] == MAXSUB
        assert m["idx_peak"] == 0
        assert m["idx_trough"] == 15
        assert m["verdetto"].startswith("RECUPERO BUONO")

    def test_pain_definizione(self):
        # pain = sqrt(media dei DD^2) calcolato a mano dai drawdown
        xs = list(self._xs())
        eq = _F["mh408_equity"](xs)
        dd = _F["mh408_drawdowns"](eq)
        assert all(d <= 0.0 for d in dd)
        pain = _F["mh408_pain_index"](eq)
        assert abs(pain - math.sqrt(sum(d * d for d in dd)
                                   / len(dd))) < 1e-12
        # equity cross-check via math.prod
        assert abs(eq[-1] - 100.0 * math.prod(1.0 + r / 100.0
                                             for r in xs)) < 1e-9

    def test_mdd_definizione(self):
        # MDD = -min(drawdown); picco prima della valle
        xs = list(self._xs())
        eq = _F["mh408_equity"](xs)
        mdd = _F["mh408_mdd"](eq)
        dd = _F["mh408_drawdowns"](eq)
        assert abs(mdd - (-min(dd))) < 1e-12
        ip, iv = _F["mh408_picco_valle"](eq)
        assert ip <= iv
        assert (ip, iv) == (0, 15)

    def test_pain_monotono_dolore(self):
        # drawdown piu' profondo a parita' di serie -> pain maggiore
        xs = list(self._xs())
        p1 = _F["mh408_pain_index"](_F["mh408_equity"](xs))
        peggio = [-5.0] + xs[1:]
        p2 = _F["mh408_pain_index"](_F["mh408_equity"](tuple(peggio)))
        assert p2 > p1

    def test_max_subacqueo(self):
        xs = list(self._xs())
        eq = _F["mh408_equity"](xs)
        assert _F["mh408_max_subacqueo"](eq) == MAXSUB
        # serie solo positiva -> mai sott'acqua
        assert _F["mh408_max_subacqueo"](
            _F["mh408_equity"](tuple([1.0] * 25))) == 0

    def test_casi_degeneri(self):
        # serie solo positiva senza cali -> pain = 0 -> +inf
        assert _F["mh408_pain_ratio"](tuple([1.0] * 25)) == math.inf
        assert _F["mh408_verdetto"](math.inf).startswith("NESSUN DRAWDOWN")
        # serie piatta a 0 -> 0.0
        assert _F["mh408_pain_ratio"](tuple([0.0] * 25)) == 0.0
        # perdita netta -> PR negativo
        pr = _F["mh408_pain_ratio"](tuple([-1.0] * 25))
        assert pr < 0.0
        assert _F["mh408_verdetto"](pr).startswith("NESSUN RECUPERO")
        # soglie intermedie
        assert _F["mh408_verdetto"](0.5).startswith("RECUPERO DEBOLE")
        assert _F["mh408_verdetto"](1.5).startswith("RECUPERO BUONO")

    def test_verdetto_stati(self):
        assert _F["mh408_verdetto"](3.0).startswith("RECUPERO FORTE")
        assert _F["mh408_verdetto"](2.0).startswith("RECUPERO FORTE")
        assert _F["mh408_verdetto"](1.999).startswith("RECUPERO BUONO")
        assert _F["mh408_verdetto"](1.0).startswith("RECUPERO BUONO")
        assert _F["mh408_verdetto"](0.999).startswith("RECUPERO DEBOLE")
        assert _F["mh408_verdetto"](0.0).startswith("NESSUN RECUPERO")
        assert _F["mh408_verdetto"](-2.0).startswith("NESSUN RECUPERO")
        with pytest.raises(ValueError):
            _F["mh408_verdetto"](True)
        with pytest.raises(ValueError):
            _F["mh408_verdetto"](float("nan"))

    def test_validatori(self):
        for _bad in (lambda: _F["mh408_equity"]((1.0,) * 19),
                     lambda: _F["mh408_equity"](None),
                     lambda: _F["mh408_drawdowns"]([100.0]),
                     lambda: _F["mh408_drawdowns"]([100.0, -5.0]),
                     lambda: _F["mh408_pain_index"]([100.0]),
                     lambda: _F["mh408_pain_ratio"]((1.0,) * 19),
                     lambda: _F["mh408_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh408_parse_serie"](
                         "\n".join(["abc"] + ["1.0"] * 20)),
                     lambda: _F["mh408_parse_serie"](None),
                     lambda: _F["mh408_num"](True, "x"),
                     lambda: _F["mh408_num"](float("nan"), "x"),
                     lambda: _F["mh408_num"]("a", "x"),
                     lambda: _F["mh408_mappa"]((1.0,) * 19)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh408_mappa"](DEMO)
        assert abs(m["pain_ratio"] - PR) < 1e-12
        assert m["n_per"] == 36

