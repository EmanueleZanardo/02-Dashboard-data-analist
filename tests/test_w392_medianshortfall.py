"""Test tab392 '🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh392_num", "mh392_var", "mh392_es", "mh392_ms", "mh392_ms_bis",
           "mh392_ratio", "mh392_verdetto", "mh392_mappa", "mh392_robust")

TITLE392 = "🎯📊 Median Shortfall: la mediana della coda, robusta tra VaR ed ES"
TITLE393 = "🎯📉 LPM: il rischio downside contro un target"
TITLE394 = "📐⚖ Expectile: la misura di rischio elicitabile e coerente"
TITLE391 = "🔀📊 RVaR: la media dei quantili tra VaR ed ES"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
MS = 22414.027276049463
VAR_ = 19599.639845400536
ES_ = 23378.027922014157
RATIO = 0.9587646721451243


class TestRegistry392:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 394
        assert "tab392" in dvars
        assert "tab392" in withs

    def test_titoli_allineati_387_388_389_390_391_392(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab387")] == TITLE387
        assert titoli[dvars.index("tab388")] == TITLE388
        assert titoli[dvars.index("tab389")] == TITLE389
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391
        assert titoli[dvars.index("tab392")] == TITLE392

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab394"
        assert titoli[-1] == TITLE394
        assert withs[-1] == "tab394"


class TestNum:
    def test_num_ok(self):
        assert _F["mh392_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_num"](float("inf"), "x")


class TestVarEs:
    def test_var_demo(self):
        assert _F["mh392_var"](MU, SIG, ALPHA) == VAR_

    def test_var_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh392_var"](MU, SIG, ALPHA) - (MU + SIG * z)) < 1e-9

    def test_var_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_var"](MU, SIG, 0.5)

    def test_var_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_var"](MU, -1.0, ALPHA)

    def test_es_demo(self):
        assert _F["mh392_es"](MU, SIG, ALPHA) == ES_

    def test_es_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh392_es"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_es_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_es"](MU, SIG, 1.0)

    def test_es_sig_zero(self):
        assert _F["mh392_es"](2000.0, 0.0, ALPHA) == 2000.0

    def test_es_supera_var(self):
        assert _F["mh392_es"](MU, SIG, ALPHA) > _F["mh392_var"](MU, SIG,
                                                               ALPHA)


class TestMs:
    def test_demo(self):
        assert _F["mh392_ms"](MU, SIG, ALPHA) == MS

    def test_forma_chiusa(self):
        from statistics import NormalDist
        q = NormalDist().inv_cdf(1.0 - (1.0 - ALPHA) / 2.0)
        assert abs(_F["mh392_ms"](MU, SIG, ALPHA) - (MU + SIG * q)) < 1e-9

    def test_bis_crosscheck(self):
        b = _F["mh392_ms_bis"](MU, SIG, ALPHA)
        assert abs(b - MS) / MS < 1e-9

    def test_bis_altro_punto(self):
        b = _F["mh392_ms_bis"](MU, SIG, 0.99)
        c = _F["mh392_ms"](MU, SIG, 0.99)
        assert abs(b - c) / c < 1e-9

    def test_sandwich(self):
        assert VAR_ <= MS <= ES_

    def test_traslazione(self):
        assert abs(_F["mh392_ms"](5000.0, SIG, ALPHA) -
                   (MS + 5000.0)) < 1e-9

    def test_scaling(self):
        assert abs(_F["mh392_ms"](0.0, 2 * SIG, ALPHA) -
                   2 * MS) < 1e-9

    def test_sig_zero(self):
        assert _F["mh392_ms"](2000.0, 0.0, ALPHA) == 2000.0

    def test_bis_sig_zero(self):
        assert _F["mh392_ms_bis"](2000.0, 0.0, ALPHA) == 2000.0

    def test_deterministico(self):
        assert _F["mh392_ms"](MU, SIG, ALPHA) == \
            _F["mh392_ms"](MU, SIG, ALPHA)

    def test_alpha_basso_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_ms"](MU, SIG, 0.4)

    def test_alpha_uno_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_ms"](MU, SIG, 1.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_ms"](MU, -1.0, ALPHA)

    def test_bis_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_ms_bis"](MU, SIG, 1.0)


class TestRatioVerdetto:
    def test_demo(self):
        assert _F["mh392_ratio"](MS, ES_) == RATIO

    def test_banda_intermedia(self):
        assert 0.90 < RATIO <= 0.97

    def test_bordi(self):
        assert _F["mh392_verdetto"](0.90).startswith("VICINA AL VaR")
        assert _F["mh392_verdetto"](0.9001).startswith("INTERMEDIA")
        assert _F["mh392_verdetto"](0.97).startswith("INTERMEDIA")
        assert _F["mh392_verdetto"](0.9701).startswith("VICINA ALL'ES")
        assert _F["mh392_verdetto"](0.0).startswith("VICINA AL VaR")
        assert _F["mh392_verdetto"](1.0).startswith("VICINA ALL'ES")

    def test_clamp(self):
        assert _F["mh392_verdetto"](-0.5).startswith("VICINA AL VaR")
        assert _F["mh392_verdetto"](1.5).startswith("VICINA ALL'ES")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_verdetto"](float("nan"))

    def test_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_verdetto"](float("inf"))

    def test_es_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_ratio"](MS, 0.0)


class TestMappa:
    def _b(self):
        return _F["mh392_mappa"](MU, SIG, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["var"] == VAR_
        assert b["es"] == ES_
        assert b["ms"] == MS
        assert b["ratio"] == RATIO
        assert b["alpha"] == ALPHA
        assert b["verdetto"].startswith("INTERMEDIA")

    def test_coerenza(self):
        b = self._b()
        assert b["var"] <= b["ms"] <= b["es"]
        assert abs(b["ratio"] - b["ms"] / b["es"]) < 1e-15


class TestRobust:
    def _r(self):
        return _F["mh392_robust"](SIG)

    def test_deterministico(self):
        assert self._r() == self._r()

    def test_n_tail(self):
        assert self._r()["n_tail"] == 50

    def test_spike(self):
        assert self._r()["spike_eur"] == 15.0 * SIG

    def test_es_salta(self):
        r = self._r()
        assert r["delta_es"] > 1000.0

    def test_ms_stabile(self):
        r = self._r()
        assert abs(r["delta_ms"]) < 500.0

    def test_sig_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_robust"](0.0)

    def test_n_piccolo_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_robust"](SIG, 199)

    def test_n_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_robust"](SIG, True)

    def test_spike_mult_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_robust"](SIG, 2000, 0.0)

    def test_seed_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh392_robust"](SIG, 2000, 15.0, True)
