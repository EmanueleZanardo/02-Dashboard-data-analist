"""Test tab440 '🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh440_num", "mh440_parse_serie", "mh440_equity",
           "mh440_drawdowns", "mh440_max_dd", "mh440_ann_return",
           "mh440_dar", "mh440_curva", "mh440_verdetto", "mh440_mappa",
           "mh439_num", "mh439_parse_serie", "mh439_equity",
           "mh439_drawdowns", "mh439_max_dd", "mh439_ann_return",
           "mh439_cdar", "mh439_cdar_ratio", "mh439_curva",
           "mh439_curva_ppy", "mh439_verdetto", "mh439_mappa",
           "mh438_num", "mh438_parse_serie", "mh438_equity",
           "mh438_drawdowns", "mh438_max_dd",
           "mh438_ann_return", "mh438_pain",
           "mh438_pain_ratio", "mh438_verdetto", "mh438_mappa",
           "mh437_num", "mh437_parse_serie", "mh437_equity",
           "mh437_drawdowns", "mh437_max_dd",
           "mh437_ann_return", "mh437_yearly_max_dds",
           "mh437_avg_max_dd", "mh437_sterling",
           "mh437_verdetto", "mh437_mappa",
           "mh436_num", "mh436_parse_serie", "mh436_equity",
           "mh436_drawdowns", "mh436_max_dd", "mh436_ulcer",
           "mh436_ann_return", "mh436_martin", "mh436_verdetto",
           "mh436_mappa",
           "mh435_num", "mh435_parse_serie", "mh435_equity",
           "mh435_drawdowns", "mh435_max_dd", "mh435_ann_return",
           "mh435_lpm", "mh435_kappa", "mh435_verdetto",
           "mh435_mappa",
           "mh434_num", "mh434_parse_serie", "mh434_equity",
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
           "mh424_num", "mh424_equity", "mh424_drawdowns", "mh424_pain",
           "mh421_num", "mh421_equity", "mh421_drawdowns",
           "mh421_ulcer", "mh421_martin")

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
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
ANN = 17.342816782940005
DAR10 = 27.773759999999996
DAR5 = 37.80865710688
DAR20 = 0.0
DAR25 = 0.0
DAR50 = 0.0
DAR100 = 0.0
CDAR10 = 35.875782277214554
CDAR5 = 40.98041559442912
CDAR20 = 21.12739113860728
CDAR25 = 18.779903234317583
CDAR50 = 9.389951617158792
CDAR100 = 4.694975808579396
GAP10 = 8.102022277214559
GAP5 = 3.17175848754912
CDARRATIO10 = 0.48341292320627066
PAINRATIO = 3.6939097218027177
STERLING = 1.1783893189997336
MARTIN = 1.385902649301104
KAPPA = 1.389386420473165
BURKE = 0.23098377488351735
OMEGA = 1.8734177215189876
SORTINO = 1.2829179004131461
CALMAR = 0.3927964396665778
DAR_C = 20.0
DAR_D = 10.0
CDAR_CD = 20.0
MAXDD_C = 20.0
MAXDD_D = 30.0
MEAN_C = 1.75
MEAN_D = 5.5
NGT_C = 0
NGT_D = 1


class TestRegistry440:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 630
        assert "tab440" in dvars
        assert "tab440" in withs

    def test_titoli_allineati_431_432_433_434_435_436_437_438_439_440(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab431")] == TITLE431
        assert titoli[dvars.index("tab432")] == TITLE432
        assert titoli[dvars.index("tab433")] == TITLE433
        assert titoli[dvars.index("tab434")] == TITLE434
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440

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


class TestDaR440:
    def _xs(self):
        return _F["mh440_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh440_mappa"](xs, 10.0, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["dar"] - DAR10) < 1e-9
        assert abs(m["cdar"] - CDAR10) < 1e-9
        assert abs(m["gap"] - GAP10) < 1e-9
        assert m["verdetto"].startswith("DISCRETO")
        # demo: DaR(10%) 27.7738%, CDaR(10%) 35.8758%, gap 8.1020
        assert m["ppy"] == 12.0
        assert m["alpha"] == 10.0
        assert m["k"] == 4
        assert m["n_dd"] == 6
        assert m["n_ge"] >= m["k"]
        assert m["n_gt"] == 3
        # in_coda: esattamente k periodi, i peggiori
        assert sum(m["in_coda"]) == m["k"] == 4
        assert len(m["in_coda"]) == 36
        # oltre: esattamente i periodi con drawdown > DaR
        assert sum(m["oltre"]) == m["n_gt"] == 3
        # DaR <= CDaR <= maxDD
        assert m["dar"] <= m["cdar"] <= m["max_dd"]
        assert m["gap"] == m["cdar"] - m["dar"]

    def test_identita_dar(self):
        xs = self._xs()
        m = _F["mh440_mappa"](xs, 10.0, 12.0)
        # DaR a mano: k-esimo drawdown peggiore
        dds = _F["mh440_drawdowns"](xs)
        top = sorted(dds, reverse=True)[:4]
        assert abs(top[-1] - m["dar"]) < 1e-12
        assert abs(sum(top) / 4 - m["cdar"]) < 1e-12
        assert abs(_F["mh440_dar"](xs, 10.0)["dar"] - m["dar"]) < 1e-12
        # DaR = VaR-DD di tab427/tab439 allo stesso alpha
        assert abs(_F["mh439_cdar"](xs, 10.0)["var_dd"] - m["dar"]) < 1e-12
        assert abs(_F["mh427_cdar"](xs, 10.0)["var_dd"] - m["dar"]) < 1e-12
        # k = 1 (alpha 1%) -> DaR = CDaR = maxDD, gap = 0
        c1 = _F["mh440_dar"](xs, 1.0)
        assert c1["k"] == 1
        assert abs(c1["dar"] - MAXDD) < 1e-12
        assert abs(c1["cdar"] - MAXDD) < 1e-12
        assert abs(c1["gap"]) < 1e-12
        assert abs(_F["mh440_mappa"](xs, 1.0, 12.0)["dar"] - MAXDD) < 1e-12
        # alpha = 100% -> DaR = drawdown minimo (0: 30 periodi al picco)
        c100 = _F["mh440_dar"](xs, 100.0)
        assert c100["k"] == 36
        assert abs(c100["dar"] - DAR100) < 1e-12
        assert abs(c100["dar"] - min(dds)) < 1e-12
        assert abs(c100["cdar"] - PAIN) < 1e-12
        # curva a gradini NON CRESCENTE in alpha; CDaR pure
        curva = _F["mh440_curva"](xs, (5.0, 10.0, 20.0, 25.0, 50.0, 100.0))
        dars = [c["dar"] for c in curva]
        assert dars == sorted(dars, reverse=True)
        assert abs(dars[0] - DAR5) < 1e-9
        assert abs(dars[1] - DAR10) < 1e-9
        assert abs(dars[2] - DAR20) < 1e-9
        assert abs(dars[3] - DAR25) < 1e-9
        assert abs(dars[4] - DAR50) < 1e-9
        assert abs(dars[5] - DAR100) < 1e-9
        cdars = [c["cdar"] for c in curva]
        assert cdars == sorted(cdars, reverse=True)
        assert abs(cdars[0] - CDAR5) < 1e-9
        assert abs(cdars[1] - CDAR10) < 1e-9
        assert abs(cdars[2] - CDAR20) < 1e-9
        assert abs(cdars[3] - CDAR25) < 1e-9
        assert abs(cdars[4] - CDAR50) < 1e-9
        assert abs(cdars[5] - CDAR100) < 1e-9
        # gap = cdar - dar su ogni punto della curva; il DaR
        # crolla a 0 da alpha 20% (k=8 > 6 periodi sott'acqua)
        for c in curva:
            assert abs(c["gap"] - (c["cdar"] - c["dar"])) < 1e-12
        assert abs(curva[0]["gap"] - GAP5) < 1e-9
        assert abs(curva[1]["gap"] - GAP10) < 1e-9

    def test_crosscheck_439_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh440_mappa"](xs, 10.0, 12.0)
        m439 = _F["mh439_mappa"](xs, 10.0, 12.0)
        assert abs(m439["cdar_ratio"] - CDARRATIO10) < 1e-9
        assert abs(m439["cdar"] - m["cdar"]) < 1e-12
        assert abs(m439["var_dd"] - m["dar"]) < 1e-12
        assert abs(m439["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m439["mean"] - m["mean"]) < 1e-12
        assert abs(m439["pain"] - m["pain"]) < 1e-12
        m438 = _F["mh438_mappa"](xs, 12.0)
        assert abs(m438["pain_ratio"] - PAINRATIO) < 1e-9
        assert abs(m438["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m438["mean"] - m["mean"]) < 1e-12
        assert abs(m438["pain"] - m["pain"]) < 1e-12
        s437 = _F["mh437_mappa"](xs, 12.0)
        assert abs(s437["sterling"] - STERLING) < 1e-9
        assert abs(s437["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(s437["mean"] - m["mean"]) < 1e-12
        assert abs(s437["pain"] - m["pain"]) < 1e-12
        ma436 = _F["mh436_mappa"](xs, 12.0)
        assert abs(ma436["martin"] - MARTIN) < 1e-9
        assert abs(ma436["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(ma436["mean"] - m["mean"]) < 1e-12
        assert abs(ma436["pain"] - m["pain"]) < 1e-12
        k435 = _F["mh435_mappa"](xs, 12.0)
        assert abs(k435["kappa"] - KAPPA) < 1e-9
        assert abs(k435["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(k435["mean"] - m["mean"]) < 1e-12
        assert abs(k435["pain"] - m["pain"]) < 1e-12
        b434 = _F["mh434_mappa"](xs, 12.0)
        assert abs(b434["burke"] - BURKE) < 1e-9
        assert abs(b434["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(b434["mean"] - m["mean"]) < 1e-12
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
        # confronto famiglia: DaR DISCRETO, CDaR ratio DEBOLE,
        # Pain ratio OTTIMO, Sterling BUONO, Martin BUONO,
        # Kappa-3 BUONO, Sortino BUONO, Omega BUONO, Burke
        # DISCRETO, Calmar DEBOLE
        assert m["verdetto"].startswith("DISCRETO")
        assert _F["mh439_verdetto"](CDARRATIO10).startswith("DEBOLE")
        assert _F["mh438_verdetto"](PAINRATIO).startswith("OTTIMO")
        assert _F["mh437_verdetto"](STERLING).startswith("BUONO")
        assert _F["mh436_verdetto"](MARTIN).startswith("BUONO")
        assert _F["mh435_verdetto"](KAPPA).startswith("BUONO")
        assert _F["mh434_verdetto"](BURKE).startswith("DISCRETO")
        assert _F["mh433_verdetto"](OMEGA).startswith("BUONO")
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
        assert abs(p427["pain"] - m["pain"]) < 1e-12
        c427 = _F["mh427_cdar"](xs, 10.0)
        assert abs(c427["cdar"] - m["cdar"]) < 1e-12
        assert abs(c427["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(c427["var_dd"] - m["dar"]) < 1e-12
        p424 = _F["mh424_pain"](xs)
        assert abs(p424["pain"] - m["pain"]) < 1e-12
        assert abs(p424["max_dd"] - m["max_dd"]) < 1e-12
        u421 = _F["mh421_ulcer"](xs)
        assert abs(u421["max_dd"] - m["max_dd"]) < 1e-12

    def test_stesso_cdar_dar_diverso(self):
        c = tuple([25.0, -20.0, 25.0, -20.0, 25.0] + [0.0] * 15)
        d = tuple([50.0, -30.0, 50.0, -10.0, 50.0] + [0.0] * 15)
        mc = _F["mh440_mappa"](c, 10.0, 10.0)
        md = _F["mh440_mappa"](d, 10.0, 10.0)
        # STESSO CDaR(10%) = 20.0 su entrambe
        assert abs(mc["cdar"] - CDAR_CD) < 1e-12
        assert abs(md["cdar"] - CDAR_CD) < 1e-12
        # DaR DIVERSO: C 20.0 (coda piatta) vs D 10.0 (concentrata)
        assert abs(mc["dar"] - DAR_C) < 1e-12
        assert abs(md["dar"] - DAR_D) < 1e-12
        assert abs(mc["dar"] / md["dar"] - 2.0) < 1e-9
        assert mc["gap"] == 0.0
        assert abs(md["gap"] - 10.0) < 1e-12
        assert mc["n_gt"] == NGT_C == 0
        assert md["n_gt"] == NGT_D == 1
        assert _F["mh440_verdetto"](DAR_C).startswith("BUONO")
        assert _F["mh440_verdetto"](DAR_D).startswith("OTTIMO")
        # il DaR da solo inganna: D ha maxDD PEGGIORE (30 > 20)
        # eppure DaR D (10) < DaR C (20) — il DaR non vede oltre
        # la soglia. Medie diverse, ma la chiave e' il CDaR uguale.
        assert abs(mc["max_dd"] - MAXDD_C) < 1e-12
        assert abs(md["max_dd"] - MAXDD_D) < 1e-12
        assert md["max_dd"] > mc["max_dd"]
        assert md["dar"] < mc["dar"]
        assert abs(mc["mean"] - MEAN_C) < 1e-12
        assert abs(md["mean"] - MEAN_D) < 1e-12

    def test_indipendenza_ppy_e_alpha(self):
        xs = self._xs()
        # il DaR NON dipende da ppy: stessa soglia a ppy 1/12/52
        assert abs(_F["mh440_mappa"](xs, 10.0, 1.0)["dar"] - DAR10) < 1e-12
        assert abs(_F["mh440_mappa"](xs, 10.0, 52.0)["dar"] - DAR10) < 1e-12
        assert abs(_F["mh440_mappa"](xs, 10.0, 1.0)["cdar"] - CDAR10) < 1e-12
        # ppy non intero AMMESSO: dar invariato, ann = ann(12.5)
        m125 = _F["mh440_mappa"](xs, 10.0, 12.5)
        assert abs(m125["dar"] - DAR10) < 1e-12
        assert abs(m125["ann"] - _F["mh440_ann_return"](xs, 12.5)) < 1e-9
        # sensibilita' ad alpha a ppy 12: gradini decrescenti
        for alpha, atteso in ((5.0, DAR5), (20.0, DAR20),
                              (25.0, DAR25), (50.0, DAR50),
                              (100.0, DAR100)):
            assert abs(_F["mh440_dar"](xs, alpha)["dar"] - atteso) < 1e-9
        assert _F["mh440_verdetto"](DAR5).startswith("DEBOLE")
        assert _F["mh440_verdetto"](DAR20).startswith("ECCEZIONALE")

    def test_verdetto_soglie(self):
        assert _F["mh440_verdetto"](0.0).startswith("ECCEZIONALE")
        assert _F["mh440_verdetto"](5.0).startswith("ECCEZIONALE")
        assert _F["mh440_verdetto"](5.001).startswith("OTTIMO")
        assert _F["mh440_verdetto"](10.0).startswith("OTTIMO")
        assert _F["mh440_verdetto"](10.001).startswith("BUONO")
        assert _F["mh440_verdetto"](20.0).startswith("BUONO")
        assert _F["mh440_verdetto"](20.001).startswith("DISCRETO")
        assert _F["mh440_verdetto"](30.0).startswith("DISCRETO")
        assert _F["mh440_verdetto"](30.001).startswith("DEBOLE")
        assert _F["mh440_verdetto"](40.0).startswith("DEBOLE")
        assert _F["mh440_verdetto"](40.001).startswith("CRITICO")
        assert _F["mh440_verdetto"](100.0).startswith("CRITICO")
        assert _F["mh440_verdetto"](float("inf")).startswith("CRITICO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh440_mappa"](flat, 10.0, 12.0)
        assert mf["dar"] == 0.0
        assert mf["cdar"] == 0.0
        assert mf["gap"] == 0.0
        assert mf["verdetto"].startswith("ECCEZIONALE")
        gains = tuple([1.0] * 25)
        mg = _F["mh440_mappa"](gains, 10.0, 12.0)
        assert mg["dar"] == 0.0
        assert mg["cdar"] == 0.0
        assert mg["ann"] > 0.0
        assert mg["verdetto"].startswith("ECCEZIONALE")
        for bad in (lambda: _F["mh440_mappa"]((1.0,) * 19, 10.0, 12.0),
                    lambda: _F["mh440_mappa"](None, 10.0, 12.0),
                    lambda: _F["mh440_mappa"](tuple([0.0] * 19 + [-100.0]), 10.0, 12.0),
                    lambda: _F["mh440_dar"](self._xs(), 0.0),
                    lambda: _F["mh440_dar"](self._xs(), 101.0),
                    lambda: _F["mh440_dar"](self._xs(), -5.0),
                    lambda: _F["mh440_mappa"](self._xs(), 10.0, 0.0),
                    lambda: _F["mh440_mappa"](self._xs(), 10.0, -12.0),
                    lambda: _F["mh440_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh440_verdetto"](float("nan")),
                    lambda: _F["mh440_verdetto"](-0.1),
                    lambda: _F["mh440_verdetto"]("10")):
            with pytest.raises(ValueError):
                bad()

    def test_in_coda_e_oltre(self):
        xs = self._xs()
        m = _F["mh440_mappa"](xs, 10.0, 12.0)
        dds = list(m["dds"])
        in_coda = m["in_coda"]
        oltre = m["oltre"]
        assert sum(in_coda) == m["k"]
        # ogni drawdown in coda >= ogni drawdown fuori coda
        dentro = [dds[i] for i in range(len(dds)) if in_coda[i]]
        fuori = [dds[i] for i in range(len(dds)) if not in_coda[i]]
        assert min(dentro) >= max(fuori)
        assert abs(min(dentro) - m["dar"]) < 1e-12
        # oltre <=> drawdown strettamente sopra il DaR
        for i in range(len(dds)):
            assert oltre[i] == (dds[i] > m["dar"])
        assert sum(oltre) == m["n_gt"]
        # n_ge conta anche i pareggi col DaR
        assert m["n_ge"] == sum(1 for d in dds if d >= m["dar"])
        assert m["n_ge"] >= m["k"]

    def test_parse_serie(self):
        xs = _F["mh440_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh440_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh440_parse_serie"]("1\n2\n")

