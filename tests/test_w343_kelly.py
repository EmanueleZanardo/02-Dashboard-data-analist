
"""Test tab343 '📐 Kelly criterion: il sizing ottimale dall'edge stimato': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del criterio di Kelly: validatori,
frazione f* = (p*(b+1)-1)/b, curva di crescita geometrica
g(f) = p*ln(1+f*b) + q*ln(1-f) (None se f >= 1), misure (b, f*, half/quarter
Kelly, EV per operazione) e verdetto a 3 stati (NESSUN EDGE / EDGE POSITIVO /
EDGE ECCESSIVO).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh343_num", "mh343_kelly", "mh343_growth", "mh343_misure",
           "mh343_verdetto")

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
TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
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
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
B = 1.2
F_STAR = 0.17500000000000016
F_HALF = 0.08750000000000008
F_QUARTER = 0.04375000000000004
EV = 21.000000000000007
VERDETTO = 'KELLY EDGE POSITIVO (f* = 17.50%): aspettativa +21.00 per operazione: taglia prudente half-Kelly = 8.75% del capitale: massimizza la crescita geometrica g(f) lasciando margine di errore sulla stima di p e b.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry343:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 463
        assert "tab343" in dvars
        assert "tab343" in withs

    def test_titoli_allineati_340_341_342_343(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab340")] == TITLE340
        assert titoli[dvars.index("tab341")] == TITLE341
        assert titoli[dvars.index("tab342")] == TITLE342
        assert titoli[dvars.index("tab343")] == TITLE343

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab463"
        assert titoli[-1] == TITLE463
        assert withs[-1] == "tab463"


class TestNum:
    def test_num_ok(self):
        assert _F["mh343_num"](1.5, "x") == 1.5
        assert _F["mh343_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh343_num"](bad, "x")


class TestKelly:
    def test_demo(self):
        f = _F["mh343_kelly"](P, B)
        assert f == pytest.approx(F_STAR, rel=1e-9)
        assert f == pytest.approx(0.175, rel=1e-9)

    def test_formula(self):
        assert _F["mh343_kelly"](0.6, 2.0) == pytest.approx(
            (0.6 * 3.0 - 1.0) / 2.0, rel=1e-9)

    def test_zero_edge(self):
        # p=0.5, b=1: f* = 0, nessun edge
        assert _F["mh343_kelly"](0.5, 1.0) == pytest.approx(0.0, abs=1e-12)

    def test_negativo(self):
        assert _F["mh343_kelly"](0.4, 1.0) < 0.0

    def test_ko_p_bordi(self):
        for p in (0.0, 1.0, -0.1, 1.5):
            with pytest.raises(ValueError):
                _F["mh343_kelly"](p, 1.2)

    def test_ko_b(self):
        for b in (0.0, -1.0):
            with pytest.raises(ValueError):
                _F["mh343_kelly"](0.55, b)


class TestGrowth:
    def test_demo(self):
        g = _F["mh343_growth"](F_STAR, P, B)
        assert g is not None and g > 0.0

    def test_zero(self):
        assert _F["mh343_growth"](0.0, P, B) == pytest.approx(0.0, abs=1e-12)

    def test_none_oltre_uno(self):
        assert _F["mh343_growth"](1.0, P, B) is None
        assert _F["mh343_growth"](1.5, P, B) is None

    def test_picco_a_fstar(self):
        g0 = _F["mh343_growth"](F_STAR * 0.5, P, B)
        g1 = _F["mh343_growth"](F_STAR, P, B)
        g2 = _F["mh343_growth"](F_STAR * 1.5, P, B)
        assert g1 > g0 and g1 > g2

    def test_formula(self):
        p, b, f = 0.6, 2.0, 0.1
        q = 1.0 - p
        assert _F["mh343_growth"](f, p, b) == pytest.approx(
            p * math.log(1.0 + f * b) + q * math.log(1.0 - f), rel=1e-9)

    def test_ko_f_negativa(self):
        with pytest.raises(ValueError):
            _F["mh343_growth"](-0.1, P, B)

    def test_ko_p_bordi(self):
        with pytest.raises(ValueError):
            _F["mh343_growth"](0.1, 1.0, B)


class TestMisure:
    def _m(self):
        return _F["mh343_misure"](P, WIN, LOSS)

    def test_demo(self):
        m = self._m()
        assert m["p"] == pytest.approx(P)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f_star"] == pytest.approx(F_STAR, rel=1e-9)
        assert m["f_half"] == pytest.approx(F_HALF, rel=1e-9)
        assert m["f_quarter"] == pytest.approx(F_QUARTER, rel=1e-9)
        assert m["ev"] == pytest.approx(EV, rel=1e-9) == pytest.approx(21.0)
        assert m["f_half"] == pytest.approx(m["f_star"] / 2.0, rel=1e-9)

    def test_relazioni(self):
        m = self._m()
        assert m["b"] == pytest.approx(m["win"] / m["loss"], rel=1e-9)
        assert m["ev"] == pytest.approx(
            m["p"] * m["win"] - (1.0 - m["p"]) * m["loss"], rel=1e-9)

    def test_ko_win_loss(self):
        with pytest.raises(ValueError):
            _F["mh343_misure"](P, 0.0, LOSS)
        with pytest.raises(ValueError):
            _F["mh343_misure"](P, WIN, -1.0)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh343_misure"](1.0, WIN, LOSS)


class TestVerdetto:
    def test_nessun_edge(self):
        v = _F["mh343_verdetto"](-0.05, 0.4, 1.0, -5.0)
        assert v.startswith("KELLY NESSUN EDGE")

    def test_nessun_edge_zero(self):
        v = _F["mh343_verdetto"](0.0, 0.5, 1.0, 0.0)
        assert v.startswith("KELLY NESSUN EDGE")

    def test_positivo(self):
        v = _F["mh343_verdetto"](0.175, 0.55, 1.2, 21.0)
        assert v.startswith("KELLY EDGE POSITIVO")
        assert "8.75%" in v

    def test_eccessivo(self):
        v = _F["mh343_verdetto"](1.5, 0.9, 5.0, 100.0)
        assert v.startswith("KELLY EDGE ECCESSIVO")

    def test_verdetto_demo(self):
        v = _F["mh343_verdetto"](F_STAR, P, B, EV)
        assert v == VERDETTO
        assert v.startswith("KELLY EDGE POSITIVO")

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh343_verdetto"]("x", P, B, EV)
