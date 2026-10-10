"""Test tab332 '🎯 Information ratio: la strategia batte davvero il benchmark?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dell'information ratio: validatori,
parse delle due serie di rendimenti %, statistiche sul rendimento attivo
(IR annualizzato, tracking error, attivo medio, t-stat, hit rate) e verdetto
a 3 stati (soglie 0.25 / 0.60).
"""
import math
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh332_num", "mh332_parse_serie", "mh332_statistiche",
           "mh332_verdetto")

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
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
SERIE_ST_DEMO = '1.57\n-1.33\n1.57\n1.47\n-2.23\n1.57\n2.07\n-1.33\n1.67\n-0.63\n0.67\n1.07\n-0.03\n0.87\n0.67\n0.67\n1.17\n-2.33\n1.57\n1.27\n-1.33\n0.87\n2.47\n-1.33\n1.67\n0.27\n0.67\n-0.03\n0.07\n1.37\n1.37\n-1.23\n1.37\n1.67\n-1.13\n1.97'
SERIE_BM_DEMO = '0.8\n-0.5\n1.2\n0.3\n-1.0\n1.5\n0.6\n-0.8\n1.1\n0.4\n-0.3\n0.9\n1.4\n0.2\n-0.6\n1.0\n0.7\n-1.2\n0.5\n1.3\n-0.4\n0.6\n1.1\n-0.7\n0.9\n1.6\n0.1\n-0.9\n0.8\n1.2\n0.4\n-0.2\n1.0\n0.5\n-0.6\n1.3'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
IR_ANN = 0.4965893718644655
TE_ANN = 3.03402922420555
ATT_MEDIO_ANN = 1.506666666666666
HIT_RATE = 61.111111111111114
T_STAT = 0.860118022567969
BEST = 1.4699999999999998
WORST = -1.43
STRAT_ANN = 6.24
BM_ANN = 4.733333333333334
STATO = "information ratio MODERATO"
VERDETTO = "information ratio MODERATO (+0.50): la strategia batte il benchmark con regolarita' (hit rate 61.1%) ma il premio per unita' di tracking error resta contenuto: verificare costi e fee prima di scalare. Attenzione: t-stat +0.86 sotto la soglia 2.0, l'outperformance potrebbe essere rumore statistico."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh332_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh332_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry332:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 369
        assert "tab332" in dvars
        assert "tab332" in withs

    def test_titoli_allineati_329_330_331_332(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab329")] == TITLE329
        assert titoli[dvars.index("tab330")] == TITLE330
        assert titoli[dvars.index("tab331")] == TITLE331
        assert titoli[dvars.index("tab332")] == TITLE332

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab369"
        assert titoli[-1] == TITLE369
        assert withs[-1] == "tab369"


class TestNum:
    def test_num_ok(self):
        assert _F["mh332_num"](1.5, "x") == 1.5
        assert _F["mh332_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh332_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh332_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.57)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh332_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh332_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh332_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh332_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestStatistiche:
    def test_demo(self):
        rs, rb = _demo()
        s = _F["mh332_statistiche"](rs, rb, 12)
        assert s["n"] == N_PER
        assert s["ir_ann"] == pytest.approx(IR_ANN, rel=1e-9)
        assert s["te_ann"] == pytest.approx(TE_ANN, rel=1e-9)
        assert s["att_medio_ann"] == pytest.approx(ATT_MEDIO_ANN, rel=1e-9)
        assert s["hit_rate"] == pytest.approx(HIT_RATE, rel=1e-9)
        assert s["t_stat"] == pytest.approx(T_STAT, rel=1e-9)
        assert s["best"] == pytest.approx(BEST, rel=1e-9)
        assert s["worst"] == pytest.approx(WORST, rel=1e-9)
        assert s["strat_ann"] == pytest.approx(STRAT_ANN, rel=1e-9)
        assert s["bm_ann"] == pytest.approx(BM_ANN, rel=1e-9)

    def test_attivo_coerente(self):
        rs, rb = _demo()
        s = _F["mh332_statistiche"](rs, rb, 12)
        assert s["att_medio_ann"] == pytest.approx(
            (s["strat_ann"] - s["bm_ann"]), rel=1e-9)
        assert s["te_ann"] > 0.0

    def test_ir_none_attivo_costante(self):
        a = np.array([1.0] * 36)
        s = _F["mh332_statistiche"](a + 0.5, a, 12)
        assert s["ir_ann"] is None
        assert s["t_stat"] is None
        assert s["te_ann"] == pytest.approx(0.0)

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh332_statistiche"](rs, rb[:20], 12)

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh332_statistiche"](np.ones(11), np.ones(11), 12)

    def test_ko_p(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh332_statistiche"](rs, rb, 0)


class TestVerdetto:
    def test_verdetto_debole(self):
        v = _F["mh332_verdetto"](0.10, 45.0, 1.2)
        assert v.startswith("information ratio DEBOLE")

    def test_verdetto_soglia_debole(self):
        v = _F["mh332_verdetto"](0.249, 50.0, 2.5)
        assert v.startswith("information ratio DEBOLE")

    def test_verdetto_moderato(self):
        v = _F["mh332_verdetto"](0.25, 55.0, 2.5)
        assert v.startswith("information ratio MODERATO")

    def test_verdetto_soglia_forte(self):
        v = _F["mh332_verdetto"](0.60, 70.0, 3.0)
        assert v.startswith("information ratio MODERATO")

    def test_verdetto_forte(self):
        v = _F["mh332_verdetto"](0.85, 75.0, 3.5)
        assert v.startswith("information ratio FORTE")

    def test_verdetto_none(self):
        v = _F["mh332_verdetto"](None, 50.0, None)
        assert v.startswith("information ratio NON MISURABILE")

    def test_verdetto_nota_significativita(self):
        v = _F["mh332_verdetto"](0.50, 61.0, 0.8)
        assert v.startswith("information ratio MODERATO")
        assert "Attenzione" in v

    def test_verdetto_nessuna_nota_se_significativo(self):
        v = _F["mh332_verdetto"](0.50, 61.0, 2.5)
        assert "Attenzione" not in v

    def test_verdetto_demo(self):
        v = _F["mh332_verdetto"](IR_ANN, HIT_RATE, T_STAT)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh332_verdetto"]("x", 50.0, 1.0)
