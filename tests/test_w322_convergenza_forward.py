"""Test tab322 '🎯📉 Convergenza forward: il forward indovina lo spot?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della convergenza forward: validatori,
parse coppie, errori, bias, RMSE, MAE, hit rate, premio %, t-stat del bias,
verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh322_num", "mh322_parse_coppie", "mh322_errori", "mh322_bias",
           "mh322_rmse", "mh322_mae", "mh322_hit", "mh322_premio_pct",
           "mh322_risultato", "mh322_verdetto")

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
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
COPPIE_DEMO = '106.93;116.98\n107.84;99.26\n101.46;97.31\n88.64;90.64\n78.61;68.61\n67.77;69.39\n70.00;69.14\n68.48;69.67\n78.87;85.82\n92.17;86.39\n104.68;98.48\n105.29;108.10\n107.33;106.83\n106.99;117.16\n98.01;90.92\n95.39;75.36\n80.48;82.50\n68.78;53.28\n67.03;47.34\n71.72;65.30\n76.58;63.33\n94.04;69.27\n100.38;106.04\n106.42;102.37'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 24
BIAS = 4.3500000000000005
RMSE = 10.1952047551778
MAE = 7.889166666666665
HIT = 0.625
PREMIO = 7.321136840834128
TSTAT = 2.0902533371280003
STATO = "premio forward sistematico"
VERDETTO = 'premio forward sistematico: bias +4.35 €/MWh (t-stat 2.09 su 24 mesi): il forward quota sistematicamente sopra lo spot realizzato, il mercato paga un premio per la certezza del prezzo.'

def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh322_risultato"](COPPIE_DEMO)


class TestRegistry322:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 514
        assert TITLE322 in titoli
        assert "tab322" in dvars
        assert "    with tab322:" in src

    def test_titoli_allineati_320_321_322(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab320")] == TITLE320
        assert titoli[dvars.index("tab321")] == TITLE321
        assert titoli[dvars.index("tab322")] == TITLE322

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert TITLE482 in titoli
        assert "tab482" in dvars


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh322_num"](3.5, "t") == 3.5
        assert _F["mh322_num"](7, "t") == 7.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh322_num"](bad, "t")

    def test_parse_ok(self):
        coppie = _F["mh322_parse_coppie"](COPPIE_DEMO)
        assert len(coppie) == N == 24
        assert all(isinstance(f, float) and isinstance(s, float)
                   for f, s in coppie)

    def test_parse_ko_poche(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["90.0;80.0"] * 11))

    def test_parse_ko_campi(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["90.0"] * 12))
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["90.0;80.0;70.0"] * 12))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["a;b"] * 12))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"](None)

    def test_parse_virgola(self):
        coppie = _F["mh322_parse_coppie"]("\n".join(["90,5;80,25"] * 12))
        assert coppie[0] == (90.5, 80.25)

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["90.0;80.0"] * 12) + "\n\n"
        assert len(_F["mh322_parse_coppie"](txt)) == 12


class TestErrori:
    def test_errori_noti(self):
        assert _F["mh322_errori"]([(100.0, 90.0), (80.0, 85.0)]) == [10.0, -5.0]

    def test_errori_vuoti_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_errori"]([])

    def test_bias_noto(self):
        assert _F["mh322_bias"]([10.0, -5.0, 4.0]) == pytest.approx(3.0)

    def test_bias_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_bias"]([])

    def test_rmse_noto(self):
        assert _F["mh322_rmse"]([3.0, 4.0]) == pytest.approx(math.sqrt(12.5))

    def test_rmse_zero(self):
        assert _F["mh322_rmse"]([0.0, 0.0]) == 0.0

    def test_rmse_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_rmse"]([])

    def test_mae_noto(self):
        assert _F["mh322_mae"]([3.0, -4.0]) == pytest.approx(3.5)

    def test_mae_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_mae"]([])

    def test_hit_noto(self):
        assert _F["mh322_hit"]([(100.0, 90.0), (80.0, 80.0),
                                (70.0, 75.0)]) == pytest.approx(1.0 / 3.0)

    def test_hit_estremi(self):
        assert _F["mh322_hit"]([(2.0, 1.0)] * 12) == 1.0
        assert _F["mh322_hit"]([(1.0, 2.0)] * 12) == 0.0

    def test_hit_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_hit"]([])

    def test_premio_pct_noto(self):
        assert _F["mh322_premio_pct"]([(110.0, 100.0),
                                       (90.0, 100.0)]) == pytest.approx(0.0)

    def test_premio_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_premio_pct"]([])


class TestRisultato:
    def _ris_demo(self):
        return _F["mh322_risultato"](COPPIE_DEMO)

    def test_risultato_demo(self):
        ris = self._ris_demo()
        assert ris["n"] == N == 24
        assert ris["bias"] == BIAS
        assert ris["rmse"] == RMSE
        assert ris["mae"] == MAE
        assert ris["hit"] == HIT
        assert ris["premio_pct"] == PREMIO
        assert ris["t_stat"] == TSTAT
        assert len(ris["errori"]) == N
        assert len(ris["coppie"]) == N

    def test_coerenza_interna(self):
        ris = self._ris_demo()
        assert sum(ris["errori"]) == pytest.approx(ris["n"] * ris["bias"])
        assert ris["rmse"] >= ris["mae"] >= 0.0
        assert 0.0 <= ris["hit"] <= 1.0
        assert ris["t_stat"] == pytest.approx(
            ris["bias"] / (ris["rmse"] / math.sqrt(ris["n"])))

    def test_demo_bias_positivo_significativo(self):
        assert BIAS > 0.0
        assert TSTAT > 2.0
        assert HIT > 0.5
        assert PREMIO > 0.0


class TestVerdetto:
    def _base(self, **kw):
        return {"n": 24, "bias": 5.0, "t_stat": 3.0, **kw}

    def test_verdetto_demo(self):
        ris = _F["mh322_risultato"](COPPIE_DEMO)
        assert _F["mh322_verdetto"](ris) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_premio(self):
        v = _F["mh322_verdetto"](self._base())
        assert v.startswith("premio forward sistematico")

    def test_stato_sconto(self):
        v = _F["mh322_verdetto"](self._base(bias=-4.0, t_stat=-3.0))
        assert v.startswith("sconto forward sistematico")

    def test_stato_imparziale(self):
        v = _F["mh322_verdetto"](self._base(bias=0.5, t_stat=0.4))
        assert v.startswith("forward imparziale")

    def test_verdetto_bordi(self):
        assert _F["mh322_verdetto"](
            self._base(bias=3.0, t_stat=2.0)).startswith("forward imparziale")
        assert _F["mh322_verdetto"](
            self._base(bias=3.0, t_stat=2.01)).startswith(
            "premio forward sistematico")
        assert _F["mh322_verdetto"](
            self._base(bias=-3.0, t_stat=-2.0)).startswith("forward imparziale")

