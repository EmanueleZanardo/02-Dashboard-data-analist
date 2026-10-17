"""Test tab441 '📈 Recovery Factor: profitto totale per unita' di peggior drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh441_num", "mh441_parse_serie", "mh441_equity",
           "mh441_drawdowns", "mh441_max_dd", "mh441_total_return",
           "mh441_ann_return", "mh441_geo_ann",
           "mh441_recovery_factor", "mh441_curva_orizzonte",
           "mh441_verdetto", "mh441_mappa",
           "mh440_num", "mh440_parse_serie", "mh440_equity",
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

TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
ANN = 17.342816782940005
TOTAL = 54.48235233549858
GEOANN = 15.600476608582682
DRAG = 1.7423401743573237
RF = 1.2339676011047631
RF_NODRAG = 1.3945694874852799
CALMAR = 0.3927964396665778
DAR10 = 27.773759999999996
CDAR10 = 35.875782277214554
CDARRATIO = 0.48341292320627066
PAINRATIO = 3.6939097218027177
STERLING = 1.1783893189997336
MARTIN = 1.385902649301104
KAPPA = 1.389386420473165
BURKE = 0.23098377488351735
OMEGA = 1.8734177215189876
SORTINO = 1.2829179004131461
RF_E = 11.899732626005598
RF_F = 0.9437895839134206
TOTAL_E = 237.99465252011186
TOTAL_F = 18.875791678268406
MAXDD_EF = 19.999999999999993
RF_P = 2.22115935465228
RF_Q = 3.8062236400861083
TOTAL_P = 44.4231870930456
TOTAL_Q = 76.12447280172216
CALMAR_PQ = 1.3412089728127274
RF_CRASH10 = 11.845362240706962
RF_CRASH20 = 4.709049884758642
RF_CRASH30 = 2.330279099442542
RF_H0 = 1.2339676011047631
RF_H6 = 1.912929755680561
RF_H12 = 2.7236460756080705
RF_H24 = 4.847571378531569


class TestRegistry441:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 510
        assert "tab441" in dvars
        assert "tab441" in withs

    def test_titoli_allineati_432_433_434_435_436_437_438_439_440_441(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab432")] == TITLE432
        assert titoli[dvars.index("tab433")] == TITLE433
        assert titoli[dvars.index("tab434")] == TITLE434
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441

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


class TestRecoveryFactor441:
    def _xs(self):
        return _F["mh441_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh441_mappa"](xs, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["total"] - TOTAL) < 1e-9
        assert abs(m["geo_ann"] - GEOANN) < 1e-9
        assert abs(m["drag"] - DRAG) < 1e-9
        assert abs(m["rf"] - RF) < 1e-9
        assert abs(m["rf_nodrag"] - RF_NODRAG) < 1e-9
        assert abs(m["calmar"] - CALMAR) < 1e-9
        assert m["verdetto"].startswith("DISCRETO")
        # demo: totale 54.4824%, maxDD 44.1522%, RF 1.2340
        assert m["ppy"] == 12.0
        assert m["n"] == 36
        assert m["n_dd"] == 6
        # sotto <=> drawdown > 0
        assert sum(m["sotto"]) == m["n_dd"] == 6
        assert len(m["sotto"]) == 36
        # RF = totale / maxDD; drag = ann - geo; RF < RF_nodrag
        assert abs(m["rf"] - m["total"] / m["max_dd"]) < 1e-12
        assert abs(m["drag"] - (m["ann"] - m["geo_ann"])) < 1e-12
        assert m["rf"] < m["rf_nodrag"]

    def test_identita_rf(self):
        xs = self._xs()
        m = _F["mh441_mappa"](xs, 12.0)
        # RF a mano: equity composta -> totale -> totale/maxDD
        eq = 100.0
        pk = 100.0
        dds = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            pk = max(pk, eq)
            dds.append((pk - eq) / pk * 100.0)
        tot = (eq / 100.0 - 1.0) * 100.0
        assert abs(tot - m["total"]) < 1e-9
        assert abs(max(dds) - m["max_dd"]) < 1e-12
        assert abs(tot / max(dds) - m["rf"]) < 1e-12
        assert abs(_F["mh441_total_return"](xs) - tot) < 1e-12
        assert abs(_F["mh441_recovery_factor"](xs) - m["rf"]) < 1e-12
        # CAGR geometrico a mano: (eq/100)^(ppy/n) - 1
        geo = ((eq / 100.0) ** (12.0 / 36.0) - 1.0) * 100.0
        assert abs(geo - m["geo_ann"]) < 1e-9
        assert abs(_F["mh441_geo_ann"](xs, 12.0) - geo) < 1e-12
        # ann mean-based a mano + Calmar = ann/maxDD (tab431)
        mean = sum(xs) / len(xs)
        ann = ((1.0 + mean / 100.0) ** 12.0 - 1.0) * 100.0
        assert abs(ann - m["ann"]) < 1e-9
        assert abs(ann / max(dds) - m["calmar"]) < 1e-12
        assert abs(_F["mh431_calmar"](xs, 12.0) - m["calmar"]) < 1e-12
        # RF senza drag a mano: ((1+ann/100)^(n/ppy)-1)*100/maxDD
        rf_nd = (((1.0 + ann / 100.0) ** (36.0 / 12.0) - 1.0) * 100.0) / max(dds)
        assert abs(rf_nd - m["rf_nodrag"]) < 1e-9
        assert m["rf_nodrag"] - m["rf"] > 0.15
        # drag positivo: la media sovrastima il composto
        assert m["drag"] > 1.7

    def test_crosscheck_440_439_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh441_mappa"](xs, 12.0)
        m440 = _F["mh440_mappa"](xs, 10.0, 12.0)
        assert abs(m440["dar"] - DAR10) < 1e-9
        assert abs(m440["cdar"] - CDAR10) < 1e-9
        assert abs(m440["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m440["mean"] - m["mean"]) < 1e-12
        assert abs(m440["pain"] - m["pain"]) < 1e-12
        assert abs(m440["ann"] - m["ann"]) < 1e-12
        m439 = _F["mh439_mappa"](xs, 10.0, 12.0)
        assert abs(m439["cdar_ratio"] - CDARRATIO) < 1e-9
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
        # confronto famiglia: RF DISCRETO, Calmar DEBOLE,
        # CDaR ratio DEBOLE, Burke DISCRETO, DaR DISCRETO,
        # Sterling BUONO, Sortino BUONO, Martin BUONO,
        # Kappa-3 BUONO, Omega BUONO, Pain ratio OTTIMO
        assert m["verdetto"].startswith("DISCRETO")
        assert _F["mh431_verdetto"](CALMAR).startswith("DEBOLE")
        assert _F["mh439_verdetto"](CDARRATIO).startswith("DEBOLE")
        assert _F["mh434_verdetto"](BURKE).startswith("DISCRETO")
        assert _F["mh440_verdetto"](DAR10).startswith("DISCRETO")
        assert _F["mh437_verdetto"](STERLING).startswith("BUONO")
        assert _F["mh432_verdetto"](SORTINO).startswith("BUONO")
        assert _F["mh436_verdetto"](MARTIN).startswith("BUONO")
        assert _F["mh435_verdetto"](KAPPA).startswith("BUONO")
        assert _F["mh433_verdetto"](OMEGA).startswith("BUONO")
        assert _F["mh438_verdetto"](PAINRATIO).startswith("OTTIMO")
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
        assert abs(c427["cdar"] - CDAR10) < 1e-12
        assert abs(c427["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(c427["var_dd"] - DAR10) < 1e-12
        p424 = _F["mh424_pain"](xs)
        assert abs(p424["pain"] - m["pain"]) < 1e-12
        assert abs(p424["max_dd"] - m["max_dd"]) < 1e-12
        u421 = _F["mh421_ulcer"](xs)
        assert abs(u421["max_dd"] - m["max_dd"]) < 1e-12

    def test_stesso_maxdd_rf_diverso(self):
        e = tuple([10.0] * 10 + [-20.0] + [5.0] * 10)
        f = tuple([2.0] * 10 + [-20.0] + [2.0] * 10)
        me = _F["mh441_mappa"](e, 12.0)
        mf = _F["mh441_mappa"](f, 12.0)
        # STESSO maxDD = 20.0 su entrambe
        assert abs(me["max_dd"] - MAXDD_EF) < 1e-12
        assert abs(mf["max_dd"] - MAXDD_EF) < 1e-12
        # RF DIVERSO: E 11.8997 (OTTIMO) vs F 0.9438 (DEBOLE)
        assert abs(me["total"] - TOTAL_E) < 1e-9
        assert abs(mf["total"] - TOTAL_F) < 1e-9
        assert abs(me["rf"] - RF_E) < 1e-9
        assert abs(mf["rf"] - RF_F) < 1e-9
        assert abs(me["rf"] / mf["rf"] - 12.6085) < 1e-3
        assert _F["mh441_verdetto"](RF_E).startswith("OTTIMO")
        assert _F["mh441_verdetto"](RF_F).startswith("DEBOLE")
        # il maxDD da solo non dice quanto hai guadagnato
        assert me["total"] > mf["total"]
        assert me["rf"] > mf["rf"]

    def test_stesso_calmar_rf_diverso(self):
        p = tuple([60.0 / 19.0] * 19 + [-20.0])
        q = tuple([80.0 / 29.0] * 29 + [-20.0])
        mp = _F["mh441_mappa"](p, 12.0)
        mq = _F["mh441_mappa"](q, 12.0)
        # STESSA media, STESSO ann, STESSO maxDD, STESSO Calmar
        assert abs(mp["mean"] - mq["mean"]) < 1e-9
        assert abs(mp["ann"] - mq["ann"]) < 1e-9
        assert abs(mp["max_dd"] - mq["max_dd"]) < 1e-9
        assert abs(mp["calmar"] - CALMAR_PQ) < 1e-9
        assert abs(mq["calmar"] - CALMAR_PQ) < 1e-9
        assert abs(mp["calmar"] - mq["calmar"]) < 1e-9
        # RF DIVERSO: P 2.2212 (BUONO) vs Q 3.8062 (BUONO)
        assert abs(mp["total"] - TOTAL_P) < 1e-9
        assert abs(mq["total"] - TOTAL_Q) < 1e-9
        assert abs(mp["rf"] - RF_P) < 1e-9
        assert abs(mq["rf"] - RF_Q) < 1e-9
        assert abs(mq["rf"] / mp["rf"] - 1.7136) < 1e-3
        assert _F["mh441_verdetto"](RF_P).startswith("BUONO")
        assert _F["mh441_verdetto"](RF_Q).startswith("BUONO")
        # il Calmar e' cieco all'orizzonte, l'RF no
        assert mq["n"] == 30 and mp["n"] == 20
        assert mq["total"] > mp["total"]

    def test_ppy_orizzonte_crash(self):
        xs = self._xs()
        # l'RF NON dipende da ppy: stessa soglia a ppy 1/12/52
        assert abs(_F["mh441_mappa"](xs, 1.0)["rf"] - RF) < 1e-12
        assert abs(_F["mh441_mappa"](xs, 52.0)["rf"] - RF) < 1e-12
        assert abs(_F["mh441_mappa"](xs, 1.0)["total"] - TOTAL) < 1e-12
        # ppy non intero AMMESSO: rf invariato, ann = ann(12.5)
        m125 = _F["mh441_mappa"](xs, 12.5)
        assert abs(m125["rf"] - RF) < 1e-12
        assert abs(m125["ann"] - _F["mh441_ann_return"](xs, 12.5)) < 1e-9
        # orizzonte: append +3% -> RF CRESCENTE a maxDD fisso
        curva = _F["mh441_curva_orizzonte"](xs, (0, 6, 12, 24), 3.0)
        rfs = [c["rf"] for c in curva]
        assert rfs == sorted(rfs)
        assert abs(rfs[0] - RF_H0) < 1e-9
        assert abs(rfs[1] - RF_H6) < 1e-9
        assert abs(rfs[2] - RF_H12) < 1e-9
        assert abs(rfs[3] - RF_H24) < 1e-9
        assert all(abs(c["max_dd"] - MAXDD) < 1e-9 for c in curva)
        assert [c["extra"] for c in curva] == [0, 6, 12, 24]
        assert [c["n"] for c in curva] == [36, 42, 48, 60]
        assert _F["mh441_verdetto"](RF_H0).startswith("DISCRETO")
        assert _F["mh441_verdetto"](RF_H12).startswith("BUONO")
        assert _F["mh441_verdetto"](RF_H24).startswith("OTTIMO")
        # crash: stesso schema, crash -10/-20/-30 -> RF decrescente
        for crash, atteso in ((-10.0, RF_CRASH10), (-20.0, RF_CRASH20),
                              (-30.0, RF_CRASH30)):
            s = tuple([3.0] * 20 + [crash] + [3.0] * 10)
            assert abs(_F["mh441_recovery_factor"](s) - atteso) < 1e-9
        assert RF_CRASH10 > RF_CRASH20 > RF_CRASH30
        assert _F["mh441_verdetto"](RF_CRASH10).startswith("OTTIMO")
        assert _F["mh441_verdetto"](RF_CRASH20).startswith("OTTIMO")
        assert _F["mh441_verdetto"](RF_CRASH30).startswith("BUONO")

    def test_verdetto_soglie(self):
        assert _F["mh441_verdetto"](-1.0).startswith("NEGATIVO")
        assert _F["mh441_verdetto"](-0.001).startswith("NEGATIVO")
        assert _F["mh441_verdetto"](0.0).startswith("MOLTO DEBOLE")
        assert _F["mh441_verdetto"](0.4999).startswith("MOLTO DEBOLE")
        assert _F["mh441_verdetto"](0.5).startswith("DEBOLE")
        assert _F["mh441_verdetto"](0.9999).startswith("DEBOLE")
        assert _F["mh441_verdetto"](1.0).startswith("DISCRETO")
        assert _F["mh441_verdetto"](1.9999).startswith("DISCRETO")
        assert _F["mh441_verdetto"](2.0).startswith("BUONO")
        assert _F["mh441_verdetto"](3.9999).startswith("BUONO")
        assert _F["mh441_verdetto"](4.0).startswith("OTTIMO")
        assert _F["mh441_verdetto"](100.0).startswith("OTTIMO")
        assert _F["mh441_verdetto"](float("inf")).startswith("OTTIMO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh441_mappa"](flat, 12.0)
        assert mf["total"] == 0.0
        assert mf["max_dd"] == 0.0
        assert mf["rf"] == 0.0
        assert mf["verdetto"].startswith("MOLTO DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh441_mappa"](gains, 12.0)
        assert mg["max_dd"] == 0.0
        assert mg["total"] > 0.0
        assert mg["rf"] == float("inf")
        assert mg["verdetto"].startswith("OTTIMO")
        neg = tuple([-1.0] * 36)
        mn = _F["mh441_mappa"](neg, 12.0)
        assert mn["total"] < 0.0
        assert mn["rf"] < 0.0
        assert abs(mn["rf"] + 1.0) < 1e-9
        assert mn["verdetto"].startswith("NEGATIVO")
        for bad in (lambda: _F["mh441_mappa"]((1.0,) * 19, 12.0),
                    lambda: _F["mh441_mappa"](None, 12.0),
                    lambda: _F["mh441_mappa"](tuple([0.0] * 19 + [-100.0]), 12.0),
                    lambda: _F["mh441_mappa"](self._xs(), 0.0),
                    lambda: _F["mh441_mappa"](self._xs(), -12.0),
                    lambda: _F["mh441_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh441_geo_ann"](self._xs(), 0.0),
                    lambda: _F["mh441_total_return"](tuple([0.0] * 19 + [-100.0])),
                    lambda: _F["mh441_curva_orizzonte"](self._xs(), (-1,), 3.0),
                    lambda: _F["mh441_verdetto"](float("nan")),
                    lambda: _F["mh441_verdetto"](float("-inf")),
                    lambda: _F["mh441_verdetto"]("1.2")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh441_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh441_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh441_parse_serie"]("1\n2\n")

