"""Test tab348 'Kelly con costi di trading: sizing netto': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh348_num", "mh348_int", "mh348_b_netto", "mh348_f_star",
           "mh348_g", "mh348_verdetto", "mh348_misure")

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
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
P = 0.55
WIN = 120.0
LOSS = 100.0
COSTO = 2.0
FMIN = 0.1
B_LORDO = 1.2
F_LORDO = 0.17500000000000007
G_LORDO = 0.018273846093402088
B_NETTO = 1.1568627450980393
F_NETTO = 0.16101694915254247
G_NETTO = 0.01494560432287488
EDGE_NETTO = 0.18627450980392168
EROSIONE = 0.0799031476997577
VERDETTO = 'COSTI SOSTENIBILI: f* netto 16.10% contro f* lordo 17.50% (erosione 8.0%).'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry348:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 810
        assert "tab348" in dvars
        assert "tab348" in withs

    def test_titoli_allineati_345_346_347_348(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab345")] == TITLE345
        assert titoli[dvars.index("tab346")] == TITLE346
        assert titoli[dvars.index("tab347")] == TITLE347
        assert titoli[dvars.index("tab348")] == TITLE348

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh348_num"](1.5, "x") == 1.5
        assert _F["mh348_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh348_num"](bad, "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh348_int"](5, "x", 1, 10) == 5
        assert _F["mh348_int"](1, "x", 1, 10) == 1

    def test_int_ko(self):
        for bad in (True, 1.5, "5", None):
            with pytest.raises(ValueError):
                _F["mh348_int"](bad, "x", 1, 10)
        for bad in (0, 11):
            with pytest.raises(ValueError):
                _F["mh348_int"](bad, "x", 1, 10)


class TestBNetto:
    def test_demo(self):
        assert _F["mh348_b_netto"](WIN, LOSS, COSTO) == pytest.approx(
            B_NETTO, rel=1e-12)
        assert B_NETTO == pytest.approx((WIN - COSTO) / (LOSS + COSTO),
                                        rel=1e-12)

    def test_costo_zero(self):
        assert _F["mh348_b_netto"](WIN, LOSS, 0.0) == pytest.approx(
            WIN / LOSS, rel=1e-12)

    def test_ko(self):
        for bad in (WIN, WIN + 10.0):
            with pytest.raises(ValueError):
                _F["mh348_b_netto"](WIN, LOSS, bad)
        with pytest.raises(ValueError):
            _F["mh348_b_netto"](WIN, LOSS, -1.0)
        with pytest.raises(ValueError):
            _F["mh348_b_netto"](WIN, 0.0, COSTO)
        with pytest.raises(ValueError):
            _F["mh348_b_netto"](0.0, LOSS, COSTO)


class TestFStar:
    def test_demo_lordo_formula(self):
        att = (P * B_LORDO - (1.0 - P)) / B_LORDO
        assert _F["mh348_f_star"](P, B_LORDO) == pytest.approx(
            att, rel=1e-12)
        assert F_LORDO == pytest.approx(att, rel=1e-12)
        assert F_LORDO == pytest.approx(0.175, rel=1e-12)

    def test_demo_netto(self):
        assert _F["mh348_f_star"](P, B_NETTO) == pytest.approx(
            F_NETTO, rel=1e-12)
        assert 0.0 < F_NETTO < F_LORDO

    def test_costo_zero_coincide_lordo(self):
        b0 = _F["mh348_b_netto"](WIN, LOSS, 0.0)
        assert _F["mh348_f_star"](P, b0) == pytest.approx(
            F_LORDO, rel=1e-12)

    def test_monotono_nei_costi(self):
        fs = [_F["mh348_f_star"](
            P, _F["mh348_b_netto"](WIN, LOSS, c))
            for c in (0.0, 1.0, 2.0, 5.0, 10.0)]
        assert all(a > b for a, b in zip(fs, fs[1:]))

    def test_senza_edge(self):
        assert _F["mh348_f_star"](0.40, 1.2) == 0.0
        assert _F["mh348_f_star"](0.50, 1.0) == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh348_f_star"](0.0, B_LORDO)
        with pytest.raises(ValueError):
            _F["mh348_f_star"](1.0, B_LORDO)
        with pytest.raises(ValueError):
            _F["mh348_f_star"](P, 0.0)


class TestG:
    def test_demo_formula(self):
        att = (P * math.log(1.0 + F_NETTO * B_NETTO)
               + (1.0 - P) * math.log(1.0 - F_NETTO))
        assert _F["mh348_g"](P, B_NETTO, F_NETTO) == pytest.approx(
            att, rel=1e-12)
        assert G_NETTO == pytest.approx(att, rel=1e-12)

    def test_ottimalita_kelly(self):
        g = _F["mh348_g"]
        assert g(P, B_NETTO, F_NETTO) >= g(P, B_NETTO, F_NETTO / 2.0)
        assert g(P, B_NETTO, F_NETTO) >= g(P, B_NETTO, 0.0)
        assert g(P, B_NETTO, F_NETTO) > 0.0

    def test_g_netto_minore_lordo(self):
        assert G_NETTO < G_LORDO

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh348_g"](P, B_NETTO, 1.0)
        with pytest.raises(ValueError):
            _F["mh348_g"](P, B_NETTO, -0.1)
        with pytest.raises(ValueError):
            _F["mh348_g"](0.0, B_NETTO, F_NETTO)


class TestVerdetto:
    def test_demo(self):
        assert VERDETTO == _F["mh348_verdetto"](EDGE_NETTO, F_NETTO,
                                                F_LORDO, FMIN)
        assert VERDETTO.startswith("COSTI SOSTENIBILI")

    def test_erosivi(self):
        v = _F["mh348_verdetto"](EDGE_NETTO, F_NETTO, F_LORDO, 0.50)
        assert v.startswith("COSTI EROSIVI")

    def test_edge_azzerato(self):
        v = _F["mh348_verdetto"](-0.01, 0.0, F_LORDO, FMIN)
        assert v.startswith("EDGE AZZERATO")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh348_verdetto"](EDGE_NETTO, F_NETTO, F_LORDO, 0.0)
        with pytest.raises(ValueError):
            _F["mh348_verdetto"](EDGE_NETTO, F_NETTO, F_LORDO, 1.0)


class TestMisure:
    def test_demo(self):
        m = _F["mh348_misure"](P, WIN, LOSS, COSTO, FMIN)
        assert m["b_lordo"] == pytest.approx(B_LORDO, rel=1e-12)
        assert m["f_lordo"] == pytest.approx(F_LORDO, rel=1e-12)
        assert m["g_lordo"] == pytest.approx(G_LORDO, rel=1e-12)
        assert m["b_netto"] == pytest.approx(B_NETTO, rel=1e-12)
        assert m["f_netto"] == pytest.approx(F_NETTO, rel=1e-12)
        assert m["g_netto"] == pytest.approx(G_NETTO, rel=1e-12)
        assert m["edge_netto"] == pytest.approx(EDGE_NETTO, rel=1e-12)
        assert m["erosione"] == pytest.approx(EROSIONE, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_erosione_formula(self):
        m = _F["mh348_misure"](P, WIN, LOSS, COSTO, FMIN)
        assert m["erosione"] == pytest.approx(
            1.0 - F_NETTO / F_LORDO, rel=1e-9)

    def test_tabella_costi(self):
        m = _F["mh348_misure"](P, WIN, LOSS, COSTO, FMIN)
        tab = m["tabella"]
        assert [r["costo"] for r in tab] == [0.0, 1.0, 2.0, 5.0, 10.0]
        fs = [r["f_star"] for r in tab]
        assert all(a >= b for a, b in zip(fs, fs[1:]))
        assert tab[0]["f_star"] == pytest.approx(F_LORDO, rel=1e-12)
        assert tab[2]["f_star"] == pytest.approx(F_NETTO, rel=1e-12)
        assert all(r["stato"] == "ok" for r in tab)

    def test_costo_alto_edge_azzerato(self):
        m = _F["mh348_misure"](P, WIN, LOSS, 60.0, FMIN)
        assert m["f_netto"] == 0.0
        assert m["edge_netto"] < 0.0
        assert m["verdetto"].startswith("EDGE AZZERATO")

    def test_ko_costo_mangia_vincita(self):
        with pytest.raises(ValueError):
            _F["mh348_misure"](P, WIN, LOSS, WIN, FMIN)

