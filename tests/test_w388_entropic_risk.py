"""Test tab388 '🧲📈 Misura entropica: rischio con avversione costante (CARA)': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh388_num", "mh388_entropic", "mh388_entropic_quad",
           "mh388_var", "mh388_es", "mh388_extra",
           "mh388_verdetto", "mh388_mappa")

TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE395 = "🌀 Distortion risk measures: VaR, ES e Wang da un'unica formula"
TITLE396 = "📊 Spectral risk measure: VaR ponderato dal tuo spettro di avversione"
TITLE397 = "🔀 Entropic risk measure: avversione esponenziale al rischio"
TITLE398 = "🎯 Contributi di rischio ES: allocazione di Eulero del portafoglio"
TITLE399 = "🔱 Risk parity: pesi a parità di contributo di rischio (risk budgeting)"
TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
MU = 0.0
SIG = 10000.0
GAMMA = 2e-05
ALPHA = 0.99
RHO = 1000.0
VAR_ = 23263.47874040841
ES_ = 26652.142203458054
EXTRA = -0.9624795638427048
RATIO = 0.03752043615729517


class TestRegistry388:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 399
        assert "tab388" in dvars
        assert "tab388" in withs

    def test_titoli_allineati_383_384_385_386_387_388(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384
        assert titoli[dvars.index("tab385")] == TITLE385
        assert titoli[dvars.index("tab386")] == TITLE386
        assert titoli[dvars.index("tab387")] == TITLE387
        assert titoli[dvars.index("tab388")] == TITLE388

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab399"
        assert titoli[-1] == TITLE399
        assert withs[-1] == "tab399"


class TestNum:
    def test_num_ok(self):
        assert _F["mh388_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_num"](float("inf"), "x")


class TestEntropic:
    def test_demo(self):
        assert _F["mh388_entropic"](GAMMA, MU, SIG) == pytest.approx(RHO)

    def test_forma_chiusa(self):
        assert _F["mh388_entropic"](GAMMA, MU, SIG) == pytest.approx(
            MU + GAMMA * SIG * SIG / 2.0)

    def test_limite_gamma_zero(self):
        # gamma -> 0: rho -> perdita attesa
        assert _F["mh388_entropic"](1e-12, MU, SIG) == pytest.approx(
            MU, abs=1e-3)
        assert _F["mh388_entropic"](1e-12, -5000.0, SIG) == pytest.approx(
            -5000.0, abs=1e-3)

    def test_crescente_gamma(self):
        assert _F["mh388_entropic"](1e-5, MU, SIG) < RHO
        assert RHO < _F["mh388_entropic"](5e-5, MU, SIG)

    def test_jensen(self):
        # gamma > 0 -> rho >= E[L] = mu
        assert _F["mh388_entropic"](GAMMA, MU, SIG) >= MU
        assert _F["mh388_entropic"](GAMMA, -5000.0, SIG) >= -5000.0

    def test_scala(self):
        # raddoppio gamma -> raddoppio penalty gamma*sig^2/2
        assert _F["mh388_entropic"](2 * GAMMA, MU, SIG) - MU == \
            pytest.approx(2 * (RHO - MU))

    def test_gamma_alto_supera_es(self):
        assert _F["mh388_entropic"](1e-3, MU, SIG) > ES_

    def test_gamma_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_entropic"](0.0, MU, SIG)
        with pytest.raises(ValueError):
            _F["mh388_entropic"](-1e-5, MU, SIG)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_entropic"](GAMMA, MU, -1.0)


class TestQuad:
    def test_uguale_forma_chiusa(self):
        assert _F["mh388_entropic_quad"](GAMMA, MU, SIG) == \
            pytest.approx(RHO, rel=1e-6)

    def test_griglia_fine(self):
        assert _F["mh388_entropic_quad"](GAMMA, MU, SIG, 8192) == \
            pytest.approx(_F["mh388_entropic_quad"](GAMMA, MU, SIG),
                          rel=5e-5)

    def test_deterministico(self):
        assert _F["mh388_entropic_quad"](GAMMA, MU, SIG) == \
            _F["mh388_entropic_quad"](GAMMA, MU, SIG)

    def test_sig_zero(self):
        assert _F["mh388_entropic_quad"](GAMMA, MU, 0.0) == pytest.approx(MU)

    def test_gamma_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_entropic_quad"](0.0, MU, SIG)
        with pytest.raises(ValueError):
            _F["mh388_entropic_quad"](-1e-5, MU, SIG)


class TestVarEs:
    def test_demo(self):
        assert _F["mh388_var"](MU, SIG, ALPHA) == pytest.approx(VAR_)
        assert _F["mh388_es"](MU, SIG, ALPHA) == pytest.approx(ES_)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh388_var"](MU, SIG, ALPHA) == pytest.approx(
            MU + SIG * z)
        assert _F["mh388_es"](MU, SIG, ALPHA) == pytest.approx(
            MU + SIG * phi / (1.0 - ALPHA))

    def test_ratio_normale_99(self):
        assert ES_ / VAR_ == pytest.approx(1.1456, abs=1e-3)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_var"](MU, SIG, 0.5)
        with pytest.raises(ValueError):
            _F["mh388_es"](MU, SIG, 1.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_var"](MU, -1.0, ALPHA)


class TestExtraVerdetto:
    def test_demo(self):
        assert _F["mh388_extra"](RHO, ES_) == pytest.approx(EXTRA)
        assert _F["mh388_verdetto"](EXTRA).startswith("MENO CONSERVATIVA")

    def test_bordi(self):
        assert _F["mh388_verdetto"](-0.90).startswith("MENO CONSERVATIVA")
        assert _F["mh388_verdetto"](-0.25).startswith("MENO CONSERVATIVA")
        assert _F["mh388_verdetto"](-0.2499).startswith("IN LINEA")
        assert _F["mh388_verdetto"](0.0999).startswith("IN LINEA")
        assert _F["mh388_verdetto"](0.10).startswith("PRUDENTE")
        assert _F["mh388_verdetto"](0.4999).startswith("PRUDENTE")
        assert _F["mh388_verdetto"](0.50).startswith("ESTREMA")
        assert _F["mh388_verdetto"](math.inf).startswith("ESTREMA")

    def test_extra_inf(self):
        assert _F["mh388_extra"](100.0, 0.0) == math.inf

    def test_extra_zero(self):
        assert _F["mh388_extra"](0.0, 0.0) == 0.0

    def test_es_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_extra"](RHO, -1.0)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh388_verdetto"](float("nan"))


class TestMappa:
    def _b(self):
        return _F["mh388_mappa"](GAMMA, MU, SIG, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["gamma"] == GAMMA
        assert b["mu"] == MU
        assert b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["rho"] == pytest.approx(RHO)
        assert b["var"] == pytest.approx(VAR_)
        assert b["es"] == pytest.approx(ES_)
        assert b["extra"] == pytest.approx(EXTRA)
        assert b["ratio"] == pytest.approx(RATIO)
        assert b["verdetto"].startswith("MENO CONSERVATIVA")

    def test_coerenza(self):
        b = self._b()
        assert b["rho"] == pytest.approx(
            b["mu"] + b["gamma"] * b["sig"] * b["sig"] / 2.0)
        assert b["extra"] == pytest.approx(b["rho"] / b["es"] - 1.0)
        assert b["ratio"] == pytest.approx(b["rho"] / b["es"])
