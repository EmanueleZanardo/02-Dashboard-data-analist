"""Test tab400 '🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh400_num", "mh400_check_vol", "mh400_check_rho",
           "mh400_check_w", "mh400_covmat", "mh400_eulero",
           "mh400_distribuzione", "mh400_enb", "mh400_verdetto",
           "mh400_mappa")

TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.6
R13 = 0.3
R23 = 0.45
W1 = 0.3333333333333333
W2 = 0.3333333333333333
W3 = 0.3333333333333333
SIGP = 0.24025449469723187
ENB = 2.937894597812594
P1 = 0.2646775745909528
P2 = 0.4278152069297401
P3 = 0.307507218479307


class TestRegistry400:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 414
        assert "tab400" in dvars
        assert "tab400" in withs

    def test_titoli_allineati_395_396_397_398_399_400(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397
        assert titoli[dvars.index("tab398")] == TITLE398
        assert titoli[dvars.index("tab399")] == TITLE399
        assert titoli[dvars.index("tab400")] == TITLE400

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab414"
        assert titoli[-1] == TITLE414
        assert withs[-1] == "tab414"


class TestEnb400:
    def _demo(self):
        return _F["mh400_mappa"]((V1, V2, V3), R12, R13, R23,
                                 (W1, W2, W3), 5.0)

    def test_demo_enb(self):
        m = self._demo()
        assert abs(m["enb"] - ENB) / ENB < 1e-9
        assert abs(m["sig"] - SIGP) / SIGP < 1e-12
        assert abs(m["enb_ratio"] - ENB / 3.0) < 1e-12
        assert m["verdetto"].startswith("DIVERSIFICATO")

    def test_demo_distribuzione(self):
        m = self._demo()
        for _g, _e in zip(m["p"], (P1, P2, P3)):
            assert abs(_g - _e) < 1e-12
        assert abs(sum(m["p"]) - 1.0) < 1e-12
        assert abs(sum(m["p_pct"]) - 100.0) < 1e-9

    def test_eulero_somma_rc_uguale_sig(self):
        S = _F["mh400_covmat"]((V1, V2, V3), R12, R13, R23)
        eu = _F["mh400_eulero"]((W1, W2, W3), S)
        assert abs(sum(eu["rc"]) - eu["sig"]) / eu["sig"] < 1e-12
        assert abs(sum(eu["rc_pct"]) - 100.0) < 1e-9

    def test_simmetria_enb_3(self):
        m = _F["mh400_mappa"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0,
                              (1.0, 1.0, 1.0), 5.0)
        assert abs(m["enb"] - 3.0) < 1e-9

    def test_singola_posizione_enb_1(self):
        m = _F["mh400_mappa"]((V1, V2, V3), R12, R13, R23,
                              (100.0, 0.0, 0.0), 5.0)
        assert abs(m["enb"] - 1.0) < 1e-9

    def test_p_zero_contributo_nullo(self):
        assert abs(_F["mh400_enb"]((0.5, 0.5, 0.0)) - 2.0) < 1e-12

    def test_bound_1_n_casi_fissi(self):
        for _w, _vv, _rr in (
                ((0.9, 0.05, 0.05), (0.25, 0.35, 0.30), (0.6, 0.3, 0.45)),
                ((0.05, 0.9, 0.05), (0.25, 0.35, 0.30), (0.0, 0.0, 0.0)),
                ((0.2, 0.3, 0.5), (0.1, 0.5, 0.4), (0.8, 0.2, 0.1)),
                ((1.0 / 3, 1.0 / 3, 1.0 / 3), (0.6, 0.1, 0.2),
                 (0.9, 0.9, 0.9)),
                ((0.7, 0.2, 0.1), (0.05, 0.05, 0.6), (0.3, 0.0, 0.5))):
            m = _F["mh400_mappa"](_vv, _rr[0], _rr[1], _rr[2], _w, 5.0)
            assert 1.0 - 1e-9 <= m["enb"] <= 3.0 + 1e-9

    def test_entropiaricalcolata_a_mano(self):
        _h = -sum(_x * math.log(_x) for _x in (P1, P2, P3) if _x > 0)
        assert abs(math.exp(_h) - ENB) / ENB < 1e-12

    def test_inviaranza_scala_vol(self):
        a = self._demo()
        b = _F["mh400_mappa"](tuple(2 * _x for _x in (V1, V2, V3)),
                              R12, R13, R23, (W1, W2, W3), 5.0)
        assert abs(a["enb"] - b["enb"]) < 1e-9
        assert abs(b["sig"] - 2 * a["sig"]) / a["sig"] < 1e-9

    def test_pesi_normalizzati(self):
        _w = _F["mh400_check_w"]((20.0, 30.0, 50.0))
        assert abs(sum(_w) - 1.0) < 1e-12
        for _g, _e in zip(_w, (0.2, 0.3, 0.5)):
            assert abs(_g - _e) < 1e-12

    def test_verdetto_stati_e_bordi(self):
        assert _F["mh400_verdetto"](2.9).startswith("DIVERSIFICATO")
        assert _F["mh400_verdetto"](2.25).startswith("DIVERSIFICATO")
        assert _F["mh400_verdetto"](2.24).startswith("BILANCIATO")
        assert _F["mh400_verdetto"](1.5).startswith("BILANCIATO")
        assert _F["mh400_verdetto"](1.49).startswith("CONCENTRATO")
        assert _F["mh400_verdetto"](1.0).startswith("CONCENTRATO")

    def test_dr_maggiore_uguale_1(self):
        m = self._demo()
        assert m["dr"] >= 1.0 - 1e-12

    def test_mappa_eur(self):
        m = self._demo()
        assert abs(m["sig_eur"] - m["sig"] * 5.0e6) / m["sig_eur"] < 1e-12
        assert abs(sum(m["w_pct"]) - 100.0) < 1e-9
        assert abs(sum(m["rc_eur"]) - m["sig_eur"]) / m["sig_eur"] < 1e-12

    def test_rc_negativo_non_definito(self):
        with pytest.raises(ValueError):
            _F["mh400_distribuzione"]((0.1, -0.05, 0.2), 0.25)

    def test_casi_degeneri(self):
        for _bad in (lambda: _F["mh400_num"](True, "x"),
                     lambda: _F["mh400_num"](float("nan"), "x"),
                     lambda: _F["mh400_num"](float("inf"), "x"),
                     lambda: _F["mh400_num"]("a", "x"),
                     lambda: _F["mh400_check_vol"](2.5),
                     lambda: _F["mh400_check_vol"](-0.1),
                     lambda: _F["mh400_check_rho"](1.5),
                     lambda: _F["mh400_check_w"]((0.0, 0.0, 0.0)),
                     lambda: _F["mh400_check_w"]((-1.0, 2.0, 1.0)),
                     lambda: _F["mh400_check_w"]((1.0, 2.0)),
                     lambda: _F["mh400_covmat"]((0.2, 0.2, 0.2),
                                                0.9, 0.9, -0.9),
                     lambda: _F["mh400_eulero"](
                         (0.0, 0.0, 0.0),
                         ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0),
                          (0.0, 0.0, 1.0))),
                     lambda: _F["mh400_distribuzione"](
                         (0.1, -0.05, 0.2), 0.25),
                     lambda: _F["mh400_enb"]((0.5, 0.5, 0.5)),
                     lambda: _F["mh400_enb"]((-0.1, 0.6, 0.5)),
                     lambda: _F["mh400_enb"](()),
                     lambda: _F["mh400_verdetto"](2.0, 0),
                     lambda: _F["mh400_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (W1, W2, W3), 0.0)):
            with pytest.raises(ValueError):
                _bad()
