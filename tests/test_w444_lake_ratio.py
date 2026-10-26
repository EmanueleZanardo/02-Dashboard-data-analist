"""Test tab444 '🏞️ Lake ratio: l'area del dolore sotto il picco': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh444_num", "mh444_parse_serie", "mh444_equity",
           "mh444_peaks", "mh444_drawdowns", "mh444_max_dd",
           "mh444_lake", "mh444_curva_orizzonte",
           "mh444_verdetto", "mh444_mappa",
           "mh443_num", "mh443_parse_serie", "mh443_equity",
           "mh443_drawdowns", "mh443_max_dd",
           "mh443_gains", "mh443_losses",
           "mh443_gain_to_pain", "mh443_curva_orizzonte",
           "mh443_verdetto", "mh443_mappa",
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
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
TOTAL = 54.48235233549858
LAKE = 6.713752987003486
TUW = 16.666666666666664
SUMDD = 169.01912910885824
SUMPEAK = 6963.748912751244
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
GPR = 1.8734177215189873
LAKE_A = 3.3494314159781364
LAKE_B = 12.240274616099414
MAXDD_A = 20.000000000000004
MAXDD_B = 19.999999999999993
LAKE_C = 7.56920734133618
LAKE_D2 = 2.495854838766142
TUW_C = 50.0
TUW_D2 = 50.0
LAKE_CRASH10 = 0.8666454694754492
LAKE_CRASH20 = 3.3494314159781364
LAKE_CRASH30 = 7.728911044398091
LAKE_H0 = 6.713752987003486
LAKE_H6 = 12.732456997425546
LAKE_H12 = 14.866077533596538
LAKE_H24 = 12.60270263124173
LAKE_H30 = 10.933119549335455
LAKE_H36 = 9.439866093795462


class TestRegistry444:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 729
        assert "tab444" in dvars
        assert "tab444" in withs

    def test_titoli_allineati_435_436_437_438_439_440_441_442_443_444(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444

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


class TestLakeRatio444:
    def _xs(self):
        return _F["mh444_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh444_mappa"](xs)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["total"] - TOTAL) < 1e-9
        assert abs(m["lake"] - LAKE) < 1e-9
        assert abs(m["tuw"] - TUW) < 1e-9
        assert abs(m["sum_dd"] - SUMDD) < 1e-9
        assert abs(m["sum_peak"] - SUMPEAK) < 1e-9
        assert m["verdetto"].startswith("DISCRETO")
        # demo: Lake 6.7138%, TUW 16.6667% (6 periodi su 36)
        assert m["n"] == 36
        assert m["n_dd"] == 6
        assert sum(m["sotto"]) == m["n_dd"] == 6
        assert len(m["sotto"]) == 36
        assert len(m["equity"]) == 36
        assert len(m["peaks"]) == 36
        assert len(m["dds"]) == 36
        assert len(m["deficit"]) == 36
        # deficit = picco - equity, >= 0; sotto <=> deficit > 0
        for p, e, d, s in zip(m["peaks"], m["equity"],
                              m["deficit"], m["sotto"]):
            assert abs(d - (p - e)) < 1e-9
            assert d >= 0.0
            assert s == (d > 0.0)
        # picchi monotoni non decrescenti, tutti >= 100 (picco iniziale)
        assert all(p >= 100.0 for p in m["peaks"])
        assert list(m["peaks"]) == sorted(m["peaks"])
        # Lake > Pain: i picchi crescono, i DD tardi pesano di piu'
        assert m["lake"] > m["pain"]

    def test_identita_lake_pain_pesata(self):
        xs = self._xs()
        m = _F["mh444_mappa"](xs)
        # Lake a mano: somma deficit / somma picchi * 100
        eq = 100.0
        pk = 100.0
        dds = []
        peaks = []
        eqs = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            pk = max(pk, eq)
            peaks.append(pk)
            eqs.append(eq)
            dds.append((pk - eq) / pk * 100.0)
        lake_mano = (sum(p - e for p, e in zip(peaks, eqs))
                     / sum(peaks) * 100.0)
        assert abs(lake_mano - m["lake"]) < 1e-12
        assert abs(_F["mh444_lake"](xs) - m["lake"]) < 1e-12
        # identita': Lake = media dei DD PESATA sui picchi
        lake_pesato = (sum(d * p / 100.0 for d, p in zip(dds, peaks))
                       / sum(peaks) * 100.0)
        assert abs(lake_pesato - m["lake"]) < 1e-12
        # Pain = media SEMPLICE dei DD (tab424): Lake != Pain
        pain_semplice = sum(dds) / len(dds)
        assert abs(pain_semplice - m["pain"]) < 1e-12
        assert abs(_F["mh424_pain"](xs)["pain"] - m["pain"]) < 1e-12
        # maxDD/Pain/total da equity composta (coerenza famiglia)
        assert abs(max(dds) - m["max_dd"]) < 1e-12
        assert abs((eq / 100.0 - 1.0) * 100.0 - m["total"]) < 1e-9
        # TUW a mano: quota periodi con DD > 0
        assert abs(sum(1 for d in dds if d > 0.0) / len(dds) * 100.0
                   - m["tuw"]) < 1e-12

    def test_crosscheck_443_442_441_440_439_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh444_mappa"](xs)
        m443 = _F["mh443_mappa"](xs)
        assert abs(m443["gpr"] - GPR) < 1e-9
        assert abs(m443["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m443["mean"] - m["mean"]) < 1e-12
        assert abs(m443["pain"] - m["pain"]) < 1e-12
        assert abs(m443["total"] - m["total"]) < 1e-12
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
        # RF DISCRETO, GPR DISCRETO, Lake DISCRETO, Sterling
        # BUONO, Sortino BUONO, Martin BUONO, Kappa-3 BUONO,
        # Omega BUONO, Pain ratio OTTIMO
        assert m["verdetto"].startswith("DISCRETO")
        assert _F["mh442_verdetto"](GEOCALMAR).startswith("DEBOLE")
        assert _F["mh431_verdetto"](CALMAR).startswith("DEBOLE")
        assert _F["mh439_verdetto"](CDARRATIO).startswith("DEBOLE")
        assert _F["mh434_verdetto"](BURKE).startswith("DISCRETO")
        assert _F["mh440_verdetto"](DAR10).startswith("DISCRETO")
        assert _F["mh441_verdetto"](RF).startswith("DISCRETO")
        assert _F["mh443_verdetto"](GPR).startswith("DISCRETO")
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

    def test_stesso_maxdd_lago_diverso(self):
        a = tuple([3.0] * 20 + [-20.0] + [3.0] * 10)
        b = tuple([3.0] * 10 + [-20.0] + [0.0] * 20 + [3.0] * 10)
        ma = _F["mh444_mappa"](a)
        mb = _F["mh444_mappa"](b)
        # STESSO maxDD = 20.0 su entrambe
        assert abs(ma["max_dd"] - MAXDD_A) < 1e-12
        assert abs(mb["max_dd"] - MAXDD_B) < 1e-12
        assert abs(ma["max_dd"] - mb["max_dd"]) < 1e-12
        # LAGO DIVERSO: A 3.3494 BUONO vs B 12.2403 DEBOLE (3.65x)
        assert abs(ma["lake"] - LAKE_A) < 1e-9
        assert abs(mb["lake"] - LAKE_B) < 1e-9
        assert mb["lake"] / ma["lake"] > 3.5
        assert _F["mh444_verdetto"](LAKE_A).startswith("BUONO")
        assert _F["mh444_verdetto"](LAKE_B).startswith("DEBOLE")
        # B resta sott'acqua molto piu' a lungo (20 periodi piatti)
        assert mb["tuw"] > ma["tuw"]
        assert mb["pain"] > ma["pain"]

    def test_stesso_tuw_lago_diverso(self):
        c = tuple([3.0] * 10 + [-20.0] + [0.0] * 5 + [3.0] * 10)
        d2 = tuple([3.0] * 10 + [-5.0] + [0.0] * 11 + [3.0] * 4)
        mc = _F["mh444_mappa"](c)
        md2 = _F["mh444_mappa"](d2)
        # STESSO TUW 50.0% (13 periodi sott'acqua su 26)
        assert abs(mc["tuw"] - TUW_C) < 1e-9
        assert abs(md2["tuw"] - TUW_D2) < 1e-9
        assert abs(mc["tuw"] - md2["tuw"]) < 1e-12
        # LAGO DIVERSO: C 7.5692 DISCRETO vs D2 2.4959 OTTIMO
        assert abs(mc["lake"] - LAKE_C) < 1e-9
        assert abs(md2["lake"] - LAKE_D2) < 1e-9
        assert mc["lake"] / md2["lake"] > 3.0
        assert _F["mh444_verdetto"](LAKE_C).startswith("DISCRETO")
        assert _F["mh444_verdetto"](LAKE_D2).startswith("OTTIMO")
        # il TUW conta i periodi, il Lake pesa la profondita'
        assert abs(mc["max_dd"] - 20.0) < 1e-9
        assert abs(md2["max_dd"] - 5.0) < 1e-9

    def test_orizzonte_crash_ppy(self):
        xs = self._xs()
        # il Lake NON dipende da ppy (non annualizza): in mappa
        # non c'e' ppy. E NON e' monotono in orizzonte: cresce
        # finche' l'equity resta sott'acqua, cala dopo il recupero
        curva = _F["mh444_curva_orizzonte"](xs, (0, 6, 12, 24), 3.0)
        lakes = [c["lake"] for c in curva]
        assert abs(lakes[0] - LAKE_H0) < 1e-9
        assert abs(lakes[1] - LAKE_H6) < 1e-9
        assert abs(lakes[2] - LAKE_H12) < 1e-9
        assert abs(lakes[3] - LAKE_H24) < 1e-9
        assert [c["extra"] for c in curva] == [0, 6, 12, 24]
        assert [c["n"] for c in curva] == [36, 42, 48, 60]
        # gobba: cresce fino a extra 12, poi cala
        assert lakes[1] > lakes[0]
        assert lakes[2] > lakes[1]
        assert lakes[3] < lakes[2]
        assert _F["mh444_verdetto"](lakes[0]).startswith("DISCRETO")
        assert _F["mh444_verdetto"](lakes[1]).startswith("DEBOLE")
        assert _F["mh444_verdetto"](lakes[2]).startswith("DEBOLE")
        assert _F["mh444_verdetto"](lakes[3]).startswith("DEBOLE")
        # oltre extra 24 il lago continua a calare (recupero completo)
        assert abs(_F["mh444_lake"](xs + tuple([3.0] * 30))
                   - LAKE_H30) < 1e-9
        assert abs(_F["mh444_lake"](xs + tuple([3.0] * 36))
                   - LAKE_H36) < 1e-9
        assert LAKE_H30 < LAKE_H24
        assert LAKE_H36 < LAKE_H30
        assert _F["mh444_verdetto"](LAKE_H36).startswith("DISCRETO")
        # crash: stesso schema, crash -10/-20/-30 -> Lake crescente
        # e convesso (3x il crash -> ~8.9x il lago)
        for crash, atteso in ((-10.0, LAKE_CRASH10),
                              (-20.0, LAKE_CRASH20),
                              (-30.0, LAKE_CRASH30)):
            s = tuple([3.0] * 20 + [crash] + [3.0] * 10)
            assert abs(_F["mh444_lake"](s) - atteso) < 1e-9
        assert LAKE_CRASH10 < LAKE_CRASH20 < LAKE_CRASH30
        assert LAKE_CRASH30 / LAKE_CRASH10 > 8.0
        assert _F["mh444_verdetto"](LAKE_CRASH10).startswith("ECCEZIONALE")
        assert _F["mh444_verdetto"](LAKE_CRASH20).startswith("BUONO")
        assert _F["mh444_verdetto"](LAKE_CRASH30).startswith("DISCRETO")

    def test_verdetto_soglie(self):
        assert _F["mh444_verdetto"](0.0).startswith("ECCEZIONALE")
        assert _F["mh444_verdetto"](0.9999).startswith("ECCEZIONALE")
        assert _F["mh444_verdetto"](1.0).startswith("OTTIMO")
        assert _F["mh444_verdetto"](2.9999).startswith("OTTIMO")
        assert _F["mh444_verdetto"](3.0).startswith("BUONO")
        assert _F["mh444_verdetto"](5.9999).startswith("BUONO")
        assert _F["mh444_verdetto"](6.0).startswith("DISCRETO")
        assert _F["mh444_verdetto"](9.9999).startswith("DISCRETO")
        assert _F["mh444_verdetto"](10.0).startswith("DEBOLE")
        assert _F["mh444_verdetto"](14.9999).startswith("DEBOLE")
        assert _F["mh444_verdetto"](15.0).startswith("NEGATIVO")
        assert _F["mh444_verdetto"](100.0).startswith("NEGATIVO")
        assert _F["mh444_verdetto"](float("inf")).startswith("NEGATIVO")
        assert _F["mh444_verdetto"](float("-inf")).startswith("ECCEZIONALE")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh444_mappa"](flat)
        assert mf["lake"] == 0.0
        assert mf["max_dd"] == 0.0
        assert mf["tuw"] == 0.0
        assert mf["verdetto"].startswith("ECCEZIONALE")
        gains = tuple([1.0] * 25)
        mg = _F["mh444_mappa"](gains)
        assert mg["lake"] == 0.0
        assert mg["max_dd"] == 0.0
        assert mg["verdetto"].startswith("ECCEZIONALE")
        neg = tuple([-1.0] * 36)
        mn = _F["mh444_mappa"](neg)
        assert mn["lake"] > 15.0
        assert mn["tuw"] == 100.0
        assert mn["verdetto"].startswith("NEGATIVO")
        for bad in (lambda: _F["mh444_mappa"]((1.0,) * 19),
                    lambda: _F["mh444_mappa"](None),
                    lambda: _F["mh444_mappa"](tuple([0.0] * 19 + [-100.0])),
                    lambda: _F["mh444_lake"]((1.0,) * 19),
                    lambda: _F["mh444_lake"](None),
                    lambda: _F["mh444_lake"](tuple([0.0] * 19 + [-100.0])),
                    lambda: _F["mh444_curva_orizzonte"](self._xs(), (-1,), 3.0),
                    lambda: _F["mh444_verdetto"](float("nan")),
                    lambda: _F["mh444_verdetto"]("1.2")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh444_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh444_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh444_parse_serie"]("1\n2\n")

