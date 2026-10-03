"""Test calcola_causalita_granger - tab173 (stile pytest, via appfuncs).

Copertura: gas che trascina il power -> GAS->POWER; due random walk
indipendenti -> NESSUNA; feedback bidirezionale -> FEEDBACK; relazione esatta
-> F=inf, p-value 0; livelli vs differenze; casi di errore (serie vuota/corta/
costante/non numerica/indice non datetime/parametri invalidi); NaN/tz-aware/
duplicati; determinismo; replicazione indipendente della statistica F con
codice scritto a parte; registry tab173.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_causalita_granger")
gng = fns["calcola_causalita_granger"]

APP = Path(__file__).resolve().parent.parent / "app.py"


def serie_giorni(valori, start="2024-01-01"):
    idx = pd.date_range(start, periods=len(valori), freq="D")
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


def coppia_gas_trascina(n=400, seed=7):
    """Gas random walk; power con dp_t = 1.2*dgas_{t-1} + rumore."""
    rng = np.random.default_rng(seed)
    eg = rng.standard_normal(n)
    gas = 40.0 + np.cumsum(eg)
    dgas = np.diff(gas, prepend=gas[0])
    dp = np.empty(n)
    dp[0] = 0.0
    dp[1:] = 1.2 * dgas[:-1] + 0.5 * rng.standard_normal(n - 1)
    power = 60.0 + np.cumsum(dp)
    return serie_giorni(gas), serie_giorni(power)


def coppia_indipendenti(n=400, seed=11):
    rng = np.random.default_rng(seed)
    gas = serie_giorni(40.0 + np.cumsum(rng.standard_normal(n)))
    power = serie_giorni(60.0 + np.cumsum(rng.standard_normal(n)))
    return gas, power


def coppia_feedback(n=400, seed=21):
    """dp_t = 0.8*dgas_{t-1} + e; dgas_t = 0.6*dp_{t-1} + u."""
    rng = np.random.default_rng(seed)
    dp = np.zeros(n)
    dgas = np.zeros(n)
    for t in range(1, n):
        dp[t] = 0.8 * dgas[t - 1] + 0.5 * rng.standard_normal()
        dgas[t] = 0.6 * dp[t - 1] + 0.5 * rng.standard_normal()
    return serie_giorni(40.0 + np.cumsum(dgas)), serie_giorni(60.0 + np.cumsum(dp))


# ------------------------------------------------- casi con segnale noto
class TestSegnale:
    def test_gas_trascina_power(self):
        gas, power = coppia_gas_trascina()
        r = gng(power, gas, differenzia=True)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "GAS->POWER"
        assert r["sig_gp"] is True
        assert r["sig_pg"] is False
        assert r["pval_gp"] < 0.05 <= r["pval_pg"]
        assert r["f_gp"] > r["crit_5"]

    def test_indipendenti_nessuna(self):
        gas, power = coppia_indipendenti()
        r = gng(power, gas, differenzia=True)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "NESSUNA"
        assert r["sig_gp"] is False and r["sig_pg"] is False

    def test_feedback(self):
        gas, power = coppia_feedback()
        r = gng(power, gas, differenzia=True)
        assert r["valido"], r["errore"]
        assert r["verdetto"] == "FEEDBACK"
        assert r["sig_gp"] is True and r["sig_pg"] is True

    def test_relazione_esatta(self):
        rng = np.random.default_rng(31)
        n = 200
        gas = serie_giorni(40.0 + np.cumsum(rng.standard_normal(n)))
        gv = gas.to_numpy()
        power = serie_giorni(3.0 + 2.0 * np.roll(gv, 1))
        power.iloc[0] = 3.0 + 2.0 * gv[0]
        r = gng(power, gas, differenzia=True, lags=2)
        assert r["valido"], r["errore"]
        assert r["sig_gp"] is True
        assert r["f_gp"] == float("inf")
        assert r["pval_gp"] == 0.0

    def test_livelli_ok(self):
        gas, power = coppia_gas_trascina()
        r = gng(power, gas, differenzia=False)
        assert r["valido"], r["errore"]
        assert r["n_giorni"] == 400

    def test_lag_fisso_rispettato(self):
        gas, power = coppia_gas_trascina()
        r = gng(power, gas, differenzia=True, lags=3)
        assert r["valido"], r["errore"]
        assert r["lags"] == 3
        assert r["lags_auto"] is False
        assert len(r["df_coef"]) == 6  # 2 direzioni x 3 lag

    def test_strutture(self):
        gas, power = coppia_gas_trascina()
        r = gng(power, gas, differenzia=True)
        det = r["df_dettaglio"]
        assert list(det.columns) == ["Direzione", "F", "p-value", "Lag",
                                     "Gdl residui", "Critica 5%",
                                     "Significativa (5%)"]
        assert len(det) == 2
        assert set(det["Direzione"]) == {"Gas → Power", "Power → Gas"}
        coef = r["df_coef"]
        assert list(coef.columns) == ["Direzione", "Lag", "Coeff. propri",
                                      "Coeff. incrociati"]
        assert (coef["Lag"] <= r["lags"]).all()
        assert r["n_scartate"] == 0
        assert "GAS->POWER" in r["giudizio"]


# ------------------------------------------------- replicazione indipendente
class TestReplicaIndipendente:
    def test_f_gas_power_a_mano(self):
        """F calcolata qui con codice scritto a parte == f_gp dell'helper."""
        gas, power = coppia_gas_trascina(n=120, seed=7)
        r = gng(power, gas, differenzia=True, lags=2)
        assert r["valido"], r["errore"]
        dg = pd.DataFrame({"gas": gas, "power": power}).diff().dropna()
        xv = dg["gas"].to_numpy()
        yv = dg["power"].to_numpy()
        T, pl = len(dg), 2
        n = T - pl
        Y = yv[pl:]
        Xu = np.column_stack(
            [np.ones(n)]
            + [yv[pl - i: T - i] for i in range(1, pl + 1)]
            + [xv[pl - i: T - i] for i in range(1, pl + 1)])
        Xr = Xu[:, :pl + 1]
        bu, _, _, _ = np.linalg.lstsq(Xu, Y, rcond=None)
        br, _, _, _ = np.linalg.lstsq(Xr, Y, rcond=None)
        rss_u = float((Y - Xu @ bu) @ (Y - Xu @ bu))
        rss_r = float((Y - Xr @ br) @ (Y - Xr @ br))
        f_mano = ((rss_r - rss_u) / pl) / (rss_u / (n - 2 * pl - 1))
        assert r["f_gp"] == pytest.approx(f_mano, rel=1e-9)
        assert r["lags"] == 2


