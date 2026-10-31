"""Test tab363 'Kelly con limite di posizione: sizing con cap f_max': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh363_num", "mh363_parse_seq", "mh363_g", "mh363_fstar",
           "mh363_feff", "mh363_verdetto", "mh363_walk", "mh363_curva",
           "mh363_analisi")

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
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE428 = "⏱️ Tempo sott'acqua: durata dei drawdown e recupero"
TITLE430 = "🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"
TITLE470 = "📈 Expected Shortfall: quanto perdi quando perdi?"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"
TITLE468 = "📉 VaR annuale: quanto capitale di rischio?"
TITLE467 = "📅 L'edge annualizzato: il trade si ripete?"
TITLE466 = "💸 Costi veri: l'edge sopravvive al netto?"
TITLE465 = "📐 Correlazione: la diversificazione è reale?"
TITLE464 = "🧺 Portafoglio: quanti trade insieme?"
TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
TITLE475 = "💰 Costo di esecuzione: quanto costa davvero ruotare"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE427 = "🛡 CDaR: la perdita media dei peggiori drawdown"
TITLE429 = "🎯 Attribuzione del drawdown: chi ha causato il peggior calo"
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
P = 0.6
B = 1.2
FMAX = 0.15
SEQ = "WLWWLWWWLLWWWLWWLWLW"
FK = 0.26666666666666666
FEFF = 0.15
GK = 0.04251707063743193
GEFF = 0.03430109128743403
GR = 0.8067604558164321
FINK = 4.212802392411251
FINE = 2.756757564718123
VERDETTO = "VINCOLO SIGNIFICATIVO: cap 15.00% su f* 26.67%, il tasso di crescita scende al 80.7% dell'ottimo (15.00% invece di 26.67%)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry363:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 826
        assert "tab363" in dvars
        assert "tab363" in withs

    def test_titoli_allineati_359_360_361_362_363(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab359")] == TITLE359
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh363_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_num"](float("nan"), "x")


class TestParseSeq:
    def test_ok(self):
        assert _F["mh363_parse_seq"]("wL") == ("W", "L")

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_parse_seq"]("   ")

    def test_carattere_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_parse_seq"]("WX")


class TestG:
    def test_g_zero(self):
        assert _F["mh363_g"](0.0, P, B) == 0.0

    def test_g_demo(self):
        assert abs(_F["mh363_g"](FK, P, B) - GK) < 1e-12

    def test_g_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_g"](1.0, P, B)


class TestFstar:
    def test_demo(self):
        assert abs(_F["mh363_fstar"](P, B) - FK) < 1e-12

    def test_no_edge(self):
        assert _F["mh363_fstar"](0.30, 1.0) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_fstar"](P, 0.0)


class TestFeff:
    def test_cap_vincolante(self):
        assert _F["mh363_feff"](FK, FMAX) == FEFF

    def test_cap_non_vincolante(self):
        assert _F["mh363_feff"](0.10, 0.30) == 0.10

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_feff"](0.10, 1.0)


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh363_verdetto"](0.0, 0.20, 0.0, 1.0).startswith(
            "NESSUN EDGE")

    def test_cap_non_vincolante(self):
        assert _F["mh363_verdetto"](0.10, 0.30, 0.10, 1.0).startswith(
            "CAP NON VINCOLANTE")

    def test_vincolo_leggero(self):
        assert _F["mh363_verdetto"](0.20, 0.15, 0.15, 0.99).startswith(
            "VINCOLO LEGGERO")

    def test_vincolo_significativo(self):
        assert _F["mh363_verdetto"](0.20, 0.15, 0.15, 0.80).startswith(
            "VINCOLO SIGNIFICATIVO")

    def test_vincolo_forte(self):
        assert _F["mh363_verdetto"](0.20, 0.10, 0.10, 0.50).startswith(
            "VINCOLO FORTE")


class TestWalk:
    def test_demo(self):
        sq = _F["mh363_parse_seq"](SEQ)
        wk = _F["mh363_walk"](sq, FK, B)
        we = _F["mh363_walk"](sq, FEFF, B)
        assert wk["n"] == we["n"] == 20
        assert abs(wk["finale"] - FINK) < 1e-9
        assert abs(we["finale"] - FINE) < 1e-9
        assert len(wk["equity"]) == 21
        assert 0.0 <= wk["max_dd"] < 1.0

    def test_f_zero_fermo(self):
        sq = _F["mh363_parse_seq"]("WL")
        w = _F["mh363_walk"](sq, 0.0, B)
        assert all(e == 1.0 for e in w["equity"])

    def test_f_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_walk"](("W",), 1.0, B)


class TestCurva:
    def test_demo(self):
        c = _F["mh363_curva"](P, B, 0.60, 25)
        assert len(c) == 25
        assert c[0]["f"] == 0.0
        assert abs(c[0]["g"]) < 1e-15
        imax = max(range(25), key=lambda i: c[i]["g"])
        assert abs(c[imax]["f"] - FK) < 0.03

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_curva"](P, B, 0.60, 1)


class TestAnalisi:
    def _demo(self):
        return _F["mh363_analisi"](P, B, FMAX, SEQ)

    def test_demo(self):
        a = self._demo()
        assert abs(a["f_kelly"] - FK) < 1e-12
        assert a["f_eff"] == FEFF
        assert abs(a["g_kelly"] - GK) < 1e-12
        assert abs(a["g_ratio"] - GR) < 1e-12
        assert abs(a["finalek"] - FINK) < 1e-9
        assert abs(a["finalee"] - FINE) < 1e-9
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("VINCOLO SIGNIFICATIVO")
        assert a["n"] == 20
        assert a["finalee"] < a["finalek"]

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["finalek"] == a2["finalek"]
        assert a1["verdetto"] == a2["verdetto"]

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_analisi"](0.0, B, FMAX, SEQ)

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_analisi"](P, B, 2.0, SEQ)

    def test_seq_ko(self):
        with pytest.raises(ValueError):
            _F["mh363_analisi"](P, B, FMAX, "WX")
