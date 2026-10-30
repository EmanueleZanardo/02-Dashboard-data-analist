"""Test tab327 '🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dello Sterling ratio: validatori,
parse equity, episodi di drawdown (picco/trough/profondita/durata/recupero),
CAGR annualizzato, stat con media dei peggiori e Sterling, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh327_num", "mh327_parse_equity", "mh327_episodi", "mh327_cagr",
           "mh327_stat", "mh327_verdetto")

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
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
SERIE_DEMO = '100\n103\n106\n109\n112\n115\n118\n121\n124\n127\n130\n126\n121\n116\n111\n107\n105\n110\n116\n122\n128\n132\n135\n131\n127\n123\n119\n115\n111\n109\n115\n121\n127\n133\n140\n145\n141\n137\n133\n130\n136\n142\n148\n154\n160\n164\n166\n168'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
CAGR = 14.163105494209782
MAXDD = 19.25925925925926
AVG_WORST = 16.27828535874513
STERLING = 0.8700612614952706
N_EP = 3
DEPTHS = [19.25925925925926, 19.230769230769234, 10.344827586206897]
RECUPERI = [True, True, True]
STATO = "sterling ratio MODERATO"
VERDETTO = 'sterling ratio MODERATO: 0.87: il rendimento batte la media dei peggiori drawdown ma con poco margine: gli episodi profondi si ripetono, rivedere sizing e stop-loss prima di scalare.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh327_parse_equity"](SERIE_DEMO)


class TestRegistry327:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 822
        assert TITLE327 in titoli
        assert "tab327" in dvars
        assert "    with tab327:" in src

    def test_titoli_allineati_325_326_327(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab325")] == TITLE325
        assert titoli[dvars.index("tab326")] == TITLE326
        assert titoli[dvars.index("tab327")] == TITLE327

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh327_num"](3.5, "t") == 3.5
        assert _F["mh327_num"](12, "t") == 12.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh327_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh327_parse_equity"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(v > 0.0 for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh327_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        for bad in ("0", "-5"):
            with pytest.raises(ValueError):
                _F["mh327_parse_equity"](
                    "\n".join(["100"] * 29 + [bad]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh327_parse_equity"]("\n".join(["a"] * 30))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh327_parse_equity"](None)

    def test_parse_virgola(self):
        vals = _F["mh327_parse_equity"]("\n".join(["100,5"] * 30))
        assert vals[0] == 100.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["100"] * 30) + "\n\n"
        assert len(_F["mh327_parse_equity"](txt)) == 30


class TestEpisodi:
    def test_demo_conteggio(self):
        epis = _F["mh327_episodi"](_eq_demo())
        assert len(epis) == N_EP == 3

    def test_demo_profondita(self):
        epis = _F["mh327_episodi"](_eq_demo())
        prof = sorted((e["profondita"] for e in epis), reverse=True)
        assert prof == pytest.approx(DEPTHS)
        assert all(p > 0.0 for p in prof)

    def test_demo_recupero(self):
        epis = _F["mh327_episodi"](_eq_demo())
        assert [e["recuperato"] for e in epis] == RECUPERI
        assert all(e["recuperato"] for e in epis)
        for e in epis:
            assert e["i_recupero"] > e["i_trough"] > e["i_picco"]
            assert e["periodi_recupero"] == e["i_recupero"] - e["i_trough"]
            assert e["durata"] == e["i_trough"] - e["i_picco"]
            assert e["v_picco"] > e["v_trough"]

    def test_demo_profondita_formula(self):
        epis = _F["mh327_episodi"](_eq_demo())
        for e in epis:
            att = (e["v_picco"] - e["v_trough"]) / e["v_picco"] * 100.0
            assert e["profondita"] == pytest.approx(att)

    def test_episodio_non_recuperato(self):
        eq = [100.0 + i for i in range(40)] + [120.0] * 8 + [110.0] * 2
        epis = _F["mh327_episodi"](eq)
        assert len(epis) == 1
        assert epis[0]["recuperato"] is False
        assert epis[0]["i_recupero"] is None
        assert epis[0]["periodi_recupero"] is None
        assert epis[0]["profondita"] == pytest.approx(
            (139.0 - 110.0) / 139.0 * 100.0)

    def test_senza_drawdown(self):
        eq = [100.0 + i for i in range(30)]
        assert _F["mh327_episodi"](eq) == []

    def test_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh327_episodi"]([100.0] * 29)


class TestCagr:
    def test_demo(self):
        assert _F["mh327_cagr"](_eq_demo(), 12) == pytest.approx(CAGR / 100.0)

    def test_cagr_scaling(self):
        eq = [100.0, 200.0] + [200.0] * 28
        assert _F["mh327_cagr"](eq, 12) == pytest.approx(2.0 ** (12 / 29) - 1)

    def test_cagr_negativo(self):
        eq = [100.0 - i for i in range(30)]
        assert _F["mh327_cagr"](eq, 12) < 0.0

    def test_cagr_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh327_cagr"](_eq_demo(), 0)


class TestStat:
    def test_stat_demo(self):
        st_ = _F["mh327_stat"](_eq_demo(), 12, 3)
        assert st_["n"] == N == 48
        assert st_["cagr"] == pytest.approx(CAGR)
        assert st_["max_dd"] == pytest.approx(MAXDD)
        assert st_["avg_worst"] == pytest.approx(AVG_WORST)
        assert st_["sterling"] == pytest.approx(STERLING)
        assert st_["n_ep"] == N_EP == 3
        assert len(st_["episodi"]) == 3

    def test_stat_keys(self):
        st_ = _F["mh327_stat"](_eq_demo(), 12, 3)
        for k in ("n", "cagr", "max_dd", "avg_worst", "sterling",
                  "n_ep", "episodi"):
            assert k in st_

    def test_stat_ordinamento_episodi(self):
        st_ = _F["mh327_stat"](_eq_demo(), 12, 3)
        prof = [e["profondita"] for e in st_["episodi"]]
        assert prof == sorted(prof, reverse=True)
        assert st_["max_dd"] == pytest.approx(prof[0])

    def test_stat_k_maggiore_episodi(self):
        st3 = _F["mh327_stat"](_eq_demo(), 12, 3)
        st9 = _F["mh327_stat"](_eq_demo(), 12, 9)
        assert st9["avg_worst"] == pytest.approx(st3["avg_worst"])
        assert st9["sterling"] == pytest.approx(st3["sterling"])

    def test_stat_k1_uguale_calmar(self):
        st_ = _F["mh327_stat"](_eq_demo(), 12, 1)
        assert st_["avg_worst"] == pytest.approx(st_["max_dd"])
        assert st_["sterling"] == pytest.approx(
            st_["cagr"] / st_["max_dd"])

    def test_stat_k_ko(self):
        for bad in (0, 2.5, -1):
            with pytest.raises(ValueError):
                _F["mh327_stat"](_eq_demo(), 12, bad)

    def test_stat_senza_drawdown_inf(self):
        eq = [100.0 + i for i in range(30)]
        st_ = _F["mh327_stat"](eq, 12, 3)
        assert math.isinf(st_["sterling"])
        assert st_["n_ep"] == 0
        assert st_["avg_worst"] == 0.0

    def test_stat_piatta_ko(self):
        with pytest.raises(ValueError):
            _F["mh327_stat"]([100.0] * 30, 12, 3)


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh327_verdetto"](2.0, 3)
        assert v.startswith("sterling ratio ECCELLENTE")

    def test_verdetto_soglia_eccellente(self):
        v = _F["mh327_verdetto"](1.5, 3)
        assert v.startswith("sterling ratio ECCELLENTE")

    def test_verdetto_inf(self):
        v = _F["mh327_verdetto"](float("inf"), 0)
        assert v.startswith("sterling ratio ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh327_verdetto"](1.0, 3)
        assert v.startswith("sterling ratio MODERATO")

    def test_verdetto_soglia_moderato(self):
        v = _F["mh327_verdetto"](0.7, 3)
        assert v.startswith("sterling ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh327_verdetto"](0.5, 3)
        assert v.startswith("sterling ratio DEBOLE")

    def test_verdetto_un_solo_episodio(self):
        v = _F["mh327_verdetto"](1.0, 1)
        assert v.startswith("sterling ratio MODERATO")
        assert "Calmar" in v

    def test_verdetto_demo(self):
        st_ = _F["mh327_stat"](_eq_demo(), 12, 3)
        v = _F["mh327_verdetto"](st_["sterling"], st_["n_ep"])
        assert v == VERDETTO
        assert v.startswith(STATO)
