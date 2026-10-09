"""Test tab298 '🚦📏 Limite VaR: quanto margine resta?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab298. Monitor del limite di VaR: headroom,
utilizzo e size massima del trade candidato per bisezione (follow-up di
tab297 Marginal VaR).
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("rb298_num", "rb298_conf", "rb298_corr",
          "rb298_parse_posizioni", "rb298_norm_cdf", "rb298_norm_ppf",
          "rb298_var_book", "rb298_var_con_candidato", "rb298_headroom",
          "rb298_max_nozionale", "rb298_verdetto")
rb298_num = _F["rb298_num"]
rb298_conf = _F["rb298_conf"]
rb298_corr = _F["rb298_corr"]
rb298_parse_posizioni = _F["rb298_parse_posizioni"]
rb298_norm_cdf = _F["rb298_norm_cdf"]
rb298_norm_ppf = _F["rb298_norm_ppf"]
rb298_var_book = _F["rb298_var_book"]
rb298_var_con_candidato = _F["rb298_var_con_candidato"]
rb298_headroom = _F["rb298_headroom"]
rb298_max_nozionale = _F["rb298_max_nozionale"]
rb298_verdetto = _F["rb298_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"

# book sintetico 2 posizioni a valori noti
SYN_POS = [("A", 1_000_000.0, 0.02), ("B", 500_000.0, 0.03)]
SYN_LIM = 300_000.0
SYN_CAND_VOL = 0.04
SYN_CAND_CORR = 0.5
SYN_PROP = 200_000.0

DEMO_TXT = """# book demo: nome;nozionale eur;vol % giornaliera
Gas TTF;2500000;3,2
Power DE;1800000;2,6
CO2 EUA;900000;2,1
Spark spread;1200000;4,0"""
DEMO_LIM = 400_000.0
DEMO_CAND = ("Coal API2", 800000.0, 0.028, 0.45)


def _demo_pos():
    return rb298_parse_posizioni(DEMO_TXT)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab298:
    def test_tab298_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 336
        assert TITLE298 in titoli
        assert "tab298" in dvars
        assert "tab298" in withs
        assert titoli[dvars.index("tab298")] == TITLE298
        assert titoli[-1] == TITLE336
        keys = re.findall(r'key="(rb298_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_296_297_298(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab296")] == TITLE296
        assert titoli[dvars.index("tab297")] == TITLE297
        assert titoli[dvars.index("tab298")] == TITLE298


class TestRb298Validatori:
    def test_num_ok(self):
        assert rb298_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            rb298_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            rb298_num(float("nan"), "x")

    def test_conf_ok(self):
        assert rb298_conf(0.99) == 0.99

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            rb298_conf(1.0)

    def test_corr_ok(self):
        assert rb298_corr(-1.0, "r") == -1.0
        assert rb298_corr(0.5, "r") == 0.5

    def test_corr_fuori_ko(self):
        with pytest.raises(ValueError):
            rb298_corr(1.5, "r")


class TestRb298Parse:
    def test_ok(self):
        t = "# cmt\n\n" + "\n".join(["Gas;1000000;2,5"] * 2)
        p = rb298_parse_posizioni(t)
        assert len(p) == 2 and p[0][0] == "Gas"
        assert p[0][1] == pytest.approx(1_000_000.0)
        assert p[0][2] == pytest.approx(0.025)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;1000000;2,5")

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;1000000\nPower;2000000")

    def test_nozionale_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;-5;2,5\nPower;2000000;2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            rb298_parse_posizioni("Gas;xx;2,5\nPower;2000000;2")


class TestRb298Norm:
    def test_cdf_nota(self):
        assert rb298_norm_cdf(0.0) == pytest.approx(0.5)
        assert rb298_norm_cdf(1.959963984540054) == pytest.approx(0.975, abs=1e-6)

    def test_ppf_noti(self):
        assert rb298_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
        assert rb298_norm_ppf(0.975) == pytest.approx(1.959963984540054,
                                                     rel=1e-6)
        assert rb298_norm_ppf(0.99) == pytest.approx(2.3263478740408408,
                                                     rel=1e-6)

    def test_ppf_bordi_ko(self):
        with pytest.raises(ValueError):
            rb298_norm_ppf(0.0)
        with pytest.raises(ValueError):
            rb298_norm_ppf(1.0)


class TestRb298VarBook:
    def test_sintetico(self):
        assert rb298_var_book(SYN_POS, 0.5, 0.99) == pytest.approx(70753.1084032727)

    def test_rho_zero(self):
        assert rb298_var_book(SYN_POS, 0.0, 0.99) == pytest.approx(58158.69685102098)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            rb298_var_book([SYN_POS[0]], 0.5, 0.99)


class TestRb298VarConCandidato:
    def test_sintetico(self):
        v = rb298_var_con_candidato(SYN_POS, 0.5, 0.99,
                                    ("C", SYN_PROP, SYN_CAND_VOL,
                                     SYN_CAND_CORR))
        assert v == pytest.approx(82871.55140944295)
        assert v >= rb298_var_book(SYN_POS, 0.5, 0.99)

    def test_nozionale_c_ko(self):
        with pytest.raises(ValueError):
            rb298_var_con_candidato(SYN_POS, 0.5, 0.99, ("C", -1.0, 0.04, 0.5))


class TestRb298Headroom:
    def test_valori(self):
        h = rb298_headroom(70753.1084032727, SYN_LIM)
        assert h["headroom"] == pytest.approx(229246.8915967273)
        assert h["utilizzo"] == pytest.approx(23.584369467757565)
        assert h["headroom"] == pytest.approx(SYN_LIM - 70753.1084032727)

    def test_sforamento_negativo(self):
        h = rb298_headroom(SYN_LIM + 1.0, SYN_LIM)
        assert h["headroom"] == pytest.approx(-1.0)
        assert h["utilizzo"] == pytest.approx(100.0 * (SYN_LIM + 1.0) / SYN_LIM)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            rb298_headroom(100.0, 0.0)


class TestRb298MaxNozionale:
    def test_sintetico(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, SYN_LIM)
        assert m == pytest.approx(2725892.773663776, rel=1e-6)

    def test_al_limite(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, SYN_LIM)
        v = rb298_var_con_candidato(SYN_POS, 0.5, 0.99, ("C", m, SYN_CAND_VOL,
                                                        SYN_CAND_CORR))
        assert v == pytest.approx(SYN_LIM, rel=1e-4)

    def test_sopra_max_sfora(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, SYN_LIM)
        v = rb298_var_con_candidato(SYN_POS, 0.5, 0.99,
                                    ("C", m * 1.5, SYN_CAND_VOL, SYN_CAND_CORR))
        assert v > SYN_LIM

    def test_book_sforato_zero(self):
        assert rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                   SYN_CAND_CORR,
                                   rb298_var_book(SYN_POS, 0.5,
                                                  0.99)) == 0.0

    def test_vol_nulla_infinito(self):
        m = rb298_max_nozionale(SYN_POS, 0.5, 0.99, 0.0, SYN_CAND_CORR,
                                SYN_LIM)
        assert math.isinf(m)

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            rb298_max_nozionale(SYN_POS, 0.5, 0.99, SYN_CAND_VOL,
                                SYN_CAND_CORR, -10.0)


class TestRb298Verdetto:
    def test_ok(self):
        assert rb298_verdetto(40.0, 100000.0).startswith("ok")

    def test_attenzione(self):
        assert rb298_verdetto(75.0, 50000.0).startswith("attenzione")
        assert rb298_verdetto(70.0, 50000.0).startswith("attenzione")

    def test_zona_rossa(self):
        assert rb298_verdetto(96.0, 5000.0).startswith("zona rossa")
        assert rb298_verdetto(95.0, 5000.0).startswith("zona rossa")

    def test_sforamento(self):
        assert rb298_verdetto(110.0, -5000.0).startswith("sforamento")

    def test_soglie(self):
        assert rb298_verdetto(69.9, 1.0).startswith("ok")
        assert rb298_verdetto(94.9, 1.0).startswith("attenzione")


class TestRb298Integrazione:
    def test_catena_demo(self):
        pos = _demo_pos()
        assert len(pos) == 4
        varb = rb298_var_book(pos, 0.35, 0.99)
        assert varb == pytest.approx(332637.92510122136)
        h = rb298_headroom(varb, DEMO_LIM)
        assert h["headroom"] == pytest.approx(67362.07489877864)
        assert h["utilizzo"] == pytest.approx(83.15948127530534)
        m = rb298_max_nozionale(pos, 0.35, 0.99, 0.028, 0.45, DEMO_LIM)
        assert m == pytest.approx(1504603.4815953365, rel=1e-6)
        vprop = rb298_var_con_candidato(pos, 0.35, 0.99, DEMO_CAND)
        assert vprop == pytest.approx(366738.14339864254)
        assert rb298_verdetto(h["utilizzo"], h["headroom"]) == 'attenzione: limite in avvicinamento'
