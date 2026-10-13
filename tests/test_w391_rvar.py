"""Test tab391 '🔀📊 RVaR: la media dei quantili tra VaR ed ES': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh391_num", "mh391_var", "mh391_es", "mh391_rvar",
           "mh391_rvar_quad", "mh391_ratio", "mh391_verdetto",
           "mh391_mappa")

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
TITLE416 = "🎚️ Kappa ratio: Omega e Sortino sono lo stesso strumento"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE428 = "⏱️ Tempo sott'acqua: durata dei drawdown e recupero"
TITLE430 = "🔄 Recupero dal drawdown: quanto rimbalzo serve per tornare al picco"
TITLE432 = "⚖️ Sortino ratio: rendimento per unita' di volatilita' negativa"
TITLE434 = "📉 Burke ratio: rendimento per unita' di drawdown quadratico"
TITLE413 = "📐 Sharpe corretto: il rendimento per unita' di rischio con code grasse"
TITLE415 = "🎯 Deflated Sharpe ratio: lo Sharpe sopravvive ai backtest multipli?"
TITLE417 = "🔺 Farinelli-Tibiletti: Omega e upside potential in un'unica formula"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE427 = "🛡 CDaR: la perdita media dei peggiori drawdown"
TITLE429 = "🎯 Attribuzione del drawdown: chi ha causato il peggior calo"
TITLE431 = "📐 Calmar ratio: rendimento per unita' di peggior perdita"
TITLE433 = "🧮 Omega ratio: guadagni pesati contro perdite pesate"
TITLE435 = "🎯 Kappa ratio (Kappa-3): rendimento per unita' di coda cubica"
TITLE390 = "🎯📈 EVaR: il bound di Chernoff piu' conservativo"
TITLE389 = "🌀📈 Wang transform: misura distorsiva del rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
MU = 0.0
SIG = 10000.0
ALPHA = 0.975
BETA = 0.99
RVAR = 21195.28506771822
VAR_ = 19599.639845400536
ES_ = 23378.027922014157
RATIO = 0.906632721049985


class TestRegistry391:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 435
        assert "tab391" in dvars
        assert "tab391" in withs

    def test_titoli_allineati_386_387_388_389_390_391(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab386")] == TITLE386
        assert titoli[dvars.index("tab387")] == TITLE387
        assert titoli[dvars.index("tab388")] == TITLE388
        assert titoli[dvars.index("tab389")] == TITLE389
        assert titoli[dvars.index("tab390")] == TITLE390
        assert titoli[dvars.index("tab391")] == TITLE391

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab435"
        assert titoli[-1] == TITLE435
        assert withs[-1] == "tab435"


class TestNum:
    def test_num_ok(self):
        assert _F["mh391_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_num"](float("inf"), "x")


class TestVarEs:
    def test_var_demo(self):
        assert _F["mh391_var"](MU, SIG, ALPHA) == VAR_

    def test_var_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        assert abs(_F["mh391_var"](MU, SIG, ALPHA) - (MU + SIG * z)) < 1e-9

    def test_var_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_var"](MU, SIG, 0.5)

    def test_var_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_var"](MU, -1.0, ALPHA)

    def test_es_demo(self):
        assert _F["mh391_es"](MU, SIG, ALPHA) == ES_

    def test_es_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert abs(_F["mh391_es"](MU, SIG, ALPHA) -
                   (MU + SIG * phi / (1.0 - ALPHA))) < 1e-9

    def test_es_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_es"](MU, SIG, 1.0)

    def test_es_sig_zero(self):
        assert _F["mh391_es"](2000.0, 0.0, ALPHA) == 2000.0

    def test_es_supera_var(self):
        assert _F["mh391_es"](MU, SIG, ALPHA) > _F["mh391_var"](MU, SIG,
                                                               ALPHA)


class TestRvar:
    def test_demo(self):
        assert _F["mh391_rvar"](MU, SIG, ALPHA, BETA) == RVAR

    def test_quad_crosscheck(self):
        q = _F["mh391_rvar_quad"](MU, SIG, ALPHA, BETA)
        assert abs(q - RVAR) / RVAR < 1e-6

    def test_quad_altro_punto(self):
        q = _F["mh391_rvar_quad"](MU, SIG, 0.95, 0.975, 1024)
        c = _F["mh391_rvar"](MU, SIG, 0.95, 0.975)
        assert abs(q - c) / c < 1e-6

    def test_limite_beta_verso_alpha(self):
        r = _F["mh391_rvar"](MU, SIG, ALPHA, ALPHA + 1e-4)
        assert abs(r - VAR_) < 20.0

    def test_limite_beta_verso_uno(self):
        r = _F["mh391_rvar"](MU, SIG, ALPHA, 1.0 - 1e-6)
        assert abs(r - ES_) < 5.0

    def test_monotonia_beta(self):
        r1 = _F["mh391_rvar"](MU, SIG, ALPHA, 0.98)
        r2 = _F["mh391_rvar"](MU, SIG, ALPHA, 0.985)
        r3 = _F["mh391_rvar"](MU, SIG, ALPHA, 0.995)
        assert r1 < r2 < r3

    def test_bounds(self):
        assert VAR_ <= RVAR <= ES_

    def test_traslazione(self):
        assert abs(_F["mh391_rvar"](5000.0, SIG, ALPHA, BETA) -
                   (RVAR + 5000.0)) < 1e-9

    def test_scaling(self):
        assert abs(_F["mh391_rvar"](0.0, 2 * SIG, ALPHA, BETA) -
                   2 * RVAR) < 1e-9

    def test_deterministico(self):
        assert _F["mh391_rvar"](MU, SIG, ALPHA, BETA) == \
            _F["mh391_rvar"](MU, SIG, ALPHA, BETA)

    def test_beta_le_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar"](MU, SIG, ALPHA, ALPHA)

    def test_beta_uno_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar"](MU, SIG, ALPHA, 1.0)

    def test_intervallo_stretto_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar"](MU, SIG, ALPHA, ALPHA + 1e-12)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar"](MU, SIG, 0.4, BETA)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar"](MU, -1.0, ALPHA, BETA)

    def test_quad_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar_quad"](MU, SIG, ALPHA, BETA, 8)

    def test_quad_dispari_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_rvar_quad"](MU, SIG, ALPHA, BETA, 17)


class TestRatioVerdetto:
    def test_demo(self):
        assert _F["mh391_ratio"](RVAR, ES_) == RATIO

    def test_banda_intermedia(self):
        assert 0.85 < RATIO <= 0.95

    def test_bordi(self):
        assert _F["mh391_verdetto"](0.85).startswith("VICINA AL VaR")
        assert _F["mh391_verdetto"](0.8501).startswith("INTERMEDIA")
        assert _F["mh391_verdetto"](0.95).startswith("INTERMEDIA")
        assert _F["mh391_verdetto"](0.9501).startswith("VICINA ALL'ES")
        assert _F["mh391_verdetto"](0.0).startswith("VICINA AL VaR")
        assert _F["mh391_verdetto"](1.0).startswith("VICINA ALL'ES")

    def test_clamp(self):
        assert _F["mh391_verdetto"](-0.5).startswith("VICINA AL VaR")
        assert _F["mh391_verdetto"](1.5).startswith("VICINA ALL'ES")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_verdetto"](float("nan"))

    def test_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_verdetto"](float("inf"))

    def test_es_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_ratio"](RVAR, 0.0)


class TestMappa:
    def _b(self):
        return _F["mh391_mappa"](MU, SIG, ALPHA, BETA)

    def test_demo(self):
        b = self._b()
        assert b["var"] == VAR_
        assert b["es"] == ES_
        assert b["rvar"] == RVAR
        assert b["ratio"] == RATIO
        assert b["alpha"] == ALPHA
        assert b["beta"] == BETA
        assert b["verdetto"].startswith("INTERMEDIA")

    def test_coerenza(self):
        b = self._b()
        assert b["var"] <= b["rvar"] <= b["es"]
        assert abs(b["ratio"] - b["rvar"] / b["es"]) < 1e-15

    def test_mappa_beta_ko(self):
        with pytest.raises(ValueError):
            _F["mh391_mappa"](MU, SIG, ALPHA, ALPHA)
