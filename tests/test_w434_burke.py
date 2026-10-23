
"""Test tab434 '📉 Burke ratio: rendimento per unita' di drawdown quadratico': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh434_num", "mh434_parse_serie", "mh434_equity",
           "mh434_drawdowns", "mh434_max_dd", "mh434_ann_return",
           "mh434_burke", "mh434_verdetto", "mh434_mappa",
           "mh433_num", "mh433_parse_serie", "mh433_equity",
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
ANN = 17.342816782940005
SUM_DD2 = 5637.367182183016
BURKE = 0.23098377488351735
BURKE_PPY1 = 0.017869255910429788
BURKE_PPY52 = 1.3315523747675233
BURKE_A = 0.024999999999999467
BURKE_G = 0.01118033988749871
ANN_AG = 0.5
MAXDD_AG = 20.0
SUM_DD2_A = 400.0
SUM_DD2_G = 2000.0
SORTINO = 1.2829179004131461
CALMAR = 0.3927964396665778
OMEGA = 1.8734177215189876


class TestRegistry434:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 656
        assert "tab434" in dvars
        assert "tab434" in withs

    def test_titoli_allineati_425_426_427_428_429_430_431_432_433_434(self):
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
        assert titoli[dvars.index("tab434")] == TITLE434

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


class TestBurke434:
    def _xs(self):
        return _F["mh434_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh434_mappa"](xs, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["sum_dd2"] - SUM_DD2) < 1e-6
        assert abs(m["burke"] - BURKE) < 1e-9
        assert m["verdetto"].startswith("DISCRETO")
        # demo: ann 17.3428%, somma dd^2 5637.37, Burke 0.2310 DISCRETO
        assert m["ppy"] == 12.0

    def test_identita_burke(self):
        xs = self._xs()
        m = _F["mh434_mappa"](xs, 12.0)
        assert abs(m["burke"] - m["ann"] / math.sqrt(m["sum_dd2"])) < 1e-12
        assert abs(m["ann"] - ((1.0 + m["mean"] / 100.0) ** 12.0 - 1.0) * 100.0) < 1e-9
        # somma dd^2 a mano
        s2 = sum(d * d for d in _F["mh434_drawdowns"](xs))
        assert abs(m["sum_dd2"] - s2) < 1e-9

    def test_crosscheck_433_432_431_430_429_427_424(self):
        xs = self._xs()
        m = _F["mh434_mappa"](xs, 12.0)
        o433 = _F["mh433_mappa"](xs, 0.0)
        assert abs(o433["omega"] - OMEGA) < 1e-9
        assert abs(o433["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(o433["mean"] - m["mean"]) < 1e-12
        assert abs(o433["pain"] - m["pain"]) < 1e-12
        s432 = _F["mh432_mappa"](xs, 0.0, 12.0)
        assert abs(s432["sortino"] - SORTINO) < 1e-9
        assert abs(s432["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(s432["mean"] - m["mean"]) < 1e-12
        c431 = _F["mh431_mappa"](xs, 12.0)
        assert abs(c431["calmar"] - CALMAR) < 1e-9
        assert abs(c431["max_dd"] - m["max_dd"]) < 1e-12
        # confronto famiglia: Burke DISCRETO, Calmar DEBOLE,
        # Sortino BUONO, Omega BUONO
        assert m["verdetto"].startswith("DISCRETO")
        assert _F["mh431_verdetto"](CALMAR).startswith("DEBOLE")
        assert _F["mh432_verdetto"](SORTINO).startswith("BUONO")
        assert _F["mh433_verdetto"](OMEGA).startswith("BUONO")
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

    def test_stesso_maxdd_media_burke_diverso(self):
        a = tuple([0.0] * 18 + [30.0, -20.0])
        g = tuple([0.0] * 14 + [30.0, -20.0, 0.0, 0.0, 0.0, 0.0])
        ma = _F["mh434_mappa"](a, 1.0)
        mg = _F["mh434_mappa"](g, 1.0)
        assert abs(ma["max_dd"] - MAXDD_AG) < 1e-12
        assert abs(mg["max_dd"] - MAXDD_AG) < 1e-12
        assert abs(ma["mean"] - ANN_AG) < 1e-12
        assert abs(mg["mean"] - ANN_AG) < 1e-12
        assert abs(ma["sum_dd2"] - SUM_DD2_A) < 1e-9
        assert abs(mg["sum_dd2"] - SUM_DD2_G) < 1e-9
        assert abs(ma["burke"] - BURKE_A) < 1e-12
        assert abs(mg["burke"] - BURKE_G) < 1e-12
        assert ma["burke"] > mg["burke"]
        assert abs(ma["burke"] / mg["burke"] - math.sqrt(5.0)) < 1e-9

    def test_sensibilita_annualizzazione(self):
        xs = self._xs()
        b1 = _F["mh434_burke"](xs, 1.0)
        b12 = _F["mh434_burke"](xs, 12.0)
        b52 = _F["mh434_burke"](xs, 52.0)
        assert abs(b1 - BURKE_PPY1) < 1e-9
        assert abs(b12 - BURKE) < 1e-9
        assert abs(b52 - BURKE_PPY52) < 1e-9
        assert b1 < b12 < b52
        assert _F["mh434_verdetto"](b1).startswith("DEBOLE")
        assert _F["mh434_verdetto"](b52).startswith("ECCEZIONALE")

    def test_verdetto_soglie(self):
        assert _F["mh434_verdetto"](-0.1).startswith("NEGATIVO")
        assert _F["mh434_verdetto"](0.0).startswith("DEBOLE")
        assert _F["mh434_verdetto"](0.049).startswith("DEBOLE")
        assert _F["mh434_verdetto"](0.05).startswith("DISCRETO")
        assert _F["mh434_verdetto"](0.249).startswith("DISCRETO")
        assert _F["mh434_verdetto"](0.25).startswith("BUONO")
        assert _F["mh434_verdetto"](0.499).startswith("BUONO")
        assert _F["mh434_verdetto"](0.5).startswith("OTTIMO")
        assert _F["mh434_verdetto"](0.999).startswith("OTTIMO")
        assert _F["mh434_verdetto"](1.0).startswith("ECCEZIONALE")
        assert _F["mh434_verdetto"](float("inf")).startswith("ECCEZIONALE")
        assert _F["mh434_verdetto"](float("-inf")).startswith("NEGATIVO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh434_mappa"](flat, 12.0)
        assert mf["sum_dd2"] == 0.0
        assert mf["ann"] == 0.0
        assert mf["burke"] == 0.0
        assert mf["verdetto"].startswith("DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh434_mappa"](gains, 12.0)
        assert mg["sum_dd2"] == 0.0
        assert mg["ann"] > 0.0
        assert mg["burke"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        for bad in (lambda: _F["mh434_mappa"]((1.0,) * 19, 12.0),
                    lambda: _F["mh434_mappa"](None, 12.0),
                    lambda: _F["mh434_mappa"](tuple([0.0] * 19 + [-100.0]), 12.0),
                    lambda: _F["mh434_burke"](self._xs(), 0.0),
                    lambda: _F["mh434_burke"](self._xs(), -12.0),
                    lambda: _F["mh434_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh434_verdetto"](float("nan"))):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh434_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh434_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh434_parse_serie"]("1\n2\n")

