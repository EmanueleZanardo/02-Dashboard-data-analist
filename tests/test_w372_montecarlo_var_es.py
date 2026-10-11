"""Test tab372 'Monte Carlo: VaR e Expected Shortfall di una posizione power': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh372_num", "mh372_int", "mh372_paths", "mh372_quantile",
           "mh372_var", "mh372_es", "mh372_prob_perdita",
           "mh372_quota_var", "mh372_verdetto", "mh372_var_teorico",
           "mh372_analisi")

TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
Q = 100.0
PREZZO = 95.0
MU = 0.0
SG = 1.5
H = 1
N = 20000
SEED = 42
ALPHA = 0.95
VAR = 249.40169299684396
ES = 309.5088619538586
PROB = 0.5016
QUOTA = 0.02625280978914147
VARTEO = 246.72804404272074
VERDETTO = 'MODERATO: VaR tra il 2% e il 5% del notionale'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry372:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 372
        assert "tab372" in dvars
        assert "tab372" in withs

    def test_titoli_allineati_367_368_369_370_371_372(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab372"
        assert titoli[-1] == TITLE372
        assert withs[-1] == "tab372"


class TestNum:
    def test_num_ok(self):
        assert _F["mh372_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_num"](float("inf"), "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh372_int"](5, "x", 1) == 5

    def test_float_intero_ok(self):
        assert _F["mh372_int"](5.0, "x", 1) == 5

    def test_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_int"](True, "x", 0)

    def test_float_non_intero_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_int"](5.5, "x", 1)

    def test_sotto_minimo_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_int"](0, "x", 1)


class TestPaths:
    def test_determinismo(self):
        p1 = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        p2 = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        assert p1 == p2

    def test_lunghezza(self):
        assert len(_F["mh372_paths"](Q, MU, SG, H, 500, SEED)) == 500

    def test_seed_diverso(self):
        p1 = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        p2 = _F["mh372_paths"](Q, MU, SG, H, N, SEED + 1)
        assert p1 != p2

    def test_media_vicina_drift(self):
        # mu=0, h=1 -> media ~ 0 (tolleranza 3 sigma/sqrt(n) * Q)
        p = _F["mh372_paths"](Q, 0.0, SG, 1, N, SEED)
        assert abs(sum(p) / len(p)) < 15.0

    def test_q_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_paths"](0.0, MU, SG, H, N, SEED)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_paths"](Q, MU, 0.0, H, N, SEED)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_paths"](Q, MU, SG, H, 50, SEED)


class TestQuantile:
    def test_mediana(self):
        assert _F["mh372_quantile"]([3, 1, 2], 0.5) == pytest.approx(2.0)

    def test_interpolazione(self):
        # pos = 0.25*3 = 0.75 -> 1 + (2-1)*0.75
        assert _F["mh372_quantile"]([1, 2, 3, 4], 0.25) == \
            pytest.approx(1.75)

    def test_estremi(self):
        assert _F["mh372_quantile"]([1, 2, 3], 0.0) == pytest.approx(1.0)
        assert _F["mh372_quantile"]([1, 2, 3], 1.0) == pytest.approx(3.0)

    def test_q_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_quantile"]([1, 2], 1.5)

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_quantile"]([], 0.5)


class TestVar:
    def test_forma_chiusa(self):
        # quantile(..., 0.2): pos=0.8 -> -10+5*0.8 = -6 -> var=6
        assert _F["mh372_var"]([-10, -5, 0, 5, 10],
                               0.8) == pytest.approx(6.0)

    def test_demo(self):
        assert _F["mh372_var"](_F["mh372_paths"](Q, MU, SG, H, N,
                                                SEED),
                               ALPHA) == pytest.approx(VAR)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_var"]([1, 2, 3], 1.0)


class TestEs:
    def test_forma_chiusa(self):
        # quantile(..., 0.2): pos=0.8 -> -10+5*0.8 = -6 -> tail=[-10] -> 10.0
        assert _F["mh372_es"]([-10, -5, 0, 5, 10],
                              0.8) == pytest.approx(10.0)

    def test_demo(self):
        assert _F["mh372_es"](_F["mh372_paths"](Q, MU, SG, H, N,
                                               SEED),
                              ALPHA) == pytest.approx(ES)

    def test_es_maggiore_var(self):
        p = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        assert _F["mh372_es"](p, ALPHA) >= _F["mh372_var"](p, ALPHA)


class TestProbPerdita:
    def test_forma_chiusa(self):
        assert _F["mh372_prob_perdita"]([-1, 0, 1]) == \
            pytest.approx(1.0 / 3.0)

    def test_demo(self):
        # mu=0 simmetrico -> ~0.5
        assert _F["mh372_prob_perdita"](_F["mh372_paths"](
            Q, MU, SG, H, N, SEED)) == pytest.approx(PROB, abs=0.02)


class TestQuotaVar:
    def test_demo(self):
        assert _F["mh372_quota_var"](VAR, Q * PREZZO) == \
            pytest.approx(QUOTA)

    def test_notionale_nullo(self):
        assert _F["mh372_quota_var"](100.0, 0.0) is None


class TestVerdetto:
    def test_demo(self):
        assert _F["mh372_verdetto"](QUOTA) == VERDETTO
        assert _F["mh372_verdetto"](QUOTA).startswith("MODERATO")

    def test_soglie(self):
        assert _F["mh372_verdetto"](0.01).startswith("BASSO")
        assert _F["mh372_verdetto"](0.02).startswith("MODERATO")
        assert _F["mh372_verdetto"](0.05).startswith("ELEVATO")
        assert _F["mh372_verdetto"](0.10).startswith("CRITICO")
        assert _F["mh372_verdetto"](0.15).startswith("CRITICO")

    def test_none(self):
        assert _F["mh372_verdetto"](None).startswith("DATI INSUFFICIENTI")


class TestVarTeorico:
    def test_demo(self):
        # 100*1.5*sqrt(1)*z_0.95 = 150*1.6448536269...
        assert _F["mh372_var_teorico"](Q, SG, H,
                                       ALPHA) == pytest.approx(VARTEO)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(0.99)
        assert _F["mh372_var_teorico"](10.0, 2.0, 4,
                                       0.99) == pytest.approx(10.0 * 2.0 *
                                                              2.0 * z)

    def test_mc_vicino_teorico(self):
        # con 20000 path il MC deve stare entro 5 EUR dal teorico
        p = _F["mh372_paths"](Q, MU, SG, H, N, SEED)
        assert abs(_F["mh372_var"](p, ALPHA) -
                   _F["mh372_var_teorico"](Q, SG, H, ALPHA)) < 5.0

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_var_teorico"](Q, 0.0, H, ALPHA)


class TestAnalisi:
    def test_demo(self):
        a = _F["mh372_analisi"](Q, PREZZO, MU, SG, H, N, SEED, ALPHA)
        assert a["notionale"] == pytest.approx(Q * PREZZO)
        assert a["var"] == pytest.approx(VAR)
        assert a["es"] == pytest.approx(ES)
        assert a["quota_var"] == pytest.approx(QUOTA)
        assert a["var_teorico"] == pytest.approx(VARTEO)
        assert a["verdetto"] == VERDETTO
        assert a["prob_perdita"] == pytest.approx(PROB, abs=0.02)
        assert abs(a["pnl_medio"]) < 15.0
        assert a["pnl_min"] < a["pnl_max"]
        assert a["es"] >= a["var"]

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_analisi"](Q, PREZZO, MU, SG, H, N, SEED, 1.5)

    def test_prezzo_ko(self):
        with pytest.raises(ValueError):
            _F["mh372_analisi"](Q, 0.0, MU, SG, H, N, SEED, ALPHA)
