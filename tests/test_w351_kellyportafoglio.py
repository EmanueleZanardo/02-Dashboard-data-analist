"""Test tab351 'Kelly con portafoglio: due posizioni simultanee': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh351_num", "mh351_kelly_f", "mh351_logstats2",
           "mh351_ottimo", "mh351_verdetto", "mh351_confronto")

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
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
P1 = 0.6
P2 = 0.58
WIN1 = 120.0
LOSS1 = 100.0
WIN2 = 150.0
LOSS2 = 100.0
B1 = 1.2
B2 = 1.5
F1IND = 0.26666666666666666
F2IND = 0.2999999999999999
F1OPT = 0.24
F2OPT = 0.28
G_OPT = 0.10339294425241553
SIGMA_OPT = 0.43117466984421066
G_IND = 0.10225526926282799
SIGMA_IND = 0.4766079727889916
VERDETTO = "RIDUCI LE SIZE: le Kelly indipendenti (f1=26.67%, f2=30.00%) sovrastimano la size congiunta. L'ottimo (f1=24.00%, f2=28.00%) dà g=+10.339%/round contro +10.226% (+0.11%) con σ=43.12% contro 47.66% (+10% di volatilità). Due posizioni simultanee condividono il rischio: la size va ridotta."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry351:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 522
        assert "tab351" in dvars
        assert "tab351" in withs

    def test_titoli_allineati_347_348_349_350_351(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab347")] == TITLE347
        assert titoli[dvars.index("tab348")] == TITLE348
        assert titoli[dvars.index("tab349")] == TITLE349
        assert titoli[dvars.index("tab350")] == TITLE350
        assert titoli[dvars.index("tab351")] == TITLE351

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh351_num"](1.5, "x") == 1.5
        assert _F["mh351_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh351_num"](bad, "x")


class TestKellyF:
    def test_demo_formula(self):
        assert _F["mh351_kelly_f"](P1, B1) == pytest.approx(
            (P1 * B1 - (1.0 - P1)) / B1, rel=1e-12)
        assert F1IND == pytest.approx(
            (P1 * B1 - (1.0 - P1)) / B1, rel=1e-12)
        assert F1IND == pytest.approx(0.32 / 1.2, rel=1e-12)
        assert _F["mh351_kelly_f"](P2, B2) == pytest.approx(
            (P2 * B2 - (1.0 - P2)) / B2, rel=1e-12)
        assert F2IND == pytest.approx(0.30, rel=1e-12)

    def test_senza_edge(self):
        assert _F["mh351_kelly_f"](0.40, 1.2) == 0.0
        assert _F["mh351_kelly_f"](0.50, 1.0) == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh351_kelly_f"](0.0, B1)
        with pytest.raises(ValueError):
            _F["mh351_kelly_f"](1.0, B1)
        with pytest.raises(ValueError):
            _F["mh351_kelly_f"](P1, 0.0)


class TestLogstats2:
    def _stati(self, f1, f2):
        return ((P1 * P2, 1.0 + f1 * B1 + f2 * B2),
                (P1 * (1.0 - P2), 1.0 + f1 * B1 - f2),
                ((1.0 - P1) * P2, 1.0 - f1 + f2 * B2),
                ((1.0 - P1) * (1.0 - P2), 1.0 - f1 - f2))

    def test_demo_g_formula(self):
        stati = self._stati(F1IND, F2IND)
        att = sum(p * math.log(r) for p, r in stati)
        assert _F["mh351_logstats2"](P1, B1, F1IND, P2, B2,
                                     F2IND)["g"] == pytest.approx(
            att, rel=1e-12)
        assert G_IND == pytest.approx(att, rel=1e-12)

    def test_demo_sigma_formula(self):
        stati = self._stati(F1IND, F2IND)
        var = sum(p * math.log(r) ** 2 for p, r in stati) - G_IND ** 2
        assert _F["mh351_logstats2"](P1, B1, F1IND, P2, B2,
                                     F2IND)["sigma"] == pytest.approx(
            math.sqrt(var), rel=1e-12)
        assert SIGMA_IND == pytest.approx(math.sqrt(var), rel=1e-12)

    def test_demo_sigma_positivo(self):
        assert SIGMA_IND > 0.0
        assert 0.0 < G_IND < 1.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh351_logstats2"](P1, B1, 0.5, P2, B2, 0.5)
        with pytest.raises(ValueError):
            _F["mh351_logstats2"](P1, B1, -0.1, P2, B2, 0.1)
        with pytest.raises(ValueError):
            _F["mh351_logstats2"](P1, B1, 0.1, P2, B2, -0.1)
        with pytest.raises(ValueError):
            _F["mh351_logstats2"](0.0, B1, 0.1, P2, B2, 0.1)
        with pytest.raises(ValueError):
            _F["mh351_logstats2"](P1, 0.0, 0.1, P2, B2, 0.1)


class TestOttimo:
    def test_demo(self):
        o = _F["mh351_ottimo"](P1, B1, P2, B2)
        assert o["f1"] == pytest.approx(F1OPT, rel=1e-12)
        assert o["f2"] == pytest.approx(F2OPT, rel=1e-12)
        assert F1OPT == pytest.approx(0.24, rel=1e-12)
        assert F2OPT == pytest.approx(0.28, rel=1e-12)
        assert o["g"] == pytest.approx(G_OPT, rel=1e-12)
        assert o["sigma"] == pytest.approx(SIGMA_OPT, rel=1e-12)

    def test_ottimo_meglio_indipendenti(self):
        o = _F["mh351_ottimo"](P1, B1, P2, B2)
        assert o["f1"] + o["f2"] < 1.0
        assert o["g"] >= G_IND - 0.001
        assert o["sigma"] <= SIGMA_IND

    def test_deterministico(self):
        assert (_F["mh351_ottimo"](P1, B1, P2, B2)
                == _F["mh351_ottimo"](P1, B1, P2, B2))

    def test_senza_edge_zeri(self):
        o = _F["mh351_ottimo"](0.40, 1.2, 0.45, 1.0)
        assert o == {"f1": 0.0, "f2": 0.0, "g": 0.0, "sigma": 0.0}

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh351_ottimo"](P1, B1, P2, B2, step=0.0)
        with pytest.raises(ValueError):
            _F["mh351_ottimo"](P1, B1, P2, B2, step=0.5)
        with pytest.raises(ValueError):
            _F["mh351_ottimo"](0.0, B1, P2, B2)


class TestVerdetto:
    def test_demo(self):
        assert VERDETTO == _F["mh351_verdetto"](
            F1IND, F2IND, F1OPT, F2OPT, G_IND, SIGMA_IND, G_OPT, SIGMA_OPT)
        assert VERDETTO.startswith("RIDUCI LE SIZE")

    def test_senza_edge(self):
        v = _F["mh351_verdetto"](0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert v.startswith("NESSUN EDGE")

    def test_solo_posizione_2(self):
        v = _F["mh351_verdetto"](0.0, 0.25, 0.0, 0.20, 0.01, 0.20,
                                 0.012, 0.18)
        assert v.startswith("SOLO POSIZIONE 2")

    def test_solo_posizione_1(self):
        v = _F["mh351_verdetto"](0.25, 0.0, 0.20, 0.0, 0.01, 0.20,
                                 0.012, 0.18)
        assert v.startswith("SOLO POSIZIONE 1")

    def test_rischio_rovina(self):
        v = _F["mh351_verdetto"](0.55, 0.55, 0.30, 0.30, None, None,
                                 0.05, 0.30)
        assert v.startswith("RISCHIO ROVINA")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh351_verdetto"](-0.1, F2IND, F1OPT, F2OPT, G_IND,
                                 SIGMA_IND, G_OPT, SIGMA_OPT)
        with pytest.raises(ValueError):
            _F["mh351_verdetto"](F1IND, F2IND, 0.6, 0.5, G_IND,
                                 SIGMA_IND, G_OPT, SIGMA_OPT)


class TestConfronto:
    def test_demo(self):
        m = _F["mh351_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2)
        assert m["b1"] == pytest.approx(B1, rel=1e-12)
        assert m["b2"] == pytest.approx(B2, rel=1e-12)
        assert m["f1_ind"] == pytest.approx(F1IND, rel=1e-12)
        assert m["f2_ind"] == pytest.approx(F2IND, rel=1e-12)
        assert m["f1_opt"] == pytest.approx(F1OPT, rel=1e-12)
        assert m["f2_opt"] == pytest.approx(F2OPT, rel=1e-12)
        assert m["g_opt"] == pytest.approx(G_OPT, rel=1e-12)
        assert m["sigma_opt"] == pytest.approx(SIGMA_OPT, rel=1e-12)
        assert m["g_ind"] == pytest.approx(G_IND, rel=1e-12)
        assert m["sigma_ind"] == pytest.approx(SIGMA_IND, rel=1e-12)
        assert m["verdetto"] == VERDETTO

    def test_strategie(self):
        m = _F["mh351_confronto"](P1, WIN1, LOSS1, P2, WIN2, LOSS2)
        nomi = [s["strategia"] for s in m["strategie"]]
        assert nomi == ["Kelly indipendenti", "Half-Kelly indipendenti",
                        "Ottimo congiunto"]
        s0 = m["strategie"][0]
        assert s0["f1"] == pytest.approx(F1IND, rel=1e-12)
        assert s0["g"] == pytest.approx(G_IND, rel=1e-12)
        s1 = m["strategie"][1]
        assert s1["f1"] == pytest.approx(F1IND / 2.0, rel=1e-15)
        assert s1["f2"] == pytest.approx(F2IND / 2.0, rel=1e-15)
        assert s1["somma"] == pytest.approx(
            (F1IND + F2IND) / 2.0, rel=1e-15)
        s2 = m["strategie"][2]
        assert s2["f1"] == pytest.approx(F1OPT, rel=1e-12)
        assert s2["g"] == pytest.approx(G_OPT, rel=1e-12)

    def test_senza_edge(self):
        m = _F["mh351_confronto"](0.40, WIN1, LOSS1, 0.45, 100.0, 100.0)
        assert m["f1_ind"] == 0.0
        assert m["f2_ind"] == 0.0
        assert m["f1_opt"] == 0.0
        assert m["f2_opt"] == 0.0
        assert m["verdetto"].startswith("NESSUN EDGE")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh351_confronto"](0.0, WIN1, LOSS1, P2, WIN2, LOSS2)
        with pytest.raises(ValueError):
            _F["mh351_confronto"](P1, 0.0, LOSS1, P2, WIN2, LOSS2)
        with pytest.raises(ValueError):
            _F["mh351_confronto"](P1, WIN1, LOSS1, P2, WIN2, 0.0)

