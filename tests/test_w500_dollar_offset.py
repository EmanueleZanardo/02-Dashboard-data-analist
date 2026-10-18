"""Test tab500 '📑 Efficacia contabile: dollar-offset delle coperture': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh500_num", "mh500_str", "mh500_tol", "mh500_banda",
           "mh500_relazione", "mh500_verdetto", "mh500_riepilogo")

TITLE500 = "📑 Efficacia contabile: dollar-offset delle coperture"
TITLE499 = "🎯 Regret della copertura: fissato vs spot"


def _rel(nome, s0, s1, c0, c1):
    return _F["mh500_relazione"](nome, s0, s1, c0, c1)


# Demo: efficace, marginale (inefficacia materiale), inefficace, non valutabile
REL_EFF = _rel("TTF Q1-27 future", -120000.0, -85000.0, 118000.0, 83500.0)
REL_MAR = _rel("Power Cal-27 DE", 240000.0, 190000.0, -238000.0, -195000.0)
REL_INE = _rel("CO2 Dec-26 EUA", 45000.0, 33000.0, -44000.0, -40000.0)
REL_NVV = _rel("PSV baseload IT", 90000.0, 90000.0, -88000.0, -88000.0)


class TestW500Validatori:
    def test_num_ok(self):
        assert _F["mh500_num"](3, "x") == 3.0
        assert _F["mh500_num"](-2.5, "x") == -2.5  # i fair value possono scendere

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh500_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh500_str"]("  TTF  ", "x") == "TTF"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh500_str"](bad, "x")

    def test_tol_ok(self):
        assert _F["mh500_tol"](0.0, "x") == 0.0

    def test_tol_ko(self):
        for bad in (-1.0, 2e9):
            with pytest.raises(ValueError):
                _F["mh500_tol"](bad, "x")

    def test_banda_ok(self):
        assert _F["mh500_banda"](0.80, 1.25) == (0.80, 1.25)

    def test_banda_ko(self):
        for inf, sup in ((1.25, 0.80), (0.80, 0.80), (0.0, 1.25),
                         (-0.5, 1.25), (0.80, 10.5)):
            with pytest.raises(ValueError):
                _F["mh500_banda"](inf, sup)


class TestW500Relazione:
    def test_delta_e_rapporto(self):
        assert REL_EFF["delta_strumento"] == pytest.approx(35000.0)
        assert REL_EFF["delta_coperto"] == pytest.approx(-34500.0)
        assert REL_EFF["segno_opposto"] is True
        assert REL_EFF["rapporto"] == pytest.approx(35000.0 / 34500.0)
        assert REL_EFF["inefficacia"] == pytest.approx(500.0)

    def test_segno_concorde(self):
        r = _rel("x", 100.0, 120.0, 50.0, 80.0)  # entrambi +
        assert r["segno_opposto"] is False
        assert _F["mh500_verdetto"](r, 0.80, 1.25, 5000.0) == "INEFFICACE"

    def test_coperto_fermo(self):
        assert REL_NVV["rapporto"] is None
        assert REL_NVV["segno_opposto"] is False
        assert _F["mh500_verdetto"](REL_NVV, 0.80, 1.25, 5000.0) == "NON_VALUTABILE"

    def test_verdetti_demo(self):
        assert _F["mh500_verdetto"](REL_EFF, 0.80, 1.25, 5000.0) == "EFFICACE"
        assert _F["mh500_verdetto"](REL_MAR, 0.80, 1.25, 5000.0) == "MARGINALE"
        assert _F["mh500_verdetto"](REL_INE, 0.80, 1.25, 5000.0) == "INEFFICACE"

    def test_banda_stretta(self):
        # con banda 1.02-1.05 la relazione efficace esce -> MARGINALE
        assert _F["mh500_verdetto"](REL_EFF, 1.02, 1.05, 5000.0) == "MARGINALE"

    def test_tol_piu_alta(self):
        # con soglia 10000 la relazione marginale rientra -> EFFICACE
        assert _F["mh500_verdetto"](REL_MAR, 0.80, 1.25, 10000.0) == "EFFICACE"

    def test_rapporto_esattamente_ai_limiti(self):
        r_inf = _rel("x", 0.0, 80.0, 0.0, -100.0)   # rapporto = 0.80
        r_sup = _rel("y", 0.0, 125.0, 0.0, -100.0)  # rapporto = 1.25
        assert _F["mh500_verdetto"](r_inf, 0.80, 1.25, 5000.0) == "EFFICACE"
        assert _F["mh500_verdetto"](r_sup, 0.80, 1.25, 5000.0) == "EFFICACE"

    def test_strumento_fermo_coperto_mosso(self):
        r = _rel("x", 100.0, 100.0, 50.0, 80.0)  # ds=0, dc=+30
        assert r["rapporto"] == pytest.approx(0.0)
        assert _F["mh500_verdetto"](r, 0.80, 1.25, 5000.0) == "INEFFICACE"


class TestW500Riepilogo:
    def test_totali_e_verdetto(self):
        rie = _F["mh500_riepilogo"]([REL_EFF, REL_MAR, REL_INE, REL_NVV],
                                    0.80, 1.25, 5000.0)
        assert rie["n_relazioni"] == 4
        assert rie["n_efficaci"] == 1
        assert rie["quota_efficaci"] == pytest.approx(0.25)
        assert rie["inefficacia_totale_eur"] == pytest.approx(
            500.0 - 7000.0 - 8000.0 + 0.0)
        assert rie["verdetto_complessivo"] == "INEFFICACE"
        assert [r["verdetto"] for r in rie["righe"]] == [
            "EFFICACE", "MARGINALE", "INEFFICACE", "NON_VALUTABILE"]

    def test_tutto_efficace(self):
        r1 = _rel("a", 0.0, 100.0, 0.0, -100.0)
        r2 = _rel("b", 50.0, 150.0, -40.0, -140.0)
        rie = _F["mh500_riepilogo"]([r1, r2], 0.80, 1.25, 5000.0)
        assert rie["verdetto_complessivo"] == "EFFICACE"
        assert rie["inefficacia_totale_eur"] == pytest.approx(0.0)

    def test_complessivo_marginale(self):
        rie = _F["mh500_riepilogo"]([REL_EFF, REL_MAR], 0.80, 1.25, 5000.0)
        assert rie["verdetto_complessivo"] == "MARGINALE"

    def test_complessivo_non_valutabile(self):
        rie = _F["mh500_riepilogo"]([REL_EFF, REL_NVV], 0.80, 1.25, 5000.0)
        assert rie["verdetto_complessivo"] == "NON_VALUTABILE"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh500_riepilogo"]([], 0.80, 1.25, 5000.0)
        with pytest.raises(ValueError):
            _F["mh500_riepilogo"]([REL_EFF], 1.25, 0.80, 5000.0)
        with pytest.raises(ValueError):
            _F["mh500_riepilogo"]([REL_EFF], 0.80, 1.25, -5.0)


def test_registry_tab500():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 543
    assert TITLE500 in titoli
    assert src.count(TITLE500) == 3
    assert "tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543 = st.tabs([" in src
    assert "    with tab500:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab500" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab500" in withs
    assert len(withs) == len(dvars) == 543
    # ordine: tab500 dopo tab499
    _decl500 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl500.index(f'"{TITLE499}"') < _decl500.index(f'"{TITLE500}"')
    assert titoli[dvars.index("tab500")] == TITLE500


def test_chiavi_st500_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st500_[^"]+)"', src) + re.findall(
        r'key=f"(st500_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10
