"""Test tab415 '🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh415_num", "mh415_parse_serie", "mh415_phi", "mh415_ppf",
           "mh415_stats", "mh415_sigma2", "mh415_e0",
           "mh415_dsr_da_stat", "mh415_verdetto", "mh415_mappa")

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
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
DEMO_K = 10
DEMO_V = 0.25
E0 = 0.7872991506728748
DSR = 0.007456825936989986
HAIRCUT = 89.06691951195427
BIAS = 2.9154784369653703
_GAM = 0.5772156649015329


class TestRegistry415:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 588
        assert "tab415" in dvars
        assert "tab415" in withs

    def test_titoli_allineati_410_411_412_413_414_415(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab410")] == TITLE410
        assert titoli[dvars.index("tab411")] == TITLE411
        assert titoli[dvars.index("tab412")] == TITLE412
        assert titoli[dvars.index("tab413")] == TITLE413
        assert titoli[dvars.index("tab414")] == TITLE414
        assert titoli[dvars.index("tab415")] == TITLE415

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


class TestDSR415:
    def _xs(self):
        return _F["mh415_parse_serie"](DEMO)

    def _fst_e0(self, K, V):
        # False Strategy Theorem indipendente (scipy): struttura identica,
        # quantile indipendente
        return math.sqrt(V) * ((1.0 - _GAM) * norm.ppf(1.0 - 1.0 / K)
                               + _GAM * norm.ppf(1.0 - 1.0 / (K * math.e)))

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh415_mappa"](xs, 0.0, DEMO_K, DEMO_V, 0.0)
        assert abs(m["e0"] - E0) < 1e-12
        assert abs(m["dsr"] - DSR) < 1e-12
        assert abs(m["haircut_pp"] - HAIRCUT) < 1e-12
        assert abs(m["bias_ratio"] - BIAS) < 1e-12
        assert m["n_per"] == 36
        assert m["k"] == DEMO_K
        assert m["v"] == DEMO_V
        assert m["sr0"] == 0.0
        # la serie che al PSR single-trial era ACCETTABILE (~0.90) crolla
        # col selection bias di K=10 trial
        assert m["verdetto"].startswith("NON SIGNIFICATIVO")
        assert m["dsr"] < 0.02
        # lo Sharpe atteso spurio mangia >2x lo Sharpe osservato
        assert m["bias_ratio"] > 2.0
        assert m["haircut_pp"] > 80.0

    def test_definizione_dsr_a_mano(self):
        # E0 = sqrt(V)*((1-g)*ppf(1-1/K)+g*ppf(1-1/(Ke))); DSR =
        # Phi((SR-SR0-E0)*sqrt(n-1)/sigma_SR) con sigma_SR da skew/curtosi
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
        e0 = self._fst_e0(10, 0.25)
        z = (sr - 0.0 - e0) * math.sqrt(n - 1) / math.sqrt(s2)
        dsr = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        s = _F["mh415_stats"](tuple(xs), 0.0)
        d = _F["mh415_dsr_da_stat"](s, 10, 0.25, 0.0)
        assert abs(d["e0"] - e0) < 1e-9
        assert abs(d["sigma2"] - s2) < 1e-12
        assert abs(d["z"] - z) < 1e-9
        assert abs(d["dsr"] - dsr) < 1e-9
        assert abs(d["haircut_pp"] - (d["psr"] - dsr) * 100.0) < 1e-9
        assert abs(d["bias_ratio"] - e0 / sr) < 1e-9

    def test_ppf(self):
        F = _F
        # round-trip
        for p in (0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99):
            assert abs(F["mh415_phi"](F["mh415_ppf"](p)) - p) < 1e-9, p
        # costanti note
        assert abs(F["mh415_ppf"](0.9) - 1.2815515655446004) < 1e-9
        assert abs(F["mh415_ppf"](0.975) - 1.959963984540054) < 1e-9
        assert abs(F["mh415_ppf"](0.5)) < 1e-9
        # contro scipy, indipendente
        for p in (0.02, 0.1, 0.5, 0.9, 0.98):
            assert abs(F["mh415_ppf"](p) - norm.ppf(p)) < 1e-9, p
        # bordi: il quantile e' +-inf, non un numero finito
        for _bad in (0.0, 1.0, -0.1, 1.1, float("nan"), float("inf"),
                     True):
            with pytest.raises(ValueError):
                F["mh415_ppf"](_bad)

    def test_e0_fst(self):
        F = _F
        for K, V in ((2, 0.25), (10, 0.25), (10, 1.0), (50, 0.5),
                     (100, 2.0)):
            assert abs(F["mh415_e0"](K, V) - self._fst_e0(K, V)) < 1e-9, \
                (K, V)
        # V=0 -> nessuno Sharpe spurio
        assert F["mh415_e0"](10, 0.0) == 0.0
        # K intero >= 2 obbligatorio
        for _bad_k in (1, 0, -3, 2.5, float("nan"), True, "x"):
            with pytest.raises(ValueError):
                F["mh415_e0"](_bad_k, 0.25)
        # V >= 0 obbligatorio
        for _bad_v in (-0.1, float("nan"), True):
            with pytest.raises(ValueError):
                F["mh415_e0"](10, _bad_v)

    def test_v_zero_e_monotonia(self):
        F = _F
        s = F["mh415_stats"](self._xs(), 0.0)
        # V=0 -> DSR coincide col PSR single-trial (nessun selection bias)
        d0 = F["mh415_dsr_da_stat"](s, 10, 0.0, 0.0)
        assert abs(d0["dsr"] - d0["psr"]) < 1e-15
        assert d0["e0"] == 0.0
        assert d0["bias_ratio"] == 0.0
        # DSR decrescente in K (piu' trial = piu' bias)
        ds = [F["mh415_dsr_da_stat"](s, K, 0.25, 0.0)["dsr"]
              for K in (2, 10, 100)]
        assert ds[0] > ds[1] > ds[2]
        # DSR decrescente in V (piu' dispersione = piu' bias)
        dv = [F["mh415_dsr_da_stat"](s, 10, V, 0.0)["dsr"]
              for V in (0.0, 0.25, 1.0)]
        assert dv[0] > dv[1] > dv[2]
        # E0 crescente in K e in V
        assert F["mh415_e0"](100, 0.25) > F["mh415_e0"](2, 0.25)
        assert F["mh415_e0"](10, 1.0) > F["mh415_e0"](10, 0.25)
        # DSR decrescente nell'hurdle
        dh = [F["mh415_dsr_da_stat"](s, 10, 0.25, h)["dsr"]
              for h in (-0.5, 0.0, 0.5)]
        assert dh[0] > dh[1] > dh[2]
        # hurdle >= Sharpe -> bias_ratio infinito
        dinf = F["mh415_dsr_da_stat"](s, 10, 0.25, 5.0)
        assert math.isinf(dinf["bias_ratio"])

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh415_verdetto"](0.0).startswith("NON SIGNIFICATIVO")
        assert F["mh415_verdetto"](0.49).startswith("NON SIGNIFICATIVO")
        assert F["mh415_verdetto"](0.50).startswith("DEBOLE")
        assert F["mh415_verdetto"](0.74).startswith("DEBOLE")
        assert F["mh415_verdetto"](0.75).startswith("ACCETTABILE")
        assert F["mh415_verdetto"](0.899).startswith("ACCETTABILE")
        assert F["mh415_verdetto"](0.90).startswith("BUONO")
        assert F["mh415_verdetto"](0.949).startswith("BUONO")
        assert F["mh415_verdetto"](0.95).startswith("FORTE")
        assert F["mh415_verdetto"](0.989).startswith("FORTE")
        assert F["mh415_verdetto"](0.99).startswith("MOLTO FORTE")
        assert F["mh415_verdetto"](1.0).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh415_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh415_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta -> ValueError
        with pytest.raises(ValueError):
            F["mh415_stats"](tuple([1.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh415_mappa"](tuple([2.0] * 25), 2.0, 10, 0.25, 0.0)
        with pytest.raises(ValueError):
            F["mh415_mappa"]((1.0,) * 19)
        # stats senza chiavi -> ValueError
        with pytest.raises(ValueError):
            F["mh415_dsr_da_stat"]({}, 10, 0.25, 0.0)
        with pytest.raises(ValueError):
            F["mh415_dsr_da_stat"]({"n": 36}, 10, 0.25, 0.0)

    def test_validatori(self):
        for _bad in (lambda: _F["mh415_stats"](None),
                     lambda: _F["mh415_stats"]((1.0,) * 19),
                     lambda: _F["mh415_stats"]((1.0,) * 25,
                                               float("nan")),
                     lambda: _F["mh415_stats"](tuple([3.0] * 25), 0.0),
                     lambda: _F["mh415_sigma2"](float("nan"), 3.0, 0.5),
                     lambda: _F["mh415_sigma2"](3.0, 4.0, 1.0),
                     lambda: _F["mh415_e0"](1, 0.25),
                     lambda: _F["mh415_e0"](2.5, 0.25),
                     lambda: _F["mh415_e0"](10, -0.1),
                     lambda: _F["mh415_dsr_da_stat"](None, 10, 0.25),
                     lambda: _F["mh415_dsr_da_stat"](
                         {"n": 36, "sharpe": 0.2, "skew": 0.0,
                          "kurt": 3.0}, 1, 0.25, 0.0),
                     lambda: _F["mh415_dsr_da_stat"](
                         {"n": 36, "sharpe": 0.2, "skew": 0.0,
                          "kurt": 3.0}, 10, -0.25, 0.0),
                     lambda: _F["mh415_dsr_da_stat"](
                         {"n": 36, "sharpe": 0.2, "skew": 0.0,
                          "kurt": 3.0}, 10, 0.25, float("nan")),
                     lambda: _F["mh415_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh415_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh415_parse_serie"](None),
                     lambda: _F["mh415_phi"](float("inf")),
                     lambda: _F["mh415_ppf"](0.0),
                     lambda: _F["mh415_ppf"](1.0),
                     lambda: _F["mh415_num"](True, "x"),
                     lambda: _F["mh415_num"](float("nan"), "x"),
                     lambda: _F["mh415_mappa"]((1.0,) * 19),
                     lambda: _F["mh415_mappa"](None),
                     lambda: _F["mh415_mappa"](
                         tuple([1.0] * 25), 0.0, 10, 0.25, 0.0),
                     lambda: _F["mh415_mappa"](
                         tuple([1.5] * 30), 0.0, 1, 0.25, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh415_mappa"](DEMO, 0.0, DEMO_K, DEMO_V, 0.0)
        assert abs(m["dsr"] - DSR) < 1e-12
        assert m["n_per"] == 36

