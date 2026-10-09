"""Test tab302 '✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab302. Incremental VaR: il risparmio ESATTO di
VaR chiudendo davvero una posizione (VaR(book) - VaR(book senza i)), contro
l'approssimazione lineare marginal*nozionale (tab297). Teorema: il VaR
parametrico e' convesso nel nozionale, quindi incremental <= marginal*nozionale
(follow-up del filone rischio tab292/294/295/296/297/298/299/300/301).
"""

import random
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("iv302_num", "iv302_conf", "iv302_corr", "iv302_parse_book",
          "iv302_sigma2", "iv302_norm_cdf", "iv302_norm_ppf",
          "iv302_var_book", "iv302_var_senza", "iv302_incremental",
          "iv302_marginale", "iv302_tabella", "iv302_verdetto")
iv302_num = _F["iv302_num"]
iv302_conf = _F["iv302_conf"]
iv302_corr = _F["iv302_corr"]
iv302_parse_book = _F["iv302_parse_book"]
iv302_sigma2 = _F["iv302_sigma2"]
iv302_norm_cdf = _F["iv302_norm_cdf"]
iv302_norm_ppf = _F["iv302_norm_ppf"]
iv302_var_book = _F["iv302_var_book"]
iv302_var_senza = _F["iv302_var_senza"]
iv302_incremental = _F["iv302_incremental"]
iv302_marginale = _F["iv302_marginale"]
iv302_tabella = _F["iv302_tabella"]
iv302_verdetto = _F["iv302_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"

BOOK = [("Cal-28 Baseload power", 2500000.0, 0.185),
        ("Q3-28 Peak power", 1200000.0, 0.26),
        ("TTF Gas Cal-28", 1800000.0, 0.22),
        ("EUA Carbon Dec-28", 700000.0, 0.31)]
RHO = 0.35
CONF = 95
NOME_TOP = 'Cal-28 Baseload power'


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab302:
    def test_tab302_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 329
        assert TITLE302 in titoli
        assert "tab302" in dvars
        assert "tab302" in withs
        assert titoli[dvars.index("tab302")] == TITLE302
        assert titoli[-1] == TITLE329
        keys = re.findall(r'key="(st302_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_300_301_302(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab300")] == TITLE300
        assert titoli[dvars.index("tab301")] == TITLE301
        assert titoli[dvars.index("tab302")] == TITLE302


class TestIv302Validatori:
    def test_num_ok(self):
        assert iv302_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            iv302_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            iv302_num(float("nan"), "x")

    def test_conf_ok(self):
        assert iv302_conf(95) == 95

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            iv302_conf(97)

    def test_corr_ok(self):
        assert iv302_corr(0.35) == 0.35

    def test_corr_ko(self):
        with pytest.raises(ValueError):
            iv302_corr(1.5)


class TestIv302ParseBook:
    def test_ok(self):
        b = iv302_parse_book("A;1000000;10,5\nB;2000000;20.0\n# cmt\n")
        assert b == [("A", 1000000.0, 0.105), ("B", 2000000.0, 0.20)]

    def test_poche_posizioni_ko(self):
        with pytest.raises(ValueError):
            iv302_parse_book("A;1000000;10")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            iv302_parse_book("A;xx;10\nB;1000000;10")

    def test_nozionale_zero_ko(self):
        with pytest.raises(ValueError):
            iv302_parse_book("A;0;10\nB;1000000;10")

    def test_tre_colonne_ko(self):
        with pytest.raises(ValueError):
            iv302_parse_book("A;1000000\nB;1000000;10")


class TestIv302Sigma2:
    def test_rho_zero_nota(self):
        s2 = iv302_sigma2([("a", 1000.0, 0.10), ("b", 2000.0, 0.20)], 0.0)
        assert s2 == pytest.approx(100.0 ** 2 + 400.0 ** 2)

    def test_rho_uno(self):
        s2 = iv302_sigma2([("a", 1000.0, 0.10), ("b", 2000.0, 0.20)], 1.0)
        assert s2 == pytest.approx((100.0 + 400.0) ** 2)

    def test_demo(self):
        assert iv302_sigma2(BOOK, RHO) == pytest.approx(1008655600000.0)


class TestIv302NormPpf:
    def test_mediana_zero(self):
        assert iv302_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)

    def test_095(self):
        assert iv302_norm_ppf(0.95) == pytest.approx(1.6448536269514715)

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            iv302_norm_ppf(0.0)


class TestIv302Var:
    def test_book_demo(self):
        assert iv302_var_book(BOOK, RHO, CONF) == pytest.approx(1651956.8868516753)

    def test_senza_top(self):
        assert iv302_var_senza(BOOK, RHO, CONF, 0) == pytest.approx(1157585.0661054882)

    def test_una_posizione_residua(self):
        v = iv302_var_senza([("a", 1000.0, 0.10), ("b", 2000.0, 0.20)],
                            0.0, 95, 0)
        assert v == pytest.approx(iv302_norm_ppf(0.95) * 400.0)

    def test_meno_di_due_ko(self):
        with pytest.raises(ValueError):
            iv302_var_book([("a", 1000.0, 0.10)], 0.0, 95)


class TestIv302Incremental:
    def test_top_demo(self):
        assert iv302_incremental(BOOK, RHO, CONF, 0) == pytest.approx(494371.8207461871)

    def test_definizione(self):
        for i in range(len(BOOK)):
            assert iv302_incremental(BOOK, RHO, CONF, i) == pytest.approx(
                iv302_var_book(BOOK, RHO, CONF)
                - iv302_var_senza(BOOK, RHO, CONF, i))

    def test_non_negativo(self):
        for i in range(len(BOOK)):
            assert iv302_incremental(BOOK, RHO, CONF, i) >= 0.0

    def test_teorema_convessita_demo(self):
        for i, (nome, w, s) in enumerate(BOOK):
            inc = iv302_incremental(BOOK, RHO, CONF, i)
            mrg = iv302_marginale(BOOK, RHO, CONF, i) * w
            assert inc <= mrg + 1e-6, nome

    def test_teorema_convessita_random(self):
        rng = random.Random(3)
        book = [(f"p{i}", rng.uniform(1e5, 3e6), rng.uniform(0.05, 0.35))
                for i in range(5)]
        for i, (nome, w, s) in enumerate(book):
            inc = iv302_incremental(book, 0.4, 95, i)
            mrg = iv302_marginale(book, 0.4, 95, i) * w
            assert inc <= mrg + 1e-6, nome


class TestIv302Marginale:
    def test_top_demo(self):
        assert iv302_marginale(BOOK, RHO, CONF, 0) * BOOK[0][1] == pytest.approx(595563.673872229)

    def test_eulero_somma_marginali(self):
        somma = sum(iv302_marginale(BOOK, RHO, CONF, i) * w
                    for i, (_, w, _) in enumerate(BOOK))
        assert somma == pytest.approx(1651956.8868516753)

    def test_rho_zero_formula(self):
        book = [("a", 1000.0, 0.10), ("b", 2000.0, 0.20)]
        import math
        sig = math.sqrt(100.0 ** 2 + 400.0 ** 2)
        m = iv302_marginale(book, 0.0, 95, 1)
        assert m == pytest.approx(iv302_norm_ppf(0.95) * 0.20 * 400.0 / sig)


class TestIv302Tabella:
    def test_quattro_righe(self):
        rows = iv302_tabella(BOOK, RHO, CONF)
        assert len(rows) == 4
        assert {r["posizione"] for r in rows} == {b[0] for b in BOOK}

    def test_chiavi(self):
        rows = iv302_tabella(BOOK, RHO, CONF)
        attese = {"posizione", "nozionale_eur", "vol_pct", "incremental_eur",
                  "marginale_x_noz_eur", "gap_pct", "quota_pct"}
        assert all(set(r) == attese for r in rows)

    def test_top_gap(self):
        rows = iv302_tabella(BOOK, RHO, CONF)
        top = max(rows, key=lambda r: r["incremental_eur"])
        assert top["posizione"] == 'Cal-28 Baseload power'
        assert top["gap_pct"] == pytest.approx(16.990937756178752)
        assert top["incremental_eur"] == pytest.approx(494371.8207461871)

    def test_gap_non_negativo(self):
        rows = iv302_tabella(BOOK, RHO, CONF)
        assert all(r["gap_pct"] >= -1e-9 for r in rows)


class TestIv302Verdetto:
    def test_lineare(self):
        assert iv302_verdetto(5.0, "X").startswith("linearita' ok")
        assert iv302_verdetto(9.99, "X").startswith("linearita' ok")

    def test_moderata(self):
        assert iv302_verdetto(10.0, "X").startswith("sovrastima moderata")
        assert iv302_verdetto(29.99, "X").startswith("sovrastima moderata")

    def test_forte(self):
        assert iv302_verdetto(30.0, "X").startswith("sovrastima forte")
        assert iv302_verdetto(60.0, "X").startswith("sovrastima forte")

    def test_nome_nel_testo(self):
        assert "Pippo" in iv302_verdetto(50.0, "Pippo")

    def test_demo(self):
        assert iv302_verdetto(16.990937756178752, 'Cal-28 Baseload power') == "sovrastima moderata: chiudere 'Cal-28 Baseload power' toglie meno VaR di quanto dica la derivata (perdi diversificazione)"


class TestIv302Integrazione:
    def test_catena_demo(self):
        rows = iv302_tabella(BOOK, RHO, CONF)
        top = max(rows, key=lambda r: r["incremental_eur"])
        vb = iv302_var_book(BOOK, RHO, CONF)
        assert top["incremental_eur"] + iv302_var_senza(
            BOOK, RHO, CONF, BOOK.index(
                next(b for b in BOOK if b[0] == top["posizione"]))) == pytest.approx(vb)
        assert iv302_verdetto(top["gap_pct"], top["posizione"]) == "sovrastima moderata: chiudere 'Cal-28 Baseload power' toglie meno VaR di quanto dica la derivata (perdi diversificazione)"
        assert 0.0 <= top["quota_pct"] <= 100.0
