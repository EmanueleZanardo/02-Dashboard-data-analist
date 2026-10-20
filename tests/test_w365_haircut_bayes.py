"""Test tab365 'Kelly con incertezza: haircut bayesiano sulla p stimata': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh365_num", "mh365_int", "mh365_betacf", "mh365_betai",
           "mh365_beta_ppf", "mh365_beta_pdf", "mh365_posterior",
           "mh365_p_low", "mh365_fstar", "mh365_haircut", "mh365_verdetto",
           "mh365_posterior_grid", "mh365_analisi")

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
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
K = 60
N = 100
B = 1.2
ALPHA = 0.05
A = 61
BETA = 41
PHAT = 0.5980392156862745
PLOW = 0.517438828147089
FHAT = 0.2630718954248366
FLOW = 0.11530451826966308
HALFK = 0.1315359477124183
HC = 0.43830040485114163
VERDETTO = "STIMA FRAGILE: haircut 44% — il campione e' troppo piccolo per fidarsi di f* = 26.31%: raccogli piu' trade o usa il Kelly prudente (11.53%)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry365:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 599
        assert "tab365" in dvars
        assert "tab365" in withs

    def test_titoli_allineati_360_361_362_363_364_365(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab360")] == TITLE360
        assert titoli[dvars.index("tab361")] == TITLE361
        assert titoli[dvars.index("tab362")] == TITLE362
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364
        assert titoli[dvars.index("tab365")] == TITLE365

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh365_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_num"](float("nan"), "x")

    def test_int_ok(self):
        assert _F["mh365_int"](60.0, "k", 0) == 60

    def test_int_non_intero_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_int"](60.5, "k", 0)

    def test_int_sotto_minimo_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_int"](-1, "k", 0)


class TestBetaCdf:
    def test_uniforme(self):
        assert _F["mh365_betai"](1, 1, 0.3) == pytest.approx(0.3)

    def test_a2_b1(self):
        assert _F["mh365_betai"](2, 1, 0.5) == pytest.approx(0.25)

    def test_a1_b2(self):
        assert _F["mh365_betai"](1, 2, 0.5) == pytest.approx(0.75)

    def test_bordi(self):
        assert _F["mh365_betai"](A, BETA, 0.0) == 0.0
        assert _F["mh365_betai"](A, BETA, 1.0) == 1.0

    def test_ppf_inverte_cdf(self):
        q = _F["mh365_beta_ppf"](0.05, A, BETA)
        assert _F["mh365_betai"](A, BETA, q) == pytest.approx(0.05, abs=1e-6)

    def test_ppf_mediana_vicina_media(self):
        med = _F["mh365_beta_ppf"](0.5, A, BETA)
        assert abs(med - PHAT) < 0.01

    def test_ppf_q_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_beta_ppf"](0.0, A, BETA)

    def test_pdf_bordi_zero(self):
        assert _F["mh365_beta_pdf"](A, BETA, 0.0) == 0.0
        assert _F["mh365_beta_pdf"](A, BETA, 1.0) == 0.0

    def test_pdf_positiva_dentro(self):
        assert _F["mh365_beta_pdf"](A, BETA, PHAT) > 0.0


class TestPosterior:
    def test_demo(self):
        post = _F["mh365_posterior"](K, N)
        assert post["a"] == A
        assert post["b"] == BETA
        assert post["p_hat"] == pytest.approx(PHAT)

    def test_k_maggiore_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_posterior"](11, 10)

    def test_n_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_posterior"](0, 0)

    def test_prior_su_zero_dati(self):
        post = _F["mh365_posterior"](0, 1)
        assert post["p_hat"] == pytest.approx(1.0 / 3.0)


class TestPLow:
    def test_demo(self):
        assert _F["mh365_p_low"](K, N, ALPHA) == pytest.approx(PLOW)

    def test_ordinamento(self):
        assert _F["mh365_p_low"](K, N, ALPHA) < PHAT

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_p_low"](K, N, 0.6)


class TestFstar:
    def test_demo(self):
        assert _F["mh365_fstar"](PHAT, B) == pytest.approx(FHAT)

    def test_no_edge(self):
        assert _F["mh365_fstar"](0.30, 1.0) == 0.0

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_fstar"](PHAT, 0.0)


class TestHaircut:
    def test_demo(self):
        assert _F["mh365_haircut"](FHAT, FLOW) == pytest.approx(HC)

    def test_f_hat_zero(self):
        assert _F["mh365_haircut"](0.0, 0.0) == 1.0

    def test_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_haircut"](-0.1, 0.05)


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh365_verdetto"](0.0, 1.0).startswith("NESSUN EDGE")

    def test_solida(self):
        assert _F["mh365_verdetto"](0.20, 0.85).startswith("STIMA SOLIDA")

    def test_incerta(self):
        assert _F["mh365_verdetto"](0.20, 0.70).startswith("STIMA INCERTA")

    def test_fragile(self):
        assert _F["mh365_verdetto"](0.20, 0.40).startswith("STIMA FRAGILE")

    def test_haircut_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_verdetto"](0.20, 1.5)


class TestGrid:
    def test_demo(self):
        g = _F["mh365_posterior_grid"](K, N, 51)
        assert len(g) == 51
        assert g[0]["p"] == 0.0
        assert g[-1]["p"] == pytest.approx(1.0)
        assert g[0]["d"] == 0.0 and g[-1]["d"] == 0.0
        imax = max(range(51), key=lambda i: g[i]["d"])
        assert abs(g[imax]["p"] - PHAT) < 0.05

    def test_normalizzazione(self):
        g = _F["mh365_posterior_grid"](K, N, 101)
        area = sum(0.5 * (g[i]["d"] + g[i + 1]["d"])
                   * (g[i + 1]["p"] - g[i]["p"])
                   for i in range(len(g) - 1))
        assert area == pytest.approx(1.0, abs=0.02)

    def test_m_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_posterior_grid"](K, N, 2)


class TestAnalisi:
    def _demo(self):
        return _F["mh365_analisi"](K, N, B, ALPHA)

    def test_demo(self):
        a = self._demo()
        assert a["a"] == A
        assert a["b"] == BETA
        assert a["p_hat"] == pytest.approx(PHAT)
        assert a["p_low"] == pytest.approx(PLOW)
        assert a["f_hat"] == pytest.approx(FHAT)
        assert a["f_low"] == pytest.approx(FLOW)
        assert a["half_kelly"] == pytest.approx(HALFK)
        assert a["haircut"] == pytest.approx(HC)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("STIMA FRAGILE")
        assert a["f_low"] < a["f_hat"]
        assert a["p_low"] < a["p_hat"]

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["p_low"] == a2["p_low"]

    def test_b_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_analisi"](K, N, 0.0, ALPHA)

    def test_k_maggiore_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_analisi"](N + 1, N, B, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh365_analisi"](K, N, B, 0.0)
