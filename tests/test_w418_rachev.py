"""Test tab418 '📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh418_num", "mh418_parse_serie", "mh418_check_coda",
           "mh418_etg", "mh418_etl", "mh418_rachev", "mh418_verdetto",
           "mh418_mappa", "mh406_tail_ratio", "mh406_check_q",
           "mh406_percentile", "mh406_num")

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
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
DEMO_A = 0.05
DEMO_B = 0.05
ETG = 4.9
ETL = 12.1
RACHEV = 0.40495867768595045


class TestRegistry418:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 746
        assert "tab418" in dvars
        assert "tab418" in withs

    def test_titoli_allineati_413_414_415_416_417_418(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab413")] == TITLE413
        assert titoli[dvars.index("tab414")] == TITLE414
        assert titoli[dvars.index("tab415")] == TITLE415
        assert titoli[dvars.index("tab416")] == TITLE416
        assert titoli[dvars.index("tab417")] == TITLE417
        assert titoli[dvars.index("tab418")] == TITLE418

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


class TestRachev418:
    def _xs(self):
        return _F["mh418_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh418_mappa"](xs, DEMO_A, DEMO_B)
        assert m["alpha"] == DEMO_A
        assert m["beta"] == DEMO_B
        assert m["n_up"] == 2 and m["n_down"] == 2
        assert abs(m["etg"] - ETG) < 1e-12
        assert abs(m["etl"] - ETL) < 1e-12
        assert abs(m["rachev"] - RACHEV) < 1e-12
        assert abs(m["etg"] - 4.9) < 1e-12
        assert abs(m["etl"] - 12.1) < 1e-12
        assert m["q_up"] == 4.8
        assert m["q_down"] == -10.2
        assert abs(m["p_sopra"] - 30.0 / 36.0) < 1e-12
        # coda sinistra domina: verdetto NEGATIVO, come il Tail ratio
        assert m["verdetto"].startswith("NEGATIVO")
        assert 0.40 < m["rachev"] < 0.41
        tr = _F["mh406_tail_ratio"](xs, 95.0)
        assert tr < 1.0  # stessa direzione del Rachev

    def test_definizione_a_mano(self):
        # R_{a,b} = ETG_a / ETL_b, medie delle code oltre le soglie
        xs = list(self._xs())
        n = len(xs)
        srt = sorted(xs)
        for A, B in ((0.05, 0.05), (0.05, 0.10), (0.10, 0.05),
                     (0.25, 0.10), (0.01, 0.50)):
            ku = math.ceil(n * A)
            kd = math.ceil(n * B)
            etg = sum(srt[-ku:]) / ku
            etl = sum(-x for x in srt[:kd]) / kd
            rch = etg / etl
            k = _F["mh418_rachev"](tuple(xs), A, B)
            assert abs(k["etg"] - etg) < 1e-12, (A, B)
            assert abs(k["etl"] - etl) < 1e-12, (A, B)
            assert abs(k["rachev"] - rch) < 1e-12, (A, B)
            assert k["n_up"] == ku and k["n_down"] == kd
            assert k["q_up"] == min(srt[-ku:])
            assert k["q_down"] == max(srt[:kd])
            assert abs(_F["mh418_etg"](tuple(xs), A) - etg) < 1e-12
            assert abs(_F["mh418_etl"](tuple(xs), B) - etl) < 1e-12

    def test_crosscheck_tab406_direzione(self):
        # Tail ratio (tab406) e Rachev devono stare dallo stesso lato
        # di 1.0: entrambi < 1 sulla serie con crash risk
        xs = self._xs()
        tr = _F["mh406_tail_ratio"](xs, 95.0)
        rch = _F["mh418_rachev"](xs, 0.05, 0.05)["rachev"]
        assert tr < 1.0 and rch < 1.0
        # il Rachev e' piu' severo: media tutta la coda, il -14.0%
        # pesa per intero (il Tail ratio guarda solo i quantili)
        assert rch < tr

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        # a parita' di b, allargare la coda destra (a alto) diluisce ETG
        ra = [F["mh418_rachev"](xs, A, 0.05)["rachev"]
              for A in (0.05, 0.10, 0.25)]
        assert ra[0] > ra[1] > ra[2]
        # a parita' di a, allargare la coda sinistra (b alto) gonfia
        # il denominatore -> Rachev sale
        rb = [F["mh418_rachev"](xs, 0.05, B)["rachev"]
              for B in (0.05, 0.10, 0.25)]
        assert rb[0] < rb[1] < rb[2]

    def test_infinito_senza_perdite(self):
        # tutti sopra lo 0: nessuna perdita nella coda sinistra -> +inf
        k = _F["mh418_rachev"](tuple([1.0] * 25), 0.05, 0.05)
        assert math.isinf(k["rachev"])
        assert k["etl"] <= 0.0  # nessuna perdita: il denominatore non esiste
        assert _F["mh418_verdetto"](k["rachev"]).startswith("MOLTO FORTE")

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh418_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh418_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh418_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh418_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh418_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh418_verdetto"](2.0).startswith("BUONO")
        assert F["mh418_verdetto"](2.99).startswith("BUONO")
        assert F["mh418_verdetto"](3.0).startswith("FORTE")
        assert F["mh418_verdetto"](4.99).startswith("FORTE")
        assert F["mh418_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh418_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh418_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh418_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta su 0 -> ValueError
        with pytest.raises(ValueError):
            F["mh418_rachev"](tuple([0.0] * 25), 0.05, 0.05)
        with pytest.raises(ValueError):
            F["mh418_mappa"](tuple([0.0] * 25), 0.05, 0.05)
        with pytest.raises(ValueError):
            F["mh418_mappa"]((1.0,) * 19)
        with pytest.raises(ValueError):
            F["mh418_mappa"](None)
        # alpha cattivi: ogni ordine cattivo va testato contro la sua
        # funzione (lezione tab417: non in coppia con uno buono)
        for _a in (0.0, -0.1, 0.51, 1.0, True, "x", float("nan"),
                   float("inf")):
            with pytest.raises(ValueError):
                F["mh418_rachev"](self._xs(), _a, 0.05)
            with pytest.raises(ValueError):
                F["mh418_etg"](self._xs(), _a)
        for _b in (0.0, -0.1, 0.51, 1.0, "x", float("nan")):
            with pytest.raises(ValueError):
                F["mh418_rachev"](self._xs(), 0.05, _b)
            with pytest.raises(ValueError):
                F["mh418_etl"](self._xs(), _b)

    def test_validatori(self):
        for _bad in (lambda: _F["mh418_rachev"](None),
                     lambda: _F["mh418_rachev"]((1.0,) * 19),
                     lambda: _F["mh418_rachev"](tuple([0.0] * 25)),
                     lambda: _F["mh418_rachev"](self._xs(), 0.0, 0.05),
                     lambda: _F["mh418_rachev"](self._xs(), 0.05, 0.51),
                     lambda: _F["mh418_rachev"](self._xs(), 0.05, True),
                     lambda: _F["mh418_etg"](None, 0.05),
                     lambda: _F["mh418_etg"]((1.0,) * 19, 0.05),
                     lambda: _F["mh418_etg"](self._xs(), 0.0),
                     lambda: _F["mh418_etg"](self._xs(), 0.6),
                     lambda: _F["mh418_etl"](None, 0.05),
                     lambda: _F["mh418_etl"]((1.0,) * 19, 0.05),
                     lambda: _F["mh418_etl"](self._xs(), -0.1),
                     lambda: _F["mh418_check_coda"](0.0, "a"),
                     lambda: _F["mh418_check_coda"](0.51, "a"),
                     lambda: _F["mh418_check_coda"](True, "a"),
                     lambda: _F["mh418_check_coda"](float("nan"), "a"),
                     lambda: _F["mh418_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh418_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh418_parse_serie"](None),
                     lambda: _F["mh418_num"](True, "x"),
                     lambda: _F["mh418_num"](float("nan"), "x"),
                     lambda: _F["mh418_mappa"]((1.0,) * 19),
                     lambda: _F["mh418_mappa"](None),
                     lambda: _F["mh418_mappa"](
                         tuple([0.0] * 25), 0.05, 0.05),
                     lambda: _F["mh418_mappa"](self._xs(), 0.0, 0.05),
                     lambda: _F["mh418_mappa"](self._xs(), 0.05, 0.99)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh418_mappa"](DEMO, DEMO_A, DEMO_B)
        assert abs(m["rachev"] - RACHEV) < 1e-12

