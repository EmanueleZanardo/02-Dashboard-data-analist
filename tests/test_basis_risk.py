"""Test tab199 (stile pytest): Basis risk locale vs hub.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_basis_risk", "genera_demo_basis")
calcola_basis_risk = _F["calcola_basis_risk"]
genera_demo_basis = _F["genera_demo_basis"]


def _df_alternato(n=61):
    idx = pd.date_range("2026-01-01", periods=n, freq="D")
    hub = [100.0] * n
    loc = [100.0 if i % 2 == 0 else 110.0 for i in range(n)]
    return pd.DataFrame({"Hub": hub, "Loc": loc}, index=idx)


class TestBasisRiskBase:
    def test_numeri_a_mano(self):
        # basis alterna 0/10 su 61 gg (31 zeri, 30 dieci): media 300/61,
        # variazioni basis alternate +-10 -> VaR99 = 10
        df = _df_alternato()
        r = calcola_basis_risk(df, "Hub", "Loc")
        assert r["errore"] is None and r["valido"]
        assert r["basis_media"] == pytest.approx(300.0 / 61.0)
        assert r["basis_min"] == 0.0 and r["basis_max"] == 10.0
        assert r["var_basis_mwh"] == pytest.approx(10.0)
        assert r["n_giorni"] == 61
        # hub fermo -> varianza tutta dal basis
        assert r["quota_basis_var"] == pytest.approx(1.0)
        # 5 critiche tutte a basis 10
        assert (r["df_critiche"]["Basis (€/MWh)"] == 10.0).all()
        assert r["verdetto"].startswith("MODERATO")

    def test_basis_costante_nullo(self):
        df = pd.DataFrame({"Hub": [90.0] * 40, "Loc": [95.0] * 40},
                          index=pd.date_range("2026-01-01", periods=40, freq="D"))
        r = calcola_basis_risk(df, "Hub", "Loc")
        assert r["errore"] is None
        assert r["verdetto"].startswith("NULLO")
        assert r["var_basis_mwh"] == 0.0
        assert r["n_spike"] == 0

    def test_volume_in_euro(self):
        df = _df_alternato()
        r = calcola_basis_risk(df, "Hub", "Loc", volume_mwh_giorno=24.0)
        assert r["var_eur_giorno"] == pytest.approx(240.0)

    def test_demo_deterministica(self):
        d1, d2 = genera_demo_basis(), genera_demo_basis()
        assert d1.equals(d2)
        assert list(d1.columns) == ["Hub (€/MWh)", "Locale (€/MWh)"]
        assert len(d1) == 372
        r = calcola_basis_risk(d1, "Hub (€/MWh)", "Locale (€/MWh)")
        assert r["errore"] is None and r["valido"]
        assert r["n_spike"] > 0

    def test_nan_droppati(self):
        df = _df_alternato()
        df.iloc[0, 0] = np.nan
        df.iloc[1, 1] = np.nan
        r = calcola_basis_risk(df, "Hub", "Loc")
        assert r["errore"] is None and r["n_giorni"] == 59


class TestBasisRiskErrori:
    def test_df_vuoto(self):
        assert calcola_basis_risk(pd.DataFrame(), "a", "b")["errore"]

    def test_non_dataframe(self):
        assert calcola_basis_risk([1, 2, 3], "a", "b")["errore"]

    def test_colonna_mancante(self):
        df = _df_alternato()
        assert calcola_basis_risk(df, "Hub", "X")["errore"]
        assert calcola_basis_risk(df, "X", "Loc")["errore"]

    def test_stessa_colonna(self):
        assert calcola_basis_risk(_df_alternato(), "Hub", "Hub")["errore"]

    def test_pochi_dati(self):
        assert calcola_basis_risk(_df_alternato(10), "Hub", "Loc")["errore"]

    def test_confidenza_fuori_range(self):
        df = _df_alternato()
        assert calcola_basis_risk(df, "Hub", "Loc", confidenza=0.5)["errore"]
        assert calcola_basis_risk(df, "Hub", "Loc", confidenza=1.0)["errore"]

    def test_soglia_fuori_range(self):
        df = _df_alternato()
        assert calcola_basis_risk(df, "Hub", "Loc", soglia_spike=0.5)["errore"]

    def test_volume_negativo(self):
        df = _df_alternato()
        assert calcola_basis_risk(df, "Hub", "Loc", volume_mwh_giorno=-1)["errore"]

    def test_colonne_non_numeriche(self):
        df = pd.DataFrame({"Hub": ["x"] * 40, "Loc": ["y"] * 40})
        assert calcola_basis_risk(df, "Hub", "Loc")["errore"]


# ------------------------------------------------------- registry
class TestRegistryTab199:
    def test_tab199_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 372
        assert titoli[-1] == "Monte Carlo: VaR e Expected Shortfall di una posizione power"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab199" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab199" in withs
        assert len(withs) == len(dvars) == 372
        keys = re.findall(r'key="(br199_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 7
