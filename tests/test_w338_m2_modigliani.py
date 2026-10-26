
"""Test tab338 '⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dell'M² di Modigliani: validatori,
parse delle due serie di rendimenti %, misure (exp_ann, bm_ann, rf_ann, sd_s,
sd_b, scala, m2, delta, vol_s_ann, vol_b_ann; risk-free parametrizzabile) e
verdetto a 4 stati (ECCELLENTE / BUONO / MODERATO / DEBOLE + NON MISURABILE),
con note su leva implicita (de-levata/levata/rischio simile).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh338_num", "mh338_parse_serie", "mh338_misure", "mh338_verdetto")

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
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
SERIE_ST_DEMO = '1.43\n0.02\n2.44\n2.61\n-1.28\n-0.76\n0.81\n0.2\n0.73\n-0.03\n2.45\n2.47\n1.51\n2.61\n1.46\n-0.45\n1.07\n-0.45\n2.17\n1.28\n1.26\n0.56\n2.72\n0.67\n0.1\n0.15\n1.45\n1.52\n1.86\n2.03\n4.13\n0.65\n0.22\n-0.4\n1.38\n2.2'
SERIE_BM_DEMO = '0.94\n-0.54\n1.43\n1.63\n-1.55\n-0.83\n0.74\n0.25\n0.58\n-0.34\n1.57\n1.46\n0.67\n1.84\n1.11\n-0.35\n1.01\n-0.45\n1.57\n0.55\n0.4\n-0.15\n1.94\n0.43\n0.13\n0.21\n1.19\n1.0\n1.05\n1.07\n2.96\n0.15\n0.04\n-0.3\n1.28\n1.84'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
EXP_ANN = 13.596666666666668
BM_ANN = 8.176666666666666
RF_ANN = 0.0
SD_S = 1.1888837969035
SD_B = 0.9234536194642302
SCALA = 0.7767400160296621
M2 = 10.56107508461664
DELTA = 2.384408417949974
VOL_S_ANN = 4.118414281064521
VOL_B_ANN = 3.1989371746908453
STATO = "M² Modigliani BUONO"
VERDETTO = "M² Modigliani BUONO (Δ +2.38 pp/anno): a parita' di rischio col benchmark la strategia rende di piu' (M² 10.56 pp/anno vs benchmark 8.18). C'e' valore aggiunto oltre il rischio corso. La strategia e' piu' rischiosa del benchmark (scala 0.78 < 1): nel M² viene de-levata, il rendimento grezzo va letto con cautela."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh338_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh338_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry338:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 727
        assert "tab338" in dvars
        assert "tab338" in withs

    def test_titoli_allineati_335_336_337_338(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab335")] == TITLE335
        assert titoli[dvars.index("tab336")] == TITLE336
        assert titoli[dvars.index("tab337")] == TITLE337
        assert titoli[dvars.index("tab338")] == TITLE338

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh338_num"](1.5, "x") == 1.5
        assert _F["mh338_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh338_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh338_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.43)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh338_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh338_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh338_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh338_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestMisure:
    def test_demo(self):
        rs, rb = _demo()
        m = _F["mh338_misure"](rs, rb)
        assert m["n"] == N_PER == 36
        assert m["exp_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert m["bm_ann"] == pytest.approx(BM_ANN, rel=1e-9)
        assert m["rf_ann"] == pytest.approx(RF_ANN, rel=1e-9)
        assert m["sd_s"] == pytest.approx(SD_S, rel=1e-9)
        assert m["sd_b"] == pytest.approx(SD_B, rel=1e-9)
        assert m["scala"] == pytest.approx(SCALA, rel=1e-9)
        assert m["m2"] == pytest.approx(M2, rel=1e-9)
        assert m["delta"] == pytest.approx(DELTA, rel=1e-9)
        assert m["vol_s_ann"] == pytest.approx(VOL_S_ANN, rel=1e-9)
        assert m["vol_b_ann"] == pytest.approx(VOL_B_ANN, rel=1e-9)
        assert m["vol_s_ann"] > m["vol_b_ann"] > 0

    def test_relazioni(self):
        rs, rb = _demo()
        m = _F["mh338_misure"](rs, rb)
        assert m["scala"] == pytest.approx(m["sd_b"] / m["sd_s"], rel=1e-9)
        assert m["m2"] == pytest.approx(
            m["rf_ann"] + m["scala"] * (m["exp_ann"] - m["rf_ann"]), rel=1e-9)
        assert m["delta"] == pytest.approx(m["m2"] - m["bm_ann"], rel=1e-9)
        assert m["vol_s_ann"] == pytest.approx(m["sd_s"] * (12 ** 0.5),
                                               rel=1e-9)

    def test_riskfree_sposta_base(self):
        rs, rb = _demo()
        m0 = _F["mh338_misure"](rs, rb, 12, 0.0)
        m1 = _F["mh338_misure"](rs, rb, 12, 1.0)
        assert m1["rf_ann"] == pytest.approx(12.0, rel=1e-9)
        assert m1["m2"] == pytest.approx(
            12.0 + m0["scala"] * (m0["exp_ann"] - 12.0), rel=1e-9)
        assert m1["delta"] == pytest.approx(m1["m2"] - m0["bm_ann"], rel=1e-9)

    def test_ko_benchmark_piatto(self):
        rs = np.arange(36, dtype=float)
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, np.ones(36))

    def test_ko_strategia_piatta(self):
        with pytest.raises(ValueError):
            _F["mh338_misure"](np.ones(36), np.arange(36, dtype=float))

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh338_misure"](np.ones(11), np.ones(11))

    def test_ko_periodi_annuo(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, rb, 0)
        with pytest.raises(ValueError):
            _F["mh338_misure"](rs, rb, -4)


class TestVerdetto:
    def test_verdetto_buono_demo(self):
        v = _F["mh338_verdetto"](2.38, 0.777, 10.56, 8.18)
        assert v.startswith("M² Modigliani BUONO")
        assert "de-levata" in v

    def test_verdetto_soglia_3(self):
        v = _F["mh338_verdetto"](3.0, 1.0, 12.0, 9.0)
        assert v.startswith("M² Modigliani ECCELLENTE")

    def test_verdetto_soglia_1(self):
        v = _F["mh338_verdetto"](1.0, 1.0, 10.0, 9.0)
        assert v.startswith("M² Modigliani BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh338_verdetto"](0.5, 1.0, 9.5, 9.0)
        assert v.startswith("M² Modigliani MODERATO")

    def test_verdetto_soglia_0(self):
        v = _F["mh338_verdetto"](0.0, 1.0, 9.0, 9.0)
        assert v.startswith("M² Modigliani MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh338_verdetto"](-0.5, 1.0, 8.5, 9.0)
        assert v.startswith("M² Modigliani DEBOLE")

    def test_verdetto_scala_levata(self):
        v = _F["mh338_verdetto"](2.0, 1.5, 11.0, 9.0)
        assert "levata" in v
        assert "meno rischiosa" in v

    def test_verdetto_scala_simile(self):
        v = _F["mh338_verdetto"](2.0, 1.0, 11.0, 9.0)
        assert "simile" in v

    def test_verdetto_none(self):
        v = _F["mh338_verdetto"](None, 0.8, 10.0, 8.0)
        assert v.startswith("M² Modigliani NON MISURABILE")
        v2 = _F["mh338_verdetto"](2.0, None, 10.0, 8.0)
        assert v2.startswith("M² Modigliani NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh338_verdetto"](DELTA, SCALA, M2, BM_ANN)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh338_verdetto"]("x", 1.0, 10.0, 9.0)
