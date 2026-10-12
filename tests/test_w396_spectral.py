"""Test tab396 '📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh396_num", "mh396_check_alpha", "mh396_check_spec",
           "mh396_check_param", "_mh396_support", "mh396_phi",
           "mh396_rho", "mh396_es_chiusa", "mh396_var_chiusa",
           "mh396_crescente_ok", "mh396_benchmarks", "mh396_verdetto",
           "mh396_mappa")

TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE400 = "🎯 Numero effettivo di scommesse (ENB): quante posizioni indipendenti hai davvero?"
TITLE401 = "📈 Massima diversificazione (MD): i pesi che massimizzano il rapporto DR"
TITLE402 = "🛡️ Minima varianza (MV): i pesi che minimizzano la volatilità di portafoglio"
TITLE403 = "🎯 Sharpe massimo (MS): i pesi che massimizzano il rendimento per unità di rischio"
TITLE404 = "🎯 Rendimento target (TR): minima varianza a rendimento atteso fissato"
TITLE405 = "κ Kappa ratio: un'unica famiglia per Omega e Sortino"
TITLE406 = "📏 Tail ratio: la coda destra contro la sinistra"
TITLE407 = "🔄 Recovery factor: quanto rende ogni euro di drawdown"
TITLE408 = "💢 Pain index: il dolore che serve per il rendimento"
TITLE409 = "🛟 Sterling ratio: quanto rende contro i K peggiori drawdown"
TITLE410 = "⚖ Gain-to-Pain ratio: quanto guadagno per ogni euro perso"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
SPEC = 'power'
PARAM = 3.0
RHO = 10292.936010217903
VAR = 19599.639845400536
ES = 23378.027922014157
_SPECS = ("es", "step", "power", "exp")
_PAR = {"es": None, "step": 0.99, "power": 3.0, "exp": 2.0}


class TestRegistry396:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 410
        assert "tab396" in dvars
        assert "tab396" in withs

    def test_titoli_allineati_391_392_393_394_395_396(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392
        assert titoli[dvars.index("tab393")] == TITLE393
        assert titoli[dvars.index("tab394")] == TITLE394
        assert titoli[dvars.index("tab395")] == TITLE395
        assert titoli[dvars.index("tab396")] == TITLE396

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab410"
        assert titoli[-1] == TITLE410
        assert withs[-1] == "tab410"


class TestNum:
    def test_num_ok(self):
        assert _F["mh396_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_num"](float("inf"), "x")


class TestCheckAlpha:
    @pytest.mark.parametrize("a", [0.5, 0.9, 0.975, 0.99])
    def test_alpha_ok(self, a):
        assert _F["mh396_check_alpha"](a) == a

    @pytest.mark.parametrize("a", [0.0, 1.0, -0.1, 1.5, True, False,
                                   "0.9", None])
    def test_alpha_ko(self, a):
        with pytest.raises(ValueError):
            _F["mh396_check_alpha"](a)

    def test_alpha_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_check_alpha"](float("nan"))


class TestSpecParam:
    @pytest.mark.parametrize("sp", ["es", "step", "power", "exp"])
    def test_spec_ok(self, sp):
        assert _F["mh396_check_spec"](sp) == sp

    @pytest.mark.parametrize("sp", ["x", "", None, 5, True])
    def test_spec_ko(self, sp):
        with pytest.raises(ValueError):
            _F["mh396_check_spec"](sp)

    def test_param_es_ignorato(self):
        assert _F["mh396_check_param"]("es", "qualsiasi") is None
        assert _F["mh396_check_param"]("es", 999) is None

    @pytest.mark.parametrize("p", [0.5, 0.99, 1.0])
    def test_param_step_ok(self, p):
        assert _F["mh396_check_param"]("step", p) == p

    @pytest.mark.parametrize("p", [0.0, -0.5, 1.5, float("nan"),
                                   float("inf"), "0.9", True])
    def test_param_step_ko(self, p):
        with pytest.raises(ValueError):
            _F["mh396_check_param"]("step", p)

    @pytest.mark.parametrize("p", [0.0, 1.0, 3.0])
    def test_param_power_ok(self, p):
        assert _F["mh396_check_param"]("power", p) == p

    @pytest.mark.parametrize("p", [-0.1, float("nan"), float("inf")])
    def test_param_power_ko(self, p):
        with pytest.raises(ValueError):
            _F["mh396_check_param"]("power", p)

    @pytest.mark.parametrize("p", [0.0, 2.0, 6.0])
    def test_param_exp_ok(self, p):
        assert _F["mh396_check_param"]("exp", p) == p

    @pytest.mark.parametrize("p", [-1.0, float("nan"), float("inf")])
    def test_param_exp_ko(self, p):
        with pytest.raises(ValueError):
            _F["mh396_check_param"]("exp", p)


class TestSupport:
    def test_es(self):
        assert _F["_mh396_support"]("es", None, ALPHA) == (ALPHA, 1.0)

    def test_step(self):
        assert _F["_mh396_support"]("step", 0.99, ALPHA) == (ALPHA, 0.99)

    def test_step_beta_minore_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["_mh396_support"]("step", 0.5, ALPHA)

    def test_power_exp(self):
        assert _F["_mh396_support"]("power", 3.0, ALPHA) == (0.0, 1.0)
        assert _F["_mh396_support"]("exp", 2.0, ALPHA) == (0.0, 1.0)


class TestPhi:
    def test_power_valore_noto(self):
        assert _F["mh396_phi"](0.5, "power", 3.0, ALPHA) == 0.5

    def test_power_k0_uno(self):
        assert _F["mh396_phi"](0.37, "power", 0.0, ALPHA) == 1.0

    def test_exp_lambda0_uno(self):
        assert _F["mh396_phi"](0.37, "exp", 0.0, ALPHA) == 1.0

    def test_es_valore_noto(self):
        assert abs(_F["mh396_phi"](0.99, "es", None, ALPHA) - 40.0) < 1e-9
        assert _F["mh396_phi"](0.5, "es", None, ALPHA) == 0.0

    def test_step_valore_noto(self):
        assert abs(_F["mh396_phi"](0.98, "step", 0.99, ALPHA) -
                   1.0 / 0.015) < 1e-12
        assert _F["mh396_phi"](0.5, "step", 0.99, ALPHA) == 0.0

    @pytest.mark.parametrize("sp", ["es", "step", "power", "exp"])
    def test_normalizzazione(self, sp):
        lo, hi = _F["_mh396_support"](sp, _PAR[sp], ALPHA)
        n = 20001
        tot = sum(_F["mh396_phi"](lo + (hi - lo) * (i + 0.5) / n,
                                  sp, _PAR[sp], ALPHA)
                  for i in range(n))
        assert abs(tot * (hi - lo) / n - 1.0) < 1e-6

    @pytest.mark.parametrize("u", [-0.1, 1.1, float("nan")])
    def test_u_ko(self, u):
        with pytest.raises(ValueError):
            _F["mh396_phi"](u, "power", 3.0, ALPHA)

    def test_step_beta_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_phi"](0.5, "step", 0.5, ALPHA)

    def test_spec_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_phi"](0.5, "xx", None, ALPHA)


class TestRho:
    def test_demo(self):
        assert _F["mh396_rho"](MU, SIG, SPEC, PARAM, ALPHA) == RHO

    def test_demo_sotto_var(self):
        assert RHO < VAR

    def test_es_vs_chiusa(self):
        r = _F["mh396_rho"](MU, SIG, "es", None, ALPHA)
        assert abs(r - ES) / SIG < 1e-4

    def test_step_beta1_uguale_es(self):
        assert _F["mh396_rho"](MU, SIG, "step", 1.0, ALPHA) == \
            _F["mh396_rho"](MU, SIG, "es", None, ALPHA)

    def test_power0_media(self):
        assert abs(_F["mh396_rho"](MU, SIG, "power", 0.0, ALPHA) - MU) < 1e-6

    def test_exp0_media(self):
        assert abs(_F["mh396_rho"](MU, SIG, "exp", 0.0, ALPHA) - MU) < 1e-6

    def test_step_demo_tra_var_ed_es(self):
        r = _F["mh396_rho"](MU, SIG, "step", 0.99, ALPHA)
        assert VAR < r < ES

    def test_monotonia_crescente_in_k(self):
        rs = [_F["mh396_rho"](MU, SIG, "power", k, ALPHA)
              for k in (0.5, 1.0, 2.0, 3.0, 5.0)]
        assert all(b > a > MU for a, b in zip(rs, rs[1:]))

    def test_monotonia_crescente_in_lambda(self):
        rs = [_F["mh396_rho"](MU, SIG, "exp", l, ALPHA)
              for l in (0.5, 1.0, 2.0, 4.0)]
        assert all(b > a > MU for a, b in zip(rs, rs[1:]))

    @pytest.mark.parametrize("sp", ["es", "step", "power", "exp"])
    def test_sig_zero(self, sp):
        assert _F["mh396_rho"](2000.0, 0.0, sp, _PAR[sp], ALPHA) == 2000.0

    def test_traslazione(self):
        assert abs(_F["mh396_rho"](5000.0, SIG, SPEC, PARAM, ALPHA) -
                   (RHO + 5000.0)) < 1e-3

    def test_scaling_mu_zero(self):
        assert abs(_F["mh396_rho"](MU, 2.0 * SIG, SPEC, PARAM, ALPHA) -
                   2.0 * RHO) < 1e-6

    def test_deterministico(self):
        assert _F["mh396_rho"](MU, SIG, "power", 3.0, ALPHA) == \
            _F["mh396_rho"](MU, SIG, "power", 3.0, ALPHA)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_rho"](MU, -1.0, SPEC, PARAM, ALPHA)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_rho"](MU, SIG, SPEC, PARAM, ALPHA, n=4)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_rho"](MU, SIG, SPEC, PARAM, 2.0)

    def test_spec_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_rho"](MU, SIG, "xx", PARAM, ALPHA)


class TestEsChiusa:
    def test_demo(self):
        assert _F["mh396_es_chiusa"](MU, SIG, ALPHA) == ES

    def test_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh396_es_chiusa"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_var_formula(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh396_var_chiusa"](MU, SIG, ALPHA) -
                   (MU + SIG * z)) < 1e-9

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_es_chiusa"](MU, -1.0, ALPHA)


class TestCrescente:
    @pytest.mark.parametrize("sp", ["es", "step", "power", "exp"])
    def test_crescente(self, sp):
        assert _F["mh396_crescente_ok"](sp, _PAR[sp], ALPHA) is True

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_crescente_ok"]("es", None, ALPHA, n=4)


class TestBenchmarks:
    def test_demo(self):
        b = _F["mh396_benchmarks"](MU, SIG, ALPHA)
        assert b["var"] == VAR
        assert b["es"] == ES

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_benchmarks"](MU, -1.0, ALPHA)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh396_verdetto"](RHO, VAR, ES).startswith("SOTTO-VaR")

    def test_bordi(self):
        assert _F["mh396_verdetto"](VAR, VAR, ES).startswith("TRA VaR")
        assert _F["mh396_verdetto"](ES, VAR, ES).startswith("TRA VaR")
        assert _F["mh396_verdetto"](VAR - 1.0, VAR,
                                    ES).startswith("SOTTO-VaR")
        assert _F["mh396_verdetto"](ES + 1.0, VAR,
                                    ES).startswith("OLTRE ES")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_verdetto"](float("nan"), VAR, ES)


class TestMappa:
    def _b(self):
        return _F["mh396_mappa"](MU, SIG, SPEC, PARAM, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["mu"] == MU and b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["spec"] == SPEC and b["param"] == PARAM
        assert b["rho"] == RHO
        assert b["var"] == VAR and b["es"] == ES
        assert b["coerente"] is True
        assert b["verdetto"].startswith("SOTTO-VaR")

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh396_mappa"](MU, SIG, SPEC, PARAM, 2.0)
