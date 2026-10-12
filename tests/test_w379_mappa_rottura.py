
"""Test tab379 'Mappa di rottura: superficie VaR su shock congiunti vol+corr': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh379_num", "mh379_z", "mh379_cov", "mh379_sigma_p",
           "mh379_AB", "mh379_var_mk", "mh379_frontier_m",
           "mh379_frontier_k", "mh379_safety", "mh379_verdetto",
           "mh379_mappa")

TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
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
TITLE411 = "🌊 Volatility drag: quanto rendimento mangia la volatilita'"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE374 = "Component VaR: contributo al rischio per posizione"
E = (10000.0, 8000.0, 6000.0)
S = (0.15, 0.2, 0.1)
RHO = (0.6, 0.3, 0.4)
SE = (1500.0, 1600.0, 600.0)
ALPHA = 0.95
LIM = 12000.0
Z = 1.6448536269514715
SIGP = 3059.0848304680926
VARB = 5031.746778547669
MSTAR = 2.3848576902082503
MSTARK1 = 1.9717518872814142
K2 = 0.9113606511669058
VAR31 = 18257.875259161334
AA = 9358000.0
BB = 4332000.0
SAFE = 0.5777777777777777
M_GRID = (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0)
K_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry379:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 411
        assert "tab379" in dvars
        assert "tab379" in withs

    def test_titoli_allineati_374_375_376_377_378_379(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab374")] == TITLE374
        assert titoli[dvars.index("tab375")] == TITLE375
        assert titoli[dvars.index("tab376")] == TITLE376
        assert titoli[dvars.index("tab377")] == TITLE377
        assert titoli[dvars.index("tab378")] == TITLE378
        assert titoli[dvars.index("tab379")] == TITLE379

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab411"
        assert titoli[-1] == TITLE411
        assert withs[-1] == "tab411"


class TestNum:
    def test_num_ok(self):
        assert _F["mh379_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_num"](float("inf"), "x")


class TestZ:
    def test_z_demo(self):
        assert _F["mh379_z"](ALPHA) == pytest.approx(Z)

    def test_z_95_forma_nota(self):
        assert _F["mh379_z"](0.95) == pytest.approx(1.6448536269514722)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_z"](0.4)
        with pytest.raises(ValueError):
            _F["mh379_z"](1.0)


class TestCov:
    def test_demo_c01(self):
        C = _F["mh379_cov"](SE, RHO)
        assert C[0][1] == pytest.approx(1440000.0)
        assert C[1][0] == pytest.approx(1440000.0)

    def test_diagonale(self):
        C = _F["mh379_cov"](SE, RHO)
        for i in range(3):
            assert C[i][i] == pytest.approx(SE[i] ** 2)

    def test_rho_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_cov"](SE, (1.5, 0.0, 0.0))

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_cov"]((-1.0, SE[1], SE[2]), RHO)

    def test_len_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_cov"]((1.0, 2.0), RHO)


class TestSigmaP:
    def test_demo(self):
        assert _F["mh379_sigma_p"](E, S, RHO) == pytest.approx(SIGP)

    def test_forma_chiusa(self):
        se = [E[i] * S[i] for i in range(3)]
        r12, r13, r23 = RHO
        var = (se[0] ** 2 + se[1] ** 2 + se[2] ** 2
               + 2.0 * (se[0] * se[1] * r12 + se[0] * se[2] * r13
                        + se[1] * se[2] * r23))
        assert _F["mh379_sigma_p"](E, S, RHO) == pytest.approx(
            math.sqrt(var))

    def test_zero_vol(self):
        assert _F["mh379_sigma_p"](E, (0.0, 0.0, 0.0), RHO) == pytest.approx(
            0.0)

    def test_s_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_sigma_p"](E, (-0.1, S[1], S[2]), RHO)


class TestAB:
    def test_demo(self):
        A, B = _F["mh379_AB"](E, S, RHO)
        assert A == pytest.approx(AA)
        assert B == pytest.approx(BB)

    def test_a_uguale_sigma_quadro(self):
        A, _ = _F["mh379_AB"](E, S, RHO)
        assert A == pytest.approx(SIGP ** 2)

    def test_b_forma_chiusa(self):
        se = [E[i] * S[i] for i in range(3)]
        r12, r13, r23 = RHO
        b = 2.0 * (se[0] * se[1] * (1.0 - r12)
                   + se[0] * se[2] * (1.0 - r13)
                   + se[1] * se[2] * (1.0 - r23))
        _, B = _F["mh379_AB"](E, S, RHO)
        assert B == pytest.approx(b)


class TestVarMK:
    def test_10_uguale_base(self):
        assert _F["mh379_var_mk"](AA, BB, Z, 1.0, 0.0) == pytest.approx(
            VARB)

    def test_31_forma_chiusa(self):
        assert _F["mh379_var_mk"](AA, BB, Z, 3.0, 1.0) == pytest.approx(
            VAR31)
        assert VAR31 == pytest.approx(3.0 * Z * math.sqrt(AA + BB))

    def test_separabile(self):
        # VaR(m, k) = m * VaR(1, k)
        for k in (0.0, 0.5, 1.0):
            assert _F["mh379_var_mk"](AA, BB, Z, 2.5, k) == pytest.approx(
                2.5 * _F["mh379_var_mk"](AA, BB, Z, 1.0, k))

    def test_monotona(self):
        v10 = _F["mh379_var_mk"](AA, BB, Z, 1.0, 0.0)
        v11 = _F["mh379_var_mk"](AA, BB, Z, 1.0, 1.0)
        v31 = _F["mh379_var_mk"](AA, BB, Z, 3.0, 1.0)
        assert v10 < v11 < v31

    def test_m_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_var_mk"](AA, BB, Z, 0.0, 0.5)
        with pytest.raises(ValueError):
            _F["mh379_var_mk"](AA, BB, Z, -1.0, 0.5)

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_var_mk"](AA, BB, Z, 1.0, 1.5)
        with pytest.raises(ValueError):
            _F["mh379_var_mk"](AA, BB, Z, 1.0, -0.1)


class TestFrontierM:
    def test_k0_demo(self):
        assert _F["mh379_frontier_m"](AA, BB, Z, LIM, 0.0) == pytest.approx(
            MSTAR)
        assert MSTAR == pytest.approx(LIM / VARB)

    def test_k1_forma_chiusa(self):
        assert _F["mh379_frontier_m"](AA, BB, Z, LIM, 1.0) == pytest.approx(
            MSTARK1)
        assert MSTARK1 == pytest.approx(LIM / (Z * math.sqrt(AA + BB)))

    def test_frontiera_rompe_davvero(self):
        ms = _F["mh379_frontier_m"](AA, BB, Z, LIM, 0.5)
        assert _F["mh379_var_mk"](AA, BB, Z, ms, 0.5) == pytest.approx(
            LIM)

    def test_gia_rotto_none(self):
        assert _F["mh379_frontier_m"](AA, BB, Z, VARB / 2.0, 0.0) is None

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_frontier_m"](AA, BB, Z, LIM, 1.5)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_frontier_m"](AA, BB, Z, 0.0, 0.5)


class TestFrontierK:
    def test_m1_none(self):
        # demo: nemmeno la correlazione piena rompe a m=1
        assert _F["mh379_frontier_k"](AA, BB, Z, LIM, 1.0) is None

    def test_m2_forma_chiusa(self):
        assert _F["mh379_frontier_k"](AA, BB, Z, LIM, 2.0) == pytest.approx(
            K2)
        assert K2 == pytest.approx(((LIM / (2.0 * Z)) ** 2 - AA) / BB)
        assert 0.0 < K2 < 1.0

    def test_k2_rompe_davvero(self):
        rp = tuple((1.0 - K2) * r + K2 for r in RHO)
        assert _F["mh379_sigma_p"](E, S, rp) * 2.0 * Z == pytest.approx(
            LIM)

    def test_negativo_gia_rotto(self):
        k = _F["mh379_frontier_k"](AA, BB, Z, VARB / 2.0, 1.0)
        assert k < 0.0

    def test_m_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_frontier_k"](AA, BB, Z, LIM, 0.0)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_frontier_k"](AA, BB, Z, -5.0, 1.0)


class TestSafety:
    def test_demo(self):
        q = _F["mh379_safety"](AA, BB, Z, LIM, M_GRID, K_GRID)
        assert q == pytest.approx(SAFE)

    def test_tutto_dentro(self):
        q = _F["mh379_safety"](AA, BB, Z, 10.0 * LIM, M_GRID, K_GRID)
        assert q == pytest.approx(1.0)

    def test_tutto_fuori(self):
        q = _F["mh379_safety"](AA, BB, Z, VARB / 2.0, M_GRID, K_GRID)
        assert q == pytest.approx(0.0)

    def test_griglia_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_safety"](AA, BB, Z, LIM, (), K_GRID)
        with pytest.raises(ValueError):
            _F["mh379_safety"](AA, BB, Z, LIM, M_GRID, [])

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_safety"](AA, BB, Z, 0.0, M_GRID, K_GRID)


class TestVerdetto:
    def test_sicuro(self):
        assert _F["mh379_verdetto"](0.95).startswith("SICURO")
        assert _F["mh379_verdetto"](0.9).startswith("SICURO")

    def test_vulnerabile(self):
        assert _F["mh379_verdetto"](0.899).startswith("VULNERABILE")
        assert _F["mh379_verdetto"](0.6).startswith("VULNERABILE")

    def test_esposto(self):
        assert _F["mh379_verdetto"](0.599).startswith("ESPOSTO")
        assert _F["mh379_verdetto"](0.3).startswith("ESPOSTO")

    def test_critico(self):
        assert _F["mh379_verdetto"](0.299).startswith("CRITICO")
        assert _F["mh379_verdetto"](0.0).startswith("CRITICO")

    def test_demo_esposto(self):
        assert _F["mh379_verdetto"](SAFE).startswith("ESPOSTO")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh379_verdetto"](1.5)


class TestMappa:
    def _b(self):
        return _F["mh379_mappa"](E, S, RHO, ALPHA, LIM)

    def test_demo(self):
        b = self._b()
        assert b["z"] == pytest.approx(Z)
        assert b["sigma_p"] == pytest.approx(SIGP)
        assert b["var_base"] == pytest.approx(VARB)
        assert b["A"] == pytest.approx(AA)
        assert b["B"] == pytest.approx(BB)
        assert b["limite"] == pytest.approx(LIM)
        assert b["m_star"] == pytest.approx(MSTAR)
        assert b["k_star"] is None
        assert b["safe"] == pytest.approx(SAFE)
        assert b["verdetto"].startswith("ESPOSTO")

    def test_coerenza(self):
        b = self._b()
        assert b["var_base"] == pytest.approx(b["z"] * b["sigma_p"])
        assert b["m_star"] == pytest.approx(b["limite"] / b["var_base"])
        assert b["A"] == pytest.approx(b["sigma_p"] ** 2)
        assert len(b["m_grid"]) == 9
        assert len(b["k_grid"]) == 5

    def test_griglia_default(self):
        b = self._b()
        assert b["m_grid"] == M_GRID
        assert b["k_grid"] == K_GRID
