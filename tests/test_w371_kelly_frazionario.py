"""Test tab371 'Kelly frazionario: frazione ottima per un budget di volatilità': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh371_num", "mh371_fstar", "mh371_growth", "mh371_vol_log",
           "mh371_sharpe", "mh371_frazione_target", "mh371_f_fraz",
           "mh371_trade_raddoppio", "mh371_curva", "mh371_verdetto",
           "mh371_analisi")

TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
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
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
MU = 0.02
SIGMA = 0.1
V = 0.05
FSTAR = 1.9999999999999996
VOLSTAR = 0.19999999999999996
CSTAR = 0.25000000000000006
F = 0.5
G = 0.00875
VOL = 0.05
SHARPE = 0.19999999999999998
TRADE2X = 79.21682063542231
VERDETTO = 'FRAZIONARIO: applica c = 25% di f* Kelly (f = 25% x f*) per rispettare il budget di vol.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry371:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 414
        assert "tab371" in dvars
        assert "tab371" in withs

    def test_titoli_allineati_366_367_368_369_370_371(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab414"
        assert titoli[-1] == TITLE414
        assert withs[-1] == "tab414"


class TestNum:
    def test_num_ok(self):
        assert _F["mh371_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_num"](float("inf"), "x")


class TestFstar:
    def test_demo(self):
        # 0.02 / 0.10^2 = 2.0
        assert _F["mh371_fstar"](MU, SIGMA) == pytest.approx(FSTAR)

    def test_forma_chiusa(self):
        assert _F["mh371_fstar"](0.03, 0.10) == pytest.approx(3.0)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_fstar"](MU, 0.0)


class TestGrowth:
    def test_demo(self):
        assert _F["mh371_growth"](F, MU, SIGMA) == pytest.approx(G)

    def test_forma_chiusa(self):
        f, mu, sg = 0.5, 0.02, 0.10
        assert _F["mh371_growth"](f, mu, sg) == pytest.approx(
            f * mu - 0.5 * (f * sg) ** 2)

    def test_zero_in_zero(self):
        assert _F["mh371_growth"](0.0, MU, SIGMA) == pytest.approx(0.0)

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_growth"](-0.1, MU, SIGMA)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_growth"](F, MU, 0.0)


class TestFrazioneTarget:
    def test_demo(self):
        # 0.05 / (2.0 * 0.10) = 0.25
        assert _F["mh371_frazione_target"](V, FSTAR,
                                           SIGMA) == pytest.approx(CSTAR)

    def test_cappata_a_uno(self):
        # V=0.30 > vol_star=0.20 -> 1.0
        assert _F["mh371_frazione_target"](0.30, 2.0,
                                           0.10) == pytest.approx(1.0)

    def test_v_zero(self):
        assert _F["mh371_frazione_target"](0.0, 2.0,
                                           0.10) == pytest.approx(0.0)

    def test_v_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_frazione_target"](-0.01, 2.0, 0.10)

    def test_fstar_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_frazione_target"](V, 0.0, SIGMA)


class TestFFraz:
    def test_demo(self):
        assert _F["mh371_f_fraz"](CSTAR, FSTAR) == pytest.approx(F)

    def test_c_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_f_fraz"](1.5, FSTAR)

    def test_c_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_f_fraz"](-0.1, FSTAR)


class TestSharpe:
    def test_demo(self):
        assert _F["mh371_sharpe"](MU, SIGMA) == pytest.approx(SHARPE)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_sharpe"](MU, 0.0)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh371_verdetto"](MU, CSTAR).startswith("FRAZIONARIO")
        assert _F["mh371_verdetto"](MU, CSTAR) == VERDETTO

    def test_nessun_edge(self):
        assert _F["mh371_verdetto"](-0.01, 0.5).startswith("NESSUN EDGE")
        assert _F["mh371_verdetto"](0.0, 1.0).startswith("NESSUN EDGE")

    def test_pieno(self):
        assert _F["mh371_verdetto"](MU, 1.0).startswith("PIENO")

    def test_nessuna_posizione(self):
        assert _F["mh371_verdetto"](MU, 0.0).startswith("NESSUNA POSIZIONE")


class TestCurva:
    def test_dimensioni(self):
        cv = _F["mh371_curva"](MU, SIGMA)
        assert len(cv["cs"]) == 81
        assert len(cv["gs"]) == 81
        assert len(cv["vols"]) == 81

    def test_estremi(self):
        cv = _F["mh371_curva"](MU, SIGMA)
        assert cv["cs"][0] == 0.0 and cv["cs"][-1] == 1.0
        assert cv["gs"][0] == pytest.approx(0.0)
        assert cv["vols"][0] == pytest.approx(0.0)
        # a c=1: g = g* = 0.02, vol = vol_star = 0.20
        assert cv["gs"][-1] == pytest.approx(0.02)
        assert cv["vols"][-1] == pytest.approx(0.20)

    def test_coerenza_punto_a_punto(self):
        cv = _F["mh371_curva"](MU, SIGMA)
        for cc, gg, vv in zip(cv["cs"][::10], cv["gs"][::10],
                              cv["vols"][::10]):
            ff = cc * FSTAR
            assert gg == pytest.approx(_F["mh371_growth"](ff, MU, SIGMA))
            assert vv == pytest.approx(_F["mh371_vol_log"](ff, SIGMA))


class TestAnalisi:
    def test_demo(self):
        a = _F["mh371_analisi"](MU, SIGMA, V)
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["vol_star"] == pytest.approx(VOLSTAR)
        assert a["c_star"] == pytest.approx(CSTAR)
        assert a["f"] == pytest.approx(F)
        assert a["g"] == pytest.approx(G)
        assert a["vol"] == pytest.approx(VOL)
        assert a["sharpe"] == pytest.approx(SHARPE)
        assert a["trade_raddoppio"] == pytest.approx(TRADE2X)
        assert a["verdetto"] == VERDETTO

    def test_trade_raddoppio_none(self):
        assert _F["mh371_trade_raddoppio"](0.0) is None
        assert _F["mh371_trade_raddoppio"](-0.01) is None
        assert _F["mh371_trade_raddoppio"](0.01) == pytest.approx(
            math.log(2.0) / 0.01)
