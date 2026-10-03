"""Test calcola_quantili_orari - tab180 (stile pytest, via appfuncs).

Copertura: serie piatta (quantili = valore piatto, bande nulle), caso
calcolabile a mano (2 giorni: quantili esatti per ora), serie vuota
(errore pulito), indice non datetime (errore pulito), parametri non
validi (banda invertita, fuori [0,100], non numerici), NaN e duplicati
(gestiti come nelle altre tab), determinismo, ore 0-23 complete,
riepilogo (ore mediana max/min, ora IQR max, ampiezza media),
registry tab180.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_quantili_orari")
qo = fns["calcola_quantili_orari"]


def serie(vals, start="2026-01-01"):
    idx = pd.date_range(start, periods=len(vals), freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


class TestQuantiliOrari:
    def test_serie_piatta(self):
        r = qo(serie([100.0] * 720))
        assert r["valido"] and r["errore"] is None
        df = r["df_quantili"]
        assert len(df) == 24
        for c in ["P10 (EUR/MWh)", "P25 (EUR/MWh)", "P50 (EUR/MWh)",
                  "P75 (EUR/MWh)", "P90 (EUR/MWh)", "Media (EUR/MWh)"]:
            assert (df[c] == 100.0).all(), c
        assert (df["Ampiezza banda (EUR/MWh)"] == 0.0).all()
        assert r["ampiezza_banda_media"] == pytest.approx(0.0)
        assert (df["N ore"] == 30).all()

    def test_caso_calcolabile_a_mano(self):
        # 2 giorni: ora h ha valori [h, h+10] -> mediana h+5, P10 h+1, P90 h+9
        vals = []
        for _ in range(2):
            vals += [float(h) for h in range(24)]
        base = serie(vals)
        # aggiungo offset al secondo giorno
        idx = base.index
        v = base.to_numpy().copy()
        v[24:] += 10.0
        p = pd.Series(v, index=idx)
        r = qo(p)
        assert r["valido"]
        df = r["df_quantili"].set_index("Ora del giorno")
        for h in range(24):
            assert df.loc[h, "P50 (EUR/MWh)"] == pytest.approx(h + 5.0)
            assert df.loc[h, "P10 (EUR/MWh)"] == pytest.approx(h + 1.0)
            assert df.loc[h, "P90 (EUR/MWh)"] == pytest.approx(h + 9.0)
            assert df.loc[h, "P25 (EUR/MWh)"] == pytest.approx(h + 2.5)
            assert df.loc[h, "P75 (EUR/MWh)"] == pytest.approx(h + 7.5)
            assert df.loc[h, "Min (EUR/MWh)"] == pytest.approx(h)
            assert df.loc[h, "Max (EUR/MWh)"] == pytest.approx(h + 10.0)
        # riepilogo: mediana cresce con h -> max alle 23, min alle 0
        assert r["ora_mediana_max"] == 23
        assert r["ora_mediana_min"] == 0
        # IQR identico per tutte le ore (5.0): prima occorrenza -> ora 0
        assert r["ora_iqr_max"] == 0
        assert r["ampiezza_banda_media"] == pytest.approx(8.0)
        assert r["n_ore"] == 48

    def test_serie_vuota(self):
        r = qo(pd.Series(dtype=float))
        assert not r["valido"] and r["errore"] is not None

    def test_indice_non_datetime(self):
        r = qo(pd.Series([1.0, 2.0, 3.0]))
        assert not r["valido"] and r["errore"] is not None

    def test_banda_invertita(self):
        r = qo(serie([100.0] * 48), q_bassa=90.0, q_alta=10.0)
        assert not r["valido"] and "P_bassa" in r["errore"]

    def test_banda_uguale(self):
        r = qo(serie([100.0] * 48), q_bassa=50.0, q_alta=50.0)
        assert not r["valido"]

    def test_banda_fuori_intervallo(self):
        assert not qo(serie([100.0] * 48), q_bassa=-5.0)["valido"]
        assert not qo(serie([100.0] * 48), q_alta=101.0)["valido"]

    def test_parametri_non_numerici(self):
        assert not qo(serie([100.0] * 48), q_bassa="x")["valido"]

    def test_nan_e_duplicati(self):
        p = serie([100.0] * 48)
        p.iloc[5] = np.nan
        p = pd.concat([p, p.iloc[[10]]])  # duplicato: keep-first
        r = qo(p)
        assert r["valido"]
        assert r["n_ore"] == 47  # NaN scartato, duplicato tenuto una volta
        assert (r["df_quantili"]["P50 (EUR/MWh)"] == 100.0).all()

    def test_determinismo(self):
        rng = np.random.default_rng(7)
        p = serie(rng.uniform(20.0, 250.0, 500))
        a, b = qo(p, 5.0, 95.0), qo(p, 5.0, 95.0)
        pd.testing.assert_frame_equal(a["df_quantili"], b["df_quantili"])
        assert a["ora_mediana_max"] == b["ora_mediana_max"]
        assert a["ora_iqr_max"] == b["ora_iqr_max"]

    def test_banda_custom_colonne(self):
        r = qo(serie([100.0] * 72), q_bassa=5.0, q_alta=95.0)
        assert r["valido"]
        assert r["q_bassa"] == 5.0 and r["q_alta"] == 95.0
        assert "P5 (EUR/MWh)" in r["df_quantili"].columns
        assert "P95 (EUR/MWh)" in r["df_quantili"].columns

    def test_registry_tab180(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "tab180" in src
        assert "with tab180:" in src
        assert "Quantili orari" in src
        assert "calcola_quantili_orari" in src
        assert 'key="qo180_bassa"' in src and 'key="qo180_alta"' in src and 'key="qo180_csv"' in src
