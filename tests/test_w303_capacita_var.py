"""Test tab303 '🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab303. Capacita' VaR: il max nozionale di un
candidato (vol + correlazione al book) con VaR(book+x) <= limite, soluzione
esatta dell'equazione quadratica (follow-up del filone rischio
tab297 marginal VaR + tab298 limite VaR).
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cf303_num", "cf303_conf", "cf303_corr", "cf303_limite",
          "cf303_parse_book", "cf303_norm_cdf", "cf303_norm_ppf",
          "cf303_sigma2_book", "cf303_var_book", "cf303_capacita",
          "cf303_curva", "cf303_verdetto")
cf303_num = _F["cf303_num"]
cf303_conf = _F["cf303_conf"]
cf303_corr = _F["cf303_corr"]
cf303_limite = _F["cf303_limite"]
cf303_parse_book = _F["cf303_parse_book"]
cf303_norm_cdf = _F["cf303_norm_cdf"]
cf303_norm_ppf = _F["cf303_norm_ppf"]
cf303_sigma2_book = _F["cf303_sigma2_book"]
cf303_var_book = _F["cf303_var_book"]
cf303_capacita = _F["cf303_capacita"]
cf303_curva = _F["cf303_curva"]
cf303_verdetto = _F["cf303_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"

BOOK_TXT = ("Cal-28 Baseload power;2500000;18,5\n"
            "Q3-28 Peak power;1200000;26,0\n"
            "TTF Gas Cal-28;1800000;22,0\n"
            "EUA Carbon Dec-28;700000;31,0")
BOOK = [("Cal-28 Baseload power", 2500000.0, 0.185),
        ("Q3-28 Peak power", 1200000.0, 0.26),
        ("TTF Gas Cal-28", 1800000.0, 0.22),
        ("EUA Carbon Dec-28", 700000.0, 0.31)]
RHO = 0.35
CONF = 95
LIMITE = 2200000.0
NOME_CAND = "Nuovo Cal-29 Baseload"
VNEW = 0.21
RHO_CB = 0.35
VAR_BOOK = 1651956.8868516753
UTIL = 75.08894940234889
HEADROOM = 548043.1131483247
CAP = 2487574.986307384
Z95 = 1.6448536269514715
SIGMA2B = 1008655600000.0
CAP_RHO0 = 4206312.354565912
NOZ_TOT = 6200000.0
VERDETTO = "capacita' ampia: puoi aggiungere fino a 2,487,575 euro di 'Nuovo Cal-29 Baseload' restando sotto il limite"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab303:
    def test_tab303_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 451
        assert TITLE303 in titoli
        assert "tab303" in dvars
        assert "tab303" in withs
        assert titoli[dvars.index("tab303")] == TITLE303
        assert titoli[-1] == TITLE451
        assert dvars[-1] == "tab451"
        keys = re.findall(r'key="(st303_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_301_302_303(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab301")] == TITLE301
        assert titoli[dvars.index("tab302")] == TITLE302
        assert titoli[dvars.index("tab303")] == TITLE303


class TestCf303Validatori:
    def test_num_ok(self):
        assert cf303_num(3, "x") == 3.0
        assert cf303_num(2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                cf303_num(bad, "x")

    def test_conf(self):
        assert cf303_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                cf303_conf(bad)

    def test_corr(self):
        assert cf303_corr(1.0) == 1.0
        assert cf303_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                cf303_corr(bad)

    def test_limite(self):
        assert cf303_limite(100.0) == 100.0
        for bad in (0.0, -5.0):
            with pytest.raises(ValueError):
                cf303_limite(bad)


class TestCf303Parse:
    def test_demo(self):
        book = cf303_parse_book(BOOK_TXT)
        assert book == BOOK

    def test_righe_vuote(self):
        book = cf303_parse_book("\n" + BOOK_TXT + "\n\n")
        assert len(book) == 4

    def test_formato_ko(self):
        for bad in ("", "   ", "solo;due", "a;b;c;d", ";100;10",
                    "x;-100;10", "x;100;-5", "x;abc;10", 123):
            with pytest.raises(ValueError):
                cf303_parse_book(bad)


class TestCf303Norm:
    def test_ppf95(self):
        assert cf303_norm_ppf(0.95) == pytest.approx(1.6448536, abs=1e-6)
        assert cf303_norm_ppf(0.95) == pytest.approx(Z95, abs=1e-9)

    def test_ppf_simmetria(self):
        assert cf303_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
        assert cf303_norm_ppf(0.05) == pytest.approx(-Z95, abs=1e-9)

    def test_cdf(self):
        assert cf303_norm_cdf(0.0) == 0.5
        assert cf303_norm_cdf(Z95) == pytest.approx(0.95, abs=1e-9)

    def test_ppf_ko(self):
        for bad in (0.0, 1.0, -0.1):
            with pytest.raises(ValueError):
                cf303_norm_ppf(bad)


class TestCf303Varianza:
    def test_singola(self):
        b = [("A", 1000.0, 0.2)]
        assert cf303_sigma2_book(b, 0.5) == pytest.approx(200.0 ** 2)

    def test_rho1(self):
        s1, s2 = 1000.0 * 0.2, 500.0 * 0.3
        assert cf303_sigma2_book(
            [("A", 1000.0, 0.2), ("B", 500.0, 0.3)], 1.0) == pytest.approx(
            (s1 + s2) ** 2)

    def test_rho0(self):
        s1, s2 = 1000.0 * 0.2, 500.0 * 0.3
        assert cf303_sigma2_book(
            [("A", 1000.0, 0.2), ("B", 500.0, 0.3)], 0.0) == pytest.approx(
            s1 ** 2 + s2 ** 2)

    def test_demo(self):
        assert cf303_sigma2_book(BOOK, RHO) == SIGMA2B

    def test_var_book(self):
        assert cf303_var_book(BOOK, RHO, CONF) == VAR_BOOK
        assert cf303_var_book(BOOK, RHO, CONF) == pytest.approx(
            Z95 * math.sqrt(SIGMA2B))


class TestCf303Capacita:
    def test_demo(self):
        c = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, RHO_CB)
        assert c["var_attuale"] == VAR_BOOK
        assert c["utilizzo_pct"] == UTIL
        assert c["headroom_eur"] == HEADROOM
        assert c["cap_noz_eur"] == CAP
        assert c["noz_tot_book"] == NOZ_TOT
        assert c["var_a_cap"] == LIMITE

    def test_analitica_rho_cb_zero(self):
        c = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, 0.0)
        atteso = math.sqrt((LIMITE / Z95) ** 2 - SIGMA2B) / VNEW
        assert c["cap_noz_eur"] == pytest.approx(atteso, rel=1e-9)
        assert c["cap_noz_eur"] == CAP_RHO0

    def test_correlazione_riduce_capacita(self):
        c_hi = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, 0.9)
        c_lo = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, -0.5)
        assert c_hi["cap_noz_eur"] < CAP < c_lo["cap_noz_eur"]

    def test_over_limite(self):
        c = cf303_capacita(BOOK, RHO, CONF, VAR_BOOK * 0.5, VNEW, RHO_CB)
        assert c["cap_noz_eur"] == 0.0
        assert c["var_a_cap"] == c["var_attuale"]
        assert c["headroom_eur"] < 0.0

    def test_vol_zero(self):
        c = cf303_capacita(BOOK, RHO, CONF, LIMITE, 0.0, RHO_CB)
        assert math.isinf(c["cap_noz_eur"])
        assert c["var_a_cap"] == c["var_attuale"]

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            cf303_capacita(BOOK, RHO, CONF, LIMITE, -0.1, RHO_CB)


class TestCf303Curva:
    def test_struttura(self):
        cur = cf303_curva(BOOK, RHO, CONF, LIMITE, VNEW, RHO_CB)
        assert len(cur) == 21
        assert cur[0]["x_noz_eur"] == 0.0
        assert cur[0]["var_eur"] == pytest.approx(VAR_BOOK)
        assert cur[-1]["x_noz_eur"] == pytest.approx(1.5 * CAP)

    def test_monotona_con_rho_positiva(self):
        cur = cf303_curva(BOOK, RHO, CONF, LIMITE, VNEW, RHO_CB)
        vals = [r["var_eur"] for r in cur]
        assert all(b >= a for a, b in zip(vals, vals[1:]))


class TestCf303Verdetto:
    def test_demo(self):
        assert cf303_verdetto(CAP, BOOK, VAR_BOOK, LIMITE, NOME_CAND) == VERDETTO
        assert VERDETTO.startswith("capacita' ampia")
        assert NOME_CAND in VERDETTO

    def test_nessuna(self):
        v = cf303_verdetto(0.0, BOOK, VAR_BOOK, VAR_BOOK * 0.5, NOME_CAND)
        assert v.startswith("nessuna capacita'")

    def test_ristretta(self):
        lim = VAR_BOOK * 1.0005
        c = cf303_capacita(BOOK, RHO, CONF, lim, VNEW, RHO_CB)
        v = cf303_verdetto(c["cap_noz_eur"], BOOK, VAR_BOOK, lim, NOME_CAND)
        assert v.startswith("capacita' ristretta")

    def test_illimitata(self):
        v = cf303_verdetto(float("inf"), BOOK, VAR_BOOK, LIMITE, NOME_CAND)
        assert v.startswith("capacita' illimitata")
