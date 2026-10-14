"""Test tab386 'VaR ed ES con code pesanti (t-Student)': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh386_num", "mh386_t_pdf", "mh386_t_cdf", "mh386_t_ppf",
           "mh386_scale", "mh386_var_t", "mh386_es_t", "mh386_var_n",
           "mh386_es_n", "mh386_extra", "mh386_verdetto", "mh386_mappa")

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
TITLE436 = "📈 Martin ratio: rendimento per unita' di Ulcer Index"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
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
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE381 = "Component VaR: attribution del VaR per asset"
SIG = 10000.0
NU = 5
ALPHA = 0.99
Q = 3.3649308144304086
SCALE = 7745.966692414834
VAR_N = 23263.47874040841
ES_N = 26652.142203458054
VAR_T = 26064.642010858268
ES_T = 34488.34440777638
EXTRA = 0.2940177245227813
RATIO = 1.2940177245227813


class TestRegistry386:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 461
        assert "tab386" in dvars
        assert "tab386" in withs

    def test_titoli_allineati_381_382_383_384_385_386(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab381")] == TITLE381
        assert titoli[dvars.index("tab382")] == TITLE382
        assert titoli[dvars.index("tab383")] == TITLE383
        assert titoli[dvars.index("tab384")] == TITLE384
        assert titoli[dvars.index("tab385")] == TITLE385
        assert titoli[dvars.index("tab386")] == TITLE386

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab461"
        assert titoli[-1] == TITLE461
        assert withs[-1] == "tab461"


class TestNum:
    def test_num_ok(self):
        assert _F["mh386_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_num"](float("inf"), "x")


class TestTPdf:
    def test_zero_nu5(self):
        assert _F["mh386_t_pdf"](0.0, 5.0) == pytest.approx(0.379606689)

    def test_simmetria(self):
        assert _F["mh386_t_pdf"](1.5, 5.0) == pytest.approx(
            _F["mh386_t_pdf"](-1.5, 5.0))

    def test_nu_grande_tende_normale(self):
        phi0 = 1.0 / math.sqrt(2.0 * math.pi)
        assert _F["mh386_t_pdf"](0.0, 10000.0) == pytest.approx(
            phi0, rel=1e-3)

    def test_nu_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_t_pdf"](0.0, 2.0)
        with pytest.raises(ValueError):
            _F["mh386_t_pdf"](0.0, 1.0)


class TestTCdf:
    def test_zero(self):
        assert _F["mh386_t_cdf"](0.0, 5.0) == pytest.approx(0.5)

    def test_simmetria(self):
        assert _F["mh386_t_cdf"](-2.0, 5.0) == pytest.approx(
            1.0 - _F["mh386_t_cdf"](2.0, 5.0))

    def test_code(self):
        assert _F["mh386_t_cdf"](-100.0, 5.0) == 0.0
        assert _F["mh386_t_cdf"](100.0, 5.0) == 1.0
        assert _F["mh386_t_cdf"](-40.0, 5.0) < 1e-6
        assert _F["mh386_t_cdf"](30.0, 5.0) == pytest.approx(1.0, abs=1e-6)

    def test_nota(self):
        # t_{0.99, 5} = 3.3649299989 -> CDF = 0.99
        assert _F["mh386_t_cdf"](3.3649299989, 5.0) == pytest.approx(
            0.99, abs=1e-4)

    def test_nu_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_t_cdf"](0.0, 2.0)


class TestTPpf:
    def test_noto(self):
        assert _F["mh386_t_ppf"](0.99, 5.0) == pytest.approx(3.3649299989)

    def test_demo(self):
        assert _F["mh386_t_ppf"](ALPHA, NU) == pytest.approx(Q)

    def test_mediana(self):
        assert _F["mh386_t_ppf"](0.5, 5.0) == 0.0

    def test_simmetria(self):
        assert _F["mh386_t_ppf"](0.25, 5.0) == pytest.approx(
            -_F["mh386_t_ppf"](0.75, 5.0))

    def test_nu_grande_tende_normale(self):
        assert _F["mh386_t_ppf"](0.99, 10000.0) == pytest.approx(
            2.32634787404084, abs=1e-3)

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_t_ppf"](1.0, 5.0)
        with pytest.raises(ValueError):
            _F["mh386_t_ppf"](0.0, 5.0)

    def test_nu_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_t_ppf"](0.99, 2.0)


class TestScale:
    def test_demo(self):
        assert _F["mh386_scale"](SIG, NU) == pytest.approx(SCALE)

    def test_forma(self):
        assert _F["mh386_scale"](SIG, NU) == pytest.approx(
            SIG * math.sqrt((NU - 2.0) / NU))

    def test_zero(self):
        assert _F["mh386_scale"](0.0, NU) == 0.0

    def test_nu_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_scale"](SIG, 2.0)

    def test_sig_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_scale"](-1.0, NU)


class TestVarEsT:
    def test_demo_var(self):
        assert _F["mh386_var_t"](SIG, NU, ALPHA) == pytest.approx(VAR_T)

    def test_demo_es(self):
        assert _F["mh386_es_t"](SIG, NU, ALPHA) == pytest.approx(ES_T)

    def test_forma_chiusa(self):
        s = _F["mh386_scale"](SIG, NU)
        q = _F["mh386_t_ppf"](ALPHA, NU)
        f = _F["mh386_t_pdf"](q, NU)
        assert _F["mh386_var_t"](SIG, NU, ALPHA) == pytest.approx(s * q)
        assert _F["mh386_es_t"](SIG, NU, ALPHA) == pytest.approx(
            s * f / (1.0 - ALPHA) * (NU + q * q) / (NU - 1.0))

    def test_es_maggiore_var(self):
        assert _F["mh386_es_t"](SIG, NU, ALPHA) > _F["mh386_var_t"](
            SIG, NU, ALPHA)

    def test_coda_pesante_supera_normale(self):
        assert _F["mh386_es_t"](SIG, NU, ALPHA) > _F["mh386_es_n"](
            SIG, ALPHA)
        assert _F["mh386_var_t"](SIG, NU, ALPHA) > _F["mh386_var_n"](
            SIG, ALPHA)

    def test_nu_grande_tende_normale(self):
        assert _F["mh386_es_t"](SIG, 10000.0, ALPHA) == pytest.approx(
            _F["mh386_es_n"](SIG, ALPHA), rel=5e-3)
        assert _F["mh386_var_t"](SIG, 10000.0, ALPHA) == pytest.approx(
            _F["mh386_var_n"](SIG, ALPHA), rel=5e-3)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_var_t"](SIG, NU, 0.5)
        with pytest.raises(ValueError):
            _F["mh386_es_t"](SIG, NU, 1.0)

    def test_nu_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_var_t"](SIG, 2.0, ALPHA)
        with pytest.raises(ValueError):
            _F["mh386_es_t"](SIG, 1.5, ALPHA)


class TestVarEsN:
    def test_demo(self):
        assert _F["mh386_var_n"](SIG, ALPHA) == pytest.approx(VAR_N)
        assert _F["mh386_es_n"](SIG, ALPHA) == pytest.approx(ES_N)

    def test_forma_chiusa(self):
        from statistics import NormalDist
        z = NormalDist().inv_cdf(ALPHA)
        phi = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
        assert _F["mh386_var_n"](SIG, ALPHA) == pytest.approx(SIG * z)
        assert _F["mh386_es_n"](SIG, ALPHA) == pytest.approx(
            SIG * phi / (1.0 - ALPHA))

    def test_ratio_normale_99(self):
        assert ES_N / VAR_N == pytest.approx(1.1456, abs=1e-3)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_var_n"](SIG, 0.5)
        with pytest.raises(ValueError):
            _F["mh386_es_n"](SIG, 1.0)


class TestExtraVerdetto:
    def test_demo(self):
        assert _F["mh386_extra"](ES_T, ES_N) == pytest.approx(EXTRA)
        assert _F["mh386_verdetto"](EXTRA).startswith("RILEVANTE")

    def test_bordi(self):
        assert _F["mh386_verdetto"](0.0).startswith("CONTENUTA")
        assert _F["mh386_verdetto"](0.0999).startswith("CONTENUTA")
        assert _F["mh386_verdetto"](0.10).startswith("MODERATA")
        assert _F["mh386_verdetto"](0.2499).startswith("MODERATA")
        assert _F["mh386_verdetto"](0.25).startswith("RILEVANTE")
        assert _F["mh386_verdetto"](0.4999).startswith("RILEVANTE")
        assert _F["mh386_verdetto"](0.50).startswith("SEVERA")
        assert _F["mh386_verdetto"](math.inf).startswith("SEVERA")

    def test_extra_inf(self):
        assert _F["mh386_extra"](100.0, 0.0) == math.inf

    def test_extra_zero(self):
        assert _F["mh386_extra"](0.0, 0.0) == 0.0

    def test_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_verdetto"](-0.01)

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_verdetto"](float("nan"))


class TestMappa:
    def _b(self):
        return _F["mh386_mappa"](SIG, NU, ALPHA)

    def test_demo(self):
        b = self._b()
        assert b["sig"] == SIG
        assert b["nu"] == NU
        assert b["alpha"] == ALPHA
        assert b["scale"] == pytest.approx(SCALE)
        assert b["q"] == pytest.approx(Q)
        assert b["var_n"] == pytest.approx(VAR_N)
        assert b["es_n"] == pytest.approx(ES_N)
        assert b["var_t"] == pytest.approx(VAR_T)
        assert b["es_t"] == pytest.approx(ES_T)
        assert b["extra"] == pytest.approx(EXTRA)
        assert b["ratio"] == pytest.approx(RATIO)
        assert b["verdetto"].startswith("RILEVANTE")

    def test_coerenza(self):
        b = self._b()
        assert b["extra"] == pytest.approx(b["es_t"] / b["es_n"] - 1.0)
        assert b["ratio"] == pytest.approx(b["es_t"] / b["es_n"])
        assert b["var_t"] == pytest.approx(b["scale"] * b["q"])

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_mappa"](SIG, NU, 0.5)

    def test_nu_ko(self):
        with pytest.raises(ValueError):
            _F["mh386_mappa"](SIG, 2.0, ALPHA)
