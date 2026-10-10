"""Test tab189 (stile pytest): cogenerazione (CHP).

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Numeri a mano (1 giorno piatto a 100 EUR/MWh, params KW):
  eta_e=0.4, eta_t=0.45, gas=40, co2=80, EF=0.202, calore=50
  costo_fuel_e = (40 + 80*0.202)/0.4 = 56.16/0.4 = 140.40 EUR/MWh_e
  credito_termico_e = (0.45/0.4)*50 = 56.25 EUR/MWh_e
  strike = 140.40 - 56.25 = 84.15 EUR/MWh_e  -> 100 > 84.15: marcia sempre
  margine_h = (100 - 84.15)*1.0 = 15.85 EUR -> totale 24*15.85 = 380.40 EUR
  MWh_e = 24, MWh_t = 24*1.125 = 27.0, MWh_fuel = 24/0.4 = 60.0
  ricavo 2400 - fuel 3369.6 + calore 1350 = 380.4 (bilancio economico)
  PES = 1 - 1/(0.4/0.525 + 0.45/0.9) = 20.7547% >= 10% -> CAR
  clean_spark_medio = 100 - 140.4 = -40.4 (negativo: il credito termico
  e' decisivo), CF 100% -> "MOLTO REDDITIZIO".
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_cogenerazione")
calcola_cogenerazione = _F["calcola_cogenerazione"]

TZ = "Europe/Zurich"

KW = dict(potenza_mw=1.0, rend_elettrico=0.4, rend_termico=0.45,
          prezzo_gas=40.0, prezzo_co2=80.0, fattore_emissione=0.202,
          valore_calore=50.0, eta_e_ref=0.525, eta_t_ref=0.90)

STRIKE = 84.15
PES_ATTESO = 20.75471698


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    return pd.Series(np.full(len(idx), prezzo), index=idx, name="p")


def mix(ore_alte, prezzo_alto=100.0, prezzo_basso=50.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=24, freq="h", tz=TZ)
    vals = np.array([prezzo_alto] * ore_alte + [prezzo_basso] * (24 - ore_alte))
    return pd.Series(vals, index=idx, name="p")


class TestNumeriAMano:
    def test_strike(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        assert r["valido"]
        assert r["prezzo_strike"] == pytest.approx(STRIKE, rel=1e-9)

    def test_marcia_e_margine_24h(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        assert r["ore_funzionamento"] == 24
        assert r["fattore_carico_pct"] == pytest.approx(100.0)
        assert r["margine_totale_eur"] == pytest.approx(24 * 15.85, rel=1e-9)
        assert r["margine_medio_eur_mwh"] == pytest.approx(15.85, rel=1e-9)

    def test_bilanci_energetici(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        assert r["mwh_elettrici"] == pytest.approx(24.0)
        assert r["mwh_termici"] == pytest.approx(27.0)
        assert r["mwh_fuel"] == pytest.approx(60.0)

    def test_bilancio_economico(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        atteso = (r["ricavo_elettrico_eur"] - r["costo_fuel_eur"]
                  + r["valore_calore_eur"])
        assert r["margine_totale_eur"] == pytest.approx(atteso, rel=1e-9)
        assert r["ricavo_elettrico_eur"] == pytest.approx(2400.0)
        assert r["costo_fuel_eur"] == pytest.approx(140.4 * 24, rel=1e-9)
        assert r["valore_calore_eur"] == pytest.approx(56.25 * 24, rel=1e-9)

    def test_pes_e_car(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        assert r["pes_pct"] == pytest.approx(PES_ATTESO, rel=1e-6)
        assert r["qualifica_car"] is True

    def test_clean_spark_negativo(self):
        # senza credito termico lo spark spread sarebbe negativo:
        # e' il calore a rendere l'impianto economico
        r = calcola_cogenerazione(piatta(1), **KW)
        assert r["clean_spark_medio_eur_mwh"] == pytest.approx(-40.4, rel=1e-9)
        assert r["margine_totale_eur"] > 0

    def test_giudizio_molto_redditizio(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        assert r["giudizio"] == "MOLTO REDDITIZIO"

    def test_fermo_sotto_strike(self):
        r = calcola_cogenerazione(piatta(1, prezzo=50.0), **KW)
        assert r["valido"]
        assert r["ore_funzionamento"] == 0
        assert r["margine_totale_eur"] == pytest.approx(0.0)
        assert r["mwh_elettrici"] == pytest.approx(0.0)
        assert r["fattore_carico_pct"] == pytest.approx(0.0)
        assert r["giudizio"] == "IN PERDITA"
        assert r["margine_medio_eur_mwh"] == pytest.approx(0.0)
        assert r["clean_spark_medio_eur_mwh"] == pytest.approx(0.0)

    def test_strike_uguale_spot_non_marcia(self):
        # dispatch con > stretto: spot == strike effettivo -> fermo
        strike_eff = calcola_cogenerazione(
            piatta(1, prezzo=0.0), **KW)["prezzo_strike"]
        r = calcola_cogenerazione(piatta(1, prezzo=strike_eff), **KW)
        assert r["ore_funzionamento"] == 0
        assert r["margine_totale_eur"] == pytest.approx(0.0)


class TestSoglieGiudizio:
    def test_cf_50_molto_redditizio(self):
        r = calcola_cogenerazione(mix(12), **KW)
        assert r["ore_funzionamento"] == 12
        assert r["fattore_carico_pct"] == pytest.approx(50.0)
        assert r["margine_totale_eur"] == pytest.approx(12 * 15.85, rel=1e-9)
        assert r["giudizio"] == "MOLTO REDDITIZIO"

    def test_cf_25_redditizio(self):
        r = calcola_cogenerazione(mix(6), **KW)
        assert r["fattore_carico_pct"] == pytest.approx(25.0)
        assert r["giudizio"] == "REDDITIZIO"

    def test_cf_basso_marginale(self):
        r = calcola_cogenerazione(mix(5), **KW)
        assert r["fattore_carico_pct"] == pytest.approx(500.0 / 24, rel=1e-9)
        assert r["giudizio"] == "MARGINALE"

    def test_car_mancata_con_rendimenti_bassi(self):
        kw = dict(KW, rend_elettrico=0.30, rend_termico=0.20)
        r = calcola_cogenerazione(piatta(1, prezzo=200.0), **kw)
        # PES = 1 - 1/(0.3/0.525 + 0.2/0.9) < 10%
        assert r["pes_pct"] < 10.0
        assert r["qualifica_car"] is False
        assert r["valido"]


class TestAggregazioni:
    def test_df_giornaliera_coerente(self):
        r = calcola_cogenerazione(piatta(3), **KW)
        df = r["df_giornaliera"]
        assert len(df) == 3
        assert df["Margine (EUR)"].sum() == pytest.approx(
            r["margine_totale_eur"], rel=1e-9)
        assert df["MWh elettrici"].sum() == pytest.approx(
            r["mwh_elettrici"], rel=1e-9)
        assert df["MWh termici"].sum() == pytest.approx(
            r["mwh_termici"], rel=1e-9)
        assert df["Ore funzionamento"].sum() == r["ore_funzionamento"]
        assert r["n_giorni"] == 3

    def test_df_mensile_cumulato(self):
        r = calcola_cogenerazione(piatta(40), **KW)
        df = r["df_mensile"]
        assert df["Margine (EUR)"].sum() == pytest.approx(
            r["margine_totale_eur"], rel=1e-9)
        assert df["Margine cumulato (EUR)"].iloc[-1] == pytest.approx(
            r["margine_totale_eur"], rel=1e-9)
        assert (df["Margine cumulato (EUR)"].diff().dropna() >= 0).all()

    def test_verdetto_contiene_strike_e_car(self):
        r = calcola_cogenerazione(piatta(1), **KW)
        assert "84.15" in r["verdetto"]
        assert "CAR" in r["verdetto"]

    def test_determinismo(self):
        a = calcola_cogenerazione(piatta(10), **KW)
        b = calcola_cogenerazione(piatta(10), **KW)
        assert a["margine_totale_eur"] == b["margine_totale_eur"]
        assert a["df_giornaliera"].equals(b["df_giornaliera"])


class TestErrori:
    @pytest.mark.parametrize("k,v", [
        ("potenza_mw", 0.0), ("potenza_mw", -1.0), ("potenza_mw", True),
        ("rend_elettrico", 0.0), ("rend_elettrico", 1.5),
        ("rend_termico", -0.1), ("rend_termico", 1.2),
        ("prezzo_gas", -1.0), ("prezzo_co2", -5.0),
        ("fattore_emissione", -0.1), ("fattore_emissione", 2.5),
        ("valore_calore", -1.0), ("eta_e_ref", 0.0), ("eta_t_ref", 0.0),
        ("potenza_mw", "x"),
    ])
    def test_parametri_invalidi(self, k, v):
        kw = dict(KW)
        kw[k] = v
        r = calcola_cogenerazione(piatta(1), **kw)
        assert not r["valido"] and r["errore"]

    def test_somma_rendimenti_troppo_alta(self):
        r = calcola_cogenerazione(
            piatta(1), **dict(KW, rend_elettrico=0.6, rend_termico=0.5))
        assert not r["valido"] and r["errore"]

    def test_serie_vuota(self):
        r = calcola_cogenerazione(pd.Series([], dtype=float), **KW)
        assert not r["valido"]

    def test_non_series(self):
        r = calcola_cogenerazione([100.0] * 24, **KW)
        assert not r["valido"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0] * 48, index=["ora-%d" % i for i in range(48)])
        r = calcola_cogenerazione(s, **KW)
        assert not r["valido"]

    def test_nan_e_tz_e_duplicati(self):
        idx = pd.date_range("2026-09-28", periods=25, freq="h", tz=TZ)
        vals = np.full(25, 100.0)
        vals[3] = np.nan
        s = pd.Series(vals, index=idx)
        s = pd.concat([s, s.iloc[[10]]])  # duplicato
        r = calcola_cogenerazione(s, **KW)
        assert r["valido"]
        assert r["n_ore"] == 24  # 25 - 1 NaN - 1 duplicato
        assert r["margine_totale_eur"] == pytest.approx(24 * 15.85, rel=1e-9)


class TestRegistryTab189:
    def test_tab189_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab189" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab189" in withs
        assert len(withs) == len(dvars) == 369
        assert '"⚡🔥 Cogenerazione (CHP)"' in src
        assert "calcola_cogenerazione" in src
        keys = re.findall(r'key="(chp189_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 8
