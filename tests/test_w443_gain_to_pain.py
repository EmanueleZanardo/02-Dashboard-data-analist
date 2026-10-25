"""Test tab443 '💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh443_num", "mh443_parse_serie", "mh443_equity",
           "mh443_drawdowns", "mh443_max_dd", "mh443_gains",
           "mh443_losses", "mh443_gain_to_pain",
           "mh443_curva_orizzonte", "mh443_verdetto", "mh443_mappa",
           "mh442_num", "mh442_parse_serie", "mh442_equity",
           "mh442_drawdowns", "mh442_max_dd",
           "mh442_total_return", "mh442_ann_return",
           "mh442_geo_ann", "mh442_geo_calmar",
           "mh442_curva_orizzonte", "mh442_verdetto",
           "mh442_mappa",
           "mh441_num", "mh441_parse_serie", "mh441_equity",
           "mh441_drawdowns", "mh441_max_dd",
           "mh441_total_return", "mh441_ann_return",
           "mh441_geo_ann", "mh441_recovery_factor",
           "mh441_curva_orizzonte", "mh441_verdetto",
           "mh441_mappa",
           "mh440_num", "mh440_parse_serie", "mh440_equity",
           "mh440_drawdowns", "mh440_max_dd",
           "mh440_ann_return", "mh440_dar",
           "mh440_curva", "mh440_verdetto", "mh440_mappa",
           "mh439_num", "mh439_parse_serie", "mh439_equity",
           "mh439_drawdowns", "mh439_max_dd",
           "mh439_ann_return", "mh439_cdar",
           "mh439_cdar_ratio", "mh439_curva",
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
           "mh435_drawdowns", "mh435_max_dd",
           "mh435_ann_return", "mh435_lpm", "mh435_kappa",
           "mh435_verdetto", "mh435_mappa",
           "mh434_num", "mh434_parse_serie", "mh434_equity",
           "mh434_drawdowns", "mh434_max_dd",
           "mh434_ann_return", "mh434_burke",
           "mh434_verdetto", "mh434_mappa",
           "mh433_num", "mh433_parse_serie", "mh433_equity",
           "mh433_drawdowns", "mh433_max_dd",
           "mh433_upside_potential",
           "mh433_downside_potential", "mh433_omega",
           "mh433_verdetto", "mh433_mappa",
           "mh432_num", "mh432_parse_serie", "mh432_equity",
           "mh432_drawdowns", "mh432_max_dd",
           "mh432_ann_return", "mh432_downside_dev",
           "mh432_sortino", "mh432_verdetto", "mh432_mappa",
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

TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
TOTAL = 54.48235233549858
GAINS = 103.6
LOSSES = 55.3
GPR = 1.8734177215189873
WINRATE = 83.33333333333334
AVGWIN = 3.453333333333333
AVGLOSS = -9.216666666666667
PAYOFF = 0.37468354430379747
GEOCALMAR = 0.35333427929544214
CALMAR = 0.3927964396665778
RF = 1.2339676011047631
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
GPR_E = 10.0
GPR_F = 10.0
MAXDD_E = 19.999999999999993
MAXDD_F = 4.000000000000001
GPR_P = 3.0
GPR_Q = 0.3333333333333333
GPR_CRASH10 = 9.0
GPR_CRASH20 = 4.5
GPR_CRASH30 = 3.0
GPR_H0 = 1.8734177215189873
GPR_H6 = 2.1989150090415914
GPR_H12 = 2.5244122965641953
GPR_H24 = 3.1754068716094035


class TestRegistry443:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 696
        assert "tab443" in dvars
        assert "tab443" in withs

    def test_titoli_allineati_434_435_436_437_438_439_440_441_442_443(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab434")] == TITLE434
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443

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


class TestGainToPain443:
    def _xs(self):
        return _F["mh443_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh443_mappa"](xs)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["total"] - TOTAL) < 1e-9
        assert abs(m["gains"] - GAINS) < 1e-9
        assert abs(m["losses"] - LOSSES) < 1e-9
        assert abs(m["gpr"] - GPR) < 1e-9
        assert abs(m["win_rate"] - WINRATE) < 1e-9
        assert abs(m["avg_win"] - AVGWIN) < 1e-9
        assert abs(m["avg_loss"] - AVGLOSS) < 1e-9
        assert abs(m["payoff"] - PAYOFF) < 1e-9
        assert m["verdetto"].startswith("DISCRETO")
        # demo: guadagni 103.6, perdite 55.3, GPR 1.8734
        assert m["n"] == 36
        assert m["n_win"] == 30
        assert m["n_loss"] == 6
        assert m["n_dd"] == 6
        assert sum(m["sotto"]) == m["n_dd"] == 6
        assert len(m["sotto"]) == 36
        # GPR = gains / losses; payoff * odds = GPR
        assert abs(m["gpr"] - m["gains"] / m["losses"]) < 1e-12
        assert abs(m["payoff"] * (m["n_win"] / m["n_loss"])
                   - m["gpr"]) < 1e-12
        # GPR > 1 <=> somma semplice > 0 (guadagni sopra le perdite)
        assert m["gpr"] > 1.0
        assert sum(xs) > 0.0
        assert abs((m["gains"] - m["losses"]) - sum(xs)) < 1e-9
        # payoff < 1 ma GPR > 1: vince la frequenza (odds 5.0)
        assert m["payoff"] < 1.0
        assert m["n_win"] / m["n_loss"] == 5.0
        # cumulate finali = totali; monotone non decrescenti
        assert abs(m["cum_gains"][-1] - m["gains"]) < 1e-12
        assert abs(m["cum_losses"][-1] - m["losses"]) < 1e-12
        assert list(m["cum_gains"]) == sorted(m["cum_gains"])
        assert list(m["cum_losses"]) == sorted(m["cum_losses"])

    def test_identita_gpr_omega0(self):
        xs = self._xs()
        m = _F["mh443_mappa"](xs)
        # GPR a mano: somma positivi / |somma negativi|
        g = sum(v for v in xs if v > 0.0)
        l = abs(sum(v for v in xs if v < 0.0))
        assert abs(g - m["gains"]) < 1e-12
        assert abs(l - m["losses"]) < 1e-12
        assert abs(_F["mh443_gains"](xs) - g) < 1e-12
        assert abs(_F["mh443_losses"](xs) - l) < 1e-12
        assert abs(_F["mh443_gain_to_pain"](xs) - g / l) < 1e-12
        # ponte Omega: Omega a soglia 0 = GPR ESATTAMENTE
        assert abs(_F["mh433_omega"](xs, 0.0) - m["gpr"]) < 1e-12
        assert abs(_F["mh433_mappa"](xs, 0.0)["omega"] - m["gpr"]) < 1e-12
        # stesso numero 1.8734, verdetti diversi (scale diverse)
        assert _F["mh433_verdetto"](OMEGA).startswith("BUONO")
        assert _F["mh443_verdetto"](GPR).startswith("DISCRETO")
        # maxDD/Pain/total da equity composta (coerenza famiglia)
        eq = 100.0
        pk = 100.0
        dds = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            pk = max(pk, eq)
            dds.append((pk - eq) / pk * 100.0)
        assert abs(max(dds) - m["max_dd"]) < 1e-12
        assert abs(sum(dds) / len(dds) - m["pain"]) < 1e-12
        assert abs((eq / 100.0 - 1.0) * 100.0 - m["total"]) < 1e-9

    def test_crosscheck_442_441_440_439_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh443_mappa"](xs)
        m442 = _F["mh442_mappa"](xs, 12.0)
        assert abs(m442["geo_calmar"] - GEOCALMAR) < 1e-9
        assert abs(m442["calmar"] - CALMAR) < 1e-9
        assert abs(m442["rf"] - RF) < 1e-9
        assert abs(m442["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m442["mean"] - m["mean"]) < 1e-12
        assert abs(m442["pain"] - m["pain"]) < 1e-12
        assert abs(m442["total"] - m["total"]) < 1e-12
        m441 = _F["mh441_mappa"](xs, 12.0)
        assert abs(m441["rf"] - RF) < 1e-9
        assert abs(m441["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m441["mean"] - m["mean"]) < 1e-12
        assert abs(m441["pain"] - m["pain"]) < 1e-12
        assert abs(m441["total"] - m["total"]) < 1e-12
        m440 = _F["mh440_mappa"](xs, 10.0, 12.0)
        assert abs(m440["dar"] - DAR10) < 1e-9
        assert abs(m440["cdar"] - CDAR10) < 1e-9
        assert abs(m440["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m440["mean"] - m["mean"]) < 1e-12
        assert abs(m440["pain"] - m["pain"]) < 1e-12
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
        # confronto famiglia: GeoCalmar DEBOLE, Calmar DEBOLE,
        # CDaR ratio DEBOLE, Burke DISCRETO, DaR DISCRETO,
        # RF DISCRETO, GPR DISCRETO, Sterling BUONO, Sortino
        # BUONO, Martin BUONO, Kappa-3 BUONO, Omega BUONO,
        # Pain ratio OTTIMO
        assert m["verdetto"].startswith("DISCRETO")
        assert _F["mh442_verdetto"](GEOCALMAR).startswith("DEBOLE")
        assert _F["mh431_verdetto"](CALMAR).startswith("DEBOLE")
        assert _F["mh439_verdetto"](CDARRATIO).startswith("DEBOLE")
        assert _F["mh434_verdetto"](BURKE).startswith("DISCRETO")
        assert _F["mh440_verdetto"](DAR10).startswith("DISCRETO")
        assert _F["mh441_verdetto"](RF).startswith("DISCRETO")
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

    def test_stesso_gpr_percorso_diverso(self):
        e = tuple([10.0] * 10 + [-20.0] + [10.0] * 10)
        f = tuple([2.0] * 10 + [-4.0] + [2.0] * 10)
        me = _F["mh443_mappa"](e)
        mf = _F["mh443_mappa"](f)
        # STESSO GPR = 10.0 su entrambe
        assert abs(me["gpr"] - GPR_E) < 1e-12
        assert abs(mf["gpr"] - GPR_F) < 1e-12
        assert abs(me["gpr"] - mf["gpr"]) < 1e-12
        assert _F["mh443_verdetto"](GPR_E).startswith("ECCEZIONALE")
        # ...ma PERCORSO DIVERSO: maxDD 20.0 vs 4.0
        assert abs(me["max_dd"] - MAXDD_E) < 1e-12
        assert abs(mf["max_dd"] - MAXDD_F) < 1e-12
        assert me["max_dd"] > mf["max_dd"]
        # il GPR non vede il percorso: somma solo guadagni/perdite
        assert me["gains"] == 200.0 and mf["gains"] == 40.0
        assert me["losses"] == 20.0 and mf["losses"] == 4.0

    def test_stesso_winrate_gpr_opposto(self):
        p = tuple([6.0] * 10 + [-2.0] * 10)
        q = tuple([2.0] * 10 + [-6.0] * 10)
        mp = _F["mh443_mappa"](p)
        mq = _F["mh443_mappa"](q)
        # STESSO win rate 50% (10 vincenti su 20)
        assert mp["win_rate"] == 50.0 and mq["win_rate"] == 50.0
        assert mp["n_win"] == mq["n_win"] == 10
        # GPR OPPOSTO: P 3.0 (OTTIMO) vs Q 0.3333 (NEGATIVO)
        assert abs(mp["gpr"] - GPR_P) < 1e-9
        assert abs(mq["gpr"] - GPR_Q) < 1e-9
        assert _F["mh443_verdetto"](GPR_P).startswith("OTTIMO")
        assert _F["mh443_verdetto"](GPR_Q).startswith("NEGATIVO")
        # conta il payoff: P 3.0 vs Q 0.3333, odds identici (1.0)
        assert abs(mp["payoff"] - 3.0) < 1e-12
        assert abs(mq["payoff"] - (1.0 / 3.0)) < 1e-12
        assert mp["gpr"] > 1.0 > mq["gpr"]
        assert sum(p) > 0.0 > sum(q)

    def test_orizzonte_crash_ppy(self):
        xs = self._xs()
        # il GPR NON dipende da ppy (non annualizza): in mappa non
        # c'e' ppy, e append di +3% fa crescere il GPR LINEARE
        # a perdite fisse (55.3000)
        curva = _F["mh443_curva_orizzonte"](xs, (0, 6, 12, 24), 3.0)
        gprs = [c["gpr"] for c in curva]
        assert gprs == sorted(gprs)
        assert abs(gprs[0] - GPR_H0) < 1e-9
        assert abs(gprs[1] - GPR_H6) < 1e-9
        assert abs(gprs[2] - GPR_H12) < 1e-9
        assert abs(gprs[3] - GPR_H24) < 1e-9
        assert all(abs(c["losses"] - LOSSES) < 1e-9 for c in curva)
        assert [c["extra"] for c in curva] == [0, 6, 12, 24]
        assert [c["n"] for c in curva] == [36, 42, 48, 60]
        assert abs(curva[1]["gains"] - (GAINS + 18.0)) < 1e-9
        assert abs(curva[2]["gains"] - (GAINS + 36.0)) < 1e-9
        assert abs(curva[3]["gains"] - (GAINS + 72.0)) < 1e-9
        assert _F["mh443_verdetto"](gprs[0]).startswith("DISCRETO")
        assert _F["mh443_verdetto"](gprs[1]).startswith("BUONO")
        assert _F["mh443_verdetto"](gprs[2]).startswith("BUONO")
        assert _F["mh443_verdetto"](gprs[3]).startswith("OTTIMO")
        # crescita LINEARE: +0.3255 ogni 6 extra (18.0 / 55.3)
        assert abs((gprs[1] - gprs[0]) - 18.0 / LOSSES) < 1e-9
        assert abs((gprs[2] - gprs[1]) - 18.0 / LOSSES) < 1e-9
        assert abs((gprs[3] - gprs[2]) - 36.0 / LOSSES) < 1e-9
        # crash: stesso schema, crash -10/-20/-30 -> GPR = 90/|crash|
        for crash, atteso in ((-10.0, GPR_CRASH10),
                              (-20.0, GPR_CRASH20),
                              (-30.0, GPR_CRASH30)):
            s = tuple([3.0] * 20 + [crash] + [3.0] * 10)
            assert abs(_F["mh443_gain_to_pain"](s) - atteso) < 1e-9
        assert GPR_CRASH10 > GPR_CRASH20 > GPR_CRASH30
        assert _F["mh443_verdetto"](GPR_CRASH10).startswith("ECCEZIONALE")
        assert _F["mh443_verdetto"](GPR_CRASH20).startswith("OTTIMO")
        assert _F["mh443_verdetto"](GPR_CRASH30).startswith("OTTIMO")

    def test_verdetto_soglie(self):
        assert _F["mh443_verdetto"](0.0).startswith("NEGATIVO")
        assert _F["mh443_verdetto"](0.9999).startswith("NEGATIVO")
        assert _F["mh443_verdetto"](1.0).startswith("DEBOLE")
        assert _F["mh443_verdetto"](1.4999).startswith("DEBOLE")
        assert _F["mh443_verdetto"](1.5).startswith("DISCRETO")
        assert _F["mh443_verdetto"](1.9999).startswith("DISCRETO")
        assert _F["mh443_verdetto"](2.0).startswith("BUONO")
        assert _F["mh443_verdetto"](2.9999).startswith("BUONO")
        assert _F["mh443_verdetto"](3.0).startswith("OTTIMO")
        assert _F["mh443_verdetto"](4.9999).startswith("OTTIMO")
        assert _F["mh443_verdetto"](5.0).startswith("ECCEZIONALE")
        assert _F["mh443_verdetto"](100.0).startswith("ECCEZIONALE")
        assert _F["mh443_verdetto"](float("inf")).startswith("ECCEZIONALE")
        assert _F["mh443_verdetto"](float("-inf")).startswith("NEGATIVO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh443_mappa"](flat)
        assert mf["gains"] == 0.0
        assert mf["losses"] == 0.0
        assert mf["gpr"] == 0.0
        assert mf["verdetto"].startswith("NEGATIVO")
        gains = tuple([1.0] * 25)
        mg = _F["mh443_mappa"](gains)
        assert mg["losses"] == 0.0
        assert mg["gains"] == 25.0
        assert mg["gpr"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        neg = tuple([-1.0] * 36)
        mn = _F["mh443_mappa"](neg)
        assert mn["gains"] == 0.0
        assert mn["losses"] == 36.0
        assert mn["gpr"] == 0.0
        assert mn["verdetto"].startswith("NEGATIVO")
        # GPR < 1 <=> somma semplice < 0 (totale in perdita)
        assert sum(neg) < 0.0
        for bad in (lambda: _F["mh443_mappa"]((1.0,) * 19),
                    lambda: _F["mh443_mappa"](None),
                    lambda: _F["mh443_mappa"](tuple([0.0] * 19 + [-100.0])),
                    lambda: _F["mh443_gains"]((1.0,) * 19),
                    lambda: _F["mh443_losses"](None),
                    lambda: _F["mh443_gain_to_pain"]((1.0,) * 19),
                    lambda: _F["mh443_curva_orizzonte"](self._xs(), (-1,), 3.0),
                    lambda: _F["mh443_verdetto"](float("nan")),
                    lambda: _F["mh443_verdetto"]("1.2")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh443_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh443_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh443_parse_serie"]("1\n2\n")

