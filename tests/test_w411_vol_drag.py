"""Test tab411 '🌊 Volatility drag: quanto rendimento mangia la volatilita'': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh411_num", "mh411_parse_serie", "mh411_equity",
           "mh411_drag", "mh411_verdetto", "mh411_mappa")

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
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
DEMO = '7.5\n-4.2\n9.1\n-6.8\n5.4\n-3.1\n8.2\n-5.5\n4.9\n-2.4\n6.7\n-7.1\n3.8\n-1.9\n5.9\n-4.6\n2.7\n6.3\n-3.8\n4.1\n-5.9\n7.8\n-2.7\n3.2\n-6.1\n5.5\n-4.9\n6.9\n-3.4\n4.4\n-5.2\n7.1\n-2.1\n3.6\n-4.4\n2.9'
MEDIA = 0.8861111111111111
GEO = 0.7489052166361976
DRAG = 0.1372058944749135
SIGMA = 5.254688529609521
APPROX = 0.13805875771604936
QUOTA = 15.484050787137575
EQUITY = 130.81335417564307
EQNODRAG = 137.38196785908085


class TestRegistry411:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 473
        assert "tab411" in dvars
        assert "tab411" in withs

    def test_titoli_allineati_406_407_408_409_410_411(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409
        assert titoli[dvars.index("tab410")] == TITLE410
        assert titoli[dvars.index("tab411")] == TITLE411

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab473"
        assert titoli[-1] == TITLE473
        assert withs[-1] == "tab473"


class TestVolDrag411:
    def _xs(self):
        return _F["mh411_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh411_mappa"](xs)
        assert abs(m["media"] - MEDIA) < 1e-12
        assert abs(m["geo"] - GEO) < 1e-12
        assert abs(m["drag"] - DRAG) < 1e-12
        assert abs(m["sigma"] - SIGMA) < 1e-12
        assert abs(m["approx"] - APPROX) < 1e-12
        assert abs(m["quota"] - QUOTA) < 1e-12
        assert abs(m["equity"][-1] - EQUITY) < 1e-9
        assert abs(m["equity_nodrag"][-1] - EQNODRAG) < 1e-9
        assert m["n_per"] == 36
        assert m["verdetto"].startswith("SIGNIFICATIVO")

    def test_drag_definizione(self):
        # drag = media - geo, calcolato a mano
        xs = list(self._xs())
        n = len(xs)
        media = sum(xs) / n
        geo = (math.prod(1.0 + r / 100.0 for r in xs)
               ** (1.0 / n) - 1.0) * 100.0
        d = _F["mh411_drag"](tuple(xs))
        assert abs(d["media"] - media) < 1e-12
        assert abs(d["geo"] - geo) < 1e-12
        assert abs(d["drag"] - (media - geo)) < 1e-12
        assert abs(d["sigma"] - statistics.pstdev(xs)) < 1e-12
        assert abs(d["quota"] - (media - geo) / media * 100.0) < 1e-12

    def test_approx_sigma_quadro(self):
        # il drag e' vicino a sigma^2/200 (Jensen): scarto piccolo sulla demo
        xs = self._xs()
        d = _F["mh411_drag"](xs)
        assert abs(d["scarto"] - (d["drag"] - d["approx"])) < 1e-15
        assert abs(d["scarto"]) < 0.02

    def test_equity_nodrag(self):
        xs = self._xs()
        m = _F["mh411_mappa"](xs)
        mu = m["media"] / 100.0
        assert len(m["equity"]) == len(m["equity_nodrag"]) == 37
        assert abs(m["equity_nodrag"][-1]
                   - 100.0 * (1.0 + mu) ** 36) < 1e-9
        assert abs(m["gap"] - (m["equity_nodrag"][-1]
                               - m["equity"][-1])) < 1e-12
        assert m["gap"] > 0.0  # con vol > 0 il drag costa sempre

    def test_casi_degeneri(self):
        F = _F
        # serie piatta -> drag 0, quota 0 -> TRASCURABILE
        d = F["mh411_drag"](tuple([2.0] * 25))
        assert abs(d["drag"]) < 1e-9
        assert abs(d["geo"] - 2.0) < 1e-9
        assert abs(d["quota"]) < 1e-9
        assert F["mh411_verdetto"](d["quota"], d["media"]
                                   ).startswith("TRASCURABILE")
        # media <= 0 -> NESSUN RENDIMENTO
        d2 = F["mh411_drag"](tuple([-1.0] * 25))
        assert d2["quota"] is None
        assert F["mh411_verdetto"](d2["quota"], d2["media"]
                                   ).startswith("NESSUN RENDIMENTO")
        # soglie verdetto
        assert F["mh411_verdetto"](4.9, 1.0).startswith("TRASCURABILE")
        assert F["mh411_verdetto"](5.0, 1.0).startswith("MODERATO")
        assert F["mh411_verdetto"](14.9, 1.0).startswith("MODERATO")
        assert F["mh411_verdetto"](15.0, 1.0).startswith("SIGNIFICATIVO")
        assert F["mh411_verdetto"](29.9, 1.0).startswith("SIGNIFICATIVO")
        assert F["mh411_verdetto"](30.0, 1.0).startswith("DEVASTANTE")
        assert F["mh411_verdetto"](80.0, 1.0).startswith("DEVASTANTE")
        with pytest.raises(ValueError):
            F["mh411_verdetto"](None, 1.0)
        with pytest.raises(ValueError):
            F["mh411_verdetto"](float("nan"), 1.0)
        with pytest.raises(ValueError):
            F["mh411_verdetto"](True, 1.0)

    def test_validatori(self):
        for _bad in (lambda: _F["mh411_drag"](None),
                     lambda: _F["mh411_drag"]((1.0,) * 19),
                     lambda: _F["mh411_drag"](tuple([50.0] * 19 + [-150.0])),
                     lambda: _F["mh411_equity"](None),
                     lambda: _F["mh411_equity"]((1.0,) * 19),
                     lambda: _F["mh411_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh411_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh411_parse_serie"](None),
                     lambda: _F["mh411_num"](True, "x"),
                     lambda: _F["mh411_num"](float("nan"), "x"),
                     lambda: _F["mh411_mappa"]((1.0,) * 19),
                     lambda: _F["mh411_mappa"](None)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh411_mappa"](DEMO)
        assert abs(m["drag"] - DRAG) < 1e-12
        assert m["n_per"] == 36

