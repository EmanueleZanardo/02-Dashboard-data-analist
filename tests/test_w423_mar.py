
"""Test tab423 '🔃 MAR ratio: il rendimento composto contro il peggior drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh423_num", "mh423_parse_serie", "mh423_equity",
           "mh423_drawdowns", "mh423_maxdd", "mh423_cagr",
           "mh423_mar", "mh423_verdetto", "mh423_curva",
           "mh423_mappa",
           "mh422_num", "mh422_equity", "mh422_drawdowns",
           "mh422_maxdd", "mh422_calmar",
           "mh411_num", "mh411_drag")

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
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAR = 0.027527732416137336
CAGR = 1.2154092337194111
MEAN = 1.3416666666666666
MAXDD = 44.15217408197824
WORST_I = 36
DRAG = 0.12625743294725544


class TestRegistry423:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 642
        assert "tab423" in dvars
        assert "tab423" in withs

    def test_titoli_allineati_417_418_419_420_421_422_423(self):
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
        assert titoli[dvars.index("tab423")] == TITLE423

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


class TestMar423:
    def _xs(self):
        return _F["mh423_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh423_mappa"](xs, 0.0)
        assert abs(m["mar"] - MAR) < 1e-12
        assert abs(m["cagr"] - CAGR) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert m["worst_i"] == WORST_I
        # CAGR 1.2154% < media 1.3417%: il drag mangia il numeratore
        assert abs(m["cagr"] - 1.2154) < 1e-3
        assert abs(m["mean"] - 1.3417) < 1e-3
        assert m["cagr"] < m["mean"]
        # identita' del drag: media - CAGR = drag di tab411
        assert abs(m["mean"] - m["cagr"] - m["drag"]) < 1e-12
        assert abs(m["drag"] - DRAG) < 1e-12
        assert abs(m["drag"] - 0.1263) < 1e-3
        assert m["n_dd"] == 6
        assert m["worst_i"] == 36
        assert m["mar"] < 1.0
        assert m["verdetto"].startswith("NEGATIVO")
        assert 0.02 < m["mar"] < 0.05
        # definizione: mar = eccesso / maxDD, eccesso = CAGR - T
        assert abs(m["mar"] - m["excess"] / m["max_dd"]) < 1e-12
        assert abs(m["excess"] - (m["cagr"] - 0.0)) < 1e-12
        # maxDD >= drawdown medio (max >= media)
        assert m["max_dd"] >= m["mean_dd"]

    def test_definizione_a_mano(self):
        # equity composta -> CAGR; running max + dd, indipendenti
        xs = list(self._xs())
        eq, dd, peak = 100.0, [], 100.0
        for x in xs:
            eq *= 1.0 + x / 100.0
            peak = max(peak, eq)
            dd.append((peak - eq) / peak * 100.0)
        n = len(xs)
        cagr_mano = (eq / 100.0) ** (1.0 / n) - 1.0
        cagr_mano *= 100.0
        k = _F["mh423_mar"](tuple(xs), 0.0)
        assert abs(k["cagr"] - cagr_mano) < 1e-9
        assert abs(k["max_dd"] - max(dd)) < 1e-12
        assert k["worst_i"] == dd.index(max(dd)) + 1
        assert abs(k["mar"] - cagr_mano / max(dd)) < 1e-12
        assert abs(_F["mh423_maxdd"](tuple(xs))["max_dd"]
                   - max(dd)) < 1e-12
        assert abs(_F["mh423_cagr"](tuple(xs))["eq_finale"] - eq) < 1e-6
        # i drawdown dell'helper coincidono punto per punto
        for a, b in zip(_F["mh423_drawdowns"](tuple(xs)), dd):
            assert abs(a - b) < 1e-12
        # l'equity dell'helper coincide
        e0 = 100.0
        for a, x in zip(_F["mh423_equity"](tuple(xs)), xs):
            e0 *= 1.0 + x / 100.0
            assert abs(a - e0) < 1e-9

    def test_chiave_teorica_mar_minore_uguale_calmar(self):
        # CHIAVE TEORICA: per maxDD > 0 vale SEMPRE MAR <= Calmar,
        # perche' CAGR <= media (AM >= GM sui fattori 1+r/100 > 0).
        # Quinto gemello: STESSO denominatore del Calmar (maxDD),
        # numeratore geometrico invece che aritmetico.
        # Sulla demo: MAR 0.0275 < Calmar 0.0304 < 1.0.
        xs = self._xs()
        mar = _F["mh423_mar"](xs, 0.0)["mar"]
        cal = _F["mh422_calmar"](xs, 0.0)["calmar"]
        assert mar < cal < 1.0
        assert abs(mar - 0.0275) < 0.005
        assert abs(cal - 0.0304) < 0.005
        # serie con un dip: maxDD > 0, MAR < Calmar stretto
        dip = [2.0] * 20
        dip[10] = -5.0
        dip = tuple(dip)
        m2 = _F["mh423_mar"](dip, 0.0)
        c2 = _F["mh422_calmar"](dip, 0.0)["calmar"]
        assert m2["max_dd"] > 0.0
        assert m2["cagr"] < m2["mean"]
        assert m2["mar"] < c2
        # rendimenti costanti: CAGR == media (uguaglianza),
        # maxDD = 0 -> entrambi +inf
        k = _F["mh423_mar"](tuple([2.0] * 25), 0.0)
        assert math.isinf(k["mar"]) and k["mar"] > 0
        assert abs(k["cagr"] - k["mean"]) < 1e-12
        kc = _F["mh422_calmar"](tuple([2.0] * 25), 0.0)
        assert math.isinf(kc["calmar"]) and kc["calmar"] > 0

    def test_crosscheck_tab411_drag(self):
        # il numeratore del MAR e' la media MENO il drag di tab411:
        # mh411_drag(xs)["geo"] == mh423_cagr(xs)["cagr"]
        xs = self._xs()
        d = _F["mh411_drag"](xs)
        g = _F["mh423_cagr"](xs)
        assert abs(d["geo"] - g["cagr"]) < 1e-12
        # drag = media aritmetica - CAGR (identita' del numeratore)
        mean_ = _F["mh423_mar"](xs, 0.0)["mean"]
        assert abs(d["drag"] - (mean_ - g["cagr"])) < 1e-9
        # approssimazione sigma^2/200 vicina al drag vero
        assert abs(d["approx"] - 0.1200) < 1e-3
        assert abs(d["drag"] - d["approx"]) < 0.01
        assert d["drag"] > 0.0
        m = _F["mh423_mappa"](xs, 0.0)
        assert abs(m["drag"] - d["drag"]) < 1e-12
        assert abs(m["approx"] - d["approx"]) < 1e-12

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        base = F["mh423_mar"](xs, 0.0)["mar"]
        # alzare i rendimenti di +1: CAGR sale -> MAR sale
        up = tuple(x + 1.0 for x in xs)
        assert F["mh423_mar"](up, 0.0)["mar"] > base
        # approfondire i crash: maxDD piu' fondo -> MAR scende
        dn = tuple(x - 1.0 if x < 0.0 else x for x in xs)
        assert F["mh423_mar"](dn, 0.0)["mar"] < base
        # alzare il target: numeratore cala -> MAR scende
        assert F["mh423_mar"](xs, 2.5)["mar"] < base
        assert F["mh423_mar"](xs, -2.5)["mar"] > base

    def test_non_invarianza_di_scala(self):
        # CHIAVE TEORICA (proprieta' intenzionale, non bug): il
        # drawdown e' una funzione di percorso non lineare
        # dell'equity composta, quindi MAR(2x) != MAR(x).
        # Come per Calmar (tab422) e UPI (tab421).
        xs = self._xs()
        base = _F["mh423_mar"](xs, 0.0)["mar"]
        sc = tuple(2.0 * x for x in xs)
        mar2 = _F["mh423_mar"](sc, 0.0)["mar"]
        assert abs(mar2 - base) > 1e-6
        assert abs(mar2 - 0.0303) < 0.005

    def test_infinito_senza_drawdown(self):
        # solo guadagni: mai sott'acqua -> maxDD=0 -> +inf
        k = _F["mh423_mar"](tuple([1.0] * 25), 0.0)
        assert math.isinf(k["mar"]) and k["mar"] > 0
        assert k["max_dd"] == 0.0
        assert _F["mh423_verdetto"](k["mar"]).startswith("MOLTO FORTE")
        # serie piatta su 0: eccesso=0, maxDD=0 -> non definito
        with pytest.raises(ValueError):
            _F["mh423_mar"](tuple([0.0] * 25), 0.0)
        # serie piatta a 2% con T=0: eccesso>0, maxDD=0 -> +inf
        k2 = _F["mh423_mar"](tuple([2.0] * 25), 0.0)
        assert math.isinf(k2["mar"]) and k2["mar"] > 0
        # serie piatta a 2% con T=5: eccesso<0, maxDD=0 -> -inf
        k3 = _F["mh423_mar"](tuple([2.0] * 25), 5.0)
        assert math.isinf(k3["mar"]) and k3["mar"] < 0
        assert _F["mh423_verdetto"](k3["mar"]).startswith("NEGATIVO")
        # perdita totale: equity a 0 -> CAGR = -100%
        k4 = _F["mh423_cagr"]((1.0,) * 24 + (-100.0,))
        assert k4["cagr"] == -100.0
        assert k4["eq_finale"] == 0.0
        # rendimento < -100%: fattore negativo -> ValueError
        with pytest.raises(ValueError):
            _F["mh423_cagr"]((1.0,) * 24 + (-101.0,))

    def test_curva(self):
        F = _F
        xs = self._xs()
        c = F["mh423_curva"](xs, -2.0, 2.0, 1.0)
        assert len(c) == 5
        assert [t for t, _ in c] == [-2.0, -1.0, 0.0, 1.0, 2.0]
        # il punto a T=0 e' il MAR della demo
        assert abs(dict(c)[0.0] - MAR) < 1e-12
        # monotona decrescente in T (numeratore cala, maxDD fissa)
        uu = [u for _, u in c]
        assert all(u is not None for u in uu)
        assert all(a > b for a, b in zip(uu, uu[1:]))
        # ogni punto coincide con mar al target T
        for t, u in c:
            mio = F["mh423_mar"](xs, t)["mar"]
            assert abs(u - mio) < 1e-12
        with pytest.raises(ValueError):
            F["mh423_curva"](None)
        with pytest.raises(ValueError):
            F["mh423_curva"](xs, 2.0, -2.0, 1.0)
        with pytest.raises(ValueError):
            F["mh423_curva"](xs, -2.0, 2.0, 0.0)

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh423_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh423_verdetto"](-3.0).startswith("NEGATIVO")
        assert F["mh423_verdetto"](float("-inf")).startswith("NEGATIVO")
        assert F["mh423_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh423_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh423_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh423_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh423_verdetto"](2.0).startswith("BUONO")
        assert F["mh423_verdetto"](2.99).startswith("BUONO")
        assert F["mh423_verdetto"](3.0).startswith("FORTE")
        assert F["mh423_verdetto"](4.99).startswith("FORTE")
        assert F["mh423_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh423_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh423_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh423_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        with pytest.raises(ValueError):
            F["mh423_mar"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh423_mappa"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh423_mappa"]((1.0,) * 19, 0.0)
        with pytest.raises(ValueError):
            F["mh423_mappa"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh423_maxdd"]((1.0,) * 19)
        with pytest.raises(ValueError):
            F["mh423_cagr"]((1.0,) * 19)
        # target cattivo contro la sua funzione (lezione tab417)
        for _t in (True, "x", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                F["mh423_mar"](self._xs(), _t)

    def test_validatori(self):
        for _bad in (lambda: _F["mh423_mar"](None, 0.0),
                     lambda: _F["mh423_mar"]((1.0,) * 19, 0.0),
                     lambda: _F["mh423_mar"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh423_mar"](self._xs(), True),
                     lambda: _F["mh423_mar"](self._xs(), float("nan")),
                     lambda: _F["mh423_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh423_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh423_parse_serie"](None),
                     lambda: _F["mh423_num"](True, "x"),
                     lambda: _F["mh423_num"](float("nan"), "x"),
                     lambda: _F["mh423_mappa"]((1.0,) * 19, 0.0),
                     lambda: _F["mh423_mappa"](None, 0.0),
                     lambda: _F["mh423_mappa"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh423_mappa"](self._xs(), True),
                     lambda: _F["mh423_curva"](None),
                     lambda: _F["mh423_curva"](self._xs(), 1.0, -1.0),
                     lambda: _F["mh423_curva"](self._xs(), 0.0, 1.0, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh423_mappa"](DEMO, 0.0)
        assert abs(m["mar"] - MAR) < 1e-12
        assert abs(m["calmar"] - _F["mh422_calmar"](self._xs(), 0.0)
                   ["calmar"]) < 1e-12
        assert abs(m["drag"] - _F["mh411_drag"](self._xs())
                   ["drag"]) < 1e-12

