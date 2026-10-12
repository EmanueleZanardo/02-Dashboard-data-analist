"""Test tab380 'Liquidity-adjusted VaR: VaR + costo di liquidazione': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh380_num", "mh380_z", "mh380_sigma_p", "mh380_var_base",
           "mh380_col", "mh380_lvar", "mh380_quota", "mh380_stress",
           "mh380_verdetto", "mh380_mappa")

TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
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
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
E = (10000.0, 8000.0, 6000.0)
S = (0.15, 0.2, 0.1)
RHO = (0.6, 0.3, 0.4)
SE = (1500.0, 1600.0, 600.0)
SB = (0.004, 0.008, 0.012)
ST = (0.001, 0.0025, 0.003)
ALPHA = 0.95
ALPHAS = 0.99
Z = 1.6448536269514715
ZT = 2.3263478740408408
SIGP = 3059.0848304680926
VARB = 5031.746778547669
COL1 = 43.26347874040841
COL2 = 78.5269574808168
COL3 = 77.87426173273514
COLT = 199.66469795396034
LVAR = 5231.411476501629
QUOTA = 0.03816650608555856


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry380:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 398
        assert "tab380" in dvars
        assert "tab380" in withs

    def test_titoli_allineati_375_376_377_378_379_380(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab375")] == TITLE375
        assert titoli[dvars.index("tab376")] == TITLE376
        assert titoli[dvars.index("tab377")] == TITLE377
        assert titoli[dvars.index("tab378")] == TITLE378
        assert titoli[dvars.index("tab379")] == TITLE379
        assert titoli[dvars.index("tab380")] == TITLE380

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab398"
        assert titoli[-1] == TITLE398
        assert withs[-1] == "tab398"


class TestNum:
    def test_num_ok(self):
        assert _F["mh380_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_num"](float("inf"), "x")


class TestZ:
    def test_z_demo(self):
        assert _F["mh380_z"](ALPHA) == pytest.approx(Z)

    def test_zt_demo(self):
        assert _F["mh380_z"](ALPHAS) == pytest.approx(ZT)

    def test_z_95_forma_nota(self):
        assert _F["mh380_z"](0.95) == pytest.approx(1.6448536269514722)

    def test_z_99_forma_nota(self):
        assert _F["mh380_z"](0.99) == pytest.approx(2.3263478740408408)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_z"](0.4)
        with pytest.raises(ValueError):
            _F["mh380_z"](1.0)


class TestSigmaP:
    def test_demo(self):
        assert _F["mh380_sigma_p"](E, S, RHO) == pytest.approx(SIGP)

    def test_forma_chiusa(self):
        se = [E[i] * S[i] for i in range(3)]
        r12, r13, r23 = RHO
        var = (se[0] ** 2 + se[1] ** 2 + se[2] ** 2
               + 2.0 * (se[0] * se[1] * r12 + se[0] * se[2] * r13
                        + se[1] * se[2] * r23))
        assert _F["mh380_sigma_p"](E, S, RHO) == pytest.approx(
            math.sqrt(var))

    def test_demo_var_9358000(self):
        assert SIGP ** 2 == pytest.approx(9358000.0, rel=1e-9)

    def test_zero_vol(self):
        assert _F["mh380_sigma_p"](E, (0.0, 0.0, 0.0), RHO) == pytest.approx(
            0.0)

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_sigma_p"](E, (-0.1, S[1], S[2]), RHO)

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_sigma_p"](E, S, (1.5, RHO[1], RHO[2]))


class TestVarBase:
    def test_demo(self):
        assert _F["mh380_var_base"](SIGP, Z) == pytest.approx(VARB)

    def test_forma_chiusa(self):
        assert VARB == pytest.approx(Z * SIGP)

    def test_zero_sigma(self):
        assert _F["mh380_var_base"](0.0, Z) == pytest.approx(0.0)

    def test_z_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_var_base"](SIGP, 0.0)
        with pytest.raises(ValueError):
            _F["mh380_var_base"](SIGP, -1.0)

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_var_base"](-1.0, Z)


class TestCol:
    def test_demo(self):
        col = _F["mh380_col"](E, SB, ST, ZT)
        assert col[0] == pytest.approx(COL1)
        assert col[1] == pytest.approx(COL2)
        assert col[2] == pytest.approx(COL3)

    def test_forma_chiusa(self):
        col = _F["mh380_col"](E, SB, ST, ZT)
        for i in range(3):
            assert col[i] == pytest.approx(
                E[i] * (SB[i] / 2.0 + ZT * ST[i]))

    def test_somma_totale(self):
        col = _F["mh380_col"](E, SB, ST, ZT)
        assert sum(col) == pytest.approx(COLT)

    def test_meta_spread_solo(self):
        # con zt -> 0+ il costo tende a meta' spread medio
        col = _F["mh380_col"](E, SB, (0.0, 0.0, 0.0), 1e-12)
        for i in range(3):
            assert col[i] == pytest.approx(E[i] * SB[i] / 2.0)

    def test_sbar_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_col"](E, (-0.001, SB[1], SB[2]), ST, ZT)

    def test_stilde_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_col"](E, SB, (ST[0], -0.001, ST[2]), ZT)

    def test_zt_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_col"](E, SB, ST, 0.0)

    def test_len_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_col"]((1.0, 2.0), SB, ST, ZT)


class TestLvar:
    def test_demo(self):
        assert _F["mh380_lvar"](VARB, COLT) == pytest.approx(LVAR)

    def test_forma_chiusa(self):
        assert LVAR == pytest.approx(VARB + COLT)

    def test_col_zero(self):
        assert _F["mh380_lvar"](VARB, 0.0) == pytest.approx(VARB)

    def test_col_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_lvar"](VARB, -1.0)

    def test_var_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_lvar"](-1.0, COLT)


class TestQuota:
    def test_demo(self):
        assert _F["mh380_quota"](COLT, LVAR) == pytest.approx(QUOTA)

    def test_forma_chiusa(self):
        assert QUOTA == pytest.approx(COLT / LVAR)

    def test_zero_col(self):
        assert _F["mh380_quota"](0.0, LVAR) == pytest.approx(0.0)

    def test_lvar_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_quota"](COLT, 0.0)
        with pytest.raises(ValueError):
            _F["mh380_quota"](COLT, -5.0)

    def test_col_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_quota"](-1.0, LVAR)


class TestStress:
    def test_w1_neutro(self):
        assert _F["mh380_stress"](COLT, 1.0) == pytest.approx(COLT)

    def test_w2_raddoppia(self):
        assert _F["mh380_stress"](COLT, 2.0) == pytest.approx(2.0 * COLT)

    def test_lineare(self):
        # COL(w) = w * COL(1): lo shock scala linearmente il costo
        for w in (1.25, 1.5, 2.5, 3.0):
            assert _F["mh380_stress"](COLT, w) == pytest.approx(
                w * _F["mh380_stress"](COLT, 1.0))

    def test_w_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_stress"](COLT, 0.0)
        with pytest.raises(ValueError):
            _F["mh380_stress"](COLT, -1.0)

    def test_col_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_stress"](-1.0, 2.0)


class TestVerdetto:
    def test_trascurabile(self):
        assert _F["mh380_verdetto"](0.0).startswith("TRASCURABILE")
        assert _F["mh380_verdetto"](0.019).startswith("TRASCURABILE")

    def test_moderata(self):
        assert _F["mh380_verdetto"](0.02).startswith("MODERATA")
        assert _F["mh380_verdetto"](0.0499).startswith("MODERATA")

    def test_rilevante(self):
        assert _F["mh380_verdetto"](0.05).startswith("RILEVANTE")
        assert _F["mh380_verdetto"](0.0999).startswith("RILEVANTE")

    def test_dominante(self):
        assert _F["mh380_verdetto"](0.10).startswith("DOMINANTE")
        assert _F["mh380_verdetto"](0.5).startswith("DOMINANTE")

    def test_demo_moderata(self):
        assert _F["mh380_verdetto"](QUOTA).startswith("MODERATA")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh380_verdetto"](1.5)
        with pytest.raises(ValueError):
            _F["mh380_verdetto"](-0.1)


class TestMappa:
    def _b(self):
        return _F["mh380_mappa"](E, S, RHO, SB, ST, ALPHA, ALPHAS)

    def test_demo(self):
        b = self._b()
        assert b["z"] == pytest.approx(Z)
        assert b["zt"] == pytest.approx(ZT)
        assert b["sigma_p"] == pytest.approx(SIGP)
        assert b["var_base"] == pytest.approx(VARB)
        assert b["col"] == (pytest.approx(COL1), pytest.approx(COL2),
                            pytest.approx(COL3))
        assert b["col_tot"] == pytest.approx(COLT)
        assert b["lvar"] == pytest.approx(LVAR)
        assert b["quota"] == pytest.approx(QUOTA)
        assert b["verdetto"].startswith("MODERATA")

    def test_coerenza(self):
        b = self._b()
        assert b["var_base"] == pytest.approx(b["z"] * b["sigma_p"])
        assert b["lvar"] == pytest.approx(b["var_base"] + b["col_tot"])
        assert b["quota"] == pytest.approx(b["col_tot"] / b["lvar"])
        assert b["col_tot"] == pytest.approx(sum(b["col"]))
        assert b["alpha"] == pytest.approx(ALPHA)
        assert b["alpha_s"] == pytest.approx(ALPHAS)

    def test_echo_input(self):
        b = self._b()
        assert b["E"] == E
        assert b["s"] == S
        assert b["rho"] == RHO
        assert b["sbar"] == SB
        assert b["stilde"] == ST
