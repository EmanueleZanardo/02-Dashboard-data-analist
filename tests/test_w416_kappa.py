"""Test tab416 '🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh416_num", "mh416_parse_serie", "mh416_lpm", "mh416_kappa",
           "mh416_verdetto", "mh416_mappa", "mh412_omega", "mh412_num")

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
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
DEMO_N = 2
DEMO_T = 0.0
KAPPA = 0.3438068155593204
KAPPA1 = 0.8734177215189873
KAPPA2 = 0.3438068155593204
OMEGA = 1.8734177215189873
DD = 3.9023853104365682


class TestRegistry416:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 653
        assert "tab416" in dvars
        assert "tab416" in withs

    def test_titoli_allineati_411_412_413_414_415_416(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab411")] == TITLE411
        assert titoli[dvars.index("tab412")] == TITLE412
        assert titoli[dvars.index("tab413")] == TITLE413
        assert titoli[dvars.index("tab414")] == TITLE414
        assert titoli[dvars.index("tab415")] == TITLE415
        assert titoli[dvars.index("tab416")] == TITLE416

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


class TestKappa416:
    def _xs(self):
        return _F["mh416_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh416_mappa"](xs, DEMO_T, DEMO_N)
        assert m["n"] == DEMO_N
        assert m["soglia"] == DEMO_T
        assert abs(m["kappa"] - KAPPA) < 1e-12
        assert abs(m["kappa1"] - KAPPA1) < 1e-12
        assert abs(m["kappa2"] - KAPPA2) < 1e-12
        assert abs(m["kappa"] - KAPPA2) < 1e-15  # demo con n=2
        assert abs(m["omega"] - OMEGA) < 1e-12
        assert abs(m["downside_dev"] - DD) < 1e-12
        assert abs(m["p_sopra"] - 30.0 / 36.0) < 1e-12
        assert abs(m["excess"] - (m["upside"] - m["downside"])) < 1e-12
        # Kappa_1 accettabile ma Kappa_2 debole: le code mangiano il profilo
        assert m["verdetto"].startswith("DEBOLE")
        assert 0.85 < m["kappa1"] < 0.90
        assert 0.30 < m["kappa2"] < 0.40

    def test_definizione_kappa_a_mano(self):
        # Kappa_n = E[r-T]/LPM_n^(1/n), LPM_n = media(max(T-r,0)^n)
        xs = list(self._xs())
        n = len(xs)
        T = 0.0
        mu = sum(xs) / n
        exc = mu - T
        for N in (1, 2, 3):
            lpm = sum(max(T - x, 0.0) ** N for x in xs) / n
            kap = exc / (lpm ** (1.0 / N))
            k = _F["mh416_kappa"](tuple(xs), T, N)
            assert abs(k["lpm_n"] - lpm) < 1e-12, N
            assert abs(k["kappa"] - kap) < 1e-12, N
            assert abs(_F["mh416_lpm"](tuple(xs), T, N) - lpm) < 1e-12, N
        # downside_dev = sqrt(LPM_2)
        k2 = _F["mh416_kappa"](tuple(xs), T, 2)
        assert abs(k2["downside_dev"] - math.sqrt(
            sum(max(T - x, 0.0) ** 2 for x in xs) / n)) < 1e-12

    def test_kappa1_eq_omega_meno_uno(self):
        # Kappa_1 = (upside-downside)/downside = Omega-1, esatto
        xs = self._xs()
        k = _F["mh416_kappa"](xs, 0.0, 1)
        o = _F["mh412_omega"](xs, 0.0)
        assert abs(k["kappa1"] - (o["omega"] - 1.0)) < 1e-12
        assert abs(k["omega"] - o["omega"]) < 1e-12
        assert abs(k["upside"] - o["upside"]) < 1e-12
        assert abs(k["downside"] - o["downside"]) < 1e-12

    def test_kappa2_eq_sortino_a_mano(self):
        # Sortino(T) = (media-T)/sqrt(media(min(r-T,0)^2))
        xs = list(self._xs())
        n = len(xs)
        mu = sum(xs) / n
        dd = math.sqrt(sum(min(x - 0.0, 0.0) ** 2 for x in xs) / n)
        s2 = mu / dd
        k = _F["mh416_kappa"](tuple(xs), 0.0, 2)
        assert abs(k["kappa2"] - s2) < 1e-12
        assert abs(k["downside_dev"] - dd) < 1e-12

    def test_monotonia_n(self):
        # con code grasse a sinistra, Kappa_n decresce in n: gli ordini
        # alti penalizzano di piu' i crash
        F = _F
        xs = self._xs()
        ks = [F["mh416_kappa"](xs, 0.0, N)["kappa"] for N in (1, 2, 3, 4)]
        assert ks[0] > ks[1] > ks[2] > ks[3]
        # monotonia nella soglia: soglia piu' alta -> kappa piu' basso
        kt = [F["mh416_kappa"](xs, T, 2)["kappa"]
              for T in (-1.0, 0.0, 1.0)]
        assert kt[0] > kt[1] > kt[2]

    def test_infinito_senza_downside(self):
        # tutti sopra la soglia: nessun downside -> +inf
        k = _F["mh416_kappa"](tuple([1.0] * 25), 0.0, 2)
        assert math.isinf(k["kappa"])
        assert math.isinf(k["kappa1"])
        assert math.isinf(k["kappa2"])
        assert _F["mh416_verdetto"](k["kappa"]).startswith("MOLTO FORTE")

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh416_verdetto"](-0.1).startswith("NEGATIVO")
        assert F["mh416_verdetto"](0.0).startswith("DEBOLE")
        assert F["mh416_verdetto"](0.49).startswith("DEBOLE")
        assert F["mh416_verdetto"](0.50).startswith("ACCETTABILE")
        assert F["mh416_verdetto"](0.99).startswith("ACCETTABILE")
        assert F["mh416_verdetto"](1.0).startswith("BUONO")
        assert F["mh416_verdetto"](1.99).startswith("BUONO")
        assert F["mh416_verdetto"](2.0).startswith("FORTE")
        assert F["mh416_verdetto"](2.99).startswith("FORTE")
        assert F["mh416_verdetto"](3.0).startswith("MOLTO FORTE")
        assert F["mh416_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh416_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh416_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta sulla soglia -> ValueError
        with pytest.raises(ValueError):
            F["mh416_kappa"](tuple([0.0] * 25), 0.0, 2)
        with pytest.raises(ValueError):
            F["mh416_mappa"](tuple([1.0] * 25), 1.0, 2)
        with pytest.raises(ValueError):
            F["mh416_mappa"]((1.0,) * 19)
        # n non intero o fuori [1, 6] -> ValueError
        for _bad_n in (0, 7, 2.5, float("nan"), True, "x"):
            with pytest.raises(ValueError):
                F["mh416_kappa"](self._xs(), 0.0, _bad_n)
            with pytest.raises(ValueError):
                F["mh416_lpm"](self._xs(), 0.0, _bad_n)

    def test_validatori(self):
        for _bad in (lambda: _F["mh416_kappa"](None),
                     lambda: _F["mh416_kappa"]((1.0,) * 19),
                     lambda: _F["mh416_kappa"]((1.0,) * 25,
                                               float("nan")),
                     lambda: _F["mh416_kappa"](tuple([0.0] * 25), 0.0, 2),
                     lambda: _F["mh416_kappa"](self._xs(), 0.0, 0),
                     lambda: _F["mh416_kappa"](self._xs(), 0.0, 7),
                     lambda: _F["mh416_lpm"](None, 0.0, 2),
                     lambda: _F["mh416_lpm"]((1.0,) * 19, 0.0, 2),
                     lambda: _F["mh416_lpm"](self._xs(), 0.0, 2.5),
                     lambda: _F["mh416_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh416_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh416_parse_serie"](None),
                     lambda: _F["mh416_num"](True, "x"),
                     lambda: _F["mh416_num"](float("nan"), "x"),
                     lambda: _F["mh416_mappa"]((1.0,) * 19),
                     lambda: _F["mh416_mappa"](None),
                     lambda: _F["mh416_mappa"](
                         tuple([0.0] * 25), 0.0, 2),
                     lambda: _F["mh416_mappa"](self._xs(), 0.0, 0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh416_mappa"](DEMO, DEMO_T, DEMO_N)
        assert abs(m["kappa"] - KAPPA) < 1e-12

