"""Test tab373 'Kelly con limite VaR: sizing con vincolo di perdita massima': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh373_num", "mh373_z", "mh373_f_kelly", "mh373_f_var",
           "mh373_crescita", "mh373_vol", "mh373_var_usato",
           "mh373_verdetto", "mh373_analisi")

TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
MU = 0.02
SG = 0.1
LIMITE = 0.03
ALPHA = 0.95
Z = 1.6448536269514715
FSTAR = 1.9999999999999996
FVAR = 0.1823870495735308
F = 0.1823870495735308
G = 0.003481415812209928
GSTAR = 0.02
GPERSA = 0.01651858418779007
VOL = 0.01823870495735308
VARUSATO = 0.03
SLACK = 0.0
RADDOPPIO = 199.09922225577253
VERDETTO = 'VINCOLO VaR: sizing ridotto al limite di perdita'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry373:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 373
        assert "tab373" in dvars
        assert "tab373" in withs

    def test_titoli_allineati_368_369_370_371_372_373(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab373"
        assert titoli[-1] == TITLE373
        assert withs[-1] == "tab373"


class TestNum:
    def test_num_ok(self):
        assert _F["mh373_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_num"](float("inf"), "x")


class TestZ:
    def test_demo(self):
        assert _F["mh373_z"](ALPHA) == pytest.approx(Z)

    def test_z95_noto(self):
        from statistics import NormalDist
        assert _F["mh373_z"](0.95) == pytest.approx(
            NormalDist().inv_cdf(0.95))

    def test_alpha_basso_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_z"](0.5)

    def test_alpha_alto_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_z"](1.0)


class TestKelly:
    def test_forma_chiusa(self):
        assert _F["mh373_f_kelly"](0.02, 0.10) == pytest.approx(2.0)

    def test_demo(self):
        assert _F["mh373_f_kelly"](MU, SG) == pytest.approx(FSTAR)

    def test_mu_nullo(self):
        assert _F["mh373_f_kelly"](0.0, 0.10) == 0.0

    def test_mu_negativo(self):
        assert _F["mh373_f_kelly"](-0.01, 0.10) == 0.0

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_f_kelly"](0.02, 0.0)


class TestFVar:
    def test_forma_chiusa(self):
        # 0.03 / (1.6448536269514722 * 0.10)
        assert _F["mh373_f_var"](0.03, 0.10,
                                 1.6448536269514722) == pytest.approx(
            0.1823870496)

    def test_demo(self):
        assert _F["mh373_f_var"](LIMITE, SG, Z) == pytest.approx(FVAR)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_f_var"](0.0, SG, Z)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_f_var"](LIMITE, 0.0, Z)


class TestCrescita:
    def test_kelly_pieno(self):
        # g(2.0) = 2*0.02 - 0.5*4*0.01 = 0.02
        assert _F["mh373_crescita"](2.0, 0.02, 0.10) == pytest.approx(0.02)

    def test_zero(self):
        assert _F["mh373_crescita"](0.0, 0.02, 0.10) == pytest.approx(0.0)

    def test_demo(self):
        assert _F["mh373_crescita"](F, MU, SG) == pytest.approx(G)

    def test_massimo_in_fstar(self):
        g_star = _F["mh373_crescita"](FSTAR, MU, SG)
        assert g_star == pytest.approx(GSTAR)
        assert g_star >= _F["mh373_crescita"](FSTAR * 0.5, MU, SG)


class TestVolVar:
    def test_vol(self):
        assert _F["mh373_vol"](0.5, 0.10) == pytest.approx(0.05)

    def test_demo(self):
        assert _F["mh373_vol"](F, SG) == pytest.approx(VOL)
        assert _F["mh373_var_usato"](F, SG, Z) == pytest.approx(VARUSATO)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_vol"](0.5, 0.0)
        with pytest.raises(ValueError):
            _F["mh373_var_usato"](0.5, 0.0, Z)


class TestVerdetto:
    def test_demo(self):
        f, lab = _F["mh373_verdetto"](FSTAR, FVAR)
        assert f == pytest.approx(F)
        assert lab == VERDETTO
        assert lab.startswith("VINCOLO VaR")

    def test_kelly_libero(self):
        f, lab = _F["mh373_verdetto"](0.5, 1.0)
        assert f == pytest.approx(0.5)
        assert lab.startswith("KELLY LIBERO")

    def test_nessun_edge(self):
        f, lab = _F["mh373_verdetto"](0.0, 1.0)
        assert f == 0.0
        assert lab.startswith("NESSUN EDGE")


class TestAnalisi:
    def test_demo(self):
        a = _F["mh373_analisi"](MU, SG, LIMITE, ALPHA)
        assert a["z"] == pytest.approx(Z)
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["f_var"] == pytest.approx(FVAR)
        assert a["f"] == pytest.approx(F)
        assert a["g"] == pytest.approx(G)
        assert a["g_star"] == pytest.approx(GSTAR)
        assert a["g_persa"] == pytest.approx(GPERSA)
        assert a["vol"] == pytest.approx(VOL)
        assert a["var_usato"] == pytest.approx(VARUSATO)
        assert a["slack"] == pytest.approx(SLACK)
        assert a["raddoppio"] == pytest.approx(RADDOPPIO)
        assert a["verdetto"] == VERDETTO
        # il vincolo morde: f_var < f_star e VaR usato = limite
        assert a["f_var"] < a["f_star"]
        assert a["var_usato"] == pytest.approx(LIMITE)
        assert a["g_persa"] > 0.0

    def test_kelly_libero(self):
        # limite largo: il vincolo non morde
        a = _F["mh373_analisi"](0.02, 0.10, 0.50, 0.95)
        assert a["f"] == pytest.approx(a["f_star"])
        assert a["verdetto"].startswith("KELLY LIBERO")
        assert a["slack"] > 0.0

    def test_nessun_edge(self):
        a = _F["mh373_analisi"](0.0, 0.10, 0.03, 0.95)
        assert a["f"] == 0.0
        assert a["g"] == pytest.approx(0.0)
        assert a["raddoppio"] is None
        assert a["verdetto"].startswith("NESSUN EDGE")

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_analisi"](MU, 0.0, LIMITE, ALPHA)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_analisi"](MU, SG, 0.0, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh373_analisi"](MU, SG, LIMITE, 1.5)
