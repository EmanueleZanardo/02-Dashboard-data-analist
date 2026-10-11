"""Test tab369 'Kelly con costi di transazione: f* netto = (μ-c)/σ²': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh369_num", "mh369_fstar_lordo", "mh369_fstar_netto",
           "mh369_growth_lordo", "mh369_growth_netto", "mh369_vol_log",
           "mh369_sharpe", "mh369_breakeven", "mh369_edge_tax",
           "mh369_curva", "mh369_verdetto", "mh369_analisi")

TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
MU = 0.02
SIGMA = 0.1
C = 0.003
CAP = 1.0
FLORDO = 1.9999999999999996
FNETTO = 1.6999999999999997
GNETTO_STAR = 0.014450000000000001
GNETTO_EFF = 0.012
GLORDO_EFF = 0.015
VOLEFF = 0.1
SHARPE = 0.19999999999999998
BREAKEVEN = 0.003
VERDETTO = 'CAP VINCOLANTE: f*_netto = 170% supera il tuo limite 100%: applichi il cap e accetti una crescita netta ridotta; valuta se alzare il limite, ridurre la size o tagliare i costi di transazione.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry369:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 373
        assert "tab369" in dvars
        assert "tab369" in withs

    def test_titoli_allineati_364_365_366_367_368_369(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab364")] == TITLE364
        assert titoli[dvars.index("tab365")] == TITLE365
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab373"
        assert titoli[-1] == TITLE373
        assert withs[-1] == "tab373"


class TestNum:
    def test_num_ok(self):
        assert _F["mh369_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_num"](float("inf"), "x")


class TestFstar:
    def test_demo_lordo(self):
        assert _F["mh369_fstar_lordo"](MU, SIGMA) == pytest.approx(FLORDO)

    def test_demo_netto(self):
        assert _F["mh369_fstar_netto"](MU, SIGMA, C) == pytest.approx(FNETTO)

    def test_forma_chiusa_netto(self):
        assert _F["mh369_fstar_netto"](0.03, 0.15, 0.003) == pytest.approx(
            (0.03 - 0.003) / 0.0225)

    def test_no_edge_netto(self):
        # mu == c -> f*_netto = 0
        assert _F["mh369_fstar_netto"](C, SIGMA, C) == 0.0

    def test_mu_sotto_costo(self):
        assert _F["mh369_fstar_netto"](0.001, SIGMA, C) == 0.0

    def test_c_zero_torna_lordo(self):
        assert _F["mh369_fstar_netto"](MU, SIGMA, 0.0) == pytest.approx(
            _F["mh369_fstar_lordo"](MU, SIGMA))

    def test_c_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_fstar_netto"](MU, SIGMA, -0.001)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_fstar_netto"](MU, 0.0, C)


class TestGrowthNetto:
    def test_demo_star(self):
        assert _F["mh369_growth_netto"](FNETTO, MU, SIGMA,
                                        C) == pytest.approx(GNETTO_STAR)

    def test_demo_eff(self):
        assert _F["mh369_growth_netto"](min(FNETTO, CAP), MU, SIGMA,
                                        C) == pytest.approx(GNETTO_EFF)

    def test_forma_chiusa(self):
        f, mu, sg, c = 0.5, 0.02, 0.10, 0.003
        assert _F["mh369_growth_netto"](f, mu, sg, c) == pytest.approx(
            f * (mu - c) - 0.5 * (f * sg) ** 2)

    def test_netto_minore_lordo(self):
        # c > 0: la curva netta sta sempre sotto la lorda
        for f in (0.0, 0.5, 1.0, 1.7):
            assert _F["mh369_growth_netto"](f, MU, SIGMA, C) <= \
                _F["mh369_growth_lordo"](f, MU, SIGMA)

    def test_massimo_in_fnetto(self):
        # g_netta(f) e' concava: il max e' in f*_netto
        fs = [i * 0.05 for i in range(81)]
        gs = [_F["mh369_growth_netto"](f, MU, SIGMA, C) for f in fs]
        assert fs[gs.index(max(gs))] == pytest.approx(FNETTO, abs=0.05)

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_growth_netto"](-0.1, MU, SIGMA, C)

    def test_c_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_growth_netto"](0.5, MU, SIGMA, -0.001)


class TestVolLog:
    def test_demo_eff(self):
        assert _F["mh369_vol_log"](min(FNETTO, CAP),
                                   SIGMA) == pytest.approx(VOLEFF)

    def test_lineare_in_f(self):
        assert _F["mh369_vol_log"](0.5, SIGMA) == pytest.approx(0.5 * SIGMA)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_vol_log"](0.5, -0.1)


class TestSharpeBreakeven:
    def test_demo_sharpe(self):
        assert _F["mh369_sharpe"](MU, SIGMA) == pytest.approx(SHARPE)

    def test_demo_breakeven(self):
        assert _F["mh369_breakeven"](C) == pytest.approx(BREAKEVEN)

    def test_breakeven_uguale_c(self):
        assert _F["mh369_breakeven"](0.005) == pytest.approx(0.005)

    def test_edge_tax_demo(self):
        assert _F["mh369_edge_tax"](MU, C) == pytest.approx(C / MU)

    def test_edge_tax_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_edge_tax"](0.0, C)

    def test_c_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_breakeven"](-0.001)


class TestCurva:
    def _cv(self):
        return _F["mh369_curva"](2.5, MU, SIGMA, C, 81)

    def test_dimensioni(self):
        cv = self._cv()
        assert len(cv["fs"]) == 81
        assert len(cv["gs_lordo"]) == 81
        assert len(cv["gs_netto"]) == 81

    def test_estremi(self):
        cv = self._cv()
        assert cv["fs"][0] == pytest.approx(0.0)
        assert cv["fs"][-1] == pytest.approx(2.5)
        assert cv["gs_lordo"][0] == pytest.approx(0.0)
        assert cv["gs_netto"][0] == pytest.approx(0.0)

    def test_netto_sotto_lordo(self):
        cv = self._cv()
        for gl, gn in zip(cv["gs_lordo"][::10], cv["gs_netto"][::10]):
            assert gn <= gl + 1e-12

    def test_coerente_con_growth(self):
        cv = self._cv()
        for f, gn in zip(cv["fs"][::10], cv["gs_netto"][::10]):
            assert gn == pytest.approx(
                _F["mh369_growth_netto"](f, MU, SIGMA, C))

    def test_massimo_vicino_fnetto(self):
        cv = self._cv()
        imax = cv["gs_netto"].index(max(cv["gs_netto"]))
        assert cv["fs"][imax] == pytest.approx(FNETTO, abs=2.5 / 80 + 1e-9)

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_curva"](2.5, MU, SIGMA, C, 1)

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_curva"](0.0, MU, SIGMA, C, 81)

    def test_c_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_curva"](2.5, MU, SIGMA, -0.001, 81)


class TestVerdetto:
    def test_nessun_edge_netto_mu_minore_c(self):
        assert _F["mh369_verdetto"](0.0, CAP, 0.002,
                                    C).startswith("NESSUN EDGE NETTO")

    def test_nessun_edge_netto_mu_uguale_c(self):
        assert _F["mh369_verdetto"](0.0, CAP, C,
                                    C).startswith("NESSUN EDGE NETTO")

    def test_cap_vincolante(self):
        assert _F["mh369_verdetto"](1.7, 1.0, 0.02,
                                    0.003).startswith("CAP VINCOLANTE")

    def test_sizing_pieno(self):
        assert _F["mh369_verdetto"](0.95, 1.0, 0.02,
                                    0.003).startswith("SIZING PIENO")

    def test_sizing_pieno_al_limite(self):
        assert _F["mh369_verdetto"](1.0, 1.0, 0.02,
                                    0.003).startswith("SIZING PIENO")

    def test_sotto_sizing(self):
        assert _F["mh369_verdetto"](0.5, 1.0, 0.02,
                                    0.003).startswith("SOTTO-SIZING OK")

    def test_cap_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_verdetto"](0.5, 0.0, 0.02, 0.003)


class TestAnalisi:
    def _demo(self):
        return _F["mh369_analisi"](MU, SIGMA, C, CAP)

    def test_demo(self):
        a = self._demo()
        assert a["f_lordo"] == pytest.approx(FLORDO)
        assert a["f_netto"] == pytest.approx(FNETTO)
        assert a["f_eff"] == pytest.approx(min(FNETTO, CAP))
        assert a["g_netto_star"] == pytest.approx(GNETTO_STAR)
        assert a["g_netto_eff"] == pytest.approx(GNETTO_EFF)
        assert a["g_lordo_eff"] == pytest.approx(GLORDO_EFF)
        assert a["vol_eff"] == pytest.approx(VOLEFF)
        assert a["sharpe"] == pytest.approx(SHARPE)
        assert a["breakeven"] == pytest.approx(BREAKEVEN)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("CAP VINCOLANTE")
        assert len(a["curva"]["fs"]) == 81

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["f_netto"] == a2["f_netto"]

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_analisi"](MU, 0.0, C, CAP)

    def test_c_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_analisi"](MU, SIGMA, -0.001, CAP)

    def test_cap_ko(self):
        with pytest.raises(ValueError):
            _F["mh369_analisi"](MU, SIGMA, C, 0.0)
