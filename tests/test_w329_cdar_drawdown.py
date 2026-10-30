"""Test tab329 '🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del CDaR: validatori, parse equity,
serie dei drawdown, DaR/CDaR (quantile e media di coda), CAGR annualizzato
e verdetto a 3 stati sulla copertura CDaR vs CAGR.
"""
import math
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh329_num", "mh329_parse_equity", "mh329_drawdown", "mh329_cagr",
           "mh329_cdar", "mh329_verdetto")

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
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
SERIE_DEMO = '100\n103\n106\n109\n112\n115\n118\n119\n120\n116\n111\n106\n101\n97\n94\n100\n106\n112\n118\n124\n130\n126\n121\n117\n115\n114\n118\n123\n128\n133\n138\n142\n139\n136\n133\n130\n134\n138\n142\n146\n149\n152\n154\n156\n158\n160\n162\n164'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
CAGR = 13.462865756360042
DAR95 = 16.374999999999996
CDAR95 = 19.166666666666664
MAXDD = 21.666666666666668
N_TAIL95 = 3
DAR99 = 20.49166666666667
CDAR99 = 21.666666666666668
N_TAIL99 = 1
STATO = "cdar MODERATO"
VERDETTO = ("cdar MODERATO: 19.17%: il rendimento (+13.46%) copre a malapena "
            "la coda media dei drawdown (0.7x): un episodio di coda piu' "
            "profondo erode il margine, rivedere sizing e stop-loss prima "
            "di scalare.")


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh329_parse_equity"](SERIE_DEMO)


