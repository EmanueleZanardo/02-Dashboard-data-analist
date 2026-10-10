"""Test tab185 (stile pytest): CO2 implicita nello spark spread.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_carbonio_implicito")
calcola_carbonio_implicito = _F["calcola_carbonio_implicito"]

TZ = "Europe/Zurich"


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    return pd.Series(np.full(len(idx), prezzo), index=idx, name="p")


class TestCarbonioImplicito:
    def test_piatta_numeri_a_mano(self):
        # P=100, gas=40, HR=2.0, VOM=3, EF=0.202 -> denom=0.404
        # CO2_impl = (100 - 80 - 3) / 0.404 = 42.0792079...
        r = calcola_carbonio_implicito(piatta(2), prezzo_gas_eur_mwh=40.0,
                                      heat_rate=2.0, vom_eur_mwh=3.0,
                                      prezzo_eua_riferimento=75.0)
        assert r["valido"] and r["errore"] is None
        assert r["co2_media"] == pytest.approx(17 / 0.404)
        assert r["co2_mediana"] == pytest.approx(17 / 0.404)
        assert r["co2_p10"] == pytest.approx(17 / 0.404)
        assert r["co2_p90"] == pytest.approx(17 / 0.404)
        # clean spark con EUA a 75: 100 - 80 - 75*0.404 - 3 = -13.3
        assert r["clean_spark_medio"] == pytest.approx(-13.3)
        assert r["ore_con_margine_positivo"] == 0
        assert r["quota_sopra_riferimento_pct"] == pytest.approx(0.0)
        assert r["giudizio"] == "CO2 SOTTO L'EUA"
        assert r["n_ore"] == 48
        assert r["emissioni_t_mwh_e"] == pytest.approx(0.404)
        assert len(r["df_oraria"]) == 48
        assert list(r["df_oraria"].columns) == ["Ora", "Prezzo (EUR/MWh)", "CO2 implicita (EUR/t)"]
        assert len(r["df_mensile"]) == 1  # 2 giorni nello stesso mese
        assert r["df_mensile"]["Ore"].iloc[0] == 48

    def test_heat_rate_custom(self):
        # CCGT 55%: HR=1.82 -> denom=0.36764; (100-72.8-3)/0.36764
        r = calcola_carbonio_implicito(piatta(1), prezzo_gas_eur_mwh=40.0,
                                      heat_rate=1.82, vom_eur_mwh=3.0,
                                      prezzo_eua_riferimento=75.0)
        assert r["valido"]
        assert r["co2_media"] == pytest.approx(24.2 / 0.36764)

    def test_sopra_eua(self):
        # prezzo alto -> implicita sopra il riferimento
        r = calcola_carbonio_implicito(piatta(1, prezzo=200.0),
                                      prezzo_gas_eur_mwh=40.0, heat_rate=2.0,
                                      vom_eur_mwh=3.0, prezzo_eua_riferimento=75.0)
        assert r["valido"]
        assert r["giudizio"] == "CO2 SOPRA L'EUA"
        assert r["quota_sopra_riferimento_pct"] == pytest.approx(100.0)
        assert r["ore_con_margine_positivo"] == 24

    def test_in_linea(self):
        # implicita esattamente all'EUA -> IN LINEA
        # CO2_impl = 75  =>  P = 75*0.404 + 80 + 3 = 113.3
        r = calcola_carbonio_implicito(piatta(1, prezzo=113.3),
                                      prezzo_gas_eur_mwh=40.0, heat_rate=2.0,
                                      vom_eur_mwh=3.0, prezzo_eua_riferimento=75.0)
        assert r["valido"]
        assert r["co2_mediana"] == pytest.approx(75.0)
        assert r["giudizio"] == "IN LINEA"

    def test_serie_vuota(self):
        s = pd.Series([], dtype=float,
                      index=pd.DatetimeIndex([], tz=TZ))
        r = calcola_carbonio_implicito(s)
        assert not r["valido"] and r["errore"]

    def test_non_series(self):
        r = calcola_carbonio_implicito([100.0] * 24)
        assert not r["valido"] and r["errore"]

    def test_parametri_non_validi(self):
        p = piatta(1)
        assert not calcola_carbonio_implicito(p, heat_rate=0.5)["valido"]
        assert not calcola_carbonio_implicito(p, heat_rate=6.0)["valido"]
        assert not calcola_carbonio_implicito(p, prezzo_gas_eur_mwh=-1.0)["valido"]
        assert not calcola_carbonio_implicito(p, vom_eur_mwh=-0.5)["valido"]
        assert not calcola_carbonio_implicito(p, fattore_emissione_t_mwh_th=0.0)["valido"]
        assert not calcola_carbonio_implicito(p, prezzo_eua_riferimento=-5.0)["valido"]
        assert not calcola_carbonio_implicito(p, heat_rate=True)["valido"]

    def test_nan_e_tz(self):
        s = piatta(2)
        s.iloc[5] = np.nan
        s.iloc[10] = np.nan
        r = calcola_carbonio_implicito(s)
        assert r["valido"] and r["n_ore"] == 46
        # indice naive
        s2 = piatta(1)
        s2.index = s2.index.tz_localize(None)
        r2 = calcola_carbonio_implicito(s2)
        assert r2["valido"] and r2["n_ore"] == 24

    def test_determinismo(self):
        p = piatta(3, prezzo=87.5)
        a = calcola_carbonio_implicito(p, prezzo_gas_eur_mwh=33.0)
        b = calcola_carbonio_implicito(p, prezzo_gas_eur_mwh=33.0)
        assert a["co2_media"] == b["co2_media"]
        assert a["giudizio"] == b["giudizio"]
        pd.testing.assert_frame_equal(a["df_oraria"], b["df_oraria"])


class TestRegistryTab185:
    def test_tab185_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab185" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab185" in withs
        assert len(withs) == len(dvars) == 357
        assert '"💨 CO₂ implicita"' in src
        assert "calcola_carbonio_implicito" in src
        keys = re.findall(r'key="(co2i185_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 6
