"""Test tab370 'Kelly e drawdown: probabilità di toccare un max drawdown': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh370_num", "mh370_growth", "mh370_vol_log",
           "mh370_sharpe", "mh370_fstar", "mh370_proba_drawdown",
           "mh370_trade_raddoppio", "mh370_verdetto",
           "mh370_curva_rischio", "mh370_mappa", "mh370_analisi")

TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
F = 1.0
MU = 0.02
SIGMA = 0.1
D = 0.3
G = 0.015
PDD = 0.343
TRADE2X = 46.20981203732969
SHARPE = 0.19999999999999998
FSTAR = 1.9999999999999996
VERDETTO = "RISCHIO ALTO: P = 34.3% di toccare un max drawdown 30% dal picco con f = 100%: sizing aggressivo, valuta frazione ridotta o stop piu' stretto."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry370:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 372
        assert "tab370" in dvars
        assert "tab370" in withs

    def test_titoli_allineati_365_366_367_368_369_370(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab365")] == TITLE365
        assert titoli[dvars.index("tab366")] == TITLE366
        assert titoli[dvars.index("tab367")] == TITLE367
        assert titoli[dvars.index("tab368")] == TITLE368
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab372"
        assert titoli[-1] == TITLE372
        assert withs[-1] == "tab372"


class TestNum:
    def test_num_ok(self):
        assert _F["mh370_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_num"](float("inf"), "x")


class TestGrowth:
    def test_demo(self):
        assert _F["mh370_growth"](F, MU, SIGMA) == pytest.approx(G)

    def test_forma_chiusa(self):
        f, mu, sg = 0.5, 0.02, 0.10
        assert _F["mh370_growth"](f, mu, sg) == pytest.approx(
            f * mu - 0.5 * (f * sg) ** 2)

    def test_zero_in_zero(self):
        assert _F["mh370_growth"](0.0, MU, SIGMA) == pytest.approx(0.0)

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_growth"](-0.1, MU, SIGMA)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_growth"](F, MU, 0.0)


class TestProbaDrawdown:
    def test_demo(self):
        # (1-0.30)^(2*0.015/0.01) = 0.7^3 = 0.343
        assert _F["mh370_proba_drawdown"](F, MU, SIGMA,
                                          D) == pytest.approx(PDD)

    def test_forma_chiusa(self):
        # f=0.5, mu=0.02, sg=0.10, D=0.2:
        # g=0.00875, v=0.05, exp=7 -> 0.8^7
        assert _F["mh370_proba_drawdown"](0.5, 0.02, 0.10,
                                          0.2) == pytest.approx(0.8 ** 7)

    def test_f_zero_nessun_rischio(self):
        assert _F["mh370_proba_drawdown"](0.0, MU, SIGMA, D) == 0.0

    def test_drift_non_positivo_certa(self):
        # mu=0 -> g = -0.5*(f*sg)^2 < 0
        assert _F["mh370_proba_drawdown"](1.0, 0.0, SIGMA, D) == 1.0

    def test_monotona_in_d(self):
        p_basso = _F["mh370_proba_drawdown"](F, MU, SIGMA, 0.20)
        p_alto = _F["mh370_proba_drawdown"](F, MU, SIGMA, 0.50)
        assert p_alto < p_basso

    def test_in_range(self):
        for f in (0.1, 0.5, 1.0, 1.5):
            p = _F["mh370_proba_drawdown"](f, MU, SIGMA, D)
            assert 0.0 <= p <= 1.0

    def test_d_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_proba_drawdown"](F, MU, SIGMA, 0.0)
        with pytest.raises(ValueError):
            _F["mh370_proba_drawdown"](F, MU, SIGMA, 1.0)
        with pytest.raises(ValueError):
            _F["mh370_proba_drawdown"](F, MU, SIGMA, -0.1)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_proba_drawdown"](F, MU, -0.1, D)


class TestTradeRaddoppio:
    def test_demo(self):
        assert _F["mh370_trade_raddoppio"](F, MU, SIGMA) == pytest.approx(
            TRADE2X)

    def test_forma_chiusa(self):
        assert _F["mh370_trade_raddoppio"](0.5, 0.02,
                                           0.10) == pytest.approx(
            math.log(2.0) / 0.00875)

    def test_none_se_drift_non_positivo(self):
        assert _F["mh370_trade_raddoppio"](1.0, 0.0, SIGMA) is None

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_trade_raddoppio"](-0.1, MU, SIGMA)


class TestVerdetto:
    def test_nessun_edge(self):
        assert _F["mh370_verdetto"](1.0, -0.001, 1.0,
                                    0.3).startswith("NESSUN EDGE")

    def test_rischio_critico(self):
        assert _F["mh370_verdetto"](0.6, 0.015, 1.0,
                                    0.3).startswith("RISCHIO CRITICO")

    def test_rischio_critico_al_limite(self):
        assert _F["mh370_verdetto"](0.5, 0.015, 1.0,
                                    0.3).startswith("RISCHIO CRITICO")

    def test_rischio_alto(self):
        assert _F["mh370_verdetto"](PDD, 0.015, 1.0,
                                    0.3).startswith("RISCHIO ALTO")

    def test_rischio_alto_al_limite(self):
        assert _F["mh370_verdetto"](0.25, 0.015, 1.0,
                                    0.3).startswith("RISCHIO ALTO")

    def test_rischio_moderato(self):
        assert _F["mh370_verdetto"](0.15, 0.015, 1.0,
                                    0.3).startswith("RISCHIO MODERATO")

    def test_rischio_contenuto(self):
        assert _F["mh370_verdetto"](0.05, 0.015, 1.0,
                                    0.3).startswith("RISCHIO CONTENUTO")

    def test_p_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_verdetto"](1.5, 0.015, 1.0, 0.3)


class TestCurva:
    def _cv(self):
        return _F["mh370_curva_rischio"](2.5, MU, SIGMA, D, 81)

    def test_dimensioni(self):
        cv = self._cv()
        assert len(cv["fs"]) == 81
        assert len(cv["ps"]) == 81

    def test_estremi(self):
        cv = self._cv()
        assert cv["fs"][0] == pytest.approx(0.0)
        assert cv["ps"][0] == pytest.approx(0.0)
        assert cv["fs"][-1] == pytest.approx(2.5)

    def test_monotona_non_decrescente(self):
        cv = self._cv()
        for i in range(1, len(cv["ps"])):
            assert cv["ps"][i] >= cv["ps"][i - 1] - 1e-12

    def test_coerente_con_proba(self):
        cv = self._cv()
        for f, p in zip(cv["fs"][::10], cv["ps"][::10]):
            assert p == pytest.approx(
                _F["mh370_proba_drawdown"](f, MU, SIGMA, D))

    def test_in_range(self):
        cv = self._cv()
        assert all(0.0 <= p <= 1.0 for p in cv["ps"])

    def test_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_curva_rischio"](2.5, MU, SIGMA, D, 1)

    def test_fmax_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_curva_rischio"](0.0, MU, SIGMA, D, 81)

    def test_d_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_curva_rischio"](2.5, MU, SIGMA, 1.0, 81)


class TestMappa:
    def _mp(self):
        return _F["mh370_mappa"](2.5, MU, SIGMA, 0.05, 0.60)

    def test_dimensioni(self):
        mp = self._mp()
        assert len(mp["fs"]) == 25
        assert len(mp["ds"]) == 13
        assert all(len(row) == 25 for row in mp["z"])

    def test_estremi(self):
        mp = self._mp()
        assert mp["fs"][0] == pytest.approx(0.05)
        assert mp["fs"][-1] == pytest.approx(2.5)
        assert mp["ds"][0] == pytest.approx(0.05)
        assert mp["ds"][-1] == pytest.approx(0.60)

    def test_in_range(self):
        mp = self._mp()
        assert all(0.0 <= p <= 1.0 for row in mp["z"] for p in row)

    def test_coerente_con_proba(self):
        mp = self._mp()
        for j in (0, 6, 12):
            for i in (0, 12, 24):
                assert mp["z"][j][i] == pytest.approx(
                    _F["mh370_proba_drawdown"](mp["fs"][i], MU, SIGMA,
                                              mp["ds"][j]))

    def test_d_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_mappa"](2.5, MU, SIGMA, 0.60, 0.05)
        with pytest.raises(ValueError):
            _F["mh370_mappa"](2.5, MU, SIGMA, 0.0, 0.60)


class TestAnalisi:
    def _demo(self):
        return _F["mh370_analisi"](F, MU, SIGMA, D)

    def test_demo(self):
        a = self._demo()
        assert a["f"] == pytest.approx(F)
        assert a["g"] == pytest.approx(G)
        assert a["p_drawdown"] == pytest.approx(PDD)
        assert a["trade_raddoppio"] == pytest.approx(TRADE2X)
        assert a["sharpe"] == pytest.approx(SHARPE)
        assert a["f_star"] == pytest.approx(FSTAR)
        assert a["vol"] == pytest.approx(0.1)
        assert a["verdetto"] == VERDETTO
        assert a["verdetto"].startswith("RISCHIO ALTO")
        assert len(a["curva"]["fs"]) == 81
        assert len(a["mappa"]["ds"]) == 13

    def test_determinismo(self):
        a1 = self._demo()
        a2 = self._demo()
        assert a1["verdetto"] == a2["verdetto"]
        assert a1["p_drawdown"] == a2["p_drawdown"]

    def test_f_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_analisi"](-0.1, MU, SIGMA, D)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_analisi"](F, MU, 0.0, D)

    def test_d_ko(self):
        with pytest.raises(ValueError):
            _F["mh370_analisi"](F, MU, SIGMA, 1.0)
