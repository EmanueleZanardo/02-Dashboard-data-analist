"""W235 - test funzioni pure + registry per tab235 'Correlazione carico-prezzo'."""
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from appfuncs import load


class TestPureTab235:
    def test_load_price_corr_correlazione_positiva(self):
        f = load("load_price_corr")["load_price_corr"]
        load_kw = np.array([50.0, 60.0, 150.0, 140.0, 55.0, 52.0])
        price = np.array([80.0, 85.0, 250.0, 240.0, 82.0, 81.0])
        r = f(load_kw, price)
        assert r["valido"]
        assert r["r_pearson"] > 0.9
        assert -1.0 <= r["r_spearman"] <= 1.0
        assert r["extra_costo_vs_scorrelato_eur"] > 0
        assert r["ore_top_concomitanti"] >= 1
        assert r["n"] == 6
        assert r["top_n"] == 4

    def test_load_price_corr_correlazione_negativa(self):
        f = load("load_price_corr")["load_price_corr"]
        load_kw = np.array([150.0, 140.0, 50.0, 55.0, 60.0, 52.0])
        price = np.array([80.0, 85.0, 250.0, 240.0, 82.0, 81.0])
        r = f(load_kw, price)
        assert r["valido"]
        assert r["r_pearson"] < -0.5
        assert r["extra_costo_vs_scorrelato_eur"] < 0

    def test_load_price_corr_profilo_piatto(self):
        f = load("load_price_corr")["load_price_corr"]
        load_kw = np.full(6, 100.0)
        price = np.array([80.0, 85.0, 250.0, 240.0, 82.0, 81.0])
        r = f(load_kw, price)
        assert r["valido"]
        assert r["r_pearson"] == 0.0
        assert abs(r["extra_costo_vs_scorrelato_eur"]) < 1e-9

    def test_load_price_corr_input_non_validi(self):
        f = load("load_price_corr")["load_price_corr"]
        assert not f([1.0, 2.0], [1.0, 2.0, 3.0])["valido"]
        assert not f([1.0, 2.0], [1.0, 2.0])["valido"]
        assert not f([1.0, float("nan"), 3.0], [1.0, 2.0, 3.0])["valido"]

    def test_load_price_corr_spearman_monotona(self):
        f = load("load_price_corr")["load_price_corr"]
        load_kw = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        price = np.array([1.0, 4.0, 9.0, 16.0, 25.0, 36.0])
        r = f(load_kw, price)
        assert r["valido"]
        assert abs(r["r_spearman"] - 1.0) < 1e-9

    def test_load_price_corr_extra_costo_formula(self):
        f = load("load_price_corr")["load_price_corr"]
        load_kw = np.array([100.0, 100.0, 100.0, 100.0])
        price = np.array([100.0, 100.0, 200.0, 200.0])
        r = f(load_kw, price)
        assert r["valido"]
        atteso = (100 * 100 + 100 * 100 + 100 * 200 + 100 * 200) / 1000.0
        scorrelato = 100.0 * (100 + 100 + 200 + 200) / 1000.0
        assert abs(r["costo_effettivo_eur"] - atteso) < 1e-9
        assert abs(r["costo_scorrelato_eur"] - scorrelato) < 1e-9
        assert abs(r["extra_costo_vs_scorrelato_eur"]) < 1e-9

    def test_profili_sintetici(self):
        fns = load("profilo_carico_sintetico_t235", "profilo_prezzo_sintetico_t235")
        lc = fns["profilo_carico_sintetico_t235"]()
        pr = fns["profilo_prezzo_sintetico_t235"]()
        assert lc.shape == (24,) and pr.shape == (24,)
        assert (lc >= 0).all() and (pr > 0).all()
        assert int(lc.argmax()) == 12
        assert int(pr.argmax()) == 18
        # riproducibilita' col seed
        lc2 = fns["profilo_carico_sintetico_t235"](rumore_pct=10.0, seed=7)
        lc3 = fns["profilo_carico_sintetico_t235"](rumore_pct=10.0, seed=7)
        assert np.array_equal(lc2, lc3)


class TestRegistryTab235:
    def test_tab235_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 326
        assert "🔁 Correlazione carico-prezzo" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab235" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab235" in withs
        assert len(withs) == len(dvars) == 326
        keys = re.findall(r'key="(t235_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10


class TestRegistryTab235Self:
    """Check della sola tab235, indipendenti dalle tab dei worker paralleli."""

    def test_tab235_blocco_e_chiavi(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(encoding="utf-8")
        assert "    with tab235:" in src
        assert "🔁 Correlazione carico-prezzo" in src
        keys = re.findall(r'key="(t235_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10
