"""Test tab194 (stile pytest): PCA dei profili orari -> fattori di forma.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Modello: giorni completi (24h) -> matrice giorni x 24 -> centratura sulle
medie di colonna -> eigh della covarianza 24x24 -> loadings/scores con
segno fissato per convenzione. Interpretazione: "Livello" se i loadings
sono quasi costanti (CV < 0.5), "Pendenza giorno/notte" se |corr| >= 0.60
con la rampa 0..23, "Curvatura (picchi)" se |corr| >= 0.60 con
(ora-11.5)^2, altrimenti "Forma residua".

Numeri a mano (caso livello: 60 giorni, prezzo = 60 + livello_d +
forma_fissa + rumore):
  forma_fissa = +20 nelle ore 8..19, -10 altrove (non contribuisce alla
  varianza perche' fissa); livello_d ~ N(0, 10^2) -> varianza per ora ~
  100 + 4 (rumore); varianza totale ~ 24 * 104 = 2496; F1 ~ shift
  parallelo con autovalore ~ 24 * 100 = 2400 -> ~96% -> "Livello", k_95=1.
Caso pendenza: prezzo = 60 + spread_d * rampa + rumore(2), spread_d ~
  N(0, 15^2) -> F1 ~ rampa -> "Pendenza giorno/notte", var F1 > 80%.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from appfuncs import load

_F = load("calcola_pca_forma_prezzo")
calcola_pca_forma_prezzo = _F["calcola_pca_forma_prezzo"]


def serie_livello(n_giorni=60, seed=7):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2026-01-01", periods=n_giorni * 24, freq="h")
    ore = idx.hour.to_numpy()
    livello = rng.normal(0.0, 10.0, size=n_giorni)
    forma = np.where((ore >= 8) & (ore < 20), 20.0, -10.0)
    vals = 60.0 + np.repeat(livello, 24) + forma + rng.normal(0.0, 2.0, size=n_giorni * 24)
    return pd.Series(vals, index=idx)


def serie_pendenza(n_giorni=60, seed=11):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2026-01-01", periods=n_giorni * 24, freq="h")
    ore = idx.hour.to_numpy()
    rampa = (ore - 11.5) / 11.5
    spread = rng.normal(0.0, 15.0, size=n_giorni)
    vals = 60.0 + np.repeat(spread, 24) * rampa + rng.normal(0.0, 2.0, size=n_giorni * 24)
    return pd.Series(vals, index=idx)


def serie_curvatura(n_giorni=60, seed=13):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2026-01-01", periods=n_giorni * 24, freq="h")
    ore = idx.hour.to_numpy()
    gobba = (ore - 11.5) ** 2
    gobba = (gobba - gobba.mean()) / gobba.std()
    ampiezza = rng.normal(0.0, 12.0, size=n_giorni)
    vals = 60.0 + np.repeat(ampiezza, 24) * gobba + rng.normal(0.0, 2.0, size=n_giorni * 24)
    return pd.Series(vals, index=idx)


class TestCasiErrore:
    def test_serie_piatta(self):
        idx = pd.date_range("2026-01-01", periods=30 * 24, freq="h")
        r = calcola_pca_forma_prezzo(pd.Series(50.0, index=idx))
        assert not r["valido"]
        assert "varianza" in r["errore"]

    def test_serie_vuota(self):
        r = calcola_pca_forma_prezzo(pd.Series(dtype=float))
        assert not r["valido"]
        assert r["errore"] is not None

    def test_indice_non_datetime(self):
        r = calcola_pca_forma_prezzo(pd.Series([1.0, 2.0, 3.0]))
        assert not r["valido"]
        assert "datetime" in r["errore"]

    def test_parametri_non_validi(self):
        s = serie_livello()
        assert not calcola_pca_forma_prezzo(s, n_fattori=0)["valido"]
        assert not calcola_pca_forma_prezzo(s, n_fattori=25)["valido"]
        assert not calcola_pca_forma_prezzo(s, min_giorni=4)["valido"]
        assert not calcola_pca_forma_prezzo(s, n_fattori="tre")["valido"]

    def test_giorni_insufficienti(self):
        s = serie_livello(n_giorni=10)
        r = calcola_pca_forma_prezzo(s, min_giorni=30)
        assert not r["valido"]
        assert "insufficienti" in r["errore"]
        r2 = calcola_pca_forma_prezzo(s, min_giorni=5)
        assert r2["valido"] and r2["giorni_validi"] == 10


class TestCasoLivello:
    def test_struttura_e_numeri(self):
        r = calcola_pca_forma_prezzo(serie_livello())
        assert r["valido"] and r["errore"] is None
        assert r["giorni_validi"] == 60
        assert r["giorni_scartati"] == 0
        assert r["n_fattori"] == 3
        assert len(r["var_spiegata_pct"]) == 24
        assert sum(r["var_spiegata_pct"]) == pytest.approx(100.0, abs=1e-6)
        # varianza decrescente
        assert all(a >= b for a, b in zip(r["var_spiegata_pct"], r["var_spiegata_pct"][1:]))
        assert r["var_spiegata_pct"][0] > 80.0
        assert r["k_95"] == 1
        assert r["interpretazione"]["Tipo"].iloc[0] == "Livello"
        assert r["df_loadings"].shape == (24, 4)
        assert list(r["df_loadings"].columns) == ["Ora", "Fattore 1", "Fattore 2", "Fattore 3"]
        assert list(r["df_loadings"]["Ora"]) == list(range(24))
        assert r["df_scores"].shape == (60, 4)
        assert len(r["profilo_medio"]) == 24
        assert "95%" in r["verdetto"] and "Livello" in r["verdetto"]

    def test_determinismo(self):
        s = serie_livello()
        r1 = calcola_pca_forma_prezzo(s)
        r2 = calcola_pca_forma_prezzo(s)
        assert_frame_equal(r1["df_loadings"], r2["df_loadings"])
        assert_frame_equal(r1["df_scores"], r2["df_scores"])
        assert r1["interpretazione"]["Tipo"].tolist() == r2["interpretazione"]["Tipo"].tolist()

    def test_n_fattori_custom(self):
        r = calcola_pca_forma_prezzo(serie_livello(), n_fattori=5)
        assert r["valido"] and r["n_fattori"] == 5
        assert r["df_loadings"].shape == (24, 6)


class TestPendenzaECurvatura:
    def test_pendenza(self):
        r = calcola_pca_forma_prezzo(serie_pendenza())
        assert r["valido"]
        assert r["interpretazione"]["Tipo"].iloc[0] == "Pendenza giorno/notte"
        assert r["var_spiegata_pct"][0] > 80.0

    def test_curvatura(self):
        r = calcola_pca_forma_prezzo(serie_curvatura())
        assert r["valido"]
        assert r["interpretazione"]["Tipo"].iloc[0] == "Curvatura (picchi)"
        assert r["var_spiegata_pct"][0] > 80.0


class TestRobustezza:
    def test_giorni_incompleti_scartati(self):
        s = serie_livello()
        # rimuove 4 ore da 3 giorni
        idx = s.index
        drop = []
        for g in [5, 17, 42]:
            base = idx[g * 24]
            drop.extend([base + pd.Timedelta(hours=h) for h in (3, 7, 15, 22)])
        s2 = s.drop(index=drop)
        r = calcola_pca_forma_prezzo(s2)
        assert r["valido"]
        assert r["giorni_scartati"] == 3
        assert r["giorni_validi"] == 57

    def test_nan_non_crashano(self):
        s = serie_livello().copy()
        rng = np.random.default_rng(3)
        pos = rng.choice(len(s), size=20, replace=False)
        s.iloc[pos] = np.nan
        r = calcola_pca_forma_prezzo(s)
        assert r["valido"]
        assert r["giorni_validi"] <= 60

    def test_tz_aware(self):
        s = serie_livello().tz_localize("Europe/Zurich")
        r = calcola_pca_forma_prezzo(s)
        assert r["valido"] and r["giorni_validi"] == 60

    def test_serie_non_ordinata(self):
        s = serie_livello().sample(frac=1.0, random_state=5)
        r = calcola_pca_forma_prezzo(s)
        assert r["valido"] and r["giorni_validi"] == 60


class TestRegistry:
    def test_tab194_dichiarata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "calcola_pca_forma_prezzo" in src
        assert '"🧬 Fattori di forma (PCA)"' in src
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab194" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert "tab194" in withs
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(withs) == len(dvars) == 241
        keys = re.findall(r'key="(pca194_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 4
