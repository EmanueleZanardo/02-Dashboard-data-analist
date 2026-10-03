"""Test calcola_anticipazione_gas - tab174 (stile pytest, via appfuncs).

Copertura: gas che anticipa il power di 3 giorni -> GAS_ANTICIPA con
lag_star=3 e beta pass-through ~1.5; due random walk indipendenti ->
NESSUNA; power che anticipa il gas -> POWER_ANTICIPA; movimento
contestuale -> CONTESTUALI; casi di errore (serie vuota/corta/costante/
non numerica/indice non datetime/parametri invalidi); NaN/tz-aware/
duplicati; determinismo; replicazione indipendente della CCF con codice
scritto a parte; registry tab174 (n titoli = n variabili, sequenza senza
buchi, tab174 dichiarata e con blocco UI).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_anticipazione_gas")
ag = fns["calcola_anticipazione_gas"]

APP = Path(__file__).resolve().parent.parent / "app.py"


def serie_giorni(valori, start="2024-01-01"):
    idx = pd.date_range(start, periods=len(valori), freq="D")
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


def coppia_gas_anticipa(n=400, seed=7, lag=3, beta=1.5):
    """Gas random walk; power con dp_t = beta*dgas_{t-lag} + rumore."""
    rng = np.random.default_rng(seed)
    gas = 40.0 + np.cumsum(rng.standard_normal(n))
    dgas = np.diff(gas, prepend=gas[0])
    dp = np.zeros(n)
    dp[lag:] = beta * dgas[:-lag] + 0.4 * rng.standard_normal(n - lag)
    power = 60.0 + np.cumsum(dp)
    return serie_giorni(gas), serie_giorni(power)


def coppia_indipendenti(n=400, seed=12):
    rng = np.random.default_rng(seed)
    gas = serie_giorni(40.0 + np.cumsum(rng.standard_normal(n)))
    power = serie_giorni(60.0 + np.cumsum(rng.standard_normal(n)))
    return gas, power


def coppia_power_anticipa(n=400, seed=21, lag=2):
    """Power random walk; gas con dgas_t = 1.2*dp_{t-lag} + rumore."""
    rng = np.random.default_rng(seed)
    power = 60.0 + np.cumsum(rng.standard_normal(n))
    dp = np.diff(power, prepend=power[0])
    dgas = np.zeros(n)
    dgas[lag:] = 1.2 * dp[:-lag] + 0.4 * rng.standard_normal(n - lag)
    gas = 40.0 + np.cumsum(dgas)
    return serie_giorni(gas), serie_giorni(power)


def coppia_contestuale(n=400, seed=31, beta=1.5):
    rng = np.random.default_rng(seed)
    gas = 40.0 + np.cumsum(rng.standard_normal(n))
    dgas = np.diff(gas, prepend=gas[0])
    power = 60.0 + np.cumsum(beta * dgas + 0.4 * rng.standard_normal(n))
    return serie_giorni(gas), serie_giorni(power)


# ------------------------------------------------- casi con segnale noto
class TestSegnale:
    def test_gas_anticipa_3_giorni(self):
        gas, power = coppia_gas_anticipa()
        r = ag(power, gas)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "GAS_ANTICIPA"
        assert r["lag_star"] == 3
        assert r["significativo"] is True
        assert r["corr_star"] > 0.5
        assert abs(r["beta_pt"] - 1.5) < 0.35
        assert r["n_giorni"] >= 60

    def test_indipendenti_nessuna(self):
        gas, power = coppia_indipendenti()
        r = ag(power, gas)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "NESSUNA"
        assert r["significativo"] is False

    def test_power_anticipa_gas(self):
        gas, power = coppia_power_anticipa()
        r = ag(power, gas)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "POWER_ANTICIPA"
        assert r["lag_star"] == -2
        assert r["significativo"] is True

    def test_contestuale(self):
        gas, power = coppia_contestuale()
        r = ag(power, gas)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "CONTESTUALI"
        assert r["lag_star"] == 0
        assert r["significativo"] is True

    def test_livelli_non_differenze(self):
        gas, power = coppia_gas_anticipa()
        r = ag(power, gas, differenzia=False)
        assert r["valido"], r["errore"]
        assert r["verdetto"] in ("GAS_ANTICIPA", "CONTESTUALI")


# ------------------------------------------------- replicazione indipendente
class TestReplicazione:
    def test_ccf_replicata(self):
        """CCF per k in {-2,-1,0,1,2} replicata con codice scritto a parte."""
        gas, power = coppia_gas_anticipa()
        r = ag(power, gas, max_lag=2)
        assert r["valido"], r["errore"]
        # replica indipendente: allinea le serie e usa np.corrcoef
        dfp = pd.DataFrame({"gas": gas, "power": power}).dropna().diff().dropna()
        x = dfp["gas"].to_numpy()
        y = dfp["power"].to_numpy()
        n = len(dfp)
        for k in (-2, -1, 0, 1, 2):
            a = x[:n - k] if k >= 0 else x[-k:]
            b = y[k:] if k >= 0 else y[:n + k]
            atteso = float(np.corrcoef(a, b)[0, 1])
            riga = r["df_ccf"][r["df_ccf"]["Lag"] == k].iloc[0]
            assert riga["Correlazione"] == round(atteso, 4)
        # banda 95% replicata
        riga0 = r["df_ccf"][r["df_ccf"]["Lag"] == 0].iloc[0]
        assert abs(riga0["Banda 95%"] - round(1.96 / np.sqrt(n), 4)) < 1e-9


# ------------------------------------------------- casi di errore
class TestErrori:
    def test_serie_vuota(self):
        r = ag(pd.Series(dtype=float), serie_giorni([1.0] * 100))
        assert not r["valido"] and r["errore"]

    def test_serie_corta(self):
        g = serie_giorni(np.arange(40, dtype=float))
        r = ag(g, g)
        assert not r["valido"] and "insufficienti" in r["errore"]

    def test_serie_costante_gas(self):
        p = serie_giorni(60.0 + np.cumsum(np.random.default_rng(1).standard_normal(200)))
        g = serie_giorni(np.full(200, 38.5))
        r = ag(p, g)
        assert not r["valido"] and "costante" in r["errore"]

    def test_serie_non_numerica(self):
        g = pd.Series(["a"] * 200, index=pd.date_range("2024-01-01", periods=200, freq="D"))
        r = ag(g, g)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        g = pd.Series(np.arange(200, dtype=float))
        r = ag(g, g)
        assert not r["valido"] and "data/ora" in r["errore"]

    def test_none(self):
        r = ag(None, None)
        assert not r["valido"] and r["errore"]

    def test_max_lag_invalido(self):
        gas, power = coppia_indipendenti()
        for bad in (0, -3, "x", 1.5):
            r = ag(power, gas, max_lag=bad)
            assert not r["valido"] and r["errore"], bad

    def test_min_giorni_invalido(self):
        gas, power = coppia_indipendenti()
        for bad in (10, "x"):
            r = ag(power, gas, min_giorni=bad)
            assert not r["valido"] and r["errore"], bad


# ------------------------------------------------- robustezza input
class TestRobustezza:
    def test_nan_e_duplicati(self):
        gas, power = coppia_gas_anticipa()
        gv = gas.copy()
        gv.iloc[10] = np.nan
        gv = pd.concat([gv, gv.iloc[[50]]])  # duplicato
        r = ag(power, gv)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "GAS_ANTICIPA"
        assert r["n_scartate"] >= 1

    def test_tz_aware(self):
        gas, power = coppia_gas_anticipa()
        gtz = gas.copy()
        gtz.index = gtz.index.tz_localize("Europe/Zurich")
        r = ag(power, gtz)
        assert r["valido"], r["errore"]
        assert r["lag_star"] == 3

    def test_determinismo(self):
        gas, power = coppia_gas_anticipa()
        r1 = ag(power, gas)
        r2 = ag(power, gas)
        assert r1["lag_star"] == r2["lag_star"]
        assert r1["corr_star"] == r2["corr_star"]
        assert r1["df_ccf"].equals(r2["df_ccf"])


# ------------------------------------------------- registry tab174
class TestRegistry:
    def test_tab174_registrata(self):
        txt = APP.read_text(encoding="utf-8")
        m = re.search(r"((?:tab\d+,\s*)+tab\d+)\s*=\s*st\.tabs\(\[(.*?)\]\)", txt, re.S)
        assert m, "dichiarazione st.tabs non trovata"
        variabili = re.findall(r"tab(\d+)", m.group(1))
        titoli = re.findall(r'"([^"]+)"', m.group(2))
        nums = sorted(int(v) for v in variabili)
        assert nums == list(range(1, 175)), f"sequenza tab con buchi: {nums[-5:]}"
        assert len(titoli) == 174, f"titoli={len(titoli)}"
        assert any("Anticipo gas" in t for t in titoli)
        assert "with tab174:" in txt
        assert "def calcola_anticipazione_gas" in txt
