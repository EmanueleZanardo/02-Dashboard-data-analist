"""Test tab394 '📐⚖ Expectile: la misura di rischio elicitabile e coerente': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh394_num", "mh394_check_alpha", "mh394_up_down",
           "mh394_expectile", "mh394_expectile_quad", "mh394_var",
           "mh394_es", "mh394_ratio", "mh394_verdetto", "mh394_mappa")

TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
EXP = 13983.771246759594
VAR = 19599.639845400536
ES = 23378.027922014157
RATIO = 0.7134708268652792


class TestRegistry394:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 396
        assert "tab394" in dvars
        assert "tab394" in withs

    def test_titoli_allineati_389_390_391_392_393_394(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab389")] == TITLE389
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab396"
        assert titoli[-1] == TITLE396
        assert withs[-1] == "tab396"


class TestNum:
    def test_num_ok(self):
        assert _F["mh394_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_num"](float("inf"), "x")


class TestCheckAlpha:
    @pytest.mark.parametrize("a", [0.5, 0.9, 0.975, 0.99])
    def test_alpha_ok(self, a):
        assert _F["mh394_check_alpha"](a) == a

    @pytest.mark.parametrize("a", [0.0, 1.0, -0.1, 1.5, True, False,
                                   "0.9", None])
    def test_alpha_ko(self, a):
        with pytest.raises(ValueError):
            _F["mh394_check_alpha"](a)

    def test_alpha_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_check_alpha"](float("nan"))


class TestUpDown:
    def test_chiuse_demo(self):
        from statistics import NormalDist
        up, down = _F["mh394_up_down"](MU, SIG, EXP)
        z = (EXP - MU) / SIG
        Phi = NormalDist().cdf(z)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(up - SIG * (phi - z * (1.0 - Phi))) < 1e-9
        assert abs(down - SIG * (phi + z * Phi)) < 1e-9

    def test_foc_demo(self):
        up, down = _F["mh394_up_down"](MU, SIG, EXP)
        assert abs(ALPHA * up - (1.0 - ALPHA) * down) < 1e-9 * SIG

    def test_sig_zero(self):
        assert _F["mh394_up_down"](2000.0, 0.0, 5000.0) == (0.0, 3000.0)
        assert _F["mh394_up_down"](2000.0, 0.0, 1000.0) == (1000.0, 0.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_up_down"](MU, -1.0, EXP)


class TestExpectile:
    def test_demo(self):
        assert _F["mh394_expectile"](MU, SIG, ALPHA) == EXP

    def test_alpha_mezzo_e_media(self):
        assert _F["mh394_expectile"](MU, SIG, 0.5) == MU
        assert _F["mh394_expectile"](1234.5, SIG, 0.5) == 1234.5

    def test_monotonia_alpha(self):
        assert _F["mh394_expectile"](MU, SIG, 0.90) < \
            _F["mh394_expectile"](MU, SIG, 0.95) < \
            _F["mh394_expectile"](MU, SIG, 0.99)

    def test_minore_del_var(self):
        assert EXP < VAR

    @pytest.mark.parametrize("pt", [(0.0, 10000.0, 0.975),
                                    (2000.0, 8000.0, 0.95)])
    def test_quad_crosscheck(self, pt):
        mu, sg, aa = pt
        c = _F["mh394_expectile"](mu, sg, aa)
        q = _F["mh394_expectile_quad"](mu, sg, aa)
        assert abs(c - q) / max(abs(c), 1e-12) < 1e-4

    def test_gerarchia_livelli(self):
        for aa in (0.90, 0.95, 0.975, 0.99):
            e = _F["mh394_expectile"](MU, SIG, aa)
            v = _F["mh394_var"](MU, SIG, aa)
            s = _F["mh394_es"](MU, SIG, aa)
            assert e < v < s

    def test_sig_zero(self):
        assert _F["mh394_expectile"](2000.0, 0.0, ALPHA) == 2000.0
        assert _F["mh394_expectile_quad"](2000.0, 0.0, ALPHA) == 2000.0

    def test_traslazione(self):
        assert abs(_F["mh394_expectile"](5000.0, SIG, ALPHA) -
                   (EXP + 5000.0)) < 1e-6

    def test_scaling(self):
        assert abs(_F["mh394_expectile"](MU, 2.0 * SIG, ALPHA) -
                   2.0 * EXP) < 1e-6

    def test_deterministico(self):
        assert _F["mh394_expectile"](MU, SIG, ALPHA) == \
            _F["mh394_expectile"](MU, SIG, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_expectile"](MU, SIG, 1.5)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_expectile"](MU, -1.0, ALPHA)

    def test_mu_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_expectile"](float("nan"), SIG, ALPHA)


class TestVarEs:
    def test_demo_var(self):
        assert _F["mh394_var"](MU, SIG, ALPHA) == VAR

    def test_demo_es(self):
        assert _F["mh394_es"](MU, SIG, ALPHA) == ES

    def test_var_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh394_var"](MU, SIG, ALPHA) - (MU + SIG * z)) < 1e-9

    def test_es_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh394_es"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_var"](MU, -1.0, ALPHA)


class TestRatioVerdetto:
    def test_demo_ratio(self):
        assert _F["mh394_ratio"](EXP, VAR) == RATIO

    def test_demo_verdetto(self):
        assert _F["mh394_verdetto"](RATIO).startswith("MENO CONSERVATIVO")

    def test_bordi(self):
        assert _F["mh394_verdetto"](1.0).startswith("CONSERVATIVO")
        assert _F["mh394_verdetto"](1.5).startswith("CONSERVATIVO")
        assert _F["mh394_verdetto"](0.99).startswith("INTERMEDIO")
        assert _F["mh394_verdetto"](0.85).startswith("INTERMEDIO")
        assert _F["mh394_verdetto"](0.849).startswith("MENO CONSERVATIVO")
        assert _F["mh394_verdetto"](0.0).startswith("MENO CONSERVATIVO")

    def test_var_non_positivo_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_ratio"](100.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh394_ratio"](100.0, -5.0)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_verdetto"](float("nan"))


class TestMappa:
    def _b(self):
        return _F["mh394_mappa"](MU, SIG, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["expectile"] == EXP
        assert b["var"] == VAR
        assert b["es"] == ES
        assert b["ratio"] == RATIO
        assert b["verdetto"].startswith("MENO CONSERVATIVO")

    def test_coerenza(self):
        b = self._b()
        assert abs(b["ratio"] - b["expectile"] / b["var"]) < 1e-15

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh394_mappa"](MU, SIG, 2.0)
