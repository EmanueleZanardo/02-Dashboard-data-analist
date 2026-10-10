"""Test tab348 'Kelly con costi di trading: sizing netto': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh348_num", "mh348_int", "mh348_b_netto", "mh348_f_star",
           "mh348_g", "mh348_verdetto", "mh348_misure")

TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
P = 0.55
WIN = 120.0
LOSS = 100.0
COSTO = 2.0
FMIN = 0.1
B_LORDO = 1.2
F_LORDO = 0.17500000000000007
G_LORDO = 0.018273846093402088
B_NETTO = 1.1568627450980393
F_NETTO = 0.16101694915254247
G_NETTO = 0.01494560432287488
EDGE_NETTO = 0.18627450980392168
EROSIONE = 0.0799031476997577
VERDETTO = 'COSTI SOSTENIBILI: f* netto 16.10% contro f* lordo 17.50% (erosione 8.0%).'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry348:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 351
        assert "tab348" in dvars
        assert "tab348" in withs

    def test_titoli_allineati_345_346_347_348(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab345")] == TITLE345
        assert titoli[dvars.index("tab346")] == TITLE346
        assert titoli[dvars.index("tab347")] == TITLE347
        assert titoli[dvars.index("tab348")] == TITLE348

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab351"
        assert titoli[-1] == TITLE351
        assert withs[-1] == "tab351"


class TestNum:
    def test_num_ok(self):
        assert _F["mh348_num"](1.5, "x") == 1.5
        assert _F["mh348_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh348_num"](bad, "x")


class TestInt:
    def test_int_ok(self):
        assert _F["mh348_int"](5, "x", 1, 10) == 5
        assert _F["mh348_int"](1, "x", 1, 10) == 1

    def test_int_ko(self):
        for bad in (True, 1.5, "5", None):
            with pytest.raises(ValueError):
                _F["mh348_int"](bad, "x", 1, 10)
        for bad in (0, 11):
            with pytest.raises(ValueError):
                _F["mh348_int"](bad, "x", 1, 10)


class TestBNetto:
    def test_demo(self):
        assert _F["mh348_b_netto"](WIN, LOSS, COSTO) == pytest.approx(
            B_NETTO, rel=1e-12)
        assert B_NETTO == pytest.approx((WIN - COSTO) / (LOSS + COSTO),
                                        rel=1e-12)

    def test_costo_zero(self):
        assert _F["mh348_b_netto"](WIN, LOSS, 0.0) == pytest.approx(
            WIN / LOSS, rel=1e-12)

    def test_ko(self):
        for bad in (WIN, WIN + 10.0):
            with pytest.raises(ValueError):
                _F["mh348_b_netto"](WIN, LOSS, bad)
        with pytest.raises(ValueError):
            _F["mh348_b_netto"](WIN, LOSS, -1.0)
        with pytest.raises(ValueError):
            _F["mh348_b_netto"](WIN, 0.0, COSTO)
        with pytest.raises(ValueError):
            _F["mh348_b_netto"](0.0, LOSS, COSTO)


class TestFStar:
    def test_demo_lordo_formula(self):
        att = (P * B_LORDO - (1.0 - P)) / B_LORDO
        assert _F["mh348_f_star"](P, B_LORDO) == pytest.approx(
            att, rel=1e-12)
        assert F_LORDO == pytest.approx(att, rel=1e-12)
        assert F_LORDO == pytest.approx(0.175, rel=1e-12)

    def test_demo_netto(self):
        assert _F["mh348_f_star"](P, B_NETTO) == pytest.approx(
            F_NETTO, rel=1e-12)
        assert 0.0 < F_NETTO < F_LORDO

    def test_costo_zero_coincide_lordo(self):
        b0 = _F["mh348_b_netto"](WIN, LOSS, 0.0)
        assert _F["mh348_f_star"](P, b0) == pytest.approx(
            F_LORDO, rel=1e-12)

    def test_monotono_nei_costi(self):
        fs = [_F["mh348_f_star"](
            P, _F["mh348_b_netto"](WIN, LOSS, c))
            for c in (0.0, 1.0, 2.0, 5.0, 10.0)]
        assert all(a > b for a, b in zip(fs, fs[1:]))

    def test_senza_edge(self):
        assert _F["mh348_f_star"](0.40, 1.2) == 0.0
        assert _F["mh348_f_star"](0.50, 1.0) == 0.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh348_f_star"](0.0, B_LORDO)
        with pytest.raises(ValueError):
            _F["mh348_f_star"](1.0, B_LORDO)
        with pytest.raises(ValueError):
            _F["mh348_f_star"](P, 0.0)


class TestG:
    def test_demo_formula(self):
        att = (P * math.log(1.0 + F_NETTO * B_NETTO)
               + (1.0 - P) * math.log(1.0 - F_NETTO))
        assert _F["mh348_g"](P, B_NETTO, F_NETTO) == pytest.approx(
            att, rel=1e-12)
        assert G_NETTO == pytest.approx(att, rel=1e-12)

    def test_ottimalita_kelly(self):
        g = _F["mh348_g"]
        assert g(P, B_NETTO, F_NETTO) >= g(P, B_NETTO, F_NETTO / 2.0)
        assert g(P, B_NETTO, F_NETTO) >= g(P, B_NETTO, 0.0)
        assert g(P, B_NETTO, F_NETTO) > 0.0

    def test_g_netto_minore_lordo(self):
        assert G_NETTO < G_LORDO

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh348_g"](P, B_NETTO, 1.0)
        with pytest.raises(ValueError):
            _F["mh348_g"](P, B_NETTO, -0.1)
        with pytest.raises(ValueError):
            _F["mh348_g"](0.0, B_NETTO, F_NETTO)


class TestVerdetto:
    def test_demo(self):
        assert VERDETTO == _F["mh348_verdetto"](EDGE_NETTO, F_NETTO,
                                                F_LORDO, FMIN)
        assert VERDETTO.startswith("COSTI SOSTENIBILI")

    def test_erosivi(self):
        v = _F["mh348_verdetto"](EDGE_NETTO, F_NETTO, F_LORDO, 0.50)
        assert v.startswith("COSTI EROSIVI")

    def test_edge_azzerato(self):
        v = _F["mh348_verdetto"](-0.01, 0.0, F_LORDO, FMIN)
        assert v.startswith("EDGE AZZERATO")

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh348_verdetto"](EDGE_NETTO, F_NETTO, F_LORDO, 0.0)
        with pytest.raises(ValueError):
            _F["mh348_verdetto"](EDGE_NETTO, F_NETTO, F_LORDO, 1.0)


class TestMisure:
    def test_demo(self):
        m = _F["mh348_misure"](P, WIN, LOSS, COSTO, FMIN)
        assert m["b_lordo"] == pytest.approx(B_LORDO, rel=1e-12)
        assert m["f_lordo"] == pytest.approx(F_LORDO, rel=1e-12)
        assert m["g_lordo"] == pytest.approx(G_LORDO, rel=1e-12)
        assert m["b_netto"] == pytest.approx(B_NETTO, rel=1e-12)
        assert m["f_netto"] == pytest.approx(F_NETTO, rel=1e-12)
        assert m["g_netto"] == pytest.approx(G_NETTO, rel=1e-12)
        assert m["edge_netto"] == pytest.approx(EDGE_NETTO, rel=1e-12)
        assert m["erosione"] == pytest.approx(EROSIONE, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_erosione_formula(self):
        m = _F["mh348_misure"](P, WIN, LOSS, COSTO, FMIN)
        assert m["erosione"] == pytest.approx(
            1.0 - F_NETTO / F_LORDO, rel=1e-9)

    def test_tabella_costi(self):
        m = _F["mh348_misure"](P, WIN, LOSS, COSTO, FMIN)
        tab = m["tabella"]
        assert [r["costo"] for r in tab] == [0.0, 1.0, 2.0, 5.0, 10.0]
        fs = [r["f_star"] for r in tab]
        assert all(a >= b for a, b in zip(fs, fs[1:]))
        assert tab[0]["f_star"] == pytest.approx(F_LORDO, rel=1e-12)
        assert tab[2]["f_star"] == pytest.approx(F_NETTO, rel=1e-12)
        assert all(r["stato"] == "ok" for r in tab)

    def test_costo_alto_edge_azzerato(self):
        m = _F["mh348_misure"](P, WIN, LOSS, 60.0, FMIN)
        assert m["f_netto"] == 0.0
        assert m["edge_netto"] < 0.0
        assert m["verdetto"].startswith("EDGE AZZERATO")

    def test_ko_costo_mangia_vincita(self):
        with pytest.raises(ValueError):
            _F["mh348_misure"](P, WIN, LOSS, WIN, FMIN)

