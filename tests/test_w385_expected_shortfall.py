"""Test tab385 'Expected Shortfall: misura di rischio coerente': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh385_num", "mh385_phi", "mh385_ppf", "mh385_port_sigma",
           "mh385_var", "mh385_es", "mh385_comp_es", "mh385_extra",
           "mh385_verdetto", "mh385_tail_prob", "mh385_mappa")

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
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
E1 = 10000.0
E2 = 8000.0
S1 = 0.15
S2 = 0.2
RHO = 0.6
ALPHA = 0.99
SIG = 2773.0849247724095
VAR = 6451.160219279
ES = 7390.865375730005
EXTRA = 0.14566451994832486
RATIO = 1.1456645199483249
CES1 = 3546.46205935549
CES2 = 3844.403316374515
TAIL2 = 1.6381173918444958e-06


class TestRegistry385:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 412
        assert "tab385" in dvars
        assert "tab385" in withs

    def test_titoli_allineati_380_381_382_383_384_385(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab380")] == TITLE380
        assert titoli[dvars.index("tab381")] == TITLE381
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384
        assert titoli[dvars.index("tab385")] == TITLE385

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab412"
        assert titoli[-1] == TITLE412
        assert withs[-1] == "tab412"


class TestNum:
    def test_num_ok(self):
        assert _F["mh385_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_num"](float("inf"), "x")


class TestPhiPpf:
    def test_phi_zero(self):
        assert _F["mh385_phi"](0.0) == pytest.approx(0.3989422804014327)

    def test_phi_simmetria(self):
        assert _F["mh385_phi"](1.5) == pytest.approx(_F["mh385_phi"](-1.5))

    def test_ppf_nota(self):
        assert _F["mh385_ppf"](0.99) == pytest.approx(2.32634787404084)

    def test_ppf_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_ppf"](1.0)
        with pytest.raises(ValueError):
            _F["mh385_ppf"](0.0)


class TestPortSigma:
    def test_demo(self):
        assert _F["mh385_port_sigma"](E1, E2, S1, S2, RHO) == pytest.approx(SIG)

    def test_forma_chiusa(self):
        v1, v2 = E1 * S1, E2 * S2
        att = math.sqrt(v1 ** 2 + v2 ** 2 + 2.0 * RHO * v1 * v2)
        assert _F["mh385_port_sigma"](E1, E2, S1, S2, RHO) == pytest.approx(att)

    def test_rho_meno_uno(self):
        v1, v2 = E1 * S1, E2 * S2
        assert _F["mh385_port_sigma"](
            E1, E2, S1, S2, -1.0) == pytest.approx(abs(v1 - v2))

    def test_rho_uno(self):
        v1, v2 = E1 * S1, E2 * S2
        assert _F["mh385_port_sigma"](
            E1, E2, S1, S2, 1.0) == pytest.approx(v1 + v2)

    def test_vuoto_zero(self):
        assert _F["mh385_port_sigma"](0.0, 0.0, S1, S2, RHO) == 0.0

    def test_rho_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_port_sigma"](E1, E2, S1, S2, 1.5)

    def test_s_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_port_sigma"](E1, E2, 0.0, S2, RHO)

    def test_e_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_port_sigma"](-1.0, E2, S1, S2, RHO)


class TestVarEs:
    def test_demo_var(self):
        assert _F["mh385_var"](SIG, ALPHA) == pytest.approx(VAR)

    def test_demo_es(self):
        assert _F["mh385_es"](SIG, ALPHA) == pytest.approx(ES)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert _F["mh385_var"](SIG, ALPHA) == pytest.approx(SIG * z)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh385_es"](SIG, ALPHA) == pytest.approx(
            SIG * phi / (1.0 - ALPHA))

    def test_es_maggiore_var(self):
        assert _F["mh385_es"](SIG, ALPHA) > _F["mh385_var"](SIG, ALPHA)

    def test_ratio_normale_99(self):
        assert ES / VAR == pytest.approx(1.1456, abs=1e-3)

    def test_sig_zero(self):
        assert _F["mh385_var"](0.0, ALPHA) == 0.0
        assert _F["mh385_es"](0.0, ALPHA) == 0.0

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_var"](SIG, 1.0)
        with pytest.raises(ValueError):
            _F["mh385_es"](SIG, 0.0)


class TestCompEs:
    def test_demo(self):
        c1, c2 = _F["mh385_comp_es"](E1, E2, S1, S2, RHO, ALPHA)
        assert c1 == pytest.approx(CES1)
        assert c2 == pytest.approx(CES2)

    def test_somma_eulero(self):
        c1, c2 = _F["mh385_comp_es"](E1, E2, S1, S2, RHO, ALPHA)
        assert c1 + c2 == pytest.approx(ES)

    def test_vuoto(self):
        assert _F["mh385_comp_es"](
            0.0, 0.0, S1, S2, RHO, ALPHA) == (0.0, 0.0)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_comp_es"](E1, E2, S1, S2, RHO, 1.5)


class TestExtraVerdetto:
    def test_demo(self):
        assert _F["mh385_extra"](ES, VAR) == pytest.approx(EXTRA)
        assert _F["mh385_verdetto"](EXTRA).startswith("MODERATA")

    def test_bordi(self):
        assert _F["mh385_verdetto"](0.0).startswith("CONTENUTA")
        assert _F["mh385_verdetto"](0.0999).startswith("CONTENUTA")
        assert _F["mh385_verdetto"](0.10).startswith("MODERATA")
        assert _F["mh385_verdetto"](0.1999).startswith("MODERATA")
        assert _F["mh385_verdetto"](0.20).startswith("RILEVANTE")
        assert _F["mh385_verdetto"](0.3499).startswith("RILEVANTE")
        assert _F["mh385_verdetto"](0.35).startswith("SEVERA")
        assert _F["mh385_verdetto"](math.inf).startswith("SEVERA")

    def test_extra_inf(self):
        assert _F["mh385_extra"](100.0, 0.0) == math.inf

    def test_extra_zero(self):
        assert _F["mh385_extra"](0.0, 0.0) == 0.0

    def test_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_verdetto"](-0.01)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_verdetto"](float("nan"))


class TestTailProb:
    def test_demo(self):
        assert _F["mh385_tail_prob"](SIG, VAR, 2.0) == pytest.approx(TAIL2)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        att = 1.0 - NormalDist().cdf(2.0 * VAR / SIG)
        assert _F["mh385_tail_prob"](SIG, VAR, 2.0) == pytest.approx(att)

    def test_piccola(self):
        assert 0.0 < _F["mh385_tail_prob"](SIG, VAR, 2.0) < 0.01

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_tail_prob"](0.0, VAR, 2.0)


class TestMappa:
    def _b(self):
        return _F["mh385_mappa"](E1, E2, S1, S2, RHO, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["sig"] == pytest.approx(SIG)
        assert b["var"] == pytest.approx(VAR)
        assert b["es"] == pytest.approx(ES)
        assert b["extra"] == pytest.approx(EXTRA)
        assert b["ratio"] == pytest.approx(RATIO)
        assert b["ces1"] == pytest.approx(CES1)
        assert b["ces2"] == pytest.approx(CES2)
        assert b["tail2"] == pytest.approx(TAIL2)
        assert b["verdetto"].startswith("MODERATA")

    def test_coerenza(self):
        b = self._b()
        assert b["ces1"] + b["ces2"] == pytest.approx(b["es"])
        assert b["es"] > b["var"]
        assert b["extra"] == pytest.approx((b["es"] - b["var"]) / b["var"])
        assert b["ratio"] == pytest.approx(b["es"] / b["var"])

    def test_echo_input(self):
        b = self._b()
        assert b["e1"] == E1
        assert b["e2"] == E2
        assert b["s1"] == S1
        assert b["s2"] == S2
        assert b["rho"] == RHO
        assert b["alpha"] == ALPHA

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh385_mappa"](E1, E2, S1, S2, RHO, 1.5)
