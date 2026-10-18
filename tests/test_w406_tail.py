"""Test tab406 '📏 Tail ratio: la coda destra contro la sinistra': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh406_num", "mh406_check_q", "mh406_parse_serie",
           "mh406_percentile", "mh406_tail_ratio", "mh406_verdetto",
           "mh406_mappa")

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
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
DEMO = '-2.4\n-1.9\n-1.6\n-1.2\n-0.9\n-0.7\n-0.5\n-0.3\n-0.2\n-0.1\n0.0\n0.1\n0.2\n0.4\n0.5\n0.6\n0.8\n0.9\n1.0\n1.1\n1.3\n1.4\n1.5\n1.7\n1.8\n2.0\n2.1\n2.2\n2.4\n2.5\n2.7\n2.9\n3.1\n6.4\n7.8\n9.5'
Q = 95
TR = 4.029850746268656
P_UP = 6.750000000000001
P_LO = -1.6750000000000003
MEDIA = 1.3083333333333333


class TestRegistry406:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 541
        assert "tab406" in dvars
        assert "tab406" in withs

    def test_titoli_allineati_401_402_403_404_405_406(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab401")] == TITLE401
        assert titoli[dvars.index("tab402")] == TITLE402
        assert titoli[dvars.index("tab403")] == TITLE403
        assert titoli[dvars.index("tab404")] == TITLE404
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406

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


class TestTail406:
    def _xs(self):
        return _F["mh406_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh406_mappa"](xs, Q)
        assert abs(m["p_up"] - P_UP) < 1e-12
        assert abs(m["p_lo"] - P_LO) < 1e-12
        assert abs(m["tail_ratio"] - TR) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert m["n_per"] == 36
        assert m["verdetto"].startswith("CODA DESTRA DOMINANTE")

    def test_percentile_vs_numpy(self):
        # controllo indipendente: interpolazione lineare == np.percentile
        xs = list(self._xs())
        for q in (5, 25, 50, 75, 90, 95, 99):
            mine = _F["mh406_percentile"](xs, q)
            ref = float(np.percentile(xs, q))
            assert abs(mine - ref) < 1e-9, q

    def test_simmetria(self):
        # campione simmetrico -> P95 = -P5 -> TR == 1
        xs = tuple(float(i) for i in range(-12, 13))
        assert len(xs) == 25
        tr = _F["mh406_tail_ratio"](xs, 95.0)
        assert abs(tr - 1.0) < 1e-9
        assert _F["mh406_verdetto"](tr).startswith("CODE BILANCIATE")

    def test_reciproco_serie_negata(self):
        # negare la serie scambia le code: TR_neg = 1 / TR
        xs = self._xs()
        tr = _F["mh406_tail_ratio"](xs, 95.0)
        tr_neg = _F["mh406_tail_ratio"](tuple(-v for v in xs), 95.0)
        assert abs(tr_neg - 1.0 / tr) < 1e-9
        assert tr_neg < 0.8
        assert _F["mh406_verdetto"](tr_neg).startswith("CODA SINISTRA")

    def test_casi_degeneri(self):
        # serie costante positiva -> P5 = P95 -> TR = 1
        xs = tuple([1.5] * 25)
        assert _F["mh406_tail_ratio"](xs, 95.0) == 1.0
        # P5 = 0 con P95 > 0 -> +inf (nessuna coda sinistra)
        xs = tuple([0.0] * 20 + [2.0] * 16)
        tr = _F["mh406_tail_ratio"](xs, 95.0)
        assert tr == math.inf
        assert _F["mh406_verdetto"](tr).startswith("NESSUNA CODA SINISTRA")
        # serie piatta a 0 -> 0.0
        assert _F["mh406_tail_ratio"](tuple([0.0] * 25), 95.0) == 0.0

    def test_verdetto_stati(self):
        assert _F["mh406_verdetto"](math.inf).startswith("NESSUNA CODA SINISTRA")
        assert _F["mh406_verdetto"](2.5).startswith("CODA DESTRA DOMINANTE")
        assert _F["mh406_verdetto"](1.0).startswith("CODE BILANCIATE")
        assert _F["mh406_verdetto"](0.5).startswith("CODA SINISTRA DOMINANTE")
        with pytest.raises(ValueError):
            _F["mh406_verdetto"](True)
        with pytest.raises(ValueError):
            _F["mh406_verdetto"](float("nan"))

    def test_validatori(self):
        xs = self._xs()
        for _bad in (lambda: _F["mh406_check_q"](50),
                     lambda: _F["mh406_check_q"](100),
                     lambda: _F["mh406_check_q"](40),
                     lambda: _F["mh406_tail_ratio"](xs, 50.0),
                     lambda: _F["mh406_tail_ratio"](xs, 99.9 + 0.2),
                     lambda: _F["mh406_percentile"](xs, -1),
                     lambda: _F["mh406_percentile"](xs, 101),
                     lambda: _F["mh406_percentile"]((1.0,) * 19, 95),
                     lambda: _F["mh406_tail_ratio"]((1.0,) * 19, 95.0),
                     lambda: _F["mh406_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh406_parse_serie"](
                         "\n".join(["abc"] + ["1.0"] * 20)),
                     lambda: _F["mh406_parse_serie"](None),
                     lambda: _F["mh406_num"](True, "x"),
                     lambda: _F["mh406_num"](float("nan"), "x"),
                     lambda: _F["mh406_num"]("a", "x"),
                     lambda: _F["mh406_mappa"](xs, float("nan"))):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh406_mappa"](DEMO, Q)
        assert abs(m["tail_ratio"] - TR) < 1e-12
        assert m["n_per"] == 36

