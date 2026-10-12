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
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
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
        assert len(titoli) == len(dvars) == len(withs) == 415
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
        assert dvars[-1] == "tab415"
        assert titoli[-1] == TITLE415
        assert withs[-1] == "tab415"


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
