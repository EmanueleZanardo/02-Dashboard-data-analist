"""Test tab518 '➡️ Forward element escluso (IFRS 9)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh518_num", "mh518_str", "mh518_forward", "mh518_valutazione",
           "mh518_riepilogo")

TITLE518 = "➡️ Forward element escluso (IFRS 9)"
TITLE517 = "🧩 Componenti di rischio designati (IFRS 9)"


def _f(rid="FW-2026-001", fv=18400.0, spot=17800.0, fe=600.0,
       tipo="periodo", nper=4, real=False):
    return {"id": rid, "fair_value": fv, "spot_value": spot,
            "forward_element": fe, "tipo": tipo, "n_periodi": nper,
            "transazione_realizzata": real}


class TestW518Validatori:
    def test_num_ok(self):
        assert _F["mh518_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh518_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh518_str"]("  FW-1 ", "x") == "FW-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh518_str"](bad, "x")


class TestW518Forward:
    def test_ok(self):
        r = _F["mh518_forward"](_f())
        assert r["id"] == "FW-2026-001"
        assert r["forward_element"] == 600.0
        assert r["scostamento_ok"] is True
        assert r["scostamento"] == pytest.approx(0.0)

    def test_scostamento_flag(self):
        r = _F["mh518_forward"](_f(fe=610.0))
        assert r["scostamento_ok"] is False
        assert r["scostamento"] == pytest.approx(-10.0)

    def test_scostamento_tolleranza(self):
        r = _F["mh518_forward"](_f(fe=600.004))
        assert r["scostamento_ok"] is True
        r2 = _F["mh518_forward"](_f(fe=600.006))
        assert r2["scostamento_ok"] is False

    def test_tipo_ko(self):
        with pytest.raises(ValueError):
            _F["mh518_forward"](_f(tipo="futuro"))

    def test_nperiodi_ko(self):
        for bad in (0, -2, 1.5, True, "4", None):
            with pytest.raises(ValueError):
                _F["mh518_forward"](_f(nper=bad))

    def test_real_ko(self):
        for bad in (1, "no", None):
            with pytest.raises(ValueError):
                _F["mh518_forward"](_f(real=bad))

    def test_chiavi_mancanti(self):
        d = _f()
        del d["spot_value"]
        with pytest.raises(ValueError):
            _F["mh518_forward"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh518_forward"](["id"])


class TestW518Valutazione:
    def test_demo(self):
        a = _F["mh518_valutazione"](
            [_f(), _f(rid="FW-2026-002", fv=9150.0, spot=9000.0, fe=150.0,
                      tipo="transazione", nper=1)])
        t = a["totali"]
        assert t["costo_totale"] == pytest.approx(750.0)
        assert t["ammortizzato_totale"] == pytest.approx(600.0)
        assert t["differito_totale"] == pytest.approx(150.0)
        assert t["rilasciato_totale"] == pytest.approx(0.0)
        assert t["n_scostamenti"] == 0
        assert t["verdetto_complessivo"] == "MISTO"
        r1 = a["righe"][0]
        assert r1["verdetto"] == "AMMORTAMENTO_SISTEMATICO"
        assert r1["quota_periodo"] == pytest.approx(150.0)
        assert len(r1["piano"]) == 4
        assert r1["piano"][0]["quota"] == pytest.approx(150.0)
        assert r1["piano"][0]["residuo"] == pytest.approx(450.0)
        assert r1["piano"][-1]["residuo"] == pytest.approx(0.0)
        r2 = a["righe"][1]
        assert r2["verdetto"] == "DIFFERITO_OCI"
        assert r2["piano"] == []
        assert r2["quota_periodo"] is None

    def test_rilascio(self):
        a = _F["mh518_valutazione"](
            [_f(tipo="transazione", nper=1, real=True)])
        r = a["righe"][0]
        assert r["verdetto"] == "RILASCIO_A_PNL"
        assert r["rilasciato"] == pytest.approx(600.0)
        assert a["totali"]["verdetto_complessivo"] == "TUTTO_RILASCIATO"

    def test_tutto_differito(self):
        a = _F["mh518_valutazione"](
            [_f(tipo="transazione"), _f(rid="B", tipo="transazione")])
        assert a["totali"]["verdetto_complessivo"] == "TUTTO_DIFFERITO"

    def test_tutto_ammortamento(self):
        a = _F["mh518_valutazione"]([_f(), _f(rid="B")])
        assert a["totali"]["verdetto_complessivo"] == "AMMORTAMENTO_SISTEMATICO"

    def test_piano_periodo_1(self):
        a = _F["mh518_valutazione"]([_f(nper=1)])
        p = a["righe"][0]["piano"]
        assert len(p) == 1
        assert p[0]["quota"] == pytest.approx(600.0)
        assert p[0]["residuo"] == pytest.approx(0.0)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh518_valutazione"]([])
        with pytest.raises(ValueError):
            _F["mh518_valutazione"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh518_valutazione"]([_f(rid="A"), _f(rid="A")])

    def test_riepilogo_wrapper(self):
        a = _F["mh518_riepilogo"]([_f()])
        assert a["totali"]["n_forward"] == 1
        assert a["righe"][0]["verdetto"] == "AMMORTAMENTO_SISTEMATICO"


def test_registry_tab518():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 531
    assert TITLE518 in titoli
    assert src.count(TITLE518) == 3
    assert ", tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531 = st.tabs([" in src
    assert "    with tab518:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab518" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab518" in withs
    assert len(withs) == len(dvars) == 531
    # ordine: tab518 dopo tab517
    _decl518 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl518.index(f'"{TITLE517}"') < _decl518.index(f'"{TITLE518}"')
    assert titoli[dvars.index("tab518")] == TITLE518


def test_chiavi_st518_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    keys = re.findall(r'key="(st518_[^"]+)"', src) + re.findall(
        r'key=f"(st518_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
