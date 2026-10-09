"""Test tab310 '💧📉 LVaR: il VaR corretto per il costo di liquidazione': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab di rischio precedenti, piu' la matematica del LVaR: costo di
liquidazione in forma chiusa, scaling radice-quadrata, quota, verdetto a 5
livelli.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("la310_num", "la310_conf", "la310_corr", "la310_giorni",
           "la310_parse_book", "la310_norm_ppf", "la310_sigmas",
           "la310_var_book", "la310_liq_pos", "la310_liq_cost",
           "la310_lvar", "la310_verdetto")

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
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
BOOK_DEMO = ("Cal-28 Baseload power;2500000;18,5;0,4;power\n"
             "Q3-28 Peak power;1200000;26,0;0,8;power\n"
             "TTF Gas Cal-28;1800000;22,0;0,6;gas\n"
             "EUA Carbon Dec-28;700000;31,0;1,2;carbon")
RHO_DEMO = 0.35
CONF_DEMO = 95
GIORNI_DEMO = 5
SOGLIA_DEMO = 0.25
LIMITE_DEMO = 1673646.7462334232

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
VAR = 1651956.8868516753
LIQ = 43379.71876349592
LVAR = 1695336.6056151714
QUOTA = 0.025587673043699258
STATO = "limite nominale illusorio"
VERDETTO = 'limite nominale illusorio: il VaR puro (1,651,957 euro) sta sotto il limite ma con il costo di liquidazione (43,380 euro) lo supera: allargare il limite o ridurre le posizioni illiquide'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry310:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 328
        assert TITLE310 in titoli
        assert "tab310" in dvars
        assert "    with tab310:" in src

    def test_titoli_allineati_308_309_310(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab308")] == TITLE308
        assert titoli[dvars.index("tab309")] == TITLE309
        assert titoli[dvars.index("tab310")] == TITLE310

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE328
        assert dvars[-1] == "tab328"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["la310_conf"](99) == 99

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["la310_conf"](97)

    def test_corr_fuori_range(self):
        with pytest.raises(ValueError):
            _F["la310_corr"](-1.5)

    def test_giorni_ok(self):
        assert _F["la310_giorni"](5) == 5.0

    def test_giorni_zero_ko(self):
        with pytest.raises(ValueError):
            _F["la310_giorni"](0)

    def test_giorni_31_ko(self):
        with pytest.raises(ValueError):
            _F["la310_giorni"](31)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["la310_num"](False, "x")

    def test_parse_book_ok(self):
        book = _F["la310_parse_book"](BOOK_DEMO)
        assert len(book) == 4
        assert book[0] == ("Cal-28 Baseload power", 2500000.0, 0.185,
                           0.004, "power")

    def test_parse_book_4campi_ko(self):
        with pytest.raises(ValueError):
            _F["la310_parse_book"]("nome;1000;20,0;0,5")

    def test_parse_book_spread_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["la310_parse_book"]("nome;1000;20,0;-0,5;power")

    def test_parse_book_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["la310_parse_book"]("   \n  ")


class TestMatematica:
    def test_ppf_95(self):
        assert abs(_F["la310_norm_ppf"](0.95) - 1.6448536269514722) < 1e-3

    def test_liq_pos_forma_chiusa(self):
        # noz=1e6, spread=2% -> 1e6 * 0.01 * sqrt(1) = 10000
        book = [("a", 1_000_000.0, 0.2, 0.02, "x")]
        pos = _F["la310_liq_pos"](book, 1)
        assert pos == [("a", 10000.0, "x")]

    def test_liq_scaling_radice(self):
        book = [("a", 1_000_000.0, 0.2, 0.02, "x")]
        c1 = _F["la310_liq_cost"](book, 1)
        c4 = _F["la310_liq_cost"](book, 4)
        assert c4 == pytest.approx(2.0 * c1)

    def test_liq_spread_zero(self):
        book = [("a", 1_000_000.0, 0.2, 0.0, "x")]
        assert _F["la310_liq_cost"](book, 5) == 0.0

    def test_liq_cost_somma(self):
        book = _F["la310_parse_book"](BOOK_DEMO)
        dett = _F["la310_liq_pos"](book, GIORNI_DEMO)
        assert _F["la310_liq_cost"](book, GIORNI_DEMO) == pytest.approx(
            sum(c for _, c, _ in dett))

    def test_lvar_somma(self):
        book = _F["la310_parse_book"](BOOK_DEMO)
        ris = _F["la310_lvar"](book, RHO_DEMO, CONF_DEMO, GIORNI_DEMO)
        assert ris["lvar"] == pytest.approx(ris["var"] + ris["liq"])
        assert ris["quota"] == pytest.approx(ris["liq"] / ris["lvar"])
        assert len(ris["dettaglio"]) == 4
        assert [n for n, _, _ in ris["dettaglio"]] == [
            n for n, _, _, _, _ in book]

    def test_demo(self):
        book = _F["la310_parse_book"](BOOK_DEMO)
        ris = _F["la310_lvar"](book, RHO_DEMO, CONF_DEMO, GIORNI_DEMO)
        assert ris["var"] == pytest.approx(VAR, rel=1e-9)
        assert ris["liq"] == pytest.approx(LIQ, rel=1e-9)
        assert ris["lvar"] == pytest.approx(LVAR, rel=1e-9)
        assert ris["quota"] == pytest.approx(QUOTA, rel=1e-9)
        assert 0.0 < ris["quota"] < 1.0
        assert ris["var"] < LIMITE_DEMO < ris["lvar"]


class TestVerdetto:
    def test_supera_puro(self):
        ris = {"var": 2_000_000.0, "liq": 100_000.0, "lvar": 2_100_000.0,
               "quota": 0.048, "dettaglio": []}
        assert _F["la310_verdetto"](ris, 1_800_000.0, SOGLIA_DEMO).startswith(
            "limite gia' superato")

    def test_illusorio(self):
        ris = {"var": 1_700_000.0, "liq": 200_000.0, "lvar": 1_900_000.0,
               "quota": 0.105, "dettaglio": []}
        assert _F["la310_verdetto"](ris, 1_800_000.0, SOGLIA_DEMO).startswith(
            "limite nominale illusorio")

    def test_dominante(self):
        ris = {"var": 1_000_000.0, "liq": 400_000.0, "lvar": 1_400_000.0,
               "quota": 0.286, "dettaglio": []}
        assert _F["la310_verdetto"](ris, 1_800_000.0, SOGLIA_DEMO).startswith(
            "costo di liquidazione dominante")

    def test_materiale(self):
        ris = {"var": 1_000_000.0, "liq": 150_000.0, "lvar": 1_150_000.0,
               "quota": 0.130, "dettaglio": []}
        assert _F["la310_verdetto"](ris, 1_800_000.0, SOGLIA_DEMO).startswith(
            "costo di liquidazione materiale")

    def test_trascurabile(self):
        ris = {"var": 1_000_000.0, "liq": 20_000.0, "lvar": 1_020_000.0,
               "quota": 0.020, "dettaglio": []}
        assert _F["la310_verdetto"](ris, 1_800_000.0, SOGLIA_DEMO).startswith(
            "costo di liquidazione trascurabile")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith(STATO)

    def test_limite_zero_ko(self):
        ris = {"var": 1.0, "liq": 0.0, "lvar": 1.0, "quota": 0.0,
               "dettaglio": []}
        with pytest.raises(ValueError):
            _F["la310_verdetto"](ris, 0.0, SOGLIA_DEMO)

    def test_soglia_ko(self):
        ris = {"var": 1.0, "liq": 0.0, "lvar": 1.0, "quota": 0.0,
               "dettaglio": []}
        with pytest.raises(ValueError):
            _F["la310_verdetto"](ris, 100.0, 0.0)
        with pytest.raises(ValueError):
            _F["la310_verdetto"](ris, 100.0, 1.0)
