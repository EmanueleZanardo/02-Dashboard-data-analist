"""Test tab321 '🧪📉 Backtest VaR: il modello resiste al tempo?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del backtest VaR: validatori, VaR
rolling, breaches, Kupiec POF, CDF chi2, Christoffersen, semaforo Basilea,
verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh321_num", "mh321_conf", "mh321_finestra", "mh321_parse_pnl",
           "mh321_losses", "mh321_quantile", "mh321_var_rolling",
           "mh321_breaches", "mh321_chi2_1_cdf", "mh321_chi2_2_cdf",
           "mh321_loglik_bin", "mh321_kupiec", "mh321_christoffersen",
           "mh321_traffic", "mh321_risultato", "mh321_verdetto")

TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
SERIE_DEMO = '1120.60\n-1328.80\n222.66\n1077.26\n1326.91\n-235.24\n-112.33\n405.17\n1010.39\n628.04\n-876.22\n-2491.20\n-730.85\n-366.36\n1751.67\n-1144.96\n-64.62\n-473.75\n185.38\n439.76\n41.39\n-878.35\n-457.01\n970.49\n603.27\n-807.86\n-649.86\n-567.50\n-1225.23\n400.15\n-369.97\n1099.55\n-209.30\n1002.05\n2292.99\n1304.76\n624.58\n-602.96\n277.48\n-76.14\n-423.18\n-381.97\n-1481.86\n-1355.92\n1518.25\n-1064.52\n-2004.64\n-867.82\n174.98\n-63.68\n-280.78\n527.09\n-2133.01\n334.76\n-384.65\n928.07\n450.37\n-1712.21\n-192.43\n-287.76\n-1155.24\n-2477.41\n900.14\n-563.85\n-254.67\n690.50\n265.57\n765.78\n211.93\n-175.97\n653.14\n84.33\n-307.08\n782.31\n217.84\n-1627.70\n-149.20\n1287.72\n177.43\n508.55\n-691.95\n808.76\n-129.09\n828.76\n378.10\n633.51\n1.47\n-1104.60\n274.43\n-2169.68\n-636.22\n-124.35\n1616.34\n87.04\n350.44\n-10.68\n442.84\n141.62\n-207.47\n-1170.82\n-336.36\n-228.11\n357.66\n-867.66\n-546.80\n641.89\n-1219.47\n-789.13\n1079.22\n-741.13\n1577.10\n87.84\n-237.36\n4.29\n983.34\n-630.33\n-550.49\n1218.69\n132.32\n-128.63\n-809.61\n1363.48\n182.25\n132.90\n1892.30\n-526.04\n-613.70\n-1129.03\n23.61\n-98.37\n750.65\n-404.18\n527.32\n78.62\n1132.37\n-660.67\n-1987.75\n-1286.86\n-570.89\n906.35\n2097.27\n-186.11\n-98.79\n-1968.20\n-637.03\n759.13\n14.50\n741.77\n-2016.48\n416.75\n-999.71\n1544.68\n-192.97\n-450.62\n207.17\n886.26\n486.14\n-1136.32\n466.40\n372.99\n314.50\n-1287.77\n-268.96\n-778.86\n-651.03\n-1540.31\n-1420.13\n1270.51\n-8.81\n-1312.01\n1575.77\n-1347.39\n-885.66\n-1465.37\n-711.99\n-53.94\n-952.97\n-366.15\n-917.99\n271.32\n-69.63\n-107.71\n552.17\n1422.76\n1547.79\n-1594.47\n719.72\n471.96\n2920.48\n160.90\n2275.91\n970.01\n1529.27\n1305.70\n113.63\n88.28\n220.04\n1600.84\n602.77\n655.37\n467.06\n2864.70\n1232.79\n-1931.35\n899.39\n401.69\n79.77\n-67.04\n849.31\n-2253.39\n-1082.60\n512.10\n-1020.81\n853.42\n-201.54\n1786.52\n-208.08\n831.65\n-917.49\n-786.68\n-275.14\n479.84\n271.10\n101.29\n-107.77\n-232.47\n1233.67\n510.93\n611.97\n-240.64\n885.50\n41.82\n157.95\n-566.05\n820.70\n-327.37\n844.07\n1011.31\n-70.82\n869.72\n185.25\n-627.27\n280.40\n-833.37\n247.94\n-123.37\n1379.90\n-189.63\n112.49\n-562.03\n450.14\n-1107.87\n27.22\n317.87\n-107.81\n375.59\n-138.04\n1271.65\n1434.00\n2587.26\n-1407.87\n-224.21\n1178.05\n-995.54\n255.96\n-1024.30\n62.70\n-618.20\n-417.57\n-1063.43\n-752.65\n-113.12\n-1823.02\n262.33\n787.18\n-419.63\n2563.15\n722.59\n961.86\n-742.38\n-1413.48\n1229.95\n524.71\n-575.95\n424.58\n1126.07\n263.86\n262.76\n952.19\n-278.86\n-1130.05\n-3200.24\n-128.64\n91.84\n-1157.37\n1312.76\n-645.07\n-948.08\n-2060.55\n-1024.01\n310.28\n144.99\n-1294.29\n-321.07\n-740.24\n-492.96\n-1968.01\n608.67\n-1341.01\n-128.96\n1563.56\n-1111.86\n-215.43\n-2072.72\n-612.85\n-682.95\n830.45\n-1478.47\n-186.78\n716.77\n478.91\n-140.09\n-585.67\n-292.42\n-662.58\n-206.07\n-56.94\n943.89\n-772.27\n-971.52\n-932.13\n-791.80\n1181.42\n928.74\n2413.45\n-318.49\n85.49\n-675.19\n-569.39\n1220.32\n-542.56\n494.58\n-746.54\n242.61\n1880.18\n701.37\n-810.08\n269.34\n-1.33\n869.23\n1783.16\n-608.63\n2033.02\n-850.28\n1692.15\n139.39\n159.34\n-916.83\n-1065.26\n27.87\n312.45\n-834.46\n-1158.54\n21.94\n570.12\n98.46\n-287.97\n938.39\n-262.88\n934.23\n-1182.93\n-1404.51\n1930.65\n-68.55\n179.71\n481.93\n1062.62\n318.04\n1288.00\n646.77\n-990.12\n-1216.03\n-592.33\n568.64\n-574.81\n-163.71\n2657.55\n-705.23\n240.85\n73.39\n1661.46\n1768.55\n691.38\n1159.80\n-330.82\n-250.51\n1040.66\n-844.41\n836.02\n-814.75\n5369.87\n-7328.61\n-603.98\n-6776.40\n-1761.92\n4743.97\n-1217.72\n5573.22\n-728.11\n2937.34\n-4609.05\n-1935.96\n-6226.60\n6113.10\n1348.54\n2744.33\n1535.60\n-6858.76\n3625.07\n3600.71\n-1733.46\n5291.35\n4826.00\n1192.51\n1026.06\n4254.74\n4195.21\n-314.98\n-2806.72\n-789.38\n-3042.71\n2059.92\n-968.92\n484.40\n-18.32\n-8283.29\n1586.71\n2102.81\n2568.07\n-235.37\n3439.61\n-830.74\n-949.74\n-1381.51\n1384.58\n-1407.50\n-4123.93\n-1647.96\n239.35\n1674.57\n2233.18\n303.21\n991.77\n3712.83\n-2027.18\n-572.31\n8638.13\n3448.63\n4296.07\n-3624.94\n-649.83\n1622.28\n-50.06\n-2666.39\n1062.21\n2437.08\n5745.58\n-506.58\n6668.65\n6216.22\n9471.60\n6387.79\n8839.08\n-5607.20\n4587.07\n3442.10\n-671.76\n1971.24\n3153.72\n-95.73\n-12583.63\n-6630.87\n-8597.07\n2833.72\n3628.75\n-6218.52\n2221.79\n14109.02\n3062.05\n3648.13\n-6730.44\n-1157.66\n6.87\n5027.47\n-2699.22\n5711.76\n853.79\n-2628.03\n-3001.51\n-6487.83\n-160.64\n-1832.16\n3264.07\n6215.86\n373.24\n5970.57\n-9797.43\n-6710.60\n2271.49\n1133.92\n2751.12\n6011.14\n-5623.58\n-816.69\n919.45\n-4915.16\n-7241.93\n-2687.47\n2042.33\n3322.32\n2984.83\n1927.79\n-2903.86\n11088.63\n-70.14\n2283.83\n-1351.84\n-2031.94\n-1114.03\n4493.35\n2131.78\n-1617.67\n-4018.71\n807.45\n5926.71\n5135.57\n1692.96\n1991.07\n1298.85\n4105.89\n-2328.39\n3462.52\n-3095.37\n-5034.95\n-5583.94\n7817.33\n7879.58\n6220.21\n4454.40\n1783.22\n-26.01\n-2068.86\n6498.95\n2887.03\n4778.73\n5153.57\n-2624.29\n-1307.80\n3200.35\n-2176.06\n-8098.00\n964.35\n-1111.40\n-4612.94\n218.76\n531.73\n-7876.89\n-7049.96\n-1686.57\n-1669.57\n-5698.42\n-1131.97\n-1049.07\n6746.17\n1859.57\n-1052.35\n1336.26\n5381.22\n4312.35\n-1882.33\n-146.40\n7571.54\n4084.50\n3432.31\n1661.77\n-3459.17\n3143.05\n-708.83\n-4321.15\n4831.40\n2335.21\n4149.53\n-1017.42\n-4388.81\n3607.38\n-5987.19\n-3860.60\n-3682.35\n2238.95\n-3139.57'
Q_DEMO = 99.0
W_DEMO = 250

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 600
N_TEST = 350
X = 10
X_ATT = 3.500000000000003
COVERAGE = 2.8571428571428545
LR_POF = 8.11914579654298
P_POF = 0.004380019184386352
LR_IND = 0.5900560930183758
P_IND = 0.4423974287160052
LR_CC = 8.709201889561356
P_CC = 0.012847565449407128
MAX_RUN = 1
ZONA = "giallo"
STATO = "copertura insufficiente"
VERDETTO = 'copertura insufficiente: 10 sforamenti contro 3.5 attesi (coverage 2.86x, p-value Kupiec 0.0044): il VaR storico rolling non ha retto il regime di mercato, ricalibra finestra o modello prima di usarlo per il limite.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh321_risultato"](SERIE_DEMO, Q_DEMO, W_DEMO)


class TestRegistry321:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 363
        assert TITLE321 in titoli
        assert "tab321" in dvars
        assert "    with tab321:" in src

    def test_titoli_allineati_319_320_321(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab319")] == TITLE319
        assert titoli[dvars.index("tab320")] == TITLE320
        assert titoli[dvars.index("tab321")] == TITLE321

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE363
        assert dvars[-1] == "tab363"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh321_conf"](99.0) == pytest.approx(0.01)
        assert _F["mh321_conf"](97.5) == pytest.approx(0.025)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh321_conf"](98.0)

    def test_finestra_ok(self):
        assert _F["mh321_finestra"](250) == 250
        assert _F["mh321_finestra"](100.0) == 100

    def test_finestra_ko(self):
        for bad in (49, 1001, 250.5):
            with pytest.raises(ValueError):
                _F["mh321_finestra"](bad)

    def test_parse_pnl_ok(self):
        r = _F["mh321_parse_pnl"](SERIE_DEMO)
        assert len(r) == N == 600
        assert all(isinstance(v, float) for v in r)

    def test_parse_pnl_ko(self):
        with pytest.raises(ValueError):
            _F["mh321_parse_pnl"](";" .join(["1.0"] * 399))
        with pytest.raises(ValueError):
            _F["mh321_parse_pnl"]("a\nb\nc")

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x"):
            with pytest.raises(ValueError):
                _F["mh321_num"](bad, "t")


class TestQuantile:
    def test_quantile_noto(self):
        vs = list(range(1, 101))
        assert _F["mh321_quantile"](vs, 0.01) == pytest.approx(99.01, abs=1e-9)

    def test_quantile_bordi(self):
        assert _F["mh321_quantile"]([1.0, 2.0, 3.0], 0.5) == 2.0
        with pytest.raises(ValueError):
            _F["mh321_quantile"]([1.0], 0.01)
        with pytest.raises(ValueError):
            _F["mh321_quantile"]([1.0, 2.0], 0.0)


class TestVarRolling:
    def test_lunghezza(self):
        L = _F["mh321_losses"](_F["mh321_parse_pnl"](SERIE_DEMO))
        var = _F["mh321_var_rolling"](L, Q_DEMO, W_DEMO)
        assert len(var) == N_TEST == 363

    def test_var_positiva_e_adattiva(self):
        L = [100.0] * 300 + [2000.0] * 300
        var = _F["mh321_var_rolling"](L, 99.0, 250)
        assert var[-1] > var[0]
        assert all(v > 0 for v in var)

    def test_finestra_ko(self):
        L = [1.0] * 500
        with pytest.raises(ValueError):
            _F["mh321_var_rolling"](L, 99.0, 450)


class TestBreaches:
    def test_breaches_noti(self):
        br = _F["mh321_breaches"]([10.0, 20.0, 5.0], [15.0, 15.0, 15.0])
        assert br["flags"] == [0, 1, 0]
        assert br["giorni"] == [2]
        assert br["w"] == 0

    def test_breaches_offset(self):
        br = _F["mh321_breaches"]([1.0, 2.0, 30.0, 4.0], [25.0, 25.0])
        assert br["w"] == 2
        assert br["flags"] == [1, 0]
        assert br["giorni"] == [3]

    def test_demo_sforamenti(self):
        ris = _ris_demo()
        assert ris["x"] == X
        assert ris["x"] > ris["x_att"]
        assert ris["coverage"] == COVERAGE > 1.0


class TestChi2:
    def test_chi2_1_noto(self):
        assert _F["mh321_chi2_1_cdf"](3.8414588) == pytest.approx(0.95, abs=1e-5)

    def test_chi2_2_noto(self):
        assert _F["mh321_chi2_2_cdf"](5.9914645) == pytest.approx(0.95, abs=1e-5)

    def test_chi2_bordi(self):
        assert _F["mh321_chi2_1_cdf"](0.0) == 0.0
        assert _F["mh321_chi2_2_cdf"](0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh321_chi2_1_cdf"](-1.0)


class TestKupiec:
    def test_kupiec_ko(self):
        with pytest.raises(ValueError):
            _F["mh321_kupiec"](-1, 100, 0.01)
        with pytest.raises(ValueError):
            _F["mh321_kupiec"](101, 100, 0.01)
        with pytest.raises(ValueError):
            _F["mh321_kupiec"](5, 100, 1.5)

    def test_kupiec_demo(self):
        ris = _ris_demo()
        assert ris["lr_pof"] == LR_POF
        assert ris["p_pof"] == P_POF
        assert P_POF < 0.05
        assert ris["lr_pof"] == pytest.approx(
            -2.0 * (math.log(0.99 ** (N_TEST - X) * 0.01 ** X) -
                    math.log((1.0 - X / N_TEST) ** (N_TEST - X) *
                             (X / N_TEST) ** X)), rel=1e-9)


class TestChristoffersen:
    def test_counts_noti(self):
        c = _F["mh321_christoffersen"]([0, 0, 1, 1, 0, 1, 0, 0])
        assert (c["n00"], c["n01"], c["n10"], c["n11"]) == (2, 2, 2, 1)
        assert c["max_run"] == 2
        assert c["x"] == 3

    def test_no_breach(self):
        c = _F["mh321_christoffersen"]([0] * 50)
        assert c["x"] == 0
        assert c["lr_ind"] == pytest.approx(0.0)

    def test_demo_values(self):
        ris = _ris_demo()
        assert ris["lr_ind"] == LR_IND
        assert ris["p_ind"] == P_IND
        assert ris["lr_cc"] == LR_CC
        assert ris["p_cc"] == P_CC
        assert ris["max_run"] == MAX_RUN
        assert ris["lr_cc"] == pytest.approx(ris["lr_pof"] + ris["lr_ind"])


class TestTraffic:
    def test_basilea_250_99(self):
        # zone Basilea: verde 0-4, giallo 5-9, rosso 10+
        for x in (0, 4):
            assert _F["mh321_traffic"](x, 250, 0.01)["zona"] == "verde"
        for x in (5, 9):
            assert _F["mh321_traffic"](x, 250, 0.01)["zona"] == "giallo"
        for x in (10, 20):
            assert _F["mh321_traffic"](x, 250, 0.01)["zona"] == "rosso"

    def test_traffic_ko(self):
        with pytest.raises(ValueError):
            _F["mh321_traffic"](-1, 250, 0.01)
        with pytest.raises(ValueError):
            _F["mh321_traffic"](251, 250, 0.01)

    def test_demo_zona(self):
        assert _ris_demo()["zona"] == ZONA


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N == 600
        assert ris["q"] == Q_DEMO
        assert ris["w"] == W_DEMO
        assert ris["n_test"] == N_TEST == 363
        assert ris["x"] == X
        assert ris["x_att"] == X_ATT == pytest.approx(N_TEST * 0.01)
        assert ris["coverage"] == COVERAGE
        assert len(ris["var"]) == N_TEST
        assert len(ris["flags"]) == N_TEST
        assert len(ris["giorni"]) == X
        assert len(ris["L"]) == N

    def test_coerenza_interna(self):
        ris = _ris_demo()
        assert sum(ris["flags"]) == ris["x"]
        assert ris["coverage"] == pytest.approx(ris["x"] / ris["x_att"])
        assert ris["lr_pof"] >= 0.0
        assert 0.0 <= ris["p_pof"] <= 1.0
        assert 0.0 <= ris["p_ind"] <= 1.0
        assert 0.0 <= ris["p_cc"] <= 1.0


class TestVerdetto:
    def _base(self, **kw):
        return {"x": 10, "x_att": 2.5, "coverage": 4.0, "p_pof": 0.001,
                "p_ind": 0.5, "zona": "rosso", "max_run": 3, **kw}

    def test_verdetto_demo(self):
        assert _F["mh321_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_copertura_insufficiente(self):
        v = _F["mh321_verdetto"](self._base())
        assert v.startswith("copertura insufficiente")

    def test_stato_copertura_eccessiva(self):
        v = _F["mh321_verdetto"](self._base(x=0, coverage=0.0, zona="verde"))
        assert v.startswith("copertura eccessiva")

    def test_stato_grappoli(self):
        v = _F["mh321_verdetto"](self._base(p_pof=0.5, p_ind=0.01,
                                            zona="verde", max_run=6,
                                            x=3, coverage=1.2, x_att=2.5))
        assert v.startswith("sforamenti a grappoli")

    def test_stato_giallo(self):
        v = _F["mh321_verdetto"](self._base(p_pof=0.2, p_ind=0.5,
                                            zona="giallo", x=6,
                                            coverage=2.4))
        assert v.startswith("semaforo giallo")

    def test_stato_affidabile(self):
        v = _F["mh321_verdetto"](self._base(p_pof=0.6, p_ind=0.7,
                                            zona="verde", x=2,
                                            coverage=0.8, x_att=2.5))
        assert v.startswith("modello affidabile")
