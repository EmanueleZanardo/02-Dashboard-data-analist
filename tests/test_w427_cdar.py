
"""Test tab427 '🛡 CDaR: la perdita media dei peggiori drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh427_num", "mh427_parse_serie", "mh427_equity",
           "mh427_drawdowns", "mh427_path", "mh427_cdar",
           "mh427_curva", "mh427_verdetto", "mh427_mappa",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain",
           "mh422_num", "mh422_equity", "mh422_drawdowns",
           "mh422_maxdd", "mh422_calmar")

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
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
CDAR10 = 35.875782277214554
VAR10 = 27.773759999999996
CDAR5 = 40.98041559442912
CDAR20 = 21.12739113860728
CDAR25 = 18.779903234317583
CDAR50 = 9.389951617158792
PAIN = 4.694975808579396
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
RATIO10 = 0.03739755850616773
RATIO100 = 0.2857664706631636
CONCPAIN = 11.880009227646003
CONCCDAR = 38.550682551850606
ALTPAIN = 15.035665573198646
ALTCDAR = 27.300815004078338


class TestRegistry427:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 522
        assert "tab427" in dvars
        assert "tab427" in withs

    def test_titoli_allineati_421_422_423_424_425_426_427(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab421")] == TITLE421
        assert titoli[dvars.index("tab422")] == TITLE422
        assert titoli[dvars.index("tab423")] == TITLE423
        assert titoli[dvars.index("tab424")] == TITLE424
        assert titoli[dvars.index("tab425")] == TITLE425
        assert titoli[dvars.index("tab426")] == TITLE426
        assert titoli[dvars.index("tab427")] == TITLE427

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


class TestCdar427:
    def _xs(self):
        return _F["mh427_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh427_mappa"](xs, 10.0, 20.0)
        d = m["demo"]
        assert abs(d["mean"] - MEAN) < 1e-12
        assert abs(d["max_dd"] - MAXDD) < 1e-12
        assert abs(d["pain"] - PAIN) < 1e-12
        # media 1.3417%/per, maxDD 44.1522%, Pain 4.6950%
        # (stessi di tab421-426)
        assert abs(d["mean"] - 1.3417) < 1e-3
        assert abs(d["max_dd"] - 44.1522) < 1e-3
        assert abs(d["pain"] - 4.6950) < 1e-3
        c = m["cdar"]
        assert c["alpha"] == 10.0
        assert c["k"] == 4
        assert abs(c["cdar"] - CDAR10) < 1e-12
        assert abs(c["var_dd"] - VAR10) < 1e-12
        assert abs(c["ratio"] - RATIO10) < 1e-12
        assert abs(c["cdar"] - 35.8758) < 1e-3
        assert abs(c["var_dd"] - 27.7738) < 1e-3
        assert abs(c["ratio"] - 0.0374) < 1e-3
        assert m["verdetto"].startswith("MOLTO FRAGILE")
        # curva: 6 punti, k attesi, CDaR(100%) = Pain
        assert len(m["curva"]) == 6
        by_a = {r["alpha"]: r for r in m["curva"]}
        assert abs(by_a[5.0]["cdar"] - CDAR5) < 1e-12
        assert abs(by_a[20.0]["cdar"] - CDAR20) < 1e-12
        assert abs(by_a[25.0]["cdar"] - CDAR25) < 1e-12
        assert abs(by_a[50.0]["cdar"] - CDAR50) < 1e-12
        assert abs(by_a[100.0]["cdar"] - PAIN) < 1e-12
        assert [r["k"] for r in m["curva"]] == [2, 4, 8, 9, 18, 36]
        assert abs(by_a[5.0]["cdar"] - 40.9804) < 1e-3
        assert abs(by_a[20.0]["cdar"] - 21.1274) < 1e-3
        assert abs(by_a[25.0]["cdar"] - 18.7799) < 1e-3
        assert abs(by_a[50.0]["cdar"] - 9.3900) < 1e-3
        # solo 6 periodi sott'acqua: per alpha >= 20% VaR-DD = 0
        assert by_a[20.0]["var_dd"] == 0.0
        assert by_a[100.0]["var_dd"] == 0.0

    def test_definizione_a_mano(self):
        # equity composta -> running max (peak iniziale 100) ->
        # drawdown punto per punto -> sort desc -> media top-k
        xs = list(self._xs())
        eq = 100.0
        peak = 100.0
        dds = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            peak = max(peak, eq)
            dds.append((peak - eq) / peak * 100.0)
        n = len(xs)
        pain_mano = sum(dds) / n
        ulcer_mano = math.sqrt(sum(v * v for v in dds) / n)
        p = _F["mh427_path"](tuple(xs))
        assert abs(p["pain"] - pain_mano) < 1e-9
        assert abs(p["ulcer"] - ulcer_mano) < 1e-9
        assert abs(p["max_dd"] - max(dds)) < 1e-9
        assert abs(p["mean"] - sum(xs) / n) < 1e-12
        assert p["ulcer"] >= p["pain"] >= 0.0
        assert p["max_dd"] >= p["pain"]
        dd = _F["mh427_drawdowns"](tuple(xs))
        assert len(dd) == n
        for a, b in zip(dd, dds):
            assert abs(a - b) < 1e-9
        eqs = _F["mh427_equity"](tuple(xs))
        assert abs(eqs[-1] - eq) < 1e-9
        # CDaR(10%) a mano: media dei 4 drawdown peggiori
        srt = sorted(dds, reverse=True)
        c = _F["mh427_cdar"](tuple(xs), 10.0)
        assert abs(c["cdar"] - sum(srt[:4]) / 4) < 1e-9
        assert abs(c["var_dd"] - srt[3]) < 1e-9
        assert c["k"] == 4

    def test_chiave_cdar100_pain_e_limite_maxdd(self):
        # CHIAVE TEORICA 1: CDaR(100%) = Pain; k = 1 -> CDaR = maxDD.
        xs = self._xs()
        c100 = _F["mh427_cdar"](xs, 100.0)
        p = _F["mh427_path"](xs)
        assert abs(c100["cdar"] - p["pain"]) < 1e-12
        assert c100["k"] == len(xs)
        assert abs(c100["ratio"] - RATIO100) < 1e-12
        assert abs(c100["ratio"] - 0.2858) < 1e-3
        # alpha <= 100/n -> k = 1 -> CDaR = maxDD (n = 36)
        for a in (1.0, 100.0 / 36.0, 2.5):
            c = _F["mh427_cdar"](xs, a)
            assert c["k"] == 1
            assert abs(c["cdar"] - p["max_dd"]) < 1e-12
            assert abs(c["var_dd"] - p["max_dd"]) < 1e-12

    def test_chiave_monotonia_e_var(self):
        # CHIAVE TEORICA 2: CDaR decrescente in alpha;
        # Pain <= CDaR(alpha) <= maxDD; CDaR >= VaR-DD.
        xs = self._xs()
        curva = _F["mh427_curva"](xs)
        vals = [r["cdar"] for r in curva]
        assert vals == sorted(vals, reverse=True)
        p = _F["mh427_path"](xs)
        for r in curva:
            assert p["pain"] - 1e-12 <= r["cdar"] <= p["max_dd"] + 1e-12
            assert r["cdar"] + 1e-12 >= r["var_dd"]
        # monotonia stretta dove la coda cambia davvero
        assert curva[0]["cdar"] > curva[1]["cdar"] > curva[2]["cdar"]
        # curva con griglia custom, non ordinata in input
        cc = _F["mh427_curva"](xs, (100.0, 10.0, 50.0))
        assert [r["alpha"] for r in cc] == [10.0, 50.0, 100.0]
        assert abs(cc[0]["cdar"] - CDAR10) < 1e-12

    def test_chiave_pain_vs_cdar_discordano(self):
        # CHIAVE TEORICA 3: Pain e CDaR possono DISACCORDARSI.
        # Alternate: Pain MAGGIORE ma CDaR MINORE della concentrata.
        conc = tuple([2.0] * 10 + [-5.0] * 10)
        alt = tuple([2.0, -5.0] * 10)
        pc = _F["mh427_path"](conc)
        pa = _F["mh427_path"](alt)
        cc = _F["mh427_cdar"](conc, 10.0)
        ca = _F["mh427_cdar"](alt, 10.0)
        assert abs(pc["pain"] - CONCPAIN) < 1e-12
        assert abs(cc["cdar"] - CONCCDAR) < 1e-12
        assert abs(pa["pain"] - ALTPAIN) < 1e-12
        assert abs(ca["cdar"] - ALTCDAR) < 1e-12
        assert pa["pain"] > pc["pain"]
        assert ca["cdar"] < cc["cdar"]
        assert abs(pc["pain"] - 11.8800) < 1e-3
        assert abs(cc["cdar"] - 38.5507) < 1e-3
        assert abs(pa["pain"] - 15.0357) < 1e-3
        assert abs(ca["cdar"] - 27.3008) < 1e-3

    def test_crosscheck_gemelli(self):
        # tab424 Pain e tab422 Calmar/maxDD sulla demo: stessi numeri
        # (stessa convenzione peak iniziale = 100).
        xs = self._xs()
        d = _F["mh427_mappa"](xs, 10.0, 20.0)["demo"]
        pain424 = _F["mh424_pain"](xs)
        assert abs(pain424["pain"] - d["pain"]) < 1e-12
        assert abs(pain424["ulcer"] - d["ulcer"]) < 1e-12
        assert abs(pain424["max_dd"] - d["max_dd"]) < 1e-12
        cal422 = _F["mh422_calmar"](xs, 0.0)
        assert abs(cal422["calmar"] - d["calmar"]) < 1e-12
        assert abs(cal422["max_dd"] - d["max_dd"]) < 1e-12
        # ratio a 100% = mean / pain = Pain ratio tab424
        c100 = _F["mh427_cdar"](xs, 100.0)
        assert abs(c100["ratio"] - d["mean"] / d["pain"]) < 1e-12

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh427_verdetto"](0.0, 20.0).startswith("ROBUSTO")
        assert F["mh427_verdetto"](10.0, 20.0).startswith("CONTROLLATO")
        assert F["mh427_verdetto"](14.9, 20.0).startswith("CONTROLLATO")
        assert F["mh427_verdetto"](15.0, 20.0).startswith("SENSIBILE")
        assert F["mh427_verdetto"](19.9, 20.0).startswith("SENSIBILE")
        assert F["mh427_verdetto"](20.0, 20.0).startswith("FRAGILE")
        assert F["mh427_verdetto"](29.9, 20.0).startswith("FRAGILE")
        assert F["mh427_verdetto"](30.0, 20.0).startswith("MOLTO FRAGILE")
        assert F["mh427_verdetto"](39.9, 20.0).startswith("MOLTO FRAGILE")
        assert F["mh427_verdetto"](40.0, 20.0).startswith("CRITICO")
        assert F["mh427_verdetto"](80.0, 20.0).startswith("CRITICO")
        for _bad in (lambda: F["mh427_verdetto"](-1.0, 20.0),
                     lambda: F["mh427_verdetto"](float("nan"), 20.0),
                     lambda: F["mh427_verdetto"](10.0, 0.0),
                     lambda: F["mh427_verdetto"](10.0, 101.0),
                     lambda: F["mh427_verdetto"](10.0, True),
                     lambda: F["mh427_verdetto"]("x", 20.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_casi_degeneri(self):
        F = _F
        # serie piatta: CDaR 0, ratio 0.0, verdetto ROBUSTO
        p = F["mh427_path"](tuple([0.0] * 25))
        assert p["max_dd"] == 0.0
        c = F["mh427_cdar"](tuple([0.0] * 25), 10.0)
        assert c["cdar"] == 0.0 and c["var_dd"] == 0.0
        assert c["ratio"] == 0.0
        m = F["mh427_mappa"](tuple([0.0] * 25), 10.0, 20.0)
        assert m["verdetto"].startswith("ROBUSTO")
        # solo guadagni: CDaR 0, ratio +inf
        g = F["mh427_cdar"](tuple([1.0] * 25), 10.0)
        assert g["cdar"] == 0.0
        assert math.isinf(g["ratio"]) and g["ratio"] > 0
        # solo perdite: CDaR vicino al maxDD (coda = quasi tutto)
        lo = tuple([-2.0] * 25)
        clo = F["mh427_cdar"](lo, 10.0)
        assert clo["cdar"] <= F["mh427_path"](lo)["max_dd"] + 1e-9
        assert clo["cdar"] > F["mh427_path"](lo)["pain"]
        # alpha fuori (0, 100] / non numerico
        for _bad in (lambda: F["mh427_cdar"](self._xs(), 0.0),
                     lambda: F["mh427_cdar"](self._xs(), 100.5),
                     lambda: F["mh427_cdar"](self._xs(), -5.0),
                     lambda: F["mh427_cdar"](self._xs(), True),
                     lambda: F["mh427_cdar"](self._xs(), "x"),
                     lambda: F["mh427_curva"](self._xs(), (10.0, 0.0)),
                     lambda: F["mh427_curva"](self._xs(), ()),
                     lambda: F["mh427_curva"](self._xs(), 10.0),
                     lambda: F["mh427_mappa"]((1.0,) * 19, 10.0, 20.0),
                     lambda: F["mh427_mappa"](None, 10.0, 20.0),
                     lambda: F["mh427_mappa"](self._xs(), 10.0, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_validatori(self):
        for _bad in (lambda: _F["mh427_path"](None),
                     lambda: _F["mh427_path"]((1.0,) * 19),
                     lambda: _F["mh427_path"](self._xs()[:5]),
                     lambda: _F["mh427_cdar"]((1.0,) * 19, 10.0),
                     lambda: _F["mh427_cdar"](None, 10.0),
                     lambda: _F["mh427_drawdowns"]((1.0,) * 19),
                     lambda: _F["mh427_equity"]((1.0,) * 19),
                     lambda: _F["mh427_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh427_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh427_parse_serie"](None),
                     lambda: _F["mh427_num"](True, "x"),
                     lambda: _F["mh427_num"](float("nan"), "x"),
                     lambda: _F["mh427_num"](float("inf"), "x"),
                     lambda: _F["mh427_num"]("x", "x"),
                     lambda: _F["mh427_mappa"]((1.0,) * 19, 10.0, 20.0),
                     lambda: _F["mh427_mappa"](None, 10.0, 20.0),
                     lambda: _F["mh427_curva"](None),
                     lambda: _F["mh427_curva"]((1.0,) * 19)):
            with pytest.raises(ValueError):
                _bad()

