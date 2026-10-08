"""Test tab309 '🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab di rischio precedenti, piu' la matematica della rho critica:
bisezione contro forma chiusa, casi limite oltre/mai, verdetto a 5 livelli.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("sv309_num", "sv309_conf", "sv309_corr", "sv309_limite",
           "sv309_parse_book", "sv309_norm_ppf", "sv309_sigmas",
           "sv309_var_book", "sv309_var_curva", "sv309_rho_critica",
           "sv309_verdetto")

TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
BOOK_DEMO = ("Cal-28 Baseload power;2500000;18,5;power\n"
             "Q3-28 Peak power;1200000;26,0;power\n"
             "TTF Gas Cal-28;1800000;22,0;gas\n"
             "EUA Carbon Dec-28;700000;31,0;carbon")
RHO_DEMO = 0.35
CONF_DEMO = 95
LIMITE_DEMO = 1900000.0
SOGLIA_DEMO = 0.30

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
Z95 = 1.6448536269514715
VAR_CORR = 1651956.8868516753
VAR_TETTO = 2282234.407395167
RHO_STAR = 0.5809515732117818
CUSCINETTO = 0.23095157321178184
HEADROOM = 248043.11314832466
STATO = "ok"
VERDETTO = 'cuscinetto moderato: il VaR tocca il limite a rho 0.58: monitorare la rho realizzata'
# book sintetico 2 posizioni: sig=[200,50], sq=42500, cp=10000
L_RHO_MEZZO = 376.88331263138866


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry309:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 317
        assert TITLE309 in titoli
        assert "tab309" in dvars
        assert "    with tab309:" in src

    def test_titoli_allineati_307_308_309(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab307")] == TITLE307
        assert titoli[dvars.index("tab308")] == TITLE308
        assert titoli[dvars.index("tab309")] == TITLE309

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE317
        assert dvars[-1] == "tab317"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["sv309_conf"](95) == 95

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["sv309_conf"](97)

    def test_corr_fuori_range(self):
        with pytest.raises(ValueError):
            _F["sv309_corr"](1.5)

    def test_limite_zero_ko(self):
        with pytest.raises(ValueError):
            _F["sv309_limite"](0.0)

    def test_limite_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["sv309_limite"](-100.0)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["sv309_num"](True, "x")

    def test_parse_book_ok(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        assert len(book) == 4
        assert book[0] == ("Cal-28 Baseload power", 2500000.0, 0.185, "power")

    def test_parse_book_3campi_ko(self):
        with pytest.raises(ValueError):
            _F["sv309_parse_book"]("nome;1000;20,0")

    def test_parse_book_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["sv309_parse_book"]("   \n  ")


class TestMatematica:
    def test_ppf_95(self):
        assert abs(_F["sv309_norm_ppf"](0.95) - 1.6448536269514722) < 1e-3

    def test_sigmas_due_posizioni(self):
        # sig1=200, sig2=50, rho=0.5 -> s2 = 40000+2500+2*0.5*200*50 = 52500
        sig, s2 = _F["sv309_sigmas"](
            [("a", 1000.0, 0.2, "x"), ("b", 500.0, 0.1, "y")], 0.5)
        assert sig == [200.0, 50.0]
        assert s2 == pytest.approx(52500.0)

    def test_rho_critica_forma_chiusa(self):
        # sq=42500, cp=10000: L_RHO_MEZZO = z*sqrt(52500) -> rho* = 0.5 esatto
        book = [("a", 1000.0, 0.2, "x"), ("b", 500.0, 0.1, "y")]
        ris = _F["sv309_rho_critica"](book, 0.0, 95, L_RHO_MEZZO)
        assert ris["stato"] == "ok"
        assert ris["rho_star"] == pytest.approx(0.5, abs=1e-9)
        assert ris["cuscinetto"] == pytest.approx(0.5, abs=1e-9)

    def test_rho_critica_inverte_var(self):
        # a rho* il VaR deve eguagliare il limite
        book = _F["sv309_parse_book"](BOOK_DEMO)
        ris = _F["sv309_rho_critica"](book, RHO_DEMO, CONF_DEMO, LIMITE_DEMO)
        assert ris["stato"] == "ok"
        assert _F["sv309_var_book"](book, ris["rho_star"], CONF_DEMO) == \
            pytest.approx(LIMITE_DEMO, rel=1e-9)

    def test_oltre(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        v0 = _F["sv309_var_book"](book, RHO_DEMO, CONF_DEMO)
        ris = _F["sv309_rho_critica"](book, RHO_DEMO, CONF_DEMO, v0 * 0.5)
        assert ris["stato"] == "oltre"
        assert ris["rho_star"] is None
        assert ris["cuscinetto"] is None
        assert ris["headroom"] < 0.0

    def test_oltre_al_limite_esatto(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        v0 = _F["sv309_var_book"](book, RHO_DEMO, CONF_DEMO)
        ris = _F["sv309_rho_critica"](book, RHO_DEMO, CONF_DEMO, v0)
        assert ris["stato"] == "oltre"

    def test_mai(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        v1 = _F["sv309_var_book"](book, 1.0, CONF_DEMO)
        ris = _F["sv309_rho_critica"](book, RHO_DEMO, CONF_DEMO, v1 * 2.0)
        assert ris["stato"] == "mai"
        assert ris["rho_star"] is None
        assert ris["headroom"] > 0.0

    def test_demo(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        ris = _F["sv309_rho_critica"](book, RHO_DEMO, CONF_DEMO, LIMITE_DEMO)
        assert ris["stato"] == STATO == "ok"
        assert ris["var_corr"] == pytest.approx(VAR_CORR, rel=1e-9)
        assert ris["var_tetto"] == pytest.approx(VAR_TETTO, rel=1e-9)
        assert ris["rho_star"] == pytest.approx(RHO_STAR, rel=1e-9)
        assert ris["cuscinetto"] == pytest.approx(CUSCINETTO, rel=1e-9)
        assert ris["headroom"] == pytest.approx(HEADROOM, rel=1e-9)
        assert 0.0 < ris["cuscinetto"] < 1.0

    def test_curva_monotona(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        curva = _F["sv309_var_curva"](book, CONF_DEMO)
        assert len(curva) == 41
        vals = [v for _, v in curva]
        assert all(b >= a for a, b in zip(vals, vals[1:]))
        assert curva[-1][1] == pytest.approx(VAR_TETTO, rel=1e-9)

    def test_curva_n_ko(self):
        book = _F["sv309_parse_book"](BOOK_DEMO)
        with pytest.raises(ValueError):
            _F["sv309_var_curva"](book, CONF_DEMO, n=2)

    def test_posizione_singola_mai(self):
        # cp=0 -> VaR costante: limite sopra -> mai
        book = [("a", 1000.0, 0.2, "x")]
        v = _F["sv309_var_book"](book, 0.3, 95)
        ris = _F["sv309_rho_critica"](book, 0.3, 95, v * 1.5)
        assert ris["stato"] == "mai"


class TestVerdetto:
    def test_oltre(self):
        ris = {"stato": "oltre", "rho_star": None, "cuscinetto": None}
        assert _F["sv309_verdetto"](ris, SOGLIA_DEMO).startswith(
            "limite gia' superato")

    def test_mai(self):
        ris = {"stato": "mai", "rho_star": None, "cuscinetto": None}
        assert _F["sv309_verdetto"](ris, SOGLIA_DEMO).startswith(
            "limite intoccabile")

    def test_ampio(self):
        ris = {"stato": "ok", "rho_star": 0.8, "cuscinetto": 0.45}
        assert _F["sv309_verdetto"](ris, SOGLIA_DEMO).startswith(
            "cuscinetto ampio")

    def test_moderato(self):
        ris = {"stato": "ok", "rho_star": 0.6, "cuscinetto": 0.20}
        assert _F["sv309_verdetto"](ris, SOGLIA_DEMO).startswith(
            "cuscinetto moderato")

    def test_sottile(self):
        ris = {"stato": "ok", "rho_star": 0.4, "cuscinetto": 0.05}
        assert _F["sv309_verdetto"](ris, SOGLIA_DEMO).startswith(
            "cuscinetto sottile")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith("cuscinetto moderato")

    def test_soglia_ko(self):
        ris = {"stato": "ok", "rho_star": 0.6, "cuscinetto": 0.25}
        with pytest.raises(ValueError):
            _F["sv309_verdetto"](ris, 0.0)
        with pytest.raises(ValueError):
            _F["sv309_verdetto"](ris, 1.0)
