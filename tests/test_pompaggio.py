"""Test tab186 (stile pytest): pompaggio idroelettrico (arbitraggio day-ahead).

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.
"""

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_pompaggio")
calcola_pompaggio = _F["calcola_pompaggio"]

TZ = "Europe/Zurich"


def due_livelli(notti=1, p_basso=10.0, p_alto=100.0, start="2026-09-28"):
    """12h a p_basso + 12h a p_alto per `notti` giorni (inizio mezzanotte)."""
    vals = []
    for _ in range(notti):
        vals += [p_basso] * 12 + [p_alto] * 12
    idx = pd.date_range(start, periods=len(vals), freq="h", tz=TZ)
    return pd.Series(np.array(vals, dtype=float), index=idx, name="p")


def piatta(giorni, prezzo=100.0, start="2026-09-28"):
    idx = pd.date_range(start, periods=giorni * 24, freq="h", tz=TZ)
    return pd.Series(np.full(len(idx), prezzo), index=idx, name="p")


BASE = dict(pot_turbina_mw=5.0, pot_pompa_mw=5.0, capacita_mwh=10.0,
            eff_turbina=1.0, eff_pompa=1.0, livello_iniziale_pct=0.0,
            apporto_naturale_mw=0.0, vom_eur_mwh=0.0, soglia_pompaggio_pct=25.0)


