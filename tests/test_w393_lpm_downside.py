"""Test tab393 '🎯📉 LPM: il rischio downside contro un target': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh393_num", "mh393_check_n", "mh393_lpm", "mh393_lpm_quad",
           "mh393_upm", "mh393_share", "mh393_verdetto", "mh393_mappa")

TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
MU = 0.0
SIG = 10000.0
TAU = 0.0
N = 2
LPM2 = 50000000.0
LPM0 = 0.5
LPM1 = 3989.422804014327
SHARE = 0.5


class TestRegistry393:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 395
        assert "tab393" in dvars
        assert "tab393" in withs

    def test_titoli_allineati_388_389_390_391_392_393(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab388")] == TITLE388
        assert titoli[dvars.index("tab389")] == TITLE389
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab395"
        assert titoli[-1] == TITLE395
        assert withs[-1] == "tab395"


class TestNum:
    def test_num_ok(self):
        assert _F["mh393_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_num"](float("inf"), "x")


class TestCheckN:
    @pytest.mark.parametrize("n", [0, 1, 2, 3])
    def test_n_ok(self, n):
        assert _F["mh393_check_n"](n) == n

    @pytest.mark.parametrize("n", [-1, 4, 5, True, False, 1.5, "2", None])
    def test_n_ko(self, n):
        with pytest.raises(ValueError):
            _F["mh393_check_n"](n)


class TestLpm:
    def test_demo_lpm2(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 2) == LPM2

    def test_demo_lpm0(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 0) == LPM0

    def test_demo_lpm1(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 1) == LPM1

    def test_forma_chiusa_n1(self):
        from statistics import NormalDist
        d = (TAU - MU) / SIG
        Phi = NormalDist().cdf(d)
        phi = math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh393_lpm"](MU, SIG, TAU, 1) -
                   SIG * (d * Phi + phi)) < 1e-9

    def test_forma_chiusa_n3(self):
        from statistics import NormalDist
        d = (TAU - MU) / SIG
        Phi = NormalDist().cdf(d)
        phi = math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh393_lpm"](MU, SIG, TAU, 3) -
                   SIG ** 3 * ((d ** 3 + 3.0 * d) * Phi +
                               (d * d + 2.0) * phi)) < 1e-9

    @pytest.mark.parametrize("n", [0, 1, 2, 3])
    @pytest.mark.parametrize("pt", [(0.0, 10000.0, 0.0),
                                    (2000.0, 8000.0, 5000.0)])
    def test_quad_crosscheck(self, n, pt):
        mu, sg, ta = pt
        c = _F["mh393_lpm"](mu, sg, ta, n)
        q = _F["mh393_lpm_quad"](mu, sg, ta, n)
        assert abs(c - q) / max(abs(c), 1e-12) < 1e-6

    def test_monotonia_tau(self):
        assert _F["mh393_lpm"](MU, SIG, -5000.0, 2) < \
            _F["mh393_lpm"](MU, SIG, 0.0, 2) < \
            _F["mh393_lpm"](MU, SIG, 5000.0, 2)

    def test_lpm0_in_unit(self):
        assert 0.0 <= _F["mh393_lpm"](MU, SIG, TAU, 0) <= 1.0
        assert _F["mh393_lpm"](MU, SIG, 1e9, 0) > 0.999999
        assert _F["mh393_lpm"](MU, SIG, -1e9, 0) < 1e-6

    def test_sig_zero_n0(self):
        assert _F["mh393_lpm"](2000.0, 0.0, 1000.0, 0) == 1.0
        assert _F["mh393_lpm"](2000.0, 0.0, 3000.0, 0) == 0.0

    def test_sig_zero_n2(self):
        assert _F["mh393_lpm"](2000.0, 0.0, 5000.0, 2) == 3000.0 ** 2
        assert _F["mh393_lpm"](2000.0, 0.0, 1000.0, 2) == 0.0

    def test_traslazione(self):
        assert _F["mh393_lpm"](5000.0, SIG, 5000.0, 2) == \
            _F["mh393_lpm"](MU, SIG, TAU, 2)

    def test_scaling(self):
        assert _F["mh393_lpm"](MU, 2 * SIG, TAU, 2) == \
            4.0 * _F["mh393_lpm"](MU, SIG, TAU, 2)

    def test_deterministico(self):
        assert _F["mh393_lpm"](MU, SIG, TAU, 3) == \
            _F["mh393_lpm"](MU, SIG, TAU, 3)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, SIG, TAU, 4)

    def test_n_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, SIG, TAU, True)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, -1.0, TAU, 2)

    def test_tau_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm"](MU, SIG, float("nan"), 2)

    def test_quad_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_lpm_quad"](MU, SIG, TAU, 5)


class TestUpmShare:
    def test_simmetria(self):
        assert _F["mh393_upm"](MU, SIG, TAU) == \
            _F["mh393_lpm"](MU, SIG, TAU, 1)

    def test_demo_share(self):
        assert _F["mh393_share"](MU, SIG, TAU) == SHARE

    def test_share_banda(self):
        s = _F["mh393_share"](2000.0, 8000.0, 5000.0)
        assert 0.0 <= s <= 1.0

    def test_share_tau_alto(self):
        assert _F["mh393_share"](MU, SIG, 20000.0) > 0.9

    def test_share_tau_basso(self):
        assert _F["mh393_share"](MU, SIG, -20000.0) < 0.1

    def test_upm_sig_zero(self):
        assert _F["mh393_upm"](5000.0, 0.0, 2000.0) == 3000.0
        assert _F["mh393_upm"](5000.0, 0.0, 8000.0) == 0.0

    def test_share_degenere(self):
        assert _F["mh393_share"](2000.0, 0.0, 2000.0) == 0.5

    def test_upm_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_upm"](MU, -1.0, TAU)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh393_verdetto"](LPM0).startswith("TARGET BILANCIATO")

    def test_bordi(self):
        assert _F["mh393_verdetto"](0.30).startswith("TARGET CONSERVATIVO")
        assert _F["mh393_verdetto"](0.3001).startswith("TARGET BILANCIATO")
        assert _F["mh393_verdetto"](0.60).startswith("TARGET BILANCIATO")
        assert _F["mh393_verdetto"](0.6001).startswith("TARGET AGGRESSIVO")
        assert _F["mh393_verdetto"](0.0).startswith("TARGET CONSERVATIVO")
        assert _F["mh393_verdetto"](1.0).startswith("TARGET AGGRESSIVO")

    def test_clamp(self):
        assert _F["mh393_verdetto"](-0.5).startswith("TARGET CONSERVATIVO")
        assert _F["mh393_verdetto"](1.5).startswith("TARGET AGGRESSIVO")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_verdetto"](float("nan"))

    def test_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_verdetto"](float("inf"))

    def test_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_verdetto"](True)


class TestMappa:
    def _b(self):
        return _F["mh393_mappa"](MU, SIG, TAU, N)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["tau"] == TAU and b["n"] == N
        assert b["lpm0"] == LPM0
        assert b["lpm1"] == LPM1
        assert b["lpm2"] == LPM2
        assert b["lpm_n"] == LPM2
        assert b["share"] == SHARE
        assert b["verdetto"].startswith("TARGET BILANCIATO")

    def test_coerenza(self):
        b = self._b()
        assert abs(b["down_std"] - math.sqrt(b["lpm2"])) < 1e-9
        assert abs(b["share"] - b["lpm1"] / (b["lpm1"] + b["upm1"])) < 1e-15
        assert b["lpm_n"] == b["lpm2"]

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh393_mappa"](MU, SIG, TAU, 7)
