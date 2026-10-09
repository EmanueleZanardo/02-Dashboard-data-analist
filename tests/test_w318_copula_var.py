"""Test tab318 '🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della copula t-Student: validatori,
CDF t via Simpson, tail dependence, simulazione equicorrelata gaussiana vs t
(deterministica), VaR/ES, breccia congiunta, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh318_num", "mh318_conf", "mh318_rho", "mh318_nu", "mh318_nsim",
           "mh318_parse_book", "mh318_norm_ppf", "mh318_t_cdf",
           "mh318_tail_dep", "mh318_rng", "mh318_quantile", "mh318_simula",
           "mh318_risultato", "mh318_verdetto")

TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
BOOK_DEMO = 'Gas TTF front-month;2500000;3,2;gas\nPower DE baseload Q1-27;1800000;2,8;power\nCO2 EUA Dic-26;900000;2,5;co2\nSpread PSV-TTF;600000;4,1;basis\nSpark spread CCGT 55%;1200000;3,6;power\nCarbone API2 ARA;700000;3,0;coal'
Q_DEMO = 99.0
RHO_DEMO = 0.5
NU_DEMO = 5
NSIM_DEMO = 10000

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_POS = 6
VAR_G = 438132.4632483595
ES_G = 514365.47922748973
VAR_T = 652930.2451757772
ES_T = 839821.5846891706
GAP = 0.4902576274190794
GAP_EUR = 214797.78192741773
LAMBDA = 0.207031233606822
JOINT = 0.049
STANDALONE = [186107.82992326727, 117247.93285165836, 52342.82716591892, 57228.15770140467, 100498.22815856434, 48853.30535485766]
STATO = "code congiunte pericolose"
VERDETTO = 'code congiunte pericolose: il VaR t-Student supera del 49.0% quello gaussiano (652,930 vs 438,132 euro): in stress le code si muovono insieme, aumenta il buffer.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh318_risultato"](BOOK_DEMO, Q_DEMO, RHO_DEMO, NU_DEMO,
                                 NSIM_DEMO)


class TestRegistry318:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 344
        assert TITLE318 in titoli
        assert "tab318" in dvars
        assert "    with tab318:" in src

    def test_titoli_allineati_316_317_318(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab316")] == TITLE316
        assert titoli[dvars.index("tab317")] == TITLE317
        assert titoli[dvars.index("tab318")] == TITLE318

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE344
        assert dvars[-1] == "tab344"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh318_conf"](99.0) == pytest.approx(0.01)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh318_conf"](97.5)

    def test_rho_ok(self):
        assert _F["mh318_rho"](0.5) == 0.5
        assert _F["mh318_rho"](0.0) == 0.0
        assert _F["mh318_rho"](0.99) == 0.99

    def test_rho_ko(self):
        for bad in (-0.1, 1.0, 1.5):
            with pytest.raises(ValueError):
                _F["mh318_rho"](bad)

    def test_nu_ok(self):
        assert _F["mh318_nu"](5) == 5
        assert _F["mh318_nu"](5.0) == 5

    def test_nu_ko(self):
        for bad in (1, 31, 4.5):
            with pytest.raises(ValueError):
                _F["mh318_nu"](bad)

    def test_nsim_ko(self):
        for bad in (999, 50001, 10000.5):
            with pytest.raises(ValueError):
                _F["mh318_nsim"](bad)

    def test_parse_book_ok(self):
        b = _F["mh318_parse_book"](BOOK_DEMO)
        assert len(b) == 6
        assert b[0]["nome"] == "Gas TTF front-month"
        assert b[0]["nozionale"] == 2500000.0
        assert b[0]["vol"] == pytest.approx(0.032)
        assert b[0]["segmento"] == "gas"

    def test_parse_book_ko(self):
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("solo una posizione;1000;2;gas")
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("a;1000;2\nb;2000;3;power")
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("a;-1000;2;gas\nb;2000;3;power")
        with pytest.raises(ValueError):
            _F["mh318_parse_book"]("a;1000;0;gas\nb;2000;3;power")

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x"):
            with pytest.raises(ValueError):
                _F["mh318_num"](bad, "t")


class TestTCdf:
    def test_zero(self):
        assert _F["mh318_t_cdf"](0.0, 5.0) == 0.5

    def test_simmetria(self):
        assert _F["mh318_t_cdf"](-1.7, 5.0) == pytest.approx(
            1.0 - _F["mh318_t_cdf"](1.7, 5.0))

    def test_valore_noto(self):
        # t_{30, 0.975} = 2.0423 (valore critico noto)
        assert _F["mh318_t_cdf"](2.042, 30.0) == pytest.approx(0.975, abs=2e-3)

    def test_monotonia(self):
        c = _F["mh318_t_cdf"]
        assert c(-3.0, 5.0) < c(-1.0, 5.0) < 0.5 < c(1.0, 5.0) < c(3.0, 5.0)

    def test_converge_normale(self):
        # nu grande -> CDF piu' vicina alla normale (convergenza monotona)
        import statistics
        phi = statistics.NormalDist().cdf(1.0)
        c = _F["mh318_t_cdf"]
        assert abs(c(1.0, 30.0) - phi) < abs(c(1.0, 5.0) - phi)
        assert abs(c(1.0, 30.0) - phi) < 0.01


class TestTailDep:
    def test_cresce_in_rho(self):
        td = _F["mh318_tail_dep"]
        assert td(0.3, 5.0) < td(0.5, 5.0) < td(0.9, 5.0)

    def test_decresce_in_nu(self):
        td = _F["mh318_tail_dep"]
        assert td(0.5, 3.0) > td(0.5, 5.0) > td(0.5, 30.0)

    def test_valori(self):
        td = _F["mh318_tail_dep"]
        assert td(0.9, 3.0) > 0.5
        assert td(0.5, 30.0) < 0.05
        assert td(0.0, 5.0) < 0.06
        assert td(0.5, 5.0) == pytest.approx(LAMBDA)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh318_tail_dep"](1.0, 5.0)
        with pytest.raises(ValueError):
            _F["mh318_tail_dep"](0.5, 1.0)


class TestSimula:
    def _book(self):
        return _F["mh318_parse_book"](BOOK_DEMO)

    def test_determinismo(self):
        b = self._book()
        s1 = _F["mh318_simula"](b, 0.5, 5, 2000, 99.0)
        s2 = _F["mh318_simula"](b, 0.5, 5, 2000, 99.0)
        assert s1["perdite_g"] == s2["perdite_g"]
        assert s1["perdite_t"] == s2["perdite_t"]
        assert s1["joint_breach"] == s2["joint_breach"]

    def test_lunghezze_e_range(self):
        b = self._book()
        s = _F["mh318_simula"](b, 0.5, 5, 2000, 99.0)
        assert len(s["perdite_g"]) == len(s["perdite_t"]) == 2000
        assert len(s["standalone"]) == 6
        assert 0.0 <= s["joint_breach"] <= 1.0

    def test_t_piu_grassa_di_gauss(self):
        b = self._book()
        s = _F["mh318_simula"](b, 0.5, 5, NSIM_DEMO, 99.0)
        q = _F["mh318_quantile"]
        assert q(s["perdite_t"], 0.99) > q(s["perdite_g"], 0.99)

    def test_diversificazione_rho_zero(self):
        b = self._book()
        s = _F["mh318_simula"](b, 0.0, 5, 5000, 99.0)
        q = _F["mh318_quantile"]
        assert q(s["perdite_g"], 0.99) < sum(s["standalone"])

    def test_rng_deterministico(self):
        u1, u2 = _F["mh318_rng"](20261008), _F["mh318_rng"](20261008)
        assert [u1() for _ in range(5)] == [u2() for _ in range(5)]
        assert all(0.0 < u1() < 1.0 for _ in range(10))


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n_pos"] == N_POS == 6
        assert ris["q"] == Q_DEMO
        assert ris["rho"] == RHO_DEMO
        assert ris["nu"] == NU_DEMO
        assert ris["nsim"] == NSIM_DEMO
        assert ris["var_g"] == VAR_G
        assert ris["es_g"] == ES_G
        assert ris["var_t"] == VAR_T
        assert ris["es_t"] == ES_T
        assert ris["gap"] == GAP
        assert ris["gap_eur"] == GAP_EUR
        assert ris["lambda"] == LAMBDA
        assert ris["joint"] == JOINT
        assert ris["standalone"] == STANDALONE
        assert ris["var_t"] > ris["var_g"] > 0.0
        assert ris["es_t"] >= ris["var_t"]
        assert ris["gap"] == pytest.approx(
            (ris["var_t"] - ris["var_g"]) / ris["var_g"])

    def test_nomi_segmenti(self):
        ris = _ris_demo()
        assert ris["nomi"][0] == "Gas TTF front-month"
        assert ris["segmenti"][3] == "basis"
        assert len(ris["perdite_g"]) == NSIM_DEMO


class TestVerdetto:
    def _base(self, **kw):
        ris = _ris_demo()
        ris.update(kw)
        return ris

    def test_verdetto_demo(self):
        assert _F["mh318_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_pericolose(self):
        v = _F["mh318_verdetto"](
            self._base(gap=0.49, var_t=650000.0, var_g=438000.0))
        assert v.startswith("code congiunte pericolose")

    def test_stato_materiali(self):
        v = _F["mh318_verdetto"](
            self._base(gap=0.15, var_t=500000.0, var_g=435000.0, joint=0.01))
        assert v.startswith("code congiunte materiali")

    def test_stato_breccia(self):
        v = _F["mh318_verdetto"](self._base(gap=0.05, joint=0.08))
        assert v.startswith("breccia congiunta frequente")

    def test_stato_modesta(self):
        v = _F["mh318_verdetto"](self._base(gap=0.05, joint=0.01))
        assert v.startswith("differenza modesta")

    def test_stato_nessuna(self):
        v = _F["mh318_verdetto"](self._base(gap=0.01, joint=0.01))
        assert v.startswith("nessuna differenza apprezzabile")
