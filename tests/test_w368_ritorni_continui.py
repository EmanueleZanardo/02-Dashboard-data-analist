"""Test tab368 'Kelly su ritorni continui: f* = μ/σ² e volatility drag': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh368_num", "mh368_fstar", "mh368_growth", "mh368_vol_log",
           "mh368_sharpe", "mh368_drag", "mh368_curva", "mh368_verdetto",
           "mh368_analisi")

TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
MU = 0.02
SIGMA = 0.1
CAP = 1.0
FSTAR = 1.9999999999999996
GSTAR = 0.020000000000000004
GEFF = 0.015
VOLSTAR = 0.19999999999999996
VOLEFF = 0.1
SHARPE = 0.19999999999999998
DRAG = 0.005000000000000001
VERDETTO = 'CAP VINCOLANTE: f* = 200% supera il tuo limite 100%: applichi il cap e accetti una crescita ridotta; valuta se alzare il limite o ridurre la size.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry368:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 374
        assert "tab368" in dvars
        assert "tab368" in withs

    def test_titoli_allineati_363_364_365_366_367_368(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab363")] == TITLE363
        assert titoli[dvars.index("tab364")] == TITLE364
        assert titoli[dvars.index("tab365")] == TITLE365
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab374"
        assert titoli[-1] == TITLE374
        assert withs[-1] == "tab374"


class TestNum:
    def test_num_ok(self):
        assert _F["mh368_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_num"](float("inf"), "x")


class TestFstar:
    def test_demo(self):
        assert _F["mh368_fstar"](MU, SIGMA) == pytest.approx(FSTAR)

    def test_forma_chiusa(self):
        assert _F["mh368_fstar"](0.03, 0.15) == pytest.approx(0.03 / 0.0225)

    def test_no_edge(self):
        assert _F["mh368_fstar"](-0.01, SIGMA) == 0.0

    def test_mu_zero(self):
        assert _F["mh368_fstar"](0.0, SIGMA) == 0.0

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_fstar"](MU, 0.0)


class TestGrowth:
    def test_demo_star(self):
        assert _F["mh368_growth"](FSTAR, MU, SIGMA) == pytest.approx(GSTAR)

    def test_demo_eff(self):
        assert _F["mh368_growth"](min(FSTAR, CAP), MU,
                                 SIGMA) == pytest.approx(GEFF)

    def test_forma_chiusa(self):
        f, mu, sg = 0.5, 0.02, 0.10
        assert _F["mh368_growth"](f, mu, sg) == pytest.approx(
            f * mu - 0.5 * (f * sg) ** 2)

    def test_f_zero(self):
        assert _F["mh368_growth"](0.0, MU, SIGMA) == pytest.approx(0.0)

    def test_massimo_in_fstar(self):
        # g(f) e' concava: il max e' in f*
        fs = [i * 0.05 for i in range(81)]
        gs = [_F["mh368_growth"](f, MU, SIGMA) for f in fs]
        assert fs[gs.index(max(gs))] == pytest.approx(FSTAR, abs=0.05)

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_growth"](-0.1, MU, SIGMA)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_growth"](0.5, MU, 0.0)


class TestVolLog:
    def test_demo_star(self):
        assert _F["mh368_vol_log"](FSTAR, SIGMA) == pytest.approx(VOLSTAR)

    def test_demo_eff(self):
        assert _F["mh368_vol_log"](min(FSTAR, CAP),
                                   SIGMA) == pytest.approx(VOLEFF)

    def test_lineare_in_f(self):
        assert _F["mh368_vol_log"](0.5, SIGMA) == pytest.approx(0.5 * SIGMA)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_vol_log"](0.5, -0.1)


class TestSharpe:
    def test_demo(self):
        assert _F["mh368_sharpe"](MU, SIGMA) == pytest.approx(SHARPE)

    def test_forma_chiusa(self):
        assert _F["mh368_sharpe"](0.03, 0.15) == pytest.approx(0.2)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_sharpe"](MU, 0.0)


class TestDrag:
    def test_demo(self):
        assert _F["mh368_drag"](SIGMA) == pytest.approx(DRAG)

    def test_forma_chiusa(self):
        assert _F["mh368_drag"](0.20) == pytest.approx(0.02)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_drag"](0.0)


class TestCurva:
    def _cv(self):
        return _F["mh368_curva"](2.5, MU, SIGMA, 81)

    def test_dimensioni(self):
        cv = self._cv()
        assert len(cv["fs"]) == 81
        assert len(cv["gs"]) == 81

    def test_estremi(self):
        cv = self._cv()
        assert cv["fs"][0] == pytest.approx(0.0)
        assert cv["fs"][-1] == pytest.approx(2.5)
        assert cv["gs"][0] == pytest.approx(0.0)

    def test_coerente_con_growth(self):
        cv = self._cv()
        for f, g in zip(cv["fs"][::10], cv["gs"][::10]):
            assert g == pytest.approx(_F["mh368_growth"](f, MU, SIGMA))

    def test_massimo_vicino_fstar(self):
        cv = self._cv()
        imax = cv["gs"].index(max(cv["gs"]))
        assert cv["fs"][imax] == pytest.approx(FSTAR, abs=2.5 / 80 + 1e-9)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_curva"](2.5, MU, SIGMA, 1)

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_curva"](0.0, MU, SIGMA, 81)


class TestVerdetto:
    def test_nessun_edge_mu(self):
        assert _F["mh368_verdetto"](0.0, CAP, -0.01).startswith("NESSUN EDGE")

    def test_nessun_edge_fstar(self):
        assert _F["mh368_verdetto"](0.0, CAP, 0.0).startswith("NESSUN EDGE")

    def test_cap_vincolante(self):
        assert _F["mh368_verdetto"](2.0, 1.0, 0.02).startswith(
            "CAP VINCOLANTE")

    def test_sizing_pieno(self):
        assert _F["mh368_verdetto"](0.95, 1.0, 0.02).startswith("SIZING PIENO")

    def test_sizing_pieno_al_limite(self):
        # f* == cap: non supera il cap -> PIENO
        assert _F["mh368_verdetto"](1.0, 1.0, 0.02).startswith("SIZING PIENO")

    def test_sotto_sizing(self):
        assert _F["mh368_verdetto"](0.5, 1.0, 0.02).startswith(
            "SOTTO-SIZING OK")

    def test_cap_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_verdetto"](0.5, 0.0, 0.02)


class TestAnalisi:
    def _demo(self):
        return _F["mh368_analisi"](MU, SIGMA, CAP)

    def test_demo(self):
        a = self._demo()
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["f_eff"] == pytest.approx(min(FSTAR, CAP))
        assert a["g_star"] == pytest.approx(GSTAR)
        assert a["g_eff"] == pytest.approx(GEFF)
        assert a["vol_star"] == pytest.approx(VOLSTAR)
        assert a["vol_eff"] == pytest.approx(VOLEFF)
        assert a["sharpe"] == pytest.approx(SHARPE)
        assert a["drag"] == pytest.approx(DRAG)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("CAP VINCOLANTE")
        assert len(a["curva"]["fs"]) == 81

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["f_star"] == a2["f_star"]

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_analisi"](MU, 0.0, CAP)

    def test_cap_ko(self):
        with pytest.raises(ValueError):
            _F["mh368_analisi"](MU, SIGMA, 0.0)
