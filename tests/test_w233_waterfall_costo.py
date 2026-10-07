"""Test tab233 (stile pytest): Waterfall del costo.

Funzioni pure build_waterfall / waterfall_total / waterfall_quote_pct
estratte da app.py via AST (tests/appfuncs). Stile QA: numeri calcolati
a mano + validazione + determinismo + registry tab233.
"""

import re
from pathlib import Path

from appfuncs import load

_F = load("build_waterfall", "waterfall_total", "waterfall_quote_pct")
build_waterfall = _F["build_waterfall"]
waterfall_total = _F["waterfall_total"]
waterfall_quote_pct = _F["waterfall_quote_pct"]

_COMP = {"Energia": 540.0, "Perdite di rete": 35.0, "Oneri di sistema": 120.0,
         "Accise": 61.29, "IVA": 75.63}
_TOT = 831.92  # 540 + 35 + 120 + 61.29 + 75.63


# ------------------------------------------------------- numeri a mano
class TestNumeriAMano:
    def test_cumulata(self):
        df = build_waterfall(_COMP)
        assert list(df.columns) == ["componente", "valore_eur", "cumulata_eur"]
        assert list(df["componente"]) == list(_COMP.keys())
        attesi = [540.0, 575.0, 695.0, 756.29, 831.92]
        for got, att in zip(df["cumulata_eur"], attesi):
            assert abs(got - att) < 1e-9

    def test_totale(self):
        assert abs(waterfall_total(_COMP) - _TOT) < 1e-9

    def test_quote_sommano_100(self):
        q = waterfall_quote_pct(_COMP)
        assert list(q.columns) == ["componente", "quota_pct"]
        assert abs(q["quota_pct"].sum() - 100.0) < 1e-9
        iva = float(q.loc[q["componente"] == "IVA", "quota_pct"].iloc[0])
        assert abs(iva - 75.63 / _TOT * 100.0) < 1e-9

    def test_vuoto(self):
        df = build_waterfall({})
        assert df.empty
        assert list(df.columns) == ["componente", "valore_eur", "cumulata_eur"]
        assert waterfall_total({}) == 0.0

    def test_sconto_negativo(self):
        comp = {"Energia": 500.0, "Sconto": -50.0}
        assert abs(waterfall_total(comp) - 450.0) < 1e-9
        df = build_waterfall(comp)
        assert abs(df["cumulata_eur"].iloc[-1] - 450.0) < 1e-9

    def test_determinismo(self):
        a = build_waterfall(_COMP)
        b = build_waterfall(_COMP)
        assert a.equals(b)


# ------------------------------------------------------- registry tab233
class TestRegistryTab233:
    def test_tab233_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 292
        assert "💧 Waterfall del costo" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab233" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab233" in withs
        assert len(withs) == len(dvars) == 292
        keys = re.findall(r'key="(t233_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10
