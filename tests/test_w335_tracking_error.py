"""Test tab335 '📏 Tracking error: quanto si discosta la strategia dal benchmark?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del tracking error: validatori,
parse delle due serie di rendimenti %, statistiche (n, exp_active, te,
te_ann, exp_active_ann, ir, max/min attivo, pct_fuori) e verdetto a 4 stati
(PASSIVA / CONTROLLATA / ATTIVA / MOLTO ATTIVA + NON MISURABILE), con nota
se l'excess return compensa il rischio attivo.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh335_num", "mh335_parse_serie", "mh335_statistiche",
           "mh335_verdetto")

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
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
SERIE_ST_DEMO = '3.3\n-2.57\n5.94\n0.15\n1.25\n-1.32\n0.96\n-0.4\n1.33\n-0.56\n3.91\n-1.51\n4.97\n-3.34\n4.03\n-1.85\n0.44\n-0.42\n3.07\n-0.04\n4.09\n-5.59\n4.22\n-1.79\n2.57\n-1.11\n2.8\n1.12\n1.4\n-1.88\n4.29\n-1.74\n5.84\n-3.08\n2.56\n-3.33'
SERIE_BM_DEMO = '1.5\n-0.8\n2.1\n0.9\n-1.4\n1.8\n-0.5\n1.2\n-2.0\n0.7\n1.6\n-1.1\n0.8\n-0.9\n2.4\n1.1\n-1.7\n0.5\n-0.6\n1.9\n2.8\n-2.3\n1.4\n-0.7\n0.6\n1.0\n-1.2\n1.7\n-0.4\n0.9\n1.3\n-1.5\n2.0\n-0.8\n1.1\n-1.9'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
EXP_ACT = 0.4502777777777777
TE = 2.4009301603588216
TE_ANN = 8.317066046331941
EXP_ANN = 5.403333333333332
IR = 0.18754305527591159
MAX_ACT = 4.17
MIN_ACT = -3.29
PCT_FUORI = 38.88888888888889
STATO = "tracking error ATTIVA"
VERDETTO = "tracking error ATTIVA (TE 8.32%): la strategia prende posizioni marcate rispetto al benchmark. Deviazioni ampie: va bene solo se l'excess return le giustifica nel tempo. L'excess return annualizzato e' positivo (+5.40 pp): il rischio attivo paga, la strategia viene ripagata per discostarsi dal benchmark."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh335_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh335_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry335:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 354
        assert "tab335" in dvars
        assert "tab335" in withs

    def test_titoli_allineati_332_333_334_335(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab332")] == TITLE332
        assert titoli[dvars.index("tab333")] == TITLE333
        assert titoli[dvars.index("tab334")] == TITLE334
        assert titoli[dvars.index("tab335")] == TITLE335

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab354"
        assert titoli[-1] == TITLE354
        assert withs[-1] == "tab354"


class TestNum:
    def test_num_ok(self):
        assert _F["mh335_num"](1.5, "x") == 1.5
        assert _F["mh335_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh335_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh335_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(3.3)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh335_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh335_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh335_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh335_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestStatistiche:
    def test_demo(self):
        rs, rb = _demo()
        s = _F["mh335_statistiche"](rs, rb)
        assert s["n"] == N_PER == 36
        assert s["exp_active"] == pytest.approx(EXP_ACT, rel=1e-9)
        assert s["te"] == pytest.approx(TE, rel=1e-9)
        assert s["te_ann"] == pytest.approx(TE_ANN, rel=1e-9)
        assert s["exp_active_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert s["ir"] == pytest.approx(IR, rel=1e-9)
        assert s["max_act"] == pytest.approx(MAX_ACT, rel=1e-9)
        assert s["min_act"] == pytest.approx(MIN_ACT, rel=1e-9)
        assert s["pct_fuori"] == pytest.approx(PCT_FUORI, rel=1e-9)

    def test_coerenti(self):
        rs, rb = _demo()
        s = _F["mh335_statistiche"](rs, rb)
        assert s["te_ann"] == pytest.approx(s["te"] * (12 ** 0.5), rel=1e-9)
        assert s["exp_active_ann"] == pytest.approx(s["exp_active"] * 12,
                                                   rel=1e-9)
        assert s["ir"] == pytest.approx(s["exp_active"] / s["te"], rel=1e-9)
        assert 0.0 <= s["pct_fuori"] <= 100.0
        assert s["max_act"] >= s["exp_active"] >= s["min_act"]

    def test_periodi_annuo(self):
        rs, rb = _demo()
        s4 = _F["mh335_statistiche"](rs, rb, 4)
        s12 = _F["mh335_statistiche"](rs, rb, 12)
        assert s4["te_ann"] == pytest.approx(s12["te"] * 2.0, rel=1e-9)
        assert s4["exp_active_ann"] == pytest.approx(s12["exp_active"] * 4,
                                                    rel=1e-9)

    def test_te_zero(self):
        rs = np.array([1.5] * 36)
        rb = np.array([1.5] * 36)
        s = _F["mh335_statistiche"](rs, rb)
        assert s["te"] == pytest.approx(0.0)
        assert s["te_ann"] == pytest.approx(0.0)
        assert s["ir"] is None
        assert s["exp_active"] == pytest.approx(0.0)

    def test_ko_periodi_annuo(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh335_statistiche"](rs, rb, 0)
        with pytest.raises(ValueError):
            _F["mh335_statistiche"](rs, rb, -4)

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh335_statistiche"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh335_statistiche"](np.ones(11), np.ones(11))


class TestVerdetto:
    def test_verdetto_passiva(self):
        v = _F["mh335_verdetto"](1.5, 3.0)
        assert v.startswith("tracking error PASSIVA")
        assert "positivo" in v

    def test_verdetto_soglia_2(self):
        v = _F["mh335_verdetto"](2.0, 1.0)
        assert v.startswith("tracking error CONTROLLATA")

    def test_verdetto_controllata(self):
        v = _F["mh335_verdetto"](4.0, -1.0)
        assert v.startswith("tracking error CONTROLLATA")
        assert "non e' positivo" in v

    def test_verdetto_soglia_6(self):
        v = _F["mh335_verdetto"](6.0, 2.0)
        assert v.startswith("tracking error ATTIVA")

    def test_verdetto_attiva(self):
        v = _F["mh335_verdetto"](8.31, 5.4)
        assert v.startswith("tracking error ATTIVA")

    def test_verdetto_soglia_12(self):
        v = _F["mh335_verdetto"](12.0, 1.0)
        assert v.startswith("tracking error MOLTO ATTIVA")

    def test_verdetto_molto_attiva(self):
        v = _F["mh335_verdetto"](15.0, -2.0)
        assert v.startswith("tracking error MOLTO ATTIVA")

    def test_verdetto_none(self):
        v = _F["mh335_verdetto"](None, 1.0)
        assert v.startswith("tracking error NON MISURABILE")
        v2 = _F["mh335_verdetto"](5.0, None)
        assert v2.startswith("tracking error NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh335_verdetto"](TE_ANN, EXP_ANN)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh335_verdetto"]("x", 1.0)
