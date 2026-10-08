"""Test tab214 'Backtest offerta indicizzata': helper calcola_backtest_indicizzato —
regolazione ex-post di una clausola indicizzata (spot medio mensile + spread,
con cap/floor opzionali) contro un'offerta a prezzo fisso, con prezzo fisso
di pareggio.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_backtest_indicizzato")
calcola_backtest_indicizzato = _F["calcola_backtest_indicizzato"]

APP = Path(__file__).parent.parent / "app.py"


def _serie_piatta(prezzo=100.0, inizio="2026-01-01", fine="2026-02-28 23:00"):
    idx = pd.date_range(inizio, fine, freq="h")
    return pd.Series(prezzo, index=idx)


class TestNumeriAMano:
    def test_piatta_due_mesi(self):
        # Gen 2026: 31 gg = 744 h; Feb 2026: 28 gg = 672 h; spot = 100
        # fisso 120, spread 10 -> indicizzato 110; volume 100 MWh/mese
        r = calcola_backtest_indicizzato(_serie_piatta(), 120.0, 10.0,
                                         volume_mensile_mwh=100.0)
        assert r["errore"] is None and r["valido"] is True
        assert r["mesi"] == 2
        df = r["df_mesi"]
        assert list(df["Mese"]) == ["2026-01", "2026-02"]
        assert list(df["Ore osservate"]) == [744, 672]
        assert (df["Prezzo indicizzato (€/MWh)"] == 110.0).all()
        # costo ind: 100*110 + 100*110 = 22000; fisso: 200*120 = 24000
        assert r["costo_totale_indicizzato"] == pytest.approx(22000.0)
        assert r["costo_totale_fisso"] == pytest.approx(24000.0)
        assert r["risparmio_totale"] == pytest.approx(2000.0)
        assert r["risparmio_pct"] == pytest.approx(round(2000.0 / 24000.0 * 100.0, 2))
        assert r["volume_totale_mwh"] == pytest.approx(200.0)
        assert r["prezzo_fisso_pareggio"] == pytest.approx(110.0)
        assert r["pmp_indicizzato"] == pytest.approx(110.0)
        assert r["mesi_vinti_indicizzato"] == 2

    def test_cap_e_floor(self):
        s = _serie_piatta()
        # cap 105: indicizzato clampato a 105 -> costo 200*105 = 21000
        r = calcola_backtest_indicizzato(s, 120.0, 10.0, cap_eur_mwh=105.0,
                                         volume_mensile_mwh=100.0)
        assert r["errore"] is None
        assert r["costo_totale_indicizzato"] == pytest.approx(21000.0)
        assert r["risparmio_totale"] == pytest.approx(3000.0)
        # floor 90 con spread -30: raw 70 -> floor 90 -> costo 200*90 = 18000
        r2 = calcola_backtest_indicizzato(s, 120.0, -30.0, floor_eur_mwh=90.0,
                                          volume_mensile_mwh=100.0)
        assert r2["errore"] is None
        assert (r2["df_mesi"]["Prezzo indicizzato (€/MWh)"] == 90.0).all()
        assert r2["costo_totale_indicizzato"] == pytest.approx(18000.0)

    def test_scalatura_mese_parziale(self):
        # solo 12 ore di marzo 2026 (31 gg -> 744 h calendario)
        idx = pd.date_range("2026-03-01", periods=12, freq="h")
        s = pd.Series(100.0, index=idx)
        r = calcola_backtest_indicizzato(s, 120.0, 10.0,
                                         volume_mensile_mwh=100.0)
        assert r["errore"] is None and r["mesi"] == 1
        assert r["volume_totale_mwh"] == pytest.approx(round(100.0 * 12 / 744, 3))
        assert r["costo_totale_indicizzato"] == pytest.approx(round(100.0 * 12 / 744 * 110.0, 2))

    def test_ore_nan_escluse(self):
        idx = pd.date_range("2026-01-01", periods=48, freq="h")
        s = pd.Series(100.0, index=idx)
        s.iloc[0] = float("nan")
        r = calcola_backtest_indicizzato(s, 120.0, 10.0,
                                         volume_mensile_mwh=100.0)
        assert r["errore"] is None
        assert r["df_mesi"]["Ore osservate"].iloc[0] == 47


class TestInputNonValidi:
    def test_serie_vuota(self):
        r = calcola_backtest_indicizzato(pd.Series(dtype=float), 120.0, 10.0)
        assert r["errore"] is not None and r["valido"] is False

    def test_indice_non_temporale(self):
        s = pd.Series([100.0, 110.0], index=[0, 1])
        r = calcola_backtest_indicizzato(s, 120.0, 10.0)
        assert r["errore"] is not None and r["valido"] is False

    def test_floor_sopra_cap(self):
        r = calcola_backtest_indicizzato(_serie_piatta(), 120.0, 10.0,
                                         cap_eur_mwh=80.0, floor_eur_mwh=90.0)
        assert r["errore"] is not None and r["valido"] is False

    def test_volume_non_positivo(self):
        r = calcola_backtest_indicizzato(_serie_piatta(), 120.0, 10.0,
                                         volume_mensile_mwh=0.0)
        assert r["errore"] is not None and r["valido"] is False

    def test_prezzo_fisso_negativo(self):
        r = calcola_backtest_indicizzato(_serie_piatta(), -5.0, 10.0)
        assert r["errore"] is not None and r["valido"] is False

    def test_determinismo(self):
        s = _serie_piatta()
        r1 = calcola_backtest_indicizzato(s, 120.0, 10.0, volume_mensile_mwh=100.0)
        r2 = calcola_backtest_indicizzato(s, 120.0, 10.0, volume_mensile_mwh=100.0)
        assert r1["risparmio_totale"] == r2["risparmio_totale"]
        assert r1["df_mesi"].equals(r2["df_mesi"])


class TestRegistry:
    def test_tab214_dichiarata(self):
        import ast as _ast
        src = APP.read_text(encoding="utf-8")
        tree = _ast.parse(src)
        titoli = None
        for node in _ast.walk(tree):
            if (isinstance(node, _ast.Assign)
                    and isinstance(node.value, _ast.Call)
                    and getattr(getattr(node.value.func, "attr", ""),
                                "lower", lambda: "")() == "tabs"
                                and node.value.args and hasattr(node.value.args[0], "elts")):
                titoli = [t.value for t in node.value.args[0].elts]
        assert titoli is not None
        assert len(titoli) == 306
        assert titoli[-1] == "💎📊 RAROC: il rendimento ripaga il rischio?"
        m = re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 306
        assert "tab213" in vars_tab
        withs = re.findall(r"^\s*with (tab\d+):", src, re.M)
        assert len(withs) == len(vars_tab) == 306
        assert "tab214" in withs
        # key widget univoche della tab214
        keys = re.findall(r'key="(idx214_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 8
