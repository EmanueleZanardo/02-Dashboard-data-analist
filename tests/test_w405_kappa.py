"""Test tab405 'κ Kappa ratio: un'unica famiglia per Omega e Sortino': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh405_num", "mh405_check_n", "mh405_parse_serie",
           "mh405_media", "mh405_lpm", "mh405_upm", "mh405_kappa",
           "mh405_omega", "mh405_sortino", "mh405_verdetto",
           "mh405_mappa")

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
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
DEMO = '1.2\n-0.8\n2.1\n0.5\n-1.5\n3.2\n0.8\n-2.2\n1.7\n5.4\n0.3\n-1.1\n2.6\n1.1\n-0.6\n4.1\n0.9\n-1.8\n2.3\n0.4\n6.2\n-0.9\n1.5\n2.8\n-2.5\n1.0\n0.7\n-1.2\n3.6\n1.4\n-0.4\n2.0\n0.6\n-1.6\n4.8\n1.9'
MEDIA = 1.0694444444444444
K1 = 2.636986301369863
K2 = 1.3163951118623083
K3 = 0.9990697758646013
K4 = 0.852015661478278
LPM1 = 0.40555555555555556
LPM2 = 0.66
UPM1 = 1.475
OMEGA = 3.636986301369863
SORTINO = 1.3163951118623083


class TestRegistry405:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 520
        assert "tab405" in dvars
        assert "tab405" in withs

    def test_titoli_allineati_400_401_402_403_404_405(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab400")] == TITLE400
        assert titoli[dvars.index("tab401")] == TITLE401
        assert titoli[dvars.index("tab402")] == TITLE402
        assert titoli[dvars.index("tab403")] == TITLE403
        assert titoli[dvars.index("tab404")] == TITLE404
        assert titoli[dvars.index("tab405")] == TITLE405

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


class TestKappa405:
    def _xs(self):
        return _F["mh405_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh405_mappa"](xs, 0.0, 2)
        assert abs(m["media"] - MEDIA) < 1e-12
        assert abs(m["kappa"] - K2) < 1e-12
        assert abs(m["lpm"] - LPM2) < 1e-12
        assert abs(m["omega"] - OMEGA) < 1e-12
        assert abs(m["sortino"] - SORTINO) < 1e-12
        for _i, _e in zip((1, 2, 3, 4), (K1, K2, K3, K4)):
            assert abs(m["famiglia"][_i] - _e) < 1e-12, _i
        assert m["verdetto"].startswith("SOPRA SOGLIA")

    def test_kappa1_uguale_omega_meno_1(self):
        # n=1: Kappa_1(T) = Omega(T) - 1 (controllo indipendente)
        xs = self._xs()
        k1 = _F["mh405_kappa"](xs, 0.0, 1)
        om = _F["mh405_omega"](xs, 0.0)
        assert abs(k1 - (om - 1.0)) < 1e-9
        assert abs(k1 - K1) < 1e-12

    def test_kappa2_uguale_sortino(self):
        # n=2: Kappa_2(T) = Sortino(T) (controllo indipendente)
        xs = self._xs()
        k2 = _F["mh405_kappa"](xs, 0.0, 2)
        so = _F["mh405_sortino"](xs, 0.0)
        assert abs(k2 - so) < 1e-12
        assert abs(k2 - K2) < 1e-12

    def test_monotonia_demo(self):
        # la serie demo ha skew positiva: ordini piu' alti penalizzano
        # le code -> Kappa decrescente in n
        xs = self._xs()
        ks = [_F["mh405_kappa"](xs, 0.0, i) for i in (1, 2, 3, 4)]
        assert ks[0] > ks[1] > ks[2] > ks[3] > 0.0

    def test_casi_degeneri(self):
        # serie costante sopra T -> nessun downside -> +inf
        xs = tuple([1.5] * 25)
        assert _F["mh405_kappa"](xs, 0.0, 2) == math.inf
        assert _F["mh405_sortino"](xs, 0.0) == math.inf
        # serie costante uguale a T -> excess 0, LPM 0 -> 0.0
        xs = tuple([0.0] * 25)
        assert _F["mh405_kappa"](xs, 0.0, 2) == 0.0
        # media sotto T -> Kappa negativo
        xs = tuple([-0.5] * 20 + [0.2] * 10)
        k = _F["mh405_kappa"](xs, 0.0, 2)
        assert k < 0.0
        assert _F["mh405_verdetto"](k).startswith("SOTTO SOGLIA")
        # soglia alta: media - T < 0 ma LPM piccolo
        xs = self._xs()
        k = _F["mh405_kappa"](xs, 6.5, 2)
        assert k < 0.0

    def test_parse_serie(self):
        xs = self._xs()
        assert len(xs) == 36
        assert abs(sum(xs) / len(xs) - MEDIA) < 1e-12
        # la virgola vale come separatore decimale
        xs2 = _F["mh405_parse_serie"](
            "\n".join(["1,5", "-0,25"] + ["0.0"] * 18))
        assert abs(xs2[0] - 1.5) < 1e-12
        assert abs(xs2[1] + 0.25) < 1e-12

    def test_verdetto_stati(self):
        assert _F["mh405_verdetto"](math.inf).startswith("PERFETTO")
        assert _F["mh405_verdetto"](1.5).startswith("SOPRA SOGLIA")
        assert _F["mh405_verdetto"](0.0).startswith("SULLA SOGLIA")
        assert _F["mh405_verdetto"](-0.7).startswith("SOTTO SOGLIA")
        with pytest.raises(ValueError):
            _F["mh405_verdetto"](True)

    def test_validatori(self):
        xs = self._xs()
        for _bad in (lambda: _F["mh405_check_n"](0),
                     lambda: _F["mh405_check_n"](5),
                     lambda: _F["mh405_check_n"](2.5),
                     lambda: _F["mh405_kappa"](xs, 0.0, 5),
                     lambda: _F["mh405_lpm"](xs, 0.0, 0),
                     lambda: _F["mh405_kappa"]((1.0,) * 19, 0.0, 2),
                     lambda: _F["mh405_media"]((1.0,) * 19),
                     lambda: _F["mh405_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh405_parse_serie"](
                         "\n".join(["abc"] + ["1.0"] * 20)),
                     lambda: _F["mh405_parse_serie"](
                         "\n".join(["nan"] + ["1.0"] * 20)),
                     lambda: _F["mh405_parse_serie"](None),
                     lambda: _F["mh405_num"](True, "x"),
                     lambda: _F["mh405_num"](float("nan"), "x"),
                     lambda: _F["mh405_num"]("a", "x"),
                     lambda: _F["mh405_mappa"](xs, float("nan"), 2)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh405_mappa"](DEMO, 0.0, 2)
        assert abs(m["kappa"] - K2) < 1e-12
        assert m["n_per"] == 36

