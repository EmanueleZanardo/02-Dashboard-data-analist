"""Test tab200 (stile pytest): Rolling VaR sul costo giornaliero.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_rolling_var", "genera_demo_rolling_risk")
calcola_rolling_var = _F["calcola_rolling_var"]
genera_demo_rolling_risk = _F["genera_demo_rolling_risk"]


def _crescente(n=60):
    return pd.Series(range(1, n + 1),
                     index=pd.date_range("2026-01-01", periods=n, freq="D"))


class TestRollingVarBase:
    def test_numeri_a_mano(self):
        # serie 1..60, finestra 30, conf 0.95:
        # prima finestra 1..30 -> quantile 0.95 = 28.55, ES = media(29,30) = 29.5
        r = calcola_rolling_var(_crescente(), finestra=30, confidenza=0.95)
        assert r["errore"] is None and r["valido"]
        assert r["n_giorni"] == 60
        assert r["serie_var"].iloc[0] == pytest.approx(28.55)
        assert r["serie_es"].iloc[0] == pytest.approx(29.5)
        assert len(r["serie_var"]) == 31  # 60 - 30 + 1
        # trend = (58.55 - 28.55) / 28.55 ~ 1.0508
        assert r["trend"] == pytest.approx(1.0508, rel=1e-3)
        assert r["verdetto"].startswith("RISCHIO IN CRESCITA")
        assert r["var_max"] >= r["var_attuale"] >= r["var_min"]
        assert len(r["df_peggiori"]) == 5

    def test_seria_costante(self):
        s = pd.Series([100.0] * 60,
                      index=pd.date_range("2026-01-01", periods=60, freq="D"))
        r = calcola_rolling_var(s, finestra=30)
        assert r["errore"] is None
        assert r["var_attuale"] == pytest.approx(100.0)
        assert r["es_attuale"] == pytest.approx(100.0)
        assert r["trend"] == pytest.approx(0.0)
        assert r["verdetto"].startswith("SOTTO CONTROLLO")

    def test_decremento_miglioramento(self):
        s = pd.Series(list(range(60, 0, -1)),
                      index=pd.date_range("2026-01-01", periods=60, freq="D"))
        r = calcola_rolling_var(s, finestra=30)
        assert r["errore"] is None
        assert r["trend"] <= -0.20
        assert r["verdetto"].startswith("IN MIGLIORAMENTO")

    def test_soglia_attenzione_e_breach(self):
        s = pd.Series([100.0] * 60,
                      index=pd.date_range("2026-01-01", periods=60, freq="D"))
        r = calcola_rolling_var(s, finestra=30, soglia_eur_giorno=90.0)
        assert r["errore"] is None
        assert r["n_breach"] == 60
        assert r["pct_breach"] == pytest.approx(100.0)
        assert len(r["date_breach"]) == 60
        assert r["verdetto"].startswith("ATTENZIONE")

    def test_demo_deterministica(self):
        d1, d2 = genera_demo_rolling_risk(), genera_demo_rolling_risk()
        assert d1.equals(d2)
        assert d1.name == "Costo (€/giorno)"
        assert len(d1) == 365
        r = calcola_rolling_var(d1)
        assert r["errore"] is None and r["valido"]
        assert r["var_attuale"] < r["es_attuale"]
        assert r["var_max"] >= r["var_media"]

    def test_nan_droppati(self):
        s = _crescente(80).astype(float)
        s.iloc[0] = np.nan
        s.iloc[5] = np.nan
        r = calcola_rolling_var(s, finestra=30)
        assert r["errore"] is None and r["n_giorni"] == 78


class TestRollingVarErrori:
    def test_serie_vuota(self):
        assert calcola_rolling_var(pd.Series(dtype=float), finestra=30)["errore"]

    def test_non_series(self):
        assert calcola_rolling_var([1, 2, 3], finestra=30)["errore"]

    def test_finestra_troppo_piccola(self):
        assert calcola_rolling_var(_crescente(), finestra=20)["errore"]

    def test_finestra_troppo_grande(self):
        assert calcola_rolling_var(_crescente(), finestra=300)["errore"]

    def test_finestra_bool(self):
        assert calcola_rolling_var(_crescente(), finestra=True)["errore"]

    def test_finestra_non_intera(self):
        assert calcola_rolling_var(_crescente(), finestra=90.5)["errore"]

    def test_pochi_dati(self):
        s = _crescente(40)
        assert calcola_rolling_var(s, finestra=30)["errore"]

    def test_confidenza_fuori_range(self):
        assert calcola_rolling_var(_crescente(), finestra=30, confidenza=0.5)["errore"]
        assert calcola_rolling_var(_crescente(), finestra=30, confidenza=1.0)["errore"]

    def test_soglia_negativa(self):
        assert calcola_rolling_var(_crescente(), finestra=30,
                                   soglia_eur_giorno=-1)["errore"]

    def test_tutti_nan(self):
        s = pd.Series([np.nan] * 70,
                      index=pd.date_range("2026-01-01", periods=70, freq="D"))
        assert calcola_rolling_var(s, finestra=30)["errore"]


# ------------------------------------------------------- registry
class TestRegistryTab200:
    def test_tab200_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 266
        assert titoli[-1] == "🌾️ Agrivoltaico: doppio reddito"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab200" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab200" in withs
        assert len(withs) == len(dvars) == 266
        keys = re.findall(r'key="(rv200_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 6
