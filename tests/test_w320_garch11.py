"""Test tab320 '⚙️📉 GARCH(1,1): la volatilita' che ricorda': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica GARCH(1,1): validatori, filtro
condizionale, fit deterministico con variance targeting, VaR/ES GARCH vs
storici, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh320_num", "mh320_conf", "mh320_alpha", "mh320_beta",
           "mh320_staz", "mh320_parse_pnl", "mh320_garch_filter",
           "mh320_fit_garch11", "mh320_norm_ppf", "mh320_var_es",
           "mh320_risultato", "mh320_verdetto")

TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
SERIE_DEMO = '896.63\n-664.29\n-743.62\n1035.36\n322.53\n-412.43\n-107.74\n-529.05\n859.18\n744.43\n668.22\n-437.46\n158.87\n1607.19\n-1225.33\n-240.64\n-441.98\n-921.36\n-776.63\n664.43\n-182.10\n108.52\n-902.53\n1177.47\n-1128.01\n293.12\n-436.28\n634.01\n814.87\n1218.18\n728.83\n747.27\n852.88\n130.17\n-659.62\n-553.24\n766.22\n-43.06\n221.49\n-181.81\n-1423.04\n793.84\n-228.72\n706.67\n-262.12\n-256.79\n309.53\n-1309.55\n477.10\n-538.56\n664.19\n-109.50\n993.25\n464.13\n50.16\n352.47\n-1081.25\n493.29\n-158.51\n326.72\n-140.40\n-1173.18\n-458.66\n409.49\n-99.92\n-391.06\n-488.56\n-705.61\n-953.46\n-480.75\n862.76\n159.72\n-976.30\n316.94\n1242.11\n1058.09\n-8.09\n272.71\n-180.80\n310.07\n-197.16\n-125.52\n-1035.93\n911.64\n-303.36\n605.12\n1417.08\n-751.98\n-449.85\n1671.33\n50.16\n694.01\n254.63\n-383.46\n-963.08\n-61.35\n-144.76\n-570.40\n1323.59\n269.50\n-1026.93\n84.93\n362.33\n-476.76\n703.66\n-234.17\n949.59\n233.19\n28.19\n-997.93\n1707.10\n-194.63\n404.74\n-1528.87\n844.08\n-507.01\n737.53\n-997.48\n541.24\n1177.02\n-337.91\n-60.97\n901.69\n1001.30\n-823.63\n-517.58\n-334.26\n-439.28\n-894.35\n570.01\n35.20\n1047.90\n-416.80\n-327.23\n-611.72\n109.68\n-36.23\n-844.45\n683.96\n93.63\n217.47\n1595.47\n378.41\n-466.50\n653.18\n-1499.88\n499.81\n-232.59\n135.13\n425.53\n-191.81\n448.49\n133.34\n424.88\n-103.89\n-3.34\n310.72\n389.62\n7.47\n-313.51\n-833.04\n-413.28\n-466.06\n-165.17\n897.96\n327.70\n645.44\n821.68\n-29.21\n222.69\n565.07\n-497.72\n-308.27\n811.58\n188.74\n-292.90\n-806.78\n1194.30\n49.96\n149.77\n-568.12\n831.50\n-849.07\n253.16\n751.22\n392.44\n-68.60\n114.53\n107.51\n1318.33\n-32.92\n-261.16\n1113.03\n1026.95\n639.74\n2051.27\n-112.89\n94.46\n-82.63\n-21.60\n1439.45\n-221.70\n-983.79\n183.07\n-206.45\n-306.26\n612.88\n-639.73\n-37.06\n274.33\n-1307.17\n-6.97\n-59.88\n-756.10\n-1660.19\n-321.14\n212.52\n718.12\n-557.07\n198.44\n154.78\n-246.08\n182.67\n-327.86\n-432.88\n465.05\n-590.56\n-278.31\n450.98\n-77.47\n-369.86\n-461.14\n1265.20\n-346.88\n724.81\n-152.44\n-32.20\n40.89\n-126.60\n-872.34\n-805.66\n-596.75\n-377.93\n171.15\n-61.04\n20.63\n232.72\n1124.07\n-779.07\n881.09\n-424.00\n700.15\n-83.36\n332.57\n289.29\n-1761.97\n-430.06\n-91.02\n-1030.31\n-236.17\n768.70\n428.83\n250.59\n-688.38\n106.12\n430.26\n430.89\n410.00\n251.67\n1131.40\n-932.24\n-66.62\n-94.63\n2059.17\n753.22\n628.25\n-4428.80\n-1410.00\n1762.94\n1576.34\n-1415.67\n-86.72\n462.62\n748.63\n6272.04\n1601.90\n10719.97\n9813.60\n-3785.28\n863.16\n-3640.88\n-5528.98\n3376.42\n-4598.32\n1977.62\n1571.28\n4805.91\n-3680.04\n4837.61\n-5115.69'
Q_DEMO = 99.0
FIN_DEMO = 1

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 300
MU = 108.2466
OMEGA = 79091.19677492412
ALPHA = 0.31
BETA = 0.65
PERS = 0.96
LL = -2123.6210809415925
SIG_NOW = 4317.318330625447
SIG_AVG = 1008.8574326441833
VAR_G = 10043.58432000806
ES_G = 11506.578208542554
VAR_HS = 4538.741799999999
ES_HS = 5189.243266666667
GAP = 1.2128565057408778
VOL_RATIO = 4.27941371191556
STATO = "GARCH molto prudente"
VERDETTO = "GARCH molto prudente: il VaR con la volatilita' stimata supera del 121.3% quello storico (10,044 vs 4,539 euro): il mercato e' in regime stressato, usa il VaR GARCH per il limite."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _r_demo():
    return _F["mh320_parse_pnl"](SERIE_DEMO)


def _ris_demo():
    return _F["mh320_risultato"](SERIE_DEMO, Q_DEMO, FIN_DEMO)


class TestRegistry320:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 327
        assert TITLE320 in titoli
        assert "tab320" in dvars
        assert "    with tab320:" in src

    def test_titoli_allineati_318_319_320(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab318")] == TITLE318
        assert titoli[dvars.index("tab319")] == TITLE319
        assert titoli[dvars.index("tab320")] == TITLE320

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE327
        assert dvars[-1] == "tab327"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh320_conf"](99.0) == pytest.approx(0.01)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh320_conf"](97.5)

    def test_alpha_ok(self):
        assert _F["mh320_alpha"](0.0) == 0.0
        assert _F["mh320_alpha"](0.2) == 0.2
        assert _F["mh320_alpha"](0.4) == 0.4

    def test_alpha_ko(self):
        for bad in (-0.01, 0.41, 1.0):
            with pytest.raises(ValueError):
                _F["mh320_alpha"](bad)

    def test_beta_ok(self):
        assert _F["mh320_beta"](0.0) == 0.0
        assert _F["mh320_beta"](0.9) == 0.9
        assert _F["mh320_beta"](0.99) == 0.99

    def test_beta_ko(self):
        for bad in (-0.01, 1.0):
            with pytest.raises(ValueError):
                _F["mh320_beta"](bad)

    def test_staz_ok(self):
        assert _F["mh320_staz"](0.05, 0.90) == pytest.approx(0.95)

    def test_staz_ko(self):
        with pytest.raises(ValueError):
            _F["mh320_staz"](0.5, 0.6)

    def test_parse_pnl_ok(self):
        r = _r_demo()
        assert len(r) == N == 300
        assert all(isinstance(v, float) for v in r)

    def test_parse_pnl_ko(self):
        with pytest.raises(ValueError):
            _F["mh320_parse_pnl"](";" .join(["1.0"] * 99))
        with pytest.raises(ValueError):
            _F["mh320_parse_pnl"]("a\nb\nc")
        with pytest.raises(ValueError):
            _F["mh320_parse_pnl"](";" .join(["1.0"] * 100) + "\nnan")

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x"):
            with pytest.raises(ValueError):
                _F["mh320_num"](bad, "t")


class TestFilter:
    def test_lunghezze_e_positivita(self):
        f = _F["mh320_garch_filter"](_r_demo(), OMEGA, ALPHA, BETA)
        assert len(f["sig"]) == N
        assert len(f["z"]) == N
        assert all(v > 0.0 for v in f["sig"])
        assert all(math.isfinite(v) for v in f["z"])
        assert math.isfinite(f["ll"])
        assert f["sig_now"] > 0.0

    def test_shock_alza_vol(self):
        r = [100.0] * 150 + [800.0] * 150
        f = _F["mh320_garch_filter"](r, 10000.0, 0.08, 0.90)
        assert f["sig"][-1] > f["sig"][0]
        assert f["sig_now"] > f["sig"][-1]

    def test_omega_ko(self):
        with pytest.raises(ValueError):
            _F["mh320_garch_filter"](_r_demo(), 0.0, ALPHA, BETA)

    def test_demo_stressato(self):
        assert SIG_NOW > SIG_AVG
        assert VOL_RATIO > 1.5


class TestFit:
    def test_determinismo(self):
        f1 = _F["mh320_fit_garch11"](_r_demo(), FIN_DEMO)
        f2 = _F["mh320_fit_garch11"](_r_demo(), FIN_DEMO)
        assert f1["alpha"] == f2["alpha"]
        assert f1["beta"] == f2["beta"]
        assert f1["ll"] == f2["ll"]

    def test_demo_params(self):
        f = _F["mh320_fit_garch11"](_r_demo(), FIN_DEMO)
        assert f["alpha"] == ALPHA
        assert f["beta"] == BETA
        assert f["pers"] == PERS
        assert f["omega"] == OMEGA
        assert f["mu"] == MU
        assert f["ll"] == LL

    def test_persistenza_stazionaria(self):
        assert 0.0 < PERS < 1.0

    def test_finezza_ko(self):
        with pytest.raises(ValueError):
            _F["mh320_fit_garch11"](_r_demo(), 3)


class TestNormPpf:
    def test_norm_ppf_noto(self):
        assert _F["mh320_norm_ppf"](0.975) == pytest.approx(1.959964, abs=1e-6)


class TestVarEs:
    def test_es_ge_var(self):
        f = _F["mh320_fit_garch11"](_r_demo(), FIN_DEMO)
        ve = _F["mh320_var_es"](_r_demo(), f["mu"], f["sig_now"], Q_DEMO)
        assert ve["es_g"] >= ve["var_g"] > 0.0
        assert ve["es_hs"] >= ve["var_hs"] > 0.0

    def test_demo_values(self):
        assert VAR_G == pytest.approx(SIG_NOW * _F["mh320_norm_ppf"](0.99))
        assert ES_G >= VAR_G
        assert VAR_HS > 0.0
        assert GAP == pytest.approx((VAR_G - VAR_HS) / VAR_HS)
        assert VOL_RATIO == pytest.approx(SIG_NOW / SIG_AVG)

    def test_garch_supera_storica_su_demo(self):
        assert VAR_G > VAR_HS > 0.0
        assert ES_G >= VAR_G
        assert GAP > 0.30


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N == 300
        assert ris["q"] == Q_DEMO
        assert ris["finezza"] == FIN_DEMO
        assert ris["mu"] == MU
        assert ris["omega"] == OMEGA
        assert ris["alpha"] == ALPHA
        assert ris["beta"] == BETA
        assert ris["pers"] == PERS
        assert ris["ll"] == LL
        assert ris["sig_now"] == SIG_NOW
        assert ris["sig_avg"] == SIG_AVG
        assert ris["var_g"] == VAR_G
        assert ris["es_g"] == ES_G
        assert ris["var_hs"] == VAR_HS
        assert ris["es_hs"] == ES_HS
        assert ris["gap"] == GAP
        assert ris["vol_ratio"] == VOL_RATIO
        assert len(ris["r"]) == N
        assert len(ris["sig"]) == N
        assert len(ris["z"]) == N

    def test_gap_coerente(self):
        ris = _ris_demo()
        assert ris["gap"] == pytest.approx(
            (ris["var_g"] - ris["var_hs"]) / ris["var_hs"])


class TestVerdetto:
    def _base(self, **kw):
        return {"gap": 0.0, "pers": 0.9, "var_g": 130000.0,
                "var_hs": 100000.0, **kw}

    def test_verdetto_demo(self):
        assert _F["mh320_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_molto_prudente(self):
        v = _F["mh320_verdetto"](self._base(gap=0.50, var_g=150000.0,
                                            var_hs=100000.0))
        assert v.startswith("GARCH molto prudente")

    def test_stato_prudente(self):
        v = _F["mh320_verdetto"](self._base(gap=0.20, pers=0.9,
                                            var_g=120000.0,
                                            var_hs=100000.0))
        assert v.startswith("GARCH prudente")

    def test_stato_persistenza(self):
        v = _F["mh320_verdetto"](self._base(gap=0.05, pers=0.985))
        assert v.startswith("persistenza altissima")

    def test_stato_clemente(self):
        v = _F["mh320_verdetto"](self._base(gap=-0.15, pers=0.9))
        assert v.startswith("GARCH piu' clemente")

    def test_stato_concordano(self):
        v = _F["mh320_verdetto"](self._base(gap=0.02, pers=0.9))
        assert v.startswith("GARCH e storica concordano")
