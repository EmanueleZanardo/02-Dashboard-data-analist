"""Test tab371 'Kelly frazionario: frazione ottima per un budget di volatilità': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh371_num", "mh371_fstar", "mh371_growth", "mh371_vol_log",
           "mh371_sharpe", "mh371_frazione_target", "mh371_f_fraz",
           "mh371_trade_raddoppio", "mh371_curva", "mh371_verdetto",
           "mh371_analisi")

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
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
MU = 0.02
SIGMA = 0.1
V = 0.05
FSTAR = 1.9999999999999996
VOLSTAR = 0.19999999999999996
CSTAR = 0.25000000000000006
F = 0.5
G = 0.00875
VOL = 0.05
SHARPE = 0.19999999999999998
TRADE2X = 79.21682063542231
VERDETTO = 'FRAZIONARIO: applica c = 25% di f* Kelly (f = 25% x f*) per rispettare il budget di vol.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry371:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 717
        assert "tab371" in dvars
        assert "tab371" in withs

    def test_titoli_allineati_366_367_368_369_370_371(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh371_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_num"](float("inf"), "x")


class TestFstar:
    def test_demo(self):
        # 0.02 / 0.10^2 = 2.0
        assert _F["mh371_fstar"](MU, SIGMA) == pytest.approx(FSTAR)

    def test_forma_chiusa(self):
        assert _F["mh371_fstar"](0.03, 0.10) == pytest.approx(3.0)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_fstar"](MU, 0.0)


class TestGrowth:
    def test_demo(self):
        assert _F["mh371_growth"](F, MU, SIGMA) == pytest.approx(G)

    def test_forma_chiusa(self):
        f, mu, sg = 0.5, 0.02, 0.10
        assert _F["mh371_growth"](f, mu, sg) == pytest.approx(
            f * mu - 0.5 * (f * sg) ** 2)

    def test_zero_in_zero(self):
        assert _F["mh371_growth"](0.0, MU, SIGMA) == pytest.approx(0.0)

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_growth"](-0.1, MU, SIGMA)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_growth"](F, MU, 0.0)


class TestFrazioneTarget:
    def test_demo(self):
        # 0.05 / (2.0 * 0.10) = 0.25
        assert _F["mh371_frazione_target"](V, FSTAR,
                                           SIGMA) == pytest.approx(CSTAR)

    def test_cappata_a_uno(self):
        # V=0.30 > vol_star=0.20 -> 1.0
        assert _F["mh371_frazione_target"](0.30, 2.0,
                                           0.10) == pytest.approx(1.0)

    def test_v_zero(self):
        assert _F["mh371_frazione_target"](0.0, 2.0,
                                           0.10) == pytest.approx(0.0)

    def test_v_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_frazione_target"](-0.01, 2.0, 0.10)

    def test_fstar_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_frazione_target"](V, 0.0, SIGMA)


class TestFFraz:
    def test_demo(self):
        assert _F["mh371_f_fraz"](CSTAR, FSTAR) == pytest.approx(F)

    def test_c_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_f_fraz"](1.5, FSTAR)

    def test_c_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_f_fraz"](-0.1, FSTAR)


class TestSharpe:
    def test_demo(self):
        assert _F["mh371_sharpe"](MU, SIGMA) == pytest.approx(SHARPE)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh371_sharpe"](MU, 0.0)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh371_verdetto"](MU, CSTAR).startswith("FRAZIONARIO")
        assert _F["mh371_verdetto"](MU, CSTAR) == VERDETTO

    def test_nessun_edge(self):
        assert _F["mh371_verdetto"](-0.01, 0.5).startswith("NESSUN EDGE")
        assert _F["mh371_verdetto"](0.0, 1.0).startswith("NESSUN EDGE")

    def test_pieno(self):
        assert _F["mh371_verdetto"](MU, 1.0).startswith("PIENO")

    def test_nessuna_posizione(self):
        assert _F["mh371_verdetto"](MU, 0.0).startswith("NESSUNA POSIZIONE")


class TestCurva:
    def test_dimensioni(self):
        cv = _F["mh371_curva"](MU, SIGMA)
        assert len(cv["cs"]) == 81
        assert len(cv["gs"]) == 81
        assert len(cv["vols"]) == 81

    def test_estremi(self):
        cv = _F["mh371_curva"](MU, SIGMA)
        assert cv["cs"][0] == 0.0 and cv["cs"][-1] == 1.0
        assert cv["gs"][0] == pytest.approx(0.0)
        assert cv["vols"][0] == pytest.approx(0.0)
        # a c=1: g = g* = 0.02, vol = vol_star = 0.20
        assert cv["gs"][-1] == pytest.approx(0.02)
        assert cv["vols"][-1] == pytest.approx(0.20)

    def test_coerenza_punto_a_punto(self):
        cv = _F["mh371_curva"](MU, SIGMA)
        for cc, gg, vv in zip(cv["cs"][::10], cv["gs"][::10],
                              cv["vols"][::10]):
            ff = cc * FSTAR
            assert gg == pytest.approx(_F["mh371_growth"](ff, MU, SIGMA))
            assert vv == pytest.approx(_F["mh371_vol_log"](ff, SIGMA))


class TestAnalisi:
    def test_demo(self):
        a = _F["mh371_analisi"](MU, SIGMA, V)
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["vol_star"] == pytest.approx(VOLSTAR)
        assert a["c_star"] == pytest.approx(CSTAR)
        assert a["f"] == pytest.approx(F)
        assert a["g"] == pytest.approx(G)
        assert a["vol"] == pytest.approx(VOL)
        assert a["sharpe"] == pytest.approx(SHARPE)
        assert a["trade_raddoppio"] == pytest.approx(TRADE2X)
        assert a["verdetto"] == VERDETTO

    def test_trade_raddoppio_none(self):
        assert _F["mh371_trade_raddoppio"](0.0) is None
        assert _F["mh371_trade_raddoppio"](-0.01) is None
        assert _F["mh371_trade_raddoppio"](0.01) == pytest.approx(
            math.log(2.0) / 0.01)
