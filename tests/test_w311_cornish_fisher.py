"""Test tab311 '📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab di rischio precedenti, piu' la matematica di Cornish-Fisher:
quantile lato perdite, segno della skew, neutralita' a momenti nulli, gap
VaR CF vs normale, pesi di portafoglio, verdetto a 6 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("cf311_num", "cf311_conf", "cf311_corr", "cf311_skew",
           "cf311_kurt", "cf311_parse_book", "cf311_norm_ppf", "cf311_zcf",
           "cf311_pesi", "cf311_sigmas", "cf311_var_normale",
           "cf311_risultato", "cf311_verdetto")

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
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
BOOK_DEMO = ("Cal-28 Baseload power;2500000;18,5;-0,8;4,0;power\n"
             "Q3-28 Peak power;1200000;26,0;-1,2;6,0;power\n"
             "TTF Gas Cal-28;1800000;22,0;-0,5;3,0;gas\n"
             "EUA Carbon Dec-28;700000;31,0;-0,3;2,0;carbon")
RHO_DEMO = 0.35
CONF_DEMO = 99
SOGLIA_DEMO = 0.25

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
VAR = 2336394.1500722347
VAR_CF = 3583686.0773059446
GAP = 1247291.92723371
GAP_PCT = 0.5338533856520515
Z = 2.326347874040838
ZCF = 3.5682765628019917
SKEW = -0.7338709677419355
KURT = 3.870967741935484
STATO = "sottostima grave"
VERDETTO = 'sottostima grave (53.4%): il VaR normale ignora le code grasse: mancano 1,247,292 euro di cuscinetto: ricalibrare i limiti sul VaR corretto'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry311:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 663
        assert TITLE311 in titoli
        assert "tab311" in dvars
        assert "    with tab311:" in src

    def test_titoli_allineati_309_310_311(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab309")] == TITLE309
        assert titoli[dvars.index("tab310")] == TITLE310
        assert titoli[dvars.index("tab311")] == TITLE311

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_conf_ok(self):
        assert _F["cf311_conf"](99) == 99

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["cf311_conf"](97)

    def test_skew_ok(self):
        assert _F["cf311_skew"](-5.0) == -5.0
        assert _F["cf311_skew"](5.0) == 5.0

    def test_skew_fuori_range(self):
        with pytest.raises(ValueError):
            _F["cf311_skew"](5.1)
        with pytest.raises(ValueError):
            _F["cf311_skew"](-5.1)

    def test_kurt_ok(self):
        assert _F["cf311_kurt"](30.0) == 30.0
        assert _F["cf311_kurt"](-1.5) == -1.5

    def test_kurt_fuori_range(self):
        with pytest.raises(ValueError):
            _F["cf311_kurt"](30.1)
        with pytest.raises(ValueError):
            _F["cf311_kurt"](-1.6)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["cf311_num"](True, "x")

    def test_parse_book_ok(self):
        book = _F["cf311_parse_book"](BOOK_DEMO)
        assert len(book) == 4
        assert book[0] == ("Cal-28 Baseload power", 2500000.0, 0.185,
                           -0.8, 4.0, "power")

    def test_parse_book_5campi_ko(self):
        with pytest.raises(ValueError):
            _F["cf311_parse_book"]("nome;1000;20,0;-0,5;2,0")

    def test_parse_book_skew_testo_ko(self):
        with pytest.raises(ValueError):
            _F["cf311_parse_book"]("nome;1000;20,0;alta;2,0;power")

    def test_parse_book_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["cf311_parse_book"]("   \n  ")


class TestMatematica:
    def test_ppf_99(self):
        assert abs(_F["cf311_norm_ppf"](0.99) - 2.32634787404084) < 1e-3

    def test_zcf_neutro(self):
        z = 1.6448536269514722
        assert _F["cf311_zcf"](z, 0.0, 0.0) == pytest.approx(z)

    def test_zcf_skew_neg_aumenta(self):
        # skew rendimenti negativa = coda perdite grassa -> quantile sale
        z = 1.6448536269514722
        assert _F["cf311_zcf"](z, -1.0, 0.0) > z

    def test_zcf_skew_pos_diminuisce(self):
        z = 1.6448536269514722
        assert _F["cf311_zcf"](z, 1.0, 0.0) < z

    def test_zcf_valore_noto(self):
        z, s, k = 1.6448536269514722, -0.5, 2.0
        att = (z - (z * z - 1.0) * s / 6.0
               + (z ** 3 - 3.0 * z) * k / 24.0
               - (2.0 * z ** 3 - 5.0 * z) * s * s / 36.0)
        assert _F["cf311_zcf"](z, s, k) == pytest.approx(att, rel=1e-12)

    def test_var_cf_coerente(self):
        book = _F["cf311_parse_book"](BOOK_DEMO)
        ris = _F["cf311_risultato"](book, RHO_DEMO, CONF_DEMO)
        _, s2 = _F["cf311_sigmas"](book, RHO_DEMO)
        sd = math.sqrt(s2)
        assert ris["var_cf"] - ris["var"] == pytest.approx(
            (ris["zcf"] - ris["z"]) * sd, rel=1e-9)
        assert ris["gap"] == pytest.approx(ris["var_cf"] - ris["var"])
        assert ris["gap_pct"] == pytest.approx(ris["gap"] / ris["var"])
        assert len(ris["dettaglio"]) == 4
        assert ris["var"] == pytest.approx(
            _F["cf311_var_normale"](book, RHO_DEMO, CONF_DEMO), rel=1e-12)

    def test_pesi_ponderati(self):
        book = [("a", 3000.0, 0.2, -1.0, 4.0, "x"),
                ("b", 1000.0, 0.2, 1.0, 0.0, "y")]
        s, k = _F["cf311_pesi"](book)
        assert s == pytest.approx((-3000.0 + 1000.0) / 4000.0)
        assert k == pytest.approx((12000.0 + 0.0) / 4000.0)

    def test_demo(self):
        book = _F["cf311_parse_book"](BOOK_DEMO)
        ris = _F["cf311_risultato"](book, RHO_DEMO, CONF_DEMO)
        assert ris["var"] == pytest.approx(VAR, rel=1e-9)
        assert ris["var_cf"] == pytest.approx(VAR_CF, rel=1e-9)
        assert ris["gap"] == pytest.approx(GAP, rel=1e-9)
        assert ris["gap_pct"] == pytest.approx(GAP_PCT, rel=1e-9)
        assert ris["z"] == pytest.approx(Z, rel=1e-9)
        assert ris["zcf"] == pytest.approx(ZCF, rel=1e-9)
        assert ris["skew"] == pytest.approx(SKEW, rel=1e-9)
        assert ris["kurt"] == pytest.approx(KURT, rel=1e-9)
        assert ris["gap"] > 0.0
        assert ris["gap_pct"] >= SOGLIA_DEMO


def _ris(z=1.6449, zcf=1.8, gap=100000.0, var=1000000.0):
    return {"z": z, "zcf": zcf, "gap": gap, "var": var,
            "gap_pct": gap / var, "var_cf": var + gap,
            "skew": -0.5, "kurt": 3.0, "dettaglio": []}


class TestVerdetto:
    def test_inaffidabile(self):
        assert _F["cf311_verdetto"](
            _ris(zcf=0.4), SOGLIA_DEMO).startswith("espansione inaffidabile")

    def test_inaffidabile_negativo(self):
        assert _F["cf311_verdetto"](
            _ris(zcf=-0.1), SOGLIA_DEMO).startswith("espansione inaffidabile")

    def test_grave(self):
        assert _F["cf311_verdetto"](
            _ris(gap=300000.0), SOGLIA_DEMO).startswith("sottostima grave")

    def test_materiale(self):
        assert _F["cf311_verdetto"](
            _ris(gap=150000.0), SOGLIA_DEMO).startswith("sottostima materiale")

    def test_moderata(self):
        assert _F["cf311_verdetto"](
            _ris(gap=50000.0), SOGLIA_DEMO).startswith("sottostima moderata")

    def test_quasi_normali(self):
        assert _F["cf311_verdetto"](
            _ris(gap=10000.0), SOGLIA_DEMO).startswith("code quasi normali")
        assert _F["cf311_verdetto"](
            _ris(gap=-10000.0), SOGLIA_DEMO).startswith("code quasi normali")

    def test_conservativo(self):
        assert _F["cf311_verdetto"](
            _ris(gap=-50000.0), SOGLIA_DEMO).startswith(
            "VaR normale conservativo")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith(STATO)

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["cf311_verdetto"](_ris(), 0.0)
        with pytest.raises(ValueError):
            _F["cf311_verdetto"](_ris(), 1.0)
