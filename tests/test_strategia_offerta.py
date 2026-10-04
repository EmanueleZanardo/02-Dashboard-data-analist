"""Test tab191 (stile pytest): strategia di offerta di vendita sul day-ahead.

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Numeri a mano (potenza 5 MW):
  T1: 24h piatte a 100, cm=45, quota_volume=90 -> politica "margine":
      bid=45 tutte le ore, quota 100%, marg_giorno = 5*24*(100-45) = 6600,
      margine periodo = 6600 (1 giorno), cattura 100,
      giudizio "STRATEGIA CONSIGLIATA".
      "volume": bid = quantile(flat, 0.10) = 100, quota 100%, stesso margine.
      "prezzo": bid = mediana = 100, quota 100%, stesso margine.
      "mercato": marg_giorno = 6600, quota 100%, cattura 100.
      frontiera: grid ridotta a un punto (100) -> margine 6600, quota 100.
  T2: 12h a 1 (ore 0-11) + 12h a 10 (ore 12-23), cm=5:
      "margine": ore 0-11 non clearate (1 < 5), ore 12-23 clearate con
      margine 5: marg_giorno = 5*12*5 = 300; MWh venduti = 5*12 = 60 su
      120 potenziali -> quota 50%; cattura = 10.0;
      giudizio "STRATEGIA CONSIGLIATA" (quota >= 50%).
      "mercato": marg_giorno = 5*((1-5)*12 + (10-5)*12) = 5*(-48+60) = 60,
      cattura = (12*1+12*10)/24 = 5.5.
      "volume" (90%): ore 0-11 bid=quantile([1],0.1)=1 -> clearate in
      perdita (-4/MWh); ore 12-23 bid=10 -> clearate (+5/MWh):
      marg_giorno = 5*(12*(-4)+12*5) = 60, quota 100%.
  T3: 24h piatte a 1, cm=5 -> margine atteso 0 -> "NON CONVENIENTE".
  T4: 20h a 100 + 4h a 1, cm=5 -> ore clearate 20/24 (83%): quota >= 50
      -> "STRATEGIA CONSIGLIATA"; marg_giorno = 5*20*95 = 9500.
  T5: 2h a 100 + 22h a 1, cm=5 -> quota 2/24 = 8.3% < 10%,
      marg_giorno = 5*2*95 = 950 > 0 -> "MERCATO DIFFICILE".
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_strategia_offerta")
calcola_strategia_offerta = _F["calcola_strategia_offerta"]

TZ = "Europe/Zurich"

KW = dict(potenza_mw=5.0, costo_marginale=45.0, quota_volume=90.0)


def serie(prezzi, start="2026-09-28", tz=TZ):
    idx = pd.date_range(start, periods=len(prezzi), freq="h", tz=tz)
    return pd.Series(np.asarray(prezzi, dtype=float), index=idx, name="p")


class TestCasiBase:
    def test_piatta_margine(self):
        r = calcola_strategia_offerta(serie([100.0] * 24), **KW)
        assert r["valido"] and r["errore"] is None
        p = r["politiche"]["margine"]
        assert (p["bids_orari"] == 45.0).all()
        assert p["quota_venduta_pct"] == pytest.approx(100.0)
        assert p["marg_giorno_eur"] == pytest.approx(6600.0, rel=1e-9)
        assert p["margine_atteso_eur"] == pytest.approx(6600.0, rel=1e-9)
        assert p["cattura_eur_mwh"] == pytest.approx(100.0)
        assert p["mwh_venduti_attesi"] == pytest.approx(120.0)
        assert r["giudizio"] == "STRATEGIA CONSIGLIATA"
        assert r["n_ore"] == 24 and r["n_giorni"] == pytest.approx(1.0)

    def test_piatta_altre_politiche(self):
        r = calcola_strategia_offerta(serie([100.0] * 24), **KW)
        for nome in ("volume", "prezzo"):
            p = r["politiche"][nome]
            assert (p["bids_orari"] == 100.0).all()
            assert p["quota_venduta_pct"] == pytest.approx(100.0)
            assert p["marg_giorno_eur"] == pytest.approx(6600.0, rel=1e-9)
        m = r["politiche"]["mercato"]
        assert m["quota_venduta_pct"] == pytest.approx(100.0)
        assert m["marg_giorno_eur"] == pytest.approx(6600.0, rel=1e-9)
        assert m["cattura_eur_mwh"] == pytest.approx(100.0)

    def test_piatta_frontiera_un_punto(self):
        r = calcola_strategia_offerta(serie([100.0] * 24), **KW)
        df = r["df_frontiera"]
        assert len(df) == 1  # grid ridotta a un unico quantile
        assert df["Bid (EUR/MWh)"].iloc[0] == pytest.approx(100.0)
        assert df["Margine atteso/giorno (EUR)"].iloc[0] == pytest.approx(6600.0)
        assert df["Quota venduta %"].iloc[0] == pytest.approx(100.0)

    def test_due_livelli(self):
        prezzi = [1.0] * 12 + [10.0] * 12
        r = calcola_strategia_offerta(serie(prezzi), potenza_mw=5.0,
                                     costo_marginale=5.0, quota_volume=90.0)
        p = r["politiche"]["margine"]
        assert (p["bids_orari"] == 5.0).all()
        assert p["quota_venduta_pct"] == pytest.approx(50.0)
        assert p["marg_giorno_eur"] == pytest.approx(300.0, rel=1e-9)
        assert p["margine_atteso_eur"] == pytest.approx(300.0, rel=1e-9)
        assert p["cattura_eur_mwh"] == pytest.approx(10.0)
        assert p["mwh_venduti_attesi"] == pytest.approx(60.0)
        assert r["giudizio"] == "STRATEGIA CONSIGLIATA"
        m = r["politiche"]["mercato"]
        assert m["marg_giorno_eur"] == pytest.approx(60.0, rel=1e-9)
        assert m["cattura_eur_mwh"] == pytest.approx(5.5)
        v = r["politiche"]["volume"]
        assert v["quota_venduta_pct"] == pytest.approx(100.0)
        assert v["marg_giorno_eur"] == pytest.approx(60.0, rel=1e-9)

    def test_non_conveniente(self):
        r = calcola_strategia_offerta(serie([1.0] * 24), **KW)
        assert r["valido"]
        assert r["politiche"]["margine"]["marg_giorno_eur"] == pytest.approx(0.0)
        assert r["politiche"]["margine"]["quota_venduta_pct"] == pytest.approx(0.0)
        assert r["giudizio"] == "NON CONVENIENTE"

    def test_mercato_difficile(self):
        prezzi = [100.0] * 2 + [1.0] * 22
        r = calcola_strategia_offerta(serie(prezzi), potenza_mw=5.0,
                                     costo_marginale=5.0, quota_volume=90.0)
        p = r["politiche"]["margine"]
        assert p["quota_venduta_pct"] == pytest.approx(100.0 * 2 / 24)
        assert p["marg_giorno_eur"] == pytest.approx(950.0, rel=1e-9)
        assert r["giudizio"] == "MERCATO DIFFICILE"

    def test_oraria_e_mensile_coerenti(self):
        prezzi = [1.0] * 12 + [10.0] * 12
        r = calcola_strategia_offerta(serie(prezzi), potenza_mw=5.0,
                                     costo_marginale=5.0, quota_volume=90.0)
        df_o = r["df_oraria"]
        assert len(df_o) == 24
        assert df_o["Bid margine"].eq(5.0).all()
        assert (df_o.loc[df_o["Ora"] < 12, "Quota margine %"] == 0.0).all()
        assert (df_o.loc[df_o["Ora"] >= 12, "Quota margine %"] == 100.0).all()
        assert df_o["Margine/giorno margine (EUR)"].sum() == pytest.approx(300.0, rel=1e-9)
        df_m = r["df_mensile"]
        assert len(df_m) == 1
        assert df_m["Margine margine (EUR)"].iloc[0] == pytest.approx(
            r["politiche"]["margine"]["margine_atteso_eur"], rel=1e-9)
        assert df_m["Quota margine %"].iloc[0] == pytest.approx(
            r["politiche"]["margine"]["quota_venduta_pct"], rel=1e-9)

    def test_frontiera_monotona(self):
        rng = np.random.default_rng(191)
        prezzi = rng.uniform(-20, 200, 24 * 30)
        r = calcola_strategia_offerta(serie(prezzi), potenza_mw=5.0,
                                     costo_marginale=45.0, quota_volume=90.0)
        df = r["df_frontiera"].sort_values("Bid (EUR/MWh)")
        assert (df["Quota venduta %"].diff().dropna() <= 1e-9).all()
        # il margine cresce fino al costo marginale (sotto cm si vende in
        # perdita) e poi decresce: monotono solo per bid >= cm
        sopra = df[df["Bid (EUR/MWh)"] >= 45.0]
        assert (sopra["Margine atteso/giorno (EUR)"].diff().dropna() <= 1e-9).all()
        # il massimo sulla griglia e' su uno dei due punti che
        # abbracciano il costo marginale (l'ottimo teorico e' b = cm)
        bmax = float(df.loc[df["Margine atteso/giorno (EUR)"].idxmax(),
                            "Bid (EUR/MWh)"])
        sotto_cm = df[df["Bid (EUR/MWh)"] <= 45.0]["Bid (EUR/MWh)"]
        sopra_cm = df[df["Bid (EUR/MWh)"] >= 45.0]["Bid (EUR/MWh)"]
        assert bmax in (float(sotto_cm.max()), float(sopra_cm.min()))
        # il punto ottimo della politica "margine" non sta sotto la frontiera
        # uniforme valutata al costo marginale
        pm = r["politiche"]["margine"]
        riga = df.iloc[(df["Bid (EUR/MWh)"] - 45.0).abs().argsort()[:1]]
        assert pm["marg_giorno_eur"] >= float(riga["Margine atteso/giorno (EUR)"].iloc[0]) - 1e-6

    def test_determinismo(self):
        rng = np.random.default_rng(7)
        prezzi = rng.uniform(0, 150, 24 * 10)
        s = serie(prezzi)
        r1 = calcola_strategia_offerta(s, **KW)
        r2 = calcola_strategia_offerta(s, **KW)
        assert r1["politiche"]["margine"]["margine_atteso_eur"] == \
            r2["politiche"]["margine"]["margine_atteso_eur"]
        assert r1["giudizio"] == r2["giudizio"]
        assert (r1["politiche"]["volume"]["bids_orari"] ==
                r2["politiche"]["volume"]["bids_orari"]).all()


class TestRobustezza:
    def test_serie_vuota(self):
        s = pd.Series([], dtype=float,
                      index=pd.DatetimeIndex([], tz=TZ), name="p")
        r = calcola_strategia_offerta(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_non_series(self):
        r = calcola_strategia_offerta([100.0] * 24, **KW)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0] * 24,
                      index=["ora-%d" % i for i in range(24)])  # non parsabili
        r = calcola_strategia_offerta(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_tutti_nan(self):
        s = serie([np.nan] * 24)
        r = calcola_strategia_offerta(s, **KW)
        assert not r["valido"] and r["errore"]

    def test_nan_tz_duplicati(self):
        idx = pd.date_range("2026-09-28", periods=25, freq="h", tz=TZ)
        vals = np.full(25, 100.0)
        vals[3] = np.nan
        s = pd.Series(vals, index=idx)
        s = pd.concat([s, s.iloc[[10]]])  # duplicato
        r = calcola_strategia_offerta(s, **KW)
        assert r["valido"]
        assert r["n_ore"] == 24  # 25 - 1 NaN - 1 duplicato
        # ora 3 senza istanze, ora 10 con due: marg_giorno = 5*23*55
        assert r["politiche"]["margine"]["marg_giorno_eur"] == pytest.approx(6325.0, rel=1e-9)

    @pytest.mark.parametrize("kw", [
        dict(potenza_mw=0.0), dict(potenza_mw=-3.0), dict(potenza_mw=True),
        dict(potenza_mw="x"), dict(costo_marginale="x"),
        dict(quota_volume=0.0), dict(quota_volume=101.0),
        dict(quota_volume=True), dict(n_punti=5), dict(n_punti=1000),
        dict(n_punti=True), dict(n_punti="x"),
    ])
    def test_parametri_invalidi(self, kw):
        base = dict(KW)
        base.update(kw)
        r = calcola_strategia_offerta(serie([100.0] * 24), **base)
        assert not r["valido"] and r["errore"]

    def test_quota_volume_100(self):
        r = calcola_strategia_offerta(serie([1.0] * 12 + [10.0] * 12),
                                     potenza_mw=5.0, costo_marginale=5.0,
                                     quota_volume=100.0)
        assert r["valido"]
        assert r["politiche"]["volume"]["quota_venduta_pct"] == pytest.approx(100.0)

    def test_costo_marginale_negativo_valido(self):
        r = calcola_strategia_offerta(serie([100.0] * 24), potenza_mw=5.0,
                                     costo_marginale=-5.0, quota_volume=90.0)
        assert r["valido"]
        assert r["politiche"]["margine"]["marg_giorno_eur"] == pytest.approx(
            5.0 * 24 * 105.0, rel=1e-9)


class TestRegistryTab191:
    def test_tab191_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        assert "calcola_strategia_offerta" in src
        assert '"🎯 Strategia di offerta"' in src
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab191" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert "tab191" in withs
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert len(withs) == len(dvars) == 202
        keys = re.findall(r'key="(off191_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 5
