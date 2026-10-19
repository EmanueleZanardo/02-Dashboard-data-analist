"""Test tab407 '🔄 Recovery factor: quanto rende ogni euro di drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh407_num", "mh407_parse_serie", "mh407_equity",
           "mh407_max_drawdown", "mh407_recovery_factor",
           "mh407_verdetto", "mh407_mappa")

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
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
DEMO = '-2.4\n-1.9\n-1.6\n-1.2\n-0.9\n-0.7\n-0.5\n-0.3\n-0.2\n-0.1\n0.0\n0.1\n0.2\n0.4\n0.5\n0.6\n0.8\n0.9\n1.0\n1.1\n1.3\n1.4\n1.5\n1.7\n1.8\n2.0\n2.1\n2.2\n2.4\n2.5\n2.7\n2.9\n3.1\n6.4\n7.8\n9.5'
R_TOT = 58.06423671123591
MDD = 9.40420516011784
RF = 6.174284346483603
MEDIA = 1.3083333333333333


class TestRegistry407:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 557
        assert "tab407" in dvars
        assert "tab407" in withs

    def test_titoli_allineati_402_403_404_405_406_407(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab402")] == TITLE402
        assert titoli[dvars.index("tab403")] == TITLE403
        assert titoli[dvars.index("tab404")] == TITLE404
        assert titoli[dvars.index("tab405")] == TITLE405
        assert titoli[dvars.index("tab406")] == TITLE406
        assert titoli[dvars.index("tab407")] == TITLE407

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


class TestRecovery407:
    def _xs(self):
        return _F["mh407_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh407_mappa"](xs)
        assert abs(m["r_tot"] - R_TOT) < 1e-12
        assert abs(m["mdd"] - MDD) < 1e-12
        assert abs(m["recovery_factor"] - RF) < 1e-12
        assert abs(m["media"] - MEDIA) < 1e-12
        assert m["n_per"] == 36
        assert m["idx_peak"] == 0
        assert m["idx_trough"] == 10
        assert m["verdetto"].startswith("RECUPERO FORTE")

    def test_equity_coerente(self):
        # equity[-1] / 100 - 1 == r_tot / 100 ; cross-check via math.prod
        xs = list(self._xs())
        eq = _F["mh407_equity"](xs)
        assert len(eq) == len(xs) + 1
        assert eq[0] == 100.0
        m = _F["mh407_mappa"](xs)
        assert abs(eq[-1] / 100.0 - 1.0 - m["r_tot"] / 100.0) < 1e-12
        assert abs(eq[-1] - 100.0 * math.prod(1.0 + r / 100.0
                                             for r in xs)) < 1e-9

    def test_mdd_definizione(self):
        # MDD = max della serie drawdown, picco prima della valle
        xs = list(self._xs())
        eq = _F["mh407_equity"](xs)
        mdd, ip, iv = _F["mh407_max_drawdown"](eq)
        assert mdd >= 0.0
        assert ip <= iv
        peak = max(eq[: iv + 1])
        assert abs((peak - eq[iv]) / peak * 100.0 - mdd) < 1e-12

    def test_rf_monotono_mdd(self):
        # drawdown maggiore a parita' di serie -> RF minore
        xs = list(self._xs())
        rf1 = _F["mh407_recovery_factor"](xs)
        peggio = [-10.0] + xs[1:]
        rf2 = _F["mh407_recovery_factor"](tuple(peggio))
        assert rf2 < rf1

    def test_casi_degeneri(self):
        # serie solo positiva senza cali -> MDD = 0 -> +inf
        xs = tuple([1.0] * 25)
        assert _F["mh407_recovery_factor"](xs) == math.inf
        assert _F["mh407_verdetto"](math.inf).startswith("NESSUN DRAWDOWN")
        # serie piatta a 0 -> 0.0
        assert _F["mh407_recovery_factor"](tuple([0.0] * 25)) == 0.0
        # perdita netta -> RF negativo
        xs = tuple([-1.0] * 25)
        rf = _F["mh407_recovery_factor"](xs)
        assert rf < 0.0
        assert _F["mh407_verdetto"](rf).startswith("NESSUN RECUPERO")
        # soglie intermedie
        assert _F["mh407_verdetto"](0.5).startswith("RECUPERO DEBOLE")
        assert _F["mh407_verdetto"](1.5).startswith("RECUPERO BUONO")

    def test_verdetto_stati(self):
        assert _F["mh407_verdetto"](3.0).startswith("RECUPERO FORTE")
        assert _F["mh407_verdetto"](2.0).startswith("RECUPERO FORTE")
        assert _F["mh407_verdetto"](1.999).startswith("RECUPERO BUONO")
        assert _F["mh407_verdetto"](1.0).startswith("RECUPERO BUONO")
        assert _F["mh407_verdetto"](0.999).startswith("RECUPERO DEBOLE")
        assert _F["mh407_verdetto"](0.0).startswith("NESSUN RECUPERO")
        assert _F["mh407_verdetto"](-2.0).startswith("NESSUN RECUPERO")
        with pytest.raises(ValueError):
            _F["mh407_verdetto"](True)
        with pytest.raises(ValueError):
            _F["mh407_verdetto"](float("nan"))

    def test_validatori(self):
        for _bad in (lambda: _F["mh407_equity"]((1.0,) * 19),
                     lambda: _F["mh407_equity"](None),
                     lambda: _F["mh407_max_drawdown"]([100.0]),
                     lambda: _F["mh407_max_drawdown"]([100.0, -5.0]),
                     lambda: _F["mh407_recovery_factor"]((1.0,) * 19),
                     lambda: _F["mh407_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh407_parse_serie"](
                         "\n".join(["abc"] + ["1.0"] * 20)),
                     lambda: _F["mh407_parse_serie"](None),
                     lambda: _F["mh407_num"](True, "x"),
                     lambda: _F["mh407_num"](float("nan"), "x"),
                     lambda: _F["mh407_num"]("a", "x"),
                     lambda: _F["mh407_mappa"]((1.0,) * 19)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh407_mappa"](DEMO)
        assert abs(m["recovery_factor"] - RF) < 1e-12
        assert m["n_per"] == 36

