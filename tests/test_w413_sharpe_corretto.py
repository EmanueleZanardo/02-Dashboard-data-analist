"""Test tab413 '📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh413_num", "mh413_parse_serie", "mh413_sharpe_adj",
           "mh413_verdetto", "mh413_mappa")

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
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
SR = 0.27004115025880615
SKEW = -1.8729294803633167
KURT = 2.0752053895871434
CORR = 0.9093999702180136
ADJ = 0.24557541400299643


class TestRegistry413:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 776
        assert "tab413" in dvars
        assert "tab413" in withs

    def test_titoli_allineati_408_409_410_411_412_413(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410
        assert titoli[dvars.index("tab411")] == TITLE411
        assert titoli[dvars.index("tab412")] == TITLE412
        assert titoli[dvars.index("tab413")] == TITLE413

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


class TestSharpeAdj413:
    def _xs(self):
        return _F["mh413_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh413_mappa"](xs)
        assert abs(m["sharpe"] - SR) < 1e-12
        assert abs(m["skew"] - SKEW) < 1e-12
        assert abs(m["kurt_ecc"] - KURT) < 1e-12
        assert abs(m["correzione"] - CORR) < 1e-12
        assert abs(m["adj_sharpe"] - ADJ) < 1e-12
        assert m["n_per"] == 36
        assert m["rf"] == 0.0
        # la correzione taglia quasi un decimo e CAMBIA il verdetto:
        # SR classico -> ACCETTABILE, ASR -> DEBOLE
        assert m["verdetto"].startswith("DEBOLE")
        assert _F["mh413_verdetto"](m["sharpe"],
                                    m["sharpe"]).startswith("ACCETTABILE")

    def test_pezier_white_definizione(self):
        # ASR = SR * [1 + (skew/6)*SR - (kurt_ecc/24)*SR^2], a mano
        xs = list(self._xs())
        n = len(xs)
        mu = sum(xs) / n
        ss = sum((x - mu) ** 2 for x in xs)
        vpop = ss / n
        std = math.sqrt(ss / (n - 1))
        sk = (sum((x - mu) ** 3 for x in xs) / n) / (vpop ** 1.5)
        ku = (sum((x - mu) ** 4 for x in xs) / n) / (vpop ** 2) - 3.0
        sr = mu / std
        corr = 1.0 + (sk / 6.0) * sr - (ku / 24.0) * sr ** 2
        s = _F["mh413_sharpe_adj"](tuple(xs), 0.0)
        assert abs(s["skew"] - sk) < 1e-12
        assert abs(s["kurt_ecc"] - ku) < 1e-12
        assert abs(s["sharpe"] - sr) < 1e-12
        assert abs(s["correzione"] - corr) < 1e-12
        assert abs(s["adj_sharpe"] - sr * corr) < 1e-12
        assert abs(s["haircut_pct"] - (1.0 - corr) * 100.0) < 1e-12

    def test_serie_simmetrica_correzione_neutra(self):
        # serie quasi normale: la correzione resta ~1
        import random
        random.seed(7)
        xs = tuple(random.gauss(0.5, 2.0) for _ in range(60))
        s = _F["mh413_sharpe_adj"](xs, 0.0)
        assert abs(s["skew"]) < 0.6
        assert abs(s["correzione"] - 1.0) < 0.15

    def test_risk_free_sposta_gli_excess(self):
        xs = self._xs()
        s0 = _F["mh413_sharpe_adj"](xs, 0.0)
        s1 = _F["mh413_sharpe_adj"](xs, 1.0)
        assert abs((s0["media"] - s1["media"]) - 1.0) < 1e-12
        assert s1["rf"] == 1.0
        assert s1["sharpe"] < s0["sharpe"]

    def test_casi_degeneri(self):
        F = _F
        # serie piatta -> ValueError
        with pytest.raises(ValueError):
            F["mh413_sharpe_adj"](tuple([1.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh413_mappa"](tuple([2.0] * 25), 2.0)
        # soglie verdetto
        assert F["mh413_verdetto"](-0.1, 0.0).startswith("NEGATIVO")
        assert F["mh413_verdetto"](0.0, 0.0).startswith("DEBOLE")
        assert F["mh413_verdetto"](0.24, 0.0).startswith("DEBOLE")
        assert F["mh413_verdetto"](0.25, 0.0).startswith("ACCETTABILE")
        assert F["mh413_verdetto"](0.49, 0.0).startswith("ACCETTABILE")
        assert F["mh413_verdetto"](0.5, 0.0).startswith("BUONO")
        assert F["mh413_verdetto"](0.99, 0.0).startswith("BUONO")
        assert F["mh413_verdetto"](1.0, 0.0).startswith("OTTIMO")
        assert F["mh413_verdetto"](1.99, 0.0).startswith("OTTIMO")
        assert F["mh413_verdetto"](2.0, 0.0).startswith("ECCEZIONALE")
        assert F["mh413_verdetto"](5.0, 5.0).startswith("ECCEZIONALE")
        with pytest.raises(ValueError):
            F["mh413_verdetto"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh413_verdetto"](float("nan"), 0.0)
        with pytest.raises(ValueError):
            F["mh413_verdetto"](True, 0.0)
        with pytest.raises(ValueError):
            F["mh413_verdetto"](1.5, float("nan"))

    def test_validatori(self):
        for _bad in (lambda: _F["mh413_sharpe_adj"](None),
                     lambda: _F["mh413_sharpe_adj"]((1.0,) * 19),
                     lambda: _F["mh413_sharpe_adj"]((1.0,) * 25,
                                                   float("nan")),
                     lambda: _F["mh413_sharpe_adj"](tuple([3.0] * 25), 0.0),
                     lambda: _F["mh413_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh413_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh413_parse_serie"](None),
                     lambda: _F["mh413_num"](True, "x"),
                     lambda: _F["mh413_num"](float("nan"), "x"),
                     lambda: _F["mh413_mappa"]((1.0,) * 19),
                     lambda: _F["mh413_mappa"](None),
                     lambda: _F["mh413_mappa"](tuple([1.0] * 25), "xx")):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh413_mappa"](DEMO)
        assert abs(m["adj_sharpe"] - ADJ) < 1e-12
        assert m["n_per"] == 36

