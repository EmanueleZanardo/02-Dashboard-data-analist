"""Test tab291 '📊💹 Sharpe & Sortino: la strategia rende davvero?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab291.
"""

import math
import re
import statistics
from pathlib import Path

import pytest

from appfuncs import load

_F = load("ss291_num", "ss291_pos", "ss291_parse_serie", "ss291_serie_demo",
          "ss291_rendimenti", "ss291_rendimento_annuo",
          "ss291_volatilita_annua", "ss291_sharpe", "ss291_sortino",
          "ss291_drawdown_serie", "ss291_max_drawdown", "ss291_calmar",
          "ss291_statistiche", "ss291_verdetto", "_ss291_ratio")
ss291_num = _F["ss291_num"]
ss291_pos = _F["ss291_pos"]
ss291_parse_serie = _F["ss291_parse_serie"]
ss291_serie_demo = _F["ss291_serie_demo"]
ss291_rendimenti = _F["ss291_rendimenti"]
ss291_rendimento_annuo = _F["ss291_rendimento_annuo"]
ss291_volatilita_annua = _F["ss291_volatilita_annua"]
ss291_sharpe = _F["ss291_sharpe"]
ss291_sortino = _F["ss291_sortino"]
ss291_drawdown_serie = _F["ss291_drawdown_serie"]
ss291_max_drawdown = _F["ss291_max_drawdown"]
ss291_calmar = _F["ss291_calmar"]
ss291_statistiche = _F["ss291_statistiche"]
ss291_verdetto = _F["ss291_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"

EQ = [100.0, 102.0, 101.0, 105.0, 103.0, 108.0]
R = [0.02, -1.0 / 102.0, 4.0 / 101.0, -2.0 / 105.0, 5.0 / 103.0]


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab291:
    def test_tab291_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 609
        assert TITLE291 in titoli
        assert "tab291" in dvars
        assert "tab291" in withs
        assert titoli[dvars.index("tab291")] == TITLE291
        assert TITLE482 in titoli
        keys = re.findall(r'key="(ss291_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_289_290_291(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab289")] == TITLE289
        assert titoli[dvars.index("tab290")] == TITLE290
        assert titoli[dvars.index("tab291")] == TITLE291


class TestSs291ValidatoriParse:
    def test_num_ok(self):
        assert ss291_num(1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            ss291_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            ss291_num(float("nan"), "x")

    def test_pos_zero_ko(self):
        with pytest.raises(ValueError):
            ss291_pos(0.0, "x")

    def test_parse_ok(self):
        assert ss291_parse_serie("100\n101,5\n# commento\n\n102") == \
            [100.0, 101.5, 102.0]

    def test_parse_riga_sporca_ko(self):
        with pytest.raises(ValueError):
            ss291_parse_serie("100\nabc")

    def test_parse_troppo_corta_ko(self):
        with pytest.raises(ValueError):
            ss291_parse_serie("100")


class TestSs291SerieDemo:
    def test_deterministica(self):
        a = ss291_serie_demo(7, 252, 1_000_000, 0.0008, 0.012)
        b = ss291_serie_demo(7, 252, 1_000_000, 0.0008, 0.012)
        assert a == b
        assert len(a) == 252
        assert a[0] == 1_000_000.0

    def test_seed_diversi_differiscono(self):
        a = ss291_serie_demo(7, 50, 1000, 0.001, 0.01)
        b = ss291_serie_demo(8, 50, 1000, 0.001, 0.01)
        assert a != b

    def test_vol_zero_drift_puro(self):
        a = ss291_serie_demo(1, 4, 1000.0, 0.01, 0.0)
        assert a == pytest.approx([1000.0, 1010.0, 1020.1, 1030.301])

    def test_seed_non_int_ko(self):
        with pytest.raises(ValueError):
            ss291_serie_demo(1.5, 10, 1000, 0.0, 0.01)

    def test_giorni_ko(self):
        with pytest.raises(ValueError):
            ss291_serie_demo(1, 1, 1000, 0.0, 0.01)


class TestSs291Rendimenti:
    def test_valori(self):
        r = ss291_rendimenti(EQ)
        assert r == pytest.approx(R)

    def test_equity_non_positiva_ko(self):
        with pytest.raises(ValueError):
            ss291_rendimenti([100.0, 0.0, 101.0])


class TestSs291RendimentoVol:
    def test_rendimento_annuo(self):
        assert ss291_rendimento_annuo(EQ, 252) == pytest.approx(
            (108.0 / 100.0) ** (252.0 / 5.0) - 1.0)

    def test_volatilita_annua(self):
        assert ss291_volatilita_annua(EQ, 252) == pytest.approx(
            statistics.stdev(R) * math.sqrt(252))


class TestSs291SharpeSortino:
    def test_sharpe_formula(self):
        rf = 0.02
        att = (statistics.mean(R) * 252 - rf) / (
            statistics.stdev(R) * math.sqrt(252))
        assert ss291_sharpe(EQ, rf, 252) == pytest.approx(att)

    def test_sharpe_vol_nulla_inf(self):
        eq = ss291_serie_demo(3, 10, 1000.0, 0.01, 0.0)
        assert ss291_sharpe(eq) == math.inf

    def test_sortino_formula(self):
        mar_g = (1.0 + 0.0) ** (1.0 / 252) - 1.0
        dd2 = sum(min(0.0, x - mar_g) ** 2 for x in R) / len(R)
        att = (sum(R) / len(R) * 252) / (math.sqrt(dd2) * math.sqrt(252))
        assert ss291_sortino(EQ, 0.0, 252) == pytest.approx(att)

    def test_sortino_maggiore_sharpe_con_upside(self):
        # con upside forte e poco downside, sortino > sharpe
        assert ss291_sortino(EQ) > ss291_sharpe(EQ)


class TestSs291Drawdown:
    def test_serie(self):
        dd = ss291_drawdown_serie(EQ)
        assert dd[0] == pytest.approx(0.0)
        assert dd[1] == pytest.approx(0.0)
        assert dd[2] == pytest.approx((101.0 - 102.0) / 102.0)

    def test_max_drawdown(self):
        m = ss291_max_drawdown(EQ)
        assert m["max_dd"] == pytest.approx((105.0 - 103.0) / 105.0)
        assert m["picco_idx"] == 3
        assert m["valle_idx"] == 4

    def test_senza_drawdown(self):
        m = ss291_max_drawdown([100.0, 101.0, 102.0])
        assert m["max_dd"] == pytest.approx(0.0)


class TestSs291Calmar:
    def test_formula(self):
        assert ss291_calmar(EQ, 252) == pytest.approx(
            ss291_rendimento_annuo(EQ, 252) / ss291_max_drawdown(EQ)["max_dd"])


class TestSs291Statistiche:
    def test_chiavi_e_coerenza(self):
        s = ss291_statistiche(EQ)
        assert s["n_giorni"] == 5
        assert s["pnl"] == pytest.approx(8.0)
        assert s["sharpe"] == pytest.approx(ss291_sharpe(EQ))
        assert s["sortino"] == pytest.approx(ss291_sortino(EQ))
        assert s["max_drawdown"] == pytest.approx(
            ss291_max_drawdown(EQ)["max_dd"])
        assert s["win_rate"] == pytest.approx(3.0 / 5.0)


class TestSs291Verdetto:
    def test_eccellente(self):
        assert ss291_verdetto(2.5, 1.0)["verdetto"] == "eccellente"

    def test_accettabile(self):
        assert ss291_verdetto(1.2, 1.0)["verdetto"] == "accettabile"

    def test_insufficiente(self):
        assert ss291_verdetto(0.5, 1.0)["verdetto"] == "insufficiente"

    def test_soglia_non_positiva_ko(self):
        with pytest.raises(ValueError):
            ss291_verdetto(1.2, 0.0)
