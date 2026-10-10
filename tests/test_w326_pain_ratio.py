"""Test tab326 '🩹 Pain index e Pain ratio: il dolore medio oltre il peggio': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Pain index/ratio: validatori,
parse equity, drawdown (underwater, max DD, picco/trough, pain index, quota
tempo in drawdown), CAGR annualizzato, stat con recupero, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh326_num", "mh326_parse_equity", "mh326_drawdown", "mh326_cagr",
           "mh326_stat", "mh326_verdetto")

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
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
SERIE_DEMO = '100\n103\n106\n109\n112\n115\n118\n121\n124\n127\n130\n128\n124\n119\n114\n112\n105\n110\n116\n122\n128\n134\n138\n136\n132\n128\n124\n120\n116\n112\n116\n122\n128\n134\n140\n146\n152\n158\n156\n152\n148\n144\n146\n150\n154\n158\n161\n164'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
CAGR = 13.462865756360042
MAXDD = 19.230769230769234
PAIN = 4.958017583223968
PAINRATIO = 2.7153727332297537
TEMPO_DD = 58.333333333333336
RECUPERO = 5
I_PICCO = 10
I_TROUGH = 16
STATO = "pain ratio MODERATO"
VERDETTO = 'pain ratio MODERATO: 2.72: il rendimento batte il dolore medio ma con poco margine: la strategia passa troppo tempo sotto i massimi, rivedere il timing di ingresso/uscita.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh326_parse_equity"](SERIE_DEMO)


class TestRegistry326:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 361
        assert TITLE326 in titoli
        assert "tab326" in dvars
        assert "    with tab326:" in src

    def test_titoli_allineati_324_325_326(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab324")] == TITLE324
        assert titoli[dvars.index("tab325")] == TITLE325
        assert titoli[dvars.index("tab326")] == TITLE326

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE361
        assert dvars[-1] == "tab361"


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh326_num"](3.5, "t") == 3.5
        assert _F["mh326_num"](12, "t") == 12.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh326_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh326_parse_equity"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(v > 0.0 for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh326_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        for bad in ("0", "-5"):
            with pytest.raises(ValueError):
                _F["mh326_parse_equity"](
                    "\n".join(["100"] * 29 + [bad]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh326_parse_equity"]("\n".join(["a"] * 30))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh326_parse_equity"](None)

    def test_parse_virgola(self):
        vals = _F["mh326_parse_equity"]("\n".join(["100,5"] * 30))
        assert vals[0] == 100.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["100"] * 30) + "\n\n"
        assert len(_F["mh326_parse_equity"](txt)) == 30


class TestDrawdownPain:
    def test_demo(self):
        dd, max_dd, i_p, i_t, pain, tempo = _F["mh326_drawdown"](_eq_demo())
        assert len(dd) == N == 48
        assert max_dd == pytest.approx(MAXDD)
        assert i_p == I_PICCO
        assert i_t == I_TROUGH
        assert pain == pytest.approx(PAIN)
        assert tempo == pytest.approx(TEMPO_DD)
        assert dd[i_p] == 0.0
        assert min(dd) == pytest.approx(-MAXDD)
        assert all(d <= 0.0 for d in dd)

    def test_pain_media(self):
        dd, _, _, _, pain, _ = _F["mh326_drawdown"](_eq_demo())
        assert pain == pytest.approx(abs(sum(dd) / len(dd)))
        assert pain > 0.0

    def test_tempo_dd_quota(self):
        dd, _, _, _, _, tempo = _F["mh326_drawdown"](_eq_demo())
        att = sum(1 for d in dd if d < 0.0) / len(dd) * 100.0
        assert tempo == pytest.approx(att)
        assert 0.0 < tempo < 100.0

    def test_senza_drawdown(self):
        eq = [100.0 + i for i in range(30)]
        dd, max_dd, _, _, pain, tempo = _F["mh326_drawdown"](eq)
        assert max_dd == 0.0
        assert pain == 0.0
        assert tempo == 0.0
        assert all(d == 0.0 for d in dd)

    def test_picco_trough_coerenti(self):
        eq = _eq_demo()
        _, _, i_p, i_t, _, _ = _F["mh326_drawdown"](eq)
        assert i_p < i_t
        assert eq[i_p] > eq[i_t]

    def test_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh326_drawdown"]([100.0] * 29)


class TestCagr:
    def test_demo(self):
        assert _F["mh326_cagr"](_eq_demo(), 12) == pytest.approx(CAGR / 100.0)

    def test_cagr_scaling(self):
        eq = [100.0, 200.0] + [200.0] * 28
        assert _F["mh326_cagr"](eq, 12) == pytest.approx(2.0 ** (12 / 29) - 1)

    def test_cagr_negativo(self):
        eq = [100.0 - i for i in range(30)]
        assert _F["mh326_cagr"](eq, 12) < 0.0

    def test_cagr_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh326_cagr"](_eq_demo(), 0)


class TestStat:
    def test_stat_demo(self):
        st_ = _F["mh326_stat"](_eq_demo(), 12)
        assert st_["n"] == N == 48
        assert st_["cagr"] == pytest.approx(CAGR)
        assert st_["max_dd"] == pytest.approx(MAXDD)
        assert st_["pain"] == pytest.approx(PAIN)
        assert st_["pain_ratio"] == pytest.approx(PAINRATIO)
        assert st_["tempo_dd"] == pytest.approx(TEMPO_DD)
        assert st_["i_picco"] == I_PICCO
        assert st_["i_trough"] == I_TROUGH
        assert st_["recupero"] == RECUPERO
        assert len(st_["dd"]) == N

    def test_stat_keys(self):
        st_ = _F["mh326_stat"](_eq_demo(), 12)
        for k in ("n", "cagr", "max_dd", "pain", "pain_ratio", "tempo_dd",
                  "i_picco", "i_trough", "recupero", "dd"):
            assert k in st_

    def test_stat_pain_ratio_inf(self):
        eq = [100.0 + i for i in range(30)]
        st_ = _F["mh326_stat"](eq, 12)
        assert math.isinf(st_["pain_ratio"])
        assert st_["pain"] == 0.0

    def test_stat_piatta_ko(self):
        with pytest.raises(ValueError):
            _F["mh326_stat"]([100.0] * 30, 12)

    def test_stat_recupero_none(self):
        eq = [100.0 + i for i in range(40)] + [120.0] * 8 + [110.0] * 2
        st_ = _F["mh326_stat"](eq, 12)
        assert st_["recupero"] is None
        assert st_["max_dd"] > 0.0
        assert st_["pain"] > 0.0


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh326_verdetto"](3.5)
        assert v.startswith("pain ratio ECCELLENTE")

    def test_verdetto_soglia_eccellente(self):
        v = _F["mh326_verdetto"](3.0)
        assert v.startswith("pain ratio ECCELLENTE")

    def test_verdetto_inf(self):
        v = _F["mh326_verdetto"](float("inf"))
        assert v.startswith("pain ratio ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh326_verdetto"](2.0)
        assert v.startswith("pain ratio MODERATO")

    def test_verdetto_soglia_moderato(self):
        v = _F["mh326_verdetto"](1.0)
        assert v.startswith("pain ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh326_verdetto"](0.5)
        assert v.startswith("pain ratio DEBOLE")

    def test_verdetto_negativo(self):
        v = _F["mh326_verdetto"](-1.0)
        assert v.startswith("pain ratio DEBOLE")

    def test_verdetto_demo(self):
        st_ = _F["mh326_stat"](_eq_demo(), 12)
        v = _F["mh326_verdetto"](st_["pain_ratio"])
        assert v == VERDETTO
        assert v.startswith(STATO)