# ------------------------------------------------- robustezza input
class TestRobustezza:
    def test_nan_scartati(self):
        gas, power = coppia_gas_trascina()
        gas.iloc[10] = np.nan
        power.iloc[20] = np.nan
        r = gng(power, gas, differenzia=True)
        assert r["valido"], r["errore"]
        assert r["n_scartate"] >= 2

    def test_tz_aware(self):
        gas, power = coppia_gas_trascina()
        gas.index = gas.index.tz_localize("Europe/Zurich")
        power.index = power.index.tz_localize("Europe/Zurich")
        r = gng(power, gas, differenzia=True)
        assert r["valido"], r["errore"]

    def test_duplicati(self):
        gas, power = coppia_gas_trascina()
        gas = pd.concat([gas, gas.iloc[[0]]])
        power = pd.concat([power, power.iloc[[0]]])
        r = gng(power, gas, differenzia=True)
        assert r["valido"], r["errore"]

    def test_determinismo(self):
        gas, power = coppia_gas_trascina()
        r1 = gng(power, gas, differenzia=True)
        r2 = gng(power, gas, differenzia=True)
        assert r1["f_gp"] == r2["f_gp"]
        assert r1["pval_pg"] == r2["pval_pg"]
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["lags"] == r2["lags"]


# ------------------------------------------------- casi di errore
class TestErrori:
    def test_serie_vuota(self):
        v = pd.Series(dtype=float, index=pd.DatetimeIndex([]))
        r = gng(v, v)
        assert not r["valido"] and r["errore"]

    def test_none(self):
        gas, _ = coppia_gas_trascina()
        r = gng(None, gas)
        assert not r["valido"] and r["errore"]

    def test_troppo_corta(self):
        gas, power = coppia_gas_trascina(n=40)
        r = gng(power, gas, differenzia=True)
        assert not r["valido"] and r["errore"]

    def test_gas_costante(self):
        _, power = coppia_gas_trascina()
        gas = serie_giorni(np.full(400, 40.0))
        r = gng(power, gas, differenzia=True)
        assert not r["valido"] and "costante" in r["errore"]

    def test_power_costante(self):
        gas, _ = coppia_gas_trascina()
        power = serie_giorni(np.full(400, 60.0))
        r = gng(power, gas, differenzia=True)
        assert not r["valido"] and "costante" in r["errore"]

    def test_non_numerica(self):
        gas, power = coppia_gas_trascina()
        idx = pd.date_range("2024-01-01", periods=400, freq="D")
        r = gng(power, pd.Series(["x"] * 400, index=idx))
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        gas, power = coppia_gas_trascina()
        r = gng(pd.Series(power.to_numpy()), pd.Series(gas.to_numpy()))
        assert not r["valido"] and r["errore"]

    def test_lags_invalidi(self):
        gas, power = coppia_gas_trascina()
        for bad in (0, -2, "x", 1.5):
            r = gng(power, gas, lags=bad)
            assert not r["valido"] and r["errore"], bad

    def test_lags_troppo_alto(self):
        gas, power = coppia_gas_trascina(n=120)
        r = gng(power, gas, differenzia=True, lags=50)
        assert not r["valido"] and r["errore"]

    def test_min_giorni_invalido(self):
        gas, power = coppia_gas_trascina()
        for bad in (10, "x", None):
            r = gng(power, gas, min_giorni=bad)
            assert not r["valido"] and r["errore"], bad


