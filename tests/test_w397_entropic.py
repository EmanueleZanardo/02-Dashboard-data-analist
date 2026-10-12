"""Test tab397 '🔀 Entropic risk measure: avversione esponenziale al rischio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh397_num", "mh397_check_gamma", "mh397_check_alpha",
           "mh397_rho_chiusa", "mh397_rho_quad", "mh397_var_chiusa",
           "mh397_es_chiusa", "mh397_gamma_target", "mh397_benchmarks",
           "mh397_verdetto", "mh397_mappa")

TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
GAMMA = 2e-05
RHO = 1000.0
VAR = 19599.639845400536
ES = 23378.027922014157
GT = 0.00046756055844028306


class TestRegistry397:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 401
        assert "tab397" in dvars
        assert "tab397" in withs

    def test_titoli_allineati_392_393_394_395_396_397(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396
        assert titoli[dvars.index("tab397")] == TITLE397

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab401"
        assert titoli[-1] == TITLE401
        assert withs[-1] == "tab401"


class TestNum:
    def test_num_ok(self):
        assert _F["mh397_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_num"](float("inf"), "x")


class TestCheckGamma:
    @pytest.mark.parametrize("g", [0.0, 2e-5, 1e-3])
    def test_gamma_ok(self, g):
        assert _F["mh397_check_gamma"](g) == g

    @pytest.mark.parametrize("g", [-1e-6, -1.0, True, False, "0.1", None,
                                   float("nan"), float("inf")])
    def test_gamma_ko(self, g):
        with pytest.raises(ValueError):
            _F["mh397_check_gamma"](g)


class TestCheckAlpha:
    @pytest.mark.parametrize("a", [0.5, 0.9, 0.975, 0.99])
    def test_alpha_ok(self, a):
        assert _F["mh397_check_alpha"](a) == a

    @pytest.mark.parametrize("a", [0.0, 1.0, -0.1, 1.5, True, False,
                                   "0.9", None])
    def test_alpha_ko(self, a):
        with pytest.raises(ValueError):
            _F["mh397_check_alpha"](a)

    def test_alpha_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_check_alpha"](float("nan"))


class TestRhoChiusa:
    def test_demo(self):
        assert _F["mh397_rho_chiusa"](MU, SIG, GAMMA) == RHO

    def test_demo_sotto_var(self):
        assert RHO < VAR

    def test_formula(self):
        assert abs(_F["mh397_rho_chiusa"](MU, SIG, GAMMA) -
                   (MU + 0.5 * GAMMA * SIG * SIG)) < 1e-9

    def test_gamma_zero_media(self):
        assert _F["mh397_rho_chiusa"](MU, SIG, 0.0) == MU

    def test_sig_zero(self):
        assert _F["mh397_rho_chiusa"](2000.0, 0.0, GAMMA) == 2000.0

    def test_monotonia_crescente_in_gamma(self):
        rs = [_F["mh397_rho_chiusa"](MU, SIG, g)
              for g in (0.0, 1e-5, 2e-5, 5e-5, 1e-4)]
        assert all(b > a for a, b in zip(rs, rs[1:]))

    def test_traslazione(self):
        assert abs(_F["mh397_rho_chiusa"](5000.0, SIG, GAMMA) -
                   (RHO + 5000.0)) < 1e-6

    def test_scaling_quadratico_in_sig(self):
        assert abs(_F["mh397_rho_chiusa"](MU, 2.0 * SIG, GAMMA) -
                   4.0 * RHO) / RHO < 1e-9

    def test_deterministico(self):
        assert _F["mh397_rho_chiusa"](MU, SIG, GAMMA) == \
            _F["mh397_rho_chiusa"](MU, SIG, GAMMA)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_chiusa"](MU, -1.0, GAMMA)

    def test_gamma_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_chiusa"](MU, SIG, -0.1)


class TestRhoQuad:
    def test_vs_chiusa(self):
        rq = _F["mh397_rho_quad"](MU, SIG, GAMMA)
        assert abs(rq - RHO) / RHO < 1e-6

    def test_gamma_zero(self):
        assert _F["mh397_rho_quad"](MU, SIG, 0.0) == MU

    def test_sig_zero(self):
        assert _F["mh397_rho_quad"](2000.0, 0.0, GAMMA) == 2000.0

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_quad"](MU, SIG, GAMMA, n=4)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_rho_quad"](MU, -1.0, GAMMA)


class TestGammaTarget:
    def test_positivo(self):
        assert GT > 0.0

    def test_eguaglia_es(self):
        assert abs(_F["mh397_rho_chiusa"](MU, SIG, GT) - ES) / ES < 1e-9

    def test_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh397_gamma_target"](SIG, ALPHA) -
                   2.0 * phi / ((1.0 - ALPHA) * SIG)) < 1e-18

    def test_sig_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_gamma_target"](0.0, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_gamma_target"](SIG, 2.0)


class TestEsVarChiusa:
    def test_var_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh397_var_chiusa"](MU, SIG, ALPHA) -
                   (MU + SIG * z)) < 1e-9

    def test_es_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh397_es_chiusa"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_var_chiusa"](MU, -1.0, ALPHA)
        with pytest.raises(ValueError):
            _F["mh397_es_chiusa"](MU, -1.0, ALPHA)


class TestBenchmarks:
    def test_demo(self):
        b = _F["mh397_benchmarks"](MU, SIG, ALPHA)
        assert b["var"] == VAR
        assert b["es"] == ES

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_benchmarks"](MU, -1.0, ALPHA)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh397_verdetto"](RHO, VAR, ES).startswith("SOTTO-VaR")

    def test_bordi(self):
        assert _F["mh397_verdetto"](VAR, VAR, ES).startswith("TRA VaR")
        assert _F["mh397_verdetto"](ES, VAR, ES).startswith("TRA VaR")
        assert _F["mh397_verdetto"](VAR - 1.0, VAR,
                                    ES).startswith("SOTTO-VaR")
        assert _F["mh397_verdetto"](ES + 1.0, VAR,
                                    ES).startswith("OLTRE ES")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_verdetto"](float("nan"), VAR, ES)


class TestMappa:
    def _b(self):
        return _F["mh397_mappa"](MU, SIG, GAMMA, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["alpha"] == ALPHA and b["gamma"] == GAMMA
        assert b["rho"] == RHO
        assert b["var"] == VAR and b["es"] == ES
        assert b["gamma_target"] == GT
        assert b["verdetto"].startswith("SOTTO-VaR")

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh397_mappa"](MU, SIG, GAMMA, 2.0)
