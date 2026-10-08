"""Test tab231 (stile pytest): Qualita' dati - gap, outlier IQR, spike.

Funzioni pure dq231_* estratte da app.py via AST (tests/appfuncs).
Stile QA: numeri calcolati a mano + determinismo + registry tab231.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

from appfuncs import load

_F = load(
    "dq231_genera_serie",
    "dq231_detect_gaps",
    "dq231_detect_outliers_iqr",
    "dq231_detect_spikes",
    "dq231_quality_summary",
)
dq231_genera_serie = _F["dq231_genera_serie"]
dq231_detect_gaps = _F["dq231_detect_gaps"]
dq231_detect_outliers_iqr = _F["dq231_detect_outliers_iqr"]
dq231_detect_spikes = _F["dq231_detect_spikes"]
dq231_quality_summary = _F["dq231_quality_summary"]


def _df_ore(n, prezzo=50.0, inizio="2026-01-01"):
    ts = pd.date_range(inizio, periods=n, freq="h")
    return pd.DataFrame({"timestamp": ts, "prezzo": float(prezzo)})


# ------------------------------------------------------- numeri a mano
class TestNumeriAMano:
    def test_gap_singolo(self):
        # 10 ore, mancano le ore 03,04,05 -> un gap da 3 ore
        df = _df_ore(10).drop(index=[3, 4, 5]).reset_index(drop=True)
        gaps = dq231_detect_gaps(df)
        assert len(gaps) == 1
        g = gaps[0]
        assert g["ore_mancanti"] == 3
        assert g["inizio"] == pd.Timestamp("2026-01-01 03:00")
        assert g["fine"] == pd.Timestamp("2026-01-01 05:00")

    def test_due_gap_separati(self):
        # mancano ora 02 e ore 07-08 -> due gap distinti
        df = _df_ore(10).drop(index=[2, 7, 8]).reset_index(drop=True)
        gaps = dq231_detect_gaps(df)
        assert len(gaps) == 2
        assert [g["ore_mancanti"] for g in gaps] == [1, 2]

    def test_nessun_gap(self):
        assert dq231_detect_gaps(_df_ore(24)) == []

    def test_outlier_iqr_evidente(self):
        # dieci valori a 50 e uno a 500: q1=q3=50, iqr=0 -> outlier solo il 500
        df = pd.DataFrame({
            "timestamp": pd.date_range("2026-01-01", periods=11, freq="h"),
            "prezzo": [50.0] * 10 + [500.0],
        })
        r = dq231_detect_outliers_iqr(df, k=1.5)
        assert r["n_outlier"] == 1
        assert r["q1"] == 50.0 and r["q3"] == 50.0 and r["iqr"] == 0.0
        assert r["soglia_bassa"] == 50.0 and r["soglia_alta"] == 50.0
        assert bool(r["mask"][-1]) is True
        assert int(r["mask"].sum()) == 1
        assert bool(r["mask"][0]) is False

    def test_spike_oltre_soglia(self):
        # 100 -> 105 (+5%) -> 200 (+90.48%) -> 210 (+5%): spike solo all'indice 2
        df = pd.DataFrame({
            "timestamp": pd.date_range("2026-01-01", periods=4, freq="h"),
            "prezzo": [100.0, 105.0, 200.0, 210.0],
        })
        r = dq231_detect_spikes(df, soglia_pct=50.0)
        assert r["n_spike"] == 1
        assert list(r["mask"]) == [False, False, True, False]
        assert abs(r["variazioni_pct"][2] - 90.47619047619048) < 1e-9
        assert abs(r["variazioni_pct"][1] - 5.0) < 1e-9

    def test_summary_numeri(self):
        df = _df_ore(8)
        gaps = [{"inizio": pd.Timestamp("2026-01-01 02:00"),
                 "fine": pd.Timestamp("2026-01-01 03:00"), "ore_mancanti": 2}]
        out = {"mask": np.array([True] + [False] * 7), "n_outlier": 1}
        spk = {"mask": np.array([False, True] + [False] * 6), "n_spike": 1}
        s = dq231_quality_summary(df, gaps, out, spk)
        assert s["ore_effettive"] == 8
        assert s["ore_mancanti"] == 2
        assert s["ore_attese"] == 10
        assert abs(s["pct_ore_mancanti"] - 20.0) < 1e-9
        assert s["n_gap"] == 1
        assert s["gap_piu_lungo_ore"] == 2
        assert s["n_ore_anomale"] == 2  # unione senza doppi conteggi
        assert abs(s["pct_ore_anomale"] - 25.0) < 1e-9


class TestDeterminismo:
    def test_genera_serie_deterministica(self):
        df1, inj1 = dq231_genera_serie(168, 90.0, 5.0, 5, 60.0, 2, 10, 7)
        df2, inj2 = dq231_genera_serie(168, 90.0, 5.0, 5, 60.0, 2, 10, 7)
        assert df1.equals(df2)
        assert inj1 == inj2

    def test_genera_serie_senza_gap(self):
        df, inj = dq231_genera_serie(168, 90.0, 0.0, 5, 60.0, 0, 12, 7)
        assert len(df) == 168
        assert len(inj) == 5
        assert list(df.columns) == ["timestamp", "prezzo"]

    def test_genera_serie_con_gap_accorcia(self):
        df, _ = dq231_genera_serie(168, 90.0, 5.0, 3, 60.0, 2, 10, 7)
        assert len(df) < 168
        assert len(df) >= 168 - 2 * 10


class TestRegistryTab231:
    def test_tab231_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 313
        assert "🔍 Qualità dati (gap & outlier)" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab231" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab231" in withs
        assert len(withs) == len(dvars) == 313
        keys = re.findall(r'key="(t231_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10
