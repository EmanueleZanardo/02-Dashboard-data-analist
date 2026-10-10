"""Test tab204 'Opzione di differimento': helper calcola_opzione_differimento —
opzione reale di differimento di un investimento energetico (call americana
sul valore del progetto via albero CRR), valore dell'attesa, soglia critica.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import ast as _ast

import numpy as np

from appfuncs import load

_F = load("calcola_opzione_differimento")
calcola_opzione_differimento = _F["calcola_opzione_differimento"]


class TestCasiLimite:
    def test_sigma_zero_deterministico(self):
        # senza volatilita' l'opzione vale l'intrinseco: attesa nulla
        r = calcola_opzione_differimento(100.0, 90.0, 2.0, 0.0, 5.0, 3.0)
        assert r["errore"] is None and r["valido"] is True
        assert abs(r["valore_opzione"] - 10.0) < 1e-9
        assert abs(r["valore_europea"] - 10.0) < 1e-9
        assert r["valore_attesa"] == 0.0
        assert r["soglia_critica"] == 90.0
        assert r["decisione"] == "INVESTI ORA"

    def test_scadenza_zero(self):
        r = calcola_opzione_differimento(100.0, 110.0, 0.0, 30.0, 5.0, 0.0)
        assert r["valido"] is True
        assert r["valore_opzione"] == 0.0
        assert r["van_immediato"] == -10.0
        assert r["decisione"] == "NON INVESTIRE"

    def test_input_non_validi(self):
        for args in [(0.0, 90.0, 2.0, 20.0, 5.0, 0.0),
                      (100.0, 0.0, 2.0, 20.0, 5.0, 0.0),
                      (100.0, 90.0, -1.0, 20.0, 5.0, 0.0),
                      (100.0, 90.0, 2.0, -5.0, 5.0, 0.0),
                      (100.0, 90.0, 2.0, 20.0, 5.0, -1.0),
                      (100.0, 90.0, 2.0, 20.0, 5.0, 0.0, 0),
                      ("x", 90.0, 2.0, 20.0, 5.0, 0.0)]:
            r = calcola_opzione_differimento(*args)
            assert r["valido"] is False and r["errore"], args

    def test_nan_non_sollevano(self):
        r = calcola_opzione_differimento(float("nan"), 90.0, 2.0, 20.0,
                                         5.0, 0.0)
        assert r["valido"] is False


class TestProprieta:
    def test_gerarchia_prezzi(self):
        r = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 5.0, 2.0)
        assert r["valido"] is True
        am, eu = r["valore_opzione"], r["valore_europea"]
        assert am >= eu >= 0.0
        assert am >= max(100.0 - 90.0, 0.0) - 1e-9
        assert r["early_premium"] >= -1e-9
        assert r["valore_attesa"] >= 0.0

    def test_determinismo(self):
        a = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 5.0, 2.0)
        b = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 5.0, 2.0)
        assert a["valore_opzione"] == b["valore_opzione"]
        assert a["soglia_critica"] == b["soglia_critica"]

    def test_monotonia(self):
        base = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 5.0,
                                            2.0)["valore_opzione"]
        up_v = calcola_opzione_differimento(120.0, 90.0, 2.0, 30.0, 5.0,
                                            2.0)["valore_opzione"]
        up_s = calcola_opzione_differimento(100.0, 90.0, 2.0, 50.0, 5.0,
                                            2.0)["valore_opzione"]
        assert up_v > base and up_s > base

    def test_deep_itm_con_costo_attesa_alto_investi_ora(self):
        r = calcola_opzione_differimento(300.0, 90.0, 2.0, 30.0, 5.0, 25.0)
        assert r["decisione"] == "INVESTI ORA"
        assert r["valore_attesa"] < 0.005 * 300.0

    def test_senza_costo_attesa_ne_interessi_mai_esercizio(self):
        # dy = 0 e r = 0: aspettare e' gratis -> mai ottimale esercitare prima
        r = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 0.0, 0.0)
        assert r["soglia_critica"] is None

    def test_soglia_coerente(self):
        r = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 5.0, 2.0)
        s = r["soglia_critica"]
        assert s is not None and s >= 90.0
        r2 = calcola_opzione_differimento(s, 90.0, 2.0, 30.0, 5.0, 2.0)
        assert abs(r2["valore_opzione"] - (s - 90.0)) < 1e-3 * s

    def test_strutture_output(self):
        r = calcola_opzione_differimento(100.0, 90.0, 2.0, 30.0, 5.0, 2.0)
        assert list(r["df_vs_V"].columns) == [
            "V_progetto (EUR)", "Opzione (EUR)", "VAN immediato (EUR)",
            "Valore attesa (EUR)"]
        assert list(r["df_vs_vol"].columns) == [
            "Volatilita' (%)", "Opzione (EUR)", "Valore attesa (EUR)"]
        assert len(r["df_vs_V"]) == 21 and len(r["df_vs_vol"]) == 11
        assert r["decisione"] in ("INVESTI ORA", "ASPETTA",
                                  "NON INVESTIRE ORA", "NON INVESTIRE")


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
        assert len(titoli) == 356
        assert titoli[-1] == "Kelly bayesiano: sizing con win-rate posterior"
        import re as _re
        m = _re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 356
        assert vars_tab[-1] == "tab356"
        withs = _re.findall(r"    with (tab\d+):", src)
        assert len(withs) == 356 and "tab205" in withs
        keys = _re.findall(r'key="(dif204_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 7
