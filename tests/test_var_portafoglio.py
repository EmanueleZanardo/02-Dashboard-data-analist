"""Test tab198 (stile pytest): VaR di portafoglio multi-commodity.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_var_portafoglio", "genera_demo_var_portafoglio")
calcola_var_portafoglio = _F["calcola_var_portafoglio"]
genera_demo_var_portafoglio = _F["genera_demo_var_portafoglio"]


def _serie_alternata(n_prezzi=102):
    idx = pd.date_range("2026-01-01", periods=n_prezzi, freq="D")
    pw = [100.0 + (10.0 if i % 2 == 0 else 0.0) for i in range(n_prezzi)]
    return pd.DataFrame({"Power": pw, "Gas": [50.0] * n_prezzi}, index=idx)


class TestVarPortafoglioBase:
    def test_numeri_a_mano(self):
        # 101 diff di Power alternate +-10, Gas fermo, pos {Power:1, Gas:2}:
        # pnl = 51x(+10), 50x(-10); quantile(pnl, 0.01) con i=1.0 -> -10.
        df = _serie_alternata()
        r = calcola_var_portafoglio(df, {"Power": 1.0, "Gas": 2.0}, confidenza=0.99)
        assert r["errore"] is None and r["valido"]
        assert r["var_eur"] == pytest.approx(10.0)
        assert r["es_eur"] == pytest.approx(10.0)  # coda: 50 valori a -10
        assert r["n_giorni"] == 101
        # Gas fermo -> componente nulla
        comp = r["componenti"]
        assert comp.loc[comp["Commodity"] == "Gas", "VaR componente (€)"].iloc[0] == 0.0
        # quote sommano a 100
        assert comp["Quota VaR (%)"].sum() == pytest.approx(100.0)

    def test_scaling_orizzonte(self):
        df = _serie_alternata()
        pos = {"Power": 1.0}
        r1 = calcola_var_portafoglio(df, pos, orizzonte_giorni=1)
        r4 = calcola_var_portafoglio(df, pos, orizzonte_giorni=4)
        assert r4["var_eur"] == pytest.approx(2.0 * r1["var_eur"])  # sqrt(4)
        assert r4["es_eur"] == pytest.approx(2.0 * r1["es_eur"])

    def test_es_maggiore_var_e_diversificazione(self):
        demo = genera_demo_var_portafoglio()
        pos = {"Power (€/MWh)": 10.0, "Gas (€/MWh)": -6.0, "CO2 (€/t)": -3.0}
        r = calcola_var_portafoglio(demo, pos, confidenza=0.99)
        assert r["valido"]
        assert r["es_eur"] >= r["var_eur"] - 1e-9
        assert np.isfinite(r["diversificazione_eur"])
        assert r["nozionale_eur"] > 0
        assert 0.0 <= r["var_pct_nozionale"] <= 1.0
        # correlazioni note del demo
        c = r["correlazione"]
        assert c.loc["Power (€/MWh)", "Gas (€/MWh)"] > 0.4
        assert len(r["df_peggiori"]) == 5
        assert (r["df_peggiori"]["P&L simulato (€)"].diff().dropna() >= 0).all()

    def test_pnl_costante_var_nullo(self):
        idx = pd.date_range("2026-01-01", periods=40, freq="D")
        df = pd.DataFrame({"Power": [100.0 + i for i in range(40)],
                           "Gas": [50.0 - 0.5 * i for i in range(40)]}, index=idx)
        r = calcola_var_portafoglio(df, {"Power": 2.0, "Gas": -4.0})
        assert r["valido"] and r["var_eur"] == 0.0
        assert "NULLO" in r["verdetto"]

    def test_prezzi_fermi(self):
        demo = genera_demo_var_portafoglio()
        flat = demo.copy()
        flat.iloc[:, :] = 50.0
        r = calcola_var_portafoglio(flat, {"Power (€/MWh)": 1.0})
        assert r["valido"] and r["var_eur"] == 0.0

    def test_moltiplicatori(self):
        df = _serie_alternata()
        r = calcola_var_portafoglio(df, {"Power": 1.0},
                                    moltiplicatori={"Power": 3.0}, confidenza=0.99)
        assert r["var_eur"] == pytest.approx(30.0)

    def test_demo_deterministico(self):
        a = genera_demo_var_portafoglio()
        b = genera_demo_var_portafoglio()
        assert a.equals(b)
        assert list(a.columns) == ["Power (€/MWh)", "Gas (€/MWh)", "CO2 (€/t)"]
        assert len(a) == 365

    def test_verdetto_tag(self):
        demo = genera_demo_var_portafoglio()
        pos = {"Power (€/MWh)": 10.0, "Gas (€/MWh)": -6.0, "CO2 (€/t)": -3.0}
        r = calcola_var_portafoglio(demo, pos)
        assert any(t in r["verdetto"] for t in ("ELEVATO", "MODERATO", "CONTENUTO", "NULLO"))


class TestVarPortafoglioErrori:
    def _demo(self):
        return genera_demo_var_portafoglio()

    @pytest.mark.parametrize("df,pos,kw,pezzo", [
        (pd.DataFrame(), {"Power": 1}, {}, "DataFrame non vuoto"),
        ("non-df", {"Power": 1}, {}, "DataFrame non vuoto"),
        (None, {"Power": 1}, {}, "DataFrame non vuoto"),
    ])
    def test_df_non_valido(self, df, pos, kw, pezzo):
        r = calcola_var_portafoglio(df, pos, **kw)
        assert r["errore"] and pezzo in r["errore"] and not r["valido"]

    def test_posizioni_vuote(self):
        r = calcola_var_portafoglio(self._demo(), {})
        assert r["errore"] and not r["valido"]

    def test_commodity_ignota(self):
        r = calcola_var_portafoglio(self._demo(), {"XXX": 1.0})
        assert "XXX" in r["errore"]

    def test_qty_zero(self):
        r = calcola_var_portafoglio(self._demo(), {"Power (€/MWh)": 0.0})
        assert r["errore"] and not r["valido"]

    @pytest.mark.parametrize("qty", [True, float("nan"), float("inf"), "x", None])
    def test_qty_non_valide(self, qty):
        r = calcola_var_portafoglio(self._demo(), {"Power (€/MWh)": qty})
        assert r["errore"] and not r["valido"]

    @pytest.mark.parametrize("conf", [0.5, 0.89, 1.0, True, float("nan"), "x"])
    def test_confidenza_non_valida(self, conf):
        r = calcola_var_portafoglio(self._demo(), {"Power (€/MWh)": 1.0},
                                    confidenza=conf)
        assert r["errore"] and not r["valido"]

    @pytest.mark.parametrize("oriz", [0, 31, True, 1.5, "x"])
    def test_orizzonte_non_valido(self, oriz):
        r = calcola_var_portafoglio(self._demo(), {"Power (€/MWh)": 1.0},
                                    orizzonte_giorni=oriz)
        assert r["errore"] and not r["valido"]

    def test_serie_troppo_corta(self):
        r = calcola_var_portafoglio(self._demo().iloc[:10], {"Power (€/MWh)": 1.0})
        assert r["errore"] and not r["valido"]

    def test_moltiplicatore_non_valido(self):
        r = calcola_var_portafoglio(self._demo(), {"Power (€/MWh)": 1.0},
                                    moltiplicatori={"Power (€/MWh)": -2.0})
        assert r["errore"] and not r["valido"]

    def test_colonna_non_numerica(self):
        demo = self._demo()
        demo["Power (€/MWh)"] = "abc"
        r = calcola_var_portafoglio(demo, {"Power (€/MWh)": 1.0})
        assert r["errore"] and not r["valido"]


# ------------------------------------------------------- registry
class TestRegistryTab198:
    def test_tab198_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 309
        assert titoli[-1] == "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab198" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab198" in withs
        assert len(withs) == len(dvars) == 309
        keys = re.findall(r'key="(var198_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 7
