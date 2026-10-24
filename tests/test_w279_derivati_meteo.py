"""Test tab279 'Derivati meteo: pricing HDD/CDD': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab279.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("wd279_num", "wd279_tipo_indice", "wd279_lato",
          "wd279_gradi_giorno", "wd279_indice_periodo", "wd279_payoff",
          "wd279_burn", "wd279_intervallo_confidenza",
          "wd279_prob_in_the_money", "wd279_sensibilita_strike",
          "wd279_verdetto", "wd279_parse_serie")
wd279_num = _F["wd279_num"]
wd279_tipo_indice = _F["wd279_tipo_indice"]
wd279_lato = _F["wd279_lato"]
wd279_gradi_giorno = _F["wd279_gradi_giorno"]
wd279_indice_periodo = _F["wd279_indice_periodo"]
wd279_payoff = _F["wd279_payoff"]
wd279_burn = _F["wd279_burn"]
wd279_intervallo_confidenza = _F["wd279_intervallo_confidenza"]
wd279_prob_in_the_money = _F["wd279_prob_in_the_money"]
wd279_sensibilita_strike = _F["wd279_sensibilita_strike"]
wd279_verdetto = _F["wd279_verdetto"]
wd279_parse_serie = _F["wd279_parse_serie"]

APP = Path(__file__).parent.parent / "app.py"

TITLE279 = "\U0001f32a\ufe0f Derivati meteo: pricing HDD/CDD"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE282 = "🧪 Margine petrolchimico: nafta → etilene"
TITLE283 = "🛢️ Carry petrolio: contango & stoccaggio fisico"
TITLE284 = "🏭 Unit commitment CCGT: accendere o no?"
TITLE285 = "🛛️ Differenziali greggio: sweet vs sour"
TITLE286 = "⛽ Basis gas TTF–PSV"
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"
TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"
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
TITLE278 = "\U0001f321\ufe0f Stress climatico: domanda e prezzo"
TITLE277 = "\u26a1 Aste MI: scostamenti vs MGP"

INDICI = [300.0, 400.0]
STRIKE = 300.0
TICK = 10.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab279:
    def test_tab279_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 691
        assert TITLE279 in titoli
        assert "tab279" in dvars
        assert "tab279" in withs
        assert titoli[dvars.index("tab279")] == TITLE279
        assert TITLE482 in titoli
        keys = re.findall(r'key="(wd279_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_277_278_279(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab277")] == TITLE277
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestWd279Validatori:
    def test_num_ok(self):
        assert wd279_num(3, "x") == 3.0
        assert wd279_num(2.5, "x") == 2.5

    def test_num_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                wd279_num(bad, "x")

    def test_tipo(self):
        assert wd279_tipo_indice("hdd") == "HDD"
        assert wd279_tipo_indice(" CDD ") == "CDD"
        for bad in ("X", "", 3, None):
            with pytest.raises(ValueError):
                wd279_tipo_indice(bad)

    def test_lato(self):
        assert wd279_lato("Call") == "call"
        assert wd279_lato("PUT") == "put"
        for bad in ("x", "", 1, None):
            with pytest.raises(ValueError):
                wd279_lato(bad)


class TestWd279GradiGiorno:
    def test_hdd(self):
        assert wd279_gradi_giorno(10.0, 18.0, "HDD") == pytest.approx(8.0)
        assert wd279_gradi_giorno(20.0, 18.0, "HDD") == pytest.approx(0.0)

    def test_cdd(self):
        assert wd279_gradi_giorno(25.0, 18.0, "CDD") == pytest.approx(7.0)
        assert wd279_gradi_giorno(15.0, 18.0, "CDD") == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_gradi_giorno(10.0, 18.0, "X")
        with pytest.raises(ValueError):
            wd279_gradi_giorno("10", 18.0, "HDD")


class TestWd279IndicePeriodo:
    def test_base(self):
        assert wd279_indice_periodo([10.0, 20.0], 18.0, "HDD") == pytest.approx(8.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_indice_periodo([], 18.0, "HDD")
        with pytest.raises(ValueError):
            wd279_indice_periodo(None, 18.0, "HDD")
        with pytest.raises(ValueError):
            wd279_indice_periodo([10.0, "x"], 18.0, "HDD")


class TestWd279Payoff:
    def test_call(self):
        assert wd279_payoff(350.0, STRIKE, TICK, "call") == pytest.approx(500.0)
        assert wd279_payoff(250.0, STRIKE, TICK, "call") == pytest.approx(0.0)

    def test_put(self):
        assert wd279_payoff(250.0, STRIKE, TICK, "put") == pytest.approx(500.0)
        assert wd279_payoff(350.0, STRIKE, TICK, "put") == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_payoff(350.0, STRIKE, 0.0, "call")
        with pytest.raises(ValueError):
            wd279_payoff(-1.0, STRIKE, TICK, "call")
        with pytest.raises(ValueError):
            wd279_payoff(350.0, -1.0, TICK, "call")
        with pytest.raises(ValueError):
            wd279_payoff(350.0, STRIKE, TICK, "x")


class TestWd279Burn:
    def test_base(self):
        b = wd279_burn(INDICI, STRIKE, TICK, "call")
        assert b["n_anni"] == 2
        assert b["premio"] == pytest.approx(500.0)
        assert b["dev_std"] == pytest.approx(500.0)
        assert b["payoff_min"] == pytest.approx(0.0)
        assert b["payoff_max"] == pytest.approx(1000.0)
        assert b["payoff_anni"] == pytest.approx([0.0, 1000.0])

    def test_un_anno(self):
        b = wd279_burn([350.0], STRIKE, TICK, "call")
        assert b["premio"] == pytest.approx(500.0)
        assert b["dev_std"] == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_burn([], STRIKE, TICK, "call")
        with pytest.raises(ValueError):
            wd279_burn([-5.0, 300.0], STRIKE, TICK, "call")


class TestWd279Intervallo:
    def test_base(self):
        ic = wd279_intervallo_confidenza(500.0, 500.0, 2)
        assert ic["inf"] == pytest.approx(0.0)
        assert ic["sup"] == pytest.approx(500.0 + 1.96 * 500.0 / 2 ** 0.5)

    def test_zero_sd(self):
        ic = wd279_intervallo_confidenza(500.0, 0.0, 10)
        assert ic["inf"] == pytest.approx(500.0)
        assert ic["sup"] == pytest.approx(500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_intervallo_confidenza(-1.0, 500.0, 2)
        with pytest.raises(ValueError):
            wd279_intervallo_confidenza(500.0, -1.0, 2)
        with pytest.raises(ValueError):
            wd279_intervallo_confidenza(500.0, 500.0, 0)


class TestWd279ProbItm:
    def test_base(self):
        assert wd279_prob_in_the_money(INDICI, STRIKE, TICK, "call") == pytest.approx(0.5)

    def test_sempre_itm(self):
        assert wd279_prob_in_the_money([400.0, 500.0], STRIKE, TICK, "call") == pytest.approx(1.0)


class TestWd279Sensibilita:
    def test_struttura(self):
        righe = wd279_sensibilita_strike(INDICI, STRIKE, TICK, "call", 5)
        assert len(righe) == 5
        assert righe[0]["strike"] == pytest.approx(60.0)
        assert righe[-1]["strike"] == pytest.approx(540.0)
        assert set(righe[0]) == {"strike", "premio"}

    def test_monotonia_call(self):
        # il premio burn e' non-crescente nello strike (0 quando strike >= max storico)
        righe = wd279_sensibilita_strike(INDICI, STRIKE, TICK, "call", 5)
        premi = [r["premio"] for r in righe]
        assert all(b <= a for a, b in zip(premi, premi[1:]))
        assert righe[2]["premio"] == pytest.approx(500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_sensibilita_strike(INDICI, 0.0, TICK, "call")
        with pytest.raises(ValueError):
            wd279_sensibilita_strike(INDICI, STRIKE, TICK, "call", 2)


class TestWd279Verdetto:
    def test_conveniente(self):
        r = wd279_verdetto(500.0, 1000.0)
        assert r["verdetto"] == "conveniente"
        assert r["rapporto"] == pytest.approx(0.5)
        assert r["scostamento_eur"] == pytest.approx(-500.0)

    def test_in_linea(self):
        r = wd279_verdetto(1050.0, 1000.0)
        assert r["verdetto"] == "in_linea"

    def test_sopra_budget(self):
        r = wd279_verdetto(1500.0, 1000.0)
        assert r["verdetto"] == "sopra_budget"
        assert r["scostamento_eur"] == pytest.approx(500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_verdetto(500.0, 0.0)
        with pytest.raises(ValueError):
            wd279_verdetto(-1.0, 1000.0)


class TestWd279ParseSerie:
    def test_misto(self):
        assert wd279_parse_serie("1, 2\n3;4") == [1.0, 2.0, 3.0, 4.0]

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_parse_serie("")
        with pytest.raises(ValueError):
            wd279_parse_serie("   ")
        with pytest.raises(ValueError):
            wd279_parse_serie("1, x")
