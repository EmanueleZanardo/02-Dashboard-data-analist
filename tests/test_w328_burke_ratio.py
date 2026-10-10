"""Test tab328 '🔻 Burke ratio: il drawdown penalizzato al quadrato': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Burke ratio: validatori,
parse equity, episodi di drawdown (picco/trough/profondita/durata/recupero),
CAGR annualizzato, stat con penalita' quadratica e Burke, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh328_num", "mh328_parse_equity", "mh328_episodi", "mh328_cagr",
           "mh328_stat", "mh328_verdetto")

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
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
SERIE_DEMO = '100\n103\n106\n109\n112\n115\n118\n119\n120\n116\n111\n106\n101\n97\n94\n100\n106\n112\n118\n124\n130\n126\n121\n117\n115\n114\n118\n123\n128\n133\n138\n142\n139\n136\n133\n130\n134\n138\n142\n146\n149\n152\n154\n156\n158\n160\n162\n164'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
CAGR = 13.462865756360042
MAXDD = 21.666666666666668
DEN_BURKE = 26.312319097518884
BURKE = 0.5116563730647946
N_EP = 3
DEPTHS = [21.666666666666668, 12.307692307692308, 8.450704225352112]
RECUPERI = [True, True, True]
STATO = "burke ratio MODERATO"
VERDETTO = "burke ratio MODERATO: 0.51: il rendimento batte la penalita' quadratica ma con poco margine: un episodio piu' profondo del solito farebbe crollare il verdetto, rivedere sizing e stop-loss prima di scalare."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh328_parse_equity"](SERIE_DEMO)


class TestRegistry328:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 360
        assert TITLE328 in titoli
        assert "tab328" in dvars
        assert "    with tab328:" in src

    def test_titoli_allineati_326_327_328(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab326")] == TITLE326
        assert titoli[dvars.index("tab327")] == TITLE327
        assert titoli[dvars.index("tab328")] == TITLE328

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE360
        assert dvars[-1] == "tab360"


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh328_num"](3.5, "t") == 3.5
        assert _F["mh328_num"](12, "t") == 12.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh328_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh328_parse_equity"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(v > 0.0 for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh328_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        for bad in ("0", "-5"):
            with pytest.raises(ValueError):
                _F["mh328_parse_equity"](
                    "\n".join(["100"] * 29 + [bad]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh328_parse_equity"]("\n".join(["a"] * 30))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh328_parse_equity"](None)

    def test_parse_virgola(self):
        vals = _F["mh328_parse_equity"]("\n".join(["100,5"] * 30))
        assert vals[0] == 100.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["100"] * 30) + "\n\n"
        assert len(_F["mh328_parse_equity"](txt)) == 30


class TestEpisodi:
    def test_demo_conteggio(self):
        epis = _F["mh328_episodi"](_eq_demo())
        assert len(epis) == N_EP == 3

    def test_demo_profondita(self):
        epis = _F["mh328_episodi"](_eq_demo())
        prof = sorted((e["profondita"] for e in epis), reverse=True)
        assert prof == pytest.approx(DEPTHS)
        assert all(p > 0.0 for p in prof)

    def test_demo_recupero(self):
        epis = _F["mh328_episodi"](_eq_demo())
        assert [e["recuperato"] for e in epis] == RECUPERI
        assert all(e["recuperato"] for e in epis)
        for e in epis:
            assert e["i_recupero"] > e["i_trough"] > e["i_picco"]
            assert e["periodi_recupero"] == e["i_recupero"] - e["i_trough"]
            assert e["durata"] == e["i_trough"] - e["i_picco"]
            assert e["v_picco"] > e["v_trough"]

    def test_demo_profondita_formula(self):
        epis = _F["mh328_episodi"](_eq_demo())
        for e in epis:
            att = (e["v_picco"] - e["v_trough"]) / e["v_picco"] * 100.0
            assert e["profondita"] == pytest.approx(att)

    def test_episodio_non_recuperato(self):
        eq = [100.0 + i for i in range(40)] + [120.0] * 8 + [110.0] * 2
        epis = _F["mh328_episodi"](eq)
        assert len(epis) == 1
        assert epis[0]["recuperato"] is False
        assert epis[0]["i_recupero"] is None
        assert epis[0]["periodi_recupero"] is None
        assert epis[0]["profondita"] == pytest.approx(
            (139.0 - 110.0) / 139.0 * 100.0)

    def test_senza_drawdown(self):
        eq = [100.0 + i for i in range(30)]
        assert _F["mh328_episodi"](eq) == []

    def test_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh328_episodi"]([100.0] * 29)


class TestCagr:
    def test_demo(self):
        assert _F["mh328_cagr"](_eq_demo(), 12) == pytest.approx(CAGR / 100.0)

    def test_cagr_scaling(self):
        eq = [100.0, 200.0] + [200.0] * 28
        assert _F["mh328_cagr"](eq, 12) == pytest.approx(2.0 ** (12 / 29) - 1)

    def test_cagr_negativo(self):
        eq = [100.0 - i for i in range(30)]
        assert _F["mh328_cagr"](eq, 12) < 0.0

    def test_cagr_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh328_cagr"](_eq_demo(), 0)


class TestStat:
    def test_stat_demo(self):
        st_ = _F["mh328_stat"](_eq_demo(), 12, 3)
        assert st_["n"] == N == 48
        assert st_["cagr"] == pytest.approx(CAGR)
        assert st_["max_dd"] == pytest.approx(MAXDD)
        assert st_["den_burke"] == pytest.approx(DEN_BURKE)
        assert st_["burke"] == pytest.approx(BURKE)
        assert st_["n_ep"] == N_EP == 3
        assert len(st_["episodi"]) == 3

    def test_stat_keys(self):
        st_ = _F["mh328_stat"](_eq_demo(), 12, 3)
        for k in ("n", "cagr", "max_dd", "den_burke", "burke",
                  "n_ep", "episodi"):
            assert k in st_

    def test_stat_ordinamento_episodi(self):
        st_ = _F["mh328_stat"](_eq_demo(), 12, 3)
        prof = [e["profondita"] for e in st_["episodi"]]
        assert prof == sorted(prof, reverse=True)
        assert st_["max_dd"] == pytest.approx(prof[0])

    def test_stat_penalita_quadratica_formula(self):
        st_ = _F["mh328_stat"](_eq_demo(), 12, 3)
        att = math.sqrt(sum(d ** 2 for d in DEPTHS))
        assert st_["den_burke"] == pytest.approx(att)
        assert st_["burke"] == pytest.approx(st_["cagr"] / att)

    def test_stat_k_maggiore_episodi(self):
        st3 = _F["mh328_stat"](_eq_demo(), 12, 3)
        st9 = _F["mh328_stat"](_eq_demo(), 12, 9)
        assert st9["den_burke"] == pytest.approx(st3["den_burke"])
        assert st9["burke"] == pytest.approx(st3["burke"])

    def test_stat_k1_uguale_calmar(self):
        st_ = _F["mh328_stat"](_eq_demo(), 12, 1)
        assert st_["den_burke"] == pytest.approx(st_["max_dd"])
        assert st_["burke"] == pytest.approx(
            st_["cagr"] / st_["max_dd"])

    def test_stat_k_ko(self):
        for bad in (0, 2.5, -1):
            with pytest.raises(ValueError):
                _F["mh328_stat"](_eq_demo(), 12, bad)

    def test_stat_senza_drawdown_inf(self):
        eq = [100.0 + i for i in range(30)]
        st_ = _F["mh328_stat"](eq, 12, 3)
        assert math.isinf(st_["burke"])
        assert st_["n_ep"] == 0
        assert st_["den_burke"] == 0.0

    def test_stat_piatta_ko(self):
        with pytest.raises(ValueError):
            _F["mh328_stat"]([100.0] * 30, 12, 3)


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh328_verdetto"](1.2, 3)
        assert v.startswith("burke ratio ECCELLENTE")

    def test_verdetto_soglia_eccellente(self):
        v = _F["mh328_verdetto"](0.8, 3)
        assert v.startswith("burke ratio ECCELLENTE")

    def test_verdetto_inf(self):
        v = _F["mh328_verdetto"](float("inf"), 0)
        assert v.startswith("burke ratio ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh328_verdetto"](0.6, 3)
        assert v.startswith("burke ratio MODERATO")

    def test_verdetto_soglia_moderato(self):
        v = _F["mh328_verdetto"](0.4, 3)
        assert v.startswith("burke ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh328_verdetto"](0.3, 3)
        assert v.startswith("burke ratio DEBOLE")

    def test_verdetto_un_solo_episodio(self):
        v = _F["mh328_verdetto"](0.6, 1)
        assert v.startswith("burke ratio MODERATO")
        assert "Calmar" in v

    def test_verdetto_demo(self):
        st_ = _F["mh328_stat"](_eq_demo(), 12, 3)
        v = _F["mh328_verdetto"](st_["burke"], st_["n_ep"])
        assert v == VERDETTO
        assert v.startswith(STATO)
