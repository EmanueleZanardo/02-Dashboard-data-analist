"""Test tab243 'Picchi quartorari (15')': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab243.
"""

import re
from pathlib import Path

import numpy as np
import pytest

from appfuncs import load

_F = load("q243_a_quarti", "q243_picchi_mensili_q", "q243_sintesi",
          "pot242_profilo_annuo")
q243_a_quarti = _F["q243_a_quarti"]
q243_picchi_mensili_q = _F["q243_picchi_mensili_q"]
q243_sintesi = _F["q243_sintesi"]
pot242_profilo_annuo = _F["pot242_profilo_annuo"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab243:
    def test_tab243_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 299
        assert "⏱️ Picchi quartorari (15')" in titoli
        assert "tab243" in dvars
        assert "tab243" in withs
        assert titoli[dvars.index("tab243")] == "⏱️ Picchi quartorari (15')"
        keys = re.findall(r'key="(t243_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_231_243(self):
        _, titoli, dvars, _ = _registry()
        attesi = {
            "tab231": "🔍 Qualità dati (gap & outlier)",
            "tab232": "🧮 Concentrazione temporale (HHI)",
            "tab234": "🎯 Score di timing",
            "tab239": "📊 Probabilità sforamento budget",
            "tab235": "🔁 Correlazione carico-prezzo",
            "tab233": "💧 Waterfall del costo",
            "tab240": "📋 Checklist gara fornitura",
            "tab238": "🌙 Baseload notturno",
            "tab241": "🗺️ Mappa prezzo×carico",
            "tab242": "⚡ Potenza impegnata ottimale",
            "tab243": "⏱️ Picchi quartorari (15')",
        }
        for var, tit in attesi.items():
            assert titoli[dvars.index(var)] == tit

    def test_ultimo_titolo(self):
        _, titoli, _, _ = _registry()
        assert titoli[-1] == "🧪⚡ Stress test: quanto perde il book negli scenari?"

    def test_helper_definiti_prima_della_ui(self):
        """Regressione bug 05/10 17:40: gli helper delle tab232-242 erano definiti
        DOPO i blocchi with tabNNN che li usano -> NameError a runtime."""
        src = APP.read_text(encoding="utf-8")
        for fn in ["q243_a_quarti", "q243_sintesi",
                   "pot242_profilo_annuo", "calcola_mappa_prezzo_carico",
                   "hhi_index", "w239_simulate_annual_cost", "checklist_score",
                   "night_share238", "clc236_carico_residuo", "flx237_shifting_saving"]:
            pos_def = src.find(f"def {fn}(")
            pos_use = src.find(f"{fn}(", src.find("    with tab"))
            assert 0 < pos_def < pos_use, f"{fn} definita dopo l'uso nella UI"


class TestQ243Funzioni:
    def test_piatto_pct_zero(self):
        q = q243_a_quarti([100.0] * 8760, 0.0, seed=1)
        assert len(q) == 35040
        assert all(x == 100.0 for x in q)

    def test_picco_e_energia(self):
        q = q243_a_quarti([100.0] * 8760, 20.0, seed=7)
        assert max(q) == pytest.approx(120.0)
        assert min(q) == pytest.approx(100.0 * (1.0 - 0.2 / 3.0))
        # energia dell'ora conservata esattamente
        assert sum(q) / 4.0 == pytest.approx(8760.0 * 100.0)

    def test_determinismo(self):
        a = q243_a_quarti([100.0] * 8760, 15.0, seed=243)
        b = q243_a_quarti([100.0] * 8760, 15.0, seed=243)
        assert a == b
        c = q243_a_quarti([100.0] * 8760, 15.0, seed=244)
        assert a != c

    def test_ore_non_positive(self):
        q = q243_a_quarti([0.0, -5.0] + [50.0] * 22, 15.0, seed=1)
        assert q[:8] == [0.0] * 8

    def test_errori_input(self):
        with pytest.raises(ValueError):
            q243_a_quarti([1.0] * 10, 15.0, 1)          # < 24 ore
        with pytest.raises(ValueError):
            q243_a_quarti([float("nan")] * 8760, 15.0, 1)  # NaN
        with pytest.raises(ValueError):
            q243_a_quarti([100.0] * 8760, -5.0, 1)       # pct negativa
        with pytest.raises(ValueError):
            q243_a_quarti([100.0] * 8760, True, 1)       # bool
        with pytest.raises(ValueError):
            q243_a_quarti([100.0] * 8760, 400.0, 1)      # > 300%
        with pytest.raises(ValueError):
            q243_a_quarti([100.0] * 8760, "x", 1)        # non numerico
        with pytest.raises(ValueError):
            q243_a_quarti("xx", 15.0, 1)                 # non sequenza numerica

    def test_picchi_mensili_q(self):
        q = q243_a_quarti([100.0] * 8760, 0.0, seed=1)
        pm = q243_picchi_mensili_q(q)
        assert pm == [100.0] * 12
        with pytest.raises(ValueError):
            q243_picchi_mensili_q([1.0] * 40)
        with pytest.raises(ValueError):
            q243_picchi_mensili_q([float("nan")] * 96)

    def test_sintesi_piatta(self):
        s = q243_sintesi([100.0] * 8760, 0.0, seed=1)
        assert s["n_ore"] == 8760
        assert s["n_quarti"] == 35040
        assert s["energia_mwh"] == pytest.approx(876.0)
        assert s["picco_orario_kw"] == pytest.approx(100.0)
        assert s["picco_quartorario_kw"] == pytest.approx(100.0)
        assert s["rapporto_qh_pct"] == pytest.approx(100.0)
        assert s["delta_picco_kw"] == pytest.approx(0.0)
        assert s["picchi_mensili_orari"] == [100.0] * 12
        assert s["picchi_mensili_quartorari"] == [100.0] * 12

    def test_sintesi_profilo_reale(self):
        h = pot242_profilo_annuo(40, 120, 12, 20, seed=7)
        s = q243_sintesi(h, 15.0, seed=3)
        assert s["picco_quartorario_kw"] >= s["picco_orario_kw"]
        assert 100.0 <= s["rapporto_qh_pct"] <= 115.0
        assert s["energia_mwh"] == pytest.approx(sum(h) / 1000.0)
        assert len(s["picchi_mensili_quartorari"]) == 12
        assert s["picchi_mensili_quartorari"] == q243_picchi_mensili_q(
            q243_a_quarti(h, 15.0, 3))
        # energia conservata nella conversione
        assert sum(q243_a_quarti(h, 15.0, 3)) / 4.0 == pytest.approx(sum(h))
