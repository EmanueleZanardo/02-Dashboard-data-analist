"""Test tab404 '🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh404_num", "mh404_check_vol", "mh404_check_rho",
           "mh404_check_mu", "mh404_check_target", "mh404_check_w",
           "mh404_covmat", "mh404_sig", "mh404_rendimento",
           "mh404_risolvi", "mh404_risolvi2", "mh404_minvar",
           "mh404_mintarget", "mh404_verdetto", "mh404_mappa")

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
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
V1 = 0.25
V2 = 0.35
V3 = 0.3
R12 = 0.4
R13 = 0.2
R23 = 0.3
MU1 = 0.08
MU2 = 0.12
MU3 = 0.06
W1 = 0.2
W2 = 0.3
W3 = 0.5
TARGET = 0.09
W1S = 0.4743918053777209
W2S = 0.3418693982074263
W3S = 0.1837387964148528
SIGSTAR = 0.2221393046685281
SIGCUR = 0.22951034835057002
MUCUR = 0.08199999999999999
GAP = -0.008000000000000007


class TestRegistry404:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 765
        assert "tab404" in dvars
        assert "tab404" in withs

    def test_titoli_allineati_399_400_401_402_403_404(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab399")] == TITLE399
        assert titoli[dvars.index("tab400")] == TITLE400
        assert titoli[dvars.index("tab401")] == TITLE401
        assert titoli[dvars.index("tab402")] == TITLE402
        assert titoli[dvars.index("tab403")] == TITLE403
        assert titoli[dvars.index("tab404")] == TITLE404

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


class TestTargetReturn404:
    def _demo(self):
        return _F["mh404_mappa"]((V1, V2, V3), R12, R13, R23,
                                 (MU1, MU2, MU3), (W1, W2, W3),
                                 TARGET, 5.0)

    def test_demo_valori(self):
        m = self._demo()
        assert abs(m["mu_cur"] - MUCUR) < 1e-12
        assert abs(m["gap"] - GAP) < 1e-12
        assert abs(m["gap"] - (MUCUR - TARGET)) < 1e-12
        assert abs(m["sig_star"] - SIGSTAR) / SIGSTAR < 1e-12
        assert abs(m["sig_cur"] - SIGCUR) / SIGCUR < 1e-12
        assert m["verdetto"].startswith("SOTTO TARGET")

    def test_demo_pesi_tr(self):
        m = self._demo()
        for _g, _e in zip(m["w_tr"], (W1S, W2S, W3S)):
            assert abs(_g - _e) < 1e-12
        assert abs(sum(m["w_tr"]) - 1.0) < 1e-12
        assert min(m["w_tr"]) >= 0.0
        assert abs(sum(m["delta_pp"])) < 1e-9
        # il vincolo di rendimento e' rispettato
        assert abs(sum(m["w_tr"][i] * (MU1, MU2, MU3)[i]
                       for i in range(3)) - TARGET) < 1e-9

    def test_estremi_target_sono_angoli(self):
        # target = min mu -> tutto sull'asset a rendimento minimo
        w = _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3), MU3)
        for _g, _e in zip(w, (0.0, 0.0, 1.0)):
            assert abs(_g - _e) < 1e-9
        # target = max mu -> tutto sull'asset a rendimento massimo
        w = _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3), MU2)
        for _g, _e in zip(w, (0.0, 1.0, 0.0)):
            assert abs(_g - _e) < 1e-9

    def test_simmetria_pesi_uguali(self):
        w = _F["mh404_mintarget"]((0.3, 0.3, 0.3), 0.0, 0.0, 0.0,
                                  (0.08, 0.08, 0.08), 0.08)
        for _g in w:
            assert abs(_g - 1.0 / 3.0) < 1e-9

    def test_condizione_kkt(self):
        # condizione del primo ordine (indipendente dal two-fund):
        # all'ottimo il gradiente S w sta in span{1, mu}
        S = _F["mh404_covmat"]((V1, V2, V3), R12, R13, R23)
        w = _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3), TARGET)
        g = [sum(S[i][j] * w[j] for j in range(3)) for i in range(3)]
        one = (1.0, 1.0, 1.0)
        mu = (MU1, MU2, MU3)
        s11 = sum(one[i] * one[i] for i in range(3))
        s12 = sum(one[i] * mu[i] for i in range(3))
        s22 = sum(mu[i] * mu[i] for i in range(3))
        t1 = sum(one[i] * g[i] for i in range(3))
        t2 = sum(mu[i] * g[i] for i in range(3))
        a, b = _F["mh404_risolvi2"](((s11, s12), (s12, s22)), (t1, t2))
        assert max(abs(g[i] - a * one[i] - b * mu[i])
                   for i in range(3)) < 1e-9

    def test_ottimalita_differenze_finite(self):
        # nessuna perturbazione ammissibile (somma=1, w'mu=target)
        # riduce la varianza
        S = _F["mh404_covmat"]((V1, V2, V3), R12, R13, R23)
        w = _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3), TARGET)
        s0 = _F["mh404_sig"](w, S)
        mu = (MU1, MU2, MU3)
        one = (1.0, 1.0, 1.0)
        d = (one[1] * mu[2] - one[2] * mu[1],
             one[2] * mu[0] - one[0] * mu[2],
             one[0] * mu[1] - one[1] * mu[0])
        assert abs(sum(d)) < 1e-12
        assert abs(sum(d[i] * mu[i] for i in range(3))) < 1e-12
        for _e in (1e-5, -1e-5):
            wp = tuple(w[i] + _e * d[i] for i in range(3))
            if min(wp) < 0.0:
                continue
            assert _F["mh404_sig"](wp, S) <= s0 * (1.0 + 1e-9)

    def test_target_fuori_range_non_raggiungibile(self):
        with pytest.raises(ValueError):
            _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3), 0.15)
        with pytest.raises(ValueError):
            _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (MU1, MU2, MU3), 0.01)

    def test_pesi_negativi_non_longonly(self):
        # rho Power-Gas 0.9, target 11.5%: la forma chiusa vorrebbe
        # short -> ValueError
        with pytest.raises(ValueError):
            _F["mh404_mintarget"]((0.25, 0.35, 0.30), 0.9, 0.2, 0.3,
                                  (0.08, 0.12, 0.06), 0.115)

    def test_mu_uguali(self):
        # mu costanti: target == mu -> ricade sulla min-var classica
        w = _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (0.08, 0.08, 0.08), 0.08)
        wmv = _F["mh404_minvar"]((V1, V2, V3), R12, R13, R23)
        for _g, _e in zip(w, wmv):
            assert abs(_g - _e) < 1e-12
        # target diverso -> non raggiungibile
        with pytest.raises(ValueError):
            _F["mh404_mintarget"]((V1, V2, V3), R12, R13, R23,
                                  (0.08, 0.08, 0.08), 0.09)

    def test_singolare_non_definito(self):
        # vol nulla -> covarianza singolare -> ValueError
        with pytest.raises(ValueError):
            _F["mh404_mintarget"]((0.25, 0.0, 0.30), 0.6, 0.3, 0.45,
                                  (0.08, 0.12, 0.06), 0.09)

    def test_risolvi2_identita_e_singolare(self):
        _x = _F["mh404_risolvi2"](((1.0, 0.0), (0.0, 1.0)), (0.08, 0.12))
        assert abs(_x[0] - 0.08) < 1e-12
        assert abs(_x[1] - 0.12) < 1e-12
        with pytest.raises(ValueError):
            _F["mh404_risolvi2"](((1.0, 1.0), (1.0, 1.0)), (1.0, 2.0))

    def test_verdetto_stati_e_bordi(self):
        assert _F["mh404_verdetto"](0.01).startswith("TARGET RAGGIUNTO")
        assert _F["mh404_verdetto"](0.0).startswith("TARGET RAGGIUNTO")
        assert _F["mh404_verdetto"](-0.004).startswith("QUASI")
        assert _F["mh404_verdetto"](-0.005).startswith("QUASI")
        assert _F["mh404_verdetto"](-0.0051).startswith("SOTTO TARGET")
        assert _F["mh404_verdetto"](-0.05).startswith("SOTTO TARGET")

    def test_mappa_eur(self):
        m = self._demo()
        assert abs(m["sig_cur_eur"] - m["sig_cur"] * 5.0e6) \
            / m["sig_cur_eur"] < 1e-12
        assert abs(m["sig_star_eur"] - m["sig_star"] * 5.0e6) \
            / m["sig_star_eur"] < 1e-12
        assert abs(sum(m["w_pct"]) - 100.0) < 1e-9
        assert abs(sum(m["w_tr_pct"]) - 100.0) < 1e-9
        assert abs(m["target"] - TARGET) < 1e-12

    def test_casi_degeneri(self):
        for _bad in (lambda: _F["mh404_num"](True, "x"),
                     lambda: _F["mh404_num"](float("nan"), "x"),
                     lambda: _F["mh404_num"](float("inf"), "x"),
                     lambda: _F["mh404_num"]("a", "x"),
                     lambda: _F["mh404_check_vol"](2.5),
                     lambda: _F["mh404_check_vol"](-0.1),
                     lambda: _F["mh404_check_rho"](1.5),
                     lambda: _F["mh404_check_mu"](2.5),
                     lambda: _F["mh404_check_mu"](-1.5),
                     lambda: _F["mh404_check_target"](2.5),
                     lambda: _F["mh404_check_target"](-1.5),
                     lambda: _F["mh404_check_w"]((0.0, 0.0, 0.0)),
                     lambda: _F["mh404_check_w"]((-1.0, 2.0, 1.0)),
                     lambda: _F["mh404_check_w"]((1.0, 2.0)),
                     lambda: _F["mh404_covmat"]((0.2, 0.2, 0.2),
                                                0.9, 0.9, -0.9),
                     lambda: _F["mh404_rendimento"]((1.0, 0.0, 0.0),
                                                    (0.1, 0.1)),
                     lambda: _F["mh404_risolvi"](
                         ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0),
                          (1.0, 1.0, 1.0)), (1.0, 2.0, 3.0)),
                     lambda: _F["mh404_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (MU1, MU2, MU3), (W1, W2, W3), 0.15, 5.0),
                     lambda: _F["mh404_mappa"](
                         (V1, V2, V3), R12, R13, R23,
                         (MU1, MU2, MU3), (W1, W2, W3), TARGET, 0.0)):
            with pytest.raises(ValueError):
                _bad()

