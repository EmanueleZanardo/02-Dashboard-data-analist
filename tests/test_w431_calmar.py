
"""Test tab431 '📐 Calmar ratio: rendimento per unita' di peggior perdita': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh431_num", "mh431_parse_serie", "mh431_equity",
           "mh431_drawdowns", "mh431_max_dd", "mh431_ann_return",
           "mh431_calmar", "mh431_verdetto", "mh431_mappa",
           "mh430_num", "mh430_equity", "mh430_drawdowns",
           "mh430_rebound", "mh430_episodes", "mh430_recovery",
           "mh430_worst", "mh430_verdetto", "mh430_mappa",
           "mh429_num", "mh429_equity", "mh429_drawdowns",
           "mh429_worst", "mh429_attribution",
           "mh427_num", "mh427_equity", "mh427_drawdowns",
           "mh427_path", "mh427_cdar",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain")

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
CALMAR = 0.3927964396665778
CALMAR_PPY1 = 0.03038732960636465
CALMAR_PPY52 = 2.264353988941508
CALMAR_PAIR = 0.024999999999999467
ANN_A = 0.49999999999998934
ANN_B = 0.24999999999999467
DD_A = 20.0
DD_B = 10.0
CALMAR_DD20 = 0.8671408391470002
CALMAR_DD40 = 0.4335704195735001


class TestRegistry431:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 583
        assert "tab431" in dvars
        assert "tab431" in withs

    def test_titoli_allineati_425_426_427_428_429_430_431(self):
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


class TestCalmar431:
    def _xs(self):
        return _F["mh431_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh431_mappa"](xs, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["calmar"] - CALMAR) < 1e-9
        assert m["verdetto"].startswith("DEBOLE")
        # demo: ann 17.3428%, maxDD 44.1522%, Calmar 0.3928 DEBOLE
        assert m["ppy"] == 12.0

    def test_identita_calmar(self):
        xs = self._xs()
        m = _F["mh431_mappa"](xs, 12.0)
        assert abs(m["calmar"] - m["ann"] / m["max_dd"]) < 1e-12
        assert abs(m["ann"] - ((1.0 + m["mean"] / 100.0) ** 12.0 - 1.0) * 100.0) < 1e-9

    def test_crosscheck_430_429_427_424(self):
        xs = self._xs()
        m = _F["mh431_mappa"](xs, 12.0)
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

    def test_stesso_calmar_storie_diverse(self):
        a = tuple([0.0] * 18 + [30.0, -20.0])
        b = tuple([0.0] * 18 + [15.0, -10.0])
        ca = _F["mh431_calmar"](a, 1.0)
        cb = _F["mh431_calmar"](b, 1.0)
        assert abs(ca - CALMAR_PAIR) < 1e-12
        assert abs(cb - CALMAR_PAIR) < 1e-12
        assert abs(_F["mh431_ann_return"](a, 1.0) - ANN_A) < 1e-12
        assert abs(_F["mh431_ann_return"](b, 1.0) - ANN_B) < 1e-12
        assert abs(_F["mh431_max_dd"](a) - DD_A) < 1e-12
        assert abs(_F["mh431_max_dd"](b) - DD_B) < 1e-12
        assert ANN_A != ANN_B and DD_A != DD_B

    def test_sensibilita_annualizzazione(self):
        xs = self._xs()
        c1 = _F["mh431_calmar"](xs, 1.0)
        c12 = _F["mh431_calmar"](xs, 12.0)
        c52 = _F["mh431_calmar"](xs, 52.0)
        assert abs(c1 - CALMAR_PPY1) < 1e-9
        assert abs(c12 - CALMAR) < 1e-9
        assert abs(c52 - CALMAR_PPY52) < 1e-9
        assert c1 < c12 < c52
        assert _F["mh431_verdetto"](c1).startswith("DEBOLE")
        assert _F["mh431_verdetto"](c52).startswith("OTTIMO")

    def test_dd_raddoppio_dimezza(self):
        xs = self._xs()
        ann = _F["mh431_ann_return"](xs, 12.0)
        assert abs(ann / 20.0 - CALMAR_DD20) < 1e-9
        assert abs(ann / 40.0 - CALMAR_DD40) < 1e-9
        assert abs(CALMAR_DD20 / CALMAR_DD40 - 2.0) < 1e-12

    def test_verdetto_soglie(self):
        assert _F["mh431_verdetto"](-0.1).startswith("NEGATIVO")
        assert _F["mh431_verdetto"](0.0).startswith("DEBOLE")
        assert _F["mh431_verdetto"](0.49).startswith("DEBOLE")
        assert _F["mh431_verdetto"](0.5).startswith("DISCRETO")
        assert _F["mh431_verdetto"](0.99).startswith("DISCRETO")
        assert _F["mh431_verdetto"](1.0).startswith("BUONO")
        assert _F["mh431_verdetto"](1.99).startswith("BUONO")
        assert _F["mh431_verdetto"](2.0).startswith("OTTIMO")
        assert _F["mh431_verdetto"](2.99).startswith("OTTIMO")
        assert _F["mh431_verdetto"](3.0).startswith("ECCEZIONALE")
        assert _F["mh431_verdetto"](float("inf")).startswith("ECCEZIONALE")
        assert _F["mh431_verdetto"](float("-inf")).startswith("NEGATIVO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh431_mappa"](flat, 12.0)
        assert mf["max_dd"] == 0.0
        assert mf["ann"] == 0.0
        assert mf["calmar"] == 0.0
        assert mf["verdetto"].startswith("DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh431_mappa"](gains, 12.0)
        assert mg["max_dd"] == 0.0
        assert mg["ann"] > 0.0
        assert mg["calmar"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        for bad in (lambda: _F["mh431_mappa"]((1.0,) * 19, 12.0),
                    lambda: _F["mh431_mappa"](None, 12.0),
                    lambda: _F["mh431_mappa"](tuple([0.0] * 19 + [-100.0]), 12.0),
                    lambda: _F["mh431_calmar"](self._xs(), 0.0),
                    lambda: _F["mh431_calmar"](self._xs(), -12.0),
                    lambda: _F["mh431_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh431_verdetto"](float("nan"))):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh431_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh431_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh431_parse_serie"]("1\n2\n")

