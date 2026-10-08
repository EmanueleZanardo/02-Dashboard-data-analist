"""Test tab190 (stile pytest): curtailment economico di un impianto rinnovabile.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Numeri a mano (profilo "piatto", potenza 10 MW, costo marginale 2 EUR/MWh):
  T1: 24h piatte a 100, soglia 0 -> nessuna ora sotto soglia: ore 0,
      MWh potenziali 240, curtailati 0, beneficio 0,
      profitto_senza = 240*100 - 240*2 = 23520, cattura 100,
      giudizio "NON NECESSARIO".
  T2: 6h a -50 + 18h a 100, soglia 0 -> 6 ore curtailate, 60 MWh (25%),
      ricavo_senza = 6*(-50)*10 + 18*100*10 = 15000,
      profitto_senza = 15000 - 480 = 14520,
      profitto_con = 18000 - 360 = 17640, beneficio = 3120,
      cattura_senza = 62.5, cattura_con = 100.0,
      O&M risparmiati = 120, giudizio "CONSIGLIATO".
  T3: 24h piatte a 100, soglia 150 -> tutto curtailato: 240 MWh, 0 consegnati,
      beneficio = -(240*(100-2)) = -23520, cattura_con = 0,
      giudizio "SOGLIA TROPPO ALTA".
  T4: 12h a 1.0 + 12h a 10.0, soglia = costo_marginale = 2 -> 12 ore curtailate,
      beneficio = -12*(1-2)*10 = 120 > 0, quota 50% -> "CONSIGLIATO".
  T5: 199h a 100 + 1h a -10, soglia 0 -> 1 ora curtailata, 10 MWh su 2000
      (quota 0.5% < 1%), beneficio = -((-10-2)*10) = 120 > 0 -> "MARGINALE".
  T6: prezzo == soglia (24h a 0, soglia 0) -> confronto stretto: nessuna ora
      curtailata, "NON NECESSARIO".
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_curtailment")
calcola_curtailment = _F["calcola_curtailment"]

TZ = "Europe/Zurich"

KW = dict(potenza_mw=10.0, profilo="piatto",
          soglia_curtailment=0.0, costo_marginale=2.0)


def serie(prezzi, start="2026-09-28", tz=TZ):
    idx = pd.date_range(start, periods=len(prezzi), freq="h", tz=tz)
    return pd.Series(np.asarray(prezzi, dtype=float), index=idx, name="p")


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    return serie([prezzo] * (giorni * 24), start=start)


class TestPiatta:
    def test_nessun_curtailment(self):
        r = calcola_curtailment(piatta(1), **KW)
        assert r["valido"]
        assert r["ore_curtailment"] == 0
        assert r["mwh_potenziali"] == pytest.approx(240.0)
        assert r["mwh_curtailed"] == pytest.approx(0.0)
        assert r["mwh_consegnati"] == pytest.approx(240.0)
        assert r["quota_curtailment_pct"] == pytest.approx(0.0)
        assert r["beneficio_eur"] == pytest.approx(0.0)
        assert r["profitto_senza_eur"] == pytest.approx(23520.0)
        assert r["profitto_con_eur"] == pytest.approx(23520.0)
        assert r["cattura_senza_eur_mwh"] == pytest.approx(100.0)
        assert r["cattura_con_eur_mwh"] == pytest.approx(100.0)
        assert r["giudizio"] == "NON NECESSARIO"

    def test_prezzi_negativi(self):
        s = serie([-50.0] * 6 + [100.0] * 18)
        r = calcola_curtailment(s, **KW)
        assert r["valido"]
        assert r["ore_curtailment"] == 6
        assert r["mwh_curtailed"] == pytest.approx(60.0)
        assert r["mwh_consegnati"] == pytest.approx(180.0)
        assert r["quota_curtailment_pct"] == pytest.approx(25.0)
        assert r["ricavo_senza_eur"] == pytest.approx(15000.0)
        assert r["profitto_senza_eur"] == pytest.approx(14520.0)
        assert r["profitto_con_eur"] == pytest.approx(17640.0)
        assert r["beneficio_eur"] == pytest.approx(3120.0)
        assert r["onm_risparmiati_eur"] == pytest.approx(120.0)
        assert r["cattura_senza_eur_mwh"] == pytest.approx(62.5)
        assert r["cattura_con_eur_mwh"] == pytest.approx(100.0)
        assert r["giudizio"] == "CONSIGLIATO"

    def test_soglia_troppo_alta(self):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo="piatto",
                                soglia_curtailment=150.0, costo_marginale=2.0)
        assert r["valido"]
        assert r["ore_curtailment"] == 24
        assert r["mwh_curtailed"] == pytest.approx(240.0)
        assert r["mwh_consegnati"] == pytest.approx(0.0)
        assert r["beneficio_eur"] == pytest.approx(-23520.0)
        assert r["cattura_con_eur_mwh"] == pytest.approx(0.0)
        assert r["giudizio"] == "SOGLIA TROPPO ALTA"

    def test_soglia_uguale_costo_marginale(self):
        s = serie([1.0] * 12 + [10.0] * 12)
        r = calcola_curtailment(s, potenza_mw=10.0, profilo="piatto",
                                soglia_curtailment=2.0, costo_marginale=2.0)
        assert r["valido"]
        assert r["ore_curtailment"] == 12
        assert r["beneficio_eur"] == pytest.approx(120.0)
        assert r["quota_curtailment_pct"] == pytest.approx(50.0)
        assert r["giudizio"] == "CONSIGLIATO"

    def test_marginale_quota_bassa(self):
        s = serie([100.0] * 199 + [-10.0])
        r = calcola_curtailment(s, **KW)
        assert r["valido"]
        assert r["ore_curtailment"] == 1
        assert r["mwh_curtailed"] == pytest.approx(10.0)
        assert r["quota_curtailment_pct"] == pytest.approx(0.5)
        assert r["beneficio_eur"] == pytest.approx(120.0)
        assert r["giudizio"] == "MARGINALE"

    def test_boundary_spot_uguale_soglia(self):
        r = calcola_curtailment(piatta(1, prezzo=0.0), **KW)
        assert r["valido"]
        assert r["ore_curtailment"] == 0  # confronto stretto: spot < soglia
        assert r["giudizio"] == "NON NECESSARIO"


class TestProfili:
    def test_solare_notte_zero(self):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo="solare",
                                soglia_curtailment=0.0, costo_marginale=2.0)
        assert r["valido"]
        assert 0.0 < r["mwh_potenziali"] < 240.0
        assert r["ore_curtailment"] == 0

    def test_solare_deterministico(self):
        a = calcola_curtailment(piatta(2), potenza_mw=5.0, profilo="solare",
                                soglia_curtailment=0.0, costo_marginale=1.0)
        b = calcola_curtailment(piatta(2), potenza_mw=5.0, profilo="solare",
                                soglia_curtailment=0.0, costo_marginale=1.0)
        assert a["mwh_potenziali"] == pytest.approx(b["mwh_potenziali"])

    def test_eolico_deterministico(self):
        kw = dict(potenza_mw=10.0, profilo="eolico",
                  soglia_curtailment=0.0, costo_marginale=2.0)
        a = calcola_curtailment(piatta(3), **kw)
        b = calcola_curtailment(piatta(3), **kw)
        assert a["valido"] and b["valido"]
        assert a["mwh_potenziali"] == pytest.approx(b["mwh_potenziali"])
        assert a["beneficio_eur"] == pytest.approx(b["beneficio_eur"])

    def test_eolico_seed_diverso(self):
        kw = dict(potenza_mw=10.0, profilo="eolico",
                  soglia_curtailment=0.0, costo_marginale=2.0)
        a = calcola_curtailment(piatta(3), **kw)
        c = calcola_curtailment(piatta(3), seed=191, **kw)
        assert abs(a["mwh_potenziali"] - c["mwh_potenziali"]) > 1e-9

    def test_eolico_range(self):
        # fattore di capacita' eolico sempre in [0.05, 0.95]: con prezzo
        # piatto a 100 e soglia 0, i MWh potenziali restano nel range
        r = calcola_curtailment(piatta(2), potenza_mw=10.0, profilo="eolico",
                                soglia_curtailment=0.0, costo_marginale=2.0)
        assert 0.05 * 10 * 48 <= r["mwh_potenziali"] <= 0.95 * 10 * 48


class TestDataframe:
    def test_coerenza_df(self):
        s = serie([-50.0] * 6 + [100.0] * 18)
        r = calcola_curtailment(s, **KW)
        df_g = r["df_giornaliera"]
        assert df_g["MWh curtailati"].sum() == pytest.approx(r["mwh_curtailed"])
        assert df_g["MWh potenziali"].sum() == pytest.approx(r["mwh_potenziali"])
        assert df_g["Beneficio (EUR)"].sum() == pytest.approx(r["beneficio_eur"])
        df_m = r["df_mensile"]
        assert df_m["Beneficio (EUR)"].sum() == pytest.approx(r["beneficio_eur"])
        assert df_m["Beneficio cumulato (EUR)"].iloc[-1] == pytest.approx(r["beneficio_eur"])
        assert (df_g["Quota curtailment %"] >= 0).all()

    def test_due_giorni(self):
        s = serie([-50.0] * 6 + [100.0] * 18 + [100.0] * 24)
        r = calcola_curtailment(s, **KW)
        assert len(r["df_giornaliera"]) == 2
        assert r["df_giornaliera"]["MWh curtailati"].iloc[1] == pytest.approx(0.0)


class TestErrori:
    @pytest.mark.parametrize("pmw", [0, -1, "x", None, True, float("nan")])
    def test_potenza_invalida(self, pmw):
        r = calcola_curtailment(piatta(1), potenza_mw=pmw, profilo="piatto",
                                soglia_curtailment=0.0, costo_marginale=2.0)
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("prof", ["nucleare", "", 123, None, True])
    def test_profilo_invalido(self, prof):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo=prof,
                                soglia_curtailment=0.0, costo_marginale=2.0)
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("soglia", ["x", None, True, float("nan")])
    def test_soglia_invalida(self, soglia):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo="piatto",
                                soglia_curtailment=soglia, costo_marginale=2.0)
        assert not r["valido"] and r["errore"]

    def test_soglia_negativa_valida(self):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo="piatto",
                                soglia_curtailment=-5.0, costo_marginale=2.0)
        assert r["valido"] and r["ore_curtailment"] == 0

    @pytest.mark.parametrize("cm", [-1, "x", None, True, float("nan")])
    def test_costo_marginale_invalido(self, cm):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo="piatto",
                                soglia_curtailment=0.0, costo_marginale=cm)
        assert not r["valido"] and r["errore"]

    def test_seed_bool_invalido(self):
        r = calcola_curtailment(piatta(1), potenza_mw=10.0, profilo="eolico",
                                soglia_curtailment=0.0, costo_marginale=2.0,
                                seed=True)
        assert not r["valido"] and r["errore"]

    def test_non_series(self):
        r = calcola_curtailment([100.0] * 24, **KW)
        assert not r["valido"] and r["errore"]

    def test_serie_vuota(self):
        r = calcola_curtailment(pd.Series([], dtype=float), **KW)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0] * 24, index=["ora-%d" % i for i in range(24)])
        r = calcola_curtailment(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_tutti_nan(self):
        s = piatta(1).copy()
        s[:] = np.nan
        r = calcola_curtailment(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_nan_tz_duplicati(self):
        idx = pd.date_range("2026-09-28", periods=25, freq="h", tz=TZ)
        vals = np.full(25, 100.0)
        vals[3] = np.nan
        s = pd.Series(vals, index=idx)
        s = pd.concat([s, s.iloc[[10]]])  # duplicato
        r = calcola_curtailment(s, **KW)
        assert r["valido"]
        assert r["n_ore"] == 24  # 25 - 1 NaN - 1 duplicato
        assert r["profitto_senza_eur"] == pytest.approx(23520.0, rel=1e-9)


class TestRegistryTab190:
    def test_tab190_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab190" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab190" in withs
        assert len(withs) == len(dvars) == 319
        assert '"⏸️ Curtailment rinnovabile"' in src
        assert "calcola_curtailment" in src
        keys = re.findall(r'key="(cur190_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 5
