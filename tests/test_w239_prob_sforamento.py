"""Test tab239: Probabilita' sforamento budget.

Le funzioni di calcolo sono pure (niente Streamlit): estratte da app.py via
AST con tests/appfuncs.py, come gli altri test pytest del repo.
"""

import re
from pathlib import Path

import numpy as np

from appfuncs import load

_F = load("w239_simulate_annual_cost", "w239_breach_prob", "w239_expected_cost",
          "w239_safety_budget", "w239_var_cost", "w239_csv_simulazioni")
w239_simulate_annual_cost = _F["w239_simulate_annual_cost"]
w239_breach_prob = _F["w239_breach_prob"]
w239_expected_cost = _F["w239_expected_cost"]
w239_safety_budget = _F["w239_safety_budget"]
w239_var_cost = _F["w239_var_cost"]
w239_csv_simulazioni = _F["w239_csv_simulazioni"]


class TestW239PureFunctions:
    def test_simulate_shape_e_seed_deterministico(self):
        mc = [10000.0] * 12
        a = w239_simulate_annual_cost(mc, n_sim=5000, vol=0.10, seed=0)
        b = w239_simulate_annual_cost(mc, n_sim=5000, vol=0.10, seed=0)
        assert a.shape == (5000,)
        np.testing.assert_array_equal(a, b)
        assert np.all(np.isfinite(a)) and np.all(a >= 0.0)

    def test_breach_prob_estremi(self):
        sims = np.array([1.0, 2.0, 3.0, 4.0])
        assert w239_breach_prob(sims, 0.0) == 1.0
        assert w239_breach_prob(sims, 4.0) == 0.0
        assert w239_breach_prob(sims, 2.0) == 0.5

    def test_expected_cost(self):
        assert w239_expected_cost([10.0, 20.0, 30.0]) == 20.0

    def test_safety_budget_e_var_quantile(self):
        sims = np.arange(1.0, 101.0)
        assert w239_safety_budget(sims, 0.95) == np.quantile(sims, 0.95)
        assert w239_var_cost(sims, 0.95) == w239_safety_budget(sims, 0.95)
        assert w239_safety_budget(sims, 0.99) >= w239_safety_budget(sims, 0.95)

    def test_vol_zero_media_corretta(self):
        mc = [1000.0] * 12
        sims = w239_simulate_annual_cost(mc, n_sim=20000, vol=0.0, seed=1)
        assert abs(float(sims.mean()) - 12000.0) < 50.0

    def test_csv_simulazioni(self):
        out = w239_csv_simulazioni([100.5, 200.0])
        righe = out.strip().split("\n")
        assert righe[0] == "simulazione,costo_annuo_eur"
        assert len(righe) == 3
        assert righe[1] == "1,100.50"
        assert righe[2] == "2,200.00"


class TestRegistryTab239:
    def test_tab239_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        # NOTA: il conteggio assoluto (240 nel task originale) non e' affidabile
        # perche' altri worker aggiungono tab in parallelo: si verifica la
        # coerenza titoli/variabili/blocchi e la presenza di tab239.
        assert len(titoli) == len(dvars) == len(withs)
        assert "📊 Probabilità sforamento budget" in titoli
        assert "tab239" in dvars
        assert "tab239" in withs
        keys = re.findall(r'key="(t239_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10
