"""Test tab401 '📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh401_num", "mh401_check_vol", "mh401_check_rho",
           "mh401_check_w", "mh401_covmat", "mh401_sig", "mh401_dr",
           "mh401_risolvi", "mh401_maxdiv", "mh401_verdetto",
           "mh401_mappa")

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
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.6
R13 = 0.3
R23 = 0.45
W1 = 0.3333333333333333
W2 = 0.3333333333333333
W3 = 0.3333333333333333
DRMAX = 1.2666942131536318
DREQ = 1.248675910842206
W1MD = 0.42555685814771393
W2MD = 0.17584994138335283
W3MD = 0.3985932004689332
SIGP = 0.24025449469723187
EFF = 0.9857753338380173


class TestRegistry401:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 535
        assert "tab401" in dvars
        assert "tab401" in withs

    def test_titoli_allineati_396_397_398_399_400_401(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397
        assert titoli[dvars.index("tab398")] == TITLE398
        assert titoli[dvars.index("tab399")] == TITLE399
        assert titoli[dvars.index("tab400")] == TITLE400
        assert titoli[dvars.index("tab401")] == TITLE401

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


class TestMaxdiv401:
    def _demo(self):
        return _F["mh401_mappa"]((V1, V2, V3), R12, R13, R23,
                                 (W1, W2, W3), 5.0)

    def test_demo_dr_max(self):
        m = self._demo()
        assert abs(m["dr_max"] - DRMAX) / DRMAX < 1e-12
        assert abs(m["dr"] - DREQ) / DREQ < 1e-12
        assert abs(m["eff"] - EFF) < 1e-12
        assert abs(m["eff"] - DREQ / DRMAX) < 1e-12
        assert m["verdetto"].startswith("OTTIMALE")

    def test_demo_pesi_md(self):
        m = self._demo()
        for _g, _e in zip(m["w_md"], (W1MD, W2MD, W3MD)):
            assert abs(_g - _e) < 1e-12
        assert abs(sum(m["w_md"]) - 1.0) < 1e-12
        assert min(m["w_md"]) >= 0.0
        assert abs(sum(m["delta_pp"])) < 1e-9

    def test_dr_max_almeno_dr_uguali_e_uno(self):
        m = self._demo()
        assert m["dr_max"] >= m["dr"] - 1e-12
        assert m["dr_max"] >= 1.0 - 1e-12
        assert 0.0 < m["eff"] <= 1.0 + 1e-12

    def test_simmetria_pesi_uguali(self):
        w = _F["mh401_maxdiv"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0)
        for _g in w:
            assert abs(_g - 1.0 / 3.0) < 1e-9

    def test_ottimalita_differenze_finite(self):
        # la forma chiusa deve essere un massimo locale del DR:
        # nessuna perturbazione ammissibile lo aumenta
        S = _F["mh401_covmat"]((V1, V2, V3), R12, R13, R23)
        w = _F["mh401_maxdiv"]((V1, V2, V3), R12, R13, R23)
        dr0 = _F["mh401_dr"](w, S)
        for _i in range(3):
            for _j in range(3):
                if _i == _j:
                    continue
                _e = [0.0, 0.0, 0.0]
                _e[_i] = 1e-5
                _e[_j] = -1e-5
                _wp = tuple(w[_k] + _e[_k] for _k in range(3))
                if min(_wp) < 0.0:
                    continue
                assert _F["mh401_dr"](_wp, S) <= dr0 * (1.0 + 1e-9)

    def test_dr_max_batte_pesi_fissi(self):
        S = _F["mh401_covmat"]((V1, V2, V3), R12, R13, R23)
        dr0 = _F["mh401_dr"](
            _F["mh401_maxdiv"]((V1, V2, V3), R12, R13, R23), S)
        for _w in ((0.9, 0.05, 0.05), (0.05, 0.9, 0.05),
                   (0.05, 0.05, 0.9), (0.2, 0.3, 0.5),
                   (0.6, 0.2, 0.2)):
            assert dr0 >= _F["mh401_dr"](_w, S) - 1e-12

    def test_singolare_non_definito(self):
        # vol nulla -> covarianza singolare -> ValueError
        with pytest.raises(ValueError):
            _F["mh401_maxdiv"]((0.25, 0.0, 0.30), 0.6, 0.3, 0.45)

    def test_pesi_negativi_non_longonly(self):
        # correlazioni estreme: la forma chiusa vuole uno short
        with pytest.raises(ValueError):
            _F["mh401_maxdiv"]((0.2, 0.2, 0.6), 0.9, 0.95, 0.99)

    def test_risolvi_identita_e_singolare(self):
        _x = _F["mh401_risolvi"](
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            (0.25, 0.35, 0.30))
        for _g, _e in zip(_x, (0.25, 0.35, 0.30)):
            assert abs(_g - _e) < 1e-12
        with pytest.raises(ValueError):
            _F["mh401_risolvi"](
                ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
                (1.0, 2.0, 3.0))

    def test_dr_sig_nulla_non_definito(self):
        with pytest.raises(ValueError):
            _F["mh401_dr"]((1.0, 0.0, 0.0),
                           ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0),
                            (0.0, 0.0, 0.0)))

    def test_verdetto_stati_e_bordi(self):
        assert _F["mh401_verdetto"](1.0).startswith("OTTIMALE")
        assert _F["mh401_verdetto"](0.98).startswith("OTTIMALE")
        assert _F["mh401_verdetto"](0.979).startswith("BUONO")
        assert _F["mh401_verdetto"](0.90).startswith("BUONO")
        assert _F["mh401_verdetto"](0.899).startswith("DA OTTIMIZZARE")
        assert _F["mh401_verdetto"](0.5).startswith("DA OTTIMIZZARE")

    def test_mappa_eur(self):
        m = self._demo()
        assert abs(m["sig_eur"] - m["sig"] * 5.0e6) / m["sig_eur"] < 1e-12
        assert abs(sum(m["w_pct"]) - 100.0) < 1e-9
        assert abs(sum(m["w_md_pct"]) - 100.0) < 1e-9
        assert abs(m["guadagno"] - (m["dr_max"] / m["dr"] - 1.0)) < 1e-12

    def test_casi_degeneri(self):
        for _bad in (lambda: _F["mh401_num"](True, "x"),
                     lambda: _F["mh401_num"](float("nan"), "x"),
                     lambda: _F["mh401_num"](float("inf"), "x"),
                     lambda: _F["mh401_num"]("a", "x"),
                     lambda: _F["mh401_check_vol"](2.5),
                     lambda: _F["mh401_check_vol"](-0.1),
                     lambda: _F["mh401_check_rho"](1.5),
                     lambda: _F["mh401_check_w"]((0.0, 0.0, 0.0)),
                     lambda: _F["mh401_check_w"]((-1.0, 2.0, 1.0)),
                     lambda: _F["mh401_check_w"]((1.0, 2.0)),
                     lambda: _F["mh401_covmat"]((0.2, 0.2, 0.2),
                                                0.9, 0.9, -0.9),
                     lambda: _F["mh401_verdetto"](0.0),
                     lambda: _F["mh401_verdetto"](1.5),
                     lambda: _F["mh401_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (W1, W2, W3), 0.0)):
            with pytest.raises(ValueError):
                _bad()
