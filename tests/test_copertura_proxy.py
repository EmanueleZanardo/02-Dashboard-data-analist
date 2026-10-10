"""Test tab195 (stile pytest): copertura proxy (cross-hedge) dello Swissix.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Modello: buyer paga lo spot Swissix pa ogni ora e compra h MW di forward
sull'hub B al prezzo F -> costo netto unitario c(h) = pa - h*(pb - F).
Ratio di minima varianza h* = Cov(pa,pb)/Var(pb); efficacia =
1 - Var(c(h*))/Var(pa) = R^2. La basis b = pa - pb e' il rischio residuo.

Numeri a mano (caso esatto: 24 ore, pa = 50 + 10*sin(2*pi*h/24),
pb = 0.5*pa + 10):
  Cov(pa,pb) = 0.5*Var(pa), Var(pb) = 0.25*Var(pa) -> h* = 2.0 esatto,
  R^2 = 1.0, std residua = 0. E[pa] = 50, E[pb] = 35; con F = 30:
  costo atteso coperto = 50 - 2*(35-30) = 40.0 €/MWh.
  Basis = pa - pb = 0.5*pa - 10 = 15 + 5*sin(...): ora 6 -> 20.0,
  ora 18 -> 10.0, media 15.0.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

from appfuncs import load

_F = load("calcola_copertura_proxy")
calcola_copertura_proxy = _F["calcola_copertura_proxy"]


def serie_esatta(fwd=30.0):
    idx = pd.date_range("2026-01-01", periods=24, freq="h")
    ore = np.arange(24, dtype=float)
    pa = 50.0 + 10.0 * np.sin(2 * np.pi * ore / 24.0)
    pb = 0.5 * pa + 10.0
    return (pd.Series(pa, index=idx, name="pa"),
            pd.Series(pb, index=idx, name="pb"), fwd)


def serie_rumorosa(n_ore=24 * 60, seed=11):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2026-01-01", periods=n_ore, freq="h")
    ore = idx.hour.to_numpy(dtype=float)
    pa = 70.0 + 15.0 * np.sin(2 * np.pi * ore / 24.0) + rng.normal(0, 5, n_ore)
    pb = 0.9 * pa + rng.normal(0, 8, n_ore)
    return pd.Series(pa, index=idx), pd.Series(pb, index=idx)


class TestCoperturaProxy:
    def test_h_star_esatto(self):
        pa, pb, fwd = serie_esatta()
        r = calcola_copertura_proxy(pa, pb, fwd)
        assert r["valido"] and r["errore"] is None
        assert r["n_ore"] == 24
        assert abs(r["h_star"] - 2.0) < 1e-9
        assert abs(r["r2"] - 1.0) < 1e-9
        assert r["std_residua_star"] < 1e-9
        assert abs(r["costo_atteso_spot"] - 50.0) < 1e-9
        assert abs(r["costo_atteso_star"] - 40.0) < 1e-9
        assert abs(r["basis_media"] - 15.0) < 1e-9
        assert abs(r["profilo_basis"][6] - 20.0) < 1e-9
        assert abs(r["profilo_basis"][18] - 10.0) < 1e-9
        assert len(r["profilo_basis"]) == 24
        assert len(r["df_h"]) == 81
        # il massimo dell'efficacia e' proprio a h = 2
        i_max = int(r["df_h"]["Efficacia (R^2)"].idxmax())
        assert abs(float(r["df_h"]["h (ratio)"].iloc[i_max]) - 2.0) < 0.05
        assert len(r["df_basis"]) == 24

    def test_naive_vs_star_rumoroso(self):
        pa, pb = serie_rumorosa()
        r = calcola_copertura_proxy(pa, pb, 65.0, mw=10.0)
        assert r["valido"]
        assert 0.0 < r["h_star"] < 2.0
        assert r["r2"] >= r["eff_naive"]
        assert r["std_residua_star"] <= r["std_residua_naive"]
        assert r["std_residua_star"] < r["std_spot"]
        assert 0.5 < r["r2"] < 1.0
        assert -1.0 <= r["correlazione"] <= 1.0
        # controvalori scalati su mw * n_ore
        assert abs(r["controvalore_spot"] - r["costo_atteso_spot"] * 10.0 * r["n_ore"]) < 1e-6
        assert abs(r["controvalore_star"] - r["costo_atteso_star"] * 10.0 * r["n_ore"]) < 1e-6

    def test_errore_serie_troppo_corta(self):
        idx = pd.date_range("2026-01-01", periods=10, freq="h")
        pa = pd.Series(np.ones(10) * 50.0, index=idx)
        pb = pd.Series(np.ones(10) * 45.0 + np.arange(10), index=idx)
        r = calcola_copertura_proxy(pa, pb, 40.0)
        assert not r["valido"] and r["errore"]

    def test_errore_serie_vuota(self):
        r = calcola_copertura_proxy(pd.Series(dtype=float), pd.Series(dtype=float), 40.0)
        assert not r["valido"] and r["errore"]

    def test_errore_hub_costante(self):
        pa, _ = serie_rumorosa()
        pb = pd.Series(45.0, index=pa.index)
        r = calcola_copertura_proxy(pa, pb, 40.0)
        assert not r["valido"] and "hub" in r["errore"].lower()

    def test_errore_swissix_costante(self):
        _, pb = serie_rumorosa()
        pa = pd.Series(50.0, index=pb.index)
        r = calcola_copertura_proxy(pa, pb, 40.0)
        assert not r["valido"] and r["errore"]

    def test_errore_parametri(self):
        pa, pb, _ = serie_esatta()
        for bad_fwd in (float("nan"), float("inf"), "x", None, True):
            r = calcola_copertura_proxy(pa, pb, bad_fwd)
            assert not r["valido"], bad_fwd
        for bad_mw in (0.0, -3.0, float("nan"), "x", True):
            r = calcola_copertura_proxy(pa, pb, 30.0, mw=bad_mw)
            assert not r["valido"], bad_mw

    def test_nan_safe(self):
        idx = pd.date_range("2026-01-01", periods=48, freq="h")
        ore = np.arange(48, dtype=float)
        pa = pd.Series(50.0 + 10.0 * np.sin(2 * np.pi * ore / 24.0), index=idx)
        pb = pd.Series(0.5 * pa.to_numpy() + 10.0, index=idx)
        pa.iloc[3] = float("nan")
        pb.iloc[40] = float("nan")
        r = calcola_copertura_proxy(pa, pb, 30.0)
        assert r["valido"] and r["n_ore"] == 46

    def test_allineamento_indici_diversi(self):
        idx = pd.date_range("2026-01-01", periods=48, freq="h")
        ore = np.arange(48, dtype=float)
        pa = pd.Series(50.0 + 10.0 * np.sin(2 * np.pi * ore / 24.0), index=idx)
        pb = pd.Series(0.5 * pa.to_numpy() + 10.0, index=idx)
        pb2 = pb.copy()
        pb2.index = pb2.index + pd.Timedelta(hours=6)  # shift: overlap parziale
        r = calcola_copertura_proxy(pa, pb2, 30.0)
        assert r["valido"] and r["n_ore"] == 42
        assert np.isfinite(r["h_star"])

    def test_determinismo(self):
        pa, pb = serie_rumorosa()
        r1 = calcola_copertura_proxy(pa, pb, 65.0)
        r2 = calcola_copertura_proxy(pa, pb, 65.0)
        assert r1["h_star"] == r2["h_star"]
        assert r1["r2"] == r2["r2"]
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["df_h"].equals(r2["df_h"])

    def test_verdetto_coerente(self):
        pa, pb, _ = serie_esatta()  # R^2 = 1 -> MOLTO EFFICACE
        r = calcola_copertura_proxy(pa, pb, 30.0)
        assert "MOLTO EFFICACE" in r["verdetto"]
        assert "h* = 2.000" in r["verdetto"]


class TestRegistry:
    def test_tab195_dichiarata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "calcola_copertura_proxy" in src
        assert '"🛡️ Copertura proxy"' in src
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab195" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert "tab195" in withs
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(withs) == len(dvars) == 366
        keys = re.findall(r'key="(pxb195_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 5
