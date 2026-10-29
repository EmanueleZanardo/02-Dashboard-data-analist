"""Test tab439 '📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh439_num", "mh439_parse_serie", "mh439_equity",
           "mh439_drawdowns", "mh439_max_dd", "mh439_ann_return",
           "mh439_cdar", "mh439_cdar_ratio", "mh439_curva",
           "mh439_curva_ppy", "mh439_verdetto", "mh439_mappa",
           "mh438_num", "mh438_parse_serie", "mh438_equity",
           "mh438_drawdowns", "mh438_max_dd", "mh438_ann_return",
           "mh438_pain", "mh438_pain_ratio", "mh438_verdetto",
           "mh438_mappa",
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
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
TITLE430 = "🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
ANN = 17.342816782940005
CDAR10 = 35.875782277214554
CDAR5 = 40.98041559442912
CDAR20 = 21.12739113860728
CDAR25 = 18.779903234317583
CDAR50 = 9.389951617158792
CDAR100 = 4.694975808579396
CDARRATIO10 = 0.48341292320627066
CDARRATIO5 = 0.4231976794617376
CDARRATIO20 = 0.8208688270672706
CDARRATIO25 = 0.9234774304506794
CDARRATIO50 = 1.8469548609013589
CDARRATIO100 = 3.6939097218027177
CDARRATIO_PPY1 = 0.03739755850616763
CDARRATIO_PPY52 = 2.786730913083509
CDARRATIO_A = 1.60540825025149
CDARRATIO_B = 0.802704125125745
CDAR_A = 10.0
CDAR_B = 20.0
ANN_AB = 16.0540825025149
MAXDD_AB = 20.0
MEAN_AB = 1.5
CALMAR_AB = 0.802704125125745
PAINRATIO = 3.6939097218027177
STERLING = 1.1783893189997336
MARTIN = 1.385902649301104
KAPPA = 1.389386420473165
BURKE = 0.23098377488351735
OMEGA = 1.8734177215189876
SORTINO = 1.2829179004131461
CALMAR = 0.3927964396665778


class TestRegistry439:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 793
        assert "tab439" in dvars
        assert "tab439" in withs

    def test_titoli_allineati_430_431_432_433_434_435_436_437_438_439(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab430")] == TITLE430
        assert titoli[dvars.index("tab431")] == TITLE431
        assert titoli[dvars.index("tab432")] == TITLE432
        assert titoli[dvars.index("tab433")] == TITLE433
        assert titoli[dvars.index("tab434")] == TITLE434
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439

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


class TestCDaRRatio439:
    def _xs(self):
        return _F["mh439_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh439_mappa"](xs, 10.0, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["cdar"] - CDAR10) < 1e-9
        assert abs(m["cdar_ratio"] - CDARRATIO10) < 1e-9
        assert m["verdetto"].startswith("DEBOLE")
        # demo: ann 17.3428%, CDaR(10%) 35.8758%, CDaR ratio 0.4834 DEBOLE
        assert m["ppy"] == 12.0
        assert m["alpha"] == 10.0
        assert m["k"] == 4
        assert m["n_dd"] == 6
        assert abs(m["var_dd"] - 27.7738) < 1e-3
        # in_coda: esattamente k periodi, i peggiori
        assert sum(m["in_coda"]) == m["k"] == 4
        assert len(m["in_coda"]) == 36
        # Pain <= CDaR <= maxDD
        assert m["pain"] <= m["cdar"] <= m["max_dd"]
        assert m["cdar"] >= m["var_dd"]

    def test_identita_cdar_ratio(self):
        xs = self._xs()
        m = _F["mh439_mappa"](xs, 10.0, 12.0)
        assert abs(m["cdar_ratio"] - m["ann"] / m["cdar"]) < 1e-12
        assert abs(m["ann"] - ((1.0 + m["mean"] / 100.0) ** 12.0 - 1.0) * 100.0) < 1e-9
        # CDaR a mano: media dei k drawdown peggiori
        dds = _F["mh439_drawdowns"](xs)
        top = sorted(dds, reverse=True)[:4]
        assert abs(sum(top) / 4 - m["cdar"]) < 1e-12
        assert abs(_F["mh439_cdar"](xs, 10.0)["cdar"] - m["cdar"]) < 1e-12
        # alpha = 100% -> CDaR = Pain, CDaR ratio = Pain ratio
        c100 = _F["mh439_cdar"](xs, 100.0)
        assert abs(c100["cdar"] - PAIN) < 1e-12
        assert abs(_F["mh439_cdar_ratio"](xs, 100.0, 12.0) - PAINRATIO) < 1e-9
        assert abs(_F["mh439_mappa"](xs, 100.0, 12.0)["cdar_ratio"] - PAINRATIO) < 1e-9
        # k = 1 (alpha 1%) -> CDaR = maxDD, CDaR ratio = Calmar
        c1 = _F["mh439_cdar"](xs, 1.0)
        assert c1["k"] == 1
        assert abs(c1["cdar"] - MAXDD) < 1e-12
        assert abs(_F["mh439_cdar_ratio"](xs, 1.0, 12.0) - CALMAR) < 1e-9
        # gerarchia per ann >= 0: Pain ratio >= CDaR ratio >= Calmar
        assert PAINRATIO >= m["cdar_ratio"] >= CALMAR
        # CDaR ratio < Martin e < Sterling sulla demo (coda piu' severa)
        assert m["cdar_ratio"] < MARTIN
        assert m["cdar_ratio"] < STERLING
        # curva monotona CRESCENTE in alpha
        curva = _F["mh439_curva_ppy"](xs, (5.0, 10.0, 20.0, 25.0, 50.0, 100.0), 12.0)
        ratios = [c["cdar_ratio"] for c in curva]
        assert ratios == sorted(ratios)
        assert abs(ratios[0] - CDARRATIO5) < 1e-9
        assert abs(ratios[1] - CDARRATIO10) < 1e-9
        assert abs(ratios[2] - CDARRATIO20) < 1e-9
        assert abs(ratios[3] - CDARRATIO25) < 1e-9
        assert abs(ratios[4] - CDARRATIO50) < 1e-9
        assert abs(ratios[5] - CDARRATIO100) < 1e-9
        cdars = [c["cdar"] for c in curva]
        assert cdars == sorted(cdars, reverse=True)
        assert abs(cdars[0] - CDAR5) < 1e-9
        assert abs(cdars[5] - CDAR100) < 1e-9

    def test_crosscheck_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh439_mappa"](xs, 10.0, 12.0)
        m438 = _F["mh438_mappa"](xs, 12.0)
        assert abs(m438["pain_ratio"] - PAINRATIO) < 1e-9
        assert abs(m438["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m438["mean"] - m["mean"]) < 1e-12
        assert abs(m438["pain"] - m["pain"]) < 1e-12
        # CDaR ratio(100%) = Pain ratio di tab438
        assert abs(_F["mh439_cdar_ratio"](xs, 100.0, 12.0) - m438["pain_ratio"]) < 1e-9
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
        # CDaR ratio(k=1) = Calmar di tab431
        assert abs(_F["mh439_cdar_ratio"](xs, 1.0, 12.0) - c431["calmar"]) < 1e-9
        # confronto famiglia: CDaR ratio DEBOLE, Pain ratio OTTIMO,
        # Sterling BUONO, Martin BUONO, Kappa-3 BUONO, Sortino
        # BUONO, Omega BUONO, Burke DISCRETO, Calmar DEBOLE
        assert m["verdetto"].startswith("DEBOLE")
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
        assert abs(c427["var_dd"] - m["var_dd"]) < 1e-12
        p424 = _F["mh424_pain"](xs)
        assert abs(p424["pain"] - m["pain"]) < 1e-12
        assert abs(p424["max_dd"] - m["max_dd"]) < 1e-12
        u421 = _F["mh421_ulcer"](xs)
        assert abs(u421["max_dd"] - m["max_dd"]) < 1e-12

    def test_stesso_maxdd_media_cdar_ratio_diverso(self):
        a = tuple([25.0, -20.0, 25.0] + [0.0] * 17)
        b = tuple([25.0, -20.0] + [0.0] * 16 + [25.0, 0.0])
        ma = _F["mh439_mappa"](a, 10.0, 10.0)
        mb = _F["mh439_mappa"](b, 10.0, 10.0)
        assert abs(ma["max_dd"] - MAXDD_AB) < 1e-12
        assert abs(mb["max_dd"] - MAXDD_AB) < 1e-12
        assert abs(ma["mean"] - MEAN_AB) < 1e-12
        assert abs(mb["mean"] - MEAN_AB) < 1e-12
        assert abs(ma["ann"] - ANN_AB) < 1e-9
        assert abs(mb["ann"] - ANN_AB) < 1e-9
        assert abs(ma["cdar"] - CDAR_A) < 1e-12
        assert abs(mb["cdar"] - CDAR_B) < 1e-12
        assert abs(ma["cdar_ratio"] - CDARRATIO_A) < 1e-12
        assert abs(mb["cdar_ratio"] - CDARRATIO_B) < 1e-12
        assert abs(ma["cdar_ratio"] / mb["cdar_ratio"] - 2.0) < 1e-9
        assert _F["mh439_verdetto"](CDARRATIO_A).startswith("BUONO")
        assert _F["mh439_verdetto"](CDARRATIO_B).startswith("DISCRETO")
        # il Calmar vede le due serie IDENTICHE (e coincide col
        # CDaR ratio della B, dove la coda e' tutta al maxDD)
        ca = _F["mh431_mappa"](a, 10.0)
        cb = _F["mh431_mappa"](b, 10.0)
        assert abs(ca["calmar"] - cb["calmar"]) < 1e-12
        assert abs(ca["calmar"] - CALMAR_AB) < 1e-9
        assert abs(mb["cdar_ratio"] - cb["calmar"]) < 1e-12

    def test_sensibilita_annualizzazione_e_alpha(self):
        xs = self._xs()
        s1 = _F["mh439_cdar_ratio"](xs, 10.0, 1.0)
        s12 = _F["mh439_cdar_ratio"](xs, 10.0, 12.0)
        s52 = _F["mh439_cdar_ratio"](xs, 10.0, 52.0)
        assert abs(s1 - CDARRATIO_PPY1) < 1e-9
        assert abs(s12 - CDARRATIO10) < 1e-9
        assert abs(s52 - CDARRATIO_PPY52) < 1e-9
        assert s1 < s12 < s52
        assert _F["mh439_verdetto"](s1).startswith("DEBOLE")
        assert _F["mh439_verdetto"](s52).startswith("OTTIMO")
        # il CDaR NON dipende da ppy: cambia solo l'annualizzazione
        assert abs(_F["mh439_mappa"](xs, 10.0, 1.0)["cdar"] - CDAR10) < 1e-12
        assert abs(_F["mh439_mappa"](xs, 10.0, 52.0)["cdar"] - CDAR10) < 1e-12
        # ppy non intero AMMESSO (nessun blocco annuo): ratio =
        # ann(12.5) / CDaR(10%)
        s125 = _F["mh439_cdar_ratio"](xs, 10.0, 12.5)
        assert abs(s125 - _F["mh439_ann_return"](xs, 12.5) / CDAR10) < 1e-9
        # sensibilita' ad alpha a ppy 12: curva monotona crescente
        for alpha, atteso in ((5.0, CDARRATIO5), (20.0, CDARRATIO20),
                              (25.0, CDARRATIO25), (50.0, CDARRATIO50)):
            assert abs(_F["mh439_cdar_ratio"](xs, alpha, 12.0) - atteso) < 1e-9

    def test_verdetto_soglie(self):
        assert _F["mh439_verdetto"](-0.1).startswith("NEGATIVO")
        assert _F["mh439_verdetto"](0.0).startswith("DEBOLE")
        assert _F["mh439_verdetto"](0.499).startswith("DEBOLE")
        assert _F["mh439_verdetto"](0.5).startswith("DISCRETO")
        assert _F["mh439_verdetto"](0.999).startswith("DISCRETO")
        assert _F["mh439_verdetto"](1.0).startswith("BUONO")
        assert _F["mh439_verdetto"](1.999).startswith("BUONO")
        assert _F["mh439_verdetto"](2.0).startswith("OTTIMO")
        assert _F["mh439_verdetto"](3.999).startswith("OTTIMO")
        assert _F["mh439_verdetto"](4.0).startswith("ECCEZIONALE")
        assert _F["mh439_verdetto"](float("inf")).startswith("ECCEZIONALE")
        assert _F["mh439_verdetto"](float("-inf")).startswith("NEGATIVO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh439_mappa"](flat, 10.0, 12.0)
        assert mf["cdar"] == 0.0
        assert mf["ann"] == 0.0
        assert mf["cdar_ratio"] == 0.0
        assert mf["verdetto"].startswith("DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh439_mappa"](gains, 10.0, 12.0)
        assert mg["cdar"] == 0.0
        assert mg["ann"] > 0.0
        assert mg["cdar_ratio"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        for bad in (lambda: _F["mh439_mappa"]((1.0,) * 19, 10.0, 12.0),
                    lambda: _F["mh439_mappa"](None, 10.0, 12.0),
                    lambda: _F["mh439_mappa"](tuple([0.0] * 19 + [-100.0]), 10.0, 12.0),
                    lambda: _F["mh439_cdar_ratio"](self._xs(), 10.0, 0.0),
                    lambda: _F["mh439_cdar_ratio"](self._xs(), 10.0, -12.0),
                    lambda: _F["mh439_cdar_ratio"](self._xs(), 0.0, 12.0),
                    lambda: _F["mh439_cdar_ratio"](self._xs(), 101.0, 12.0),
                    lambda: _F["mh439_cdar_ratio"](self._xs(), -5.0, 12.0),
                    lambda: _F["mh439_cdar"](self._xs(), 0.0),
                    lambda: _F["mh439_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh439_verdetto"](float("nan"))):
            with pytest.raises(ValueError):
                bad()

    def test_in_coda(self):
        xs = self._xs()
        m = _F["mh439_mappa"](xs, 10.0, 12.0)
        dds = list(m["dds"])
        in_coda = m["in_coda"]
        assert sum(in_coda) == m["k"]
        # ogni drawdown in coda >= ogni drawdown fuori coda
        dentro = [dds[i] for i in range(len(dds)) if in_coda[i]]
        fuori = [dds[i] for i in range(len(dds)) if not in_coda[i]]
        assert min(dentro) >= max(fuori)
        assert abs(min(dentro) - m["var_dd"]) < 1e-12

    def test_parse_serie(self):
        xs = _F["mh439_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh439_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh439_parse_serie"]("1\n2\n")

