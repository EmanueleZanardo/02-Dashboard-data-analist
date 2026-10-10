"""Test tab248 'Interessi moratori & ritardo pagamenti': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab248.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("d248_tasso_moratorio", "d248_interessi_moratori",
          "d248_costo_ritardo", "d248_confronto_sconto")
d248_tasso_moratorio = _F["d248_tasso_moratorio"]
d248_interessi_moratori = _F["d248_interessi_moratori"]
d248_costo_ritardo = _F["d248_costo_ritardo"]
d248_confronto_sconto = _F["d248_confronto_sconto"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab248:
    def test_tab248_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 359
        assert "💲 Interessi moratori & ritardo pagamenti" in titoli
        assert "tab248" in dvars
        assert "tab248" in withs
        assert titoli[dvars.index("tab248")] == "💲 Interessi moratori & ritardo pagamenti"
        keys = re.findall(r'key="(t248_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_247_248(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab247")] == "🔄 Voltura e subentro"
        assert titoli[dvars.index("tab248")] == "💲 Interessi moratori & ritardo pagamenti"


class TestD248TassoMoratorio:
    def test_bce_piu_8pp(self):
        # D.Lgs. 231/2002: BCE 2.00 + 8 pp = 10.00
        r = d248_tasso_moratorio(2.0)
        assert r == {"tasso_bce_pct": 2.0, "maggiorazione_pp": 8.0,
                     "tasso_moratorio_pct": 10.0}

    def test_maggiorazione_personalizzata(self):
        r = d248_tasso_moratorio(3.5, 5.0)
        assert r["tasso_moratorio_pct"] == pytest.approx(8.5)

    def test_tasso_negativo_errore(self):
        with pytest.raises(ValueError):
            d248_tasso_moratorio(-1.0)


class TestD248InteressiMoratori:
    def test_valore_noto(self):
        # 15000 * 10% * 30/365 = 123.287... -> 123.29
        r = d248_interessi_moratori(15000.0, 10.0, 30)
        assert r == {"capitale": 15000.0, "tasso_pct": 10.0, "giorni": 30,
                     "interessi": pytest.approx(123.29, abs=0.005)}

    def test_zero_giorni_zero_interessi(self):
        r = d248_interessi_moratori(15000.0, 10.0, 0)
        assert r["interessi"] == 0.0

    def test_importo_negativo_errore(self):
        with pytest.raises(ValueError):
            d248_interessi_moratori(-100.0, 10.0, 30)


class TestD248CostoRitardo:
    def test_valore_noto(self):
        # interessi 123.29 + spese 40 = 163.29; incidenza 1.0886% -> 1.089
        r = d248_costo_ritardo(15000.0, 10.0, 30, 40.0)
        assert r["interessi"] == pytest.approx(123.29, abs=0.005)
        assert r["recupero_spese"] == 40.0
        assert r["totale"] == pytest.approx(163.29, abs=0.01)
        assert r["incidenza_pct"] == pytest.approx(1.089, abs=0.001)
        assert r["costo_giornaliero"] == pytest.approx(5.44, abs=0.01)

    def test_spese_negative_errore(self):
        with pytest.raises(ValueError):
            d248_costo_ritardo(15000.0, 10.0, 30, -5.0)


class TestD248ConfrontoSconto:
    def test_mancato_risparmio(self):
        # sconto 2% su 15000 = 300; costo ritardo 163.29 -> mancato 463.29
        r = d248_confronto_sconto(15000.0, 163.29, 2.0)
        assert r == {"sconto_valore": 300.0, "costo_ritardo": 163.29,
                     "mancato_risparmio": pytest.approx(463.29, abs=0.01)}

    def test_sconto_zero(self):
        r = d248_confronto_sconto(15000.0, 100.0, 0.0)
        assert r["mancato_risparmio"] == 100.0
