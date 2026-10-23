"""Test tab387 '🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh387_num", "mh387_phi_exp", "mh387_j", "mh387_spectral",
           "mh387_var", "mh387_es", "mh387_spectral_flat",
           "mh387_extra", "mh387_verdetto", "mh387_mappa")

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
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
MU = 0.0
SIG = 10000.0
K = 5.0
ALPHA = 0.99
J_K = 1.0813608715043361
M_K = 10813.608715043361
VAR_ = 23263.47874040841
ES_ = 26652.142203458054
EXTRA = -0.5942686845772449
RATIO = 0.40573131542275503


class TestRegistry387:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 671
        assert "tab387" in dvars
        assert "tab387" in withs

    def test_titoli_allineati_382_383_384_385_386_387(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384
        assert titoli[dvars.index("tab385")] == TITLE385
        assert titoli[dvars.index("tab386")] == TITLE386
        assert titoli[dvars.index("tab387")] == TITLE387

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestNum:
    def test_num_ok(self):
        assert _F["mh387_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_num"](float("inf"), "x")


class TestPhi:
    def test_normalizzazione(self):
        n = 2048
        s = sum(_F["mh387_phi_exp"](K, (i + 0.5) / n)
                for i in range(n)) / n
        assert s == pytest.approx(1.0, abs=1e-6)

    def test_crescente(self):
        assert _F["mh387_phi_exp"](K, 0.2) < _F["mh387_phi_exp"](K, 0.5)
        assert _F["mh387_phi_exp"](K, 0.5) < _F["mh387_phi_exp"](K, 0.9)

    def test_k_piccolo_tende_uniforme(self):
        assert _F["mh387_phi_exp"](1e-6, 0.3) == pytest.approx(1.0, abs=1e-3)
        assert _F["mh387_phi_exp"](1e-6, 0.9) == pytest.approx(1.0, abs=1e-3)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](0.0, 0.5)
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](-2.0, 0.5)

    def test_u_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](K, 0.0)
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](K, 1.0)


class TestJ:
    def test_demo(self):
        assert _F["mh387_j"](K) == pytest.approx(J_K)

    def test_limite_k_zero(self):
        # k -> 0: phi -> uniforme, J -> integrale z = 0
        assert _F["mh387_j"](1e-9) == pytest.approx(0.0, abs=1e-6)

    def test_crescente(self):
        assert _F["mh387_j"](1.0) < _F["mh387_j"](K)
        assert _F["mh387_j"](K) < _F["mh387_j"](20.0)

    def test_griglia_fine(self):
        assert _F["mh387_j"](K, 8192) == pytest.approx(
            _F["mh387_j"](K), rel=5e-4)

    def test_deterministico(self):
        assert _F["mh387_j"](K) == _F["mh387_j"](K)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_j"](0.0)
        with pytest.raises(ValueError):
            _F["mh387_j"](-1.0)


class TestSpectral:
    def test_demo(self):
        assert _F["mh387_spectral"](K, MU, SIG) == pytest.approx(M_K)

    def test_forma(self):
        assert _F["mh387_spectral"](K, MU, SIG) == pytest.approx(
            MU + SIG * _F["mh387_j"](K))

    def test_maggiore_perdita_attesa(self):
        # J(k) >= 0 -> rho(k) >= mu
        assert _F["mh387_spectral"](K, MU, SIG) >= MU
        assert _F["mh387_spectral"](K, -5000.0, SIG) >= -5000.0

    def test_crescente_k(self):
        assert _F["mh387_spectral"](1.0, MU, SIG) < M_K
        assert M_K < _F["mh387_spectral"](20.0, MU, SIG)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_spectral"](0.0, MU, SIG)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_spectral"](K, MU, -1.0)


class TestFlat:
    def test_uguale_es(self):
        # peso piatto su [alpha, 1] = ES in forma chiusa
        assert _F["mh387_spectral_flat"](ALPHA, MU, SIG) == pytest.approx(
            ES_, rel=1e-4)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh387_spectral_flat"](ALPHA, MU, SIG) == pytest.approx(
            MU + SIG * phi / (1.0 - ALPHA), rel=1e-4)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_spectral_flat"](0.5, MU, SIG)


class TestVarEs:
    def test_demo(self):
        assert _F["mh387_var"](MU, SIG, ALPHA) == pytest.approx(VAR_)
        assert _F["mh387_es"](MU, SIG, ALPHA) == pytest.approx(ES_)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh387_var"](MU, SIG, ALPHA) == pytest.approx(
            MU + SIG * z)
        assert _F["mh387_es"](MU, SIG, ALPHA) == pytest.approx(
            MU + SIG * phi / (1.0 - ALPHA))

    def test_ratio_normale_99(self):
        assert ES_ / VAR_ == pytest.approx(1.1456, abs=1e-3)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_var"](MU, SIG, 0.5)
        with pytest.raises(ValueError):
            _F["mh387_es"](MU, SIG, 1.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_var"](MU, -1.0, ALPHA)


class TestExtraVerdetto:
    def test_demo(self):
        assert _F["mh387_extra"](M_K, ES_) == pytest.approx(EXTRA)
        assert _F["mh387_verdetto"](EXTRA).startswith("MENO CONSERVATIVA")

    def test_bordi(self):
        assert _F["mh387_verdetto"](-0.90).startswith("MENO CONSERVATIVA")
        assert _F["mh387_verdetto"](-0.25).startswith("MENO CONSERVATIVA")
        assert _F["mh387_verdetto"](-0.2499).startswith("IN LINEA")
        assert _F["mh387_verdetto"](0.0999).startswith("IN LINEA")
        assert _F["mh387_verdetto"](0.10).startswith("PRUDENTE")
        assert _F["mh387_verdetto"](0.4999).startswith("PRUDENTE")
        assert _F["mh387_verdetto"](0.50).startswith("ESTREMA")
        assert _F["mh387_verdetto"](math.inf).startswith("ESTREMA")

    def test_extra_inf(self):
        assert _F["mh387_extra"](100.0, 0.0) == math.inf

    def test_extra_zero(self):
        assert _F["mh387_extra"](0.0, 0.0) == 0.0

    def test_es_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_extra"](M_K, -1.0)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_verdetto"](float("nan"))


class TestMappa:
    def _b(self):
        return _F["mh387_mappa"](K, MU, SIG, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["k"] == K
        assert b["mu"] == MU
        assert b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["J"] == pytest.approx(J_K)
        assert b["var"] == pytest.approx(VAR_)
        assert b["es"] == pytest.approx(ES_)
        assert b["m"] == pytest.approx(M_K)
        assert b["extra"] == pytest.approx(EXTRA)
        assert b["ratio"] == pytest.approx(RATIO)
        assert b["verdetto"].startswith("MENO CONSERVATIVA")

    def test_coerenza(self):
        b = self._b()
        assert b["m"] == pytest.approx(b["mu"] + b["sig"] * b["J"])
        assert b["extra"] == pytest.approx(b["m"] / b["es"] - 1.0)
        assert b["ratio"] == pytest.approx(b["m"] / b["es"])
