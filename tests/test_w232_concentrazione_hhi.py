"""Test tab232 "Concentrazione temporale (HHI)": funzioni pure + registry."""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from appfuncs import load

_fns = load("hhi_index", "effective_hours", "top_hours_share",
            "ore_per_copertura", "cumulative_curve",
            "genera_costi_orari_sintetici")
hhi_index = _fns["hhi_index"]
effective_hours = _fns["effective_hours"]
top_hours_share = _fns["top_hours_share"]
ore_per_copertura = _fns["ore_per_copertura"]
cumulative_curve = _fns["cumulative_curve"]
genera_costi_orari_sintetici = _fns["genera_costi_orari_sintetici"]


class TestRegistryTab232:
    def test_tab232_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 282
        assert "🧮 Concentrazione temporale (HHI)" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab232" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab232" in withs
        assert len(withs) == len(dvars) == 282
        keys = re.findall(r'key="(t232_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10


class TestHhiPure:
    def test_hhi_uniforme(self):
        # costo uniforme su N ore -> HHI = 1/N
        assert hhi_index([10.0] * 100) == 1 / 100

    def test_hhi_massima_concentrazione(self):
        assert hhi_index([0.0, 0.0, 50.0]) == 1.0

    def test_hhi_bounds(self):
        c = [5.0, 1.0, 3.0, 2.0, 9.0]
        h = hhi_index(c)
        assert 1 / len(c) <= h <= 1.0

    def test_hhi_vuoto_nan(self):
        assert np.isnan(hhi_index([]))
        assert np.isnan(hhi_index([0.0, -1.0]))

    def test_effective_hours(self):
        assert effective_hours([10.0] * 100) == 100.0
        assert effective_hours([0.0, 0.0, 50.0]) == 1.0

    def test_effective_hours_bounds(self):
        c = [5.0, 1.0, 3.0, 2.0, 9.0]
        e = effective_hours(c)
        assert 1.0 <= e <= len(c)

    def test_top_hours_share(self):
        c = [1.0, 2.0, 3.0, 4.0]  # tot 10
        assert top_hours_share(c, 1) == 0.4
        assert top_hours_share(c, 2) == 0.7
        assert top_hours_share(c, 99) == 1.0  # k oltre N -> tutto
        assert np.isnan(top_hours_share(c, 0))
        assert np.isnan(top_hours_share([], 5))

    def test_ore_per_copertura(self):
        c = [40.0] + [1.0] * 60  # tot 100, prima ora = 40%
        assert ore_per_copertura(c, 40.0) == 1.0
        assert ore_per_copertura(c, 80.0) == 41.0

    def test_cumulative_curve(self):
        df = cumulative_curve([1.0, 2.0, 3.0, 4.0])
        assert list(df.columns) == ["ora_rank", "costo_eur", "quota_costo",
                                    "costo_cumulato_pct"]
        assert len(df) == 4
        assert df["costo_eur"].iloc[0] == 4.0  # decrescente
        assert abs(df["costo_cumulato_pct"].iloc[-1] - 100.0) < 1e-9
        assert (df["costo_cumulato_pct"].diff().fillna(df["costo_cumulato_pct"].iloc[0]) >= 0).all()

    def test_cumulative_curve_vuota(self):
        df = cumulative_curve([])
        assert df.empty

    def test_genera_sintetici(self):
        c = genera_costi_orari_sintetici(8760, 80.0, 250.0, 120, seed=7)
        assert len(c) == 8760
        assert (c > 0).all()
        c2 = genera_costi_orari_sintetici(8760, 80.0, 250.0, 120, seed=7)
        assert np.array_equal(c, c2)  # riproducibile
        # con picchi la concentrazione deve salire
        base = genera_costi_orari_sintetici(8760, 80.0, 0.0, 0, seed=7)
        assert hhi_index(c) > hhi_index(base)
