"""Test tab291 '📊💹 Sharpe & Sortino: la strategia rende davvero?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab291.
"""

import math
import re
import statistics
from pathlib import Path

import pytest

from appfuncs import load

_F = load("ss291_num", "ss291_pos", "ss291_parse_serie", "ss291_serie_demo",
          "ss291_rendimenti", "ss291_rendimento_annuo",
          "ss291_volatilita_annua", "ss291_sharpe", "ss291_sortino",
          "ss291_drawdown_serie", "ss291_max_drawdown", "ss291_calmar",
          "ss291_statistiche", "ss291_verdetto", "_ss291_ratio")
ss291_num = _F["ss291_num"]
ss291_pos = _F["ss291_pos"]
ss291_parse_serie = _F["ss291_parse_serie"]
ss291_serie_demo = _F["ss291_serie_demo"]
ss291_rendimenti = _F["ss291_rendimenti"]
ss291_rendimento_annuo = _F["ss291_rendimento_annuo"]
ss291_volatilita_annua = _F["ss291_volatilita_annua"]
ss291_sharpe = _F["ss291_sharpe"]
ss291_sortino = _F["ss291_sortino"]
ss291_drawdown_serie = _F["ss291_drawdown_serie"]
ss291_max_drawdown = _F["ss291_max_drawdown"]
ss291_calmar = _F["ss291_calmar"]
ss291_statistiche = _F["ss291_statistiche"]
ss291_verdetto = _F["ss291_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
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
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"

EQ = [100.0, 102.0, 101.0, 105.0, 103.0, 108.0]
R = [0.02, -1.0 / 102.0, 4.0 / 101.0, -2.0 / 105.0, 5.0 / 103.0]


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab291:
    def test_tab291_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 341
        assert TITLE291 in titoli
        assert "tab291" in dvars
        assert "tab291" in withs
        assert titoli[dvars.index("tab291")] == TITLE291
        assert titoli[-1] == TITLE341
        keys = re.findall(r'key="(ss291_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_289_290_291(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab289")] == TITLE289
        assert titoli[dvars.index("tab290")] == TITLE290
        assert titoli[dvars.index("tab291")] == TITLE291


class TestSs291ValidatoriParse:
    def test_num_ok(self):
        assert ss291_num(1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            ss291_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            ss291_num(float("nan"), "x")

    def test_pos_zero_ko(self):
        with pytest.raises(ValueError):
            ss291_pos(0.0, "x")

    def test_parse_ok(self):
        assert ss291_parse_serie("100\n101,5\n# commento\n\n102") == \
            [100.0, 101.5, 102.0]

    def test_parse_riga_sporca_ko(self):
        with pytest.raises(ValueError):
            ss291_parse_serie("100\nabc")

    def test_parse_troppo_corta_ko(self):
        with pytest.raises(ValueError):
            ss291_parse_serie("100")


class TestSs291SerieDemo:
    def test_deterministica(self):
        a = ss291_serie_demo(7, 252, 1_000_000, 0.0008, 0.012)
        b = ss291_serie_demo(7, 252, 1_000_000, 0.0008, 0.012)
        assert a == b
        assert len(a) == 252
        assert a[0] == 1_000_000.0

    def test_seed_diversi_differiscono(self):
        a = ss291_serie_demo(7, 50, 1000, 0.001, 0.01)
        b = ss291_serie_demo(8, 50, 1000, 0.001, 0.01)
        assert a != b

    def test_vol_zero_drift_puro(self):
        a = ss291_serie_demo(1, 4, 1000.0, 0.01, 0.0)
        assert a == pytest.approx([1000.0, 1010.0, 1020.1, 1030.301])

    def test_seed_non_int_ko(self):
        with pytest.raises(ValueError):
            ss291_serie_demo(1.5, 10, 1000, 0.0, 0.01)

    def test_giorni_ko(self):
        with pytest.raises(ValueError):
            ss291_serie_demo(1, 1, 1000, 0.0, 0.01)


class TestSs291Rendimenti:
    def test_valori(self):
        r = ss291_rendimenti(EQ)
        assert r == pytest.approx(R)

    def test_equity_non_positiva_ko(self):
        with pytest.raises(ValueError):
            ss291_rendimenti([100.0, 0.0, 101.0])


class TestSs291RendimentoVol:
    def test_rendimento_annuo(self):
        assert ss291_rendimento_annuo(EQ, 252) == pytest.approx(
            (108.0 / 100.0) ** (252.0 / 5.0) - 1.0)

    def test_volatilita_annua(self):
        assert ss291_volatilita_annua(EQ, 252) == pytest.approx(
            statistics.stdev(R) * math.sqrt(252))


class TestSs291SharpeSortino:
    def test_sharpe_formula(self):
        rf = 0.02
        att = (statistics.mean(R) * 252 - rf) / (
            statistics.stdev(R) * math.sqrt(252))
        assert ss291_sharpe(EQ, rf, 252) == pytest.approx(att)

    def test_sharpe_vol_nulla_inf(self):
        eq = ss291_serie_demo(3, 10, 1000.0, 0.01, 0.0)
        assert ss291_sharpe(eq) == math.inf

    def test_sortino_formula(self):
        mar_g = (1.0 + 0.0) ** (1.0 / 252) - 1.0
        dd2 = sum(min(0.0, x - mar_g) ** 2 for x in R) / len(R)
        att = (sum(R) / len(R) * 252) / (math.sqrt(dd2) * math.sqrt(252))
        assert ss291_sortino(EQ, 0.0, 252) == pytest.approx(att)

    def test_sortino_maggiore_sharpe_con_upside(self):
        # con upside forte e poco downside, sortino > sharpe
        assert ss291_sortino(EQ) > ss291_sharpe(EQ)


class TestSs291Drawdown:
    def test_serie(self):
        dd = ss291_drawdown_serie(EQ)
        assert dd[0] == pytest.approx(0.0)
        assert dd[1] == pytest.approx(0.0)
        assert dd[2] == pytest.approx((101.0 - 102.0) / 102.0)

    def test_max_drawdown(self):
        m = ss291_max_drawdown(EQ)
        assert m["max_dd"] == pytest.approx((105.0 - 103.0) / 105.0)
        assert m["picco_idx"] == 3
        assert m["valle_idx"] == 4

    def test_senza_drawdown(self):
        m = ss291_max_drawdown([100.0, 101.0, 102.0])
        assert m["max_dd"] == pytest.approx(0.0)


class TestSs291Calmar:
    def test_formula(self):
        assert ss291_calmar(EQ, 252) == pytest.approx(
            ss291_rendimento_annuo(EQ, 252) / ss291_max_drawdown(EQ)["max_dd"])


class TestSs291Statistiche:
    def test_chiavi_e_coerenza(self):
        s = ss291_statistiche(EQ)
        assert s["n_giorni"] == 5
        assert s["pnl"] == pytest.approx(8.0)
        assert s["sharpe"] == pytest.approx(ss291_sharpe(EQ))
        assert s["sortino"] == pytest.approx(ss291_sortino(EQ))
        assert s["max_drawdown"] == pytest.approx(
            ss291_max_drawdown(EQ)["max_dd"])
        assert s["win_rate"] == pytest.approx(3.0 / 5.0)


class TestSs291Verdetto:
    def test_eccellente(self):
        assert ss291_verdetto(2.5, 1.0)["verdetto"] == "eccellente"

    def test_accettabile(self):
        assert ss291_verdetto(1.2, 1.0)["verdetto"] == "accettabile"

    def test_insufficiente(self):
        assert ss291_verdetto(0.5, 1.0)["verdetto"] == "insufficiente"

    def test_soglia_non_positiva_ko(self):
        with pytest.raises(ValueError):
            ss291_verdetto(1.2, 0.0)
