"""Test tab410 '⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh410_num", "mh410_parse_serie", "mh410_gain_pain",
           "mh410_verdetto", "mh410_mappa")

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
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
DEMO = '3.2\n1.8\n-1.2\n2.5\n4.1\n-2.8\n0.9\n2.2\n-0.9\n3.0\n1.5\n-1.5\n5.2\n2.8\n1.1\n-3.1\n0.7\n3.6\n-0.6\n2.0\n1.4\n-1.9\n2.6\n0.8\n-1.1\n3.3\n1.7\n-2.2\n2.9\n0.5\n1.9\n-1.4\n2.4\n3.1\n-0.8\n1.6'
SOMMA = 39.3
PERDITE = 17.5
GUADAGNI = 56.8
GTP = 2.2457142857142856
N_DOWN = 11
N_UP = 25
MEDIA = 1.0916666666666666
MAXDOWN = -3.1


class TestRegistry410:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 803
        assert "tab410" in dvars
        assert "tab410" in withs

    def test_titoli_allineati_405_406_407_408_409_410(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410

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


class TestGainPain410:
    def _xs(self):
        return _F["mh410_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh410_mappa"](xs)
        assert abs(m["somma"] - SOMMA) < 1e-12
        assert abs(m["perdite"] - PERDITE) < 1e-12
        assert abs(m["guadagni"] - GUADAGNI) < 1e-12
        assert abs(m["gain_pain"] - GTP) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert abs(m["max_down"] - MAXDOWN) < 1e-9
        assert m["n_per"] == 36
        assert m["n_down"] == N_DOWN
        assert m["n_up"] == N_UP
        assert m["verdetto"].startswith("ECCELLENTE")

    def test_gain_pain_definizione(self):
        # gtp = somma / |somma negativi|, calcolato a mano
        xs = list(self._xs())
        somma = sum(xs)
        perdite = -sum(v for v in xs if v < 0.0)
        assert abs(somma - SOMMA) < 1e-9
        assert abs(perdite - PERDITE) < 1e-9
        assert abs(_F["mh410_gain_pain"](tuple(xs))
                   - somma / perdite) < 1e-12
        assert abs(min(xs) - MAXDOWN) < 1e-9

    def test_casi_degeneri(self):
        F = _F
        assert F["mh410_gain_pain"](tuple([1.0] * 25)) == math.inf
        assert F["mh410_gain_pain"](tuple([0.0] * 25)) == 0.0
        assert F["mh410_gain_pain"](tuple([-1.0] * 25)) < 0.0
        assert F["mh410_gain_pain"](
            tuple([2.0] * 20 + [-1.0] * 5)) == (2.0 * 20 - 5.0) / 5.0
        assert F["mh410_verdetto"](math.inf).startswith("NESSUNA PERDITA")
        assert F["mh410_verdetto"](2.5).startswith("ECCELLENTE")
        assert F["mh410_verdetto"](2.0).startswith("ECCELLENTE")
        assert F["mh410_verdetto"](1.7).startswith("BUONO")
        assert F["mh410_verdetto"](1.2).startswith("ACCETTABILE")
        assert F["mh410_verdetto"](0.8).startswith("DEBOLE")
        assert F["mh410_verdetto"](0.3).startswith("SCARSO")
        assert F["mh410_verdetto"](-1.0).startswith("SCARSO")

    def test_validatori(self):
        F = _F
        for _bad in (lambda: F["mh410_gain_pain"](None),
                     lambda: F["mh410_gain_pain"]((1.0,) * 19),
                     lambda: F["mh410_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: F["mh410_parse_serie"](
                         "\n".join(["1.0"] * 19 + ["xx"])),
                     lambda: F["mh410_num"](True, "x"),
                     lambda: F["mh410_num"](float("nan"), "x"),
                     lambda: F["mh410_mappa"]((1.0,) * 19),
                     lambda: F["mh410_mappa"](None)):
            try:
                _bad()
                raise AssertionError("caso degenere non rilevato")
            except ValueError:
                pass

    def test_coerenza_mappa_gain_pain(self):
        # mappa e gain_pain devono concordare su serie arbitrarie
        xs = tuple([round(3.0 * ((-1) ** i) * (1 + i % 4), 2)
                    for i in range(25)])
        m = _F["mh410_mappa"](xs)
        assert abs(m["gain_pain"] - _F["mh410_gain_pain"](xs)) < 1e-12
        assert m["n_down"] + m["n_up"] <= m["n_per"]
        assert abs(m["guadagni"] - m["perdite"] - m["somma"]) < 1e-9
