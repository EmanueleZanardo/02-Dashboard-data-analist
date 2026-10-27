"""Test tab347 'VaR & Expected Shortfall del P&L dopo N trade': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del VaR/Expected Shortfall:
validatori, quantile normale di Acklam, VaR = percentile delle perdite a
confidenza conf, ES = media delle perdite oltre il VaR, cross-check
analitico via normale sul log-capitale, casi limite (f=0 -> perdite nulle;
conf alta -> VaR >= VaR a conf piu' bassa) e verdetto a 3 stati
(VAR NEI LIMITI / SOTTO OSSERVAZIONE / RIDURRE f).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh347_num", "mh347_int", "mh347_norm_ppf", "mh347_var_es",
           "mh347_verdetto", "mh347_misure", "mh346_num", "mh346_int",
           "mh346_g", "mh346_simula", "mh346_percentile")

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
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
F = 0.0875
N = 250
NSIM = 2000
SEED = 42
CONF = 0.95
VARMAX = 0.3
B = 1.2
G = 0.013709697146873145
VAR = -1.3241517924696615
ES = -0.49267159051089016
VAR_AN = -1.587851439192605
NCODA = 104
VERDETTO = 'VAR NEI LIMITI (VaR = -132.4% <= 30%): il P&L di coda resta entro la soglia del desk.'

_VE = None


def _ve():
    global _VE
    if _VE is None:
        _VE = _F["mh347_var_es"](P, B, F, N, NSIM, CONF, SEED)
    return _VE


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry347:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 754
        assert "tab347" in dvars
        assert "tab347" in withs

    def test_titoli_allineati_344_345_346_347(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab344")] == TITLE344
        assert titoli[dvars.index("tab345")] == TITLE345
        assert titoli[dvars.index("tab346")] == TITLE346
        assert titoli[dvars.index("tab347")] == TITLE347

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh347_num"](1.5, "x") == 1.5
        assert _F["mh347_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh347_num"](bad, "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh347_int"](5, "x", 1, 10) == 5
        assert _F["mh347_int"](1, "x", 1, 10) == 1

    def test_int_ko(self):
        for bad in (True, 1.5, "5", None):
            with pytest.raises(ValueError):
                _F["mh347_int"](bad, "x", 1, 10)
        for bad in (0, 11):
            with pytest.raises(ValueError):
                _F["mh347_int"](bad, "x", 1, 10)


class TestNormPpf:
    def test_mediana(self):
        assert _F["mh347_norm_ppf"](0.5) == pytest.approx(0.0, abs=1e-9)

    def test_valori_noti(self):
        assert _F["mh347_norm_ppf"](0.975) == pytest.approx(1.9599639845,
                                                           rel=1e-6)
        assert _F["mh347_norm_ppf"](0.025) == pytest.approx(-1.9599639845,
                                                           rel=1e-6)
        assert _F["mh347_norm_ppf"](0.95) == pytest.approx(1.6448536269,
                                                           rel=1e-6)

    def test_simmetria(self):
        assert _F["mh347_norm_ppf"](0.9) == pytest.approx(
            -_F["mh347_norm_ppf"](0.1), rel=1e-9)

    def test_ko(self):
        for bad in (0.0, 1.0, -0.1, 1.5, float("nan")):
            with pytest.raises(ValueError):
                _F["mh347_norm_ppf"](bad)


class TestVarEs:
    def test_determinismo(self):
        v1, v2 = _ve(), _F["mh347_var_es"](P, B, F, N, NSIM, CONF, SEED)
        assert v1["perdite"] == v2["perdite"]
        assert v1["var"] == v2["var"]
        assert v1["es"] == v2["es"]

    def test_seed_diverso(self):
        v1 = _ve()
        v2 = _F["mh347_var_es"](P, B, F, N, NSIM, CONF, SEED + 1)
        assert v1["perdite"] != v2["perdite"]

    def test_demo_valori(self):
        v = _ve()
        assert v["g"] == pytest.approx(G, rel=1e-9)
        assert v["var"] == pytest.approx(VAR, rel=1e-9)
        assert v["es"] == pytest.approx(ES, rel=1e-9)
        assert v["var_analitico"] == pytest.approx(VAR_AN, rel=1e-9)
        assert v["n_coda"] == NCODA
        assert v["conf"] == pytest.approx(CONF)
        assert v["seed"] == SEED

    def test_es_maggiore_var(self):
        v = _ve()
        assert v["es"] >= v["var"]

    def test_var_analitico_formula(self):
        v = _ve()
        z = _F["mh347_norm_ppf"](1.0 - CONF)
        up, down = 1.0 + F * B, 1.0 - F
        sig2 = P * (1.0 - P) * (math.log(up / down)) ** 2
        att = 1.0 - math.exp(N * G + z * math.sqrt(N * sig2))
        assert v["var_analitico"] == pytest.approx(att, rel=1e-9)

    def test_var_analitico_vicino_simulato(self):
        v = _ve()
        assert v["var_analitico"] == pytest.approx(v["var"], rel=0.35)

    def test_var_cresce_con_confidenza(self):
        v90 = _F["mh347_var_es"](P, B, F, N, NSIM, 0.90, SEED)
        v99 = _F["mh347_var_es"](P, B, F, N, NSIM, 0.99, SEED)
        assert v99["var"] >= v90["var"]
        assert v99["es"] >= v90["es"]

    def test_f_zero(self):
        v = _F["mh347_var_es"](P, B, 0.0, 50, 100, CONF, 7)
        assert all(x == 0.0 for x in v["perdite"])
        assert v["var"] == 0.0
        assert v["es"] == 0.0
        assert v["var_analitico"] == pytest.approx(0.0, abs=1e-12)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, 0, NSIM, CONF, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, N, 50, CONF, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, N, NSIM, 0.5, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, N, NSIM, 1.0, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, 1.0, N, NSIM, CONF, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, 0.0, F, N, NSIM, CONF, SEED)


class TestVerdetto:
    def test_nei_limiti(self):
        v = _F["mh347_verdetto"](0.20, 0.30)
        assert v.startswith("VAR NEI LIMITI")

    def test_sotto_osservazione(self):
        v = _F["mh347_verdetto"](0.40, 0.30)
        assert v.startswith("SOTTO OSSERVAZIONE")

    def test_ridurre(self):
        v = _F["mh347_verdetto"](0.60, 0.30)
        assert v.startswith("RIDURRE f")

    def test_demo(self):
        assert VERDETTO == _F["mh347_verdetto"](VAR, VARMAX)

    def test_ko_varmax(self):
        with pytest.raises(ValueError):
            _F["mh347_verdetto"](0.20, 0.0)


class TestMisure:
    def test_demo(self):
        m = _F["mh347_misure"](P, WIN, LOSS, F, N, NSIM, CONF, VARMAX,
                                SEED)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f"] == pytest.approx(F)
        assert m["n_trade"] == N
        assert m["n_sim"] == NSIM
        assert m["seed"] == SEED
        assert m["var"] == pytest.approx(VAR, rel=1e-9)
        assert m["es"] == pytest.approx(ES, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_f_zero(self):
        m = _F["mh347_misure"](P, WIN, LOSS, 0.0, 50, 100, CONF, VARMAX,
                                7)
        assert m["var"] == 0.0
        assert m["es"] == 0.0

    def test_ko_win(self):
        with pytest.raises(ValueError):
            _F["mh347_misure"](P, 0.0, LOSS, F, N, NSIM, CONF, VARMAX,
                                SEED)

