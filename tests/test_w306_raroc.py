"""Test tab306 '💎📊 RAROC: il rendimento ripaga il rischio?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab306. RAROC: il P&L atteso per segmento viene
diviso per il VaR del segmento (componenti di Eulero sul modello parametrico
equi-correlato, tab304/305) e confrontato con l'hurdle rate del desk:
crea valore / sotto soglia / distrugge valore / non valutabile.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("rc306_num", "rc306_conf", "rc306_corr", "rc306_parse_book",
          "rc306_parse_pnl", "rc306_norm_cdf", "rc306_norm_ppf",
          "rc306_sigmas", "rc306_var_book", "rc306_componenti",
          "rc306_var_seg", "rc306_raroc", "rc306_verdetto")
rc306_num = _F["rc306_num"]
rc306_conf = _F["rc306_conf"]
rc306_corr = _F["rc306_corr"]
rc306_parse_book = _F["rc306_parse_book"]
rc306_parse_pnl = _F["rc306_parse_pnl"]
rc306_norm_cdf = _F["rc306_norm_cdf"]
rc306_norm_ppf = _F["rc306_norm_ppf"]
rc306_sigmas = _F["rc306_sigmas"]
rc306_var_book = _F["rc306_var_book"]
rc306_componenti = _F["rc306_componenti"]
rc306_var_seg = _F["rc306_var_seg"]
rc306_raroc = _F["rc306_raroc"]
rc306_verdetto = _F["rc306_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"

BOOK_TXT = ("Cal-28 Baseload power;2500000;18,5;power\n"
            "Q3-28 Peak power;1200000;26,0;power\n"
            "TTF Gas Cal-28;1800000;22,0;gas\n"
            "EUA Carbon Dec-28;700000;31,0;carbon\n"
            "Batteria arbitrage;500000;28,0;flex")
BOOK = [("Cal-28 Baseload power", 2500000.0, 0.185, "power"),
        ("Q3-28 Peak power", 1200000.0, 0.26, "power"),
        ("TTF Gas Cal-28", 1800000.0, 0.22, "gas"),
        ("EUA Carbon Dec-28", 700000.0, 0.31, "carbon"),
        ("Batteria arbitrage", 500000.0, 0.28, "flex")]
PNL_TXT = "power;206700\ngas;47800\ncarbon;-15000\nflex;40000"
PNL = {'power': 206700.0, 'gas': 47800.0, 'carbon': -15000.0, 'flex': 40000.0}
RHO = 0.35
CONF = 95
HURDLE = 15.0
VAR_TOT = 1774789.1364575038
SEG_VAR = {'power': 939628.3175022749, 'gas': 478125.4133484301, 'carbon': 223514.3115130074, 'flex': 133521.09409379173}
RAROC_SEG = {'flex': 0.2995781323653778, 'power': 0.21998059887068014, 'gas': 0.09997376977986762, 'carbon': -0.06710979667683194}
RAROC_BOOK = 0.15748349719893187
VERDETTO = "crea valore: RAROC 15.7 % sopra l'hurdle del 15.0 %"
Z95 = 1.6448536269514715


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab306:
    def test_tab306_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 319
        assert TITLE306 in titoli
        assert "tab306" in dvars
        assert "tab306" in withs
        assert titoli[dvars.index("tab306")] == TITLE306
        assert titoli[-1] == TITLE319
        assert dvars[-1] == "tab319"
        keys = re.findall(r'key="(st306_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_304_305_306(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab304")] == TITLE304
        assert titoli[dvars.index("tab305")] == TITLE305
        assert titoli[dvars.index("tab306")] == TITLE306


class TestRc306Validatori:
    def test_num_ok(self):
        assert rc306_num(3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                rc306_num(bad, "x")

    def test_conf(self):
        assert rc306_conf(95) == 95
        for bad in (97, "95"):
            with pytest.raises(ValueError):
                rc306_conf(bad)

    def test_corr(self):
        assert rc306_corr(1.0) == 1.0
        assert rc306_corr(-1.0) == -1.0
        for bad in (1.5, -1.01):
            with pytest.raises(ValueError):
                rc306_corr(bad)


class TestRc306Parse:
    def test_demo_book(self):
        assert rc306_parse_book(BOOK_TXT) == BOOK

    def test_book_ko(self):
        for bad in ("solo;tre", "x;abc;10;power", "x;10;-5;power",
                    "x;0;10;power", ""):
            with pytest.raises(ValueError):
                rc306_parse_book(bad)

    def test_demo_pnl(self):
        assert rc306_parse_pnl(PNL_TXT) == PNL

    def test_pnl_negativo_ok(self):
        assert rc306_parse_pnl("carbon;-15000") == {"carbon": -15000.0}

    def test_pnl_ko(self):
        for bad in ("power", "power;abc", "power;10;extra", "   \n"):
            with pytest.raises(ValueError):
                rc306_parse_pnl(bad)

    def test_pnl_duplicato_ko(self):
        with pytest.raises(ValueError):
            rc306_parse_pnl("power;10\npower;20")


class TestRc306Model:
    def test_ppf_95(self):
        assert rc306_norm_ppf(0.95) == pytest.approx(Z95)

    def test_var_totale(self):
        assert rc306_var_book(BOOK, RHO, CONF) == pytest.approx(VAR_TOT)

    def test_eulero_somma_var(self):
        comp = rc306_componenti(BOOK, RHO, CONF)
        assert sum(comp) == pytest.approx(rc306_var_book(BOOK, RHO, CONF))

    def test_var_seg_somma_var(self):
        seg = rc306_var_seg(BOOK, rc306_componenti(BOOK, RHO, CONF))
        assert sum(seg.values()) == pytest.approx(rc306_var_book(BOOK, RHO, CONF))

    def test_var_seg_valori(self):
        seg = rc306_var_seg(BOOK, rc306_componenti(BOOK, RHO, CONF))
        assert set(seg) == set(SEG_VAR)
        for s, v in SEG_VAR.items():
            assert seg[s] == pytest.approx(v)

    def test_componenti_degeneri(self):
        book0 = [("Zero", 1000000.0, 0.0, "zero")]
        assert rc306_componenti(book0, RHO, CONF) == [0.0]
        assert rc306_var_book(book0, RHO, CONF) == 0.0

    def test_var_seg_lunghezza_ko(self):
        with pytest.raises(ValueError):
            rc306_var_seg(BOOK, [1.0])


class TestRc306Raroc:
    def _rows(self):
        seg = rc306_var_seg(BOOK, rc306_componenti(BOOK, RHO, CONF))
        return rc306_raroc(seg, PNL)

    def test_raroc_valori(self):
        rows = self._rows()
        got = {r["segmento"]: r["raroc"] for r in rows}
        assert set(got) == set(RAROC_SEG)
        for s, r in RAROC_SEG.items():
            assert got[s] == pytest.approx(r)

    def test_raroc_coerente(self):
        for r in self._rows():
            assert r["raroc"] == pytest.approx(r["pnl_eur"] / r["var_eur"])

    def test_ordinato_decrescente(self):
        rows = self._rows()
        assert [r["segmento"] for r in rows] == ["flex", "power", "gas", "carbon"]

    def test_raroc_book(self):
        seg = rc306_var_seg(BOOK, rc306_componenti(BOOK, RHO, CONF))
        var = rc306_var_book(BOOK, RHO, CONF)
        assert sum(PNL.values()) / var == pytest.approx(RAROC_BOOK)

    def test_var_zero_none(self):
        rows = rc306_raroc({"zero": 0.0}, {"zero": 100.0})
        assert rows[0]["raroc"] is None

    def test_segmento_solo_pnl(self):
        seg = rc306_var_seg(BOOK, rc306_componenti(BOOK, RHO, CONF))
        rows = rc306_raroc(seg, {"power": 1.0, "nuke": 500.0})
        nuke = [r for r in rows if r["segmento"] == "nuke"][0]
        assert nuke["var_eur"] == 0.0
        assert nuke["raroc"] is None
        assert rows[-1]["segmento"] == "nuke"

    def test_var_negativo_ko(self):
        with pytest.raises(ValueError):
            rc306_raroc({"s": -1.0}, {"s": 10.0})


class TestRc306Verdetto:
    def test_crea_valore(self):
        assert rc306_verdetto(0.20, 15.0).startswith("crea valore")
        assert rc306_verdetto(0.15, 15.0).startswith("crea valore")

    def test_sotto_soglia(self):
        assert rc306_verdetto(0.10, 15.0).startswith("sotto soglia")
        assert rc306_verdetto(0.0, 15.0).startswith("sotto soglia")

    def test_distrugge_valore(self):
        assert rc306_verdetto(-0.05, 15.0).startswith("distrugge valore")

    def test_non_valutabile(self):
        assert rc306_verdetto(None, 15.0).startswith("non valutabile")

    def test_hurdle_negativo_ko(self):
        with pytest.raises(ValueError):
            rc306_verdetto(0.2, -1.0)

    def test_verdetto_demo(self):
        assert rc306_verdetto(RAROC_BOOK, HURDLE) == VERDETTO
