"""Test tab333 '📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dei capture ratio: validatori,
parse delle due serie di rendimenti %, statistiche up/down (up/down capture
%, medie di fase, asimmetria) e verdetto a 4 stati
(OTTIMO / AGGRESSIVO / DIFENSIVO / DEBOLE + NON MISURABILE).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh333_num", "mh333_parse_serie", "mh333_statistiche",
           "mh333_verdetto")

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
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
SERIE_ST_DEMO = '1.87\n-0.38\n2.56\n1.18\n-0.74\n2.22\n-0.2\n1.53\n-1.1\n0.95\n1.99\n-0.56\n1.07\n-0.44\n2.91\n1.41\n-0.92\n0.72\n-0.26\n2.33\n3.37\n-1.28\n1.76\n-0.32\n0.84\n1.3\n-0.62\n2.1\n-0.14\n1.18\n1.64\n-0.8\n2.45\n-0.38\n1.41\n-1.04'
SERIE_BM_DEMO = '1.5\n-0.8\n2.1\n0.9\n-1.4\n1.8\n-0.5\n1.2\n-2.0\n0.7\n1.6\n-1.1\n0.8\n-0.9\n2.4\n1.1\n-1.7\n0.5\n-0.6\n1.9\n2.8\n-2.3\n1.4\n-0.7\n0.6\n1.0\n-1.2\n1.7\n-0.4\n0.9\n1.3\n-1.5\n2.0\n-0.8\n1.1\n-1.9'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
N_UP = 21
N_DOWN = 15
UP_CAP = 125.56313993174062
DOWN_CAP = 51.573033707865164
ASIMMETRIA = 73.99010622387546
BM_UP_AVG = 1.3952380952380952
ST_UP_AVG = 1.7519047619047619
BM_DOWN_AVG = -1.1866666666666668
ST_DOWN_AVG = -0.612
STATO = "capture ratio OTTIMO"
VERDETTO = "capture ratio OTTIMO (up 125.6% / down 51.6%): la strategia cattura piu' delle salite del benchmark e perde meno nelle discese: asimmetria favorevole, la gestione attiva crea valore in entrambe le fasi di mercato."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh333_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh333_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry333:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 368
        assert "tab333" in dvars
        assert "tab333" in withs

    def test_titoli_allineati_330_331_332_333(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab330")] == TITLE330
        assert titoli[dvars.index("tab331")] == TITLE331
        assert titoli[dvars.index("tab332")] == TITLE332
        assert titoli[dvars.index("tab333")] == TITLE333

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab368"
        assert titoli[-1] == TITLE368
        assert withs[-1] == "tab368"


class TestNum:
    def test_num_ok(self):
        assert _F["mh333_num"](1.5, "x") == 1.5
        assert _F["mh333_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh333_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh333_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.87)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh333_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh333_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh333_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh333_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestStatistiche:
    def test_demo(self):
        rs, rb = _demo()
        s = _F["mh333_statistiche"](rs, rb)
        assert s["n"] == N_PER
        assert s["n_up"] == N_UP == 21
        assert s["n_down"] == N_DOWN == 15
        assert s["up_capture"] == pytest.approx(UP_CAP, rel=1e-9)
        assert s["down_capture"] == pytest.approx(DOWN_CAP, rel=1e-9)
        assert s["asimmetria"] == pytest.approx(ASIMMETRIA, rel=1e-9)
        assert s["bm_up_avg"] == pytest.approx(BM_UP_AVG, rel=1e-9)
        assert s["st_up_avg"] == pytest.approx(ST_UP_AVG, rel=1e-9)
        assert s["bm_down_avg"] == pytest.approx(BM_DOWN_AVG, rel=1e-9)
        assert s["st_down_avg"] == pytest.approx(ST_DOWN_AVG, rel=1e-9)

    def test_capture_coerenti(self):
        rs, rb = _demo()
        s = _F["mh333_statistiche"](rs, rb)
        assert s["up_capture"] == pytest.approx(
            s["st_up_avg"] / s["bm_up_avg"] * 100.0, rel=1e-9)
        assert s["down_capture"] == pytest.approx(
            s["st_down_avg"] / s["bm_down_avg"] * 100.0, rel=1e-9)
        assert s["asimmetria"] == pytest.approx(
            s["up_capture"] - s["down_capture"], rel=1e-9)

    def test_ko_senza_periodi_su(self):
        rs = np.array([0.5] * 36)
        rb = np.array([-0.5] * 36)
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_senza_periodi_giu(self):
        rs = np.array([0.5] * 36)
        rb = np.array([0.5] * 36)
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_pochi_su(self):
        rb = np.array([1.0, 2.0, 3.0] + [-1.0] * 33)
        rs = rb * 1.1
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_pochi_giu(self):
        rb = np.array([1.0] * 33 + [-1.0, -2.0, -3.0])
        rs = rb * 1.1
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb)

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh333_statistiche"](np.ones(11), np.ones(11))


class TestVerdetto:
    def test_verdetto_ottimo(self):
        v = _F["mh333_verdetto"](125.6, 51.6)
        assert v.startswith("capture ratio OTTIMO")

    def test_verdetto_aggressivo(self):
        v = _F["mh333_verdetto"](110.0, 120.0)
        assert v.startswith("capture ratio AGGRESSIVO")

    def test_verdetto_soglia_100(self):
        v = _F["mh333_verdetto"](100.0, 100.0)
        assert v.startswith("capture ratio AGGRESSIVO")

    def test_verdetto_difensivo(self):
        v = _F["mh333_verdetto"](90.0, 80.0)
        assert v.startswith("capture ratio DIFENSIVO")

    def test_verdetto_debole(self):
        v = _F["mh333_verdetto"](90.0, 120.0)
        assert v.startswith("capture ratio DEBOLE")

    def test_verdetto_none(self):
        v = _F["mh333_verdetto"](None, 51.6)
        assert v.startswith("capture ratio NON MISURABILE")
        v2 = _F["mh333_verdetto"](125.6, None)
        assert v2.startswith("capture ratio NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh333_verdetto"](UP_CAP, DOWN_CAP)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh333_verdetto"]("x", 50.0)
