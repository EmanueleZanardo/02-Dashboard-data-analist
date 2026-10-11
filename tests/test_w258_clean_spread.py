"""Test tab258 'Clean spread (con CO2)': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab258.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cs258_num", "cs258_fattori_default", "cs258_spread",
          "cs258_confronto", "cs258_co2_break_even", "cs258_sensibilita_co2")
cs258_num = _F["cs258_num"]
cs258_fattori_default = _F["cs258_fattori_default"]
cs258_spread = _F["cs258_spread"]
cs258_confronto = _F["cs258_confronto"]
cs258_co2_break_even = _F["cs258_co2_break_even"]
cs258_sensibilita_co2 = _F["cs258_sensibilita_co2"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab258:
    def test_tab258_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 370
        assert "🌿 Clean spread (con CO₂)" in titoli
        assert "tab258" in dvars
        assert "tab258" in withs
        assert titoli[dvars.index("tab258")] == "🌿 Clean spread (con CO₂)"
        assert titoli[-1] == "Kelly e drawdown: probabilità di toccare un max drawdown"
        keys = re.findall(r'key="(cs258_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8

    def test_titoli_allineati_257_258(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab257")] == "🔥 Teleriscaldamento vs caldaia"
        assert titoli[dvars.index("tab258")] == "🌿 Clean spread (con CO₂)"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("cs258_num", "cs258_fattori_default", "cs258_spread",
                   "cs258_confronto", "cs258_co2_break_even",
                   "cs258_sensibilita_co2"):
            assert src.index(f"def {fn}(") < i_ws
            assert src.index(f"    with tab258:") > i_ws


class TestCs258Num:
    def test_validi(self):
        assert cs258_num(10, "x") == 10.0
        assert cs258_num(2.5, "x") == 2.5
        assert cs258_num(-3, "x") == -3.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            cs258_num(True, "x")

    def test_non_numeri(self):
        for v in ("10", None, [1], {"a": 1}):
            with pytest.raises(ValueError):
                cs258_num(v, "x")

    def test_nan_inf(self):
        for v in (math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                cs258_num(v, "x")


class TestCs258FattoriDefault:
    def test_valori(self):
        d = cs258_fattori_default()
        assert d == {"gas": 0.202, "carbone": 0.341}


class TestCs258Spread:
    def test_gas(self):
        # P=95, F=40, HR=2.0, CO2=80, EF=0.202
        # spread = 95-80 = 15.0; co2 = 80*0.202*2 = 32.32;
        # clean = -17.32; breakeven = 112.32
        r = cs258_spread(95.0, 40.0, 2.0, 80.0, 0.202)
        assert r["spread_eur_mwh"] == pytest.approx(15.0)
        assert r["costo_co2_eur_mwh"] == pytest.approx(32.32)
        assert r["clean_spread_eur_mwh"] == pytest.approx(-17.32)
        assert r["breakeven_power_eur_mwh"] == pytest.approx(112.32)

    def test_carbone(self):
        # P=95, F=15, HR=2.5, CO2=80, EF=0.341
        # spread = 95-37.5 = 57.5; co2 = 80*0.341*2.5 = 68.2;
        # clean = -10.7; breakeven = 105.7
        r = cs258_spread(95.0, 15.0, 2.5, 80.0, 0.341)
        assert r["spread_eur_mwh"] == pytest.approx(57.5)
        assert r["costo_co2_eur_mwh"] == pytest.approx(68.2)
        assert r["clean_spread_eur_mwh"] == pytest.approx(-10.7)
        assert r["breakeven_power_eur_mwh"] == pytest.approx(105.7)

    def test_senza_co2(self):
        r = cs258_spread(100.0, 30.0, 2.0, 0.0, 0.202)
        assert r["clean_spread_eur_mwh"] == pytest.approx(40.0)
        assert r["costo_co2_eur_mwh"] == pytest.approx(0.0)

    def test_power_negativo_ammesso(self):
        r = cs258_spread(-10.0, 40.0, 2.0, 80.0, 0.202)
        assert r["clean_spread_eur_mwh"] == pytest.approx(-122.32)

    def test_errori(self):
        with pytest.raises(ValueError):
            cs258_spread(95.0, -1.0, 2.0, 80.0, 0.202)
        with pytest.raises(ValueError):
            cs258_spread(95.0, 40.0, 0.0, 80.0, 0.202)
        with pytest.raises(ValueError):
            cs258_spread(95.0, 40.0, 2.0, -5.0, 0.202)
        with pytest.raises(ValueError):
            cs258_spread(95.0, 40.0, 2.0, 80.0, -0.1)
        with pytest.raises(ValueError):
            cs258_spread(95.0, 40.0, True, 80.0, 0.202)


class TestCs258Confronto:
    def test_carbone_marginale(self):
        r = cs258_confronto(-17.32, -10.7)
        assert r["marginale"] == "carbone"
        assert r["diff_eur_mwh"] == pytest.approx(-6.62)
        assert r["entrambi_negativi"] is True
        assert r["entrambi_positivi"] is False

    def test_gas_marginale(self):
        r = cs258_confronto(10.0, 3.0)
        assert r["marginale"] == "gas"
        assert r["diff_eur_mwh"] == pytest.approx(7.0)
        assert r["entrambi_positivi"] is True

    def test_pari(self):
        r = cs258_confronto(5.0, 5.0)
        assert r["marginale"] == "pari"
        assert r["diff_eur_mwh"] == pytest.approx(0.0)


class TestCs258Co2BreakEven:
    def test_gas(self):
        # (95-80)/(0.202*2) = 15/0.404 = 37.1287128712871...
        be = cs258_co2_break_even(95.0, 40.0, 2.0, 0.202)
        assert be == pytest.approx(37.12871287128713)

    def test_negativo_fuori_mercato(self):
        # spread gia' negativo a CO2=0
        be = cs258_co2_break_even(50.0, 40.0, 2.0, 0.202)
        assert be < 0

    def test_ef_zero_none(self):
        assert cs258_co2_break_even(95.0, 40.0, 2.0, 0.0) is None

    def test_errori(self):
        with pytest.raises(ValueError):
            cs258_co2_break_even(95.0, 40.0, 0.0, 0.202)


class TestCs258SensibilitaCo2:
    def test_griglia(self):
        righe = cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, 0.0, 100.0, 3)
        assert len(righe) == 3
        assert [r["prezzo_co2_eur_t"] for r in righe] == pytest.approx([0.0, 50.0, 100.0])
        # a CO2=0 il clean e' lo spark; poi decresce linearmente
        assert righe[0]["clean_spread_eur_mwh"] == pytest.approx(15.0)
        assert righe[1]["clean_spread_eur_mwh"] == pytest.approx(15.0 - 50 * 0.202 * 2)
        assert righe[2]["clean_spread_eur_mwh"] == pytest.approx(15.0 - 100 * 0.202 * 2)
        assert righe[2]["costo_co2_eur_mwh"] == pytest.approx(40.4)

    def test_deterministico(self):
        a = cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, 0.0, 150.0)
        b = cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, 0.0, 150.0)
        assert a == b
        assert len(a) == 21

    def test_errori(self):
        with pytest.raises(ValueError):
            cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, 0.0, 100.0, 1)
        with pytest.raises(ValueError):
            cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, 100.0, 100.0)
        with pytest.raises(ValueError):
            cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, -10.0, 100.0)
        with pytest.raises(ValueError):
            cs258_sensibilita_co2(95.0, 40.0, 2.0, 0.202, 0.0, 100.0, True)
