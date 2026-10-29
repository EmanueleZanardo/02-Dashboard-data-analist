"""Test tab307 '🌊📉 Expected Shortfall: la perdita oltre il VaR': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab307. Expected Shortfall parametrico sotto
normale equi-correlata: ES = sigma*phi(z)/(1-alpha), decomposizione di Eulero
per posizione e segmento, rapporto ES/VaR costante nel modello normale,
semaforo coda grassa/moderata/sotto controllo contro la soglia del desk.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("es307_num", "es307_conf", "es307_corr", "es307_parse_book",
          "es307_norm_cdf", "es307_norm_ppf", "es307_norm_pdf",
          "es307_sigmas", "es307_es_book", "es307_var_book",
          "es307_componenti_es", "es307_componenti_var", "es307_seg",
          "es307_ratio", "es307_verdetto")
es307_num = _F["es307_num"]
es307_conf = _F["es307_conf"]
es307_corr = _F["es307_corr"]
es307_parse_book = _F["es307_parse_book"]
es307_norm_cdf = _F["es307_norm_cdf"]
es307_norm_ppf = _F["es307_norm_ppf"]
es307_norm_pdf = _F["es307_norm_pdf"]
es307_sigmas = _F["es307_sigmas"]
es307_es_book = _F["es307_es_book"]
es307_var_book = _F["es307_var_book"]
es307_componenti_es = _F["es307_componenti_es"]
es307_componenti_var = _F["es307_componenti_var"]
es307_seg = _F["es307_seg"]
es307_ratio = _F["es307_ratio"]
es307_verdetto = _F["es307_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
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
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"

BOOK_TXT = ("Cal-28 Baseload power;2500000;18,5;power\n"
            "Q3-28 Peak power;1200000;26,0;power\n"
            "TTF Gas Cal-28;1800000;22,0;gas\n"
            "EUA Carbon Dec-28;700000;31,0;carbon\n"
            "Batteria arbitrage;500000;28,0;flex")
BOOK = [("Cal-28 Baseload power", 2500000.0, 0.185, "power"),
        ("Q3-28 Peak power", 1200000.0, 0.26, "power"),
        ("TTF Gas Cal-28", 1800000.0, 0.22, "gas"),
        ("EUA Carbon Dec-28", 700000.0, 0.31, "carbon"),
        ("Batteria arbitrage", 500000.0, 0.28, "flex")]
RHO = 0.35
CONF = 95
SOGLIA = 1.25
VAR_TOT = 1774789.1364575038
ES_TOT = 2225657.178493701
RATIO_BOOK = 1.2540403435960477
SEG_ES = {'power': 1178331.8181331288, 'gas': 599588.5576374677, 'carbon': 280295.96400840586, 'flex': 167440.83871469882}
SEG_VAR = {'power': 939628.3175022749, 'gas': 478125.4133484301, 'carbon': 223514.3115130074, 'flex': 133521.09409379173}
RATIO_SEG = {'power': 1.2540403435960474, 'carbon': 1.2540403435960479, 'gas': 1.2540403435960479, 'flex': 1.2540403435960479}
VERDETTO = "coda grassa: ES/VaR 1.25 sopra la soglia 1.25: la perdita attesa oltre il VaR e' severa, ridurre l'esposizione di coda o aumentare il buffer di capitale"
Z95 = 1.6448536269514715
PHI_Z95 = 0.10313564037537153


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab307:
    def test_tab307_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 787
        assert TITLE307 in titoli
        assert "tab307" in dvars
        assert "tab307" in withs
        assert titoli[dvars.index("tab307")] == TITLE307
        assert TITLE482 in titoli
        assert "tab482" in dvars
        keys = re.findall(r'key="(st307_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_305_306_307(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab305")] == TITLE305
        assert titoli[dvars.index("tab306")] == TITLE306
        assert titoli[dvars.index("tab307")] == TITLE307


class TestEs307Validatori:
    def test_num_ok(self):
        assert es307_num(3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                es307_num(bad, "x")

    def test_conf(self):
        assert es307_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                es307_conf(bad)

    def test_corr(self):
        assert es307_corr(1.0) == 1.0
        assert es307_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                es307_corr(bad)


class TestEs307Parse:
    def test_demo_book(self):
        assert es307_parse_book(BOOK_TXT) == BOOK

    def test_book_ko(self):
        for bad in ("solo;tre", "x;abc;10;power", "x;10;-5;power",
                    "x;0;10;power", ""):
            with pytest.raises(ValueError):
                es307_parse_book(bad)


class TestEs307Model:
    def test_ppf_pdf_95(self):
        z = es307_norm_ppf(0.95)
        assert z == pytest.approx(Z95)
        assert es307_norm_pdf(z) == pytest.approx(PHI_Z95)

    def test_es_totale(self):
        assert es307_es_book(BOOK, RHO, CONF) == pytest.approx(ES_TOT)

    def test_var_totale(self):
        assert es307_var_book(BOOK, RHO, CONF) == pytest.approx(VAR_TOT)

    def test_es_supera_var(self):
        assert es307_es_book(BOOK, RHO, CONF) > es307_var_book(BOOK, RHO, CONF)

    def test_eulero_es_somma(self):
        comp = es307_componenti_es(BOOK, RHO, CONF)
        assert sum(comp) == pytest.approx(es307_es_book(BOOK, RHO, CONF))

    def test_eulero_var_somma(self):
        comp = es307_componenti_var(BOOK, RHO, CONF)
        assert sum(comp) == pytest.approx(es307_var_book(BOOK, RHO, CONF))

    def test_seg_es_valori(self):
        seg = es307_seg(BOOK, es307_componenti_es(BOOK, RHO, CONF))
        assert set(seg) == set(SEG_ES)
        for s, v in SEG_ES.items():
            assert seg[s] == pytest.approx(v)

    def test_seg_var_somma(self):
        segv = es307_seg(BOOK, es307_componenti_var(BOOK, RHO, CONF))
        assert sum(segv.values()) == pytest.approx(es307_var_book(BOOK, RHO, CONF))

    def test_componenti_degeneri(self):
        book0 = [("Zero", 1000000.0, 0.0, "zero")]
        assert es307_componenti_es(book0, RHO, CONF) == [0.0]
        assert es307_componenti_var(book0, RHO, CONF) == [0.0]
        assert es307_es_book(book0, RHO, CONF) == 0.0
        assert es307_var_book(book0, RHO, CONF) == 0.0

    def test_seg_lunghezza_ko(self):
        with pytest.raises(ValueError):
            es307_seg(BOOK, [1.0])


class TestEs307Ratio:
    def _seg(self):
        segv = es307_seg(BOOK, es307_componenti_var(BOOK, RHO, CONF))
        sege = es307_seg(BOOK, es307_componenti_es(BOOK, RHO, CONF))
        return segv, sege

    def test_ratio_valori(self):
        segv, sege = self._seg()
        got = es307_ratio(segv, sege)
        assert set(got) == set(RATIO_SEG)
        for s, r in RATIO_SEG.items():
            assert got[s] == pytest.approx(r)

    def test_ratio_costante_normale(self):
        segv, sege = self._seg()
        got = es307_ratio(segv, sege)
        for r in got.values():
            assert r == pytest.approx(RATIO_BOOK)

    def test_ratio_book(self):
        assert es307_es_book(BOOK, RHO, CONF) / es307_var_book(BOOK, RHO, CONF) \
            == pytest.approx(RATIO_BOOK)

    def test_var_zero_none(self):
        assert es307_ratio({"s": 0.0}, {"s": 100.0}) == {"s": None}

    def test_var_negativo_ko(self):
        with pytest.raises(ValueError):
            es307_ratio({"s": -1.0}, {"s": 10.0})


class TestEs307Verdetto:
    def test_coda_grassa(self):
        assert es307_verdetto(1.30, 1.25).startswith("coda grassa")
        assert es307_verdetto(1.25, 1.25).startswith("coda grassa")

    def test_coda_moderata(self):
        assert es307_verdetto(1.20, 1.25).startswith("coda moderata")
        assert es307_verdetto(1.15, 1.25).startswith("coda moderata")

    def test_sotto_controllo(self):
        assert es307_verdetto(1.05, 1.25).startswith("coda sotto controllo")

    def test_soglia_ko(self):
        for bad in (1.0, 0.9, -1.5):
            with pytest.raises(ValueError):
                es307_verdetto(1.3, bad)

    def test_verdetto_demo(self):
        assert es307_verdetto(RATIO_BOOK, SOGLIA) == VERDETTO
