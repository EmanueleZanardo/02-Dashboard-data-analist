"""Test tab242 'Potenza impegnata ottimale': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab242.
"""

import re
from pathlib import Path

import numpy as np
import pytest

from appfuncs import load

_F = load("pot242_profilo_annuo", "pot242_picchi_mensili",
          "pot242_costo_annuo", "pot242_curva_ottimo")
pot242_profilo_annuo = _F["pot242_profilo_annuo"]
pot242_picchi_mensili = _F["pot242_picchi_mensili"]
pot242_costo_annuo = _F["pot242_costo_annuo"]
pot242_curva_ottimo = _F["pot242_curva_ottimo"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab242:
    def test_tab242_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 360
        assert "⚡ Potenza impegnata ottimale" in titoli
        assert "tab242" in dvars
        assert "tab242" in withs
        assert titoli[dvars.index("tab242")] == "⚡ Potenza impegnata ottimale"
        keys = re.findall(r'key="(t242_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_231_242(self):
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
        }
        for var, tit in attesi.items():
            assert titoli[dvars.index(var)] == tit, var


class TestCostoAnnuo:
    def test_caso_base_a_mano(self):
        # 12 mesi a picco 100 kW, impegnata 100: fisso 100*10=1000, penali 0
        r = pot242_costo_annuo([100] * 12, 100, 10, 2)
        assert r["fisso"] == 1000.0
        assert r["penale"] == 0.0
        assert r["totale"] == 1000.0
        assert r["mesi_sforati"] == 0
        assert r["sforamento_max_kw"] == 0.0

    def test_sforamento_a_mano(self):
        # impegnata 90: fisso 900 + penali 12*10*2 = 240 -> totale 1140
        r = pot242_costo_annuo([100] * 12, 90, 10, 2)
        assert r["fisso"] == 900.0
        assert r["penale"] == 240.0
        assert r["totale"] == 1140.0
        assert r["mesi_sforati"] == 12
        assert r["sforamento_max_kw"] == 10.0

    def test_picchi_misti_a_mano(self):
        # 6 mesi a 120 + 6 mesi a 80, impegnata 100, fisso 24, penale 3
        # fisso 2400 + penale 6*20*3 = 360 -> 2760
        r = pot242_costo_annuo([120] * 6 + [80] * 6, 100, 24, 3)
        assert r["totale"] == 2760.0
        assert r["mesi_sforati"] == 6
        assert r["sforamento_max_kw"] == 20.0

    def test_errori(self):
        with pytest.raises(ValueError):
            pot242_costo_annuo([100] * 11, 100, 10, 2)  # non 12 valori
        with pytest.raises(ValueError):
            pot242_costo_annuo([100] * 12, -5, 10, 2)  # impegnata negativa
        with pytest.raises(ValueError):
            pot242_costo_annuo([100] * 12, 100, -1, 2)  # fisso negativo
        with pytest.raises(ValueError):
            pot242_costo_annuo([float("nan")] + [100] * 11, 100, 10, 2)  # NaN


class TestCurvaOttimo:
    def test_ottimo_caso_piatto(self):
        # picco piatto 100: l'ottimo e' esattamente 100 (nessuna penale, fisso minimo)
        o = pot242_curva_ottimo([100] * 12, 10, 2, passo=5.0)
        assert o["p_ottima"] == 100.0
        assert o["costo_ottimo"] == 1000.0
        assert all(c >= 1000.0 for _, c in o["curva"])

    def test_ottimo_caso_misto_a_mano(self):
        # 6 mesi 120 + 6 mesi 80, fisso 24 €/kW/anno, penale 3 €/kW/mese
        # costi a mano: P=120->2880, P=100->2760, P=80->2640, P=60->2880 => ottimo 80
        o = pot242_curva_ottimo([120] * 6 + [80] * 6, 24, 3, passo=10.0)
        assert o["p_ottima"] == 80.0
        assert o["costo_ottimo"] == 2640.0
        assert all(c >= 2640.0 for _, c in o["curva"])

    def test_ottimo_risparmio_vs_picco(self):
        # con penale bassa conviene impegnare meno del picco
        o = pot242_curva_ottimo([100] * 12, 100, 0.5, passo=1.0)
        assert o["p_ottima"] < 100.0  # fisso 100 €/kW/anno >> penale 0.5 €/kW/mese
        c_picco = pot242_costo_annuo([100] * 12, 100, 100, 0.5)["totale"]
        assert o["costo_ottimo"] < c_picco

    def test_errori(self):
        with pytest.raises(ValueError):
            pot242_curva_ottimo([100] * 12, 10, 2, passo=0)
        with pytest.raises(ValueError):
            pot242_curva_ottimo([100] * 12, 10, 2, p_min=200, p_max=100)


class TestProfiloEPicchi:
    def test_profilo_8760_e_determinismo(self):
        p1 = pot242_profilo_annuo(40, 120, 12, 20, seed=242)
        p2 = pot242_profilo_annuo(40, 120, 12, 20, seed=242)
        assert len(p1) == 8760
        assert p1 == p2
        assert all(x >= 0 for x in p1)

    def test_picchi_costanti(self):
        picchi = pot242_picchi_mensili([50.0] * 8760)
        assert len(picchi) == 12
        assert picchi == [50.0] * 12

    def test_picchi_massimi_mensili(self):
        prof = [0.0] * 8760
        prof[100] = 999.0  # gennaio (ore 0..729)
        prof[8500] = 500.0  # dicembre (ore 8030..8759)
        picchi = pot242_picchi_mensili(prof)
        assert picchi[0] == 999.0
        assert picchi[11] == 500.0

    def test_stagionalita_luglio_piu_alto(self):
        p = pot242_profilo_annuo(40, 120, 12, 60, seed=7)
        picchi = pot242_picchi_mensili(p)
        assert picchi[6] > picchi[0]  # luglio > gennaio

    def test_errori(self):
        with pytest.raises(ValueError):
            pot242_picchi_mensili([1.0] * 100)  # non 8760 ore
        with pytest.raises(ValueError):
            pot242_picchi_mensili([1.0] * 8759 + [float("nan")])
        with pytest.raises(ValueError):
            pot242_profilo_annuo(-1, 100, 12, 20)
