"""Test tab297 '➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab297. Marginal/incremental VaR parametrico:
decision tool pre-trade (follow-up di tab292 Component VaR).
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("mv297_num", "mv297_conf", "mv297_corr",
          "mv297_parse_posizioni", "mv297_norm_cdf", "mv297_norm_ppf",
          "mv297_sigma_port", "mv297_componenti", "mv297_incrementale",
          "mv297_verdetto")
mv297_num = _F["mv297_num"]
mv297_conf = _F["mv297_conf"]
mv297_corr = _F["mv297_corr"]
mv297_parse_posizioni = _F["mv297_parse_posizioni"]
mv297_norm_cdf = _F["mv297_norm_cdf"]
mv297_norm_ppf = _F["mv297_norm_ppf"]
mv297_sigma_port = _F["mv297_sigma_port"]
mv297_componenti = _F["mv297_componenti"]
mv297_incrementale = _F["mv297_incrementale"]
mv297_verdetto = _F["mv297_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"

# book sintetico 2 posizioni a valori noti
SYN_POS = [("A", 1_000_000.0, 0.02), ("B", 500_000.0, 0.03)]
SYN_CAND = ("C", 200_000.0, 0.04, 0.5)

DEMO_TXT = """# book demo: nome;nozionale eur;vol % giornaliera
Gas TTF;2500000;3,2
Power DE;1800000;2,6
CO2 EUA;900000;2,1
Spark spread;1200000;4,0"""


def _demo_pos():
    return mv297_parse_posizioni(DEMO_TXT)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab297:
    def test_tab297_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 501
        assert TITLE297 in titoli
        assert "tab297" in dvars
        assert "tab297" in withs
        assert titoli[dvars.index("tab297")] == TITLE297
        assert TITLE482 in titoli
        keys = re.findall(r'key="(mv297_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_295_296_297(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab295")] == TITLE295
        assert titoli[dvars.index("tab296")] == TITLE296
        assert titoli[dvars.index("tab297")] == TITLE297


class TestMv297Validatori:
    def test_num_ok(self):
        assert mv297_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            mv297_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            mv297_num(float("nan"), "x")

    def test_conf_ok(self):
        assert mv297_conf(0.99) == 0.99

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            mv297_conf(1.0)

    def test_corr_ok(self):
        assert mv297_corr(-1.0, "r") == -1.0
        assert mv297_corr(0.5, "r") == 0.5

    def test_corr_fuori_ko(self):
        with pytest.raises(ValueError):
            mv297_corr(1.5, "r")


class TestMv297Parse:
    def test_ok(self):
        t = "# cmt\n\n" + "\n".join(["Gas;1000000;2,5"] * 2)
        p = mv297_parse_posizioni(t)
        assert len(p) == 2 and p[0][0] == "Gas"
        assert p[0][1] == pytest.approx(1_000_000.0)
        assert p[0][2] == pytest.approx(0.025)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;1000000;2,5")

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;1000000\nPower;2000000")

    def test_nozionale_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;-5;2,5\nPower;2000000;2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;xx;2,5\nPower;2000000;2")


class TestMv297Norm:
    def test_cdf_nota(self):
        assert mv297_norm_cdf(0.0) == pytest.approx(0.5)
        assert mv297_norm_cdf(1.959963984540054) == pytest.approx(0.975, abs=1e-6)

    def test_ppf_noti(self):
        assert mv297_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
        assert mv297_norm_ppf(0.975) == pytest.approx(1.959963984540054,
                                                     rel=1e-6)
        assert mv297_norm_ppf(0.99) == pytest.approx(2.3263478740408408,
                                                     rel=1e-6)

    def test_ppf_bordi_ko(self):
        with pytest.raises(ValueError):
            mv297_norm_ppf(0.0)
        with pytest.raises(ValueError):
            mv297_norm_ppf(1.0)


class TestMv297Sigma:
    def test_sintetico(self):
        # v = [20000, 15000], rho=0.5:
        # var = 20000^2+15000^2+2*0.5*20000*15000
        assert mv297_sigma_port(SYN_POS, 0.5) == pytest.approx(30413.8126514911)

    def test_rho_zero(self):
        assert mv297_sigma_port(SYN_POS, 0.0) == pytest.approx(25000.0)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            mv297_sigma_port([SYN_POS[0]], 0.5)


class TestMv297Componenti:
    def test_somma_eulero(self):
        r = mv297_componenti(SYN_POS, 0.5, 0.99)
        assert r["somma"] == pytest.approx(r["var"])
        assert r["var"] == pytest.approx(70753.1084032727)
        assert r["componenti"][0] == pytest.approx(42069.415807351324)
        assert r["componenti"][1] == pytest.approx(28683.69259592136)

    def test_nomi(self):
        r = mv297_componenti(SYN_POS, 0.5, 0.99)
        assert r["nomi"] == ["A", "B"]


class TestMv297Incrementale:
    def test_valori_noti(self):
        r = mv297_incrementale(SYN_POS, 0.5, 0.99, SYN_CAND)
        assert r["var_old"] == pytest.approx(70753.1084032727)
        assert r["var_new"] == pytest.approx(82871.55140944295)
        assert r["incrementale"] == pytest.approx(12118.443006170259)
        assert r["incrementale"] == pytest.approx(r["var_new"] - r["var_old"])
        assert r["componente_candidato"] == pytest.approx(13322.140652109032)
        assert r["standalone_candidato"] == pytest.approx(18610.782992326713)
        assert r["diversificazione"] == pytest.approx(5288.642340217681)
        assert r["quota"] == pytest.approx(r["incrementale"] / r["var_old"])

    def test_nozionale_c_ko(self):
        with pytest.raises(ValueError):
            mv297_incrementale(SYN_POS, 0.5, 0.99, ("C", -1.0, 0.04, 0.5))


class TestMv297Verdetto:
    def test_trascurabile(self):
        assert mv297_verdetto(100.0, 10000.0).startswith("impatto trascurabile")

    def test_contenuto(self):
        assert mv297_verdetto(1000.0, 10000.0).startswith("impatto contenuto")

    def test_rilevante(self):
        assert mv297_verdetto(3000.0, 10000.0).startswith("impatto rilevante")

    def test_soglie(self):
        assert mv297_verdetto(500.0, 10000.0).startswith("impatto contenuto")
        assert mv297_verdetto(2000.0, 10000.0).startswith("impatto rilevante")

    def test_var_old_ko(self):
        with pytest.raises(ValueError):
            mv297_verdetto(100.0, 0.0)


class TestMv297Integrazione:
    def test_catena_demo(self):
        pos = _demo_pos()
        assert len(pos) == 4
        r = mv297_incrementale(pos, 0.35, 0.99,
                               ("Coal API2", 800000.0, 0.028, 0.45))
        assert r["var_old"] == pytest.approx(332637.92510122136)
        assert r["var_new"] == pytest.approx(366738.14339864254)
        assert r["incrementale"] == pytest.approx(34100.218297421176)
        assert r["componente_candidato"] == pytest.approx(36217.051915279015)
        assert r["diversificazione"] == pytest.approx(15893.14046323578)
        assert mv297_verdetto(r["incrementale"],
                              r["var_old"]) == 'impatto contenuto: il trade alza il VaR in misura gestibile'
        # parse round-trip della demo come appare nella UI
        p2 = mv297_parse_posizioni(DEMO_TXT)
        assert len(p2) == 4
