"""Test tab197 (stile pytest): KPI di performance risk-adjusted.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_kpi_performance", "calcola_pnl_posizione_aperta")
calcola_kpi_performance = _F["calcola_kpi_performance"]
calcola_pnl_posizione_aperta = _F["calcola_pnl_posizione_aperta"]

TZ = "Europe/Zurich"


def serie_5():
    return pd.Series([100., -50., 200., -100., 50.],
                     index=pd.date_range("2026-01-01", periods=5, freq="D",
                                         tz=TZ))


# ------------------------------------------------------- numeri a mano
class TestNumeriAMano:
    def test_caso_5_periodi(self):
        r = calcola_kpi_performance(serie_5())
        assert r["errore"] is None and r["valido"]
        assert r["n_periodi"] == 5
        assert r["pnl_totale_eur"] == pytest.approx(200.0)
        assert r["rend_medio_periodo_eur"] == pytest.approx(40.0)
        assert r["win_rate_pct"] == pytest.approx(60.0)
        # profit factor = 350 / 150
        assert r["profit_factor"] == pytest.approx(350.0 / 150.0)
        # equity: 100,50,250,150,200 -> dd: 0,-50,0,-100,-50
        assert r["max_drawdown_eur"] == pytest.approx(-100.0)
        assert r["calmar"] == pytest.approx(40.0 * 365 / 100.0)
        exc = np.array([100., -50., 200., -100., 50.])
        assert r["sharpe"] == pytest.approx(
            exc.mean() / exc.std(ddof=1) * np.sqrt(365))
        dd_dev = np.sqrt((np.minimum(exc, 0.0) ** 2).mean())
        assert r["sortino"] == pytest.approx(
            exc.mean() / dd_dev * np.sqrt(365))
        assert r["best_periodo_eur"] == pytest.approx(200.0)
        assert r["worst_periodo_eur"] == pytest.approx(-100.0)
        assert len(r["equity"]) == 5
        assert (r["drawdown"] <= 0).all()
        assert "ECCELLENTE" in r["verdetto"]

    def test_df_mensile(self):
        r = calcola_kpi_performance(serie_5())
        df = r["df_mensile"]
        assert list(df.columns)[:2] == ["Anno", "M01"]
        assert len(df.columns) == 13
        assert df.loc[0, "Anno"] == 2026
        assert df.loc[0, "M01"] == pytest.approx(200.0)
        assert df.loc[0, "M02"] == pytest.approx(0.0)


# ------------------------------------------------------- casi limite
class TestCasiLimite:
    def test_piatta_ratio_none(self):
        r = calcola_kpi_performance(pd.Series([100.] * 10))
        assert r["valido"]
        assert r["sharpe"] is None
        assert r["sortino"] is None
        assert r["calmar"] is None          # drawdown nullo
        assert r["profit_factor"] is None   # mai perdite
        assert r["max_drawdown_eur"] == pytest.approx(0.0)
        assert r["win_rate_pct"] == pytest.approx(100.0)
        assert r["pnl_totale_eur"] == pytest.approx(1000.0)
        assert "N.D." in r["verdetto"]

    def test_solo_perdite(self):
        r = calcola_kpi_performance(pd.Series([-10., -20., -30., -5.]))
        assert r["valido"]
        assert r["profit_factor"] is None   # mai profitti
        assert r["win_rate_pct"] == pytest.approx(0.0)
        assert r["sharpe"] < 0
        assert "NEGATIVO" in r["verdetto"]

    def test_sortino_none_mai_sotto_rf(self):
        r = calcola_kpi_performance(pd.Series([50., 60., 70.]),
                                    periodi_anno=365, tasso_free_pct=0.0)
        assert r["valido"]
        assert r["sortino"] is None
        assert r["sharpe"] is not None

    def test_risk_free_sottratto(self):
        s = pd.Series([101., 99.])
        a = calcola_kpi_performance(s, periodi_anno=365, tasso_free_pct=0.0)
        b = calcola_kpi_performance(s, periodi_anno=365, tasso_free_pct=36.5)
        assert a["valido"] and b["valido"]
        assert b["sharpe"] < a["sharpe"]  # rf_p = 0.001 sottratto alla media
        exc = np.array([101. - 0.001, 99. - 0.001])
        assert b["sharpe"] == pytest.approx(
            exc.mean() / exc.std(ddof=1) * np.sqrt(365))

    def test_df_mensile_vuoto_senza_date(self):
        r = calcola_kpi_performance(pd.Series([10., -5., 8., -3.]))
        assert r["valido"]
        assert len(r["df_mensile"]) == 0
        assert r["best_data"] is None and r["worst_data"] is None

    def test_npa_252(self):
        r = calcola_kpi_performance(serie_5(), periodi_anno=252)
        assert r["valido"]
        exc = np.array([100., -50., 200., -100., 50.])
        assert r["sharpe"] == pytest.approx(
            exc.mean() / exc.std(ddof=1) * np.sqrt(252))


# ------------------------------------------------------- errori
class TestErrori:
    def test_serie_vuota(self):
        r = calcola_kpi_performance(pd.Series(dtype=float))
        assert not r["valido"] and r["errore"]

    def test_non_numerica(self):
        r = calcola_kpi_performance(pd.Series(["a", "b", "c"]))
        assert not r["valido"] and r["errore"]

    def test_inf(self):
        r = calcola_kpi_performance(pd.Series([1.0, np.inf, 2.0]))
        assert not r["valido"] and r["errore"]

    def test_un_solo_punto(self):
        r = calcola_kpi_performance(pd.Series([5.0]))
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("npa", [True, 0, 11, 367, 365.5, "x", None])
    def test_periodi_anno_invalidi(self, npa):
        r = calcola_kpi_performance(serie_5(), periodi_anno=npa)
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("trf", [True, float("nan"), -1.0, 51.0, "x"])
    def test_risk_free_invalido(self, trf):
        r = calcola_kpi_performance(serie_5(), tasso_free_pct=trf)
        assert not r["valido"] and r["errore"]

    def test_nan_come_serie(self):
        r = calcola_kpi_performance(pd.Series([np.nan, np.nan]))
        assert not r["valido"] and r["errore"]


# ------------------------------------------------------- determinismo
class TestDeterminismo:
    def test_due_chiamate_uguali(self):
        a = calcola_kpi_performance(serie_5())
        b = calcola_kpi_performance(serie_5())
        for k in ("sharpe", "sortino", "calmar", "win_rate_pct",
                  "profit_factor", "max_drawdown_eur", "pnl_totale_eur",
                  "rend_annuo_eur", "vol_annua_eur"):
            assert a[k] == b[k]
        assert a["verdetto"] == b["verdetto"]
        assert a["equity"].equals(b["equity"])
        assert a["df_mensile"].equals(b["df_mensile"])


# ------------------------------------------------------- integrazione
class TestIntegrazione:
    def test_da_pnl_posizione_aperta(self):
        idx = pd.date_range("2026-09-01", periods=10 * 24, freq="h", tz=TZ)
        rng = np.random.default_rng(7)
        prezzi = pd.Series(80 + 20 * np.sin(2 * np.pi * idx.hour / 24)
                           + rng.normal(0, 3, len(idx)), index=idx)
        pnl = calcola_pnl_posizione_aperta(prezzi, 2.0, 100.0,
                                           ruolo="acquisto")
        assert pnl["valido"]
        r = calcola_kpi_performance(pnl["serie_giornaliera"])
        assert r["valido"] and r["errore"] is None
        assert r["n_periodi"] == 10
        assert r["pnl_totale_eur"] == pytest.approx(pnl["pnl_totale"])


# ------------------------------------------------------- registry
class TestRegistryTab197:
    def test_tab197_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 219
        assert titoli[-1] == "🚨 Anomalie di carico"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab197" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab197" in withs
        assert len(withs) == len(dvars) == 219
        keys = re.findall(r'key="(kpi197_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 7
