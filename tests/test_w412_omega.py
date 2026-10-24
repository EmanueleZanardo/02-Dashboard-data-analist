"""Test tab412 '🎯 Omega ratio: quanto upside prendi per ogni euro di downside': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh412_num", "mh412_parse_serie", "mh412_omega",
           "mh412_verdetto", "mh412_mappa")

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
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
DEMO = '7.5\n-4.2\n9.1\n-6.8\n5.4\n-3.1\n8.2\n-5.5\n4.9\n-2.4\n6.7\n-7.1\n3.8\n-1.9\n5.9\n-4.6\n2.7\n6.3\n-3.8\n4.1\n-5.9\n7.8\n-2.7\n3.2\n-6.1\n5.5\n-4.9\n6.9\n-3.4\n4.4\n-5.2\n7.1\n-2.1\n3.6\n-4.4\n2.9'
OMEGA = 1.4304993252361675
UPSIDE = 2.9444444444444446
DOWNSIDE = 2.058333333333333
PSOPRA = 0.5277777777777778
OMEGA_T05 = 1.1682808716707023
GAIN_MEDIO = 5.578947368421052
LOSS_MEDIO = 4.358823529411764
SOMMA_UP = 106.0
SOMMA_DN = 74.1


class TestRegistry412:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 687
        assert "tab412" in dvars
        assert "tab412" in withs

    def test_titoli_allineati_407_408_409_410_411_412(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410
        assert titoli[dvars.index("tab411")] == TITLE411
        assert titoli[dvars.index("tab412")] == TITLE412

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


class TestOmega412:
    def _xs(self):
        return _F["mh412_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh412_mappa"](xs)
        assert abs(m["upside"] - UPSIDE) < 1e-12
        assert abs(m["downside"] - DOWNSIDE) < 1e-12
        assert abs(m["omega"] - OMEGA) < 1e-12
        assert abs(m["p_sopra"] - PSOPRA) < 1e-12
        assert abs(m["gain_medio"] - GAIN_MEDIO) < 1e-12
        assert abs(m["loss_medio"] - LOSS_MEDIO) < 1e-12
        assert abs(m["somma_up"] - SOMMA_UP) < 1e-9
        assert abs(m["somma_dn"] - SOMMA_DN) < 1e-9
        assert m["n_per"] == 36
        assert m["verdetto"].startswith("ACCETTABILE")

    def test_omega_definizione(self):
        # Omega = somma upside / somma downside, calcolato a mano
        xs = list(self._xs())
        su = sum(max(r - 0.0, 0.0) for r in xs)
        sd = sum(max(0.0 - r, 0.0) for r in xs)
        o = _F["mh412_omega"](tuple(xs), 0.0)
        assert abs(o["somma_up"] - su) < 1e-12
        assert abs(o["somma_dn"] - sd) < 1e-12
        assert abs(o["omega"] - su / sd) < 1e-12
        assert abs(o["upside"] - su / 36) < 1e-12
        assert abs(o["downside"] - sd / 36) < 1e-12
        assert abs(o["p_sopra"]
                   - sum(1 for r in xs if r > 0.0) / 36) < 1e-15

    def test_soglia(self):
        # alzare la soglia mangia l'edge: Omega(0.5%) < Omega(0%)
        xs = self._xs()
        o05 = _F["mh412_mappa"](xs, 0.5)
        assert abs(o05["omega"] - OMEGA_T05) < 1e-12
        assert o05["omega"] < OMEGA
        assert _F["mh412_omega"](xs, 0.5)["soglia"] == 0.5

    def test_casi_degeneri(self):
        F = _F
        # serie piatta sulla soglia -> ValueError
        with pytest.raises(ValueError):
            F["mh412_omega"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh412_mappa"](tuple([2.0] * 25), 2.0)
        # solo upside -> +inf -> ECCEZIONALE
        oi = F["mh412_omega"](tuple([1.0] * 25), 0.0)
        assert oi["omega"] == math.inf
        assert F["mh412_verdetto"](oi["omega"], 0.0
                                   ).startswith("ECCEZIONALE")
        # solo downside -> 0.0 -> SOTTO SOGLIA
        oz = F["mh412_omega"](tuple([-1.0] * 25), 0.0)
        assert oz["omega"] == 0.0
        assert F["mh412_verdetto"](oz["omega"], 0.0
                                   ).startswith("SOTTO SOGLIA")
        # soglie verdetto
        assert F["mh412_verdetto"](0.99, 0.0).startswith("SOTTO SOGLIA")
        assert F["mh412_verdetto"](1.0, 0.0).startswith("ACCETTABILE")
        assert F["mh412_verdetto"](1.49, 0.0).startswith("ACCETTABILE")
        assert F["mh412_verdetto"](1.5, 0.0).startswith("BUONO")
        assert F["mh412_verdetto"](2.49, 0.0).startswith("BUONO")
        assert F["mh412_verdetto"](2.5, 0.0).startswith("ECCELLENTE")
        assert F["mh412_verdetto"](3.99, 0.0).startswith("ECCELLENTE")
        assert F["mh412_verdetto"](4.0, 0.0).startswith("ECCEZIONALE")
        assert F["mh412_verdetto"](9.0, 0.0).startswith("ECCEZIONALE")
        with pytest.raises(ValueError):
            F["mh412_verdetto"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh412_verdetto"](float("nan"), 0.0)
        with pytest.raises(ValueError):
            F["mh412_verdetto"](True, 0.0)
        with pytest.raises(ValueError):
            F["mh412_verdetto"](1.5, float("nan"))

    def test_validatori(self):
        for _bad in (lambda: _F["mh412_omega"](None),
                     lambda: _F["mh412_omega"]((1.0,) * 19),
                     lambda: _F["mh412_omega"]((1.0,) * 25,
                                              float("nan")),
                     lambda: _F["mh412_omega"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh412_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh412_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh412_parse_serie"](None),
                     lambda: _F["mh412_num"](True, "x"),
                     lambda: _F["mh412_num"](float("nan"), "x"),
                     lambda: _F["mh412_mappa"]((1.0,) * 19),
                     lambda: _F["mh412_mappa"](None),
                     lambda: _F["mh412_mappa"](tuple([1.0] * 25), "xx")):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh412_mappa"](DEMO)
        assert abs(m["omega"] - OMEGA) < 1e-12
        assert m["n_per"] == 36