# ------------------------------------------------- registry tab173
class TestRegistry:
    def test_tab173_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        tree = __import__("ast").parse(src)
        nomi, titoli = [], []
        for node in __import__("ast").walk(tree):
            if (isinstance(node, __import__("ast").Assign)
                    and isinstance(node.value, __import__("ast").Call)):
                func = node.value.func
                if (isinstance(func, __import__("ast").Attribute)
                        and func.attr == "tabs"):
                    nomi = [t.id for t in node.targets[0].elts]
                    titoli = [e.value for e in node.value.args[0].elts]
        assert "tab173" in nomi
        assert "🔀 Causalità di Granger" in titoli
        assert nomi.index("tab173") == titoli.index("🔀 Causalità di Granger")
        # sequenza senza buchi: tab1..tab173 tutte presenti
        attesi = {f"tab{i}" for i in range(1, 174)}
        assert attesi <= set(nomi), attesi - set(nomi)
        assert len(titoli) == len(nomi)

    def test_helper_a_livello_modulo(self):
        src = APP.read_text(encoding="utf-8")
        tree = __import__("ast").parse(src)
        fns = [n.name for n in tree.body
               if isinstance(n, __import__("ast").FunctionDef)]
        assert "calcola_causalita_granger" in fns

    def test_chiavi_widget_uniche(self):
        src = APP.read_text(encoding="utf-8")
        chiavi = re.findall(r'key="(gr173_[^"]+)"', src)
        assert len(chiavi) >= 5
        assert len(set(chiavi)) == len(chiavi)
        tutte = re.findall(r'key="([^"]+)"', src)
        assert len(set(tutte)) == len(tutte), "chiave widget duplicata in app.py"
