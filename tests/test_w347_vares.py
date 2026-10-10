"""Test tab347 'VaR & Expected Shortfall del P&L dopo N trade': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del VaR/Expected Shortfall:
validatori, quantile normale di Acklam, VaR = percentile delle perdite a
confidenza conf, ES = media delle perdite oltre il VaR, cross-check
analitico via normale sul log-capitale, casi limite (f=0 -> perdite nulle;
conf alta -> VaR >= VaR a conf piu' bassa) e verdetto a 3 stati
(VAR NEI LIMITI / SOTTO OSSERVAZIONE / RIDURRE f).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh347_num", "mh347_int", "mh347_norm_ppf", "mh347_var_es",
           "mh347_verdetto", "mh347_misure", "mh346_num", "mh346_int",
           "mh346_g", "mh346_simula", "mh346_percentile")

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
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
F = 0.0875
N = 250
NSIM = 2000
SEED = 42
CONF = 0.95
VARMAX = 0.3
B = 1.2
G = 0.013709697146873145
VAR = -1.3241517924696615
ES = -0.49267159051089016
VAR_AN = -1.587851439192605
NCODA = 104
VERDETTO = 'VAR NEI LIMITI (VaR = -132.4% <= 30%): il P&L di coda resta entro la soglia del desk.'

_VE = None


def _ve():
    global _VE
    if _VE is None:
        _VE = _F["mh347_var_es"](P, B, F, N, NSIM, CONF, SEED)
    return _VE


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry347:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 365
        assert "tab347" in dvars
        assert "tab347" in withs

    def test_titoli_allineati_344_345_346_347(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab344")] == TITLE344
        assert titoli[dvars.index("tab345")] == TITLE345
        assert titoli[dvars.index("tab346")] == TITLE346
        assert titoli[dvars.index("tab347")] == TITLE347

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab365"
        assert titoli[-1] == TITLE365
        assert withs[-1] == "tab365"


class TestNum:
    def test_num_ok(self):
        assert _F["mh347_num"](1.5, "x") == 1.5
        assert _F["mh347_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh347_num"](bad, "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh347_int"](5, "x", 1, 10) == 5
        assert _F["mh347_int"](1, "x", 1, 10) == 1

    def test_int_ko(self):
        for bad in (True, 1.5, "5", None):
            with pytest.raises(ValueError):
                _F["mh347_int"](bad, "x", 1, 10)
        for bad in (0, 11):
            with pytest.raises(ValueError):
                _F["mh347_int"](bad, "x", 1, 10)


class TestNormPpf:
    def test_mediana(self):
        assert _F["mh347_norm_ppf"](0.5) == pytest.approx(0.0, abs=1e-9)

    def test_valori_noti(self):
        assert _F["mh347_norm_ppf"](0.975) == pytest.approx(1.9599639845,
                                                           rel=1e-6)
        assert _F["mh347_norm_ppf"](0.025) == pytest.approx(-1.9599639845,
                                                           rel=1e-6)
        assert _F["mh347_norm_ppf"](0.95) == pytest.approx(1.6448536269,
                                                           rel=1e-6)

    def test_simmetria(self):
        assert _F["mh347_norm_ppf"](0.9) == pytest.approx(
            -_F["mh347_norm_ppf"](0.1), rel=1e-9)

    def test_ko(self):
        for bad in (0.0, 1.0, -0.1, 1.5, float("nan")):
            with pytest.raises(ValueError):
                _F["mh347_norm_ppf"](bad)


class TestVarEs:
    def test_determinismo(self):
        v1, v2 = _ve(), _F["mh347_var_es"](P, B, F, N, NSIM, CONF, SEED)
        assert v1["perdite"] == v2["perdite"]
        assert v1["var"] == v2["var"]
        assert v1["es"] == v2["es"]

    def test_seed_diverso(self):
        v1 = _ve()
        v2 = _F["mh347_var_es"](P, B, F, N, NSIM, CONF, SEED + 1)
        assert v1["perdite"] != v2["perdite"]

    def test_demo_valori(self):
        v = _ve()
        assert v["g"] == pytest.approx(G, rel=1e-9)
        assert v["var"] == pytest.approx(VAR, rel=1e-9)
        assert v["es"] == pytest.approx(ES, rel=1e-9)
        assert v["var_analitico"] == pytest.approx(VAR_AN, rel=1e-9)
        assert v["n_coda"] == NCODA
        assert v["conf"] == pytest.approx(CONF)
        assert v["seed"] == SEED

    def test_es_maggiore_var(self):
        v = _ve()
        assert v["es"] >= v["var"]

    def test_var_analitico_formula(self):
        v = _ve()
        z = _F["mh347_norm_ppf"](1.0 - CONF)
        up, down = 1.0 + F * B, 1.0 - F
        sig2 = P * (1.0 - P) * (math.log(up / down)) ** 2
        att = 1.0 - math.exp(N * G + z * math.sqrt(N * sig2))
        assert v["var_analitico"] == pytest.approx(att, rel=1e-9)

    def test_var_analitico_vicino_simulato(self):
        v = _ve()
        assert v["var_analitico"] == pytest.approx(v["var"], rel=0.35)

    def test_var_cresce_con_confidenza(self):
        v90 = _F["mh347_var_es"](P, B, F, N, NSIM, 0.90, SEED)
        v99 = _F["mh347_var_es"](P, B, F, N, NSIM, 0.99, SEED)
        assert v99["var"] >= v90["var"]
        assert v99["es"] >= v90["es"]

    def test_f_zero(self):
        v = _F["mh347_var_es"](P, B, 0.0, 50, 100, CONF, 7)
        assert all(x == 0.0 for x in v["perdite"])
        assert v["var"] == 0.0
        assert v["es"] == 0.0
        assert v["var_analitico"] == pytest.approx(0.0, abs=1e-12)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, 0, NSIM, CONF, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, N, 50, CONF, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, N, NSIM, 0.5, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, F, N, NSIM, 1.0, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, B, 1.0, N, NSIM, CONF, SEED)
        with pytest.raises(ValueError):
            _F["mh347_var_es"](P, 0.0, F, N, NSIM, CONF, SEED)


class TestVerdetto:
    def test_nei_limiti(self):
        v = _F["mh347_verdetto"](0.20, 0.30)
        assert v.startswith("VAR NEI LIMITI")

    def test_sotto_osservazione(self):
        v = _F["mh347_verdetto"](0.40, 0.30)
        assert v.startswith("SOTTO OSSERVAZIONE")

    def test_ridurre(self):
        v = _F["mh347_verdetto"](0.60, 0.30)
        assert v.startswith("RIDURRE f")

    def test_demo(self):
        assert VERDETTO == _F["mh347_verdetto"](VAR, VARMAX)

    def test_ko_varmax(self):
        with pytest.raises(ValueError):
            _F["mh347_verdetto"](0.20, 0.0)


class TestMisure:
    def test_demo(self):
        m = _F["mh347_misure"](P, WIN, LOSS, F, N, NSIM, CONF, VARMAX,
                                SEED)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f"] == pytest.approx(F)
        assert m["n_trade"] == N
        assert m["n_sim"] == NSIM
        assert m["seed"] == SEED
        assert m["var"] == pytest.approx(VAR, rel=1e-9)
        assert m["es"] == pytest.approx(ES, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_f_zero(self):
        m = _F["mh347_misure"](P, WIN, LOSS, 0.0, 50, 100, CONF, VARMAX,
                                7)
        assert m["var"] == 0.0
        assert m["es"] == 0.0

    def test_ko_win(self):
        with pytest.raises(ValueError):
            _F["mh347_misure"](P, 0.0, LOSS, F, N, NSIM, CONF, VARMAX,
                                SEED)

