"""Test tab336 '📉 Max drawdown relativo: quanto si scende sotto il benchmark?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del max drawdown relativo:
validatori, parse delle due serie di rendimenti %, statistiche (n, max_dd,
dd_corrente, durata_max, pct_sottacqua, picco_max, valle_min,
exp_active_ann) e verdetto a 4 stati (LIEVE / MODERATO / ELEVATO / SEVERO +
NON MISURABILE), con nota su recupero avvenuto o meno e nota se l'excess
return ripaga il rischio attivo corso.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh336_num", "mh336_parse_serie", "mh336_statistiche",
           "mh336_verdetto")

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
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
SERIE_ST_DEMO = '1.28\n-1.5\n0.5\n3.35\n0.34\n0.7\n0.09\n1.22\n1.34\n0.6\n3.69\n2.41\n2.44\n0.41\n0.08\n-0.76\n-3.16\n-2.58\n-0.83\n-2.15\n1.75\n4.39\n2.23\n4.02\n-1.05\n1.46\n2.03\n2.61\n2.88\n3.05\n2.88\n-0.13\n2.13\n-0.09\n-0.47\n0.35'
SERIE_BM_DEMO = '0.94\n-0.54\n1.43\n1.63\n-1.55\n-0.83\n0.74\n0.25\n0.58\n-0.34\n1.57\n1.46\n0.67\n1.84\n1.11\n-0.35\n1.01\n-0.45\n1.57\n0.55\n0.4\n-0.15\n1.94\n0.43\n0.13\n0.21\n1.19\n1.0\n1.05\n1.07\n2.96\n0.15\n0.04\n-0.3\n1.28\n1.84'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
MAX_DD = 14.27
DD_CORR = 3.24
DURATA_MAX = 16
PCT_UW = 66.66666666666666
PICCO_MAX = 14.22
VALLE_MIN = -3.8200000000000007
EXP_ANN = 3.6599999999999993
STATO = "max drawdown relativo ELEVATO"
VERDETTO = "max drawdown relativo ELEVATO (14.27 pp): la strategia ha attraversato uno scivolone profondo rispetto al benchmark. Accettabile solo se l'excess return di lungo periodo lo ripaga e il mandato tollera oscillazioni ampie. Attenzione: la strategia e' ancora in drawdown relativo (3.24 pp sotto il picco attivo): non ha ancora recuperato lo scivolone. L'excess return annualizzato e' positivo (+3.66 pp): nel complesso il rischio attivo corso e' stato ripagato."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh336_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh336_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry336:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 354
        assert "tab336" in dvars
        assert "tab336" in withs

    def test_titoli_allineati_333_334_335_336(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab333")] == TITLE333
        assert titoli[dvars.index("tab334")] == TITLE334
        assert titoli[dvars.index("tab335")] == TITLE335
        assert titoli[dvars.index("tab336")] == TITLE336

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab354"
        assert titoli[-1] == TITLE354
        assert withs[-1] == "tab354"


class TestNum:
    def test_num_ok(self):
        assert _F["mh336_num"](1.5, "x") == 1.5
        assert _F["mh336_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh336_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh336_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.28)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh336_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh336_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh336_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh336_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestStatistiche:
    def test_demo(self):
        rs, rb = _demo()
        s = _F["mh336_statistiche"](rs, rb)
        assert s["n"] == N_PER == 36
        assert s["max_dd"] == pytest.approx(MAX_DD, rel=1e-9)
        assert s["dd_corrente"] == pytest.approx(DD_CORR, rel=1e-9)
        assert s["durata_max"] == DURATA_MAX
        assert s["pct_sottacqua"] == pytest.approx(PCT_UW, rel=1e-9)
        assert s["picco_max"] == pytest.approx(PICCO_MAX, rel=1e-9)
        assert s["valle_min"] == pytest.approx(VALLE_MIN, rel=1e-9)
        assert s["exp_active_ann"] == pytest.approx(EXP_ANN, rel=1e-9)

    def test_coerenti(self):
        rs, rb = _demo()
        s = _F["mh336_statistiche"](rs, rb)
        assert s["max_dd"] >= 0.0
        assert s["dd_corrente"] >= 0.0
        assert s["max_dd"] >= s["dd_corrente"]
        assert 0 <= s["durata_max"] <= s["n"]
        assert 0.0 <= s["pct_sottacqua"] <= 100.0
        assert s["picco_max"] >= s["valle_min"]
        assert s["max_dd"] <= s["picco_max"] - s["valle_min"] + 1e-9

    def test_periodi_annuo(self):
        rs, rb = _demo()
        s4 = _F["mh336_statistiche"](rs, rb, 4)
        s12 = _F["mh336_statistiche"](rs, rb, 12)
        assert s4["exp_active_ann"] == pytest.approx(s12["exp_active_ann"] / 3,
                                                    rel=1e-9)
        assert s4["max_dd"] == pytest.approx(s12["max_dd"], rel=1e-9)

    def test_dd_zero_sempre_sopra(self):
        rs = np.array([2.0] * 36)
        rb = np.array([1.0] * 36)
        s = _F["mh336_statistiche"](rs, rb)
        assert s["max_dd"] == pytest.approx(0.0)
        assert s["dd_corrente"] == pytest.approx(0.0)
        assert s["durata_max"] == 0
        assert s["pct_sottacqua"] == pytest.approx(0.0)

    def test_ko_periodi_annuo(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh336_statistiche"](rs, rb, 0)
        with pytest.raises(ValueError):
            _F["mh336_statistiche"](rs, rb, -4)

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh336_statistiche"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh336_statistiche"](np.ones(11), np.ones(11))


class TestVerdetto:
    def test_verdetto_lieve(self):
        v = _F["mh336_verdetto"](3.5, 0.0, 2.0)
        assert v.startswith("max drawdown relativo LIEVE")
        assert "recuperato" in v
        assert "positivo" in v

    def test_verdetto_soglia_5(self):
        v = _F["mh336_verdetto"](5.0, 1.0, 1.0)
        assert v.startswith("max drawdown relativo MODERATO")

    def test_verdetto_moderato(self):
        v = _F["mh336_verdetto"](7.0, 2.5, -1.0)
        assert v.startswith("max drawdown relativo MODERATO")
        assert "ancora in drawdown relativo" in v
        assert "non e' positivo" in v

    def test_verdetto_soglia_10(self):
        v = _F["mh336_verdetto"](10.0, 0.0, 1.0)
        assert v.startswith("max drawdown relativo ELEVATO")

    def test_verdetto_elevato(self):
        v = _F["mh336_verdetto"](14.27, 3.24, 3.66)
        assert v.startswith("max drawdown relativo ELEVATO")
        assert "ancora in drawdown relativo" in v

    def test_verdetto_soglia_20(self):
        v = _F["mh336_verdetto"](20.0, 0.0, 1.0)
        assert v.startswith("max drawdown relativo SEVERO")

    def test_verdetto_severo(self):
        v = _F["mh336_verdetto"](26.0, 10.0, -2.0)
        assert v.startswith("max drawdown relativo SEVERO")

    def test_verdetto_none(self):
        v = _F["mh336_verdetto"](None, 1.0, 1.0)
        assert v.startswith("max drawdown relativo NON MISURABILE")
        v2 = _F["mh336_verdetto"](5.0, None, 1.0)
        assert v2.startswith("max drawdown relativo NON MISURABILE")
        v3 = _F["mh336_verdetto"](5.0, 1.0, None)
        assert v3.startswith("max drawdown relativo NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh336_verdetto"](MAX_DD, DD_CORR, EXP_ANN)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh336_verdetto"]("x", 1.0, 1.0)