class TestPompaggio:
    def test_due_livelli_numeri_a_mano(self):
        # 12h a 10 + 12h a 100, eff=1, C=10, P=5, bacino vuoto:
        # pompa H0,H1 (10 MWh a 10), genera H12,H13 (10 MWh a 100)
        r = calcola_pompaggio(due_livelli(1), **BASE)
        assert r["valido"] and r["errore"] is None
        assert r["energia_pompata_mwh"] == pytest.approx(10.0)
        assert r["energia_generata_mwh"] == pytest.approx(10.0)
        assert r["costo_pompaggio_eur"] == pytest.approx(100.0)
        assert r["ricavo_generazione_eur"] == pytest.approx(1000.0)
        assert r["ricavo_lordo_eur"] == pytest.approx(900.0)
        assert r["ricavo_netto_eur"] == pytest.approx(900.0)
        assert r["cicli_equivalenti"] == pytest.approx(1.0)
        assert r["spread_medio_catturato_eur_mwh"] == pytest.approx(90.0)
        assert r["ricavo_eur_mw_giorno"] == pytest.approx(180.0)
        assert r["ore_pompaggio"] == 2
        assert r["ore_generazione"] == 2
        assert r["livello_finale_pct"] == pytest.approx(0.0)
        assert r["round_trip"] == pytest.approx(1.0)
        assert r["giudizio"] == "ARBITRAGGIO VINCENTE"
        assert r["n_ore"] == 24 and r["n_giorni"] == 1

    def test_rendimenti_09(self):
        # eff 0.9/0.9: pompa 5+5+1.111=11.111 MWh (costo 111.11),
        # genera 5.0+4.0=9.0 MWh (ricavo 900) -> netto 788.89
        kw = dict(BASE, eff_turbina=0.9, eff_pompa=0.9)
        r = calcola_pompaggio(due_livelli(1), **kw)
        assert r["valido"]
        assert r["energia_pompata_mwh"] == pytest.approx(11.111111, rel=1e-6)
        assert r["energia_generata_mwh"] == pytest.approx(9.0)
        assert r["costo_pompaggio_eur"] == pytest.approx(111.111111, rel=1e-6)
        assert r["ricavo_generazione_eur"] == pytest.approx(900.0)
        assert r["ricavo_netto_eur"] == pytest.approx(788.888889, rel=1e-6)
        assert r["round_trip"] == pytest.approx(0.81)
        assert r["breakeven_spread_pct"] == pytest.approx((1 / 0.81 - 1) * 100)
        assert r["giudizio"] == "ARBITRAGGIO VINCENTE"

    def test_prezzi_piatti_non_conviene(self):
        # 24h a 50, eff=1, VOM=2: 13 pompaggi (65 MWh) e 11 generazioni
        # (55 MWh) alternati -> lordo -500, VOM 240, netto -740
        kw = dict(BASE, vom_eur_mwh=2.0)
        r = calcola_pompaggio(piatta(1, prezzo=50.0), **kw)
        assert r["valido"]
        assert r["energia_pompata_mwh"] == pytest.approx(65.0)
        assert r["energia_generata_mwh"] == pytest.approx(55.0)
        assert r["ricavo_lordo_eur"] == pytest.approx(-500.0)
        assert r["vom_totale_eur"] == pytest.approx(240.0)
        assert r["ricavo_netto_eur"] == pytest.approx(-740.0)
        assert r["livello_finale_pct"] == pytest.approx(100.0)
        assert r["giudizio"] == "NON CONVIENE"

    def test_apporto_naturale(self):
        # 12h a 10 + 12h a 100, apporto 1 MWh/h, C=100:
        # ore economiche: L += 6/h -> 72; ore care: L -= 4/h -> 24 finale
        kw = dict(BASE, capacita_mwh=100.0, apporto_naturale_mw=1.0)
        r = calcola_pompaggio(due_livelli(1), **kw)
        assert r["valido"]
        assert r["energia_pompata_mwh"] == pytest.approx(60.0)
        assert r["energia_generata_mwh"] == pytest.approx(60.0)
        assert r["costo_pompaggio_eur"] == pytest.approx(600.0)
        assert r["ricavo_generazione_eur"] == pytest.approx(6000.0)
        assert r["ricavo_netto_eur"] == pytest.approx(5400.0)
        assert r["livello_finale_pct"] == pytest.approx(24.0)
        assert r["cicli_equivalenti"] == pytest.approx(0.6)

    def test_livello_iniziale_netto_zero(self):
        # 24h a 100, bacino al 50% (5 MWh gratis): pompa e genera a turno
        # a pari prezzo -> netto esattamente 0 -> NON CONVIENE (serve > 0)
        kw = dict(BASE, livello_iniziale_pct=50.0)
        r = calcola_pompaggio(piatta(1, prezzo=100.0), **kw)
        assert r["valido"]
        assert r["energia_pompata_mwh"] == pytest.approx(60.0)
        assert r["energia_generata_mwh"] == pytest.approx(60.0)
        assert r["ricavo_netto_eur"] == pytest.approx(0.0)
        assert r["giudizio"] == "NON CONVIENE"

    def test_df_giornaliera_coerente(self):
        r = calcola_pompaggio(due_livelli(2), **BASE)
        assert r["valido"] and r["n_giorni"] == 2
        dfg = r["df_giornaliera"]
        assert len(dfg) == 2
        for c in ["Giorno", "Ricavo generazione (EUR)", "Costo pompaggio (EUR)",
                  "Ricavo netto (EUR)", "Energia generata (MWh)",
                  "Energia pompata (MWh)", "Cicli"]:
            assert c in dfg.columns
        assert dfg["Ricavo generazione (EUR)"].sum() == pytest.approx(
            r["ricavo_generazione_eur"])
        assert dfg["Costo pompaggio (EUR)"].sum() == pytest.approx(
            r["costo_pompaggio_eur"])
        assert (dfg["Ricavo netto (EUR)"]
                == dfg["Ricavo generazione (EUR)"] - dfg["Costo pompaggio (EUR)"]).all()
        dfo = r["df_oraria"]
        assert len(dfo) == 48
        assert set(dfo["Azione"].unique()) <= {"Pompaggio", "Generazione", "Fermo"}
        assert (dfo["Livello bacino (MWh)"] >= 0).all()
        assert (dfo["Livello bacino (MWh)"] <= 10.0 + 1e-9).all()

    def test_parametri_non_validi(self):
        p = due_livelli(1)
        assert not calcola_pompaggio(p, **dict(BASE, pot_turbina_mw=-1.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, pot_pompa_mw=0.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, capacita_mwh=0.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, eff_turbina=0.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, eff_turbina=1.5))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, eff_pompa=-0.1))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, livello_iniziale_pct=101.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, livello_iniziale_pct=-1.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, apporto_naturale_mw=-1.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, vom_eur_mwh=-0.5))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, soglia_pompaggio_pct=0.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, soglia_pompaggio_pct=50.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, soglia_pompaggio_pct=60.0))["valido"]
        assert not calcola_pompaggio(p, **dict(BASE, pot_turbina_mw=True))["valido"]

    def test_serie_vuota(self):
        s = pd.Series([], dtype=float, index=pd.DatetimeIndex([], tz=TZ))
        r = calcola_pompaggio(s, **BASE)
        assert not r["valido"] and r["errore"]

    def test_non_series(self):
        r = calcola_pompaggio([100.0] * 24, **BASE)
        assert not r["valido"] and r["errore"]

    def test_nan_tz_duplicati(self):
        s = due_livelli(2)
        s.iloc[5] = np.nan
        s.iloc[30] = np.nan
        r = calcola_pompaggio(s, **BASE)
        assert r["valido"] and r["n_ore"] == 46
        s2 = due_livelli(1)
        s2.index = s2.index.tz_localize(None)
        r2 = calcola_pompaggio(s2, **BASE)
        assert r2["valido"] and r2["n_ore"] == 24
        s3 = pd.concat([due_livelli(1), due_livelli(1)])
        r3 = calcola_pompaggio(s3, **BASE)
        assert r3["valido"] and r3["n_ore"] == 24  # duplicati keep-first

    def test_determinismo(self):
        p = due_livelli(3)
        kw = dict(BASE, apporto_naturale_mw=2.0, vom_eur_mwh=1.5)
        a = calcola_pompaggio(p, **kw)
        b = calcola_pompaggio(p, **kw)
        assert a["ricavo_netto_eur"] == b["ricavo_netto_eur"]
        assert a["giudizio"] == b["giudizio"]
        pd.testing.assert_frame_equal(a["df_oraria"], b["df_oraria"])
        pd.testing.assert_frame_equal(a["df_giornaliera"], b["df_giornaliera"])


class TestRegistryTab186:
    def test_tab186_registrata(self):
        import re
        from pathlib import Path
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab186" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab186" in withs
        assert len(withs) == len(dvars) == 196
        assert '"🏔️ Pompaggio"' in src
        assert "calcola_pompaggio" in src
        keys = re.findall(r'key="(pmp186_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 10
