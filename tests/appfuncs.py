"""Helper condiviso dei test pytest: estrae funzioni pure da app.py via AST.

Le funzioni di calcolo di app.py sono pure (niente Streamlit a livello di
corpo funzione); questo modulo le compila in un namespace con solo
pandas/numpy (+ un dummy di st per i decoratori @st.cache_data) così i test
girano senza avviare Streamlit.

Uso:
    from appfuncs import load
    fns = load("fascia_oraria", "calcola_volatilita")
"""

import ast
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

APP = Path(__file__).resolve().parent.parent / "app.py"


class _DummySt:
    """Solo per i decoratori @st.cache_data: li rende no-op nei test."""

    @staticmethod
    def cache_data(*a, **k):
        def deco(fn):
            return fn

        # supporta sia @st.cache_data sia @st.cache_data(...)
        if a and callable(a[0]) and len(a) == 1 and not k:
            return a[0]
        return deco


_TREE = None


def load(*names):
    """Ritorna dict {nome: funzione} con le funzioni richieste da app.py.

    Solleva AssertionError se una funzione non esiste in app.py.
    """
    global _TREE
    if _TREE is None:
        _TREE = ast.parse(APP.read_text(encoding="utf-8"))
    ns = {"np": np, "pd": pd, "st": _DummySt(), "norm": norm}
    out = {}
    for node in _TREE.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(APP), "exec"), ns)  # noqa: S102 - repo proprio
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(f"funzioni non trovate in app.py: {missing}")
    return out
