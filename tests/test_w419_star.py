
"""Test tab419 '⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh419_num", "mh419_parse_serie", "mh419_check_delta",
           "mh419_media", "mh419_etl", "mh419_star", "mh419_verdetto",
           "mh419_mappa", "mh418_etl", "mh418_rachev", "mh418_num",
           "mh418_check_coda")

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
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
DEMO_D = 0.05
MEDIA = 1.3416666666666666
ETL = 12.1
STAR = 0.11088154269972451


class TestRegistry419:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 468
        assert "tab419" in dvars
        assert "tab419" in withs

    def test_titoli_allineati_414_415_416_417_418_419(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab414")] == TITLE414
        assert titoli[dvars.index("tab415")] == TITLE415
        assert titoli[dvars.index("tab416")] == TITLE416
        assert titoli[dvars.index("tab417")] == TITLE417
        assert titoli[dvars.index("tab418")] == TITLE418
        assert titoli[dvars.index("tab419")] == TITLE419

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab468"
        assert titoli[-1] == TITLE468
        assert withs[-1] == "tab468"


class TestStar419:
    def _xs(self):
        return _F["mh419_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh419_mappa"](xs, DEMO_D)
        assert m["delta"] == DEMO_D
        assert m["n_down"] == 2
        assert abs(m["media"] - MEDIA) < 1e-12
        assert abs(m["etl"] - ETL) < 1e-12
        assert abs(m["star"] - STAR) < 1e-12
        assert abs(m["media"] - 48.3 / 36.0) < 1e-12
        assert abs(m["etl"] - 12.1) < 1e-12
        assert m["q_down"] == -10.2
        assert abs(m["p_sopra"] - 30.0 / 36.0) < 1e-12
        # la coda mangia la media: verdetto NEGATIVO, come il Rachev
        assert m["verdetto"].startswith("NEGATIVO")
        assert 0.11 < m["star"] < 0.12
        assert abs(m["star"] - m["media"] / m["etl"]) < 1e-12

    def test_definizione_a_mano(self):
        # STAR_delta = media / ETL_delta, ETL = media delle perdite
        # delle ceil(n*delta) piu' basse in valore assoluto
        xs = list(self._xs())
        n = len(xs)
        media = sum(xs) / n
        srt = sorted(xs)
        for D in (0.05, 0.10, 0.25, 0.01, 0.50):
            kd = math.ceil(n * D)
            etl = sum(-x for x in srt[:kd]) / kd
            star = media / etl
            k = _F["mh419_star"](tuple(xs), D)
            assert abs(k["media"] - media) < 1e-12, D
            assert abs(k["etl"] - etl) < 1e-12, D
            assert abs(k["star"] - star) < 1e-12, D
            assert k["n_down"] == kd
            assert k["q_down"] == max(srt[:kd])
            assert abs(_F["mh419_etl"](tuple(xs), D) - etl) < 1e-12
            assert abs(_F["mh419_media"](tuple(xs)) - media) < 1e-12

    def test_crosscheck_tab418_denominatore(self):
        # tab418 e tab419 condividono lo stesso denominatore ETL:
        # mh419_etl deve coincidere con mh418_etl sulla stessa serie
        xs = self._xs()
        for D in (0.05, 0.10, 0.25):
            assert abs(_F["mh419_etl"](xs, D) -
                       _F["mh418_etl"](xs, D)) < 1e-12, D
        # round-trip: STAR * ETL == media
        k = _F["mh419_star"](xs, 0.05)
        assert abs(k["star"] * k["etl"] - k["media"]) < 1e-12
        # stessa direzione del Rachev tab418: entrambi < 1.0
        rch = _F["mh418_rachev"](xs, 0.05, 0.05)["rachev"]
        assert rch < 1.0 and k["star"] < 1.0

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        # allargare delta include perdite meno estreme: ETL cala,
        # lo STAR sale (la media resta fissa)
        sv = [F["mh419_star"](xs, D)["star"] for D in (0.05, 0.10, 0.25)]
        assert sv[0] < sv[1] < sv[2]
        ev = [F["mh419_etl"](xs, D) for D in (0.05, 0.10, 0.25)]
        assert ev[0] > ev[1] > ev[2]

    def test_infinito_senza_perdite(self):
        # tutti sopra lo 0: nessuna perdita nella coda sinistra -> +inf
        k = _F["mh419_star"](tuple([1.0] * 25), 0.05)
        assert math.isinf(k["star"])
        assert k["etl"] <= 0.0  # nessuna perdita: il denominatore non esiste
        assert _F["mh419_verdetto"](k["star"]).startswith("MOLTO FORTE")

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh419_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh419_verdetto"](-0.5).startswith("NEGATIVO")
        assert F["mh419_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh419_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh419_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh419_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh419_verdetto"](2.0).startswith("BUONO")
        assert F["mh419_verdetto"](2.99).startswith("BUONO")
        assert F["mh419_verdetto"](3.0).startswith("FORTE")
        assert F["mh419_verdetto"](4.99).startswith("FORTE")
        assert F["mh419_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh419_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh419_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh419_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta su 0 -> ValueError
        with pytest.raises(ValueError):
            F["mh419_star"](tuple([0.0] * 25), 0.05)
        with pytest.raises(ValueError):
            F["mh419_mappa"](tuple([0.0] * 25), 0.05)
        with pytest.raises(ValueError):
            F["mh419_mappa"]((1.0,) * 19)
        with pytest.raises(ValueError):
            F["mh419_mappa"](None)
        # delta cattivi: ogni ordine cattivo va testato contro la sua
        # funzione (lezione tab417: non in coppia con uno buono)
        for _d in (0.0, -0.1, 0.51, 1.0, True, "x", float("nan"),
                   float("inf")):
            with pytest.raises(ValueError):
                F["mh419_star"](self._xs(), _d)
            with pytest.raises(ValueError):
                F["mh419_etl"](self._xs(), _d)

    def test_validatori(self):
        for _bad in (lambda: _F["mh419_star"](None),
                     lambda: _F["mh419_star"]((1.0,) * 19),
                     lambda: _F["mh419_star"](tuple([0.0] * 25)),
                     lambda: _F["mh419_star"](self._xs(), 0.0),
                     lambda: _F["mh419_star"](self._xs(), 0.51),
                     lambda: _F["mh419_star"](self._xs(), True),
                     lambda: _F["mh419_media"](None),
                     lambda: _F["mh419_media"]((1.0,) * 19),
                     lambda: _F["mh419_etl"](None, 0.05),
                     lambda: _F["mh419_etl"]((1.0,) * 19, 0.05),
                     lambda: _F["mh419_etl"](self._xs(), -0.1),
                     lambda: _F["mh419_check_delta"](0.0, "d"),
                     lambda: _F["mh419_check_delta"](0.51, "d"),
                     lambda: _F["mh419_check_delta"](True, "d"),
                     lambda: _F["mh419_check_delta"](float("nan"), "d"),
                     lambda: _F["mh419_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh419_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh419_parse_serie"](None),
                     lambda: _F["mh419_num"](True, "x"),
                     lambda: _F["mh419_num"](float("nan"), "x"),
                     lambda: _F["mh419_mappa"]((1.0,) * 19),
                     lambda: _F["mh419_mappa"](None),
                     lambda: _F["mh419_mappa"](
                         tuple([0.0] * 25), 0.05),
                     lambda: _F["mh419_mappa"](self._xs(), 0.0),
                     lambda: _F["mh419_mappa"](self._xs(), 0.99)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh419_mappa"](DEMO, DEMO_D)
        assert abs(m["star"] - STAR) < 1e-12

