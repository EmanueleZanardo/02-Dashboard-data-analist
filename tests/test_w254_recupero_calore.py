"""Test tab254 'Recupero calore di scarto': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab254.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("_wh254_num", "wh254_energia_recuperabile", "wh254_risparmio_gas",
          "wh254_pompa_calore", "wh254_co2_evitata",
          "wh254_business_case", "wh254_sensitivita", "wh254_sensitivita_pdc")
wh254_energia_recuperabile = _F["wh254_energia_recuperabile"]
wh254_risparmio_gas = _F["wh254_risparmio_gas"]
wh254_pompa_calore = _F["wh254_pompa_calore"]
wh254_co2_evitata = _F["wh254_co2_evitata"]
wh254_business_case = _F["wh254_business_case"]
wh254_sensitivita = _F["wh254_sensitivita"]
wh254_sensitivita_pdc = _F["wh254_sensitivita_pdc"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab254:
    def test_tab254_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 299
        assert "♨️ Recupero calore di scarto" in titoli
        assert "tab254" in dvars
        assert "tab254" in withs
        assert titoli[dvars.index("tab254")] == "♨️ Recupero calore di scarto"
        assert titoli[-1] == "🧪⚡ Stress test: quanto perde il book negli scenari?"
        keys = re.findall(r'key="(wh254_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_253_254(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab253")] == "🌑 Costo interruzioni (VoLL)"
        assert titoli[dvars.index("tab254")] == "♨️ Recupero calore di scarto"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("wh254_energia_recuperabile", "wh254_risparmio_gas",
                   "wh254_pompa_calore", "wh254_co2_evitata",
                   "wh254_business_case", "wh254_sensitivita",
                   "wh254_sensitivita_pdc"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestWh254EnergiaRecuperabile:
    def test_base(self):
        r = wh254_energia_recuperabile(500.0, 4000.0, 70.0)
        assert r["energia_utile_kwh"] == 1400000.0
        assert r["potenza_utile_kw"] == 350.0

    def test_zero(self):
        r = wh254_energia_recuperabile(500.0, 0.0, 70.0)
        assert r["energia_utile_kwh"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_energia_recuperabile(-1.0, 4000.0, 70.0)
        with pytest.raises(ValueError):
            wh254_energia_recuperabile(500.0, 9000.0, 70.0)
        with pytest.raises(ValueError):
            wh254_energia_recuperabile(500.0, 4000.0, 101.0)
        with pytest.raises(ValueError):
            wh254_energia_recuperabile(math.nan, 4000.0, 70.0)


class TestWh254RisparmioGas:
    def test_base(self):
        r = wh254_risparmio_gas(1400000.0, 0.09, 90.0)
        assert r["gas_risparmiato_kwh"] == 1555555.56
        assert r["risparmio_lordo_eur"] == 140000.0

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_risparmio_gas(-1.0, 0.09, 90.0)
        with pytest.raises(ValueError):
            wh254_risparmio_gas(1400000.0, 0.09, 0.0)


class TestWh254PompaCalore:
    def test_base(self):
        r = wh254_pompa_calore(200.0, 4.0, 4000.0, 0.18, 0.09, 90.0)
        assert r["calore_utile_kw"] == 266.67
        assert r["energia_utile_kwh"] == 1066666.67
        assert r["energia_elettrica_kwh"] == 266666.67
        assert r["costo_elettrico_eur"] == 48000.0
        assert r["gas_risparmiato_kwh"] == 1185185.19
        assert r["risparmio_lordo_eur"] == 106666.67
        assert r["risparmio_netto_eur"] == 58666.67
        assert r["cop_min_convenienza"] == 1.8
        assert r["pdc_conveniente"] is True

    def test_pdc_non_conveniente(self):
        r = wh254_pompa_calore(200.0, 2.0, 4000.0, 0.30, 0.09, 90.0)
        assert r["pdc_conveniente"] is False

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_pompa_calore(200.0, 1.0, 4000.0, 0.18, 0.09, 90.0)
        with pytest.raises(ValueError):
            wh254_pompa_calore(200.0, 4.0, 4000.0, -0.1, 0.09, 90.0)


class TestWh254Co2Evitata:
    def test_base(self):
        r = wh254_co2_evitata(1555555.56, 0.201)
        assert r["co2_evitata_t_anno"] == 312.67

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_co2_evitata(-1.0)


class TestWh254BusinessCase:
    def test_conveniente(self):
        r = wh254_business_case(140000.0, 250000.0, 8000.0)
        assert r["flusso_annuo_eur"] == 132000.0
        assert r["payback_mesi"] == 22.7
        assert r["conviene"] is True

    def test_lungo(self):
        r = wh254_business_case(140000.0, 900000.0, 8000.0)
        assert r["payback_mesi"] == 81.8
        assert r["conviene"] is False

    def test_mai(self):
        r = wh254_business_case(5000.0, 250000.0, 8000.0)
        assert r["payback_mesi"] is None
        assert r["conviene"] is False

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_business_case(140000.0, -1.0, 8000.0)


class TestWh254Sensitivita:
    def test_base(self):
        righe = wh254_sensitivita([0.09], [4000.0], 500.0, 70.0, 90.0, 8000.0)
        assert len(righe) == 1
        assert righe[0]["risparmio_netto_annuo_eur"] == 132000.0

    def test_matrice(self):
        righe = wh254_sensitivita([0.05, 0.15], [2000.0, 8000.0], 500.0, 70.0, 90.0, 8000.0)
        assert len(righe) == 4
        mappa = {(r["prezzo_gas_eur_kwh"], r["ore_anno"]): r["risparmio_netto_annuo_eur"]
                 for r in righe}
        assert mappa[(0.05, 2000.0)] == 30888.89
        assert mappa[(0.15, 8000.0)] == 458666.67

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_sensitivita([], [4000.0], 500.0, 70.0, 90.0, 8000.0)

    def test_determinismo(self):
        a = wh254_sensitivita([0.09], [4000.0], 500.0, 70.0, 90.0, 8000.0)
        b = wh254_sensitivita([0.09], [4000.0], 500.0, 70.0, 90.0, 8000.0)
        assert a == b


class TestWh254SensitivitaPdc:
    def test_base(self):
        righe = wh254_sensitivita_pdc([0.09], [4000.0], 200.0, 4.0, 0.18, 90.0, 8000.0)
        assert len(righe) == 1
        assert righe[0]["risparmio_netto_annuo_eur"] == 50666.67

    def test_errori(self):
        with pytest.raises(ValueError):
            wh254_sensitivita_pdc([], [4000.0], 200.0, 4.0, 0.18, 90.0, 8000.0)

    def test_determinismo(self):
        a = wh254_sensitivita_pdc([0.09], [4000.0], 200.0, 4.0, 0.18, 90.0, 8000.0)
        b = wh254_sensitivita_pdc([0.09], [4000.0], 200.0, 4.0, 0.18, 90.0, 8000.0)
        assert a == b
