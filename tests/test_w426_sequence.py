
"""Test tab426 '🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown': registry + funzioni pure."""

import math
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh426_num", "mh426_parse_serie", "mh426_equity",
           "mh426_drawdowns", "mh426_path", "mh426_bound",
           "mh426_percentile", "mh426_shuffle", "mh426_simulazione",
           "mh426_verdetto", "mh426_mappa",
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain",
           "mh422_num", "mh422_equity", "mh422_drawdowns",
           "mh422_maxdd", "mh422_calmar")

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
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
PAIN = 4.694975808579396
ULCER = 12.513733768880378
CALMAR = 0.030387329606364723
MEAN = 1.3416666666666666
BOUND = 44.15217408197824
MED = 19.481898000000005
P5 = 13.999999999999998
P95 = 30.108659999999993
PGT = 0.055
ASCPAIN = 19.398843279591347
DESCPAIN = 4.05420778408784
ASCULCER = 25.22125163771801
DESCULCER = 11.244070820277617


class TestRegistry426:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 687
        assert "tab426" in dvars
        assert "tab426" in withs

    def test_titoli_allineati_420_421_422_423_424_425_426(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab420")] == TITLE420
        assert titoli[dvars.index("tab421")] == TITLE421
        assert titoli[dvars.index("tab422")] == TITLE422
        assert titoli[dvars.index("tab423")] == TITLE423
        assert titoli[dvars.index("tab424")] == TITLE424
        assert titoli[dvars.index("tab425")] == TITLE425
        assert titoli[dvars.index("tab426")] == TITLE426

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


class TestSeq426:
    def _xs(self):
        return _F["mh426_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh426_mappa"](xs, 200, 30.0)
        d = m["demo"]
        assert abs(d["max_dd"] - MAXDD) < 1e-12
        assert abs(d["pain"] - PAIN) < 1e-12
        assert abs(d["ulcer"] - ULCER) < 1e-12
        assert abs(d["calmar"] - CALMAR) < 1e-12
        assert abs(d["mean"] - MEAN) < 1e-12
        # media 1.3417%/per, maxDD 44.1522%, Pain 4.6950%,
        # Ulcer 12.5137%, Calmar 0.0304 (stessi di tab421-424)
        assert abs(d["mean"] - 1.3417) < 1e-3
        assert abs(d["max_dd"] - 44.1522) < 1e-3
        assert abs(d["pain"] - 4.6950) < 1e-3
        assert abs(d["ulcer"] - 12.5137) < 1e-3
        assert abs(d["calmar"] - 0.0304) < 1e-3
        assert abs(m["bound"] - BOUND) < 1e-12
        assert abs(m["bound"] - 44.1522) < 1e-3
        s = m["sim"]
        assert s["n_sim"] == 200
        assert abs(s["med_maxdd"] - MED) < 1e-12
        assert abs(s["p5_maxdd"] - P5) < 1e-12
        assert abs(s["p95_maxdd"] - P95) < 1e-12
        assert abs(m["p_gt_soglia"] - PGT) < 1e-12
        assert abs(m["p_gt_soglia"] - 0.055) < 1e-9
        assert m["verdetto"].startswith("CONTROLLATO")
        # la demo e' il caso peggiore, non il tipico
        assert s["med_maxdd"] < d["max_dd"]
        assert s["max_maxdd"] <= m["bound"] + 1e-9
        assert len(s["worst"]) == 5
        assert s["worst"][0]["max_dd"] == s["max_maxdd"]

    def test_definizione_a_mano(self):
        # equity composta -> running max (peak iniziale 100) ->
        # drawdown punto per punto, indipendente dall'helper
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
        p = _F["mh426_path"](tuple(xs))
        assert abs(p["pain"] - pain_mano) < 1e-9
        assert abs(p["ulcer"] - ulcer_mano) < 1e-9
        assert abs(p["max_dd"] - max(dds)) < 1e-9
        assert abs(p["mean"] - sum(xs) / n) < 1e-12
        assert abs(p["calmar"] - p["mean"] / p["max_dd"]) < 1e-12
        # ulcer >= pain >= 0 (RMS >= AM), max_dd >= pain
        assert p["ulcer"] >= p["pain"] >= 0.0
        assert p["max_dd"] >= p["pain"]
        # drawdowns helper identici, punto per punto
        dd = _F["mh426_drawdowns"](tuple(xs))
        assert len(dd) == n
        for a, b in zip(dd, dds):
            assert abs(a - b) < 1e-9
        # equity helper: ultimo valore a mano
        eqs = _F["mh426_equity"](tuple(xs))
        assert abs(eqs[-1] - eq) < 1e-9

    def test_chiave_teorica_bound_maxdd(self):
        # CHIAVE TEORICA 1: per OGNI ordinamento,
        #   maxDD <= 1 - prod(1 + perdita_i) sulle sole perdite.
        # Gli ordinamenti estremi (guadagni poi perdite E perdite
        # poi guadagni) RAGGIUNGONO il bound; la demo stessa
        # (guadagni poi perdite) lo raggiunge.
        xs = self._xs()
        m = _F["mh426_mappa"](xs, 200, 30.0)
        assert abs(m["demo"]["max_dd"] - m["bound"]) < 1e-9
        assert abs(m["asc"]["max_dd"] - m["bound"]) < 1e-9
        assert abs(m["desc"]["max_dd"] - m["bound"]) < 1e-9
        # bound a mano: prodotto sulle sole perdite
        prod = 1.0
        for x in xs:
            if x < 0.0:
                prod *= 1.0 + x / 100.0
        assert abs(m["bound"] - (1.0 - prod) * 100.0) < 1e-9
        # tutti gli shuffle sotto il bound
        assert all(v <= m["bound"] + 1e-9
                   for v in m["sim"]["maxdds"])
        # serie senza perdite: bound 0
        assert _F["mh426_bound"](tuple([1.0] * 25)) == 0.0

    def test_chiave_teorica_momenti_invarianti(self):
        # CHIAVE TEORICA 2: media e deviazione standard sono
        # IDENTICHE per ogni shuffle (stesso multiset); il maxDD
        # varia: la distribuzione esiste solo perche' il percorso
        # conta.
        xs = self._xs()
        mean0 = statistics.mean(xs)
        std0 = statistics.pstdev(xs)
        seen = set()
        for seed in (426000, 426001, 426042, 426199):
            sh = _F["mh426_shuffle"](xs, seed)
            assert sorted(sh) == sorted(xs)
            assert abs(statistics.mean(sh) - mean0) < 1e-12
            assert abs(statistics.pstdev(sh) - std0) < 1e-12
            seen.add(round(_F["mh426_path"](sh)["max_dd"], 9))
        assert len(seen) == 4
        m = _F["mh426_mappa"](xs, 200, 30.0)
        assert len(set(round(v, 9)
                       for v in m["sim"]["maxdds"])) > 100

    def test_chiave_teorica_stesso_maxdd_pain_diverso(self):
        # CHIAVE TEORICA 3: asc e desc hanno lo STESSO maxDD
        # (bound) ma Pain diverso: il Pain misura QUANTO A LUNGO
        # resti sott'acqua, non solo quanto scendi.
        xs = self._xs()
        m = _F["mh426_mappa"](xs, 200, 30.0)
        assert abs(m["asc"]["max_dd"] - m["desc"]["max_dd"]) < 1e-9
        assert abs(m["asc"]["pain"] - ASCPAIN) < 1e-12
        assert abs(m["desc"]["pain"] - DESCPAIN) < 1e-12
        assert abs(m["asc"]["ulcer"] - ASCULCER) < 1e-12
        assert abs(m["desc"]["ulcer"] - DESCULCER) < 1e-12
        assert m["asc"]["pain"] > m["desc"]["pain"]
        assert m["asc"]["ulcer"] > m["desc"]["ulcer"]
        # perdite prima = sott'acqua dall'inizio (Pain alto);
        # guadagni prima = sott'acqua solo alla fine (Pain basso)
        assert abs(m["asc"]["pain"] - 19.3988) < 1e-3
        assert abs(m["desc"]["pain"] - 4.0542) < 1e-3

    def test_chiave_teorica_concentrazione_dolore(self):
        # CHIAVE TEORICA 4: perdite concentrate in fila danno maxDD
        # maggiore che perdite alternate a guadagni.
        conc = tuple([2.0] * 10 + [-5.0] * 10)
        alt = tuple([2.0, -5.0] * 10)
        pc = _F["mh426_path"](conc)
        pa = _F["mh426_path"](alt)
        assert pc["max_dd"] > pa["max_dd"]
        # concentrate a mano: picco 100*1.02^10, calo 1-0.95^10
        assert abs(pc["max_dd"] - (1.0 - 0.95 ** 10) * 100.0) < 1e-9
        # alternate a mano: picco 102 dopo il primo +2%, finale
        # 100*0.969^10, maxDD dal picco 102
        assert abs(pa["max_dd"]
                   - (102.0 - 100.0 * 0.969 ** 10) / 102.0 * 100.0) < 1e-9

    def test_crosscheck_gemelli(self):
        # tab424 Pain e tab422 Calmar sulla demo: stessi numeri
        # (stessa convenzione peak iniziale = 100).
        xs = self._xs()
        d = _F["mh426_mappa"](xs, 200, 30.0)["demo"]
        pain424 = _F["mh424_pain"](xs)
        assert abs(pain424["pain"] - d["pain"]) < 1e-12
        assert abs(pain424["ulcer"] - d["ulcer"]) < 1e-12
        assert abs(pain424["max_dd"] - d["max_dd"]) < 1e-12
        cal422 = _F["mh422_calmar"](xs, 0.0)
        assert abs(cal422["calmar"] - d["calmar"]) < 1e-12
        assert abs(cal422["max_dd"] - d["max_dd"]) < 1e-12

    def test_shuffle_deterministico(self):
        xs = self._xs()
        a = _F["mh426_shuffle"](xs, 426000)
        b = _F["mh426_shuffle"](xs, 426000)
        assert a == b
        c = _F["mh426_shuffle"](xs, 426001)
        assert c != a
        assert sorted(a) == sorted(xs)
        # simulazione deterministica: due run identiche
        s1 = _F["mh426_simulazione"](xs, 50, 30.0)
        s2 = _F["mh426_simulazione"](xs, 50, 30.0)
        assert s1["maxdds"] == s2["maxdds"]
        assert s1["worst"] == s2["worst"]
        # seed_base diverso -> almeno un maxDD diverso
        s3 = _F["mh426_simulazione"](xs, 50, 30.0, 999000)
        assert s3["maxdds"] != s1["maxdds"]
        # percentile nearest-rank
        assert _F["mh426_percentile"]([1.0, 2.0, 3.0, 4.0, 5.0,
                                        6.0, 7.0, 8.0, 9.0, 10.0],
                                       50) == 5.0
        assert _F["mh426_percentile"]([1.0, 2.0, 3.0], 0) == 1.0
        assert _F["mh426_percentile"]([1.0, 2.0, 3.0], 100) == 3.0

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh426_verdetto"](0.0).startswith("ROBUSTO")
        assert F["mh426_verdetto"](0.05).startswith("CONTROLLATO")
        assert F["mh426_verdetto"](0.099).startswith("CONTROLLATO")
        assert F["mh426_verdetto"](0.10).startswith("SENSIBILE")
        assert F["mh426_verdetto"](0.20).startswith("SENSIBILE")
        assert F["mh426_verdetto"](0.25).startswith("FRAGILE")
        assert F["mh426_verdetto"](0.40).startswith("FRAGILE")
        assert F["mh426_verdetto"](0.50).startswith("MOLTO FRAGILE")
        assert F["mh426_verdetto"](0.60).startswith("MOLTO FRAGILE")
        assert F["mh426_verdetto"](0.75).startswith("CRITICO")
        assert F["mh426_verdetto"](0.90).startswith("CRITICO")
        assert F["mh426_verdetto"](1.0).startswith("CRITICO")
        for _bad in (float("nan"), True, -0.1, 1.1, "x"):
            with pytest.raises(ValueError):
                F["mh426_verdetto"](_bad)

    def test_casi_degeneri(self):
        F = _F
        # serie piatta: maxDD 0, calmar 0.0, simulazione tutta a 0
        p = F["mh426_path"](tuple([0.0] * 25))
        assert p["max_dd"] == 0.0
        assert p["calmar"] == 0.0
        assert p["pain"] == 0.0
        m = F["mh426_mappa"](tuple([0.0] * 25), 50, 30.0)
        assert m["sim"]["max_maxdd"] == 0.0
        assert m["p_gt_soglia"] == 0.0
        assert m["verdetto"].startswith("ROBUSTO")
        # solo guadagni: maxDD 0, calmar +inf
        g = F["mh426_path"](tuple([1.0] * 25))
        assert g["max_dd"] == 0.0
        assert math.isinf(g["calmar"]) and g["calmar"] > 0
        # solo perdite: bound = maxDD (tutto in fila dal picco)
        lo = tuple([-2.0] * 25)
        assert abs(F["mh426_path"](lo)["max_dd"]
                   - F["mh426_bound"](lo)) < 1e-9
        # soglia estrema: p_gt a 0% = 1.0 se c'e' un drawdown
        s0 = F["mh426_simulazione"](self._xs(), 50, 0.0)
        assert s0["p_gt_soglia"] == 1.0
        # n_sim fuori range / non intero
        for _bad in (lambda: F["mh426_simulazione"](self._xs(), 9),
                     lambda: F["mh426_simulazione"](self._xs(), 2001),
                     lambda: F["mh426_simulazione"](self._xs(), 10.5),
                     lambda: F["mh426_simulazione"](self._xs(), True),
                     lambda: F["mh426_simulazione"](self._xs(), 50, -1.0),
                     lambda: F["mh426_simulazione"](self._xs(), 50, 101.0),
                     lambda: F["mh426_simulazione"](self._xs(), 50, 30.0,
                                                    True),
                     lambda: F["mh426_shuffle"](self._xs(), 1.5),
                     lambda: F["mh426_shuffle"](self._xs(), True),
                     lambda: F["mh426_percentile"]([1.0], -1.0),
                     lambda: F["mh426_percentile"]([1.0], 101.0),
                     lambda: F["mh426_percentile"]([], 50),
                     lambda: F["mh426_mappa"]((1.0,) * 19, 50, 30.0),
                     lambda: F["mh426_mappa"](None, 50, 30.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_validatori(self):
        for _bad in (lambda: _F["mh426_path"](None),
                     lambda: _F["mh426_path"]((1.0,) * 19),
                     lambda: _F["mh426_path"](self._xs()[:5]),
                     lambda: _F["mh426_bound"]((1.0,) * 19),
                     lambda: _F["mh426_drawdowns"]((1.0,) * 19),
                     lambda: _F["mh426_equity"]((1.0,) * 19),
                     lambda: _F["mh426_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh426_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh426_parse_serie"](None),
                     lambda: _F["mh426_num"](True, "x"),
                     lambda: _F["mh426_num"](float("nan"), "x"),
                     lambda: _F["mh426_num"](float("inf"), "x"),
                     lambda: _F["mh426_num"]("x", "x"),
                     lambda: _F["mh426_mappa"]((1.0,) * 19, 50, 30.0),
                     lambda: _F["mh426_mappa"](None, 50, 30.0),
                     lambda: _F["mh426_simulazione"](None, 50, 30.0),
                     lambda: _F["mh426_shuffle"](None, 1)):
            with pytest.raises(ValueError):
                _bad()

