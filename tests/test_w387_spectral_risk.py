"""Test tab387 '🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh387_num", "mh387_phi_exp", "mh387_j", "mh387_spectral",
           "mh387_var", "mh387_es", "mh387_spectral_flat",
           "mh387_extra", "mh387_verdetto", "mh387_mappa")

TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
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
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
MU = 0.0
SIG = 10000.0
K = 5.0
ALPHA = 0.99
J_K = 1.0813608715043361
M_K = 10813.608715043361
VAR_ = 23263.47874040841
ES_ = 26652.142203458054
EXTRA = -0.5942686845772449
RATIO = 0.40573131542275503


class TestRegistry387:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 398
        assert "tab387" in dvars
        assert "tab387" in withs

    def test_titoli_allineati_382_383_384_385_386_387(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384
        assert titoli[dvars.index("tab385")] == TITLE385
        assert titoli[dvars.index("tab386")] == TITLE386
        assert titoli[dvars.index("tab387")] == TITLE387

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab398"
        assert titoli[-1] == TITLE398
        assert withs[-1] == "tab398"


class TestNum:
    def test_num_ok(self):
        assert _F["mh387_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_num"](float("inf"), "x")


class TestPhi:
    def test_normalizzazione(self):
        n = 2048
        s = sum(_F["mh387_phi_exp"](K, (i + 0.5) / n)
                for i in range(n)) / n
        assert s == pytest.approx(1.0, abs=1e-6)

    def test_crescente(self):
        assert _F["mh387_phi_exp"](K, 0.2) < _F["mh387_phi_exp"](K, 0.5)
        assert _F["mh387_phi_exp"](K, 0.5) < _F["mh387_phi_exp"](K, 0.9)

    def test_k_piccolo_tende_uniforme(self):
        assert _F["mh387_phi_exp"](1e-6, 0.3) == pytest.approx(1.0, abs=1e-3)
        assert _F["mh387_phi_exp"](1e-6, 0.9) == pytest.approx(1.0, abs=1e-3)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](0.0, 0.5)
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](-2.0, 0.5)

    def test_u_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](K, 0.0)
        with pytest.raises(ValueError):
            _F["mh387_phi_exp"](K, 1.0)


class TestJ:
    def test_demo(self):
        assert _F["mh387_j"](K) == pytest.approx(J_K)

    def test_limite_k_zero(self):
        # k -> 0: phi -> uniforme, J -> integrale z = 0
        assert _F["mh387_j"](1e-9) == pytest.approx(0.0, abs=1e-6)

    def test_crescente(self):
        assert _F["mh387_j"](1.0) < _F["mh387_j"](K)
        assert _F["mh387_j"](K) < _F["mh387_j"](20.0)

    def test_griglia_fine(self):
        assert _F["mh387_j"](K, 8192) == pytest.approx(
            _F["mh387_j"](K), rel=5e-4)

    def test_deterministico(self):
        assert _F["mh387_j"](K) == _F["mh387_j"](K)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_j"](0.0)
        with pytest.raises(ValueError):
            _F["mh387_j"](-1.0)


class TestSpectral:
    def test_demo(self):
        assert _F["mh387_spectral"](K, MU, SIG) == pytest.approx(M_K)

    def test_forma(self):
        assert _F["mh387_spectral"](K, MU, SIG) == pytest.approx(
            MU + SIG * _F["mh387_j"](K))

    def test_maggiore_perdita_attesa(self):
        # J(k) >= 0 -> rho(k) >= mu
        assert _F["mh387_spectral"](K, MU, SIG) >= MU
        assert _F["mh387_spectral"](K, -5000.0, SIG) >= -5000.0

    def test_crescente_k(self):
        assert _F["mh387_spectral"](1.0, MU, SIG) < M_K
        assert M_K < _F["mh387_spectral"](20.0, MU, SIG)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_spectral"](0.0, MU, SIG)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_spectral"](K, MU, -1.0)


class TestFlat:
    def test_uguale_es(self):
        # peso piatto su [alpha, 1] = ES in forma chiusa
        assert _F["mh387_spectral_flat"](ALPHA, MU, SIG) == pytest.approx(
            ES_, rel=1e-4)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh387_spectral_flat"](ALPHA, MU, SIG) == pytest.approx(
            MU + SIG * phi / (1.0 - ALPHA), rel=1e-4)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_spectral_flat"](0.5, MU, SIG)


class TestVarEs:
    def test_demo(self):
        assert _F["mh387_var"](MU, SIG, ALPHA) == pytest.approx(VAR_)
        assert _F["mh387_es"](MU, SIG, ALPHA) == pytest.approx(ES_)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh387_var"](MU, SIG, ALPHA) == pytest.approx(
            MU + SIG * z)
        assert _F["mh387_es"](MU, SIG, ALPHA) == pytest.approx(
            MU + SIG * phi / (1.0 - ALPHA))

    def test_ratio_normale_99(self):
        assert ES_ / VAR_ == pytest.approx(1.1456, abs=1e-3)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_var"](MU, SIG, 0.5)
        with pytest.raises(ValueError):
            _F["mh387_es"](MU, SIG, 1.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_var"](MU, -1.0, ALPHA)


class TestExtraVerdetto:
    def test_demo(self):
        assert _F["mh387_extra"](M_K, ES_) == pytest.approx(EXTRA)
        assert _F["mh387_verdetto"](EXTRA).startswith("MENO CONSERVATIVA")

    def test_bordi(self):
        assert _F["mh387_verdetto"](-0.90).startswith("MENO CONSERVATIVA")
        assert _F["mh387_verdetto"](-0.25).startswith("MENO CONSERVATIVA")
        assert _F["mh387_verdetto"](-0.2499).startswith("IN LINEA")
        assert _F["mh387_verdetto"](0.0999).startswith("IN LINEA")
        assert _F["mh387_verdetto"](0.10).startswith("PRUDENTE")
        assert _F["mh387_verdetto"](0.4999).startswith("PRUDENTE")
        assert _F["mh387_verdetto"](0.50).startswith("ESTREMA")
        assert _F["mh387_verdetto"](math.inf).startswith("ESTREMA")

    def test_extra_inf(self):
        assert _F["mh387_extra"](100.0, 0.0) == math.inf

    def test_extra_zero(self):
        assert _F["mh387_extra"](0.0, 0.0) == 0.0

    def test_es_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_extra"](M_K, -1.0)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh387_verdetto"](float("nan"))


class TestMappa:
    def _b(self):
        return _F["mh387_mappa"](K, MU, SIG, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["k"] == K
        assert b["mu"] == MU
        assert b["sig"] == SIG
        assert b["alpha"] == ALPHA
        assert b["J"] == pytest.approx(J_K)
        assert b["var"] == pytest.approx(VAR_)
        assert b["es"] == pytest.approx(ES_)
        assert b["m"] == pytest.approx(M_K)
        assert b["extra"] == pytest.approx(EXTRA)
        assert b["ratio"] == pytest.approx(RATIO)
        assert b["verdetto"].startswith("MENO CONSERVATIVA")

    def test_coerenza(self):
        b = self._b()
        assert b["m"] == pytest.approx(b["mu"] + b["sig"] * b["J"])
        assert b["extra"] == pytest.approx(b["m"] / b["es"] - 1.0)
        assert b["ratio"] == pytest.approx(b["m"] / b["es"])
