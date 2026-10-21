"""Test tab398 '🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh398_num", "mh398_check_w", "mh398_check_vol",
           "mh398_check_rho", "mh398_check_alpha", "mh398_cov",
           "mh398_es_chiusa", "mh398_euler", "mh398_verdetto",
           "mh398_mappa")

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
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
W1 = 1.5
W2 = 1.0
W3 = 0.8
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.6
R13 = 0.3
R23 = 0.45
ALPHA = 0.975
ES = 1822624.28409285
RC1 = 738780.1719135869
RC2 = 716815.4240322394
RC3 = 367028.688147024
PCT1 = 40.533870768724555
PCT2 = 39.328754164438784
PCT3 = 20.137375066836675
BEN = 0.19209189313314545


class TestRegistry398:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 608
        assert "tab398" in dvars
        assert "tab398" in withs

    def test_titoli_allineati_393_394_395_396_397_398(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397
        assert titoli[dvars.index("tab398")] == TITLE398

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


class TestEuler:
    def _demo(self):
        return _F["mh398_euler"]((W1, W2, W3), (V1, V2, V3),
                                 R12, R13, R23, ALPHA)

    def test_somma_rc_uguale_es(self):
        # teorema di Eulero: Σ RC_i == ES (1-omogeneita')
        e = self._demo()
        assert abs(sum(e["rc"]) - e["es"]) / e["es"] < 1e-12

    def test_rc_pct_somma_100(self):
        e = self._demo()
        assert abs(sum(e["rc_pct"]) - 100.0) < 1e-9

    def test_demo_costanti(self):
        e = self._demo()
        assert abs(e["es"] - ES) / ES < 1e-12
        for got, exp in zip(e["rc"], (RC1, RC2, RC3)):
            assert abs(got - exp) / ES < 1e-12
        for got, exp in zip(e["rc_pct"], (PCT1, PCT2, PCT3)):
            assert abs(got - exp) < 1e-9
        assert abs(e["benefit"] - BEN) < 1e-12

    def test_omogeneita(self):
        # scala nozionali x2 -> RC x2, RC% invariati
        e1 = self._demo()
        e2 = _F["mh398_euler"]((2 * W1, 2 * W2, 2 * W3),
                               (V1, V2, V3), R12, R13, R23, ALPHA)
        assert abs(e2["es"] - 2 * e1["es"]) / e1["es"] < 1e-12
        for a, b in zip(e2["rc"], e1["rc"]):
            assert abs(a - 2 * b) / e1["es"] < 1e-12
        for a, b in zip(e2["rc_pct"], e1["rc_pct"]):
            assert abs(a - b) < 1e-9

    def test_simmetria_indipendente(self):
        # rho=0, tutto uguale -> 1/3 ciascuno
        e = _F["mh398_euler"]((1.0, 1.0, 1.0), (0.2, 0.2, 0.2),
                              0.0, 0.0, 0.0, 0.975)
        for p in e["rc_pct"]:
            assert abs(p - 100.0 / 3.0) < 1e-9

    def test_singolo_asset(self):
        # una sola posizione -> tutto il rischio e' suo
        e = _F["mh398_euler"]((2.0, 0.0, 0.0), (0.3, 0.3, 0.3),
                              0.5, 0.5, 0.5, 0.975)
        assert abs(e["rc"][0] - e["es"]) / e["es"] < 1e-12
        assert e["rc"][1] == 0.0 and e["rc"][2] == 0.0
        assert abs(e["rc_pct"][0] - 100.0) < 1e-9

    def test_beneficio_non_negativo(self):
        # subadditivita': il beneficio non e' mai negativo
        e = self._demo()
        assert e["benefit"] >= -1e-12
        assert e["es"] <= e["standalone"] * (1.0 + 1e-12)

    def test_hedge_rc_negativo(self):
        # asset 3 anti-correlato -> contributo negativo (hedge)
        e = _F["mh398_euler"]((1.0, 1.0, 1.0), (0.2, 0.2, 0.2),
                              0.9, -0.6, -0.6, 0.975)
        assert e["rc"][2] < 0.0
        assert abs(sum(e["rc"]) - e["es"]) / e["es"] < 1e-12

    def test_cov_psd_ko(self):
        # matrice non PSD -> ValueError
        with pytest.raises(ValueError):
            _F["mh398_cov"]((1.0, 1.0, 1.0), 0.9, 0.9, -0.9)
        with pytest.raises(ValueError):
            _F["mh398_euler"]((1.0, 1.0, 1.0), (0.2, 0.2, 0.2),
                              0.9, 0.9, -0.9, 0.975)

    def test_verdetto_stati(self):
        e = self._demo()
        assert _F["mh398_verdetto"](e["rc_pct"], 0).startswith("MODERATO")
        e1 = _F["mh398_euler"]((2.0, 0.0, 0.0), (0.3, 0.3, 0.3),
                               0.5, 0.5, 0.5, 0.975)
        assert _F["mh398_verdetto"](e1["rc_pct"], 0).startswith(
            "CONCENTRATO")
        e2 = _F["mh398_euler"]((1.0, 1.0, 1.0), (0.2, 0.2, 0.2),
                               0.0, 0.0, 0.0, 0.975)
        assert _F["mh398_verdetto"](e2["rc_pct"], 0).startswith(
            "DIVERSIFICATO")
        eh = _F["mh398_euler"]((1.0, 1.0, 1.0), (0.2, 0.2, 0.2),
                               0.9, -0.6, -0.6, 0.975)
        _vh = _F["mh398_verdetto"](
            eh["rc_pct"], sum(1 for _x in eh["rc"] if _x < 0.0))
        assert "hedge" in _vh

    def test_num_ko(self):
        with pytest.raises(ValueError):
            _F["mh398_num"](True, "x")
        with pytest.raises(ValueError):
            _F["mh398_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh398_num"](float("inf"), "x")
        with pytest.raises(ValueError):
            _F["mh398_check_w"](-0.5)
        with pytest.raises(ValueError):
            _F["mh398_check_vol"](2.5)
        with pytest.raises(ValueError):
            _F["mh398_check_rho"](1.5)
        with pytest.raises(ValueError):
            _F["mh398_check_alpha"](1.0)
        with pytest.raises(ValueError):
            _F["mh398_es_chiusa"](-1.0, 0.975)

    def test_mappa_demo(self):
        b = _F["mh398_mappa"]((W1, W2, W3), (V1, V2, V3),
                              R12, R13, R23, ALPHA)
        assert abs(b["es"] - ES) / ES < 1e-12
        assert b["n_hedge"] == 0
        assert b["verdetto"].startswith("MODERATO")
        assert b["rho"] == (R12, R13, R23)
