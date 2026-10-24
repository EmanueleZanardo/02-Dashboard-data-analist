"""Test tab367 'Kelly: mappa di sensibilità f* e crescita su (p, b)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh367_num", "mh367_fstar", "mh367_log_g", "mh367_p_edge",
           "mh367_margine", "mh367_griglia", "mh367_verdetto",
           "mh367_analisi")

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
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
P = 0.6
B = 1.2
FSTAR = 0.26666666666666666
G = 0.04251707063743193
PEDGE = 0.45454545454545453
DELTA = 0.14545454545454545
VERDETTO = 'MARGINE ADEGUATO: cuscinetto di 14.5% su p: il sizing regge errori di stima moderati, mezza Kelly consigliata per prudenza.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry367:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 689
        assert "tab367" in dvars
        assert "tab367" in withs

    def test_titoli_allineati_362_363_364_365_366_367(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364
        assert titoli[dvars.index("tab365")] == TITLE365
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh367_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_num"](float("inf"), "x")


class TestFstar:
    def test_demo(self):
        assert _F["mh367_fstar"](P, B) == pytest.approx(FSTAR)

    def test_forma_chiusa(self):
        assert _F["mh367_fstar"](0.7, 2.0) == pytest.approx((0.7 * 2 - 0.3) / 2)

    def test_no_edge(self):
        assert _F["mh367_fstar"](0.40, 1.0) == 0.0

    def test_sul_confine(self):
        # p = 1/(1+b) -> f* = 0
        assert _F["mh367_fstar"](1.0 / 2.2, 1.2) == pytest.approx(0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_fstar"](1.5, B)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_fstar"](P, 0.0)


class TestLogG:
    def test_demo(self):
        assert _F["mh367_log_g"](FSTAR, P, B) == pytest.approx(G)

    def test_f_zero(self):
        assert _F["mh367_log_g"](0.0, P, B) == pytest.approx(0.0)

    def test_f_uno_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_log_g"](1.0, P, B)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_log_g"](FSTAR, 0.0, B)


class TestPEdge:
    def test_identita(self):
        for b in (0.2, 0.5, 1.2, 3.0):
            assert _F["mh367_p_edge"](b) * (1.0 + b) == pytest.approx(1.0)

    def test_demo(self):
        assert _F["mh367_p_edge"](B) == pytest.approx(PEDGE)

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_p_edge"](0.0)


class TestMargine:
    def test_demo(self):
        m = _F["mh367_margine"](P, B)
        assert m["p_edge"] == pytest.approx(PEDGE)
        assert m["delta_p"] == pytest.approx(DELTA)

    def test_sotto_edge(self):
        m = _F["mh367_margine"](0.40, 1.2)
        assert m["delta_p"] < 0.0

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_margine"](1.5, B)


class TestGriglia:
    def _gr(self):
        return _F["mh367_griglia"](0.30, 0.90, 0.20, 3.00, 41)

    def test_dimensioni(self):
        gr = self._gr()
        assert len(gr["ps"]) == 41
        assert len(gr["bs"]) == 41
        assert len(gr["fstar"]) == 41
        assert all(len(r) == 41 for r in gr["fstar"])
        assert len(gr["g"]) == 41
        assert all(len(r) == 41 for r in gr["g"])

    def test_estremi(self):
        gr = self._gr()
        assert gr["ps"][0] == pytest.approx(0.30)
        assert gr["ps"][-1] == pytest.approx(0.90)
        assert gr["bs"][0] == pytest.approx(0.20)
        assert gr["bs"][-1] == pytest.approx(3.00)

    def test_angoli_coerenti(self):
        gr = self._gr()
        assert gr["fstar"][0][0] == pytest.approx(
            _F["mh367_fstar"](gr["ps"][0], gr["bs"][0]))
        assert gr["g"][-1][-1] == pytest.approx(
            _F["mh367_log_g"](gr["fstar"][-1][-1],
                              gr["ps"][-1], gr["bs"][-1]))

    def test_zero_sotto_confine(self):
        gr = self._gr()
        b0 = gr["bs"][0]
        pe = 1.0 / (1.0 + b0)
        attesi = sum(1 for p in gr["ps"] if p <= pe)
        reali = sum(1 for f in gr["fstar"][0] if f == 0.0)
        assert attesi > 0
        assert reali == attesi

    def test_monotonia_in_p(self):
        gr = self._gr()
        for row in gr["fstar"]:
            assert all(a <= b for a, b in zip(row, row[1:]))

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_griglia"](0.30, 0.90, 0.20, 3.00, 1)

    def test_bounds_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_griglia"](0.90, 0.30, 0.20, 3.00, 41)


class TestVerdetto:
    def test_nessun_edge_margine(self):
        assert _F["mh367_verdetto"](-0.01, 0.02).startswith("NESSUN EDGE")

    def test_nessun_edge_g(self):
        assert _F["mh367_verdetto"](0.10, 0.0).startswith("NESSUN EDGE")

    def test_sottile(self):
        assert _F["mh367_verdetto"](0.03, 0.02).startswith("MARGINE SOTTILE")

    def test_adeguato(self):
        assert _F["mh367_verdetto"](0.10, 0.02).startswith("MARGINE ADEGUATO")

    def test_adeguato_al_limite(self):
        # 0.05 non e' < 0.05 -> ADEGUATO
        assert _F["mh367_verdetto"](0.05, 0.02).startswith("MARGINE ADEGUATO")

    def test_ampio(self):
        assert _F["mh367_verdetto"](0.30, 0.02).startswith("MARGINE AMPIO")

    def test_ampio_al_limite(self):
        # 0.15 non e' < 0.15 -> AMPIO
        assert _F["mh367_verdetto"](0.15, 0.02).startswith("MARGINE AMPIO")


class TestAnalisi:
    def _demo(self):
        return _F["mh367_analisi"](P, B)

    def test_demo(self):
        a = self._demo()
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["g"] == pytest.approx(G)
        assert a["p_edge"] == pytest.approx(PEDGE)
        assert a["delta_p"] == pytest.approx(DELTA)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("MARGINE ADEGUATO")
        assert len(a["griglia"]["ps"]) == 41

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["f_star"] == a2["f_star"]

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_analisi"](P, 0.0)

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh367_analisi"](1.5, B)
