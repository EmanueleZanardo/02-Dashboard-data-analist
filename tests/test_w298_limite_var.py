"""Test tab298 '🚦📏 Limite VaR: quanto margine resta?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab298. Monitor del limite di VaR: headroom,
utilizzo e size massima del trade candidato per bisezione (follow-up di
tab297 Marginal VaR).
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("rb298_num", "rb298_conf", "rb298_corr",
          "rb298_parse_posizioni", "rb298_norm_cdf", "rb298_norm_ppf",
          "rb298_var_book", "rb298_var_con_candidato", "rb298_headroom",
          "rb298_max_nozionale", "rb298_verdetto")
rb298_num = _F["rb298_num"]
rb298_conf = _F["rb298_conf"]
rb298_corr = _F["rb298_corr"]
rb298_parse_posizioni = _F["rb298_parse_posizioni"]
rb298_norm_cdf = _F["rb298_norm_cdf"]
rb298_norm_ppf = _F["rb298_norm_ppf"]
rb298_var_book = _F["rb298_var_book"]
rb298_var_con_candidato = _F["rb298_var_con_candidato"]
rb298_headroom = _F["rb298_headroom"]
rb298_max_nozionale = _F["rb298_max_nozionale"]
rb298_verdetto = _F["rb298_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"

# book sintetico 2 posizioni a valori noti
SYN_POS = [("A", 1_000_000.0, 0.02), ("B", 500_000.0, 0.03)]
SYN_LIM = 300_000.0
SYN_CAND_VOL = 0.04
SYN_CAND_CORR = 0.5
SYN_PROP = 200_000.0

DEMO_TXT = """# book demo: nome;nozionale eur;vol % giornaliera
Gas TTF;2500000;3,2
Power DE;1800000;2,6
CO2 EUA;900000;2,1
Spark spread;1200000;4,0"""
DEMO_LIM = 400_000.0
DEMO_CAND = ("Coal API2", 800000.0, 0.028, 0.45)


def _demo_pos():
    return rb298_parse_posizioni(DEMO_TXT)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab298:
    def test_tab298_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 576
        assert TITLE298 in titoli
        assert "tab298" in dvars
        assert "tab298" in withs
        assert titoli[dvars.index("tab298")] == TITLE298
        assert TITLE482 in titoli
        keys = re.findall(r'key="(rb298_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_296_297_298(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab296")] == TITLE296
        assert titoli[dvars.index("tab297")] == TITLE297
        assert titoli[dvars.index("tab298")] == TITLE298


class TestRb298Validatori:
    def test_num_ok(self):
        assert rb298_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            rb298_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            rb298_num(float("nan"), "x")

    def test_conf_ok(self):
        assert rb298_conf(0.99) == 0.99

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            rb298_conf(1.0)

    def test_corr_ok(self):
        assert rb298_corr(-1.0, "r") == -1.0
        assert rb298_corr(0.5, "r") == 0.5

    def test_corr_fuori_ko(self):
        with pytest.raises(ValueError):
            rb298_corr(1.5, "r")


class TestRb298Parse:
    def test_ok(self):
        t = "# cmt\n\n" + "\n".join(["Gas;1000000;2,5"] * 2)
        p = rb298_parse_posizioni(t)
        assert len(p) == 2 and p[0][0] == "Gas"
        assert p[0][1] == pytest.approx(1_000_000.0)
        assert p[0][2] == pytest.approx(0.025)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;1000000;2,5")

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;1000000\nPower;2000000")

    def test_nozionale_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;-5;2,5\nPower;2000000;2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;xx;2,5\nPower;2000000;2")


class TestRb298Norm:
    def test_cdf_nota(self):
        assert rb298_norm_cdf(0.0) == pytest.approx(0.5)
        assert rb298_norm_cdf(1.959963984540054) == pytest.approx(0.975, abs=1e-6)

    def test_ppf_noti(self):
        assert rb298_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
        assert rb298_norm_ppf(0.975) == pytest.approx(1.959963984540054,
                                                     rel=1e-6)
        assert rb298_norm_ppf(0.99) == pytest.approx(2.3263478740408408,
                                                     rel=1e-6)

    def test_ppf_bordi_ko(self):
        with pytest.raises(ValueError):
            rb298_norm_ppf(0.0)
        with pytest.raises(ValueError):
            rb298_norm_ppf(1.0)


class TestRb298VarBook:
    def test_sintetico(self):
        assert rb298_var_book(SYN_POS, 0.5, 0.99) == pytest.approx(70753.1084032727)

    def test_rho_zero(self):
        assert rb298_var_book(SYN_POS, 0.0, 0.99) == pytest.approx(58158.69685102098)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            rb298_var_book([SYN_POS[0]], 0.5, 0.99)


class TestRb298VarConCandidato:
    def test_sintetico(self):
        v = rb298_var_con_candidato(SYN_POS, 0.5, 0.99,
                                    ("C", SYN_PROP, SYN_CAND_VOL,
                                     SYN_CAND_CORR))
        assert v == pytest.approx(82871.55140944295)
        assert v >= rb298_var_book(SYN_POS, 0.5, 0.99)

    def test_nozionale_c_ko(self):
        with pytest.raises(ValueError):
            rb298_var_con_candidato(SYN_POS, 0.5, 0.99, ("C", -1.0, 0.04, 0.5))


class TestRb298Headroom:
    def test_valori(self):
        h = rb298_headroom(70753.1084032727, SYN_LIM)
        assert h["headroom"] == pytest.approx(229246.8915967273)
        assert h["utilizzo"] == pytest.approx(23.584369467757565)
        assert h["headroom"] == pytest.approx(SYN_LIM - 70753.1084032727)

    def test_sforamento_negativo(self):
        h = rb298_headroom(SYN_LIM + 1.0, SYN_LIM)
        assert h["headroom"] == pytest.approx(-1.0)
        assert h["utilizzo"] == pytest.approx(100.0 * (SYN_LIM + 1.0) / SYN_LIM)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            rb298_headroom(100.0, 0.0)


class TestRb298MaxNozionale:
    def test_sintetico(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, SYN_LIM)
        assert m == pytest.approx(2725892.773663776, rel=1e-6)

    def test_al_limite(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, SYN_LIM)
        v = rb298_var_con_candidato(SYN_POS, 0.5, 0.99, ("C", m, SYN_CAND_VOL,
                                                        SYN_CAND_CORR))
        assert v == pytest.approx(SYN_LIM, rel=1e-4)

    def test_sopra_max_sfora(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, SYN_LIM)
        v = rb298_var_con_candidato(SYN_POS, 0.5, 0.99,
                                    ("C", m * 1.5, SYN_CAND_VOL, SYN_CAND_CORR))
        assert v > SYN_LIM

    def test_book_sforato_zero(self):
        assert rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                   SYN_CAND_CORR,
                                   rb298_var_book(SYN_POS, 0.5,
                                                  0.99)) == 0.0

    def test_vol_nulla_infinito(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, 0.0, SYN_CAND_CORR,
                                SYN_LIM)
        assert math.isinf(m)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, -10.0)


class TestRb298Verdetto:
    def test_ok(self):
        assert rb298_verdetto(40.0, 100000.0).startswith("ok")

    def test_attenzione(self):
        assert rb298_verdetto(75.0, 50000.0).startswith("attenzione")
        assert rb298_verdetto(70.0, 50000.0).startswith("attenzione")

    def test_zona_rossa(self):
        assert rb298_verdetto(96.0, 5000.0).startswith("zona rossa")
        assert rb298_verdetto(95.0, 5000.0).startswith("zona rossa")

    def test_sforamento(self):
        assert rb298_verdetto(110.0, -5000.0).startswith("sforamento")

    def test_soglie(self):
        assert rb298_verdetto(69.9, 1.0).startswith("ok")
        assert rb298_verdetto(94.9, 1.0).startswith("attenzione")


class TestRb298Integrazione:
    def test_catena_demo(self):
        pos = _demo_pos()
        assert len(pos) == 4
        varb = rb298_var_book(pos, 0.35, 0.99)
        assert varb == pytest.approx(332637.92510122136)
        h = rb298_headroom(varb, DEMO_LIM)
        assert h["headroom"] == pytest.approx(67362.07489877864)
        assert h["utilizzo"] == pytest.approx(83.15948127530534)
        m = rb298_max_nozionale(pos, 0.35, 0.99, 0.028, 0.45, DEMO_LIM)
        assert m == pytest.approx(1504603.4815953365, rel=1e-6)
        vprop = rb298_var_con_candidato(pos, 0.35, 0.99, DEMO_CAND)
        assert vprop == pytest.approx(366738.14339864254)
        assert rb298_verdetto(h["utilizzo"], h["headroom"]) == 'attenzione: limite in avvicinamento'
