"""Test tab325 '📈📉 Calmar ratio: il rendimento che paga il drawdown': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Calmar ratio: validatori,
parse equity, drawdown (underwater, max DD, picco/trough), CAGR annualizzato,
stat con recupero, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh325_num", "mh325_parse_equity", "mh325_drawdown", "mh325_cagr",
           "mh325_stat", "mh325_verdetto")

TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
SERIE_DEMO = '100\n102\n104\n106\n108\n110\n109\n107\n105\n103\n101\n99\n97\n99\n102\n105\n108\n111\n114\n117\n119\n122\n124\n126\n129\n131\n129\n127\n124\n121\n118\n115\n113\n112\n115\n118\n122\n126\n130\n134\n138\n142\n146\n150\n154\n157\n160\n163'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
CAGR = 13.285821564989364
MAXDD = 14.50381679389313
CALMAR = 0.9160224342176877
RECUPERO = 6
I_PICCO = 25
I_TROUGH = 33
STATO = "calmar MODERATO"
VERDETTO = 'calmar MODERATO: 0.92: il rendimento copre il drawdown ma con poco margine, profilo migliorabile: ridurre le esposizioni nei periodi di calo o alzare il rendimento per periodo.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh325_parse_equity"](SERIE_DEMO)


class TestRegistry325:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 332
        assert TITLE325 in titoli
        assert "tab325" in dvars
        assert "    with tab325:" in src

    def test_titoli_allineati_323_324_325(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab323")] == TITLE323
        assert titoli[dvars.index("tab324")] == TITLE324
        assert titoli[dvars.index("tab325")] == TITLE325

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE332
        assert dvars[-1] == "tab332"


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh325_num"](3.5, "t") == 3.5
        assert _F["mh325_num"](12, "t") == 12.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh325_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh325_parse_equity"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(v > 0.0 for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh325_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        for bad in ("0", "-5"):
            with pytest.raises(ValueError):
                _F["mh325_parse_equity"](
                    "\n".join(["100"] * 29 + [bad]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh325_parse_equity"]("\n".join(["a"] * 30))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh325_parse_equity"](None)

    def test_parse_virgola(self):
        vals = _F["mh325_parse_equity"]("\n".join(["100,5"] * 30))
        assert vals[0] == 100.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["100"] * 30) + "\n\n"
        assert len(_F["mh325_parse_equity"](txt)) == 30


class TestDrawdown:
    def test_demo(self):
        dd, max_dd, i_p, i_t = _F["mh325_drawdown"](_eq_demo())
        assert len(dd) == N == 48
        assert max_dd == pytest.approx(MAXDD)
        assert i_p == I_PICCO
        assert i_t == I_TROUGH
        assert dd[i_p] == 0.0
        assert min(dd) == pytest.approx(-MAXDD)
        assert all(d <= 0.0 for d in dd)

    def test_senza_drawdown(self):
        eq = [100.0 + i for i in range(30)]
        dd, max_dd, _, _ = _F["mh325_drawdown"](eq)
        assert max_dd == 0.0
        assert all(d == 0.0 for d in dd)

    def test_picco_trough_coerenti(self):
        eq = _eq_demo()
        _, _, i_p, i_t = _F["mh325_drawdown"](eq)
        assert i_p < i_t
        assert eq[i_p] > eq[i_t]

    def test_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh325_drawdown"]([100.0] * 29)


class TestCagr:
    def test_demo(self):
        assert _F["mh325_cagr"](_eq_demo(), 12) == pytest.approx(CAGR / 100.0)

    def test_cagr_scaling(self):
        eq = [100.0, 200.0] + [200.0] * 28
        assert _F["mh325_cagr"](eq, 12) == pytest.approx(2.0 ** (12 / 29) - 1)

    def test_cagr_raddoppio_biennale(self):
        eq = [100.0] * 24 + [200.0] * 6
        assert _F["mh325_cagr"](eq, 24) == pytest.approx(2.0 ** (24 / 29) - 1)

    def test_cagr_negativo(self):
        eq = [100.0 - i for i in range(30)]
        assert _F["mh325_cagr"](eq, 12) < 0.0

    def test_cagr_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh325_cagr"](_eq_demo(), 0)


class TestStat:
    def test_stat_demo(self):
        st_ = _F["mh325_stat"](_eq_demo(), 12)
        assert st_["n"] == N == 48
        assert st_["cagr"] == pytest.approx(CAGR)
        assert st_["max_dd"] == pytest.approx(MAXDD)
        assert st_["calmar"] == pytest.approx(CALMAR)
        assert st_["i_picco"] == I_PICCO
        assert st_["i_trough"] == I_TROUGH
        assert st_["recupero"] == RECUPERO
        assert len(st_["dd"]) == N

    def test_stat_keys(self):
        st_ = _F["mh325_stat"](_eq_demo(), 12)
        for k in ("n", "cagr", "max_dd", "calmar", "i_picco", "i_trough",
                  "recupero", "dd"):
            assert k in st_

    def test_stat_calmar_inf(self):
        eq = [100.0 + i for i in range(30)]
        st_ = _F["mh325_stat"](eq, 12)
        assert math.isinf(st_["calmar"])
        assert st_["max_dd"] == 0.0

    def test_stat_piatta_ko(self):
        with pytest.raises(ValueError):
            _F["mh325_stat"]([100.0] * 30, 12)

    def test_stat_recupero_none(self):
        eq = [100.0 + i for i in range(40)] + [120.0] * 8 + [110.0] * 2
        st_ = _F["mh325_stat"](eq, 12)
        assert st_["recupero"] is None
        assert st_["max_dd"] > 0.0


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh325_verdetto"](2.0)
        assert v.startswith("calmar ECCELLENTE")

    def test_verdetto_inf(self):
        v = _F["mh325_verdetto"](float("inf"))
        assert v.startswith("calmar ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh325_verdetto"](0.9)
        assert v.startswith("calmar MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh325_verdetto"](0.2)
        assert v.startswith("calmar DEBOLE")

    def test_verdetto_negativo(self):
        v = _F["mh325_verdetto"](-1.0)
        assert v.startswith("calmar DEBOLE")

    def test_verdetto_demo(self):
        st_ = _F["mh325_stat"](_eq_demo(), 12)
        v = _F["mh325_verdetto"](st_["calmar"])
        assert v == VERDETTO
        assert v.startswith(STATO)
