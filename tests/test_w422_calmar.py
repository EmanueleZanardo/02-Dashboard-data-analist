
"""Test tab422 '🎯 Calmar ratio: il rendimento medio contro il peggior drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh422_num", "mh422_parse_serie", "mh422_equity",
           "mh422_drawdowns", "mh422_maxdd", "mh422_calmar",
           "mh422_verdetto", "mh422_curva", "mh422_mappa",
           "mh421_num", "mh421_equity", "mh421_drawdowns",
           "mh421_ulcer", "mh421_martin",
           "mh419_star", "mh419_check_delta", "mh419_num")

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
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
CALMAR = 0.030387329606364723
MEAN = 1.3416666666666666
MAXDD = 44.15217408197824
WORST_I = 36


class TestRegistry422:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 622
        assert "tab422" in dvars
        assert "tab422" in withs

    def test_titoli_allineati_417_418_419_420_421_422(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab417")] == TITLE417
        assert titoli[dvars.index("tab418")] == TITLE418
        assert titoli[dvars.index("tab419")] == TITLE419
        assert titoli[dvars.index("tab420")] == TITLE420
        assert titoli[dvars.index("tab421")] == TITLE421
        assert titoli[dvars.index("tab422")] == TITLE422

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


class TestCalmar422:
    def _xs(self):
        return _F["mh422_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh422_mappa"](xs, 0.0)
        assert abs(m["calmar"] - CALMAR) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert m["worst_i"] == WORST_I
        # media 1.3417%, maxDD 44.1522% al periodo 36 (crash finale):
        # il peggior drawdown schiaccia il rapporto
        assert abs(m["mean"] - 103.6 / 36.0 + 55.3 / 36.0) < 1e-9
        assert m["n_dd"] == 6
        assert m["worst_i"] == 36
        assert m["calmar"] < 1.0
        assert m["verdetto"].startswith("NEGATIVO")
        assert 0.02 < m["calmar"] < 0.05
        # definizione: calmar = eccesso / maxDD
        assert abs(m["calmar"] - m["excess"] / m["max_dd"]) < 1e-12
        # maxDD >= drawdown medio (max >= media)
        assert m["max_dd"] >= m["mean_dd"]

    def test_definizione_a_mano(self):
        # equity composta + running max + dd, indipendente dall'helper
        xs = list(self._xs())
        eq, dd, peak = 100.0, [], 100.0
        for x in xs:
            eq *= 1.0 + x / 100.0
            peak = max(peak, eq)
            dd.append((peak - eq) / peak * 100.0)
        n = len(xs)
        mean = sum(xs) / n
        k = _F["mh422_calmar"](tuple(xs), 0.0)
        assert abs(k["mean"] - mean) < 1e-12
        assert abs(k["max_dd"] - max(dd)) < 1e-12
        assert k["worst_i"] == dd.index(max(dd)) + 1
        assert abs(k["calmar"] - mean / max(dd)) < 1e-12
        assert abs(_F["mh422_maxdd"](tuple(xs))["max_dd"]
                   - max(dd)) < 1e-12
        # i drawdown dell'helper coincidono punto per punto
        for a, b in zip(_F["mh422_drawdowns"](tuple(xs)), dd):
            assert abs(a - b) < 1e-12
        # l'equity dell'helper coincide
        e0 = 100.0
        for a, x in zip(_F["mh422_equity"](tuple(xs)), xs):
            e0 *= 1.0 + x / 100.0
            assert abs(a - e0) < 1e-9

    def test_crosscheck_tab421_upi_vs_calmar(self):
        # gemelli di percorso: stesso numeratore (media - 0), una
        # volta / Ulcer (UPI), una volta / maxDD (Calmar). Per
        # eccesso > 0 vale SEMPRE Calmar <= UPI (max >= RMS).
        # Sulla demo: maxDD 44.15% >> ulcer 12.51% => il Calmar e'
        # molto piu' severo (0.03 vs 0.11), entrambi NEGATIVI.
        xs = self._xs()
        cal = _F["mh422_calmar"](xs, 0.0)["calmar"]
        upi = _F["mh421_martin"](xs, 0.0)["upi"]
        ulc = _F["mh421_ulcer"](xs)["ulcer"]
        mdd = _F["mh422_maxdd"](xs)["max_dd"]
        assert mdd >= ulc
        assert cal <= upi
        assert cal < 1.0 and upi < 1.0
        assert abs(cal - 0.0304) < 0.005
        assert abs(upi - 0.1072) < 0.005
        assert _F["mh422_verdetto"](cal).startswith("NEGATIVO")

    def test_crosscheck_tab419_star(self):
        # il Calmar e' piu' severo anche dello STAR: maxDD 44.15%
        # >> ETL 12.10% (stesso numeratore)
        xs = self._xs()
        cal = _F["mh422_calmar"](xs, 0.0)["calmar"]
        star = _F["mh419_star"](xs, 0.05)["star"]
        assert cal < star < 1.0

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        base = F["mh422_calmar"](xs, 0.0)["calmar"]
        # alzare i rendimenti di +1: media sale -> Calmar sale
        up = tuple(x + 1.0 for x in xs)
        assert F["mh422_calmar"](up, 0.0)["calmar"] > base
        # approfondire i crash: maxDD piu' fondo -> Calmar scende
        dn = tuple(x - 1.0 if x < 0.0 else x for x in xs)
        assert F["mh422_calmar"](dn, 0.0)["calmar"] < base
        # alzare il target: numeratore cala -> Calmar scende
        assert F["mh422_calmar"](xs, 2.5)["calmar"] < base
        assert F["mh422_calmar"](xs, -2.5)["calmar"] > base

    def test_non_invarianza_di_scala(self):
        # CHIAVE TEORICA (proprieta' intenzionale, non bug): il
        # drawdown e' una funzione di percorso non lineare
        # dell'equity composta, quindi Calmar(2x) != Calmar(x).
        # Come per l'UPI (tab421).
        xs = self._xs()
        base = _F["mh422_calmar"](xs, 0.0)["calmar"]
        sc = tuple(2.0 * x for x in xs)
        cal2 = _F["mh422_calmar"](sc, 0.0)["calmar"]
        assert abs(cal2 - base) > 1e-6
        # sulla demo 2x migliora leggermente (0.0378 vs 0.0304):
        # il numeratore raddoppia, il maxDD cresce meno che in
        # proporzione (70.90% < 2 x 44.15%)
        assert abs(cal2 - 0.0378) < 0.005

    def test_infinito_senza_drawdown(self):
        # solo guadagni: mai sott'acqua -> maxDD=0 -> +inf
        k = _F["mh422_calmar"](tuple([1.0] * 25), 0.0)
        assert math.isinf(k["calmar"]) and k["calmar"] > 0
        assert k["max_dd"] == 0.0
        assert _F["mh422_verdetto"](k["calmar"]).startswith("MOLTO FORTE")
        # serie piatta su 0: eccesso=0, maxDD=0 -> non definito
        with pytest.raises(ValueError):
            _F["mh422_calmar"](tuple([0.0] * 25), 0.0)
        # serie piatta a 2% con T=0: eccesso>0, maxDD=0 -> +inf
        k2 = _F["mh422_calmar"](tuple([2.0] * 25), 0.0)
        assert math.isinf(k2["calmar"]) and k2["calmar"] > 0
        # serie piatta a 2% con T=5: eccesso<0, maxDD=0 -> -inf
        k3 = _F["mh422_calmar"](tuple([2.0] * 25), 5.0)
        assert math.isinf(k3["calmar"]) and k3["calmar"] < 0
        assert _F["mh422_verdetto"](k3["calmar"]).startswith("NEGATIVO")

    def test_curva(self):
        F = _F
        xs = self._xs()
        c = F["mh422_curva"](xs, -2.0, 2.0, 1.0)
        assert len(c) == 5
        assert [t for t, _ in c] == [-2.0, -1.0, 0.0, 1.0, 2.0]
        # il punto a T=0 e' il Calmar della demo
        assert abs(dict(c)[0.0] - CALMAR) < 1e-12
        # monotona decrescente in T (numeratore cala, maxDD fissa)
        uu = [u for _, u in c]
        assert all(u is not None for u in uu)
        assert all(a > b for a, b in zip(uu, uu[1:]))
        # ogni punto coincide con calmar al target T
        for t, u in c:
            mio = F["mh422_calmar"](xs, t)["calmar"]
            assert abs(u - mio) < 1e-12
        with pytest.raises(ValueError):
            F["mh422_curva"](None)
        with pytest.raises(ValueError):
            F["mh422_curva"](xs, 2.0, -2.0, 1.0)
        with pytest.raises(ValueError):
            F["mh422_curva"](xs, -2.0, 2.0, 0.0)

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh422_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh422_verdetto"](-3.0).startswith("NEGATIVO")
        assert F["mh422_verdetto"](float("-inf")).startswith("NEGATIVO")
        assert F["mh422_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh422_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh422_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh422_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh422_verdetto"](2.0).startswith("BUONO")
        assert F["mh422_verdetto"](2.99).startswith("BUONO")
        assert F["mh422_verdetto"](3.0).startswith("FORTE")
        assert F["mh422_verdetto"](4.99).startswith("FORTE")
        assert F["mh422_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh422_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh422_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh422_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        with pytest.raises(ValueError):
            F["mh422_calmar"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh422_mappa"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh422_mappa"]((1.0,) * 19, 0.0)
        with pytest.raises(ValueError):
            F["mh422_mappa"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh422_maxdd"]((1.0,) * 19)
        # target cattivo contro la sua funzione (lezione tab417)
        for _t in (True, "x", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                F["mh422_calmar"](self._xs(), _t)

    def test_validatori(self):
        for _bad in (lambda: _F["mh422_calmar"](None, 0.0),
                     lambda: _F["mh422_calmar"]((1.0,) * 19, 0.0),
                     lambda: _F["mh422_calmar"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh422_calmar"](self._xs(), True),
                     lambda: _F["mh422_calmar"](self._xs(), float("nan")),
                     lambda: _F["mh422_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh422_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh422_parse_serie"](None),
                     lambda: _F["mh422_num"](True, "x"),
                     lambda: _F["mh422_num"](float("nan"), "x"),
                     lambda: _F["mh422_mappa"]((1.0,) * 19, 0.0),
                     lambda: _F["mh422_mappa"](None, 0.0),
                     lambda: _F["mh422_mappa"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh422_mappa"](self._xs(), True),
                     lambda: _F["mh422_curva"](None),
                     lambda: _F["mh422_curva"](self._xs(), 1.0, -1.0),
                     lambda: _F["mh422_curva"](self._xs(), 0.0, 1.0, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh422_mappa"](DEMO, 0.0)
        assert abs(m["calmar"] - CALMAR) < 1e-12
        assert abs(m["upi"] - _F["mh421_martin"](self._xs(), 0.0)
                   ["upi"]) < 1e-12
        assert abs(m["star"] - _F["mh419_star"](self._xs(), 0.05)
                   ["star"]) < 1e-12

