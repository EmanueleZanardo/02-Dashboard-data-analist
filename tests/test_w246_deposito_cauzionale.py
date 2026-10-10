"""Test tab246 'Deposito cauzionale': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab246.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("d246_deposito", "d246_costo_opportunita", "d246_costo_fideiussione", "d246_sintesi")
d246_deposito = _F["d246_deposito"]
d246_costo_opportunita = _F["d246_costo_opportunita"]
d246_costo_fideiussione = _F["d246_costo_fideiussione"]
d246_sintesi = _F["d246_sintesi"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab246:
    def test_tab246_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 369
        assert "🛡️ Deposito cauzionale" in titoli
        assert "tab246" in dvars
        assert "tab246" in withs
        assert titoli[dvars.index("tab246")] == "🛡️ Deposito cauzionale"
        keys = re.findall(r'key="(t246_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_245_246(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab245")] == "💳 Conguaglio a rate"
        assert titoli[dvars.index("tab246")] == "🛡️ Deposito cauzionale"


class TestD246Deposito:
    def test_valore_noto(self):
        lordo, netto = d246_deposito(12000.0, 2, 50.0)
        assert (lordo, netto) == (2000.0, 1000.0)

    def test_zero_mesi(self):
        assert d246_deposito(12000.0, 0, 0.0) == (0.0, 0.0)

    def test_sdd_100_azzera(self):
        lordo, netto = d246_deposito(12000.0, 3, 100.0)
        assert lordo == 3000.0 and netto == 0.0

    def test_input_invalidi(self):
        for args in [(0, 2, 50), (12000, 7, 50), (12000, 2, 101), (12000, 2, -1)]:
            with pytest.raises(ValueError):
                d246_deposito(*args)


class TestD246Costi:
    def test_opportunita(self):
        assert d246_costo_opportunita(1000.0, 4.0) == pytest.approx(40.0)

    def test_fideiussione(self):
        assert d246_costo_fideiussione(1000.0, 1.0) == pytest.approx(10.0)

    def test_negativi(self):
        with pytest.raises(ValueError):
            d246_costo_opportunita(-1.0, 4.0)
        with pytest.raises(ValueError):
            d246_costo_fideiussione(100.0, -1.0)


class TestD246Sintesi:
    def test_sintesi_completa(self):
        s = d246_sintesi(12000.0, 2, 50.0, 4.0, 1.0)
        assert s["deposito_lordo"] == 2000.0
        assert s["deposito_netto"] == 1000.0
        assert s["costo_opportunita_annuo"] == pytest.approx(40.0)
        assert s["costo_fideiussione_annuo"] == pytest.approx(10.0)
        assert s["costo_totale_annuo"] == pytest.approx(50.0)
        assert s["incidenza_pct"] == pytest.approx(0.417, rel=1e-3)

    def test_sdd_100_costi_zero(self):
        s = d246_sintesi(12000.0, 3, 100.0, 4.0, 1.0)
        assert s["deposito_netto"] == 0.0
        assert s["costo_totale_annuo"] == 0.0
