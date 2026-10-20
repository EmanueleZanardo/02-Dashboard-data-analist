"""Test tab318 '🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della copula t-Student: validatori,
CDF t via Simpson, tail dependence, simulazione equicorrelata gaussiana vs t
(deterministica), VaR/ES, breccia congiunta, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh318_num", "mh318_conf", "mh318_rho", "mh318_nu", "mh318_nsim",
           "mh318_parse_book", "mh318_norm_ppf", "mh318_t_cdf",
           "mh318_tail_dep", "mh318_rng", "mh318_quantile", "mh318_simula",
           "mh318_risultato", "mh318_verdetto")

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
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
BOOK_DEMO = 'Gas TTF front-month;2500000;3,2;gas\nPower DE baseload Q1-27;1800000;2,8;power\nCO2 EUA Dic-26;900000;2,5;co2\nSpread PSV-TTF;600000;4,1;basis\nSpark spread CCGT 55%;1200000;3,6;power\nCarbone API2 ARA;700000;3,0;coal'
Q_DEMO = 99.0
RHO_DEMO = 0.5
NU_DEMO = 5
NSIM_DEMO = 10000

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_POS = 6
VAR_G = 438132.4632483595
ES_G = 514365.47922748973
VAR_T = 652930.2451757772
ES_T = 839821.5846891706
GAP = 0.4902576274190794
GAP_EUR = 214797.78192741773
LAMBDA = 0.207031233606822
JOINT = 0.049
STANDALONE = [186107.82992326727, 117247.93285165836, 52342.82716591892, 57228.15770140467, 100498.22815856434, 48853.30535485766]
STATO = "code congiunte pericolose"
VERDETTO = 'code congiunte pericolose: il VaR t-Student supera del 49.0% quello gaussiano (652,930 vs 438,132 euro): in stress le code si muovono insieme, aumenta il buffer.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh318_risultato"](BOOK_DEMO, Q_DEMO, RHO_DEMO, NU_DEMO,
                                 NSIM_DEMO)


class TestRegistry318:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 580
        assert TITLE318 in titoli
        assert "tab318" in dvars
        assert "    with tab318:" in src

    def test_titoli_allineati_316_317_318(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab316")] == TITLE316
        assert titoli[dvars.index("tab317")] == TITLE317
        assert titoli[dvars.index("tab318")] == TITLE318

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh318_conf"](99.0) == pytest.approx(0.01)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh318_conf"](97.5)

    def test_rho_ok(self):
        assert _F["mh318_rho"](0.5) == 0.5
        assert _F["mh318_rho"](0.0) == 0.0
        assert _F["mh318_rho"](0.99) == 0.99

    def test_rho_ko(self):
        for bad in (-0.1, 1.0, 1.5):
            with pytest.raises(ValueError):
                _F["mh318_rho"](bad)

    def test_nu_ok(self):
        assert _F["mh318_nu"](5) == 5
        assert _F["mh318_nu"](5.0) == 5

    def test_nu_ko(self):
        for bad in (1, 31, 4.5):
            with pytest.raises(ValueError):
                _F["mh318_nu"](bad)

    def test_nsim_ko(self):
        for bad in (999, 50001, 10000.5):
            with pytest.raises(ValueError):
                _F["mh318_nsim"](bad)

    def test_parse_book_ok(self):
        b = _F["mh318_parse_book"](BOOK_DEMO)
        assert len(b) == 6
        assert b[0]["nome"] == "Gas TTF front-month"
        assert b[0]["nozionale"] == 2500000.0
        assert b[0]["vol"] == pytest.approx(0.032)
        assert b[0]["segmento"] == "gas"

    def test_parse_book_ko(self):
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("solo una posizione;1000;2;gas")
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("a;1000;2\nb;2000;3;power")
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("a;-1000;2;gas\nb;2000;3;power")
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("a;1000;0;gas\nb;2000;3;power")

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x"):
            with pytest.raises(ValueError):
                _F["mh318_num"](bad, "t")


class TestTCdf:
    def test_zero(self):
        assert _F["mh318_t_cdf"](0.0, 5.0) == 0.5

    def test_simmetria(self):
        assert _F["mh318_t_cdf"](-1.7, 5.0) == pytest.approx(
            1.0 - _F["mh318_t_cdf"](1.7, 5.0))

    def test_valore_noto(self):
        # t_{30, 0.975} = 2.0423 (valore critico noto)
        assert _F["mh318_t_cdf"](2.042, 30.0) == pytest.approx(0.975, abs=2e-3)

    def test_monotonia(self):
        c = _F["mh318_t_cdf"]
        assert c(-3.0, 5.0) < c(-1.0, 5.0) < 0.5 < c(1.0, 5.0) < c(3.0, 5.0)

    def test_converge_normale(self):
        # nu grande -> CDF piu' vicina alla normale (convergenza monotona)
        import statistics
        phi = statistics.NormalDist().cdf(1.0)
        c = _F["mh318_t_cdf"]
        assert abs(c(1.0, 30.0) - phi) < abs(c(1.0, 5.0) - phi)
        assert abs(c(1.0, 30.0) - phi) < 0.01


class TestTailDep:
    def test_cresce_in_rho(self):
        td = _F["mh318_tail_dep"]
        assert td(0.3, 5.0) < td(0.5, 5.0) < td(0.9, 5.0)

    def test_decresce_in_nu(self):
        td = _F["mh318_tail_dep"]
        assert td(0.5, 3.0) > td(0.5, 5.0) > td(0.5, 30.0)

    def test_valori(self):
        td = _F["mh318_tail_dep"]
        assert td(0.9, 3.0) > 0.5
        assert td(0.5, 30.0) < 0.05
        assert td(0.0, 5.0) < 0.06
        assert td(0.5, 5.0) == pytest.approx(LAMBDA)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh318_tail_dep"](1.0, 5.0)
        with pytest.raises(ValueError):
            _F["mh318_tail_dep"](0.5, 1.0)


class TestSimula:
    def _book(self):
        return _F["mh318_parse_book"](BOOK_DEMO)

    def test_determinismo(self):
        b = self._book()
        s1 = _F["mh318_simula"](b, 0.5, 5, 2000, 99.0)
        s2 = _F["mh318_simula"](b, 0.5, 5, 2000, 99.0)
        assert s1["perdite_g"] == s2["perdite_g"]
        assert s1["perdite_t"] == s2["perdite_t"]
        assert s1["joint_breach"] == s2["joint_breach"]

    def test_lunghezze_e_range(self):
        b = self._book()
        s = _F["mh318_simula"](b, 0.5, 5, 2000, 99.0)
        assert len(s["perdite_g"]) == len(s["perdite_t"]) == 2000
        assert len(s["standalone"]) == 6
        assert 0.0 <= s["joint_breach"] <= 1.0

    def test_t_piu_grassa_di_gauss(self):
        b = self._book()
        s = _F["mh318_simula"](b, 0.5, 5, NSIM_DEMO, 99.0)
        q = _F["mh318_quantile"]
        assert q(s["perdite_t"], 0.99) > q(s["perdite_g"], 0.99)

    def test_diversificazione_rho_zero(self):
        b = self._book()
        s = _F["mh318_simula"](b, 0.0, 5, 5000, 99.0)
        q = _F["mh318_quantile"]
        assert q(s["perdite_g"], 0.99) < sum(s["standalone"])

    def test_rng_deterministico(self):
        u1, u2 = _F["mh318_rng"](20261008), _F["mh318_rng"](20261008)
        assert [u1() for _ in range(5)] == [u2() for _ in range(5)]
        assert all(0.0 < u1() < 1.0 for _ in range(10))


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n_pos"] == N_POS == 6
        assert ris["q"] == Q_DEMO
        assert ris["rho"] == RHO_DEMO
        assert ris["nu"] == NU_DEMO
        assert ris["nsim"] == NSIM_DEMO
        assert ris["var_g"] == VAR_G
        assert ris["es_g"] == ES_G
        assert ris["var_t"] == VAR_T
        assert ris["es_t"] == ES_T
        assert ris["gap"] == GAP
        assert ris["gap_eur"] == GAP_EUR
        assert ris["lambda"] == LAMBDA
        assert ris["joint"] == JOINT
        assert ris["standalone"] == STANDALONE
        assert ris["var_t"] > ris["var_g"] > 0.0
        assert ris["es_t"] >= ris["var_t"]
        assert ris["gap"] == pytest.approx(
            (ris["var_t"] - ris["var_g"]) / ris["var_g"])

    def test_nomi_segmenti(self):
        ris = _ris_demo()
        assert ris["nomi"][0] == "Gas TTF front-month"
        assert ris["segmenti"][3] == "basis"
        assert len(ris["perdite_g"]) == NSIM_DEMO


class TestVerdetto:
    def _base(self, **kw):
        ris = _ris_demo()
        ris.update(kw)
        return ris

    def test_verdetto_demo(self):
        assert _F["mh318_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_pericolose(self):
        v = _F["mh318_verdetto"](
            self._base(gap=0.49, var_t=650000.0, var_g=438000.0))
        assert v.startswith("code congiunte pericolose")

    def test_stato_materiali(self):
        v = _F["mh318_verdetto"](
            self._base(gap=0.15, var_t=500000.0, var_g=435000.0, joint=0.01))
        assert v.startswith("code congiunte materiali")

    def test_stato_breccia(self):
        v = _F["mh318_verdetto"](self._base(gap=0.05, joint=0.08))
        assert v.startswith("breccia congiunta frequente")

    def test_stato_modesta(self):
        v = _F["mh318_verdetto"](self._base(gap=0.05, joint=0.01))
        assert v.startswith("differenza modesta")

    def test_stato_nessuna(self):
        v = _F["mh318_verdetto"](self._base(gap=0.01, joint=0.01))
        assert v.startswith("nessuna differenza apprezzabile")
