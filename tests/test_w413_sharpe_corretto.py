"""Test tab413 '📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh413_num", "mh413_parse_serie", "mh413_sharpe_adj",
           "mh413_verdetto", "mh413_mappa")

TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
SR = 0.27004115025880615
SKEW = -1.8729294803633167
KURT = 2.0752053895871434
CORR = 0.9093999702180136
ADJ = 0.24557541400299643


class TestRegistry413:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 415
        assert "tab413" in dvars
        assert "tab413" in withs

    def test_titoli_allineati_408_409_410_411_412_413(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410
        assert titoli[dvars.index("tab411")] == TITLE411
        assert titoli[dvars.index("tab412")] == TITLE412
        assert titoli[dvars.index("tab413")] == TITLE413

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab415"
        assert titoli[-1] == TITLE415
        assert withs[-1] == "tab415"


class TestSharpeAdj413:
    def _xs(self):
        return _F["mh413_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh413_mappa"](xs)
        assert abs(m["sharpe"] - SR) < 1e-12
        assert abs(m["skew"] - SKEW) < 1e-12
        assert abs(m["kurt_ecc"] - KURT) < 1e-12
        assert abs(m["correzione"] - CORR) < 1e-12
        assert abs(m["adj_sharpe"] - ADJ) < 1e-12
        assert m["n_per"] == 36
        assert m["rf"] == 0.0
        # la correzione taglia quasi un decimo e CAMBIA il verdetto:
        # SR classico -> ACCETTABILE, ASR -> DEBOLE
        assert m["verdetto"].startswith("DEBOLE")
        assert _F["mh413_verdetto"](m["sharpe"],
                                    m["sharpe"]).startswith("ACCETTABILE")

    def test_pezier_white_definizione(self):
        # ASR = SR * [1 + (skew/6)*SR - (kurt_ecc/24)*SR^2], a mano
        xs = list(self._xs())
        n = len(xs)
        mu = sum(xs) / n
        ss = sum((x - mu) ** 2 for x in xs)
        vpop = ss / n
        std = math.sqrt(ss / (n - 1))
        sk = (sum((x - mu) ** 3 for x in xs) / n) / (vpop ** 1.5)
        ku = (sum((x - mu) ** 4 for x in xs) / n) / (vpop ** 2) - 3.0
        sr = mu / std
        corr = 1.0 + (sk / 6.0) * sr - (ku / 24.0) * sr ** 2
        s = _F["mh413_sharpe_adj"](tuple(xs), 0.0)
        assert abs(s["skew"] - sk) < 1e-12
        assert abs(s["kurt_ecc"] - ku) < 1e-12
        assert abs(s["sharpe"] - sr) < 1e-12
        assert abs(s["correzione"] - corr) < 1e-12
        assert abs(s["adj_sharpe"] - sr * corr) < 1e-12
        assert abs(s["haircut_pct"] - (1.0 - corr) * 100.0) < 1e-12

    def test_serie_simmetrica_correzione_neutra(self):
        # serie quasi normale: la correzione resta ~1
        import random
        random.seed(7)
        xs = tuple(random.gauss(0.5, 2.0) for _ in range(60))
        s = _F["mh413_sharpe_adj"](xs, 0.0)
        assert abs(s["skew"]) < 0.6
        assert abs(s["correzione"] - 1.0) < 0.15

    def test_risk_free_sposta_gli_excess(self):
        xs = self._xs()
        s0 = _F["mh413_sharpe_adj"](xs, 0.0)
        s1 = _F["mh413_sharpe_adj"](xs, 1.0)
        assert abs((s0["media"] - s1["media"]) - 1.0) < 1e-12
        assert s1["rf"] == 1.0
        assert s1["sharpe"] < s0["sharpe"]

    def test_casi_degeneri(self):
        F = _F
        # serie piatta -> ValueError
        with pytest.raises(ValueError):
            F["mh413_sharpe_adj"](tuple([1.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh413_mappa"](tuple([2.0] * 25), 2.0)
        # soglie verdetto
        assert F["mh413_verdetto"](-0.1, 0.0).startswith("NEGATIVO")
        assert F["mh413_verdetto"](0.0, 0.0).startswith("DEBOLE")
        assert F["mh413_verdetto"](0.24, 0.0).startswith("DEBOLE")
        assert F["mh413_verdetto"](0.25, 0.0).startswith("ACCETTABILE")
        assert F["mh413_verdetto"](0.49, 0.0).startswith("ACCETTABILE")
        assert F["mh413_verdetto"](0.5, 0.0).startswith("BUONO")
        assert F["mh413_verdetto"](0.99, 0.0).startswith("BUONO")
        assert F["mh413_verdetto"](1.0, 0.0).startswith("OTTIMO")
        assert F["mh413_verdetto"](1.99, 0.0).startswith("OTTIMO")
        assert F["mh413_verdetto"](2.0, 0.0).startswith("ECCEZIONALE")
        assert F["mh413_verdetto"](5.0, 5.0).startswith("ECCEZIONALE")
        with pytest.raises(ValueError):
            F["mh413_verdetto"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh413_verdetto"](float("nan"), 0.0)
        with pytest.raises(ValueError):
            F["mh413_verdetto"](True, 0.0)
        with pytest.raises(ValueError):
            F["mh413_verdetto"](1.5, float("nan"))

    def test_validatori(self):
        for _bad in (lambda: _F["mh413_sharpe_adj"](None),
                     lambda: _F["mh413_sharpe_adj"]((1.0,) * 19),
                     lambda: _F["mh413_sharpe_adj"]((1.0,) * 25,
                                                   float("nan")),
                     lambda: _F["mh413_sharpe_adj"](tuple([3.0] * 25), 0.0),
                     lambda: _F["mh413_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh413_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh413_parse_serie"](None),
                     lambda: _F["mh413_num"](True, "x"),
                     lambda: _F["mh413_num"](float("nan"), "x"),
                     lambda: _F["mh413_mappa"]((1.0,) * 19),
                     lambda: _F["mh413_mappa"](None),
                     lambda: _F["mh413_mappa"](tuple([1.0] * 25), "xx")):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh413_mappa"](DEMO)
        assert abs(m["adj_sharpe"] - ADJ) < 1e-12
        assert m["n_per"] == 36

