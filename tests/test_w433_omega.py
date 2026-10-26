
"""Test tab433 '🧮 Omega ratio: guadagni pesati contro perdite pesate': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh433_num", "mh433_parse_serie", "mh433_equity",
           "mh433_drawdowns", "mh433_max_dd",
           "mh433_upside_potential", "mh433_downside_potential",
           "mh433_omega", "mh433_verdetto", "mh433_mappa",
           "mh432_num", "mh432_parse_serie", "mh432_equity",
           "mh432_drawdowns", "mh432_max_dd", "mh432_ann_return",
           "mh432_downside_dev", "mh432_sortino", "mh432_verdetto",
           "mh432_mappa",
           "mh431_num", "mh431_equity", "mh431_drawdowns",
           "mh431_max_dd", "mh431_ann_return", "mh431_calmar",
           "mh431_verdetto", "mh431_mappa",
           "mh430_num", "mh430_equity", "mh430_drawdowns",
           "mh430_rebound", "mh430_episodes", "mh430_recovery",
           "mh430_worst", "mh430_verdetto", "mh430_mappa",
           "mh429_num", "mh429_equity", "mh429_drawdowns",
           "mh429_worst", "mh429_attribution",
           "mh427_num", "mh427_equity", "mh427_drawdowns",
           "mh427_path", "mh427_cdar",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain")

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
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
TITLE430 = "🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco"
TITLE429 = "🎯 Attribuzione del drawdown: chi ha causato il peggior calo"
TITLE428 = "⏱️ Tempo sott'acqua: durata dei drawdown e recupero"
TITLE427 = "🛡 CDaR: la perdita media dei peggiori drawdown"
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
UP = 2.8777777777777778
DP = 1.536111111111111
OMEGA = 1.8734177215189876
OMEGA_T2 = 0.6478454680534919
OMEGA_TM2 = 3.7782909930715936
OMEGA_E = 1.5
OMEGA_F = 3.0
MEAN_EF = 0.5
SORTINO = 1.2829179004131461
CALMAR = 0.3927964396665778


class TestRegistry433:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 736
        assert "tab433" in dvars
        assert "tab433" in withs

    def test_titoli_allineati_425_426_427_428_429_430_431_432_433(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab425")] == TITLE425
        assert titoli[dvars.index("tab426")] == TITLE426
        assert titoli[dvars.index("tab427")] == TITLE427
        assert titoli[dvars.index("tab428")] == TITLE428
        assert titoli[dvars.index("tab429")] == TITLE429
        assert titoli[dvars.index("tab430")] == TITLE430
        assert titoli[dvars.index("tab431")] == TITLE431
        assert titoli[dvars.index("tab432")] == TITLE432
        assert titoli[dvars.index("tab433")] == TITLE433

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


class TestOmega433:
    def _xs(self):
        return _F["mh433_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh433_mappa"](xs, 0.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["up"] - UP) < 1e-9
        assert abs(m["dp"] - DP) < 1e-9
        assert abs(m["omega"] - OMEGA) < 1e-9
        assert m["verdetto"].startswith("BUONO")
        # demo: UP 2.8778%/per, DP 1.5361%/per, Omega 1.8734 BUONO
        assert m["target"] == 0.0

    def test_identita_omega(self):
        xs = self._xs()
        m = _F["mh433_mappa"](xs, 0.0)
        assert abs(m["omega"] - m["up"] / m["dp"]) < 1e-12
        # UP - DP = media - target (target 0)
        assert abs((m["up"] - m["dp"]) - (m["mean"] - 0.0)) < 1e-12
        # potenziali a mano: denominatore N=36, tutti i periodi
        up = sum(max(0.0, r) for r in xs) / 36.0
        dp = sum(max(0.0, -r) for r in xs) / 36.0
        assert abs(m["up"] - up) < 1e-12
        assert abs(m["dp"] - dp) < 1e-12

    def test_crosscheck_432_431_430_429_427_424(self):
        xs = self._xs()
        m = _F["mh433_mappa"](xs, 0.0)
        s432 = _F["mh432_mappa"](xs, 0.0, 12.0)
        assert abs(s432["sortino"] - SORTINO) < 1e-9
        assert abs(s432["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(s432["mean"] - m["mean"]) < 1e-12
        assert abs(s432["pain"] - m["pain"]) < 1e-12
        c431 = _F["mh431_mappa"](xs, 12.0)
        assert abs(c431["calmar"] - CALMAR) < 1e-9
        assert abs(c431["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(c431["mean"] - m["mean"]) < 1e-12
        # confronto famiglia: Omega BUONO, Sortino BUONO, Calmar DEBOLE
        assert m["verdetto"].startswith("BUONO")
        assert _F["mh432_verdetto"](SORTINO).startswith("BUONO")
        assert _F["mh431_verdetto"](CALMAR).startswith("DEBOLE")
        rec = _F["mh430_recovery"](xs)
        assert abs(rec["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(rec["mean"] - m["mean"]) < 1e-12
        assert abs(rec["pain"] - m["pain"]) < 1e-12
        att = _F["mh429_attribution"](xs)
        assert abs(att["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(att["mean"] - m["mean"]) < 1e-12
        p427 = _F["mh427_path"](xs)
        assert abs(p427["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(p427["mean"] - m["mean"]) < 1e-12
        p424 = _F["mh424_pain"](xs)
        assert abs(p424["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(p424["pain"] - m["pain"]) < 1e-12

    def test_target_media_omega_uno(self):
        xs = self._xs()
        m = _F["mh433_mappa"](xs, MEAN)
        assert abs(m["omega"] - 1.0) < 1e-12
        assert abs(m["up"] - m["dp"]) < 1e-12
        assert m["verdetto"].startswith("DEBOLE")

    def test_stessa_media_omega_diverso(self):
        e = tuple([0.0] * 18 + [30.0, -20.0])
        f = tuple([0.0] * 18 + [15.0, -5.0])
        me = _F["mh433_mappa"](e, 0.0)
        mf = _F["mh433_mappa"](f, 0.0)
        assert abs(me["mean"] - MEAN_EF) < 1e-12
        assert abs(mf["mean"] - MEAN_EF) < 1e-12
        assert abs(me["omega"] - OMEGA_E) < 1e-12
        assert abs(mf["omega"] - OMEGA_F) < 1e-12
        assert OMEGA_E != OMEGA_F
        assert me["verdetto"].startswith("BUONO")
        assert mf["verdetto"].startswith("ECCEZIONALE")

    def test_sensibilita_target(self):
        xs = self._xs()
        o_m2 = _F["mh433_omega"](xs, -2.0)
        o_0 = _F["mh433_omega"](xs, 0.0)
        o_2 = _F["mh433_omega"](xs, 2.0)
        assert abs(o_m2 - OMEGA_TM2) < 1e-9
        assert abs(o_0 - OMEGA) < 1e-9
        assert abs(o_2 - OMEGA_T2) < 1e-9
        assert o_m2 > o_0 > o_2
        assert _F["mh433_verdetto"](o_m2).startswith("ECCEZIONALE")
        assert _F["mh433_verdetto"](o_2).startswith("NEGATIVO")

    def test_verdetto_soglie(self):
        assert _F["mh433_verdetto"](0.0).startswith("NEGATIVO")
        assert _F["mh433_verdetto"](0.99).startswith("NEGATIVO")
        assert _F["mh433_verdetto"](1.0).startswith("DEBOLE")
        assert _F["mh433_verdetto"](1.19).startswith("DEBOLE")
        assert _F["mh433_verdetto"](1.2).startswith("DISCRETO")
        assert _F["mh433_verdetto"](1.49).startswith("DISCRETO")
        assert _F["mh433_verdetto"](1.5).startswith("BUONO")
        assert _F["mh433_verdetto"](1.99).startswith("BUONO")
        assert _F["mh433_verdetto"](2.0).startswith("OTTIMO")
        assert _F["mh433_verdetto"](2.99).startswith("OTTIMO")
        assert _F["mh433_verdetto"](3.0).startswith("ECCEZIONALE")
        assert _F["mh433_verdetto"](float("inf")).startswith("ECCEZIONALE")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh433_mappa"](flat, 0.0)
        assert mf["up"] == 0.0
        assert mf["dp"] == 0.0
        assert mf["omega"] == 1.0
        assert mf["verdetto"].startswith("DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh433_mappa"](gains, 0.0)
        assert mg["dp"] == 0.0
        assert mg["up"] > 0.0
        assert mg["omega"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        losses = tuple([-1.0] * 25)
        ml = _F["mh433_mappa"](losses, 0.0)
        assert ml["up"] == 0.0
        assert ml["dp"] > 0.0
        assert ml["omega"] == 0.0
        assert ml["verdetto"].startswith("NEGATIVO")
        for bad in (lambda: _F["mh433_mappa"]((1.0,) * 19, 0.0),
                    lambda: _F["mh433_mappa"](None, 0.0),
                    lambda: _F["mh433_mappa"](tuple([0.0] * 19 + [-100.0]), 0.0),
                    lambda: _F["mh433_omega"](self._xs(), float("nan")),
                    lambda: _F["mh433_upside_potential"](self._xs(), "x"),
                    lambda: _F["mh433_verdetto"](float("nan"))):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh433_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh433_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh433_parse_serie"]("1\n2\n")

