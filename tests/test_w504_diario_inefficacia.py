"""Test tab504 '📊📓 Diario dell'inefficacia: OCI vs P&L per periodo': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh504_num", "mh504_str", "mh504_pct", "mh504_periodo",
           "mh504_lower_of", "mh504_inefficacia", "mh504_riepilogo")

TITLE504 = "📊📓 Diario dell'inefficacia: OCI vs P&L per periodo"
TITLE503 = "📦 Cost-of-carry: scomponi il premio del forward"

TOL = 5.0


def _demo():
    return [_F["mh504_periodo"](n, dh, di) for n, dh, di in
            [("Gennaio", 1000000.0, -1000000.0),
             ("Febbraio", 500000.0, -480000.0),
             ("Marzo", -200000.0, 260000.0),
             ("Aprile", -1000000.0, 1100000.0)]]


class TestW504Validatori:
    def test_num_ok(self):
        assert _F["mh504_num"](3, "x") == 3.0
        assert _F["mh504_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh504_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh504_str"]("  Gennaio  ", "x") == "Gennaio"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh504_str"](bad, "x")

    def test_pct_ok(self):
        assert _F["mh504_pct"](0, "x") == 0.0
        assert _F["mh504_pct"](100, "x") == 100.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, "5", None):
            with pytest.raises(ValueError):
                _F["mh504_pct"](bad, "x")

    def test_periodo_ok(self):
        p = _F["mh504_periodo"](" Q1 ", 100.0, -90.0)
        assert p == {"nome": "Q1", "d_hedge": 100.0, "d_item": -90.0}

    def test_periodo_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_periodo"]("", 100.0, -90.0)
        with pytest.raises(ValueError):
            _F["mh504_periodo"]("Q1", "100", -90.0)
        with pytest.raises(ValueError):
            _F["mh504_periodo"]("Q1", 100.0, float("nan"))


class TestW504LowerOf:
    def test_hedge_zero(self):
        assert _F["mh504_lower_of"](0.0, 5000.0) == 0.0
        assert _F["mh504_lower_of"](1e-12, -3000.0) == 0.0

    def test_min_item(self):
        # |I| < |H| -> efficace = I col segno di H
        assert _F["mh504_lower_of"](1000000.0, -800000.0) == 800000.0
        assert _F["mh504_lower_of"](-1000000.0, 800000.0) == -800000.0

    def test_min_hedge(self):
        # |H| < |I| -> efficace = H
        assert _F["mh504_lower_of"](-150.0, -200.0) == -150.0
        assert _F["mh504_lower_of"](150.0, -200.0) == 150.0

    def test_uguali(self):
        assert _F["mh504_lower_of"](1000000.0, -1000000.0) == 1000000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_lower_of"]("x", 1.0)


class TestW504Diario:
    def test_gennaio_efficace(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[0]
        assert r["cum_hedge"] == 1000000.0
        assert r["cum_item"] == -1000000.0
        assert r["eff_cum"] == 1000000.0
        assert r["ineff_cum"] == 0.0
        assert r["eff_periodo"] == 1000000.0
        assert r["ineff_periodo"] == 0.0
        assert r["verdetto"] == "EFFICACE"

    def test_febbraio_entro_soglia(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[1]
        assert r["cum_hedge"] == 1500000.0
        assert r["cum_item"] == -1480000.0
        assert r["eff_cum"] == 1480000.0
        assert r["ineff_cum"] == 20000.0
        assert r["ineff_periodo"] == 20000.0
        assert r["eff_periodo"] == 480000.0
        assert r["soglia"] == pytest.approx(25000.0)
        assert r["verdetto"] == "INEFFICACE_ENTRO_SOGLIA"

    def test_marzo_oltre_soglia(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[2]
        assert r["cum_hedge"] == 1300000.0
        assert r["cum_item"] == -1220000.0
        assert r["eff_cum"] == 1220000.0
        assert r["ineff_cum"] == 80000.0
        assert r["ineff_periodo"] == 60000.0
        assert r["eff_periodo"] == -260000.0
        assert r["soglia"] == pytest.approx(10000.0)
        assert r["verdetto"] == "INEFFICACE_OLTRE_SOGLIA"

    def test_aprile_oltre_soglia(self):
        r = _F["mh504_inefficacia"](_demo(), TOL)[3]
        assert r["cum_hedge"] == 300000.0
        assert r["cum_item"] == -120000.0
        assert r["eff_cum"] == 120000.0
        assert r["ineff_cum"] == 180000.0
        assert r["ineff_periodo"] == 100000.0
        assert r["eff_periodo"] == -1100000.0
        assert r["soglia"] == pytest.approx(50000.0)
        assert r["verdetto"] == "INEFFICACE_OLTRE_SOGLIA"

    def test_identita_contabile(self):
        # d_hedge = eff_periodo + ineff_periodo per ogni riga
        for r in _F["mh504_inefficacia"](_demo(), TOL):
            assert r["d_hedge"] == pytest.approx(r["eff_periodo"] + r["ineff_periodo"])
            assert r["cum_hedge"] == pytest.approx(r["eff_cum"] + r["ineff_cum"])

    def test_tolleranza_zero(self):
        # con tolleranza 0, qualsiasi inefficacia != 0 e' OLTRE_SOGLIA
        demo = [_F["mh504_periodo"]("A", 1000.0, -990.0)]
        assert _F["mh504_inefficacia"](demo, 0.0)[0]["verdetto"] == \
            "INEFFICACE_OLTRE_SOGLIA"

    def test_soglia_rispettata_con_tolleranza_alta(self):
        demo = [_F["mh504_periodo"]("A", 1000.0, -990.0)]
        assert _F["mh504_inefficacia"](demo, 100.0)[0]["verdetto"] == \
            "INEFFICACE_ENTRO_SOGLIA"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_inefficacia"]([], TOL)
        with pytest.raises(ValueError):
            _F["mh504_inefficacia"](_demo(), -1.0)
        with pytest.raises(ValueError):
            _F["mh504_inefficacia"](_demo(), 101.0)


class TestW504Riepilogo:
    def test_demo(self):
        s = _F["mh504_riepilogo"](_demo(), TOL)
        assert s["n_periodi"] == 4
        assert s["conteggi"] == {"EFFICACE": 1, "INEFFICACE_ENTRO_SOGLIA": 1,
                                 "INEFFICACE_OLTRE_SOGLIA": 2}
        assert s["verdetto_complessivo"] == "INEFFICACE_OLTRE_SOGLIA"
        assert s["oci_cum_eur"] == 120000.0
        assert s["pnl_cum_eur"] == 180000.0
        assert s["ratio_inefficacia"] == pytest.approx(0.6)
        assert s["periodi_con_inefficacia"] == 3
        assert len(s["righe"]) == 4

    def test_tutto_efficace(self):
        demo = [_F["mh504_periodo"]("A", 1000.0, -1000.0),
                _F["mh504_periodo"]("B", -500.0, 500.0)]
        s = _F["mh504_riepilogo"](demo, TOL)
        assert s["verdetto_complessivo"] == "EFFICACE"
        assert s["oci_cum_eur"] == 500.0
        assert s["pnl_cum_eur"] == 0.0
        assert s["ratio_inefficacia"] == 0.0
        assert s["periodi_con_inefficacia"] == 0

    def test_severita_complessivo(self):
        # il piu' severo vince: ENTRO < OLTRE
        demo = [_F["mh504_periodo"]("A", 1000.0, -990.0),   # entro soglia 5%
                _F["mh504_periodo"]("B", 1000.0, -1000.0)]  # efficace
        s = _F["mh504_riepilogo"](demo, TOL)
        assert s["verdetto_complessivo"] == "INEFFICACE_ENTRO_SOGLIA"

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh504_riepilogo"]([], TOL)


def test_registry_tab504():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 517
    assert TITLE504 in titoli
    assert src.count(TITLE504) == 3
    assert "tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517 = st.tabs([" in src
    assert "    with tab504:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab504" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab504" in withs
    assert len(withs) == len(dvars) == 517
    # ordine: tab504 dopo tab503
    _decl504 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl504.index(f'"{TITLE503}"') < _decl504.index(f'"{TITLE504}"')
    assert titoli[dvars.index("tab504")] == TITLE504


def test_chiavi_st504_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st504_[^"]+)"', src) + re.findall(
        r'key=f"(st504_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
