"""Test calcola_flessibilita_oraria - tab178 (stile pytest, via appfuncs).

Copertura: serie piatta (valore zero), serie vuota (errore pulito),
caso calcolabile a mano (2 ore, raggio 1), quota 0% (zero), parametri
non validi (quota>100, raggio<1, carico nullo, indice non datetime),
NaN-safe, determinismo, profilo 0-23 completo, replica indipendente
del pipeline, registry tab178.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_flessibilita_oraria", "fascia_oraria")
fo = fns["calcola_flessibilita_oraria"]
fascia_oraria = fns["fascia_oraria"]


def serie(vals, start="2026-01-01"):
    idx = pd.date_range(start, periods=len(vals), freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


def quota_manuale(prezzi, mw_f1, mw_f2, mw_f3, quota_pct, raggio):
    """Replica indipendente: carico da fasce + min in finestra."""
    p = prezzi.astype(float).dropna()
    p = p[~p.index.duplicated(keep="first")].sort_index()
    mw_of = {"F1": mw_f1, "F2": mw_f2, "F3": mw_f3}
    carico = np.array([mw_of[x] for x in p.index.map(fascia_oraria)])
    pa = p.to_numpy()
    n = len(p)
    risp = np.zeros(n)
    for i in range(n):
        a, b = max(0, i - raggio), min(n - 1, i + raggio)
        j = a + int(np.argmin(pa[a:b + 1]))
        risp[i] = max(0.0, (pa[i] - pa[j]) * (quota_pct / 100.0 * carico[i]))
    return risp


class TestFlessibilitaOraria:
    def test_serie_piatta_valore_zero(self):
        r = fo(serie([100.0] * 720), 2.0, 2.0, 2.0, 10.0, 6)
        assert r["valido"] and r["errore"] is None
        assert r["risparmio_totale"] == 0.0
        assert r["ore_con_risparmio"] == 0
        assert (r["df_ore"]["Risparmio (EUR)"] == 0.0).all()
        assert (r["df_profilo"]["Risparmio medio (EUR/ora)"] == 0.0).all()

    def test_caso_calcolabile_a_mano(self):
        # ora0=50 (min in finestra), ora1=150: solo ora1 vale 100*(1MW)
        r = fo(serie([50.0, 150.0]), 1.0, 1.0, 1.0, 100.0, 1)
        assert r["valido"]
        assert r["risparmio_totale"] == pytest.approx(100.0)
        df = r["df_ore"]
        assert df["Risparmio (EUR)"].iloc[0] == pytest.approx(0.0)
        assert df["Risparmio (EUR)"].iloc[1] == pytest.approx(100.0)
        assert df["Prezzo destinazione (EUR/MWh)"].iloc[1] == pytest.approx(50.0)
        assert df["Ora destinazione"].iloc[1] == df["Ora"].iloc[0]

    def test_serie_vuota_errore_pulito(self):
        r = fo(pd.Series(dtype=float), 2.0, 2.0, 2.0, 10.0, 6)
        assert not r["valido"] and r["errore"]
        assert r["df_ore"].empty and r["df_profilo"].empty

    def test_quota_zero(self):
        r = fo(serie([80.0, 160.0, 90.0]), 2.0, 2.0, 2.0, 0.0, 1)
        assert r["valido"] and r["risparmio_totale"] == 0.0

    def test_parametri_non_validi(self):
        p = serie([80.0, 120.0])
        assert not fo(p, 2.0, 2.0, 2.0, 101.0, 6)["valido"]       # quota > 100
        assert not fo(p, 2.0, 2.0, 2.0, -1.0, 6)["valido"]        # quota < 0
        assert not fo(p, 2.0, 2.0, 2.0, 10.0, 0)["valido"]        # raggio < 1
        assert not fo(p, 0.0, 0.0, 0.0, 10.0, 6)["valido"]        # carico nullo
        assert not fo(pd.Series([1.0, 2.0]), 2.0, 2.0, 2.0, 10.0, 6)["valido"]  # indice non datetime

    def test_nan_e_duplicati_safe(self):
        idx = pd.to_datetime(["2026-01-01 00", "2026-01-01 01", "2026-01-01 01", "2026-01-01 02"])
        s = pd.Series([100.0, np.nan, 120.0, 90.0], index=idx)
        r = fo(s, 2.0, 2.0, 2.0, 10.0, 1)
        assert r["valido"] and r["n_ore"] == 3

    def test_determinismo(self):
        rng = np.random.default_rng(7)
        p = serie(rng.uniform(40, 180, 500))
        a = fo(p, 2.0, 2.0, 2.0, 15.0, 8)
        b = fo(p, 2.0, 2.0, 2.0, 15.0, 8)
        pd.testing.assert_frame_equal(a["df_ore"], b["df_ore"])
        pd.testing.assert_frame_equal(a["df_profilo"], b["df_profilo"])
        assert a["risparmio_totale"] == b["risparmio_totale"]

    def test_profilo_ore_0_23(self):
        r = fo(serie([100.0] * 168), 2.0, 2.0, 2.0, 10.0, 6)
        assert list(r["df_profilo"]["Ora del giorno"]) == list(range(24))
        assert (r["df_profilo"]["Ore totali"] == 7).all()
        assert 0 <= r["miglior_ora_giorno"] <= 23
        assert 0 <= r["peggior_ora_giorno"] <= 23

    def test_replica_indipendente(self):
        rng = np.random.default_rng(42)
        p = serie(rng.uniform(30, 200, 300))
        r = fo(p, 1.5, 2.5, 1.0, 20.0, 5)
        atteso = quota_manuale(p, 1.5, 2.5, 1.0, 20.0, 5)
        np.testing.assert_allclose(r["df_ore"]["Risparmio (EUR)"].to_numpy(), atteso, rtol=1e-9)
        assert r["risparmio_totale"] == pytest.approx(float(atteso.sum()))
        carico_tot = (p.to_numpy() * np.array([{"F1": 1.5, "F2": 2.5, "F3": 1.0}[x]
                                                for x in p.index.map(fascia_oraria)])).sum()
        assert r["quota_risparmio_pct"] == pytest.approx(r["risparmio_totale"] / carico_tot * 100)

    def test_registry_tab178(self):
        src = Path(__file__).resolve().parent.parent / "app.py"
        txt = src.read_text(encoding="utf-8")
        assert "tab178" in txt
        assert "Flessibilità oraria" in txt
        assert "calcola_flessibilita_oraria" in txt
        assert 'key="fl178_quota"' in txt and 'key="fl178_raggio"' in txt and 'key="fl178_csv"' in txt
