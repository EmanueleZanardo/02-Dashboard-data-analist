"""Test tab324 'Ω📊 Omega ratio: oltre Sharpe e Sortino': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dell'Omega ratio: validatori,
parse rendimenti, omega(T) con gestione inf/degenere, statistiche di base,
curva su 21 soglie, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh324_num", "mh324_parse_serie", "mh324_omega", "mh324_stat",
           "mh324_curva", "mh324_verdetto")

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
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
SERIE_DEMO = '1.2\n-0.8\n2.1\n0.5\n-1.5\n3.2\n0.8\n-2.2\n1.7\n5.4\n0.3\n-1.1\n2.6\n1.1\n-0.6\n4.1\n0.9\n-1.8\n2.3\n0.4\n6.2\n-0.9\n1.5\n2.8\n-2.5\n1.0\n0.7\n-1.2\n3.6\n1.4\n-0.4\n2.0\n0.6\n-1.6\n4.8\n1.9'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 36
MEDIA = 1.0694444444444444
VOL = 2.1293620029676825
SHARPE = 0.5022370282525772
OMEGA0 = 3.636986301369863
MINR = -2.5
MAXR = 6.2
PCTPOS = 69.44444444444444
STATO = "asimmetria FORTEMENTE positiva"
VERDETTO = "asimmetria FORTEMENTE positiva: Omega(0) 3.64 (Sharpe 0.50): i guadagni sopra lo zero dominano le perdite, la strategia ha code destre grasse: il rischio di coda e' contenuto rispetto al potenziale."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _rets_demo():
    return _F["mh324_parse_serie"](SERIE_DEMO)


class TestRegistry324:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 627
        assert TITLE324 in titoli
        assert "tab324" in dvars
        assert "    with tab324:" in src

    def test_titoli_allineati_322_323_324(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab322")] == TITLE322
        assert titoli[dvars.index("tab323")] == TITLE323
        assert titoli[dvars.index("tab324")] == TITLE324

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh324_num"](3.5, "t") == 3.5
        assert _F["mh324_num"](0, "t") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh324_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh324_parse_serie"](SERIE_DEMO)
        assert len(vals) == N == 36
        assert all(isinstance(v, float) for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh324_parse_serie"]("\n".join(["1.0"] * 19))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh324_parse_serie"]("\n".join(["a"] * 20))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh324_parse_serie"](None)

    def test_parse_virgola(self):
        vals = _F["mh324_parse_serie"]("\n".join(["1,5"] * 20))
        assert vals[0] == 1.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["1.0"] * 20) + "\n\n"
        assert len(_F["mh324_parse_serie"](txt)) == 20


class TestOmega:
    def test_omega_simmetrico(self):
        assert _F["mh324_omega"]([-2.0, -1.0, 1.0, 2.0], 0.0) == pytest.approx(1.0)

    def test_omega_tutti_positivi_inf(self):
        assert math.isinf(_F["mh324_omega"]([1.0, 2.0, 3.0], 0.0))

    def test_omega_degenere_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_omega"]([0.0] * 20, 0.0)

    def test_omega_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_omega"]([], 0.0)

    def test_omega_non_crescente_in_soglia(self):
        rets = _rets_demo()
        o1 = _F["mh324_omega"](rets, -2.0)
        o2 = _F["mh324_omega"](rets, 0.0)
        o3 = _F["mh324_omega"](rets, 2.0)
        assert o1 >= o2 >= o3

    def test_omega_demo(self):
        assert _F["mh324_omega"](_rets_demo(), 0.0) == pytest.approx(OMEGA0)
        assert OMEGA0 > 1.0
        assert not math.isinf(OMEGA0)


class TestStat:
    def test_stat_demo(self):
        st_ = _F["mh324_stat"](_rets_demo())
        assert st_["n"] == N == 36
        assert st_["media"] == pytest.approx(MEDIA)
        assert st_["vol"] == pytest.approx(VOL)
        assert st_["sharpe"] == pytest.approx(SHARPE)
        assert st_["min"] == pytest.approx(MINR)
        assert st_["max"] == pytest.approx(MAXR)
        assert st_["pct_pos"] == pytest.approx(PCTPOS)
        assert st_["omega0"] == pytest.approx(OMEGA0)

    def test_stat_keys(self):
        st_ = _F["mh324_stat"](_rets_demo())
        for k in ("n", "media", "vol", "sharpe", "min", "max",
                  "pct_pos", "omega0"):
            assert k in st_

    def test_stat_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_stat"]([1.0] * 19)

    def test_pct_pos_range(self):
        assert 0.0 < PCTPOS < 100.0


class TestCurva:
    def test_curva_punti(self):
        cur = _F["mh324_curva"](_rets_demo())
        assert len(cur) == 21
        assert cur[0][0] == pytest.approx(MINR)
        assert cur[-1][0] == pytest.approx(MAXR)

    def test_curva_estremi(self):
        cur = _F["mh324_curva"](_rets_demo())
        assert math.isinf(cur[0][1])
        assert cur[-1][1] == pytest.approx(0.0)

    def test_curva_non_crescente(self):
        cur = _F["mh324_curva"](_rets_demo())
        vals = [v for _, v in cur if not math.isinf(v)]
        assert all(b <= a + 1e-12 for a, b in zip(vals, vals[1:]))

    def test_curva_costante_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_curva"]([2.0] * 20)

    def test_curva_pochi_punti_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_curva"](_rets_demo(), n_punti=2)


class TestVerdetto:
    def test_verdetto_forte(self):
        v = _F["mh324_verdetto"](3.6, 0.5)
        assert v.startswith("asimmetria FORTEMENTE positiva")

    def test_verdetto_inf(self):
        v = _F["mh324_verdetto"](float("inf"), 1.2)
        assert v.startswith("asimmetria FORTEMENTE positiva")

    def test_verdetto_moderata(self):
        v = _F["mh324_verdetto"](1.2, 0.3)
        assert v.startswith("asimmetria positiva MODERATA")

    def test_verdetto_negativa(self):
        v = _F["mh324_verdetto"](0.7, -0.2)
        assert v.startswith("coda negativa DOMINANTE")

    def test_verdetto_demo(self):
        st_ = _F["mh324_stat"](_rets_demo())
        v = _F["mh324_verdetto"](st_["omega0"], st_["sharpe"])
        assert v == VERDETTO
        assert v.startswith(STATO)
