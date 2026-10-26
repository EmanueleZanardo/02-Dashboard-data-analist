"""Test tab409 '🛟 Sterling ratio: quanto rende contro i K peggiori drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh409_num", "mh409_parse_serie", "mh409_equity",
           "mh409_episodi", "mh409_r_tot", "mh409_sterling",
           "mh409_verdetto", "mh409_mappa")

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
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
DEMO = '1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n-2.0\n-2.0\n-2.0\n-2.0\n1.6\n1.6\n1.6\n1.6\n1.6\n1.6\n-1.7\n-1.7\n-1.7\n1.5\n1.5\n1.5\n1.5\n1.5\n1.5\n-1.5\n-1.5\n1.8\n1.8\n1.8\n1.8\n1.8\n1.8\n1.8'
R_TOT = 30.484402864682146
MDD = 7.763184000000006
AVGWORST3 = 5.251491766666668
STERLING = 5.804903486315816
N_EP = 3
MEDIA = 0.7527777777777778
EP1 = (8, 12, 18, 7.7632, 10)
EP2 = (18, 21, 25, 5.0138, 7)
EP3 = (27, 29, 31, 2.9775, 4)


class TestRegistry409:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 732
        assert "tab409" in dvars
        assert "tab409" in withs

    def test_titoli_allineati_404_405_406_407_408_409(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab404")] == TITLE404
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407
        assert titoli[dvars.index("tab408")] == TITLE408
        assert titoli[dvars.index("tab409")] == TITLE409

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


class TestSterling409:
    def _xs(self):
        return _F["mh409_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh409_mappa"](xs, 3)
        assert abs(m["r_tot"] - R_TOT) < 1e-12
        assert abs(m["mdd"] - MDD) < 1e-12
        assert abs(m["avg_worst"] - AVGWORST3) < 1e-12
        assert abs(m["sterling"] - STERLING) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert m["n_per"] == 36
        assert m["n_ep"] == N_EP
        assert m["k"] == 3
        assert m["verdetto"].startswith("ROBUSTO")

    def test_demo_episodi(self):
        xs = self._xs()
        m = _F["mh409_mappa"](xs, 3)
        epis = m["episodi"]
        assert len(epis) == 3
        for ep, exp in zip(epis, (EP1, EP2, EP3)):
            assert (ep["i0"], ep["iv"], ep["i1"]) == exp[:3]
            assert abs(ep["prof"] - exp[3]) < 1e-4
            assert ep["durata"] == exp[4]
            assert ep["aperto"] is False
        profs = [e["prof"] for e in epis]
        assert profs == sorted(profs, reverse=True)

    def test_sterling_definizione(self):
        # sterling = R_tot / media dei K peggiori, calcolato a mano
        xs = list(self._xs())
        eq = _F["mh409_equity"](xs)
        r_tot = _F["mh409_r_tot"](eq)
        assert abs(r_tot - R_TOT) < 1e-9
        epis = _F["mh409_episodi"](eq)
        pegg = sorted((e["prof"] for e in epis), reverse=True)[:3]
        assert abs(sum(pegg) / 3 - AVGWORST3) < 1e-9
        assert abs(_F["mh409_sterling"](xs, 3) - r_tot / (sum(pegg) / 3)) < 1e-12

    def test_sterling_k1_uguale_recovery_factor(self):
        # con K=1 lo Sterling coincide col Recovery factor (tab407):
        # R_tot / |MDD|
        xs = self._xs()
        m = _F["mh409_mappa"](xs, 1)
        assert m["k"] == 1
        assert abs(m["sterling"] - m["r_tot"] / m["mdd"]) < 1e-12

    def test_k_maggiore_di_episodi(self):
        # K >= n_ep si comporta come 'tutti'
        xs = self._xs()
        a = _F["mh409_mappa"](xs, 3)
        b = _F["mh409_mappa"](xs, 10 ** 9)
        assert b["k"] == 3
        assert abs(a["sterling"] - b["sterling"]) < 1e-12
        assert abs(a["avg_worst"] - b["avg_worst"]) < 1e-12

    def test_casi_degeneri(self):
        F = _F
        assert F["mh409_sterling"](tuple([1.0] * 25), 3) == math.inf
        assert F["mh409_sterling"](tuple([0.0] * 25), 3) == 0.0
        assert F["mh409_sterling"](tuple([-1.0] * 25), 3) < 0.0
        assert F["mh409_mappa"](tuple([1.0] * 25), 3)["n_ep"] == 0
        assert F["mh409_verdetto"](math.inf).startswith("NESSUN DRAWDOWN")
        assert F["mh409_verdetto"](2.5).startswith("ROBUSTO")
        assert F["mh409_verdetto"](2.0).startswith("ROBUSTO")
        assert F["mh409_verdetto"](1.7).startswith("SOLIDO")
        assert F["mh409_verdetto"](1.2).startswith("ACCETTABILE")
        assert F["mh409_verdetto"](0.8).startswith("FRAGILE")
        assert F["mh409_verdetto"](0.3).startswith("CRITICO")
        assert F["mh409_verdetto"](-1.0).startswith("CRITICO")

    def test_episodio_aperto(self):
        # serie che finisce sott'acqua: ultimo episodio aperto
        xs = tuple([1.0] * 18 + [-3.0] * 6 + [0.5] * 2)
        m = _F["mh409_mappa"](xs, 3)
        assert m["n_ep"] >= 1
        assert m["episodi"][-1]["aperto"] is True
        assert m["episodi"][-1]["i1"] == len(xs)

    def test_validatori(self):
        F = _F
        for _bad in (lambda: F["mh409_equity"]((1.0,) * 19),
                     lambda: F["mh409_equity"](None),
                     lambda: F["mh409_episodi"]([100.0]),
                     lambda: F["mh409_episodi"]([100.0, -5.0]),
                     lambda: F["mh409_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: F["mh409_num"](True, "x"),
                     lambda: F["mh409_num"](float("nan"), "x"),
                     lambda: F["mh409_sterling"]((1.0,) * 25, 0),
                     lambda: F["mh409_sterling"]((1.0,) * 25, -2),
                     lambda: F["mh409_sterling"]((1.0,) * 25, True),
                     lambda: F["mh409_mappa"]((1.0,) * 19, 3),
                     lambda: F["mh409_mappa"]((1.0,) * 25, 0)):
            try:
                _bad()
                raise AssertionError("caso degenere non rilevato")
            except ValueError:
                pass

    def test_coerenza_ui_ids(self):
        # gli id usati dalla UI per i top-K esistono davvero
        xs = self._xs()
        m = _F["mh409_mappa"](xs, 3)
        ids = {id(e) for e in m["episodi"]}
        top = sorted(m["episodi"], key=lambda e: e["prof"],
                     reverse=True)[:m["k"]]
        assert all(id(e) in ids for e in top)
        assert len({id(e) for e in top}) == m["k"]
