"""Test tab305 '🎯🛡 Risk budgeting: il book rispetta i target?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab305. Risk budgeting: i component VaR di Eulero
(tab292) aggregati per segmento (tab304) vengono confrontati con i target di
quota di rischio del desk: gap in punti % e in euro, fattori di scala dei
nozionali per riallineare il book e semaforo rispettato/da
riequilibrare/fuori target.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("rb305_num", "rb305_conf", "rb305_corr", "rb305_parse_book",
          "rb305_norm_cdf", "rb305_norm_ppf", "rb305_sigmas",
          "rb305_var_book", "rb305_componenti", "rb305_quote_seg",
          "rb305_parse_target", "rb305_gap", "rb305_proposta",
          "rb305_book_proposto", "rb305_verdetto")
rb305_num = _F["rb305_num"]
rb305_conf = _F["rb305_conf"]
rb305_corr = _F["rb305_corr"]
rb305_parse_book = _F["rb305_parse_book"]
rb305_norm_cdf = _F["rb305_norm_cdf"]
rb305_norm_ppf = _F["rb305_norm_ppf"]
rb305_sigmas = _F["rb305_sigmas"]
rb305_var_book = _F["rb305_var_book"]
rb305_componenti = _F["rb305_componenti"]
rb305_quote_seg = _F["rb305_quote_seg"]
rb305_parse_target = _F["rb305_parse_target"]
rb305_gap = _F["rb305_gap"]
rb305_proposta = _F["rb305_proposta"]
rb305_book_proposto = _F["rb305_book_proposto"]
rb305_verdetto = _F["rb305_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
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
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"

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
TARGET_TXT = "power;40\ngas;30\ncarbon;20\nflex;10"
TARGET = {'power': 40.0, 'gas': 30.0, 'carbon': 20.0, 'flex': 10.0}
RHO = 0.35
CONF = 95
VAR_TOT = 1774789.1364575038
SEG_QUOTE = {'power': 52.94309606705063, 'gas': 26.939843360928663, 'carbon': 12.593851681960599, 'flex': 7.5232088900600935}
GAP_MAX_SEG = 'power'
GAP_MAX_PP = 12.943096067050632
GAP_MAX_AFTER = 3.4984660183509604
VAR_AFTER = 1794251.6618691445
VERDETTO = 'budget da riequilibrare: scostamento massimo 12.9 punti (tolleranza 5): applica i fattori di scala proposti'
Z95 = 1.6448536269514715


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab305:
    def test_tab305_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 733
        assert TITLE305 in titoli
        assert "tab305" in dvars
        assert "tab305" in withs
        assert titoli[dvars.index("tab305")] == TITLE305
        assert TITLE482 in titoli
        assert "tab482" in dvars
        keys = re.findall(r'key="(st305_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_303_304_305(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab303")] == TITLE303
        assert titoli[dvars.index("tab304")] == TITLE304
        assert titoli[dvars.index("tab305")] == TITLE305


class TestRb305Validatori:
    def test_num_ok(self):
        assert rb305_num(3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                rb305_num(bad, "x")

    def test_conf(self):
        assert rb305_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                rb305_conf(bad)

    def test_corr(self):
        assert rb305_corr(1.0) == 1.0
        assert rb305_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                rb305_corr(bad)


class TestRb305Parse:
    def test_demo_book(self):
        assert rb305_parse_book(BOOK_TXT) == BOOK

    def test_book_ko(self):
        for bad in ("solo;tre", "x;abc;10;power", "x;10;-5;power",
                    "x;0;10;power", ""):
            with pytest.raises(ValueError):
                rb305_parse_book(bad)

    def test_demo_target(self):
        assert rb305_parse_target(TARGET_TXT) == TARGET

    def test_target_somma_ko(self):
        with pytest.raises(ValueError):
            rb305_parse_target("power;40\ngas;30")

    def test_target_duplicato_ko(self):
        with pytest.raises(ValueError):
            rb305_parse_target("power;40\npower;60")

    def test_target_negativo_ko(self):
        with pytest.raises(ValueError):
            rb305_parse_target("power;-10\ngas;110")

    def test_target_riga_ko(self):
        with pytest.raises(ValueError):
            rb305_parse_target("power")

    def test_target_vuoto_ko(self):
        with pytest.raises(ValueError):
            rb305_parse_target("   \n")


class TestRb305Model:
    def test_ppf_95(self):
        assert rb305_norm_ppf(0.95) == pytest.approx(Z95)

    def test_var_totale(self):
        assert rb305_var_book(BOOK, RHO, CONF) == pytest.approx(VAR_TOT)

    def test_eulero_somma_var(self):
        comp = rb305_componenti(BOOK, RHO, CONF)
        assert sum(comp) == pytest.approx(rb305_var_book(BOOK, RHO, CONF))

    def test_quote_sommano_100(self):
        seg = rb305_quote_seg(BOOK, rb305_componenti(BOOK, RHO, CONF))
        assert sum(r["quota_pct"] for r in seg) == pytest.approx(100.0)

    def test_quote_valori(self):
        seg = rb305_quote_seg(BOOK, rb305_componenti(BOOK, RHO, CONF))
        got = {r["segmento"]: r["quota_pct"] for r in seg}
        assert set(got) == set(SEG_QUOTE)
        for s, q in SEG_QUOTE.items():
            assert got[s] == pytest.approx(q)

    def test_componenti_degeneri(self):
        book0 = [("Zero", 1000000.0, 0.0, "zero")]
        assert rb305_componenti(book0, RHO, CONF) == [0.0]
        assert rb305_var_book(book0, RHO, CONF) == 0.0


class TestRb305Gap:
    def _gap(self):
        seg = rb305_quote_seg(BOOK, rb305_componenti(BOOK, RHO, CONF))
        return rb305_gap(seg, TARGET, VAR_TOT)

    def test_ordinato_per_gap_assoluto(self):
        gap = self._gap()
        mags = [abs(r["gap_pp"]) for r in gap]
        assert mags == sorted(mags, reverse=True)

    def test_gap_eur_coerente(self):
        for r in self._gap():
            assert r["gap_eur"] == pytest.approx(r["gap_pp"] / 100.0 * VAR_TOT)

    def test_gap_max(self):
        gap = self._gap()
        assert gap[0]["segmento"] == GAP_MAX_SEG
        assert abs(gap[0]["gap_pp"]) == pytest.approx(GAP_MAX_PP)

    def test_segmento_senza_posizioni(self):
        seg = rb305_quote_seg(BOOK, rb305_componenti(BOOK, RHO, CONF))
        gap = rb305_gap(seg, {"power": 60.0, "nuke": 40.0}, VAR_TOT)
        nuke = [r for r in gap if r["segmento"] == "nuke"][0]
        assert nuke["quota_attuale"] == 0.0
        assert nuke["gap_pp"] == pytest.approx(-40.0)

    def test_var_tot_negativo_ko(self):
        seg = rb305_quote_seg(BOOK, rb305_componenti(BOOK, RHO, CONF))
        with pytest.raises(ValueError):
            rb305_gap(seg, TARGET, -1.0)


class TestRb305Proposta:
    def _prop(self):
        comp = rb305_componenti(BOOK, RHO, CONF)
        return comp, rb305_proposta(BOOK, comp, TARGET)

    def test_fattore_power(self):
        comp, prop = self._prop()
        p0 = prop[0]
        assert p0["posizione"] == "Cal-28 Baseload power"
        assert p0["fattore"] == pytest.approx(
            TARGET["power"] / SEG_QUOTE["power"])
        assert p0["nozionale_proposto"] == pytest.approx(
            p0["nozionale_attuale"] * p0["fattore"])

    def test_fattore_none_quota_zero(self):
        book0 = [("Zero", 1000000.0, 0.0, "zero")]
        comp0 = rb305_componenti(book0, RHO, CONF)
        prop = rb305_proposta(book0, comp0, {"zero": 50.0, "power": 50.0})
        assert prop[0]["fattore"] is None
        assert prop[0]["nozionale_proposto"] == 1000000.0

    def test_book_proposto_lunghezza_ko(self):
        with pytest.raises(ValueError):
            rb305_book_proposto(BOOK, [])

    def test_var_dopo_proposta(self):
        comp, prop = self._prop()
        bookp = rb305_book_proposto(BOOK, prop)
        assert len(bookp) == len(BOOK)
        assert rb305_var_book(bookp, RHO, CONF) == pytest.approx(VAR_AFTER)

    def test_proposta_riduce_gap_max(self):
        assert GAP_MAX_AFTER < GAP_MAX_PP


class TestRb305Verdetto:
    def test_rispettato(self):
        assert rb305_verdetto(3.0).startswith("budget rispettato")
        assert rb305_verdetto(5.0).startswith("budget rispettato")

    def test_da_riequilibrare(self):
        assert rb305_verdetto(10.0).startswith("budget da riequilibrare")
        assert rb305_verdetto(15.0).startswith("budget da riequilibrare")

    def test_fuori_target(self):
        assert rb305_verdetto(20.0).startswith("budget fuori target")

    def test_verdetto_demo(self):
        assert rb305_verdetto(GAP_MAX_PP) == VERDETTO
