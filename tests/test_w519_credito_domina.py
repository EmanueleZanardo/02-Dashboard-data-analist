"""Test tab519 '⚠️💳 Rischio di credito che domina (IFRS 9)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh519_num", "mh519_str", "mh519_strumento", "mh519_valutazione",
           "mh519_riepilogo")

TITLE519 = "⚠️💳 Rischio di credito che domina (IFRS 9)"
TITLE518 = "➡️ Forward element escluso (IFRS 9)"


def _s(rid="SWP-2026-001", fv=245000.0, dfv=18500.0, cva=-950.0, dva=-120.0):
    return {"id": rid, "fair_value": fv, "delta_fv": dfv, "cva": cva,
            "dva": dva}


class TestW519Validatori:
    def test_num_ok(self):
        assert _F["mh519_num"](2, "x") == 2.0
        assert _F["mh519_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh519_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh519_str"]("  SWP-1 ", "x") == "SWP-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh519_str"](bad, "x")


class TestW519Strumento:
    def test_ok(self):
        r = _F["mh519_strumento"](_s())
        assert r["id"] == "SWP-2026-001"
        assert r["impatto_credito"] == pytest.approx(1070.0)
        assert r["ratio"] == pytest.approx(1070.0 / 18500.0)
        assert r["verdetto"] == "RAPPORTO_OK"

    def test_soglia_10_ok(self):
        r = _F["mh519_strumento"](_s(dfv=10000.0, cva=-1000.0, dva=0.0))
        assert r["ratio"] == pytest.approx(0.10)
        assert r["verdetto"] == "RAPPORTO_OK"

    def test_soglia_10_avviso(self):
        r = _F["mh519_strumento"](_s(dfv=10000.0, cva=-1000.01, dva=0.0))
        assert r["ratio"] > 0.10
        assert r["verdetto"] == "AVVISO_CREDITO"

    def test_soglia_25_avviso(self):
        r = _F["mh519_strumento"](_s(dfv=10000.0, cva=-2500.0, dva=0.0))
        assert r["ratio"] == pytest.approx(0.25)
        assert r["verdetto"] == "AVVISO_CREDITO"

    def test_soglia_25_dominante(self):
        r = _F["mh519_strumento"](_s(dfv=10000.0, cva=-2500.01, dva=0.0))
        assert r["ratio"] > 0.25
        assert r["verdetto"] == "CREDITO_DOMINANTE"

    def test_delta_zero_impatto_zero(self):
        r = _F["mh519_strumento"](_s(dfv=0.0, cva=0.0, dva=0.0))
        assert r["ratio"] == 0.0
        assert r["verdetto"] == "RAPPORTO_OK"

    def test_delta_zero_impatto_positivo(self):
        r = _F["mh519_strumento"](_s(dfv=0.0, cva=-10.0, dva=0.0))
        assert math.isinf(r["ratio"])
        assert r["verdetto"] == "CREDITO_DOMINANTE"

    def test_valori_assoluti(self):
        r = _F["mh519_strumento"](_s(cva=950.0, dva=120.0))
        assert r["impatto_credito"] == pytest.approx(1070.0)
        r2 = _F["mh519_strumento"](_s(dfv=-18500.0))
        assert r2["ratio"] == pytest.approx(1070.0 / 18500.0)
        assert r2["verdetto"] == "RAPPORTO_OK"

    def test_chiavi_mancanti(self):
        d = _s()
        del d["dva"]
        with pytest.raises(ValueError):
            _F["mh519_strumento"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh519_strumento"](["id"])

    def test_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh519_strumento"](_s(rid="  "))

    def test_valori_ko(self):
        for bad in (True, float("nan"), float("inf"), "950"):
            with pytest.raises(ValueError):
                _F["mh519_strumento"](_s(cva=bad))


class TestW519Valutazione:
    def test_demo(self):
        a = _F["mh519_valutazione"](
            [_s(), _s(rid="SWP-2026-002", fv=96200.0, dfv=4100.0,
                      cva=-1450.0, dva=-80.0)])
        t = a["totali"]
        assert t["n_strumenti"] == 2
        assert t["cva_totale"] == pytest.approx(-2400.0)
        assert t["impatto_credito_totale"] == pytest.approx(2600.0)
        assert t["delta_fv_assoluto_totale"] == pytest.approx(22600.0)
        assert t["ratio_complessivo"] == pytest.approx(2600.0 / 22600.0)
        assert t["n_ok"] == 1
        assert t["n_avviso"] == 0
        assert t["n_dominanti"] == 1
        assert t["verdetto_complessivo"] == "CREDITO_DOMINANTE"
        assert a["righe"][0]["verdetto"] == "RAPPORTO_OK"
        assert a["righe"][1]["verdetto"] == "CREDITO_DOMINANTE"
        assert a["righe"][1]["ratio"] == pytest.approx(1530.0 / 4100.0)

    def test_tutti_ok(self):
        a = _F["mh519_valutazione"]([_s(), _s(rid="B", dfv=50000.0)])
        assert a["totali"]["verdetto_complessivo"] == "TUTTI_OK"
        assert a["totali"]["n_ok"] == 2

    def test_avvisi(self):
        a = _F["mh519_valutazione"](
            [_s(dfv=10000.0, cva=-1500.0, dva=0.0)])
        assert a["totali"]["verdetto_complessivo"] == "AVVISI"
        assert a["totali"]["n_avviso"] == 1

    def test_ratio_complessivo_zero(self):
        a = _F["mh519_valutazione"](
            [_s(dfv=0.0, cva=0.0, dva=0.0)])
        assert a["totali"]["ratio_complessivo"] == 0.0
        assert a["totali"]["verdetto_complessivo"] == "TUTTI_OK"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh519_valutazione"]([])
        with pytest.raises(ValueError):
            _F["mh519_valutazione"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh519_valutazione"]([_s(rid="A"), _s(rid="A")])

    def test_riepilogo_wrapper(self):
        a = _F["mh519_riepilogo"]([_s()])
        assert a["totali"]["n_strumenti"] == 1
        assert a["righe"][0]["verdetto"] == "RAPPORTO_OK"


def test_registry_tab519():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 531
    assert TITLE519 in titoli
    assert src.count(TITLE519) == 3
    assert ", tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531 = st.tabs([" in src
    assert "    with tab519:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab519" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab519" in withs
    assert len(withs) == len(dvars) == 531
    # ordine: tab519 dopo tab518
    _decl519 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl519.index(f'"{TITLE518}"') < _decl519.index(f'"{TITLE519}"')
    assert titoli[dvars.index("tab519")] == TITLE519


def test_chiavi_st519_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    keys = re.findall(r'key="(st519_[^"]+)"', src) + re.findall(
        r'key=f"(st519_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
