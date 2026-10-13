"""Test tab344 '🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del risk of ruin: validatori,
half-Kelly, unita' di capitale u = ln(barriera)/ln(1-f), edge per trade
e = f*(p*b-q), coefficiente di Lundberg theta (radice di
p*(1+f*b)^(-theta) + q*(1-f)^(-theta) = 1 via bisezione), formula
R = barriera^theta (Cramer-Lundberg), Monte Carlo deterministico come
controprova e verdetto a 3 stati (SICURO / ACCETTABILE / PERICOLOSO).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh344_num", "mh344_kelly_half", "mh344_units", "mh344_edge",
           "mh344_lundberg", "mh344_ror", "mh344_ror_mc", "mh344_misure",
           "mh344_verdetto")

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
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
F = 0.0875
BAR = 0.5
B = 1.2
F_STAR = 0.17500000000000016
F_HALF = 0.08750000000000008
U = 7.56982008372886
EDGE = 0.018375000000000006
THETA = 3.0072874162569665
ROR = 0.12437018551099853
ROR_MC = 0.1112
VERDETTO = "ROR PERICOLOSO (R = 12.44%): oltre il 10%: il sizing e' troppo aggressivo per la barriera scelta: dimezzare la frazione (quarter-Kelly) o alzare la tolleranza al drawdown."

_M = None


def _misure():
    global _M
    if _M is None:
        _M = _F["mh344_misure"](P, WIN, LOSS, F, BAR)
    return _M


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry344:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 423
        assert "tab344" in dvars
        assert "tab344" in withs

    def test_titoli_allineati_341_342_343_344(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab341")] == TITLE341
        assert titoli[dvars.index("tab342")] == TITLE342
        assert titoli[dvars.index("tab343")] == TITLE343
        assert titoli[dvars.index("tab344")] == TITLE344

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab423"
        assert titoli[-1] == TITLE423
        assert withs[-1] == "tab423"


class TestNum:
    def test_num_ok(self):
        assert _F["mh344_num"](1.5, "x") == 1.5
        assert _F["mh344_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh344_num"](bad, "x")


class TestKellyHalf:
    def test_demo(self):
        assert _F["mh344_kelly_half"](P, B) == pytest.approx(F_HALF, rel=1e-9)
        assert _F["mh344_kelly_half"](P, B) == pytest.approx(0.0875, rel=1e-9)

    def test_formula(self):
        assert _F["mh344_kelly_half"](0.6, 2.0) == pytest.approx(
            max(0.0, (0.6 * 3.0 - 1.0) / 2.0) / 2.0, rel=1e-9)

    def test_nessun_edge_zero(self):
        assert _F["mh344_kelly_half"](0.4, 1.0) == 0.0

    def test_ko_p_bordi(self):
        for p in (0.0, 1.0):
            with pytest.raises(ValueError):
                _F["mh344_kelly_half"](p, B)

    def test_ko_b(self):
        with pytest.raises(ValueError):
            _F["mh344_kelly_half"](P, 0.0)


class TestUnits:
    def test_demo(self):
        u = _F["mh344_units"](F, BAR)
        assert u == pytest.approx(U, rel=1e-9)
        assert u == pytest.approx(math.log(0.5) / math.log(1.0 - 0.0875),
                                  rel=1e-9)
        assert u > 0

    def test_formula(self):
        assert _F["mh344_units"](0.1, 0.5) == pytest.approx(
            math.log(0.5) / math.log(0.9), rel=1e-9)

    def test_barriera_severa_piu_unita(self):
        assert _F["mh344_units"](0.1, 0.2) > _F["mh344_units"](0.1, 0.8)

    def test_ko_f(self):
        for f in (0.0, 1.0, -0.1):
            with pytest.raises(ValueError):
                _F["mh344_units"](f, BAR)

    def test_ko_barriera(self):
        for br in (0.0, 1.0, 1.5):
            with pytest.raises(ValueError):
                _F["mh344_units"](F, br)


class TestEdge:
    def test_demo(self):
        e = _F["mh344_edge"](P, B, F)
        assert e == pytest.approx(EDGE, rel=1e-9)
        assert e == pytest.approx(0.0875 * (0.55 * 1.2 - 0.45), rel=1e-9)

    def test_formula(self):
        assert _F["mh344_edge"](0.6, 2.0, 0.1) == pytest.approx(
            0.1 * (0.6 * 2.0 - 0.4), rel=1e-9)

    def test_zero_f(self):
        assert _F["mh344_edge"](P, B, 0.0) == 0.0

    def test_negativo(self):
        assert _F["mh344_edge"](0.4, 1.0, 0.05) < 0.0

    def test_ko_f_uno(self):
        with pytest.raises(ValueError):
            _F["mh344_edge"](P, B, 1.0)


class TestLundberg:
    def test_demo_radice(self):
        th = _F["mh344_lundberg"](P, B, F)
        assert th == pytest.approx(THETA, rel=1e-9)
        assert th > 0
        up, down = 1.0 + F * B, 1.0 - F
        assert P * up ** (-th) + (1.0 - P) * down ** (-th) == pytest.approx(
            1.0, rel=1e-9)

    def test_nessun_edge_zero(self):
        # drift logaritmico <= 0: nessuna radice positiva
        assert _F["mh344_lundberg"](0.4, 1.0, 0.05) == 0.0

    def test_ko_f(self):
        with pytest.raises(ValueError):
            _F["mh344_lundberg"](P, B, 1.0)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh344_lundberg"](1.0, B, F)


class TestRor:
    def test_demo(self):
        r = _F["mh344_ror"](P, B, F, BAR)
        assert r == pytest.approx(ROR, rel=1e-9)
        assert r == pytest.approx(BAR ** THETA, rel=1e-9)

    def test_nessun_edge_uno(self):
        assert _F["mh344_ror"](0.4, 1.0, 0.05, 0.5) == 1.0

    def test_edge_forte_piccolo(self):
        r = _F["mh344_ror"](0.99, 12.0, 0.02, 0.8)
        assert 0.0 <= r < 0.01

    def test_monotonia_f(self):
        # a parita' di edge, piu' f -> piu' rischio di rovina
        r1 = _F["mh344_ror"](P, B, 0.02, BAR)
        r2 = _F["mh344_ror"](P, B, 0.15, BAR)
        assert r1 < r2

    def test_range(self):
        for p, b, f in ((0.55, 1.2, 0.0875), (0.6, 2.0, 0.05),
                        (0.51, 1.1, 0.02)):
            r = _F["mh344_ror"](p, b, f, 0.5)
            assert 0.0 <= r <= 1.0

    def test_ko_barriera(self):
        with pytest.raises(ValueError):
            _F["mh344_ror"](P, B, F, 1.0)


class TestRorMc:
    def test_deterministico(self):
        a = _F["mh344_ror_mc"](P, B, F, BAR)
        b = _F["mh344_ror_mc"](P, B, F, BAR)
        assert a == b == pytest.approx(ROR_MC, rel=1e-12)

    def test_vicino_formula(self):
        assert abs(_F["mh344_ror_mc"](P, B, F, BAR) - ROR) < 0.05

    def test_range(self):
        r = _F["mh344_ror_mc"](0.6, 2.0, 0.05, 0.5, n_paths=500,
                               max_trades=500)
        assert 0.0 <= r <= 1.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh344_ror_mc"](P, B, F, BAR, n_paths=0)


class TestMisure:
    def test_demo(self):
        m = _misure()
        assert m["p"] == pytest.approx(P)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f_star"] == pytest.approx(F_STAR, rel=1e-9)
        assert m["f_half"] == pytest.approx(F_HALF, rel=1e-9)
        assert m["f"] == pytest.approx(F, rel=1e-9)
        assert m["barriera"] == pytest.approx(BAR)
        assert m["u"] == pytest.approx(U, rel=1e-9)
        assert m["edge"] == pytest.approx(EDGE, rel=1e-9)
        assert m["ror"] == pytest.approx(ROR, rel=1e-9)
        assert m["ror_mc"] == pytest.approx(ROR_MC, rel=1e-12)
        assert m["verdetto"] == VERDETTO

    def test_relazioni(self):
        m = _misure()
        assert m["f_half"] == pytest.approx(m["f_star"] / 2.0, rel=1e-9)
        assert m["u"] == pytest.approx(
            math.log(m["barriera"]) / math.log(1.0 - m["f"]), rel=1e-9)
        assert m["ror"] == pytest.approx(m["barriera"] ** THETA, rel=1e-9)

    def test_ko_win(self):
        with pytest.raises(ValueError):
            _F["mh344_misure"](P, 0.0, LOSS, F, BAR)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh344_misure"](1.0, WIN, LOSS, F, BAR)


class TestVerdetto:
    def test_sicuro(self):
        v = _F["mh344_verdetto"](0.005)
        assert v.startswith("ROR SICURO")

    def test_accettabile(self):
        v = _F["mh344_verdetto"](0.05)
        assert v.startswith("ROR ACCETTABILE")

    def test_pericoloso(self):
        v = _F["mh344_verdetto"](0.5)
        assert v.startswith("ROR PERICOLOSO")

    def test_soglie(self):
        assert _F["mh344_verdetto"](0.0099).startswith("ROR SICURO")
        assert _F["mh344_verdetto"](0.01).startswith("ROR ACCETTABILE")
        assert _F["mh344_verdetto"](0.099).startswith("ROR ACCETTABILE")
        assert _F["mh344_verdetto"](0.10).startswith("ROR PERICOLOSO")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith("ROR PERICOLOSO")
        assert "12.4" in VERDETTO
