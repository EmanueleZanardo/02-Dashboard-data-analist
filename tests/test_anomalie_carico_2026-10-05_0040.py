"""Test tab219 (stile pytest): Anomalie di carico.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_anomalie_carico", "genera_demo_carico_anomalie")
calcola_anomalie_carico = _F["calcola_anomalie_carico"]
genera_demo_carico_anomalie = _F["genera_demo_carico_anomalie"]

_IDX60 = pd.date_range("2026-01-05", periods=60 * 24, freq="h")


def _serie_rumore(seed=7, media=1000.0, sigma=5.0):
    rng = np.random.default_rng(seed)
    return pd.Series(media + rng.normal(0.0, sigma, len(_IDX60)),
                     index=_IDX60, name="Carico (kW)")


class TestAnomalieCaricoBase:
    def test_demo_deterministica(self):
        d1 = genera_demo_carico_anomalie()
        d2 = genera_demo_carico_anomalie()
        assert d1.equals(d2)
        assert len(d1) == 60 * 24
        r = calcola_anomalie_carico(d1)
        assert r["errore"] is None and r["valido"]
        assert r["n_episodi"] == 4
        tipi = set(r["df_episodi"]["Tipo"])
        assert tipi == {"⚡ Picco", "🧊 Zero", "🧱 Piatto", "📉 Crollo"}
        zero = r["df_episodi"][r["df_episodi"]["Tipo"] == "🧊 Zero"].iloc[0]
        assert zero["Ore"] == 30
        picco = r["df_episodi"][r["df_episodi"]["Tipo"] == "⚡ Picco"].iloc[0]
        assert picco["Ore"] == 6
        assert picco["Scostamento (MWh)"] == pytest.approx(5.4, abs=0.05)
        assert r["verdetto"].startswith("🔴")

    def test_numeri_a_mano_spike(self):
        s = _serie_rumore()
        s.iloc[100:106] = s.iloc[100:106] + 500.0
        r = calcola_anomalie_carico(s)
        assert r["errore"] is None
        assert r["n_episodi"] == 1
        ep = r["df_episodi"].iloc[0]
        assert ep["Tipo"] == "⚡ Picco"
        assert ep["Ore"] == 6
        assert ep["Scostamento (MWh)"] == pytest.approx(3.0, abs=0.05)
        assert r["verdetto"].startswith("🟠")  # |z| >> 6

    def test_zero_run(self):
        s = _serie_rumore()
        s.iloc[200:230] = 0.0
        r = calcola_anomalie_carico(s)
        assert r["errore"] is None
        assert r["n_episodi"] == 1
        ep = r["df_episodi"].iloc[0]
        assert ep["Tipo"] == "🧊 Zero"
        assert ep["Ore"] == 30
        assert ep["Scostamento (MWh)"] == pytest.approx(-30.0, abs=0.2)
        assert r["verdetto"].startswith("🔴")

    def test_piatto_run(self):
        s = _serie_rumore(media=800.0, sigma=3.0)
        s.iloc[300:324] = 777.7
        r = calcola_anomalie_carico(s)
        assert r["errore"] is None
        assert r["n_episodi"] == 1
        ep = r["df_episodi"].iloc[0]
        assert ep["Tipo"] == "🧱 Piatto"
        assert ep["Ore"] == 24
        assert r["verdetto"].startswith("🔴")

    def test_serie_intera_piatta_e_zero(self):
        idx = pd.date_range("2026-01-01", periods=200, freq="h")
        r = calcola_anomalie_carico(pd.Series(np.full(200, 500.0),
                                              index=idx))
        assert r["errore"] is None and r["verdetto"].startswith("🔴")
        assert r["df_episodi"].iloc[0]["Tipo"] == "🧱 Piatto"
        r = calcola_anomalie_carico(pd.Series(np.zeros(200), index=idx))
        assert r["errore"] is None and r["verdetto"].startswith("🔴")
        assert r["df_episodi"].iloc[0]["Tipo"] == "🧊 Zero"

    def test_serie_pulita(self):
        r = calcola_anomalie_carico(_serie_rumore())
        assert r["errore"] is None
        assert r["n_episodi"] == 0
        assert r["verdetto"].startswith("🟢")

    def test_prezzo_controvalore(self):
        s = _serie_rumore()
        s.iloc[100:106] = s.iloc[100:106] + 500.0
        r = calcola_anomalie_carico(s, prezzo_eur_mwh=100.0)
        assert r["errore"] is None
        assert r["costo_stimato_eur"] == pytest.approx(
            r["impatto_tot_mwh"] * 100.0, abs=0.01)
        assert r["df_episodi"].iloc[0]["Costo stimato (€)"] == \
            pytest.approx(r["df_episodi"].iloc[0]["Scostamento (MWh)"]
                          * 100.0, abs=0.2)  # doppio arrotondamento

    def test_tz_aware_ok(self):
        s = _serie_rumore()
        s.index = s.index.tz_localize("Europe/Zurich")
        r = calcola_anomalie_carico(s)
        assert r["errore"] is None and r["valido"]


class TestAnomalieCaricoInvalidi:
    def test_serie_vuota_e_non_datetime(self):
        assert calcola_anomalie_carico(
            pd.Series([], dtype=float,
                      index=pd.DatetimeIndex([])))["errore"]
        assert calcola_anomalie_carico(
            pd.Series([1.0, 2.0, 3.0]))["errore"]
        assert calcola_anomalie_carico(
            pd.Series(["a"] * 200,
                      index=pd.date_range("2026-01-01", periods=200,
                                          freq="h")))["errore"]

    def test_serie_troppo_corta(self):
        idx = pd.date_range("2026-01-01", periods=100, freq="h")
        assert calcola_anomalie_carico(
            pd.Series(np.ones(100), index=idx))["errore"]

    def test_soglia_non_valida(self):
        d = genera_demo_carico_anomalie()
        for bad in [0, -1.0, 21.0, "x", True, None, np.nan]:
            assert calcola_anomalie_carico(d, soglia_z=bad)["errore"], bad

    def test_run_non_valido(self):
        d = genera_demo_carico_anomalie()
        for bad in [0, -3, "x", True, None, 2.5]:
            assert calcola_anomalie_carico(d, run_min_ore=bad)["errore"], \
                bad

    def test_prezzo_non_valido(self):
        d = genera_demo_carico_anomalie()
        for bad in [-5.0, "x", True, float("inf"), float("nan")]:
            assert calcola_anomalie_carico(d,
                                           prezzo_eur_mwh=bad)["errore"], bad


# ------------------------------------------------------- registry
class TestRegistryTab219:
    def test_tab219_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 321
        assert titoli[-1] == "🧪📉 Backtest VaR: il modello resiste al tempo?"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab219" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab219" in withs
        assert len(withs) == len(dvars) == 321
        keys = re.findall(r'key="(ac219_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 4
