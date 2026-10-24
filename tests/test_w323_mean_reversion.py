"""Test tab323 '🔄📉 Half-life di mean reversion: lo spot torna alla media?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della mean reversion: validatori,
parse serie, stima OLS di beta (se, t-stat, R2), half-life, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh323_num", "mh323_parse_serie", "mh323_beta",
           "mh323_half_life", "mh323_risultato", "mh323_verdetto")

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
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
SERIE_DEMO = '79.81\n81.48\n93.40\n95.39\n90.10\n86.24\n96.97\n94.32\n87.08\n85.19\n80.96\n87.50\n90.32\n83.94\n85.56\n86.96\n93.54\n99.15\n88.03\n86.26\n88.44\n95.28\n99.54\n86.99\n89.42\n85.97\n89.25\n96.91\n102.51\n102.44\n95.33\n90.81\n85.86\n80.26\n85.01\n91.36\n103.15\n97.06\n102.36\n96.99\n89.46\n82.88\n76.32\n75.04\n75.33\n80.15\n69.20\n72.93'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
MEDIA = 88.71770833333333
BETA = -0.2765819440306293
SE = 0.10913133936554696
TSTAT = -2.5343952125813174
R2 = 0.12440563341620703
HL = 2.14087612352128
STATO = "mean reversion RAPIDA"
VERDETTO = 'mean reversion RAPIDA: half-life 2.1 mesi (beta -0.2766, t-stat -2.53, R2 0.12): gli scostamenti dalla media si dimezzano in pochi mesi, picchi e crolli vanno colti in fretta prima del rientro.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh323_risultato"](SERIE_DEMO)


class TestRegistry323:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 682
        assert TITLE323 in titoli
        assert "tab323" in dvars
        assert "    with tab323:" in src

    def test_titoli_allineati_321_322_323(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab321")] == TITLE321
        assert titoli[dvars.index("tab322")] == TITLE322
        assert titoli[dvars.index("tab323")] == TITLE323

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh323_num"](3.5, "t") == 3.5
        assert _F["mh323_num"](7, "t") == 7.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh323_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh323_parse_serie"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(isinstance(v, float) for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh323_parse_serie"]("\n".join(["90.0"] * 23))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh323_parse_serie"]("\n".join(["a"] * 24))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh323_parse_serie"](None)

    def test_parse_virgola(self):
        vals = _F["mh323_parse_serie"]("\n".join(["90,5"] * 24))
        assert vals[0] == 90.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["90.0"] * 24) + "\n\n"
        assert len(_F["mh323_parse_serie"](txt)) == 24


class TestBeta:
    def test_beta_sintetica(self):
        # serie alternata 10/5: mu=7.5, dp = -2*(p_{t-1}-mu) esatto
        vals = _F["mh323_parse_serie"]("\n".join(["10", "5"] * 14))
        st_ = _F["mh323_beta"](vals)
        assert st_["beta"] == pytest.approx(-2.0)
        assert st_["m"] == len(vals) - 1
        assert st_["media"] == pytest.approx(7.5)

    def test_beta_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh323_beta"]([1.0] * 23)

    def test_beta_costante_ko(self):
        with pytest.raises(ValueError):
            _F["mh323_beta"]([50.0] * 30)

    def test_beta_demo(self):
        st_ = _F["mh323_beta"](_F["mh323_parse_serie"](SERIE_DEMO))
        assert st_["beta"] == pytest.approx(BETA)
        assert st_["se_beta"] == pytest.approx(SE)
        assert st_["t_stat"] == pytest.approx(TSTAT)
        assert st_["r2"] == pytest.approx(R2)
        assert st_["media"] == pytest.approx(MEDIA)

    def test_t_stat_significativo(self):
        assert TSTAT < -2.0


class TestHalfLife:
    def test_hl_beta_mezza(self):
        assert _F["mh323_half_life"](-0.5) == pytest.approx(1.0)

    def test_hl_random_walk_none(self):
        assert _F["mh323_half_life"](0.0) is None
        assert _F["mh323_half_life"](0.1) is None

    def test_hl_beta_uno_none(self):
        assert _F["mh323_half_life"](-1.0) is None

    def test_hl_demo(self):
        hl = _F["mh323_half_life"](BETA)
        assert hl == pytest.approx(HL)
        assert 1.0 < hl < 3.0


class TestRisultato:
    def test_ris_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N == 48
        assert ris["half_life"] == pytest.approx(HL)
        assert ris["beta"] == pytest.approx(BETA)
        assert ris["media"] == pytest.approx(MEDIA)

    def test_ris_keys(self):
        ris = _ris_demo()
        for k in ("beta", "se_beta", "t_stat", "r2", "m", "media",
                  "n", "half_life"):
            assert k in ris

    def test_verdetto_demo(self):
        ris = _ris_demo()
        verd = _F["mh323_verdetto"](ris)
        assert verd == VERDETTO
        assert verd.startswith(STATO)


class TestVerdetto:
    def test_verdetto_rapida(self):
        ris = {"beta": -0.27, "se_beta": 0.1, "t_stat": -2.7, "r2": 0.1,
               "half_life": 2.1, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith("mean reversion RAPIDA")

    def test_verdetto_moderata(self):
        ris = {"beta": -0.13, "se_beta": 0.05, "t_stat": -2.6, "r2": 0.1,
               "half_life": 5.0, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith("mean reversion MODERATA")

    def test_verdetto_assente_none(self):
        ris = {"beta": 0.05, "se_beta": 0.05, "t_stat": 1.0, "r2": 0.01,
               "half_life": None, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith(
            "mean reversion debole o assente")

    def test_verdetto_assente_t_debole(self):
        ris = {"beta": -0.02, "se_beta": 0.05, "t_stat": -0.4, "r2": 0.01,
               "half_life": 30.0, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith(
            "mean reversion debole o assente")