class TestRegistry329:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 817
        assert TITLE329 in titoli
        assert "tab329" in dvars
        assert "    with tab329:" in src

    def test_titoli_allineati_326_327_328_329(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab326")] == TITLE326
        assert titoli[dvars.index("tab327")] == TITLE327
        assert titoli[dvars.index("tab328")] == TITLE328
        assert titoli[dvars.index("tab329")] == TITLE329

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh329_num"](3.5, "t") == 3.5
        assert _F["mh329_num"](12, "t") == 12.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh329_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh329_parse_equity"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(v > 0.0 for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh329_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        for bad in ("0", "-5"):
            with pytest.raises(ValueError):
                _F["mh329_parse_equity"](
                    "\n".join(["100"] * 29 + [bad]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh329_parse_equity"]("\n".join(["a"] * 30))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh329_parse_equity"](None)

    def test_parse_virgola(self):
        vals = _F["mh329_parse_equity"]("\n".join(["100,5"] * 30))
        assert vals[0] == 100.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["100"] * 30) + "\n\n"
        assert len(_F["mh329_parse_equity"](txt)) == 30


class TestDrawdown:
    def test_demo_non_negativo(self):
        dd = _F["mh329_drawdown"](_eq_demo())
        assert len(dd) == N == 48
        assert all(d >= 0.0 for d in dd)

    def test_demo_partenza_zero(self):
        dd = _F["mh329_drawdown"](_eq_demo())
        assert dd[0] == 0.0

    def test_demo_max(self):
        dd = _F["mh329_drawdown"](_eq_demo())
        assert float(np.max(dd)) * 100.0 == pytest.approx(MAXDD)
        assert int(np.argmax(dd)) == 14

    def test_demo_formula(self):
        eq = _eq_demo()
        dd = _F["mh329_drawdown"](eq)
        peak = np.maximum.accumulate(eq)
        assert dd == pytest.approx((peak - eq) / peak)

    def test_senza_drawdown(self):
        dd = _F["mh329_drawdown"](np.array([100.0 + i for i in range(30)]))
        assert all(d == 0.0 for d in dd)

    def test_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh329_drawdown"]([100.0] * 29)


class TestCdar:
    def test_demo_95(self):
        r = _F["mh329_cdar"](_eq_demo(), 0.95)
        assert r["n"] == N == 48
        assert r["dar"] * 100.0 == pytest.approx(DAR95)
        assert r["cdar"] * 100.0 == pytest.approx(CDAR95)
        assert r["max_dd"] * 100.0 == pytest.approx(MAXDD)
        assert r["n_tail"] == N_TAIL95 == 3

    def test_keys(self):
        r = _F["mh329_cdar"](_eq_demo(), 0.95)
        for k in ("dar", "cdar", "max_dd", "n_tail", "n"):
            assert k in r

    def test_formula_coda(self):
        eq = _eq_demo()
        r = _F["mh329_cdar"](eq, 0.95)
        dd = _F["mh329_drawdown"](eq)
        dar_att = float(np.quantile(dd, 0.95))
        tail = dd[dd >= dar_att]
        assert r["dar"] == pytest.approx(dar_att)
        assert r["cdar"] == pytest.approx(float(np.mean(tail)))
        assert r["n_tail"] == len(tail)

    def test_demo_99(self):
        r = _F["mh329_cdar"](_eq_demo(), 0.99)
        assert r["dar"] * 100.0 == pytest.approx(DAR99)
        assert r["cdar"] * 100.0 == pytest.approx(CDAR99)
        assert r["n_tail"] == N_TAIL99 == 1
        assert r["cdar"] == pytest.approx(r["max_dd"])

    def test_cdar_ge_dar(self):
        for a in (0.90, 0.95, 0.99):
            r = _F["mh329_cdar"](_eq_demo(), a)
            assert r["cdar"] >= r["dar"] - 1e-12
            assert r["max_dd"] >= r["cdar"] - 1e-12

    def test_alpha_ko(self):
        for bad in (0.5, 1.0, 1.5, 0.0):
            with pytest.raises(ValueError):
                _F["mh329_cdar"](_eq_demo(), bad)

    def test_senza_drawdown_zero(self):
        eq = np.array([100.0 + i for i in range(30)])
        r = _F["mh329_cdar"](eq, 0.95)
        assert r["dar"] == 0.0
        assert r["cdar"] == 0.0
        assert r["max_dd"] == 0.0


class TestCagr:
    def test_demo(self):
        assert _F["mh329_cagr"](_eq_demo(), 12) == pytest.approx(CAGR / 100.0)

    def test_cagr_scaling(self):
        eq = [100.0, 200.0] + [200.0] * 28
        assert _F["mh329_cagr"](eq, 12) == pytest.approx(2.0 ** (12 / 29) - 1)

    def test_cagr_negativo(self):
        eq = [100.0 - i for i in range(30)]
        assert _F["mh329_cagr"](eq, 12) < 0.0

    def test_cagr_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh329_cagr"](_eq_demo(), 0)


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh329_verdetto"](2.0, 13.46)
        assert v.startswith("cdar ECCELLENTE")

    def test_verdetto_soglia_eccellente(self):
        v = _F["mh329_verdetto"](13.46 / 1.5, 13.46)
        assert v.startswith("cdar ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh329_verdetto"](19.17, 13.46)
        assert v.startswith("cdar MODERATO")

    def test_verdetto_soglia_moderato(self):
        v = _F["mh329_verdetto"](13.46 / 0.7, 13.46)
        assert v.startswith("cdar MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh329_verdetto"](25.0, 13.46)
        assert v.startswith("cdar DEBOLE")

    def test_verdetto_cdar_zero(self):
        v = _F["mh329_verdetto"](0.0, 5.0)
        assert v.startswith("cdar ECCELLENTE")
        assert "0.00%" in v

    def test_verdetto_demo(self):
        eq = _eq_demo()
        r = _F["mh329_cdar"](eq, 0.95)
        cagr = _F["mh329_cagr"](eq, 12) * 100.0
        v = _F["mh329_verdetto"](r["cdar"] * 100.0, cagr)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_num_ko(self):
        with pytest.raises(ValueError):
            _F["mh329_verdetto"]("x", 5.0)
