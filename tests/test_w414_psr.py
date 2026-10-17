"""Test tab414 '🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh414_num", "mh414_parse_serie", "mh414_phi", "mh414_stats",
           "mh414_sigma2", "mh414_psr_da_stat", "mh414_verdetto",
           "mh414_mappa")

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
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
PSR = 0.8981260210565327
PSR_N = 0.9449323153940414
SIG = 1.2570048886573466
MINTRL = 59.62306872222972


class TestRegistry414:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 522
        assert "tab414" in dvars
        assert "tab414" in withs

    def test_titoli_allineati_409_410_411_412_413_414(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410
        assert titoli[dvars.index("tab411")] == TITLE411
        assert titoli[dvars.index("tab412")] == TITLE412
        assert titoli[dvars.index("tab413")] == TITLE413
        assert titoli[dvars.index("tab414")] == TITLE414

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


class TestPSR414:
    def _xs(self):
        return _F["mh414_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh414_mappa"](xs)
        assert abs(m["psr"] - PSR) < 1e-12
        assert abs(m["psr_norm"] - PSR_N) < 1e-12
        assert abs(m["sigma"] - SIG) < 1e-12
        assert abs(m["mintrl"] - MINTRL) < 1e-9
        assert m["n_per"] == 36
        assert m["rf"] == 0.0
        assert m["sr0"] == 0.0
        # 0.8981 -> ACCETTABILE: evidenza ma non significativita' al 95%
        assert m["verdetto"].startswith("ACCETTABILE")
        # le code grasse tagliano quasi 5pp di confidenza vs normale
        assert m["haircut_pp"] > 4.0
        # MinTRL: servono ~60 periodi, contro ~38 dell'ipotesi normale
        assert m["mintrl"] > 55.0

    def test_definizione_psr_a_mano(self):
        # sigma_SR^2 = 1-sk*SR+((ku-1)/4)*SR^2; PSR = Phi(SR*sqrt(n-1)/sig)
        xs = list(self._xs())
        n = len(xs)
        mu = sum(xs) / n
        ss = sum((x - mu) ** 2 for x in xs)
        vpop = ss / n
        std = math.sqrt(ss / (n - 1))
        sk = (sum((x - mu) ** 3 for x in xs) / n) / (vpop ** 1.5)
        ku = (sum((x - mu) ** 4 for x in xs) / n) / (vpop ** 2)
        sr = mu / std
        s2 = 1.0 - sk * sr + ((ku - 1.0) / 4.0) * sr ** 2
        z = sr * math.sqrt(n - 1) / math.sqrt(s2)
        psr = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        z_n = sr * math.sqrt(n - 1)
        psr_n = 0.5 * (1.0 + math.erf(z_n / math.sqrt(2.0)))
        p = _F["mh414_psr_da_stat"](_F["mh414_stats"](tuple(xs), 0.0), 0.0)
        assert abs(p["sigma2"] - s2) < 1e-12
        assert abs(p["z"] - z) < 1e-12
        assert abs(p["psr"] - psr) < 1e-12
        assert abs(p["psr_norm"] - psr_n) < 1e-12
        assert abs(p["haircut_pp"] - (psr_n - psr) * 100.0) < 1e-12

    def test_phi(self):
        assert abs(_F["mh414_phi"](0.0) - 0.5) < 1e-15
        assert abs(_F["mh414_phi"](1.6448536269514722) - 0.95) < 1e-9
        assert abs(_F["mh414_phi"](10.0) - 1.0) < 1e-12
        assert _F["mh414_phi"](-10.0) < 1e-12
        with pytest.raises(ValueError):
            _F["mh414_phi"](float("nan"))

    def test_sigma2(self):
        F = _F
        # momenti estremi -> ValueError (1 - 3 + 0.75 < 0)
        with pytest.raises(ValueError):
            F["mh414_sigma2"](3.0, 4.0, 1.0)
        # normalita' + SR=0 -> varianza esattamente 1
        assert abs(F["mh414_sigma2"](0.0, 3.0, 0.0) - 1.0) < 1e-12
        with pytest.raises(ValueError):
            F["mh414_sigma2"](float("nan"), 3.0, 0.5)
        with pytest.raises(ValueError):
            F["mh414_sigma2"](0.0, 3.0, True)

    def test_hurdle_e_mintrl(self):
        F = _F
        s = F["mh414_stats"](self._xs(), 0.0)
        pm = F["mh414_psr_da_stat"](s, -0.5)
        p0 = F["mh414_psr_da_stat"](s, 0.0)
        pp = F["mh414_psr_da_stat"](s, 0.5)
        # il PSR e' decrescente nell'hurdle
        assert pm["psr"] > p0["psr"] > pp["psr"]
        # hurdle >= Sharpe osservato -> MinTRL infinito (nessun T basta)
        assert math.isinf(F["mh414_psr_da_stat"](s, s["sharpe"])["mintrl"])
        assert math.isinf(F["mh414_psr_da_stat"](s, 5.0)["mintrl"])
        assert not math.isinf(p0["mintrl"])
        assert p0["mintrl"] > 1.0

    def test_serie_simmetrica_psr_quasi_normale(self):
        # serie quasi normale: la correzione code grasse resta ~neutra
        import random
        random.seed(7)
        xs = tuple(random.gauss(0.5, 2.0) for _ in range(60))
        s = _F["mh414_stats"](xs, 0.0)
        p = _F["mh414_psr_da_stat"](s, 0.0)
        assert abs(p["sigma"] - 1.0) < 0.15
        assert abs(p["psr"] - p["psr_norm"]) < 0.05

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh414_verdetto"](0.0).startswith("NON SIGNIFICATIVO")
        assert F["mh414_verdetto"](0.49).startswith("NON SIGNIFICATIVO")
        assert F["mh414_verdetto"](0.50).startswith("DEBOLE")
        assert F["mh414_verdetto"](0.74).startswith("DEBOLE")
        assert F["mh414_verdetto"](0.75).startswith("ACCETTABILE")
        assert F["mh414_verdetto"](0.899).startswith("ACCETTABILE")
        assert F["mh414_verdetto"](0.90).startswith("BUONO")
        assert F["mh414_verdetto"](0.949).startswith("BUONO")
        assert F["mh414_verdetto"](0.95).startswith("FORTE")
        assert F["mh414_verdetto"](0.989).startswith("FORTE")
        assert F["mh414_verdetto"](0.99).startswith("MOLTO FORTE")
        assert F["mh414_verdetto"](1.0).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh414_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh414_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta -> ValueError
        with pytest.raises(ValueError):
            F["mh414_stats"](tuple([1.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh414_mappa"](tuple([2.0] * 25), 2.0)
        with pytest.raises(ValueError):
            F["mh414_mappa"]((1.0,) * 19)
        # stats senza chiavi -> ValueError
        with pytest.raises(ValueError):
            F["mh414_psr_da_stat"]({}, 0.0)
        with pytest.raises(ValueError):
            F["mh414_psr_da_stat"]({"n": 36}, 0.0)

    def test_validatori(self):
        for _bad in (lambda: _F["mh414_stats"](None),
                     lambda: _F["mh414_stats"]((1.0,) * 19),
                     lambda: _F["mh414_stats"]((1.0,) * 25,
                                               float("nan")),
                     lambda: _F["mh414_stats"](tuple([3.0] * 25), 0.0),
                     lambda: _F["mh414_sigma2"](float("nan"), 3.0, 0.5),
                     lambda: _F["mh414_sigma2"](3.0, 4.0, 1.0),
                     lambda: _F["mh414_psr_da_stat"](None, 0.0),
                     lambda: _F["mh414_psr_da_stat"](
                         {"n": 36, "sharpe": 0.2, "skew": 0.0,
                          "kurt": 3.0}, float("nan")),
                     lambda: _F["mh414_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh414_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh414_parse_serie"](None),
                     lambda: _F["mh414_phi"](float("inf")),
                     lambda: _F["mh414_num"](True, "x"),
                     lambda: _F["mh414_num"](float("nan"), "x"),
                     lambda: _F["mh414_mappa"]((1.0,) * 19),
                     lambda: _F["mh414_mappa"](None),
                     lambda: _F["mh414_mappa"](tuple([1.0] * 25), "xx")):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh414_mappa"](DEMO)
        assert abs(m["psr"] - PSR) < 1e-12
        assert m["n_per"] == 36

