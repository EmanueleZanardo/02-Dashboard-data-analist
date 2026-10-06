"""Test tab205 'Dimensionamento debito (DSCR)': helper calcola_debt_sizing —
debt sizing project-finance con debt service sculpted a DSCR costante,
gearing, LLCR/PLCR, IRR equity.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import ast as _ast

import numpy as np

from appfuncs import load

_F = load("calcola_debt_sizing")
calcola_debt_sizing = _F["calcola_debt_sizing"]


class TestCasiBase:
    def test_numeri_a_mano(self):
        # 10 MW x 1500 h = 15000 MWh; prezzo 80 -> ricavi 1.2M; OPEX 150k
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25)
        assert r["errore"] is None and r["valido"] is True
        assert abs(r["capex"] - 8_000_000.0) < 1e-6
        assert abs(r["energia_anno1"] - 15000.0) < 1e-6
        assert abs(r["cfads_anno1"] - 1_050_000.0) < 1e-6
        # debt service anno 1 = CFADS / DSCR
        ds1 = r["df_annuale"]["Debt service (EUR)"][0]
        assert abs(ds1 - 1_050_000.0 / 1.4) < 1.0
        assert r["tenor"] == 15
        assert len(r["df_annuale"]) == 25

    def test_invariante_sculpting(self):
        # con sculpting a DSCR costante: DSCR profilo == target e LLCR == target
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25)
        assert abs(r["dscr_min"] - 1.4) < 1e-9
        assert abs(r["dscr_medio"] - 1.4) < 1e-9
        assert abs(r["llcr"] - 1.4) < 1e-9
        assert r["plcr"] > r["llcr"]  # vita > tenor
        assert abs(r["equity"] - (r["capex"] - r["debito_max"])) < 1e-6

    def test_tasso_zero(self):
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.0, 0.0, 15, 1.4, 25)
        atteso = sum(1_050_000.0 / 1.4 for _ in range(15))
        assert abs(r["debito_max"] - atteso) < 1e-3

    def test_irr_equity_coerente(self):
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25)
        irr = r["irr_equity"]
        assert irr is not None and irr > 0.0
        df = r["df_annuale"]
        cf = [-r["equity"]] + list(
            df["CFADS (EUR)"].values - df["Debt service (EUR)"].values)
        npv = sum(c / (1.0 + irr) ** i for i, c in enumerate(cf))
        assert abs(npv) < 1.0  # per definizione di IRR

    def test_non_finanziabile(self):
        # prezzo alto -> debito > CAPEX -> gearing oltre 100%
        r = calcola_debt_sizing(10, 1500, 200, 800, 15, 0.5, 5.0, 15, 1.3, 25)
        assert r["valido"] is True
        assert r["finanziabile"] is False and r["gearing"] > 1.0

    def test_tenor_limitato_dalla_vita(self):
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 30, 1.4, 20)
        assert r["tenor"] == 20
        assert len(r["df_annuale"]) == 20

    def test_degrado_riduce_energia(self):
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 2.0, 5.0, 15, 1.4, 25)
        e = r["df_annuale"]["Energia (MWh)"].values
        assert abs(e[2] - e[0] * 0.98 ** 2) < 0.1
        assert all(e[i] > e[i + 1] for i in range(len(e) - 1))

    def test_dscr_piu_alto_meno_debito(self):
        a = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.2, 25)
        b = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.8, 25)
        assert b["debito_max"] < a["debito_max"]
        assert b["gearing"] < a["gearing"]

    def test_input_non_validi(self):
        base = [10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25]
        for i, bad in [(0, 0.0), (1, 0.0), (2, 0.0), (3, 0.0), (4, -1.0),
                       (5, 100.0), (6, -1.0), (7, 0.0), (8, 0.9), (9, 0.0)]:
            args = list(base)
            args[i] = bad
            r = calcola_debt_sizing(*args)
            assert r["valido"] is False and r["errore"], (i, bad)
        # OPEX che azzera il CFADS
        r = calcola_debt_sizing(10, 1500, 80, 800, 5000, 0.5, 5.0, 15, 1.4, 25)
        assert r["valido"] is False and r["errore"]
        # non numerico e NaN
        assert calcola_debt_sizing("x", *base[1:])["valido"] is False
        assert calcola_debt_sizing(float("nan"), *base[1:])["valido"] is False

    def test_determinismo(self):
        a = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25)
        b = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25)
        assert a["debito_max"] == b["debito_max"]
        assert a["df_annuale"].equals(b["df_annuale"])
        assert a["irr_equity"] == b["irr_equity"]

    def test_colonne_df(self):
        r = calcola_debt_sizing(10, 1500, 80, 800, 15, 0.5, 5.0, 15, 1.4, 25)
        assert list(r["df_annuale"].columns) == [
            "Anno", "Energia (MWh)", "Ricavi (EUR)", "OPEX (EUR)",
            "CFADS (EUR)", "Debt service (EUR)", "DSCR"]


class TestRegistryTab205:
    def test_registry_205(self):
        from pathlib import Path
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
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
        assert len(titoli) == 272
        assert titoli[-1] == "🌬️ Eolico offshore: business case"
        import re as _re
        m = _re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 272
        assert vars_tab[-1] == "tab272"
        withs = _re.findall(r"    with (tab\d+):", src)
        assert len(withs) == 272 and "tab205" in withs
        keys = _re.findall(r'key="(deb205_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 11
