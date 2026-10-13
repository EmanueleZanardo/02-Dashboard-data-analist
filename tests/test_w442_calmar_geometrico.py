"""Test tab442 '📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh442_num", "mh442_parse_serie", "mh442_equity",
           "mh442_drawdowns", "mh442_max_dd", "mh442_total_return",
           "mh442_ann_return", "mh442_geo_ann",
           "mh442_geo_calmar", "mh442_curva_orizzonte",
           "mh442_verdetto", "mh442_mappa",
           "mh441_num", "mh441_parse_serie", "mh441_equity",
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

TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MAXDD = 44.15217408197824
MEAN = 1.3416666666666666
PAIN = 4.694975808579396
ANN = 17.342816782940005
TOTAL = 54.48235233549858
GEOANN = 15.600476608582682
DRAG = 1.7423401743573237
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
GEOCALMAR_E = 5.027766033243799
GEOCALMAR_F = 0.519255909564649
TOTAL_E = 237.99465252011186
TOTAL_F = 18.875791678268406
MAXDD_EF = 19.999999999999993
GEOCALMAR_P = 1.2337898734724217
GEOCALMAR_Q = 1.2704381262412834
TOTAL_P = 44.4231870930456
TOTAL_Q = 76.12447280172216
CALMAR_PQ = 1.3412089728127274
RF_P = 2.22115935465228
RF_Q = 3.8062236400861083
GEOCALMAR_CRASH10 = 3.5320898018824503
GEOCALMAR_CRASH20 = 1.4644845093157097
GEOCALMAR_CRASH30 = 0.7592180840556749
GEOCALMAR_H0 = 0.35333427929544214
GEOCALMAR_H6 = 0.43296935281604715
GEOCALMAR_H12 = 0.49428120352444954
GEOCALMAR_H24 = 0.5824657383692183
GEOCALMAR_PPY1 = 0.027527732416137336
GEOCALMAR_PPY52 = 1.9800594602267219


class TestRegistry442:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 442
        assert "tab442" in dvars
        assert "tab442" in withs

    def test_titoli_allineati_433_434_435_436_437_438_439_440_441_442(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab433")] == TITLE433
        assert titoli[dvars.index("tab434")] == TITLE434
        assert titoli[dvars.index("tab435")] == TITLE435
        assert titoli[dvars.index("tab436")] == TITLE436
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab442"
        assert titoli[-1] == TITLE442
        assert withs[-1] == "tab442"


class TestGeoCalmar442:
    def _xs(self):
        return _F["mh442_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh442_mappa"](xs, 12.0)
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAIN) < 1e-12
        assert abs(m["ann"] - ANN) < 1e-9
        assert abs(m["total"] - TOTAL) < 1e-9
        assert abs(m["geo_ann"] - GEOANN) < 1e-9
        assert abs(m["drag"] - DRAG) < 1e-9
        assert abs(m["geo_calmar"] - GEOCALMAR) < 1e-9
        assert abs(m["calmar"] - CALMAR) < 1e-9
        assert abs(m["rf"] - RF) < 1e-9
        assert m["verdetto"].startswith("DEBOLE")
        # demo: CAGR 15.6005%, maxDD 44.1522%, GeoCalmar 0.3533
        assert m["ppy"] == 12.0
        assert m["n"] == 36
        assert m["n_dd"] == 6
        # sotto <=> drawdown > 0
        assert sum(m["sotto"]) == m["n_dd"] == 6
        assert len(m["sotto"]) == 36
        # GeoCalmar = CAGR / maxDD; Calmar - GeoCalmar = drag / maxDD
        assert abs(m["geo_calmar"] - m["geo_ann"] / m["max_dd"]) < 1e-12
        assert abs(m["drag"] - (m["ann"] - m["geo_ann"])) < 1e-12
        assert abs((m["calmar"] - m["geo_calmar"])
                   - m["drag"] / m["max_dd"]) < 1e-12
        assert m["geo_calmar"] < m["calmar"]
        # identita' ponte: RF = ((1+CAGR/100)^(n/ppy)-1)*100/maxDD
        rf_ponte = ((((1.0 + m["geo_ann"] / 100.0) ** (36.0 / 12.0)
                      - 1.0) * 100.0) / m["max_dd"])
        assert abs(rf_ponte - m["rf"]) < 1e-9

    def test_identita_geocalmar(self):
        xs = self._xs()
        m = _F["mh442_mappa"](xs, 12.0)
        # GeoCalmar a mano: equity composta -> totale/CAGR -> CAGR/maxDD
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
        assert abs(_F["mh442_total_return"](xs) - tot) < 1e-12
        # CAGR geometrico a mano: (eq/100)^(ppy/n) - 1
        geo = ((eq / 100.0) ** (12.0 / 36.0) - 1.0) * 100.0
        assert abs(geo - m["geo_ann"]) < 1e-9
        assert abs(_F["mh442_geo_ann"](xs, 12.0) - geo) < 1e-12
        assert abs(_F["mh442_geo_calmar"](xs, 12.0)
                   - geo / max(dds)) < 1e-12
        assert abs(_F["mh442_geo_calmar"](xs, 12.0)
                   - m["geo_calmar"]) < 1e-12
        # ann mean-based a mano + Calmar = ann/maxDD (tab431)
        mean = sum(xs) / len(xs)
        ann = ((1.0 + mean / 100.0) ** 12.0 - 1.0) * 100.0
        assert abs(ann - m["ann"]) < 1e-9
        assert abs(ann / max(dds) - m["calmar"]) < 1e-12
        assert abs(_F["mh431_calmar"](xs, 12.0) - m["calmar"]) < 1e-12
        # drag positivo: la media sovrastima il composto
        assert m["drag"] > 1.7
        assert m["geo_ann"] < m["ann"]

    def test_crosscheck_441_440_439_438_437_436_435_434_433_432_431_430_429_427_424_421(self):
        xs = self._xs()
        m = _F["mh442_mappa"](xs, 12.0)
        m441 = _F["mh441_mappa"](xs, 12.0)
        assert abs(m441["rf"] - RF) < 1e-9
        assert abs(m441["geo_ann"] - m["geo_ann"]) < 1e-12
        assert abs(m441["calmar"] - m["calmar"]) < 1e-12
        assert abs(m441["max_dd"] - m["max_dd"]) < 1e-12
        assert abs(m441["mean"] - m["mean"]) < 1e-12
        assert abs(m441["pain"] - m["pain"]) < 1e-12
        assert abs(m441["ann"] - m["ann"]) < 1e-12
        assert abs(m441["total"] - m["total"]) < 1e-12
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
        # confronto famiglia: GeoCalmar DEBOLE, Calmar DEBOLE,
        # CDaR ratio DEBOLE, Burke DISCRETO, DaR DISCRETO,
        # RF DISCRETO, Sterling BUONO, Sortino BUONO,
        # Martin BUONO, Kappa-3 BUONO, Omega BUONO,
        # Pain ratio OTTIMO
        assert m["verdetto"].startswith("DEBOLE")
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

    def test_stesso_maxdd_geocalmar_diverso(self):
        e = tuple([10.0] * 10 + [-20.0] + [5.0] * 10)
        f = tuple([2.0] * 10 + [-20.0] + [2.0] * 10)
        me = _F["mh442_mappa"](e, 12.0)
        mf = _F["mh442_mappa"](f, 12.0)
        # STESSO maxDD = 20.0 su entrambe
        assert abs(me["max_dd"] - MAXDD_EF) < 1e-12
        assert abs(mf["max_dd"] - MAXDD_EF) < 1e-12
        # GEOCALMAR DIVERSO: E 5.0278 (ECCEZIONALE) vs F 0.5193 (DISCRETO)
        assert abs(me["total"] - TOTAL_E) < 1e-9
        assert abs(mf["total"] - TOTAL_F) < 1e-9
        assert abs(me["geo_calmar"] - GEOCALMAR_E) < 1e-9
        assert abs(mf["geo_calmar"] - GEOCALMAR_F) < 1e-9
        assert abs(me["geo_calmar"] / mf["geo_calmar"] - 9.6826) < 1e-3
        assert _F["mh442_verdetto"](GEOCALMAR_E).startswith("ECCEZIONALE")
        assert _F["mh442_verdetto"](GEOCALMAR_F).startswith("DISCRETO")
        # il maxDD da solo non dice quanto rendimento composto hai incassato
        assert me["total"] > mf["total"]
        assert me["geo_calmar"] > mf["geo_calmar"]

    def test_stesso_calmar_geocalmar_quasi_uguale(self):
        p = tuple([60.0 / 19.0] * 19 + [-20.0])
        q = tuple([80.0 / 29.0] * 29 + [-20.0])
        mp = _F["mh442_mappa"](p, 12.0)
        mq = _F["mh442_mappa"](q, 12.0)
        # STESSA media, STESSO ann, STESSO maxDD, STESSO Calmar
        assert abs(mp["mean"] - mq["mean"]) < 1e-9
        assert abs(mp["ann"] - mq["ann"]) < 1e-9
        assert abs(mp["max_dd"] - mq["max_dd"]) < 1e-9
        assert abs(mp["calmar"] - CALMAR_PQ) < 1e-9
        assert abs(mq["calmar"] - CALMAR_PQ) < 1e-9
        assert abs(mp["calmar"] - mq["calmar"]) < 1e-9
        # GEOCALMAR QUASI UGUALE: P 1.2338 vs Q 1.2704 (+2.97%)
        assert abs(mp["total"] - TOTAL_P) < 1e-9
        assert abs(mq["total"] - TOTAL_Q) < 1e-9
        assert abs(mp["geo_calmar"] - GEOCALMAR_P) < 1e-9
        assert abs(mq["geo_calmar"] - GEOCALMAR_Q) < 1e-9
        assert abs(mq["geo_calmar"] / mp["geo_calmar"] - 1.0297) < 1e-3
        assert _F["mh442_verdetto"](GEOCALMAR_P).startswith("BUONO")
        assert _F["mh442_verdetto"](GEOCALMAR_Q).startswith("BUONO")
        # ...mentre l'RF differisce del 71%: GeoCalmar e Calmar sono
        # ciechi all'orizzonte, l'RF no
        assert abs(mp["rf"] - RF_P) < 1e-9
        assert abs(mq["rf"] - RF_Q) < 1e-9
        assert abs(mq["rf"] / mp["rf"] - 1.7136) < 1e-3
        assert mq["n"] == 30 and mp["n"] == 20
        assert mq["total"] > mp["total"]

    def test_ppy_orizzonte_crash(self):
        xs = self._xs()
        # il GeoCalmar DIPENDE da ppy (e' annualizzato): ppy 1/12/52
        assert abs(_F["mh442_mappa"](xs, 1.0)["geo_calmar"]
                   - GEOCALMAR_PPY1) < 1e-9
        assert abs(_F["mh442_mappa"](xs, 52.0)["geo_calmar"]
                   - GEOCALMAR_PPY52) < 1e-9
        assert abs(_F["mh442_mappa"](xs, 1.0)["total"] - TOTAL) < 1e-12
        # ppy non intero AMMESSO: geo_calmar = geo_ann(12.5)/maxDD
        m125 = _F["mh442_mappa"](xs, 12.5)
        assert abs(m125["geo_calmar"]
                   - _F["mh442_geo_ann"](xs, 12.5) / m125["max_dd"]) < 1e-9
        # orizzonte: append +3% -> GeoCalmar CRESCENTE LENTO a maxDD
        # fisso, mentre l'RF cresce VELOCE (confronto con tab441)
        curva = _F["mh442_curva_orizzonte"](xs, (0, 6, 12, 24), 3.0, 12.0)
        gcs = [c["geo_calmar"] for c in curva]
        assert gcs == sorted(gcs)
        assert abs(gcs[0] - GEOCALMAR_H0) < 1e-9
        assert abs(gcs[1] - GEOCALMAR_H6) < 1e-9
        assert abs(gcs[2] - GEOCALMAR_H12) < 1e-9
        assert abs(gcs[3] - GEOCALMAR_H24) < 1e-9
        assert all(abs(c["max_dd"] - MAXDD) < 1e-9 for c in curva)
        assert [c["extra"] for c in curva] == [0, 6, 12, 24]
        assert [c["n"] for c in curva] == [36, 42, 48, 60]
        assert _F["mh442_verdetto"](gcs[0]).startswith("DEBOLE")
        assert _F["mh442_verdetto"](gcs[1]).startswith("DEBOLE")
        assert _F["mh442_verdetto"](gcs[2]).startswith("DEBOLE")
        assert _F["mh442_verdetto"](gcs[3]).startswith("DISCRETO")
        # RF dalla curva tab441: cresce VELOCE (1.2340 -> 4.8476)
        curva_rf = _F["mh441_curva_orizzonte"](xs, (0, 6, 12, 24), 3.0)
        rfs = [c["rf"] for c in curva_rf]
        assert rfs == sorted(rfs)
        assert abs(rfs[0] - RF) < 1e-9
        assert rfs[3] / rfs[0] > 3.9
        assert gcs[3] / gcs[0] < 1.7
        assert [c["rf"] for c in curva] == rfs
        # crash: stesso schema, crash -10/-20/-30 -> GeoCalmar decrescente
        for crash, atteso in ((-10.0, GEOCALMAR_CRASH10),
                              (-20.0, GEOCALMAR_CRASH20),
                              (-30.0, GEOCALMAR_CRASH30)):
            s = tuple([3.0] * 20 + [crash] + [3.0] * 10)
            assert abs(_F["mh442_geo_calmar"](s, 12.0) - atteso) < 1e-9
        assert GEOCALMAR_CRASH10 > GEOCALMAR_CRASH20 > GEOCALMAR_CRASH30
        assert _F["mh442_verdetto"](GEOCALMAR_CRASH10).startswith("ECCEZIONALE")
        assert _F["mh442_verdetto"](GEOCALMAR_CRASH20).startswith("BUONO")
        assert _F["mh442_verdetto"](GEOCALMAR_CRASH30).startswith("DISCRETO")
        # il gap Calmar - GeoCalmar CRESCE col crash (il drag sale)
        gaps = []
        for crash in (-10.0, -20.0, -30.0):
            s = tuple([3.0] * 20 + [crash] + [3.0] * 10)
            gaps.append(_F["mh431_calmar"](s, 12.0)
                        - _F["mh442_geo_calmar"](s, 12.0))
        assert gaps[0] < gaps[1] < gaps[2]
        assert all(g > 0.0 for g in gaps)

    def test_verdetto_soglie(self):
        assert _F["mh442_verdetto"](-1.0).startswith("NEGATIVO")
        assert _F["mh442_verdetto"](-0.001).startswith("NEGATIVO")
        assert _F["mh442_verdetto"](0.0).startswith("DEBOLE")
        assert _F["mh442_verdetto"](0.4999).startswith("DEBOLE")
        assert _F["mh442_verdetto"](0.5).startswith("DISCRETO")
        assert _F["mh442_verdetto"](0.9999).startswith("DISCRETO")
        assert _F["mh442_verdetto"](1.0).startswith("BUONO")
        assert _F["mh442_verdetto"](1.9999).startswith("BUONO")
        assert _F["mh442_verdetto"](2.0).startswith("OTTIMO")
        assert _F["mh442_verdetto"](2.9999).startswith("OTTIMO")
        assert _F["mh442_verdetto"](3.0).startswith("ECCEZIONALE")
        assert _F["mh442_verdetto"](100.0).startswith("ECCEZIONALE")
        assert _F["mh442_verdetto"](float("inf")).startswith("ECCEZIONALE")
        assert _F["mh442_verdetto"](float("-inf")).startswith("NEGATIVO")

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        mf = _F["mh442_mappa"](flat, 12.0)
        assert mf["total"] == 0.0
        assert mf["geo_ann"] == 0.0
        assert mf["max_dd"] == 0.0
        assert mf["geo_calmar"] == 0.0
        assert mf["verdetto"].startswith("DEBOLE")
        gains = tuple([1.0] * 25)
        mg = _F["mh442_mappa"](gains, 12.0)
        assert mg["max_dd"] == 0.0
        assert mg["total"] > 0.0
        assert mg["geo_calmar"] == float("inf")
        assert mg["verdetto"].startswith("ECCEZIONALE")
        neg = tuple([-1.0] * 36)
        mn = _F["mh442_mappa"](neg, 12.0)
        assert mn["total"] < 0.0
        assert mn["geo_ann"] < 0.0
        assert mn["geo_calmar"] < 0.0
        assert abs(mn["geo_calmar"]
                   - mn["geo_ann"] / mn["max_dd"]) < 1e-12
        assert mn["verdetto"].startswith("NEGATIVO")
        for bad in (lambda: _F["mh442_mappa"]((1.0,) * 19, 12.0),
                    lambda: _F["mh442_mappa"](None, 12.0),
                    lambda: _F["mh442_mappa"](tuple([0.0] * 19 + [-100.0]), 12.0),
                    lambda: _F["mh442_mappa"](self._xs(), 0.0),
                    lambda: _F["mh442_mappa"](self._xs(), -12.0),
                    lambda: _F["mh442_ann_return"](self._xs(), 0.0),
                    lambda: _F["mh442_geo_ann"](self._xs(), 0.0),
                    lambda: _F["mh442_total_return"](tuple([0.0] * 19 + [-100.0])),
                    lambda: _F["mh442_curva_orizzonte"](self._xs(), (-1,), 3.0, 12.0),
                    lambda: _F["mh442_verdetto"](float("nan")),
                    lambda: _F["mh442_verdetto"]("1.2")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh442_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh442_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh442_parse_serie"]("1\n2\n")

