"""Test tab384 'Delta-Gamma VaR: VaR parametrico di una posizione con opzioni': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh384_num", "mh384_phi", "mh384_ppf", "mh384_ab",
           "mh384_moments", "mh384_z_cf", "mh384_var_delta",
           "mh384_var_dg", "mh384_incremento", "mh384_verdetto",
           "mh384_pdf_pnl", "mh384_mappa")

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
TITLE412 = "🎯 Omega ratio: quanto upside prendi per ogni euro di downside"
TITLE414 = "🎯 Probabilistic Sharpe ratio: lo Sharpe e' davvero significativo?"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
S0 = 80.0
QTA = 1000.0
DELTA = 0.6
GAMMA = -0.05
SIG = 0.4
T = 0.003968253968253968
ALPHA = 0.99
A = 48000.0
B = -160000.0
S = 0.025197631533948484
MEAN = -101.58730158730161
VAR = 1483497.102544722
SKEW = -0.49811373765008327
KURT = 0.3315901701323254
VAR_D = 2813.6859143935444
VAR_DG = 3361.856972190826
INCR = 0.1948231161811937


def _moments_demo():
    return _F["mh384_moments"](A, B, S)


class TestRegistry384:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 415
        assert "tab384" in dvars
        assert "tab384" in withs

    def test_titoli_allineati_379_380_381_382_383_384(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab379")] == TITLE379
        assert titoli[dvars.index("tab380")] == TITLE380
        assert titoli[dvars.index("tab381")] == TITLE381
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab415"
        assert titoli[-1] == TITLE415
        assert withs[-1] == "tab415"


class TestNum:
    def test_num_ok(self):
        assert _F["mh384_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_num"](float("inf"), "x")


class TestPhiPpf:
    def test_phi_zero(self):
        assert _F["mh384_phi"](0.0) == pytest.approx(1.0 / math.sqrt(
            2.0 * math.pi))

    def test_phi_simmetria(self):
        assert _F["mh384_phi"](1.5) == pytest.approx(_F["mh384_phi"](-1.5))

    def test_ppf_nota(self):
        assert _F["mh384_ppf"](0.01) == pytest.approx(-2.32634787404084)

    def test_ppf_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_ppf"](0.0)
        with pytest.raises(ValueError):
            _F["mh384_ppf"](1.0)


class TestAB:
    def test_demo(self):
        a, b = _F["mh384_ab"](DELTA, GAMMA, QTA, S0)
        assert a == pytest.approx(A)
        assert b == pytest.approx(B)

    def test_forma_chiusa(self):
        assert A == pytest.approx(DELTA * QTA * S0)
        assert B == pytest.approx(0.5 * GAMMA * QTA * S0 ** 2)

    def test_qta_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_ab"](DELTA, GAMMA, 0.0, S0)

    def test_s0_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_ab"](DELTA, GAMMA, QTA, -1.0)


class TestMoments:
    def test_demo_media(self):
        mean, _, _, _ = _moments_demo()
        assert mean == pytest.approx(MEAN)

    def test_demo_var(self):
        _, var, _, _ = _moments_demo()
        assert var == pytest.approx(VAR)

    def test_demo_skew(self):
        _, _, skew, _ = _moments_demo()
        assert skew == pytest.approx(SKEW)

    def test_demo_kurt(self):
        _, _, _, kurt = _moments_demo()
        assert kurt == pytest.approx(KURT)

    def test_forme_chiuse(self):
        s2 = S ** 2
        assert MEAN == pytest.approx(B * s2)
        assert VAR == pytest.approx(s2 * (A ** 2 + 2.0 * B ** 2 * s2))
        m3 = 2.0 * B * s2 ** 2 * (3.0 * A ** 2 + 4.0 * B ** 2 * s2)
        assert SKEW == pytest.approx(m3 / VAR ** 1.5)
        m4 = (3.0 * A ** 4 * s2 ** 2 + 60.0 * A ** 2 * B ** 2 * s2 ** 3
              + 60.0 * B ** 4 * s2 ** 4)
        assert KURT == pytest.approx(m4 / VAR ** 2 - 3.0)

    def test_gamma_zero_degenere(self):
        mean, var, skew, kurt = _F["mh384_moments"](A, 0.0, S)
        assert mean == pytest.approx(0.0)
        assert var == pytest.approx(A ** 2 * S ** 2)
        assert skew == pytest.approx(0.0)
        assert kurt == pytest.approx(0.0)

    def test_gamma_lungo_skew_positiva(self):
        _, _, skew, _ = _F["mh384_moments"](A, abs(B), S)
        assert skew > 0.0

    def test_posizione_nulla(self):
        mean, var, skew, kurt = _F["mh384_moments"](0.0, 0.0, S)
        assert var == 0.0
        assert skew == 0.0
        assert kurt == 0.0

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_moments"](A, B, 0.0)


class TestZCf:
    def test_normale_degenere(self):
        z = _F["mh384_ppf"](1.0 - ALPHA)
        assert _F["mh384_z_cf"](z, 0.0, 0.0) == pytest.approx(z)

    def test_forma_chiusa(self):
        z = -2.0
        sk, ku = -0.5, 0.3
        assert _F["mh384_z_cf"](z, sk, ku) == pytest.approx(
            z + (z ** 2 - 1.0) * sk / 6.0
            + (z ** 3 - 3.0 * z) * ku / 24.0
            - (2.0 * z ** 3 - 5.0 * z) * sk ** 2 / 36.0)

    def test_short_gamma_piu_estremo(self):
        z = _F["mh384_ppf"](1.0 - ALPHA)
        assert _F["mh384_z_cf"](z, SKEW, KURT) < z


class TestVarDelta:
    def test_demo(self):
        assert _F["mh384_var_delta"](A, S, ALPHA) == pytest.approx(VAR_D)

    def test_demo_chiusa(self):
        assert VAR_D == pytest.approx(
            abs(A) * S * abs(_F["mh384_ppf"](1.0 - ALPHA)))

    def test_delta_zero(self):
        assert _F["mh384_var_delta"](0.0, S, ALPHA) == 0.0

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_var_delta"](A, 0.0, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_var_delta"](A, S, 0.4)


class TestVarDg:
    def test_demo(self):
        assert _F["mh384_var_dg"](A, B, S, ALPHA) == pytest.approx(VAR_DG)

    def test_demo_sopra_delta(self):
        assert VAR_DG > VAR_D

    def test_gamma_zero_degenere(self):
        assert _F["mh384_var_dg"](A, 0.0, S, ALPHA) == pytest.approx(VAR_D)

    def test_gamma_lungo_sotto_delta(self):
        assert _F["mh384_var_dg"](A, abs(B), S, ALPHA) < VAR_D

    def test_posizione_nulla(self):
        assert _F["mh384_var_dg"](0.0, 0.0, S, ALPHA) == 0.0

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_var_dg"](A, B, 0.0, ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_var_dg"](A, B, S, 0.4)


class TestIncremento:
    def test_demo(self):
        assert _F["mh384_incremento"](VAR_DG, VAR_D) == pytest.approx(INCR)

    def test_forma_chiusa(self):
        assert INCR == pytest.approx((VAR_DG - VAR_D) / VAR_D)

    def test_demo_rilevante(self):
        assert 0.15 <= INCR < 0.30

    def test_vd_zero_vdg_zero(self):
        assert _F["mh384_incremento"](0.0, 0.0) == 0.0

    def test_vd_zero_vdg_pos(self):
        assert _F["mh384_incremento"](100.0, 0.0) == math.inf

    def test_negativi_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_incremento"](VAR_DG, -1.0)


class TestVerdetto:
    def test_riduttivo(self):
        assert _F["mh384_verdetto"](-0.2).startswith("RIDUTTIVO")

    def test_trascurabile(self):
        assert _F["mh384_verdetto"](0.0).startswith("TRASCURABILE")
        assert _F["mh384_verdetto"](0.0499).startswith("TRASCURABILE")

    def test_moderato(self):
        assert _F["mh384_verdetto"](0.05).startswith("MODERATO")
        assert _F["mh384_verdetto"](0.1499).startswith("MODERATO")

    def test_rilevante(self):
        assert _F["mh384_verdetto"](0.15).startswith("RILEVANTE")
        assert _F["mh384_verdetto"](0.2999).startswith("RILEVANTE")

    def test_dominante(self):
        assert _F["mh384_verdetto"](0.30).startswith("DOMINANTE")
        assert _F["mh384_verdetto"](math.inf).startswith("DOMINANTE")

    def test_demo_rilevante(self):
        assert _F["mh384_verdetto"](INCR).startswith("RILEVANTE")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_verdetto"](math.nan)


class TestPdfPnl:
    def test_non_negativa(self):
        xs = [MEAN - 6.0 * math.sqrt(VAR) + i * 0.01 * math.sqrt(VAR)
              for i in range(200)]
        for x in xs:
            assert _F["mh384_pdf_pnl"](x, A, B, S) >= 0.0

    def test_integra_uno(self):
        n = 2001
        lo = MEAN - 8.0 * math.sqrt(VAR)
        hi = MEAN + 8.0 * math.sqrt(VAR)
        h = (hi - lo) / (n - 1)
        tot = 0.0
        for i in range(n):
            x = lo + i * h
            fx = _F["mh384_pdf_pnl"](x, A, B, S)
            tot += (0.5 if i in (0, n - 1) else 1.0) * fx
        assert tot * h == pytest.approx(1.0, abs=1e-3)

    def test_fuori_supporto_zero(self):
        y0 = -A ** 2 / (4.0 * B)
        assert B < 0.0
        assert _F["mh384_pdf_pnl"](y0 + 1.0, A, B, S) == 0.0
        assert _F["mh384_pdf_pnl"](y0 - 100.0, A, B, S) > 0.0

    def test_b_zero_degenere_normale(self):
        sd = abs(A) * S
        for x in (-1000.0, 0.0, 1000.0):
            assert _F["mh384_pdf_pnl"](x, A, 0.0, S) == pytest.approx(
                _F["mh384_phi"](x / sd) / sd)

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_pdf_pnl"](0.0, A, B, 0.0)


class TestMappa:
    def _b(self):
        return _F["mh384_mappa"](S0, QTA, DELTA, GAMMA, SIG, T, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["var_delta"] == pytest.approx(VAR_D)
        assert b["var_dg"] == pytest.approx(VAR_DG)
        assert b["incr"] == pytest.approx(INCR)
        assert b["A"] == pytest.approx(A)
        assert b["B"] == pytest.approx(B)
        assert b["skew"] == pytest.approx(SKEW)
        assert b["kurt"] == pytest.approx(KURT)
        assert b["verdetto"].startswith("RILEVANTE")

    def test_coerenza(self):
        b = self._b()
        assert b["incr"] == pytest.approx(
            (b["var_dg"] - b["var_delta"]) / b["var_delta"])
        assert b["var_dg"] > b["var_delta"]
        assert b["sd"] == pytest.approx(math.sqrt(b["var"]))
        assert b["mean"] == pytest.approx(b["B"] * b["s"] ** 2)
        assert b["alpha"] == pytest.approx(ALPHA)

    def test_echo_input(self):
        b = self._b()
        assert b["s0"] == S0
        assert b["qta"] == QTA
        assert b["delta"] == DELTA
        assert b["gamma"] == GAMMA
        assert b["sigma"] == SIG
        assert b["t"] == T

    def test_sigma_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_mappa"](S0, QTA, DELTA, GAMMA, 0.0, T, ALPHA)

    def test_t_ko(self):
        with pytest.raises(ValueError):
            _F["mh384_mappa"](S0, QTA, DELTA, GAMMA, SIG, 0.0, ALPHA)
