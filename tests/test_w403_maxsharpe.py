"""Test tab403 '🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh403_num", "mh403_check_vol", "mh403_check_rho",
           "mh403_check_mu", "mh403_check_w", "mh403_covmat",
           "mh403_sig", "mh403_rendimento", "mh403_sharpe",
           "mh403_risolvi", "mh403_maxsharpe", "mh403_verdetto",
           "mh403_mappa")

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
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
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
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.4
R13 = 0.2
R23 = 0.3
MU1 = 0.08
MU2 = 0.12
MU3 = 0.06
W1 = 0.3333333333333333
W2 = 0.3333333333333333
W3 = 0.3333333333333333
SRSTAR = 0.4054637345304572
SREQ = 0.39285862539007466
EFF = 0.9689118703674454
W1MS = 0.4660101042399437
W2MS = 0.37003581249600304
W3MS = 0.16395408326405322
SIGP = 0.22060522810365726
MUP = 0.08666666666666666


class TestRegistry403:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 469
        assert "tab403" in dvars
        assert "tab403" in withs

    def test_titoli_allineati_398_399_400_401_402_403(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab398")] == TITLE398
        assert titoli[dvars.index("tab399")] == TITLE399
        assert titoli[dvars.index("tab400")] == TITLE400
        assert titoli[dvars.index("tab401")] == TITLE401
        assert titoli[dvars.index("tab402")] == TITLE402
        assert titoli[dvars.index("tab403")] == TITLE403

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab469"
        assert titoli[-1] == TITLE469
        assert withs[-1] == "tab469"


class TestMaxSharpe403:
    def _demo(self):
        return _F["mh403_mappa"]((V1, V2, V3), R12, R13, R23,
                                 (MU1, MU2, MU3), (W1, W2, W3), 5.0)

    def test_demo_sharpe_star(self):
        m = self._demo()
        assert abs(m["sr_star"] - SRSTAR) / SRSTAR < 1e-12
        assert abs(m["sr"] - SREQ) / SREQ < 1e-12
        assert abs(m["eff"] - EFF) < 1e-12
        assert abs(m["eff"] - SREQ / SRSTAR) < 1e-12
        assert abs(m["mu_p"] - MUP) / MUP < 1e-12
        assert m["verdetto"].startswith("BUONO")

    def test_demo_pesi_ms(self):
        m = self._demo()
        for _g, _e in zip(m["w_ms"], (W1MS, W2MS, W3MS)):
            assert abs(_g - _e) < 1e-12
        assert abs(sum(m["w_ms"]) - 1.0) < 1e-12
        assert min(m["w_ms"]) >= 0.0
        assert abs(sum(m["delta_pp"])) < 1e-9

    def test_sharpe_star_almeno_sharpe_uguali(self):
        m = self._demo()
        assert m["sr_star"] >= m["sr"] - 1e-12
        assert 0.0 < m["eff"] <= 1.0 + 1e-12
        assert m["gap"] >= -1e-12

    def test_simmetria_pesi_uguali(self):
        w = _F["mh403_maxsharpe"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0,
                                  (0.08, 0.08, 0.08))
        for _g in w:
            assert abs(_g - 1.0 / 3.0) < 1e-9

    def test_ottimalita_differenze_finite(self):
        # la forma chiusa deve essere un massimo locale dello Sharpe:
        # nessuna perturbazione ammissibile lo aumenta
        S = _F["mh403_covmat"]((V1, V2, V3), R12, R13, R23)
        w = _F["mh403_maxsharpe"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3))
        s0 = _F["mh403_sharpe"](w, (MU1, MU2, MU3), S)
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
                assert _F["mh403_sharpe"](_wp, (MU1, MU2, MU3), S) \
                    <= s0 * (1.0 + 1e-9)

    def test_maxsharpe_batte_pesi_fissi(self):
        S = _F["mh403_covmat"]((V1, V2, V3), R12, R13, R23)
        s0 = _F["mh403_sharpe"](
            _F["mh403_maxsharpe"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3)),
            (MU1, MU2, MU3), S)
        for _w in ((0.9, 0.05, 0.05), (0.05, 0.9, 0.05),
                   (0.05, 0.05, 0.9), (0.2, 0.3, 0.5),
                   (0.6, 0.2, 0.2)):
            assert s0 >= _F["mh403_sharpe"](_w, (MU1, MU2, MU3), S) - 1e-12

    def test_condizione_lagrange(self):
        # condizione del primo ordine (indipendente dalla forma chiusa):
        # all'ottimo (Sw)_i / mu_i e' costante su i
        S = _F["mh403_covmat"]((V1, V2, V3), R12, R13, R23)
        w = _F["mh403_maxsharpe"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3))
        _lg = [sum(S[i][j] * w[j] for j in range(3)) / (MU1, MU2, MU3)[i]
               for i in range(3)]
        assert max(_lg) - min(_lg) < 1e-9

    def test_singolare_non_definito(self):
        # vol nulla -> covarianza singolare -> ValueError
        with pytest.raises(ValueError):
            _F["mh403_maxsharpe"]((0.25, 0.0, 0.30), 0.6, 0.3, 0.45,
                                  (0.08, 0.12, 0.06))

    def test_mu_nulli_non_definiti(self):
        with pytest.raises(ValueError):
            _F["mh403_maxsharpe"]((0.25, 0.35, 0.30), 0.4, 0.2, 0.3,
                                  (0.0, 0.0, 0.0))

    def test_pesi_negativi_non_longonly(self):
        # mu=(2%,15%,3%): la forma chiusa vorrebbe short su
        # Power (-49%) e CO2 (-8%) -> ValueError
        with pytest.raises(ValueError):
            _F["mh403_maxsharpe"]((0.25, 0.35, 0.30), 0.4, 0.2, 0.3,
                                  (0.02, 0.15, 0.03))

    def test_risolvi_identita_e_singolare(self):
        _x = _F["mh403_risolvi"](
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            (0.08, 0.12, 0.06))
        for _g, _e in zip(_x, (0.08, 0.12, 0.06)):
            assert abs(_g - _e) < 1e-12
        with pytest.raises(ValueError):
            _F["mh403_risolvi"](
                ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)),
                (1.0, 2.0, 3.0))

    def test_verdetto_stati_e_bordi(self):
        assert _F["mh403_verdetto"](1.0).startswith("OTTIMALE")
        assert _F["mh403_verdetto"](0.98).startswith("OTTIMALE")
        assert _F["mh403_verdetto"](0.979).startswith("BUONO")
        assert _F["mh403_verdetto"](0.90).startswith("BUONO")
        assert _F["mh403_verdetto"](0.899).startswith("DA OTTIMIZZARE")
        assert _F["mh403_verdetto"](0.5).startswith("DA OTTIMIZZARE")

    def test_mappa_eur(self):
        m = self._demo()
        assert abs(m["sig_eur"] - m["sig"] * 5.0e6) / m["sig_eur"] < 1e-12
        assert abs(m["mu_p_eur"] - m["mu_p"] * 5.0e6) \
            / m["mu_p_eur"] < 1e-12
        assert abs(sum(m["w_pct"]) - 100.0) < 1e-9
        assert abs(sum(m["w_ms_pct"]) - 100.0) < 1e-9
        assert abs(m["gap"] - (1.0 - m["eff"])) < 1e-12
        assert abs(m["sr"] - m["mu_p"] / m["sig"]) < 1e-12

    def test_casi_degeneri(self):
        for _bad in (lambda: _F["mh403_num"](True, "x"),
                     lambda: _F["mh403_num"](float("nan"), "x"),
                     lambda: _F["mh403_num"](float("inf"), "x"),
                     lambda: _F["mh403_num"]("a", "x"),
                     lambda: _F["mh403_check_vol"](2.5),
                     lambda: _F["mh403_check_vol"](-0.1),
                     lambda: _F["mh403_check_rho"](1.5),
                     lambda: _F["mh403_check_mu"](2.5),
                     lambda: _F["mh403_check_mu"](-1.5),
                     lambda: _F["mh403_check_w"]((0.0, 0.0, 0.0)),
                     lambda: _F["mh403_check_w"]((-1.0, 2.0, 1.0)),
                     lambda: _F["mh403_check_w"]((1.0, 2.0)),
                     lambda: _F["mh403_covmat"]((0.2, 0.2, 0.2),
                                                0.9, 0.9, -0.9),
                     lambda: _F["mh403_rendimento"]((1.0, 0.0, 0.0),
                                                    (0.1, 0.1)),
                     lambda: _F["mh403_verdetto"](0.0),
                     lambda: _F["mh403_verdetto"](1.5),
                     lambda: _F["mh403_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (0.0, 0.0, 0.0), (W1, W2, W3), 5.0),
                     lambda: _F["mh403_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (MU1, MU2, MU3), (W1, W2, W3), 0.0)):
            with pytest.raises(ValueError):
                _bad()

