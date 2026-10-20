
"""Test tab340 '📉 Calmar ratio: il rendimento annuo per unità di max drawdown': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Calmar ratio: validatori, parse
della serie di rendimenti %, equity curve, misure (exp_ann, picco/minimo
1-based, max_dd %, recupero periodi o None, calmar) e verdetto a 4 stati
(ECCELLENTE / BUONO / MODERATO / DEBOLE + NON MISURABILE), con note su
profondita' del drawdown e tempo di recupero.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh340_num", "mh340_parse_serie", "mh340_equity",
           "mh340_misure", "mh340_verdetto")

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
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
SERIE_DEMO = '1.2\n0.8\n1.5\n-0.6\n0.9\n1.1\n-4.8\n-2.5\n1.6\n0.7\n-0.9\n1.3\n0.8\n1.0\n1.4\n-1.2\n0.6\n0.9\n1.7\n-0.5\n1.1\n0.4\n-0.7\n1.2\n0.9\n0.5\n1.6\n-1.4\n0.8\n1.0\n0.6\n1.3\n-0.8\n0.9\n0.7\n1.2'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
EXP_ANN = 4.766666666666667
PICCO = 6
MINIMO = 8
MAX_DD = -7.179999999999998
RECUPERO = 11
CALMAR = 0.6638811513463326
STATO = "Calmar ratio MODERATO"
VERDETTO = "Calmar ratio MODERATO (0.66): il rendimento annuo (+4.77 pp) copre a malapena il peggior ribasso: il sizing deve restare contenuto. Il peggior ribasso vissuto e' stato -7.2%: e' il dolore massimo che il capitale deve reggere (36 periodi). Recupero in 11 periodi."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return _F["mh340_parse_serie"](SERIE_DEMO, "strategia")


class TestRegistry340:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 592
        assert "tab340" in dvars
        assert "tab340" in withs

    def test_titoli_allineati_337_338_339_340(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab337")] == TITLE337
        assert titoli[dvars.index("tab338")] == TITLE338
        assert titoli[dvars.index("tab339")] == TITLE339
        assert titoli[dvars.index("tab340")] == TITLE340

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh340_num"](1.5, "x") == 1.5
        assert _F["mh340_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh340_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh340_parse_serie"](SERIE_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.2)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh340_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh340_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh340_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh340_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestEquity:
    def test_equity_base(self):
        eq = _F["mh340_equity"](_demo())
        assert eq[0] == pytest.approx(100.0)
        assert len(eq) == N_PER + 1

    def test_equity_compound(self):
        eq = _F["mh340_equity"](np.array([10.0, -10.0]))
        assert eq[1] == pytest.approx(110.0)
        assert eq[2] == pytest.approx(99.0)


class TestMisure:
    def test_demo(self):
        r = _demo()
        m = _F["mh340_misure"](r)
        assert m["n"] == N_PER == 36
        assert m["exp_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert m["picco"] == PICCO
        assert m["minimo"] == MINIMO
        assert m["minimo"] > m["picco"]
        assert m["max_dd"] == pytest.approx(MAX_DD, rel=1e-9)
        assert m["max_dd"] < 0
        assert m["recupero"] == RECUPERO
        assert m["calmar"] == pytest.approx(CALMAR, rel=1e-9)
        assert m["calmar"] > 0

    def test_relazioni(self):
        r = _demo()
        m = _F["mh340_misure"](r)
        assert m["exp_ann"] == pytest.approx(float(r.mean()) * 12, rel=1e-9)
        assert m["calmar"] == pytest.approx(
            m["exp_ann"] / abs(m["max_dd"]), rel=1e-9)
        assert m["dd_pct"][m["minimo"]] == pytest.approx(m["max_dd"],
                                                         rel=1e-9)
        assert min(m["dd_pct"]) == pytest.approx(m["max_dd"], rel=1e-9)

    def test_recupero_none(self):
        r = np.array([-1.0] * 11 + [1.0])
        assert len(r) == 12
        m = _F["mh340_misure"](r)
        assert m["max_dd"] < 0
        assert m["recupero"] is None

    def test_ko_monotona(self):
        with pytest.raises(ValueError):
            _F["mh340_misure"](np.full(36, 1.0))

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh340_misure"](np.ones(11))

    def test_ko_periodi_annuo(self):
        r = _demo()
        with pytest.raises(ValueError):
            _F["mh340_misure"](r, 0)
        with pytest.raises(ValueError):
            _F["mh340_misure"](r, -4)


class TestVerdetto:
    def test_verdetto_buono_demo(self):
        v = _F["mh340_verdetto"](1.8, 7.2, -4.0, 6, 36)
        assert v.startswith("Calmar ratio BUONO")
        assert "-4.0%" in v

    def test_verdetto_soglia_3(self):
        v = _F["mh340_verdetto"](3.0, 9.0, -3.0, 4, 36)
        assert v.startswith("Calmar ratio ECCELLENTE")

    def test_verdetto_soglia_15(self):
        v = _F["mh340_verdetto"](1.5, 6.0, -4.0, 4, 36)
        assert v.startswith("Calmar ratio BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh340_verdetto"](0.8, 4.0, -5.0, 8, 36)
        assert v.startswith("Calmar ratio MODERATO")

    def test_verdetto_soglia_05(self):
        v = _F["mh340_verdetto"](0.5, 2.5, -5.0, 8, 36)
        assert v.startswith("Calmar ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh340_verdetto"](0.3, 1.5, -5.0, 10, 36)
        assert v.startswith("Calmar ratio DEBOLE")

    def test_verdetto_recupero_lento(self):
        v = _F["mh340_verdetto"](1.6, 6.4, -4.0, 12, 36)
        assert "12 periodi" in v

    def test_verdetto_non_recuperato(self):
        v = _F["mh340_verdetto"](1.6, 6.4, -4.0, None, 36)
        assert "NON MISURABILE" in v

    def test_verdetto_none(self):
        v = _F["mh340_verdetto"](None, 6.4, -4.0, 6, 36)
        assert v.startswith("Calmar ratio NON MISURABILE")
        v2 = _F["mh340_verdetto"](1.6, None, -4.0, 6, 36)
        assert v2.startswith("Calmar ratio NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh340_verdetto"](CALMAR, EXP_ANN, MAX_DD, RECUPERO, N_PER)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh340_verdetto"]("x", 6.4, -4.0, 6, 36)
