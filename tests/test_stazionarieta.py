"""Test calcola_test_stazionarieta - tab171 (stile pytest, via appfuncs).

Copertura: white noise -> stazionaria; random walk -> radice unitaria in
livelli e stazionaria alle differenze (I(1)); serie costante; casi di errore
(serie vuota/corta/non numerica/parametri invalidi); lag fisso rispettato;
tz-aware e NaN; determinismo; replicazione indipendente della statistica ADF
con codice scritto a parte; registry tab171.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_test_stazionarieta")
tst = fns["calcola_test_stazionarieta"]


def serie_ore(valori, start="2025-01-01"):
    idx = pd.date_range(start, periods=len(valori), freq="h")
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


def white_noise(n=2000, seed=7, sigma=5.0):
    rng = np.random.default_rng(seed)
    return serie_ore(100.0 + rng.normal(0, sigma, n))


def random_walk(n=2000, seed=11, sigma=2.0, start=100.0):
    rng = np.random.default_rng(seed)
    return serie_ore(start + np.cumsum(rng.normal(0, sigma, n)))


# ---------------------------------------------------------------- white noise
class TestWhiteNoise:
    def test_stazionaria(self):
        r = tst(white_noise())
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "STAZIONARIA"
        assert r["rifiuta_5"] is True
        assert r["ordine_integrazione"] == "I(0)"
        assert r["stat"] < r["cv"][5] < 0  # piu' negativa del critico 5%

    def test_lag_ragionevoli(self):
        r = tst(white_noise())
        assert 0 <= r["lags"] <= 12
        assert r["n_obs"] == 2000


# ---------------------------------------------------------------- random walk
class TestRandomWalk:
    def test_radice_unitaria_livelli(self):
        r = tst(random_walk())
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "RADICE UNITARIA"
        assert r["rifiuta_5"] is False
        assert r["stat"] > r["cv"][5]  # non rifiuta H0

    def test_differenze_stazionarie_i1(self):
        r = tst(random_walk())
        assert r["stat_diff"] is not None
        assert r["rifiuta_diff_5"] is True
        assert r["ordine_integrazione"] == "I(1)"

    def test_con_trend(self):
        # random walk con drift: con costante+trend resta non stazionario
        rw = random_walk() + np.arange(2000) * 0.05
        r = tst(rw, regression="ct")
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "RADICE UNITARIA"


# ------------------------------------------------------- serie deterministica
class TestSerieCostante:
    def test_costante_stazionaria(self):
        r = tst(serie_ore(np.full(500, 80.0)))
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "STAZIONARIA"
        assert r["serie_costante"] is True
        assert r["ordine_integrazione"] == "I(0)"

    def test_ar1_senza_rumore(self):
        # y_t = 0.9*y_{t-1} esatto -> fit perfetto, gamma<0 -> stazionaria
        y = 100.0 * 0.9 ** np.arange(400)
        r = tst(serie_ore(y))
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "STAZIONARIA"
        assert r["stat"] == -np.inf


# ------------------------------------------------------------------- errori
class TestErrori:
    def test_serie_vuota(self):
        r = tst(pd.Series([], dtype=float))
        assert r["valido"] is False and "30" in r["errore"]

    def test_serie_troppo_corta(self):
        r = tst(serie_ore(np.ones(20)))
        assert r["valido"] is False and "30" in r["errore"]

    def test_non_numerica(self):
        r = tst(pd.Series(["a", "b"] * 20))
        assert r["valido"] is False

    def test_regression_invalida(self):
        r = tst(white_noise(), regression="xx")
        assert r["valido"] is False

    def test_lags_invalido(self):
        assert tst(white_noise(), lags=-1)["valido"] is False
        assert tst(white_noise(), lags="molti")["valido"] is False

    def test_max_lags_invalido(self):
        assert tst(white_noise(), max_lags=-2)["valido"] is False

    def test_lag_fisso_troppo_alto(self):
        r = tst(white_noise(n=40), lags=30)
        assert r["valido"] is False

    def test_tutti_nan(self):
        r = tst(pd.Series([np.nan] * 50))
        assert r["valido"] is False


# ------------------------------------------------------------------ robustezza
class TestRobustezza:
    def test_nan_intermedi(self):
        s = white_noise()
        s.iloc[10:20] = np.nan
        r = tst(s)
        assert r["valido"] and r["n_obs"] == 1990
        assert r["verdetto"] == "STAZIONARIA"

    def test_tz_aware(self):
        s = white_noise()
        s.index = s.index.tz_localize("Europe/Zurich")
        r = tst(s)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "STAZIONARIA"
        assert len(r["rolling"]) > 0

    def test_lag_fisso_rispettato(self):
        r = tst(white_noise(), lags=3)
        assert r["valido"] and r["lags"] == 3 and r["lags_auto"] is False

    def test_max_lags_tetto(self):
        r = tst(white_noise(), max_lags=2)
        assert r["valido"] and r["lags"] <= 2

    def test_determinismo(self):
        s = white_noise()
        a, b = tst(s)["stat"], tst(s)["stat"]
        assert a == b

    def test_regression_n(self):
        r = tst(white_noise(), regression="n")
        assert r["valido"] and r["regression"] == "n"
        assert set(r["cv"]) == {1, 5, 10}

    def test_rolling_mensile(self):
        s = white_noise(n=24 * 90)  # ~3 mesi
        r = tst(s)
        assert r["valido"]
        df = r["rolling"]
        assert list(df.columns) == ["Mese", "Ore", "Statistica", "Verdetto"]
        assert len(df) == 3
        assert df["Verdetto"].isin(["STAZIONARIA"]).all()
        assert 0.0 <= r["quota_mesi_stazionari"] <= 1.0


# ------------------------------------------- replicazione indipendente (ADF)
class TestReplicaIndipendente:
    def test_statistica_manuale(self):
        """Ricalcola t(gamma) con codice indipendente e confronta."""
        s = white_noise(n=500, seed=42)
        y = s.to_numpy()
        p = 4
        dy, yl = np.diff(y), y[:-1]
        n = len(y) - 1 - p
        X = np.column_stack(
            [np.ones(n), yl[p:]] +
            [dy[p - i: len(y) - 1 - i] for i in range(1, p + 1)]
        )
        Y = dy[p:]
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        resid = Y - X @ beta
        s2 = resid @ resid / (n - X.shape[1])
        se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
        t_manuale = beta[1] / se

        r = tst(s, lags=p)
        assert r["valido"], r["errore"]
        assert r["stat"] == pytest.approx(t_manuale, rel=1e-9)
        assert r["stat"] < -2.862  # critico 5% con costante


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab171_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab171" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab171" in withs
        assert len(withs) == len(dvars) >= 171
        assert '"📏 Test di stazionarietà"' in src
        keys = re.findall(r'key="(st171_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 4
        assert re.search(r"^def calcola_test_stazionarieta\(", src, re.M) is not None
