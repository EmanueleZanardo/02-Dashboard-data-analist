"""Test tab203 'Costo di liquidazione': helper calcola_costo_liquidazione —
bid-ask spread + impatto di mercato, giorni necessari, alert fuori tempo.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import numpy as np
import pandas as pd

from appfuncs import load

_F = load("calcola_costo_liquidazione")
calcola_costo_liquidazione = _F["calcola_costo_liquidazione"]

COLS = ["Prodotto", "MW", "Ore", "Prezzo_EUR_MWh",
        "Vol_medio_giornaliero_MWh"]


def _df(righe):
    return pd.DataFrame(righe, columns=COLS)


class TestValoriAttesi:
    def test_numeri_calcolabili_a_mano(self):
        # MW=5, Ore=744 -> volume 3720 MWh; nozionale 353400 EUR.
        # spread 10 bps -> meta' spread: 3720*95*10/20000 = 176.70
        # capacita' gg = 0.2*10000 = 2000 -> giorni = ceil(3720/2000) = 2
        # partecipazione media = 3720/(2*10000) = 0.186
        # impatto bps = 10*1.0*(0.186/0.2) = 9.3
        # costo impatto = 3720*95*9.3/10000 = 328.662
        # totale = 505.362; EUR/MWh = 0.1358468; pct = 0.143008%
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 95.0, 10000.0]]), 10.0, 0.2, 10, 1.0)
        assert r["errore"] is None
        assert r["valido"] is True
        assert r["n_posizioni"] == 1
        g = r["df_dettaglio"]
        assert abs(g.loc[0, "Costo spread (EUR)"] - 176.70) < 1e-6
        assert abs(g.loc[0, "Costo impatto (EUR)"] - 328.66) < 1e-9
        assert abs(g.loc[0, "Impatto (bps)"] - 9.3) < 1e-9
        assert abs(g.loc[0, "Costo totale (EUR)"] - 505.36) < 1e-9
        assert abs(g.loc[0, "Costo (EUR/MWh)"] - 0.1358) < 1e-9
        assert g.loc[0, "Giorni necessari"] == 2
        assert g.loc[0, "Stato"] == "OK"
        assert g.loc[0, "Direzione"] == "Long"
        assert abs(r["costo_totale"] - 505.362) < 1e-6
        assert abs(r["nozionale_totale"] - 353400.0) < 1e-6
        assert abs(r["costo_pct_nozionale"] - 100.0 * 505.362 / 353400.0) < 1e-9
        assert abs(r["costo_medio_mwh"] - 505.362 / 3720.0) < 1e-9
        assert "CONTENUTO" in r["verdetto"]

    def test_fuori_tempo(self):
        # MW=100, Ore=744 -> volume 74400; capacita' 2000/gg
        # giorni = ceil(74400/2000) = 38 > 10 -> FUORI TEMPO, verdetto CRITICO
        r = calcola_costo_liquidazione(
            _df([["B", 100.0, 744.0, 95.0, 10000.0]]), 10.0, 0.2, 10, 1.0)
        assert r["errore"] is None
        g = r["df_dettaglio"]
        assert g.loc[0, "Giorni necessari"] == 38
        assert g.loc[0, "Stato"] == "FUORI TEMPO"
        assert r["n_fuori_tempo"] == 1
        assert "CRITICO" in r["verdetto"]

    def test_costo_elevato_sopra_1pct(self):
        # spread enorme 400 bps su volume piccolo: costo > 1% nozionale
        r = calcola_costo_liquidazione(
            _df([["C", 1.0, 100.0, 50.0, 100000.0]]), 400.0, 0.5, 10, 1.0)
        assert r["errore"] is None
        assert r["costo_pct_nozionale"] > 1.0
        assert "ELEVATO" in r["verdetto"]

    def test_spread_zero_impatto_zero(self):
        r = calcola_costo_liquidazione(
            _df([["D", 2.0, 100.0, 50.0, 100000.0]]), 0.0, 0.2, 10, 1.0)
        assert r["errore"] is None
        assert r["costo_totale"] == 0.0
        assert r["df_dettaglio"].loc[0, "Impatto (bps)"] == 0.0

    def test_short_usa_valore_assoluto(self):
        r = calcola_costo_liquidazione(
            _df([["E", -5.0, 744.0, 95.0, 10000.0]]), 10.0, 0.2, 10, 1.0)
        assert r["errore"] is None
        g = r["df_dettaglio"]
        assert g.loc[0, "Direzione"] == "Short"
        assert abs(g.loc[0, "Volume (MWh)"] - 3720.0) < 1e-9
        assert abs(g.loc[0, "Costo totale (EUR)"] - 505.36) < 1e-9


class TestInputInvalidi:
    def test_vuoto(self):
        r = calcola_costo_liquidazione(_df([]))
        assert r["errore"] is not None and r["valido"] is False

    def test_non_dataframe(self):
        r = calcola_costo_liquidazione("no")
        assert r["errore"] is not None

    def test_colonne_mancanti(self):
        df = _df([["A", 5.0, 744.0, 95.0, 10000.0]]).drop(columns=["Ore"])
        r = calcola_costo_liquidazione(df)
        assert "Ore" in r["errore"]

    def test_mw_zero(self):
        r = calcola_costo_liquidazione(
            _df([["A", 0.0, 744.0, 95.0, 10000.0]]))
        assert r["errore"] is not None

    def test_ore_negative(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, -10.0, 95.0, 10000.0]]))
        assert r["errore"] is not None

    def test_prezzo_zero(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 0.0, 10000.0]]))
        assert r["errore"] is not None

    def test_vol_medio_zero(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 95.0, 0.0]]))
        assert r["errore"] is not None

    def test_prodotto_vuoto(self):
        r = calcola_costo_liquidazione(
            _df([["  ", 5.0, 744.0, 95.0, 10000.0]]))
        assert r["errore"] is not None

    def test_spread_negativo(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 95.0, 10000.0]]), -1.0)
        assert r["errore"] is not None

    def test_partecipazione_fuori_banda(self):
        df = _df([["A", 5.0, 744.0, 95.0, 10000.0]])
        assert calcola_costo_liquidazione(df, 10.0, 0.0)["errore"] is not None
        assert calcola_costo_liquidazione(df, 10.0, 1.5)["errore"] is not None

    def test_giorni_max_zero(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 95.0, 10000.0]]), 10.0, 0.2, 0)
        assert r["errore"] is not None

    def test_fattore_negativo(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 95.0, 10000.0]]), 10.0, 0.2, 10, -0.5)
        assert r["errore"] is not None

    def test_bool_rifiutato(self):
        r = calcola_costo_liquidazione(
            _df([["A", 5.0, 744.0, 95.0, 10000.0]]), True)
        assert r["errore"] is not None


class TestDeterminismo:
    def test_due_run_identici(self):
        df = _df([["A", 5.0, 744.0, 95.0, 10000.0],
                  ["B", -2.0, 300.0, 120.0, 1500.0]])
        r1 = calcola_costo_liquidazione(df, 10.0, 0.2, 10, 1.0)
        r2 = calcola_costo_liquidazione(df, 10.0, 0.2, 10, 1.0)
        assert r1["costo_totale"] == r2["costo_totale"]
        assert r1["df_dettaglio"].equals(r2["df_dettaglio"])


class TestRegistry:
    def test_registry_tab203(self):
        src = open("app.py").read()
        import ast as _ast
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
        assert len(titoli) == 296
        assert titoli[-1] == "🪓🛡 Component ES: chi contribuisce alla coda?"
        # variabili tabN: devono essere 204 e tab203 presente (non più ultima)
        import re as _re
        m = _re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 296
        assert "tab203" in vars_tab
        # key widget uniche
        keys = _re.findall(r'key="(liq203_[^"]+)"', src)
        assert len(keys) == 6
        assert len(set(keys)) == 6
