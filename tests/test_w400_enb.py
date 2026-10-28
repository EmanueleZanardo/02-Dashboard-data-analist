"""Test tab400 '🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh400_num", "mh400_check_vol", "mh400_check_rho",
           "mh400_check_w", "mh400_covmat", "mh400_eulero",
           "mh400_distribuzione", "mh400_enb", "mh400_verdetto",
           "mh400_mappa")

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
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.6
R13 = 0.3
R23 = 0.45
W1 = 0.3333333333333333
W2 = 0.3333333333333333
W3 = 0.3333333333333333
SIGP = 0.24025449469723187
ENB = 2.937894597812594
P1 = 0.2646775745909528
P2 = 0.4278152069297401
P3 = 0.307507218479307


class TestRegistry400:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 780
        assert "tab400" in dvars
        assert "tab400" in withs

    def test_titoli_allineati_395_396_397_398_399_400(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397
        assert titoli[dvars.index("tab398")] == TITLE398
        assert titoli[dvars.index("tab399")] == TITLE399
        assert titoli[dvars.index("tab400")] == TITLE400

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


class TestEnb400:
    def _demo(self):
        return _F["mh400_mappa"]((V1, V2, V3), R12, R13, R23,
                                 (W1, W2, W3), 5.0)

    def test_demo_enb(self):
        m = self._demo()
        assert abs(m["enb"] - ENB) / ENB < 1e-9
        assert abs(m["sig"] - SIGP) / SIGP < 1e-12
        assert abs(m["enb_ratio"] - ENB / 3.0) < 1e-12
        assert m["verdetto"].startswith("DIVERSIFICATO")

    def test_demo_distribuzione(self):
        m = self._demo()
        for _g, _e in zip(m["p"], (P1, P2, P3)):
            assert abs(_g - _e) < 1e-12
        assert abs(sum(m["p"]) - 1.0) < 1e-12
        assert abs(sum(m["p_pct"]) - 100.0) < 1e-9

    def test_eulero_somma_rc_uguale_sig(self):
        S = _F["mh400_covmat"]((V1, V2, V3), R12, R13, R23)
        eu = _F["mh400_eulero"]((W1, W2, W3), S)
        assert abs(sum(eu["rc"]) - eu["sig"]) / eu["sig"] < 1e-12
        assert abs(sum(eu["rc_pct"]) - 100.0) < 1e-9

    def test_simmetria_enb_3(self):
        m = _F["mh400_mappa"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0,
                              (1.0, 1.0, 1.0), 5.0)
        assert abs(m["enb"] - 3.0) < 1e-9

    def test_singola_posizione_enb_1(self):
        m = _F["mh400_mappa"]((V1, V2, V3), R12, R13, R23,
                              (100.0, 0.0, 0.0), 5.0)
        assert abs(m["enb"] - 1.0) < 1e-9

    def test_p_zero_contributo_nullo(self):
        assert abs(_F["mh400_enb"]((0.5, 0.5, 0.0)) - 2.0) < 1e-12

    def test_bound_1_n_casi_fissi(self):
        for _w, _vv, _rr in (
                ((0.9, 0.05, 0.05), (0.25, 0.35, 0.30), (0.6, 0.3, 0.45)),
                ((0.05, 0.9, 0.05), (0.25, 0.35, 0.30), (0.0, 0.0, 0.0)),
                ((0.2, 0.3, 0.5), (0.1, 0.5, 0.4), (0.8, 0.2, 0.1)),
                ((1.0 / 3, 1.0 / 3, 1.0 / 3), (0.6, 0.1, 0.2),
                 (0.9, 0.9, 0.9)),
                ((0.7, 0.2, 0.1), (0.05, 0.05, 0.6), (0.3, 0.0, 0.5))):
            m = _F["mh400_mappa"](_vv, _rr[0], _rr[1], _rr[2], _w, 5.0)
            assert 1.0 - 1e-9 <= m["enb"] <= 3.0 + 1e-9

    def test_entropiaricalcolata_a_mano(self):
        _h = -sum(_x * math.log(_x) for _x in (P1, P2, P3) if _x > 0)
        assert abs(math.exp(_h) - ENB) / ENB < 1e-12

    def test_inviaranza_scala_vol(self):
        a = self._demo()
        b = _F["mh400_mappa"](tuple(2 * _x for _x in (V1, V2, V3)),
                              R12, R13, R23, (W1, W2, W3), 5.0)
        assert abs(a["enb"] - b["enb"]) < 1e-9
        assert abs(b["sig"] - 2 * a["sig"]) / a["sig"] < 1e-9

    def test_pesi_normalizzati(self):
        _w = _F["mh400_check_w"]((20.0, 30.0, 50.0))
        assert abs(sum(_w) - 1.0) < 1e-12
        for _g, _e in zip(_w, (0.2, 0.3, 0.5)):
            assert abs(_g - _e) < 1e-12

    def test_verdetto_stati_e_bordi(self):
        assert _F["mh400_verdetto"](2.9).startswith("DIVERSIFICATO")
        assert _F["mh400_verdetto"](2.25).startswith("DIVERSIFICATO")
        assert _F["mh400_verdetto"](2.24).startswith("BILANCIATO")
        assert _F["mh400_verdetto"](1.5).startswith("BILANCIATO")
        assert _F["mh400_verdetto"](1.49).startswith("CONCENTRATO")
        assert _F["mh400_verdetto"](1.0).startswith("CONCENTRATO")

    def test_dr_maggiore_uguale_1(self):
        m = self._demo()
        assert m["dr"] >= 1.0 - 1e-12

    def test_mappa_eur(self):
        m = self._demo()
        assert abs(m["sig_eur"] - m["sig"] * 5.0e6) / m["sig_eur"] < 1e-12
        assert abs(sum(m["w_pct"]) - 100.0) < 1e-9
        assert abs(sum(m["rc_eur"]) - m["sig_eur"]) / m["sig_eur"] < 1e-12

    def test_rc_negativo_non_definito(self):
        with pytest.raises(ValueError):
            _F["mh400_distribuzione"]((0.1, -0.05, 0.2), 0.25)

    def test_casi_degeneri(self):
        for _bad in (lambda: _F["mh400_num"](True, "x"),
                     lambda: _F["mh400_num"](float("nan"), "x"),
                     lambda: _F["mh400_num"](float("inf"), "x"),
                     lambda: _F["mh400_num"]("a", "x"),
                     lambda: _F["mh400_check_vol"](2.5),
                     lambda: _F["mh400_check_vol"](-0.1),
                     lambda: _F["mh400_check_rho"](1.5),
                     lambda: _F["mh400_check_w"]((0.0, 0.0, 0.0)),
                     lambda: _F["mh400_check_w"]((-1.0, 2.0, 1.0)),
                     lambda: _F["mh400_check_w"]((1.0, 2.0)),
                     lambda: _F["mh400_covmat"]((0.2, 0.2, 0.2),
                                                0.9, 0.9, -0.9),
                     lambda: _F["mh400_eulero"](
                         (0.0, 0.0, 0.0),
                         ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0),
                          (0.0, 0.0, 1.0))),
                     lambda: _F["mh400_distribuzione"](
                         (0.1, -0.05, 0.2), 0.25),
                     lambda: _F["mh400_enb"]((0.5, 0.5, 0.5)),
                     lambda: _F["mh400_enb"]((-0.1, 0.6, 0.5)),
                     lambda: _F["mh400_enb"](()),
                     lambda: _F["mh400_verdetto"](2.0, 0),
                     lambda: _F["mh400_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (W1, W2, W3), 0.0)):
            with pytest.raises(ValueError):
                _bad()
