"""Test tab346 '📊 Monte Carlo: distribuzione del capitale dopo N trade': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Monte Carlo sul capitale:
validatori, percentile con interpolazione lineare, crescita logaritmica attesa g = p*ln(1+f*b)+q*ln(1-f),
simulazione deterministica (seed) con curve percentili per trade,
cross-check analitici (media dei log, mediana vs exp(N*g), E[C_N]
aritmetico), casi limite (f=0 -> capitale fermo; f=0.99 -> barriera
quasi certa) e verdetto a 3 stati (SIZING COMPATIBILE / RISCHIO SOPRA
SOGLIA / RIDURRE f).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh346_num", "mh346_int", "mh346_g", "mh346_simula",
           "mh346_verdetto", "mh346_misure", "mh346_percentile")

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
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
F = 0.0875
N = 250
NSIM = 2000
SEED = 42
BAR = 0.5
PMAX = 0.05
B = 1.2
G = 0.013709697146873145
CAP_MED = 27.98638165712015
P5 = 2.3241517924696615
P95 = 408.0923192188394
PHIT = 0.108
DDMED = 0.16734375
CAP_MED_ATTESO = 30.79721570541028
CAP_MEDIO_ATTESO = 94.82706953954282
VERDETTO = 'RISCHIO SOPRA SOGLIA (P tocco barriera = 10.80% > 5%): valutare se tagliare f o alzare la tolleranza.'

_M = None


def _misure():
    global _M
    if _M is None:
        _M = _F["mh346_misure"](P, WIN, LOSS, F, N, NSIM, BAR, PMAX, SEED)
    return _M


def _sim(**kw):
    args = dict(p=P, b=B, f=F, n_trade=N, n_sim=NSIM, barriera=BAR,
                seed=SEED)
    args.update(kw)
    return _F["mh346_simula"](args["p"], args["b"], args["f"],
                              args["n_trade"], args["n_sim"],
                              args["barriera"], args["seed"])


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry346:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 372
        assert "tab346" in dvars
        assert "tab346" in withs

    def test_titoli_allineati_343_344_345_346(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab343")] == TITLE343
        assert titoli[dvars.index("tab344")] == TITLE344
        assert titoli[dvars.index("tab345")] == TITLE345
        assert titoli[dvars.index("tab346")] == TITLE346

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab372"
        assert titoli[-1] == TITLE372
        assert withs[-1] == "tab372"


class TestNum:
    def test_num_ok(self):
        assert _F["mh346_num"](1.5, "x") == 1.5
        assert _F["mh346_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh346_num"](bad, "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh346_int"](5, "x", 1, 10) == 5
        assert _F["mh346_int"](1, "x", 1, 10) == 1

    def test_int_ko(self):
        for bad in (True, 1.5, "5", None):
            with pytest.raises(ValueError):
                _F["mh346_int"](bad, "x", 1, 10)
        for bad in (0, 11):
            with pytest.raises(ValueError):
                _F["mh346_int"](bad, "x", 1, 10)


class TestG:
    def test_demo(self):
        assert _F["mh346_g"](P, B, F) == pytest.approx(G, rel=1e-9)
        assert _F["mh346_g"](P, B, F) > 0.0

    def test_formula(self):
        assert _F["mh346_g"](0.6, 2.0, 0.1) == pytest.approx(
            0.6 * math.log(1.2) + 0.4 * math.log(0.9), rel=1e-9)

    def test_zero_f(self):
        assert _F["mh346_g"](P, B, 0.0) == 0.0

    def test_negativo_senza_edge(self):
        assert _F["mh346_g"](0.4, 1.0, 0.05) < 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh346_g"](1.0, B, F)
        with pytest.raises(ValueError):
            _F["mh346_g"](P, 0.0, F)
        with pytest.raises(ValueError):
            _F["mh346_g"](P, B, 1.0)


class TestPercentile:
    def test_mediana(self):
        assert _F["mh346_percentile"]([3.0, 1.0, 2.0], 0.5) == 2.0

    def test_estremi(self):
        assert _F["mh346_percentile"]([3.0, 1.0, 2.0], 0.0) == 1.0
        assert _F["mh346_percentile"]([3.0, 1.0, 2.0], 1.0) == 3.0

    def test_singolo(self):
        assert _F["mh346_percentile"]([5.0], 0.5) == 5.0


class TestSimula:
    def test_determinismo(self):
        s1, s2 = _sim(), _sim()
        assert s1["finali"] == s2["finali"]
        assert s1["curve"]["mediana"] == s2["curve"]["mediana"]
        assert s1["dd_max"] == s2["dd_max"]

    def test_seed_diverso(self):
        s1, s2 = _sim(), _sim(seed=SEED + 1)
        assert s1["finali"] != s2["finali"]

    def test_demo_valori(self):
        s = _sim()
        assert s["g"] == pytest.approx(G, rel=1e-9)
        assert s["cap_mediana"] == pytest.approx(CAP_MED, rel=1e-9)
        assert s["cap_p5"] == pytest.approx(P5, rel=1e-9)
        assert s["cap_p95"] == pytest.approx(P95, rel=1e-9)
        assert s["p_hit_barriera"] == pytest.approx(PHIT, rel=1e-9)
        assert s["dd_mediano"] == pytest.approx(DDMED, rel=1e-9)
        assert s["cap_mediano_atteso"] == pytest.approx(CAP_MED_ATTESO,
                                                       rel=1e-9)
        assert s["cap_medio_atteso"] == pytest.approx(CAP_MEDIO_ATTESO,
                                                      rel=1e-9)

    def test_media_logaritmi(self):
        s = _sim()
        mean_log = sum(math.log(c) for c in s["finali"]) / NSIM
        assert mean_log == pytest.approx(N * G, abs=0.15)

    def test_mediana_vs_attesa(self):
        s = _sim()
        assert s["cap_mediana"] == pytest.approx(s["cap_mediano_atteso"],
                                                rel=0.25)

    def test_cap_medio_atteso_formula(self):
        s = _sim()
        edge = P * B - (1.0 - P)
        assert s["cap_medio_atteso"] == pytest.approx((1.0 + F * edge) ** N,
                                                    rel=1e-9)

    def test_curve(self):
        s = _sim()
        for nm in ("p5", "p25", "mediana", "p75", "p95"):
            assert len(s["curve"][nm]) == N + 1
            assert s["curve"][nm][0] == 1.0
        for t in range(N + 1):
            c = s["curve"]
            assert c["p5"][t] <= c["p25"][t] <= c["mediana"][t] <= \
                c["p75"][t] <= c["p95"][t]

    def test_f_zero(self):
        s = _sim(f=0.0, n_trade=50, n_sim=100, seed=7)
        assert all(c == 1.0 for c in s["finali"])
        assert all(d == 0.0 for d in s["dd_max"])
        assert s["p_hit_barriera"] == 0.0
        assert s["g"] == 0.0

    def test_f_estremo_barriera_quasi_certa(self):
        s = _sim(f=0.99, n_trade=50, n_sim=200, seed=7)
        assert s["p_hit_barriera"] == 1.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _sim(n_trade=0)
        with pytest.raises(ValueError):
            _sim(n_sim=50)
        with pytest.raises(ValueError):
            _sim(barriera=0.0)
        with pytest.raises(ValueError):
            _sim(seed=-1)
        with pytest.raises(ValueError):
            _sim(p=1.0)
        with pytest.raises(ValueError):
            _sim(f=1.0)


class TestVerdetto:
    def test_compatibile(self):
        v = _F["mh346_verdetto"](0.02, 0.05)
        assert v.startswith("SIZING COMPATIBILE")

    def test_sopra_soglia(self):
        v = _F["mh346_verdetto"](0.10, 0.05)
        assert v.startswith("RISCHIO SOPRA SOGLIA")

    def test_ridurre(self):
        v = _F["mh346_verdetto"](0.20, 0.05)
        assert v.startswith("RIDURRE f")

    def test_demo(self):
        assert VERDETTO == _F["mh346_verdetto"](PHIT, PMAX)

    def test_ko_pmax(self):
        with pytest.raises(ValueError):
            _F["mh346_verdetto"](0.02, 0.0)


class TestMisure:
    def test_demo(self):
        m = _misure()
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f"] == pytest.approx(F)
        assert m["n_trade"] == N
        assert m["n_sim"] == NSIM
        assert m["seed"] == SEED
        assert m["cap_mediana"] == pytest.approx(CAP_MED, rel=1e-9)
        assert m["p_hit_barriera"] == pytest.approx(PHIT, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_f_zero(self):
        m = _F["mh346_misure"](P, WIN, LOSS, 0.0, 50, 100, BAR, PMAX, 7)
        assert m["cap_mediana"] == 1.0
        assert m["p_hit_barriera"] == 0.0

    def test_ko_win(self):
        with pytest.raises(ValueError):
            _F["mh346_misure"](P, 0.0, LOSS, F, N, NSIM, BAR, PMAX, SEED)

