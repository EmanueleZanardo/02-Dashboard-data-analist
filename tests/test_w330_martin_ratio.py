"""Test tab330 '🔍📉 Martin ratio: il Calmar che guarda tutto il dolore': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Martin ratio: validatori, parse
equity, serie dei drawdown, Ulcer Index (media quadratica), CAGR annualizzato,
Martin = CAGR / Ulcer e verdetto a 3 stati (soglie 2.0 / 1.0).
"""
import math
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh330_num", "mh330_parse_equity", "mh330_drawdown", "mh330_ulcer",
           "mh330_cagr", "mh330_martin", "mh330_verdetto")

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
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
SERIE_DEMO = '100\n103\n106\n109\n112\n115\n118\n119\n120\n116\n111\n106\n101\n97\n94\n100\n106\n112\n118\n124\n130\n126\n121\n117\n115\n114\n118\n123\n128\n133\n138\n142\n139\n136\n133\n130\n134\n138\n142\n146\n149\n152\n154\n156\n158\n160\n162\n164'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
CAGR = 13.462865756360042
ULCER = 7.194094635946087
MARTIN = 1.871377350124274
MAXDD = 21.666666666666668
STATO = "martin ratio MODERATO"
VERDETTO = 'martin ratio MODERATO: 1.87: il rendimento copre a malapena il dolore continuo (Ulcer Index 7.19%): drawdown frequenti anche senza colpi profondissimi, rivedere sizing e stop-loss prima di scalare.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh330_parse_equity"](SERIE_DEMO)


class TestRegistry330:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 356
        assert TITLE330 in titoli
        assert "tab330" in dvars
        assert "    with tab330:" in src

    def test_titoli_allineati_327_328_329_330(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab327")] == TITLE327
        assert titoli[dvars.index("tab328")] == TITLE328
        assert titoli[dvars.index("tab329")] == TITLE329
        assert titoli[dvars.index("tab330")] == TITLE330

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert titoli[-1] == TITLE356
        assert dvars[-1] == "tab356"
        assert withs[-1] == "tab356"


class TestNum:
    def test_num_ok(self):
        assert _F["mh330_num"](3, "x") == 3.0
        assert _F["mh330_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh330_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        eq = _F["mh330_parse_equity"](SERIE_DEMO)
        assert len(eq) == N == 48
        assert (eq > 0).all()

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh330_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        with pytest.raises(ValueError):
            _F["mh330_parse_equity"]("\n".join(["100"] * 29 + ["0"]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh330_parse_equity"]("\n".join(["100"] * 29 + ["abc"]))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh330_parse_equity"]([100.0] * 30)

    def test_parse_virgola(self):
        eq = _F["mh330_parse_equity"]("\n".join(["100,5"] * 30))
        assert eq[0] == pytest.approx(100.5)

    def test_parse_righe_vuote(self):
        eq = _F["mh330_parse_equity"]("\n\n".join(["100"] * 30))
        assert len(eq) == 30


class TestDrawdown:
    def test_drawdown_formula(self):
        eq = _eq_demo()
        dd = _F["mh330_drawdown"](eq)
        peak = np.maximum.accumulate(eq)
        att = (peak - eq) / peak
        assert dd == pytest.approx(att)
        assert (dd >= 0).all()

    def test_drawdown_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh330_drawdown"]([100.0] * 29)


class TestUlcer:
    def test_ulcer_demo(self):
        assert _F["mh330_ulcer"](_eq_demo()) == pytest.approx(ULCER / 100.0)

    def test_ulcer_formula(self):
        eq = _eq_demo()
        dd = _F["mh330_drawdown"](eq)
        att = math.sqrt(float(np.mean(dd ** 2)))
        assert _F["mh330_ulcer"](eq) == pytest.approx(att)

    def test_ulcer_senza_drawdown_zero(self):
        eq = [100.0 + i for i in range(30)]
        assert _F["mh330_ulcer"](eq) == 0.0

    def test_ulcer_minore_uguale_maxdd(self):
        eq = _eq_demo()
        assert _F["mh330_ulcer"](eq) <= _F["mh330_martin"](eq, 12)["max_dd"]


class TestCagr:
    def test_demo(self):
        assert _F["mh330_cagr"](_eq_demo(), 12) == pytest.approx(CAGR / 100.0)

    def test_cagr_scaling(self):
        eq = [100.0, 200.0] + [200.0] * 28
        assert _F["mh330_cagr"](eq, 12) == pytest.approx(2.0 ** (12 / 29) - 1)

    def test_cagr_negativo(self):
        eq = [100.0 - i for i in range(30)]
        assert _F["mh330_cagr"](eq, 12) < 0.0

    def test_cagr_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh330_cagr"](_eq_demo(), 0)


class TestMartin:
    def test_stat_demo(self):
        r = _F["mh330_martin"](_eq_demo(), 12)
        assert r["n"] == N == 48
        assert r["cagr"] == pytest.approx(CAGR / 100.0)
        assert r["ulcer"] == pytest.approx(ULCER / 100.0)
        assert r["max_dd"] == pytest.approx(MAXDD / 100.0)
        assert r["martin"] == pytest.approx(MARTIN)

    def test_stat_keys(self):
        r = _F["mh330_martin"](_eq_demo(), 12)
        for k in ("n", "cagr", "ulcer", "max_dd", "martin"):
            assert k in r

    def test_martin_formula(self):
        r = _F["mh330_martin"](_eq_demo(), 12)
        assert r["martin"] == pytest.approx(r["cagr"] / r["ulcer"])

    def test_martin_maggiore_uguale_calmar(self):
        # ulcer <= max_dd => cagr/ulcer >= cagr/max_dd (il Calmar)
        r = _F["mh330_martin"](_eq_demo(), 12)
        calmar = r["cagr"] / r["max_dd"]
        assert r["martin"] >= calmar

    def test_martin_senza_drawdown_inf(self):
        eq = [100.0 + i for i in range(30)]
        r = _F["mh330_martin"](eq, 12)
        assert r["ulcer"] == 0.0
        assert math.isinf(r["martin"])

    def test_martin_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh330_martin"]([100.0] * 29, 12)

    def test_martin_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh330_martin"](_eq_demo(), 0)


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh330_verdetto"](2.5, 7.0)
        assert v.startswith("martin ratio ECCELLENTE")

    def test_verdetto_soglia_eccellente(self):
        v = _F["mh330_verdetto"](2.0, 7.0)
        assert v.startswith("martin ratio ECCELLENTE")

    def test_verdetto_inf(self):
        v = _F["mh330_verdetto"](float("inf"), 0.0)
        assert v.startswith("martin ratio ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh330_verdetto"](1.5, 7.0)
        assert v.startswith("martin ratio MODERATO")

    def test_verdetto_soglia_moderato(self):
        v = _F["mh330_verdetto"](1.0, 7.0)
        assert v.startswith("martin ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh330_verdetto"](0.99, 7.0)
        assert v.startswith("martin ratio DEBOLE")

    def test_verdetto_ko_nan(self):
        with pytest.raises(ValueError):
            _F["mh330_verdetto"](float("nan"), 7.0)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh330_verdetto"]("x", 7.0)

    def test_verdetto_demo(self):
        r = _F["mh330_martin"](_eq_demo(), 12)
        v = _F["mh330_verdetto"](r["martin"], r["ulcer"] * 100.0)
        assert v == VERDETTO
        assert v.startswith(STATO)
