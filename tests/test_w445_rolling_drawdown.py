"""Test tab445 '🌀 Rolling drawdown: il peggior calo in ogni finestra': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh445_num", "mh445_parse_serie", "mh445_equity",
           "mh445_peaks", "mh445_drawdowns", "mh445_max_dd",
           "mh445_window_dds", "mh445_window_max_dd",
           "mh445_rolling", "mh445_worst_window",
           "mh445_curva_w", "mh445_verdetto", "mh445_mappa",
           "mh444_num", "mh444_parse_serie", "mh444_equity",
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
           "mh424_num", "mh424_equity", "mh424_drawdowns",
           "mh424_pain",
           "mh421_num", "mh421_equity", "mh421_drawdowns",
           "mh421_ulcer", "mh421_martin")

TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
TOTAL = 54.48235233549858
TUW = 16.666666666666664
LAKE = 6.713752987003486
WORST = 44.15217408197823
BEST = 0.0
MEDIAN = 0.0
MEANWIN = 6.760765164354329
SHAREOVER = 16.0
WSTART = 25
WEND = 36
WPEAK = 30
WTROUGH = 36
WORST_W3 = 27.77376000000001
WORST_W6 = 44.15217408197824
WORST_W18 = 44.15217408197824
WORST_W24 = 44.15217408197823
NW_12 = 25
NW_3 = 34
NW_6 = 31
NW_18 = 19
NW_24 = 13
SHARE_W3 = 11.76470588235294
SHARE_W6 = 12.903225806451612
SHARE_W18 = 21.052631578947366
SHARE_W24 = 30.76923076923077
SPREAD_X = 2.870687760113566
SPREAD_MAXDD = 44.152174081978266
SPREAD_WORST = 29.49762247892646
SPREAD_WORST_W3 = 8.36720352406941
SPREAD_WORST_W6 = 16.034306100006816
SPREAD_WORST_W18 = 40.80218949843779
SPREAD_WORST_W24 = 44.15217408197826
LOSSES_WORST = 11.361512828387077
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


class TestRegistry445:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 592
        assert "tab445" in dvars
        assert "tab445" in withs

    def test_titoli_allineati_436_437_438_439_440_441_442_443_444_445(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445

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


class TestRolling445:
    def _xs(self):
        return _F["mh445_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh445_mappa"](xs)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["total"] - TOTAL) < 1e-9
        assert abs(m["tuw"] - TUW) < 1e-9
        assert abs(m["worst"] - WORST) < 1e-9
        assert abs(m["best"] - BEST) < 1e-12
        assert abs(m["median"] - MEDIAN) < 1e-12
        assert abs(m["mean_win"] - MEANWIN) < 1e-9
        assert abs(m["share_over"] - SHAREOVER) < 1e-9
        assert m["worst_start"] == WSTART
        assert m["worst_end"] == WEND
        assert m["worst_peak"] == WPEAK
        assert m["worst_trough"] == WTROUGH
        assert m["w"] == 12
        assert m["n"] == 36
        assert m["n_win"] == NW_12
        assert m["verdetto"].startswith("NEGATIVO")
        # demo: worst 44.1522% = maxDD totale (il crollo 30->36 sta
        # in una finestra da 12); 19 finestre su 25 a 0.0
        assert m["worst"] <= m["max_dd"] + 1e-12
        assert abs(m["worst"] - m["max_dd"]) < 1e-9
        assert len(m["windows"]) == 25
        assert len(m["equity"]) == 36
        assert len(m["peaks"]) == 36
        assert len(m["dds"]) == 36
        # finestre: start 1..25, end = start + 11
        for i, d in enumerate(m["windows"]):
            assert d["start"] == i + 1
            assert d["end"] == i + 12
            assert d["max_dd"] >= 0.0
        assert m["windows"][0]["max_dd"] == 0.0
        assert m["windows"][18]["max_dd"] == 0.0
        assert abs(m["windows"][19]["max_dd"] - 9.5) < 1e-9
        assert abs(m["windows"][24]["max_dd"] - WORST) < 1e-9
        # worst window = ultima (start 25)
        assert m["windows"][24]["start"] == WSTART
        # picchi monotoni non decrescenti, tutti >= 100
        assert all(p >= 100.0 for p in m["peaks"])
        assert list(m["peaks"]) == sorted(m["peaks"])

    def test_identita_rolling(self):
        xs = self._xs()
        m = _F["mh445_mappa"](xs)
        # equity / picchi / drawdown a mano (percorso globale)
        eq = 100.0
        pk = 100.0
        dds = []
        eqs = []
        pks = []
        for x in xs:
            eq *= 1.0 + x / 100.0
            pk = max(pk, eq)
            pks.append(pk)
            eqs.append(eq)
            dds.append((pk - eq) / pk * 100.0)
        assert abs(max(dds) - m["max_dd"]) < 1e-12
        assert abs(sum(dds) / len(dds) - m["pain"]) < 1e-12
        assert abs((eq / 100.0 - 1.0) * 100.0 - m["total"]) < 1e-9
        assert abs(sum(1 for d in dds if d > 0.0) / len(dds) * 100.0
                   - m["tuw"]) < 1e-12
        # rolling a mano W=12: equity di finestra da 100, picco
        # resettato; un maxDD per finestra
        mano = []
        for s in range(1, 36 - 12 + 2):
            feq = 100.0
            fpk = 100.0
            fmax = 0.0
            for x in xs[s - 1:s - 1 + 12]:
                feq *= 1.0 + x / 100.0
                fpk = max(fpk, feq)
                fmax = max(fmax, (fpk - feq) / fpk * 100.0)
            mano.append(fmax)
        wins = _F["mh445_rolling"](xs, 12)
        assert len(wins) == 25
        for d, atteso in zip(wins, mano):
            assert abs(d["max_dd"] - atteso) < 1e-12
        assert abs(max(mano) - m["worst"]) < 1e-12
        assert abs(min(mano) - m["best"]) < 1e-12
        assert abs(sorted(mano)[12] - m["median"]) < 1e-12
        assert abs(sum(mano) / len(mano) - m["mean_win"]) < 1e-12
        assert abs(sum(1 for v in mano if v > 20.0) / len(mano) * 100.0
                   - m["share_over"]) < 1e-12
        # finestra singola a mano: la peggiore (start 25)
        wdds = _F["mh445_window_dds"](xs, 25, 12)
        assert len(wdds) == 12
        assert abs(max(wdds) - m["worst"]) < 1e-12
        assert abs(_F["mh445_window_max_dd"](xs, 25, 12)
                   - m["worst"]) < 1e-12
        # finestra peggiore a mano: picco/minimo interni
        ww = _F["mh445_worst_window"](xs, 12)
        assert ww["start"] == WSTART
        assert ww["end"] == WEND
        assert abs(ww["max_dd"] - WORST) < 1e-12
        assert ww["peak_period"] == WPEAK
        assert ww["trough_period"] == WTROUGH
        # finestra che cade da subito: picco = punto pre-finestra
        ww3 = _F["mh445_worst_window"](xs, 3)
        assert ww3["start"] == 31
        assert ww3["end"] == 33
        assert abs(ww3["max_dd"] - WORST_W3) < 1e-9
        assert ww3["peak_period"] == 30
        assert ww3["trough_period"] == 33

    def test_crosscheck_444_443_442_441_440_439_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh445_mappa"](xs)
        m444 = _F["mh444_mappa"](xs)
        assert abs(m444["lake"] - LAKE) < 1e-9
        assert abs(m444["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m444["mean"] - m["mean"]) < 1e-12
        assert abs(m444["pain"] - m["pain"]) < 1e-12
        assert abs(m444["total"] - m["total"]) < 1e-12
        assert abs(m444["tuw"] - m["tuw"]) < 1e-12
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
        # confronto famiglia: worst rolling NEGATIVO, Lake
        # DISCRETO, GeoCalmar DEBOLE, Calmar DEBOLE, CDaR
        # ratio DEBOLE, Burke DISCRETO, DaR DISCRETO, RF
        # DISCRETO, GPR DISCRETO, Sterling BUONO, Sortino
        # BUONO, Martin BUONO, Kappa-3 BUONO, Omega BUONO,
        # Pain ratio OTTIMO
        assert m["verdetto"].startswith("NEGATIVO")
        assert _F["mh444_verdetto"](LAKE).startswith("DISCRETO")
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

    def test_monotonia_w(self):
        xs = self._xs()
        curva = _F["mh445_curva_w"](xs, (3, 6, 12, 18, 24))
        worsts = [c["worst"] for c in curva]
        assert [c["w"] for c in curva] == [3, 6, 12, 18, 24]
        assert [c["n_win"] for c in curva] == [NW_3, NW_6, NW_12,
                                               NW_18, NW_24]
        assert abs(worsts[0] - WORST_W3) < 1e-9
        assert abs(worsts[1] - WORST_W6) < 1e-9
        assert abs(worsts[2] - WORST) < 1e-9
        assert abs(worsts[3] - WORST_W18) < 1e-9
        assert abs(worsts[4] - WORST_W24) < 1e-9
        # NON DECRESCENTE in W (finestra piu' larga contiene la
        # piu' stretta che parte dallo stesso punto)
        for a, b in zip(worsts, worsts[1:]):
            assert b >= a - 1e-12
        # SATURAZIONE al maxDD totale: gia' a W=6 il crollo
        # (6 periodi) sta interamente in finestra
        assert abs(worsts[1] - MAXDD) < 1e-9
        assert abs(worsts[4] - MAXDD) < 1e-9
        # share oltre 20% NON DECRESCENTE in W
        shares = [c["share_over"] for c in curva]
        assert abs(shares[0] - SHARE_W3) < 1e-9
        assert abs(shares[1] - SHARE_W6) < 1e-9
        assert abs(shares[2] - SHAREOVER) < 1e-9
        assert abs(shares[3] - SHARE_W18) < 1e-9
        assert abs(shares[4] - SHARE_W24) < 1e-9
        for a, b in zip(shares, shares[1:]):
            assert b >= a - 1e-12
        assert _F["mh445_verdetto"](worsts[0]).startswith("DISCRETO")
        assert _F["mh445_verdetto"](worsts[1]).startswith("NEGATIVO")

    def test_stesso_maxdd_profilo_diverso(self):
        xs = self._xs()
        m = _F["mh445_mappa"](xs)
        # SPREAD: 10 x +3% poi 20 cadute da -SPREAD_X, costruite
        # per avere ESATTAMENTE lo stesso maxDD totale della demo
        spread = tuple([3.0] * 10 + [-SPREAD_X] * 20)
        assert len(spread) == 30
        ms = _F["mh445_mappa"](spread)
        assert abs(ms["max_dd"] - SPREAD_MAXDD) < 1e-9
        assert abs(ms["max_dd"] - m["max_dd"]) < 1e-9
        # STESSO maxDD totale, worst rolling MOLTO diverso:
        # la demo concentra il crollo in 6 periodi (una finestra
        # da 12 lo contiene tutto), la spread lo spalma su 20
        assert abs(ms["worst"] - SPREAD_WORST) < 1e-9
        assert ms["worst"] < m["worst"] - 10.0
        assert _F["mh445_verdetto"](ms["worst"]).startswith("DISCRETO")
        assert _F["mh445_verdetto"](m["worst"]).startswith("NEGATIVO")
        # curva W della spread: STRETTAMENTE crescente fino a
        # W=24 (il calo dura 20 periodi, nessuna finestra da
        # 3/6/12/18 lo contiene tutto)
        curva = _F["mh445_curva_w"](spread, (3, 6, 12, 18, 24))
        worsts = [c["worst"] for c in curva]
        assert abs(worsts[0] - SPREAD_WORST_W3) < 1e-9
        assert abs(worsts[1] - SPREAD_WORST_W6) < 1e-9
        assert abs(worsts[2] - SPREAD_WORST) < 1e-9
        assert abs(worsts[3] - SPREAD_WORST_W18) < 1e-9
        assert abs(worsts[4] - SPREAD_WORST_W24) < 1e-9
        for a, b in zip(worsts, worsts[1:]):
            assert b > a + 1e-9
        assert abs(worsts[4] - SPREAD_MAXDD) < 1e-9

    def test_verdetto_soglie(self):
        assert _F["mh445_verdetto"](0.0).startswith("ECCEZIONALE")
        assert _F["mh445_verdetto"](4.9999).startswith("ECCEZIONALE")
        assert _F["mh445_verdetto"](5.0).startswith("OTTIMO")
        assert _F["mh445_verdetto"](9.9999).startswith("OTTIMO")
        assert _F["mh445_verdetto"](10.0).startswith("BUONO")
        assert _F["mh445_verdetto"](19.9999).startswith("BUONO")
        assert _F["mh445_verdetto"](20.0).startswith("DISCRETO")
        assert _F["mh445_verdetto"](29.9999).startswith("DISCRETO")
        assert _F["mh445_verdetto"](30.0).startswith("DEBOLE")
        assert _F["mh445_verdetto"](39.9999).startswith("DEBOLE")
        assert _F["mh445_verdetto"](40.0).startswith("NEGATIVO")
        assert _F["mh445_verdetto"](100.0).startswith("NEGATIVO")
        assert _F["mh445_verdetto"](float("inf")).startswith("NEGATIVO")
        assert _F["mh445_verdetto"](float("-inf")).startswith("ECCEZIONALE")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh445_mappa"](flat)
        assert mf["worst"] == 0.0
        assert mf["best"] == 0.0
        assert mf["median"] == 0.0
        assert mf["share_over"] == 0.0
        assert mf["verdetto"].startswith("ECCEZIONALE")
        gains = tuple([1.0] * 25)
        mg = _F["mh445_mappa"](gains)
        assert mg["worst"] == 0.0
        assert mg["max_dd"] == 0.0
        assert mg["verdetto"].startswith("ECCEZIONALE")
        neg = tuple([-1.0] * 36)
        mn = _F["mh445_mappa"](neg)
        assert abs(mn["worst"] - LOSSES_WORST) < 1e-9
        assert abs(mn["median"] - LOSSES_WORST) < 1e-9
        assert mn["share_over"] == 0.0
        assert mn["verdetto"].startswith("BUONO")
        xs = self._xs()
        for bad in (lambda: _F["mh445_mappa"]((1.0,) * 19),
                    lambda: _F["mh445_mappa"](None),
                    lambda: _F["mh445_mappa"](
                        tuple([0.0] * 19 + [-100.0])),
                    lambda: _F["mh445_mappa"](xs, 1),
                    lambda: _F["mh445_mappa"](xs, 0),
                    lambda: _F["mh445_mappa"](xs, 37),
                    lambda: _F["mh445_mappa"](xs, "12"),
                    lambda: _F["mh445_rolling"](xs, 1),
                    lambda: _F["mh445_rolling"](xs, 37),
                    lambda: _F["mh445_rolling"](None, 12),
                    lambda: _F["mh445_window_dds"](xs, 0, 12),
                    lambda: _F["mh445_window_dds"](xs, 26, 12),
                    lambda: _F["mh445_window_dds"](xs, 1, 1),
                    lambda: _F["mh445_window_dds"](xs, 1, 37),
                    lambda: _F["mh445_worst_window"](xs, 1),
                    lambda: _F["mh445_worst_window"](xs, 37),
                    lambda: _F["mh445_curva_w"](xs, ()),
                    lambda: _F["mh445_curva_w"](xs, (37,)),
                    lambda: _F["mh445_curva_w"](xs, (1,)),
                    lambda: _F["mh445_verdetto"](float("nan")),
                    lambda: _F["mh445_verdetto"]("1.2")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh445_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh445_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh445_parse_serie"]("1\n2\n")

