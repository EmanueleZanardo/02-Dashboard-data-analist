"""Test tab333 '📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dei capture ratio: validatori,
parse delle due serie di rendimenti %, statistiche up/down (up/down capture
%, medie di fase, asimmetria) e verdetto a 4 stati
(OTTIMO / AGGRESSIVO / DIFENSIVO / DEBOLE + NON MISURABILE).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh333_num", "mh333_parse_serie", "mh333_statistiche",
           "mh333_verdetto")

TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
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
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
SERIE_ST_DEMO = '1.87\n-0.38\n2.56\n1.18\n-0.74\n2.22\n-0.2\n1.53\n-1.1\n0.95\n1.99\n-0.56\n1.07\n-0.44\n2.91\n1.41\n-0.92\n0.72\n-0.26\n2.33\n3.37\n-1.28\n1.76\n-0.32\n0.84\n1.3\n-0.62\n2.1\n-0.14\n1.18\n1.64\n-0.8\n2.45\n-0.38\n1.41\n-1.04'
SERIE_BM_DEMO = '1.5\n-0.8\n2.1\n0.9\n-1.4\n1.8\n-0.5\n1.2\n-2.0\n0.7\n1.6\n-1.1\n0.8\n-0.9\n2.4\n1.1\n-1.7\n0.5\n-0.6\n1.9\n2.8\n-2.3\n1.4\n-0.7\n0.6\n1.0\n-1.2\n1.7\n-0.4\n0.9\n1.3\n-1.5\n2.0\n-0.8\n1.1\n-1.9'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
N_UP = 21
N_DOWN = 15
UP_CAP = 125.56313993174062
DOWN_CAP = 51.573033707865164
ASIMMETRIA = 73.99010622387546
BM_UP_AVG = 1.3952380952380952
ST_UP_AVG = 1.7519047619047619
BM_DOWN_AVG = -1.1866666666666668
ST_DOWN_AVG = -0.612
STATO = "capture ratio OTTIMO"
VERDETTO = "capture ratio OTTIMO (up 125.6% / down 51.6%): la strategia cattura piu' delle salite del benchmark e perde meno nelle discese: asimmetria favorevole, la gestione attiva crea valore in entrambe le fasi di mercato."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh333_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh333_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry333:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 717
        assert "tab333" in dvars
        assert "tab333" in withs

    def test_titoli_allineati_330_331_332_333(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab330")] == TITLE330
        assert titoli[dvars.index("tab331")] == TITLE331
        assert titoli[dvars.index("tab332")] == TITLE332
        assert titoli[dvars.index("tab333")] == TITLE333

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh333_num"](1.5, "x") == 1.5
        assert _F["mh333_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh333_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh333_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.87)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh333_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh333_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh333_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh333_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestStatistiche:
    def test_demo(self):
        rs, rb = _demo()
        s = _F["mh333_statistiche"](rs, rb)
        assert s["n"] == N_PER
        assert s["n_up"] == N_UP == 21
        assert s["n_down"] == N_DOWN == 15
        assert s["up_capture"] == pytest.approx(UP_CAP, rel=1e-9)
        assert s["down_capture"] == pytest.approx(DOWN_CAP, rel=1e-9)
        assert s["asimmetria"] == pytest.approx(ASIMMETRIA, rel=1e-9)
        assert s["bm_up_avg"] == pytest.approx(BM_UP_AVG, rel=1e-9)
        assert s["st_up_avg"] == pytest.approx(ST_UP_AVG, rel=1e-9)
        assert s["bm_down_avg"] == pytest.approx(BM_DOWN_AVG, rel=1e-9)
        assert s["st_down_avg"] == pytest.approx(ST_DOWN_AVG, rel=1e-9)

    def test_capture_coerenti(self):
        rs, rb = _demo()
        s = _F["mh333_statistiche"](rs, rb)
        assert s["up_capture"] == pytest.approx(
            s["st_up_avg"] / s["bm_up_avg"] * 100.0, rel=1e-9)
        assert s["down_capture"] == pytest.approx(
            s["st_down_avg"] / s["bm_down_avg"] * 100.0, rel=1e-9)
        assert s["asimmetria"] == pytest.approx(
            s["up_capture"] - s["down_capture"], rel=1e-9)

    def test_ko_senza_periodi_su(self):
        rs = np.array([0.5] * 36)
        rb = np.array([-0.5] * 36)
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_senza_periodi_giu(self):
        rs = np.array([0.5] * 36)
        rb = np.array([0.5] * 36)
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_pochi_su(self):
        rb = np.array([1.0, 2.0, 3.0] + [-1.0] * 33)
        rs = rb * 1.1
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_pochi_giu(self):
        rb = np.array([1.0] * 33 + [-1.0, -2.0, -3.0])
        rs = rb * 1.1
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](np.ones(11), np.ones(11))


class TestVerdetto:
    def test_verdetto_ottimo(self):
        v = _F["mh333_verdetto"](125.6, 51.6)
        assert v.startswith("capture ratio OTTIMO")

    def test_verdetto_aggressivo(self):
        v = _F["mh333_verdetto"](110.0, 120.0)
        assert v.startswith("capture ratio AGGRESSIVO")

    def test_verdetto_soglia_100(self):
        v = _F["mh333_verdetto"](100.0, 100.0)
        assert v.startswith("capture ratio AGGRESSIVO")

    def test_verdetto_difensivo(self):
        v = _F["mh333_verdetto"](90.0, 80.0)
        assert v.startswith("capture ratio DIFENSIVO")

    def test_verdetto_debole(self):
        v = _F["mh333_verdetto"](90.0, 120.0)
        assert v.startswith("capture ratio DEBOLE")

    def test_verdetto_none(self):
        v = _F["mh333_verdetto"](None, 51.6)
        assert v.startswith("capture ratio NON MISURABILE")
        v2 = _F["mh333_verdetto"](125.6, None)
        assert v2.startswith("capture ratio NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh333_verdetto"](UP_CAP, DOWN_CAP)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh333_verdetto"]("x", 50.0)
