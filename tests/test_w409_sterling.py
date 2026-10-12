"""Test tab409 '🛟 Sterling ratio: quanto rende contro i K peggiori drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh409_num", "mh409_parse_serie", "mh409_equity",
           "mh409_episodi", "mh409_r_tot", "mh409_sterling",
           "mh409_verdetto", "mh409_mappa")

TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
DEMO = '1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n-2.0\n-2.0\n-2.0\n-2.0\n1.6\n1.6\n1.6\n1.6\n1.6\n1.6\n-1.7\n-1.7\n-1.7\n1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n-1.5\n-1.5\n1.8\n1.8\n1.8\n1.8\n1.8\n1.8\n1.8'
R_TOT = 30.484402864682146
MDD = 7.763184000000006
AVGWORST3 = 5.251491766666668
STERLING = 5.804903486315816
N_EP = 3
MEDIA = 0.7527777777777778
EP1 = (8, 12, 18, 7.7632, 10)
EP2 = (18, 21, 25, 5.0138, 7)
EP3 = (27, 29, 31, 2.9775, 4)


class TestRegistry409:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 410
        assert "tab409" in dvars
        assert "tab409" in withs

    def test_titoli_allineati_404_405_406_407_408_409(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab404")] == TITLE404
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab410"
        assert titoli[-1] == TITLE410
        assert withs[-1] == "tab410"


class TestSterling409:
    def _xs(self):
        return _F["mh409_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh409_mappa"](xs, 3)
        assert abs(m["r_tot"] - R_TOT) < 1e-12
        assert abs(m["mdd"] - MDD) < 1e-12
        assert abs(m["avg_worst"] - AVGWORST3) < 1e-12
        assert abs(m["sterling"] - STERLING) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert m["n_per"] == 36
        assert m["n_ep"] == N_EP
        assert m["k"] == 3
        assert m["verdetto"].startswith("ROBUSTO")

    def test_demo_episodi(self):
        xs = self._xs()
        m = _F["mh409_mappa"](xs, 3)
        epis = m["episodi"]
        assert len(epis) == 3
        for ep, exp in zip(epis, (EP1, EP2, EP3)):
            assert (ep["i0"], ep["iv"], ep["i1"]) == exp[:3]
            assert abs(ep["prof"] - exp[3]) < 1e-4
            assert ep["durata"] == exp[4]
            assert ep["aperto"] is False
        profs = [e["prof"] for e in epis]
        assert profs == sorted(profs, reverse=True)

    def test_sterling_definizione(self):
        # sterling = R_tot / media dei K peggiori, calcolato a mano
        xs = list(self._xs())
        eq = _F["mh409_equity"](xs)
        r_tot = _F["mh409_r_tot"](eq)
        assert abs(r_tot - R_TOT) < 1e-9
        epis = _F["mh409_episodi"](eq)
        pegg = sorted((e["prof"] for e in epis), reverse=True)[:3]
        assert abs(sum(pegg) / 3 - AVGWORST3) < 1e-9
        assert abs(_F["mh409_sterling"](xs, 3) - r_tot / (sum(pegg) / 3)) < 1e-12

    def test_sterling_k1_uguale_recovery_factor(self):
        # con K=1 lo Sterling coincide col Recovery factor (tab407):
        # R_tot / |MDD|
        xs = self._xs()
        m = _F["mh409_mappa"](xs, 1)
        assert m["k"] == 1
        assert abs(m["sterling"] - m["r_tot"] / m["mdd"]) < 1e-12

    def test_k_maggiore_di_episodi(self):
        # K >= n_ep si comporta come 'tutti'
        xs = self._xs()
        a = _F["mh409_mappa"](xs, 3)
        b = _F["mh409_mappa"](xs, 10 ** 9)
        assert b["k"] == 3
        assert abs(a["sterling"] - b["sterling"]) < 1e-12
        assert abs(a["avg_worst"] - b["avg_worst"]) < 1e-12

    def test_casi_degeneri(self):
        F = _F
        assert F["mh409_sterling"](tuple([1.0] * 25), 3) == math.inf
        assert F["mh409_sterling"](tuple([0.0] * 25), 3) == 0.0
        assert F["mh409_sterling"](tuple([-1.0] * 25), 3) < 0.0
        assert F["mh409_mappa"](tuple([1.0] * 25), 3)["n_ep"] == 0
        assert F["mh409_verdetto"](math.inf).startswith("NESSUN DRAWDOWN")
        assert F["mh409_verdetto"](2.5).startswith("ROBUSTO")
        assert F["mh409_verdetto"](2.0).startswith("ROBUSTO")
        assert F["mh409_verdetto"](1.7).startswith("SOLIDO")
        assert F["mh409_verdetto"](1.2).startswith("ACCETTABILE")
        assert F["mh409_verdetto"](0.8).startswith("FRAGILE")
        assert F["mh409_verdetto"](0.3).startswith("CRITICO")
        assert F["mh409_verdetto"](-1.0).startswith("CRITICO")

    def test_episodio_aperto(self):
        # serie che finisce sott'acqua: ultimo episodio aperto
        xs = tuple([1.0] * 18 + [-3.0] * 6 + [0.5] * 2)
        m = _F["mh409_mappa"](xs, 3)
        assert m["n_ep"] >= 1
        assert m["episodi"][-1]["aperto"] is True
        assert m["episodi"][-1]["i1"] == len(xs)

    def test_validatori(self):
        F = _F
        for _bad in (lambda: F["mh409_equity"]((1.0,) * 19),
                     lambda: F["mh409_equity"](None),
                     lambda: F["mh409_episodi"]([100.0]),
                     lambda: F["mh409_episodi"]([100.0, -5.0]),
                     lambda: F["mh409_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: F["mh409_num"](True, "x"),
                     lambda: F["mh409_num"](float("nan"), "x"),
                     lambda: F["mh409_sterling"]((1.0,) * 25, 0),
                     lambda: F["mh409_sterling"]((1.0,) * 25, -2),
                     lambda: F["mh409_sterling"]((1.0,) * 25, True),
                     lambda: F["mh409_mappa"]((1.0,) * 19, 3),
                     lambda: F["mh409_mappa"]((1.0,) * 25, 0)):
            try:
                _bad()
                raise AssertionError("caso degenere non rilevato")
            except ValueError:
                pass

    def test_coerenza_ui_ids(self):
        # gli id usati dalla UI per i top-K esistono davvero
        xs = self._xs()
        m = _F["mh409_mappa"](xs, 3)
        ids = {id(e) for e in m["episodi"]}
        top = sorted(m["episodi"], key=lambda e: e["prof"],
                     reverse=True)[:m["k"]]
        assert all(id(e) in ids for e in top)
        assert len({id(e) for e in top}) == m["k"]
