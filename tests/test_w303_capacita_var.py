"""Test tab303 '🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab303. Capacita' VaR: il max nozionale di un
candidato (vol + correlazione al book) con VaR(book+x) <= limite, soluzione
esatta dell'equazione quadratica (follow-up del filone rischio
tab297 marginal VaR + tab298 limite VaR).
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cf303_num", "cf303_conf", "cf303_corr", "cf303_limite",
          "cf303_parse_book", "cf303_norm_cdf", "cf303_norm_ppf",
          "cf303_sigma2_book", "cf303_var_book", "cf303_capacita",
          "cf303_curva", "cf303_verdetto")
cf303_num = _F["cf303_num"]
cf303_conf = _F["cf303_conf"]
cf303_corr = _F["cf303_corr"]
cf303_limite = _F["cf303_limite"]
cf303_parse_book = _F["cf303_parse_book"]
cf303_norm_cdf = _F["cf303_norm_cdf"]
cf303_norm_ppf = _F["cf303_norm_ppf"]
cf303_sigma2_book = _F["cf303_sigma2_book"]
cf303_var_book = _F["cf303_var_book"]
cf303_capacita = _F["cf303_capacita"]
cf303_curva = _F["cf303_curva"]
cf303_verdetto = _F["cf303_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"

BOOK_TXT = ("Cal-28 Baseload power;2500000;18,5\n"
            "Q3-28 Peak power;1200000;26,0\n"
            "TTF Gas Cal-28;1800000;22,0\n"
            "EUA Carbon Dec-28;700000;31,0")
BOOK = [("Cal-28 Baseload power", 2500000.0, 0.185),
        ("Q3-28 Peak power", 1200000.0, 0.26),
        ("TTF Gas Cal-28", 1800000.0, 0.22),
        ("EUA Carbon Dec-28", 700000.0, 0.31)]
RHO = 0.35
CONF = 95
LIMITE = 2200000.0
NOME_CAND = "Nuovo Cal-29 Baseload"
VNEW = 0.21
RHO_CB = 0.35
VAR_BOOK = 1651956.8868516753
UTIL = 75.08894940234889
HEADROOM = 548043.1131483247
CAP = 2487574.986307384
Z95 = 1.6448536269514715
SIGMA2B = 1008655600000.0
CAP_RHO0 = 4206312.354565912
NOZ_TOT = 6200000.0
VERDETTO = "capacita' ampia: puoi aggiungere fino a 2,487,575 euro di 'Nuovo Cal-29 Baseload' restando sotto il limite"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab303:
    def test_tab303_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 338
        assert TITLE303 in titoli
        assert "tab303" in dvars
        assert "tab303" in withs
        assert titoli[dvars.index("tab303")] == TITLE303
        assert titoli[-1] == TITLE338
        assert dvars[-1] == "tab338"
        keys = re.findall(r'key="(st303_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_301_302_303(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab301")] == TITLE301
        assert titoli[dvars.index("tab302")] == TITLE302
        assert titoli[dvars.index("tab303")] == TITLE303


class TestCf303Validatori:
    def test_num_ok(self):
        assert cf303_num(3, "x") == 3.0
        assert cf303_num(2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                cf303_num(bad, "x")

    def test_conf(self):
        assert cf303_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                cf303_conf(bad)

    def test_corr(self):
        assert cf303_corr(1.0) == 1.0
        assert cf303_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                cf303_corr(bad)

    def test_limite(self):
        assert cf303_limite(100.0) == 100.0
        for bad in (0.0, -5.0):
            with pytest.raises(ValueError):
                cf303_limite(bad)


class TestCf303Parse:
    def test_demo(self):
        book = cf303_parse_book(BOOK_TXT)
        assert book == BOOK

    def test_righe_vuote(self):
        book = cf303_parse_book("\n" + BOOK_TXT + "\n\n")
        assert len(book) == 4

    def test_formato_ko(self):
        for bad in ("", "   ", "solo;due", "a;b;c;d", ";100;10",
                    "x;-100;10", "x;100;-5", "x;abc;10", 123):
            with pytest.raises(ValueError):
                cf303_parse_book(bad)


class TestCf303Norm:
    def test_ppf95(self):
        assert cf303_norm_ppf(0.95) == pytest.approx(1.6448536, abs=1e-6)
        assert cf303_norm_ppf(0.95) == pytest.approx(Z95, abs=1e-9)

    def test_ppf_simmetria(self):
        assert cf303_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
        assert cf303_norm_ppf(0.05) == pytest.approx(-Z95, abs=1e-9)

    def test_cdf(self):
        assert cf303_norm_cdf(0.0) == 0.5
        assert cf303_norm_cdf(Z95) == pytest.approx(0.95, abs=1e-9)

    def test_ppf_ko(self):
        for bad in (0.0, 1.0, -0.1):
            with pytest.raises(ValueError):
                cf303_norm_ppf(bad)


class TestCf303Varianza:
    def test_singola(self):
        b = [("A", 1000.0, 0.2)]
        assert cf303_sigma2_book(b, 0.5) == pytest.approx(200.0 ** 2)

    def test_rho1(self):
        s1, s2 = 1000.0 * 0.2, 500.0 * 0.3
        assert cf303_sigma2_book(
            [("A", 1000.0, 0.2), ("B", 500.0, 0.3)], 1.0) == pytest.approx(
            (s1 + s2) ** 2)

    def test_rho0(self):
        s1, s2 = 1000.0 * 0.2, 500.0 * 0.3
        assert cf303_sigma2_book(
            [("A", 1000.0, 0.2), ("B", 500.0, 0.3)], 0.0) == pytest.approx(
            s1 ** 2 + s2 ** 2)

    def test_demo(self):
        assert cf303_sigma2_book(BOOK, RHO) == SIGMA2B

    def test_var_book(self):
        assert cf303_var_book(BOOK, RHO, CONF) == VAR_BOOK
        assert cf303_var_book(BOOK, RHO, CONF) == pytest.approx(
            Z95 * math.sqrt(SIGMA2B))


class TestCf303Capacita:
    def test_demo(self):
        c = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, RHO_CB)
        assert c["var_attuale"] == VAR_BOOK
        assert c["utilizzo_pct"] == UTIL
        assert c["headroom_eur"] == HEADROOM
        assert c["cap_noz_eur"] == CAP
        assert c["noz_tot_book"] == NOZ_TOT
        assert c["var_a_cap"] == LIMITE

    def test_analitica_rho_cb_zero(self):
        c = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, 0.0)
        atteso = math.sqrt((LIMITE / Z95) ** 2 - SIGMA2B) / VNEW
        assert c["cap_noz_eur"] == pytest.approx(atteso, rel=1e-9)
        assert c["cap_noz_eur"] == CAP_RHO0

    def test_correlazione_riduce_capacita(self):
        c_hi = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, 0.9)
        c_lo = cf303_capacita(BOOK, RHO, CONF, LIMITE, VNEW, -0.5)
        assert c_hi["cap_noz_eur"] < CAP < c_lo["cap_noz_eur"]

    def test_over_limite(self):
        c = cf303_capacita(BOOK, RHO, CONF, VAR_BOOK * 0.5, VNEW, RHO_CB)
        assert c["cap_noz_eur"] == 0.0
        assert c["var_a_cap"] == c["var_attuale"]
        assert c["headroom_eur"] < 0.0

    def test_vol_zero(self):
        c = cf303_capacita(BOOK, RHO, CONF, LIMITE, 0.0, RHO_CB)
        assert math.isinf(c["cap_noz_eur"])
        assert c["var_a_cap"] == c["var_attuale"]

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            cf303_capacita(BOOK, RHO, CONF, LIMITE, -0.1, RHO_CB)


class TestCf303Curva:
    def test_struttura(self):
        cur = cf303_curva(BOOK, RHO, CONF, LIMITE, VNEW, RHO_CB)
        assert len(cur) == 21
        assert cur[0]["x_noz_eur"] == 0.0
        assert cur[0]["var_eur"] == pytest.approx(VAR_BOOK)
        assert cur[-1]["x_noz_eur"] == pytest.approx(1.5 * CAP)

    def test_monotona_con_rho_positiva(self):
        cur = cf303_curva(BOOK, RHO, CONF, LIMITE, VNEW, RHO_CB)
        vals = [r["var_eur"] for r in cur]
        assert all(b >= a for a, b in zip(vals, vals[1:]))


class TestCf303Verdetto:
    def test_demo(self):
        assert cf303_verdetto(CAP, BOOK, VAR_BOOK, LIMITE, NOME_CAND) == VERDETTO
        assert VERDETTO.startswith("capacita' ampia")
        assert NOME_CAND in VERDETTO

    def test_nessuna(self):
        v = cf303_verdetto(0.0, BOOK, VAR_BOOK, VAR_BOOK * 0.5, NOME_CAND)
        assert v.startswith("nessuna capacita'")

    def test_ristretta(self):
        lim = VAR_BOOK * 1.0005
        c = cf303_capacita(BOOK, RHO, CONF, lim, VNEW, RHO_CB)
        v = cf303_verdetto(c["cap_noz_eur"], BOOK, VAR_BOOK, lim, NOME_CAND)
        assert v.startswith("capacita' ristretta")

    def test_illimitata(self):
        v = cf303_verdetto(float("inf"), BOOK, VAR_BOOK, LIMITE, NOME_CAND)
        assert v.startswith("capacita' illimitata")
